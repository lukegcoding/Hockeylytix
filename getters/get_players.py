import pandas as pd
import requests

def get_team_roster(team_abbrev: str, season: str) -> pd.DataFrame:
    """
    Pulls one team's roster for one season from the NHL API, returning
    a dataframe of biographical player info -- no team/season columns.

    Example: get_team_roster("COL", "20212022")
    """

    response = requests.get(f"https://api-web.nhle.com/v1/roster/{team_abbrev}/{season}")
    json_data = response.json()

    all_players = json_data["forwards"] + json_data["defensemen"] + json_data["goalies"]
    df = pd.DataFrame(all_players)

    df["firstName"] = df["firstName"].apply(lambda x: x.get("default"))
    df["lastName"] = df["lastName"].apply(lambda x: x.get("default"))
    df["birthCity"] = df["birthCity"].apply(lambda x: x.get("default") if isinstance(x, dict) else None)
    df["birthState"] = df["birthStateProvince"].apply(
        lambda x: x.get("default") if isinstance(x, dict) else None
    )

    df = df.rename(columns={
        "positionCode": "position",
        "shootsCatches": "shoots",
        "heightInInches": "height",
        "weightInPounds": "weight",
        "birthDate": "birthdate",
    })

    df = df.sort_values(by="lastName", ignore_index=True)

    return df[[
        "id", "firstName", "lastName", "position", "shoots",
        "height", "weight", "birthdate", "birthCity", "birthCountry", "birthState",
    ]]

if __name__ == "__main__":
    players_df = get_team_roster("COL", "20222023")
    players_df.to_csv("data/players_COL_20252026.csv", index=False)
    print(f"Saved {len(players_df)} players to players_COL_20252026.csv")
