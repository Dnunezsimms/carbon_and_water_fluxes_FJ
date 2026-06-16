# =============================================================================
# FIGURE 1 â€” ET, T and T/ET (double bottom axis, ecohydrological years)
# =============================================================================

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
# ---------------------------------------------------------------------
# GLOBAL STYLE (FONT + SIZE)
# ---------------------------------------------------------------------
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11
})
# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_CSV = BASE_DIR / "data" / "processed" / "LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv"

COLOR_T  = '#ff7f0e'
COLOR_ET = '#1f77b4'
LINE_COLOR = '#000000'
SMOOTH_DAYS = 7

ECO_YEARS = {
    "Year 1": ("2022-07-01", "2023-06-30"),
    "Year 2": ("2023-07-01", "2024-06-30"),
    "Year 3": ("2024-07-01", "2025-06-30"),
}

# ---------------------------------------------------------------------
def assign_eco_year(df):
    df = df.copy()
    df['eco_year'] = None
    for label, (start, end) in ECO_YEARS.items():
        mask = (df['TIMESTAMP'] >= start) & (df['TIMESTAMP'] <= end)
        df.loc[mask, 'eco_year'] = label
    return df

# ---------------------------------------------------------------------
def main():

    # ---------------- LOAD ----------------
    df = pd.read_csv(DATA_CSV, parse_dates=['TIMESTAMP'])
    df = df.sort_values('TIMESTAMP')

    # ---------------- CLEAN ----------------
    df['T'] = pd.to_numeric(df['T'], errors='coerce')
    df['E'] = pd.to_numeric(df['E'], errors='coerce')

    df = df.dropna(subset=['T','E'])
    df = df[(df['T'] >= 0) & (df['E'] >= 0)]

    # ---------------- COMPUTE ----------------
    df['ET'] = df['T'] + df['E']

    with np.errstate(divide='ignore', invalid='ignore'):
        df['T_frac'] = 100 * df['T'] / df['ET'].replace(0, np.nan)

    df['T_frac_smooth'] = (
        df['T_frac']
        .rolling(window=SMOOTH_DAYS, center=True, min_periods=1)
        .median()
    )

    df = assign_eco_year(df)

    # ---------------- PLOT ----------------
    fig, ax1 = plt.subplots(figsize=(13,5))

    # Fluxes
    ax1.fill_between(df['TIMESTAMP'], 0, df['ET'], color=COLOR_ET, step='mid')
    ax1.fill_between(df['TIMESTAMP'], 0, df['T'],  color=COLOR_T, step='mid')

    ax1.set_ylabel('Water flux (mm day$^{-1}$)')
    ax1.set_ylim(bottom=0)

    # Fraction axis
    ax2 = ax1.twinx()
    ax2.plot(df['TIMESTAMP'], df['T_frac_smooth'], color=LINE_COLOR, lw=1.1)
    ax2.axhline(50, color='gray', linestyle='--')
    ax2.set_ylim(0,100)
    ax2.set_ylabel('T/ET (%)')

    # ---------------- X AXIS LEVEL 1 (MONTHS) ----------------
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))

    # ---------------- X AXIS LEVEL 2 (ECO YEARS) ----------------
    year_centers = []
    year_labels = []

    for label, (start, end) in ECO_YEARS.items():
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        year_centers.append(start + (end - start)/2)
        year_labels.append(label)

    ax_bottom2 = ax1.secondary_xaxis('bottom')
    ax_bottom2.set_xticks(year_centers)
    ax_bottom2.set_xticklabels(year_labels, fontsize=11)

    ax_bottom2.spines['bottom'].set_position(('outward', 35))
    ax_bottom2.spines['bottom'].set_visible(False)
    ax_bottom2.tick_params(length=0)

    # ---------------- YEAR SEPARATION ----------------
    year_lines = [
        pd.to_datetime("2023-07-01"),
        pd.to_datetime("2024-07-01"),
    ]

    for d in year_lines:
        ax1.axvline(
            d,
            color='0.3',
            lw=1.2,
            ls='--',
            ymin=-0.08,
            ymax=1.0,
            clip_on=False,
            zorder=10
        )

    # ---------------- LEGENDS ----------------
    ax1.legend(handles=[
        Patch(facecolor=COLOR_ET, label='ET'),
        Patch(facecolor=COLOR_T, label='T')
    ], loc='upper center', ncol=2, frameon=False)

    ax2.legend(handles=[
        Line2D([0],[0], color=LINE_COLOR, label='T/ET'),
        Line2D([0],[0], color='gray', linestyle='--', label='50%')
    ], loc='upper right', frameon=False)

    fig.subplots_adjust(top=0.85, bottom=0.18)

    plt.show()

# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()

