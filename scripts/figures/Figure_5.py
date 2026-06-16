"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : 01-22-2026
# Version     : 1.0
# Description : Time series of carbon fluxes with PAR and REW
#               REW computed from mean soil water content (SWC sensors)
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
# FIGURE â€” Carbon fluxes + PAR + REW (FINAL WITH DOUBLE X AXIS)
# =============================================================================

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11
})
# =============================================================================
# PATHS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_CSV = BASE_DIR / "data" / "processed" / "LEVEL3_FJ_2022_2025_ss_v4_daily.csv"

# =============================================================================
# LOAD DATA
# =============================================================================

df = pd.read_csv(DATA_CSV, parse_dates=["TIMESTAMP"])
df = df.set_index("TIMESTAMP").sort_index()

# ðŸ”¥ CORTE CONSISTENTE CON TODAS LAS FIGURAS
X_START = pd.to_datetime("2022-07-01")
X_END   = pd.to_datetime("2025-07-30")

df = df.loc[X_START:X_END]

# =============================================================================
# VARIABLES
# =============================================================================

PAR  = pd.to_numeric(df["PPFD_sum"], errors="coerce")
NEE  = pd.to_numeric(df["NEE_F2"], errors="coerce")
GPP  = pd.to_numeric(df["GPP_NT"], errors="coerce").clip(lower=0)
RECO = pd.to_numeric(df["RECO_NT"], errors="coerce")

PAR = PAR.where(PAR > 0)

SWC_cols = ["SWC_F_1_1_1", "SWC_F_2_1_1", "SWC_F_3_1_1"]
SWC = df[SWC_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)

# =============================================================================
# REW
# =============================================================================

theta_wp = 0.05532005
theta_fc = 0.064879662

REW = (SWC - theta_wp) / (theta_fc - theta_wp)
REW = REW.clip(0, 1)

# =============================================================================
# ECO YEARS
# =============================================================================

ECO_YEARS = {
    "Year 1": ("2022-07-01", "2023-06-30"),
    "Year 2": ("2023-07-01", "2024-06-30"),
    "Year 3": ("2024-07-01", "2025-07-30"),
}

YEAR_LINES = [
    pd.to_datetime("2023-07-01"),
    pd.to_datetime("2024-07-01"),
]

# =============================================================================
# FIGURE
# =============================================================================

fig = plt.figure(figsize=(14, 7))
gs = GridSpec(3, 1, height_ratios=[1, 3, 0.8], hspace=0.0)

# ------------------------------------------------------------------
# a) PAR
# ------------------------------------------------------------------
ax0 = fig.add_subplot(gs[0])
ax0.plot(df.index, PAR, color="black", lw=0.8)

ax0.text(0.005, 0.90, "a)", transform=ax0.transAxes, fontsize=13, fontweight="bold")

ax0.spines["bottom"].set_visible(False)
ax0.tick_params(labelbottom=False)

ax0_r = ax0.twinx()
ax0_r.set_ylabel("PAR\n(mol m$^{-2}$ s$^{-1}$)")
ax0_r.set_ylim(ax0.get_ylim())
ax0_r.spines["top"].set_visible(False)
ax0_r.spines["bottom"].set_visible(False)

# ------------------------------------------------------------------
# b) Carbon fluxes
# ------------------------------------------------------------------
ax1 = fig.add_subplot(gs[1], sharex=ax0)

ax1.plot(df.index, GPP, color="0.5", lw=1.0, label="GPP")
ax1.plot(df.index, RECO, color="orange", lw=1.0, label="Reco")

ax1.fill_between(df.index, 0, NEE, where=NEE < 0, color="steelblue", alpha=0.8)
ax1.fill_between(df.index, 0, NEE, where=NEE > 0, color="tomato", alpha=0.8)

ax1.axhline(0, color="k", lw=0.8)
ax1.set_ylabel("Carbon flux (g C m$^{-2}$ day$^{-1}$)")

ax1.text(0.005, 0.94, "b)", transform=ax1.transAxes, fontsize=13, fontweight="bold")

ax1.legend(ncol=4, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.02))

ax1.spines["bottom"].set_visible(False)
ax1.tick_params(labelbottom=False)

# ------------------------------------------------------------------
# c) REW
# ------------------------------------------------------------------
ax2 = fig.add_subplot(gs[2], sharex=ax0)
ax2.fill_between(df.index, 0, REW, color="0.6")

ax2.set_ylim(0, 1)
ax2.set_yticks([])

ax2.text(0.005, 1.02, "c)", transform=ax2.transAxes, fontsize=13, fontweight="bold")

ax2_r = ax2.twinx()
ax2_r.set_ylabel("REW (-)")
ax2_r.set_ylim(0, 1)

# =============================================================================
# ðŸ”¥ X AXIS NIVEL 1 (MONTHS)
# =============================================================================

ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))

# =============================================================================
# ðŸ”¥ X AXIS NIVEL 2 (ECO YEARS)
# =============================================================================

year_centers = []
year_labels = []

for label, (start, end) in ECO_YEARS.items():
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    start_clip = max(start, X_START)
    end_clip   = min(end, X_END)

    year_centers.append(start_clip + (end_clip - start_clip)/2)
    year_labels.append(label)

ax_bottom2 = ax2.secondary_xaxis('bottom')
ax_bottom2.set_xticks(year_centers)
ax_bottom2.set_xticklabels(year_labels, fontsize=12)

ax_bottom2.spines['bottom'].set_position(('outward', 35))
ax_bottom2.spines['bottom'].set_visible(False)
ax_bottom2.tick_params(length=0)

# =============================================================================
# ðŸ”¥ YEAR SEPARATION (SOLO INTERNAS)
# =============================================================================

for d in YEAR_LINES:
    for ax in [ax0, ax1, ax2]:
        ax.axvline(
            d,
            color='0.3',
            lw=1.2,
            ls='--',
            ymin=-0.08,
            ymax=1.0,
            clip_on=False,
            zorder=10
        )

# =============================================================================
# ðŸ”¥ LÃMITES (CLAVE)
# =============================================================================

for ax in [ax0, ax1, ax2]:
    ax.set_xlim(X_START, X_END)
    ax.margins(x=0)

# =============================================================================
# FINAL
# =============================================================================


fig.tight_layout()
plt.show()

