"""Parse repository sources and notebook structure without executing analyses."""
import argparse
import ast
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-r", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    r_sources = []
    count = 0
    for path in root.rglob("*"):
        if any(part in {".git", ".venv", "data", "outputs", "__pycache__"} for part in path.relative_to(root).parts):
            continue
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            count += 1
        elif path.suffix.lower() == ".r":
            r_sources.append((str(path), path.read_text(encoding="utf-8")))
        elif path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix == ".ipynb":
            notebook = json.loads(path.read_text(encoding="utf-8"))
            if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
                raise ValueError(f"Invalid notebook structure: {path}")
            language = notebook.get("metadata", {}).get("kernelspec", {}).get("language", "python").lower()
            if "widgets" in notebook.get("metadata", {}):
                raise ValueError(f"Notebook contains widget state: {path}")
            for index, cell in enumerate(notebook["cells"], 1):
                if cell.get("cell_type") != "code":
                    continue
                if cell.get("outputs") != [] or cell.get("execution_count") is not None:
                    raise ValueError(f"Notebook contains execution output: {path}, cell {index}")
                source = "".join(cell["source"])
                label = f"{path}:cell {index}"
                if language == "r":
                    r_sources.append((label, source))
                else:
                    ast.parse(source, filename=label)
                count += 1
    rscript = shutil.which("Rscript")
    if r_sources and not rscript and args.require_r:
        raise RuntimeError("Rscript is required to parse R source.")
    if rscript:
        for label, source in r_sources:
            with tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "source.R"
                target.write_text(source, encoding="utf-8")
                result = subprocess.run([rscript, "--vanilla", "-e", "invisible(parse(file=commandArgs(TRUE)[1]))", str(target)], capture_output=True, text=True)
                if result.returncode:
                    raise SyntaxError(f"{label}\n{result.stderr}")
    print(f"Parsed {count} Python sources/notebook cells; R source blocks: {len(r_sources)} ({'parsed' if rscript else 'Rscript unavailable'}).")


if __name__ == "__main__":
    main()
