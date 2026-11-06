"""File locations and plotting configuration shared by the notebooks."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("HSSC_DATA_DIR", ROOT / "data")).expanduser().resolve()
OUTPUT_DIR = Path(os.environ.get("HSSC_OUTPUT_DIR", ROOT / "outputs")).expanduser().resolve()
MARGINS_DIR = Path(os.environ.get("HSSC_MARGINS_DIR", OUTPUT_DIR)).expanduser().resolve()
BOOTSTRAP_RESAMPLES = int(os.environ.get("HSSC_BOOTSTRAP_RESAMPLES", "10000"))
RANDOM_SEED = int(os.environ.get("HSSC_RANDOM_SEED", "1"))
FOCAL_AUTHOR_ID = int(os.environ.get("HSSC_FOCAL_AUTHOR_ID", "2163147449"))
BUNDLED_LAUREATES = ROOT / "423NobelLaureates_2024.csv.zip"
if BOOTSTRAP_RESAMPLES < 1000:
    raise ValueError("HSSC_BOOTSTRAP_RESAMPLES must be at least 1000 for interval estimation.")


def input_file(name):
    """Resolve a required external CSV, accepting its compressed counterpart."""
    base = name[:-4] if name.endswith(".zip") else name
    for candidate in (DATA_DIR / name, DATA_DIR / base, DATA_DIR / (base + ".zip")):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Required input {name!r} is missing from {DATA_DIR}. See README.md.")


def output_file(name):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR / name


def margin_file(name):
    path = MARGINS_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}. Generate it with R reg margins.ipynb or set HSSC_MARGINS_DIR.")
    return path
