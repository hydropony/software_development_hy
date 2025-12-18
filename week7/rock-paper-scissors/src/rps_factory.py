from rps_ai import RPSAI
from rps_pvp import RPSPlayerVsPlayer
from rps_enhanced_ai import RPSImprovedAI


def create_game(type):
    if type == 'a':
        return RPSPlayerVsPlayer()
    if type == 'b':
        return RPSAI()
    if type == 'c':
        return RPSImprovedAI()

    return None
