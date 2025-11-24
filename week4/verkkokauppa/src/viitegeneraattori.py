class ReferenceGenerator:
    def __init__(self):
        self._next = 1

    def new(self):
        self._next = self._next + 1

        return self._next


reference_generator = ReferenceGenerator()
