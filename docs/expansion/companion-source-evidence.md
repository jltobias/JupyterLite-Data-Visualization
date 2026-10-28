# Verified companion lesson inputs

Checked 2026-10-28 by direct source/API inspection. These supplement the pinned
repository reviews. This is the implementation input register, not a claim that
all sources below have already been bundled in this repository.

- **NASA GISTEMP:** repository `jltobias/JupyterLite-Climate-and-Health`, commit
  `248f9860d189502013b36b3c4271777edafc4f7f`, paths
  `content/data/nasa-gistemp-raw.csv`, `content/data/global-temperature.csv`,
  `content/data/provenance.json`. The raw table has Year, Jan–Dec and J-D;
  `***` means missing. The tidy table has year, anomaly_c, data_type, 146 rows
  1880–2025; units C relative to 1951–1980. Original retrieval 2026-10-09.
  [NASA source/citations](https://data.giss.nasa.gov/gistemp/): GISTEMP Team (2026),
  Lenssen et al. (2024), DOI 10.1029/2023JD040179. Retain source headers/metadata;
  do not assign the repository software license to NASA data. This is a global
  observational estimate, not local temperature or a measured health outcome.
- **CoralWatch:** same repository/commit, paths
  `content/data/coralwatch_random_survey_20.csv` and
  `content/data/coralwatch_random_survey_20.metadata.json`.
  Twenty real citizen-science observations from one opportunistic survey;
  sample_id, coral_form, lightest/darkest/average_colour_score fields. Metadata
  includes survey-specific CC BY 4.0 evidence, source citation, transformations,
  removal of coordinates/personal fields/photos, and a primary BioCollect URL:
  <https://biocollect.ala.org.au/coralwatch/bioActivity/index/bd39e449-038f-4d45-ab6d-b56922a6f532>.
  Two readings are paired on a colony; average=(light+dark)/2. Scores are chart
  indices 1–6, not percent bleaching, reef coverage, or temperature. Keep metadata
  and CC BY notice; no geographic generalization from this single small sample.
- **NOAA CO-OPS:** [fixed Sewells Point query](https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=monthly_mean&application=JupyterLiteDataVisualization&begin_date=20000101&end_date=20241231&datum=MSL&station=8638610&time_zone=gmt&units=metric&format=json).
  Verified 300 months, 2000–2024, station 8638610, 36.9428 N/-76.3286 E.
  Raw JSON ~83 KB; fields year, month, MSL, highest, lowest, inferred plus others.
  Units meters, datum MSL, time zone GMT. Preserve response/query and date.
  [Definitions](https://api.tidesandcurrents.noaa.gov/api/dev),
  [NOS reuse/credit guidance](https://oceanservice.noaa.gov/about/faq.html).
  Local relative sea level is not global rise or an inundation forecast. Use the
  Sea-Level-Rise repository as a visualization/narrative reference; its exposure
  scenarios are fictional, so do not import them as observations.
- **Historical cholera:** `jltobias/JupyterLite-GeoLibre-GeoAI`, commit
  `dda3a4667a1267b5ac4858723c46d8c0c82cb7a6`, prefix
  `book/notebooks/data/cholera/`: `cholera_deaths.csv`, `pumps.csv`, `README.md`,
  `provenance.json`, `LICENSE` (full GPL-3.0). This bundle identifies unchanged
  data from PHI cholera commit `476f6dd5a8430e6eb823e79614fda1d7e12a78fb`.
  Deaths: FID,DEATHS,LON,LAT, 250 locations/489 recorded deaths, SHA-256
  `1be1926dca480fe8c9a83b663e62758e57c7ebe6c296d6a32c5e93a50d62b40a`.
  Pumps: FID,LON,LAT,Street, 8 rows, SHA-256
  `6ad041659f2dc2abf9048aa4c08c01a9a7d181bd19684f76c74b7df7a4b4b830`.
  Retain source bytes/notices and GPL terms separately from undecided project
  licensing. Original digitization/completeness is not independently verified.
  One row is a location, not a person. No dates, population denominator, controls,
  walking network, or causal labels. Privacy perturbations are teaching scenarios
  on historical records; masking is not a privacy guarantee. New code/prose must
  be original, not copied from unlicensed notebooks.
- **WorldPop metadata:** [historical UGA_DUG_2020 item](https://api.stac.worldpop.org/collections/UGA/items/UGA_DUG_2020),
  about 6.4 KB. Collection UGA and item TIFF copyright identify CC BY 4.0;
  DOI 10.5258/SOTON/WP00879, Bondarenko et al., WorldPop/University of Southampton,
  2026. Retain actual item/license metadata. Degree-of-Urbanisation classes and
  footprints are not population counts or sampled raster pixels. The RustGIS
  teaching repository has future 2028–2030 counterparts; prefer the historical
  reference year and make product publication year distinct.
- **Sentinel/Gaborone metadata:** [bounded Earth Search query](https://earth-search.aws.element84.com/v1/search?collections=sentinel-2-l2a&bbox=25.7%2C-24.9%2C26.2%2C-24.4&datetime=2024-01-01T00%3A00%3A00Z%2F2024-01-31T23%3A59%3A59Z&limit=8),
  eight real Items, ~172 KB. Includes polygons, datetime, eo:cloud_cover, assets.
  Collection license is `proprietary` but links the
  [Copernicus Sentinel legal notice](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).
  Preserve that exact distinction and the required Copernicus/processing credit;
  do not relabel it CC/MIT. This is a returned sample, not all January scenes;
  metadata is not pixels. Use Gaborone TB story repository as a narrative reference
  without copying its unlicensed project or invented risk/incidence fields.
- **USGS earthquakes:** [fixed January 2024 Japan query](https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2024-01-01&endtime=2024-02-01&minmagnitude=4.5&minlatitude=30&maxlatitude=46&minlongitude=128&maxlongitude=148&orderby=time-asc),
  verified 78 events/~55 KB. Longitude, latitude, depth_km; UTC milliseconds,
  magnitude/type, place, event IDs and revisions. Credit USGS; preserve exact
  query/retrieval time. [USGS copyright guidance](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits)
  distinguishes USGS public-domain products from third-party content. Declare
  local projection approximation, vertical exaggeration, depth sign, selection,
  magnitude-type differences, and revisions. Event patterns are not predictions.

The repository atlas should be a clearly labeled **curated inspected sample**
using the commits in the existing two reviews, not an exhaustive or live ranking
of all repositories. Give each source a specific lesson connection and preserve
the distinction between adapting a teaching idea, copying licensed code/data,
and linking an external application.
