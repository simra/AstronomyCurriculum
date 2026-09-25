# ASTR 472 Reference Log

## Verified readings and sources

| Use | Source | Verification | Scope and caveat |
|---|---|---|---|
| Introductory radio-instrument context | OpenStax, *Astronomy 2e*, §6.4 “Radio Telescopes” and Chapter 6 Exercises; https://openstax.org/books/astronomy-2e/pages/6-4-radio-telescopes | **Level 1, live-verified 2026-09-25**, page fetched and cross-checked against local extracted text | Correct section 6.4; embedded figure captions 6.17–6.22 occur within the section, confirming no chapter-heading numbering offset. Chapter 6 Review Question 15 asks how radio astronomers obtain visible-like resolution; Review Question 23 asks about very-long/very-short-wavelength sources. The source is introductory, not a substitute for derivations here. |
| Textbook H I/pulsar/Doppler context | OpenStax, *Astronomy 2e*, §§5.6, 20.2, 23.4 | **Level 1** local extracted-text spot-check for section labels; §6.4 live page checked | Introductory coverage only. Exact page/figure anchors and adopted-edition exercise numbering require human PDF spot-check before LMS assignment. |
| Interferometry, ALMA frequency, beam, largest-scale, channels | ALMA Science Portal, “ALMA Basics,” https://almascience.nrao.edu/about-alma/alma-basics | **Level 1, live-verified 2026-09-25** | Page states visibility is the Fourier transform of sky brightness, current frequency range about 35-950 GHz, 12-m maximum baseline about 16 km, field of view set by primary beam, largest structure approximately 0.6 lambda/b_min, and channel/sensitivity details. Values can change by observing cycle; check current handbook for proposals. |
| VLA facility and public observing/archive tools | NSF National Radio Astronomy Observatory, Karl G. Jansky VLA, https://science.nrao.edu/facilities/vla | **Level 1, live-verified 2026-09-25** | The official page and linked Observational Status Summary, archive, and calibration resources were inspected. OpenStax §6.4 supplies the 27 x 25-m / 36-km historical textbook description; current setup details should come from the observing cycle's official documentation. |
| Pulsar parameter definitions and catalogue | ATNF Pulsar Catalogue, https://www.atnf.csiro.au/research/pulsar/psrcat/ ; Manchester et al. 2005, AJ 129, 1993, DOI: 10.1086/428488 | **Level 1, live-verified catalogue interface 2026-09-25** | Interface exposes P0, P1, DM, S400, S1400, and derived Age/BSurf/Edot fields. Individual object parameters are not downloaded into this package; query/version must be cited for student archive work. |
| All-sky H I survey and data products | HI4PI Collaboration, 2016, A&A 594, A116, DOI: 10.1051/0004-6361/201629178; https://arxiv.org/abs/1610.06175; CDS catalog J/A+A/594/A116, https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/594/A116 | **Level 1, live-verified 2026-09-25** | The arXiv HTML and CDS ReadMe/catalog were fetched. They identify full-sky FITS cubes, 20-by-20-degree subcubes, spectra and N_HI products; Table 1 reports 16.2 arcmin FWHM, 1.29 km/s channel separation, 1.49 km/s spectral resolution, and about 43 mK RMS. Do not conflate channel separation with spectral resolution. The survey's standard N_HI relation is explicitly optically thin. The separate Bonn portal and A&A publisher fetch returned 403, but the arXiv and CDS primary records were accessible. |
| Real survey and facility comparisons | NRAO archive and VLA Sky Survey (VLASS) pages; Condon et al. 1998, AJ 115, 1693, DOI: 10.1086/300337 (NVSS) | **Level 1 for official archive navigation; level 2 for literature survey specifications** | No raw radio archive files were present in the workspace during production. Students are directed to retrieve real products with release, project identifier, mask, and calibration provenance recorded; bundled compact CSVs are synthetic level-3 teaching records. |

## Tri-level data provenance

- **Level 1, live-verified this session:** the OpenStax section title/embedded figure sequence and exact exercise anchors; ALMA Basics statements listed above; official NRAO VLA page/navigation; ATNF catalogue field definitions; HI4PI paper metadata, Table 1 beam/channel/spectral/noise values, thin-column relation, and CDS product inventory.
- **Level 2, published/literature values not re-verified this session:** historical NVSS and standard object parameters quoted in literature. The Bonn HI4PI portal and A&A publisher page returned 403, but the same paper and product metadata were live-verified through arXiv and CDS. Human spot-check is still required before proposal-grade use of current specifications.
- **Level 3, synthetic/instructor-provided:** `data/continuum_spectrum.csv`, `radiometer_trials.csv`, `uv_samples.csv`, `calibration_records.csv`, `hi_spectrum_teaching.csv`, `pulsar_arrivals.csv`, and `survey_injections.csv`. These are generated teaching tables, not observational records. `radio_facility_reference.csv` keeps cited real specifications separate and marks their level.

## Numbered OpenStax exercise anchors used in problem sets

Each student problem set now includes at least one exact numbered companion exercise, checked against the local extracted OpenStax index. The exercise-type labels below match the index (including the PS05 correction from a misclassified Review Question to Thought Question):

| Problem set | Exact companion anchor(s) | Relevance |
|---|---|---|
| PS01 | Chapter 5, Figuring for Yourself 41; Chapter 6, Review Question 15 | Frequency-to-wavelength conversion; interferometric resolution |
| PS02 | Chapter 6, Review Questions 2 and 15 | Radio spectral window and resolution context |
| PS03 | Chapter 6, Review Question 15 | Baseline/resolution context for visibilities |
| PS04 | Chapter 6, Review Questions 1 and 11 | Instrument chain; radio versus radar observing |
| PS05 | Chapter 20, Review Question 5; Chapter 6, Thought Question 23 | The 21-cm line; radio/far-IR/short-wavelength emission context |
| PS06 | Chapter 23, Figuring for Yourself 42, 43, and 53 | Pulsar rotation speed and pulse-count calculations |
| PS07 | Chapter 20, Review Question 5 and Thought Question 25 | 21-cm formation and using the line to infer gas motion |

The exercise names/numbers and their relevant text are supported by `references/source-indexes/openstax-astronomy-2e-problem-index.md`; chapter 6 numbering was cross-checked against the native chapter marker and embedded figure sequence. Student assignments explicitly state that exercise numbering/page breaks can vary by edition and require instructor spot-check against the adopted print/PDF edition before LMS assignment. The local extraction is an anchor-finding aid, not a substitute for the adopted-edition check.

## Computation and visual provenance

All worked results in the slides, notes, labs, and solution keys are calculated by `src/generate_astr472_package.py` from the shared constants and input records. No radio archive data were present locally. The supplied compact exercise tables are level-3 teaching data; Lab 07 additionally requires retrieving one actual HI4PI 20-degree subcube from the verified CDS release and comparing a real spectrum/column integral, with file-level provenance recorded by the student. The fourteen SVG figures are original and use different geometry and data relations; no external image is embedded, so no third-party visual license is implied.

## Human spot-check before instructional use

1. Spot-check the HI4PI 2016 beam/channel/spectral/noise values and the selected CDS FITS product metadata against the adopted release before instructional use; live verification used arXiv HTML and the CDS catalog/ReadMe, while the Bonn portal and publisher page were blocked (403).
2. Check current VLA/ALMA configuration and band/setup details against the relevant observing-cycle manuals before proposing live observations.
3. Spot-check OpenStax Chapter 6 Review Question numbering against the adopted edition PDF and confirm instructor-selected readings/exercises.
4. Query versioned pulsar catalogue values and NVSS/VLASS completeness/calibration documentation before adding catalog measurements to submitted coursework.
