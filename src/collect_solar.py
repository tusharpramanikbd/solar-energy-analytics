from pathlib import Path
import pandas as pd


def collect_solar():
    file_path = Path(__file__).resolve().parent.parent / "data" / "solar_vaasa_2024.csv"

    solar_df = pd.read_csv(
        file_path,
        skiprows=9,
        na_values=[-999]
    )

    solar_df["date"] = pd.to_datetime({
        "year": solar_df["YEAR"],
        "month": solar_df["MO"],
        "day": solar_df["DY"]
    })

    solar_df = solar_df.rename(columns={
        "ALLSKY_SFC_SW_DWN": "solar_irradiation_kwh_m2_day"
    })

    solar_df["city"] = "Vaasa"

    solar_df = solar_df[
        ["date", "city", "solar_irradiation_kwh_m2_day"]
    ]

    if len(solar_df) != 366:
        raise ValueError("Unexpected number of solar records.")

    if solar_df.isna().any().any():
        raise ValueError("Missing values found in solar data.")

    if solar_df["date"].duplicated().any():
        raise ValueError("Duplicate dates found in solar data.")

    if (solar_df["solar_irradiation_kwh_m2_day"] < 0).any():
        raise ValueError("Negative solar irradiation found.")

    return solar_df
