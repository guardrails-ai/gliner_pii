from typing import Any, Callable, Dict, Optional, Tuple

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
    ErrorSpan,
)

from gliner import GLiNER


@register_validator(name="guardrails/gliner_pii", data_type="string")
class GlinerPII(Validator):
    DEFAULT_ENTITIES = [
        "date",
        "time",
        "city",
        "state",
        "country",
        "zip code",
        "location",
        "name",
        "person",
        "phone number",
        "driver license",
    ]
    """Validates that the input string contains no personally identifiable information (PII) based on the provided entities.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `guardrails/gliner_pii`           |
    | Supported data types          | `string`                          |
    | Programmatic fix              | Anonymizes the text by replacing PII with placeholders. |

    Args:
        entities (list[str]): A list of entities that the model should detect.
        model (str): The name of the GLiNER model to use. Defaults to "urchade/gliner_medium-v2.1".
    """  # noqa

    def __init__(
        self,
        entities: list[str] = DEFAULT_ENTITIES,
        model: str = "urchade/gliner_medium-v2.1",
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail, entities=entities, model=model)
        self.entities = entities
        self.model = GLiNER.from_pretrained(model)

    def anonymize(self, text: str, entities: list[str]) -> Tuple[str, list[ErrorSpan]]:
        predictions = self.model.predict_entities(text, entities)

        error_spans = [
            ErrorSpan(start=p["start"], end=p["end"], reason=p["label"])
            for p in predictions
        ]

        anonymized_text = text
        for span in sorted(error_spans, key=lambda x: x.start, reverse=True):
            start, end, entity = span.start, span.end, span.reason
            entity_name = entity.replace(" ", "_").upper()
            anonymized_text = (
                f"{anonymized_text[:start]}<{entity_name}>{anonymized_text[end:]}"
            )

        return anonymized_text, error_spans

    def validate(self, value: Any, metadata: Dict = {}) -> ValidationResult:
        entities = metadata.get("entities", self.entities)
        if entities is None:
            raise ValueError(
                "`entities` must be set in order to use the `GlinerPII` validator."
            )

        anonymized_text, error_spans = self.anonymize(text=value, entities=entities)

        if len(error_spans) == 0:
            return PassResult()
        else:
            return FailResult(
                error_message=f"The following text contains PII:\n{value}",
                fix_value=anonymized_text,
                error_spans=error_spans,
            )
