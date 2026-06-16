# GitHub Publication Plan

## Goal

Prepare the repository for a professional, honest, and technically viable GitHub publication without deleting scientific assets or altering the manuscript `.docx`.

## Minimum Changes Required Before First Push

1. Initialize Git in `C:\projects\carbon_and_water_fluxes_FJ`
2. Keep files larger than 100 MB out of normal Git tracking
3. Add a root `.gitignore`
4. Add a root `README.md`
5. Add citation metadata
6. Decide whether the repository will be:
   - a full working thesis repo, or
   - a curated publication repo focused only on the paper workflow

## Recommended Changes Before Public Release

1. Declare one canonical workflow
   - likely the `scripts/` + `data/` + `models/` + `outputs/` branch for the revised manuscript
2. Treat `NEE_Model/` as one of:
   - `legacy/`
   - `archive/`
   - or a separate repository
3. Exclude unrelated career/application files from the publication footprint
4. Add stable figure/table export scripts
5. Add a small provenance manifest for final manuscript outputs

## Files That Should Stay Out of a Standard GitHub Push

### Must stay out unless Git LFS or external archive is used

- `data/raw/NEE_predictors_pixels_season_1_20220704_20230630.csv`
- `data/raw/NEE_predictors_pixels_season_2_20230701_20240630.csv`
- `data/raw/NEE_predictors_pixels_season_3_20240701_20250630.csv`

Reason:

- each file exceeds GitHub's normal 100 MB limit

### Strong candidates to exclude from version control

- `vendimia_5_0_obj_3/.venv/`
- `NEE_Model/Figuras/model_30m_2/tmp_chunks_limpios_2/`
- `results/raster_pipeline/shards_*`
- `*.aux`, `*.log`, `*.out`, `*.synctex.gz`
- `*.pyc`, `__pycache__/`
- lock files such as `.~lock*`
- `figures/figures.rar`
- root CV and cover-letter artifacts if this repo is meant to be article-focused

## Files That Should Be Included

### Core project metadata

- `README.md`
- `.gitignore`
- `requirements.txt`
- `CITATION.cff`
- `docs/workflow.md`
- `docs/data_dictionary.md`
- `docs/reproducibility_audit/*.md`

### Core scientific scripts

- `scripts/`
- selected `tests/` only if clearly documented as reproducibility checks

### Core reproducible data and model assets

- daily and processed CSVs needed for main figures/tables
- shapefiles under `data/complementary/`
- `models/best_SVR_NDVI_RAD_topo.joblib`
- `models/best_SVR_NDVI_Pol_moisture_RAD_topo.joblib`
- final outputs under `outputs/`
- selected raster outputs in `results/raster_pipeline/` if they are part of the declared publication package

## Risks to Report Transparently

1. The repo was not under Git at the time of this audit.
2. Some figure/table outputs were likely finalized manually or from interactive scripts.
3. Several scripts still contain absolute local paths.
4. More than one modelling lineage exists inside the same directory tree.
5. Exact software versions are not yet pinned.
6. TEA installation source is not documented in the repo.
7. EddyPro is an external preprocessing dependency and is not distributed here.

## Suggested Final Structure

This is a target structure proposal, not a request to move files immediately:

```text
carbon_and_water_fluxes_FJ/
  README.md
  .gitignore
  requirements.txt
  CITATION.cff
  data/
    raw/
    processed/
    complementary/
  models/
  outputs/
  results/
    raster_pipeline/
  scripts/
  docs/
    workflow.md
    data_dictionary.md
    reproducibility_audit/
  manuscript/
    Nunez-Simms manuscript-revised.docx   # optional future move, not done here
  legacy/
    NEE_Model/                            # optional future move, not done here
```

## Publication Strategies

### Option A: Single working repository

Keep most of the current content, but publish with strong documentation and a careful `.gitignore`.

Pros:

- preserves the real working history and scientific context
- less restructuring effort

Cons:

- still somewhat heavy
- legacy/current boundaries remain messier

### Option B: Curated publication repository

Create a cleaner GitHub-facing repo that includes only the canonical workflow and the assets required for the revised manuscript.

Pros:

- cleaner for reviewers, coauthors, and external collaborators
- easier to maintain on GitHub

Cons:

- requires a curation pass
- must clearly document what was intentionally omitted

## Recommended Publication Path

For this project, the safest professional path is:

1. keep this folder as the full working archive;
2. define the canonical revised-manuscript workflow inside it;
3. exclude large raw pixel files and obvious temp/auxiliary artifacts;
4. publish only after the workflow and figure provenance are documented;
5. consider a second curated public repo later if journal or collaborator expectations require a lighter footprint.
