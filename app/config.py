import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API-Football config
API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

# Manchester United team ID (API-Football)
# Based on live API probing, season 2022 has fixtures
# in Premier League with league ID 39.
TEAM_ID = 33
SEASON = 2022  # First full season under Ten Hag
COMPETITIONS = [39]  # Premier League

# Output Path
RAW_MATCHES_DIR = os.path.join("data", "raw", "matches")

os.makedirs(RAW_MATCHES_DIR, exist_ok=True)