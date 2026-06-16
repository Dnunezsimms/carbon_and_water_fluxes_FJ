"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : 01-22-2026
# Version     : 1.0
# Description : accumulated_ET
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
# ===========================================================================
# Imports
# =============================================================================
from pathlib import Path
import pandas as pd
import numpy as np

# =============================================================================
# Paths
# =============================================================================
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
DATA_FILE = DATA_DIR / "LEVEL3_FJ_2022_2025_ss_daily.csv"

# =============================================================================
# Load data
# =============================================================================
df = pd.read_csv(DATA_FILE)

# =============================================================================
# Parse date
# =============================================================================
df["date"] = pd.to_datetime(df["TIMESTAMP"])

# =============================================================================
# Define ecohydrological year (Julyâ€“June)
# =============================================================================
def ecohydrological_year(date):
    return date.year if date.month >= 7 else date.year - 1

df["ecohydro_year"] = df["date"].apply(ecohydrological_year)

# =============================================================================
# Select and clean ET
# =============================================================================
et = df[["date", "ecohydro_year", "ET_F"]].dropna()

# =============================================================================
# Annual accumulation
# =============================================================================
annual_et = (
    et
    .groupby("ecohydro_year")
    .agg(
        ET_annual=("ET_F", "sum"),
        n_days=("ET_F", "count"),
        first_day=("date", "min"),
        last_day=("date", "max")
    )
)

# =============================================================================
# Keep only full ecohydrological years (~365 days)
# =============================================================================
annual_et_full = annual_et[
    annual_et["n_days"] >= 360
]

# =============================================================================
# Interannual statistics (n = 3)
# =============================================================================
mean_et = annual_et_full["ET_annual"].mean()
std_et = annual_et_full["ET_annual"].std()
n_years = annual_et_full.shape[0]
se_et = std_et / np.sqrt(n_years)

# =============================================================================
# Results
# =============================================================================
print("\nAnnual accumulated ET by ecohydrological year [g C mâ»Â² yearâ»Â¹]\n")
print(annual_et_full)

print("\nInterannual mean ET (full years only):")
print(f"Mean Â± SE = {mean_et:.1f} Â± {se_et:.1f} g C mâ»Â² yearâ»Â¹")
print(f"Number of years = {n_years}")

