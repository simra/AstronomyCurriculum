# ASTR 370: Solar Physics and Space Weather

3-credit, 300-level elective. Prerequisites: PHYS 172; ASTR 230. Year 3 elective in the four-year astronomy curriculum.

Introduces solar structure, magnetic activity, sunspots, flares, coronal mass ejections, the solar wind, heliophysics missions, magnetospheric response, and space weather impacts on technology.

## Contents

- `syllabus.html` — course description, learning outcomes, assessment weights, cadence rationale, and prerequisites justification.
- `schedule.html` — lecture, lab, and problem-set schedule.
- `reference-log.md` — tri-level (live-verified / standard published / synthetic) data-provenance log for every real dataset and mission fact used.
- `course-manifest.json` — machine-readable course metadata, artifact counts, cadence, and data provenance.
- `review-report.md` — course-materials review findings and release status.
- `index.html` — course landing page linking every artifact.
- `lectures/` — 14 lecture slide decks (`lecture-NN-slides.html`) and paired lecture notes (`lecture-NN-notes.html`).
- `labs/` — 7 labs (`lab-NN.html`).
- `problem-sets/` — 7 problem sets, each with a student version (`problem-set-NN.html`), solution key (`problem-set-NN-solutions.html`), and grading-agent assessment instructions (`problem-set-NN-assessment.md`).
- `data/` — generated CSV datasets and provenance notes.
- `src/` — Python generator scripts that programmatically compute every worked example and render every lecture/lab/problem-set page.

## Reproducing the Generated Content

```
python materials/ASTR370/src/generate_astr370_content.py
python materials/ASTR370/src/generate_astr370_labs_psets.py
```

Both scripts are deterministic: every numeric worked example is computed from the shared physical constants and real datasets defined in `generate_astr370_content.py`, and the same constants are reused across the lecture, lab, and problem set referencing the same scenario.

## Running Case Study

This course uses one real, extensively documented event as a running case study across Units 3, 4, 6, and 7: the 6 September 2017 X9.3 solar flare from active region 12673, its associated fast coronal mass ejection, and the resulting G4 geomagnetic storm. It is explicitly flagged in Lecture 06 as an illustrative worked example, not a statistically typical flare-to-storm chain. The historic 1859 Carrington Event and the Parker Solar Probe mission are used as comparison points (both live-verified via direct web fetch this session; see `reference-log.md`).

## Status

Approved for review release (course-materials review complete). Not yet approved for instructional use; see `review-report.md` for outstanding human spot-check items.
