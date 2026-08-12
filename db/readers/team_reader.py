from db.connection import get_connection

def get_team_abbrevs() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT abbrev FROM teams")
    abbrevs = [row[0] for row in cursor.fetchall()]

    conn.close()
    return abbrevs