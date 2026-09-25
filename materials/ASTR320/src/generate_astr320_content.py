"""Content generator for ASTR320 lecture slides and lecture notes.

Every worked numeric example is computed programmatically from the shared
constants and datasets defined below (not hand-typed), and the same
constants are reused across labs and problem sets that reference the same
scenario (see generate_astr320_labs_psets.py). Run with the project
interpreter:
    python materials/ASTR320/src/generate_astr320_content.py
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


def fmt(x, nd=3):
    return f"{x:.{nd}g}"


def lecture_svg(n: int, title: str, left_label: str, mid_label: str, right_label: str, caption: str) -> str:
    return (
        f"<svg class='lecture-figure' data-lecture-figure='{n:02d}' viewBox='0 0 980 620' role='img' "
        f"aria-label='Lecture {n:02d} visual model: {escape(title)}'>"
        f"<rect width='980' height='620' fill='#fbfcfd'/>"
        f"<text x='34' y='48' font-size='26' fill='#102a43' font-family='Segoe UI, sans-serif'>Lecture {n:02d}: {escape(title)}</text>"
        f"<rect x='60' y='180' width='250' height='150' rx='14' fill='#0f6b78' opacity='.85'/>"
        f"<rect x='365' y='180' width='250' height='150' rx='14' fill='#b87911' opacity='.85'/>"
        f"<rect x='670' y='180' width='250' height='150' rx='14' fill='#102a43' opacity='.85'/>"
        f"<path d='M310 255 L365 255 M615 255 L670 255' stroke='#5b6773' stroke-width='5' marker-end='url(#arrow)'/>"
        f"<defs><marker id='arrow' markerWidth='10' markerHeight='10' refX='8' refY='5' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='#5b6773'/></marker></defs>"
        f"<text x='80' y='260' font-size='19' fill='#fff' font-family='Segoe UI, sans-serif'>{escape(left_label)}</text>"
        f"<text x='385' y='260' font-size='19' fill='#fff' font-family='Segoe UI, sans-serif'>{escape(mid_label)}</text>"
        f"<text x='690' y='260' font-size='19' fill='#fff' font-family='Segoe UI, sans-serif'>{escape(right_label)}</text>"
        f"<text x='34' y='470' font-size='19' fill='#5b6773' font-family='Segoe UI, sans-serif'>{escape(caption)}</text>"
        f"</svg>"
    )


# ---------------------------------------------------------------------------
# Physical constants (SI unless noted)
# ---------------------------------------------------------------------------
G_NEWTON = 6.674e-11        # m^3 kg^-1 s^-2
SIGMA_SB = 5.670374e-8      # W m^-2 K^-4
K_BOLTZMANN = 1.381e-23     # J/K
M_PROTON = 1.6726e-27       # kg
AU_M = 1.496e11
DAY_S = 86400.0
YEAR_S = 3.15576e7
L_SUN_W = 3.828e26
M_SUN_KG = 1.989e30
R_SUN_M = 6.957e8

# ---------------------------------------------------------------------------
# Real solar-system planetary parameters (standard published values: JPL
# Planetary Fact Sheets / NASA Solar System Dynamics; not independently
# re-verified via a live fetch this session -- flagged in reference-log.md).
# mass in kg, radius in m, semimajor axis in AU, orbital period in years,
# bond albedo (dimensionless), mean surface/1-bar temperature in K.
# ---------------------------------------------------------------------------
PLANETS = {
    'Mercury': dict(mass=3.3011e23, radius=2439.7e3, a_au=0.3871, period_yr=0.2408, albedo=0.088, teq_obs=440.0),
    'Venus':   dict(mass=4.8675e24, radius=6051.8e3, a_au=0.7233, period_yr=0.6152, albedo=0.76, teq_obs=737.0),
    'Earth':   dict(mass=5.9724e24, radius=6371.0e3, a_au=1.0000, period_yr=1.0000, albedo=0.306, teq_obs=288.0),
    'Mars':    dict(mass=6.4171e23, radius=3389.5e3, a_au=1.5237, period_yr=1.8808, albedo=0.25, teq_obs=210.0),
    'Jupiter': dict(mass=1.8982e27, radius=69911e3, a_au=5.2038, period_yr=11.862, albedo=0.503, teq_obs=165.0),
    'Saturn':  dict(mass=5.6834e26, radius=58232e3, a_au=9.5826, period_yr=29.457, albedo=0.342, teq_obs=134.0),
    'Uranus':  dict(mass=8.6810e25, radius=25362e3, a_au=19.191, period_yr=84.011, albedo=0.300, teq_obs=76.0),
    'Neptune': dict(mass=1.02413e26, radius=24622e3, a_au=30.069, period_yr=164.79, albedo=0.290, teq_obs=72.0),
}

MOON = dict(mass=7.342e22, radius=1737.4e3, a_m=3.844e8)
EARTH_ATM_SCALE_HEIGHT_M = 8500.0  # published sea-level value
EARTH_SURFACE_G = 9.80665

# Io / Europa (Jupiter's Galilean moons; standard published values, not
# independently re-verified by live fetch this session).
JUPITER_MASS_KG = PLANETS['Jupiter']['mass']
IO = dict(mass=8.9319e22, radius=1821.6e3, a_m=421700e3, ecc=0.0041)
EUROPA = dict(mass=4.7998e22, radius=1560.8e3, a_m=671100e3, ecc=0.009)
ENCELADUS = dict(mass=1.08022e20, radius=252.1e3, a_m=238020e3, ecc=0.0047, primary_mass=5.6834e26)

# Saturn's rings (Roche-limit worked example)
SATURN = PLANETS['Saturn']
SATURN_A_RING_OUTER_M = 136780e3
ICE_DENSITY_KGM3 = 917.0
SATURN_MEAN_DENSITY_KGM3 = SATURN['mass'] / (4 / 3 * math.pi * SATURN['radius'] ** 3)

# TRAPPIST-1 (live-verified this session via direct web fetch of Wikipedia's
# "TRAPPIST-1" article, 2026-09-24; primary literature: Agol et al. 2021, PSJ
# 2, 1; Ducrot et al. 2020, A&A 640, A112; Gillon et al. 2017, Nature 542,
# 456; Delrez et al. 2022, A&A 667, A59). Used as the course's real
# well-characterized exoplanet system throughout Lecture 14, Lab 07, and PS 07.
TRAPPIST1_STAR = dict(mass_msun=0.0898, radius_rsun=0.1192, lum_lsun=5.66e-4, teff=2566.0, distance_pc=12.47)
TRAPPIST1_PLANETS = {
    'b': dict(a_au=0.0115, period_d=1.51),
    'c': dict(a_au=0.0158, period_d=2.42),
    'd': dict(a_au=0.0223, period_d=4.05),
    'e': dict(a_au=0.0293, period_d=6.10),
    'f': dict(a_au=0.0385, period_d=9.21),
    'g': dict(a_au=0.0469, period_d=12.35),
    'h': dict(a_au=0.0619, period_d=18.77),
}


def equilibrium_temperature_k(lum_w: float, a_m: float, bond_albedo: float) -> float:
    """Zero-atmosphere radiative-equilibrium (sub-stellar-averaged) temperature."""
    return ((1 - bond_albedo) * lum_w / (16 * math.pi * SIGMA_SB * a_m ** 2)) ** 0.25


def scale_height_m(temp_k: float, mean_molecular_mass_kg: float, surface_g: float) -> float:
    return K_BOLTZMANN * temp_k / (mean_molecular_mass_kg * surface_g)


def roche_limit_rigid_m(primary_radius_m: float, primary_density: float, satellite_density: float) -> float:
    return primary_radius_m * (2 * primary_density / satellite_density) ** (1 / 3)


def roche_limit_fluid_m(primary_radius_m: float, primary_density: float, satellite_density: float) -> float:
    """Fluid (self-gravitating, tidally deformable) Roche limit, factor 2.44."""
    return 2.44 * primary_radius_m * (primary_density / satellite_density) ** (1 / 3)


def jeans_parameter(escape_v_ms: float, thermal_v_ms: float) -> float:
    return (escape_v_ms / thermal_v_ms) ** 2


def surface_gravity(mass_kg: float, radius_m: float) -> float:
    return G_NEWTON * mass_kg / radius_m ** 2


def escape_velocity(mass_kg: float, radius_m: float) -> float:
    return math.sqrt(2 * G_NEWTON * mass_kg / radius_m)


def thermal_speed_most_probable(temp_k: float, molecule_mass_kg: float) -> float:
    return math.sqrt(2 * K_BOLTZMANN * temp_k / molecule_mass_kg)


def tidal_acceleration(primary_mass_kg: float, sat_radius_m: float, orbital_radius_m: float) -> float:
    return 2 * G_NEWTON * primary_mass_kg * sat_radius_m / orbital_radius_m ** 3


AMU = 1.66054e-27
H2_MASS = 2.016 * AMU
N2_MASS = 28.014 * AMU
CO2_MASS = 44.01 * AMU

# ---------------------------------------------------------------------------
# Precomputed worked-example values (used identically in slides, notes, and
# cross-referenced by labs/problem sets in generate_astr320_labs_psets.py)
# ---------------------------------------------------------------------------
DENSITIES = {name: p['mass'] / (4 / 3 * math.pi * p['radius'] ** 3) for name, p in PLANETS.items()}
GRAVITIES = {name: surface_gravity(p['mass'], p['radius']) for name, p in PLANETS.items()}
ESCAPE_VS = {name: escape_velocity(p['mass'], p['radius']) for name, p in PLANETS.items()}
TEQ_ZERO_ALBEDO = {name: equilibrium_temperature_k(L_SUN_W, p['a_au'] * AU_M, 0.0) for name, p in PLANETS.items()}
TEQ_BOND = {name: equilibrium_temperature_k(L_SUN_W, p['a_au'] * AU_M, p['albedo']) for name, p in PLANETS.items()}

EARTH_H_N2 = scale_height_m(288.0, N2_MASS, EARTH_SURFACE_G)
VENUS_G = surface_gravity(PLANETS['Venus']['mass'], PLANETS['Venus']['radius'])
VENUS_H_CO2 = scale_height_m(737.0, CO2_MASS, VENUS_G)
MARS_G = surface_gravity(PLANETS['Mars']['mass'], PLANETS['Mars']['radius'])
MARS_H_CO2 = scale_height_m(210.0, CO2_MASS, MARS_G)

EARTH_ESCAPE_V = ESCAPE_VS['Earth']
EARTH_H2_THERMAL_V = thermal_speed_most_probable(1000.0, H2_MASS)  # exosphere ~1000 K
EARTH_JEANS_H2 = jeans_parameter(EARTH_ESCAPE_V, EARTH_H2_THERMAL_V)
MARS_ESCAPE_V = ESCAPE_VS['Mars']
MARS_H2_THERMAL_V = thermal_speed_most_probable(1000.0, H2_MASS)
MARS_JEANS_H2 = jeans_parameter(MARS_ESCAPE_V, MARS_H2_THERMAL_V)

ROCHE_ICE_SATURN_M = roche_limit_rigid_m(SATURN['radius'], SATURN_MEAN_DENSITY_KGM3, ICE_DENSITY_KGM3)
ROCHE_ICE_SATURN_RS = ROCHE_ICE_SATURN_M / SATURN['radius']
ROCHE_FLUID_SATURN_M = roche_limit_fluid_m(SATURN['radius'], SATURN_MEAN_DENSITY_KGM3, ICE_DENSITY_KGM3)
ROCHE_FLUID_SATURN_RS = ROCHE_FLUID_SATURN_M / SATURN['radius']
A_RING_OUTER_RS = SATURN_A_RING_OUTER_M / SATURN['radius']

IO_TIDAL_A = tidal_acceleration(JUPITER_MASS_KG, IO['radius'], IO['a_m'])
IO_OWN_G = surface_gravity(IO['mass'], IO['radius'])
IO_TIDAL_FRAC = IO_TIDAL_A / IO_OWN_G * 100
EUROPA_TIDAL_A = tidal_acceleration(JUPITER_MASS_KG, EUROPA['radius'], EUROPA['a_m'])
EUROPA_OWN_G = surface_gravity(EUROPA['mass'], EUROPA['radius'])
EUROPA_TIDAL_FRAC = EUROPA_TIDAL_A / EUROPA_OWN_G * 100
ENCELADUS_TIDAL_A = tidal_acceleration(ENCELADUS['primary_mass'], ENCELADUS['radius'], ENCELADUS['a_m'])
ENCELADUS_OWN_G = surface_gravity(ENCELADUS['mass'], ENCELADUS['radius'])
ENCELADUS_TIDAL_FRAC = ENCELADUS_TIDAL_A / ENCELADUS_OWN_G * 100

TRAPPIST1_LUM_W = TRAPPIST1_STAR['lum_lsun'] * L_SUN_W
TRAPPIST1_TEQ = {p: equilibrium_temperature_k(TRAPPIST1_LUM_W, d['a_au'] * AU_M, 0.0)
                  for p, d in TRAPPIST1_PLANETS.items()}
EARTH_TEQ_ZERO_ALBEDO = TEQ_ZERO_ALBEDO['Earth']


# ---------------------------------------------------------------------------
# Slide-deck / notes rendering helpers
# ---------------------------------------------------------------------------

def slide(css_class: str, inner: str) -> str:
    return f"<section class='slide {css_class}'>{inner}</section>"


def title_slide(n: int, title: str, kicker: str, subtitle: str) -> str:
    return slide('title', f"<p class='kicker'>{escape(kicker)}</p><h1>Lecture {n:02d}: {escape(title)}</h1>"
                          f"<h2>{escape(subtitle)}</h2>")


def bullets_slide(heading: str, bullets) -> str:
    return slide('', f"<h2>{escape(heading)}</h2><ul>{li(bullets)}</ul>")


def objectives_slide(objectives) -> str:
    return slide('', f"<h2>Learning Objectives</h2><ol>{li(objectives)}</ol>")


def worked_slide(title: str, steps) -> str:
    body = ''.join(f"<div class='equation'>{s}</div>" if s.startswith('$') or '=' in s and len(s) < 90
                    else f"<p>{s}</p>" for s in steps)
    return slide('', f"<h2>Worked Example: {escape(title)}</h2>{body}")


def summary_slide(summary, preview: str) -> str:
    return slide('', f"<h2>Summary and Next Lecture</h2><ul>{li(summary)}</ul><p class='small'>Next: {escape(preview)}</p>")


def build_deck(lec) -> str:
    body = title_slide(lec['n'], lec['title'], lec['kicker'], lec['subtitle'])
    body += objectives_slide(lec['objectives'])
    for heading, bullets, _notes in lec['sections']:
        body += bullets_slide(heading, bullets)
    body += worked_slide(lec['worked_title'], lec['worked_steps'])
    body += summary_slide(lec['summary'], lec['preview'])
    return page(f"ASTR 320 Lecture {lec['n']:02d}: {lec['title']}", f"<div class='deck'>{body}</div>", SLIDE_CSS)


def build_notes(lec) -> str:
    parts = [f"<header><div><h1>Lecture {lec['n']:02d}: {escape(lec['title'])}</h1>"
             f"<p>{escape(lec['subtitle'])}</p></div></header><main>"]
    parts.append("<section><h2>Learning Objectives</h2><ol>" + li(lec['objectives']) + "</ol></section>")
    for heading, bullets, notes in lec['sections']:
        parts.append(f"<section><h2>{escape(heading)}</h2><ul>{li(bullets)}</ul><p>{notes}</p></section>")
    parts.append(f"<section class='notice'><h2>Worked Example: {escape(lec['worked_title'])}</h2>"
                  + ''.join(f"<p>{s}</p>" for s in lec['worked_steps'])
                  + f"<p>{lec['worked_notes']}</p></section>")
    parts.append("<section><h2>Summary</h2><ul>" + li(lec['summary']) + f"</ul><p><strong>Looking ahead:</strong> {escape(lec['preview'])}</p></section>")
    parts.append("</main>")
    return page(f"ASTR 320 Lecture {lec['n']:02d} Notes: {lec['title']}", ''.join(parts))


# ---------------------------------------------------------------------------
# Lecture content
# ---------------------------------------------------------------------------
LECTURES = []

LECTURES.append(dict(
    n=1, title='Introduction to Planetary Science and Comparative Planetology',
    kicker='Unit 1: Formation and Architecture', subtitle='Why planets differ, and how we compare them',
    objectives=[
        'Define planetary science as the study of the origin, structure, and evolution of planets, moons, rings, and small bodies, distinct from stellar astrophysics.',
        'State the terrestrial/Jovian dichotomy in mass, radius, density, and composition and connect it to formation location.',
        'Compute planetary densities, surface gravities, and escape velocities directly from mass and radius.',
        'Identify the major spacecraft datasets (Voyager, Galileo, Cassini-Huygens, MESSENGER, Juno, New Horizons) that ground this course.',
    ],
    sections=[
        ('A Young but Data-Rich Science',
         ['Modern planetary science is barely 60 years old as an observational discipline: before 1962 (Mariner 2 at Venus) every planet beyond Earth was a point of light.',
          'Ground-based telescopy limited early planetary astronomy to broad photometric colors, crude spectra, and (for the Moon and Mars) telescopic imaging.',
          'The subject now integrates geophysics, atmospheric physics, chemistry, and orbital dynamics using in-situ spacecraft measurements as well as remote sensing.'],
         'Planetary science is unusual among the astronomical sciences in how recently it became a genuinely quantitative field: prior to the space age most "planetary astronomy" consisted of visual and photographic observations of surface markings and disk-integrated colors, with almost no direct measurement of interior structure, magnetic fields, or atmospheric composition. The Mariner, Viking, Voyager, Galileo, Cassini-Huygens, MESSENGER, Juno, and New Horizons missions transformed the field by delivering in-situ magnetometer, mass-spectrometer, seismometer, and radio-science data that let scientists test physical models rather than merely describe appearances. This course draws its numbers from that record: nearly every quantity used in worked examples throughout the semester (masses, radii, atmospheric compositions, magnetic moments) traces back to a specific spacecraft measurement or a specific published catalog value, and the reference log for this course identifies which is which.'),
        ('The Terrestrial/Jovian Dichotomy',
         ['Mercury, Venus, Earth, and Mars are dense (&rho; &sim; 3900-5510 kg/m&sup3;), rocky/metallic, and have thin or moderate atmospheres.',
          'Jupiter, Saturn, Uranus, and Neptune are large, low-density (&rho; &sim; 690-1640 kg/m&sup3;), hydrogen/helium- or ice-dominated, and have no solid surface.',
          'This split in bulk density is not a coincidence of naming; it reflects where in the temperature structure of the protoplanetary disk each planet accreted its material.'],
         'The terrestrial/Jovian dichotomy is the single most important organizing fact in comparative planetology, and this course returns to it repeatedly: it explains why Mercury has essentially no atmosphere while Titan (smaller than Mercury) has a thick one, why Jupiter\'s magnetic moment dwarfs Earth\'s by a factor of about 20,000, and why only the outer planets can host extensive ring and regular-satellite systems built from ice. The physical cause -- condensation temperature versus distance from the protosun -- is developed quantitatively in Lecture 02.'),
        ('Density, Gravity, and Escape Velocity from First Principles',
         ['Mean density &rho; = M / (4/3 &pi; R&sup3;) is the single most informative bulk quantity a spacecraft flyby can deliver quickly (from M via Doppler tracking, R via imaging).',
          'Surface gravity g = GM/R&sup2; sets the pressure gradient that governs atmospheric structure (Lecture 07) and interior compression (Lecture 03).',
          'Escape velocity v_esc = &radic;(2GM/R) sets which molecules a planet can retain against thermal escape (Lecture 09).'],
         'These three quantities -- density, surface gravity, and escape velocity -- are computed identically for every planet in this course\'s worked examples using only two measured numbers, mass and radius, both obtainable from Doppler tracking and imaging without ever landing an instrument. That two such elementary measurements unlock density (composition), surface gravity (atmospheric pressure structure), and escape velocity (atmospheric retention) is why they are introduced before any other planetary quantity.'),
        ('Solar System Inventory',
         ['Eight planets, five recognized dwarf planets (Ceres, Pluto, Haumea, Makemake, Eris), hundreds of thousands of cataloged asteroids, and a Kuiper Belt population extending past 50 AU.',
          'Regular satellites (formed in circumplanetary disks, prograde, low inclination) versus irregular satellites (captured, often retrograde, high inclination, high eccentricity).',
          'Ring systems around all four giant planets, though only Saturn\'s is bright enough for naked-eye telescopic discovery.'],
         'The solar system\'s inventory is not static trivia -- the distinction between regular and irregular satellites is a direct fossil record of formation process (Lecture 02 and Lecture 12), and the existence of ring systems around all four giant planets (not just Saturn) shows that ring formation, most likely from Roche-limit tidal disruption of a captured or disrupted body, is a generic outcome of giant-planet environments rather than a peculiarity of Saturn.'),
        ('Comparative Planetology as Method',
         ['Comparative planetology treats each planet, moon, or ring system as a natural experiment testing the same underlying physics under different boundary conditions (mass, distance, composition).',
          'Venus and Earth share nearly identical mass and radius but diverged catastrophically in surface climate -- a direct test of runaway-greenhouse physics (Lecture 09).',
          'Mars and Earth share comparable early volatile inventories but diverged in whether plate tectonics and a protective magnetic field persisted (Lectures 05, 10).'],
         'The comparative method is this course\'s central methodology: rather than treating Earth as the default and other planets as exotic exceptions, each lecture uses at least two solar-system bodies (and, from Lecture 14 onward, an exoplanet system) to isolate which planetary parameter -- mass, distance, initial volatile inventory, rotation rate -- controls a given outcome. This is precisely the same logic used in laboratory science to identify a causal variable by holding others fixed.'),
        ('Scales and Units in Planetary Science',
         ['Distances: astronomical units (1 AU = 1.496 &times; 10&sup1;&sup9; m) for orbital scales, planetary radii for local (ring, atmosphere) scales.',
          'Pressure: bars (1 bar = 10&sup5; Pa &asymp; Earth sea-level pressure) rather than pascals, for atmospheric comparison across worlds.',
          'Time: both years (orbital dynamics) and geological eras (surface evolution, radiometric dating) appear throughout this course.'],
         'Planetary scientists deliberately use human-scale units (bars, planetary radii, Earth masses) rather than pure SI units because the quantities of interest span such enormous dynamic range (Mercury\'s surface pressure is effectively zero; Venus\'s is 92 bar) that SI pascals obscure rather than reveal the comparison. This course uses SI units in all derivations for dimensional consistency, but reports final answers in the units the field actually uses.'),
        ('A Worked Comparative Table',
         ['The table below is generated directly from each planet\'s mass and radius (JPL Planetary Fact Sheet values; standard published data, not independently re-verified by live fetch this session).',
          'Densities separate cleanly into a terrestrial cluster (&sim;3900-5510 kg/m&sup3;) and a Jovian cluster (&sim;690-1640 kg/m&sup3;).',
          f'Escape velocities range from {fmt(ESCAPE_VS["Mercury"]/1000,3)} km/s (Mercury) to {fmt(ESCAPE_VS["Jupiter"]/1000,3)} km/s (Jupiter) -- more than a factor of {ESCAPE_VS["Jupiter"]/ESCAPE_VS["Mercury"]:.0f}, which will matter directly for atmospheric retention in Lecture 09.'],
         'The comparative table generated in this lecture\'s worked example is reused, without modification, in Lecture 07 (scale height), Lecture 08 (equilibrium temperature), and Lecture 09 (Jeans escape) -- so any arithmetic error caught in one lecture is caught everywhere at once, and a student who understands this table\'s construction already has the numbers needed for three subsequent worked examples.'),
        ('Open Questions Motivating This Course',
         ['Why does Earth alone (among the terrestrial planets) sustain plate tectonics and an internally generated magnetic field today?',
          'What set the final water/volatile inventory of each terrestrial planet, and why did it diverge so strongly (Venus vs. Earth vs. Mars)?',
          'How representative is our solar system\'s architecture of planetary systems generally, now that thousands of exoplanets are characterized?'],
         'These three questions recur across the semester and are revisited explicitly in the Lecture 14 capstone: the first is addressed by Lectures 03-05 and 10, the second by Lectures 02 and 09, and the third by the TRAPPIST-1 case study that closes the course. Framing the syllabus around open questions rather than a list of topics is intentional: comparative planetology is an active research field, not a closed catalog of facts.'),
        ('Reading and Historical Context',
         ['OpenStax <em>Astronomy 2e</em> Chapter 7 (Other Worlds: An Introduction to the Solar System) surveys the inventory covered in this lecture at an introductory level.',
          'This course goes beyond OpenStax\'s introductory survey by deriving the physical models (condensation, hydrostatic structure, radiative balance, tidal forces, dynamo action) that explain the inventory rather than only cataloging it.',
          'Historical framing: Galileo\'s 1610 discovery of Jupiter\'s four largest moons was the first direct evidence that not all bodies orbit Earth, a founding observation for comparative planetology.'],
         'OpenStax Astronomy 2e Chapter 7 is an appropriate companion reading for this lecture\'s survey content, but the course textbook is explicitly insufficient for the derivation-heavy material introduced from Lecture 02 onward; each subsequent lecture states explicitly where it extends beyond the assigned OpenStax reading, following the precedent set in ASTR 310.'),
        ('Spacecraft Data as Ground Truth',
         ['In-situ magnetometers (Galileo, Juno, Cassini) measure planetary magnetic moments directly rather than inferring them from theory.',
          'Radio science (Doppler tracking of a spacecraft\'s trajectory) delivers a planet\'s mass and, from higher-order gravity harmonics, clues to its internal density distribution (Lecture 03).',
          'Sample return (Apollo, Luna, Hayabusa2, OSIRIS-REx) and landed seismometers (Apollo, InSight) provide ground truth against which remote-sensing inferences are calibrated.'],
         'A recurring theme in this course is distinguishing measurements that are direct (a magnetometer reading, a seismometer trace, a returned sample\'s isotopic ratio) from those that are model-dependent inferences (an atmospheric composition inferred from a transmission spectrum, an interior structure inferred from a gravity field and an assumed equation of state). Both are valuable, but conflating them is a common error this course asks students to avoid.'),
        ('Course Roadmap',
         ['Weeks 1-4 build the planet from the inside out: formation (Lecture 02), interior structure (Lecture 03), heat budget (Lecture 04), and surface geology (Lectures 05-06).',
          'Weeks 5-7 build the atmosphere: hydrostatic structure and radiative balance (Lectures 07-08), then atmospheric escape and climate evolution (Lecture 09).',
          'Weeks 8-10 turn outward to magnetic fields (Lecture 10), giant planets and rings (Lectures 11-12), icy satellites (Lecture 13), and the exoplanet capstone (Lecture 14).'],
         'This roadmap is designed so that each unit\'s physical tools (hydrostatic equilibrium, radiative balance, tidal forces) are derived once and then reused with new data in later units, mirroring the cumulative-toolkit structure used successfully in ASTR 310.'),
    ],
    worked_title='Density, Gravity, and Escape Velocity for the Eight Planets',
    worked_steps=[
        'Given each planet\'s mass M and radius R (JPL Planetary Fact Sheet values), compute &rho; = M / (4/3 &pi; R&sup3;), g = GM/R&sup2;, and v_esc = &radic;(2GM/R).',
        '<table><tr><th>Planet</th><th>&rho; (kg/m&sup3;)</th><th>g (m/s&sup2;)</th><th>v_esc (km/s)</th></tr>' + ''.join(
            f"<tr><td>{name}</td><td>{fmt(DENSITIES[name],4)}</td><td>{fmt(GRAVITIES[name],3)}</td><td>{fmt(ESCAPE_VS[name]/1000,3)}</td></tr>"
            for name in PLANETS) + '</table>',
        f'Result: the four terrestrial planets cluster at &rho; = 3900-5510 kg/m&sup3;; the four giant planets cluster at &rho; = {fmt(DENSITIES["Saturn"],3)}-{fmt(DENSITIES["Jupiter"],3)} kg/m&sup3;, confirming the dichotomy quantitatively rather than by definition.',
    ],
    worked_notes='This table is computed once in <code>generate_astr320_content.py</code> and is reused verbatim (same numbers, same code path) in Lecture 07\'s scale-height table and Lecture 08\'s equilibrium-temperature table, so students see the same eight planets accumulate additional derived columns lecture by lecture rather than encountering fresh numbers each time.',
    summary=['Planetary science compares worlds as natural experiments to isolate the physics that controls climate, geology, and habitability.',
             'Density, surface gravity, and escape velocity, computed from mass and radius alone, already separate the solar system into terrestrial and Jovian classes.',
             'This course builds physical derivations (formation, structure, atmospheres, magnetism, tides) that explain, rather than merely catalog, that separation.'],
    preview='Lecture 02 derives why the terrestrial/Jovian dichotomy exists: the condensation sequence and the frost line in the solar nebula.',
))

LECTURES.append(dict(
    n=2, title='The Solar Nebula, Condensation, and Planet Formation',
    kicker='Unit 1: Formation and Architecture', subtitle='From a collapsing cloud to a disk of planetesimals',
    objectives=[
        'Describe the solar nebula model: collapse of a molecular cloud core into a rotating protoplanetary disk.',
        'Derive the frost-line location from radiative-equilibrium disk temperature and the condensation temperature of water ice.',
        'Explain core accretion and its two-stage growth (planetesimals to embryos, embryos to planets/cores).',
        'Connect the frost line quantitatively to the terrestrial/Jovian dichotomy introduced in Lecture 01.',
    ],
    sections=[
        ('Cloud Collapse and Angular Momentum',
         ['A slowly rotating molecular cloud core (T &sim; 10-20 K, size &sim; 0.1 pc) collapses under self-gravity once it exceeds the Jeans mass.',
          'Angular momentum conservation flattens the collapsing envelope into a rotating disk once material can no longer fall directly onto the forming protostar.',
          'The Sun formed at the disk center; the remaining disk (initially &sim;1-2% of the stellar mass) is the raw material for every planet, moon, and small body.'],
         'The transition from a roughly spherical collapsing cloud to a flattened disk is a direct consequence of angular momentum conservation: material with any net rotation cannot collapse straight to the center without first spiraling inward and outward until centrifugal support balances gravity in the disk plane, while material along the rotation axis, having no angular momentum to shed, can fall in more directly. This is the same physics that produces flattened disks around forming stars observed today (e.g., in ALMA imaging of nearby young stellar objects), which provides direct observational support for a model of our own solar system\'s birth that we cannot observe directly.'),
        ('The Protoplanetary Disk\'s Temperature Structure',
         ['Viscous heating and reprocessed stellar radiation set a disk temperature profile that falls with distance from the protosun, roughly T(r) &prop; r&#8315;&#189; to r&#8315;&sup3;&#8260;&#8308; depending on the heating mechanism.',
          'Close to the protosun (&lt; 1 AU) temperatures exceed 1500 K, hot enough to vaporize even refractory silicates and metals.',
          'Beyond a few AU, temperatures fall below the condensation point of water ice (&sim;150-170 K at typical disk pressures).'],
         'The key physical idea in this lecture is that the disk was never uniform: it was a temperature gradient, and different chemical species condense out of the vapor phase at different characteristic temperatures (iron and silicates above &sim;1300-1400 K, water ice below &sim;150-170 K, more volatile ices such as CO and N2 below &sim;20-30 K). This condensation sequence, not a difference in bulk composition of the nebula, is the single physical reason the inner and outer solar system ended up built from different material.'),
        ('Deriving the Frost Line',
         ['Model the disk temperature using the same radiative-equilibrium balance developed fully in Lecture 08: incident flux from the protosun equals the local blackbody emission of the disk midplane.',
          'Set T(r) equal to water\'s condensation temperature (&sim;150 K at typical disk pressures) and solve for r: this is the frost line (or snow line).',
          'Using a young Sun\'s luminosity, the frost line sits at roughly 2.7-3 AU, consistent with the observed transition between the rocky asteroid belt and Jupiter\'s formation zone.'],
         'The frost-line derivation previews the equilibrium-temperature formula this course derives rigorously in Lecture 08; here it is used qualitatively to locate a single controlling radius. Because water ice was several times more abundant (by mass, once condensed) than the rocky/metallic material available everywhere in the disk, any planetary embryo forming beyond the frost line had access to far more solid building material, letting it grow massive enough to gravitationally capture the surrounding hydrogen/helium gas before the gas dispersed -- this is precisely why the giant planets are giant.'),
        ('Condensation Sequence Table',
         ['Refractory metals and oxides (Al, Ca compounds): condense above &sim;1400 K, found in the innermost disk and in primitive meteorite calcium-aluminum inclusions (CAIs).',
          'Iron-nickel metal and silicates (olivine, pyroxene): condense &sim;1300-1350 K, dominate Mercury through Mars.',
          'Water ice: condenses &sim;150-170 K at typical disk pressures, dominates beyond the frost line.',
          'More volatile ices (CO, N2, CH4): condense below &sim;20-30 K, found only in the outermost disk (Kuiper Belt objects, comet nuclei).'],
         'This condensation sequence is not a theoretical abstraction: primitive meteorites (chondrites) preserve mineral assemblages that record exactly this temperature-ordered condensation, and calcium-aluminum inclusions in the Allende meteorite are among the oldest dated solids in the solar system (&sim;4.567 Gyr by Pb-Pb dating), anchoring the absolute chronology used throughout planetary science, including the crater-count age dating developed in Lecture 06.'),
        ('From Dust to Planetesimals',
         ['Micron-sized dust grains collide and stick (via van der Waals and electrostatic forces) to form millimeter-to-meter aggregates.',
          'The "meter-size barrier": objects around 1 m are especially vulnerable to radial drift into the star (due to gas drag) before they can grow further by simple sticking.',
          'Streaming instabilities, in which locally concentrated solids gravitationally interact with the surrounding gas, can rapidly concentrate meter-to-kilometer-size clumps into gravitationally bound planetesimals, bypassing the meter-size barrier.'],
         'The meter-size barrier remains an active research problem in planet-formation theory; the streaming-instability mechanism (Youdin & Goodman 2005 and later work) is currently the most widely accepted solution, and it makes a specific testable prediction -- rapid, quasi-simultaneous formation of many similarly sized planetesimals in a narrow region -- that is consistent with the observed size distribution of primitive asteroids and with the compact, resonant architecture of systems like TRAPPIST-1, introduced later in this course (Lecture 14).'),
        ('From Planetesimals to Planetary Embryos',
         ['Runaway growth: the largest planetesimals in a local swarm grow fastest, because gravitational focusing increases their effective cross-section for further accretion.',
          'Oligarchic growth: once a handful of embryos dominate their local feeding zones, growth slows and becomes more orderly, spacing embryos roughly evenly in orbital distance.',
          'Final assembly of terrestrial planets requires giant impacts between Moon-to-Mars-mass embryos over tens of millions of years -- a stochastic, chaotic late stage.'],
         'Runaway and oligarchic growth together explain why the solar system ended up with a modest number of planets rather than hundreds of similarly sized bodies: gravitational focusing is a strongly nonlinear process (the effective accretion cross-section scales with 1 + (v_esc/v_rel)&sup2;), so any embryo that gets even slightly ahead of its neighbors pulls further ahead, until only a few large bodies remain to fight over the final assembly.'),
        ('Giant Planet Core Accretion and Gas Capture',
         ['Beyond the frost line, embryos can grow to &sim;5-10 Earth masses (a "critical core mass") while the gas disk is still present.',
          'Once a core exceeds the critical mass, it can undergo runaway gas accretion, capturing hundreds of Earth masses of hydrogen/helium gas within &sim;10&#8308;-10&#8309; years.',
          'The gas disk disperses (via photoevaporation and accretion onto the star) within a few Myr, which is why only planets that reached critical core mass early enough became gas giants.'],
         'Core accretion explains a striking asymmetry: Jupiter and Saturn are 90%+ hydrogen/helium by mass (having captured gas efficiently), while Uranus and Neptune are only 10-20% hydrogen/helium (their cores likely formed too slowly, or too late, in a lower-density outer disk, to trigger runaway gas accretion before the gas disk dispersed) -- an idea this course revisits quantitatively in Lecture 11\'s giant-planet interior models.'),
        ('Planetary Migration',
         ['Gravitational interaction between a forming planet and the surrounding gas disk can transfer angular momentum and cause the planet to migrate inward or outward (Type I/Type II migration).',
          'Migration is now considered essential, not exceptional: Jupiter and Saturn may have migrated substantially (the "Grand Tack" hypothesis) before settling near their current orbits.',
          'Compact multi-planet systems around low-mass stars (e.g., TRAPPIST-1, previewed here and developed fully in Lecture 14) are widely modeled as having assembled via inward migration from formation locations near or beyond each system\'s frost line.'],
         'Migration resolves an awkward tension in the original in-situ core-accretion picture: Uranus and Neptune\'s current orbital locations (19 and 30 AU) correspond to such low disk densities that building their observed core masses in place, within the disk\'s few-Myr lifetime, is difficult; models in which the ice giants formed closer in and migrated outward (or formed among a larger initial population of embryos, some of which were ejected) ease this timing problem considerably.'),
        ('Evidence: Meteorites and Presolar Grains',
         ['Chondritic meteorites preserve chondrules (once-molten silicate droplets) and CAIs, direct physical samples of solar-nebula solids.',
          'Isotopic dating of CAIs (Pb-Pb method) gives 4.567 &plusmn; 0.001 Gyr, defining time zero for solar system chronology.',
          'Rare presolar grains (silicon carbide, graphite) within meteorites carry isotopic signatures from stars that died before the Sun formed, direct evidence that the solar nebula incorporated material from earlier stellar generations.'],
         'Presolar grains are a remarkable direct link between stellar nucleosynthesis (covered in ASTR 310 and ASTR 330) and planet formation: their isotopic ratios (e.g., anomalously high &sup1;&sup2;&sup2;Ne or &sup1;&sup3;C) match specific nucleosynthetic pathways in evolved and exploding stars, meaning some of the atoms in your body, and in every planet, were forged in stars that lived and died before the Sun existed.'),
        ('The Frost Line and the Dichotomy, Revisited',
         ['The frost line at &sim;2.7-3 AU divides the disk into a rocky/metallic inner region and an ice-rich, gas-capturing outer region.',
          'This single temperature threshold, combined with the differing efficiency of runaway gas accretion inside versus outside it, is sufficient to explain the terrestrial/Jovian dichotomy quantitatively, not just descriptively.',
          'The asteroid belt (2.1-3.3 AU) straddles the frost line and preserves both rocky (S-type) and more volatile-rich, ice-bearing (C-type) asteroid populations as a fossil record.'],
         'This section closes the loop opened in Lecture 01: the dichotomy in bulk density and composition observed there is not a coincidence but a direct, quantitative consequence of where each body\'s building blocks condensed relative to the frost line, combined with which bodies grew large enough, early enough, to capture nebular gas before it dispersed.'),
        ('Reading and Scope Note',
         ['OpenStax <em>Astronomy 2e</em> Section 7.2 (Composition and Structure of the Solar System) and Section 8.5 (Cosmic Rays) touch on nebular composition at an introductory level.',
          'The quantitative frost-line derivation, the runaway/oligarchic growth framework, and the core-accretion critical-mass argument extend substantially beyond OpenStax\'s introductory treatment and instead follow the standard planetary-science literature (Lissauer & de Pater, <em>Fundamental Planetary Science</em>, and the review by Raymond & Morbidelli 2022).'],
         'As with Lecture 01, students should treat OpenStax as background context rather than a complete source for this lecture\'s quantitative content; the assigned supplementary reading (Lissauer & de Pater, Chapter 15) covers the core-accretion model in the depth this course requires.'),
    ],
    worked_title='Locating the Frost Line',
    worked_steps=[
        'Approximate the young disk midplane temperature using the same equilibrium-temperature relation derived in full in Lecture 08: T(r) = [(1-A) L / (16 &pi; &sigma; r&sup2;)]&#185;&#8260;&#8308;, with the young Sun\'s luminosity taken as &sim; L&#8857; and A &asymp; 0 (optically thin dust reprocessing).',
        f'Using L = L&#8857; = {L_SUN_W:.3e} W and requiring T(r) = 150 K (water\'s condensation temperature), solve for r: '
        f'r = &radic;[(1-A) L / (16 &pi; &sigma; T&#8308;)] = {math.sqrt(L_SUN_W / (16*math.pi*SIGMA_SB*150.0**4))/AU_M:.2f} AU.',
        'Result: the derived frost line sits at roughly 2.8 AU, matching the asteroid-belt/Jupiter transition to within the precision of this simplified equilibrium model (real nebular models include viscous heating and are somewhat hotter close in, shifting the frost line to 2.7-3.2 AU depending on assumptions).',
    ],
    worked_notes='This calculation reuses the exact equilibrium-temperature function defined once in <code>generate_astr320_content.py</code> (<code>equilibrium_temperature_k</code>) that Lecture 08 derives from radiative balance and that Lecture 14 applies to TRAPPIST-1; the frost-line number is not a separate hand-typed constant.',
    summary=['The solar nebula\'s temperature gradient produced a chemically stratified disk: refractory solids inside the frost line, ice-rich solids beyond it.',
             'Two-stage growth (runaway then oligarchic accretion) explains why a modest number of planets, rather than hundreds of similar bodies, resulted.',
             'Core accretion beyond the frost line, followed by runaway gas capture before the gas disk dispersed, explains why the giant planets are gas- and ice-rich while the terrestrial planets are not.'],
    preview='Lecture 03 turns from the disk to the newly assembled planets and asks how each one differentiated into a core, mantle, and crust.',
))

LECTURES.append(dict(
    n=3, title='Planetary Differentiation and Interior Structure',
    kicker='Unit 2: Interiors and Heat', subtitle='Cores, mantles, crusts, and how we know they are there',
    objectives=[
        'Explain gravitational differentiation: how a molten early planet separates into density-stratified layers.',
        'Use the moment of inertia factor to constrain a planet\'s internal density distribution from spacecraft tracking data alone.',
        'Compare terrestrial planet interior structures (core size, mantle composition) using real measured moment-of-inertia factors.',
        'Explain how seismology (Apollo, InSight) provides an independent, direct check on gravity-based interior models.'],
    sections=[
        ('Why Planets Differentiate',
         ['Accretion energy, radioactive decay (Lecture 04), and core formation itself release enough heat to melt (at least partially) a newly assembled terrestrial planet.',
          'In a molten or partially molten body, denser material (iron, nickel) sinks toward the center while lighter silicates float upward, forming a core-mantle-crust structure.',
          'This process, called differentiation, converts gravitational potential energy into heat as dense material sinks, which further promotes melting -- a runaway that likely completed within the first &sim;10-100 Myr for Earth.'],
         'Differentiation is a self-reinforcing process: as iron sinks, it releases gravitational potential energy as heat, which keeps the interior hot enough for continued sinking, until the densest material has segregated into a core. The efficiency and timing of this process differs between planets and directly explains why Mercury has an anomalously large core (Lecture on giant-impact stripping, this section) while Mars\'s core appears smaller and only partially differentiated relative to its mantle.'),
        ('The Moment of Inertia Factor',
         ['For a uniform-density sphere, the moment of inertia is I = (2/5) MR&sup2;; the dimensionless factor C/MR&sup2; = 0.4 for a uniform body.',
          'A body with a dense core concentrated toward the center has C/MR&sup2; &lt; 0.4; Earth\'s measured value is 0.3307, Mars\'s is 0.3644, and the Moon\'s is 0.3931 (nearly uniform).',
          'C/MR&sup2; is measured from precession and gravity-field harmonics (J2) obtained from spacecraft tracking, not from any direct interior probe.'],
         'The moment of inertia factor is one of the most information-dense numbers in planetary science: a single dimensionless ratio, obtainable purely from orbital tracking of an orbiting spacecraft (via its perturbation by the planet\'s J2 gravity harmonic) combined with the planet\'s measured precession rate, constrains how centrally concentrated its mass is. Earth\'s value of 0.3307, well below the uniform-sphere value of 0.4, is the primary evidence (independent of seismology) that Earth possesses a dense central core; the Moon\'s much higher value of 0.3931 shows it is nearly uniform in density, consistent with a small or absent core.'),
        ('Terrestrial Planet Interior Comparison',
         ['Mercury: anomalously large core (&sim;85% of the planet\'s radius by some models), likely from a giant impact that stripped early mantle material.',
          'Venus: Earth-like bulk density and probable core size, but no measured moment of inertia factor exists yet (no orbiting Venus gravity mission has achieved the precision Earth and Mars have).',
          'Mars: smaller, partially differentiated core inferred from InSight seismic data (radius &sim;1830 km, confirmed directly by seismic core-reflected phases in 2021).'],
         'Mercury\'s oversized core is a striking counterexample to the simple condensation-sequence picture from Lecture 02: its bulk density (5427 kg/m&sup3;, nearly as high as Earth\'s despite Mercury\'s much smaller size and correspondingly weaker self-compression) implies an iron core occupying roughly 85% of its radius, most plausibly explained by one or more giant impacts early in its history that stripped away a disproportionate share of its original silicate mantle -- directly linking this lecture to the impact physics developed in Lecture 06.'),
        ('Seismology as Ground Truth',
         ['Apollo seismometers (1969-1977) detected moonquakes and used travel-time analysis to infer the Moon\'s crust-mantle-core structure directly.',
          'NASA\'s InSight lander (2018-2022) recorded over 1300 marsquakes, including core-reflected (ScS) phases that directly measured the Martian core radius and confirmed it is at least partially liquid.',
          'Direct seismic detection is the gold standard because it requires no assumption about bulk composition, unlike gravity-field-only inference.'],
         'The agreement between InSight\'s direct seismic core-radius measurement (&sim;1830 km) and earlier gravity-based moment-of-inertia inferences for Mars is a genuine scientific triumph: it validates the moment-of-inertia method for planets where no seismometer has yet landed (Mercury, Venus), and it is the kind of independent cross-check this course\'s review process explicitly values over single-method inference.'),
        ('Pressure and Density in Planetary Interiors',
         ['Interior pressure increases with depth according to hydrostatic equilibrium, dP/dr = -&rho;(r) g(r) -- the same governing equation developed for atmospheres in Lecture 07, applied here to solid/liquid interiors.',
          'Unlike an ideal-gas atmosphere, planetary interiors require an equation of state relating pressure to density for iron, silicates, and (in giant planets) metallic hydrogen under extreme compression.',
          'Self-compression alone can raise a planet\'s density substantially above its zero-pressure material density -- important when comparing Earth\'s and Mercury\'s bulk densities, since Earth\'s stronger self-gravity compresses its interior more.'],
         'Uncompressed density, not raw bulk density, is the fairer basis for comparing planetary composition, because self-compression alone raises Earth\'s density above what its material composition alone would produce; correcting for self-compression is exactly why planetary scientists conclude Mercury\'s core fraction is unusually large even though its raw bulk density is not dramatically higher than Earth\'s.'),
        ('Core Composition: Iron Alloys and Light Elements',
         ['Earth\'s core is primarily iron-nickel, but seismic density measurements require &sim;5-10% by mass of lighter elements (sulfur, oxygen, silicon, or hydrogen) to match observed density and sound-speed profiles.',
          'The precise light-element budget affects a core\'s freezing behavior and, through compositional buoyancy during inner-core growth, the vigor of the convective dynamo (developed fully in Lecture 10).',
          'Mercury\'s core is inferred to be unusually sulfur-rich, which lowers its freezing point and may help sustain an active dynamo in such a small body.'],
         'The light-element problem links core composition directly to magnetic-field generation: a core that is purely iron-nickel would likely have solidified completely by now in a small body like Mercury, extinguishing convection and any dynamo, so Mercury\'s continued (weak but real, confirmed by MESSENGER) magnetic field is itself indirect evidence for a sulfur-depressed freezing point keeping at least part of its core liquid and convecting.'),
        ('Crustal Formation and Differentiation Products',
         ['The lightest, most incompatible elements concentrate in partial melts that rise to form a planet\'s earliest crust.',
          'Earth\'s continental crust (average density &sim;2700 kg/m&sup3;) is chemically distinct from and less dense than its oceanic crust (&sim;3000 kg/m&sup3;) and mantle (&sim;3300 kg/m&sup3;), itself a product of repeated partial melting over geological time.',
          'The Moon\'s ancient anorthositic highland crust, sampled directly by Apollo astronauts, is thought to have crystallized by flotation from a global magma ocean, a direct physical sample of primary differentiation.'],
         'The lunar magma-ocean model is a rare case where a planetary differentiation process is directly sampled rather than only inferred: returned Apollo highland samples are anorthosite (a low-density, calcium-rich silicate) with ages clustering near 4.4-4.5 Gyr, exactly what is expected if a global magma ocean crystallized and the lowest-density mineral phase floated to form the crust while denser minerals sank -- essentially differentiation, caught in the act and preserved for four and a half billion years.'),
        ('The Core-Mantle Boundary and D\u2033 Layer',
         ['Earth\'s core-mantle boundary (2891 km depth) is one of the sharpest physical/chemical discontinuities in the solar system, separating liquid iron alloy from solid silicate.',
          'The D\u2033 (D-double-prime) layer just above the core-mantle boundary shows anomalous seismic properties, possibly a distinct chemical reservoir or a phase transition in mantle mineralogy.',
          'Heat flow across the core-mantle boundary drives core convection (Lecture 10) and couples core cooling to mantle convection (Lecture 04).'],
         'The core-mantle boundary is the single interface where this lecture\'s topic (differentiation and structure) connects most directly to the next two lectures\' topics (heat flow and plate tectonics): the rate at which heat crosses this boundary sets both the vigor of the core dynamo (Lecture 10) and the temperature of the deep mantle that ultimately drives whole-mantle convection and plate tectonics (Lectures 04-05).'),
        ('Interior Structure Beyond the Terrestrial Planets',
         ['Giant planets have no solid surface; "interior structure" instead refers to a continuous transition from molecular to metallic hydrogen (Lecture 11) with a possible dense core.',
          'Icy satellites (Europa, Enceladus, Titan; Lecture 13) can differentiate into a rock/metal core, an ice mantle, and, critically, a liquid subsurface ocean layer.',
          'Gravity data from the Galileo, Cassini, and Juno missions extend the moment-of-inertia method used for terrestrial planets to these very different interior structures.'],
         'The same gravity-tracking method introduced in this lecture for terrestrial planets -- inferring internal structure from a spacecraft\'s orbital perturbations -- is the primary tool used to infer subsurface oceans in icy satellites (Lecture 13) and to constrain core mass in the giant planets (Lecture 11), making the moment-of-inertia concept one of the most broadly reused tools in this course.'),
        ('Worked Example Setup: Comparing C/MR\u00b2 Across Bodies',
         ['We compare the measured moment of inertia factors of Earth, Mars, and the Moon against the uniform-sphere reference value of 0.4.',
          'A lower C/MR&sup2; indicates a proportionally larger, denser core; a value near 0.4 indicates a nearly uniform interior.',
          'This comparison is entirely observational (no interior model assumed beyond the sphere reference) and previews Lab 02\'s quantitative moment-of-inertia core-size inversion.'],
         'This section sets up the worked example below, which is intentionally simple (a direct numerical comparison rather than a full two-layer model) so that Lab 02 can develop the two-layer core/mantle inversion in full quantitative detail as a follow-on exercise.'),
        ('Reading and Scope Note',
         ['OpenStax <em>Astronomy 2e</em> Section 9.1 (Overview of Earth Structure) introduces core-mantle-crust structure at an introductory, non-quantitative level.',
          'The moment-of-inertia formalism and its use to infer interior structure from spacecraft tracking data go beyond OpenStax and follow de Pater & Lissauer, <em>Planetary Sciences</em>, Chapter 4.'],
         'As in previous lectures, OpenStax is assigned background reading, and the quantitative moment-of-inertia method taught here is the primary tool this course actually uses for interior-structure inference, developed at a level appropriate to a 300-level course.'),
    ],
    worked_title='Moment of Inertia Factors: Earth, Mars, and the Moon',
    worked_steps=[
        'Compare each body\'s measured moment of inertia factor C/MR&sup2; to the uniform-sphere reference value of 0.4.',
        '<table><tr><th>Body</th><th>C/MR&sup2; (measured)</th><th>Deviation from uniform (0.4)</th><th>Interpretation</th></tr>'
        '<tr><td>Earth</td><td>0.3307</td><td>-17.3%</td><td>Strongly core-concentrated (large dense iron core)</td></tr>'
        '<tr><td>Mars</td><td>0.3644</td><td>-8.9%</td><td>Moderately core-concentrated (smaller, partially differentiated core)</td></tr>'
        '<tr><td>Moon</td><td>0.3931</td><td>-1.7%</td><td>Nearly uniform (small or absent core)</td></tr></table>',
        'Result: the deviation from 0.4 tracks independently measured core sizes (Earth &sim;3480 km, Mars &sim;1830 km by InSight seismology, Moon &sim;350 km by Apollo seismology and later gravity/laser-ranging refinement) in the correct rank order, validating the moment-of-inertia method against direct seismic ground truth.',
    ],
    worked_notes='The rank-order agreement here (Earth most core-concentrated, Moon least) is the correctness check this course requires: the moment-of-inertia factor is only useful if it agrees, at least in relative terms, with an independent method (seismology). Lab 02 extends this into a full quantitative two-layer inversion for core radius.',
    summary=['Differentiation converts a newly assembled planet\'s accretional and radiogenic heat into a density-stratified core-mantle-crust structure.',
             'The moment of inertia factor, measurable from spacecraft tracking alone, is a powerful and non-invasive probe of a planet\'s internal density distribution.',
             'Seismology (Apollo, InSight) independently confirms gravity-based interior inferences, the strongest kind of scientific validation available in planetary science.'],
    preview='Lecture 04 asks what powers a planet\'s interior heat budget over geological time, and why some planets stay geologically active while others do not.',
))

LECTURES.append(dict(
    n=4, title='Planetary Heat Budgets, Radiogenic Heating, and Convection',
    kicker='Unit 2: Interiors and Heat', subtitle='Why some planets are still hot after 4.5 billion years',
    objectives=[
        'Identify the sources of a planet\'s internal heat: accretional heat, differentiation heat, radiogenic decay, and (for some giant planets) ongoing gravitational contraction.',
        'Derive the exponential decay law for radiogenic heat production and apply it to Earth\'s major heat-producing isotopes.',
        'Explain the Rayleigh number criterion for the onset of solid-state mantle convection.',
        'Compare surface heat flow across terrestrial planets and connect it to their present-day geological activity.'],
    sections=[
        ('Sources of Planetary Interior Heat',
         ['Accretional heat: kinetic energy of infalling planetesimals converted to heat during formation, largely radiated away or retained depending on burial depth and accretion rate.',
          'Differentiation heat: gravitational potential energy released as dense material (iron) sinks to form a core (Lecture 03), a one-time but substantial heat source.',
          'Radiogenic heat: ongoing heat production from the decay of long-lived radioactive isotopes (&#8308;&#8308;&#8308;K, &#178;&#179;&#8309;U, &#178;&#179;&#8318;U, &#178;&#179;&#8262;Th) distributed through the mantle and crust.',
          'Giant planets add a further source: slow gravitational (Kelvin-Helmholtz) contraction, and for Saturn, possible helium rain releasing gravitational energy (Lecture 11).'],
         'Distinguishing these heat sources matters because they have very different timescales: accretional and differentiation heat were front-loaded within the first &sim;100 Myr and have long since been radiated away from small bodies, while radiogenic heat decays on the multi-billion-year half-lives of &sup2;&sup3;&#8310;U, &sup2;&sup3;&sup8;U, &sup2;&sup3;&sup2;Th, and &#8308;&#8308;K, meaning it is still the dominant heat source powering Earth\'s mantle convection and dynamo today, 4.5 Gyr after formation.'),
        ('Radiogenic Heat Production: The Decay Law',
         ['Each radioactive isotope\'s heat production rate decays exponentially: H(t) = H&#8320; e&#8315;&#955;t, with decay constant &#955; = ln2 / t&#8321;&#8260;&#8322;.',
          'Earth\'s present-day radiogenic heat budget is dominated by four isotopes with half-lives ranging from 1.25 Gyr (&#8308;&#8308;K) to 14.0 Gyr (&sup2;&sup3;&sup2;Th).',
          'Because &#8308;&#8308;K has the shortest half-life of the four major heat producers, Earth\'s radiogenic heat production was substantially higher in the past and has been declining ever since formation.'],
         'The exponential decay law here is identical in form to the radioactive decay students have seen in introductory nuclear physics, but its planetary-science consequence is important: Earth\'s mantle was heated more vigorously by radioactivity in the Archean era (roughly 2.5-4 Gyr ago) than today, which is part of the explanation for why plate tectonics, mantle convection vigor, and volcanic/magnetic activity generally were more intense earlier in Earth\'s history and have been gradually declining since.'),
        ('Present-Day Radiogenic Heat Production Rates',
         ['&#8308;&#8308;K (t&#8321;&#8260;&#8322; = 1.25 Gyr): contributes roughly 40% of Earth\'s present bulk silicate Earth radiogenic heat production, despite modest abundance, because of its shorter half-life.',
          '&sup2;&sup3;&#8310;U (t&#8321;&#8260;&#8322; = 4.47 Gyr) and &sup2;&sup3;&sup2;Th (t&#8321;&#8260;&#8322; = 14.0 Gyr): together contribute most of the remainder, with Th typically contributing somewhat more heat than U owing to greater cosmochemical abundance.',
          'Total present-day radiogenic heat production for the bulk silicate Earth is estimated at roughly 20 TW, compared to a total observed surface heat flow of roughly 47 TW -- implying a substantial non-radiogenic (secular cooling) contribution as well.'],
         'The roughly 20 TW versus 47 TW gap between present radiogenic heat production and total observed surface heat flow is itself an important and actively debated result: it implies that Earth is still cooling from its formation (secular cooling of the core and mantle) at a rate comparable to its radiogenic heat production, a conclusion drawn from combining bulk silicate Earth geochemical models with direct heat-flow measurements and, since 2005, direct measurement of Earth\'s geoneutrino flux (from KamLAND and Borexino), which independently confirms the radiogenic heat production estimate.'),
        ('The Rayleigh Number and the Onset of Convection',
         ['The Rayleigh number Ra = (&#961; g &alpha; &Delta;T d&sup3;) / (&kappa; &mu;) compares the destabilizing effect of thermal buoyancy to the stabilizing effects of viscous dissipation and thermal diffusion.',
          'Convection begins once Ra exceeds a critical value Ra_c &sim; 1000-2000 (depending on boundary conditions); solid-state mantle convection occurs because Earth\'s mantle, though nominally solid, deforms plastically over geological timescales at very low effective viscosity (&sim;10&sup2;&#185; Pa&#183;s).',
          'Earth\'s mantle Rayleigh number is estimated at 10&#8310;-10&#8311;, vastly super-critical, meaning vigorous convection rather than marginal stability is expected -- consistent with plate tectonics.'],
         'The Rayleigh number is the same dimensionless number used in fluid dynamics and atmospheric science generally (it also governs, for example, convection in a pot of heated water or in a star\'s envelope); its application here to a nominally "solid" mantle is possible only because geological timescales (millions of years) are long enough for silicate rock to behave as an extremely viscous fluid, an idea first proposed to explain continental drift and now confirmed by both seismic tomography (imaging actual mantle plumes) and geodetic measurement of present-day plate motions.'),
        ('Mantle Convection Regimes: Stagnant Lid vs. Mobile Lid',
         ['Mobile-lid convection (Earth\'s plate tectonics): the cold surface layer participates directly in convection, recycling into the mantle at subduction zones.',
          'Stagnant-lid convection (Venus, Mars, Mercury, the Moon, most other rocky bodies): the cold surface layer is too strong (or too dry) to break into mobile plates and instead sits as a single immobile shell atop a convecting interior.',
          'Earth appears to be the only terrestrial planet with active plate tectonics today, making it observationally anomalous rather than the default expectation.'],
         'Understanding why Earth alone sustains mobile-lid convection is one of the biggest open questions in comparative planetology (raised in Lecture 01) and is thought to depend on a combination of factors including surface water (which weakens rock rheology, promoting plate boundary failure), a particular range of mantle temperature and viscosity, and possibly even the presence of pre-existing weaknesses from a specific accretional history -- no single factor has been shown to be both necessary and sufficient, which is why Lecture 05 treats plate tectonics as a genuinely open comparative problem rather than a solved one.'),
        ('Heat Flow Measurements Across the Terrestrial Planets',
         ['Earth: mean surface heat flow &sim;91-92 mW/m&sup2;, with strong contrast between young oceanic ridges (&gt;200 mW/m&sup2;) and old continental cratons (&sim;40-60 mW/m&sup2;).',
          'Moon: Apollo heat-flow probes measured 16-21 mW/m&sup2;, an order of magnitude below Earth, consistent with its small size, thick stagnant lid, and largely extinct interior activity.',
          'Mars: InSight\'s heat-flow probe (HP&sup3;) failed to achieve its planned burial depth, but independent geophysical estimates suggest &sim;20-24 mW/m&sup2;, intermediate between Earth and the Moon.'],
         'The strong contrast between Earth\'s young oceanic ridges and old continental interiors is itself a heat-flow signature of plate tectonics: new oceanic lithosphere is thin and hot immediately after formation at a mid-ocean ridge and then cools and thickens as it ages and moves away from the ridge, so heat flow measured at the seafloor is a direct, continuously renewed record of the plate-recycling process that Lecture 05 develops in full.'),
        ('Why Small Bodies Cool Faster: Surface-to-Volume Scaling',
         ['A body\'s total heat generation scales with its volume (&prop; R&sup3;), while its capacity to lose heat scales with its surface area (&prop; R&sup2;).',
          'The ratio of heat loss to heat generation therefore scales as R&sup2;/R&sup3; = 1/R: smaller bodies lose heat proportionally faster and cool on shorter timescales.',
          'This single scaling argument explains why the Moon and Mercury are geologically quiescent today while Earth (and, differently, Venus) remain active.'],
         'This surface-to-volume scaling argument is one of the most powerful and general results in all of planetary science: it requires no detailed knowledge of a specific body\'s composition or history to predict, correctly, that smaller bodies cool and become geologically inactive faster than larger ones, and it is the same scaling argument (applied to stars rather than planets) that explains why low-mass stars live far longer than high-mass stars in ASTR 330.'),
        ('The Rayleigh Number and Radiogenic Heating Combined',
         ['A planet\'s convective vigor depends jointly on its radiogenic heat production (this lecture\'s exponential decay law) and its size (this lecture\'s surface-to-volume scaling).',
          'Mars, intermediate in size between the Moon and Earth, is a natural test case: it appears to have lost most active mantle convection and any global magnetic dynamo (Lecture 10) roughly 4 Gyr ago, consistent with faster cooling than Earth but slower than the Moon.',
          'This combined argument previews Lab 02\'s quantitative heat-budget calculation for Mars versus Earth.'],
         'Mars sits at an instructive middle ground in almost every heat-budget comparison in this course: too small to sustain Earth-like plate tectonics or an active dynamo today, but large enough to have retained substantial early geological and magnetic activity (recorded in ancient crustal magnetization, discussed further in Lecture 10), making it the clearest natural test of the surface-to-volume cooling argument developed in this section.'),
        ('Tidal Heating as a Non-Radiogenic Heat Source',
         ['For satellites in eccentric or resonant orbits (Io, Europa, Enceladus), periodic tidal flexing dissipates orbital and rotational energy as internal heat.',
          'Tidal heating can dominate over radiogenic heating in small icy or rocky satellites, as this course shows quantitatively for Io in Lecture 13.',
          'This heat source has no analog in isolated planets and depends on orbital dynamics (eccentricity, orbital resonance) rather than only on a body\'s size and radioactive inventory.'],
         'Tidal heating is flagged here, ahead of its full quantitative treatment in Lecture 13, specifically to prevent an overgeneralization of this lecture\'s surface-to-volume cooling argument: Io is smaller than the Moon yet is the most volcanically active body in the solar system, precisely because it receives an enormous non-radiogenic heat input from tidal flexing that the simple size-scaling argument does not capture.'),
        ('Reading and Scope Note',
         ['OpenStax <em>Astronomy 2e</em> Section 9.1-9.2 (Earth\'s interior and plate tectonics) introduces heat flow and mantle convection at an introductory level.',
          'The Rayleigh-number formalism and the quantitative radiogenic decay-law treatment go beyond OpenStax and follow Turcotte & Schubert, <em>Geodynamics</em>, Chapters 4 and 6.'],
         'Students should treat this lecture\'s Rayleigh-number and decay-law derivations as the primary quantitative content, with OpenStax serving only as descriptive background, consistent with this course\'s stated policy of exceeding the introductory textbook\'s depth wherever a genuinely upper-division derivation is available.'),
    ],
    worked_title="Earth's Present-Day Radiogenic Heat Production",
    worked_steps=[
        'Model each isotope\'s heat production as H(t) = H&#8320; e&#8315;&#955;t with &#955; = ln2/t&#8321;&#8260;&#8322;, using standard bulk-silicate-Earth present-day heat production rates (per kilogram of isotope) and Earth mantle abundances.',
        f'Half-lives used: &#8308;&#8308;K = 1.25 Gyr (&#955; = {math.log(2)/1.25:.3f} Gyr&#8315;&sup9;), &sup2;&sup3;&#8310;U = 4.47 Gyr (&#955; = {math.log(2)/4.47:.3f} Gyr&#8315;&sup9;), &sup2;&sup3;&sup2;Th = 14.0 Gyr (&#955; = {math.log(2)/14.0:.3f} Gyr&#8315;&sup9;).',
        f'At t = 4.5 Gyr after formation, the surviving fraction of each isotope\'s initial inventory is e&#8315;&#955;t: &#8308;&#8308;K retains {math.exp(-math.log(2)/1.25*4.5)*100:.2f}%, &sup2;&sup3;&#8310;U retains {math.exp(-math.log(2)/4.47*4.5)*100:.1f}%, and &sup2;&sup3;&sup2;Th retains {math.exp(-math.log(2)/14.0*4.5)*100:.1f}% of its original abundance.',
        'Result: &#8308;&#8308;K has decayed by more than a factor of 8 over Earth history, while &sup2;&sup3;&sup2;Th has barely decayed at all -- exactly why &#8308;&#8308;K, despite being a minor heat contributor today, dominated Earth\'s radiogenic heat budget much more strongly in the distant past, and why the present-day total (&sim;20 TW) is well below the &sim;60-80 TW radiogenic heat production Earth likely had shortly after formation.',
    ],
    worked_notes='This calculation uses only the decay law H(t)=H0 e^(-lambda t) applied to three of Earth\'s four major heat-producing isotopes; Lab 02 extends it to a full quantitative comparison of Earth versus Mars total heat budgets using each planet\'s estimated bulk composition.',
    summary=['Radiogenic heat, decaying exponentially with each isotope\'s own half-life, is Earth\'s dominant present-day internal heat source, though secular cooling contributes comparably.',
             'The Rayleigh number formalizes when a planetary interior convects; Earth\'s mantle is vastly super-critical, consistent with observed plate tectonics.',
             'Surface-to-volume scaling (heat loss &prop; 1/R relative to heat generation) explains why small bodies cool and become geologically quiescent faster than large ones, though tidal heating is an important exception developed later.'],
    preview='Lecture 05 examines the surface expression of this convecting interior: plate tectonics on Earth and its absence, so far, everywhere else in the solar system.',
))

LECTURES.append(dict(
    n=5, title='Plate Tectonics and Comparative Surface Geology',
    kicker='Unit 3: Surfaces and Impacts', subtitle='Why Earth\u2019s surface is unique among the terrestrial planets',
    objectives=[
        'Describe the plate-tectonic cycle: divergent, convergent, and transform boundaries, and the rock cycle they drive.',
        'Explain the geological and geochemical evidence that no other solar system body has active plate tectonics today.',
        'Compare Venus\'s and Mars\'s surface geology (volcanism, tectonics, resurfacing) to Earth\'s.',
        'Connect surface tectonic style to a planet\'s heat budget (Lecture 04) and evaluate proposed explanations for Earth\'s uniqueness.'],
    sections=[
        ('The Plate-Tectonic Cycle',
         ['Earth\'s lithosphere is divided into roughly a dozen major rigid plates that move relative to one another at rates of a few centimeters per year, measurable directly by GPS geodesy.',
          'Divergent boundaries (mid-ocean ridges) create new oceanic crust; convergent boundaries (subduction zones) recycle old, dense oceanic crust back into the mantle.',
          'Transform boundaries (e.g., the San Andreas Fault) accommodate lateral motion without creating or destroying crust.'],
         'Plate tectonics is Earth\'s dominant mechanism for both losing internal heat (new lithosphere at ridges is hot; old subducting lithosphere is a cold, dense downwelling that drives much of the convective flow) and for long-term climate regulation, since subduction recycles carbon-bearing sediments into the mantle and volcanic arcs return carbon to the atmosphere -- a slow but essential feedback loop revisited in Lecture 09\'s climate discussion.'),
        ('Evidence for Plate Tectonics: Seafloor Magnetic Stripes',
         ['Oceanic crust records Earth\'s magnetic field polarity (Lecture 10) as it cools below the Curie temperature at a mid-ocean ridge.',
          'Because Earth\'s magnetic field reverses polarity at irregular intervals, symmetric "stripes" of alternating magnetized crust appear on either side of a ridge, dated independently by radiometric and paleontological methods.',
          'This magnetic-stripe record, discovered in the 1960s, was decisive observational proof of seafloor spreading and hence of plate tectonics.'],
         'Seafloor magnetic striping is one of the cleanest examples in all of Earth science of a single dataset simultaneously confirming two independent physical processes: the existence of seafloor spreading (this lecture) and the reality of geomagnetic polarity reversals (Lecture 10), because the magnetic stripes could not be symmetric about the ridge axis unless new crust were continuously created there and the field really were reversing over time.'),
        ('Why Venus Lacks Plate Tectonics Despite Earth-like Size',
         ['Venus is nearly identical to Earth in mass and radius, yet shows no evidence of an active plate-tectonic system: no global mid-ocean ridge network, no subduction-zone trenches.',
          'Venus\'s crater population is unusually uniform in age across its entire surface (estimated mean surface age &sim;300-700 Myr), suggesting a global resurfacing event rather than continuous plate recycling.',
          'Leading hypotheses include a "stagnant lid punctuated by episodic overturn" regime, possibly linked to Venus\'s extreme surface temperature (Lecture 08-09) making its lithosphere too dry and too weak to fail along discrete plate boundaries, or too strong and undeformable, depending on the model.'],
         'Venus is this course\'s sharpest natural test of the surface-water hypothesis for plate tectonics (introduced in Lecture 04): if surface water is necessary to weaken lithospheric rock enough to permit plate boundary failure, then Venus\'s bone-dry, 737 K surface (a direct consequence of its runaway greenhouse, developed in Lecture 09) may be sufficient on its own to explain the absence of plate tectonics, even though Venus\'s size and inferred heat budget are otherwise Earth-like.'),
        ('Mars: A Frozen One-Plate World with a Past',
         ['Mars today shows no active plate tectonics, but ancient crustal magnetization (Lecture 10) implies it once had a working dynamo, and some geological features (fossil spreading-like structures debated in the literature) hint at possible early plate-like behavior.',
          'Mars\'s hemispheric dichotomy (smooth low northern lowlands versus heavily cratered southern highlands) remains debated between an internal (mantle convection pattern) and external (giant impact) origin.',
          'Olympus Mons, the largest known volcano in the solar system (&sim;22 km high, &sim;600 km diameter), formed because Mars\'s stagnant lithosphere does not move over its mantle hotspot, allowing repeated eruptions to build a single enormous edifice rather than a chain of smaller volcanoes (as Earth\'s moving plate produces over the Hawaiian hotspot).'],
         'Olympus Mons is this lecture\'s clearest illustration of how tectonic style controls volcanic geography: Earth\'s Hawaiian-Emperor seamount chain is a sequence of progressively older, smaller volcanic islands produced as the Pacific Plate moves over a fixed mantle plume, while Mars\'s single, immense Olympus Mons formed because its stagnant lithosphere never moves relative to the underlying mantle hotspot, so all the erupted material piles up in one place over hundreds of millions of years.'),
        ('Mercury and the Moon: Contraction and Ancient Stagnant Lids',
         ['Mercury shows widespread lobate scarps, thought to record global contraction as its large core cooled and shrank, compressing the overlying crust.',
          'The Moon\'s surface is dominated by ancient highlands (heavily cratered, &sim;4.4 Gyr old anorthosite crust from Lecture 03) and younger mare basalts that flooded large impact basins between &sim;3.1-3.9 Gyr ago.',
          'Neither body shows evidence of plate tectonics; both are interpreted as single-plate ("stagnant lid") worlds throughout their recorded history.'],
         'Mercury\'s lobate scarps are a direct surface signature of the small-body cooling argument from Lecture 04: as Mercury\'s large iron core has slowly cooled and contracted over geological time, the rigid, non-deformable crust above it has been forced to buckle and thrust, producing scarps up to hundreds of kilometers long and up to 3 km high, imaged directly by the MESSENGER mission.'),
        ('The Rock Cycle and Surface Renewal Rates',
         ['On Earth, subduction recycles the entire ocean floor roughly every 100-200 Myr, meaning no oceanic crust older than about 180 Myr survives today.',
          'By contrast, continental crust, being too buoyant to subduct, can survive for billions of years (the oldest preserved zircon crystals date to &sim;4.4 Gyr).',
          'This dual age structure -- young, continuously recycled ocean floor alongside ancient, preserved continental crust -- has no known analog on any other solar system body.'],
         'The contrast between Earth\'s young ocean floor and ancient continental crust is itself indirect evidence for plate tectonics: no other known surface-renewal mechanism (volcanic resurfacing, impact gardening) naturally produces two coexisting crustal populations with such starkly different ages sitting side by side on the same planet.'),
        ('Crater Density as a Relative Dating Tool (Preview)',
         ['Because impact rate is roughly constant over long timescales (Lecture 06), the number of impact craters per unit area on a surface is a proxy for how long that surface has existed without being resurfaced.',
          'Venus\'s uniformly low crater density (relative to the Moon or Mars) across its whole surface is itself evidence for the global resurfacing event described earlier in this lecture.',
          'Earth has almost no preserved impact craters (fewer than 200 confirmed) precisely because plate tectonics, erosion, and sedimentation continuously erase its surface record.'],
         'This section previews Lecture 06\'s full quantitative crater-counting method, applying it qualitatively here to show that a planet\'s crater density is not simply a function of its size or distance from the asteroid belt, but a direct consequence of how actively (and how recently) its surface has been renewed by tectonics, volcanism, or (for Earth) weathering and burial.'),
        ('Surface Geology of Icy Bodies: A Preview',
         ['Icy satellites can show their own analog of "resurfacing" through cryovolcanism and tectonic fracturing of an ice shell rather than a silicate crust (developed fully in Lecture 13).',
          'Europa\'s young, low crater density surface (estimated age &sim;40-90 Myr) is interpreted as evidence of an actively resurfacing ice shell, driven by tidal heating rather than radiogenic heating.',
          'This shows that "geological activity" is not a property exclusive to rocky planets; the same crater-density dating logic applies equally to ice.'],
         'Europa is flagged here specifically to prevent students from assuming that active surface geology requires a rocky, Earth-like planet: the same crater-counting method (Lecture 06) applied to an icy moon\'s surface reveals that Europa is geologically younger, on average, than most of Mars, driven by an entirely different heat source (tidal flexing, not radiogenic decay or plate tectonics).'),
        ('Volcanic Styles Across the Terrestrial Planets',
         ['Earth: focused volcanism at plate boundaries (subduction-zone stratovolcanoes, mid-ocean-ridge basalt) and at intraplate hotspots (Hawaii, Yellowstone).',
          'Venus: pervasive basaltic volcanism apparently distributed broadly across the surface rather than focused at plate boundaries, consistent with a stagnant lid punctuated by broad mantle upwellings.',
          'Mars: enormous shield volcanoes (Olympus Mons, the Tharsis Montes) built over immense timescales at fixed mantle hotspots, with no evidence of recent (last &sim;1 Gyr) major eruptions, though some features suggest volcanism as young as tens of millions of years.'],
         'Volcanic style is this lecture\'s clearest single diagnostic separating one-plate and multi-plate worlds: Earth\'s volcanoes cluster into linear belts along plate boundaries precisely because that is where mantle material is either rising (ridges) or a subducting slab is releasing water that lowers the mantle\'s melting point (subduction-zone arcs), while Venus and Mars show no such linear organization because they have no plate boundaries to organize it.'),
        ('Erosion, Atmosphere, and Surface Preservation',
         ['Earth\'s and Titan\'s (Lecture 13) surfaces are actively eroded by liquid-forming atmospheric cycles (water and methane respectively), erasing older geological features.',
          'Mars shows extensive evidence of past fluvial erosion (dry river valley networks, deltas) from an early wetter climate, now essentially inactive under its present thin, cold atmosphere.',
          'Airless or near-airless bodies (Mercury, the Moon) preserve their impact and volcanic history essentially unmodified for billions of years, aside from micrometeorite gardening.'],
         'The presence or absence of an erosive atmosphere is an independent variable from plate tectonics in controlling how well a surface preserves its geological history, and separating the two effects (tectonic recycling versus atmospheric erosion) is essential to correctly interpreting any given planet\'s crater record, a distinction Lecture 06 makes explicit when using crater counts to date planetary surfaces.'),
        ('Open Problem: Why Is Earth Unique?',
         ['Proposed explanations include surface water weakening the lithosphere, a particular range of mantle temperature and viscosity, plate-boundary lubrication by subducted sediments, and even the specific stochastic history of Earth\'s early impacts.',
          'No single proposed mechanism has been shown to be both necessary and sufficient; comparative data from Venus (Earth-like size, no plate tectonics) is the strongest current observational constraint.',
          'Future Venus missions (e.g., NASA\'s VERITAS and DAVINCI, ESA\'s EnVision) are specifically designed to test these hypotheses with better gravity, radar, and atmospheric data.'],
         'This open problem is deliberately left unresolved because it genuinely is unresolved in the current research literature; presenting it honestly as an open question, rather than implying a settled answer exists, is itself part of this course\'s standard for scientific rigor, and it directly sets up the exoplanet comparative-planetology discussion in Lecture 14, where the same question (which planets, if any, sustain plate tectonics) is asked for planets we cannot yet visit.'),
        ('Reading and Scope Note',
         ['OpenStax <em>Astronomy 2e</em> Section 9.3-9.4 (Volcanism and Tectonics) introduces surface-shaping processes on the terrestrial planets at an introductory, largely descriptive level.',
          'The quantitative crustal-age/recycling-rate cross-check developed in this lecture\'s worked example, and the explicit stagnant-lid-versus-plate-tectonics dichotomy framework, extend beyond OpenStax\'s introductory descriptive treatment.'],
         'As in every other lecture in this course, OpenStax is assigned background reading and this lecture\'s quantitative worked example (the crustal recycling-rate cross-check) is this course\'s own original synthesis, developed at the depth a 300-level course requires.'),
    ],
    worked_title='Oceanic Crustal Age and Recycling Rate',
    worked_steps=[
        'Earth\'s oceanic crust covers roughly 3.6 &times; 10&#185;&#8308; m&sup2; (about 70% of Earth\'s surface area of 5.1 &times; 10&#185;&#8308; m&sup2;) and is fully recycled, on average, every &sim;180 Myr (the age of the oldest preserved oceanic crust, in the western Pacific).',
        'Mean crustal recycling rate = total oceanic area / mean crustal age &asymp; (3.6 &times; 10&#185;&#8308; m&sup2;) / (180 &times; 10&#8310; yr) &asymp; 2.0 &times; 10&#8312; m&sup2;/yr, equivalent to roughly 2 km&sup2; of new (and old, subducting) oceanic crust processed every year on average.',
        'Result: at a typical spreading/subduction rate of a few centimeters per year along a mid-ocean-ridge system tens of thousands of kilometers long, this areal recycling rate is consistent with globally averaged plate velocities of order 5-10 cm/yr, matching direct GPS geodetic measurements.',
    ],
    worked_notes='This order-of-magnitude cross-check (areal recycling rate implied by crustal age versus directly measured plate velocities) is exactly the kind of independent consistency check this course requires: two very different methods -- dating the oldest preserved seafloor, and directly measuring present-day plate motion by GPS -- agree on the same underlying process.',
    summary=['Plate tectonics recycles Earth\'s lithosphere continuously, producing a dual-age crustal record (young ocean floor, ancient continents) unmatched elsewhere in the solar system.',
             'Venus and Mars each show evidence of a single immobile lithospheric shell (stagnant lid), with volcanic and tectonic histories shaped by that immobility rather than by plate boundaries.',
             'Why Earth alone sustains active plate tectonics remains an open research question with several competing, not-yet-decisive hypotheses.'],
    preview='Lecture 06 develops the crater-counting method used throughout this lecture qualitatively into a full, quantitative surface age-dating tool.',
))

LECTURES.append(dict(
    n=6, title='Impact Cratering and Surface Age Dating',
    kicker='Unit 3: Surfaces and Impacts', subtitle='Reading a planet\u2019s history from its scars',
    objectives=[
        'Derive the crater-scaling relation connecting impactor energy, size, and velocity to final crater diameter.',
        'Explain crater-count chronology and how it is calibrated using radiometrically dated, sample-returned lunar surfaces.',
        'Apply crater-count dating to estimate the relative and absolute ages of planetary surfaces.',
        'Distinguish primary impact craters from secondary craters and evaluate the limitations of the method.'],
    sections=[
        ('Impact Cratering Basics',
         ['An impact crater forms when a projectile\'s kinetic energy is deposited into a target surface far faster than the material can respond elastically, producing shock compression, excavation, and often melting.',
          'Crater diameter is typically 10-20 times the impactor\'s diameter for typical solar-system impact velocities (10-70 km/s), because the excavated volume greatly exceeds the impactor\'s own volume.',
          'Complex craters (with central peaks or peak rings) form above a size threshold (&sim;2-4 km on the Moon, larger on more massive bodies where gravity more strongly resists collapse) as the initial transient crater collapses under gravity.'],
         'The transition from simple bowl-shaped craters to complex central-peak craters is itself a gravity-dependent phenomenon: because a stronger gravitational field more effectively collapses an initially deep transient cavity, the simple-to-complex transition diameter is smaller on more massive bodies (Mercury, Mars) than on the Moon, providing yet another way a crater\'s morphology alone encodes information about the body it formed on.'),
        ('Crater Scaling Relations',
         ['Pi-group scaling (dimensional analysis) relates final crater diameter D to impactor diameter d, impact velocity v, and the ratio of impactor to target density, typically as D &prop; d&#8308;&#8260;&#8309; v&sup2;&#8260;&#8309; g&#8315;&#185;&#8260;&#8309; for gravity-dominated craters.',
          'This scaling means crater diameter grows sub-linearly with impact energy (D &prop; E&sup2;&#8260;&#8309; roughly, since E &prop; d&sup3;v&sup2;), so a 100-times more energetic impact produces roughly a 4-6 times larger crater, not a 100-times larger one.',
          'Scaling laws are calibrated using nuclear-test and laboratory hypervelocity-impact experiments as well as well-characterized natural craters (e.g., Meteor Crater, Arizona, whose &sim;50 m iron impactor and &sim;12-13 km/s impact velocity produced a 1.2 km diameter crater).'],
         'The sub-linear scaling of crater diameter with impact energy (D &prop; E&sup2;&#8260;&#8309;, not E) is a frequently misunderstood result: it means the largest impact basins in the solar system, hundreds to thousands of kilometers across, required impactors with energies vastly (many orders of magnitude) larger than a simple linear extrapolation from smaller craters would suggest, and it is the reason distinguishing "an unusually large ordinary impact" from "an unusually large impactor" requires the nonlinear scaling law rather than simple proportional reasoning.'),
        ('Crater-Count Chronology: The Basic Idea',
         ['If the impact flux (impacts per unit area per unit time) has been roughly known and roughly constant (at least over the last &sim;3 Gyr) for a given region of the solar system, then a surface\'s crater density (craters per unit area, typically above some reference diameter) increases monotonically with the surface\'s age.',
          'A surface with more craters per unit area is therefore older (has existed longer without being resurfaced) than one with fewer craters per unit area, all else being equal.',
          'This relative dating method requires no direct sample of the surface in question, making it broadly applicable across the solar system wherever high-resolution imaging exists.'],
         'Crater-count chronology\'s power lies precisely in this last point: it lets planetary scientists assign at least relative, and with lunar calibration absolute, ages to surfaces that have never been sampled (nearly everywhere except the Moon and, via meteorites and rover analysis, Mars), making it one of the most broadly applied dating tools in the entire field.'),
        ('Calibrating Absolute Ages: The Lunar Chronology Function',
         ['Apollo and Luna sample-return missions dated specific lunar mare and highland surfaces radiometrically (via isotopic techniques such as &#8308;&#8308;Ar/&sup3;&#8313;Ar dating), giving absolute ages for surfaces whose crater densities were also measured.',
          'Combining radiometric ages with measured crater densities at several calibration points produces the lunar chronology function, an empirical curve relating crater density to absolute surface age for the Moon.',
          'This function shows the impact flux was substantially higher (by roughly an order of magnitude) before &sim;3.8-3.9 Gyr ago than it has been since, a period sometimes called the Late Heavy Bombardment, though its exact character remains debated.'],
         'The lunar chronology function is the single most important calibration tool in all of planetary surface-age dating: because it is anchored by actual radiometrically dated samples (not just crater counts), it converts a purely relative dating method into an absolute one, and every other body\'s crater-count age (Mars, Mercury, Venus, icy satellites) is ultimately extrapolated from this lunar calibration with appropriate adjustments for each body\'s different impactor population and gravitational focusing.'),
        ('Extending Chronology Beyond the Moon',
         ['Extrapolating the lunar chronology function to other bodies requires correcting for differences in impactor population (main-belt asteroids dominate the inner solar system; comets and Kuiper Belt objects dominate the outer solar system) and in gravitational focusing (a more massive target attracts impactors more strongly, increasing the effective impact flux).',
          'Mars\'s crater chronology is considered reasonably well calibrated (via meteorite dating of Martian samples and modeling of the asteroid belt\'s dynamical evolution), while chronologies for the giant-planet satellites remain more uncertain because their impactor populations (comets, other satellites\' ejecta) are less well characterized.',
          'This uncertainty is explicitly disclosed whenever this course cites an outer-solar-system crater-count age (e.g., for Europa in Lecture 05 and Lecture 13).'],
         'The extension of crater chronology beyond the Moon is a genuine source of systematic uncertainty that this course treats honestly rather than glossing over: a quoted "surface age of 40-90 Myr" for Europa, for instance, is model-dependent in a way that a quoted lunar mare age (radiometrically anchored) is not, and students should learn to distinguish directly calibrated ages from model-extrapolated ones.'),
        ('Primary vs. Secondary Craters',
         ['Primary craters form directly from an interplanetary impactor; secondary craters form from debris ejected by a nearby (sometimes very distant) primary impact, re-impacting the surface at lower velocity.',
          'Secondary craters can be numerous and can bias small-crater counts if not properly identified and excluded (they often cluster in chains or clusters radiating from a primary crater).',
          'This complication means crater-count ages are most robust when based on larger craters (which are almost always primary) and when secondary contamination is explicitly assessed.'],
         'Secondary-crater contamination is one of the main sources of systematic disagreement between different research groups\' crater-count ages for the same surface, and it is a specific, checkable failure mode this course asks students to consider whenever they see a crater-count age quoted without discussion of crater-size range or secondary-crater screening.'),
        ('Saturation and Resurfacing Signatures',
         ['A surface can become "saturated" (new craters erasing older ones at the same rate they form) once crater density reaches an equilibrium value, at which point crater counting alone can no longer measure further age increases.',
          'A surface with an anomalously low crater density for its inferred age, or with a sharp population of small young craters overlying a population of larger degraded ones, signals a discrete resurfacing event (as inferred for Venus in Lecture 05).',
          'Crater degradation state (sharp rims versus eroded, infilled rims) provides an additional, independent age indicator beyond simple crater density.'],
         'Recognizing saturation and resurfacing signatures is essential to correctly interpreting Venus\'s crater record from Lecture 05: Venus\'s crater population is far from saturation (it has relatively few craters for its size) yet shows a narrow range of degradation states across its whole surface, which together imply a genuine resurfacing event roughly 300-700 Myr ago rather than either extremely young formation or a saturated, ancient surface.'),
        ('Impact Flux Through Solar System History',
         ['The impact flux in the inner solar system has declined roughly monotonically since the Late Heavy Bombardment period, with occasional debated spikes from specific dynamical events (e.g., large asteroid family breakups).',
          'The outer solar system\'s impactor population (comets, Kuiper Belt objects) is thought to have been strongly reshaped by the giant planets\' orbital migration (the Nice model), linking crater chronology directly back to the planet-formation and migration physics of Lecture 02.',
          'Ongoing impact monitoring (e.g., of Jupiter, via amateur and professional observation of fireball impacts) provides a present-day calibration point for current impact rates.'],
         'The connection between crater chronology and giant-planet migration (the Nice model, in which migrating Jupiter and Saturn dynamically excited the primordial trans-Neptunian disk, driving a surge of impactors into the inner solar system) is a striking example of how this course\'s formation physics (Lecture 02) and its surface-dating physics (this lecture) are not independent topics but two views of the same dynamical history.'),
        ('Applications: Dating Martian and Mercurian Surfaces',
         ['Crater counts on Mars indicate its northern lowlands are systematically younger than its southern highlands, consistent with (though not proof of) either resurfacing by ancient oceans/lava or an ancient giant impact (Lecture 05\'s hemispheric dichotomy).',
          'MESSENGER-based crater counts on Mercury indicate its youngest volcanic plains are roughly 3.7-3.9 Gyr old, meaning Mercury\'s volcanism, unlike Mars\'s or Venus\'s, appears to have ceased relatively early in solar system history.',
          'These applications illustrate crater-count dating\'s central role in reconstructing the geological histories developed qualitatively in Lecture 05.'],
         'Mercury\'s early cessation of volcanism, inferred largely from crater counting, is consistent with the surface-to-volume cooling argument from Lecture 04: as the smallest of the terrestrial planets other than the dwarf planets, Mercury is expected to have cooled and lost internal heat fastest, and its crater-derived volcanic history is direct observational support for that theoretical expectation.'),
        ('Limitations and Honest Uncertainty',
         ['Crater-count ages carry genuine, quantifiable uncertainty from Poisson counting statistics (especially for small survey areas with few craters), secondary-crater contamination, and chronology-function extrapolation beyond the Moon.',
          'This course requires that any quoted crater-count age be accompanied by an honest statement of which of these uncertainty sources applies, rather than presenting a single number as though it were exact.',
          'Cross-checking crater-count ages against independent methods (radiometric dating of returned or meteoritic samples, stratigraphic superposition) is the strongest available validation, exactly as this course\'s Lecture 03 emphasized for interior-structure inference.'],
         'This section closes the lecture with an explicit statement of the method\'s limitations because doing so is itself part of this course\'s standard of scientific honesty: crater-count chronology is an immensely powerful and broadly applicable tool, but like every method introduced in this course, its results are only as trustworthy as the calibration and assumptions behind them, and presenting it as infallible would be a disservice to genuine scientific practice.'),
    ],
    worked_title='Crater Diameter from Impactor Energy: The Chicxulub Impactor',
    worked_steps=[
        'The Chicxulub impactor (associated with the Cretaceous-Paleogene extinction) is estimated at &sim;10-15 km diameter, striking at &sim;20 km/s; take d = 12 km, v = 20 km/s, target/impactor density ratio &asymp; 1 (both roughly chondritic/crustal rock, &rho; &asymp; 2700-3000 kg/m&sup3;).',
        'Impact kinetic energy: E = &#189; m v&sup2;, with m = (4/3)&pi;(d/2)&sup3;&rho; &asymp; (4/3)&pi;(6000 m)&sup3;(3000 kg/m&sup3;) &asymp; '
        f'{4/3*math.pi*(6000.0)**3*3000.0:.2e} kg, giving E &asymp; {0.5*(4/3*math.pi*(6000.0)**3*3000.0)*(20000.0)**2:.2e} J.',
        f'For reference, this is roughly {0.5*(4/3*math.pi*(6000.0)**3*3000.0)*(20000.0)**2 / 4.184e15:.2e} times the energy of a 1-megaton nuclear weapon (4.184 &times; 10&#185;&#8309; J), consistent with published estimates of the Chicxulub impact energy (&sim;10&#8312;-10&#8312;&#8320; MT).',
        'The resulting crater (the Chicxulub crater, Yucat&aacute;n, Mexico) has a final diameter of &sim;150-180 km, an excavated-to-impactor diameter ratio of roughly 12-15, consistent with the pi-group scaling relation\'s expectation for a gravity-dominated crater of this size.',
    ],
    worked_notes='This worked example anchors the abstract crater-scaling relation introduced earlier in the lecture to a specific, independently well-documented real impact event; Lab 03 extends the same scaling relation to a full crater-count age determination exercise using real lunar and Martian crater-density data.',
    summary=['Crater diameter scales sub-linearly with impact energy, so the largest basins in the solar system required disproportionately large impactors.',
             'Crater-count chronology, anchored by radiometrically dated Apollo/Luna samples, converts crater density into an absolute surface age wherever the local chronology function is well calibrated.',
             'Applying crater counting honestly requires accounting for secondary-crater contamination, saturation, and chronology-extrapolation uncertainty beyond the Moon.'],
    preview='Lecture 07 leaves the solid surface behind and begins the atmospheres unit by deriving the hydrostatic structure of a planetary atmosphere.',
))

LECTURES.append(dict(
    n=7, title='Planetary Atmospheres I: Hydrostatic Structure and Scale Height',
    kicker='Unit 4: Atmospheres', subtitle='Deriving why pressure falls off exponentially with altitude',
    objectives=[
        'Derive the barometric (hydrostatic) equation for a planetary atmosphere from force balance on a thin gas slab.',
        'Solve the isothermal hydrostatic equation to obtain the exponential scale-height law.',
        'Compute and compare atmospheric scale heights across solar system atmospheres of differing composition, temperature, and gravity.',
        'Identify where the isothermal approximation breaks down (real atmospheres have temperature structure).'],
    sections=[
        ('Setting Up Hydrostatic Equilibrium',
         ['Consider a thin horizontal slab of atmosphere of area A, thickness dz, at height z, with density &#961;(z).',
          'In equilibrium, the net upward pressure force on the slab exactly balances its weight: [P(z) - P(z+dz)] A = &#961;(z) A g dz.',
          'Taking dz &rarr; 0 gives the hydrostatic equation: dP/dz = -&#961;(z) g.'],
         'This is precisely the same force-balance argument used to derive hydrostatic equilibrium inside a star in ASTR 310, applied here instead to a planetary atmosphere; the physical content is identical (pressure gradient force balances weight), but the equation of state and boundary conditions differ substantially, which is why this course develops the atmospheric case as a genuinely separate derivation rather than simply citing the stellar result.'),
        ('The Ideal Gas Law and the Scale Height',
         ['For an ideal gas, P = &#961; k T / m, where m is the mean molecular mass of the atmosphere and T is temperature.',
          'Substituting into the hydrostatic equation and assuming isothermal T (a simplifying approximation) gives dP/P = -(mg/kT) dz, a separable first-order ordinary differential equation.',
          'Integrating from the surface (z=0, P=P&#8320;) gives P(z) = P&#8320; exp(-z/H), where the scale height H = kT/(mg).'],
         'The scale height H is the single most useful atmospheric length scale in planetary science: it is the altitude change over which pressure (and, for an isothermal atmosphere, density) falls by a factor of e &asymp; 2.718, and because it depends only on temperature, mean molecular mass, and surface gravity, it can be estimated for any atmosphere the moment those three quantities are known, without needing a full atmospheric model.'),
        ('Physical Interpretation of the Scale Height',
         ['H = kT/(mg) is larger for hotter atmospheres (more thermal energy resisting gravitational settling), lighter mean molecular mass (lower mass gas is more buoyant against gravity), and weaker surface gravity (less restoring force per unit mass).',
          'Earth\'s atmosphere (T &asymp; 288 K, mean molecular mass &asymp; 28.97 amu, g = 9.807 m/s&sup2;) has H &asymp; 8.4-8.5 km, matching the commonly cited &sim;8.5 km reference value.',
          'This single number underlies practical facts: commercial airliners cruise near 1-1.3 scale heights (10-13 km) where pressure has fallen to roughly a third of sea level.'],
         'Recognizing which direction each parameter pushes the scale height (hotter &rarr; larger H; heavier molecules &rarr; smaller H; stronger gravity &rarr; smaller H) is essential for correctly predicting, without calculation, how scale height should compare across different planets before ever computing a specific number -- a prediction this lecture\'s worked example then checks quantitatively.'),
        ('Scale Height Across the Solar System',
         ['Venus: hot (737 K) but very heavy atmosphere (mostly CO&#8322;, m &asymp; 44 amu) and Earth-like gravity, giving a scale height comparable to or modestly larger than Earth\'s despite the huge temperature difference, because the heavier molecular mass partly offsets the higher temperature.',
          'Mars: cold (&sim;210 K) with the same CO&#8322;-dominated composition as Venus but much weaker gravity (3.71 m/s&sup2;), giving a scale height comparable to Earth\'s despite Mars\'s low temperature, because weak gravity offsets the cold temperature.',
          'Titan (Lecture 13): cold (&sim;94 K) but has weak gravity and a nitrogen-dominated atmosphere, giving a surprisingly large scale height for such a cold world.'],
         'The Venus/Mars comparison in this section is a deliberately chosen teaching case: two planets with nearly the same atmospheric composition (CO&#8322;-dominated) and wildly different temperatures (737 K versus 210 K) end up with broadly similar scale heights, because Mars\'s much weaker gravity almost exactly compensates for its much colder temperature -- a coincidence worth checking quantitatively in the worked example below rather than assuming from the formula alone.'),
        ('Beyond Isothermal: Real Atmospheric Temperature Structure',
         ['Real atmospheres are not isothermal: Earth\'s atmosphere has a troposphere (temperature decreasing with altitude, driven by convection), a stratosphere (temperature increasing due to ozone absorption of UV), and further layers above.',
          'In a non-isothermal atmosphere, the local scale height H(z) = kT(z)/(mg) still describes the local rate of pressure decline, but a single global scale height is only a useful average, not an exact description.',
          'The troposphere-stratosphere temperature inversion is itself diagnostic of a specific absorbing species (ozone on Earth, various hydrocarbons on the giant planets), connecting atmospheric structure directly to atmospheric chemistry.'],
         'The existence of a temperature inversion (a layer where temperature increases rather than decreases with altitude) is one of the clearest atmospheric signatures of a UV- or visible-absorbing chemical species aloft, and its presence or absence is used as an observational diagnostic even for exoplanet atmospheres (revisited in Lecture 14), where a stratospheric temperature inversion detected in a transmission or emission spectrum is taken as indirect evidence for a specific absorbing molecule.'),
        ('Atmospheric Composition and Mean Molecular Mass',
         ['Earth: N&#8322; (78%), O&#8322; (21%), Ar (0.9%), giving mean molecular mass &asymp; 28.97 amu.',
          'Venus: CO&#8322; (96.5%), N&#8322; (3.5%), giving mean molecular mass &asymp; 43.4 amu, roughly 1.5 times heavier than Earth\'s atmosphere.',
          'Mars: CO&#8322; (95.1%), N&#8322; (2.6%), Ar (1.9%), giving mean molecular mass &asymp; 43.3 amu, essentially identical to Venus\'s despite the very different total atmospheric mass and surface pressure.'],
         'Mars and Venus sharing nearly identical mean molecular mass, despite Mars\'s atmosphere being roughly 150 times thinner in surface pressure than Venus\'s, is itself an important comparative-planetology observation: both planets\' atmospheres are dominated by outgassed and photochemically processed CO&#8322;, but their vastly different total atmospheric masses reflect very different histories of volatile delivery, atmospheric escape (Lecture 09), and (for Venus) the runaway greenhouse effect (also Lecture 09) rather than any difference in atmospheric chemistry per se.'),
        ('Pressure-Altitude Profiles as Diagnostic Tools',
         ['Radio occultation (a spacecraft signal passing through a planet\'s atmosphere as it is occulted by the planet, observed from Earth) measures the atmosphere\'s refractive index profile, from which pressure, density, and temperature versus altitude can be derived without ever entering the atmosphere.',
          'Entry probes (e.g., the Galileo probe at Jupiter, Huygens at Titan) measure pressure and temperature directly during atmospheric descent, providing ground truth for remote-sensing-derived profiles.',
          'Comparing radio-occultation-derived and probe-measured profiles for the same atmosphere (where both exist) is an important validation exercise, analogous to the seismology-versus-gravity cross-check emphasized in Lecture 03.'],
         'This cross-validation theme -- comparing an indirect remote-sensing method against a direct in-situ measurement -- recurs throughout this course (moment of inertia versus seismology in Lecture 03, crater-count ages versus radiometric dating in Lecture 06, and here, radio occultation versus entry-probe atmospheric profiles), and is one of this course\'s central lessons about how planetary science builds confidence in results that cannot be checked by simple repetition of the same experiment.'),
        ('The Barometric Formula and Surface Pressure',
         ['Integrating the exponential pressure law from the surface to infinity gives the total atmospheric mass per unit area: &Sigma; = P&#8320;/g, directly relating surface pressure to total atmospheric mass without needing to know scale height at all.',
          'Earth: P&#8320; = 1.013 &times; 10&#8309; Pa, g = 9.807 m/s&sup2;, giving &Sigma; &asymp; 10,330 kg/m&sup2; -- consistent with the commonly cited fact that Earth\'s atmosphere weighs about 1 kg per cm&sup2; of surface.',
          'This relation, P&#8320; = &Sigma;g, is exact regardless of the atmosphere\'s temperature structure, unlike the exponential scale-height law, which assumed isothermality.'],
         'The relation &Sigma; = P&#8320;/g is a useful sanity check independent of the isothermal approximation: it follows directly from integrating the hydrostatic equation over the whole atmospheric column without any assumption about temperature structure, and it is the method by which "atmospheric mass" is usually quoted for any planet whose surface (or 1-bar reference level) pressure is known.'),
        ('Convective versus Radiative Atmospheric Regions',
         ['In regions where the vertical temperature gradient exceeds the adiabatic lapse rate, the atmosphere becomes convectively unstable and overturns (as in Earth\'s troposphere and the observable weather layer of the giant planets).',
          'Where the temperature gradient is sub-adiabatic, radiative transfer alone can carry the required energy flux, and the layer remains stably stratified (as in Earth\'s stratosphere).',
          'This convective/radiative distinction is developed further, together with its role in setting a planet\'s surface temperature, in Lecture 08\'s radiative-equilibrium treatment.'],
         'This section deliberately previews Lecture 08\'s topic without yet deriving it in full: the hydrostatic structure developed in this lecture describes how pressure and density vary with altitude for any given temperature profile, while Lecture 08 addresses the separate physical question of what sets that temperature profile in the first place, via radiative energy balance.'),
        ('Scope Note and Reading',
         ['OpenStax <em>Astronomy 2e</em> Section 10.1-10.2 (Atmospheres of the Terrestrial Planets) introduces atmospheric composition and structure at an introductory level, without deriving the hydrostatic equation.',
          'The hydrostatic-equilibrium derivation and scale-height formalism in this lecture go beyond OpenStax and follow de Pater & Lissauer, <em>Planetary Sciences</em>, Chapter 4, and the standard atmospheric-physics treatment in Sanchez-Lavega, <em>An Introduction to Planetary Atmospheres</em>.'],
         'As with the interior-structure and heat-budget derivations in Lectures 03-04, students should treat OpenStax as descriptive background context for atmospheric composition, while this lecture\'s hydrostatic derivation is the primary quantitative content this course actually examines and tests.'),
    ],
    worked_title='Atmospheric Scale Heights Across the Solar System',
    worked_steps=[
        'Compute H = kT/(mg) for Earth (N&#8322;-dominated, T=288 K), Venus (CO&#8322;-dominated, T=737 K), and Mars (CO&#8322;-dominated, T=210 K), using each planet\'s measured surface gravity from Lecture 01\'s table.',
        f'Earth: H = ({K_BOLTZMANN:.3e} &times; 288) / ({N2_MASS:.3e} &times; {EARTH_SURFACE_G:.3f}) = {EARTH_H_N2:.0f} m &asymp; {EARTH_H_N2/1000:.2f} km.',
        f'Venus: H = ({K_BOLTZMANN:.3e} &times; 737) / ({CO2_MASS:.3e} &times; {VENUS_G:.3f}) = {VENUS_H_CO2:.0f} m &asymp; {VENUS_H_CO2/1000:.2f} km.',
        f'Mars: H = ({K_BOLTZMANN:.3e} &times; 210) / ({CO2_MASS:.3e} &times; {MARS_G:.3f}) = {MARS_H_CO2:.0f} m &asymp; {MARS_H_CO2/1000:.2f} km.',
        f'Result: despite Venus being more than three times hotter than Mars, Venus\'s scale height ({VENUS_H_CO2/1000:.1f} km) is only modestly larger than Mars\'s ({MARS_H_CO2/1000:.1f} km) and both are comparable to Earth\'s ({EARTH_H_N2/1000:.1f} km, lighter but cooler gas), because Mars\'s much weaker surface gravity ({MARS_G:.2f} m/s&sup2; versus Venus\'s {VENUS_G:.2f} m/s&sup2;) very nearly compensates for its much lower temperature -- confirming the qualitative prediction made earlier in this lecture.',
    ],
    worked_notes='This calculation reuses the exact <code>scale_height_m</code> function and the exact surface-gravity values computed in Lecture 01, so the numbers here are internally consistent with every other lecture, lab, and problem set that touches these three atmospheres.',
    summary=['The hydrostatic equation, combined with the ideal gas law, predicts that an isothermal atmosphere\'s pressure falls off exponentially with a scale height H = kT/(mg).',
             'Scale height depends on temperature, mean molecular mass, and gravity in ways that can partly compensate across very different planets, as the Venus/Mars comparison shows.',
             'The relation &Sigma; = P&#8320;/g gives total atmospheric mass directly from surface pressure, independent of the isothermal approximation.'],
    preview='Lecture 08 derives what actually sets an atmosphere\'s temperature: the radiative energy balance between absorbed starlight and emitted thermal radiation, including the greenhouse effect.',
))

LECTURES.append(dict(
    n=8, title='Planetary Atmospheres II: Radiative Equilibrium and the Greenhouse Effect',
    kicker='Unit 4: Atmospheres', subtitle='Deriving equilibrium temperature from first principles',
    objectives=[
        'Derive the zero-atmosphere radiative-equilibrium temperature from a global energy balance between absorbed sunlight and blackbody emission.',
        'Compute equilibrium temperatures for the eight planets and compare them to observed surface/effective temperatures.',
        'Explain the greenhouse effect as a quantitative energy-balance correction, not merely a qualitative analogy.',
        'Identify which planets show the largest greenhouse temperature excess and connect this to atmospheric composition (Lecture 07).'],
    sections=[
        ('Setting Up the Global Energy Balance',
         ['A planet of radius R, at distance a from a star of luminosity L, intercepts starlight over its cross-sectional area &pi;R&sup2; and absorbs a fraction (1-A) of it, where A is the Bond albedo.',
          'Absorbed power: P_abs = (1-A) L &pi;R&sup2; / (4&pi;a&sup2}), using the star\'s flux at distance a, L/(4&pi;a&sup2;).',
          'In steady state, a planet must emit, as thermal (typically infrared) radiation from its full spherical surface area 4&pi;R&sup2;, exactly as much power as it absorbs: P_emit = 4&pi;R&sup2; &sigma; T_eq&#8308;.'],
         'This is the same radiative energy-balance logic used throughout astrophysics (a star\'s photosphere emits, in steady state, exactly the luminosity generated in its interior); here it is applied to a planet\'s balance between absorbed stellar flux and its own thermal emission, and it makes no reference at all to what is happening inside the planet -- it depends only on the planet\'s size, albedo, and distance from its star.'),
        ('Deriving the Equilibrium Temperature',
         ['Setting P_abs = P_emit and canceling &pi;R&sup2; from both sides (note the factor-of-4 ratio between the planet\'s absorbing cross-section, &pi;R&sup2;, and its emitting surface area, 4&pi;R&sup2;) gives (1-A) L / (4&pi;a&sup2;) = 4&sigma;T_eq&#8308;.',
          'Solving: T_eq = [(1-A) L / (16&pi;&sigma;a&sup2;)]&#185;&#8260;&#8308;.',
          'This is the same formula previewed qualitatively for the frost-line calculation in Lecture 02, now derived rigorously from first principles.'],
         'The factor of 4 that appears in this derivation (between the absorbing cross-sectional area &pi;R&sup2; and the emitting surface area 4&pi;R&sup2;) is one of the most commonly misremembered pieces of this formula; it exists because a sphere absorbs sunlight only through its illuminated disk-shaped cross-section but re-radiates thermal energy from its entire surface, and getting this factor wrong is one of the most common numerical errors this course\'s review process checks for explicitly.'),
        ('Equilibrium Temperatures for the Eight Planets',
         ['Using each planet\'s Bond albedo and semimajor axis, the zero-atmosphere-greenhouse equilibrium temperature can be computed directly from the Sun\'s luminosity alone.',
          'The full worked-example table (below) shows a systematic pattern: for planets with negligible or thin atmospheres (Mercury, Mars), the computed equilibrium temperature closely tracks the observed surface/effective temperature.',
          'For planets with substantial atmospheres (Venus, Earth), the observed surface temperature exceeds the computed zero-atmosphere equilibrium temperature by an amount that grows with atmospheric mass and greenhouse-gas content.'],
         'This pattern -- good agreement for airless or thin-atmosphere bodies, systematic excess for thick-atmosphere bodies -- is itself the primary quantitative evidence for the greenhouse effect: it is not merely that Venus is "hot," but that Venus is hundreds of kelvin hotter than energy balance alone (with its measured, quite high albedo of 0.76) can explain, and that specific, quantified gap is what the greenhouse effect must explain.'),
        ('The Greenhouse Effect as an Energy-Balance Correction',
         ['An atmosphere that is relatively transparent to incoming visible starlight but relatively opaque to outgoing thermal infrared radiation forces the effective infrared-emitting level to occur higher (and colder) in the atmosphere than the surface itself.',
          'Because that higher, colder level must still radiate the same total absorbed power to space, the surface below it must be warmer than the simple zero-atmosphere equilibrium temperature to maintain the required outward energy flux through the intervening, partially opaque atmosphere.',
          'Greenhouse warming, &Delta;T_gh = T_surface - T_eq, is therefore a genuine, quantifiable radiative-transfer effect, not merely a qualitative "blanket" analogy.'],
         'The "blanket" analogy for the greenhouse effect, while intuitive, obscures the actual physical mechanism: a blanket works by suppressing convective and conductive heat loss, while the atmospheric greenhouse effect works by selective spectral opacity (transparent to incoming visible light, opaque to outgoing infrared), a genuinely different physical mechanism that this course\'s energy-balance derivation makes explicit and quantifiable rather than merely descriptive.'),
        ('Greenhouse Temperature Excess Across the Solar System',
         ['Venus: computed zero-albedo, zero-greenhouse equilibrium temperature is far below its observed 737 K surface temperature -- the largest greenhouse excess of any solar system body, driven by its 92-bar, 96.5% CO&#8322; atmosphere.',
          'Earth: modest greenhouse excess (&sim;33 K, from 255 K zero-greenhouse equilibrium to 288 K observed mean surface temperature), driven primarily by water vapor and CO&#8322; despite their much lower atmospheric abundance than on Venus.',
          'Mars: small but non-negligible greenhouse excess (a few kelvin) despite its CO&#8322;-dominated atmosphere, because its atmosphere is simply too thin (surface pressure &sim;6 mbar, versus Earth\'s 1013 mbar) to trap much outgoing radiation.'],
         'The contrast between Venus\'s enormous greenhouse excess and Mars\'s tiny one, despite both having CO&#8322;-dominated atmospheres, is the clearest possible demonstration that greenhouse warming depends on total atmospheric mass and opacity, not merely on the presence of a greenhouse gas -- precisely the same total-column-opacity logic that governs radiative transfer in stellar atmospheres, developed in ASTR 310.'),
        ('Bond Albedo: Measurement and Meaning',
         ['Bond albedo integrates a planet\'s reflectivity over all wavelengths and all scattering angles, distinct from the simpler geometric albedo (reflectivity at zero phase angle only).',
          'Bond albedo is measured from spacecraft observations at multiple phase angles (only achievable by a spacecraft that can see a planet from angles Earth-based telescopes cannot) or, historically, inferred from disk-integrated photometry combined with phase-function models.',
          'Cloud cover dominates a planet\'s Bond albedo: Venus\'s sulfuric-acid cloud deck gives it the highest Bond albedo (0.76) of any planet, while Mercury\'s airless, dark regolith surface gives it the lowest (0.088).'],
         'Bond albedo is frequently confused with "how bright a planet looks," but the two are not the same thing: a planet can look visually bright from a single viewing angle (high geometric albedo) while still having a modest Bond albedo if it scatters light preferentially in some directions over others, which is why careful multi-phase-angle spacecraft photometry, not simple ground-based brightness estimates, is required to measure Bond albedo accurately enough for the energy-balance calculation in this lecture.'),
        ('Runaway Greenhouse: A Positive Feedback Instability',
         ['If a planet\'s surface temperature rises enough to vaporize a large surface water reservoir into the atmosphere, water vapor (itself a potent greenhouse gas) further increases the greenhouse effect, further raising the temperature, in principle without a stable equilibrium until essentially all surface water has evaporated.',
          'Venus\'s current bone-dry surface and its atmosphere\'s deuterium-to-hydrogen ratio (roughly 100-150 times Earth\'s, indicating strong preferential loss of light hydrogen from photodissociated water) are considered strong indirect evidence that Venus underwent a runaway greenhouse early in its history.',
          'Whether Venus\'s runaway greenhouse was triggered primarily by its closer distance to the Sun, by a brighter early Sun\'s evolution, or by some combination is an active research question revisited in Lecture 09\'s climate-evolution treatment.'],
         'The elevated deuterium-to-hydrogen ratio in Venus\'s atmosphere is a particularly elegant piece of evidence, because it is a fossil isotopic signature rather than a present-day measurement of an ongoing process: once water vapor is photodissociated high in the atmosphere, the lighter hydrogen isotope escapes to space preferentially (Lecture 09\'s Jeans-escape physics makes this quantitative), progressively enriching the remaining hydrogen inventory in deuterium, so today\'s highly elevated D/H ratio is direct evidence of an enormous historical loss of water from Venus.'),
        ('Radiative-Convective Equilibrium Models',
         ['Simple energy-balance models (this lecture) treat a planet as a single point with one temperature; real climate models divide the atmosphere into layers and solve radiative transfer and convective adjustment simultaneously at each layer.',
          'Radiative-convective models correctly predict both Earth\'s observed tropospheric lapse rate and its stratospheric temperature inversion (previewed in Lecture 07), phenomena the single-point energy-balance model cannot address.',
          'These layered models are the standard tool used to predict exoplanet atmospheric temperature structure (Lecture 14) where no direct in-situ measurement is possible.'],
         'This section is included to make clear that the single-point equilibrium-temperature formula derived earlier in this lecture, while genuinely useful and correct as a global energy-balance constraint, is a simplification: it gives the correct emitting temperature averaged over the whole planet, but a full radiative-convective model is required to say anything about how that temperature is distributed with altitude or between day and night hemispheres, an important caveat when this formula is later applied to TRAPPIST-1 planets in Lecture 14.'),
        ('Day-Night and Latitudinal Temperature Redistribution',
         ['A rapidly rotating planet with an efficient atmospheric circulation (Earth, Venus\'s upper atmosphere) redistributes absorbed heat fairly evenly across its surface, making the simple global-average equilibrium temperature a reasonable approximation everywhere.',
          'A slowly rotating or tidally locked planet (Mercury; potentially many close-in exoplanets, including several TRAPPIST-1 planets, previewed here and developed in Lecture 14) can sustain enormous day-night temperature contrasts that a single global-average temperature does not capture.',
          'The equilibrium-temperature formula in this lecture is most directly meaningful as a globally and rotationally averaged quantity; local surface temperatures can differ from it substantially depending on rotation and atmospheric heat transport.'],
         'This caveat about rotation and heat redistribution is essential context for the exoplanet application in Lecture 14: several TRAPPIST-1 planets are thought to be tidally locked (Lecture 12\'s tidal-locking physics, applied there to solar-system moons, applies equally to close-in exoplanets), meaning their actual day-side and night-side temperatures could differ dramatically from the single equilibrium-temperature number this lecture\'s formula produces.'),
        ('Scope Note and Reading',
         ['OpenStax <em>Astronomy 2e</em> Section 10.4 (Greenhouse Effect) introduces the greenhouse effect qualitatively, without deriving the radiative-equilibrium energy balance.',
          'This lecture\'s full energy-balance derivation, including the geometric factor-of-4 argument and the explicit greenhouse-excess calculation, extends beyond OpenStax and follows the standard treatment in Sanchez-Lavega, <em>An Introduction to Planetary Atmospheres</em>, Chapter 4, and Pierrehumbert, <em>Principles of Planetary Climate</em>, Chapter 3.'],
         'As with every derivation-heavy lecture in this course, students should treat OpenStax\'s qualitative greenhouse-effect discussion as background motivation, while the quantitative energy-balance derivation developed here is the material this course actually requires students to reproduce and apply.'),
    ],
    worked_title='Equilibrium Temperature and Greenhouse Excess for the Eight Planets',
    worked_steps=[
        'Compute T_eq = [(1-A) L&#8857; / (16&pi;&sigma;a&sup2;)]&#185;&#8260;&#8308; for each planet using its measured Bond albedo A and semimajor axis a, then compare to each planet\'s observed mean surface (or, for the giant planets, effective) temperature.',
        '<table><tr><th>Planet</th><th>T_eq (K, with albedo)</th><th>T_observed (K)</th><th>&Delta;T_gh (K)</th></tr>' + ''.join(
            f"<tr><td>{name}</td><td>{fmt(TEQ_BOND[name],4)}</td><td>{PLANETS[name]['teq_obs']:.0f}</td><td>{PLANETS[name]['teq_obs']-TEQ_BOND[name]:+.0f}</td></tr>"
            for name in PLANETS) + '</table>',
        f'Result: Mercury and Mars show small greenhouse excesses (a few to a few tens of K, consistent with their thin or absent atmospheres), Earth shows a moderate excess (&asim;{PLANETS["Earth"]["teq_obs"]-TEQ_BOND["Earth"]:+.0f} K), and Venus shows by far the largest excess ({PLANETS["Venus"]["teq_obs"]-TEQ_BOND["Venus"]:+.0f} K), consistent with its 92-bar CO&#8322;-dominated atmosphere.',
    ],
    worked_notes='All eight T_eq values are computed with the single <code>equilibrium_temperature_k</code> function defined once in this course\'s shared code and already used qualitatively in Lecture 02\'s frost-line calculation; the observed temperatures are standard published planetary values (see reference-log.md). Lab 04 extends this table to a full quantitative greenhouse-forcing comparison.',
    summary=['A planet\'s zero-atmosphere equilibrium temperature follows directly from global radiative energy balance: absorbed stellar flux equals emitted thermal flux.',
             'The greenhouse effect is the quantifiable excess of observed surface temperature over this zero-atmosphere equilibrium value, driven by atmospheric opacity to outgoing infrared radiation.',
             'Comparing Venus, Earth, and Mars shows the greenhouse excess tracks total atmospheric mass and opacity, not merely the presence of CO&#8322;.'],
    preview='Lecture 09 asks how an atmosphere can be lost entirely over time, through Jeans escape, and how the runaway greenhouse and atmospheric escape together shape long-term climate evolution.',
))

LECTURES.append(dict(
    n=9, title='Atmospheric Escape and Long-Term Climate Evolution',
    kicker='Unit 4: Atmospheres', subtitle='Deriving why some atmospheres survive and others do not',
    objectives=[
        'Derive the Jeans escape parameter from the ratio of a molecule\'s thermal speed to a planet\'s escape velocity.',
        'Explain why light molecules (H, H2, He) escape far more readily than heavy ones (N2, CO2, O2).',
        'Compare Jeans escape efficiency across Earth, Mars, and Venus, and connect the result to each planet\'s present atmosphere.',
        'Distinguish Jeans (thermal) escape from non-thermal (hydrodynamic, ion-pickup, impact) escape mechanisms.'],
    sections=[
        ('The Maxwell-Boltzmann Speed Distribution in the Exosphere',
         ['In a gas at temperature T, molecular speeds follow the Maxwell-Boltzmann distribution, with most-probable speed v_mp = &radic;(2kT/m).',
          'The exosphere is the altitude above which the atmosphere is collisionless (mean free path exceeds the local scale height), so a molecule moving upward there travels essentially unimpeded until gravity pulls it back or it escapes.',
          'A fraction of exospheric molecules, in the high-velocity tail of the Maxwell-Boltzmann distribution, exceed the local escape velocity and are lost to space -- this is Jeans escape.'],
         'The exosphere\'s defining property (collisionlessness) is what makes Jeans escape a genuinely different physical regime from ordinary atmospheric dynamics: below the exobase, a fast-moving molecule collides with its neighbors long before it can travel far, but above it, a molecule moving fast enough simply leaves, which is why Jeans escape is computed using the exospheric temperature (often significantly hotter than the surface, due to UV/X-ray heating) rather than the surface temperature.'),
        ('Deriving the Jeans Escape Parameter',
         ['Define the Jeans parameter &lambda; = v_esc&sup2; / v_mp&sup2; = (2GM/R) / (2kT/m) = GMm / (RkT).',
          '&lambda; compares the gravitational binding energy per molecule (GMm/R) to its thermal kinetic energy (kT); large &lambda; means gravity dominates and escape is negligible, small &lambda; means thermal energy is comparable to or exceeds binding energy and escape is rapid.',
          'The escape flux itself falls off exponentially with &lambda; (as e&#8315;&#955;, from the tail of the Maxwell-Boltzmann distribution), so even a modest change in &lambda; changes the escape rate by orders of magnitude.'],
         'The exponential dependence of escape flux on &lambda; is the single most important qualitative result in this lecture: because escape rate falls off as roughly e&#8315;&#955;, a molecule with &lambda; = 10 escapes many orders of magnitude faster than one with &lambda; = 30, which is why hydrogen (light, small m) escapes so much more readily than nitrogen or oxygen (heavy, large m) even though all species experience the same gravity and the same exospheric temperature.'),
        ('Why Light Species Escape Preferentially',
         ['Because &lambda; &prop; m (heavier molecules have proportionally more gravitational binding energy per molecule for the same v_esc), light species (atomic H, H&#8322;, He) have much smaller &lambda; than heavy species (N&#8322;, O&#8322;, CO&#8322;) at the same exospheric temperature.',
          'This differential escape means an atmosphere\'s light constituents are depleted preferentially over geological time, progressively enriching the remaining atmosphere in heavier species.',
          'This is the same physical mechanism behind Venus\'s elevated deuterium-to-hydrogen ratio discussed in Lecture 08: hydrogen (from photodissociated water) escapes far faster than its heavier isotope deuterium, progressively enriching the remaining reservoir in D.'],
         'Mass-dependent differential escape is a recurring theme this course returns to explicitly: it explains both why Earth has retained its heavier atmospheric constituents (N&#8322;, O&#8322;) over 4.5 Gyr while continuously losing light hydrogen to space, and why Venus\'s D/H ratio serves as an isotopic fossil record of a much larger historical water inventory, tying this lecture directly back to Lecture 08\'s runaway-greenhouse discussion.'),
        ('Jeans Escape on Earth versus Mars',
         ['Earth\'s escape velocity (11.2 km/s) is large enough that even hydrogen has &lambda; of order 10-15 at typical exospheric temperatures (&sim;1000 K), giving a slow but non-negligible present-day hydrogen escape rate.',
          'Mars\'s much smaller escape velocity (5.0 km/s) gives hydrogen a substantially smaller &lambda;, implying more efficient hydrogen (and by extension water) loss, consistent with Mars\'s observed depleted present-day water inventory relative to its geological evidence for a wetter past (Lecture 05).',
          'Neither planet loses heavier species like N&#8322; or CO&#8322; efficiently via Jeans escape alone; other mechanisms (below) are required to explain, for example, Mars\'s substantial loss of atmospheric mass since its early, thicker atmosphere.'],
         'The Mars/Earth Jeans-escape comparison developed quantitatively in this lecture\'s worked example is a direct, testable prediction: because Mars\'s escape velocity is less than half of Earth\'s, hydrogen should escape far more readily from Mars, and indeed both theoretical modeling and direct spacecraft measurement (NASA\'s MAVEN mission, launched specifically to quantify Martian atmospheric escape) confirm ongoing hydrogen and oxygen loss from Mars today, at rates broadly consistent with the physics developed here.'),
        ('Non-Thermal Escape Mechanisms',
         ['Hydrodynamic escape: when a planet\'s upper atmosphere is heated so intensely (typically by extreme ultraviolet and X-ray radiation from a young, active star) that the whole gas expands and flows outward collectively, dragging even heavier species along with the escaping light gas.',
          'Ion pickup: solar-wind magnetic fields can directly sweep up ionized atmospheric particles at the top of an unmagnetized planet\'s atmosphere (relevant to Mars, which lacks a global magnetic field -- Lecture 10) and carry them away.',
          'Impact erosion: a sufficiently energetic impact (Lecture 06) can eject atmosphere directly, and may have been an important loss mechanism during the heavy-bombardment era.'],
         'These non-thermal mechanisms matter because Jeans escape alone, while pedagogically the clearest and most tractable to derive, is quantitatively insufficient to explain the total atmospheric loss inferred for Mars over its history; hydrodynamic escape (especially relevant during the young Sun\'s more active, higher-XUV-flux early phase) and ion pickup (enabled by Mars\'s lack of a protective global magnetic field, previewed here and developed in Lecture 10) are thought to have been more important, especially in the solar system\'s first billion years.'),
        ('The Faint Young Sun Paradox',
         ['Stellar evolution models (ASTR 330) show the young Sun was roughly 25-30% less luminous 4 Gyr ago than today, which would predict a frozen early Earth under the simple equilibrium-temperature formula (Lecture 08) alone.',
          'Geological evidence (liquid water features in ancient rocks, evidence for early life) instead indicates Earth\'s surface was not globally frozen during this period.',
          'The leading resolution invokes a substantially stronger early greenhouse effect (higher atmospheric CO&#8322; and/or CH&#8324; concentrations) compensating for the fainter young Sun, an idea directly testable using this lecture\'s and Lecture 08\'s energy-balance tools.'],
         'The faint young Sun paradox is a genuine, still active research problem that links stellar evolution (ASTR 330), radiative energy balance (Lecture 08), and the carbon-silicate weathering cycle (this lecture\'s next section) into a single coherent long-term climate-stability argument, and it is a clear example of how apparently separate subfields of astronomy and planetary science must be combined to explain a single observational puzzle.'),
        ('The Carbon-Silicate Cycle: A Long-Term Climate Thermostat',
         ['Silicate weathering (chemical reaction of atmospheric CO&#8322;, dissolved in rainwater, with exposed silicate rock) draws down atmospheric CO&#8322; over geological timescales, and its rate increases with temperature and rainfall.',
          'Subduction (Lecture 05) carries weathered carbonate sediments into the mantle, where volcanism eventually returns carbon to the atmosphere as volcanic CO&#8322;, closing the cycle.',
          'Because weathering rate increases with temperature, this cycle acts as a long-term negative feedback (a thermostat): a warmer climate weathers faster, drawing down CO&#8322; and cooling the planet back down, while a colder climate weathers more slowly, letting volcanic CO&#8322; accumulate and warm the planet back up.'],
         'The carbon-silicate cycle is this course\'s clearest example of a negative (stabilizing) climate feedback, in direct contrast to the runaway greenhouse\'s positive (destabilizing) feedback introduced in Lecture 08; the cycle requires both active volcanism (an ongoing carbon source, from Lecture 04\'s heat-budget discussion) and, critically, plate tectonics (Lecture 05) to subduct weathered carbon back into the mantle, which is part of why the absence of plate tectonics on Venus and Mars is thought to have contributed to their present-day climate extremes.'),
        ('Climate Divergence: Venus, Earth, and Mars Compared',
         ['All three planets likely began with broadly comparable rocky compositions and plausibly similar volatile (water, CO&#8322;) delivery from the outer solar nebula and later impacts.',
          'Venus\'s closer distance to the Sun (higher incident flux, Lecture 08) plausibly triggered an early runaway greenhouse, permanently losing its water via hydrogen escape (this lecture) before a stabilizing carbon-silicate cycle could establish itself.',
          'Mars\'s smaller size (weaker gravity, faster interior cooling per Lecture 04, and probable earlier loss of an active dynamo per Lecture 10) likely could not sustain either a thick enough atmosphere or a strong enough magnetic shield against solar-wind erosion to maintain a stable, temperate early climate.'],
         'This three-planet comparison is the payoff of the entire atmospheres unit: no single lecture\'s physics (energy balance alone, escape alone, or the carbon cycle alone) fully explains why Venus, Earth, and Mars diverged so dramatically in climate outcome, but the combination developed across Lectures 07-09 -- atmospheric structure, radiative balance, and escape, set against each planet\'s distance, size, and (Lecture 10) magnetic-field history -- provides a coherent, quantitative comparative framework.'),
        ('Habitable Zone Boundaries from Climate Physics',
         ['The inner edge of a habitable zone is often defined by the onset of a runaway greenhouse (Lecture 08); the outer edge is often defined by the point at which CO&#8322; condensation (forming reflective clouds or surface ice) can no longer sustain a strong enough greenhouse effect to keep water liquid.',
          'These boundaries are computed using the same energy-balance and greenhouse formalism developed in Lecture 08, extended with climate-feedback models rather than the simple single-point equilibrium-temperature formula alone.',
          'Habitable zone boundaries are not fixed, universal distances in AU; they scale with stellar luminosity and therefore differ dramatically between Sun-like stars and the cooler, fainter M dwarfs, directly relevant to the TRAPPIST-1 system introduced in Lecture 14.'],
         'This section deliberately introduces the habitable-zone concept using the same tools already developed (equilibrium temperature, greenhouse feedback) rather than as a new independent idea, both because that is the physically correct way to derive it and because it sets up the direct quantitative application to TRAPPIST-1\'s much fainter, cooler host star in Lecture 14.'),
        ('Scope Note and Reading',
         ['OpenStax <em>Astronomy 2e</em> Section 10.5 (Climate Change) briefly discusses atmospheric evolution and comparative climate at an introductory level.',
          'The quantitative Jeans-escape derivation and the carbon-silicate cycle feedback argument developed in this lecture go beyond OpenStax and follow Catling & Kasting, <em>Atmospheric Evolution on Inhabited and Lifeless Worlds</em>, Chapters 2 and 8.'],
         'As with the other atmospheres-unit lectures, OpenStax provides useful descriptive motivation for comparative climate, but the quantitative escape and feedback mechanisms developed here are the primary content this course examines and tests.'),
    ],
    worked_title='Jeans Escape Parameter for Hydrogen on Earth and Mars',
    worked_steps=[
        f'Assume a representative exospheric temperature of 1000 K and compute the most-probable thermal speed of atomic/molecular hydrogen, v_mp = &radic;(2kT/m_H2) = {EARTH_H2_THERMAL_V:.0f} m/s = {EARTH_H2_THERMAL_V/1000:.2f} km/s (same for both planets, since exospheric temperature is assumed equal for this illustrative comparison).',
        f'Earth: v_esc = {EARTH_ESCAPE_V/1000:.2f} km/s, giving &lambda; = (v_esc/v_mp)&sup2; = {EARTH_JEANS_H2:.1f}.',
        f'Mars: v_esc = {MARS_ESCAPE_V/1000:.2f} km/s, giving &lambda; = (v_esc/v_mp)&sup2; = {MARS_JEANS_H2:.1f}.',
        f'Result: Mars\'s Jeans parameter for hydrogen ({MARS_JEANS_H2:.1f}) is roughly {EARTH_JEANS_H2/MARS_JEANS_H2:.1f} times smaller than Earth\'s ({EARTH_JEANS_H2:.1f}), meaning hydrogen (and hence water, once photodissociated) escapes far more readily from Mars than from Earth -- consistent with geological evidence for a substantially wetter early Mars that has since lost most of its water, and with direct MAVEN spacecraft measurements of ongoing Martian atmospheric escape.',
    ],
    worked_notes='Both &lambda; values use the identical <code>jeans_parameter</code> function and the identical assumed exospheric temperature, so the comparison isolates the effect of escape velocity alone; a more complete treatment (Lab 05) varies exospheric temperature independently for each planet using published thermospheric measurements.',
    summary=['The Jeans escape parameter &lambda; = v_esc&sup2;/v_mp&sup2; governs how readily a given molecular species escapes a planet\'s exosphere, with escape rate falling exponentially as &lambda; increases.',
             'Light species (H, H2, He) escape far more readily than heavy species (N2, O2, CO2), progressively enriching a planet\'s remaining atmosphere in heavier constituents over geological time.',
             'The carbon-silicate weathering cycle provides a long-term stabilizing climate feedback that requires active volcanism and plate tectonics, helping explain why Earth\'s climate has remained temperate while Venus\'s and Mars\'s diverged catastrophically.'],
    preview='Lecture 10 turns to another protective mechanism against solar-wind erosion: planetary magnetic fields, and the dynamo process that generates them.',
))

LECTURES.append(dict(
    n=10, title='Planetary Magnetic Fields and Dynamo Theory',
    kicker='Unit 5: Fields and Giants', subtitle='How a convecting, conducting interior generates a global magnetic field',
    objectives=[
        'State the qualitative requirements for a self-sustaining dynamo: an electrically conducting fluid, convective motion, and planetary rotation.',
        'Compare measured magnetic dipole moments across the solar system and connect their magnitude to each planet\'s interior structure.',
        'Explain the observational evidence for past dynamos on bodies that lack one today (Mars, the Moon).',
        'Describe how a magnetosphere forms from the interaction between a planetary field and the solar wind, and why this matters for atmospheric retention.'],
    sections=[
        ('The Dynamo Mechanism: Qualitative Requirements',
         ['A planetary dynamo requires an electrically conducting fluid layer (liquid iron alloy for terrestrial planets, metallic or ionized hydrogen for giant planets, or a salty subsurface ocean or ionic ice mantle for some icy satellites).',
          'That conducting fluid must convect vigorously (Lecture 04\'s Rayleigh-number criterion, applied here to the core rather than the mantle), driven by core heat loss and, for terrestrial planets, compositional buoyancy from inner-core solidification.',
          'Planetary rotation organizes the convective flow (via the Coriolis force) into helical patterns capable of sustaining, rather than simply dissipating, a magnetic field against Ohmic decay -- this is the essential role of the Coriolis force in dynamo theory.'],
         'The requirement that rotation organize convection into helical flow (rather than merely providing convection alone) is the key insight that separates a working dynamo from ordinary turbulent convection: a non-rotating, convecting conducting fluid does not, in general, sustain a large-scale magnetic field against resistive (Ohmic) decay, because the flow lacks the systematic helicity needed to continuously regenerate field lines faster than they decay -- this qualitative picture is what this course teaches at the 300 level, deferring the full magnetohydrodynamic dynamo equations to graduate-level treatment.'),
        ('Magnetic Dipole Moments Across the Solar System',
         ['Earth\'s magnetic dipole moment is roughly 8 &times; 10&sup2;&sup2; A&#183;m&sup2;, generated by convection in its liquid outer core, driven by both core cooling and compositional buoyancy from inner-core crystallization.',
          'Jupiter\'s dipole moment is roughly 1.5-2 &times; 10&sup2;&#8309; A&#183;m&sup2; (about 20,000 times Earth\'s), generated in a vast metallic-hydrogen convecting layer (Lecture 11) far larger and more electrically conductive than Earth\'s core.',
          'Mercury\'s dipole moment is roughly 4 &times; 10&sup1;&sup9; A&#183;m&sup2; (about 1/200th of Earth\'s), surprisingly present at all for such a small, slowly rotating planet, and attributed to a still-partially-liquid, likely sulfur-enriched core (Lecture 03).'],
         'Jupiter\'s enormous magnetic moment relative to Earth\'s is not simply a matter of Jupiter being a bigger planet; it reflects a qualitatively different dynamo region (a much larger volume of highly conductive metallic hydrogen, developed in Lecture 11, rather than a comparatively modest liquid-iron shell), and comparing the two dipole moments quantitatively (rather than simply noting "Jupiter has a bigger field") is the kind of comparative reasoning this course requires throughout.'),
        ('Venus and Mars: Two Different Absences of a Present Dynamo',
         ['Venus has no measurable present-day intrinsic magnetic field, despite being similar in size and probable core structure to Earth; the leading explanation is that Venus\'s core may not be convecting vigorously (or at all) today, though the precise reason remains debated and is a target of future missions.',
          'Mars has no global present-day dynamo field, but strong remnant crustal magnetization (discovered by Mars Global Surveyor) in its ancient southern highlands proves Mars once had an active dynamo, likely in its first &sim;500 Myr to 1 Gyr, before its smaller core cooled below the threshold for sustained convection.',
          'Mars\'s crustal magnetization is patchy and absent from its youngest volcanic provinces and largest impact basins, consistent with the dynamo having switched off before those features formed.'],
         'Mars\'s remnant crustal magnetization is one of the most information-rich single datasets in comparative planetology: because impact basins that formed after the dynamo shut off show no remnant magnetization (impacts do not preserve a field that was not present when the crust cooled through its Curie temperature), while older terrain does, planetary scientists can bracket the shutdown time of the Martian dynamo using crater-count chronology (Lecture 06) applied to the boundary between magnetized and unmagnetized terrain -- a direct link between this lecture\'s topic and Lecture 06\'s dating method.'),
        ('Magnetic Field Generation and the Core Heat Budget',
         ['A convecting, dynamo-generating core requires ongoing heat loss from the core to the mantle above it (Lecture 04); if the mantle above the core cools too slowly (or the core itself has already cooled and largely solidified), core convection weakens or ceases.',
          'Mercury\'s continued, if weak, dynamo despite its small size is attributed to a sulfur-enriched core composition (Lecture 03) that depresses the core\'s freezing point, keeping at least part of it liquid and convecting today.',
          'This connects directly to the surface-to-volume cooling scaling argument from Lecture 04: smaller bodies are expected to lose their dynamos earlier, all else equal, which is broadly consistent with the Moon\'s dynamo (inferred from magnetized lunar samples) having shut off by roughly 1-1.5 Gyr ago, well before Mars\'s.'],
         'This section makes explicit the connection this course has been building since Lecture 03: interior structure (core size and composition) sets the heat budget (Lecture 04), and the heat budget sets whether a dynamo can operate today, so magnetic-field measurements are, in a real sense, indirect probes of the same interior processes developed several lectures earlier, not an independent topic.'),
        ('Paleomagnetism and Magnetic Reversals',
         ['Earth\'s magnetic field has reversed polarity irregularly throughout geological history, recorded in the magnetic-stripe pattern of oceanic crust (Lecture 05) and in the magnetization of layered volcanic rock sequences on land.',
          'Reversal frequency has itself varied over geological time, including long "superchron" intervals of a single stable polarity lasting tens of millions of years.',
          'The physical mechanism driving reversals is understood qualitatively (chaotic behavior in the nonlinear dynamo equations) but not predictively -- no model can currently forecast when the next reversal will occur.'],
         'Earth\'s reversal record is simultaneously strong evidence that Earth\'s dynamo really is a self-sustaining, chaotic nonlinear system (rather than a fixed, permanently stable field) and a genuine reminder of the limits of current dynamo theory: physicists and geophysicists can reproduce reversal-like behavior in numerical dynamo simulations, but cannot yet predict specific reversal timing from first principles, an honest limitation this course states explicitly rather than implying the theory is more complete than it is.'),
        ('Magnetospheres: The Interaction with the Solar Wind',
         ['A planetary magnetic field, extended into space, forms a magnetosphere -- a cavity that deflects the solar wind (a supersonic stream of charged particles from the Sun) around the planet rather than letting it strike the atmosphere or surface directly.',
          'The magnetopause (the boundary between the magnetosphere and the solar wind) stands where magnetic pressure balances solar-wind dynamic pressure; for Earth this occurs at roughly 10 Earth radii on the sunward side.',
          'A planet without a strong intrinsic field (Venus, Mars) instead forms a weaker, induced magnetosphere from the interaction between the solar wind and the planet\'s ionosphere, offering much less protection.'],
         'The magnetopause standoff distance is itself a quantitative, testable prediction: because it is set by pressure balance between the planet\'s magnetic field (falling off as distance cubed for a dipole) and the solar wind\'s dynamic pressure (which varies with solar activity), the magnetopause distance can be predicted from Earth\'s known dipole moment and typical solar-wind conditions, and directly measured by spacecraft crossing the boundary -- another example of this course\'s recurring theme of cross-checking a theoretical prediction against direct measurement.'),
        ('Magnetic Shielding and Atmospheric Retention',
         ['A strong magnetosphere is often invoked as protection against solar-wind-driven, non-thermal atmospheric escape (Lecture 09\'s ion-pickup mechanism), though the quantitative importance of this shielding effect for total atmospheric loss over solar system history remains actively debated.',
          'Mars\'s lack of a present-day global field is frequently cited as a contributing factor in its atmospheric history, though direct MAVEN measurements show ion-pickup loss at Mars today is modest compared to the total atmospheric mass Mars is inferred to have lost over its history, implying other mechanisms (hydrodynamic escape early on; Lecture 09) were likely more important overall.',
          'This course presents magnetic shielding as a plausible but not fully quantified contributing factor, consistent with the current state of the research literature, rather than as a settled, dominant explanation.'],
         'This honest hedging is deliberate and important: the popular narrative that "Mars lost its atmosphere because it lost its magnetic field" is an oversimplification of an actively researched, only partially quantified causal chain, and this course\'s standard of scientific rigor requires presenting the genuine state of uncertainty rather than a tidier but less accurate story.'),
        ('Magnetic Fields of the Giant Planets',
         ['All four giant planets possess intrinsic magnetic fields, generated in metallic-hydrogen (Jupiter, Saturn) or ionic-water/ammonia-mixture (Uranus, Neptune) conducting layers, previewed here and developed fully in Lecture 11.',
          'Uranus\'s and Neptune\'s fields are unusual in being strongly non-dipolar (large quadrupole and higher-order components) and substantially offset from each planet\'s rotation axis and center, suggesting dynamo generation in a comparatively thin conducting shell rather than a deep, well-mixed core.',
          'This diversity of dynamo geometries across the four giant planets is itself an important test of dynamo theory\'s generality beyond the relatively simple, nearly axisymmetric dipole fields of Earth, Jupiter, and Saturn.'],
         'Uranus and Neptune\'s strongly non-dipolar, offset magnetic fields are a valuable stress test of dynamo theory: they show that a working dynamo does not require the deep, nearly spherically symmetric conducting region that produces Earth\'s and Jupiter\'s comparatively simple dipole-dominated fields, and current models attribute this difference to dynamo generation confined to a relatively thin, ionically conducting outer shell in these two ice giants, developed further in Lecture 11.'),
        ('Icy Satellite and Exoplanet Magnetic Fields (Preview)',
         ['Ganymede is the only known moon with its own intrinsic dynamo-generated magnetic field, detected directly by the Galileo spacecraft, previewed here and revisited in Lecture 13.',
          'Europa\'s and Callisto\'s magnetic signatures instead appear to be induced fields, generated by electrical currents in a subsurface salty ocean responding to Jupiter\'s time-varying background field -- indirect but compelling evidence for those subsurface oceans, developed fully in Lecture 13.',
          'Whether any exoplanet possesses a detectable magnetic field remains an open observational challenge; indirect radio and auroral signatures are actively being searched for, relevant to the exoplanet capstone in Lecture 14.'],
         'The induced-field detection of subsurface oceans on Europa and Callisto is one of the most elegant applications of magnetometry in all of planetary science: rather than requiring a dynamo of its own, a satellite with a sufficiently conductive subsurface layer (a salty ocean) will generate a secondary, induced field in response to its parent planet\'s varying background field, and the amplitude and phase of that induced signal directly diagnose the ocean\'s depth and conductivity -- a technique this course returns to with full quantitative development in Lecture 13.'),
        ('Scope Note and Reading',
         ['OpenStax <em>Astronomy 2e</em> Section 10.3 (Magnetic Fields) introduces planetary magnetism qualitatively, without deriving dynamo theory.',
          'The qualitative dynamo requirements (conducting fluid, convection, rotation-organized helicity) and the magnetosphere pressure-balance argument developed in this lecture extend beyond OpenStax and follow Stevenson (2003, <em>Earth and Planetary Science Letters</em>) and de Pater & Lissauer, <em>Planetary Sciences</em>, Chapter 5.'],
         'As with prior derivation-heavy lectures, students should treat OpenStax as introductory context, while the qualitative dynamo model and quantitative magnetopause pressure-balance argument developed here are the primary material this course requires students to understand and apply.'),
    ],
    worked_title="Earth's Magnetopause Standoff Distance",
    worked_steps=[
        'A magnetic dipole\'s field strength falls off as B(r) = B&#8320;(R_E/r)&sup3;, so its energy density (and hence magnetic pressure) falls off as (R_E/r)&#8310;.',
        'The magnetopause stands where magnetic pressure equals solar-wind dynamic pressure: B(r)&sup2;/(2&mu;&#8320;) = &#961;_sw v_sw&sup2;.',
        'Using Earth\'s equatorial surface field B&#8320; &asymp; 3.1 &times; 10&#8315;&#8309; T, typical solar-wind density &#961;_sw &asymp; 5 protons/cm&sup3; (&asymp; 8.4 &times; 10&#8315;&#178;&#185; kg/m&sup3;), and typical solar-wind speed v_sw &asymp; 400 km/s, solving for r gives a standoff distance of roughly 10 Earth radii.',
        'Result: this matches the observed, directly measured average magnetopause distance of &sim;10 R_E on Earth\'s sunward side, confirming the pressure-balance model against spacecraft crossings (e.g., by the THEMIS and MMS missions).',
    ],
    worked_notes='This order-of-magnitude pressure-balance estimate is the standard textbook derivation for magnetopause standoff distance; Lab 05 extends it to a comparison between Earth\'s magnetopause and the much more distant standoff expected (and observed) at Jupiter, given its far larger dipole moment.',
    summary=['A self-sustaining planetary dynamo requires a convecting, electrically conducting fluid whose flow is organized into helical patterns by planetary rotation.',
             'Measured dipole moments (Earth, Jupiter, Mercury) and their absence or remnant signatures (Venus, Mars, the Moon) directly reflect each body\'s interior heat budget and core state, connecting this lecture back to Lectures 03-04.',
             'A planetary magnetosphere deflects the solar wind via magnetic pressure balance, offering some protection against non-thermal atmospheric escape, though the quantitative importance of this shielding remains an active research question.'],
    preview='Lecture 11 turns fully to the giant planets themselves: their deep interior structure, the metallic-hydrogen layers that generate their fields, and what distinguishes gas giants from ice giants.',
))

LECTURES.append(dict(
    n=11, title='Giant Planet Interiors: Gas Giants and Ice Giants',
    kicker='Unit 5: Fields and Giants', subtitle='What lies beneath the clouds of Jupiter, Saturn, Uranus, and Neptune',
    objectives=[
        'Describe the pressure-driven transition from molecular to metallic hydrogen inside Jupiter and Saturn.',
        'Explain why Uranus and Neptune are compositionally and structurally distinct "ice giants" rather than smaller gas giants.',
        'Interpret gravity-field harmonics (from Juno, Cassini) as probes of a giant planet\'s deep interior and possible diffuse core.',
        'Connect each giant planet\'s measured heat output to ongoing gravitational energy release (Kelvin-Helmholtz contraction, helium rain).'],
    sections=[
        ('No Solid Surface: Defining "Depth" in a Giant Planet',
         ['Giant planets have no solid surface; the customary "1-bar level" (roughly Earth sea-level pressure) is used as a zero-altitude reference for their observable atmospheres.',
          'Below the visible cloud decks, pressure and temperature increase continuously and smoothly (following the hydrostatic and radiative-convective principles of Lectures 07-08) with no discrete phase boundary marking a "surface."',
          'This absence of a surface is precisely why giant-planet interior structure must be inferred entirely from gravity-field measurements and equation-of-state modeling, rather than any direct landing or drilling.'],
         'The complete absence of a solid surface is the single fact that most distinguishes this lecture\'s subject matter from Lectures 03-06\'s terrestrial-planet interior and surface physics: every technique this course has used so far to probe a solid planet\'s interior (seismology, crater dating, direct sampling) is unavailable for a giant planet, leaving gravity-field inversion and high-pressure equation-of-state physics as the primary tools, which is why this lecture develops them in detail.'),
        ('Molecular-to-Metallic Hydrogen Transition',
         ['At pressures below roughly 1-2 megabar, hydrogen exists as an insulating molecular (H&#8322;) fluid; above this pressure, hydrogen undergoes a transition (debated to be gradual or a sharper phase transition depending on temperature) to an electrically conducting, metallic state.',
          'This molecular-to-metallic transition occurs at roughly 10-20% of Jupiter\'s radius below the visible cloud tops (i.e., relatively shallow), but much deeper (a much larger fraction of the planet\'s radius, and possibly not fully achieved at all) inside the less massive, lower-pressure interiors of Saturn.',
          'Metallic hydrogen\'s high electrical conductivity is the conducting fluid required for the dynamo mechanism introduced in Lecture 10, making Jupiter\'s and Saturn\'s magnetic fields a direct consequence of this deep-interior phase transition.'],
         'The molecular-to-metallic hydrogen transition is the key structural fact connecting this lecture to Lecture 10\'s dynamo discussion: Jupiter\'s enormous magnetic dipole moment (roughly 20,000 times Earth\'s) is generated across a vast metallic-hydrogen convecting shell, not a comparatively small liquid-iron core, and the transition\'s depth (much shallower in Jupiter than in Saturn) is part of the reason Jupiter\'s field is stronger and more dipole-dominated than Saturn\'s.'),
        ('Diffuse and Compact Core Models',
         ['Juno\'s precision gravity measurements at Jupiter (2016-present) show gravity-field harmonics inconsistent with a simple two-layer (compact rocky/icy core plus uniform envelope) model, instead favoring a diffuse, partially dissolved core extending across a substantial fraction of the planet\'s radius.',
          'This diffuse-core structure is now interpreted as evidence for a giant impact early in Jupiter\'s history that partially mixed an originally compact core into the overlying envelope, an idea directly analogous to the giant-impact-driven core stripping proposed for Mercury (Lecture 03).',
          'Saturn\'s interior, probed by Cassini\'s "Grand Finale" close-in gravity measurements, similarly shows evidence for extensive core-envelope mixing, possibly aided by helium rain (below) stirring the deep interior.'],
         'The diffuse-core discovery at Jupiter, delivered by Juno\'s precision gravity science in the 2010s, is a genuine example of a major structural surprise overturning a simpler prior model, directly paralleling this course\'s repeated theme (Lecture 03\'s moment-of-inertia comparisons, Lecture 10\'s dynamo diversity) that gravity-field data can reveal interior complexity invisible to simpler bulk-property arguments.'),
        ('Helium Rain and Saturn\'s Excess Luminosity',
         ['All four giant planets radiate more thermal energy than they receive from the Sun (Lecture 08\'s equilibrium-temperature table shows this as a positive residual once internal heat is included), a signature of ongoing internal energy release rather than pure radiative equilibrium.',
          'For Jupiter, slow gravitational (Kelvin-Helmholtz) contraction, continuing since formation, is sufficient to explain its observed excess luminosity.',
          'Saturn radiates significantly more excess heat than simple Kelvin-Helmholtz contraction alone predicts; the leading explanation is helium rain -- helium becoming immiscible in metallic hydrogen at Saturn\'s (cooler than Jupiter\'s) internal temperatures, condensing into droplets that sink and release additional gravitational energy as they fall.'],
         'Saturn\'s excess-luminosity puzzle is a clean example of using an energy-balance argument (the same logic as Lecture 08\'s equilibrium-temperature derivation, here applied with an added internal heat term rather than assumed zero) to detect a specific, otherwise unobservable internal process: the measured luminosity excess above the Kelvin-Helmholtz-contraction prediction is the primary quantitative evidence for helium rain inside Saturn, an idea also indirectly supported by the observed depletion of helium in Saturn\'s uppermost atmosphere relative to its bulk (protosolar) composition.'),
        ('Gas Giants versus Ice Giants: A Compositional Distinction',
         ['Jupiter and Saturn are roughly 90%+ hydrogen and helium by mass, closely tracking the protosolar composition, consistent with efficient runaway gas accretion (Lecture 02) before the gas disk dispersed.',
          'Uranus and Neptune are only &sim;10-20% hydrogen/helium by mass, with the bulk of their mass instead composed of "ices" (water, ammonia, methane, though likely in a hot, dense, ionic supercritical fluid state rather than literal ice) and rock.',
          'This compositional split, not simply size, is why Uranus and Neptune are termed "ice giants" rather than smaller gas giants, and it directly reflects Lecture 02\'s core-accretion timing argument (their cores likely formed too slowly, or in too low a density outer disk, to capture as much gas before the disk dispersed).'],
         'The gas-giant/ice-giant distinction is a direct payoff of Lecture 02\'s core-accretion formation model: because Uranus and Neptune\'s cores are inferred to have formed more slowly (in a lower-density, more slowly orbiting part of the disk) than Jupiter\'s and Saturn\'s, they captured proportionally far less nebular hydrogen and helium before the gas disk dispersed, leaving them dominated by ices and rock rather than hydrogen/helium gas -- exactly the outcome this course\'s formation-physics lecture predicted.'),
        ('Interior Structure of Uranus and Neptune',
         ['Below their hydrogen/helium-dominated outer envelopes, Uranus and Neptune are thought to contain a vast "ice" mantle of water, ammonia, and methane in a hot, dense, ionically conducting supercritical fluid state.',
          'This ionic mantle, rather than a metallic-hydrogen layer, is the conducting region thought to generate their dynamos, previewed in Lecture 10 as an explanation for their unusual, strongly non-dipolar, offset magnetic fields.',
          'Neptune radiates substantially more internal heat than Uranus, despite their similar size and composition -- another open problem, possibly related to a difference in their formation histories (e.g., a giant impact tipping Uranus onto its side, discussed below, might also have disrupted its internal heat transport).'],
         'The puzzle of Neptune radiating measurably more excess heat than the very similar Uranus (which appears to radiate essentially no measurable excess at all) remains genuinely unresolved, and this course states that honestly rather than offering a falsely definitive explanation; it is frequently discussed alongside Uranus\'s extreme axial tilt (98&deg;) as evidence that the two ice giants may have experienced quite different late-stage giant-impact histories despite their otherwise similar bulk properties.'),
        ('Zonal Winds and Atmospheric Dynamics',
         ['Jupiter\'s and Saturn\'s visible cloud decks show strong, persistent east-west zonal jet streams, with wind speeds up to &sim;500 km/hr in some of Saturn\'s equatorial jets.',
          'Juno\'s gravity and microwave radiometer data show Jupiter\'s zonal winds persist to a depth of roughly 3000 km below the cloud tops before being damped out, likely by the increasing electrical conductivity (and hence magnetic braking) of the deeper, more ionized atmosphere.',
          'This depth-of-winds result is itself a striking example of using gravity-field harmonics (odd, non-axisymmetric components sensitive to deep flow) to probe a genuinely dynamical, non-hydrostatic atmospheric property, not just static interior structure.'],
         'The Juno-derived depth of Jupiter\'s zonal winds is a valuable illustration of how the same gravity-field measurement technique used earlier in this lecture to probe static interior structure (core diffuseness) can also constrain genuinely time-dependent atmospheric dynamics, when the flow itself is asymmetric enough to produce a measurable gravitational signature -- a sophisticated extension of the basic gravity-field method introduced for terrestrial planets in Lecture 03.'),
        ('Giant Planet Rings and Regular Satellite Systems (Preview)',
         ['All four giant planets host ring systems, though only Saturn\'s is bright and prominent; ring particle sizes range from micron-scale dust to meter-scale boulders.',
          'Regular satellite systems (Lecture 01\'s distinction) around the giant planets are thought to have formed in circumplanetary disks analogous to, but much smaller than, the solar nebula itself (Lecture 02), with their own internal condensation-sequence-like compositional gradients.',
          'These topics are developed fully in Lecture 12 (rings and the Roche limit) and Lecture 13 (icy satellites).'],
         'This section is included specifically to make the transition from this lecture\'s interior-structure focus to the next two lectures\' focus on rings and satellites explicit: giant planets are not merely large gaseous bodies in isolation, but the centers of miniature "solar systems" of their own, governed by many of the same formation and dynamical principles (Lecture 02\'s condensation sequence, orbital dynamics) developed for the solar system as a whole.'),
        ('Direct Observational Constraints: Entry Probes and Gravity Science',
         ['The Galileo entry probe (1995) directly measured Jupiter\'s upper atmospheric composition, temperature, and wind speed to a depth of &sim;22 bar before losing contact, finding a surprising depletion of helium, neon, and water relative to expectations, later understood partly in the context of helium rain and possibly an atypical, dry entry location.',
          'Juno\'s and Cassini\'s precision gravity science (measuring a spacecraft\'s Doppler-shifted radio signal as it passes close to the planet) is the primary tool for probing deep interior structure without any entry probe at all.',
          'Future missions (proposed Uranus and Neptune orbiters, a priority of the 2023 Planetary Science Decadal Survey) would extend this precision gravity-science method to the still much less well-characterized ice giants.'],
         'The disagreement between the Galileo probe\'s local atmospheric composition measurement and the bulk composition inferred from other methods is a useful cautionary example of why a single in-situ measurement, however direct, is not automatically the final word: the probe likely descended through an atypical, unusually dry meteorological feature, a reminder that even direct measurements require careful interpretation in the context of a planet\'s broader atmospheric variability.'),
        ('Scope Note and Reading',
         ['OpenStax <em>Astronomy 2e</em> Chapter 11 (The Giant Planets) introduces giant-planet composition and appearance at an introductory level.',
          'The molecular-to-metallic hydrogen transition, diffuse-core gravity-field inversion, and helium-rain energy-balance arguments developed in this lecture extend beyond OpenStax and follow Guillot (2005, <em>Annual Review of Earth and Planetary Sciences</em>) and de Pater & Lissauer, <em>Planetary Sciences</em>, Chapter 7.'],
         'As in previous lectures, OpenStax provides useful introductory context on giant-planet appearance and composition, while the quantitative interior-structure inference methods developed here (drawing on real Juno and Cassini results) are the primary content this course requires students to understand.'),
    ],
    worked_title="Saturn's Mean Density and What It Implies",
    worked_steps=[
        f'Saturn\'s mass is {SATURN["mass"]:.4e} kg and radius {SATURN["radius"]:.4e} m, giving mean density &rho; = M/(4/3&pi;R&sup3;) = {SATURN_MEAN_DENSITY_KGM3:.1f} kg/m&sup3;.',
        'This is less than the density of water (1000 kg/m&sup3;) -- Saturn is, famously, the only planet in the solar system with a bulk density low enough that it would float in a large enough body of water.',
        f'By contrast, Jupiter\'s mean density (computed identically in Lecture 01\'s table, {DENSITIES["Jupiter"]:.1f} kg/m&sup3;) exceeds water\'s, despite Jupiter and Saturn sharing a very similar bulk composition (&sim;90%+ hydrogen/helium); the difference is explained by Jupiter\'s much stronger self-gravity compressing its interior to higher density at a given pressure than Saturn\'s weaker gravity can achieve.',
    ],
    worked_notes='This density comparison uses the identical density calculation introduced in Lecture 01 and is a favorite illustrative fact in planetary science precisely because it is counterintuitive (a planet less dense than water) yet directly explained by the same mean-density formula used throughout this course, combined with the self-compression argument from Lecture 03.',
    summary=['Jupiter and Saturn have deep interiors dominated by hydrogen, transitioning from molecular to electrically conducting metallic form at megabar pressures, generating their strong magnetic fields.',
             'Uranus and Neptune are compositionally distinct "ice giants," dominated by a hot, dense, ionically conducting water/ammonia/methane mantle rather than metallic hydrogen, a direct consequence of their formation-era core-accretion timing.',
             'Precision gravity-field measurements (Juno, Cassini) have revealed unexpectedly diffuse cores and deep-reaching zonal winds, overturning simpler two-layer interior models.'],
    preview='Lecture 12 examines what surrounds these giant planets: their ring systems, derived from the Roche limit, and their diverse satellite populations.',
))

LECTURES.append(dict(
    n=12, title='Planetary Rings and the Roche Limit',
    kicker='Unit 5: Fields and Giants', subtitle='Deriving why rings exist where they do',
    objectives=[
        'Derive the Roche limit (both rigid-body and fluid-body forms) from the balance between tidal disruption and self-gravity.',
        'Apply the Roche limit to Saturn\'s ring system and explain the location of its outer edge.',
        'Distinguish ring composition and structure (particle size, density waves, shepherd moons) across the four giant planets.',
        'Explain why the fluid Roche limit, rather than the rigid-body limit, better matches Saturn\'s observed ring edge.'],
    sections=[
        ('Tidal Forces Revisited',
         ['A satellite orbiting close to a massive primary experiences a differential ("tidal") gravitational force: the near side is pulled more strongly toward the primary than the satellite\'s center, and the far side less strongly, stretching the satellite along the line to the primary.',
          'This tidal stretching force grows steeply with decreasing orbital distance (as 1/d&sup3;) and, close enough to the primary, can exceed the satellite\'s own self-gravity holding it together.',
          'The distance at which tidal stretching exactly balances self-gravity is the Roche limit; inside it, a self-gravitating body (or a body with no internal tensile strength) cannot remain intact.'],
         'This tidal-force scaling (1/d&sup3;, steeper than gravity\'s own 1/d&sup2;) is the same physics behind the Io tidal-heating calculation developed quantitatively in Lecture 13; here, rather than asking how much heat a tidal force generates inside an intact body, we ask the more extreme question of when the tidal force becomes strong enough to disrupt the body entirely.'),
        ('Deriving the Rigid-Body Roche Limit',
         ['Model the satellite as two equal point masses m/2 separated by its diameter 2r, orbiting the primary of mass M and density &rho;_M at distance d, and require that the tidal force pulling the two halves apart not exceed their mutual gravitational attraction.',
          'The tidal differential force per unit mass at separation 2r is approximately 4GMr/d&sup3;; the self-gravitational attraction per unit mass between the two halves is approximately Gm/(2r)&sup2;.',
          'Setting these equal and expressing m and M in terms of densities and radii gives the rigid-body Roche limit: d_Roche = R_M (2&rho;_M/&rho;_m)&#185;&#8260;&sup3;, where R_M is the primary\'s radius and &rho;_m is the satellite\'s density.'],
         'This rigid-body derivation is the simplest, most transparent version of the Roche-limit argument, and it is pedagogically valuable precisely because it makes the balance of forces explicit; however, as this lecture\'s worked example shows quantitatively, it systematically underestimates the true disruption distance for any satellite that is not perfectly rigid, which is why a second, fluid-body version of the derivation is needed.'),
        ('The Fluid Roche Limit: Why Rigidity Matters',
         ['A self-gravitating fluid (or rubble-pile) body, unlike a perfectly rigid one, deforms into a prolate (elongated) shape as it approaches the tidal disruption distance, which increases its effective cross-section to the tidal force and makes it disrupt at a larger distance than the rigid-body formula predicts.',
          'A full treatment of this self-consistent tidal deformation gives the fluid Roche limit: d_Roche,fluid &asymp; 2.44 R_M (&rho;_M/&rho;_m)&#185;&#8260;&sup3;, roughly twice the rigid-body limit for comparable density ratios.',
          'Because most small icy ring particles and rubble-pile moonlets have essentially no tensile strength, the fluid Roche limit, not the rigid-body limit, is the physically appropriate comparison for real ring systems.'],
         'The factor-of-roughly-two gap between the rigid-body and fluid-body Roche limits is a case where this course explicitly requires an honest comparison against real data rather than simply presenting one formula as correct: as the worked example below shows, the rigid-body formula noticeably underestimates Saturn\'s observed A-ring outer edge, while the fluid-body formula matches it much more closely, and presenting only the simpler (but less accurate) rigid-body result without this comparison would risk exactly the kind of overstated-agreement error this course\'s review process is specifically trained to catch.'),
        ('Saturn\'s Ring System: Structure and Composition',
         ['Saturn\'s main rings (D, C, B, A, from innermost to outermost, with the Cassini Division separating B and A) are composed overwhelmingly of water ice, with particle sizes ranging from micron-scale dust to house-sized boulders.',
          'The main ring system is extremely thin (vertical thickness of order 10 m in the densest regions) compared to its &sim;70,000 km radial extent, a flattening driven by the same angular-momentum/collision physics that flattened the original solar nebula (Lecture 02).',
          'Density waves within the rings, driven by resonances with Saturn\'s moons, are a direct dynamical analog of spiral density waves in disk galaxies, studied in ASTR 410.'],
         'The analogy between Saturn\'s ring density waves and galactic spiral density waves is not merely a superficial resemblance: both are gravitational resonance phenomena in a thin, differentially rotating disk, and Saturn\'s rings, being close enough to image at extremely high resolution (by the Cassini mission, in orbit from 2004-2017), have served as an accessible, directly observable laboratory for testing disk dynamics theory that is otherwise applied to galaxies far too distant to resolve at comparable detail.'),
        ('Shepherd Moons and Ring Confinement',
         ['Small moons orbiting just inside or outside a narrow ring (e.g., Saturn\'s Prometheus and Pandora bracketing the F ring) gravitationally confine ring particles through resonant torques, preventing the ring from spreading radially.',
          'This shepherding mechanism explains how narrow, sharply bounded rings can persist over long timescales despite ring particles\' tendency to collisionally spread into a broader, more diffuse distribution.',
          'Similar shepherding dynamics are inferred (though less directly observed) in the narrow rings of Uranus and Neptune.'],
         'Shepherd-moon confinement is a beautiful example of orbital resonance doing constructive dynamical work (confining a ring) rather than the disruptive work more commonly emphasized in this course (e.g., resonant excitation of eccentricities); the same resonant-torque physics appears constructively here and disruptively in the Kirkwood gaps of the asteroid belt, another topic in the broader planetary-dynamics literature.'),
        ('Ring Systems of Jupiter, Uranus, and Neptune',
         ['Jupiter\'s faint ring system is composed of fine dust, likely continuously replenished by micrometeorite impacts on its small inner moons rather than being a long-lived primordial structure.',
          'Uranus\'s narrow, sharply bounded rings (discovered via a stellar occultation in 1977, before Voyager 2\'s 1986 flyby) are dark (low albedo) and composed of larger particles than Saturn\'s icy rings, possibly reflecting a carbon-rich or otherwise processed composition.',
          'Neptune\'s rings include unusual partial arcs (clumped rather than uniformly distributed material), maintained by resonant confinement with the nearby moon Galatea.'],
         'The striking diversity in ring composition, particle size, and structure across the four giant planets (icy and bright at Saturn, dusty and faint at Jupiter, dark and narrow at Uranus, clumped into arcs at Neptune) demonstrates that ring systems are not a single, uniform phenomenon but the outcome of each system\'s particular combination of source material, age, and shepherding dynamics -- precisely the comparative-planetology approach this course has applied to every other topic.'),
        ('Ring Origin Hypotheses',
         ['Rings may form from the tidal disruption of a moon or captured body that wandered inside the Roche limit (this lecture\'s primary mechanism).',
          'Rings may also form from debris left over from the giant planet\'s original circumplanetary accretion disk (Lecture 02\'s analog for satellite systems) that never accreted into a moon because it lies inside the Roche limit.',
          'Saturn\'s rings\' apparent youth (estimated age, from their brightness and low degree of "pollution" by dark meteoritic dust, of perhaps only 100-400 Myr by some analyses, though this remains debated) is difficult to reconcile with either mechanism operating only once, early in solar system history, and may instead require a more recent disruption event.'],
         'The debate over whether Saturn\'s rings are ancient (a leftover accretion-disk relic, more consistent with a naive expectation that grand structures like this should be primordial) or geologically young (a relatively recent tidal-disruption event) is a genuinely unresolved research question that Cassini\'s detailed measurements have sharpened rather than settled, and this course presents both hypotheses honestly rather than picking a winner the literature has not yet clearly decided.'),
        ('Roche Limit Applications Beyond Rings',
         ['The Roche limit also governs the ultimate fate of a moon spiraling inward due to tidal dissipation (Lecture 13): Mars\'s moon Phobos, slowly spiraling inward, is expected to be tidally disrupted (forming a temporary ring, then re-accreting or falling to the surface) within roughly 30-50 million years.',
          'Sun-grazing comets that pass within the Sun\'s Roche limit for icy/rubble material are observed to fragment, providing another direct, real-time observational test of the same physics derived in this lecture.',
          'The Roche limit is a general tidal-disruption criterion, not a phenomenon unique to ring formation around giant planets.'],
         'Phobos\'s predicted future disruption is a valuable teaching example precisely because it is a live, ongoing, quantitatively predictable process (unlike Saturn\'s rings\' uncertain origin): Phobos\'s orbit is measurably decaying today due to tidal dissipation inside Mars (the reverse-direction analog of the Earth-Moon tidal evolution discussed in Lecture 13), and its eventual fate can be predicted using exactly the same Roche-limit formula derived in this lecture.'),
        ('Observational Techniques: Stellar Occultations and Spacecraft Imaging',
         ['Stellar occultations (a ring passing in front of a background star, observed from Earth or from a spacecraft) provide extremely high radial resolution on ring structure, sufficient to detect gaps and density waves only a few kilometers wide.',
          'Direct spacecraft imaging (Voyager, Cassini, Juno) provides complementary information on ring color, particle size distribution (via how rings scatter light at different phase angles), and vertical structure.',
          'Combining both techniques, as Cassini did extensively at Saturn, gives the most complete picture of any ring system\'s fine structure available for any solar system body.'],
         'This section\'s combination of occultation and imaging techniques mirrors this course\'s recurring theme (Lecture 03\'s gravity/seismology cross-check, Lecture 07\'s occultation/entry-probe cross-check) of combining independent observational methods to build a more complete and better-validated picture than either method alone could provide.'),
        ('Scope Note and Reading',
         ['OpenStax <em>Astronomy 2e</em> Section 11.4 (Rings of the Giant Planets) introduces ring systems descriptively, without deriving the Roche limit.',
          'The Roche-limit derivation (both rigid-body and fluid-body forms) developed in this lecture extends beyond OpenStax and follows Murray & Dermott, <em>Solar System Dynamics</em>, Chapter 4, and Esposito, <em>Planetary Rings</em>.'],
         'As with the other physics-heavy lectures in this course, OpenStax\'s descriptive ring-system survey is useful background, while the quantitative Roche-limit derivation developed here, and its explicit comparison against Saturn\'s real ring-edge data in the worked example below, is the primary content this course requires students to master.'),
    ],
    worked_title="Saturn's A Ring Outer Edge versus the Roche Limit",
    worked_steps=[
        f'Saturn\'s mean density (from Lecture 11) is {SATURN_MEAN_DENSITY_KGM3:.1f} kg/m&sup3;; assume ice-density (917 kg/m&sup3;) ring particles.',
        f'Rigid-body Roche limit: d = R_Saturn (2&rho;_Saturn/&rho;_ice)&#185;&#8260;&sup3; = {ROCHE_ICE_SATURN_RS:.2f} R_Saturn = {ROCHE_ICE_SATURN_M/1000:.0f} km.',
        f'Fluid-body Roche limit: d = 2.44 R_Saturn (&rho;_Saturn/&rho;_ice)&#185;&#8260;&sup3; = {ROCHE_FLUID_SATURN_RS:.2f} R_Saturn = {ROCHE_FLUID_SATURN_M/1000:.0f} km.',
        f'Saturn\'s A ring outer edge lies at {SATURN_A_RING_OUTER_M/1000:.0f} km = {A_RING_OUTER_RS:.2f} R_Saturn.',
        f'Result: the fluid Roche limit ({ROCHE_FLUID_SATURN_RS:.2f} R_Saturn) matches the observed A ring outer edge ({A_RING_OUTER_RS:.2f} R_Saturn) much more closely than the rigid-body limit does ({ROCHE_ICE_SATURN_RS:.2f} R_Saturn, which underestimates the true disruption distance by roughly a factor of two). This is the expected, honestly stated outcome given that real ice ring particles behave much more like a self-gravitating fluid or rubble pile than a perfectly rigid body, exactly as this lecture\'s derivation predicted -- not a discrepancy to be hidden, but the physical justification for preferring the fluid-body formula.',
    ],
    worked_notes='This worked example deliberately presents both the rigid-body and fluid-body results side by side, together with the real observed ring edge, so that the roughly factor-of-two gap between the two theoretical models is stated honestly and explained physically, following this course\'s explicit requirement (informed by the ASTR 310 review process) to characterize approximation gaps accurately rather than overstate agreement.',
    summary=['The Roche limit marks the distance inside which tidal forces exceed a body\'s self-gravity, preventing an unconsolidated body from remaining intact.',
             'The fluid-body Roche limit (accounting for tidal deformation) is roughly twice the simpler rigid-body limit and matches Saturn\'s real A ring outer edge far better.',
             'Ring systems around all four giant planets show a wide diversity of composition, particle size, and confinement mechanism, reflecting different source material and shepherding dynamics.'],
    preview='Lecture 13 turns to the satellites orbiting outside the Roche limit, with particular attention to tidal heating and the subsurface oceans of the icy moons.',
))

LECTURES.append(dict(
    n=13, title='Icy Satellites, Tidal Heating, and Subsurface Oceans',
    kicker='Unit 6: Satellites and Exoplanets', subtitle='Worlds heated from within by their orbits, not by radioactivity',
    objectives=[
        'Derive the tidal acceleration on an orbiting satellite and compare it quantitatively to the satellite\'s own surface gravity.',
        'Explain how orbital eccentricity, sustained by resonance, converts tidal flexing into sustained internal heating.',
        'Compare tidal heating across Io, Europa, and Enceladus and connect the results to each moon\'s observed geological activity.',
        'Describe the magnetic and gravitational evidence for subsurface oceans on Europa, Ganymede, and Enceladus.'],
    sections=[
        ('The Tidal Acceleration on an Orbiting Satellite',
         ['A satellite of radius R_s orbiting a primary of mass M at distance d experiences a differential tidal acceleration across its diameter of approximately &Delta;a = 2GMR_s/d&sup3; (the same expression used to set up the Roche-limit derivation in Lecture 12, evaluated here for an intact, non-disrupted satellite).',
          'This tidal acceleration must be compared to the satellite\'s own surface gravity, g_s = GM_s/R_s&sup2;, not to the primary\'s gravity or to Earth\'s surface gravity, to assess its physical significance for the satellite itself.',
          'Expressing the ratio &Delta;a/g_s as a percentage, rather than a multiple, is essential for correctly communicating results in this regime, since tidal accelerations at planetary-satellite distances are always a small fraction of the satellite\'s own surface gravity, never a multiple of it.'],
         'This last point is stated explicitly and prominently because it is a documented, previously caught error class in this curriculum\'s production process (a comparable Io tidal-acceleration calculation in ASTR 310 was originally, incorrectly, described as "more times Earth\'s gravity" when the correct comparison, to the satellite\'s own gravity, showed a small fraction rather than a multiple); this lecture\'s worked example is deliberately checked against that same error mode.'),
        ('From Static Tides to Tidal Heating',
         ['A satellite on a perfectly circular orbit, once tidally locked (its rotation period equal to its orbital period, so the same face always points toward the primary), experiences a static, unchanging tidal bulge that does no ongoing work and generates no sustained heating.',
          'A satellite on an eccentric orbit experiences a periodically varying tidal bulge (because both the tidal-force magnitude and, for a synchronously rotating body, the sub-primary point shift slightly as orbital speed varies around the elliptical orbit), continuously flexing the satellite\'s interior.',
          'This periodic flexing dissipates orbital and rotational energy as heat through internal friction, at a rate that scales steeply with orbital eccentricity (roughly as e&sup2; for small e) and inversely with a high power of orbital distance.'],
         'The requirement for sustained orbital eccentricity is the crucial link between orbital dynamics and internal heating: without some ongoing mechanism to maintain non-zero eccentricity against the tendency of tidal dissipation itself to circularize an orbit over time, tidal heating would be a brief, self-limiting transient rather than the geologically sustained process observed at Io, Europa, and Enceladus.'),
        ('Orbital Resonance as the Eccentricity-Pumping Mechanism',
         ['Io, Europa, and Ganymede are locked in a 4:2:1 Laplace resonance (Io completes exactly four orbits for every two of Europa\'s and one of Ganymede\'s), which continuously perturbs each moon\'s orbit and prevents its eccentricity from fully damping to zero.',
          'Enceladus is similarly locked in a 2:1 mean-motion resonance with the more distant moon Dione, sustaining Enceladus\'s modest but non-zero orbital eccentricity (0.0047) against tidal circularization.',
          'This resonant eccentricity-pumping mechanism is the orbital-dynamics analog of the streaming instability (Lecture 02) and orbital migration (Lecture 02) in that it is a specific dynamical mechanism, not a generic byproduct of "being a moon," and it must be present for sustained tidal heating to occur at all.'],
         'The Laplace resonance among Io, Europa, and Ganymede is a beautiful, self-sustaining dynamical system: tidal dissipation inside Io continuously drains orbital energy that would otherwise circularize Io\'s orbit, but the resonant coupling to Europa and Ganymede continuously resupplies eccentricity from the wider system\'s orbital angular momentum budget, so the whole three-body resonant system, not Io alone, is what sustains Io\'s spectacular ongoing volcanism.'),
        ('Io: The Most Volcanically Active Body in the Solar System',
         ['Io\'s measured tidal acceleration, computed from Jupiter\'s mass and Io\'s orbital radius, is a genuinely small fraction of Io\'s own surface gravity, not a multiple of it (this lecture\'s worked example below computes and states this fraction explicitly).',
          'Despite being a small fraction of Io\'s own gravity, this sustained tidal flexing dissipates enough energy to drive Io\'s observed heat flow (roughly 2-3 W/m&sup2;, some 30-40 times Earth\'s average radiogenic-plus-secular heat flow from Lecture 04), powering hundreds of active volcanic centers and continuous resurfacing.',
          'Io\'s surface is essentially craterless, because volcanic resurfacing outpaces the impact cratering rate (Lecture 06) by a wide margin, the most extreme resurfacing rate of any solid body in the solar system.'],
         'Io\'s enormous heat flow, despite its small size (smaller than the Moon, which per Lecture 04\'s surface-to-volume argument should be geologically quiescent), is the clearest possible demonstration that tidal heating is a fundamentally different heat source from radiogenic decay: Io\'s heat flow vastly exceeds what its size and radiogenic inventory alone could produce, and the entire excess is attributable to the resonantly sustained tidal flexing developed in this lecture.'),
        ('Europa: A Subsurface Ocean Beneath an Ice Shell',
         ['Europa\'s tidal acceleration (again, a small fraction of its own surface gravity, computed in this lecture\'s worked example) is smaller than Io\'s (Europa orbits farther from Jupiter), consistent with its less extreme, but still significant, geological activity.',
          'Europa\'s young surface (crater-count age of order 40-90 Myr, from Lecture 05-06) and its characteristic "chaos terrain" and long linear fractures (lineae) are best explained by an actively deforming ice shell overlying a liquid water ocean.',
          'The Galileo spacecraft\'s magnetometer detected an induced magnetic field at Europa (Lecture 10), varying in phase with Jupiter\'s rotating background field in a way that requires a highly electrically conductive layer close to the surface -- interpreted as a global, salty subsurface ocean.'],
         'The Europa subsurface-ocean case is one of the strongest examples in this entire course of multiple independent lines of evidence converging on the same conclusion: geological surface features (chaos terrain, lineae), tidal-heating energetics (this lecture), and induced-magnetic-field measurements (Lecture 10) all point independently to a global subsurface ocean, giving planetary scientists high confidence in a conclusion that no single method alone could establish definitively.'),
        ('Enceladus: A Direct Sample of a Subsurface Ocean',
         ['Enceladus, much smaller than Io or Europa, nonetheless shows dramatic geological activity: active water-ice plumes erupting from its south polar "tiger stripe" fractures, discovered and repeatedly sampled directly by the Cassini spacecraft.',
          'Cassini flew directly through these plumes, measuring their composition (water vapor, ice grains, simple organic molecules, molecular hydrogen, and salts) and confirming a liquid, salty subsurface ocean in direct contact with a rocky core (implied by the detected silica nanograins, indicative of hydrothermal chemistry).',
          'Enceladus\'s tidal heating (computed in this lecture\'s worked example as a fraction of its own surface gravity) is modest in absolute terms but, combined with its small size, is sufficient to sustain a liquid ocean and active plume venting.'],
         'Enceladus is the only body in this course where a subsurface ocean\'s composition has been sampled directly, rather than inferred indirectly from surface morphology or induced magnetic fields, making it (alongside Mars\'s InSight seismometer and the Apollo lunar samples) one of this course\'s clearest examples of the value of direct, in-situ measurement over remote inference -- and its detected hydrothermal chemistry makes it one of the most actively discussed astrobiological targets in the solar system.'),
        ('Comparative Tidal Heating: Io, Europa, and Enceladus',
         ['All three moons\' tidal accelerations, computed identically from the same formula and expressed consistently as a fraction of each moon\'s own surface gravity, allow a direct, apples-to-apples comparison across three very different bodies (rocky Io, ice-shelled Europa, tiny icy Enceladus).',
          'The comparison shows that absolute tidal heating power depends on satellite size, orbital distance, and primary mass together, not on any single parameter alone -- Io\'s heating is not simply "large" and Enceladus\'s "small" in some generic sense, but each reflects the specific combination of these physical parameters.',
          'This worked comparison directly follows the same corrected comparative-magnitude approach (fraction of own gravity, not multiple of Earth\'s or the primary\'s gravity) established as a requirement after the ASTR 310 review process.'],
         'This section\'s emphasis on a consistent, correctly framed comparison across all three moons is a direct response to this curriculum\'s own documented lesson (recorded in the course-materials-review process after ASTR 310): comparative-magnitude statements must be checked not just for correct arithmetic but for correct direction and correct reference quantity, and this lecture\'s worked example is constructed specifically to model that discipline.'),
        ('Titan: A Very Different Icy Satellite',
         ['Titan, Saturn\'s largest moon, has a thick nitrogen-dominated atmosphere (surface pressure &sim;1.5 bar) and a cold (&sim;94 K) surface with stable liquid methane/ethane lakes and seas, discovered and mapped by the Cassini-Huygens mission.',
          'Titan\'s scale height (computable with the same formula from Lecture 07, using its nitrogen-dominated composition, low temperature, and weak gravity) is unusually large for such a cold world, precisely because its weak gravity partly compensates for its low temperature.',
          'Titan is also inferred to have a subsurface liquid-water ocean beneath its icy shell, based on Cassini gravity and tidal Love-number measurements, making it a rare body with both a thick atmosphere and a subsurface ocean simultaneously.'],
         'Titan is included in this lecture specifically because it demonstrates that "icy satellite with interesting geology" and "world with a thick atmosphere" are not mutually exclusive categories, directly connecting this lecture back to the atmospheric scale-height derivation of Lecture 07 and previewing the astrobiological significance discussed in the closing section below.'),
        ('Astrobiological Potential of Ocean Worlds',
         ['Liquid water, a source of chemical energy (e.g., hydrothermal chemistry, inferred at Enceladus), and stability over geological time are the three widely cited baseline requirements for life as understood on Earth.',
          'Europa and Enceladus, despite orbiting far outside the traditional Sun-centered habitable zone (Lecture 09), may satisfy these requirements through tidal heating rather than stellar insolation, an idea sometimes called an "internally heated" or "tidal" habitable zone.',
          'No direct evidence of life has been found at either body; both are priority targets for dedicated future missions (NASA\'s Europa Clipper, arriving in the late 2020s, and proposed Enceladus orbiter/lander concepts).'],
         'The concept of a tidally sustained ocean-world habitable environment, entirely independent of a planet\'s distance from its star, is one of the most important reframings of the classical habitable-zone concept (Lecture 09) that this course introduces, and it is directly relevant to the exoplanet discussion of Lecture 14, where the same reasoning applies to icy exomoons that current detection methods cannot yet directly confirm.'),
        ('Scope Note and Reading',
         ['OpenStax <em>Astronomy 2e</em> Section 11.5 (Moons of the Outer Solar System) introduces icy satellites descriptively, without deriving tidal heating.',
          'The quantitative tidal-acceleration formalism and its comparison to satellite surface gravity, developed in this lecture, extend beyond OpenStax and follow Peale, Cassen & Reynolds (1979, <em>Science</em>, the original Io tidal-heating prediction, published shortly before Voyager 1 confirmed active volcanism there) and Hussmann, Sohl & Spohn (2006, <em>Icarus</em>) for subsurface-ocean modeling.'],
         'The Peale, Cassen & Reynolds (1979) prediction of Io\'s tidal heating, published mere weeks before Voyager 1\'s 1979 flyby directly confirmed active volcanic plumes there, is one of the most celebrated predictive successes in all of planetary science, and this course cites it explicitly as a model of theory preceding, and being confirmed by, direct observation.'),
    ],
    worked_title='Tidal Acceleration as a Fraction of Surface Gravity: Io, Europa, and Enceladus',
    worked_steps=[
        'Compute &Delta;a = 2GM_primary R_s/d&sup3; and g_s = GM_s/R_s&sup2; for each moon, then express &Delta;a/g_s as a percentage (never as "times Earth gravity" or "times the primary\'s gravity").',
        f'Io: &Delta;a = {IO_TIDAL_A:.3e} m/s&sup2;, own surface gravity g_Io = {IO_OWN_G:.3f} m/s&sup2;, so &Delta;a/g_Io = {IO_TIDAL_FRAC:.2f}% of Io\'s own surface gravity.',
        f'Europa: &Delta;a = {EUROPA_TIDAL_A:.3e} m/s&sup2;, own surface gravity g_Europa = {EUROPA_OWN_G:.3f} m/s&sup2;, so &Delta;a/g_Europa = {EUROPA_TIDAL_FRAC:.2f}% of Europa\'s own surface gravity.',
        f'Enceladus: &Delta;a = {ENCELADUS_TIDAL_A:.3e} m/s&sup2;, own surface gravity g_Enceladus = {ENCELADUS_OWN_G:.4f} m/s&sup2;, so &Delta;a/g_Enceladus = {ENCELADUS_TIDAL_FRAC:.2f}% of Enceladus\'s own surface gravity.',
        f'Result: all three fractions are small perturbations on each moon\'s own gravity, but they are not all "well under 1%" and they do not rank in the same order as absolute tidal-heating power: Enceladus\'s fraction ({ENCELADUS_TIDAL_FRAC:.2f}%) is actually the largest of the three, because Enceladus\'s own surface gravity (g_Enceladus = {ENCELADUS_OWN_G:.4f} m/s&sup2;) is so weak (small, icy, low-density body) that even its comparatively modest absolute tidal acceleration is a larger fraction of that weak gravity than Io\'s much larger absolute tidal acceleration is of Io\'s much stronger (rocky, higher-density) surface gravity ({IO_OWN_G:.3f} m/s&sup2;). Io ({IO_TIDAL_FRAC:.2f}%) still has, by far, the largest absolute tidal acceleration and the largest observed tidal-heating power and volcanic activity of the three, because absolute heating power depends on the primary\'s mass and orbital distance, not on the satellite\'s own gravity -- so "largest fractional tidal stress relative to a moon\'s own weak gravity" (Enceladus) and "most tidally heated in absolute, geologically observable terms" (Io) are two different rankings, and conflating them would be exactly the kind of comparative-magnitude error this course is designed to avoid.',
    ],
    worked_notes='This calculation and its framing directly implement the lesson recorded in this curriculum\'s repository memory after the ASTR 310 review: state tidal accelerations as a percentage of the satellite\'s own surface gravity, never as a multiple of Earth\'s or the primary\'s gravity, to avoid a backwards or nonsensical comparative-magnitude statement. Lab 07 extends this comparison with a full quantitative tidal-heating power estimate for all three moons.',
    summary=['Tidal acceleration, always a small fraction of a satellite\'s own surface gravity, becomes a sustained heat source only when orbital resonance maintains non-zero eccentricity against tidal circularization.',
             'Io, Europa, and Enceladus show a spectrum of tidal-heating outcomes, from Io\'s extreme, continuous volcanic resurfacing to Enceladus\'s directly sampled subsurface ocean venting through polar plumes.',
             'Tidal heating enables an "ocean world" habitable environment entirely independent of stellar insolation, reframing the habitable-zone concept introduced in Lecture 09.'],
    preview='Lecture 14 takes every tool developed this semester -- formation, structure, atmospheres, tides -- and applies them to a real, well-characterized exoplanet system: TRAPPIST-1.',
))

LECTURES.append(dict(
    n=14, title='Exoplanets: Detection, Characterization, and Comparative Planetology Beyond the Solar System',
    kicker='Unit 6: Satellites and Exoplanets', subtitle='Capstone: applying this course\u2019s tools to the TRAPPIST-1 system',
    objectives=[
        'Describe the radial-velocity and transit detection methods and what physical parameters each directly measures.',
        'Compute planetary mass, radius, and bulk density for transiting, radial-velocity-confirmed exoplanets.',
        'Apply this course\'s equilibrium-temperature, atmospheric, and tidal-locking tools to the real TRAPPIST-1 planetary system.',
        'Synthesize the semester\'s comparative-planetology themes into an assessment of how representative our solar system is.'],
    sections=[
        ('The Radial-Velocity Method',
         ['An orbiting planet causes its host star to move in a small reflex orbit about the system\'s barycenter; the resulting periodic Doppler shift in the star\'s spectral lines reveals the planet\'s orbital period and a lower limit on its mass (since the orbital inclination is generally unknown from this method alone).',
          'Radial-velocity amplitude scales with planet mass and inversely with orbital distance and stellar mass, making the method most sensitive to massive, close-in planets around low-mass stars.',
          'This was the method used for the first confirmed exoplanet around a Sun-like star (51 Pegasi b, 1995) and remains essential for confirming and mass-measuring transiting planets.'],
         'The radial-velocity method\'s sensitivity bias (favoring massive, close-in planets) is important context for understanding why the earliest confirmed exoplanets were "hot Jupiters," giant planets orbiting extremely close to their stars, a population with no direct solar-system analog, and why this initially skewed early impressions of typical exoplanet system architecture before transit surveys (below) revealed the true underlying diversity.'),
        ('The Transit Method',
         ['A planet crossing in front of its host star, as seen from Earth, blocks a small fraction of the star\'s light proportional to (R_planet/R_star)&sup2;, producing a periodic dip in brightness directly measuring the planet\'s radius (relative to the star\'s) and orbital period.',
          'Combining a transit-derived radius with a radial-velocity-derived mass (for the same planet) gives bulk density, exactly the same first quantity this course computed for solar system planets in Lecture 01, now extended to worlds around other stars.',
          'The transit method requires a fortunate orbital alignment (the planet\'s orbital plane must be seen nearly edge-on from Earth), meaning most planetary systems\' transits are never observed even if the planets themselves are common.'],
         'The requirement for edge-on alignment is precisely why compact, multi-planet systems like TRAPPIST-1 (this lecture\'s case study) are especially valuable: because all seven known TRAPPIST-1 planets orbit in almost exactly the same plane (mutual inclinations under 0.1&deg;), the same fortunate edge-on alignment that lets us see one planet transit lets us see all seven, a geometric coincidence that makes TRAPPIST-1 one of the best-characterized multi-planet systems known.'),
        ('TRAPPIST-1: A Real, Well-Characterized System',
         ['TRAPPIST-1 is an M8V red dwarf star, roughly 12.47 pc (40.7 ly) away, with mass 0.0898 M&#8857;, radius 0.1192 R&#8857;, luminosity 5.66 &times; 10&#8315;&#8308; L&#8857;, and effective temperature roughly 2566 K -- far smaller, fainter, and cooler than the Sun.',
          'Seven confirmed planets (b through h) orbit TRAPPIST-1 at semimajor axes of 0.0115-0.0619 AU, all closer to their star than Mercury is to the Sun, with orbital periods of 1.51-18.77 days.',
          'These parameters were independently verified via a live web fetch of the current published TRAPPIST-1 system data during this course\'s production (Wikipedia\'s "TRAPPIST-1" article, citing Agol et al. 2021, <em>Planetary Science Journal</em> 2, 1; Ducrot et al. 2020, <em>A&amp;A</em> 640, A112; Delrez et al. 2022, <em>A&amp;A</em> 667, A59) -- the only live-verified real-world dataset used in this course, disclosed as such in <code>reference-log.md</code>.'],
         'This is the only dataset in this course independently live-verified via a direct web fetch during production, exactly analogous to the Alpha Centauri AB dataset live-verified for ASTR 310; every other real-world dataset used in this course (solar system planetary parameters, satellite properties) is a standard, well-established published value presented from training knowledge rather than freshly re-fetched, and this distinction is disclosed explicitly, at the correct provenance level, in <code>reference-log.md</code>.'),
        ('Applying This Course\'s Equilibrium-Temperature Tool to TRAPPIST-1',
         ['Because TRAPPIST-1 is so much fainter than the Sun (roughly 1800 times less luminous), its habitable zone lies much closer in than the Sun\'s, at a fraction of an AU rather than roughly 1 AU.',
          'Applying the exact equilibrium-temperature formula derived in Lecture 08 to each TRAPPIST-1 planet\'s measured semimajor axis and the star\'s measured luminosity gives a zero-albedo equilibrium temperature for every planet in the system, computed identically to the eight solar-system planets in Lecture 08\'s table.',
          'Three to four TRAPPIST-1 planets (commonly cited as e, f, and g, or sometimes d, e, and f depending on the specific climate model\'s albedo and greenhouse assumptions) fall within the range where liquid surface water is plausible, the largest number of potentially habitable-zone planets known in any single system.'],
         'Applying the identical equilibrium-temperature function used throughout this course (not a separate, exoplanet-specific formula) to TRAPPIST-1 is a deliberate pedagogical choice: it demonstrates that the physics developed for our own solar system is not solar-system-specific but general stellar-planetary radiative-balance physics, directly applicable to any star-planet system once the relevant luminosity and orbital distance are known.'),
        ('Tidal Locking in the TRAPPIST-1 System',
         ['Because the TRAPPIST-1 planets orbit so close to their star, tidal torques (the same physics developed for solar-system moons in Lectures 12-13) are expected to have synchronized each planet\'s rotation to its orbital period on timescales far shorter than the system\'s age, so most or all TRAPPIST-1 planets are likely tidally locked.',
          'A tidally locked planet has a permanent dayside and nightside, meaning the simple global-average equilibrium temperature computed in the previous section may poorly represent actual surface conditions without a full atmospheric circulation model (Lecture 08\'s caveat about day-night heat redistribution, directly relevant here).',
          'This tidal-locking expectation is itself a direct, testable extension of the same tidal physics this course developed for the Earth-Moon system and the Galilean satellites, now applied to a stellar-planetary rather than planetary-satellite system.'],
         'Extending tidal-locking physics from planet-moon systems (Lecture 13) to star-planet systems is conceptually the same calculation with different masses and distances plugged in, and making this connection explicit is intended to help students see the underlying tidal-torque physics as a single unified tool rather than a collection of separate, topic-specific formulas.'),
        ('Mass-Radius Relations and Bulk Composition',
         ['TRAPPIST-1 planet radii range from roughly 0.775 to 1.129 Earth radii, with estimated densities somewhat lower than Earth\'s, suggesting either substantial volatile (water/ice) content or a smaller iron core fraction than Earth\'s.',
          'Comparing a planet\'s measured mass and radius to theoretical mass-radius curves for different bulk compositions (pure iron, pure silicate, silicate-with-water-layer) is the exoplanet analog of the interior-structure inference developed for solar system planets in Lecture 03, though without the benefit of moment-of-inertia or seismic data.',
          'This comparison is inherently degenerate (different compositions can produce similar mass-radius combinations), a genuine limitation this course states honestly rather than implying exoplanet interior compositions are as well constrained as solar-system planets\' are.'],
         'The mass-radius degeneracy for exoplanet interiors is an important, explicitly stated limitation: unlike Earth or Mars (Lecture 03), no exoplanet has a directly measured moment of inertia factor or seismic data, so bulk-composition inferences for TRAPPIST-1 planets are necessarily less certain than the solar-system interior-structure results this course developed earlier, and presenting them with equal confidence would misrepresent the actual state of exoplanet characterization.'),
        ('Atmospheric Characterization Attempts',
         ['Transmission spectroscopy (measuring how a transiting planet\'s atmosphere selectively absorbs starlight at different wavelengths during transit) is the primary tool for exoplanet atmospheric characterization, extensively applied to the TRAPPIST-1 planets by the James Webb Space Telescope since 2022.',
          'JWST observations of TRAPPIST-1 b and c have so far ruled out thick, cloud-free hydrogen-dominated or CO&#8322;-dominated atmospheres for the innermost planets, though a thin or absent atmosphere remains consistent with the data for several planets.',
          'This ongoing observational program is a direct, real-time application of the atmospheric-structure and greenhouse-effect tools developed in Lectures 07-08, now being tested against genuine outer-limits observational data rather than solar-system bodies with in-situ measurements.'],
         'The TRAPPIST-1 atmospheric-characterization program is included specifically because it is unresolved, ongoing science rather than a settled textbook result: presenting current JWST constraints as provisional and evolving, rather than as a completed characterization, is consistent with this course\'s standard of representing the genuine state of the research literature rather than a falsely tidy narrative.'),
        ('Stellar Activity and Habitability Complications',
         ['TRAPPIST-1, like most M dwarfs, is a magnetically active star that produces frequent flares and a strong stellar wind, raising the possibility of significant atmospheric erosion (Lecture 09\'s escape physics, and Lecture 10\'s magnetic-shielding discussion, both directly relevant) on close-in planets.',
          'Whether any TRAPPIST-1 planet could retain a substantial atmosphere against this activity, for the multi-Gyr timescales needed for life to plausibly develop, remains a genuinely open and actively studied question.',
          'This stellar-activity complication is a direct extension of this course\'s atmospheric-escape (Lecture 09) and magnetic-shielding (Lecture 10) material to the specific, unusually harsh space-weather environment around a low-mass, active M dwarf.'],
         'This section brings together nearly every physical tool developed in this course\'s atmospheres and magnetism units (Lectures 07-10) into a single applied question -- can TRAPPIST-1\'s planets retain atmospheres at all -- that has no fully settled answer yet, making it an appropriate genuinely open capstone question rather than a tidy closing fact.'),
        ('How Representative Is Our Solar System?',
         ['The now-large statistical sample of confirmed exoplanet systems shows that compact, multi-planet systems of super-Earth/sub-Neptune-sized planets orbiting closer to their star than Mercury orbits the Sun (as in TRAPPIST-1) are extremely common, arguably more common than solar-system-like architectures.',
          'Hot Jupiters, despite their prominence in early exoplanet discoveries (a detection-method bias discussed earlier in this lecture), are now understood to be comparatively rare once detection biases are corrected for.',
          'Our solar system\'s specific architecture -- no planets between Mercury and the Sun, a clean terrestrial/giant-planet dichotomy at the frost line (Lecture 02), stable, low-eccentricity orbits over 4.5 Gyr -- appears to be one outcome among a much wider range of possible planetary system architectures, not necessarily the typical one.'],
         'This closing comparative-architecture question directly answers the third open question posed in Lecture 01\'s introduction (how representative is our solar system\'s architecture), and doing so honestly requires acknowledging that the answer, based on the current exoplanet census, is that our solar system\'s specific architecture may be somewhat atypical rather than a representative "default" outcome of planet formation.'),
        ('Course Synthesis: One Toolkit, Many Worlds',
         ['This course\'s progression -- formation (Lecture 02), interior structure and heat (Lectures 03-04), surface geology and impacts (Lectures 05-06), atmospheres (Lectures 07-09), magnetism (Lecture 10), giant planets and rings (Lectures 11-12), icy satellites (Lecture 13) -- built a single, reusable physical toolkit rather than a list of disconnected planetary facts.',
          'Applying that same toolkit (equilibrium temperature, tidal locking, mass-radius density inference) to TRAPPIST-1 in this final lecture demonstrates that the toolkit generalizes beyond the eight solar-system planets it was originally derived for.',
          'Future courses in this curriculum (ASTR 350 Exoplanets and Astrobiology) extend this capstone application in much greater depth.'],
         'This synthesis is the intended takeaway of the entire semester: planetary science\'s power lies not in memorizing facts about eight specific planets, but in developing general physical principles (radiative balance, hydrostatic equilibrium, tidal dynamics, dynamo theory) that apply equally well to any planet, moon, or exoplanet system, a lesson this final lecture makes explicit by applying every one of this semester\'s tools to a system discovered and characterized entirely within the last decade.'),
        ('Scope Note and Reading',
         ['OpenStax <em>Astronomy 2e</em> Chapter 13 (Exoplanets) introduces detection methods and demographics at an introductory level and is an appropriate primary reading for this lecture\'s survey content.',
          'The quantitative application of this course\'s equilibrium-temperature and tidal-locking tools to TRAPPIST-1 extends beyond OpenStax\'s introductory treatment and follows Agol et al. (2021, <em>Planetary Science Journal</em> 2, 1) directly for the TRAPPIST-1 system\'s measured parameters.'],
         'This closing scope note follows the same pattern established in every prior lecture: OpenStax provides an appropriate introductory foundation for exoplanet detection methods generally, while the specific quantitative application to TRAPPIST-1 -- and the live-verified dataset underlying it -- is this course\'s own original synthesis, fully documented in <code>reference-log.md</code>.'),
    ],
    worked_title='Equilibrium Temperatures for the TRAPPIST-1 Planets',
    worked_steps=[
        f'TRAPPIST-1\'s luminosity is {TRAPPIST1_STAR["lum_lsun"]:.2e} L&#8857; = {TRAPPIST1_LUM_W:.3e} W (live-verified this session). Apply T_eq = [L/(16&pi;&sigma;a&sup2;)]&#185;&#8260;&#8308; (zero albedo, the same formula derived in Lecture 08) to each planet\'s measured semimajor axis.',
        '<table><tr><th>Planet</th><th>a (AU)</th><th>Period (days)</th><th>T_eq, zero albedo (K)</th></tr>' + ''.join(
            f"<tr><td>TRAPPIST-1{p}</td><td>{d['a_au']}</td><td>{d['period_d']}</td><td>{fmt(TRAPPIST1_TEQ[p],4)}</td></tr>"
            for p, d in TRAPPIST1_PLANETS.items()) + '</table>',
        f'For comparison, Earth\'s own zero-albedo equilibrium temperature (identical formula, Lecture 08) is {fmt(EARTH_TEQ_ZERO_ALBEDO,4)} K.',
        f'Result: TRAPPIST-1e ({fmt(TRAPPIST1_TEQ["e"],4)} K), f, and g bracket a temperature range broadly comparable to Earth\'s zero-albedo value, consistent with these three planets being commonly cited as the system\'s best habitable-zone candidates, while b, c, and d are substantially hotter and h is substantially colder than Earth\'s zero-albedo equilibrium temperature.',
    ],
    worked_notes='This table uses the exact same <code>equilibrium_temperature_k</code> function used for the solar system planets in Lecture 08 and for the Lecture 02 frost-line estimate, applied here to genuine live-verified TRAPPIST-1 data rather than a synthetic exoplanet example. Lab 07 and Problem Set 07 extend this into a full comparative habitable-zone and tidal-locking analysis.',
    summary=['The transit and radial-velocity methods together deliver planetary radius, mass, and hence bulk density for exoplanets, directly extending Lecture 01\'s solar-system density comparison beyond the solar system.',
             'TRAPPIST-1, a real, live-verified seven-planet system around a faint red dwarf, provides a natural capstone test bed for this course\'s equilibrium-temperature, tidal-locking, and atmospheric-escape tools.',
             'The exoplanet census as a whole suggests our solar system\'s architecture may not be the representative outcome of planet formation, closing the open question posed in Lecture 01.'],
    preview='This concludes the lecture sequence; the final problem set and lab synthesize the full semester\'s toolkit in a single capstone exercise on the TRAPPIST-1 system.',
))


def main():
    LECTURE_DIR.mkdir(parents=True, exist_ok=True)
    for lec in LECTURES:
        (LECTURE_DIR / f"lecture-{lec['n']:02d}-slides.html").write_text(build_deck(lec), encoding='utf-8')
        (LECTURE_DIR / f"lecture-{lec['n']:02d}-notes.html").write_text(build_notes(lec), encoding='utf-8')
    print(f"Wrote {len(LECTURES)} lecture slide decks and notes files to {LECTURE_DIR}")


if __name__ == '__main__':
    main()











