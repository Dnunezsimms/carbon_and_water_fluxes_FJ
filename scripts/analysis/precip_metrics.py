"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : 01-15-2026
# Version     : 1.0
# Description : Precipitation metrics
# =============================================================================
# Diego NÃºÃ±ez Simms | Agricultural & Natural Ecosystem Data Scientist
# GIS | Eddy Covariance | ML | Carbon & Water Fluxes | Python
# MSc Territorial Management of Natural Resources
# Contact: diegonunezsimms@gmail.com
#         +56 939 058 165
#         https://www.linkedin.com/in/dnunezsimms
#         https://github.com/Dnunezsimms
# =============================================================================
"""
from pathlib import Path
import pandas as pd
import numpy as np

# ---------------- CONFIGURATION ----------------
SCRIPT_DIR = Path(__file__).resolve().parents[2] / "scripts" / "analysis"
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
DATA_FILE = DATA_DIR / "LEVEL3_FJ_2022_2025_ss_daily.csv"

# Effective precipitation year: March (t) â€“ February (t+1)
EFFECTIVE_YEARS = {
    "Year 1": ("2022-03-01", "2023-02-28"),
    "Year 2": ("2023-03-01", "2024-02-29"),
    "Year 3": ("2024-03-01", "2025-02-28"),
}

P_EVENT = 5.0     # mm day-1 â†’ effective rainfall
P_LARGE = 15.0    # mm day-1 â†’ recharge events
# -----------------------------------------------

# Load data
df = pd.read_csv(DATA_FILE, encoding="latin1")
df.columns = df.columns.str.strip()
df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce")
df["P_RAIN"] = pd.to_numeric(df["P_RAIN"], errors="coerce")

rows = []

for year, (start, end) in EFFECTIVE_YEARS.items():
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    d = df.loc[
        (df["TIMESTAMP"] >= start) &
        (df["TIMESTAMP"] <= end),
        "P_RAIN"
    ].dropna()

    if d.empty:
        continue

    row = {
        "Year": year,
        "PP_effective_total_mm": d.sum(),
        "Frac_days_P_gt_5mm": (d > P_EVENT).mean(),
        "Frac_days_P_gt_15mm": (d > P_LARGE).mean(),
        "Mean_event_P_mm": d[d > P_EVENT].mean(),
        "Max_daily_P_mm": d.max(),
    }

    rows.append(row)

df_metrics = pd.DataFrame(rows)

print("\nEffective precipitation metrics (Marchâ€“February):\n")
print(df_metrics.round(2))



