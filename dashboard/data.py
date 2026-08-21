from db.connection import get_connection

def get_team_options() -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, fullName FROM teams ORDER BY fullName")
    teams = cursor.fetchall()

    conn.close()

    teams = [{'label': row[1], 'value': row[0]} for row in teams]

    return teams

def get_season_options() -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT season FROM games ORDER BY season")
    seasons = cursor.fetchall()

    conn.close()

    seasons = [{'label': f"{str(row[0])[:4]}-{str(row[0])[6:8]}", 'value': row[0]} for row in seasons] # Want them to look like 2024-25

    return seasons

def get_event_type_options() -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT event_type FROM plays WHERE x_coord IS NOT NULL AND y_coord IS NOT NULL ORDER BY event_type")
    event_types = cursor.fetchall()

    conn.close()

    event_types = [{'label': str(row[0]).replace("-", " "), 'value': row[0]} for row in event_types]

    return event_types

def get_event_location(team_id, season, event_type) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.x_coord, p.y_coord
        FROM plays p
        JOIN games g ON p.game_id = g.game_id
        WHERE p.team_id = ?
            AND g.season = ?
            AND p.event_type = ?
            AND p.x_coord IS NOT NULL
    """, (team_id, season, event_type))

    rows = cursor.fetchall()
    conn.close()

    return rows

if __name__ == "__main__":
    print(get_event_location(21, 20252026, 'goal'))