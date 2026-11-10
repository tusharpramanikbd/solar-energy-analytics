import requests

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 63.096,
    "longitude": 21.616,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "daily": "temperature_2m_mean,cloud_cover_mean,sunshine_duration",
    "timezone": "UTC"
}

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    daily = data["daily"]

    print("Total Records:", len(daily["time"]))

    print("Date:", daily["time"][0])
    print("Temperature:", daily["temperature_2m_mean"][0])
    print("Cloud Cover:", daily["cloud_cover_mean"][0])
    print("Sunshine Duration:", daily["sunshine_duration"][0])

    fields = ["temperature_2m_mean", "cloud_cover_mean", "sunshine_duration"]

    for field in fields:
        print(field, len(daily[field]) == len(daily["time"]))

    for field in fields:
        missing_count = sum(value is None for value in daily[field])
        print(f"{field}: {missing_count} missing values")

    sunshine_hours = [round(seconds / 3600, 2) for seconds in daily["sunshine_duration"]]

    print("Sunshine Hours:", sunshine_hours[0])

except requests.exceptions.RequestException as error:
    print(f"API Request Failed: {error}")

except ValueError as error:
    print(f"Invalid JSON Response: {error}")