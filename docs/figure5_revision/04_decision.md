# Decision

Date: 2026-06-17

## Decision

Do not impute the three conspicuous PAR zero periods in Figure 5. Replace the plotted `PPFD_sum == 0` values with missing values in the plotting layer so the figure shows gaps rather than false PAR = 0 plateaus.

## Explicit decision criterion

For this revision, PAR imputation would be accepted only if all of the following were true:

1. A proxy existed with direct coverage in the target gaps.
2. The proxy showed a high and physically interpretable relation with observed PAR.
3. The relation was temporally stable across the relevant seasons and years.
4. The imputation would not depend mainly on another already-filled meteorological series with uncertain provenance.
5. The predicted values remained physically reasonable and scientifically defensible for manuscript use.

## Why imputation was rejected

- `SW_IN_F` is the only viable candidate with full gap coverage.
- Its overall fit to `PPFD_sum` is strong (`R² = 0.8798`), but that alone is not enough.
- Two of the three target gaps occur in May-Jun, where the pooled relation drops to `R² = 0.7223`.
- The slope also shifts noticeably across ecohydrological years, especially between 2022-2023 and later years.
- The proxy required for imputation is itself a filled variable (`SW_IN_F`), not an independent observed shortwave series available during the gaps.

## Why leaving the gaps blank is stronger scientifically

- The zero plateaus are demonstrably artifacts, not real PAR observations.
- Converting those artifacts to missing values prevents visual misinterpretation without fabricating replacement data.
- The correction is confined to the plotting layer and does not alter `NEE`, `GPP`, `RECO`, or any numerical analysis outputs.

## Recommendation to respond to Jorge

The technically preferred response is:

- remove those false PAR = 0 segments from the plotted series by treating them as missing values;
- do not impute PAR in the manuscript figure because the only usable proxy is a filled shortwave product whose PAR conversion is not stable enough across the relevant seasons to support a fully defensible scientific replacement.
