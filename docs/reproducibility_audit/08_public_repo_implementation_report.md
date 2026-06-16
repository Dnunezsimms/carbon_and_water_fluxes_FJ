# 08. Public Repository Implementation Report

Date: 2026-06-16  
Source directory: `C:\projects\carbon_and_water_fluxes_FJ`  
Destination directory: `C:\projects\carbon_and_water_fluxes_FJ_public`

## Scope

This report documents the implementation of a curated, manuscript-facing public repository derived from the working archive. The original project was preserved as the full internal workspace. The public copy was built using an allow-list strategy to minimize the risk of publishing oversized, redundant, experimental, or sensitive material.

## Destination Status

- Public folder created: `C:\projects\carbon_and_water_fluxes_FJ_public`
- Curation strategy used: allow-list, based on `06_github_strategy_curated_vs_current.md`
- Original repository modified destructively: no
- Raw data modified: no
- Manuscript `.docx` modified: no
- Local Git initialized in public copy: yes
- Commit created: no
- GitHub upload performed: no

## Main Content Copied

The public repository currently includes:

- root documentation and metadata:
  - `README.md`
  - `CITATION.cff`
  - `LICENSE` placeholder
  - `requirements.txt`
  - `.gitignore`
- documentation:
  - `docs/workflow.md`
  - `docs/data_dictionary.md`
  - `docs/data_availability.md`
  - `docs/reproducibility_audit/`
- manuscript-facing scripts:
  - `scripts/preprocessing/`
  - `scripts/analysis/`
  - `scripts/figures/`
- lightweight, public-facing data subsets:
  - selected `data/processed/` files
  - selected `data/external/complementary/` files
  - compact seasonal predictor CSVs in `data/external/remote_sensing_predictors/`
- lightweight models and outputs:
  - `models/`
  - final figures in `results/figures/`
  - manuscript-relevant tables in `results/tables/`
  - selected raster summaries in `results/rasters/`
  - selected diagnostic CSVs in `results/diagnostics/`
- placeholders and disclosure files:
  - `data/README.md`
  - `data/raw/README.md`
  - `data/external/README.md`
  - `manuscript/README.md`
  - `notebooks/README.md`

## Main Content Excluded

The following categories were intentionally left out of the public copy:

- heavy raw eddy covariance and pixel-level predictor datasets
- any file over 100 MB
- any file over 50 MB without strong manuscript-facing justification
- large intermediate outputs not needed to understand the paper workflow
- experimental or branch-like analysis areas not clearly tied to the manuscript
- reviewer-working binary material and internal working subfolders
- manuscript Word files and other internal editorial artifacts
- caches, checkpoints, and temporary files

## Documentation Changes Applied

The public repository documentation was adapted to make the scope honest and GitHub-ready:

- a new public `README.md` was created with:
  - project description
  - manuscript relationship
  - repository structure
  - reproduction guidance
  - explicit data availability language
  - citation guidance
- `docs/workflow.md` received a public-repository note
- `docs/data_dictionary.md` received a public-repository note
- `docs/data_availability.md` was created
- `.gitignore` was tailored for a curated public repository
- `CITATION.cff` was created for repository citation
- placeholder README files were added where data or manuscript files are intentionally absent

## Script Adjustments Applied

Only safe, non-scientific path and packaging adjustments were made in the public copy:

- several Python scripts were updated to derive the repository root from `__file__`
- multiple scripts were pointed from flat `data/` paths to the curated public layout:
  - `data/processed/`
  - `data/external/complementary/`
  - `data/external/remote_sensing_predictors/`
  - `results/tables/`
  - `results/figures/`
- `RF_CART.R` was updated to use `data/processed/LEVEL3_FJ_merged_ET_T_WUE.csv`
- files that still depend on excluded heavy inputs were left documented rather than force-rewritten

No scientific logic, manuscript text, or original numerical results were intentionally altered.

## Final Size Audit

- Total public repository size: `69,537,871 bytes` (`66.32 MB`)
- Files `>10 MB`: none
- Files `>50 MB`: none
- Files `>100 MB`: none

Largest files currently present:

| File | Approx. size |
|---|---:|
| `results/tables/pixel_stats_cross_seasons_accum_stats.csv` | 8.57 MB |
| `data/processed/LEVEL3_FJ_2022_2025_no_gaps_for_TEA.csv` | 6.82 MB |
| `results/figures/figure_9.png` | 5.02 MB |
| `results/figures/NEE_COMPARISON_4MAPS.png` | 4.66 MB |
| `results/figures/NEE_FINAL_PAPER.png` | 4.23 MB |

## GitHub Risk Check

Current status for the curated public copy:

- oversized files blocking standard GitHub use: not detected
- files above the 100 MB GitHub hard limit: not detected
- accidental copy of the heavy original `data/`, `results/`, or `NEE_Model/` trees: not detected
- obvious absolute Windows paths in public scripts: not detected after path cleanup
- raw data accidentally exposed: not detected in the curated subset reviewed for this build

## Residual Risks

The public repository is substantially cleaner than the working archive, but some honest limitations remain:

- some scripts still require datasets that are intentionally not distributed in the public copy
- some figure or modeling scripts may need a future second pass for fully parameterized execution from a single entry point
- `LICENSE` is currently a placeholder and should be replaced with a formal license decision before publication
- `CITATION.cff` is usable, but author and DOI metadata should be checked before the first public release
- text encoding artifacts remain in a few script print statements; these do not appear to affect scientific outputs but should be cleaned later
- the manuscript file itself is not distributed here, so the `manuscript/` folder is documentation-only

## Git Initialization Check

Local `git init` was executed in `C:\projects\carbon_and_water_fluxes_FJ_public`.

Observed status:

- the repository initialized successfully
- `git status` showed the curated repository files as expected untracked content
- no unexpected heavy directories appeared at initialization time

Assessment:

- size is comfortably below practical GitHub thresholds
- no file exceeds GitHub's 100 MB hard limit
- the repository structure is manuscript-facing and explainable
- explicit documentation exists for omitted data and absent manuscript files
- the main remaining issues are documentation/polish issues rather than publication blockers

## Checklist Before First Commit

- review `LICENSE` and replace placeholder text with the selected license
- confirm `CITATION.cff` metadata, especially authors, title, year, and repository URL
- inspect `git status` after `git init` to confirm no unexpected files appear
- decide whether `models/` should remain in the first public release or move to a later tagged release
- optionally clean minor encoding artifacts in user-facing script messages
- optionally add a top-level release note or `CHANGELOG.md` for the first public version

## Suggested Next Step

Proceed with local initialization only:

1. review `git status`
2. decide whether all currently untracked files belong in the first public release
3. stage selectively after the final metadata check

Do not push until the license decision and metadata review are complete.
