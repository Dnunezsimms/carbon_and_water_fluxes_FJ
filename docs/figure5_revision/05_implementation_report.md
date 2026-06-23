# Implementation report

Date: 2026-06-17

## What was detected

Three conspicuous artifact periods in `PPFD_sum` were confirmed:

- `2023-05-05` to `2023-06-21` (`48` days)
- `2024-09-16` to `2024-11-24` (`70` days)
- `2025-05-29` to `2025-06-08` (`11` days)

These intervals are missing-data artifacts encoded as zero, not physically real daily PAR = 0.

## Was PAR imputed?

No.

The plotting layer was cleaned so that `PPFD_sum <= 0` is shown as missing, and the three conspicuous artifact periods are explicitly masked in the revision script.

## Criterion used

Imputation was rejected because:

- the only usable candidate with full gap coverage was `SW_IN_F`;
- although its overall linear fit was strong (`R² = 0.8798`), temporal stability was weaker in the seasons that matter for the gaps;
- two of the three target gaps fall in May-Jun, where the pooled `SW_IN_F -> PAR` relation dropped to `R² = 0.7223`;
- the proxy itself is already a filled meteorological series, so replacing PAR would mean substituting one inferred quantity with another inferred quantity in a manuscript figure.

## Files created or modified

Created:

- `scripts/analysis/figure5_par_revision_analysis.py`
- `scripts/figures/Figure_5_PAR_revision.py`
- `docs/figure5_revision/01_figure5_pipeline_identification.md`
- `docs/figure5_revision/02_par_zero_periods.md`
- `docs/figure5_revision/03_par_imputation_feasibility.md`
- `docs/figure5_revision/04_decision.md`
- `docs/figure5_revision/05_implementation_report.md`

Generated outputs:

- `results/figures/Figure5_PAR_cleaned.png`
- `results/figures/Figure5_PAR_original_vs_cleaned.png`

Not modified:

- `data/processed/LEVEL3_FJ_2022_2025_ss_v4_daily.csv`
- `scripts/figures/Figure_5.py`
- any NEE or other flux datasets

## Scientific scope of the change

- No scientific flux result was altered.
- No `NEE`, `GPP`, `RECO`, `ET`, `T`, or `E` values were changed.
- The correction only affects how PAR artifacts are displayed in the revised Figure 5 export.

## Risks and limitations

- The repository Figure 5 script and current export already show PAR gaps rather than zero plateaus, so the issue likely concerns a manuscript-side or earlier export version.
- The manuscript description says panel a includes Ta and PAR, while the current repository script/export only shows PAR. That discrepancy should be checked before final resubmission.
- If the coauthors later decide that a visually continuous PAR series is essential, the least risky exploratory route would be a clearly flagged figure-only imputation from `SW_IN_F`, but that was not adopted here.

## Suggested text for Jorge

Revisé los tres tramos donde PAR cae a cero y confirmé que no corresponden a valores físicos reales, sino a faltas de datos codificadas como 0. Evalué la posibilidad de reconstruir PAR con proxies radiativas y la única variable con cobertura completa fue `SW_IN_F`, pero aunque el ajuste global fue bueno, la relación no fue lo suficientemente estable en las ventanas estacionales críticas como para justificar una imputación defendible en la figura del manuscrito. Por eso implementé la opción más conservadora: esos tramos quedaron como missing y ahora se muestran como huecos en la figura, sin alterar NEE ni otros flujos.
