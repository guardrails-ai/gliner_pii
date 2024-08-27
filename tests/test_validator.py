from guardrails import Guard
from validator import GlinerPII


guard = Guard.from_string(validators=[GlinerPII(on_fail="fix")])


def test_validator_success():
    TEST_OUTPUT = "This is my number"
    raw_output, guarded_output, *rest = guard.parse(TEST_OUTPUT)
    assert guarded_output == TEST_OUTPUT


def test_validator_fail():
    TEST_FAIL_OUTPUT = "This is my number is 1234567890"
    raw_output, guarded_output, *rest = guard.parse(TEST_FAIL_OUTPUT)
    assert guarded_output == "This is my number is <PHONE_NUMBER>"
