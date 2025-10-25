import sys, os, json
from datetime import datetime
from colorama import init, Fore

from .operations import get_operation
from .input_validators import validate_number
from .calculation import Calculation
from .history import History
from .logger_observers import LoggingObserver, AutoSaveObserver
from .calculator_config import get_config
from .logger import logger

init(autoreset=True)

_cfg = get_config()
os.makedirs(_cfg['LOG_DIR'], exist_ok=True)
os.makedirs(_cfg['HISTORY_DIR'], exist_ok=True)

HISTORY_JSON_PATH = os.path.join(_cfg['HISTORY_DIR'], 'history.json')

class Calculator:
    def __init__(self):
        self.history = History()
        self.observers = []
        if _cfg.get('AUTO_SAVE', False):
            self.register_observer(AutoSaveObserver())
        self.register_observer(LoggingObserver())
        self.load_json_history()

    def register_observer(self, obs):
        if obs not in self.observers:
            self.observers.append(obs)

    def notify(self, calc):
        for obs in self.observers:
            try:
                obs.notify(calc)
            except Exception as e:
                logger.error(f"Observer failed: {e}")

    def calculate(self, op_name, a_raw, b_raw=None):
        a = validate_number(a_raw)
        b = validate_number(b_raw) if b_raw is not None else None
        op = get_operation(op_name)
        result = op.execute(a, b)
        result = round(result, _cfg.get('PRECISION', 2))
        calc = Calculation(op_name, a, b if b is not None else 0, result, datetime.now())
        self.history.push(calc)
        self.notify(calc)
        self.safe_save_history()
        return calc

    def safe_save_history(self):
        try:
            self.save_json_history()
        except Exception as e:
            logger.error(f"Failed to save history: {e}")

    def save_json_history(self):
        data = [c.to_dict() for c in self.history.list()]
        with open(HISTORY_JSON_PATH, 'w', encoding=_cfg['ENCODING']) as f:
            json.dump(data, f, indent=2)

    def load_json_history(self):
        if not os.path.exists(HISTORY_JSON_PATH):
            return
        try:
            with open(HISTORY_JSON_PATH, 'r', encoding=_cfg['ENCODING']) as f:
                data = json.load(f)
            for r in data:
                try:
                    c = Calculation(
                        r['operation'],
                        float(r.get('a', 0)),
                        float(r.get('b', 0)),
                        float(r.get('result', 0)),
                        datetime.now()
                    )
                    self.history.push(c)
                except (KeyError, ValueError, TypeError):
                    logger.warning("Skipping invalid record in history.json")
        except Exception as e:
            logger.error(f"Failed to load history.json: {e}")

    # --- Test hooks for non-interactive coverage ---
    def _test_command(self, command, *args):
        command = command.lower()
        if command == 'clear':
            self.history.clear()
            return 'cleared'
        elif command == 'undo':
            return 'undo' if self.history.undo() else 'nothing_to_undo'
        elif command == 'redo':
            return 'redo' if self.history.redo() else 'nothing_to_redo'
        elif command == 'save':
            self.save_json_history()
            return 'saved'
        elif command == 'load':
            self.load_json_history()
            return 'loaded'
        elif command == 'history':
            return [h.to_dict() for h in self.history.list()]
        else:
            a, b = (args + (None, None))[:2]
            calc = self.calculate(command, a, b)
            return calc.result

def repl():  # pragma: no cover
    calc = Calculator()
    print(Fore.CYAN + 'Advanced Calculator REPL (type "help" for commands)')

    while True:
        try:
            cmd = input(Fore.YELLOW + '> ').strip()
            if not cmd:
                continue
            parts = cmd.split()
            command = parts[0].lower()

            if command in ('exit', 'quit'):
                print(Fore.CYAN + 'Goodbye!')
                break
            elif command == 'help':
                print(Fore.CYAN + 'Commands: add, subtract, multiply, divide, power, root, modulus, '
                      'int_divide, percent, abs_diff, sin, cos, tan, log, ln, exp, abs, history, '
                      'clear, undo, redo, save, load, help, exit')
            else:
                args = parts[1:]
                if command == 'history':
                    for i, c in enumerate(calc.history.list(), 1):
                        print(Fore.GREEN + f'{i}. {c.operation}({c.a},{c.b}) = {c.result} at {c.timestamp}')
                elif command in ('clear', 'undo', 'redo', 'save', 'load'):
                    res = calc._test_command(command, *args)
                    print(Fore.CYAN + f'{command.title()} executed.')
                else:
                    if len(args) not in (1, 2):
                        print(Fore.RED + 'Usage: <operation> <a> [b]')
                        continue
                    res = calc._test_command(command, *args)
                    print(Fore.GREEN + f'Result: {res}')
        except Exception as e:
            logger.error(str(e))
            print(Fore.RED + f'Error: {e}')

if __name__ == '__main__':  # pragma: no cover
    repl()
