# Manuscript Inventory

## Source Inspected

Primary manuscript path:

- `docs/Fray Jorge/Nunez-Simms manuscript-revised.docx`

For text inspection, this audit relied on the extracted text already present in:

- `docs/Fray Jorge/_working_codex_review/manuscript_revised_extracted.txt`

The manuscript `.docx` in `docs/Fray Jorge/` and the backup copy in `docs/Fray Jorge/_working_codex_review/source_docs/` have the same SHA256 hash:

- `94ED0EC374BB03CA09E2513CB2D57393F599B3A0A659FABAD7A00381E697B4D1`

Therefore, the extracted text used in this audit is anchored to the same manuscript file currently in scope.

## Title

`Carbon and water fluxes reveal that one of the world's most arid shrublands functions as a net carbon sink`

## Study Objectives Identified

The manuscript explicitly states three study objectives:

1. quantify annual carbon and water fluxes using eddy covariance measurements;
2. identify key climatic drivers and thresholds controlling these fluxes;
3. develop and validate a remote sensing based predictive model to upscale tower-derived NEE and quantify landscape carbon balance.

## Study Site

- Bosque Fray Jorge National Park (PNBFJ), Coquimbo Region, northern Chile
- Long-Term Socio-Ecological Research (LTSER) site
- Eddy covariance tower installed in July 2022
- Tower coordinates reported in the manuscript near `30 deg 39' 29.54'' S, 71 deg 39' 50.73'' W`
- Operational spatial unit for modelling: `Shrubland with Succulent` land-cover class

## Main Variables Mentioned

### Carbon fluxes

- NEE
- GPP
- RECO

### Water fluxes

- ET
- T
- E
- WUE
- RUE

### Ecohydrological and meteorological drivers

- precipitation
- effective precipitation
- PAR / PPFD
- VPD
- air temperature
- soil temperature
- SWC
- REW
- LW_IN

### Remote sensing / spatial predictors

- NDVI
- EVI
- NDWI
- LST
- SWC_norm
- Pol_moisture
- RAD_topo

## Data Sources Mentioned or Implied

1. Eddy covariance measurements, July 2022 to June 2025
2. Tower meteorological variables recorded every 30 minutes
3. EddyPro-based flux post-processing
4. ERA5 gap-filling support for meteorological variables
5. Historical precipitation records (1984-2025)
6. Sentinel-2 vegetation/moisture indices
7. Landsat 8/9 land surface temperature
8. Sentinel-1 radar-derived soil moisture proxies
9. DEM-derived terrain-adjusted radiation
10. CONAF vegetation maps / spatial masks

## Methods and Analyses Identified

### Flux processing and QA/QC

- Eddy covariance post-processing with EddyPro
- quality screening using plausible ranges and diagnostics
- CO2 filtering
- footprint filtering
- low-turbulence filtering using `u*`
- gap-filling of meteorological variables using ERA5 relationships

### Temporal aggregation

- ecohydrological years defined as July to June
- effective precipitation treated on a March to March logic
- daily, annual, and multi-year summaries

### Water partitioning

- TEA-based partitioning of ET into T and E

### Carbon-water diagnostics

- annual accumulations
- ecohydrological metrics
- Pearson correlations
- CART threshold analysis

### Spatial NEE modelling

- remote sensing predictors matched to tower NEE
- machine-learning model comparison
- SVR selected as the best-performing model
- retained model variants:
  - statistical optimum: `NDVI + RAD_topo`
  - ecohydrological model: `NDVI + RAD_topo + Pol_moisture`

## Figures Identified

| Element | Description from manuscript | Repo support expected |
|---|---|---|
| Figure 1 | Study area, tower location, fetch/footprint, ground photo | shapefiles, map script or GIS export |
| Figure 2 | Annual precipitation 1984-2025 | rainfall workbook + plotting script |
| Figure 3 | Daily VPD, ET, SWC, precipitation | daily flux dataset + figure script |
| Figure 4 | Daily ET partitioning into T and E, plus T/ET | daily T/E dataset + figure script |
| Figure 5 | PAR, carbon fluxes, REW | daily flux dataset + figure script |
| Figure 6 | Annual accumulations of NEE, GPP, RECO, ET, PP | daily flux dataset + aggregation script |
| Figure 7 | Pearson correlation matrix | merged daily dataset + correlation script |
| Figure 8 | CART models for NEE, ET, E, T | merged daily dataset + R CART workflow |
| Figure 9 | Spatial distribution of mean accumulated NEE and CV for two model configurations | model outputs + map script |
| Figure 10 | Comparison of model configurations / spatial variability interpretation | landscape outputs and/or raster diagnostics |

Supplementary figures/tables explicitly mentioned:

- Figure S1
- Figure S2
- Figure S3
- Table S1
- Table S2
- Table S3

## Tables Identified

| Element | Description from manuscript | Repo support expected |
|---|---|---|
| Table 1 | Remote sensing predictor variables and metadata | predictor summary or manually curated table |
| Table 2 | Selected SVR model configurations and performance | model metrics outputs |
| Table 3 | Literature comparison of shrubland/savanna NEE worldwide | manuscript-only synthesis, likely outside repo reproduction |
| Table S1 | Soil profile properties | supplementary-only, likely external/lab source |
| Table S2 | LOYO model performance summary | metrics CSVs from modelling workflow |
| Table S3 | Annual ecohydrological summary | daily flux + precipitation + T/E metrics scripts |

## Main Scientific Results Extracted

### From the abstract

- The shrubland acted as a persistent net carbon sink.
- Annual NEE ranged from `-187` to `-305 g C m^-2 yr^-1`.
- Annual ET ranged from `182` to `257 mm yr^-1`.
- Precipitation ranged from `66` to `184 mm yr^-1`.
- ET exceeded precipitation each year, interpreted as consistent with groundwater use.
- An SVR model using Sentinel-2 and terrain-adjusted radiation predicted NEE with `R^2 = 0.56`.
- Mean landscape NEE reported as `-188 +- 31 g C m^-2 yr^-1`.

### From the results section

- Year 1 effective precipitation: `90.1 mm`
- Year 2 effective precipitation: `65.9 mm`
- Year 3 effective precipitation: `183.7 mm`
- T/ET reported as `55.6%`, `50.7%`, and `62.1%` for Years 1-3
- WUE reported as `4.70`, `3.69`, `3.74 g C mm^-1`
- RUE reported as `9.50`, `11.54`, `5.24 g C mm^-1`
- Example annual tower-based NEE values include `-279`, `-187`, and `-305 g C m^-2 yr^-1`
- Best model section reports:
  - SVR with `NDVI + RADtopo + Polmoisture`: mean `R^2 = 0.563`, `RMSE = 0.983`, `MAE = 0.749`
  - ecologically retained alternative with `NDVI + RAD_topo + Pol_moisture`: mean `R^2 = 0.551`, `RMSE = 0.995`, `MAE = 0.769`
- Landscape mean NEE from optimal model:
  - Year 1: `-193.2 g C m^-2 yr^-1`
  - Year 2: `-208.5 g C m^-2 yr^-1`
  - Year 3: `-162.8 g C m^-2 yr^-1`
  - Overall mean: `-188.2 g C m^-2 yr^-1`

## Procedures in the Repo That Should Support These Results

### Tower/daily flux branch

- `scripts/EC_postprocessing_FJ.py`
- `scripts/EC_postprocessing_FrayJorge_v3.py`
- `scripts/FJ_data_to_daily.py`
- `scripts/make_TEA_ready_dataset.py`
- `scripts/run_TEA_partitioning.py`
- `scripts/make_T_E_WUE_dataset.py`
- `scripts/merge_tea_with_full_data.py`
- `scripts/Figure_3.py` to `scripts/Figure_7.py`
- `tests/ecohydrological_metrics.py`
- `tests/accumulated_NEE.py`
- `tests/accumulated_et.py`
- `tests/precip_metrics.py`

### Spatial modelling branch

- `scripts/build_model_dataset.py`
- `scripts/modelo_predictivo.py`
- `scripts/model_nee_v2.py`
- `scripts/metrics_model_results.py`
- `scripts/plot_nee.py`
- `scripts/Figure_10.py`

### Legacy / alternate modelling branch

- `NEE_Model/Scripts/model_30m_2_matorral_suculentas.py`
- `NEE_Model/Scripts/prediccion_nee_matorral_suculentas_fj.py`
- `NEE_Model/Scripts/mapas_tesis_dnunez.py`

These legacy files are important for transparency, but they complicate version traceability because their predictor sets and outputs do not fully match the revised manuscript.

## Inventory Conclusions

The manuscript is scientifically rich and specific enough to support a strong reproducibility package. The repository contains many of the expected supporting assets, but not all manuscript elements map cleanly to one stable script-output path. The temporal and ecohydrological results are better supported than the map-production and final figure-export chain.
