import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------
# 1. RUTA BASE
# -------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
file_path = BASE_DIR / "data" / "processed" / "rainfall_data_1984-2025_updated.xlsx"

# -------------------------
# 2. READ
# -------------------------
df = pd.read_excel(file_path, sheet_name=0)

# -------------------------
# 3. SELECT
# -------------------------
df = df[["aÃ±os", "mes", "monthly.pp"]]

# -------------------------
# 4. CLEAN
# -------------------------
df = df.dropna(subset=["aÃ±os"])
df["aÃ±os"] = df["aÃ±os"].astype(int)
df["mes"] = df["mes"].astype(int)
df["monthly.pp"] = df["monthly.pp"].fillna(0)

# -------------------------
# 5. AGREGACIÃ“N ANUAL
# -------------------------
annual = df.groupby("aÃ±os")["monthly.pp"].sum().reset_index()

# -------------------------
# ðŸ” DEBUG (opcional pero Ãºtil)
# -------------------------
print("AÃ±o inicial:", annual["aÃ±os"].min())
print("AÃ±o final:", annual["aÃ±os"].max())
print("2025:", annual[annual["aÃ±os"] == 2025])

# -------------------------
# 6. PLOT
# -------------------------
plt.figure(figsize=(14,5))
plt.bar(annual["aÃ±os"], annual["monthly.pp"])

plt.ylabel("Annual precipitation (mm)")


# ðŸ”¥ ticks cada 5 aÃ±os (clave)
year_min = annual["aÃ±os"].min()
year_max = annual["aÃ±os"].max()
ticks = list(range(year_min, year_max + 1, 5))

plt.xticks(ticks, rotation=0)

plt.tight_layout()
plt.show()
