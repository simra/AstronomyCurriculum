# ASTR 350 Course Materials Review Report

Status: Approved for review release. Not yet approved for instructional use.

## Review Scope

Reviewed against the quality floor established by `materials/ASTR340/review-report.md` and `materials/ASTR320/review-report.md` (a direct prerequisite). Inspected: `syllabus.html`, `schedule.html`, `course-manifest.json`, all 14 lecture slide decks and lecture notes, all 7 labs, all 7 problem sets with solution keys and assessment instructions, `reference-log.md`, `data/README.md`, `src/generate_astr350_content.py`, and `src/generate_astr350_labs_psets.py`.

## Artifact Completeness and Dependency Order

- Syllabus and schedule exist before all lecture/lab/problem-set artifacts; 14 lectures, 7 labs, 7 problem sets, matched 1:1 biweekly cadence documented explicitly in `syllabus.html` and `course-manifest.json`, with an explicit rationale (seven thematic units each exactly two lectures long, giving an unambiguous strict two-lecture-per-lab grid).
- Every lecture slide deck has a paired lecture-notes file; every lab has concrete apparatus/data, procedure, uncertainty treatment, deliverables, and assessment criteria; every problem set has a paired solution key and assessment-instructions file.
- `course-manifest.json` counts (14/14/7/7/7/7) match the actual file counts.

## Depth and Rigor Appropriate to This Elective

- Each of the 14 lecture slide decks contains 15 slides (title plus 14 content sections).
- Governing relations are derived rather than merely applied: the radial-velocity semi-amplitude equation (Lecture 01), transit depth/duration (Lecture 02), the mass-radius interior-composition degeneracy (Lecture 06), transmission/emission spectroscopy (Lecture 07), the radiative-equilibrium habitable-zone boundary (Lecture 09), and the Drake equation as a structured estimation framework (Lecture 14).
- A workspace-wide search across `materials/ASTR350/` for placeholder/meta-commentary strings found only legitimate, honest disclosures (the Drake equation's unconstrained biological terms f_l, f_i, f_c, L are explicitly and repeatedly labeled "illustrative placeholders" in the lecture text and `reference-log.md`, which is the correct way to present genuinely unconstrained estimation terms, not a defect).
- Every worked numeric example is computed programmatically in `src/generate_astr350_content.py` / `src/generate_astr350_labs_psets.py`, not hand-typed, with real exoplanet systems (51 Pegasi b, HD 209458 b, TRAPPIST-1 carried forward from ASTR320) reused across the lecture, lab, and problem set that reference the same scenario.

## Final-Assembly Defect Found and Corrected During This Review

- **`index.html` initially built from the wrong course's content:** a first attempt at generating `index.html` erroneously reused ASTR 340's (Astronomical Instrumentation) lecture/lab titles and links wholesale, rather than ASTR 350's own content, despite the underlying lecture/lab HTML files being correct. This was caught by directly reading a source lecture file's own `<h1>` (confirmed "Detecting Other Worlds: The Radial-Velocity Method" for Lecture 01) and comparing it against the initially generated index, which showed ASTR 340 titles instead. The index was regenerated correctly from ASTR 350's own files and re-verified line-by-line before approval.

## Mechanical Visual-Reasoning Diagram Check

Grepped all 14 `lectures/*-slides.html` files for the previously-identified repeated three-box diagram signature (zero matches) and confirmed distinct figure structures by spot-checking Lectures 01, 04, 09, and 14 (a radial-velocity phase curve, a mass-radius scatter with composition curves, a habitable-zone radiative-equilibrium boundary plot, and a Drake-equation term-by-term bar/range chart, respectively).

## Independent Recomputation Spot-Checks

- **Lecture 01 / Lab 01 radial-velocity semi-amplitude:** recomputed the 51 Pegasi b semi-amplitude from its stated orbital period and minimum mass and confirmed consistency with the deck's stated ~59 m/s value (the real, historically significant discovery amplitude).
- **Lecture 02 / Lab 01 transit depth:** recomputed HD 209458 b's transit depth from its stated planet/star radius ratio and confirmed consistency with the deck's stated ~1.5% value.
- **Lecture 09 habitable-zone boundary:** recomputed the radiative-equilibrium inner/outer habitable-zone distances for the Sun from the stated equilibrium-temperature bounds and confirmed the derived astronomical-unit values are correctly ordered (inner < outer) and of the expected magnitude.
- No unit-conversion, comparative-magnitude-direction, or approximation-overclaiming defects were found.

## Reference and Data Integrity

- 51 Pegasi b, HD 209458 b, and TRAPPIST-1 (the latter carried forward from ASTR 320's live-verified provenance) are the course's primary real exoplanet datasets; provenance levels are correctly disclosed in `reference-log.md`.
- The Drake equation's biological terms are correctly and explicitly labeled level 3 (synthetic/illustrative placeholder) throughout, since no observational constraint exists for them -- this is the honest, correct treatment of a genuinely unconstrained estimation exercise, not an undisclosed fabrication.
- OpenStax Astronomy 2e chapter citations are extrapolated by analogy from ASTR320/330's verified citations, correctly flagged for human spot-check rather than presented as independently cross-checked this session.
- No fabricated references or URLs were found.

## Labs

- All seven labs are lecture-specific and non-formulaic (radial-velocity/transit analysis of two real systems, mass-radius demographics, TRAPPIST-1 resonances, atmospheric spectroscopy, habitable-zone boundaries, biosignature false-positive reasoning, and a Drake-equation capstone), each with explicit uncertainty treatment and distinct deliverables.

## Final Assembly

- `index.html` corrected and verified to contain only ASTR 350's own real lecture/lab/problem-set titles and links (see defect note above).
- `astronomy_curriculum.html` updated: the ASTR 350 "Course Calendar Entries" card (which already carries an "Elective" tag) now also links to `materials/ASTR350/index.html` via a "Course materials" badge. ASTR 350 is correctly not added to the "Four-Year Course List" table, since that table lists only the required-sequence courses and ASTR 350 is confirmed to not already appear there.

## Current Status

**Approved for review release.** The lecture/lab/problem-set content required no substantive corrections; the one defect found and corrected during this review was a final-assembly artifact (an index page briefly built from the wrong course's files), not a scientific or pedagogical error. Not yet approved for instructional use pending the residual items below.

## Outstanding Items Before Instructional Use

- **Human instructional approval:** required, as for every course package in this curriculum.
- **Catalog/dataset spot-checks:** confirm 51 Pegasi b and HD 209458 b's parameters against a current exoplanet archive (e.g., the NASA Exoplanet Archive) directly.
- **OpenStax spot-check:** verify exact Chapter 7/30 section/page numbers against the adopted edition.
- **Accessibility review:** alt text, color contrast, and accommodation alternatives have not been separately audited in this pass.
- **Policy alignment:** local academic-integrity, resubmission, and grading policy language finalized by the instructor of record.

Last updated: 2026-09-25
