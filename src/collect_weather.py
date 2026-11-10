
import requests
import pandas as pd


def collect_weather():
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": 63.096,
        "longitude": 21.616,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "daily": "temperature_2m_mean,cloud_cover_mean,sunshine_duration",
        "timezone": "UTC"
    }

    # Collect weather data from API
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        daily = response.json()["daily"]

    except (requests.exceptions.RequestException, ValueError, KeyError) as error:
        raise RuntimeError(f"Weather data collection failed: {error}") from error

    # Validate weather data
    fields = ["temperature_2m_mean", "cloud_cover_mean", "sunshine_duration"]

    if not daily["time"]:
        raise ValueError("Weather data is empty.")

    for field in fields:
        if len(daily[field]) != len(daily["time"]):
            raise ValueError(f"Data length mismatch: {field}")

        if any(value is None for value in daily[field]):
            raise ValueError(f"Missing values found: {field}")

    # Convert sunshine duration from seconds to hours
    sunshine_hours = [
        round(seconds / 3600, 2)
        for seconds in daily["sunshine_duration"]
    ]

    # Prepare structured DataFrame
    weather_df = pd.DataFrame({
        "date": daily["time"],
        "city": "Vaasa",
        "temperature_mean_c": daily["temperature_2m_mean"],
        "cloud_cover_mean_pct": daily["cloud_cover_mean"],
        "sunshine_hours": sunshine_hours
    })

    # Convert date column to datetime format
    weather_df["date"] = pd.to_datetime(weather_df["date"], format="%Y-%m-%d")

    return weather_df
