from getters.get_playbyplay import get_play_by_play
from loaders.load_playbyplay import load_games_plays
from loaders.load_nhl_roster import load_game_roster

def load_full_game(game_id):
    pbp = get_play_by_play(game_id)

    load_game_roster(pbp)
    load_games_plays(pbp)
    
if __name__ == "__main__":
    load_full_game(2024020001)