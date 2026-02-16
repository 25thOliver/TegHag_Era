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