import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API-Football config
API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

# Manchester United team ID (API-Football)
# Based on live API probing, season 2022 has fixtures
# across multiple competitions for team 33.
TEAM_ID = 33
SEASON = 2022  # First full season under Ten Hag
# Filter to competitive matches: Premier League, FA Cup, League Cup, Europa League
COMPETITIONS = [39, 45, 48, 3]

# Output Path
RAW_MATCHES_DIR = os.path.join("data", "raw", "matches")

os.makedirs(RAW_MATCHES_DIR, exist_ok=True)