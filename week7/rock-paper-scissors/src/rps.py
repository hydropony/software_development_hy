from abc import abstractmethod
from referee import Referee

class RockPaperScissors:
    @abstractmethod
    def _second_move(self, first_move):
        raise Exception("This method must be overridden in a subclass")
    
    def __init__(self):
        print(
                "Game ends when a player makes an invalid move, i.e., something other than r, p, or s"
            )

    def play(self):
        referee = Referee()

        first_move = self._first_move()
        second_move = self._second_move(first_move)

        print(f"Computer chose: {second_move}")

        while self._is_valid_move(first_move) and self._is_valid_move(second_move):
            referee.record_move(first_move, second_move)
            print(referee)

            first_move = self._first_move()
            second_move = self._second_move(first_move)
            print(f"Computer chose: {second_move}")

        print("Thanks!")
        print(referee)

    def _first_move(self):
        return input("First player's move: ")

    def _is_valid_move(self, move):
        return move == "r" or move == "p" or move == "s"
