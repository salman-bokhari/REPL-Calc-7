from .calculation import Calculation
from .calculator_memento import Memento
from collections import deque
from datetime import datetime
from .calculator_config import get_config

_cfg = get_config()

class History:
    def __init__(self):
        self._items = []
        self._undo_stack = []
        self._redo_stack = []

    def push(self, calc: Calculation):
        self._items.append(calc)
        self._undo_stack.append(Memento(self._items))
        # clear redo on new action
        self._redo_stack.clear()
        # enforce max size
        if len(self._items) > _cfg['MAX_HISTORY']:
            self._items.pop(0)

    def list(self):
        return list(self._items)

    def clear(self):
        self._items.clear()
        self._undo_stack.clear()
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            return None
        # pop current state
        self._redo_stack.append(self._undo_stack.pop())
        if not self._undo_stack:
            self._items = []
            return None
        prev = self._undo_stack[-1].get_state()
        self._items = prev
        return self._items

    def redo(self):
        if not self._redo_stack:
            return None
        m = self._redo_stack.pop()
        self._undo_stack.append(m)
        self._items = m.get_state()
        return self._items
