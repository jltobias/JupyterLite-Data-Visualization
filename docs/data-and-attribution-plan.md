# Data, references, and attribution plan

Sources checked on 2026-10-28. This file records the proposed evidence and reuse
approach; no datasets have been downloaded or bundled yet. During implementation,
the README must contain the complete final citations and attribution table,
not merely a link to this planning file.

## Foundational sources

- Lengler, R., and Eppler, M. J. (2007). *Towards a Periodic Table of
  Visualization Methods for Management*. IASTED Conference on Graphics and
  Visualization in Engineering, Clearwater, Florida, USA.
  [Authors' source and paper](https://www.visual-literacy.org/pages/documents.htm),
  [original interactive table](https://www.visual-literacy.org/periodic_table/periodic_table.html),
  [university publication record](https://search.usi.ch/en/publications/1002/towards-a-periodic-table-of-visualization-methods-for-management).
  Cite the framework and link to its artwork; permission to republish the
  original poster has not been established. At the owner's instruction, the
  copied screenshot has been removed from the notebook; retain the source link
  and create an original course navigator. See the
  [reuse review](periodic-table-reuse-evidence.md).
- Oliveira, E. C., Oliveira, L. C., Cardoso, A., et al. (2017).
  *Meta-model of information visualization based on Treemap*.
  Universal Access in the Information Society, 16, 903–912.
  [DOI](https://doi.org/10.1007/s10209-016-0477-9).
  This reference is inherited from the current README. Its publisher content
  could not be retrieved during this review; verify the full record and explain
  its specific relevance before using it as a course citation. It is not the
  source of the periodic table.

## Proposed datasets

| Dataset | Source and intended use | Reuse and attribution requirements |
| --- | --- | --- |
| Historical Gapminder country indicators | [Gapminder data](https://www.gapminder.org/data/), [documentation](https://www.gapminder.org/data/documentation/); a compact historical teaching extract such as Plotly's packaged Gapminder example | Attribute Gapminder and each original indicator source identified by that release; retain the extract's specific provenance and year range. [Gapminder reuse guidance](https://www.gapminder.org/free-material/) and [FAQ](https://www.gapminder.org/about/about-gapminder/faq/) require attention to original provider terms. Never claim that a dataset mirror's software license licenses every dataset it hosts. |
| Mauna Loa monthly CO₂ | [NOAA Global Monitoring Laboratory data page](https://gml.noaa.gov/ccgg/trends/data.html), [monthly CSV](https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv) | Retain the downloaded header and its current citation and use conditions; credit NOAA/GML and Scripps as specified for the selected release. The data page names Xin Lan and Ralph Keeling. Record retrieval time, units, missing-value conventions, revisions, and station continuity notes; do not assign a blanket Creative Commons license to the data. |
| Earthquake events | [USGS catalog API](https://earthquake.usgs.gov/fdsnws/event/1/), [GeoJSON format](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) | Use a fixed historical window and documented magnitude threshold; retain event IDs, coordinate order, UTC timestamps, depth units, and agency attribution. [USGS copyright policy](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits) identifies USGS-produced data as U.S. public domain and distinguishes third-party material. Credit U.S. Geological Survey. |
| Coarse country boundaries | [Natural Earth](https://www.naturalearthdata.com/), [terms](https://www.naturalearthdata.com/about/terms-of-use/) | Public domain. Credit “Made with Natural Earth.” Pin the exact release, document geometry simplification and country joins, and show unmatched countries rather than assigning zero. Boundaries are generalized context, not authoritative legal borders. |

If indicator provenance cannot be established for the historical extract, replace
it with a documented [World Bank Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)
snapshot using release-specific [data license terms](https://datacatalog.worldbank.org/public-licenses).
Do not merge incompatible PPP bases or present historical observations as current.

Each bundled file needs an entry in `content/data/manifest.json` with the source
page, exact download URL/query, retrieval date/time, release or observation window,
SHA-256, row count, units, schema, filters, transformations, license/terms URL,
attribution text, and known limitations. Derived products must identify their
input snapshots. A separate explicit refresh script should validate schemas and
write atomically; ordinary notebook execution must use the bundled files.

## Maps, software, media, and artwork

- Use local coarse boundaries for default maps. External basemap tiles, if added,
  need provider attribution, usage-policy compliance, and a no-tiles fallback.
  Do not imply that open data eliminates a tile server's service restrictions.
- Record the exact shipped versions and retain notices for JupyterLite,
  the Pyodide kernel, Pyodide, Jupyter Book, JupyterLab, NumPy, pandas,
  Matplotlib, NetworkX, Plotly, Folium/Leaflet, and any other bundled dependency.
  Distinguish linked services from redistributed software. Inspect actual
  distribution licenses during implementation rather than guessing from names.
- Select short videos from official author, university, NOAA, USGS, or Gapminder
  pages. Link or embed only where supported by the provider. Include title,
  creator, source, transcript/captions link when available, a concise text
  alternative, and discussion prompts. Downloading or relicensing videos is
  not part of the plan. TED-hosted talks have separate usage terms.
- `assets/visualization-splash.png` is original AI-generated conceptual cover
  art created with the built-in image generation tool for this project. It is
  not a measured map, real terrain model, or quantitative earthquake scene.
  The exact prompt is preserved in `assets/visualization-splash.prompt.txt`.
  Alt text: “Visualization tiles connect charts and networks to a globe, world
  map, and an illustrative underground earthquake scene.”

The repository currently has no project license. On 2026-10-28, the owner chose
to leave project licensing undecided. Do not add MIT, Creative Commons, or
other license grants for project-authored material. The README should state
that this decision is pending while documenting and preserving each
third-party source's own attribution and reuse terms.

## Build documentation

- [JupyterLite deployment guide](https://jupyterlite.readthedocs.io/en/stable/quickstart/deploy.html)
  documents static publication and the distinction between build dependencies
  and browser runtime packages.
- [Jupyter Book 1 documentation](https://jupyterbook.org/v1/intro.html) supports
  the Python-native build already installed locally (`1.0.4.post1`). Version 1
  is in maintenance mode. Pin this explicitly if selected; [Jupyter Book 2](https://jupyterbook.org/stable/)
  uses the MyST engine and a different build configuration. Do not mix the two.
- [Plotly 3D scatter documentation](https://plotly.com/python/3d-scatter-plots/)
  supports a browser-renderable scene without a paid mapping account.
- [Leaflet reference](https://leafletjs.com/reference.html) documents accessible
  map controls and attributions. Keep scene units and projection assumptions
  visible alongside interactive views.
