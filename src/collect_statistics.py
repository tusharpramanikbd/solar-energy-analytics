
from pathlib import Path
import pandas as pd


def collect_statistics():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "finland_solar_2020_2024.xlsx"
    )

    statistics_df = pd.read_excel(
        file_path,
        sheet_name="11sr",
        skiprows=3,
        nrows=5,
        usecols="A:C",
        header=None,
        names=["year", "production_type", "solar_generation_gwh"],
        engine="openpyxl"
    )

    if statistics_df["year"].tolist() != list(range(2020, 2025)):
        raise ValueError("Unexpected years in statistics data.")

    if not statistics_df["production_type"].eq("Solar power").all():
        raise ValueError("Unexpected production type.")

    if (
        statistics_df["solar_generation_gwh"].isna().any()
        or (statistics_df["solar_generation_gwh"] < 0).any()
    ):
        raise ValueError("Invalid solar generation values.")

    statistics_df = statistics_df.drop(columns=["production_type"])
    statistics_df["country"] = "Finland"

    statistics_df = statistics_df[
        ["year", "country", "solar_generation_gwh"]
    ]

    return statistics_df
