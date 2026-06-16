# Public Repository Manifest

## Purpose

This manifest defines the allow-list used to construct the public manuscript-facing repository:

- source archive: `C:\projects\carbon_and_water_fluxes_FJ`
- public destination: `C:\projects\carbon_and_water_fluxes_FJ_public`

The strategy is allow-list based. Only explicitly selected assets should be copied.

## Decision Summary

### Public repository goal

Create a clean, professional, GitHub-ready repository that contains:

- manuscript-facing documentation
- selected reproducible scripts
- lightweight final figures and tables
- small/medium processed data needed for transparency
- explicit placeholders for large or excluded data

### Archive repository goal

Keep the original directory unchanged as the full research workspace and provenance archive.

## Inclusion List

| Include block | Source path(s) | Approx. size | Reason for inclusion | Risk notes | Decision |
|---|---|---:|---|---|---|
| Root metadata | `README.md`, `.gitignore`, `requirements.txt`, `CITATION.cff` | `<1 MB` | Core project metadata for public repo | Low | Include |
| Public license placeholder | new `LICENSE` in public repo | negligible | Avoid shipping a repo without license guidance, while not inventing legal terms on behalf of all stakeholders | Must be explicit that final license selection is pending | Include |
| Main reproducibility docs | `docs/workflow.md`, `docs/data_dictionary.md` | `<1 MB` | Core interpretation and reproducibility narrative | Low | Include |
| Audit docs | `docs/reproducibility_audit/*.md` | `<1 MB` | Transparency about curation, gaps, and decisions | Low | Include |
| Selected preprocessing scripts | `scripts/make_TEA_ready_dataset.py`, `scripts/run_TEA_partitioning.py`, `scripts/make_T_E_WUE_dataset.py`, `scripts/merge_tea_with_full_data.py` | `<1 MB` | Support TEA and merged daily workflow used by manuscript-facing analyses | Some scripts require path cleanup or TODO notes | Include |
| Selected analysis scripts | `scripts/build_model_dataset.py`, `scripts/modelo_predictivo.py`, `scripts/RF_CART.R`; selected metric/check scripts from `tests/` | `<1 MB` | Support modelling, CART, and supplementary annual metrics | `tests/` scripts are not formal tests; should be reframed as checks in public repo | Include |
| Selected figure scripts | `scripts/Figure_2.py` to `scripts/Figure_7.py`, `scripts/Figure_10.py`, `scripts/plot_nee.py` | `<1 MB` | Direct support for main manuscript figures and spatial figure assembly | Several need relative-path adjustment in public copy | Include |
| Processed daily datasets | `data/LEVEL3_FJ_2022_2025_ss_daily.csv`, `data/LEVEL3_FJ_2022_2025_ss_v4_daily.csv`, `data/LEVEL3_FJ_2022_2025_daily_cleaned_T_E.csv`, `data/LEVEL3_FJ_merged_ET_T_WUE.csv` | `~4.49 MB` | Core small/medium tables for figures and checks | Low | Include |
| TEA-related processed datasets | `data/LEVEL3_FJ_2022_2025_no_gaps_for_TEA.csv`, `data/LEVEL3_FJ_2022_2025_no_gaps_for_TEA_TEA_outputs.csv`, `data/LEVEL3_FJ_2022_2025_no_gaps_for_TEA_TEA_outputs_daily_with_T_E.csv`, `data/processed/*` | `~11.36 MB` | Supports partitioning provenance and modelling dataset creation | Medium; TEA dependency remains external | Include |
| Small external predictor tables | `data/raw/NEE_predictors_season_1_20220704_20230630.csv`, `data/raw/NEE_predictors_season_2_20230701_20240630.csv`, `data/raw/NEE_predictors_season_3_20240701_20250630.csv` | `<0.05 MB` | Small remote-sensing predictor tables that help trace model inputs | Low | Include |
| Spatial support files | `data/complementary/*` | `~1.21 MB` | Tower location, park polygon, and modelling mask are central to map reproducibility | Low | Include |
| Saved manuscript models | `models/*` | `~1.06 MB` | Required for landscape NEE outputs and traceability | Low | Include |
| Final manuscript figures | `figures/figures/figure_1.png` to `figure_9.png` | `~12.22 MB` | Lightweight figure set already organized as manuscript figure exports | Need to state that they are included as generated outputs, not regenerated during audit | Include |
| Selected landscape outputs | `outputs/nee_opt_season_*.csv`, `outputs/nee_eco_season_*.csv`, `outputs/NEE_COMPARISON_4MAPS.png`, `outputs/NEE_FINAL_PAPER.png` | `~28.32 MB` | Supports spatial results in manuscript and public inspection of model outputs | Medium; some duplication with other figure exports remains | Include |
| Modelling summary tables | `results_intermediate_nonGPR.csv`, `results_with_GPR.csv`, `linear_loso_fold_metrics.csv`, `linear_per_season_coeffs.csv` | `<1 MB` | Supports model performance interpretation and table reconstruction | Low | Include |
| Lightweight raster summaries | `results/raster_pipeline/*.tif`, `results/raster_pipeline/pixel_stats_cross_seasons_accum_stats.csv`, `results/raster_pipeline/diagnostics/*.csv` | `~12 MB` | Keeps a compact spatial-summary branch without copying shard-heavy intermediates | Medium; public repo should explain that large shards are excluded | Include |
| Placeholders / explanatory READMEs | new files under `data/`, `data/external/`, `manuscript/`, `notebooks/` | negligible | Make exclusions explicit and professional | Low | Include |

## Exclusion List

| Exclude block | Source path(s) | Approx. size | Reason for exclusion | Risk if included | Decision |
|---|---|---:|---|---|---|
| Large raw pixel predictors | `data/raw/NEE_predictors_pixels_season_*.csv` | `>1.5 GB` total | Over GitHub limits and not required for a clean first public repo | Critical size and accidental-history risk | Exclude |
| Large ambiguous source tables | `data/frayjorge_fulloutput_2022_2025.csv`, `data/LEVEL3_FJ_2022_2025_ss.csv`, `data/biomet_FJ_20220704_20250918.csv` | `~141 MB` total | Large, ambiguously scoped for first public release, not needed for the manuscript-facing subset | Raises repo size and scope ambiguity | Exclude |
| Legacy/alternate workflow | `NEE_Model/` | `~1.833 GB` | Important archive branch, but not sufficiently clean or portable for first public repo | Major clutter, absolute paths, temp outputs | Exclude |
| Heavy raster shard intermediates | `results/raster_pipeline/shards_*` | `~1.6 GB` class with results tree | Intermediate-only outputs, not needed in public repo | Severe size inflation | Exclude |
| Temporary chunk outputs | `NEE_Model/Figuras/model_30m_2/tmp_chunks_limpios_2/` | many `70–80 MB` files | Temporary processing artifacts | High accidental staging risk | Exclude |
| Reviewer/private working exports | `docs/Fray Jorge/_working_codex_review/` large binaries and internal reviewer assets | `>100 MB` class within docs | Internal revision workspace, not needed for GitHub-facing repo | Confusing, bulky, not manuscript-facing in the public sense | Exclude |
| Full docs directory copy | `docs/` as a whole | `~215.63 MB` | Most of this weight comes from large internal manuscript/reviewer assets | Bloats repo and blurs publication scope | Exclude whole-copy; selectively include docs |
| Root career/application files | `CV_Dnunez.*`, `cv_academic.*`, `cv_spanish.*`, `cover_letter.*` | moderate | Not relevant to scientific public repo | Professional scope confusion | Exclude |
| Nested project | `vendimia_5_0_obj_3/` | small but unrelated | Separate project, separate environment | Noise and confusion | Exclude |
| Temporary / cache files | `.history/`, `__pycache__/`, `*.pyc`, `.~lock*`, LaTeX artifacts, `.venv`, `.ipynb_checkpoints` | low individually, high cumulatively | Not part of scientific release | Noise and accidental staging | Exclude |
| Duplicate landscape outputs | `outputs/nee_landscape_season_*.csv` | `~9.7 MB` | Duplicative relative to selected `nee_opt/nee_eco` outputs | Avoid ambiguity over canonical outputs | Exclude |
| Word manuscript files | manuscript `.docx` files | moderate | User requested not to copy the manuscript blindly; manuscript folder should carry explanation instead | Potential tracked-change/internal-comment risk | Exclude |

## Estimated Public Repository Size

A practical pre-copy estimate for the selected allow-list is approximately:

- `~70–80 MB`

This estimate assumes:

- only selected docs are copied, not the whole `docs/` tree;
- only selected `outputs/` are copied;
- large raw predictors, `NEE_Model/`, and shard directories remain excluded.

## Key Risks Still Present After Curation

1. Some selected scripts still need relative-path adjustments or explicit `TODO` notes.
2. The TEA dependency remains external and must be documented clearly.
3. The public repo will still not be fully push-button reproducible without the excluded large raw inputs.
4. Some final figures are included as results artifacts even when the exact final export chain remains partially ambiguous.

## Final Manifest Decision

Proceed with curation using a strict allow-list.

Do not copy:

- large raw pixel predictor files,
- `NEE_Model/`,
- shard directories,
- reviewer working binaries,
- or root personal/career files.

Do copy:

- lightweight reproducibility documentation,
- selected manuscript-facing scripts,
- compact processed data,
- compact model assets,
- lightweight figures/tables,
- and explicit placeholders for omitted data.
