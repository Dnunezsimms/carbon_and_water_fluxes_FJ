# Repository Diagnosis

## Scope

Audit date: 2026-06-16  
Repository path audited: `C:\projects\carbon_and_water_fluxes_FJ`  
Primary manuscript in scope: `docs/Fray Jorge/Nunez-Simms manuscript-revised.docx`

This diagnosis is based only on files currently present in the repository directory. No scientific scripts, raw data, or manuscript `.docx` files were modified.

## Executive Summary

The repository contains substantial scientific material for the thesis/article workflow, including processed eddy covariance datasets, TEA-related partitioning inputs/outputs, remote sensing predictor tables, trained models, landscape predictions, figures, and manuscript files. The scientific content is real and extensive.

However, the project is not yet ready for a clean GitHub publication. The main blockers are structural rather than scientific:

- the folder is not initialized as a Git repository;
- there is no root `README.md`, `.gitignore`, `LICENSE`, or project-level environment specification;
- multiple workflows coexist (`scripts/`, `tests/`, `NEE_Model/`, `results/raster_pipeline/`) without a single documented canonical path;
- several scripts still contain absolute local paths;
- the directory includes unrelated professional documents, temporary files, caches, lock files, and a nested `.venv`;
- several files exceed practical GitHub publication limits, and at least three raw CSV files exceed GitHub's 100 MB file limit.

## Repository Map

Approximate total size observed: `5.43 GB`

Top-level directories and approximate file counts:

| Path | Approx. files | Role inferred |
|---|---:|---|
| `.history/` | 1 | Editor/history artifact |
| `data/` | 45 | Core scientific data |
| `docs/` | 43 | Thesis/article documents and review workspace |
| `figures/` | 49 | Final or candidate figures |
| `models/` | 3 | Saved fitted models used by current scripts |
| `NEE_Model/` | 330 | Legacy or alternate NEE modelling workflow |
| `outputs/` | 11 | Final model outputs and landscape maps |
| `results/` | 158 | Raster pipeline outputs and intermediate shards |
| `scripts/` | 37 | Main Python/R workflow scripts |
| `tests/` | 12 | Analysis/check scripts, not formal automated tests |
| `vendimia_5_0_obj_3/` | 74 | Nested secondary project with its own env and `.venv` |

Important project-level observations:

- No root `.git/` directory detected.
- No root `README.md` detected.
- No root `.gitignore` detected.
- No root `LICENSE` detected.
- No root `CITATION.cff` detected before this audit.
- No root `requirements.txt` or `environment.yml` detected before this audit.
- No notebooks (`*.ipynb`) were detected in the repository scan.

## What Appears Complete or Substantive

The following parts appear materially present and scientifically useful:

1. **Main manuscript package**
   - `docs/Fray Jorge/Nunez-Simms manuscript-revised.docx`
   - additional manuscript/reviewer files under `docs/Fray Jorge/`

2. **Core eddy covariance and daily summary datasets**
   - `data/LEVEL3_FJ_2022_2025_ss.csv`
   - `data/LEVEL3_FJ_2022_2025_ss_daily.csv`
   - `data/LEVEL3_FJ_2022_2025_ss_v4_daily.csv`
   - `data/LEVEL3_FJ_merged_ET_T_WUE.csv`
   - `data/LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv`

3. **TEA-related preprocessing and outputs**
   - `scripts/make_TEA_ready_dataset.py`
   - `scripts/run_TEA_partitioning.py`
   - `scripts/make_T_E_WUE_dataset.py`
   - TEA-ready / TEA-derived files in `data/` and `data/processed/`

4. **Figure-generation scripts for the temporal/ecohydrological part of the paper**
   - `scripts/Figure_2.py` to `scripts/Figure_7.py`
   - related check scripts under `tests/`

5. **Remote sensing modelling branch used by the manuscript**
   - `scripts/build_model_dataset.py`
   - `scripts/modelo_predictivo.py`
   - `models/best_SVR_NDVI_RAD_topo.joblib`
   - `models/best_SVR_NDVI_Pol_moisture_RAD_topo.joblib`
   - `outputs/nee_opt_season_*.csv`
   - `outputs/nee_eco_season_*.csv`

6. **Landscape/raster outputs**
   - `results/raster_pipeline/*.tif`
   - `results/raster_pipeline/pixel_stats_cross_seasons_accum_stats.csv`
   - diagnostics and shard subfolders

7. **Supporting spatial inputs**
   - `data/complementary/Matorral_SUCULENTAS_PNBFJ_UNI_TOPO.*`
   - `data/complementary/PNBFJ.*`
   - `data/complementary/Torre Eddy.*`

## What Is Disordered

### 1. Multiple overlapping workflows

There is no single declared canonical workflow. At least four partially overlapping branches coexist:

- `scripts/` current paper workflow;
- `tests/` analysis/check scripts used like ad hoc notebooks;
- `NEE_Model/` older or alternate modelling workflow with different predictor sets and outputs;
- `results/raster_pipeline/` an additional rasterized prediction workflow.

This creates ambiguity about which branch generated the manuscript-ready numbers and figures.

### 2. Mixed publication scope

The repository mixes article/thesis content with unrelated or semi-related materials:

- CVs and cover letters in the repository root;
- LaTeX build artifacts (`*.aux`, `*.log`, `*.out`, `*.synctex.gz`);
- a nested project `vendimia_5_0_obj_3/`;
- PowerPoint files in `docs/`;
- reviewer working files and candidate exports under `docs/Fray Jorge/_working_codex_review/`.

### 3. Inconsistent path practices

Several scripts are portable and use `Path(__file__)`, but others still contain absolute local paths, including paths from different machines/users. Examples were detected in:

- `scripts/EC_postprocessing_FJ.py`
- `scripts/EC_postprocessing_FrayJorge_v3.py`
- `scripts/FJ_data_to_daily.py`
- `scripts/merge_tea_with_full_data.py`
- `scripts/t_media_años.py`
- `NEE_Model/Figuras/figura_matorral_suculentas.py`
- `NEE_Model/Scripts/mapas_tesis_dnunez.py`

### 4. Duplicate or version-fragmented outputs

Examples:

- `data/LEVEL3_FJ_2022_2025_ss_daily.csv` and `data/LEVEL3_FJ_2022_2025_ss_v4_daily.csv`
- multiple manuscript copies in `docs/` and `_working_codex_review/source_docs/`
- model outputs in both `outputs/` and `results/raster_pipeline/`
- older NEE models in `NEE_Model/` using different predictor sets than the revised manuscript

### 5. Encoding and naming issues

Several scripts display mojibake in headers/comments and some filenames contain spaces or ad hoc naming. This is manageable locally but weakens portability and professional presentation.

## What Is Missing for Reproducibility

1. A root-level project overview (`README.md`)
2. A root-level ignore policy (`.gitignore`)
3. A license choice and `LICENSE` file
4. A clean dependency lock or at least a documented base environment
5. A declared canonical workflow from raw inputs to manuscript figures/tables
6. A run order for scripts
7. A documented policy for data inclusion/exclusion on GitHub
8. A documented distinction between:
   - source data,
   - derived data,
   - final outputs,
   - exploratory/legacy files
9. Formal automated tests are absent
10. A reproducible script that exports final figure files directly to stable locations for all main manuscript figures

## GitHub Publication Risks

### Critical risks

1. **No Git repository initialized**
   - The folder is not yet under Git version control.

2. **Files too large for normal GitHub**
   - At least these files exceed 100 MB:
     - `data/raw/NEE_predictors_pixels_season_1_20220704_20230630.csv` (`~452.71 MB`)
     - `data/raw/NEE_predictors_pixels_season_2_20230701_20240630.csv` (`~505.40 MB`)
     - `data/raw/NEE_predictors_pixels_season_3_20240701_20250630.csv` (`~599.23 MB`)

3. **Repository size is already large**
   - Observed total size is `~5.43 GB`, before Git history.

### High risks

1. Temporary chunk files under `NEE_Model/Figuras/model_30m_2/tmp_chunks_limpios_2/`
2. Raster shard directories under `results/raster_pipeline/shards_*`
3. Nested virtual environment under `vendimia_5_0_obj_3/.venv/`
4. Lock files such as:
   - `data/.~lock.LEVEL3_FJ_2022_2025_ss.csv#`
   - lock-like files under `NEE_Model/outputs/...`

### Medium risks

1. Personal contact information embedded in script headers and CV files
   - `diegonunezsimms@gmail.com`
   - phone number in CV files and some headers
2. Reviewer workspace contains large TIFF/PDF/PNG candidate files
3. Root contains career documents not relevant to the article repository

### Sensitive information review

No API keys, tokens, private keys, or obvious credential files were detected in the repository scan performed for this audit.

## Recommendations, Prioritized

### Priority 1: Make publication technically possible

1. Initialize Git in the project root before any GitHub push.
2. Exclude >100 MB raw predictor files from normal Git tracking.
3. Exclude caches, lock files, temporary chunks, shard outputs, and nested `.venv`.
4. Add root-level `README.md`, `.gitignore`, `requirements.txt`, and `CITATION.cff`.
5. Decide whether `NEE_Model/` is:
   - part of the canonical workflow,
   - legacy archive,
   - or a separate project to be split later.

### Priority 2: Make the science traceable

1. Define one canonical path for:
   - flux preprocessing,
   - TEA partitioning,
   - merged daily dataset creation,
   - manuscript figure generation,
   - landscape modelling.
2. Document which output file corresponds to each manuscript figure/table.
3. Mark low-confidence figure/table links explicitly rather than forcing false certainty.

### Priority 3: Improve professional structure

1. Keep manuscript-facing documentation in `docs/`
2. Keep scientific scripts in `scripts/`
3. Separate `legacy/` or `archive/` content in a future cleanup pass
4. Remove unrelated career/application files from the publication footprint, or at minimum ignore them in Git

### Priority 4: Improve long-term reproducibility

1. Replace remaining hardcoded absolute paths with repo-relative paths
2. Add stable output writes for every figure script
3. Add a lightweight orchestration script once the canonical workflow is finalized
4. Convert `tests/` from exploratory scripts into either:
   - `checks/` for reproducibility audits, or
   - true automated tests with assertions

## Bottom Line

The repository contains enough real scientific material to support a strong open-science release, but it is not yet in publishable GitHub shape. The biggest immediate issue is not missing science; it is missing project hygiene and the coexistence of multiple partially overlapping workflows.
