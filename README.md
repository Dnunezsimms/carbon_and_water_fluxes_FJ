# carbon_and_water_fluxes_FJ_public

This repository is a curated public subset of the broader Fray Jorge carbon and water flux research workspace. It is designed as a manuscript-facing, GitHub-ready release focused on transparency, reproducibility, and professional presentation.

The related study examines carbon and water fluxes in the arid shrubland of Bosque Fray Jorge National Park, northern Chile, combining eddy covariance observations, ecohydrological analysis, and remote-sensing-based modelling of net ecosystem exchange (NEE).

## What This Repository Contains

- public-facing project metadata
- workflow and reproducibility documentation
- selected manuscript-facing scripts
- lightweight final figures and supporting result tables
- compact processed datasets that are suitable for public sharing in this repository
- saved model objects used by the manuscript-facing modelling branch
- placeholders and documentation for data that are not distributed here

## What This Repository Does Not Contain

- large raw pixel-level predictor tables
- heavy intermediate raster shards
- legacy or alternate modelling branches not needed for the curated release
- internal reviewer workspaces
- manuscript Word files or tracked-change review files
- unrelated personal or career documents from the original working archive

## Relation to the Working Archive

Source archive used to curate this public repository:

- `C:\projects\carbon_and_water_fluxes_FJ`

This public version was intentionally constructed using an allow-list approach. It should be interpreted as a clean release subset rather than a full mirror of the research workspace.

## Repository Structure

```text
README.md
CITATION.cff
LICENSE
requirements.txt
.gitignore
docs/
scripts/
data/
results/
models/
manuscript/
notebooks/
```

## Reproducibility Scope

The current best-supported public workflow is:

1. inspect workflow documentation in `docs/workflow.md`
2. review data availability notes in `docs/data_availability.md`
3. use processed datasets in `data/processed/`
4. review preprocessing scripts in `scripts/preprocessing/`
5. review analysis scripts in `scripts/analysis/`
6. review figure scripts in `scripts/figures/`
7. inspect final figures and result tables in `results/`

This repository improves transparency substantially, but it is not a fully push-button end-to-end rerun of the entire original workspace because some large upstream inputs are intentionally excluded.

## Data Availability

Raw eddy covariance and large model input datasets are not included in this repository due to file size and/or data sharing restrictions. Publicly shareable processed datasets, final figures, tables, scripts and workflow documentation are provided when available. Additional data may be requested from the corresponding author, subject to availability and permissions.

See also:

- `docs/data_availability.md`
- `data/README.md`
- `manuscript/README.md`

## Citation

Please cite this repository using `CITATION.cff`. For the associated scientific study, see the manuscript description in `manuscript/README.md`.

## Project Status

Current state: curated public release candidate prepared from the working research archive.
