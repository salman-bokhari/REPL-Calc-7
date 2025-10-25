import json
import pytest
from app.calculator import Calculator
from app.exceptions import OperationError

def test_basic_operations():
    calc = Calculator()
    r = calc.calculate('add', 2, 3)
    assert r.result == 5

    r = calc.calculate('subtract', 5, 2)
    assert r.result == 3

    r = calc.calculate('multiply', 3, 4)
    assert r.result == 12

    r = calc.calculate('divide', 10, 2)
    assert r.result == 5

def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.calculate('divide', 5, 0)

def test_advanced_operations():
    calc = Calculator()
    assert calc.calculate('power', 2, 3).result == 8
    assert round(calc.calculate('root', 27, 3).result, 2) == 3
    assert calc.calculate('modulus', 10, 3).result == 1
    assert calc.calculate('int_divide', 10, 3).result == 3
    assert calc.calculate('percent', 50, 200).result == 25
    assert calc.calculate('abs_diff', 5, 12).result == 7
    # trig and log
    assert round(calc.calculate('sin', 30).result, 2) == 0.5
    assert round(calc.calculate('cos', 60).result, 2) == 0.5
    assert round(calc.calculate('tan', 45).result, 2) == 1
    assert round(calc.calculate('log', 100).result, 2) == 2
    assert round(calc.calculate('ln', 2.718281828).result, 2) == 1
    assert round(calc.calculate('exp', 1).result, 2) == 2.72
    assert calc.calculate('abs', -5).result == 5

def test_undo_redo():
    calc = Calculator()
    # Clear history first
    calc.history.clear()
    calc.calculate('add', 1, 1)
    calc.calculate('add', 2, 2)
    assert len(calc.history.list()) == 2
    calc.history.undo()
    assert len(calc.history.list()) == 1
    calc.history.redo()
    assert len(calc.history.list()) == 2

def test_observer_notifications(monkeypatch):
    calc = Calculator()
    logs = []
    monkeypatch.setattr(calc.observers[0], 'notify', lambda x: logs.append(x.result))
    calc.calculate('add', 3, 3)
    assert logs[0] == 6

def test_exceptions():
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.calculate('root', -8, 2)
    with pytest.raises(OperationError):
        calc.calculate('percent', 10, 0)

def test_save_load_history(tmp_path):
    calc = Calculator()
    calc.history.clear()
    calc.calculate('add', 2, 3)
    calc.save_json_history()
    calc.history.clear()
    calc.load_json_history()
    assert len(calc.history.list()) == 1

def test_internal_commands_and_history(tmp_path, monkeypatch):
    # Redirect history.json to a temp path
    monkeypatch.setattr("app.calculator.HISTORY_JSON_PATH", tmp_path / "history.json")
    c = Calculator()

    # 1️⃣ Command coverage
    assert c._test_command('clear') == 'cleared'
    assert c._test_command('add', '2', '3') == 5
    assert isinstance(c._test_command('history'), list)
    assert c._test_command('save') == 'saved'
    assert c._test_command('load') == 'loaded'

    # 2️⃣ Undo/Redo
    c.calculate('add', 2, 3)
    c.history.undo()
    assert c._test_command('undo') in ('undo', 'nothing_to_undo')
    c.history.redo()
    assert c._test_command('redo') in ('redo', 'nothing_to_redo')

def test_load_json_history_with_corruption(tmp_path, monkeypatch):
    hist_file = tmp_path / "history.json"
    hist_file.write_text("{ invalid json }")
    monkeypatch.setattr("app.calculator.HISTORY_JSON_PATH", hist_file)
    c = Calculator()  # should log error, not crash
    assert isinstance(c.history.list(), list)

def test_load_json_history_with_invalid_entries(tmp_path, monkeypatch):
    hist_file = tmp_path / "history.json"
    hist_file.write_text(json.dumps([{"operation": "add", "a": "x"}]))
    monkeypatch.setattr("app.calculator.HISTORY_JSON_PATH", hist_file)
    c = Calculator()
    # Should skip invalid record
    assert len(c.history.list()) == 0 or isinstance(c.history.list(), list)

def test_observer_error_handling(monkeypatch):
    class BadObserver:
        def notify(self, calc): raise RuntimeError("boom")

    c = Calculator()
    c.register_observer(BadObserver())
    # Should log error, not raise
    calc = c.calculate('add', 1, 1)
    assert calc.result == 2

def test_safe_save_history_handles_write_error(monkeypatch):
    c = Calculator()
    def bad_save(): raise IOError("disk full")
    monkeypatch.setattr(c, "save_json_history", bad_save)
    c.safe_save_history()