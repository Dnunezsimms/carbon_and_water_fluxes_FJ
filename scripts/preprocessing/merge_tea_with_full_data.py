# =========================================================
# ðŸ”§ MERGE E, T, WUE A DATASET PRINCIPAL (ROBUSTO)
# =========================================================

import pandas as pd
from pathlib import Path

base_path = Path(__file__).resolve().parents[2]

file_ET = base_path / "data" / "processed" / "LEVEL3_FJ_2022_2025_daily_T_E_WUE.csv"
file_main = base_path / "data" / "processed" / "LEVEL3_FJ_2022_2025_ss_v4_daily.csv"

output_file = base_path / "data" / "processed" / "LEVEL3_FJ_merged_ET_T_WUE.csv"

# =========================================================
# ðŸ“¥ LEER DATOS (FORZANDO BIEN EL CSV)
# =========================================================

print("ðŸ“¥ Leyendo archivos...")

df_ET = pd.read_csv(file_ET, sep=",", encoding="utf-8-sig")
df_main = pd.read_csv(file_main)

# =========================================================
# ðŸ” DEBUG CLAVE
# =========================================================

print("\nColumnas df_ET:")
print(df_ET.columns.tolist())

# limpiar nombres de columnas (CLAVE)
df_ET.columns = df_ET.columns.str.strip().str.upper()
df_main.columns = df_main.columns.str.strip().str.upper()

print("\nColumnas df_ET (limpias):")
print(df_ET.columns.tolist())

# =========================================================
# ðŸ§¹ ASEGURAR TIMESTAMP
# =========================================================

if "TIMESTAMP" not in df_ET.columns:
    raise ValueError(f"âŒ TIMESTAMP no encontrado en df_ET. Columnas disponibles: {df_ET.columns.tolist()}")

if "TIMESTAMP" not in df_main.columns:
    raise ValueError(f"âŒ TIMESTAMP no encontrado en df_main. Columnas disponibles: {df_main.columns.tolist()}")

df_ET["TIMESTAMP"] = pd.to_datetime(df_ET["TIMESTAMP"]).dt.date
df_main["TIMESTAMP"] = pd.to_datetime(df_main["TIMESTAMP"]).dt.date

# =========================================================
# ðŸ”— MERGE
# =========================================================

print("ðŸ”— Haciendo merge...")

df_merged = df_main.merge(
    df_ET[["TIMESTAMP", "E", "T", "WUE"]],
    on="TIMESTAMP",
    how="left"
)

# =========================================================
# ðŸ’¾ GUARDAR
# =========================================================

df_merged.to_csv(output_file, index=False)

print(f"\nâœ… Listo. Guardado en:\n{output_file}")



