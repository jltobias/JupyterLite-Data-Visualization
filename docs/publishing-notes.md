# Publishing update — 2026-10-28

The README now displays the original splash and links to the book, browser lab,
project home, and optional AI demo. `scripts/build_site.py` assembles one Pages
artifact containing those destinations. The book publishes the current synthetic
teaching catalog; the larger open-data curriculum remains draft work.

The previously deployed notebook was checked directly over HTTPS after commit
`021876e`: it contained no attachments and its replacement markdown citation was
present. The deployment for that commit also reported success. JupyterLite can
give an older browser-saved notebook precedence over the server copy. The new
launch URL opens `visualization_methods_v2.ipynb`, generated from the maintained
source during the build, and resets the workspace layout. It does not erase the
reader's older notebooks or edits.

The source notebooks received the fixes needed for the rendered book: two pandas
label lookups, portable box-plot tick labels, the missing SciPy dependency,
explicit inline rendering for desktop kernels, and an independent browser
bootstrap plus cell IDs for the AI starter.

## Local validation

- Both notebooks executed without errors for the book. The catalog rendered
  98 chart/diagram figures; the AI starter rendered its bar chart.
- Jupyter Book built with warnings treated as errors. A Windows file-replacement
  issue in the generated search index required clearing that cache file before
  the successful build; source files were unaffected by that cleanup.
- Site checks passed for required routes, landing-page and AI-page local links,
  release/source notebook equality, actual chart outputs, exported distribution
  license files, and absence of the removed poster's image hash.
- The source notebook schemas and publishing-script syntax passed validation.
- Browser UI automation was unavailable in this session. No fresh-browser
  Pyodide execution or visual layout inspection is claimed.

The original poster remains excluded; the project license remains undecided.
The splash and newly rendered original example figures are separate assets.
