import pytest
from app.operations import get_operation, OperationError

@pytest.mark.parametrize('op,a,b,expected', [
    ('add', 1, 2, 3),
    ('subtract', 5, 3, 2),
    ('multiply', 2, 4, 8),
    ('power', 2, 3, 8),
    ('root', 27, 3, 3),
    ('modulus', 10, 3, 1),
    ('int_divide', 7, 2, 3),
    ('percent', 50, 200, 25),
    ('abs_diff', 5, 2, 3),
])
def test_ops(op,a,b,expected):
    o = get_operation(op)
    assert o.execute(a,b) == expected

def test_divide_zero():
    o = get_operation('divide')
    with pytest.raises(Exception):
        o.execute(1,0)
