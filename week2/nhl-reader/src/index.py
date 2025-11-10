import requests
from player import Player
from playerReader import PlayerReader
from playerStats import PlayerStats

from rich.console import Console
from rich.table import Table

console = Console()

def print_players_table(players, title="Top NHL Players"):
    table = Table(title=title)
    table.add_column("Name", style="bold cyan")
    table.add_column("Team", style="magenta")
    table.add_column("G", justify="right")
    table.add_column("A", justify="right")
    table.add_column("Pts", justify="right")

    for p in players:
        name = getattr(p, "name", str(p))
        team = getattr(p, "team", "")
        goals = getattr(p, "goals", "")
        assists = getattr(p, "assists", "")
        points = (goals or 0) + (assists or 0)
        table.add_row(str(name), str(team), str(goals), str(assists), str(points))

    console.print(table)

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    while True:
        target_nat = input("Enter nationality code (e.g., 'FIN' for Finland) or 'q' to quit: ").strip().upper()
        players = stats.top_scorers_by_nationality(target_nat)
        if target_nat.lower() == 'q':
            break
        print_players_table(players, title="Top Finnish NHL Players")

if __name__ == "__main__":
    main()
