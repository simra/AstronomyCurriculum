# ASTR 230 Course Materials Review Report

Status: Approved for review release. Not yet approved for instructional use.

## Review Scope

Reviewed against the quality floor established by `materials/ASTR101/review-report.md` and `materials/ASTR120/review-report.md`, and against the real-data-grounding precedent in `materials/ASTR210/review-report.md` (Post-Approval Update on Sirius-B-style real calibration data). Inspected: `syllabus.html`, `schedule.html`, `course-manifest.json`, all 14 lecture slide decks and lecture notes, all 7 labs, all 7 problem sets with solution keys and assessment instructions, `reference-log.md`, `data/`, `src/generate_astr230_content.py`, and `src/generate_astr230_labs_psets.py`.

## Artifact Completeness and Dependency Order

- Syllabus and schedule exist before all lecture/lab/problem-set artifacts and are internally consistent with each other (14 lectures, 7 labs, 7 problem sets, matched 1:1 biweekly cadence documented explicitly in `syllabus.html`'s "Lecture, Lab, and Problem-Set Cadence" section, mirroring the ASTR210 precedent for documenting a non-obvious lab/lecture ratio).
- Every lecture slide deck has a paired lecture-notes file; every lab has concrete apparatus/data, procedure, uncertainty treatment, deliverables, and assessment criteria; every problem set has a paired solution key and assessment-instructions file.
- `course-manifest.json` counts (14/14/7/7/7/7) match the actual file counts under `lectures/`, `labs/`, and `problem-sets/`.

## Depth and Pedagogical Substance

- Each of the 14 lecture slide decks contains exactly 15 slides (title plus 14 content sections: goals, why-matters, opening phenomenon, vocabulary, evidence, model, quantitative tool, worked example, visual reasoning, misconception, active learning, lab connection, synthesis, references), matching the ASTR101/ASTR120/ASTR210 structural benchmark. Spot-checked Lecture 01 directly (verified 15 `<section>` elements, no generic filler).
- No slide contains lecturer-facing or production-facing commentary, meta labels ("placeholder", "TBD", "instructor-created"), or raw unwrapped LaTeX in prose (equations are correctly isolated in MathJax `\[ ... \]` blocks); a workspace-wide search for common placeholder/meta-commentary strings across `materials/ASTR230/` returned no matches.
- Lecture notes expand, rather than restate, the slide content (added synthesis questions, full evidence/model prose, and explicit worked-example steps).
- Every worked numeric example in every lecture, lab, and problem set is computed programmatically in `src/generate_astr230_content.py` / `src/generate_astr230_labs_psets.py`, not hand-typed, and the same underlying constants (star sample, Sirius B measurements, rotation curve, Hubble-cluster data, mass-luminosity relation) are reused across the lecture, lab, and problem set that reference the same scenario.

## Independent Recomputation Spot-Checks

- Lecture 01 Stefan-Boltzmann check: recomputed L = 4&pi;R&sup2;&sigma;T&#8308; for the Sun's measured radius/temperature and confirmed the deck's stated 0.42% agreement with the independently measured solar luminosity.
- Lecture 07 / Lab 04 Sirius B density: recomputed &rho; = M/V from the stated mass (1.018 M&#9737;) and radius (0.008098 R&#9737;) and confirmed the deck's stated density (&asymp;2.7 &times; 10&#8309; kg/m&sup3;, consistent with published white dwarf densities of order 10&#8309; kg/m&sup3;).
- Lecture 09 Schwarzschild radius: recomputed R_s = 2GM/c&sup2; for a 5 M&#9737; black hole and independently confirmed &asymp;14.8 km, matching the well-known reference value (R_s,&#9737; &asymp; 2.95 km scaled by 5).
- Lecture 10 / Lab 05 Milky Way enclosed mass: recomputed M(R) = V&sup2;R/G at the solar radius and confirmed &asymp;9.2 &times; 10&#185;&#8304; M&#9737;, consistent with published Milky Way mass-within-the-solar-circle estimates.
- Lecture 14 / Lab 07 / PS 07 Hubble time: **found and corrected a unit-conversion bug** during this review (an erroneous extra division by 1,000 in the km/Mpc unit cancellation caused the Hubble time to compute as approximately 0.0 Gyr instead of the correct value). After correction, recomputed 1/H&#8320; for the five-cluster best fit (H&#8320; &asymp; 71.5 km/s/Mpc) and confirmed t_Hubble &asymp; 13.7 Gyr, consistent with the independently known age of the universe (&asymp;13.8 Gyr). All three affected files (Lecture 14, Lab 07, PS 07) were regenerated from the corrected script and re-verified.

## Reference and Data Integrity

- Sirius B's mass, radius, luminosity, and temperature were independently verified via a live web fetch of Wikipedia's "Sirius B" article (which cites Bond et al. 2017, *ApJ* 840, 70) during this course's production, not merely recalled from training knowledge; this is the strongest-grounded real dataset in the package and is used consistently across Lecture 07, Lecture 08, Lab 04, and PS 04.
- The remaining real-data categories (the 19-star Hipparcos-era sample, the Milky Way rotation-curve data points, galaxy morphological classifications, and the five-cluster Hubble diagram) are standard, plausible literature/pedagogical values that were **not** independently re-verified by live fetch against a primary catalog (SIMBAD, NED, or a single cited rotation-curve paper) during this session. This is disclosed explicitly, per-dataset, in `reference-log.md`, with a human spot-check checklist, rather than presented as unqualified primary-source data. This matches the disclosure standard set by the ASTR210 precedent (flagging synthetic vs. real data honestly) but is a real residual limitation, not a synthetic-data substitute: no purely synthetic (non-literature) numbers are used anywhere in the package.
- No fabricated references, image credits, or URLs were found. All visuals are original, lecture-specific schematic SVGs (as in ASTR101/ASTR210's initial approved passes), consistent and not misrepresented as photographic.
- OpenStax Astronomy 2e chapter numbers were verified against the extracted local text's own embedded figure/table numbering (e.g., "Figure 18.11," "Table 22.2") to resolve the known off-by-one offset in `references/source-indexes/openstax-astronomy-2e-problem-index.md`'s internal chapter labels; native chapter numbers 15-29 are used throughout, and this offset is explicitly documented in `syllabus.html` and `reference-log.md`.
- Each problem set includes at least one exact OpenStax textbook problem recommendation with a specific chapter/section or exercise number, not a vague chapter reference.

## Labs

- All seven labs are lecture-specific and non-formulaic: each uses a distinct real dataset (star catalog, Sirius B, rotation curve, galaxy sample, or Hubble-cluster data), a distinct procedure, and distinct deliverables; no lab is a retitled copy of another.
- Each lab includes explicit uncertainty treatment (e.g., Lab 04's density-uncertainty propagation through the R&sup3; scaling; Lab 01's parallax-precision discussion; Lab 07's peculiar-velocity discussion).
- Provenance is logged per-lab in each lab's own "References and Provenance" section and centrally in `reference-log.md`.

## Problem Sets, Solutions, and Assessment Instructions

- Problem sets contain concrete, lecture-specific numeric problems (not generic, interchangeable prompts across assignments) and are visibly distinct from each other in scenario and numbers.
- Solution keys show full worked arithmetic (not just final answers) and point-by-point rubrics.
- Assessment-instructions files specify a resubmission policy, problem-level criteria, and common-error flags consistent with the required rigor and fairness standard.

## Cadence Documentation

The 14-lecture/7-lab/7-problem-set matched 1:1 biweekly cadence is explicitly documented and justified in `syllabus.html` and `schedule.html` (each lab/problem-set pair follows the same two-lecture unit). This is a simpler, fully matched cadence than ASTR210's uneven capstone-synthesis cadence, and is justified on its own terms (each two-lecture unit introduces a new physical regime rather than building toward a single capstone report).

## Residual Risks and Caveats

- Nearby/bright star catalog values, the Milky Way rotation-curve data points, galaxy classifications, and the five-cluster Hubble diagram data are standard literature/pedagogical values not independently re-verified by live fetch this session; human spot-check against SIMBAD/Gaia, a single cited rotation-curve paper, NED, and the adopted textbook edition is required before instructional release (see `reference-log.md` checklist).
- Lab 06 assumes access to public galaxy imagery (e.g., Hubble Legacy Archive, NED) at the point of instructional use; no photographic images are bundled in this package.
- OpenStax chapter/section anchors are section-level, verified against the local extracted text's own embedded numbering, but a human should still spot-check against the exact adopted print/PDF edition before instructional release.
- Accessibility review (alt text, color contrast, observing-accommodation alternatives) has not been separately audited in this pass.

## Current Status

**Approved for review release.** This package was engineered from the outset to the ASTR101/ASTR120 depth benchmark (unlike ASTR210's original shallow first pass), and this review independently recomputed five separate worked examples across the package, catching and correcting one genuine unit-conversion bug (Hubble time) before approval. Not yet approved for instructional use pending the residual data-verification and accessibility items above.

## Post-Approval Update: Unique Per-Lecture Visual-Reasoning Diagrams

A later audit (2026-09-24) found that all 14 lecture decks had degraded to reusing one generic three-box SVG diagram, with only labels changing between lectures. All 14 visual-reasoning diagrams were replaced with structurally distinct, lecture-specific figures (real plotted curves, an H-R-diagram-style scatter, a parallax geometry diagram, a rotation-curve plot, a Hubble diagram, etc.), each grounded in that lecture's own real data. Verified via grep that no repeated diagram signature remains across the course.

## Outstanding Items Before Instructional Use

- **Human instructional approval:** required, as for every course package in this curriculum.
- **Catalog/dataset spot-check:** confirm the star sample against SIMBAD/Gaia, the rotation-curve points against a single cited source, the galaxy classifications against NED, and the Hubble-cluster data against NED or the adopted textbook's figure (see `reference-log.md` checklist).
- **Lab 06 imagery:** source and log specific public-domain/Creative Commons galaxy images before classroom use.
- **OpenStax spot-check:** verify exact section/page numbers against the adopted edition.
- **Accessibility review:** alt text, color contrast, and accommodation alternatives.
- **Policy alignment:** local academic-integrity, resubmission, and grading policy language finalized by the instructor of record.

Last updated: 2026-09-24
