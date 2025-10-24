import pytest
from app.input_validators import validate_number
from app.calculator_config import get_config
from app.exceptions import OperationError

_cfg = get_config()

def test_valid_numbers():
    assert validate_number(10) == 10
    assert validate_number('20.5') == 20.5

def test_invalid_numbers():
    with pytest.raises(OperationError):
        validate_number('abc')

    with pytest.raises(OperationError):
        validate_number(_cfg['CALCULATOR_MAX_INPUT_VALUE'] + 1)
