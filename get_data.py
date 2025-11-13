import os
import requests
import pandas as pd
import numpy as np
import time


AQI_TOKEN = os.getenv("AQI_TOKEN")

if AQI_TOKEN is None:
    raise ValueError(
        "Missing AQI_TOKEN.\nSet it with:\n\n    export AQI_TOKEN='your_key_here'\n"
    )



NUM_POINTS = 250  

np.random.seed(42)
lats = np.random.uniform(25, 49, NUM_POINTS)
lons = np.random.uniform(-124, -66, NUM_POINTS)

locations = list(zip(lats, lons))



def get_air_quality(lat, lon):
    url = f"https://api.waqi.info/feed/geo:{lat:.4f};{lon:.4f}/?token={AQI_TOKEN}"
    r = requests.get(url)
    try:
        r.raise_for_status()
    except:
        print(f"Request failed for {lat}, {lon}")
        return None

    data = r.json()
    if data["status"] != "ok":
        return None

    d = data["data"]
    iaqi = d.get("iaqi", {})

    return {
        "lat": lat,
        "lon": lon,
        "station": d.get("city", {}).get("name"),
        "timestamp": d.get("time", {}).get("s"),
        "aqi": d.get("aqi"),
        "pm25": iaqi.get("pm25", {}).get("v"),
        "pm10": iaqi.get("pm10", {}).get("v"),
        "o3": iaqi.get("o3", {}).get("v"),
        "no2": iaqi.get("no2", {}).get("v"),
        "so2": iaqi.get("so2", {}).get("v"),
        "co": iaqi.get("co", {}).get("v"),
    }


def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "surface_pressure", "wind_speed_10m"]
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json().get("current", {})

    return {
        "temp": data.get("temperature_2m"),
        "humidity": data.get("relative_humidity_2m"),
        "pressure": data.get("surface_pressure"),
        "wind": data.get("wind_speed_10m"),
    }



def collect_data():
    rows = []

    for i, (lat, lon) in enumerate(locations):
        print(f"Collecting {i+1}/{NUM_POINTS} — lat={lat:.3f}, lon={lon:.3f}")

        aq = get_air_quality(lat, lon)
        if aq is None:
            continue

        wx = get_weather(lat, lon)

        row = {**aq, **wx}
        rows.append(row)

        time.sleep(1.0)  

    df = pd.DataFrame(rows)

    pollutant_cols = ["pm25", "pm10", "o3", "no2", "so2", "co", "aqi"]
    for col in pollutant_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df



if __name__ == "__main__":
    df = collect_data()

    print("\nCollected rows:", len(df))
    print(df.head())

    df.to_csv("air_quality_dataset.csv", index=False)
    print("\nSaved → air_quality_dataset.csv")
