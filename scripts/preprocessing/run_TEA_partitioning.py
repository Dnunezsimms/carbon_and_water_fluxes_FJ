"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : 01-22-2026
# Version     : 1.0
# Description : 
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
# IMPORTANT

# Select Pyhton 3.10 version and TEA environment before running  

from pathlib import Path
import os
import sys
import numpy as np
import pandas as pd

# =============================================================================
# PORTABLE CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = Path(
    os.getenv(
        "TEA_INPUT_CSV",
        BASE_DIR / "data" / "processed" / "LEVEL3_FJ_2022_2025_TEA_ready_hf.csv"
    )
)

OUT_DIR = Path(
    os.getenv(
        "TEA_OUTPUT_DIR",
        BASE_DIR / "data" / "processed"
    )
)

# Columns required by TEA
REQUIRED_COLS = {
    "ET_F": "ET (mm per timestep)",
    "GPP_NT": "GPP",
    "RH": "Relative humidity (%)",
    "SW_IN_F": "Incoming shortwave radiation",
    "TA_F": "Air temperature (Â°C)",
    "VPD_F": "Vapor pressure deficit",
    "P_RAIN": "Precipitation (mm)",
    "WS_F": "Wind speed"
}

# =============================================================================
# VALIDATION UTILITIES
# =============================================================================

def validate_and_cast_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure required TEA inputs are numeric.
    Converts columns to float and reports coercions.
    """
    print("\n[VALIDATION] Casting TEA input variables to numeric...")
    for col in REQUIRED_COLS:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")
        before_na = df[col].isna().sum()
        df[col] = pd.to_numeric(df[col], errors="coerce")
        after_na = df[col].isna().sum()
        if after_na > before_na:
            print(f"[WARN] Column {col}: {after_na - before_na} values coerced to NaN")
    return df


def validate_arrays(*arrays):
    """
    Ensure all arrays have same length and are numeric.
    """
    lengths = [len(a) for a in arrays]
    if len(set(lengths)) != 1:
        raise ValueError(f"Input arrays have inconsistent lengths: {lengths}")

    for a in arrays:
        if not np.issubdtype(a.dtype, np.number):
            raise TypeError("Non-numeric array detected in TEA inputs")


def print_summary(name, arr):
    print(
        f"{name:8s} | dtype={arr.dtype} | "
        f"min={np.nanmin(arr):.3f} | max={np.nanmax(arr):.3f} | "
        f"NaN={np.isnan(arr).sum()}"
    )


# =============================================================================
# MAIN
# =============================================================================

def main():

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"TEA-ready CSV not found: {CSV_PATH}")

    print("======================================")
    print("Reading TEA-ready dataset")
    print("======================================")

    df = pd.read_csv(CSV_PATH, index_col=0, parse_dates=True)
    df = df.sort_index()
    df.index.name = "TIMESTAMP"

    # -------------------------------------------------------------------------
    # VALIDATION & CASTING
    # -------------------------------------------------------------------------
    df = validate_and_cast_numeric(df)

    # -------------------------------------------------------------------------
    # BUILD TEA INPUT ARRAYS
    # -------------------------------------------------------------------------
    ts     = df.index.to_pydatetime()
    ET     = df["ET_F"].values
    GPP    = df["GPP_NT"].values
    RH     = df["RH"].values
    Rg     = df["SW_IN_F"].values
    Tair   = df["TA_F"].values
    VPD    = df["VPD_F"].values
    precip = df["P_RAIN"].fillna(0.0).values
    u      = df["WS_F"].fillna(0.0).values

    # Optional Rg_pot proxy
    if "Rg_pot_proxy" in df.columns:
        Rg_pot = pd.to_numeric(df["Rg_pot_proxy"], errors="coerce").values
    else:
        Rg_pot = None
        print("[INFO] Rg_pot_proxy not found â†’ passing None to TEA")

    # -------------------------------------------------------------------------
    # FINAL CHECK BEFORE TEA
    # -------------------------------------------------------------------------
    print("\n[VALIDATION] Final input summary:")
    print_summary("ET", ET)
    print_summary("GPP", GPP)
    print_summary("RH", RH)
    print_summary("Rg", Rg)
    print_summary("Tair", Tair)
    print_summary("VPD", VPD)
    print_summary("precip", precip)
    print_summary("u", u)

    validate_arrays(ET, GPP, RH, Rg, Tair, VPD, precip, u)

    # -------------------------------------------------------------------------
    # RUN TEA
    # -------------------------------------------------------------------------
    print("\n======================================")
    print("Running TEA.simplePartition()")
    print("======================================")

    try:
        from TEA import simplePartition
    except Exception as e:
        raise ImportError("TEA not installed in this environment") from e

    TEA_T, TEA_E, TEA_WUE = simplePartition(
        ts, ET, GPP, RH, Rg, Rg_pot, Tair, VPD, precip, u
    )

    # -------------------------------------------------------------------------
    # SAVE OUTPUTS
    # -------------------------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    out_df = pd.DataFrame(
        {
            "TEA_T":   np.asarray(TEA_T).reshape(-1),
            "TEA_E":   np.asarray(TEA_E).reshape(-1),
            "TEA_WUE": np.asarray(TEA_WUE).reshape(-1),
        },
        index=df.index
    )

    out_file = OUT_DIR / "LEVEL3_FJ_2022_2025_TEA_outputs.csv"
    out_df.to_csv(out_file)

    print("======================================")
    print("TEA completed successfully")
    print(f"Outputs written to: {out_file}")
    print("======================================")

# =============================================================================

if __name__ == "__main__":
    main()


