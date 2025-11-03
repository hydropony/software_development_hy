import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
  def setUp(self):
    self.service = StatisticsService(PlayerReaderStub())

  def test_search(self):
     res: Player = self.service.search("Kurri")
     self.assertEqual(res.name, "Kurri")
     res: Player = self.service.search("James")
     self.assertEqual(res, None)

  def test_team(self):
     res: list[Player] = self.service.team("EDM")
     self.assertEqual(len(res), 3)

  def test_top_points(self):
     res: list[Player] = self.service.top(4)
     names = list(map(lambda x: x.name, res))
     self.assertEqual(names, ["Gretzky", "Lemieux", "Yzerman", "Kurri"])
  
  def test_top_goals(self):
     res: list[Player] = self.service.top(4, SortBy.GOALS)
     names = list(map(lambda x: x.name, res))
     self.assertEqual(names, ["Lemieux", "Yzerman", "Kurri", "Gretzky"])
  
  def test_top_assists(self):
     res: list[Player] = self.service.top(4, SortBy.ASSISTS)
     names = list(map(lambda x: x.name, res))
     self.assertEqual(names, ["Gretzky", "Yzerman", "Lemieux", "Kurri"])
  