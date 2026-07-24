import pandas as pd

from db.connection import get_connection
from db.readers.team_reader import get_team_abbrevs
from getters.get_players import get_team_roster

#Doesn't totally work yet (Need to debug being able to see how many new players were added)

def upsert_players(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        params = (
            row["id"],
            row["firstName"], row["lastName"], row["position"], row["shoots"],
            row["height"], row["weight"], row["birthdate"], row["birthCity"],
            row["birthCountry"], row["birthState"],
            row["id"], 
            row["firstName"], row["lastName"], row["position"], row["shoots"],
            row["height"], row["weight"], row["birthdate"], row["birthCity"],
            row["birthCountry"], row["birthState"],
        )

        params = [None if pd.isna(x) else x for x in params]

        cursor.execute("""
            MERGE players AS target
            USING (SELECT ? AS id) AS source
            ON target.id = source.id
            WHEN MATCHED THEN
                UPDATE SET
                    firstName = ?,
                    lastName = ?,
                    position = ?,
                    shoots = ?,
                    height = ?,
                    weight = ?,
                    birthdate = ?,
                    birthCity = ?,
                    birthCountry = ?,
                    birthState = ?
            WHEN NOT MATCHED THEN
                INSERT (id, firstName, lastName, position, shoots, height, weight, birthdate, birthCity, birthCountry, birthState)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, params)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    all_players = []
    for abbrev in get_team_abbrevs():
        team_df = get_team_roster(abbrev, "20242025")
        all_players.append(team_df)

    all_players_df = pd.concat(all_players, ignore_index=True)
    
    all_players_df.to_csv("data/all_players.csv")

    upsert_players(all_players_df)
    print(f"Upserted {len(all_players_df)} players.")
