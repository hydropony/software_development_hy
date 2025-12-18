from referee import Referee
from ai_enhanced import ImprovedAI
from rps import RockPaperScissors

class RPSImprovedAI(RockPaperScissors):
    def __init__(self):
        super().__init__()
        self.ai = ImprovedAI(10)

    def _second_move(self, first_move):
        move = self.ai.get_move()
        self.ai.set_move(first_move)
        return move