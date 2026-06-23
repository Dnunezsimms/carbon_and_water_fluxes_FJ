from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


ROOT = Path(r"C:\projects\carbon_and_water_fluxes_FJ_public")
CLIMATE_CSV = ROOT / "data" / "processed" / "LEVEL3_FJ_2022_2025_ss_daily.csv"
TE_CSV = ROOT / "data" / "processed" / "LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv"
OUT_DIR = ROOT / "results" / "figures"
PNG_OUT = OUT_DIR / "figure_3_4_combined.png"

X_START = pd.Timestamp("2022-07-01")
X_END = pd.Timestamp("2025-07-30")
YEAR_LINES = [pd.Timestamp("2023-07-01"), pd.Timestamp("2024-07-01")]
ECO_YEARS = {
    "Year 1": ("2022-07-01", "2023-06-30"),
    "Year 2": ("2023-07-01", "2024-06-30"),
    "Year 3": ("2024-07-01", "2025-07-30"),
}


def apply_month_ticks(ax: plt.Axes, show_labels: bool) -> None:
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[7, 10, 1, 4], bymonthday=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.tick_params(axis="x", which="major", length=6, width=0.9, bottom=True, labelbottom=show_labels)
    ax.tick_params(axis="x", which="minor", length=3.5, width=0.8, bottom=True)


def add_secondary_year_axis(ax: plt.Axes) -> None:
    year_centers = []
    labels = []
    for label, (start, end) in ECO_YEARS.items():
        start_ts = pd.Timestamp(start)
        end_ts = pd.Timestamp(end)
        start_clip = max(start_ts, X_START)
        end_clip = min(end_ts, X_END)
        year_centers.append(start_clip + (end_clip - start_clip) / 2)
        labels.append(label)

    ax2 = ax.secondary_xaxis("bottom")
    ax2.set_xticks(year_centers)
    ax2.set_xticklabels(labels, fontsize=12)
    ax2.spines["bottom"].set_position(("outward", 35))
    ax2.spines["bottom"].set_visible(False)
    ax2.tick_params(length=0)


def add_year_lines(axes: list[plt.Axes]) -> None:
    for d in YEAR_LINES:
        for ax in axes:
            ax.axvline(d, color="0.3", lw=1.2, ls="--", ymin=-0.08, ymax=1.0, clip_on=False, zorder=10)


def add_panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(0.01, 0.88, label, transform=ax.transAxes, fontsize=13, fontweight="bold")


def main() -> None:
    plt.rcParams.update(
        {
            "font.size": 12,
            "axes.labelsize": 13,
            "axes.titlesize": 14,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "legend.fontsize": 11,
        }
    )

    climate = pd.read_csv(CLIMATE_CSV)
    climate["TIMESTAMP"] = pd.to_datetime(climate["TIMESTAMP"], errors="coerce")
    climate = climate[(climate["TIMESTAMP"] >= X_START) & (climate["TIMESTAMP"] <= X_END)].copy()
    climate["VPD_kPa"] = pd.to_numeric(climate["VPD_F"], errors="coerce") / 1000
    climate["SWC"] = climate[["SWC_F_1_1_1", "SWC_F_2_1_1", "SWC_F_3_1_1"]].mean(axis=1)
    climate["P_RAIN"] = pd.to_numeric(climate["P_RAIN"], errors="coerce")

    te = pd.read_csv(TE_CSV, parse_dates=["TIMESTAMP"]).sort_values("TIMESTAMP")
    te = te[(te["TIMESTAMP"] >= X_START) & (te["TIMESTAMP"] <= X_END)].copy()
    te["T"] = pd.to_numeric(te["T"], errors="coerce")
    te["E"] = pd.to_numeric(te["E"], errors="coerce")
    te = te.dropna(subset=["T", "E"])
    te = te[(te["T"] >= 0) & (te["E"] >= 0)]
    te["ET"] = te["T"] + te["E"]
    with np.errstate(divide="ignore", invalid="ignore"):
        te["T_ET_pct"] = 100 * te["T"] / te["ET"].replace(0, np.nan)
    te["T_ET_pct_smooth"] = te["T_ET_pct"].rolling(window=7, center=True, min_periods=1).median()
    x_end_plot = te["TIMESTAMP"].max()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(14, 10.2))
    gs = gridspec.GridSpec(5, 1, height_ratios=[0.72, 1.9, 1.0, 0.9, 1.0], hspace=0.08)

    ax_vpd = fig.add_subplot(gs[0])
    ax_flux = fig.add_subplot(gs[1], sharex=ax_vpd)
    ax_ratio = fig.add_subplot(gs[2], sharex=ax_vpd)
    ax_prec = fig.add_subplot(gs[3], sharex=ax_vpd)
    ax_swc = fig.add_subplot(gs[4], sharex=ax_vpd)

    ax_vpd.plot(climate["TIMESTAMP"], climate["VPD_kPa"], color="black", lw=1.2)
    ax_vpd.set_ylabel("VPD\n(kPa)", fontsize=11)
    ax_vpd.yaxis.set_label_position("right")
    ax_vpd.yaxis.tick_right()
    add_panel_label(ax_vpd, "a)")
    ax_vpd.margins(y=0)

    ax_flux.fill_between(te["TIMESTAMP"], 0, te["ET"], color="#1f77b4", alpha=0.95, step="mid")
    ax_flux.fill_between(te["TIMESTAMP"], 0, te["T"], color="#ff7f0e", alpha=0.95, step="mid")
    ax_flux.set_ylabel("Water flux\n(mm day$^{-1}$)", fontsize=13)
    ax_flux.set_ylim(bottom=0)
    add_panel_label(ax_flux, "b)")
    ax_flux.margins(y=0)
    ax_flux.legend(
        handles=[
            Patch(facecolor="#1f77b4", label="ET"),
            Patch(facecolor="#ff7f0e", label="T"),
        ],
        loc="upper right",
        ncol=2,
        frameon=True,
        facecolor="white",
        edgecolor="0.85",
        bbox_to_anchor=(0.985, 0.82),
        columnspacing=1.4,
        handlelength=2.0,
    )

    ax_ratio.plot(te["TIMESTAMP"], te["T_ET_pct_smooth"], color="black", lw=1.2, label="T/ET")
    ax_ratio.axhline(50, color="gray", linestyle="--", lw=1.0, label="50%")
    ax_ratio.set_ylim(0, 100)
    ax_ratio.set_yticks([0, 20, 40, 60, 80, 100])
    ax_ratio.set_ylabel("T/ET\n(%)")
    add_panel_label(ax_ratio, "c)")
    ax_ratio.legend(
        handles=[
            Line2D([0], [0], color="black", lw=1.2, label="T/ET"),
            Line2D([0], [0], color="gray", linestyle="--", lw=1.0, label="50%"),
        ],
        loc="lower right",
        ncol=2,
        frameon=True,
        facecolor="white",
        edgecolor="0.85",
        bbox_to_anchor=(0.985, 0.08),
        columnspacing=1.4,
        handlelength=2.0,
    )

    ax_prec.bar(climate["TIMESTAMP"], climate["P_RAIN"], color="royalblue")
    ax_prec.set_ylabel("Precipitation\n(mm)", fontsize=11, color="royalblue")
    ax_prec.tick_params(axis="y", labelcolor="royalblue")
    ax_prec.set_ylim(bottom=0)
    ax_prec.margins(y=0)
    add_panel_label(ax_prec, "d)")

    ax_swc.plot(climate["TIMESTAMP"], climate["SWC"], color="black", lw=2.8)
    ax_swc.set_ylabel("SWC\n(m$^3$ m$^{-3}$)", fontsize=11)
    ax_swc.yaxis.set_label_position("right")
    ax_swc.yaxis.tick_right()
    ax_swc.margins(y=0)
    add_panel_label(ax_swc, "e)")

    for ax in [ax_vpd, ax_flux, ax_ratio, ax_prec, ax_swc]:
        apply_month_ticks(ax, show_labels=(ax is ax_swc))
        ax.set_xlim(X_START, x_end_plot)
        ax.margins(x=0)

    add_secondary_year_axis(ax_swc)
    add_year_lines([ax_vpd, ax_flux, ax_ratio, ax_prec, ax_swc])

    fig.align_ylabels([ax_vpd, ax_flux, ax_ratio, ax_prec, ax_swc])
    fig.subplots_adjust(top=0.97, bottom=0.14)
    fig.savefig(PNG_OUT, dpi=450, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {PNG_OUT}")


if __name__ == "__main__":
    main()
