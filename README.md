# Overview

| Developed by | Guardrails AI |
| --- | --- |
| Date of development | Feb 15, 2024 |
| Validator type | Format |
| Blog |  |
| License | Apache 2 |
| Input/Output | Output |

## Description

### Intended Use

GLiNER (Generalist Model for Named Entity Recognition using Bidirectional Transformer) is a novel approach to named entity recognition that employs a small bidirectional transformer encoder and parallel entity extraction [^1]. This model has demonstrated strong performance, outperforming both ChatGPT and fine-tuned LLMs in zero-shot evaluations on various NER benchmarks. It's worth noting that most GLiNER models tend to perform optimally when entity types are in lowercase or title case.



### Requirements

* Dependencies:
	- guardrails-ai>=0.4.0
	- gliner

## Installation

```bash
$ guardrails hub install hub://guardrails/gliner_pii
```

## Usage Examples

### Validating string output via Python

In this example, we apply the validator to a string output generated by an LLM.

```python
# Import Guard and Validator
from guardrails.hub import GlinerPII
from guardrails import Guard

# Setup Guard
guard = Guard().use(
    GlinerPII
)

guard.validate("Today is a great day.")  # Validator passes
guard.validate("This is my phone number is 1234567890")  # Validator fails
```


# API Reference

**`__init__(self, on_fail="noop")`**
<ul>
Initializes a new instance of the GlinerPII class.

**Parameters**
- **`entities`** *(list[str])*: A list of entities that the model should detect.
- **`model`** *(str)*: The name of the GLiNER model to use. Defaults to `"urchade/gliner_medium-v2.1".`
- **`on_fail`** *(str, Callable)*: The policy to enact when a validator fails.  If `str`, must be one of `reask`, `fix`, `filter`, `refrain`, `noop`, `exception` or `fix_reask`. Otherwise, must be a function that is called when the validator fails.
</ul>
<br/>

**`validate(self, value, metadata) -> ValidationResult`**
<ul>
Validates the given `value` using the rules defined in this validator, relying on the `metadata` provided to customize the validation process. This method is automatically invoked by `guard.parse(...)`, ensuring the validation logic is applied to the input data.

Note:

1. This method should not be called directly by the user. Instead, invoke `guard.parse(...)` where this method will be called internally for each associated Validator.
2. When invoking `guard.parse(...)`, ensure to pass the appropriate `metadata` dictionary that includes keys and values required by this validator. If `guard` is associated with multiple validators, combine all necessary metadata into a single dictionary.

**Parameters**
- **`value`** *(Any):* The input value to validate.
- **`metadata`** *(dict):* A dictionary containing metadata required for validation. Keys and values must match the expectations of this validator.

    | Key | Type | Description | Default |
    | --- | --- | --- | --- |
    | `entities` | _Optional[List[str]]_ | A list of entities that the model should detect. If not provided, the validator will use the entities specified during initialization. | None |
</ul>

# References

[^1]: Urchade Zaratiana, Pierre Holat, Nadi Tomeh, & Thierry Charnois. (2023). GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer. arXiv. https://arxiv.org/abs/2311.08526
