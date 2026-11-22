
import pandas as pd

# Calculate monthly solar irradiation totals for descriptive analysis.
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

# Predict daily solar irradiation using a 7-day moving average.
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

# Evaluate prediction accuracy using Mean Absolute Error (MAE).
def calculate_prediction_mae(prediction_df):
    errors = (
        prediction_df["solar_irradiation_kwh_m2_day"]
        - prediction_df["predicted_irradiation_kwh_m2_day"]
    ).abs()

    return errors.mean()

# Summarize seasonal solar irradiation to support energy planning recommendations.
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

# Calculate the three annual KPIs for solar irradiation, sunshine, and cloud cover.
def calculate_kpis(df):
    kpi_df = pd.DataFrame([
        {
            "measure": "Average Daily Solar Irradiation",
            "value": round(df["solar_irradiation_kwh_m2_day"].mean(), 2),
            "unit": "kWh/m²/day",
            "target": "Not defined",
            "source": "NASA POWER",
            "frequency": "2024 Annual Average"
        },
        {
            "measure": "Average Daily Sunshine Duration",
            "value": round(df["sunshine_hours"].mean(), 2),
            "unit": "hours/day",
            "target": "Not defined",
            "source": "Open-Meteo",
            "frequency": "2024 Annual Average"
        },
        {
            "measure": "Average Cloud Cover",
            "value": round(df["cloud_cover_mean_pct"].mean(), 2),
            "unit": "%",
            "target": "Not defined",
            "source": "Open-Meteo",
            "frequency": "2024 Annual Average"
        }
    ])

    return kpi_df

# Calculate monthly averages for the three KPI visualizations.
def calculate_monthly_kpis(df):
    monthly_df = df.copy()

    monthly_df["month"] = monthly_df["date"].dt.month

    monthly_df = monthly_df.groupby("month", as_index=False).agg(
        avg_solar_irradiation=("solar_irradiation_kwh_m2_day", "mean"),
        avg_sunshine_hours=("sunshine_hours", "mean"),
        avg_cloud_cover=("cloud_cover_mean_pct", "mean")
    )

    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    monthly_df["month"] = monthly_df["month"].map(
        dict(enumerate(months, start=1))
    )

    return monthly_df

# Calculate the correlation between cloud cover and solar irradiation.
def calculate_cloud_irradiation_correlation(df):
    correlation = df["cloud_cover_mean_pct"].corr(
        df["solar_irradiation_kwh_m2_day"]
    )

    return correlation
