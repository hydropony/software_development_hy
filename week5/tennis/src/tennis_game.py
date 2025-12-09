class TennisGame:
    SCORE_NAMES = {
        0: "Love",
        1: "Fifteen",
        2: "Thirty",
        3: "Forty"
    }

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1

    def get_score(self):
        if self._is_tied():
            return self._get_tied_score()
        if self._is_endgame():
            return self._get_endgame_score()
        return self._get_regular_score()

    def _is_tied(self):
        return self.player1_score == self.player2_score

    def _is_endgame(self):
        return self.player1_score >= 4 or self.player2_score >= 4

    def _get_tied_score(self):
        if self.player1_score >= 3:
            return "Deuce"
        return f"{self.SCORE_NAMES[self.player1_score]}-All"

    def _get_endgame_score(self):
        difference = self.player1_score - self.player2_score
        leader = "player1" if difference > 0 else "player2"

        if abs(difference) == 1:
            return f"Advantage {leader}"
        return f"Win for {leader}"

    def _get_regular_score(self):
        player1_score = self.SCORE_NAMES[self.player1_score]
        player2_score = self.SCORE_NAMES[self.player2_score]
        return f"{player1_score}-{player2_score}"
