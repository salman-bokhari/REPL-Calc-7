import pytest
from app.operations import get_operation
from app.exceptions import OperationError

def test_operations_errors():
    op = get_operation('divide')
    with pytest.raises(OperationError):
        op.execute(5, 0)

    op = get_operation('int_divide')
    with pytest.raises(OperationError):
        op.execute(5, 0)

    op = get_operation('modulus')
    with pytest.raises(OperationError):
        op.execute(5, 0)

    op = get_operation('root')
    with pytest.raises(OperationError):
        op.execute(-8, 2)

    op = get_operation('percent')
    with pytest.raises(OperationError):
        op.execute(5, 0)

    op = get_operation('log')
    with pytest.raises(OperationError):
        op.execute(0)
    with pytest.raises(OperationError):
        op.execute(-10)

    op = get_operation('ln')
    with pytest.raises(OperationError):
        op.execute(0)
    with pytest.raises(OperationError):
        op.execute(-5)
