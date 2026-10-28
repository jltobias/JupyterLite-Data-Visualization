# Repository-inspired companion lessons

Nine original lessons connect the visualization catalog to small, real evidence
snapshots and a curated inspected sample of related repositories. Each lesson
starts independently, validates its packaged inputs, constructs several views,
and includes interpretation, an exercise, limitations and source credit.

Read a lesson in the Book, or open its code in the Python (Pyodide) lab. Initial
runtime/package downloads are required in the browser; live data APIs, tokens,
paid services and GPUs are unnecessary for the default lessons.

The Lab links in this index open the published production Lab, including when
you read this page in a local preview. For a local Lab, open your preview's
`lab/index.html` and select a notebook under `repository_examples/`.

| Lesson | Evidence and visual question | Open code in Lab |
| --- | --- | --- |
| [1. Repository atlas](01_repository_atlas.ipynb) | 18 pinned source reviews; tables, matrix and bipartite connections | [Run atlas](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples/01_repository_atlas.ipynb) |
| [2. NASA climate](02_nasa_climate.ipynb) | Global annual anomaly estimates; lines, heatmaps and baselines | [Run climate](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples/02_nasa_climate.ipynb) |
| [3. NOAA sea level](03_noaa_sea_level.ipynb) | 300 monthly means at Sewells Point; season, trend and residuals | [Run sea level](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples/03_noaa_sea_level.ipynb) |
| [4. Historical cholera](04_historical_cholera.ipynb) | 250 locations / 489 recorded deaths; symbol area, weighted grids and distances | [Run cholera](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples/04_historical_cholera.ipynb) |
| [5. Spatial privacy](05_spatial_privacy.ipynb) | Hypothetical perturbations of historical points; displacement and aggregation utility | [Run privacy](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples/05_spatial_privacy.ipynb) |
| [6. STAC discovery](06_stac_discovery.ipynb) | Eight Sentinel Items and one WorldPop DUG item; metadata, footprints and terms | [Run STAC](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples/06_stac_discovery.ipynb) |
| [7. USGS earthquake scenes](07_usgs_earthquake_scenes.ipynb) | 78 January 2024 Japan events; time, map, depth and 3D coordinates | [Run earthquakes](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples/07_usgs_earthquake_scenes.ipynb) |
| [8. CoralWatch](08_coralwatch.ipynb) | Twenty real colonies in one survey; paired scores and descriptive groups | [Run CoralWatch](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples/08_coralwatch.ipynb) |
| [9. Storytelling and GIS](09_storytelling_and_gis.ipynb) | Original earthquake story panels; GeoJSON, CSV, HTML and provenance exports | [Run story/GIS](https://jltobias.github.io/JupyterLite-Data-Visualization/lab/index.html?path=repository_examples/09_storytelling_and_gis.ipynb) |

The original [interactive earthquake story](https://jltobias.github.io/JupyterLite-Data-Visualization/repository-examples/)
provides inspectable 2D/3D controls, a table, downloads, and explicit depth/CRS
assumptions. Its default canvas route uses no WebGL or remote map tiles; the
optional deck.gl view reports resource/GPU failures and retains the fallback.

## Keep the evidence types distinct

Climate and relative water level are observational estimates. Cholera records
are a historical digitization with incomplete lineage. Pump distances are
derived geometric quantities. Privacy displacement is a hypothetical scenario.
STAC footprints, dates, cloud attributes and asset references are metadata,
not sampled imagery or population counts. CoralWatch scores are paired chart
indices in one opportunistic survey. Earthquake records are a bounded, revisable
catalog, not predictions. Each lesson explains what those distinctions permit.

The atlas links every reviewed repository to a specific teaching question at its
inspected commit. It is a curated sample, not a live ranking. Full source,
query, schema, checksum, transformation and terms records are in the
[downloadable manifest](https://jltobias.github.io/JupyterLite-Data-Visualization/files/repository_examples/data/manifest.json)
and [dataset notices](https://jltobias.github.io/JupyterLite-Data-Visualization/files/repository_examples/data/NOTICES.md).
GPL-3.0 cholera terms and CC BY 4.0 survey/WorldPop terms remain separate from the
undecided project license; Sentinel retains its collection license label and
Copernicus notice. No unlicensed authored notebooks or figures were copied.

## Run and save

In Lab, open `repository_examples/`, select the Python (Pyodide) kernel and run
from the first cell. On desktop, keep each notebook alongside `repo_examples.py`
and `data/`; launching from the repository or content root is also supported.
Missing or altered snapshots fail clearly instead of substituting observations.
Keep `data/` unchanged. Lesson 9 writes new artifacts under `exports/` and supplies
direct download links. Download your notebooks and exports to persist them
outside browser storage. Existing browser-saved files are retained.

Native RustGIS, GeoAI, QGIS, GDAL, hosted viewers and JupyterGIS workspaces are
external continuation routes with their own runtime and provider requirements.
The broader 100-method expansion and full GIS integrations remain separate draft
work. See [references and attribution](https://jltobias.github.io/JupyterLite-Data-Visualization/book/references.html).
