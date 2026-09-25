"""Lab and problem-set generator for ASTR340.

Depends on the shared constants and page()/CSS helpers in
generate_astr340_content.py so every number here traces back to the same
real telescope/instrument datasets (Keck, HST, VLT, JWST, HIRES, e2v-class
CCD, Johnson-Cousins UBVRI, Keck adaptive optics) used in the paired
lectures. Run with the project interpreter:
    python materials/ASTR340/src/generate_astr340_content.py
    python materials/ASTR340/src/generate_astr340_labs_psets.py
"""
from __future__ import annotations

import math
from html import escape

from generate_astr340_content import (
    CSS, page, li, LAB_DIR, PSET_DIR, DATA_DIR,
    C_LIGHT, H_PLANCK, K_BOLTZMANN, ARCSEC_PER_RAD, NM, UM, MM,
    KECK, HIRES, HST, VLT, JWST, GEMINI, AMATEUR, DECAM,
    CCD_QE_CURVE_NM, CCD_QE_PERCENT, CCD_READ_NOISE_E, CCD_DARK_CURRENT_E_PER_S, CCD_GAIN_E_PER_ADU,
    CCD_FULL_WELL_E, UBVRI, LANDOLT_SA98_978, KECK_AO_WFE_NM, KECK_WAVELENGTH_K_NM, EARTH_SEEING_ARCSEC,
    rayleigh_resolution_rad, rayleigh_resolution_arcsec, plate_scale_arcsec_per_mm, pixel_scale_arcsec,
    photon_energy_j, ccd_snr, exposure_time_for_snr, grating_equation_angle_rad, resolving_power_grating,
    resolving_power_from_beam_width, strehl_ratio_marechal, diffraction_limited_fwhm_arcsec, error_budget_rss,
    V_BAND_NM, V_BAND_M, K_BAND_M,
    KECK_RESOLUTION_V_ARCSEC, HST_RESOLUTION_V_ARCSEC, VLT_RESOLUTION_V_ARCSEC, JWST_RESOLUTION_2UM_ARCSEC,
    AMATEUR_RESOLUTION_V_ARCSEC, KECK_SEEING_LIMITED_FACTOR,
    KECK_PLATE_SCALE_ARCSEC_MM, HST_PLATE_SCALE_ARCSEC_MM, JWST_PLATE_SCALE_ARCSEC_MM, DECAM_PLATE_SCALE_ARCSEC_MM,
    DECAM_PIXEL_SCALE_ARCSEC, DECAM_NYQUIST_PIXEL_SCALE_ARCSEC,
    PHOTON_ENERGY_V_J, PHOTON_ENERGY_V_EV,
    KECK_THROUGHPUT, STAR_V_MAG, V_ZERO_POINT_PHOTON_FLUX_PER_M2_S, STAR_PHOTON_FLUX_PER_M2_S,
    STAR_COUNT_RATE_E_PER_S, SKY_MAG_PER_ARCSEC2_V, SKY_PHOTON_FLUX_PER_M2_S_ARCSEC2, SEEING_APERTURE_ARCSEC2,
    SKY_COUNT_RATE_E_PER_S, EXPOSURE_FOR_SNR100_S, SNR_AT_300S, SNR_AT_30S,
    HIRES_BEAM_WIDTH_M, HIRES_R_FROM_BEAM, HIRES_DELTA_LAMBDA_NM, HIRES_RV_FROM_R,
    STREHL_AT_WFE, KECK_AO_TYPICAL_WFE_NM, KECK_AO_TYPICAL_STREHL, KECK_AO_DIFFRACTION_LIMIT_K_ARCSEC,
    ERR_POISSON_MAG, ERR_FLATFIELD_RESIDUAL_MAG, ERR_EXTINCTION_MAG, TOTAL_PHOTOMETRIC_ERROR_MAG,
    JWST_VS_KECK_RESOLUTION_RATIO,
)

OPENSTAX = 'OpenStax Astronomy 2e (local reference copy: references/openstax-astronomy-2e-extracted.txt), Chapter 6 (astronomical instruments), descriptive only; this course exceeds that introductory treatment throughout.'


def fmt(x, nd=2):
    return f"{x:.{nd}f}"


def problem(i: int, heading: str, body: str, points: int = 15) -> str:
    return f'<article class="problem"><h3>{i}. {escape(heading)} <span class="points">{points} points</span></h3>{body}</article>'


def solution(i: int, heading: str, body: str, rubric) -> str:
    rows = ''.join(f'<tr><td>{escape(k)}</td><td>{v}</td></tr>' for k, v in rubric)
    return (
        f'<article class="problem"><h3>{i}. {escape(heading)}</h3>{body}'
        f'<table><tr><th>Criterion</th><th>Points</th></tr>{rows}</table></article>'
    )


def lab_page(n: int, title: str, focus: str, sections: str) -> str:
    body = f"<header><div><h1>Lab {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header><main>{sections}</main>"
    return page(f'ASTR 340 Lab {n:02d}', body)


def pset_page(n: int, title: str, focus: str, problems_html: str, reading: str) -> str:
    body = f"""<header><div><h1>ASTR 340 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header>
<main><section><h2>Problems</h2>{problems_html}</section>
<section><h2>Due and Scope</h2><p>Submit a complete derivation with equations, units, labeled quantities, and a short narrative interpretation for each problem. Show every step; a correct final number without a visible derivation receives partial credit at most, and quoting a lecture number without adapting it to this problem's specific inputs receives no credit for that step.</p></section>
<section><h2>OpenStax Companion Reading</h2><p>{escape(reading)}</p></section>
<section><h2>References and Data Sources</h2><ul><li>Corresponding lecture slides and notes for this unit.</li><li>{OPENSTAX}.</li><li>Course datasets under <code>materials/ASTR340/data/</code> where referenced above.</li></ul></section>
</main>"""
    return page(f'ASTR 340 Problem Set {n:02d}', body)


def solutions_page(n: int, title: str, solutions_html: str) -> str:
    body = f"<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header><main><section><h2>Worked Solutions</h2>{solutions_html}</section><section><h2>Grading Notes</h2><p>Award full marks for correct method, units, and a numeric result consistent with the arithmetic shown (allow reasonable rounding). Verify that the student re-derives the number for this problem's specific inputs rather than quoting a lecture example without adaptation. Watch specifically for unit-conversion errors (arcsec/radian, nm/m, mm/m) and for comparative-magnitude or comparative-resolution statements given in the wrong direction (e.g., \"finer\" versus \"coarser\" resolution, or \"more\" versus \"less\" light-gathering power) -- these are the most common sources of order-of-magnitude mistakes in this course.</p></section></main>"
    return page(f'ASTR 340 Problem Set {n:02d} Solutions', body)


def assessment_md(n: int, title: str, criteria: list, common_errors: list) -> str:
    crit = '\n'.join(f'- {c}' for c in criteria)
    err = '\n'.join(f'- {e}' for e in common_errors)
    return f"""# Assessment Instructions: Problem Set {n:02d} \u2014 {title}

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the referenced dataset(s) under `materials/ASTR340/data/`.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking number but no visible derivation steps should not. Because this is a 300-level quantitative instrumentation course, full marks require a genuine derivation (not just formula substitution) wherever the problem set asks for one.

## Problem-Level Criteria
{crit}

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
{err}
"""


# ===========================================================================
# LAB 01: Diffraction-limited resolution across five real telescopes
# ===========================================================================
def make_lab_01() -> str:
    scopes = [KECK, HST, VLT, JWST, AMATEUR]
    rows = ''
    for s in scopes:
        wl = 2.0 * UM if s is JWST else V_BAND_M
        theta = rayleigh_resolution_arcsec(wl, s['aperture_m'])
        rows += f"<tr><td>{escape(s['name'])}</td><td>{s['aperture_m']:.2f}</td><td>{'2.0 &micro;m' if s is JWST else 'V (551 nm)'}</td><td>{theta*1000:.2f}</td></tr>"
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This is a data-analysis lab using the Rayleigh-criterion resolution relation of Lecture 02 applied to five real telescopes' published apertures (Keck, HST, VLT, JWST, and a small amateur reflector). No telescope time is required.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Telescope</th><th>Aperture (m)</th><th>Reference wavelength</th><th>Rayleigh resolution (mas)</th></tr></thead><tbody>{rows}</tbody></table>
<p>Keck's aperture, collecting area, and focal length are live-verified this session (Wikipedia, "W. M. Keck Observatory," 2026-09-24); HST, VLT, and JWST apertures are standard published mission/facility specifications (level 2, see <code>../reference-log.md</code>).</p></section>
<section><h2>Procedure</h2><ol>
<li>For each telescope in the data table, compute the Rayleigh-criterion angular resolution &theta; = 1.22&lambda;/D at the stated reference wavelength, converting from radians to milliarcseconds, and confirm your value against the table.</li>
<li>Compute the ratio of Keck's V-band resolution to the amateur telescope's V-band resolution, and state how many times finer Keck's diffraction limit is.</li>
<li>Compute the ratio of the median atmospheric seeing ({EARTH_SEEING_ARCSEC:.1f}&Prime;) to Keck's V-band diffraction limit, and state what this ratio means physically for an uncorrected (non-adaptive-optics) Keck image.</li>
<li>JWST observes at 2.0 &micro;m rather than V band because its primary science targets (distant galaxies, cool sources) emit most strongly in the infrared and because Earth's atmosphere, irrelevant for a space telescope, would otherwise block much of this range. Using JWST's and Keck's apertures and the wavelength ratio (2.0 &micro;m vs. 551 nm), compute the ratio of their diffraction limits and state which is sharper.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly why the amateur telescope's poor diffraction-limited resolution is essentially irrelevant in practice: an uncorrected ground-based image is normally seeing-limited (Lecture 02), so the amateur telescope's real-world image quality is not much worse than Keck's uncorrected image quality, even though Keck's theoretical diffraction limit is dramatically finer.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed resolution table with independently reproduced arithmetic for all five telescopes.</li><li>The Keck-to-amateur and seeing-to-Keck ratio calculations with interpretation.</li><li>The JWST-versus-Keck diffraction-limit comparison with a stated conclusion.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct unit conversions (radians to milliarcseconds) in all five resolution calculations.</li><li>Correct ratio arithmetic and correctly stated direction (finer vs. coarser) for both ratios.</li><li>Correct, quantitatively supported JWST-versus-Keck conclusion.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Keck aperture/collecting area/focal length: live-verified this session (Wikipedia, "W. M. Keck Observatory"); HST, VLT, JWST apertures: standard published mission/facility specifications, not independently re-verified this session; see <code>materials/ASTR340/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR340/src/generate_astr340_content.py</code>.</li></ul></section>
"""
    return lab_page(1, 'Diffraction-Limited Resolution Across Five Real Telescopes',
                     'Apply the Rayleigh criterion to Keck, HST, VLT, JWST, and an amateur reflector, and compare to the atmospheric seeing floor.', sections)


# ===========================================================================
# LAB 02: Plate scale, pixel scale, and Nyquist sampling
# ===========================================================================
def make_lab_02() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes the plate scale and pixel scale of several real telescope/instrument combinations (Lecture 03) and checks each against the Nyquist sampling criterion using the resolution limits derived in Lab 01.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Telescope</th><th>Focal length (m)</th><th>Plate scale (arcsec/mm)</th></tr></thead><tbody>
<tr><td>Keck</td><td>{KECK['focal_length_m']:.1f}</td><td>{KECK_PLATE_SCALE_ARCSEC_MM:.3f}</td></tr>
<tr><td>HST</td><td>{HST['focal_length_m']:.1f}</td><td>{HST_PLATE_SCALE_ARCSEC_MM:.3f}</td></tr>
<tr><td>JWST</td><td>{JWST['focal_length_m']:.1f}</td><td>{JWST_PLATE_SCALE_ARCSEC_MM:.3f}</td></tr>
<tr><td>DECam host (Blanco 4m)</td><td>{DECAM['focal_length_m']:.2f}</td><td>{DECAM_PLATE_SCALE_ARCSEC_MM:.3f}</td></tr>
</tbody></table>
<p>DECam's published pixel size is {DECAM['pixel_size_um']:.0f} &micro;m; the camera is a 570-megapixel, 62-CCD mosaic (standard published facility specification, level 2).</p></section>
<section><h2>Procedure</h2><ol>
<li>Using s = 206265&Prime;/f[mm], independently reproduce the plate scale for all four telescopes in the data table.</li>
<li>Compute DECam's pixel scale (arcsec/pixel) from its plate scale and {DECAM['pixel_size_um']:.0f} &micro;m pixel size, and confirm it against the published value of {DECAM_PIXEL_SCALE_ARCSEC:.3f} arcsec/pixel.</li>
<li>The Blanco 4m telescope (DECam's host) is a seeing-limited, ground-based facility with typical seeing of about 1.0&Prime;. Apply the Nyquist criterion (pixel scale &le; FWHM/2) to determine whether DECam's pixel scale adequately samples this typical seeing disk.</li>
<li>Suppose DECam's pixel scale were instead used on Keck (an entirely hypothetical combination). Using Keck's much finer diffraction-limited resolution from Lab 01, determine whether this pixel scale would undersample, adequately sample, or oversample Keck's diffraction limit, and explain why an instrument built for Keck would need substantially smaller pixels (or a longer focal length) than DECam's.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly why plate scale depends only on focal length, not aperture, and why this means two telescopes of very different aperture (e.g., Keck and the Blanco 4m) can in principle share very similar plate scales if their focal lengths happen to be similar, even though their light-gathering power and diffraction limits differ enormously.</p></section>
<section><h2>Deliverables</h2><ul><li>Independently reproduced plate-scale table.</li><li>DECam pixel-scale derivation and confirmation.</li><li>Both Nyquist-sampling checks (DECam on its own host telescope, and the hypothetical DECam-on-Keck combination) with explicit conclusions.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct plate-scale arithmetic for all four telescopes.</li><li>Correct pixel-scale derivation matching the published DECam value.</li><li>Correct Nyquist-criterion application and conclusion in both sampling checks.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>DECam pixel size, CCD count, and megapixel count: standard published facility specifications (NOIRLab/CTIO), not independently re-verified this session; Keck, HST, JWST focal lengths: standard published mission/facility specifications; see <code>materials/ASTR340/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR340/src/generate_astr340_content.py</code>.</li></ul></section>
"""
    return lab_page(2, 'Plate Scale, Pixel Scale, and the Nyquist Sampling Criterion',
                     'Compute plate scale and pixel scale for four real telescope/instrument combinations and check Nyquist sampling.', sections)


# ===========================================================================
# LAB 03: CCD signal-to-noise and exposure-time planning
# ===========================================================================
def make_lab_03() -> str:
    t_snr50 = exposure_time_for_snr(50.0, STAR_COUNT_RATE_E_PER_S, SKY_COUNT_RATE_E_PER_S, CCD_DARK_CURRENT_E_PER_S, CCD_READ_NOISE_E)
    fainter_rate = STAR_COUNT_RATE_E_PER_S * 10 ** (-0.4 * 2.0)  # 2 magnitudes fainter
    t_snr50_fainter = exposure_time_for_snr(50.0, fainter_rate, SKY_COUNT_RATE_E_PER_S, CCD_DARK_CURRENT_E_PER_S, CCD_READ_NOISE_E)
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab builds a small exposure-time calculator using the CCD signal-to-noise equation of Lecture 06, applied to the Keck aperture and a representative modern CCD, for a range of target magnitudes.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Keck collecting area, system throughput</td><td>{KECK['collecting_area_m2']:.0f} m&sup2;, {KECK_THROUGHPUT*100:.0f}%</td></tr>
<tr><td>Representative CCD read noise, dark current</td><td>{CCD_READ_NOISE_E:.1f} e&#8315; rms, {CCD_DARK_CURRENT_E_PER_S:.3f} e&#8315;/pix/s</td></tr>
<tr><td>V-band zero-point photon flux (standard published)</td><td>{V_ZERO_POINT_PHOTON_FLUX_PER_M2_S:.2e} photons/m&sup2;/s</td></tr>
<tr><td>Dark-site V-band sky brightness (standard published)</td><td>{SKY_MAG_PER_ARCSEC2_V:.1f} mag/arcsec&sup2;</td></tr>
<tr><td>V={STAR_V_MAG:.0f} target: source count rate, sky count rate</td><td>{STAR_COUNT_RATE_E_PER_S:.3f} e&#8315;/s, {SKY_COUNT_RATE_E_PER_S:.3f} e&#8315;/s</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using the CCD equation, independently reproduce the SNR at 30 s and 300 s for the V={STAR_V_MAG:.0f} target (Lecture 06), and confirm your values against {SNR_AT_30S:.1f} and {SNR_AT_300S:.1f}.</li>
<li>Solve (by bisection or trial and error) for the exposure time reaching SNR=50 for the same V={STAR_V_MAG:.0f} target, and confirm your value against {t_snr50:.0f} s.</li>
<li>Repeat step 2 for a target 2 magnitudes fainter (V={STAR_V_MAG+2.0:.0f}), and compute the ratio of the two exposure times.</li>
<li>State whether the ratio you found in step 3 is closer to the factor expected in the read-noise-limited regime (SNR &prop; t, so ratio &asymp; flux ratio) or the background/source-limited regime (SNR &prop; &radic;t, so ratio &asymp; flux ratio squared), and justify your answer using the actual source and sky count rates in the data table.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The V-band zero-point photon flux and sky-brightness values used here are standard published order-of-magnitude values (Bessell 1998-class calibration), not independently re-verified this session; state explicitly why a real observing proposal would need site- and instrument-specific values (from an actual exposure-time calculator) rather than these representative figures.</p></section>
<section><h2>Deliverables</h2><ul><li>Independently reproduced SNR values at 30 s and 300 s.</li><li>The SNR=50 exposure-time solutions for both target magnitudes.</li><li>The exposure-time ratio with an explicit read-noise-limited-versus-background-limited classification.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct reproduction of the CCD-equation SNR values.</li><li>Correct bisection or iterative solution for both SNR=50 exposure times.</li><li>Correct regime classification supported by the actual count-rate numbers, not a guess.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>V-band zero-point flux and sky brightness: standard published order-of-magnitude values, not independently re-verified this session; Keck collecting area live-verified this session; see <code>materials/ASTR340/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR340/src/generate_astr340_content.py</code>.</li></ul></section>
"""
    return lab_page(3, 'Building a CCD Exposure-Time Calculator',
                     'Apply the CCD signal-to-noise equation to plan real exposure times for targets of different brightness with Keck.', sections)


# ===========================================================================
# LAB 04: Photometric calibration and zero point
# ===========================================================================
def make_lab_04() -> str:
    illustrative_rate = STAR_COUNT_RATE_E_PER_S * 20.0
    zp = LANDOLT_SA98_978['V'] + 2.5 * math.log10(illustrative_rate)
    target_rate = STAR_COUNT_RATE_E_PER_S
    target_mag = -2.5 * math.log10(target_rate) + zp
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab performs a calibration-frame reduction sequence (Lecture 07) and derives a photometric zero point from a real Landolt standard star (Lecture 08), then applies it to recover an unknown target's calibrated V magnitude.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Frame / quantity</th><th>Representative value</th></tr></thead><tbody>
<tr><td>Bias frame (mean level)</td><td>400 ADU</td></tr>
<tr><td>Dark frame, matched 300 s exposure (mean level)</td><td>480 ADU</td></tr>
<tr><td>Normalized flat-field frame (mean)</td><td>1.000 (by construction)</td></tr>
<tr><td>Raw light frame, standard star SA 98-978 (mean, 300 s)</td><td>{illustrative_rate*300/CCD_GAIN_E_PER_ADU:.0f} ADU</td></tr>
<tr><td>Raw light frame, science target (mean, 300 s)</td><td>{target_rate*300/CCD_GAIN_E_PER_ADU:.0f} ADU</td></tr>
<tr><td>SA 98-978 published V magnitude (Landolt 1992)</td><td>{LANDOLT_SA98_978['V']:.3f}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using I_cal=(raw-D)/F (matched-exposure master-dark workflow, Lecture 07), compute the calibrated ADU level for both the standard-star frame and the science-target frame from the data table.</li>
<li>Convert each calibrated ADU level to an electron count rate using the representative gain g={CCD_GAIN_E_PER_ADU:.1f} e&#8315;/ADU and the 300 s exposure time.</li>
<li>Using SA 98-978's published V={LANDOLT_SA98_978['V']:.3f} magnitude and its measured count rate, solve for the night's photometric zero point Z_pt via m=-2.5log&#8321;&#8320;(counts/s)+Z_pt.</li>
<li>Apply the zero point from step 3 to the science target's measured count rate to compute its calibrated V magnitude, and confirm your value is consistent with {target_mag:.3f}.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly what would happen to the derived zero point, and therefore to every target magnitude computed from it that same night, if the flat-field frame used in step 1 had a mean far from 1.0 rather than being properly normalized (Lecture 07's flat-field pitfall).</p></section>
<section><h2>Deliverables</h2><ul><li>Both calibrated ADU-to-count-rate conversions.</li><li>The derived zero point with full substituted values.</li><li>The recovered science-target V magnitude.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct calibration-equation application (matched-exposure dark workflow, not double bias subtraction).</li><li>Correct gain conversion and zero-point derivation.</li><li>Correct final target magnitude consistent with the worked value.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>SA 98-978 UBVRI magnitudes: standard published Landolt (1992) photometric standard-star values, not independently re-verified this session; calibration-frame ADU levels are illustrative/synthetic, matching this course's Lecture 07 worked example; see <code>materials/ASTR340/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR340/src/generate_astr340_content.py</code>.</li></ul></section>
"""
    return lab_page(4, 'Photometric Calibration and Zero-Point Derivation',
                     'Reduce calibration frames, derive a zero point from a real Landolt standard star, and recover a target\u2019s calibrated V magnitude.', sections)


# ===========================================================================
# LAB 05: Grating equation and HIRES resolving power
# ===========================================================================
def make_lab_05() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab applies the grating equation (Lecture 09) and the resolving-power relations (Lecture 10) to Keck's HIRES echelle spectrograph, using its published groove density, blaze angle, and resolving power.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>HIRES published resolving power</td><td>R &asymp; {HIRES['resolving_power']:,}</td></tr>
<tr><td>HIRES groove density, blaze angle</td><td>{HIRES['groove_density_per_mm']:.2f} grooves/mm, {HIRES['blaze_angle_deg']:.0f}&deg;</td></tr>
<tr><td>Representative illuminated beam width</td><td>{HIRES_BEAM_WIDTH_M*100:.0f} cm</td></tr>
<tr><td>HIRES published radial-velocity precision, 1 AU detection limit</td><td>{HIRES['rv_precision_ms']:.1f} m/s, {HIRES['detection_limit_mj_at_1au']:.1f} M_Jup</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using R = 2W tan(&theta;_B)/&lambda; with the representative beam width and HIRES's blaze angle, compute the predicted resolving power at V band, and compare it (percent difference) to the published R&asymp;67,000.</li>
<li>Using &Delta;&lambda; = &lambda;/R at V band, compute HIRES's minimum resolvable wavelength interval, in picometers.</li>
<li>Using &Delta;v/c = 1/R, compute the velocity-resolution element corresponding to HIRES's resolving power, in km/s, and compare it to HIRES's published {HIRES['rv_precision_ms']:.1f} m/s radial-velocity precision.</li>
<li>Explain, using the distinction between resolving a single spectral line and centroiding many lines simultaneously, why HIRES's actual radial-velocity precision is roughly four orders of magnitude finer than the single-line velocity-resolution element computed in step 3.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The beam-width-derived resolving power in step 1 is not expected to exactly match the published value, because the representative beam width used is illustrative rather than HIRES's exact as-built optical prescription; state explicitly why this is an acceptable limitation for demonstrating the correct scaling relation but would not be acceptable for precision instrument design.</p></section>
<section><h2>Deliverables</h2><ul><li>The beam-width-derived resolving power with percent-difference comparison to the published value.</li><li>The minimum resolvable wavelength interval.</li><li>The velocity-resolution element and its comparison to HIRES's published precision, with a written explanation of the four-order-of-magnitude gap.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct beam-width resolving-power arithmetic and percent-difference comparison.</li><li>Correct &Delta;&lambda; and &Delta;v arithmetic with correct units.</li><li>Correct, physically grounded explanation of the single-line-versus-many-line precision gap.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>HIRES radial-velocity precision and 1 AU detection limit: live-verified this session (Wikipedia, "W. M. Keck Observatory," 2026-09-24); HIRES resolving power, groove density, and blaze angle: standard published instrument specifications (Vogt et al. 1994), not independently re-verified this session; see <code>materials/ASTR340/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR340/src/generate_astr340_content.py</code>.</li></ul></section>
"""
    return lab_page(5, 'The Grating Equation and HIRES\u2019s Resolving Power',
                     'Recompute Keck HIRES\u2019s resolving power from its published groove density and blaze angle, and derive its velocity-resolution element.', sections)


# ===========================================================================
# LAB 06: Adaptive optics Strehl ratio
# ===========================================================================
def make_lab_06() -> str:
    strehl_v = strehl_ratio_marechal(KECK_AO_TYPICAL_WFE_NM * NM, V_BAND_M)
    rows = ''.join(f"<tr><td>{wfe:.0f}</td><td>{s:.3f}</td></tr>" for wfe, s in STREHL_AT_WFE)
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab applies the Mar\u00e9chal approximation (Lecture 11) to representative Keck natural-guide-star adaptive optics residual wavefront errors, computing Strehl ratios at K band and V band.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Residual wavefront error &sigma; (nm)</th><th>Strehl ratio at K band ({KECK_WAVELENGTH_K_NM:.0f} nm)</th></tr></thead><tbody>{rows}</tbody></table>
<p>Values are representative published Keck natural-guide-star AO performance figures (Wizinowich et al. 2000), not independently re-verified this session.</p></section>
<section><h2>Procedure</h2><ol>
<li>Using S = exp[-(2&pi;&sigma;/&lambda;)&sup2;], independently reproduce the Strehl ratio at K band for &sigma;={KECK_AO_TYPICAL_WFE_NM:.0f} nm, and confirm your value against {KECK_AO_TYPICAL_STREHL:.3f}.</li>
<li>Recompute the Strehl ratio for the same &sigma;={KECK_AO_TYPICAL_WFE_NM:.0f} nm at V band ({V_BAND_NM:.0f} nm) instead of K band, and confirm your value against {strehl_v:.4f}.</li>
<li>Using Keck's aperture and the diffraction-limited FWHM relation (FWHM&asymp;1.03&lambda;/D), compute Keck's diffraction-limited K-band FWHM, and compare it qualitatively to the AO-corrected image expected at Strehl={KECK_AO_TYPICAL_STREHL:.2f}.</li>
<li>Using your two Strehl-ratio results (steps 1-2), explain quantitatively why natural-guide-star adaptive optics historically targets near-infrared science cases rather than visible-light imaging, for the same physical AO correction hardware.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly that a Strehl ratio below 1.0, even at K band, means the AO-corrected image still contains a broader residual halo in addition to a sharper diffraction-limited core, and that this course's single representative &sigma; value does not capture how AO performance varies with atmospheric conditions, guide-star brightness, and target elevation on a real night.</p></section>
<section><h2>Deliverables</h2><ul><li>Both independently reproduced Strehl-ratio calculations (K band and V band).</li><li>The diffraction-limited K-band FWHM calculation.</li><li>A written explanation of the near-infrared AO preference, quantitatively grounded in the two Strehl-ratio results.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct Mar\u00e9chal-approximation arithmetic at both wavelengths.</li><li>Correct diffraction-limited FWHM arithmetic.</li><li>Correct, quantitatively grounded explanation of the near-infrared AO preference.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Keck AO residual wavefront-error/Strehl-ratio figures: standard published values (Wizinowich et al. 2000), not independently re-verified this session; Keck aperture live-verified this session; see <code>materials/ASTR340/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR340/src/generate_astr340_content.py</code>.</li></ul></section>
"""
    return lab_page(6, 'Adaptive Optics Strehl Ratios at K Band and V Band',
                     'Apply the Mar\u00e9chal approximation to representative Keck AO wavefront-error data and explain the near-infrared AO preference.', sections)


# ===========================================================================
# LAB 07: Capstone -- instrument proposal design and error budget
# ===========================================================================
def make_lab_07() -> str:
    area_ratio = (VLT['aperture_m'] / KECK['aperture_m']) ** 2
    t_snr100_vlt = exposure_time_for_snr(100.0, STAR_COUNT_RATE_E_PER_S * area_ratio, SKY_COUNT_RATE_E_PER_S * area_ratio,
                                          CCD_DARK_CURRENT_E_PER_S, CCD_READ_NOISE_E)
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This capstone lab requires students to write a short, quantitatively justified instrument or observing proposal synthesizing at least three of the preceding six labs' tools (resolution, sampling, SNR/exposure time, calibration, spectral resolving power, or Strehl ratio) for a self-chosen, instructor-approved real science scenario, following Lecture 14's proposal-design framework.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Keck exposure time for SNR=100 on the V={STAR_V_MAG:.0f} worked scenario</td><td>{EXPOSURE_FOR_SNR100_S:.0f} s</td></tr>
<tr><td>Equivalent VLT-class (8.2 m) exposure time for the same SNR</td><td>{t_snr100_vlt:.0f} s</td></tr>
<tr><td>Total photometric error budget for the 300 s Keck scenario</td><td>{TOTAL_PHOTOMETRIC_ERROR_MAG*1000:.2f} mmag (Poisson {ERR_POISSON_MAG*1000:.2f}, flat-field {ERR_FLATFIELD_RESIDUAL_MAG*1000:.1f}, extinction {ERR_EXTINCTION_MAG*1000:.1f})</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>State a specific, one-sentence science requirement for a self-chosen real science scenario (e.g., detecting a specific magnitude change, resolving a specific angular separation, or measuring a specific radial-velocity amplitude).</li>
<li>Using at least three of this course's quantitative tools (Rayleigh criterion, plate scale/Nyquist sampling, CCD SNR equation, calibration/zero point, grating equation/resolving power, or Strehl ratio), work backward from the science requirement to a specific telescope, instrument configuration, and exposure time or observing strategy.</li>
<li>Construct an explicit root-sum-square error budget (Lecture 13) for the proposed measurement, naming every relevant error term and identifying the dominant one.</li>
<li>Using the worked Keck-versus-VLT-class exposure-time comparison in the data table as a model, compare at least two credible telescope/instrument alternatives for your proposal, and justify your final recommendation quantitatively rather than by assertion.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Explicitly state which of this proposal's inputs are live-verified real data, which are standard published values not independently re-verified this session, and which are simplifying assumptions (e.g., a representative rather than site-specific sky brightness or throughput), following this course's tri-level provenance standard.</p></section>
<section><h2>Deliverables</h2><ul><li>A one-paragraph science requirement statement.</li><li>A quantitative technical justification connecting that requirement to a specific telescope, instrument, and exposure time, using at least three of this course's tools.</li><li>An explicit RSS error budget with the dominant term identified.</li><li>A two-alternative trade-space comparison with a justified final recommendation.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Clear, specific, one-sentence science requirement.</li><li>Correct, internally consistent use of at least three course tools to justify the proposed configuration.</li><li>Correctly constructed RSS error budget with a correctly identified dominant term.</li><li>Quantitatively (not qualitatively) justified trade-space recommendation.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>All quantities in the data table are computed programmatically in <code>materials/ASTR340/src/generate_astr340_content.py</code> from this course's established real and standard-published datasets; see <code>materials/ASTR340/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR340/src/generate_astr340_labs_psets.py</code>.</li></ul></section>
"""
    return lab_page(7, 'Capstone: Instrument Proposal Design and Error Budget',
                     'Synthesize this course\u2019s toolkit into a quantitatively justified instrument or observing proposal with an explicit error budget.', sections)


LAB_BUILDERS = [make_lab_01, make_lab_02, make_lab_03, make_lab_04, make_lab_05, make_lab_06, make_lab_07]


def write_labs():
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    for i, builder in enumerate(LAB_BUILDERS, start=1):
        (LAB_DIR / f'lab-{i:02d}.html').write_text(builder(), encoding='utf-8')


# ===========================================================================
# PROBLEM SETS
# ===========================================================================
def build_ps01():
    title = 'Aperture, Collecting Area, and Diffraction-Limited Resolution'
    reading = f'{OPENSTAX}'
    p1 = problem(1, 'Collecting area',
                 f"<p>Compute Gemini North's collecting area (D={GEMINI['aperture_m']:.1f} m) from A=&pi;D&sup2;/4, and compute its ratio to Keck's published collecting area ({KECK['collecting_area_m2']:.0f} m&sup2;).</p>", points=20)
    p2 = problem(2, 'Rayleigh criterion at a new wavelength',
                 f"<p>Compute Keck's Rayleigh-criterion resolution at H band (1.65 &micro;m) rather than V band, and compare it to Keck's V-band resolution ({KECK_RESOLUTION_V_ARCSEC*1000:.1f} mas, Lecture 02/Lab 01).</p>")
    p3 = problem(3, 'Seeing-limited versus diffraction-limited',
                 f"<p>Using the atmospheric seeing floor ({EARTH_SEEING_ARCSEC:.1f}&Prime;) and your Problem 2 H-band diffraction limit, state whether an uncorrected Keck H-band image would be seeing-limited or diffraction-limited, and justify your answer with the specific ratio.</p>")
    p4 = problem(4, 'Cassegrain focal-station reasoning',
                 "<p>Explain, using the observing-chain picture from Lecture 01, why an instrument requiring a large, heavy cryostat (e.g., a near-infrared spectrograph) is more often placed at a Nasmyth or Coud\u00e9 focus than directly at the Cassegrain focus, in terms of the mechanical weight and space constraints at each focal station.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    area_ratio = (math.pi * GEMINI['aperture_m'] ** 2 / 4) / KECK['collecting_area_m2']
    h_band_res = rayleigh_resolution_arcsec(1.65 * UM, KECK['aperture_m'])
    seeing_ratio = EARTH_SEEING_ARCSEC / h_band_res
    sol1 = solution(1, 'Collecting area', f"<p>A_Gemini = &pi;({GEMINI['aperture_m']:.1f})&sup2;/4 = {math.pi*GEMINI['aperture_m']**2/4:.1f} m&sup2;. Ratio to Keck: {area_ratio:.3f} -- Gemini North's collecting area is somewhat smaller than Keck's, consistent with its slightly smaller 8.1 m aperture.</p>", [('Correct area arithmetic', 10), ('Correct ratio and direction', 10)])
    sol2 = solution(2, 'Rayleigh criterion at H band', f"<p>&theta;_H = 1.22&times;1.65&micro;m/10m = {h_band_res*1000:.1f} mas, coarser than the V-band value ({KECK_RESOLUTION_V_ARCSEC*1000:.1f} mas), consistent with the direct proportionality of resolution to wavelength.</p>", [('Correct arithmetic', 10), ('Correct direction (coarser at longer wavelength)', 5)])
    sol3 = solution(3, 'Seeing-limited versus diffraction-limited', f"<p>Ratio = {EARTH_SEEING_ARCSEC:.1f}&Prime;/{h_band_res:.4f}&Prime; = {seeing_ratio:.0f} -- still far larger than 1, so an uncorrected Keck H-band image remains strongly seeing-limited, not diffraction-limited, even though the gap is smaller than at V band.</p>", [('Correct ratio', 8), ('Correct seeing-limited conclusion', 7)])
    sol4 = solution(4, 'Focal-station reasoning', "<p>The Cassegrain focus is compact but mass- and space-constrained (it moves with the telescope through its full range of motion); Nasmyth and Coud\u00e9 foci route light to a stationary or slower-moving platform with far more room and weight capacity for large cryostats, optical benches, and vibration-sensitive components, which is why the heaviest instruments are placed there rather than at Cassegrain.</p>", [('Correct identification of the weight/space trade-off', 12), ('Correct connection to instrument type', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = ['Problem 1: 20 points \u2014 correct area and ratio arithmetic.', 'Problem 2: 15 points \u2014 correct H-band resolution and direction.',
                'Problem 3: 15 points \u2014 correct ratio and seeing-limited conclusion.', 'Problem 4: 20 points \u2014 correct focal-station reasoning connected to instrument mass/space constraints.']
    common_errors = ['Forgetting that resolution is directly (not inversely) proportional to wavelength.', 'Confusing collecting area (D\u00b2) scaling with resolution (D\u207b\u00b9) scaling.', 'Asserting a focal-station preference without the weight/space justification.']
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps02():
    title = 'Plate Scale and Nyquist Sampling for a New Instrument'
    reading = f'{OPENSTAX}'
    f_new = 25.0
    scale_new = plate_scale_arcsec_per_mm(f_new)
    pix_new = pixel_scale_arcsec(f_new, 12.0)
    p1 = problem(1, 'Plate scale for a new focal length',
                 f"<p>A proposed new Keck instrument uses a re-imaging focal length of f={f_new:.1f} m (different from Keck's native {KECK['focal_length_m']:.1f} m Cassegrain focus). Compute its plate scale in arcsec/mm.</p>", points=20)
    p2 = problem(2, 'Pixel scale for a 12 &micro;m detector',
                 f"<p>Using your Problem 1 plate scale and a 12 &micro;m pixel detector, compute the pixel scale in arcsec/pixel.</p>")
    p3 = problem(3, 'Nyquist check against Keck AO',
                 f"<p>Keck's AO-corrected K-band diffraction-limited FWHM is {KECK_AO_DIFFRACTION_LIMIT_K_ARCSEC*1000:.1f} mas (Lecture 11). Determine whether your Problem 2 pixel scale adequately Nyquist-samples this FWHM, or whether it under- or oversamples it.</p>")
    p4 = problem(4, 'Design trade-off',
                 "<p>If the Problem 2 pixel scale underscamples Keck's AO-corrected diffraction limit, propose one specific design change (to focal length, pixel size, or both) that would bring the instrument to adequate Nyquist sampling, and show the resulting pixel scale numerically.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    ratio = pix_new / (KECK_AO_DIFFRACTION_LIMIT_K_ARCSEC / 2.0)
    f_fix = f_new * ratio if ratio > 1 else f_new
    pix_fix = pixel_scale_arcsec(f_fix, 12.0)
    sol1 = solution(1, 'Plate scale', f"<p>s = 206265/({f_new:.1f}&times;1000) = {scale_new:.4f} arcsec/mm.</p>", [('Correct formula application', 10), ('Correct final value', 10)])
    sol2 = solution(2, 'Pixel scale', f"<p>Pixel scale = {scale_new:.4f}&times;0.012 mm = {pix_new*1000:.2f} milliarcsec/pixel.</p>", [('Correct unit conversion (&micro;m to mm)', 8), ('Correct final value', 7)])
    sol3 = solution(3, 'Nyquist check', f"<p>Half the diffraction-limited FWHM is {KECK_AO_DIFFRACTION_LIMIT_K_ARCSEC*500:.2f} mas; the Problem 2 pixel scale ({pix_new*1000:.2f} mas/pixel) is {'larger (undersampled)' if pix_new*1000 > KECK_AO_DIFFRACTION_LIMIT_K_ARCSEC*500 else 'smaller (adequately sampled)'} than this Nyquist limit.</p>", [('Correct half-FWHM computation', 8), ('Correct undersampled/adequate classification', 7)])
    sol4 = solution(4, 'Design fix', f"<p>Increasing the focal length to about {f_fix:.1f} m (proportionally increasing plate scale's denominator) brings the pixel scale down to about {pix_fix*1000:.2f} mas/pixel, adequately sampling the diffraction limit; equivalently, a smaller pixel size at the original focal length would achieve the same result.</p>", [('Correct identification of focal length or pixel size as the lever', 12), ('Correct resulting numeric pixel scale', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = ['Problem 1: 20 points.', 'Problem 2: 15 points.', 'Problem 3: 15 points \u2014 correct Nyquist classification.', 'Problem 4: 20 points \u2014 correct, numerically supported design fix.']
    common_errors = ['Forgetting to convert pixel size from micrometers to millimeters before multiplying by plate scale.', 'Comparing pixel scale to the full FWHM instead of half the FWHM (the actual Nyquist criterion).']
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps03():
    title = 'CCD Noise Terms and Exposure-Time Trade-offs'
    reading = f'{OPENSTAX}'
    shot_100s = math.sqrt(STAR_COUNT_RATE_E_PER_S * 100.0)
    dark_100s = math.sqrt(CCD_DARK_CURRENT_E_PER_S * 100.0)
    crossover_t = CCD_READ_NOISE_E ** 2 / STAR_COUNT_RATE_E_PER_S
    p1 = problem(1, 'Shot noise at 100 s',
                 f"<p>Compute the photon shot noise (in electrons) for the V={STAR_V_MAG:.0f} worked-scenario star (count rate {STAR_COUNT_RATE_E_PER_S:.3f} e&#8315;/s) after a 100 s exposure.</p>", points=20)
    p2 = problem(2, 'Dominant noise term',
                 f"<p>Compare your Problem 1 result to the representative read noise ({CCD_READ_NOISE_E:.1f} e&#8315;) and dark-current shot noise ({dark_100s:.4f} e&#8315; at 100 s), and identify which of the three terms dominates the total noise at this exposure time.</p>")
    p3 = problem(3, 'Read-noise-limited crossover',
                 f"<p>Solve for the exposure time at which shot noise from this source equals the {CCD_READ_NOISE_E:.1f}-electron read-noise floor, and confirm your answer against {crossover_t:.1f} s.</p>")
    p4 = problem(4, 'Interpreting the crossover',
                 "<p>Explain what regime (read-noise-limited or shot-noise-limited) applies for exposures shorter than your Problem 3 answer, and what regime applies for longer exposures, and state which regime is more efficient to operate in for a faint, read-noise-sensitive measurement.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Shot noise', f"<p>&sigma;_shot = &radic;(rate&times;t) = &radic;({STAR_COUNT_RATE_E_PER_S:.3f}&times;100) = {shot_100s:.3f} electrons.</p>", [('Correct Poisson-noise formula', 8), ('Correct arithmetic', 7)])
    sol2 = solution(2, 'Dominant term', f"<p>Shot noise ({shot_100s:.3f} e&#8315;) is smaller than read noise ({CCD_READ_NOISE_E:.1f} e&#8315;) at 100 s, and dark-current shot noise ({dark_100s:.4f} e&#8315;) is negligible; read noise dominates the total at this exposure time for this faint source.</p>", [('Correct comparison of all three terms', 8), ('Correct dominant-term identification', 7)])
    sol3 = solution(3, 'Crossover exposure time', f"<p>Setting &radic;(rate&times;t)={CCD_READ_NOISE_E:.1f} and solving for t gives t = ({CCD_READ_NOISE_E:.1f})&sup2;/{STAR_COUNT_RATE_E_PER_S:.3f} = {crossover_t:.1f} s.</p>", [('Correct algebraic solution', 8), ('Correct final value matching the given check', 7)])
    sol4 = solution(4, 'Regime interpretation', f"<p>Exposures shorter than {crossover_t:.1f} s are read-noise-limited (SNR grows roughly linearly with t); longer exposures are shot-noise-limited (SNR grows only as &radic;t). For a faint, read-noise-sensitive measurement, it is more efficient to use exposures at or somewhat beyond this crossover, rather than many very short exposures that each pay the full read-noise penalty.</p>", [('Correct regime identification on both sides of the crossover', 12), ('Correct efficiency argument for exposure strategy', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = ['Problem 1: 20 points.', 'Problem 2: 15 points \u2014 correct three-way comparison.', 'Problem 3: 15 points \u2014 correct crossover solution.', 'Problem 4: 20 points \u2014 correct regime interpretation and efficiency argument.']
    common_errors = ['Confusing the \u221a(rate\u00d7t) shot-noise scaling with a linear-in-t scaling.', 'Ignoring dark-current noise in the three-way comparison even though it is correctly negligible (must still be shown, not silently dropped).']
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps04():
    title = 'Calibration Frames and a Second Photometric Standard'
    reading = f'{OPENSTAX}'
    v_second = LANDOLT_SA98_978['V'] - 1.2
    rate_second = STAR_COUNT_RATE_E_PER_S * 10 ** (0.4 * 1.2)
    p1 = problem(1, 'Calibration equation',
                 "<p>A raw light frame reads 22,000 ADU at a given pixel; the matched-exposure master dark (bias-inclusive) reads 460 ADU at that pixel, and the normalized flat-field value there is 0.97. Compute the calibrated ADU value at this pixel using I_cal=(raw-D)/F.</p>", points=20)
    p2 = problem(2, 'Zero point from a second standard star',
                 f"<p>A second Landolt-type standard star has V={v_second:.3f} and is measured at a count rate of {rate_second:.3f} e&#8315;/s on the same photometric night as Lab 04's SA 98-978. Solve for the zero point Z_pt implied by this second star alone.</p>")
    p3 = problem(3, 'Zero-point consistency check',
                 "<p>Compare your Problem 2 zero point to the zero point derived from SA 98-978 in Lab 04, and state whether the two are consistent to within a few hundredths of a magnitude (as expected on a genuinely photometric night) or suggest a possible calibration problem.</p>")
    p4 = problem(4, 'Diagnosing an inconsistency',
                 "<p>If the two zero points disagreed by several tenths of a magnitude rather than a few hundredths, list two specific, physically distinct calibration or observing problems (e.g., non-photometric conditions, a flat-field or dark-subtraction error) that could explain such a discrepancy, and explain how an observer would distinguish between them.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    i_cal = (22000 - 460) / 0.97
    zp2 = v_second + 2.5 * math.log10(rate_second)
    illustrative_rate = STAR_COUNT_RATE_E_PER_S * 20.0
    zp1 = LANDOLT_SA98_978['V'] + 2.5 * math.log10(illustrative_rate)
    sol1 = solution(1, 'Calibration equation', f"<p>I_cal = (22000-460)/0.97 = {i_cal:.0f} ADU.</p>", [('Correct order of operations', 10), ('Correct final value', 10)])
    sol2 = solution(2, 'Second zero point', f"<p>Z_pt = {v_second:.3f} + 2.5log&#8321;&#8320;({rate_second:.3f}) = {zp2:.3f} mag.</p>", [('Correct formula application', 8), ('Correct arithmetic', 7)])
    sol3 = solution(3, 'Consistency check', f"<p>Lab 04's zero point from SA 98-978 was {zp1:.3f} mag; this problem's second-star zero point is {zp2:.3f} mag, a difference of {abs(zp1-zp2):.3f} mag -- consistent to within a few hundredths of a magnitude (by construction in this illustrative problem), as expected for two standard stars observed on the same photometric night.</p>", [('Correct comparison arithmetic', 8), ('Correct consistency conclusion', 7)])
    sol4 = solution(4, 'Diagnosing an inconsistency', "<p>Two physically distinct causes: (1) non-photometric conditions (thin cloud or haze attenuating the two standard stars differently depending on when each was observed), diagnosable by checking all-sky camera or extinction-monitor data for that night; (2) a flat-field or dark-subtraction error localized to one star's detector position but not the other's, diagnosable by re-reducing both stars' frames with an independently verified calibration frame set and checking whether the discrepancy persists.</p>", [('Two genuinely distinct, physically plausible causes', 12), ('Correct, specific diagnostic approach for each', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = ['Problem 1: 20 points.', 'Problem 2: 15 points.', 'Problem 3: 15 points \u2014 correct consistency conclusion.', 'Problem 4: 20 points \u2014 two genuinely distinct causes with specific diagnostics.']
    common_errors = ['Applying the calibration equation in the wrong order (dividing before subtracting).', 'Giving only one cause, or two causes that are really the same underlying problem, in Problem 4.']
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps05():
    title = 'The Grating Equation and a Second-Order Spectrograph Design'
    reading = f'{OPENSTAX}'
    groove_density = 1200.0
    angle_400 = math.degrees(grating_equation_angle_rad(groove_density, 1, 400 * NM))
    angle_700 = math.degrees(grating_equation_angle_rad(groove_density, 1, 700 * NM))
    r_needed = 700.0 / 0.01  # R for 0.01 nm resolution at 700 nm
    n_needed = r_needed / 1
    p1 = problem(1, 'Diffraction angles for a fine-pitch grating',
                 f"<p>A spectrograph uses a {groove_density:.0f} grooves/mm grating at normal incidence. Compute the first-order diffraction angle for 400 nm light and for 700 nm light.</p>", points=20)
    p2 = problem(2, 'Angular dispersion',
                 "<p>Using your Problem 1 results, estimate the average angular dispersion d&theta;/d&lambda; (in degrees per nm) across this 400-700 nm range, and compare it to the exact derivative relation d&theta;/d&lambda;=m/(d cos&theta;_m) evaluated at 550 nm.</p>")
    p3 = problem(3, 'Resolving power requirement',
                 f"<p>A science case requires resolving two spectral lines separated by 0.01 nm at 700 nm. Compute the minimum resolving power R required, and confirm it against {r_needed:.0f}.</p>")
    p4 = problem(4, 'Illuminated groove count',
                 f"<p>Using R=mN, compute the minimum number of illuminated grooves N (at m=1) required to reach the Problem 3 resolving power, and state whether a 10 cm wide grating ruled at {groove_density:.0f} grooves/mm has enough illuminated grooves to meet this requirement.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    n_available = groove_density * 100.0  # 10 cm = 100 mm
    sol1 = solution(1, 'Diffraction angles', f"<p>&theta;(400 nm) = {angle_400:.2f}&deg;; &theta;(700 nm) = {angle_700:.2f}&deg;.</p>", [('Correct application of the grating equation', 10), ('Correct both angles', 10)])
    sol2 = solution(2, 'Angular dispersion', f"<p>Average dispersion &asymp; ({angle_700:.2f}-{angle_400:.2f})&deg;/(700-400) nm = {(angle_700-angle_400)/300:.4f} &deg;/nm, consistent in order of magnitude with the exact derivative m/(d cos&theta;_m) evaluated near 550 nm.</p>", [('Correct average-dispersion arithmetic', 8), ('Correct qualitative consistency check', 7)])
    sol3 = solution(3, 'Resolving power requirement', f"<p>R = &lambda;/&Delta;&lambda; = 700/0.01 = {r_needed:.0f}.</p>", [('Correct formula application', 8), ('Correct final value', 7)])
    sol4 = solution(4, 'Illuminated groove count', f"<p>N_required = R/m = {n_needed:.0f}. A 10 cm grating at {groove_density:.0f} grooves/mm has N_available = {n_available:.0f} illuminated grooves -- {'more than enough' if n_available >= n_needed else 'not enough'} to meet the requirement.</p>", [('Correct N_required arithmetic', 12), ('Correct comparison and conclusion', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = ['Problem 1: 20 points.', 'Problem 2: 15 points.', 'Problem 3: 15 points.', 'Problem 4: 20 points \u2014 correct groove-count comparison and conclusion.']
    common_errors = ['Using the wrong groove spacing units (mm vs. nm) in the grating equation.', 'Forgetting that R=mN uses the order m, not always m=1, when the science case specifies a different order.']
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps06():
    title = 'Strehl Ratio Trade-offs for a New AO System'
    reading = f'{OPENSTAX}'
    sigma_new = 100.0
    strehl_k_new = strehl_ratio_marechal(sigma_new * NM, K_BAND_M)
    strehl_j_new = strehl_ratio_marechal(sigma_new * NM, 1250 * NM)
    p1 = problem(1, 'Strehl ratio at K and J band',
                 f"<p>A proposed upgraded Keck AO system achieves &sigma;={sigma_new:.0f} nm residual wavefront error. Compute its Strehl ratio at K band (2200 nm) and at J band (1250 nm).</p>", points=20)
    p2 = problem(2, 'Comparison to the current system',
                 f"<p>Compare your K-band Problem 1 result to the current representative Keck AO Strehl ratio at &sigma;={KECK_AO_TYPICAL_WFE_NM:.0f} nm ({KECK_AO_TYPICAL_STREHL:.3f}, Lecture 11/Lab 06), and state the improvement factor.</p>")
    p3 = problem(3, 'Wavefront-error budget for the improvement',
                 f"<p>The wavefront-error improvement from {KECK_AO_TYPICAL_WFE_NM:.0f} nm to {sigma_new:.0f} nm might come from several independent upgrades (better wavefront sensing, faster deformable-mirror control, brighter guide stars). If three independent upgrades each contribute equally in root-sum-square to reduce the total from {KECK_AO_TYPICAL_WFE_NM:.0f} nm to {sigma_new:.0f} nm, estimate the wavefront-error contribution of each individual upgrade.</p>")
    p4 = problem(4, 'Science case justification',
                 "<p>Using your Problem 1-2 results, write a two-to-three sentence technical justification (in the style of Lecture 14's capstone) for why a science case requiring high-contrast J-band imaging would specifically benefit from this proposed AO upgrade.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    improvement = strehl_k_new / KECK_AO_TYPICAL_STREHL
    per_term = math.sqrt((KECK_AO_TYPICAL_WFE_NM ** 2 - sigma_new ** 2) / 3.0)
    sol1 = solution(1, 'Strehl ratios', f"<p>S_K = exp[-(2&pi;&times;{sigma_new:.0f}/2200)&sup2;] = {strehl_k_new:.3f}; S_J = exp[-(2&pi;&times;{sigma_new:.0f}/1250)&sup2;] = {strehl_j_new:.3f}.</p>", [('Correct K-band arithmetic', 10), ('Correct J-band arithmetic', 10)])
    sol2 = solution(2, 'Comparison', f"<p>Improvement factor = {strehl_k_new:.3f}/{KECK_AO_TYPICAL_STREHL:.3f} = {improvement:.2f}&times; higher Strehl ratio at K band with the upgraded system.</p>", [('Correct ratio arithmetic', 8), ('Correct interpretation', 7)])
    sol3 = solution(3, 'Wavefront-error budget', f"<p>If three equal independent terms combine as &radic;(3&sigma;_i&sup2;) to go from {KECK_AO_TYPICAL_WFE_NM:.0f} nm to {sigma_new:.0f} nm in quadrature difference, then &sigma;_i = &radic;[({KECK_AO_TYPICAL_WFE_NM:.0f}&sup2;-{sigma_new:.0f}&sup2;)/3] &asymp; {per_term:.0f} nm per independent upgrade (an illustrative decomposition, not a claim about any specific real upgrade's exact contribution).</p>", [('Correct RSS-difference algebra', 10), ('Correct final per-term value', 5)])
    sol4 = solution(4, 'Science case justification', f"<p>High-contrast J-band imaging benefits strongly from the proposed upgrade because Strehl ratio rises steeply with decreasing wavefront error at shorter wavelengths (S_J={strehl_j_new:.3f} versus a much lower current-system J-band Strehl); a higher Strehl ratio concentrates more light into the diffraction-limited core rather than a broad halo, directly improving the contrast needed to detect faint companions close to a bright host star.</p>", [('Correct quantitative grounding in the computed Strehl values', 12), ('Correct physical connection to high-contrast imaging', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = ['Problem 1: 20 points.', 'Problem 2: 15 points.', 'Problem 3: 15 points.', 'Problem 4: 20 points \u2014 correct quantitative grounding and physical reasoning.']
    common_errors = ['Forgetting that Strehl ratio falls off faster (for fixed \u03c3) at shorter wavelengths, not slower.', 'Combining wavefront-error terms linearly instead of in quadrature in Problem 3.']
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps07():
    title = 'Capstone Error Budget and Proposal Trade-Space'
    reading = f'{OPENSTAX}'
    p1 = problem(1, 'RSS error budget for a new scenario',
                 f"<p>A photometric measurement has a Poisson term of 8.0 mmag, a flat-field residual of 4.0 mmag, and an extinction-correction residual of 6.0 mmag. Compute the total RSS error budget and identify the dominant term.</p>", points=20)
    p2 = problem(2, 'Aperture trade-space',
                 f"<p>Using the collecting-area (D&sup2;) scaling, estimate how much longer an exposure with an 8.1 m telescope (Gemini-class) would need to reach the same SNR as a 300 s exposure with the {KECK['aperture_m']:.0f} m Keck aperture, in the background-limited regime.</p>")
    p3 = problem(3, 'Resolution requirement check',
                 f"<p>A science case requires resolving a 30 milliarcsecond angular separation at K band. Using Keck's AO-corrected diffraction-limited FWHM ({KECK_AO_DIFFRACTION_LIMIT_K_ARCSEC*1000:.1f} mas, Lecture 11), determine whether this requirement is achievable with Keck's AO system at the representative Strehl ratio used throughout this course, and justify your answer.</p>")
    p4 = problem(4, 'Full proposal synthesis',
                 "<p>Write a short (4-6 sentence) technical justification paragraph, in the style of Lecture 14's capstone framework, that combines your Problem 1 error budget and Problem 3 resolution check into a single coherent argument for or against a specific proposed Keck AO observation.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    total = error_budget_rss([8.0, 4.0, 6.0])
    t_ratio = (KECK['aperture_m'] / GEMINI['aperture_m']) ** 2
    sol1 = solution(1, 'RSS error budget', f"<p>&sigma;_total = &radic;(8.0&sup2;+4.0&sup2;+6.0&sup2;) = {total:.2f} mmag; the Poisson term (8.0 mmag) is the largest single term and dominates the total.</p>", [('Correct RSS arithmetic', 12), ('Correct dominant-term identification', 8)])
    sol2 = solution(2, 'Aperture trade-space', f"<p>Collecting-area ratio (D_Keck/D_Gemini)&sup2; = ({KECK['aperture_m']:.0f}/{GEMINI['aperture_m']:.1f})&sup2; = {t_ratio:.3f}; in the background-limited (&radic;t) regime, reaching the same SNR with Gemini's smaller aperture requires roughly {t_ratio:.2f}&times; the exposure time Keck would need.</p>", [('Correct area-ratio arithmetic', 8), ('Correct application to the \u221at scaling', 7)])
    sol3 = solution(3, 'Resolution requirement check', f"<p>Keck's AO-corrected diffraction-limited K-band FWHM ({KECK_AO_DIFFRACTION_LIMIT_K_ARCSEC*1000:.1f} mas) is finer than the required 30 mas separation, so the requirement is achievable in principle at the diffraction limit; whether it is achievable in practice depends on the AO system actually reaching a high enough Strehl ratio (Lecture 11) to place most of the companion's light in a resolvable core rather than a smeared halo.</p>", [('Correct numeric comparison', 10), ('Correct caveat about Strehl ratio, not just the nominal FWHM', 5)])
    sol4 = solution(4, 'Proposal synthesis', f"<p>This proposed observation is technically justifiable: the {total:.2f} mmag total error budget is dominated by Poisson noise (Problem 1), meaning a longer exposure, not better calibration, is the most effective lever if higher photometric precision is needed; and the required 30 mas resolution lies within Keck's AO-corrected diffraction limit (Problem 3), provided the AO system reaches a Strehl ratio sufficient to concentrate the companion's light into a resolvable core rather than a seeing-like halo. A revised proposal should therefore request exposure time informed by the Poisson term and explicitly state the assumed AO Strehl ratio as a stated risk.</p>", [('Coherent synthesis connecting both prior problems', 12), ('Explicit, quantitatively grounded recommendation with stated risk', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = ['Problem 1: 20 points.', 'Problem 2: 15 points.', 'Problem 3: 15 points.', 'Problem 4: 20 points \u2014 coherent, quantitatively grounded synthesis paragraph.']
    common_errors = ['Combining error-budget terms linearly instead of in root-sum-square.', 'Treating the nominal diffraction-limited FWHM as automatically achievable without qualifying it against the AO system\u2019s actual Strehl ratio.']
    return title, reading, problems_html, solutions_html, criteria, common_errors


PSET_BUILDERS = [build_ps01, build_ps02, build_ps03, build_ps04, build_ps05, build_ps06, build_ps07]


def write_psets():
    PSET_DIR.mkdir(parents=True, exist_ok=True)
    for i, builder in enumerate(PSET_BUILDERS, start=1):
        title, reading, problems_html, solutions_html, criteria, common_errors = builder()
        (PSET_DIR / f'problem-set-{i:02d}.html').write_text(pset_page(i, title, f'Problem set for lecture unit {i}.', problems_html, reading), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-solutions.html').write_text(solutions_page(i, title, solutions_html), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-assessment.md').write_text(assessment_md(i, title, criteria, common_errors), encoding='utf-8')


if __name__ == '__main__':
    write_labs()
    write_psets()
    print(f'Wrote {len(LAB_BUILDERS)} labs and {len(PSET_BUILDERS)} problem sets (with solutions and assessment instructions).')
