import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 40.034147,
    "longitude": -75.119198,
    "hourly": "temperature_2m",
    "temperature_unit": "fahrenheit",
    "forecast_days": 1,
}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()
data = response.json()

times = data["hourly"]["time"]
temps = data["hourly"]["temperature_2m"]

for t, temp in list(zip(times, temps))[:6]:
    print(t, temp)

print(f"Pulled {len(temps)} hourly readings")