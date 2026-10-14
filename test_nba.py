import requests

url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
data = requests.get(url, timeout=10).json()

events = data.get("events", [])
print(f"{len(events)} games on the current scoreboard\n")

for e in events[:5]:
    comp = e["competitions"][0]
    teams = [f'{c["team"]["abbreviation"]} {c.get("score", "")}' for c in comp["competitors"]]
    print(e["date"], "|", " vs ".join(teams), "|", e["status"]["type"]["description"])