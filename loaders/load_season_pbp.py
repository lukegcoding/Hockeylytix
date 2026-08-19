import time
from db.connection import get_connection
from getters.get_playbyplay import get_play_by_play
from loaders.load_playbyplay_bulk import load_games_plays_bulk
from loaders.load_nhl_roster import load_game_roster

def get_game_ids_for_season(season: int) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT game_id FROM games WHERE season = ? ORDER BY game_date", (season,))
    game_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return game_ids

def load_season_pbp(season: int, delay_seconds: float = 0.5):
    game_ids = get_game_ids_for_season(season)
    print(f"Loading {len(game_ids)} games for season {season}")

    succeeded, failed = 0, 0
    start = time.time()

    for i, game_id in enumerate(game_ids, 1):
        try:
            pbp = get_play_by_play(game_id)

            load_game_roster(pbp)
            load_games_plays_bulk(pbp)
            
            succeeded += 1
        except Exception as e:
            failed += 1
            print(f"FAILED game_id {game_id}: {e}")

        if i % 100 == 0:
            elapsed = time.time() - start
            print(f"  ...{i}/{len(game_ids)} processed ({elapsed:.0f}s elapsed)")

        time.sleep(delay_seconds)

    elapsed = time.time() - start
    print(f"\nDone in {elapsed/60:.1f} min -- {succeeded} succeeded, {failed} failed")

if __name__ == "__main__":
    load_season_pbp(20252026)