# ASTR 330 Reference Log

Tracks references, datasets, and visuals used in ASTR 330 materials, their verification status, and any human spot-check requirements. Provenance is labeled at one of three explicit levels throughout: **(1) live-verified this session** (fetched/extracted from a primary or authoritative source during this course's production), **(2) standard published/literature value not re-verified this session** (flagged for human spot-check), or **(3) synthetic/instructor-provided placeholder**. No purely synthetic (non-literature) numeric data is used anywhere in this package; every real-world number is either level 1 or level 2. Schematic physics approximations (Kramers opacity coefficient, pp/CNO power-law exponents, mass-core-temperature scaling, white-dwarf cooling-law calibration constant) are explicitly labeled as illustrative order-of-magnitude fits, not precision values, and are distinct from the data-provenance question addressed here.

## Textbook

- OpenStax Astronomy 2e (openly licensed; local extracted copy `references/openstax-astronomy-2e-extracted.txt`; problem index `references/source-indexes/openstax-astronomy-2e-problem-index.md`). Chapter numbers cited in ASTR 330 materials are the **published edition's native chapter numbers**, cross-checked against the local extracted text's own embedded figure/table numbering, following the ASTR 230/ASTR 310 precedent for resolving the source index's internal numbering offset. Status: chapter alignment verified for Chapters 16, 19, 21-23; several ASTR 330 topics (the four-equation stellar-structure system, the equation-of-state/opacity formalism, the radiative-gradient/Schwarzschild-criterion derivation, the Gamow-peak formalism, homology relations and polytropes, the Sch&ouml;nberg-Chandrasekhar limit, the triple-alpha resonance argument, and the Chandrasekhar-mass derivation) are **not covered at the introductory level in OpenStax Astronomy 2e at all** and are developed here from first principles instead; this is stated explicitly in `syllabus.html`, `schedule.html`, and each affected lecture's slides/notes rather than presented as an OpenStax-sourced result.

## Real Data Used in Labs/Problem Sets

| Dataset | Used in | Source | Verification Level |
|---|---|---|---|
| Hyades open cluster: distance 47 pc (153 ly), age 625 Myr, main-sequence turnoff mass 2.3 M&#8857;, total mass 400 M&#8857;, core radius 2.7 pc, half-mass radius 5.7 pc, tidal radius 10 pc, metallicity +0.14 dex | Lectures 07, 09; Lab 05; PS 05 | Wikipedia "Hyades (star cluster)" article, retrieved live this session (2026-09-24), citing Perryman, M.A.C. et al. (1998), *A&A* 331, 81, "The Hyades: distance, structure, dynamics, and age" | **Level 1: live-verified this session.** This is the course's primary real star-cluster dataset. |
| PSR J0348+0432: neutron star mass 2.01 &plusmn; 0.04 M&#8857;, neutron star radius &asymp;13 km, spin period 39.1226563571297 ms, white dwarf companion mass 0.172 M&#8857;, white dwarf radius 0.065 R&#8857;, orbital period 0.102424062722 days, orbital semimajor axis 832,000 km, inclination 40.2&deg;, distance &asymp;2.1 kpc | Lectures 12, 13, 14; Labs 06, 07; PS 06, 07 | Wikipedia "PSR J0348+0432" article, retrieved live this session (2026-09-24), citing Antoniadis, J. et al. (2013), *Science* 340, 1233232, "A Massive Pulsar in a Compact Relativistic Binary" | **Level 1: live-verified this session.** This is the course's primary real compact-remnant (neutron star) dataset. |
| Alpha Centauri A and B: masses, radii, luminosities, temperatures | Lectures 06, 07; Lab 04; PS 01, 02, 03, 04 | Carried forward unchanged from ASTR 310, where they were live-verified via a direct web fetch (citing Akeson et al. 2021, *AJ* 162, 14) | **Level 1, provenance carried forward from ASTR 310.** Not independently re-verified this session; this disclosure is intentional (re-verifying an already-established real dataset would not add information). |
| Sirius A: T_eff = 9,940 K, R = 1.711 R&#8857;, L &asymp; 25.4 L&#8857;, mass &asymp; 2.063 M&#8857; | Lectures 06, 07; Lab 03, 04; PS 04 | Standard Hipparcos-era/visual-binary literature value, carried forward from ASTR 310 | **Level 2: not independently re-verified this session.** Flagged for spot-check against SIMBAD. |
| Sirius B: mass 1.018 M&#8857;, radius 0.008098 R&#8857;, T_eff = 25,000 K | Lectures 11, 12, 13, 14; Lab 06; PS 06 | Live-verified in ASTR 230's production (Bond et al. 2017, *ApJ* 840, 70), carried forward through ASTR 310 and this course with its provenance chain intact | **Level 1, provenance carried forward from ASTR 230.** Not independently re-verified this session; this disclosure is intentional. |
| Standard solar-model core density (&asymp;1.5 &times; 10&#8309; kg/m&sup3;), core temperature (&asymp;1.57 &times; 10&#8309; K), and central pressure (&asymp;2.477 &times; 10&#185;&#8310; Pa) | Lectures 01, 02, 03, 04, 05, 06; Lab 01, 02 | Standard published standard-solar-model literature values, carried forward from ASTR 310 | **Level 2: not independently re-verified this session.** |
| Standard nuclear saturation density (&asymp;2.3 &times; 10&#185;&#8309; kg/m&sup3;) and typical core-collapse supernova observed kinetic-plus-radiated energy (&asymp;10&#8308;&#8308; J) | Lecture 13, 14; Lab 07 | Standard published nuclear-physics and supernova-observation literature values | **Level 2: not independently re-verified this session.** |

## Schematic (Illustrative) Physics Approximations

The following are labeled explicitly, in the lecture/lab/problem-set text itself and again here, as illustrative order-of-magnitude fits rather than precision physical results, and are not to be confused with the real-data provenance table above:

- Kramers opacity-law coefficient (Lecture 02): an illustrative order-of-magnitude coefficient, not a precision OPAL/OP tabulated value.
- pp-chain and CNO-cycle power-law exponents (&epsilon;_pp &prop; T6&#8308;, &epsilon;_CNO &prop; T6&sup2;&#8304;, Lecture 06): standard textbook approximations valid only over a limited temperature range, not exact reaction-network results.
- Mass-to-core-temperature scaling (T_core &prop; M^0.7, Lectures 06, 07, 09) and the fixed n=3.5 mass-luminosity exponent (Lecture 07): approximate scaling relations, whose limitations are discussed explicitly in Lecture 07's pitfall and demonstrated honestly via the Hyades turnoff-age discrepancy (Lecture 09, Lab 05).
- White dwarf cooling-law calibration constant (Lecture 11/Lab 06): a schematic Mestel-type scaling, not a full cooling-track model.

## Synthetic Data

No purely synthetic (non-literature) numeric data is used in ASTR 330; every real-world dataset above is either live-verified this session (level 1), carried forward with established level-1 provenance from a prior course, or a standard published literature value flagged for spot-check (level 2). Physical constants (G, c, h, &#295;, k, &sigma;, m_p, the Thomson cross-section, the n=3 Lane-Emden constant &omega;3&sup0; = 2.018236) are CODATA/standard mathematical-physics values, not independently re-verified this session but not astronomically variable quantities requiring the same spot-check treatment as catalog data.

## Visuals

Lecture-specific SVG diagrams are generated programmatically per lecture (see `src/generate_astr330_content.py`) and are schematic/explanatory rather than photographic; no external image licensing is required.

## Human Spot-Check Checklist Before Instructional Release

- [ ] Confirm the Hyades cluster's distance, age, turnoff mass, total mass, and structural radii against Perryman et al. (1998) directly and against Gaia DR3.
- [ ] Confirm PSR J0348+0432's neutron star and white dwarf masses, radius, and orbital parameters against Antoniadis et al. (2013) directly.
- [ ] Confirm Sirius A's parameters against SIMBAD.
- [ ] Confirm the standard solar-model core density, temperature, and central pressure against a current published standard solar model.
- [ ] Confirm the standard nuclear saturation density and typical core-collapse supernova energy budget against a current published nuclear-physics/supernova reference.
- [ ] Verify exact OpenStax Astronomy 2e section/page numbers against the adopted print or PDF edition, and confirm which topics are correctly documented as extending beyond OpenStax's introductory coverage.
