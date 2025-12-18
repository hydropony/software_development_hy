# "Remembering AI"
class ImprovedAI:
    def __init__(self, memory_size):
        self._memory = [None] * memory_size
        self._free_memory_index = 0

    def set_move(self, move):
        # if memory is full, forget the oldest element
        if self._free_memory_index == len(self._memory):
            for i in range(1, len(self._memory)):
                self._memory[i - 1] = self._memory[i]

            self._free_memory_index = self._free_memory_index - 1

        self._memory[self._free_memory_index] = move
        self._free_memory_index = self._free_memory_index + 1

    def get_move(self):
        if self._free_memory_index == 0 or self._free_memory_index == 1:
            return "r"

        last_move = self._memory[self._free_memory_index - 1]

        r = 0
        p = 0
        s = 0

        for i in range(0, self._free_memory_index - 1):
            if last_move == self._memory[i]:
                next_move = self._memory[i + 1]

                if next_move == "r":
                    r = r + 1
                elif next_move == "p":
                    p = p + 1
                else:
                    s = s + 1

        # Make move selection as follows:
        # - if rock is most common, always give paper
        # - if paper is most common, always give scissors
        # otherwise always give rock
        if r > p or r > s:
            return "p"
        elif p > r or p > s:
            return "s"
        else:
            return "r"

        # More efficient ways exist, but more on that later
        # Johdatus Tekoälyyn kurssilla!
