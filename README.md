# Nobel laureate repeat collaboration

Code and author–paper identifiers for studying repeated collaboration, collaboration duration, and citation/innovation measures among Nobel laureates in Physics, Chemistry, and Medicine. Python notebooks produce figures, and the R notebook estimates regressions and exports prediction grids.

## Contents

| File | Purpose |
| --- | --- |
| `423NobelLaureates_2024.csv.zip` | 423 laureate records with `AuthorID`, `Author_Name`, `Prize year`, and `Field`. |
| `NobelLauPubs_2024.csv.zip` | Author–paper links with `PaperID` and `AuthorID`. |
| `Career illustration.ipynb` | Focal-author career illustration and collaboration duration/count figures. |
| `Prize paper show lower k.ipynb` | Comparisons between papers grouped by the `Nobel_paper` indicator. |
| `R reg margins.ipynb` | Regressions and prediction grids for the full sample and each field. |
| `Plot margins.ipynb` | Surface plots from the R prediction grids. |

Official prize metadata is available from [NobelPrize.org](https://www.nobelprize.org/prizes/lists/all-nobel-prizes/).

## Installation

Use Python 3.11 or newer and launch Jupyter from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

For `R reg margins.ipynb`, use R 4.4 with `IRkernel`, `fixest`, and `marginaleffects`:

```r
install.packages(c("IRkernel", "fixest", "marginaleffects"))
IRkernel::installspec(user = TRUE)
```

Record the Python and R package versions with generated results.

## Configuration

Set directory and analysis parameters through environment variables before starting Jupyter:

| Variable | Default | Purpose |
| --- | --- | --- |
| `HSSC_DATA_DIR` | `data/` | Input table directory. |
| `HSSC_OUTPUT_DIR` | `outputs/` | Figure and regression output directory. |
| `HSSC_MARGINS_DIR` | Output directory | Prediction grids used by the surface plotting notebook. |
| `HSSC_FOCAL_AUTHOR_ID` | `2163147449` | Author used in the career illustration. |
| `HSSC_BOOTSTRAP_RESAMPLES` | `10000` | Bootstrap repetitions; minimum 1,000. |
| `HSSC_RANDOM_SEED` | `1` | Random seed for bootstrap figures. |

```bash
export HSSC_DATA_DIR=data
export HSSC_OUTPUT_DIR=outputs
jupyter lab
```

Python and R input helpers accept CSV files and ZIP archives containing a single CSV. Bundled laureate metadata is read from the repository root.

## Usage

1. Set the input and output directories for the selected notebook.
2. Open a fresh Python or R kernel and run cells from top to bottom.
3. Run `R reg margins.ipynb` before `Plot margins.ipynb`. The R notebook exports citation and disruption prediction grids for the full sample, Physics, Chemistry, and Medicine.
4. Find figures and tables in the configured output directory.

The career illustration uses the focal author's first publication year as the career origin. Collaboration figures summarize duration, publication counts, citation measures, novelty, and disruption. Prize-paper comparisons use the supplied binary `Nobel_paper` indicator and author–career-year matching. The R notebook contains the outcome definitions, field splits, and model specifications. Bootstrap figures use the configured number of repetitions and seed.

## Source checks

```bash
python scripts/check_sources.py
python scripts/check_sources.py --require-r
```

The source checks parse Python, notebook JSON, and R syntax, and require clean notebook execution state. GitHub Actions runs the same static checks.

## Citation and license

Use `CITATION.cff` to cite the repository and record the exact commit used. Cite upstream datasets separately. `LICENSE` covers code and documentation; source datasets remain subject to their respective terms.
