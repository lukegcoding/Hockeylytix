import pandas as pd
import requests

def get_current_teams() -> pd.DataFrame:
    """
    Pulls all NHL teams from the /team endpoint,
    then filters down to only the teams currently active and renames UHC to Utah Mammoth.
    """

    response = requests.get("https://api.nhle.com/stats/rest/en/team")
    json_data = response.json()

    all_teams_df = pd.DataFrame(json_data["data"])

    nhl_teams = [
            "Anaheim Ducks",
            "Boston Bruins",
            "Buffalo Sabres",
            "Calgary Flames",
            "Carolina Hurricanes",
            "Chicago Blackhawks",
            "Colorado Avalanche",
            "Columbus Blue Jackets",
            "Dallas Stars",
            "Detroit Red Wings",
            "Edmonton Oilers",
            "Florida Panthers",
            "Los Angeles Kings",
            "Minnesota Wild",
            "Montréal Canadiens",
            "Nashville Predators",
            "New Jersey Devils",
            "New York Islanders",
            "New York Rangers",
            "Ottawa Senators",
            "Philadelphia Flyers",
            "Pittsburgh Penguins",
            "San Jose Sharks",
            "Seattle Kraken",
            "St. Louis Blues",
            "Tampa Bay Lightning",
            "Toronto Maple Leafs",
            "Utah Hockey Club",
            "Vancouver Canucks",
            "Vegas Golden Knights",
            "Washington Capitals",
            "Winnipeg Jets"
        ]

    current_teams_df = all_teams_df[all_teams_df["fullName"].isin(nhl_teams)].copy()

    current_teams_df["fullName"] = current_teams_df["fullName"].replace({
        "Utah Hockey Club": "Utah Mammoth",
        "Montréal Canadiens": "Montreal Canadiens",
    })

    current_teams_df = current_teams_df.sort_values(by="fullName")

    current_teams_df = current_teams_df[["id", "franchiseId", "fullName", "triCode"]]

    current_teams_df = current_teams_df.sort_values(by="fullName", ignore_index=True)

    return current_teams_df

if __name__ == "__main__":
    teams_df = get_current_teams()
    teams_df.to_csv("data/teams.csv", index=False)
    print(f"Saved {len(teams_df)} teams to teams.csv")