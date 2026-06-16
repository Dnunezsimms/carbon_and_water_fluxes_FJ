# =============================================================================
# FIGURE 2 â€” VPD, ET, Precipitation, SWC (double bottom axis fixed)
# =============================================================================

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
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
# ---------------- CONFIG ----------------
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "processed"
DATA_FILE = DATA_DIR / "LEVEL3_FJ_2022_2025_ss_daily.csv"

PRECIP_COLOR = "royalblue"
PRECIP_EDGE = "navy"
SWC_COLOR = "black"

ECO_YEARS = {
    "Year 1": ("2022-07-01", "2023-06-30"),
    "Year 2": ("2023-07-01", "2024-06-30"),
    "Year 3": ("2024-07-01", "2025-06-30"),
}

# ---------------------------------------------------------------------
def main():

    # ---------------- LOAD ----------------
    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.str.strip()

    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce")

    # ---------------- VARIABLES ----------------
    df["VPD_kPa"] = df["VPD_F"] / 1000
    df["SWC"] = df[[
        "SWC_F_1_1_1",
        "SWC_F_2_1_1",
        "SWC_F_3_1_1"
    ]].mean(axis=1)

    df_plot = df[[
        "TIMESTAMP","VPD_kPa","ET_F","SWC","P_RAIN"
    ]].dropna(subset=["TIMESTAMP"])

    # ðŸ”¥ CORTE REAL DEL DATASET (MEJOR QUE SOLO VISUAL)
    X_START = pd.to_datetime("2022-07-01")
    X_END   = pd.to_datetime("2025-07-30")

    df_plot = df_plot[
        (df_plot["TIMESTAMP"] >= X_START) &
        (df_plot["TIMESTAMP"] <= X_END)
    ]

    # ---------------- FIGURE ----------------
    fig = plt.figure(figsize=(14, 9))
    gs = gridspec.GridSpec(
        4, 1,
        height_ratios=[0.7, 2.0, 0.9, 1.1],
        hspace=0.06
    )

    ax_vpd = fig.add_subplot(gs[0])
    ax_et  = fig.add_subplot(gs[1], sharex=ax_vpd)
    ax_p   = fig.add_subplot(gs[2], sharex=ax_vpd)
    ax_swc = fig.add_subplot(gs[3], sharex=ax_vpd)

    # ---------------- VPD ----------------
    ax_vpd.plot(df_plot["TIMESTAMP"], df_plot["VPD_kPa"], color="black", lw=1.2)
    ax_vpd.set_ylabel("VPD\n(kPa)", fontsize=11)
    ax_vpd.yaxis.set_label_position("right")
    ax_vpd.yaxis.tick_right()
    ax_vpd.set_xticks([])
    ax_vpd.spines["bottom"].set_visible(False)
    ax_vpd.margins(y=0)

    # ---------------- ET ----------------
    ax_et.fill_between(df_plot["TIMESTAMP"], 0, df_plot["ET_F"], color="C0", alpha=0.95, step="mid")
    ax_et.set_ylabel("ET\n(mm day$^{-1}$)", fontsize=13)
    ax_et.spines["top"].set_visible(False)
    ax_et.spines["bottom"].set_visible(False)
    ax_et.set_xticks([])
    ax_et.set_ylim(bottom=0)
    ax_et.margins(y=0)

    # ---------------- PRECIP ----------------
    ax_p.bar(df_plot["TIMESTAMP"], df_plot["P_RAIN"], color=PRECIP_COLOR)
    ax_p.set_ylabel("Precipitation\n(mm)", fontsize=11, color=PRECIP_COLOR)
    ax_p.tick_params(axis="y", labelcolor=PRECIP_COLOR)
    ax_p.set_ylim(bottom=0)
    ax_p.margins(y=0)
    ax_p.set_xticks([])

    # ---------------- SWC ----------------
    ax_swc.plot(df_plot["TIMESTAMP"], df_plot["SWC"], color=SWC_COLOR, lw=2.8)
    ax_swc.set_ylabel("SWC\n(mÂ³ mâ»Â³)", fontsize=11)
    ax_swc.yaxis.set_label_position("right")
    ax_swc.yaxis.tick_right()
    ax_swc.margins(y=0)

    # ---------------- X AXIS LEVEL 1 (MONTHS) ----------------
    ax_swc.xaxis.set_major_locator(
        mdates.MonthLocator(bymonth=[7, 10, 1, 4])
)
    ax_swc.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))

    # ---------------- X AXIS LEVEL 2 (ECO YEARS) ----------------
    year_centers = []
    year_labels = []

    for label, (start, end) in ECO_YEARS.items():
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        if end < X_START or start > X_END:
            continue

        start_clip = max(start, X_START)
        end_clip   = min(end, X_END)

        year_centers.append(start_clip + (end_clip - start_clip)/2)
        year_labels.append(label)

    ax_bottom2 = ax_swc.secondary_xaxis('bottom')
    ax_bottom2.set_xticks(year_centers)
    ax_bottom2.set_xticklabels(year_labels, fontsize=12)

    ax_bottom2.spines['bottom'].set_position(('outward', 35))
    ax_bottom2.spines['bottom'].set_visible(False)
    ax_bottom2.tick_params(length=0)

    # ---------------- YEAR SEPARATION ----------------
    year_lines = [
        pd.to_datetime("2023-07-01"),
        pd.to_datetime("2024-07-01"),
    ]

    for d in year_lines:
        if X_START <= d <= X_END:
            for ax in [ax_vpd, ax_et, ax_p, ax_swc]:
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

    # ---------------- LIMITS ----------------
    for ax in [ax_vpd, ax_et, ax_p, ax_swc]:
        ax.set_xlim(X_START, X_END)
        ax.margins(x=0)

    # ---------------- FINAL (MISMO ESTILO ORIGINAL) ----------------
    fig.align_ylabels([ax_vpd, ax_et, ax_p, ax_swc])
    fig.subplots_adjust(top=0.96, bottom=0.14)

    plt.show()
# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()


