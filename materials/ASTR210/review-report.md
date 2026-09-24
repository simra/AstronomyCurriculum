# ASTR 210 Course Materials Review Report

Status: Approved for review release (second pass); not yet approved for instructional use.

## Trigger for Second Pass

The prior "Approved for review release" status recorded in this file was granted on structural completeness only (file counts, template shape, manifest consistency) and was voided by the orchestrator at the user's direction. On inspection, the first-pass slide decks, lecture notes, labs, and problem sets were template-shallow: slide decks stopped after roughly 11 generic slides (missing dedicated misconception, active-learning, lab-connection, and synthesis slides present in the ASTR101/ASTR120 benchmark); labs had blank measurement tables with no real data, apparatus, or computed check values; problem sets used generic prompts ("compute the corrected quantity from the supplied raw values") with no actual supplied values. This is exactly the shallow-generation failure mode the ASTR101 second pass corrected, and ASTR210 required the same correction.

## Corrections Applied

- Regenerated all 14 lecture slide decks to 15 slides each (title plus 14 content slides: goals, why-matters, opening phenomenon, vocabulary, evidence, model, quantitative tool, worked example, visual reasoning, misconception, active learning, lab connection, synthesis, references), matching the ASTR101/ASTR120 structural and depth benchmark.
- Regenerated all 14 lecture notes to expand rather than restate the slides, with the same evidence, model, and worked-example content plus study-guide synthesis questions.
- Grounded every lecture in an exact OpenStax Astronomy 2e chapter/section anchor (Ch 1.3, 4.1, 5.3, 5.6, 6.1-6.3, 17.1, 19.2-19.3, 21.4), verified against `references/source-indexes/openstax-astronomy-2e-problem-index.md`.
- Replaced every lecture's worked example with a quantitatively correct calculation computed in Python at generation time (see `materials/ASTR210/src/generate_astr210_content.py`), eliminating a real arithmetic error present in the first-pass calibration example (the old deck claimed a 588 ADU result that did not match its own stated inputs).
- Tied six of the fourteen worked examples directly to the course's real CSV datasets (photometric zero-point derivation from `photometry_standard_stars.csv`, light-curve dip depth from `variable_star_lightcurve.csv`, plate-scale derivation from `asteroid_astrometry.csv`, three-line radial-velocity cross-check from `spectrum_lines.csv`, and a parallax quality cut from `archive_query_sample.csv`), so lecture, lab, and problem-set numbers are internally consistent with each other rather than independently invented.
- Rewrote all seven labs with concrete apparatus/data tables, step-by-step procedures, explicit uncertainty-propagation steps, deliverables, and assessment criteria; replaced blank measurement tables with real raw values and at least one worked check per lab.
- Rewrote all seven problem sets, solution keys, and assessment-instruction files with concrete, lecture-specific numeric problems (not generic prompts), fully worked solutions with correct arithmetic, and point-by-point grading criteria plus a resubmission policy.
- Verified and documented that the 14-lecture / 7-lab / 7-problem-set structure is an intentional biweekly technique-unit cadence, not a gap: added an explicit "Lab and Problem-Set Cadence" table to `syllabus.html` showing which lecture pairs map to which lab/problem set, and confirming the final two lecture pairs (stacking/time-domain, and uncertainty/report workshop) are assessed via problem sets and the capstone technical observing report rather than a dedicated lab.
- Updated `reference-log.md` to document the regenerated content, the shared/consistent dataset use, and the calibration-frame/SNR-scenario values that remain synthetic and require replacement with local raw data before instructional use.

## Post-Approval Update: Real Calibration Data for Lab 01

After the second-pass approval below, Lecture 1, Lecture 3, Lab 01, and Problem Set 1 were regrounded in real Canon EOS M50 calibration data (bias/dark/flat master frames and light-frame patches from a real 2022-07-19 BackyardEOS/Astro Pixel Processor imaging session, verified directly from the FITS headers and raw CR3 pixel data), replacing the previously synthetic "cooled CCD imager" bias/dark/flat numbers. The calibration model was also corrected from a separate bias-then-dark subtraction to a single matched-exposure dark subtraction (I_cal=(raw-D)/F), which is the physically correct model for this camera's master-dark workflow and is more advanced/accurate than the original synthetic example. See `reference-log.md` for exact file citations and patch coordinates. Lab 02 remains an intentionally synthetic, computation-only SNR exercise and does not require raw frames.

## Remaining Review Items

- Human reviewer should confirm the local teaching style matches the depth level chosen here (15-slide decks, four-problem problem sets).
- Lab 01 now uses real, verified Canon EOS M50 calibration data (see the Post-Approval Update above and `reference-log.md`); Lab 02 remains an intentionally synthetic, computation-only SNR exercise that does not require raw frames.
- External/mission imagery has not been added; all visuals remain original, lecture-specific SVG schematics, consistent with the ASTR101 pattern before its own visual-enrichment pass. A `VisualReferenceResearchAgent` pass could add verified real observational imagery (e.g., NASA/ESA CCD frames, arc-lamp spectra) as a future enhancement, but its absence does not block review-release status, matching the ASTR101 precedent.
- The OpenStax chapter/section anchors are section-level, not exact problem-number citations, because ASTR210's data-reduction content (calibration, SNR, plate solving) goes beyond OpenStax Astronomy 2e's introductory-textbook scope; a human should spot-check these anchors against the adopted edition before instructional release, exactly as flagged for ASTR101.
- Lab local feasibility (equipment, software, safety, weather policy) has not been assessed and remains a pre-instructional-use requirement, as for every course in this curriculum.

## Current Status

Approved for review release. Not yet approved for instructional use. This approval reflects a genuine content-quality review against the ASTR101/ASTR120 benchmark (lecture-specific depth, quantitative rigor, internally consistent data, concrete labs and problem sets), not a structural or file-count check.

## Outstanding Items Before Instructional Use

- **Human instructional approval:** required, as for every course package in this curriculum; agent review validates structure, consistency, and depth but not local teaching judgment.
- **Raw calibration data:** Lab 01 now uses real Canon EOS M50 master bias/dark/flat frames and light-frame patches (see the Post-Approval Update above); a human should still spot-check the cited patch coordinates and file provenance. Lab 02 remains an intentionally synthetic, computation-only exercise.
- **Lab local feasibility:** telescope/CCD/spectrograph availability, safety practices, and weather alternatives must be confirmed locally.
- **OpenStax spot-check:** a human should verify the exact section anchors against the adopted OpenStax Astronomy 2e edition.
- **Accessibility review:** alt text, color contrast, and observing-accommodation alternatives have not been separately audited in this pass.
- **Policy alignment:** syllabus language for local academic-integrity, safety, and weather policies should be finalized by the instructor of record.

Last updated: 2026-09-24
