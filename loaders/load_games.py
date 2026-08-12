import pandas as pd
from db.connection import get_connection
from db.readers.team_reader import get_team_abbrevs
from getters.get_season_games import get_season_games

def upsert_games(games_list):
    conn = get_connection()
    cursor = conn.cursor()

    inserted, updated, failed = 0, 0, 0

    for game in games_list:
        params = (
            game["game_id"], 
            game["season"], game["game_type"], game["game_date"], game["overtime"], game["home_team_id"],
            game["away_team_id"], game["home_score"], game["away_score"], game["game_state"],

            game["game_id"], 
            game["season"], game["game_type"], game["game_date"], game["overtime"], game["home_team_id"],
            game["away_team_id"], game["home_score"], game["away_score"], game["game_state"]
        )

        try:
            cursor.execute("""
            MERGE games AS target
            USING (SELECT ? AS game_id) AS source
            On target.game_id = source.game_id
            WHEN MATCHED THEN
                UPDATE SET
                season = ?, game_type = ?, game_date = ?, overtime = ?, home_team_id = ?, away_team_id = ?, home_score = ?, away_score = ?, game_state = ?
            WHEN NOT MATCHED THEN
                INSERT (game_id, season, game_type, game_date, overtime, home_team_id, away_team_id, home_score, away_score, game_state)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            OUTPUT $action;
            """, params)

            result = cursor.fetchone()
            if result[0] == "INSERT":
                inserted += 1
            else:
                updated += 1

        except Exception as e:
            failed += 1
            print(f"FAILED game_id {game['game_id']}: {e}")

    conn.commit()
    conn.close()
    print(f"Inserted {inserted}, updated {updated}, failed {failed}")

if __name__ == "__main__":
    season = "20262027"
    game_types = [2, 3]

    all_games = {}
    for abbrev in get_team_abbrevs():
        team_games = get_season_games(abbrev, season, game_types)
        for game in team_games:
            all_games[game["game_id"]] = game

    games_list = list(all_games.values())
    print(f"Found {len(games_list)} unique games")

    upsert_games(games_list)