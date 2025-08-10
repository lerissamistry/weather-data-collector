import argparse
import csv
import datetime as dt
import os
from typing import Dict, Any, Tuple

import requests

UA = "WeatherDataCollectorMini/1.0 (educational demo)"

def geocode(city: str) -> Tuple[float, float, str]:
    """Return (lat, lon, resolved_name) using Open-Meteo Geocoding."""
    r = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
        headers={"User-Agent": UA},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json() or {}
    results = data.get("results") or []
    if not results:
        raise RuntimeError(f"No results for city '{city}'. Try a more specific name.")
    top = results[0]
    return float(top["latitude"]), float(top["longitude"]), str(top["name"])

def current_weather(lat: float, lon: float) -> Dict[str, Any]:
    """Return current weather for the given coordinates from Open-Meteo."""
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True},
        headers={"User-Agent": UA},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json() or {}
    cur = data.get("current_weather")
    if not cur:
        raise RuntimeError("Missing 'current_weather' in response.")
    return cur

def save_csv(row: Dict[str, Any], path: str) -> str:
    fields = ["city", "latitude", "longitude", "temperature_c", "windspeed", "winddirection", "weathercode", "ts_utc"]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            w.writeheader()
        w.writerow(row)
    return os.path.abspath(path)

def main():
    parser = argparse.ArgumentParser(description="Fetch current weather for a city and save to CSV (Open-Meteo).")
    parser.add_argument("--city", default="London")
    args = parser.parse_args()

    lat, lon, resolved = geocode(args.city)
    cur = current_weather(lat, lon)

    row = {
        "city": resolved,
        "latitude": lat,
        "longitude": lon,
        "temperature_c": cur.get("temperature"),
        "windspeed": cur.get("windspeed"),
        "winddirection": cur.get("winddirection"),
        "weathercode": cur.get("weathercode"),
        "ts_utc": dt.datetime.utcnow().isoformat(),
    }

    date_str = dt.date.today().strftime("%Y-%m-%d")
    out = save_csv(row, f"data/weather_{date_str}.csv")
    print(f"Saved: {out}")

if __name__ == "__main__":
    main()
