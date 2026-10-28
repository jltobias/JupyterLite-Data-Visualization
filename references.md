# References and attribution

## Visualization framework

Lengler, R., and Eppler, M. J. (2007). *Towards a Periodic Table of Visualization
Methods for Management*. IASTED Conference on Graphics and Visualization in
Engineering, Clearwater, Florida, USA.
[Authors' publication page](https://www.visual-literacy.org/pages/documents.htm),
[original interactive table, version 1.5](https://www.visual-literacy.org/periodic_table/periodic_table.html),
and [research paper](https://www.visual-literacy.org/periodic_table/periodic_table.pdf).

The original table artwork is not included in this book or the distributed
notebooks. Its redistribution permission could not be verified. A citation or
link does not grant a license to reproduce that artwork. The source repository
contains the detailed review and removal record.

## Related reading

Oliveira, E. C., Oliveira, L. C., Cardoso, A., et al. (2017). *Meta-model of
information visualization based on Treemap*. Universal Access in the Information
Society, 16, 903–912. [DOI: 10.1007/s10209-016-0477-9](https://doi.org/10.1007/s10209-016-0477-9).
This reference was supplied with the original repository; it is related reading,
not the source of the periodic-table framework or of the example data.

## Data and illustrations

The original catalog and AI starter generate synthetic teaching datasets in
their code cells. Their diagram scores, targets, and relationships are
illustrative. The companion lessons below use separately attributed, packaged
observations, historical records and catalog metadata; privacy perturbations
are explicitly hypothetical.

The splash was generated for this project using OpenAI's image generation tool.
It is conceptual cover art. Its exact prompt is in
[`assets/visualization-splash.prompt.txt`](https://github.com/jltobias/JupyterLite-Data-Visualization/blob/main/assets/visualization-splash.prompt.txt).
It does not reproduce the original periodic-table poster.

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

## Software and licensing

Project licensing remains undecided. No project-wide license is granted for
the teaching text, notebooks, or splash artwork. Upstream software retains its
own terms. The [README's software attribution table](https://github.com/jltobias/JupyterLite-Data-Visualization#software-and-license-attributions)
links to the projects and their licenses; license files from the installed build
distributions are also included in the published
[software license directory](https://jltobias.github.io/JupyterLite-Data-Visualization/third-party-licenses/index.json).

Jupyter Book 1.0.4.post1 supplies the current Python-based publishing toolchain.
Version 1 is in maintenance mode; its configuration differs from Jupyter Book 2.
See the [Jupyter Book 1 documentation](https://jupyterbook.org/v1/intro.html)
and the [JupyterLite documentation](https://jupyterlite.readthedocs.io/en/stable/).
