# ASTR 340 Reference Log

Tracks references, datasets, and visuals used in ASTR 340 materials, their verification status, and any human spot-check requirements. Provenance is labeled at one of three explicit levels throughout: **(1) live-verified this session** (fetched/extracted from a primary or authoritative source during this course's production), **(2) standard published/literature or manufacturer/mission-specification value not re-verified this session** (flagged for human spot-check), or **(3) synthetic/instructor-provided placeholder**. Schematic physics approximations (e.g., a representative rather than site-specific sky brightness or system throughput, an illustrative rather than exact-as-built HIRES beam width) are explicitly labeled as illustrative, not precision values, and are distinct from the data-provenance question addressed here.

## Textbook

- OpenStax Astronomy 2e (openly licensed; local extracted copy `references/openstax-astronomy-2e-extracted.txt`). Chapter 6 (astronomical instruments) covers telescopes, detectors, and instrumentation only descriptively at an introductory level. Nearly every quantitative ASTR 340 topic (the Rayleigh criterion derivation, plate scale/Nyquist sampling, CCD noise theory, the CCD signal-to-noise equation, the calibration equation, the grating equation and resolving power, the Mar&eacute;chal approximation, and radiometric error budgets) is **not covered at the introductory level in OpenStax Astronomy 2e at all** and is developed here from first principles instead; this is stated explicitly in `syllabus.html`, `schedule.html`, and each affected lecture's slides/notes rather than presented as an OpenStax-sourced result.

## Real Data Used in Lectures/Labs/Problem Sets

| Dataset | Used in | Source | Verification Level |
|---|---|---|---|
| Keck I/II: 10 m aperture, 76 m&sup2; collecting area, 17.5 m effective focal length, 36 hexagonal 1.8 m segments, 4,145 m altitude, 4 nm active-optics surface accuracy | Lectures 01, 02, 03, 11, 12, 13, 14; Labs 01, 02, 03, 06, 07; PS 01, 07 | Wikipedia "W. M. Keck Observatory" article, retrieved live this session (2026-09-24) | **Level 1: live-verified this session.** This is the course's primary real telescope dataset. |
| Keck HIRES: radial-velocity precision 1.0 m/s, 1 AU planet-detection limit 0.2 M_Jup | Lecture 10; Lab 05 | Wikipedia "W. M. Keck Observatory" article (Instruments section), retrieved live this session (2026-09-24), citing Vogt et al. (1994), *SPIE* 2198, 362 | **Level 1: live-verified this session.** |
| HIRES resolving power (R&asymp;67,000), groove density (52.67 grooves/mm), blaze angle (70&deg;) | Lecture 10; Lab 05; PS 05 | Standard published instrument specification consistent with Vogt et al. (1994), *SPIE* 2198, 362, not independently re-verified this session (a direct fetch of the dedicated HIRES specification page was attempted this session and did not return usable content; the value used is a well-established, widely cited instrument parameter) | **Level 2: not independently re-verified this session.** Flagged for spot-check against the Keck Observatory HIRES instrument page. |
| HST: 2.4 m aperture, 57.6 m effective focal length | Lectures 01, 02, 03, 12 | Standard published NASA/STScI mission specification | **Level 2: not independently re-verified this session.** |
| VLT (ESO Unit Telescope): 8.2 m aperture, 120 m effective focal length | Lectures 01, 03, 14; Lab 07 | Standard published ESO facility specification | **Level 2: not independently re-verified this session.** |
| JWST: 6.5 m aperture, 18 segments, 0.6-28.3 &micro;m wavelength coverage, 131.4 m effective focal length | Lectures 01, 03, 12 | Standard published NASA/STScI mission specification | **Level 2: not independently re-verified this session.** |
| DECam: 570-megapixel, 62-CCD mosaic on the 4 m Blanco telescope, 15 &micro;m pixels, 11.28 m effective focal length | Lecture 03; Lab 02 | Standard published NOIRLab/CTIO facility specification | **Level 2: not independently re-verified this session.** |
| e2v CCD231-84-class quantum-efficiency curve (peaking &asymp;96% near 600 nm) | Lecture 04; Lab 03 | Standard published manufacturer specification (e2v/Teledyne datasheet class) | **Level 2: not independently re-verified this session.** |
| Representative modern scientific CCD read noise (3.5 e&#8315; rms), dark current (0.001 e&#8315;/pix/s at -100&deg;C), gain (1.8 e&#8315;/ADU), full well (130,000 e&#8315;) | Lectures 05, 06, 07; Labs 03, 04 | Representative published values for a modern cooled scientific CCD (order-of-magnitude consistent with e2v/Teledyne datasheet-class devices) | **Level 2: not independently re-verified this session.** |
| Johnson-Cousins UBVRI central wavelengths and effective bandwidths | Lecture 08; Lab 04; PS 04 | Bessell, M.S. (1990), *PASP* 102, 1181, "UBVRI Passbands" (standard published photometric-system reference) | **Level 2: not independently re-verified this session.** |
| Landolt standard star SA 98-978: V=9.061, B-V=0.593, U-B=0.048, V-R=0.353, R-I=0.343 | Lecture 07; Lab 04; PS 04 | Landolt, A.U. (1992), *AJ* 104, 340, "UBVRI photometric standard stars" (standard published photometric standard) | **Level 2: not independently re-verified this session.** |
| Keck adaptive optics: representative natural-guide-star residual wavefront errors and K-band Strehl ratios | Lecture 11; Lab 06 | Wizinowich, P. et al. (2000), *PASP* 112, 315, "First Light Adaptive Optics Images from the Keck II Telescope" (standard published performance figures) | **Level 2: not independently re-verified this session.** |
| Gemini North: 8.1 m aperture; Palomar/amateur-class 0.2 m reflector | Lecture 01; PS 01 | Standard published facility specification (Gemini North); a generic representative amateur-telescope aperture (illustrative, not a specific named instrument) | **Level 2 (Gemini) / illustrative representative value (amateur reflector), not a specific catalog entry.** |
| Median atmospheric seeing (0.8&Prime;), dark-site V-band sky brightness (21.5 mag/arcsec&sup2;), V-band zero-point photon flux | Lecture 02, 06, 12, 13; Labs 01, 03 | Standard published order-of-magnitude values representative of a good astronomical site (consistent with Bessell 1998-class photometric calibration literature) | **Level 2: not independently re-verified this session.** |

## Schematic (Illustrative) Approximations

The following are labeled explicitly, in the lecture/lab/problem-set text itself and again here, as illustrative representative values rather than site- or instrument-specific precision figures, and are not to be confused with the real-data provenance table above:

- End-to-end system throughput (60%, Lecture 06 and onward): a representative round-number value for a well-baffled Cassegrain imaging path, not a measured value for any specific Keck instrument configuration.
- HIRES illuminated collimated beam width (20 cm, Lecture 10/Lab 05): a representative value chosen to demonstrate the beam-width resolving-power relation's correct order of magnitude and scaling, not HIRES's exact as-built optical prescription.
- Calibration-frame pixel levels (bias/dark/flat/light ADU values, Lecture 07/Lab 04): illustrative, constructed values consistent with a typical modern CCD's dynamic range, not measurements from a specific real exposure.
- Photometric error-budget terms (flat-field residual, extinction-correction residual, Lecture 13): representative published order-of-magnitude values for a well-calibrated modern imager on a good photometric night, not measurements from a specific real observing run.

## Visuals

Lecture-specific SVG diagrams are generated programmatically per lecture (see `src/generate_astr340_content.py`), including a numerically computed Airy diffraction pattern from a Bessel-function series, published CCD quantum-efficiency and filter-transmission curves, and grating-equation/Strehl-ratio curves; they are schematic/explanatory rather than photographic, so no external image licensing is required. Every lecture's visual-reasoning figure is a structurally distinct diagram (verified via a mechanical grep-based check for repeated SVG coordinate signatures across all 14 lecture files; zero repeats found).

## Human Spot-Check Checklist Before Instructional Release

- [ ] Confirm HIRES's resolving power, groove density, and blaze angle directly against the Keck Observatory HIRES instrument page or Vogt et al. (1994).
- [ ] Confirm HST, VLT, and JWST aperture and focal-length specifications against their respective mission/facility documentation.
- [ ] Confirm DECam's pixel size, CCD count, and megapixel count against NOIRLab/CTIO documentation.
- [ ] Confirm the e2v/Teledyne CCD quantum-efficiency curve against a current manufacturer datasheet for the specific device planned for instructional use.
- [ ] Confirm Johnson-Cousins UBVRI central wavelengths/bandwidths against Bessell (1990) directly.
- [ ] Confirm Landolt standard star SA 98-978's magnitudes against Landolt (1992) directly, or against a current online standard-star catalog.
- [ ] Confirm the representative Keck AO Strehl-ratio figures against Wizinowich et al. (2000) directly, or against current published Keck AO performance data.
- [ ] Verify exact OpenStax Astronomy 2e Chapter 6 section/page numbers against the adopted print or PDF edition, and confirm the several places this course explicitly extends beyond OpenStax's introductory coverage.
