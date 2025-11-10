import requests
from player import Player

class PlayerReader():
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        response = response.json()

        players = []

        for player_dict in response:
            player = Player(player_dict)
            players.append(player)

        return players

    def dummy_method(self):
        pass
