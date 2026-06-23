from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


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
OUTPUT_FINAL = OUTPUT_DIR / "Figure5_PAR_final.png"
OUTPUT_FINAL_BLANK = OUTPUT_DIR / "Figure5_PAR_final_blank.png"

X_START = pd.Timestamp("2022-07-01")
X_END = pd.Timestamp("2025-07-30")
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

YEAR_LINES = [pd.Timestamp("2023-07-01"), pd.Timestamp("2024-07-01")]


def load_daily_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_CSV)
    df.index = pd.to_datetime(df.iloc[:, 0], errors="coerce")
    df = df.loc[(df.index >= X_START) & (df.index <= X_END)].copy()

    for column in set(
        PROXIES
        + [
            "PPFD_sum",
            "PPFD",
            "P_RAIN",
            "NEE_F2",
            "GPP_NT",
            "RECO_NT",
            "SWC_F_1_1_1",
            "SWC_F_2_1_1",
            "SWC_F_3_1_1",
        ]
    ):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


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
        slope, intercept = np.polyfit(x, y, 1)
        y_hat = intercept + slope * x
        ss_tot = ((y - y.mean()) ** 2).sum()
        r2 = 1 - ((y - y_hat) ** 2).sum() / ss_tot
        rmse = float(np.sqrt(((y - y_hat) ** 2).mean()))

        factor_origin = float((x @ y) / (x @ x))
        y_hat_origin = factor_origin * x
        r2_origin = 1 - ((y - y_hat_origin) ** 2).sum() / ss_tot
        rmse_origin = float(np.sqrt(((y - y_hat_origin) ** 2).mean()))

        rows.append(
            {
                "proxy": proxy,
                "n": len(sub),
                "slope": float(slope),
                "intercept": float(intercept),
                "r2": float(r2),
                "rmse": rmse,
                "factor_origin": factor_origin,
                "r2_origin": float(r2_origin),
                "rmse_origin": rmse_origin,
            }
        )

    return pd.DataFrame(rows).sort_values("r2", ascending=False)


def select_par_proxy_model(df: pd.DataFrame) -> dict[str, float | str]:
    fits = fit_linear_models(df, PROXIES)
    best = fits.loc[fits["proxy"] == "SW_IN_F"].iloc[0]
    return {
        "proxy": "SW_IN_F",
        "factor_origin": float(best["factor_origin"]),
        "r2_origin": float(best["r2_origin"]),
        "rmse_origin": float(best["rmse_origin"]),
    }


def build_plotting_series(df: pd.DataFrame, reconstruction_model: dict[str, float | str]) -> dict[str, pd.Series]:
    par_raw = df["PPFD_sum"].copy()
    par_observed = par_raw.where(par_raw > 0)
    par_reconstructed_only = pd.Series(np.nan, index=df.index, dtype=float)

    factor = float(reconstruction_model["factor_origin"])
    proxy = str(reconstruction_model["proxy"])

    for start, end in PROMINENT_PERIODS:
        sl = slice(pd.Timestamp(start), pd.Timestamp(end))
        par_observed.loc[sl] = np.nan
        par_est = (factor * df.loc[sl, proxy]).clip(lower=0)
        par_reconstructed_only.loc[sl] = par_est

    swc = df[["SWC_F_1_1_1", "SWC_F_2_1_1", "SWC_F_3_1_1"]].mean(axis=1)
    theta_wp = 0.05532005
    theta_fc = 0.064879662
    rew = ((swc - theta_wp) / (theta_fc - theta_wp)).clip(0, 1)

    return {
        "ta": df["TA_F"],
        "par_observed": par_observed,
        "par_reconstructed_only": par_reconstructed_only,
        "gpp": df["GPP_NT"].clip(lower=0),
        "reco": df["RECO_NT"],
        "nee": df["NEE_F2"],
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


def render_figure(
    df: pd.DataFrame,
    series: dict[str, pd.Series],
    output_path: Path,
    reconstruction_model: dict[str, float | str],
    show_reconstruction: bool,
) -> None:
    fig = plt.figure(figsize=(14, 7.4))
    gs = GridSpec(3, 1, height_ratios=[1.1, 3, 0.8], hspace=0.0)

    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex=ax0)
    ax2 = fig.add_subplot(gs[2], sharex=ax0)

    ta_line = ax0.plot(df.index, series["ta"], color="#b24a2b", lw=1.1, label="Ta")[0]
    ax0.set_ylabel("Air temperature\n(Ta, °C)", color="#b24a2b")
    ax0.tick_params(axis="y", labelcolor="#b24a2b")
    ax0.text(0.005, 0.90, "a)", transform=ax0.transAxes, fontsize=13, fontweight="bold")
    ax0.spines["bottom"].set_visible(False)
    ax0.tick_params(labelbottom=False)

    ax0_r = ax0.twinx()
    par_obs = ax0_r.plot(df.index, series["par_observed"], color="black", lw=0.9, label="PAR observed")[0]
    handles = [ta_line, par_obs]
    if show_reconstruction:
        par_fill = ax0_r.plot(
            df.index,
            series["par_reconstructed_only"],
            color="#0f766e",
            lw=1.5,
            ls="--",
            label="PAR reconstructed",
        )[0]
        handles.append(par_fill)
    ax0_r.set_ylabel("PAR\n(mol m$^{-2}$ day$^{-1}$)")
    ax0_r.spines["top"].set_visible(False)
    ax0_r.spines["bottom"].set_visible(False)
    ax0.legend(
        handles=handles,
        ncol=len(handles),
        loc="upper center",
        bbox_to_anchor=(0.52, 1.18),
        frameon=True,
        facecolor="white",
        edgecolor="0.85",
        columnspacing=1.6,
        handlelength=2.2,
    )

    ax1.plot(df.index, series["gpp"], color="0.5", lw=1.0, label="GPP")
    ax1.plot(df.index, series["reco"], color="orange", lw=1.0, label="Reco")
    ax1.fill_between(df.index, 0, series["nee"], where=series["nee"] < 0, color="steelblue", alpha=0.8)
    ax1.fill_between(df.index, 0, series["nee"], where=series["nee"] > 0, color="tomato", alpha=0.8)
    ax1.axhline(0, color="k", lw=0.8)
    ax1.set_ylabel("Carbon flux (g C m$^{-2}$ day$^{-1}$)")
    ax1.text(0.005, 0.94, "b)", transform=ax1.transAxes, fontsize=13, fontweight="bold")
    ax1.legend(
        handles=[
            Line2D([0], [0], color="0.5", lw=1.0, label="GPP"),
            Line2D([0], [0], color="orange", lw=1.0, label="Reco"),
            Patch(facecolor="steelblue", edgecolor="none", alpha=0.8, label="NEE sink"),
            Patch(facecolor="tomato", edgecolor="none", alpha=0.8, label="NEE source"),
        ],
        ncol=4,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.02),
        frameon=True,
        facecolor="white",
        edgecolor="0.85",
        columnspacing=1.5,
        handlelength=2.0,
    )
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

    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_daily_data()
    reconstruction_model = select_par_proxy_model(df)
    series = build_plotting_series(df, reconstruction_model)
    render_figure(
        df,
        series,
        OUTPUT_FINAL,
        reconstruction_model=reconstruction_model,
        show_reconstruction=True,
    )
    render_figure(
        df,
        series,
        OUTPUT_FINAL_BLANK,
        reconstruction_model=reconstruction_model,
        show_reconstruction=False,
    )

    print(f"Saved: {OUTPUT_FINAL}")
    print(f"Saved: {OUTPUT_FINAL_BLANK}")
    print(
        f"PAR reconstruction: {reconstruction_model['proxy']} * {reconstruction_model['factor_origin']:.6f} "
        f"(R2={reconstruction_model['r2_origin']:.4f}, RMSE={reconstruction_model['rmse_origin']:.3f})"
    )


if __name__ == "__main__":
    main()
