# JupyterLite Data Visualization

![Charts and networks connect to a globe, world map, and illustrative underground scene.](assets/visualization-splash.png)

Read the illustrated visualization catalog in a Jupyter Book, then edit and run its Python examples in JupyterLite Lab directly in your browser.

| Explore | Link |
| --- | --- |
| **Read the Jupyter Book** | [Open the book](https://jltobias.github.io/JupyterLite-Data-Visualization/book/) |
| **Run the notebook in JupyterLite Lab** | [Open the current notebook](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=visualization_methods_v2.ipynb&reset) |
| Project splash page | [Open project home](https://jltobias.github.io/JupyterLite-Data-Visualization/) |
| Optional AI discussion demo | [Open the AI demo](https://jltobias.github.io/JupyterLite-Data-Visualization/ai-demo/) |

The splash is original AI-generated conceptual artwork, created for this project. The map and underground scene are illustrations, not measured data. [Generation prompt and provenance](assets/visualization-splash.prompt.txt).

The current catalog uses synthetic teaching data and simplified diagrams. The broader open-data lessons, 2D/3D maps, scenes, and storymap are described in the [draft course specification](_bmad-output/implementation-artifacts/spec-open-data-visualization-course.md); they are not yet implemented.

Periodic Table of Visualization Methods:  https://www.visual-literacy.org/periodic_table/periodic_table.html

Framework citation: Lengler, R., and Eppler, M. J. (2007). *Towards a Periodic Table of Visualization Methods for Management*. IASTED Conference on Graphics and Visualization in Engineering, Clearwater, Florida, USA. [Authors' publication page](https://www.visual-literacy.org/pages/documents.htm).

The original table graphic is linked rather than reproduced. Its screenshot was removed from the notebook because permission to redistribute it could not be verified. See the [graphic reuse review](docs/periodic-table-reuse-evidence.md). Project licensing remains undecided; no reuse license for the authors' artwork is implied.

Citation:  Oliveira, E.C., Oliveira, L.C., Cardoso, A. et al. Meta-model of information visualization based on Treemap. Univ Access Inf Soc 16, 903–912 (2017). https://doi.org/10.1007/s10209-016-0477-9   URL:  https://doi.org/10.1007/s10209-016-0477-9

The notebook is prepared for the **Python (Pyodide)** kernel and uses Pyodide-compatible packages:

- `numpy`
- `pandas`
- `matplotlib`
- `networkx`
- `scipy` (required by the Kamada–Kawai network layout)
- `jinja2` (required by the styled table in section 3)

The current notebooks generate their teaching datasets in code; they do not fetch real-world CSVs. JupyterLite downloads its Python runtime and packages as needed. The static book displays outputs generated during publication.

## Notebook

The main notebook is:

```text
content/periodic_table_visualization_methods_python_examples_jupyterlite_REVISED.ipynb
```

The lab launch link above opens `visualization_methods_v2.ipynb`, a release copy generated from this maintained source during the build. Both use the same code and contain no copy of the original periodic-table artwork.

**If you still see the old graphic:** JupyterLite gives browser-saved notebooks precedence over newer server copies. Close the old notebook tab and use [Open the current notebook](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=visualization_methods_v2.ipynb&reset). Your older files and edits remain in browser storage; download any work you want to keep. See [JupyterLite's content storage documentation](https://jupyterlite.readthedocs.io/en/stable/howto/content/files.html#server-contents-and-local-contents).

**If section 3 in an older saved copy reports that `.style` requires Jinja2:** run this once in a code cell, then rerun section 3:

```python
import piplite
await piplite.install("jinja2")
```

The current source notebook installs Jinja2 in setup. Desktop packages listed in `requirements.txt` do not automatically install into the browser kernel. This command also repairs an already-open session without deleting its saved work.

Published project home:

```text
https://jltobias.github.io/JupyterLite-Data-Visualization/
```

## Repository layout

```text
.
├── README.md
├── requirements.txt
├── _config.yml
├── _toc.yml
├── intro.md
├── references.md
├── assets/
│   └── visualization-splash.png
├── scripts/
│   ├── build_site.py
│   └── check_site.py
├── static/
│   ├── index.html
│   └── ai-demo/
├── .github/
│   └── workflows/
│       └── deploy.yml
└── content/
    └── periodic_table_visualization_methods_python_examples_jupyterlite_REVISED.ipynb
```

## Local validation

The publishing build executes the notebooks with a desktop Python kernel to prepare the book's figures. Pyodide package bootstrap is skipped in desktop Python. Desktop execution and browser execution are separate checks.

To build the complete site after installing `requirements.txt` in a virtual environment:

```bash
python -m pip install -r requirements.txt
python scripts/build_site.py
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000/`. The assembled artifact includes `book/`, `lab/`, the landing page, the optional AI page, and the splash asset. `scripts/check_site.py` verifies advertised routes, local page links, matching release content, and the absence of the removed graphic. Generated files are ignored by Git.

Jupyter Book is pinned to `1.0.4.post1` for this Python-based publishing setup. [Jupyter Book 1](https://jupyterbook.org/v1/intro.html) is in maintenance mode; Jupyter Book 2 uses a different configuration.

To test locally before pushing:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python - <<'PY'
import nbformat
from nbclient import NotebookClient

path = 'content/periodic_table_visualization_methods_python_examples_jupyterlite_REVISED.ipynb'
nb = nbformat.read(path, as_version=4)
NotebookClient(nb, timeout=120, kernel_name='python3', allow_errors=False).execute()
print('Notebook executed successfully.')
PY
```

## Deploy with GitHub Pages and GitHub Actions

1. Keep the root book configuration (`_config.yml`, `_toc.yml`), `intro.md`, `references.md`, `scripts/`, `static/`, `assets/`, and `content/` in the repository alongside `requirements.txt`.
2. Commit and push to the `main` branch.
3. In GitHub, open **Settings > Pages**.
4. Under **Build and deployment**, set **Source** to **GitHub Actions**.
5. Open **Settings > Actions > General** and confirm workflow permissions allow **Read and write permissions**.
6. Open the **Actions** tab and run or wait for the **Deploy Jupyter Book and JupyterLite to GitHub Pages** workflow.
7. After the workflow succeeds, visit:

```text
https://jltobias.github.io/JupyterLite-Data-Visualization/
```

## Updating the notebook

1. Edit the notebook locally or in JupyterLite.
2. Save it under `content/`.
3. Commit and push to `main`.
4. GitHub Actions will execute the notebooks, rebuild the book and lab, check the combined artifact, and deploy it to GitHub Pages.

## Notes for Pyodide/JupyterLite

- Avoid packages that require native compiled extensions unless they are available in Pyodide or installed through a compatible JupyterLite/emscripten-forge workflow.
- This notebook intentionally uses Pyodide-friendly plotting and data-analysis packages.
- The setup cell installs or verifies runtime packages when running in JupyterLite.
- Large notebooks with many Matplotlib figures may take time to run in the browser; run individual sections if the browser becomes sluggish.

## Software and license attributions

Project licensing remains undecided. No project-wide reuse license has been added. Third-party software retains its own terms; those licenses do not license the authors' periodic-table artwork or this project's educational material.

| Software | Purpose | Upstream license / notices |
| --- | --- | --- |
| [JupyterLite](https://github.com/jupyterlite/jupyterlite) | Browser lab and static content | [License](https://github.com/jupyterlite/jupyterlite/blob/main/LICENSE) |
| [JupyterLite Pyodide kernel](https://github.com/jupyterlite/pyodide-kernel) | Browser Python kernel | [License](https://github.com/jupyterlite/pyodide-kernel/blob/main/LICENSE) |
| [Pyodide](https://github.com/pyodide/pyodide) | Python runtime in WebAssembly | [License](https://github.com/pyodide/pyodide/blob/main/LICENSE) |
| [JupyterLab](https://github.com/jupyterlab/jupyterlab) | Lab interface | [License](https://github.com/jupyterlab/jupyterlab/blob/main/LICENSE) |
| [Jupyter Book](https://github.com/jupyter-book/jupyter-book) | Static book publishing | [Installed distribution license](https://jltobias.github.io/JupyterLite-Data-Visualization/third-party-licenses/index.json) |
| [NumPy](https://numpy.org/) | Numeric data | [License](https://github.com/numpy/numpy/blob/main/LICENSE.txt) |
| [pandas](https://pandas.pydata.org/) | Tables and transformations | [License](https://github.com/pandas-dev/pandas/blob/main/LICENSE) |
| [Matplotlib](https://matplotlib.org/) | Charts and diagrams | [License](https://matplotlib.org/stable/project/license.html) |
| [NetworkX](https://networkx.org/) | Graphs and networks | [License](https://github.com/networkx/networkx/blob/main/LICENSE.txt) |
| [SciPy](https://scipy.org/) | Network layout optimization | [License](https://github.com/scipy/scipy/blob/main/LICENSE.txt) |
| [Jinja](https://jinja.palletsprojects.com/) | Templates | [License](https://github.com/pallets/jinja/blob/main/LICENSE.txt) |
| [WebLLM](https://github.com/mlc-ai/web-llm) | Optional browser AI demo | [License](https://github.com/mlc-ai/web-llm/blob/main/LICENSE); downloaded models retain their respective terms |

The published [distribution license index](https://jltobias.github.io/JupyterLite-Data-Visualization/third-party-licenses/index.json) records installed build versions and links to the license/notice files provided by those distributions. Python packages loaded by Pyodide retain their upstream terms as well.

The framework and related-reading citations appear above and in the book's [References and attribution](https://jltobias.github.io/JupyterLite-Data-Visualization/book/references.html). The original poster is linked rather than bundled. [Graphic reuse evidence](docs/periodic-table-reuse-evidence.md) and the [future data attribution plan](docs/data-and-attribution-plan.md) distinguish current sources from proposed datasets.
