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
    path = tmp_path/'h.json'
    # Use the new method
    c.save_json_history()
    # Optionally, load to verify
    c.load_json_history()
    assert len(c.history.list()) > 0