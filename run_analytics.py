
from getpass import getpass
from pathlib import Path

from src.database import connect_mysql
from src.analytics import (
    load_analytics_data,
    calculate_monthly_irradiation,
    calculate_solar_predictions,
    calculate_prediction_mae,
    calculate_seasonal_irradiation,
    calculate_kpis,
    calculate_monthly_kpis
)

from src.plots import (
    plot_monthly_irradiation,
    plot_solar_predictions,
    plot_monthly_kpis
)


def main():
    # Step 1: Load analytics data from MySQL
    username = input("MySQL Username: ")
    password = getpass("MySQL Password: ")

    connection = connect_mysql(username, password)

    try:
        df = load_analytics_data(connection)
    finally:
        connection.close()

    print(f"Analytics records loaded: {len(df)}")

    # Step 2: Descriptive Analytics
    monthly_df = calculate_monthly_irradiation(df)
    plot_monthly_irradiation(monthly_df)
    print("Descriptive Analytics completed.")

    # Step 3: Predictive Analytics
    prediction_df = calculate_solar_predictions(df)
    plot_solar_predictions(prediction_df)
    print(f"Predictive records calculated: {len(prediction_df)}")

    mae = calculate_prediction_mae(prediction_df)
    print(f"Prediction MAE: {mae:.4f} kWh/m²/day")

    print("Predictive Analytics completed.")

    # Step 4: Prepare Power BI Data
    seasonal_df = calculate_seasonal_irradiation(monthly_df)

    output_dir = Path(__file__).resolve().parent / "exports"
    output_dir.mkdir(exist_ok=True)

    seasonal_df.to_csv(
        output_dir / "seasonal_solar_irradiation_2024.csv",
        index=False
    )

    print("Power BI seasonal data exported successfully.")

    # Step 5: Calculate and export KPIs
    kpi_df = calculate_kpis(df)

    kpi_table = kpi_df.T

    kpi_table.columns = [
        "Solar Irradiation",
        "Sunshine Duration",
        "Cloud Cover"
    ]

    kpi_table.index = [
        "Measure", "Value", "Unit",
        "Target", "Source", "Frequency"
    ]

    kpi_table.to_excel(output_dir / "kpi_summary_2024.xlsx")

    print(kpi_df.to_string(index=False))
    print("KPI summary exported successfully.")

    # Step 6: Generate KPI Visualizations
    monthly_kpi_df = calculate_monthly_kpis(df)
    plot_monthly_kpis(monthly_kpi_df)

    print("KPI visualizations generated successfully.")

    print("All analytics completed successfully!")


if __name__ == "__main__":
    main()
