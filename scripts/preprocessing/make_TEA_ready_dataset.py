"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : 01-15-2026
# Version     : 1.0
# Description : Make TEA ready dataset
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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_TEA_ready_dataset.py

Genera un dataset TEA-ready de alta frecuencia a partir de datos EC Level 3.

- Recorta el perÃ­odo de anÃ¡lisis hasta 30-06-2025
- Regulariza la frecuencia temporal
- Interpola gaps cortos
- Rellena precipitaciÃ³n con ceros
- Garantiza viento (WS_F o estimado desde USTAR_F)
- Elimina dÃ­as incompletos
- Exporta SOLO variables requeridas por TEA

Salida:
LEVEL3_FJ_2022_2025_TEA_ready_hf.csv
"""

from pathlib import Path
import os
import sys
import numpy as np
import pandas as pd

# =============================================================================
# CONFIGURACIÃ“N PORTABLE
# =============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_CSV = Path(
    os.getenv(
        "TEA_SOURCE_CSV",
        BASE_DIR / "data" / "processed" / "LEVEL3_FJ_2022_2025_ss_v4_daily.csv"
    )
)

OUT_DIR = Path(
    os.getenv(
        "TEA_OUTPUT_DIR",
        BASE_DIR / "data" / "processed"
    )
)

# PerÃ­odo de anÃ¡lisis
END_DATE = pd.Timestamp("2025-06-30 23:59:59")

# Gap-filling
MAX_INTERP_GAPS = 6        # nÂº de pasos consecutivos
EXPECTED_MINUTES = None   # inferir frecuencia automÃ¡ticamente

# =============================================================================
# FUNCIONES
# =============================================================================

def load_and_prepare(csv_path):
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {csv_path}")

    df = pd.read_csv(csv_path)
    if "TIMESTAMP" not in df.columns:
        raise KeyError("La columna TIMESTAMP es obligatoria.")

    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
    df = df.set_index("TIMESTAMP").sort_index()

    # Recorte temporal
    df = df.loc[df.index <= END_DATE]

    return df


def regularize_time(df, expected_minutes=None):

    if expected_minutes is not None:
        freq_min = int(expected_minutes)

    else:
        inferred = pd.infer_freq(df.index)

        freq_min = None
        if inferred is not None:
            try:
                freq_min = int(pd.to_timedelta(inferred).total_seconds() / 60)
            except Exception:
                freq_min = None  # infer_freq devolviÃ³ algo tipo "T"

        if freq_min is None or freq_min <= 0:
            diffs = df.index.to_series().diff().dropna()
            if diffs.empty:
                raise ValueError("No se puede inferir frecuencia temporal (diffs vacÃ­os)")
            freq_min = int(diffs.dt.total_seconds().median() / 60)

    freq_str = f"{freq_min}min"
    n_per_day = int(round(1440 / freq_min))

    full_index = pd.date_range(
        start=df.index[0].floor(freq_str),
        end=df.index[-1].ceil(freq_str),
        freq=freq_str
    )

    df_reg = df.reindex(full_index)

    # InterpolaciÃ³n
    num_cols = df_reg.select_dtypes(include=[np.number]).columns
    df_reg[num_cols] = df_reg[num_cols].interpolate(
        method="time",
        limit=MAX_INTERP_GAPS,
        limit_direction="both"
    )

    if "P_RAIN" in df_reg.columns:
        df_reg["P_RAIN"] = df_reg["P_RAIN"].fillna(0.0)

    total_len = len(df_reg)
    new_len = (total_len // n_per_day) * n_per_day
    df_reg = df_reg.iloc[:new_len]

    return df_reg, freq_min, n_per_day



def ensure_wind(df):
    n = len(df)

    if "WS_F" in df.columns:
        u = pd.to_numeric(df["WS_F"], errors="coerce").values

    elif "USTAR_F" in df.columns:
        ustar = pd.to_numeric(df["USTAR_F"], errors="coerce").values
        factor = 7.0  # factor empÃ­rico razonable
        u = ustar * factor

    else:
        u = np.zeros(n, dtype=float)

    # Si todo es NaN â†’ ceros (fallback seguro)
    if np.all(np.isnan(u)):
        u = np.zeros(n, dtype=float)

    return u

def compute_Rg_pot_proxy(df, rg_col="SW_IN_F"):
    """
    Calcula Rg_pot_proxy como el percentil 98 de SW_IN_F
    por dÃ­a del aÃ±o (DOY), forzando dtype numÃ©rico.
    """
    if rg_col not in df.columns:
        raise KeyError(f"No existe la columna {rg_col} para calcular Rg_pot_proxy.")

    # Forzar a numÃ©rico (valores no numÃ©ricos -> NaN)
    rg = pd.to_numeric(df[rg_col], errors="coerce")

    doy = df.index.dayofyear

    # Calcular percentil 98 ignorando NaN
    p98 = rg.groupby(doy).quantile(0.98)

    # Mapear al Ã­ndice temporal
    rg_pot = df.index.to_series().dt.dayofyear.map(p98)

    return rg_pot.values

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("Leyendo datos fuente...")
    df = load_and_prepare(INPUT_CSV)

    print("Regularizando frecuencia temporal...")
    df_reg, freq_min, n_per_day = regularize_time(df)

    print(f"Frecuencia final: {freq_min} min ({n_per_day} registros/dÃ­a)")
    print(f"PerÃ­odo final: {df_reg.index.min()} â†’ {df_reg.index.max()}")

    print("Asegurando viento...")
    df_reg["WS_F"] = ensure_wind(df_reg)

    # Calcular Rg_pot_proxy si no existe
    if "Rg_pot_proxy" not in df_reg.columns:
        print("Calculando Rg_pot_proxy desde SW_IN_F (percentil 98 por DOY)...")
        df_reg["Rg_pot_proxy"] = compute_Rg_pot_proxy(
            df_reg, rg_col="SW_IN_F"
        )

    # SelecciÃ³n estricta de variables TEA
    tea_cols = [
        "ET_F",
        "GPP_NT",
        "TA_F",
        "RH",
        "VPD_F",
        "SW_IN_F",
        "P_RAIN",
        "USTAR_F",
        "WS_F",
        "Rg_pot_proxy",
    ]

    missing = [c for c in tea_cols if c not in df_reg.columns]
    if missing:
        raise KeyError(f"Faltan columnas requeridas por TEA: {missing}")

    df_tea = df_reg[tea_cols].copy()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUT_DIR / "LEVEL3_FJ_2022_2025_TEA_ready_hf.csv"
    df_tea.to_csv(out_file)

    print("======================================")
    print("Dataset TEA-ready generado con Ã©xito:")
    print(out_file)
    print("======================================")


if __name__ == "__main__":
    main()


