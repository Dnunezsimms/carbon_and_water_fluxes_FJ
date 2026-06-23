# Figure 5 pipeline confirmation

Date: 2026-06-17

## Confirmed script

Yes. The operative repository script associated with Figure 5 is:

- `C:\projects\carbon_and_water_fluxes_FJ_public\scripts\figures\Figure_5.py`

This is supported by:

- direct code inspection of `scripts/figures/Figure_5.py`
- `docs/workflow.md`
- `docs/reproducibility_audit/03_traceability_matrix.md`

## Main input dataset

- `C:\projects\carbon_and_water_fluxes_FJ_public\data\processed\LEVEL3_FJ_2022_2025_ss_v4_daily.csv`

## Existing repository figure output

- Existing exported figure in the repository:
  - `C:\projects\carbon_and_water_fluxes_FJ_public\results\figures\figure_5.png`

Important note:

- `Figure_5.py` currently displays the figure with `plt.show()` and does not save an output file.
- Therefore, `results/figures/figure_5.png` is consistent with this pipeline, but it was exported outside the current script body or from an earlier saved version.

## Variables used by the original script in the top panel

Original `Figure_5.py` top panel uses:

- PAR variable: `PPFD_sum`
- Temperature variable: none

The current original script does not draw air temperature in panel a.

## Variables used in the revised pipeline

For the present revision, the top panel was rebuilt explicitly using:

- PAR: `PPFD_sum`
- Temperature: `TA_F`

The revision script created for this task is:

- `C:\projects\carbon_and_water_fluxes_FJ_public\scripts\figures\Figure_5_revision_final.py`

## Revised outputs generated

- Blank-gap version:
  - `C:\projects\carbon_and_water_fluxes_FJ_public\results\figures\Figure5_PAR_gaps_blank.png`
- Reconstructed-gap comparison version:
  - `C:\projects\carbon_and_water_fluxes_FJ_public\results\figures\Figure5_PAR_gaps_reconstructed.png`
