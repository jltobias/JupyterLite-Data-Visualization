"""Build a shared JupyterLite / Jupyter Book Pages artifact from repository sources."""

from __future__ import annotations

import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "_build"
SITE = ROOT / "dist"
SOURCE_NOTEBOOK = "periodic_table_visualization_methods_python_examples_jupyterlite_REVISED.ipynb"
RELEASE_NOTEBOOK = "visualization_methods_v2.ipynb"


def run(*args: str) -> None:
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    env["PYTHONUTF8"] = "1"
    subprocess.run(args, cwd=ROOT, env=env, check=True)


def export_license_files() -> None:
    destination = SITE / "third-party-licenses"
    destination.mkdir(parents=True, exist_ok=True)
    records = []
    for name in (
        "jupyterlite-core", "jupyterlite-pyodide-kernel", "jupyterlab",
        "jupyter-book", "numpy", "pandas", "matplotlib", "networkx", "scipy", "jinja2",
    ):
        distribution = importlib.metadata.distribution(name)
        files = []
        for entry in distribution.files or ():
            # Copy distribution-provided legal notices, not arbitrary project files.
            if not any(part.endswith(".dist-info") for part in entry.parts):
                continue
            if not any(word in entry.name.lower() for word in ("license", "copying", "notice")):
                continue
            source = Path(distribution.locate_file(entry))
            if not source.is_file():
                continue
            relative = Path(name) / Path(*entry.parts[1:])
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            files.append(relative.as_posix())
        records.append({"name": name, "version": distribution.version, "files": files})
    (destination / "index.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    run(sys.executable, str(ROOT / "scripts" / "check_repository_examples.py"))
    run(sys.executable, str(ROOT / "scripts" / "package_repository_scene.py"))
    lite_content = BUILD / "lite-content"
    shutil.copytree(ROOT / "content", lite_content, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "exports", ".data-refresh-*", ".data-previous"))
    # A fresh path avoids a previous browser-saved notebook taking precedence.
    # It leaves the reader's older files and edits in their existing browser store.
    shutil.copy2(ROOT / "content" / SOURCE_NOTEBOOK, lite_content / RELEASE_NOTEBOOK)
    run(sys.executable, "-m", "jupyter", "lite", "build", "--contents", str(lite_content), "--output-dir", str(SITE))
    book_command = str(Path(sys.executable).parent / ("jupyter-book.exe" if os.name == "nt" else "jupyter-book"))
    run(book_command, "build", str(ROOT), "--all", "--warningiserror", "--keep-going")
    shutil.copytree(BUILD / "html", SITE / "book", dirs_exist_ok=True)
    shutil.copytree(ROOT / "static", SITE, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("*.template.html"))
    shutil.copytree(ROOT / "assets", SITE / "assets", dirs_exist_ok=True)
    (SITE / ".nojekyll").touch()
    export_license_files()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    (SITE / "build-info.json").write_text(
        json.dumps({"revision": revision, "notebook": RELEASE_NOTEBOOK}, indent=2) + "\n",
        encoding="utf-8",
    )
    run(sys.executable, str(ROOT / "scripts" / "check_site.py"))


if __name__ == "__main__":
    main()
