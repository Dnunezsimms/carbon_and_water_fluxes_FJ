# TODO PUBLIC REPO: verify execution from repository root and further parameterize file paths if needed.
# =============================================================================
# MODELO PREDICTIVO FINAL (DOBLE MODELO - ROBUSTO)
# =============================================================================

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from joblib import Parallel, delayed

# =============================================================================
# CONFIG
# =============================================================================

MODELS_CONFIG = [
    {
        "name": "opt",
        "path": "models/best_SVR_NDVI_RAD_topo.joblib",
        "predictors": ["NDVI", "RAD_topo"]
    },
    {
        "name": "eco",
        "path": "models/best_SVR_NDVI_Pol_moisture_RAD_topo.joblib",
        "predictors": ["NDVI", "Pol_moisture", "RAD_topo"]
    }
]

INPUT_FILES = [
    "data/raw/NEE_predictors_pixels_season_1_20220704_20230630.csv",
    "data/raw/NEE_predictors_pixels_season_2_20230701_20240630.csv",
    "data/raw/NEE_predictors_pixels_season_3_20240701_20250630.csv",
]

RES_DEG = 0.0002694946

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


def process_pixel(g, model, predictors):

    g = g.sort_values("fecha_dt")

    # ðŸ”¥ eliminar filas con NaN en predictores
    g = g.dropna(subset=predictors)

    if len(g) == 0:
        return None

    try:
        X = g[predictors]  # ðŸ”¥ mantiene nombres â†’ evita warning sklearn
        y_pred = model.predict(X)
    except Exception:
        return None

    y_pred = np.asarray(y_pred, dtype=float)

    if len(y_pred) == 0:
        return None

    # ðŸ”¥ acumulaciÃ³n anual robusta
    mean_daily = np.nanmean(y_pred)
    accum = mean_daily * 365

    return pd.Series({
        "lon": g["lon"].iloc[0],
        "lat": g["lat"].iloc[0],
        "accum": accum,
        "n_obs": len(y_pred)
    })


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    Path("outputs").mkdir(exist_ok=True)

    for model_cfg in MODELS_CONFIG:

        print("\n==============================")
        print("MODELO:", model_cfg["name"])
        print("==============================")

        model = joblib.load(model_cfg["path"])
        predictors = model_cfg["predictors"]

        for i, infile in enumerate(INPUT_FILES):

            print("\nProcesando:", infile)

            df = pd.read_csv(infile)

            # ðŸ”¥ limpieza bÃ¡sica
            for col in predictors + ["lon", "lat"]:
                df[col] = to_numeric(df[col])

            df["fecha_dt"] = parse_date(df)

            # ðŸ”¥ eliminar basura crÃ­tica
            df = df.dropna(subset=["lon", "lat", "fecha_dt"])

            # ðŸ”¥ pixel_id robusto (clave)
            df["pixel_id"] = (
                np.round(df["lon"] / RES_DEG).astype(int).astype(str) + "_" +
                np.round(df["lat"] / RES_DEG).astype(int).astype(str)
            )

            print("Agrupando pixeles...")

            grouped = df.groupby("pixel_id")

            results = Parallel(n_jobs=8)(
                delayed(process_pixel)(g, model, predictors)
                for _, g in grouped
            )

            # ðŸ”¥ filtrar resultados vÃ¡lidos
            results = [r for r in results if r is not None]

            if len(results) == 0:
                print("âš ï¸ WARNING: 0 pixeles procesados")
                continue

            res = pd.DataFrame(results)

            print("Pixeles:", len(res))
            print("Mean:", round(res["accum"].mean(), 3))
            print("Std:", round(res["accum"].std(), 3))

            # ðŸ”¥ OUTPUT por modelo
            outfile = f"outputs/nee_{model_cfg['name']}_season_{i+1}.csv"
            res.to_csv(outfile, index=False)

            print("Guardado:", outfile)

    print("\nðŸš€ TODOS LOS MODELOS LISTOS")
