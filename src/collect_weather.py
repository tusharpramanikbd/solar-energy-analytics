
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

    # Collect weather data
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        raw_df = pd.DataFrame(response.json()["daily"])

    except (requests.exceptions.RequestException, ValueError, KeyError) as error:
        raise RuntimeError(f"Weather data collection failed: {error}") from error

    # Prepare structured DataFrame
    weather_df = pd.DataFrame({
        "date": pd.to_datetime(raw_df["time"], format="%Y-%m-%d"),
        "city": "Vaasa",
        "temperature_mean_c": raw_df["temperature_2m_mean"],
        "cloud_cover_mean_pct": raw_df["cloud_cover_mean"],
        "sunshine_hours": (raw_df["sunshine_duration"] / 3600).round(2)
    })

    # Validate weather data
    if len(weather_df) != 366:
        raise ValueError("Unexpected number of weather records.")

    if weather_df.isna().any().any():
        raise ValueError("Missing values found in weather data.")

    if weather_df["date"].duplicated().any():
        raise ValueError("Duplicate dates found in weather data.")

    if not weather_df["cloud_cover_mean_pct"].between(0, 100).all():
        raise ValueError("Invalid cloud cover values.")

    if not weather_df["sunshine_hours"].between(0, 24).all():
        raise ValueError("Invalid sunshine duration values.")

    return weather_df
