from pathlib import Path

from src.database import (
    connect_mysql,
    load_analytics_data,
    load_national_solar_data,
    load_pv_benchmark_data
)

from src.analytics import (
    calculate_monthly_irradiation,
    calculate_solar_predictions,
    calculate_prediction_mae,
    calculate_seasonal_irradiation,
    calculate_kpis,
    calculate_monthly_kpis,
    calculate_cloud_irradiation_correlation,
)

from src.plots import (
    plot_monthly_irradiation,
    plot_solar_predictions,
    plot_monthly_kpis,
    plot_solar_generation_trend,
    plot_cloud_irradiation_correlation,
    plot_pv_benchmark
)


def main():
    # Step 1: Establish database connection and load data
    connection = connect_mysql()

    try:
        df = load_analytics_data(connection)
        national_df = load_national_solar_data(connection)
        benchmark_df = load_pv_benchmark_data(connection)
    finally:
        connection.close()

    print(f"Analytics records loaded: {len(df)}")
    print(f"National solar records loaded: {len(national_df)}")
    print(national_df)

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
        output_dir / "prescriptive_seasonal_solar_irradiation_2024.csv",
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

    # Step 7: Trend Analysis
    plot_solar_generation_trend(national_df)

    print("Trend Analysis visualization generated successfully.")

    # Step 8: Correlation Analysis
    correlation = calculate_cloud_irradiation_correlation(df)

    plot_cloud_irradiation_correlation(df, correlation)

    print(f"Cloud Cover vs Solar Irradiation Correlation: {correlation:.4f}")
    print("Correlation visualization generated successfully.")

    # Step 9: Benchmarking
    plot_pv_benchmark(benchmark_df)
    print("PV Benchmarking visualization generated successfully.")


    # Step 10: Prepare Power BI Dashboard Data
    powerbi_df = df.copy()

    powerbi_df["month"] = powerbi_df["date"].dt.strftime("%b")
    powerbi_df["month_number"] = powerbi_df["date"].dt.month

    seasons = {
        1: "Winter", 2: "Winter", 12: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    }

    powerbi_df["season"] = powerbi_df["month_number"].map(seasons)

    powerbi_df.to_csv(
        output_dir / "powerbi_dashboard_2024.csv",
        index=False
    )

    print("Power BI dashboard data exported successfully.")

    print("All analytics completed successfully!")


if __name__ == "__main__":
    main()
