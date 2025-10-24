import sys, os, json
from .operations import get_operation
from .input_validators import validate_number
from .calculation import Calculation
from .history import History
from .logger_observers import LoggingObserver, AutoSaveObserver
from .calculator_config import get_config
from .logger import logger
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

_cfg = get_config()
os.makedirs(_cfg['LOG_DIR'], exist_ok=True)
os.makedirs(_cfg['HISTORY_DIR'], exist_ok=True)

HISTORY_JSON_PATH = os.path.join(_cfg['HISTORY_DIR'], 'history.json')

class Calculator:
    def __init__(self):
        self.history = History()
        self.observers = []
        if _cfg['AUTO_SAVE']:
            self.register_observer(AutoSaveObserver())
        self.register_observer(LoggingObserver())
        self.load_json_history()

    def register_observer(self, obs): self.observers.append(obs)
    def notify(self, calc):
        for o in self.observers: o.notify(calc)

    def calculate(self, op_name, a_raw, b_raw=None):
        a = validate_number(a_raw)
        b = validate_number(b_raw) if b_raw is not None else None
        op = get_operation(op_name)
        result = op.execute(a, b)
        result = round(result, _cfg['PRECISION'])
        calc = Calculation(op_name, a, b if b is not None else 0, result, datetime.now())
        self.history.push(calc)
        self.notify(calc)
        self.save_json_history()
        return calc

    def save_json_history(self):
        data = [c.to_dict() for c in self.history.list()]
        with open(HISTORY_JSON_PATH, 'w', encoding=_cfg['ENCODING']) as f:
            json.dump(data, f, indent=2)

    def load_json_history(self):
        if os.path.exists(HISTORY_JSON_PATH):
            try:
                with open(HISTORY_JSON_PATH, 'r', encoding=_cfg['ENCODING']) as f:
                    data = json.load(f)
                for r in data:
                    c = Calculation(r['operation'], float(r['a']), float(r['b']), float(r['result']), datetime.now())
                    self.history.push(c)
            except Exception as e:
                logger.error(f'Failed to load history.json: {e}')

# Enhanced REPL

def repl():
    calc = Calculator()
    print(Fore.CYAN + 'Advanced Calculator REPL (type "help" for commands)')

    while True:
        try:
            cmd = input(Fore.YELLOW + '> ').strip()
            if not cmd: continue
            parts = cmd.split()
            command = parts[0].lower()

            if command in ('exit', 'quit'):
                print(Fore.CYAN + 'Goodbye!')
                break
            elif command == 'help':
                print(Fore.CYAN + 'Commands: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff, sin, cos, tan, log, ln, exp, abs, history, clear, undo, redo, save, load, help, exit')
            elif command == 'history':
                for i, c in enumerate(calc.history.list(), 1):
                    print(Fore.GREEN + f'{i}. {c.operation}({c.a},{c.b}) = {c.result} at {c.timestamp}')
            elif command == 'clear':
                calc.history.clear()
                print(Fore.CYAN + 'History cleared.')
            elif command == 'undo':
                res = calc.history.undo()
                print(Fore.CYAN + ('Undo performed.' if res is not None else 'Nothing to undo.'))
            elif command == 'redo':
                res = calc.history.redo()
                print(Fore.CYAN + ('Redo performed.' if res is not None else 'Nothing to redo.'))
            elif command in ('save','load'):
                calc.save_json_history() if command=='save' else calc.load_json_history()
                print(Fore.CYAN + f'History {command}d.')
            else:
                # operation
                args = parts[1:]
                if len(args) not in (1,2):
                    print(Fore.RED + 'Usage: <operation> <a> [b]')
                    continue
                c = calc.calculate(command, args[0], args[1] if len(args)==2 else None)
                print(Fore.GREEN + f'Result: {c.result}')

        except Exception as e:
            logger.error(str(e))
            print(Fore.RED + f'Error: {e}')

if __name__ == '__main__':
    repl()
