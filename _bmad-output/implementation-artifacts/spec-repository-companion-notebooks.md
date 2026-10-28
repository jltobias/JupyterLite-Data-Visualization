---
title: 'Repository-inspired visualization companion notebooks'
type: 'feature'
created: '2026-10-28'
status: 'done'
route: 'dispatch'
baseline_commit: '798469b638434b2a44b1bf3012e4d70658e2a451'
review_loop_iteration: 0
context: ['{project-root}/docs/expansion/README.md', '{project-root}/docs/expansion/companion-source-evidence.md']
---

<frozen-after-approval reason="human-owned intent — owner explicitly requested these notebook additions after reviewing the expansion design">

## Intent

**Problem:** The committed expansion design has no executable companion lessons
that explore the owner's related repositories and PHI cases.

**Approach:** Add nine original, substantial notebooks: repository atlas,
NASA climate, NOAA sea level, historical cholera, spatial privacy, STAC discovery,
USGS earthquake scenes, CoralWatch, and geographic storytelling/GIS handoffs.
Use the inspected repositories as cited examples and verified small real-data
snapshots as evidence; connect the lessons to existing visualization methods.

## Boundaries & Constraints

**Always:** Retain existing notebooks, splash, Book/Lab routes, startup marker,
explicit jinja2 support, and user-saved files. Each new notebook runs independently
in JupyterLite and the Book, with setup, objectives, visible code, several views,
interpretation, an exercise, limitations, and citations. Package dated inputs with
checksums, queries, schemas, attribution and terms. Keep project licensing
undecided. Distinguish historical records, observational estimates, metadata,
derived distances, and hypothetical privacy perturbations. Keep data modest and
default execution independent of live APIs, tokens, or paid services.

**Never:** Copy unlicensed authored notebooks/figures, restore the removed poster,
represent metadata as pixels/population counts, invent empirical observations,
infer disease causation from a spot map, claim masking guarantees privacy, or
describe a native GIS/GeoAI package as running in Pyodide. The broader 100-method
course and full GIS workspace integrations remain separate draft work.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Behavior | Error Handling |
| --- | --- | --- | --- |
| Fresh lesson | New kernel | Own setup, local data, complete figures | Clear missing-data/dependency error |
| Invalid snapshot | Missing/modified file | Hash/schema validation | Explicit failure; no fallback observations |
| Different cwd | Book/Lab/test | Resolve helper/data consistently | Explain supported launch location |
| No GPU/network | Story scene | Static/table route remains available | Visible loading/resource failure |
| Export | Browser filesystem | Small GeoJSON/HTML/CSV artifact | No silent overwrite of source data |

</frozen-after-approval>

## Code Map

- `docs/expansion/`: pinned source/license/runtime reviews and method crosswalk.
- `content/`: existing sampler/AI notebook remain; add `repository_examples/`.
- `_toc.yml`, `intro.md`, `README.md`, `references.md`: add actual lesson routes
  and full data/repository attribution; preserve existing navigation.
- `scripts/build_site.py`: already copies content into Lite and static into dist;
  extend scene/data packaging only where required.
- `scripts/check_site.py`: preserve startup, jinja2 and poster checks; add checks
  for new Book/Lite notebooks and scene/data routes.
- `_config.yml`: retain Book 1 and error-on-execution-failure behavior.

## Tasks & Acceptance

**Execution:**
- [x] `scripts/refresh_repository_data.py`, `content/repository_examples/data/`:
  acquire fixed, bounded snapshots, retain source metadata/license notices, derive
  tidy tables transparently, and generate a manifest. Refresh is explicit and atomic.
- [x] `content/repository_examples/repo_examples.py`: portable data resolution,
  checksum validation, source cards, and shared presentation helpers only.
- [x] `content/repository_examples/01_repository_atlas.ipynb` through
  `09_storytelling_and_gis.ipynb`: implement the nine topics, substantive
  constructions, method connections, evidence tables, exercises and citations.
- [x] `static/repository-examples/`: original data-driven earthquake story with
  inspectable 2D/3D controls and a table/download alternative; provide GIS handoff
  exports with clear external-app/native-runtime boundaries.
- [x] TOC/intro/README/references/notices: expose real working entry points and
  complete attribution. Do not claim the entire 100-method expansion is finished.
- [x] Checks/tests: validate source hashes, important transformations, independent
  notebook execution, browser Python compatibility, and new published routes.
  Build the shared Book/Lite artifact. Commit/push and deployment inspection follow
  review using the owner's existing authorization.

**Acceptance Criteria:**
- Given any new notebook, when run in a fresh supported kernel, then its local
  evidence, figures, interpretation, exercise, and attribution are complete.
- Given the two repository collections, when the companion index is opened,
  then reviewed repositories have specific lesson connections and pinned source links.
- Given a clean site build, when checked, then all new Book/Lab/story links resolve
  and prior startup, notebook, legal-notice and removed-artwork regressions pass.
- Given a scene or GIS export, when inspected, then units, depth sign, coordinate
  assumptions, source, runtime, and limitations are visible and data are downloadable.

## Implementation Notes

- 2026-10-28: the owner explicitly requested implementation of new repository-example
  notebooks after the concrete expansion design was committed. This bounded spec
  records that authorization; the larger 100-method draft remains unapproved.

## Spec Change Log

## Review Triage Log

| Finding | Verdict | Evidence and disposition |
| --- | --- | --- |
| B1 | medium | Book cache hashes omit helper/data dependencies; local refresh can pair old outputs with new packaged evidence. Patch execution freshness. |
| B2 | medium | Refresh parses some responses but accepts collection bodies before semantic/license validation; malformed HTTP-200 data can replace valid evidence. Patch staging checks. |
| B3 | medium | All new notebook footers and index reference a root Markdown file absent from Lite content. Patch attribution URLs. |
| B4 | medium | Reset restores controls but leaves chapter prose and aria-pressed on the previous chapter. Patch synchronized reset. |
| B5 | medium | Inspector retains a previously picked event after filtering excludes it. Patch selection-aware inspection. |
| B6 | low | Rejected optional deck loader is cached forever, so normal transient failure cannot be retried. Directly reset failed loading state. |
| B7 | medium | Optional deck camera target/zoom is fixed despite changing display depth and viewport; source extents can be clipped. Patch internal camera fitting and test captured camera parameters. |
| B8 | medium | Per-event source links are exposed only by pointer picking; the fallback table lacks equivalent keyboard links. Add links within existing rows. |
| B9 | medium | Standalone lesson-09 provenance omits source hash, selection/count and terms link; exports lose precise traceability when separated. Complete existing metadata. |
| B10 | medium | Publishing build does not gate the already-written scene or pinned-WASM checks. Add CI verification steps. |
| B11 | low | Index links deliberately target the requested production Lab, which can surprise local-preview readers. Clarify published-Lab labeling; portable preview hosting is not claimed. |
| E1 | medium | Duplicate of B2 verified at collection downloads: malformed JSON is downloaded without parsing before replacement. Same staging-validation patch. |
| E2 | medium | Duplicate of B5 verified at update: inspected selection state is never invalidated. Same inspector patch. |
| E3 | medium | Local scene fetch/body have no timeout; a stalled resource leaves loading state indefinitely. Add bounded request failure handling with static fallback. |
| V1 | medium | Pre-verified gap: standalone scene assertions are not called by the publishing workflow. Same CI patch as B10. |
| V2 | medium | Pre-verified gap: filtered CSV check inspects filename only, not downloaded selection/values. Test the Blob bytes against selected records. |
| V3 | medium | Pre-verified gap: existing refresh test fails before either replacement rename and cannot establish rollback restoration. Test injected replacement failure in scratch data. |
| V4 | medium | Pre-verified gap: lesson-09 execution checks count/dimensions but not actual exported coordinate order/depth. Assert its emitted GeoJSON against selected source records. |

## Design Notes

No unresolved intent gaps. Independent source investigations verified actual
small datasets and separated third-party terms from undecided project licensing.
New lessons are original code/narrative; dataset reuse is separately attributed.
Footprint: nine notebooks, helper, snapshots/manifest/notices, one scene, build and
navigation checks. Previously authorized push triggers the existing Pages build.

## Verification

- Validate source schemas/hashes and test scientific invariants such as weighted
  death totals, anomaly baselines, paired coral arithmetic, and depth coordinates.
- Execute each notebook independently on desktop and pinned Pyodide.
- `python scripts/build_site.py`: shared build and all site checks pass.
- Exercise scene controls/fallbacks, inspect resulting figures/HTML, and verify
  deployed build revision; report unperformed browser checks accurately.

- 2026-10-28: implemented nine original lessons and 21 validated local input files.
  All nine passed fresh desktop and Pyodide 0.29.3 / actual piplite 0.7.2 execution,
  three rendered figures each. Parent reviewed all lesson constructions and 27
  rendered figures; reran data, scene and complete site checks successfully.
- Parent staged-blob audit verified all 21 source SHA-256 values after Git clean
  filters. Added byte-preserving/whitespace attributes for unchanged vendor data.
  README now includes all dataset/software credits and 18 pinned repository citations.
- Matrix audit: fresh kernels/cwd via independent notebook executions; missing,
  changed-byte and schema failures plus failed-refresh rollback via companion checks;
  canvas/deck/HTTP/checksum fallbacks and extreme controls via Node scene checks;
  exclusive export creation and source preservation via fresh notebook executions.
- Browser host is unavailable. JupyterLite UI/service-worker and optional deck.gl/GPU
  smoke tests remain unperformed; external GIS imports are explicitly unverified.

- Review resolution: all 18 graded findings were handled by grouped direct fixes.
  Fresh Book execution plus Sphinx --all avoids stale external dependencies; staging
  validation and scratch replacement-failure tests protect data refreshes; Lab
  attribution links and published-Lab preview labels are corrected; scene reset,
  inspection, retry, timeouts, camera fitting, source links and decoded CSV checks pass.
  Lesson 09 carries input hash/filter/count/terms and verifies serialized features.
  CI now gates upload on Node scene and pinned Pyodide checks.
- Final parent verification passed after all fixes: fresh complete Book/Lite build,
  site/data/refresh invariants and rollback tests, scene regression suite, and all
  nine fresh Pyodide 0.29.3 / piplite 0.7.2 processes with 27 PNG renders.
