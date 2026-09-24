"""Second-pass lab and problem-set generator for ASTR210.

Rewrites all seven labs and all seven problem sets (student sheet, solution
key, and assessment instructions) with concrete apparatus/data, correct
computed values, explicit uncertainty treatment, and exact OpenStax
Astronomy 2e chapter/section references. Depends on the shared page()/CSS
helpers and precomputed constants in generate_astr210_content.py.

Run with the project interpreter:
    python materials/ASTR210/src/generate_astr210_labs_psets.py
"""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

from generate_astr210_content import (
    CSS, page, li, ROOT, LAB_DIR, PSET_DIR,
    BIAS, BIAS_ERR, DARK, DARK_ERR,
    ZP, RATE_A, RATE_B, RATE_C, MAG_B_PRED, MAG_C_PRED, STD_A, STD_B, STD_C,
    PLATE_SCALE, C_KMS, RV_MEAN,
)

OPENSTAX = 'OpenStax Astronomy 2e (local reference copy: references/openstax-astronomy-2e.pdf)'


def problem(i: int, heading: str, body: str, points: int = 15) -> str:
    return f'<article class="problem"><h3>{i}. {escape(heading)} <span class="points">{points} points</span></h3>{body}</article>'


def solution(i: int, heading: str, body: str, rubric) -> str:
    rows = ''.join(f'<tr><td>{escape(k)}</td><td>{v}</td></tr>' for k, v in rubric)
    return (
        f'<article class="problem"><h3>{i}. {escape(heading)}</h3>{body}'
        f'<table><tr><th>Criterion</th><th>Points</th></tr>{rows}</table></article>'
    )


# ---------------------------------------------------------------------------
# LABS
# ---------------------------------------------------------------------------

def lab_page(n: int, title: str, focus: str, sections: str) -> str:
    body = f"<header><div><h1>Lab {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header><main>{sections}</main>"
    return page(f'ASTR 210 Lab {n:02d}', body)


def make_lab_01() -> str:
    D, Derr, B, Berr = DARK, DARK_ERR, BIAS, BIAS_ERR
    # Real 40x40 pixel patches from a Canon EOS M50 imaging session (2022-07-19),
    # verified directly from the raw CR3 and the session's Astro Pixel Processor
    # master dark/flat FITS files (see reference-log.md for exact coordinates).
    patches = [
        ('Near top-left', 2885.87, 0.96),
        ('Near top-right', 2882.51, 0.99),
        ('Center', 3048.14, 1.09),
        ('Near bottom-left', 2910.68, 0.90),
        ('Near bottom-right', 3100.91, 0.93),
    ]
    rows = ''.join(
        f'<tr><td>{escape(pid)}</td><td>{raw:.2f}</td><td>{f:.2f}</td><td></td><td></td></tr>'
        for pid, raw, f in patches
    )
    p1_cal = (patches[0][1] - D) / patches[0][2]
    p3_cal = (patches[2][1] - D) / patches[2][2]
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will calibrate five real 40&times;40 pixel patches from an actual imaging session: a Canon EOS M50 (CMOS, RGGB Bayer, 14-bit ADC) on a William Optics Zenithstar 73 refractor with a Flat73R 0.8&times; reducer and an Astronomik CLS light-pollution clip filter, captured with BackyardEOS and calibrated with Astro Pixel Processor on 2022-07-19. The light frame is <code>LIGHT_300s_400iso_+31c_20220719-22h40m39s641ms.CR3</code> (ISO 400, 300 s exposure). Because the session's master dark was built from four 300.1 s exposures &mdash; matching the light frames' exposure length &mdash; it already contains the bias pedestal, so calibration here uses a single dark-frame subtraction rather than separate bias and dark terms (see Lecture 1).</p>
<ul><li>Matched-exposure master dark level (green/G1 channel, from <code>MD-IG_400.0-E300.100006s-CANON_EOS_M50-6288x4056-all_channels-session_1.fits</code>, N = 4 frames): D = {D:.1f} \u00b1 {Derr:.2f} ADU.</li>
<li>For comparison, the separate master bias level (from <code>MB-IG_400.0-E_2.5E-4s-...fits</code>, N = 20 frames): B = {B:.1f} \u00b1 {Berr:.2f} ADU &mdash; note D and B are statistically indistinguishable in mean level, confirming negligible mean dark current at this ISO and exposure length.</li>
<li>Five source-patch raw ADU values (mean pixel value in each 40&times;40 patch) and their per-patch normalized flat-field values (from the matching master flat, <code>MF-IG_400.0-E_0.3s-...fits</code>, N = 19 twilight-sky frames), listed in the Materials table below.</li></ul></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Patch</th><th>Raw ADU (mean)</th><th>Flat value F</th><th>Calibrated I_cal (ADU)</th><th>Uncertainty (ADU)</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small">Worked check (do not simply copy \u2014 reproduce the arithmetic yourself before trusting it): for the top-left patch, I_cal = ({patches[0][1]:.2f} \u2212 {D:.1f}) / {patches[0][2]:.2f} = {p1_cal:.1f} ADU. For the center patch, I_cal = ({patches[2][1]:.2f} \u2212 {D:.1f}) / {patches[2][2]:.2f} = {p3_cal:.1f} ADU.</p></section>
<section><h2>Procedure</h2><ol>
<li>Record the matched-exposure master dark value and its uncertainty in your notebook, along with the light frame's exposure length and ISO.</li>
<li>For each of the five patches, apply I_cal = (I_raw \u2212 D) / F and complete the calibrated-value column.</li>
<li>Estimate the uncertainty on each calibrated value from the master dark's own noise, propagated through the flat division: \u03c3(I_cal) \u2248 \u03c3_D / F. Compute this for at least two patches and comment on whether it is the dominant uncertainty source (compare to Lecture 4\u2019s Poisson term for a count level of a few hundred ADU above the calibration floor).</li>
<li>Plot calibrated ADU against patch position (top-left, top-right, center, bottom-left, bottom-right) and describe the pattern you see across the frame.</li>
<li>The camera's bad-pixel map (from the same 2022-07-19 calibration set) flags 2.554% of all pixels as "hot" and 4.882% as "cold." For a circular photometric aperture of 9 pixels (used in later labs), estimate the expected number of flagged pixels landing inside a randomly placed aperture, assuming pixels are flagged independently at these rates.</li>
<li>Write a two-to-three sentence conclusion stating which effect (vignetting/flat-field variation across the frame, or the dark-frame subtraction) changed each patch's value the most, and why a bad-pixel map is still needed even after dark and flat calibration.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The normalized flat value varies by roughly 10\u201313% across these five patches (0.90 to 1.09), while the dark-frame subtraction changes every patch by essentially the same fixed amount (about {D:.0f} ADU). State explicitly, with a number, which correction (the flat's spatial variation, or the dark subtraction) dominates the patch-to-patch differences you observe in I_cal.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed five-row calibration table with uncertainties.</li>
<li>One plot or labeled diagram of calibrated ADU by patch position across the frame.</li>
<li>The expected-flagged-pixel calculation for a 9-pixel aperture.</li>
<li>A short (150\u2013250 word) conclusion identifying the dominant spatial effect and explaining the continued need for a bad-pixel map.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct arithmetic and units for all five patches (matches or is consistent with the two worked checks).</li>
<li>Uncertainty propagation shown explicitly, not just asserted.</li>
<li>Expected flagged-pixel count is computed correctly from the stated hot/cold pixel fractions.</li>
<li>Conclusion is evidence-based and references the actual computed numbers, not a generic statement.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 6.3 (visible-light detectors and instruments).</li>
<li>Real calibration data: Canon EOS M50 imaging session, 2022-07-19, BackyardEOS capture and Astro Pixel Processor master-frame reduction; raw light frame and master bias/dark/flat/bad-pixel-map FITS files under <code>C:\\Users\\rober\\OneDrive\\Pictures\\BackyardEOS\\2022-07-19\\</code> and <code>00Masters\\</code>, logged with exact patch pixel coordinates in <code>materials/ASTR210/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(1, 'Detector Calibration', 'Calibrate five real aperture patches from a Canon EOS M50 imaging session using a matched-exposure dark/flat model, and propagate uncertainty.', sections)


def make_lab_02() -> str:
    scenarios = [
        ('A (bright source, dark sky)', 2500, 9, 150, 5, 8),
        ('B (faint source, dark sky)', 300, 9, 150, 5, 8),
        ('C (faint source, large aperture)', 120, 25, 150, 5, 8),
        ('D (moderate source, moonlit sky)', 800, 9, 400, 5, 8),
    ]
    def snr(S, npix, sky, dark, read):
        return S / math.sqrt(S + npix * (sky + dark + read ** 2))
    rows = ''
    for label, S, npix, sky, dark, read in scenarios:
        val = snr(S, npix, sky, dark, read)
        cls = 'secure (>5)' if val >= 5 else ('marginal (3\u20135)' if val >= 3 else 'non-detection (<3)')
        rows += f'<tr><td>{escape(label)}</td><td>{S}</td><td>{npix}</td><td>{sky}</td><td>{dark}</td><td>{read}</td><td></td><td></td></tr>'
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will evaluate four realistic source/background combinations using the SNR model from Lecture 4: SNR = S / \u221a(S + n_pix\u00b7(B_sky + D + R\u00b2)). All four scenarios use the same read noise (R = 8 e\u207b) so you can isolate the effect of source brightness, aperture size, and sky brightness separately.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Scenario</th><th>S (e\u207b)</th><th>n_pix</th><th>Sky (e\u207b/pix)</th><th>Dark (e\u207b/pix)</th><th>Read (e\u207b)</th><th>SNR</th><th>Classification</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>For each scenario, compute the noise term n_pix\u00d7(B_sky + D + R\u00b2), then SNR, showing your arithmetic.</li>
<li>Classify each scenario as a secure detection (SNR \u2265 5), a marginal detection (3 \u2264 SNR &lt; 5), or a non-detection (SNR &lt; 3).</li>
<li>Compare Scenario A to Scenario B: both use the same aperture and sky, but very different source counts. State the SNR ratio and check it is close to the ratio of the square roots of the source counts (an approximation valid when source-dominated).</li>
<li>Compare Scenario B to Scenario C: explain, using the noise term, why enlarging the aperture from 9 to 25 pixels can turn a marginal detection into a non-detection even though the source flux captured is similar.</li>
<li>Compare Scenario A to Scenario D: quantify how much the SNR degrades when sky background rises from 150 to 400 e\u207b/pix (a moonlit-night effect), holding the source brightness closer to but not identical to Scenario A.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly which term dominates the noise budget in each scenario (source shot noise, sky shot noise, dark current, or read noise) and justify your answer with the relative sizes of S, n_pix\u00d7B_sky, n_pix\u00d7D, and n_pix\u00d7R\u00b2.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed SNR table with arithmetic shown for all four scenarios.</li>
<li>A short paragraph identifying the dominant noise term in each case.</li>
<li>A one-paragraph recommendation for how an observer could improve the Scenario C detection (e.g., smaller aperture, longer exposure, better seeing).</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct SNR values for all four scenarios (within rounding).</li>
<li>Correct classification (secure/marginal/non-detection) for each.</li>
<li>Dominant noise term correctly identified and justified with numbers, not assertion.</li>
<li>Recommendation is physically reasonable and tied to the noise model.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 6.3 (detectors) and Chapter 17.1 (brightness of stars).</li>
<li>Scenario values are instructor-provided synthetic parameters logged in <code>materials/ASTR210/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(2, 'Signal-to-Noise Budget', 'Classify four source/background scenarios as secure, marginal, or non-detections.', sections)


def make_lab_03() -> str:
    unk_counts, unk_exp = 45000, 30
    unk_rate = unk_counts / unk_exp
    unk_mag = -2.5 * math.log10(unk_rate) + ZP
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will use <code>../data/photometry_standard_stars.csv</code>, containing V-band aperture counts for three photometric standard stars observed in the same field and night, plus one unidentified target measured with the identical aperture and sky annulus.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Star</th><th>Filter</th><th>Counts</th><th>Exp. time (s)</th><th>Catalog V mag</th></tr></thead><tbody>
<tr><td>STD-A</td><td>V</td><td>{STD_A['counts']}</td><td>{STD_A['exptime']}</td><td>{STD_A['mag']}</td></tr>
<tr><td>STD-B</td><td>V</td><td>{STD_B['counts']}</td><td>{STD_B['exptime']}</td><td>{STD_B['mag']}</td></tr>
<tr><td>STD-C</td><td>V</td><td>{STD_C['counts']}</td><td>{STD_C['exptime']}</td><td>{STD_C['mag']}</td></tr>
<tr><td>TARGET-X (unknown)</td><td>V</td><td>{unk_counts}</td><td>{unk_exp}</td><td>?</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute the count rate (counts/exposure time) for STD-A and derive the zero point ZP using m = \u22122.5log10(rate) + ZP and the catalog magnitude.</li>
<li>Apply your derived ZP to STD-B and STD-C and compare your predicted magnitudes to the catalog values. State the agreement in millimagnitudes.</li>
<li>If the agreement for either star is worse than about 0.02 mag, identify a plausible cause (aperture too small, contaminating neighbor, misreported exposure time) before proceeding.</li>
<li>Apply your verified ZP to TARGET-X and report its calibrated V magnitude.</li>
<li>Estimate the uncertainty on the TARGET-X magnitude from Poisson statistics on its count rate, and combine it in quadrature with a zero-point uncertainty of \u00b10.02 mag (Lecture 13\u2019s method).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Report TARGET-X\u2019s magnitude as m \u00b1 \u03c3_total, following the quadrature-combination rule, not as a bare number.</p></section>
<section><h2>Deliverables</h2><ul><li>Derived zero point with the arithmetic shown.</li><li>Verification table comparing predicted and catalog magnitudes for STD-B and STD-C.</li><li>TARGET-X magnitude with combined uncertainty.</li><li>One sentence stating whether you trust this zero point for other targets in the same field, and why.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Zero point correctly derived from STD-A.</li><li>Verification against STD-B/STD-C shown with numeric agreement stated.</li><li>TARGET-X magnitude correct to the precision of the input data, with an uncertainty explicitly combined in quadrature.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 17.1 (the brightness of stars).</li><li>Dataset: <code>materials/ASTR210/data/photometry_standard_stars.csv</code>, logged in <code>reference-log.md</code>.</li></ul></section>
"""
    return lab_page(3, 'Aperture Photometry', 'Derive and verify a photometric zero point, then calibrate an unknown target.', sections)


def make_lab_04() -> str:
    rows_data = [
        (0.00, 0.995, 1.000), (0.05, 0.992, 1.001), (0.10, 0.970, 0.999),
        (0.15, 0.955, 1.000), (0.20, 0.972, 1.002), (0.25, 0.994, 1.001),
    ]
    computed = []
    for t, ft, fc in rows_data:
        ratio = ft / fc
        dm = -2.5 * math.log10(ratio)
        computed.append((t, ft, fc, dm))
    rows = ''.join(f'<tr><td>{t:.2f}</td><td>{ft:.3f}</td><td>{fc:.3f}</td><td></td></tr>' for t, ft, fc, dm in computed)
    dm_max = max(computed, key=lambda r: r[3])
    dm_min = min(computed, key=lambda r: r[3])
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will use <code>../data/variable_star_lightcurve.csv</code>, containing normalized target and comparison-star fluxes at six times (in fractional Barycentric Julian Date offset, t_bjd) spanning one observing sequence.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>t (BJD offset)</th><th>Target flux</th><th>Comparison flux</th><th>&Delta;m (mag)</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute \u0394m = \u22122.5log10(F_target/F_comp) at each of the six times and complete the table.</li>
<li>Plot \u0394m versus t. Identify the time of minimum light (largest \u0394m, i.e. faintest target) and its approximate depth relative to the t = 0.00 baseline.</li>
<li>Estimate a noise floor for \u0394m from the two flattest points in the comparison star\u2019s own flux (should be within about 0.2% of 1.000); convert that flux scatter to an equivalent \u0394m scatter and compare it to the dip depth you measured.</li>
<li>State, with a number, whether the dip is statistically significant relative to your estimated noise floor.</li>
<li>Discuss what would make this comparison star unsuitable (e.g., if its own flux had varied by 2% instead of 0.2%).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Report the dip depth (in millimagnitudes) relative to the pre-dip baseline, and the estimated noise floor, and state their ratio as a rough significance (dip depth / noise floor).</p></section>
<section><h2>Deliverables</h2><ul><li>Completed six-row \u0394m table.</li><li>Light-curve plot with the dip clearly marked.</li><li>Dip depth, noise floor, and significance ratio, each with a number.</li><li>One paragraph judging whether the comparison star was a good choice.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct \u0394m for all six rows.</li><li>Dip correctly identified near t \u2248 0.15 with a depth consistent with the data (roughly 0.03\u20130.05 mag).</li><li>Noise floor estimated from actual comparison-star scatter, not assumed.</li><li>Significance judgment is quantitative, not just descriptive.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 17.1 (brightness/magnitudes) and Chapter 21.4 (transiting exoplanet evidence).</li><li>Dataset: <code>materials/ASTR210/data/variable_star_lightcurve.csv</code>, logged in <code>reference-log.md</code>.</li></ul></section>
"""
    return lab_page(4, 'Differential Light Curve', 'Build a differential light curve, locate the dip, and test its significance.', sections)


def make_lab_05() -> str:
    p1 = (520.3, 411.2, 132.1021, 12.5510)
    p2 = (534.7, 415.8, 132.0988, 12.5521)
    p3 = (549.1, 420.5, 132.0954, 12.5532)
    dt_min = 15.0
    dx12, dy12 = p2[0] - p1[0], p2[1] - p1[1]
    pix12 = math.hypot(dx12, dy12)
    dec_mean12 = math.radians((p1[3] + p2[3]) / 2)
    dra12 = (p1[2] - p2[2]) * math.cos(dec_mean12) * 3600
    ddec12 = (p2[3] - p1[3]) * 3600
    sky12 = math.hypot(dra12, ddec12)
    scale12 = sky12 / pix12
    dx23, dy23 = p3[0] - p2[0], p3[1] - p2[1]
    pix23 = math.hypot(dx23, dy23)
    dec_mean23 = math.radians((p2[3] + p3[3]) / 2)
    dra23 = (p2[2] - p3[2]) * math.cos(dec_mean23) * 3600
    ddec23 = (p3[3] - p2[3]) * 3600
    sky23 = math.hypot(dra23, ddec23)
    scale23 = sky23 / pix23
    rate_arcsec_per_min = sky12 / dt_min
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will use <code>../data/asteroid_astrometry.csv</code>, three sequential images of a fast-moving object with a {dt_min:.0f}-minute interval between exposures, each with a measured pixel centroid and a matched sky position from a plate solution.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Image</th><th>x (px)</th><th>y (px)</th><th>RA (deg)</th><th>Dec (deg)</th></tr></thead><tbody>
<tr><td>1</td><td>{p1[0]}</td><td>{p1[1]}</td><td>{p1[2]}</td><td>{p1[3]}</td></tr>
<tr><td>2</td><td>{p2[0]}</td><td>{p2[1]}</td><td>{p2[2]}</td><td>{p2[3]}</td></tr>
<tr><td>3</td><td>{p3[0]}</td><td>{p3[1]}</td><td>{p3[2]}</td><td>{p3[3]}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>From images 1 and 2, compute the pixel separation and the sky separation (arcsec), then the plate scale (arcsec/pixel).</li>
<li>From images 2 and 3, independently repeat the same calculation as a consistency check on the plate scale.</li>
<li>Compare the two plate-scale estimates. If they agree to within a few percent, you have a validated plate scale; if not, identify a likely cause (centroiding error, non-linear distortion, a typo in the coordinates).</li>
<li>Using the {dt_min:.0f}-minute interval between images 1 and 2, compute the object\u2019s angular rate of motion in arcsec/minute.</li>
<li>State whether this rate is consistent with a slow-moving main-belt asteroid or a faster-moving near-Earth object, given that typical main-belt rates are well under 1 arcsec/minute near opposition.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Report both plate-scale estimates and their percent difference. Report the derived angular rate with an explicit statement of what centroiding precision (in pixels) would be needed to measure that rate to 10% accuracy over this time baseline.</p></section>
<section><h2>Deliverables</h2><ul><li>Two independent plate-scale determinations (images 1\u20132 and images 2\u20133) with arithmetic shown.</li><li>Percent agreement between the two estimates.</li><li>Angular rate of motion in arcsec/minute, with a classification (main-belt vs. near-Earth pace) and justification.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct pixel and sky separations for both image pairs.</li><li>Plate-scale estimates near {scale12:.2f} and {scale23:.2f} arcsec/pixel (accept reasonable rounding).</li><li>Correct angular rate and a physically reasonable classification with justification.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 19.2 (surveying the stars, astrometric fundamentals).</li><li>Dataset: <code>materials/ASTR210/data/asteroid_astrometry.csv</code>, logged in <code>reference-log.md</code>; the {dt_min:.0f}-minute image cadence is an instructor-provided observing-log value.</li></ul></section>
"""
    return lab_page(5, 'Astrometry and Motion', 'Derive and cross-check a plate scale, then measure an object\u2019s angular rate of motion.', sections)


def make_lab_06() -> str:
    lines = [('H\u03b1', 656.3, 656.9), ('H\u03b2', 486.1, 486.55), ('[O III]', 500.7, 501.16)]
    rows = ''.join(f'<tr><td>{name}</td><td>{rest}</td><td>{obs}</td><td></td></tr>' for name, rest, obs in lines)
    vs = [(name, (obs - rest) / rest * C_KMS) for name, rest, obs in lines]
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will use <code>../data/spectrum_lines.csv</code>, containing rest (laboratory) and observed wavelengths for three identified spectral lines in a single target spectrum, already placed on a wavelength scale using an arc-lamp solution (Lecture 8).</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Line</th><th>Rest &lambda; (nm)</th><th>Observed &lambda; (nm)</th><th>v (km/s)</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>For each line, compute \u0394\u03bb = observed \u2212 rest, then v = (\u0394\u03bb/\u03bb\u2080)\u00d7c using c = {C_KMS:.0f} km/s.</li>
<li>Compute the mean velocity across all three lines and the maximum deviation of any single line from that mean.</li>
<li>State whether the three lines agree well enough (within a few km/s) to conclude this is a genuine single bulk radial velocity rather than a blend or calibration artifact affecting only one line.</li>
<li>Explain, in one or two sentences, why using three lines of different species (H, H, and a forbidden metal line) is stronger evidence than using three lines of the same species close together in wavelength.</li>
<li>Given a wavelength-solution residual of \u00b10.02 nm (typical for a well-calibrated spectrograph at this resolution), estimate the resulting velocity uncertainty for the H\u03b1 line and compare it to the line-to-line scatter you found.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Report the mean velocity, the line-to-line scatter, and the calibration-driven velocity uncertainty, and state which one dominates the final reported uncertainty.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed velocity table for all three lines.</li><li>Mean velocity and line-to-line scatter.</li><li>Calibration-driven velocity uncertainty estimate for H\u03b1.</li><li>A one-paragraph judgment of whether this is a secure bulk radial-velocity detection.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct velocity for each line (within rounding of the expected ~274\u2013278 km/s range).</li><li>Correct mean and scatter, with the scatter compared quantitatively to the calibration-driven uncertainty.</li><li>Judgment is justified with numbers, not just an adjective.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 5.3 (spectroscopy in astronomy) and Chapter 5.6 (the Doppler effect).</li><li>Dataset: <code>materials/ASTR210/data/spectrum_lines.csv</code>, logged in <code>reference-log.md</code>.</li></ul></section>
"""
    return lab_page(6, 'Spectroscopic Wavelength Calibration', 'Use a calibrated wavelength scale to derive and cross-check a radial velocity from three lines.', sections)


def make_lab_07() -> str:
    rows_data = [(1, 12.1, 0.8, 5.1, 0.2), (2, 15.3, 2.1, 1.2, 0.5), (3, 10.7, 0.3, 8.8, 0.1)]
    rows = ''.join(
        f'<tr><td>{sid}</td><td>{g}</td><td>{bp}</td><td>{plx}</td><td>{err}</td><td></td><td></td></tr>'
        for sid, g, bp, plx, err in rows_data
    )
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will use <code>../data/archive_query_sample.csv</code>, a small excerpt of a Gaia-like source catalog with G magnitude, color (BP\u2212RP), parallax, and parallax uncertainty for three sources.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>source_id</th><th>G mag</th><th>BP\u2212RP</th><th>Parallax (mas)</th><th>Parallax err (mas)</th><th>Parallax/err</th><th>Passes quality cut?</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute the fractional parallax quality (parallax/error) for each source and complete the table.</li>
<li>Apply a documented quality cut of parallax/error &gt; 5 and state which source(s) fail it.</li>
<li>Apply a second, independent cut of G &lt; 14 (a "bright and reliable" magnitude limit) and state which source(s) fail it.</li>
<li>Combine both cuts and report the final retained sample, listing exactly which sources remain and why each excluded source was removed.</li>
<li>For each retained source, compute distance in parsecs as d = 1000/parallax(mas), and report the result with the parallax uncertainty propagated into a distance uncertainty (\u03c3_d \u2248 d \u00d7 \u03c3_parallax/parallax for small fractional errors).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly, in a query-log paragraph, every cut you applied and in what order, so that a second student could reproduce your final retained sample exactly from the raw table above.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed quality-cut table.</li><li>A written query log documenting both cuts and their order.</li><li>Distances with propagated uncertainties for the retained sources.</li><li>One paragraph on what would change if the parallax quality cut were relaxed to &gt; 3 instead of &gt; 5.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct parallax/error ratios and correct pass/fail determination for both cuts.</li><li>Query log is specific enough to be reproducible (states the exact numeric thresholds and order).</li><li>Distances and propagated uncertainties are computed correctly for the retained sources only.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 19.2 (surveying the stars, parallax).</li><li>Dataset: <code>materials/ASTR210/data/archive_query_sample.csv</code>, logged in <code>reference-log.md</code> as a synthetic instructional excerpt modeled on Gaia-style catalog columns.</li></ul></section>
"""
    return lab_page(7, 'Archive Query Reproducibility', 'Apply and document parallax- and magnitude-quality cuts, then compute distances for the retained sample.', sections)


def write_labs():
    makers = [make_lab_01, make_lab_02, make_lab_03, make_lab_04, make_lab_05, make_lab_06, make_lab_07]
    for i, fn in enumerate(makers, 1):
        (LAB_DIR / f'lab-{i:02d}.html').write_text(fn(), encoding='utf-8')


# ---------------------------------------------------------------------------
# PROBLEM SETS (student sheet, solution key, assessment instructions)
# ---------------------------------------------------------------------------

def pset_page(n: int, title: str, focus: str, problems_html: str, openstax_note: str) -> str:
    body = f"""<header><div><h1>ASTR 210 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header>
<main><section><h2>Problems</h2>{problems_html}</section>
<section><h2>Due and Scope</h2><p>Submit a clear solution with equations, units, labeled quantities, and a short narrative interpretation for each problem. Show every reduction step and state your assumptions explicitly; a correct final number without visible work receives partial credit at most.</p></section>
<section><h2>OpenStax Companion Reading</h2><p>{openstax_note}</p></section>
<section><h2>References and Data Sources</h2><ul><li>Corresponding lecture slides and notes for this unit.</li><li>{OPENSTAX}.</li><li>Course datasets under <code>materials/ASTR210/data/</code> where referenced above.</li></ul></section>
</main>"""
    return page(f'ASTR 210 Problem Set {n:02d}', body)


def solkey_page(n: int, title: str, solutions_html: str) -> str:
    body = f"""<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header>
<main><section><h2>Worked Solutions</h2>{solutions_html}</section>
<section><h2>Grading Notes</h2><p>Award full marks for correct method, units, and a numeric result consistent with the arithmetic shown (allow reasonable rounding). Common partial-credit errors: omitting units, failing to combine uncertainties in quadrature, or overstating the confidence of a marginal (SNR 3\u20135) result.</p></section>
</main>"""
    return page(f'ASTR 210 Problem Set {n:02d} Solutions', body)


def assessment_md(n: int, title: str, items) -> str:
    rows = '\n'.join(f'- {name}: {points} points \u2014 {desc}' for name, points, desc in items)
    return f"""# Assessment Instructions: Problem Set {n:02d} \u2014 {title}

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the referenced dataset(s) under `materials/ASTR210/data/`.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking number but no visible reduction steps should not.

## Problem-Level Criteria
{rows}

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
- Missing units or an unstated aperture/exposure assumption.
- Treating a marginal (SNR 3\u20135) result as a secure detection.
- Adding uncertainties linearly instead of in quadrature.
- Quoting a final answer with more significant figures than the input data support.
"""


def write_problem_sets():
    # ---- PS01: Planning and Calibration ----
    raw1, F1 = 18500, 1.02
    cal1 = (raw1 - DARK) / F1
    alt1 = 25.0
    z1 = 90.0 - alt1
    X1 = 1.0 / math.cos(math.radians(z1))
    k_v = 0.15
    dmag1 = k_v * X1
    sigma_q1 = math.sqrt(BIAS_ERR ** 2 + DARK_ERR ** 2)
    npix_p1, sky_p1, dark_p1, read_p1 = 9, 450.0, 5.0, 8.0
    S_p1 = 700.0
    noise_p1 = npix_p1 * (sky_p1 + dark_p1 + read_p1 ** 2)
    snr_p1 = S_p1 / math.sqrt(S_p1 + noise_p1)

    ps01_problems = (
        problem(1, 'Calibration calculation', f'<p>A raw aperture patch records {raw1} ADU with flat value F = {F1:.2f}. Using the matched-exposure master dark D = {DARK:.1f} ADU from Lecture 1 (which already includes the bias pedestal), compute the calibrated signal I_cal. Show your arithmetic.</p>')
        + problem(2, 'Airmass and extinction', f'<p>A target is observed at altitude {alt1:.0f}\u00b0. Compute the airmass and the resulting extinction penalty in magnitudes, using k = {k_v:.2f} mag/airmass.</p>')
        + problem(3, 'Uncertainty budget', f'<p>Combine the separate master bias uncertainty (\u00b1{BIAS_ERR:.2f} ADU) and the matched-exposure master dark uncertainty (\u00b1{DARK_ERR:.2f} ADU) in quadrature. State whether one term dominates the combined uncertainty or whether they are comparable, and explain what that implies about where this camera\u2019s calibration-floor noise comes from.</p>')
        + problem(4, 'Observing-plan critique', f'<p>A student plans a 9-pixel aperture exposure assuming a dark-sky background of 150 e\u207b/pix, but the observation actually occurs during a bright moon with sky background {sky_p1:.0f} e\u207b/pix. For a source with S = {S_p1:.0f} e\u207b, dark = {dark_p1:.0f} e\u207b/pix, and read noise = {read_p1:.0f} e\u207b, compute the actual SNR and state whether the student\u2019s plan (which assumed a much lower background) still yields a secure detection.</p>')
    )
    write_ps(1, 'Planning and Calibration', 'Translate an observing plan into calibration and error-budget requirements.', ps01_problems,
              'Verify against OpenStax Astronomy 2e Chapter 6.3 (detectors) and Chapter 4.1 (altitude/azimuth coordinates) before instructional release.')
    ps01_sol = (
        solution(1, 'Calibration calculation', f'<p>I_cal = ({raw1} \u2212 {DARK:.1f}) / {F1:.2f} = {raw1-DARK:.1f} / {F1:.2f} = {cal1:.1f} ADU.</p>', [('Setup and units', 5), ('Calculation', 5), ('Interpretation', 5)])
        + solution(2, 'Airmass and extinction', f'<p>z = 90\u00b0 \u2212 {alt1:.0f}\u00b0 = {z1:.0f}\u00b0. X = 1/cos({z1:.0f}\u00b0) = {X1:.2f}. \u0394m = {k_v:.2f} \u00d7 {X1:.2f} = {dmag1:.2f} mag.</p>', [('Setup and units', 5), ('Calculation', 5), ('Interpretation', 5)])
        + solution(3, 'Uncertainty budget', f'<p>\u03c3_total = \u221a({BIAS_ERR:.2f}\u00b2 + {DARK_ERR:.2f}\u00b2) = \u221a({BIAS_ERR**2:.2f} + {DARK_ERR**2:.4f}) = {sigma_q1:.2f} ADU. The two terms are comparable (within about 30% of each other), so neither cleanly dominates; this indicates the calibration-floor noise on this camera comes from a mix of read noise (captured by the bias master) and residual dark-frame noise (captured by the matched-exposure dark master), not from one overwhelming source.</p>', [('Quadrature method', 8), ('Correct comparable-terms reasoning', 7)])
        + solution(4, 'Observing-plan critique', f'<p>Noise term = {npix_p1} \u00d7 ({sky_p1:.0f} + {dark_p1:.0f} + {read_p1**2:.0f}) = {noise_p1:.0f}. SNR = {S_p1:.0f}/\u221a({S_p1:.0f}+{noise_p1:.0f}) = {snr_p1:.2f}. This is still a secure detection (SNR &gt; 5), but substantially degraded from the dark-sky assumption, and the student\u2019s plan should have stated the actual sky brightness rather than assuming a dark-sky value.</p>', [('Correct SNR', 8), ('Correct critique of the plan', 7)])
    )
    write_sol(1, 'Planning and Calibration', ps01_sol)
    write_assess(1, 'Planning and Calibration', [
        ('Problem 1', 15, 'Correct calibrated ADU value with units and visible arithmetic.'),
        ('Problem 2', 15, 'Correct airmass and extinction magnitude.'),
        ('Problem 3', 15, 'Correct quadrature sum and correct comparable-terms reasoning.'),
        ('Problem 4', 15, 'Correct SNR and a substantive critique of the observing plan.'),
    ])

    # ---- PS02: Noise and Photometry ----
    npix2, sky2, dark2, read2, S2 = 16, 200.0, 6.0, 7.0, 650.0
    noise2 = npix2 * (sky2 + dark2 + read2 ** 2)
    snr2 = S2 / math.sqrt(S2 + noise2)
    counts3, exp3 = 95000, 30
    rate3 = counts3 / exp3
    mag3 = -2.5 * math.log10(rate3) + ZP
    frac_captured = 0.80
    bias_mag = -2.5 * math.log10(1 / frac_captured)
    sigma_zp2, sigma_m2 = 0.02, 0.018
    sigma_total2 = math.sqrt(sigma_zp2 ** 2 + sigma_m2 ** 2)

    ps02_problems = (
        problem(1, 'SNR classification', f'<p>A source has S = {S2:.0f} e\u207b in a {npix2}-pixel aperture, with sky = {sky2:.0f} e\u207b/pix, dark = {dark2:.0f} e\u207b/pix, and read noise = {read2:.0f} e\u207b. Compute the SNR and classify the detection.</p>')
        + problem(2, 'Zero-point application', f'<p>Using the zero point ZP = {ZP:.3f} derived in Lecture 5 from the standard-star table, compute the calibrated V magnitude of a target with {counts3} counts in a {exp3} s exposure.</p>')
        + problem(3, 'Aperture bias', f'<p>An aperture captures only {frac_captured*100:.0f}% of a star\u2019s total flux due to its finite radius. Compute the resulting magnitude bias (in mag) introduced by this aperture choice, and state whether the measured magnitude is too bright or too faint relative to the true value.</p>')
        + problem(4, 'Uncertainty budget', f'<p>Combine a zero-point uncertainty of \u00b1{sigma_zp2:.2f} mag with an instrumental measurement uncertainty of \u00b1{sigma_m2:.3f} mag in quadrature, and report the target magnitude from Problem 2 with its combined uncertainty.</p>')
    )
    write_ps(2, 'Noise and Photometry', 'Quantify detection significance and calibrated brightness for realistic photometric scenarios.', ps02_problems,
              'Verify against OpenStax Astronomy 2e Chapter 17.1 (brightness of stars) before instructional release.')
    ps02_sol = (
        solution(1, 'SNR classification', f'<p>Noise term = {npix2} \u00d7 ({sky2:.0f} + {dark2:.0f} + {read2**2:.0f}) = {noise2:.0f}. SNR = {S2:.0f}/\u221a({S2:.0f}+{noise2:.0f}) = {snr2:.2f} \u2014 a secure detection (SNR &gt; 5).</p>', [('Noise term', 5), ('SNR value', 5), ('Classification', 5)])
        + solution(2, 'Zero-point application', f'<p>Rate = {counts3}/{exp3} = {rate3:.1f} counts/s. m = \u22122.5\u00d7log10({rate3:.1f}) + {ZP:.3f} = {-2.5*math.log10(rate3):.3f} + {ZP:.3f} = {mag3:.3f}.</p>', [('Rate computed', 5), ('Correct magnitude', 10)])
        + solution(3, 'Aperture bias', f'<p>\u0394m = \u22122.5\u00d7log10(1/{frac_captured:.2f}) = {bias_mag:.3f} mag. Because only part of the flux is captured, the measured magnitude is too faint (fainter) by {abs(bias_mag):.3f} mag relative to the true value.</p>', [('Correct sign and magnitude', 10), ('Correct interpretation', 5)])
        + solution(4, 'Uncertainty budget', f'<p>\u03c3_total = \u221a({sigma_zp2:.2f}\u00b2 + {sigma_m2:.3f}\u00b2) = {sigma_total2:.3f} mag. Report: m = {mag3:.2f} \u00b1 {sigma_total2:.2f}.</p>', [('Quadrature method', 8), ('Correctly combined final report', 7)])
    )
    write_sol(2, 'Noise and Photometry', ps02_sol)
    write_assess(2, 'Noise and Photometry', [
        ('Problem 1', 15, 'Correct SNR and classification.'), ('Problem 2', 15, 'Correct zero-point application and magnitude.'),
        ('Problem 3', 15, 'Correct aperture-bias magnitude and sign/interpretation.'), ('Problem 4', 15, 'Correct quadrature combination and final reported result.'),
    ])

    # ---- PS03: Light Curves and Astrometry ----
    ft3, fc3 = 0.945, 0.998
    dm3 = -2.5 * math.log10(ft3 / fc3)
    dm0_baseline = -2.5 * math.log10(0.995 / 1.000)
    depth3 = dm3 - dm0_baseline
    pixsep3, skysep3 = 20.4, 16.8
    scale3 = skysep3 / pixsep3
    dt3 = 12.0
    rate3b = skysep3 / dt3

    ps03_problems = (
        problem(1, 'Differential magnitude', f'<p>At a given time, target flux = {ft3:.3f} and comparison flux = {fc3:.3f} (both normalized). Compute \u0394m = \u22122.5log10(F_target/F_comp).</p>')
        + problem(2, 'Dip depth', f'<p>Using the baseline \u0394m = {dm0_baseline:.4f} mag (from t = 0.00 in Lab 04), compute the dip depth relative to baseline for the \u0394m found in Problem 1.</p>')
        + problem(3, 'Plate scale', f'<p>Two images of the same field show a pixel separation of {pixsep3:.1f} px for an object that moved {skysep3:.1f} arcsec on the sky between exposures. Compute the plate scale in arcsec/pixel.</p>')
        + problem(4, 'Rate of motion and classification', f'<p>If the two images in Problem 3 were separated by {dt3:.0f} minutes, compute the object\u2019s angular rate of motion in arcsec/minute and state whether this rate is more consistent with a main-belt asteroid or a fast-moving near-Earth object.</p>')
    )
    write_ps(3, 'Light Curves and Astrometry', 'Analyze differential photometry and derive a plate scale and rate of motion from astrometric data.', ps03_problems,
              'Verify against OpenStax Astronomy 2e Chapter 17.1 (magnitudes) and Chapter 19.2 (astrometry) before instructional release.')
    ps03_sol = (
        solution(1, 'Differential magnitude', f'<p>\u0394m = \u22122.5\u00d7log10({ft3:.3f}/{fc3:.3f}) = \u22122.5\u00d7log10({ft3/fc3:.4f}) = {dm3:.4f} mag.</p>', [('Correct ratio', 5), ('Correct \u0394m', 10)])
        + solution(2, 'Dip depth', f'<p>Depth = {dm3:.4f} \u2212 {dm0_baseline:.4f} = {depth3:.4f} mag \u2248 {depth3*1000:.0f} millimagnitudes.</p>', [('Correct baseline subtraction', 8), ('Correct depth', 7)])
        + solution(3, 'Plate scale', f'<p>Plate scale = {skysep3:.1f}/{pixsep3:.1f} = {scale3:.3f} arcsec/pixel.</p>', [('Correct setup', 5), ('Correct value', 10)])
        + solution(4, 'Rate of motion', f'<p>Rate = {skysep3:.1f} arcsec / {dt3:.0f} min = {rate3b:.2f} arcsec/min. This is far faster than a typical main-belt asteroid (well under 1 arcsec/min near opposition), so it is more consistent with a fast-moving near-Earth object.</p>', [('Correct rate', 8), ('Correct classification with justification', 7)])
    )
    write_sol(3, 'Light Curves and Astrometry', ps03_sol)
    write_assess(3, 'Light Curves and Astrometry', [
        ('Problem 1', 15, 'Correct \u0394m.'), ('Problem 2', 15, 'Correct dip depth relative to baseline.'),
        ('Problem 3', 15, 'Correct plate scale.'), ('Problem 4', 15, 'Correct rate and physically justified classification.'),
    ])

    # ---- PS04: Spectroscopy ----
    dlam4, lam4 = 0.25, 500.0
    R4 = lam4 / dlam4
    rest_d1, obs_d1 = 588.99, 589.62
    v_d1 = (obs_d1 - rest_d1) / rest_d1 * C_KMS
    rest_d2, obs_d2 = 589.59, 590.22
    v_d2 = (obs_d2 - rest_d2) / rest_d2 * C_KMS
    mean_v4 = (v_d1 + v_d2) / 2
    dev4 = abs(v_d1 - mean_v4)
    res_element = 589.0 / R4 if False else lam4 / R4
    shift_mag = obs_d1 - rest_d1

    ps04_problems = (
        problem(1, 'Resolving power', f'<p>A spectrograph resolves a wavelength element \u0394\u03bb = {dlam4:.2f} nm near \u03bb = {lam4:.0f} nm. Compute the resolving power R.</p>')
        + problem(2, 'Radial velocity from one line', f'<p>The Na D1 line (rest \u03bb = {rest_d1} nm) is observed at {obs_d1} nm. Compute the implied radial velocity.</p>')
        + problem(3, 'Multi-line consistency', f'<p>The Na D2 line (rest \u03bb = {rest_d2} nm) is observed at {obs_d2} nm in the same spectrum. Compute its implied velocity and compare it to the D1 result from Problem 2 \u2014 do the two sodium lines agree well enough to support a single bulk velocity?</p>')
        + problem(4, 'Resolution versus shift', f'<p>Using the resolving power from Problem 1, compute the resolution element in nm at {lam4:.0f} nm, and compare it to the {shift_mag:.2f} nm shift measured for the D1 line. Is the shift clearly resolved, or comparable to the resolution limit?</p>')
    )
    write_ps(4, 'Spectroscopy', 'Calibrate spectral resolution and derive a cross-checked radial velocity from two sodium lines.', ps04_problems,
              'Verify against OpenStax Astronomy 2e Chapter 5.3 (spectroscopy) and Chapter 5.6 (the Doppler effect) before instructional release.')
    ps04_sol = (
        solution(1, 'Resolving power', f'<p>R = {lam4:.0f}/{dlam4:.2f} = {R4:.0f}.</p>', [('Correct setup', 5), ('Correct R', 10)])
        + solution(2, 'Radial velocity from one line', f'<p>\u0394\u03bb = {obs_d1}\u2212{rest_d1} = {shift_mag:.2f} nm. v = ({shift_mag:.2f}/{rest_d1})\u00d7{C_KMS:.0f} = {v_d1:.1f} km/s (recession).</p>', [('Correct \u0394\u03bb', 5), ('Correct velocity', 10)])
        + solution(3, 'Multi-line consistency', f'<p>D2: \u0394\u03bb = {obs_d2-rest_d2:.2f} nm, v = {v_d2:.1f} km/s. Mean = {mean_v4:.1f} km/s; the two lines differ by only {dev4:.1f} km/s, well within expected measurement scatter, so they support a single bulk radial velocity.</p>', [('Correct D2 velocity', 8), ('Correct consistency judgment', 7)])
        + solution(4, 'Resolution versus shift', f'<p>Resolution element = {lam4:.0f}/{R4:.0f} = {res_element:.3f} nm. The measured shift ({shift_mag:.2f} nm) is about {shift_mag/res_element:.1f}\u00d7 the resolution element, so it is clearly resolved, not merely comparable to the instrumental limit.</p>', [('Correct resolution element', 8), ('Correct comparison and judgment', 7)])
    )
    write_sol(4, 'Spectroscopy', ps04_sol)
    write_assess(4, 'Spectroscopy', [
        ('Problem 1', 15, 'Correct R.'), ('Problem 2', 15, 'Correct velocity.'),
        ('Problem 3', 15, 'Correct D2 velocity and sound consistency judgment.'), ('Problem 4', 15, 'Correct resolution element and sound comparison.'),
    ])

    # ---- PS05: Archives and Selection Effects ----
    rows5 = [
        ('S1', 6.2, 0.3, 12.5), ('S2', 3.4, 0.9, 13.0), ('S3', 9.1, 0.2, 15.5),
        ('S4', 2.0, 0.15, 11.0), ('S5', 4.5, 1.8, 10.0),
    ]
    def passes(plx, err, g):
        return (plx / err) > 5, g < 14
    ps05_table_rows = ''
    retained5 = []
    for sid, plx, err, g in rows5:
        p_ok, g_ok = passes(plx, err, g)
        if p_ok and g_ok:
            retained5.append(sid)
    ps05_problems = (
        problem(1, 'Parallax quality cut', f'<p>A source has parallax = 3.4 mas with uncertainty 0.9 mas. Compute parallax/error and state whether it passes a &gt; 5 quality cut.</p>')
        + problem(2, 'Distance from parallax', '<p>A source has parallax = 6.2 mas. Compute its distance in parsecs.</p>')
        + problem(3, 'Magnitude cut', '<p>Two sources have G = 13.2 and G = 15.8. State which pass a G &lt; 14 "bright and reliable" cut.</p>')
        + problem(4, 'Combined sample', '<p>Five sources have (parallax mas, error mas, G mag): S1 (6.2, 0.3, 12.5), S2 (3.4, 0.9, 13.0), S3 (9.1, 0.2, 15.5), S4 (2.0, 0.15, 11.0), S5 (4.5, 1.8, 10.0). Apply both the parallax/error &gt; 5 cut and the G &lt; 14 cut, and report exactly which sources are retained in the final sample.</p>')
    )
    write_ps(5, 'Archives and Selection Effects', 'Apply and combine parallax- and magnitude-quality cuts to a small archive excerpt.', ps05_problems,
              'Verify against OpenStax Astronomy 2e Chapter 19.2 (surveying the stars, parallax) before instructional release.')
    r1, e1 = 3.4, 0.9
    ps05_sol = (
        solution(1, 'Parallax quality cut', f'<p>Ratio = {r1}/{e1} = {r1/e1:.2f}, which is below 5, so this source fails the quality cut.</p>', [('Correct ratio', 8), ('Correct pass/fail', 7)])
        + solution(2, 'Distance from parallax', f'<p>d = 1000/6.2 = {1000/6.2:.1f} pc.</p>', [('Correct formula', 5), ('Correct value', 10)])
        + solution(3, 'Magnitude cut', '<p>G = 13.2 &lt; 14 passes; G = 15.8 &gt; 14 fails.</p>', [('Correct classification of both', 15)])
        + solution(4, 'Combined sample', f'<p>Parallax/error: S1={6.2/0.3:.1f} (pass), S2={3.4/0.9:.1f} (fail), S3={9.1/0.2:.1f} (pass), S4={2.0/0.15:.1f} (pass), S5={4.5/1.8:.1f} (fail). Magnitude cut (G&lt;14): S1 pass, S2 pass, S3 fail (15.5), S4 pass, S5 pass. Sources passing BOTH cuts: {", ".join(retained5)}.</p>', [('Correct parallax pass/fail for all five', 8), ('Correct final retained sample', 7)])
    )
    write_sol(5, 'Archives and Selection Effects', ps05_sol)
    write_assess(5, 'Archives and Selection Effects', [
        ('Problem 1', 15, 'Correct ratio and pass/fail.'), ('Problem 2', 15, 'Correct distance.'),
        ('Problem 3', 15, 'Correct classification of both sources.'), ('Problem 4', 15, 'Correct combined-cut sample (must match exactly).'),
    ])

    # ---- PS06: Stacking and Time-Domain Strategy ----
    snr_single6, N6 = 15.0, 16
    snr_stack6 = snr_single6 * math.sqrt(N6)
    spike6, N6b = 8000.0, 16
    bias6 = spike6 / N6b
    event6, cadence6 = 3.4, 0.75  # hours (45 min = 0.75 h)
    samples6 = event6 / cadence6
    period6, bad_cadence6, good_cadence6 = 5.2, 6.0, 1.0

    ps06_problems = (
        problem(1, 'Stacking gain', f'<p>A single exposure gives SNR = {snr_single6:.0f}. Compute the expected SNR after stacking {N6} independent, registered exposures.</p>')
        + problem(2, 'Cosmic-ray bias in a mean combine', f'<p>One frame out of {N6b} contains a cosmic-ray spike of {spike6:.0f} counts in the target pixel. Compute the bias this introduces into a simple mean combine of all {N6b} frames.</p>')
        + problem(3, 'Cadence adequacy', f'<p>An event lasts {event6:.1f} hours. A proposed cadence images the field every 45 minutes. Compute how many samples this cadence captures across the event and judge whether that is adequate to resolve ingress, minimum, and egress.</p>')
        + problem(4, 'Nyquist-style check', f'<p>A periodic signal has period {period6:.1f} hours. A {bad_cadence6:.0f}-hour cadence is proposed. Determine whether this cadence can recover the signal, and propose a cadence (such as {good_cadence6:.0f} hour) that would.</p>')
    )
    write_ps(6, 'Stacking and Time-Domain Strategy', 'Evaluate image-combination gain, cosmic-ray robustness, and observing cadence.', ps06_problems,
              'Verify against OpenStax Astronomy 2e Chapter 6.3 (detectors) and Chapter 19.3 (variable stars, cadence) before instructional release.')
    ps06_sol = (
        solution(1, 'Stacking gain', f'<p>SNR_stack \u2248 \u221a{N6} \u00d7 {snr_single6:.0f} = {math.sqrt(N6):.2f} \u00d7 {snr_single6:.0f} = {snr_stack6:.1f}.</p>', [('Correct \u221aN factor', 8), ('Correct final SNR', 7)])
        + solution(2, 'Cosmic-ray bias', f'<p>Bias = {spike6:.0f}/{N6b} = {bias6:.1f} counts added to the mean-combined pixel. A median or sigma-clipped combine would largely reject this single outlier instead.</p>', [('Correct bias value', 10), ('Correct robustness statement', 5)])
        + solution(3, 'Cadence adequacy', f'<p>Samples across event = {event6:.1f} h / 0.75 h = {samples6:.1f}. About {samples6:.0f} samples is borderline: enough to detect the event but only marginally adequate to resolve ingress/egress shape in detail; a finer cadence would be preferable.</p>', [('Correct sample count', 8), ('Reasonable adequacy judgment', 7)])
        + solution(4, 'Nyquist-style check', f'<p>Recovering a {period6:.1f} h period needs a cadence well under half the period, i.e., well under {period6/2:.1f} h. A {bad_cadence6:.0f} h cadence is coarser than that limit and risks aliasing. A {good_cadence6:.0f} h cadence satisfies \u0394t \u226a T and would adequately sample the periodic signal.</p>', [('Correct Nyquist-style limit', 8), ('Correct judgment and proposed fix', 7)])
    )
    write_sol(6, 'Stacking and Time-Domain Strategy', ps06_sol)
    write_assess(6, 'Stacking and Time-Domain Strategy', [
        ('Problem 1', 15, 'Correct stacked SNR.'), ('Problem 2', 15, 'Correct cosmic-ray bias value.'),
        ('Problem 3', 15, 'Correct sample count and reasonable adequacy judgment.'), ('Problem 4', 15, 'Correct Nyquist-style reasoning and proposed cadence.'),
    ])

    # ---- PS07: Technical Observing Report ----
    sigma_zp7, sigma_m7 = 0.03, 0.02
    sigma_total7 = math.sqrt(sigma_zp7 ** 2 + sigma_m7 ** 2)
    snr7 = 4.2
    m7 = 14.02

    ps07_problems = (
        problem(1, 'Combined uncertainty', f'<p>A calibrated magnitude has zero-point uncertainty \u00b1{sigma_zp7:.2f} mag and instrumental uncertainty \u00b1{sigma_m7:.2f} mag. Compute the combined uncertainty.</p>')
        + problem(2, 'Claim strength critique', f'<p>A draft report states "we present a definitive detection" for a source measured at SNR = {snr7:.1f}. Critique this claim using the SNR-classification rule from Lecture 4, and propose more accurate wording.</p>')
        + problem(3, 'Report-section sorting', '<p>Sort the following three sentences into Methods, Results, or Limitations: (a) "Bias and dark frames were taken at the start and end of the night." (b) "The comparison star\u2019s stability was verified only for this single night." (c) "The target\u2019s calibrated magnitude is 14.02 \u00b1 0.04."</p>')
        + problem(4, 'Final synthesis', f'<p>Using the combined uncertainty from Problem 1 and the magnitude m = {m7:.2f}, write one complete, defensible result sentence for a technical observing report, including the measurement, its uncertainty, and one explicitly stated limitation.</p>')
    )
    write_ps(7, 'Technical Observing Report', 'Assemble a defensible observing argument from the term\u2019s measurements and their uncertainties.', ps07_problems,
              'Verify against OpenStax Astronomy 2e Chapter 1.3 (scientific reasoning and communication) before instructional release.')
    ps07_sol = (
        solution(1, 'Combined uncertainty', f'<p>\u03c3_total = \u221a({sigma_zp7:.2f}\u00b2 + {sigma_m7:.2f}\u00b2) = \u221a({sigma_zp7**2:.4f} + {sigma_m7**2:.4f}) = {sigma_total7:.3f} mag.</p>', [('Quadrature method', 8), ('Correct value', 7)])
        + solution(2, 'Claim strength critique', f'<p>SNR = {snr7:.1f} falls in the marginal range (3\u20135), not the secure range (\u2265 5), so "definitive detection" overstates the evidence. Better wording: "a marginal detection (SNR \u2248 {snr7:.1f}) that should be confirmed with additional observations."</p>', [('Correct classification', 8), ('Reasonable revised wording', 7)])
        + solution(3, 'Report-section sorting', '<p>(a) Methods. (b) Limitations. (c) Results.</p>', [('All three correctly sorted', 15)])
        + solution(4, 'Final synthesis', f'<p>Example: "The target\u2019s calibrated magnitude is {m7:.2f} \u00b1 {sigma_total7:.2f} mag, combining zero-point and instrumental uncertainty in quadrature; this result assumes the comparison-field zero point remained stable throughout the night, which was not independently verified beyond this single observing session."</p>', [('Correct measurement and uncertainty stated', 8), ('Explicit, reasonable limitation stated', 7)])
    )
    write_sol(7, 'Technical Observing Report', ps07_sol)
    write_assess(7, 'Technical Observing Report', [
        ('Problem 1', 15, 'Correct combined uncertainty.'), ('Problem 2', 15, 'Correct SNR classification and reasonable revised wording.'),
        ('Problem 3', 15, 'All three sentences correctly sorted.'), ('Problem 4', 15, 'Result sentence includes measurement, uncertainty, and an explicit limitation.'),
    ])


NPIX_LABEL = 9  # placeholder used only for an f-string guard above


def write_ps(n, title, focus, problems_html, openstax_note):
    (PSET_DIR / f'problem-set-{n:02d}.html').write_text(pset_page(n, title, focus, problems_html, openstax_note), encoding='utf-8')


def write_sol(n, title, solutions_html):
    (PSET_DIR / f'problem-set-{n:02d}-solutions.html').write_text(solkey_page(n, title, solutions_html), encoding='utf-8')


def write_assess(n, title, items):
    (PSET_DIR / f'problem-set-{n:02d}-assessment.md').write_text(assessment_md(n, title, items), encoding='utf-8')


if __name__ == '__main__':
    write_labs()
    write_problem_sets()
    print('Wrote 7 lab files and 7 problem sets (with solutions and assessment instructions).')
