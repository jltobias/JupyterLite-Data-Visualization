---
title: 'Fix companion notebooks under JupyterLite JSON transport'
type: 'bugfix'
created: '2026-10-28'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="user requested repair of the failing companion notebooks">

## Intent

The first cell of all companion notebooks rejects valid JSON exposed by
JupyterLite's Contents/DriveFS transport. The reported failure is
`Snapshot checksum mismatch: nasa/provenance.json`. Installed 0.7.6/0.7.2 code
parses JSON into an object and serializes it again; the previous NODEFS test
preserved original bytes and missed this supported delivery path.

Accept provably equivalent JSON serialization using an additional deterministic
semantic fingerprint while retaining original raw artifact hashes and rejection
of changed data. Preserve original snapshots, scientific examples, licensing and
browser-saved edits. Execute every notebook against the real JSON parse/stringify
delivery transformation in isolated Pyodide filesystems, retain desktop and site
checks, and publish the verified correction under existing commit/push authority.
Provide a fresh release entry when needed to avoid old browser-saved helpers.

</frozen-after-approval>

## Implementation Notes

- The working tree was clean at investigation; no intent gaps or destructive
  actions are needed. This is a targeted shared-validator and test-fixture fix.

- Confirmed from installed JupyterLite 0.7.6 / kernel 0.7.2 source maps:
  contents/drive.js parses JSON; drivecontents.js JSON.stringify serializes it;
  drivefs.js TextEncoder exposes those new bytes. NASA provenance changes from
  1541 to 1363 bytes, with unchanged values. Six data files change byte spelling;
  WorldPop includes 27 numeric spelling changes such as 3.0 to 3.
- Added typed, exact-decimal JSON value fingerprints alongside unchanged raw
  SHA-256/length fields. Objects ignore key order; array order, scalar types and
  exact numbers remain checked. Non-JSON byte validation remains strict.
- New runtime test uses empty MEMFS, actual JS parse/stringify delivery, and
  alternate content-root/notebook-directory launches of the corrected v2 release;
  it no longer mounts original files through NODEFS. The atlas passed this path.
- Original input files are unchanged. Only the manifest gains transport hashes.
  All nine startup cells reload the helper; a fresh release directory avoids
  saved older copies without deleting user work.

## Review Triage Log

| Finding | Verdict | Evidence and correction |
| --- | --- | --- |
| Story launch still uses old folder | medium | Confirmed template href; changed it to repository_examples_v2 and regenerate during build. |
| Index directions still name old folder | low | Confirmed run/save paragraph; corrected release directions and preserved-copy explanation. |
| Content-root startup can find old helper first | medium | Confirmed candidate order; prefer v2 and test root launches with only v2 present. |
| Unsupported browser numbers can enter refreshed metadata | medium | Decimal fingerprints detect later value loss, but staging must reject it earlier; added exact binary64-roundtrip eligibility checks and a scratch-refresh unsafe-integer regression. |
| Merged release staging can retain excluded artifacts | medium | Confirmed dirs_exist_ok merge; recreate only the verified generated release directory and check both published copies for excluded artifacts. |

- Final verification passed: all nine unchanged scientific examples executed in
  separate Pyodide 0.29.3 / actual piplite 0.7.2 processes, with seven JSON
  representations changed in each isolated filesystem (six inputs plus manifest).
  Every lesson rendered three PNG figures. Alternate launches exercised v2-only
  content-root discovery and direct notebook-directory startup.
- Fresh complete Book/Lite build and all site checks passed, including the new
  release copies, helper, manifest, original raw file hashes and exclusion checks.
  JSON semantic unit tests, corruption rejection, precision/duplicate-key cases,
  malformed-refresh/rollback checks all passed. No review findings were deferred.
- Browser UI access remains unavailable. Verification specifically reproduces
  the installed Contents/DriveFS serialization responsible for the user's trace;
  it does not claim an interactive browser smoke test.
