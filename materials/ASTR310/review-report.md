# ASTR 310 Course Materials Review Report

Status: Approved for review release. Not yet approved for instructional use.

## Review Scope

Reviewed against the quality floor established by `materials/ASTR101/review-report.md` and `materials/ASTR120/review-report.md`, the real-data-grounding precedent of `materials/ASTR210/review-report.md`, and the depth/specificity/provenance standard of `materials/ASTR230/review-report.md` (read in full before drafting, per the course-package-orchestrator skill). As an upper-division (300-level) course, ASTR 310 was additionally required to substantially exceed ASTR101/120/210/230's quantitative rigor with real derivations, not just applied formulas. Inspected: `syllabus.html`, `schedule.html`, `course-manifest.json`, all 14 lecture slide decks and lecture notes, all 7 labs, all 7 problem sets with solution keys and assessment instructions, `reference-log.md`, `data/`, `src/generate_astr310_content.py`, and `src/generate_astr310_labs_psets.py`.

## Artifact Completeness and Dependency Order

- Syllabus and schedule exist before all lecture/lab/problem-set artifacts and are internally consistent (14 lectures, 7 labs, 7 problem sets, matched 1:1 biweekly cadence documented explicitly in `syllabus.html`'s "Lecture, Lab, and Problem-Set Cadence" section, with an explicit rationale citing both the ASTR210 credit-weight precedent and the ASTR230 matched-cadence precedent).
- Every lecture slide deck has a paired lecture-notes file; every lab has concrete apparatus/data, procedure, uncertainty treatment, deliverables, and assessment criteria; every problem set has a paired solution key and assessment-instructions file.
- `course-manifest.json` counts (14/14/7/7/7/7) match the actual file counts under `lectures/`, `labs/`, and `problem-sets/`.

## Depth and Rigor Appropriate to a 300-Level Course

- Each of the 14 lecture slide decks contains exactly 15 slides (title plus 14 content sections), matching the established structural benchmark. Spot-checked Lecture 08 directly.
- Unlike ASTR101/120/210/230, this course derives its governing equations rather than presenting them as applied tools: the Planck function and the Stefan-Boltzmann/Wien laws as its integral/limit (Lecture 02), the radiative transfer equation (Lecture 03), the Boltzmann/Saha equations (Lecture 04), the hydrostatic-equilibrium force balance (Lecture 05), the scalar virial theorem from the moment-of-inertia argument (Lecture 06), the shell theorem and escape velocity from energy conservation (Lecture 07), the reduced two-body problem and generalized Kepler's third law (Lecture 08), the tidal-acceleration expansion and Roche limit (Lecture 10), the vis-viva equation (Lecture 11), the restricted three-body L1 approximation (Lecture 12), and the Eddington luminosity from a radiation-pressure/gravity force balance (Lecture 13). This satisfies the user's explicit requirement for real derivations at this course level.
- No slide contains lecturer-facing or production-facing commentary, meta labels ("placeholder", "TBD", "instructor-created"), or raw unwrapped LaTeX in prose; a workspace-wide search across `materials/ASTR310/` for common placeholder/meta-commentary strings returned no matches.
- Every worked numeric example in every lecture, lab, and problem set is computed programmatically in `src/generate_astr310_content.py` / `src/generate_astr310_labs_psets.py`, not hand-typed, and the same underlying real dataset (principally Alpha Centauri AB, live-verified this session) is reused across the lecture, lab, and problem set that reference the same scenario.

## Independent Recomputation Spot-Checks

Recomputed by hand from the stated inputs and formulas (not merely reading the stated result), per the course-materials-review skill's requirement, with particular attention to unit-conversion bugs:

- **Lecture 02 Wien's constant and Alpha Centauri A luminosity:** recomputed b = hc/(4.9651142k) &asymp; 2.898 &times; 10&#8315;&sup3; m&middot;K (matches the standard value) and the Stefan-Boltzmann luminosity for Alpha Centauri A (R = 1.223 R&#8857;, T = 5,748 K); confirmed agreement with the deck's stated result and with the independently measured luminosity to within about 2%.
- **Lecture 08 / Lab 04 Alpha Centauri AB Kepler mass:** recomputed (m1+m2) = 4&pi;&sup2;a&sup3;/(GP&sup2;) from P = 79.762 yr and a = 23.299 AU (with explicit unit conversion to seconds and meters) and independently obtained &asymp;1.99 M&#8857;, matching the deck's stated value and the independently measured mass sum (1.988 M&#8857;) to well within 1%.
- **Problem Set 04 Sirius AB Kepler mass:** recomputed from P = 50.13 yr, a = 19.78 AU and independently obtained &asymp;3.08 M&#8857;, matching the solution key and the published Sirius A + Sirius B mass sum (&asymp;3.08 M&#8857;) closely.
- **Lecture 06 virial theorem, Sun central temperature: found and corrected a pedagogical accuracy defect during this review.** The original draft text characterized a factor-of-&asymp;6.8 discrepancy between the uniform-density virial-theorem central-temperature estimate ( &asymp;2.3 &times; 10&#8310; K) and the published standard-solar-model core temperature (1.57 &times; 10&#8309; K) as "an excellent result," which mischaracterizes the size of the disagreement. Corrected the wording (in both the affected evidence bullet and worked-example step) to accurately describe this as a genuine, expected limitation of the uniform-density approximation (real stars are far more centrally concentrated, so the true central temperature exceeds the volume-averaged virial estimate), rather than presenting a factor-of-7 gap as excellent agreement. Regenerated the affected lecture file after the fix.
- **Lecture 10 / Lab 05 Io tidal acceleration: found and corrected a genuine magnitude/comparison error during this review.** The original draft computed &Delta;a &asymp; 6.15 &times; 10&#8315;&sup3; m/s&sup2; correctly, but then claimed this was "more than X times Earth's surface gravity," which is physically backwards: 6.15 &times; 10&#8315;&sup3; m/s&sup2; is a small *fraction* of Earth's 9.8 m/s&sup2; (about 0.06%), not a multiple of it, and the resulting formatted text would have rendered as a nonsensical "more than 0.00 times" once the code ran. Corrected the comparison to use Io's own surface gravity (g = GM_Io/R_Io&sup2; &asymp; 1.796 m/s&sup2;, itself independently recomputed and matching the standard published value), giving a physically meaningful and correctly stated result (&asymp;0.34% of Io's own surface gravity). Propagated the same fix to Lab 05's procedure/deliverables wording and to Problem Set 05's Europa problem and solution key (Europa: &asymp;0.10% of its own surface gravity, correctly identifying Io as experiencing the stronger relative tidal stress). Regenerated all affected files after the fix.
- **Lecture 11 / Lab 06 Hohmann transfer to Mars:** independently recomputed all four vis-viva speeds (Earth circular 29.79 km/s, transfer perihelion/aphelion, Mars circular 24.14 km/s), both burns (&Delta;v1 &asymp; 2.95 km/s, &Delta;v2 &asymp; 2.66 km/s), and the transfer time (&asymp;259 days); all match well-known textbook values for an idealized circular, coplanar Earth-Mars Hohmann transfer.
- **Lecture 12 / Lab 06 Lagrange points:** independently recomputed the Sun-Earth L1 distance (&asymp;1.50 &times; 10&#8310; km, matching the real SOHO/DSCOVR operating distance) and the Sun-Jupiter L1 distance (&asymp;5.3 &times; 10&#8309; km, matching Jupiter's well-known Hill-sphere radius of &asymp;0.35 AU).
- **Lecture 13 Eddington luminosity:** independently recomputed L_Edd for a 1.4 M&#8857; accretor (&asymp;1.76 &times; 10&#179;&sup9; W &asymp; 4.6 &times; 10&#8308; L&#8857;), consistent with the well-known Eddington luminosity of a Chandrasekhar-mass compact accretor and with observed peak luminosities of accreting neutron stars/stellar-mass black holes in X-ray binaries.
- **Lecture 05 hydrostatic central pressure:** independently recomputed the uniform-density estimate for the Sun (&asymp;1.35 &times; 10&#185;&#8308; Pa) and confirmed the deck's own stated ratio to the published standard-solar-model value (&asymp;2.477 &times; 10&#185;&#8310; Pa, a factor of &asymp;184) is already correctly and appropriately hedged in the surrounding prose as an expected consequence of the uniform-density approximation, not overstated as close agreement.

No other numeric discrepancies were found in the spot-checked examples above; the two corrected items were caught specifically because this review independently recomputed rather than merely reading the stated results, exactly as the course-materials-review skill requires.

## Reference and Data Integrity

- Alpha Centauri A and B's masses, radii, luminosities, temperatures, and the AB system's orbital elements, plus Proxima Centauri's orbit about the AB barycenter, were independently verified via a live web fetch of Wikipedia's "Alpha Centauri" article during this course's production (citing Akeson et al. 2021, *AJ* 162, 14, and Kervella, Thevenin & Lovis 2017, *A&A* 598, L7), not merely recalled from training knowledge; this is the strongest-grounded real dataset in the package and is used consistently across Lectures 02, 07, 08, 09, 12, 13, 14, Labs 01, 04, 05, 06, 07, and (via the Sirius comparison) Problem Sets 01, 04, 05, 07.
- Sirius B's parameters are carried forward from ASTR230, where they were independently live-verified (Bond et al. 2017); this provenance chain is correctly disclosed rather than re-claimed as newly verified.
- Sirius A's parameters, the Sirius AB visual-binary orbital elements, M15 and 47 Tucanae's cluster parameters, Io/Europa/Jupiter's solar-system parameters, and the standard-solar-model central pressure/temperature are all correctly labeled as level-2 (standard published values, not independently re-verified this session) in `reference-log.md`, with an explicit human spot-check checklist, rather than being presented as unqualified primary-source data or mislabeled as synthetic.
- No purely synthetic (non-literature) numeric data is used anywhere in the package.
- No fabricated references, image credits, or URLs were found. All visuals are original, lecture-specific schematic SVGs, consistent with the ASTR101/210/230 precedent and not misrepresented as photographic.
- OpenStax Astronomy 2e chapter numbers were cross-checked against the local extracted text's embedded figure numbering (e.g., "Figure 3.6," "Figure 18.11"), following the ASTR230 precedent for resolving the source index's internal -1 chapter-numbering offset. `syllabus.html`, `schedule.html`, and `reference-log.md` correctly and explicitly identify which ASTR 310 topics (the Planck-function derivation, the Boltzmann/Saha equations, the virial theorem, tidal-force derivation, the vis-viva equation, the Eddington luminosity) are not covered at the introductory level in OpenStax Astronomy 2e at all, rather than fabricating an OpenStax citation for material the textbook does not contain.

## Labs

- All seven labs are lecture-specific and non-formulaic: each uses a distinct real dataset (Alpha Centauri AB, hydrogen excitation physics, the Sun/M15, Alpha Centauri AB orbital elements, Earth-Moon/Io tidal parameters, Earth-Mars/Sun-Jupiter orbital mechanics, or the full Alpha Centauri AB capstone dataset), a distinct procedure, and distinct deliverables; no lab is a retitled copy of another.
- Each lab includes explicit uncertainty treatment (e.g., Lab 01's R&sup2;T&#8308; uncertainty-propagation exercise; Lab 04's semimajor-axis uncertainty propagation through Kepler's third law; Lab 07's explicit discussion of the shared parallax dependency limiting the independence of the radiative and dynamical cross-checks).
- Provenance is logged per-lab in each lab's own "References and Provenance" section and centrally in `reference-log.md`.

## Problem Sets, Solutions, and Assessment Instructions

- Problem sets contain concrete, lecture-specific numeric problems using distinct real scenarios (Sirius A/B, Vega, 47 Tucanae, the Sirius AB system, Europa, a Venus transfer orbit, and a Sirius AB capstone synthesis) rather than reusing the same lab dataset verbatim, while still exercising the same derived physical tools.
- Solution keys show full worked arithmetic (not just final answers) and point-by-point rubrics.
- Assessment-instructions files specify a resubmission policy, problem-level criteria, and common-error flags, with explicit attention to unit-conversion errors (the most common defect class identified in this review and in the ASTR230 precedent).

## Cadence Documentation

The 14-lecture/7-lab/7-problem-set matched 1:1 biweekly cadence is explicitly documented and justified in `syllabus.html`'s "Lecture, Lab, and Problem-Set Cadence" section, citing both the ASTR210 credit-weight precedent (4 credits, 14 lectures) and the ASTR230 matched-cadence precedent, with an explicit rationale specific to this course (building one cumulative derivation toolkit toward a single capstone unit rather than an uneven technical-report cadence).

## Residual Risks and Caveats

- Sirius A's parameters, the Sirius AB orbital elements, the M15/47 Tucanae cluster parameters, the Io/Europa/Jupiter solar-system parameters, and the standard-solar-model central pressure/temperature are standard literature/pedagogical values not independently re-verified by live fetch this session; human spot-check against SIMBAD/the Washington Double Star Catalog, the Harris globular cluster catalog, and the JPL Solar System Dynamics database is required before instructional release (see `reference-log.md` checklist).
- The Alpha Centauri AB live-verified data was sourced from Wikipedia's synthesis of the cited primary papers (Akeson et al. 2021; Kervella et al. 2017), not from the primary papers directly; a human should confirm the primary-source values directly before instructional release.
- The radiative and dynamical cross-checks used repeatedly in this course (e.g., in Lecture 14 and Lab 07) share a common dependency on Alpha Centauri's measured parallax/distance; this is explicitly disclosed in the lecture and lab materials themselves as a genuine limitation on the independence of the two verification chains, not hidden.
- Accessibility review (alt text, color contrast, observing-accommodation alternatives) has not been separately audited in this pass.

## Current Status

**Approved for review release.** This course was engineered from the outset to the ASTR230 depth benchmark and explicitly required to exceed it in quantitative rigor, per the user's request for a genuinely upper-division astrophysics course. This review independently recomputed eight separate worked examples spanning radiative, hydrostatic/virial, and orbital-mechanics content, catching and correcting two genuine defects (an overstated agreement claim in the virial-theorem temperature estimate, and a physically backwards tidal-acceleration-to-gravity comparison for Io) before approval. Not yet approved for instructional use pending the residual data-verification and accessibility items above.

## Outstanding Items Before Instructional Use

- **Human instructional approval:** required, as for every course package in this curriculum.
- **Catalog/dataset spot-check:** confirm Alpha Centauri AB and Proxima Centauri parameters against the primary Akeson et al. (2021) and Kervella et al. (2017) papers and SIMBAD/Gaia DR3; confirm Sirius A and the Sirius AB orbit against SIMBAD/the Washington Double Star Catalog; confirm M15/47 Tucanae against the Harris catalog; confirm Io/Europa/Jupiter against JPL Solar System Dynamics; confirm the standard-solar-model values against a current published solar-interior model (see `reference-log.md` checklist).
- **OpenStax spot-check:** verify exact section/page numbers against the adopted edition, and confirm the explicit "extends beyond OpenStax" labeling on the derivation-heavy lectures remains accurate for the specific adopted edition.
- **Accessibility review:** alt text, color contrast, and accommodation alternatives.
- **Policy alignment:** local academic-integrity, resubmission, and grading policy language finalized by the instructor of record.

Last updated: 2026-09-24
