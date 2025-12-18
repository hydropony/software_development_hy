from referee import Referee
from ai import AI
from rps import RockPaperScissors


class RPSAI(RockPaperScissors):
    def __init__(self):
        super().__init__()
        self.ai = AI()
    
    def _second_move(self, first_move):
        return self.ai.get_move()