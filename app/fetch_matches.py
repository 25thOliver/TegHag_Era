import os
import json
from api_client import APIClient
from config import TEAM_ID, SEASON, COMPETITIONS, RAW_MATCHES_DIR

def fetch_team_matches(team_id: int, season: int, competitions: list):
    client = APIClient()
    all_matches = []

    for comp_id in competitions:
        page = 1
        while True:
            params = {
                "team": team_id,
                "season": season,
                "league": comp_id,
                "page": page
            }
            data = client.get("fixtures", params=params)
            matches = data.get("response", [])
            if not matches:
                break

            all_matches.extend(matches)
            print(f"Fetched {len(matches)} matches for compettition {comp_id} page {page}")
            page += 1

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