# JupyterLite Data Visualization Notebook

This repository publishes a browser-runnable JupyterLite notebook demonstrating Python examples for the **Periodic Table of Visualization Methods**.

The notebook is prepared for the **Python (Pyodide)** kernel and uses Pyodide-compatible packages:

- `numpy`
- `pandas`
- `matplotlib`
- `networkx`

The notebook also includes small fallback datasets, so the examples can still run if the browser session cannot retrieve the public CSV files used by the examples.

## Notebook

The main notebook is:

```text
content/periodic_table_visualization_methods_python_examples_jupyterlite.ipynb
```

After GitHub Pages is deployed, open the JupyterLite site and launch the notebook from the file browser.

Expected Pages URL after deployment:

```text
https://jltobias.github.io/JupyterLite-Data-Visualization/
```

## Repository layout

```text
.
├── README.md
├── requirements.txt
├── .github/
│   └── workflows/
│       └── deploy.yml
└── content/
    └── periodic_table_visualization_methods_python_examples_jupyterlite.ipynb
```

## Local validation

The notebook was locally executed with a standard Python kernel to check that all cells run without errors. JupyterLite/Pyodide-specific package bootstrap code is included in the first setup cell and is skipped automatically in regular local Python.

To test locally before pushing:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install jupyter nbclient numpy pandas matplotlib networkx
python - <<'PY'
import nbformat
from nbclient import NotebookClient

path = 'content/periodic_table_visualization_methods_python_examples_jupyterlite.ipynb'
nb = nbformat.read(path, as_version=4)
NotebookClient(nb, timeout=120, kernel_name='python3', allow_errors=False).execute()
print('Notebook executed successfully.')
PY
```

## Deploy with GitHub Pages and GitHub Actions

1. Copy `README.md`, `requirements.txt`, `.github/workflows/deploy.yml`, and the `content/` folder into the root of the repository.
2. Commit and push to the `main` branch.
3. In GitHub, open **Settings > Pages**.
4. Under **Build and deployment**, set **Source** to **GitHub Actions**.
5. Open **Settings > Actions > General** and confirm workflow permissions allow **Read and write permissions**.
6. Open the **Actions** tab and run or wait for the **Deploy JupyterLite to GitHub Pages** workflow.
7. After the workflow succeeds, visit:

```text
https://jltobias.github.io/JupyterLite-Data-Visualization/
```

## Updating the notebook

1. Edit the notebook locally or in JupyterLite.
2. Save it under `content/`.
3. Commit and push to `main`.
4. GitHub Actions will rebuild and redeploy the JupyterLite site.

## Notes for Pyodide/JupyterLite

- Avoid packages that require native compiled extensions unless they are available in Pyodide or installed through a compatible JupyterLite/emscripten-forge workflow.
- This notebook intentionally uses Pyodide-friendly plotting and data-analysis packages.
- The setup cell installs or verifies runtime packages when running in JupyterLite.
- Large notebooks with many Matplotlib figures may take time to run in the browser; run individual sections if the browser becomes sluggish.
