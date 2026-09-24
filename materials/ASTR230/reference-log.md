# ASTR 230 Reference Log

Tracks references, datasets, and visuals used in ASTR 230 materials, their verification status, and any human spot-check requirements.

## Textbook

- OpenStax Astronomy 2e (openly licensed; local extracted copy `references/openstax-astronomy-2e-extracted.txt`; problem index `references/source-indexes/openstax-astronomy-2e-problem-index.md`). Chapter numbers cited in ASTR 230 materials are the **published edition's native chapter numbers** (verified directly against section headers and figure numbers in the extracted text, e.g. "Figure 18.11", "Table 22.2"), not the source index's internal chapter labels (which run one lower, e.g. index "Chapter 17" = native Chapter 18). Status: verified chapter alignment for Chapters 15-29; human spot-check of exact page/section numbers against the adopted print or PDF edition is still recommended before final instructional release.

## Real Data Used in Labs/Problem Sets

| Dataset | Used in | Source | Verification |
|---|---|---|---|
| Sirius B mass (1.018 &plusmn; 0.011 M&#8857;), radius (0.008098 R&#8857;, 5,634 km), luminosity (0.02448 L&#8857;), temperature (25,000 K), Hipparcos parallax (2.637 pc) | Lecture 07, Lab 04, PS 04 | Bond, H. E. et al. (2017), *ApJ* 840, 70, "The Sirius System and its Astrophysical Puzzles"; Wikipedia "Sirius B" (cites same paper), retrieved live this session | **Verified** via live web fetch this session (2026-09-24). |
| Nearby/bright star sample (Sun, Sirius A, Vega, Rigel, Betelgeuse, Proxima Centauri, Alpha Centauri A, Barnard's Star, Altair, Procyon A, Arcturus, Aldebaran, Pollux, Capella, Fomalhaut, Deneb, Antares, Spica, 61 Cygni A, Wolf 359) with apparent magnitude, parallax/distance, spectral type, approximate T_eff and luminosity | Lecture 01-03, Lab 01, Lab 02, PS 01, PS 02 | Standard Hipparcos/general-catalog literature values (van Leeuwen 2007 revision; SIMBAD) recalled from general astronomical knowledge | **Not independently re-verified by live fetch this session.** Human spot-check against SIMBAD or the Hipparcos/Gaia catalog is required before instructional use; values are individually plausible and internally consistent (e.g., recomputed luminosities from T_eff and radius match quoted absolute magnitudes to the precision used), but exact digits (parallax to 0.01 mas, T_eff to 10 K) should be confirmed. |
| Milky Way rotation curve, flat at ~220-235 km/s from R = 5-25 kpc, Sun at R&#8320; = 8.2 kpc, V&#8320; = 220 km/s | Lecture 10, Lab 05, PS 05 | Representative of published circular-velocity curves, e.g. Eilers, A.-C. et al. (2019), *ApJ* 871, 120; Sofue, Y. (2020); McGaugh (2018) as summarized on Wikipedia "Galaxy rotation curve" (retrieved live this session, general history/values confirmed, but the exact tabulated (R, V) pairs used in Lab 05 are illustrative round numbers consistent with the published flat-curve result, not digitized directly from a single paper's table). | **Partially verified**: the qualitative flat-curve result and approximate normalization (~220 km/s) are confirmed via live fetch; the specific (R, V) data points used for student calculation are instructor-constructed to match that published behavior and should be replaced with digitized values from a single cited source (e.g. Eilers et al. 2019 Table) before instructional release if exact literature fidelity is required. |
| Galaxy morphology: M31 (SA(s)b), M87 (E0/cD), M101 (SAB(rs)cd), M104/Sombrero (SA(s)a, edge-on), M82 (irregular starburst), NGC 1300 (SB(rs)bc, barred spiral) | Lecture 11, Lab 06 | Standard de Vaucouleurs/RC3-style classifications widely reproduced in astronomical references (e.g. NED, SIMBAD) | **Not independently re-verified by live fetch this session.** These are widely reproduced, uncontroversial classifications; human spot-check against NED is recommended before instructional release. |
| Five-cluster Hubble diagram: Virgo (d &asymp; 16.5 Mpc, v &asymp; 1150 km/s), Ursa Major (d &asymp; 210 Mpc, v &asymp; 15,000 km/s), Corona Borealis (d &asymp; 320 Mpc, v &asymp; 21,600 km/s), Bootes (d &asymp; 520 Mpc, v &asymp; 39,300 km/s), Hydra (d &asymp; 190 Mpc, v &asymp; 10,000 km/s) | Lecture 14, Lab 07, PS 07 | Classic pedagogical redshift-distance data set reproduced in many introductory astronomy textbooks (in the tradition of Sandage/Humason cluster-redshift surveys) | **Not independently re-verified by live fetch this session** (the general Hubble-law history and H&#8320; tension values were confirmed via live fetch of Wikipedia "Hubble's law", but the specific cluster table is a standard pedagogical set recalled from general knowledge). Human spot-check against NED or the adopted textbook's own Hubble-diagram figure is required before instructional release; flagged explicitly here rather than presented as an unqualified primary-source table. |

## Synthetic Data

No purely synthetic (non-literature) numeric data is used in ASTR 230; all lab/problem-set numbers are grounded in real literature values or standard published relationships (Stefan-Boltzmann law, mass-luminosity relation, Chandrasekhar limit, Hubble's law), with the caveats above logged for anything not independently re-verified this session.

## Visuals

Lecture-specific SVG diagrams are generated programmatically per lecture (see `src/generate_astr230_content.py`) and are schematic/explanatory rather than photographic; no external image licensing is required. If photographic images of real objects (e.g. HST images of M31, M87, M82) are added in a future revision, they must be logged here with source, creator/institution, license, and access date before use, per the course-materials-review skill.

## Human Spot-Check Checklist Before Instructional Release

- [ ] Confirm nearby/bright star catalog values against SIMBAD or the Gaia DR3 catalog.
- [ ] Replace the Lab 05 rotation-curve data points with digitized values from a single cited source if exact literature fidelity is required for grading.
- [ ] Confirm galaxy morphological classifications against NED.
- [ ] Confirm the five-cluster Hubble diagram data against NED or the adopted textbook's own figure.
- [ ] Confirm exact OpenStax Astronomy 2e chapter/section/page numbers against the adopted print or PDF edition.
