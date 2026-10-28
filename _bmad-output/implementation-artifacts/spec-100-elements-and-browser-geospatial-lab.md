---
title: '100-method open-data course and browser geospatial lab'
type: 'feature'
created: '2026-10-28'
status: 'draft'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/docs/expansion/README.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The synthetic sampler lacks substantial open-data examples for all
100 framework methods and the requested GIS/storytelling/GeoAI experience.

**Approach:** Implement the 100-row coverage matrix in six independently runnable
family notebooks, plus a separate `/geospatial/` area in this repository. Use the
presentation, PHI cases, and related repositories as cited context. Restore eight
missing methods; preserve the sampler and expand its eight extras in an appendix
(100 framework lessons plus eight additional lessons).

## Boundaries & Constraints

**Always:** Follow `docs/expansion/100-element-coverage.json`, its source register,
and learning design. Each method needs visible code, evidence, interpretation,
comparison, activity, limitation, and citation. Bundle dated extracts with the
documented provenance contract; distinguish observations, estimates, and scenarios.
Include accessible alternatives, videos with summaries, and critical discussion
of democratization/AI/spatial ethics. Keep project licensing undecided and retain
third-party terms. Preserve working routes, startup configuration, jinja2 support,
and browser-saved work. Commit/push the verified result as previously authorized.

**Never:** Republish the removed poster/unlicensed assets; fabricate observations,
hide assumptions, expose credentials, require paid services, silently upload data,
or claim native RustGIS/GeoAI runs in Pyodide. Avoid unnecessary runtime migrations.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Behavior | Error Handling |
| --- | --- | --- | --- |
| Fresh kernel | Any family | Own setup, local evidence | Actionable dependency error |
| Invalid data | Nulls, flags, duplicate keys | Visible gaps, validated joins | Reject invalid schema; no false zeros |
| Refresh failure | Source unavailable | Preserve validated snapshot | Explicit failure; no fabricated fallback |
| GPU/network absent | Scene/hosted GIS | 2D/table/download alternative | Capability/resource message |
| Scenario changes | Rules/weights/durations | Recomputed labeled assumptions | Validate ranges and units |

</frozen-after-approval>

## Code Map

- `content/periodic_table_visualization_methods_python_examples_jupyterlite_REVISED.ipynb`:
  retain sampler and explicit section-3 `import jinja2`.
- `scripts/build_site.py`, `scripts/check_site.py`: extend assembly/checks;
  preserve release aliases and ancestor config-script regression checks.
- `static/index.html`, `assets/`: retain splash and required startup marker.
  `_toc.yml`, `_config.yml`: extend the existing Book 1 build.
- `docs/expansion/`: matrix, provenance contract, learning design, pinned source
  and runtime reviews; implement these boundaries.

## Tasks & Acceptance

**Execution:**
- [ ] `content/data/`, `scripts/refresh_data.py`: acquire/validate registered
  snapshots and manifest; core data <=25 MB, optional imagery/models separate.
  Unverified historical assets remain linked; verified sources supply lessons.
- [ ] `content/01_start_here.ipynb`, `content/elements/`, `content/viz_helpers.py`:
  implement six family notebooks and every matrix row with stable anchors;
  helpers handle loading/style, not hidden method substitution.
- [ ] `content/geospatial/`, `static/geospatial/`: implement 2D/3D maps, USGS
  depth/cross-sections, deck.gl controls, accessible storymap, working GeoLibre/
  RustGIS projects, and optional PyScript. Provide native GeoAI reproduction and
  labeled precomputed outputs; optional local ONNX requires separate validation.
- [ ] `intro.md`, `_toc.yml`, `content/democratization.md`, `references.md`:
  connect lessons, videos, cases, and critical AI/GeoAI discussion.
- [ ] `README.md`, `THIRD_PARTY_NOTICES.md`, `CITATION.cff`: publish navigation,
  splash, full citations/attribution, and the pending-license decision.
- [ ] Build/check scripts, `.github/workflows/`, tests: package assets/notices;
  validate coverage, data contracts, scenario math, and matrix edge cases.
  Run fresh Pyodide/browser checks; verify pushed deployment.

**Acceptance Criteria:**
- Given the inventory, when checked, then all 100 methods have substantial runnable
  examples and every legacy example remains reachable.
- Given a clean checkout, when built, then Book/Lab share error-free lessons and
  README/splash/GIS/story routes resolve with complete citations.
- Given any example, when explored, then evidence/assumptions are traceable and
  its comparison, activity, and limitations are usable.
- Given the GIS area, when exercised, then scenes, project round-trips, story,
  downloads, and fallbacks have browser evidence; runtime/AI boundaries are explicit.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

Supersedes the earlier unapproved course draft. No unresolved intent questions;
large cross-file footprint, data contract, static-scene interfaces. Publication
triggers are previously authorized external effects. Core data/scenes remain
local to limit external GIS/service availability risks.

## Verification

- Validate coverage/crosswalk, snapshot hashes, schemas, joins, and scenario math.
- `python scripts/build_site.py`: clean Book/Lite build and site checks; repeat in CI.
- Execute each family independently in pinned Pyodide and desktop Python.
- Check deployed startup, keyboard/mobile, scenes, CORS/Range guards, project
  round-trips, and fallbacks; distinguish performed and blocked checks.
