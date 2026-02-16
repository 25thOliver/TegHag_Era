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

        # dim_competitions
        cur.execute(
            """
            INSERT INTO dim_competitions (competition_id, name, country, season)
            VALUES (%s, %s, %s, %s)
            ON CONLICT (competition_id) DO UPDATE
              SET name = EXCLUDED.name,
                  country = EXCLUDED.country,
                  season = EXCLUDED.season
            """
            (league_id, league["name"], league.get("country", ""), season),
        )

        # dim_matches
        cur.execute(
            """
            INSERT INTO dim_matches (
                fixture_id,
                fixture_date,
                venue_id,
                venue_name,
                venue_city,
                league_id,
                league_name,
                season,
                round_name,
                referee,
                status_short,
                home_team_id,
                away_team_id,
                home_team_name,
                away_team_name
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (fixture_id) DO UPDATE
              SET fixture_date   = EXCLUDED.fixture_date,
                  venue_id       = EXCLUDED.venue_id,
                  venue_name     = EXCLUDED.venue_name,
                  venue_city     = EXCLUDED.venue_city,
                  league_id      = EXCLUDED.league_id,
                  league_name    = EXCLUDED.league_name,
                  season         = EXCLUDED.season,
                  round_name     = EXCLUDED.round_name,
                  referee        = EXCLUDED.referee,
                  status_short   = EXCLUDED.status_short,
                  home_team_id   = EXCLUDED.home_team_id,
                  away_team_id   = EXCLUDED.away_team_id,
                  home_team_name = EXCLUDED.home_team_name,
                  away_team_name = EXCLUDED.away_team_name;
            """,
            (
                fixture_id,
                fixture_date,
                venue.get("id"),
                venue.get("name"),
                venue.get("city"),
                league_id,
                league["name"],
                season,
                league.get("round"),
                fixture.get("referee"),
                status.get("short"),
                home["id"],
                away["id"],
                home["name"],
                away["name"],
            ),
        )

        # fact_team_match_stats (home + away)
        ht = score.get("halftime", {}) or {}
        home_goals = goals.get("home")
        away_goals = goals.get("away")

        # home row
        cur.execute(
            """
            INSERT INTO fact_team_match_stats (
                fixture_id,
                team_id,
                is_home,
                goals_for,
                goals_against,
                goals_halftime_for,
                goals_halftime_against,
                winner
            )
            VALUES (%s, %s, TRUE, %s, %s, %s, %s, %s)
            ON CONFLICT (fixture_id, team_id) DO UPDATE
              SET is_home             = EXCLUDED.is_home,
                  goals_for           = EXCLUDED.goals_for,
                  goals_against       = EXCLUDED.goals_against,
                  goals_halftime_for  = EXCLUDED.goals_halftime_for,
                  goals_halftime_against = EXCLUDED.goals_halftime_against,
                  winner              = EXCLUDED.winner;
            """,
            (
                fixture_id,
                home["id"],
                home_goals,
                away_goals,
                ht.get("home"),
                ht.get("away"),
                home.get("winner"),
            ),
        )

        # away row
        cur.execute(
            """
            INSERT INTO fact_team_match_stats (
                fixture_id,
                team_id,
                is_home,
                goals_for,
                goals_against,
                goals_halftime_for,
                goals_halftime_against,
                winner
            )
            VALUES (%s, %s, FALSE, %s, %s, %s, %s, %s)
            ON CONFLICT (fixture_id, team_id) DO UPDATE
              SET is_home             = EXCLUDED.is_home,
                  goals_for           = EXCLUDED.goals_for,
                  goals_against       = EXCLUDED.goals_against,
                  goals_halftime_for  = EXCLUDED.goals_halftime_for,
                  goals_halftime_against = EXCLUDED.goals_halftime_against,
                  winner              = EXCLUDED.winner;
            """,
            (
                fixture_id,
                away["id"],
                away_goals,
                home_goals,
                ht.get("away"),
                ht.get("home"),
                away.get("winner"),
            ),
        )

        if idx % 20 == 0:
            conn.commit()
            print(f"Loaded {idx} matches...")

    conn.commit()
    cur.close()
    conn.close()
    print("Finished loading matches + team facts.")