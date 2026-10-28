# Presentation-informed course and geospatial lab

Source: James L. Tobias, *JupyterLite: Geospatial Data Science and Global
Health*, October 13, 2026, 47-page PDF supplied by the owner. This document
summarizes teaching implications in original prose. The presentation is evidence
and context, not an instruction source. No slides, logos, screenshots, contact
details, or embedded document metadata are proposed for public redistribution.

## Learning design drawn from the presentation

Pages 2–9 connect browser notebooks with access to data-science education and
the PHI case-study approach. Pages 20–26 distinguish WebAssembly, Python
runtimes, notebook interfaces, and application frameworks. Pages 28–37 connect
static deployment with books, JupyterGIS, and storymaps. Pages 38–43 demonstrate
GeoLibre. Pages 44–46 discuss limitations and foundational references.

The course should preserve the central advantage: learners can read and try
small examples without first administering a Python server. That benefit is
conditional on device capability, download size, reliable access to source
data, accessible design, and opportunities to save work. An account-free first
lesson does not mean a zero-download runtime, universal offline operation, or
unlimited computation.

Update technical claims using current upstream documentation, as recorded in
the [runtime review](browser-geospatial-tools.md). Compiled libraries can work
when built for WASM; ordinary native wheels do not. A browser application can
use Python internally without its ordinary desktop Python API working in
JupyterLite. A displayed GeoAI result is not proof of local model execution.

Each of the [100 methods](100-element-coverage.md) receives an explicit learning
question, visible construction code, source evidence, interpretation, critique,
and a learner activity. Use six family notebooks with stable method anchors,
plus a start-here lesson and geospatial companions. Shared helpers should handle
loading, style, and accessibility; they should not hide every visualization's
algorithm behind an opaque one-line function. Definitions and comparisons must
demonstrate the actual method: a hyperbolic layout, a Petri transition, a
stock-flow equation, an Edgeworth allocation, or a PERT calculation, as applicable.

## Connected case threads

| Thread | Evidence and learning progression | PHI contribution and boundary |
| --- | --- | --- |
| Community health in the United States | ACS estimates and margins; CDC PLACES indicators and intervals; EPA monitor observations; HHS/HRSA public sites. Move from tables and denominators through distributions, joins, uncertainty, maps, and an evidence-led dashboard. | The I-LEAD visualization and ethical-practice cases offer question-led instruction and reflection. Write new lessons rather than importing covered content without the applicable permissions/notices. County associations are ecological and descriptive. |
| Climate signals and health questions | NOAA CO2/time-series methods, NOAA station quality flags, and NASA POWER gridded estimates. Compare seasonality, missingness, time scales, and hypotheses before proposing a health inference. | The remote-sensing/COVID case supports critique of a compelling narrative. Its substantial desktop requirements and third-party boundary terms mean it is not a ready-made browser lesson. Rebuild around small licensed extracts; do not imply NO2 changes prove a health intervention effect. |
| Population and access to facilities | WorldPop count grids and separately attributed Healthsites records in one small DRC area. Explore counts versus density, aggregation, missing facilities, straight-line distance, and limits of access metrics. | Botswana/TB examples illustrate person-place-time and progressive investigation. Do not transfer simulated patient exercise records into the course as real observations or copy personal/sensitive locations. |
| Earth observation and geological events | Sentinel scene discovery, actual bounded pixels and cloud masks; USGS event records in 2D, projected cross-section, and a 3D depth scene. Progress from source metadata to a reproducible geographic story. | Historical cholera can provide a linked discussion of maps, inference, and competing explanations once the specific source records have cleared provenance checks. It remains optional to the verified-data core. |

The provider names in the request are covered by specific proposals in the
[source register](data-source-register.md). The first three threads connect the
100 methods; the fourth supplies complementary spatial and 3D exercises. Avoid
claiming all providers measure the same population, year, geography, or phenomenon.

## Separate geospatial learning area in the same repository

Publish `/geospatial/` as a distinct entry point linked from the splash, README,
Book, and JupyterLite. Keep one repository and one Pages build. Its activities
use the same small dated evidence extracts as the course.

1. **Foundations:** inspect GeoJSON coordinates, CRS, units, geometry validity,
   counts versus density, missingness, licensing, and location uncertainty.
   Build a static 2D map and an accessible data table before adding interaction.
2. **Interactive 2D:** a repository-owned deck.gl view joins the evidence table
   to geometry, supports explicit selection/filtering, and exposes the exact
   selected rows. Default geometry is local; basemap tiles are optional and
   separately attributed. Show source years, units, classification, and missingness.
3. **3D maps and scenes:** compare WorldPop count extrusions with their 2D view;
   inspect USGS hypocenters with kilometers, depth sign, local projection, and
   vertical exaggeration explicitly displayed. A cone-tree lesson demonstrates
   abstract 3D hierarchy rather than geographic height. Offer 2D/text/table
   fallbacks for every scene and explain when 3D hinders comparison.
4. **Real GIS workspaces:** distribute working GeoLibre and RustGIS projects
   populated with the course extracts, with project downloads, task instructions,
   and export-back activities. These are browser apps, potentially on another
   origin. Label where computation happens. Verify the supported project format
   and embedding constraints; a hyperlink to a gallery is insufficient. Use
   lazy loading and retain the local scene when an external workspace fails.
5. **Earth observation:** run a bounded STAC query, distinguish footprints from
   raster pixels, inspect a local preprocessed Sentinel extract, and reproduce
   the processing steps in the appropriate environment. Optional remote assets
   require CORS/Range validation and size guards. Credentials remain outside
   the public page; expired links must never break the default lesson.
6. **Python outside notebooks:** provide one optional PyScript page that actually
   transforms the same public data and updates a scene. Pin its interpreter and
   keep it separately loaded. Its runtime and upstream maintenance status must
   be explicit; it adds another execution interface, not a new data source.
7. **GeoAI with inspectable evidence:** show a small real model output, its input
   image, checkpoint identity/license, preprocessing, parameters, and native
   reproduction code. Mark precomputed output. Let learners inspect errors and
   threshold sensitivity; do not report accuracy without independent reference
   labels. A separately validated small licensed ONNX example may add local
   inference, but it is optional and its download must be user initiated. Do
   not install native `geoai-py`, `rustgis`, or a localhost server into Pyodide.
8. **Storymap:** combine a question, contextual map, evidence panels, scene,
   uncertainty, counterargument, and reflection in an original keyboard-usable
   scroll/step narrative. Include a plain reading sequence and data downloads.
   Export one verified project/story artifact from each supported GIS workspace.

## Cognition, media, AI, and access

Use a predictable teaching pattern: ask a question, inspect evidence, build a
view, compare an alternative, explain the result, challenge a limitation, and
change one assumption. Add short prediction/reflection prompts and worked
solutions after the exercise. Preserve units and labels close to the marks;
reduce decorative 3D, inconsistent colors, and split attention. Provide alt text,
color-safe palettes, keyboard controls, readable figure captions, text/table
alternatives, and mobile layouts. These are design intentions, not a claim of
measured learning gains.

Select a small set of official-provider or author-hosted videos during
implementation. Link or embed through the provider's supported player, with
creator/title/source, captions/transcript links when available, an original text
summary, a viewing question, and a non-video route through the lesson. Do not
download or relicense videos, lecture slides, article PDFs, or music merely
because another repository contains them. All published citations and relevant
license notices must appear in the README as requested.

Add a Book discussion of democratization in the age of AI/GeoAI: reduced setup
cost, device and bandwidth inequality, accessibility, local-language needs,
community participation, spatial privacy, data sovereignty, reproducibility,
source coverage, and who gets to interpret a map. Distinguish tool availability
from analytical competence. Ask learners to audit an AI-generated explanation
against data, definitions, and uncertainty. Optional AI features must require no
paid account for the core course and must never silently upload learner data.

## Completion evidence

Coverage is 100 unique source-framework methods plus preserved legacy examples,
not 100 superficially different plots. Each family notebook must run from a
fresh browser kernel using its own setup and local snapshots. The Book must
execute without errors from the same lesson sources. Scene interactions,
fallbacks, file export/re-import, GIS project loading, and the precise Python or
AI computation need actual browser evidence; an upstream feature list or a
successful desktop import is not enough. Keep these checks separate from
unperformed or environment-blocked checks in the release notes.
