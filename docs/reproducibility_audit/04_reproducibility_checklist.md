# Reproducibility Checklist

## Current Technical Status

| Item | Current status | Notes |
|---|---|---|
| Git repository initialized | No | Folder is not yet a Git repo |
| Root README | No before this audit | Added in this audit |
| Root `.gitignore` | No before this audit | Added in this audit |
| Root citation metadata | No before this audit | Added `CITATION.cff` in this audit |
| Environment specification | No before this audit | Added inferred `requirements.txt` in this audit |
| Canonical workflow document | No before this audit | Added `docs/workflow.md` in this audit |
| Data dictionary | No before this audit | Added `docs/data_dictionary.md` in this audit |
| Formal automated tests | No | `tests/` contains check scripts, not assertion-based tests |
| Manuscript traceability matrix | No before this audit | Added in this audit |
| GitHub-safe file policy | No before this audit | Proposed via docs and `.gitignore` |

## What Can Be Reproduced Today

### Reasonably reproducible with existing files

- Daily/annual flux summaries from `data/LEVEL3_FJ_2022_2025_ss_daily.csv` and `data/LEVEL3_FJ_2022_2025_ss_v4_daily.csv`
- TEA input preparation via `scripts/make_TEA_ready_dataset.py`
- TEA partitioning run logic via `scripts/run_TEA_partitioning.py`
- Daily T/E/WUE derivation via `scripts/make_T_E_WUE_dataset.py`
- Main temporal figure logic for Figures 3-7
- Spatial model inputs via `scripts/build_model_dataset.py`
- Selected SVR prediction workflow via `scripts/modelo_predictivo.py`
- Landscape mean NEE values reported for the optimal model from `outputs/nee_opt_season_*.csv`

### Reproducible only after minor cleanup

- Figure exports for Figures 2-7
  - scripts exist
  - stable output writes are missing
- Supplementary annual metrics (Table S3)
  - calculations exist in `tests/`
  - export table is not versioned as a final artifact
- Figure 8 CART outputs
  - model logic exists
  - export path is not cleanly scripted

## What Is Not Reliably Reproducible Today

### 1. Full repo publication to GitHub

Why not:

- no Git repo yet
- no root publication metadata before this audit
- multiple files over GitHub's 100 MB limit
- total repo size is already large

How to fix:

- initialize Git
- keep large raw pixel predictor files outside normal Git or use LFS/external archive
- exclude caches, temp chunks, shards, lock files, and nested `.venv`

### 2. Exact final export for every manuscript figure/table

Why not:

- several scripts only show figures instead of saving them
- multiple candidate outputs exist
- some figures likely involved manual finishing outside the saved scripts

How to fix:

- add stable output paths for all figure scripts
- create a final `manifest` document mapping manuscript element -> script -> output file

### 3. Site map workflow (Figure 1)

Why not:

- the candidate script uses absolute external paths
- no portable final export chain is present

How to fix:

- create a portable map script using `data/complementary/`
- or document the exact GIS workflow if the final figure was assembled manually

### 4. One single modelling lineage

Why not:

- `scripts/` and `NEE_Model/` contain overlapping but not identical modelling workflows
- predictor sets differ across branches

How to fix:

- explicitly designate one workflow as canonical for the revised manuscript
- mark the other branch as `legacy` or `archive`

## Key Technical Gaps

| Gap | Why it matters | Suggested remedy |
|---|---|---|
| Absolute paths remain in several scripts | Breaks portability across machines | Replace with repo-relative `Path` usage |
| Mixed current and legacy workflows | Makes results hard to audit | Declare canonical branch in `README` and `docs/workflow.md` |
| `tests/` is not a real test suite | No automated verification | Rename to `checks/` or add assertions/pytest |
| Missing explicit output writes | Figure regeneration is fragile | Save final figures/tables programmatically |
| Large files exceed GitHub limits | Blocks standard GitHub push | Ignore, externalize, or place under LFS/archive |
| Environment versions are not pinned | Runs may drift over time | Add version pinning after first clean execution |
| TEA dependency source is not recorded | Water partitioning may fail on other machines | Document installation source and version explicitly |
| Some derived files have ambiguous provenance | Weakens trust in final numbers | Add per-output provenance notes or manifests |

## Minimal Action Set to Reach a Defensible Reproducibility Baseline

1. Initialize Git in the project root.
2. Keep >100 MB raw pixel predictors out of normal Git tracking.
3. Keep temp chunks, shards, caches, lock files, and nested `.venv` out of Git.
4. Use `docs/workflow.md` and `03_traceability_matrix.md` as the canonical narrative.
5. Decide the canonical modelling branch for the revised manuscript.
6. Add explicit `savefig` / `to_csv` targets for Figures 2-8 and Table S2/Table S3 outputs.
7. Record the external dependency source for TEA and any proprietary/preprocessing software such as EddyPro.

## Honest Bottom Line

This project is scientifically substantial and already contains enough material to support a reproducibility-oriented release. It is not yet a push-button reproducible repository, but the remaining barriers are mostly organizational and provenance-related rather than scientific absence.
