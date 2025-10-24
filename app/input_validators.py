from .exceptions import ValidationError
from .calculator_config import get_config

_cfg = get_config()

def validate_number(x):
    try:
        val = float(x)
    except Exception:
        raise ValidationError(f'Invalid numerical input: {x}')
    if abs(val) > _cfg['MAX_INPUT']:
        raise ValidationError(f'Input {val} exceeds max allowed {_cfg["MAX_INPUT"]}')
    return val
