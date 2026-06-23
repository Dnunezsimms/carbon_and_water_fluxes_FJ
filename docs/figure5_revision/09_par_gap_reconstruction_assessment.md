# PAR gap reconstruction assessment

Date: 2026-06-17

## Target PAR gaps

The three conspicuous PAR gaps reviewed for this task are:

| Gap | Start | End | Duration |
|---|---|---|---:|
| 1 | 2023-05-05 | 2023-06-21 | 48 days |
| 2 | 2024-09-16 | 2024-11-24 | 70 days |
| 3 | 2025-05-29 | 2025-06-08 | 11 days |

These correspond to `PPFD_sum = 0` plateaus that are not physically real and are best interpreted as missing PAR encoded as zero.

## Candidate proxy variables

The following radiative candidates were evaluated against observed valid PAR (`PPFD_sum > 0`):

- `SW_IN_F`
- `SW_IN`
- `NETRAD_F`
- `NETRAD`

## Simple model forms tested

For each candidate proxy:

- simple linear regression: `PAR = intercept + slope * proxy`
- origin-constrained factor model: `PAR = factor * proxy`

The origin-constrained version was considered especially relevant for `SW_IN`-type proxies because a zero-radiation proxy should correspond approximately to zero PAR.

## Summary metrics

| Proxy | n | Linear slope | Intercept | R² | RMSE | Origin factor | R² (origin) | RMSE (origin) | Assessment |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `SW_IN_F` | 988 | 0.1384 | 0.9280 | 0.8798 | 5.384 | 0.1414 | 0.8793 | 5.395 | Best simple reconstruction candidate |
| `SW_IN` | 962 | 0.0815 | -2.0585 | 0.7724 | 7.335 | 0.0778 | 0.7706 | 7.363 | Moderate, but unavailable in the target gaps |
| `NETRAD_F` | 988 | 0.2171 | 10.1575 | 0.8269 | 6.462 | 0.2799 | 0.7401 | 7.918 | Usable but weaker than `SW_IN_F` |
| `NETRAD` | 963 | 0.1447 | 17.9341 | 0.4838 | 11.076 | 0.2438 | 0.1956 | 13.827 | Too weak |

## Coverage in the target gaps

Coverage matters as much as fit:

- `SW_IN` and `NETRAD` do not cover the target long gaps, so they cannot be used directly there.
- `SW_IN_F` and `NETRAD_F` are available throughout the three target gaps.

This makes `SW_IN_F` the only strong and fully usable reconstruction proxy.

## Chosen simple reconstruction for comparison

For the comparison-only reconstructed figure, the chosen reconstruction is:

- `PAR_reconstructed = 0.141391 * SW_IN_F`

Reason:

- this is the origin-constrained factor form;
- it is physically interpretable;
- it is almost indistinguishable in fit from the unconstrained linear model;
- it avoids introducing a non-zero intercept into a manuscript-facing gap reconstruction.

## Plausibility in the three gaps

Using `SW_IN_F` with the factor above, the reconstructed PAR values are physically plausible and remain within the same broad range as neighboring observed PAR.

The reconstruction therefore works as a simple visual continuity check. However, it still depends on a filled shortwave series (`SW_IN_F`) rather than on independently observed shortwave radiation during the gaps.

## Technical interpretation

Strengths:

- simple
- transparent
- physically interpretable
- based on the best available radiative proxy
- complete coverage of all three target gaps

Limitations:

- depends on `SW_IN_F`, which is itself a filled series
- should be treated as a derived plotting layer only
- should not replace the original PAR series in the dataset
- should not be mistaken for observed PAR

## Recommendation

- Generate and keep the reconstructed figure as a comparison product.
- Use the blank-gap figure as the primary manuscript-facing version unless the coauthors explicitly prefer a continuous PAR trace and are willing to state that those segments were reconstructed from `SW_IN_F`.
