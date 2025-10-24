from .exceptions import OperationError
import math

class Operation:
    def execute(self, a, b):
        raise NotImplementedError()

class Add(Operation):
    def execute(self, a, b): 
        return a + b

class Subtract(Operation):
    def execute(self, a, b):
        return a - b

class Multiply(Operation):
    def execute(self, a, b):
        return a * b

class Divide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError('Division by zero')
        return a / b

class Power(Operation):
    def execute(self, a, b):
        return a ** b

class Root(Operation):
    def execute(self, a, b):
        # nth root of a: a ** (1/b). handle negative a with odd root
        if b == 0:
            raise OperationError('Root degree cannot be zero')
        if a < 0 and int(b) % 2 == 0:
            raise OperationError('Even root of negative number')
        return a ** (1.0 / b)

class Modulus(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError('Modulus by zero')
        return a % b

class IntDivide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError('Integer division by zero')
        return a // b

class Percent(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError('Percentage base cannot be zero')
        return (a / b) * 100.0

class AbsDiff(Operation):
    def execute(self, a, b):
        return abs(a - b)

# Factory
def get_operation(name):
    ops = {
        'add': Add(),
        'subtract': Subtract(),
        'multiply': Multiply(),
        'divide': Divide(),
        'power': Power(),
        'root': Root(),
        'modulus': Modulus(),
        'int_divide': IntDivide(),
        'percent': Percent(),
        'abs_diff': AbsDiff(),
    }
    op = ops.get(name)
    if op is None:
        raise OperationError(f'Unknown operation {name}')
    return op
