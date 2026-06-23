# PAR gap decision

Date: 2026-06-17

## Decision

Primary manuscript recommendation:

- use the Figure 5 version with PAR gaps left blank

Secondary comparison product:

- retain a version where the three PAR gaps are reconstructed from `SW_IN_F` using a simple origin-constrained factor

## Why the blank-gap version is recommended

- the three zero plateaus are artifacts, not real observations
- leaving them blank removes the false signal without fabricating replacement values
- this is the most conservative and least arguable manuscript choice

## Why a reconstructed version was still generated

- `SW_IN_F` showed a strong and physically interpretable relationship with observed PAR
- the origin-constrained factor model was simple and transparent
- the reconstructed trace is useful as a visual comparison for discussion with coauthors

## Reconstruction used in the comparison version

- proxy variable: `SW_IN_F`
- formula: `PAR_reconstructed = 0.141391 * SW_IN_F`

## Final recommendation

Use:

- `Figure5_PAR_gaps_blank.png` in the manuscript

Keep:

- `Figure5_PAR_gaps_reconstructed.png` as an internal comparison or coauthor discussion figure
