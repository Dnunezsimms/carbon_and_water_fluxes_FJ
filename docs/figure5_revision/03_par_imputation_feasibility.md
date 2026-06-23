# PAR imputation feasibility

Date: 2026-06-17

## Objective

Evaluate whether the three conspicuous PAR zero periods in Figure 5 can be defensibly imputed from a proxy variable, instead of being left blank.

## Candidate proxies reviewed

Primary radiative candidates present in the daily dataset:

- `SW_IN`
- `SW_IN_F`
- `NETRAD`
- `NETRAD_F`
- `LW_IN`
- `LW_IN_F`
- `LW_OUT`
- `LW_OUT_F`

Secondary temperature candidates reviewed only as weak fallback diagnostics:

- `TA`
- `TA_F`

## Summary table

| Proxy | Period overlap with valid PAR | n | Model | R² | Observations | Apta para imputación |
|---|---|---:|---|---:|---|---|
| `SW_IN_F` | Full overlap on valid days; full coverage inside the 3 target gaps | 988 | Linear | 0.8798 | Best candidate overall; physically sensible PAR proxy; but temporal stability weakens in May-Jun | Conditionally, but not adopted |
| `NETRAD_F` | Full overlap on valid days; full coverage inside the 3 target gaps | 988 | Linear | 0.8269 | Good but clearly weaker than `SW_IN_F` | No |
| `SW_IN` | Good overlap where observed, but no coverage inside target gaps | 962 | Linear | 0.7724 | Reasonable relation, but unusable for the actual missing intervals | No |
| `NETRAD` | Good overlap where observed, but no coverage inside target gaps | 963 | Linear | 0.4838 | Weak relation and no coverage in target gaps | No |
| `LW_OUT` | Good overlap where observed | 988 | Linear | 0.5910 | Indirect proxy only; lower explanatory power | No |
| `LW_OUT_F` | Good overlap where observed | 988 | Linear | 0.5880 | Indirect proxy only; lower explanatory power | No |
| `TA_F` | Good overlap where observed; full coverage in target gaps | 988 | Linear | 0.3585 | Too weak for defensible PAR gap-filling | No |
| `TA` | Partial overlap where observed | 988 | Linear | 0.3550 | Too weak for defensible PAR gap-filling | No |
| `LW_IN` | Good overlap where observed | 988 | Linear | 0.0098 | Not informative for PAR reconstruction | No |
| `LW_IN_F` | Good overlap where observed; full coverage in target gaps | 988 | Linear | 0.0087 | Not informative for PAR reconstruction | No |

## Best candidate: `SW_IN_F`

Global linear fit using all valid days:

- Model: `PAR = 0.928 + 0.1384 * SW_IN_F`
- `n = 988`
- `R² = 0.8798`

Forced-through-origin alternative:

- Model: `PAR = 0.1414 * SW_IN_F`
- `R² = 0.8793`

Interpretation:

- The intercept is small relative to the observed PAR range.
- A simple linear model is physically plausible because PAR and shortwave radiation should scale closely.
- `SW_IN_F` is the only candidate that both covers the gap periods and shows strong overall explanatory power.

## Stability check for `SW_IN_F`

By ecohydrological year:

| Eco year | n | Slope | Intercept | R² |
|---|---:|---:|---:|---:|
| 2022-2023 | 312 | 0.1740 | -2.994 | 0.9109 |
| 2023-2024 | 365 | 0.1338 | 0.636 | 0.9886 |
| 2024-2025 | 281 | 0.1293 | -0.166 | 0.9353 |
| 2025-2026* | 30 | 0.1350 | -0.596 | 0.9866 |

\* truncated end window only.

Key point:

- The 2022-2023 slope is materially steeper than the later years.
- This matters because one of the target gaps falls in May-Jun 2023, and another in May-Jun 2025.

Seasonal behavior relevant to the target gaps:

- May-Jun pooled fit:
  - slope = `0.1369`
  - intercept = `-1.314`
  - `R² = 0.7223`
- Sep-Nov pooled fit:
  - slope = `0.1211`
  - intercept = `7.442`
  - `R² = 0.8339`

This is the main technical concern: the relation remains useful, but it is clearly weaker in May-Jun than in the full dataset.

## Predicted PAR magnitudes for the three target periods using `SW_IN_F`

Using the season-appropriate simple linear fit:

| Period | Proxy season | Predicted mean PAR | Predicted min | Predicted max | Nearby observed PAR mean |
|---|---|---:|---:|---:|---:|
| 2023-05-05 to 2023-06-21 | May-Jun | 18.77 | 7.69 | 24.17 | 23.99 |
| 2024-09-16 to 2024-11-24 | Sep-Nov | 44.62 | 23.91 | 52.33 | 48.51 |
| 2025-05-29 to 2025-06-08 | May-Jun | 18.97 | 15.13 | 20.48 | 17.88 |

These predicted values are physically plausible and not absurd. However, plausibility alone is not enough for manuscript replacement.

## Technical assessment

Arguments in favor of imputation:

- `SW_IN_F` is available during all three gaps.
- The PAR vs `SW_IN_F` relation is strong overall and physically interpretable.
- Predicted values for the gap periods look reasonable relative to neighboring days.

Arguments against imputation:

- The raw observed shortwave variable `SW_IN` is itself absent during the target gaps, so imputation would rely on an already filled product (`SW_IN_F`) rather than an independent observed radiation series.
- The `SW_IN_F -> PAR` relation is not equally stable across years.
- The May-Jun relationship, relevant to two of the three target periods, drops to `R² = 0.72` pooled and is less robust than the full-period fit.
- Because the purpose here is a manuscript figure, imputed PAR could be read as real observation unless explicitly flagged.

## Conclusion

`SW_IN_F` is the only candidate that is even potentially suitable for PAR imputation. However, the evidence is not strong enough to justify replacing all three target PAR gaps in the manuscript figure with synthetic values. The conservative and technically strongest option is to leave those periods blank in the plot.
