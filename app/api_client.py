import requests
import time
from config import API_KEY, BASE_URL

class APIClient:
    # Simple API-Football client

    def __init__(self):
        self.headers = {
            "x-apisports-key": API_KEY
        }

    def get(self, endpoint, params=None, max_retries=3):
        url = f"{BASE_URL}/{endpoint}"
        for attempt in range(max_retries):
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("Rate limit reached, sleeping 60s...")
                time.sleep(60)
            else:
                print(f"Error {response.status_code}: {response.text}")
                time.sleep(5)
        raise Exception(f"Failed API request after {max_retries} attempts: {url}")