# ASTR 472 Course Materials Review Report

Status: Approved for review release. Not yet approved for instructional use.

## Initial Review Finding

The first review found that the seven student problem sets lacked adequately cross-checked numbered OpenStax companion exercises and an explicit adopted-edition caveat. It returned `Needs correction`; no release approval was granted.

## Correction Applied

- Added an exact numbered OpenStax exercise/question anchor to each of the seven student assignments, checked against `references/source-indexes/openstax-astronomy-2e-problem-index.md`.
- Corrected PS05 from the erroneous label "Chapter 6 Review Question 23" to the index's correct classification, "Chapter 6 Thought Question 23."
- Added a student-facing note to all seven assignments explaining that numbering/page breaks can vary by edition and requiring the instructor to spot-check the adopted print/PDF edition before LMS assignment.
- Added a per-set anchor/relevance table to `reference-log.md`, with an explicit note that the local extraction is an aid and not a substitute for adopted-edition verification.
- Regenerated all seven student problem sets from `src/generate_astr472_package.py`.

## Re-review Evidence

The first fresh re-review confirmed the exercise anchors but returned `Needs correction` because the outcome and release status had not yet been recorded. After documenting that correction and synchronizing the package to an awaiting-re-review state, the final reviewer re-review returned **Approved for review release**. It confirmed that all seven rendered assignments contain valid numbered anchors and the student-facing edition caveat; PS05 correctly identifies Thought Question 23; PS06 includes Figuring for Yourself 42, 43, and 53. The reviewer also confirmed manifest counts, local index links, the curriculum calendar link, and that ASTR472 remains an elective rather than a required-table course.

## Scope and Residual Caveats

The package contains 14 lectures with notes, seven labs, and seven problem sets with separate solutions and assessment instructions. It uses verified introductory OpenStax context while developing advanced radio-astronomy mathematics beyond the text. Exact exercise numbering has been checked against the local extracted index, but the adopted edition's page/exercise layout still requires instructor spot-check before LMS assignment. Survey/facility specifications and synthetic teaching tables retain the provenance and verification caveats recorded in `reference-log.md`.

Last updated: 2026-09-25
