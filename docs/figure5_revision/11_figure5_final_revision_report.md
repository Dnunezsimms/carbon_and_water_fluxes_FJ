# Figure 5 final revision report

Date: 2026-06-17

## Confirmed script

The repository script actually associated with Figure 5 is:

- `scripts/figures/Figure_5.py`

## Variables actually involved in the top panel

Original script:

- PAR variable: `PPFD_sum`
- temperature variable: none

Revised final script:

- PAR variable: `PPFD_sum`
- temperature variable: `TA_F`

## Inconsistency found in temperature handling

The inconsistency was not just a label issue:

- the manuscript description refers to PAR plus daily air temperature (`Ta`) in panel a;
- the original repository script currently plots only PAR;
- if temperature is to be shown continuously, `TA_F` is the correct plotting series because it is complete over the target PAR gap periods, while `TA` is not.

## PAR-affected periods

- `2023-05-05` to `2023-06-21` (`48` days)
- `2024-09-16` to `2024-11-24` (`70` days)
- `2025-05-29` to `2025-06-08` (`11` days)

These were confirmed as missing-data artifacts encoded as zero, not physically real PAR = 0 periods.

## Proxy evaluated for PAR gap reconstruction

Best proxy:

- `SW_IN_F`

Simple reconstruction used in the comparison figure:

- `PAR_reconstructed = 0.141391 * SW_IN_F`

Main performance metrics for `SW_IN_F`:

- `n = 988`
- linear model `R² = 0.8798`, `RMSE = 5.384`
- origin-constrained model `R² = 0.8793`, `RMSE = 5.395`

## Final decision

- Main manuscript figure: leave the three PAR gaps blank
- Comparison-only figure: show the three gaps reconstructed from `SW_IN_F`

## New final script

- `C:\projects\carbon_and_water_fluxes_FJ_public\scripts\figures\Figure_5_revision_final.py`

This script:

- loads the original daily dataset without modifying it
- rebuilds the top panel using `TA_F` and `PPFD_sum`
- produces a blank-gap PAR version
- produces a comparison version with reconstructed PAR only in the three target gaps
- preserves all other panels and fluxes unchanged

## Figures generated

- Blank-gap version:
  - `C:\projects\carbon_and_water_fluxes_FJ_public\results\figures\Figure5_PAR_gaps_blank.png`
- Reconstructed comparison version:
  - `C:\projects\carbon_and_water_fluxes_FJ_public\results\figures\Figure5_PAR_gaps_reconstructed.png`

## Recommended manuscript figure

Recommended for manuscript submission:

- `Figure5_PAR_gaps_blank.png`

Reason:

- it corrects the false PAR = 0 artifacts
- it restores a top panel with explicit temperature
- it is the most conservative and scientifically defensible version
