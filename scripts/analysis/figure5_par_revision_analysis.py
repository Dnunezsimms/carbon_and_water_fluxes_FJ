from pathlib import Path
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_CSV = BASE_DIR / "data" / "processed" / "LEVEL3_FJ_2022_2025_ss_v4_daily.csv"
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


def load_daily_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_CSV)
    df.index = pd.to_datetime(df.iloc[:, 0], errors="coerce")
    df = df.loc[(df.index >= X_START) & (df.index <= X_END)].copy()

    for column in set(PROXIES + ["PPFD_sum", "PPFD", "P_RAIN", "NEE_F2", "GPP_NT", "RECO_NT"]):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def detect_zero_runs(df: pd.DataFrame) -> pd.DataFrame:
    par = df["PPFD_sum"]
    is_zero = par.eq(0)
    run_id = (is_zero != is_zero.shift()).cumsum()
    rows = []

    for _, idx in is_zero.groupby(run_id).groups.items():
        sub_zero = is_zero.loc[idx]
        if not bool(sub_zero.iloc[0]):
            continue

        sub = df.loc[sub_zero.index]
        rows.append(
            {
                "start": sub_zero.index.min(),
                "end": sub_zero.index.max(),
                "days": len(sub_zero),
                "ppfd_nonnull": int(sub["PPFD"].notna().sum()) if "PPFD" in sub else 0,
                "sw_in_nonnull": int(sub["SW_IN"].notna().sum()) if "SW_IN" in sub else 0,
                "sw_in_f_nonnull": int(sub["SW_IN_F"].notna().sum()) if "SW_IN_F" in sub else 0,
                "netrad_nonnull": int(sub["NETRAD"].notna().sum()) if "NETRAD" in sub else 0,
                "netrad_f_nonnull": int(sub["NETRAD_F"].notna().sum()) if "NETRAD_F" in sub else 0,
                "ta_nonnull": int(sub["TA"].notna().sum()) if "TA" in sub else 0,
                "ta_f_nonnull": int(sub["TA_F"].notna().sum()) if "TA_F" in sub else 0,
                "gpp_mean": float(sub["GPP_NT"].mean()) if "GPP_NT" in sub else np.nan,
                "nee_mean": float(sub["NEE_F2"].mean()) if "NEE_F2" in sub else np.nan,
            }
        )

    return pd.DataFrame(rows).sort_values(["days", "start"], ascending=[False, True])


def fit_linear_models(df: pd.DataFrame, proxies: list[str]) -> pd.DataFrame:
    par = df["PPFD_sum"]
    valid_par = par.gt(0)
    rows = []

    for proxy in proxies:
        if proxy not in df.columns:
            continue

        sub = pd.DataFrame({"proxy": df[proxy], "par": par}).dropna()
        sub = sub[sub["par"] > 0]
        n = len(sub)
        if n < 30:
            continue

        x = sub["proxy"].to_numpy()
        y = sub["par"].to_numpy()
        slope, intercept = np.polyfit(x, y, 1)
        y_hat = intercept + slope * x
        ss_tot = ((y - y.mean()) ** 2).sum()
        r2 = 1 - ((y - y_hat) ** 2).sum() / ss_tot

        slope_origin = (x @ y) / (x @ x)
        y_hat_origin = slope_origin * x
        r2_origin = 1 - ((y - y_hat_origin) ** 2).sum() / ss_tot

        overlap = int((valid_par & df[proxy].notna()).sum())
        apt = "Yes" if (proxy == "SW_IN_F" and r2 >= 0.85) else "No"

        rows.append(
            {
                "proxy": proxy,
                "overlap_n": overlap,
                "n": n,
                "model": "PAR = intercept + slope * proxy",
                "slope": float(slope),
                "intercept": float(intercept),
                "r2": float(r2),
                "slope_origin": float(slope_origin),
                "r2_origin": float(r2_origin),
                "apt_for_imputation": apt,
            }
        )

    return pd.DataFrame(rows).sort_values("r2", ascending=False)


def fit_by_ecohydrological_year(df: pd.DataFrame, proxy: str) -> pd.DataFrame:
    par = df["PPFD_sum"]
    df = df.copy()
    df["eco_year"] = [ts.year if ts.month >= 7 else ts.year - 1 for ts in df.index]
    valid = par.gt(0) & df[proxy].notna()
    rows = []

    for eco_year in sorted(df["eco_year"].dropna().unique()):
        sub = df.loc[valid & (df["eco_year"] == eco_year), [proxy, "PPFD_sum"]]
        if len(sub) < 30:
            continue

        x = sub[proxy].to_numpy()
        y = sub["PPFD_sum"].to_numpy()
        slope, intercept = np.polyfit(x, y, 1)
        y_hat = intercept + slope * x
        r2 = 1 - ((y - y_hat) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        rows.append(
            {
                "eco_year": f"{eco_year}-{eco_year + 1}",
                "n": len(sub),
                "slope": float(slope),
                "intercept": float(intercept),
                "r2": float(r2),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    df = load_daily_data()
    print("Zero runs")
    print(detect_zero_runs(df).to_string(index=False))
    print()
    print("Proxy fits")
    print(fit_linear_models(df, PROXIES).to_string(index=False))
    print()
    print("SW_IN_F stability by ecohydrological year")
    print(fit_by_ecohydrological_year(df, "SW_IN_F").to_string(index=False))


if __name__ == "__main__":
    main()
