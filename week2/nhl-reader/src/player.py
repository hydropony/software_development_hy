class Player:
    def __init__(self, in_dict):
        self.name = in_dict['name']
        self.team = in_dict['team']
        self.goals = in_dict['goals']
        self.assists = in_dict['assists']
        self.nationality = in_dict['nationality']

    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:<3} + {self.assists:<3} = {self.goals+self.assists}"

    def dummy_method(self):
        pass
