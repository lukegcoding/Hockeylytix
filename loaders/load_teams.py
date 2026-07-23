import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "getters"))

from get_teams import get_current_teams
from db import get_connection

def insert_teams(df):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True

    rows = [tuple(row) for row in df[["id", "franchiseId", "fullName", "triCode"]].itertuples(index=False)]

    cursor.executemany(
        "INSERT INTO teams (id, franchiseId, fullName, abbrev) VALUES (?, ?, ?, ?)", 
        rows
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    teams_df = get_current_teams()
    insert_teams(teams_df)
    print(f"Inserted {len(teams_df)} teams.")
