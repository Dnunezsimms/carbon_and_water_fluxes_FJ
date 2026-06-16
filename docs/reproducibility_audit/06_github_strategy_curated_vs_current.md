# GitHub Strategy: Curated Copy vs Current Working Directory

## Decision Context

Current working directory:

- `C:\projects\carbon_and_water_fluxes_FJ`

Observed context from the audit:

- approximate total size: `5.43 GB`
- three raw CSV files over `100 MB`
- `31` files over `50 MB`
- mixed workflows across `scripts/`, `tests/`, `NEE_Model/`, and `results/`
- portable and non-portable scripts coexist
- large intermediate outputs, shard directories, and temporary chunk files are present
- reproducibility documentation has now been added, but the working tree is still a research archive rather than a clean public repository

## Executive Recommendation

**Recommended option: A) create a curated public copy in a separate directory**

Suggested name:

- `C:\projects\carbon_and_water_fluxes_FJ_public`

Why:

- it minimizes the risk of accidental publication of heavy, internal, redundant, or legacy material;
- it makes the first Git history cleaner and more defensible;
- it preserves the current directory as the full working archive;
- it reduces day-to-day anxiety around `git status`, accidental `git add`, and later cleanup;
- it aligns better with the current state of the project, where the manuscript-facing branch is identifiable but not yet isolated.

## Quick Comparative View

| Option | Short description | Strategic fit now | Recommended? |
|---|---|---|---|
| A. Curated copy | Build a separate GitHub-facing directory from selected files only | Strong | Yes |
| B. Same working directory | Turn the current directory into the Git repo and rely on `.gitignore`, exclusions, and discipline | Possible but risky | Not preferred |

## 1. Risks of Uploading This Same Directory

### 1.1 Large files and GitHub limits

Critical blockers already present:

- `data/raw/NEE_predictors_pixels_season_1_20220704_20230630.csv` (`~452.71 MB`)
- `data/raw/NEE_predictors_pixels_season_2_20230701_20240630.csv` (`~505.40 MB`)
- `data/raw/NEE_predictors_pixels_season_3_20240701_20250630.csv` (`~599.23 MB`)

Additional context:

- `31` files exceed `50 MB`
- several of those are clearly non-publication artifacts, including temporary chunks and reviewer-export TIFFs

Implication:

- a same-directory Git workflow is operationally fragile from the first commit onward
- one accidental `git add .` can stage material that should never enter public history

### 1.2 Raw and intermediate scientific data

The current directory contains:

- raw predictor exports
- large daily/full-output CSVs
- intermediate raster shards
- alternate modelling intermediates
- duplicated or legacy derived products

Implication:

- the public boundary is not encoded in the current filesystem layout
- the distinction between `must publish`, `can publish`, and `should not publish` is still mostly conceptual

### 1.3 Sensitive or internal material

No API keys or obvious credentials were detected in prior audit passes, but the directory does include internal or non-publication material such as:

- CVs and cover letters at the repository root
- personal contact information in some script headers
- manuscript review workspace with large internal TIFF/PNG/PDF candidates
- nested project files under `vendimia_5_0_obj_3/`

Implication:

- the main risk is not secret leakage in the classical credential sense
- the main risk is publication of irrelevant, personal, or confusing internal material

### 1.4 Rutas absolutas y portabilidad

Multiple scripts still contain local machine paths, including:

- `C:\Users\...`
- `D:\Respaldos\...`
- `/home/cgajardo/...`
- Dropbox-based paths

This is especially frequent in `NEE_Model/` and in some preprocessing scripts.

Implication:

- the same directory is not just “large”; it is also heterogeneous in reproducibility quality
- if this directory becomes the public repo, the apparent scope of maintainability is wider than what is actually ready

### 1.5 Experimental branches and legacy analysis

Large branches not clearly needed for the revised manuscript include:

- `NEE_Model/` at roughly `1.833 GB`
- `results/` at roughly `1.647 GB`
- nested temp chunks under `NEE_Model/Figuras/model_30m_2/tmp_chunks_limpios_2/`
- raster shard directories under `results/raster_pipeline/shards_*`

Implication:

- same-directory publication forces you to actively defend why these remain present but excluded
- future maintenance becomes a constant “do not accidentally stage this” problem

### 1.6 Dirty-history risk

If you initialize Git in the current working directory:

- the first commit boundary becomes socially and technically important
- if large or irrelevant files are ever committed once, later removing them does not fully solve the repository-history problem

Implication:

- the cost of one early mistake is high

### 1.7 Reproducibility management risk

A single repo can still be reproducible, but only if:

- the canonical workflow is stable,
- ignored content is consistently ignored,
- legacy content is clearly quarantined,
- and the team maintains strong Git discipline.

This project is not yet at that equilibrium.

### 1.8 Accidental push risk

This is the most practical risk.

In the current directory, the probability of accidental staging is high because the workspace includes:

- giant raw files
- large generated outputs
- reviewer assets
- personal documents
- nested environments
- archived or alternate analyses

## 2. Advantages and Disadvantages of Creating a Curated Copy

### Concept

Example target:

- `C:\projects\carbon_and_water_fluxes_FJ_public`

Purpose:

- a public, manuscript-facing repository
- built from selected, justified, documented assets only
- leaving the original directory untouched as the working archive

### Advantages

#### 2.1 Clean publication boundary

The public scope becomes explicit by construction.

Only selected assets enter the new directory:

- repository metadata
- manuscript-facing scripts
- reproducibility docs
- lightweight figures/tables
- small publicable processed data
- placeholders or instructions for excluded data

#### 2.2 Lower accidental-risk surface

Because excluded material never enters the public directory, you reduce risk from:

- accidental staging
- accidental push
- later history cleanup

#### 2.3 Better first Git history

The first commit can already look professional:

- coherent structure
- clear README
- no giant binaries
- no legacy clutter

#### 2.4 Better signaling to reviewers and collaborators

A curated repository communicates:

- intentionality
- scope control
- professionalism
- transparency about what is and is not included

#### 2.5 Easier maintenance

You can continue working messily, honestly, and fully in the original archive, while only promoting stable pieces into the public repo.

This is often the safest workflow for thesis/article projects.

#### 2.6 Size feasibility

A rough upper-bound estimate for a manuscript-facing subset including docs, scripts, models, outputs, selected figures, `data/processed`, `data/complementary`, and small seasonal predictor files was around:

- `~272.62 MB`

That is still not tiny, but it is dramatically more manageable than `5.43 GB`, and it is compatible with a serious curation pass.

### Disadvantages

#### 2.7 Duplicate maintenance

You will temporarily maintain:

- one working archive
- one public-facing repository

This is extra work.

#### 2.8 Need for explicit sync discipline

After the public repo exists, you need a rule for promoting changes:

- fix in working archive first
- then copy or patch into the public repo

#### 2.9 Possible drift if unmanaged

If the curated repo is built once and then neglected, it can diverge from the live science workflow.

This is manageable, but only if the public repo is treated as a maintained deliverable rather than a one-time export.

## 3. Advantages and Disadvantages of Keeping a Single Repo

### What option B would require

At minimum:

- robust `.gitignore`
- very careful first staging
- strong exclusion policy
- possibly Git LFS
- clear README and workflow docs
- ongoing discipline to keep experimental outputs out of history

### Advantages

#### 3.1 One source of truth

You avoid duplication and repository drift.

#### 3.2 Simpler mentally if the project is already clean

For mature and stable projects, one repository is often ideal.

#### 3.3 Easier future linking between public and working history

You keep everything in one versioned place.

### Disadvantages

#### 3.4 High setup risk right now

The current directory is not yet clean enough for this to be the low-risk choice.

#### 3.5 `.gitignore` is not a safety guarantee

`.gitignore` helps, but:

- it does not protect against all staging mistakes forever
- it does not simplify conceptual scope
- it does not automatically separate manuscript-critical from legacy content

#### 3.6 Git LFS does not solve the strategic problem

Git LFS is useful only if large files truly belong in the public repo.

Here, many large files are not just “large”; they are also:

- raw
- intermediate
- redundant
- legacy
- or not required for a clean manuscript-facing release

So LFS would solve only part of the problem, and could create cost or complexity without improving clarity.

#### 3.7 Public scope remains blurry

Even with a good `.gitignore`, the directory still physically contains:

- legacy workflows
- experimental chunks
- reviewer exports
- personal documents
- nested project debris

That blurriness makes the public repo harder to defend.

### Viability assessment for option B

Option B is **viable**, but **not the most advisable first move** for this project in its current state.

It becomes more attractive only if:

- you strongly need a single long-lived repository,
- you are prepared to spend time quarantining legacy branches inside the same tree,
- and you are comfortable managing a high-discipline first commit.

## 4. Recommendation

## Recommended option

**Choose A: create a curated public copy**

Suggested path:

- `C:\projects\carbon_and_water_fluxes_FJ_public`

### Why this is the best fit

1. It keeps the current working archive intact.
2. It sharply lowers accidental publication risk.
3. It produces a cleaner first Git history.
4. It makes the manuscript-facing workflow easier to explain and defend.
5. It avoids forcing Git LFS decisions before you decide what actually deserves publication.

### Residual risks even with option A

- the curated repo can still drift if not maintained;
- some scripts still need path cleanup before they become fully reproducible;
- some figures/tables still need explicit export stabilization;
- decisions about excluding raw heavy data must be clearly documented in the public README.

### When I would choose option B instead

I would choose option B only if all of the following were true:

1. you want this to remain the long-term active development repo;
2. you are willing to quarantine or archive `NEE_Model/`, heavy shards, reviewer exports, and personal files inside the same tree;
3. you accept the risk and discipline demands of a very careful first commit;
4. you want the public and working histories to be identical from day one.

That is possible, but it is not the safer professional move here.

## 5. Proposed Structure for the Public Repo

```text
carbon_and_water_fluxes_FJ_public/
  README.md
  .gitignore
  CITATION.cff
  requirements.txt
  LICENSE                  # if chosen
  data/
    README.md              # describes included/excluded data
    processed/
    complementary/
    raw/
      README.md            # placeholder only, or small publicable files
  docs/
    workflow.md
    data_dictionary.md
    reproducibility_audit/
  figures/
    manuscript/
  models/
  outputs/
    tables/
    lightweight_maps/
  scripts/
  checks/                  # optional rename of manuscript-facing test/check scripts
```

## 6. Preliminary Include List

These are strong candidates to include in the curated public repo.

### Root metadata

- `README.md`
- `.gitignore`
- `requirements.txt`
- `CITATION.cff`
- `LICENSE` if you choose one

### Documentation

- `docs/workflow.md`
- `docs/data_dictionary.md`
- `docs/reproducibility_audit/`

### Core manuscript-facing scripts

- `scripts/Figure_2.py`
- `scripts/Figure_3.py`
- `scripts/Figure_4.py`
- `scripts/Figure_5.py`
- `scripts/Figure_6.py`
- `scripts/Figure_7.py` or one declared final variant
- `scripts/build_model_dataset.py`
- `scripts/make_TEA_ready_dataset.py`
- `scripts/run_TEA_partitioning.py`
- `scripts/make_T_E_WUE_dataset.py`
- `scripts/merge_tea_with_full_data.py`
- `scripts/modelo_predictivo.py`
- `scripts/plot_nee.py`
- `scripts/RF_CART.R` if retained as documented legacy/manuscript support

### Small/medium data likely needed

- selected files from `data/processed/`
- selected daily processed files from `data/`
- `data/complementary/` shapefiles
- small seasonal predictor tables:
  - `data/raw/NEE_predictors_season_1_20220704_20230630.csv`
  - `data/raw/NEE_predictors_season_2_20230701_20240630.csv`
  - `data/raw/NEE_predictors_season_3_20240701_20250630.csv`

### Models and outputs

- `models/best_SVR_NDVI_RAD_topo.joblib`
- `models/best_SVR_NDVI_Pol_moisture_RAD_topo.joblib`
- selected outputs in `outputs/`
- selected lightweight final figures
- selected lightweight table exports

### Optional manuscript-facing checks

From `tests/`, include only those that truly support manuscript numbers, and preferably rename or relocate them later:

- `tests/ecohydrological_metrics.py`
- `tests/accumulated_NEE.py`
- `tests/accumulated_et.py`
- `tests/precip_metrics.py`

## 7. Preliminary Exclude List

### Must exclude from normal GitHub repo

- `data/raw/NEE_predictors_pixels_season_*.csv`

### Strongly recommended to exclude

- `NEE_Model/` as a whole, unless you later decide to publish it as a clearly marked legacy branch
- `results/raster_pipeline/shards_*`
- `NEE_Model/Figuras/model_30m_2/tmp_chunks_limpios_2/`
- nested `.venv`
- lock files
- LaTeX build artifacts
- root CV and cover-letter materials
- reviewer working TIFF/PDF/PNG candidate exports not essential to the public package
- `figures/figures.rar`
- nested project `vendimia_5_0_obj_3/`

### Case-by-case exclude

- large Word/PDF internal documents
- duplicate figures
- exploratory scripts that are not part of the manuscript-facing workflow
- alternate figure versions
- outputs that can be regenerated and are large but not needed for the repo narrative

## 8. Suggested Commands (Do Not Execute Yet)

These are suggestion-only commands for a future implementation pass.

### Create curated directory

```powershell
New-Item -ItemType Directory -Path "C:\projects\carbon_and_water_fluxes_FJ_public"
```

### Create top-level public structure

```powershell
New-Item -ItemType Directory -Path "C:\projects\carbon_and_water_fluxes_FJ_public\docs"
New-Item -ItemType Directory -Path "C:\projects\carbon_and_water_fluxes_FJ_public\data"
New-Item -ItemType Directory -Path "C:\projects\carbon_and_water_fluxes_FJ_public\scripts"
New-Item -ItemType Directory -Path "C:\projects\carbon_and_water_fluxes_FJ_public\models"
New-Item -ItemType Directory -Path "C:\projects\carbon_and_water_fluxes_FJ_public\outputs"
New-Item -ItemType Directory -Path "C:\projects\carbon_and_water_fluxes_FJ_public\figures"
```

### Example copy commands for selected assets

```powershell
Copy-Item "C:\projects\carbon_and_water_fluxes_FJ\README.md" "C:\projects\carbon_and_water_fluxes_FJ_public\"
Copy-Item "C:\projects\carbon_and_water_fluxes_FJ\CITATION.cff" "C:\projects\carbon_and_water_fluxes_FJ_public\"
Copy-Item "C:\projects\carbon_and_water_fluxes_FJ\requirements.txt" "C:\projects\carbon_and_water_fluxes_FJ_public\"
Copy-Item "C:\projects\carbon_and_water_fluxes_FJ\docs" "C:\projects\carbon_and_water_fluxes_FJ_public\" -Recurse
```

### Size checks before Git init

```powershell
Get-ChildItem "C:\projects\carbon_and_water_fluxes_FJ_public" -Recurse -File | Sort-Object Length -Descending | Select-Object -First 50 Name, Length
Get-ChildItem "C:\projects\carbon_and_water_fluxes_FJ_public" -Recurse -File | Where-Object { $_.Length -gt 50MB }
Get-ChildItem "C:\projects\carbon_and_water_fluxes_FJ_public" -Recurse -File | Where-Object { $_.Length -gt 100MB }
```

### Git initialization only after curation is verified

```powershell
git init
git status
```

## 9. Concrete Implementation Plan for Option A

### Phase 1. Prepare scope

1. Define the public repo name.
2. Confirm the canonical manuscript-facing workflow.
3. Confirm which datasets are publicable and which must be replaced by placeholders.

### Phase 2. Build the curated directory

1. Create the new public directory.
2. Copy only repository metadata and documentation first.
3. Copy only the selected manuscript-facing scripts.
4. Copy only required small/medium data and complementary shapefiles.
5. Copy only selected models and lightweight outputs.
6. Add `data/README.md` placeholders for excluded raw data.

### Phase 3. Size and risk audit

1. Check total size.
2. Check files over `50 MB`.
3. Check files over `100 MB`.
4. Search again for absolute paths and personal/internal materials.
5. Verify there is no nested environment or temp directory.

### Phase 4. Public-facing cleanup

1. Tighten `.gitignore` for the curated repo.
2. Make the README explicitly state what is excluded and why.
3. Add placeholders or instructions for non-included data.
4. Keep only final figures/tables that add value and remain lightweight.

### Phase 5. Git only after review

1. Review the curated directory manually.
2. Only then initialize Git in the curated directory.
3. Inspect `git status` before any first commit.

## 10. Checklist Before the First Commit

- [ ] Public repo directory created separately from the working archive
- [ ] Total size checked
- [ ] No files over `100 MB`
- [ ] Heavy raw predictor pixel files excluded
- [ ] No nested `.venv`
- [ ] No temp chunks or shard directories
- [ ] No root CVs, cover letters, or unrelated personal materials
- [ ] No reviewer-only TIFF/PDF exports unless intentionally justified
- [ ] README explains included and excluded data clearly
- [ ] Data placeholders exist where public data cannot be shipped
- [ ] Canonical workflow is documented
- [ ] Scripts included are manuscript-facing and minimally portable
- [ ] Models included are actually referenced by the manuscript branch
- [ ] Final output list is intentional and not duplicated
- [ ] Only then: initialize Git

## Final Bottom Line

For this project, a **curated public copy is the safer and more professional strategy**.

It is more honest, easier to defend, less error-prone, and much better aligned with the current reality of the repository: a rich scientific working archive that is not yet structurally equivalent to a clean public software/data release.
