# ASTR 320 Course Materials Review Report

Status: Approved for review release. Not yet approved for instructional use.

## Review Scope

Reviewed against the quality floor established by `materials/ASTR101/review-report.md`, `materials/ASTR230/review-report.md`, and `materials/ASTR310/review-report.md` (read in full before drafting, per the course-package-orchestrator skill). As an upper-division (300-level) course, ASTR 320 was required to substantially exceed ASTR101/120/210/230's quantitative rigor with real derivations, matching the ASTR310 precedent. Inspected: `syllabus.html`, `schedule.html`, `course-manifest.json`, all 14 lecture slide decks and lecture notes, all 7 labs, all 7 problem sets with solution keys and assessment instructions, `reference-log.md`, `data/README.md`, `src/generate_astr320_content.py`, and `src/generate_astr320_labs_psets.py`.

## Artifact Completeness and Dependency Order

- Syllabus and schedule exist before all lecture/lab/problem-set artifacts and are internally consistent (14 lectures, 7 labs, 7 problem sets, matched 1:1 biweekly cadence documented explicitly in `syllabus.html`'s "Lecture, Lab, and Problem-Set Cadence" section, including an explicit note on how the six thematic units of variable length (2-3 lectures) still map onto a strict two-lecture lab/problem-set grid).
- Every lecture slide deck has a paired lecture-notes file; every lab has concrete apparatus/data, procedure, uncertainty treatment, deliverables, and assessment criteria; every problem set has a paired solution key and assessment-instructions file.
- `course-manifest.json` counts (14/14/7/7/7/7) match the actual file counts under `lectures/`, `labs/`, and `problem-sets/`.

## Depth and Rigor Appropriate to a 300-Level Course

- Each of the 14 lecture slide decks contains 15 slides (title plus 14 content sections), matching the established structural benchmark.
- Governing equations are derived rather than merely applied where appropriate for this course level: the radiative-equilibrium/frost-line derivation (Lecture 02), the moment-of-inertia interior-structure formalism (Lecture 03), the hydrostatic scale-height derivation (Lecture 07), the Jeans-escape parameter and magnetopause pressure-balance derivations (Lectures 09-10), and the Roche-limit/tidal-heating derivations (Lectures 12-13).
- A workspace-wide search across `materials/ASTR320/` for common placeholder/meta-commentary strings ("TBD", "placeholder", "instructor-created", "to be replaced") returned no matches outside `reference-log.md`'s own description of the tri-level labeling scheme.
- Every worked numeric example is computed programmatically in `src/generate_astr320_content.py` / `src/generate_astr320_labs_psets.py`, not hand-typed, with the same underlying real datasets (eight solar-system planets, TRAPPIST-1 system, Io/Europa/Enceladus, Titan, Uranus/Saturn rings) reused across the lecture, lab, and problem set that reference the same scenario.

## Independent Recomputation and Corrections Found

Recomputation was performed with particular attention to unit-conversion bugs, comparative-magnitude statement direction, and honest characterization of approximation-vs-reality discrepancies, per the course-materials-review skill. Three genuine defects were found and corrected during this course's production (documented in full in `reference-log.md`'s "Corrections Made During Review" section, verified here):

- **Escape-velocity comparative statement (Lecture 01):** a hand-typed bullet ("4.25 km/s to 59.5 km/s") did not match the deck's own computed Jupiter escape velocity (60.2 km/s). Fixed by drawing the bullet directly from the same computed values used in the worked-example table, eliminating the possibility of future drift.
- **Tidal-acceleration ranking (Lecture 13):** the original draft ranked Io as having the largest fractional tidal-acceleration-to-own-gravity ratio among Io/Europa/Enceladus; independent recomputation showed Enceladus's fraction (1.25%) is actually larger than Io's (0.34%), because Enceladus's own surface gravity is much weaker. Corrected to distinguish "largest fractional tidal stress relative to a moon's own weak gravity" (Enceladus) from "largest absolute tidal heating power" (Io, still correctly the largest in absolute terms), rather than conflating the two.
- **Missing reading/scope note (Lecture 05):** Lecture 05 was missing the per-lecture OpenStax citation present in every other lecture; added, consistent with adjacent lectures' section numbering.

These are exactly the class of defects the course-materials-review skill is designed to catch (backwards comparative-magnitude statements and internal-consistency drift between a worked example and a hand-typed bullet), and they were caught by genuine independent recomputation, not accepted at face value.

## Reference and Data Integrity

- The TRAPPIST-1 system (star and seven-planet parameters) was independently verified via a live web fetch of Wikipedia's "TRAPPIST-1" article (citing Agol et al. 2021, Ducrot et al. 2020, Gillon et al. 2017, Delrez et al. 2022) during this course's production; correctly labeled level 1 in `reference-log.md`.
- All other real-world datasets (solar-system planets, moons, Ceres/Vesta, moment-of-inertia factors, heat-flow values, lunar chronology, Titan, planetary magnetic fields, ring radii) are correctly labeled level 2 (standard published values, not independently re-verified this session) with an explicit per-dataset human spot-check checklist, rather than presented as unqualified primary data or mislabeled as synthetic.
- No purely synthetic (non-literature) numeric data is used anywhere in the package.
- No fabricated references, image credits, or URLs were found. All visuals are original, lecture-specific schematic SVGs.
- OpenStax Astronomy 2e chapter numbers use the published native numbering, following the ASTR230/310 offset-resolution precedent, though `reference-log.md` correctly flags that this course's specific chapter alignment was extrapolated by analogy from ASTR310's verified citations rather than independently cross-checked against embedded figure/table numbering this session -- flagged for human spot-check rather than presented as independently verified.

## Labs

- All seven labs are lecture-specific and non-formulaic, each using a distinct real dataset and distinct deliverables (Ceres/Vesta condensation evidence, Earth/Mars moment-of-inertia and heat budget, real lunar crater-chronology calibration, Titan scale height, Earth/Jupiter Jeans escape and magnetopause standoff, Uranus Roche limit, and the TRAPPIST-1e capstone tidal-heating/habitability synthesis).
- Each lab includes explicit uncertainty treatment and assessment criteria consistent with the ASTR310 benchmark.

## Final Assembly

- `index.html` created using the `materials/ASTR310/index.html` structure as a pattern; every lecture and lab link includes its real title pulled from the file's own heading (verified directly, including a duplicated-prefix bug introduced during initial generation and corrected before this review closed).
- `astronomy_curriculum.html` updated: the ASTR 320 "Course Calendar Entries" card now links to `materials/ASTR320/index.html` via a "Course materials" badge, and the "Four-Year Course List" Fall row links to the same page.

## Current Status

**Approved for review release.** This package was engineered from the outset to the ASTR230/ASTR310 depth benchmark, with real derivations appropriate to a 300-level course, real (TRAPPIST-1, level 1) and standard-published (level 2) data throughout, and three genuine defects caught and corrected by independent recomputation rather than accepted at face value. Not yet approved for instructional use pending the residual data-verification and accessibility items below.

## Outstanding Items Before Instructional Use

- **Human instructional approval:** required, as for every course package in this curriculum.
- **Catalog/dataset spot-checks:** confirm TRAPPIST-1 parameters against the primary papers directly (not just Wikipedia's synthesis), and confirm all level-2 datasets (solar-system planets, moons, Ceres/Vesta, moment-of-inertia factors, heat-flow values, lunar chronology, Titan, magnetic fields, ring radii) against the sources listed in `reference-log.md`'s spot-check checklist.
- **OpenStax spot-check:** verify exact section/page numbers against the adopted edition; this course's chapter/section citations were extrapolated by analogy from ASTR310 rather than independently cross-checked against embedded figure/table numbering this session.
- **Accessibility review:** alt text, color contrast, and accommodation alternatives have not been separately audited in this pass.
- **Policy alignment:** local academic-integrity, resubmission, and grading policy language finalized by the instructor of record.

Last updated: 2026-09-24
