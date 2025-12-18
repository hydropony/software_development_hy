
# Class keeps track of first and second player points and the number of draws.
class Referee:
    def __init__(self):
        self.first_player_points = 0
        self.second_player_points = 0
        self.draws = 0

    def record_move(self, first_move, second_move):
        if self._is_draw(first_move, second_move):
            self.draws = self.draws + 1
        elif self._first_wins(first_move, second_move):
            self.first_player_points = self.first_player_points + 1
        else:
            self.second_player_points = self.second_player_points + 1

    def __str__(self):
        return f"Score: {self.first_player_points} - {self.second_player_points}\nDraws: {self.draws}"

    # internal method to check if there was a draw
    def _is_draw(self, first, second):
        if first == second:
            return True

        return False

    # internal method to check if first player beats second
    def _first_wins(self, first, second):
        if first == "r" and second == "s":
            return True
        elif first == "s" and second == "p":
            return True
        elif first == "p" and second == "r":
            return True

        return False
