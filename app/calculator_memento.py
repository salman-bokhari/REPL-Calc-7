class Memento:
    def __init__(self, state):
        self._state = list(state)

    def get_state(self):
        return list(self._state)
