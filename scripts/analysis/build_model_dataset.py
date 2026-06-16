# TODO PUBLIC REPO: verify execution from repository root and further parameterize file paths if needed.
# =============================================================================
# SCRIPT FINAL - DATASET OPTIMIZADO PARA MODELADO (CON FECHA)
# =============================================================================

import pandas as pd
import numpy as np

# =============================================================================
# CONFIG
# =============================================================================

PATH_NEE = "data/processed/nee_clean.csv"

PATHS_PRED = [
    "data/external/remote_sensing_predictors/NEE_predictors_season_3_20240701_20250630.csv",
    "data/external/remote_sensing_predictors/NEE_predictors_season_2_20230701_20240630.csv",
    "data/external/remote_sensing_predictors/NEE_predictors_season_1_20220704_20230630.csv",
]

TARGET = "NEE_F2"

MIN_COVERAGE = 40
MIN_CORR = 0.05
MIN_STD = 0.01

# =============================================================================
# LOAD NEE
# =============================================================================

nee = pd.read_csv(PATH_NEE)

date_col = next((c for c in ['TIMESTAMP','timestamp','fecha','date','time'] if c in nee.columns), None)
if date_col is None:
    raise ValueError("NEE sin fecha")

nee['fecha'] = pd.to_datetime(nee[date_col], errors='coerce')
nee = nee.dropna(subset=['fecha'])

nee[TARGET] = pd.to_numeric(nee[TARGET], errors='coerce')
nee = nee.dropna(subset=[TARGET])

nee['fecha'] = nee['fecha'].values.astype('datetime64[ns]')

print("\nNEE:", len(nee))

# =============================================================================
# LOAD PREDICTORS
# =============================================================================

pred_list = []

for i, path in enumerate(PATHS_PRED):

    df = pd.read_csv(path)

    if 'system:index' in df.columns:
        df['fecha'] = pd.to_datetime(
            df['system:index'].astype(str).str.extract(r'(\d{8})')[0],
            format='%Y%m%d',
            errors='coerce'
        )
    else:
        date_col_pred = next((c for c in df.columns if 'fecha' in c.lower()), None)
        df['fecha'] = pd.to_datetime(df[date_col_pred], errors='coerce')

    df = df.dropna(subset=['fecha'])
    df['fecha'] = df['fecha'].values.astype('datetime64[ns]')
    df['temporada'] = i + 1

    pred_list.append(df)

pred = pd.concat(pred_list, ignore_index=True)

print("PRED:", len(pred))

# =============================================================================
# MERGE
# =============================================================================

merged = pd.merge_asof(
    nee.sort_values('fecha'),
    pred.sort_values('fecha'),
    on='fecha',
    direction='nearest',
    tolerance=pd.Timedelta(days=10)
)

merged = merged.dropna(subset=[TARGET])

print("\nMerged:", len(merged))

# =============================================================================
# ANALISIS VARIABLES
# =============================================================================

predictors = [c for c in merged.columns if c not in ["fecha", "temporada", TARGET]]

summary = []

for col in predictors + [TARGET]:

    serie = pd.to_numeric(merged[col], errors='coerce')

    summary.append({
        "variable": col,
        "coverage": serie.notna().mean()*100,
        "std": serie.std(),
        "corr": serie.corr(merged[TARGET]) if col != TARGET else np.nan
    })

df_vars = pd.DataFrame(summary)

print("\nVARIABLES:")
print(df_vars.sort_values("coverage", ascending=False).round(3))

# =============================================================================
# FEATURE SELECTION
# =============================================================================

df_sel = df_vars[
    (df_vars["variable"] != TARGET) &
    (df_vars["coverage"] >= MIN_COVERAGE) &
    (df_vars["std"].abs() >= MIN_STD) &
    (df_vars["corr"].abs() >= MIN_CORR)
]

selected_vars = df_sel["variable"].tolist()

print("\nVariables seleccionadas:")
print(selected_vars)

# =============================================================================
# DATASET FINAL (ðŸ”¥ FIX AQUI)
# =============================================================================

model_df = merged[selected_vars + [TARGET, "fecha"]].copy()

print("\nDataset inicial:", model_df.shape)

model_df = model_df.dropna()

print("Dataset final limpio:", model_df.shape)

# =============================================================================
# GUARDAR
# =============================================================================

model_df.to_csv("data/processed/model_dataset_final.csv", index=False)

print("\nDataset guardado â†’ data/processed/model_dataset_final.csv")

# =============================================================================
# CHECK FINAL
# =============================================================================

print("\nTop correlaciones:")
print(df_sel.sort_values("corr", ascending=False).round(3))

print("\nSCRIPT FINAL OK ðŸš€")



