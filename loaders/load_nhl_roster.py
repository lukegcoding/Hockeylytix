from db.connection import get_connection
from getters.get_playbyplay import parse_roster_spots

def game_roster_already_loaded(cursor, game_id) -> bool:
    cursor.execute("SELECT TOP 1 player_id FROM nhl_roster where game_id = ?", (game_id,))
    return cursor.fetchone() is not None

def stub_player_if_missing(cursor, player_id, first_name, last_name):
    cursor.execute("""
        MERGE players as target
        USING (SELECT ? AS id) AS source
        ON target.id = source.id
        WHEN NOT MATCHED THEN
            INSERT (id, firstName, lastName) VALUES (?, ?, ?);
    """, (player_id, player_id, first_name, last_name))

def upsert_nhl_roster_row(cursor, row):
    cursor.execute("""
        MERGE nhl_roster AS target
        USING (SELECT ? AS game_id, ? AS player_id) AS source
        ON target.game_id = source.game_id AND target.player_id = source.player_id
        WHEN NOT MATCHED THEN
            INSERT (game_id, player_id, team_id, jersey_number, position_code)
            VALUES (?, ?, ?, ?, ?);
    """, (
        row["game_id"], row["player_id"],
        row["game_id"], row["player_id"], row["team_id"], row["jersey_number"], row["position_code"]
    ))

def load_game_roster(pbp):
    conn = get_connection()
    cursor = conn.cursor()

    game_id = pbp["id"]

    if game_roster_already_loaded(cursor, game_id):
            print(f"Skipping game {game_id} -- roster already loaded")
            conn.close()
            return

    roster = parse_roster_spots(pbp)

    for row in roster:
        stub_player_if_missing(cursor, row["player_id"], row["first_name"], row["last_name"])
        upsert_nhl_roster_row(cursor, row)

    conn.commit()
    conn.close()
    print(f"Loaded {len(roster)} roster spots for game {pbp['id']}")

if __name__ == "__main__":
    from getters.get_playbyplay import get_play_by_play
    pbp = get_play_by_play(2024020001)
    load_game_roster(pbp)