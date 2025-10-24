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
    calc.calculate('add', 2, 3)
    path = tmp_path / 'history.json'
    calc.save_json_history(path)
    calc.load_json_history(path)
    assert len(calc.history.list()) == 1
