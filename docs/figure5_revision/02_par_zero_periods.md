# PAR zero periods

Date: 2026-06-17

## Three conspicuous periods affecting the manuscript figure

These are the three long periods that appear as flat PAR sections at zero in the unmasked `PPFD_sum` series and are visually conspicuous at manuscript scale:

| Period | Start | End | Duration |
|---|---|---|---:|
| 1 | 2023-05-05 | 2023-06-21 | 48 days |
| 2 | 2024-09-16 | 2024-11-24 | 70 days |
| 3 | 2025-05-29 | 2025-06-08 | 11 days |

## Additional short zero runs present in the daily series

These were also detected in `PPFD_sum`, but they are short and are not the three conspicuous blocks mentioned by Jorge:

| Start | End | Duration |
|---|---|---:|
| 2022-07-05 | 2022-07-06 | 2 days |
| 2024-06-23 | 2024-06-23 | 1 day |
| 2025-05-10 | 2025-05-12 | 3 days |

## Evidence that the three conspicuous periods are not physically real PAR = 0

### Period 1: 2023-05-05 to 2023-06-21

- `PPFD_sum` is exactly `0` for 48 consecutive days.
- `PPFD` has `0/48` non-missing values.
- `SW_IN` has `0/48` non-missing values.
- `NETRAD` has `0/48` non-missing values.
- Filled radiative proxies remain positive through the whole interval:
  - mean `SW_IN_F` = `146.72`
  - mean `NETRAD_F` = `59.30`
  - mean `LW_IN_F` = `316.21`
  - mean `LW_OUT_F` = `387.09`
- Carbon fluxes remain active:
  - mean `GPP_NT` = `1.72`
  - mean `NEE_F2` = `0.56`

Interpretation: this is consistent with a PAR data outage or a missing-value coding artifact, not with true daily PAR = 0.

### Period 2: 2024-09-16 to 2024-11-24

- `PPFD_sum` is exactly `0` for 70 consecutive days.
- `PPFD`, `SW_IN`, and `NETRAD` all have `0` valid daily values in the interval.
- Filled radiative proxies remain positive:
  - mean `SW_IN_F` = `307.11`
  - mean `NETRAD_F` = `163.28`
  - mean `LW_IN_F` = `315.30`
  - mean `LW_OUT_F` = `403.78`
- Carbon fluxes remain active:
  - mean `GPP_NT` = `3.53`
  - mean `NEE_F2` = `-1.80`

Interpretation: a 70-day spring period with true PAR = 0 is physically impossible at Fray Jorge. This is a missing-data artifact.

### Period 3: 2025-05-29 to 2025-06-08

- `PPFD_sum` is exactly `0` for 11 consecutive days.
- `PPFD`, `SW_IN`, and `NETRAD` all have `0` valid daily values in the interval.
- Filled radiative proxies remain positive:
  - mean `SW_IN_F` = `148.12`
  - mean `NETRAD_F` = `54.92`
  - mean `LW_IN_F` = `303.77`
  - mean `LW_OUT_F` = `378.80`
- Carbon fluxes remain active:
  - mean `GPP_NT` = `1.45`
  - mean `NEE_F2` = `0.05`

Interpretation: this is also a missing-data artifact, not a real zero-radiation event.

## Conclusion

The three target intervals are best interpreted as missing PAR encoded as zero, or an equivalent processing artifact. They should not be shown as real PAR = 0 observations in a manuscript figure.
