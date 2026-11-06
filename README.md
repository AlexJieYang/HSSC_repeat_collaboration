# Nobel laureate repeat collaboration

Code and author–paper identifiers for studying repeated collaboration, collaboration duration, and citation/innovation measures among Nobel laureates in Physics, Chemistry, and Medicine. The Python notebooks produce figures; the R notebook estimates the supplied regression specifications and exports prediction grids.

## Contents

| File | Purpose |
| --- | --- |
| `423NobelLaureates_2024.csv.zip` | 423 laureate records: `AuthorID`, `Author_Name`, `Prize year`, `Field`. |
| `NobelLauPubs_2024.csv.zip` | Author–paper links with `PaperID` and `AuthorID`. These links do not label prize-winning papers. |
| `Career illustration.ipynb` | Focal-author career illustration and collaboration duration/count figures. |
| `Prize paper show lower k.ipynb` | Comparisons using externally supplied `Nobel_paper` labels. |
| `R reg margins.ipynb` | R regressions and prediction grids for all records and each field. |
| `Plot margins.ipynb` | Surface plots from the R prediction grids. |

The bundled author list is a research sample, not a complete official Nobel laureate register. Its original author-ID matching procedure, bibliographic database release, and sample inclusion criteria are not recorded in this repository. In particular, the list does not contain Andrea Ghez. Do not infer an exhaustive population or a particular database release from the filename. Author and paper identifiers must be resolved against the matching bibliographic source release before joining other datasets.

Official prize metadata is available from [NobelPrize.org](https://www.nobelprize.org/prizes/lists/all-nobel-prizes/), including the [Medicine laureate list](https://www.nobelprize.org/prizes/lists/all-nobel-laureates-in-physiology-or-medicine/) and [Chemistry laureate list](https://www.nobelprize.org/prizes/lists/all-nobel-prizes-in-chemistry/).

## Environment

Use Python 3.11 or newer and launch Jupyter from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

For `R reg margins.ipynb`, use R 4.4 with the `IRkernel`, `fixest`, and `marginaleffects` packages. Install and register an R kernel in your local environment before opening that notebook:

```r
install.packages(c("IRkernel", "fixest", "marginaleffects"))
IRkernel::installspec(user = TRUE)
```

The dependency ranges identify the intended environment; the repository does not contain a resolved environment lockfile. Record the installed Python and R package versions with any generated results.

## Input and output locations

All external inputs belong in `data/` by default. Set environment variables before starting Jupyter when using other locations:

```bash
export HSSC_DATA_DIR=/absolute/path/to/input_tables
export HSSC_OUTPUT_DIR=/absolute/path/to/results
jupyter lab
```

Python and R accept either a named `.csv` or a ZIP containing its CSV counterpart. Put the files listed below directly inside `HSSC_DATA_DIR`. Bundled laureate metadata is read from the repository root. Missing required files produce an explicit message instead of substituting data.

| Input basename | Required fields used by the code | Used by |
| --- | --- | --- |
| `NobelCoauthors_.csv` | `Focal_AID`, `Field`, `PaperID`, `t`, `Nobel_paper`, `b_cum_k` | Prize comparison |
| `NobelCoauthors_2024.csv` | `Focal_AID`, `AuthorID`, `Field`, `PaperID`, `t`, `t_start`, `b_cum_k`, `age_diff`, `strong_tie`, `Team_Size`, `fau_Productivity`, `fau_cit`, `paper_cit5`, `CD_pct`, `Novelty_pct`, `paper_RaoStirling`, `cit_pct` | Career distributions; R models |
| `Paper_Author.csv` | `PaperID`, `AuthorID` | Focal-author illustration |
| `Paper_year.csv` | `PaperID`, `Year` | Focal-author illustration |
| `Paper_nref.csv` | `PaperID`, `Reference_Count` | Focal-author illustration |
| `Paper_nau.csv` | `PaperID`, `Team_Size` | Focal-author illustration |
| `Paper_ncit.csv` | `PaperID`, `cit_pct` | Focal-author illustration |
| `Paper_Disruption.csv` | `PaperID`, `CD_pct` | Focal-author illustration |
| `Paper_Atypicality.csv` | `PaperID`, `Novelty_pct` | Focal-author illustration |
| `Author_beginyear.csv` | `AuthorID`, `FirstYear` | Laureate career-time reference |

These external analysis tables and their preprocessing pipeline are not included. The bundled author–paper links alone do not determine collaboration histories, prize-winning paper labels, author ages, citation percentiles, or innovation measures. Obtain the matching processed tables and their variable definitions from the data provider/project maintainers; the notebooks do not infer or fabricate them. Keep `NobelCoauthors_` and `NobelCoauthors_2024` distinct unless their provenance and definitions establish equivalence.

Identifier lookup tables require one row per `PaperID` or `AuthorID` as appropriate. `Field` uses `Physics`, `Chemistry`, or `Medicine`. `Nobel_paper` is a supplied 0/1 label; `strong_tie` is a supplied indicator. `t`, `t_start`, and `age_diff` must use the source table's documented year convention consistently. `b_cum_k` and count variables must be nonnegative; `Team_Size` must be positive for logarithmic models. The source definitions and scales of percentile and innovation columns must accompany the data; no normalization is performed implicitly by the input helpers.

## Workflow

1. Obtain the external tables required for the selected notebook and configure their directory.
2. Run notebook cells from top to bottom in a fresh matching kernel. The career illustration uses `HSSC_FOCAL_AUTHOR_ID=2163147449` by default; set it to another bundled author ID as needed. Its career origin is the first available publication year in the supplied focal-author publication records.
3. For regression surfaces, run `R reg margins.ipynb` first. It writes `margins1_cit.csv` through `margins4_cit.csv` and the corresponding `_cd.csv` files. The indices denote all records, Physics, Chemistry, and Medicine. Then run `Plot margins.ipynb`.
4. Find figures and regression tables in `HSSC_OUTPUT_DIR` (default `outputs/`). `HSSC_MARGINS_DIR` can point the plotting notebook at existing prediction grids; it otherwise equals the output directory. Each grid needs `b_cum_k`, `age_diff_abs`, and `estimate` columns.

Bootstrap figures use `HSSC_BOOTSTRAP_RESAMPLES=10000` and `HSSC_RANDOM_SEED=1`; these are configurable, with at least 1,000 resamples required. Regression specifications, field splits, and supplied outcome definitions are contained in the R notebook. The bootstrap setting controls computational precision of the existing interval procedure and does not address dependence between observations.

## Source checks

```bash
python scripts/check_sources.py
python scripts/check_sources.py --require-r
```

The checks parse Python and notebook JSON, require empty notebook outputs, and parse R code when `Rscript` is installed. GitHub Actions requires R parsing as well. They do not execute notebook cells, estimate models, produce figures, or establish agreement with any publication.

## Citation and terms

Use `CITATION.cff` to cite this repository and record the exact commit used. Cite and comply with the terms of each upstream dataset separately. The repository does not specify a publication DOI. `LICENSE` applies to code and documentation; it does not grant rights to third-party bibliographic data. Confirm data provenance and redistribution terms before redistributing the bundled or external tables.
