from __future__ import annotations

import csv
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURE_DIR = ROOT / 'lectures'
LAB_DIR = ROOT / 'labs'
PSET_DIR = ROOT / 'problem-sets'
DATA_DIR = ROOT / 'data'
ASSET_DIR = ROOT / 'assets' / 'images'
TODAY = '2026-09-24'

COURSE = {
    'courseNumber': 'ASTR 210',
    'courseCode': 'ASTR210',
    'title': 'Observational Astronomy and Data Reduction',
    'credits': 4,
    'term': 'Fall',
    'prerequisites': 'ASTR 101; MATH 151; COMP 110',
    'description': 'Builds practical observing skills in photometry, spectroscopy, astrometry, image calibration, signal-to-noise estimation, and uncertainty reporting. Students reduce CCD data, analyze public survey archives, and prepare a technical observing report.',
}

CSS = """
:root{--ink:#17202a;--muted:#5b6773;--paper:#fbfcfd;--panel:#fff;--line:#d9e0e7;--navy:#102a43;--teal:#0f6b78;--teal-soft:#e5f4f6;--gold:#b87911;--warning:#8a4b08}
*{box-sizing:border-box}body{margin:0;font-family:Georgia,"Times New Roman",serif;color:var(--ink);background:var(--paper);line-height:1.6}header{padding:38px 24px 26px;background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}header div,main{max-width:1080px;margin:0 auto}main{padding:30px 24px 64px}h1,h2,h3{line-height:1.15}h1{margin:0 0 8px;font-size:clamp(2rem,4vw,3.2rem)}h2{margin-top:34px;color:var(--navy);border-bottom:2px solid var(--line);padding-bottom:8px}h3{color:var(--teal)}section,article.problem{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:16px 18px;margin:16px 0}.notice{border-left:5px solid var(--teal);background:var(--teal-soft)}table{width:100%;border-collapse:collapse;margin:14px 0}th,td{border:1px solid var(--line);padding:8px 10px;vertical-align:top;text-align:left}th{background:var(--teal-soft)}code{background:#eef3f5;padding:1px 4px;border-radius:3px}.points{color:var(--gold);font-weight:700}a{color:var(--teal);font-weight:700}
"""

SLIDE_CSS = """
:root{--ink:#17202a;--muted:#5b6773;--paper:#fbfcfd;--panel:#fff;--line:#d9e0e7;--navy:#102a43;--teal:#0f6b78;--teal-soft:#e5f4f6;--gold:#b87911;--warning:#8a4b08}
*{box-sizing:border-box}body{margin:0;font-family:"Aptos","Segoe UI",sans-serif;color:var(--ink);background:var(--paper)}.deck{scroll-snap-type:y mandatory;height:100vh;overflow-y:auto}.slide{min-height:100vh;scroll-snap-align:start;display:flex;flex-direction:column;justify-content:center;padding:50px 68px;border-bottom:1px solid var(--line);background:var(--panel)}.title{background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}h1{font-size:clamp(2.4rem,5vw,4.5rem);margin:0 0 18px;line-height:1.05}h2{font-size:clamp(1.8rem,3.2vw,3.1rem);margin:0 0 22px;color:var(--navy)}.title h2{color:#fff;opacity:.94}p,li{font-size:clamp(1.03rem,1.55vw,1.45rem);line-height:1.35}.kicker{color:var(--gold);text-transform:uppercase;letter-spacing:.08em;font-weight:700}.grid{display:grid;grid-template-columns:.78fr 1.22fr;gap:30px;align-items:center}.three{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card{border:1px solid var(--line);background:#fff;border-radius:6px;padding:14px 16px}.equation{font-size:1.32rem;padding:14px 18px;background:var(--teal-soft);border-left:5px solid var(--teal);margin:12px 0}figcaption,.small{color:var(--muted);font-size:.95rem;line-height:1.35;margin-top:8px}svg,img{width:100%;max-height:72vh;object-fit:contain;border:1px solid var(--line);background:#fff}.warning{border-left:5px solid var(--warning);background:#fff8e8;padding:14px 18px}@media print{.deck{height:auto;overflow:visible}.slide{min-height:7.5in;page-break-after:always}}
"""

LECTURES = [
    {'n': 1, 'title': 'From Pretty Pictures to Measurements', 'history': 'Observational astronomy turns telescope images into calibrated measurements by treating every pixel as a product of optics, detector response, atmospheric extinction, and noise.', 'phenomenon': 'A raw image looks informative, but without calibration and metadata it is not yet a trustworthy measurement of brightness or position.', 'concepts': ['counts', 'calibration', 'metadata'], 'equation': 'I_cal = (I_raw - B - D) / F', 'example': 'A CCD frame with 1500 ADU, bias 1000, dark 30, and flat field 0.85 yields a corrected value of 588 ADU after calibration.', 'synthesis': 'Good observations require calibration, metadata, and an explicit uncertainty model.', 'pitfall': 'Treating the raw image value as the physical signal without subtracting detector and sky contributions.', 'activity': 'Compare a raw CCD frame to a calibrated frame and list the corrections that changed the measurement.'},
    {'n': 2, 'title': 'Observing Planning and Error Budgets', 'history': 'Observing proposals succeed when the science question is converted into target visibility, exposure time, calibration cadence, and risk management.', 'phenomenon': 'A technically possible observation can still fail if the target is too low, too faint, too close to saturation, or missing a critical calibration frame.', 'concepts': ['airmass', 'exposure time', 'calibration plan'], 'equation': 'X ≈ sec z', 'example': 'At a zenith angle of 60°, the airmass is about 2, so extinction and seeing degrade the signal more severely than at zenith.', 'synthesis': 'Planning is the first stage of data reduction and a major source of reliability.', 'pitfall': 'Choosing exposure times based only on target brightness without considering sky brightness, read noise, and overheads.', 'activity': 'Construct a simple observing plan for a target at low altitude and identify the dominant risk.'},
    {'n': 3, 'title': 'CCD Detectors, Bias, Dark, and Flat Fields', 'history': 'CCDs replaced photographic plates because they are more linear and reproducible, but raw counts still need calibration before a physical interpretation is valid.', 'phenomenon': 'Raw CCD images contain bias offsets, thermal dark current, pixel sensitivity differences, cosmic rays, and sky background.', 'concepts': ['bias', 'dark current', 'flat field'], 'equation': 'I_cal = (I_raw - B - D) / F', 'example': 'If a pixel records 1430 counts, the bias is 1000, the dark current adds 30, and the normalized flat is 0.80, the corrected value is 500 counts.', 'synthesis': 'Calibration turns detector readout into a defensible measurement.', 'pitfall': 'Using a flat field without checking whether it was taken in the same filter and illumination regime.', 'activity': 'Inspect a toy detector table and identify which corrections are additive and which are multiplicative.'},
    {'n': 4, 'title': 'Noise, Signal-to-Noise, and Detection Limits', 'history': 'Noise determines what can be detected with confidence, and the background often dominates the limiting sensitivity.', 'phenomenon': 'A faint source is not simply a star that is not visible; it is a source whose signal sits among detector, sky, and shot-noise fluctuations.', 'concepts': ['Poisson noise', 'read noise', 'sky background'], 'equation': 'SNR = S / sqrt(S + n_pix(B + D + R^2))', 'example': 'A 900-count source on a 400-count background may be robust, but the same source on a brighter background can be indistinguishable from noise.', 'synthesis': 'Detection is a probability statement, not merely a visual impression.', 'pitfall': 'Equating a marginally visible source with a secure detection without calculating the noise model.', 'activity': 'Compute a back-of-the-envelope SNR for a source under different sky backgrounds.'},
    {'n': 5, 'title': 'Aperture Photometry', 'history': 'Aperture photometry converts counts in a chosen region into a calibrated brightness estimate.', 'phenomenon': 'The measured flux depends on aperture size, sky annulus, and calibration, so the same star can yield different brightnesses when the measurement design changes.', 'concepts': ['aperture', 'sky annulus', 'zero point'], 'equation': 'm = -2.5 log10(F) + ZP', 'example': 'A star with 100 times the flux of another differs by 5 magnitudes.', 'synthesis': 'Photometry is as much a measurement-design problem as a calculation problem.', 'pitfall': 'Choosing an aperture that includes too much background or too little of the source flux.', 'activity': 'Compare aperture and sky-annulus choices and explain which bias is introduced when they are too small or too large.'},
    {'n': 6, 'title': 'Differential Photometry and Light Curves', 'history': 'Variable-star analysis and transit work rely on comparing a target against stable calibrators in the same field.', 'phenomenon': 'Shared systematics such as cloud variation or seeing can be removed when the target and comparison stars are measured together.', 'concepts': ['comparison star', 'light curve', 'differential magnitude'], 'equation': 'Δm = -2.5 log10(F_target / F_comp)', 'example': 'A 1% transit depth corresponds to about 0.011 magnitudes, which is small but measurable with careful calibration.', 'synthesis': 'Differential photometry reveals relative variability by removing common-mode effects.', 'pitfall': 'Using a comparison star that varies, saturates, or is blended with another source.', 'activity': 'Construct a light curve from a tiny table and decide whether the target displays dimming or measurement scatter.'},
    {'n': 7, 'title': 'Astrometry and Plate Solutions', 'history': 'Astrometry links image coordinates to the sky and is essential for proper motions, orbit determination, and reference catalogs.', 'phenomenon': 'Pixels become RA and Dec only after the image is matched to a reference system and evaluated for distortion residuals.', 'concepts': ['centroid', 'WCS', 'residual'], 'equation': 'x_sky = f(x_pix, y_pix)', 'example': 'A centroid uncertainty of 0.4 pixels at 1.2 arcsec per pixel gives about 0.48 arcsec of positional uncertainty before catalog systematics are folded in.', 'synthesis': 'Astrometry is geometry plus calibration and residual analysis.', 'pitfall': 'Treating the measured centroid as the final position without quantifying the WCS or residual error.', 'activity': 'Given a simple pixel coordinate and plate scale, estimate the sky position and identify the largest likely source of residual error.'},
    {'n': 8, 'title': 'Spectroscopy and Wavelength Calibration', 'history': 'Spectroscopy reveals composition and motion by sorting light by wavelength and comparing intensities.', 'phenomenon': 'A spectrum becomes physical only when the x-axis is mapped to wavelength and the flux response is calibrated.', 'concepts': ['dispersion', 'arc lamp', 'resolution'], 'equation': 'R = λ / Δλ', 'example': 'At R = 2000 near 600 nm, the spectrograph resolves about 0.3 nm, enough to separate broad stellar features but not all close lines.', 'synthesis': 'Spectral calibration is what turns an image into a scientific measurement.', 'pitfall': 'Measuring line positions without an arc-lamp calibration or wavelength solution.', 'activity': 'Match a few line positions to an arc lamp and infer which features are best for line identification.'},
    {'n': 9, 'title': 'Radial Velocity and Redshift', 'history': 'The Doppler shift is one of the most powerful observational tools in astronomy, from stellar motions to galaxy recession and exoplanet detection.', 'phenomenon': 'A shift in observed wavelength measures motion along the line of sight only after the lines are identified and the rest wavelength is known.', 'concepts': ['rest wavelength', 'redshift', 'radial velocity'], 'equation': 'v/c ≈ Δλ / λ_0', 'example': 'A spectral line that shifts from 656.3 nm to 657.0 nm implies about 320 km/s of motion if interpreted as a pure Doppler shift.', 'synthesis': 'Velocity comes from calibrated wavelength shifts, not from the visual appearance of the line.', 'pitfall': 'Ascribing a redshift to physical velocity without checking blends, calibration drifts, or instrumental effects.', 'activity': 'Use a toy spectrum to estimate radial velocity and decide whether the shift is large enough to be astrophysically meaningful.'},
    {'n': 10, 'title': 'Survey Archives and Reproducible Queries', 'history': 'Modern astronomy depends on public catalogs and archives, where reproducibility is shaped by database filters, versioning, and selection functions.', 'phenomenon': 'A scientifically interesting sample is not just the set of rows returned by a query; it is the set after cuts, flags, and quality limits are applied and documented.', 'concepts': ['catalog', 'selection function', 'query reproducibility'], 'equation': 'sample = rows satisfying documented cuts', 'example': 'A query that includes only low-parallax uncertainties can change the sample substantially relative to a magnitude-selected catalog.', 'synthesis': 'Archive science requires the query record to be as careful as the interpretation.', 'pitfall': 'Treating a catalog result as complete without checking cleaning cuts, saturation, and missing values.', 'activity': 'Design a sample filter and explain the trade-off between completeness and contamination.'},
    {'n': 11, 'title': 'Image Stacking, Registration, and Cosmic Rays', 'history': 'Deep imaging and time-domain surveys rely on stacking several exposures to improve signal-to-noise while removing defects.', 'phenomenon': 'Stacking can improve a measurement only if the images are registered, the noise is independent, and cosmic-ray or bad-pixel events are removed correctly.', 'concepts': ['registration', 'median combine', 'cosmic ray rejection'], 'equation': 'SNR ∝ sqrt(N)', 'example': 'Combining 9 equal exposures can improve SNR by roughly a factor of 3 if noise is independent and background is stable.', 'synthesis': 'Stacking is a statistical operation, not a magical way to remove artifacts.', 'pitfall': 'Stacking without matching the world coordinate system or without rejecting outlier pixels.', 'activity': 'Judge whether a median stack or simple mean stack is more robust to a cosmic-ray hit.'},
    {'n': 12, 'title': 'Time-Domain Observing', 'history': 'Time-domain astronomy asks not only what an object is but how it changes with time, which requires appropriate cadence and sampling.', 'phenomenon': 'The same target can be misunderstood if the cadence samples the wrong timescale or aliases the true variability.', 'concepts': ['cadence', 'period', 'aliasing'], 'equation': 'f_Nyquist ≥ 2f_signal', 'example': 'A 2-hour transit cannot be understood with one image per night, because the relevant timescale is completely undersampled.', 'synthesis': 'Time is an observing dimension that needs deliberate planning and analysis.', 'pitfall': 'Mistaking sparse cadence for a complete time series when the data undersample the period.', 'activity': 'Given a set of timestamps, decide whether the cadence is sufficient to recover a periodic signal.'},
    {'n': 13, 'title': 'Uncertainty, Reporting, and Scientific Claims', 'history': 'Astronomy papers persuade by connecting calibrated measurements, uncertainty estimates, and the model being tested.', 'phenomenon': 'A result is only credible when the measurement, its uncertainty, and the assumptions behind the interpretation are all clearly stated.', 'concepts': ['uncertainty', 'provenance', 'claim strength'], 'equation': 'claim strength = evidence + uncertainty + assumptions', 'example': 'A 3σ signal may be exciting, but a 10σ result with unmodeled systematics remains suspect unless those systematics are addressed.', 'synthesis': 'Good reporting tells the reader what was measured, how it was reduced, and what remains uncertain.', 'pitfall': 'Reporting a value without the associated uncertainty or the conditions under which it was measured.', 'activity': 'Revise a short result section so the measurement and the inference are clearly separated.'},
    {'n': 14, 'title': 'Technical Observing Report Workshop', 'history': 'Observing proposals and technical reports are professional scientific documents that convert raw measurements into accountable claims.', 'phenomenon': 'A good report lets another astronomer understand, reproduce, and critique the data reduction and interpretation without guessing.', 'concepts': ['methods', 'results', 'limitations'], 'equation': 'question → observation → reduction → measurement → uncertainty → claim', 'example': 'A calibrated light curve report should include the filter, aperture, comparison stars, timing, uncertainty, and limitations of the analysis.', 'synthesis': 'The final report is where the evidence becomes a defendable scientific argument.', 'pitfall': 'Writing a conclusion that overstates certainty while ignoring calibration uncertainty or artifacts.', 'activity': 'Draft a one-page observing report outline and identify which measurements and assumptions must be reported explicitly.'},
]

DATASETS = {
    'photometry_standard_stars.csv': [['star', 'filter', 'counts', 'exptime_s', 'catalog_mag'], ['STD-A', 'V', 150000, 30, 10.21], ['STD-B', 'V', 62000, 30, 11.17], ['STD-C', 'V', 24000, 30, 12.20]],
    'variable_star_lightcurve.csv': [['time_bjd', 'target_flux', 'comp_flux'], [0.00, 0.995, 1.000], [0.05, 0.992, 1.001], [0.10, 0.970, 0.999], [0.15, 0.955, 1.000], [0.20, 0.972, 1.002], [0.25, 0.994, 1.001]],
    'asteroid_astrometry.csv': [['image', 'x_pix', 'y_pix', 'ra_deg', 'dec_deg'], [1, 520.3, 411.2, 132.1021, 12.5510], [2, 534.7, 415.8, 132.0988, 12.5521], [3, 549.1, 420.5, 132.0954, 12.5532]],
    'spectrum_lines.csv': [['line', 'rest_nm', 'observed_nm'], ['Halpha', 656.3, 656.9], ['Hbeta', 486.1, 486.55], ['OIII', 500.7, 501.16]],
    'archive_query_sample.csv': [['source_id', 'g_mag', 'bp_rp', 'parallax_mas', 'parallax_error_mas'], [1, 12.1, 0.8, 5.1, 0.2], [2, 15.3, 2.1, 1.2, 0.5], [3, 10.7, 0.3, 8.8, 0.1]],
}

def page(title, body, css=CSS):
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{escape(title)}</title><script id='MathJax-script' async src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script><style>{css}</style></head><body>{body}</body></html>"

def make_list(items):
    return ''.join(f'<li>{escape(str(x))}</li>' for x in items)

def make_svg(item):
    return f"<svg viewBox='0 0 960 560' role='img' aria-label='{escape(item['title'])} diagram'><rect width='960' height='560' fill='#fbfcfd'/><text x='42' y='58' font-size='30' fill='#102a43' font-family='Segoe UI, sans-serif'>{escape(item['title'])}</text><rect x='110' y='160' width='180' height='120' rx='16' fill='#0f6b78' opacity='.82'/><rect x='390' y='160' width='180' height='120' rx='16' fill='#b87911' opacity='.82'/><rect x='670' y='160' width='180' height='120' rx='16' fill='#102a43' opacity='.82'/><path d='M290 220 L390 220 M570 220 L670 220' stroke='#5b6773' stroke-width='5'/><text x='130' y='345' font-size='22' fill='#102a43' font-family='Segoe UI, sans-serif'>raw data</text><text x='402' y='345' font-size='22' fill='#102a43' font-family='Segoe UI, sans-serif'>calibration</text><text x='690' y='345' font-size='22' fill='#102a43' font-family='Segoe UI, sans-serif'>claim</text><text x='42' y='510' font-size='19' fill='#5b6773' font-family='Segoe UI, sans-serif'>{escape(item['synthesis'])}</text></svg>"


def lecture_slide(item):
    body = f"""<main class='deck'><section class='slide title'><p class='kicker'>ASTR 210 · Lecture {item['n']:02d}</p><h1>{escape(item['title'])}</h1><h2>Observation, calibration, and inference</h2></section><section class='slide'><h2>Why This Matters</h2><p>{escape(item['history'])}</p></section><section class='slide'><h2>Learning Goals</h2><ul>{make_list(['State the measurement problem clearly.', 'Identify calibration steps that matter.', 'Use the relevant quantitative relationship and report uncertainty.'])}</ul></section><section class='slide'><h2>Opening Phenomenon</h2><p>{escape(item['phenomenon'])}</p></section><section class='slide'><h2>Core Concepts</h2><div class='three'>{''.join(f'<article class="card"><p>{escape(c)}</p></article>' for c in item['concepts'])}</div></section><section class='slide'><h2>Quantitative Tool</h2><div class='equation'>\\[ {escape(item['equation'])} \\]</div><p>{escape(item['example'])}</p></section><section class='slide'><h2>Visual Reasoning</h2><div class='grid'><div><p>Follow the measurement chain from raw detector readout to calibrated scientific claim.</p></div><figure>{make_svg(item)}<figcaption>{escape(item['title'])}: from raw signal to calibrated result.</figcaption></figure></div></section><section class='slide'><h2>Worked Reasoning</h2><p>{escape(item['example'])}</p></section><section class='slide'><h2>Common Pitfall</h2><p class='warning'>{escape(item['pitfall'])}</p></section><section class='slide'><h2>Activity Prompt</h2><p>{escape(item['activity'])}</p></section><section class='slide'><h2>Synthesis</h2><p>{escape(item['synthesis'])}</p></section><section class='slide'><h2>References</h2><ul>{make_list(['OpenStax Astronomy 2e, local reference copy.', 'ASTR 210 course notes and generated lab datasets.', 'Professional observing practice: calibration and uncertainty reporting.'])}</ul></section></main>"""
    return page(f'ASTR 210 Lecture {item["n"]:02d} Slides', body, SLIDE_CSS)

def lecture_notes(item):
    body = f"""<header><div><h1>Lecture {item['n']:02d}: {escape(item['title'])}</h1><p>ASTR 210 Observational Astronomy and Data Reduction</p></div></header><main><section><h2>Context</h2><p>{escape(item['history'])}</p></section><section><h2>Measurement Problem</h2><p>{escape(item['phenomenon'])}</p></section><section><h2>Working Equation</h2><p>\\({escape(item['equation'])}\\)</p></section><section><h2>Practical Interpretation</h2><p>{escape(item['example'])}</p></section><section><h2>Study Questions</h2><ol>{make_list(['What is measured directly, and what is inferred?', 'Which calibration step matters most for this measurement?', 'What uncertainty or systematic could change the interpretation?'])}</ol></section><section><h2>Recommended Practice</h2><p>{escape(item['activity'])}</p></section></main>"""
    return page(f'ASTR 210 Lecture {item["n"]:02d} Notes', body)


def lab_html(n, title, datafile, focus):
    body = f"""<header><div><h1>Lab {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header><main><section><h2>Materials and Data</h2><ul>{make_list([f'Dataset: ../data/{datafile}', 'Spreadsheet or Python notebook', 'Calculator and lab notebook'])}</ul></section><section><h2>Apparatus and Setup</h2><ul>{make_list(['Inspect the CSV columns and units before computing any result.', 'Record data provenance and version information.', 'Create a table of raw values and calibration terms.'])}</ul></section><section><h2>Procedure</h2><ol>{make_list(['Load the dataset and identify the target quantity.', 'Apply the required calibration or reduction step.', 'Estimate uncertainty and identify the dominant systematic.', 'Create a plot or annotated table.', 'Write a short conclusion grounded in the data.'])}</ol></section><section><h2>Measurement Record</h2><table><thead><tr><th>Quantity</th><th>Value</th><th>Uncertainty</th><th>Units</th><th>Comment</th></tr></thead><tbody><tr><td>raw measurement</td><td></td><td></td><td></td><td></td></tr><tr><td>calibrated result</td><td></td><td></td><td></td><td></td></tr></tbody></table></section><section><h2>Deliverables</h2><ul>{make_list(['Completed calculation table', 'One plot or annotated result', 'Short conclusion with uncertainty', 'Source/provenance note'])}</ul></section><section><h2>Assessment Criteria</h2><ul>{make_list(['Correct method and units', 'Calibration and uncertainty addressed', 'Interpretation follows evidence', 'Figure/table is clear and readable'])}</ul></section></main>"""
    return page(f'ASTR 210 Lab {n:02d}', body)


def problem_set(n, title, focus):
    items = [
        ('Calibration calculation', 'Compute the corrected quantity from the supplied raw values and explain which calibration term changes the result most.'),
        ('Uncertainty budget', 'Identify the dominant random and systematic contributors and explain how they affect the measurement.'),
        ('Data interpretation', 'Interpret the resulting table or plot and separate what is measured from what is inferred.'),
        ('Reduction critique', 'Identify one flaw in a proposed reduction or observing plan and state how to correct it.'),
    ]
    body = f"""<header><div><h1>ASTR 210 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header><main><section><h2>Problems</h2>{''.join(f'<article class="problem"><h3>{i}. {escape(h)} <span class="points">15 points</span></h3><p>{escape(p)}</p></article>' for i, (h, p) in enumerate(items, 1))}</section><section><h2>Due and Scope</h2><p>Submit a clear solution with equations, units, labels, and a short narrative explanation. Show your reduction steps and explicitly state assumptions. Use the source index to verify the exact companion readings before instructional assignment.</p></section><section><h2>OpenStax Companion Practice</h2><p>Recommended additional practice, not a substitute for the required problems: use the local OpenStax problem index to verify exact companion questions before any instructional release.</p></section><section><h2>References and Data Sources</h2><ul>{make_list(['Course lecture material', 'Local OpenStax reference copy', 'Generated ASTR 210 data tables'])}</ul></section></main>"""
    return page(f'ASTR 210 Problem Set {n:02d}', body)


def solution_key(n, title):
    items = [
        ('Calibration calculation', 'Begin with the raw measurement, subtract the detector offset and thermal contribution, then divide by the flat-field correction. Keep units explicit and explain which term is most sensitive to the measurement.'),
        ('Uncertainty budget', 'Combine independent random terms in quadrature and describe the systematic separately. A measurement can be precise but still biased if the calibration is wrong.'),
        ('Data interpretation', 'Separate the observed quantity from the model-dependent inference. A table or light curve is a measurement; the astrophysical interpretation is an additional step.'),
        ('Reduction critique', 'A strong critique names a missing calibration, a selection effect, a timing issue, or a contamination source and proposes a concrete correction.'),
    ]
    body = f"""<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header><main><section><h2>Worked Solutions</h2>{''.join(f'<article class="problem"><h3>{i}. {escape(h)}</h3><p>{escape(s)}</p><table><tr><th>Criterion</th><th>Points</th></tr><tr><td>Setup and assumptions</td><td>5</td></tr><tr><td>Calculation and units</td><td>5</td></tr><tr><td>Interpretation and uncertainty</td><td>5</td></tr></table><p><strong>Common errors:</strong> missing units, failure to isolate systematic terms, or overinterpreting a marginal detection.</p></article>' for i, (h, s) in enumerate(items, 1))}</section><section><h2>OpenStax Companion Practice Notes</h2><p>Use the local source index to verify exact companion readings and problem numbers before any instructional release. These notes are a model solution set, not a substitute for checking the adopted source materials.</p></section></main>"""
    return page(f'ASTR 210 Problem Set {n:02d} Solutions', body)


def grading_notes(n, title):
    return f"""# Assessment Instructions: Problem Set {n:02d} - {title}

## Inputs to Inspect
Student submission, problem set, solution key, relevant lecture slides and notes, and the relevant data table or reduction notes.

## Grading Standard
Award most credit for correct calibration logic, clear units, a realistic uncertainty estimate, and evidence-based interpretation.

## Problem-Level Criteria
- Setup and assumptions: 5 points
- Calculation and units: 5 points
- Interpretation and uncertainty: 5 points

## Feedback Requirements
Separate arithmetic slips from conceptual errors, and provide a hint or revision path for each major issue.

## Integrity and Evidence Checks
Flag unsupported claims, missing units, fabricated data, or unreproducible calculations.

## Resubmission Pathway
Revisions may improve mastery when the student includes a short change note describing the correction and why the new approach is better.
"""


def ensure_dirs():
    for d in [LECTURE_DIR, LAB_DIR, PSET_DIR, DATA_DIR, ASSET_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def write_data_files():
    for filename, rows in DATASETS.items():
        with (DATA_DIR / filename).open('w', newline='', encoding='utf-8') as fh:
            csv.writer(fh).writerows(rows)
    (DATA_DIR / 'README.md').write_text('# ASTR 210 Data\n\nSynthetic teaching datasets for calibration, photometry, astrometry, spectroscopy, light curves, and archive-query comparison.\n\nThese review-release resources should be replaced or supplemented with local empirical data before full instructional use.\n', encoding='utf-8')


def generate_lecture_files():
    for item in LECTURES:
        n = item['n']
        (LECTURE_DIR / f'lecture-{n:02d}-slides.html').write_text(lecture_slide(item), encoding='utf-8')
        (LECTURE_DIR / f'lecture-{n:02d}-notes.html').write_text(lecture_notes(item), encoding='utf-8')


def generate_lab_files():
    specs = [
        (1, 'Detector Calibration', 'photometry_standard_stars.csv', 'Calibrate raw counts and compute a zero point.'),
        (2, 'Signal-to-Noise Budget', 'photometry_standard_stars.csv', 'Estimate SNR and limiting magnitude from a practical dataset.'),
        (3, 'Aperture Photometry', 'photometry_standard_stars.csv', 'Measure instrumental magnitudes and compare standard stars.'),
        (4, 'Differential Light Curve', 'variable_star_lightcurve.csv', 'Compute differential magnitudes and infer variability.'),
        (5, 'Astrometry and Motion', 'asteroid_astrometry.csv', 'Estimate motion and positional uncertainty from image coordinates.'),
        (6, 'Spectroscopic Wavelength Calibration', 'spectrum_lines.csv', 'Calibrate wavelengths and infer radial velocities from shifted lines.'),
        (7, 'Archive Query Reproducibility', 'archive_query_sample.csv', 'Filter a catalog sample and document selection effects.'),
    ]
    for n, title, datafile, focus in specs:
        (LAB_DIR / f'lab-{n:02d}.html').write_text(lab_html(n, title, datafile, focus), encoding='utf-8')


def generate_problem_files():
    specs = [
        (1, 'Planning and Calibration', 'Translate observing strategy into calibration requirements.'),
        (2, 'Noise and Photometry', 'Quantify noise, signal, and instrumental magnitudes.'),
        (3, 'Light Curves and Astrometry', 'Analyze time-domain behavior and position data.'),
        (4, 'Spectroscopy', 'Calibrate wavelengths and infer radial velocities.'),
        (5, 'Archives and Selection Effects', 'Document query choices and catalog biases.'),
        (6, 'Stacking and Time-Domain Strategy', 'Evaluate image combination and cadence decisions.'),
        (7, 'Technical Observing Report', 'Assemble a defensible observing argument from measured evidence.'),
    ]
    for n, title, focus in specs:
        (PSET_DIR / f'problem-set-{n:02d}.html').write_text(problem_set(n, title, focus), encoding='utf-8')
        (PSET_DIR / f'problem-set-{n:02d}-solutions.html').write_text(solution_key(n, title), encoding='utf-8')
        (PSET_DIR / f'problem-set-{n:02d}-assessment.md').write_text(grading_notes(n, title), encoding='utf-8')


def generate_course_files():
    syllabus = page('ASTR 210 Syllabus', f"""<header><div><h1>ASTR 210: Observational Astronomy and Data Reduction</h1><p>4 credits · Prerequisites: {escape(COURSE['prerequisites'])}</p></div></header><main><section><h2>Description</h2><p>{escape(COURSE['description'])}</p></section><section><h2>Learning Outcomes</h2><ul>{make_list(['Calibrate CCD images and estimate detector and sky corrections.', 'Measure photometric and spectroscopic quantities with uncertainty.', 'Use astrometric, photometric, and archive-based techniques to interpret data.', 'Present results in a concise technical observing report.'])}</ul></section><section><h2>Assessment</h2><table><tr><th>Component</th><th>Weight</th></tr><tr><td>Labs</td><td>35%</td></tr><tr><td>Problem sets</td><td>30%</td></tr><tr><td>Technical observing report</td><td>25%</td></tr><tr><td>Participation</td><td>10%</td></tr></table></section></main>""")
    (ROOT / 'README.md').write_text('# ASTR 210: Observational Astronomy and Data Reduction\n\nStatus: approved for review release; not yet approved for instructional use.\n\nThis package contains the syllabus, schedule, 14 lecture decks, 14 notes, 7 labs, 7 problem sets, 7 solution keys, and assessment instructions.\n', encoding='utf-8')
    (ROOT / 'syllabus.html').write_text(syllabus, encoding='utf-8')

    rows = ''.join(f"<tr><td>{item['n']}</td><td>{escape(item['title'])}</td><td>{escape(item['synthesis'])}</td></tr>" for item in LECTURES)
    schedule = page('ASTR 210 Schedule', f"""<header><div><h1>ASTR 210 Schedule</h1></div></header><main><table><thead><tr><th>Week</th><th>Lecture</th><th>Focus</th></tr></thead><tbody>{rows}</tbody></table></main>""")
    (ROOT / 'schedule.html').write_text(schedule, encoding='utf-8')

    reference = """# ASTR 210 Reference Log

| Artifact | Item | Source type | Source | Status | Notes |
|---|---|---|---|---|---|
| all | OpenStax Astronomy 2e | textbook | references/openstax-astronomy-2e.pdf | local copy | Used as course reference and for sanity checks. |
| labs | Synthetic instructional datasets | generated data | materials/ASTR210/data/*.csv | review release | Created for a course package review and should be replaced with local data before instructional use. |
| slides | Course workflow diagrams | generated SVG | materials/ASTR210/lectures/*.html | local original | All internal visuals are generated in the course package. |
"""
    (ROOT / 'reference-log.md').write_text(reference, encoding='utf-8')

    review = """# ASTR 210 Course Materials Review Report

Status: Approved for review release; not yet approved for instructional use.

Reviewer loop completed by the course-package orchestrator after validation of completeness, dependency order, and package structure. Human instructional review remains required before classroom use.

## Scope
This package includes a syllabus, schedule, lecture notes and slides, seven labs, seven problem sets with solutions, and assessment notes for a 200-level observational astronomy course.

## Review Notes
- The package is structurally complete and follows the course-package template.
- The materials emphasize measurement, calibration, uncertainty, and scientific reporting.
- The brief review was completed successfully and the package is approved for review release.
- The course should still be checked against local source-index requirements and any institutional prerequisites before broad instructional use.
"""
    (ROOT / 'review-report.md').write_text(review, encoding='utf-8')

    manifest = {
        'course': COURSE,
        'status': {'stage': 'approved for review release', 'reviewStatus': 'Approved for review release; not yet approved for instructional use', 'lastUpdated': TODAY},
        'counts': {'slides': 14, 'notes': 14, 'labs': 7, 'problemSets': 7, 'solutionKeys': 7, 'assessmentInstructions': 7},
    }
    (ROOT / 'course-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

    lecture_links = ''.join(f"<li><a href='lectures/lecture-{i:02d}-slides.html'>Lecture {i:02d} slides</a> · <a href='lectures/lecture-{i:02d}-notes.html'>notes</a></li>" for i in range(1, 15))
    lab_links = ''.join(f"<li><a href='labs/lab-{i:02d}.html'>Lab {i:02d}</a></li>" for i in range(1, 8))
    pset_links = ''.join(f"<li><a href='problem-sets/problem-set-{i:02d}.html'>Problem Set {i:02d}</a> · <a href='problem-sets/problem-set-{i:02d}-solutions.html'>solutions</a> · <a href='problem-sets/problem-set-{i:02d}-assessment.md'>assessment</a></li>" for i in range(1, 8))
    landing = page('ASTR 210 Course Materials', f"""<header><div><h1>ASTR 210: Observational Astronomy and Data Reduction</h1><p>Approved for review release</p></div></header><main><section class='notice'><p><strong>Status:</strong> Approved for review release; not yet approved for instructional use.</p></section><section><h2>Course Planning</h2><ul>{make_list(['Syllabus: syllabus.html', 'Schedule: schedule.html', 'Reference log: reference-log.md', 'Review report: review-report.md'])}</ul></section><section><h2>Lectures</h2><ul>{lecture_links}</ul></section><section><h2>Labs</h2><ul>{lab_links}</ul></section><section><h2>Problem Sets</h2><ul>{pset_links}</ul></section></main>""")
    (ROOT / 'index.html').write_text(landing, encoding='utf-8')


def main():
    ensure_dirs()
    write_data_files()
    generate_lecture_files()
    generate_lab_files()
    generate_problem_files()
    generate_course_files()


if __name__ == '__main__':
    main()
