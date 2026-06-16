# TODO PUBLIC REPO: verify execution from repository root and further parameterize file paths if needed.
# =============================================================================
# MODELO PREDICTIVO FINAL + CORRECCIÃ“N DE SESGO + MAPEO LIMPIO
# =============================================================================

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from joblib import Parallel, delayed
from scipy.spatial import cKDTree

# =============================================================================
# CONFIG
# =============================================================================

MODEL_PATH = "models/best_SVR_NDVI_RAD_topo.joblib"

INPUT_FILES = [
    "data/raw/NEE_predictors_pixels_season_1_20220704_20230630.csv",
    "data/raw/NEE_predictors_pixels_season_2_20230701_20240630.csv",
    "data/raw/NEE_predictors_pixels_season_3_20240701_20250630.csv",
]

OUTPUT_FILES = [
    "outputs/nee_landscape_season_1_20220704_20230630.csv",
    "outputs/nee_landscape_season_2_20230701_20240630.csv",
    "outputs/nee_landscape_season_3_20240701_20250630.csv",
]

PREDICTORS = ["NDVI", "RAD_topo"]

RES_DEG = 0.0002694946

# ðŸ”¥ calibraciÃ³n (clave)
TARGET_MEAN = -260  

# =============================================================================
# FUNCIONES
# =============================================================================

def to_numeric(s):
    return pd.to_numeric(s, errors="coerce")

def parse_date(df):
    if "fecha" in df.columns:
        return pd.to_datetime(df["fecha"], format="%Y%m%d", errors="coerce")
    elif "system_time_start" in df.columns:
        return pd.to_datetime(df["system_time_start"], unit="ms", errors="coerce")
    return pd.NaT


def fill_nan_nearest(raster):

    mask = np.isfinite(raster)

    if mask.sum() == 0:
        return raster

    coords = np.array(np.nonzero(mask)).T
    values = raster[mask]

    tree = cKDTree(coords)

    nan_coords = np.array(np.nonzero(~mask)).T
    _, idx = tree.query(nan_coords)

    filled = raster.copy()
    filled[~mask] = values[idx]

    return filled


def build_grid(df):

    df = df.dropna(subset=["lon", "lat", "accum"])

    lon = df["lon"].values
    lat = df["lat"].values
    val = df["accum"].values

    ix = np.rint(lon / RES_DEG).astype(int)
    iy = np.rint(lat / RES_DEG).astype(int)

    min_ix, max_ix = ix.min(), ix.max()
    min_iy, max_iy = iy.min(), iy.max()

    width = (max_ix - min_ix) + 1
    height = (max_iy - min_iy) + 1

    raster = np.full((height, width), np.nan)

    rows = (max_iy - iy).astype(int)
    cols = (ix - min_ix).astype(int)

    for r, c, v in zip(rows, cols, val):
        raster[r, c] = v

    return raster


def process_pixel(g, model):

    g = g.sort_values("fecha_dt")

    X = g[PREDICTORS].values

    try:
        y_pred = model.predict(X)
    except:
        return None

    accum = np.nansum(y_pred)

    return pd.Series({
        "lon": g["lon"].iloc[0],
        "lat": g["lat"].iloc[0],
        "accum": accum,
        "n_obs": len(g)
    })


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    print("Cargando modelo...")
    model = joblib.load(MODEL_PATH)

    for infile, outfile in zip(INPUT_FILES, OUTPUT_FILES):

        print("\nProcesando:", infile)

        df = pd.read_csv(infile)

        # convertir
        for p in PREDICTORS:
            df[p] = to_numeric(df[p])

        df["lon"] = to_numeric(df["lon"])
        df["lat"] = to_numeric(df["lat"])
        df["fecha_dt"] = parse_date(df)

        # pixel_id
        df["pixel_id"] = (
            np.rint(df["lon"]/RES_DEG).astype(int).astype(str) + "_" +
            np.rint(df["lat"]/RES_DEG).astype(int).astype(str)
        )

        print("Agrupando por pixel...")

        results = Parallel(n_jobs=8)(
            delayed(process_pixel)(g, model)
            for _, g in df.groupby("pixel_id")
        )

        res = pd.DataFrame([r for r in results if r is not None])

        # =============================================================================
        # ðŸ”¥ CORRECCIÃ“N DE SESGO (CLAVE)
        # =============================================================================

        model_mean = res["accum"].mean()

        bias_factor = TARGET_MEAN / model_mean

        print("Bias factor:", bias_factor)

        res["accum"] = res["accum"] * bias_factor

        # =============================================================================
        # GUARDAR CSV
        # =============================================================================

        Path("outputs").mkdir(exist_ok=True)

        res.to_csv(outfile, index=False)

        print("Guardado:", outfile)

        # =============================================================================
        # RASTER LIMPIO (SIN LÃNEAS)
        # =============================================================================

        raster = build_grid(res)

        raster_filled = fill_nan_nearest(raster)

        print("Raster listo (sin lÃ­neas) ðŸš€")

