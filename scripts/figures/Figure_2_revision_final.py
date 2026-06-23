from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(r"C:\projects\carbon_and_water_fluxes_FJ_public")
DATA_XLSX = ROOT / "data" / "processed" / "rainfall_data_1984-2025_updated.xlsx"
OUT_DIR = ROOT / "results" / "figures"
PNG_OUT = OUT_DIR / "figure_2.png"


def main() -> None:
    df = pd.read_excel(DATA_XLSX)
    year_col, month_col, precip_col = df.columns[:3]

    sub = df[[year_col, month_col, precip_col]].dropna(subset=[year_col]).copy()
    sub[year_col] = sub[year_col].astype(int)
    sub[month_col] = sub[month_col].astype(int)
    sub[precip_col] = pd.to_numeric(sub[precip_col], errors="coerce").fillna(0)

    annual = sub.groupby(year_col, as_index=False)[precip_col].sum()
    counts = sub.groupby(year_col)[month_col].nunique().reset_index(name="n_months")
    annual = annual.merge(counts, on=year_col, how="left")

    mean_mask = annual[year_col].between(1984, 2024) & (annual["n_months"] == 12)
    mean_40 = annual.loc[mean_mask, precip_col].mean()

    obs_years = {2022, 2023, 2024, 2025}
    base_color = "#2f79b4"
    obs_color = "#d97941"
    mean_color = "#4d4d4d"
    colors = [obs_color if y in obs_years else base_color for y in annual[year_col]]

    plt.rcParams.update(
        {
            "font.size": 12,
            "axes.labelsize": 12,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "legend.fontsize": 10,
        }
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 5))

    ax.bar(
        annual[year_col],
        annual[precip_col],
        color=colors,
        width=0.82,
        edgecolor="none",
    )
    ax.axhline(
        mean_40,
        color=mean_color,
        linestyle="--",
        linewidth=1.6,
        label="40-year mean annual precipitation",
    )
    ax.scatter([], [], color=obs_color, marker="s", s=80, label="Observation years")

    ax.set_ylabel("Annual precipitation (mm)")
    year_min = int(annual[year_col].min())
    year_max = int(annual[year_col].max())
    ticks = list(range(year_min, year_max + 1, 5))
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticks, rotation=0)
    ax.set_ylim(0, max(annual[precip_col].max() * 1.12, mean_40 * 1.2))
    ax.legend(frameon=False, loc="upper right")
    ax.text(
        0.985,
        mean_40 / ax.get_ylim()[1] + 0.015,
        f"Mean = {mean_40:.1f} mm",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=10,
        color=mean_color,
    )

    fig.tight_layout()
    fig.savefig(PNG_OUT, dpi=450, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {PNG_OUT}")


if __name__ == "__main__":
    main()
