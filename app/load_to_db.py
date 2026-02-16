import os
import json
from glob import glob

import psycopg2

from config import RAW_MATCHES_DIR, RAW_PLAYER_STATS_DIR

# DB connection config
DB_SETTINGS ={
    "host": "localhost",
    "port": 5432,
    "dbname": "foota_warehouse",
    "user": "foota",
    "password": "foota",
}

def get_connection():
    return psycopg2.connect(**DB_SETTINGS)

# Load Matches + Competitions + Team Facts 
def load_matches_and_teams():
    conn = get_connection()
    cur = conn.cursor()

    # Start fresh for each run
    cur.execute("TRUNCATE fact_team_match_stats RESTART IDENTITY CASCADE;")
    cur.execute("TRUNCATE dim_matches CASCADE;")
    cur.execute("TRUNCATE dim_competitions CASCADE;")
    conn.commit()

    match_files = sorted(glob(os.path.join(RAW_MATCHES_DIR, "*.json")))
    print(f"Found {len(match_files)} match files in {RAW_MATCHES_DIR}")

    for idx, path in enumerate(match_files, start=1):
        with open(path, "r", encoding="utf0-8") as f:
            m = json.load(f)

        fixture = m["fixture"]
        league = m["league"]
        teams = m["teams"]
        goals = m.get("goals", {})
        score = m.get("score", {})

        fixture_id = fixture["id"]
        fixture_date = fixture["date"]
        venue = fixture.get("venue", {}) or {}
        status = fixture.get("status", {}) or {}

        league_id = league["id"]
        season = league["season"]

        home = teams["home"]
        away = teams["away"]