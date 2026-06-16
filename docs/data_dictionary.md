# Public Repo Note

This file describes the main datasets observed in the original working archive. In this curated public subset, only a selected shareable subset of those datasets is actually distributed.

# Data Dictionary

## Scope

This dictionary documents the main datasets observed in the repository that are relevant to the thesis/article workflow. It does not invent missing metadata. Where uncertainty remains, the field is marked `TO VERIFY`.

## Dataset Inventory

| Dataset | Path | Processing level | Role in workflow | Notes |
|---|---|---|---|---|
| Level 3 main flux table | `data/LEVEL3_FJ_2022_2025_ss.csv` | Processed | Main postprocessed EC/meteorological dataset | Large core table; exact temporal resolution `TO VERIFY` |
| Daily Level 3 table | `data/LEVEL3_FJ_2022_2025_ss_daily.csv` | Processed daily | Main daily ecohydrological analyses | Used by Figures 3 and several metric scripts |
| Daily Level 3 table v4 | `data/LEVEL3_FJ_2022_2025_ss_v4_daily.csv` | Processed daily | Used by Figures 5-6 and TEA preparation script | Version lineage should be clarified |
| Daily cleaned T/E | `data/LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv` | Derived daily | Used for Figure 4 | Contains daily `T` and `E` |
| Merged ET/T/WUE table | `data/LEVEL3_FJ_merged_ET_T_WUE.csv` | Derived daily | Correlations, CART, integrated diagnostics | Merges daily master data with T/E/WUE |
| TEA source table | `data/LEVEL3_FJ_2022_2025_no_gaps_for_TEA.csv` | Derived | Input/archive for TEA branch | Exact generation step `TO VERIFY` |
| TEA outputs | `data/LEVEL3_FJ_2022_2025_no_gaps_for_TEA_TEA_outputs.csv` | Derived | Water partitioning outputs | Contains `TEA_T`, `TEA_E`, `TEA_WUE` expected |
| TEA outputs merged daily | `data/LEVEL3_FJ_2022_2025_no_gaps_for_TEA_TEA_outputs_daily_with_T_E.csv` | Derived daily | Water partitioning summary | Exact creation script `TO VERIFY` |
| TEA-ready HF table | `data/processed/LEVEL3_FJ_2022_2025_TEA_ready_hf.csv` | Derived | Input to `run_TEA_partitioning.py` | Script name suggests high frequency |
| NEE target table | `data/processed/nee_clean.csv` | Derived daily | Target variable for remote-sensing model | Two columns observed: `fecha`, `NEE_F2` |
| Modelling dataset | `data/processed/model_dataset_final.csv` | Derived modelling-ready | Final tower + predictor table for ML | Used by current manuscript model scripts |
| Historical rainfall workbook | `data/processed/rainfall_data_1984-2025_updated.xlsx` | Curated external + derived | Figure 2 precipitation history | Used by `scripts/Figure_2.py` |
| Historical rainfall raw workbook | `data/raw/rainfall_data_1984-2024.xlsx` | Raw/curated | Pre-merge rainfall history | Likely predecessor of updated workbook |
| Seasonal predictors (tower scale) | `data/raw/NEE_predictors_season_*.csv` | Raw/curated remote sensing exports | Inputs for building the modelling dataset | Small seasonal predictor tables |
| Seasonal predictors (pixel scale) | `data/raw/NEE_predictors_pixels_season_*.csv` | Raw/curated remote sensing exports | Inputs for landscape prediction | Very large files; not GitHub-safe in normal Git |
| Daily T/E/WUE export | `data/raw/LEVEL3_FJ_2022_2025_daily_T_E_WUE.csv` | Derived daily | Intermediate between TEA and merged daily dataset | Created by `make_T_E_WUE_dataset.py` |
| Complementary spatial layers | `data/complementary/*.shp`, `.geojson`, `.dbf`, etc. | Supporting spatial inputs | Site map, mask, tower location | Includes matorral polygon, park polygon, tower point |
| Full output table | `data/frayjorge_fulloutput_2022_2025.csv` | `TO VERIFY` | Large derived table | File present but canonical use not documented |
| Biomet table | `data/biomet_FJ_20220704_20250918.csv` | `TO VERIFY` | Ancillary meteorological support | Present but not directly documented in scripts reviewed |

## Key Variables

### Flux and climate variables from daily Level 3 tables

| Variable | Observed in | Meaning inferred | Units | Notes |
|---|---|---|---|---|
| `TIMESTAMP` | daily flux tables | Daily timestamp | date | Core temporal key |
| `NEE_F2` | daily flux tables, `nee_clean.csv` | Net ecosystem exchange | `g C m^-2 day^-1` inferred from manuscript | Negative values indicate sink |
| `GPP_NT` | daily flux tables | Gross primary productivity | `g C m^-2 day^-1` inferred | Manuscript plots GPP as positive in some figures, negative in Figure 6 convention |
| `RECO_NT` | daily flux tables | Ecosystem respiration | `g C m^-2 day^-1` inferred | |
| `ET_F` | daily flux tables | Evapotranspiration | `mm day^-1` inferred | |
| `P_RAIN` | daily flux tables | Precipitation | `mm day^-1` inferred | Used also for effective precipitation windows |
| `PPFD_sum` | daily flux tables | Daily PAR / PPFD sum | `TO VERIFY`; used as PAR | Scripts interpret as daily PAR |
| `PPFD` | daily flux tables | Instantaneous PPFD | `TO VERIFY` | Used as PAR-related field in checks |
| `VPD_F` | daily flux tables | Vapor pressure deficit | raw likely `Pa`; scripts convert to `kPa` by dividing by 1000 | Important for manuscript Figure 3 and CART |
| `TA_F` | daily flux tables | Air temperature | `deg C` inferred | |
| `LW_IN_F` | daily flux tables | Incoming longwave radiation | `TO VERIFY` | Used in Figure 7 and CART |
| `SWC_F_1_1_1` | daily flux tables | Soil water content sensor 1 | `m^3 m^-3` inferred | |
| `SWC_F_2_1_1` | daily flux tables | Soil water content sensor 2 | `m^3 m^-3` inferred | |
| `SWC_F_3_1_1` | daily flux tables | Soil water content sensor 3 | `m^3 m^-3` inferred | |
| `TS_F_1_1_1` etc. | daily flux tables | Soil temperature sensors | `deg C` inferred | |
| `T` | `data/LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv`, merged table | Transpiration | `mm day^-1` inferred | TEA-derived |
| `E` | same | Soil evaporation | `mm day^-1` inferred | TEA-derived |
| `WUE` | same | Water use efficiency or TEA-derived ratio | `TO VERIFY` exact formula per file | In some scripts it is recomputed from `T/(T+E)` when missing |

### Remote sensing predictor variables

| Variable | Observed in | Meaning inferred | Units | Notes |
|---|---|---|---|---|
| `NDVI` | modelling dataset, predictor CSVs | Normalized Difference Vegetation Index | unitless | Used in selected SVR models |
| `EVI` | modelling dataset, predictor CSVs | Enhanced Vegetation Index | unitless | |
| `NDWI` | modelling dataset, predictor CSVs | Normalized Difference Water Index | unitless | |
| `LST` | modelling dataset, predictor CSVs | Land surface temperature | `TO VERIFY` | |
| `Pol_moisture` | modelling dataset, predictor CSVs | Radar-derived moisture proxy | `TO VERIFY` | Included in ecohydrological SVR model |
| `RAD_topo` | modelling dataset, predictor CSVs | Terrain-adjusted radiation | `TO VERIFY` | Included in selected SVR models |
| `SWC_norm` | modelling dataset, predictor CSVs | Normalized soil-moisture proxy | `TO VERIFY` | Prominent in legacy workflow |
| `SAVI` | modelling dataset | Soil Adjusted Vegetation Index | unitless | Present in modelling dataset but not selected in revised manuscript's final model |
| `VV_VH_ratio` | modelling dataset | Radar ratio | unitless | Present in modelling dataset |
| `fecha` | modelling dataset and raw predictor tables | Date key | date | |
| `lon`, `lat` | pixel predictor outputs and model outputs | Spatial coordinates | decimal degrees | Used for map outputs |

## Spatial Datasets

| Dataset | Path | Purpose | Notes |
|---|---|---|---|
| Matorral polygon | `data/complementary/Matorral_SUCULENTAS_PNBFJ_UNI_TOPO.*` | Spatial mask for target vegetation unit | Core for landscape masking |
| Park polygon | `data/complementary/PNBFJ.*` | Park boundary context | Used for site map context |
| Tower point | `data/complementary/Torre Eddy.*` | Tower location | Used in map figures |

## Temporal Resolution Summary

| Dataset family | Resolution inferred | Confidence |
|---|---|---|
| `LEVEL3_FJ_2022_2025_ss.csv` | `TO VERIFY` | Low |
| `LEVEL3_FJ_2022_2025_ss_daily.csv` | daily | High |
| `LEVEL3_FJ_2022_2025_ss_v4_daily.csv` | daily | High |
| `LEVEL3_FJ_2022_2025_TEA_ready_hf.csv` | high frequency / regularized sub-daily | Medium |
| `LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv` | daily | High |
| `NEE_predictors_season_*.csv` | one record per date/scene at tower or aggregated support scale | Medium |
| `NEE_predictors_pixels_season_*.csv` | pixel-by-date records | High |

## Data Availability for GitHub

### Reasonable candidates to include

- processed daily flux tables needed to reproduce manuscript figures
- TEA-derived daily tables
- modelling-ready dataset
- seasonal predictor tables at small size
- complementary shapefiles
- final model outputs and selected raster products

### Strong candidates to exclude from normal GitHub tracking

- `data/raw/NEE_predictors_pixels_season_*.csv`
- temporary chunk directories
- shard outputs
- lock files

### Files excluded from GitHub if needed

If raw pixel predictor tables are excluded from GitHub, this should be documented in the public `README` and future data availability notes as:

- `excluded due to file size`
- `available on request`
- or `available via external archive / Zenodo / OSF / institutional storage`

## Important Uncertainties To Verify

1. Exact temporal resolution and provenance of `data/LEVEL3_FJ_2022_2025_ss.csv`
2. Exact distinction between `ss_daily` and `ss_v4_daily`
3. Exact formula represented by `WUE` in every derived table
4. Installation source/version of TEA
5. Which daily dataset is the manuscript's final source of record for each figure

