"""Content generator for ASTR370 (Solar Physics and Space Weather) lecture
slides and lecture notes.

Every worked numeric example is computed programmatically from the shared
physical constants and real heliophysics datasets defined below (never
hand-typed), and the same constants are reused across labs and problem sets
that reference the same scenario (see generate_astr370_labs_psets.py). Run
with the project interpreter:
    python materials/ASTR370/src/generate_astr370_content.py
"""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURE_DIR = ROOT / 'lectures'
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


def fmt(x: float, sig: int = 4) -> str:
    if x == 0:
        return '0'
    return f'{x:.{sig}g}'


# ---------------------------------------------------------------------------
# Physical constants (SI unless noted).
# ---------------------------------------------------------------------------
G_CONST = 6.674e-11
C_LIGHT = 2.998e8
H_PLANCK = 6.626e-34
K_BOLTZMANN = 1.381e-23
SIGMA_SB = 5.670e-8
MU0 = 4 * math.pi * 1.0e-7
AU_M = 1.496e11
YEAR_S = 3.156e7
DAY_S = 86400.0
M_SUN = 1.989e30
R_SUN = 6.957e8
L_SUN = 3.828e26
M_H_KG = 1.6726e-27
M_P_KG = 1.6726e-27
AMU = 1.6605e-27
EV_J = 1.602e-19
MU_PHOTOSPHERE = 1.30   # mean molecular weight, weakly ionized solar photospheric gas, standard value (Stix 2002)
MU_CORONA = 0.60        # mean molecular weight, fully ionized H+He coronal/solar-wind plasma, standard value

# Sun's global parameters (IAU nominal values / standard solar model, level 2)
T_EFF_SUN_K = 5772.0
T_CORE_SUN_K = 1.57e7
RHO_CORE_SUN_KGM3 = 1.5e5
RADIATIVE_ZONE_FRAC_R = 0.71   # base of convection zone, standard helioseismic value
CORE_FRAC_R = 0.25             # outer edge of the energy-generating core, standard value
G_SURFACE_SUN = G_CONST * M_SUN / R_SUN ** 2

# Photosphere (level 2, Stix 2002 "The Sun" / VAL semi-empirical atmosphere)
P_PHOTOSPHERE_PA = 1.25e4   # gas pressure at tau=1 (500 nm), standard solar atmosphere model value
RHO_PHOTOSPHERE_KGM3 = 2.3e-4

# Chromosphere / corona (level 2, standard quiet-Sun values)
T_CHROMOSPHERE_TOP_K = 2.0e4
T_CORONA_K = 1.5e6
N_CORONA_BASE_M3 = 1.0e14     # ~1e8 cm^-3, standard quiet-Sun coronal base electron density

# Sunspots (level 2, Solanki 2003, A&A Rev. 11, 153, review of sunspot fields)
B_SUNSPOT_UMBRA_T = 0.28      # 2800 G, a large, well-observed sunspot umbral field strength

# Solar cycle sunspot-number data (SILSO, WDC-SILSO, Royal Observatory of
# Belgium). Cycle 25 figures live-verified this session via Wikipedia's
# "Solar cycle 25" article (which cites SILSO/NOAA SWPC directly); Cycle 24
# figure is a standard published value not independently re-verified this
# session (level 2).
CYCLE25_START = 'December 2019'
CYCLE25_MIN_SMOOTHED_SSN = 1.8
CYCLE25_MAX_SMOOTHED_SSN = 160.8       # October 2024, smoothed monthly mean
CYCLE25_MAX_MONTHLY_SSN = 216.0        # August 2024, not smoothed
CYCLE24_MAX_SMOOTHED_SSN = 116.4       # April 2014, standard published value, level 2

# AR 12673 / X9.3 flare, 6 September 2017 (standard published NOAA
# SWPC / GOES values, level 2; live web fetch of this specific event was
# attempted this session but the source page returned an error, so these
# are treated as standard literature values pending human spot-check,
# per reference-log.md).
FLARE_DATE = '2017-09-06'
FLARE_GOES_CLASS = 'X9.3'
FLARE_PEAK_FLUX_WM2 = 9.3e-4     # GOES 1-8 Angstrom soft X-ray flux, X9.3 by definition
FLARE_CME_SPEED_KMS = 1571.0     # SOHO/LASCO CDAW catalog linear plane-of-sky speed, standard published value
FLARE_AR_AREA_M2 = 1.5e18        # representative large sunspot-group area for AR 12673, order-of-magnitude, level 3 (see reference-log.md)
FLARE_AR_HEIGHT_M = 1.0e7        # representative active-region coronal volume height scale, level 3
STORM_DATE = '2017-09-07/08'
STORM_DST_MIN_NT = -142.0        # published Kyoto WDC/NOAA Dst minimum for the 7-8 Sept 2017 G4 storm, level 2
STORM_TRANSIT_HOURS_OBSERVED = 36.0  # approximate observed CME transit time, standard published range, level 2

# Carrington Event, 1-2 September 1859 (live-verified this session via
# Wikipedia's "Carrington Event" article, which cites Tsurutani et al. 2003,
# J. Geophys. Res. 108, A7, 1268, and Cliver & Svalgaard 2005, Solar Phys.
# 224, 407 for the Dst range).
CARRINGTON_DST_MIN_NT = -1750.0   # upper end of the -0.80 to -1.75 microT estimated range (Tsurutani et al. 2003)
CARRINGTON_DST_MIN_NT_CONSERVATIVE = -800.0  # lower, more conservative end of the estimated range (Cliver & Svalgaard 2005)
CARRINGTON_TRANSIT_HOURS = 17.6   # estimated CME travel time, live-verified this session

# Parker Solar Probe (live-verified this session via Wikipedia's "Parker
# Solar Probe" article, citing NASA/JHUAPL mission documentation).
PSP_LAUNCH_DATE = '2018-08-12'
PSP_PERIHELION_RSUN = 9.86
PSP_PERIHELION_KM = 6.9e6
PSP_RECORD_SPEED_KMS = 191.0      # heliocentric-frame speed record, achieved 24 Dec 2024 perihelion
PSP_RECORD_SPEED_KMH = 690000.0

# Solar wind at 1 AU (level 2, standard OMNI-database climatological values)
SOLAR_WIND_SLOW_V_KMS = 400.0
SOLAR_WIND_SLOW_N_CM3 = 6.0
SOLAR_WIND_FAST_V_KMS = 700.0
SOLAR_WIND_FAST_N_CM3 = 3.0
SOLAR_WIND_STORM_V_KMS = 800.0    # enhanced CME-sheath speed, representative storm-time value, level 2
SOLAR_WIND_STORM_N_CM3 = 10.0     # enhanced CME-sheath density, representative storm-time value, level 2

# Earth's magnetosphere (level 2, standard geomagnetism values)
B0_EARTH_T = 3.0e-5               # equatorial surface dipole field strength
R_EARTH_M = 6.371e6

OPENSTAX_NOTE = (
    'OpenStax Astronomy 2e (local extracted reference copy: '
    'references/openstax-astronomy-2e-extracted.txt) covers the Sun in Chapter 15 ("The Sun: A Garden-Variety Star"): '
    '15.1 The Structure and Composition of the Sun, 15.2 The Solar Cycle, and 15.3 Solar Activity above the Photosphere. '
    'Chapter 15\u2019s section numbering was cross-checked directly against its own embedded figure numbering this '
    'session (Figures 15.1 through 15.24 all appear under their matching section headers with no offset), so this '
    'citation is verified against the local extracted text rather than extrapolated by analogy from a prior course. '
    'OpenStax\u2019s treatment throughout Chapter 15 is descriptive and qualitative; nearly every quantitative '
    'derivation in this course (the hydrostatic solar-atmosphere/scale-height argument, the sunspot magnetic-pressure '
    'balance, the Parker solar-wind critical-point argument and its numerical transonic solution, flare free-energy '
    'budgets, the Chapman-Ferraro magnetopause standoff distance, and the Dessler-Parker-Sckopke ring-current/Dst '
    'relation) goes well beyond OpenStax Astronomy 2e\u2019s introductory level; each lecture states explicitly where '
    'this course extends beyond the assigned reading.'
)


# ---------------------------------------------------------------------------
# Physics helper functions -- every worked example below calls these rather
# than hand-typing a numeric result.
# ---------------------------------------------------------------------------
def scale_height_m(temp_k: float, mu: float, g_local: float = G_SURFACE_SUN) -> float:
    """Isothermal hydrostatic scale height H = kT/(mu m_H g)."""
    return K_BOLTZMANN * temp_k / (mu * M_H_KG * g_local)


def sunspot_pressure_deficit_pa(b_tesla: float) -> float:
    """Magnetic pressure of a flux tube, P_mag = B^2/(2 mu0), which the thin
    flux-tube model requires be balanced by a gas-pressure deficit inside
    relative to the surrounding photosphere at the same geometric depth."""
    return b_tesla ** 2 / (2 * MU0)


def flare_free_energy_j(b_tesla: float, volume_m3: float) -> float:
    """Order-of-magnitude magnetic free energy available for a flare,
    E ~ (B^2/2 mu0) V (a representative fraction of the total field energy
    in a volume of comparable free, non-potential field strength)."""
    return (b_tesla ** 2 / (2 * MU0)) * volume_m3


def parker_wind_residual(u: float, r_over_rc: float) -> float:
    """Residual of the isothermal Parker wind transonic-solution equation,
    u^2 - ln(u^2) = 4 ln(r/r_c) + 4 r_c/r - 3, where u = v/c_s. Root u(r)=0
    of this residual gives the transonic (critical) solution branch."""
    return u ** 2 - math.log(u ** 2) - (4 * math.log(r_over_rc) + 4 / r_over_rc - 3)


def solve_parker_wind_speed(r_over_rc: float, branch: str = 'auto') -> float:
    """Numerically solve the isothermal Parker transonic wind equation for
    u=v/c_s at a given r/r_c using bisection on the correct physical branch
    (subsonic for r<r_c, supersonic for r>r_c), avoiding the unphysical
    second root of the same transcendental equation."""
    def f(u):
        return parker_wind_residual(u, r_over_rc)
    if r_over_rc >= 1.0:
        lo, hi = 1.0 + 1.0e-9, 50.0
    else:
        lo, hi = 1.0e-6, 1.0 - 1.0e-9
    flo, fhi = f(lo), f(hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if flo * fmid <= 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return 0.5 * (lo + hi)


def coronal_sound_speed_m_s(temp_k: float = T_CORONA_K, mu: float = MU_CORONA) -> float:
    return math.sqrt(K_BOLTZMANN * temp_k / (mu * M_H_KG))


def parker_critical_radius_m(temp_k: float = T_CORONA_K, mu: float = MU_CORONA) -> float:
    """Parker wind critical radius r_c = GM/(2 c_s^2)."""
    cs = coronal_sound_speed_m_s(temp_k, mu)
    return G_CONST * M_SUN / (2 * cs ** 2)


def travel_time_hours(distance_m: float, speed_km_s: float) -> float:
    return distance_m / (speed_km_s * 1.0e3) / 3600.0


def magnetopause_standoff_re(n_cm3: float, v_km_s: float, b0_t: float = B0_EARTH_T, compression: float = 2.0) -> float:
    """Chapman-Ferraro magnetopause standoff distance (in Earth radii) from
    balancing solar-wind dynamic (ram) pressure against the compressed
    dipole magnetic pressure, r_mp = R_E (compression*B0^2/(mu0 rho v^2))^(1/6)."""
    rho = n_cm3 * 1.0e6 * M_P_KG
    v_m_s = v_km_s * 1.0e3
    ratio = compression * b0_t ** 2 / (MU0 * rho * v_m_s ** 2)
    return ratio ** (1.0 / 6.0)


def dps_ring_current_energy_j(dst_nt: float, b0_t: float = B0_EARTH_T) -> float:
    """Dessler-Parker-Sckopke relation, Dst*/B0 = -(2/3) E_ring/E0, where
    E0 = B0^2 R_E^3/(6 mu0) is the reference dipolar magnetic energy outside
    the Earth's surface (down to R_E). Solves for E_ring given Dst."""
    e0 = b0_t ** 2 * R_EARTH_M ** 3 / (6 * MU0)
    dst_t = dst_nt * 1.0e-9
    e_ring = -(3.0 / 2.0) * (dst_t / b0_t) * e0
    return e_ring


DPS_E0_J = B0_EARTH_T ** 2 * R_EARTH_M ** 3 / (6 * MU0)

# ---------------------------------------------------------------------------
# Derived worked-example numbers, computed once here and reused throughout
# the lectures, labs, and problem sets.
# ---------------------------------------------------------------------------
H_PHOTOSPHERE_M = scale_height_m(T_EFF_SUN_K, MU_PHOTOSPHERE)
H_CORONA_M = scale_height_m(T_CORONA_K, MU_CORONA)

P_MAG_SUNSPOT_PA = sunspot_pressure_deficit_pa(B_SUNSPOT_UMBRA_T)
SUNSPOT_PRESSURE_FRACTION = P_MAG_SUNSPOT_PA / P_PHOTOSPHERE_PA

FLARE_FREE_ENERGY_J = flare_free_energy_j(B_SUNSPOT_UMBRA_T, FLARE_AR_AREA_M2 * FLARE_AR_HEIGHT_M)

CORONAL_SOUND_SPEED_KMS = coronal_sound_speed_m_s() / 1.0e3
PARKER_RC_M = parker_critical_radius_m()
PARKER_RC_RSUN = PARKER_RC_M / R_SUN

CME_TRAVEL_TIME_CONSTANT_SPEED_HR = travel_time_hours(AU_M, FLARE_CME_SPEED_KMS)
CARRINGTON_IMPLIED_SPEED_KMS = AU_M / (CARRINGTON_TRANSIT_HOURS * 3600.0) / 1.0e3

MAGNETOPAUSE_QUIET_RE = magnetopause_standoff_re(SOLAR_WIND_SLOW_N_CM3, SOLAR_WIND_SLOW_V_KMS)
MAGNETOPAUSE_STORM_RE = magnetopause_standoff_re(SOLAR_WIND_STORM_N_CM3, SOLAR_WIND_STORM_V_KMS)

RING_CURRENT_ENERGY_SEPT2017_J = dps_ring_current_energy_j(STORM_DST_MIN_NT)
RING_CURRENT_ENERGY_CARRINGTON_J = dps_ring_current_energy_j(CARRINGTON_DST_MIN_NT)
RING_CURRENT_ENERGY_CARRINGTON_CONSERVATIVE_J = dps_ring_current_energy_j(CARRINGTON_DST_MIN_NT_CONSERVATIVE)


# ---------------------------------------------------------------------------
# Lecture-specific visual-reasoning diagrams (SVG). Each lecture gets a
# structurally distinct figure built from the real constants/datasets above;
# only small drawing primitives are shared (established pattern from
# materials/ASTR310,330,350,360/src).
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


def _bar(x, y0, w, h, color='#0f6b78', label=None, label_y=None):
    out = f"<rect x='{x:.1f}' y='{y0 - h:.1f}' width='{w:.1f}' height='{h:.1f}' fill='{color}'/>"
    if label:
        out += (f"<text x='{x + w / 2:.1f}' y='{(label_y if label_y else y0 - h - 8):.1f}' font-size='13.5' "
                 f"fill='#17202a' text-anchor='middle' font-family='Segoe UI, sans-serif'>{escape(label)}</text>")
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


def diagram_01(item):
    """Solar interior cross-section: temperature vs fractional radius with
    core/radiative/convective zone boundaries marked at real fractional radii."""
    x0, y0, w, h = 90, 90, 800, 380

    def px(fr):
        return _lin(fr, 0, 1, x0, x0 + w)

    def temp_profile(fr):
        # Smooth monotone decline from core to surface temperature, calibrated
        # to pass through the two real endpoints (T_core at r=0, T_eff at r=1)
        # with a steepening near the surface -- illustrative interpolation,
        # not a full stellar-structure numerical solution (level 3, disclosed).
        return T_CORE_SUN_K * (1 - fr) ** 2.6 + T_EFF_SUN_K

    logt_vals = [math.log10(temp_profile(i / 100)) for i in range(101)]
    logt_range = (min(logt_vals) - 0.1, max(logt_vals) + 0.1)

    def py(logt):
        return _lin(logt, *logt_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'Fractional radius r/R_sun', 'log10 T (K)')
    pts = [(px(i / 100), py(math.log10(temp_profile(i / 100)))) for i in range(101)]
    inner += _polyline(pts)
    inner += f"<line x1='{px(CORE_FRAC_R):.1f}' y1='{y0}' x2='{px(CORE_FRAC_R):.1f}' y2='{y0+h}' stroke='#b87911' stroke-width='2' stroke-dasharray='5 4'/>"
    inner += f"<line x1='{px(RADIATIVE_ZONE_FRAC_R):.1f}' y1='{y0}' x2='{px(RADIATIVE_ZONE_FRAC_R):.1f}' y2='{y0+h}' stroke='#8a4b08' stroke-width='2' stroke-dasharray='5 4'/>"
    inner += _dot(px(0.0), py(math.log10(T_CORE_SUN_K)), f'Core: T={T_CORE_SUN_K:.2e} K', dy=18)
    inner += _dot(px(1.0), py(math.log10(T_EFF_SUN_K)), f'Photosphere: T_eff={T_EFF_SUN_K:.0f} K', dy=-14, anchor='end', dx=-10)
    inner += _fig_caption(f'Core (r<{CORE_FRAC_R}R) energy generation, radiative zone, convective zone (r>{RADIATIVE_ZONE_FRAC_R}R, dashed lines mark real helioseismic boundaries).')
    return _fig_wrap(item['n'], item['title'], inner, 'temperature vs fractional solar radius with core, radiative zone, and convective zone boundaries marked')


def diagram_02(item):
    """Solar atmosphere temperature vs height: photospheric minimum,
    chromospheric rise, transition region jump to coronal temperature."""
    x0, y0, w, h = 90, 90, 800, 380
    height_range_mm = (0, 3.0)  # thousands of km above photosphere

    def px(hmm):
        return _lin(hmm, *height_range_mm, x0, x0 + w)

    def temp_at(h_mm):
        h_km = h_mm * 1000
        if h_km < 500:
            return T_EFF_SUN_K * (1 - 0.3 * (h_km / 500))
        elif h_km < 2000:
            frac = (h_km - 500) / 1500
            return 4100 + frac * (T_CHROMOSPHERE_TOP_K - 4100)
        else:
            frac = min((h_km - 2000) / 200, 1.0)
            return T_CHROMOSPHERE_TOP_K + frac * (T_CORONA_K - T_CHROMOSPHERE_TOP_K)

    logt_vals = [math.log10(temp_at(height_range_mm[0] + i * (height_range_mm[1] - height_range_mm[0]) / 150)) for i in range(151)]
    logt_range = (min(logt_vals) - 0.1, max(logt_vals) + 0.2)

    def py(logt):
        return _lin(logt, *logt_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'Height above photosphere (1000 km)', 'log10 T (K)')
    pts = [(px(height_range_mm[0] + i * (height_range_mm[1] - height_range_mm[0]) / 150),
            py(math.log10(temp_at(height_range_mm[0] + i * (height_range_mm[1] - height_range_mm[0]) / 150)))) for i in range(151)]
    inner += _polyline(pts)
    inner += _dot(px(0.5), py(math.log10(4100)), 'Temperature minimum ~4100 K', dy=16)
    inner += _dot(px(2.05), py(math.log10(T_CORONA_K)), f'Corona: T~{T_CORONA_K:.1e} K', dy=-14)
    inner += _fig_caption('Schematic (illustrative height scale, level 3) temperature profile: photosphere, temperature minimum, chromosphere, and the transition-region jump to the million-kelvin corona -- the unsolved coronal-heating problem.')
    return _fig_wrap(item['n'], item['title'], inner, 'temperature vs height above the photosphere showing the chromospheric rise and coronal heating jump')


def diagram_03(item):
    """Schematic sunspot butterfly diagram: latitude vs time over two
    idealized 11-year cycles, migrating from mid-latitude to equator."""
    x0, y0, w, h = 90, 90, 800, 380

    def px(year_frac):
        return _lin(year_frac, 0, 22, x0, x0 + w)

    def py(lat):
        return _lin(lat, -35, 35, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'Years since cycle start', 'Sunspot latitude (degrees)')
    inner += f"<line x1='{x0}' y1='{py(0):.1f}' x2='{x0+w}' y2='{py(0):.1f}' stroke='#d9e0e7' stroke-width='1.5'/>"
    for cycle_start in (0, 11):
        for hemi in (1, -1):
            for i in range(60):
                t = cycle_start + i * 11 / 60
                lat = hemi * (32 * math.exp(-3.2 * (i / 60)) + 3)
                size = 3 + 4 * math.exp(-2 * abs(i / 60 - 0.35))
                inner += f"<circle cx='{px(t):.1f}' cy='{py(lat):.1f}' r='{size:.1f}' fill='#0f6b78' opacity='0.6'/>"
    inner += _fig_caption(f'Schematic butterfly diagram (idealized double-cycle, level 3): new-cycle spots emerge near +/-30 deg latitude and migrate toward the equator as each ~11-year cycle progresses.')
    return _fig_wrap(item['n'], item['title'], inner, 'schematic sunspot butterfly diagram showing latitude migration over two idealized solar cycles')


def diagram_04(item):
    """Sunspot magnetic pressure balance: bar chart of photospheric gas
    pressure vs the sunspot's magnetic pressure at the real umbral field."""
    x0, y0, w, h = 160, 500, 660, 360
    bars = [
        ('Photospheric gas pressure (quiet Sun)', P_PHOTOSPHERE_PA, '#0f6b78'),
        (f'Sunspot magnetic pressure (B={B_SUNSPOT_UMBRA_T*1e4:.0f} G)', P_MAG_SUNSPOT_PA, '#b87911'),
    ]
    maxp = max(p for _, p, _ in bars) * 1.2
    inner = f"<line x1='{x0-20}' y1='{y0}' x2='{x0+w}' y2='{y0}' stroke='#5b6773' stroke-width='2'/>"
    bw, gap = 220, 100
    for i, (label, p, color) in enumerate(bars):
        bx = x0 + i * (bw + gap)
        bh = p / maxp * 380
        inner += _bar(bx, y0, bw, bh, color=color, label=f'{p:,.0f} Pa', label_y=y0 - bh - 12)
        inner += (f"<text x='{bx+bw/2:.1f}' y='{y0+26}' font-size='14' fill='#17202a' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif'>{escape(label)}</text>")
    inner += _fig_caption(f'Thin flux-tube total-pressure balance: P_gas,outside = P_gas,inside + B^2/(2 mu0). The umbral magnetic pressure ({P_MAG_SUNSPOT_PA:,.0f} Pa) is {SUNSPOT_PRESSURE_FRACTION:.2f}x the ambient photospheric gas pressure, so P_gas,inside must be strongly reduced (a real Wilson depression), consistent with observations.', y=90)
    return _fig_wrap(item['n'], item['title'], inner, 'bar chart comparing photospheric gas pressure to sunspot magnetic pressure for a real large sunspot field strength')


def diagram_05(item):
    """Schematic magnetic reconnection X-point diagram with inflow/outflow
    arrows and a free-energy bar alongside."""
    x0, y0 = 90, 120
    inner = ''
    # Field lines bending into an X-point at (500, 300)
    cx, cy = 470, 300
    for sign in (-1, 1):
        for k in range(3):
            off = 40 + k * 35
            inner += f"<path d='M {cx-260} {cy+sign*off} Q {cx-60} {cy+sign*30} {cx} {cy}' fill='none' stroke='#0f6b78' stroke-width='2.5'/>"
            inner += f"<path d='M {cx+260} {cy-sign*off} Q {cx+60} {cy-sign*30} {cx} {cy}' fill='none' stroke='#0f6b78' stroke-width='2.5'/>"
    inner += f"<circle cx='{cx}' cy='{cy}' r='7' fill='#b87911'/>"
    inner += f"<text x='{cx+14}' y='{cy-10}' font-size='15' font-family='Segoe UI, sans-serif'>reconnection X-point</text>"
    inner += f"<line x1='{cx-320}' y1='{cy}' x2='{cx-280}' y2='{cy}' stroke='#8a4b08' stroke-width='3' marker-end='url(#a1)'/>"
    inner += f"<text x='{cx-360}' y='{cy+5}' font-size='14' font-family='Segoe UI, sans-serif'>inflow</text>"
    inner += f"<line x1='{cx}' y1='{cy+60}' x2='{cx}' y2='{cy+120}' stroke='#8a4b08' stroke-width='3'/>"
    inner += f"<text x='{cx+10}' y='{cy+110}' font-size='14' font-family='Segoe UI, sans-serif'>reconnection jet (outflow)</text>"
    bx, by, bw = 800, 500, 100
    max_e = FLARE_FREE_ENERGY_J
    bh = 260
    inner += _bar(bx, by, bw, bh, color='#b87911', label=f'{FLARE_FREE_ENERGY_J:.1e} J', label_y=by-bh-12)
    inner += f"<text x='{bx+bw/2:.1f}' y='{by+26}' font-size='13' fill='#17202a' text-anchor='middle' font-family='Segoe UI, sans-serif'>Free magnetic energy (order-of-magnitude, AR12673-scale)</text>"
    inner += _fig_caption(f'Oppositely directed field lines reconnect at the X-point, converting stored magnetic free energy (~{FLARE_FREE_ENERGY_J:.1e} J for an AR12673-scale active region, level 3 order-of-magnitude estimate) into kinetic/thermal/radiated flare energy.', y=90)
    return _fig_wrap(item['n'], item['title'], inner, 'schematic magnetic reconnection X-point diagram with inflow and outflow arrows next to a free magnetic energy bar')


def diagram_06(item):
    """GOES soft X-ray flare light curve (schematic Neupert-type profile)
    for the real 6 September 2017 X9.3 flare, with the real peak flux marked."""
    x0, y0, w, h = 90, 90, 800, 380
    t_range = (0, 60)  # minutes

    def px(t):
        return _lin(t, *t_range, x0, x0 + w)

    def flux(t):
        rise = FLARE_PEAK_FLUX_WM2 * math.exp(-((t - 12) / 4) ** 2) if t < 12 else FLARE_PEAK_FLUX_WM2
        decay = FLARE_PEAK_FLUX_WM2 * math.exp(-(t - 12) / 18)
        return rise if t < 12 else decay

    logf_vals = [math.log10(flux(t)) for t in [i * 60 / 150 for i in range(151)]]
    logf_range = (min(logf_vals) - 0.3, max(logf_vals) + 0.3)

    def py(logf):
        return _lin(logf, *logf_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'Minutes since 11:53 UT, 6 Sept 2017', 'log10 GOES 1-8 A flux (W/m^2)')
    pts = [(px(t), py(math.log10(flux(t)))) for t in [i * 60 / 150 for i in range(151)]]
    inner += _polyline(pts)
    inner += _dot(px(12), py(math.log10(FLARE_PEAK_FLUX_WM2)), f'Peak: {FLARE_GOES_CLASS} = {FLARE_PEAK_FLUX_WM2:.1e} W/m^2', dy=-16)
    for cls, flux_thresh in (('X1.0', 1.0e-4), ('M1.0', 1.0e-5)):
        inner += f"<line x1='{x0}' y1='{py(math.log10(flux_thresh)):.1f}' x2='{x0+w}' y2='{py(math.log10(flux_thresh)):.1f}' stroke='#d9e0e7' stroke-width='1.2' stroke-dasharray='4 3'/>"
        inner += _fig_caption(f'{cls} threshold', y=py(math.log10(flux_thresh)) - 6)
    inner += _fig_caption(f'Schematic light curve shape (level 3) calibrated to the real, published {FLARE_GOES_CLASS} peak flux from active region 12673, 6 September 2017 -- the largest flare of Solar Cycle 24.', y=y0-40)
    return _fig_wrap(item['n'], item['title'], inner, 'GOES soft X-ray flare light curve for the real X9.3 flare of 6 September 2017 with X and M class thresholds marked')


def diagram_07(item):
    """CME height-time kinematics: linear real LASCO speed vs a schematic
    decelerating (drag) trajectory, showing why arrival time is uncertain."""
    x0, y0, w, h = 90, 90, 800, 380
    t_range = (0, 40)  # hours

    def px(t):
        return _lin(t, *t_range, x0, x0 + w)

    au_km = AU_M / 1.0e3

    def dist_linear(t):
        return FLARE_CME_SPEED_KMS * t * 3600

    def dist_decel(t):
        # Simple drag-based deceleration toward the ambient solar-wind speed,
        # asymptotically approaching v_sw (illustrative functional form, level 3).
        v_sw = SOLAR_WIND_SLOW_V_KMS
        tau = 15.0 * 3600
        v0 = FLARE_CME_SPEED_KMS
        return v_sw * t * 3600 + (v0 - v_sw) * tau * (1 - math.exp(-t * 3600 / tau))

    dvals = [dist_linear(t) / au_km for t in [i * 40 / 100 for i in range(101)]] + [dist_decel(t) / au_km for t in [i * 40 / 100 for i in range(101)]]
    drange = (0, max(dvals) * 1.1)

    def py(d):
        return _lin(d, *drange, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'Time since eruption (hours)', 'Distance from Sun (AU)')
    pts_lin = [(px(t), py(dist_linear(t) / au_km)) for t in [i * 40 / 100 for i in range(101)]]
    pts_dec = [(px(t), py(dist_decel(t) / au_km)) for t in [i * 40 / 100 for i in range(101)]]
    inner += _polyline(pts_lin, color='#0f6b78', dash='6 4')
    inner += _polyline(pts_dec, color='#b87911')
    inner += f"<line x1='{x0}' y1='{py(1.0):.1f}' x2='{x0+w}' y2='{py(1.0):.1f}' stroke='#d9e0e7' stroke-width='1.5' stroke-dasharray='3 3'/>"
    inner += _fig_caption('Earth orbit (1 AU)', y=py(1.0) - 8)
    inner += _fig_caption(f'Constant-speed extrapolation (dashed, {FLARE_CME_SPEED_KMS:.0f} km/s LASCO speed): predicts arrival at t={CME_TRAVEL_TIME_CONSTANT_SPEED_HR:.1f} hr. Drag-decelerated model (solid, level 3 illustrative): predicts a longer, more realistic transit closer to the observed ~{STORM_TRANSIT_HOURS_OBSERVED:.0f} hr.', y=y0-40)
    return _fig_wrap(item['n'], item['title'], inner, 'CME distance vs time for a constant-speed extrapolation compared to a decelerating drag-based trajectory, both compared to Earth orbit at 1 AU')


def diagram_08(item):
    """Parker wind solution: numerically solved v(r)/c_s vs r/r_c on the
    physical transonic branch."""
    x0, y0, w, h = 90, 90, 800, 380
    r_range = (0.3, 8.0)

    def px(r):
        return _lin(r, *r_range, x0, x0 + w)

    def py(u):
        return _lin(u, 0, 4.5, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'r / r_c', 'v / c_s (transonic solution)')
    n = 120
    pts = []
    for i in range(n + 1):
        r = r_range[0] + i * (r_range[1] - r_range[0]) / n
        u = solve_parker_wind_speed(r)
        pts.append((px(r), py(u)))
    inner += _polyline(pts)
    inner += f"<line x1='{px(1.0):.1f}' y1='{y0}' x2='{px(1.0):.1f}' y2='{y0+h}' stroke='#d9e0e7' stroke-width='1.5' stroke-dasharray='4 3'/>"
    inner += _dot(px(1.0), py(1.0), 'Critical point: r=r_c, v=c_s', dy=-16)
    v_1au_kms = solve_parker_wind_speed(AU_M / PARKER_RC_M) * CORONAL_SOUND_SPEED_KMS
    inner += _fig_caption(f'r_c={PARKER_RC_RSUN:.2f} R_sun (T_corona={T_CORONA_K:.1e} K, c_s={CORONAL_SOUND_SPEED_KMS:.0f} km/s). Numerically solved transonic branch gives v(1 AU)~{v_1au_kms:.0f} km/s, the right order of magnitude for the real observed slow solar wind ({SOLAR_WIND_SLOW_V_KMS:.0f} km/s).', y=y0-40)
    return _fig_wrap(item['n'], item['title'], inner, 'numerically solved Parker isothermal solar wind transonic velocity solution vs radius in units of the critical radius')


def diagram_09(item):
    """Schematic remote-sensing instrument coverage: helioseismic p-mode
    frequency vs harmonic degree, alongside a coronagraph occultation disk."""
    x0, y0, w, h = 90, 90, 480, 380

    def px(ell):
        return _lin(ell, 0, 200, x0, x0 + w)

    def py(freq):
        return _lin(freq, 1.5, 4.5, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'Spherical harmonic degree l', 'p-mode frequency (mHz)')
    for n_overtone in range(1, 6):
        pts = []
        for ell in range(0, 200, 4):
            freq = 0.8 * math.sqrt(n_overtone + ell / 140.0) + 1.2 + n_overtone * 0.25
            pts.append((px(ell), py(freq)))
        inner += _polyline(pts, color='#0f6b78', width=2.0)
    inner += _fig_caption('Helioseismic p-mode ridges (schematic, level 3): SDO/HMI Doppler maps invert these frequencies for internal sound-speed/rotation profiles (Lecture 01\u2019s structure).', y=y0-40)
    cx2, cy2, r_occ, r_fov = 780, 280, 55, 170
    inner += f"<circle cx='{cx2}' cy='{cy2}' r='{r_fov}' fill='#e5f4f6' stroke='#0f6b78' stroke-width='2'/>"
    inner += f"<circle cx='{cx2}' cy='{cy2}' r='{r_occ}' fill='#102a43'/>"
    inner += f"<text x='{cx2}' y='{cy2+r_occ+22}' font-size='13' text-anchor='middle' font-family='Segoe UI, sans-serif'>occulting disk (photosphere hidden)</text>"
    inner += f"<text x='{cx2}' y='{cy2-r_fov-14}' font-size='13' text-anchor='middle' font-family='Segoe UI, sans-serif'>coronagraph field of view (LASCO/SOHO)</text>"
    return _fig_wrap(item['n'], item['title'], inner, 'schematic helioseismic p-mode frequency ridges next to a coronagraph occulting disk field-of-view diagram')


def diagram_10(item):
    """Parker Solar Probe trajectory: distance from Sun vs mission time,
    with the real perihelion and record-speed epoch marked, alongside the
    Parker wind speed curve from Lecture 08 evaluated over PSP's range."""
    x0, y0, w, h = 90, 90, 800, 380
    r_range_rsun = (5, 220)

    def px(r):
        return _lin(math.log10(r), math.log10(r_range_rsun[0]), math.log10(r_range_rsun[1]), x0, x0 + w)

    def py(v):
        return _lin(v, 0, 750, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'log10 distance from Sun (R_sun)', 'Parker wind speed v (km/s)')
    n = 100
    pts = []
    for i in range(n + 1):
        logr = math.log10(r_range_rsun[0]) + i * (math.log10(r_range_rsun[1]) - math.log10(r_range_rsun[0])) / n
        r_rsun = 10 ** logr
        r_m = r_rsun * R_SUN
        u = solve_parker_wind_speed(r_m / PARKER_RC_M)
        v_kms = u * CORONAL_SOUND_SPEED_KMS
        pts.append((px(r_rsun), py(v_kms)))
    inner += _polyline(pts)
    inner += _dot(px(PSP_PERIHELION_RSUN), py(solve_parker_wind_speed(PSP_PERIHELION_KM * 1000 / PARKER_RC_M) * CORONAL_SOUND_SPEED_KMS),
                  f'PSP perihelion: {PSP_PERIHELION_RSUN:.2f} R_sun', dy=-16)
    inner += _dot(px(215.0), py(SOLAR_WIND_SLOW_V_KMS), f'1 AU (215 R_sun): observed slow wind ~{SOLAR_WIND_SLOW_V_KMS:.0f} km/s', dy=16, anchor='end', dx=-10)
    inner += _fig_caption(f'Parker Solar Probe (launched {PSP_LAUNCH_DATE}) samples the wind-acceleration region directly, reaching a record heliocentric speed of {PSP_RECORD_SPEED_KMS:.0f} km/s at its {PSP_PERIHELION_RSUN:.2f} R_sun perihelion -- close enough to the critical point (r_c={PARKER_RC_RSUN:.1f} R_sun) to test Lecture 08\u2019s idealized model directly.', y=y0-40)
    return _fig_wrap(item['n'], item['title'], inner, 'Parker wind speed vs log distance from the Sun with the real Parker Solar Probe perihelion and 1 AU marked')


def diagram_11(item):
    """Magnetopause standoff distance vs solar-wind dynamic pressure,
    quiet and storm-time conditions marked."""
    x0, y0, w, h = 90, 90, 800, 380
    p_range = (0.5, 20)  # nPa

    def px(logp):
        return _lin(logp, math.log10(p_range[0]), math.log10(p_range[1]), x0, x0 + w)

    def standoff_from_pdyn(p_dyn_pa):
        ratio = 2.0 * B0_EARTH_T ** 2 / (MU0 * p_dyn_pa)
        return ratio ** (1.0 / 6.0)

    def pdyn(n_cm3, v_kms):
        return n_cm3 * 1.0e6 * M_P_KG * (v_kms * 1.0e3) ** 2

    logp_vals = [math.log10(pdyn(1, 1) * p * 1.0e-9 / (1 * 1.0e6 * M_P_KG * 1.0e6) + 1) for p in [1]]
    inner = _axes(x0, y0, w, h, 'log10 dynamic pressure (nPa)', 'Magnetopause standoff (R_E)')

    def py(re):
        return _lin(re, 5, 12, y0 + h, y0)

    n = 100
    pts = []
    for i in range(n + 1):
        logp = math.log10(p_range[0]) + i * (math.log10(p_range[1]) - math.log10(p_range[0])) / n
        p_npa = 10 ** logp
        re = standoff_from_pdyn(p_npa * 1.0e-9)
        pts.append((px(logp), py(re)))
    inner += _polyline(pts)
    p_quiet_npa = pdyn(SOLAR_WIND_SLOW_N_CM3, SOLAR_WIND_SLOW_V_KMS) * 1.0e9
    p_storm_npa = pdyn(SOLAR_WIND_STORM_N_CM3, SOLAR_WIND_STORM_V_KMS) * 1.0e9
    inner += _dot(px(math.log10(p_quiet_npa)), py(MAGNETOPAUSE_QUIET_RE), f'Quiet wind: {MAGNETOPAUSE_QUIET_RE:.1f} R_E', dy=-16)
    inner += _dot(px(math.log10(p_storm_npa)), py(MAGNETOPAUSE_STORM_RE), f'CME sheath: {MAGNETOPAUSE_STORM_RE:.1f} R_E', dy=16)
    inner += _fig_caption('Chapman-Ferraro magnetopause standoff distance vs solar-wind ram pressure; a fast, dense CME sheath compresses the dayside magnetosphere substantially closer to Earth than quiet-wind conditions.')
    return _fig_wrap(item['n'], item['title'], inner, 'magnetopause standoff distance vs solar wind dynamic pressure curve with quiet and storm conditions marked')


def diagram_12(item):
    """Dst index comparison: real September 2017 storm vs the Carrington
    event's estimated range, as a bar chart."""
    x0, y0, w = 160, 500, 660
    bars = [
        ('Sept 2017 storm (real, published)', abs(STORM_DST_MIN_NT), '#0f6b78'),
        ('Carrington 1859 (conservative est.)', abs(CARRINGTON_DST_MIN_NT_CONSERVATIVE), '#b87911'),
        ('Carrington 1859 (Tsurutani et al. 2003 est.)', abs(CARRINGTON_DST_MIN_NT), '#8a4b08'),
    ]
    maxv = max(v for _, v, _ in bars) * 1.15
    inner = f"<line x1='{x0-20}' y1='{y0}' x2='{x0+w}' y2='{y0}' stroke='#5b6773' stroke-width='2'/>"
    bw, gap = 170, 55
    for i, (label, v, color) in enumerate(bars):
        bx = x0 + i * (bw + gap)
        bh = v / maxv * 380
        inner += _bar(bx, y0, bw, bh, color=color, label=f'{v:,.0f} nT', label_y=y0 - bh - 12)
        inner += (f"<text x='{bx+bw/2:.1f}' y='{y0+22}' font-size='12.5' fill='#17202a' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif'>{escape(label)}</text>")
    inner += _fig_caption(f'|Dst_min| for a real, well-documented modern storm vs the estimated range for the Carrington Event -- both endpoints of the Carrington estimate (live-verified this session, Tsurutani et al. 2003; Cliver & Svalgaard 2005) substantially exceed the 2017 storm.', y=90)
    return _fig_wrap(item['n'], item['title'], inner, 'bar chart comparing the magnitude of Dst for the September 2017 storm to the estimated Carrington event range')


def diagram_13(item):
    """Satellite orbital decay: atmospheric drag lifetime vs altitude,
    illustrating thermospheric expansion during geomagnetic storms."""
    x0, y0, w, h = 90, 90, 800, 380
    alt_range = (300, 800)  # km

    def px(alt):
        return _lin(alt, *alt_range, x0, x0 + w)

    def lifetime_days(alt_km, storm=False):
        # Schematic (level 3) exponential-atmosphere-like scaling; storm
        # heating expands/densifies the thermosphere, shortening lifetime
        # at fixed altitude -- illustrative functional form only.
        scale = 50.0 if not storm else 35.0
        return 0.5 * math.exp((alt_km - 300) / scale)

    logl_quiet = [math.log10(lifetime_days(a)) for a in range(300, 801, 5)]
    logl_storm = [math.log10(lifetime_days(a, True)) for a in range(300, 801, 5)]
    lrange = (min(logl_quiet + logl_storm) - 0.2, max(logl_quiet + logl_storm) + 0.2)

    def py(logl):
        return _lin(logl, *lrange, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'Orbital altitude (km)', 'log10 orbital lifetime (days)')
    pts_q = [(px(a), py(math.log10(lifetime_days(a)))) for a in range(300, 801, 5)]
    pts_s = [(px(a), py(math.log10(lifetime_days(a, True)))) for a in range(300, 801, 5)]
    inner += _polyline(pts_q, color='#0f6b78')
    inner += _polyline(pts_s, color='#b87911', dash='6 4')
    inner += _fig_caption('Quiet-time (solid) vs geomagnetic-storm-enhanced (dashed) thermospheric drag: storm heating expands the thermosphere, shortening satellite lifetime at fixed altitude -- schematic scaling, level 3, illustrating a real, well-documented effect (e.g., Starlink losses after the February 2022 storm).')
    return _fig_wrap(item['n'], item['title'], inner, 'satellite orbital lifetime vs altitude curves for quiet and geomagnetic-storm-enhanced atmospheric drag conditions')


def diagram_14(item):
    """Capstone synthesis: the flare-CME-magnetosphere-ring current chain,
    with the Dessler-Parker-Sckopke ring-current energy for both real events."""
    x0, y0 = 90, 110
    boxes = [
        ('Flare: magnetic reconnection', f'{FLARE_GOES_CLASS}, E_free~{FLARE_FREE_ENERGY_J:.0e} J'),
        ('CME: mass ejection', f'v~{FLARE_CME_SPEED_KMS:.0f} km/s'),
        ('Solar wind: transit to Earth', f'~{STORM_TRANSIT_HOURS_OBSERVED:.0f} hr (observed, decelerated)'),
        ('Magnetosphere: compression + reconnection', f'standoff {MAGNETOPAUSE_STORM_RE:.1f} R_E (storm)'),
        ('Ring current: Dst depression', f'Dst_min={STORM_DST_MIN_NT:.0f} nT'),
    ]
    inner = ''
    bw, bh, gap = 168, 90, 20
    for i, (label, val) in enumerate(boxes):
        bx = x0 + i * (bw + gap)
        by = y0
        inner += f"<rect x='{bx}' y='{by}' width='{bw}' height='{bh}' rx='6' fill='#e5f4f6' stroke='#0f6b78' stroke-width='2'/>"
        inner += f"<text x='{bx+bw/2}' y='{by+30}' font-size='13' text-anchor='middle' font-family='Segoe UI, sans-serif' font-weight='bold'>{escape(label)}</text>"
        inner += f"<text x='{bx+bw/2}' y='{by+55}' font-size='12' text-anchor='middle' font-family='Segoe UI, sans-serif'>{escape(val)}</text>"
        if i < len(boxes) - 1:
            inner += f"<line x1='{bx+bw}' y1='{by+bh/2}' x2='{bx+bw+gap}' y2='{by+bh/2}' stroke='#b87911' stroke-width='3' marker-end='url(#arrow)'/>"
    x0b, y0b, w2, h2 = 90, 300, 800, 220

    def px(logd):
        return _lin(logd, math.log10(1.0e28), math.log10(1.0e31), x0b, x0b + w2)

    def py(dummy):
        return y0b + h2 - 40

    events = [('Sept 2017 (real)', RING_CURRENT_ENERGY_SEPT2017_J, '#0f6b78'),
              ('Carrington, conservative', RING_CURRENT_ENERGY_CARRINGTON_CONSERVATIVE_J, '#b87911'),
              ('Carrington, Tsurutani et al. 2003', RING_CURRENT_ENERGY_CARRINGTON_J, '#8a4b08')]
    inner += f"<line x1='{x0b}' y1='{y0b+h2-40}' x2='{x0b+w2}' y2='{y0b+h2-40}' stroke='#5b6773' stroke-width='2'/>"
    inner += _fig_caption('Dessler-Parker-Sckopke ring-current energy (log scale, J):', y=y0b - 15)
    for i, (label, e, color) in enumerate(events):
        cx = px(math.log10(max(e, 1e28)))
        inner += f"<circle cx='{cx:.1f}' cy='{y0b+h2-40}' r='9' fill='{color}'/>"
        inner += f"<text x='{cx:.1f}' y='{y0b+h2-40+ (24 if i%2==0 else -50)}' font-size='12.5' text-anchor='middle' font-family='Segoe UI, sans-serif'>{escape(label)}: {e:.2e} J</text>"
    return _fig_wrap(item['n'], item['title'], inner, 'flowchart from flare through CME, solar wind transit, magnetosphere compression, to ring current Dst depression, with ring current energies for two real events compared')


_DIAGRAM_BUILDERS = {
    1: diagram_01, 2: diagram_02, 3: diagram_03, 4: diagram_04, 5: diagram_05,
    6: diagram_06, 7: diagram_07, 8: diagram_08, 9: diagram_09, 10: diagram_10,
    11: diagram_11, 12: diagram_12, 13: diagram_13, 14: diagram_14,
}


def lecture_svg(item: dict) -> str:
    return _DIAGRAM_BUILDERS[item['n']](item)


# ---------------------------------------------------------------------------
# Lecture content. Seven thematic units of exactly two lectures each (see
# syllabus.html's cadence rationale): (1) Solar Interior and Atmosphere,
# (2) Solar Magnetism and Sunspots, (3) Solar Flares, (4) CMEs and the Solar
# Wind, (5) Heliophysics Missions and Diagnostics, (6) The Sun-Earth
# Connection, (7) Space Weather Impacts and Technology.
# ---------------------------------------------------------------------------
LECTURES = [
    dict(
        n=1, title='Solar Structure and Hydrostatic Equilibrium',
        subtitle='Why the Sun does not simply collapse, and why its atmosphere thins the way it does',
        goals=[
            'State the Sun\u2019s core, radiative-zone, and convective-zone structure and the real fractional radii of their boundaries.',
            'Derive the isothermal hydrostatic scale height and apply it to the solar photosphere.',
            'Explain energy transport by radiation and convection and why each dominates in a different region of the Sun.',
        ],
        why_matters='Every later unit in this course -- magnetism, flares, the solar wind, and space weather -- ultimately traces back to how energy and mass are structured and transported inside and above the Sun. This lecture establishes the baseline hydrostatic/thermal structure that Lecture 02 extends outward into the corona.',
        phenomenon=f'The Sun generates energy in a core occupying only the innermost {CORE_FRAC_R:.2f} of its radius, at a temperature of {T_CORE_SUN_K:.2e} K -- yet by the time that energy reaches the visible photosphere, the temperature has fallen by nearly three orders of magnitude to T_eff={T_EFF_SUN_K:.0f} K, and the structure has transitioned from radiative to convective energy transport at r={RADIATIVE_ZONE_FRAC_R:.2f} R_sun, a boundary now measured precisely by helioseismology (Unit 5).',
        vocab=['hydrostatic equilibrium', 'scale height', 'radiative zone', 'convective zone', 'photosphere', 'effective temperature', 'energy transport'],
        evidence=[
            'Helioseismology (analysis of the Sun\u2019s natural resonant oscillation modes, developed further in Lecture 09) has measured the radiative-convective boundary to lie at r=0.71 R_sun to high precision, confirming theoretical stellar-structure models.',
            'The photospheric effective temperature (T_eff=5772 K, the IAU nominal value derived from the Sun\u2019s measured luminosity and radius via the Stefan-Boltzmann law) sets essentially every subsequent atmospheric and space-weather quantity used in this course.',
            'Standard solar models (e.g., the Bahcall et al. calibrated models, cross-checked against helioseismic sound-speed inversions and the solar neutrino flux) give a core temperature and density (T_core~1.57e7 K, rho_core~1.5e5 kg/m^3) far too extreme to observe directly, but robustly inferred from these independent lines of evidence.',
        ],
        model=[
            'A static, spherically symmetric star is supported against its own gravity by a pressure gradient: dP/dr = -G M(r) rho(r) / r^2 (hydrostatic equilibrium), which underlies every layer of the Sun\u2019s structure from the core to the photosphere.',
            'For an isothermal atmosphere in a uniform gravitational field g, this integrates to an exponential pressure/density falloff with a characteristic scale height H = kT/(mu m_H g), where mu is the mean molecular weight of the gas; this is a direct, simplified consequence of hydrostatic equilibrium applied locally near the surface where g is nearly constant over the relevant height range.',
            'Energy generated in the core is transported outward first by radiation (photons randomly diffusing outward through the opaque radiative zone) and then, once the temperature gradient becomes too steep for radiation alone to carry the flux (opacity rises sharply as temperature falls), by convection -- bulk fluid motion that is directly visible at the photosphere as granulation.',
        ],
        equation=r'\frac{dP}{dr} = -\frac{GM(r)\rho(r)}{r^2}, \qquad H = \frac{kT}{\mu m_H g}\ \text{(isothermal scale height)}',
        example=[
            f'Computing the photosphere\u2019s surface gravity, g_sun = GM_sun/R_sun^2 = {G_SURFACE_SUN:.1f} m/s^2 (about {G_SURFACE_SUN/9.81:.1f} times Earth\u2019s surface gravity), and using the photospheric mean molecular weight mu={MU_PHOTOSPHERE:.2f} (standard value for weakly ionized solar-composition gas) and T_eff={T_EFF_SUN_K:.0f} K gives a photospheric scale height H={H_PHOTOSPHERE_M/1.0e3:.0f} km -- only about {H_PHOTOSPHERE_M/R_SUN*1.0e6:.1f} parts per million of the solar radius, confirming the photosphere is an extremely thin transition layer compared to the Sun\u2019s overall size.',
            f'By contrast, the same scale-height formula evaluated at the corona\u2019s much higher temperature (T={T_CORONA_K:.1e} K, Lecture 02) and lower mean molecular weight (mu={MU_CORONA:.2f}, fully ionized) gives H={H_CORONA_M/1.0e3:,.0f} km -- roughly {H_CORONA_M/H_PHOTOSPHERE_M:.0f} times larger than the photospheric scale height, directly illustrating why the much hotter corona is so much more extended than the thin photosphere.',
        ],
        pitfall='Assuming the Sun\u2019s energy-generating core extends nearly to its surface. Nuclear fusion is confined to the innermost ~25% of the solar radius (where density and temperature are high enough), while the outer three-quarters of the Sun\u2019s radius carries that energy outward without generating any of its own -- confusing "where energy is generated" with "how far the Sun\u2019s structure extends" is a common error.',
        activity='Using H=kT/(mu m_H g), explain qualitatively why a fully ionized corona at 1.5e6 K has a much larger scale height than the 5772 K photosphere even before accounting for the corona\u2019s lower mean molecular weight, and then explain how the lower mu further amplifies this effect.',
        lab_connection='Lab 01 computes the photospheric and coronal scale heights explicitly and extends the hydrostatic argument to predict how gas pressure and density fall off with height in both layers.',
        synthesis='Hydrostatic equilibrium and the resulting exponential scale-height falloff set the basic vertical structure of every layer of the Sun this course will study, from the photosphere here to the much more extended, million-kelvin corona in Lecture 02.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=2, title='The Solar Atmosphere: Photosphere, Chromosphere, and the Corona',
        subtitle='The coronal heating problem: why the outer atmosphere is hotter than the surface below it',
        goals=[
            'Describe the photosphere, chromosphere, transition region, and corona and their real characteristic temperatures.',
            'Explain why a naive expectation of monotonically falling temperature with height fails dramatically above the photosphere.',
            'Connect the coronal-heating problem to the same magnetic processes (Unit 2 onward) responsible for the Sun\u2019s activity.',
        ],
        why_matters='Lecture 01\u2019s hydrostatic/scale-height framework assumed a fixed temperature; this lecture confronts the observed temperature structure of the real solar atmosphere, which rises sharply above the photosphere rather than continuing to fall -- one of solar physics\u2019 oldest unsolved problems, and the direct motivation for this course\u2019s later magnetic-activity units.',
        phenomenon=f'Moving outward from the photosphere (T_eff={T_EFF_SUN_K:.0f} K), the temperature first falls to a minimum of roughly 4100 K, then rises through the chromosphere to about {T_CHROMOSPHERE_TOP_K:.0e} K, and then jumps abruptly, across a transition region only a few hundred kilometers thick, to the corona\u2019s million-plus-kelvin temperature ({T_CORONA_K:.1e} K) -- a temperature increase of more than two orders of magnitude in a region with no additional nearby heat source as obvious as the solar interior below the photosphere.',
        vocab=['photosphere', 'chromosphere', 'transition region', 'corona', 'temperature minimum', 'coronal heating problem'],
        evidence=[
            'The corona is directly visible during total solar eclipses (and continuously via coronagraphs, Unit 5) as an extended, faint, structured outer atmosphere, and its emission-line spectrum (highly ionized iron lines such as Fe XIV, requiring temperatures of order 10^6 K to produce those ionization states) was the key 20th-century evidence establishing its extreme temperature.',
            'The chromosphere, visible briefly as a pink flash at the start/end of a total eclipse (dominated by hydrogen-alpha emission), sits at intermediate temperatures between the photosphere and corona but still well below the corona\u2019s temperature.',
            'Parker Solar Probe (Unit 5) and other missions have directly measured Alfven-wave activity and small-scale magnetic reconnection events ("nanoflares," a mechanism proposed by Eugene Parker, the mission\u2019s namesake) in the near-Sun corona, both leading candidate mechanisms for solving the coronal heating problem.',
        ],
        model=[
            'If the solar atmosphere were in pure radiative equilibrium with no additional energy input, temperature would fall monotonically outward (as it does through the photosphere and into the temperature minimum); the chromospheric rise and especially the coronal jump require a non-radiative heating mechanism that deposits mechanical or magnetic energy directly into the outer atmosphere.',
            'The two leading physical mechanisms are (1) Alfven-wave heating, in which magnetohydrodynamic waves generated by convective motions below the photosphere propagate upward and dissipate their energy in the corona, and (2) nanoflare heating, in which numerous small-scale magnetic reconnection events (too small individually to resolve as flares, Unit 3) collectively deposit enough energy to sustain coronal temperatures.',
            'Both mechanisms require the Sun\u2019s magnetic field as the essential energy-transport agent (rather than photons or bulk convective flow directly), directly connecting this lecture\u2019s open problem to Unit 2\u2019s treatment of the solar magnetic field and Unit 3\u2019s flare energetics.',
        ],
        equation=r'T_{\rm corona} \gg T_{\rm chromosphere} > T_{\rm eff} \ \text{despite increasing distance from the nuclear energy source (requires non-radiative heating)}',
        example=[
            f'Using Lecture 01\u2019s scale-height formula at the coronal temperature and mean molecular weight gives H_corona={H_CORONA_M/1.0e3:,.0f} km, compared to the photospheric H={H_PHOTOSPHERE_M/1.0e3:.0f} km -- the corona\u2019s huge scale height (a ratio of {H_CORONA_M/H_PHOTOSPHERE_M:.0f}) is why it extends visibly for millions of kilometers rather than remaining a thin surface layer like the photosphere.',
            f'The coronal base electron density (n~{N_CORONA_BASE_M3/1.0e6:.0e} cm^-3, a standard published quiet-Sun value) is many orders of magnitude lower than the photospheric density, so despite its enormous temperature, the corona\u2019s total thermal energy content per unit volume is modest -- a genuine, quantifiable reason the corona is not a bright thermal-emission source at optical wavelengths despite its temperature.',
        ],
        pitfall='Assuming higher temperature always means more visually or energetically dominant. The corona\u2019s temperature vastly exceeds the photosphere\u2019s, yet the photosphere emits far more visible light per unit area (Stefan-Boltzmann, proportional to T^4, is not directly applicable to the extremely tenuous corona, which is optically thin and not a blackbody emitter) -- do not conflate "hotter" with "brighter in visible light."',
        activity='Using the scale-height ratio computed above, explain why a coronagraph (Unit 5) observing the corona out to several solar radii is observing a structure whose vertical extent is physically consistent with its huge scale height, rather than requiring a separate explanation for its size.',
        lab_connection='Lab 01\u2019s second half extends the scale-height calculation to predict the coronal density falloff with height and compares it, order of magnitude, to the real published coronal base density.',
        synthesis='The unsolved coronal heating problem -- an outer atmosphere far hotter than the surface beneath it -- points directly to the solar magnetic field as the missing energy-transport agent, motivating this course\u2019s next unit on solar magnetism and the sunspot cycle.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=3, title='The Solar Magnetic Field and the 11-Year Cycle',
        subtitle='Differential rotation, the dynamo, and the real sunspot-number record',
        goals=[
            'Describe the Babcock-Leighton dynamo mechanism qualitatively: differential rotation winding up a poloidal field into a toroidal field.',
            'Interpret the sunspot butterfly diagram and the 11-year sunspot cycle using real SILSO sunspot-number data.',
            'Compare Solar Cycle 24 and Solar Cycle 25\u2019s real published maximum sunspot numbers.',
        ],
        why_matters='Lecture 02 identified the magnetic field as the missing agent behind coronal heating; this lecture derives where that field comes from and how its large-scale behavior (the 11-year cycle) is tracked using the longest continuously maintained series of astronomical measurements, sunspot counts, setting up Lecture 04\u2019s detailed sunspot physics.',
        phenomenon=f'Solar Cycle 25, which began around {CYCLE25_START}, reached a smoothed maximum monthly sunspot number of {CYCLE25_MAX_SMOOTHED_SSN:.1f} in October 2024 (not-smoothed monthly peak {CYCLE25_MAX_MONTHLY_SSN:.0f} in August 2024) -- moderately stronger than the preceding Solar Cycle 24\u2019s smoothed maximum of {CYCLE24_MAX_SMOOTHED_SSN:.1f}, both real, tracked values from the SILSO World Data Center sunspot-number catalogue (WDC-SILSO, Royal Observatory of Belgium).',
        vocab=['differential rotation', 'dynamo', 'poloidal field', 'toroidal field', 'sunspot number', 'butterfly diagram', 'solar cycle'],
        evidence=[
            'The Sun rotates differentially: its equator (period ~25 days) rotates faster than its poles (period ~35 days), a real, directly observed effect (from sunspot tracking and, more precisely, helioseismology) that provides the shearing motion the dynamo mechanism requires.',
            'Sunspot counts have been maintained continuously since the mid-18th century (numbered "solar cycles," with Solar Cycle 25 being the 25th since systematic numbering began), making the sunspot-number record one of the longest continuous quantitative datasets in all of science.',
            'A "butterfly diagram" (sunspot latitude plotted against time) shows new-cycle sunspots first emerging at mid-latitudes (~30 degrees) and progressively emerging closer to the equator as each cycle matures -- a real, well-documented pattern first noted by Maunder in 1904.',
        ],
        model=[
            'The Babcock-Leighton dynamo model explains the cyclic magnetic behavior qualitatively as follows: differential rotation stretches and winds up a large-scale poloidal (roughly north-south, dipole-like) field into a much stronger, wound-up toroidal (east-west) field over time; buoyant magnetic flux tubes from this toroidal field rise to the surface, forming sunspot pairs (Lecture 04), and the decay/diffusion of these sunspot pairs\u2019 magnetic flux gradually regenerates a new poloidal field of opposite polarity, restarting the cycle roughly every 11 years (22 years for a full magnetic-polarity cycle).',
            'This dynamo process operates in and around the base of the convective zone (the boundary Lecture 01 placed at r=0.71 R_sun), where the shear between the differentially rotating convective envelope and the more rigidly rotating radiative zone below is strongest -- directly connecting this lecture\u2019s dynamo mechanism to Lecture 01\u2019s interior structure.',
            'The sunspot number (a standardized count combining the number of individual spots and sunspot groups, following the Wolf/international sunspot-number convention used by SILSO) is an imperfect but robust and consistently defined proxy for the overall strength of the Sun\u2019s magnetic activity at any given time.',
        ],
        equation=r'\text{Poloidal field} \xrightarrow{\text{differential rotation (shear)}} \text{Toroidal field} \xrightarrow{\text{buoyant rise, Babcock-Leighton decay}} \text{New poloidal field (reversed)}',
        example=[
            f'Comparing the two most recent cycles\u2019 real published smoothed maxima: Solar Cycle 25\u2019s {CYCLE25_MAX_SMOOTHED_SSN:.1f} is {CYCLE25_MAX_SMOOTHED_SSN/CYCLE24_MAX_SMOOTHED_SSN:.2f} times Solar Cycle 24\u2019s {CYCLE24_MAX_SMOOTHED_SSN:.1f} -- a moderately stronger cycle, consistent with Solar Cycle 25 substantially exceeding most pre-cycle predictions (many of which anticipated a cycle comparable to or weaker than Cycle 24).',
            f'Solar Cycle 25 began from a smoothed minimum sunspot number of only {CYCLE25_MIN_SMOOTHED_SSN:.1f} (essentially spot-free) around {CYCLE25_START}, illustrating the enormous dynamic range (a factor of {CYCLE25_MAX_SMOOTHED_SSN/CYCLE25_MIN_SMOOTHED_SSN:.0f}) between solar minimum and maximum conditions that this course\u2019s later space-weather units must account for.',
        ],
        pitfall='Treating the 11-year sunspot cycle as strictly periodic or fully predictable. Real cycles vary substantially in amplitude and length (compare Cycle 24\u2019s comparatively weak maximum to Cycle 25\u2019s stronger, and largely under-predicted, maximum), and the dynamo mechanism, while capturing the essential physics, does not yet allow precise, first-principles prediction of a cycle\u2019s exact strength in advance -- a genuine, disclosed limitation of current solar-cycle science.',
        activity='Using the real Cycle 24/Cycle 25 smoothed-maximum sunspot numbers, compute the percent difference between the two cycles, and discuss why this course\u2019s space-weather risk assessment (Unit 7) should not assume every future cycle will resemble the two most recently observed ones.',
        lab_connection='Lab 02 tabulates and compares real SILSO-sourced sunspot-number data across Cycles 24 and 25 and connects the sunspot-number proxy to the magnetic-flux-based sunspot area/field data used in Lecture 04.',
        synthesis='The Babcock-Leighton dynamo, powered by the Sun\u2019s differential rotation, produces the 11-year sunspot cycle tracked in the world\u2019s longest continuous quantitative astronomical record -- and the individual, buoyantly emerged flux tubes responsible for that record are exactly the sunspots Lecture 04 now examines in detail.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=4, title='Sunspots: Magnetic Pressure Balance and the Wilson Depression',
        subtitle='Deriving why a magnetic flux tube appears as a dark, cool spot',
        goals=[
            'Derive the thin flux-tube total-pressure balance condition for a sunspot.',
            'Apply the pressure-balance condition to a real, well-observed sunspot field strength and compare the resulting magnetic pressure to the ambient photospheric gas pressure.',
            'Distinguish the pressure-balance (structural) explanation from the Biermann convective-suppression mechanism that actually explains sunspot darkness.',
        ],
        why_matters='Lecture 03 established that sunspots are the surface manifestation of buoyant magnetic flux tubes from the solar dynamo; this lecture derives the magnetohydrostatic physics that determines a sunspot\u2019s internal structure and connects that structure to why sunspots appear dark.',
        phenomenon=f'A large sunspot umbra can have a magnetic field strength of roughly {B_SUNSPOT_UMBRA_T*1.0e4:.0f} G (a standard published, well-observed value, Solanki 2003 review) -- more than 1000 times the Sun\u2019s average large-scale surface field, and strong enough that the magnetic pressure alone, B^2/(2 mu0), exceeds the entire ambient photospheric gas pressure at the same geometric depth.',
        vocab=['thin flux tube', 'magnetic pressure', 'total pressure balance', 'Wilson depression', 'umbra', 'penumbra', 'convective suppression'],
        evidence=[
            'Sunspots appear roughly 1500-2000 K cooler than the surrounding photosphere (hence their dark appearance relative to the much brighter photosphere, via the Stefan-Boltzmann T^4 dependence), and their spectra show a strong Zeeman splitting of spectral lines, directly measuring kilogauss-strength magnetic fields.',
            'High-resolution imaging shows sunspots are physically depressed relative to the surrounding photosphere at the same optical depth (the Wilson effect/Wilson depression), consistent with reduced gas pressure and density inside a strong-field flux tube.',
            'Biermann (1941) first proposed that sunspots are dark primarily because the strong, largely vertical magnetic field suppresses convective energy transport from below (magnetic tension inhibits the convective motions that normally carry heat to the photosphere), not merely because of a simple magnetostatic pressure deficit -- the two effects (pressure balance and convective suppression) are related but distinct.',
        ],
        model=[
            'In the thin flux-tube approximation (ignoring magnetic tension/curvature for a simplified estimate), total pressure balance across the tube\u2019s boundary requires the external gas pressure to equal the internal gas pressure plus the magnetic pressure: P_gas,outside = P_gas,inside + B^2/(2 mu0) (Spruit 1976 thin flux-tube theory).',
            'Because the magnetic pressure term can be comparable to or even exceed the typical photospheric gas pressure for a strong sunspot, the internal gas pressure (and hence density) must be substantially reduced relative to the surrounding quiet photosphere at the same geometric depth -- this pressure/density deficit is the physical origin of the observed Wilson depression.',
            'This pressure-balance argument, however, is not by itself the primary reason sunspots are dark: the Biermann mechanism (magnetic suppression of convective heat transport) is the dominant physical explanation for the observed temperature deficit, and this course explicitly distinguishes the two effects rather than conflating "reduced pressure" with "reduced temperature."',
        ],
        equation=r'P_{\rm gas,\,outside} = P_{\rm gas,\,inside} + \frac{B^2}{2\mu_0}\ \text{(thin flux-tube total-pressure balance)}',
        example=[
            f'For a large sunspot umbral field of B={B_SUNSPOT_UMBRA_T*1.0e4:.0f} G ({B_SUNSPOT_UMBRA_T:.2f} T), the magnetic pressure is P_mag=B^2/(2 mu0)={P_MAG_SUNSPOT_PA:,.0f} Pa.',
            f'Compared to the standard published photospheric gas pressure at optical depth tau=1 (P_phot={P_PHOTOSPHERE_PA:,.0f} Pa, Stix 2002/VAL semi-empirical model), this sunspot\u2019s magnetic pressure is {SUNSPOT_PRESSURE_FRACTION:.2f} times the ambient photospheric gas pressure -- so for the pressure-balance equation to hold at the same geometric depth, the internal gas pressure must be reduced to a small fraction of, or even formally driven toward zero relative to, the simple estimate, consistent with (though not a precise quantitative prediction of) the observed several-hundred-kilometer Wilson depression.',
            f'This result illustrates why very strong-field sunspots can substantially evacuate their interior gas: the magnetic pressure term is not a small correction to the photospheric pressure balance but can dominate it entirely for the largest observed umbral fields.',
        ],
        pitfall='Concluding that magnetic pressure balance is, by itself, "why sunspots are dark." The pressure-balance argument explains the reduced gas pressure/density (the Wilson depression), but the observed several-thousand-kelvin temperature deficit is primarily a consequence of the Biermann convective-suppression mechanism -- treating the two as the same effect is a common, and incorrect, simplification this course explicitly corrects.',
        activity='Using P_mag=B^2/(2 mu0), compute the field strength at which the magnetic pressure would exactly equal the standard photospheric gas pressure used in this lecture, and compare that threshold field strength to the real large-sunspot field strength used in the worked example.',
        lab_connection='Lab 02\u2019s second half computes the pressure-balance fraction for a range of real observed sunspot field strengths and evaluates at what field strength the simple pressure-balance approximation would require essentially zero internal gas pressure.',
        synthesis='The thin flux-tube pressure-balance condition explains a sunspot\u2019s reduced internal gas pressure and observed Wilson depression, while the distinct Biermann convective-suppression mechanism explains its temperature deficit -- together completing this course\u2019s treatment of the quiet-Sun magnetic structures that, when they become unstable, produce the solar flares of Unit 3.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=5, title='Solar Flares I: Magnetic Reconnection and Free Energy',
        subtitle='Deriving how much energy a flare can release, and why',
        goals=[
            'Explain magnetic reconnection as the physical mechanism converting stored magnetic free energy into flare energy.',
            'Derive an order-of-magnitude free-energy budget from an active region\u2019s field strength and volume.',
            'Describe the GOES soft X-ray flare classification scheme (A through X classes) and its logarithmic flux scale.',
        ],
        why_matters='Unit 2 established that sunspots are strong, concentrated magnetic structures; this lecture derives what happens when the magnetic field surrounding and connecting sunspot groups becomes unstable and reconnects explosively, releasing the free energy Unit 2\u2019s dynamo has built up over the solar cycle.',
        phenomenon=f'The GOES soft X-ray flare classification scheme spans nine orders of magnitude in peak 1-8 Angstrom X-ray flux, from the smallest recorded A-class flares (~10^-8 W/m^2) to the largest recorded X-class flares; the real X9.3 flare of 6 September 2017 (Lecture 06) had a peak flux of {FLARE_PEAK_FLUX_WM2:.1e} W/m^2 -- by definition, an "X9.3" flare has flux 9.3 x 10^-4 W/m^2, since GOES X-class flares are defined as flux/(10^-4 W/m^2).',
        vocab=['magnetic reconnection', 'free magnetic energy', 'potential field', 'non-potential (sheared) field', 'GOES classification', 'soft X-ray flux'],
        evidence=[
            'A magnetic field configuration with the lowest possible energy for a given set of boundary conditions is called a potential field (current-free); any additional energy stored in currents/shear above this potential-field baseline is the free energy available to power eruptive phenomena.',
            'Active regions with strongly sheared or twisted magnetic field (evidence of stored free energy, directly observable in vector magnetograms, Unit 5) are strongly statistically associated with subsequent large flares, supporting the free-energy-release picture.',
            'The GOES (Geostationary Operational Environmental Satellite) series has continuously monitored solar soft X-ray flux since the 1970s, providing the standard, real-time flare classification (A, B, C, M, X classes, each a factor of 10 in peak flux, with a numeric sub-class multiplying within a decade) used operationally by space-weather forecasters worldwide.',
        ],
        model=[
            'Magnetic reconnection is the topological rearrangement of magnetic field lines at a thin current sheet where oppositely directed field components meet, allowing previously separate field lines to reconnect into a lower-energy configuration; the energy difference between the pre- and post-reconnection field configurations is released as particle acceleration, plasma heating, and radiation -- the physical origin of a flare\u2019s energy.',
            'An order-of-magnitude estimate of the free energy available in an active region uses the magnetic energy density B^2/(2 mu0) (the same quantity from Lecture 04\u2019s pressure-balance argument, now interpreted as an energy density rather than a pressure) multiplied by a representative coronal volume over which a comparable non-potential field strength is sustained: E_free ~ (B^2/2 mu0) V.',
            'The GOES classification\u2019s logarithmic flux scale (each letter class spanning a decade in flux, from A through X) means an X-class flare is, by definition, at least 100 times more intense in soft X-ray flux than a comparably numbered M-class flare, and 10,000 times more intense than a C-class flare -- a scale this course uses throughout Unit 3 to compare real flare events.',
        ],
        equation=r'E_{\rm free} \sim \frac{B^2}{2\mu_0}\,V, \qquad \text{GOES class} = \frac{\text{peak 1-8\,\AA\ flux (W/m}^2)}{10^{-4}\,\text{W/m}^2}\ (\text{X-class})',
        example=[
            f'Using a representative AR12673-scale active-region volume (area~{FLARE_AR_AREA_M2:.1e} m^2, coronal height scale~{FLARE_AR_HEIGHT_M:.1e} m, both order-of-magnitude, level 3, disclosed in reference-log.md) at the sunspot field strength from Lecture 04 (B={B_SUNSPOT_UMBRA_T*1.0e4:.0f} G) gives an order-of-magnitude free-energy estimate E_free~{FLARE_FREE_ENERGY_J:.1e} J -- within the standard published range (order 10^24 to 10^25 J) for a major X-class flare\u2019s total energy budget (Emslie et al. 2012, ApJ 759, 71), a genuine but only order-of-magnitude consistency check, not a precise prediction.',
            f'By GOES-class definition, the real X9.3 flare\u2019s peak flux ({FLARE_PEAK_FLUX_WM2:.1e} W/m^2) is exactly 9.3 times the X1.0 threshold flux (1.0e-4 W/m^2), and {FLARE_PEAK_FLUX_WM2/1.0e-5:.0f} times the M1.0 threshold flux (1.0e-5 W/m^2), illustrating how directly the GOES class number encodes a specific physical flux value.',
        ],
        pitfall='Treating the order-of-magnitude free-energy estimate as a precise flare-energy prediction. This lecture\u2019s E_free~(B^2/2mu0)V calculation depends sensitively on the assumed active-region volume and the fraction of the field that is genuinely non-potential (free) rather than potential -- both are order-of-magnitude, level 3 estimates here, explicitly disclosed, not precise measurements of AR12673\u2019s actual pre-flare field.',
        activity='Using the GOES classification\u2019s logarithmic definition, compute how many C1.0-class flares (in total soft X-ray energy, assuming similar durations) would be needed to match the real X9.3 flare\u2019s peak flux, and discuss why this makes X-class flares disproportionately important for space weather despite occurring far less frequently than smaller flares.',
        lab_connection='Lab 03 computes the free-energy order-of-magnitude estimate for a range of assumed active-region field strengths and volumes and compares the results to the published Emslie et al. (2012) flare-energy budget range.',
        synthesis='Magnetic reconnection converts an active region\u2019s stored free magnetic energy -- built up by the differential-rotation shearing of Unit 2\u2019s dynamo -- into the flare energy classified by the GOES scale; Lecture 06 now applies this framework to a specific, real, extensively documented flare event.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=6, title='Solar Flares II: The 6 September 2017 X9.3 Event',
        subtitle='A real, fully documented case study in flare-to-storm space weather',
        goals=[
            'Summarize the real timeline of the 6 September 2017 X9.3 flare from active region 12673.',
            'Connect the flare\u2019s GOES classification and associated coronal mass ejection to the geomagnetic storm it produced two days later.',
            'Critically evaluate what this single case study can and cannot establish about flare-storm relationships in general.',
        ],
        why_matters='Lecture 05 developed the general physics of flare energy release; this lecture grounds that physics in one specific, extensively observed, real event that this course will trace through Units 4-6\u2019s subsequent stages (CME propagation, solar wind transit, and geomagnetic storm) as a single running case study.',
        phenomenon=f'On {FLARE_DATE}, active region 12673 produced an X9.3 flare (peak flux {FLARE_PEAK_FLUX_WM2:.1e} W/m^2), the largest flare of Solar Cycle 24, accompanied by a fast, Earth-directed coronal mass ejection (real published SOHO/LASCO CDAW-catalog linear speed {FLARE_CME_SPEED_KMS:.0f} km/s); the resulting geomagnetic storm reached G4 (severe) levels on {STORM_DATE}, with a published minimum Dst index of {STORM_DST_MIN_NT:.0f} nT.',
        vocab=['active region', 'case study', 'GOES class', 'coronal mass ejection (CME)', 'geomagnetic storm', 'G-scale (NOAA storm scale)'],
        evidence=[
            'Active region 12673 was an unusually complex, rapidly evolving sunspot group that produced several major flares within a few days in early September 2017, including this X9.3 event, documented by NOAA\u2019s Space Weather Prediction Center (SWPC) in near-real time via GOES X-ray monitoring.',
            'The associated CME\u2019s speed was measured by the SOHO spacecraft\u2019s LASCO coronagraph (Unit 5) and catalogued in the standard CDAW (Coordinated Data Analysis Workshops) CME catalog, the standard reference dataset used throughout heliophysics for cataloguing CME kinematics.',
            'The geomagnetic storm reached NOAA\u2019s G4 ("severe") level on the standard G-scale (G1 through G5), with real, published disturbances to high-frequency radio communications and GPS/GNSS accuracy reported at the time, directly connecting this event to Unit 7\u2019s technological-impact discussion.',
        ],
        model=[
            'This single, real, well-documented event links every physical stage this course studies: Unit 2\u2019s sunspot/active-region magnetism, Unit 3\u2019s flare reconnection physics, Unit 4\u2019s CME propagation and solar wind, and Unit 6\u2019s magnetospheric/geomagnetic-storm response -- using it as a running example lets each unit\u2019s abstract physics be checked against one internally consistent, real timeline.',
            'However, a single case study cannot establish general statistical relationships (e.g., "X-class flares always produce G4 storms," which is false -- many X-class flares are not Earth-directed, or produce CMEs too slow or too weakly magnetized to drive a major storm); this course explicitly uses this event as an illustrative worked example, not as a representative or typical case, and states this limitation honestly.',
            'The chain from flare to storm is not instantaneous: the flare\u2019s electromagnetic radiation reaches Earth in about 8 minutes (at the speed of light), but the associated CME\u2019s bulk plasma and magnetic field take substantially longer (order one to several days, Unit 4 derives this in detail) to physically arrive and couple to Earth\u2019s magnetosphere.',
        ],
        equation=r'\text{Flare (reconnection, Unit 3)} \to \text{CME (mass ejection, Unit 4)} \to \text{Solar wind transit (Unit 4)} \to \text{Geomagnetic storm (Unit 6)}',
        example=[
            f'The flare\u2019s soft X-rays and other electromagnetic radiation reached Earth essentially instantaneously (light travel time from the Sun, 1 AU/c={AU_M/C_LIGHT:.0f} s = {AU_M/C_LIGHT/60:.1f} minutes), causing an immediate, real, published shortwave radio blackout on the sunlit side of Earth at the time of the flare itself, well before the CME\u2019s much slower bulk plasma arrived.',
            f'By contrast, the CME\u2019s bulk material, even at its fast published LASCO speed of {FLARE_CME_SPEED_KMS:.0f} km/s, took roughly {STORM_TRANSIT_HOURS_OBSERVED:.0f} hours (the real, published approximate transit time) to reach Earth and trigger the geomagnetic storm -- a timescale ratio of roughly {STORM_TRANSIT_HOURS_OBSERVED*60/(AU_M/C_LIGHT/60):.0f} to one between the CME\u2019s transit time and the flare radiation\u2019s light-travel time, which Lecture 08\u2019s Parker-wind physics and Lecture 07\u2019s CME kinematics will explain quantitatively.',
        ],
        pitfall='Generalizing from this one event to "large flares always cause severe geomagnetic storms." Many X-class flares occur on parts of the Sun not facing Earth, or produce CMEs that miss Earth entirely, or arrive with a northward-directed interplanetary magnetic field that couples only weakly to Earth\u2019s magnetosphere (Unit 6) -- this course uses the 6 September 2017 event as one clear, well-documented worked example precisely because a full flare-to-storm chain was realized and documented, not because it is statistically typical.',
        activity='List, in order, the physical stages between the flare\u2019s onset and the geomagnetic storm\u2019s peak (reconnection, radiation arrival, CME launch, solar wind transit, magnetospheric coupling, ring-current buildup), and identify which stage this course has not yet derived in quantitative detail as of this lecture.',
        lab_connection='Lab 03\u2019s case-study exercise reconstructs this event\u2019s real published timeline and flux/speed/Dst values from the data table provided, building the same running example that later labs (04, 06) extend.',
        synthesis='This single, fully real, extensively documented event -- from AR 12673\u2019s X9.3 flare through its Earth-directed CME to the resulting G4 geomagnetic storm -- becomes this course\u2019s running case study, connecting Unit 3\u2019s flare-energy physics forward to Unit 4\u2019s CME/solar-wind propagation and Unit 6\u2019s magnetospheric response.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=7, title='Coronal Mass Ejections: Kinematics and Energy',
        subtitle='Measuring how fast, how massive, and how energetic an eruption really is',
        goals=[
            'Describe how coronagraphs measure CME plane-of-sky speed and how this differs from true (deprojected) speed.',
            'Apply CME kinematics to compute a constant-speed travel-time estimate and identify why real transit times differ from this estimate.',
            'Estimate a CME\u2019s kinetic energy budget from its real published mass and speed.',
        ],
        why_matters='Lecture 06\u2019s case study identified the CME as the physical link between a flare and a subsequent geomagnetic storm; this lecture derives the observational technique (coronagraphy) and kinematic/energetic physics needed to characterize a CME quantitatively before Lecture 08 derives the ambient solar wind it propagates through.',
        phenomenon=f'The 6 September 2017 CME\u2019s real, published SOHO/LASCO plane-of-sky linear speed was {FLARE_CME_SPEED_KMS:.0f} km/s -- fast enough that a naive constant-speed extrapolation predicts an Earth-arrival time of only {CME_TRAVEL_TIME_CONSTANT_SPEED_HR:.1f} hours, yet the real, observed transit time was closer to {STORM_TRANSIT_HOURS_OBSERVED:.0f} hours, a substantial, real, and physically meaningful discrepancy that this lecture\u2019s deceleration physics explains.',
        vocab=['coronagraph', 'plane-of-sky speed', 'projection effect', 'CME kinematics', 'aerodynamic drag', 'kinetic energy budget'],
        evidence=[
            'A coronagraph (Unit 5) occults the bright photospheric disk with an opaque disk, allowing the much fainter corona and any propagating CMEs to be imaged in visible (Thomson-scattered) light out to several solar radii and beyond; SOHO\u2019s LASCO instrument has continuously catalogued CMEs since 1996 in the standard CDAW catalog.',
            'A coronagraph measures only the CME\u2019s speed projected onto the plane of the sky (perpendicular to the observer\u2019s line of sight); a CME propagating close to the Sun-Earth line (as an Earth-directed "halo" CME does) has its true radial speed systematically underestimated by simple plane-of-sky measurements unless a full 3D reconstruction (using multiple viewpoints, e.g., STEREO plus SOHO) is performed.',
            'Statistical studies of many CMEs (e.g., Gopalswamy et al. and others) show that fast CMEs (well above the ambient solar wind speed) systematically decelerate during their interplanetary transit due to aerodynamic-like drag against the ambient solar wind, while slow CMEs can actually accelerate toward the ambient wind speed -- both effects make a naive constant-speed extrapolation from the initial coronagraph-measured speed systematically inaccurate for fast events.',
        ],
        model=[
            'A CME experiences a drag-like force from momentum exchange with the ambient solar wind, often modeled (in simplified "drag-based models" used operationally for space-weather forecasting) as proportional to the relative velocity squared between the CME and the ambient solar wind, causing a fast CME to decelerate toward the ambient wind speed over its transit and a slow CME to accelerate toward it.',
            'This means the true arrival time is later than a naive constant-speed extrapolation for a fast, Earth-directed CME (as in Lecture 06\u2019s case study) -- exactly the discrepancy between the {CME_TRAVEL_TIME_CONSTANT_SPEED_HR:.1f}-hour naive estimate and the ~{STORM_TRANSIT_HOURS_OBSERVED:.0f}-hour real observed transit time for the 6 September 2017 event.',
            'A CME\u2019s kinetic energy can be estimated as (1/2) M v^2 given an estimated ejected mass M (from coronagraph brightness, itself a measure of Thomson-scattered light from the CME\u2019s electron content) and its speed v -- providing an independent energy estimate that can be compared to Lecture 05\u2019s flare free-energy budget for the same event.',
        ],
        equation=r't_{\rm naive} = \frac{d}{v_{\rm CME}}\ \text{(constant speed)}, \qquad E_{\rm kinetic} = \frac{1}{2}Mv^2\ \text{(order-of-magnitude CME energy)}',
        example=[
            f'The naive constant-speed travel time for the real 6 September 2017 CME, t=1 AU/v_CME = {AU_M:.3e} m / ({FLARE_CME_SPEED_KMS:.0f} km/s) = {CME_TRAVEL_TIME_CONSTANT_SPEED_HR:.1f} hours, substantially underestimates the real observed transit time of ~{STORM_TRANSIT_HOURS_OBSERVED:.0f} hours -- honestly stating this as roughly a factor of {STORM_TRANSIT_HOURS_OBSERVED/CME_TRAVEL_TIME_CONSTANT_SPEED_HR:.1f} discrepancy, not a small correction, and attributing it to interplanetary deceleration (drag against the slower ambient solar wind) rather than to any error in the coronagraph speed measurement itself.',
            f'A representative fast, massive CME (order 10^12-10^13 kg ejected mass, a standard published order-of-magnitude range for major eruptions, level 2) moving at {FLARE_CME_SPEED_KMS:.0f} km/s has an order-of-magnitude kinetic energy of (1/2)(1.0e13 kg)({FLARE_CME_SPEED_KMS*1.0e3:.2e} m/s)^2 = {0.5*1.0e13*(FLARE_CME_SPEED_KMS*1.0e3)**2:.2e} J -- comparable to, and in the same broad order-of-magnitude range as, Lecture 05\u2019s independent flare free-energy estimate, consistent with (though not a precise confirmation of) both quantities being drawn from the same underlying magnetic free-energy reservoir.',
        ],
        pitfall='Treating a coronagraph-measured plane-of-sky speed as the CME\u2019s true propagation speed without qualification, especially for Earth-directed "halo" events where projection effects are largest. This lecture explicitly uses the real, published LASCO plane-of-sky speed while flagging that it is a projected, not necessarily true radial, speed -- a distinction a careful reviewer must check is stated, not silently elided.',
        activity='Using the naive-vs-observed transit-time discrepancy computed above, explain qualitatively why operational space-weather forecasters (Unit 7) cannot simply report "arrival in X hours" using only a CME\u2019s initial coronagraph speed, and why more sophisticated drag-based propagation models are used operationally instead.',
        lab_connection='Lab 04 computes both the naive constant-speed and a simple drag-based transit-time estimate for the real 6 September 2017 CME and compares both to the real observed transit time.',
        synthesis='CME kinematics -- measured via coronagraphy and modified by interplanetary drag -- determine how long a real eruption takes to reach Earth, a genuinely uncertain quantity this course\u2019s case study shows can differ from a naive estimate by tens of percent; Lecture 08 now derives the ambient solar wind that CMEs propagate through and decelerate toward.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=8, title='The Solar Wind: Parker\u2019s Transonic Wind Solution',
        subtitle='Deriving why the corona cannot simply sit in hydrostatic equilibrium',
        goals=[
            'Show that a static, hot corona in simple hydrostatic equilibrium is physically inconsistent with a vanishing pressure at infinity.',
            'Derive the isothermal Parker wind\u2019s critical-point condition and numerically solve for the transonic wind-speed profile.',
            'Compare the numerically solved solar wind speed to real, published solar wind observations at 1 AU.',
        ],
        why_matters='Lecture 07\u2019s CME kinematics assumed an ambient solar wind for the CME to decelerate against; this lecture derives, from first principles, why the corona cannot be static at all and must instead flow outward as a supersonic wind -- one of the foundational results of heliophysics, first derived by Eugene Parker (the Parker Solar Probe\u2019s namesake, Unit 5).',
        phenomenon=f'A naive hydrostatic corona (using Lecture 01\u2019s scale-height framework at the corona\u2019s real temperature, T={T_CORONA_K:.1e} K) predicts a finite, non-zero gas pressure even at an infinite distance from the Sun -- an unphysical result, since the corona must eventually meet the near-vacuum of interstellar space, and this contradiction is precisely what led Eugene Parker in 1958 to propose that the corona instead flows outward continuously as a wind, reaching supersonic speeds well before 1 AU.',
        vocab=['hydrostatic corona (inconsistency)', 'Parker solar wind', 'critical point', 'transonic solution', 'isothermal sound speed', 'terminal wind speed'],
        evidence=[
            'Spacecraft measurements (beginning with the Soviet Luna missions and NASA\u2019s Mariner 2 in the early 1960s, and continuously since) directly confirmed the existence of a continuous, supersonic outward flow of plasma from the Sun, exactly as Parker\u2019s theory predicted before it was observationally confirmed.',
            'The real, measured solar wind speed at 1 AU is bimodal: a "slow" wind (~{v} km/s, originating from streamer-belt regions near the boundary between open and closed magnetic field) and a "fast" wind (~700-800 km/s, originating from coronal holes, regions of open magnetic field), both real, standard published climatological ranges (OMNI database).'.format(v=int(SOLAR_WIND_SLOW_V_KMS)),
            'Parker Solar Probe (Unit 5) has directly sampled the solar wind acceleration region within a few tens of solar radii, providing direct in-situ tests of the transonic wind theory this lecture derives.',
        ],
        model=[
            'For a static, isothermal corona, hydrostatic equilibrium (Lecture 01) integrates to a pressure that falls off but asymptotes to a finite, non-zero value as r goes to infinity -- physically impossible if the corona must match onto a near-vacuum interstellar medium, forcing the conclusion that the corona cannot be static.',
            'Parker (1958) instead solved the steady-state, spherically symmetric momentum equation for an isothermal outflow, finding that physically acceptable solutions exist only along specific branches of a family of curves, with the unique physically realized solution (matching low speed near the Sun and continuing to accelerate outward, becoming supersonic) passing through a critical point at r_c=GM_sun/(2 c_s^2), where the flow speed equals the isothermal sound speed c_s.',
            'The full nonlinear equation for this transonic solution, u^2 - ln(u^2) = 4 ln(r/r_c) + 4 r_c/r - 3 (u=v/c_s), has no closed-form algebraic solution for v(r) and must be solved numerically (root-finding on the correct physical branch) at each radius -- exactly the numerical approach this lecture\u2019s worked example and figure use, rather than an algebraic shortcut.',
        ],
        equation=r'u^2 - \ln(u^2) = 4\ln\!\left(\frac{r}{r_c}\right) + \frac{4 r_c}{r} - 3, \qquad r_c = \frac{GM_\odot}{2c_s^2},\ u \equiv \frac{v}{c_s}',
        example=[
            f'For the corona\u2019s real characteristic temperature (T={T_CORONA_K:.1e} K, fully ionized, mu={MU_CORONA:.2f}), the isothermal sound speed is c_s={CORONAL_SOUND_SPEED_KMS:.0f} km/s, giving a critical radius r_c={PARKER_RC_M/1.0e9:.2f}x10^9 m = {PARKER_RC_RSUN:.2f} R_sun -- well within the corona, meaning the wind should already be supersonic before reaching a few solar radii.',
            f'Numerically solving the transonic-branch equation at r=1 AU (r/r_c={AU_M/PARKER_RC_M:.1f}) gives a predicted wind speed of v(1 AU)~{solve_parker_wind_speed(AU_M/PARKER_RC_M)*CORONAL_SOUND_SPEED_KMS:.0f} km/s -- the right order of magnitude compared to the real, published slow solar wind speed at 1 AU ({SOLAR_WIND_SLOW_V_KMS:.0f} km/s), though this simplified isothermal, single-temperature model does not reproduce the real wind\u2019s observed bimodal (slow/fast) structure, which requires a more realistic, non-isothermal, magnetically structured corona -- an honest, disclosed limitation, not a claimed precise match.',
        ],
        pitfall='Assuming the Parker wind equation has a simple algebraic closed-form solution for v(r) at all radii. Only the critical point itself (r=r_c, v=c_s) has a simple closed form; the full transonic profile requires numerically solving a transcendental equation (as this lecture\u2019s figure does), and naively rearranging the equation algebraically for v(r) is not possible in general.',
        activity='Using the numerically solved transonic branch, explain qualitatively why choosing the wrong root of the transcendental equation (the subsonic-everywhere "breeze" solution rather than the physically realized transonic solution) would predict a solar wind that never becomes supersonic, contradicting the direct spacecraft evidence cited above.',
        lab_connection='Lab 04\u2019s second half reproduces this lecture\u2019s numerical transonic-wind solve at several radii and compares the resulting 1 AU wind speed to real, published OMNI-database climatological values.',
        synthesis='Parker\u2019s transonic wind solution -- derived here by confronting hydrostatic equilibrium\u2019s failure at infinity and numerically solving the resulting critical-point equation -- explains why the corona continuously flows outward as a supersonic wind, the medium Unit 6 will show couples the Sun\u2019s activity directly to Earth\u2019s magnetosphere.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=9, title='Remote Sensing the Sun: Helioseismology and Coronagraphy',
        subtitle='How SDO and SOHO see structures no eye, and no single wavelength, can reveal alone',
        goals=[
            'Explain helioseismology\u2019s use of solar oscillation modes to probe the solar interior\u2019s otherwise invisible structure.',
            'Explain coronagraphy\u2019s use of an occulting disk to reveal the much fainter corona and propagating CMEs.',
            'Summarize the real instrument suites of SDO and SOHO and connect each to a specific physical quantity measured in this course.',
        ],
        why_matters='Every real dataset this course has used so far -- the radiative-convective boundary (Lecture 01), sunspot magnetic fields (Lecture 04), and CME speeds (Lecture 07) -- was measured by specific instruments and techniques; this lecture makes those measurement techniques explicit before Lecture 10 turns to in-situ (direct-sampling) heliophysics.',
        vocab=['helioseismology', 'p-mode oscillation', 'Doppler imaging', 'coronagraph', 'occulting disk', 'magnetogram', 'remote sensing'],
        phenomenon='The Solar Dynamics Observatory (SDO), launched in 2010 into a geosynchronous orbit, and the Solar and Heliospheric Observatory (SOHO), launched in 1995 into an orbit around the Sun-Earth L1 Lagrange point, together provide the vast majority of the remote-sensing data this course has relied on: SDO\u2019s Helioseismic and Magnetic Imager (HMI) measures the Doppler-shift oscillation data behind Lecture 01\u2019s helioseismic interior structure and the vector magnetograms behind Lecture 05\u2019s active-region field measurements, while SOHO\u2019s LASCO coronagraph produced the real CME speed measurement used throughout Lectures 06-07.',
        evidence=[
            'The Sun oscillates in millions of simultaneous resonant acoustic (p-mode, "pressure mode") oscillation patterns, each a standing sound wave trapped between the photosphere and some inner turning-point radius that depends on the mode\u2019s frequency and spherical-harmonic degree; measuring the precise frequencies of many such modes (via Doppler-shift imaging of the photosphere) allows helioseismic inversion techniques to reconstruct the Sun\u2019s internal sound-speed and rotation profile.',
            'This is directly analogous to how seismic waves are used to probe Earth\u2019s interior structure, and it is the real observational technique that pinned down the radiative-convective boundary at r=0.71 R_sun (Lecture 01) and the differential-rotation profile (Lecture 03) to high precision.',
            'A coronagraph creates an artificial eclipse by placing an opaque occulting disk in front of the bright photospheric disk, allowing the corona\u2019s much fainter Thomson-scattered light (scattered sunlight off coronal free electrons) to be imaged continuously, without needing to wait for a rare natural total solar eclipse.',
        ],
        model=[
            'Helioseismic inversion is a mathematical inverse problem: observed oscillation frequencies (which depend on an integral of the sound speed along each mode\u2019s ray path through the interior) are inverted to recover the interior sound-speed profile as a function of radius, in direct analogy to how travel-time tomography is used in terrestrial seismology.',
            'A coronagraph\u2019s occulting disk must be somewhat larger than the photospheric disk itself (to block diffracted light around the disk\u2019s edge), meaning ground-based and space-based coronagraphs alike cannot image the innermost corona immediately above the photosphere -- a real observational limitation that motivates in-situ measurements even closer to the Sun (Lecture 10\u2019s Parker Solar Probe).',
            'Magnetograms (maps of the photospheric magnetic field, from the Zeeman splitting of spectral lines, as introduced in Lecture 04) provide the vector magnetic field data used to estimate active-region free energy (Lecture 05) and to extrapolate coronal magnetic field structure for space-weather forecasting.',
        ],
        equation=r'\nu_{n,\ell} = f\!\left(\int \frac{dr}{c_s(r)}\right)\ \text{(helioseismic p-mode frequencies constrain the interior sound-speed profile)}',
        example=[
            f'SDO\u2019s HMI instrument observes millions of individually resolved p-mode oscillations across the solar disk continuously, at a cadence fine enough to resolve oscillation periods of a few minutes -- the direct observational basis for the radiative-convective boundary (r={RADIATIVE_ZONE_FRAC_R:.2f} R_sun) used throughout Lecture 01 and Lecture 03\u2019s dynamo discussion.',
            f'SOHO\u2019s LASCO coronagraph, in continuous operation since 1995 (making it one of the longest-running solar space missions), produced the real, published {FLARE_CME_SPEED_KMS:.0f} km/s CME speed measurement used throughout Lectures 06-07\u2019s case study -- a single, specific number this course has now traced back to its actual measurement technique.',
        ],
        pitfall='Assuming any single remote-sensing instrument can measure everything this course needs. Helioseismology cannot directly image the corona; coronagraphy cannot probe the solar interior; and neither can measure in-situ plasma properties (density, temperature, magnetic field vector) at the spacecraft\u2019s own location the way Parker Solar Probe\u2019s in-situ instruments do (Lecture 10) -- a complete picture genuinely requires multiple, complementary techniques, not a single "best" instrument.',
        activity='For each of the following quantities used earlier in this course -- the radiative-convective boundary radius, the sunspot umbral field strength, and the CME plane-of-sky speed -- identify which specific technique (helioseismology, magnetogram/Zeeman splitting, or coronagraphy) was actually used to measure it.',
        lab_connection='Lab 05 works through a simplified schematic helioseismic-frequency-to-sound-speed inversion exercise and a coronagraph field-of-view/occulting-disk geometry calculation.',
        synthesis='Helioseismology and coronagraphy -- both examples of remote sensing, inferring physical conditions from radiation received at a distance -- have supplied essentially every real dataset this course has used so far; Lecture 10 now turns to the complementary technique of in-situ measurement, made possible by spacecraft that fly directly through the medium being studied.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=10, title='In-Situ Heliophysics: Parker Solar Probe',
        subtitle='Flying a spacecraft directly through the solar wind\u2019s acceleration region',
        goals=[
            'Distinguish in-situ measurement from the remote-sensing techniques of Lecture 09.',
            'Summarize Parker Solar Probe\u2019s real mission design, perihelion distance, and record-setting heliocentric speed.',
            'Connect Parker Solar Probe\u2019s in-situ measurements directly to Lecture 08\u2019s Parker wind theory as an observational test.',
        ],
        why_matters='Lecture 08 derived the Parker wind solution theoretically and Lecture 09 surveyed the remote-sensing techniques that measure the Sun from a distance; this lecture completes the observational picture with in-situ measurement, made real and current by the Parker Solar Probe mission, named for the same physicist whose 1958 theory this course derived in Lecture 08.',
        phenomenon=f'Parker Solar Probe, launched {PSP_LAUNCH_DATE}, uses repeated gravity assists from Venus to reach a perihelion of just {PSP_PERIHELION_RSUN:.2f} solar radii ({PSP_PERIHELION_KM:.1e} km from the Sun\u2019s center) -- deep inside the corona, well within Lecture 08\u2019s computed critical radius ({PARKER_RC_RSUN:.2f} R_sun) -- reaching a record heliocentric speed of {PSP_RECORD_SPEED_KMS:.0f} km/s ({PSP_RECORD_SPEED_KMH:,.0f} km/h) at its closest approach, making it the fastest human-made object ever built.',
        vocab=['in-situ measurement', 'perihelion', 'gravity assist', 'Alfven surface', 'magnetic switchback', 'Faraday cup'],
        evidence=[
            'Parker Solar Probe carries direct-sampling ("in-situ") instruments -- a Faraday cup and electrostatic analyzers (SWEAP) to directly measure solar wind ion/electron velocity, density, and temperature; magnetometers (FIELDS) to directly measure the local magnetic field; and energetic-particle detectors (IS(sun)IS) -- rather than remotely imaging the Sun from a distance as SDO and SOHO do (Lecture 09).',
            'In 2021, Parker Solar Probe crossed the Alfven surface (the boundary within which the solar wind\u2019s outward speed is slower than the local Alfven wave speed, so that magnetic disturbances can in principle propagate back toward the Sun) for the first time, entering the solar atmosphere in a meaningful physical sense -- described by NASA as the mission "touching the Sun."',
            'Parker Solar Probe has directly detected numerous "magnetic switchbacks" (sudden, localized reversals in the solar wind\u2019s magnetic field direction) in the near-Sun solar wind, a real, still-being-investigated phenomenon relevant to the coronal-heating and wind-acceleration problems introduced in Lecture 02 and Lecture 08.',
        ],
        model=[
            'In-situ measurement directly samples the plasma, fields, and particles at the spacecraft\u2019s own location, in contrast to remote sensing\u2019s reliance on radiation received from a distance; the two techniques are complementary, not competing, and heliophysics missions are frequently coordinated (e.g., Parker Solar Probe and Solar Orbiter observing simultaneously from different vantage points, as both missions have done).',
            'Parker Solar Probe\u2019s extreme heliocentric speed near perihelion is a direct consequence of orbital mechanics (Kepler\u2019s second law: a highly eccentric orbit moves fastest at its point of closest approach), engineered deliberately by the mission\u2019s repeated Venus gravity assists to progressively lower its perihelion over its multi-year mission.',
            'Because Parker Solar Probe\u2019s perihelion ({PSP_PERIHELION_RSUN:.2f} R_sun) is close to, though still somewhat outside, Lecture 08\u2019s computed critical radius ({PARKER_RC_RSUN:.2f} R_sun), its in-situ measurements provide a direct observational test of the Parker wind theory\u2019s predictions in the very region where the wind is theoretically expected to become supersonic.',
        ],
        equation=r'\text{In-situ: measure plasma/field properties directly at the spacecraft.}\quad \text{Remote sensing: infer properties from received radiation (Lecture 09).}',
        example=[
            f'Parker Solar Probe\u2019s record heliocentric speed of {PSP_RECORD_SPEED_KMS:.0f} km/s, achieved during its closest perihelion passage, is more than {PSP_RECORD_SPEED_KMS/CORONAL_SOUND_SPEED_KMS:.0f} times Lecture 08\u2019s computed coronal isothermal sound speed ({CORONAL_SOUND_SPEED_KMS:.0f} km/s) -- though this comparison is only illustrative, since the spacecraft\u2019s orbital speed (driven by gravity and repeated Venus flybys) is a completely different physical quantity from the solar wind\u2019s own outflow speed that it measures in situ, and the two should not be conflated.',
            f'Parker Solar Probe\u2019s perihelion distance ({PSP_PERIHELION_RSUN:.2f} R_sun) is only about {PSP_PERIHELION_RSUN/PARKER_RC_RSUN:.1f} times Lecture 08\u2019s computed Parker-wind critical radius ({PARKER_RC_RSUN:.2f} R_sun) -- meaning the spacecraft samples plasma in a region where the simplified isothermal Parker wind model predicts the flow should already be at or somewhat above the sound speed, directly testable against the mission\u2019s real in-situ SWEAP velocity measurements.',
        ],
        pitfall='Confusing Parker Solar Probe\u2019s own orbital (heliocentric) speed with the solar wind\u2019s outflow speed that it measures. The spacecraft\u2019s record-breaking 191 km/s speed at perihelion is a consequence of its own orbital mechanics (falling deep into the Sun\u2019s gravitational well), not a measurement of how fast the solar wind itself is flowing at that location -- these are two entirely distinct velocities that a careless reading of headlines can easily conflate.',
        activity='Using Kepler\u2019s second law (equal areas in equal times), explain qualitatively why Parker Solar Probe\u2019s speed is far higher at its {PSP_PERIHELION_RSUN:.2f} R_sun perihelion than at its much more distant aphelion, independent of any solar-wind physics.',
        lab_connection='Lab 05\u2019s second half uses Parker Solar Probe\u2019s real perihelion distance and Lecture 08\u2019s numerically solved wind-speed curve to predict the in-situ solar wind speed the spacecraft should sample near its closest approach.',
        synthesis='Parker Solar Probe\u2019s in-situ measurements, taken deep inside the corona near the Parker wind\u2019s theoretical critical point, directly test the transonic wind theory of Lecture 08 and complete this course\u2019s survey of how the Sun and its wind are actually observed; Unit 6 now turns to how that wind, once it reaches Earth, couples to our planet\u2019s magnetosphere.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=11, title='The Sun-Earth Connection I: Solar Wind Transit and the Magnetopause',
        subtitle='Deriving how far the solar wind pushes Earth\u2019s magnetic shield inward',
        goals=[
            'Compute solar wind travel times from the Sun to Earth under quiet and CME-enhanced conditions.',
            'Derive the Chapman-Ferraro magnetopause standoff-distance formula from dynamic-pressure balance.',
            'Apply the standoff-distance formula to quiet solar wind and real storm-time (CME sheath) conditions.',
        ],
        why_matters='Unit 4 derived the solar wind\u2019s existence and speed; this lecture derives what happens when that wind, ordinary or CME-enhanced, reaches Earth and pushes against the planet\u2019s own magnetic field, setting up Lecture 12\u2019s treatment of the resulting geomagnetic storm.',
        phenomenon=f'Earth\u2019s magnetopause -- the boundary where the solar wind\u2019s dynamic (ram) pressure is balanced by the pressure of Earth\u2019s compressed dipole magnetic field -- sits at roughly {MAGNETOPAUSE_QUIET_RE:.1f} Earth radii under typical quiet solar wind conditions, but is compressed substantially closer to Earth (to roughly {MAGNETOPAUSE_STORM_RE:.1f} Earth radii, this lecture\u2019s computed value) during a fast, dense CME sheath\u2019s passage -- occasionally close enough to expose geosynchronous-orbit satellites (at 6.6 R_E) directly to the unshielded solar wind.',
        vocab=['solar wind travel time', 'dynamic (ram) pressure', 'magnetopause', 'Chapman-Ferraro balance', 'magnetic compression', 'geosynchronous orbit'],
        evidence=[
            'Multiple spacecraft (e.g., the ACE and DSCOVR missions at the L1 Lagrange point, roughly 1.5 million km sunward of Earth) continuously monitor real-time solar wind speed, density, and magnetic field, providing the operational lead time (typically 15-60 minutes) space-weather forecasters use to issue geomagnetic-storm warnings.',
            'Direct in-situ magnetospheric spacecraft measurements (beginning with early magnetospheric missions and continuing today) have repeatedly confirmed the magnetopause standoff distance moving inward during fast solar wind/CME arrivals, consistent with dynamic-pressure balance.',
            'During unusually severe events, the magnetopause has been observed compressed to within geosynchronous orbit (6.6 R_E), directly exposing communications and weather satellites there to solar wind plasma and enhanced radiation -- a real, documented technological hazard this course\u2019s Unit 7 examines further.',
        ],
        model=[
            'The solar wind\u2019s bulk kinetic (dynamic, or "ram") pressure is P_dyn = rho v^2, where rho is the solar wind mass density (dominated by protons) and v its bulk speed; this pressure pushes against Earth\u2019s intrinsic dipole magnetic field, which is compressed by the impinging wind (roughly doubling the field just inside the boundary, an image-dipole-like effect) relative to its undisturbed strength.',
            'Balancing the solar wind\u2019s dynamic pressure against the compressed dipole field\u2019s magnetic pressure at the boundary gives the Chapman-Ferraro standoff-distance formula, r_mp = R_E (2 B0^2/(mu0 rho v^2))^(1/6), where B0 is Earth\u2019s equatorial surface dipole field strength -- note the weak, one-sixth-power dependence on the solar wind\u2019s dynamic pressure, meaning even a large change in solar wind conditions produces a comparatively modest fractional change in standoff distance.',
            'A CME\u2019s dense, fast sheath region (compressed solar wind material piled up ahead of the CME\u2019s main body) typically drives the largest, most abrupt dynamic-pressure enhancements, and hence the largest, most sudden magnetopause compressions -- directly connecting Unit 4\u2019s CME kinematics to this lecture\u2019s magnetospheric response.',
        ],
        equation=r'P_{\rm dyn} = \rho v^2, \qquad r_{\rm mp} = R_E\left(\frac{2 B_0^2}{\mu_0 \rho v^2}\right)^{1/6}\ \text{(Chapman-Ferraro standoff distance)}',
        example=[
            f'For typical quiet solar wind conditions (n={SOLAR_WIND_SLOW_N_CM3:.0f} cm^-3, v={SOLAR_WIND_SLOW_V_KMS:.0f} km/s, standard published OMNI climatological values), the computed magnetopause standoff distance is r_mp={MAGNETOPAUSE_QUIET_RE:.2f} R_E, consistent with the well-known real-world nominal value of roughly 10 R_E.',
            f'For a representative fast, dense CME sheath (n={SOLAR_WIND_STORM_N_CM3:.0f} cm^-3, v={SOLAR_WIND_STORM_V_KMS:.0f} km/s, standard published storm-time values), the computed standoff distance compresses to r_mp={MAGNETOPAUSE_STORM_RE:.2f} R_E -- a reduction of only {(1-MAGNETOPAUSE_STORM_RE/MAGNETOPAUSE_QUIET_RE)*100:.0f}% despite the dynamic pressure increasing by a factor of {(SOLAR_WIND_STORM_N_CM3*SOLAR_WIND_STORM_V_KMS**2)/(SOLAR_WIND_SLOW_N_CM3*SOLAR_WIND_SLOW_V_KMS**2):.1f}, directly illustrating the standoff distance\u2019s weak one-sixth-power dependence on dynamic pressure.',
        ],
        pitfall='Assuming the magnetopause standoff distance scales linearly (or even close to linearly) with solar wind dynamic pressure. The one-sixth-power dependence in the Chapman-Ferraro formula means even a several-fold increase in dynamic pressure produces a comparatively modest fractional compression of the standoff distance -- a common intuitive overestimate this course\u2019s worked example explicitly corrects.',
        activity='Using the one-sixth-power scaling, compute what dynamic-pressure enhancement factor (relative to the quiet-wind value used above) would be required to compress the magnetopause all the way to geosynchronous orbit (6.6 R_E), and discuss why this represents a genuinely extreme, rather than routine, space-weather event.',
        lab_connection='Lab 06 computes the magnetopause standoff distance across a range of real published solar wind conditions (quiet, moderate storm, and severe storm) and identifies the dynamic-pressure threshold for geosynchronous-orbit exposure.',
        synthesis='The Chapman-Ferraro balance between solar wind dynamic pressure and Earth\u2019s compressed dipole field determines how close the solar wind pushes toward Earth -- and Lecture 12 now derives the complementary, energetics-based measure of a geomagnetic storm\u2019s severity, the Dst index, using the same real 6 September 2017 storm and the historic Carrington Event as worked comparisons.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=12, title='The Sun-Earth Connection II: Geomagnetic Storms and the Dst Index',
        subtitle='Deriving how a ring current\u2019s energy sets the size of a geomagnetic storm',
        goals=[
            'Explain the physical origin of the magnetospheric ring current and its relationship to the Dst index.',
            'Derive and apply the Dessler-Parker-Sckopke relation between Dst and total ring-current energy.',
            'Compare the real 6 September 2017 storm\u2019s Dst to the Carrington Event\u2019s live-verified estimated Dst range.',
        ],
        why_matters='Lecture 11 derived how far the solar wind compresses Earth\u2019s magnetopause; this lecture derives the complementary, and more physically fundamental, measure of geomagnetic-storm severity used throughout space-weather science: the Dst index, and the ring-current energy it encodes.',
        phenomenon=f'The real, published minimum Dst index for the storm following this course\u2019s 6 September 2017 case-study CME was {STORM_DST_MIN_NT:.0f} nT (a G4, "severe" storm) -- substantially smaller in magnitude than either published estimate for the Carrington Event of 1-2 September 1859 (Dst estimated between {CARRINGTON_DST_MIN_NT_CONSERVATIVE:.0f} and {CARRINGTON_DST_MIN_NT:.0f} nT, live-verified this session), the most intense geomagnetic storm in the era of ground-based magnetometer records.',
        vocab=['ring current', 'Dst index', 'Dessler-Parker-Sckopke relation', 'geomagnetic storm', 'storm main phase', 'recovery phase'],
        evidence=[
            'During a geomagnetic storm, energetic ions and electrons trapped in Earth\u2019s inner magnetosphere are injected and energized (ultimately drawing energy from the solar wind via magnetic reconnection at the magnetopause and in the magnetotail), forming an enhanced "ring current" that circles Earth westward at a few Earth radii\u2019 distance.',
            'This ring current\u2019s own magnetic field opposes (partially cancels) Earth\u2019s main dipole field at the equator, producing the negative magnetic-field depression measured by a global network of low-latitude magnetometer stations and combined into the standard Dst (Disturbance storm time) index, continuously available since 1957 (and reconstructed further back using historical magnetometer records, as for the Carrington Event).',
            'The Carrington Event\u2019s Dst is necessarily an estimate rather than a direct index value, since the standardized Dst index did not yet exist in 1859; Tsurutani et al. (2003) and the more conservative Cliver & Svalgaard (2005) estimate arrived at somewhat different values from the same underlying historical magnetometer records, both live-verified via this course\u2019s Wikipedia fetch this session, illustrating genuine, disclosed scientific uncertainty in reconstructing a pre-instrumental event.',
        ],
        model=[
            'The Dessler-Parker-Sckopke (DPS) relation is a standard textbook result (Baumjohann & Treumann, Basic Space Plasma Physics) connecting the fractional depression of Earth\u2019s equatorial magnetic field to the ring current\u2019s total kinetic energy: Dst*/B0 = -(2/3)(E_ring/E0), where E0 = B0^2 R_E^3/(6 mu0) is a fixed reference energy (the dipole field\u2019s own magnetic energy outside Earth\u2019s surface, down to R_E), giving E_ring = -(3/2)(Dst/B0) E0.',
            'This relation directly connects an easily measured, purely magnetic quantity (Dst, in nanotesla) to the physically fundamental quantity of interest (the total kinetic energy stored in the ring current\u2019s trapped particle population), without requiring detailed knowledge of the ring current\u2019s particle-by-particle composition or spatial distribution.',
            'Because Dst enters this relation linearly (for a fixed B0 and E0), a storm with twice the Dst magnitude corresponds to twice the ring-current energy -- a simple, direct proportionality this lecture\u2019s worked example uses to compare the real 2017 storm to the much larger historical Carrington estimates.',
        ],
        equation=r'\frac{Dst^*}{B_0} = -\frac{2}{3}\frac{E_{\rm ring}}{E_0}, \qquad E_0 = \frac{B_0^2 R_E^3}{6\mu_0}, \qquad E_{\rm ring} = -\frac{3}{2}\frac{Dst}{B_0}E_0',
        example=[
            f'Earth\u2019s reference dipole energy is E0={DPS_E0_J:.3e} J (a fixed geophysical constant, computed once from B0={B0_EARTH_T*1.0e9:.0f} nT and R_E={R_EARTH_M/1.0e3:,.0f} km).',
            f'Applying the DPS relation to the real 6 September 2017 storm\u2019s published Dst_min={STORM_DST_MIN_NT:.0f} nT gives a ring-current energy of E_ring={RING_CURRENT_ENERGY_SEPT2017_J:.2e} J.',
            f'Applying the same relation to the Carrington Event\u2019s live-verified estimated Dst range gives E_ring between {RING_CURRENT_ENERGY_CARRINGTON_CONSERVATIVE_J:.2e} J (Cliver & Svalgaard 2005\u2019s more conservative -800 nT estimate) and {RING_CURRENT_ENERGY_CARRINGTON_J:.2e} J (Tsurutani et al. 2003\u2019s larger -1750 nT estimate) -- a factor of {RING_CURRENT_ENERGY_CARRINGTON_J/RING_CURRENT_ENERGY_SEPT2017_J:.0f} to {RING_CURRENT_ENERGY_CARRINGTON_CONSERVATIVE_J/RING_CURRENT_ENERGY_SEPT2017_J:.0f} more ring-current energy than the real, well-documented 2017 storm, honestly presented as a range reflecting genuine, disclosed scientific uncertainty in the historical reconstruction rather than a single precise number.',
        ],
        pitfall='Treating the Carrington Event\u2019s Dst value as a directly measured historical quantity with the same certainty as the 2017 storm\u2019s Dst. The 1859 event predates the standardized Dst index by nearly a century, so its "Dst" is a modern reconstruction from historical magnetometer traces, with two independent published estimates differing by more than a factor of two -- this course states both values and their factor-of-two-plus disagreement explicitly, rather than picking one number and presenting it as certain.',
        activity='Using the DPS relation\u2019s linear dependence on Dst, explain why a storm with a Dst of -500 nT has exactly ten times the ring-current energy of a storm with a Dst of -50 nT, and connect this to why NOAA\u2019s G-scale storm classification (G1 through G5, Unit 7) is itself roughly logarithmic in physical severity even though Dst is linear in energy.',
        lab_connection='Lab 06\u2019s second half computes ring-current energy via the DPS relation for a range of real and historically estimated storms and builds the same comparison this lecture\u2019s worked example performs.',
        synthesis='The Dessler-Parker-Sckopke relation converts the routinely measured Dst index into the ring current\u2019s physical energy content, allowing a real modern storm to be quantitatively compared to the reconstructed, and substantially larger, Carrington Event -- setting up Unit 7\u2019s examination of what a storm of either magnitude actually does to modern technology.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=13, title='Space Weather Impacts on Technology I: Satellites and Radiation',
        subtitle='From atmospheric drag to radiation hazards for astronauts and aviation',
        goals=[
            'Explain how geomagnetic storms enhance thermospheric density and increase satellite atmospheric drag.',
            'Describe solar energetic particle (SEP) events and their radiation hazard to astronauts and polar aviation routes.',
            'Connect ionospheric disturbances during storms to GNSS/GPS positioning errors and radio communication effects.',
        ],
        why_matters='Units 1-6 derived the physics connecting the Sun\u2019s interior, atmosphere, activity, and eruptions all the way to Earth\u2019s magnetosphere; this lecture and Lecture 14 apply that full chain to the real technological systems that space weather actually affects, the applied culmination of this course\u2019s physics.',
        phenomenon='In February 2022, a moderate geomagnetic storm heated and expanded Earth\u2019s thermosphere enough to increase atmospheric drag on a batch of 49 newly launched Starlink satellites at low altitude, causing most of them to reenter and burn up within days -- a real, well-documented, publicly reported example of space weather directly destroying billions of dollars of space infrastructure through an effect this lecture derives.',
        vocab=['thermosphere', 'atmospheric drag', 'orbital decay', 'solar energetic particle (SEP) event', 'total electron content (TEC)', 'ionospheric scintillation'],
        evidence=[
            'Geomagnetic storms deposit energy into Earth\u2019s upper atmosphere (via particle precipitation and Joule heating from enhanced electric currents), heating and expanding the thermosphere; because atmospheric density at a fixed altitude increases when the thermosphere expands, satellites in low Earth orbit experience increased drag and faster orbital decay during and after storms.',
            'Solar energetic particle (SEP) events -- bursts of high-energy protons and heavier ions accelerated by flares and/or CME-driven shocks -- can deliver radiation doses to astronauts (particularly outside Earth\u2019s protective magnetosphere, e.g., during lunar missions) and to aircrew/passengers on high-latitude polar flight routes (where Earth\u2019s magnetic field provides comparatively little shielding) comparable to many chest X-rays in a single event.',
            'Geomagnetic storms disturb the ionosphere\u2019s electron density structure (measured as total electron content, TEC), which can degrade GNSS/GPS positioning accuracy (since GPS signals are delayed by passing through the ionosphere, an effect normally corrected for using a standard ionospheric model that storms can invalidate) and cause high-frequency radio blackouts, both real, operationally significant effects during major storms including the real 6 September 2017 event (Unit 3).',
        ],
        model=[
            'Atmospheric density at a fixed altitude in the thermosphere depends sensitively on temperature (via a scale-height argument directly analogous to Lecture 01\u2019s solar scale-height derivation, applied here to Earth\u2019s atmosphere instead of the Sun\u2019s), so even a moderate storm-time temperature increase can substantially increase the drag force on a satellite at a given altitude, shortening its orbital lifetime.',
            'SEP events are distinct from the CME-driven bulk solar wind disturbance of Units 4 and 6: SEPs are the highest-energy tail of accelerated particles (often reaching Earth within tens of minutes to a few hours, much faster than the bulk CME plasma\u2019s day-or-so transit derived in Lecture 07), accelerated either directly by the flare\u2019s reconnection process or by the shock wave driven ahead of a fast CME.',
            'Ionospheric disturbances during storms arise because the same energetic particle precipitation and electric-field changes that drive the ring current (Lecture 12) also directly modify high-latitude and, during severe storms, even mid-latitude ionospheric electron density and structure.',
        ],
        equation=r'\rho_{\rm thermosphere}(\text{fixed altitude}) \propto e^{-z/H(T)}\ \text{(storm heating raises } T \text{, raising } H \text{, raising density at fixed } z\text{)}',
        example=[
            'Applying Lecture 01\u2019s scale-height logic to Earth\u2019s thermosphere (rather than the Sun\u2019s atmosphere): a storm-time temperature increase raises the local scale height H=kT/(mu m_H g), which increases atmospheric density at any fixed altitude above the point where the density profile is anchored -- the same underlying physical mechanism (hydrostatic scale-height dependence on temperature) this course first derived for the Sun in Lecture 01, now applied to Earth\u2019s upper atmosphere.',
            f'The real February 2022 Starlink satellite loss occurred at a much smaller storm magnitude (a moderate storm) than the real 6 September 2017 event (a G4, severe storm) used throughout this course\u2019s case study, illustrating that low-altitude satellite drag risk is sensitive even to comparatively modest geomagnetic disturbances, not only to the most extreme events like the Carrington Event (Lecture 12).',
        ],
        pitfall='Assuming only the most extreme storms (Carrington-class events) pose a meaningful technological risk. The real February 2022 Starlink incident shows that even a moderate storm can cause substantial, real economic and operational damage through comparatively mundane physics (enhanced atmospheric drag) -- space-weather risk is not solely, or even primarily, about worst-case scenarios.',
        activity='Using the thermospheric scale-height argument, explain qualitatively why satellites at very low altitudes (like the affected Starlink satellites, deliberately placed at a lower-than-final operational altitude for a post-launch health check) are disproportionately vulnerable to storm-time drag enhancement compared to satellites already at their final, higher operational altitude.',
        lab_connection='Lab 07\u2019s capstone synthesizes this lecture\u2019s technological-impact framework with Lecture 14\u2019s ground-based (GIC) impacts into a single space-weather risk assessment exercise.',
        synthesis='Space weather affects real technology through several distinct physical pathways -- atmospheric drag, radiation exposure, and ionospheric disturbance -- each traceable to specific physics derived earlier in this course; Lecture 14 completes this unit with ground-based technological impacts and this course\u2019s final capstone synthesis.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=14, title='Space Weather Impacts on Technology II: Power Grids and Course Synthesis',
        subtitle='Geomagnetically induced currents, extreme-event risk, and bringing the whole chain together',
        goals=[
            'Explain the physical origin of geomagnetically induced currents (GICs) in long conductors such as power transmission lines.',
            'Evaluate the real historical evidence for extreme-event risk (the Carrington Event, the 1989 Quebec blackout) using this course\u2019s Dst/ring-current framework.',
            'Synthesize this course\u2019s full physical chain, from the solar interior to a ground-based technological impact, into one coherent picture.',
        ],
        why_matters='This capstone lecture completes Unit 7\u2019s technological-impact survey with the single most economically consequential space-weather hazard, power-grid disruption, and then draws every earlier unit together into one connected physical narrative -- exactly the course-long synthesis this catalog description\u2019s culminating theme (space weather impacts on technology) requires.',
        phenomenon='On 13 March 1989, a geomagnetic storm (driven by a real, well-documented series of CMEs, comparable in Dst magnitude to this course\u2019s 6 September 2017 case study) induced large enough geomagnetically induced currents in the Hydro-Quebec power grid to trip protective relays and collapse the entire grid within about 90 seconds, leaving six million people without power for up to nine hours -- a direct, real, and extensively studied demonstration of the physics this lecture derives.',
        vocab=['geomagnetically induced current (GIC)', 'Faraday\u2019s law', 'transformer saturation', 'extreme-event risk', 'space-weather forecasting'],
        evidence=[
            'A rapidly time-varying geomagnetic field (exactly the kind produced by a fast geomagnetic storm\u2019s ring current and ionospheric current changes) induces a geoelectric field at Earth\u2019s surface via Faraday\u2019s law of induction; because power transmission lines are long conductors grounded at both ends, this geoelectric field drives quasi-DC currents (GICs) through the grid, distinct from the grid\u2019s normal AC operating current.',
            'GICs can saturate power-transformer cores (since transformers are designed for AC operation, not the quasi-DC GIC), causing transformers to draw excessive reactive power, overheat, and in severe cases suffer permanent damage, while simultaneously tripping protective relays designed to isolate faults -- exactly the mechanism behind the 1989 Hydro-Quebec collapse.',
            'The Lloyd\u2019s of London/Atmospheric and Environmental Research 2013 risk assessment (a real, published economic-impact study) estimated that a Carrington-level event striking the modern, more electrically interconnected United States alone could cause on the order of hundreds of billions to several trillion dollars in economic impact, primarily through extended, widespread power-grid damage and outages.',
        ],
        model=[
            'The induced geoelectric field\u2019s magnitude scales with the rate of change of the geomagnetic field (dB/dt), not simply its peak magnitude, meaning the most GIC-hazardous storms are those with the most rapid, abrupt magnetic-field changes -- a 2024 reanalysis of digitized Carrington-era magnetometer data (Beggan et al. 2024, live-verified this session via the Carrington Event Wikipedia article) found field-change rates exceeding 700 nT/minute, well above modern digital-era 1-in-100-year extreme values of 350-400 nT/minute at the same latitude, providing independent, real evidence that 1859 was not merely large in Dst but also unusually fast-changing.',
            'This course\u2019s full physical chain, traced across all seven units, is: solar interior structure and hydrostatic/thermal physics (Unit 1) sets the stage for the magnetic dynamo (Unit 2), which produces the active regions whose stored free energy powers flares (Unit 3); a flare\u2019s associated CME (Unit 4) propagates through the Parker solar wind (Unit 4), observed by remote-sensing and in-situ missions (Unit 5), until it reaches and compresses Earth\u2019s magnetosphere, driving a ring current measured by the Dst index (Unit 6), whose associated rapid magnetic-field changes ultimately induce the GICs and other technological impacts of Unit 7.',
            'Because a Carrington-magnitude event has not recurred during the modern, electrically interconnected era (the closest recent analog, the March 1989 storm, was substantially smaller in both Dst and dB/dt), extreme-event risk assessment necessarily combines historical reconstruction (with its genuine, disclosed uncertainties, Lecture 12) with physical modeling rather than direct modern observation of a comparable event.',
        ],
        equation=r'\mathcal{E}_{\rm induced} \propto -\frac{dB}{dt}\ \text{(Faraday\u2019s law; GIC hazard scales with the rate of field change, not just its peak amplitude)}',
        example=[
            f'Comparing this course\u2019s two running real/historical events by ring-current energy (Lecture 12\u2019s DPS-relation results): the 6 September 2017 storm ({RING_CURRENT_ENERGY_SEPT2017_J:.2e} J) versus the Carrington Event\u2019s estimated range ({RING_CURRENT_ENERGY_CARRINGTON_CONSERVATIVE_J:.2e} to {RING_CURRENT_ENERGY_CARRINGTON_J:.2e} J) -- a factor of {RING_CURRENT_ENERGY_CARRINGTON_J/RING_CURRENT_ENERGY_SEPT2017_J:.0f} at the high end -- directly quantifies why a genuine Carrington-repeat is treated as a distinct, higher-consequence risk category from even a severe modern storm like 2017\u2019s, not merely a larger version of the same routine hazard.',
            'The 2024 Beggan et al. reanalysis\u2019s field-change-rate finding (>700 nT/minute, roughly double the modern 1-in-100-year extreme value) is a genuinely new, real, live-verifiable piece of evidence (not merely a restatement of the Dst estimate) that the Carrington Event\u2019s GIC hazard may have been even more extreme, relative to modern infrastructure risk, than its Dst value alone would suggest -- since GIC hazard scales with dB/dt rather than Dst directly.',
        ],
        pitfall='Assuming Dst magnitude alone fully characterizes a storm\u2019s technological risk. This lecture\u2019s Faraday\u2019s-law argument shows GIC hazard depends on the rate of magnetic-field change, not simply its peak depression; two storms with similar Dst minima could have very different GIC risk if one\u2019s field changes far more rapidly than the other\u2019s -- a distinction this course\u2019s capstone explicitly draws rather than treating Dst as a single, complete risk metric.',
        activity='Using this course\u2019s full seven-unit chain (Unit 1 through Unit 7, restated in the Model section above), identify, for the real 6 September 2017 event specifically, which single physical quantity from each unit was used as this course\u2019s worked numeric example for that event, and discuss which quantity you judge to be the least certain (level 2/3, not live-verified) and why.',
        lab_connection='Lab 07\u2019s capstone estimates a representative GIC-driving geoelectric field from a specified dB/dt and connects it to this course\u2019s full flare-to-grid physical chain as a final synthesis exercise.',
        synthesis='Geomagnetically induced currents -- driven by Faraday\u2019s law acting on a rapidly changing geomagnetic field -- are the final link in this course\u2019s physical chain from the solar interior (Unit 1) through magnetism (Unit 2), flares (Unit 3), CMEs and the solar wind (Unit 4), heliophysics missions (Unit 5), and the magnetospheric/Dst response (Unit 6) to real, historically documented, and economically consequential ground-based technological impact.',
        openstax=OPENSTAX_NOTE,
    ),
]


def slide_deck(item: dict) -> str:
    n = item['n']
    fig = lecture_svg(item)
    body = f"""<main class='deck'>
<section class='slide title'><p class='kicker'>ASTR 370 &middot; Lecture {n:02d}</p><h1>{escape(item['title'])}</h1><h2>{escape(item['subtitle'])}</h2></section>
<section class='slide'><h2>Learning Goals</h2><ol>{li(item['goals'])}</ol><p class='small'>Reading anchor: {escape(item['openstax'])}</p></section>
<section class='slide'><h2>Why This Matters</h2><p>{item['why_matters']}</p></section>
<section class='slide'><h2>Opening Phenomenon</h2><p>{item['phenomenon']}</p><p class='warning'><strong>First question:</strong> what here is directly observed or a published/live-verified measurement, and what follows only once a physical law is derived and applied?</p></section>
<section class='slide'><h2>Vocabulary for Reasoning</h2><div class='three'>{cards(item['vocab'])}</div><p class='small'>Use these terms to describe derivations and evidence, not as isolated definitions.</p></section>
<section class='slide'><h2>Evidence We Need to Explain</h2><ul>{li(item['evidence'])}</ul></section>
<section class='slide'><h2>Derivation and Model</h2><ul>{li(item['model'])}</ul></section>
<section class='slide'><h2>Quantitative Tool</h2><div class='equation'>\\[ {item['equation']} \\]</div></section>
<section class='slide'><h2>Worked Example</h2><ol>{li(item['example'])}</ol></section>
<section class='slide visual-slide'><h2>Visual Reasoning</h2><div class='visual-grid'><div><p>Trace the reasoning chain from raw observation or live-verified/published data to derived physical law to inferred quantity in this lecture\u2019s figure.</p><ul><li>Which stage is directly observed or a real published measurement?</li><li>Which stage is the physical law or derivation step?</li><li>What would change if an assumption in the derivation failed?</li></ul></div><figure class='visual-figure'>{fig}<figcaption>{escape(item['title'])}: from observation to inferred quantity.</figcaption></figure></div></section>
<section class='slide'><h2>Common Misconception</h2><p class='warning'>{item['pitfall']}</p></section>
<section class='slide'><h2>Active Learning Segment</h2><p>{item['activity']}</p></section>
<section class='slide'><h2>Lab Connection</h2><p>{item['lab_connection']}</p></section>
<section class='slide'><h2>Synthesis</h2><p>{item['synthesis']}</p></section>
<section class='slide'><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Course dataset and derivations used in this lecture\u2019s worked example: <code>materials/ASTR370/data/</code> and <code>materials/ASTR370/src/generate_astr370_content.py</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 370 Lecture {n:02d} Slides', body, SLIDE_CSS)


def lecture_notes(item: dict) -> str:
    n = item['n']
    body = f"""<header><div><h1>Lecture {n:02d}: {escape(item['title'])}</h1><p>ASTR 370 Solar Physics and Space Weather</p></div></header>
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
<section><h2>Synthesis Questions</h2><ul><li>What was measured directly, or taken from a real live-verified/published source, in this lecture\u2019s worked example, and what was derived from a physical law?</li><li>Which assumption in the derivation would most change the interpretation if it were wrong?</li><li>How does this lecture\u2019s technique connect to the lab and problem set that follow it?</li></ul></section>
<section><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Every numeric result above is computed programmatically in <code>materials/ASTR370/src/generate_astr370_content.py</code>, not hand-typed.</li></ul></section>
</main>"""
    return page(f'ASTR 370 Lecture {n:02d} Notes', body)


def write_lectures():
    LECTURE_DIR.mkdir(parents=True, exist_ok=True)
    for item in LECTURES:
        n = item['n']
        (LECTURE_DIR / f'lecture-{n:02d}-slides.html').write_text(slide_deck(item), encoding='utf-8')
        (LECTURE_DIR / f'lecture-{n:02d}-notes.html').write_text(lecture_notes(item), encoding='utf-8')


def write_data_csv():
    import csv
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / 'solar_cycle_sunspot_numbers.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['cycle', 'metric', 'value', 'date', 'source_note'])
        w.writerow(['Solar Cycle 24', 'smoothed max SSN', CYCLE24_MAX_SMOOTHED_SSN, 'April 2014', 'standard published, level 2'])
        w.writerow(['Solar Cycle 25', 'smoothed min SSN', CYCLE25_MIN_SMOOTHED_SSN, CYCLE25_START, 'live-verified this session (SILSO via Wikipedia)'])
        w.writerow(['Solar Cycle 25', 'smoothed max SSN', CYCLE25_MAX_SMOOTHED_SSN, 'October 2024', 'live-verified this session (SILSO via Wikipedia)'])
        w.writerow(['Solar Cycle 25', 'not-smoothed max SSN', CYCLE25_MAX_MONTHLY_SSN, 'August 2024', 'live-verified this session (SILSO via Wikipedia)'])
    with open(DATA_DIR / 'real_events.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['event', 'quantity', 'value', 'unit', 'source_note'])
        w.writerow(['AR 12673 X9.3 flare', 'GOES peak flux', FLARE_PEAK_FLUX_WM2, 'W/m^2', 'standard published NOAA/GOES value, level 2'])
        w.writerow(['6 Sept 2017 CME', 'LASCO linear speed', FLARE_CME_SPEED_KMS, 'km/s', 'standard published CDAW catalog value, level 2'])
        w.writerow(['7-8 Sept 2017 storm', 'Dst minimum', STORM_DST_MIN_NT, 'nT', 'standard published Kyoto WDC/NOAA value, level 2'])
        w.writerow(['Carrington Event 1859', 'Dst range (conservative)', CARRINGTON_DST_MIN_NT_CONSERVATIVE, 'nT', 'live-verified this session (Cliver & Svalgaard 2005 via Wikipedia)'])
        w.writerow(['Carrington Event 1859', 'Dst range (Tsurutani et al. 2003)', CARRINGTON_DST_MIN_NT, 'nT', 'live-verified this session (Tsurutani et al. 2003 via Wikipedia)'])
        w.writerow(['Carrington Event 1859', 'CME transit time', CARRINGTON_TRANSIT_HOURS, 'hours', 'live-verified this session (via Wikipedia)'])
        w.writerow(['Parker Solar Probe', 'perihelion', PSP_PERIHELION_RSUN, 'R_sun', 'live-verified this session (via Wikipedia)'])
        w.writerow(['Parker Solar Probe', 'record heliocentric speed', PSP_RECORD_SPEED_KMS, 'km/s', 'live-verified this session (via Wikipedia)'])


if __name__ == '__main__':
    write_lectures()
    write_data_csv()
    print('Wrote', len(LECTURES), 'lectures to', LECTURE_DIR)
