class AI:
    def __init__(self):
        self._move = 0

    def get_move(self):
        self._move = self._move + 1
        self._move = self._move % 3

        if self._move == 0:
            return "r"
        elif self._move == 1:
            return "p"
        else:
            return "s"

    def set_move(self, move):
        # does nothing
        pass
