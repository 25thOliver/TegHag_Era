import os
import json
from api_client import APIClient
from config import TEAM_ID, SEASON, COMPETITIONS, RAW_MATCHES_DIR

def fetch_team_matches(team_id: int, season: int, competitions: list):
    client = APIClient()
    all_matches = []

    # Fetch all fixtures for the team & season in a single call,
    # then filter by competition IDs and finished status.
    params = {
        "team": team_id,
        "season": season,
    }
    data = client.get("fixtures", params=params)
    matches = data.get("response", [])

    print(f"Request params (single call): {params}")
    print(f"Total matches in API response: {len(matches)}")

    filtered = [
        m for m in matches
        if m["league"]["id"] in competitions and m["fixture"]["status"]["short"] == "FT"
    ]
    print(f"Kept {len(filtered)} finished matches in target competitions")
    all_matches.extend(filtered)

    return all_matches

def save_matches(matches):
    for match in matches:
        match_id = match["fixture"]["id"]
        file_path = os.path.join(RAW_MATCHES_DIR, f"{match_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(match, f, indent=2)
    print(f"Saved {len(matches)} matches to {RAW_MATCHES_DIR}")
 
if __name__ == "__main__":
    matches = fetch_team_matches(TEAM_ID, SEASON, COMPETITIONS)
    save_matches(matches)