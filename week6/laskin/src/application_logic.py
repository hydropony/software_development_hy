class ApplicationLogic:
    def __init__(self, value=0):
        self._value = value
        self._previous_value = value

    def subtract(self, operand):
        self._previous_value = self._value
        self._value = self._value - operand

    def add(self, operand):
        self._previous_value = self._value
        self._value = self._value + operand

    def reset(self):
        self._value = 0

    def undo(self):
        self._value, self._previous_value = self._previous_value, self._value

    def set_value(self, value):
        self._value = value

    def value(self):
        return self._value
