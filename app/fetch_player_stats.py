import os
import json

from api_client import APIClient
from config import RAW_MATCHES_DIR, RAW_PLAYER_STATS_DIR

def load_fixtures_ids():
    # Read all match JSON files and collect unique fixture IDs
    fixture_ids = set()

    for filename in os.listdir(RAW_MATCHES_DIR):
        if not filename.endswith(".json"):
            continue

        path = os.path.join(RAW_MATCHES_DIR. filename)
        with open(path, "r", encoding="utf-8") as f:
            match = json.load(f)

        fixture_id = match["fixture"]["id"]
        fixture_ids.add(fixture_id)

    # Sort for consistent progress output
    return sorted(fixture_ids)