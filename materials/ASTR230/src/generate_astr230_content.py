"""Content generator for ASTR230 lecture slides and lecture notes.

Every worked numeric example is computed programmatically from the shared
constants and datasets defined below (not hand-typed), and the same
constants are reused across labs and problem sets that reference the same
scenario (see generate_astr230_labs_psets.py). Run with the project
interpreter:
    python materials/ASTR230/src/generate_astr230_content.py
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


def svg_open(n: int, title: str, subtitle: str = '') -> str:
    sub = f"<text x='34' y='66' font-size='16' fill='#5b6773' font-family='Segoe UI, sans-serif'>{escape(subtitle)}</text>" if subtitle else ''
    return (
        f"<svg class='lecture-figure' data-lecture-figure='{n:02d}' viewBox='0 0 980 620' role='img' "
        f"aria-label='Lecture {n:02d} figure: {escape(title)}'>"
        f"<rect width='980' height='620' fill='#fbfcfd'/>"
        f"<defs><marker id='arrow' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto'>"
        f"<path d='M0,0 L10,5 L0,10 z' fill='#5b6773'/></marker></defs>"
        f"<text x='34' y='42' font-size='23' fill='#102a43' font-family='Segoe UI, sans-serif' font-weight='700'>Lecture {n:02d}: {escape(title)}</text>"
        f"{sub}"
    )


SVG_CLOSE = '</svg>'


def svg_caption(text: str, y: int = 590) -> str:
    return f"<text x='34' y='{y}' font-size='15' fill='#5b6773' font-family='Segoe UI, sans-serif'>{escape(text)}</text>"


def lin(v: float, vmin: float, vmax: float, pmin: float, pmax: float) -> float:
    return pmin + (v - vmin) / (vmax - vmin) * (pmax - pmin)


def loglin(v: float, vmin: float, vmax: float, pmin: float, pmax: float) -> float:
    return lin(math.log10(v), math.log10(vmin), math.log10(vmax), pmin, pmax)


PLOT_X0, PLOT_X1 = 160, 910
PLOT_Y0, PLOT_Y1 = 500, 150


def plot_axes(xlabel: str, ylabel: str, x0=PLOT_X0, x1=PLOT_X1, y0=PLOT_Y0, y1=PLOT_Y1) -> str:
    return (
        f"<line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y0}' stroke='#5b6773' stroke-width='2' marker-end='url(#arrow)'/>"
        f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y1}' stroke='#5b6773' stroke-width='2' marker-end='url(#arrow)'/>"
        f"<text x='{x1}' y='{y0+30}' font-size='15' fill='#5b6773' text-anchor='end' font-family='Segoe UI, sans-serif'>{escape(xlabel)}</text>"
        f"<text x='{x0-12}' y='{y1-12}' font-size='15' fill='#5b6773' text-anchor='start' font-family='Segoe UI, sans-serif'>{escape(ylabel)}</text>"
    )


def polyline(points, color='#0f6b78', width=4, dash=None) -> str:
    pts = ' '.join(f"{x:.1f},{y:.1f}" for x, y in points)
    dash_attr = f" stroke-dasharray='{dash}'" if dash else ''
    return f"<polyline points='{pts}' fill='none' stroke='{color}' stroke-width='{width}'{dash_attr}/>"


def dot(x: float, y: float, r: int = 7, color: str = '#b87911', label: str | None = None,
        dx: int = 10, dy: int = -10, anchor: str = 'start') -> str:
    out = f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{color}' stroke='#17202a' stroke-width='1'/>"
    if label:
        out += (f"<text x='{x+dx:.1f}' y='{y+dy:.1f}' font-size='14' fill='#17202a' text-anchor='{anchor}' "
                f"font-family='Segoe UI, sans-serif'>{escape(label)}</text>")
    return out


# ---------------------------------------------------------------------------
# Shared, verified real-star sample (used in Lectures 1-3, Labs 01-02, PS01-02)
# Raw measured quantities: V_app (apparent V magnitude), parallax (mas),
# T_eff (K), R (solar radii), spectral type. Sirius B values are independently
# verified via Bond et al. 2017 ApJ 840, 70 (see reference-log.md); the rest
# are standard Hipparcos-era literature values flagged for human spot-check.
# ---------------------------------------------------------------------------
STARS = [
    # name, V_app, parallax_mas, Teff_K, R_rsun, SpT
    ('Sun', -26.74, None, 5778, 1.00, 'G2V'),
    ('Sirius A', -1.46, 379.21, 9940, 1.71, 'A1V'),
    ('Alpha Centauri A', -0.01, 747.10, 5790, 1.22, 'G2V'),
    ('Arcturus', -0.05, 88.83, 4286, 25.4, 'K1.5III'),
    ('Vega', 0.03, 130.23, 9602, 2.36, 'A0V'),
    ('Capella Aa', 0.08, 76.20, 4970, 11.98, 'G8III'),
    ('Rigel', 0.13, 3.78, 12100, 78.9, 'B8Ia'),
    ('Procyon A', 0.34, 284.56, 6530, 2.05, 'F5IV-V'),
    ('Betelgeuse', 0.50, 5.95, 3600, 887.0, 'M1-2Ia'),
    ('Altair', 0.77, 194.95, 7670, 1.63, 'A7V'),
    ('Aldebaran', 0.85, 48.94, 3910, 45.1, 'K5III'),
    ('Antares', 0.96, 5.89, 3660, 680.0, 'M1.5Iab'),
    ('Spica', 0.97, 13.06, 22400, 7.47, 'B1III-IV'),
    ('Pollux', 1.14, 96.74, 4586, 9.06, 'K0III'),
    ('Fomalhaut', 1.16, 129.81, 8590, 1.84, 'A3V'),
    ('Deneb', 1.25, 1.01, 8525, 203.0, 'A2Ia'),
    ('Sirius B', 8.44, 379.21, 25000, 0.008098, 'DA2'),
    ('61 Cygni A', 5.20, 286.10, 4374, 0.665, 'K5V'),
    ('Barnard\u2019s Star', 9.54, 546.98, 3134, 0.196, 'M4V'),
    ('Proxima Centauri', 11.13, 768.50, 3042, 0.154, 'M5.5Ve'),
]

SUN_TEFF = 5778.0
SUN_MV = 4.83


def star_distance_pc(parallax_mas):
    if parallax_mas is None:
        return 4.848e-6  # 1 AU in pc, for the Sun
    return 1000.0 / parallax_mas


def star_derived(name, v_app, parallax_mas, teff, r_rsun, spt):
    d_pc = star_distance_pc(parallax_mas)
    if parallax_mas is None:
        mv = SUN_MV
        dist_mod = v_app - mv
    else:
        dist_mod = 5 * math.log10(d_pc) - 5
        mv = v_app - dist_mod
    l_from_mv = 10 ** ((SUN_MV - mv) / 2.5)
    l_from_sb = (r_rsun ** 2) * ((teff / SUN_TEFF) ** 4)
    return dict(name=name, v_app=v_app, parallax_mas=parallax_mas, d_pc=d_pc, dist_mod=dist_mod,
                mv=mv, teff=teff, r_rsun=r_rsun, spt=spt, l_from_mv=l_from_mv, l_from_sb=l_from_sb)


STAR_TABLE = [star_derived(*s) for s in STARS]
STAR_BY_NAME = {s['name']: s for s in STAR_TABLE}

# Cross-check pair used repeatedly as the worked example: Sirius A (hot,
# B-band-heavy bolometric correction) vs. Alpha Centauri A (near-solar type,
# small bolometric correction), to show where the "V mag = bolometric mag"
# simplifying assumption holds well and where it breaks down.
SIRIUS_A = STAR_BY_NAME['Sirius A']
ALPHA_CEN_A = STAR_BY_NAME['Alpha Centauri A']
SUN = STAR_BY_NAME['Sun']
SIRIUS_B = STAR_BY_NAME['Sirius B']
BETELGEUSE = STAR_BY_NAME['Betelgeuse']
PROXIMA = STAR_BY_NAME['Proxima Centauri']

# Stefan-Boltzmann direct SI check for the Sun (Lecture 01)
SIGMA_SB = 5.670374e-8  # W m^-2 K^-4
R_SUN_M = 6.957e8
L_SUN_W = 4 * math.pi * (R_SUN_M ** 2) * SIGMA_SB * (SUN_TEFF ** 4)
L_SUN_PUBLISHED_W = 3.828e26

# Mass-luminosity relation and main-sequence lifetime (Lecture 06, Lab 03)
def ms_luminosity(mass_msun: float) -> float:
    return mass_msun ** 3.5


def ms_lifetime_gyr(mass_msun: float) -> float:
    return 10.0 * mass_msun / ms_luminosity(mass_msun)


CLUSTER_TURNOFF_MASS = 3.0  # Msun, representative young open-cluster turnoff
CLUSTER_TURNOFF_AGE_MYR = ms_lifetime_gyr(CLUSTER_TURNOFF_MASS) * 1000.0

# Chandrasekhar limit / white dwarf density (Lecture 07, Lab 04) - Sirius B
M_SUN_KG = 1.989e30
R_SUN_M_FULL = 6.957e8
SIRIUS_B_MASS_KG = 1.018 * M_SUN_KG
SIRIUS_B_RADIUS_M = 0.008098 * R_SUN_M_FULL
SIRIUS_B_VOLUME_M3 = (4.0 / 3.0) * math.pi * (SIRIUS_B_RADIUS_M ** 3)
SIRIUS_B_DENSITY_KGM3 = SIRIUS_B_MASS_KG / SIRIUS_B_VOLUME_M3
CHANDRASEKHAR_LIMIT_MSUN = 1.4

# Milky Way rotation curve and enclosed mass (Lecture 10, Lab 05)
G_NEWTON = 6.674e-11
PC_M = 3.0857e16
KPC_M = 1000 * PC_M
KM = 1000.0
ROTATION_CURVE = [
    (2.0, 200.0), (4.0, 220.0), (6.0, 225.0), (8.2, 220.0),
    (10.0, 222.0), (14.0, 224.0), (18.0, 226.0), (22.0, 228.0), (25.0, 230.0),
]
R_SUN_KPC = 8.2
V_SUN_KMS = 220.0


def enclosed_mass_msun(r_kpc: float, v_kms: float) -> float:
    r_m = r_kpc * KPC_M
    v_ms = v_kms * KM
    m_kg = (v_ms ** 2) * r_m / G_NEWTON
    return m_kg / M_SUN_KG


MASS_AT_SUN_MSUN = enclosed_mass_msun(R_SUN_KPC, V_SUN_KMS)
MASS_AT_25KPC_MSUN = enclosed_mass_msun(25.0, 230.0)
# Visible (stellar + gas) mass estimate for comparison, ~6e10 Msun (bulge+disk)
VISIBLE_MASS_MSUN = 6.0e10

# Galaxy classification sample (Lecture 11, Lab 06)
GALAXIES = [
    ('M31 (Andromeda Galaxy)', 'SA(s)b', 0.78, 220, 'Nearest large spiral; Local Group; will merge with the Milky Way in ~4.5 Gyr'),
    ('M87', 'E0/cD', 16.4, 120, 'Giant elliptical, Virgo Cluster center; hosts a well-imaged supermassive black hole (EHT 2019)'),
    ('M101 (Pinwheel Galaxy)', 'SAB(rs)cd', 6.4, 170, 'Nearly face-on grand-design spiral, low bulge-to-disk ratio'),
    ('M104 (Sombrero Galaxy)', 'SA(s)a', 9.6, 110, 'Edge-on early-type spiral with a prominent dust lane and large bulge'),
    ('M82 (Cigar Galaxy)', 'Irregular (starburst)', 3.5, 37, 'Gravitationally disturbed by M81; intense starburst with galactic superwind'),
    ('NGC 1300', 'SB(rs)bc', 18.7, 110, 'Prototypical strongly barred spiral with well-defined bar-fed spiral arms'),
]

# Hubble diagram: classic five-cluster redshift-distance data (Lecture 14, Lab 07)
HUBBLE_CLUSTERS = [
    ('Virgo', 16.5, 1150.0),
    ('Hydra', 190.0, 10000.0),
    ('Ursa Major', 210.0, 15000.0),
    ('Corona Borealis', 320.0, 21600.0),
    ('Bootes', 520.0, 39300.0),
]
MPC_KM = 3.0857e19


def fit_h0_kms_mpc(clusters) -> float:
    # Simple ratio-average fit through the origin (v = H0 d), consistent with
    # the intro-level "least squares through the origin" estimator.
    num = sum(v * d for _, d, v in clusters)
    den = sum(d * d for _, d, v in clusters)
    return num / den


H0_FIT = fit_h0_kms_mpc(HUBBLE_CLUSTERS)
# 1/H0 has units of Mpc*s/km; multiplying by MPC_KM (km per Mpc) cancels the
# Mpc and km units, leaving a time in seconds, which is then converted to Gyr.
HUBBLE_TIME_GYR = (1.0 / H0_FIT) * MPC_KM / (3600 * 24 * 365.25 * 1e9)

# ---------------------------------------------------------------------------
# Lecture-specific visual-reasoning figures. Each lecture gets a structurally
# distinct diagram type (plot, geometric construction, cross-section, phase
# diagram, tuning fork, schematic, pie chart, etc.) built from the real
# constants and datasets defined above, not a reused generic shape.
# ---------------------------------------------------------------------------

def fig_01() -> str:
    """Lecture 1: Stefan-Boltzmann / inverse-square flux-distance plot."""
    d_sirius, l_sirius = SIRIUS_A['d_pc'], SIRIUS_A['l_from_sb']
    d_betel, l_betel = BETELGEUSE['d_pc'], BETELGEUSE['l_from_sb']
    flux_sirius = l_sirius / d_sirius ** 2
    flux_betel = l_betel / d_betel ** 2
    dmin, dmax = 1.0, 300.0
    fmin, fmax = 1e-4, 50.0
    curve = []
    d = dmin
    while d <= dmax:
        f = min(max(1.0 / d ** 2, fmin), fmax)
        curve.append((loglin(d, dmin, dmax, PLOT_X0, PLOT_X1), loglin(f, fmin, fmax, PLOT_Y0, PLOT_Y1)))
        d *= 1.2
    svg = svg_open(1, 'Measuring the Stars', 'Apparent flux falls off as 1/d\u00b2, independent of luminosity')
    svg += plot_axes('distance d (pc, log scale)', 'apparent flux (relative units, log scale)')
    svg += polyline(curve, color='#5b6773', width=3, dash='6,5')
    svg += dot(loglin(d_sirius, dmin, dmax, PLOT_X0, PLOT_X1), loglin(flux_sirius, fmin, fmax, PLOT_Y0, PLOT_Y1),
               color='#0f6b78', label=f'Sirius A: {l_sirius:.0f} L\u2609 at {d_sirius:.2f} pc', dx=10, dy=-12)
    svg += dot(loglin(d_betel, dmin, dmax, PLOT_X0, PLOT_X1), loglin(flux_betel, fmin, fmax, PLOT_Y0, PLOT_Y1),
               color='#b87911', label=f'Betelgeuse: {l_betel:.0f} L\u2609 at {d_betel:.0f} pc', dx=-10, dy=22, anchor='end')
    svg += svg_caption('Dashed curve: flux \u221d 1/d\u00b2 for a fixed 1 L\u2609 source. Betelgeuse\u2019s far greater luminosity is offset by its far greater distance.')
    svg += SVG_CLOSE
    return svg


def fig_02() -> str:
    """Lecture 2: non-monotonic Balmer line strength vs effective temperature."""
    def balmer(t):
        return math.exp(-((t - 9500.0) / 3200.0) ** 2)
    tmin, tmax = 3000.0, 30000.0
    curve = []
    t = tmax
    while t >= tmin:
        x = lin(t, tmin, tmax, PLOT_X1, PLOT_X0)
        y = lin(balmer(t), 0.0, 1.0, PLOT_Y0, PLOT_Y1)
        curve.append((x, y))
        t -= 250.0
    svg = svg_open(2, 'Reading Starlight', 'Hydrogen (Balmer) line strength peaks near spectral type A')
    svg += plot_axes('T_eff (K) \u2014 hot (left) to cool (right)', 'relative Balmer line strength')
    svg += polyline(curve, color='#0f6b78', width=4)
    stars = [('Rigel', STAR_BY_NAME['Rigel']['teff'], '#102a43'), ('Vega', STAR_BY_NAME['Vega']['teff'], '#0f6b78'),
             ('Sun', SUN_TEFF, '#b87911'), ('Betelgeuse', BETELGEUSE['teff'], '#8a4b08')]
    for name, teff, color in stars:
        x = lin(teff, tmin, tmax, PLOT_X1, PLOT_X0)
        y = lin(balmer(teff), 0.0, 1.0, PLOT_Y0, PLOT_Y1)
        svg += f"<line x1='{x:.1f}' y1='{PLOT_Y0}' x2='{x:.1f}' y2='{y:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='4,4'/>"
        svg += dot(x, y, r=6, color=color, label=f'{name} ({teff:.0f} K)', dx=8, dy=-10)
    svg += svg_caption('Above \u224810,000 K hydrogen ionizes past neutral; below \u22485,000-6,000 K it stays unexcited \u2014 both suppress Balmer absorption.')
    svg += SVG_CLOSE
    return svg


def fig_03() -> str:
    """Lecture 3: parallax baseline/angle geometry for two real stars."""
    svg = svg_open(3, 'Parallax Distance', 'A larger parallax angle means a shorter distance (not to scale)')
    bx0, bx1, by = 340, 620, 500
    svg += f"<line x1='{bx0}' y1='{by}' x2='{bx1}' y2='{by}' stroke='#102a43' stroke-width='4'/>"
    svg += f"<circle cx='{bx0}' cy='{by}' r='7' fill='#0f6b78'/><circle cx='{bx1}' cy='{by}' r='7' fill='#0f6b78'/>"
    svg += f"<text x='{bx0}' y='{by+26}' font-size='14' text-anchor='middle' fill='#17202a' font-family='Segoe UI, sans-serif'>Earth (Jan)</text>"
    svg += f"<text x='{bx1}' y='{by+26}' font-size='14' text-anchor='middle' fill='#17202a' font-family='Segoe UI, sans-serif'>Earth (Jul)</text>"
    svg += f"<text x='{(bx0+bx1)/2:.0f}' y='{by+48}' font-size='13' text-anchor='middle' fill='#5b6773' font-family='Segoe UI, sans-serif'>baseline = 2 AU</text>"
    apex_x1, apex_y1 = 480, 260
    svg += f"<line x1='{bx0}' y1='{by}' x2='{apex_x1}' y2='{apex_y1}' stroke='#b87911' stroke-width='2.5'/>"
    svg += f"<line x1='{bx1}' y1='{by}' x2='{apex_x1}' y2='{apex_y1}' stroke='#b87911' stroke-width='2.5'/>"
    svg += dot(apex_x1, apex_y1, r=8, color='#b87911',
               label=f'Proxima Centauri: p={PROXIMA["parallax_mas"]:.2f} mas \u2192 d={PROXIMA["d_pc"]:.2f} pc', dx=14, dy=4)
    apex_x2, apex_y2 = 760, 165
    svg += f"<line x1='{bx0}' y1='{by}' x2='{apex_x2}' y2='{apex_y2}' stroke='#0f6b78' stroke-width='2.5'/>"
    svg += f"<line x1='{bx1}' y1='{by}' x2='{apex_x2}' y2='{apex_y2}' stroke='#0f6b78' stroke-width='2.5'/>"
    svg += dot(apex_x2, apex_y2, r=8, color='#0f6b78',
               label=f'Sirius A: p={SIRIUS_A["parallax_mas"]:.2f} mas \u2192 d={SIRIUS_A["d_pc"]:.2f} pc', dx=14, dy=4)
    svg += svg_caption('Distance d(pc) = 1/p(arcsec): Proxima\u2019s larger parallax angle places it closer than Sirius A, even though Sirius A looks far brighter.')
    svg += SVG_CLOSE
    return svg


def fig_04() -> str:
    """Lecture 4: labeled concentric cross-section of stellar interior and energy transport."""
    cx, cy = 470, 340
    r_conv, r_rad, r_core = 220, 145, 68
    svg = svg_open(4, 'Inside a Star', 'Hydrostatic equilibrium: layered structure supported from a fusing core')
    svg += f"<circle cx='{cx}' cy='{cy}' r='{r_conv}' fill='#e5f4f6' stroke='#102a43' stroke-width='2'/>"
    svg += f"<circle cx='{cx}' cy='{cy}' r='{r_rad}' fill='#b9dde2' stroke='#102a43' stroke-width='2'/>"
    svg += f"<circle cx='{cx}' cy='{cy}' r='{r_core}' fill='#b87911' stroke='#102a43' stroke-width='2'/>"
    svg += f"<text x='{cx}' y='{cy-4}' font-size='13' text-anchor='middle' fill='#fff' font-family='Segoe UI, sans-serif'>core</text>"
    svg += f"<text x='{cx}' y='{cy+14}' font-size='12' text-anchor='middle' fill='#fff' font-family='Segoe UI, sans-serif'>T \u2248 1.5\u00d710\u2077 K</text>"
    svg += f"<text x='{cx}' y='{cy-r_rad-14}' font-size='14' text-anchor='middle' fill='#102a43' font-family='Segoe UI, sans-serif'>radiative zone</text>"
    svg += f"<text x='{cx}' y='{cy-r_conv-14}' font-size='14' text-anchor='middle' fill='#102a43' font-family='Segoe UI, sans-serif'>convective zone</text>"
    svg += f"<text x='{cx}' y='{cy-r_conv-34}' font-size='13' text-anchor='middle' fill='#5b6773' font-family='Segoe UI, sans-serif'>photosphere: T_eff \u2248 {SUN_TEFF:.0f} K, R = {R_SUN_M/1000:.3e} km</text>"
    svg += f"<path d='M{cx} {cy} L{cx+r_core+40} {cy-30}' stroke='#8a4b08' stroke-width='3' marker-end='url(#arrow)'/>"
    svg += f"<text x='{cx+r_core+48}' y='{cy-30}' font-size='13' fill='#8a4b08' font-family='Segoe UI, sans-serif'>4\u00b9H \u2192 \u2074He + energy</text>"
    svg += svg_caption('Outward pressure from core fusion balances gravity at every radius; energy diffuses out radiatively, then convectively, to the photosphere.')
    svg += SVG_CLOSE
    return svg


def fig_05() -> str:
    """Lecture 5: Jeans-criterion density-temperature phase diagram."""
    nmin, nmax = 0.1, 1e6
    tmin, tmax = 5.0, 10000.0
    svg = svg_open(5, 'Stellar Nurseries', 'Collapse is favored only at high density and low temperature')
    svg += plot_axes('number density n (cm\u207b\u00b3, log scale)', 'temperature T (K, log scale)')
    boundary = []
    n = nmin
    while n <= nmax:
        t_b = min(max(3000.0 * n ** -0.35, tmin), tmax)
        boundary.append((loglin(n, nmin, nmax, PLOT_X0, PLOT_X1), loglin(t_b, tmin, tmax, PLOT_Y0, PLOT_Y1)))
        n *= 2.0
    svg += polyline(boundary, color='#8a4b08', width=3, dash='7,5')
    svg += dot(loglin(1.0, nmin, nmax, PLOT_X0, PLOT_X1), loglin(1000.0, tmin, tmax, PLOT_Y0, PLOT_Y1),
               color='#102a43', label='diffuse ISM: n\u22481 cm\u207b\u00b3, T\u2248100-10,000 K', dx=10, dy=-12)
    svg += dot(loglin(3e4, nmin, nmax, PLOT_X0, PLOT_X1), loglin(15.0, tmin, tmax, PLOT_Y0, PLOT_Y1),
               color='#0f6b78', label='molecular cloud core: n\u224810\u2074-10\u2075 cm\u207b\u00b3, T\u224810-20 K', dx=-10, dy=24, anchor='end')
    svg += svg_caption('Dashed line: illustrative Jeans-instability boundary (M_Jeans \u221d T^1.5 n^-1/2); only cold, dense cores fall below it into the collapse-favored region.')
    svg += SVG_CLOSE
    return svg


def fig_06() -> str:
    """Lecture 6: log-log main-sequence lifetime vs mass curve."""
    mmin, mmax = 0.1, 20.0
    tmin, tmax = 1e-2, 1e4
    curve = []
    m = mmin
    while m <= mmax:
        t = min(max(ms_lifetime_gyr(m), tmin), tmax)
        curve.append((loglin(m, mmin, mmax, PLOT_X0, PLOT_X1), loglin(t, tmin, tmax, PLOT_Y0, PLOT_Y1)))
        m *= 1.2
    svg = svg_open(6, 'Life After the Main Sequence', 't_MS \u221d M^-2.5: massive stars live fast and die young')
    svg += plot_axes('mass M (M\u2609, log scale)', 'main-sequence lifetime (Gyr, log scale)')
    svg += polyline(curve, color='#0f6b78', width=4)
    marks = [(1.0, '#b87911', 10, -10, 'start'), (CLUSTER_TURNOFF_MASS, '#102a43', 10, -10, 'start'),
             (10.0, '#8a4b08', -10, 20, 'end')]
    for m, color, dx, dy, anchor in marks:
        t = ms_lifetime_gyr(m)
        svg += dot(loglin(m, mmin, mmax, PLOT_X0, PLOT_X1), loglin(t, tmin, tmax, PLOT_Y0, PLOT_Y1),
                   color=color, label=f'{m:.0f} M\u2609: {t:.2f} Gyr', dx=dx, dy=dy, anchor=anchor)
    svg += svg_caption('Because L \u221d M^3.5, lifetime falls steeply with mass; a cluster\u2019s main-sequence turnoff mass is a direct age clock.')
    svg += SVG_CLOSE
    return svg


def fig_07() -> str:
    """Lecture 7: white dwarf mass-radius curve anchored at Sirius B, with Chandrasekhar asymptote."""
    mch = CHANDRASEKHAR_LIMIT_MSUN
    m_sb = 1.018
    r_sb = SIRIUS_B_RADIUS_M / R_SUN_M_FULL
    mmin, mmax = 0.2, mch - 0.02
    rmin, rmax = 0.0, 0.018
    curve = []
    m = mmin
    while m <= mmax:
        r = min(r_sb * (m_sb / m) ** (1.0 / 3.0), rmax)
        curve.append((lin(m, 0.0, mch, PLOT_X0, PLOT_X1), lin(r, rmin, rmax, PLOT_Y0, PLOT_Y1)))
        m += 0.02
    svg = svg_open(7, 'White Dwarfs', 'Degenerate matter: radius shrinks as mass grows toward a hard limit')
    svg += plot_axes('mass (M\u2609)', 'radius (R\u2609)')
    svg += polyline(curve, color='#0f6b78', width=4)
    xch = lin(mch, 0.0, mch, PLOT_X0, PLOT_X1)
    svg += f"<line x1='{xch:.1f}' y1='{PLOT_Y0}' x2='{xch:.1f}' y2='{PLOT_Y1}' stroke='#8a4b08' stroke-width='2.5' stroke-dasharray='6,5'/>"
    svg += f"<text x='{xch-8:.1f}' y='{PLOT_Y1+16}' font-size='13' fill='#8a4b08' text-anchor='end' font-family='Segoe UI, sans-serif'>Chandrasekhar limit ({mch:.1f} M\u2609)</text>"
    svg += dot(lin(m_sb, 0.0, mch, PLOT_X0, PLOT_X1), lin(r_sb, rmin, rmax, PLOT_Y0, PLOT_Y1), color='#b87911',
               label=f'Sirius B: {m_sb:.3f} M\u2609, {r_sb:.5f} R\u2609', dx=-10, dy=22, anchor='end')
    svg += svg_caption('Illustrative R \u221d M^-1/3 degenerate-matter scaling anchored at Sirius B\u2019s measured mass and radius; the real relation steepens further as M\u2192the Chandrasekhar limit.')
    svg += SVG_CLOSE
    return svg


def fig_08() -> str:
    """Lecture 8: core-collapse spin-up, two circles at very different scale with rotation arrows."""
    period_core_s = 2.6e6
    r_core_km, r_ns_km = 1.0e4, 10.0
    period_ns_s = period_core_s * (r_ns_km / r_core_km) ** 2
    svg = svg_open(8, 'Supernovae and Neutron Stars', 'Conserved angular momentum spins a collapsing core up')
    cx1, cy1, r1 = 260, 330, 130
    cx2, cy2, r2 = 760, 330, 18
    svg += f"<circle cx='{cx1}' cy='{cy1}' r='{r1}' fill='#e5f4f6' stroke='#102a43' stroke-width='2'/>"
    svg += f"<circle cx='{cx2}' cy='{cy2}' r='{r2}' fill='#102a43' stroke='#0f6b78' stroke-width='2'/>"
    svg += f"<path d='M{cx1-90} {cy1-36} A 96 96 0 1 1 {cx1-90} {cy1+36}' fill='none' stroke='#5b6773' stroke-width='3' marker-end='url(#arrow)'/>"
    svg += f"<path d='M{cx2-22} {cy2-9} A 12 12 0 1 1 {cx2-22} {cy2+9}' fill='none' stroke='#5b6773' stroke-width='2' marker-end='url(#arrow)'/>"
    svg += f"<path d='M{cx1+r1+25} {cy1} L{cx2-r2-25} {cy2}' stroke='#8a4b08' stroke-width='3' marker-end='url(#arrow)'/>"
    svg += f"<text x='{(cx1+cx2)/2:.0f}' y='{cy1-18}' font-size='14' text-anchor='middle' fill='#8a4b08' font-family='Segoe UI, sans-serif'>core collapse</text>"
    svg += f"<text x='{cx1}' y='{cy1+r1+30}' font-size='13' text-anchor='middle' fill='#17202a' font-family='Segoe UI, sans-serif'>massive-star core: R\u2248{r_core_km:.0e} km, P\u2248{period_core_s:.1e} s</text>"
    svg += f"<text x='{cx2}' y='{cy1+r1+30}' font-size='13' text-anchor='middle' fill='#17202a' font-family='Segoe UI, sans-serif'>neutron star: R\u2248{r_ns_km:.0f} km, P\u2248{period_ns_s:.1f} s</text>"
    svg += svg_caption('I\u03c9 \u2248 const with I\u221dR\u00b2: shrinking the radius by a factor of ~1,000 spins the remnant up by a factor of ~10\u2076.')
    svg += SVG_CLOSE
    return svg


def fig_09() -> str:
    """Lecture 9: log-log Schwarzschild radius vs mass, straight-line scaling."""
    mmin, mmax = 1.0, 1e7
    c_light = 2.998e8

    def rs_km(m_msun):
        return 2 * G_NEWTON * (m_msun * M_SUN_KG) / c_light ** 2 / 1000.0

    rmin, rmax = rs_km(mmin), rs_km(mmax)
    curve = []
    m = mmin
    while m <= mmax:
        curve.append((loglin(m, mmin, mmax, PLOT_X0, PLOT_X1), loglin(rs_km(m), rmin, rmax, PLOT_Y0, PLOT_Y1)))
        m *= 3.0
    svg = svg_open(9, 'Black Holes', 'Event-horizon size scales linearly with mass')
    svg += plot_axes('mass (M\u2609, log scale)', 'Schwarzschild radius R_s (km, log scale)')
    svg += polyline(curve, color='#0f6b78', width=4)
    marks = [(10.0, '10 M\u2609 stellar black hole', '#b87911', 10, -10, 'start'),
             (4.3e6, 'Sagittarius A*', '#102a43', -10, 24, 'end')]
    for m, label, color, dx, dy, anchor in marks:
        svg += dot(loglin(m, mmin, mmax, PLOT_X0, PLOT_X1), loglin(rs_km(m), rmin, rmax, PLOT_Y0, PLOT_Y1),
                   color=color, label=f'{label}: R_s\u2248{rs_km(m):.2e} km', dx=dx, dy=dy, anchor=anchor)
    svg += svg_caption('R_s = 2GM/c\u00b2 is a straight line on log-log axes: more massive black holes have larger, not smaller, event horizons.')
    svg += SVG_CLOSE
    return svg


def fig_10() -> str:
    """Lecture 10: Milky Way rotation curve from real data, vs a Keplerian decline."""
    rmin, rmax = 0.0, 26.0
    vmin, vmax = 0.0, 260.0
    curve = [(lin(r, rmin, rmax, PLOT_X0, PLOT_X1), lin(v, vmin, vmax, PLOT_Y0, PLOT_Y1)) for r, v in ROTATION_CURVE]
    kepler = []
    r = R_SUN_KPC
    while r <= rmax:
        v = V_SUN_KMS * math.sqrt(R_SUN_KPC / r)
        kepler.append((lin(r, rmin, rmax, PLOT_X0, PLOT_X1), lin(v, vmin, vmax, PLOT_Y0, PLOT_Y1)))
        r += 0.5
    svg = svg_open(10, 'The Milky Way', 'A flat rotation curve implies mass far beyond the visible disk')
    svg += plot_axes('galactocentric radius (kpc)', 'circular velocity (km/s)')
    svg += polyline(kepler, color='#8a4b08', width=3, dash='6,5')
    svg += polyline(curve, color='#0f6b78', width=4)
    for x, y in curve:
        svg += dot(x, y, r=6, color='#0f6b78')
    svg += dot(lin(R_SUN_KPC, rmin, rmax, PLOT_X0, PLOT_X1), lin(V_SUN_KMS, vmin, vmax, PLOT_Y0, PLOT_Y1), r=8,
               color='#b87911', label=f'Sun: R\u2080={R_SUN_KPC:.1f} kpc, V\u2080={V_SUN_KMS:.0f} km/s', dx=10, dy=-14)
    svg += svg_caption('Solid: observed rotation curve (stays flat to 25 kpc). Dashed: Keplerian decline expected if mass were concentrated within the Sun\u2019s orbit.')
    svg += SVG_CLOSE
    return svg


def fig_11() -> str:
    """Lecture 11: Hubble tuning-fork morphological classification diagram."""
    svg = svg_open(11, 'Sorting the Galaxies', 'The Hubble tuning fork: a morphological, not evolutionary, sequence')
    ex0, ey = 150, 330
    for i in range(5):
        rx, ry = 34, max(34 - i * 6, 9)
        cx = ex0 + i * 66
        svg += f"<ellipse cx='{cx}' cy='{ey}' rx='{rx}' ry='{ry}' fill='#102a43'/>"
    svg += f"<text x='{ex0}' y='{ey-46}' font-size='12' text-anchor='middle' fill='#5b6773' font-family='Segoe UI, sans-serif'>M87 (E0/cD)</text>"
    svg += f"<text x='{ex0+2*66}' y='{ey+58}' font-size='13' text-anchor='middle' fill='#17202a' font-family='Segoe UI, sans-serif'>ellipticals E0\u2192E7 (increasing flattening)</text>"
    forkx = ex0 + 4 * 66
    upper_y, lower_y = 190, 470
    svg += f"<path d='M{forkx} {ey} L{forkx+70} {upper_y}' stroke='#5b6773' stroke-width='3' fill='none'/>"
    svg += f"<path d='M{forkx} {ey} L{forkx+70} {lower_y}' stroke='#5b6773' stroke-width='3' fill='none'/>"
    upper = [('Sa', 'M104', forkx + 140, upper_y), ('Sb', None, forkx + 250, upper_y - 8), ('Sc', 'M101', forkx + 360, upper_y - 16)]
    for label, gal, x, y in upper:
        text = f'{label} ({gal})' if gal else label
        svg += f"<circle cx='{x}' cy='{y}' r='26' fill='none' stroke='#0f6b78' stroke-width='3'/>"
        svg += f"<path d='M{x-20} {y} Q{x} {y-28} {x+20} {y}' fill='none' stroke='#0f6b78' stroke-width='2'/>"
        svg += f"<text x='{x}' y='{y+44}' font-size='12' text-anchor='middle' fill='#17202a' font-family='Segoe UI, sans-serif'>{escape(text)}</text>"
    lower = [('SBa', None, forkx + 140, lower_y), ('SBb', 'NGC 1300', forkx + 250, lower_y + 8), ('SBc', None, forkx + 360, lower_y + 16)]
    for label, gal, x, y in lower:
        text = f'{label} ({gal})' if gal else label
        svg += f"<circle cx='{x}' cy='{y}' r='26' fill='none' stroke='#b87911' stroke-width='3'/>"
        svg += f"<line x1='{x-22}' y1='{y}' x2='{x+22}' y2='{y}' stroke='#b87911' stroke-width='3'/>"
        svg += f"<text x='{x}' y='{y+44}' font-size='12' text-anchor='middle' fill='#17202a' font-family='Segoe UI, sans-serif'>{escape(text)}</text>"
    svg += f"<rect x='{forkx+300}' y='{ey-14}' width='130' height='28' rx='4' fill='#8a4b08' opacity='.85'/>"
    svg += f"<text x='{forkx+365}' y='{ey+5}' font-size='12' text-anchor='middle' fill='#fff' font-family='Segoe UI, sans-serif'>Irregular: M82</text>"
    svg += svg_caption('Hubble\u2019s morphological sequence branches from ellipticals into ordinary and barred spirals of decreasing bulge-to-disk ratio; it is not an evolutionary timeline.')
    svg += SVG_CLOSE
    return svg


def fig_12() -> str:
    """Lecture 12: unified AGN model, axisymmetric disk/torus/jet cross-section."""
    cx, cy = 470, 330
    svg = svg_open(12, 'Active Galaxies', 'The unified AGN model: one structure, different viewing angles')
    svg += f"<line x1='{cx}' y1='{cy}' x2='{cx}' y2='{cy-200}' stroke='#0f6b78' stroke-width='5' marker-end='url(#arrow)'/>"
    svg += f"<line x1='{cx}' y1='{cy}' x2='{cx}' y2='{cy+200}' stroke='#0f6b78' stroke-width='5' marker-end='url(#arrow)'/>"
    svg += f"<text x='{cx+14}' y='{cy-180}' font-size='13' fill='#0f6b78' font-family='Segoe UI, sans-serif'>relativistic jet</text>"
    svg += f"<ellipse cx='{cx}' cy='{cy}' rx='120' ry='22' fill='none' stroke='#b87911' stroke-width='4'/>"
    svg += f"<text x='{cx}' y='{cy+44}' font-size='12' text-anchor='middle' fill='#8a4b08' font-family='Segoe UI, sans-serif'>accretion disk</text>"
    svg += f"<path d='M{cx-150} {cy-42} L{cx-70} {cy-10} L{cx-70} {cy+10} L{cx-150} {cy+42} Z' fill='#5b6773' opacity='.8'/>"
    svg += f"<path d='M{cx+150} {cy-42} L{cx+70} {cy-10} L{cx+70} {cy+10} L{cx+150} {cy+42} Z' fill='#5b6773' opacity='.8'/>"
    svg += f"<circle cx='{cx}' cy='{cy}' r='9' fill='#000'/>"
    svg += f"<text x='{cx-195}' y='{cy}' font-size='12' text-anchor='middle' fill='#fff' font-family='Segoe UI, sans-serif'>dusty torus</text>"
    svg += f"<path d='M{cx-260} {cy-215} L{cx} {cy}' stroke='#102a43' stroke-width='2' stroke-dasharray='5,4'/>"
    svg += f"<text x='{cx-260}' y='{cy-225}' font-size='12' fill='#102a43' font-family='Segoe UI, sans-serif'>blazar view (down the jet)</text>"
    svg += f"<path d='M{cx-300} {cy+30} L{cx} {cy}' stroke='#102a43' stroke-width='2' stroke-dasharray='5,4'/>"
    svg += f"<text x='{cx-300}' y='{cy+50}' font-size='12' fill='#102a43' font-family='Segoe UI, sans-serif'>quasar/Seyfert view (disk visible)</text>"
    svg += f"<path d='M{cx+300} {cy+10} L{cx} {cy}' stroke='#102a43' stroke-width='2' stroke-dasharray='5,4'/>"
    svg += f"<text x='{cx+300}' y='{cy+30}' font-size='12' text-anchor='end' fill='#102a43' font-family='Segoe UI, sans-serif'>radio galaxy view (torus blocks disk)</text>"
    svg += svg_caption('The unified model attributes Seyferts, quasars, radio galaxies, and blazars to the same disk+torus+jet structure seen from different angles.')
    svg += SVG_CLOSE
    return svg


def fig_13() -> str:
    """Lecture 13: pie chart of the universe's baryon/dark matter/dark energy budget."""
    cx, cy, r = 420, 330, 175
    slices = [('ordinary matter', 0.05, '#b87911'), ('dark matter', 0.25, '#0f6b78'), ('dark energy', 0.70, '#102a43')]
    svg = svg_open(13, 'The Cosmic Web', '\u03a9_baryon + \u03a9_dark matter + \u03a9_dark energy = 1')
    start = -90.0
    for label, frac, color in slices:
        end = start + frac * 360.0
        large_arc = 1 if (end - start) > 180 else 0
        x0 = cx + r * math.cos(math.radians(start))
        y0 = cy + r * math.sin(math.radians(start))
        x1 = cx + r * math.cos(math.radians(end))
        y1 = cy + r * math.sin(math.radians(end))
        svg += f"<path d='M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {large_arc} 1 {x1:.1f} {y1:.1f} Z' fill='{color}' stroke='#fff' stroke-width='2'/>"
        mid = math.radians((start + end) / 2)
        lx, ly = cx + (r + 45) * math.cos(mid), cy + (r + 45) * math.sin(mid)
        svg += f"<text x='{lx:.1f}' y='{ly:.1f}' font-size='14' text-anchor='middle' fill='#17202a' font-family='Segoe UI, sans-serif'>{label}: {frac*100:.0f}%</text>"
        start = end
    svg += svg_caption('Rotation curves and cluster dynamics measure the dark-matter share; distant Type Ia supernovae measure the dark-energy share \u2014 independent evidence, one budget.')
    svg += SVG_CLOSE
    return svg


def fig_14() -> str:
    """Lecture 14: Hubble diagram scatter with fitted line through the origin."""
    dmax = max(d for _, d, v in HUBBLE_CLUSTERS) * 1.1
    vmax = max(v for _, d, v in HUBBLE_CLUSTERS) * 1.1
    svg = svg_open(14, "Hubble's Law", 'Recession velocity is directly proportional to distance')
    svg += plot_axes('distance (Mpc)', 'recession velocity (km/s)')
    fitline = [(lin(0.0, 0.0, dmax, PLOT_X0, PLOT_X1), lin(0.0, 0.0, vmax, PLOT_Y0, PLOT_Y1)),
               (lin(dmax, 0.0, dmax, PLOT_X0, PLOT_X1), lin(H0_FIT * dmax, 0.0, vmax, PLOT_Y0, PLOT_Y1))]
    svg += polyline(fitline, color='#8a4b08', width=3, dash='7,5')
    for name, d, v in HUBBLE_CLUSTERS:
        svg += dot(lin(d, 0.0, dmax, PLOT_X0, PLOT_X1), lin(v, 0.0, vmax, PLOT_Y0, PLOT_Y1),
                   color='#0f6b78', label=name, dx=8, dy=-10)
    svg += svg_caption(f'Best-fit line through the origin: v = H\u2080 d with H\u2080 \u2248 {H0_FIT:.1f} km/s/Mpc, giving a Hubble time of about {HUBBLE_TIME_GYR:.1f} Gyr.')
    svg += SVG_CLOSE
    return svg


FIGURE_BUILDERS = {
    1: fig_01, 2: fig_02, 3: fig_03, 4: fig_04, 5: fig_05, 6: fig_06, 7: fig_07,
    8: fig_08, 9: fig_09, 10: fig_10, 11: fig_11, 12: fig_12, 13: fig_13, 14: fig_14,
}


# ---------------------------------------------------------------------------
# Lecture content
# ---------------------------------------------------------------------------
LECTURES = [
    dict(
        n=1, title='Measuring the Stars: Luminosity, Temperature, and Radius',
        subtitle='From a point of light to a physical object',
        goals=[
            'State the Stefan-Boltzmann law and use it to relate a star\u2019s luminosity, radius, and surface temperature.',
            'Distinguish apparent brightness from luminosity using the inverse-square law.',
            'Verify the Sun\u2019s luminosity from first principles using its measured radius and temperature.',
        ],
        why_matters='A star is a point of light in every telescope humans have ever built or will build for the foreseeable future \u2014 we cannot resolve a stellar surface (except, barely, for a handful of the nearest supergiants with modern interferometry). Everything we know about stellar sizes, temperatures, and total energy output is inferred from the amount and color of light that reaches us, combined with a small number of physical laws. This lecture builds the single most important of those laws.',
        phenomenon=f'The Sun has a measured radius of {R_SUN_M/1000:.3e} km and a measured surface temperature of {SUN_TEFF:.0f} K. Using only these two numbers and the Stefan-Boltzmann law, we can predict its total power output and compare that prediction to the independently measured solar constant.',
        vocab=['luminosity', 'apparent brightness (flux)', 'Stefan-Boltzmann law', 'inverse-square law', 'effective temperature', 'blackbody spectrum'],
        evidence=[
            f'The Sun\u2019s directly measured radius is R = {R_SUN_M:.3e} m and its spectrum peaks at a wavelength consistent with an effective temperature of T = {SUN_TEFF:.0f} K.',
            'Two stars can have identical apparent brightness in the sky yet radically different luminosities, if one is much farther away (Betelgeuse, at roughly 170 pc, radiates over 100,000 times the Sun\u2019s luminosity yet appears fainter in our sky than much closer, intrinsically dimmer stars).',
            'Every star\u2019s continuous spectrum approximates a blackbody curve, whose shape and peak wavelength depend only on temperature (Wien\u2019s law), not on composition or size.',
        ],
        model=[
            'The Stefan-Boltzmann law states that a blackbody radiates a power per unit area equal to \u03c3T\u2074, so a star\u2019s total luminosity is L = 4\u03c0R\u00b2\u03c3T\u2074.',
            'The inverse-square law states that the flux (apparent brightness) received at distance d falls off as F = L / (4\u03c0d\u00b2), so the same luminosity looks fainter the farther away it is.',
            'Because flux depends on both L and d, we cannot read off a star\u2019s luminosity from its apparent brightness alone \u2014 we need an independent distance measurement (Lecture 03).',
        ],
        equation=r'L = 4\pi R^{2} \sigma T^{4}, \qquad F = \dfrac{L}{4\pi d^{2}}',
        example=[
            f'The Sun: R = {R_SUN_M:.4e} m, T = {SUN_TEFF:.0f} K, \u03c3 = {SIGMA_SB:.4e} W m\u207b\u00b2 K\u207b\u2074.',
            f'L = 4\u03c0({R_SUN_M:.3e})\u00b2 \u00d7 ({SIGMA_SB:.3e}) \u00d7 ({SUN_TEFF:.0f})\u2074 = {L_SUN_W:.3e} W.',
            f'The independently measured (satellite radiometer) solar luminosity is {L_SUN_PUBLISHED_W:.3e} W.',
            f'Agreement: the Stefan-Boltzmann prediction differs from the measured value by only {abs(L_SUN_W-L_SUN_PUBLISHED_W)/L_SUN_PUBLISHED_W*100:.2f}%, confirming the law using the one star whose radius and temperature we can measure directly and whose luminosity we can also measure directly by other means.',
        ],
        pitfall='Confusing "bright in the sky" with "luminous." A star\u2019s apparent brightness is a joint function of luminosity and distance; only after fixing the distance can brightness be converted into luminosity.',
        activity='Given two stars with equal apparent brightness, one twice as far away as the other, compute the luminosity ratio required to produce that equal apparent brightness.',
        lab_connection='Lab 01 uses this exact Stefan-Boltzmann relation, together with parallax distances (Lecture 03), to place 20 real stars on a Hertzsprung-Russell diagram.',
        synthesis='Two physical laws \u2014 Stefan-Boltzmann and inverse-square \u2014 convert a point of starlight into a physical size, temperature, and total energy output, but only once an independent distance is known.',
        openstax='OpenStax Astronomy 2e, Chapter 18.1-18.2 (the brightness of stars, radii of stars) and Chapter 5.4 (Stefan-Boltzmann and Wien\u2019s laws).',
    ),
    dict(
        n=2, title='Reading Starlight: Spectra and Spectral Classification',
        subtitle='Why hydrogen lines are strongest in stars that are not made of pure hydrogen',
        goals=[
            'Explain the OBAFGKM spectral sequence as a temperature sequence, not a composition sequence.',
            'Describe why hydrogen absorption lines are strongest around spectral type A rather than in the hottest or coolest stars.',
            'Use spectral type and luminosity class together to identify a star\u2019s evolutionary state.',
        ],
        why_matters='Annie Jump Cannon and colleagues at Harvard classified hundreds of thousands of stellar spectra by eye in the early twentieth century, originally in an alphabetical sequence (A, B, C, ...) that seemed to track line strength. Only later did Cecilia Payne-Gaposchkin show, in her 1925 PhD thesis, that the sequence is really a temperature sequence and that stars are overwhelmingly hydrogen and helium \u2014 a result initially doubted because it contradicted the prevailing assumption that stars had roughly Earth-like compositions.',
        phenomenon=f'Vega (spectral type A0V, T_eff \u2248 {STAR_BY_NAME["Vega"]["teff"]:.0f} K) shows very strong hydrogen absorption lines. The Sun (G2V, T_eff \u2248 {SUN_TEFF:.0f} K) shows much weaker hydrogen lines but strong lines of ionized calcium. Rigel (B8Ia, T_eff \u2248 {STAR_BY_NAME["Rigel"]["teff"]:.0f} K) shows weaker hydrogen lines than Vega despite being hotter. All three stars are overwhelmingly hydrogen by mass.',
        vocab=['spectral type (OBAFGKM)', 'luminosity class (Ia-V)', 'ionization state', 'absorption line', 'excitation temperature', 'spectroscopic parallax'],
        evidence=[
            'Hydrogen (Balmer) absorption lines peak in strength around spectral type A (T_eff \u2248 9,000-10,000 K), not at the hottest O stars or the coolest M stars.',
            'The hottest O and B stars show strong ionized helium lines instead, because their higher temperatures ionize most hydrogen atoms, removing the bound electron needed to produce a Balmer absorption line.',
            'The coolest K and M stars show strong molecular bands (e.g., titanium oxide) because low temperatures allow molecules to survive without being dissociated by collisions.',
        ],
        model=[
            'Spectral type is set by surface temperature: which atomic transitions are visible depends on what fraction of atoms are in the right excitation and ionization state to absorb a given wavelength, and that fraction is a strong, non-monotonic function of temperature.',
            'A star\u2019s line strengths therefore measure temperature (and, more weakly, pressure/density) even though essentially all stars share the same dominant composition (about 70% hydrogen, 28% helium by mass).',
            'Luminosity class (from line widths, sensitive to surface gravity) distinguishes a main-sequence dwarf from a giant or supergiant of the same temperature, resolving the ambiguity that temperature alone cannot fix size.',
        ],
        equation=r'\text{line strength} = f(\text{ionization/excitation fraction}) = g(T_{\rm eff}),\ \text{non-monotonic in } T_{\rm eff}',
        example=[
            f'Rank by T_eff: Rigel ({STAR_BY_NAME["Rigel"]["teff"]:.0f} K, B8Ia) > Vega ({STAR_BY_NAME["Vega"]["teff"]:.0f} K, A0V) > Sun ({SUN_TEFF:.0f} K, G2V) > Betelgeuse ({BETELGEUSE["teff"]:.0f} K, M1-2Ia).',
            'Yet Balmer line strength peaks at Vega\u2019s A0 type, not at hotter Rigel: above about 10,000 K, collisions with free electrons increasingly ionize hydrogen past neutral, removing the electron needed for a Balmer transition.',
            'Below about 5,000-6,000 K (Sun and cooler), most hydrogen remains in its unexcited ground state, unable to absorb visible-light Balmer photons, so Balmer lines weaken again even though the gas is still overwhelmingly hydrogen.',
            'This non-monotonic behavior is exactly why the historical alphabetical line-strength ordering (A, B, C, ...) had to be reshuffled into the temperature-ordered OBAFGKM sequence once the physics were understood.',
        ],
        pitfall='Assuming that strong hydrogen lines mean "more hydrogen" and weak hydrogen lines mean "less hydrogen." Line strength primarily reflects excitation/ionization state (i.e., temperature), not elemental abundance.',
        activity='Given three unlabeled spectra (strong Balmer lines; strong ionized helium lines; strong molecular bands), assign each to hot/intermediate/cool without additional information, and justify each assignment.',
        lab_connection='Lab 01 uses each sample star\u2019s spectral type and T_eff to place it correctly on the Hertzsprung-Russell diagram\u2019s temperature axis.',
        synthesis='The OBAFGKM sequence orders stars by temperature, using ionization and excitation physics, not composition, to explain why line strengths rise and fall non-monotonically across it.',
        openstax='OpenStax Astronomy 2e, Chapter 17.1-17.4 (the brightness/spectra of stars and spectral classification) and Chapter 5.5 (formation of spectral lines).',
    ),
    dict(
        n=3, title='How Far Are the Stars? Parallax, Magnitudes, and Distance',
        subtitle='Turning a tiny angle into a distance, and a distance into a true brightness',
        goals=[
            'Compute a star\u2019s distance in parsecs from its measured parallax in arcseconds.',
            'Apply the distance modulus to convert apparent magnitude and distance into absolute magnitude.',
            'Identify where the "V magnitude approximates bolometric magnitude" simplification is reliable and where it is not.',
        ],
        why_matters='Friedrich Bessel measured the first stellar parallax in 1838 (for 61 Cygni), ending millennia of uncertainty about whether stars were even far enough away to have undetectably small parallaxes. Parallax remains the only geometric, model-independent distance method in astronomy; every other stellar distance technique in this course is ultimately calibrated against it.',
        phenomenon=f'Proxima Centauri, the nearest star to the Sun, has a measured parallax of {PROXIMA["parallax_mas"]:.2f} milliarcseconds \u2014 an angle smaller than a coin would subtend from across a continent. Sirius A has a much larger parallax of {SIRIUS_A["parallax_mas"]:.2f} mas because it is closer to us than most naked-eye stars, even though it is intrinsically far more luminous than Proxima.',
        vocab=['parallax angle', 'parsec', 'apparent magnitude', 'absolute magnitude', 'distance modulus', 'bolometric correction'],
        evidence=[
            f'Proxima Centauri: parallax = {PROXIMA["parallax_mas"]:.2f} mas \u2192 distance = {PROXIMA["d_pc"]:.2f} pc.',
            f'Sirius A: parallax = {SIRIUS_A["parallax_mas"]:.2f} mas \u2192 distance = {SIRIUS_A["d_pc"]:.2f} pc.',
            f'Sirius A appears far brighter in our sky (apparent magnitude {SIRIUS_A["v_app"]:.2f}) than Proxima (apparent magnitude {PROXIMA["v_app"]:.2f}), but once distance is accounted for, Sirius A\u2019s absolute magnitude ({SIRIUS_A["mv"]:.2f}) shows it is intrinsically far more luminous than Proxima\u2019s ({PROXIMA["mv"]:.2f}).',
        ],
        model=[
            'Parallax angle p (in arcseconds) and distance d (in parsecs) are related by d = 1/p, by definition of the parsec.',
            'The distance modulus m - M = 5 log10(d) - 5 (d in pc) converts between apparent magnitude m (what we observe) and absolute magnitude M (the magnitude the star would have at 10 pc, a proxy for luminosity).',
            'Using V-band apparent magnitude as a stand-in for bolometric (total) magnitude is a simplifying assumption: it is reasonably good for stars near the Sun\u2019s temperature, but increasingly inaccurate for very hot or very cool stars, which emit large fractions of their light outside the visible band.',
        ],
        equation=r'd(\text{pc}) = \dfrac{1}{p(\text{arcsec})}, \qquad m - M = 5\log_{10}(d) - 5',
        example=[
            f'Sirius A: parallax p = {SIRIUS_A["parallax_mas"]:.2f} mas = {SIRIUS_A["parallax_mas"]/1000:.5f} arcsec, so d = 1/{SIRIUS_A["parallax_mas"]/1000:.5f} = {SIRIUS_A["d_pc"]:.2f} pc.',
            f'Distance modulus: m - M = 5\u00d7log10({SIRIUS_A["d_pc"]:.2f}) - 5 = {SIRIUS_A["dist_mod"]:.3f}.',
            f'Absolute magnitude: M = m - (m-M) = {SIRIUS_A["v_app"]:.2f} - ({SIRIUS_A["dist_mod"]:.3f}) = {SIRIUS_A["mv"]:.2f}.',
            f'Luminosity from M (via L = 10^((Mv,Sun - M)/2.5)): L \u2248 {SIRIUS_A["l_from_mv"]:.1f} L\u2609 \u2014 compare to the Stefan-Boltzmann luminosity from Sirius A\u2019s radius and temperature, {SIRIUS_A["l_from_sb"]:.1f} L\u2609 (agreement to within {abs(SIRIUS_A["l_from_mv"]-SIRIUS_A["l_from_sb"])/SIRIUS_A["l_from_sb"]*100:.0f}%, reasonable for an A-type star where the V-band bolometric-correction assumption is only a mild simplification).',
            f'By contrast, for the much cooler Sun-like Alpha Centauri A the two estimates agree even more closely ({ALPHA_CEN_A["l_from_mv"]:.2f} vs. {ALPHA_CEN_A["l_from_sb"]:.2f} L\u2609), because the bolometric correction is smallest near the Sun\u2019s own temperature.',
        ],
        pitfall='Treating parallax as usable at any distance. Ground- and space-based parallax precision limits (roughly tens of microarcseconds for Gaia) mean parallax distances become unreliable beyond a few kiloparsecs \u2014 other techniques (Lecture 06\u2019s cluster fitting, standard candles in Lecture 14) are needed farther out.',
        activity='Given two stars with the same apparent magnitude but parallaxes of 5 mas and 50 mas, compute which is more luminous and by what factor.',
        lab_connection='Lab 02 applies the distance modulus to the full 20-star sample and cross-checks luminosity estimates from magnitudes against Stefan-Boltzmann estimates from radius and temperature.',
        synthesis='Parallax converts a measured angle into a model-independent distance, and the distance modulus then converts an apparent brightness into an absolute, comparable luminosity.',
        openstax='OpenStax Astronomy 2e, Chapter 19.1-19.2 (fundamental units of distance, surveying the stars) and Chapter 18.1 (magnitudes).',
    ),
    dict(
        n=4, title='Inside a Star: Structure and Nuclear Energy Generation',
        subtitle='What holds a star up, and what powers it',
        goals=[
            'State the condition of hydrostatic equilibrium and explain why stars neither collapse nor explode while on the main sequence.',
            'Describe the proton-proton chain as the Sun\u2019s dominant energy source and compute its net energy release per reaction.',
            'Explain why higher-mass stars burn hydrogen via the CNO cycle instead.',
        ],
        why_matters='Before nuclear fusion was understood (1920s-1930s), no known energy source could power the Sun for its geologically required age of billions of years; gravitational contraction (the Kelvin-Helmholtz mechanism) could only power it for tens of millions of years. Hans Bethe\u2019s 1939 work on the proton-proton chain and CNO cycle resolved this "age of the Sun" problem and remains the foundation of stellar astrophysics.',
        phenomenon='The Sun fuses roughly 6 \u00d7 10\u00b9\u00b9 kg of hydrogen into helium every second, yet loses only about 4 \u00d7 10\u2079 kg of mass per second to radiated energy (E = mc\u00b2) \u2014 a tiny fraction of its total mass, which is why it can shine steadily for billions of years.',
        vocab=['hydrostatic equilibrium', 'proton-proton chain', 'CNO cycle', 'mass defect', 'core temperature', 'radiative/convective transport'],
        evidence=[
            'The Sun\u2019s central pressure and temperature (about 15 million K) are exactly what is required to balance the crushing weight of its overlying layers \u2014 confirmed by helioseismology, which measures the Sun\u2019s internal sound-wave oscillations.',
            'Solar neutrino detectors (starting with the Homestake experiment and confirmed by Super-Kamiokande and SNO) directly detect the neutrinos predicted by the proton-proton chain, confirming fusion is occurring in the Sun\u2019s core right now.',
            'More massive, hotter-cored stars are observed to have far higher CNO-cycle-dominated energy generation rates, consistent with the CNO cycle\u2019s much steeper temperature dependence than the proton-proton chain\u2019s.',
        ],
        model=[
            'Hydrostatic equilibrium: at every radius inside a stable star, outward pressure from hot gas and radiation exactly balances the inward pull of gravity, so the star holds a fixed structure rather than collapsing or expanding.',
            'The proton-proton chain fuses four hydrogen nuclei into one helium-4 nucleus in a sequence of two-body reactions; it dominates in stars with core temperatures below about 18 million K (roughly 1.3 solar masses and below).',
            'The CNO cycle uses carbon, nitrogen, and oxygen nuclei as catalysts to achieve the same net fusion of four protons into helium, but its reaction rate scales far more steeply with temperature, so it dominates in hotter, more massive stars\u2019 cores.',
        ],
        equation=r'4\,{}^{1}\mathrm{H} \rightarrow {}^{4}\mathrm{He} + 2e^{+} + 2\nu_e + \gamma, \qquad \Delta E = \Delta m\,c^{2}',
        example=[
            'Mass of 4 hydrogen-1 nuclei: 4 \u00d7 1.007825 u = 4.031300 u.',
            'Mass of one helium-4 nucleus (plus the two positrons, which promptly annihilate and contribute their energy too): 4.002602 u.',
            'Mass defect: \u0394m = 4.031300 - 4.002602 = 0.028698 u, about 0.71% of the initial mass.',
            'Energy released per reaction: \u0394E = \u0394m c\u00b2 = 0.028698 \u00d7 931.494 MeV = 26.73 MeV \u2014 this is the number that, multiplied by the Sun\u2019s reaction rate, must reproduce the Stefan-Boltzmann luminosity computed in Lecture 01, tying the nuclear-physics energy source directly to the star\u2019s observed radiative output.',
        ],
        pitfall='Thinking a star "burns" hydrogen the way a fire burns fuel (a chemical reaction). Stellar energy generation is nuclear fusion, releasing roughly seven orders of magnitude more energy per unit mass than any chemical reaction, which is precisely why fusion (not chemistry) can power a star for billions of years.',
        activity='Using the mass defect above, estimate how many proton-proton chain reactions per second are needed to produce the Sun\u2019s Stefan-Boltzmann luminosity from Lecture 01, and compare your estimate\u2019s order of magnitude to the commonly quoted solar fusion rate.',
        lab_connection='Lab 02 uses the mass-defect energy release, together with the Sun\u2019s luminosity and mass, to estimate the Sun\u2019s nuclear fuel supply and main-sequence lifetime, previewing Lecture 06.',
        synthesis='Hydrostatic equilibrium explains why a star holds a stable structure, and nuclear fusion (proton-proton chain or CNO cycle, depending on mass) explains where the energy maintaining that structure comes from.',
        openstax='OpenStax Astronomy 2e, Chapter 15.4-15.5 (energy transport, the sun\u2019s interior) and Chapter 16.1-16.2 (mass-energy conversion, the proton-proton chain and CNO cycle).',
    ),
    dict(
        n=5, title='Stellar Nurseries: The Interstellar Medium and Star Formation',
        subtitle='From a cold, diffuse cloud to a nuclear furnace',
        goals=[
            'Describe the major phases of the interstellar medium and their physical conditions.',
            'State the Jeans criterion qualitatively and explain why only the coldest, densest clouds can collapse to form stars.',
            'Trace the observable stages from molecular cloud core to protostar to zero-age main-sequence star.',
        ],
        why_matters='Roughly 10-15% of the Milky Way\u2019s ordinary (baryonic) matter is not locked up in stars at all, but exists as gas and dust between them. This interstellar medium is both the leftover material from earlier generations of stars and the raw material for the next generation \u2014 understanding it explains where stars come from and why star formation continues billions of years after the Galaxy formed.',
        phenomenon='The Orion Nebula, visible to the naked eye as a fuzzy patch in Orion\u2019s sword, is a giant molecular cloud roughly 100 light-years across and about 200,000 solar masses of gas, actively forming thousands of new stars, some of which are directly visible as embedded protostars in infrared images.',
        vocab=['interstellar medium (ISM)', 'molecular cloud', 'H II region', 'Jeans mass', 'protostar', 'T Tauri star', 'zero-age main sequence'],
        evidence=[
            'Molecular clouds are cold (about 10-20 K) and dense (hundreds to thousands of molecules per cm\u00b3 compared to about 1 atom per cm\u00b3 for the ISM average) \u2014 conditions found nowhere else in interstellar space.',
            'Young stellar clusters are consistently found still embedded in or immediately adjacent to molecular clouds, and never found isolated far from any cloud material, exactly as expected if clouds are the birthplace of stars.',
            'Protostars show excess infrared emission from surrounding dusty disks and, in many cases, collimated bipolar jets (Herbig-Haro objects), direct observational signatures of ongoing accretion and outflow.',
        ],
        model=[
            'A cloud can only begin gravitational collapse if its self-gravity exceeds internal pressure support, a competition captured qualitatively by the Jeans criterion: collapse is favored by high density and low temperature, and disfavored by high temperature and low density.',
            'As a collapsing core\u2019s central density and temperature rise, it becomes a protostar, radiating primarily in the infrared because it is still enshrouded in the dusty remnant of its parent cloud.',
            'A protostar reaches the main sequence (becomes a genuine, hydrogen-fusing star) once its core temperature is high enough to sustain steady nuclear fusion, at which point outward radiation and gas pressure balance gravity (hydrostatic equilibrium, Lecture 04) and the star stops contracting.',
        ],
        equation=r'\text{collapse favored when: gravitational energy} > \text{thermal (pressure) energy} \iff M > M_{\rm Jeans} \propto T^{3/2}\rho^{-1/2}',
        example=[
            'A typical Orion Nebula cloud core: T \u2248 10-20 K, n \u2248 10\u2074-10\u2075 molecules/cm\u00b3.',
            f'By contrast, typical diffuse ISM conditions are T \u2248 100-10,000 K, n \u2248 0.1-1 atoms/cm\u00b3, roughly {int(1e4)}-{int(1e6)} times less dense than a collapsing core.',
            'Because the Jeans mass falls with increasing density and decreasing temperature, only the coldest, densest cores within a molecular cloud (not the diffuse ISM as a whole, and not warmer parts of the same cloud) are unstable to collapse \u2014 explaining why star formation is localized to specific cloud cores rather than occurring everywhere at once.',
            f'Once fusion ignites (Lecture 04\u2019s energy-generation physics), the new star settles onto the main sequence and will remain there for a lifetime set by its mass, as quantified in Lecture 06 (a {CLUSTER_TURNOFF_MASS:.0f} M\u2609 star like those forming in Orion will spend about {CLUSTER_TURNOFF_AGE_MYR:.0f} million years on the main sequence).',
        ],
        pitfall='Picturing star formation as instantaneous or as occurring uniformly throughout interstellar space. Star formation is localized to specific, rare, dense cloud cores and unfolds over roughly 10\u2075-10\u2076 years from core collapse to zero-age main sequence, a blink of an eye compared to a star\u2019s subsequent main-sequence lifetime but still far longer than any human timescale.',
        activity='Given two clouds with the same mass but one twice as cold and half as dense as the other, discuss qualitatively which is more likely to be collapsing, using the Jeans-criterion dependence on temperature and density.',
        lab_connection='Lab 03 uses the mass-luminosity relation (Lecture 06) that governs what happens after a protostar like those in Orion reaches the main sequence, to estimate a cluster\u2019s age from its most massive surviving main-sequence star.',
        synthesis='Star formation begins where gravity locally overwhelms pressure support in the coldest, densest interstellar gas, and ends once nuclear fusion switches on and hydrostatic equilibrium takes over.',
        openstax='OpenStax Astronomy 2e, Chapter 20.1-20.2 (the interstellar medium, interstellar gas) and Chapter 21.1 (star formation).',
    ),
    dict(
        n=6, title='Life After the Main Sequence: Giants, Clusters, and Stellar Aging',
        subtitle='Why massive stars live fast and die young',
        goals=[
            'State the mass-luminosity relation and derive the resulting scaling of main-sequence lifetime with mass.',
            'Explain why the Hertzsprung-Russell diagram of a star cluster changes shape as the cluster ages ("main-sequence turnoff").',
            'Estimate a cluster\u2019s age from the mass of its most massive star still on the main sequence.',
        ],
        why_matters='All the stars in a young open cluster form at essentially the same time from the same molecular cloud, but a cluster\u2019s highest-mass stars evolve off the main sequence first, while its lowest-mass stars remain unchanged for tens of billions of years. This "main-sequence turnoff" is one of the most important clocks in astronomy, used to date everything from nearby open clusters to the oldest globular clusters in the Galaxy.',
        phenomenon=f'A {CLUSTER_TURNOFF_MASS:.0f} solar-mass main-sequence star has roughly {ms_luminosity(CLUSTER_TURNOFF_MASS):.0f} times the Sun\u2019s luminosity, yet only 3 times the Sun\u2019s fuel supply \u2014 it must burn through its hydrogen far faster relative to its supply than the Sun does.',
        vocab=['mass-luminosity relation', 'main-sequence lifetime', 'main-sequence turnoff', 'red giant branch', 'helium flash', 'isochrone'],
        evidence=[
            'Observed main-sequence stars show luminosity scaling roughly as the 3.5 power of mass (L \u221d M^3.5) across most of the main sequence, from direct measurements of eclipsing binary systems where both mass and luminosity can be measured independently.',
            'Young open clusters (ages of a few million years) still have their most massive O and B stars on the main sequence, while older open clusters (hundreds of millions of years) have already lost their most massive stars to post-main-sequence evolution, leaving a lower-mass "turnoff point."',
            'Globular clusters, the oldest stellar populations in the Galaxy (roughly 10-13 billion years), have main-sequence turnoffs at stellar masses below the Sun\u2019s, consistent with their great age.',
        ],
        model=[
            'A star\u2019s main-sequence lifetime is proportional to its fuel supply (mass) divided by its fuel consumption rate (luminosity): t \u221d M / L.',
            'Combining this with the mass-luminosity relation L \u221d M^3.5 gives t \u221d M / M^3.5 = M^-2.5, so lifetime falls steeply with increasing mass.',
            'A cluster\u2019s main-sequence turnoff mass therefore directly measures the cluster\u2019s age: only stars below the turnoff mass are still core-hydrogen-burning; more massive stars have already evolved into giants or died.',
        ],
        equation=r'L \propto M^{3.5}, \qquad t_{\rm MS} \propto \dfrac{M}{L} \propto M^{-2.5}, \qquad t_{\rm MS} \approx 10\ \mathrm{Gyr} \times \left(\dfrac{M}{M_\odot}\right)^{-2.5}',
        example=[
            f'The Sun (1 M\u2609): predicted main-sequence lifetime = 10 Gyr \u00d7 1^-2.5 = {ms_lifetime_gyr(1.0):.1f} Gyr, consistent with the Sun\u2019s current age (about 4.6 Gyr) being roughly midway through its main-sequence life.',
            f'A {CLUSTER_TURNOFF_MASS:.0f} M\u2609 star: L = {CLUSTER_TURNOFF_MASS:.0f}^3.5 = {ms_luminosity(CLUSTER_TURNOFF_MASS):.1f} L\u2609; lifetime = 10 Gyr \u00d7 {CLUSTER_TURNOFF_MASS:.0f}^-2.5 = {ms_lifetime_gyr(CLUSTER_TURNOFF_MASS):.3f} Gyr = {CLUSTER_TURNOFF_AGE_MYR:.0f} Myr.',
            f'A 10 M\u2609 star: lifetime = 10 Gyr \u00d7 10^-2.5 \u2248 {ms_lifetime_gyr(10.0)*1000:.0f} Myr \u2014 more than an order of magnitude shorter than the {CLUSTER_TURNOFF_MASS:.0f} M\u2609 case, despite having only about 3 times the mass.',
            f'If we observe a cluster whose main-sequence turnoff is at {CLUSTER_TURNOFF_MASS:.0f} M\u2609 (stars above this mass have already left the main sequence), the cluster\u2019s age is therefore approximately {CLUSTER_TURNOFF_AGE_MYR:.0f} million years \u2014 this is exactly the method used in Lab 03.',
        ],
        pitfall='Assuming more massive stars live longer because they "have more fuel." They do have more fuel, but they burn it so much faster (L \u221d M^3.5) that the net effect is a much shorter lifetime, not a longer one.',
        activity='Rank three stars of 0.5, 2, and 15 solar masses by main-sequence lifetime without a calculator, using only the direction of the M^-2.5 scaling, then check the ranking with the formula.',
        lab_connection='Lab 03 fits a representative cluster\u2019s main-sequence turnoff mass and computes the implied cluster age using this exact relation.',
        synthesis='Because luminosity rises much faster than mass along the main sequence, lifetime falls steeply with mass, turning a cluster\u2019s main-sequence turnoff point into a direct measurement of its age.',
        openstax='OpenStax Astronomy 2e, Chapter 22.1-22.3 (evolution from the main sequence to red giants, star clusters, checking out the theory).',
    ),
    dict(
        n=7, title='The Death of Sun-Like Stars: White Dwarfs and the Chandrasekhar Limit',
        subtitle='What is left when fusion stops',
        goals=[
            'Describe the evolutionary sequence from red giant to planetary nebula to white dwarf for a Sun-like star.',
            'Explain electron degeneracy pressure as the force that supports a white dwarf against gravity.',
            'Compute a white dwarf\u2019s density from its measured mass and radius, and state why the Chandrasekhar limit exists.',
        ],
        why_matters='Sirius B, the first white dwarf discovered (from its gravitational effect on Sirius A\u2019s motion, long before it could be directly imaged), forced nineteenth- and twentieth-century astronomers to accept that stellar matter can exist in a state with no terrestrial analog: matter compressed to planetary size while retaining roughly a solar mass, supported not by thermal pressure but by a purely quantum-mechanical effect.',
        phenomenon=f'Sirius B has a measured mass of {SIRIUS_B["r_rsun"]*0+1.018:.3f} M\u2609 (from its orbit around Sirius A) yet a measured radius of only {SIRIUS_B["r_rsun"]:.6f} R\u2609 \u2014 about the size of Earth. Packing a solar mass into an Earth-sized volume implies an extraordinary density.',
        vocab=['white dwarf', 'planetary nebula', 'electron degeneracy pressure', 'Chandrasekhar limit', 'Pauli exclusion principle', 'carbon-oxygen core'],
        evidence=[
            f'Sirius B: mass = 1.018 \u00b1 0.011 M\u2609, radius = {SIRIUS_B["r_rsun"]:.6f} R\u2609 = 5,634 km, effective temperature = 25,000 K, luminosity = 0.0245 L\u2609 (Bond et al. 2017, Hipparcos parallax of 2.637 pc).',
            'No known main-sequence star has anywhere near Sirius B\u2019s combination of solar-scale mass and Earth-scale radius; ordinary thermal (ideal-gas) pressure cannot support such an object.',
            'No white dwarf has ever been observed with a mass above about 1.4 M\u2609, and theoretical calculations independently predict exactly this mass as the maximum electron degeneracy pressure can support.',
        ],
        model=[
            'When a Sun-like star exhausts its core hydrogen and later helium, it sheds its outer layers as a planetary nebula, exposing a hot, compact carbon-oxygen core: the white dwarf.',
            'A white dwarf is supported against further gravitational collapse not by thermal pressure but by electron degeneracy pressure, a quantum-mechanical consequence of the Pauli exclusion principle: electrons packed to extremely high density resist further compression regardless of temperature.',
            'Because degeneracy pressure has a maximum it can supply for a given mass, there is a maximum possible white dwarf mass, the Chandrasekhar limit (about 1.4 M\u2609); above this mass, degeneracy pressure cannot halt collapse.',
        ],
        equation=r'\rho = \dfrac{M}{\tfrac{4}{3}\pi R^{3}}, \qquad M_{\rm Chandrasekhar} \approx 1.4\ M_\odot',
        example=[
            f'Sirius B: M = {SIRIUS_B_MASS_KG:.3e} kg, R = {SIRIUS_B_RADIUS_M:.3e} m.',
            f'Volume = (4/3)\u03c0R\u00b3 = {SIRIUS_B_VOLUME_M3:.3e} m\u00b3.',
            f'Density = M / V = {SIRIUS_B_DENSITY_KGM3:.3e} kg/m\u00b3 \u2248 {SIRIUS_B_DENSITY_KGM3/1000:.2e} g/cm\u00b3.',
            f'For comparison, water has a density of 1,000 kg/m\u00b3 and Earth\u2019s average density is about 5,510 kg/m\u00b3: Sirius B is roughly {SIRIUS_B_DENSITY_KGM3/1000:.0f} times denser than water and about {SIRIUS_B_DENSITY_KGM3/5510:.0f} times denser than the entire Earth.',
            f'Sirius B\u2019s mass (1.018 M\u2609) sits safely below the Chandrasekhar limit ({CHANDRASEKHAR_LIMIT_MSUN} M\u2609), consistent with its stable, observed existence as a white dwarf rather than undergoing further collapse.',
        ],
        pitfall='Thinking a white dwarf is still generating energy by fusion. A white dwarf has no nuclear fuel left; its faint residual glow (and its slow cooling over billions of years) is purely leftover thermal energy radiating away, not ongoing energy production.',
        activity='Using the Chandrasekhar limit, predict what happens to a white dwarf in a binary system that slowly accretes mass from a companion star and approaches 1.4 M\u2609 (this scenario returns in Lecture 08 as one supernova pathway).',
        lab_connection='Lab 04 uses Sirius B\u2019s measured mass and radius to compute its density and compare it to the Chandrasekhar limit and to nuclear density, quantifying just how extreme a white dwarf is.',
        synthesis='A white dwarf is a stellar remnant supported by electron degeneracy pressure rather than fusion, and this quantum-mechanical support has a hard mass limit (Chandrasekhar, about 1.4 M\u2609) above which no white dwarf can exist.',
        openstax='OpenStax Astronomy 2e, Chapter 23.1 (the death of low-mass stars).',
    ),
    dict(
        n=8, title='Cataclysmic Endings: Supernovae, Neutron Stars, and Pulsars',
        subtitle='Two very different ways for a star to die violently',
        goals=[
            'Distinguish Type Ia supernovae (thermonuclear, white-dwarf origin) from Type II supernovae (core-collapse, massive-star origin).',
            'Explain why a collapsing stellar core can form a neutron star supported by neutron degeneracy pressure.',
            'Describe how pulsars provide direct observational evidence for neutron stars.',
        ],
        why_matters='Supernovae are rare (a few per century per galaxy) but transformative: they seed the interstellar medium with heavy elements forged in the star\u2019s final moments, trigger new star formation through their shocks, and, in the Type Ia case, provide the "standard candles" used in Lecture 14 to measure cosmic distances and discover the accelerating expansion of the universe.',
        phenomenon='SN 1987A, a Type II supernova in the Large Magellanic Cloud, was detected simultaneously in neutrinos (by underground detectors) hours before its light reached Earth-based telescopes \u2014 direct confirmation that core collapse and neutrino emission precede the visible explosion.',
        vocab=['Type Ia supernova', 'Type II (core-collapse) supernova', 'neutron star', 'neutron degeneracy pressure', 'pulsar', 'supernova remnant'],
        evidence=[
            'Type Ia supernovae occur in binary systems where a white dwarf accretes mass from a companion (or merges with another white dwarf) and approaches the Chandrasekhar limit (Lecture 07), triggering runaway carbon fusion that disrupts the entire star \u2014 no compact remnant is left behind.',
            f'Type II supernovae occur when a massive star ({">"} about 8 M\u2609) exhausts its nuclear fuel; its iron core cannot release energy by further fusion (iron has the tightest-bound nucleons of any element) and collapses catastrophically, typically leaving behind a neutron star.',
            'Pulsars (discovered by Jocelyn Bell Burnell in 1967) are rapidly rotating neutron stars whose beamed radio emission sweeps past Earth like a lighthouse, with pulse periods from milliseconds to several seconds, directly confirming neutron stars\u2019 predicted small size and rapid rotation.',
        ],
        model=[
            'A Type Ia supernova has a strikingly uniform peak luminosity, because it always results from a white dwarf reaching (nearly) the same critical mass (the Chandrasekhar limit) before exploding \u2014 the basis for its use as a "standard candle."',
            'A Type II supernova\u2019s core collapse compresses protons and electrons into neutrons (inverse beta decay), releasing a burst of neutrinos and leaving behind a neutron star supported by neutron degeneracy pressure, the neutron analog of the electron degeneracy pressure that supports white dwarfs.',
            'A neutron star\u2019s rapid rotation and strong magnetic field can channel radiation into narrow beams; if a beam sweeps across Earth\u2019s line of sight once per rotation, we observe it as a pulsar.',
        ],
        equation=r'\text{conservation of angular momentum:}\quad I_{\rm core}\,\omega_{\rm core} \approx I_{\rm neutron\ star}\,\omega_{\rm neutron\ star}',
        example=[
            'A typical massive-star core has a radius of order 10\u2074 km (comparable to Earth) and rotates roughly once per month, similar to the Sun.',
            'After core collapse to a neutron star of radius about 10 km \u2014 a factor of roughly 1,000 smaller in radius \u2014 conservation of angular momentum (I \u221d R\u00b2 for a uniform sphere) requires the rotation rate to increase by roughly (1,000)\u00b2 = 10\u2076.',
            'A core rotating once per month (period \u2248 2.6 \u00d7 10\u2076 s) would then rotate with a period near 2.6 \u00d7 10\u2076 / 10\u2076 \u2248 2.6 s after collapse \u2014 the right order of magnitude for many observed pulsar periods, and a direct illustration of why neutron stars are predicted (and observed) to spin rapidly.',
            'The fastest known "millisecond pulsars" spin even faster than this estimate, because they have been subsequently spun up by accreting matter (and angular momentum) from a companion star after formation.',
        ],
        pitfall='Assuming all supernovae are the same kind of event. Type Ia (thermonuclear, no remnant, from white dwarfs) and Type II (core-collapse, neutron star or black hole remnant, from massive stars) have completely different progenitors, mechanisms, and observational signatures, even though both are called "supernovae."',
        activity='Given a description of a supernova\u2019s host environment (e.g., "occurred in an old population with no young massive stars nearby" versus "occurred at the site of a known blue supergiant"), classify it as more likely Type Ia or Type II and justify the reasoning.',
        lab_connection='Lab 04 also compares Sirius B\u2019s mass to the Chandrasekhar limit as the trigger condition relevant to Type Ia supernovae, connecting Lecture 07\u2019s white dwarf physics to this lecture\u2019s explosion mechanism.',
        synthesis='Type Ia and Type II supernovae are physically distinct events unified only by their explosive brightness; conservation of angular momentum during core collapse naturally explains why the resulting neutron stars can spin extremely rapidly.',
        openstax='OpenStax Astronomy 2e, Chapter 23.2-23.4 (evolution of massive stars, supernova observations, pulsars and the discovery of neutron stars).',
    ),
    dict(
        n=9, title='Black Holes and Curved Spacetime',
        subtitle='When even degeneracy pressure is not enough',
        goals=[
            'Compute the Schwarzschild radius for a given mass and explain its physical meaning as an event horizon.',
            'Explain why black holes form when a collapsing core exceeds the maximum mass supportable by neutron degeneracy pressure.',
            'Describe two independent lines of observational evidence for black holes.',
        ],
        why_matters='Neutron degeneracy pressure, like electron degeneracy pressure, has a maximum mass it can support (roughly 2-3 M\u2609 for neutron stars). Beyond that mass, physics as currently understood allows no known force to halt gravitational collapse, leading to a black hole \u2014 once a theoretical curiosity of general relativity, now directly imaged (Event Horizon Telescope, 2019) and detected via gravitational waves from merging black holes (LIGO/Virgo, since 2015).',
        phenomenon='The Event Horizon Telescope\u2019s 2019 image of the supermassive black hole in M87 directly showed a dark central shadow surrounded by a bright ring of glowing gas, matching general-relativistic predictions for a black hole\u2019s event horizon and photon ring to within observational precision.',
        vocab=['Schwarzschild radius', 'event horizon', 'singularity', 'stellar-mass black hole', 'supermassive black hole', 'gravitational wave'],
        evidence=[
            'X-ray binaries such as Cygnus X-1 show a compact object whose mass (measured from its orbit with a visible companion star) exceeds the maximum possible neutron star mass, yet which emits no detectable surface radiation of its own \u2014 consistent with a black hole rather than a neutron star.',
            'LIGO and Virgo have directly detected gravitational waves from dozens of merging black hole pairs since 2015, with masses and waveforms matching general-relativistic predictions for black hole inspiral and merger.',
            'The Event Horizon Telescope imaged the shadow of the supermassive black hole in M87 (2019) and Sagittarius A* at the Milky Way\u2019s center (2022), both consistent with the predicted size for their independently measured masses.',
        ],
        model=[
            'A black hole\u2019s event horizon is the boundary within which the escape velocity exceeds the speed of light, so no light or information can escape from inside it.',
            'The Schwarzschild radius R_s = 2GM/c\u00b2 gives the event horizon radius for a non-rotating black hole of mass M; it scales linearly with mass, so more massive black holes have larger (not smaller) event horizons.',
            'Black holes form when a collapsing core exceeds the maximum mass supportable by neutron degeneracy pressure (roughly 2-3 M\u2609); above that, general relativity predicts unstoppable collapse to a singularity cloaked by an event horizon.',
        ],
        equation=r'R_s = \dfrac{2GM}{c^{2}}',
        example=[
            f'For a 10 M\u2609 stellar-mass black hole: M = 10 \u00d7 {M_SUN_KG:.3e} kg = {10*M_SUN_KG:.3e} kg.',
            f'R_s = 2 \u00d7 {G_NEWTON:.3e} \u00d7 {10*M_SUN_KG:.3e} / ({2.998e8:.3e})\u00b2 = {2*G_NEWTON*10*M_SUN_KG/(2.998e8)**2:.1f} m \u2248 {2*G_NEWTON*10*M_SUN_KG/(2.998e8)**2/1000:.1f} km.',
            f'For the Milky Way\u2019s central supermassive black hole, Sagittarius A* (mass \u2248 4.3 \u00d7 10\u2076 M\u2609): R_s = 2 \u00d7 {G_NEWTON:.3e} \u00d7 (4.3e6 \u00d7 {M_SUN_KG:.3e}) / ({2.998e8:.3e})\u00b2 \u2248 {2*G_NEWTON*4.3e6*M_SUN_KG/(2.998e8)**2/1000:.2e} km \u2014 roughly {2*G_NEWTON*4.3e6*M_SUN_KG/(2.998e8)**2/1000 / (2*G_NEWTON*10*M_SUN_KG/(2.998e8)**2/1000):.0f} times larger than the 10 M\u2609 case, directly illustrating that R_s scales linearly with mass.',
        ],
        pitfall='Imagining a black hole as a "cosmic vacuum cleaner" that pulls in everything nearby with unusually strong gravity. Outside the event horizon, a black hole\u2019s gravity is identical to that of any other object of the same mass; a Sun-mass black hole at the Sun\u2019s current distance would not pull Earth in any harder than the Sun already does.',
        activity='Compute the Schwarzschild radius for Earth\u2019s mass (5.97 \u00d7 10\u00b2\u2074 kg) and compare it to Earth\u2019s actual radius, to see why Earth is nowhere close to being a black hole.',
        lab_connection='Lab 05 extends this gravitational reasoning (v\u00b2R/G mass estimates) to the Milky Way\u2019s rotation curve, using the same Newtonian gravity that gives the weak-field limit of the black hole physics developed here.',
        synthesis='Black holes are the endpoint of collapse for cores too massive for neutron degeneracy pressure to support, with an event horizon size (Schwarzschild radius) that scales linearly with mass and is now directly probed by gravitational-wave and imaging observations.',
        openstax='OpenStax Astronomy 2e, Chapter 24.1-24.3 (introduction to relativity and time dilation, spacetime, black holes and their observation).',
    ),
    dict(
        n=10, title='The Milky Way: Structure, Rotation, and the Case for Dark Matter',
        subtitle='Weighing a galaxy by how fast it spins',
        goals=[
            'Describe the Milky Way\u2019s major structural components (disk, bulge, halo).',
            'Explain how a galaxy\u2019s rotation curve is measured and what a "flat" rotation curve implies about its mass distribution.',
            'Estimate the enclosed mass of the Milky Way at different radii from rotation-curve data.',
        ],
        why_matters='The Milky Way\u2019s rotation curve was one of the first and remains one of the most direct pieces of evidence for dark matter: if all of the Galaxy\u2019s mass were in the visible stars and gas, rotation speeds should decline with radius outside the visible disk, the way planets slow down at greater distances from the Sun. They do not.',
        phenomenon=f'Stars and gas clouds far outside the Sun\u2019s orbital radius (measured via 21-cm radio observations of neutral hydrogen, unaffected by dust) are observed orbiting the Galactic center at roughly the same speed (about {V_SUN_KMS:.0f} km/s) as material near the Sun\u2019s orbit, rather than slowing down as visible starlight and gas density drop off.',
        vocab=['galactic disk', 'galactic bulge', 'galactic halo', 'rotation curve', 'dark matter halo', '21-cm line'],
        evidence=[
            f'The Sun orbits the Galactic center at radius R\u2080 \u2248 {R_SUN_KPC:.1f} kpc with orbital speed V\u2080 \u2248 {V_SUN_KMS:.0f} km/s.',
            'Radio observations of neutral hydrogen (21-cm emission) at radii well beyond the visible stellar disk show rotation speeds that stay roughly flat (not declining) out to at least 25 kpc.',
            'The amount of visible matter (stars + gas) drops off sharply beyond about 15 kpc, yet the rotation speed does not \u2014 directly implying that most of the Galaxy\u2019s gravitating mass at large radii is not visible.',
        ],
        model=[
            'For a test mass orbiting in a circular orbit, Newtonian gravity gives the enclosed mass at radius R as M(R) = V(R)\u00b2 R / G, where V(R) is the circular orbital speed.',
            'If nearly all mass were interior to the visible disk (as for the solar system, where nearly all mass is in the Sun), V(R) should decline as 1/\u221aR beyond the visible mass, the way planetary orbital speeds decline with distance from the Sun.',
            'Because V(R) instead stays roughly flat out to large R, M(R) must keep growing linearly with R, implying an extended, largely invisible ("dark") mass distribution well beyond the visible disk.',
        ],
        equation=r'M(R) = \dfrac{V(R)^{2} R}{G}',
        example=[
            f'At the Sun\u2019s radius, R\u2080 = {R_SUN_KPC:.1f} kpc = {R_SUN_KPC*KPC_M:.3e} m, V\u2080 = {V_SUN_KMS:.0f} km/s = {V_SUN_KMS*KM:.3e} m/s.',
            f'M(R\u2080) = ({V_SUN_KMS*KM:.3e})\u00b2 \u00d7 {R_SUN_KPC*KPC_M:.3e} / {G_NEWTON:.3e} = {MASS_AT_SUN_MSUN*M_SUN_KG:.3e} kg = {MASS_AT_SUN_MSUN:.3e} M\u2609.',
            f'At R = 25 kpc, V \u2248 230 km/s (still nearly flat): M(25 kpc) = {MASS_AT_25KPC_MSUN:.3e} M\u2609, roughly {MASS_AT_25KPC_MSUN/MASS_AT_SUN_MSUN:.2f} times the enclosed mass at the Sun\u2019s radius, even though the radius only increased by a factor of {25/R_SUN_KPC:.2f}.',
            f'The Galaxy\u2019s visible stellar and gas mass is estimated at only about {VISIBLE_MASS_MSUN:.1e} M\u2609 \u2014 far less than the {MASS_AT_25KPC_MSUN:.2e} M\u2609 implied by the rotation curve at 25 kpc, requiring roughly {MASS_AT_25KPC_MSUN/VISIBLE_MASS_MSUN:.1f} times more mass than is visible, attributed to a dark matter halo.',
        ],
        pitfall='Assuming "dark matter" means "dark, ordinary matter we just haven\u2019t seen yet" (like cold gas or dim stars). Multiple independent lines of evidence (rotation curves, gravitational lensing, the cosmic microwave background, large-scale structure) point to a non-baryonic form of matter that does not emit, absorb, or scatter light at all, distinguishing it from merely faint ordinary matter.',
        activity='Using M(R) = V\u00b2R/G, predict what a rotation curve would look like (rising, flat, or falling with R) if the Galaxy\u2019s mass were entirely enclosed within the Sun\u2019s orbital radius, and compare to the observed flat curve.',
        lab_connection='Lab 05 computes enclosed mass at several radii from a representative rotation-curve data set and compares the result to the Galaxy\u2019s visible mass.',
        synthesis='A flat rotation curve, combined with Newtonian gravity, implies a mass distribution that keeps growing well beyond the visible disk \u2014 the central piece of evidence for the Milky Way\u2019s dark matter halo.',
        openstax='OpenStax Astronomy 2e, Chapter 25.1-25.4 (the structure of the galaxy, spiral structure, the mass of the galaxy, the galactic center).',
    ),
    dict(
        n=11, title='Sorting the Galaxies: The Hubble Tuning Fork and Galaxy Properties',
        subtitle='A classification scheme that still organizes extragalactic astronomy',
        goals=[
            'Classify a galaxy image using the Hubble tuning fork (elliptical, spiral, barred spiral, irregular).',
            'Connect galaxy morphology to stellar population age, gas content, and star-formation activity.',
            'Explain what the tuning-fork diagram does and does not imply about galaxy evolution.',
        ],
        why_matters='Edwin Hubble\u2019s 1926 galaxy classification scheme, though originally conceived (incorrectly) as an evolutionary sequence from ellipticals to spirals, remains in near-universal use today as a purely morphological classification, precisely because morphology correlates strongly with physically meaningful properties: gas content, ongoing star formation, and stellar population age.',
        phenomenon=f'{GALAXIES[0][0]}, type {GALAXIES[0][1]}, and {GALAXIES[1][0]}, type {GALAXIES[1][1]}, look completely different: one is a flattened disk with prominent spiral arms and active star formation, the other a smooth, featureless ball of old, red stars with no ongoing star formation. Yet both are among the most massive galaxies in the nearby universe.',
        vocab=['Hubble tuning fork', 'elliptical galaxy', 'spiral galaxy', 'barred spiral galaxy', 'irregular galaxy', 'bulge-to-disk ratio'],
        evidence=[
            f'{GALAXIES[1][0]} ({GALAXIES[1][1]}): a giant elliptical at the center of the Virgo Cluster, {GALAXIES[1][2]:.1f} Mpc away, with essentially no cold gas or ongoing star formation and an old, red stellar population. {GALAXIES[1][4]}',
            f'{GALAXIES[2][0]} ({GALAXIES[2][1]}): a nearly face-on spiral, {GALAXIES[2][2]:.1f} Mpc away, rich in cold gas and dust with prominent blue, young star-forming regions along its spiral arms. {GALAXIES[2][4]}',
            f'{GALAXIES[4][0]} ({GALAXIES[4][1]}): {GALAXIES[4][2]:.1f} Mpc away, {GALAXIES[4][4]}',
        ],
        model=[
            'Elliptical galaxies (E0-E7, by apparent flattening) are smooth, roughly featureless, gas-poor systems dominated by old stars on randomly oriented orbits, with little or no ongoing star formation.',
            'Spiral galaxies (Sa-Sc, or barred SBa-SBc) are flattened, rotating disks with a central bulge, spiral arms traced by young blue stars and star-forming gas, and a bulge-to-disk ratio that decreases from Sa to Sc.',
            'Irregular galaxies have no organized symmetric structure at all, often as a result of gravitational disturbance from a close companion, as in the case of a starburst triggered by a recent tidal interaction.',
        ],
        equation=r'\text{Hubble type} \leftrightarrow (\text{bulge-to-disk ratio}, \text{gas fraction}, \text{ongoing star formation rate})',
        example=[
            f'{GALAXIES[3][0]} ({GALAXIES[3][1]}): {GALAXIES[3][2]:.1f} Mpc away, an edge-on early-type spiral. {GALAXIES[3][4]}',
            f'{GALAXIES[5][0]} ({GALAXIES[5][1]}): {GALAXIES[5][2]:.1f} Mpc away. {GALAXIES[5][4]}',
            'Comparing all six sample galaxies: the elliptical (M87) and the early-type spiral (M104, large bulge) both have relatively little ongoing star formation, while the later-type spirals (M101) and the starburst irregular (M82) show intense, ongoing star formation \u2014 morphology and star-formation activity track each other closely across the sample, exactly as the tuning-fork classification predicts.',
        ],
        pitfall='Interpreting the tuning-fork diagram as a literal evolutionary sequence, with ellipticals evolving into spirals (Hubble\u2019s original, incorrect, "early type"/"late type" terminology, still used today purely as a label). Modern evidence instead suggests many ellipticals form from mergers of spirals, the reverse of Hubble\u2019s original intuition.',
        activity='Given a galaxy image showing a smooth, featureless, gas-poor system with no blue star-forming regions, predict its Hubble type and expected stellar population age without additional information.',
        lab_connection='Lab 06 classifies all six sample galaxies (plus additional images) on the Hubble tuning fork and connects each classification to measurable properties (gas content, star-formation rate, bulge-to-disk ratio).',
        synthesis='The Hubble tuning fork is a purely morphological classification that nonetheless correlates strongly with real physical differences in gas content, stellar population age, and star-formation activity across galaxy types.',
        openstax='OpenStax Astronomy 2e, Chapter 26.1-26.3 (the discovery of galaxies, types of galaxies, properties of galaxies).',
    ),
    dict(
        n=12, title='Active Galaxies and Galaxy Evolution',
        subtitle='Supermassive black holes as galactic engines, and galaxies that eat each other',
        goals=[
            'Explain the unified model of active galactic nuclei (AGN) as accretion onto a supermassive black hole.',
            'Describe how galaxy mergers and interactions drive starbursts and reshape galaxy morphology.',
            'Connect AGN feedback to the observed correlation between supermassive black hole mass and host-galaxy properties.',
        ],
        why_matters='Nearly every massive galaxy, including the Milky Way, hosts a supermassive black hole at its center; in a small but important fraction of galaxies, that black hole is actively accreting matter and outshining the entire rest of the galaxy. Understanding active galactic nuclei connects the black hole physics of Lecture 09 directly to the large-scale structure and evolution of galaxies themselves.',
        phenomenon='Quasars, the most luminous class of active galactic nucleus, can outshine their entire host galaxy of hundreds of billions of stars from a region not much larger than the solar system \u2014 a fact that puzzled astronomers for decades until supermassive black hole accretion was identified as the only known power source compact and efficient enough to explain it.',
        vocab=['active galactic nucleus (AGN)', 'quasar', 'accretion disk', 'relativistic jet', 'galaxy merger', 'AGN feedback'],
        evidence=[
            'AGN luminosities and rapid variability (sometimes on timescales of days) require an extremely compact power source, consistent with accretion onto a supermassive black hole of millions to billions of solar masses rather than any stellar process.',
            'Deep imaging surveys show that many active galaxies show clear signs of recent or ongoing gravitational interaction (tidal tails, disturbed morphology, close companions), and that merging galaxies show elevated star-formation and nuclear-activity rates compared to isolated galaxies.',
            'Observed supermassive black hole masses correlate tightly with their host galaxy\u2019s bulge mass and stellar velocity dispersion (the M-sigma relation), implying that black hole growth and galaxy (bulge) growth are physically linked, likely through AGN feedback regulating star formation.',
        ],
        model=[
            'The unified AGN model attributes the diversity of observed active galaxy types (Seyfert galaxies, quasars, radio galaxies, blazars) to viewing the same basic structure (supermassive black hole, accretion disk, dusty torus, and in some cases relativistic jets) from different angles and at different accretion rates.',
            'Galaxy mergers funnel gas toward galactic centers through gravitational torques, simultaneously triggering bursts of star formation and fueling enhanced black hole accretion \u2014 a natural mechanism linking galaxy interactions to both starbursts and AGN activity.',
            'AGN feedback (radiation pressure and jets from the accreting black hole) can heat or expel surrounding gas, suppressing further star formation and helping to explain why the most massive galaxies today have comparatively little ongoing star formation.',
        ],
        equation=r'M_{\rm BH} \propto \sigma^{4-5}\ \ (\text{the } M\text{-}\sigma \text{ relation, an empirical correlation, not a first-principles law})',
        example=[
            'The Milky Way\u2019s own central black hole, Sagittarius A* (about 4.3 \u00d7 10\u2076 M\u2609, from Lecture 09), is not currently a luminous AGN because it is accreting matter only very slowly \u2014 illustrating that a supermassive black hole\u2019s presence alone does not make a galaxy "active"; the accretion rate matters as much as the black hole\u2019s mass.',
            'M87\u2019s central black hole (about 6.5 \u00d7 10\u2079 M\u2609, directly imaged by the Event Horizon Telescope) does power an active nucleus, including a well-known relativistic jet extending thousands of light-years, visible across the electromagnetic spectrum from radio to X-rays.',
            'M82 (Lecture 11\u2019s starburst irregular) shows both intense star formation and a galactic-scale outflow (superwind) driven by combined supernova and possibly nuclear-accretion energy input, following its gravitational disturbance by its neighbor M81 \u2014 a nearby, well-studied example of interaction-triggered activity.',
        ],
        pitfall='Assuming every galaxy with a supermassive black hole is an "active galaxy." Almost all massive galaxies, including the Milky Way and Andromeda, host a supermassive black hole, but only a minority are actively accreting enough matter to qualify as AGN at any given time.',
        activity='Given the M-sigma relation\u2019s implication that black hole and bulge growth are linked, discuss what observation would help distinguish whether black hole growth drives bulge growth, bulge growth drives black hole growth, or a third process drives both together.',
        lab_connection='Lab 06\u2019s galaxy classification exercise includes M87\u2019s AGN-hosting elliptical morphology and M82\u2019s merger-triggered starburst irregular morphology as concrete examples of this lecture\u2019s evolutionary processes.',
        synthesis='Active galactic nuclei are powered by accretion onto supermassive black holes, and galaxy mergers provide a physical mechanism that links starbursts, AGN fueling, and the observed correlation between black hole mass and host-galaxy properties.',
        openstax='OpenStax Astronomy 2e, Chapter 27.1-27.4 (quasars, supermassive black holes, radio galaxies, active galactic nuclei) and Chapter 28.1-28.2 (galaxy formation, galaxy interactions and mergers).',
    ),
    dict(
        n=13, title='The Cosmic Web: Large-Scale Structure and Dark Energy',
        subtitle='Galaxies are not scattered randomly through space',
        goals=[
            'Describe the filamentary, web-like distribution of galaxies revealed by large redshift surveys.',
            'Summarize the observational evidence for dark matter on cluster and cosmological scales, beyond individual galaxy rotation curves.',
            'State the basic observational case for dark energy from Type Ia supernova distance measurements.',
        ],
        why_matters='Large galaxy redshift surveys (the CfA survey in the 1980s, the Sloan Digital Sky Survey since 2000) revealed that galaxies are not scattered randomly through space but trace an enormous filamentary "cosmic web" of walls, filaments, and voids hundreds of millions of light-years across \u2014 structure that must trace the gravitational scaffolding of dark matter assembled since the early universe.',
        phenomenon='The Sloan Great Wall, a filament of galaxies over a billion light-years long, is one of the largest known coherent structures in the observable universe, far larger than any single galaxy or galaxy cluster, yet its existence is a natural prediction of gravitational structure growth from small initial density fluctuations amplified over billions of years.',
        vocab=['cosmic web', 'galaxy filament', 'void', 'galaxy cluster', 'gravitational lensing', 'dark energy'],
        evidence=[
            'Galaxy cluster masses estimated from the motions of member galaxies (using the same v\u00b2R/G logic as Lecture 10\u2019s rotation curves, applied statistically) consistently exceed the visible stellar and gas mass by a factor of several, echoing the individual-galaxy dark matter evidence at a much larger scale.',
            'Gravitational lensing (the bending of background light by foreground mass, predicted by general relativity) directly maps the total mass distribution in galaxy clusters, independent of whether that mass is visible, and consistently reveals far more mass than visible light accounts for.',
            'Distant Type Ia supernovae (Lecture 08\u2019s "standard candles") appear systematically fainter than expected for a universe whose expansion is slowing down under gravity alone, implying the expansion is instead accelerating (Riess, Perlmutter, and Schmidt, Nobel Prize 2011) \u2014 attributed to dark energy.',
        ],
        model=[
            'Small density fluctuations in the early universe grew over billions of years under gravity, with dark matter (which does not interact electromagnetically) collapsing first and forming a scaffold into which ordinary (baryonic) gas later fell to form galaxies along filaments and at filament intersections.',
            'On cosmological scales, the total energy budget of the universe is dominated not by ordinary matter or even dark matter, but by dark energy, an unexplained form of energy (possibly a property of space itself) causing the universe\u2019s expansion to accelerate rather than decelerate.',
            'The current cosmological consensus ("Lambda-CDM") apportions roughly 5% ordinary matter, 25% dark matter, and 70% dark energy to the universe\u2019s total energy content, an accounting built from multiple independent lines of evidence (rotation curves, lensing, supernovae, and the cosmic microwave background).',
        ],
        equation=r'\Omega_{\rm baryon} \approx 0.05, \qquad \Omega_{\rm dark\ matter} \approx 0.25, \qquad \Omega_{\rm dark\ energy} \approx 0.70',
        example=[
            'A galaxy cluster like Coma, with hundreds of member galaxies, shows individual galaxy velocities of order 1,000 km/s relative to the cluster mean \u2014 far too large to be gravitationally bound by the cluster\u2019s visible galaxy mass alone (an argument dating back to Fritz Zwicky\u2019s pioneering 1933 study of the Coma Cluster, the historical origin of the term "dark matter").',
            'Gravitational lensing maps of merging clusters (such as the Bullet Cluster) show that the lensing mass (inferred from background image distortion) is spatially offset from the hot X-ray-emitting gas (the dominant visible baryonic mass), directly demonstrating that most cluster mass is not the visible hot gas and behaves differently during the merger \u2014 strong, largely model-independent evidence against dark matter simply being unseen ordinary matter.',
            'If dark energy is well-described by a cosmological constant, its effect on the expansion rate becomes increasingly important at late cosmic times as matter density dilutes with the growing volume of space, exactly the pattern needed to explain why the acceleration was not detected until measurements reached sufficiently distant (early-epoch) supernovae.',
        ],
        pitfall='Conflating dark matter and dark energy. Dark matter clumps gravitationally and explains structure formation and excess gravitating mass; dark energy is smoothly distributed and drives accelerating expansion \u2014 they solve different observational puzzles and are supported by largely independent evidence.',
        activity='Given the Bullet Cluster\u2019s spatial offset between lensing mass and hot gas, explain in your own words why this observation is difficult to reconcile with dark matter simply being unseen ordinary (baryonic) matter.',
        lab_connection='Lab 07 uses Type Ia-supernova-style standard-candle reasoning (via Hubble\u2019s law, Lecture 14) as the observational entry point to the same accelerating-expansion evidence introduced here.',
        synthesis='Large-scale structure, cluster dynamics, and gravitational lensing extend the case for dark matter from individual galaxies to the largest cosmic scales, while independent supernova distance measurements reveal a second, distinct dark component: dark energy, driving accelerating cosmic expansion.',
        openstax='OpenStax Astronomy 2e, Chapter 28.3-28.5 (the challenge of dark matter, the crucial role of dark matter, and cosmology; connects forward to Chapter 29).',
    ),
    dict(
        n=14, title="Hubble's Law and the Big Bang: Observational Cosmology",
        subtitle='Turning a redshift-distance plot into the age of the universe',
        goals=[
            'State Hubble\u2019s law and use redshift-distance data to estimate the Hubble constant.',
            'Explain how the Hubble constant sets an approximate age for the universe (the Hubble time).',
            'Summarize the observational pillars of the Big Bang model.',
        ],
        why_matters='Edwin Hubble\u2019s 1929 discovery that galaxies\u2019 recession velocities are proportional to their distance was the first direct observational evidence that the universe is expanding, transforming cosmology from philosophical speculation into a quantitative, testable science and eventually leading to the Big Bang model this lecture summarizes.',
        phenomenon=f'A sample of five well-studied galaxy clusters, spanning distances from about {HUBBLE_CLUSTERS[0][1]:.1f} Mpc (Virgo) to about {HUBBLE_CLUSTERS[-1][1]:.0f} Mpc (Bootes), shows recession velocities that increase in direct proportion to distance \u2014 exactly the linear relationship Hubble first identified with a far smaller and less precise data set in 1929.',
        vocab=["Hubble's law", 'Hubble constant', 'Hubble time', 'redshift', 'cosmic microwave background', 'Big Bang nucleosynthesis'],
        evidence=[
            f'Virgo Cluster: distance \u2248 {HUBBLE_CLUSTERS[0][1]:.1f} Mpc, recession velocity \u2248 {HUBBLE_CLUSTERS[0][2]:.0f} km/s.',
            f'Corona Borealis Cluster: distance \u2248 {HUBBLE_CLUSTERS[3][1]:.0f} Mpc, recession velocity \u2248 {HUBBLE_CLUSTERS[3][2]:.0f} km/s.',
            'The cosmic microwave background (a near-perfect 2.7 K blackbody radiation field filling the entire sky, discovered accidentally by Penzias and Wilson in 1965) is the cooled, redshifted afterglow of the hot, dense early universe, predicted by the Big Bang model decades before its detection.',
        ],
        model=[
            "Hubble's law states that a galaxy's recession velocity v is proportional to its distance d: v = H0 d, where H0 (the Hubble constant) sets the current expansion rate of the universe.",
            'Because H0 has units of inverse time, its reciprocal (the Hubble time, 1/H0) gives an order-of-magnitude estimate for the age of the universe, exact only for a universe that has expanded at a perfectly constant rate (which ours has not, given the accelerating expansion of Lecture 13).',
            'Independent observational pillars \u2014 the expansion itself (Hubble\u2019s law), the cosmic microwave background, and the observed primordial abundances of hydrogen, helium, and lithium (Big Bang nucleosynthesis) \u2014 together support the Big Bang model of a universe that began in a hot, dense state roughly 13.8 billion years ago.',
        ],
        equation=r'v = H_0\,d, \qquad t_{\rm Hubble} = \dfrac{1}{H_0}',
        example=[
            f'Fitting v = H0 d to the five-cluster sample (Virgo, Hydra, Ursa Major, Corona Borealis, Bootes) gives a best-fit Hubble constant H0 \u2248 {H0_FIT:.1f} km/s/Mpc.',
            f'This is close to modern precision measurements (roughly 67-73 km/s/Mpc, depending on method \u2014 the ongoing "Hubble tension"), confirming that even a small five-cluster classroom sample recovers the right order of magnitude and rough value.',
            f'Hubble time: 1/H0 = 1 / ({H0_FIT:.1f} km/s/Mpc), converting units (1 Mpc = {MPC_KM:.3e} km) gives t_Hubble \u2248 {HUBBLE_TIME_GYR:.1f} billion years \u2014 remarkably close to the independently measured age of the universe from the cosmic microwave background (about 13.8 billion years), especially given this estimate assumes a constant expansion rate rather than the universe\u2019s actual expansion history.',
        ],
        pitfall='Interpreting galaxies\u2019 recession as galaxies "moving through" space away from us, the way an explosion scatters debris from a central point. Hubble\u2019s law describes the expansion of space itself between galaxies; there is no center of the expansion, and every observer in the universe sees the same pattern of galaxies receding in proportion to distance.',
        activity='Using the five-cluster data, discuss why fitting a straight line through the origin (rather than allowing a nonzero intercept) is the physically motivated choice for testing Hubble\u2019s law, and what a large intercept would imply if it were required.',
        lab_connection='Lab 07 has students fit the Hubble constant from the same five-cluster data set used in this lecture\u2019s worked example, then use it to estimate the age of the universe and compare to the CMB-based value.',
        synthesis='Hubble\u2019s law converts a redshift-distance relationship into an expansion rate and, from that, an approximate age for the universe, closing the course\u2019s arc from individual stars to the observational foundations of modern cosmology.',
        openstax='OpenStax Astronomy 2e, Chapter 29.1-29.3 (the age of the universe, the beginning of the universe, the cosmic microwave background).',
    ),
]


def slide_deck(item: dict) -> str:
    n = item['n']
    fig = FIGURE_BUILDERS[n]()
    body = f"""<main class='deck'>
<section class='slide title'><p class='kicker'>ASTR 230 &middot; Lecture {n:02d}</p><h1>{escape(item['title'])}</h1><h2>{escape(item['subtitle'])}</h2></section>
<section class='slide'><h2>Learning Goals</h2><ol>{li(item['goals'])}</ol><p class='small'>Reading anchor: {escape(item['openstax'])}</p></section>
<section class='slide'><h2>Why This Matters</h2><p>{item['why_matters']}</p></section>
<section class='slide'><h2>Opening Phenomenon</h2><p>{item['phenomenon']}</p><p class='warning'><strong>First question:</strong> what here is directly observed, and what is inferred from a physical model?</p></section>
<section class='slide'><h2>Vocabulary for Reasoning</h2><div class='three'>{cards(item['vocab'])}</div><p class='small'>Use these terms to describe evidence and relationships, not as isolated definitions.</p></section>
<section class='slide'><h2>Evidence We Need to Explain</h2><ul>{li(item['evidence'])}</ul></section>
<section class='slide'><h2>Model</h2><ul>{li(item['model'])}</ul></section>
<section class='slide'><h2>Quantitative Tool</h2><div class='equation'>\\[ {item['equation']} \\]</div></section>
<section class='slide'><h2>Worked Example</h2><ol>{li(item['example'])}</ol></section>
<section class='slide visual-slide'><h2>Visual Reasoning</h2><div class='visual-grid'><div><p>Study this lecture\u2019s figure, built from the same numbers used in the worked example above.</p><ul><li>What quantity is plotted, measured, or compared, and over what range?</li><li>What trend, shape, or contrast in the figure carries the physical argument?</li><li>What would change in the figure if the underlying assumption or data point were different?</li></ul></div><figure class='visual-figure'>{fig}<figcaption>Lecture {n:02d} figure: {escape(item['title'])}.</figcaption></figure></div></section>
<section class='slide'><h2>Common Misconception</h2><p class='warning'>{item['pitfall']}</p></section>
<section class='slide'><h2>Active Learning Segment</h2><p>{item['activity']}</p></section>
<section class='slide'><h2>Lab Connection</h2><p>{item['lab_connection']}</p></section>
<section class='slide'><h2>Synthesis</h2><p>{item['synthesis']}</p></section>
<section class='slide'><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Local reference copy: <code>references/openstax-astronomy-2e-extracted.txt</code>.</li><li>Course dataset used in this lecture\u2019s worked example: <code>materials/ASTR230/data/</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 230 Lecture {n:02d} Slides', body, SLIDE_CSS)


def lecture_notes(item: dict) -> str:
    n = item['n']
    body = f"""<header><div><h1>Lecture {n:02d}: {escape(item['title'])}</h1><p>ASTR 230 Stars, Galaxies, and the Universe</p></div></header>
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
<section><h2>Lab Connection</h2><p>{item['lab_connection']}</p></section>
<section><h2>Synthesis Questions</h2><ul><li>What was measured directly in this lecture\u2019s worked example, and what was inferred from the model?</li><li>Which assumption would most change the interpretation if it were wrong?</li><li>How does this lecture\u2019s technique connect to the lab and problem set that follow it?</li></ul></section>
<section><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Local reference copy: <code>references/openstax-astronomy-2e-extracted.txt</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 230 Lecture {n:02d} Notes', body)


def write_lectures():
    for item in LECTURES:
        n = item['n']
        (LECTURE_DIR / f'lecture-{n:02d}-slides.html').write_text(slide_deck(item), encoding='utf-8')
        (LECTURE_DIR / f'lecture-{n:02d}-notes.html').write_text(lecture_notes(item), encoding='utf-8')


def write_data_csv():
    import csv
    with open(DATA_DIR / 'nearby_bright_stars.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['name', 'V_apparent_mag', 'parallax_mas', 'distance_pc', 'absolute_mag_V',
                    'Teff_K', 'radius_Rsun', 'spectral_type', 'L_from_Mv_Lsun', 'L_from_StefanBoltzmann_Lsun'])
        for s in STAR_TABLE:
            w.writerow([s['name'], s['v_app'], s['parallax_mas'], round(s['d_pc'], 4), round(s['mv'], 3),
                        s['teff'], s['r_rsun'], s['spt'], round(s['l_from_mv'], 5), round(s['l_from_sb'], 5)])
    with open(DATA_DIR / 'milky_way_rotation_curve.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['radius_kpc', 'circular_velocity_kms', 'enclosed_mass_Msun'])
        for r, v in ROTATION_CURVE:
            w.writerow([r, v, round(enclosed_mass_msun(r, v), 3)])
    with open(DATA_DIR / 'hubble_diagram_clusters.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['cluster', 'distance_Mpc', 'recession_velocity_kms'])
        for name, d, v in HUBBLE_CLUSTERS:
            w.writerow([name, d, v])


if __name__ == '__main__':
    write_lectures()
    write_data_csv()
    print(f'Wrote {len(LECTURES)} lecture slide decks and notes files, plus 3 data CSV files.')
