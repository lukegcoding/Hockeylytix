from db.connection import get_connection
from getters.get_playbyplay import parse_plays

def upsert_play(cursor, play):
    cursor.execute("""
        MERGE plays AS target
        USING (SELECT ? AS game_id, ? AS api_event_id) AS source
        ON target.game_id = source.game_id AND target.api_event_id = source.api_event_id
        WHEN MATCHED THEN
            UPDATE SET
                period = ?, period_time = ?, time_remaining = ?, event_type = ?,
                team_id = ?, x_coord = ?, y_coord = ?, zone_code = ?, shot_type = ?,
                reason = ?, situation_code = ?, away_score = ?, home_score = ?, sort_order = ?
        WHEN NOT MATCHED THEN
            INSERT (game_id, api_event_id, period, period_time, time_remaining, event_type,
                    team_id, x_coord, y_coord, zone_code, shot_type, reason, situation_code,
                    away_score, home_score, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        OUTPUT INSERTED.event_id;
    """, (
        play['game_id'], play['api_event_id'],
        play['period'], play['period_time'], play['time_remaining'], play['event_type'],play['team_id'], play['x_coord'], play['y_coord'], 
        play['zone_code'], play['shot_type'], play['reason'], play['situation_code'], play['away_score'], play['home_score'], play['sort_order'],

        play['game_id'], play['api_event_id'],
        play['period'], play['period_time'], play['time_remaining'], play['event_type'],play['team_id'], play['x_coord'], play['y_coord'], 
        play['zone_code'], play['shot_type'], play['reason'], play['situation_code'], play['away_score'], play['home_score'], play['sort_order'],
    ))

    return cursor.fetchone()[0]

def upsert_play_player(cursor, event_id, player_id, role):
    cursor.execute(""" 
        MERGE play_players AS target
        USING (SELECT ? AS event_id, ? AS player_id, ? AS role) AS source
        ON target.event_id = source.event_id
            AND target.player_id = source.player_id
            AND target.role = source.role
        WHEN NOT MATCHED THEN
            INSERT (event_id, player_id, role) VALUES (?, ?, ?);
        """, (event_id, player_id, role, event_id, player_id, role))

def load_games_plays(pbp):
    conn = get_connection()
    cursor = conn.cursor()

    plays = parse_plays(pbp)

    for play in plays:
        players = play.pop("_players")
        event_id = upsert_play(cursor, play)
        for p in players:
            upsert_play_player(cursor, event_id, p['player_id'], p['role'])

    conn.commit()
    conn.close()
    print(f"Loaded {len(plays)} plays for game {pbp['id']}")

if __name__ == "__main__":
    from getters.get_playbyplay import get_play_by_play
    pbp = get_play_by_play(2024020001)
    load_games_plays(pbp)