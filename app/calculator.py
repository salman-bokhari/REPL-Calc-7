import sys
from .operations import get_operation
from .input_validators import validate_number
from .calculation import Calculation
from .history import History
from .logger_observers import LoggingObserver, AutoSaveObserver
from .calculator_config import get_config
from .logger import logger
import pandas as pd
import os
from datetime import datetime

_cfg = get_config()
os.makedirs(_cfg['LOG_DIR'], exist_ok=True)
os.makedirs(_cfg['HISTORY_DIR'], exist_ok=True)

class Calculator:
    def __init__(self):
        self.history = History()
        self.observers = []
        if _cfg['AUTO_SAVE']:
            self.register_observer(AutoSaveObserver())
        self.register_observer(LoggingObserver())

    def register_observer(self, obs):
        self.observers.append(obs)

    def notify(self, calc):
        for o in self.observers:
            o.notify(calc)

    def calculate(self, op_name, a_raw, b_raw):
        a = validate_number(a_raw)
        b = validate_number(b_raw)
        op = get_operation(op_name)
        result = op.execute(a, b)
        # rounding per precision
        result = round(result, _cfg['PRECISION'])
        calc = Calculation(op_name, a, b, result, datetime.now())
        self.history.push(calc)
        self.notify(calc)
        return calc

    # persistence
    def save_history(self, path=None):
        p = path or os.path.join(_cfg['HISTORY_DIR'], _cfg['HISTORY_FILE'])
        rows = [c.to_dict() for c in self.history.list()]
        df = pd.DataFrame(rows)
        df.to_csv(p, index=False, encoding=_cfg['ENCODING'])
        return p

    def load_history(self, path=None):
        p = path or os.path.join(_cfg['HISTORY_DIR'], _cfg['HISTORY_FILE'])
        if not os.path.exists(p):
            raise FileNotFoundError(p)
        df = pd.read_csv(p, encoding=_cfg['ENCODING'])
        self.history.clear()
        for _, r in df.iterrows():
            # naive conversion
            c = Calculation(r['operation'], float(r['a']), float(r['b']), float(r['result']), datetime.now())
            self.history.push(c)
        return len(self.history.list())

# Simple REPL
def repl():
    calc = Calculator()
    print('Advanced Calculator REPL. type "help" for commands.')
    while True:
        try:
            cmd = input('> ').strip()
            if not cmd:
                continue
            parts = cmd.split()
            command = parts[0].lower()
            if command in ('exit', 'quit'):
                print('Goodbye!')
                break
            elif command == 'help':
                print('Commands: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff, history, clear, undo, redo, save, load, help, exit')
            elif command == 'history':
                for i, c in enumerate(calc.history.list(), 1):
                    print(f'{i}. {c.operation}({c.a},{c.b}) = {c.result} at {c.timestamp}')
            elif command == 'clear':
                calc.history.clear()
                print('History cleared.')
            elif command == 'undo':
                res = calc.history.undo()
                print('Undo performed.' if res is not None else 'Nothing to undo.')
            elif command == 'redo':
                res = calc.history.redo()
                print('Redo performed.' if res is not None else 'Nothing to redo.')
            elif command == 'save':
                path = calc.save_history()
                print(f'History saved to {path}')
            elif command == 'load':
                try:
                    cnt = calc.load_history()
                    print(f'Loaded {cnt} entries.')
                except FileNotFoundError:
                    print('No history file found.')
            else:
                # operation
                args = parts[1:]
                if len(args) != 2:
                    print('Usage: <operation> <a> <b>')
                    continue
                c = calc.calculate(command, args[0], args[1])
                print(f'Result: {c.result}')
        except Exception as e:
            logger.error(str(e))
            print(f'Error: {e}')

if __name__ == '__main__':
    repl()
