# Public Repo Note

This file was copied from the full research workspace and retained here as the manuscript-facing workflow narrative for the curated public repository.

# Scientific Workflow

## Purpose

This document reconstructs the most plausible end-to-end workflow currently represented in the repository for the Fray Jorge carbon and water flux manuscript.

It is written for:

- thesis committee members,
- coauthors,
- external collaborators,
- journal reviewers,
- reproducibility auditors.

This is a reconstruction from existing files. Where the workflow is ambiguous, that ambiguity is stated explicitly.

## High-Level Diagram

```text
external EC + biomet + ERA5 + rainfall + RS exports + shapefiles
    ->
raw / intermediate flux processing
    ->
daily flux datasets
    ->
TEA partitioning and merged ecohydrological dataset
    ->
temporal figures, annual metrics, correlations, CART
    ->
remote sensing modelling dataset
    ->
SVR models
    ->
pixel-level landscape predictions
    ->
map figures and manuscript
```

## Branch A: Flux Processing and Daily Datasets

### A1. Eddy covariance / meteorological preprocessing

Candidate scripts:

- `scripts/EC_postprocessing_FJ.py`
- `scripts/EC_postprocessing_FrayJorge_v3.py`

Role inferred:

- merge tower, biomet, and ERA5-support data
- apply post-processing logic after EddyPro
- create Level 3 style flux tables

Current reproducibility caveat:

- these scripts still contain hardcoded absolute local paths
- they are important for provenance, but they are not yet portable

Likely outputs or descendants in the repo:

- `data/LEVEL3_FJ_2022_2025_ss.csv`
- later daily derivatives such as `data/LEVEL3_FJ_2022_2025_ss_daily.csv`

### A2. Daily aggregation

Candidate script:

- `scripts/FJ_data_to_daily.py`

Role inferred:

- convert postprocessed flux data to daily time steps
- merge or append precipitation-related information

Current caveat:

- contains absolute local paths
- output naming in the script does not fully match the final data naming now present in the repo

### A3. Daily master datasets currently used downstream

Most important observed daily files:

- `data/LEVEL3_FJ_2022_2025_ss_daily.csv`
- `data/LEVEL3_FJ_2022_2025_ss_v4_daily.csv`
- `data/LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv`
- `data/LEVEL3_FJ_merged_ET_T_WUE.csv`

Practical note:

The revised manuscript workflow appears to depend mainly on `ss_daily`, `ss_v4_daily`, and the merged `ET/T/WUE` table.

## Branch B: TEA Water Partitioning

### B1. Prepare a TEA-ready high-frequency dataset

Script:

- `scripts/make_TEA_ready_dataset.py`

Observed input:

- `data/LEVEL3_FJ_2022_2025_ss_v4_daily.csv` is the configured default source in the current script, despite the script header describing a high-frequency product

Observed output:

- `data/processed/LEVEL3_FJ_2022_2025_TEA_ready_hf.csv`

Important caveat:

- the script is portable, but the default input naming suggests a possible mismatch between intended temporal resolution and actual source file naming. This should be verified.

### B2. Run TEA partitioning

Script:

- `scripts/run_TEA_partitioning.py`

Role:

- read TEA-ready input
- call `TEA.simplePartition()`
- export `TEA_T`, `TEA_E`, and `TEA_WUE`

Observed caveat:

- TEA is an external dependency not documented in the repo
- the current script writes to `outputs/`, while archived TEA outputs also exist under `data/`

Observed TEA-related files:

- `data/LEVEL3_FJ_2022_2025_no_gaps_for_TEA.csv`
- `data/LEVEL3_FJ_2022_2025_no_gaps_for_TEA_TEA_outputs.csv`
- `data/LEVEL3_FJ_2022_2025_no_gaps_for_TEA_TEA_outputs_daily_with_T_E.csv`

### B3. Build daily T/E/WUE and merge back to the main daily dataset

Scripts:

- `scripts/make_T_E_WUE_dataset.py`
- `scripts/merge_tea_with_full_data.py`

Observed outputs:

- `data/raw/LEVEL3_FJ_2022_2025_daily_T_E_WUE.csv`
- `data/LEVEL3_FJ_merged_ET_T_WUE.csv`

Important caveat:

- `merge_tea_with_full_data.py` still uses a hardcoded absolute repo path

## Branch C: Temporal Figures and Ecohydrological Diagnostics

### Figure 2: Annual precipitation

Script:

- `scripts/Figure_2.py`

Main input:

- `data/processed/rainfall_data_1984-2025_updated.xlsx`

### Figure 3: VPD, ET, SWC, precipitation

Script:

- `scripts/Figure_3.py`

Main input:

- `data/LEVEL3_FJ_2022_2025_ss_daily.csv`

### Figure 4: ET partitioning into T and E

Script:

- `scripts/Figure_4.py`

Main input:

- `data/LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv`

### Figure 5: PAR, carbon fluxes, REW

Script:

- `scripts/Figure_5.py`

Main input:

- `data/LEVEL3_FJ_2022_2025_ss_v4_daily.csv`

### Figure 6: Annual accumulations

Script:

- `scripts/Figure_6.py`

Main input:

- `data/LEVEL3_FJ_2022_2025_ss_v4_daily.csv`

### Figure 7: Correlation matrix

Scripts:

- `scripts/Figure_7.py`
- `scripts/Figure_7_v2.py`
- `scripts/Figure_7_v3.py`

Main input:

- `data/LEVEL3_FJ_merged_ET_T_WUE.csv`

Interpretation:

- there were multiple iterations of the same analysis
- one canonical version should be declared for publication

### Supplementary annual metrics and checks

Observed check scripts:

- `tests/ecohydrological_metrics.py`
- `tests/accumulated_NEE.py`
- `tests/accumulated_et.py`
- `tests/precip_metrics.py`
- `tests/swc_metrics.py`
- `tests/vpd_metrics.py`

These currently function more like reproducibility checks than automated tests.

## Branch D: CART Threshold Analysis

Main R workflow:

- `scripts/RF_CART.R`

Observed input:

- `data/LEVEL3_FJ_merged_ET_T_WUE.csv`

Observed related figure assets:

- `figures/NEE_CART.png`
- `figures/ET_CART.png`
- `figures/E_CART.png`
- `figures/T_CART.png`
- `figures/CART_explanatory_NEE.png`

Important caveats:

- the R script is interactive
- package installation occurs inside the script
- the final manuscript export path for all CART panels is not fully stabilized

## Branch E: Remote Sensing Modelling for Landscape NEE

### E1. Build the modelling dataset

Script:

- `scripts/build_model_dataset.py`

Observed inputs:

- `data/processed/nee_clean.csv`
- `data/raw/NEE_predictors_season_1_20220704_20230630.csv`
- `data/raw/NEE_predictors_season_2_20230701_20240630.csv`
- `data/raw/NEE_predictors_season_3_20240701_20250630.csv`

Observed output:

- `data/processed/model_dataset_final.csv`

### E2. Train/select models

Main candidate scripts:

- `scripts/modelo_predictivo.py`
- `scripts/model_nee_v2.py`
- `scripts/metrics_model_results.py`

Observed saved models used by the revised manuscript branch:

- `models/best_SVR_NDVI_RAD_topo.joblib`
- `models/best_SVR_NDVI_Pol_moisture_RAD_topo.joblib`

Observed metrics tables:

- `results_intermediate_nonGPR.csv`
- `results_with_GPR.csv`
- `linear_loso_fold_metrics.csv`
- `linear_per_season_coeffs.csv`

Important caveat:

- a separate legacy modelling branch also exists under `NEE_Model/` with different predictor naming and output logic

### E3. Predict annual NEE at pixel level

Script:

- `scripts/modelo_predictivo.py`

Observed large inputs:

- `data/raw/NEE_predictors_pixels_season_1_20220704_20230630.csv`
- `data/raw/NEE_predictors_pixels_season_2_20230701_20240630.csv`
- `data/raw/NEE_predictors_pixels_season_3_20240701_20250630.csv`

Observed outputs:

- `outputs/nee_opt_season_1.csv`
- `outputs/nee_opt_season_2.csv`
- `outputs/nee_opt_season_3.csv`
- `outputs/nee_eco_season_1.csv`
- `outputs/nee_eco_season_2.csv`
- `outputs/nee_eco_season_3.csv`

Strong traceability note:

The means of `outputs/nee_opt_season_*.csv` match the revised manuscript values exactly:

- Year 1 mean: `-193.2`
- Year 2 mean: `-208.5`
- Year 3 mean: `-162.8`
- overall mean across years: `-188.2`

### E4. Map and summarize spatial outputs

Scripts:

- `scripts/plot_nee.py`
- `scripts/Figure_10.py`
- `scripts/diagnostico_cv_plots_resumen.py` (alternate raster branch)

Observed outputs:

- `outputs/NEE_COMPARISON_4MAPS.png`
- `outputs/NEE_FINAL_PAPER.png`
- `results/raster_pipeline/*.tif`
- `results/raster_pipeline/pixel_stats_cross_seasons_accum_stats.csv`

Important caveat:

- the exact split between manuscript Figure 9 and Figure 10 is not yet documented as a single canonical export chain

## Branch F: Legacy / Alternate NEE Modelling Workflow

Directory:

- `NEE_Model/`

This branch contains:

- alternative model training scripts,
- alternate predictor engineering,
- older outputs,
- chunked temp files,
- map-generation scripts,
- legacy metrics tables.

Examples:

- `NEE_Model/Scripts/model_30m_2_matorral_suculentas.py`
- `NEE_Model/Scripts/prediccion_nee_matorral_suculentas_fj.py`
- `NEE_Model/Figuras/model_30m_2/tabla_resumen_metricas.csv`

Important interpretation:

This branch should be preserved for transparency, but it should not remain ambiguous whether it belongs to the revised manuscript's canonical workflow.

## External Dependencies Outside the Repo

The workflow depends on tools or data sources not packaged inside the repo:

- EddyPro for flux post-processing
- TEA for ET partitioning
- ERA5 for some meteorological gap-filling support
- Google Earth Engine / Earth Engine exports for remote-sensing predictors

These dependencies should be documented explicitly in any public release.

## Recommended Canonical Workflow for This Repo

Based on current evidence, the cleanest manuscript-facing workflow is:

```text
1. data/LEVEL3_FJ_2022_2025_ss*.csv
2. scripts/make_TEA_ready_dataset.py
3. scripts/run_TEA_partitioning.py
4. scripts/make_T_E_WUE_dataset.py
5. scripts/merge_tea_with_full_data.py
6. scripts/Figure_2.py ... scripts/Figure_7.py
7. scripts/build_model_dataset.py
8. scripts/modelo_predictivo.py
9. scripts/plot_nee.py
10. manuscript
```

The `NEE_Model/` and `results/raster_pipeline/` branches should remain documented, but should be marked as:

- `legacy`,
- `supporting`,
- or `alternate`,

unless they are explicitly re-adopted as the canonical route for the revised manuscript.

