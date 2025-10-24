import pytest
from app.history import History
from app.calculation import Calculation
from datetime import datetime

def test_history_push_undo_redo():
    h = History()
    c1 = Calculation('add', 1, 1, 2, datetime.now())
    c2 = Calculation('add', 2, 2, 4, datetime.now())

    h.push(c1)
    h.push(c2)
    assert len(h.list()) == 2

    h.undo()
    assert len(h.list()) == 1

    h.redo()
    assert len(h.list()) == 2

    h.clear()
    assert len(h.list()) == 0

def test_history_boundaries():
    h = History()
    h.undo()  # undo on empty
    h.redo()  # redo on empty
    assert len(h.list()) == 0
