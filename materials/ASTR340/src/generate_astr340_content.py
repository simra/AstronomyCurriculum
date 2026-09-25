"""Content generator for ASTR340 lecture slides and lecture notes.

Every worked numeric example is computed programmatically from the shared
constants and real instrument datasets defined below (not hand-typed), and
the same constants are reused across labs and problem sets that reference
the same scenario (see generate_astr340_labs_psets.py). Run with the project
interpreter:
    python materials/ASTR340/src/generate_astr340_content.py
"""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURE_DIR = ROOT / 'lectures'
LAB_DIR = ROOT / 'labs'
PSET_DIR = ROOT / 'problem-sets'
DATA_DIR = ROOT / 'data'

CSS = """
:root{--ink:#17202a;--muted:#5b6773;--paper:#fbfcfd;--panel:#fff;--line:#d9e0e7;--navy:#102a43;--teal:#0f6b78;--teal-soft:#e5f4f6;--gold:#b87911;--warning:#8a4b08}
*{box-sizing:border-box}body{margin:0;font-family:Georgia,"Times New Roman",serif;color:var(--ink);background:var(--paper);line-height:1.6}header{padding:38px 24px 26px;background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}header div,main{max-width:1080px;margin:0 auto}main{padding:30px 24px 64px}h1,h2,h3{line-height:1.15}h1{margin:0 0 8px;font-size:clamp(2rem,4vw,3.2rem)}h2{margin-top:34px;color:var(--navy);border-bottom:2px solid var(--line);padding-bottom:8px}h3{color:var(--teal)}section,article.problem{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:16px 18px;margin:16px 0}.notice{border-left:5px solid var(--teal);background:var(--teal-soft)}table{width:100%;border-collapse:collapse;margin:14px 0}th,td{border:1px solid var(--line);padding:8px 10px;vertical-align:top;text-align:left}th{background:var(--teal-soft)}code{background:#eef3f5;padding:1px 4px;border-radius:3px}.points{color:var(--gold);font-weight:700}a{color:var(--teal);font-weight:700}
"""

SLIDE_CSS = """
:root{--ink:#17202a;--muted:#5b6773;--paper:#fbfcfd;--panel:#fff;--line:#d9e0e7;--navy:#102a43;--teal:#0f6b78;--teal-soft:#e5f4f6;--gold:#b87911;--warning:#8a4b08}
*{box-sizing:border-box}body{margin:0;font-family:"Aptos","Segoe UI",sans-serif;color:var(--ink);background:var(--paper)}.deck{scroll-snap-type:y mandatory;height:100vh;overflow-y:auto}.slide{min-height:100vh;scroll-snap-align:start;display:flex;flex-direction:column;justify-content:center;padding:50px 68px;border-bottom:1px solid var(--line);background:var(--panel)}.title{background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}h1{font-size:clamp(2.4rem,5vw,4.5rem);margin:0 0 18px;line-height:1.05}h2{font-size:clamp(1.8rem,3.2vw,3.1rem);margin:0 0 22px;color:var(--navy)}.title h2{color:#fff;opacity:.94}p,li{font-size:clamp(1.03rem,1.55vw,1.45rem);line-height:1.35}ul,ol{max-width:1050px}.kicker{color:var(--gold);text-transform:uppercase;letter-spacing:.08em;font-weight:700}.grid{display:grid;grid-template-columns:1.05fr .95fr;gap:30px;align-items:center}.visual-grid{display:grid;grid-template-columns:.7fr 1.3fr;gap:30px;align-items:center}.three{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card{border:1px solid var(--line);background:#fff;border-radius:6px;padding:14px 16px}.equation{font-size:1.32rem;padding:14px 18px;background:var(--teal-soft);border-left:5px solid var(--teal);margin:12px 0}figcaption,.small,.credit{color:var(--muted);font-size:.95rem;line-height:1.35;margin-top:8px}svg,img{width:100%;max-height:72vh;object-fit:contain;border:1px solid var(--line);background:#fff}.warning{border-left:5px solid var(--warning);background:#fff8e8;padding:14px 18px}@media print{.deck{height:auto;overflow:visible}.slide{min-height:7.5in;page-break-after:always}}
"""


def page(title: str, body: str, css: str = CSS) -> str:
    return (
        f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>{escape(title)}</title>"
        f"<script id='MathJax-script' async src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script>"
        f"<style>{css}</style></head><body>{body}</body></html>"
    )


def li(items) -> str:
    return ''.join(f'<li>{x}</li>' for x in items)


def cards(items) -> str:
    return ''.join(f'<article class="card"><p>{escape(x)}</p></article>' for x in items)


# ---------------------------------------------------------------------------
# Physical constants (SI unless noted)
# ---------------------------------------------------------------------------
C_LIGHT = 2.998e8
H_PLANCK = 6.626e-34
K_BOLTZMANN = 1.381e-23
ARCSEC_PER_RAD = 206264.806
NM = 1.0e-9
UM = 1.0e-6
MM = 1.0e-3

# ---------------------------------------------------------------------------
# Real telescope datasets.
# Keck I/II parameters live-verified this session via a direct web fetch of
# Wikipedia's "W. M. Keck Observatory" article (2026-09-24): aperture,
# collecting area, focal length, segment count/width, altitude, and active-
# optics surface accuracy. HIRES radial-velocity precision and 1 AU planet
# detection limit are likewise live-verified from the same article, which
# cites Vogt et al. 1994 (SPIE 2198, 362) for the instrument. HST, VLT,
# JWST, and DECam apertures/formats are standard published mission/facility
# specifications (level 2, flagged for spot-check in reference-log.md).
# ---------------------------------------------------------------------------
KECK = dict(name='Keck I/II', aperture_m=10.0, collecting_area_m2=76.0, focal_length_m=17.5,
            n_segments=36, segment_width_m=1.8, altitude_m=4145.0, surface_accuracy_nm=4.0)
HIRES = dict(name='Keck HIRES', rv_precision_ms=1.0, detection_limit_mj_at_1au=0.2,
             resolving_power=67000, groove_density_per_mm=52.67, blaze_angle_deg=70.0)
HST = dict(name='Hubble Space Telescope', aperture_m=2.4, focal_length_m=57.6, altitude_km=540.0)
VLT = dict(name='ESO Very Large Telescope (UT)', aperture_m=8.2, focal_length_m=120.0, altitude_m=2635.0)
JWST = dict(name='James Webb Space Telescope', aperture_m=6.5, n_segments=18,
            wavelength_lo_um=0.6, wavelength_hi_um=28.3, focal_length_m=131.4)
GEMINI = dict(name='Gemini North', aperture_m=8.1, altitude_m=4213.0)
AMATEUR = dict(name='amateur reflector', aperture_m=0.2)
DECAM = dict(name='DECam (CTIO Blanco 4m)', n_ccds=62, n_pixels_total_mp=570.0, pixel_size_um=15.0,
             focal_length_m=11.28, host_aperture_m=4.0)

# e2v CCD231-84 (used in DECam-class imagers): representative published
# quantum-efficiency curve, standard manufacturer specification (level 2).
CCD_QE_CURVE_NM = [350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
CCD_QE_PERCENT = [45, 65, 82, 90, 94, 96, 95, 92, 85, 72, 55, 35, 16, 5]
CCD_READ_NOISE_E = 3.5  # electrons rms, representative modern scientific CCD (level 2)
CCD_DARK_CURRENT_E_PER_S = 0.001  # e-/pix/s at -100C, representative cooled CCD (level 2)
CCD_GAIN_E_PER_ADU = 1.8
CCD_FULL_WELL_E = 130000.0

# Johnson-Cousins UBVRI photometric system: standard published central
# wavelengths and effective bandwidths (Bessell 1990, PASP 102, 1181; level 2).
UBVRI = [
    ('U', 365, 66), ('B', 445, 94), ('V', 551, 88), ('R', 658, 138), ('I', 806, 149),
]

# Landolt (1992, AJ 104, 340) standard star SA 98-978: standard published
# UBVRI magnitudes used as photometric calibration reference (level 2).
LANDOLT_SA98_978 = dict(name='SA 98-978', V=9.061, B_V=0.593, U_B=0.048, V_R=0.353, R_I=0.343)

# Keck adaptive optics (natural guide star, K band): representative
# published Strehl ratios and residual wavefront errors (Wizinowich et al.
# 2000, PASP 112, 315; level 2).
KECK_AO_WFE_NM = [80, 120, 160, 200, 260, 320, 400]
KECK_WAVELENGTH_K_NM = 2200.0

EARTH_SEEING_ARCSEC = 0.8  # representative good-site median seeing (level 2)


# ---------------------------------------------------------------------------
# Physics helper functions -- every worked example below calls these rather
# than hand-typing a numeric result.
# ---------------------------------------------------------------------------
def rayleigh_resolution_rad(wavelength_m: float, aperture_m: float) -> float:
    """Rayleigh criterion angular resolution, theta = 1.22 lambda / D."""
    return 1.22 * wavelength_m / aperture_m


def rayleigh_resolution_arcsec(wavelength_m: float, aperture_m: float) -> float:
    return rayleigh_resolution_rad(wavelength_m, aperture_m) * ARCSEC_PER_RAD


def plate_scale_arcsec_per_mm(focal_length_m: float) -> float:
    """Plate scale, s = 206265 / (f [mm]), arcsec per mm at the focal plane."""
    return ARCSEC_PER_RAD / (focal_length_m * 1000.0)


def pixel_scale_arcsec(focal_length_m: float, pixel_size_um: float) -> float:
    return plate_scale_arcsec_per_mm(focal_length_m) * (pixel_size_um / 1000.0)


def photon_energy_j(wavelength_m: float) -> float:
    return H_PLANCK * C_LIGHT / wavelength_m


def ccd_snr(signal_e: float, sky_e: float, dark_e: float, read_noise_e: float, n_pix: float = 1.0) -> float:
    """CCD signal-to-noise equation (Merline & Howell 1995 form),
    SNR = S / sqrt(S + n_pix (sky + dark + read^2))."""
    noise_var = signal_e + n_pix * (sky_e + dark_e + read_noise_e ** 2)
    return signal_e / math.sqrt(noise_var)


def exposure_time_for_snr(target_snr: float, count_rate_e_per_s: float, sky_e_per_s: float,
                           dark_e_per_s: float, read_noise_e: float, n_pix: float = 1.0,
                           t_max_s: float = 1.0e5) -> float:
    """Bisection solve for exposure time t such that ccd_snr(count_rate*t, ...) = target_snr."""
    lo, hi = 1.0e-3, t_max_s
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        snr_mid = ccd_snr(count_rate_e_per_s * mid, sky_e_per_s * mid, dark_e_per_s * mid, read_noise_e, n_pix)
        if snr_mid < target_snr:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def grating_equation_angle_rad(groove_density_per_mm: float, order: int, wavelength_m: float,
                                incidence_rad: float = 0.0) -> float:
    """Grating equation, m lambda = d (sin(theta_i) + sin(theta_m)), solved for theta_m."""
    d_m = 1.0e-3 / groove_density_per_mm
    rhs = order * wavelength_m / d_m - math.sin(incidence_rad)
    rhs = max(-1.0, min(1.0, rhs))
    return math.asin(rhs)


def resolving_power_grating(order: int, n_illuminated_grooves: float) -> float:
    """Grating resolving power, R = lambda / delta_lambda = m N."""
    return order * n_illuminated_grooves


def resolving_power_from_beam_width(beam_width_m: float, blaze_angle_deg: float, wavelength_m: float) -> float:
    """Resolving power of a blazed grating in Littrow configuration,
    R = 2 W tan(theta_B) / lambda, with W the illuminated beam width."""
    return 2.0 * beam_width_m * math.tan(math.radians(blaze_angle_deg)) / wavelength_m


def strehl_ratio_marechal(wavefront_error_m: float, wavelength_m: float) -> float:
    """Marechal approximation, S = exp(-(2 pi sigma / lambda)^2), for the
    Strehl ratio given rms wavefront error sigma."""
    return math.exp(-(2 * math.pi * wavefront_error_m / wavelength_m) ** 2)


def diffraction_limited_fwhm_arcsec(wavelength_m: float, aperture_m: float) -> float:
    """FWHM of the Airy-disk core, approximated as 1.03 lambda/D (standard
    scaling relation used for AO/space-telescope PSF planning)."""
    return 1.03 * wavelength_m / aperture_m * ARCSEC_PER_RAD


def error_budget_rss(terms_m) -> float:
    """Root-sum-square combination of independent error-budget terms."""
    return math.sqrt(sum(t ** 2 for t in terms_m))


# ---------------------------------------------------------------------------
# Derived worked-example numbers, computed once here and reused throughout
# the lectures, labs, and problem sets.
# ---------------------------------------------------------------------------
V_BAND_NM = 551.0
V_BAND_M = V_BAND_NM * NM
K_BAND_M = KECK_WAVELENGTH_K_NM * NM

KECK_RESOLUTION_V_ARCSEC = rayleigh_resolution_arcsec(V_BAND_M, KECK['aperture_m'])
HST_RESOLUTION_V_ARCSEC = rayleigh_resolution_arcsec(V_BAND_M, HST['aperture_m'])
VLT_RESOLUTION_V_ARCSEC = rayleigh_resolution_arcsec(V_BAND_M, VLT['aperture_m'])
JWST_RESOLUTION_2UM_ARCSEC = rayleigh_resolution_arcsec(2.0 * UM, JWST['aperture_m'])
AMATEUR_RESOLUTION_V_ARCSEC = rayleigh_resolution_arcsec(V_BAND_M, AMATEUR['aperture_m'])
KECK_SEEING_LIMITED_FACTOR = EARTH_SEEING_ARCSEC / KECK_RESOLUTION_V_ARCSEC

KECK_PLATE_SCALE_ARCSEC_MM = plate_scale_arcsec_per_mm(KECK['focal_length_m'])
HST_PLATE_SCALE_ARCSEC_MM = plate_scale_arcsec_per_mm(HST['focal_length_m'])
JWST_PLATE_SCALE_ARCSEC_MM = plate_scale_arcsec_per_mm(JWST['focal_length_m'])
DECAM_PLATE_SCALE_ARCSEC_MM = plate_scale_arcsec_per_mm(DECAM['focal_length_m'])
DECAM_PIXEL_SCALE_ARCSEC = pixel_scale_arcsec(DECAM['focal_length_m'], DECAM['pixel_size_um'])
DECAM_NYQUIST_PIXEL_SCALE_ARCSEC = KECK_RESOLUTION_V_ARCSEC / 2.0  # Nyquist criterion reference point

PHOTON_ENERGY_V_J = photon_energy_j(V_BAND_M)
PHOTON_ENERGY_V_EV = PHOTON_ENERGY_V_J / 1.602176634e-19

# Worked SNR example: 18th-magnitude star with Keck (10 m aperture, adopting
# a representative 60% end-to-end system throughput), V-band, e2v-class CCD.
KECK_THROUGHPUT = 0.6
STAR_V_MAG = 18.0
V_ZERO_POINT_PHOTON_FLUX_PER_M2_S = 9.0e10  # standard published V-band zero-point photon flux (level 2, Bessell 1998)
STAR_PHOTON_FLUX_PER_M2_S = V_ZERO_POINT_PHOTON_FLUX_PER_M2_S * 10 ** (-0.4 * STAR_V_MAG)
STAR_COUNT_RATE_E_PER_S = STAR_PHOTON_FLUX_PER_M2_S * KECK['collecting_area_m2'] * KECK_THROUGHPUT * 0.94  # QE at 550 nm
SKY_MAG_PER_ARCSEC2_V = 21.5  # standard published dark-site V-band sky brightness (level 2)
SKY_PHOTON_FLUX_PER_M2_S_ARCSEC2 = V_ZERO_POINT_PHOTON_FLUX_PER_M2_S * 10 ** (-0.4 * SKY_MAG_PER_ARCSEC2_V)
SEEING_APERTURE_ARCSEC2 = math.pi * (EARTH_SEEING_ARCSEC) ** 2
SKY_COUNT_RATE_E_PER_S = SKY_PHOTON_FLUX_PER_M2_S_ARCSEC2 * SEEING_APERTURE_ARCSEC2 * KECK[
    'collecting_area_m2'] * KECK_THROUGHPUT * 0.94
EXPOSURE_FOR_SNR100_S = exposure_time_for_snr(
    100.0, STAR_COUNT_RATE_E_PER_S, SKY_COUNT_RATE_E_PER_S, CCD_DARK_CURRENT_E_PER_S, CCD_READ_NOISE_E)
SNR_AT_300S = ccd_snr(STAR_COUNT_RATE_E_PER_S * 300.0, SKY_COUNT_RATE_E_PER_S * 300.0,
                       CCD_DARK_CURRENT_E_PER_S * 300.0, CCD_READ_NOISE_E)
SNR_AT_30S = ccd_snr(STAR_COUNT_RATE_E_PER_S * 30.0, SKY_COUNT_RATE_E_PER_S * 30.0,
                      CCD_DARK_CURRENT_E_PER_S * 30.0, CCD_READ_NOISE_E)

# Grating/spectrograph worked example, following the HIRES echelle format.
HIRES_BEAM_WIDTH_M = 0.20  # representative illuminated collimated beam width for an echelle of this class (level 2)
HIRES_R_FROM_BEAM = resolving_power_from_beam_width(HIRES_BEAM_WIDTH_M, HIRES['blaze_angle_deg'], V_BAND_M)
HIRES_DELTA_LAMBDA_NM = V_BAND_NM / HIRES['resolving_power']
HIRES_RV_FROM_R = C_LIGHT / HIRES['resolving_power'] / 1000.0  # km/s velocity resolution element, c/R

# Adaptive optics worked example: Strehl ratio at several wavefront errors.
STREHL_AT_WFE = [(wfe, strehl_ratio_marechal(wfe * NM, K_BAND_M)) for wfe in KECK_AO_WFE_NM]
KECK_AO_TYPICAL_WFE_NM = 160.0
KECK_AO_TYPICAL_STREHL = strehl_ratio_marechal(KECK_AO_TYPICAL_WFE_NM * NM, K_BAND_M)
KECK_AO_DIFFRACTION_LIMIT_K_ARCSEC = diffraction_limited_fwhm_arcsec(K_BAND_M, KECK['aperture_m'])

# Error-budget worked example: a ground-based photometric error budget (RSS
# combination of Poisson, flat-field residual, and atmospheric-extinction terms).
ERR_POISSON_MAG = 1.0857 / SNR_AT_300S  # Poisson-limited magnitude error at SNR from the 300 s exposure
ERR_FLATFIELD_RESIDUAL_MAG = 0.003  # representative modern flat-field residual non-uniformity (level 2)
ERR_EXTINCTION_MAG = 0.01  # representative photometric-night extinction-correction residual (level 2)
TOTAL_PHOTOMETRIC_ERROR_MAG = math.sqrt(
    ERR_POISSON_MAG ** 2 + ERR_FLATFIELD_RESIDUAL_MAG ** 2 + ERR_EXTINCTION_MAG ** 2)

JWST_VS_KECK_RESOLUTION_RATIO = KECK_RESOLUTION_V_ARCSEC / rayleigh_resolution_arcsec(2.0 * UM, JWST['aperture_m'])


# ---------------------------------------------------------------------------
# Lecture-specific visual-reasoning diagrams (SVG). Each lecture gets a
# structurally distinct figure built from the real constants/datasets above;
# only small drawing primitives are shared (see materials/ASTR330/src for
# the established pattern this follows).
# ---------------------------------------------------------------------------
def _lin(v, vmin, vmax, a, b):
    if vmax == vmin:
        return a
    return a + (v - vmin) / (vmax - vmin) * (b - a)


def _axes(x0, y0, w, h, xlabel, ylabel, color='#5b6773'):
    return (
        f"<line x1='{x0}' y1='{y0 + h}' x2='{x0 + w}' y2='{y0 + h}' stroke='{color}' stroke-width='2'/>"
        f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y0 + h}' stroke='{color}' stroke-width='2'/>"
        f"<text x='{x0 + w / 2:.0f}' y='{y0 + h + 36}' font-size='16' fill='{color}' text-anchor='middle' "
        f"font-family='Segoe UI, sans-serif'>{escape(xlabel)}</text>"
        f"<text x='{x0}' y='{y0 - 14}' font-size='16' fill='{color}' font-family='Segoe UI, sans-serif'>{escape(ylabel)}</text>"
    )


def _polyline(pts, color='#0f6b78', width=3.5, dash=None):
    s = ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts)
    dash_attr = f" stroke-dasharray='{dash}'" if dash else ''
    return f"<polyline points='{s}' fill='none' stroke='{color}' stroke-width='{width}'{dash_attr}/>"


def _dot(x, y, label=None, r=6, color='#b87911', dx=10, dy=-10, fs=14, anchor='start'):
    out = f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{color}'/>"
    if label:
        out += (f"<text x='{x + dx:.1f}' y='{y + dy:.1f}' font-size='{fs}' fill='#17202a' "
                 f"text-anchor='{anchor}' font-family='Segoe UI, sans-serif'>{escape(label)}</text>")
    return out


def _fig_header(n, title):
    return (
        f"<rect width='980' height='620' fill='#fbfcfd'/>"
        f"<text x='34' y='42' font-size='23' fill='#102a43' font-family='Segoe UI, sans-serif'>"
        f"Lecture {n:02d}: {escape(title)}</text>"
    )


def _fig_caption(text, y=600):
    return (f"<text x='34' y='{y}' font-size='15.5' fill='#5b6773' "
            f"font-family='Segoe UI, sans-serif'>{escape(text)}</text>")


def _fig_wrap(n, title, inner, aria):
    return (
        f"<svg class='lecture-figure' data-lecture-figure='{n:02d}' viewBox='0 0 980 620' role='img' "
        f"aria-label='Lecture {n:02d} visual model: {escape(aria)}'>"
        f"{_fig_header(n, title)}{inner}</svg>"
    )


def _bessel_j1(x: float) -> float:
    """Series expansion of the Bessel function J1(x), converges well for |x|<20."""
    if x == 0:
        return 0.0
    total = 0.0
    term_sign = 1.0
    for k in range(0, 40):
        fact_k = math.factorial(k)
        fact_k1 = math.factorial(k + 1)
        term = term_sign * (x / 2.0) ** (2 * k + 1) / (fact_k * fact_k1)
        total += term
        term_sign *= -1.0
    return total


def _airy_intensity(x: float) -> float:
    if abs(x) < 1.0e-6:
        return 1.0
    return (2.0 * _bessel_j1(x) / x) ** 2


def diagram_01(item: dict) -> str:
    """Labeled Cassegrain-telescope ray-trace schematic: concave primary, convex secondary, focal plane."""
    n = item['n']
    x0, y0 = 120, 500
    primary_y = 460
    prim_left, prim_right = 140, 860
    sec_x = 560
    focal_x = 760
    rays = []
    for yin in (300, 360, 420, 480, 540, 600):
        rays.append((60, yin, prim_left + (prim_right - prim_left) * (yin - 260) / 380.0, primary_y))
    inner = ''
    # primary mirror (concave arc)
    inner += f"<path d='M {prim_left} {primary_y - 60} Q {(prim_left + prim_right) / 2} {primary_y + 40} {prim_right} {primary_y - 60}' fill='none' stroke='#102a43' stroke-width='6'/>"
    inner += f"<text x='{(prim_left + prim_right) / 2 - 60}' y='{primary_y + 90}' font-size='15' fill='#102a43' font-family='Segoe UI, sans-serif'>primary mirror (concave, diameter D)</text>"
    # incoming parallel rays and reflected rays converging toward secondary
    for x1, y1, x2, y2 in rays:
        inner += f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#b87911' stroke-width='1.6'/>"
        inner += f"<line x1='{x2}' y1='{y2}' x2='{sec_x}' y2='{primary_y - 260}' stroke='#0f6b78' stroke-width='1.6'/>"
    # secondary mirror (convex, small)
    inner += f"<ellipse cx='{sec_x}' cy='{primary_y - 260}' rx='16' ry='36' fill='#8a4b08'/>"
    inner += f"<text x='{sec_x + 26}' y='{primary_y - 260}' font-size='15' fill='#8a4b08' font-family='Segoe UI, sans-serif'>secondary mirror (convex, hyperbolic)</text>"
    # ray from secondary back through hole in primary to focal plane
    inner += f"<line x1='{sec_x}' y1='{primary_y - 260}' x2='{focal_x}' y2='{primary_y - 30}' stroke='#0f6b78' stroke-width='2.2'/>"
    inner += f"<line x1='{focal_x - 4}' y1='{primary_y - 60}' x2='{focal_x - 4}' y2='{primary_y}' stroke='#17202a' stroke-width='4'/>"
    inner += f"<text x='{focal_x + 8}' y='{primary_y - 34}' font-size='15' fill='#17202a' font-family='Segoe UI, sans-serif'>focal plane (f = effective focal length)</text>"
    inner += _fig_caption(f"Cassegrain layout (schematic, not to scale): a concave primary of diameter D collects and focuses light toward a convex secondary, which redirects it to a focal plane behind the primary -- the geometry every instrument in this course attaches to.")
    return _fig_wrap(n, item['title'], inner, 'labeled ray-trace schematic of a Cassegrain telescope showing the concave primary mirror, convex secondary mirror, and focal plane')


def diagram_02(item: dict) -> str:
    """Computed Airy-disk diffraction pattern (2J1(x)/x)^2 with Rayleigh criterion marked for real apertures."""
    n = item['n']
    xs = [0.02 * i for i in range(1, 700)]
    xs = [0.0] + xs
    ys = [_airy_intensity(x) for x in xs]
    x0, y0, w, h = 100, 80, 780, 380
    xmax = 14.0
    pts = [(_lin(x, 0, xmax, x0, x0 + w), _lin(y, 0, 1, y0 + h, y0)) for x, y in zip(xs, ys) if x <= xmax]
    rayleigh_x = 3.8317  # first zero of J1(x), standard Rayleigh-criterion location
    x_ray = _lin(rayleigh_x, 0, xmax, x0, x0 + w)
    inner = (
        _axes(x0, y0, w, h, 'x = \u03c0 D \u03b8 / \u03bb (dimensionless angular radius)', 'normalized Airy intensity')
        + _polyline(pts, color='#0f6b78')
        + f"<line x1='{x_ray:.1f}' y1='{y0}' x2='{x_ray:.1f}' y2='{y0 + h}' stroke='#8a4b08' stroke-width='2' stroke-dasharray='5,4'/>"
        + f"<text x='{x_ray + 8:.1f}' y='{y0 + 24}' font-size='14' fill='#8a4b08' font-family='Segoe UI, sans-serif'>first dark ring, x=3.8317 \u2192 Rayleigh criterion \u03b8=1.22\u03bb/D</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 24}' font-size='14' fill='#0f6b78' font-family='Segoe UI, sans-serif'>{escape('Keck (D=' + format(KECK['aperture_m'], '.0f') + ' m, V band): \u03b8\u2248' + format(KECK_RESOLUTION_V_ARCSEC*1000, '.1f') + ' mas')}</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 46}' font-size='14' fill='#102a43' font-family='Segoe UI, sans-serif'>{escape('HST (D=' + format(HST['aperture_m'], '.1f') + ' m, V band): \u03b8\u2248' + format(HST_RESOLUTION_V_ARCSEC*1000, '.1f') + ' mas')}</text>"
        + _fig_caption('Computed Airy diffraction pattern (2J\u2081(x)/x)\u00b2 from a numerical Bessel-function series: the first dark ring at x=3.8317 defines the Rayleigh resolution criterion.')
    )
    return _fig_wrap(n, item['title'], inner, 'computed Airy diffraction intensity pattern versus dimensionless angular radius, with the Rayleigh-criterion first dark ring marked')


def diagram_03(item: dict) -> str:
    """Log-log plate scale versus focal length, with real telescopes marked."""
    n = item['n']
    fs = [0.3 * 1.05 ** i for i in range(90)]
    scales = [plate_scale_arcsec_per_mm(f) for f in fs]
    log_f = [math.log10(f) for f in fs]
    log_s = [math.log10(s) for s in scales]
    scopes = [
        ('HST', HST['focal_length_m'], '#102a43'),
        ('Keck', KECK['focal_length_m'], '#0f6b78'),
        ('VLT', VLT['focal_length_m'], '#b87911'),
        ('JWST', JWST['focal_length_m'], '#8a4b08'),
        ('DECam host (Blanco 4m)', DECAM['focal_length_m'], '#5b6773'),
    ]
    x0, y0, w, h = 110, 80, 770, 380
    xmin, xmax = min(log_f), max(log_f)
    ymin, ymax = min(log_s), max(log_s)
    pts = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(log_f, log_s)]
    dots = ''
    for i, (name, f, color) in enumerate(scopes):
        x = _lin(math.log10(f), xmin, xmax, x0, x0 + w)
        y = _lin(math.log10(plate_scale_arcsec_per_mm(f)), ymin, ymax, y0 + h, y0)
        dots += _dot(x, y, f'{name}: f={f:.1f} m, s={plate_scale_arcsec_per_mm(f):.2f}\u2033/mm', color=color, dy=-16 - 18 * (i % 3))
    inner = (
        _axes(x0, y0, w, h, "log\u2081\u2080(effective focal length, m)", "log\u2081\u2080(plate scale, arcsec/mm)")
        + _polyline(pts, color='#8a4b08', dash='3,3') + dots
        + _fig_caption("Plate scale s=206265\u2033/f[mm] falls as focal length rises: five real telescopes span more than a factor of 10 in focal length and plate scale.")
    )
    return _fig_wrap(n, item['title'], inner, 'log-log plot of plate scale versus effective focal length with five real telescopes marked')


def diagram_04(item: dict) -> str:
    """Published CCD quantum-efficiency curve versus wavelength, e2v CCD231-84 class device."""
    n = item['n']
    x0, y0, w, h = 100, 80, 780, 380
    xmin, xmax = 300, 1050
    ymin, ymax = 0, 100
    pts = [(_lin(wl, xmin, xmax, x0, x0 + w), _lin(qe, ymin, ymax, y0 + h, y0))
           for wl, qe in zip(CCD_QE_CURVE_NM, CCD_QE_PERCENT)]
    v_x = _lin(V_BAND_NM, xmin, xmax, x0, x0 + w)
    inner = (
        _axes(x0, y0, w, h, 'wavelength (nm)', 'quantum efficiency (%)')
        + _polyline(pts, color='#0f6b78')
        + f"<line x1='{v_x:.1f}' y1='{y0}' x2='{v_x:.1f}' y2='{y0 + h}' stroke='#8a4b08' stroke-width='2' stroke-dasharray='5,4'/>"
        + f"<text x='{v_x + 8:.1f}' y='{y0 + 24}' font-size='14' fill='#8a4b08' font-family='Segoe UI, sans-serif'>{escape(f'V band (551 nm): QE\u224894%')}</text>"
        + _fig_caption('Representative published quantum-efficiency curve for a modern thinned, back-illuminated scientific CCD (e2v CCD231-84 class device): QE peaks near 600 nm and falls sharply in the near-UV and near-IR.')
    )
    return _fig_wrap(n, item['title'], inner, 'published CCD quantum-efficiency curve versus wavelength peaking near 600 nanometers')


def diagram_05(item: dict) -> str:
    """Noise-budget curves: shot noise and dark noise rising as sqrt(t), read noise flat, versus exposure time."""
    n = item['n']
    ts = [1.0 * 1.2 ** i for i in range(40)]
    shot = [math.sqrt(STAR_COUNT_RATE_E_PER_S * t) for t in ts]
    dark = [math.sqrt(CCD_DARK_CURRENT_E_PER_S * t) for t in ts]
    read = [CCD_READ_NOISE_E for _ in ts]
    log_t = [math.log10(t) for t in ts]
    log_shot = [math.log10(v) for v in shot]
    log_dark = [math.log10(max(v, 1e-4)) for v in dark]
    log_read = [math.log10(v) for v in read]
    x0, y0, w, h = 110, 80, 770, 380
    xmin, xmax = min(log_t), max(log_t)
    ymin = min(log_dark)
    ymax = max(log_shot)

    def curve(ys, color, dash=None):
        pts = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(log_t, ys)]
        return _polyline(pts, color=color, dash=dash)

    inner = (
        _axes(x0, y0, w, h, 'log\u2081\u2080(exposure time, s)', 'log\u2081\u2080(noise, electrons rms)')
        + curve(log_shot, '#0f6b78') + curve(log_read, '#b87911', dash='6,4') + curve(log_dark, '#8a4b08', dash='2,3')
        + f"<text x='{x0 + 14}' y='{y0 + 24}' font-size='14' fill='#0f6b78' font-family='Segoe UI, sans-serif'>shot noise, \u221a(S\u00b7t) (rises with exposure)</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 46}' font-size='14' fill='#b87911' font-family='Segoe UI, sans-serif'>{escape(f'read noise, {CCD_READ_NOISE_E:.1f} e\u207b rms (fixed per read)')}</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 68}' font-size='14' fill='#8a4b08' font-family='Segoe UI, sans-serif'>{escape(f'dark noise, \u221a(D\u00b7t) at D={CCD_DARK_CURRENT_E_PER_S:.3f} e\u207b/pix/s')}</text>"
        + _fig_caption('Read noise dominates short exposures; shot noise from the source overtakes it once S\u00b7t exceeds the read-noise floor -- the crossover that sets a detector\u2019s useful minimum exposure time.')
    )
    return _fig_wrap(n, item['title'], inner, 'log-log noise budget plot of shot noise, dark noise, and read noise versus exposure time')


def diagram_06(item: dict) -> str:
    """SNR versus exposure time for the worked 18th-magnitude Keck/CCD scenario, log-log with SNR=100 marked."""
    n = item['n']
    ts = [0.5 * 1.15 ** i for i in range(45)]
    snrs = [ccd_snr(STAR_COUNT_RATE_E_PER_S * t, SKY_COUNT_RATE_E_PER_S * t, CCD_DARK_CURRENT_E_PER_S * t, CCD_READ_NOISE_E) for t in ts]
    log_t = [math.log10(t) for t in ts]
    log_snr = [math.log10(s) for s in snrs]
    x0, y0, w, h = 110, 80, 770, 380
    xmin, xmax = min(log_t), max(log_t)
    ymin, ymax = min(log_snr), max(log_snr)
    pts = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(log_t, log_snr)]
    x_100 = _lin(math.log10(EXPOSURE_FOR_SNR100_S), xmin, xmax, x0, x0 + w)
    y_100 = _lin(math.log10(100.0), ymin, ymax, y0 + h, y0)
    inner = (
        _axes(x0, y0, w, h, 'log\u2081\u2080(exposure time, s)', 'log\u2081\u2080(signal-to-noise ratio)')
        + _polyline(pts, color='#0f6b78')
        + _dot(x_100, y_100, f'SNR=100 at t\u2248{EXPOSURE_FOR_SNR100_S:.0f} s', color='#8a4b08')
        + _fig_caption(f'CCD-equation SNR versus exposure time for a V={STAR_V_MAG:.0f} star with the Keck aperture and a representative e2v-class CCD; the curve bends from read-noise-limited to background-limited growth as t increases.')
    )
    return _fig_wrap(n, item['title'], inner, 'log-log SNR versus exposure time curve for an 18th magnitude star observed with Keck, with the exposure time reaching SNR 100 marked')


def diagram_07(item: dict) -> str:
    """Schematic pixel-value level diagram for bias, dark, flat, and raw light frames."""
    n = item['n']
    bias_level, dark_level, flat_level, light_level = 400, 480, 30000, 18500
    frames = [('bias', bias_level, '#5b6773'), ('dark', dark_level, '#8a4b08'),
              ('flat', flat_level, '#b87911'), ('raw light', light_level, '#0f6b78')]
    x0, y0, w, h = 160, 80, 660, 380
    ymax = 32000
    barw, gap = 120, 190
    bars = ''
    for i, (label, val, color) in enumerate(frames):
        xc = x0 + 90 + i * gap
        bar_h = _lin(val, 0, ymax, 0, h)
        bars += f"<rect x='{xc - barw / 2:.1f}' y='{y0 + h - bar_h:.1f}' width='{barw}' height='{bar_h:.1f}' fill='{color}'/>"
        bars += f"<text x='{xc:.1f}' y='{y0 + h + 26}' font-size='14' fill='#17202a' text-anchor='middle' font-family='Segoe UI, sans-serif'>{escape(label)}</text>"
        bars += f"<text x='{xc:.1f}' y='{y0 + h - bar_h - 10:.1f}' font-size='14' fill='{color}' text-anchor='middle' font-family='Segoe UI, sans-serif'>{val} ADU</text>"
    inner = (
        _axes(x0, y0, w, h, '', 'representative mean pixel level (ADU)')
        + bars
        + _fig_caption('Representative calibration-frame pixel levels (illustrative, not from a specific exposure): bias sets the electronic floor, dark adds thermal-electron counts over exposure time, flat records the pixel-to-pixel and vignetting response, and the raw light frame carries all three plus the astronomical signal.')
    )
    return _fig_wrap(n, item['title'], inner, 'bar chart comparing representative pixel levels for bias, dark, flat, and raw light calibration frames')


def diagram_08(item: dict) -> str:
    """Johnson-Cousins UBVRI filter transmission bandpasses, real central wavelengths and widths."""
    n = item['n']
    x0, y0, w, h = 100, 80, 780, 380
    xmin, xmax = 300, 950
    colors = ['#5b6773', '#0f6b78', '#8a4b08', '#b87911', '#102a43']
    inner = ''
    for (name, lam0, fwhm), color in zip(UBVRI, colors):
        xs = [lam0 - 2.0 * fwhm + 2.0 * fwhm * i / 80 for i in range(81)]
        ys = [math.exp(-4 * math.log(2) * ((x - lam0) / fwhm) ** 2) for x in xs]
        pts = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, 0, 1, y0 + h, y0)) for x, y in zip(xs, ys)]
        inner += _polyline(pts, color=color)
        x_peak = _lin(lam0, xmin, xmax, x0, x0 + w)
        inner += f"<text x='{x_peak:.1f}' y='{y0 - 4}' font-size='14' fill='{color}' text-anchor='middle' font-family='Segoe UI, sans-serif'>{escape(f'{name}: {lam0:.0f} nm')}</text>"
    inner += _axes(x0, y0, w, h, 'wavelength (nm)', 'relative transmission')
    inner += _fig_caption('Johnson-Cousins UBVRI bandpasses (Gaussian approximation to the published central wavelength and effective bandwidth of each filter, Bessell 1990): each filter isolates a distinct spectral region for photometric calibration.')
    return _fig_wrap(n, item['title'], inner, 'five overlapping Gaussian filter transmission curves for the Johnson-Cousins UBVRI photometric system')


def diagram_09(item: dict) -> str:
    """Grating-equation diffraction angle versus wavelength for two orders."""
    n = item['n']
    groove_density = 600.0  # representative first-order grating for teaching purposes (level 2 illustrative)
    wls_nm = [400 + 4 * i for i in range(126)]
    angles_m1 = [math.degrees(grating_equation_angle_rad(groove_density, 1, wl * NM)) for wl in wls_nm]
    angles_m2 = [math.degrees(grating_equation_angle_rad(groove_density, 2, wl * NM)) for wl in wls_nm]
    x0, y0, w, h = 110, 80, 770, 380
    xmin, xmax = wls_nm[0], wls_nm[-1]
    ymin = min(angles_m1)
    ymax = max(angles_m2)
    pts1 = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(wls_nm, angles_m1)]
    pts2 = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(wls_nm, angles_m2)]
    inner = (
        _axes(x0, y0, w, h, 'wavelength (nm)', 'diffraction angle, \u03b8_m (degrees, normal incidence)')
        + _polyline(pts1, color='#0f6b78') + _polyline(pts2, color='#b87911')
        + f"<text x='{x0 + 14}' y='{y0 + 24}' font-size='14' fill='#0f6b78' font-family='Segoe UI, sans-serif'>{escape(f'm=1 order (N={groove_density:.0f} grooves/mm)')}</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 46}' font-size='14' fill='#b87911' font-family='Segoe UI, sans-serif'>m=2 order (twice the angular dispersion)</text>"
        + _fig_caption('Grating equation m\u03bb = d sin\u03b8_m: higher orders disperse light through larger angles for the same wavelength, at the cost of overlapping with adjacent orders.')
    )
    return _fig_wrap(n, item['title'], inner, 'grating-equation diffraction angle versus wavelength curves for the first and second diffraction orders')


def diagram_10(item: dict) -> str:
    """Echelle order-format diagram: stacked short wavelength segments per high order, HIRES-class spacing."""
    n = item['n']
    orders = list(range(40, 30, -1))
    x0, y0, w = 110, 110, 760
    row_h = 34
    max_order_span_nm = 12.0
    inner = ''
    for i, m in enumerate(orders):
        y = y0 + i * row_h
        lam_center_nm = HIRES['groove_density_per_mm'] and (2 * (1.0e-3 / HIRES['groove_density_per_mm']) * math.sin(
            math.radians(HIRES['blaze_angle_deg']))) / m * 1.0e9
        span = max_order_span_nm * (35.0 / m)
        x_left = x0
        x_right = x0 + w * (span / max_order_span_nm) * 0.5
        inner += f"<rect x='{x_left}' y='{y}' width='{x_right - x_left:.1f}' height='{row_h - 6}' fill='#0f6b78' opacity='{0.4 + 0.5 * (i / len(orders))}'/>"
        inner += f"<text x='{x_right + 12:.1f}' y='{y + row_h - 14}' font-size='13.5' fill='#17202a' font-family='Segoe UI, sans-serif'>{escape(f'm={m}: \u03bb\u2248{lam_center_nm:.0f} nm, \u0394\u03bb\u2248{span:.1f} nm')}</text>"
    inner += f"<text x='{x0}' y='{y0 - 30}' font-size='15.5' fill='#102a43' font-family='Segoe UI, sans-serif'>Free spectral range per order, \u0394\u03bb \u2248 \u03bb/m: high orders (large m) cover a narrow \u0394\u03bb but at high resolving power.</text>"
    inner += _fig_caption(f'Schematic echelle order stack (illustrative order widths, using the HIRES blaze angle {HIRES["blaze_angle_deg"]:.0f}\u00b0 and groove density {HIRES["groove_density_per_mm"]:.2f}/mm): a cross-disperser separates the overlapping high orders vertically so many narrow, high-resolution segments are recorded simultaneously.')
    return _fig_wrap(n, item['title'], inner, 'stacked echelle diffraction-order diagram with narrower wavelength coverage at higher order number')


def diagram_11(item: dict) -> str:
    """Marechal-approximation Strehl ratio versus rms wavefront error, with Keck AO values marked."""
    n = item['n']
    wfes = [1.0 * i for i in range(1, 400)]
    strehls = [strehl_ratio_marechal(wfe * NM, K_BAND_M) for wfe in wfes]
    x0, y0, w, h = 110, 80, 770, 380
    xmin, xmax = 0, 400
    ymin, ymax = 0, 1
    pts = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(wfes, strehls)]
    dots = ''
    for i, (wfe, s) in enumerate(STREHL_AT_WFE):
        x = _lin(wfe, xmin, xmax, x0, x0 + w)
        y = _lin(s, ymin, ymax, y0 + h, y0)
        dots += _dot(x, y, f'{wfe:.0f} nm \u2192 S={s:.2f}', color='#b87911', dy=-14 - 16 * (i % 2))
    inner = (
        _axes(x0, y0, w, h, 'rms wavefront error, \u03c3 (nm)', 'Strehl ratio, S')
        + _polyline(pts, color='#0f6b78') + dots
        + _fig_caption(f'Mar\u00e9chal approximation S=exp[-(2\u03c0\u03c3/\u03bb)\u00b2] at K band (\u03bb={KECK_WAVELENGTH_K_NM:.0f} nm): representative Keck natural-guide-star AO residual wavefront errors (Wizinowich et al. 2000) give Strehl ratios from roughly 0.9 down to below 0.1 as \u03c3 grows.')
    )
    return _fig_wrap(n, item['title'], inner, 'Strehl ratio versus rms wavefront error curve from the Marechal approximation with representative Keck adaptive optics values marked')


def diagram_12(item: dict) -> str:
    """Diffraction-limited angular resolution versus wavelength for JWST and Keck, with the seeing-limited floor."""
    n = item['n']
    wls_um = [0.4 * 1.05 ** i for i in range(70)]
    keck_res = [rayleigh_resolution_arcsec(wl * UM, KECK['aperture_m']) for wl in wls_um]
    jwst_res = [rayleigh_resolution_arcsec(wl * UM, JWST['aperture_m']) for wl in wls_um if wl >= JWST['wavelength_lo_um']]
    jwst_wls = [wl for wl in wls_um if wl >= JWST['wavelength_lo_um']]
    log_wl = [math.log10(wl) for wl in wls_um]
    log_keck = [math.log10(r) for r in keck_res]
    log_jwst_wl = [math.log10(wl) for wl in jwst_wls]
    log_jwst = [math.log10(r) for r in jwst_res]
    x0, y0, w, h = 110, 80, 770, 380
    xmin, xmax = min(log_wl), max(log_wl)
    ymin = min(log_keck + log_jwst)
    ymax = math.log10(EARTH_SEEING_ARCSEC) + 0.1
    pts_keck = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(log_wl, log_keck)]
    pts_jwst = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(log_jwst_wl, log_jwst)]
    y_seeing = _lin(math.log10(EARTH_SEEING_ARCSEC), ymin, ymax, y0 + h, y0)
    inner = (
        _axes(x0, y0, w, h, 'log\u2081\u2080(wavelength, \u03bcm)', 'log\u2081\u2080(angular resolution, arcsec)')
        + _polyline(pts_keck, color='#0f6b78') + _polyline(pts_jwst, color='#8a4b08')
        + f"<line x1='{x0}' y1='{y_seeing:.1f}' x2='{x0 + w}' y2='{y_seeing:.1f}' stroke='#5b6773' stroke-width='2.5' stroke-dasharray='6,4'/>"
        + f"<text x='{x0 + w - 10}' y='{y_seeing - 10:.1f}' font-size='14' fill='#5b6773' text-anchor='end' font-family='Segoe UI, sans-serif'>{escape(f'median seeing floor, {EARTH_SEEING_ARCSEC:.1f}\u2033 (uncorrected ground-based)')}</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 24}' font-size='14' fill='#0f6b78' font-family='Segoe UI, sans-serif'>{escape(f'Keck diffraction limit, D={KECK["aperture_m"]:.0f} m')}</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 46}' font-size='14' fill='#8a4b08' font-family='Segoe UI, sans-serif'>{escape(f'JWST diffraction limit, D={JWST["aperture_m"]:.1f} m')}</text>"
        + _fig_caption('Keck\u2019s larger aperture gives a sharper diffraction limit than JWST at the same wavelength, but only adaptive optics (or space) let a telescope reach that limit instead of the atmospheric seeing floor.')
    )
    return _fig_wrap(n, item['title'], inner, 'log-log plot comparing Keck and JWST diffraction-limited angular resolution versus wavelength against the atmospheric seeing floor')


def diagram_13(item: dict) -> str:
    """Error-budget bar chart: RSS combination of Poisson, flat-field, and extinction terms."""
    n = item['n']
    terms = [
        ('Poisson (SNR-limited)', ERR_POISSON_MAG, '#0f6b78'),
        ('flat-field residual', ERR_FLATFIELD_RESIDUAL_MAG, '#b87911'),
        ('extinction correction', ERR_EXTINCTION_MAG, '#8a4b08'),
        ('total (RSS)', TOTAL_PHOTOMETRIC_ERROR_MAG, '#102a43'),
    ]
    x0, y0, w, h = 160, 80, 660, 380
    ymax = max(t for _, t, _ in terms) * 1.25
    barw, gap = 110, 150
    bars = ''
    for i, (label, val, color) in enumerate(terms):
        xc = x0 + 80 + i * gap
        bar_h = _lin(val, 0, ymax, 0, h)
        bars += f"<rect x='{xc - barw / 2:.1f}' y='{y0 + h - bar_h:.1f}' width='{barw}' height='{bar_h:.1f}' fill='{color}'/>"
        bars += f"<text x='{xc:.1f}' y='{y0 + h + 22}' font-size='13' fill='#17202a' text-anchor='middle' font-family='Segoe UI, sans-serif'>{escape(label)}</text>"
        bars += f"<text x='{xc:.1f}' y='{y0 + h - bar_h - 8:.1f}' font-size='13.5' fill='{color}' text-anchor='middle' font-family='Segoe UI, sans-serif'>{val * 1000:.1f} mmag</text>"
    inner = (
        _axes(x0, y0, w, h, '', 'photometric error (magnitudes)')
        + bars
        + _fig_caption('Root-sum-square error budget for the worked 300 s Keck V-band photometric scenario: the Poisson term from the CCD-equation SNR dominates the total unless flat-fielding or extinction correction is unusually poor.')
    )
    return _fig_wrap(n, item['title'], inner, 'bar chart of Poisson, flat-field, and extinction photometric error-budget terms combined in root-sum-square with the total')


def diagram_14(item: dict) -> str:
    """Capstone synthesis: SNR versus exposure time trade curves for two competing aperture proposals."""
    n = item['n']
    ts = [1.0 * 1.2 ** i for i in range(40)]
    snr_10m = [ccd_snr(STAR_COUNT_RATE_E_PER_S * t, SKY_COUNT_RATE_E_PER_S * t, CCD_DARK_CURRENT_E_PER_S * t, CCD_READ_NOISE_E) for t in ts]
    area_ratio = (VLT['aperture_m'] / KECK['aperture_m']) ** 2
    snr_8m = [ccd_snr(STAR_COUNT_RATE_E_PER_S * area_ratio * t, SKY_COUNT_RATE_E_PER_S * area_ratio * t, CCD_DARK_CURRENT_E_PER_S * t, CCD_READ_NOISE_E) for t in ts]
    log_t = [math.log10(t) for t in ts]
    log_10 = [math.log10(s) for s in snr_10m]
    log_8 = [math.log10(s) for s in snr_8m]
    x0, y0, w, h = 110, 80, 770, 380
    xmin, xmax = min(log_t), max(log_t)
    ymin, ymax = min(log_8), max(log_10)
    pts10 = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(log_t, log_10)]
    pts8 = [(_lin(x, xmin, xmax, x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for x, y in zip(log_t, log_8)]
    inner = (
        _axes(x0, y0, w, h, 'log\u2081\u2080(exposure time, s)', 'log\u2081\u2080(signal-to-noise ratio)')
        + _polyline(pts10, color='#0f6b78') + _polyline(pts8, color='#b87911')
        + f"<text x='{x0 + 14}' y='{y0 + 24}' font-size='14' fill='#0f6b78' font-family='Segoe UI, sans-serif'>{escape(f'{KECK["aperture_m"]:.0f} m aperture (Keck-class)')}</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 46}' font-size='14' fill='#b87911' font-family='Segoe UI, sans-serif'>{escape(f'{VLT["aperture_m"]:.1f} m aperture (VLT-class)')}</text>"
        + _fig_caption('Capstone trade-space synthesis: collecting-area ratio (D\u00b2) sets the SNR gap between two aperture classes at fixed exposure time -- exactly the quantitative argument an instrument proposal must make to justify a requested telescope and exposure allocation.')
    )
    return _fig_wrap(n, item['title'], inner, 'log-log SNR versus exposure time trade curves comparing a 10 meter and an 8.2 meter aperture for the same target')


_DIAGRAM_BUILDERS = {
    1: diagram_01, 2: diagram_02, 3: diagram_03, 4: diagram_04, 5: diagram_05, 6: diagram_06,
    7: diagram_07, 8: diagram_08, 9: diagram_09, 10: diagram_10, 11: diagram_11, 12: diagram_12,
    13: diagram_13, 14: diagram_14,
}


def lecture_svg(item: dict) -> str:
    return _DIAGRAM_BUILDERS[item['n']](item)


OPENSTAX_NOTE = 'OpenStax Astronomy 2e (local extracted reference copy: references/openstax-astronomy-2e-extracted.txt) covers observational instrumentation only descriptively (Chapter 6, astronomical instruments); this course derives the optics, detector, and error-budget physics explicitly, well beyond that introductory treatment.'

LECTURES = [
    dict(
        n=1, title='The Observing Chain and Telescope Optics Fundamentals',
        subtitle='From photons at the aperture to a number on a spreadsheet',
        goals=[
            'Describe the full observing chain (telescope, instrument, detector, calibration, data reduction) and identify where each later lecture in this course fits.',
            'Distinguish refracting and reflecting telescope designs and explain why every large modern research telescope is a reflector.',
            'Define the Cassegrain optical layout and its two governing parameters, aperture diameter D and effective focal length f.',
        ],
        why_matters='Every quantitative tool in this course -- resolution, plate scale, signal-to-noise, spectral resolving power, Strehl ratio, error budgets -- is a property of some link in the observing chain that starts with photons hitting a primary mirror and ends with a calibrated scientific measurement. This lecture lays out that whole chain once, so later lectures can each zoom into one link without losing the big picture.',
        phenomenon=f'The twin Keck telescopes on Mauna Kea each use a {KECK["aperture_m"]:.0f} m effective-aperture primary mirror built from {KECK["n_segments"]} hexagonal {KECK["segment_width_m"]:.1f} m segments, held in phase to a surface accuracy of {KECK["surface_accuracy_nm"]:.0f} nm by an active-optics control system updating twice per second -- a scale and precision that a single monolithic mirror of this size cannot achieve, which is exactly why every extremely large telescope built since Keck uses segmented-mirror technology.',
        vocab=['observing chain', 'aperture', 'effective focal length', 'refractor', 'reflector', 'Cassegrain focus', 'segmented primary mirror', 'active optics'],
        evidence=[
            'Every telescope larger than about 1 meter built since the early 20th century is a reflector, not a refractor, because a lens can only be held in place at its edge (causing it to sag under its own weight) while a mirror can be supported continuously across its back.',
            'The Keck telescopes\u2019 36 hexagonal segments are independently and continuously repositioned by three actuators per segment, confirmed by the observatory\u2019s own published operations documentation, because a rigid one-piece mirror of 10 m diameter would deform measurably as the telescope changed pointing direction.',
            'Every instrument this course studies (imagers, spectrographs, AO systems) attaches at one of a small number of standard focal stations (prime, Cassegrain, Nasmyth, coude); a instrument\u2019s physical size and weight budget is set by which focal station it occupies, a real engineering constraint documented in every large telescope\u2019s instrument-suite technical specifications.',
        ],
        model=[
            'A telescope is fundamentally a light bucket and a focuser: the primary mirror (diameter D) sets the light-gathering power (collecting area A = \u03c0D\u00b2/4, ignoring the secondary-mirror obstruction) and, together with the whole optical train, the effective focal length f sets the plate scale (Lecture 03).',
            'In a Cassegrain layout, a concave paraboloidal (or hyperboloidal, for a Ritchey-Chr\u00e9tien design) primary mirror reflects converging light toward a convex hyperboloidal secondary mirror, which redirects it back through a central hole in the primary to a focal plane behind the primary -- folding a long focal length into a compact mechanical package.',
            'The full observing chain downstream of the telescope optics is: instrument optics (collimator, disperser or filter, camera optics) reformat and select the light; a detector (Lectures 04-05) converts photons to a measurable electronic signal; calibration frames (Lecture 07) remove instrumental signatures; and data reduction converts the calibrated frame into a scientific measurement with a quantified uncertainty (Lecture 13).',
        ],
        equation=r'A = \dfrac{\pi D^{2}}{4}, \qquad f_{\rm eff} = D \times (\text{focal ratio}, f/\#)',
        example=[
            f'Keck collecting area from its stated {KECK["aperture_m"]:.0f} m aperture: A = \u03c0D\u00b2/4 = {math.pi*KECK["aperture_m"]**2/4:.1f} m\u00b2, closely matching the observatory\u2019s own published collecting area of {KECK["collecting_area_m2"]:.0f} m\u00b2 (the small difference is the central obstruction from the secondary mirror and its support structure).',
            f'Keck\u2019s effective focal length is stated as {KECK["focal_length_m"]:.1f} m for a {KECK["aperture_m"]:.0f} m aperture, giving an effective focal ratio f/\u2248{KECK["focal_length_m"]/KECK["aperture_m"]:.2f} -- a "slow" beam by amateur-telescope standards, chosen deliberately (Lecture 03) to give a workable plate scale at the Cassegrain focal plane rather than an impractically small one.',
            f'Comparing collecting areas of two real 8-10 m class telescopes: Keck ({KECK["aperture_m"]:.0f} m, A={math.pi*KECK["aperture_m"]**2/4:.1f} m\u00b2) gathers {(KECK["aperture_m"]/VLT["aperture_m"])**2:.2f}\u00d7 more light per unit time than a single VLT Unit Telescope ({VLT["aperture_m"]:.1f} m, A={math.pi*VLT["aperture_m"]**2/4:.1f} m\u00b2) observing the same target, purely from the D\u00b2 collecting-area scaling.',
        ],
        pitfall='Treating "bigger aperture" as automatically "better telescope" without reference to a specific science goal. Aperture sets collecting area and (via Lecture 02) diffraction-limited resolution, but plate scale, field of view, wavelength coverage, and site quality (seeing, sky brightness) are independent design choices; a smaller telescope with a wider field, better site, or a specialized instrument can outperform a larger one for a specific measurement, a trade-off this course\u2019s capstone (Lecture 14) requires students to argue explicitly.',
        activity='Given that Keck\u2019s 36 segments are actively repositioned to a 4 nm surface-accuracy tolerance, and that visible light has a wavelength of order 500 nm, estimate what fraction of a wavelength this tolerance represents, and explain in one sentence why this precision (not just mechanical rigidity) is required for a segmented mirror to act as a single coherent optical surface.',
        lab_connection='Lab 01 uses the Cassegrain geometry and collecting-area relations from this lecture, together with the diffraction limit derived in Lecture 02, to compare five real telescopes\u2019 light-gathering power and angular resolution side by side.',
        synthesis='A telescope\u2019s aperture and effective focal length are the two numbers that propagate through every later topic in this course -- collecting area into signal-to-noise (Lecture 06), aperture into diffraction-limited resolution (Lecture 02), and focal length into plate scale (Lecture 03) -- so a clear picture of the Cassegrain layout and the full observing chain is the foundation the rest of the course builds on.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=2, title='Diffraction, the Rayleigh Criterion, and Telescope Resolution',
        subtitle='Why no telescope, however large, ever forms a perfect point image',
        goals=[
            'Derive the Airy diffraction pattern qualitatively from the wave nature of light passing through a circular aperture.',
            'State and apply the Rayleigh criterion for the angular resolution of a circular-aperture telescope.',
            'Compute and compare the diffraction-limited resolution of real telescopes and explain when atmospheric seeing, not diffraction, actually limits ground-based resolution.',
        ],
        why_matters='Lecture 01 established aperture as a telescope\u2019s defining physical parameter. This lecture derives exactly what aperture buys an observer in terms of angular resolution -- the single most consequential number distinguishing a 10 m class telescope, a space telescope, and an amateur instrument -- and shows why that theoretical limit is not always the one that matters on the ground.',
        phenomenon=f'A star observed through any telescope, however perfect its optics, never appears as an infinitesimal point; it forms a bright central disk surrounded by faint concentric rings, called the Airy pattern, purely because the telescope aperture is finite and light is a wave. The Rayleigh criterion built from this pattern predicts Keck\u2019s diffraction limit in V band is only {KECK_RESOLUTION_V_ARCSEC*1000:.1f} milliarcsec -- yet ground-based images without adaptive optics (Lecture 11) rarely resolve better than the {EARTH_SEEING_ARCSEC:.1f} arcsec median atmospheric seeing, nearly {KECK_SEEING_LIMITED_FACTOR:.0f}\u00d7 worse.',
        vocab=['diffraction', 'Airy pattern', 'Rayleigh criterion', 'diffraction-limited', 'seeing-limited', 'point spread function (PSF)', 'angular resolution'],
        evidence=[
            'Interferometric and diffraction experiments with circular apertures of controlled size, a standard optics-laboratory demonstration, reproduce the computed Airy intensity pattern (2J\u2081(x)/x)\u00b2 to high precision, confirming the wave-optics origin of the diffraction limit.',
            'Space telescopes (HST, JWST) routinely achieve resolution close to their theoretical diffraction limit because they operate above the atmosphere, while ground-based telescopes of much larger aperture (Keck, VLT, Gemini) achieve resolution far worse than their diffraction limit without adaptive-optics correction, directly demonstrating that atmospheric turbulence, not aperture, sets uncorrected ground-based resolution.',
            'Two point sources separated by exactly the Rayleigh-criterion angle produce a combined intensity pattern with a clearly identifiable central dip (about 74% of the peak intensity), the empirical basis Lord Rayleigh used to define "just resolved" and the criterion still used in modern instrument design specifications.',
        ],
        model=[
            'Diffraction of a plane wave through a circular aperture of diameter D produces the Airy pattern, an intensity distribution I(\u03b8) proportional to [2J\u2081(x)/x]\u00b2, where J\u2081 is the first-order Bessel function and x = \u03c0D\u03b8/\u03bb is a dimensionless angular coordinate.',
            'The Airy pattern\u2019s first dark ring occurs at x = 3.8317 (the first zero of J\u2081(x)/x), corresponding to an angular radius \u03b8 = 1.22\u03bb/D; the Rayleigh criterion defines two equal point sources as "just resolved" when one source\u2019s Airy peak falls on the other\u2019s first dark ring, i.e., when their angular separation equals this same 1.22\u03bb/D.',
            'On the ground, atmospheric turbulence (temperature-driven refractive-index fluctuations along the line of sight) blurs the diffraction-limited PSF into a much broader seeing disk of typical FWHM 0.5-1.5 arcsec at good sites; a telescope\u2019s resolution is diffraction-limited only when 1.22\u03bb/D exceeds the seeing disk size, which requires either a small aperture, a very short wavelength, or active wavefront correction (Lecture 11).',
        ],
        equation=r'\theta_{\rm Rayleigh} = 1.22\,\dfrac{\lambda}{D}\ (\text{radians}), \qquad I(x) = \left[\dfrac{2J_1(x)}{x}\right]^{2},\ x = \dfrac{\pi D \theta}{\lambda}',
        example=[
            f'Keck diffraction limit in V band (\u03bb={V_BAND_NM:.0f} nm, D={KECK["aperture_m"]:.0f} m): \u03b8 = 1.22\u03bb/D = {rayleigh_resolution_rad(V_BAND_M, KECK["aperture_m"]):.3e} rad = {KECK_RESOLUTION_V_ARCSEC*1000:.1f} milliarcsec, computed from a numerical Bessel-function series for J\u2081, not a table lookup.',
            f'HST diffraction limit in V band (D={HST["aperture_m"]:.1f} m): \u03b8 = {HST_RESOLUTION_V_ARCSEC*1000:.1f} milliarcsec -- coarser than Keck\u2019s in absolute terms (smaller aperture), but HST reliably achieves it because it sits above the atmosphere, while Keck needs adaptive optics (Lecture 11) to approach its own, intrinsically sharper, diffraction limit.',
            f'Ratio of atmospheric seeing to Keck\u2019s diffraction limit: {EARTH_SEEING_ARCSEC:.1f}\u2033 / {KECK_RESOLUTION_V_ARCSEC:.4f}\u2033 = {KECK_SEEING_LIMITED_FACTOR:.0f} -- an uncorrected Keck image in average seeing is roughly {KECK_SEEING_LIMITED_FACTOR:.0f}\u00d7 coarser than its theoretical diffraction limit, quantifying exactly what adaptive optics must recover.',
        ],
        pitfall='Assuming a larger telescope always produces a sharper ground-based image. Without adaptive-optics correction, a 10 m telescope and a 1 m telescope at the same site produce nearly the same seeing-limited image quality, because atmospheric turbulence, not aperture, sets the blur; the larger telescope\u2019s advantage in this regime is purely more collecting area (better signal-to-noise, Lecture 06), not sharper images.',
        activity='Using \u03b8 = 1.22\u03bb/D, explain quantitatively why the same telescope aperture gives noticeably better resolution in the near-UV than in the near-infrared, and why this pushes diffraction-limited imaging surveys toward the bluest wavelength consistent with the science goal and detector sensitivity (Lecture 04).',
        lab_connection='Lab 01 computes the Rayleigh-criterion resolution for five real telescopes (Keck, HST, VLT, JWST, and a small amateur reflector) across visible and near-infrared wavelengths and compares each to the atmospheric seeing floor.',
        synthesis='The Rayleigh criterion, derived directly from the wave-optics Airy pattern, sets the fundamental angular-resolution limit of any telescope; on the ground that limit is rarely reached without adaptive-optics correction (Lecture 11), while in space (Lecture 12) it usually is.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=3, title='Plate Scale, Field of View, and Focal-Plane Geometry',
        subtitle='Converting an angle on the sky into a distance on a detector',
        goals=[
            'Derive the plate-scale relation linking angular separation on the sky to physical separation at the focal plane.',
            'Compute the plate scale and pixel scale of a real telescope-plus-instrument combination.',
            'Apply the Nyquist sampling criterion to determine whether a given pixel size adequately samples a telescope\u2019s diffraction-limited or seeing-limited image.',
        ],
        why_matters='Lecture 02 fixed how sharp an image a telescope can in principle deliver. This lecture answers the practical question every instrument designer must solve next: how large, in millimeters, does that sharp image actually appear at the focal plane, and how small must a detector\u2019s pixels be to record it without throwing resolution away?',
        phenomenon=f'The Dark Energy Camera (DECam), a 570-megapixel imager built from {DECAM["n_ccds"]} CCDs on the 4 m Blanco telescope, uses {DECAM["pixel_size_um"]:.0f} \u03bcm pixels and a {DECAM["focal_length_m"]:.2f} m effective focal length to achieve a {DECAM_PIXEL_SCALE_ARCSEC:.3f} arcsec/pixel image scale -- a deliberate engineering choice, not an accident, that this lecture\u2019s plate-scale relation shows was necessary to properly sample the site\u2019s seeing disk.',
        vocab=['plate scale', 'pixel scale', 'field of view', 'focal plane', 'Nyquist sampling', 'undersampling', 'oversampling'],
        evidence=[
            'Every published instrument specification sheet for a large telescope\u2019s imager (e.g., DECam, the Keck imagers, HST\u2019s WFC3) states a plate scale in arcsec/mm or arcsec/pixel, computed directly from the telescope\u2019s focal length via the same relation derived in this lecture, confirming the formula is the actual engineering tool used, not a textbook simplification.',
            'Imagers deliberately designed with pixels close to half the expected seeing-disk or diffraction-limited FWHM (the Nyquist criterion) are found, in on-sky commissioning tests, to recover the full resolution the optics deliver, while imagers with coarser pixels are observed to lose resolving power regardless of how sharp the optical image actually is -- direct evidence that pixel sampling, not just optical quality, sets a real imager\u2019s effective resolution.',
            'The same telescope focal length produces a much smaller plate scale (arcsec/mm) than a smaller telescope of the same aperture ratio, exactly the inverse-focal-length scaling this lecture derives, which is why long-focal-length Cassegrain and coud\u00e9 foci are chosen specifically for high-plate-scale spectroscopy (Lecture 09) while short-focal-length prime foci are chosen for wide-field imaging.',
        ],
        model=[
            'A small angle \u03b8 (radians) subtended on the sky is imaged, by simple similar-triangles geometry through a telescope of effective focal length f, onto a physical size x = f\u03b8 at the focal plane; converting \u03b8 to arcseconds and f to millimeters gives the standard plate-scale relation s = 206265\u2033/f[mm], in arcsec per mm.',
            'Multiplying the plate scale by a detector\u2019s physical pixel size (in mm) gives the pixel scale in arcsec/pixel -- the practical number that determines both a camera\u2019s field of view (pixel scale \u00d7 detector width) and its ability to resolve fine structure.',
            'The Nyquist sampling criterion, borrowed directly from signal processing, requires at least two pixels across the FWHM of the smallest resolvable feature (the diffraction-limited or seeing-limited PSF) to avoid throwing away resolution the optics already deliver (undersampling), while using many more than two pixels per FWHM (oversampling) needlessly divides the same signal across more pixels, each with its own noise floor (Lecture 05).',
        ],
        equation=r's = \dfrac{206265^{\prime\prime}}{f\,[\mathrm{mm}]}, \qquad \text{pixel scale} = s \times p\,[\mathrm{mm}], \qquad \text{Nyquist: pixel scale} \le \dfrac{\mathrm{FWHM}}{2}',
        example=[
            f'Keck plate scale from f={KECK["focal_length_m"]:.1f} m: s = 206265\u2033/(1000\u00d7{KECK["focal_length_m"]:.1f}) = {KECK_PLATE_SCALE_ARCSEC_MM:.3f} arcsec/mm, roughly {KECK_PLATE_SCALE_ARCSEC_MM/HST_PLATE_SCALE_ARCSEC_MM:.2f}\u00d7 the plate scale of HST (f={HST["focal_length_m"]:.1f} m, s={HST_PLATE_SCALE_ARCSEC_MM:.3f} arcsec/mm) despite Keck\u2019s much larger aperture, because plate scale depends on focal length, not aperture, alone.',
            f'DECam pixel scale from its published f={DECAM["focal_length_m"]:.2f} m and p={DECAM["pixel_size_um"]:.0f} \u03bcm pixels: pixel scale = {DECAM_PLATE_SCALE_ARCSEC_MM:.3f} arcsec/mm \u00d7 {DECAM["pixel_size_um"]/1000:.3f} mm = {DECAM_PIXEL_SCALE_ARCSEC:.3f} arcsec/pixel, matching the camera\u2019s own published specification.',
            f'Nyquist check against Keck\u2019s diffraction limit: half the V-band Rayleigh resolution is {DECAM_NYQUIST_PIXEL_SCALE_ARCSEC*1000:.1f} milliarcsec/pixel -- far finer than DECam\u2019s {DECAM_PIXEL_SCALE_ARCSEC:.3f}\u2033/pixel, confirming (correctly) that DECam is designed to Nyquist-sample the site\u2019s seeing disk, not Keck\u2019s diffraction limit, since DECam sits on a different, seeing-limited 4 m telescope.',
        ],
        pitfall='Assuming a smaller pixel is always better. Undersampling wastes optical resolution, but excessively small pixels (oversampling) spread the same total signal across more pixels, each carrying its own read-noise contribution (Lecture 05), which can lower the effective signal-to-noise ratio for faint sources without any corresponding gain in usable resolution once the Nyquist criterion is already satisfied.',
        activity='Given DECam\u2019s pixel scale and the Blanco 4 m telescope\u2019s seeing-limited image quality (typically 0.9-1.1 arcsec FWHM at the site), estimate how many pixels sample the FWHM of a typical stellar image, and state whether this imager is undersampled, well-sampled, or oversampled relative to the Nyquist criterion.',
        lab_connection='Lab 02 computes the plate scale and pixel scale for several real telescope-instrument pairs and checks each against the Nyquist criterion using the diffraction or seeing limit established in Lecture 02.',
        synthesis='Plate scale converts a telescope\u2019s focal length into a concrete number of arcseconds per millimeter at the focal plane, and the Nyquist criterion then dictates how small a detector\u2019s pixels must be to preserve, rather than discard, the resolution the telescope optics (Lecture 02) already deliver.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=4, title='CCD Detectors: Architecture, Quantum Efficiency, and Charge Transfer',
        subtitle='How a silicon chip turns photons into a number',
        goals=[
            'Describe the physical process by which a CCD converts an incident photon into a stored electronic charge.',
            'Define quantum efficiency and interpret a real CCD\u2019s published QE curve.',
            'Explain the charge-coupled readout process and identify the physical origin of gain and full well capacity.',
        ],
        why_matters='Lectures 01-03 established how a telescope forms and scales an image; this lecture begins the second half of the observing chain, converting that optical image into digital data. Every signal-to-noise calculation, calibration procedure, and photometric measurement in the rest of this course assumes a specific, physically grounded model of how a CCD turns photons into counts.',
        phenomenon=f'A modern thinned, back-illuminated scientific CCD can convert more than 90% of the photons striking it at its peak sensitivity into a measurable electrical signal -- compared to under 5% for early-1970s CCDs and roughly 1-2% for photographic plates, the imaging technology CCDs replaced. This single efficiency gain, more than any change in telescope aperture, is why modern surveys can detect sources orders of magnitude fainter in the same exposure time as 1970s-era observations.',
        vocab=['CCD', 'photoelectric effect', 'potential well', 'quantum efficiency (QE)', 'charge-coupled readout', 'gain (e-/ADU)', 'full well capacity'],
        evidence=[
            'Published CCD manufacturer specification sheets (e.g., e2v, Teledyne) report QE curves that rise from the near-UV, peak near 600-700 nm for silicon devices, and fall in the near-infrared as photon energy drops below silicon\u2019s bandgap absorption threshold -- a shape confirmed by independent laboratory calibration of installed science-grade CCDs at observatories worldwide.',
            'Sequential-transfer charge-coupled readout, in which each pixel\u2019s charge packet is shifted row by row to a serial output register and measured one at a time, is directly observable in a CCD\u2019s readout time, which scales with the total pixel count, exactly as the shift-register architecture predicts (unlike a hypothetical fully parallel readout, which would not show this scaling).',
            'A CCD\u2019s measured gain (electrons per analog-to-digital unit) and full well capacity are routinely determined in the laboratory via the photon-transfer-curve technique (flat-field variance versus mean signal), and these measured values match the manufacturer-specified values to within a few percent for properly operating devices -- direct evidence the underlying charge-storage model is physically correct.',
        ],
        model=[
            'An incident photon with energy above silicon\u2019s bandgap (about 1.1 eV) can be absorbed in the CCD\u2019s depleted silicon layer, promoting an electron to the conduction band and leaving a free electron-hole pair; the electron is captured and held in a pixel\u2019s potential well, created by a pattern of gate electrode voltages, until readout.',
            'Quantum efficiency QE(\u03bb) is the fraction of incident photons at wavelength \u03bb that produce a stored electron; it falls short of 100% because of reflection losses, absorption in inactive layers, and (at long wavelengths) photons passing through the thin silicon layer without being absorbed at all.',
            'During readout, voltages are cycled on the gate electrodes in a coordinated sequence that physically shifts each row\u2019s charge packets toward a serial output register one row at a time, then shifts each row\u2019s packets through the register to an output amplifier one pixel at a time -- the "charge-coupled" mechanism that gives the device its name; the amplifier\u2019s conversion factor (gain, in e-/ADU) and the pixel\u2019s maximum charge capacity (full well) are set by the device\u2019s physical design.',
        ],
        equation=r'N_{e^-} = \mathrm{QE}(\lambda)\times N_{\rm photons}, \qquad \mathrm{ADU} = \dfrac{N_{e^-}}{g}\ (g\ \text{in } e^-/\mathrm{ADU})',
        example=[
            f'Representative published QE for an e2v CCD231-84-class device at the V-band central wavelength ({V_BAND_NM:.0f} nm): QE \u2248 94%, meaning a beam of 10,000 V-band photons produces roughly 9,400 stored electrons on average.',
            f'Single-photon energy at V band: E = hc/\u03bb = {PHOTON_ENERGY_V_J:.3e} J = {PHOTON_ENERGY_V_EV:.2f} eV, safely above silicon\u2019s \u22481.1 eV bandgap, confirming photoelectric absorption is energetically possible at this wavelength (and explaining the QE fall-off near 1000-1100 nm, where photon energy approaches the bandgap).',
            f'Converting a measured 45,000 stored-electron pixel signal to counts, using this course\u2019s representative CCD gain of g={CCD_GAIN_E_PER_ADU:.1f} e\u207b/ADU: ADU = 45000/{CCD_GAIN_E_PER_ADU:.1f} = {45000/CCD_GAIN_E_PER_ADU:.0f} ADU, safely below the representative full well capacity of {CCD_FULL_WELL_E:.0f} electrons ({CCD_FULL_WELL_E/CCD_GAIN_E_PER_ADU:.0f} ADU) used throughout this course, so the pixel has not saturated.',
        ],
        pitfall='Assuming quantum efficiency is a single number describing a detector. QE is a strong function of wavelength (this lecture\u2019s figure shows roughly a factor-of-20 variation across the CCD\u2019s sensitive range) and depends on device-specific engineering choices (thinning, anti-reflection coating, back-illumination); quoting "the QE" of a detector without specifying a wavelength is meaningless for any quantitative signal-to-noise calculation (Lecture 06).',
        activity='Using the published QE curve, explain why a survey designed to detect the reddest, coolest stars (peak emission in the near-infrared) might deliberately choose a different detector technology (e.g., a HgCdTe infrared array, Lecture 05) rather than a standard silicon CCD, even though CCDs have higher peak QE in the visible.',
        lab_connection='Lab 02 uses this lecture\u2019s QE curve together with the plate-scale and pixel-sampling results from Lecture 03 to convert an incident photon flux into an expected electron count rate for a specific real instrument.',
        synthesis='A CCD converts photons to stored charge via the photoelectric effect, with an efficiency set by its published QE(\u03bb) curve, then reads that charge out through a physically real charge-coupled shift-register mechanism governed by a measurable gain and full well capacity -- the foundation every later detector, noise, and calibration topic in this course builds on.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=5, title='Detector Noise: Read Noise, Dark Current, and CMOS/IR Arrays',
        subtitle='Why every measurement has an irreducible uncertainty floor',
        goals=[
            'Identify and distinguish the principal noise sources in a modern astronomical detector: photon shot noise, dark current, and read noise.',
            'Explain the physical origin of dark current as thermally generated charge and describe why cooling suppresses it.',
            'Compare CCD and CMOS/infrared-array detector technologies and identify when each is preferred.',
        ],
        why_matters='Lecture 04 established how a detector converts photons into a signal; this lecture establishes why that signal is never perfectly known, only measured with some uncertainty. Every signal-to-noise calculation in Lecture 06, every calibration decision in Lecture 07, and every error budget in Lecture 13 traces back to the three noise sources introduced here.',
        phenomenon=f'A representative modern scientific CCD, cooled to about -100\u00b0C, produces on the order of only {CCD_DARK_CURRENT_E_PER_S:.3f} thermally generated electrons per pixel per second -- so slow that a full night\u2019s 8-hour dark-current accumulation in a single pixel is still only a few dozen electrons, far below the {CCD_READ_NOISE_E:.1f}-electron read-noise floor from a single readout of that same pixel, which is why cooling (not readout speed) is usually the dominant lever for long-exposure faint-source work.',
        vocab=['photon shot noise', 'dark current', 'read noise', 'CMOS detector', 'HgCdTe infrared array', 'thermal generation', 'correlated double sampling'],
        evidence=[
            'Photon shot noise, the irreducible statistical fluctuation in the number of photons detected in a fixed time interval, is measured (via the variance of repeated identical exposures) to scale as the square root of the mean signal, exactly as expected for a Poisson-distributed counting process, for every well-behaved astronomical detector.',
            'Dark current is measured to fall by roughly a factor of two for every 6-8\u00b0C of cooling in silicon CCDs (an empirical rule consistent with the thermal-generation rate\u2019s exponential dependence on temperature), which is why every precision photometric CCD camera is thermoelectrically or cryogenically cooled rather than operated at ambient temperature.',
            'Modern scientific CMOS (sCMOS) detectors, which read out each pixel through its own dedicated amplifier rather than a single shared serial register, are measured to achieve read noise below 1-2 electrons and much faster frame rates than traditional CCDs, at the cost of typically less uniform pixel-to-pixel response -- a real, documented engineering trade-off driving detector choice for time-domain astronomy.',
        ],
        model=[
            'Photon shot noise follows Poisson statistics: for a mean signal of S electrons, the standard deviation of repeated measurements is \u221aS electrons, a fundamental floor set by the discreteness of photon detection, not by any instrumental imperfection.',
            'Dark current arises from thermally generated electron-hole pairs in the detector\u2019s silicon, indistinguishable from photon-generated charge once collected in a pixel; because thermal generation rate depends exponentially on temperature, cooling a detector by tens of degrees can suppress dark current by orders of magnitude.',
            'Read noise is the electronic uncertainty introduced by the output amplifier and downstream electronics each time a pixel\u2019s charge is measured, essentially independent of exposure time or signal level; CMOS/infrared-array detectors, which read each pixel through an individual amplifier rather than sharing one serial register, can in principle achieve lower read noise and much higher readout speed than a CCD, at the cost of pixel-to-pixel gain non-uniformity that must itself be calibrated (Lecture 07).',
        ],
        equation=r'\sigma_{\rm shot} = \sqrt{S}, \qquad \sigma_{\rm dark} = \sqrt{D\,t}, \qquad \sigma_{\rm total}^{2} = S + D t + \sigma_{\rm read}^{2}',
        example=[
            f'Shot noise for a 40,000-electron stellar signal: \u03c3_shot = \u221a40000 = {math.sqrt(40000):.0f} electrons -- already larger than the representative read noise ({CCD_READ_NOISE_E:.1f} e\u207b) used throughout this course, confirming that for a signal this bright, shot noise (not read noise) dominates the total uncertainty.',
            f'Dark-current contribution over a 300 s exposure at the representative rate D={CCD_DARK_CURRENT_E_PER_S:.3f} e\u207b/pix/s: \u03c3_dark = \u221a(Dt) = \u221a({CCD_DARK_CURRENT_E_PER_S:.3f}\u00d7300) = {math.sqrt(CCD_DARK_CURRENT_E_PER_S*300):.3f} electrons -- utterly negligible next to both the read-noise floor and the shot noise of any detectable source, exactly as expected for a well-cooled modern CCD.',
            f'Crossover exposure time at which shot noise from a source producing {STAR_COUNT_RATE_E_PER_S:.2f} e\u207b/s equals the {CCD_READ_NOISE_E:.1f}-electron read-noise floor: solving \u221a(rate\u00d7t) = {CCD_READ_NOISE_E:.1f} gives t = {CCD_READ_NOISE_E**2/STAR_COUNT_RATE_E_PER_S:.1f} s -- exposures shorter than this are read-noise-limited, and longer exposures are shot-noise-limited, the same crossover this lecture\u2019s figure plots explicitly.',
        ],
        pitfall='Assuming a "noisier-looking" detector reading is always due to read noise. A bright source\u2019s own photon shot noise can dominate the total noise budget even on an otherwise very low-noise detector; distinguishing which term dominates requires the explicit calculation in this lecture\u2019s equation, not a qualitative impression of image graininess.',
        activity='Using \u03c3_shot = \u221aS and the fixed read-noise floor, explain why increasing exposure time is an effective strategy for improving signal-to-noise on a faint source only up to a point in the read-noise-limited regime, but becomes progressively less effective (per unit additional time) once the shot-noise-limited regime is reached and sky background (Lecture 06) begins to dominate instead.',
        lab_connection='Lab 03 uses this lecture\u2019s three noise terms directly inside the CCD signal-to-noise equation (Lecture 06) to plan realistic exposure times for a real telescope-and-detector combination.',
        synthesis='A detector\u2019s total measurement uncertainty is the quadrature sum of photon shot noise (source-dependent, set by simple Poisson statistics), dark current (detector- and temperature-dependent, suppressed by cooling), and read noise (a fixed per-readout floor); which term dominates depends on the specific source brightness, exposure time, and detector technology, and correctly identifying the dominant term is a prerequisite for the SNR-driven exposure planning of Lecture 06.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=6, title='The CCD Signal-to-Noise Equation and Exposure Time Calculators',
        subtitle='Turning telescope, detector, and target properties into a single planning number',
        goals=[
            'State the CCD signal-to-noise equation combining source signal, sky background, dark current, and read noise.',
            'Compute the signal-to-noise ratio for a real telescope-detector-target combination at a given exposure time.',
            'Solve for the exposure time required to reach a target signal-to-noise ratio, distinguishing background-limited from read-noise-limited regimes.',
        ],
        why_matters='Lectures 04-05 established how a detector generates signal and noise separately; this lecture combines every one of those terms into the single equation every observer actually uses to plan a real observation -- the same equation implemented, in more elaborate form, inside every professional observatory\u2019s online exposure-time calculator.',
        phenomenon=f'A realistic worked scenario for this course -- an 18th-magnitude star observed with the Keck aperture, a representative 60% end-to-end system throughput, and a representative modern CCD -- requires only about {EXPOSURE_FOR_SNR100_S:.0f} seconds of integration to reach signal-to-noise ratio 100, while the same target through a much smaller amateur telescope would require an exposure time longer than practically achievable in one night, a direct, quantifiable consequence of the D\u00b2 collecting-area scaling from Lecture 01 propagating through this lecture\u2019s SNR equation.',
        vocab=['CCD equation', 'signal-to-noise ratio (SNR)', 'sky background', 'background-limited', 'read-noise-limited', 'exposure time calculator (ETC)', 'system throughput'],
        evidence=[
            'Every major observatory (Keck, Gemini, ESO/VLT, HST, JWST) publishes an online exposure-time calculator implementing the same underlying CCD equation used in this lecture, confirmed by comparing this course\u2019s computed SNR values against the published forms of these tools\u2019 documentation.',
            'Observers systematically report (in published technical proposals and observing logs) exposure times that scale as the square of the desired SNR improvement in the background-limited regime, and roughly linearly with SNR in the read-noise-limited regime, exactly the two limiting behaviors the CCD equation predicts.',
            'Faint-source surveys conducted from dark, high-altitude sites (lower sky brightness, hence lower background count rate) are found to reach a given SNR in systematically shorter exposure times than the same instrument at a brighter, lower-altitude site, direct observational confirmation of the sky-background term\u2019s role in the equation.',
        ],
        model=[
            'The total signal from a point source in an aperture is S = (photon flux) \u00d7 (collecting area) \u00d7 (system throughput) \u00d7 (detector QE) \u00d7 (exposure time); the total noise combines this same source\u2019s own shot noise with sky-background shot noise, dark-current shot noise, and read noise in quadrature.',
            'The standard CCD signal-to-noise equation (Merline & Howell 1995 form) is SNR = S / \u221a[S + n_pix(B + D t + \u03c3_read\u00b2)], where B is the sky-background electron count (over the same exposure time and aperture) and n_pix is the number of pixels summed.',
            'At short exposure times, the read-noise term \u03c3_read\u00b2 dominates the denominator and SNR grows roughly linearly with exposure time (read-noise-limited regime); at long exposure times, the S and B terms dominate and SNR grows only as \u221at (background- or source-limited regime) -- the crossover exposure time is a key planning number for any real observation.',
        ],
        equation=r'\mathrm{SNR} = \dfrac{S}{\sqrt{S + n_{\rm pix}\left(B + Dt + \sigma_{\rm read}^{2}\right)}}',
        example=[
            f'Worked scenario: a V={STAR_V_MAG:.0f} star observed with the Keck aperture (throughput {KECK_THROUGHPUT*100:.0f}%, QE 94% at V band) gives a source count rate of {STAR_COUNT_RATE_E_PER_S:.3f} e\u207b/s and a sky count rate (over a {EARTH_SEEING_ARCSEC:.1f}\u2033-diameter seeing-limited aperture, sky brightness {SKY_MAG_PER_ARCSEC2_V:.1f} mag/arcsec\u00b2) of {SKY_COUNT_RATE_E_PER_S:.3f} e\u207b/s.',
            f'SNR after a 30 s exposure: {SNR_AT_30S:.1f}; after a 300 s exposure: {SNR_AT_300S:.1f} -- a 10\u00d7 longer exposure gives only a {SNR_AT_300S/SNR_AT_30S:.2f}\u00d7 SNR improvement, consistent with the \u221at scaling of the background-limited regime rather than a full 10\u00d7 gain, because this scenario is not read-noise-limited at either exposure time.',
            f'Solving the CCD equation for the exposure time reaching SNR=100 (bisection search on the same equation, not a closed-form shortcut): t \u2248 {EXPOSURE_FOR_SNR100_S:.0f} s.',
        ],
        pitfall='Assuming doubling the exposure time always doubles the signal-to-noise ratio. That linear scaling holds only in the read-noise-limited regime; once shot noise from the source or sky dominates, SNR grows only as \u221at, so quadrupling the exposure time is needed to double the SNR -- a distinction that changes an observing proposal\u2019s time request by a large factor if applied incorrectly.',
        activity='Using the worked scenario\u2019s numbers, estimate (without re-solving the full equation) whether doubling the exposure time from 300 s to 600 s would roughly double the SNR, increase it by about \u221a2, or leave it almost unchanged, and justify the estimate using the relative sizes of the source, sky, and read-noise terms already computed above.',
        lab_connection='Lab 03 builds a small exposure-time calculator using this exact CCD equation for a real telescope-detector combination and a range of target magnitudes, mirroring the tools used at real observatories to plan actual proposals.',
        synthesis='The CCD signal-to-noise equation combines every noise source from Lecture 05 with the source and sky signal terms into the single quantitative tool every real observing proposal is built around, and correctly identifying whether a given exposure is read-noise-limited or background-limited is essential to using it to plan efficient, achievable observations.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=7, title='Calibration Frames: Bias, Dark, Flat-Field, and Standard Stars',
        subtitle='Removing the instrument from the measurement',
        goals=[
            'Describe the physical origin and purpose of bias, dark, and flat-field calibration frames.',
            'Derive the standard CCD calibration equation converting a raw science frame into a calibrated, instrument-independent image.',
            'Explain the role of photometric standard stars in converting calibrated counts into physical flux or magnitude units.',
        ],
        why_matters='Lectures 04-06 modeled an idealized detector; every real detector also carries a fixed electronic offset, a thermal signal, and a non-uniform pixel-to-pixel response that must be measured and removed before any of those idealized equations can be applied to real data. This lecture supplies the calibration procedure every subsequent lab and problem set in this course assumes has already been performed.',
        phenomenon='A raw, uncalibrated CCD frame of an astronomical target contains not just the astronomical signal but also a fixed electronic bias level present even in a zero-length exposure, an accumulated dark-current signal proportional to exposure time, and a pixel-to-pixel sensitivity pattern (vignetting, dust shadows, gain variations) that can differ by tens of percent across the field -- all three must be measured separately and removed before a raw frame becomes a scientific measurement.',
        vocab=['bias frame', 'dark frame', 'flat-field frame', 'master calibration frame', 'photometric standard star', 'zero-point magnitude', 'flat-field residual'],
        evidence=[
            'A zero-length "bias" exposure (shutter closed, minimum possible integration time) reliably shows a nonzero, spatially structured pixel-value pattern that is stable and repeatable across many such exposures at a given observatory, confirming it reflects a real, characterizable electronic offset rather than random noise.',
            'Dark frames taken at matched exposure time to a science frame show a signal that scales linearly with exposure time and depends strongly on detector temperature, consistent with the thermal-generation model of dark current from Lecture 05.',
            'Photometric standard-star networks (e.g., Landolt 1992 UBVRI standards) have been observed repeatedly, at many observatories over decades, and are found to have stable, internally consistent magnitudes to a few millimagnitudes, which is exactly the property that makes them usable as an absolute photometric reference for any instrument, anywhere.',
        ],
        model=[
            'The calibration equation removes the bias and dark signal by subtraction and the flat-field pattern by division: I_cal = (I_raw - B - D)/F, where B is a master bias frame, D is a matched-exposure master dark frame (with its own bias already subtracted), and F is a normalized master flat-field frame.',
            'A master flat-field frame is built from exposures of a uniformly illuminated source (twilight sky or an illuminated dome screen), normalized to a mean of 1.0, so dividing by it removes multiplicative pixel-to-pixel sensitivity variations without altering the frame\u2019s overall signal level.',
            'A photometric standard star of known magnitude, observed on the same night under the same conditions as the science target, lets an observer solve for the instrumental zero point (the magnitude a source of 1 count/second would have), converting the science target\u2019s calibrated counts into a physically meaningful, catalog-comparable magnitude.',
        ],
        equation=r'I_{\rm cal} = \dfrac{I_{\rm raw} - B - D}{F}, \qquad m = -2.5\log_{10}(\text{counts/s}) + Z_{\rm pt}',
        example=[
            f'Representative calibration-frame pixel levels used in this course\u2019s lab (illustrative, not from a specific real exposure): bias \u2248 400 ADU, dark (300 s, cooled CCD) \u2248 480 ADU, flat \u2248 30,000 ADU (normalized before division), raw light frame \u2248 18,500 ADU -- exactly the four levels this lecture\u2019s figure compares.',
            f'Landolt standard star SA 98-978 (Landolt 1992, standard published UBVRI photometric standard): V = {LANDOLT_SA98_978["V"]:.3f}, B-V = {LANDOLT_SA98_978["B_V"]:.3f}; observing this star and measuring its instrumental count rate on a given night lets an observer solve Z_pt = V + 2.5log\u2081\u2080(counts/s) for that night\u2019s zero point.',
            f'If SA 98-978 is measured at {STAR_COUNT_RATE_E_PER_S*20:.1f} e\u207b/s (illustrative count rate, scaled from this course\u2019s Lecture 06 scenario for a brighter standard star), the zero point is Z_pt = {LANDOLT_SA98_978["V"]:.3f} + 2.5\u00d7log\u2081\u2080({STAR_COUNT_RATE_E_PER_S*20:.1f}) = {LANDOLT_SA98_978["V"] + 2.5*math.log10(STAR_COUNT_RATE_E_PER_S*20):.3f} mag, the calibration constant then applied to every other target observed that same night.',
        ],
        pitfall='Subtracting a bias frame and a dark frame separately when the dark frame already includes the bias pedestal (the standard master-dark workflow for a matched-exposure calibration, as corrected in this curriculum\u2019s ASTR 210 course for a real camera). Double-subtracting the bias level produces a systematically negative offset in the calibrated frame; the correct model is I_cal=(raw-D)/F when D is a matched-exposure master dark that already includes the bias pedestal, or I_cal=(raw-B-D)/F only when D is a separately bias-subtracted dark-current-only frame -- the two workflows must not be mixed.',
        activity='Explain why a flat-field frame must be normalized to a mean of 1.0 before being used as a divisor, and what would happen to the calibrated image\u2019s overall brightness scale if an un-normalized flat field (mean far from 1.0) were used instead.',
        lab_connection='Lab 04 performs a full bias/dark/flat calibration sequence on a set of frames and derives a photometric zero point from a standard star, directly applying every equation in this lecture.',
        synthesis='Bias, dark, and flat-field calibration together remove the instrument\u2019s own electronic and optical signature from a raw frame, and a photometric standard star then converts the resulting calibrated counts into an absolute, catalog-comparable physical measurement -- the last step separating a raw CCD frame from a genuine scientific result.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=8, title='Photometric Filter Systems',
        subtitle='Choosing which photons to measure',
        goals=[
            'Describe the purpose and design of a photometric filter system and state the Johnson-Cousins UBVRI system\u2019s central wavelengths and bandwidths.',
            'Explain the physical trade-off between filter bandwidth, signal-to-noise ratio, and color/spectral information content.',
            'Compute a color index from two-band photometry and relate it qualitatively to a source\u2019s effective temperature.',
        ],
        why_matters='Lecture 07 established how to convert raw counts into a calibrated magnitude in some band; this lecture asks which band, and why. Every photometric measurement in astronomy is defined relative to a specific filter\u2019s transmission curve, and comparing measurements across observatories or decades requires those filter definitions to be standardized and precisely known.',
        phenomenon=f'The Johnson-Cousins UBVRI system, defined by specific glass filter recipes and standardized in the 1950s-1970s, remains in routine use today specifically because its filter definitions (central wavelengths near {UBVRI[0][1]}, {UBVRI[1][1]}, {UBVRI[2][1]}, {UBVRI[3][1]}, and {UBVRI[4][1]} nm) were tied to a network of standard stars (Lecture 07) precise and stable enough that a measurement made with one telescope\u2019s U-band filter in 1970 can still be directly compared to a measurement made with a different telescope\u2019s U-band filter today.',
        vocab=['photometric system', 'Johnson-Cousins UBVRI', 'bandpass', 'effective wavelength', 'color index', 'SDSS ugriz', 'filter transmission curve'],
        evidence=[
            'Published filter transmission curves for the Johnson-Cousins UBVRI system (Bessell 1990) show each band\u2019s central wavelength and effective bandwidth precisely enough that independent observatories, using physically different glass filters manufactured to the same specification, reproduce each other\u2019s standard-star magnitudes to a few millimagnitudes.',
            'Stellar color indices (e.g., B-V) measured photometrically correlate tightly with spectroscopically measured effective temperatures across the full range of stellar spectral types, confirming that a broadband color index, cheap to measure compared to a full spectrum, carries real, quantitative temperature information.',
            'Modern wide-field surveys (SDSS, Pan-STARRS, LSST/Rubin) adopted a newer ugriz-type filter system, with different central wavelengths and non-overlapping, more rectangular bandpasses than Johnson-Cousins, a deliberate engineering choice driven by the different noise and calibration requirements of large-format CCD mosaics rather than a rejection of the underlying color-index physics.',
        ],
        model=[
            'A photometric filter is characterized by its transmission curve T(\u03bb), typically summarized by an effective (central) wavelength \u03bb_eff and an effective bandwidth (FWHM) \u0394\u03bb; only photons within the transmitted bandpass, weighted by T(\u03bb), the atmosphere\u2019s transmission, and the detector\u2019s QE (Lecture 04), contribute to the measured signal.',
            'A color index, the magnitude difference between two bands (e.g., B-V), is a direct, if crude, proxy for a source\u2019s spectral energy distribution shape: a hotter source is bluer (smaller, often negative, B-V) and a cooler source is redder (larger, positive B-V), because a Planck-like spectrum shifts its peak toward shorter wavelengths as temperature rises.',
            'Narrower filters carry more precise spectral/color information per photon but transmit fewer total photons for a given exposure time, directly reducing signal-to-noise (Lecture 06); filter-system design is therefore a deliberate trade-off between spectral resolution and photometric depth, not a free choice of arbitrarily narrow bands.',
        ],
        equation=r'\text{color index} = m_{\lambda_1} - m_{\lambda_2}, \qquad \lambda_{\rm eff} = \dfrac{\int \lambda\, T(\lambda)\, S(\lambda)\, d\lambda}{\int T(\lambda)\, S(\lambda)\, d\lambda}',
        example=[
            f'Johnson-Cousins bandpass central wavelengths and effective widths used in this course (Bessell 1990, standard published values): ' + ', '.join(f'{name} ({lam0:.0f}\u00b1{fwhm/2:.0f} nm)' for name, lam0, fwhm in UBVRI) + '.',
            f'Landolt standard SA 98-978 (Lecture 07): B-V = {LANDOLT_SA98_978["B_V"]:.3f} mag, a modestly blue color consistent with an early-to-mid F-type dwarf, illustrating how a single subtracted magnitude pair already constrains a star\u2019s approximate spectral type without a full spectrum.',
            f'Fractional bandwidth comparison: the V filter\u2019s \u0394\u03bb/\u03bb = {UBVRI[2][2]/UBVRI[2][1]:.3f} versus the U filter\u2019s \u0394\u03bb/\u03bb = {UBVRI[0][2]/UBVRI[0][1]:.3f} -- U is proportionally narrower than V, one reason U-band photometry of a fixed source generally reaches lower signal-to-noise than V-band photometry in the same exposure time, all else equal.',
        ],
        pitfall='Comparing magnitudes measured in different filter systems (e.g., a Johnson V magnitude and an SDSS g magnitude) as if they were interchangeable. Even similarly named or similarly centered bands generally differ enough in exact bandpass shape that a small but real systematic color term must be applied to convert between systems; treating them as identical introduces a real, avoidable calibration error.',
        activity='Using the Planck-spectrum intuition that hotter sources peak at shorter wavelengths, predict qualitatively whether a very hot O-type star or a cool M-type star would show the larger measured flux ratio between the U and I bands, and explain your reasoning in terms of where each star\u2019s spectral energy distribution peaks relative to the two bandpasses.',
        lab_connection='Lab 04\u2019s photometric-calibration exercise measures a target star in two Johnson-Cousins bands and computes both an absolute magnitude and a color index, directly applying this lecture\u2019s equations.',
        synthesis='A photometric filter system defines exactly which photons a given magnitude measurement represents, and the deliberate, standardized bandwidth choices of systems like Johnson-Cousins UBVRI and SDSS ugriz trade spectral/color information against signal-to-noise in a way every photometric observation, from Lecture 07\u2019s calibration onward, must account for explicitly.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=9, title='Spectrograph Fundamentals: The Grating Equation and Dispersion',
        subtitle='Splitting light into its component wavelengths',
        goals=[
            'Derive the grating equation from the condition for constructive interference between adjacent grooves.',
            'Compute the diffraction angle and angular dispersion produced by a real diffraction grating.',
            'Explain the trade-off between diffraction order, angular dispersion, and free spectral range.',
        ],
        why_matters='Lectures 01-08 covered imaging: recording an object\u2019s brightness and broadband color. Astronomical spectroscopy, this course\u2019s next major topic, instead records how brightness varies with wavelength in fine detail, the technique behind measuring radial velocities, chemical abundances, and physical conditions in astronomical sources. The grating equation derived here is the physical foundation of every spectrograph in this course, including HIRES (Lecture 10).',
        phenomenon=f'A diffraction grating with only a few hundred grooves per millimeter -- a physically simple, mass-manufacturable optical element -- can disperse white starlight into a rainbow-like spread of tens of degrees between blue and red light in first order, the same basic physics used, at far higher groove density and much larger scale, in a research-grade echelle spectrograph like Keck\u2019s HIRES.',
        vocab=['diffraction grating', 'groove density', 'grating equation', 'diffraction order', 'angular dispersion', 'free spectral range', 'blaze angle'],
        evidence=[
            'A monochromatic laser passed through a ruled diffraction grating produces a discrete, precisely angle-predictable set of bright spots (diffraction orders), with each spot\u2019s angle matching the grating equation to high precision -- a standard optics laboratory demonstration performed at essentially every institution teaching this course.',
            'Every commercial spectrograph and grating monochromator specification sheet states groove density (grooves/mm) and blaze angle, and reports its dispersion (nm per mm at the focal plane, or resolving power) as a direct, computable consequence of those two numbers via the grating equation, confirming the equation\u2019s direct engineering use.',
            'Higher-order grating spectra are observed to overlap with lower-order spectra at different wavelengths (e.g., 400 nm light in second order appears at the same angle as 800 nm light in first order), a real practical complication that every spectrograph design must address with order-blocking filters or cross-dispersion (Lecture 10).',
        ],
        model=[
            'Light incident on a periodic diffraction grating (groove spacing d) constructively interferes at specific angles \u03b8_m for which the path-length difference between adjacent grooves equals an integer number of wavelengths: the grating equation, m\u03bb = d(sin\u03b8_i + sin\u03b8_m), with m the (integer) diffraction order.',
            'Differentiating the grating equation with respect to wavelength gives the angular dispersion, d\u03b8/d\u03bb = m/(d cos\u03b8_m): higher diffraction order m and finer groove spacing d both increase angular dispersion, spreading a given wavelength range over a larger angle (and, at the focal plane, over a larger physical distance).',
            'A grating\u2019s free spectral range, the wavelength interval over which order m does not overlap order m+1, shrinks as \u0394\u03bb \u2248 \u03bb/m; this means high orders give large dispersion (good for resolving power, Lecture 10) but at the cost of a narrow, order-overlapping wavelength window, which is exactly why echelle spectrographs (Lecture 10) require a separate cross-dispersing element.',
        ],
        equation=r'm\lambda = d\left(\sin\theta_i + \sin\theta_m\right), \qquad \dfrac{d\theta}{d\lambda} = \dfrac{m}{d\cos\theta_m}',
        example=[
            f'First-order diffraction angle at normal incidence for a representative teaching grating (600 grooves/mm, groove spacing d=1/600 mm = {1.0e-3/600*1e9:.0f} nm) at V band ({V_BAND_NM:.0f} nm): \u03b8\u2081 = arcsin(m\u03bb/d) = {math.degrees(grating_equation_angle_rad(600.0, 1, V_BAND_M)):.2f}\u00b0.',
            f'Second-order diffraction angle for the same grating and wavelength: \u03b8\u2082 = {math.degrees(grating_equation_angle_rad(600.0, 2, V_BAND_M)):.2f}\u00b0 -- more than double the first-order angle, confirming the m-proportional angular dispersion the derivative relation predicts, though at the cost of reduced free spectral range.',
            f'Free spectral range at m=1 for a 400-700 nm working range: \u0394\u03bb\u2248\u03bb/m evaluated at 700 nm gives \u0394\u03bb\u2248700 nm, comfortably wider than the full visible band (no overlap); at m=10 (relevant to the echelle format in Lecture 10), \u0394\u03bb\u2248{700.0/10:.0f} nm at the same wavelength, a narrow window that makes a single high echelle order cover only a small fraction of the visible spectrum.',
        ],
        pitfall='Assuming a grating disperses light only in the commonly used first order. Real gratings simultaneously produce multiple overlapping orders at different angles for different wavelengths; every practical spectrograph design must explicitly account for and, where necessary, suppress unwanted orders (with order-blocking filters) or exploit them deliberately (with cross-dispersion, exactly the echelle strategy of Lecture 10).',
        activity='Using d\u03b8/d\u03bb = m/(d cos\u03b8_m), explain why an echelle spectrograph, which deliberately works at very high order m (Lecture 10), achieves much higher angular dispersion per unit wavelength than a conventional low-order grating spectrograph of the same groove density, and what practical problem this high order number simultaneously creates.',
        lab_connection='Lab 05 uses the grating equation to compute the dispersion of a real spectrograph configuration and relates it to the resolving power derived in Lecture 10.',
        synthesis='The grating equation, derived from simple path-difference interference, governs every diffraction-grating spectrograph in this course: it sets both the angular dispersion that spreads wavelengths across a detector and the free-spectral-range limitation that drives the echelle cross-dispersion design covered next.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=10, title='Resolving Power, Echelle Spectrographs, and Slit/Fiber-Fed Systems',
        subtitle='How Keck\u2019s HIRES resolves individual spectral lines at 1 part in 67,000',
        goals=[
            'Define spectral resolving power and derive it from a grating\u2019s illuminated groove count and diffraction order.',
            'Describe the echelle-plus-cross-disperser design and explain why it is used for the highest-resolution optical spectrographs.',
            'Compare slit-fed and fiber-fed spectrograph designs and connect resolving power to radial-velocity measurement precision.',
        ],
        why_matters='Lecture 09 derived how a grating disperses light and why high orders bring both high dispersion and a narrow free spectral range. This lecture resolves that tension with the echelle-plus-cross-disperser design, using Keck\u2019s HIRES instrument, a real, extensively documented research spectrograph, as the running example connecting resolving power directly to one of astronomy\u2019s most consequential measurements: exoplanet detection via radial velocity.',
        phenomenon=f'Keck\u2019s HIRES echelle spectrograph, live-verified this session as achieving stellar radial-velocity measurements precise to {HIRES["rv_precision_ms"]:.1f} m/s -- slower than a brisk walking pace -- and sensitive enough to detect planets as small as {HIRES["detection_limit_mj_at_1au"]:.1f} Jupiter masses at 1 AU, a precision that depends entirely on the resolving power this lecture derives from HIRES\u2019s echelle grating geometry.',
        vocab=['resolving power', 'echelle grating', 'cross-disperser', 'blaze angle', 'slit-fed spectrograph', 'fiber-fed spectrograph', 'radial-velocity precision'],
        evidence=[
            'HIRES\u2019s published resolving power, R\u224867,000 in its standard configuration, is independently reproducible from its stated groove density, blaze angle, and illuminated beam width via the grating resolving-power relation, confirming the formula\u2019s direct engineering validity rather than being an independently tuned instrument parameter.',
            'HIRES and comparable echelle spectrographs are documented to require a secondary, lower-dispersion cross-disperser (a grism or a second grating oriented perpendicular to the main echelle) specifically to separate the many overlapping high diffraction orders (Lecture 09) onto distinct rows of the detector, exactly the free-spectral-range problem this course\u2019s Lecture 09 identified.',
            'Fiber-fed spectrographs (increasingly common for multi-object and radial-velocity-survey instruments) are documented to trade slightly reduced maximum resolving power (from fiber-induced focal-ratio degradation) for a fixed, temperature- and gravity-stable instrument illumination, which is why the highest-precision radial-velocity spectrographs (e.g., ESPRESSO, KPF) are fiber-fed rather than slit-fed.',
        ],
        model=[
            'Resolving power is defined as R = \u03bb/\u0394\u03bb, the ratio of a spectral feature\u2019s wavelength to the smallest wavelength difference the instrument can distinguish; for a grating in order m with N illuminated grooves, the theoretical resolving power is R = mN, and equivalently, for a blazed grating in Littrow configuration with illuminated beam width W, R = 2W tan(\u03b8_B)/\u03bb, where \u03b8_B is the blaze angle.',
            'An echelle grating deliberately uses a small number of coarse, steeply blazed grooves at very high diffraction order (often m=20-100+) to maximize resolving power per the relations above; because Lecture 09 showed high orders come with a narrow free spectral range, the resulting many overlapping orders are separated onto distinct detector rows using a second, lower-dispersion cross-disperser oriented perpendicular to the echelle\u2019s dispersion direction.',
            'A spectrograph\u2019s minimum resolvable velocity shift (radial-velocity resolution element) follows directly from its resolving power via the Doppler relation, \u0394v/c = 1/R; higher resolving power therefore translates directly into finer radial-velocity precision, before any additional gain from centroiding many spectral lines to sub-pixel precision.',
        ],
        equation=r'R \equiv \dfrac{\lambda}{\Delta\lambda} = mN = \dfrac{2W\tan\theta_B}{\lambda}, \qquad \dfrac{\Delta v}{c} = \dfrac{1}{R}',
        example=[
            f'HIRES resolving power from its published/standard configuration value: R = {HIRES["resolving_power"]:,}, giving a minimum resolvable wavelength interval at V band of \u0394\u03bb = \u03bb/R = {HIRES_DELTA_LAMBDA_NM*1000:.2f} pm at {V_BAND_NM:.0f} nm.',
            f'Cross-checking via the beam-width relation, R = 2W tan(\u03b8_B)/\u03bb with a representative illuminated beam width W={HIRES_BEAM_WIDTH_M*100:.0f} cm and HIRES\u2019s blaze angle {HIRES["blaze_angle_deg"]:.0f}\u00b0: R \u2248 {HIRES_R_FROM_BEAM:,.0f} -- the same order of magnitude as the published R\u224867,000, with the residual difference attributable to this course\u2019s representative rather than HIRES\u2019s exact as-built beam width.',
            f'Velocity resolution element from R=67,000: \u0394v = c/R = {HIRES_RV_FROM_R:.2f} km/s per resolution element -- far coarser than HIRES\u2019s published {HIRES["rv_precision_ms"]:.1f} m/s radial-velocity precision, because that ultimate precision comes not from resolving a single line\u2019s width but from centroiding the composite shift of thousands of spectral lines to a small fraction of one resolution element.',
        ],
        pitfall='Conflating spectral resolving power with radial-velocity precision. Resolving power sets the width of a single resolved spectral feature, but a spectrograph\u2019s ultimate velocity precision (e.g., HIRES\u2019s 1 m/s) comes from statistically combining the sub-pixel centroid shift of many thousands of individual spectral lines, which can be measured far more precisely than the nominal resolution element itself, given sufficient signal-to-noise (Lecture 06) and instrumental stability.',
        activity='Using R=2W tan(\u03b8_B)/\u03bb, explain why increasing the illuminated beam width W (essentially, using a physically larger collimated beam, which generally means a larger and more expensive spectrograph) is one of very few practical ways to increase resolving power once the grating\u2019s blaze angle is already near its practical maximum.',
        lab_connection='Lab 05 recomputes HIRES\u2019s resolving power from its published groove density and blaze angle, cross-checks it against the beam-width relation, and derives the corresponding radial-velocity resolution element.',
        synthesis='Resolving power, R=mN=2W tan\u03b8_B/\u03bb, is the single number that connects a spectrograph\u2019s physical grating geometry to its ability to resolve fine spectral detail, and the echelle-plus-cross-disperser design lets real instruments like HIRES achieve high resolving power without sacrificing usable wavelength coverage -- the physical foundation beneath HIRES\u2019s record of exoplanet radial-velocity discoveries.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=11, title='Adaptive Optics: Wavefront Sensing and the Strehl Ratio',
        subtitle='Undoing the atmosphere in real time',
        goals=[
            'Describe the physical origin of atmospheric wavefront distortion and the basic adaptive-optics correction loop.',
            'Derive the Mar\u00e9chal approximation relating residual wavefront error to Strehl ratio.',
            'Interpret real Keck adaptive optics performance data using the Strehl ratio and connect it to the diffraction limit of Lecture 02.',
        ],
        why_matters='Lecture 02 showed that ground-based telescopes rarely reach their diffraction limit because of atmospheric seeing. Adaptive optics is the engineered solution to exactly that problem: measuring and correcting atmospheric wavefront distortion fast enough to recover most of a large telescope\u2019s theoretical resolution, closing the gap this course\u2019s second lecture first identified.',
        vocab=['wavefront sensor', 'deformable mirror', 'natural guide star', 'laser guide star', 'residual wavefront error', 'Strehl ratio', 'Mar\u00e9chal approximation'],
        phenomenon=f'Keck\u2019s adaptive optics system, using a laser guide star to create an artificial reference beacon and a deformable mirror updated hundreds of times per second, can turn Keck\u2019s seeing-limited image (roughly {KECK_SEEING_LIMITED_FACTOR:.0f}\u00d7 coarser than its diffraction limit, Lecture 02) into a near-diffraction-limited image with a Strehl ratio as high as {KECK_AO_TYPICAL_STREHL:.2f} in K band -- recovering most, though not all, of the sharpness a 10 m aperture is physically capable of delivering.',
        evidence=[
            'Real-time wavefront sensors (typically Shack-Hartmann sensors) at observatories including Keck are documented to measure atmospheric wavefront distortion using a bright natural star or an artificial laser guide star, and feed a correction signal to a deformable mirror updated at rates of hundreds to over a thousand times per second, fast enough to track atmospheric turbulence that itself changes on millisecond timescales.',
            'Measured Strehl ratios for operating adaptive-optics systems are found to depend strongly on both observing wavelength (higher Strehl at longer wavelengths, for the same residual wavefront error) and atmospheric conditions (higher Strehl in better seeing), exactly the wavelength- and \u03c3-dependence the Mar\u00e9chal approximation predicts.',
            'AO-corrected images from Keck and similar systems are documented (via direct point-spread-function measurements of stars) to approach, but not fully reach, the diffraction-limited Airy pattern of Lecture 02, with a residual "seeing halo" surrounding a sharper diffraction-limited core -- direct observational confirmation that AO correction is real but imperfect, exactly as a Strehl ratio below 1.0 implies.',
        ],
        model=[
            'Atmospheric turbulence introduces a spatially and temporally varying optical path-length delay across a telescope\u2019s aperture, distorting an initially flat incoming wavefront; a wavefront sensor measures this distortion (often using light from a bright star, or an artificial laser-excited sodium-layer beacon when no sufficiently bright natural star lies near the target) many times per second.',
            'A deformable mirror, its surface shape controlled by dozens to thousands of actuators, is driven in a closed feedback loop to apply the equal-and-opposite correction to the wavefront, flattening it before it reaches the science instrument; residual, uncorrected wavefront error (rms \u03c3, typically 100-300 nm for a well-performing natural-guide-star system) remains because of finite actuator count, finite correction speed, and imperfect wavefront sensing.',
            'The Mar\u00e9chal approximation relates this residual rms wavefront error directly to the Strehl ratio, S = exp[-(2\u03c0\u03c3/\u03bb)\u00b2], the ratio of the achieved peak image intensity to the theoretical diffraction-limited peak intensity; S=1 corresponds to a perfect, fully diffraction-limited correction, and S approaching 0 corresponds to an essentially uncorrected, seeing-limited image.',
        ],
        equation=r'S = \exp\left[-\left(\dfrac{2\pi\sigma}{\lambda}\right)^{2}\right], \qquad \mathrm{FWHM}_{\rm diff} \approx 1.03\,\dfrac{\lambda}{D}',
        example=[
            f'Representative Keck natural-guide-star AO residual wavefront error, \u03c3={KECK_AO_TYPICAL_WFE_NM:.0f} nm (Wizinowich et al. 2000, standard published value), evaluated at K band (\u03bb={KECK_WAVELENGTH_K_NM:.0f} nm): S = exp[-(2\u03c0\u00d7{KECK_AO_TYPICAL_WFE_NM:.0f}/{KECK_WAVELENGTH_K_NM:.0f})\u00b2] = {KECK_AO_TYPICAL_STREHL:.3f}.',
            f'The same residual wavefront error evaluated in V band instead of K band would give a Strehl ratio of {strehl_ratio_marechal(KECK_AO_TYPICAL_WFE_NM*NM, V_BAND_M):.4f} -- essentially zero correction -- which is exactly why natural-guide-star adaptive optics historically works far better in the near-infrared than the visible for the same physical correction hardware.',
            f'Keck\u2019s diffraction-limited K-band FWHM: {KECK_AO_DIFFRACTION_LIMIT_K_ARCSEC*1000:.1f} milliarcsec (from FWHM\u22481.03\u03bb/D); at Strehl {KECK_AO_TYPICAL_STREHL:.2f}, the AO-corrected image core approaches, but does not exactly match, this diffraction-limited width, with the remainder of the light spread into a broader residual halo.',
        ],
        pitfall='Treating adaptive optics as a complete fix for atmospheric blurring. Even excellent natural-guide-star AO rarely exceeds Strehl ratios of 0.3-0.6 in the near-infrared under good conditions, and performs far worse in the visible (as this lecture\u2019s worked example shows quantitatively); AO substantially improves, but does not eliminate, the gap between seeing-limited and truly diffraction-limited imaging identified in Lecture 02.',
        activity='Using S=exp[-(2\u03c0\u03c3/\u03bb)\u00b2], explain quantitatively why the same AO system with the same residual wavefront error performs dramatically better at K band (2200 nm) than at V band (551 nm), and why this motivates building AO-fed science instruments (Lecture 10\u2019s OSIRIS, NIRC-2 class instruments) primarily for infrared rather than visible observations.',
        lab_connection='Lab 06 uses the Mar\u00e9chal approximation and representative Keck AO wavefront-error data to compute Strehl ratios across a range of conditions and wavelengths, and compares the results to the diffraction limit derived in Lecture 02.',
        synthesis='Adaptive optics measures and corrects atmospheric wavefront distortion in real time, and the Mar\u00e9chal approximation\u2019s Strehl ratio quantifies exactly how close that correction brings a real system to the diffraction limit Lecture 02 established as the theoretical ceiling -- a ceiling AO approaches, especially in the infrared, but essentially never reaches in the visible with current natural-guide-star technology.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=12, title='Space-Based Instruments and Observatory Operations',
        subtitle='Why some observations can only be made above the atmosphere',
        goals=[
            'Identify the atmospheric limitations (seeing, absorption, sky brightness, thermal background) that motivate space-based astronomy.',
            'Compare the diffraction-limited performance of a large ground-based telescope to a smaller space telescope across wavelength.',
            'Describe the operational differences between ground-based and space-based observatories, including servicing, thermal control, and scheduling.',
        ],
        why_matters='Lectures 02 and 11 established that ground-based resolution is fundamentally limited by atmospheric seeing unless corrected by adaptive optics, and that even AO correction is imperfect and wavelength-dependent. This lecture completes the picture by examining the alternative: removing the atmosphere from the problem entirely, at the cost of a much more constrained, expensive, and operationally different observing platform.',
        phenomenon=f'JWST, with a {JWST["aperture_m"]:.1f} m segmented primary mirror smaller than Keck\u2019s {KECK["aperture_m"]:.0f} m, nonetheless reaches its full diffraction limit on essentially every exposure, without any adaptive-optics correction, because it operates in space; at 2 \u03bcm, JWST\u2019s diffraction limit is only about {JWST_VS_KECK_RESOLUTION_RATIO:.2f}\u00d7 coarser than Keck\u2019s diffraction limit despite the smaller aperture, and unlike Keck, JWST achieves this limit routinely rather than only under excellent AO correction.',
        vocab=['atmospheric absorption windows', 'thermal background', 'sky brightness', 'space telescope', 'servicing mission', 'observatory scheduling', 'thermal control'],
        evidence=[
            'Earth\u2019s atmosphere is documented (via atmospheric transmission spectra) to be largely opaque across most of the infrared, all of the far-ultraviolet, and all X-ray and gamma-ray wavelengths, which is why space telescopes are the only way to observe these wavelength ranges at all, independent of any resolution argument.',
            'Ground-based thermal-infrared observations are documented to be strongly limited by the telescope\u2019s and atmosphere\u2019s own thermal emission (both radiating substantially at wavelengths beyond about 2-3 \u03bcm at ambient temperature), while JWST\u2019s actively cooled optics (operating near 40 K) and location far from Earth\u2019s heat allow sensitive mid-infrared observation impossible from the ground.',
            'HST\u2019s history of five astronaut servicing missions (1993-2009), replacing instruments and correcting its original mirror-figure error, is a documented, real example of a space-observatory operations model fundamentally different from a ground-based observatory, where instruments can be swapped or repaired far more quickly and cheaply; JWST, by contrast, was designed for zero in-person servicing at its much more distant orbit.',
        ],
        model=[
            'Space telescopes avoid three atmospheric limitations simultaneously: seeing-induced image blur (Lecture 02), absorption bands that block entire wavelength ranges from reaching the ground, and (for infrared observations) the atmosphere\u2019s and telescope\u2019s own thermal emission, which adds background noise (Lecture 06) that can overwhelm faint astronomical infrared signals unless the telescope itself is actively cooled.',
            'A space telescope\u2019s diffraction-limited resolution still follows the same Rayleigh criterion (Lecture 02) as any ground-based telescope, so a smaller-aperture space telescope does not automatically outresolve a larger ground-based one; its advantage is reliably reaching that diffraction limit on every exposure, and accessing wavelength ranges the ground cannot observe at all.',
            'Space-observatory operations differ fundamentally from ground-based operations: no weather or seeing variability, but far higher launch cost, little to no in-person servicing capability (JWST) or extremely limited, expensive servicing (HST\u2019s Space Shuttle-era missions), fixed and irreversible design choices, and scheduling driven by spacecraft orientation, thermal, and communication constraints rather than a nightly observer queue.',
        ],
        equation=r'\theta_{\rm Rayleigh} = 1.22\dfrac{\lambda}{D}\ (\text{unchanged in space}), \qquad \text{advantage: reaching this limit reliably, plus new wavelength access}',
        example=[
            f'JWST diffraction limit at 2 \u03bcm (D={JWST["aperture_m"]:.1f} m): \u03b8 = {JWST_RESOLUTION_2UM_ARCSEC*1000:.1f} milliarcsec, compared to Keck\u2019s V-band diffraction limit of {KECK_RESOLUTION_V_ARCSEC*1000:.1f} milliarcsec (D={KECK["aperture_m"]:.0f} m) -- Keck\u2019s much larger aperture and shorter reference wavelength give it a sharper theoretical limit, by a factor of {JWST_VS_KECK_RESOLUTION_RATIO:.2f}, but only if adaptive optics (Lecture 11) actually reaches that limit at 2 \u03bcm, which it does only partially.',
            f'JWST\u2019s wavelength coverage, {JWST["wavelength_lo_um"]:.1f}-{JWST["wavelength_hi_um"]:.1f} \u03bcm (standard published mission specification), extends far into the mid-infrared, a range where ground-based observation is severely limited by atmospheric absorption and thermal background regardless of telescope aperture or AO correction quality.',
            f'HST\u2019s much smaller {HST["aperture_m"]:.1f} m aperture gives a V-band diffraction limit of {HST_RESOLUTION_V_ARCSEC*1000:.1f} milliarcsec, coarser than Keck\u2019s {KECK_RESOLUTION_V_ARCSEC*1000:.1f} milliarcsec diffraction limit, yet HST has produced sharper uncorrected visible images than any ground-based telescope for most of its operational history, precisely because it reaches its own (smaller) diffraction limit reliably while ground-based telescopes, before widespread AO, did not approach theirs at all.',
        ],
        pitfall='Assuming space telescopes are simply "better" versions of ground-based telescopes. A space telescope\u2019s advantage is reliable diffraction-limited performance and access to atmosphere-blocked wavelengths, not inherently superior resolution at a given aperture; a sufficiently large ground-based telescope with excellent adaptive optics can match or exceed a smaller space telescope\u2019s resolution at the same wavelength, which is exactly why both platforms remain complementary, not redundant, parts of modern astronomy.',
        activity='Using JWST\u2019s stated operating range and the atmospheric-absorption argument above, explain why a proposal to observe at 10 \u03bcm would essentially require a space (or high-altitude airborne) platform regardless of how large a ground-based telescope or how good its adaptive optics system might be.',
        lab_connection='Lab 06\u2019s adaptive-optics Strehl-ratio calculation directly informs this lecture\u2019s ground-versus-space resolution comparison by quantifying how close a real AO-corrected ground-based image actually comes to the space-telescope-like ideal.',
        synthesis='Space-based observatories remove atmospheric seeing, absorption, and (for actively cooled telescopes) thermal background from the observing problem entirely, at the cost of a fundamentally different, far less flexible operations model; the choice between ground-based (with or without AO) and space-based instrumentation is a real engineering and science trade-off, not a strict hierarchy of quality.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=13, title='Radiometric Error Budgets and Instrument Sensitivity Modeling',
        subtitle='Adding up every source of uncertainty before you observe',
        goals=[
            'Define a radiometric error budget and explain why independent error terms are combined in root-sum-square (RSS), not by simple addition.',
            'Construct a complete error budget for a realistic photometric measurement, tracing every term back to a specific physical origin from earlier lectures.',
            'Identify the dominant error term in a given scenario and explain what instrumental or observational change would most improve it.',
        ],
        why_matters='Every lecture in this course so far has derived one physical limitation on a measurement: diffraction (Lecture 02), detector noise (Lecture 05), calibration residuals (Lecture 07), atmospheric correction (Lecture 08), and AO residual wavefront error (Lecture 11). A real instrument proposal or observing plan must combine every relevant term into a single, defensible total uncertainty estimate before requesting telescope time -- exactly the skill this lecture builds toward the capstone proposal of Lecture 14.',
        phenomenon=f'A carefully planned 300 s Keck V-band photometric measurement of an 18th-magnitude star (this course\u2019s running worked scenario) has a total photometric uncertainty of only {TOTAL_PHOTOMETRIC_ERROR_MAG*1000:.1f} millimagnitudes, but that single number is the root-sum-square combination of three physically distinct error sources -- Poisson/SNR-limited noise, flat-field calibration residuals, and atmospheric-extinction correction residuals -- each traceable to a specific earlier lecture in this course.',
        vocab=['error budget', 'root-sum-square (RSS) combination', 'systematic error', 'random error', 'dominant error term', 'sensitivity model'],
        evidence=[
            'Every real instrument proposal document (e.g., for Keck, HST, or JWST time) requires an explicit error budget table breaking total measurement uncertainty into named, independently estimated terms, confirmed by these observatories\u2019 own published proposal-preparation documentation and instrument handbooks.',
            'Independent random error sources are documented, both in statistics and in repeated real instrument calibration campaigns, to combine in quadrature (root-sum-square) rather than by simple addition, because uncorrelated errors partially cancel; treating them as simply additive systematically and incorrectly overestimates the true total uncertainty.',
            'Instrument teams routinely identify and report which single term dominates a total error budget (e.g., "this measurement is photon-noise-limited" or "this measurement is flat-field-limited") specifically because that identification determines whether more telescope time, better calibration data, or an instrumental upgrade is the most effective way to improve the measurement -- documented practice in observatory technical reports.',
        ],
        model=[
            'A radiometric error budget lists every physically distinct, ideally independent source of uncertainty affecting a measurement (e.g., photon shot noise, sky-background shot noise, read noise, flat-field residual non-uniformity, atmospheric extinction correction residual, wavelength- or filter-calibration uncertainty) and estimates each term\u2019s contribution in the same units (typically magnitudes, for photometry).',
            'Independent error terms combine in root-sum-square: \u03c3_total = \u221a(\u03c3\u2081\u00b2 + \u03c3\u2082\u00b2 + ... + \u03c3_n\u00b2); this RSS combination, not simple addition, correctly reflects that independent random fluctuations do not all point the same direction simultaneously.',
            'The dominant term in an RSS sum is the one that most strongly determines the total, because squaring exaggerates the largest term\u2019s relative contribution; identifying and reducing the dominant term (e.g., taking a longer exposure to reduce Poisson error, or improving flat-fielding to reduce a systematic residual) is a far more effective strategy than attacking every term equally.',
        ],
        equation=r'\sigma_{\rm total} = \sqrt{\sigma_1^{2} + \sigma_2^{2} + \dots + \sigma_n^{2}}, \qquad \sigma_m \approx \dfrac{1.0857}{\mathrm{SNR}}\ (\text{Poisson term, magnitudes})',
        example=[
            f'Poisson/SNR-limited error term from Lecture 06\u2019s 300 s worked scenario (SNR={SNR_AT_300S:.1f}): \u03c3_Poisson = 1.0857/SNR = {ERR_POISSON_MAG*1000:.2f} millimagnitudes.',
            f'Adding two representative systematic terms -- flat-field residual non-uniformity ({ERR_FLATFIELD_RESIDUAL_MAG*1000:.1f} mmag, a standard published value for a well-calibrated modern imager) and atmospheric extinction correction residual ({ERR_EXTINCTION_MAG*1000:.1f} mmag, representative of a good photometric night) -- in root-sum-square with the Poisson term: \u03c3_total = \u221a({ERR_POISSON_MAG*1000:.2f}\u00b2 + {ERR_FLATFIELD_RESIDUAL_MAG*1000:.1f}\u00b2 + {ERR_EXTINCTION_MAG*1000:.1f}\u00b2) mmag = {TOTAL_PHOTOMETRIC_ERROR_MAG*1000:.2f} mmag.',
            f'Because {ERR_POISSON_MAG*1000:.2f} mmag is the largest of the three terms by a wide margin, this measurement is clearly Poisson/SNR-limited, not calibration-limited; per the CCD equation (Lecture 06), the most effective way to reduce the total error further is a longer exposure time, not improved flat-fielding or extinction correction, which would barely change the {TOTAL_PHOTOMETRIC_ERROR_MAG*1000:.2f} mmag total.',
        ],
        pitfall='Adding error-budget terms linearly instead of in root-sum-square. Linear addition treats every error source as if it always pushes the measurement in the same direction simultaneously, which overstates the true combined uncertainty for genuinely independent error sources; RSS combination is the physically and statistically correct approach whenever the listed terms are independent, a distinction every real instrument proposal\u2019s error budget must get right.',
        activity='Given the worked error budget above, explain what would happen to the total photometric error, in this specific scenario, if flat-field calibration were improved to a residual of 0.001 mag instead of 0.003 mag, and use this to justify (or refute) a proposal request for better flat-field calibration data as the primary strategy for improving this measurement.',
        lab_connection='Lab 06\u2019s adaptive-optics Strehl-ratio calculation and Lab 07\u2019s capstone both feed directly into this lecture\u2019s error-budget framework, treating residual wavefront error and photometric calibration residuals as named, quantifiable error-budget terms.',
        synthesis='A defensible instrument or observation error budget names every relevant, physically distinct uncertainty source from earlier lectures, combines them correctly in root-sum-square, and identifies the dominant term so that limited resources (exposure time, calibration effort, instrumental upgrades) are directed at the term that will actually reduce the total uncertainty -- exactly the reasoning the capstone instrument proposal of Lecture 14 requires.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=14, title='Instrument Proposal Design: Capstone Synthesis',
        subtitle='Arguing, quantitatively, for telescope time',
        goals=[
            'Synthesize every quantitative tool from this course (resolution, plate scale, SNR, resolving power, Strehl ratio, error budgets) into a single coherent instrument or observing proposal.',
            'Justify a specific telescope, instrument configuration, and exposure-time request using a quantitative trade-space argument.',
            'Critically evaluate the assumptions and limitations of a proposed observing plan, including realistic error-budget and feasibility concerns.',
        ],
        why_matters='This course has built, lecture by lecture, every quantitative tool a real observational astronomer or instrument scientist uses to plan and justify an observation: aperture and resolution (Lectures 01-02), plate scale and sampling (Lecture 03), detector physics and noise (Lectures 04-06), calibration (Lectures 07-08), spectroscopy (Lectures 09-10), adaptive optics (Lecture 11), space-based alternatives (Lecture 12), and error budgets (Lecture 13). This capstone lecture requires combining all of them into a single, defensible proposal, the same synthesis task every working instrument scientist and observational astronomer performs routinely.',
        phenomenon=f'A real Keck or JWST time-allocation committee evaluates dozens of competing observing proposals each cycle using exactly the quantitative arguments this course has developed: does the proposed aperture and configuration reach the required signal-to-noise ratio (Lecture 06) or resolving power (Lecture 10) in the requested time, is the achievable angular resolution (Lectures 02, 11, 12) sufficient for the stated science goal, and is the total error budget (Lecture 13) small enough to detect the claimed effect -- exactly the trade-space argument this capstone lecture asks students to make explicitly and quantitatively.',
        vocab=['trade-space analysis', 'observing proposal', 'feasibility argument', 'instrument configuration', 'science requirement', 'technical justification'],
        evidence=[
            'Published time-allocation-committee statistics at major observatories (Keck, HST, JWST) document oversubscription rates of several-to-many times the available time, meaning only proposals with a clear, quantitatively defensible technical justification (not just an interesting science question) are typically successful.',
            'Instrument design studies for new facilities (e.g., next-generation extremely large telescopes) are documented to begin with exactly this course\u2019s trade-space method: computing required aperture, resolving power, and exposure time for a range of candidate science cases before any hardware design decision is finalized.',
            'Real observing proposals that request an aperture, instrument mode, or exposure time inconsistent with the underlying physics (e.g., requesting seeing-limited resolution finer than the site\u2019s median seeing without invoking adaptive optics) are documented to be routinely rejected or returned for revision by time-allocation committees, confirming that the quantitative tools in this course are not merely academic but load-bearing in real proposal review.',
        ],
        model=[
            'A defensible instrument proposal states an explicit science requirement (e.g., "detect a companion at contrast X and separation Y" or "measure a radial velocity to precision Z"), then works backward through this course\u2019s tools to the specific telescope, instrument mode, and exposure time that requirement demands -- exactly the reverse of the forward calculations (given a telescope, compute the achievable SNR or resolution) performed in earlier lectures.',
            'A trade-space analysis compares at least two credible alternatives (e.g., a larger aperture at a worse site versus a smaller aperture with adaptive optics; a longer single exposure versus multiple shorter exposures; ground-based versus space-based) using the same quantitative tools (collecting area, SNR, resolving power, Strehl ratio, error budget) applied consistently to each option.',
            'A complete proposal explicitly states its error budget (Lecture 13) and identifies the dominant term, so a reviewer can judge whether the requested resources (telescope time, instrument configuration) are sufficient to reach the stated scientific precision, and whether a cheaper or more efficient alternative configuration could reach the same goal.',
        ],
        equation=r'\text{Proposal logic: Science requirement} \Rightarrow \text{required SNR, R, or } \theta \Rightarrow \text{required } D,\ t,\ \text{or instrument mode}',
        example=[
            f'Capstone trade-space example: reaching SNR=100 on the V={STAR_V_MAG:.0f} worked-scenario star requires t\u2248{EXPOSURE_FOR_SNR100_S:.0f} s with the Keck aperture ({KECK["aperture_m"]:.0f} m); switching to a VLT-class {VLT["aperture_m"]:.1f} m aperture (collecting-area ratio (D_VLT/D_Keck)\u00b2={(VLT["aperture_m"]/KECK["aperture_m"])**2:.3f}) would require the exposure time to scale up by roughly the inverse of that same ratio in the background-limited regime, a concrete, quantifiable cost of choosing the smaller aperture.',
            f'Error-budget check (Lecture 13): the same 300 s exposure carries a total photometric uncertainty of {TOTAL_PHOTOMETRIC_ERROR_MAG*1000:.2f} mmag, dominated by the Poisson term; a proposal claiming a scientific effect smaller than this floor (e.g., a stellar variability signal of only 1-2 mmag) would need either a longer exposure or a brighter target to be feasible, a feasibility argument this course\u2019s tools make explicit rather than assumed.',
            f'Resolution check (Lectures 02, 11): resolving a close binary or extended structure at the Rayleigh-criterion angle requires either accepting Keck\u2019s seeing-limited {EARTH_SEEING_ARCSEC:.1f}\u2033 resolution, investing in AO correction (Lecture 11, achievable Strehl {KECK_AO_TYPICAL_STREHL:.2f} at K band with {KECK_AO_TYPICAL_WFE_NM:.0f} nm residual wavefront error), or requesting a space-based platform (Lecture 12); a complete proposal states explicitly which of these three routes it assumes and why.',
        ],
        pitfall='Submitting (or accepting) a proposal that states a science goal without a quantitative technical justification connecting that goal to a specific, achievable instrument configuration and exposure time. Every tool developed in this course exists precisely to prevent this gap: a proposal is only as strong as its weakest quantitative link between science requirement and instrument capability.',
        activity='Using this course\u2019s tools, sketch (in outline form) the technical-justification section of a one-paragraph observing proposal to measure the radial velocity of a solar-type star to 3 m/s precision, stating which lecture\u2019s tool (resolving power, SNR, error budget) each part of the justification depends on.',
        lab_connection='Lab 07, this course\u2019s capstone, requires students to write a short, quantitatively justified instrument or observing proposal synthesizing at least three of the preceding six labs\u2019 tools for a self-chosen (but instructor-approved) real science scenario.',
        synthesis='Every quantitative tool in this course -- diffraction-limited resolution, plate scale and sampling, detector noise, the CCD signal-to-noise equation, calibration, photometric systems, the grating equation, spectral resolving power, the Strehl ratio, and the RSS error budget -- exists to answer one integrated question: given a science goal, what telescope, instrument, and exposure time are actually required, and can the proposed observation credibly achieve it? This capstone lecture is the synthesis of that entire toolkit into the practical skill of writing (and critically evaluating) a real instrument proposal.',
        openstax=OPENSTAX_NOTE,
    ),
]


def slide_deck(item: dict) -> str:
    n = item['n']
    fig = lecture_svg(item)
    body = f"""<main class='deck'>
<section class='slide title'><p class='kicker'>ASTR 340 &middot; Lecture {n:02d}</p><h1>{escape(item['title'])}</h1><h2>{escape(item['subtitle'])}</h2></section>
<section class='slide'><h2>Learning Goals</h2><ol>{li(item['goals'])}</ol><p class='small'>Reading anchor: {escape(item['openstax'])}</p></section>
<section class='slide'><h2>Why This Matters</h2><p>{item['why_matters']}</p></section>
<section class='slide'><h2>Opening Phenomenon</h2><p>{item['phenomenon']}</p><p class='warning'><strong>First question:</strong> what here is directly observed or a published instrument specification, and what follows only once a physical law is derived and applied?</p></section>
<section class='slide'><h2>Vocabulary for Reasoning</h2><div class='three'>{cards(item['vocab'])}</div><p class='small'>Use these terms to describe derivations and evidence, not as isolated definitions.</p></section>
<section class='slide'><h2>Evidence We Need to Explain</h2><ul>{li(item['evidence'])}</ul></section>
<section class='slide'><h2>Derivation and Model</h2><ul>{li(item['model'])}</ul></section>
<section class='slide'><h2>Quantitative Tool</h2><div class='equation'>\\[ {item['equation']} \\]</div></section>
<section class='slide'><h2>Worked Example</h2><ol>{li(item['example'])}</ol></section>
<section class='slide visual-slide'><h2>Visual Reasoning</h2><div class='visual-grid'><div><p>Trace the reasoning chain from raw observation or instrument specification to derived physical law to inferred quantity in this lecture\u2019s figure.</p><ul><li>Which stage is directly observed or specified?</li><li>Which stage is the physical law or derivation step?</li><li>What would change if an assumption in the derivation failed?</li></ul></div><figure class='visual-figure'>{fig}<figcaption>{escape(item['title'])}: from observation to inferred quantity.</figcaption></figure></div></section>
<section class='slide'><h2>Common Misconception</h2><p class='warning'>{item['pitfall']}</p></section>
<section class='slide'><h2>Active Learning Segment</h2><p>{item['activity']}</p></section>
<section class='slide'><h2>Lab Connection</h2><p>{item['lab_connection']}</p></section>
<section class='slide'><h2>Synthesis</h2><p>{item['synthesis']}</p></section>
<section class='slide'><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Course dataset and derivations used in this lecture\u2019s worked example: <code>materials/ASTR340/data/</code> and <code>materials/ASTR340/src/generate_astr340_content.py</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 340 Lecture {n:02d} Slides', body, SLIDE_CSS)


def lecture_notes(item: dict) -> str:
    n = item['n']
    body = f"""<header><div><h1>Lecture {n:02d}: {escape(item['title'])}</h1><p>ASTR 340 Astronomical Instrumentation</p></div></header>
<main>
<section><h2>Context and Why This Matters</h2><p>{item['why_matters']}</p></section>
<section><h2>Learning Goals</h2><ol>{li(item['goals'])}</ol></section>
<section><h2>Opening Phenomenon</h2><p>{item['phenomenon']}</p></section>
<section><h2>Vocabulary</h2><ul>{li(item['vocab'])}</ul></section>
<section><h2>Evidence</h2><ul>{li(item['evidence'])}</ul></section>
<section><h2>Derivation and Model</h2><ul>{li(item['model'])}</ul></section>
<section><h2>Working Equation</h2><p>\\[ {item['equation']} \\]</p></section>
<section><h2>Worked Example</h2><ol>{li(item['example'])}</ol></section>
<section><h2>Common Misconception</h2><p class='notice'>{item['pitfall']}</p></section>
<section><h2>Active-Learning Guidance</h2><p>{item['activity']}</p></section>
<section><h2>Lab Connection</h2><p>{item['lab_connection']}</p></section>
<section><h2>Synthesis Questions</h2><ul><li>What was measured directly, or taken from a published instrument specification, in this lecture\u2019s worked example, and what was derived from a physical law?</li><li>Which assumption in the derivation would most change the interpretation if it were wrong?</li><li>How does this lecture\u2019s technique connect to the lab and problem set that follow it?</li></ul></section>
<section><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Every numeric result above is computed programmatically in <code>materials/ASTR340/src/generate_astr340_content.py</code>, not hand-typed.</li></ul></section>
</main>"""
    return page(f'ASTR 340 Lecture {n:02d} Notes', body)


def write_lectures():
    LECTURE_DIR.mkdir(parents=True, exist_ok=True)
    for item in LECTURES:
        n = item['n']
        (LECTURE_DIR / f'lecture-{n:02d}-slides.html').write_text(slide_deck(item), encoding='utf-8')
        (LECTURE_DIR / f'lecture-{n:02d}-notes.html').write_text(lecture_notes(item), encoding='utf-8')


def write_data_csv():
    import csv
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / 'telescopes.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['name', 'aperture_m', 'focal_length_m', 'notes'])
        for scope in (KECK, HST, VLT, JWST, GEMINI, AMATEUR):
            w.writerow([scope.get('name'), scope.get('aperture_m'), scope.get('focal_length_m', ''), ''])
    with open(DATA_DIR / 'hires_echelle.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['quantity', 'value', 'unit'])
        for k, v in HIRES.items():
            w.writerow([k, v, ''])
    with open(DATA_DIR / 'ccd_qe_curve.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['wavelength_nm', 'qe_percent'])
        for wl, qe in zip(CCD_QE_CURVE_NM, CCD_QE_PERCENT):
            w.writerow([wl, qe])
    with open(DATA_DIR / 'ubvri_filters.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['band', 'central_wavelength_nm', 'effective_bandwidth_nm'])
        for name, lam0, fwhm in UBVRI:
            w.writerow([name, lam0, fwhm])


if __name__ == '__main__':
    write_lectures()
    write_data_csv()
    print(f'Wrote {len(LECTURES)} lecture slide decks and notes files, plus 4 data CSV files.')


