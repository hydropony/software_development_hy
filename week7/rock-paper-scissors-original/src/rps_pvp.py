from referee import Referee
from rps import RockPaperScissors

class RPSPlayerVsPlayer(RockPaperScissors):
    def _second_move(self, first_move):
        return input("Second player's move: ")
