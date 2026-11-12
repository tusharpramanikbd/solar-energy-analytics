
from pathlib import Path

import matplotlib.pyplot as plt


def plot_monthly_irradiation(monthly_df):
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    plt.figure(figsize=(10, 5))

    plt.bar(
        months,
        monthly_df["total_irradiation_kwh_m2"]
    )

    plt.title("Monthly Solar Irradiation in Vaasa (2024)")
    plt.xlabel("Month")
    plt.ylabel("Total Solar Irradiation (kWh/m²)")

    plt.tight_layout()

    output_dir = Path(__file__).resolve().parent.parent / "charts"
    output_dir.mkdir(exist_ok=True)

    plt.savefig(
        output_dir / "monthly_solar_irradiation_2024.png",
        dpi=200
    )

    plt.close()


def plot_solar_predictions(prediction_df):
    plt.figure(figsize=(12, 5))

    plt.plot(
        prediction_df["date"],
        prediction_df["solar_irradiation_kwh_m2_day"],
        label="Actual",
        alpha=0.6
    )

    plt.plot(
        prediction_df["date"],
        prediction_df["predicted_irradiation_kwh_m2_day"],
        label="Predicted (7-Day Moving Average)"
    )

    plt.title("Actual vs Predicted Solar Irradiation in Vaasa (2024)")
    plt.xlabel("Date")
    plt.ylabel("Daily Solar Irradiation (kWh/m²/day)")
    plt.legend()

    plt.tight_layout()

    output_dir = Path(__file__).resolve().parent.parent / "charts"
    output_dir.mkdir(exist_ok=True)

    plt.savefig(
        output_dir / "solar_irradiation_predictions_2024.png",
        dpi=200
    )

    plt.close()