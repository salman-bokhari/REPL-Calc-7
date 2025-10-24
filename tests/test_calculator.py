import os
import pytest
from app.calculator import Calculator
from app.calculation import Calculation

def test_calculate_and_history(tmp_path):
    c = Calculator()
    res = c.calculate('add','2','3')
    assert res.result == 5
    assert len(c.history.list())==1

def test_save_and_load(tmp_path, monkeypatch):
    c = Calculator()
    c.calculate('add','2','3')
    path = tmp_path/'h.csv'
    c.save_history(path)
    assert os.path.exists(path)
    # load into new calculator
    c2 = Calculator()
    c2.load_history(path)
    assert len(c2.history.list())==1
