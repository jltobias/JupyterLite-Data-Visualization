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

The existing catalog uses synthetic teaching data and simplified diagrams. Nine new [repository-inspired companion lessons](content/repository_examples/index.md) use small, checksum-validated real-data snapshots with original code, several views, interpretation, exercises and full attribution. [Read the companion lessons](https://jltobias.github.io/JupyterLite-Data-Visualization/book/content/repository_examples/index.html), [run the atlas](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples_v2/01_repository_atlas.ipynb), or [inspect the earthquake story](https://jltobias.github.io/JupyterLite-Data-Visualization/repository-examples/). The broader 100-method expansion and full GIS workspace integrations remain separate draft work.

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

The original catalog/AI starter generate teaching data in code. Companion notebooks instead read packaged NASA, NOAA, historical cholera, STAC, USGS and CoralWatch snapshots; their default execution never calls live data APIs. JupyterLite downloads its Python runtime and packages as needed. The static book displays outputs generated during publication. Native GIS/GeoAI and JupyterGIS workspaces are separate external continuation routes.

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

## Companion evidence and repository attribution

The [companion index](content/repository_examples/index.md) links all nine
lessons. The [repository atlas](content/repository_examples/01_repository_atlas.ipynb)
identifies all 18 reviewed repositories, exact inspected commits, scoped rights
evidence and specific lesson connections. This is a curated inspected sample,
not a live or exhaustive ranking. Source reviews are retained in
[docs/expansion](https://github.com/jltobias/JupyterLite-Data-Visualization/tree/main/docs/expansion).
All new lesson code, narrative, charts and the earthquake story are original;
no unlicensed authored notebooks or figures were copied.

- **NASA GISTEMP v4:** GISTEMP Team (2026); Lenssen et al. (2024),
  [doi:10.1029/2023JD040179](https://doi.org/10.1029/2023JD040179).
  [NASA source/citations](https://data.giss.nasa.gov/gistemp/). Global annual
  anomalies relative to 1951–1980, 1880–2025; source retrieval 2026-10-09.
  Retained raw headers and provenance distinguish these US-government estimates
  from the upstream repository's separately licensed software/synthetic data.
- **NOAA CO-OPS:** National Ocean Service, Sewells Point station 8638610,
  monthly mean water levels 2000–2024, meters, MSL datum, GMT.
  [CO-OPS definitions](https://api.tidesandcurrents.noaa.gov/api/dev),
  [NOS credit/reuse guidance](https://oceanservice.noaa.gov/about/faq.html).
  Exact bounded query and raw response are packaged. These are local relative
  levels, not global rise, exposure observations or a flood forecast.
- **Historical cholera:** PHI-Case-Studies browser cholera commit
  `476f6dd5a8430e6eb823e79614fda1d7e12a78fb`, supplied through the
  [GeoLibre-GeoAI data bundle at dda3a4667a12](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI/tree/dda3a4667a1267b5ac4858723c46d8c0c82cb7a6/book/notebooks/data/cholera).
  The unchanged 250-location/489-death CSV, eight-pump CSV, provenance, README
  and full GPL-3.0 terms are retained together. Original digitization completeness
  is not independently verified; no population denominator or causal label exists.
- **CoralWatch (2026):** [BioCollect survey bd39e449-038f-4d45-ab6d-b56922a6f532](https://biocollect.ala.org.au/coralwatch/bioActivity/index/bd39e449-038f-4d45-ab6d-b56922a6f532),
  Abu Sawatyr, Egypt, accessed 2026-10-09, 20-observation reduced extract under
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: numeric
  scores extracted from chart codes; personal fields, exact coordinates and
  photographs omitted. Full source citation, license evidence and transformation
  metadata are retained. Paired scores are chart indices, not bleaching percent.
- **WorldPop / University of Southampton:** Bondarenko et al. (2026),
  [doi:10.5258/SOTON/WP00879](https://doi.org/10.5258/SOTON/WP00879),
  [UGA_DUG_2020 STAC Item](https://api.stac.worldpop.org/collections/UGA/items/UGA_DUG_2020).
  Collection CC BY 4.0 and item asset copyright metadata are retained. Reference
  year 2020 differs from publication year 2026. This bundle contains Degree of
  Urbanisation metadata/footprint, no population counts or sampled pixels.
- **Copernicus Sentinel / Element 84 Earth Search:** eight returned Sentinel-2
  L2A Items from a fixed Gaborone bbox/January 2024 query. Contains modified
  Copernicus Sentinel data (2024), processed by Element 84; metadata selection
  by this course. The retained collection license label is `proprietary` and links
  the [Copernicus Sentinel Data Legal Notice](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice);
  this is not a CC/MIT declaration. Only metadata is bundled, with no satellite
  pixels or invented TB attributes.
- **U.S. Geological Survey Earthquake Hazards Program:** 78 January 2024 Japan
  catalog events, magnitude ≥4.5, fixed 30–46° N / 128–148° E bounds.
  [USGS format](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php),
  [copyright and credit guidance](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits).
  USGS-authored government products are generally public domain; third-party
  content remains separate. Query, retrieval, IDs, revisions and magnitude types
  are retained. Depth km is positive down; scene z is negative depth with visible
  exaggeration. GIS handoffs retain two-dimensional WGS84 geometry and a named
  depth property rather than confusing depth with GeoJSON altitude.

The [snapshot manifest](https://jltobias.github.io/JupyterLite-Data-Visualization/files/repository_examples/data/manifest.json)
records exact queries, retrieval UTC, field schemas, row counts, SHA-256 hashes
and transformations. [Dataset notices](https://jltobias.github.io/JupyterLite-Data-Visualization/files/repository_examples/data/NOTICES.md),
the bundled GPL-3.0 and CC BY 4.0 texts, and original provider metadata stay with
the snapshots. Dataset terms do not set this project's license. Refresh is an
explicit maintainer action, not a build-time or notebook-time download.

The story has an optional [deck.gl](https://deck.gl/) 9.1.0 renderer, loaded from
a pinned jsDelivr distribution only when selected. deck.gl uses its
[MIT license](https://github.com/visgl/deck.gl/blob/v9.1.0/LICENSE). The default
original canvas view, static table and local downloads remain available without
that resource or WebGL. Native GIS/GeoAI execution and full external workspace
integrations are not represented as running in Pyodide.

### Pinned repository citations

The following repositories informed the original companion lessons. Inspection
was on 2026-10-28; links identify the exact reviewed revision. Their general
software terms do not automatically cover every dataset, figure, or linked service.

| Source repository | Inspected revision | Recorded rights evidence |
| --- | --- | --- |
| [JupyterLite-GeoLibre-GeoAI](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI/blob/dda3a4667a1267b5ac4858723c46d8c0c82cb7a6/README.md) | `dda3a4667a1267b5ac4858723c46d8c0c82cb7a6` | No repository-wide license |
| [JupyterLite-RustGIS](https://github.com/jltobias/JupyterLite-RustGIS/blob/64ee4e32222c07006ab28a634b759d985a002bda/README.md) | `64ee4e32222c07006ab28a634b759d985a002bda` | No repository-wide license |
| [JupyterGIS-StoryMap-Gaborone-TB-ABM](https://github.com/jltobias/JupyterGIS-StoryMap-Gaborone-TB-ABM/blob/a89bafaa49202382f5931645ab0100a37179bc36/README.md) | `a89bafaa49202382f5931645ab0100a37179bc36` | No repository-wide license |
| [JupyterLite-Global-Health-GIS](https://github.com/jltobias/JupyterLite-Global-Health-GIS/blob/fef5e91014837acfd09fce5731319d84439a0194/README.md) | `fef5e91014837acfd09fce5731319d84439a0194` | MIT software; separate data terms |
| [JupyterLite-Climate-and-Health](https://github.com/jltobias/JupyterLite-Climate-and-Health/blob/248f9860d189502013b36b3c4271777edafc4f7f/README.md) | `248f9860d189502013b36b3c4271777edafc4f7f` | MIT software; scoped CC BY/CC0; separate data |
| [JupyterLite-STAC-Browser](https://github.com/jltobias/JupyterLite-STAC-Browser/blob/fa623cc4ef5fc472da3c0237e6d270980f2273b1/README.md) | `fa623cc4ef5fc472da3c0237e6d270980f2273b1` | MIT original content; separate data terms |
| [JupyterLite-Sea-Level-Rise](https://github.com/jltobias/JupyterLite-Sea-Level-Rise/blob/6076bea2c8781285b204a5af0c3cd0ccc5d5ef8e/README.md) | `6076bea2c8781285b204a5af0c3cd0ccc5d5ef8e` | MIT software; scoped CC BY/CC0; separate data |
| [JupyterLite-DRC-Population-Mobility-Border-Mapping](https://github.com/jltobias/JupyterLite-DRC-Population-Mobility-Border-Mapping/blob/a73ae3ce2f071d96fe1b0a1083b468f156545aa2/README.md) | `a73ae3ce2f071d96fe1b0a1083b468f156545aa2` | README MIT assertion; no license file |
| [JupyterLite-Rewiring-Global-Health](https://github.com/jltobias/JupyterLite-Rewiring-Global-Health/blob/84bf945de91ad5ae3c8b2f67e9bd3e4781cf88b9/README.md) | `84bf945de91ad5ae3c8b2f67e9bd3e4781cf88b9` | MIT software; scoped CC BY; separate data |
| [Development guide](https://github.com/PHI-Case-Studies/Case-Study-Development-Guide/blob/58b4d4ba6b02e739f93b26a3f45c6f3dae04876b/README.md) | `58b4d4ba6b02e739f93b26a3f45c6f3dae04876b` | AGPL-3.0 file; individual case terms separate |
| [JupyterLite cholera](https://github.com/PHI-Case-Studies/Jupyterlite-1854-Cholera-Basic/blob/476f6dd5a8430e6eb823e79614fda1d7e12a78fb/README.md) | `476f6dd5a8430e6eb823e79614fda1d7e12a78fb` | GPL-3.0 file; provenance retained |
| [Cholera basic](https://github.com/PHI-Case-Studies/1854-Cholera-Outbreak-London-Basic/blob/3d02bafc779c03d3195738b3d110e43a8184cfaf/README.md) | `3d02bafc779c03d3195738b3d110e43a8184cfaf` | Apache-2.0 code; data rights not established there |
| [Nightingale](https://github.com/PHI-Case-Studies/1859-Crimean-War-Mortality/blob/cf2206a6f666f39b83d6e958ce70c2d6754c0f40/README.md) | `cf2206a6f666f39b83d6e958ce70c2d6754c0f40` | Apache-2.0 code; external assets separate |
| [MDR-TB](https://github.com/PHI-Case-Studies/2005-MDR-TB-Outbreak-Thailand/blob/6d50f558cd39b40089cd3eea1fbc19425e5191d1/README.md) | `6d50f558cd39b40089cd3eea1fbc19425e5191d1` | Apache-2.0 code; external assets separate |
| [Botswana HIV](https://github.com/PHI-Case-Studies/2019-HIV-Prevalence-Botswana/blob/a1dfa7bda19b891a2453f8763c2ef116547494a8/README.md) | `a1dfa7bda19b891a2453f8763c2ef116547494a8` | Apache-2.0 code; external assets separate |
| [COVID-19 / NO₂](https://github.com/PHI-Case-Studies/2020-COVID19-NO2-Remote-Sensing/blob/7efbfb3dc5f01bdec1a31ffe996c6574eaaf8b80/README.md) | `7efbfb3dc5f01bdec1a31ffe996c6574eaaf8b80` | Apache-2.0 code; external assets separate |
| [Geoprivacy](https://github.com/PHI-Case-Studies/2023-Ethical-Practice-Geospatial-Data-Science/blob/9cd3b73ca2a3630335cd74753e38b819871e3974/README.md) | `9cd3b73ca2a3630335cd74753e38b819871e3974` | README Apache assertion; no license file |
| [I-LEAD](https://github.com/PHI-Case-Studies/2024-I-LEAD-Visualization/blob/57cf61c19e1e59c2b7b4a9f107cb5d74c8f479b9/README.md) | `57cf61c19e1e59c2b7b4a9f107cb5d74c8f479b9` | GPL-3.0 file; data terms unverified |

The current Lab links open the corrected `repository_examples_v2/` release.
This fresh directory leaves older browser-saved notebooks and edits intact.
The maintained source remains `content/repository_examples/`. Run the setup cell
from the top in a fresh kernel when switching releases.

JupyterLite exposes JSON through its Contents/DriveFS layer, which may change
indentation, key order and numeric spelling (for example, `1.0` to `1`). Source
and published artifacts retain their exact byte hashes. Notebook validation also
checks a versioned JSON value fingerprint so equivalent serialization is accepted,
while changed values, strings, types and array order are still rejected. CSV,
license and other non-JSON files retain strict byte validation.

## Local validation

Companion evidence and independent notebook checks:

```sh
python scripts/check_repository_examples.py --execute
python scripts/build_site.py
node scripts/check_repository_scene.mjs
```

The notebook check uses nine fresh desktop kernels, exercises the three supported
launch directories, and verifies at least three rendered figures per lesson.
The build validates source/published hashes, Book/Lite routes, story downloads,
the original startup marker/Jinja2 dependency and removed-artwork regressions.
The Node scene test checks controls, depth sign, extreme views, filtered downloads
and loading/resource fallbacks with a DOM/canvas test double; it does not claim
browser/GPU rendering verification.

For the separate pinned WebAssembly Python check, install Node.js, build Lite
once to supply its actual `piplite` wheel, then run:

```sh
python scripts/prepare_repository_pyodide.py --download
node scripts/check_repository_pyodide.mjs
```

This explicit development download places hash-checked Pyodide 0.29.3 and its
package wheels in ignored `_build/` storage. Each lesson then executes unchanged
in a separate WASM process with actual piplite 0.7.2, NumPy, pandas and Matplotlib.
The isolated filesystem receives JSON through the real `JSON.parse` /
`JSON.stringify` transformation used by Contents/DriveFS, rather than a direct
mount of the original files.
It checks browser Python compatibility; JupyterLite UI/service-worker storage and
optional deck.gl/GPU rendering still require a browser inspection.

Data refresh is a separate, explicit maintainer operation:

```sh
python scripts/refresh_repository_data.py --refresh
```

It downloads bounded, fixed queries/pinned files into staging, validates them,
and replaces the data directory only after success. A provider/schema/count/hash
failure retains the current snapshot. Review the manifest, dates, terms,
scientific invariants and rendered outputs before publishing. Git attributes
preserve exact snapshot bytes across Windows and Linux. Ordinary builds and
notebooks use the committed inputs and never run this refresh.

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
