# ASTR 476 Course Materials Review

Review date: 2026-09-25  
Review status: **Approved for review release. Not yet approved for instructional use.**

## Review scope and standard

Reviewed the syllabus and paired-module schedule; all 14 slide/notes pairs; all seven labs; all seven problem sets, solution keys, and grading instructions; source code; Pantheon+ excerpt and covariance metadata; provenance log; manifest; and generated index. The instructional depth and specificity were compared with the approved ASTR101 and ASTR120 benchmark review reports. This is a package-level review, not institutional curriculum approval or external peer review.

## Findings and correction log

1. **Resolved: invalid learning-objective HTML.** The first build placed an ordered list inside a paragraph. The generator now emits a closed paragraph followed by the list.
2. **Resolved: lecture notes too dependent on repeated scaffolding.** Added a distinct physical/observational explanation for every lecture, preserving the model assumptions, evidence class, worked anchor, limitation, and retrieval prompt.
3. **Resolved: incomplete computed answer detail.** Problem Set 02 now reports all requested distance measures at both redshifts; Problem Set 06 includes both finite-difference growth-rate estimates and their difference; Problem Set 04 reports uncertainty in radians, degrees, and arcminutes. Values are produced by the build script.
4. **Resolved: index notes links lacked lecture titles.** The generator now includes each lecture's source h1 title on both slide and notes links. The Pantheon+ retrieval date in the reference log is generated from the build date.
5. **Resolved: prerequisite disagreement.** Updated the generated syllabus and manifest to `ASTR 420 or concurrent enrollment`, matching both `astronomy_curriculum.html` and `astronomy_curriculum.json`.
6. **Resolved: schedule-context course link.** Added ASTR476 as an explicit linked option in the existing generic Year 4 Spring advanced-elective slot, while retaining its elective status and separate calendar-card link.
7. **Resolved: inaccurate paper titles.** Updated the reference-log generator with the exact published BOSS DR12 and DES Year 3 paper titles, so a rebuild preserves the bibliography correction.

## Scientific and instructional checks

- The Pantheon+ source table and 1701x1701 covariance were fetched and hashed. The 18-object excerpt is stratified, unique-CID, non-calibrator data; covariance indexing preserves source row order. The matched covariance block is included and used for the conditional intercept example. The excerpt is explicitly prohibited from supporting a survey-level cosmological constraint.
- Source covariance asymmetry was measured at 3e-8, consistent with its printed precision; the extractor accepts no more than 5e-8 and averages paired values. The selected block is checked for positive definiteness.
- Planck bandpower retrieval was attempted and failed (TT content extraction; TE HTTP 401). Planck is represented only by a published parameter summary; the CMB spectrum diagram is explicitly theoretical, not observed Planck data.
- Planck, BOSS, Pantheon+, and DES values are labeled published summaries not re-fetched from the papers. No combined probe likelihood is claimed. Model, schematic, and synthetic figures are labeled separately from data.
- The 14 diagrams use different data/geometries and are checked for distinct normalized SVG structure. Lecture titles are extracted from each artifact h1 for index generation.
- Labs specify setup/data, ordered procedures, uncertainty or numerical-error treatment, deliverables, and weighted criteria. Problem sets use exact questions, separate computed keys, and explicit grading/resubmission standards.
- Numeric checks include FLRW/Astropy agreement under matched matter-plus-Lambda assumptions, unit-conversion checks, BAO convention, covariance-aware likelihood, and shared computed solution values. The Hubble time is not described as the Universe's age.

## Final reviewer verdict

The final CourseMaterialsReviewAgent verdict is **Approved for review release**. The full package validator passed after the corrections (exit code 0): 14 slide/note pairs, seven labs, seven problem sets/solutions/assessment files, 52 HTML pages, 80 local links, four JSON files, 14 unique lecture diagrams, an 18-row excerpt with 18x18 covariance (minimum eigenvalue 0.01094), and all cosmology calculation self-tests. The exact `ASTR 420 or concurrent enrollment` prerequisite agrees across generated syllabus/manifest and catalog HTML/JSON. The calendar card and elective schedule slot both point to the course index. The generator emits the corrected BOSS/DES paper titles.

This is review-release approval only. Local instructor review of calendar dates, policies, and the cited level-2 literature values remains necessary before instructional use.