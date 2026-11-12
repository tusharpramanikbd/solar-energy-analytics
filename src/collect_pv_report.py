
import re
from pathlib import Path

import pandas as pd
from pypdf import PdfReader


def collect_pv_report():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "finland_pv_report_2024.pdf"
    )

    page_text = PdfReader(file_path).pages[30].extract_text()

    text = re.sub(r"-\s*\n\s*", "", page_text)
    text = " ".join(text.split())

    metrics = [
        (
            "estimated_grid_connected_pv_capacity",
            "Early 2024",
            "MW",
            r"In early 2024, the installed grid-connected PV capacity was estimated to be approximately ([\d ]+) MW"
        ),
        (
            "pv_electricity_share",
            "2024",
            "%",
            r"In 2024, PV represented ([\d.]+)% of the total electricity production in Finland"
        ),
        (
            "largest_pv_plant_capacity",
            "2024",
            "MW",
            r"This PV plant of ([\d.]+) MW is owned by"
        )
    ]

    rows = []

    for metric, reference_period, unit, pattern in metrics:
        match = re.search(pattern, text)

        if not match:
            raise ValueError(f"Metric not found in PDF: {metric}")

        rows.append({
            "country": "Finland",
            "reference_period": reference_period,
            "metric": metric,
            "metric_value": float(match.group(1).replace(" ", "")),
            "unit": unit,
            "source_page": 31
        })

    pv_df = pd.DataFrame(rows)

    if pv_df.isna().any().any():
        raise ValueError("Missing values found in PV report data.")

    if (pv_df["metric_value"] < 0).any():
        raise ValueError("Negative PV benchmark value found.")

    return pv_df
