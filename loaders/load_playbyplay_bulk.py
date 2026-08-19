from db.connection import get_connection
from getters.get_playbyplay import parse_plays

def game_plays_already_loaded(cursor, game_id) -> bool:
    cursor.execute("SELECT TOP 1 event_id FROM plays WHERE game_id = ?", (game_id,))
    return cursor.fetchone() is not None

def bulk_insert_plays(cursor, plays):
    cursor.fast_executemany = True
    rows = [
        (
            play["game_id"], play["api_event_id"], play["period"], play["period_time"],
            play["time_remaining"], play["event_type"], play["team_id"], play["x_coord"],
            play["y_coord"], play["zone_code"], play["shot_type"], play["reason"],
            play["situation_code"], play["away_score"], play["home_score"], play["sort_order"],
        )
        for play in plays
    ]
    cursor.executemany("""
        INSERT INTO plays (game_id, api_event_id, period, period_time, time_remaining, event_type,
                            team_id, x_coord, y_coord, zone_code, shot_type, reason, situation_code,
                            away_score, home_score, sort_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

def fetch_event_id_map(cursor, game_id) -> dict:
    """Maps api_event_id -> the real event_id SQL Server generated, for one game"""
    cursor.execute("SELECT api_event_id, event_id FROM plays WHERE game_id = ?", (game_id,))
    return {row[0]: row[1] for row in cursor.fetchall()}

def bulk_insert_play_players(cursor, plays, event_id_map):
    cursor.fast_executemany = True

    rows = []

    for play in plays:
        event_id = event_id_map[play["api_event_id"]]
        for p in play["_players"]:
            rows.append((event_id, p["player_id"], p["role"]))

    cursor.executemany("""
        INSERT INTO play_players (event_id, player_id, role)
        VALUES (?, ?, ?)
    """, rows)

def load_games_plays_bulk(pbp):
    conn = get_connection()
    cursor = conn.cursor()

    game_id = pbp["id"]

    if game_plays_already_loaded(cursor, game_id):
        print(f"Skipping game {game_id} -- play by play already loaded")
        conn.close()
        return

    plays = parse_plays(pbp)
    bulk_insert_plays(cursor, plays)

    event_id_map = fetch_event_id_map(cursor, game_id)
    bulk_insert_play_players(cursor, plays, event_id_map)

    conn.commit()
    conn.close()
    print(f"Loaded {len(plays)} plays for game {game_id}")