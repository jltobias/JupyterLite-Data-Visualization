# Periodic table graphic: reuse evidence

Review date: 2026-10-28. Scope: identify the graphic already embedded in this
repository and establish whether there is evidence permitting its republication
in the proposed public GitHub repository, Jupyter Book, and JupyterLite lab.
This is a permissions-evidence review, not a definitive legal determination.

## Repository evidence

- Before removal, the only embedded graphic in
  `content/periodic_table_visualization_methods_python_examples_jupyterlite_REVISED.ipynb`
  is in zero-based cell 1, referenced as
  `attachment:27260795-c852-4eb0-818a-c7a6e4cbfe94.png`.
- It is a 1630 × 1272 PNG screenshot of the original interactive table. The
  browser address bar identifies
  `visual-literacy.org/periodic_table/periodic_table.html`.
- The screenshot visibly says version 1.5 and retains the copyright line
  naming Ralph Lengler and Martin J. Eppler and the visual-literacy.org URL.
  It is not a new illustration created by the repository maintainer.
- Decoded PNG SHA-256:
  `689c3f7c25eadff15c030ba2f32ac952f29285c4ec607206882ff120f688ac89`.
- The original cell's alt text was `image.png`; there was no adjacent attribution,
  license statement, permission reference, or accessible table description.
- The original README linked to the source table but did not document permission
  or provide the foundational authors' citation. The current README now includes
  that citation and explains the screenshot removal.
- The original tracked repository has no license file or third-party notices.
  On 2026-10-28, the owner chose to leave project licensing undecided.
- A temporary local extraction was inspected visually. It is not a new course
  asset and should not be added as another published copy.

## Primary publisher sources checked

1. [Original interactive table](https://www.visual-literacy.org/periodic_table/periodic_table.html).
   Identifies the source visible in the screenshot. The extracted page content
   is largely image-based; a text search alone cannot establish rights.
2. [Authors' books and maps page](https://www.visual-literacy.org/pages/documents.htm).
   Provides the Lengler–Eppler 2007 paper citation and a separate version 1.5
   poster download. Describes access to the interactive material; no explicit
   republication license was identified in the reviewed content.
3. [Version 1.5 poster PDF](https://www.visual-literacy.org/periodic_table/periodic_table_as_pdf.pdf).
   This is the poster download linked by the authors. It is distinct from
   `periodic_table.pdf`, which is the six-page research paper. No explicit
   reuse grant has been identified in this review. Image-only PDF text extraction
   cannot by itself demonstrate the absence of terms.
4. [Research paper](https://www.visual-literacy.org/periodic_table/periodic_table.pdf).
   Documents the framework and authors. It is not a license for the poster,
   screenshot, or all hover examples. Searches of extracted paper text did not
   identify a license or permission grant.
5. [Current publisher home](https://www.visual-literacy.org/),
   [about](https://www.visual-literacy.org/about-us/), and
   [contact](https://www.visual-literacy.org/contact-us/) pages;
   [legacy project description](https://www.visual-literacy.org/pages/project_description.htm)
   and [legacy contact page](https://www.visual-literacy.org/pages/contacts.htm).
   These identify the project and a route to request permission. The legacy
   contact page identifies Martin Eppler and publishes a contact email. It does
   not establish that one contact can authorize every third-party example.

The review found **no affirmative public license or written permission covering
this repository's reproduction**. This means permission is unverified; it does
not mean that the authors refused permission or that none could exist elsewhere.
Third-party reposts, a free download, a non-profit website, a funding credit,
and another publication's license are not evidence of a grant for this image.

## Rights questions for the planned publication

- Reproduction in a publicly downloadable repository and notebooks.
- Display in the book and lab and redistribution through forks, archives,
  and any downloadable course exports.
- Any resizing, cropping, annotations, translation, or interactive adaptation.
- Exact required credit, copyright line, source link, and any usage restrictions.
- Whether the person granting permission controls the relevant rights in the
  table artwork; hover examples require their own rights assessment if copied.

The course will provide scholarly attribution and retain the notices and credits
required by any applicable reuse basis. Attribution alone does not document
permission. An independently written learning navigator can cite the
framework without copying the poster's artwork or distinctive arrangement.
Simply tracing, recoloring, or relabeling the poster is not an independent design.

## Relevant general guidance

The [U.S. Copyright Office FAQ](https://www.copyright.gov/help/faq/faq-fairuse.html)
describes contacting the copyright owner and explains that fair use depends on
the circumstances. Its [Fair Use Index](https://www.copyright.gov/fair-use/)
expressly says that nonprofit educational uses are not automatically fair.
This review does not conclude whether this particular reproduction qualifies
for a statutory exception in any jurisdiction.

## Current disposition

**Reuse permission remains unverified; the copied graphic has been removed from
the current working tree at the owner's explicit instruction.**
The notebook's attachment and image reference were removed and replaced with
readable attribution and external links to the original table and publication
page. The temporary extracted PNG was deleted. A scan of both notebooks and
current repository assets found no other copy of the poster. The original
AI-generated splash image is a separate asset and was retained.

The existing public repository previously distributed the screenshot. Local
removal does not alter remote branches, earlier commits, forks, or already
downloaded copies. Pushing this removal updates the current branch; it does not
erase earlier commits or copies held elsewhere. No history rewrite is included.
If artwork is added later, document an applicable reuse basis first; an original
navigator can instead link to the authors' work. Continue teaching the methods
with original examples and accurate citations.
Do not represent permission as denied, attach an invented CC license, or imply
that the generated splash banner supplies rights to the original poster.

No permission request has been sent.

## Removal verification

- Compared the notebook with Git HEAD: only markdown cell 1 changed; all 101
  executable cells and notebook metadata are identical.
- Both notebook files pass nbformat schema validation. The AI starter retains
  its pre-existing missing-cell-ID warning; this removal did not modify it.
- Scanned both notebooks for attachments, image outputs, inline image payloads,
  and image references: none remain.
- Scanned current `content/`, `static/`, `assets/`, and `docs/` image/PDF files:
  only the separate original `assets/visualization-splash.png` remains.
- `git diff --check` passes. Code execution was unnecessary for this markdown
  and attachment removal; no code-execution result is claimed.

## Independent review and disposition

The BMAD adversarial review substantiated four distinct findings; no findings
were added to meet an arbitrary count. The original findings are preserved in
`periodic-table-review-findings.json`.

| Finding | Disposition in the current working tree |
| --- | --- |
| Complete screenshot distributed without documented reuse basis | Removed the screenshot attachment and temporary extracted copy; permission remains unverified. |
| Readable table provenance missing beside the image and in README | Replaced the image cell with authors, version, citation, and source links; added the citation to README. |
| Review focused on future publication and overlooked existing distribution | Recorded prior public distribution and the limits of local removal above. |
| Review overstated attribution as a universal legal condition | Distinguished course attribution policy from the actual conditions of an applicable reuse basis. |
