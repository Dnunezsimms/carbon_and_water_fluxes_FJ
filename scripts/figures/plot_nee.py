# TODO PUBLIC REPO: verify execution from repository root and further parameterize file paths if needed.
# =============================================================================
# FIGURA FINAL NEE (4 MAPAS: OPT vs ECO) - VERSION FINAL PRO
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

# =============================================================================
# CONFIG
# =============================================================================

FILES_OPT = [
    "results/tables/nee_opt_season_1.csv",
    "results/tables/nee_opt_season_2.csv",
    "results/tables/nee_opt_season_3.csv",
]

FILES_ECO = [
    "results/tables/nee_eco_season_1.csv",
    "results/tables/nee_eco_season_2.csv",
    "results/tables/nee_eco_season_3.csv",
]

SHAPEFILE = "data/external/complementary/Matorral_SUCULENTAS_PNBFJ_UNI_TOPO.shp"
TOWER_SHP = "data/external/complementary/Torre Eddy.shp"

# =============================================================================
# FUNCION METRICAS
# =============================================================================

def build_metrics(files):

    dfs = [pd.read_csv(f) for f in files]

    df = dfs[0][["lon","lat","accum"]].copy()
    df = df.rename(columns={"accum":"s1"})
    df["s2"] = dfs[1]["accum"].values
    df["s3"] = dfs[2]["accum"].values

    df["mean"] = df[["s1","s2","s3"]].mean(axis=1)
    df["std"] = df[["s1","s2","s3"]].std(axis=1)

    df["cv"] = 100 * df["std"] / np.abs(df["mean"])
    df.loc[np.abs(df["mean"]) < 1e-8, "cv"] = np.nan
    df.loc[df["cv"] > 200, "cv"] = np.nan

    return df

# =============================================================================
# LOAD
# =============================================================================

df_opt = build_metrics(FILES_OPT)
df_eco = build_metrics(FILES_ECO)

gdf = gpd.read_file(SHAPEFILE)
tower = gpd.read_file(TOWER_SHP)
pt = tower.geometry.iloc[0].centroid

# =============================================================================
# FIGURA (SIN constrained_layout)
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(16,12))

ax1, ax2, ax3, ax4 = axes.flatten()

# =============================================================================
# PLOTS
# =============================================================================

# OPT
sc1 = ax1.scatter(df_opt["lon"], df_opt["lat"], c=df_opt["mean"], s=2, cmap="viridis")
sc2 = ax2.scatter(df_opt["lon"], df_opt["lat"], c=df_opt["cv"], s=2, cmap="plasma_r")

# ECO
sc3 = ax3.scatter(df_eco["lon"], df_eco["lat"], c=df_eco["mean"], s=2, cmap="viridis")
sc4 = ax4.scatter(df_eco["lon"], df_eco["lat"], c=df_eco["cv"], s=2, cmap="plasma_r")

# =============================================================================
# SHAPE + TORRE
# =============================================================================

for ax in [ax1, ax2, ax3, ax4]:
    gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)
    ax.scatter(pt.x, pt.y, marker="^", s=100,
               color="red", edgecolor="black", zorder=10)
    ax.set_aspect("equal")
    ax.set_xlabel("Longitude")

ax1.set_ylabel("Latitude")
ax3.set_ylabel("Latitude")

# =============================================================================
# TITULOS
# =============================================================================

ax1.set_title("OPT - Mean NEE")
ax2.set_title("OPT - CV (%)")
ax3.set_title("ECO - Mean NEE")
ax4.set_title("ECO - CV (%)")

# =============================================================================
# COLORBARS
# =============================================================================

fig.colorbar(sc1, ax=ax1, fraction=0.046, pad=0.02).set_label("NEE")
fig.colorbar(sc2, ax=ax2, fraction=0.046, pad=0.02).set_label("CV (%)")
fig.colorbar(sc3, ax=ax3, fraction=0.046, pad=0.02).set_label("NEE")
fig.colorbar(sc4, ax=ax4, fraction=0.046, pad=0.02).set_label("CV (%)")

# =============================================================================
# LEYENDAS
# =============================================================================

legend = [
    Line2D([0],[0], marker='^', color='w',
           markerfacecolor='red',
           markeredgecolor='black',
           markersize=9,
           label='Eddy tower')
]

for ax in [ax1, ax2, ax3, ax4]:
    ax.legend(handles=legend, loc='lower right')

# =============================================================================
# SCALEBAR (CORREGIDA)
# =============================================================================

def add_scalebar(fig, ax_left, ax_right):

    pos1 = ax_left.get_position()
    pos2 = ax_right.get_position()

    x0 = pos1.x0
    width = pos2.x1 - pos1.x0

    # ðŸ”¥ POSICIÃ“N PERFECTA
    y = min(pos1.y0, pos2.y0) - 0.08

    bar_ax = fig.add_axes([x0, y, width, 0.02])
    bar_ax.axis("off")

    for i in range(5):
        bar_ax.add_patch(Rectangle(
            (i/5, 0.2), 1/5, 0.6,
            facecolor='black' if i % 2 == 0 else 'white',
            edgecolor='black'
        ))

    for i in range(6):
        bar_ax.text(i/5, -0.6, f"{i*2}", ha='center')

    bar_ax.text(1.02, -0.6, "km")

# ðŸ”¥ LLAMADA REAL (ESTO ERA LO QUE FALTABA)
add_scalebar(fig, ax3, ax4)

# =============================================================================
# AJUSTE FINAL
# =============================================================================

plt.subplots_adjust(wspace=0.25, hspace=0.25)

# =============================================================================
# SAVE
# =============================================================================

plt.savefig("results/figures/NEE_COMPARISON_4MAPS.png", dpi=300, bbox_inches="tight")

print("âœ… FIGURA 4 MAPAS PERFECTA")









