
import pandas as pd

def load_analytics_data(connection):
    query = """
        SELECT
            w.date,
            w.city,
            w.temperature_mean_c,
            w.cloud_cover_mean_pct,
            w.sunshine_hours,
            s.solar_irradiation_kwh_m2_day
        FROM solar_energy_analytics.weather_daily AS w
        INNER JOIN solar_energy_analytics.solar_daily AS s
            ON w.date = s.date AND w.city = s.city
        WHERE w.city = %s
        ORDER BY w.date
    """

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, ("Vaasa",))
        rows = cursor.fetchall()
    finally:
        cursor.close()

    analytics_df = pd.DataFrame(rows)

    if analytics_df.empty:
        raise ValueError("No matching analytics data found.")

    analytics_df["date"] = pd.to_datetime(analytics_df["date"])

    return analytics_df

def calculate_monthly_irradiation(df):
    monthly_df = df.copy()

    monthly_df["month"] = monthly_df["date"].dt.month

    monthly_df = monthly_df.groupby(
        "month", as_index=False
    )["solar_irradiation_kwh_m2_day"].sum()

    monthly_df = monthly_df.rename(columns={
        "solar_irradiation_kwh_m2_day": "total_irradiation_kwh_m2"
    })

    return monthly_df

def calculate_solar_predictions(df):
    prediction_df = df[[
        "date",
        "solar_irradiation_kwh_m2_day"
    ]].copy()

    prediction_df["predicted_irradiation_kwh_m2_day"] = (
        prediction_df["solar_irradiation_kwh_m2_day"]
        .shift(1)
        .rolling(window=7)
        .mean()
    )

    prediction_df = prediction_df.dropna().reset_index(drop=True)

    return prediction_df

def calculate_prediction_mae(prediction_df):
    errors = (
        prediction_df["solar_irradiation_kwh_m2_day"]
        - prediction_df["predicted_irradiation_kwh_m2_day"]
    ).abs()

    return errors.mean()


def calculate_seasonal_irradiation(monthly_df):
    seasonal_df = monthly_df.copy()

    seasons = {
        1: "Winter", 2: "Winter", 12: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    }

    seasonal_df["season"] = seasonal_df["month"].map(seasons)

    seasonal_df = (
        seasonal_df.groupby("season")["total_irradiation_kwh_m2"]
        .sum()
        .reindex(["Winter", "Spring", "Summer", "Autumn"])
        .reset_index()
    )

    return seasonal_df
