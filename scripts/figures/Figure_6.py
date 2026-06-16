"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : MM-DD-YYYY
# Version     : 1.0
# Description : Reproduction of Figure 6: Seasonal accumulated carbon fluxes
and multiyear mean (NEE, GPP, RECO, Precipitation).
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

# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Paths
# =============================================================================
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_CSV = BASE_DIR / "data" / "processed" / "LEVEL3_FJ_2022_2025_ss_v4_daily.csv"

# =============================================================================
# Load data
# =============================================================================
df = pd.read_csv(DATA_CSV)
df["date"] = pd.to_datetime(df["TIMESTAMP"])

for c in ["NEE_F2", "GPP_NT", "RECO_NT", "P_RAIN"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# =============================================================================
# Ecohydrological year for carbon fluxes (Julâ€“Jun)
# =============================================================================
def ecohydro_year(date):
    return date.year if date.month >= 7 else date.year - 1

df["eco_year"] = df["date"].apply(ecohydro_year)

# Only full years with flux data
flux_years = [2022, 2023, 2024]
df_flux = df[df["eco_year"].isin(flux_years)]

# =============================================================================
# Hydrological year for precipitation (Marâ€“Mar)
# =============================================================================
def precip_hydro_year(date):
    return date.year if date.month >= 3 else date.year - 1

df["pp_year"] = df["date"].apply(precip_hydro_year)

pp_accum = (
    df.groupby("pp_year")["P_RAIN"]
      .sum()
      .to_dict()
)

# Reassign precipitation to ecohydrological years
# (PP from Mar(t)â€“Feb(t+1) â†’ ecohydro year t)
pp_by_eco = {y: pp_accum.get(y, np.nan) for y in flux_years}

# =============================================================================
# Annual accumulations (carbon fluxes)
# =============================================================================
acum = (
    df_flux.groupby("eco_year")
           .agg(
               NEE=("NEE_F2", "sum"),
               GPP=("GPP_NT", "sum"),
               RECO=("RECO_NT", "sum"),
               ET=("ET_F","sum")
           )
           .sort_index()
)

# Add precipitation
acum["PP"] = pd.Series(pp_by_eco)

# Convention: GPP negative
acum["GPP"] = -acum["GPP"]

# Labels
year_labels = [f"{y}-{y+1}" for y in acum.index]

# =============================================================================
# Multiyear statistics
# =============================================================================
means = acum.mean()
stds = acum.std()

# =============================================================================
# Plot
# =============================================================================
x = np.arange(len(acum))
w = 0.22
pp_offset = 0.651

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(13, 6),
    gridspec_kw={"width_ratios": [3, 1]}
)

# -----------------------------------------------------------------------------
# Panel A: annual accumulated fluxes
# -----------------------------------------------------------------------------
bars_nee  = ax1.bar(x - w, acum["NEE"],  w, label="NEE",  color="blue", zorder=4)
bars_gpp  = ax1.bar(x,     acum["GPP"],  w, label="GPP",  color="green", zorder=4)
bars_reco = ax1.bar(x + w, acum["RECO"], w, label="RECO", color="orange", zorder=4)
bars_et = ax1.bar(x + 2*w, acum["ET"], w, label="ET", color="brown", zorder=4)

def annotate_inside(ax, bars, values):
    for bar, val in zip(bars, values):
        if np.isnan(val):
            continue
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.0f}",
            ha="center", va="center",
            fontsize=11, fontweight="bold",
            color="white",
            zorder=10,        # <-- CLAVE
            clip_on=False     # <-- CLAVE
        )


annotate_inside(ax1, bars_nee,  acum["NEE"])
annotate_inside(ax1, bars_gpp,  acum["GPP"])
annotate_inside(ax1, bars_reco, acum["RECO"])
annotate_inside(ax1, bars_et, acum["ET"])
                
ax1.set_xticks(x)
ax1.set_xticklabels(["Year 1", "Year 2", "Year 3"], fontsize=12)
ax1.set_ylabel("Accumulation (g C m$^{-2}$ year$^{-1}$)")


# -----------------------------------------------------------------------------
# Precipitation (secondary axis)
# -----------------------------------------------------------------------------
ax1b = ax1.twinx()

bars_pp = ax1b.bar(x + pp_offset, acum["PP"], 0.20,
                   color="royalblue", label="PP", zorder=4)

ax1b.set_ylabel("Precipitation (mm, Marâ€“Mar)", color="royalblue")
ax1b.tick_params(axis="y", colors="royalblue")
# Expand precipitation axis to avoid overlap with RECO bars
ymin_pp, ymax_pp = ax1b.get_ylim()
ax1b.set_ylim(ymin_pp, ymax_pp * 1.25)

# Annotate PP bars (near top, inside)
for bar, val in zip(bars_pp, acum["PP"]):
    if np.isnan(val):
        continue
    x_txt = bar.get_x() + bar.get_width() / 2
    y_txt = val * 0.85   # 85% of height (robusto y visual)
    ax1b.text(
        x_txt, y_txt, f"{val:.0f}",
        ha="center", va="top",
        fontsize=11, fontweight="bold",
        color="white", zorder=5
    )


# Legend
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax1b.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2,
           loc="upper center", ncol=5, frameon=False)

# -----------------------------------------------------------------------------
# Panel B: multiyear mean Â± SD
# -----------------------------------------------------------------------------
vars_order = ["PP", "NEE", "GPP", "RECO","ET"]
colors = ["royalblue", "blue", "green", "orange","brown"]

ax2.bar(vars_order, means[vars_order], color=colors)
ax2.errorbar(vars_order, means[vars_order],
             yerr=stds[vars_order],
             fmt="none", ecolor="k", capsize=6)

ymin, ymax = ax2.get_ylim()
yrange = ymax - ymin

# Annotate means with color depending on variable
text_colors = {
    "PP": "black",
    "NEE": "white",
    "GPP": "white",
    "RECO": "black",
    "ET": "black",
}

for i, v in enumerate(vars_order):
    ax2.text(
        i,
        means[v] + stds[v] + 0.03 * yrange,
        f"{means[v]:.0f}",
        ha="center", va="bottom",
        fontsize=11, fontweight="bold",
        color=text_colors[v]
    )
    
# --- expand y-limits to avoid clipping (panel B) ---
ymin, ymax = ax2.get_ylim()
ax2.set_ylim(ymin, ymax * 1.15)

ax2.set_ylabel("Mean accumulation")
ax2.grid(axis="y", linestyle="--", alpha=0.3)


# =============================================================================
# Final layout
# =============================================================================
plt.tight_layout()
plt.show()



