# ASTR 370 Reference Log

This log records every real dataset, mission fact, and derived-model choice used in ASTR 370, with an explicit tri-level data-provenance label for each entry:

- **Level 1 (live-verified this session):** fetched or extracted directly from a primary/authoritative source during this course's production.
- **Level 2 (standard published, not re-verified this session):** a standard, plausible literature or textbook value, presented from training knowledge but not independently re-fetched this session. Flagged for human spot-check against the named source.
- **Level 3 (synthetic/illustrative/order-of-magnitude):** an instructor-constructed or order-of-magnitude estimate used for a worked example, explicitly not a claimed precise measurement.

## Level 1: Live-Verified This Session

| Dataset | Value(s) used | Primary source (as cited by the fetched page) |
|---|---|---|
| Solar Cycle 25 sunspot numbers | Start Dec 2019; smoothed min SSN 1.8; smoothed max SSN 160.8 (Oct 2024); not-smoothed max SSN 216 (Aug 2024) | SILSO/WDC-SILSO (Royal Observatory of Belgium), via Wikipedia "Solar cycle 25" |
| Carrington Event (1-2 Sept 1859) Dst range | -800 nT (conservative) to -1750 nT | Cliver & Svalgaard (2005, *Solar Phys.* 224, 407); Tsurutani et al. (2003, *J. Geophys. Res.* 108, A7, 1268), via Wikipedia "Carrington Event" |
| Carrington Event CME transit time | 17.6 hours (estimated) | Wikipedia "Carrington Event" (citing historical reconstruction) |
| 2024 Carrington-era magnetometer reanalysis | Field-change rate >700 nT/minute, vs modern 1-in-100-year extreme of 350-400 nT/minute | Beggan, Clarke, Lawrence, Eaton, Williamson, Matsumoto & Hayakawa (2024, *Space Weather* 22, e2023SW003807), via Wikipedia "Carrington Event" |
| Parker Solar Probe mission facts | Launch 12 Aug 2018; perihelion 9.86 R_sun (6.9x10^6 km); record heliocentric speed 191 km/s (690,000 km/h), achieved 24 Dec 2024 | NASA/JHUAPL mission documentation, via Wikipedia "Parker Solar Probe" |

## Level 2: Standard Published, Not Independently Re-Verified This Session

| Dataset | Value(s) used | Standard source |
|---|---|---|
| IAU nominal solar effective temperature | T_eff = 5772 K | IAU nominal solar constants |
| Standard solar model core parameters | T_core=1.57e7 K, rho_core=1.5e5 kg/m^3 | Bahcall et al. standard solar models, cross-checked against helioseismic sound-speed inversions |
| Radiative-convective boundary | r = 0.71 R_sun | Standard helioseismic result |
| Photospheric gas pressure at tau=1 | ~1.25e4 Pa | Stix (2002), *The Sun*, and the VAL semi-empirical atmosphere model |
| Chromosphere/corona characteristic temperatures | T_min~4100 K; T_corona~1.5e6 K; n_corona,base~1e8 cm^-3 | Standard quiet-Sun solar-atmosphere values |
| Large sunspot umbral field strength | ~2800 G | Solanki (2003), *A&A Rev.* 11, 153 |
| Solar Cycle 24 smoothed maximum sunspot number | 116.4 (April 2014) | SILSO, standard published |
| AR 12673 X9.3 flare peak GOES flux | 9.3e-4 W/m^2 (by GOES-class definition) | NOAA SWPC/GOES, standard published |
| 6 Sept 2017 CME LASCO linear speed | 1571 km/s | SOHO/LASCO CDAW catalog, standard published |
| 7-8 Sept 2017 storm Dst minimum | -142 nT | Kyoto WDC/NOAA, standard published |
| Solar wind climatological speed/density | Slow: 400 km/s, 6 cm^-3; Fast: 700 km/s, 3 cm^-3; storm sheath: 800 km/s, 10 cm^-3 | OMNI database climatology, standard published |
| Earth's equatorial dipole field strength | B0 = 3.0e-5 T (30,000 nT) | Standard geomagnetism value (IGRF-era) |

**Human spot-check note:** a direct live web fetch specifically targeting the "Solar storm of September 2017" Wikipedia article was attempted this session and returned an HTTP 404 error; the AR12673/X9.3 flare, CME, and storm values above are therefore level 2 (standard published, not independently re-verified this session via live fetch), not level 1, despite being the course's central running case study. A human should spot-check these specific values against NOAA SWPC's event reports or the CDAW CME catalog directly before instructional use.

## Level 3: Synthetic/Illustrative/Order-of-Magnitude

| Item | Where used | Disclosure |
|---|---|---|
| Representative active-region area/height-scale volume | Lecture 05/Lab 03 flare free-energy estimate | Order-of-magnitude only; not AR12673's actual measured pre-flare volume |
| CME drag-based deceleration functional form (15-hour time constant) | Lecture 07/Lab 04 figure and travel-time comparison | Illustrative exponential-relaxation model calibrated only to roughly reproduce the real observed transit time, not a first-principles drag-force solution |
| Solar interior temperature-vs-radius interpolation | Lecture 01 diagram | Smooth interpolating curve through the two real endpoints (core, photosphere); not a full numerical stellar-structure solution |
| Solar atmosphere height-vs-temperature schematic | Lecture 02 diagram | Illustrative height scale; real chromosphere/transition-region heights vary with solar activity and observing technique |
| Sunspot butterfly diagram | Lecture 03 diagram | Idealized double-cycle schematic, not a plot of a specific real cycle's actual sunspot catalog |
| GOES flare light-curve shape | Lecture 06 diagram | Schematic Neupert-type profile calibrated to the real peak flux and approximate timing; not the flare's actual measured GOES time series |
| Helioseismic p-mode ridge diagram | Lecture 09 diagram | Schematic representative ridge pattern illustrating the real technique, not real GONG/HMI frequency-degree data |
| Satellite orbital-lifetime-vs-altitude scaling | Lecture 13 diagram | Illustrative exponential scaling illustrating a real, well-documented effect (e.g., the Feb 2022 Starlink loss), not a physical atmospheric-density model |
| GIC geoelectric-field sqrt(dB/dt) scaling used in Lab 07/PS 07 | Lecture 14/Lab 07 capstone | A standard, simplified space-weather-engineering approximation; the specific numeric ground-conductivity assumption underlying it is this course's own illustrative choice |

## Visual/Image Assets

All figures in this course are original, programmatically generated SVG diagrams (schematic plots, bar charts, and flowcharts built from the real/level-2/level-3 constants above), not photographic or externally sourced images. No external image licensing review is required for this package.

## Human Spot-Check Checklist Before Instructional Use

- Verify the AR12673/X9.3 flare, CME speed, and storm Dst values directly against NOAA SWPC event archives and the SOHO/LASCO CDAW CME catalog (flagged above as level 2, not live-verified, despite being this course's central case study).
- Verify the Solar Cycle 24 smoothed-maximum sunspot number directly against the SILSO catalogue.
- Verify the sunspot umbral field strength and standard solar-atmosphere pressure/density values against a current solar-physics textbook edition (e.g., Stix, *The Sun*, or an updated equivalent).
- Confirm the OpenStax Astronomy 2e Chapter 15 section/figure numbering against the locally extracted text and the adopted print/PDF edition.
