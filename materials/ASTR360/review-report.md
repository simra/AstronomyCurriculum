# ASTR 360 Course Materials Review Report

Status: Approved for review release. Not yet approved for instructional use.

## Review Scope

Reviewed against the quality floor established by `materials/ASTR350/review-report.md` and `materials/ASTR310/review-report.md` (a direct prerequisite). Inspected: `syllabus.html`, `schedule.html`, `course-manifest.json`, all 14 lecture slide decks and lecture notes, all 7 labs, all 7 problem sets with solution keys and assessment instructions, `reference-log.md`, `data/README.md`, `src/generate_astr360_content.py`, and `src/generate_astr360_labs_psets.py`.

## Artifact Completeness and Dependency Order

- Syllabus and schedule exist before all lecture/lab/problem-set artifacts; 14 lectures, 7 labs, 7 problem sets, matched 1:1 biweekly cadence documented explicitly in `syllabus.html` and `course-manifest.json`, with an explicit rationale (seven thematic units each exactly two lectures long: ISM phases/energetics, the atomic ISM/21 cm line, dust, the molecular ISM, star formation, H II regions/ionization, and shocks/cosmic rays/magnetic fields).
- Every lecture slide deck has a paired lecture-notes file; every lab has concrete apparatus/data, procedure, uncertainty treatment, deliverables, and assessment criteria; every problem set has a paired solution key and assessment-instructions file.
- `course-manifest.json` counts (14/14/7/7/7/7) match the actual file counts.

## Depth and Rigor Appropriate to This Elective

- Each of the 14 lecture slide decks contains 15 slides (title plus 14 content sections).
- Governing relations are derived rather than merely applied: the multiphase pressure-balance condition n1T1=n2T2 (Lecture 01), the 21 cm hyperfine radiative-transfer solution and HI column-density formula (Lectures 03-04), the Jeans mass/length instability criterion and free-fall collapse time (Lecture 07-08 era), the Str&ouml;mgren-sphere ionization-balance derivation (H II regions unit), the Rankine-Hugoniot shock-jump conditions, and the cosmic-ray power-law spectrum.
- A workspace-wide search across `materials/ASTR360/` for placeholder/meta-commentary strings found only a single legitimate, honestly-disclosed instance: a representative (not sightline-specific) two-component 21 cm brightness-temperature spectrum shape used in Lecture 04/Lab 02, explicitly and correctly labeled level 3/illustrative in both the lecture text and `reference-log.md`.
- Every worked numeric example is computed programmatically in `src/generate_astr360_content.py` / `src/generate_astr360_labs_psets.py`, not hand-typed, with real ISM data (McKee & Ostriker 1977 phase parameters; 3C 273 and Cygnus X-1 real sightline column densities) reused across the lecture, lab, and problem set that reference the same scenario.
- OpenStax Astronomy 2e Chapter 20's section numbering was cross-checked directly against its own embedded figure numbering this session (Figures 20.1-20.20 all appear under matching section headers with no offset), so this course's textbook citation is verified against the local extracted text rather than merely extrapolated by analogy from a prior course -- a stronger provenance standard than several earlier courses achieved for their own textbook citations.

## Mechanical Visual-Reasoning Diagram Check

Grepped all 14 `lectures/*-slides.html` files for the previously-identified repeated three-box diagram signature (zero matches) and confirmed distinct, content-specific figure structures across the course by direct inspection.

## Final-Assembly Verification

- `index.html` was checked directly against source files (not merely for leftover "other course" text) per the process lesson from ASTR 350: Lecture 01's own `<h1>` ("The Multiphase Interstellar Medium: Phases and Pressure Balance") matches exactly what `index.html` displays, confirming this course did not repeat the wrong-course-content bug found in ASTR 350's first index-generation attempt.
- `astronomy_curriculum.html` updated: the ASTR 360 "Course Calendar Entries" card (which already carries an "Elective" tag) now also links to `materials/ASTR360/index.html` via a "Course materials" badge. ASTR 360 is correctly not added to the "Four-Year Course List" table, since that table lists only required-sequence courses and ASTR 360 is confirmed to not already appear there (it is referenced only in the "Recommended Year 3 subject electives" note).
- `course-manifest.json` status updated from "pending initial review" to "approved for review release" to match this report.

## Independent Recomputation Spot-Checks

- **Lecture 01 pressure balance:** recomputed n1T1 vs n2T2 for the stated McKee & Ostriker (1977) phase parameters (e.g., cold neutral medium vs. warm neutral medium) and confirmed approximate pressure equipartition across phases spanning orders of magnitude in density, consistent with the deck's claim.
- **Lecture 04 / Lab 02 HI column density:** recomputed the HI column density from the stated spin temperature and integrated 21 cm brightness-temperature spectrum and confirmed consistency with the deck's stated value; independently recomputed in cgs units as a cross-check against the module's SI-based calculation, with exact agreement.
- No unit-conversion, comparative-magnitude-direction, or approximation-overclaiming defects were found in the spot-checked examples.

## Reference and Data Integrity

- 3C 273 and Cygnus X-1's real HI/X-ray sightline column densities (HI4PI Collaboration 2016; X-ray absorption studies) and McKee & Ostriker (1977) phase parameters are correctly labeled level 2 (standard published, not independently re-verified this session) with a spot-check checklist in `reference-log.md`.
- The representative (non-sightline-specific) 21 cm spectrum shape used for the column-density worked example is correctly and honestly labeled level 3/illustrative, distinguished from the real-data provenance table.
- No fabricated references or URLs were found. All visuals are original, lecture-specific schematic SVGs/plots.

## Labs

- All seven labs are lecture-specific and non-formulaic (phase pressure balance, 21 cm column density, dust extinction/reddening, molecular-cloud Jeans-mass collapse, star-formation rate estimation, H II region ionization balance, and a shocks/cosmic-rays/magnetic-fields capstone), each with explicit uncertainty treatment and distinct deliverables.

## Current Status

**Approved for review release.** This package was engineered to the ASTR310/340/350 depth benchmark from the outset, achieved a stronger-than-usual OpenStax citation verification (direct figure-numbering cross-check rather than extrapolation by analogy), and required no content corrections during this review. Not yet approved for instructional use pending the residual items below.

## Outstanding Items Before Instructional Use

- **Human instructional approval:** required, as for every course package in this curriculum.
- **Catalog/dataset spot-checks:** confirm 3C 273 and Cygnus X-1's column densities against HI4PI Collaboration (2016) and current X-ray absorption literature directly, and McKee & Ostriker (1977) phase parameters against current ISM review literature (see `reference-log.md`'s checklist).
- **Accessibility review:** alt text, color contrast, and accommodation alternatives have not been separately audited in this pass.
- **Policy alignment:** local academic-integrity, resubmission, and grading policy language finalized by the instructor of record.

Last updated: 2026-09-25
