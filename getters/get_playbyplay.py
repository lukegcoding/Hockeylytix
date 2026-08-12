import requests

def get_play_by_play(game_id: int) -> dict:
    response = requests.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play")
    return response.json()

ROLE_FIELD_MAP = {
    "hittingPlayerId": "Hitter",
    "hitteePlayerId": "Hittee",
    "scoringPlayerId": "Scorer",
    "assist1PlayerId": "Assist1",
    "assist2PlayerId": "Assist2",
    "shootingPlayerId": "Shooter",
    "goalieInNetId": "Goalie",
    "blockingPlayerId": "Blocker",
    "winningPlayerId": "Winner",
    "losingPlayerId": "Loser",
    "committedByPlayerId": "PenaltyOn",
    "drawnByPlayerId": "DrawnBy",
    "playerId": "Involved",
}

def parse_plays(pbp: dict) -> list:
    """
    Returns a list of dicts, one per play, each with a '_players' key
    holding a list of {player_id, role} for that event.
    """
    game_id = pbp["id"]
    plays = []

    for ev in pbp["plays"]:
        details = ev.get("details", {})

        play = {
            "game_id": game_id,
            "api_event_id": ev["eventId"],
            "period": ev["periodDescriptor"]["number"],
            "period_time": ev["timeInPeriod"],
            "time_remaining": ev["timeRemaining"],
            "event_type": ev["typeDescKey"],
            "team_id": details.get("eventOwnerTeamId"),
            "x_coord": details.get("xCoord"),
            "y_coord": details.get("yCoord"),
            "zone_code": details.get("zoneCode"),
            "shot_type": details.get("shotType"),
            "reason": details.get("reason"),
            "situation_code": ev.get("situationCode"),
            "away_score": details.get("awayScore"),
            "home_score": details.get("homeScore"),
            "sort_order": ev["sortOrder"],
        }

        players = []
        for field, role in ROLE_FIELD_MAP.items():
            player_id = details.get(field)
            if player_id is not None:
                players.append({"player_id": player_id, "role": role})

        play["_players"] = players
        plays.append(play)

    return plays

if __name__ == "__main__":
    pbp = get_play_by_play(2025021174)
    plays = parse_plays(pbp)

    print(f"Parsed {len(plays)} plays")
    print(plays[18])
        