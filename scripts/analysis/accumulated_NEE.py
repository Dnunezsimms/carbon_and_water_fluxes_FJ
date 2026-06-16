"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : MM-DD-YYYY
# Version     : 1.0
# Description : Annual accumulated ecosystem NEE by ecohydrological year
              (Julyâ€“June) at Fray Jorge. Reports mean Â± SE across full years.
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
# =============================================================================
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
# Select and clean NEE
# =============================================================================
nee = df[["date", "ecohydro_year", "NEE_F2"]].dropna()

# =============================================================================
# Annual accumulation
# =============================================================================
annual_nee = (
    nee
    .groupby("ecohydro_year")
    .agg(
        NEE_annual=("NEE_F2", "sum"),
        n_days=("NEE_F2", "count"),
        first_day=("date", "min"),
        last_day=("date", "max")
    )
)

# =============================================================================
# Keep only full ecohydrological years (~365 days)
# =============================================================================
annual_nee_full = annual_nee[
    annual_nee["n_days"] >= 360
]

# =============================================================================
# Interannual statistics (n = 3)
# =============================================================================
mean_nee = annual_nee_full["NEE_annual"].mean()
std_nee = annual_nee_full["NEE_annual"].std()
n_years = annual_nee_full.shape[0]
se_nee = std_nee / np.sqrt(n_years)

# =============================================================================
# Results
# =============================================================================
print("\nAnnual accumulated NEE by ecohydrological year [g C mâ»Â² yearâ»Â¹]\n")
print(annual_nee_full)

print("\nInterannual mean NEE (full years only):")
print(f"Mean Â± SE = {mean_nee:.1f} Â± {se_nee:.1f} g C mâ»Â² yearâ»Â¹")
print(f"Number of years = {n_years}")

