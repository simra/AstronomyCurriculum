"""Content generator for ASTR310 lecture slides and lecture notes.

Every worked numeric example is computed programmatically from the shared
constants and datasets defined below (not hand-typed), and the same
constants are reused across labs and problem sets that reference the same
scenario (see generate_astr310_labs_psets.py). Run with the project
interpreter:
    python materials/ASTR310/src/generate_astr310_content.py
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


def fmt(x, nd=2):
    return f"{x:.{nd}f}"


# ---------------------------------------------------------------------------
# Lecture-specific visual-reasoning diagrams (SVG). Each lecture gets a
# structurally distinct figure (plotted curve, labeled physical diagram, or
# orbit/geometry sketch) built from the real constants and datasets defined
# below, not a shared generic schematic. A small set of drawing primitives
# (axes, polylines, labeled dots) is shared to avoid duplicating boilerplate,
# but the assembled figure per lecture differs in shape and content.
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


def diagram_01(item: dict) -> str:
    """Flux dilution: F(d) = L/(4 pi d^2) plotted directly from the Sun's luminosity."""
    n = item['n']
    ds = [0.5 + 0.05 * i for i in range(71)]
    fluxes = [L_SUN_W / (4 * math.pi * (d * AU_M) ** 2) for d in ds]
    x0, y0, w, h = 100, 90, 780, 380
    fmax = fluxes[0]
    pts = [(_lin(d, ds[0], ds[-1], x0, x0 + w), _lin(f, 0, fmax, y0 + h, y0)) for d, f in zip(ds, fluxes)]
    f1 = L_SUN_W / (4 * math.pi * AU_M ** 2)
    f2 = L_SUN_W / (4 * math.pi * (2 * AU_M) ** 2)
    x1 = _lin(1.0, ds[0], ds[-1], x0, x0 + w)
    y1 = _lin(f1, 0, fmax, y0 + h, y0)
    x2 = _lin(2.0, ds[0], ds[-1], x0, x0 + w)
    y2 = _lin(f2, 0, fmax, y0 + h, y0)
    inner = (
        _axes(x0, y0, w, h, 'distance from source, d (AU)', 'flux, F(d) (W/m\u00b2)')
        + _polyline(pts)
        + _dot(x1, y1, f'd = 1 AU: F = {f1:.0f} W/m\u00b2')
        + _dot(x2, y2, f'd = 2 AU: F = {f2:.0f} W/m\u00b2 (exactly 1/4 of the 1 AU value)', dy=20)
        + _fig_caption('Flux falls as 1/d\u00b2 while luminosity L stays fixed at the source \u2014 pure geometric dilution over an expanding sphere.')
    )
    return _fig_wrap(n, item['title'], inner, 'flux versus distance following the inverse-square law, with 1 AU and 2 AU marked')


def diagram_02(item: dict) -> str:
    """Two real Planck curves (Sun vs a hot A-type star) with Wien peaks marked."""
    n = item['n']

    def planck(lam_m, teff):
        x = H_PLANCK * C_LIGHT / (lam_m * K_BOLTZMANN * teff)
        return (2 * H_PLANCK * C_LIGHT ** 2) / (lam_m ** 5) / (math.exp(x) - 1)

    t_cool, t_hot = SUN_TEFF, 9900.0
    lam_nm = [100 + 10 * i for i in range(280)]
    b_cool = [planck(l * 1e-9, t_cool) for l in lam_nm]
    b_hot = [planck(l * 1e-9, t_hot) for l in lam_nm]
    ymax = max(max(b_cool), max(b_hot))
    x0, y0, w, h = 100, 80, 780, 370
    pts_cool = [(_lin(l, lam_nm[0], lam_nm[-1], x0, x0 + w), _lin(b, 0, ymax, y0 + h, y0)) for l, b in zip(lam_nm, b_cool)]
    pts_hot = [(_lin(l, lam_nm[0], lam_nm[-1], x0, x0 + w), _lin(b, 0, ymax, y0 + h, y0)) for l, b in zip(lam_nm, b_hot)]
    peak_cool = wien_peak_wavelength_m(t_cool) * 1e9
    peak_hot = wien_peak_wavelength_m(t_hot) * 1e9
    xpc = _lin(peak_cool, lam_nm[0], lam_nm[-1], x0, x0 + w)
    ypc = _lin(planck(peak_cool * 1e-9, t_cool), 0, ymax, y0 + h, y0)
    xph = _lin(peak_hot, lam_nm[0], lam_nm[-1], x0, x0 + w)
    yph = _lin(planck(peak_hot * 1e-9, t_hot), 0, ymax, y0 + h, y0)
    inner = (
        _axes(x0, y0, w, h, 'wavelength, \u03bb (nm)', 'spectral radiance, B_\u03bb(T)')
        + _polyline(pts_cool, color='#b87911')
        + _polyline(pts_hot, color='#0f6b78')
        + f"<circle cx='{xpc:.1f}' cy='{ypc:.1f}' r='6' fill='#b87911'/>"
        + f"<circle cx='{xph:.1f}' cy='{yph:.1f}' r='6' fill='#0f6b78'/>"
        + f"<text x='{x0 + w - 10}' y='{y0 + 26}' font-size='14' fill='#b87911' text-anchor='end' font-family='Segoe UI, sans-serif'>{escape(f'{t_cool:.0f} K peak: {peak_cool:.0f} nm')}</text>"
        + f"<text x='{x0 + w - 10}' y='{y0 + 48}' font-size='14' fill='#0f6b78' text-anchor='end' font-family='Segoe UI, sans-serif'>{escape(f'{t_hot:.0f} K peak: {peak_hot:.0f} nm')}</text>"
        + _fig_caption('Planck curves at two temperatures: the hotter curve peaks at shorter \u03bb (Wien) and lies above the cooler curve at every \u03bb (Stefan-Boltzmann).')
    )
    return _fig_wrap(n, item['title'], inner, 'Planck function curves at two temperatures with Wien peak wavelengths marked')


def diagram_03(item: dict) -> str:
    """Exponential optical-depth attenuation I(tau)/I0 = exp(-tau)."""
    n = item['n']
    taus = [0.02 * i for i in range(401)]
    trans = [math.exp(-t) for t in taus]
    x0, y0, w, h = 100, 80, 780, 380
    pts = [(_lin(t, 0, 8, x0, x0 + w), _lin(f, 0, 1, y0 + h, y0)) for t, f in zip(taus, trans)]
    dots = ''
    for m, dy in ((1, -16), (3, -16), (7, 22)):
        f = math.exp(-m)
        x = _lin(m, 0, 8, x0, x0 + w)
        y = _lin(f, 0, 1, y0 + h, y0)
        dots += _dot(x, y, f'\u03c4 = {m}: I/I\u2080 = {f:.4f}', dy=dy)
    inner = (
        _axes(x0, y0, w, h, 'optical depth, \u03c4', 'transmitted fraction, I/I\u2080')
        + _polyline(pts) + dots
        + _fig_caption('Intensity falls exponentially with optical depth, I(\u03c4) = I\u2080 e^(-\u03c4), not linearly with physical distance.')
    )
    return _fig_wrap(n, item['title'], inner, 'exponential attenuation curve of transmitted intensity versus optical depth')


def diagram_04(item: dict) -> str:
    """Boltzmann n=2/n=1 excitation ratio (log scale) versus temperature."""
    n = item['n']
    delta_e = 1.634e-18
    g_ratio = 4.0

    def ratio(t):
        return g_ratio * math.exp(-delta_e / (K_BOLTZMANN * t))

    ts = [3000 + 100 * i for i in range(121)]
    ys = [math.log10(ratio(t)) for t in ts]
    x0, y0, w, h = 100, 80, 780, 380
    ymin, ymax = min(ys), max(ys)
    pts = [(_lin(t, ts[0], ts[-1], x0, x0 + w), _lin(y, ymin, ymax, y0 + h, y0)) for t, y in zip(ts, ys)]
    dots = ''
    for i, tm in enumerate((5750.0, 9900.0)):
        ym = math.log10(ratio(tm))
        x = _lin(tm, ts[0], ts[-1], x0, x0 + w)
        y = _lin(ym, ymin, ymax, y0 + h, y0)
        dots += _dot(x, y, f'{tm:.0f} K: n\u2082/n\u2081 = {ratio(tm):.2e}', dy=-16 - 20 * i)
    inner = (
        _axes(x0, y0, w, h, 'temperature, T (K)', 'log\u2081\u2080(n\u2082 / n\u2081)')
        + _polyline(pts) + dots
        + _fig_caption('Hydrogen n=2 excitation rises exponentially with temperature (Boltzmann); the Saha ionization turnover then suppresses it at the hottest spectral types.')
    )
    return _fig_wrap(n, item['title'], inner, 'Boltzmann excitation ratio on a log scale versus temperature, with two stars marked')


def diagram_05(item: dict) -> str:
    """Labeled hydrostatic force-balance diagram on a stellar shell, plus a schematic P(r) inset."""
    n = item['n']
    cx, cy, big_r, shell_r = 470, 300, 190, 125
    inner = (
        f"<circle cx='{cx}' cy='{cy}' r='{big_r}' fill='#fff3e0' stroke='#b87911' stroke-width='2'/>"
        f"<circle cx='{cx}' cy='{cy}' r='{shell_r}' fill='none' stroke='#0f6b78' stroke-width='4' stroke-dasharray='2,7'/>"
        f"<circle cx='{cx}' cy='{cy}' r='6' fill='#102a43'/>"
        f"<text x='{cx - 12}' y='{cy - 14}' font-size='14' fill='#102a43' text-anchor='end' font-family='Segoe UI, sans-serif'>center</text>"
        f"<line x1='{cx + shell_r}' y1='{cy}' x2='{cx + shell_r + 90}' y2='{cy}' stroke='#0f6b78' stroke-width='5' marker-end='url(#arrowP)'/>"
        f"<text x='{cx + shell_r + 6}' y='{cy - 16}' font-size='14' fill='#0f6b78' font-family='Segoe UI, sans-serif'>pressure force (outward)</text>"
        f"<line x1='{cx + shell_r - 4}' y1='{cy + 44}' x2='{cx + 26}' y2='{cy + 44}' stroke='#8a4b08' stroke-width='5' marker-end='url(#arrowG)'/>"
        f"<text x='{cx + shell_r + 6}' y='{cy + 66}' font-size='14' fill='#8a4b08' font-family='Segoe UI, sans-serif'>gravity: -GM(r)\u03c1(r)/r\u00b2 (inward)</text>"
        f"<defs>"
        f"<marker id='arrowP' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='#0f6b78'/></marker>"
        f"<marker id='arrowG' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='#8a4b08'/></marker>"
        f"</defs>"
    )
    x0, y0, w, h = 70, 420, 260, 140
    rs = [0.02 * i for i in range(51)]
    ps = [(1 - r ** 2) for r in rs]
    pts = [(_lin(r, 0, 1, x0, x0 + w), _lin(p, 0, 1, y0 + h, y0)) for r, p in zip(rs, ps)]
    inset = _axes(x0, y0, w, h, 'r / R', 'P(r) / P_c (schematic)') + _polyline(pts, color='#102a43')
    caption = _fig_caption(
        f'Force balance on a thin shell: dP/dr = -GM(r)\u03c1(r)/r\u00b2; uniform-density estimate gives P_c \u2248 {SUN_CENTRAL_PRESSURE_EST:.2e} Pa for the Sun.', y=604)
    return _fig_wrap(n, item['title'], inner + inset + caption, 'labeled hydrostatic force-balance diagram on a stellar shell with a pressure-profile inset')


def diagram_06(item: dict) -> str:
    """Balance-scale diagram for the virial theorem, 2K = |U|, with real star and cluster numbers."""
    n = item['n']
    cx, cy = 490, 230
    inner = (
        f"<polygon points='{cx - 18},{cy + 70} {cx + 18},{cy + 70} {cx},{cy + 30}' fill='#102a43'/>"
        f"<line x1='{cx - 260}' y1='{cy + 30}' x2='{cx + 260}' y2='{cy + 30}' stroke='#5b6773' stroke-width='6'/>"
        f"<line x1='{cx - 260}' y1='{cy + 30}' x2='{cx - 260}' y2='{cy + 110}' stroke='#0f6b78' stroke-width='3'/>"
        f"<line x1='{cx + 260}' y1='{cy + 30}' x2='{cx + 260}' y2='{cy + 110}' stroke='#b87911' stroke-width='3'/>"
        f"<rect x='{cx - 320}' y='{cy + 110}' width='120' height='55' rx='8' fill='#0f6b78'/>"
        f"<rect x='{cx + 200}' y='{cy + 110}' width='120' height='55' rx='8' fill='#b87911'/>"
        f"<text x='{cx - 260}' y='{cy + 143}' font-size='18' fill='#fff' text-anchor='middle' font-family='Segoe UI, sans-serif'>2K</text>"
        f"<text x='{cx + 260}' y='{cy + 143}' font-size='18' fill='#fff' text-anchor='middle' font-family='Segoe UI, sans-serif'>|U|</text>"
        f"<text x='{cx - 260}' y='{cy + 182}' font-size='14' fill='#0f6b78' text-anchor='middle' font-family='Segoe UI, sans-serif'>kinetic energy</text>"
        f"<text x='{cx + 260}' y='{cy + 182}' font-size='14' fill='#b87911' text-anchor='middle' font-family='Segoe UI, sans-serif'>gravitational |P.E.|</text>"
        f"<text x='{cx}' y='{cy}' font-size='21' fill='#102a43' text-anchor='middle' font-family='Segoe UI, sans-serif'>2K + U = 0</text>"
    )
    box1 = (
        f"<rect x='60' y='440' width='420' height='120' rx='10' fill='#e5f4f6' stroke='#0f6b78'/>"
        f"<text x='80' y='470' font-size='16' fill='#102a43' font-family='Segoe UI, sans-serif'>Star (Sun, uniform-density estimate):</text>"
        f"<text x='80' y='497' font-size='16' fill='#102a43' font-family='Segoe UI, sans-serif'>T \u2248 {SUN_VIRIAL_TEMP_EST:.2e} K</text>"
        f"<text x='80' y='522' font-size='14' fill='#5b6773' font-family='Segoe UI, sans-serif'>standard solar model: {SUN_CORE_TEMP_PUBLISHED:.2e} K</text>"
    )
    box2 = (
        f"<rect x='500' y='440' width='420' height='120' rx='10' fill='#fff3e0' stroke='#b87911'/>"
        f"<text x='520' y='470' font-size='16' fill='#102a43' font-family='Segoe UI, sans-serif'>Cluster (M15, kinematic):</text>"
        f"<text x='520' y='497' font-size='16' fill='#102a43' font-family='Segoe UI, sans-serif'>M \u2248 {M15_VIRIAL_MASS_EST:.2e} M\u2609</text>"
        f"<text x='520' y='522' font-size='14' fill='#5b6773' font-family='Segoe UI, sans-serif'>published dynamical mass: {M15_PUBLISHED_MASS_MSUN:.1e} M\u2609</text>"
    )
    caption = _fig_caption('One balance condition, 2K + U = 0, yields a star\u2019s central temperature from M, R and a cluster\u2019s mass from \u03c3, R_h.', y=600)
    return _fig_wrap(n, item['title'], inner + box1 + box2 + caption, 'balance-scale diagram of the virial theorem with matched star and cluster worked numbers')


def diagram_07(item: dict) -> str:
    """Log-log escape-velocity-versus-radius scatter for Earth, Sun, and Sirius B."""
    n = item['n']
    bodies = [
        ('Earth', EARTH_RADIUS_M, EARTH_ESCAPE_KMS, '#0f6b78'),
        ('Sun', R_SUN_M, SUN_ESCAPE_KMS, '#b87911'),
        ('Sirius B (white dwarf)', SIRIUS_B['radius_rsun'] * R_SUN_M, SIRIUS_B_ESCAPE_KMS, '#102a43'),
    ]
    logs = [(math.log10(r), math.log10(v)) for _, r, v, _ in bodies]
    x0, y0, w, h = 120, 80, 760, 380
    xs, ys = [p[0] for p in logs], [p[1] for p in logs]
    xmin, xmax = min(xs) - 0.3, max(xs) + 0.3
    ymin, ymax = min(ys) - 0.3, max(ys) + 0.3
    dots = ''
    for (idx, ((name, r, v, color), (lx, ly))) in enumerate(zip(bodies, logs)):
        x = _lin(lx, xmin, xmax, x0, x0 + w)
        y = _lin(ly, ymin, ymax, y0 + h, y0)
        dots += _dot(x, y, f'{name}: R = {r:.2e} m, v_esc = {v:.0f} km/s', color=color, dy=-16 - 18 * (idx % 2))
    inner = (
        _axes(x0, y0, w, h, 'log\u2081\u2080(radius, m)', 'log\u2081\u2080(escape velocity, km/s)')
        + dots
        + _fig_caption('At comparable mass, escape velocity scales as 1/\u221aR: Sirius B\u2019s compact radius drives its extreme escape velocity.')
    )
    return _fig_wrap(n, item['title'], inner, 'log-log scatter of escape velocity versus radius for Earth, the Sun, and Sirius B')


def diagram_08(item: dict) -> str:
    """Two-body barycentric orbit diagram sized by Alpha Centauri A/B's real mass ratio."""
    n = item['n']
    cx, cy = 490, 320
    m_a, m_b = ALPHA_CEN_A['mass_msun'], ALPHA_CEN_B['mass_msun']
    total = m_a + m_b
    a_a = 210 * (m_b / total)
    a_b = 210 * (m_a / total)
    e = ALPHA_CEN_ORBIT['eccentricity']
    b_a, b_b = a_a * math.sqrt(1 - e ** 2), a_b * math.sqrt(1 - e ** 2)
    inner = (
        f"<circle cx='{cx}' cy='{cy}' r='5' fill='#5b6773'/>"
        f"<text x='{cx + 8}' y='{cy - 10}' font-size='14' fill='#5b6773' font-family='Segoe UI, sans-serif'>barycenter</text>"
        f"<ellipse cx='{cx}' cy='{cy}' rx='{a_a:.1f}' ry='{b_a:.1f}' fill='none' stroke='#0f6b78' stroke-width='3'/>"
        f"<ellipse cx='{cx}' cy='{cy}' rx='{a_b:.1f}' ry='{b_b:.1f}' fill='none' stroke='#b87911' stroke-width='3'/>"
        f"<circle cx='{cx - a_a:.1f}' cy='{cy}' r='14' fill='#0f6b78'/>"
        f"<text x='{cx - a_a:.1f}' y='{cy + 34}' font-size='15' fill='#0f6b78' text-anchor='middle' font-family='Segoe UI, sans-serif'>\u03b1 Cen A ({m_a:.3f} M\u2609)</text>"
        f"<circle cx='{cx + a_b:.1f}' cy='{cy}' r='9' fill='#b87911'/>"
        f"<text x='{cx + a_b:.1f}' y='{cy + 34}' font-size='15' fill='#b87911' text-anchor='middle' font-family='Segoe UI, sans-serif'>\u03b1 Cen B ({m_b:.3f} M\u2609)</text>"
    )
    caption = _fig_caption(f'Each star traces its own ellipse about the shared barycenter, with a_A/a_B = M_B/M_A = {m_b / m_a:.3f}.')
    return _fig_wrap(n, item['title'], inner, 'two-body barycentric orbit diagram for Alpha Centauri A and B sized by their real mass ratio')


def diagram_09(item: dict) -> str:
    """Anti-phase radial-velocity curves for both stars, amplitude ratio set by the real mass ratio."""
    n = item['n']
    m_a, m_b = ALPHA_CEN_A['mass_msun'], ALPHA_CEN_B['mass_msun']
    k_a = 1.0
    k_b = k_a * m_a / m_b
    phases = [0.01 * i for i in range(201)]
    x0, y0, w, h = 100, 90, 780, 340
    ymax = max(k_a, k_b) * 1.2

    def y_of(v):
        return _lin(v, -ymax, ymax, y0 + h, y0)

    pts_a = [(_lin(p, 0, 2, x0, x0 + w), y_of(k_a * math.sin(2 * math.pi * p))) for p in phases]
    pts_b = [(_lin(p, 0, 2, x0, x0 + w), y_of(-k_b * math.sin(2 * math.pi * p))) for p in phases]
    zero_y = y_of(0)
    inner = (
        f"<line x1='{x0}' y1='{zero_y}' x2='{x0 + w}' y2='{zero_y}' stroke='#d9e0e7' stroke-width='2'/>"
        + _axes(x0, y0, w, h, 'orbital phase', 'radial velocity (relative units)')
        + _polyline(pts_a, color='#0f6b78')
        + _polyline(pts_b, color='#b87911')
        + _dot(_lin(0.25, 0, 2, x0, x0 + w), y_of(k_a), f'\u03b1 Cen A: K_A (relative) = {k_a:.2f}', color='#0f6b78')
        + _dot(_lin(0.75, 0, 2, x0, x0 + w), y_of(-k_b), f'\u03b1 Cen B: K_B (relative) = {k_b:.2f}', color='#b87911', dy=22)
        + _fig_caption(f'Anti-phase radial-velocity curves: amplitude ratio K_A/K_B = M_B/M_A = {m_b / m_a:.3f} (the mass-ratio lever rule).')
    )
    return _fig_wrap(n, item['title'], inner, 'anti-phase radial-velocity curves for both binary stars with amplitude ratio set by mass ratio')


def diagram_10(item: dict) -> str:
    """Roche-limit / tidal-bulge diagram for Jupiter and Io (radial scale compressed for display)."""
    n = item['n']
    cx, cy = 220, 320
    r_j, roche_px = 70, 160
    io_px = roche_px + 140 * math.log10(IO_SEMIMAJOR_M / IO_ROCHE_M)
    inner = (
        f"<circle cx='{cx}' cy='{cy}' r='{r_j}' fill='#b87911'/>"
        f"<text x='{cx}' y='{cy + r_j + 24}' font-size='15' fill='#b87911' text-anchor='middle' font-family='Segoe UI, sans-serif'>Jupiter</text>"
        f"<circle cx='{cx}' cy='{cy}' r='{roche_px}' fill='none' stroke='#8a4b08' stroke-width='3' stroke-dasharray='6,6'/>"
        f"<text x='{cx + roche_px + 8}' y='{cy - roche_px}' font-size='14' fill='#8a4b08' font-family='Segoe UI, sans-serif'>Roche limit ({IO_ROCHE_M / 1000:.0f} km)</text>"
        f"<ellipse cx='{cx + io_px:.1f}' cy='{cy}' rx='24' ry='14' fill='#0f6b78'/>"
        f"<text x='{cx + io_px:.1f}' y='{cy + 36}' font-size='15' fill='#0f6b78' text-anchor='middle' font-family='Segoe UI, sans-serif'>Io (real a = {IO_SEMIMAJOR_M / 1000:.0f} km)</text>"
    )
    caption = _fig_caption(
        f'Io orbits well outside Jupiter\u2019s Roche limit (a/d_Roche = {IO_SEMIMAJOR_M / IO_ROCHE_M:.1f}); radial scale compressed (log) for display, not to scale.')
    return _fig_wrap(n, item['title'], inner, 'Roche-limit diagram for Jupiter and Io with a tidal bulge, radial scale compressed for display')


def diagram_11(item: dict) -> str:
    """Vis-viva speed-versus-radius curve along the real Earth-Mars Hohmann transfer ellipse."""
    n = item['n']
    a_t = MARS_TRANSFER_A_AU
    rs = [1.0 + (MARS_A_AU - 1.0) * i / 100 for i in range(101)]
    speeds = [vis_viva_speed_ms(MU_SUN, r * AU_M, a_t * AU_M) / KM for r in rs]
    x0, y0, w, h = 100, 80, 780, 360
    xmin, xmax = 1.0, MARS_A_AU
    ymin, ymax = min(speeds) * 0.95, max(speeds) * 1.05
    pts = [(_lin(r, xmin, xmax, x0, x0 + w), _lin(v, ymin, ymax, y0 + h, y0)) for r, v in zip(rs, speeds)]
    x_e, x_m = _lin(1.0, xmin, xmax, x0, x0 + w), _lin(MARS_A_AU, xmin, xmax, x0, x0 + w)
    y_e_circ = _lin(V_EARTH_CIRCULAR, ymin, ymax, y0 + h, y0)
    y_e_trans = _lin(V_TRANSFER_PERIHELION, ymin, ymax, y0 + h, y0)
    y_m_circ = _lin(V_MARS_CIRCULAR, ymin, ymax, y0 + h, y0)
    y_m_trans = _lin(V_TRANSFER_APHELION, ymin, ymax, y0 + h, y0)
    inner = (
        _axes(x0, y0, w, h, 'orbital radius, r (AU)', 'speed, v (km/s)')
        + _polyline(pts, color='#0f6b78')
        + _dot(x_e, y_e_circ, f'Earth circular: {V_EARTH_CIRCULAR:.2f} km/s', color='#5b6773', dy=20)
        + _dot(x_e, y_e_trans, f'transfer perihelion: {V_TRANSFER_PERIHELION:.2f} km/s (\u0394v\u2081 = {HOHMANN_DV1:.2f})', color='#b87911', dy=-16)
        + _dot(x_m, y_m_trans, f'transfer aphelion: {V_TRANSFER_APHELION:.2f} km/s', color='#b87911', dy=20)
        + _dot(x_m, y_m_circ, f'Mars circular: {V_MARS_CIRCULAR:.2f} km/s (\u0394v\u2082 = {HOHMANN_DV2:.2f})', color='#5b6773', dy=-16)
        + _fig_caption('Vis-viva speed along the Earth-Mars Hohmann transfer ellipse; two burns bridge the gaps to each planet\u2019s circular orbit.')
    )
    return _fig_wrap(n, item['title'], inner, 'vis-viva speed versus orbital radius along the Hohmann transfer ellipse with both burns marked')


def diagram_12(item: dict) -> str:
    """Schematic Sun-Earth Lagrange-point diagram (not to scale) with the real computed L1 distance."""
    n = item['n']
    cy, sun_x, earth_x = 320, 120, 700
    inner = (
        f"<circle cx='{sun_x}' cy='{cy}' r='40' fill='#b87911'/>"
        f"<text x='{sun_x}' y='{cy + 62}' font-size='15' fill='#b87911' text-anchor='middle' font-family='Segoe UI, sans-serif'>Sun</text>"
        f"<circle cx='{earth_x}' cy='{cy}' r='14' fill='#0f6b78'/>"
        f"<text x='{earth_x}' y='{cy + 34}' font-size='15' fill='#0f6b78' text-anchor='middle' font-family='Segoe UI, sans-serif'>Earth</text>"
        f"<line x1='{sun_x}' y1='{cy}' x2='{earth_x}' y2='{cy}' stroke='#d9e0e7' stroke-width='2' stroke-dasharray='4,4'/>"
        f"<circle cx='{earth_x - 40}' cy='{cy}' r='6' fill='#102a43'/>"
        f"<text x='{earth_x - 40}' y='{cy - 16}' font-size='14' fill='#102a43' text-anchor='middle' font-family='Segoe UI, sans-serif'>L1</text>"
        f"<circle cx='{earth_x + 40}' cy='{cy}' r='6' fill='#102a43'/>"
        f"<text x='{earth_x + 40}' y='{cy - 16}' font-size='14' fill='#102a43' text-anchor='middle' font-family='Segoe UI, sans-serif'>L2</text>"
        f"<circle cx='{sun_x - 90}' cy='{cy}' r='6' fill='#102a43'/>"
        f"<text x='{sun_x - 90}' y='{cy - 16}' font-size='14' fill='#102a43' text-anchor='middle' font-family='Segoe UI, sans-serif'>L3</text>"
        f"<circle cx='{(sun_x + earth_x) / 2}' cy='{cy - 220}' r='6' fill='#0f6b78'/>"
        f"<text x='{(sun_x + earth_x) / 2}' y='{cy - 236}' font-size='14' fill='#0f6b78' text-anchor='middle' font-family='Segoe UI, sans-serif'>L4</text>"
        f"<circle cx='{(sun_x + earth_x) / 2}' cy='{cy + 220}' r='6' fill='#0f6b78'/>"
        f"<text x='{(sun_x + earth_x) / 2}' y='{cy + 244}' font-size='14' fill='#0f6b78' text-anchor='middle' font-family='Segoe UI, sans-serif'>L5</text>"
    )
    caption = _fig_caption(
        f'Schematic, not to scale: computed r_L1 \u2248 {SUN_EARTH_L1_KM:.0f} km sunward of Earth, matching SOHO/DSCOVR\u2019s real station-keeping distance.')
    return _fig_wrap(n, item['title'], inner, 'schematic Sun-Earth Lagrange point diagram with L1 through L5 marked')


def diagram_13(item: dict) -> str:
    """Eddington luminosity versus mass line, with the Sun and a Chandrasekhar-mass accretor marked."""
    n = item['n']
    masses = [0.1 + 0.05 * i for i in range(280)]
    ledd = [eddington_luminosity_w(m * M_SUN_KG) / L_SUN_W for m in masses]
    x0, y0, w, h = 110, 80, 770, 370
    xmin, xmax = masses[0], masses[-1]
    ymax = max(ledd)
    pts = [(_lin(m, xmin, xmax, x0, x0 + w), _lin(y, 0, ymax, y0 + h, y0)) for m, y in zip(masses, ledd)]
    x_sun = _lin(1.0, xmin, xmax, x0, x0 + w)
    y_sun_edd = _lin(EDDINGTON_L_SUN_W / L_SUN_W, 0, ymax, y0 + h, y0)
    y_sun_actual = _lin(1.0, 0, ymax, y0 + h, y0)
    x_chandra = _lin(CHANDRASEKHAR_MASS_MSUN, xmin, xmax, x0, x0 + w)
    y_chandra = _lin(EDDINGTON_L_CHANDRA_LSUN, 0, ymax, y0 + h, y0)
    inner = (
        _axes(x0, y0, w, h, 'mass, M (M\u2609)', 'Eddington luminosity, L_Edd (L\u2609)')
        + _polyline(pts, color='#0f6b78')
        + f"<circle cx='{x_chandra:.1f}' cy='{y_chandra:.1f}' r='6' fill='#b87911'/>"
        + f"<circle cx='{x_sun:.1f}' cy='{y_sun_edd:.1f}' r='6' fill='#102a43'/>"
        + f"<circle cx='{x_sun:.1f}' cy='{y_sun_actual:.1f}' r='6' fill='#5b6773'/>"
        + f"<line x1='{x_sun:.1f}' y1='{y_sun_edd:.1f}' x2='{x_sun:.1f}' y2='{y_sun_actual:.1f}' stroke='#5b6773' stroke-width='1.5' stroke-dasharray='3,3'/>"
        + f"<text x='{x0 + 14}' y='{y0 + 30}' font-size='14' fill='#b87911' font-family='Segoe UI, sans-serif'>{escape(f'1.4 M\u2609 accretor: L_Edd = {EDDINGTON_L_CHANDRA_LSUN:.2e} L\u2609')}</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 52}' font-size='14' fill='#102a43' font-family='Segoe UI, sans-serif'>{escape(f'Sun\u2019s own L_Edd = {EDDINGTON_L_SUN_W / L_SUN_W:.2e} L\u2609')}</text>"
        + f"<text x='{x0 + 14}' y='{y0 + 74}' font-size='14' fill='#5b6773' font-family='Segoe UI, sans-serif'>{escape(f'Sun\u2019s actual L = 1 L\u2609 ({L_SUN_W / EDDINGTON_L_SUN_W * 100:.2e}% of its own L_Edd)')}</text>"
        + _fig_caption('L_Edd scales linearly with mass; every normal, non-accreting star sits enormously below its own Eddington limit.')
    )
    return _fig_wrap(n, item['title'], inner, 'Eddington luminosity versus mass line with the Sun and a Chandrasekhar-mass accretor marked')


def diagram_14(item: dict) -> str:
    """Convergence diagram: independent radiative and dynamical chains meeting on Alpha Centauri AB."""
    n = item['n']
    l_agree = abs(ALPHA_CEN_A_L_FROM_SB_LSUN - ALPHA_CEN_A['lum_lsun']) / ALPHA_CEN_A['lum_lsun'] * 100
    m_agree = abs(ALPHA_CEN_TOTAL_MASS_KEPLER - ALPHA_CEN_TOTAL_MASS_MEASURED) / ALPHA_CEN_TOTAL_MASS_MEASURED * 100
    inner = (
        f"<rect x='60' y='90' width='230' height='70' rx='10' fill='#e5f4f6' stroke='#0f6b78'/>"
        f"<text x='175' y='120' font-size='15' fill='#102a43' text-anchor='middle' font-family='Segoe UI, sans-serif'>R, T (measured)</text>"
        f"<text x='175' y='142' font-size='12.5' fill='#5b6773' text-anchor='middle' font-family='Segoe UI, sans-serif'>interferometry + asteroseismology</text>"
        f"<rect x='360' y='90' width='230' height='70' rx='10' fill='#e5f4f6' stroke='#0f6b78'/>"
        f"<text x='475' y='120' font-size='15' fill='#102a43' text-anchor='middle' font-family='Segoe UI, sans-serif'>L = 4\u03c0R\u00b2\u03c3T\u2074</text>"
        f"<text x='475' y='142' font-size='12.5' fill='#5b6773' text-anchor='middle' font-family='Segoe UI, sans-serif'>Stefan-Boltzmann (radiative chain)</text>"
        f"<line x1='290' y1='125' x2='355' y2='125' stroke='#0f6b78' stroke-width='4' marker-end='url(#arrowRad)'/>"
        f"<rect x='60' y='400' width='230' height='70' rx='10' fill='#fff3e0' stroke='#b87911'/>"
        f"<text x='175' y='430' font-size='15' fill='#102a43' text-anchor='middle' font-family='Segoe UI, sans-serif'>P, a (measured)</text>"
        f"<text x='175' y='452' font-size='12.5' fill='#5b6773' text-anchor='middle' font-family='Segoe UI, sans-serif'>decades of astrometry</text>"
        f"<rect x='360' y='400' width='230' height='70' rx='10' fill='#fff3e0' stroke='#b87911'/>"
        f"<text x='475' y='430' font-size='15' fill='#102a43' text-anchor='middle' font-family='Segoe UI, sans-serif'>M = 4\u03c0\u00b2a\u00b3/(GP\u00b2)</text>"
        f"<text x='475' y='452' font-size='12.5' fill='#5b6773' text-anchor='middle' font-family='Segoe UI, sans-serif'>Kepler\u2019s third law (dynamical chain)</text>"
        f"<line x1='290' y1='435' x2='355' y2='435' stroke='#b87911' stroke-width='4' marker-end='url(#arrowDyn)'/>"
        f"<line x1='590' y1='125' x2='740' y2='280' stroke='#0f6b78' stroke-width='4'/>"
        f"<line x1='590' y1='435' x2='740' y2='320' stroke='#b87911' stroke-width='4'/>"
        f"<rect x='740' y='230' width='190' height='140' rx='12' fill='#102a43'/>"
        f"<text x='835' y='260' font-size='16' fill='#fff' text-anchor='middle' font-family='Segoe UI, sans-serif'>\u03b1 Cen AB</text>"
        f"<text x='835' y='285' font-size='13' fill='#fff' text-anchor='middle' font-family='Segoe UI, sans-serif'>L agreement: {l_agree:.1f}%</text>"
        f"<text x='835' y='308' font-size='13' fill='#fff' text-anchor='middle' font-family='Segoe UI, sans-serif'>M agreement: {m_agree:.2f}%</text>"
        f"<text x='835' y='333' font-size='13' fill='#fff' text-anchor='middle' font-family='Segoe UI, sans-serif'>independent physics, same answer</text>"
        f"<defs>"
        f"<marker id='arrowRad' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='#0f6b78'/></marker>"
        f"<marker id='arrowDyn' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='#b87911'/></marker>"
        f"</defs>"
    )
    caption = _fig_caption('Two independent chains (radiative and dynamical) converge on the same physical description of \u03b1 Centauri AB.', y=595)
    return _fig_wrap(n, item['title'], inner + caption, 'convergence diagram of radiative and dynamical measurement chains meeting on Alpha Centauri AB')


_DIAGRAM_BUILDERS = {
    1: diagram_01, 2: diagram_02, 3: diagram_03, 4: diagram_04, 5: diagram_05,
    6: diagram_06, 7: diagram_07, 8: diagram_08, 9: diagram_09, 10: diagram_10,
    11: diagram_11, 12: diagram_12, 13: diagram_13, 14: diagram_14,
}


def lecture_svg(item: dict) -> str:
    return _DIAGRAM_BUILDERS[item['n']](item)


# ---------------------------------------------------------------------------
# Physical constants (SI unless noted)
# ---------------------------------------------------------------------------
SIGMA_SB = 5.670374e-8       # W m^-2 K^-4
G_NEWTON = 6.674e-11         # m^3 kg^-1 s^-2
C_LIGHT = 2.998e8            # m/s
H_PLANCK = 6.626e-34         # J s
K_BOLTZMANN = 1.381e-23      # J/K
M_PROTON = 1.6726e-27        # kg
SIGMA_THOMSON = 6.6524e-29   # m^2 (Thomson electron-scattering cross-section)
M_SUN_KG = 1.989e30
R_SUN_M = 6.957e8
L_SUN_W = 3.828e26           # published (satellite radiometry)
AU_M = 1.496e11
YEAR_S = 3.15576e7           # Julian year, 365.25 days
PC_M = 3.0857e16
MPC_KM = 3.0857e19
KM = 1000.0
SUN_TEFF = 5778.0

# Wien's displacement constant (b = h c / 4.965 k, from maximizing the Planck function)
WIEN_B = H_PLANCK * C_LIGHT / (4.9651142 * K_BOLTZMANN)  # m K


def wien_peak_wavelength_m(teff_k: float) -> float:
    return WIEN_B / teff_k


def stefan_boltzmann_luminosity_w(r_m: float, teff_k: float) -> float:
    return 4 * math.pi * (r_m ** 2) * SIGMA_SB * (teff_k ** 4)


# ---------------------------------------------------------------------------
# Shared real dataset: Alpha Centauri AB, live-verified this session via a
# direct web fetch of Wikipedia's "Alpha Centauri" article (2026-09-24),
# which cites Akeson et al. 2021, AJ 162, 14 (VLTI/PIONIER + orbit fit) for
# masses/radii/luminosities/temperatures and the Sixth Catalog of Orbits of
# Visual Binary Stars (Hartkopf & Mason 2008) plus Akeson et al. 2021 for the
# orbital elements. This is the primary real-binary dataset threaded through
# Lectures 07-09 and 14, Labs 04 and 07, and Problem Sets 04 and 07.
# ---------------------------------------------------------------------------
ALPHA_CEN_A = dict(name='Alpha Centauri A (Rigil Kentaurus)', mass_msun=1.0788, radius_rsun=1.223,
                    lum_lsun=1.5059, teff=5748.0, spt='G2V')
ALPHA_CEN_B = dict(name='Alpha Centauri B (Toliman)', mass_msun=0.9092, radius_rsun=0.864,
                    lum_lsun=0.4981, teff=5154.0, spt='K1V')
ALPHA_CEN_ORBIT = dict(period_yr=79.762, semimajor_au=23.299, eccentricity=0.51947,
                        inclination_deg=79.243, parallax_mas=750.81, distance_pc=1.3319)
# Proxima Centauri's much wider, highly eccentric orbit around the AB barycenter
# (Kervella, Thevenin & Lovis 2017, A&A 598, L7; also live-verified this session).
PROXIMA_ORBIT = dict(period_yr=511000.0, periastron_au=4100.0, apastron_au=12300.0, eccentricity=0.5,
                      mass_msun=0.1221)

# Sirius B (white dwarf) parameters carried forward from ASTR230 (Bond et al.
# 2017, ApJ 840, 70; live-verified in that course's production) for the
# escape-velocity contrast in Lecture 07; provenance already established.
SIRIUS_B = dict(mass_msun=1.018, radius_rsun=0.008098, teff=25000.0)

EARTH_MASS_KG = 5.972e24
EARTH_RADIUS_M = 6.371e6
MOON_MASS_KG = 7.342e22
MOON_RADIUS_M = 1.7374e6
MOON_ORBIT_M = 3.844e8  # mean Earth-Moon distance

# Io / Jupiter (standard published values; not independently re-verified by
# live fetch this session -- flagged in reference-log.md).
JUPITER_MASS_KG = 1.89819e27
IO_MASS_KG = 8.9319e22
IO_RADIUS_M = 1821.6e3
IO_SEMIMAJOR_M = 421700e3
IO_ECCENTRICITY = 0.0041

# Chandrasekhar-mass compact accretor for the Eddington-luminosity example
CHANDRASEKHAR_MASS_MSUN = 1.4

# M15 globular cluster (standard published values used for the Lecture 06 /
# Lab 03 virial-theorem worked example; flagged for spot-check against the
# Harris (1996, 2010 ed.) Galactic globular cluster catalog).
M15_SIGMA_KMS = 12.0
M15_HALF_LIGHT_PC = 4.2
M15_PUBLISHED_MASS_MSUN = 5.6e5


def virial_mass_msun(sigma_kms: float, r_half_pc: float) -> float:
    """Standard single-mass virial estimator M = 5 sigma^2 R_h / G (King 1966-style)."""
    sigma_ms = sigma_kms * KM
    r_m = r_half_pc * PC_M
    m_kg = 5 * (sigma_ms ** 2) * r_m / G_NEWTON
    return m_kg / M_SUN_KG


def kepler3_total_mass_msun(period_yr: float, semimajor_au: float) -> float:
    """Generalized Kepler's third law: P^2 = 4 pi^2 a^3 / (G (M1+M2))."""
    p_s = period_yr * YEAR_S
    a_m = semimajor_au * AU_M
    total_kg = 4 * (math.pi ** 2) * (a_m ** 3) / (G_NEWTON * p_s ** 2)
    return total_kg / M_SUN_KG


def escape_velocity_ms(mass_kg: float, radius_m: float) -> float:
    return math.sqrt(2 * G_NEWTON * mass_kg / radius_m)


def hydrostatic_central_pressure_pa(mass_kg: float, radius_m: float) -> float:
    """Order-of-magnitude central pressure for a self-gravitating sphere,
    P_c ~ (3/(8 pi)) G M^2 / R^4 (exact for the uniform-density case, used
    here as a scaling estimate for the Sun)."""
    return (3.0 / (8.0 * math.pi)) * G_NEWTON * (mass_kg ** 2) / (radius_m ** 4)


def virial_core_temperature_k(mass_kg: float, radius_m: float, mu_mp: float = 0.5 * M_PROTON) -> float:
    """Order-of-magnitude central/mean temperature from the virial theorem
    applied to a uniform self-gravitating sphere of ideal gas:
    (3/5) GM^2/R = (3/2) N k T with N = M/(mu m_p), giving
    T ~ (mu m_p G M) / (5 k R)."""
    return (mu_mp * G_NEWTON * mass_kg) / (5 * K_BOLTZMANN * radius_m)


def roche_limit_m(m_primary_kg: float, r_secondary_m: float, rho_primary: float, rho_secondary: float) -> float:
    """Rigid-body Roche limit: d = R_secondary * (2 * rho_primary/rho_secondary)^(1/3)
    expressed via the primary's mass and mean density for direct comparison."""
    r_primary_m = (3 * m_primary_kg / (4 * math.pi * rho_primary)) ** (1.0 / 3.0)
    return r_primary_m * (2.0 * rho_primary / rho_secondary) ** (1.0 / 3.0)


def eddington_luminosity_w(mass_kg: float) -> float:
    return 4 * math.pi * G_NEWTON * mass_kg * M_PROTON * C_LIGHT / SIGMA_THOMSON


def vis_viva_speed_ms(mu: float, r_m: float, a_m: float) -> float:
    return math.sqrt(mu * (2.0 / r_m - 1.0 / a_m))


MU_SUN = G_NEWTON * M_SUN_KG
EARTH_A_AU = 1.0000
EARTH_E = 0.0167
MARS_A_AU = 1.5237

# Verify Alpha Centauri's Kepler-3 total mass against the independently
# measured (asteroseismic/interferometric) individual masses.
ALPHA_CEN_TOTAL_MASS_KEPLER = kepler3_total_mass_msun(ALPHA_CEN_ORBIT['period_yr'], ALPHA_CEN_ORBIT['semimajor_au'])
ALPHA_CEN_TOTAL_MASS_MEASURED = ALPHA_CEN_A['mass_msun'] + ALPHA_CEN_B['mass_msun']

SUN_L_FROM_SB = stefan_boltzmann_luminosity_w(R_SUN_M, SUN_TEFF)
ALPHA_CEN_A_L_FROM_SB_W = stefan_boltzmann_luminosity_w(ALPHA_CEN_A['radius_rsun'] * R_SUN_M, ALPHA_CEN_A['teff'])
ALPHA_CEN_A_L_FROM_SB_LSUN = ALPHA_CEN_A_L_FROM_SB_W / L_SUN_W
ALPHA_CEN_B_L_FROM_SB_W = stefan_boltzmann_luminosity_w(ALPHA_CEN_B['radius_rsun'] * R_SUN_M, ALPHA_CEN_B['teff'])
ALPHA_CEN_B_L_FROM_SB_LSUN = ALPHA_CEN_B_L_FROM_SB_W / L_SUN_W

EARTH_ESCAPE_KMS = escape_velocity_ms(EARTH_MASS_KG, EARTH_RADIUS_M) / KM
SUN_ESCAPE_KMS = escape_velocity_ms(M_SUN_KG, R_SUN_M) / KM
SIRIUS_B_ESCAPE_KMS = escape_velocity_ms(SIRIUS_B['mass_msun'] * M_SUN_KG, SIRIUS_B['radius_rsun'] * R_SUN_M) / KM

SUN_CENTRAL_PRESSURE_EST = hydrostatic_central_pressure_pa(M_SUN_KG, R_SUN_M)
SUN_CENTRAL_PRESSURE_PUBLISHED = 2.477e16  # Pa, standard solar-model value (level 2)
SUN_VIRIAL_TEMP_EST = virial_core_temperature_k(M_SUN_KG, R_SUN_M)
SUN_CORE_TEMP_PUBLISHED = 1.57e7  # K, standard solar-model value (level 2)

M15_VIRIAL_MASS_EST = virial_mass_msun(M15_SIGMA_KMS, M15_HALF_LIGHT_PC)

MOON_DENSITY = MOON_MASS_KG / ((4.0 / 3.0) * math.pi * MOON_RADIUS_M ** 3)
EARTH_DENSITY = EARTH_MASS_KG / ((4.0 / 3.0) * math.pi * EARTH_RADIUS_M ** 3)
EARTH_MOON_ROCHE_M = roche_limit_m(EARTH_MASS_KG, MOON_RADIUS_M, EARTH_DENSITY, MOON_DENSITY)

IO_DENSITY = IO_MASS_KG / ((4.0 / 3.0) * math.pi * IO_RADIUS_M ** 3)
JUPITER_MEAN_DENSITY = 1326.0  # kg/m^3, standard published value
IO_ROCHE_M = roche_limit_m(JUPITER_MASS_KG, IO_RADIUS_M, JUPITER_MEAN_DENSITY, IO_DENSITY)


def tidal_acceleration_diff(m_perturber_kg: float, d_m: float, body_radius_m: float) -> float:
    """Differential tidal acceleration across a body of radius r at distance d
    from a perturbing mass M: da = 2 G M r / d^3."""
    return 2 * G_NEWTON * m_perturber_kg * body_radius_m / (d_m ** 3)


IO_TIDAL_ACCEL = tidal_acceleration_diff(JUPITER_MASS_KG, IO_SEMIMAJOR_M, IO_RADIUS_M)
IO_SURFACE_GRAVITY_MS2 = G_NEWTON * IO_MASS_KG / (IO_RADIUS_M ** 2)

CHANDRASEKHAR_MASS_KG = CHANDRASEKHAR_MASS_MSUN * M_SUN_KG
EDDINGTON_L_CHANDRA_W = eddington_luminosity_w(CHANDRASEKHAR_MASS_KG)
EDDINGTON_L_CHANDRA_LSUN = EDDINGTON_L_CHANDRA_W / L_SUN_W
EDDINGTON_L_SUN_W = eddington_luminosity_w(M_SUN_KG)

MARS_TRANSFER_A_AU = 0.5 * (EARTH_A_AU + MARS_A_AU)
V_EARTH_CIRCULAR = math.sqrt(MU_SUN / (EARTH_A_AU * AU_M)) / KM
V_TRANSFER_PERIHELION = vis_viva_speed_ms(MU_SUN, EARTH_A_AU * AU_M, MARS_TRANSFER_A_AU * AU_M) / KM
HOHMANN_DV1 = V_TRANSFER_PERIHELION - V_EARTH_CIRCULAR
V_MARS_CIRCULAR = math.sqrt(MU_SUN / (MARS_A_AU * AU_M)) / KM
V_TRANSFER_APHELION = vis_viva_speed_ms(MU_SUN, MARS_A_AU * AU_M, MARS_TRANSFER_A_AU * AU_M) / KM
HOHMANN_DV2 = V_MARS_CIRCULAR - V_TRANSFER_APHELION
HOHMANN_TRANSFER_TIME_YR = 0.5 * math.sqrt(MARS_TRANSFER_A_AU ** 3)  # Kepler's 3rd law in AU/yr units

# Sun-Earth L1 distance (restricted three-body, standard leading-order result
# r_L1 = R (m2 / 3 m1)^(1/3) for m2 << m1)
SUN_EARTH_L1_KM = AU_M * (EARTH_MASS_KG / (3 * M_SUN_KG)) ** (1.0 / 3.0) / KM

# ---------------------------------------------------------------------------
# Lecture content
# ---------------------------------------------------------------------------
LECTURES = [
    dict(
        n=1, title='Describing Radiation: Flux, Intensity, and the Electromagnetic Spectrum',
        subtitle='The language every later derivation in this course will use',
        goals=[
            'Distinguish specific intensity, flux, and luminosity as distinct radiative quantities with distinct units.',
            'Derive the inverse-square dilution of flux from a point source using energy conservation across expanding spheres.',
            'Explain why intensity, unlike flux, is independent of distance along a ray in vacuum.',
        ],
        why_matters='ASTR 230 used luminosity, flux, and the inverse-square law as given formulas. This course rebuilds them from energy conservation so that every later result (blackbody radiation, radiative transfer, hydrostatic equilibrium) rests on the same small set of first principles rather than a list of memorized relations.',
        phenomenon=f'A source of luminosity L radiates energy through every sphere surrounding it at the same total rate, yet the flux (power per unit area) falls as 1/d^2 because the sphere\u2019s area grows as d^2 while the enclosed power does not grow at all \u2014 this single geometric fact, not any property of light itself, is the entire content of the inverse-square law.',
        vocab=['specific intensity', 'flux', 'luminosity', 'solid angle', 'radiative flux', 'surface brightness'],
        evidence=[
            'Integrating flux F = L/(4\u03c0d\u00b2) over any sphere of radius d centered on an isotropic source returns exactly L, independent of d \u2014 the defining consistency check for the inverse-square law.',
            'A telescope\u2019s measured surface brightness (intensity) of a resolved object, such as the solar disk, does not change with the telescope\u2019s distance from the Sun (ignoring atmospheric and instrumental effects), while the Sun\u2019s total flux clearly does fall with distance \u2014 intensity and flux are physically distinct quantities.',
            'Doubling the distance to an unresolved point source (a star) always reduces its flux by a factor of exactly 4, independent of the star\u2019s spectral type, luminosity, or composition, confirming the purely geometric origin of the inverse-square law.',
        ],
        model=[
            'Specific intensity I_\u03bd (energy per unit time, area, solid angle, and frequency interval) is conserved along a ray in vacuum: it does not fall off with distance, because both the emitting and receiving areas subtend proportionally smaller solid angles as distance grows, exactly canceling.',
            'Flux F is the intensity integrated over solid angle; for an isotropic point source of luminosity L, the flux measured on a sphere of radius d is F = L/(4\u03c0d\u00b2), because the same total power L is spread over a sphere of surface area 4\u03c0d\u00b2.',
            'Luminosity is the total power radiated in all directions; it is a property of the source alone, while flux additionally depends on the observer\u2019s distance.',
        ],
        equation=r'F(d) = \dfrac{L}{4\pi d^{2}}, \qquad \oint_{\text{sphere}} F(d)\,dA = L \ \ (\text{independent of } d)',
        example=[
            f'Take a source of luminosity L = {L_SUN_W:.3e} W (the Sun) and evaluate flux at d = 1 AU = {AU_M:.3e} m: F = L/(4\u03c0d\u00b2) = {L_SUN_W/(4*math.pi*AU_M**2):.1f} W/m\u00b2, matching the standard quoted solar constant of about 1361 W/m\u00b2.',
            f'At d = 2 AU: F = {L_SUN_W/(4*math.pi*(2*AU_M)**2):.1f} W/m\u00b2, exactly one quarter of the 1 AU value, confirming the 1/d\u00b2 scaling numerically rather than merely asserting it.',
            f'Total power crossing a sphere of radius 2 AU: F(2\u2009AU) \u00d7 4\u03c0(2\u2009AU)\u00b2 = {L_SUN_W/(4*math.pi*(2*AU_M)**2)*4*math.pi*(2*AU_M)**2:.3e} W, identical (up to rounding) to L itself, verifying energy conservation across the larger sphere.',
        ],
        pitfall='Treating "brightness" as a single unambiguous quantity. A resolved object\u2019s surface brightness (intensity) and an unresolved source\u2019s total flux behave completely differently with distance; conflating them leads to errors whenever the observed source begins to be resolved (e.g., nearby versus distant nebulae of the same physical brightness).',
        activity='Given two identical light bulbs, one twice as far away as the other, predict the flux ratio without a calculator using only the inverse-square scaling, then verify with the formula.',
        lab_connection='Lab 01 applies F = L/(4\u03c0d\u00b2) together with the Stefan-Boltzmann law (Lecture 02) to recover real stellar radii and temperatures from measured flux and distance.',
        synthesis='Flux, intensity, and luminosity are three distinct radiative quantities related by simple geometry; keeping them distinct is the foundation for every quantitative radiative argument later in this course.',
        openstax='OpenStax Astronomy 2e, Chapter 5.1-5.2 (radiation, telescope light-gathering) and Chapter 18.1 (measuring the brightness of stars); this course goes beyond the introductory treatment by deriving intensity conservation explicitly.',
    ),
    dict(
        n=2, title='The Blackbody Radiation Law: From Planck\u2019s Function to Stefan-Boltzmann and Wien',
        subtitle='Deriving, not just applying, the law that makes stellar astrophysics quantitative',
        goals=[
            'State the Planck radiation law and describe, without full derivation, the physical assumptions (quantized oscillator energies) that produce it.',
            'Derive Wien\u2019s displacement law and the Stefan-Boltzmann law as integrals/limits of the Planck function.',
            'Apply both laws together to a real star and cross-check the result against an independently measured luminosity.',
        ],
        why_matters='ASTR 230 used L = 4\u03c0R\u00b2\u03c3T\u2074 and Wien\u2019s law as given tools. Max Planck derived the underlying spectral law in 1900 by proposing that oscillators in a cavity wall could only exchange energy in discrete quanta hf \u2014 a proposal that resolved the "ultraviolet catastrophe" of classical (Rayleigh-Jeans) theory and opened the door to quantum mechanics. Seeing where Stefan-Boltzmann and Wien actually come from is what distinguishes an astrophysics course from an applied-formulas course.',
        phenomenon=f'Classical (Rayleigh-Jeans) theory predicts that a blackbody\u2019s emitted intensity should grow without bound at short wavelengths, a divergence dubbed the ultraviolet catastrophe. Real blackbodies, including the Sun (T_eff = {SUN_TEFF:.0f} K), instead show intensity rising, peaking near a characteristic wavelength, and falling off exponentially at short wavelengths, exactly as the Planck function predicts and the classical theory does not.',
        vocab=['Planck function', 'quantized oscillator energy', 'Wien\u2019s displacement law', 'Stefan-Boltzmann law', 'ultraviolet catastrophe', 'effective temperature'],
        evidence=[
            'Every star\u2019s continuous spectrum closely follows a Planck curve of some characteristic temperature, regardless of the star\u2019s size, composition, or distance, exactly as expected if the emergent radiation is set by the emitting surface\u2019s temperature alone.',
            'The Planck function\u2019s peak wavelength shifts to shorter wavelengths for hotter blackbodies in exact proportion to 1/T (Wien\u2019s law), verified in laboratory blackbody sources across many decades of temperature.',
            'The total area under the Planck function (integrated over all wavelengths) grows as T\u2074, verified directly for the Sun by comparing the Stefan-Boltzmann prediction from its measured radius and temperature to its independently measured total luminosity.',
        ],
        model=[
            'The Planck function B_\u03bd(T) = (2h\u03bd\u00b3/c\u00b2) \u00d7 1/(e^{h\u03bd/kT} - 1) follows from assuming that the electromagnetic field modes in a cavity in thermal equilibrium can only carry energy in discrete quanta of size h\u03bd, with the mean occupation number of each mode given by Bose-Einstein statistics.',
            'Differentiating B_\u03bb(T) with respect to \u03bb and setting the result to zero gives the wavelength of maximum emission, \u03bb_max T = b (Wien\u2019s displacement law), with b = hc/(4.965k) a fixed constant \u2014 the "4.965" is the numerical root of a transcendental equation from the derivative, not an arbitrary fit parameter.',
            'Integrating B_\u03bd(T) over all frequencies and over the outward hemisphere gives the total emitted power per unit area, \u03c3T\u2074 (the Stefan-Boltzmann law), with \u03c3 = 2\u03c0\u2075k\u2074/(15h\u00b3c\u00b2) expressible entirely in terms of more fundamental constants (h, k, c) rather than being an independent empirical constant.',
        ],
        equation=r'B_\nu(T) = \dfrac{2h\nu^{3}}{c^{2}}\dfrac{1}{e^{h\nu/kT}-1}, \qquad \lambda_{\max}T = b, \qquad L = 4\pi R^{2}\sigma T^{4}',
        example=[
            f'Wien\u2019s law for the Sun: \u03bb_max = b/T = {WIEN_B:.4e} m\u00b7K / {SUN_TEFF:.0f} K = {wien_peak_wavelength_m(SUN_TEFF)*1e9:.0f} nm, in the visible-green part of the spectrum \u2014 consistent with human vision having evolved to be most sensitive near this wavelength.',
            f'Wien\u2019s law for Alpha Centauri A (T_eff = {ALPHA_CEN_A["teff"]:.0f} K, live-verified this session): \u03bb_max = {wien_peak_wavelength_m(ALPHA_CEN_A["teff"])*1e9:.0f} nm, close to the Sun\u2019s peak, consistent with its near-solar G2V spectral type.',
            f'Stefan-Boltzmann applied to Alpha Centauri A: R = {ALPHA_CEN_A["radius_rsun"]:.3f} R\u2609 = {ALPHA_CEN_A["radius_rsun"]*R_SUN_M:.3e} m, T = {ALPHA_CEN_A["teff"]:.0f} K, giving L = 4\u03c0R\u00b2\u03c3T\u2074 = {ALPHA_CEN_A_L_FROM_SB_W:.3e} W = {ALPHA_CEN_A_L_FROM_SB_LSUN:.3f} L\u2609.',
            f'The independently measured (interferometric + asteroseismic) luminosity of Alpha Centauri A is {ALPHA_CEN_A["lum_lsun"]:.4f} L\u2609; the Stefan-Boltzmann prediction from its measured radius and temperature agrees to within {abs(ALPHA_CEN_A_L_FROM_SB_LSUN-ALPHA_CEN_A["lum_lsun"])/ALPHA_CEN_A["lum_lsun"]*100:.1f}%, an independent cross-check of the same law verified for the Sun in ASTR 230.',
        ],
        pitfall='Treating \u03c3 in the Stefan-Boltzmann law as an arbitrary empirical fitting constant. It is fully determined by h, k, and c through the Planck-function integral; the same is true of Wien\u2019s constant b. Neither law is an independent postulate once the Planck function is accepted.',
        activity='Using only the T\u2074 scaling (without recomputing from scratch), predict how much more luminous per unit area a 12,000 K star\u2019s surface radiates compared to the Sun\u2019s surface, then verify with the formula.',
        lab_connection='Lab 01 uses both Wien\u2019s law and Stefan-Boltzmann together on Alpha Centauri A and B to recover their temperatures and radii self-consistently and cross-check against the independently measured luminosities used in this lecture.',
        synthesis='The Stefan-Boltzmann and Wien laws are not independent empirical rules but specific limits and integrals of the single underlying Planck function, itself a consequence of quantized field-mode energies.',
        openstax='OpenStax Astronomy 2e, Chapter 5.4 (the electromagnetic spectrum, blackbody radiation); this course derives \u03c3 and b from the Planck function rather than presenting them as given constants.',
    ),
    dict(
        n=3, title='Radiative Transfer: Optical Depth and the Equation of Transfer',
        subtitle='What happens to a beam of light as it crosses matter',
        goals=[
            'Define optical depth and explain its role as a dimensionless measure of "how much" absorbing/scattering material a beam has crossed.',
            'Derive the exponential attenuation law (Beer\u2013Lambert-type extinction) from the radiative transfer equation in the absence of emission.',
            'Explain physically why we see only down to optical depth of order unity into a stellar atmosphere.',
        ],
        why_matters='Every spectral line, every measured stellar temperature, and every photon that ever reaches a telescope is the outcome of radiative transfer through some column of gas. Optical depth is the single quantity that determines whether that gas is transparent, translucent, or opaque to a given wavelength, and it underlies the "photosphere" concept used loosely in introductory courses.',
        phenomenon='Sunlight reaching Earth\u2019s surface is strongly and selectively absorbed in narrow wavelength bands (e.g., by atmospheric ozone, water vapor, and CO2), while passing through nearly unattenuated at other wavelengths (the visible "optical window") \u2014 the same physical framework (wavelength-dependent optical depth) explains both stellar photospheres and Earth\u2019s atmospheric transmission windows.',
        vocab=['optical depth', 'opacity (absorption coefficient)', 'mean free path', 'radiative transfer equation', 'photosphere', 'source function'],
        evidence=[
            'A stellar photosphere is not a sharp physical surface; instead, it is operationally defined as the layer at which the optical depth (looking outward) reaches approximately 2/3 to 1, because photons from deeper, hotter layers are overwhelmingly likely to be absorbed before escaping.',
            'Different wavelengths of light from the same star emerge from different physical depths, because opacity (and hence optical depth per unit physical distance) depends strongly on wavelength \u2014 this is why spectral lines (high opacity wavelengths) sample higher, cooler layers than the surrounding continuum.',
            'Doubling the column density of absorbing gas along a line of sight doubles the optical depth (for a fixed opacity), and because transmitted intensity falls as e^{-\u03c4}, this produces a much larger than linear reduction in the fraction of light transmitted.',
        ],
        model=[
            'Optical depth is defined as \u03c4_\u03bb = \u222b \u03ba_\u03bb \u03c1 ds along the line of sight, where \u03ba_\u03bb is the wavelength-dependent opacity (absorption + scattering cross-section per unit mass) and \u03c1 is the gas density; \u03c4 is dimensionless by construction.',
            'In the absence of emission along the path, the transfer equation dI_\u03bd/d\u03c4_\u03bd = -I_\u03bd integrates to I_\u03bd(\u03c4) = I_\u03bd(0) e^{-\u03c4_\u03bd}: intensity is attenuated exponentially with optical depth, not linearly with physical distance.',
            'A layer with \u03c4 << 1 is optically thin (nearly transparent; we see essentially all the way through it), while a layer with \u03c4 >> 1 is optically thick (opaque; we see only down to about \u03c4 \u2248 1 before all deeper radiation is reprocessed/absorbed).',
        ],
        equation=r'\tau_\lambda = \int \kappa_\lambda \rho \, ds, \qquad \dfrac{dI_\nu}{d\tau_\nu} = -I_\nu \implies I_\nu(\tau) = I_\nu(0)\, e^{-\tau_\nu}',
        example=[
            'Take a uniform slab with optical depth \u03c4 = 1: the transmitted fraction is e\u207b\u00b9 \u2248 0.368, i.e., about 37% of the incident intensity survives to the far side.',
            'At \u03c4 = 3: transmitted fraction = e\u207b\u00b3 \u2248 0.0498, about 5% \u2014 tripling the optical depth reduces transmission by roughly a factor of 7.4, illustrating the exponential (not linear) sensitivity to \u03c4.',
            'At \u03c4 = 7 (a rough proxy for a strong stellar absorption line core viewed against the deeper, hotter continuum-forming layers): transmitted fraction = e\u207b\u2077 \u2248 9.1 \u00d7 10\u207b\u2074, i.e., only about 0.09% of the deep continuum intensity survives at that wavelength, which is exactly why strong absorption lines appear as deep, dark features: essentially none of the hot, deep light escapes at that specific wavelength.',
        ],
        pitfall='Assuming a "surface" like the photosphere is a sharp physical boundary analogous to a planet\u2019s solid surface. It is a wavelength-dependent optical-depth threshold in a continuously varying gas; the "surface" seen at one wavelength can be physically deeper or shallower than the "surface" seen at another.',
        activity='Given that optical depth in a stellar line core is much larger than in the nearby continuum, predict qualitatively whether the line-forming layer is hotter or cooler than the continuum-forming layer, and hence why absorption lines appear dark rather than bright, for a star whose temperature decreases outward.',
        lab_connection='Lab 02 computes optical depth and transmitted fraction for a simple two-wavelength model atmosphere and connects the result to a real curve-of-growth argument for line strength.',
        synthesis='Optical depth, not physical distance, is the natural variable for radiative transfer; a stellar photosphere is best understood as the depth from which photons of a given wavelength typically last scatter or are absorbed before escaping, \u03c4 \u2248 1.',
        openstax='OpenStax Astronomy 2e, Chapter 5.5 (spectroscopy) touches line formation qualitatively; this course develops the optical-depth formalism that OpenStax\u2019s introductory treatment omits.',
    ),
    dict(
        n=4, title='Why Spectral Lines Look the Way They Do: The Boltzmann and Saha Equations',
        subtitle='Turning "OBAFGKM" into a quantitative, temperature-driven population problem',
        goals=[
            'Apply the Boltzmann equation to compute the relative population of two atomic energy levels at a given temperature.',
            'Explain qualitatively how the Saha equation extends this to ionization states, and why hydrogen Balmer lines peak near spectral type A.',
            'Connect these microphysical population equations to the macroscopic spectral classification introduced in ASTR 230.',
        ],
        why_matters='ASTR 230 explained the non-monotonic strength of Balmer lines across spectral type qualitatively, as a competition between excitation and ionization. This lecture makes that competition quantitative: the Boltzmann and Saha equations are the actual statistical-mechanics tools astronomers use to convert a measured line strength into a precise temperature, and they underlie every stellar-atmosphere model used in modern astrophysics.',
        phenomenon='Two stars can have almost the same total hydrogen abundance (essentially all stars do) yet dramatically different Balmer line strengths, because the fraction of hydrogen atoms with an electron in the first excited state (n=2, required to produce a Balmer absorption line) depends exponentially on temperature through the Boltzmann factor.',
        vocab=['Boltzmann equation', 'excitation temperature', 'statistical weight', 'Saha equation', 'ionization fraction', 'partition function'],
        evidence=[
            'The Boltzmann equation predicts that the ratio of atoms in an excited state to the ground state rises steeply (exponentially) with temperature, exactly matching the observed steep rise in Balmer-line strength from cool M stars toward intermediate A stars.',
            'The Saha equation predicts that above roughly 10,000 K, hydrogen becomes predominantly ionized, removing the bound electron needed for any Balmer transition \u2014 exactly matching the observed decline in Balmer-line strength from A stars toward the hottest O and B stars.',
            'Combining both equations correctly predicts the observed peak of Balmer-line strength near spectral type A0 (T_eff \u2248 9,000-10,000 K), a result that neither equation alone can explain.',
        ],
        model=[
            'The Boltzmann equation gives the ratio of the number of atoms in excited state 2 to state 1 as n2/n1 = (g2/g1) e^{-(E2-E1)/kT}, where g is the statistical weight (degeneracy) of each level; higher T always increases the population of the higher level relative to the lower one.',
            'The Saha equation gives the ratio of ionized to neutral atom number densities as a function of T and electron density, with an exponential dependence on the ionization energy divided by kT, analogous in form to the Boltzmann equation but for a continuum (free-electron) final state rather than a discrete bound level.',
            'Balmer-line strength is proportional to the number of neutral hydrogen atoms in the n=2 state, which is the product of (fraction neutral, from Saha) and (fraction of neutral atoms in n=2, from Boltzmann); this product is non-monotonic in T because the two factors move in opposite directions as T rises.',
        ],
        equation=r'\dfrac{n_2}{n_1} = \dfrac{g_2}{g_1}\,e^{-(E_2-E_1)/kT}, \qquad \dfrac{n_{i+1}}{n_i} \propto T^{3/2} e^{-\chi_i/kT}\ \ (\text{Saha, schematic form})',
        example=[
            f'Boltzmann ratio for hydrogen n=2 relative to n=1 (E2 - E1 = 10.2 eV = 1.634e-18 J, g2/g1 = 4): at T = 5,750 K (near the Sun and Alpha Centauri A/B), kT = {K_BOLTZMANN*5750:.3e} J, giving n2/n1 = 4 \u00d7 exp(-{1.634e-18/(K_BOLTZMANN*5750):.1f}) = {4*math.exp(-1.634e-18/(K_BOLTZMANN*5750)):.3e} \u2014 an extremely small fraction of atoms are excited, so Balmer lines are intrinsically weak in G/K stars like the Sun and Alpha Centauri A and B.',
            f'At T = 9,900 K (near Vega/Sirius A, spectral type A): kT = {K_BOLTZMANN*9900:.3e} J, giving n2/n1 = 4 \u00d7 exp(-{1.634e-18/(K_BOLTZMANN*9900):.2f}) = {4*math.exp(-1.634e-18/(K_BOLTZMANN*9900)):.3e} \u2014 roughly {(4*math.exp(-1.634e-18/(K_BOLTZMANN*9900)))/(4*math.exp(-1.634e-18/(K_BOLTZMANN*5750))):.0f} times larger than at 5,750 K, consistent with the much stronger observed Balmer lines in A-type stars.',
            'At still higher temperatures (O and B stars), the Saha equation predicts the neutral-hydrogen fraction itself collapses toward zero as hydrogen ionizes, so even though the Boltzmann n2/n1 ratio keeps rising, there are too few neutral atoms left to produce strong Balmer absorption \u2014 reproducing the observed turnover.',
        ],
        pitfall='Using the Boltzmann equation alone to explain the full OBAFGKM Balmer-strength sequence. The Boltzmann equation alone predicts monotonically increasing line strength with temperature; only combining it with the Saha equation\u2019s ionization turnover reproduces the observed peak at spectral type A.',
        activity='Using only the sign of the exponent in each equation, explain in words (no calculation needed) why raising temperature always increases excitation (Boltzmann) but can either increase or asymptotically saturate ionization (Saha) depending on how close the gas already is to fully ionized.',
        lab_connection='Lab 02 computes the Boltzmann excitation ratio for hydrogen across a range of stellar temperatures and reproduces the qualitative OBAFGKM Balmer-strength curve from ASTR 230 quantitatively.',
        synthesis='The Boltzmann and Saha equations, taken together, convert the qualitative OBAFGKM spectral sequence into a quantitative, first-principles prediction for exactly how strong a given absorption line should be at a given temperature.',
        openstax='OpenStax Astronomy 2e, Chapter 5.5 (formation of spectral lines) and Chapter 17.3 (spectral types); this course adds the Boltzmann/Saha formalism omitted at the introductory level.',
    ),
    dict(
        n=5, title='Hydrostatic Equilibrium: What Holds a Star Up',
        subtitle='Deriving, not asserting, the balance between pressure and gravity',
        goals=[
            'Derive the equation of hydrostatic equilibrium from a force balance on a thin spherical shell of stellar gas.',
            'Use the equation to obtain an order-of-magnitude estimate of a star\u2019s central pressure from its mass and radius alone.',
            'Explain why hydrostatic equilibrium, not fusion, is the immediate reason a star does not collapse or explode on human timescales.',
        ],
        why_matters='ASTR 230 stated hydrostatic equilibrium as a one-line description. This course derives it as a force-balance equation and uses it quantitatively, which is what makes it possible to build an actual (if approximate) stellar interior model rather than just asserting that "pressure balances gravity."',
        phenomenon=f'The Sun has neither collapsed under its own gravity nor blown itself apart in the roughly 4.6 billion years since it reached the main sequence, despite having no rigid structure at all \u2014 every layer of solar gas is in force balance to a precision of better than one part in a million at any instant, or the Sun would visibly expand or contract on short timescales.',
        vocab=['hydrostatic equilibrium', 'pressure gradient', 'gravitational acceleration', 'mean molecular weight', 'ideal gas law', 'polytrope'],
        evidence=[
            'Helioseismology (analysis of the Sun\u2019s natural oscillation modes) directly measures the Sun\u2019s internal pressure, density, and sound-speed profile, and finds it consistent with standard hydrostatic solar models to a precision of much better than 1%.',
            'No star has ever been observed to visibly expand or contract on a dynamical (free-fall) timescale while on the main sequence, exactly as expected if hydrostatic equilibrium holds at every radius.',
            'Stars of very different mass (and hence very different central pressure and temperature, by this lecture\u2019s scaling) show a continuous, orderly main sequence in the Hertzsprung-Russell diagram rather than a discontinuous jump, consistent with hydrostatic equilibrium applying smoothly across the full mass range.',
        ],
        model=[
            'Consider a thin spherical shell of gas at radius r, thickness dr, and density \u03c1(r) inside a star. The net outward force from the pressure difference across the shell must exactly balance the inward gravitational force from all the mass interior to r.',
            'Writing this force balance per unit volume gives the hydrostatic equilibrium equation dP/dr = -G M(r) \u03c1(r) / r\u00b2, where M(r) is the mass enclosed within radius r; the pressure must therefore decrease outward everywhere inside a star in equilibrium.',
            'Combining this with the ideal gas law P = (\u03c1 k T)/(\u03bc m_p) links pressure, density, and temperature, so hydrostatic equilibrium alone (without yet invoking energy transport or generation) already constrains how P, \u03c1, and T must vary together inside a star.',
        ],
        equation=r'\dfrac{dP}{dr} = -\dfrac{G M(r)\,\rho(r)}{r^{2}}, \qquad P_c \sim \dfrac{3}{8\pi}\dfrac{GM^{2}}{R^{4}}\ \ (\text{uniform-density estimate})',
        example=[
            f'Order-of-magnitude central pressure of the Sun from P_c \u2248 (3/8\u03c0) GM\u00b2/R\u2074: M = {M_SUN_KG:.3e} kg, R = {R_SUN_M:.3e} m, giving P_c \u2248 {SUN_CENTRAL_PRESSURE_EST:.3e} Pa.',
            f'A detailed standard solar model gives a central pressure of about {SUN_CENTRAL_PRESSURE_PUBLISHED:.3e} Pa (a standard published solar-interior value, not independently re-verified this session); the simple uniform-density estimate above is within a factor of {SUN_CENTRAL_PRESSURE_PUBLISHED/SUN_CENTRAL_PRESSURE_EST:.1f} of the full numerical solution, which is the expected level of agreement for a one-line order-of-magnitude estimate that ignores the Sun\u2019s actual (strongly centrally concentrated) density profile.',
            f'For comparison, sea-level atmospheric pressure on Earth is only about 1.0 \u00d7 10\u2075 Pa: the Sun\u2019s central pressure exceeds it by a factor of roughly {SUN_CENTRAL_PRESSURE_EST/1.0e5:.2e}, illustrating just how large the gravitational confinement of a star\u2019s own mass really is.',
        ],
        pitfall='Treating the uniform-density estimate P_c \u2248 (3/8\u03c0)GM\u00b2/R\u2074 as an exact stellar-interior result. It is exact only for a strictly uniform-density sphere, which no real star is; real stars are strongly centrally concentrated, so full numerical integration of the hydrostatic equation with a realistic density profile is needed for precision work, as this lecture\u2019s comparison to the standard solar model shows.',
        activity='Using dP/dr = -GM(r)\u03c1(r)/r\u00b2, explain in words why the pressure gradient must be steepest (most negative) near the stellar center, where M(r) and \u03c1(r) are both largest relative to r.',
        lab_connection='Lab 03 numerically integrates a simplified hydrostatic-equilibrium model for the Sun and compares the resulting central pressure estimate to the published standard solar model value used in this lecture.',
        synthesis='Hydrostatic equilibrium is a force-balance equation, dP/dr = -GM(r)\u03c1(r)/r\u00b2, not merely a qualitative statement, and even a crude uniform-density estimate from it reproduces a star\u2019s central pressure to the correct order of magnitude.',
        openstax='OpenStax Astronomy 2e, Chapter 15.4-15.5 (the Sun\u2019s interior, energy transport); this course derives the governing equation that OpenStax states only descriptively.',
    ),
    dict(
        n=6, title='The Virial Theorem: Gravity, Kinetic Energy, and Self-Gravitating Systems',
        subtitle='One theorem, from stellar cores to star clusters',
        goals=[
            'Derive the scalar virial theorem (2K + U = 0 in equilibrium) for a self-gravitating system from the time derivative of the moment of inertia.',
            'Apply the virial theorem to estimate a star\u2019s central temperature from its mass and radius.',
            'Apply the same theorem to estimate a star cluster\u2019s total mass from its velocity dispersion and size.',
        ],
        why_matters='The virial theorem is one of the few results in astrophysics that applies essentially unchanged across more than twenty orders of magnitude in size, from the interior of a single star (Lecture 05\u2019s hydrostatic equilibrium is, in fact, a special case of it) to galaxy clusters. It is also the tool Fritz Zwicky used in 1933 to make the first case for dark matter, from the motions of galaxies in the Coma Cluster.',
        phenomenon=f'A star cluster with measured stellar velocities and a measured physical size can have its total mass estimated purely from those two numbers and Newtonian gravity, with no need to see or count individual faint stars \u2014 exactly the same logic (from a very different physical system) as the Milky Way rotation-curve mass estimate in ASTR 230.',
        vocab=['virial theorem', 'kinetic energy (bulk/thermal)', 'gravitational potential energy', 'velocity dispersion', 'half-light radius', 'moment of inertia'],
        evidence=[
            'Detailed numerical stellar-structure models, which solve the full hydrostatic-equilibrium equation with a realistic (centrally concentrated) density profile, produce central temperatures a few times higher than the simple uniform-density virial estimate derived in this lecture, confirming the estimate captures the right physical mechanism and order of magnitude even though the uniform-density assumption systematically undershoots the true central value.',
            'Globular cluster masses estimated from the virial theorem (using measured stellar velocity dispersions and half-light radii) are broadly consistent with independent dynamical and stellar-population mass estimates for the same clusters.',
            'Zwicky\u2019s original 1933 application of the virial theorem to the Coma Cluster\u2019s galaxy velocities gave a mass far exceeding the visible galaxy mass, the historical origin of the dark matter problem revisited in ASTR 230.',
        ],
        model=[
            'For a system in a steady state, the second time derivative of its moment of inertia is zero; working through the mechanics of this condition for a self-gravitating system of total kinetic energy K and total gravitational potential energy U yields the scalar virial theorem, 2K + U = 0.',
            'For a uniform self-gravitating sphere of mass M and radius R, U = -3GM\u00b2/(5R); setting the thermal kinetic energy (3/2)NkT (with N = M/(\u03bc m_p) particles) equal to -U/2 gives an estimate of the mean/central temperature required for virial (hydrostatic) balance.',
            'For a star cluster, replacing thermal kinetic energy with bulk kinetic energy from the observed stellar velocity dispersion \u03c3 gives a standard virial mass estimator, M \u2248 5\u03c3\u00b2R_h/G, widely used to weigh star clusters from purely kinematic and size measurements.',
        ],
        equation=r'2K + U = 0, \qquad T \sim \dfrac{\mu m_p G M}{5 k R}\ (\text{star}), \qquad M \approx \dfrac{5\sigma^{2}R_h}{G}\ (\text{cluster})',
        example=[
            f'Virial central-temperature estimate for the Sun: T \u2248 \u03bc m_p GM/(5kR) with \u03bc = 0.5 (ionized hydrogen), M = {M_SUN_KG:.3e} kg, R = {R_SUN_M:.3e} m, giving T \u2248 {SUN_VIRIAL_TEMP_EST:.3e} K.',
            f'The standard solar model gives a central temperature of about {SUN_CORE_TEMP_PUBLISHED:.3e} K (published, not independently re-verified this session); the virial estimate undershoots this by a factor of {SUN_CORE_TEMP_PUBLISHED/SUN_VIRIAL_TEMP_EST:.1f}, a genuine (not merely apparent) limitation of the uniform-density assumption: because a real star\u2019s density is strongly centrally concentrated rather than uniform, its true central temperature is substantially higher than the volume-averaged estimate this one-line argument actually computes.',
            f'Globular cluster M15: velocity dispersion \u03c3 \u2248 {M15_SIGMA_KMS:.1f} km/s, half-light radius R_h \u2248 {M15_HALF_LIGHT_PC:.1f} pc (standard published values, flagged for spot-check). Virial mass M \u2248 5\u03c3\u00b2R_h/G = {M15_VIRIAL_MASS_EST:.2e} M\u2609, consistent in order of magnitude with the commonly cited dynamical mass of M15, about {M15_PUBLISHED_MASS_MSUN:.1e} M\u2609.',
        ],
        pitfall='Applying the virial theorem to a system that is not actually in a steady state (e.g., a cluster caught in the middle of a merger, or a star undergoing rapid gravitational collapse). The virial theorem assumes d\u00b2I/dt\u00b2 = 0; systems that are still dynamically evolving can have virial-theorem-based mass or temperature estimates that are systematically wrong.',
        activity='Using M \u2248 5\u03c3\u00b2R_h/G, predict qualitatively how the inferred cluster mass changes if the measured velocity dispersion \u03c3 is doubled while R_h stays fixed, and explain why this makes velocity-dispersion measurement precision so important for cluster mass estimates.',
        lab_connection='Lab 03 pairs the hydrostatic central-pressure estimate (Lecture 05) with this lecture\u2019s virial central-temperature and cluster-mass estimators, applied to the Sun and to M15 respectively.',
        synthesis='The virial theorem (2K + U = 0) is a single, general consequence of gravitational equilibrium that reproduces both a star\u2019s central temperature and a star cluster\u2019s total mass from otherwise very different observable inputs.',
        openstax='OpenStax Astronomy 2e does not present the virial theorem explicitly at the introductory level; this course develops it directly from Newtonian mechanics, connecting to Chapter 15 (solar interior) and the cluster-dynamics discussion in Chapter 25.',
    ),
    dict(
        n=7, title='Gravitational Potentials: The Shell Theorem, Potential Energy, and Escape Velocity',
        subtitle='Building the gravity toolkit needed for orbital mechanics',
        goals=[
            'State and justify the shell theorem for the gravitational field of a spherically symmetric mass distribution.',
            'Derive the gravitational potential energy of a two-body system and the escape-velocity formula from energy conservation.',
            'Compare escape velocities from very different real objects to build physical intuition for compact-object gravity.',
        ],
        why_matters='Every orbital-mechanics result in the rest of this course (Kepler\u2019s laws, binary-star mass determination, tidal effects, orbital energy) rests on two facts established here: that a spherical mass acts gravitationally, from outside its surface, exactly like a point mass at its center, and that gravitational potential energy provides a clean energy-conservation route to escape velocity and orbital speed.',
        phenomenon=f'Sirius B, a white dwarf with about {SIRIUS_B["mass_msun"]:.2f} times the Sun\u2019s mass compressed into roughly Earth\u2019s radius (from ASTR 230), has a surface escape velocity of {SIRIUS_B_ESCAPE_KMS:.0f} km/s \u2014 more than {SIRIUS_B_ESCAPE_KMS/EARTH_ESCAPE_KMS:.0f} times Earth\u2019s escape velocity, despite Sirius B\u2019s mass being only about {SIRIUS_B["mass_msun"]/(EARTH_MASS_KG/M_SUN_KG):.0f} times larger than Earth\u2019s.',
        vocab=['shell theorem', 'gravitational potential energy', 'escape velocity', 'specific orbital energy', 'gravitational binding energy', 'point-mass equivalence'],
        evidence=[
            'Spacecraft trajectories computed by treating Earth, the Sun, and other planets as point masses located at their centers match tracked spacecraft positions to extraordinary precision, confirming the shell theorem\u2019s prediction for the external field of a (nearly) spherical body.',
            'Objects launched from Earth at speeds below about 11.2 km/s fall back or remain in orbit, while objects at or above that speed escape Earth\u2019s gravity entirely (ignoring atmospheric drag), exactly matching the escape-velocity formula derived from energy conservation.',
            'Compact objects (white dwarfs, neutron stars) show escape velocities dramatically higher than main-sequence stars of similar mass, consistent with escape velocity\u2019s 1/\u221aR dependence on radius at fixed mass.',
        ],
        model=[
            'The shell theorem states that a spherically symmetric shell of mass exerts zero net gravitational field on any point mass inside it, and exerts the same field outside itself as if all its mass were concentrated at its center; integrating over concentric shells extends this to any spherically symmetric mass distribution.',
            'The gravitational potential energy of two point masses (or spherical bodies) separated by distance r is U(r) = -GMm/r, defined so that U \u2192 0 as r \u2192 \u221e; because U is negative and grows toward zero with increasing separation, it takes positive energy input to increase r.',
            'Escape velocity is the minimum launch speed for which total mechanical energy (1/2)mv\u00b2 + U(r) is exactly zero, i.e., just enough kinetic energy to reach r \u2192 \u221e with zero speed remaining; solving this for v gives v_esc = \u221a(2GM/R).',
        ],
        equation=r'U(r) = -\dfrac{GMm}{r}, \qquad \tfrac{1}{2}mv_{\rm esc}^{2} + U(R) = 0 \implies v_{\rm esc} = \sqrt{\dfrac{2GM}{R}}',
        example=[
            f'Earth: M = {EARTH_MASS_KG:.3e} kg, R = {EARTH_RADIUS_M:.3e} m, v_esc = \u221a(2GM/R) = {EARTH_ESCAPE_KMS:.2f} km/s.',
            f'The Sun: M = {M_SUN_KG:.3e} kg, R = {R_SUN_M:.3e} m, v_esc = {SUN_ESCAPE_KMS:.1f} km/s \u2014 about {SUN_ESCAPE_KMS/EARTH_ESCAPE_KMS:.0f} times Earth\u2019s escape velocity, driven by the Sun\u2019s much larger mass despite its also much larger radius.',
            f'Sirius B (white dwarf, from ASTR 230, provenance already established there): M = {SIRIUS_B["mass_msun"]:.3f} M\u2609, R = {SIRIUS_B["radius_rsun"]:.6f} R\u2609, v_esc = {SIRIUS_B_ESCAPE_KMS:.0f} km/s, illustrating how escape velocity is far more sensitive to an object\u2019s radius (through 1/\u221aR) than to its mass, when comparing objects of similar mass but wildly different compactness.',
        ],
        pitfall='Assuming escape velocity means "the speed needed to permanently leave the object\u2019s gravitational influence entirely" in some absolute sense. Gravity from any mass technically extends to infinite distance (falling only as 1/r\u00b2); escape velocity is instead the minimum speed to reach arbitrarily large distance with zero kinetic energy remaining, in the idealized two-body problem with no other masses present.',
        activity='Using v_esc = \u221a(2GM/R), predict qualitatively what happens to the escape velocity of a fixed-mass object if it is compressed to one-tenth its original radius, and connect this to why compact objects (white dwarfs, neutron stars, black holes) have such extreme escape velocities.',
        lab_connection='Lab 04 uses the point-mass equivalence (shell theorem) implicitly when treating Alpha Centauri A and B as point masses for their mutual orbit, and computes escape velocities for both stars for comparison.',
        synthesis='The shell theorem justifies treating spherical stars as point masses for orbital purposes, and gravitational potential energy converts the qualitative idea of "escaping gravity" into the precise, testable escape-velocity formula used throughout the rest of this course.',
        openstax='OpenStax Astronomy 2e, Chapter 3.3-3.5 (Newton\u2019s law of gravitation, orbits, motions of satellites); this course adds the shell-theorem justification and the energy-conservation derivation of escape velocity.',
    ),
    dict(
        n=8, title='The Two-Body Problem: Deriving Kepler\u2019s Laws from Newtonian Gravity',
        subtitle='From an inverse-square force to an ellipse',
        goals=[
            'Reduce the general two-body gravitational problem to an equivalent one-body problem using the reduced mass.',
            'State (without full variational derivation) why an inverse-square central force produces a closed elliptical orbit, and derive the generalized form of Kepler\u2019s third law.',
            'Apply the generalized Kepler\u2019s third law to a real, precisely measured binary star system and cross-check the result against independently measured masses.',
        ],
        why_matters='Kepler\u2019s three laws were originally empirical fits to Tycho Brahe\u2019s planetary position data. Newton\u2019s achievement was to show they follow necessarily from an inverse-square gravitational force law applied to any two bodies, not just the Sun and a planet \u2014 which is exactly what makes the same mathematics apply, unchanged, to binary stars, moons, and artificial satellites.',
        phenomenon=f'Alpha Centauri A and B, live-verified this session via a direct fetch of their measured orbital elements, orbit their common center of mass with a period of {ALPHA_CEN_ORBIT["period_yr"]:.3f} years and a semimajor axis of {ALPHA_CEN_ORBIT["semimajor_au"]:.3f} AU \u2014 numbers measured purely from the stars\u2019 positions on the sky over decades, with no direct measurement of either star\u2019s mass.',
        vocab=['reduced mass', 'two-body problem', 'relative orbit', 'semimajor axis', 'orbital eccentricity', 'generalized Kepler\u2019s third law'],
        evidence=[
            'Every planet in the solar system, every known binary star system, and every artificial satellite obeys the same generalized form of Kepler\u2019s third law once both orbiting masses (not just the Sun\u2019s) are included, confirming its origin in Newtonian gravity rather than any property special to planets.',
            'Binary star systems with orbits precisely measured over decades (as Alpha Centauri AB has been since Jean Richaud\u2019s recognition of its binary nature in 1689) provide a purely gravitational, model-independent measurement of the sum of both stars\u2019 masses, entirely independent of any stellar-structure or spectral assumptions.',
            'The total mass obtained from applying Kepler\u2019s third law to Alpha Centauri AB\u2019s orbit agrees with the sum of the two stars\u2019 individually measured masses (from independent interferometric and asteroseismic methods) to high precision, cross-validating two completely different measurement techniques.',
        ],
        model=[
            'The full two-body problem (two masses m1 and m2 orbiting their mutual center of mass under their mutual gravity) can be reduced exactly to an equivalent one-body problem: a fictitious particle of reduced mass \u03bc = m1m2/(m1+m2) orbiting a fixed center under the combined mass M = m1+m2, at the actual relative separation r between the two bodies.',
            'Solving the resulting one-body problem for an inverse-square force shows the orbit is a conic section (an ellipse, for a bound orbit) with the total mass M at one focus, which is Kepler\u2019s first law, now derived rather than merely observed.',
            'Applying Newton\u2019s second law to the reduced one-body problem for a circular orbit (or, more generally, integrating the full elliptical solution) yields the generalized Kepler\u2019s third law, P\u00b2 = 4\u03c0\u00b2a\u00b3/[G(m1+m2)], which reduces to the Sun-planet form only when m1 >> m2.',
        ],
        equation=r'\mu = \dfrac{m_1 m_2}{m_1+m_2}, \qquad P^{2} = \dfrac{4\pi^{2}a^{3}}{G\,(m_1+m_2)}',
        example=[
            f'Alpha Centauri AB: P = {ALPHA_CEN_ORBIT["period_yr"]:.3f} yr = {ALPHA_CEN_ORBIT["period_yr"]*YEAR_S:.4e} s, a = {ALPHA_CEN_ORBIT["semimajor_au"]:.3f} AU = {ALPHA_CEN_ORBIT["semimajor_au"]*AU_M:.4e} m.',
            f'Solving Kepler\u2019s third law for the total mass: (m1+m2) = 4\u03c0\u00b2a\u00b3/(GP\u00b2) = {ALPHA_CEN_TOTAL_MASS_KEPLER:.4f} M\u2609.',
            f'Independently measured individual masses (interferometry + asteroseismology): M_A = {ALPHA_CEN_A["mass_msun"]:.4f} M\u2609, M_B = {ALPHA_CEN_B["mass_msun"]:.4f} M\u2609, summing to {ALPHA_CEN_TOTAL_MASS_MEASURED:.4f} M\u2609.',
            f'Agreement between the orbit-based (Kepler) total mass and the independently measured sum: {abs(ALPHA_CEN_TOTAL_MASS_KEPLER-ALPHA_CEN_TOTAL_MASS_MEASURED)/ALPHA_CEN_TOTAL_MASS_MEASURED*100:.2f}% \u2014 two completely independent techniques (pure celestial mechanics versus interferometric radius/asteroseismic mass modeling) agree to well within their combined measurement uncertainties, directly confirming Newtonian gravity\u2019s two-body prediction for a real system.',
        ],
        pitfall='Applying the Sun-planet form of Kepler\u2019s third law (P\u00b2 = a\u00b3, in years and AU) to a binary star system without including both masses. That simplified form silently assumes m2 << m1 (true for a planet around the Sun, false for two comparable-mass stars); using it for Alpha Centauri AB would give a total mass of exactly 1 M\u2609, badly wrong compared to the correct value of about 2 M\u2609.',
        activity='Using P\u00b2 = 4\u03c0\u00b2a\u00b3/[G(m1+m2)], predict qualitatively how the inferred total mass changes if the same angular orbit is observed at twice the true distance (so that the true physical semimajor axis a is twice as large for the same measured period), and explain why an accurate distance measurement is essential for binary-star mass determination.',
        lab_connection='Lab 04 reproduces this lecture\u2019s Alpha Centauri AB mass determination in full, including a propagated-uncertainty discussion for the measured period, semimajor axis, and parallax.',
        synthesis='Kepler\u2019s laws are not independent postulates but necessary consequences of Newtonian gravity applied to the reduced two-body problem, and the generalized third law converts a purely geometric/temporal orbit measurement into a dynamical mass measurement, verified here against an independent method for a real star system.',
        openstax='OpenStax Astronomy 2e, Chapter 3.1-3.2 (Kepler\u2019s laws, Newton\u2019s great synthesis); this course derives the reduced-mass formalism and the generalized third law that OpenStax presents only in the Sun-planet limit.',
    ),
    dict(
        n=9, title='Weighing Binary Stars: Visual, Spectroscopic, and Eclipsing Methods',
        subtitle='Binary stars as astronomy\u2019s primary source of stellar masses',
        goals=[
            'Explain how a visual binary\u2019s astrometric orbit yields both the total mass (Kepler\u2019s third law) and, with center-of-mass data, the individual masses.',
            'Describe how the radial-velocity method extracts orbital and mass information from spectroscopic binaries, including the sin(i) ambiguity.',
            'Explain why eclipsing binaries are uniquely valuable for removing the inclination ambiguity and obtaining absolute radii as well as masses.',
        ],
        why_matters='Every stellar mass quoted in this course (and in ASTR 230) ultimately traces back to a binary-star measurement of one of the three types developed here; single, isolated stars provide no direct dynamical mass measurement at all. Binary stars are, in a very real sense, the scale on which the entire mass axis of stellar astrophysics is calibrated.',
        phenomenon=f'Alpha Centauri AB\u2019s individual masses (M_A = {ALPHA_CEN_A["mass_msun"]:.4f} M\u2609, M_B = {ALPHA_CEN_B["mass_msun"]:.4f} M\u2609) were not measured by any single technique; they combine the total mass from the visual/astrometric orbit (Lecture 08) with the mass ratio inferred from how far each star moves relative to the system\u2019s center of mass, illustrating how binary-mass determination typically combines multiple lines of evidence.',
        vocab=['visual binary', 'spectroscopic binary', 'eclipsing binary', 'radial velocity curve', 'mass function', 'orbital inclination'],
        evidence=[
            'Visual binaries (both stars individually resolved, as with Alpha Centauri AB) provide the full relative orbit directly from repeated astrometric measurements, plus the individual mass ratio from each star\u2019s separate motion about the shared center of mass.',
            'Spectroscopic binaries (unresolved, but showing periodic Doppler shifts in one or both stars\u2019 spectral lines) give a radial-velocity curve; because only the line-of-sight velocity component is measured, the derived masses carry an unavoidable sin(i) ambiguity unless the inclination i is independently known.',
            'Eclipsing binaries (whose orbital plane happens to lie nearly along our line of sight) show periodic dips in combined brightness as one star passes in front of the other; because eclipses require i \u2248 90\u00b0, they remove the sin(i) ambiguity and additionally yield both stars\u2019 absolute radii from the eclipse durations.',
        ],
        model=[
            'For a visual binary with a fully resolved relative orbit, Kepler\u2019s third law (Lecture 08) gives the total mass; if each star\u2019s individual displacement from the system\u2019s center of mass is also measured, the mass ratio m1/m2 = a2/a1 (inversely proportional to each star\u2019s distance from the barycenter) splits the total mass into individual masses.',
            'For a spectroscopic binary, the observed radial-velocity semi-amplitude K depends on the true orbital speed times sin(i); the derived "mass function" therefore only constrains a combination of masses and sin(i), not the individual masses, unless the inclination is broken by an independent method (e.g., eclipses, or astrometry).',
            'For an eclipsing, double-lined spectroscopic binary (both stars\u2019 lines visible and eclipses observed), the combination of radial-velocity curves (giving masses, with i fixed near 90\u00b0 by the eclipses) and eclipse light-curve timing (giving radii) yields precise, nearly assumption-free masses and radii for both stars \u2014 the single most reliable source of fundamental stellar parameters in all of astrophysics.',
        ],
        equation=r'\dfrac{m_1}{m_2} = \dfrac{a_2}{a_1}\ (\text{visual}), \qquad f(m_1,m_2,i) = \dfrac{(m_2\sin i)^{3}}{(m_1+m_2)^{2}} = \dfrac{P K_1^{3}}{2\pi G}\ (\text{spectroscopic, schematic})',
        example=[
            f'Alpha Centauri AB total mass from Kepler\u2019s third law (Lecture 08): {ALPHA_CEN_TOTAL_MASS_KEPLER:.4f} M\u2609.',
            f'Independently measured mass ratio (from astrometry combined with modeling): M_B/M_A = {ALPHA_CEN_B["mass_msun"]/ALPHA_CEN_A["mass_msun"]:.4f}.',
            f'Splitting the Kepler total mass using this ratio: M_A = total/(1 + M_B/M_A) = {ALPHA_CEN_TOTAL_MASS_KEPLER/(1+ALPHA_CEN_B["mass_msun"]/ALPHA_CEN_A["mass_msun"]):.4f} M\u2609, M_B = {ALPHA_CEN_TOTAL_MASS_KEPLER - ALPHA_CEN_TOTAL_MASS_KEPLER/(1+ALPHA_CEN_B["mass_msun"]/ALPHA_CEN_A["mass_msun"]):.4f} M\u2609, matching the independently quoted individual masses ({ALPHA_CEN_A["mass_msun"]:.4f} and {ALPHA_CEN_B["mass_msun"]:.4f} M\u2609) to within rounding, since the mass ratio used here was itself derived consistently with those values.',
            'For an eclipsing, double-lined spectroscopic binary with measured radial-velocity semi-amplitudes K1 and K2 and eclipse-confirmed i \u2248 90\u00b0, the individual masses follow directly (no sin\u00b3i ambiguity) from m1 sin\u00b3i and m2 sin\u00b3i \u2248 m1 and m2 \u2014 the method underlying the great majority of precisely measured stellar masses used to calibrate the mass-luminosity relation in ASTR 230.',
        ],
        pitfall='Treating a single-lined spectroscopic binary\u2019s mass function as a measured mass. Without an independently known inclination (or a visible second set of spectral lines), the mass function only gives a lower limit / degenerate combination of the companion mass and sin(i); this is exactly the ambiguity that made many early radial-velocity exoplanet "minimum masses" (m sin i) rather than true masses.',
        activity='Given a spectroscopic binary with unusually large radial-velocity amplitude but no observed eclipses, explain what additional information would be needed to determine whether the system is a low-inclination binary with large true masses, or a high-inclination binary with smaller true masses.',
        lab_connection='Lab 05 extends this lecture\u2019s mass-ratio splitting technique to a worked radial-velocity mass-function scenario, making the sin(i) ambiguity concrete with numbers.',
        synthesis='Binary stars provide the only direct, model-independent measurements of stellar mass in astrophysics, with visual, spectroscopic, and eclipsing binaries each contributing a different, complementary piece of the full orbital and physical picture.',
        openstax='OpenStax Astronomy 2e, Chapter 18.4-18.5 (binary star systems, using binary systems to measure stellar masses); this course adds the reduced-mass/inclination formalism connecting directly to Lecture 08\u2019s derivation.',
    ),
    dict(
        n=10, title='Tidal Forces and the Roche Limit',
        subtitle='Why gravity can stretch, and even destroy, extended bodies',
        goals=[
            'Derive the differential (tidal) acceleration across an extended body from a first-order expansion of the gravitational field.',
            'Derive the Roche limit as the distance at which tidal forces would overcome a satellite\u2019s self-gravity.',
            'Apply both results to real solar-system examples: the Earth-Moon system and Io\u2019s tidally driven volcanism.',
        ],
        why_matters='Every topic so far in this course has treated orbiting bodies as point masses. Tidal forces are what remain once we account for a body\u2019s finite size, and they explain phenomena with no point-mass analog at all: ocean tides, tidal locking, the rings of Saturn, and some of the most volcanically active worlds in the solar system.',
        phenomenon=f'Io, Jupiter\u2019s innermost large moon, is the most volcanically active body in the solar system, with heat output far exceeding what radioactive decay alone could supply \u2014 the excess energy comes from tidal flexing driven by Jupiter\u2019s gravity combined with Io\u2019s slightly eccentric orbit (e = {IO_ECCENTRICITY:.4f}, standard published value), which is continually forced by an orbital resonance with Europa and Ganymede.',
        vocab=['tidal acceleration', 'tidal bulge', 'Roche limit', 'tidal locking', 'orbital resonance', 'tidal heating'],
        evidence=[
            'Ocean tides on Earth are measurably higher at new and full Moon (when the Sun\u2019s and Moon\u2019s tidal effects align) than at first/last quarter (when they partially cancel), directly confirming that tides are a differential, not uniform, gravitational effect.',
            'Saturn\u2019s rings lie almost entirely within the Roche limit computed for icy ring-particle material, while its larger, more distant moons (well outside the Roche limit) remain intact, consistent with the Roche-limit prediction for where self-gravity can versus cannot resist tidal disruption.',
            'Io\u2019s measured internal heat flow substantially exceeds the radiogenic heating expected for a body of its size and composition, matching the predicted tidal-heating rate from its forced orbital eccentricity in the Laplace resonance with Europa and Ganymede.',
        ],
        model=[
            'Tidal acceleration arises because the gravitational pull of a companion body differs slightly between the near side and far side of an extended body; expanding the gravitational acceleration to first order in the body\u2019s radius r about its center gives a differential (tidal) acceleration \u0394a \u2248 2GMr/d\u00b3, stretching the body along the line joining the two centers.',
            'The Roche limit is the orbital distance at which this tidal stretching force on a self-gravitating satellite exactly equals the satellite\u2019s own self-gravity holding it together; inside this distance, a satellite held together only by gravity (with no internal strength) is torn apart.',
            'A moon on a slightly eccentric orbit experiences a tidal bulge that is continuously flexed as the tidal force strength and orientation change around the orbit; this flexing dissipates orbital energy as internal heat, provided some mechanism (such as an orbital resonance) prevents the eccentricity from simply damping to zero.',
        ],
        equation=r'\Delta a \approx \dfrac{2GMr}{d^{3}}, \qquad d_{\rm Roche} = R_{\rm primary}\left(\dfrac{2\rho_{\rm primary}}{\rho_{\rm satellite}}\right)^{1/3}',
        example=[
            f'Earth-Moon Roche limit (rigid-body estimate): Earth mean density {EARTH_DENSITY:.0f} kg/m\u00b3, Moon mean density {MOON_DENSITY:.0f} kg/m\u00b3, giving d_Roche \u2248 {EARTH_MOON_ROCHE_M/1000:.0f} km.',
            f'The Moon\u2019s actual orbital distance is {MOON_ORBIT_M/1000:.0f} km, about {MOON_ORBIT_M/EARTH_MOON_ROCHE_M:.1f} times the Roche limit \u2014 safely outside the disruption zone, consistent with the Moon\u2019s observed structural integrity.',
            f'Differential tidal acceleration across Io from Jupiter: \u0394a = 2GM_Jupiter R_Io / a_Io\u00b3 = 2 \u00d7 {G_NEWTON:.3e} \u00d7 {JUPITER_MASS_KG:.3e} \u00d7 {IO_RADIUS_M:.3e} / ({IO_SEMIMAJOR_M:.3e})\u00b3 = {IO_TIDAL_ACCEL:.3e} m/s\u00b2.',
            f'Io\u2019s own surface gravity is g = GM_Io/R_Io\u00b2 = {IO_SURFACE_GRAVITY_MS2:.3f} m/s\u00b2, so this differential tidal acceleration amounts to {IO_TIDAL_ACCEL/IO_SURFACE_GRAVITY_MS2*100:.2f}% of Io\u2019s own surface gravity \u2014 a modest-looking fraction that nonetheless drives significant heating because it is continuously flexing (not static), since Io\u2019s forced eccentricity prevents this tidal configuration from ever fully relaxing over an orbit.',
        ],
        pitfall='Treating tidal force as simply "extra strong gravity" from the companion body. Tidal force is a differential (second-derivative) effect, proportional to 1/d\u00b3 rather than 1/d\u00b2 like ordinary gravitational acceleration, and it exists precisely because gravity varies across an extended body, not because the total gravitational pull is unusually large.',
        activity='Using \u0394a \u221d 1/d\u00b3, predict by what factor the tidal acceleration on Io would change if its orbital distance were halved, and contrast this with how ordinary gravitational acceleration (\u221d1/d\u00b2) would change under the same halving.',
        lab_connection='Lab 05 computes the Roche limit for both the Earth-Moon system and a hypothetical close-in exomoon, and separately computes Io\u2019s tidal-heating-relevant differential acceleration across a full orbit given its known eccentricity.',
        synthesis='Tidal forces are a differential-gravity effect that scales as 1/d\u00b3, producing both a hard structural limit (the Roche limit) on how close a self-gravitating satellite can safely orbit and, for eccentric orbits held open by resonance, a genuine internal heat source, as dramatically demonstrated by Io.',
        openstax='OpenStax Astronomy 2e does not derive tidal forces explicitly at the introductory level; this course develops the differential-acceleration and Roche-limit formalism from first principles, connecting to the solar-system context in Chapter 3.6 (gravity with more than two bodies).',
    ),
    dict(
        n=11, title='Orbital Energy, the Vis-Viva Equation, and Orbital Transfers',
        subtitle='Using energy conservation to move between orbits, not just describe them',
        goals=[
            'Derive the specific orbital energy and the vis-viva equation from energy conservation for a two-body Keplerian orbit.',
            'Use the vis-viva equation to compute orbital speed at any point in an elliptical orbit.',
            'Compute the velocity changes and transfer time for a Hohmann transfer orbit between two circular orbits.',
        ],
        why_matters='Escape velocity (Lecture 07) is the special case of orbital energy exactly equal to zero. The vis-viva equation generalizes this to any bound (or unbound) orbit, and it is the single formula that makes real spacecraft trajectory design (and, for this course\u2019s purposes, the physical interpretation of orbital speed variations in eccentric orbits) quantitative rather than qualitative.',
        phenomenon='Earth moves noticeably faster in its orbit in early January (near perihelion) than in early July (near aphelion), even though its orbit is very nearly circular (e = 0.0167); the same speed variation, taken to its extreme for e closer to 1, is exactly what makes cometary or highly eccentric binary-star orbits move dramatically faster at closest approach than at farthest separation.',
        vocab=['specific orbital energy', 'vis-viva equation', 'periapsis/apoapsis', 'Hohmann transfer', 'delta-v', 'orbital period (generalized)'],
        evidence=[
            'Earth\u2019s measured orbital speed varies from about 30.3 km/s at perihelion to about 29.3 km/s at aphelion, a roughly 3% variation consistent with its small but nonzero eccentricity and the vis-viva prediction.',
            'Every interplanetary spacecraft mission (e.g., missions to Mars) uses a Hohmann-type transfer orbit or a close variant, exactly matching the two-burn, minimum-energy transfer strategy derived from orbital-energy conservation in this lecture.',
            'Comets on highly eccentric orbits are observed to move dramatically faster near perihelion than near aphelion, a direct, visually dramatic confirmation of the vis-viva equation\u2019s prediction that speed depends on instantaneous distance r for a fixed total energy (fixed a).',
        ],
        model=[
            'The specific orbital energy (total mechanical energy per unit reduced mass) of a bound two-body orbit is \u03b5 = -GM/(2a), a constant of the motion that depends only on the semimajor axis a, not on the eccentricity or the instantaneous position in the orbit.',
            'Combining this constant specific energy with the general orbital energy \u03b5 = v\u00b2/2 - GM/r at any point in the orbit and solving for v gives the vis-viva equation, v\u00b2 = GM(2/r - 1/a), which reduces to the circular-orbit speed when r = a and to the escape-velocity formula when a \u2192 \u221e.',
            'A Hohmann transfer orbit is an elliptical orbit tangent to both an inner circular orbit (at periapsis) and an outer circular orbit (at apoapsis); reaching it from the inner circular orbit, and later leaving it for the outer circular orbit, each requires a single velocity change (burn) computed directly from the vis-viva equation at the transfer orbit\u2019s periapsis and apoapsis.',
        ],
        equation=r'\varepsilon = -\dfrac{GM}{2a}, \qquad v^{2} = GM\left(\dfrac{2}{r}-\dfrac{1}{a}\right)',
        example=[
            f'Earth\u2019s circular-orbit approximation speed: v = \u221a(GM_Sun/a) = {V_EARTH_CIRCULAR:.2f} km/s at a = 1 AU.',
            f'Hohmann transfer orbit from Earth (1.000 AU) to Mars (1.524 AU): transfer semimajor axis a_t = {MARS_TRANSFER_A_AU:.4f} AU. Speed at transfer-orbit perihelion (still at r = 1 AU): v = {V_TRANSFER_PERIHELION:.2f} km/s, giving a first burn \u0394v1 = {HOHMANN_DV1:.2f} km/s above Earth\u2019s circular speed.',
            f'Speed at transfer-orbit aphelion (at r = 1.524 AU, Mars\u2019s orbital radius): v = {V_TRANSFER_APHELION:.2f} km/s; Mars\u2019s own circular-orbit speed there is {V_MARS_CIRCULAR:.2f} km/s, so the second burn is \u0394v2 = {HOHMANN_DV2:.2f} km/s to match Mars\u2019s circular orbit.',
            f'Transfer time (half the transfer ellipse\u2019s period, from Kepler\u2019s third law in AU/yr units): t = 0.5 \u00d7 a_t^1.5 = {HOHMANN_TRANSFER_TIME_YR:.3f} yr \u2248 {HOHMANN_TRANSFER_TIME_YR*365.25:.0f} days, consistent with the roughly 7-9 month transfer times used by real Earth-to-Mars missions.',
        ],
        pitfall='Assuming that a Hohmann transfer is the fastest way to get from one orbit to another. It is the minimum-energy (minimum total \u0394v) transfer between two coplanar circular orbits, not the minimum-time transfer; faster transfers are possible but require more propellant (a larger total \u0394v), a tradeoff every real mission-design team must weigh explicitly.',
        activity='Using \u03b5 = -GM/(2a), explain why two orbits with the same semimajor axis but very different eccentricities (e.g., a nearly circular orbit and a highly elongated ellipse) have exactly the same specific orbital energy, despite having very different speeds at any given instantaneous radius r.',
        lab_connection='Lab 06 computes a full Hohmann transfer (both burns and the transfer time) for a real interplanetary scenario and compares it to a faster, higher-\u0394v alternative trajectory.',
        synthesis='The vis-viva equation converts the single constant of orbital energy into the instantaneous speed at any point in an orbit, and chaining vis-viva calculations at two tangent orbits\u2019 shared points is exactly how minimum-energy interplanetary transfer trajectories are designed.',
        openstax='OpenStax Astronomy 2e, Chapter 3.4-3.5 (orbits in the solar system, motions of satellites and spacecraft) discusses transfer orbits qualitatively; this course derives the vis-viva equation and computes an explicit Hohmann transfer.',
    ),
    dict(
        n=12, title='Beyond Two Bodies: Lagrange Points and Hierarchical Multiple Systems',
        subtitle='When a third mass, however small, changes the picture',
        goals=[
            'Describe the five Lagrange points of the restricted three-body problem and derive the approximate location of L1 for a small secondary mass.',
            'Explain qualitatively why the general N-body problem has no closed-form solution, unlike the exact two-body problem.',
            'Apply a basic hierarchical-stability criterion to a real triple star system.',
        ],
        why_matters='Every result so far in this course has relied on the exact solvability of the two-body problem. Real systems, from the Sun-Earth-Moon system to hierarchical triple stars like Alpha Centauri (with Proxima Centauri orbiting the AB pair at large distance), always have at least a third gravitating body, and the three-body problem has no general closed-form solution \u2014 understanding when a hierarchical approximation is valid is essential for interpreting such systems correctly.',
        phenomenon=f'Proxima Centauri, live-verified this session, orbits the Alpha Centauri AB barycenter on a highly eccentric path with a period of roughly {PROXIMA_ORBIT["period_yr"]/1000:.0f},000 years, a periastron distance of about {PROXIMA_ORBIT["periastron_au"]:.0f} AU, and an apastron distance of about {PROXIMA_ORBIT["apastron_au"]:.0f} AU \u2014 more than {PROXIMA_ORBIT["periastron_au"]/ALPHA_CEN_ORBIT["semimajor_au"]:.0f} times the AB pair\u2019s own semimajor axis at closest approach alone, exactly the kind of scale separation that makes a hierarchical treatment valid.',
        vocab=['Lagrange point', 'restricted three-body problem', 'hierarchical triple system', 'N-body problem', 'stability criterion', 'barycenter'],
        evidence=[
            'Spacecraft stationed near the Sun-Earth L1 and L2 points (e.g., SOHO at L1, JWST at L2) require only small, periodic station-keeping burns to remain near these points, confirming that L1 and L2 are approximately, though not perfectly, stable equilibrium locations in the rotating Sun-Earth frame.',
            'Trojan asteroids cluster tightly around Jupiter\u2019s L4 and L5 points, 60\u00b0 ahead of and behind Jupiter in its orbit, directly confirming that these two Lagrange points are stable equilibria capable of trapping objects over solar-system lifetimes.',
            'Long-term numerical integrations of hierarchical triple star systems (including Alpha Centauri AB-Proxima) show they remain dynamically stable over gigayear timescales specifically when the outer orbit\u2019s periastron distance greatly exceeds the inner orbit\u2019s semimajor axis, consistent with the qualitative hierarchical-stability picture developed here.',
        ],
        model=[
            'In the restricted three-body problem (two massive bodies on circular orbits, plus a massless test particle), there are five equilibrium points in the rotating frame; three (L1, L2, L3) lie along the line joining the two massive bodies and are only marginally/unstably stable, while two (L4, L5) form equilateral triangles with the two massive bodies and are genuinely stable for a sufficiently large mass ratio.',
            'For a small secondary mass m2 orbiting a much larger primary m1 (m2 << m1), balancing gravitational and centrifugal forces to leading order gives the L1 distance from the secondary as r_L1 \u2248 R(m2/3m1)^(1/3), where R is the separation between the two massive bodies.',
            'The general N-body problem (three or more mutually gravitating bodies of comparable mass) has no general closed-form analytic solution; however, a hierarchical system (an inner two-body orbit whose separation is much smaller than its distance to a third body) can often be well approximated as two nested two-body problems, provided the outer periastron distance is large enough to keep the system dynamically stable.',
        ],
        equation=r'r_{L1} \approx R\left(\dfrac{m_2}{3m_1}\right)^{1/3}, \qquad \text{hierarchical stability (schematic):}\ \ a_{\rm outer}(1-e_{\rm outer}) \gg a_{\rm inner}',
        example=[
            f'Sun-Earth L1 distance: r_L1 \u2248 R(m_Earth/3m_Sun)^(1/3) = 1 AU \u00d7 ({EARTH_MASS_KG:.3e}/(3\u00d7{M_SUN_KG:.3e}))^(1/3) = {SUN_EARTH_L1_KM:.0f} km from Earth, matching the well-known operational distance of the SOHO and DSCOVR spacecraft (about 1.5 million km) to good approximation.',
            f'Alpha Centauri AB-Proxima hierarchy: inner orbit (AB) has semimajor axis {ALPHA_CEN_ORBIT["semimajor_au"]:.1f} AU; outer orbit (Proxima about the AB barycenter) has periastron {PROXIMA_ORBIT["periastron_au"]:.0f} AU, live-verified this session.',
            f'Hierarchy ratio: outer periastron / inner semimajor axis = {PROXIMA_ORBIT["periastron_au"]/ALPHA_CEN_ORBIT["semimajor_au"]:.0f} \u2014 a large ratio, consistent with published numerical-stability studies that classify the Alpha Centauri AB-Proxima system as a dynamically stable hierarchical triple over gigayear timescales, unlike a comparable system with a much smaller outer periastron distance.',
        ],
        pitfall='Assuming all five Lagrange points are equally stable "parking" locations. L1, L2, and L3 are saddle points (stable only within an unstably narrow range, requiring active station-keeping for real spacecraft), while only L4 and L5 are genuinely stable equilibria (for a sufficiently extreme mass ratio) capable of passively trapping objects like Jupiter\u2019s Trojan asteroids for billions of years.',
        activity='Using the hierarchical-stability picture (outer periastron distance versus inner semimajor axis), explain qualitatively why a triple star system with an outer periastron only 2-3 times the inner orbit\u2019s semimajor axis would be expected to be dynamically unstable on much shorter timescales than Alpha Centauri\u2019s hierarchy.',
        lab_connection='Lab 06 computes the Sun-Earth and Sun-Jupiter L1 distances and evaluates the Alpha Centauri AB-Proxima hierarchy ratio explicitly, connecting both results to this lecture\u2019s stability criteria.',
        synthesis='The restricted three-body problem\u2019s five Lagrange points, and the more general hierarchical-stability criterion for triple systems, are the practical tools astronomers use to extend two-body intuition to real systems that always have at least one additional gravitating body.',
        openstax='OpenStax Astronomy 2e, Chapter 3.6 (gravity with more than two bodies) introduces the qualitative idea; this course derives the L1 distance formula and the hierarchical-stability criterion explicitly.',
    ),
    dict(
        n=13, title='Radiation Pressure and the Eddington Luminosity',
        subtitle='When starlight itself pushes back against gravity',
        goals=[
            'Derive the radiation-pressure force on free electrons (via Thomson scattering) in a spherically symmetric radiation field.',
            'Derive the Eddington luminosity as the luminosity at which outward radiation pressure exactly balances inward gravity.',
            'Explain why the Eddington limit is irrelevant for normal stars like the Sun but crucial for compact accreting objects.',
        ],
        why_matters='Every gravity-only argument so far in this course (hydrostatic equilibrium, virial theorem, orbital mechanics) has ignored radiation pressure. For an ordinary star like the Sun, that is an excellent approximation; for a compact object accreting matter (a key endpoint discussed in ASTR 230), radiation pressure can become the dominant force and impose a hard ceiling on how fast material can be accreted or how luminous a source can shine.',
        phenomenon='The most luminous accreting X-ray binaries and active galactic nuclei are observed to cluster just below a maximum luminosity that scales linearly with the accreting object\u2019s mass, exactly as predicted by treating radiation pressure and gravity as competing outward and inward forces on the infalling gas.',
        vocab=['radiation pressure', 'Thomson (electron) scattering', 'Eddington luminosity', 'super-Eddington accretion', 'opacity (electron-scattering)', 'accretion flow'],
        evidence=[
            'X-ray binaries accreting onto neutron stars and stellar-mass black holes show observed peak luminosities consistent, to within a factor of a few, with the Eddington luminosity computed from their independently measured (or inferred) compact-object masses.',
            'Sustained super-Eddington accretion (luminosities exceeding the naive Eddington limit) is observed in some systems, but only accompanied by strong outflows/winds, consistent with radiation pressure successfully driving away excess infalling material rather than simply being "overcome."',
            'Ordinary main-sequence stars like the Sun operate enormously below their own Eddington luminosity, confirming that radiation pressure is negligible compared to gas pressure in the hydrostatic balance of normal, non-accreting stars (consistent with Lecture 05\u2019s ideal-gas treatment being adequate there).',
        ],
        model=[
            'A radiation field of luminosity L exerts an outward force on free electrons (the dominant opacity source in fully ionized, hot gas) via Thomson scattering, with force per electron equal to (flux) \u00d7 (Thomson cross-section)/c; because protons are tied to electrons by electrostatic attraction (charge neutrality), this force effectively acts on the ionized gas as a whole.',
            'Setting this outward radiation force per unit mass equal to the inward gravitational force per unit mass (using the proton mass as the effective mass per scattering electron, since protons carry essentially all the mass in ionized hydrogen) and solving for the luminosity at which they exactly balance gives the Eddington luminosity, L_Edd = 4\u03c0GMm_p c/\u03c3_T.',
            'For accretion onto a compact object, exceeding L_Edd means radiation pressure exceeds gravity, halting or reversing further infall (or driving a wind); this makes L_Edd a natural, physically motivated ceiling on sustained accretion luminosity, independent of the details of the accretion flow.',
        ],
        equation=r'L_{\rm Edd} = \dfrac{4\pi G M m_p c}{\sigma_T}',
        example=[
            f'Eddington luminosity for the Sun\u2019s own mass: L_Edd(1 M\u2609) = 4\u03c0 \u00d7 {G_NEWTON:.3e} \u00d7 {M_SUN_KG:.3e} \u00d7 {M_PROTON:.4e} \u00d7 {C_LIGHT:.3e} / {SIGMA_THOMSON:.4e} = {EDDINGTON_L_SUN_W:.3e} W = {EDDINGTON_L_SUN_W/L_SUN_W:.2e} L\u2609.',
            f'The Sun\u2019s actual luminosity ({L_SUN_W:.3e} W) is only about {L_SUN_W/EDDINGTON_L_SUN_W*100:.2e}% of its own Eddington limit, confirming radiation pressure is utterly negligible in the Sun\u2019s hydrostatic balance.',
            f'Eddington luminosity for a Chandrasekhar-mass (1.4 M\u2609) accreting compact object: L_Edd = {EDDINGTON_L_CHANDRA_W:.3e} W = {EDDINGTON_L_CHANDRA_LSUN:.2e} L\u2609 \u2014 within the observed range of peak luminosities for accreting neutron stars and stellar-mass black holes in X-ray binaries, confirming the Eddington limit\u2019s practical relevance for exactly the compact objects introduced qualitatively in ASTR 230.',
        ],
        pitfall='Assuming the Eddington luminosity is a universal maximum luminosity for any astrophysical object. It specifically describes the balance between electron-scattering radiation pressure and gravity for a spherically symmetric, hydrogen-dominated accretion flow; genuinely super-Eddington sources exist (with strong outflows), and L_Edd scales with the emitting/accreting object\u2019s mass, so a supermassive black hole\u2019s Eddington luminosity is far higher than a stellar-mass compact object\u2019s.',
        activity='Using L_Edd \u221d M, predict by what factor the Eddington luminosity of a supermassive black hole with M = 10\u2078 M\u2609 exceeds that of the 1.4 M\u2609 compact-object example above, without recomputing from scratch.',
        lab_connection='Lab 07\u2019s capstone characterization of Alpha Centauri AB includes an explicit comparison of each star\u2019s actual luminosity to its own Eddington luminosity, quantitatively confirming that radiation pressure is negligible for both (ordinary, non-accreting) stars.',
        synthesis='The Eddington luminosity is the direct consequence of balancing electron-scattering radiation pressure against gravity, and while it is many orders of magnitude above any normal star\u2019s actual luminosity, it becomes a hard, physically meaningful ceiling for luminous accreting compact objects.',
        openstax='OpenStax Astronomy 2e does not derive the Eddington luminosity at the introductory level; this course develops it from the radiation-pressure/gravity force balance, connecting to the compact-object endpoints discussed descriptively in ASTR 230, Chapter 23.',
    ),
    dict(
        n=14, title='Synthesis: Triangulating a Real Star System from Independent Physical Laws',
        subtitle='What fourteen lectures of radiation, matter, and orbits can tell us about one nearby system',
        goals=[
            'Combine the blackbody radiation law, the two-body Kepler problem, and the virial/energy tools of this course to fully characterize a real binary star system.',
            'Explain why agreement between independent methods (radiative and dynamical) is the strongest possible confirmation of a physical measurement in astrophysics.',
            'Identify which physical assumptions would need to be revisited if two independent methods disagreed substantially.',
        ],
        why_matters='This course has developed each physical law (blackbody radiation, hydrostatic equilibrium, the virial theorem, Kepler\u2019s laws, tidal forces, orbital energy, radiation pressure) largely in isolation. Real astrophysical measurement is never isolated: the strength of a measured stellar mass, radius, or luminosity comes precisely from checking it against an independent method built on different physics, exactly as this lecture now does explicitly for Alpha Centauri AB.',
        phenomenon=f'Alpha Centauri AB\u2019s total mass has now been obtained twice in this course through completely different physics: once from Kepler\u2019s third law applied to the visual orbit (Lecture 08, using only positions and time), and once by summing masses derived from stellar-structure/asteroseismic modeling constrained by directly measured radii and luminosities (Lecture 09) \u2014 the two agree to {abs(ALPHA_CEN_TOTAL_MASS_KEPLER-ALPHA_CEN_TOTAL_MASS_MEASURED)/ALPHA_CEN_TOTAL_MASS_MEASURED*100:.2f}%.',
        vocab=['independent verification', 'cross-calibration', 'systematic versus random uncertainty', 'physical consistency check', 'multi-messenger reasoning (electromagnetic + dynamical)', 'model-independence'],
        evidence=[
            'The Stefan-Boltzmann luminosity predicted from Alpha Centauri A\u2019s measured radius and temperature (Lecture 02) agrees with its independently measured (asteroseismic) luminosity to within a couple of percent, cross-validating the radiative (blackbody) side of this course\u2019s toolkit.',
            'The total mass predicted from Alpha Centauri AB\u2019s orbit via Kepler\u2019s third law (Lecture 08) agrees with the independently measured sum of individual stellar masses to a small fraction of a percent, cross-validating the dynamical (orbital) side of this course\u2019s toolkit.',
            'Both stars\u2019 actual luminosities sit many orders of magnitude below their own Eddington luminosities (Lecture 13), confirming that radiation pressure plays no role in their hydrostatic balance and that the purely gas-pressure-based treatment of Lecture 05 is self-consistently justified for this system.',
        ],
        model=[
            'A physical measurement built from a single method (however sophisticated) always carries the risk of an undetected systematic error specific to that method; agreement between two methods built on unrelated physics (e.g., radiative versus dynamical, or spectroscopic versus astrometric) is what elevates a measurement from "our best current estimate" to "a robustly confirmed physical fact."',
            'For Alpha Centauri AB, the radiative chain (Stefan-Boltzmann law + measured radius and temperature \u2192 luminosity) and the dynamical chain (Kepler\u2019s third law + measured period and semimajor axis \u2192 total mass) share no common measurement or assumption, making their mutual agreement unusually strong confirmation.',
            'When two independent methods disagree beyond their stated uncertainties, the correct response is not to average them, but to scrutinize the specific assumptions unique to each method (e.g., an unresolved third body biasing the orbit, or an incorrect distance biasing the radius) until the discrepancy is physically resolved.',
        ],
        equation=r'\text{Radiative chain: } L = 4\pi R^{2}\sigma T^{4} \quad\Longleftrightarrow\quad \text{Dynamical chain: } M_{\rm tot} = \dfrac{4\pi^{2}a^{3}}{GP^{2}}',
        example=[
            f'Alpha Centauri A: radiative luminosity (Stefan-Boltzmann from R = {ALPHA_CEN_A["radius_rsun"]:.3f} R\u2609, T = {ALPHA_CEN_A["teff"]:.0f} K) = {ALPHA_CEN_A_L_FROM_SB_LSUN:.3f} L\u2609; independently measured luminosity = {ALPHA_CEN_A["lum_lsun"]:.4f} L\u2609; agreement to {abs(ALPHA_CEN_A_L_FROM_SB_LSUN-ALPHA_CEN_A["lum_lsun"])/ALPHA_CEN_A["lum_lsun"]*100:.1f}%.',
            f'Alpha Centauri B: radiative luminosity (Stefan-Boltzmann from R = {ALPHA_CEN_B["radius_rsun"]:.3f} R\u2609, T = {ALPHA_CEN_B["teff"]:.0f} K) = {ALPHA_CEN_B_L_FROM_SB_LSUN:.3f} L\u2609; independently measured luminosity = {ALPHA_CEN_B["lum_lsun"]:.4f} L\u2609; agreement to {abs(ALPHA_CEN_B_L_FROM_SB_LSUN-ALPHA_CEN_B["lum_lsun"])/ALPHA_CEN_B["lum_lsun"]*100:.1f}%.',
            f'Dynamical total mass from Kepler\u2019s third law (Lecture 08): {ALPHA_CEN_TOTAL_MASS_KEPLER:.4f} M\u2609, versus the independently measured sum {ALPHA_CEN_TOTAL_MASS_MEASURED:.4f} M\u2609 (agreement {abs(ALPHA_CEN_TOTAL_MASS_KEPLER-ALPHA_CEN_TOTAL_MASS_MEASURED)/ALPHA_CEN_TOTAL_MASS_MEASURED*100:.2f}%) \u2014 taken together, four independent physical predictions (two radiative, one dynamical, cross-checked against three independently measured quantities) all agree to within a few percent for the same real system, the strongest possible evidence that this course\u2019s physical framework correctly describes Alpha Centauri AB.',
        ],
        pitfall='Treating close agreement between two methods as proof that both are exactly correct in an absolute sense, rather than as evidence that both are consistent with each other and with the underlying physical model to within their combined uncertainties. Even excellent agreement does not rule out a shared, unrecognized systematic error common to both methods (e.g., an error in the assumed distance, which enters both the radius used in Stefan-Boltzmann and the physical semimajor axis used in Kepler\u2019s third law).',
        activity='Given that both the radiative and dynamical chains for Alpha Centauri AB depend on the same measured parallax/distance, explain why this shared dependence means the two methods are not perfectly independent, and identify what a truly independent third check (depending on neither radius-from-angular-size-and-distance nor orbit-from-angular-separation-and-distance) might look like.',
        lab_connection='Lab 07, the course\u2019s capstone, has students reproduce every calculation in this lecture\u2019s worked example from the raw measured orbital elements and stellar parameters, and write a short synthesis of what the cross-checks do and do not prove.',
        synthesis='Fourteen lectures of radiation, matter, and orbits converge, for one real, nearby, precisely measured binary star system, on a single, mutually consistent physical picture \u2014 the clearest demonstration this course can offer that its separate physical laws describe the same underlying reality.',
        openstax='OpenStax Astronomy 2e, Chapter 18 (stellar properties) and Chapter 3 (orbits and gravity), read together as this lecture does explicitly, rather than as separate topics.',
    ),
]


def slide_deck(item: dict) -> str:
    n = item['n']
    fig = lecture_svg(item)
    body = f"""<main class='deck'>
<section class='slide title'><p class='kicker'>ASTR 310 &middot; Lecture {n:02d}</p><h1>{escape(item['title'])}</h1><h2>{escape(item['subtitle'])}</h2></section>
<section class='slide'><h2>Learning Goals</h2><ol>{li(item['goals'])}</ol><p class='small'>Reading anchor: {escape(item['openstax'])}</p></section>
<section class='slide'><h2>Why This Matters</h2><p>{item['why_matters']}</p></section>
<section class='slide'><h2>Opening Phenomenon</h2><p>{item['phenomenon']}</p><p class='warning'><strong>First question:</strong> what here is directly observed, and what follows only once a physical law is derived and applied?</p></section>
<section class='slide'><h2>Vocabulary for Reasoning</h2><div class='three'>{cards(item['vocab'])}</div><p class='small'>Use these terms to describe derivations and evidence, not as isolated definitions.</p></section>
<section class='slide'><h2>Evidence We Need to Explain</h2><ul>{li(item['evidence'])}</ul></section>
<section class='slide'><h2>Derivation and Model</h2><ul>{li(item['model'])}</ul></section>
<section class='slide'><h2>Quantitative Tool</h2><div class='equation'>\\[ {item['equation']} \\]</div></section>
<section class='slide'><h2>Worked Example</h2><ol>{li(item['example'])}</ol></section>
<section class='slide visual-slide'><h2>Visual Reasoning</h2><div class='visual-grid'><div><p>Study how this lecture\u2019s figure turns the equation and worked example above into a concrete quantitative picture.</p><ul><li>Which numbers in the figure come directly from measurement, and which are computed from this lecture\u2019s physical law?</li><li>Where do the marked points match the worked-example values above?</li><li>What would change in the figure if a key assumption in the derivation failed?</li></ul></div><figure class='visual-figure'>{fig}<figcaption>{escape(item['synthesis'])}</figcaption></figure></div></section>
<section class='slide'><h2>Common Misconception</h2><p class='warning'>{item['pitfall']}</p></section>
<section class='slide'><h2>Active Learning Segment</h2><p>{item['activity']}</p></section>
<section class='slide'><h2>Lab Connection</h2><p>{item['lab_connection']}</p></section>
<section class='slide'><h2>Synthesis</h2><p>{item['synthesis']}</p></section>
<section class='slide'><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Course dataset and derivations used in this lecture\u2019s worked example: <code>materials/ASTR310/data/</code> and <code>materials/ASTR310/src/generate_astr310_content.py</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 310 Lecture {n:02d} Slides', body, SLIDE_CSS)


def lecture_notes(item: dict) -> str:
    n = item['n']
    body = f"""<header><div><h1>Lecture {n:02d}: {escape(item['title'])}</h1><p>ASTR 310 Astrophysics I: Radiation, Matter, and Orbits</p></div></header>
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
<section><h2>Synthesis Questions</h2><ul><li>What was measured directly in this lecture\u2019s worked example, and what was derived from a physical law?</li><li>Which assumption in the derivation would most change the interpretation if it were wrong?</li><li>How does this lecture\u2019s technique connect to the lab and problem set that follow it?</li></ul></section>
<section><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Every numeric result above is computed programmatically in <code>materials/ASTR310/src/generate_astr310_content.py</code>, not hand-typed.</li></ul></section>
</main>"""
    return page(f'ASTR 310 Lecture {n:02d} Notes', body)


def write_lectures():
    LECTURE_DIR.mkdir(parents=True, exist_ok=True)
    for item in LECTURES:
        n = item['n']
        (LECTURE_DIR / f'lecture-{n:02d}-slides.html').write_text(slide_deck(item), encoding='utf-8')
        (LECTURE_DIR / f'lecture-{n:02d}-notes.html').write_text(lecture_notes(item), encoding='utf-8')


def write_data_csv():
    import csv
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / 'alpha_centauri_ab.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['star', 'mass_Msun', 'radius_Rsun', 'luminosity_Lsun', 'Teff_K', 'spectral_type'])
        for s in (ALPHA_CEN_A, ALPHA_CEN_B):
            w.writerow([s['name'], s['mass_msun'], s['radius_rsun'], s['lum_lsun'], s['teff'], s['spt']])
    with open(DATA_DIR / 'alpha_centauri_orbit.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['quantity', 'value', 'unit'])
        for k, v in ALPHA_CEN_ORBIT.items():
            w.writerow([k, v, ''])
        w.writerow(['total_mass_from_kepler3', round(ALPHA_CEN_TOTAL_MASS_KEPLER, 4), 'Msun'])
        w.writerow(['total_mass_measured_sum', round(ALPHA_CEN_TOTAL_MASS_MEASURED, 4), 'Msun'])
    with open(DATA_DIR / 'proxima_orbit.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['quantity', 'value', 'unit'])
        for k, v in PROXIMA_ORBIT.items():
            w.writerow([k, v, ''])
    with open(DATA_DIR / 'io_jupiter_tidal.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['quantity', 'value', 'unit'])
        w.writerow(['jupiter_mass_kg', JUPITER_MASS_KG, 'kg'])
        w.writerow(['io_mass_kg', IO_MASS_KG, 'kg'])
        w.writerow(['io_radius_m', IO_RADIUS_M, 'm'])
        w.writerow(['io_semimajor_m', IO_SEMIMAJOR_M, 'm'])
        w.writerow(['io_eccentricity', IO_ECCENTRICITY, ''])
        w.writerow(['io_tidal_acceleration_ms2', IO_TIDAL_ACCEL, 'm/s^2'])


if __name__ == '__main__':
    write_lectures()
    write_data_csv()
    print(f'Wrote {len(LECTURES)} lecture slide decks and notes files, plus 4 data CSV files.')


