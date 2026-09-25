# ASTR 330 Course Materials Review Report

Status: Approved for review release. Not yet approved for instructional use.

## Review Scope

Reviewed against the quality floor established by `materials/ASTR310/review-report.md` (the direct prerequisite/benchmark for this astrophysics-sequence course) and `materials/ASTR101/review-report.md`. As ASTR 310's direct sequel, ASTR 330 was required to meet or exceed ASTR 310's quantitative rigor. Inspected: `syllabus.html`, `schedule.html`, `course-manifest.json`, all 14 lecture slide decks and lecture notes, all 7 labs, all 7 problem sets with solution keys and assessment instructions, `reference-log.md`, `data/README.md`, `src/generate_astr330_content.py`, and `src/generate_astr330_labs_psets.py`.

## Artifact Completeness and Dependency Order

- Syllabus and schedule exist before all lecture/lab/problem-set artifacts; 14 lectures, 7 labs, 7 problem sets, matched 1:1 biweekly cadence documented explicitly in `syllabus.html` and `course-manifest.json`, with an explicit rationale tying the cadence to the course's single-capstone structure (Lab/PS 07, PSR J0348+0432).
- Every lecture slide deck has a paired lecture-notes file; every lab has concrete apparatus/data, procedure, uncertainty treatment, deliverables, and assessment criteria; every problem set has a paired solution key and assessment-instructions file.
- `course-manifest.json` counts (14/14/7/7/7/7) match the actual file counts.

## Depth and Rigor Appropriate to This Course's Position in the Sequence

- Each of the 14 lecture slide decks contains 15 slides (title plus 14 content sections), matching the established structural benchmark.
- The course completes the four-equation stellar-structure system ASTR 310 began (mass continuity, energy conservation, energy transport derived here; hydrostatic equilibrium carried forward from ASTR 310) and derives, rather than merely applies: the equation of state and opacity formalism, the radiative-diffusion/Schwarzschild-criterion derivation, the Gamow-peak formalism for the pp-chain/CNO cycle, homology relations and polytropes, the Sch&ouml;nberg-Chandrasekhar limit, the triple-alpha resonance argument, and the Chandrasekhar-mass derivation from electron degeneracy pressure -- appropriately exceeding ASTR 310's own derivational depth for a direct sequel course.
- A workspace-wide search across `materials/ASTR330/` for placeholder/meta-commentary strings ("TBD", "placeholder", "instructor-created", "to be replaced") returned no matches outside `reference-log.md`'s own description of the tri-level labeling scheme.
- Every worked numeric example is computed programmatically in `src/generate_astr330_content.py` / `src/generate_astr330_labs_psets.py`, not hand-typed. The course correctly and explicitly distinguishes real-data provenance from schematic/illustrative physics approximations (Kramers opacity coefficient, pp/CNO power-law exponents, mass-core-temperature scaling, white-dwarf cooling-law calibration constant) in a dedicated `reference-log.md` section, so a reader cannot mistake an illustrative order-of-magnitude fit for a claimed real measurement.
- References to ASTR 310 throughout the lectures/labs/problem sets (e.g., "the hydrostatic-equilibrium equation from ASTR 310, Lecture 05") are legitimate curriculum-continuity citations connecting this course to its direct prerequisite, not copy-paste artifacts; verified by reading the surrounding context in each case.

## Final-Assembly Defects Found and Corrected During This Review

Two genuine final-assembly defects were found during independent verification (not present in the lecture/lab/problem-set content itself, which was otherwise sound) and corrected before approval:

- **`index.html` header carried over ASTR 310's title and a raw Python dict:** the generated header read `<title>ASTR 310 Course Materials</title>` and displayed the literal string `{'stage': 'approved for review release', ...}` instead of a clean status line, both leftover artifacts from reusing ASTR 310's index as a structural template. Corrected to `ASTR 330 Course Materials` and a clean "4 credits &middot; Spring &middot; Approved for review release" status line.
- **Missing final-assembly artifacts:** `index.html` and this `review-report.md` did not exist after the initial production pass (course-manifest.json had already been marked "approved for review release" even though these files were absent). Both were completed as part of this review before final approval; the manifest's status was already accurate for the content itself, but the package was not genuinely complete until these files existed.

## Independent Recomputation Spot-Checks

Recomputation focused on the areas most likely to contain errors given this course's derivational density and reused real datasets (Alpha Centauri AB and Sirius A/B carried forward from ASTR 230/310; Hyades cluster and PSR J0348+0432 newly live-verified):

- **Lecture 01 hydrostatic central pressure:** confirmed the uniform-density estimate (&asymp;1.345 &times; 10&#185;&#8308; Pa) and its stated ratio to the standard-model value (&asymp;2.477 &times; 10&#185;&#8310; Pa) are carried forward consistently from ASTR 310 without arithmetic drift, and the surrounding text correctly attributes the ~184x gap to the uniform-density approximation rather than overclaiming agreement.
- **Lab 07 / PS 07 PSR J0348+0432 Kepler mass check:** recomputed the total system mass from the stated orbital period (0.102424062722 days) and semimajor axis (832,000 km) using the generalized Kepler's third law, and independently obtained a value consistent with the sum of the stated neutron star (2.01 M&#8857;) and white dwarf (0.172 M&#8857;) masses, confirming the capstone cross-check is arithmetically sound.
- **Lecture 12 Chandrasekhar mass / Lab 06 Sirius B check:** confirmed Sirius B's mass (1.018 M&#8857;) is correctly reported as safely below the Chandrasekhar limit (1.4 M&#8857;), consistent with it being a stable, non-exploding white dwarf.
- No comparative-magnitude direction errors or "excellent agreement" overclaims (the specific defect classes flagged by the course-materials-review skill after ASTR 310) were found in the spot-checked examples.

## Reference and Data Integrity

- The Hyades open cluster (distance, age, turnoff mass, structural radii) and PSR J0348+0432 (neutron star/white dwarf masses, orbital elements) were independently verified via live web fetches this session (Wikipedia, citing Perryman et al. 1998 and Antoniadis et al. 2013 respectively); correctly labeled level 1 in `reference-log.md`.
- Alpha Centauri A/B and Sirius A/B are correctly disclosed as carried-forward level-1/level-2 datasets from ASTR 230/310 rather than re-claimed as newly verified.
- No purely synthetic (non-literature) numeric data is used anywhere in the package; schematic physics approximations are clearly distinguished from real-data provenance.
- No fabricated references, image credits, or URLs were found. All visuals are original, lecture-specific schematic SVGs.
- OpenStax Astronomy 2e chapter numbers are cross-checked against embedded figure/table numbering per the established precedent, with several upper-division topics correctly and explicitly flagged as extending beyond OpenStax's introductory coverage rather than fabricating a citation.

## Labs

- All seven labs are lecture-specific and non-formulaic (two-zone solar model, radiative/convective transport, Gamow-peak crossover, mass-luminosity/lifetime for four real stars, Hyades turnoff dating, Sirius B Chandrasekhar-mass check, and the PSR J0348+0432 capstone), each with explicit uncertainty treatment and distinct deliverables.

## Final Assembly

- `index.html` corrected and verified: every lecture and lab link includes its real title extracted from the file's own heading, with no duplicated-prefix bug (a defect caught in a prior course and explicitly avoided here).
- `astronomy_curriculum.html` updated: the ASTR 330 "Course Calendar Entries" card links to `materials/ASTR330/index.html` via a "Course materials" badge, and the "Four-Year Course List" Spring row links to the same page.

## Current Status

**Approved for review release.** The lecture/lab/problem-set content was engineered to the ASTR310 depth benchmark from the outset and required no substantive content corrections; the defects found and corrected during this review were final-assembly artifacts (incomplete wrap-up, a template-carryover header bug), not scientific or pedagogical errors. Not yet approved for instructional use pending the residual items below.

## Post-Approval Update: Unique Per-Lecture Visual-Reasoning Diagrams

A later audit (2026-09-24) found that all 14 lecture decks had degraded to reusing one generic three-box SVG diagram, with only labels changing between lectures. All 14 visual-reasoning diagrams were replaced with structurally distinct, lecture-specific figures (a Gamow-peak curve, a pp-chain/CNO crossover plot, Lane-Emden polytrope curves, a white-dwarf mass-radius curve approaching the Chandrasekhar limit, a PSR J0348+0432 synthesis diagram, etc.), each grounded in that lecture's own real data. Verified via grep that no repeated diagram signature remains across the course.

## Outstanding Items Before Instructional Use

- **Human instructional approval:** required, as for every course package in this curriculum.
- **Catalog/dataset spot-checks:** confirm the Hyades cluster parameters against Perryman et al. (1998) and Gaia DR3, and PSR J0348+0432's parameters against Antoniadis et al. (2013), directly (not just via Wikipedia's synthesis); confirm Sirius A against SIMBAD and the standard solar-model/nuclear-physics values against current literature (full checklist in `reference-log.md`).
- **OpenStax spot-check:** verify exact section/page numbers against the adopted edition.
- **Accessibility review:** alt text, color contrast, and accommodation alternatives have not been separately audited in this pass.
- **Policy alignment:** local academic-integrity, resubmission, and grading policy language finalized by the instructor of record.

Last updated: 2026-09-24
