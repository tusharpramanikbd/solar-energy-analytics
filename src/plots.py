
from pathlib import Path
import seaborn as sns
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

def plot_monthly_kpis(monthly_df):
    output_dir = Path(__file__).resolve().parent.parent / "charts"
    output_dir.mkdir(exist_ok=True)

    sns.set_theme(style="whitegrid")

    # KPI 1: Average Daily Solar Irradiation
    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=monthly_df,
        x="month",
        y="avg_solar_irradiation",
        ax=ax
    )

    ax.set_title("Monthly Average Daily Solar Irradiation - Vaasa 2024")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Irradiation (kWh/m²/day)")

    fig.tight_layout()
    fig.savefig(output_dir / "kpi_avg_daily_irradiation.png", dpi=200)
    plt.close(fig)

    # KPI 2: Average Daily Sunshine Duration
    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=monthly_df,
        x="month",
        y="avg_sunshine_hours",
        marker="o",
        sort=False,
        ax=ax
    )

    ax.set_title("Monthly Average Sunshine Duration - Vaasa 2024")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Sunshine (hours/day)")

    fig.tight_layout()
    fig.savefig(output_dir / "kpi_avg_sunshine_hours.png", dpi=200)
    plt.close(fig)

    # KPI 3: Average Cloud Cover
    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=monthly_df,
        x="month",
        y="avg_cloud_cover",
        marker="o",
        sort=False,
        ax=ax
    )

    ax.set_title("Monthly Average Cloud Cover - Vaasa 2024")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Cloud Cover (%)")
    ax.set_ylim(0, 100)

    fig.tight_layout()
    fig.savefig(output_dir / "kpi_avg_cloud_cover.png", dpi=200)
    plt.close(fig)
