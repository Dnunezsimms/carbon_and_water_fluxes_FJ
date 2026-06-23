from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd


ROOT = Path(r"C:\projects\carbon_and_water_fluxes_FJ_public")
DATA_CSV = ROOT / "data" / "processed" / "LEVEL3_FJ_2022_2025_ss_v4_daily.csv"
OUT_DIR = ROOT / "results" / "figures"
PNG_OUT = OUT_DIR / "figure_5.png"
PNG_OUT_RECONSTRUCTED = OUT_DIR / "figure_5_par_reconstructed.png"
PNG_OUT_BLANK = OUT_DIR / "figure_5_par_not_reconstructed.png"

X_START = pd.Timestamp("2022-07-01")
X_END = pd.Timestamp("2025-07-30")
YEAR_LINES = [pd.Timestamp("2023-07-01"), pd.Timestamp("2024-07-01")]
PROMINENT_PERIODS = [
    ("2023-05-05", "2023-06-21"),
    ("2024-09-16", "2024-11-24"),
    ("2025-05-29", "2025-06-08"),
]
PROXIES = [
    "SW_IN",
    "SW_IN_F",
    "NETRAD",
    "NETRAD_F",
    "LW_IN",
    "LW_IN_F",
    "LW_OUT",
    "LW_OUT_F",
    "TA",
    "TA_F",
]
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

    ax_bottom = ax.secondary_xaxis("bottom")
    ax_bottom.set_xticks(year_centers)
    ax_bottom.set_xticklabels(labels, fontsize=12)
    ax_bottom.spines["bottom"].set_position(("outward", 35))
    ax_bottom.spines["bottom"].set_visible(False)
    ax_bottom.tick_params(length=0)


def fit_linear_models(df: pd.DataFrame, proxies: list[str]) -> pd.DataFrame:
    par = df["PPFD_sum"]
    rows = []

    for proxy in proxies:
        if proxy not in df.columns:
            continue

        sub = pd.DataFrame({"proxy": df[proxy], "par": par}).dropna()
        sub = sub[sub["par"] > 0]
        if len(sub) < 30:
            continue

        x = sub["proxy"].to_numpy()
        y = sub["par"].to_numpy()
        factor_origin = float((x @ y) / (x @ x))
        y_hat_origin = factor_origin * x
        ss_tot = ((y - y.mean()) ** 2).sum()
        r2_origin = 1 - ((y - y_hat_origin) ** 2).sum() / ss_tot
        rmse_origin = float(np.sqrt(((y - y_hat_origin) ** 2).mean()))

        rows.append(
            {
                "proxy": proxy,
                "n": len(sub),
                "factor_origin": factor_origin,
                "r2_origin": float(r2_origin),
                "rmse_origin": rmse_origin,
            }
        )

    return pd.DataFrame(rows).sort_values("r2_origin", ascending=False)


def build_par_series(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    fits = fit_linear_models(df, PROXIES)
    best = fits.loc[fits["proxy"] == "SW_IN_F"].iloc[0]
    factor = float(best["factor_origin"])

    par_blank = df["PPFD_sum"].copy()
    par_blank = par_blank.where(par_blank > 0)
    par_final = par_blank.copy()

    for start, end in PROMINENT_PERIODS:
        sl = slice(pd.Timestamp(start), pd.Timestamp(end))
        par_est = (factor * pd.to_numeric(df.loc[sl, "SW_IN_F"], errors="coerce")).clip(lower=0)
        par_final.loc[sl] = par_est

    return par_final, par_blank


def render_figure(df: pd.DataFrame, par: pd.Series, output_path: Path) -> None:
    ta = df["TA_F"]
    nee = df["NEE_F2"]
    gpp = df["GPP_NT"].clip(lower=0)
    reco = df["RECO_NT"]
    swc = df[["SWC_F_1_1_1", "SWC_F_2_1_1", "SWC_F_3_1_1"]].mean(axis=1)
    theta_wp = 0.05532005
    theta_fc = 0.064879662
    rew = ((swc - theta_wp) / (theta_fc - theta_wp)).clip(0, 1)

    fig = plt.figure(figsize=(14, 7.4))
    gs = GridSpec(3, 1, height_ratios=[1.1, 3, 0.8], hspace=0.0)

    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex=ax0)
    ax2 = fig.add_subplot(gs[2], sharex=ax0)

    ta_line = ax0.plot(df.index, ta, color="#d54c45", lw=1.1, label="Ta")[0]
    ax0.set_ylabel("Ta\n($^\\circ$C)", color="#d54c45")
    ax0.tick_params(axis="y", labelcolor="#d54c45")
    ax0.text(0.005, 0.90, "a)", transform=ax0.transAxes, fontsize=13, fontweight="bold")

    ax0_r = ax0.twinx()
    par_line = ax0_r.plot(df.index, par, color="black", lw=0.9, label="PAR")[0]
    ax0_r.set_ylabel("PAR\n(mol m$^{-2}$ day$^{-1}$)")
    leg0 = ax0.legend(
        handles=[ta_line, par_line],
        ncol=2,
        loc="upper center",
        bbox_to_anchor=(0.64, 0.97),
        frameon=True,
        facecolor="white",
        framealpha=1.0,
        edgecolor="0.85",
        columnspacing=1.4,
        handlelength=2.1,
    )

    ax1.plot(df.index, gpp, color="0.5", lw=1.0, label="GPP")
    ax1.plot(df.index, reco, color="orange", lw=1.0, label="Reco")
    ax1.fill_between(df.index, 0, nee, where=nee < 0, color="steelblue", alpha=0.8)
    ax1.fill_between(df.index, 0, nee, where=nee > 0, color="tomato", alpha=0.8)
    ax1.axhline(0, color="k", lw=0.8)
    ax1.set_ylabel("Carbon flux (g C m$^{-2}$ day$^{-1}$)")
    ax1.text(0.005, 0.94, "b)", transform=ax1.transAxes, fontsize=13, fontweight="bold")
    leg1 = ax1.legend(
        handles=[
            Line2D([0], [0], color="0.5", lw=1.0, label="GPP"),
            Line2D([0], [0], color="orange", lw=1.0, label="Reco"),
            Patch(facecolor="steelblue", edgecolor="none", alpha=0.8, label="NEE sink"),
            Patch(facecolor="tomato", edgecolor="none", alpha=0.8, label="NEE source"),
        ],
        ncol=4,
        loc="upper center",
        bbox_to_anchor=(0.52, 1.00),
        frameon=True,
        facecolor="white",
        framealpha=1.0,
        edgecolor="0.85",
        columnspacing=1.5,
        handlelength=2.0,
    )

    ax2.fill_between(df.index, 0, rew, color="0.6")
    ax2.set_ylim(0, 1)
    ax2.set_yticks([])
    ax2.text(0.005, 1.02, "c)", transform=ax2.transAxes, fontsize=13, fontweight="bold")

    ax2_r = ax2.twinx()
    ax2_r.set_ylabel("REW (-)")
    ax2_r.set_ylim(0, 1)

    for ax in [ax0, ax1, ax2]:
        apply_month_ticks(ax, show_labels=(ax is ax2))
        ax.set_xlim(X_START, X_END)
        ax.margins(x=0)

    add_secondary_year_axis(ax2)

    for d in YEAR_LINES:
        for ax in [ax0, ax1, ax2]:
            ax.axvline(d, color="0.3", lw=1.2, ls="--", ymin=-0.08, ymax=1.0, clip_on=False, zorder=10)

    leg0.set_zorder(30)
    leg1.set_zorder(30)

    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(output_path, dpi=450, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output_path}")


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

    df = pd.read_csv(DATA_CSV)
    df.index = pd.to_datetime(df.iloc[:, 0], errors="coerce")
    df = df.loc[(df.index >= X_START) & (df.index <= X_END)].copy()

    numeric_cols = set(
        PROXIES
        + [
            "PPFD_sum",
            "NEE_F2",
            "GPP_NT",
            "RECO_NT",
            "SWC_F_1_1_1",
            "SWC_F_2_1_1",
            "SWC_F_3_1_1",
            "TA_F",
        ]
    )
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    par_reconstructed, par_blank = build_par_series(df)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    render_figure(df, par_reconstructed, PNG_OUT)
    render_figure(df, par_reconstructed, PNG_OUT_RECONSTRUCTED)
    render_figure(df, par_blank, PNG_OUT_BLANK)


if __name__ == "__main__":
    main()
