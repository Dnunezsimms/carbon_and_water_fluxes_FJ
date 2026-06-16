#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : 04-02-2026
# Version     : 1.1
# Description : Build DAILY dataset (T, E, WUE) and save to data/raw
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

# =============================================================================
# PATHS (PORTABLE)
# =============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
RAW_DIR  = DATA_DIR

RAW_DIR.mkdir(parents=True, exist_ok=True)

CLEANED_CSV = DATA_DIR / "LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv"
TEA_OUT = DATA_DIR / "LEVEL3_FJ_2022_2025_no_gaps_for_TEA_TEA_outputs.csv"

OUT_CSV = RAW_DIR / "LEVEL3_FJ_2022_2025_daily_T_E_WUE.csv"

# =============================================================================
# FUNCTIONS
# =============================================================================

def build_daily_from_tea(tea_path: Path) -> pd.DataFrame:
    """Build daily T, E and WUE from TEA outputs."""
    tea = (
        pd.read_csv(tea_path, index_col=0, parse_dates=True)
        .sort_index()
    )

    required = {"TEA_T", "TEA_E", "TEA_WUE"}
    if not required.issubset(tea.columns):
        raise RuntimeError(
            "TEA outputs must contain TEA_T, TEA_E and TEA_WUE columns"
        )

    daily_T = tea["TEA_T"].resample("D").sum()
    daily_E = tea["TEA_E"].resample("D").sum()
    daily_WUE = tea["TEA_WUE"].resample("D").mean()

    return pd.DataFrame({
        "TIMESTAMP": daily_T.index,
        "T": daily_T.values,
        "E": daily_E.values,
        "WUE": daily_WUE.values
    })


def load_daily_T_E_WUE() -> pd.DataFrame:
    """Load or build daily dataframe with T, E and WUE."""

    # Priority 1: cleaned daily CSV
    if CLEANED_CSV.exists():
        df = pd.read_csv(CLEANED_CSV, parse_dates=["TIMESTAMP"])

        df["T"] = pd.to_numeric(df["T"], errors="coerce")
        df["E"] = pd.to_numeric(df["E"], errors="coerce")

        if "WUE" not in df.columns:
            with np.errstate(divide="ignore", invalid="ignore"):
                df["WUE"] = df["T"] / (df["T"] + df["E"])

        return df[["TIMESTAMP", "T", "E", "WUE"]]

    # Priority 2: TEA outputs
    if TEA_OUT.exists():
        return build_daily_from_tea(TEA_OUT)

    raise FileNotFoundError(
        "No cleaned daily CSV or TEA outputs found."
    )

# =============================================================================
# MAIN
# =============================================================================

def main():

    df = load_daily_T_E_WUE()

    # final cleaning
    df[["T", "E", "WUE"]] = df[["T", "E", "WUE"]].apply(
        pd.to_numeric, errors="coerce"
    )
    df[["T", "E"]] = df[["T", "E"]].clip(lower=0.0)

    df = (
        df.sort_values("TIMESTAMP")
          .reset_index(drop=True)
    )

    # save dataset
    df.to_csv(OUT_CSV, index=False)

    print(
        f"[OK] Dataset DAILY Tâ€“Eâ€“WUE creado correctamente en la ruta:\n"
        f"     {OUT_CSV}"
    )


if __name__ == "__main__":
    main()



