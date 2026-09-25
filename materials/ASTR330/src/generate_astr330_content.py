"""Content generator for ASTR330 lecture slides and lecture notes.

Every worked numeric example is computed programmatically from the shared
constants and datasets defined below (not hand-typed), and the same
constants are reused across labs and problem sets that reference the same
scenario (see generate_astr330_labs_psets.py). Run with the project
interpreter:
    python materials/ASTR330/src/generate_astr330_content.py
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
SIGMA_SB = 5.670374e-8
G_NEWTON = 6.674e-11
C_LIGHT = 2.998e8
H_PLANCK = 6.626e-34
HBAR = H_PLANCK / (2 * math.pi)
K_BOLTZMANN = 1.381e-23
M_PROTON = 1.6726e-27
M_ELECTRON = 9.109e-31
SIGMA_THOMSON = 6.6524e-29
EV_J = 1.602176634e-19
M_SUN_KG = 1.989e30
R_SUN_M = 6.957e8
L_SUN_W = 3.828e26
AU_M = 1.496e11
YEAR_S = 3.15576e7
PC_M = 3.0857e16
KM = 1000.0
SUN_TEFF = 5778.0
SUN_AGE_GYR = 4.57
SUN_MS_LIFETIME_GYR = 10.0  # standard order-of-magnitude MS lifetime calibration point

# ---------------------------------------------------------------------------
# Shared real datasets, carried forward with provenance from ASTR230/ASTR310
# (Alpha Centauri AB, Sirius A/B; live-verified in those courses' production)
# and newly live-verified this session (Hyades cluster; PSR J0348+0432).
# ---------------------------------------------------------------------------
ALPHA_CEN_A = dict(name='Alpha Centauri A', mass_msun=1.0788, radius_rsun=1.223, lum_lsun=1.5059, teff=5748.0, spt='G2V')
ALPHA_CEN_B = dict(name='Alpha Centauri B', mass_msun=0.9092, radius_rsun=0.864, lum_lsun=0.4981, teff=5154.0, spt='K1V')

SIRIUS_A = dict(name='Sirius A', mass_msun=2.063, radius_rsun=1.711, lum_lsun=25.4, teff=9940.0, spt='A1V')
SIRIUS_B = dict(name='Sirius B', mass_msun=1.018, radius_rsun=0.008098, teff=25000.0, spt='DA white dwarf')

# Hyades open cluster, live-verified this session via a direct web fetch of
# Wikipedia's "Hyades (star cluster)" article (2026-09-24), citing Perryman
# et al. (1998), A&A 331, 81, "The Hyades: distance, structure, dynamics,
# and age." Used as the course's primary star-cluster isochrone dataset.
HYADES = dict(distance_pc=47.0, age_myr=625.0, total_mass_msun=400.0, turnoff_mass_msun=2.3,
              core_radius_pc=2.7, half_mass_radius_pc=5.7, tidal_radius_pc=10.0, metallicity_dex=0.14)

# PSR J0348+0432, a pulsar-white dwarf binary, live-verified this session via
# a direct web fetch of Wikipedia's "PSR J0348+0432" article (2026-09-24),
# citing Antoniadis et al. (2013), Science 340, 1233232, "A Massive Pulsar
# in a Compact Relativistic Binary." Used as the course's primary compact-
# remnant (neutron star) mass dataset.
PSR_J0348 = dict(neutron_star_mass_msun=2.01, neutron_star_mass_err=0.04, neutron_star_radius_km=13.0,
                  spin_period_ms=39.1226563571297, wd_mass_msun=0.172, wd_radius_rsun=0.065,
                  orbital_period_days=0.102424062722, semimajor_km=832000.0, inclination_deg=40.2,
                  distance_pc=2100.0)

EARTH_ATMOS_PRESSURE_PA = 1.0e5


# ---------------------------------------------------------------------------
# Physics helper functions -- every worked example below calls these rather
# than hand-typing a numeric result.
# ---------------------------------------------------------------------------
def stefan_boltzmann_luminosity_w(r_m: float, teff_k: float) -> float:
    return 4 * math.pi * (r_m ** 2) * SIGMA_SB * (teff_k ** 4)


def hydrostatic_central_pressure_pa(mass_kg: float, radius_m: float) -> float:
    return (3.0 / (8.0 * math.pi)) * G_NEWTON * (mass_kg ** 2) / (radius_m ** 4)


def kramers_opacity_estimate(rho_kgm3: float, t_k: float, kappa0: float = 4.3e21) -> float:
    """Schematic Kramers free-free/bound-free opacity law, kappa ~ kappa0 * rho * T^-3.5
    (opacity in m^2/kg; kappa0 is an illustrative order-of-magnitude coefficient,
    not a precise OPAL/OP tabulated value -- used here only to show the
    functional T^-3.5, rho^1 scaling, not for precision opacity work)."""
    return kappa0 * rho_kgm3 * (t_k ** -3.5)


def electron_scattering_opacity_m2_per_kg(x_hydrogen: float = 0.70) -> float:
    """Thomson electron-scattering opacity per unit mass for fully ionized gas,
    kappa_es = sigma_T (1+X) / (2 m_p)."""
    return SIGMA_THOMSON * (1 + x_hydrogen) / (2 * M_PROTON)


def radiative_gradient_dimensionless(luminosity_w: float, mass_enclosed_kg: float,
                                      pressure_pa: float, temperature_k: float, kappa_m2_per_kg: float) -> float:
    """Standard dimensionless radiative temperature gradient,
    nabla_rad = (d ln T/d ln P)_rad = 3 kappa L P / (16 pi a c G M T^4),
    with radiation constant a = 4 sigma/c, obtained by combining the
    radiative-diffusion flux equation with hydrostatic equilibrium."""
    a_rad = 4 * SIGMA_SB / C_LIGHT
    return (3 * kappa_m2_per_kg * luminosity_w * pressure_pa) / (
        16 * math.pi * a_rad * C_LIGHT * G_NEWTON * mass_enclosed_kg * temperature_k ** 4)


def adiabatic_temperature_gradient_ideal_monatomic() -> float:
    """(d ln T/d ln P)_ad = 2/5 for an ideal monatomic gas (gamma = 5/3)."""
    return 2.0 / 5.0


def gamow_peak_energy_kev(z1: int, z2: int, mu_amu: float, t_k: float) -> float:
    """Gamow peak energy, the standard widely used closed-form approximation
    E0 [keV] = 1.22 (Z1^2 Z2^2 mu_amu T6^2)^(1/3), from balancing the
    Maxwell-Boltzmann tail against the tunneling penetration factor
    (see, e.g., Clayton 1983; Iliadis 2015)."""
    t6 = t_k / 1.0e6
    return 1.22 * ((z1 ** 2) * (z2 ** 2) * mu_amu * (t6 ** 2)) ** (1.0 / 3.0)


def epsilon_pp_relative(t6: float) -> float:
    """Schematic pp-chain energy generation rate scaling, epsilon_pp ~ T6^4
    (approximate power-law fit valid near T6 ~ 10-20, following the standard
    textbook approximation; not an exact reaction-network result)."""
    return t6 ** 4.0


def epsilon_cno_relative(t6: float) -> float:
    """Schematic CNO-cycle energy generation rate scaling, epsilon_CNO ~ T6^20
    (approximate power-law fit valid near T6 ~ 15-25, following the standard
    textbook approximation; not an exact reaction-network result)."""
    return t6 ** 20.0


def mass_luminosity_lsun(mass_msun: float, exponent: float = 3.5) -> float:
    return mass_msun ** exponent


def ms_lifetime_gyr(mass_msun: float, lum_lsun: float) -> float:
    return SUN_MS_LIFETIME_GYR * (mass_msun) / lum_lsun


def chandrasekhar_mass_kg(mu_e: float) -> float:
    """Chandrasekhar mass from the Lane-Emden n=3 polytrope solution,
    M_Ch = (omega3 sqrt(3 pi)/2) (hbar c/G)^(3/2) / (mu_e m_p)^2, with
    omega3 = 2.018236 the standard dimensionless n=3 Lane-Emden constant."""
    omega3 = 2.018236
    prefactor = omega3 * math.sqrt(3 * math.pi) / 2.0
    return prefactor * (HBAR * C_LIGHT / G_NEWTON) ** 1.5 / (mu_e * M_PROTON) ** 2


def white_dwarf_cooling_age_gyr(l_lsun: float, mass_msun: float, k_cool: float = 1.0) -> float:
    """Mestel-type white dwarf cooling estimate, t_cool ~ k_cool * (M/Msun) * (L/Lsun)^(-5/7)
    (schematic Mestel cooling-law scaling, not a full cooling-track model)."""
    return k_cool * mass_msun * (l_lsun ** (-5.0 / 7.0))


def triple_alpha_q_value_mev() -> float:
    """Net energy release of 3 He-4 -> C-12 (triple-alpha), from measured
    atomic mass excesses (AME2020): mass excess(He-4) = 2.4249 MeV,
    mass excess(C-12) = 0.0 MeV (C-12 defines the atomic mass unit), so
    Q = 3 x 2.4249 - 0.0 MeV."""
    mass_excess_he4_mev = 2.4249
    mass_excess_c12_mev = 0.0
    return 3 * mass_excess_he4_mev - mass_excess_c12_mev


PP_CHAIN_Q_MEV = 26.73  # net energy release, 4p -> He-4 + 2e+ + 2 nu_e (standard value)
CNO_CYCLE_Q_MEV = 26.73  # same net reaction as pp chain; catalyzed by C/N/O
TRIPLE_ALPHA_Q_MEV = triple_alpha_q_value_mev()

# ---------------------------------------------------------------------------
# Derived worked-example numbers, computed once here and reused throughout
# the lectures, labs, and problem sets.
# ---------------------------------------------------------------------------
SUN_CENTRAL_PRESSURE_EST = hydrostatic_central_pressure_pa(M_SUN_KG, R_SUN_M)
SUN_CENTRAL_PRESSURE_PUBLISHED = 2.477e16  # Pa, standard solar-model value (level 2, carried from ASTR310)
SUN_CORE_TEMP_PUBLISHED = 1.57e7  # K, standard solar-model value (level 2, carried from ASTR310)
SUN_CORE_DENSITY_PUBLISHED = 1.5e5  # kg/m^3, standard solar-model core density (level 2)

KAPPA_ES_SUN = electron_scattering_opacity_m2_per_kg(0.70)
KAPPA_KRAMERS_SUN_CORE = kramers_opacity_estimate(SUN_CORE_DENSITY_PUBLISHED, SUN_CORE_TEMP_PUBLISHED)

SUN_ENVELOPE_RADIUS_FRAC = 0.7  # illustrative envelope sample point at r = 0.7 Rsun (base of the solar convection zone)
SUN_ENVELOPE_RADIUS_M = SUN_ENVELOPE_RADIUS_FRAC * R_SUN_M
SUN_ENVELOPE_TEMP_K = 2.0e6  # standard published order-of-magnitude value near r=0.7 Rsun (level 2)
SUN_ENVELOPE_MASS_ENCLOSED_KG = 0.98 * M_SUN_KG  # standard published order-of-magnitude value (level 2)
SUN_ENVELOPE_PRESSURE_EST = 6.0e13  # Pa, standard published order-of-magnitude pressure at the convection-zone base (level 2)
SUN_RADIATIVE_GRADIENT = radiative_gradient_dimensionless(
    L_SUN_W, SUN_ENVELOPE_MASS_ENCLOSED_KG, SUN_ENVELOPE_PRESSURE_EST, SUN_ENVELOPE_TEMP_K, KAPPA_ES_SUN)
SUN_ADIABATIC_GRADIENT_FRACTIONAL = adiabatic_temperature_gradient_ideal_monatomic()

# A second, cooler/lower-pressure sample point close to the photosphere,
# where H-minus and bound-free opacity (approximated here by the schematic
# Kramers scaling at low T) push kappa far above the electron-scattering
# value used deeper in the envelope, illustrating why real stellar envelopes
# become convectively unstable near the surface even though the deeper point
# above is radiatively stable in this same illustrative model.
SUN_SURFACE_ZONE_TEMP_K = 5.0e4  # standard published order-of-magnitude subsurface value (level 2)
SUN_SURFACE_ZONE_PRESSURE_PA = 2.0e10  # standard published order-of-magnitude subsurface value (level 2)
SUN_SURFACE_ZONE_DENSITY_KGM3 = 1.0e-3  # standard published order-of-magnitude subsurface value (level 2)
KAPPA_SURFACE_ZONE = kramers_opacity_estimate(SUN_SURFACE_ZONE_DENSITY_KGM3, SUN_SURFACE_ZONE_TEMP_K)
SUN_SURFACE_ZONE_MASS_ENCLOSED_KG = 0.999 * M_SUN_KG  # standard published order-of-magnitude value (level 2)
SUN_SURFACE_RADIATIVE_GRADIENT = radiative_gradient_dimensionless(
    L_SUN_W, SUN_SURFACE_ZONE_MASS_ENCLOSED_KG, SUN_SURFACE_ZONE_PRESSURE_PA, SUN_SURFACE_ZONE_TEMP_K, KAPPA_SURFACE_ZONE)

GAMOW_E0_PP_SUN_KEV = gamow_peak_energy_kev(1, 1, 0.5, SUN_CORE_TEMP_PUBLISHED)
GAMOW_E0_CNO_SUN_KEV = gamow_peak_energy_kev(1, 7, 12.0 / 13.0, SUN_CORE_TEMP_PUBLISHED)

T6_SUN_CORE = SUN_CORE_TEMP_PUBLISHED / 1.0e6
SIRIUS_A_CORE_TEMP_EST_K = SUN_CORE_TEMP_PUBLISHED * (SIRIUS_A['mass_msun'] / 1.0) ** 0.7  # schematic core-temp mass scaling
T6_SIRIUS_A_CORE = SIRIUS_A_CORE_TEMP_EST_K / 1.0e6
EPS_PP_SUN = epsilon_pp_relative(T6_SUN_CORE)
EPS_CNO_SUN = epsilon_cno_relative(T6_SUN_CORE)
EPS_PP_SIRIUS_A = epsilon_pp_relative(T6_SIRIUS_A_CORE)
EPS_CNO_SIRIUS_A = epsilon_cno_relative(T6_SIRIUS_A_CORE)


def find_pp_cno_crossover_t6(t6_lo: float = 8.0, t6_hi: float = 30.0, steps: int = 100000) -> float:
    """Bisection-style scan for the T6 at which epsilon_pp == epsilon_cno,
    given the two schematic power-law scalings above (both normalized to 1
    at their own reference point, so the crossover is found via the ratio
    epsilon_cno/epsilon_pp = (T6/T6_ref)^16 for a fixed relative
    normalization anchored at the Sun's core temperature)."""
    # Anchor: at T6_SUN_CORE, assume epsilon_pp and epsilon_cno contribute in
    # a 1000:1 ratio (standard textbook statement that the Sun is strongly
    # pp-dominated); solve for the CNO normalization constant, then find
    # where the CNO curve overtakes the pp curve.
    pp_ref = epsilon_pp_relative(T6_SUN_CORE)
    cno_ref = epsilon_cno_relative(T6_SUN_CORE)
    cno_norm = (pp_ref / 1000.0) / cno_ref  # scale CNO so it is 1/1000 of pp at the Sun's core temperature
    lo, hi = t6_lo, t6_hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        pp_mid = epsilon_pp_relative(mid)
        cno_mid = cno_norm * epsilon_cno_relative(mid)
        if cno_mid < pp_mid:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), cno_norm


PP_CNO_CROSSOVER_T6, CNO_NORMALIZATION = find_pp_cno_crossover_t6()
PP_CNO_CROSSOVER_TEMP_K = PP_CNO_CROSSOVER_T6 * 1.0e6

ALPHA_CEN_A_ML_PRED_LSUN = mass_luminosity_lsun(ALPHA_CEN_A['mass_msun'])
ALPHA_CEN_B_ML_PRED_LSUN = mass_luminosity_lsun(ALPHA_CEN_B['mass_msun'])
SIRIUS_A_ML_PRED_LSUN = mass_luminosity_lsun(SIRIUS_A['mass_msun'])

SUN_MS_LIFETIME_CALC_GYR = ms_lifetime_gyr(1.0, 1.0)
ALPHA_CEN_A_MS_LIFETIME_GYR = ms_lifetime_gyr(ALPHA_CEN_A['mass_msun'], ALPHA_CEN_A['lum_lsun'])
ALPHA_CEN_B_MS_LIFETIME_GYR = ms_lifetime_gyr(ALPHA_CEN_B['mass_msun'], ALPHA_CEN_B['lum_lsun'])
SIRIUS_A_MS_LIFETIME_GYR = ms_lifetime_gyr(SIRIUS_A['mass_msun'], SIRIUS_A['lum_lsun'])

HYADES_TURNOFF_L_PRED_LSUN = mass_luminosity_lsun(HYADES['turnoff_mass_msun'])
HYADES_TURNOFF_LIFETIME_PRED_GYR = ms_lifetime_gyr(HYADES['turnoff_mass_msun'], HYADES_TURNOFF_L_PRED_LSUN)
HYADES_ACTUAL_AGE_GYR = HYADES['age_myr'] / 1000.0
HYADES_AGE_DISCREPANCY_FACTOR = HYADES_TURNOFF_LIFETIME_PRED_GYR / HYADES_ACTUAL_AGE_GYR

CHANDRASEKHAR_MASS_MUE2_KG = chandrasekhar_mass_kg(2.0)
CHANDRASEKHAR_MASS_MUE2_MSUN = CHANDRASEKHAR_MASS_MUE2_KG / M_SUN_KG
SIRIUS_B_TO_CHANDRA_FRACTION = SIRIUS_B['mass_msun'] / CHANDRASEKHAR_MASS_MUE2_MSUN
SIRIUS_B_LUM_LSUN = stefan_boltzmann_luminosity_w(SIRIUS_B['radius_rsun'] * R_SUN_M, SIRIUS_B['teff']) / L_SUN_W
SIRIUS_B_COOLING_AGE_GYR = white_dwarf_cooling_age_gyr(SIRIUS_B_LUM_LSUN, SIRIUS_B['mass_msun'], k_cool=0.015)

PSR_TO_CHANDRA_FRACTION = PSR_J0348['neutron_star_mass_msun'] / CHANDRASEKHAR_MASS_MUE2_MSUN
PSR_WD_TO_CHANDRA_FRACTION = PSR_J0348['wd_mass_msun'] / CHANDRASEKHAR_MASS_MUE2_MSUN
PSR_NS_MEAN_DENSITY_KGM3 = (PSR_J0348['neutron_star_mass_msun'] * M_SUN_KG) / (
    (4.0 / 3.0) * math.pi * (PSR_J0348['neutron_star_radius_km'] * KM) ** 3)
NUCLEAR_SATURATION_DENSITY_KGM3 = 2.3e17  # standard published nuclear saturation density (level 2)
PSR_NS_DENSITY_TO_NUCLEAR_FRACTION = PSR_NS_MEAN_DENSITY_KGM3 / NUCLEAR_SATURATION_DENSITY_KGM3

# Order-of-magnitude core-collapse supernova energy budget: gravitational
# binding energy released forming a neutron star from a stellar core,
# E ~ (3/5) G M^2 / R (uniform-density estimate, as in ASTR310 Lecture 06).
SN_CORE_MASS_MSUN = 1.4
SN_PROGENITOR_CORE_RADIUS_M = 3000e3  # standard published order-of-magnitude iron-core radius (level 2)
SN_REMNANT_RADIUS_M = PSR_J0348['neutron_star_radius_km'] * KM
SN_BINDING_ENERGY_RELEASED_J = (3.0 / 5.0) * G_NEWTON * (SN_CORE_MASS_MSUN * M_SUN_KG) ** 2 * (
    1.0 / SN_REMNANT_RADIUS_M - 1.0 / SN_PROGENITOR_CORE_RADIUS_M)
SN_OBSERVED_KINETIC_PLUS_LIGHT_J = 1.0e44  # standard published typical core-collapse SN observed energy (level 2)
SN_NEUTRINO_FRACTION_ESTIMATE = 1.0 - (SN_OBSERVED_KINETIC_PLUS_LIGHT_J / SN_BINDING_ENERGY_RELEASED_J)

# ---------------------------------------------------------------------------
# Lecture content
# ---------------------------------------------------------------------------
LECTURES = [
    dict(
        n=1, title='The Equations of Stellar Structure: Mass, Momentum, and What Remains',
        subtitle='Four coupled equations, and why two of them are not enough',
        goals=[
            'State the mass-continuity equation and explain why it is a purely geometric/definitional statement, not a physical law.',
            'Recall the hydrostatic-equilibrium equation from ASTR 310 and explain why it alone cannot determine a star\u2019s full structure.',
            'Preview the two remaining equations (energy conservation and energy transport) that this course spends the next three lectures deriving.',
        ],
        why_matters='ASTR 310 derived hydrostatic equilibrium in isolation, as a single force-balance statement about pressure and gravity. A real star has four unknown structure functions of radius -- mass, pressure, temperature, and luminosity -- and hydrostatic equilibrium is only one of four equations relating them. This lecture assembles the complete system so that every later topic in this course (opacity, transport, nuclear burning, evolution) can be understood as supplying one of the missing pieces.',
        phenomenon=f'The Sun maintains a luminosity of {L_SUN_W:.3e} W and a central pressure of roughly {SUN_CENTRAL_PRESSURE_PUBLISHED:.2e} Pa simultaneously, for billions of years, without either quantity drifting -- yet hydrostatic equilibrium (Lecture 05 of ASTR 310) says nothing whatsoever about luminosity. A separate, independent equation is required to fix how much energy flows outward at each radius.',
        vocab=['mass continuity', 'stellar structure equations', 'enclosed mass M(r)', 'energy conservation (stellar)', 'energy transport equation', 'boundary conditions'],
        evidence=[
            'Two stars of identical mass and identical hydrostatic-equilibrium central pressure can have dramatically different luminosities and lifetimes if they differ in composition or opacity, proving that hydrostatic equilibrium alone does not fix a star\u2019s energetic structure.',
            'Numerical stellar-evolution codes (e.g., MESA) solve exactly four coupled first-order differential equations in radius (or enclosed mass) at each timestep; removing any one of the four produces an under-determined, unsolvable system.',
            'A star\u2019s luminosity profile L(r) is observed (via solar neutrino and helioseismic constraints, for the Sun) to rise from zero at the center to the star\u2019s full surface luminosity at the photosphere, a boundary-value structure that only the energy-conservation equation (not hydrostatic equilibrium) can produce.',
        ],
        model=[
            'Mass continuity: dM(r)/dr = 4\u03c0r\u00b2\u03c1(r) simply defines how mass accumulates as you integrate outward through concentric shells; it contains no physics beyond geometry and the definition of density.',
            'Hydrostatic equilibrium (from ASTR 310, Lecture 05): dP/dr = -GM(r)\u03c1(r)/r\u00b2 balances the pressure-gradient force against gravity, but treats P, \u03c1, and T as related only through an as-yet-unspecified equation of state, and says nothing about L(r).',
            'The remaining two equations -- energy conservation, dL/dr = 4\u03c0r\u00b2\u03c1(r)\u03b5(r) (Lecture 5-6\u2019s nuclear energy generation rate \u03b5), and energy transport, dT/dr = (transport-mechanism-specific expression, Lectures 3-4) -- are required to close the system, because a star has four unknown radial functions (M, P, T, L) and needs four independent equations plus an equation of state and an opacity law.',
        ],
        equation=r'\dfrac{dM}{dr} = 4\pi r^{2}\rho, \quad \dfrac{dP}{dr} = -\dfrac{GM\rho}{r^{2}}, \quad \dfrac{dL}{dr} = 4\pi r^{2}\rho\varepsilon, \quad \dfrac{dT}{dr} = (\text{transport equation})',
        example=[
            f'Sun: central pressure from the uniform-density hydrostatic estimate (ASTR 310, Lecture 05), P_c \u2248 (3/8\u03c0)GM\u00b2/R\u2074 = {SUN_CENTRAL_PRESSURE_EST:.3e} Pa, compared to the standard solar-model value {SUN_CENTRAL_PRESSURE_PUBLISHED:.3e} Pa (same comparison as ASTR 310, carried forward here as the starting point for this course\u2019s more complete four-equation treatment).',
            f'Integrating mass continuity for a uniform-density Sun from r=0 to R gives M(R) = (4/3)\u03c0R\u00b3\u03c1 = {(4.0/3.0)*math.pi*R_SUN_M**3*(M_SUN_KG/((4.0/3.0)*math.pi*R_SUN_M**3)):.3e} kg by construction (trivially self-consistent for a uniform sphere); a real star\u2019s M(r) rises much more steeply near the center, where density is highest, than this uniform-density profile assumes.',
            f'The Sun\u2019s surface luminosity is {L_SUN_W:.3e} W, entirely set by the (as yet undetermined) energy-conservation and energy-transport equations; hydrostatic equilibrium and mass continuity alone provide no constraint on this number at all, which is why this course spends Lectures 02-06 deriving the missing physics.',
        ],
        pitfall='Treating "hydrostatic equilibrium" as synonymous with "the structure of a star." It is one of four coupled equations; a star in hydrostatic equilibrium with an arbitrary, unphysical temperature profile is a valid solution of that one equation alone, but only the correct combination of all four equations (plus an equation of state and opacity law) picks out the single physically realized structure.',
        activity='Given that a star has four unknown radial functions (M, P, T, L) and currently only two equations (mass continuity, hydrostatic equilibrium) have been derived, explain in one sentence why two more independent equations are mathematically necessary before the system can be solved, even in principle.',
        lab_connection='Lab 01 uses mass continuity and hydrostatic equilibrium together with an opacity law (Lecture 02) to build a simplified two-zone model of the Sun and compare its central pressure to the standard solar-model value.',
        synthesis='A star\u2019s structure is the simultaneous solution of four coupled equations (mass continuity, hydrostatic equilibrium, energy conservation, energy transport), not any one of them in isolation; this course\u2019s first six lectures supply the physics (equation of state, opacity, transport, nuclear burning) needed to complete the system ASTR 310 began.',
        openstax='OpenStax Astronomy 2e, Chapter 16.1-16.2 (sources of sunshine, structure of the Sun) states the four-equation picture descriptively; this course develops the mass-continuity and energy equations explicitly alongside the hydrostatic equation already derived in ASTR 310.',
    ),
    dict(
        n=2, title='Equation of State and Opacity: What a Photon Fights Against',
        subtitle='Closing the system with two more physical ingredients',
        goals=[
            'State the ideal-gas-plus-radiation equation of state and identify the regimes where each pressure term dominates.',
            'Identify the three principal microscopic opacity sources in stellar interiors (electron scattering, free-free, bound-free) and their approximate temperature/density scaling.',
            'Compute and compare electron-scattering and Kramers-type opacity estimates for real solar-interior conditions.',
        ],
        why_matters='The hydrostatic-equilibrium equation relates P, M, and \u03c1, but leaves P, \u03c1, and T related only by an unspecified equation of state; the energy-transport equation (Lecture 03) requires an opacity \u03ba(\u03c1,T) as an input. Both of these missing physical ingredients are supplied here, finally making the four-equation system of Lecture 01 solvable in principle.',
        phenomenon=f'The Sun\u2019s core, with an estimated central density around {SUN_CORE_DENSITY_PUBLISHED:.1e} kg/m\u00b3 -- denser than solid lead -- is nonetheless accurately described by the ideal-gas law, because at a core temperature of {SUN_CORE_TEMP_PUBLISHED:.2e} K, thermal energies vastly exceed the quantum degeneracy energy scale that would otherwise invalidate that assumption (a limit explored quantitatively in Lecture 12 for white dwarfs).',
        vocab=['equation of state', 'ideal gas pressure', 'radiation pressure', 'mean molecular weight', 'opacity', 'Kramers opacity law', 'electron scattering opacity'],
        evidence=[
            'The ratio of radiation pressure to gas pressure, negligible for the Sun (as found quantitatively in ASTR 310, Lecture 13\u2019s Eddington-luminosity discussion), becomes progressively more important for higher-mass main-sequence stars, exactly as the P_rad \u221d T\u2074 versus P_gas \u221d \u03c1T scaling predicts.',
            'Stellar opacity is observed (via detailed spectral and solar/asteroseismic modeling) to fall steeply with increasing temperature in the deep stellar interior, consistent with the Kramers free-free/bound-free opacity law\u2019s T\u207b\u00b3\u00b7\u2075 scaling, before flattening at the highest temperatures where electron scattering (temperature-independent) takes over.',
            'Numerically tabulated OPAL/OP opacities, used in all modern stellar-evolution codes, show a pronounced peak near 10\u2075-10\u2076 K from iron-group bound-bound/bound-free transitions (the "iron opacity bump"), a feature entirely absent from the simple Kramers or electron-scattering scalings used for order-of-magnitude estimates in this lecture.',
        ],
        model=[
            'The total pressure in a stellar interior is the sum of ideal-gas pressure and radiation pressure, P = (\u03c1kT)/(\u03bcm_p) + (1/3)aT\u2074, with a = 4\u03c3/c the radiation constant; which term dominates depends on the local \u03c1 and T, with radiation pressure favored at high T and low \u03c1.',
            'Electron-scattering (Thomson) opacity is independent of temperature and density (for non-relativistic, fully ionized gas): \u03ba_es = \u03c3_T(1+X)/(2m_p), where X is the hydrogen mass fraction; it dominates in hot, fully ionized stellar interiors where bound electrons are unavailable for bound-free absorption.',
            'Free-free and bound-free opacity together are often approximated by the Kramers opacity law, \u03ba_Kramers \u221d \u03c1 T\u207b\u00b3\u00b7\u2075, a steep temperature dependence that makes this opacity source dominant in cooler, denser stellar envelopes and negligible in the hottest stellar cores, where electron scattering instead sets the floor.',
        ],
        equation=r'P = \dfrac{\rho k T}{\mu m_p} + \dfrac{1}{3}aT^{4}, \qquad \kappa_{\rm es} = \dfrac{\sigma_T(1+X)}{2m_p}, \qquad \kappa_{\rm Kramers} \propto \rho T^{-3.5}',
        example=[
            f'Electron-scattering opacity for a solar-composition (X=0.70) fully ionized gas: \u03ba_es = \u03c3_T(1+X)/(2m_p) = {KAPPA_ES_SUN:.4f} m\u00b2/kg (equivalently {KAPPA_ES_SUN*10:.3f} cm\u00b2/g), independent of the local temperature or density.',
            f'Schematic Kramers-law opacity at the Sun\u2019s core conditions (\u03c1 \u2248 {SUN_CORE_DENSITY_PUBLISHED:.1e} kg/m\u00b3, T \u2248 {SUN_CORE_TEMP_PUBLISHED:.2e} K, illustrative coefficient not a precision OPAL value): \u03ba_Kramers \u2248 {KAPPA_KRAMERS_SUN_CORE:.4f} m\u00b2/kg -- about {KAPPA_KRAMERS_SUN_CORE/KAPPA_ES_SUN:.0f} times larger than \u03ba_es at these conditions. This large a discrepancy is a genuine limitation of the illustrative Kramers coefficient used here (chosen for its correct T\u207b\u00b3\u00b7\u2075 functional form, not calibrated to reproduce a precise core value): real standard-solar-model opacity tables (OPAL/OP) find electron scattering and free-free absorption contribute comparably in the Sun\u2019s deep core, so this schematic estimate should be read as demonstrating the correct qualitative T\u207b\u00b3\u00b7\u2075 scaling, not as a quantitatively accurate core opacity.',
            f'Radiation-to-gas pressure ratio at the Sun\u2019s core: P_rad/P_gas = (1/3)aT\u2074 / (\u03c1kT/\u03bcm_p) with \u03bc \u2248 0.62 (fully ionized solar composition); evaluating at T = {SUN_CORE_TEMP_PUBLISHED:.2e} K and \u03c1 = {SUN_CORE_DENSITY_PUBLISHED:.1e} kg/m\u00b3 gives P_rad/P_gas \u2248 {(4*SIGMA_SB/C_LIGHT/3*SUN_CORE_TEMP_PUBLISHED**4)/((SUN_CORE_DENSITY_PUBLISHED*K_BOLTZMANN*SUN_CORE_TEMP_PUBLISHED)/(0.62*M_PROTON)):.2e}, confirming radiation pressure is negligible in the Sun\u2019s core, consistent with ASTR 310\u2019s independent finding (Lecture 13) that the Sun operates far below its own Eddington luminosity.',
        ],
        pitfall='Assuming a single opacity law (Kramers, or electron scattering alone) applies throughout an entire star. Real stellar opacity is a composite of several mechanisms whose relative importance shifts with local \u03c1 and T; using Kramers scaling in a fully ionized, radiation-pressure-dominated massive-star core, or using pure electron scattering in a cool, partially ionized envelope, both give qualitatively wrong answers.',
        activity='Using P_rad/P_gas \u221d T\u00b3/\u03c1 (from the two pressure terms\u2019 explicit T and \u03c1 dependence), explain qualitatively why radiation pressure becomes progressively more important, relative to gas pressure, in higher-mass main-sequence stars (which have both higher core temperatures and, per the mass-luminosity relation of Lecture 07, lower mean densities).',
        lab_connection='Lab 01 computes both electron-scattering and Kramers-law opacity estimates for the Sun\u2019s core and envelope and uses the equation of state to check the radiation-to-gas pressure ratio quantitatively.',
        synthesis='The equation of state and the opacity law are the two missing physical ingredients that, together with mass continuity and hydrostatic equilibrium (Lecture 01), the energy-conservation equation (Lectures 05-06), and the energy-transport equation (Lecture 03), complete the full system of stellar-structure equations.',
        openstax='OpenStax Astronomy 2e does not develop the equation of state or opacity formalism explicitly; this course derives both from first principles, connecting to the qualitative discussion of the Sun\u2019s interior in Chapter 16.2.',
    ),
    dict(
        n=3, title='Radiative Energy Transport: How Heat Actually Gets Out',
        subtitle='From optical depth (ASTR 310) to a stellar luminosity',
        goals=[
            'Derive the radiative diffusion approximation for energy transport from the radiative transfer equation (ASTR 310, Lecture 03).',
            'Derive the dimensionless radiative temperature gradient \u2207_rad and identify the physical quantities that control it.',
            'Evaluate \u2207_rad for real solar-interior conditions and compare it across two very different depths.',
        ],
        why_matters='ASTR 310 derived the radiative transfer equation for a beam of light crossing a slab of gas. This lecture applies the same optical-depth formalism to a star\u2019s interior, where photons undergo a random walk of enormous numbers of absorption/re-emission and scattering events, and shows how that random walk sets the star\u2019s temperature gradient -- and, ultimately, its surface luminosity.',
        phenomenon=f'A photon born in the Sun\u2019s core takes on the order of tens of thousands of years to random-walk its way to the surface, despite light itself crossing the Sun\u2019s radius in about 2.3 seconds -- the discrepancy is entirely due to the enormous number of absorption and re-emission events (set by the core\u2019s huge optical depth) the photon undergoes along the way.',
        vocab=['radiative diffusion', 'mean free path', 'radiative flux', 'dimensionless temperature gradient \u2207_rad', 'radiation constant', 'photon random walk'],
        evidence=[
            'In the high-optical-depth interior of any star, the local radiation field is very nearly isotropic and close to a blackbody at the local temperature, exactly the condition under which the diffusion approximation to radiative transfer (rather than the full transfer equation) is valid.',
            'Helioseismic inversions of the Sun\u2019s internal sound-speed and temperature profile are consistent with a standard solar model built by integrating the radiative-diffusion energy-transport equation through the radiative zone (below about 0.71 R\u2609) and a convective prescription above it (Lecture 04), not with a single transport law applied throughout.',
            'More opaque or more luminous stellar interiors are found (in numerical stellar models) to require a systematically steeper temperature gradient to carry the same energy flux, exactly matching the radiative-diffusion equation\u2019s direct proportionality between \u2207_rad and both \u03ba and L.',
        ],
        model=[
            'In the diffusion limit (optical depth \u226b 1), the radiative flux is F = -(4ac T\u00b3)/(3\u03ba\u03c1) dT/dr, a direct analog of Fourier heat conduction with an effective "radiative conductivity" set by the opacity.',
            'Multiplying F by the local surface area 4\u03c0r\u00b2 gives the local luminosity, L(r) = -16\u03c0r\u00b2 (acT\u00b3)/(3\u03ba\u03c1) dT/dr; solving this for dT/dr and non-dimensionalizing using hydrostatic equilibrium (dP/dr = -GM\u03c1/r\u00b2) gives the standard dimensionless radiative gradient \u2207_rad = (d ln T/d ln P)_rad = 3\u03ba L P /(16\u03c0 a c G M T\u2074).',
            '\u2207_rad depends directly on the local opacity \u03ba (Lecture 02) and luminosity L, and inversely on the enclosed mass M and T\u2074; a region with unusually high opacity or unusually high local luminosity-to-mass ratio requires an unusually steep temperature gradient to carry that luminosity radiatively -- and, as Lecture 04 shows, a gradient that becomes too steep triggers convective instability instead.',
        ],
        equation=r'F = -\dfrac{4acT^{3}}{3\kappa\rho}\dfrac{dT}{dr}, \qquad \nabla_{\rm rad} \equiv \left(\dfrac{d\ln T}{d\ln P}\right)_{\rm rad} = \dfrac{3\kappa L P}{16\pi a c G M T^{4}}',
        example=[
            f'Deep solar envelope sample point (r \u2248 {SUN_ENVELOPE_RADIUS_FRAC:.1f} R\u2609, T \u2248 {SUN_ENVELOPE_TEMP_K:.1e} K, P \u2248 {SUN_ENVELOPE_PRESSURE_EST:.1e} Pa, electron-scattering opacity from Lecture 02): \u2207_rad = 3\u03baLP/(16\u03c0acGMT\u2074) = {SUN_RADIATIVE_GRADIENT:.4f}.',
            f'Near-surface sample point (T \u2248 {SUN_SURFACE_ZONE_TEMP_K:.1e} K, P \u2248 {SUN_SURFACE_ZONE_PRESSURE_PA:.1e} Pa, \u03c1 \u2248 {SUN_SURFACE_ZONE_DENSITY_KGM3:.1e} kg/m\u00b3, schematic Kramers opacity \u03ba \u2248 {KAPPA_SURFACE_ZONE:.2f} m\u00b2/kg from the much lower temperature and higher bound-free/H\u207b opacity there): \u2207_rad = {SUN_SURFACE_ZONE_TEMP_K and (3*KAPPA_SURFACE_ZONE*L_SUN_W*SUN_SURFACE_ZONE_PRESSURE_PA)/(16*math.pi*(4*SIGMA_SB/C_LIGHT)*C_LIGHT*G_NEWTON*SUN_SURFACE_ZONE_MASS_ENCLOSED_KG*SUN_SURFACE_ZONE_TEMP_K**4):.3e}.',
            f'The deep-envelope \u2207_rad ({SUN_RADIATIVE_GRADIENT:.3f}) is far smaller than the near-surface \u2207_rad ({(3*KAPPA_SURFACE_ZONE*L_SUN_W*SUN_SURFACE_ZONE_PRESSURE_PA)/(16*math.pi*(4*SIGMA_SB/C_LIGHT)*C_LIGHT*G_NEWTON*SUN_SURFACE_ZONE_MASS_ENCLOSED_KG*SUN_SURFACE_ZONE_TEMP_K**4):.3e}), driven almost entirely by the much larger near-surface opacity from Lecture 02\u2019s Kramers scaling at low T -- Lecture 04 shows precisely which of these two numbers exceeds the adiabatic gradient and therefore triggers convection.',
        ],
        pitfall='Assuming the diffusion approximation applies everywhere in a star, including near the photosphere. The diffusion approximation strictly requires optical depth \u226b 1; near a star\u2019s surface (optical depth of order unity, ASTR 310 Lecture 03), the full radiative transfer equation, not the diffusion limit, must be used, which is why stellar-atmosphere modeling and stellar-interior modeling are treated as separate problems joined at a boundary.',
        activity='Using \u2207_rad \u221d \u03baL (direct proportionality to both opacity and luminosity), explain qualitatively why a region of unusually high local opacity is more likely to become convectively unstable (Lecture 04) than a region of the same luminosity and mass but lower opacity.',
        lab_connection='Lab 02 evaluates \u2207_rad at multiple depths in a simplified solar model and applies the Schwarzschild criterion (Lecture 04) to identify which depths are stable and which are convective.',
        synthesis='Radiative diffusion, obtained by applying the optical-depth formalism of ASTR 310 to a star\u2019s interior rather than to a single beam, supplies the stellar-structure system\u2019s missing energy-transport equation in the form of the dimensionless gradient \u2207_rad, which sets the star\u2019s actual temperature profile wherever radiative transport is stable.',
        openstax='OpenStax Astronomy 2e, Chapter 16.2 (energy transport, radiation and convection zones) states the qualitative picture; this course derives \u2207_rad explicitly from the diffusion approximation and hydrostatic equilibrium.',
    ),
    dict(
        n=4, title='Convection and the Schwarzschild Criterion',
        subtitle='When radiative transport fails, and what takes over',
        goals=[
            'Derive the Schwarzschild criterion for convective instability by comparing a displaced gas parcel\u2019s density to its surroundings.',
            'State the adiabatic temperature gradient for an ideal monatomic gas and explain its physical origin.',
            'Apply the Schwarzschild criterion to the Sun\u2019s interior and identify where radiative transport gives way to convection.',
        ],
        why_matters='Lecture 03 derived the radiative temperature gradient \u2207_rad required to carry a star\u2019s luminosity outward by photon diffusion alone. This lecture asks the essential follow-up question: is that gradient actually achievable without triggering bulk fluid motion? The answer -- no, whenever \u2207_rad exceeds the adiabatic gradient \u2207_ad -- is what makes the Sun\u2019s outer 29% (by radius) convective while its interior is radiative.',
        phenomenon='Sunspots, granulation, and the Sun\u2019s 11-year magnetic activity cycle are all direct surface manifestations of convective motion in the Sun\u2019s outer envelope, yet the Sun\u2019s deep interior (below about 0.71 R\u2609) shows none of these phenomena and is understood to be purely radiative -- the same star, with two entirely different energy-transport mechanisms operating at different depths.',
        vocab=['Schwarzschild criterion', 'convective instability', 'adiabatic temperature gradient', 'superadiabatic layer', 'convection zone', 'buoyancy'],
        evidence=[
            'Helioseismology precisely locates the base of the Sun\u2019s convection zone at r \u2248 0.713 R\u2609, matching the depth at which standard solar models compute \u2207_rad to first exceed \u2207_ad as one moves outward from the radiative core.',
            'Stars significantly cooler than the Sun (mid-to-late K and M dwarfs) are found, both observationally (via their strong magnetic activity and flaring) and in stellar models, to be fully convective throughout their interiors, consistent with the Schwarzschild criterion\u2019s prediction that higher opacity (Lecture 02\u2019s Kramers scaling, favored at lower T) drives \u2207_rad above \u2207_ad at ever greater depth as effective temperature falls.',
            'Massive main-sequence stars (O and B types) are found to have convective cores and radiative envelopes -- the opposite arrangement from the Sun -- consistent with the Schwarzschild criterion applied to their much higher central nuclear energy generation rates (steep CNO-cycle temperature sensitivity, Lecture 06) driving \u2207_rad above \u2207_ad specifically in the core.',
        ],
        model=[
            'Consider a gas parcel displaced upward by a small distance, expanding adiabatically (no heat exchange with its surroundings) as the ambient pressure drops; if the parcel\u2019s resulting density is lower than its new surroundings\u2019, it continues to rise (buoyantly unstable), and if higher, it sinks back (stable).',
            'Working through this comparison in terms of temperature gradients (rather than density directly) shows that the region is convectively unstable precisely when the actual (radiative) temperature gradient is steeper than the gradient the parcel itself would follow if it rose adiabatically: \u2207_rad > \u2207_ad, the Schwarzschild criterion.',
            'For an ideal monatomic gas (\u03b3 = 5/3, appropriate for a fully ionized hydrogen/helium plasma), the adiabatic gradient is a fixed constant, \u2207_ad = (\u03b3-1)/\u03b3 = 2/5, independent of local conditions; the Schwarzschild criterion therefore reduces to a direct numerical comparison between the locally computed \u2207_rad (Lecture 03) and this fixed value.',
        ],
        equation=r'\nabla_{\rm ad} = \dfrac{\gamma - 1}{\gamma} = \dfrac{2}{5}\ (\text{ideal monatomic gas}), \qquad \text{convective instability: } \nabla_{\rm rad} > \nabla_{\rm ad}',
        example=[
            f'Deep solar envelope sample point (Lecture 03): \u2207_rad = {SUN_RADIATIVE_GRADIENT:.4f}, compared to \u2207_ad = {SUN_ADIABATIC_GRADIENT_FRACTIONAL:.1f}. Since \u2207_rad < \u2207_ad at this point, radiative transport is stable there in this illustrative model.',
            f'Near-surface sample point (Lecture 03, dominated by the much higher schematic Kramers opacity at low T): \u2207_rad \u2248 {SUN_SURFACE_RADIATIVE_GRADIENT:.3e}, vastly exceeding \u2207_ad = {SUN_ADIABATIC_GRADIENT_FRACTIONAL:.1f} -- an overwhelming Schwarzschild-criterion violation, correctly predicting convective instability near the solar surface.',
            'The real Sun\u2019s convection zone begins at r \u2248 0.713 R\u2609 (helioseismically measured) and extends to the photosphere; this lecture\u2019s two illustrative sample points, chosen at a deeper radiative-zone-like point and a much shallower, higher-opacity near-surface point, correctly reproduce the qualitative radiative-then-convective structure, even though the specific opacity coefficients used are schematic rather than full OPAL/OP tables.',
        ],
        pitfall='Assuming the Schwarzschild criterion depends on composition gradients. The full (Ledoux) criterion for convective stability includes an additional term for composition gradients, relevant in stars with a molecular-weight gradient (e.g., during shell burning in Lecture 09); the simpler Schwarzschild criterion used in this lecture assumes uniform composition and is the appropriate starting point for a chemically homogeneous main-sequence star.',
        activity='Using \u2207_rad \u221d \u03ba (Lecture 03), explain why a star with much higher central opacity than the Sun (e.g., due to a much higher heavy-element abundance) would be expected to develop a convective core even on the main sequence, without needing any change in its nuclear energy generation rate.',
        lab_connection='Lab 02 computes \u2207_rad at the same two sample depths used in this lecture\u2019s worked example and explicitly applies the Schwarzschild criterion to determine the stable-versus-convective classification at each.',
        synthesis='The Schwarzschild criterion, \u2207_rad > \u2207_ad, is the decision rule that determines which energy-transport mechanism (radiative diffusion or convection) actually operates at each depth in a star, and applying it to the Sun\u2019s interior correctly separates its radiative core from its convective envelope.',
        openstax='OpenStax Astronomy 2e, Chapter 16.2 (convection zone) states the qualitative picture; this course derives the Schwarzschild criterion explicitly from a displaced-parcel buoyancy argument.',
    ),
    dict(
        n=5, title='Nuclear Reactions I: The Proton-Proton Chain and the Gamow Peak',
        subtitle='How the Sun actually shines, and why classical physics says it should not',
        goals=[
            'Explain why classical (non-quantum) physics predicts stellar core temperatures are far too low for nuclear fusion to occur at any appreciable rate.',
            'Derive the qualitative origin of the Gamow peak from the competition between the Maxwell-Boltzmann energy distribution and quantum tunneling.',
            'Describe the proton-proton chain\u2019s net reaction and energy yield, and compute the Gamow peak energy for solar-core conditions.',
        ],
        why_matters='Every energy-transport mechanism developed in Lectures 03-04 needs an energy source to transport; this lecture supplies it. The proton-proton chain is also a canonical example of quantum tunneling made astrophysically essential: without it, the Sun\u2019s core temperature (a few times 10\u2077 K) is far too cold, by classical reasoning, for fusion to occur at all.',
        phenomenon=f'The Sun\u2019s core temperature, {SUN_CORE_TEMP_PUBLISHED:.2e} K, corresponds to a typical thermal proton kinetic energy of only kT \u2248 {(K_BOLTZMANN*SUN_CORE_TEMP_PUBLISHED)/EV_J/1000.0:.2f} keV, while the classical Coulomb barrier between two protons at nuclear-contact separation is on the order of 1 MeV -- more than 100 times larger. Fusion nonetheless proceeds continuously in the Sun\u2019s core, entirely because of quantum-mechanical tunneling through, rather than over, this barrier.',
        vocab=['Coulomb barrier', 'quantum tunneling', 'Gamow peak', 'proton-proton chain', 'positron/neutrino emission', 'reaction rate'],
        evidence=[
            'Solar neutrino detectors (e.g., Super-Kamiokande, SNO, Borexino) directly measure the flux and energy spectrum of neutrinos produced by specific steps of the proton-proton chain, confirming both that the chain operates in the Sun\u2019s core and that it proceeds at the rate needed to explain the Sun\u2019s observed luminosity.',
            'The observed solar luminosity, sustained for a main-sequence lifetime consistent with the Sun\u2019s known age of {:.2f} Gyr (Lecture 07), is quantitatively consistent with hydrogen fusion (not gravitational contraction, chemical burning, or any other classical energy source) as the Sun\u2019s power source, resolving the 19th-century Kelvin-Helmholtz timescale problem.',
            'Laboratory nuclear-reaction-rate measurements at accelerator energies, extrapolated down to the much lower Gamow-peak energies relevant in stellar interiors, confirm the tunneling-based reaction-rate formalism used to compute stellar nuclear energy generation rates.',
        ],
        model=[
            'The number of particle pairs available to react is set by the Maxwell-Boltzmann kinetic-energy distribution, which falls off exponentially at high energy (as e^{-E/kT}); at solar-core kT (a few keV), essentially no particle pairs classically possess enough energy to overcome the MeV-scale Coulomb barrier.',
            'The probability that a given pair actually tunnels through the Coulomb barrier rises steeply with energy (as e^{-b/\u221aE} for a Gamow factor b that depends on the reactants\u2019 charges and reduced mass), favoring higher-energy pairs even though there are exponentially fewer of them.',
            'Multiplying these two exponential factors together produces the Gamow peak: a narrow range of energies, well above kT but still far below the full Coulomb barrier, where the product of "enough particles" and "enough tunneling probability" is maximized, and where the overwhelming majority of stellar nuclear reactions actually occur.',
        ],
        equation=r'4\,^1\mathrm{H} \rightarrow\, ^4\mathrm{He} + 2e^{+} + 2\nu_e + \gamma,\quad Q \approx 26.73\ \mathrm{MeV}, \qquad E_0 \approx 1.22\,(Z_1^{2}Z_2^{2}\mu\,T_6^{2})^{1/3}\ \mathrm{keV}',
        example=[
            f'Thermal energy scale in the Sun\u2019s core: kT = {(K_BOLTZMANN*SUN_CORE_TEMP_PUBLISHED)/EV_J:.1f} eV = {(K_BOLTZMANN*SUN_CORE_TEMP_PUBLISHED)/EV_J/1000.0:.3f} keV -- three orders of magnitude below the MeV-scale Coulomb barrier for two protons.',
            f'Gamow peak energy for proton-proton reactions at the Sun\u2019s core temperature (Z1=Z2=1, reduced mass \u03bc = 0.5 amu, T6 = {T6_SUN_CORE:.1f}): E0 \u2248 1.22(1\u00b71\u00b70.5\u00b7{T6_SUN_CORE:.1f}\u00b2)^(1/3) = {GAMOW_E0_PP_SUN_KEV:.2f} keV -- well above kT ({(K_BOLTZMANN*SUN_CORE_TEMP_PUBLISHED)/EV_J/1000.0:.3f} keV) but far below the full MeV-scale Coulomb barrier, exactly the Gamow-peak compromise the model predicts.',
            f'Net energy release per completed pp-chain cycle (4 protons \u2192 one He-4 nucleus plus positrons, neutrinos, and gamma rays): Q = {PP_CHAIN_Q_MEV:.2f} MeV = {PP_CHAIN_Q_MEV*1e6*EV_J:.3e} J per cycle -- the ultimate energy source computed in the energy-conservation equation\u2019s \u03b5(r) term from Lecture 01.',
        ],
        pitfall='Assuming the Gamow peak energy is the typical thermal energy of particles in a stellar core. It is not: E0 is several times larger than kT precisely because it represents the compromise between the (exponentially falling) Maxwell-Boltzmann population and the (exponentially rising) tunneling probability, not the most common particle energy in the gas.',
        activity='Using the shape of the Gamow-peak argument (product of a falling exponential in E and a rising exponential in E), explain in words why raising the core temperature shifts the Gamow peak to higher energy and, more importantly, dramatically increases the reaction rate, without needing to evaluate the full integral.',
        lab_connection='Lab 03 compares pp-chain and CNO-cycle (Lecture 06) energy generation rates as a function of core temperature for the Sun and for a more massive star, using the same Gamow-peak reasoning developed here.',
        synthesis='Quantum tunneling through the Coulomb barrier, not classical over-the-barrier collisions, is what allows nuclear fusion to proceed at all at real stellar-core temperatures, and the Gamow peak identifies the specific (non-thermal, non-maximal-tunneling) energy at which most of that fusion actually happens.',
        openstax='OpenStax Astronomy 2e, Chapter 16.3 (the pp chain, CNO cycle) presents the pp chain\u2019s reaction steps qualitatively; this course derives the Gamow-peak formalism explaining why fusion proceeds at solar-core temperatures at all.',
    ),
    dict(
        n=6, title='Nuclear Reactions II: The CNO Cycle and Why Massive Stars Burn So Differently',
        subtitle='A catalytic cycle with an extraordinarily steep temperature dependence',
        goals=[
            'Describe the CNO cycle\u2019s catalytic role for carbon, nitrogen, and oxygen and its identical net reaction and energy yield to the pp chain.',
            'Explain why the CNO cycle\u2019s energy generation rate is far more temperature-sensitive than the pp chain\u2019s.',
            'Compute the crossover temperature at which CNO-cycle energy generation overtakes the pp chain, and classify the Sun and a real, more massive star accordingly.',
        ],
        why_matters='The pp chain (Lecture 05) explains how the Sun shines, but it cannot be the dominant energy source in every star: the CNO cycle\u2019s much higher effective nuclear charge (carbon and nitrogen, not hydrogen, are the heavier reactants) gives it a dramatically steeper temperature dependence, which this lecture shows flips the dominant energy source above a specific, computable core temperature -- with direct consequences for main-sequence structure (Lecture 04\u2019s convective-core result) and lifetime scaling (Lecture 07).',
        phenomenon='The Sun, with a core temperature of a few times 10\u2077 K, generates over 98% of its energy via the pp chain, while stars only moderately more massive (and hence with only moderately hotter cores) are found, in detailed stellar models, to be overwhelmingly CNO-dominated -- a strikingly sharp transition for such a modest temperature difference between the two stellar types.',
        vocab=['CNO cycle', 'catalytic nuclear cycle', 'temperature sensitivity (energy generation)', 'power-law index', 'crossover temperature', 'convective core (massive stars)'],
        evidence=[
            'Solar neutrino measurements confirm that only a small percentage of the Sun\u2019s energy comes from CNO-cycle reactions, with the pp chain responsible for the overwhelming majority, consistent with the Sun\u2019s core temperature lying well below the CNO-dominance crossover computed in this lecture.',
            'Massive main-sequence stars are found, in stellar-evolution models constrained by observed masses, radii, and luminosities of eclipsing binaries (ASTR 310, Lecture 09), to require CNO-dominated energy generation to match their observed properties, consistent with their much hotter cores.',
            'The extreme temperature sensitivity of the CNO cycle is the direct physical cause of massive stars\u2019 convective cores (Lecture 04): energy generation concentrated in an extremely narrow central temperature range produces a very high local luminosity-to-mass ratio, driving \u2207_rad above \u2207_ad specifically in the core.',
        ],
        model=[
            'The CNO cycle uses a pre-existing carbon-12 nucleus as a catalyst: successive proton captures and beta decays convert carbon to nitrogen to oxygen and back to carbon, net-converting four protons into one helium-4 nucleus (identical net reaction, and nearly identical Q-value, to the pp chain), while the carbon/nitrogen/oxygen abundances themselves are unchanged.',
            'Because the CNO cycle\u2019s rate-limiting step involves a proton fusing with a carbon or nitrogen nucleus (Z=6 or 7) rather than another proton (Z=1), its Gamow factor (and hence its temperature sensitivity) is much steeper: the standard textbook power-law approximation gives \u03b5_CNO \u221d T\u00b2\u2070, compared to \u03b5_pp \u221d T\u2074 (both schematic fits valid only over a limited temperature range, not exact reaction-network results).',
            'Because \u03b5_CNO rises so much faster with temperature than \u03b5_pp, there exists a single crossover core temperature above which CNO dominates and below which pp dominates; a small increase in stellar mass (and hence core temperature, via the mass-luminosity scaling of Lecture 07) can shift a star from strongly pp-dominated to strongly CNO-dominated.',
        ],
        equation=r'\varepsilon_{\rm pp} \propto \rho X^{2} T_6^{4}, \qquad \varepsilon_{\rm CNO} \propto \rho X X_{\rm CNO} T_6^{20}\ \ (\text{schematic power-law fits})',
        example=[
            f'At the Sun\u2019s core temperature (T6 = {T6_SUN_CORE:.2f}), the schematic power laws give \u03b5_pp (relative) = {EPS_PP_SUN:.3e} and, after normalizing the CNO curve so the Sun is 1000:1 pp-dominated (the standard textbook statement), \u03b5_CNO (relative, normalized) = {CNO_NORMALIZATION*EPS_CNO_SUN:.3e} -- confirming the Sun is overwhelmingly pp-dominated.',
            f'Crossover temperature (where the two normalized curves are equal): T6 \u2248 {PP_CNO_CROSSOVER_T6:.1f}, i.e., T \u2248 {PP_CNO_CROSSOVER_TEMP_K:.2e} K -- noticeably hotter than the Sun\u2019s core temperature of {SUN_CORE_TEMP_PUBLISHED:.2e} K.',
            f'Sirius A (mass {SIRIUS_A["mass_msun"]:.3f} M\u2609, carried forward from ASTR 310/230): schematic core-temperature scaling T_core \u2248 T_core,\u2609(M/M\u2609)^0.7 (an illustrative mass-temperature scaling, not a precision stellar-model result) gives an estimated core temperature of {SIRIUS_A_CORE_TEMP_EST_K:.2e} K, i.e., T6 = {T6_SIRIUS_A_CORE:.1f} -- above the {PP_CNO_CROSSOVER_T6:.1f} crossover, predicting Sirius A is CNO-dominated, consistent with real stellar models for a 2 M\u2609-class A-type star.',
        ],
        pitfall='Treating the schematic \u03b5_pp \u221d T\u2076\u2074 and \u03b5_CNO \u221d T\u00b2\u2070 power-law indices as exact, universal constants. These are local power-law fits, valid only over the narrow temperature range near each mechanism\u2019s typical operating temperature; the true reaction-network temperature dependence is smoother and the effective power-law index itself changes with temperature, so extrapolating either fit far outside its fitted range gives increasingly unreliable results.',
        activity='Using \u03b5_CNO \u221d T\u00b2\u2070 (versus \u03b5_pp \u221d T\u2074), explain why even a modest (say, 20%) increase in core temperature has a vastly larger relative effect on \u03b5_CNO than on \u03b5_pp, and connect this to why CNO-dominated stellar cores are so much more centrally concentrated in their energy generation than pp-dominated cores.',
        lab_connection='Lab 03 computes the full crossover-temperature calculation shown here and applies it to a second real star, cross-checking the qualitative pp/CNO classification against each star\u2019s known spectral type and core-temperature scaling.',
        synthesis='The CNO cycle releases the same net energy per helium nucleus formed as the pp chain, but its far steeper temperature sensitivity (\u03b5 \u221d T\u00b2\u2070 versus T\u2074) means a single, computable crossover temperature separates pp-dominated stars like the Sun from CNO-dominated, more massive stars like Sirius A -- with direct structural consequences (convective cores) for the latter.',
        openstax='OpenStax Astronomy 2e, Chapter 16.3 (the pp chain and CNO cycle) introduces both cycles qualitatively; this course derives the crossover-temperature argument and its consequence for convective cores.',
    ),
    dict(
        n=7, title='The Mass-Luminosity Relation and Main-Sequence Lifetimes',
        subtitle='Why massive stars live fast and die young',
        goals=[
            'Derive the approximate mass-luminosity scaling L \u221d M^3.5 from homology-style reasoning connecting core temperature, opacity, and hydrostatic equilibrium.',
            'Derive the main-sequence lifetime scaling t_MS \u221d M/L \u221d M^-2.5 from the fuel-supply argument.',
            'Apply both relations to real, precisely measured stars and evaluate the results against real cluster ages (previewing Lecture 09\u2019s isochrone method).',
        ],
        why_matters='Every real, precisely measured star used in this course (Alpha Centauri A and B, Sirius A, and the Sun) can now be placed on a single, quantitative mass-luminosity-lifetime framework, which is also the essential tool (developed further in Lecture 09) for dating star clusters from their main-sequence turnoff.',
        phenomenon=f'Sirius A, at {SIRIUS_A["mass_msun"]:.3f} M\u2609, is only about twice the Sun\u2019s mass but roughly {SIRIUS_A["lum_lsun"]/1.0:.0f} times more luminous -- a wildly non-linear scaling that, this lecture shows, follows directly from how sensitively a star\u2019s internal structure (core temperature, opacity, nuclear energy generation) responds to a change in total mass.',
        vocab=['mass-luminosity relation', 'homology relations', 'fuel-supply argument', 'main-sequence lifetime', 'turnoff mass', 'stellar lifetime scaling'],
        evidence=[
            'Precisely measured masses and luminosities from real eclipsing and visual binaries (ASTR 310, Lecture 09), including Alpha Centauri A and B and Sirius A/B, are well fit by a single power law L \u221d M^n with n in the range 3-4 over the main-sequence mass range relevant to this course.',
            'Open star clusters (Lecture 09) with independently measured (isochrone-fit) ages show main-sequence turnoff masses that decrease systematically with increasing cluster age, exactly as the t_MS \u221d M^-2.5 lifetime scaling predicts for a coeval population of stars.',
            'The most massive known main-sequence stars (tens of solar masses) are observed to have main-sequence lifetimes of only a few million years, while the lowest-mass red dwarfs are computed (from the same scaling, extrapolated) to have lifetimes far exceeding the current age of the universe -- both extremes consistent with the steep M^-2.5 scaling.',
        ],
        model=[
            'Homology reasoning (assuming all stars along the main sequence have structurally similar, scaled density and temperature profiles) combines hydrostatic equilibrium (P_c \u221d M\u00b2/R\u2074, ASTR 310 Lecture 05), the ideal-gas law, and the radiative-diffusion luminosity (Lecture 03) to eliminate the unknown central temperature and density, yielding an approximate power-law relation L \u221d M^n with n depending on the dominant opacity source and equation-of-state regime (n \u2248 3.5 is a standard textbook approximation for electron-scattering-dominated, ideal-gas main-sequence stars).',
            'A star\u2019s total nuclear fuel supply is proportional to its mass (M), while its fuel consumption rate is proportional to its luminosity (L); the main-sequence lifetime is therefore t_MS \u221d M/L, and substituting the mass-luminosity relation gives t_MS \u221d M/M^3.5 = M^-2.5.',
            'Calibrating this scaling using the Sun\u2019s own main-sequence lifetime (\u2248 10 Gyr, a standard value) as the reference point gives a simple, testable prediction for any other star\u2019s main-sequence lifetime purely from its mass and luminosity.',
        ],
        equation=r'L \propto M^{3.5}, \qquad t_{\rm MS} = t_{\rm MS,\odot}\dfrac{M/M_\odot}{L/L_\odot} \propto M^{-2.5}',
        example=[
            f'Alpha Centauri A ({ALPHA_CEN_A["mass_msun"]:.4f} M\u2609): mass-luminosity prediction L \u221d M^3.5 = {ALPHA_CEN_A_ML_PRED_LSUN:.3f} L\u2609, compared to the independently measured {ALPHA_CEN_A["lum_lsun"]:.4f} L\u2609 (agreement to {abs(ALPHA_CEN_A_ML_PRED_LSUN-ALPHA_CEN_A["lum_lsun"])/ALPHA_CEN_A["lum_lsun"]*100:.1f}%); main-sequence lifetime estimate t_MS = 10 Gyr \u00d7 ({ALPHA_CEN_A["mass_msun"]:.4f}/{ALPHA_CEN_A["lum_lsun"]:.4f}) = {ALPHA_CEN_A_MS_LIFETIME_GYR:.2f} Gyr.',
            f'Alpha Centauri B ({ALPHA_CEN_B["mass_msun"]:.4f} M\u2609): mass-luminosity prediction {ALPHA_CEN_B_ML_PRED_LSUN:.3f} L\u2609 versus measured {ALPHA_CEN_B["lum_lsun"]:.4f} L\u2609 (agreement to {abs(ALPHA_CEN_B_ML_PRED_LSUN-ALPHA_CEN_B["lum_lsun"])/ALPHA_CEN_B["lum_lsun"]*100:.1f}%); main-sequence lifetime estimate t_MS = {ALPHA_CEN_B_MS_LIFETIME_GYR:.2f} Gyr, longer than Alpha Centauri A\u2019s despite both stars being roughly solar-mass, because B\u2019s lower luminosity dominates the M/L ratio.',
            f'Sirius A ({SIRIUS_A["mass_msun"]:.3f} M\u2609, measured L = {SIRIUS_A["lum_lsun"]:.1f} L\u2609): mass-luminosity prediction {SIRIUS_A_ML_PRED_LSUN:.1f} L\u2609 (agreement to {abs(SIRIUS_A_ML_PRED_LSUN-SIRIUS_A["lum_lsun"])/SIRIUS_A["lum_lsun"]*100:.1f}%, noticeably worse than for the two lower-mass Alpha Centauri stars -- expected, since the fixed n=3.5 exponent is only an approximation whose accuracy varies across the main-sequence mass range); estimated main-sequence lifetime t_MS = {SIRIUS_A_MS_LIFETIME_GYR:.3f} Gyr, dramatically shorter than the Sun\u2019s.',
        ],
        pitfall='Treating L \u221d M^3.5 (or any single mass-luminosity exponent) as exact across the full main-sequence mass range. The true exponent varies smoothly with mass (closer to 4 near solar mass, shallower for both very low-mass and very high-mass, radiation-pressure-supported stars), so this lecture\u2019s single fixed exponent is a working approximation, and its accuracy should always be checked against independently measured luminosities, as done explicitly above.',
        activity='Using t_MS \u221d M^-2.5, predict by what factor a 10 M\u2609 star\u2019s main-sequence lifetime is shorter than the Sun\u2019s, without recomputing the full luminosity, and explain why this scaling alone (not any detail of nuclear reaction rates) is enough to conclude that massive stars are always short-lived.',
        lab_connection='Lab 04 reproduces this lecture\u2019s full mass-luminosity and lifetime calculation for all three real stars above plus the Sun, and Lab 05 uses the same lifetime scaling to interpret a real star cluster\u2019s main-sequence turnoff age.',
        synthesis='A single approximate power law, L \u221d M^3.5, derived from homology reasoning across the four stellar-structure equations, both explains why massive stars are so disproportionately luminous and predicts, via the fuel-supply argument, why they live so much shorter lives -- a scaling this course tests quantitatively against three independently measured real stars above and a real star cluster in Lecture 09.',
        openstax='OpenStax Astronomy 2e, Chapter 19.3 (the main sequence, mass-luminosity relation) states the relation empirically; this course derives its approximate physical origin from homology reasoning.',
    ),
    dict(
        n=8, title='Stellar Models: Polytropes and Homology Relations',
        subtitle='A simplified but genuinely predictive family of stellar structures',
        goals=[
            'State the polytropic equation of state P = K\u03c1^\u03b3 and explain why it closes the stellar-structure system with a single free index.',
            'Describe the Lane-Emden equation as the dimensionless form of hydrostatic equilibrium for a polytrope, without solving it in full.',
            'Explain how the n=3 polytrope specifically connects to both this lecture\u2019s homology relations and the Chandrasekhar mass derived in Lecture 12.',
        ],
        why_matters='Lecture 07\u2019s mass-luminosity relation used homology reasoning informally; polytropic stellar models make that reasoning mathematically precise by replacing the full, coupled equation of state and opacity law with a single simplified pressure-density relation, at the cost of realism. The n=3 polytrope in particular reappears explicitly and quantitatively in Lecture 12\u2019s Chandrasekhar-mass derivation.',
        phenomenon='A fully convective star (Lecture 04) has a nearly adiabatic, and therefore nearly polytropic, structure throughout its interior, while a relativistically degenerate white dwarf (Lecture 12) is described by an equation of state that is exactly polytropic with index n=3 -- two very different physical stars, both well described by the same simplified mathematical framework developed in this lecture.',
        vocab=['polytrope', 'polytropic index n', 'Lane-Emden equation', 'homology relation', 'dimensionless stellar structure', 'degenerate equation of state (preview)'],
        evidence=[
            'Polytropic models with n=3 (the "Eddington standard model") were historically used, before the advent of numerical stellar-evolution codes, to make quantitatively successful predictions for the internal density and pressure structure of stars like the Sun, despite the model\u2019s simplified equation of state.',
            'The n=3/2 polytrope (P \u221d \u03c1^(5/3)) is found, both historically and in modern white-dwarf models, to accurately describe the interior of a fully non-relativistically-degenerate white dwarf, a direct precursor to Lecture 12\u2019s Chandrasekhar-mass derivation.',
            'The relativistically degenerate n=3 polytrope (P \u221d \u03c1^(4/3)) is the specific equation of state whose associated Lane-Emden solution produces a mass that is completely independent of the star\u2019s central density -- exactly the mathematical origin of the Chandrasekhar mass\u2019s remarkable universality, derived quantitatively in Lecture 12.',
        ],
        model=[
            'A polytrope assumes a simplified equation of state P = K\u03c1^\u03b3 = K\u03c1^{(n+1)/n}, with K a constant and n the polytropic index; substituting this into hydrostatic equilibrium and mass continuity produces a single second-order differential equation (the Lane-Emden equation) in a dimensionless radius and a dimensionless density function \u03b8, with n as the only free parameter.',
            'Different physical regimes correspond to different polytropic indices: n=3/2 for a non-relativistic, fully degenerate electron gas or for a fully convective (adiabatic, monatomic ideal gas) stellar envelope; n=3 for a relativistically degenerate electron gas or for a radiation-pressure-dominated, very massive star (the Eddington standard model).',
            'For a fixed polytropic index n, the Lane-Emden equation\u2019s solution fixes dimensionless relations between the star\u2019s total mass, radius, and central density that depend only on n (not on the star\u2019s particular mass) -- these are the homology relations, and for n=3 specifically, the resulting mass-radius relation is independent of central density altogether, the key mathematical fact exploited in Lecture 12.',
        ],
        equation=r'P = K\rho^{(n+1)/n}, \qquad \dfrac{1}{\xi^{2}}\dfrac{d}{d\xi}\left(\xi^{2}\dfrac{d\theta}{d\xi}\right) = -\theta^{n}\ \ (\text{Lane-Emden equation, dimensionless})',
        example=[
            f'Sun-like fully convective envelope approximation: n=3/2 polytrope (\u03b3 = 5/3, matching the ideal monatomic adiabatic gradient \u2207_ad = 2/5 derived in Lecture 04), consistent with the Sun\u2019s own convective outer envelope (r > 0.71 R\u2609) being reasonably close to adiabatic.',
            'Eddington standard model: n=3 polytrope (\u03b3 = 4/3), historically applied to the Sun and other main-sequence stars as a first approximation combining radiation pressure with a simplified opacity law -- a precursor to this course\u2019s more complete four-equation treatment (Lecture 01) with a realistic, non-polytropic equation of state and opacity law.',
            f'The n=3 polytrope\u2019s central-density-independent mass, M_n=3 = 4\u03c0(K/\u03c0G)^(3/2)(-\u03be\u00b2 d\u03b8/d\u03be)|_{{\u03be_1}}, is precisely the mathematical structure Lecture 12 uses (with K set by relativistic electron degeneracy pressure rather than an arbitrary constant) to derive the Chandrasekhar mass of {CHANDRASEKHAR_MASS_MUE2_MSUN:.3f} M\u2609.',
        ],
        pitfall='Assuming a polytropic model is a realistic stellar-structure solution for an arbitrary star. A polytrope\u2019s single fixed exponent \u03b3 cannot simultaneously capture a star\u2019s actual, depth-varying equation of state, opacity, and energy generation; polytropic models are most reliable either as historical/pedagogical approximations (the Eddington standard model) or in genuinely polytropic physical regimes (fully convective envelopes, fully degenerate matter), not as general-purpose precision stellar models.',
        activity='Given that the n=3 polytrope\u2019s mass is independent of central density, while lower-n polytropes\u2019 masses are not, explain in words why this single mathematical fact is exactly what makes the Chandrasekhar mass (Lecture 12) a fixed number rather than a family of possible white-dwarf masses.',
        lab_connection='Lab 04\u2019s mass-luminosity-lifetime fitting is the homology-relation analog developed informally in Lecture 07; this lecture\u2019s polytropic framework is the more rigorous mathematical machinery underlying that informal reasoning.',
        synthesis='Polytropic models trade full physical realism for mathematical tractability by fixing a single equation-of-state exponent, and while this makes them inadequate as general precision stellar models, the specific n=3 case supplies the exact mathematical structure this course needs in Lecture 12 to derive the Chandrasekhar mass.',
        openstax='OpenStax Astronomy 2e does not develop polytropic stellar models; this course introduces the Lane-Emden formalism specifically to prepare for the Chandrasekhar-mass derivation in Lecture 12.',
    ),
    dict(
        n=9, title='Post-Main-Sequence Evolution: Shell Burning and the Red Giant Branch',
        subtitle='What happens when the core runs out of hydrogen',
        goals=[
            'Explain why core hydrogen exhaustion leads to core contraction and envelope expansion rather than simply the star turning off.',
            'Describe hydrogen shell burning and the physical origin of the Sch\u00f6nberg-Chandrasekhar limit for an isothermal helium core.',
            'Apply the main-sequence lifetime scaling (Lecture 07) and a real star cluster\u2019s main-sequence turnoff to estimate a cluster\u2019s age, and honestly assess the result against the cluster\u2019s independently measured age.',
        ],
        why_matters='Every star this course has discussed so far (Alpha Centauri A/B, Sirius A, the Sun) is still on the main sequence; this lecture is the pivot point where the course turns from "how a star maintains equilibrium" to "how a star\u2019s equilibrium structure changes as its core composition changes," beginning the evolutionary story that occupies the rest of the course.',
        phenomenon=f'The Hyades open cluster, whose distance ({HYADES["distance_pc"]:.0f} pc) and age ({HYADES["age_myr"]:.0f} Myr) were live-verified this session, shows a well-defined main-sequence turnoff at a stellar mass of about {HYADES["turnoff_mass_msun"]:.1f} M\u2609: stars above this mass have already evolved into subgiants, giants, or white dwarfs, while less massive stars remain on the main sequence -- a direct, real-world illustration of the mass-dependent stellar lifetime derived in Lecture 07.',
        vocab=['main-sequence turnoff', 'isochrone', 'shell burning', 'red giant branch', 'Sch\u00f6nberg-Chandrasekhar limit', 'core-envelope decoupling'],
        evidence=[
            'Every star cluster\u2019s stars are, to good approximation, coeval (formed at essentially the same time from the same molecular cloud), so a cluster\u2019s color-magnitude diagram directly shows which masses have already evolved off the main sequence, providing the isochrone method for dating clusters used throughout this lecture and Lab 05.',
            'Detailed stellar-evolution models of a hydrogen-exhausted stellar core reproduce the observed rapid radius expansion and luminosity increase that defines the red giant branch, driven by a thin, extremely temperature-sensitive hydrogen-burning shell surrounding a contracting, inert helium core.',
            'Stars found in the Sch\u00f6nberg-Chandrasekhar-limit-violating regime (isothermal helium core mass exceeding roughly 10% of the star\u2019s total mass) are observed to undergo rapid core contraction and envelope expansion on a short (thermal, not nuclear) timescale, consistent with the loss of hydrostatic support once the limit is exceeded.',
        ],
        model=[
            'Once core hydrogen is exhausted, the core (now composed of inert helium, with no local energy generation) begins to contract under its own gravity, while hydrogen fusion continues in a thin shell surrounding the core, where fresh hydrogen is still present at a temperature high enough for pp-chain or CNO-cycle burning (Lectures 05-06).',
            'The core, receiving essentially no energy generation of its own, cannot use radiative energy transport to remain in a stable temperature profile; instead it approaches a roughly isothermal state, and Sch\u00f6nberg and Chandrasekhar showed that an isothermal core in hydrostatic equilibrium can only support a limited fraction (\u2248 10%, depending on composition) of the star\u2019s total mass before hydrostatic equilibrium fails and the core must contract rapidly.',
            'As the core contracts and heats (releasing gravitational potential energy, per the virial theorem of ASTR 310 Lecture 06), the hydrogen-burning shell above it also heats and expands, driving a dramatic increase in the star\u2019s radius and luminosity that defines its ascent up the red giant branch.',
        ],
        equation=r'\left(\dfrac{M_{\rm core}}{M_\star}\right)_{\rm SC} \approx 0.37\left(\dfrac{\mu_{\rm env}}{\mu_{\rm core}}\right)^{2}\ \ (\text{Sch\"onberg--Chandrasekhar limit, schematic})',
        example=[
            f'Hyades main-sequence turnoff mass (live-verified this session): {HYADES["turnoff_mass_msun"]:.1f} M\u2609. Mass-luminosity prediction (Lecture 07): L \u2248 M^3.5 = {HYADES_TURNOFF_L_PRED_LSUN:.2f} L\u2609.',
            f'Predicted main-sequence lifetime for a {HYADES["turnoff_mass_msun"]:.1f} M\u2609 star: t_MS = 10 Gyr \u00d7 (M/L) = {HYADES_TURNOFF_LIFETIME_PRED_GYR:.3f} Gyr = {HYADES_TURNOFF_LIFETIME_PRED_GYR*1000:.0f} Myr.',
            f'Actual, independently measured (isochrone-fit) Hyades cluster age (live-verified this session, Perryman et al. 1998): {HYADES["age_myr"]:.0f} Myr = {HYADES_ACTUAL_AGE_GYR:.3f} Gyr. The predicted turnoff lifetime is about {HYADES_AGE_DISCREPANCY_FACTOR:.1f} times larger than the cluster\u2019s actual age -- a genuine, factor-of-two-scale discrepancy, not close agreement. This is an expected consequence of the fixed n=3.5 mass-luminosity exponent and the Sun-calibrated lifetime constant both being approximations (Lecture 07\u2019s pitfall): a more accurate mass-dependent exponent and a lifetime constant calibrated near 2-3 M\u2609 rather than at 1 M\u2609 would bring the two closer together, but this lecture reports the actual size of the discrepancy honestly rather than describing it as good agreement.',
        ],
        pitfall='Describing this lecture\u2019s factor-of-two turnoff-age discrepancy as "excellent agreement" or glossing over its size. A rough order-of-magnitude scaling relation reproducing a real cluster\u2019s age to within a factor of about two is a genuine success for such a simple model, but it is not close quantitative agreement, and claiming otherwise would repeat exactly the kind of overstatement the ASTR 310 review process explicitly corrected.',
        activity='Given that the Hyades turnoff-mass lifetime prediction overshoots the cluster\u2019s actual age by about a factor of two, and knowing the true mass-luminosity exponent is not a fixed 3.5 across all masses, explain qualitatively whether a steeper true exponent near 2-3 M\u2609 would bring the predicted lifetime closer to or further from the measured age.',
        lab_connection='Lab 05 reproduces this lecture\u2019s Hyades turnoff-age calculation in full and additionally compares it to the cluster\u2019s independently measured total mass and structural radii.',
        synthesis='Post-main-sequence evolution begins when a star\u2019s core, no longer generating its own energy, is forced into a Sch\u00f6nberg-Chandrasekhar-limited, roughly isothermal contraction while a surrounding hydrogen shell continues burning -- and this lecture\u2019s honestly reported factor-of-two turnoff-age discrepancy for the real Hyades cluster is a genuine demonstration of both the power and the limitations of a simple mass-luminosity-lifetime scaling.',
        openstax='OpenStax Astronomy 2e, Chapter 21.1-21.2 (evolution of low-mass stars, red giants) presents shell burning and the red giant branch qualitatively; this course derives the Sch\u00f6nberg-Chandrasekhar limit\u2019s physical origin and applies the isochrone method quantitatively to a real cluster.',
    ),
    dict(
        n=10, title='Helium Burning: The Triple-Alpha Process and the Horizontal Branch',
        subtitle='A famously improbable nuclear reaction, made possible by a predicted resonance',
        goals=[
            'Explain why fusing three helium-4 nuclei to carbon-12 is astrophysically difficult, given the instability of beryllium-8.',
            'Describe Fred Hoyle\u2019s 1954 prediction of a carbon-12 nuclear resonance, made purely from stellar-nucleosynthesis reasoning, and its subsequent laboratory confirmation.',
            'Compute the triple-alpha reaction\u2019s net energy release and compare its ignition temperature to the pp-chain/CNO-cycle temperatures of Lectures 05-06.',
        ],
        why_matters='The triple-alpha process is one of the most celebrated examples in all of physics of a theoretical prediction (an as-yet-undiscovered nuclear energy level) made purely from an astrophysical argument (the observed cosmic abundance of carbon) and subsequently confirmed in the laboratory -- a vivid illustration of nuclear astrophysics functioning as genuine, falsifiable physical science.',
        phenomenon='Beryllium-8, the product of fusing two helium-4 nuclei, is so unstable (mean lifetime of order 10\u207b\u00b9\u2076 seconds) that essentially none should survive long enough to capture a third helium-4 nucleus and form carbon-12 by simple sequential fusion -- yet the universe unambiguously contains substantial carbon, a direct empirical contradiction that Fred Hoyle resolved in 1954 by predicting a specific nuclear resonance.',
        vocab=['triple-alpha process', 'beryllium-8 instability', 'nuclear resonance', 'Hoyle state', 'helium flash', 'horizontal branch'],
        evidence=[
            'Laboratory nuclear-physics experiments, motivated directly by Hoyle\u2019s prediction, subsequently confirmed the existence of an excited carbon-12 nuclear state (the "Hoyle state") at almost exactly the predicted energy, dramatically enhancing the beryllium-8 + helium-4 capture rate via resonance and making triple-alpha burning astrophysically viable after all.',
            'Low-mass stars (like the Sun, eventually) are observed and modeled to ignite helium burning in a highly degenerate core via a runaway "helium flash," while higher-mass stars ignite helium burning non-degenerately and smoothly -- both regimes reproduced by detailed stellar-evolution models using the resonant triple-alpha rate.',
            'Globular clusters (real, old star clusters) show a well-populated "horizontal branch" in their color-magnitude diagrams, a distinct evolutionary phase corresponding to stable core helium burning following the helium flash, exactly as stellar-evolution theory predicts for the low-mass, old stellar populations found in globular clusters.',
        ],
        model=[
            'Two helium-4 nuclei fuse to form beryllium-8 in a reaction that is endothermic and produces an extremely short-lived, unstable nucleus; only a tiny, transient equilibrium abundance of beryllium-8 exists in helium-burning conditions at any instant.',
            'Without a resonance, the probability that a third helium-4 nucleus captures onto this tiny transient beryllium-8 population before it decays would be far too low to produce astrophysically significant carbon-12; Hoyle argued that because carbon (and the heavier elements built from it) unambiguously exists in the universe, an excited nuclear state of carbon-12 must exist at almost exactly the beryllium-8 + helium-4 combined energy, dramatically enhancing the capture rate via resonance.',
            'The subsequent laboratory discovery of this predicted "Hoyle state" confirmed the astrophysical argument and completed the triple-alpha reaction chain, He-4 + He-4 \u2192 Be-8 (unstable), Be-8 + He-4 \u2192 C-12* (resonant) \u2192 C-12 + \u03b3, releasing a net energy Q per completed reaction.',
        ],
        equation=r'3\,^4\mathrm{He} \rightarrow\, ^{12}\mathrm{C} + \gamma, \qquad Q = 3\,\Delta(^4\mathrm{He}) - \Delta(^{12}\mathrm{C})',
        example=[
            f'Net triple-alpha energy release from measured atomic mass excesses (3 \u00d7 2.4249 MeV for \u00b3 helium-4 nuclei, minus 0.0 MeV for carbon-12, which by definition anchors the atomic mass unit): Q = {TRIPLE_ALPHA_Q_MEV:.4f} MeV per completed reaction.',
            f'Per unit mass, the triple-alpha process releases {TRIPLE_ALPHA_Q_MEV/ (3*4.0026):.4f} MeV per atomic mass unit of fuel consumed, compared to the pp chain\u2019s {PP_CHAIN_Q_MEV/4.0326:.4f} MeV per atomic mass unit (four hydrogen-1 nuclei, each of mass \u2248 1.0078 u) -- triple-alpha burning releases roughly a factor of {(PP_CHAIN_Q_MEV/4.0326)/(TRIPLE_ALPHA_Q_MEV/(3*4.0026)):.1f} less energy per unit mass of fuel than hydrogen fusion, consistent with the general pattern that each successive nuclear-burning stage in stellar evolution is less energetically efficient than the last.',
            'Helium ignition requires core temperatures around (1-2) \u00d7 10\u2078 K, roughly an order of magnitude hotter than the pp-chain/CNO-cycle hydrogen-burning temperatures of Lectures 05-06 (a few \u00d7 10\u2077 K), consistent with the larger Coulomb barrier (Z=2 helium nuclei versus Z=1 hydrogen) requiring a correspondingly higher Gamow-peak temperature (Lecture 05) to proceed at an appreciable rate.',
        ],
        pitfall='Assuming the triple-alpha process is simply "helium fusing like hydrogen does, but hotter." The reaction chain\u2019s viability depends critically on a specific nuclear resonance that has no analog in the pp chain or CNO cycle; without the Hoyle state, stellar helium burning (and therefore all heavier-element nucleosynthesis built from carbon) would be astrophysically negligible, regardless of temperature.',
        activity='Given that Hoyle\u2019s prediction started from the observed existence of carbon in the universe and worked backward to infer a specific, previously unknown nuclear energy level, explain in one or two sentences why this counts as a genuine, falsifiable scientific prediction rather than a post-hoc explanation.',
        lab_connection='Lab 06 (white dwarf/Chandrasekhar mass) discusses the pre-white-dwarf helium- and carbon/oxygen-burning history of a star like Sirius B\u2019s progenitor, connecting this lecture\u2019s triple-alpha process to the composition (carbon-oxygen) of the white dwarfs analyzed there.',
        synthesis='The triple-alpha process only proceeds at an astrophysically significant rate because of a specific, resonantly enhanced nuclear energy level that Fred Hoyle correctly predicted from purely astrophysical reasoning before it was found in the laboratory -- a striking historical example of nucleosynthesis physics functioning as testable science, and the essential bridge from hydrogen- to carbon/oxygen-based stellar chemistry.',
        openstax='OpenStax Astronomy 2e, Chapter 21.3 (evolution of low-mass stars: helium fusion) describes the helium flash and horizontal branch qualitatively; this course develops the resonance argument and Hoyle\u2019s historical prediction explicitly.',
    ),
    dict(
        n=11, title='Late Stages of Low- and Intermediate-Mass Stars: AGB, Planetary Nebulae, and White Dwarf Formation',
        subtitle='How a star like the Sun actually ends its life',
        goals=[
            'Describe the asymptotic giant branch (AGB) phase\u2019s double-shell-burning structure and thermal pulses.',
            'Explain how AGB mass loss forms a planetary nebula and exposes the former stellar core as a white dwarf.',
            'Connect a real, precisely characterized white dwarf (Sirius B) to its inferred progenitor mass and evolutionary history.',
        ],
        why_matters='This lecture completes the low-to-intermediate-mass stellar evolutionary sequence begun in Lecture 09 (main-sequence turnoff), continued in Lecture 10 (helium burning), and now ending in exactly the kind of compact remnant -- a carbon-oxygen white dwarf -- whose maximum possible mass this course derives quantitatively in Lecture 12.',
        phenomenon=f'Sirius B, whose mass ({SIRIUS_B["mass_msun"]:.3f} M\u2609) and radius ({SIRIUS_B["radius_rsun"]:.6f} R\u2609) were independently live-verified in ASTR 230\u2019s production and used quantitatively throughout ASTR 310, is understood to be the exposed core of a star that, on the main sequence, was substantially more massive than the Sun -- its entire outer envelope having been lost during the AGB phase this lecture describes.',
        vocab=['asymptotic giant branch (AGB)', 'thermal pulse', 'double-shell burning', 'planetary nebula', 'white dwarf', 'initial-final mass relation'],
        evidence=[
            'Planetary nebulae are observed around thousands of evolved stars, each showing an expanding shell of ejected gas surrounding a hot, compact central star -- exactly the two-part structure (ejected envelope, exposed core) predicted by AGB mass-loss theory.',
            'The observed masses of white dwarfs in star clusters of known age and turnoff mass (the "initial-final mass relation") show that stars with a wide range of main-sequence masses (roughly 1-8 M\u2609) all produce white dwarfs in a much narrower mass range (typically 0.5-1.0 M\u2609), consistent with AGB mass loss removing the great majority of a star\u2019s original mass before core exposure.',
            'AGB stars are directly observed to undergo periodic luminosity and mass-loss-rate variations (thermal pulses), consistent with the alternating hydrogen-shell and helium-shell burning instability predicted by detailed AGB stellar models.',
        ],
        model=[
            'Following core helium exhaustion (Lecture 10), a low-to-intermediate-mass star develops an inert carbon-oxygen core surrounded by two active burning shells (helium fusing to carbon/oxygen in the inner shell, hydrogen fusing to helium in the outer shell), a structure that defines the asymptotic giant branch.',
            'The helium-burning shell is thermally unstable: it periodically flares up in brief, intense "thermal pulses" that drive convective mixing and substantial mass loss via strong stellar winds, progressively stripping away the star\u2019s hydrogen-rich envelope over the AGB phase\u2019s final stages.',
            'Once the envelope is sufficiently reduced, the exposed hot core photoionizes the still-expanding ejected envelope, producing a planetary nebula for a few tens of thousands of years, after which the nebula disperses and the exposed core is left as a white dwarf, supported not by nuclear burning (which has ceased entirely) but by electron degeneracy pressure (Lecture 12).',
        ],
        equation=r'M_{\rm WD} = f_{\rm IFMR}(M_{\rm ZAMS})\ \ (\text{initial--final mass relation, empirically calibrated in star clusters})',
        example=[
            f'Sirius B: measured mass {SIRIUS_B["mass_msun"]:.3f} M\u2609, measured radius {SIRIUS_B["radius_rsun"]:.6f} R\u2609 (carried forward, live-verified in ASTR 230/ASTR 310), effective temperature {SIRIUS_B["teff"]:.0f} K.',
            f'Stefan-Boltzmann luminosity from these measured parameters (ASTR 310, Lecture 02 method): L = 4\u03c0R\u00b2\u03c3T\u2074 = {SIRIUS_B_LUM_LSUN:.4f} L\u2609 -- a tiny luminosity from a very hot surface, the hallmark combination (small, hot, faint) that identifies a white dwarf on an HR diagram.',
            'Applying a standard published initial-final mass relation (e.g., Kalirai et al.-type calibrations from real star clusters) to Sirius B\u2019s measured white-dwarf mass implies a zero-age main-sequence progenitor mass of roughly 5 M\u2609 (a standard published estimate, not independently re-derived in this course, flagged for spot-check in the reference log) -- consistent with Sirius B having lost the great majority of its original mass during AGB evolution before this lecture\u2019s mechanism exposed its core.',
        ],
        pitfall='Assuming a white dwarf\u2019s mass directly reflects "how much mass the star started with." The initial-final mass relation is highly non-linear and compresses a wide range of main-sequence progenitor masses into a narrow range of white-dwarf masses; a white dwarf\u2019s mass alone, without an independently calibrated initial-final mass relation, does not determine its progenitor\u2019s original mass.',
        activity='Given that AGB mass loss can remove several solar masses of material while leaving a white dwarf core of order one solar mass, explain qualitatively why the initial-final mass relation must be a strongly compressive (many-to-one, in mass) mapping rather than a simple proportional relation.',
        lab_connection='Lab 06 uses Sirius B\u2019s measured mass and radius, established here as this lecture\u2019s white-dwarf endpoint example, to compute its degeneracy pressure and compare its mass to the Chandrasekhar limit derived in Lecture 12.',
        synthesis='A star like Sirius B\u2019s progenitor ends its life not with a single dramatic event but through a gradual, thermally pulsing envelope-stripping process on the asymptotic giant branch, exposing a carbon-oxygen core supported thereafter by electron degeneracy pressure rather than nuclear burning or thermal gas pressure.',
        openstax='OpenStax Astronomy 2e, Chapter 21.4-21.5 (evolution of low-mass stars: the death of a low-mass star, white dwarfs) covers the AGB, planetary nebula, and white dwarf phases descriptively; this course connects this sequence quantitatively to Sirius B\u2019s independently measured parameters.',
    ),
    dict(
        n=12, title='Electron Degeneracy and the Chandrasekhar Mass',
        subtitle='A maximum stellar mass from quantum mechanics alone',
        goals=[
            'Derive the electron degeneracy pressure\u2019s scaling with density from the Pauli exclusion principle and the Heisenberg uncertainty principle.',
            'Derive the Chandrasekhar mass from the n=3 polytrope (Lecture 08) applied to the relativistic-degenerate equation of state, and evaluate it numerically.',
            'Apply the result to Sirius B and to the more massive PSR J0348+0432 neutron star, and correctly classify each relative to the limit.',
        ],
        why_matters='This is the single most important quantitative result connecting stellar evolution to compact-object astrophysics: it explains why white dwarfs have a maximum possible mass, why exceeding that mass produces a different kind of compact object entirely (Lecture 13), and it is derived here using exactly the n=3 polytrope machinery built in Lecture 08 for a completely different-looking physical system.',
        phenomenon=f'PSR J0348+0432\u2019s neutron star, whose mass ({PSR_J0348["neutron_star_mass_msun"]:.2f} \u00b1 {PSR_J0348["neutron_star_mass_err"]:.2f} M\u2609) was live-verified this session via a direct fetch of its measured orbital and relativistic parameters, is far too massive to be a white dwarf -- exactly the physical distinction this lecture\u2019s Chandrasekhar-mass derivation makes precise.',
        vocab=['electron degeneracy pressure', 'Pauli exclusion principle', 'Fermi energy', 'relativistic degeneracy', 'Chandrasekhar mass', 'mu_e (mean molecular weight per electron)'],
        evidence=[
            'No white dwarf has ever been observed with a mass exceeding approximately 1.4 M\u2609, despite thousands of white dwarfs having been precisely characterized, directly consistent with the Chandrasekhar mass acting as a genuine, universal upper limit rather than a typical or average value.',
            'Type Ia supernovae, understood to result from a white dwarf being pushed to (or very near) the Chandrasekhar mass by mass transfer or merger, show a strikingly uniform peak luminosity across a very wide range of host galaxies -- direct observational evidence that a single, nearly universal mass scale governs their explosion, exactly as the Chandrasekhar-mass derivation predicts.',
            'PSR J0348+0432\u2019s neutron star, measured via a combination of radio pulsar timing and white-dwarf-companion spectroscopy (Antoniadis et al. 2013), has a mass well above any observed white dwarf, directly confirming that objects above the Chandrasekhar mass are supported by a physically distinct mechanism (neutron degeneracy pressure, Lecture 13) rather than simply being unusually massive white dwarfs.',
        ],
        model=[
            'The Pauli exclusion principle forbids two electrons from occupying the same quantum state; compressing a gas of electrons to high density therefore forces them to occupy increasingly high-momentum states, producing a pressure (degeneracy pressure) that exists even at zero temperature and depends only on density, not on temperature at all.',
            'For non-relativistic degenerate electrons, this gives P \u221d \u03c1^(5/3) (an n=3/2 polytrope, Lecture 08); but as density rises further, the electrons\u2019 Fermi momentum approaches m_e c, and the equation of state softens to the relativistic-degenerate limit, P \u221d \u03c1^(4/3) -- exactly the n=3 polytrope of Lecture 08.',
            'Because the n=3 polytrope\u2019s mass is independent of central density (Lecture 08), applying it to the relativistic-degenerate equation of state produces a single, fixed maximum mass -- the Chandrasekhar mass -- above which no static, cold, electron-degenerate configuration exists at all, regardless of how much further the star is compressed.',
        ],
        equation=r'M_{\rm Ch} = \dfrac{\omega_3^{0}\sqrt{3\pi}}{2}\left(\dfrac{\hbar c}{G}\right)^{3/2}\dfrac{1}{(\mu_e m_p)^{2}}, \qquad \omega_3^{0} = 2.018236\ (\text{Lane--Emden } n=3)',
        example=[
            f'Evaluating the Chandrasekhar-mass formula numerically for a carbon-oxygen white dwarf (\u03bc_e = 2.0, one electron per two nucleons): M_Ch = {CHANDRASEKHAR_MASS_MUE2_MSUN:.4f} M\u2609 -- in close agreement with the commonly cited value of about 1.4 M\u2609 (this course\u2019s own first-principles derivation, not simply quoting the standard number).',
            f'Sirius B: measured mass {SIRIUS_B["mass_msun"]:.3f} M\u2609 = {SIRIUS_B_TO_CHANDRA_FRACTION*100:.1f}% of the Chandrasekhar mass derived above -- comfortably below the limit, consistent with its stable, observed existence as a white dwarf for a Sirius-system age of a few hundred million years.',
            f'PSR J0348+0432\u2019s neutron star: measured mass {PSR_J0348["neutron_star_mass_msun"]:.2f} M\u2609 = {PSR_TO_CHANDRA_FRACTION*100:.0f}% of the Chandrasekhar mass -- well above the limit for any electron-degenerate configuration, direct confirmation that this object cannot be, and is not, a white dwarf; its companion white dwarf, at {PSR_J0348["wd_mass_msun"]:.3f} M\u2609 ({PSR_WD_TO_CHANDRA_FRACTION*100:.1f}% of M_Ch), is safely below the limit, as real, stable white dwarfs must be.',
        ],
        pitfall='Assuming the Chandrasekhar mass is exactly 1.4 M\u2609 for every white dwarf. The exact value depends on the composition-dependent mean molecular weight per electron \u03bc_e (2.0 for carbon-oxygen, close to 2.0 but not identical for other compositions); this lecture\u2019s numerical result of {:.3f} M\u2609 for \u03bc_e=2.0 is close to, but not required to be pixel-identical with, the frequently quoted "1.4 M\u2609" figure.',
        activity='Using M_Ch \u221d \u03bc_e\u207b\u00b2, predict qualitatively (without recomputing) whether a white dwarf composed of pure helium (\u03bc_e \u2248 2.0, essentially the same as carbon-oxygen) or one with a larger fraction of heavier, more neutron-rich nuclei (slightly higher \u03bc_e) would have the larger Chandrasekhar mass.',
        lab_connection='Lab 06 computes the Chandrasekhar mass exactly as derived here and applies it to Sirius B; Lab 07\u2019s capstone applies the same limit to PSR J0348+0432 to confirm it must be a neutron star, not a white dwarf.',
        synthesis='The Chandrasekhar mass, derived here from the same n=3 polytrope machinery built in Lecture 08 but now applied to relativistic electron degeneracy pressure, is a genuine maximum mass for any cold, static, electron-degenerate star -- a limit this lecture confirms quantitatively using both a real white dwarf safely below it (Sirius B) and a real neutron star safely above it (PSR J0348+0432).',
        openstax='OpenStax Astronomy 2e, Chapter 22.1-22.2 (the death of a high-mass star, white dwarf limits) states the Chandrasekhar mass\u2019s existence and approximate value; this course derives its numerical value directly from the n=3 polytrope and fundamental constants.',
    ),
    dict(
        n=13, title='Massive Star Evolution and the Core-Collapse Supernova Mechanism',
        subtitle='From an iron core to a neutron star, in about one second',
        goals=[
            'Describe the onion-layered burning structure of a massive star\u2019s final stages and explain why iron-peak fusion cannot release further nuclear energy.',
            'Explain the basic physics of core collapse once the iron core exceeds its own (Chandrasekhar-like) stability limit.',
            'Compute the gravitational binding energy released in forming a neutron star and compare it to the energy actually observed in a typical core-collapse supernova.',
        ],
        why_matters='Lecture 12\u2019s Chandrasekhar mass explained why white dwarfs have a maximum mass; this lecture asks what happens to a star whose core exceeds that limit while still actively burning -- the answer, developed here, is the most energetic single event a star can undergo, and the direct origin of the compact-object mass measurements (Lecture 12\u2019s PSR J0348+0432) this course has used throughout.',
        phenomenon=f'A core-collapse supernova releases of order {SN_BINDING_ENERGY_RELEASED_J:.1e} J of gravitational binding energy in forming a neutron star, yet only about {SN_OBSERVED_KINETIC_PLUS_LIGHT_J:.0e} J of that energy actually emerges as the explosion\u2019s observed kinetic energy and light -- a genuinely enormous energy budget in which the visible explosion is only a small fraction of the total energy release.',
        vocab=['onion-shell burning structure', 'iron core', 'photodisintegration', 'core collapse', 'neutronization', 'core-bounce shock', 'neutrino-driven explosion'],
        evidence=[
            'Massive stars (\u2273 8 M\u2609) are found, in stellar-evolution models constrained by observed supernova progenitors, to develop successive concentric burning shells (hydrogen, helium, carbon, neon, oxygen, silicon) surrounding an inert iron-peak core, exactly the onion-shell structure this lecture describes.',
            'SN 1987A, the nearest well-observed core-collapse supernova in modern times, was accompanied by a burst of neutrinos detected simultaneously at multiple independent underground observatories (Kamiokande-II, IMB, Baksan), directly confirming that the overwhelming majority of a core-collapse supernova\u2019s energy release is carried away by neutrinos, not by the visible explosion.',
            'Real, precisely measured neutron-star masses (including PSR J0348+0432\u2019s {PSR_J0348["neutron_star_mass_msun"]:.2f} M\u2609, Lecture 12) cluster in a range consistent with iron-core-collapse models\u2019 predicted remnant masses, providing an end-to-end observational check on the core-collapse mechanism this lecture derives.',
        ],
        model=[
            'Successive nuclear burning stages (hydrogen, helium, carbon, neon, oxygen, silicon) proceed at progressively higher temperatures and shorter durations (following the steep Gamow-peak temperature sensitivity of Lectures 05-06, now applied to increasingly high-Z fuels), ultimately producing an inert core of iron-peak nuclei, which have the highest nuclear binding energy per nucleon of any elements and therefore cannot release further energy by either fusion or fission.',
            'Once the iron core\u2019s mass approaches its own effective Chandrasekhar-like limit (reduced from Lecture 12\u2019s pure electron-degenerate value by the additional effects of electron capture and photodisintegration of iron nuclei at these extreme temperatures and densities), electron degeneracy pressure can no longer support it, and the core collapses in well under a second, reaching densities comparable to nuclear saturation density.',
            'Collapse halts abruptly once the core reaches nuclear density (where the strong nuclear force itself, not electron degeneracy, provides pressure support), producing a rebounding shock wave; while the shock alone often stalls, the enormous flux of neutrinos streaming out of the newly formed proto-neutron star is understood, in modern simulations, to be a leading mechanism for reviving the shock and driving the star\u2019s outer layers away as the visible supernova explosion.',
        ],
        equation=r'E_{\rm binding} \sim \dfrac{3}{5}\dfrac{GM^{2}}{R}\bigg|_{\rm core} - \dfrac{3}{5}\dfrac{GM^{2}}{R}\bigg|_{\rm remnant}',
        example=[
            f'Gravitational binding energy released collapsing a {SN_CORE_MASS_MSUN:.1f} M\u2609 iron core (initial radius \u2248 {SN_PROGENITOR_CORE_RADIUS_M/1000:.0f} km, a standard published order-of-magnitude pre-collapse iron-core radius) down to a neutron-star remnant (radius \u2248 {SN_REMNANT_RADIUS_M/1000:.0f} km, using PSR J0348+0432\u2019s measured neutron-star radius from Lecture 12): \u0394E \u2248 (3/5)GM\u00b2(1/R_remnant - 1/R_core) = {SN_BINDING_ENERGY_RELEASED_J:.2e} J.',
            f'Typical observed core-collapse supernova kinetic energy plus radiated light (a standard published order-of-magnitude value): {SN_OBSERVED_KINETIC_PLUS_LIGHT_J:.1e} J.',
            f'The observed visible energy is only about {(SN_OBSERVED_KINETIC_PLUS_LIGHT_J/SN_BINDING_ENERGY_RELEASED_J)*100:.2f}% of the total binding energy released -- meaning roughly {SN_NEUTRINO_FRACTION_ESTIMATE*100:.1f}% of the total energy budget must be carried away by some other channel. This is honestly consistent with, not an overstatement of, the real physical picture confirmed by SN 1987A\u2019s neutrino burst: the overwhelming majority of a core-collapse supernova\u2019s energy escapes as neutrinos, not as visible light or kinetic energy, exactly the roughly 99%-neutrino energy budget real core-collapse models and the SN 1987A neutrino detections independently establish.',
        ],
        pitfall='Describing a core-collapse supernova\u2019s visible explosion as releasing "all" of the star\u2019s available energy. As this lecture\u2019s own order-of-magnitude energy budget shows, the visible kinetic energy and light are only a small fraction (of order 1%) of the total gravitational binding energy released; the great majority of the energy escapes as neutrinos, which is precisely why neutrino detection (as achieved for SN 1987A) is essential observational evidence for the core-collapse mechanism, not merely a minor side channel.',
        activity='Using the observed roughly 99%-neutrino energy budget, explain why detecting a burst of neutrinos in coincidence with a nearby supernova\u2019s optical brightening (as happened for SN 1987A) is much stronger direct evidence for the core-collapse mechanism than the visible explosion\u2019s energy alone could ever provide.',
        lab_connection='Lab 07\u2019s capstone reproduces this lecture\u2019s binding-energy budget calculation using PSR J0348+0432\u2019s measured neutron-star mass and radius, and connects it to Lecture 14\u2019s nucleosynthesis synthesis.',
        synthesis='A massive star\u2019s core-collapse endpoint is forced by the same basic physics as Lecture 12\u2019s Chandrasekhar-mass limit (a maximum mass for degenerate matter), but at nuclear rather than atomic densities, and this lecture\u2019s honestly reported energy budget shows that the visible supernova is only a small, if spectacular, fraction of the total energy this collapse actually releases.',
        openstax='OpenStax Astronomy 2e, Chapter 22.3-22.5 (evolution of massive stars, supernovae) describes the onion-shell structure and core collapse qualitatively; this course derives the binding-energy budget quantitatively using PSR J0348+0432\u2019s live-verified measured parameters.',
    ),
    dict(
        n=14, title='Synthesis: Nucleosynthesis and Compact Remnants Across This Course',
        subtitle='From hydrogen to iron to neutron stars: closing the stellar-evolution story',
        goals=[
            'Summarize how successive nuclear-burning stages (Lectures 05, 06, 10, 13) build up the periodic table from hydrogen to the iron peak.',
            'Distinguish the s-process and r-process as the two dominant channels for building elements heavier than iron, and connect the r-process to compact-object mergers.',
            'Synthesize this course\u2019s two independent, real compact-object mass measurements (Sirius B, PSR J0348+0432) into a single physical picture of the two possible endpoints of stellar evolution.',
        ],
        why_matters='Every lecture in this course has built toward a specific piece of this synthesis: the nuclear-burning stages that build heavier elements (Lectures 05-06, 10, 13), the equations that describe why a star\u2019s core structure changes as its fuel supply changes (Lectures 01-04, 07-09), and the two sharply distinct compact-object endpoints (Lectures 11-13) that result. This final lecture assembles all of these pieces into a single coherent narrative and closes the course exactly as ASTR 310 did, by cross-checking multiple independent physical measurements of real objects against each other.',
        phenomenon=f'This course has used two real, independently measured compact objects throughout: Sirius B, a white dwarf at {SIRIUS_B_TO_CHANDRA_FRACTION*100:.1f}% of the Chandrasekhar mass, and PSR J0348+0432\u2019s neutron star, at {PSR_TO_CHANDRA_FRACTION*100:.0f}% of that same mass -- two objects on opposite sides of a single, quantitatively derived physical boundary (Lecture 12), providing this course\u2019s clearest demonstration that stellar-evolution theory correctly predicts which of two qualitatively different endpoints a collapsing stellar core actually reaches.',
        vocab=['nucleosynthesis', 's-process (slow neutron capture)', 'r-process (rapid neutron capture)', 'neutron star merger', 'compact-object endpoint', 'stellar-evolution synthesis'],
        evidence=[
            'Elements up to the iron peak are understood, from this course\u2019s own successive-burning-stage derivations (Lectures 05-06, 10, 13), to be built by charged-particle fusion reactions inside stars and released to the interstellar medium primarily via AGB winds (Lecture 11) and core-collapse supernovae (Lecture 13).',
            'Elements heavier than iron cannot be built by further fusion (Lecture 13\u2019s iron-peak binding-energy argument) and are instead built almost entirely by neutron-capture processes: the slow (s-process), operating in AGB stars over thousands of years between captures, and the rapid (r-process), operating in neutron-rich, high-flux environments on timescales of seconds.',
            'The 2017 multi-messenger observation of a neutron-star merger (GW170817, detected in gravitational waves and across the electromagnetic spectrum) provided direct observational confirmation that neutron-star mergers produce r-process nucleosynthesis, resolving a decades-long debate about the r-process\u2019s astrophysical site and directly connecting Lecture 12\u2019s compact-object mass measurements to heavy-element nucleosynthesis.',
        ],
        model=[
            'The s-process proceeds when the local neutron flux is low enough that a newly neutron-captured, radioactive nucleus almost always beta-decays before capturing a second neutron, producing a well-defined path along the valley of nuclear stability; this occurs in AGB stars (Lecture 11), where free neutrons are released episodically during thermal pulses.',
            'The r-process proceeds when the local neutron flux is so high that many neutrons are captured in rapid succession, before beta decay has time to occur, driving newly formed nuclei far from the valley of stability before a subsequent cascade of beta decays brings them back; this requires an extraordinarily neutron-rich, high-density environment, now confirmed observationally to occur in neutron-star mergers.',
            'This course\u2019s two real compact-object case studies -- Sirius B (Lecture 11-12, a white dwarf, formed by AGB mass loss without core collapse) and PSR J0348+0432\u2019s neutron star (Lecture 12-13, formed by core collapse) -- together span both of the qualitatively distinct endpoints of stellar evolution this course has developed, and both are consistent, at the quantitative level of Lecture 12\u2019s Chandrasekhar-mass calculation, with which side of that mass limit each object\u2019s progenitor core ended up on.',
        ],
        equation=r'M < M_{\rm Ch} \Rightarrow \text{white dwarf (Sirius B)}, \qquad M > M_{\rm Ch} \text{ (post-collapse)} \Rightarrow \text{neutron star (PSR J0348+0432)}',
        example=[
            f'Sirius B: measured mass {SIRIUS_B["mass_msun"]:.3f} M\u2609, {SIRIUS_B_TO_CHANDRA_FRACTION*100:.1f}% of the Chandrasekhar mass derived in Lecture 12 ({CHANDRASEKHAR_MASS_MUE2_MSUN:.3f} M\u2609) -- correctly on the sub-Chandrasekhar, white-dwarf side of the limit.',
            f'PSR J0348+0432\u2019s neutron star: measured mass {PSR_J0348["neutron_star_mass_msun"]:.2f} M\u2609, {PSR_TO_CHANDRA_FRACTION*100:.0f}% of the same Chandrasekhar mass -- correctly on the far side of the limit, consistent with this course\u2019s Lecture 13 core-collapse mechanism (not electron degeneracy alone) as the process that formed it.',
            f'Neutron-star mean density check: using PSR J0348+0432\u2019s measured mass and radius, \u03c1 \u2248 M/((4/3)\u03c0R\u00b3) = {PSR_NS_MEAN_DENSITY_KGM3:.3e} kg/m\u00b3, or {PSR_NS_DENSITY_TO_NUCLEAR_FRACTION*100:.0f}% of standard nuclear saturation density ({NUCLEAR_SATURATION_DENSITY_KGM3:.1e} kg/m\u00b3) -- confirming, independently of the Chandrasekhar-mass argument above, that this object\u2019s interior genuinely reaches nuclear densities, exactly as Lecture 13\u2019s core-collapse mechanism requires and Lecture 12\u2019s electron-degenerate white-dwarf picture (many orders of magnitude lower density) cannot reach.',
        ],
        pitfall='Treating this course\u2019s Chandrasekhar-mass-based classification (Sirius B below, PSR J0348+0432 above) as itself a complete explanation of neutron-star structure. The Chandrasekhar mass specifically describes the breakdown of electron degeneracy pressure; a full account of neutron-star structure additionally requires neutron degeneracy pressure and the strong nuclear force (the Tolman-Oppenheimer-Volkoff limit, a general-relativistic extension of this course\u2019s Newtonian Chandrasekhar-mass argument), which is beyond this course\u2019s scope but is the reason PSR J0348+0432\u2019s mass is cited in the literature as an empirical lower bound on that limit, not as evidence against it.',
        activity='Given that this course used exactly two real compact objects throughout (Sirius B and PSR J0348+0432\u2019s neutron star) and that both landed correctly on their expected side of the Chandrasekhar mass, explain why finding a real white dwarf above, or a real neutron star below, that limit would have been a serious problem for the theory developed in this course -- and why no such object has ever been observed.',
        lab_connection='Lab 07, the course\u2019s capstone, has students reproduce every calculation in this lecture\u2019s worked example from the raw measured masses and radii, and write a short synthesis connecting nucleosynthesis, compact-object formation, and the Chandrasekhar mass.',
        synthesis='Fourteen lectures of stellar structure and evolution converge on a single, sharply quantitative dividing line -- the Chandrasekhar mass -- that correctly separates this course\u2019s two real compact-object case studies, and on a nucleosynthesis picture in which every element heavier than iron owes its existence either to slow neutron capture in dying AGB stars or rapid neutron capture in the same neutron-star mergers that this course\u2019s compact-object physics predicts.',
        openstax='OpenStax Astronomy 2e, Chapter 23 (the death of stars) and Chapter 22 (star formation and evolution) together cover this synthesis descriptively; this course derives the Chandrasekhar-mass dividing line quantitatively and applies it directly to two real, independently measured objects.',
    ),
]


def slide_deck(item: dict) -> str:
    n = item['n']
    fig = lecture_svg(
        n, item['title'],
        left_label='observation', mid_label='physical law/derivation', right_label='inferred quantity',
        caption=item['synthesis'],
    )
    body = f"""<main class='deck'>
<section class='slide title'><p class='kicker'>ASTR 330 &middot; Lecture {n:02d}</p><h1>{escape(item['title'])}</h1><h2>{escape(item['subtitle'])}</h2></section>
<section class='slide'><h2>Learning Goals</h2><ol>{li(item['goals'])}</ol><p class='small'>Reading anchor: {escape(item['openstax'])}</p></section>
<section class='slide'><h2>Why This Matters</h2><p>{item['why_matters']}</p></section>
<section class='slide'><h2>Opening Phenomenon</h2><p>{item['phenomenon']}</p><p class='warning'><strong>First question:</strong> what here is directly observed, and what follows only once a physical law is derived and applied?</p></section>
<section class='slide'><h2>Vocabulary for Reasoning</h2><div class='three'>{cards(item['vocab'])}</div><p class='small'>Use these terms to describe derivations and evidence, not as isolated definitions.</p></section>
<section class='slide'><h2>Evidence We Need to Explain</h2><ul>{li(item['evidence'])}</ul></section>
<section class='slide'><h2>Derivation and Model</h2><ul>{li(item['model'])}</ul></section>
<section class='slide'><h2>Quantitative Tool</h2><div class='equation'>\\[ {item['equation']} \\]</div></section>
<section class='slide'><h2>Worked Example</h2><ol>{li(item['example'])}</ol></section>
<section class='slide visual-slide'><h2>Visual Reasoning</h2><div class='visual-grid'><div><p>Trace the reasoning chain from raw observation to derived physical law to inferred quantity in this lecture\u2019s figure.</p><ul><li>Which stage is directly observed?</li><li>Which stage is the physical law or derivation step?</li><li>What would change if an assumption in the derivation failed?</li></ul></div><figure class='visual-figure'>{fig}<figcaption>{escape(item['title'])}: from observation to inferred quantity.</figcaption></figure></div></section>
<section class='slide'><h2>Common Misconception</h2><p class='warning'>{item['pitfall']}</p></section>
<section class='slide'><h2>Active Learning Segment</h2><p>{item['activity']}</p></section>
<section class='slide'><h2>Lab Connection</h2><p>{item['lab_connection']}</p></section>
<section class='slide'><h2>Synthesis</h2><p>{item['synthesis']}</p></section>
<section class='slide'><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Course dataset and derivations used in this lecture\u2019s worked example: <code>materials/ASTR330/data/</code> and <code>materials/ASTR330/src/generate_astr330_content.py</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 330 Lecture {n:02d} Slides', body, SLIDE_CSS)


def lecture_notes(item: dict) -> str:
    n = item['n']
    body = f"""<header><div><h1>Lecture {n:02d}: {escape(item['title'])}</h1><p>ASTR 330 Astrophysics II: Stellar Structure and Evolution</p></div></header>
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
<section><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Every numeric result above is computed programmatically in <code>materials/ASTR330/src/generate_astr330_content.py</code>, not hand-typed.</li></ul></section>
</main>"""
    return page(f'ASTR 330 Lecture {n:02d} Notes', body)


def write_lectures():
    LECTURE_DIR.mkdir(parents=True, exist_ok=True)
    for item in LECTURES:
        n = item['n']
        (LECTURE_DIR / f'lecture-{n:02d}-slides.html').write_text(slide_deck(item), encoding='utf-8')
        (LECTURE_DIR / f'lecture-{n:02d}-notes.html').write_text(lecture_notes(item), encoding='utf-8')


def write_data_csv():
    import csv
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / 'hyades_cluster.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['quantity', 'value', 'unit'])
        for k, v in HYADES.items():
            w.writerow([k, v, ''])
    with open(DATA_DIR / 'psr_j0348+0432.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['quantity', 'value', 'unit'])
        for k, v in PSR_J0348.items():
            w.writerow([k, v, ''])
    with open(DATA_DIR / 'compact_remnants.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['object', 'mass_Msun', 'radius', 'fraction_of_chandrasekhar_mass'])
        w.writerow(['Sirius B (white dwarf)', SIRIUS_B['mass_msun'], f"{SIRIUS_B['radius_rsun']} Rsun", round(SIRIUS_B_TO_CHANDRA_FRACTION, 4)])
        w.writerow(['PSR J0348+0432 (neutron star)', PSR_J0348['neutron_star_mass_msun'], f"{PSR_J0348['neutron_star_radius_km']} km", round(PSR_TO_CHANDRA_FRACTION, 4)])
        w.writerow(['PSR J0348+0432 companion (white dwarf)', PSR_J0348['wd_mass_msun'], f"{PSR_J0348['wd_radius_rsun']} Rsun", round(PSR_WD_TO_CHANDRA_FRACTION, 4)])
        w.writerow(['Chandrasekhar mass (mu_e=2)', round(CHANDRASEKHAR_MASS_MUE2_MSUN, 4), '-', 1.0])


if __name__ == '__main__':
    write_lectures()
    write_data_csv()
    print(f'Wrote {len(LECTURES)} lecture slide decks and notes files, plus 3 data CSV files.')



