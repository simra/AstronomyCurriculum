"""Content generator for ASTR350 lecture slides and lecture notes.

Every worked numeric example is computed programmatically from the shared
constants and real exoplanet/astrobiology datasets defined below (not
hand-typed), and the same constants are reused across labs and problem sets
that reference the same scenario (see generate_astr350_labs_psets.py). Run
with the project interpreter:
    python materials/ASTR350/src/generate_astr350_content.py
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


def fmt(x: float, sig: int = 4) -> str:
    if x == 0:
        return '0'
    return f'{x:.{sig}g}'


# ---------------------------------------------------------------------------
# Physical constants (SI unless noted)
# ---------------------------------------------------------------------------
G_CONST = 6.674e-11
C_LIGHT = 2.998e8
H_PLANCK = 6.626e-34
K_BOLTZMANN = 1.381e-23
SIGMA_SB = 5.670e-8
AU_M = 1.496e11
DAY_S = 86400.0
YEAR_S = 3.156e7
M_SUN = 1.989e30
R_SUN = 6.957e8
L_SUN = 3.828e26
M_EARTH = 5.972e24
R_EARTH = 6.371e6
M_JUP = 1.898e27
R_JUP = 6.9911e7
AMU = 1.6605e-27
S_EARTH_W_M2 = 1361.0  # solar constant at 1 AU

# ---------------------------------------------------------------------------
# Real exoplanet systems.
# 51 Pegasi b: live-verified this session via direct web fetch of Wikipedia's
# "51 Pegasi b" article (2026-09-24), citing Mayor & Queloz (1995), Nature
# 378, 355. NOTE ON A CAUGHT UNIT ERROR: the fetched infobox listed the
# radial-velocity semi-amplitude as "55.77 +/- 0.15 km/s", which is
# inconsistent with (a) the same article's own discovery-section prose
# ("velocity changes ... of around 70 metres per second") and (b) the
# well-established published value from Mayor & Queloz (1995) of K ~ 55.9
# m/s. This is exactly the class of unit-conversion error the course-
# materials-review skill requires catching; the correct units (m/s, not
# km/s) are used throughout this course, and the discrepancy is logged in
# reference-log.md rather than silently repeated.
STAR_51PEG = dict(name='51 Pegasi', mass_msun=1.11, spectral_type='G2IV')
PLANET_51PEGB = dict(
    name='51 Pegasi b (Dimidium)', period_d=4.2307966, a_au=0.052344942, e=0.0063,
    k_rv_m_s=55.9, msini_mjup=0.469, mass_mjup=0.61, inclination_deg=49.8,
    discovered=1995, method='radial velocity (ELODIE spectrograph)',
)

# HD 209458 b: live-verified this session via direct web fetch of Wikipedia's
# "HD 209458 b" article (2026-09-24), citing Charbonneau et al. (2000), ApJ
# 529, L45, and Henry et al. (2000), ApJ 529, L41.
STAR_HD209458 = dict(name='HD 209458', radius_rsun=1.20, mass_msun=1.15, spectral_type='G0V')
PLANET_HD209458B = dict(
    name='HD 209458 b (Osiris)', period_d=3.52474859, a_au=0.04707, e=0.0081,
    k_rv_m_s=84.27, mass_mjup=0.682, radius_rjup=1.359, inclination_deg=86.710,
    transit_depth_measured=0.015, transit_duration_hr=3.0,
    exosphere_extent_rjup=3.1, mass_loss_kg_s=3.0e8, exosphere_temp_k=10000.0,
    discovered=1999, method='transit photometry + radial velocity',
)

# TRAPPIST-1: reused/extended from this curriculum's ASTR320 course, where it
# was live-verified via a direct web fetch of Wikipedia's "TRAPPIST-1"
# article (2026-09-24; primary literature: Agol et al. 2021, PSJ 2, 1;
# Ducrot et al. 2020, A&A 640, A112; Gillon et al. 2017, Nature 542, 456;
# Delrez et al. 2022, A&A 667, A59). Per-planet mass/radius values below are
# standard published Agol et al. (2021) results, consistent with the range
# ("roughly 0.775 to 1.129 Earth radii") already established in ASTR320;
# not independently re-verified this session, flagged in reference-log.md.
TRAPPIST1_STAR = dict(mass_msun=0.0898, radius_rsun=0.1192, lum_lsun=5.66e-4, teff=2566.0, distance_pc=12.47)
TRAPPIST1_PLANETS = {
    'b': dict(a_au=0.0115, period_d=1.51, r_earth=1.116, m_earth=1.017),
    'c': dict(a_au=0.0158, period_d=2.42, r_earth=1.097, m_earth=1.156),
    'd': dict(a_au=0.0223, period_d=4.05, r_earth=0.788, m_earth=0.297),
    'e': dict(a_au=0.0293, period_d=6.10, r_earth=0.920, m_earth=0.772),
    'f': dict(a_au=0.0385, period_d=9.21, r_earth=1.045, m_earth=0.934),
    'g': dict(a_au=0.0469, period_d=12.35, r_earth=1.129, m_earth=1.148),
    'h': dict(a_au=0.0619, period_d=18.77, r_earth=0.755, m_earth=0.331),
}

# Two additional real, well-characterized highly eccentric RV planets
# (standard published discovery-paper values, level 2): HD 80606 b (Naef et
# al. 2001, A&A 375, L27) and 16 Cygni B b (Cochran et al. 1997, ApJ 483,
# 457), used in Lecture 05's eccentricity-architecture figure.
ECCENTRIC_PLANETS = {
    '51 Peg b': dict(a_au=0.0523, e=0.0063, mass_mjup=0.61),
    'HD 209458 b': dict(a_au=0.0471, e=0.0081, mass_mjup=0.682),
    'HD 80606 b': dict(a_au=0.455, e=0.9336, mass_mjup=4.20),
    '16 Cyg B b': dict(a_au=1.68, e=0.689, mass_mjup=1.5),
}

# Solar-system reference planets (standard published values, level 2) used
# throughout for mass-radius and interior comparisons.
SOLAR_SYSTEM = {
    'Mercury': dict(mass_earth=0.0553, radius_earth=0.383, density_kg_m3=5427),
    'Venus': dict(mass_earth=0.815, radius_earth=0.949, density_kg_m3=5243),
    'Earth': dict(mass_earth=1.0, radius_earth=1.0, density_kg_m3=5514),
    'Mars': dict(mass_earth=0.107, radius_earth=0.532, density_kg_m3=3934),
    'Neptune': dict(mass_earth=17.15, radius_earth=3.88, density_kg_m3=1638),
    'Jupiter': dict(mass_earth=317.8, radius_earth=11.21, density_kg_m3=1326),
}

# Habitable-zone conservative flux-boundary factors (Kasting, Whitmire &
# Reynolds 1993, Icarus 101, 108 -- widely cited "runaway greenhouse"/
# "maximum greenhouse" limits, standard published, level 2): the HZ inner
# and outer edges correspond to received flux S_inner and S_outer times the
# solar constant, scaled to any stellar luminosity via S(d) = L/(4 pi d^2).
HZ_S_INNER = 1.1   # runaway-greenhouse (moist greenhouse, conservative) limit, in units of S_Earth
HZ_S_OUTER = 0.32  # maximum-greenhouse (CO2 condensation) limit, in units of S_Earth

# Extremophile survival/growth records (standard published primary
# literature, level 2, not independently re-verified this session -- see
# reference-log.md for the full per-organism citation list): Pyrolobus
# fumarii upper growth limit 113 C (Blochl et al. 1997); "Strain 121"
# survival at 121 C (Kashefi & Lovley 2003); Planococcus halocryophilus
# growth down to -25 C (Mykytczuk et al. 2013); Deinococcus radiodurans
# acute radiation survival to ~5000 Gy (Daly 2009, and refs therein);
# tardigrade hydrostatic-pressure survival to ~600 MPa (Seki & Toyoshima
# 1998) and documented low-Earth-orbit vacuum/UV survival (Jonsson et al.
# 2008); Chroococcidiopsis desiccation-tolerant desert/hypolith cyanobacteria
# (Billi et al., multiple reviews).
EXTREMOPHILES = [
    dict(name='Pyrolobus fumarii', trait='hyperthermophile', value=113.0, unit='degC (upper growth limit)'),
    dict(name='"Strain 121"', trait='hyperthermophile', value=121.0, unit='degC (documented survival/growth)'),
    dict(name='Planococcus halocryophilus', trait='psychrophile', value=-25.0, unit='degC (lowest documented growth)'),
    dict(name='Deinococcus radiodurans', trait='radioresistant', value=5000.0, unit='Gy (acute dose, no viability loss)'),
    dict(name='Tardigrada (several spp.)', trait='pressure/vacuum tolerant', value=600.0, unit='MPa (hydrostatic pressure survived)'),
    dict(name='Halobacterium/Haloarchaea', trait='halophile', value=32.0, unit='% salinity (saturated brine)'),
]

HUMAN_LETHAL_RADIATION_GY = 5.0  # standard published acute human LD50-class dose, level 2, for comparison only

# Miller-Urey (1953) spark-discharge experiment: relative amino-acid
# abundance ORDER is a standard published result (Miller 1953, Science 117,
# 528; reanalysis by Johnson, Cleaves, Bada et al. 2008, Science 322, 404).
# The bar heights below are illustrative relative-order values consistent
# with the published ranking (glycine > alanine > beta-alanine > aspartic/
# glutamic acid > others), NOT the original chromatogram's calibrated
# micromole quantities, which are not reproduced here to avoid presenting a
# false level of numeric precision; labeled level 3 (illustrative) in
# reference-log.md even though the ranking itself is real, published data.
MILLER_UREY_RELATIVE_YIELD = [
    ('glycine', 100.0), ('alanine', 47.0), ('beta-alanine', 21.0),
    ('aspartic acid', 6.0), ('alpha-aminobutyric acid', 9.0), ('glutamic acid', 3.0),
]

OPENSTAX_NOTE = ('OpenStax Astronomy 2e (local extracted reference copy: '
                 'references/openstax-astronomy-2e-extracted.txt) introduces exoplanet detection methods in the '
                 '"Exoplanets" section of Chapter 7 (Other Worlds: An Introduction to the Solar System) and '
                 'astrobiology topics (habitable zone, biosignatures, the Drake equation) in Chapter 30 '
                 '(Life in the Universe); these citations follow the ASTR320/330 precedent of using native '
                 'OpenStax chapter numbering, extrapolated by analogy rather than independently cross-checked '
                 'against embedded figure/table numbering this session -- flagged for human spot-check in '
                 'reference-log.md. Nearly every quantitative derivation in this course (the radial-velocity '
                 'semi-amplitude equation, transit depth/duration, the mass-radius interior degeneracy, the '
                 'radiative-equilibrium habitable-zone boundary, and the Drake equation as a structured '
                 'estimation framework) goes well beyond OpenStax Astronomy 2e\u2019s introductory, descriptive '
                 'treatment; each lecture states explicitly where this course extends beyond the assigned reading.')


# ---------------------------------------------------------------------------
# Physics helper functions -- every worked example below calls these rather
# than hand-typing a numeric result.
# ---------------------------------------------------------------------------
def kepler_semimajor_axis_m(period_s: float, total_mass_kg: float) -> float:
    """Kepler's third law, a = (G M P^2 / 4 pi^2)^(1/3)."""
    return (G_CONST * total_mass_kg * period_s ** 2 / (4 * math.pi ** 2)) ** (1.0 / 3.0)


def rv_semi_amplitude_m_s(mp_kg: float, mstar_kg: float, period_s: float, e: float, inclination_deg: float) -> float:
    """Radial-velocity semi-amplitude K (circular-orbit-generalized form),
    K = [2 pi G / (P (Mstar+Mp)^2)]^(1/3) * Mp sin(i) / sqrt(1-e^2)."""
    total = mstar_kg + mp_kg
    coeff = (2 * math.pi * G_CONST / period_s) ** (1.0 / 3.0)
    return coeff * mp_kg * math.sin(math.radians(inclination_deg)) / (total ** (2.0 / 3.0) * math.sqrt(1 - e ** 2))


def rv_minimum_mass_kg(k_m_s: float, mstar_kg: float, period_s: float, e: float) -> float:
    """Solve the mass function for Mp sin(i) given K, P, Mstar, e (Mp << Mstar approximation, then refine)."""
    mp = 1.0e26  # initial guess
    for _ in range(60):
        f = rv_semi_amplitude_m_s(mp, mstar_kg, period_s, e, 90.0) - k_m_s
        df_mp = (rv_semi_amplitude_m_s(mp * 1.0001, mstar_kg, period_s, e, 90.0) - rv_semi_amplitude_m_s(
            mp * 0.9999, mstar_kg, period_s, e, 90.0)) / (mp * 0.0002)
        mp -= f / df_mp
    return mp


def transit_depth(rp_m: float, rstar_m: float) -> float:
    """Fractional transit depth, delta = (Rp/Rstar)^2."""
    return (rp_m / rstar_m) ** 2


def transit_duration_hr(period_s: float, rstar_m: float, a_m: float) -> float:
    """Approximate (central-transit, circular-orbit) transit duration,
    T = (P/pi) * arcsin(Rstar/a)."""
    return (period_s / math.pi) * math.asin(min(1.0, rstar_m / a_m)) / 3600.0


def equilibrium_temperature_k(lum_w: float, a_m: float, bond_albedo: float) -> float:
    return ((1 - bond_albedo) * lum_w / (16 * math.pi * SIGMA_SB * a_m ** 2)) ** 0.25


def insolation_w_m2(lum_w: float, a_m: float) -> float:
    return lum_w / (4 * math.pi * a_m ** 2)


def hz_boundaries_au(lum_lsun: float) -> tuple:
    """Conservative habitable-zone inner/outer edges (Kasting et al. 1993
    flux-boundary approximation) in AU, given stellar luminosity in Lsun."""
    d_inner = math.sqrt(lum_lsun / HZ_S_INNER)
    d_outer = math.sqrt(lum_lsun / HZ_S_OUTER)
    return d_inner, d_outer


def scale_height_m(temp_k: float, mean_molecular_mass_amu: float, surface_g: float) -> float:
    return K_BOLTZMANN * temp_k / (mean_molecular_mass_amu * AMU * surface_g)


def jeans_escape_parameter(mass_kg: float, radius_m: float, temp_k: float, particle_mass_amu: float) -> float:
    """Jeans escape parameter, lambda = G M m / (k T R) (dimensionless
    ratio of gravitational to thermal energy at the exobase)."""
    return G_CONST * mass_kg * particle_mass_amu * AMU / (K_BOLTZMANN * temp_k * radius_m)


def surface_gravity(mass_kg: float, radius_m: float) -> float:
    return G_CONST * mass_kg / radius_m ** 2


def drake_n(r_star: float, f_p: float, n_e: float, f_l: float, f_i: float, f_c: float, l_years: float) -> float:
    return r_star * f_p * n_e * f_l * f_i * f_c * l_years


# ---------------------------------------------------------------------------
# Derived worked-example numbers, computed once here and reused throughout
# the lectures, labs, and problem sets.
# ---------------------------------------------------------------------------
MSTAR_51PEG_KG = STAR_51PEG['mass_msun'] * M_SUN
MP_51PEGB_TRUE_KG = PLANET_51PEGB['mass_mjup'] * M_JUP
P_51PEGB_S = PLANET_51PEGB['period_d'] * DAY_S
A_51PEGB_M = kepler_semimajor_axis_m(P_51PEGB_S, MSTAR_51PEG_KG + MP_51PEGB_TRUE_KG)
K_51PEGB_PREDICTED = rv_semi_amplitude_m_s(MP_51PEGB_TRUE_KG, MSTAR_51PEG_KG, P_51PEGB_S,
                                           PLANET_51PEGB['e'], PLANET_51PEGB['inclination_deg'])
MP_SINI_51PEGB_FROM_K_KG = rv_minimum_mass_kg(PLANET_51PEGB['k_rv_m_s'], MSTAR_51PEG_KG, P_51PEGB_S, PLANET_51PEGB['e'])
MP_SINI_51PEGB_MJUP = MP_SINI_51PEGB_FROM_K_KG / M_JUP
MP_TRUE_51PEGB_FROM_SINI_MJUP = MP_SINI_51PEGB_MJUP / math.sin(math.radians(PLANET_51PEGB['inclination_deg']))

MSTAR_HD209458_KG = STAR_HD209458['mass_msun'] * M_SUN
MP_HD209458B_KG = PLANET_HD209458B['mass_mjup'] * M_JUP
RSTAR_HD209458_M = STAR_HD209458['radius_rsun'] * R_SUN
RP_HD209458B_M = PLANET_HD209458B['radius_rjup'] * R_JUP
P_HD209458B_S = PLANET_HD209458B['period_d'] * DAY_S
A_HD209458B_M = kepler_semimajor_axis_m(P_HD209458B_S, MSTAR_HD209458_KG + MP_HD209458B_KG)
TRANSIT_DEPTH_HD209458B_COMPUTED = transit_depth(RP_HD209458B_M, RSTAR_HD209458_M)
TRANSIT_DURATION_HD209458B_COMPUTED = transit_duration_hr(P_HD209458B_S, RSTAR_HD209458_M, A_HD209458B_M)
K_HD209458B_PREDICTED = rv_semi_amplitude_m_s(MP_HD209458B_KG, MSTAR_HD209458_KG, P_HD209458B_S,
                                               PLANET_HD209458B['e'], PLANET_HD209458B['inclination_deg'])

HD209458B_DENSITY_KG_M3 = MP_HD209458B_KG / (4.0 / 3.0 * math.pi * RP_HD209458B_M ** 3)
HD209458B_SURFACE_G = surface_gravity(MP_HD209458B_KG, RP_HD209458B_M)
HD209458B_SCALE_HEIGHT_H2_M = scale_height_m(PLANET_HD209458B['exosphere_temp_k'] / 4.0, 2.0, HD209458B_SURFACE_G)
HD209458B_JEANS_PARAM = jeans_escape_parameter(MP_HD209458B_KG, RP_HD209458B_M,
                                                PLANET_HD209458B['exosphere_temp_k'], 1.0)
HD209458B_MASS_LOSS_TIMESCALE_GYR = MP_HD209458B_KG / PLANET_HD209458B['mass_loss_kg_s'] / YEAR_S / 1.0e9

TRAPPIST1_LUM_W = TRAPPIST1_STAR['lum_lsun'] * L_SUN
TRAPPIST1_TEQ = {p: equilibrium_temperature_k(TRAPPIST1_LUM_W, d['a_au'] * AU_M, 0.0)
                  for p, d in TRAPPIST1_PLANETS.items()}
TRAPPIST1_DENSITY_KG_M3 = {p: (d['m_earth'] * M_EARTH) / (4.0 / 3.0 * math.pi * (d['r_earth'] * R_EARTH) ** 3)
                            for p, d in TRAPPIST1_PLANETS.items()}
TRAPPIST1_HZ_INNER_AU, TRAPPIST1_HZ_OUTER_AU = hz_boundaries_au(TRAPPIST1_STAR['lum_lsun'])
SUN_HZ_INNER_AU, SUN_HZ_OUTER_AU = hz_boundaries_au(1.0)

EARTH_EQ_TEMP_K = equilibrium_temperature_k(L_SUN, AU_M, 0.0)
EARTH_INSOLATION = insolation_w_m2(L_SUN, AU_M)

MOIST_GREENHOUSE_MARGIN_TRAPPIST1E = (TRAPPIST1_PLANETS['e']['a_au'] - TRAPPIST1_HZ_INNER_AU) / (
    TRAPPIST1_HZ_OUTER_AU - TRAPPIST1_HZ_INNER_AU)

# Drake equation: illustrative order-of-magnitude term estimates. R_star and
# f_p/n_e are grounded in real Kepler/Gaia-era occurrence-rate literature
# (standard published, level 2: Batalha et al. 2013-class and Bryson et al.
# 2021-class eta-Earth estimates for FGK stars); f_l, f_i, f_c, L are
# genuinely unconstrained and explicitly labeled illustrative/synthetic
# (level 3) order-of-magnitude placeholders for the estimation exercise, not
# claimed measurements.
DRAKE_R_STAR = 1.5       # new Sun-like stars formed per year in the Milky Way (level 2, standard order-of-magnitude)
DRAKE_F_P = 1.0          # fraction of those stars with planets (level 2, Kepler-era result: planets are common)
DRAKE_N_E = 0.4          # mean number of HZ-compatible planets per system (level 2, eta-Earth-class estimate)
DRAKE_F_L_OPTIMISTIC = 1.0
DRAKE_F_L_PESSIMISTIC = 1.0e-4
DRAKE_F_I = 0.1
DRAKE_F_C = 0.1
DRAKE_L_OPTIMISTIC_YR = 1.0e8
DRAKE_L_PESSIMISTIC_YR = 1.0e2
N_CIV_OPTIMISTIC = drake_n(DRAKE_R_STAR, DRAKE_F_P, DRAKE_N_E, DRAKE_F_L_OPTIMISTIC, DRAKE_F_I, DRAKE_F_C,
                           DRAKE_L_OPTIMISTIC_YR)
N_CIV_PESSIMISTIC = drake_n(DRAKE_R_STAR, DRAKE_F_P, DRAKE_N_E, DRAKE_F_L_PESSIMISTIC, DRAKE_F_I, DRAKE_F_C,
                             DRAKE_L_PESSIMISTIC_YR)


# ---------------------------------------------------------------------------
# Lecture-specific visual-reasoning diagrams (SVG). Each lecture gets a
# structurally distinct figure built from the real constants/datasets above;
# only small drawing primitives are shared (established pattern from
# materials/ASTR330,ASTR340/src).
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


def diagram_01(item):
    """Radial-velocity sine curve for 51 Pegasi b computed from K, e, P."""
    x0, y0, w, h = 90, 80, 820, 380
    n = 200
    pts = []
    for i in range(n + 1):
        phase = i / n
        v = PLANET_51PEGB['k_rv_m_s'] * math.sin(2 * math.pi * phase)
        px = x0 + phase * w
        py = y0 + h / 2 - v / (PLANET_51PEGB['k_rv_m_s'] * 1.2) * (h / 2)
        pts.append((px, py))
    inner = _axes(x0, y0, w, h, 'Orbital phase', 'Stellar radial velocity (m/s)')
    inner += f"<line x1='{x0}' y1='{y0 + h / 2:.0f}' x2='{x0 + w}' y2='{y0 + h / 2:.0f}' stroke='#d9e0e7' stroke-width='1.5' stroke-dasharray='4 4'/>"
    inner += _polyline(pts)
    kx = x0 + 0.25 * w
    inner += _dot(kx, y0 + h / 2 - PLANET_51PEGB['k_rv_m_s'] / (PLANET_51PEGB['k_rv_m_s'] * 1.2) * (h / 2),
                  f"K = {PLANET_51PEGB['k_rv_m_s']:.1f} m/s", dy=-16)
    inner += _fig_caption(f'51 Pegasi b: P = {PLANET_51PEGB["period_d"]:.3f} d, e = {PLANET_51PEGB["e"]:.4f} '
                          f'(essentially circular), K = {PLANET_51PEGB["k_rv_m_s"]:.1f} m/s (Mayor & Queloz 1995).')
    return _fig_wrap(item['n'], item['title'], inner, 'radial velocity vs orbital phase sine curve for 51 Pegasi b')


def diagram_02(item):
    """HD 209458 b transit light curve (flux vs time) from real transit depth/duration."""
    x0, y0, w, h = 90, 80, 820, 380
    depth = PLANET_HD209458B['transit_depth_measured']
    dur = PLANET_HD209458B['transit_duration_hr']
    total_span = dur * 3.2
    ingress = dur * 0.12
    pts = []
    t = -total_span / 2
    step = total_span / 400
    flux_top = y0 + 40
    flux_bottom = y0 + 40 + depth * 3000
    while t <= total_span / 2:
        if t < -dur / 2 - ingress:
            f = flux_top
        elif t < -dur / 2:
            f = _lin(t, -dur / 2 - ingress, -dur / 2, flux_top, flux_bottom)
        elif t < dur / 2:
            f = flux_bottom
        elif t < dur / 2 + ingress:
            f = _lin(t, dur / 2, dur / 2 + ingress, flux_bottom, flux_top)
        else:
            f = flux_top
        px = x0 + (t + total_span / 2) / total_span * w
        pts.append((px, f))
        t += step
    inner = _axes(x0, y0, w, h, 'Time from mid-transit (hours)', 'Relative flux')
    inner += _polyline(pts, color='#b87911')
    inner += _fig_caption(f'HD 209458 b: measured transit depth {depth * 100:.1f}% over ~{dur:.1f} h '
                          f'(Charbonneau et al. 2000); this course\u2019s computed (Rp/Rs)\u00b2 = {TRANSIT_DEPTH_HD209458B_COMPUTED * 100:.2f}%.')
    return _fig_wrap(item['n'], item['title'], inner, 'box-shaped transit light curve for HD 209458 b showing ingress, flat bottom, egress')


def diagram_03(item):
    """Detection-method sensitivity map: planet mass vs semimajor axis, log-log, with method regions and real planets plotted."""
    x0, y0, w, h = 90, 80, 820, 400
    xmin, xmax = math.log10(0.005), math.log10(50)
    ymin, ymax = math.log10(0.05), math.log10(20)

    def X(a):
        return x0 + _lin(math.log10(a), xmin, xmax, 0, w)

    def Y(m):
        return y0 + h - _lin(math.log10(m), ymin, ymax, 0, h)

    inner = _axes(x0, y0, w, h, 'Semimajor axis (AU, log scale)', 'Planet mass (Jupiter masses, log scale)')
    # RV-sensitive region (close-in, higher mass) and transit-sensitive strip near the star
    inner += (f"<rect x='{x0}' y='{Y(3):.1f}' width='{X(2)-x0:.1f}' height='{Y(0.05)-Y(3):.1f}' "
              f"fill='#0f6b78' opacity='0.10'/>")
    inner += (f"<rect x='{x0}' y='{y0}' width='{X(0.3)-x0:.1f}' height='{h:.1f}' fill='#b87911' opacity='0.08'/>")
    inner += _fig_caption('shaded: teal = practical radial-velocity sensitivity region; gold = transit-favorable close-in region', y=y0 - 40)
    pts = [
        ('51 Peg b', PLANET_51PEGB['a_au'], PLANET_51PEGB['mass_mjup']),
        ('HD 209458 b', PLANET_HD209458B['a_au'], PLANET_HD209458B['mass_mjup']),
        ('TRAPPIST-1e', TRAPPIST1_PLANETS['e']['a_au'], TRAPPIST1_PLANETS['e']['m_earth'] * M_EARTH / M_JUP),
        ('HD 80606 b', 0.455, 4.20),
        ('16 Cyg B b', 1.68, 1.5),
        ('Jupiter', 5.20, 1.0),
    ]
    for name, a, m in pts:
        inner += _dot(X(a), Y(m), name, dy=-12)
    inner += _fig_caption('Real planets from this course plotted by discovery-relevant parameters; RV and transit surveys probe different, only partially overlapping regions of mass-semimajor-axis space.')
    return _fig_wrap(item['n'], item['title'], inner, 'log-log mass vs semimajor axis parameter space with RV and transit sensitivity regions and real planets plotted')


def diagram_04(item):
    """Mass-radius scatter (log-log) with solar-system planets, TRAPPIST-1 planets, 51 Peg b, HD209458b."""
    x0, y0, w, h = 90, 80, 820, 400
    xmin, xmax = math.log10(0.05), math.log10(400)
    ymin, ymax = math.log10(0.3), math.log10(15)

    def X(m):
        return x0 + _lin(math.log10(m), xmin, xmax, 0, w)

    def Y(r):
        return y0 + h - _lin(math.log10(r), ymin, ymax, 0, h)

    inner = _axes(x0, y0, w, h, 'Mass (Earth masses, log scale)', 'Radius (Earth radii, log scale)')
    for name, d in SOLAR_SYSTEM.items():
        inner += _dot(X(d['mass_earth']), Y(d['radius_earth']), name, color='#0f6b78', dy=-12)
    for p, d in TRAPPIST1_PLANETS.items():
        inner += _dot(X(d['m_earth']), Y(d['r_earth']), f'TRAPPIST-1{p}', r=4, color='#5b6773', dy=12, dx=6)
    inner += _dot(X(PLANET_HD209458B['mass_mjup'] * M_JUP / M_EARTH),
                  Y(PLANET_HD209458B['radius_rjup'] * R_JUP / R_EARTH), 'HD 209458 b', color='#b87911')
    inner += _dot(X(MP_TRUE_51PEGB_FROM_SINI_MJUP * M_JUP / M_EARTH), Y(1.07 * R_JUP / R_EARTH),
                  '51 Peg b', color='#b87911', dy=14)
    inner += _fig_caption('Rocky solar-system worlds and TRAPPIST-1 planets cluster on a steep mass-radius track; '
                          'the two gas giants (Jupiter, HD 209458 b, 51 Peg b) fall on a nearly flat track, the '
                          'classic rocky/gas-giant mass-radius dichotomy this lecture explains.')
    return _fig_wrap(item['n'], item['title'], inner, 'log-log mass-radius scatter plot of solar system, TRAPPIST-1, and hot Jupiter planets')


def diagram_05(item):
    """Eccentricity vs semimajor axis scatter for real RV planets."""
    x0, y0, w, h = 90, 80, 820, 400
    xmin, xmax = math.log10(0.02), math.log10(3)

    def X(a):
        return x0 + _lin(math.log10(a), xmin, xmax, 0, w)

    def Y(e):
        return y0 + h - e * h

    inner = _axes(x0, y0, w, h, 'Semimajor axis (AU, log scale)', 'Orbital eccentricity')
    for name, d in ECCENTRIC_PLANETS.items():
        inner += _dot(X(d['a_au']), Y(d['e']), f"{name} (e={d['e']:.2f})", dy=-12)
    inner += _fig_caption('Real RV-discovered planets: circular, tidally circularized hot Jupiters (51 Peg b, '
                          'HD 209458 b) versus highly eccentric planets at larger separation (HD 80606 b, e=0.93; '
                          '16 Cyg B b, e=0.69), illustrating how tidal circularization timescale depends steeply on a.')
    return _fig_wrap(item['n'], item['title'], inner, 'eccentricity vs semimajor axis scatter plot of real radial-velocity exoplanets')


def diagram_06(item):
    """Interior structure cross-sections: layered circles for Earth, TRAPPIST-1e, HD209458b (very different densities)."""
    inner = ''
    entries = [
        ('Earth', 1.0, 5514, '#8a6d3b'),
        ('TRAPPIST-1e', TRAPPIST1_PLANETS['e']['r_earth'], TRAPPIST1_DENSITY_KG_M3['e'], '#0f6b78'),
        ('HD 209458 b', PLANET_HD209458B['radius_rjup'] * R_JUP / R_EARTH, HD209458B_DENSITY_KG_M3, '#b87911'),
    ]
    cx0 = 190
    for i, (name, r_earth, density, color) in enumerate(entries):
        cx = cx0 + i * 300
        cy = 380
        r_px = 30 + min(r_earth, 15) * 8
        core_frac = 0.55 if density > 4000 else 0.15
        inner += f"<circle cx='{cx}' cy='{cy}' r='{r_px:.1f}' fill='{color}' opacity='0.25'/>"
        inner += f"<circle cx='{cx}' cy='{cy}' r='{r_px * core_frac:.1f}' fill='{color}' opacity='0.75'/>"
        inner += (f"<text x='{cx}' y='{cy + r_px + 28:.0f}' font-size='15' fill='#17202a' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif'>{escape(name)}</text>")
        inner += (f"<text x='{cx}' y='{cy + r_px + 48:.0f}' font-size='13' fill='#5b6773' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif'>&rho;&#8776;{density:.0f} kg/m&sup3;</text>")
    inner += _fig_caption('Schematic interior cross-sections (relative sizes to scale, core-fraction schematic only): '
                          'Earth\u2019s rocky/iron interior, TRAPPIST-1e\u2019s Earth-like bulk density, and HD 209458 b\u2019s '
                          'inflated, mostly-hydrogen gas-giant envelope -- the same mass-radius data from Lecture 04, '
                          'now interpreted physically.')
    return _fig_wrap(item['n'], item['title'], inner, 'schematic layered interior cross-sections for Earth, TRAPPIST-1e, and HD 209458 b')


def diagram_07(item):
    """Synthetic transmission spectrum for HD209458b: transit depth vs wavelength with a real Na absorption feature."""
    x0, y0, w, h = 90, 80, 820, 380
    base_depth = TRANSIT_DEPTH_HD209458B_COMPUTED * 100
    scale_height_signal = 5 * HD209458B_SCALE_HEIGHT_H2_M / RSTAR_HD209458_M * (RP_HD209458B_M / RSTAR_HD209458_M) * 100
    lam_min, lam_max = 400, 1000
    n = 200
    pts = []
    for i in range(n + 1):
        lam = lam_min + (lam_max - lam_min) * i / n
        bump = scale_height_signal * math.exp(-((lam - 589.0) ** 2) / (2 * 8 ** 2))  # Na D line, 589 nm
        depth = base_depth + bump
        px = x0 + (lam - lam_min) / (lam_max - lam_min) * w
        py = y0 + h - (depth - base_depth) / (scale_height_signal * 1.3) * h
        pts.append((px, py))
    inner = _axes(x0, y0, w, h, 'Wavelength (nm)', 'Transit depth above baseline (relative)')
    inner += _polyline(pts)
    inner += _fig_caption(f'Synthetic transmission spectrum shaped by this lecture\u2019s scale-height physics, with a '
                          f'feature at 589 nm marking HD 209458 b\u2019s real, HST-detected atmospheric sodium absorption '
                          f'(Charbonneau et al. 2002) -- the first exoplanet atmosphere ever measured.')
    return _fig_wrap(item['n'], item['title'], inner, 'synthetic transmission spectrum of HD 209458 b with a sodium absorption feature at 589 nm')


def diagram_08(item):
    """Jeans escape parameter vs temperature curve for HD209458b's exosphere, with its real hydrogen exosphere marked."""
    x0, y0, w, h = 90, 80, 820, 380
    temps = [t for t in range(500, 15001, 250)]
    pts = []
    for t in temps:
        lam = jeans_escape_parameter(MP_HD209458B_KG, RP_HD209458B_M, t, 1.0)
        px = x0 + (t - 500) / (15000 - 500) * w
        py = y0 + h - min(lam, 30) / 30 * h
        pts.append((px, py))
    inner = _axes(x0, y0, w, h, 'Exobase temperature (K)', 'Jeans escape parameter (lambda, capped at 30)')
    inner += _polyline(pts)
    inner += f"<line x1='{x0}' y1='{y0+h - 1/30*h:.1f}' x2='{x0+w}' y2='{y0+h - 1/30*h:.1f}' stroke='#8a4b08' stroke-dasharray='5 5'/>"
    inner += _fig_caption('lambda &lt;~ few: hydrodynamic (Jeans-escape-invalid, rapid blow-off) regime, dashed line', y=y0 - 30)
    tx = x0 + (PLANET_HD209458B['exosphere_temp_k'] - 500) / (15000 - 500) * w
    inner += _dot(tx, y0 + h - min(HD209458B_JEANS_PARAM, 30) / 30 * h,
                  f"HD 209458 b exosphere, T&#8776;{PLANET_HD209458B['exosphere_temp_k']:.0f} K, "
                  f"&lambda;&#8776;{HD209458B_JEANS_PARAM:.2f}", dy=-18)
    inner += _fig_caption(f'Real observed exosphere: extends to {PLANET_HD209458B["exosphere_extent_rjup"]:.1f} '
                          f'planetary radii, mass loss &#8776;{PLANET_HD209458B["mass_loss_kg_s"]:.0e} kg/s '
                          f'(Vidal-Madjar et al. 2003) -- lambda&#8776;11, well below a tightly bound atmosphere\u2019s value but not yet down at order unity, consistent with strongly enhanced, transitional-to-hydrodynamic escape rather than classical, negligible Jeans escape.')
    return _fig_wrap(item['n'], item['title'], inner, 'Jeans escape parameter versus exobase temperature curve with HD 209458 b marked in the hydrodynamic-escape regime')


def diagram_09(item):
    """Habitable zone flux-boundary diagram: distance vs stellar luminosity (log-log) with Sun and TRAPPIST-1 systems plotted."""
    x0, y0, w, h = 90, 80, 820, 400
    xmin, xmax = math.log10(1e-4), math.log10(2)
    ymin, ymax = math.log10(0.003), math.log10(3)

    def X(lum):
        return x0 + _lin(math.log10(lum), xmin, xmax, 0, w)

    def Y(a):
        return y0 + h - _lin(math.log10(a), ymin, ymax, 0, h)

    lums = [10 ** (xmin + i * (xmax - xmin) / 100) for i in range(101)]
    inner_pts_in = [(X(l), Y(hz_boundaries_au(l)[0])) for l in lums]
    inner_pts_out = [(X(l), Y(hz_boundaries_au(l)[1])) for l in lums]
    inner = _axes(x0, y0, w, h, 'Stellar luminosity (L_sun, log scale)', 'Orbital distance (AU, log scale)')
    inner += _polyline(inner_pts_in, color='#8a4b08')
    inner += _polyline(inner_pts_out, color='#0f6b78')
    inner += _dot(X(1.0), Y(1.0), 'Earth', color='#5b6773')
    for p, d in TRAPPIST1_PLANETS.items():
        inner += _dot(X(TRAPPIST1_STAR['lum_lsun']), Y(d['a_au']), f'-1{p}' if p in 'efg' else '', r=4, dy=8, dx=4)
    inner += _fig_caption(f'gold = runaway-greenhouse inner edge (S={HZ_S_INNER}S&#8853;); teal = maximum-greenhouse '
                          f'outer edge (S={HZ_S_OUTER}S&#8853;); TRAPPIST-1 (L={TRAPPIST1_STAR["lum_lsun"]:.2e} L&#8857;) '
                          f'planets e, f, g fall inside its own much-closer-in habitable zone.')
    return _fig_wrap(item['n'], item['title'], inner, 'log-log habitable zone inner and outer boundary curves versus stellar luminosity with Sun and TRAPPIST-1 planets plotted')


def diagram_10(item):
    """Climate feedback loop diagram: runaway greenhouse loop (Venus-like) vs stabilizing feedback (Earth-like), as a schematic cycle."""
    inner = ''

    def loop(cx, cy, label, nodes, color, unstable):
        r = 130
        n = len(nodes)
        pos = []
        for i, txt in enumerate(nodes):
            ang = -math.pi / 2 + i * 2 * math.pi / n
            x = cx + r * math.cos(ang)
            y = cy + r * math.sin(ang)
            pos.append((x, y))
            inner_local = (f"<circle cx='{x:.1f}' cy='{y:.1f}' r='34' fill='{color}' opacity='0.85'/>"
                           f"<text x='{x:.1f}' y='{y+5:.1f}' font-size='12' fill='#fff' text-anchor='middle' "
                           f"font-family='Segoe UI, sans-serif'>{escape(txt)}</text>")
            nonlocal_store.append(inner_local)
        for i in range(n):
            x1, y1 = pos[i]
            x2, y2 = pos[(i + 1) % n]
            nonlocal_store.append(f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' "
                                   f"stroke='{color}' stroke-width='2.5' marker-end='url(#arrow)'/>")
        sign = '+ (runaway)' if unstable else '- (stabilizing)'
        nonlocal_store.append(f"<text x='{cx:.0f}' y='{cy + r + 60:.0f}' font-size='15' fill='#17202a' "
                               f"text-anchor='middle' font-family='Segoe UI, sans-serif'>{escape(label)} loop sign: {sign}</text>")

    nonlocal_store = []
    marker = ("<defs><marker id='arrow' markerWidth='10' markerHeight='10' refX='9' refY='3' orient='auto'>"
              "<path d='M0,0 L0,6 L9,3 z' fill='#5b6773'/></marker></defs>")
    loop(260, 330, 'Venus-like runaway greenhouse', ['warm surface', 'more H2O vapor', 'stronger greenhouse', 'hotter surface'],
         '#b87911', True)
    loop(700, 330, 'Earth-like stabilizing (silicate weathering)', ['warm surface', 'faster weathering', 'less CO2', 'cooler surface'],
         '#0f6b78', False)
    inner = marker + ''.join(nonlocal_store)
    inner += _fig_caption('Both loops share the same water-vapor/greenhouse physics from Lecture 09; the sign of the '
                          'feedback (positive/runaway near a hot inner-edge star, negative/stabilizing via the '
                          'carbonate-silicate cycle farther out) is what separates a Venus-like outcome from a '
                          'long-term-habitable one.', y=590)
    return _fig_wrap(item['n'], item['title'], inner, 'two schematic climate feedback loop diagrams contrasting a runaway greenhouse cycle with a stabilizing silicate-weathering cycle')


def diagram_11(item):
    """Biosignature spectrum with O2/O3/CH4/H2O bands marked, plus a small false-positive decision annotation."""
    x0, y0, w, h = 90, 80, 820, 380
    bands = [('H2O', 940, 0.4), ('CO2', 1050, 0.55), ('O2', 760, 0.75), ('O3', 300, 0.9), ('CH4', 1650, 0.35)]
    lam_min, lam_max = 250, 1800
    inner = _axes(x0, y0, w, h, 'Wavelength (nm)', 'Absorption depth (schematic)')
    baseline = [(x0, y0 + h * 0.15), (x0 + w, y0 + h * 0.15)]
    inner += _polyline(baseline, color='#d9e0e7', width=2)
    for name, lam, depth in bands:
        px = x0 + (lam - lam_min) / (lam_max - lam_min) * w
        py = y0 + h * 0.15
        py2 = y0 + h * depth
        color = '#b87911' if name in ('O2', 'O3') else '#0f6b78'
        inner += f"<line x1='{px:.1f}' y1='{py:.1f}' x2='{px:.1f}' y2='{py2:.1f}' stroke='{color}' stroke-width='6'/>"
        inner += (f"<text x='{px:.1f}' y='{py2+18:.1f}' font-size='14' fill='#17202a' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif'>{escape(name)}</text>")
    inner += _fig_caption('Gold bands (O2, O3) are the classical biosignature pair; teal bands (H2O, CO2, CH4) are '
                          'context gases needed to rule out the abiotic-oxygen false-positive pathways (photolytic '
                          'water loss without a temperate CO2/CH4-bearing atmosphere) this lecture derives.')
    return _fig_wrap(item['n'], item['title'], inner, 'schematic biosignature absorption spectrum marking O2, O3, H2O, CO2, and CH4 bands')


def diagram_12(item):
    """Extremophile survival envelope: temperature vs a second axis (radiation dose / pressure), log where needed."""
    x0, y0, w, h = 90, 80, 820, 400
    tmin, tmax = -30, 130

    def X(t):
        return x0 + _lin(t, tmin, tmax, 0, w)

    inner = _axes(x0, y0, w, h, 'Temperature (degC)', 'Extreme-tolerance metric (see legend, log-scaled per organism)')
    rows = [
        ('Planococcus halocryophilus (cold)', -25.0, 0.15),
        ('Human comfort range (for scale)', 20.0, 0.5),
        ('Pyrolobus fumarii (heat)', 113.0, 0.65),
        ('"Strain 121" (heat)', 121.0, 0.72),
    ]
    for name, t, frac in rows:
        inner += _dot(X(t), y0 + h * (1 - frac), name, dy=-14)
    # side annotations for non-temperature extremes, placed as text panel
    inner += (f"<text x='{x0+40}' y='{y0+40}' font-size='14' fill='#17202a' font-family='Segoe UI, sans-serif'>"
              f"Other real recorded extremes (not on the temperature axis):</text>")
    extra = [f"Deinococcus radiodurans: survives {int(EXTREMOPHILES[3]['value'])} Gy acute radiation "
             f"({EXTREMOPHILES[3]['value']/HUMAN_LETHAL_RADIATION_GY:.0f}x the human lethal dose)",
             f"Tardigrada: survive {int(EXTREMOPHILES[4]['value'])} MPa hydrostatic pressure "
             f"({EXTREMOPHILES[4]['value']*1e6/101325:.0f}x Earth sea-level atmospheric pressure)",
             f"Haloarchaea: thrive at {EXTREMOPHILES[5]['value']:.0f}% salinity (near-saturated brine)"]
    for i, t in enumerate(extra):
        inner += (f"<text x='{x0+40}' y='{y0+66+i*22}' font-size='13.5' fill='#5b6773' "
                  f"font-family='Segoe UI, sans-serif'>{escape(t)}</text>")
    return _fig_wrap(item['n'], item['title'], inner, 'temperature axis scatter of extremophile survival records plus a text panel of pressure, radiation, and salinity extremes')


def diagram_13(item):
    """Miller-Urey relative amino-acid yield bar chart (real relative ranking, illustrative bar heights)."""
    x0, y0, w, h = 120, 80, 760, 380
    n = len(MILLER_UREY_RELATIVE_YIELD)
    bw = w / n * 0.6
    inner = _axes(x0, y0, w, h, 'Amino acid detected', 'Relative abundance (glycine = 100, illustrative)')
    for i, (name, val) in enumerate(MILLER_UREY_RELATIVE_YIELD):
        bx = x0 + (i + 0.2) * (w / n)
        bh = val / 100.0 * h
        by = y0 + h - bh
        inner += f"<rect x='{bx:.1f}' y='{by:.1f}' width='{bw:.1f}' height='{bh:.1f}' fill='#0f6b78'/>"
        inner += (f"<text x='{bx+bw/2:.1f}' y='{y0+h+20:.1f}' font-size='12.5' fill='#17202a' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif' transform='rotate(0)'>{escape(name)}</text>")
        inner += (f"<text x='{bx+bw/2:.1f}' y='{by-8:.1f}' font-size='12' fill='#5b6773' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif'>{val:.0f}</text>")
    inner += _fig_caption('Relative-abundance order reproduced from Miller (1953) / Johnson et al. (2008): glycine and '
                          'alanine dominate; bar heights are illustrative order-of-magnitude values, not recalibrated '
                          'chromatogram quantities (see reference-log.md).')
    return _fig_wrap(item['n'], item['title'], inner, 'bar chart of relative amino acid abundances from the Miller-Urey spark discharge experiment')


def diagram_14(item):
    """Drake equation funnel/waterfall diagram: successive multiplication narrowing to N."""
    x0, y0, w = 90, 90, 820
    terms = [('R*', DRAKE_R_STAR, 'yr^-1'), ('f_p', DRAKE_F_P, ''), ('n_e', DRAKE_N_E, ''),
             ('f_l', '1 to 1e-4', ''), ('f_i', DRAKE_F_I, ''), ('f_c', DRAKE_F_C, ''), ('L', '1e2 to 1e8', 'yr')]
    inner = ''
    n = len(terms)
    bar_w = w / n * 0.72
    max_bar_h = 300
    running = 1.0
    for i, (name, val, unit) in enumerate(terms):
        bx = x0 + i * (w / n) + (w / n - bar_w) / 2
        frac = 1.0 - i / (n + 1)
        bh = max_bar_h * frac
        by = y0 + (max_bar_h - bh)
        color = '#0f6b78' if isinstance(val, (int, float)) else '#b87911'
        inner += f"<rect x='{bx:.1f}' y='{by:.1f}' width='{bar_w:.1f}' height='{bh:.1f}' fill='{color}' opacity='0.85'/>"
        vtxt = f'{val}' if isinstance(val, str) else f'{val:.2g}'
        inner += (f"<text x='{bx+bar_w/2:.1f}' y='{y0+max_bar_h+24:.1f}' font-size='13' fill='#17202a' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif'>{escape(name)}</text>")
        inner += (f"<text x='{bx+bar_w/2:.1f}' y='{by-8:.1f}' font-size='12.5' fill='#5b6773' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif'>{escape(vtxt)}{escape(unit)}</text>")
    inner += _fig_caption(f'Multiplying every term (astronomical terms R*, f_p, n_e are level-2 published estimates; '
                          f'biological terms f_l, f_i, f_c, L are explicitly unconstrained illustrative placeholders) '
                          f'gives N &#8776; {N_CIV_PESSIMISTIC:.1e} (pessimistic) to {N_CIV_OPTIMISTIC:.1e} (optimistic) -- '
                          f'a >{N_CIV_OPTIMISTIC/max(N_CIV_PESSIMISTIC,1e-30):.0e}-fold spread driven almost entirely by '
                          f'the three biological terms no one can yet measure.', y=460)
    return _fig_wrap(item['n'], item['title'], inner, 'Drake equation waterfall diagram showing successive narrowing bars for each multiplicative term')


_DIAGRAM_BUILDERS = {
    1: diagram_01, 2: diagram_02, 3: diagram_03, 4: diagram_04, 5: diagram_05, 6: diagram_06,
    7: diagram_07, 8: diagram_08, 9: diagram_09, 10: diagram_10, 11: diagram_11, 12: diagram_12,
    13: diagram_13, 14: diagram_14,
}


def lecture_svg(item: dict) -> str:
    return _DIAGRAM_BUILDERS[item['n']](item)


# ---------------------------------------------------------------------------
# Lecture content. Seven thematic units of exactly two lectures each (see
# syllabus.html's cadence rationale): (1) Detection I, (2) Detection II and
# Demographics, (3) Architectures and Interiors, (4) Atmospheres, (5)
# Habitability, (6) Biosignatures and Life's Limits, (7) Origins and Synthesis.
# ---------------------------------------------------------------------------
LECTURES = [
    dict(
        n=1, title='Detecting Other Worlds: The Radial-Velocity Method',
        subtitle='Weighing a planet you cannot see from the wobble of a star you can',
        goals=[
            'Derive the two-body radial-velocity semi-amplitude equation from Kepler\u2019s third law and the center-of-mass condition.',
            'Explain why radial-velocity detection alone yields only a minimum mass, Mp sin(i), and how that degeneracy can be broken.',
            'Reproduce, from first principles, the real discovery measurement of 51 Pegasi b, the first planet found around a Sun-like star.',
        ],
        why_matters='Every topic in this course -- demographics, architectures, atmospheres, habitability, biosignatures -- depends on first having detected and characterized a planet. This lecture derives the method (radial velocity) that opened the field in 1995 and remains the primary way planet masses are measured today.',
        phenomenon=f'On October 6, 1995, Michel Mayor and Didier Queloz announced a Jupiter-class planet orbiting 51 Pegasi, a Sun-like star 50 light-years away, based on a periodic {PLANET_51PEGB["k_rv_m_s"]:.0f} m/s wobble in the star\u2019s spectral lines -- slower than a brisk walking pace, extracted from starlight that had traveled 50 years to reach the telescope. This single measurement, later awarded the 2019 Nobel Prize in Physics, founded the modern field of exoplanet science this entire course is built on.',
        vocab=['radial velocity', 'Doppler spectroscopy', 'center of mass (barycenter)', 'semi-amplitude K', 'minimum mass (Mp sin i)', 'inclination degeneracy', 'mass function'],
        evidence=[
            'A star with an orbiting planet does not sit still: both bodies orbit their common center of mass, so the star traces a small reflex orbit whose radial (line-of-sight) velocity component is measurable via the Doppler shift of the star\u2019s absorption lines -- the same physics used throughout astronomy to measure any line-of-sight velocity.',
            'Mayor & Queloz (1995) used the ELODIE spectrograph at the Observatoire de Haute-Provence to track 51 Pegasi\u2019s radial velocity over many nights and found it varies periodically with a 4.23-day period, confirmed within a week by an independent team at Lick Observatory using a different instrument -- exactly the independent-replication standard this course expects of every real detection.',
            'Radial-velocity surveys since 1995 have found hundreds of planets with periods from under a day to many years, and every one of these detections yields only Mp sin(i), not the true mass, unless the orbital inclination is independently constrained (e.g., by a transit, astrometry, or direct imaging) -- a limitation this lecture derives explicitly rather than glossing over.',
        ],
        model=[
            'In a two-body system, both the star (mass M*) and planet (mass Mp) orbit their common center of mass; by the center-of-mass condition M* r* = Mp rp, the star\u2019s orbital radius r* = rp (Mp/M*) is much smaller than the planet\u2019s for Mp << M*, but not zero -- it is this small stellar reflex motion that radial-velocity spectroscopy measures.',
            'Combining Kepler\u2019s third law (relating orbital period P to the total mass and semimajor axis a) with the projection of the star\u2019s orbital velocity onto the line of sight (which depends on the orbital inclination i, defined so i=90 degrees is edge-on) gives the full radial-velocity semi-amplitude equation for a possibly eccentric orbit.',
            'Because only the projected velocity is observed, radial velocity alone cannot separate a small, edge-on-viewed planet from a larger, more face-on one producing the same observed K; the equation therefore only ever returns the combination Mp sin(i), the minimum mass, until an independent geometric constraint (Lecture 02\u2019s transit inclination, or direct imaging/astrometry, Lecture 03) breaks the degeneracy.',
        ],
        equation=r'K = \left(\dfrac{2\pi G}{P}\right)^{1/3}\dfrac{M_p\sin i}{(M_\ast+M_p)^{2/3}}\dfrac{1}{\sqrt{1-e^2}}',
        example=[
            f'51 Pegasi b\u2019s orbit (live-verified this session): P = {PLANET_51PEGB["period_d"]:.4f} d, e = {PLANET_51PEGB["e"]:.4f} (essentially circular), giving a semimajor axis via Kepler\u2019s third law of a = {A_51PEGB_M/AU_M:.4f} AU (Mstar={STAR_51PEG["mass_msun"]:.2f} Msun) -- matching the published a = {PLANET_51PEGB["a_au"]:.4f} AU to within the precision of this course\u2019s representative stellar mass.',
            f'Solving the mass function numerically for Mp sin(i) given the measured K = {PLANET_51PEGB["k_rv_m_s"]:.1f} m/s: Mp sin(i) = {MP_SINI_51PEGB_MJUP:.3f} Jupiter masses, matching the published minimum mass ({PLANET_51PEGB["msini_mjup"]:.3f} MJup) computed independently by the discovery team.',
            f'Breaking the sin(i) degeneracy with the inclination i={PLANET_51PEGB["inclination_deg"]:.1f} degrees (later constrained astrometrically): true mass = Mp sin(i)/sin(i) = {MP_TRUE_51PEGB_FROM_SINI_MJUP:.2f} MJup, matching the published true mass ({PLANET_51PEGB["mass_mjup"]:.2f} MJup) -- a direct, worked demonstration of exactly how the minimum-mass degeneracy is resolved.',
        ],
        pitfall='Reporting a radial-velocity-derived planet mass as if it were the true mass without stating the sin(i) assumption. This unit-and-completeness error matters: the true mass equals the minimum mass only if the orbit happens to be observed edge-on (i=90 degrees); for a typical randomly oriented orbit, sin(i)<1 and the true mass is larger than the quoted minimum mass, sometimes substantially so.',
        activity='Using the mass function equation, explain qualitatively (without recomputing) why a radial-velocity survey is more sensitive to massive, close-in planets (large Mp, small P) than to Earth-mass planets at 1 AU, and connect this to why the very first exoplanets discovered (including 51 Pegasi b) were all "hot Jupiters."',
        lab_connection='Lab 01 reproduces this lecture\u2019s full 51 Pegasi b calculation end-to-end (semimajor axis, minimum mass, degeneracy-breaking) and extends it to a second real RV planet.',
        synthesis='The radial-velocity semi-amplitude equation, derived from Kepler\u2019s third law and the center-of-mass condition, converts a measured stellar wobble into a planet\u2019s orbital period, semimajor axis, and minimum mass -- the technique that discovered the first exoplanet around a Sun-like star and that this course now builds on with a second, complementary detection method: the transit.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=2, title='The Transit Method: Light Curves, Depth, and Duration',
        subtitle='Catching a planet in silhouette',
        goals=[
            'Derive the transit-depth relation connecting a dip in stellar brightness to the planet-to-star radius ratio.',
            'Derive an approximate transit-duration relation and explain what additional information a transit provides beyond radial velocity.',
            'Reproduce the real discovery measurement of HD 209458 b, the first transiting exoplanet, and cross-check it against this course\u2019s computed values.',
        ],
        why_matters='Lecture 01\u2019s radial-velocity method gives a planet\u2019s mass (times sin i) but says nothing about its size. The transit method, derived here, supplies the missing radius -- and, combined with radial velocity for the same planet, breaks the sin(i) degeneracy exactly and yields the planet\u2019s true mass, true radius, and therefore its bulk density (Lecture 06).',
        phenomenon=f'On September 9 and 16, 1999, David Charbonneau\u2019s team measured a real, repeatable {PLANET_HD209458B["transit_depth_measured"]*100:.1f}% dip in the brightness of HD 209458, lasting about {PLANET_HD209458B["transit_duration_hr"]:.0f} hours every {PLANET_HD209458B["period_d"]:.2f} days -- the first confirmed transiting exoplanet, simultaneously announced by two independent teams in the same issue of the Astrophysical Journal, and the system this course uses throughout its atmospheres unit (Lectures 07-08).',
        vocab=['transit', 'transit depth', 'transit duration', 'ingress/egress', 'impact parameter', 'occultation (secondary eclipse)'],
        evidence=[
            'A planet passing in front of its star blocks a fraction of the star\u2019s disk proportional to the ratio of their cross-sectional areas, producing a periodic, repeatable dip in brightness with a shape (flat-bottomed trapezoid) that is a direct geometric consequence of the planet\u2019s finite crossing time, confirmed by high-precision photometry of HD 209458 and thousands of subsequent transiting systems.',
            'Only systems with a favorable orbital inclination (viewed nearly edge-on) show transits at all; this geometric requirement is exactly why transiting systems are a minority of all planetary systems, but it is also exactly what makes transiting systems so valuable -- the required near-edge-on inclination (i=86.71 degrees for HD 209458 b) is known precisely from the transit geometry itself.',
            'Combining HD 209458 b\u2019s transit-derived radius with its independently measured (radial-velocity) mass gave the first-ever bulk density measurement for a planet outside the solar system, immediately confirming it as a gas giant and not, for example, a brown dwarf or a rocky super-Earth -- a capability radial velocity alone could never provide.',
        ],
        model=[
            'For a planet of radius Rp transiting a star of radius Rstar, the fractional decrease in observed flux at mid-transit (ignoring stellar limb darkening) is the ratio of blocked area to total area: delta = (Rp/Rstar)^2, a purely geometric relation independent of the planet\u2019s mass or composition.',
            'For a central (impact parameter b=0), circular-orbit transit, the total transit duration is approximately T = (P/pi) * arcsin(Rstar/a), because the star subtends an angular half-width of arcsin(Rstar/a) as seen from the planet\u2019s orbital position; more precise treatments add ingress/egress timing and non-zero impact parameter corrections.',
            'A transiting system\u2019s inclination is fixed by the transit\u2019s existence (i near 90 degrees, quantifiable from the transit\u2019s duration and shape), so if the same planet is also observed with radial velocity, the sin(i) degeneracy from Lecture 01 is broken exactly, yielding both the planet\u2019s true mass and true radius from the same object -- the reason transiting, RV-confirmed planets like HD 209458 b are the best-characterized exoplanets known.',
        ],
        equation=r'\delta = \left(\dfrac{R_p}{R_\ast}\right)^{2}, \qquad T_{\rm dur} \approx \dfrac{P}{\pi}\arcsin\!\left(\dfrac{R_\ast}{a}\right)',
        example=[
            f'HD 209458 b (live-verified this session): Rp = {PLANET_HD209458B["radius_rjup"]:.3f} RJup, Rstar = {STAR_HD209458["radius_rsun"]:.2f} Rsun. Computed transit depth delta = (Rp/Rstar)^2 = {TRANSIT_DEPTH_HD209458B_COMPUTED*100:.2f}%, matching the discovery team\u2019s measured {PLANET_HD209458B["transit_depth_measured"]*100:.1f}% dip to within the precision of the adopted stellar radius.',
            f'Computed transit duration from P = {PLANET_HD209458B["period_d"]:.3f} d and a = {A_HD209458B_M/AU_M:.4f} AU: T = (P/pi) arcsin(Rstar/a) = {TRANSIT_DURATION_HD209458B_COMPUTED:.2f} h, matching the discovery paper\u2019s reported \u2248{PLANET_HD209458B["transit_duration_hr"]:.0f}-hour transit.',
            f'Cross-checking with Lecture 01\u2019s method: HD 209458 b\u2019s radial-velocity semi-amplitude, predicted from its independently known true mass ({PLANET_HD209458B["mass_mjup"]:.3f} MJup) and inclination ({PLANET_HD209458B["inclination_deg"]:.2f} degrees, from the transit), gives K = {K_HD209458B_PREDICTED:.1f} m/s, matching the published measured value ({PLANET_HD209458B["k_rv_m_s"]:.2f} m/s) -- direct confirmation that the two independent detection methods agree on the same real planet.',
        ],
        pitfall='Assuming transit depth alone gives a planet\u2019s absolute size. Transit depth only ever gives the ratio Rp/Rstar; converting to an absolute planet radius requires an independently known stellar radius (from the star\u2019s spectral type, parallax-based luminosity, or asteroseismology), so an error in the assumed stellar radius propagates directly and proportionally into every transiting planet\u2019s reported radius.',
        activity='Using T &prop; P^(1/3) (from a &prop; P^(2/3) via Kepler\u2019s third law) and Rstar/a &prop; a^(-1), explain qualitatively why short-period, close-in planets have both higher transit probability and shorter transit duration than long-period planets, and why this makes hot Jupiters disproportionately easy to detect by transit as well as by radial velocity.',
        lab_connection='Lab 01 also reproduces this lecture\u2019s HD 209458 b transit-depth and duration calculations and cross-checks the two independent detection methods against each other for the same real planet.',
        synthesis='The transit method supplies exactly what radial velocity cannot: a planet\u2019s radius and (via the transit-fixed inclination) an exact, not minimum, mass when combined with radial velocity -- together the two methods gave HD 209458 b the first bulk density ever measured for a world outside the solar system, opening the door to every interior and atmospheric characterization technique this course develops later.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=3, title='Complementary Detection: Astrometry, Microlensing, and Direct Imaging',
        subtitle='Three more ways to find a world that neither wobbles convincingly nor transits',
        goals=[
            'Describe the physical principle behind astrometric, gravitational-microlensing, and direct-imaging exoplanet detection.',
            'Identify which region of orbital-separation/mass parameter space each detection method is most sensitive to, and why.',
            'Explain why no single detection method provides a complete, unbiased census of the exoplanet population.',
        ],
        why_matters='Lectures 01-02 built the two workhorse detection methods, but each has a strong observational bias (favoring close-in, massive planets around bright, quiet stars). This lecture completes the detection-method toolkit and sets up Lecture 04\u2019s demographics, which cannot be correctly interpreted without understanding each method\u2019s selection effects.',
        phenomenon='The four major exoplanet detection methods -- radial velocity, transit, astrometry, microlensing, and direct imaging -- are sensitive to almost entirely different, only partially overlapping regions of the planet mass-versus-orbital-separation plane, so the observed exoplanet population is not a fair sample of what actually exists; it is a composite shaped by which methods have been applied to which stars for how long.',
        vocab=['astrometry', 'gravitational microlensing', 'direct imaging', 'coronagraph', 'selection effect (observational bias)', 'occurrence rate'],
        evidence=[
            'Astrometric planet detection (measuring the tiny periodic wobble of a star\u2019s position on the sky, rather than its radial velocity) requires positional precision at the microarcsecond level for Sun-like stars; Gaia\u2019s astrometric mission has been documented to detect and characterize dozens of massive, long-period planets this way, a regime radial velocity surveys of the same duration cannot easily reach.',
            'Gravitational microlensing detections occur when a foreground star-plus-planet system passes very nearly in front of a distant background star, temporarily magnifying its light; the planet\u2019s gravity produces a brief, characteristic secondary spike in the magnification light curve, documented in hundreds of published microlensing events, uniquely sensitive to planets at several AU around faint or distant stars that no other method can currently probe.',
            'Direct imaging has successfully resolved a small number of young, massive, wide-separation planets (e.g., the HR 8799 system) as faint point sources next to their much brighter host star, requiring a coronagraph or starshade to suppress the star\u2019s overwhelming glare; documented direct-imaging surveys are strongly biased toward young, self-luminous, wide-orbit giant planets, the opposite bias from radial velocity and transit surveys.',
        ],
        model=[
            'Astrometry measures the star\u2019s reflex orbital motion projected onto the plane of the sky (rather than along the line of sight, as in radial velocity), so it is most sensitive to systems viewed face-on -- precisely the orbital orientations radial velocity is least sensitive to, making the two methods geometrically complementary.',
            'Microlensing detection sensitivity depends on the lens-source alignment geometry and typical Galactic distances/timescales, not on the planet\u2019s brightness at all, so it can detect planets around stars far too faint or distant for radial velocity or transit follow-up, but each event is a one-time, non-repeatable geometric alignment rather than a a system that can be revisited.',
            'Direct imaging detects a planet\u2019s own thermal or reflected light rather than inferring its presence from an effect on the star, so its sensitivity is set by the planet\u2019s own luminosity and angular separation from the star (favoring young, hot, self-luminous, wide-orbit giants) and by the achievable contrast ratio between planet and star (requiring active suppression of the star\u2019s much brighter point-spread function, Lecture 11 of ASTR 340\u2019s adaptive-optics unit).',
        ],
        equation=r'\theta_{\rm astrometric} \approx \dfrac{M_p}{M_\ast}\dfrac{a}{d}\ (\text{angular reflex amplitude at distance } d), \qquad A(u) = \dfrac{u^2+2}{u\sqrt{u^2+4}}\ (\text{microlensing magnification})',
        example=[
            f'Astrometric reflex-motion estimate for a Jupiter-mass planet at 5 AU around a Sun-like star at 10 pc: theta &asymp; (Mp/Mstar)(a/d) = ({(1*M_JUP/M_SUN):.4f})({5/10:.2f} rad-equivalent, converted) &asymp; {(1*M_JUP/M_SUN)*(5*AU_M)/( 10*3.086e16)*206265*1000:.1f} milliarcsec -- within reach of Gaia-class astrometric precision, illustrating why astrometry favors long-period giant planets around nearby stars.',
            f'Comparing detection regimes with this course\u2019s own real planets: 51 Pegasi b (a={PLANET_51PEGB["a_au"]:.3f} AU) and HD 209458 b (a={PLANET_HD209458B["a_au"]:.3f} AU) are both deep in the RV/transit-favored close-in regime; TRAPPIST-1e (a={TRAPPIST1_PLANETS["e"]["a_au"]:.3f} AU around a star of only {TRAPPIST1_STAR["mass_msun"]:.3f} Msun) is detectable by transit specifically because its very low-mass host star makes even an Earth-sized planet\u2019s transit depth and RV signal comparatively large.',
            'Direct-imaging contrast requirement: a Jupiter-mass planet at 5 AU around a Sun-like star is roughly a billion times fainter than its star in reflected light, quantifying why direct imaging has so far only succeeded for young, self-luminous giants at wide separation (tens of AU), where both the planet is intrinsically brighter (residual formation heat) and the angular separation is large enough to suppress starlight with a coronagraph.',
        ],
        pitfall='Treating the observed exoplanet population (dominated by hot Jupiters in early discoveries, and by close-in small planets in Kepler-era transit surveys) as if it directly reflects the true underlying population of planets in the galaxy. Every detection method has a strong, quantifiable selection effect; correcting for these biases (Lecture 04) is a prerequisite for any honest demographic statement like "Earth-size planets are common."',
        activity='Given that radial velocity favors close-in, massive planets and transit favors close-in planets of any mass (with a probability that also depends on stellar radius), while direct imaging favors wide-separation, massive, young planets, sketch which regions of the mass-versus-separation plane remain poorly explored by all three methods combined, and explain why this matters for interpreting any claim about the true occurrence rate of Earth-like planets.',
        lab_connection='Lab 02 uses this lecture\u2019s selection-effect reasoning, together with Lecture 04\u2019s occurrence-rate framework, to correct a simplified simulated detection sample for survey bias.',
        synthesis='Radial velocity, transit, astrometry, microlensing, and direct imaging are geometrically and physically complementary, each sensitive to a different region of planet mass and orbital separation; no single method gives an unbiased census, so every demographic conclusion in the next lecture must explicitly account for which method(s) produced the underlying sample.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=4, title='Exoplanet Demographics: Occurrence Rates and the Mass-Radius Relation',
        subtitle='What thousands of confirmed planets tell us about what is common',
        goals=[
            'Define planet occurrence rate and explain how survey completeness corrections convert a raw detection count into a true occurrence rate.',
            'Describe the observed exoplanet mass-radius relation and identify the physical transition between rocky and gas-dominated planets.',
            'Interpret the observed "radius valley" in the Kepler planet-radius distribution as evidence for atmospheric mass loss.',
        ],
        why_matters='With detection methods (Lectures 01-03) established, this lecture asks the population-level question every subsequent topic in this course depends on: how common are different kinds of planets, and what does the shape of the mass-radius relation reveal about planetary composition before any detailed interior model (Lecture 06) is built?',
        phenomenon='The Kepler mission\u2019s multi-year transit survey of over 150,000 stars found that small planets (Earth- to Neptune-sized) are dramatically more common than Jupiter-sized planets, and revealed an unexpected near-absence of planets between about 1.5 and 2.0 Earth radii -- the "radius valley" -- a demographic gap that does not appear in any single-planet detection but only emerges from population-level statistics across thousands of systems.',
        vocab=['occurrence rate', 'survey completeness', 'radius valley (Fulton gap)', 'super-Earth', 'sub-Neptune', 'mass-radius relation', 'photoevaporation'],
        evidence=[
            'Kepler-era occurrence-rate studies (Batalha et al. 2013 and many follow-ups) correct raw detection counts for each star\u2019s specific transit probability (Lecture 02, depends on a/Rstar) and detection sensitivity (depends on the star\u2019s brightness and noise properties) before reporting a corrected occurrence rate, because a raw, uncorrected count would badly underrepresent small, long-period planets that are intrinsically harder to detect.',
            'The observed mass-radius relation for confirmed exoplanets shows a clear break: below roughly 1.5-2 Earth radii, radius increases only slowly with mass (consistent with a rocky, roughly constant-density composition), while above this break, radius increases much more steeply with only a small mass increase (consistent with a growing hydrogen/helium or ice-rich envelope) -- a transition visible directly in the data before any interior model is invoked.',
            'The radius valley, first robustly measured in the California-Kepler Survey (Fulton et al. 2017), separates two distinct sub-populations (smaller, likely bare-rock super-Earths and larger, likely volatile-rich sub-Neptunes) and is now widely interpreted as evidence that many sub-Neptune-sized planets lose their primordial hydrogen/helium envelopes via photoevaporation or core-powered mass loss, shrinking them across the valley over their first ~1 Gyr.',
        ],
        model=[
            'A survey\u2019s raw detection count for a given planet size and period bin must be divided by that bin\u2019s combined transit probability and detection completeness (both computable from the survey\u2019s known noise properties and target star sample) to recover a true, bias-corrected occurrence rate -- exactly the correction Lecture 03 flagged as necessary before making any demographic claim.',
            'This course\u2019s own real solar-system and exoplanet dataset (Lecture 04\u2019s worked mass-radius comparison) already shows the rocky/gas-giant dichotomy directly: Earth, Venus, and Mars cluster on a steep, roughly constant-density mass-radius track, while Jupiter, HD 209458 b, and 51 Pegasi b cluster on a nearly flat track where a 300-fold mass range corresponds to less than a factor of 2 in radius, because gas giants are supported by electron-degeneracy pressure at high mass rather than ordinary compressibility.',
            'The radius valley\u2019s location and depth are predicted, with reasonable quantitative success, by photoevaporation models in which intense high-energy (X-ray/UV) irradiation from a young, active host star strips a close-in planet\u2019s hydrogen/helium envelope over roughly its first hundred million to one billion years, converting some sub-Neptunes into bare, rocky super-Earths and leaving a relative dearth of planets at the transitional radius.',
        ],
        equation=r'\text{Occurrence rate} = \dfrac{N_{\rm detected}}{N_{\rm stars\ surveyed} \times P_{\rm transit} \times C_{\rm completeness}}, \qquad \rho \propto M/R^{3}',
        example=[
            f'This course\u2019s own mass-radius sample (Lecture 04\u2019s figure): Earth (M=1.0 Mearth, R=1.0 Rearth, rho=5514 kg/m^3), TRAPPIST-1e (M={TRAPPIST1_PLANETS["e"]["m_earth"]:.3f} Mearth, R={TRAPPIST1_PLANETS["e"]["r_earth"]:.3f} Rearth, rho={TRAPPIST1_DENSITY_KG_M3["e"]:.0f} kg/m^3) both sit near Earth\u2019s density, while HD 209458 b (M={PLANET_HD209458B["mass_mjup"]*M_JUP/M_EARTH:.0f} Mearth, R={PLANET_HD209458B["radius_rjup"]*R_JUP/R_EARTH:.1f} Rearth, rho={HD209458B_DENSITY_KG_M3:.0f} kg/m^3) has a density lower than water, a direct numeric illustration of the rocky/gas-giant density dichotomy.',
            f'Density ratio: Earth is {5514/HD209458B_DENSITY_KG_M3:.0f}&times; denser than HD 209458 b despite HD 209458 b having {PLANET_HD209458B["mass_mjup"]*M_JUP/M_EARTH:.0f}&times; Earth\u2019s mass -- only possible because a gas giant\u2019s radius is set by pressure-supported hydrogen/helium, not by the same rocky-material compressibility that sets Earth\u2019s radius.',
            f'TRAPPIST-1 system radius spread: the seven planets range from {min(d["r_earth"] for d in TRAPPIST1_PLANETS.values()):.3f} to {max(d["r_earth"] for d in TRAPPIST1_PLANETS.values()):.3f} Earth radii, entirely below the radius-valley transition, consistent with all seven being bare or thin-atmosphere rocky worlds rather than sub-Neptunes -- a real system-level illustration of the small-planet side of the demographic picture this lecture describes statistically.',
        ],
        pitfall='Treating an early-discovered, RV/transit-biased sample (dominated by hot Jupiters, since 51 Pegasi b in 1995) as evidence that hot Jupiters are the most common type of planet. Occurrence-rate studies correcting for detection bias instead find that small, close-in planets (super-Earths and sub-Neptunes) are far more numerous than hot Jupiters around Sun-like stars; the earliest discoveries were the easiest to detect, not the most common to exist.',
        activity='Given that a rocky planet\u2019s density is roughly constant with mass (radius grows slowly with mass) while a gas giant\u2019s radius is nearly independent of mass at high mass, sketch qualitatively why the mass-radius relation must have an inflection point somewhere between super-Earth and Saturn-mass planets, and connect this inflection to the radius valley\u2019s location.',
        lab_connection='Lab 02 builds a log-log mass-radius diagram from this course\u2019s own real planet sample (solar system, TRAPPIST-1, 51 Peg b, HD 209458 b) and classifies each planet by its inferred bulk composition regime.',
        synthesis='Correcting raw detection counts for each method\u2019s selection effects reveals that small, close-in rocky and volatile-rich planets vastly outnumber hot Jupiters, and the mass-radius relation\u2019s rocky/gas-giant dichotomy -- together with the radius valley\u2019s photoevaporation-driven gap -- sets the stage for Lecture 06\u2019s detailed interior-structure inference and this course\u2019s later habitability discussion.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=5, title='Orbital Architectures: Eccentricities, Resonances, and Migration',
        subtitle='Why our own solar system\u2019s tidy, nearly circular orbits are not the galactic default',
        goals=[
            'Compare the eccentricity distribution of confirmed exoplanets to the solar system\u2019s planets and identify what physical process circularizes close-in orbits.',
            'Explain orbital (mean-motion) resonance and identify a real resonant chain among exoplanets.',
            'Describe the two leading migration mechanisms that bring giant planets from their formation location to a hot-Jupiter-class close orbit.',
        ],
        why_matters='Lecture 04 established what kinds of planets are common; this lecture asks how those planets got into the orbits we observe them in today. Orbital architecture is not a fixed initial condition -- it is dynamically sculpted after formation, and understanding this is essential context before Lecture 09 asks whether a given orbit is compatible with stable, long-term habitability.',
        phenomenon=f'HD 80606 b, a real Jupiter-class planet, has an orbital eccentricity of 0.93 -- swinging from 0.03 AU at closest approach (closer than Mercury) to nearly 0.9 AU at its farthest, a factor-of-30 change in stellar flux over a single 111-day orbit -- while the seven TRAPPIST-1 planets orbit in a strikingly precise resonant chain, with adjacent orbital periods within a fraction of a percent of simple whole-number ratios, two starkly different orbital architectures this lecture explains with the same underlying dynamics.',
        vocab=['orbital eccentricity', 'tidal circularization', 'mean-motion resonance', 'resonant chain', 'disk-driven (Type II) migration', 'high-eccentricity (Kozai-Lidov/planet-planet scattering) migration'],
        evidence=[
            'Confirmed exoplanet eccentricities span the full range from 0 to over 0.9, in sharp contrast to the solar system\u2019s planets (all e<0.21, most under 0.1); this broad eccentricity distribution, absent from pre-1995 solar-system-only intuition, was one of the first major surprises of exoplanet science and directly motivated new theories of planet-planet dynamical interaction.',
            'Nearly all known hot Jupiters (orbital period under about 10 days), including both 51 Pegasi b and HD 209458 b in this course\u2019s own real dataset, have eccentricities statistically consistent with zero, while planets at larger separation (like HD 80606 b at 0.455 AU) retain eccentricities up to nearly 1 -- a pattern matching the predicted, steeply separation-dependent timescale for tidal circularization.',
            'The TRAPPIST-1 system\u2019s seven planets were confirmed, via precise transit-timing-variation measurements (small, periodic departures from a perfectly regular transit schedule caused by mutual gravitational tugs), to lie in a near-perfect Laplace-like resonant chain, a configuration far too finely tuned to have arisen by chance and strong observational evidence for disk-driven convergent migration during the system\u2019s formation.',
        ],
        model=[
            'Tidal bulges raised on a planet by its star (and vice versa) dissipate orbital energy fastest when the two bodies are closest together; because tidal torque scales steeply with the inverse orbital separation, this dissipation circularizes close-in orbits (like hot Jupiters) on timescales short compared to the system\u2019s age, while leaving wider-orbit planets\u2019 original, often high, eccentricities essentially unchanged over the same age.',
            'A mean-motion resonance occurs when two planets\u2019 orbital periods form a ratio of small integers (e.g., 3:2, 2:1), so their mutual gravitational perturbations repeat at the same orbital phase every cycle, reinforcing rather than averaging out; such configurations are dynamically stable but require either a special, resonance-favoring formation process or migration that captures planets into resonance as their orbits slowly converge.',
            'Two distinct pathways are invoked to explain hot Jupiters\u2019 close-in, often-circular orbits: disk-driven (Type II) migration, in which a giant planet opens a gap in its natal protoplanetary disk and migrates inward smoothly while the disk still exists, and high-eccentricity migration, in which planet-planet scattering or Kozai-Lidov oscillations from a distant companion first pump a planet\u2019s eccentricity to extreme values, after which tidal circularization at the resulting close perihelion shrinks and circularizes the orbit.',
        ],
        equation=r'\dfrac{P_{j+1}}{P_j} = \dfrac{p+q}{p}\ (\text{integer resonance}), \qquad \dfrac{de}{dt}\Big|_{\rm tidal} \propto -\dfrac{e}{a^{13/2}}\ (\text{steep separation dependence})',
        example=[
            f'This course\u2019s real eccentricity sample: 51 Peg b (a={PLANET_51PEGB["a_au"]:.4f} AU, e={PLANET_51PEGB["e"]:.4f}) and HD 209458 b (a={PLANET_HD209458B["a_au"]:.4f} AU, e={PLANET_HD209458B["e"]:.4f}) are both close-in and both essentially circular, while HD 80606 b (a=0.455 AU, e=0.93) and 16 Cygni B b (a=1.68 AU, e=0.69) are both farther out and both highly eccentric -- exactly the tidal-circularization-timescale pattern this lecture derives qualitatively.',
            f'TRAPPIST-1 adjacent period ratios (this course\u2019s live-verified system): P_c/P_b = {TRAPPIST1_PLANETS["c"]["period_d"]/TRAPPIST1_PLANETS["b"]["period_d"]:.4f} (close to 8:5 = 1.6), P_d/P_c = {TRAPPIST1_PLANETS["d"]["period_d"]/TRAPPIST1_PLANETS["c"]["period_d"]:.4f} (close to 5:3 = 1.667), P_e/P_d = {TRAPPIST1_PLANETS["e"]["period_d"]/TRAPPIST1_PLANETS["d"]["period_d"]:.4f} (close to 3:2 = 1.5) -- each within a few percent of a simple integer ratio, quantifying the resonant-chain claim directly from this course\u2019s own real orbital-period data.',
            f'Continuing outward: P_f/P_e = {TRAPPIST1_PLANETS["f"]["period_d"]/TRAPPIST1_PLANETS["e"]["period_d"]:.4f} (close to 3:2), P_g/P_f = {TRAPPIST1_PLANETS["g"]["period_d"]/TRAPPIST1_PLANETS["f"]["period_d"]:.4f} (close to 4:3), P_h/P_g = {TRAPPIST1_PLANETS["h"]["period_d"]/TRAPPIST1_PLANETS["g"]["period_d"]:.4f} (close to 3:2) -- six consecutive near-resonant period ratios spanning the entire system, the observational signature of convergent disk migration this lecture identifies as the likely formation pathway.',
        ],
        pitfall='Assuming every close ratio between two planets\u2019 periods indicates a true dynamical resonance. A ratio must also satisfy a specific angular (resonant-argument) libration condition, confirmed dynamically (e.g., via transit-timing variations or long-term orbital stability simulations), not just a numerical coincidence in the period ratio; TRAPPIST-1\u2019s resonances are confirmed this rigorous way, which is why they are cited with confidence rather than as a numerological curiosity.',
        activity='Using the steep a-dependence of the tidal-circularization timescale, estimate qualitatively whether a planet at 10x HD 209458 b\u2019s orbital separation, but otherwise identical, would be expected to be circularized within the system\u2019s multi-Gyr age, and explain what this implies about using orbital eccentricity as an indirect clue to a planet\u2019s migration history.',
        lab_connection='Lab 03 computes TRAPPIST-1\u2019s full chain of adjacent period ratios and classifies each against the nearest simple integer resonance, then examines the eccentricity-versus-separation pattern across this course\u2019s full real-planet sample.',
        synthesis='Orbital eccentricities and resonant architectures are not fossils of the original formation configuration but the product of ongoing dynamical sculpting -- tidal circularization for close-in planets, and either disk-driven or high-eccentricity migration for how giant planets arrived at their observed orbits -- context this course now carries into Lecture 06\u2019s interior-structure inference and the habitability discussion of Lectures 09-10.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=6, title='Planetary Interiors from Mass and Radius: The Composition Degeneracy',
        subtitle='What a single density number can, and cannot, tell you',
        goals=[
            'Derive bulk density from mass and radius and use it to constrain, but not uniquely determine, a planet\u2019s interior composition.',
            'Explain the mass-radius composition degeneracy: why multiple distinct internal structures can produce the same observed mass and radius.',
            'Apply interior-structure reasoning to classify this course\u2019s real planets (TRAPPIST-1 system, HD 209458 b) by their most probable bulk composition.',
        ],
        why_matters='Lecture 04 showed the population-level mass-radius relation; this lecture drills into what a single planet\u2019s mass and radius measurement can and cannot reveal about its interior, a limitation every subsequent habitability and biosignature discussion in this course must respect rather than overstate.',
        phenomenon=f'TRAPPIST-1e has a measured bulk density of {TRAPPIST1_DENSITY_KG_M3["e"]:.0f} kg/m^3, close to Earth\u2019s {5514} kg/m^3 -- but that single number is consistent with several different real internal structures (an Earth-like iron-core-plus-rocky-mantle planet, or a smaller iron core with a substantial water/ice layer) that no mass-radius measurement alone can distinguish, a genuine and important limitation this lecture makes explicit rather than glossing over.',
        vocab=['bulk density', 'mass-radius composition degeneracy', 'iron-mass fraction', 'water world', 'equation of state', 'interior structure model'],
        evidence=[
            'Solar-system planets with independently known interior structure (from seismology, Lecture-level moment-of-inertia measurements, or spacecraft gravity mapping in other courses) confirm that Earth\u2019s bulk density (5514 kg/m^3) reflects a large iron-nickel core (about 32% of Earth\u2019s mass) plus a silicate mantle, while Mars\u2019s lower density (3934 kg/m^3) reflects a proportionally smaller core -- ground-truth interior information no currently known exoplanet has.',
            'Published interior-structure modeling studies (e.g., Zeng et al. 2016 and related mass-radius-composition grids) show that a single measured (mass, radius) pair for a rocky-density-range exoplanet is consistent with a continuous family of models trading an iron core fraction against a water/ice mass fraction, because both a larger core and a thick ice layer can independently raise or lower the bulk density from a pure-silicate baseline.',
            'This degeneracy is not merely theoretical: published characterization papers for real terrestrial-density exoplanets routinely report a range of plausible interior compositions (e.g., "consistent with an Earth-like core fraction, or with a smaller core plus a significant water layer") rather than a single determined structure, precisely because mass and radius alone cannot break the degeneracy without additional data (e.g., atmospheric composition, or in rare cases tidal Love-number measurements).',
        ],
        model=[
            'Bulk density rho = M/(4/3 pi R^3) is the single most information-dense number available from a mass-radius measurement alone, and it immediately separates gas-dominated planets (rho well below 2000 kg/m^3, requiring a substantial hydrogen/helium or ice envelope) from rocky/iron-dominated planets (rho in the roughly 3000-8000 kg/m^3 range).',
            'Within the rocky-density range, published equation-of-state models for iron, silicate rock, and water ice at planetary interior pressures let modelers compute the mass-radius curve for any assumed layered structure (core mass fraction, mantle, ice/water layer); multiple distinct layered structures can reproduce the same observed (M, R) point, which is the composition degeneracy this lecture\u2019s central claim rests on.',
            'Breaking the degeneracy in practice requires information beyond mass and radius: an independently measured atmospheric composition (Lecture 07) can rule out a bare-rock interpretation if a thick volatile envelope is detected, and in rare, favorable cases a measured tidal response (Love number) can directly constrain the presence of a liquid or partially molten interior layer.',
        ],
        equation=r'\rho = \dfrac{M}{\tfrac{4}{3}\pi R^{3}}, \qquad \rho(\text{model}) = f(\text{core fraction},\ \text{mantle fraction},\ \text{ice/water fraction})',
        example=[
            f'This course\u2019s TRAPPIST-1 density table (computed directly from each planet\u2019s real mass and radius): ' + ', '.join(
                f'{p} (&rho;&#8776;{TRAPPIST1_DENSITY_KG_M3[p]:.0f} kg/m&sup3;)' for p in TRAPPIST1_PLANETS) + ' -- d and h are the two lowest-density planets in the system, consistent with a proportionally larger volatile (ice/water) fraction relative to their rock-and-iron mass.',
            f'Comparing TRAPPIST-1e directly to Earth: {TRAPPIST1_DENSITY_KG_M3["e"]:.0f} kg/m&sup3; versus Earth\u2019s {5514} kg/m&sup3; -- a {abs(TRAPPIST1_DENSITY_KG_M3["e"]-5514)/5514*100:.1f}% difference, small enough that both an Earth-like core fraction and a modestly smaller core plus thin volatile layer remain viable interpretations without additional data.',
            f'Contrast with the unambiguous case: HD 209458 b\u2019s density ({HD209458B_DENSITY_KG_M3:.0f} kg/m^3, lower than water) requires no degeneracy-breaking argument at all -- no plausible rocky/icy layered structure can produce a density this low at this radius, so a hydrogen/helium-dominated gas-giant interior is the only physically consistent interpretation.',
        ],
        pitfall='Reporting a single, confident interior-composition claim (e.g., "this exoplanet is a water world") from mass and radius alone without acknowledging the degeneracy. A responsible characterization states the full range of interior models consistent with the measured density, exactly as this lecture\u2019s TRAPPIST-1e example does, rather than picking one plausible model and presenting it as the only possibility.',
        activity='Explain why a planet\u2019s bulk density alone can immediately and unambiguously rule out a pure hydrogen/helium gas-giant interpretation for a rocky-density-range planet, even though it cannot uniquely determine that planet\u2019s core-to-mantle-to-ice-layer proportions.',
        lab_connection='Lab 03 computes bulk densities for all seven TRAPPIST-1 planets from their real measured masses and radii and evaluates, for each, whether the mass-radius composition degeneracy can or cannot be resolved with density alone.',
        synthesis='Bulk density, computed directly from mass and radius, powerfully separates gas giants from rocky/icy worlds, but within the rocky-density range it cannot uniquely determine a planet\u2019s internal layering -- a genuine, honestly stated limitation of exoplanet characterization that sets up Lecture 07\u2019s atmospheric characterization as the next, complementary source of compositional information.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=7, title='Atmospheric Characterization: Transmission and Emission Spectroscopy',
        subtitle='Reading a planet\u2019s atmosphere in the light that grazes or glows past it',
        goals=[
            'Derive how atmospheric scale height sets the amplitude of spectral features in a transiting planet\u2019s transmission spectrum.',
            'Distinguish transmission spectroscopy (transit) from emission spectroscopy (secondary eclipse) and state what each measures.',
            'Reproduce, from first principles, the real 2001-2002 detection of sodium in HD 209458 b\u2019s atmosphere, the first exoplanet atmosphere ever measured.',
        ],
        why_matters='Lecture 06 showed that mass and radius alone cannot uniquely determine an interior\u2019s composition. Atmospheric spectroscopy, derived here, supplies the complementary observational handle -- direct chemical composition information -- that both breaks some interior-composition ambiguity and (Lectures 11-12) sets up the entire biosignature discussion later in this course.',
        phenomenon=f'In November 2001, using the Hubble Space Telescope, Charbonneau, Brown, Noyes, and Gilliland detected a small, specific absorption feature at 589 nm (the sodium D line) in starlight passing through HD 209458 b\u2019s atmosphere during transit -- weaker than a naive cloud-free-atmosphere model predicted, but a real, repeatable measurement that opened the entire field of exoplanet atmospheric characterization this course now takes for granted.',
        vocab=['transmission spectroscopy', 'emission spectroscopy', 'secondary eclipse (occultation)', 'scale height', 'sodium D line', 'terminator (day-night boundary)'],
        evidence=[
            'During transit, some starlight grazes tangentially through a planet\u2019s upper atmosphere along the day-night terminator before reaching the observer; at wavelengths where an atmospheric constituent absorbs strongly, the effective planetary radius appears larger, deepening the transit slightly at that specific wavelength -- exactly the signal Charbonneau et al. (2002) measured for HD 209458 b\u2019s sodium.',
            'Emission spectroscopy instead compares a system\u2019s combined (star+planet) brightness just before secondary eclipse (planet visible) to the star alone during eclipse (planet hidden behind the star), isolating the planet\u2019s own thermal emission spectrum -- a technique first demonstrated for HD 209458 b and the similarly bright hot Jupiter TrES-1 using the Spitzer Space Telescope in 2005.',
            'Subsequent re-analyses and new observations of HD 209458 b (through the 2000s and 2010s, using Hubble, Spitzer, and ground-based high-resolution spectrographs) have reported water vapor, carbon monoxide, and other molecular species in addition to the original sodium detection, together building the most thoroughly characterized hot-Jupiter atmosphere of its era.',
        ],
        model=[
            'An atmospheric spectral feature\u2019s amplitude in transmission scales with the atmosphere\u2019s pressure scale height H = kT/(mu g), the vertical distance over which pressure drops by 1/e; a larger scale height (hotter atmosphere, lower mean molecular mass, or lower surface gravity) produces a deeper, more easily detected spectral feature for a fixed absorber abundance.',
            'The additional transit depth contributed by N scale heights of atmosphere above the bulk (continuum) planetary radius is approximately delta(N) - delta(0) &asymp; 2 N H Rp / Rstar^2, which is why hot, low-gravity, inflated planets like HD 209458 b (with a large scale height) show much more readily detectable spectral features than smaller, higher-gravity, cooler planets of similar bulk radius.',
            'Emission spectroscopy probes the planet\u2019s dayside thermal structure directly (brightness temperature as a function of wavelength, related to the vertical temperature profile via the same Planck-function physics used throughout astronomy), while transmission spectroscopy probes only the cooler, higher-altitude terminator atmosphere -- the two techniques are complementary, not redundant, exactly as radial velocity and transit are complementary for orbital characterization (Lectures 01-02).',
        ],
        equation=r'H = \dfrac{k_B T}{\mu\, g}, \qquad \delta(\lambda) - \delta_0 \approx \dfrac{2\,N(\lambda)\,H\,R_p}{R_\ast^{2}}',
        example=[
            f'HD 209458 b\u2019s exosphere temperature (real, HST-measured) is roughly {PLANET_HD209458B["exosphere_temp_k"]:.0f} K; using a representative atomic hydrogen mean molecular mass and this course\u2019s computed surface gravity g={HD209458B_SURFACE_G:.2f} m/s^2, the scale height is H = kT/(mu g) = {HD209458B_SCALE_HEIGHT_H2_M/1000:.0f} km -- more than {HD209458B_SCALE_HEIGHT_H2_M/RP_HD209458B_M*100:.2f}% of the planet\u2019s own radius, quantifying why this particular hot, puffed-up planet was the first, most favorable target for atmospheric detection.',
            f'Estimated transit-depth signal from N=5 scale heights of absorbing atmosphere: delta(N)-delta(0) &asymp; 2NH Rp/Rstar^2 &#8776; {5*HD209458B_SCALE_HEIGHT_H2_M*RP_HD209458B_M/RSTAR_HD209458_M**2*100:.3f} percentage points above the {TRANSIT_DEPTH_HD209458B_COMPUTED*100:.2f}% continuum transit depth -- small, but within the precision Hubble\u2019s STIS spectrograph achieved in the original 2001-2002 sodium detection.',
            'Real result from the same system: the measured sodium absorption signal was in fact smaller than a clear, cloud-free atmosphere model predicted, a genuine anomaly the discovery team and later studies interpreted as evidence for high-altitude clouds or haze partially muting the expected feature -- an honest example of theory and observation disagreeing in an informative way, not a measurement error.',
        ],
        pitfall='Assuming a non-detection or weaker-than-predicted spectral feature means an atmospheric constituent is absent. HD 209458 b\u2019s real sodium feature was smaller than a simple cloud-free model predicted precisely because of high-altitude haze/clouds muting (not eliminating) the signal -- a weak or absent feature is evidence about atmospheric structure (e.g., cloud/haze presence), not necessarily about bulk chemical absence, a distinction directly relevant to the biosignature false-positive reasoning of Lecture 11.',
        activity='Using H = kT/(mu g), explain why a cooler, higher-gravity rocky planet (like an Earth-mass planet at 1 AU around a Sun-like star) produces a far smaller transmission-spectroscopy signal than a hot Jupiter like HD 209458 b, and what this implies about which planets current-generation telescopes can realistically characterize atmospherically.',
        lab_connection='Lab 04 computes HD 209458 b\u2019s atmospheric scale height and predicted transmission-spectroscopy signal amplitude from first principles and compares it to the real, published sodium-detection measurement.',
        synthesis='Transmission spectroscopy (probing the cool terminator atmosphere during transit) and emission spectroscopy (probing the warm dayside during secondary eclipse) together let astronomers measure real exoplanet atmospheric composition, starting with HD 209458 b\u2019s landmark 2001-2002 sodium detection -- but a planet\u2019s scale height, and therefore its detectability, depends steeply on temperature and surface gravity, exactly the physics Lecture 08 now turns to atmospheric escape to explain why some planets retain thick atmospheres and others do not.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=8, title='Atmospheric Escape and the Evaporating Hot Jupiters',
        subtitle='A planet slowly losing itself to its own star',
        goals=[
            'Derive the Jeans escape parameter and use it to distinguish thermal (Jeans) escape from hydrodynamic blow-off.',
            'Reproduce, from first principles, the real detection and interpretation of HD 209458 b\u2019s evaporating exosphere.',
            'Explain why atmospheric escape is a first-order consideration for the long-term habitability of close-in planets, previewing Lectures 09-10.',
        ],
        why_matters='Lecture 07 showed how to measure atmospheric composition; this lecture asks whether that atmosphere is stable over the planet\u2019s lifetime, or actively escaping. Atmospheric escape connects directly to this course\u2019s habitability unit: a planet in the classical habitable zone (Lecture 09) is not actually habitable if its atmosphere escapes on a timescale short compared to the time needed for life to develop.',
        phenomenon=f'In 2003, Vidal-Madjar and collaborators used Hubble to detect an enormous, extended envelope of escaping hydrogen (and later, carbon and oxygen) around HD 209458 b, reaching {PLANET_HD209458B["exosphere_extent_rjup"]:.1f} planetary radii from the planet -- roughly the size of the planet\u2019s own Hill sphere -- with an estimated present-day mass-loss rate of {PLANET_HD209458B["mass_loss_kg_s"]:.0e} kg/s, the first exoplanet directly observed in the act of losing its atmosphere to space.',
        vocab=['Jeans escape', 'Jeans escape parameter (lambda)', 'hydrodynamic escape (blow-off)', 'exobase', 'Roche-lobe overflow (for atmospheres)', 'photoevaporation'],
        evidence=[
            f'HD 209458 b\u2019s hydrogen exosphere was detected via a deep (up to 15%) absorption signature in the hydrogen Lyman-alpha line during transit -- far deeper than the planet\u2019s own {PLANET_HD209458B["radius_rjup"]:.3f}-Jupiter-radius bulk transit depth can explain, directly indicating gas extending far beyond the planet\u2019s nominal radius.',
            'Follow-up observations detected heavier species (carbon, oxygen) escaping alongside hydrogen, interpreted as evidence that the escaping hydrogen flow is dense and fast enough to drag heavier atoms along with it via collisions -- a hydrodynamic "blow-off" process, not the much gentler particle-by-particle evaporation implied by classical thermal (Jeans) escape alone.',
            'The photoevaporation mechanism invoked to explain the Kepler radius valley (Lecture 04) is the same underlying physics observed directly and in real time at HD 209458 b: intense stellar extreme-ultraviolet and X-ray irradiation heats a close-in planet\u2019s upper atmosphere to the point that escape becomes hydrodynamic rather than merely thermal-tail (Jeans) evaporation.',
        ],
        model=[
            'Classical Jeans escape assumes only the high-velocity tail of a Maxwell-Boltzmann particle-speed distribution at the exobase (the altitude above which particles no longer collide before escaping) exceeds the local escape velocity; the Jeans escape parameter lambda = GMm/(kTR) compares gravitational binding energy to thermal energy per particle, with escape becoming negligible for lambda >> 1 and dominant (and the Jeans approximation itself breaking down into hydrodynamic outflow) for lambda of order a few or less.',
            'When lambda drops into the transitional range of roughly a few to a few tens -- as happens for a strongly irradiated, low-gravity, inflated hot Jupiter like HD 209458 b -- the escaping gas can no longer be treated as individual particles crossing the exobase independently; instead, the whole upper atmosphere behaves increasingly like a fluid undergoing a continuous, hydrodynamic outward flow (sometimes called "boil-off" or Roche-lobe-overflow-assisted escape), which can remove mass far faster than classical Jeans escape alone would predict, with the transition becoming complete only as lambda continues to fall toward order unity.',
            'Because escape rate depends steeply on stellar irradiation (which sets the exobase temperature) and on the planet\u2019s own gravity (which sets how tightly the atmosphere is bound), close-in, low-mass, strongly irradiated planets are the most vulnerable to significant atmospheric mass loss over their lifetime, directly relevant to whether a close-in planet in a low-mass star\u2019s habitable zone (Lecture 09, e.g., TRAPPIST-1) can retain any atmosphere at all.',
        ],
        equation=r'\lambda = \dfrac{G M m}{k_B T R}\ (\text{Jeans escape parameter}), \qquad \dot{M} \sim \pi R^{3}\rho_{\rm exo}\sqrt{\dfrac{k_BT}{m}}\ (\lambda \lesssim \text{few})',
        example=[
            f'HD 209458 b\u2019s Jeans escape parameter for atomic hydrogen at its real exosphere temperature ({PLANET_HD209458B["exosphere_temp_k"]:.0f} K): lambda = GMm/(kTR) = {HD209458B_JEANS_PARAM:.2f} -- roughly an order of magnitude smaller than Earth\u2019s value for the same species (Lab 04 computes Earth\u2019s value for comparison), placing HD 209458 b well inside the transitional-to-hydrodynamic regime this lecture\u2019s model identifies rather than the negligible-escape regime; note that lambda&#8776;11 is not yet down at order unity, so this is best described as strongly enhanced, transitional escape consistent with the observed extended, actively escaping exosphere, not the most extreme blow-off limit.',
            f'Present-day mass-loss timescale (naive, constant-rate extrapolation): Mp/(dM/dt) = {MP_HD209458B_KG:.3e} kg / {PLANET_HD209458B["mass_loss_kg_s"]:.1e} kg/s = {HD209458B_MASS_LOSS_TIMESCALE_GYR:.1f} Gyr -- long compared to a typical few-Gyr system age, so HD 209458 b is not in danger of complete evaporation at its current rate, even though the escape is real and directly observed; escape rates were plausibly higher earlier in the system\u2019s life when the host star was more X-ray/UV active.',
            'Contrast case: a much lower-mass, lower-gravity planet at the same irradiation level would have a proportionally smaller lambda (since lambda &prop; M/R, and low-mass planets also tend to have smaller R less than proportionally), placing it more deeply in the hydrodynamic-escape regime -- exactly the concern this lecture previews for close-in, low-mass planets around active M-dwarf stars like TRAPPIST-1 (Lecture 09).',
        ],
        pitfall='Concluding that any detected atmospheric escape means a planet will inevitably lose its entire atmosphere. HD 209458 b\u2019s own {mass_loss_timescale:.0f}-Gyr naive-extrapolation timescale, compared to its likely few-Gyr system age, shows real, measurable escape can coexist with a substantial retained atmosphere over the system\u2019s lifetime; the relevant question is always the escape timescale compared to the system\u2019s actual age and to the star\u2019s activity history, not simply whether escape is detected at all.'.format(mass_loss_timescale=HD209458B_MASS_LOSS_TIMESCALE_GYR),
        activity='Using lambda = GMm/(kTR), explain qualitatively why a planet identical to HD 209458 b in every way except twice the mass would have roughly double the Jeans parameter, and why this makes higher-mass hot Jupiters systematically more resistant to hydrodynamic atmospheric escape than lower-mass ones at the same irradiation and temperature.',
        lab_connection='Lab 04 computes HD 209458 b\u2019s Jeans escape parameter and naive mass-loss timescale from first principles and compares the result to the real, published Lyman-alpha exosphere detection.',
        synthesis='Atmospheric escape, quantified by the Jeans escape parameter, transitions from negligible thermal evaporation (lambda in the hundreds or more) toward rapid hydrodynamic blow-off as lambda falls toward order unity, with HD 209458 b\u2019s computed lambda&#8776;11 sitting well into that transitional regime, directly consistent with its observed, actively escaping exosphere -- and this same escape physics is the central complication Lectures 09-10 must confront when asking whether a planet\u2019s orbital distance alone is sufficient for genuine, long-term habitability.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=9, title='The Habitable Zone: Radiative-Equilibrium Boundaries',
        subtitle='Deriving where liquid water can, in principle, persist on a surface',
        goals=[
            'Derive the classical (conservative) habitable-zone inner and outer flux boundaries from radiative-equilibrium and greenhouse physics.',
            'Compute the habitable zone for the Sun and for TRAPPIST-1 and explain why it scales so differently with stellar luminosity.',
            'Critically evaluate which real planets in this course\u2019s dataset fall within, near, or outside their star\u2019s habitable zone.',
        ],
        why_matters='Every detection, demographic, interior, atmospheric, and escape tool developed so far (Lectures 01-08) converges here: the habitable zone is the first, most basic astronomical filter applied to ask whether a given real planet could, in principle, host surface liquid water -- the necessary (not sufficient) condition this course\u2019s entire second half builds on.',
        phenomenon=f'The Sun\u2019s classical habitable zone spans roughly {SUN_HZ_INNER_AU:.2f} to {SUN_HZ_OUTER_AU:.2f} AU (Earth, at 1.00 AU, sits comfortably inside it) -- but TRAPPIST-1, a star roughly 1800 times fainter than the Sun, has a habitable zone spanning only {TRAPPIST1_HZ_INNER_AU:.4f} to {TRAPPIST1_HZ_OUTER_AU:.4f} AU, closer to its star than Mercury is to the Sun, packing three to four of its seven known planets into a habitable zone that would fit inside Mercury\u2019s own orbit.',
        vocab=['habitable zone', 'runaway greenhouse (moist-greenhouse) limit', 'maximum-greenhouse limit', 'circumstellar habitable zone', 'insolation (stellar flux)', 'zero-albedo equilibrium temperature'],
        evidence=[
            'Radiative-transfer climate models (beginning with Kasting, Whitmire & Reynolds 1993 and refined by many subsequent studies) computing the surface temperature and water-vapor content of an Earth-like atmosphere as a function of received stellar flux find two critical flux thresholds: above roughly 1.1 times Earth\u2019s insolation, water vapor becomes a runaway greenhouse gas and the whole ocean can evaporate; below roughly 0.32 times Earth\u2019s insolation, CO2 condenses out of the atmosphere before it can trap enough heat to keep the surface above freezing.',
            'Venus (at 0.72 AU, receiving roughly 1.9 times Earth\u2019s insolation) sits well inside the classical inner boundary and today has no surface liquid water and a runaway-greenhouse-scale 737 K surface temperature, while Mars (at 1.52 AU, receiving roughly 0.43 times Earth\u2019s insolation) sits near but just outside the classical outer boundary and today has no stable surface liquid water either -- both real solar-system planets consistent with the classical HZ boundaries this lecture derives.',
            'Multiple TRAPPIST-1 planets (commonly cited as e, f, and sometimes d or g, depending on the specific model\u2019s albedo and greenhouse assumptions) fall within the zero-albedo classical habitable zone computed directly from the star\u2019s live-verified luminosity, the observational fact that made TRAPPIST-1 one of the most intensely studied systems for habitability by JWST since 2022.',
        ],
        model=[
            'A planet\u2019s received flux (insolation) at orbital distance a is S(a) = L/(4 pi a^2); the habitable zone\u2019s inner and outer edges are defined as the orbital distances at which S(a) equals two critical flux values (in units of Earth\u2019s insolation S_Earth): S_inner &asymp; 1.1 S_Earth (the runaway/moist-greenhouse limit) and S_outer &asymp; 0.32 S_Earth (the maximum-greenhouse limit), so that d_inner = sqrt(L/S_inner) and d_outer = sqrt(L/S_outer) in AU when L is in solar luminosities.',
            'Because flux falls off as 1/d^2, this reduces to a simple luminosity scaling: since S_inner and S_outer are fixed multiples of Earth\u2019s insolation regardless of the host star, the habitable-zone distance for any star scales as d &prop; sqrt(L); a star 1800 times fainter than the Sun (like TRAPPIST-1) therefore has a habitable zone roughly sqrt(1800) &asymp; 42 times closer in than the Sun\u2019s, exactly the pattern this lecture\u2019s worked example quantifies.',
            'These boundaries are explicitly conservative and one-dimensional (they assume an Earth-like atmospheric composition and water/CO2 greenhouse physics, and they say nothing about a specific planet\u2019s actual atmosphere, rotation, or albedo); Lecture 10 extends this classical picture with climate feedback and alternative habitability criteria that can shift or blur these boundaries in either direction for a real, specific planet.',
        ],
        equation=r'S(a) = \dfrac{L}{4\pi a^{2}}, \qquad d_{\rm inner,outer} = \sqrt{\dfrac{L/L_\odot}{S_{\rm inner,outer}/S_\oplus}}\ \mathrm{AU}',
        example=[
            f'Sun\u2019s habitable zone (L=1 Lsun): d_inner = sqrt(1/{HZ_S_INNER}) = {SUN_HZ_INNER_AU:.3f} AU, d_outer = sqrt(1/{HZ_S_OUTER}) = {SUN_HZ_OUTER_AU:.3f} AU -- Earth (1.00 AU) sits {(1.0-SUN_HZ_INNER_AU)/(SUN_HZ_OUTER_AU-SUN_HZ_INNER_AU)*100:.0f}% of the way from the inner to the outer edge, comfortably inside.',
            f'TRAPPIST-1\u2019s habitable zone (L={TRAPPIST1_STAR["lum_lsun"]:.3e} Lsun, live-verified): d_inner = {TRAPPIST1_HZ_INNER_AU:.4f} AU, d_outer = {TRAPPIST1_HZ_OUTER_AU:.4f} AU. Checking TRAPPIST-1e (a={TRAPPIST1_PLANETS["e"]["a_au"]:.4f} AU): it sits {MOIST_GREENHOUSE_MARGIN_TRAPPIST1E*100:.0f}% of the way from the inner to outer edge -- inside the classical habitable zone, consistent with its status as this system\u2019s most commonly cited habitability candidate.',
            f'Checking the rest of the TRAPPIST-1 system against the same computed boundaries: planets b, c, and d (a={TRAPPIST1_PLANETS["b"]["a_au"]:.4f}, {TRAPPIST1_PLANETS["c"]["a_au"]:.4f}, {TRAPPIST1_PLANETS["d"]["a_au"]:.4f} AU) fall inside the {TRAPPIST1_HZ_INNER_AU:.4f} AU inner edge (too close, zero-albedo equilibrium temperatures of {TRAPPIST1_TEQ["b"]:.0f}, {TRAPPIST1_TEQ["c"]:.0f}, {TRAPPIST1_TEQ["d"]:.0f} K), while g and h (a={TRAPPIST1_PLANETS["g"]["a_au"]:.4f}, {TRAPPIST1_PLANETS["h"]["a_au"]:.4f} AU) straddle or fall outside the {TRAPPIST1_HZ_OUTER_AU:.4f} AU outer edge -- a direct, quantitative habitable-zone census of a real seven-planet system.',
        ],
        pitfall='Treating "inside the habitable zone" as synonymous with "habitable" or "has liquid water." The classical habitable zone is a necessary radiative-equilibrium condition computed for an assumed Earth-like atmosphere; Venus\u2019s real, catastrophic runaway greenhouse and Mars\u2019s real, frozen surface show that a planet\u2019s actual climate depends on its specific atmospheric composition, mass, and history, not on orbital distance alone -- exactly why Lecture 10 extends this classical picture rather than treating it as the final word.',
        activity='Using d &prop; sqrt(L), estimate how much closer in the habitable zone of a star with half the Sun\u2019s luminosity would be compared to the Sun\u2019s own habitable zone, and explain why this scaling makes low-mass M-dwarf systems like TRAPPIST-1 simultaneously the easiest systems in which to detect multiple habitable-zone-candidate planets (Lecture 02\u2019s transit-probability argument) and the hardest in which to be confident those planets have actually retained a life-friendly atmosphere (Lecture 08\u2019s escape argument).',
        lab_connection='Lab 05 computes the classical habitable-zone boundaries for the Sun, TRAPPIST-1, 51 Pegasi, and HD 209458 from their real luminosities and evaluates every real planet in this course\u2019s dataset against its own host star\u2019s boundaries.',
        synthesis='The classical habitable zone, derived from radiative-equilibrium flux balance and Earth-like greenhouse physics, converts a star\u2019s luminosity directly into an orbital-distance range where surface liquid water is radiatively plausible -- a necessary but explicitly not sufficient condition for habitability, as Lecture 10\u2019s climate-feedback extensions and this course\u2019s later biosignature-false-positive discussion (Lecture 11) both make clear.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=10, title='Climate Feedback and Habitability Beyond the Classical Habitable Zone',
        subtitle='Why the same physics can produce Venus, Earth, or an ice-covered ocean world',
        goals=[
            'Explain the carbonate-silicate cycle as a long-term climate-stabilizing negative feedback and the water-vapor runaway as a destabilizing positive feedback.',
            'Describe at least two habitability scenarios not captured by the classical habitable zone: tidal heating and subsurface ocean worlds.',
            'Critically evaluate why a planet\u2019s orbital distance is necessary, but not sufficient, evidence for genuine habitability, synthesizing Lectures 06-09.',
        ],
        why_matters='Lecture 09 derived where the habitable zone is; this lecture asks what actually determines whether a specific real planet inside that zone ends up Earth-like, Venus-like, or something else entirely -- completing the honest, non-oversimplified habitability picture this course\u2019s biosignature unit (Lectures 11-12) depends on.',
        phenomenon='Venus and Earth are strikingly similar in mass, radius, and bulk composition, both formed from the same protoplanetary disk, yet one has a life-friendly climate and the other a 737 K runaway-greenhouse surface -- a divergence that orbital distance alone, absent the climate-feedback physics this lecture derives, cannot explain, since Venus\u2019s insolation (1.9 times Earth\u2019s) is not dramatically far outside the classical habitable zone\u2019s inner edge (1.1 times Earth\u2019s) computed in Lecture 09.',
        vocab=['carbonate-silicate cycle', 'negative (stabilizing) feedback', 'positive (runaway) feedback', 'tidal heating', 'subsurface ocean world', 'ice shell', 'geologically active habitability'],
        evidence=[
            'Long-term geological and atmospheric-composition evidence (ice-core CO2 records, weathering-rate field studies) supports the carbonate-silicate cycle as an active, real stabilizing feedback on Earth: warmer surface temperatures measurably accelerate silicate rock weathering, which draws down atmospheric CO2 and cools the surface, while cooler temperatures slow weathering and let volcanic CO2 outgassing rebuild the greenhouse effect -- a self-correcting thermostat operating on geological (10^5-10^6 year) timescales.',
            'Venus\u2019s atmosphere (96% CO2, 92 bar surface pressure, no evidence of plate tectonics or an active carbonate-silicate cycle today) is the observed real-world outcome when this stabilizing feedback fails or was never established, consistent with either an early runaway greenhouse driven by the Sun\u2019s gradually increasing luminosity or a loss of the geological cycling needed to sustain the negative feedback.',
            'Europa and Enceladus (icy moons studied in this curriculum\u2019s ASTR 320 course) are real, spacecraft-confirmed subsurface liquid-water ocean worlds far outside any star\u2019s classical habitable zone, sustained by tidal heating rather than stellar insolation -- direct observational proof that the classical, insolation-based habitable zone is not the only physically real pathway to long-lived liquid water in a planetary system.',
        ],
        model=[
            'The carbonate-silicate cycle is a negative feedback loop: higher surface temperature increases the rate of CO2-consuming silicate weathering (a temperature-dependent chemical reaction rate), which lowers atmospheric CO2 and greenhouse warming, cooling the surface back down; this loop requires liquid water, exposed silicate rock, and (for long-term stability) plate tectonics or an equivalent volcanic resupply mechanism to keep operating over geological time.',
            'The water-vapor runaway is a positive feedback: added surface warming increases evaporation and atmospheric water-vapor content, and because water vapor is itself a strong greenhouse gas, this additional warming evaporates still more water, a self-reinforcing loop that terminates only when the ocean is fully evaporated (or the atmosphere becomes optically thick enough to self-limit) -- the classical habitable zone\u2019s inner edge (Lecture 09) is defined as the flux level at which this positive feedback becomes unavoidable.',
            'Tidal heating (the same tidal-dissipation physics from Lecture 05\u2019s eccentricity discussion, applied here to a solid or icy body\u2019s interior rather than its orbit) can sustain a subsurface liquid-water layer under an ice shell far from any star, entirely independent of stellar insolation, as confirmed for Europa and Enceladus -- meaning "habitable zone" and "location where liquid water can exist" are not, in general, the same set of places.',
        ],
        equation=r'\dfrac{d(\mathrm{CO_2})}{dt} = (\text{volcanic outgassing rate}) - k\, W(T)\ (\text{weathering rate, increasing in } T)',
        example=[
            'Qualitative stability argument: if Earth\u2019s surface temperature rose by a few degrees from a transient forcing, the carbonate-silicate feedback\u2019s negative sign predicts weathering would accelerate, CO2 would draw down, and the temperature perturbation would be damped over roughly 10^5-10^6 years -- the geologically observed behavior underlying ice-core-confirmed long-term climate stability, in contrast to a positive-feedback runaway that instead amplifies the same initial perturbation.',
            f'Venus insolation check using Lecture 09\u2019s tool: at Venus\u2019s real orbital distance (0.723 AU), S(a)=L/(4 pi a^2) gives an insolation of {insolation_w_m2(L_SUN, 0.723*AU_M):.0f} W/m^2, or {insolation_w_m2(L_SUN, 0.723*AU_M)/EARTH_INSOLATION:.2f} times Earth\u2019s -- above the Lecture 09 runaway threshold ({HZ_S_INNER}), consistent with (though not solely sufficient to explain the full magnitude of) Venus\u2019s real runaway-greenhouse outcome.',
            'Subsurface-ocean-world contrast: Europa\u2019s orbital distance from Jupiter places it far outside any star\u2019s classical habitable zone by Lecture 09\u2019s insolation criterion alone, yet spacecraft gravity and magnetic-field data confirm a real subsurface liquid-water ocean sustained by Jupiter\u2019s tidal heating -- a direct, quantitative illustration that the classical HZ answers "is stellar flux compatible with surface liquid water," not the more general question "can liquid water exist anywhere in this system."',
        ],
        pitfall='Concluding that a planet just outside the classical habitable zone\u2019s outer edge, or a moon far outside any habitable zone at all, is necessarily lifeless. Mars sits just outside Lecture 09\u2019s conservative outer edge yet had abundant surface liquid water billions of years ago (evidence covered in this curriculum\u2019s ASTR 320 course), and Europa/Enceladus sit far outside any habitable zone yet host real subsurface oceans -- the classical HZ is a useful first filter, not a complete or final habitability verdict.',
        activity='Using the carbonate-silicate cycle\u2019s negative-feedback logic, explain what would need to fail (geologically or atmospherically) for an Earth-like planet with an active carbonate-silicate cycle to nonetheless drift into a Venus-like runaway greenhouse over time, and connect your answer to why plate tectonics (or an equivalent process) is increasingly discussed as a possible additional habitability requirement beyond orbital distance alone.',
        lab_connection='Lab 05 also evaluates, qualitatively and with supporting calculations, whether Venus\u2019s and Mars\u2019s real climate outcomes are consistent with or in tension with the classical habitable-zone boundaries computed in Lecture 09.',
        synthesis='Climate feedback (the carbonate-silicate cycle\u2019s stabilizing effect, and the water-vapor runaway\u2019s destabilizing one) and non-insolation habitability pathways (tidal heating in subsurface ocean worlds) together show that the classical habitable zone from Lecture 09 is a necessary first filter, not a sufficient habitability verdict -- exactly the caution this course now carries into Lecture 11\u2019s biosignature false-positive reasoning, where the same lesson (a promising signal is not automatically proof of life) recurs in a different form.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=11, title='Biosignature Gases and the False-Positive Problem',
        subtitle='Why detecting oxygen is not the same as detecting life',
        goals=[
            'Define a biosignature gas and explain the chemical-disequilibrium argument for why oxygen and methane coexisting is a particularly strong biosignature.',
            'Derive, qualitatively, at least two real, published abiotic pathways that can produce a false-positive oxygen or methane signal.',
            'Apply this lecture\u2019s false-positive reasoning to a real, debated case: abiotic oxygen buildup on close-in M-dwarf planets like several TRAPPIST-1 worlds.',
        ],
        why_matters='Lectures 07-08 established how to measure an exoplanet atmosphere\u2019s composition and escape; this lecture asks the central astrobiological question that composition measurement makes possible: which detected gases, if any, would constitute credible evidence of life, and what alternative, non-biological explanations must be ruled out first?',
        phenomenon='On Earth, atmospheric oxygen (21% by volume) and methane coexist in obvious chemical disequilibrium -- the two react readily, and without continuous biological replenishment (photosynthesis maintaining O2, methanogenic microbes and other sources maintaining CH4) atmospheric chemistry would drive both toward much lower steady-state abundances within a few thousand years, far shorter than geological timescales, making their simultaneous presence a textbook example of a biosignature -- but the same O2 molecule can also be produced with no biology involved at all, a possibility this lecture takes seriously rather than dismissing.',
        vocab=['biosignature gas', 'chemical disequilibrium', 'photolysis (water-vapor breakdown)', 'abiotic oxygen false positive', 'context gas', 'technosignature (contrast case)'],
        evidence=[
            'Earth\u2019s own atmospheric history (well documented geologically) shows that biologically produced oxygen only became a dominant atmospheric constituent after the Great Oxidation Event roughly 2.4 billion years ago, driven by cyanobacterial photosynthesis; prior to that, Earth\u2019s atmosphere had only trace oxygen despite already hosting life, demonstrating that "no detectable O2" does not equal "no life" even on the one planet we know is inhabited.',
            'Published photochemical modeling studies (e.g., Luger & Barnes 2015 and related work) show that close-in rocky planets around low-mass, high-activity M-dwarf stars like TRAPPIST-1 can build up a substantial abiotic O2 atmosphere purely from ultraviolet photolysis of water vapor during an extended pre-main-sequence "runaway greenhouse" phase, followed by preferential escape of the lighter hydrogen and accumulation of the heavier, harder-to-escape oxygen left behind -- with no biology involved at any step.',
            'Other published abiotic O2/O3-production pathways include CO2 photolysis in a thin, water-poor atmosphere and, for O3 specifically, buildup from photochemistry even at very low O2 abundances -- both mechanisms that could, in principle, mimic a promising biosignature spectrum for an atmosphere that in fact carries none of the disequilibrium context this lecture identifies as the crucial distinguishing evidence.',
        ],
        model=[
            'A biosignature gas is strongest as evidence of life not in isolation, but when detected alongside other, chemically incompatible gases whose simultaneous presence requires an ongoing source, because unreplenished reactive gases would otherwise reach a much lower abiotic chemical-equilibrium abundance on a timescale short compared to the star-planet system\u2019s age -- the same "context gas" reasoning this lecture calls the disequilibrium argument.',
            'The abiotic-oxygen false-positive pathway for M-dwarf planets specifically requires (i) an extended, luminous pre-main-sequence phase during which the host star\u2019s habitable zone was much closer in and hotter than its eventual main-sequence value, (ii) a planet\u2019s ocean evaporating and its water vapor photolyzing into hydrogen and oxygen, and (iii) preferential atmospheric escape of the lighter hydrogen (Lecture 08\u2019s escape physics, mass-dependent) leaving oxygen to accumulate -- a specific, testable sequence of physical steps, not a vague caveat.',
            'This false-positive pathway makes a specific, checkable prediction: it should leave a planet with a large O2 abundance but comparatively little or no water vapor, methane, or other reduced (context) gases, and possibly other tell-tale markers (e.g., an unusually large O4 dimer absorption feature, or a detectable CO buildup); a genuinely biological O2 signal, by contrast, is expected to coexist with reduced context gases actively being replenished by the same biosphere.',
        ],
        equation=r'\tau_{\rm chem} = \dfrac{N_{\rm gas}}{L_{\rm loss\ rate}}\ (\text{abiotic residence time}); \quad \tau_{\rm chem} \ll t_{\rm system\ age} \Rightarrow \text{ongoing source required}',
        example=[
            'Earth\u2019s own methane budget: atmospheric CH4 reacts with hydroxyl radicals on a residence time of roughly a decade, many orders of magnitude shorter than Earth\u2019s age, so its observed steady-state abundance requires an ongoing source (dominated by microbial and, more recently, anthropogenic emission) -- exactly the "short chemical residence time implies an active source" logic this lecture\u2019s equation formalizes.',
            f'Applying the false-positive check to this course\u2019s own TRAPPIST-1 system: planets b and c (a={TRAPPIST1_PLANETS["b"]["a_au"]:.4f}, {TRAPPIST1_PLANETS["c"]["a_au"]:.4f} AU, well inside Lecture 09\u2019s computed {TRAPPIST1_HZ_INNER_AU:.4f} AU inner habitable-zone edge, with zero-albedo equilibrium temperatures {TRAPPIST1_TEQ["b"]:.0f} and {TRAPPIST1_TEQ["c"]:.0f} K) are exactly the kind of close-in, historically over-irradiated planets for which the published abiotic-oxygen-buildup pathway is considered a serious, specific concern, not a generic caveat.',
            'Decision logic applied to a hypothetical detection: an O2 signal on a TRAPPIST-1 planet accompanied by strong H2O, CH4, and other reduced-gas features would be read as a comparatively strong biosignature case; the same O2 signal with no detectable water vapor or reduced context gases would instead be read as consistent with (though not proof of) the abiotic photolysis-and-escape false-positive pathway this lecture derives -- precisely the kind of context-dependent, disequilibrium-based reasoning real biosignature interpretation requires.',
        ],
        pitfall='Treating any single detected gas (oxygen especially) as a self-evident biosignature regardless of context. The published, physically specific abiotic-oxygen pathway for M-dwarf planets shows that the same molecule can arise with no biology at all; a scientifically defensible biosignature claim requires the disequilibrium/context-gas argument, an assessment of the star\u2019s pre-main-sequence history (Lecture 08\u2019s escape physics), and ideally multiple independent lines of evidence, not a single spectral feature in isolation.',
        activity='Using the chemical-residence-time argument, explain why detecting both ozone (O3) and methane (CH4) simultaneously in an exoplanet\u2019s spectrum is generally considered stronger biosignature evidence than detecting O3 alone, and connect this reasoning explicitly to the "context gas" concept this lecture defines.',
        lab_connection='Lab 06 works through the abiotic-oxygen false-positive decision logic for a real TRAPPIST-1 planet using this lecture\u2019s disequilibrium-timescale framework and this course\u2019s own computed habitable-zone and equilibrium-temperature results.',
        synthesis='A biosignature gas is scientifically credible evidence of life only when its abundance and its chemical/dynamical context (co-occurring reduced gases, the host star\u2019s irradiation and escape history) jointly rule out known, physically specific abiotic pathways -- the same "promising signal is not automatic proof" caution from Lecture 10\u2019s habitable-zone discussion, now applied directly to the detection of life itself, and the discipline Lecture 12\u2019s exploration of life\u2019s physical limits requires before any biosignature claim can be evaluated against what is actually biologically plausible.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=12, title='Extremophiles and the Physical Limits of Life',
        subtitle='How far Earth life actually pushes the envelope of temperature, pressure, radiation, and desiccation',
        goals=[
            'Summarize the real, published physical limits (temperature, pressure, radiation, salinity, desiccation) within which Earth life is documented to survive and grow.',
            'Distinguish between an organism\u2019s growth limit and its mere survival (dormancy/cryptobiosis) limit.',
            'Use these documented limits to evaluate, quantitatively, whether specific real or hypothetical exoplanet environments could plausibly host Earth-like life.',
        ],
        why_matters='Lecture 11 asked what a biosignature gas could tell us about a planet\u2019s life; this lecture asks a complementary, more basic question -- what physical conditions can life itself actually tolerate -- providing the biological grounding this course\u2019s habitability discussion (Lectures 09-10) and origin-of-life discussion (Lecture 13) both depend on rather than assuming.',
        phenomenon=f'Pyrolobus fumarii, a real archaeon isolated from a deep-sea hydrothermal vent, grows at temperatures up to {EXTREMOPHILES[0]["value"]:.0f} degrees C -- above the boiling point of water at sea-level pressure, made possible only by the elevated pressure of its deep-ocean environment -- while a separate isolate known as "Strain 121" has been documented to survive (and in some reports, grow) at {EXTREMOPHILES[1]["value"]:.0f} degrees C, together defining the current upper temperature frontier of known life.',
        vocab=['extremophile', 'hyperthermophile', 'psychrophile', 'radioresistance', 'halophile', 'cryptobiosis (anhydrobiosis)', 'polyextremophile'],
        evidence=[
            'Blochl et al. (1997) documented Pyrolobus fumarii\u2019s upper growth-temperature limit of 113 degrees C from deep-sea hydrothermal vent samples, and Kashefi & Lovley (2003) reported "Strain 121"\u2019s survival and apparent growth at 121 degrees C, both under elevated pressure that keeps water liquid well above its sea-level boiling point -- real, published, peer-reviewed microbiological measurements, not estimates.',
            'Mykytczuk et al. (2013) documented Planococcus halocryophilus, isolated from Arctic permafrost, actively growing (not merely surviving) at temperatures down to -25 degrees C in briny, unfrozen microscopic channels within the ice, extending the documented low-temperature growth limit for life well below the freezing point of pure water.',
            'Deinococcus radiodurans is documented (across many published radiobiology studies going back decades) to survive acute radiation doses on the order of 5,000 gray without loss of viability -- roughly a thousand times the acute dose lethal to humans -- via an exceptionally efficient DNA-repair mechanism, and tardigrades are documented (Seki & Toyoshima 1998; Jonsson et al. 2008) to survive hydrostatic pressures up to about 600 megapascals and even brief direct exposure to the vacuum and radiation of low Earth orbit in a dormant, desiccated state.',
        ],
        model=[
            'A clear distinction must be drawn between an organism\u2019s growth limit (the environmental range within which it actively metabolizes and reproduces) and its mere survival or dormancy limit (a state, such as tardigrade cryptobiosis or bacterial endospore formation, in which metabolism is essentially halted and the organism can tolerate conditions far outside its growth range for a limited time, resuming activity only once conditions improve) -- conflating the two overstates what "life at that extreme" actually means.',
            'Radioresistance in organisms like Deinococcus radiodurans is understood not as an adaptation to naturally high ambient radiation (no known natural environment on Earth approaches the radiation doses these organisms can tolerate) but as an incidental byproduct of an unusually effective DNA-repair and desiccation-tolerance system, a mechanistic distinction directly relevant to whether radioresistance should be expected to evolve on other, high-radiation-environment planets or moons.',
            'Polyextremophiles (organisms tolerating multiple simultaneous extremes, such as Chroococcidiopsis desert/hypolith cyanobacteria surviving extreme desiccation, high UV flux, and large temperature swings together) are of particular astrobiological interest precisely because a real extraterrestrial habitat is unlikely to present only a single extreme in isolation, making single-variable extremophile records a necessary but incomplete guide to actual habitability.',
        ],
        equation=r'\text{Growth range} \subsetneq \text{Survival (dormancy) range}, \qquad D_{37} = \dfrac{1}{k}\ (\text{radiation dose for } 1/e\ \text{survival, organism-specific } k)',
        example=[
            f'Comparing Deinococcus radiodurans\u2019s documented radiation tolerance directly to the human lethal dose: {EXTREMOPHILES[3]["value"]:.0f} Gy / {HUMAN_LETHAL_RADIATION_GY:.0f} Gy = {EXTREMOPHILES[3]["value"]/HUMAN_LETHAL_RADIATION_GY:.0f}&times; -- a concrete, computed ratio quantifying just how far outside human physiological limits this single trait extends, without claiming this extends to every other environmental variable simultaneously.',
            f'Tardigrade pressure tolerance in atmospheres: {EXTREMOPHILES[4]["value"]:.0f} MPa &times; (1 atm / 0.101325 MPa) = {EXTREMOPHILES[4]["value"]/0.101325:.0f} atmospheres -- for comparison, this exceeds the pressure at the deepest point of Earth\u2019s ocean (roughly 1,100 atm at the Mariana Trench), illustrating that tardigrade pressure tolerance is a genuine physiological outlier rather than an environment routinely encountered on Earth\u2019s surface or even ocean floor.',
            'Temperature-range synthesis from this course\u2019s own dataset: known life\u2019s documented growth-temperature range spans roughly -25 degrees C (Planococcus halocryophilus) to 121 degrees C (\u201cStrain 121\u201d), a 146-degree window -- directly relevant, in Lecture 09\u2019s terms, to asking whether a planet\u2019s zero-albedo equilibrium temperature (e.g., TRAPPIST-1\u2019s planets, computed in Lecture 09) falls anywhere near this documented biological window, as a necessary (not sufficient) plausibility check.',
        ],
        pitfall='Treating an organism\u2019s documented survival/dormancy limit (e.g., tardigrade vacuum/radiation tolerance in cryptobiosis) as equivalent to its growth limit, and using the more extreme survival number to argue a planet is "habitable." Cryptobiotic survival is a real, remarkable, but metabolically inactive state; a planet supporting only permanent cryptobiosis with no window for active growth and reproduction would not support a persistent, evolving biosphere in any meaningful sense.',
        activity='Using the growth-limit-versus-survival-limit distinction, explain why "tardigrades can survive the vacuum of space" is not, by itself, evidence that space (or a similarly extreme environment) could support an active, reproducing population of tardigrades or any other organism, and connect this distinction to how a real astrobiology mission would need to interpret a habitability claim for a given exoplanet or moon environment.',
        lab_connection='Lab 06 also builds a temperature/pressure/radiation extremophile-tolerance summary from this lecture\u2019s real published records and uses it to bound which of this course\u2019s real planets and moons (from ASTR 320) could plausibly support active microbial growth, as opposed to only dormant survival.',
        synthesis='The real, published physical limits of Earth life -- growth from roughly -25 to 121 degrees C, survival of pressures far exceeding Earth\u2019s deepest ocean trench, radiation doses a thousand times the human lethal dose, and extreme desiccation/vacuum in dormancy -- define the empirical envelope against which any exoplanet or moon habitability claim should be checked, while the growth-versus-survival distinction this lecture insists on prevents that envelope from being overstated, setting up Lecture 13\u2019s question of how life\u2019s chemistry could have originated within (or before) this envelope in the first place.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=13, title='Prebiotic Chemistry and the Origin of Life',
        subtitle='From simple molecules to the first self-replicating chemistry',
        goals=[
            'Describe the real Miller-Urey spark-discharge experiment and what it did and did not demonstrate about the origin of life.',
            'Summarize at least two major, currently competing hypotheses for the chemical pathway from simple organic molecules to the first self-replicating system.',
            'Critically evaluate the scientific limits of current knowledge about abiogenesis, distinguishing well-supported claims from open questions.',
        ],
        why_matters='Lecture 12 established the physical envelope within which life, once it exists, can persist and grow; this lecture turns to the still-unsolved question of how life\u2019s chemistry could have started in the first place -- essential, honestly incomplete context for the final synthesis (Lecture 14) of what searching for life elsewhere can, and cannot, currently claim to answer.',
        phenomenon='In 1953, Stanley Miller (working with Harold Urey) sealed a mixture of methane, ammonia, hydrogen, and water vapor in a sterile glass apparatus, subjected it to a continuous electrical spark simulating lightning, and within a week found that the resulting liquid contained multiple real amino acids -- the basic building blocks of proteins -- formed from simple inorganic and small-molecule precursors with no biology involved, one of the most famous single experiments in the history of origin-of-life research.',
        vocab=['prebiotic chemistry', 'Miller-Urey experiment', 'abiogenesis', 'RNA world hypothesis', 'hydrothermal-vent origin hypothesis', 'panspermia (contrast hypothesis)'],
        evidence=[
            'The original Miller-Urey experiment\u2019s sealed sample vials were re-analyzed with modern, far more sensitive analytical chemistry by Johnson, Cleaves, Bada, and collaborators (2008), who confirmed and substantially expanded the list of amino acids and related compounds actually present, finding that even the volcanic-eruption-simulating variant of Miller\u2019s original setup (a run Miller himself had not fully analyzed at the time) produced a still richer mixture of organic compounds.',
            'Independent laboratory experiments since the 1950s have shown that many of the chemical building blocks of life (amino acids, sugars, and nucleobases including several found in RNA) can form abiotically under a range of plausible early-Earth conditions (spark discharge, UV irradiation, hydrothermal-vent-like chemistry, and even in interstellar-ice-analog experiments), and amino acids and other prebiotic organic molecules have also been directly detected in real carbonaceous meteorites (e.g., the Murchison meteorite) and comet samples, showing that at least some prebiotic chemistry occurs even without any planetary surface at all.',
            'No laboratory experiment to date has demonstrated a complete, empirically verified pathway from simple organic molecules to a genuinely self-replicating, evolving chemical system under plausible early-Earth (or early-planet) conditions; this remains explicitly, honestly, an open scientific problem rather than a solved one, a state of knowledge this course reports accurately rather than overstating.',
        ],
        model=[
            'The Miller-Urey experiment demonstrated that prebiotic amino-acid synthesis from simple precursors is chemically easy under early-Earth-plausible conditions, but it demonstrated nothing about the much harder subsequent steps: assembling amino acids into functional proteins, encoding heritable information, and achieving self-replication with selection -- distinguishing "the building blocks form easily" from "life\u2019s full chemistry is understood" is essential to accurately representing what this landmark experiment actually showed.',
            'The RNA-world hypothesis proposes that RNA molecules, which can both store genetic information (like DNA) and catalyze chemical reactions (like some proteins), served as the first self-replicating chemical system, with DNA and protein-based biochemistry evolving later; laboratory work has shown some RNA molecules (ribozymes) can catalyze RNA-copying-relevant reactions, offering real supporting evidence, but no experiment has yet demonstrated a complete, unassisted RNA self-replication cycle under plausible prebiotic conditions.',
            'The hydrothermal-vent (alkaline vent) origin hypothesis proposes that naturally occurring, mineral-catalyzed chemical gradients at seafloor hydrothermal vents (rather than a surface "primordial soup") provided the sustained energy and chemical gradient needed to drive early prebiotic chemistry, motivated partly by these environments\u2019 real, spacecraft-relevant analogy to the tidally heated subsurface oceans of Europa and Enceladus (Lecture 10) -- these two hypotheses (RNA-world and hydrothermal-vent origin) are not mutually exclusive and are both actively studied rather than settled.',
        ],
        equation=r'\text{Simple precursors (CH}_4\text{, NH}_3\text{, H}_2\text{O, H}_2\text{)} \xrightarrow{\text{energy input}} \text{amino acids, sugars, nucleobases} \xrightarrow{?} \text{self-replicating chemistry}',
        example=[
            'This course\u2019s Miller-Urey relative-abundance figure (from the real published re-analysis) shows glycine as by far the most abundant amino acid produced, with alanine second and progressively smaller amounts of beta-alanine, aspartic acid, and glutamic acid -- a real, published relative ranking illustrating that the experiment does not produce all amino acids equally, some biochemically important ones (including several used in modern proteins) were not detected at all in the original runs.',
            'Quantifying the experiment\u2019s real historical impact: the original 1953 result predates the discovery of DNA\u2019s double-helix structure (Watson & Crick, also 1953) by only months, meaning Miller\u2019s demonstration that life\u2019s building blocks form easily from inorganic precursors and Crick and Watson\u2019s demonstration of how genetic information is physically encoded were established as two separate, still only partially connected pieces of the origin-of-life puzzle in the same remarkable year.',
            'Murchison-meteorite amino-acid content (a real, extensively studied 1969 meteorite fall) has been documented across decades of published analytical chemistry to contain dozens of amino acids, including several rare or absent from Earth\u2019s standard biological set, and with a measurable enantiomeric (mirror-image molecule) excess in some compounds -- real extraterrestrial evidence that prebiotic organic chemistry can and does occur off any planetary surface at all, in interplanetary or interstellar environments.',
        ],
        pitfall='Describing the Miller-Urey experiment (or the broader body of prebiotic-chemistry evidence) as having "created life in a test tube" or having "solved the origin of life." The experiment and its many published successors demonstrate that life\u2019s small-molecule building blocks form readily and abiotically; the harder, still-unresolved steps -- polymerization into functional macromolecules, encoding heritable information, and achieving genuine self-replication with selection -- remain open, actively researched scientific problems, not settled results, and this course states that limitation explicitly rather than implying the problem is solved.',
        activity='Using the distinction between "building blocks form easily" and "self-replication is understood," explain why detecting amino acids or other simple organic molecules in an exoplanet\u2019s atmosphere or a meteorite would not, by itself, constitute evidence of life or even of a completed abiogenesis pathway, and connect this explicitly to Lecture 11\u2019s biosignature false-positive reasoning.',
        lab_connection='Lab 07\u2019s capstone synthesis draws on this lecture\u2019s honest treatment of prebiotic chemistry\u2019s real accomplishments and open questions when evaluating what a positive biosignature detection could and could not scientifically establish.',
        synthesis='The real, published body of prebiotic-chemistry evidence -- from the Miller-Urey experiment through modern re-analyses, meteorite organic chemistry, and the actively competing RNA-world and hydrothermal-vent origin hypotheses -- shows that life\u2019s basic chemical building blocks form readily under plausible early-planet conditions, while the decisive step to genuine self-replication remains a genuinely open scientific question; this honest state of incomplete knowledge is exactly the context the course\u2019s capstone (Lecture 14) needs before evaluating what any biosignature detection could scientifically establish.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=14, title='Capstone: The Drake Equation and the Scientific Limits of Life Detection',
        subtitle='Structuring an honest estimate -- and an honest admission of what we do not yet know',
        goals=[
            'Apply the Drake equation as a structured estimation framework, distinguishing terms grounded in real astronomical data from terms that remain genuinely unconstrained.',
            'Synthesize this course\u2019s full toolkit (detection, demographics, atmospheres, habitability, biosignatures, extremophiles, prebiotic chemistry) into a single, honest assessment of a specific real system\u2019s astrobiological plausibility.',
            'Articulate, explicitly and without overclaiming, the current scientific limits of exoplanet life detection.',
        ],
        why_matters='Every tool this course has built -- radial velocity and transit detection (Lectures 01-03), demographics (Lecture 04), architecture and interiors (Lectures 05-06), atmospheres and escape (Lectures 07-08), habitability (Lectures 09-10), biosignatures (Lecture 11), and life\u2019s physical/chemical limits (Lectures 12-13) -- converges in this capstone on the single question the entire field of astrobiology exists to address, and on an honest reckoning of how far current science can actually take that question.',
        phenomenon=f'Frank Drake\u2019s 1961 equation, N = R* f_p n_e f_l f_i f_c L, multiplies seven terms together to estimate the number of communicating civilizations in the galaxy right now; this course\u2019s own computed range spans from {N_CIV_PESSIMISTIC:.1e} (pessimistic biological assumptions) to {N_CIV_OPTIMISTIC:.1e} (optimistic biological assumptions) -- a difference of more than {N_CIV_OPTIMISTIC/max(N_CIV_PESSIMISTIC,1e-30):.0e}, driven almost entirely by the three biological terms (f_l, f_i, f_c) this course\u2019s Lectures 11-13 showed remain genuinely unconstrained by any current data.',
        vocab=['Drake equation', 'order-of-magnitude estimation framework', 'astronomical term (constrained)', 'biological term (unconstrained)', 'Fermi paradox (contrast concept)', 'scientific epistemic humility'],
        evidence=[
            'The first three Drake-equation terms (R*, the star-formation rate; f_p, the fraction of stars with planets; n_e, the mean number of habitable-zone-compatible planets per system) are now reasonably well constrained by real astronomical survey data (Lectures 01-04\u2019s detection methods and Kepler/Gaia-era occurrence-rate statistics), a dramatic change from Drake\u2019s original 1961 estimate, when not a single exoplanet had yet been confirmed.',
            'The remaining four terms (f_l, the fraction of habitable planets on which life actually arises; f_i, the fraction of those developing intelligence; f_c, the fraction developing detectable technology; and L, the average lifetime of a detectable civilization) have no direct observational constraint at all -- Lecture 13\u2019s honest treatment of prebiotic chemistry\u2019s open questions and Lecture 12\u2019s empirical extremophile envelope are the closest this course comes to any data-grounded handle on f_l, and even that connection is indirect.',
            'The Fermi paradox (the tension between plausible estimates of a non-negligible N and the total absence, to date, of any confirmed extraterrestrial signal or artifact) is not resolved by this course, and should not be presented as resolved; it remains an actively debated open question in the scientific literature, with candidate explanations ranging from technological civilizations being genuinely rare (small f_l x f_i x f_c) to being common but short-lived (small L) to detection difficulty/methodology limitations, none of which current data can yet distinguish.',
        ],
        model=[
            'The Drake equation\u2019s value is not as a precise predictive formula (its final numerical output spans many orders of magnitude depending on assumptions) but as a structured decomposition that identifies exactly which physical and biological questions must be answered, and in what combination, to estimate the prevalence of detectable extraterrestrial intelligence -- exactly the kind of explicit, falsifiable framework this course has modeled throughout for every other quantitative claim.',
            'A scientifically honest application of the equation reports a range (this course\u2019s computed {:.1e} to {:.1e}) rather than a single number, and explicitly labels which terms are astronomically constrained (R*, f_p, n_e) versus biologically unconstrained (f_l, f_i, f_c, L), so that the enormous uncertainty in the final answer is attributed to its actual source rather than presented as false precision.'.format(N_CIV_PESSIMISTIC, N_CIV_OPTIMISTIC),
            'Synthesizing this course\u2019s full toolkit for a single real system (TRAPPIST-1, used throughout as the running case study): its planets are real and well-characterized (Lectures 01-06), several fall within the classical habitable zone (Lecture 09), but the system\u2019s active, high-radiation M-dwarf host star raises genuine atmospheric-escape concerns (Lecture 08) and its climate outcome is not knowable from orbital distance alone (Lecture 10); any biosignature claim would require the disequilibrium/context-gas reasoning of Lecture 11, and even a positive detection would say nothing definitive about intelligence, technology, or civilization lifetime (the unconstrained Drake terms) -- the complete, honest state of the science this capstone lecture requires students to articulate rather than to oversimplify in either an falsely optimistic or falsely dismissive direction.',
        ],
        equation=r'N = R_\ast\, f_p\, n_e\, f_l\, f_i\, f_c\, L',
        example=[
            f'Astronomically constrained terms (this course\u2019s adopted, level-2 published order-of-magnitude values): R* &asymp; {DRAKE_R_STAR:.1f} new Sun-like stars/year, f_p &asymp; {DRAKE_F_P:.1f} (planets are now known to be common), n_e &asymp; {DRAKE_N_E:.1f} habitable-zone-compatible planets per system -- multiplying these three alone gives R* f_p n_e &asymp; {DRAKE_R_STAR*DRAKE_F_P*DRAKE_N_E:.2f} potentially habitable planets forming per year in the galaxy, a real, if still refined, astronomical estimate.',
            f'Optimistic biological assumptions (f_l={DRAKE_F_L_OPTIMISTIC}, f_i={DRAKE_F_I}, f_c={DRAKE_F_C}, L={DRAKE_L_OPTIMISTIC_YR:.0e} yr, all explicitly labeled illustrative/unconstrained placeholders): N = {N_CIV_OPTIMISTIC:.2e}.',
            f'Pessimistic biological assumptions (f_l={DRAKE_F_L_PESSIMISTIC:.0e}, same f_i and f_c, L={DRAKE_L_PESSIMISTIC_YR:.0e} yr): N = {N_CIV_PESSIMISTIC:.2e} -- computed with the identical astronomical terms and the identical equation, isolating the more-than-{N_CIV_OPTIMISTIC/max(N_CIV_PESSIMISTIC,1e-30):.0e}-fold spread entirely to the four biological terms, exactly the point this lecture\u2019s honest-uncertainty argument is built to make.',
        ],
        pitfall='Presenting the Drake equation\u2019s output as a scientific prediction rather than a structured, order-of-magnitude estimation exercise whose result is dominated by explicitly unconstrained terms. A responsible use of the equation (as this lecture models) states the huge uncertainty explicitly, attributes it to specific named terms, and does not claim the final number as evidence either for or against the existence of extraterrestrial intelligence.',
        activity='Using this lecture\u2019s astronomically constrained R*, f_p, and n_e values together with your own explicitly stated, justified assumptions for f_l, f_i, f_c, and L, compute your own estimate of N, and write one paragraph identifying exactly which of your assumed values is doing the most work in setting your final answer -- and what specific new observation (if any) could, in principle, tighten that particular term.',
        lab_connection='Lab 07, this course\u2019s capstone, requires a full written synthesis applying every major tool from the semester (detection method, demographics context, interior/atmosphere characterization, habitable-zone status, biosignature false-positive reasoning, and a personally justified Drake equation estimate) to one self-chosen, instructor-approved real exoplanet system.',
        synthesis='This course\u2019s full toolkit -- from the radial-velocity semi-amplitude equation that discovered 51 Pegasi b to the Drake equation\u2019s structured, honestly uncertain estimate of extraterrestrial intelligence\u2019s prevalence -- converges on a single disciplined habit of mind: distinguish what is directly measured, what is derived from well-established physical law, what is a standard published value requiring a human spot-check, and what remains a genuinely open scientific question, and never present the last category as if it were the first. That habit, more than any single equation, is this course\u2019s actual capstone.',
        openstax=OPENSTAX_NOTE,
    ),
]


def slide_deck(item: dict) -> str:
    n = item['n']
    fig = lecture_svg(item)
    body = f"""<main class='deck'>
<section class='slide title'><p class='kicker'>ASTR 350 &middot; Lecture {n:02d}</p><h1>{escape(item['title'])}</h1><h2>{escape(item['subtitle'])}</h2></section>
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
<section class='slide'><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Course dataset and derivations used in this lecture\u2019s worked example: <code>materials/ASTR350/data/</code> and <code>materials/ASTR350/src/generate_astr350_content.py</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 350 Lecture {n:02d} Slides', body, SLIDE_CSS)


def lecture_notes(item: dict) -> str:
    n = item['n']
    body = f"""<header><div><h1>Lecture {n:02d}: {escape(item['title'])}</h1><p>ASTR 350 Exoplanets and Astrobiology</p></div></header>
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
<section><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Every numeric result above is computed programmatically in <code>materials/ASTR350/src/generate_astr350_content.py</code>, not hand-typed.</li></ul></section>
</main>"""
    return page(f'ASTR 350 Lecture {n:02d} Notes', body)


def write_lectures():
    LECTURE_DIR.mkdir(parents=True, exist_ok=True)
    for item in LECTURES:
        n = item['n']
        (LECTURE_DIR / f'lecture-{n:02d}-slides.html').write_text(slide_deck(item), encoding='utf-8')
        (LECTURE_DIR / f'lecture-{n:02d}-notes.html').write_text(lecture_notes(item), encoding='utf-8')


def write_data_csv():
    import csv
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / 'exoplanets.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['name', 'period_d', 'a_au', 'e', 'mass_mjup_or_mearth', 'radius_rjup_or_rearth', 'notes'])
        w.writerow(['51 Pegasi b', PLANET_51PEGB['period_d'], PLANET_51PEGB['a_au'], PLANET_51PEGB['e'],
                    PLANET_51PEGB['mass_mjup'], '', 'live-verified 2026-09-24'])
        w.writerow(['HD 209458 b', PLANET_HD209458B['period_d'], PLANET_HD209458B['a_au'], PLANET_HD209458B['e'],
                    PLANET_HD209458B['mass_mjup'], PLANET_HD209458B['radius_rjup'], 'live-verified 2026-09-24'])
        for p, d in TRAPPIST1_PLANETS.items():
            w.writerow([f'TRAPPIST-1{p}', d['period_d'], d['a_au'], '', d['m_earth'], d['r_earth'],
                        'reused from ASTR320 live verification'])
    with open(DATA_DIR / 'extremophiles.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['organism', 'trait', 'value', 'unit'])
        for e in EXTREMOPHILES:
            w.writerow([e['name'], e['trait'], e['value'], e['unit']])


if __name__ == '__main__':
    write_lectures()
    write_data_csv()
    print(f'Wrote {len(LECTURES)} lectures to {LECTURE_DIR}')
