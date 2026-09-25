# ASTR 420 Course Materials Review Report

**Status: Approved for review release. Not yet approved for instructional use.**

## Review scope

Reviewed the complete ASTR420 package: syllabus, schedule, reference log, manifest, README files, data README and five teaching extracts, 14 lecture slide decks, 14 lecture notes files, 7 labs, 7 problem sets, 7 solution keys, 7 assessment-instruction files, and final index. The package was checked against the approved ASTR101/ASTR120 quality floor and the ASTR370/ASTR410 review reports.

## Completeness and dependency order

- The package contains 14 lecture slide/note pairs, 7 labs, 7 problem sets, 7 solution keys, and 7 assessment-instruction files.
- Syllabus and schedule define the sequence before downstream artifacts. The seven labs and problem sets follow seven explicitly documented two-lecture units.
- The manifest counts match the concrete files on disk: 14/14/7/7/7/7.
- `index.html` links planning documents, all title-bearing lecture slide/note pairs, all labs, all problem-set artifacts, data, source, manifest, and this review report.

## Depth, rigor, and alignment

The lecture arc moves from expansion and redshift through relativistic distance measures, Friedmann dynamics, cosmic time, thermal history, the CMB, nucleosynthesis, inflation, perturbation growth, BAO, supernovae and dark energy, lensing, the matter power spectrum, and a multi-probe synthesis with parameter tensions. Each deck contains objectives, motivation, an observational evidence frame, a governing relation, a computed example, an interpretation/limitation boundary, an active reasoning prompt, a unit connection, takeaways, and exact reading anchors. Notes expand the same sequence with derivation context, misconceptions, assumptions, and study guidance.

Labs require a named CSV, setup, raw-data inspection, a reproducible transformation or fit, a prescribed sensitivity test, uncertainty treatment, a validation check, a labeled figure, deliverables, and grading criteria. Problem sets contain four concrete derivation/data/critique/transfer questions, separate solution keys, and separate assessment instructions.

## Visual-reasoning check

Each of the 14 lecture slide files contains one large SVG visual with a lecture-specific `aria-label`. The diagrams are mechanically distinct: Hubble plot, light cone, component-density curves, cosmic timeline, cooling curve, CMB spectrum, nucleosynthesis flow, inflation horizon, perturbation growth, BAO correlation, supernova residual curve, lensing mass map, power spectrum, and evidence matrix. The final generated decks contain no repeated SVG string across lectures and no student-facing production labels or raw forbidden LaTeX command tokens.

## Textbook and provenance integrity

The local extracted OpenStax text was directly inspected for native Chapter 29 headings and embedded figure identifiers, including Figures 29.10 and 29.11. The source index has a chapter-label offset near the Chapter 29 boundary; exact exercise identifiers are therefore recorded with an explicit adopted-PDF spot-check requirement rather than treated as authoritative pagination. Chapter 26 section 26.5 and Chapter 28 sections 28.4-28.5 are used for distance, lensing, and structure context.

Provenance is tri-level and honest. Level 1 covers the local extracted source text inspected during production. CMB, BAO, supernova, BBN, and matter-power values are level 2 published summaries not re-verified during this session and are flagged for human spot-check. Compact CSVs and SVG/model curves are level 3 instructor-provided teaching artifacts derived from those summaries; they are not new observations.

## Independent recomputation

An independent calculation, retyping the formulas rather than importing the generator, checked the following relationships and directions:

- $H_0=67.4\,\mathrm{km\,s^{-1}\,Mpc^{-1}}$ converts to the SI expansion rate before evaluating $\rho_c=3H_0^2/(8\pi G)$.
- Simpson integration of $1/[(1+z)E(z)]$ with the shared $\Omega_r$, $\Omega_m$, and $\Omega_\Lambda$ values gives a finite lookback time to $z=1$ of approximately $7.7$ Gyr, not $1/H_0$ by assertion.
- $Y_p=2(1/7)/(1+1/7)=0.25$ for the explicitly stated neutron-to-proton estimate.
- Wien's law with $T=2.7255$ K gives a CMB intensity-peak frequency of approximately $160.2$ GHz; the frequency/wavelength peak distinction is stated.
- $\mu=43.16$ gives $D_L=10^{(\mu-25)/5}\approx2.83\times10^3$ Mpc.
- Independent Gaussian summaries $73.04\pm1.04$ and $67.4\pm0.5$ differ by approximately $4.9\sigma$ under the stated independence assumption.

No unit-direction, comparative-direction, or approximation-honesty defect remained in these checks. The power-spectrum and lensing examples explicitly identify their model and calibration dependence rather than claiming direct measurement.

## Final assembly and navigation

Lecture anchor text in `index.html` was generated from the lecture metadata and directly compared with each linked lecture `<h1>`. Lab anchor text was directly compared with each linked lab `<h1>`; Lab 01 is `ASTR 420 Lab 01: Expansion and Redshift Audit`. `astronomy_curriculum.html` contains one ASTR420 Course materials badge in the calendar card and the existing Four-Year Course List row links to `materials/ASTR420/index.html`. Root `index.html` was not changed.

## Residual risks before instructional use

- Human spot-check all level-2 values against the adopted Planck/CMB, BAO, supernova, BBN, and matter-power sources named in `reference-log.md`.
- Confirm OpenStax Chapter 29 exercise wording and numbering against the adopted PDF because the generated local problem index has a boundary offset.
- Complete accessibility/contrast review and add institution-specific academic-integrity, accommodations, attendance, calendar, and instructor-policy language.

**Review verdict: Approved for review release.**
