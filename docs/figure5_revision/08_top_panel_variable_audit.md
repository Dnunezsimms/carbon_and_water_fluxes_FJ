# Top panel variable audit

Date: 2026-06-17

## What the original script actually uses

From `scripts/figures/Figure_5.py`:

- PAR source variable: `PPFD_sum`
- Temperature source variable: none

In other words, the current repository script does not plot `TA`, `TA_F`, or any other temperature series in panel a.

## How the original top panel is currently labeled

Current original script:

- panel comment: `# a) PAR`
- plotted line: `ax0.plot(df.index, PAR, ...)`
- right y-axis label: `PAR (mol m^-2 s^-1)`
- no left y-axis temperature label
- no temperature legend entry

## Inconsistency identified

There are two distinct inconsistencies:

1. Manuscript-to-script inconsistency

- The manuscript text describes panel a as:
  - daily PAR and mean daily air temperature (`Ta`)
- The actual repository script/export shows only PAR.

2. Variable-name inconsistency for temperature

- The daily dataset contains both `TA` and `TA_F`.
- For the three PAR gap periods, `TA` is incomplete, but `TA_F` is complete.
- If the panel is meant to show a continuous temperature context together with PAR, the technically consistent choice is `TA_F`, not `TA`.

## Temperature audit: `TA` versus `TA_F`

Across the full daily series:

- overlap `n = 1073`
- correlation between `TA` and `TA_F` = `0.9939`
- mean difference (`TA_F - TA`) = `0.00003 °C`
- mean absolute difference = `0.0389 °C`
- max absolute difference = `3.8745 °C`

Interpretation:

- `TA_F` closely tracks `TA` where both exist.
- `TA_F` is the more complete series and is appropriate for plotting the top-panel temperature line when continuity is required.

## Final correction adopted for the revision script

In `scripts/figures/Figure_5_revision_final.py` the top panel is made explicit and internally consistent:

- temperature variable used in code: `TA_F`
- temperature legend label: `TA_F`
- temperature axis label: `Air temperature (TA_F, °C)`
- PAR variable used in code: `PPFD_sum`
- PAR axis label: `PAR (mol m^-2 day^-1)`

## Why this is the cleanest manuscript-facing option

- It avoids ambiguity about whether the plotted temperature series is raw `TA` or filled `TA_F`.
- It uses the complete daily temperature series during the same periods where PAR has data gaps.
- It makes the figure code, the plotted variable, and the visible labels fully consistent.
