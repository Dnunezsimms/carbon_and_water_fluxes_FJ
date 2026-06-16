"""
# =============================================================================
# Author      : Diego NÃºÃ±ez Simms
# Date        : 01-23-2026
# Version     : 1.0
# Description : Build colormap
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
# Author      : Diego NÃºÃ±ez Simms
# Date        : 01-23-2026
# Version     : 1.1
# Description : Correlation heatmap with robust REW computation
# =============================================================================

from pathlib import Path
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

# =============================================================================
# PATHS (PORTABLE)
# =============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_CSV = BASE_DIR / "data" / "processed" / "LEVEL3_FJ_merged_ET_T_WUE.csv"

# =============================================================================
# CONFIG
# =============================================================================

MIN_PAIRS = 10
ALPHA = None
APPLY_FDR = True

sns.set(style="white")

LABEL_MAP = {
    'SWC': 'SWC',
    'REW': 'REW',
    'TA_F': 'TA',
    'TS_prom': 'TS',
    'PPFD': 'PAR',
    'LW_IN_F': 'LW_IN'
}

TARGETS = ['NEE', 'GPP', 'RECO', 'ET', 'E', 'T']
DRIVERS = ['SWC', 'REW', 'TA_F', 'TS_prom', 'PPFD', 'LW_IN_F']

# =============================================================================
# LOAD DATA
# =============================================================================

def read_df(path):
    df = pd.read_csv(path, encoding='latin1', decimal=',', parse_dates=['TIMESTAMP'])
    df.columns = [c.strip() for c in df.columns]
    return df.set_index("TIMESTAMP").sort_index()

# =============================================================================
# DATA PREP
# =============================================================================

def coalesce_priority(df, names):
    s = pd.Series(np.nan, index=df.index)
    for n in names:
        if n in df.columns:
            s = s.combine_first(pd.to_numeric(df[n], errors='coerce'))
    return s


def ensure_columns(df):

    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    df['GPP']  = coalesce_priority(df, ['GPP', 'GPP_NT', 'GPP_DT'])
    df['RECO'] = coalesce_priority(df, ['RECO', 'RECO_NT', 'RECO_DT'])
    df['NEE']  = coalesce_priority(df, ['NEE', 'NEE_F', 'NEE_F2'])
    df['ET']   = coalesce_priority(df, ['ET', 'ET_F', 'ET_F2'])

    ts_cols  = [c for c in df.columns if c.startswith('TS_')]
    #swc_cols = [c for c in df.columns if c.startswith('SWC_')]

    if ts_cols:
        df['TS_prom'] = df[ts_cols].mean(axis=1)

    # SWC: promedio SWC_F* o SWC_*
    swcf = [c for c in df.columns if c.startswith('SWC_F')]
    swc = [c for c in df.columns if c.startswith('SWC_') and c not in swcf]
    if 'SWC' not in df.columns or df['SWC'].isna().all():
        cand = swcf if swcf else swc
        if cand:
            df['SWC'] = df[cand].mean(axis=1)

    # REW desde SWC
    pmp, cc = 0.05532005, 0.064879662
    if 'SWC' in df.columns:
        df['REW'] = ((df['SWC'] - pmp) / (cc - pmp)).clip(0, 1)
    return df

    # --- REW (percentile-based, portable) ---
#    swc = df['SWC']
#    theta_wp = np.nanpercentile(swc, 5)
#    theta_fc = np.nanpercentile(swc, 95)
#    df['REW'] = ((swc - theta_wp) / (theta_fc - theta_wp)).clip(0, 1)



# =============================================================================
# CORRELATION
# =============================================================================

def compute_pairwise_R_P(df, drivers, targets, min_pairs):
    R = pd.DataFrame(index=drivers, columns=targets)
    P = pd.DataFrame(index=drivers, columns=targets)
    N = pd.DataFrame(index=drivers, columns=targets)

    for d in drivers:
        for t in targets:
            sub = df[[d, t]].dropna()
            n = len(sub)
            N.loc[d, t] = n
            if n >= min_pairs:
                r, p = stats.pearsonr(sub[d], sub[t])
                R.loc[d, t] = r
                P.loc[d, t] = p
            else:
                R.loc[d, t] = np.nan
                P.loc[d, t] = np.nan
    return R.astype(float), P.astype(float), N.astype(int)

# =============================================================================
# PLOT
# =============================================================================

def plot_heatmap(R, P, N):

    cmap = LinearSegmentedColormap.from_list(
        'rwb', ['#8B0000', '#FFFFFF', '#0004FF']
    )
    norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)

    mask = (N < MIN_PAIRS) | R.isna()

    fig, ax = plt.subplots(figsize=(10, 6))
    mesh = ax.pcolormesh(R.values, cmap=cmap, norm=norm, shading='auto')

    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            if not mask.iloc[i, j]:
                ax.text(j + 0.5, i + 0.5, f"{R.iloc[i,j]:.2f}",
                        ha='center', va='center',
                        color='white' if abs(R.iloc[i,j]) > 0.5 else 'black')

    ax.set_xticks(np.arange(len(R.columns)) + 0.5)
    ax.set_yticks(np.arange(len(R.index)) + 0.5)
    ax.set_xticklabels([LABEL_MAP.get(c, c) for c in R.columns])
    ax.set_yticklabels([LABEL_MAP.get(r, r) for r in R.index])

    fig.colorbar(mesh, ax=ax, label="Pearson r")
    plt.tight_layout()
    plt.show()

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("Inicio:", datetime.now().isoformat())
    df = read_df(DATA_CSV)
    df = df.loc["2022-07-01":"2025-06-30"]
    df = ensure_columns(df)

    drivers = [d for d in DRIVERS if d in df.columns]
    targets = [t for t in TARGETS if t in df.columns]

    R, P, N = compute_pairwise_R_P(df, drivers, targets, MIN_PAIRS)
    plot_heatmap(R, P, N)

    print("Fin:", datetime.now().isoformat())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)

