from dataclasses import dataclass
from datetime import datetime

@dataclass
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: datetime = datetime.now()

    def to_dict(self):
        return {
            'operation': self.operation,
            'a': self.a,
            'b': self.b,
            'result': self.result,
            'timestamp': self.timestamp.isoformat(),
        }
