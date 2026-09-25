"""Second-pass content generator for ASTR210.

Regenerates lecture slides/notes, labs, and problem sets (+ solutions +
assessment instructions) with lecture-specific, quantitatively grounded
content to meet the ASTR101/ASTR120 review-release quality floor.

This replaces the shallow, template-only output previously produced by
generate_astr210_package_fixed.py. Run with the project interpreter:
    python materials/ASTR210/src/generate_astr210_content.py
"""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURE_DIR = ROOT / 'lectures'
LAB_DIR = ROOT / 'labs'
PSET_DIR = ROOT / 'problem-sets'

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
# Lecture-figure SVGs are defined below, after the shared worked-example
# constants (see `diagram_svg` and the per-lecture `svg_XX` builders just
# above the LECTURES table). Each lecture gets a structurally distinct
# diagram built from a small set of shared drawing primitives.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Precomputed, verified quantities used across lectures/labs/problem sets
# ---------------------------------------------------------------------------

# Detector calibration (ties Lecture 1, Lecture 3, Lab 1) -- real Canon EOS M50
# master calibration frames, 2022-07-19 BackyardEOS/Astro Pixel Processor
# session (William Optics Zenithstar 73 + Flat73R reducer, Astronomik CLS clip
# filter), green (G1) Bayer channel, native 14-bit camera ADU. Source:
# 00Masters/MB-IG_400.0-E_2.5E-4s-...fits (bias, N=20) and
# MD-IG_400.0-E300.100006s-...fits (dark, N=4, 300.1 s exposure matching the
# night's 300 s light frames). BSCALE=4.000183 in the FITS pixel data was
# divided out; these are the header MEAN-G1/NOISE-G1 keyword values, already
# in native ADU.
BIAS, BIAS_ERR = 2047.6, 1.71
# The matched-exposure master dark already contains the bias pedestal (its
# mean, 2046.0 ADU, is statistically indistinguishable from the bias mean),
# so the calibration model subtracts the dark frame directly: I_cal = (raw - D) / F.
DARK, DARK_ERR = 2046.0, 1.32
# Patch 1 = "near top-left" 40x40 patch; Patch 3 = "center" 40x40 patch, both
# from LIGHT_300s_400iso_+31c_20220719-22h40m39s641ms.CR3, normalized against
# the same-session master flat (Lab 01 documents all five real patches).
P1_RAW, P1_FLAT = 2886, 0.96
P1_CAL = (P1_RAW - DARK) / P1_FLAT
P3_RAW, P3_FLAT = 3048, 1.09
P3_CAL = (P3_RAW - DARK) / P3_FLAT

# Airmass (Lecture 2)
ALT_DEG = 35.0
Z_DEG = 90.0 - ALT_DEG
AIRMASS = 1.0 / math.cos(math.radians(Z_DEG))
K_V = 0.15
EXTRA_MAG = K_V * AIRMASS

# SNR (Lecture 4)
S_BRIGHT, S_FAINT = 2500.0, 300.0
NPIX, SKY_E, DARK_E, READ_E = 9, 150.0, 5.0, 8.0
NOISE_TERM = NPIX * (SKY_E + DARK_E + READ_E ** 2)
SNR_BRIGHT = S_BRIGHT / math.sqrt(S_BRIGHT + NOISE_TERM)
SNR_FAINT = S_FAINT / math.sqrt(S_FAINT + NOISE_TERM)

# Photometric zero point (Lecture 5) -- from data/photometry_standard_stars.csv
STD_A = dict(counts=150000, exptime=30, mag=10.21)
STD_B = dict(counts=62000, exptime=30, mag=11.17)
STD_C = dict(counts=24000, exptime=30, mag=12.20)
RATE_A = STD_A['counts'] / STD_A['exptime']
ZP = STD_A['mag'] + 2.5 * math.log10(RATE_A)
RATE_B = STD_B['counts'] / STD_B['exptime']
MAG_B_PRED = -2.5 * math.log10(RATE_B) + ZP
RATE_C = STD_C['counts'] / STD_C['exptime']
MAG_C_PRED = -2.5 * math.log10(RATE_C) + ZP

# Differential photometry (Lecture 6) -- from data/variable_star_lightcurve.csv
DM_BASELINE = -2.5 * math.log10(0.995 / 1.000)
DM_DIP = -2.5 * math.log10(0.970 / 0.999)
DM_DEPTH = DM_DIP - DM_BASELINE

# Astrometry / plate scale (Lecture 7) -- from data/asteroid_astrometry.csv
DX_PIX = 534.7 - 520.3
DY_PIX = 415.8 - 411.2
PIX_SEP = math.hypot(DX_PIX, DY_PIX)
DEC_MEAN = math.radians((12.551 + 12.5521) / 2)
D_RA_DEG = (132.1021 - 132.0988) * math.cos(DEC_MEAN)
D_DEC_DEG = 12.5521 - 12.551
SKY_SEP_DEG = math.hypot(D_RA_DEG, D_DEC_DEG)
SKY_SEP_ARCSEC = SKY_SEP_DEG * 3600
PLATE_SCALE = SKY_SEP_ARCSEC / PIX_SEP

# Spectroscopy / resolution (Lecture 8)
R_RESOLUTION = 656.0 / 0.3

# Radial velocity multi-line check (Lecture 9) -- data/spectrum_lines.csv
C_KMS = 299792.458
LINES = [
    ('H\u03b1', 656.3, 656.9),
    ('H\u03b2', 486.1, 486.55),
    ('[O III]', 500.7, 501.16),
]
RV_RESULTS = [(name, (obs - rest) / rest * C_KMS) for name, rest, obs in LINES]
RV_MEAN = sum(v for _, v in RV_RESULTS) / len(RV_RESULTS)

# Archive parallax quality cut (Lecture 10) -- data/archive_query_sample.csv
PARALLAX_ROWS = [
    (1, 5.1, 0.2),
    (2, 1.2, 0.5),
    (3, 8.8, 0.1),
]
def _dist_pc(plx_mas):
    return 1000.0 / plx_mas

# Stacking (Lecture 11)
N_STACK = 9
SNR_GAIN = math.sqrt(N_STACK)
SNR_BEFORE, SNR_AFTER = 12.0, 12.0 * SNR_GAIN

# Time domain (Lecture 12)
ECLIPSE_HOURS = 2.1
NIGHTLY_CADENCE_HOURS = 24.0
GOOD_CADENCE_MIN = 20.0

# Uncertainty budget (Lecture 13)
SIGMA_ZP, SIGMA_M = 0.02, 0.015
SIGMA_TOTAL = math.sqrt(SIGMA_ZP ** 2 + SIGMA_M ** 2)


def fmt(x, nd=2):
    return f"{x:.{nd}f}"


# ---------------------------------------------------------------------------
# Shared SVG drawing primitives (axes, curves, points) used to assemble a
# structurally distinct diagram for each lecture below. No single shape or
# layout is reused across lectures; only these low-level primitives are
# shared, exactly as intended by the lecture-slide-authoring style guide.
# ---------------------------------------------------------------------------

FONT = "Segoe UI, sans-serif"


def _lin(v, vmin, vmax, a, b):
    if vmax == vmin:
        return (a + b) / 2
    return a + (v - vmin) / (vmax - vmin) * (b - a)


def _svg_open(n: int, title: str) -> str:
    return (
        f"<svg class='lecture-figure' data-lecture-figure='{n:02d}' viewBox='0 0 980 620' role='img' "
        f"aria-label='Lecture {n:02d} visual model: {escape(title)}'>"
        f"<rect width='980' height='620' fill='#fbfcfd'/>"
        f"<text x='34' y='40' font-size='23' fill='#102a43' font-family='{FONT}'>Lecture {n:02d}: {escape(title)}</text>"
        f"<defs><marker id='arrow{n:02d}' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto'>"
        f"<path d='M0,0 L10,5 L0,10 z' fill='#5b6773'/></marker></defs>"
    )


def _svg_close(caption: str) -> str:
    return f"<text x='34' y='602' font-size='16' fill='#5b6773' font-family='{FONT}'>{escape(caption)}</text></svg>"


def _axes(x0, y0, x1, y1, xlabel, ylabel):
    """x0,y0 = bottom-left pixel; x1,y1 = top-right pixel (y1 < y0)."""
    return (
        f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y1}' stroke='#5b6773' stroke-width='2'/>"
        f"<line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y0}' stroke='#5b6773' stroke-width='2'/>"
        f"<text x='{x0+(x1-x0)/2-70}' y='{y0+38}' font-size='15' fill='#5b6773' font-family='{FONT}'>{escape(xlabel)}</text>"
        f"<text x='{x0-52}' y='{y1+(y0-y1)/2}' font-size='15' fill='#5b6773' font-family='{FONT}' "
        f"transform='rotate(-90 {x0-52} {y1+(y0-y1)/2})'>{escape(ylabel)}</text>"
    )


def _polyline(pts, color='#0f6b78', width=3, dash=None):
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    dash_attr = f" stroke-dasharray='{dash}'" if dash else ''
    return f"<polyline points='{d}' fill='none' stroke='{color}' stroke-width='{width}'{dash_attr}/>"


def _dot(x, y, r=6, fill='#b87911', label=None, dx=8, dy=-8):
    out = f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{fill}'/>"
    if label:
        out += f"<text x='{x+dx:.1f}' y='{y+dy:.1f}' font-size='14' fill='#102a43' font-family='{FONT}'>{escape(label)}</text>"
    return out


def _box(x, y, w, h, fill, label, sub=None, text_color='#fff'):
    out = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='10' fill='{fill}'/>"
    out += f"<text x='{x+14}' y='{y+28}' font-size='17' fill='{text_color}' font-family='{FONT}'>{escape(label)}</text>"
    if sub:
        out += f"<text x='{x+14}' y='{y+52}' font-size='16' fill='{text_color}' font-family='{FONT}'>{escape(sub)}</text>"
    return out


# ---------------------------------------------------------------------------
# Lecture 1 -- calibration-frame diagram: real bias/dark/flat frames combine
# to correct the Lab 01 raw patch.
# ---------------------------------------------------------------------------

def svg_01(item) -> str:
    n = 1
    s = _svg_open(n, item['title'])
    tiles = [(60, 90, '#3a3f45', 'Bias frame', f'mean {fmt(BIAS,1)} ADU', 'speckle'),
             (60, 250, '#5a4632', 'Dark frame', f'mean {fmt(DARK,1)} ADU, hot pixels', 'hotpix'),
             (60, 410, None, 'Flat field', 'vignetted response map', 'gradient')]
    for (x, y, fill, label, sub, kind) in tiles:
        if kind == 'gradient':
            s += (f"<defs><radialGradient id='flatgrad' cx='50%' cy='50%' r='75%'>"
                  f"<stop offset='0%' stop-color='#0f6b78'/><stop offset='100%' stop-color='#c8dade'/>"
                  f"</radialGradient></defs>"
                  f"<rect x='{x}' y='{y}' width='230' height='130' rx='8' fill='url(#flatgrad)'/>")
        else:
            s += f"<rect x='{x}' y='{y}' width='230' height='130' rx='8' fill='{fill}'/>"
        if kind == 'speckle':
            for i in range(24):
                s += _dot(x + 12 + (i * 37) % 206, y + 16 + (i * 53) % 106, r=1.6, fill='#cfd8dd')
        if kind == 'hotpix':
            for i in range(10):
                s += _dot(x + 20 + (i * 61) % 200, y + 20 + (i * 41) % 100, r=2.6, fill='#ffce6b')
        s += f"<rect x='{x}' y='{y}' width='230' height='130' rx='8' fill='none' stroke='#102a43' stroke-width='1.5'/>"
        s += f"<text x='{x+10}' y='{y+150}' font-size='15' fill='#102a43' font-family='{FONT}'>{escape(label)}: {escape(sub)}</text>"
    s += _box(420, 235, 190, 90, '#eef3f5', 'Raw patch (top-left)', f'{P1_RAW} ADU', text_color='#102a43')
    s += f"<path d='M610 280 L700 280' stroke='#5b6773' stroke-width='5' marker-end='url(#arrow{n:02d})'/>"
    s += _box(700, 235, 230, 90, '#0f6b78', 'I_cal = (raw \u2212 D) / F', f'{fmt(P1_CAL,1)} ADU')
    s += _svg_close(f'Bias, dark, and flat frames from the 2022-07-19 session calibrate the {P1_RAW} ADU raw patch to {fmt(P1_CAL,1)} ADU.')
    return s


# ---------------------------------------------------------------------------
# Lecture 2 -- airmass vs altitude curve, with the planned target marked.
# ---------------------------------------------------------------------------

def svg_02(item) -> str:
    n = 2
    s = _svg_open(n, item['title'])
    x0, y0, x1, y1 = 110, 520, 900, 100
    s += _axes(x0, y0, x1, y1, 'altitude (degrees)', 'airmass X = sec z')
    pts = []
    for alt in range(10, 91, 2):
        z = math.radians(90 - alt)
        x_val = min(1 / math.cos(z), 6.0)
        px = _lin(alt, 10, 90, x0, x1)
        py = _lin(x_val, 0.9, 6.0, y0, y1)
        pts.append((px, py))
    s += _polyline(pts, color='#0f6b78', width=3)
    px = _lin(ALT_DEG, 10, 90, x0, x1)
    py = _lin(min(AIRMASS, 6.0), 0.9, 6.0, y0, y1)
    s += _dot(px, py, r=7, fill='#b87911', label=f'target: {ALT_DEG:.0f}\u00b0, X={fmt(AIRMASS,2)}', dx=10, dy=-10)
    s += f"<line x1='{px}' y1='{py}' x2='{px}' y2='{y0}' stroke='#b87911' stroke-width='1.5' stroke-dasharray='5,4'/>"
    s += (f"<text x='{x0+20}' y='{y1+40}' font-size='15' fill='#8a4b08' font-family='{FONT}'>"
          f"Extinction penalty: k \u00d7 X = {K_V:.2f} \u00d7 {fmt(AIRMASS,2)} = {fmt(EXTRA_MAG,2)} mag</text>")
    s += _svg_close(f'Airmass rises sharply below about 30\u00b0 altitude; the {ALT_DEG:.0f}\u00b0 target already costs {fmt(EXTRA_MAG,2)} mag of extinction.')
    return s


# ---------------------------------------------------------------------------
# Lecture 3 -- flat-field vignetting profile: response vs radial position,
# with the two real Lab 01 patches (top-left, center) marked on the curve.
# ---------------------------------------------------------------------------

def svg_03(item) -> str:
    n = 3
    s = _svg_open(n, item['title'])
    x0, y0, x1, y1 = 110, 520, 900, 120
    s += _axes(x0, y0, x1, y1, 'radial distance from frame center (px)', 'flat-field response F')
    r_p3, f_p3 = 40.0, P3_FLAT   # center patch: small radius
    r_p1, f_p1 = 340.0, P1_FLAT  # top-left patch: large radius
    pts = []
    for r in range(0, 361, 10):
        f_val = f_p3 + (f_p1 - f_p3) * (r / 360.0) ** 1.4
        px = _lin(r, 0, 360, x0, x1)
        py = _lin(f_val, 0.9, 1.15, y0, y1)
        pts.append((px, py))
    s += _polyline(pts, color='#0f6b78', width=3)
    s += _dot(_lin(r_p3, 0, 360, x0, x1), _lin(f_p3, 0.9, 1.15, y0, y1), fill='#102a43',
              label=f'center patch F={fmt(f_p3,2)}', dx=10, dy=-12)
    s += _dot(_lin(r_p1, 0, 360, x0, x1), _lin(f_p1, 0.9, 1.15, y0, y1), fill='#b87911',
              label=f'top-left patch F={fmt(f_p1,2)}', dx=-190, dy=-10)
    s += f"<line x1='{x0}' y1='{_lin(1.0,0.9,1.15,y0,y1)}' x2='{x1}' y2='{_lin(1.0,0.9,1.15,y0,y1)}' stroke='#5b6773' stroke-width='1' stroke-dasharray='4,4'/>"
    s += _svg_close('The reducer optics make the sensor center more sensitive than its corners: this is why a center-patch raw count is divided up (F>1) and a corner-patch count is divided down (F<1).')
    return s


# ---------------------------------------------------------------------------
# Lecture 4 -- SNR noise-budget bar chart for the bright vs faint source.
# ---------------------------------------------------------------------------

def svg_04(item) -> str:
    n = 4
    s = _svg_open(n, item['title'])
    x0, y0, x1, y1 = 110, 520, 900, 120
    s += _axes(x0, y0, x1, y1, 'source', 'electrons (e\u207b)')
    ymax = max(S_BRIGHT, S_FAINT, NOISE_TERM) * 1.15
    groups = [('Bright source', S_BRIGHT, SNR_BRIGHT, 260), ('Faint source', S_FAINT, SNR_FAINT, 620)]
    for label, signal, snr, cx in groups:
        bar_w = 90
        s_h = _lin(signal, 0, ymax, y0, y1)
        n_h = _lin(NOISE_TERM, 0, ymax, y0, y1)
        s += f"<rect x='{cx-100}' y='{s_h}' width='{bar_w}' height='{y0-s_h:.1f}' fill='#0f6b78'/>"
        s += f"<text x='{cx-95}' y='{s_h-8:.1f}' font-size='14' fill='#102a43' font-family='{FONT}'>S={signal:.0f} e\u207b</text>"
        s += f"<rect x='{cx+10}' y='{n_h}' width='{bar_w}' height='{y0-n_h:.1f}' fill='#b87911'/>"
        s += f"<text x='{cx+15}' y='{n_h-8:.1f}' font-size='14' fill='#102a43' font-family='{FONT}'>bkg={NOISE_TERM:.0f} e\u207b\u00b2</text>"
        s += f"<text x='{cx-95}' y='{y0+28}' font-size='16' fill='#102a43' font-family='{FONT}'>{escape(label)}</text>"
        s += f"<text x='{cx-95}' y='{y0+50}' font-size='16' fill='#0f6b78' font-family='{FONT}'>SNR = {fmt(snr,1)}</text>"
    s += _svg_close(f'Identical background/read noise ({NOISE_TERM:.0f} e\u207b\u00b2) combines in quadrature with source signal; only the bright source ({fmt(SNR_BRIGHT,1)}) clears a secure-detection threshold as easily as shown.')
    return s


# ---------------------------------------------------------------------------
# Lecture 5 -- aperture/sky-annulus schematic plus zero-point verification
# scatter (predicted vs catalog magnitude for the three standards).
# ---------------------------------------------------------------------------

def svg_05(item) -> str:
    n = 5
    s = _svg_open(n, item['title'])
    cx, cy = 240, 320
    s += f"<circle cx='{cx}' cy='{cy}' r='160' fill='#eef3f5' stroke='#d9e0e7'/>"
    s += f"<circle cx='{cx}' cy='{cy}' r='110' fill='none' stroke='#0f6b78' stroke-width='2' stroke-dasharray='6,4'/>"
    s += f"<circle cx='{cx}' cy='{cy}' r='38' fill='#b87911'/>"
    s += f"<text x='{cx-30}' y='{cy+60}' font-size='14' fill='#0f6b78' font-family='{FONT}'>sky annulus</text>"
    s += f"<text x='{cx-24}' y='{cy+5}' font-size='13' fill='#fff' font-family='{FONT}'>aperture</text>"
    x0, y0, x1, y1 = 520, 520, 900, 140
    s += _axes(x0, y0, x1, y1, 'catalog V (mag)', 'predicted V (mag)')
    mmin, mmax = 9.8, 12.6
    s += _polyline([(_lin(mmin, mmin, mmax, x0, x1), _lin(mmin, mmin, mmax, y0, y1)),
                    (_lin(mmax, mmin, mmax, x0, x1), _lin(mmax, mmin, mmax, y0, y1))],
                   color='#5b6773', width=1, dash='4,4')
    checks = [('A (defines ZP)', STD_A['mag'], STD_A['mag']),
              ('B', STD_B['mag'], MAG_B_PRED),
              ('C', STD_C['mag'], MAG_C_PRED)]
    for label, cat, pred in checks:
        px = _lin(cat, mmin, mmax, x0, x1)
        py = _lin(pred, mmin, mmax, y0, y1)
        s += _dot(px, py, fill='#102a43', label=f'STD-{label}', dx=8, dy=-8)
    s += _svg_close(f'STD-B and STD-C, held out of the zero-point fit, land on the 1:1 line to within a few millimagnitudes -- confirming ZP={fmt(ZP,3)} is internally consistent.')
    return s


# ---------------------------------------------------------------------------
# Lecture 6 -- differential light curve for target and comparison star.
# ---------------------------------------------------------------------------

def svg_06(item) -> str:
    n = 6
    s = _svg_open(n, item['title'])
    x0, y0, x1, y1 = 120, 500, 900, 140
    s += _axes(x0, y0, x1, y1, 'time (fraction of night)', 'normalized flux')
    tgt = [(0.00, 0.995), (0.04, 0.985), (0.07, 0.974), (0.10, 0.970), (0.13, 0.982), (0.17, 0.994)]
    comp = [(0.00, 1.000), (0.04, 1.000), (0.07, 0.999), (0.10, 0.999), (0.13, 1.000), (0.17, 1.000)]
    fmin, fmax = 0.96, 1.005
    s += _polyline([(_lin(t, 0, 0.17, x0, x1), _lin(f, fmin, fmax, y0, y1)) for t, f in comp], color='#b87911', width=2, dash='5,3')
    s += _polyline([(_lin(t, 0, 0.17, x0, x1), _lin(f, fmin, fmax, y0, y1)) for t, f in tgt], color='#0f6b78', width=3)
    s += _dot(_lin(0.00, 0, 0.17, x0, x1), _lin(0.995, fmin, fmax, y0, y1), fill='#0f6b78', label='target, t=0.00')
    s += _dot(_lin(0.10, 0, 0.17, x0, x1), _lin(0.970, fmin, fmax, y0, y1), fill='#0f6b78', label='target, t=0.10 (dip)', dy=18)
    s += _dot(_lin(0.00, 0, 0.17, x0, x1), _lin(1.000, fmin, fmax, y0, y1), fill='#b87911', label='comparison')
    s += _svg_close(f'The comparison star stays flat within 0.2% while the target dips: \u0394m grows from {fmt(DM_BASELINE,3)} to {fmt(DM_DIP,3)} mag, a {fmt(DM_DEPTH,3)}-mag dip.')
    return s


# ---------------------------------------------------------------------------
# Lecture 7 -- astrometric pixel-plane vector plus matched sky-plane shift.
# ---------------------------------------------------------------------------

def svg_07(item) -> str:
    n = 7
    s = _svg_open(n, item['title'])
    s += f"<text x='90' y='110' font-size='16' fill='#102a43' font-family='{FONT}'>Pixel plane</text>"
    ox, oy = 90, 140
    for i in range(6):
        for j in range(5):
            s += _dot(ox + i * 55, oy + j * 55, r=1.6, fill='#d9e0e7')
    p1x, p1y = ox + (520.3 - 500) * 0.9, oy + (411.2 - 400) * 0.9
    p2x, p2y = ox + (534.7 - 500) * 0.9, oy + (415.8 - 400) * 0.9
    s += _dot(p1x, p1y, fill='#0f6b78', label='image 1 (520.3, 411.2)', dx=-10, dy=-14)
    s += _dot(p2x, p2y, fill='#b87911', label='image 2 (534.7, 415.8)', dx=8, dy=22)
    s += f"<path d='M{p1x:.1f} {p1y:.1f} L{p2x:.1f} {p2y:.1f}' stroke='#5b6773' stroke-width='3' marker-end='url(#arrow{n:02d})'/>"
    s += (f"<text x='90' y='430' font-size='15' fill='#102a43' font-family='{FONT}'>"
          f"\u0394pixel = {fmt(PIX_SEP,2)} px</text>")
    s += f"<text x='560' y='110' font-size='16' fill='#102a43' font-family='{FONT}'>Sky plane (RA, Dec)</text>"
    sx, sy = 620, 140
    for i in range(6):
        for j in range(5):
            s += _dot(sx + i * 55, sy + j * 55, r=1.6, fill='#d9e0e7')
    q1x, q1y = sx + 240, sy + 140
    q2x, q2y = q1x - (DX_PIX * 6), q1y + (DY_PIX * 6)
    s += _dot(q1x, q1y, fill='#0f6b78', label='(132.1021\u00b0, 12.5510\u00b0)', dx=-190, dy=-14)
    s += _dot(q2x, q2y, fill='#b87911', label='(132.0988\u00b0, 12.5521\u00b0)', dx=8, dy=22)
    s += f"<path d='M{q1x:.1f} {q1y:.1f} L{q2x:.1f} {q2y:.1f}' stroke='#5b6773' stroke-width='3' marker-end='url(#arrow{n:02d})'/>"
    s += (f"<text x='620' y='430' font-size='15' fill='#102a43' font-family='{FONT}'>"
          f"\u0394sky = {fmt(SKY_SEP_ARCSEC,2)} arcsec</text>")
    s += _svg_close(f'Plate scale = \u0394sky/\u0394pixel = {fmt(PLATE_SCALE,3)} arcsec/pixel, derived from the same asteroid-track pair used in the worked example.')
    return s


# ---------------------------------------------------------------------------
# Lecture 8 -- pixel-to-wavelength dispersion solution with a resolution
# inset comparing a barely resolved pair to a trivially resolved pair.
# ---------------------------------------------------------------------------

def svg_08(item) -> str:
    n = 8
    s = _svg_open(n, item['title'])
    x0, y0, x1, y1 = 110, 340, 560, 120
    s += _axes(x0, y0, x1, y1, 'pixel column', 'wavelength (nm)')
    pmin, pmax = 0, 1024
    lmin, lmax = 400, 700
    s += _polyline([(_lin(pmin, pmin, pmax, x0, x1), _lin(lmin, lmin, lmax, y0, y1)),
                    (_lin(pmax, pmin, pmax, x0, x1), _lin(lmax, lmin, lmax, y0, y1))], color='#0f6b78', width=3)
    s += _dot(_lin(512, pmin, pmax, x0, x1), _lin(656.3, lmin, lmax, y0, y1), fill='#b87911',
              label='pixel 512 \u2192 656.3 nm', dx=-150, dy=-12)
    s += f"<text x='110' y='90' font-size='16' fill='#102a43' font-family='{FONT}'>Wavelength solution (arc lamp fit)</text>"
    s += f"<text x='610' y='90' font-size='16' fill='#102a43' font-family='{FONT}'>Resolving power R\u2248{R_RESOLUTION:.0f}</text>"
    ax0, ay = 610, 220
    for lam, lab, blend in [(656.3, 'H\u03b1', False), (656.5, 'unresolved neighbor', True)]:
        px = ax0 + (lam - 656.0) * 900
        s += f"<line x1='{px:.1f}' y1='{ay-20}' x2='{px:.1f}' y2='{ay+20}' stroke='#0f6b78' stroke-width='4'/>"
        s += f"<text x='{px-30:.1f}' y='{ay+42}' font-size='12' fill='#102a43' font-family='{FONT}'>{escape(lab)}</text>"
    s += f"<text x='610' y='{ay+80}' font-size='14' fill='#8a4b08' font-family='{FONT}'>0.3 nm apart: blend into one feature</text>"
    ay2 = 380
    for lam, lab in [(656.3, 'H\u03b1'), (486.1, 'H\u03b2')]:
        px = ax0 + (lam - 400) * 0.9
        s += f"<line x1='{px:.1f}' y1='{ay2-20}' x2='{px:.1f}' y2='{ay2+20}' stroke='#0f6b78' stroke-width='4'/>"
        s += f"<text x='{px-15:.1f}' y='{ay2+42}' font-size='12' fill='#102a43' font-family='{FONT}'>{escape(lab)}</text>"
    s += f"<text x='610' y='{ay2+80}' font-size='14' fill='#0f6b78' font-family='{FONT}'>170 nm apart: trivially resolved</text>"
    s += _svg_close(f'A linear pixel-to-wavelength fit anchors pixel 512 at 656.3 nm; at R\u2248{R_RESOLUTION:.0f} a 0.3 nm pair blends but H\u03b1/H\u03b2 (170 nm apart) never do.')
    return s


# ---------------------------------------------------------------------------
# Lecture 9 -- Doppler shift tick-mark diagram for three independent lines.
# ---------------------------------------------------------------------------

def svg_09(item) -> str:
    n = 9
    s = _svg_open(n, item['title'])
    x0, y0, x1, y1 = 140, 500, 900, 110
    s += _axes(x0, y0, x1, y1, 'wavelength (nm)', '')
    lmin, lmax = 480, 505
    rows = [(90, LINES[0]), (250, LINES[1]), (410, LINES[2])]
    for (rowy, (name, rest, obs)) in rows:
        lmin_r, lmax_r = rest - 3, rest + 3
        rx = 140
        s += f"<text x='{rx-70}' y='{rowy+6}' font-size='15' fill='#102a43' font-family='{FONT}'>{escape(name)}</text>"
        px_rest = _lin(rest, lmin_r, lmax_r, rx, rx + 700)
        px_obs = _lin(obs, lmin_r, lmax_r, rx, rx + 700)
        s += f"<line x1='{rx}' y1='{rowy}' x2='{rx+700}' y2='{rowy}' stroke='#d9e0e7' stroke-width='2'/>"
        s += f"<line x1='{px_rest:.1f}' y1='{rowy-16}' x2='{px_rest:.1f}' y2='{rowy+16}' stroke='#5b6773' stroke-width='3'/>"
        s += f"<line x1='{px_obs:.1f}' y1='{rowy-16}' x2='{px_obs:.1f}' y2='{rowy+16}' stroke='#b87911' stroke-width='3'/>"
        s += f"<path d='M{px_rest:.1f} {rowy} L{px_obs:.1f} {rowy}' stroke='#0f6b78' stroke-width='2' marker-end='url(#arrow{n:02d})'/>"
        v = (obs - rest) / rest * C_KMS
        s += f"<text x='{px_obs+10:.1f}' y='{rowy-20}' font-size='13' fill='#0f6b78' font-family='{FONT}'>v={v:.0f} km/s</text>"
    s += f"<text x='140' y='500' font-size='12' fill='#5b6773' font-family='{FONT}'>gray tick = rest wavelength; gold tick = observed wavelength</text>"
    s += _svg_close(f'Three unrelated lines (H\u03b1, H\u03b2, [O III]) all shift redward and agree on v\u2248{fmt(RV_MEAN,1)} km/s -- evidence of one genuine bulk velocity, not a line-specific artifact.')
    return s


# ---------------------------------------------------------------------------
# Lecture 10 -- parallax quality-cut scatter plot.
# ---------------------------------------------------------------------------

def svg_10(item) -> str:
    n = 10
    s = _svg_open(n, item['title'])
    x0, y0, x1, y1 = 130, 500, 900, 130
    s += _axes(x0, y0, x1, y1, 'parallax (mas)', 'parallax / error')
    pmin, pmax = 0, 10
    rmin, rmax = 0, 45
    cut_y = _lin(5, rmin, rmax, y0, y1)
    s += f"<line x1='{x0}' y1='{cut_y:.1f}' x2='{x1}' y2='{cut_y:.1f}' stroke='#8a4b08' stroke-width='2' stroke-dasharray='6,4'/>"
    s += f"<text x='{x1-190}' y='{cut_y-8:.1f}' font-size='14' fill='#8a4b08' font-family='{FONT}'>quality cut: ratio &gt; 5</text>"
    for sid, plx, err in PARALLAX_ROWS:
        ratio = plx / err
        color = '#0f6b78' if ratio > 5 else '#8a4b08'
        px = _lin(plx, pmin, pmax, x0, x1)
        py = _lin(min(ratio, rmax), rmin, rmax, y0, y1)
        s += _dot(px, py, r=8, fill=color, label=f'src {sid}: d={_dist_pc(plx):.1f} pc' + ('' if ratio > 5 else ' (fails cut)'), dx=10, dy=-10)
    s += _svg_close('Sources 1 and 3 clear a parallax/error > 5 cut and get trustworthy distances; Source 2 fails the cut and must be flagged, not silently inverted.')
    return s


# ---------------------------------------------------------------------------
# Lecture 11 -- sqrt(N) stacking-gain curve plus a mean-vs-median outlier bar.
# ---------------------------------------------------------------------------

def svg_11(item) -> str:
    n = 11
    s = _svg_open(n, item['title'])
    x0, y0, x1, y1 = 110, 500, 560, 140
    s += _axes(x0, y0, x1, y1, 'number of stacked frames N', 'SNR gain factor \u221aN')
    pts = []
    for nn in range(1, 17):
        px = _lin(nn, 1, 16, x0, x1)
        py = _lin(math.sqrt(nn), 1, 4, y0, y1)
        pts.append((px, py))
    s += _polyline(pts, color='#0f6b78', width=3)
    s += _dot(_lin(N_STACK, 1, 16, x0, x1), _lin(SNR_GAIN, 1, 4, y0, y1), fill='#b87911',
              label=f'N={N_STACK}: \u221aN={fmt(SNR_GAIN,2)}, SNR {SNR_BEFORE:.0f}\u2192{fmt(SNR_AFTER,1)}', dx=-260, dy=-14)
    bx0, by0 = 640, 500
    spike = 5000.0
    mean_add = spike / N_STACK
    s += f"<text x='{bx0}' y='140' font-size='15' fill='#102a43' font-family='{FONT}'>Cosmic-ray robustness (1 of {N_STACK} frames spiked)</text>"
    s += f"<rect x='{bx0}' y='{by0-40}' width='90' height='40' fill='#8a4b08'/>"
    s += f"<text x='{bx0}' y='{by0+20}' font-size='14' fill='#102a43' font-family='{FONT}'>mean: +{mean_add:.0f} ADU bias</text>"
    s += f"<rect x='{bx0+140}' y='{by0-6}' width='90' height='6' fill='#0f6b78'/>"
    s += f"<text x='{bx0+140}' y='{by0+20}' font-size='14' fill='#102a43' font-family='{FONT}'>median: unaffected</text>"
    s += _svg_close(f'Stacking N={N_STACK} registered frames gains \u221a{N_STACK}={fmt(SNR_GAIN,2)}\u00d7 in SNR, but only a median combine resists a single-frame cosmic-ray spike.')
    return s


# ---------------------------------------------------------------------------
# Lecture 12 -- two-panel cadence comparison (nightly vs fine sampling of the
# same eclipse).
# ---------------------------------------------------------------------------

def svg_12(item) -> str:
    n = 12
    s = _svg_open(n, item['title'])
    dip_center, half_width = 2.0, ECLIPSE_HOURS / 2
    def dip_flux(t):
        if abs(t - dip_center) > half_width:
            return 1.0
        return 1.0 - 0.03 * math.cos((t - dip_center) / half_width * math.pi / 2) ** 2

    def panel(x0, y0, x1, y1, cadence_hours, label, color):
        s2 = _axes(x0, y0, x1, y1, 'time (hours)', 'flux')
        curve = [(_lin(t, 0, 4, x0, x1), _lin(dip_flux(t), 0.96, 1.01, y0, y1)) for t in [i * 0.05 for i in range(81)]]
        s2 += _polyline(curve, color='#d9e0e7', width=2)
        t = 0.0
        while t <= 4.0001:
            s2 += _dot(_lin(t, 0, 4, x0, x1), _lin(dip_flux(t), 0.96, 1.01, y0, y1), r=5, fill=color)
            t += cadence_hours
        s2 += f"<text x='{x0}' y='{y1-14}' font-size='15' fill='#102a43' font-family='{FONT}'>{escape(label)}</text>"
        return s2
    s += panel(110, 300, 460, 120, NIGHTLY_CADENCE_HOURS, f'Nightly cadence ({NIGHTLY_CADENCE_HOURS:.0f} h): event essentially unsampled', '#8a4b08')
    s += panel(560, 300, 900, 120, GOOD_CADENCE_MIN / 60, f'{GOOD_CADENCE_MIN:.0f}-min cadence: dip fully resolved', '#0f6b78')
    s += _svg_close(f'The same {ECLIPSE_HOURS:.1f}-hour dip is invisible at a {NIGHTLY_CADENCE_HOURS:.0f}-hour cadence but well resolved at {GOOD_CADENCE_MIN:.0f}-minute cadence.')
    return s


# ---------------------------------------------------------------------------
# Lecture 13 -- quadrature error-budget right triangle.
# ---------------------------------------------------------------------------

def svg_13(item) -> str:
    n = 13
    s = _svg_open(n, item['title'])
    ox, oy = 200, 500
    scale = 4000
    leg1 = SIGMA_ZP * scale
    leg2 = SIGMA_M * scale
    hyp_x, hyp_y = ox + leg1, oy - leg2
    s += f"<path d='M{ox} {oy} L{ox+leg1:.1f} {oy} L{hyp_x:.1f} {hyp_y:.1f} Z' fill='#eef3f5' stroke='#102a43' stroke-width='2'/>"
    s += f"<text x='{ox+leg1/2-60:.1f}' y='{oy+30}' font-size='16' fill='#102a43' font-family='{FONT}'>\u03c3_ZP = {SIGMA_ZP:.2f} mag</text>"
    s += f"<text x='{ox+leg1+14:.1f}' y='{oy-leg2/2:.1f}' font-size='16' fill='#102a43' font-family='{FONT}'>\u03c3_m = {SIGMA_M:.3f} mag</text>"
    s += f"<text x='{ox+leg1/2-70:.1f}' y='{oy-leg2/2-14:.1f}' font-size='16' fill='#0f6b78' font-family='{FONT}'>\u03c3_total = {fmt(SIGMA_TOTAL,3)} mag</text>"
    s += f"<rect x='{ox+leg1-16:.1f}' y='{oy-16}' width='16' height='16' fill='none' stroke='#102a43'/>"
    s += _svg_close(f'Independent uncertainties add in quadrature, not linearly: \u221a({SIGMA_ZP:.2f}\u00b2+{SIGMA_M:.3f}\u00b2) = {fmt(SIGMA_TOTAL,3)} mag, not {SIGMA_ZP+SIGMA_M:.3f} mag.')
    return s


# ---------------------------------------------------------------------------
# Lecture 14 -- vertical report-anatomy outline, each section quoting the
# exact worked-example sentence it corresponds to.
# ---------------------------------------------------------------------------

def svg_14(item) -> str:
    n = 14
    s = _svg_open(n, item['title'])
    sections = [('Methods', item['example'][0], '#0f6b78'),
                ('Results', item['example'][1], '#102a43'),
                ('Limitations', item['example'][2], '#b87911')]
    y = 90
    for label, quote, color in sections:
        s += f"<rect x='90' y='{y}' width='800' height='120' rx='10' fill='{color}' opacity='.92'/>"
        s += f"<text x='110' y='{y+30}' font-size='18' fill='#fff' font-family='{FONT}'>{escape(label)}</text>"
        clean = quote.strip('"')
        wrapped = clean if len(clean) < 110 else clean[:107] + '...'
        s += f"<text x='110' y='{y+62}' font-size='14' fill='#fff' font-family='{FONT}'>{escape(wrapped)}</text>"
        if y > 90:
            s += f"<path d='M490 {y-30} L490 {y}' stroke='#5b6773' stroke-width='3' marker-end='url(#arrow{n:02d})'/>"
        y += 150
    s += _svg_close('Every claim in Results and Limitations traces back to a specific, checkable calculation from an earlier lecture -- that traceability is what makes the report defensible.')
    return s


_DIAGRAM_FUNCS = {1: svg_01, 2: svg_02, 3: svg_03, 4: svg_04, 5: svg_05, 6: svg_06, 7: svg_07,
                   8: svg_08, 9: svg_09, 10: svg_10, 11: svg_11, 12: svg_12, 13: svg_13, 14: svg_14}


def diagram_svg(item: dict) -> str:
    return _DIAGRAM_FUNCS[item['n']](item)


# Per-lecture visual-reasoning prompt text and figure caption, matched to the
# structurally distinct diagram assembled above (not a generic recolored
# flow-chart question set).
VISUAL_PROMPTS = {
    1: ('Study how the three real calibration frames combine to correct the raw patch.',
        ['Why does the flat field divide rather than subtract?',
         'What would change in the calibrated value if the dark frame were mismatched in exposure length?'],
        'The measurement chain from raw detector frames to a calibrated patch value.'),
    2: ('Read the airmass curve to see why altitude choice dominates an observing plan.',
        ['Why does the curve steepen so quickly below 30\u00b0 altitude?',
         'How much flux is lost to extinction at the marked target altitude?'],
        'Airmass versus altitude, with the planned target and its extinction penalty marked.'),
    3: ('Trace the vignetting profile from sensor center to edge.',
        ['Why is the center patch divided by a flat value above 1, and the corner patch by a value below 1?',
         'What would a flat taken through a different filter do to this curve?'],
        'Flat-field response as a function of radial distance, with the two real Lab 01 patches marked.'),
    4: ('Compare the noise budgets of the bright and faint source.',
        ['Why does the faint source have a much lower SNR despite an identical background term?',
         'What happens to each bar if the aperture (n_pix) is enlarged?'],
        'Signal and background-noise terms for the bright and faint sources, with their resulting SNR.'),
    5: ('Use the aperture/annulus schematic and the zero-point check together.',
        ['Why must the sky annulus be placed outside the source aperture?',
         'What would it mean if STD-B or STD-C fell far off the 1:1 line?'],
        'Aperture and sky-annulus geometry, plus the zero-point verification against two independent standards.'),
    6: ('Read the light curve for the target and comparison star together, not separately.',
        ['Why is the comparison star\u2019s flat line essential to trusting the target\u2019s dip?',
         'What differential-magnitude value corresponds to the deepest point of the dip?'],
        'Target and comparison-star flux over the night, with the real dip highlighted.'),
    7: ('Compare the pixel-plane vector to the matched sky-plane vector.',
        ['Why must both vectors correspond to the same physical displacement?',
         'What would a mismatch between the two vector lengths imply about the plate solution?'],
        'The measured pixel displacement and its matched sky-coordinate displacement.'),
    8: ('Use the dispersion line and resolution inset together.',
        ['Why do the two 0.3 nm-separated lines blend while H\u03b1 and H\u03b2 do not?',
         'What would a steeper or shallower dispersion line do to the resolving power at fixed pixel resolution?'],
        'Pixel-to-wavelength dispersion solution, with a resolved and an unresolved line pair compared.'),
    9: ('Compare the three independent line shifts.',
        ['Why does agreement across H\u03b1, H\u03b2, and [O III] strengthen the case for a real bulk velocity?',
         'What pattern would you expect if one line were contaminated by a blend?'],
        'Rest and observed positions for three independent lines, with each implied velocity labeled.'),
    10: ('Use the quality-cut line to judge each archive source.',
         ['Why does Source 2 fail the cut despite having a measured parallax?',
          'What happens to the inferred distance if you ignore the cut and invert Source 2\u2019s parallax anyway?'],
         'Parallax-to-error ratio for three archive sources, with the quality-cut threshold marked.'),
    11: ('Read the stacking-gain curve alongside the cosmic-ray comparison.',
         ['Why does the SNR gain grow more slowly as N increases?',
          'Why does a median combine resist the single spiked frame while a mean combine does not?'],
         'SNR gain from stacking N frames, plus a comparison of mean and median combination under a cosmic-ray spike.'),
    12: ('Compare the two sampling panels of the same event.',
         ['Why is the nightly-cadence panel unable to show the dip shape at all?',
          'How many samples fall inside the dip in the fine-cadence panel?'],
         'The same eclipse sampled at a nightly cadence versus a fine cadence.'),
    13: ('Read the uncertainty triangle as a vector sum, not a simple addition.',
         ['Why is \u03c3_total smaller than \u03c3_ZP + \u03c3_m?',
          'Which leg of the triangle dominates the final uncertainty here?'],
         'Zero-point and measurement uncertainties combined in quadrature into a total reported uncertainty.'),
    14: ('Trace each report section back to the calculation it depends on.',
         ['Which earlier lecture does the Results-section claim depend on?',
          'What would you add to the Limitations section if the comparison star\u2019s long-term stability were unverified?'],
         'The methods-results-limitations anatomy of the technical observing report, quoting the term\u2019s own calculations.'),
}


# ---------------------------------------------------------------------------
# Lecture content table
# ---------------------------------------------------------------------------
# Each entry defines the substantive content for one 15-slide deck and its
# paired notes document: goals, historical/why-matters framing, phenomenon,
# vocabulary, evidence, model claims, a quantitative tool with a worked
# example computed above, a visual-reasoning prompt, a misconception, an
# active-learning prompt, a lab connection, a synthesis, and an exact
# OpenStax Astronomy 2e chapter/section anchor.

LECTURES = [
    dict(
        n=1, title='From Pretty Pictures to Measurements',
        subtitle='Observation, calibration, and inference',
        goals=[
            'State why a raw astronomical image is not yet a measurement.',
            'Identify the additive (bias, dark current) and multiplicative (flat field) corrections that convert counts into a defensible signal.',
            'Propagate a simple calibration-frame uncertainty and report a result with units and an error bar.',
        ],
        why_matters='Photographic plates gave way to CCDs and CMOS sensors in the late 20th century because they are linear and reproducible, but linearity only helps if the observer removes the detector\u2019s own signature from every pixel. A "pretty picture" straight off the camera mixes source light with bias voltage, thermal electrons, and pixel-to-pixel sensitivity variations; none of those artifacts are physically part of the object being observed. This lecture uses a real amateur imaging session (Canon EOS M50 on a William Optics Zenithstar 73 refractor, captured with BackyardEOS and calibrated in Astro Pixel Processor) so every number below is a measured quantity, not a hypothetical one.',
        phenomenon='On the night of 2022-07-19, a 300 s light frame of a galaxy field (LIGHT_300s_400iso_+31c_20220719-22h40m39s641ms.CR3) records raw pixel values around 2,900\u20133,100 ADU in ordinary background regions \u2014 far above zero, yet the camera has not been pointed at anything bright there. Only after subtracting a matched calibration frame and dividing by a flat field can that number be compared to a catalog or to a different night\u2019s data.',
        vocab=['ADU (analog-to-digital unit)', 'bias frame', 'dark current', 'flat field', 'gain', 'calibration frame', 'provenance'],
        evidence=[
            'A master bias built from 20 stacked zero-length-equivalent exposures shows a stable mean level of about 2,048 ADU with only a 1.7\u20132.2 ADU pixel-to-pixel scatter \u2014 this offset is present in every exposure regardless of light.',
            'A master dark built from four 300.1 s exposures (matching the night\u2019s 300 s light frames) has a mean level (2,046 ADU) statistically indistinguishable from the bias mean, but its pixel-to-pixel scatter (about 27 ADU) is roughly 15 times larger \u2014 revealing that at this ISO and exposure length, dark "noise" is dominated by scattered hot pixels, not a uniform thermal rise.',
            'A master flat from 19 twilight-sky exposures is not uniform in the raw data: its normalized response varies by several percent from the frame center to the edges (vignetting) and differs noticeably between color channels because of the camera\u2019s narrowband light-pollution clip filter.',
        ],
        model=[
            'The calibration model is additive-then-multiplicative: subtract a bias-and-dark term first, then divide by a normalized flat field.',
            'When a master dark is captured at the same exposure length as the science frames (as it is here), it already contains the bias pedestal, so a single dark-frame subtraction replaces a separate bias-then-dark subtraction.',
            'Each calibration frame carries its own uncertainty, and that uncertainty propagates into the corrected science measurement.',
            'A measurement without a stated calibration history and uncertainty is not reproducible and should not be treated as a scientific result.',
        ],
        equation=r'I_{\rm cal} = \dfrac{I_{\rm raw} - D}{F}',
        example=[
            f'A raw 40\u00d740 pixel patch near the top-left of the frame records {P1_RAW} ADU (mean).',
            f'The matched-exposure master dark level is D = {fmt(DARK,1)} \u00b1 {fmt(DARK_ERR,2)} ADU (already including the bias pedestal, whose own level is B = {fmt(BIAS,1)} \u00b1 {fmt(BIAS_ERR,2)} ADU for comparison).',
            f'The normalized flat-field response at this patch is F = {fmt(P1_FLAT,2)}.',
            f'Corrected signal: I_cal = ({P1_RAW} \u2212 {fmt(DARK,1)}) / {fmt(P1_FLAT,2)} = {fmt(P1_CAL,1)} ADU.',
            
            'This is real diffuse sky-background-plus-source signal above the calibration floor, not sensor noise \u2014 the dominant remaining uncertainty is photon (shot) statistics, developed in Lecture 4.',
        ],
        pitfall='Treating the raw pixel value as the physical brightness of the source. A brighter raw number can result from a warmer detector or a more sensitive pixel, not a brighter star.',
        activity='In pairs, take the printed raw-count table from Lab 01 and calibrate two of the five real patches by hand before checking your arithmetic against a neighbor\u2019s.',
        lab_connection='Lab 01 (Detector Calibration) requires calibrating five real aperture patches from this same imaging session using this exact dark/flat model and reporting the least-certain step.',
        synthesis='A defensible astronomical measurement is a corrected number with an uncertainty and a documented calibration history \u2014 not the number the detector happened to display.',
        openstax='OpenStax Astronomy 2e, Chapter 1.3 (the nature of scientific measurement) and Chapter 6.3 (visible-light detectors and instruments).',
    ),
    dict(
        n=2, title='Observing Planning and Error Budgets',
        subtitle='Turning a science goal into an executable observing plan',
        goals=[
            'Compute airmass from altitude and estimate the resulting extinction penalty.',
            'Identify the planning decisions (target altitude, exposure time, calibration cadence) that dominate a night\u2019s success.',
            'Distinguish a planning error from a reduction error in a failed observation.',
        ],
        why_matters='Telescope time is scarce and expensive, and a plan built without an error budget fails quietly: the data come back, but they cannot answer the question that was asked. Professional proposals are reviewed partly on whether the requested exposure times and target altitudes are realistic.',
        phenomenon=f'A target visible at only {ALT_DEG:.0f}\u00b0 altitude looks like a fine plan on a star chart, but the light must pass through {fmt(AIRMASS,2)} times as much atmosphere as it would at the zenith, dimming the source by roughly {fmt(EXTRA_MAG,2)} magnitudes before it even reaches the detector.',
        vocab=['airmass', 'zenith angle', 'extinction coefficient', 'exposure time', 'overhead', 'calibration cadence', 'observing window'],
        evidence=[
            'Standard-star measurements repeated across an night at different altitudes show systematically fainter magnitudes at low altitude even though the star has not changed.',
            'Exposure-time calculators show diminishing returns: doubling exposure time only improves signal-to-noise by about 40% because noise grows with the square root of the signal.',
            'Missing a bias, dark, or flat calibration sequence cannot be repaired after the night ends, unlike a slightly short exposure.',
        ],
        model=[
            'Airmass X approximates sec(z), where z is the zenith angle; X = 1 at the zenith and grows quickly below about 30\u00b0 altitude.',
            'An extinction coefficient k (mag per airmass) converts airmass into a predictable magnitude penalty, k·X.',
            'A complete observing plan allocates time not only to the science target but to calibration frames, standard stars, and overheads.',
        ],
        equation=r'X \approx \sec z = \dfrac{1}{\cos z}, \qquad \Delta m_{\rm ext} = k\,X',
        example=[
            f'A target is at altitude {ALT_DEG:.0f}\u00b0, so the zenith angle is z = 90\u00b0 \u2212 {ALT_DEG:.0f}\u00b0 = {Z_DEG:.0f}\u00b0.',
            f'Airmass: X = 1/cos({Z_DEG:.0f}\u00b0) = {fmt(AIRMASS,2)}.',
            f'Using a typical V-band extinction coefficient k = {K_V:.2f} mag/airmass, the extra dimming is {K_V:.2f} \u00d7 {fmt(AIRMASS,2)} = {fmt(EXTRA_MAG,2)} mag relative to the zenith.',
            'A 0.26-magnitude penalty is a roughly 24% flux loss \u2014 large enough to change whether a faint target is detectable at all.',
        ],
        pitfall='Choosing an exposure time based only on the target\u2019s catalog brightness, ignoring sky brightness, airmass, and detector read noise, all of which change the achievable signal-to-noise.',
        activity='Given a target rising through the night, plot airmass versus time and identify the observing window where airmass stays below 2.0.',
        lab_connection='Lab 01 opens with a short planning checklist before any calibration arithmetic begins, so a bad plan is caught before data are "collected."',
        synthesis='Planning is the first stage of data reduction: a technically achievable exposure at the wrong altitude, or without calibration frames, cannot be rescued afterward.',
        openstax='OpenStax Astronomy 2e, Chapter 4.1 (Earth and sky, altitude/azimuth coordinates) and Chapter 6.1\u20136.2 (telescopes and observing constraints).',
    ),
    dict(
        n=3, title='CCD Detectors, Bias, Dark, and Flat Fields',
        subtitle='What a modern detector actually records',
        goals=[
            'Explain the physical origin of bias, dark current, and flat-field variations in a CCD.',
            'Apply the full calibration equation to a second, independent worked example.',
            'Distinguish additive corrections from multiplicative corrections.',
        ],
        why_matters='A CCD or CMOS sensor converts photons into electrons with high linearity, which is why it replaced photographic plates, but every pixel adds its own small, systematic offset and its own sensitivity. Understanding these effects at the hardware level explains why calibration frames must be taken on the same night, with the same instrument setup, as the science frames \u2014 exactly as Lecture 1\u2019s Canon EOS M50 example did.',
        phenomenon='A galaxy image taken with a dirty or scratched filter shows a faint ring pattern (dust donuts) that has nothing to do with the galaxy. The same instrumental pattern appears, identically, in a flat-field exposure of blank twilight sky.',
        vocab=['bias frame', 'dark current', 'flat field', 'quantum efficiency', 'vignetting', 'read noise', 'linearity'],
        evidence=[
            'The Lecture 1 master bias (20 stacked frames) gives a stable mean of about 2,048 ADU with a small (1.7\u20132.2 ADU) scatter, independent of exposure time.',
            'The matched-exposure master dark shows almost no mean-level rise above the bias (2,046 vs. 2,048 ADU) at this ISO, but a roughly 15-fold increase in pixel-to-pixel scatter, confirming that scattered hot pixels, not a uniform thermal current, dominate this camera\u2019s dark signal at moderate exposure lengths.',
            'The master flat is systematically brighter near the frame center and dimmer at the edges (vignetting from the reducer optics) and differs by a large factor between color channels because the Astronomik CLS clip filter suppresses the red channel\u2019s throughput far more than green or blue.',
        ],
        model=[
            'Bias and dark current are additive detector signals; when the master dark is captured at the same exposure length as the light frames, a single dark-frame subtraction removes both at once.',
            'The flat field is a normalized (mean-value-one) map of relative sensitivity; dividing by it removes multiplicative structure without changing the overall brightness scale.',
            'The corrected count I_cal in ADU (or electrons, once converted by the detector gain) is the quantity that should be compared across nights, instruments, and catalogs.',
        ],
        equation=r'I_{\rm cal} = \dfrac{I_{\rm raw} - D}{F}',
        example=[
            f'A second real patch (the "center" patch in Lab 01) records {P3_RAW} raw ADU with flat value F = {fmt(P3_FLAT,2)}.',
            f'Using the same matched-exposure master dark D = {fmt(DARK,1)} ADU as Lecture 1: corrected signal = ({P3_RAW} \u2212 {fmt(DARK,1)}) / {fmt(P3_FLAT,2)} = {fmt(P3_CAL,1)} ADU.',
            f'Note that the center patch has a higher flat value (F = {fmt(P3_FLAT,2)} > 1) than the top-left patch (F = {fmt(P1_FLAT,2)} < 1), consistent with the vignetting pattern: the sensor center is more sensitive than its corners, so a center-patch raw count is divided up rather than down to match the true source brightness.',
        ],
        pitfall='Using a flat field taken through a different filter, at a different focus, or on a different night than the science frames. Flats are only valid for the exact optical configuration that produced them.',
        activity='Sketch, without numbers, how a bias frame, a dark frame, and a flat frame would each look if photographed directly, and explain which corrections are additive and which are multiplicative.',
        lab_connection='Lab 01 requires completing the calibration table for all five real aperture patches, including the two shown here as worked examples plus three left for the student.',
        synthesis='Calibration turns raw detector counts into a defensible measurement by separating what the detector adds (bias, dark) from what it scales (flat field).',
        openstax='OpenStax Astronomy 2e, Chapter 6.3 (visible-light detectors and instruments, CCDs).',
    ),
    dict(
        n=4, title='Noise, Signal-to-Noise, and Detection Limits',
        subtitle='Detection is a probability statement',
        goals=[
            'Write the CCD signal-to-noise equation including source, sky, dark, and read-noise terms.',
            'Compute SNR for a bright and a faint source using identical instrumental conditions.',
            'State the SNR threshold conventionally used to claim a secure detection.',
        ],
        why_matters='A faint source is not simply "a star you cannot quite see"; it is a source whose signal sits among several independent noise sources. Whether a signal counts as a detection is a statistical judgment, not a visual impression, and that judgment depends on the noise model, not just the raw counts.',
        phenomenon=f'Two sources produce very different counts on the same field with an identical 3\u00d73 pixel aperture: one at {S_BRIGHT:.0f} electrons, one at only {S_FAINT:.0f} electrons. Both sit on the same sky background and read noise, but only one is a secure detection.',
        vocab=['Poisson noise', 'sky background', 'read noise', 'dark current (SNR term)', 'aperture', 'detection threshold', 'shot noise'],
        evidence=[
            'Repeated measurements of the same faint source scatter by an amount consistent with the square root of the total counts (Poisson statistics), not a fixed absolute error.',
            'Increasing the aperture size to include more sky pixels increases the noise term even when it does not increase the captured source signal.',
            'A source with SNR near 3 appears in some exposures and not others of the same field \u2014 exactly the behavior expected of a marginal detection.',
        ],
        model=[
            'Random noise sources (source shot noise, sky shot noise, dark current shot noise, and read noise) combine in quadrature, not by simple addition.',
            'SNR above about 5 is conventionally treated as a secure detection; SNR between about 3 and 5 is marginal and requires independent confirmation.',
            'A quoted flux without an SNR or an aperture specification cannot be evaluated for reliability.',
        ],
        equation=r'{\rm SNR} = \dfrac{S}{\sqrt{S + n_{\rm pix}\,(B_{\rm sky} + D + R^2)}}',
        example=[
            f'Aperture has n_pix = {NPIX} pixels; sky background B = {SKY_E:.0f} e\u207b/pix, dark D = {DARK_E:.0f} e\u207b/pix, read noise R = {READ_E:.0f} e\u207b (R\u00b2 = {READ_E**2:.0f}).',
            f'Noise term per pixel-summed background: n_pix \u00d7 (B + D + R\u00b2) = {NPIX} \u00d7 ({SKY_E:.0f} + {DARK_E:.0f} + {READ_E**2:.0f}) = {NOISE_TERM:.0f} e\u207b\u00b2.',
            f'Bright source (S = {S_BRIGHT:.0f} e\u207b): SNR = {S_BRIGHT:.0f} / \u221a({S_BRIGHT:.0f} + {NOISE_TERM:.0f}) = {S_BRIGHT:.0f} / {math.sqrt(S_BRIGHT+NOISE_TERM):.2f} = {fmt(SNR_BRIGHT,1)} \u2014 a secure detection.',
            f'Faint source (S = {S_FAINT:.0f} e\u207b): SNR = {S_FAINT:.0f} / \u221a({S_FAINT:.0f} + {NOISE_TERM:.0f}) = {S_FAINT:.0f} / {math.sqrt(S_FAINT+NOISE_TERM):.2f} = {fmt(SNR_FAINT,1)} \u2014 marginal; still above 5 but close enough that a single frame should not be over-interpreted.',
        ],
        pitfall='Equating "visible in the displayed image" with "securely detected." Image display stretches can make an SNR-3 fluctuation look identical to an SNR-30 source.',
        activity='Recompute the faint-source SNR after doubling the exposure time (S and background terms both double) and explain why SNR improves by less than a factor of two.',
        lab_connection='Lab 02 (Signal-to-Noise Budget) requires computing SNR for several source/background combinations and identifying which are secure detections.',
        synthesis='Detection is a probability statement built from a noise model, not merely a visual impression of the displayed image.',
        openstax='OpenStax Astronomy 2e, Chapter 6.3 (detectors) and Chapter 17.1 (the brightness of stars).',
    ),
    dict(
        n=5, title='Aperture Photometry',
        subtitle='Measurement design as much as calculation',
        goals=[
            'Define instrumental magnitude and photometric zero point.',
            'Derive a zero point from one standard star and verify it against two others.',
            'Explain how aperture and sky-annulus choice bias a photometric measurement.',
        ],
        why_matters='Aperture photometry converts pixel counts into a calibrated brightness, but the same star can yield different reported magnitudes depending on aperture radius, sky-annulus placement, and how carefully the zero point was derived. Photometry is a measurement-design problem, not only an arithmetic one.',
        phenomenon='A photometric pipeline processes three standard stars in the same field and filter. If the zero point derived from one star is correct, it should reproduce the catalog magnitudes of the other two without further adjustment.',
        vocab=['instrumental magnitude', 'zero point', 'aperture radius', 'sky annulus', 'count rate', 'photometric standard', 'curve of growth'],
        evidence=[
            f'STD-A: {STD_A["counts"]} counts in a {STD_A["exptime"]} s exposure, catalog V = {STD_A["mag"]}.',
            f'STD-B: {STD_B["counts"]} counts in {STD_B["exptime"]} s, catalog V = {STD_B["mag"]}.',
            f'STD-C: {STD_C["counts"]} counts in {STD_C["exptime"]} s, catalog V = {STD_C["mag"]}.',
        ],
        model=[
            'Instrumental magnitude is defined from a count rate (counts per second), not raw counts, so exposures of different length can be compared.',
            'The zero point ZP absorbs the telescope aperture, filter throughput, and detector sensitivity into one number for a given night and setup.',
            'A zero point derived from a single well-measured standard should reproduce the catalog magnitudes of independent standards if the calibration is internally consistent.',
        ],
        equation=r'm = -2.5\log_{10}(\text{rate}) + {\rm ZP}',
        example=[
            f'STD-A count rate = {STD_A["counts"]}/{STD_A["exptime"]} = {RATE_A:.1f} counts/s.',
            f'Solve for the zero point using the catalog magnitude: ZP = {STD_A["mag"]} + 2.5\u00d7log10({RATE_A:.1f}) = {STD_A["mag"]} + {2.5*math.log10(RATE_A):.3f} = {fmt(ZP,3)}.',
            f'Apply ZP to STD-B: rate = {RATE_B:.1f} counts/s, predicted m = \u22122.5\u00d7log10({RATE_B:.1f}) + {fmt(ZP,3)} = {fmt(MAG_B_PRED,3)} (catalog: {STD_B["mag"]}) \u2014 agreement to about {abs(MAG_B_PRED-STD_B["mag"])*1000:.0f} millimagnitudes.',
            f'Apply ZP to STD-C: rate = {RATE_C:.1f} counts/s, predicted m = \u22122.5\u00d7log10({RATE_C:.1f}) + {fmt(ZP,3)} = {fmt(MAG_C_PRED,3)} (catalog: {STD_C["mag"]}) \u2014 agreement to about {abs(MAG_C_PRED-STD_C["mag"])*1000:.0f} millimagnitudes.',
            'Because both independent checks reproduce the catalog values to a few millimagnitudes, this zero point is internally consistent and can be applied to the unknown target in the same field.',
        ],
        pitfall='Choosing an aperture radius too small (losing source flux to the wings of the point-spread function) or too large (including excess sky noise), then blaming the resulting magnitude error on "bad seeing" rather than measurement design.',
        activity='Using the STD-A-derived zero point above, predict the magnitude of a fourth star with 38,000 counts in 30 s, then discuss what would make you distrust the prediction.',
        lab_connection='Lab 03 (Aperture Photometry) uses this exact standard-star table to derive and verify a zero point, then applies it to an unknown target.',
        synthesis='Photometry is a measurement-design problem: aperture size, sky annulus, and zero-point derivation all shape the final calibrated brightness.',
        openstax='OpenStax Astronomy 2e, Chapter 17.1 (the brightness of stars, magnitudes).',
    ),
    dict(
        n=6, title='Differential Photometry and Light Curves',
        subtitle='Removing common-mode effects to reveal relative variability',
        goals=[
            'Define differential magnitude and explain why it cancels shared atmospheric and instrumental effects.',
            'Compute a light-curve dip depth from real flux ratios.',
            'Identify a poor choice of comparison star.',
        ],
        why_matters='Variable-star and exoplanet-transit science rarely needs an absolute magnitude; it needs a precise relative measurement between a target and a stable comparison star in the same field, observed at the same time and airmass. Differential photometry removes clouds, seeing changes, and airmass drifts that affect both stars equally.',
        phenomenon='A light curve of target and comparison-star fluxes over one night shows a shallow dip in the target relative to the comparison, while the comparison star alone stays flat within measurement noise.',
        vocab=['comparison star', 'differential magnitude', 'common-mode noise', 'light curve', 'transit depth', 'baseline', 'ensemble photometry'],
        evidence=[
            'At t = 0.00 (start of the sequence): target flux = 0.995, comparison flux = 1.000 (both normalized).',
            'At t = 0.10: target flux = 0.970, comparison flux = 0.999 \u2014 the comparison star barely moved while the target dropped noticeably.',
            'The comparison star\u2019s flux stays within about 0.2% of 1.000 throughout, confirming it is not itself variable.',
        ],
        model=[
            'Differential magnitude \u0394m = \u22122.5 log10(F_target / F_comp) removes atmospheric and instrumental effects common to both stars.',
            'A genuine astrophysical dip shows up as a change in the target-to-comparison ratio, not merely a change in either star\u2019s raw flux.',
            'The comparison star must be checked for its own stability before being trusted; an unstable comparison star creates a false signal in the target.',
        ],
        equation=r'\Delta m = -2.5\log_{10}\!\left(\dfrac{F_{\rm target}}{F_{\rm comp}}\right)',
        example=[
            f'Baseline (t = 0.00): \u0394m = \u22122.5\u00d7log10(0.995/1.000) = {fmt(DM_BASELINE,4)} mag.',
            f'During the dip (t = 0.10): \u0394m = \u22122.5\u00d7log10(0.970/0.999) = {fmt(DM_DIP,4)} mag.',
            f'Dip depth relative to baseline: {fmt(DM_DIP,4)} \u2212 ({fmt(DM_BASELINE,4)}) = {fmt(DM_DEPTH,4)} mag \u2248 {DM_DEPTH*1000:.0f} millimagnitudes.',
            'A dip of this size (about 2.5\u20133% relative flux change) is comparable to a hot-Jupiter transit depth around a Sun-like star, which is why differential photometry at the millimagnitude level is central to transit science.',
        ],
        pitfall='Choosing a comparison star that is itself variable, blended with a neighbor, or near saturation \u2014 any of these injects a false signal into the "constant" reference and corrupts the differential light curve.',
        activity='Given a table of target and comparison fluxes at five times, compute \u0394m at each time and decide whether the pattern is a real dip or measurement scatter.',
        lab_connection='Lab 04 (Differential Light Curve) uses the full variable-star flux table to build a light curve and test whether an observed dip exceeds the noise floor.',
        synthesis='Differential photometry reveals relative variability by removing common-mode effects that would otherwise swamp a small, real signal.',
        openstax='OpenStax Astronomy 2e, Chapter 17.1 (brightness and magnitudes) and Chapter 21.4 (evidence for planets from transits).',
    ),
    dict(
        n=7, title='Astrometry and Plate Solutions',
        subtitle='Geometry plus calibration plus residual analysis',
        goals=[
            'Explain how a plate solution links pixel coordinates to sky coordinates.',
            'Derive a plate scale from two matched image/catalog coordinate pairs.',
            'State what residual analysis after a plate solution tells you about systematic error.',
        ],
        why_matters='Pixels become right ascension and declination only after an image is matched to a reference catalog through a plate solution (World Coordinate System). Astrometry underlies proper motions, orbit determination for asteroids and comets, and the reference frames used for every other kind of positional measurement.',
        phenomenon='An asteroid imaged twice, minutes apart, shifts noticeably in pixel coordinates. Converting that pixel shift into an angular sky motion requires knowing the plate scale (arcseconds per pixel), which is itself derived from the same data.',
        vocab=['centroid', 'plate scale', 'World Coordinate System (WCS)', 'astrometric residual', 'proper motion', 'reference catalog', 'pixel-to-sky transformation'],
        evidence=[
            f'Image 1: (x, y) = (520.3, 411.2) px corresponds to (RA, Dec) = (132.1021\u00b0, 12.5510\u00b0).',
            f'Image 2, taken shortly after: (x, y) = (534.7, 415.8) px corresponds to (RA, Dec) = (132.0988\u00b0, 12.5521\u00b0).',
            'The pixel shift and the sky-coordinate shift both scale together, which is exactly the relationship a plate solution is built to capture.',
        ],
        model=[
            'A plate solution is a geometric transformation, calibrated using catalog stars, from pixel coordinates to sky coordinates.',
            'Plate scale (arcsec/pixel) converts a measured pixel displacement into a physically meaningful angular displacement.',
            'A believable astrometric position always comes with a residual: the leftover scatter between predicted and catalog positions of the calibration stars.',
        ],
        equation=r'\text{plate scale} = \dfrac{\Delta(\text{sky separation, arcsec})}{\Delta(\text{pixel separation, px})}',
        example=[
            f'Pixel displacement: \u0394x = {DX_PIX:.1f} px, \u0394y = {DY_PIX:.1f} px, so the total pixel separation is \u221a({DX_PIX:.1f}\u00b2 + {DY_PIX:.1f}\u00b2) = {fmt(PIX_SEP,2)} px.',
            f'Sky displacement: \u0394RA\u00b7cos(Dec) = {D_RA_DEG*3600:.3f} arcsec, \u0394Dec = {D_DEC_DEG*3600:.3f} arcsec, so the total angular separation is {fmt(SKY_SEP_ARCSEC,2)} arcsec.',
            f'Plate scale = {fmt(SKY_SEP_ARCSEC,2)} arcsec / {fmt(PIX_SEP,2)} px = {fmt(PLATE_SCALE,3)} arcsec/pixel.',
            'This plate scale, once derived, can be applied to any other pixel measurement on the same image without re-deriving it from scratch \u2014 but only if the optical setup has not changed.',
        ],
        pitfall='Treating a measured centroid as the final position without asking about the plate-solution residual. A centroid can be very precise (small statistical uncertainty) yet still biased by an uncorrected optical distortion.',
        activity='Given a third image/catalog coordinate pair, check whether it predicts the same plate scale derived above to within about 5%, and discuss what a large discrepancy would imply.',
        lab_connection='Lab 05 (Astrometry and Motion) extends this two-point plate-scale derivation to a full three-image asteroid track and asks for a proper-motion estimate.',
        synthesis='Astrometry is geometry plus calibration plus residual analysis \u2014 a plate scale is only as good as the consistency check that follows it.',
        openstax='OpenStax Astronomy 2e, Chapter 19.2 (surveying the stars, parallax and astrometric fundamentals).',
    ),
    dict(
        n=8, title='Spectroscopy and Wavelength Calibration',
        subtitle='Turning a dispersed image into a scientific measurement',
        goals=[
            'Explain why an arc-lamp exposure is required before a stellar spectrum can be interpreted.',
            'Compute spectral resolving power R = \u03bb/\u0394\u03bb and relate it to line separation.',
            'Identify which spectral features can and cannot be resolved at a given R.',
        ],
        why_matters='A spectrum is only a scientific measurement once its horizontal axis has been mapped from pixel position to wavelength using a known calibration source (an arc lamp with well-documented emission lines). Without that step, a spectrum is just a picture of a rainbow.',
        phenomenon='A raw spectral image shows a source trace crossed by a set of bright calibration lines from a companion arc-lamp exposure. Matching those lines to a reference list is what converts "pixel column 512" into "656.3 nanometers."',
        vocab=['dispersion', 'arc lamp', 'wavelength solution', 'resolving power', 'line list', 'spectral order', 'continuum'],
        evidence=[
            'An arc-lamp spectrum shows several bright, sharp emission lines at well-documented laboratory wavelengths.',
            'Fitting a polynomial to (pixel position, known wavelength) pairs from the arc lamp gives a wavelength solution that can be applied to the adjacent science spectrum.',
            'Two spectral lines separated by less than about one resolution element blend into a single broadened feature rather than appearing as two distinct peaks.',
        ],
        model=[
            'Resolving power R = \u03bb/\u0394\u03bb quantifies how finely a spectrograph can separate two nearby wavelengths.',
            'A wavelength solution derived from arc-lamp lines must be checked for residual scatter before being trusted on science data.',
            'Line identification requires both an accurate wavelength solution and a reference list of expected transitions for the object type being studied.',
        ],
        equation=r'R = \dfrac{\lambda}{\Delta\lambda}',
        example=[
            f'A spectrograph has a measured resolution element of \u0394\u03bb = 0.3 nm near \u03bb = 656.0 nm (the H\u03b1 region).',
            f'Resolving power: R = 656.0 / 0.3 \u2248 {R_RESOLUTION:.0f}.',
            'At R \u2248 2200, two lines separated by less than about 0.3 nm will blend; H\u03b1 (656.3 nm) and a hypothetical line at 656.5 nm would not be cleanly separated, but H\u03b1 and H\u03b2 (486.1 nm), separated by over 170 nm, are trivially resolved.',
            'This matters directly for the next lecture: measuring a Doppler shift of order 0.5\u20130.6 nm requires a resolution element several times smaller than the shift itself, which R \u2248 2200 comfortably provides.',
        ],
        pitfall='Measuring a line\u2019s pixel position and reporting a "wavelength" without ever taking or applying an arc-lamp calibration exposure from the same instrumental configuration.',
        activity='Given a short table of arc-lamp pixel positions and known wavelengths, fit a straight line by hand (two-point slope) and predict the wavelength of a science-target absorption line at a specified pixel.',
        lab_connection='Lab 06 (Spectroscopic Wavelength Calibration) requires deriving a wavelength solution from arc-lamp data before measuring any target line shifts.',
        synthesis='Spectral calibration is what turns a dispersed image into a scientific measurement; resolving power sets the limit on what can be told apart.',
        openstax='OpenStax Astronomy 2e, Chapter 5.3 (spectroscopy in astronomy).',
    ),
    dict(
        n=9, title='Radial Velocity and Redshift',
        subtitle='Velocity from calibrated wavelength shifts',
        goals=[
            'Apply the non-relativistic Doppler formula to measure radial velocity from a wavelength shift.',
            'Cross-check a velocity measurement using multiple independent spectral lines.',
            'Explain why line blends or calibration drift can masquerade as a velocity signal.',
        ],
        why_matters='The Doppler shift is one of the most productive tools in observational astronomy: it reveals orbital motion in binary stars, radial velocities in exoplanet detection, and cosmological redshift in distant galaxies. Its reliability depends entirely on the wavelength calibration developed in the previous lecture.',
        phenomenon='Three lines in the same spectrum \u2014 H\u03b1, H\u03b2, and [O III] \u2014 are all shifted redward of their laboratory wavelengths. If the shift is a genuine bulk radial velocity, all three lines should imply the same velocity.',
        vocab=['rest wavelength', 'observed wavelength', 'redshift', 'blueshift', 'radial velocity', 'line blend', 'systemic velocity'],
        evidence=[
            f'H\u03b1: rest {LINES[0][1]} nm, observed {LINES[0][2]} nm.',
            f'H\u03b2: rest {LINES[1][1]} nm, observed {LINES[1][2]} nm.',
            f'[O III]: rest {LINES[2][1]} nm, observed {LINES[2][2]} nm.',
        ],
        model=[
            'For velocities much less than the speed of light, v/c \u2248 \u0394\u03bb/\u03bb\u2080, with positive \u0394\u03bb (redshift) meaning recession.',
            'A genuine bulk-motion signal produces a consistent velocity across multiple, unrelated spectral lines.',
            'A velocity estimate from a single line is far less trustworthy than one confirmed by several lines of different species.',
        ],
        equation=r'\dfrac{v}{c} \approx \dfrac{\Delta\lambda}{\lambda_0}',
        example=(
            [f'{name}: \u0394\u03bb = {obs-rest:.2f} nm, \u03bb\u2080 = {rest} nm, v = ({obs-rest:.2f}/{rest})\u00d7{C_KMS:.0f} km/s = {v:.1f} km/s.'
             for name, (label, rest, obs), (name2, v) in zip((l[0] for l in LINES), LINES, RV_RESULTS)]
            + [f'All three independent lines agree to within about {max(abs(v-RV_MEAN) for _, v in RV_RESULTS):.1f} km/s of the mean, v \u2248 {fmt(RV_MEAN,1)} km/s \u2014 strong evidence for a genuine, single bulk radial velocity rather than a line-specific artifact.']
        ),
        pitfall='Ascribing an observed wavelength shift to physical velocity without checking for calibration drift, line blending with a neighboring feature, or an error in identifying which transition produced the line.',
        activity='Given a fourth line with rest wavelength 434.0 nm, predict its observed wavelength if the source has the same radial velocity found above, then discuss what a large discrepancy from that prediction would suggest.',
        lab_connection='Lab 06 continues into a multi-line radial-velocity determination using the wavelength solution derived earlier in the same lab.',
        synthesis='Velocity comes from calibrated wavelength shifts confirmed across multiple lines, not from the visual appearance of a single shifted feature.',
        openstax='OpenStax Astronomy 2e, Chapter 5.6 (the Doppler effect).',
    ),
    dict(
        n=10, title='Survey Archives and Reproducible Queries',
        subtitle='The query record is part of the scientific result',
        goals=[
            'Explain why a catalog query is a scientific decision, not a neutral data pull.',
            'Apply a parallax signal-to-noise cut and justify the threshold.',
            'Compute distances from parallax for a small archive sample.',
        ],
        why_matters='Modern astronomy runs on public catalogs (Gaia, SDSS, and similar surveys), where the scientifically interesting sample is defined by the cuts applied to it, not simply by what the archive returns. Two astronomers using different, undocumented cuts on the same catalog can reach different conclusions from identical raw data.',
        phenomenon='A three-row archive excerpt reports parallaxes with very different fractional uncertainties. Naively inverting every parallax to get a distance produces one wildly unreliable value hiding among two good ones.',
        vocab=['parallax', 'fractional parallax error', 'selection function', 'query reproducibility', 'catalog flag', 'completeness', 'contamination'],
        evidence=[f'Source {sid}: parallax = {plx} mas, uncertainty = {err} mas (fractional error = {err/plx*100:.0f}%).' for sid, plx, err in PARALLAX_ROWS],
        model=[
            'A parallax measurement is only useful for a distance estimate when its fractional uncertainty is small (a common cut is requiring parallax/error > 5).',
            'Distance in parsecs is the reciprocal of parallax in arcseconds; a poorly measured parallax produces a wildly uncertain, potentially unphysical, distance.',
            'A reproducible query documents every cut applied (magnitude limits, parallax quality, flags) so another astronomer could recover the same sample.',
        ],
        equation=r'd\,({\rm pc}) = \dfrac{1}{\pi\,(\text{arcsec})} = \dfrac{1000}{\pi\,({\rm mas})}',
        example=[
            f'Source 1: parallax/error = {PARALLAX_ROWS[0][1]/PARALLAX_ROWS[0][2]:.1f} (passes a >5 cut); distance = 1000/{PARALLAX_ROWS[0][1]} = {_dist_pc(PARALLAX_ROWS[0][1]):.1f} pc.',
            f'Source 2: parallax/error = {PARALLAX_ROWS[1][1]/PARALLAX_ROWS[1][2]:.1f} (fails a >5 cut); a naive distance of {_dist_pc(PARALLAX_ROWS[1][1]):.1f} pc should not be trusted and this source should be flagged or excluded.',
            f'Source 3: parallax/error = {PARALLAX_ROWS[2][1]/PARALLAX_ROWS[2][2]:.1f} (passes easily); distance = 1000/{PARALLAX_ROWS[2][1]} = {_dist_pc(PARALLAX_ROWS[2][1]):.1f} pc.',
            'Applying a uniform parallax/error > 5 cut removes Source 2 from any distance-based analysis while keeping Sources 1 and 3 \u2014 exactly the kind of documented decision a reproducible query record must state explicitly.',
        ],
        pitfall='Reporting "the archive returned N objects" without stating the magnitude limits, quality flags, and parallax-quality cuts that produced that number \u2014 the sample cannot be reproduced or critiqued without them.',
        activity='Given two additional archive rows, decide which pass a parallax/error > 5 cut and compute distances only for those that do.',
        lab_connection='Lab 07 (Archive Query Reproducibility) requires writing out the exact cuts applied to a larger sample and reporting how many sources each cut removes.',
        synthesis='Archive science requires the query record to be as carefully documented as the scientific interpretation that follows it.',
        openstax='OpenStax Astronomy 2e, Chapter 19.2 (surveying the stars, parallax) and general survey-data practice.',
    ),
    dict(
        n=11, title='Image Stacking, Registration, and Cosmic Rays',
        subtitle='Stacking is a statistical operation, not magic noise removal',
        goals=[
            'Explain how signal-to-noise improves with the number of stacked, independent exposures.',
            'Compare median and mean combination for robustness to cosmic-ray hits.',
            'State the registration requirement that must be satisfied before stacking is valid.',
        ],
        why_matters='Deep imaging and faint-source detection depend on combining many exposures, but stacking only improves a measurement if the images are registered to a common coordinate system and the noise in each frame is independent. Careless stacking can inject artifacts rather than removing them.',
        phenomenon=f'A single {ECLIPSE_HOURS:.0f}-hour-old exposure gives SNR = {SNR_BEFORE:.0f} for a faint source \u2014 barely a secure detection. Combining {N_STACK} such exposures, taken under similar conditions, should improve the detection significantly if the images are well registered.',
        vocab=['image registration', 'median combine', 'sigma-clipping', 'cosmic ray', 'independent noise', 'stack depth', 'outlier rejection'],
        evidence=[
            'A cosmic-ray strike appears as a single, very bright pixel in exactly one frame of a stack and nowhere else \u2014 it is not reproduced across exposures the way real astrophysical signal is.',
            'Stacking without first aligning (registering) the frames to a common pixel grid blurs point sources and can create false extended structure.',
            'A simple mean combine is pulled toward the cosmic-ray value in the affected pixel; a median combine of nine frames is essentially unaffected by one outlier.',
        ],
        model=[
            'If per-frame noise is independent and Gaussian, stacking N frames improves SNR by \u221aN relative to a single frame.',
            'Median combination (or sigma-clipped mean) is far more robust to single-frame outliers like cosmic rays than a simple arithmetic mean.',
            'Registration (aligning frames to a common World Coordinate System or pixel grid) must happen before combination, not after.',
        ],
        equation=r'{\rm SNR}_{\rm stack} \approx \sqrt{N}\,\times\,{\rm SNR}_{\rm single}',
        example=[
            f'Single-frame SNR = {SNR_BEFORE:.0f}; stacking N = {N_STACK} independent, registered frames gives an expected improvement factor of \u221a{N_STACK} = {fmt(SNR_GAIN,2)}.',
            f'Stacked SNR \u2248 {SNR_BEFORE:.0f} \u00d7 {fmt(SNR_GAIN,2)} = {fmt(SNR_AFTER,1)} \u2014 a marginal detection becomes a secure one.',
            'If one of the nine frames contains a 5000-count cosmic-ray spike in the target pixel, a simple mean combine adds roughly 5000/9 \u2248 556 counts of spurious signal to that pixel, while a median combine of nine values is essentially untouched by the single spike.',
        ],
        pitfall='Assuming that stacking automatically removes artifacts. Stacking only removes random, independent noise; it does not remove a systematic error (like an uncorrected flat field) present in every frame, and a naive mean combine does not remove cosmic rays.',
        activity='Given nine simulated per-frame values for one pixel, one of which is a clear outlier, compute both the mean and median and discuss which combination method a careful reduction pipeline should use.',
        lab_connection='This unit is assessed through Problem Set 06 rather than a dedicated lab, using simulated per-frame values that mirror this worked example.',
        synthesis='Stacking is a statistical operation that trades exposure count for signal-to-noise; it rewards careful registration and is easily defeated by sloppy combination methods.',
        openstax='OpenStax Astronomy 2e, Chapter 6.3 (detectors, CCD imaging).',
    ),
    dict(
        n=12, title='Time-Domain Observing',
        subtitle='Cadence must match the timescale of the phenomenon',
        goals=[
            'State the Nyquist-style sampling requirement for recovering a periodic or transient signal.',
            'Evaluate whether a given cadence can resolve a specific event duration.',
            'Explain the difference between undersampling and aliasing.',
        ],
        why_matters='Time-domain astronomy asks not only what an object is, but how it changes with time \u2014 and the answer depends entirely on whether the observing cadence matches the timescale of the phenomenon. A real signal can be completely invisible, or badly misrepresented, if the sampling is too coarse.',
        phenomenon=f'A transiting source produces a dip lasting about {ECLIPSE_HOURS:.1f} hours. One observer images the field once per night ({NIGHTLY_CADENCE_HOURS:.0f}-hour cadence); another images it every {GOOD_CADENCE_MIN:.0f} minutes during the predicted event window.',
        vocab=['cadence', 'sampling interval', 'aliasing', 'undersampling', 'ingress/egress', 'period', 'duty cycle'],
        evidence=[
            f'A once-per-night cadence ({NIGHTLY_CADENCE_HOURS:.0f} hours) is roughly {NIGHTLY_CADENCE_HOURS/ECLIPSE_HOURS:.0f} times coarser than the {ECLIPSE_HOURS:.1f}-hour event, so the event is essentially invisible in that dataset.',
            f'A {GOOD_CADENCE_MIN:.0f}-minute cadence during the event window gives roughly {ECLIPSE_HOURS*60/GOOD_CADENCE_MIN:.0f} samples across the dip, enough to resolve ingress, the flat bottom, and egress.',
            'A periodic signal sampled at close to its own period can appear to be constant or slowly varying even though it is rapidly changing \u2014 classic aliasing.',
        ],
        model=[
            'To recover the shape of an event of duration T, the sampling interval should be a small fraction of T, not merely shorter than the total observing run.',
            'Sparse, evenly spaced sampling of a periodic signal can alias to a spuriously long or short apparent period.',
            'Cadence, exposure time, and total baseline are three separate observing-design choices, each driven by a different aspect of the science goal.',
        ],
        equation=r'\Delta t_{\rm cadence} \ll T_{\rm event}',
        example=[
            f'Event duration T = {ECLIPSE_HOURS:.1f} hours.',
            f'Nightly cadence \u0394t = {NIGHTLY_CADENCE_HOURS:.0f} hours \u2192 \u0394t/T = {NIGHTLY_CADENCE_HOURS/ECLIPSE_HOURS:.1f}, far too coarse; the event is effectively unsampled.',
            f'Fine cadence \u0394t = {GOOD_CADENCE_MIN:.0f} minutes = {GOOD_CADENCE_MIN/60:.2f} hours \u2192 \u0394t/T = {(GOOD_CADENCE_MIN/60)/ECLIPSE_HOURS:.3f}, giving about {ECLIPSE_HOURS/(GOOD_CADENCE_MIN/60):.0f} samples across the event \u2014 adequate to characterize ingress, minimum, and egress.',
        ],
        pitfall='Treating a sparse light curve (one point per night) as a complete time series when the phenomenon of interest varies on a timescale of hours, not days.',
        activity='Given a claimed 2.3-hour periodic signal and a proposed 6-hour cadence, decide whether the cadence is adequate and, if not, propose a better one.',
        lab_connection='This unit is assessed through Problem Set 06, which pairs the stacking calculation above with a cadence-adequacy problem for the same kind of dataset.',
        synthesis='Time is an observing dimension that requires deliberate cadence planning; the same phenomenon can be either well characterized or completely missed depending on sampling alone.',
        openstax='OpenStax Astronomy 2e, Chapter 19.3 (variable stars and cosmic distances, period-luminosity work) and Chapter 21.4 (transiting exoplanets).',
    ),
    dict(
        n=13, title='Uncertainty, Reporting, and Scientific Claims',
        subtitle='What the reader needs to trust a result',
        goals=[
            'Combine independent random uncertainties in quadrature.',
            'Separate a random uncertainty from a systematic one in a worked example.',
            'Write a one-paragraph result statement that meets a professional reporting standard.',
        ],
        why_matters='A number without an uncertainty is not a scientific claim \u2014 it is an assertion. Every measurement discussed this term (a calibrated flux, a zero point, a radial velocity, a distance) carries an uncertainty budget, and combining those budgets correctly is what lets a reader judge whether a claimed result is credible.',
        phenomenon=f'A calibrated magnitude depends on both the photometric zero point (uncertain by {SIGMA_ZP:.2f} mag, from Lecture 5\u2019s calibration) and the instrumental measurement itself (uncertain by {SIGMA_M:.3f} mag from photon statistics). Neither uncertainty alone tells the whole story.',
        vocab=['random uncertainty', 'systematic uncertainty', 'quadrature sum', 'error budget', 'claim strength', 'provenance', 'reproducibility'],
        evidence=[
            'Repeating the same measurement many times under identical conditions produces a scatter consistent with the random (statistical) uncertainty alone.',
            'Changing the calibration reference (a different zero point derivation) shifts every measurement in the same direction \u2014 the signature of a systematic uncertainty.',
            'A result quoted as "12.4 mag" with no uncertainty cannot be compared to a second team\u2019s "12.6 mag" measurement to decide whether they agree.',
        ],
        model=[
            'Independent random uncertainties combine in quadrature: \u03c3_total = \u221a(\u03c3\u2081\u00b2 + \u03c3\u2082\u00b2 + \u2026).',
            'A systematic uncertainty (like an uncertain zero point) affects all measurements the same way and should be reported separately from random scatter when possible.',
            'A defensible scientific claim states the measurement, its uncertainty, the method, and the assumptions \u2014 omitting any one weakens the claim.',
        ],
        equation=r'\sigma_{\rm total} = \sqrt{\sigma_{\rm ZP}^2 + \sigma_{m}^2}',
        example=[
            f'Zero-point uncertainty: \u03c3_ZP = {SIGMA_ZP:.2f} mag.',
            f'Instrumental measurement uncertainty: \u03c3_m = {SIGMA_M:.3f} mag.',
            f'Combined uncertainty: \u03c3_total = \u221a({SIGMA_ZP:.2f}\u00b2 + {SIGMA_M:.3f}\u00b2) = \u221a({SIGMA_ZP**2:.4f} + {SIGMA_M**2:.4f}) = \u221a{SIGMA_ZP**2+SIGMA_M**2:.4f} = {fmt(SIGMA_TOTAL,3)} mag.',
            f'A magnitude of, say, 13.42 should be reported as 13.42 \u00b1 {fmt(SIGMA_TOTAL,2)}, not as a bare number.',
        ],
        pitfall='Reporting a high-precision instrumental scatter (small \u03c3_m) as though it were the total uncertainty, while ignoring a larger systematic uncertainty (like an uncertain zero point) that dominates the real error budget.',
        activity='Given a new pair of uncertainties (a calibration uncertainty and a measurement uncertainty), compute the combined uncertainty and write one sentence stating the final result correctly.',
        lab_connection='Every lab this term has required an explicit uncertainty column; this lecture formalizes the rule used to combine those numbers into a single reported value.',
        synthesis='Good reporting tells the reader what was measured, how it was reduced, what the combined uncertainty is, and what remains unknown.',
        openstax='OpenStax Astronomy 2e, Chapter 1.3 (the nature and practice of science).',
    ),
    dict(
        n=14, title='Technical Observing Report Workshop',
        subtitle='Turning measurements into a defensible argument',
        goals=[
            'Assemble a methods-results-limitations report structure from the term\u2019s measurements.',
            'Identify which prior calculation (calibration, SNR, photometry, astrometry, spectroscopy, or uncertainty) belongs in each report section.',
            'Critique a draft report paragraph for unsupported claims.',
        ],
        why_matters='An observing proposal or technical report is a professional scientific document: it must let another astronomer understand, reproduce, and critique the reduction and interpretation without guessing at missing steps. This capstone report is 25% of the course grade and draws on every technique covered this term.',
        phenomenon='A student draft report states, "The star appeared to brighten." A stronger draft states the calibrated magnitude, its uncertainty, the aperture and zero point used, and the SNR of the detection \u2014 turning an impression into a claim that can be checked.',
        vocab=['methods section', 'results section', 'limitations section', 'reduction pipeline', 'reproducibility statement', 'claim strength', 'technical audience'],
        evidence=[
            'A methods section that omits the calibration frames used (bias, dark, flat) cannot be reproduced by another observer, exactly as flagged in Lecture 1.',
            'A results section that reports a magnitude without an SNR or uncertainty cannot be judged for reliability, exactly as flagged in Lectures 4 and 13.',
            'A limitations section that never mentions cadence, stacking method, or comparison-star stability leaves the reader unable to judge systematic risk.',
        ],
        model=[
            'A technical report follows a fixed logical order: observing question, methods (instrument, calibration, reduction), results (measurements with uncertainty), and limitations (systematics, cadence, sample size).',
            'Every quantitative claim in the results section should trace back to an explicit calculation the reader could redo.',
            'A strong conclusion states what was learned and what remains uncertain; it does not overstate certainty beyond what the uncertainty budget supports.',
        ],
        equation=r'\text{question} \rightarrow \text{observation} \rightarrow \text{reduction} \rightarrow \text{measurement} \rightarrow \text{uncertainty} \rightarrow \text{claim}',
        example=[
            f'Methods: "Standard stars STD-A/B/C were calibrated using bias B = {fmt(BIAS,1)} ADU and dark D = {fmt(DARK,2)} ADU; a zero point ZP = {fmt(ZP,3)} was derived from STD-A and verified against STD-B and STD-C to within a few millimagnitudes (Lecture 5)."',
            f'Results: "The target light curve shows a differential dip of {fmt(DM_DEPTH,3)} mag (Lecture 6), detected at SNR \u2248 {fmt(SNR_AFTER,0)} after stacking nine frames (Lecture 11)."',
            f'Limitations: "The {GOOD_CADENCE_MIN:.0f}-minute cadence resolves the {ECLIPSE_HOURS:.1f}-hour event shape (Lecture 12), but the comparison star\u2019s long-term stability beyond this night has not been independently verified."',
            'This paragraph is defensible precisely because each clause traces back to a specific, checkable calculation from earlier in the course.',
        ],
        pitfall='Writing a confident conclusion ("the star is a variable") that outruns the uncertainty budget and cadence limitations actually established by the data.',
        activity='Working from your own Lab 03\u2013Lab 07 results, draft the methods paragraph of your technical observing report and trade drafts with a partner for a two-minute reproducibility check.',
        lab_connection='This lecture directly scaffolds Problem Set 07 and the graded Technical Observing Report (25% of the course grade per the syllabus).',
        synthesis='The final report is where the term\u2019s evidence becomes a defensible scientific argument, built from calibration through uncertainty reporting.',
        openstax='OpenStax Astronomy 2e, Chapter 1.3 (scientific reasoning and communication) and Chapter 6.3 (instrumentation, for methods-section grounding).',
    ),
]


def slide_deck(item: dict) -> str:
    n = item['n']
    fig = diagram_svg(item)
    prompt_intro, prompt_qs, fig_caption = VISUAL_PROMPTS[n]
    body = f"""<main class='deck'>
<section class='slide title'><p class='kicker'>ASTR 210 &middot; Lecture {n:02d}</p><h1>{escape(item['title'])}</h1><h2>{escape(item['subtitle'])}</h2></section>
<section class='slide'><h2>Learning Goals</h2><ol>{li(item['goals'])}</ol><p class='small'>Reading anchor: {escape(item['openstax'])}</p></section>
<section class='slide'><h2>Why This Matters</h2><p>{item['why_matters']}</p></section>
<section class='slide'><h2>Opening Phenomenon</h2><p>{item['phenomenon']}</p><p class='warning'><strong>First question:</strong> what here is directly measured, and what is inferred from a model?</p></section>
<section class='slide'><h2>Vocabulary for Reasoning</h2><div class='three'>{cards(item['vocab'])}</div><p class='small'>Use these terms to describe evidence and relationships, not as isolated definitions.</p></section>
<section class='slide'><h2>Evidence We Need to Explain</h2><ul>{li(item['evidence'])}</ul></section>
<section class='slide'><h2>Model</h2><ul>{li(item['model'])}</ul></section>
<section class='slide'><h2>Quantitative Tool</h2><div class='equation'>\\[ {item['equation']} \\]</div></section>
<section class='slide'><h2>Worked Example</h2><ol>{li(item['example'])}</ol></section>
<section class='slide visual-slide'><h2>Visual Reasoning</h2><div class='visual-grid'><div><p>{escape(prompt_intro)}</p><ul>{li(prompt_qs)}</ul></div><figure class='visual-figure'>{fig}<figcaption>{escape(fig_caption)}</figcaption></figure></div></section>
<section class='slide'><h2>Common Pitfall</h2><p class='warning'>{item['pitfall']}</p></section>
<section class='slide'><h2>Active Learning Segment</h2><p>{item['activity']}</p></section>
<section class='slide'><h2>Lab or Observing Connection</h2><p>{item['lab_connection']}</p></section>
<section class='slide'><h2>Synthesis</h2><p>{item['synthesis']}</p></section>
<section class='slide'><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Local reference copy: <code>references/openstax-astronomy-2e.pdf</code>.</li><li>Course dataset used in this lecture\u2019s worked example: <code>materials/ASTR210/data/</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 210 Lecture {n:02d} Slides', body, SLIDE_CSS)


def lecture_notes(item: dict) -> str:
    n = item['n']
    body = f"""<header><div><h1>Lecture {n:02d}: {escape(item['title'])}</h1><p>ASTR 210 Observational Astronomy and Data Reduction</p></div></header>
<main>
<section><h2>Context and Why This Matters</h2><p>{item['why_matters']}</p></section>
<section><h2>Learning Goals</h2><ol>{li(item['goals'])}</ol></section>
<section><h2>Opening Phenomenon</h2><p>{item['phenomenon']}</p></section>
<section><h2>Vocabulary</h2><ul>{li(item['vocab'])}</ul></section>
<section><h2>Evidence</h2><ul>{li(item['evidence'])}</ul></section>
<section><h2>Model</h2><ul>{li(item['model'])}</ul></section>
<section><h2>Working Equation</h2><p>\\[ {item['equation']} \\]</p></section>
<section><h2>Worked Example</h2><ol>{li(item['example'])}</ol></section>
<section><h2>Common Misconception</h2><p class='notice'>{item['pitfall']}</p></section>
<section><h2>Active-Learning Guidance</h2><p>{item['activity']}</p></section>
<section><h2>Lab / Observing Connection</h2><p>{item['lab_connection']}</p></section>
<section><h2>Synthesis Questions</h2><ul><li>What was measured directly in this lecture\u2019s worked example, and what was inferred from the model?</li><li>Which uncertainty or systematic would most change the interpretation?</li><li>How does this technique connect to the technical observing report due at the end of the term?</li></ul></section>
<section><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Local reference copy: <code>references/openstax-astronomy-2e.pdf</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 210 Lecture {n:02d} Notes', body)


def write_lectures():
    for item in LECTURES:
        n = item['n']
        (LECTURE_DIR / f'lecture-{n:02d}-slides.html').write_text(slide_deck(item), encoding='utf-8')
        (LECTURE_DIR / f'lecture-{n:02d}-notes.html').write_text(lecture_notes(item), encoding='utf-8')


if __name__ == '__main__':
    write_lectures()
    print(f'Wrote {len(LECTURES)} lecture slide decks and notes files.')
