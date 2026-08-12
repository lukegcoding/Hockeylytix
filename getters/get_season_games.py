import requests
import pandas as pd


def get_season_games(team_abbrev: str, season: str, game_types: list) -> list:
    """
    Returns a list of dicts, one per game, containing everything the
    `games` table needs -- pulled from the schedule endpoint directly,
    no separate play-by-play call required for this data.
    """
    response = requests.get(f"https://api-web.nhle.com/v1/club-schedule-season/{team_abbrev}/{season}")
    json_data = response.json()

    games = []
    for game in json_data["games"]:
        if game["gameType"] not in game_types:
            continue

        games.append({
            "game_id": game["id"],
            "season": game["season"],
            "game_type": game["gameType"],
            "game_date": game["gameDate"],
            "overtime": game["gameOutcome"].get("lastPeriodType"),
            "home_team_id": game["homeTeam"]["id"],
            "away_team_id": game["awayTeam"]["id"],
            "home_score": game["homeTeam"].get("score"),
            "away_score": game["awayTeam"].get("score"),
            "game_state": game["gameState"],
        })

    return games


if __name__ == "__main__":
    from db.readers.team_reader import get_team_abbrevs

    season = "20262027"
    game_types = [2, 3] # [1] Preseason [2] Regular season [3] Playoffs

    all_games = {}
    for abbrev in get_team_abbrevs():
        team_games = get_season_games(abbrev, season, game_types)
        for game in team_games:
            all_games[game["game_id"]] = game

    games_list = list(all_games.values())

    all_game_ids_df = pd.DataFrame(games_list)

    all_game_ids_df.to_csv("data/game_ids_20252026.csv", index=False)

    print(f"Found {len(games_list)} unique games")