# ASTR 340: Astronomical Instrumentation

3-credit, 300-level, one-semester course. Year 3, Spring, in the four-year curriculum. Prerequisites: ASTR 210; PHYS 275.

See [syllabus.html](syllabus.html) for the full syllabus, [schedule.html](schedule.html) for the lecture/lab/problem-set schedule, and [index.html](index.html) for the full course package landing page.

## Structure

- `lectures/` - 14 lecture slide decks and paired lecture notes.
- `labs/` - 7 labs (biweekly, matched 1:1 with problem sets).
- `problem-sets/` - 7 problem sets, each with a solution key and assessment instructions.
- `src/` - generator scripts that compute every worked example programmatically and produce the HTML lecture/lab/problem-set content.
- `data/` - course datasets (see `data/README.md`).
- `reference-log.md` - reference, dataset, and visual verification log.
- `review-report.md` - review status and history.

## What This Course Builds On and Adds

ASTR 340 is the direct instrumentation-focused sequel to ASTR 210 (Observational Astronomy and Data Analysis). Where ASTR 210 taught operational CCD reduction and calibration, ASTR 340 derives the underlying physics of every stage of the observing chain from first principles -- the Rayleigh criterion and diffraction limit, plate scale and Nyquist sampling, CCD detector and noise physics, the CCD signal-to-noise equation, the calibration equation, photometric filter systems, the grating equation and spectral resolving power, adaptive-optics wavefront correction and the Strehl ratio, space-based-instrument trade-offs, and radiometric error budgets -- and applies each derivation to real telescope and instrument specifications. Every worked numeric example is computed programmatically from real astronomical instrument data, principally the Keck Observatory (aperture, collecting area, focal length, and its HIRES echelle spectrograph's radial-velocity precision, both independently live-verified for this course) plus standard published specifications for HST, VLT, JWST, DECam, and Keck's adaptive optics system, rather than hand-typed.
