"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : MM-DD-YYYY
# Version     : 1.0
# Description : Ecohydrological metrics for precipitation, PAR, carbon fluxes
#               and soil water availability (REW)
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

# ---------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "processed" / "LEVEL3_FJ_2022_2025_ss_daily.csv"

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
P_EVENT = 5.0
P_LARGE = 15.0
REW_STRESS = 0.2

# --- Precipitation years (EXACTLY like precip_metrics.py)
PP_YEARS = {
    "Year 1": ("2022-03-01", "2023-02-28"),
    "Year 2": ("2023-03-01", "2024-02-29"),
    "Year 3": ("2024-03-01", "2025-02-28"),
}

# --- Ecohydrological years (Julâ€“Jun)
ECO_YEARS = {
    "Year 1": ("2022-07-01", "2023-06-30"),
    "Year 2": ("2023-07-01", "2024-06-30"),
    "Year 3": ("2024-07-01", "2025-06-30"),
}

# ---------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------
df = pd.read_csv(DATA_FILE, encoding="latin1")
df.columns = df.columns.str.strip()
df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
df = df.set_index("TIMESTAMP").sort_index()

# ---------------------------------------------------------------------
# VARIABLES
# ---------------------------------------------------------------------
df["P_RAIN"] = pd.to_numeric(df["P_RAIN"], errors="coerce")
df["PAR"]    = pd.to_numeric(df["PPFD_sum"], errors="coerce").where(lambda x: x > 0)
df["GPP"]    = pd.to_numeric(df["GPP_NT"], errors="coerce").clip(lower=0)
df["RECO"]   = pd.to_numeric(df["RECO_NT"], errors="coerce")
df["NEE"]    = pd.to_numeric(df["NEE_F2"], errors="coerce")

SWC_cols = ["SWC_F_1_1_1", "SWC_F_2_1_1", "SWC_F_3_1_1"]
SWC = df[SWC_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)

theta_wp = np.nanpercentile(SWC, 5)
theta_fc = np.nanpercentile(SWC, 95)
df["REW"] = ((SWC - theta_wp) / (theta_fc - theta_wp)).clip(0, 1)

# ---------------------------------------------------------------------
# METRICS
# ---------------------------------------------------------------------
rows = []

for year in ["Year 1", "Year 2", "Year 3"]:

    # ---------------- PP EFFECTIVE (Marâ€“Feb) ----------------
    p_start, p_end = PP_YEARS[year]
    dpp = df.loc[p_start:p_end, "P_RAIN"].dropna()

    # ---------------- FLUXES / PAR / REW (Julâ€“Jun) ----------
    f_start, f_end = ECO_YEARS[year]
    d = df.loc[f_start:f_end].copy()

    row = {
        "Year": year,

        # --- Precipitation (IDENTICAL logic to precip_metrics.py)
        "PP_effective_total_mm": dpp.sum(),
        "Frac_days_P_gt_5mm": (dpp > P_EVENT).mean(),
        "Frac_days_P_gt_15mm": (dpp > P_LARGE).mean(),
        "Mean_event_P_mm": dpp[dpp > P_EVENT].mean(),
        "Max_daily_P_mm": dpp.max(),

        # --- PAR
        "PAR_mean": d["PAR"].mean(),
        "PAR_p90": d["PAR"].quantile(0.9),

        # --- GPP
        "GPP_mean": d["GPP"].mean(),
        "GPP_max": d["GPP"].max(),
        "GPP_annual": d["GPP"].sum(),

        # --- RECO
        "RECO_mean": d["RECO"].mean(),
        "RECO_annual": d["RECO"].sum(),

        # --- NEE
        "NEE_annual": d["NEE"].sum(),

        # --- REW
        "REW_mean": d["REW"].mean(),
        "Frac_days_REW_lt_0.2": (d["REW"] < REW_STRESS).mean(),
    }

    rows.append(row)

df_metrics = pd.DataFrame(rows)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", None)

print("\nEcohydrological metrics summary:\n")
print(df_metrics.round(2))



