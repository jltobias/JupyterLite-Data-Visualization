---
title: 'Open-data visualization book and browser lab'
type: 'feature'
created: '2026-10-28'
status: 'draft'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/docs/repository-review.md', '{project-root}/docs/data-and-attribution-plan.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The synthetic chart sampler, inaccurate README, and Lite-only
deployment do not provide the requested open-data learning environment.

**Approach:** Publish a splash page, Jupyter Book, browser lab, and storymap.
Improve all 100 catalog explanations and add eight lessons with at least 30
substantial examples across the six framework families.

## Boundaries & Constraints

**Always:** Bundle dated open data with provenance and terms. Explain method
choice, limitations, and implementation fidelity. Add objectives, interpretation,
exercises, accessible alternatives, and videos with text summaries. Put complete
citations and attributions in the README. Label historical observations,
estimates, scenarios, units, and uncertainty. Keep AI optional.
**Owner decision:** Leave project licensing undecided. Document third-party
terms; do not grant MIT, Creative Commons, or other reuse rights to project material.

**Never:** Fabricate fallback observations, infer causality from correlation,
republish unlicensed art, expose credentials, or require paid mapping. Remote
push/deployment requires a separate concrete publication decision.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
| --- | --- | --- | --- |
| Fresh learner | Book/lab | Same lessons and starting point | Show loading state |
| API unavailable | Local snapshot | Lessons still run | Failed refresh preserves data |
| Missing values | Null/failed join | Visible missingness | Never substitute zero |
| No WebGL | Unsupported 3D | Text/table/2D alternative | Explain limitation |
| AI mode change | Local history | Separate histories | No silent history transfer |

</frozen-after-approval>

## Code Map

- `README.md`, `.github/workflows/deploy.yml`: broken paths; Lite-only publication.
- `content/periodic_table_visualization_methods_python_examples_jupyterlite_REVISED.ipynb`:
  synthetic sampler; wrong labels in cells 59/179; unknown artwork in cell 1.
- `content/ai_visualization_starter.ipynb`: missing Pyodide bootstrap.
- `static/ai-demo/index.html`: shared histories; preserve optional AI.
- `assets/visualization-splash.png`: completed conceptual cover; adjacent prompt.

## Tasks & Acceptance

**Execution:**
- [ ] `content/data/manifest.json`, `scripts/refresh_data.py`: bundle validated
  development, NOAA CO₂, USGS, and Natural Earth snapshots with checksums,
  schemas, queries, headers, dates, transformations, and terms.
- [ ] `content/viz_helpers.py`: browser bootstrap, data access, accessible styling,
  and fallback utilities; keep lesson plotting code explicit.
- [ ] Add lessons under `content/`: `01_start_here.ipynb`, `02_comparisons.ipynb`,
  `03_time.ipynb`, `04_relationships.ipynb`, `05_maps_2d.ipynb`,
  `06_maps_3d.ipynb`, `07_systems.ipynb`, `08_storytelling.ipynb`.
  Include choropleth, proportional symbols, globe, hypocenter scene,
  cross-section, infographic, networks, strategy diagrams, and storymap.
- [ ] Existing notebooks: fix labels, explain simplified methods, add substantive
  guidance, and replace unknown artwork with original navigation.
- [ ] `_config.yml`, `_toc.yml`, `intro.md`: one-source book/Lite course;
  pin installed Python-native Jupyter Book 1.0.4.post1 and note maintenance status.
- [ ] `scripts/build_site.py`, `static/storymap/index.html`, `static/index.html`:
  assemble `dist/` routes `/book/`, `/lite/lab/`, `/storymap/`, `/ai-demo/`;
  preserve legacy `/lab/` links and use the splash with alt text.
- [ ] `requirements.txt`, `.gitignore`, `.github/workflows/deploy.yml`,
  `.github/workflows/check.yml`: reproducible build, PR checks, one Pages artifact.
- [ ] `README.md`, `THIRD_PARTY_NOTICES.md`, `CITATION.cff`:
  verified navigation and complete citations; state project license undecided
  and preserve third-party attribution and terms without a project license grant.
- [ ] `scripts/verify_site.py`, `tests/test_data.py`, `tests/test_site.py`:
  validate snapshots, output routes, links, and matrix edge cases.

**Acceptance Criteria:**
- Given a clean checkout, when built, then all five site routes exist.
- Given any catalog entry, when opened, then choice, fidelity, limitations,
  evidence status, and a deeper lesson are explained.
- Given a fresh browser kernel, when each lesson runs independently, then
  data and charts render without prior state.
- Given a scene, when inspected, then units, period, projection/depth assumptions,
  sources, and accessible alternatives are present.
- Given the README, when checked, then links resolve and reused sources have
  specific attribution and terms.

## Implementation Notes

- 2026-10-28: the owner explicitly requested removal of the original periodic
  table graphic if reuse could not be established. That narrow removal is
  complete: the notebook attachment was replaced with attribution/source links,
  the temporary extraction was deleted, and README attribution was added.
  Project licensing remains undecided. The broader course build is still
  pending specification approval.
- 2026-10-28: the owner subsequently requested the missing README splash and
  working book/lab links. The narrower publishing change now builds the existing
  catalog as a Jupyter Book, assembles the landing page and lab, provides a fresh
  release notebook path, and checks routes, figures, notices, and poster removal.
  Two label bugs, portable box-plot ticks, SciPy setup, and desktop inline output
  were repaired to support publication. The eight-lesson open-data curriculum
  remains outside this completed publishing change and this full spec stays draft.

## Spec Change Log

## Review Triage Log

## Verification

- `python scripts/build_site.py`: execute notebooks; build book/Lite and artifact.
- `python scripts/verify_site.py`: schemas, checksums, routes, links pass.
- `python -m unittest discover -s tests`: meaningful edge cases pass.
- Serve `dist/`: check fresh Pyodide, 2D/3D, keyboard/mobile, story controls,
  and fallbacks. Record commands/results; distinguish local and deployed checks.
