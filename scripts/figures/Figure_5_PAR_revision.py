from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates


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

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_CSV = BASE_DIR / "data" / "processed" / "LEVEL3_FJ_2022_2025_ss_v4_daily.csv"
OUTPUT_DIR = BASE_DIR / "results" / "figures"
OUTPUT_FIG = OUTPUT_DIR / "Figure5_PAR_cleaned.png"
OUTPUT_COMPARISON = OUTPUT_DIR / "Figure5_PAR_original_vs_cleaned.png"

X_START = pd.Timestamp("2022-07-01")
X_END = pd.Timestamp("2025-07-30")
KNOWN_PAR_DATA_GAPS = [
    ("2023-05-05", "2023-06-21"),
    ("2024-09-16", "2024-11-24"),
    ("2025-05-29", "2025-06-08"),
]

ECO_YEARS = {
    "Year 1": ("2022-07-01", "2023-06-30"),
    "Year 2": ("2023-07-01", "2024-06-30"),
    "Year 3": ("2024-07-01", "2025-07-30"),
}

YEAR_LINES = [
    pd.Timestamp("2023-07-01"),
    pd.Timestamp("2024-07-01"),
]


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_CSV)
    df.index = pd.to_datetime(df.iloc[:, 0], errors="coerce")
    df = df.loc[(df.index >= X_START) & (df.index <= X_END)].copy()

    numeric_cols = [
        "PPFD_sum",
        "NEE_F2",
        "GPP_NT",
        "RECO_NT",
        "SWC_F_1_1_1",
        "SWC_F_2_1_1",
        "SWC_F_3_1_1",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def build_series(df: pd.DataFrame) -> dict[str, pd.Series]:
    par_raw = df["PPFD_sum"].copy()
    par_clean = par_raw.where(par_raw > 0)

    for start, end in KNOWN_PAR_DATA_GAPS:
        par_clean.loc[pd.Timestamp(start) : pd.Timestamp(end)] = np.nan

    gpp = df["GPP_NT"].clip(lower=0)
    reco = df["RECO_NT"]
    nee = df["NEE_F2"]
    swc = df[["SWC_F_1_1_1", "SWC_F_2_1_1", "SWC_F_3_1_1"]].mean(axis=1)

    theta_wp = 0.05532005
    theta_fc = 0.064879662
    rew = ((swc - theta_wp) / (theta_fc - theta_wp)).clip(0, 1)

    return {
        "par_raw": par_raw,
        "par_clean": par_clean,
        "gpp": gpp,
        "reco": reco,
        "nee": nee,
        "rew": rew,
    }


def add_common_x_axis(ax2: plt.Axes) -> None:
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))

    year_centers = []
    year_labels = []
    for label, (start, end) in ECO_YEARS.items():
        start = pd.Timestamp(start)
        end = pd.Timestamp(end)
        start_clip = max(start, X_START)
        end_clip = min(end, X_END)
        year_centers.append(start_clip + (end_clip - start_clip) / 2)
        year_labels.append(label)

    ax_bottom2 = ax2.secondary_xaxis("bottom")
    ax_bottom2.set_xticks(year_centers)
    ax_bottom2.set_xticklabels(year_labels, fontsize=12)
    ax_bottom2.spines["bottom"].set_position(("outward", 35))
    ax_bottom2.spines["bottom"].set_visible(False)
    ax_bottom2.tick_params(length=0)


def add_year_lines(axes: list[plt.Axes]) -> None:
    for date in YEAR_LINES:
        for ax in axes:
            ax.axvline(
                date,
                color="0.3",
                lw=1.2,
                ls="--",
                ymin=-0.08,
                ymax=1.0,
                clip_on=False,
                zorder=10,
            )


def save_cleaned_figure(df: pd.DataFrame, series: dict[str, pd.Series]) -> None:
    fig = plt.figure(figsize=(14, 7))
    gs = GridSpec(3, 1, height_ratios=[1, 3, 0.8], hspace=0.0)

    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex=ax0)
    ax2 = fig.add_subplot(gs[2], sharex=ax0)

    ax0.plot(df.index, series["par_clean"], color="black", lw=0.8)
    ax0.text(0.005, 0.90, "a)", transform=ax0.transAxes, fontsize=13, fontweight="bold")
    ax0.spines["bottom"].set_visible(False)
    ax0.tick_params(labelbottom=False)
    ax0_r = ax0.twinx()
    ax0_r.set_ylabel("PAR\n(mol m$^{-2}$ day$^{-1}$)")
    ax0_r.set_ylim(ax0.get_ylim())
    ax0_r.spines["top"].set_visible(False)
    ax0_r.spines["bottom"].set_visible(False)

    ax1.plot(df.index, series["gpp"], color="0.5", lw=1.0, label="GPP")
    ax1.plot(df.index, series["reco"], color="orange", lw=1.0, label="Reco")
    ax1.fill_between(df.index, 0, series["nee"], where=series["nee"] < 0, color="steelblue", alpha=0.8)
    ax1.fill_between(df.index, 0, series["nee"], where=series["nee"] > 0, color="tomato", alpha=0.8)
    ax1.axhline(0, color="k", lw=0.8)
    ax1.set_ylabel("Carbon flux (g C m$^{-2}$ day$^{-1}$)")
    ax1.text(0.005, 0.94, "b)", transform=ax1.transAxes, fontsize=13, fontweight="bold")
    ax1.legend(ncol=4, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.02))
    ax1.spines["bottom"].set_visible(False)
    ax1.tick_params(labelbottom=False)

    ax2.fill_between(df.index, 0, series["rew"], color="0.6")
    ax2.set_ylim(0, 1)
    ax2.set_yticks([])
    ax2.text(0.005, 1.02, "c)", transform=ax2.transAxes, fontsize=13, fontweight="bold")
    ax2_r = ax2.twinx()
    ax2_r.set_ylabel("REW (-)")
    ax2_r.set_ylim(0, 1)

    add_common_x_axis(ax2)
    add_year_lines([ax0, ax1, ax2])

    for ax in [ax0, ax1, ax2]:
        ax.set_xlim(X_START, X_END)
        ax.margins(x=0)

    fig.tight_layout()
    fig.savefig(OUTPUT_FIG, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_comparison_figure(df: pd.DataFrame, series: dict[str, pd.Series]) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(14, 5), sharex=True, constrained_layout=True)

    axes[0].plot(df.index, series["par_raw"], color="black", lw=0.8)
    axes[0].set_ylabel("PAR raw")
    axes[0].set_title("Original PPFD_sum series")

    axes[1].plot(df.index, series["par_clean"], color="black", lw=0.8)
    axes[1].set_ylabel("PAR clean")
    axes[1].set_title("Plotting series with PPFD_sum <= 0 masked as missing")
    axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))

    for ax in axes:
        ax.set_xlim(X_START, X_END)
        for start, end in KNOWN_PAR_DATA_GAPS:
            ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), color="tomato", alpha=0.08, lw=0)

    fig.savefig(OUTPUT_COMPARISON, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    series = build_series(df)
    save_cleaned_figure(df, series)
    save_comparison_figure(df, series)
    print(f"Saved: {OUTPUT_FIG}")
    print(f"Saved: {OUTPUT_COMPARISON}")


if __name__ == "__main__":
    main()
