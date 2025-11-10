from player import Player

class PlayerStats():
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, target_nationality):
        players: list[Player] = self.reader.get_players()
        players = filter((lambda x: x.nationality == target_nationality), players)
        players = sorted(players, key=(lambda x: x.goals + x.assists), reverse=True)
        return players

    def dummy_method(self):
        pass
