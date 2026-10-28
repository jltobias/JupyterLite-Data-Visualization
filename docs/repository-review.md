# Repository review

Reviewed 2026-10-28 against commit `8e36a072e53f20ef874657982cf8dd13553a4a4c`.
This is a static review of the eight tracked files, notebook cells, deployment
configuration, and upstream documentation. Notebook execution, a fresh Pyodide
session, and a production deployment have not been verified in this review.
Both notebook files pass nbformat schema validation, with a missing-cell-ID
warning for all four cells of the AI starter. Requests for the published root,
lab, and proposed book URL could not
be retrieved through the web tool; this is not evidence that those URLs are down.

Follow-up on 2026-10-28: at the owner's instruction, the embedded screenshot of
the original periodic table was removed because redistribution permission could
not be verified. The notebook now links to the authors' table and publication,
and the README supplies the foundational citation. See
[reuse evidence and removal record](periodic-table-reuse-evidence.md).
The findings below otherwise describe the original reviewed commit.

## Findings to address first

1. **The deployment does not publish the authored website.**
   `.github/workflows/deploy.yml` builds JupyterLite from `content/`, but never
   assembles `static/index.html` or `static/ai-demo/index.html`. There is no
   Jupyter Book configuration, table of contents, build, or publication step.
   The intended landing and AI pages therefore are not supplied by this workflow.

2. **The README cannot be followed as written.**
   Its notebook path and validation command omit `_REVISED`, which is present
   in the actual filename. It describes public CSV retrieval with fallbacks;
   the notebook instead creates synthetic teaching datasets in setup cell 2.
   The published URL is described as expected after deployment, not verified live.

3. **Two expressions produce incorrect chart labels.**
   In the main notebook, cell 59 uses `row.item`, which accesses a pandas
   method; use `row["item"]`. Cell 179 uses `r.name`, which accesses the row
   index; use `r["name"]`. Cell numbers here are zero-based JSON cell indices.

4. **Several headings promise methods that the code does not implement.**
   Cell 39 draws a Cartesian tree in a circle under “Hyperbolic tree”; cell 59
   plots assigned groups under “Clustering”; cell 163 presents an unexplained
   matrix under “House of quality.” Cell 175 relabels reach/quality as different
   constructs, with a horizontal quadrant divider outside the displayed range.
   The spectrogram example in cell 25 also needs terminology reconciled with
   the original table. Implement each method faithfully or explicitly describe
   it as a simplified illustration, with its missing features explained.

5. **Attribution is incomplete and there is no project license.**
   The foundational Lengler–Eppler paper is absent from the README. A treemap
   paper appears without an explanation of its role. Cell 1 contains an embedded
   PNG with generic alt text and no credit or permission statement. Its reuse
   rights have not been established. Replace it with an original navigator and
   a link to the authors' table unless permission can be documented. Do not
   apply a new repository license to third-party artwork or data by implication.

## Teaching and accessibility

The main notebook contains 204 cells: 101 code cells, 100 method headings, a
catalog, and introductory material. No code outputs are saved. Its data are
generated examples; there are no real-data map lessons, video links, learning
checks, or source-to-chart provenance records. Most method descriptions repeat
the same construction sentence rather than teaching when and why to use them.

Build a progression from a question to data inspection, visual encoding,
interpretation, limitations, and a short exercise. Add definitions, units,
sample windows, missingness explanations, and source captions. Distinguish
observations from estimates, hypotheses, scenarios, and illustrative scores.
For example, cell 77 labels synthetic links as causes, while cell 155 turns a
synthetic baseline into a target without establishing either claim.

Use comparable views of the same evidence: a table and bar chart; a time series
and seasonal heatmap; a 2D epicenter map, a globe, and a 3D depth scene. Include
the reasons to prefer 2D when 3D occlusion makes comparison harder. Provide
text summaries and data tables, keyboard-accessible controls, clear focus,
color choices with adequate contrast, reduced-motion behavior, and a usable
layout on small screens.

The original table has six application families and additional dimensions,
including overview/detail, process/structure, and thinking modes. Treat it as
a selection framework, not a claim that this repository reproduces a canonical,
exhaustive list. Label additions and adaptations. The [authors' paper and
materials](https://www.visual-literacy.org/pages/documents.htm) establish this
context.

## Browser runtime and optional AI

The main notebook bootstraps packages with `piplite`; the four-cell AI starter
does not. Desktop packages in `requirements.txt` do not automatically install
those packages in Pyodide. Validate each notebook independently in a fresh
browser kernel, with clean storage and without having run another notebook.

The optional AI demo keeps the same message array across local and gateway
modes. After a mode switch, submitting to a gateway can include earlier local
conversation messages. Separate histories and describe the actual transfer
behavior before submission. Add explicit labels for the question and context
textareas. The gateway is a configurable integration, not a deployed or
approved agency service. Keep the visualization course usable without AI.

## Publication and verification

Build a single Pages artifact containing a landing page, book, JupyterLite,
storymap, and optional AI page. Use stable relative paths and preserve or
redirect old `/lab/` links. Add a pull-request check that builds and executes
without deploying. Restrict Pages publication to the main branch/manual
deployment job and its existing environment permissions.

Bundle small, dated real-data snapshots, a schema, retrieval query, checksum,
attribution, and transformation notes. A refresh command should validate new
data before replacing an existing snapshot. Live feeds are optional extensions;
the default lesson must not silently substitute fabricated rows.

Check notebook execution, the book build, artifact routes and local links,
browser package installation, chart rendering, map controls, WebGL failure
fallbacks, captions, and narrow-screen layouts. A desktop notebook execution
alone does not establish JupyterLite compatibility. Report production URLs as
deployment targets until the Pages deployment and those routes are verified.

## Suggested course sequence

| Lesson | Evidence and cognition goal | Principal outputs |
| --- | --- | --- |
| Start here | Ask a question; inspect provenance and missingness | Data dictionary, source audit, chart-choice navigator |
| Compare and distribute | Historical development indicators; distinguish country and person weighting | Ranked bars, histogram, box plot, dot plot, table |
| Change over time | NOAA CO₂; separate seasonality from long-term change | Lines, small multiples, heatmap, annotated infographic |
| Relationships | Development indicators; association and aggregation | Log-scale scatter, bubbles, parallel coordinates, correlation view |
| Geographic patterns | Country indicators and USGS earthquakes | Choropleth, proportional symbols, classification comparison |
| Beneath the surface | Earthquake coordinates and depths | 3D globe/map, regional depth scene, 2D cross-section |
| Explain systems | Observed earthquake reporting process; clearly marked scenarios | Network, concept map, flow, decision and strategy diagrams |
| Tell a responsible story | Combine evidence, context, and uncertainty | Guided storymap, dashboard, infographic, capstone |

Every existing catalog entry should receive a substantive explanation, appropriate
status (implemented method or simplified illustration), limitations, and a
route into a deeper lesson. The new lessons should contain at least 30 substantial
examples across the six families, with real evidence wherever the method supports
it. Concept and strategy diagrams may express explicitly labeled interpretations
or scenarios rather than pretending to be measurements.
