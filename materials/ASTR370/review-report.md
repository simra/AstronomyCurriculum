# ASTR 370 Course Materials Review Report

Status: Approved for review release. Not yet approved for instructional use.

## Review Scope

Reviewed against the quality floor established by `materials/ASTR360/review-report.md` and `materials/ASTR230/review-report.md` (a direct prerequisite). Inspected: `syllabus.html`, `schedule.html`, `course-manifest.json`, all 14 lecture slide decks and lecture notes, all 7 labs, all 7 problem sets with solution keys and assessment instructions, `reference-log.md`, `data/README.md` and its two generated CSVs, `src/generate_astr370_content.py`, and `src/generate_astr370_labs_psets.py`.

## Artifact Completeness and Dependency Order

- Syllabus and schedule exist before all lecture/lab/problem-set artifacts; 14 lectures, 7 labs, 7 problem sets, matched 1:1 biweekly cadence documented explicitly in `syllabus.html` and `course-manifest.json`, with an explicit rationale (seven thematic units each exactly two lectures long: Solar Interior and Atmosphere, Solar Magnetism and Sunspots, Solar Flares, CMEs and the Solar Wind, Heliophysics Missions and Diagnostics, the Sun-Earth Connection, Space Weather Impacts on Technology).
- Every lecture slide deck has a paired lecture-notes file (confirmed via file listing and direct `<h1>` inspection of all 14 notes files); every lab has concrete apparatus/data, procedure, uncertainty treatment, deliverables, and assessment criteria; every problem set has a paired solution key and assessment-instructions file.
- `course-manifest.json` counts (14/14/7/7/7/7) match the actual file counts under `lectures/`, `labs/`, and `problem-sets/`.

## Depth and Rigor Appropriate to This Elective

- Governing relations are derived rather than merely applied: the hydrostatic scale-height relation (Lecture 01), the thin flux-tube magnetic-pressure balance (Lecture 04), the magnetic-reconnection free-energy order-of-magnitude estimate (Lecture 05), the isothermal Parker transonic wind critical-point equation -- solved numerically via bisection on the physical branch, not merely quoted (Lecture 08), the Chapman-Ferraro magnetopause standoff-distance formula (Lecture 11), and the Dessler-Parker-Sckopke ring-current/Dst relation (Lecture 12).
- A workspace-wide search across `materials/ASTR370/` for placeholder/meta-commentary strings (TODO, TBD, placeholder, instructor-created, FIXME, lorem ipsum) returned zero matches.
- Every worked numeric example is computed programmatically in `src/generate_astr370_content.py` / `src/generate_astr370_labs_psets.py`, not hand-typed, with real data (Solar Cycle 24/25 sunspot numbers, the 6 September 2017 AR12673 flare/CME/storm case study, the Carrington Event, and Parker Solar Probe) reused across the lecture, lab, and problem set that reference the same scenario.
- OpenStax Astronomy 2e Chapter 15's section numbering was cross-checked directly against its own embedded figure numbering this session (Figures 15.1-15.24 all appear under matching section headers with no offset), so this course's textbook citation is verified against the local extracted text rather than merely extrapolated by analogy.
- The Parker wind's numerical transonic solution (Lecture 08, Lab 04) is a genuine root-finding computation (bisection on the correct physical branch of a transcendental equation), not an algebraic shortcut -- matching this course's stated quantitative-rigor bar for an upper-division elective.

## Mechanical Visual-Reasoning Diagram Check

Grepped all 14 `lectures/*-slides.html` files for `data-lecture-figure` and confirmed 14 distinct `aria-label` descriptions (temperature-vs-radius profile, temperature-vs-height profile, schematic butterfly diagram, pressure bar chart, reconnection X-point diagram, GOES light curve, CME height-time kinematics, numerically solved Parker-wind curve, helioseismic ridge/coronagraph geometry, PSP trajectory overlay on the Parker-wind curve, magnetopause-standoff curve, Dst bar-chart comparison, satellite-lifetime curves, and a flowchart/energy-comparison capstone diagram) and confirmed via file-size inspection that no two files share byte-for-byte identical figure content. No repeated three-box or other generic diagram signature was found; each lecture's figure is a distinct plot type, bar chart, schematic, or flowchart built from that lecture's own real constants.

## Independent Recomputation Spot-Checks

An independent Python recomputation (outside the generator script, retyping the formulas from scratch rather than re-importing them) confirmed, to full precision: `g_sun = GM_sun/R_sun^2 = 274.27 m/s^2`; the sunspot magnetic pressure `P_mag = B^2/(2 mu0) = 31,194 Pa` for B=0.28 T; and the quiet-wind magnetopause standoff ratio `= 9.81 R_E`. The photospheric scale height matched to within 0.1% (a rounding-level discrepancy from the independently retyped mean molecular weight, not a formula error). No unit-conversion, comparative-magnitude-direction, or approximation-overclaiming defects were found in the spot-checked examples. The Dessler-Parker-Sckopke ring-current energies (Sept 2017: 2.19e14 J; Carrington conservative: 1.23e15 J; Carrington Tsurutani et al. 2003: 2.70e15 J) and the reference dipole energy E0=3.09e16 J were confirmed consistent with the module's own reported values.

## Reference and Data Integrity

- Solar Cycle 25 sunspot-number data (start date, smoothed minimum, smoothed maximum, not-smoothed maximum), the Carrington Event's Dst range and CME transit time, the 2024 Beggan et al. magnetometer-reanalysis field-change-rate finding, and Parker Solar Probe's launch date, perihelion, and record heliocentric speed were all live-verified this session via direct web fetch (Wikipedia articles citing SILSO/NOAA SWPC, Tsurutani et al. 2003, Cliver & Svalgaard 2005, Beggan et al. 2024, and NASA/JHUAPL mission documentation respectively) -- correctly labeled level 1 in `reference-log.md`.
- A direct live fetch specifically targeting the "Solar storm of September 2017" Wikipedia article was attempted this session and returned an HTTP 404 error. The AR12673/X9.3 flare, CME speed, and 2017 storm Dst values -- this course's central running case study -- are therefore correctly labeled level 2 (standard published, not independently re-verified this session), not level 1, and `reference-log.md` discloses this honestly with an explicit human spot-check recommendation, rather than silently presenting the case-study numbers as live-verified because other nearby facts were.
- The representative active-region volume (flare free-energy estimate), the CME drag-based deceleration functional form, and several schematic figure functional forms (solar interior temperature profile, atmosphere height profile, butterfly diagram, GOES light-curve shape, helioseismic ridge pattern, satellite-lifetime scaling) are correctly and honestly labeled level 3/illustrative in both the lecture text and `reference-log.md`, distinguished from the real-data provenance table.
- No fabricated references, mission facts, or URLs were found. All visuals are original, lecture-specific schematic SVGs/plots; no photographic or externally sourced images are used, so no external image-licensing review is required.

## Labs

- All seven labs are lecture-specific and non-formulaic (hydrostatic scale heights; solar-cycle data and sunspot pressure balance; flare free energy and the AR12673 case-study timeline; CME transit time and the numerically solved Parker wind; remote-sensing geometry and PSP in-situ prediction; magnetopause compression and ring-current energy; a GIC/course-synthesis capstone), each with explicit uncertainty/limitation discussion and distinct deliverables.

## Cadence Documentation

The 14-lecture/7-lab/7-problem-set matched 1:1 biweekly cadence is explicitly documented and justified in `syllabus.html`, following the ASTR230/310/320/340/350/360 matched-cadence precedent, with the specific justification (seven exactly-two-lecture thematic units) stated rather than assumed.

## Current Status

**Approved for review release.** This package was engineered to the ASTR230/ASTR360 depth benchmark from the outset, achieved live-verified (level 1) provenance for its historic-event and mission-fact comparisons (Carrington Event, Parker Solar Probe, Solar Cycle 25), and required no content corrections during this review beyond the honest level-2 disclosure of the central AR12673 case study (whose dedicated source page could not be live-fetched this session). Not yet approved for instructional use pending the residual items below.

## Outstanding Items Before Instructional Use

- **Human instructional approval:** required, as for every course package in this curriculum.
- **AR12673/X9.3 flare case-study spot-check:** confirm the flare's peak GOES flux, the CME's CDAW-catalog LASCO speed, and the 7-8 September 2017 storm's Dst minimum directly against NOAA SWPC event archives and the SOHO/LASCO CDAW catalog (flagged level 2, not live-verified this session, in `reference-log.md`).
- **Catalog/dataset spot-checks:** confirm the Solar Cycle 24 smoothed-maximum sunspot number, the sunspot umbral field strength, and standard solar-atmosphere pressure/density values against current solar-physics literature (see `reference-log.md`'s checklist).
- **Accessibility review:** alt text, color contrast, and accommodation alternatives have not been separately audited in this pass.
- **Policy alignment:** local academic-integrity, resubmission, and grading policy language finalized by the instructor of record.

Last updated: 2026-09-25
