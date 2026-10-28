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

## Blank lab startup correction

The authored landing page initially omitted `script#jupyter-config-data`.
JupyterLite 0.7.6's `config-utils.js` reads that element from each ancestor
`index.html`, including the landing page, before injecting the lab bundle.
An HTTP 200 response therefore did not establish successful startup: the missing
element caused `Cannot read properties of null (reading 'textContent')`.

The parent-page JSON configuration element has been restored without loading
the lab on the splash page. `check_site.py` now requires valid JSON configuration
in both the landing page and lab entry page. The check failed on the old artifact
and passed after assembly with the corrected landing page.

The actual generated loader was also run in an isolated JavaScript test with
mock page/config responses: removing the tag reproduced that error; the fixed
page let configuration merge and injected the application bundle with the correct
project base URL. This checks the loader contract, not a complete browser or
Pyodide session; browser UI access remained unavailable.

## Section 3 styled-table dependency

The table uses pandas `DataFrame.style`, which needs the optional Jinja2
package. Jinja2 was listed in desktop build requirements but omitted from the
browser's `piplite.install` list. Setup now installs and imports it explicitly.
The published-notebook checker now rejects a notebook using `.style` if its
browser setup omits Jinja2; it rejected the previous artifact and passed after
the source and release copies were updated.

A separate fresh WebAssembly Python test used the exact Pyodide 0.29.3 runtime
specified by the lab's kernel settings, with Python 3.13.2 and pandas 2.3.3.
It executed the notebook's actual `programs` definition and section 3 code:

- Without Jinja2, it reproduced the reported `.style` AttributeError.
- After loading Jinja2 3.1.6 and MarkupSafe 3.0.2, the same cell rendered a
  five-row HTML table, with benefit/cost ratios sorted descending.

This test used the Python WebAssembly runtime under Node.js, not a browser UI.
Runtime files and wheels were downloaded from the official Pyodide distribution
into the ignored build folder; package wheel hashes were checked against its
manifest. The Node.js test executable came from the official distribution and
was verified against its published SHA-256. None of those test binaries are
committed or included in the published site.

For a reader's older saved notebook, installing Jinja2 once with `piplite` and
rerunning section 3 fixes the current session without clearing browser storage.
