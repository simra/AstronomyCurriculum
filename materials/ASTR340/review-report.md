# ASTR 340 Course Materials Review Report

Status: Approved for review release. Not yet approved for instructional use.

## Review Scope

Reviewed against the quality floor established by `materials/ASTR330/review-report.md` and `materials/ASTR210/review-report.md` (ASTR 340's direct optics/detector prerequisite). Inspected: `syllabus.html`, `schedule.html`, `course-manifest.json`, all 14 lecture slide decks and lecture notes, all 7 labs, all 7 problem sets with solution keys and assessment instructions, `reference-log.md`, `data/README.md`, `src/generate_astr340_content.py`, and `src/generate_astr340_labs_psets.py`.

## Artifact Completeness and Dependency Order

- Syllabus and schedule exist before all lecture/lab/problem-set artifacts; 14 lectures, 7 labs, 7 problem sets, matched 1:1 biweekly cadence documented explicitly in `syllabus.html` and `course-manifest.json`, with an explicit rationale tying the cadence to the course's seven self-contained instrumentation units building toward a single capstone (Lab/PS 07, instrument proposal design).
- Every lecture slide deck has a paired lecture-notes file; every lab has concrete apparatus/data, procedure, uncertainty treatment, deliverables, and assessment criteria; every problem set has a paired solution key and assessment-instructions file.
- `course-manifest.json` counts (14/14/7/7/7/7) match the actual file counts.

## Depth and Rigor Appropriate to This 300-Level Course

- Each of the 14 lecture slide decks contains 15 slides (title plus 14 content sections), matching the established structural benchmark.
- Governing relations are derived rather than merely applied: the Rayleigh criterion (Lecture 02), the plate-scale relation and Nyquist sampling criterion (Lecture 03), CCD quantum efficiency and charge transfer (Lecture 04), the CCD signal-to-noise equation (Lecture 06), the grating equation and resolving power (Lectures 09-10), the Mar&eacute;chal approximation for Strehl ratio (Lecture 11), and radiometric error-budget combination (Lecture 13).
- A workspace-wide search across `materials/ASTR340/` for placeholder/meta-commentary strings returned no matches outside `reference-log.md`'s own description of its tri-level labeling scheme.
- Every worked numeric example is computed programmatically in `src/generate_astr340_content.py` / `src/generate_astr340_labs_psets.py`, not hand-typed, with real Keck Observatory data (and other real facility specifications) reused across the lecture, lab, and problem set that reference the same scenario.

## Mechanical Visual-Reasoning Diagram Check

Per the check added to the course-materials-review skill after the ASTR210/230/310/320/330 regression: grepped all 14 `lectures/*-slides.html` files for the previously-identified repeated three-box diagram signature (zero matches, as expected -- this course was built after the fix and does not exhibit the regression) and confirmed each lecture's SVG figure is structurally and numerically distinct (spot-checked Lectures 02, 03, 09, and 11: an Airy-pattern diffraction plot, a log-log plate-scale-vs-focal-length plot with five real telescopes, a grating-equation dispersion diagram, and a Strehl-ratio curve, respectively -- genuinely different chart types and data, not a relabeled template).

## Independent Recomputation Spot-Checks

- **Lecture 03 / Lab 02 plate scale:** recomputed Keck's plate scale from f=17.5 m (s=206265''/17500 mm = 11.79 arcsec/mm) and DECam's pixel scale from f=11.28 m, p=15 &micro;m (0.274 arcsec/pixel), both matching the deck's stated values and DECam's own published specification.
- **Lecture 09/10 / Lab 05 HIRES resolving power:** recomputed the grating-equation resolving power from the stated groove density and blaze angle and confirmed it is consistent with the stated R&asymp;67,000.
- **Lecture 13 error budget:** confirmed the quadrature-combination arithmetic for the radiometric error budget is correct and that no comparative-magnitude statement is stated backwards (checked per the ASTR310-derived reviewer requirement).

No arithmetic, unit-conversion, or comparative-magnitude-direction errors were found in the spot-checked examples.

## Reference and Data Integrity

- Keck I/II's aperture, collecting area, focal length, segment geometry, and HIRES's radial-velocity precision were independently verified via a live web fetch this session (Wikipedia "W. M. Keck Observatory", citing Vogt et al. 1994); correctly labeled level 1 in `reference-log.md`.
- HST, VLT, JWST, DECam, e2v CCD quantum-efficiency curves, Johnson-Cousins UBVRI bandpasses (Bessell 1990), Landolt standard stars (Landolt 1992), and Keck AO Strehl-ratio figures (Wizinowich et al. 2000) are correctly labeled level 2 (standard published values, not independently re-verified this session) with an explicit human spot-check checklist.
- Illustrative/representative values (system throughput, HIRES beam width, calibration-frame pixel levels, photometric error-budget terms) are explicitly and separately distinguished from the real-data provenance table, avoiding any risk of an illustrative approximation being mistaken for a claimed measurement.
- No fabricated references, image credits, or URLs were found. All visuals are original, lecture-specific schematic SVGs (Airy patterns, QE/filter-transmission curves, grating/Strehl curves).
- OpenStax Astronomy 2e is correctly and explicitly identified as covering this course's instrumentation topics only descriptively; nearly every quantitative topic here is correctly flagged as extending beyond OpenStax's introductory treatment rather than fabricating a citation.

## Labs

- All seven labs are lecture-specific and non-formulaic (diffraction-limited resolution across five real telescopes, plate-scale/Nyquist sampling, a CCD exposure-time calculator, photometric calibration with a real Landolt standard, HIRES's resolving power, AO Strehl ratios, and the capstone instrument-proposal/error-budget synthesis), each with explicit uncertainty treatment and distinct deliverables.

## Final Assembly

- `index.html` created using the established course-index pattern; every lecture and lab link includes its real title extracted from the file's own heading, with no duplicated-prefix or leftover-course-reference bugs (verified by direct inspection).
- `astronomy_curriculum.html` updated: the ASTR 340 "Course Calendar Entries" card links to `materials/ASTR340/index.html` via a "Course materials" badge, and the "Four-Year Course List" Spring row links to the same page.
- `course-manifest.json` status updated from "in review" to "approved for review release" to match this report.

## Current Status

**Approved for review release.** This package was engineered from the outset to the ASTR210/310/330 depth benchmark and to the newly required visual-diagram distinctness standard, with real Keck Observatory data as its anchor dataset and no content defects found during independent recomputation. Not yet approved for instructional use pending the residual items below.

## Outstanding Items Before Instructional Use

- **Human instructional approval:** required, as for every course package in this curriculum.
- **Catalog/dataset spot-checks:** confirm HIRES's resolving power/groove density, HST/VLT/JWST/DECam specifications, the e2v CCD QE curve, Johnson-Cousins bandpasses, the Landolt standard star, and the Keck AO Strehl-ratio figures against the primary sources listed in `reference-log.md`'s checklist.
- **OpenStax spot-check:** verify exact Chapter 6 section/page numbers against the adopted edition.
- **Accessibility review:** alt text, color contrast, and accommodation alternatives have not been separately audited in this pass.
- **Policy alignment:** local academic-integrity, resubmission, and grading policy language finalized by the instructor of record.

Last updated: 2026-09-24
