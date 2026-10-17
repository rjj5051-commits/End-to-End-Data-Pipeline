import json
import sys
import time
from pathlib import Path


import requests

BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
RAW_DIR = Path("data/raw/scoreboard")
REGULAR_SEASON_2024_2025__START = "20241022"
REGULAR_SEASON_2024_2025___END = "20250413"

def fetch_scoreboard(date_str):
    """Fetch one day of NBA scoreboard data. date_str is YYYYMMDD."""
    response = requests.get(BASE_URL, params = {"dates": date_str}, timeout = 30)
    response.raise_for_status() #Checks the HTTP status code. So if ESPN returns a 400 or 500, this throws an error. Without it if there was an error, the code would save it as if there was data
    return response.json() # Parses the JSON text into a Python dictionary and hands it back


def save_scoreboard(date_str,payload):
    """Save the data points that we've fetch."""
    RAW_DIR.mkdir(parents=True, exist_ok=True) #creates the folder if it’s missing
    file_path = RAW_DIR / f"{date_str}.json"
    with open(file_path, "w") as f:
        json.dump(payload, f, indent=2)


def ingest_date(date_str):
    """Fetch and save one date. Returns True if it saved, False otherwise."""
    file_path = RAW_DIR / f"{date_str}.json"
    if file_path.exists():
        print(f"skip {date_str}: already exists and is saved")
        return False

    try:
        data = fetch_scoreboard(date_str)
    except requests.RequestException as e:
        print(f"Failed {date_str}: {e}")
        return False

    save_scoreboard(date_str, data)
    time.sleep(1)
    print(f"saved {date_str}: {len(data.get('events',[]))} events")
    return True

def load_calendar_dates(reference_file):
    """Read a saved scoreboard file and return its season calendar as YYYYMMDD strings"""
    with open(reference_file) as f:
        data = json.load(f)

    calendar = data["leagues"][0]["calendar"]
    
    dates = []
    for entry in calendar:
        dates.append(entry[:10].replace("-", ""))

    return dates


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ingest_date(sys.argv[1])
    else:
        dates = load_calendar_dates("data/raw/scoreboard/20250115.json")
        dates = [d for d in dates if REGULAR_SEASON_2024_2025__START <= d <= REGULAR_SEASON_2024_2025___END]
        saved = 0
        for date_str in dates:
            if ingest_date(date_str):
                saved += 1
        print(f"done: {saved} new, {len(dates) - saved} skipped or failed")


