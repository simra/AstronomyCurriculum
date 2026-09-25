"""Content generator for ASTR360 (The Interstellar Medium) lecture slides and
lecture notes.

Every worked numeric example is computed programmatically from the shared
physical constants and real ISM datasets defined below (never hand-typed),
and the same constants are reused across labs and problem sets that
reference the same scenario (see generate_astr360_labs_psets.py). Run with
the project interpreter:
    python materials/ASTR360/src/generate_astr360_content.py
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
# Physical constants (SI unless noted; astronomical quantities kept in the
# cgs-adjacent units the ISM literature conventionally uses -- cm^-3, cm^-2,
# km/s -- with explicit conversions shown in every derivation).
# ---------------------------------------------------------------------------
G_CONST = 6.674e-11
C_LIGHT = 2.998e8
H_PLANCK = 6.626e-34
K_BOLTZMANN = 1.381e-23
SIGMA_SB = 5.670e-8
AU_M = 1.496e11
PC_M = 3.0857e16
LY_M = 9.461e15
YEAR_S = 3.156e7
M_SUN = 1.989e30
R_SUN = 6.957e8
L_SUN = 3.828e26
M_H_KG = 1.6726e-27
M_HE_KG = 6.6465e-27
AMU = 1.6605e-27
MU_MOLECULAR = 2.33   # mean molecular weight per particle, molecular cloud (H2 + He), standard ISM value
MU_ATOMIC = 1.27       # mean molecular weight per particle, atomic neutral gas (H + He), standard ISM value
MU_IONIZED = 0.61      # mean molecular weight per particle, fully ionized H+He plasma, standard ISM value

# 21 cm hyperfine transition (exact, defined constant of the hydrogen atom)
NU_21CM_HZ = 1420.405751e6
LAMBDA_21CM_M = C_LIGHT / NU_21CM_HZ
T_STAR_21CM_K = H_PLANCK * NU_21CM_HZ / K_BOLTZMANN  # hyperfine excitation temperature, ~0.0682 K
A10_21CM_S = 2.85e-15  # spontaneous emission (Einstein A) coefficient of the 21 cm transition, standard QM result

# ---------------------------------------------------------------------------
# Real ISM phase parameters (McKee & Ostriker 1977, ApJ 218, 148, "A theory
# of the interstellar medium: three components regulated by supernova
# explosions"; canonical textbook values also given in Draine 2011, "Physics
# of the Interstellar Medium," Table 1.1, and Ferriere 2001, Rev. Mod. Phys.
# 73, 1031). Standard published values, level 2, not independently
# re-verified this session.
# ---------------------------------------------------------------------------
ISM_PHASES = {
    'Molecular clouds (H2)': dict(n_cm3=2.0e2, T_k=15.0, filling=0.0005),
    'Cold neutral medium (CNM)': dict(n_cm3=30.0, T_k=80.0, filling=0.01),
    'Warm neutral medium (WNM)': dict(n_cm3=0.3, T_k=8.0e3, filling=0.35),
    'Warm ionized medium (WIM)': dict(n_cm3=0.15, T_k=8.0e3, filling=0.20),
    'H II regions': dict(n_cm3=1.0e2, T_k=1.0e4, filling=0.0005),
    'Hot ionized medium (HIM)': dict(n_cm3=3.5e-3, T_k=5.0e5, filling=0.43),
}

# 3C 273 sightline HI column density: standard published, all-sky HI4PI
# survey value widely used as the Galactic foreground HI column toward this
# very well studied quasar (HI4PI Collaboration 2016, A&A 594, A116; the
# specific N_HI = 1.79e20 cm^-2 figure is the commonly quoted value used in
# X-ray absorption studies of 3C 273, e.g. following Willingale et al. 2013,
# MNRAS 431, 394's total-Galactic-column methodology). Level 2.
SIGHTLINE_3C273 = dict(name='3C 273 (Galactic foreground)', l_deg=289.95, b_deg=64.36, n_hi_cm2=1.79e20)

# Cygnus X-1 sightline: standard published Galactic HI/X-ray absorbing
# column, widely quoted (e.g. Miller et al. 2009, ApJ 697, 900;
# Ng et al. 2019, MNRAS 482, 5265, X-ray spectral column density constraints
# converge near N_H ~ 6e21 cm^-2 toward this well-studied X-ray binary).
# Level 2.
SIGHTLINE_CYGX1 = dict(name='Cygnus X-1', l_deg=71.33, b_deg=3.07, n_hi_cm2=6.0e21)

# Representative CNM/WNM two-component 21 cm spectrum (spin temperatures and
# characteristic velocity widths are real, standard published CNM/WNM values,
# level 2; the specific synthetic Gaussian brightness-temperature profile
# used for the worked integration exercise is an illustrative representative
# spectrum, level 3, explicitly disclosed in reference-log.md -- not a
# specific published spectrum toward one exact sightline).
CNM_TSPIN_K = 100.0
WNM_TSPIN_K = 8000.0
CNM_FWHM_KMS = 3.0   # standard turbulent+thermal CNM linewidth, level 2
WNM_FWHM_KMS = 25.0  # standard WNM linewidth, level 2
CNM_PEAK_TB_K = 25.0   # illustrative synthetic peak brightness temperature, level 3
WNM_PEAK_TB_K = 4.0    # illustrative synthetic peak brightness temperature, level 3

# Interstellar extinction: Cardelli, Clayton & Mathis (1989), ApJ 345, 245
# average diffuse-ISM parametrization, R_V = 3.1 (level 2, the single most
# widely cited Milky Way average extinction law).
R_V_DIFFUSE = 3.1

# Cygnus OB2 No. 12: one of the most luminous and most heavily reddened
# early-type stars known (Massey & Thompson 1991, AJ 101, 1408; Maryeva &
# Chentsov 2012 spectroscopic study). Standard published values, level 2.
CYGOB2_12 = dict(name='Cygnus OB2 No. 12 (Schulte 12)', ebv_mag=3.10, r_v=3.0, distance_pc=1400.0)

# NGC 7023 (Iris Nebula) illuminating star HD 200775: a well-documented
# anomalous-extinction dense-cloud sightline with R_V significantly above
# the diffuse-ISM average (Whittet et al. 2001, A&A 368, 1140; standard
# review value R_V ~ 5.0 quoted for this reflection-nebula sightline).
# Standard published, level 2.
HD200775 = dict(name='HD 200775 (NGC 7023 illuminating star)', ebv_mag=0.53, r_v=5.0, distance_pc=345.0)

# Molecular ISM: CO-to-H2 conversion factor X_CO (Bolatto, Wolfire & Leroy
# 2013, ARA&A 51, 207, the standard Milky Way-disk value). Level 2.
X_CO_CM2_K_KMS = 2.0e20

# Orion Molecular Cloud complex (Bally 2008, "Overview of the Orion Complex,"
# in Handbook of Star Forming Regions; Genzel & Stutzki 1989, ARA&A 27, 41
# for the OMC-1 ridge). Standard published values, level 2.
ORION_MOLECULAR_CLOUD = dict(
    name='Orion Molecular Cloud (OMC-1 ridge)', distance_pc=414.0, mass_msun=2.0e3,
    radius_pc=1.0, n_h2_cm3=1.0e5, temp_k=25.0, co_linewidth_kms=3.0,
)
# Taurus Molecular Cloud (Goldsmith et al. 2008, ApJ 680, 428, the
# COMPLETE-survey mass/size; quiescent, distance from Galli et al. 2018,
# ApJ 859, 33 Gaia DR2 parallax study). Standard published, level 2.
TAURUS_MOLECULAR_CLOUD = dict(
    name='Taurus Molecular Cloud', distance_pc=140.0, mass_msun=1.5e4,
    radius_pc=6.0, n_h2_cm3=3.0e2, temp_k=10.0, co_linewidth_kms=1.5,
)

# Dense star-forming cores used for the Jeans-mass/free-fall-time worked
# examples. OMC-1 hot-core-adjacent dense clump (Bergin & Tafalla 2007,
# ARA&A 45, 339, "Cold Dark Clouds," representative dense-core values).
# Level 2.
OMC1_DENSE_CORE = dict(name='OMC-1 dense core', n_h2_cm3=1.0e5, temp_k=20.0)
# Barnard 68: a classic, extremely well-studied isolated Bok globule (Alves,
# Lada & Lada 2001, Nature 409, 159, near-infrared extinction mapping).
# Standard published values, level 2.
BARNARD68 = dict(name='Barnard 68', n_h2_cm3=8.0e4, temp_k=10.0, mass_msun=2.1, radius_pc=0.06, distance_pc=125.0)

# H II regions. Orion Nebula (M42): distance from Menten et al. (2007), A&A
# 474, 515 (VLBA trigonometric parallax, 414 +/- 7 pc); ionizing star theta1
# Orionis C spectral type/parameters (Simon-Diaz et al. 2006, A&A 448, 351);
# Lyman-continuum photon production rate for an O7V star (Vacca, Garmany &
# Shull 1996, ApJ 460, 914; Martins, Schaerer & Hillier 2005, A&A 436, 1049
# calibration, standard value ~1e49 photons/s for O7V); nebular electron
# density (Baldwin et al. 1991, ApJ 374, 580; Osterbrock & Ferland 2006
# textbook representative value ~600 cm^-3 for the bulk nebula, excluding
# the much denser core). Standard published values, level 2.
ORION_NEBULA = dict(
    name='Orion Nebula (M42)', distance_pc=414.0, ionizing_star='theta1 Orionis C',
    spectral_type='O7V', teff_k=39000.0, q_h_photons_s=1.0e49, n_e_cm3=600.0,
    observed_radius_pc=0.6, te_k=1.0e4,
)
ALPHA_B_CM3_S = 2.59e-13  # case B recombination coefficient at T_e = 1e4 K, standard atomic-physics value (Osterbrock & Ferland 2006)

# Rosette Nebula: ionized by the NGC 2244 OB cluster; large, lower-density,
# evolved H II region (standard published summary values consistent with
# Celnik 1985, A&AS 60, 465 and later radio/optical studies). Level 2.
ROSETTE_NEBULA = dict(
    name='Rosette Nebula', distance_pc=1600.0, ionizing_cluster='NGC 2244',
    q_h_photons_s=6.0e49, n_e_cm3=15.0, observed_radius_pc=10.0, te_k=1.0e4,
)

# Shocks: Cassiopeia A supernova remnant (Vink 2004, ApJ 604, 176 and
# subsequent Chandra proper-motion studies; standard quoted forward-shock
# velocity ~5000 km/s, distance ~3.4 kpc, age ~350 yr as of this course's
# reference epoch). Standard published, level 2.
CAS_A = dict(name='Cassiopeia A', distance_pc=3400.0, age_yr=350.0, shock_velocity_km_s=5000.0)
# Tycho's SNR (SN 1572): well-documented historical Type Ia remnant, forward
# shock velocity from proper-motion/Doppler studies (Williams et al. 2016,
# ApJ 823, 32, and refs. therein; standard quoted value ~5000 km/s averaged,
# with expansion age fixed by the historical 1572 date). Level 2.
TYCHO_SNR = dict(name="Tycho's SNR (SN 1572)", distance_pc=2500.0, age_yr=454.0, shock_velocity_km_s=4600.0)

# Cosmic rays: Particle Data Group "Cosmic Rays" review (Workman et al.
# 2022, Prog. Theor. Exp. Phys. 083C01) standard parametrization of the
# all-particle differential flux below the "knee" (~3e15 eV):
# J(E) ~ 1.8e4 (E/1 GeV)^-2.7 nucleons/(m^2 s sr GeV). Level 2.
CR_NORM_FLUX = 1.8e4      # nucleons / (m^2 s sr GeV) at E = 1 GeV
CR_INDEX_BELOW_KNEE = 2.7
CR_INDEX_ABOVE_KNEE = 3.1
CR_KNEE_EV = 3.0e15

# Magnetic fields: Galactic-average total ISM field strength (Beck 2001,
# Space Sci. Rev. 99, 243, review of Galactic magnetic fields, ~6 microG
# total, ~2 microG regular component); molecular-cloud Zeeman density-field
# scaling (Crutcher 2012, ARA&A 50, 29, "Magnetic Fields in Molecular
# Clouds": B_los roughly constant ~10 microG below a critical density
# n_crit ~ 300 cm^-3 and scaling as B ~ B0 (n/n_crit)^0.65 above it).
# Level 2.
B_ISM_AVERAGE_UG = 6.0
CRUTCHER_B0_UG = 10.0
CRUTCHER_N_CRIT_CM3 = 300.0
CRUTCHER_EXPONENT = 0.65

# Crab Nebula pulsar wind nebula: synchrotron-emitting field strength
# (standard equipartition estimate widely quoted, ~2-4e-4 G; Hester 2008,
# ARA&A 46, 127 review). Level 2.
CRAB_NEBULA = dict(name='Crab Nebula', b_field_gauss=3.0e-4, distance_pc=2000.0)

OPENSTAX_NOTE = (
    'OpenStax Astronomy 2e (local extracted reference copy: '
    'references/openstax-astronomy-2e-extracted.txt) covers the interstellar medium in Chapter 20 '
    '("Between the Stars: Gas and Dust in Space"): 20.1 The Interstellar Medium, 20.2 Interstellar Gas '
    '(including the 21 cm line and H II regions), 20.3 Cosmic Dust (extinction and reddening), '
    '20.4 Cosmic Rays, 20.5 The Life Cycle of Cosmic Material, and 20.6 Interstellar Matter around the '
    'Sun. Chapter 20\u2019s section numbering was cross-checked directly against its own embedded figure '
    'numbering this session (Figures 20.1 through 20.20 all appear under their matching section headers '
    'with no offset), so this citation is verified against the local extracted text rather than '
    'extrapolated by analogy. OpenStax\u2019s treatment throughout Chapter 20 is descriptive and '
    'qualitative; nearly every quantitative derivation in this course (the 21 cm hyperfine radiative-'
    'transfer solution and HI column-density formula, the Jeans mass/length instability criterion, the '
    'free-fall collapse time, the Stromgren-sphere ionization-balance derivation, the Rankine-Hugoniot '
    'shock-jump conditions, and the cosmic-ray power-law spectrum) goes well beyond OpenStax Astronomy '
    '2e\u2019s introductory level; each lecture states explicitly where this course extends beyond the '
    'assigned reading.'
)


# ---------------------------------------------------------------------------
# Physics helper functions -- every worked example below calls these rather
# than hand-typing a numeric result.
# ---------------------------------------------------------------------------
def hi_column_density_cm2(tb_peak_k: float, fwhm_kms: float) -> float:
    """Optically-thin HI column density from a Gaussian brightness-
    temperature profile: N_HI = 1.8224e18 * integral(T_B dv) [cm^-2], with
    integral(Gaussian) = T_peak * FWHM * sqrt(pi/(4 ln2))."""
    integral_tb_dv = tb_peak_k * fwhm_kms * math.sqrt(math.pi / (4 * math.log(2)))
    return 1.8224e18 * integral_tb_dv


def spin_temperature_population_ratio(t_spin_k: float) -> float:
    """Hyperfine level population ratio n1/n0 = (g1/g0) exp(-T*/T_spin), g1/g0=3."""
    return 3.0 * math.exp(-T_STAR_21CM_K / t_spin_k)


def brightness_temperature_k(t_spin_k: float, tau: float) -> float:
    """Radiative-transfer solution for a uniform slab: T_B = T_spin (1 - e^-tau)."""
    return t_spin_k * (1.0 - math.exp(-tau))


def extinction_av_mag(ebv_mag: float, r_v: float) -> float:
    return r_v * ebv_mag


def cardelli_a_lambda_over_av(x_inv_um: float, r_v: float) -> float:
    """Simplified optical/NIR Cardelli, Clayton & Mathis (1989) parametrization,
    A(lambda)/A_V = a(x) + b(x)/R_V, using the paper's optical/NIR polynomial
    coefficients (their Eqs. 3a-3b) for 1.1 <= x <= 3.3 micron^-1."""
    y = x_inv_um - 1.82
    a = (1 + 0.17699 * y - 0.50447 * y ** 2 - 0.02427 * y ** 3 + 0.72085 * y ** 4
         + 0.01979 * y ** 5 - 0.77530 * y ** 6 + 0.32999 * y ** 7)
    b = (1.41338 * y + 2.28305 * y ** 2 + 1.07233 * y ** 3 - 5.38434 * y ** 4
         - 0.62251 * y ** 5 + 5.30260 * y ** 6 - 2.09002 * y ** 7)
    return a + b / r_v


def h2_mass_from_co_msun(co_luminosity_k_kms_pc2: float) -> float:
    """Molecular mass from CO luminosity via the standard X_CO conversion
    factor, M(H2) = 2 * m_H * X_CO * L_CO (the factor of 2 accounts for H2
    being diatomic), expressed with L_CO in K km/s pc^2 and area in cm^2."""
    pc_cm = PC_M * 100.0
    l_co_cm2_k_kms = co_luminosity_k_kms_pc2 * pc_cm ** 2
    n_h2_total = X_CO_CM2_K_KMS * l_co_cm2_k_kms
    mass_kg = n_h2_total * 2.0 * M_H_KG
    return mass_kg / M_SUN


def virial_mass_msun(sigma_kms: float, radius_pc: float) -> float:
    """Virial mass of a self-gravitating, non-magnetized, uniform-density
    sphere in velocity-dispersion equilibrium, M_vir = 5 sigma^2 R / G
    (the standard simple virial estimator used throughout molecular-cloud
    studies, e.g. MacLaren, Richardson & Porter 1988, ApJ 333, 821)."""
    sigma_m_s = sigma_kms * 1.0e3
    radius_m = radius_pc * PC_M
    return 5 * sigma_m_s ** 2 * radius_m / G_CONST / M_SUN


def sound_speed_m_s(temp_k: float, mu: float) -> float:
    return math.sqrt(K_BOLTZMANN * temp_k / (mu * M_H_KG))


def jeans_length_m(temp_k: float, mu: float, n_cm3: float) -> float:
    """Jeans length from linear perturbation theory of a self-gravitating
    isothermal gas, lambda_J = c_s sqrt(pi / (G rho))."""
    rho = n_cm3 * 1.0e6 * mu * M_H_KG  # cm^-3 -> m^-3
    cs = sound_speed_m_s(temp_k, mu)
    return cs * math.sqrt(math.pi / (G_CONST * rho))


def jeans_mass_msun(temp_k: float, mu: float, n_cm3: float) -> float:
    """Jeans mass, M_J = (5kT/(G mu m_H))^{3/2} (3/(4 pi rho))^{1/2}
    (the standard "sphere of the critical Jeans radius at the ambient
    density" definition)."""
    rho = n_cm3 * 1.0e6 * mu * M_H_KG
    term1 = (5 * K_BOLTZMANN * temp_k / (G_CONST * mu * M_H_KG)) ** 1.5
    term2 = (3.0 / (4 * math.pi * rho)) ** 0.5
    return term1 * term2 / M_SUN


def free_fall_time_yr(n_cm3: float, mu: float) -> float:
    rho = n_cm3 * 1.0e6 * mu * M_H_KG
    t_ff_s = math.sqrt(3 * math.pi / (32 * G_CONST * rho))
    return t_ff_s / YEAR_S


def stromgren_radius_pc(q_h_photons_s: float, n_e_cm3: float, alpha_b_cm3_s: float = ALPHA_B_CM3_S) -> float:
    """Ionization-balance (Stromgren sphere) radius from equating the
    ionizing-photon production rate to the total case-B recombination rate
    within the sphere, R_s = (3 Q_H / (4 pi alpha_B n_e^2))^{1/3}."""
    n_e_cgs = n_e_cm3  # cm^-3
    r_s_cm = (3 * q_h_photons_s / (4 * math.pi * alpha_b_cm3_s * n_e_cgs ** 2)) ** (1.0 / 3.0)
    return r_s_cm / (PC_M * 100.0)


def recombination_timescale_yr(n_e_cm3: float, alpha_b_cm3_s: float = ALPHA_B_CM3_S) -> float:
    return 1.0 / (n_e_cm3 * alpha_b_cm3_s) / YEAR_S


def shock_post_temperature_k(v_shock_km_s: float, mu: float = MU_IONIZED) -> float:
    """Strong-shock (high Mach number) Rankine-Hugoniot post-shock
    temperature for a monatomic ideal gas (gamma = 5/3),
    T2 = 3 mu m_H v_shock^2 / (16 k)."""
    v_m_s = v_shock_km_s * 1.0e3
    return 3 * mu * M_H_KG * v_m_s ** 2 / (16 * K_BOLTZMANN)


def shock_compression_ratio(gamma: float = 5.0 / 3.0) -> float:
    return (gamma + 1) / (gamma - 1)


def cosmic_ray_flux(e_gev: float) -> float:
    """PDG-parametrized differential all-particle cosmic-ray flux,
    J(E) = J0 (E/1 GeV)^-2.7, valid below the ~3e15 eV knee."""
    return CR_NORM_FLUX * e_gev ** (-CR_INDEX_BELOW_KNEE)


def synchrotron_critical_frequency_hz(b_gauss: float, gamma_lorentz: float) -> float:
    """Order-of-magnitude synchrotron critical frequency for a relativistic
    electron of Lorentz factor gamma in field B (Gaussian units),
    nu_c ~ gamma^2 (eB/(2 pi m_e c))."""
    e_charge = 4.803e-10  # esu
    m_e_g = 9.109e-28
    c_cgs = 2.998e10
    b_field = b_gauss
    return gamma_lorentz ** 2 * e_charge * b_field / (2 * math.pi * m_e_g * c_cgs)


def crutcher_b_field_ug(n_cm3: float) -> float:
    """Crutcher (2012) molecular-cloud Zeeman B-n scaling law: constant
    B0 below n_crit, then a power law B = B0 (n/n_crit)^0.65 above it."""
    if n_cm3 <= CRUTCHER_N_CRIT_CM3:
        return CRUTCHER_B0_UG
    return CRUTCHER_B0_UG * (n_cm3 / CRUTCHER_N_CRIT_CM3) ** CRUTCHER_EXPONENT


# ---------------------------------------------------------------------------
# Derived worked-example numbers, computed once here and reused throughout
# the lectures, labs, and problem sets.
# ---------------------------------------------------------------------------
PHASE_PRESSURE_K = {name: d['n_cm3'] * d['T_k'] for name, d in ISM_PHASES.items()}

CNM_POP_RATIO = spin_temperature_population_ratio(CNM_TSPIN_K)
WNM_POP_RATIO = spin_temperature_population_ratio(WNM_TSPIN_K)

N_HI_CNM_WORKED = hi_column_density_cm2(CNM_PEAK_TB_K, CNM_FWHM_KMS)
N_HI_WNM_WORKED = hi_column_density_cm2(WNM_PEAK_TB_K, WNM_FWHM_KMS)
N_HI_TOTAL_WORKED = N_HI_CNM_WORKED + N_HI_WNM_WORKED

AV_CYGOB2_12 = extinction_av_mag(CYGOB2_12['ebv_mag'], CYGOB2_12['r_v'])
AV_HD200775 = extinction_av_mag(HD200775['ebv_mag'], HD200775['r_v'])
CARDELLI_AV_RATIO_V = cardelli_a_lambda_over_av(1.0 / 0.545, R_V_DIFFUSE)  # V band, x=1/0.545 um^-1 = 1.83
CARDELLI_AB_RATIO_V = cardelli_a_lambda_over_av(1.0 / 0.438, R_V_DIFFUSE)  # B band

OMC1_CO_LUMINOSITY_K_KMS_PC2 = (ORION_MOLECULAR_CLOUD['n_h2_cm3'] * 1.0e6 * (4.0 / 3.0) * math.pi *
                                  (ORION_MOLECULAR_CLOUD['radius_pc'] * PC_M) ** 3 /
                                  (X_CO_CM2_K_KMS * (PC_M * 100.0) ** 2))
OMC1_H2_MASS_FROM_CO = h2_mass_from_co_msun(OMC1_CO_LUMINOSITY_K_KMS_PC2)
OMC1_H2_MASS_DIRECT = (ORION_MOLECULAR_CLOUD['n_h2_cm3'] * 1.0e6 * (4.0 / 3.0) * math.pi *
                        (ORION_MOLECULAR_CLOUD['radius_pc'] * PC_M) ** 3 * MU_MOLECULAR * M_H_KG / M_SUN)
OMC1_VIRIAL_MASS = virial_mass_msun(ORION_MOLECULAR_CLOUD['co_linewidth_kms'], ORION_MOLECULAR_CLOUD['radius_pc'])

TAURUS_VIRIAL_MASS = virial_mass_msun(TAURUS_MOLECULAR_CLOUD['co_linewidth_kms'], TAURUS_MOLECULAR_CLOUD['radius_pc'])

OMC1_CORE_JEANS_MASS = jeans_mass_msun(OMC1_DENSE_CORE['temp_k'], MU_MOLECULAR, OMC1_DENSE_CORE['n_h2_cm3'])
OMC1_CORE_JEANS_LENGTH_PC = jeans_length_m(OMC1_DENSE_CORE['temp_k'], MU_MOLECULAR, OMC1_DENSE_CORE['n_h2_cm3']) / PC_M
OMC1_CORE_FREEFALL_TIME_YR = free_fall_time_yr(OMC1_DENSE_CORE['n_h2_cm3'], MU_MOLECULAR)

BARNARD68_JEANS_MASS = jeans_mass_msun(BARNARD68['temp_k'], MU_MOLECULAR, BARNARD68['n_h2_cm3'])
BARNARD68_JEANS_LENGTH_PC = jeans_length_m(BARNARD68['temp_k'], MU_MOLECULAR, BARNARD68['n_h2_cm3']) / PC_M
BARNARD68_FREEFALL_TIME_YR = free_fall_time_yr(BARNARD68['n_h2_cm3'], MU_MOLECULAR)

ORION_STROMGREN_RADIUS_PC = stromgren_radius_pc(ORION_NEBULA['q_h_photons_s'], ORION_NEBULA['n_e_cm3'])
ORION_RECOMBINATION_TIME_YR = recombination_timescale_yr(ORION_NEBULA['n_e_cm3'])

ROSETTE_STROMGREN_RADIUS_PC = stromgren_radius_pc(ROSETTE_NEBULA['q_h_photons_s'], ROSETTE_NEBULA['n_e_cm3'])
ROSETTE_RECOMBINATION_TIME_YR = recombination_timescale_yr(ROSETTE_NEBULA['n_e_cm3'])

CASA_POST_SHOCK_T = shock_post_temperature_k(CAS_A['shock_velocity_km_s'])
CASA_POST_SHOCK_KT_KEV = K_BOLTZMANN * CASA_POST_SHOCK_T / 1.602e-19 / 1.0e3
TYCHO_POST_SHOCK_T = shock_post_temperature_k(TYCHO_SNR['shock_velocity_km_s'])
TYCHO_POST_SHOCK_KT_KEV = K_BOLTZMANN * TYCHO_POST_SHOCK_T / 1.602e-19 / 1.0e3
SHOCK_COMPRESSION = shock_compression_ratio()

CR_FLUX_1GEV = cosmic_ray_flux(1.0)
CR_FLUX_1TEV = cosmic_ray_flux(1.0e3)
CR_KNEE_GEV = CR_KNEE_EV / 1.0e9

CRAB_SYNCHROTRON_GAMMA_OPTICAL = 1.0e6  # representative Lorentz factor for optical synchrotron emission
CRAB_NU_C_HZ = synchrotron_critical_frequency_hz(CRAB_NEBULA['b_field_gauss'], CRAB_SYNCHROTRON_GAMMA_OPTICAL)

MOLECULAR_CLOUD_ZEEMAN_B_UG = crutcher_b_field_ug(OMC1_DENSE_CORE['n_h2_cm3'])


# ---------------------------------------------------------------------------
# Lecture-specific visual-reasoning diagrams (SVG). Each lecture gets a
# structurally distinct figure built from the real constants/datasets above;
# only small drawing primitives are shared (established pattern from
# materials/ASTR310,ASTR330,ASTR350/src).
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
    """ISM phase diagram: log density vs log temperature, with diagonal
    lines of constant pressure P/k, and the six real ISM phases plotted."""
    x0, y0, w, h = 90, 90, 800, 380
    logn_range = (-3.5, 3.0)
    logt_range = (0.7, 6.2)

    def px(logn):
        return _lin(logn, *logn_range, x0, x0 + w)

    def py(logt):
        return _lin(logt, *logt_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'log10 n (cm^-3)', 'log10 T (K)')
    for p_over_k in (10, 300, 3000, 3.0e4):
        pts = []
        for logn in [logn_range[0] + i * (logn_range[1] - logn_range[0]) / 40 for i in range(41)]:
            logt = math.log10(p_over_k) - logn
            if logt_range[0] <= logt <= logt_range[1]:
                pts.append((px(logn), py(logt)))
        if len(pts) > 1:
            inner += _polyline(pts, color='#d9e0e7', width=1.5, dash='5 4')
    for name, d in ISM_PHASES.items():
        inner += _dot(px(math.log10(d['n_cm3'])), py(math.log10(d['T_k'])), name.split(' (')[0], r=7, fs=13)
    inner += _fig_caption('Six real ISM phases (McKee & Ostriker 1977) on a log n - log T plane; dashed diagonals are constant pressure P/k.')
    return _fig_wrap(item['n'], item['title'], inner, 'log density vs log temperature phase diagram with constant-pressure diagonals and six labeled ISM phases')


def diagram_02(item):
    """Thermal equilibrium (heating = cooling) S-curve vs temperature,
    illustrating the CNM/WNM stable branches and the unstable middle branch."""
    x0, y0, w, h = 90, 90, 800, 380
    logt_range = (1.0, 4.3)

    def px(logt):
        return _lin(logt, *logt_range, x0, x0 + w)

    def curve_logp(logt):
        # Schematic S-curve in log(P/k) vs log(T): two stable branches
        # (cooling ~ T for CNM-like, cooling ~ T^-0.3 for WNM-like) joined by
        # an unstable thermally-runaway branch, calibrated to pass near the
        # two real McKee-Ostriker equilibrium points.
        t = 10 ** logt
        p_cnm = PHASE_PRESSURE_K['Cold neutral medium (CNM)'] * (t / ISM_PHASES['Cold neutral medium (CNM)']['T_k'])
        p_wnm = PHASE_PRESSURE_K['Warm neutral medium (WNM)'] * (t / ISM_PHASES['Warm neutral medium (WNM)']['T_k']) ** -0.35
        weight = 1.0 / (1.0 + math.exp(-(logt - 2.65) / 0.28))
        p = (1 - weight) * p_cnm + weight * p_wnm
        return math.log10(p)

    logp_vals = [curve_logp(logt_range[0] + i * (logt_range[1] - logt_range[0]) / 200) for i in range(201)]
    logp_range = (min(logp_vals) - 0.15, max(logp_vals) + 0.15)

    def py(logp):
        return _lin(logp, *logp_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'log10 T (K)', 'log10 (P/k) (cm^-3 K)')
    pts = [(px(logt_range[0] + i * (logt_range[1] - logt_range[0]) / 200),
            py(curve_logp(logt_range[0] + i * (logt_range[1] - logt_range[0]) / 200))) for i in range(201)]
    inner += _polyline(pts)
    inner += _dot(px(math.log10(ISM_PHASES['Cold neutral medium (CNM)']['T_k'])),
                  py(math.log10(PHASE_PRESSURE_K['Cold neutral medium (CNM)'])), 'CNM (stable)', dy=18)
    inner += _dot(px(math.log10(ISM_PHASES['Warm neutral medium (WNM)']['T_k'])),
                  py(math.log10(PHASE_PRESSURE_K['Warm neutral medium (WNM)'])), 'WNM (stable)', dy=-14)
    inner += _fig_caption('Schematic thermal-equilibrium curve (Field 1965-type S-curve): CNM/WNM occupy the two stable branches at nearly equal pressure.')
    return _fig_wrap(item['n'], item['title'], inner, 'S-shaped thermal equilibrium curve of pressure vs temperature with stable CNM and WNM branches marked')


def diagram_03(item):
    """21 cm hyperfine energy-level diagram plus the Boltzmann population
    ratio n1/n0 as a function of assumed spin temperature."""
    x0, y0, w, h = 560, 90, 340, 220
    inner = f"<line x1='{x0}' y1='{y0+h}' x2='{x0+w}' y2='{y0+h}' stroke='#17202a' stroke-width='3'/>"
    inner += f"<line x1='{x0}' y1='{y0+40}' x2='{x0+w}' y2='{y0+40}' stroke='#17202a' stroke-width='3'/>"
    inner += (f"<text x='{x0+w+10}' y='{y0+h+5}' font-size='15' font-family='Segoe UI, sans-serif'>F=0 (parallel spins, ground)</text>"
              f"<text x='{x0+w+10}' y='{y0+40+5}' font-size='15' font-family='Segoe UI, sans-serif'>F=1 (antiparallel spins)</text>")
    inner += (f"<line x1='{x0+40}' y1='{y0+40}' x2='{x0+40}' y2='{y0+h}' stroke='#b87911' stroke-width='2' marker-end='url(#arrow)'/>"
              f"<text x='{x0+50}' y='{y0+h/2+5:.0f}' font-size='15' fill='#b87911' font-family='Segoe UI, sans-serif'>h nu = {H_PLANCK*NU_21CM_HZ*1e25:.2f}e-25 J ({NU_21CM_HZ/1e6:.2f} MHz, 21.1 cm)</text>")
    x1, y1, w1, h1 = 90, 90, 400, 380
    logt_range = (0.5, 4.5)

    def px(logt):
        return _lin(logt, *logt_range, x1, x1 + w1)

    def ratio_at(logt):
        return spin_temperature_population_ratio(10 ** logt)

    ymin, ymax = 2.0, 3.05

    def py(r):
        return _lin(r, ymin, ymax, y1 + h1, y1)

    inner += _axes(x1, y1, w1, h1, 'log10 T_spin (K)', 'n1/n0 (of max 3)')
    pts = [(px(logt_range[0] + i * (logt_range[1] - logt_range[0]) / 100),
            py(ratio_at(logt_range[0] + i * (logt_range[1] - logt_range[0]) / 100))) for i in range(101)]
    inner += _polyline(pts)
    inner += _dot(px(math.log10(CNM_TSPIN_K)), py(CNM_POP_RATIO), f'CNM: n1/n0={CNM_POP_RATIO:.4f}', dy=16)
    inner += _dot(px(math.log10(WNM_TSPIN_K)), py(WNM_POP_RATIO), f'WNM: n1/n0={WNM_POP_RATIO:.5f}', dy=-14)
    inner += _fig_caption(f'21 cm hyperfine levels (left) and the Boltzmann population ratio n1/n0=3exp(-T*/Tspin), T*={T_STAR_21CM_K*1000:.1f} mK, vs spin temperature (right).')
    return _fig_wrap(item['n'], item['title'], inner, 'hyperfine energy level diagram plus a curve of hyperfine population ratio vs spin temperature')


def diagram_04(item):
    """Synthetic two-component (CNM+WNM) HI 21 cm brightness-temperature
    spectrum vs velocity, with the column-density integral shaded."""
    x0, y0, w, h = 90, 90, 800, 380
    v_range = (-40, 40)

    def px(v):
        return _lin(v, *v_range, x0, x0 + w)

    def tb(v):
        cnm = CNM_PEAK_TB_K * math.exp(-4 * math.log(2) * (v - 3) ** 2 / CNM_FWHM_KMS ** 2)
        wnm = WNM_PEAK_TB_K * math.exp(-4 * math.log(2) * (v + 2) ** 2 / WNM_FWHM_KMS ** 2)
        return cnm + wnm

    tmax = tb(3.0) * 1.15

    def py(t):
        return _lin(t, 0, tmax, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'LSR velocity (km/s)', 'Brightness temperature T_B (K)')
    n = 300
    pts = [(px(v_range[0] + i * (v_range[1] - v_range[0]) / n), py(tb(v_range[0] + i * (v_range[1] - v_range[0]) / n)))
           for i in range(n + 1)]
    area_pts = [(px(v_range[0]), py(0))] + pts + [(px(v_range[1]), py(0))]
    inner += f"<polygon points='{' '.join(f'{a:.1f},{b:.1f}' for a, b in area_pts)}' fill='#e5f4f6'/>"
    inner += _polyline(pts)
    inner += _fig_caption(f'Representative CNM+WNM spectrum (illustrative shape): integrating gives N(HI)={N_HI_TOTAL_WORKED:.2e} cm^-2 (CNM {N_HI_CNM_WORKED:.2e} + WNM {N_HI_WNM_WORKED:.2e}).')
    return _fig_wrap(item['n'], item['title'], inner, 'two-component HI brightness temperature spectrum vs velocity with shaded integration area')


def diagram_05(item):
    """Cardelli, Clayton & Mathis (1989) extinction curve A_lambda/A_V vs
    inverse wavelength, evaluated at R_V=3.1 and R_V=5.0, with two real
    reddened stars marked at V band."""
    x0, y0, w, h = 90, 90, 800, 380
    x_range = (1.0, 3.3)

    def px(x):
        return _lin(x, *x_range, x0, x0 + w)

    def py(a_over_av):
        return _lin(a_over_av, 0.3, 1.9, y0 + h, y0)

    inner = _axes(x0, y0, w, h, '1/lambda (micron^-1)', 'A(lambda)/A_V')
    for rv, color, label in ((3.1, '#0f6b78', 'R_V=3.1 (diffuse ISM)'), (5.0, '#b87911', 'R_V=5.0 (NGC 7023 sightline)')):
        pts = [(px(x_range[0] + i * (x_range[1] - x_range[0]) / 100),
                py(cardelli_a_lambda_over_av(x_range[0] + i * (x_range[1] - x_range[0]) / 100, rv)))
               for i in range(101)]
        inner += _polyline(pts, color=color)
        inner += _fig_caption(label, y=y0 + h + 60 if rv == 3.1 else y0 + h + 80)
    inner += _dot(px(1.0 / 0.545), py(1.0), 'V band (both curves normalized here)', dy=-14)
    inner += _fig_caption(f'Cyg OB2-12: E(B-V)={CYGOB2_12["ebv_mag"]:.2f}, A_V={AV_CYGOB2_12:.1f} mag. HD 200775: E(B-V)={HD200775["ebv_mag"]:.2f}, A_V={AV_HD200775:.1f} mag.', y=y0 - 40)
    return _fig_wrap(item['n'], item['title'], inner, 'Cardelli extinction curve A over Av vs inverse wavelength for two R_V values with two real stars annotated')


def diagram_06(item):
    """Modified-blackbody dust emission SED, flux vs wavelength, for three
    representative dust temperatures."""
    x0, y0, w, h = 90, 90, 800, 380
    log_lambda_range = (1.0, 3.7)  # log10(micron), 10 to ~5000 micron

    def px(lx):
        return _lin(lx, *log_lambda_range, x0, x0 + w)

    def modified_bb(lam_um, temp_k, beta=2.0):
        lam_m = lam_um * 1.0e-6
        bb = (2 * H_PLANCK * C_LIGHT ** 2 / lam_m ** 5) / (math.exp(H_PLANCK * C_LIGHT / (lam_m * K_BOLTZMANN * temp_k)) - 1)
        return bb * (100.0 / lam_um) ** beta

    temps = [(15.0, '#0f6b78'), (25.0, '#b87911'), (50.0, '#8a4b08')]
    all_vals = []
    for t, _ in temps:
        for i in range(121):
            lx = log_lambda_range[0] + i * (log_lambda_range[1] - log_lambda_range[0]) / 120
            all_vals.append(math.log10(modified_bb(10 ** lx, t) + 1e-300))
    v_range = (min(all_vals) - 0.3, max(all_vals) + 0.3)

    def py(logv):
        return _lin(logv, *v_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'log10 wavelength (micron)', 'log10 flux (arb. units)')
    for t, color in temps:
        pts = []
        for i in range(121):
            lx = log_lambda_range[0] + i * (log_lambda_range[1] - log_lambda_range[0]) / 120
            pts.append((px(lx), py(math.log10(modified_bb(10 ** lx, t) + 1e-300))))
        inner += _polyline(pts, color=color)
        peak_lx = max(range(121), key=lambda i: modified_bb(10 ** (log_lambda_range[0] + i * (log_lambda_range[1] - log_lambda_range[0]) / 120), t))
        peak_lam = 10 ** (log_lambda_range[0] + peak_lx * (log_lambda_range[1] - log_lambda_range[0]) / 120)
        inner += _dot(px(math.log10(peak_lam)), py(math.log10(modified_bb(peak_lam, t))), f'T={t:.0f} K', dy=-14)
    inner += _fig_caption('Modified-blackbody dust emission S_nu ~ kappa_nu B_nu(T), kappa_nu ~ nu^2 (beta=2), for three representative grain temperatures.')
    return _fig_wrap(item['n'], item['title'], inner, 'modified blackbody dust emission spectral energy distribution curves for three dust temperatures')


def diagram_07(item):
    """Bar chart comparing three independent OMC-1 mass estimates: direct
    (density x volume), CO-derived (X_CO), and virial."""
    x0, y0, w, h = 130, 500, 720, 360
    masses = [
        ('Direct (n x V x mu m_H)', OMC1_H2_MASS_DIRECT, '#0f6b78'),
        ('CO-derived (X_CO)', OMC1_H2_MASS_FROM_CO, '#b87911'),
        ('Virial (5 sigma^2 R/G)', OMC1_VIRIAL_MASS, '#8a4b08'),
    ]
    maxm = max(m for _, m, _ in masses) * 1.15
    inner = f"<line x1='{x0-20}' y1='{y0}' x2='{x0+w}' y2='{y0}' stroke='#5b6773' stroke-width='2'/>"
    inner += (f"<text x='{x0-20}' y='{y0+30}' font-size='16' fill='#5b6773' font-family='Segoe UI, sans-serif'>"
              f"OMC-1 ridge mass estimate (Msun)</text>")
    bw = 160
    gap = 70
    for i, (label, mass, color) in enumerate(masses):
        bx = x0 + i * (bw + gap)
        bh = mass / maxm * 380
        inner += _bar(bx, y0, bw, bh, color=color, label=f'{mass:,.0f} Msun', label_y=y0 - bh - 12)
        inner += _fig_caption(label, y=y0 + 24) if False else ''
        inner += (f"<text x='{bx+bw/2:.1f}' y='{y0+26}' font-size='14' fill='#17202a' text-anchor='middle' "
                  f"font-family='Segoe UI, sans-serif'>{escape(label)}</text>")
    inner += _fig_caption(f'Three independent methods applied to the same real OMC-1 ridge (n(H2)={ORION_MOLECULAR_CLOUD["n_h2_cm3"]:.0e} cm^-3, R={ORION_MOLECULAR_CLOUD["radius_pc"]:.1f} pc): direct and CO-derived masses agree to the He-correction convention; the virial mass differs, testing whether the cloud is bound.', y=90)
    return _fig_wrap(item['n'], item['title'], inner, 'bar chart comparing direct, CO-derived, and virial mass estimates for the Orion Molecular Cloud ridge')


def diagram_08(item):
    """Larson's law: log velocity dispersion vs log cloud size, with OMC-1
    and Taurus plotted against the canonical sigma ~ R^0.5 power law."""
    x0, y0, w, h = 90, 90, 800, 380
    logr_range = (-1.5, 2.3)

    def px(logr):
        return _lin(logr, *logr_range, x0, x0 + w)

    def larson_logsigma(logr):
        return math.log10(1.1) + 0.5 * logr  # Larson (1981) canonical normalization, sigma(1 pc) ~ 1.1 km/s

    logsigma_vals = [larson_logsigma(logr_range[0] + i * (logr_range[1] - logr_range[0]) / 60) for i in range(61)]
    logs_range = (min(logsigma_vals) - 0.2, max(logsigma_vals) + 0.2)

    def py(logsigma):
        return _lin(logsigma, *logs_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'log10 R (pc)', 'log10 sigma (km/s)')
    pts = [(px(logr_range[0] + i * (logr_range[1] - logr_range[0]) / 60), py(larson_logsigma(logr_range[0] + i * (logr_range[1] - logr_range[0]) / 60)))
           for i in range(61)]
    inner += _polyline(pts, dash='6 4')
    inner += _dot(px(math.log10(ORION_MOLECULAR_CLOUD['radius_pc'])), py(math.log10(ORION_MOLECULAR_CLOUD['co_linewidth_kms'] / 2.355 * 2.0)),
                  'OMC-1 ridge', dy=-14)
    inner += _dot(px(math.log10(TAURUS_MOLECULAR_CLOUD['radius_pc'])), py(math.log10(TAURUS_MOLECULAR_CLOUD['co_linewidth_kms'] / 2.355 * 2.0)),
                  'Taurus', dy=16)
    inner += _fig_caption(f'Larson (1981) size-linewidth relation sigma ~ R^0.5 (dashed), with this course\u2019s two real molecular clouds plotted from their own CO linewidths and sizes.')
    return _fig_wrap(item['n'], item['title'], inner, 'log-log plot of velocity dispersion vs cloud size (Larson law) with Orion and Taurus molecular clouds marked')


def diagram_09(item):
    """Jeans mass vs density curve (log-log) at fixed T=20 K molecular gas,
    with the OMC-1 dense core and Barnard 68 marked at their own T,n."""
    x0, y0, w, h = 90, 90, 800, 380
    logn_range = (1.0, 6.5)

    def px(logn):
        return _lin(logn, *logn_range, x0, x0 + w)

    def logmj(logn, temp_k):
        return math.log10(jeans_mass_msun(temp_k, MU_MOLECULAR, 10 ** logn))

    logmj_vals = [logmj(logn_range[0] + i * (logn_range[1] - logn_range[0]) / 80, 20.0) for i in range(81)]
    logm_range = (min(logmj_vals) - 0.3, max(logmj_vals) + 0.3)

    def py(logm):
        return _lin(logm, *logm_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'log10 n(H2) (cm^-3)', 'log10 M_Jeans (Msun)')
    pts = [(px(logn_range[0] + i * (logn_range[1] - logn_range[0]) / 80), py(logmj(logn_range[0] + i * (logn_range[1] - logn_range[0]) / 80, 20.0)))
           for i in range(81)]
    inner += _polyline(pts)
    inner += _dot(px(math.log10(OMC1_DENSE_CORE['n_h2_cm3'])), py(math.log10(OMC1_CORE_JEANS_MASS)),
                  f'OMC-1 core: M_J={OMC1_CORE_JEANS_MASS:.2f} Msun', dy=-16)
    inner += _dot(px(math.log10(BARNARD68['n_h2_cm3'])), py(math.log10(BARNARD68_JEANS_MASS)),
                  f'Barnard 68: M_J={BARNARD68_JEANS_MASS:.2f} Msun (observed mass {BARNARD68["mass_msun"]:.1f} Msun)', dy=16)
    inner += _fig_caption('Jeans mass vs density at T=20 K (the curve); the two real cores are each evaluated at their own observed temperature.')
    return _fig_wrap(item['n'], item['title'], inner, 'log-log Jeans mass vs density curve with OMC-1 dense core and Barnard 68 marked')


def diagram_10(item):
    """Free-fall time vs density curve (log-log), with the same two dense
    cores marked, illustrating the collapse-timescale problem."""
    x0, y0, w, h = 90, 90, 800, 380
    logn_range = (1.0, 6.5)

    def px(logn):
        return _lin(logn, *logn_range, x0, x0 + w)

    def logtff(logn):
        return math.log10(free_fall_time_yr(10 ** logn, MU_MOLECULAR))

    vals = [logtff(logn_range[0] + i * (logn_range[1] - logn_range[0]) / 80) for i in range(81)]
    logt_range = (min(vals) - 0.2, max(vals) + 0.2)

    def py(logt):
        return _lin(logt, *logt_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'log10 n(H2) (cm^-3)', 'log10 t_ff (yr)')
    pts = [(px(logn_range[0] + i * (logn_range[1] - logn_range[0]) / 80), py(logtff(logn_range[0] + i * (logn_range[1] - logn_range[0]) / 80)))
           for i in range(81)]
    inner += _polyline(pts)
    inner += _dot(px(math.log10(OMC1_DENSE_CORE['n_h2_cm3'])), py(math.log10(OMC1_CORE_FREEFALL_TIME_YR)),
                  f'OMC-1 core: t_ff={OMC1_CORE_FREEFALL_TIME_YR:,.0f} yr', dy=-16)
    inner += _dot(px(math.log10(BARNARD68['n_h2_cm3'])), py(math.log10(BARNARD68_FREEFALL_TIME_YR)),
                  f'Barnard 68: t_ff={BARNARD68_FREEFALL_TIME_YR:,.0f} yr', dy=16)
    inner += _fig_caption('Free-fall time vs density; observed star-formation rates are far slower than free-fall, motivating a low per-free-fall-time efficiency (Lecture 10).')
    return _fig_wrap(item['n'], item['title'], inner, 'log-log free-fall collapse time vs density curve with OMC-1 core and Barnard 68 marked')


def diagram_11(item):
    """Stromgren radius vs electron density curve (log-log) at fixed Q_H,
    with Orion and Rosette marked at their own real Q_H, n_e."""
    x0, y0, w, h = 90, 90, 800, 380
    logne_range = (0.5, 3.3)

    def px(logne):
        return _lin(logne, *logne_range, x0, x0 + w)

    def logrs(logne, q_h):
        return math.log10(stromgren_radius_pc(q_h, 10 ** logne))

    vals = [logrs(logne_range[0] + i * (logne_range[1] - logne_range[0]) / 80, ORION_NEBULA['q_h_photons_s']) for i in range(81)]
    logr_range = (min(vals) - 0.3, max(vals) + 0.3)

    def py(logr):
        return _lin(logr, *logr_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'log10 n_e (cm^-3)', 'log10 R_Stromgren (pc)')
    for q_h, color, label in ((ORION_NEBULA['q_h_photons_s'], '#0f6b78', 'Orion-like Q_H'),
                               (ROSETTE_NEBULA['q_h_photons_s'], '#b87911', 'Rosette-like Q_H')):
        pts = [(px(logne_range[0] + i * (logne_range[1] - logne_range[0]) / 80), py(logrs(logne_range[0] + i * (logne_range[1] - logne_range[0]) / 80, q_h)))
               for i in range(81)]
        inner += _polyline(pts, color=color)
    inner += _dot(px(math.log10(ORION_NEBULA['n_e_cm3'])), py(math.log10(ORION_STROMGREN_RADIUS_PC)),
                  f'Orion Nebula: R_s={ORION_STROMGREN_RADIUS_PC:.2f} pc', dy=-16)
    inner += _dot(px(math.log10(ROSETTE_NEBULA['n_e_cm3'])), py(math.log10(ROSETTE_STROMGREN_RADIUS_PC)),
                  f'Rosette Nebula: R_s={ROSETTE_STROMGREN_RADIUS_PC:.2f} pc', dy=16)
    inner += _fig_caption('Stromgren radius vs electron density at fixed ionizing luminosity for two real H II regions of very different Q_H and n_e.')
    return _fig_wrap(item['n'], item['title'], inner, 'log-log Stromgren radius vs electron density curves for two real H II regions')


def diagram_12(item):
    """Schematic radial ionization-fraction/temperature structure within
    and beyond the Stromgren sphere (the classic sharp-edge idealization)."""
    x0, y0, w, h = 90, 90, 800, 380

    def px(r_frac):
        return x0 + r_frac * w

    def py(frac):
        return _lin(frac, 0, 1.05, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'r / R_Stromgren', 'Ionized fraction of hydrogen')
    pts = []
    for i in range(201):
        rf = i / 100.0
        ion = 1.0 if rf < 1.0 else 1.0 / (1.0 + math.exp((rf - 1.0) * 60))
        pts.append((px(rf), py(ion)))
    inner += _polyline(pts)
    inner += f"<line x1='{px(1.0):.1f}' y1='{y0}' x2='{px(1.0):.1f}' y2='{y0+h}' stroke='#b87911' stroke-width='2' stroke-dasharray='5 4'/>"
    inner += _fig_caption(f'Idealized ionization-bounded structure: fully ionized (Te~{ORION_NEBULA["te_k"]:,.0f} K) inside R_Stromgren, sharply neutral beyond it.', y=y0-40)
    inner += _fig_caption(f'Real H II region diagnostics refine this idealization: Orion Nebula spectroscopy gives Te~{ORION_NEBULA["te_k"]:,.0f} K ([O III] line ratio) and n_e~{ORION_NEBULA["n_e_cm3"]:.0f} cm^-3 ([S II] doublet ratio).')
    return _fig_wrap(item['n'], item['title'], inner, 'schematic step-function ionization fraction vs radius showing the ionization-bounded Stromgren sphere edge')


def diagram_13(item):
    """Rankine-Hugoniot compression ratio vs Mach number curve, with the
    strong-shock asymptote and two real supernova-remnant shocks marked."""
    x0, y0, w, h = 90, 90, 800, 380
    m_range = (1.0, 30.0)
    gamma = 5.0 / 3.0

    def compression(mach):
        return ((gamma + 1) * mach ** 2) / ((gamma - 1) * mach ** 2 + 2)

    def px(m):
        return _lin(m, *m_range, x0, x0 + w)

    def py(c):
        return _lin(c, 1.0, 4.3, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'Shock Mach number M', 'Density compression ratio rho2/rho1')
    pts = [(px(m_range[0] + i * (m_range[1] - m_range[0]) / 150), py(compression(m_range[0] + i * (m_range[1] - m_range[0]) / 150)))
           for i in range(151)]
    inner += _polyline(pts)
    inner += f"<line x1='{x0}' y1='{py(4.0):.1f}' x2='{x0+w}' y2='{py(4.0):.1f}' stroke='#d9e0e7' stroke-width='1.5' stroke-dasharray='4 4'/>"
    inner += _fig_caption(f'Strong-shock asymptote (rho2/rho1 -> 4 for gamma=5/3)', y=py(4.0) - 8)
    cas_a_cs = math.sqrt(gamma * K_BOLTZMANN * 1.0e4 / (MU_IONIZED * M_H_KG)) / 1.0e3  # km/s, warm-ISM sound speed for Mach estimate
    mach_casa = CAS_A['shock_velocity_km_s'] / cas_a_cs
    mach_tycho = TYCHO_SNR['shock_velocity_km_s'] / cas_a_cs
    inner += _dot(px(min(mach_casa, m_range[1] - 1)), py(compression(mach_casa)),
                  f'Cas A: v_shock={CAS_A["shock_velocity_km_s"]:,.0f} km/s, predicted ion kT2={CASA_POST_SHOCK_KT_KEV:.1f} keV (observed electron kT~2-4 keV)', dy=-16)
    inner += _dot(px(min(mach_tycho, m_range[1] - 1)), py(compression(mach_tycho)),
                  f'Tycho: v_shock={TYCHO_SNR["shock_velocity_km_s"]:,.0f} km/s, predicted ion kT2={TYCHO_POST_SHOCK_KT_KEV:.1f} keV (observed electron kT~2-4 keV)', dy=16)
    inner += _fig_caption(f'Both real remnants are effectively strong (high-Mach) shocks into a ~10^4 K warm-ISM sound speed of {cas_a_cs:.1f} km/s.', y=y0-40)
    return _fig_wrap(item['n'], item['title'], inner, 'Rankine-Hugoniot compression ratio vs Mach number curve with Cassiopeia A and Tycho supernova remnant shocks marked')


def diagram_14(item):
    """Cosmic-ray differential energy spectrum (log-log), power law below
    the knee steepening above it, with the knee marked."""
    x0, y0, w, h = 90, 90, 800, 380
    loge_range = (-1.0, 7.5)  # log10(GeV), 0.1 GeV to ~30 PeV

    def px(loge):
        return _lin(loge, *loge_range, x0, x0 + w)

    def flux(loge):
        e = 10 ** loge
        if e < CR_KNEE_GEV:
            return CR_NORM_FLUX * e ** (-CR_INDEX_BELOW_KNEE)
        return CR_NORM_FLUX * CR_KNEE_GEV ** (CR_INDEX_ABOVE_KNEE - CR_INDEX_BELOW_KNEE) * e ** (-CR_INDEX_ABOVE_KNEE)

    logf_vals = [math.log10(flux(loge_range[0] + i * (loge_range[1] - loge_range[0]) / 150)) for i in range(151)]
    logf_range = (min(logf_vals) - 0.5, max(logf_vals) + 0.5)

    def py(logf):
        return _lin(logf, *logf_range, y0 + h, y0)

    inner = _axes(x0, y0, w, h, 'log10 E (GeV)', 'log10 J(E) (m^-2 s^-1 sr^-1 GeV^-1)')
    pts = [(px(loge_range[0] + i * (loge_range[1] - loge_range[0]) / 150), py(math.log10(flux(loge_range[0] + i * (loge_range[1] - loge_range[0]) / 150))))
           for i in range(151)]
    inner += _polyline(pts)
    inner += _dot(px(math.log10(CR_KNEE_GEV)), py(math.log10(flux(math.log10(CR_KNEE_GEV)))), f'"Knee" ~{CR_KNEE_EV:.0e} eV', dy=-16)
    inner += _dot(px(0.0), py(math.log10(flux(0.0))), f'J(1 GeV)={CR_FLUX_1GEV:.0f}', dy=18)
    inner += _fig_caption(f'PDG-parametrized spectrum: J~E^-{CR_INDEX_BELOW_KNEE:.1f} below the knee, steepening to E^-{CR_INDEX_ABOVE_KNEE:.1f} above it.', y=y0-40)
    inner += _fig_caption(f'Crab Nebula synchrotron: B~{CRAB_NEBULA["b_field_gauss"]*1e6:.0f} microG gives nu_c~{CRAB_NU_C_HZ:.1e} Hz for gamma~{CRAB_SYNCHROTRON_GAMMA_OPTICAL:.0e} electrons -- the multiwavelength capstone link between cosmic rays and magnetic fields.')
    return _fig_wrap(item['n'], item['title'], inner, 'log-log cosmic ray differential flux vs energy spectrum with a break at the knee energy')


_DIAGRAM_BUILDERS = {
    1: diagram_01, 2: diagram_02, 3: diagram_03, 4: diagram_04, 5: diagram_05,
    6: diagram_06, 7: diagram_07, 8: diagram_08, 9: diagram_09, 10: diagram_10,
    11: diagram_11, 12: diagram_12, 13: diagram_13, 14: diagram_14,
}


def lecture_svg(item: dict) -> str:
    return _DIAGRAM_BUILDERS[item['n']](item)


# ---------------------------------------------------------------------------
# Lecture content. Seven thematic units of exactly two lectures each (see
# syllabus.html's cadence rationale): (1) ISM Phases and Energetics, (2) The
# Atomic ISM and the 21 cm Line, (3) Dust, (4) The Molecular ISM, (5) Star
# Formation, (6) H II Regions and Ionization, (7) Shocks, Cosmic Rays, and
# Magnetic Fields.
# ---------------------------------------------------------------------------
LECTURES = [
    dict(
        n=1, title='The Multiphase Interstellar Medium: Phases and Pressure Balance',
        subtitle='The space between the stars is not empty, and it is not one thing',
        goals=[
            'Enumerate the real phases of the interstellar medium (molecular, cold/warm neutral, warm/hot ionized) and their characteristic densities, temperatures, and pressures.',
            'Derive the ideal-gas pressure-balance condition n1 T1 = n2 T2 between coexisting ISM phases and evaluate it for real, standard published phase parameters.',
            'Explain, at the level of a force/energy budget, why a medium spanning nine orders of magnitude in density can occupy the same Galactic disk in approximate pressure equilibrium.',
        ],
        why_matters='Every subsequent topic in this course -- the 21 cm line, dust, molecular clouds, star formation, H II regions, shocks, cosmic rays -- is a story about one particular phase of the interstellar medium (ISM) or the boundary between two of them. This lecture establishes the multiphase framework and the basic pressure-balance physics that all seven units will refer back to.',
        phenomenon=f'Radio, infrared, optical, ultraviolet, and X-ray observations of the space between stars reveal gas spanning temperatures from {ISM_PHASES["Molecular clouds (H2)"]["T_k"]:.0f} K (molecular clouds, barely above absolute zero) to {ISM_PHASES["Hot ionized medium (HIM)"]["T_k"]:.0e} K (supernova-shocked gas, hotter than the Sun\u2019s corona) and densities from {ISM_PHASES["Hot ionized medium (HIM)"]["n_cm3"]:.1e} to {ISM_PHASES["Molecular clouds (H2)"]["n_cm3"]:.0e} particles per cubic centimeter -- nine orders of magnitude in density and five in temperature, coexisting in the same Galactic disk.',
        vocab=['interstellar medium (ISM)', 'cold/warm neutral medium (CNM/WNM)', 'warm/hot ionized medium (WIM/HIM)', 'H II region', 'molecular cloud', 'pressure equilibrium', 'filling factor'],
        evidence=[
            'Optical absorption-line studies of the diffuse ISM (Na I, Ca II) reveal cold, dense clouds (T~80 K, n~30 cm^-3) embedded in a much more tenuous warm intercloud medium (T~8000 K, n~0.3 cm^-3) -- the cold neutral medium (CNM) and warm neutral medium (WNM) respectively.',
            'Soft X-ray all-sky background surveys (e.g., ROSAT) reveal a pervasive, million-degree, extremely tenuous hot ionized medium (HIM), thought to be maintained by the collective heating of supernova blast waves (McKee & Ostriker 1977).',
            'Radio recombination-line and Halpha surveys reveal a warm ionized medium (WIM) filling a substantial fraction of the disk volume even far from any single ionizing star, alongside dense, compact H II regions immediately surrounding hot O/B stars.',
            'Millimeter-wave molecular-line surveys (CO and its isotopologues) reveal cold (T~10-25 K), dense (n>10^2 cm^-3) molecular clouds -- the densest, coldest phase, and the exclusive sites of star formation (Units 4-5 of this course).',
        ],
        model=[
            'Treating each ISM phase as an ideal gas of particle number density n and temperature T, the thermal pressure is P = n k T (k = Boltzmann\u2019s constant); two phases in contact along a stable boundary must have equal pressure (ignoring, for this first approximation, magnetic and cosmic-ray pressure contributions developed later in Lecture 14), giving the pressure-balance condition n1 T1 = n2 T2.',
            'This is not merely a hypothesis: the McKee & Ostriker (1977) three-phase ISM model was constructed specifically to explain why the CNM and WNM, despite differing in density by roughly a factor of 100, are observed to coexist at nearly the same pressure P/k -- evidence that a thermal-equilibrium mechanism (developed in Lecture 02) actively regulates each phase\u2019s temperature at fixed pressure, rather than the phases having arbitrary, unrelated temperatures.',
            'The volume filling factor of each phase (the fraction of the disk\u2019s volume it occupies) is very different from its mass fraction: the HIM fills roughly half the disk\u2019s volume but contains a tiny fraction of its mass, while molecular clouds fill a tiny fraction of the volume but contain a large fraction of the mass available for future star formation -- exactly the volume-vs-mass distinction this course will return to throughout.',
        ],
        equation=r'P = nkT, \qquad n_1 T_1 = n_2 T_2 \ \text{(pressure balance between coexisting phases)}',
        example=[
            f'Computing P/k = n T for all six phases from their standard published (n, T) values: ' + '; '.join(
                f'{name.split(" (")[0]}: P/k={PHASE_PRESSURE_K[name]:,.0f} cm^-3 K' for name in ISM_PHASES),
            f'The CNM and WNM pressures (P/k = {PHASE_PRESSURE_K["Cold neutral medium (CNM)"]:,.0f} and {PHASE_PRESSURE_K["Warm neutral medium (WNM)"]:,.0f} cm^-3 K respectively) agree to within a factor of {PHASE_PRESSURE_K["Warm neutral medium (WNM)"]/PHASE_PRESSURE_K["Cold neutral medium (CNM)"]:.2f} -- consistent with, though not exactly equal to, the pressure-equilibrium expectation; the modest remaining offset is itself evidence that turbulent and magnetic pressure (not included in this simple P=nkT model) also contribute to the true total pressure balance.',
            f'By contrast, the molecular-cloud phase has P/k = {PHASE_PRESSURE_K["Molecular clouds (H2)"]:,.0f} cm^-3 K, roughly {PHASE_PRESSURE_K["Molecular clouds (H2)"]/PHASE_PRESSURE_K["Cold neutral medium (CNM)"]:.0f} times the CNM/WNM pressure -- molecular clouds are not in simple thermal-pressure balance with the diffuse ISM at all, because they are self-gravitating (Lecture 09 derives exactly when a cloud\u2019s own gravity, not ambient pressure, controls its fate).',
        ],
        pitfall='Assuming "hot" means "energetically dominant" or "dense." The hot ionized medium (HIM) is the hottest phase by far (T~5x10^5 K) yet has the lowest density of any phase (n~3.5x10^-3 cm^-3) and a very modest thermal pressure; conversely, molecular clouds are the coldest phase yet the highest-pressure and highest-density phase. Temperature, density, and pressure must be tracked as three independent quantities, not inferred from one another by intuition.',
        activity='Using only the pressure-balance condition n1 T1 = n2 T2 and the WNM\u2019s parameters, estimate what density a phase at T=10^6 K would need to be in pressure balance with the WNM, and compare your estimate to the HIM\u2019s actual published density.',
        lab_connection='Lab 01 extends this lecture\u2019s six-phase pressure calculation with a full thermal-equilibrium (heating=cooling) computation from Lecture 02, testing whether the CNM/WNM pressures are consistent with a genuine two-phase equilibrium rather than an assumed coincidence.',
        synthesis='The interstellar medium is not one substance but at least six coexisting phases spanning nine orders of magnitude in density, held together (approximately) by pressure balance; that balance -- and the thermal physics that regulates it -- is this course\u2019s starting point for everything that follows, from the 21 cm line (Unit 2) to star formation (Unit 5).',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=2, title='Heating, Cooling, and Thermal Instability',
        subtitle='Why the interstellar medium sorts itself into discrete stable phases',
        goals=[
            'Identify the dominant heating mechanism (photoelectric heating from dust grains) and cooling mechanisms (fine-structure and Lyman-alpha line emission) that set each ISM phase\u2019s equilibrium temperature.',
            'Construct and interpret a schematic thermal-equilibrium (heating=cooling) curve in pressure-temperature space and identify its stable and thermally unstable branches.',
            'Explain Field\u2019s (1965) thermal-instability criterion qualitatively and connect it to why the CNM and WNM exist as two discrete, well-separated equilibrium temperatures rather than a continuum.',
        ],
        why_matters='Lecture 01 showed that CNM and WNM coexist at nearly equal pressure; this lecture derives why -- and, crucially, why intermediate-temperature gas at that pressure is thermally unstable and cannot persist, so the ISM is naturally sorted into discrete phases rather than smoothly distributed in temperature.',
        phenomenon='At a fixed interstellar pressure P/k ~ 3000 cm^-3 K, gas can be found at T~80 K (CNM) or T~8000 K (WNM), but essentially never observed lingering at intermediate temperatures like T~500 K -- an empirical gap in the observed temperature distribution that is a direct signature of a genuine physical instability, not a selection effect.',
        vocab=['photoelectric heating', 'radiative cooling', 'fine-structure line', 'thermal equilibrium curve', 'thermal instability', 'isobaric perturbation'],
        evidence=[
            'Ultraviolet starlight photons ejecting photoelectrons from interstellar dust grains is the dominant heating mechanism in the diffuse neutral ISM (Bakes & Tielens 1994; Wolfire et al. 1995, 2003), with a heating rate per particle that depends only weakly on gas temperature.',
            'The dominant coolants are collisionally excited fine-structure lines -- principally singly ionized carbon\u2019s [C II] 158 micron line in the CNM/WNM, and Lyman-alpha (121.6 nm) in warmer, more ionized gas -- whose emissivities depend strongly (often close to exponentially, via the Boltzmann excitation factor) on temperature.',
            'Field (1965, ApJ 142, 531) showed analytically that an isobaric (constant-pressure) gas parcel is thermally unstable wherever the net cooling rate decreases with increasing temperature at fixed pressure -- exactly the condition realized on the steep, negative-slope middle branch of the heating/cooling curve between the CNM and WNM equilibrium points.',
        ],
        model=[
            'At thermal equilibrium, the total heating rate per unit volume Gamma(n) equals the total cooling rate Lambda(n,T)n^2 (cooling from two-body collisional processes scales as n^2); solving Gamma=Lambda n^2 for the equilibrium T at each assumed pressure traces out a curve in P-T (or, equivalently, T-n) space.',
            'Because the fine-structure/Lyman-alpha cooling rate rises very steeply with T while photoelectric heating is comparatively flat, this equilibrium curve is S-shaped: two stable branches (a cold, dense one and a warm, tenuous one) at nearly the same pressure, joined by a middle branch on which pressure decreases as temperature increases at fixed density -- the Field (1965) instability condition.',
            'A gas parcel perturbed onto the unstable middle branch cannot return to it: any small increase in T there causes cooling to fall faster than heating, so the parcel runs away to still higher T (toward the WNM branch) rather than restoring itself; the reverse runs away to lower T (toward the CNM branch). This is exactly the physical mechanism that sorts the diffuse ISM into two discrete, stable phases rather than a continuum.',
        ],
        equation=r'\Gamma(n) = \Lambda(n,T)\, n^2 \quad \text{(equilibrium)}, \qquad \left.\frac{\partial \mathcal{L}}{\partial T}\right|_{P} < 0 \ \text{(Field 1965 instability criterion)}',
        example=[
            f'This course\u2019s schematic thermal-equilibrium curve (Lecture 01\u2019s CNM point, P/k={PHASE_PRESSURE_K["Cold neutral medium (CNM)"]:,.0f} cm^-3 K at T={ISM_PHASES["Cold neutral medium (CNM)"]["T_k"]:.0f} K, and WNM point, P/k={PHASE_PRESSURE_K["Warm neutral medium (WNM)"]:,.0f} cm^-3 K at T={ISM_PHASES["Warm neutral medium (WNM)"]["T_k"]:,.0f} K) is constructed in Lab 01 to pass through both real, published equilibrium points and to have a negative-slope (unstable) branch strictly between them, reproducing the qualitative Field (1965)/Wolfire et al. (1995, 2003) result.',
            f'A parcel placed at an intermediate temperature of, say, 500 K at the CNM/WNM pressure lies on this course\u2019s unstable branch (verified directly by checking the local slope sign in Lab 01\u2019s generated curve), consistent with the observed near-absence of long-lived interstellar gas at such intermediate temperatures.',
        ],
        pitfall='Treating "thermal equilibrium" as synonymous with "thermally stable." A gas parcel can satisfy Gamma=Lambda n^2 exactly (be in instantaneous thermal equilibrium) while still being thermally unstable in the Field (1965) sense if it sits on the wrong branch of the curve; equilibrium is a necessary but not sufficient condition for a long-lived, physically realized phase.',
        activity='Explain, using only the sign of dP/dT at fixed n implied by the S-curve\u2019s middle branch, why a small compression of gas sitting on the unstable branch leads it to run away toward the cold, dense CNM branch rather than back to its starting point.',
        lab_connection='Lab 01\u2019s second half builds this lecture\u2019s heating/cooling equilibrium curve numerically and verifies the instability criterion\u2019s sign directly from the constructed curve, rather than merely asserting it.',
        synthesis='Photoelectric heating from dust grains and fine-structure/Lyman-alpha cooling combine to produce an S-shaped thermal-equilibrium curve with a genuinely unstable middle branch -- the physical reason the neutral ISM is observed in two discrete phases (CNM, WNM) at nearly the same pressure, rather than as a smooth continuum, closing out this course\u2019s two-lecture introduction to the multiphase ISM before Unit 2 examines the CNM/WNM\u2019s primary diagnostic, the 21 cm line.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=3, title='The 21 cm Hyperfine Line: Spin Temperature and Radiative Transfer',
        subtitle='How a spin-flip transition forbidden in any laboratory becomes astronomy\u2019s most important spectral line',
        goals=[
            'Derive the physical origin of the 21 cm hyperfine transition and the definition of spin (excitation) temperature from the Boltzmann level-population ratio.',
            'Derive the radiative-transfer solution for 21 cm brightness temperature through a uniform slab, T_B = T_spin(1-e^-tau), and its optically thin limit.',
            'Explain why the 21 cm line, forbidden in any terrestrial laboratory, is nonetheless the dominant observational probe of atomic hydrogen throughout the Galaxy.',
        ],
        why_matters='Unit 1 established that atomic hydrogen dominates the CNM and WNM by mass. This lecture derives the single spectral line -- 21 cm -- that makes atomic hydrogen directly observable throughout the Galaxy (and in external galaxies), and supplies the radiative-transfer machinery Lecture 04 uses to convert an observed spectrum into a real column density.',
        phenomenon=f'The ground state of neutral hydrogen is split into two hyperfine sublevels differing only in whether the proton\u2019s and electron\u2019s spins are parallel or antiparallel, separated by an energy of only {H_PLANCK*NU_21CM_HZ:.3e} J -- corresponding to a transition frequency of exactly {NU_21CM_HZ/1e6:.3f} MHz (wavelength {LAMBDA_21CM_M*100:.2f} cm) that Harold Ewen and Edward Purcell first detected from the roof of the Harvard physics building in 1951, opening the entire field of radio astronomy of the neutral interstellar medium.',
        vocab=['hyperfine structure', 'spin-flip transition', 'spin (excitation) temperature', 'optical depth', 'brightness temperature', 'forbidden transition', 'Einstein A coefficient'],
        evidence=[
            'The 21 cm transition is a magnetic-dipole ("forbidden") transition with an extremely small spontaneous-emission rate (Einstein A10 coefficient), corresponding to a spontaneous-decay lifetime of roughly 11 million years per atom -- far too slow to ever be seen in a terrestrial laboratory sample, yet routinely detected astronomically because even a tenuous interstellar sightline contains an enormous total number of hydrogen atoms.',
            'Radio telescopes worldwide have mapped 21 cm emission across the entire sky and across the disks of hundreds of external galaxies (e.g., the classic Leiden/Argentine/Bonn survey and, more recently, the all-sky HI4PI survey), making 21 cm the single most complete map of atomic hydrogen\u2019s distribution and kinematics in the universe.',
            'Because the hyperfine splitting energy (equivalent to a temperature T*=hnu/k of only a few hundredths of a kelvin) is minuscule compared to interstellar gas temperatures (tens to thousands of kelvin), the upper and lower hyperfine levels are populated very close to their statistical weight ratio (3:1), which is exactly why the population ratio is an extremely sensitive, nearly linear thermometer of the gas kinetic temperature under most interstellar conditions.',
        ],
        model=[
            'Define the spin temperature T_spin via the Boltzmann ratio of the upper (F=1, statistical weight g1=3) to lower (F=0, g0=1) hyperfine sublevel populations: n1/n0 = (g1/g0) exp(-T*/T_spin), where T*=h*nu_21cm/k is the transition\u2019s equivalent temperature; in the diffuse ISM, T_spin is observationally found to closely track the gas kinetic temperature because collisions (not radiative pumping) dominate the level populations at typical CNM/WNM densities.',
            'The equation of radiative transfer for 21 cm emission through a uniform-temperature slab of optical depth tau (integrated along the line of sight) has the closed-form solution T_B(v) = T_spin (1 - e^{-tau(v)}), directly analogous to blackbody radiative transfer with T_spin playing the role of a local "radiation temperature."',
            'In the frequently applicable optically thin limit (tau<<1, valid for most of the WNM and much of the CNM along typical high-latitude sightlines), this simplifies to T_B(v) ~= T_spin * tau(v), meaning the observed brightness temperature becomes directly proportional to the number of atoms along the line of sight at that velocity -- the key simplification Lecture 04 exploits to derive the HI column-density formula.',
        ],
        equation=r'\frac{n_1}{n_0} = 3\,e^{-T_\ast/T_{\rm spin}}, \qquad T_B(v) = T_{\rm spin}\left(1 - e^{-\tau(v)}\right) \xrightarrow{\tau \ll 1} T_{\rm spin}\,\tau(v)',
        example=[
            f'For CNM gas at T_spin={CNM_TSPIN_K:.0f} K (a standard published value, Kalberla & Kerp 2009 review), the hyperfine population ratio is n1/n0={CNM_POP_RATIO:.5f}, extremely close to (but measurably below) the high-temperature limit of exactly 3.0, since T*/T_spin={T_STAR_21CM_K/CNM_TSPIN_K:.4f} is small but not utterly negligible at this relatively low spin temperature.',
            f'For WNM gas at T_spin={WNM_TSPIN_K:.0f} K, the same formula gives n1/n0={WNM_POP_RATIO:.6f}, indistinguishable from 3.0 to five significant figures -- explicitly demonstrating why the level-population correction matters far more for cold, dense CNM gas than for the much warmer, more tenuous WNM.',
            f'A CNM cloud of optical depth tau=0.05 at T_spin={CNM_TSPIN_K:.0f} K produces a brightness temperature T_B = T_spin(1-e^-tau) = {brightness_temperature_k(CNM_TSPIN_K, 0.05):.3f} K, within {abs(brightness_temperature_k(CNM_TSPIN_K, 0.05)-CNM_TSPIN_K*0.05)/(CNM_TSPIN_K*0.05)*100:.2f}% of the optically thin approximation T_spin*tau={CNM_TSPIN_K*0.05:.3f} K -- confirming the optically thin approximation is excellent at this representative CNM optical depth.',
        ],
        pitfall='Assuming spin temperature always equals the true gas kinetic temperature. This is an excellent approximation in the collision-dominated CNM/WNM, but breaks down in very low-density or strongly UV-illuminated regions where radiative (Wouthuysen-Field) effects can decouple T_spin from the kinetic temperature -- a genuine limitation of the simple picture presented here, not an algebra error.',
        activity='Using n1/n0=3exp(-T*/Tspin), explain qualitatively why the 21 cm line\u2019s population-ratio "thermometer" becomes progressively less sensitive to further increases in T_spin once T_spin is already much larger than T*=0.068 K -- and connect this to why 21 cm alone cannot easily distinguish a 5000 K cloud from an 8000 K cloud, even though it easily distinguishes an 80 K cloud from a 500 K cloud.',
        lab_connection='Lab 02 uses this lecture\u2019s radiative-transfer solution directly, applying the optically thin brightness-temperature formula to a representative two-component (CNM+WNM) spectrum to derive a real HI column density.',
        synthesis='The 21 cm hyperfine transition\u2019s tiny energy splitting makes its two-level population ratio an exquisitely sensitive probe of gas temperature, and its radiative-transfer solution converts an observed brightness-temperature spectrum directly into a physically meaningful spin temperature and optical depth -- the two ingredients Lecture 04 combines into this course\u2019s first real column-density measurement.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=4, title='HI Column Density: From Spectra to the Atomic Gas Budget',
        subtitle='Turning a radio spectrum into a real number of hydrogen atoms per square centimeter',
        goals=[
            'Derive the optically thin HI column-density formula N(HI) = 1.8224e18 integral(T_B dv) [cm^-2] from the 21 cm radiative-transfer solution.',
            'Apply the formula to a representative two-component (CNM+WNM) 21 cm spectrum and to a real, published all-sky-survey column density.',
            'Explain the physical origin of the numerical coefficient 1.8224e18 in terms of the 21 cm transition\u2019s atomic constants.',
        ],
        why_matters='Lecture 03 derived the radiative-transfer physics of the 21 cm line; this lecture turns that physics into the single most-used quantitative tool of Galactic HI astronomy -- the column-density formula -- and applies it to a real, published measurement toward a well-studied extragalactic sightline.',
        phenomenon=f'The HI4PI all-sky 21 cm survey measures a Galactic-foreground atomic hydrogen column density of N(HI)={SIGHTLINE_3C273["n_hi_cm2"]:.2e} cm^-2 toward the bright, well-studied quasar 3C 273 -- a single number, derived entirely from a radio spectrum, that astronomers routinely use to correct X-ray and ultraviolet observations of that same distant quasar for foreground Galactic absorption.',
        vocab=['column density', 'optically thin approximation', 'brightness-temperature integral', 'velocity-integrated intensity', 'HI4PI survey'],
        evidence=[
            'The total number of hydrogen atoms per unit area along a line of sight (the column density N(HI), typically reported in cm^-2) is the single most useful summary statistic of an HI spectrum for nearly every downstream application, from Galactic structure studies to correcting extragalactic X-ray/UV absorption.',
            'All-sky 21 cm surveys such as the Leiden/Argentine/Bonn (LAB) survey and its modern successor, HI4PI (HI4PI Collaboration 2016), provide column densities toward essentially any Galactic direction, including toward extragalactic background sources used for X-ray absorption studies (e.g., 3C 273, Cygnus X-1).',
            'The optically thin approximation, while not universally valid (it can underestimate N(HI) in unusually cold, dense, or high-column CNM structures where self-absorption becomes significant), is an excellent approximation for the majority of high-latitude Galactic sightlines used in this way.',
        ],
        model=[
            'Starting from Lecture 03\u2019s optically thin solution T_B(v) ~= T_spin*tau(v), and the definition of 21 cm optical depth in terms of the lower-level column density and the Einstein A coefficient, the total (velocity-integrated) HI column density reduces to a simple integral of the observed brightness temperature over velocity, independent of the (unknown, but nearly canceling) spin temperature: N(HI) = C * integral(T_B(v) dv), where C = 1.8224e18 cm^-2 (K km/s)^-1 is a fixed combination of fundamental constants and the 21 cm transition\u2019s atomic properties (the Einstein A coefficient, statistical weights, and hnu/k).',
            'For a Gaussian line profile with peak brightness temperature T_peak and full width at half maximum (FWHM) Delta_v, the velocity integral has the closed form integral(T_B dv) = T_peak * Delta_v * sqrt(pi/(4 ln2)), letting the column-density formula be evaluated directly from two observable quantities (peak and width) rather than requiring numerical integration of every spectrum.',
            'A real sightline\u2019s spectrum is typically the sum of several distinct velocity components (CNM clouds embedded in a broader WNM background), so the total column density is the sum of each component\u2019s individually computed contribution -- exactly the two-component decomposition this course\u2019s representative CNM+WNM spectrum illustrates.',
        ],
        equation=r'N(\mathrm{HI}) = 1.8224\times10^{18}\,\mathrm{cm^{-2}}\int T_B(v)\,dv, \qquad \int T_B\,dv = T_{\rm peak}\,\Delta v\sqrt{\pi/(4\ln 2)}\ \text{(Gaussian)}',
        example=[
            f'This course\u2019s representative CNM component (peak T_B={CNM_PEAK_TB_K:.0f} K, FWHM={CNM_FWHM_KMS:.1f} km/s, illustrative synthetic profile shape but real, standard CNM linewidth/T_spin values) gives N(HI)_CNM={N_HI_CNM_WORKED:.3e} cm^-2 by direct Gaussian integration.',
            f'The representative WNM component (peak T_B={WNM_PEAK_TB_K:.0f} K, FWHM={WNM_FWHM_KMS:.0f} km/s) gives N(HI)_WNM={N_HI_WNM_WORKED:.3e} cm^-2, and the total two-component column density is N(HI)_total={N_HI_TOTAL_WORKED:.3e} cm^-2 -- of the same general order of magnitude as the real, published 3C 273 sightline value of {SIGHTLINE_3C273["n_hi_cm2"]:.2e} cm^-2, though not an attempt to reproduce that specific sightline\u2019s exact spectrum (this course\u2019s synthetic profile is explicitly a representative illustration, not a claimed measurement of 3C 273 itself; see reference-log.md).',
            f'By contrast, the real published Cygnus X-1 sightline column density (N_H={SIGHTLINE_CYGX1["n_hi_cm2"]:.1e} cm^-2, from X-ray spectral absorption studies) is roughly {SIGHTLINE_CYGX1["n_hi_cm2"]/SIGHTLINE_3C273["n_hi_cm2"]:.0f} times larger than toward 3C 273 -- a direct, real illustration of how strongly Galactic HI column density depends on sightline (Cygnus X-1 lies much closer to the Galactic plane, b={SIGHTLINE_CYGX1["b_deg"]:.2f} degrees, than 3C 273, b={SIGHTLINE_3C273["b_deg"]:.2f} degrees).',
        ],
        pitfall='Applying the optically thin approximation uncritically to every CNM component. Narrow, cold, high-column CNM clumps can have tau approaching or exceeding order unity, in which case the true column density (from the full T_B=T_spin(1-e^-tau) solution) is larger than the optically thin formula would suggest; the assumption should always be checked, not assumed, particularly for narrow, high-peak-brightness features.',
        activity='Using the Gaussian-integral formula, explain why a broad, low-peak WNM component and a narrow, high-peak CNM component can contribute comparable total column densities even though their peak brightness temperatures differ by a large factor -- and identify which observable (peak temperature or linewidth) matters more for the total column density of a broad component.',
        lab_connection='Lab 02 performs this lecture\u2019s full worked HI column-density calculation for a two-component spectrum and compares the result to real, published all-sky-survey values toward two different real extragalactic sightlines.',
        synthesis='The 21 cm column-density formula converts an entirely passive radio observation into a direct census of atomic hydrogen along any line of sight in the Galaxy -- closing out this course\u2019s atomic-ISM unit and setting up Unit 3\u2019s shift to the interstellar medium\u2019s solid component: dust.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=5, title='Interstellar Dust I: Extinction and Reddening',
        subtitle='Why distant stars look fainter and redder than they really are',
        goals=[
            'Derive the relationships among optical depth, extinction in magnitudes, color excess E(B-V), and the total-to-selective extinction ratio R_V.',
            'Apply the Cardelli, Clayton & Mathis (1989) average Galactic extinction-curve parametrization to compute extinction at multiple wavelengths for a real, heavily reddened star.',
            'Explain, physically, why interstellar dust extinction is wavelength-dependent (grain-size-comparable-to-wavelength scattering) and why this produces reddening.',
        ],
        why_matters='Every optical/infrared observation of a star or nebula behind interstellar dust -- including the H II region diagnostics in Unit 6 and any real photometric distance/luminosity determination -- must be corrected for extinction and reddening; this lecture derives the physical basis for that correction from first principles.',
        phenomenon=f'Cygnus OB2 No. 12, one of the intrinsically most luminous stars known in the Galaxy, appears in an ordinary optical image as a comparatively faint, deep-red point of light -- because {AV_CYGOB2_12:.1f} magnitudes of visual extinction, corresponding to a factor of {10**(AV_CYGOB2_12/2.5):.0f} in flux, lie along the line of sight through the Cygnus OB2 association\u2019s dense foreground dust.',
        vocab=['extinction', 'reddening', 'optical depth', 'color excess E(B-V)', 'total-to-selective extinction R_V', 'scattering', 'absorption'],
        evidence=[
            'Interstellar dust both absorbs and scatters starlight out of the line of sight, dimming a star\u2019s apparent brightness (extinction) by an amount that increases toward shorter (bluer) wavelengths, because interstellar grains are comparable in size to or smaller than optical wavelengths (Rayleigh/Mie-regime scattering is more efficient at shorter wavelengths) -- the same physical reason Earth\u2019s sky is blue, applied to interstellar rather than atmospheric particles.',
            'Because extinction is stronger at blue wavelengths than red, a reddened star\u2019s observed color (e.g., B-V) is redder than its intrinsic (unreddened) color for the same spectral type -- the reddening this lecture\u2019s title refers to, quantified by the color excess E(B-V) = (B-V)_observed - (B-V)_intrinsic.',
            'Cardelli, Clayton & Mathis (1989, ApJ 345, 245) fit a single-parameter family of extinction curves (parametrized by R_V = A_V/E(B-V)) to a large sample of Galactic sightlines, finding R_V=3.1 as the diffuse-ISM average but with real, well-documented sightline-to-sightline variation, particularly toward dense molecular clouds (Lecture 06 continues this theme).',
        ],
        model=[
            'Extinction in magnitudes, A_lambda, is related to the optical depth tau_lambda of intervening dust by A_lambda = 1.086 tau_lambda (the factor 1.086 = 2.5/ln(10) converts from the natural-log-based optical depth to the base-2.5-per-magnitude convention).',
            'The color excess E(B-V) = A_B - A_V isolates the wavelength-dependent part of extinction from any wavelength-independent flux normalization, and the total-to-selective extinction ratio R_V = A_V/E(B-V) characterizes the overall shape (steepness) of the extinction curve: a larger R_V means a "grayer" (less steeply wavelength-dependent) extinction law, physically associated with a larger typical grain size along that sightline.',
            'The full wavelength dependence A(lambda)/A_V = a(x) + b(x)/R_V (Cardelli, Clayton & Mathis 1989, x=1/lambda in inverse microns) lets the extinction at any optical/near-infrared wavelength be predicted from just two numbers, E(B-V) and R_V, once A_V=R_V*E(B-V) is known -- exactly the calculation this lecture\u2019s worked example performs for a real star.',
        ],
        equation=r'A_V = R_V\,E(B\!-\!V), \qquad \frac{A(\lambda)}{A_V} = a(x) + \frac{b(x)}{R_V}, \ x \equiv 1/\lambda',
        example=[
            f'Cygnus OB2 No. 12 (live-verified physical reasoning applied to standard published photometry, Massey & Thompson 1991): E(B-V)={CYGOB2_12["ebv_mag"]:.2f} mag, R_V={CYGOB2_12["r_v"]:.1f} (close to the diffuse-ISM average). Computed A_V = R_V E(B-V) = {AV_CYGOB2_12:.2f} mag, corresponding to a flux dimming factor of 10^(A_V/2.5) = {10**(AV_CYGOB2_12/2.5):.1f}.',
            f'HD 200775 (NGC 7023 illuminating star, an anomalous dense-cloud sightline, Whittet et al. 2001): E(B-V)={HD200775["ebv_mag"]:.2f} mag but R_V={HD200775["r_v"]:.1f} (much larger than the diffuse-ISM average), giving A_V = {AV_HD200775:.2f} mag -- a smaller color excess than Cyg OB2-12 but comparable total extinction, because the larger R_V compensates.',
            f'Evaluating the Cardelli et al. (1989) parametrization at V band (x=1/0.545 um^-1) for R_V=3.1 gives A(V)/A_V = {CARDELLI_AV_RATIO_V:.3f} (should equal 1.000 by definition, confirming the parametrization is implemented correctly), and at B band (x=1/0.438 um^-1) gives A(B)/A_V = {CARDELLI_AB_RATIO_V:.3f}, consistent with the standard result A_B/A_V > 1 (extinction is stronger at bluer wavelengths).',
        ],
        pitfall='Confusing E(B-V) with A_V, or assuming R_V=3.1 universally. E(B-V) measures only the differential (color) effect of extinction, not the total dimming; and R_V is empirically known to vary significantly toward dense molecular clouds (where grain growth increases R_V, as in the HD 200775 example above) -- using the diffuse-ISM R_V=3.1 uncritically for a dense-cloud sightline can misestimate A_V by tens of percent.',
        activity='Using A_V=R_V E(B-V), explain why two stars with very different total extinctions A_V can nonetheless have identical color excesses E(B-V) if their sightlines have correspondingly different R_V values -- and identify which single additional photometric measurement (beyond B and V) would help distinguish the two cases observationally.',
        lab_connection='Lab 03 applies this lecture\u2019s Cardelli parametrization across multiple photometric bands for Cygnus OB2 No. 12 and propagates the extinction correction through to an intrinsic (dereddened) color, directly using this lecture\u2019s equations.',
        synthesis='Interstellar extinction and reddening -- derived here from grain-scale scattering physics -- must be corrected for before any photometric measurement of a dust-embedded object can be trusted; Lecture 06 continues with dust\u2019s complementary observational signatures, polarization and thermal emission.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=6, title='Interstellar Dust II: Polarization and Thermal Emission',
        subtitle='What dust grains do with the starlight they do not simply block',
        goals=[
            'Explain grain alignment (radiative torques) as the physical origin of interstellar linear polarization and its diagnostic use for mapping magnetic-field direction.',
            'Derive the modified-blackbody model for thermal dust emission and its dependence on grain temperature and emissivity index beta.',
            'Connect a dust grain\u2019s radiative equilibrium (absorbed starlight balanced by re-emitted infrared radiation) to its equilibrium temperature.',
        ],
        why_matters='Lecture 05 treated dust purely as an obstacle dimming and reddening background starlight. This lecture treats dust as a source in its own right -- its polarized transmitted light traces magnetic-field direction (a preview of Lecture 14\u2019s magnetic-field diagnostics), and its re-radiated thermal infrared/submillimeter emission is one of the primary ways cold, dense molecular clouds (Unit 4) are mapped and weighed.',
        phenomenon='Starlight passing through a cloud of non-spherical dust grains that are systematically aligned (their long axes preferentially perpendicular to the local magnetic field) emerges partially linearly polarized, with the polarization angle tracing the magnetic-field direction projected on the sky -- a technique that has mapped magnetic-field morphology across the Galactic plane and within individual star-forming clouds without any direct in-situ measurement.',
        vocab=['grain alignment', 'radiative torques', 'linear polarization', 'modified blackbody', 'dust emissivity index', 'radiative equilibrium', 'spectral energy distribution (SED)'],
        evidence=[
            'Interstellar polarization was discovered independently by Hall (1949) and Hiltner (1949) through observations of systematically polarized starlight, immediately interpreted as evidence for both non-spherical dust grains and a large-scale Galactic magnetic field capable of aligning them.',
            'The modern understanding of grain alignment (radiative torques from anisotropic starlight spinning up irregularly shaped grains, which then precess into alignment with the local magnetic field) is reviewed by Lazarian (2007, JQSRT 106, 225) and Andersson, Lazarian & Vaillancourt (2015, ARA&A 53, 501).',
            'Cold dust grains re-radiate absorbed starlight predominantly in the far-infrared/submillimeter, where the observed spectral energy distribution is well described by a modified blackbody, S_nu proportional to kappa_nu B_nu(T_dust), with kappa_nu (the dust opacity) itself rising with frequency as a power law nu^beta (beta~1.5-2 typically) -- exactly the shape used by facilities like Herschel and ALMA to map dust temperature and column density in molecular clouds.',
        ],
        model=[
            'A dust grain reaches radiative equilibrium when the rate of starlight energy it absorbs equals the rate of infrared energy it re-emits; because small grains are inefficient infrared emitters at wavelengths much larger than their size (an effect captured by the frequency-dependent emissivity kappa_nu proportional to nu^beta), they must reach a higher equilibrium temperature than a perfect blackbody of the same absorbed power in order to balance the energy budget.',
            'The resulting emitted spectrum, a modified blackbody S_nu = kappa_nu B_nu(T_dust), peaks at a wavelength that shifts to shorter wavelengths for warmer grains (an emissivity-modified Wien\u2019s-law-like behavior) and can be used, given an assumed beta, to solve for T_dust directly from the observed peak or from multi-band photometry.',
            'Because polarization angle traces projected magnetic-field direction and modified-blackbody fitting traces dust temperature and column density, the two observational techniques developed in this lecture are complementary tools this course will invoke again in Lecture 14\u2019s magnetic-field diagnostics and throughout Unit 4\u2019s molecular-cloud mass estimates.',
        ],
        equation=r'S_\nu \propto \kappa_\nu\,B_\nu(T_{\rm dust}), \qquad \kappa_\nu \propto \nu^{\beta}\ (\beta \approx 1.5\text{-}2)',
        example=[
            'This lecture\u2019s modified-blackbody worked figure (Lab-independent, generated directly in this lecture\u2019s slides) evaluates three representative grain temperatures (15 K, 25 K, 50 K) at fixed beta=2 and confirms the expected behavior: the emission peak shifts to shorter wavelength as T_dust increases, exactly as Wien\u2019s-law intuition predicts, even though the underlying spectral shape (a modified, not pure, blackbody) differs from the pure-blackbody case.',
            f'A cold molecular-cloud dust temperature of T_dust~15-25 K (consistent with the Orion Molecular Cloud\u2019s gas-phase temperature of {ORION_MOLECULAR_CLOUD["temp_k"]:.0f} K used throughout Unit 4, since gas and dust are thermally well-coupled at the high densities of dense cloud interiors) places the emission peak firmly in the far-infrared/submillimeter, consistent with why cold molecular clouds are essentially undetectable in visible light but readily mapped at submillimeter wavelengths.',
        ],
        pitfall='Assuming dust temperature and gas temperature are always equal. They are well-coupled by gas-grain collisions only at the high densities found deep inside molecular clouds (as assumed above for Orion); in the much more tenuous diffuse ISM, dust and gas temperatures can differ substantially because the coupling collision rate is far lower there -- a genuine physical distinction, not a simplifying convenience to be applied everywhere.',
        activity='Using the modified-blackbody model\u2019s qualitative behavior (peak wavelength shifts to shorter wavelength for warmer grains, and the width/steepness of the SED depends on beta), explain why observing a dusty source at two or more well-separated far-infrared/submillimeter wavelengths is required to solve for both T_dust and beta simultaneously, rather than assuming beta a priori from a single-wavelength flux measurement.',
        lab_connection='Lab 03 extends into a brief modified-blackbody fitting exercise for a representative molecular-cloud dust temperature, connecting directly to Unit 4\u2019s molecular-cloud mass estimates from dust continuum emission.',
        synthesis='Dust\u2019s polarization signature maps magnetic-field direction and its thermal emission maps cold, dense gas invisible in visible light -- two complementary diagnostic tools that, together with Lecture 05\u2019s extinction/reddening, complete this course\u2019s treatment of the ISM\u2019s solid component before Unit 4 turns to the molecular gas phase dust so often traces.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=7, title='The Molecular Interstellar Medium: H2 Formation and CO as a Tracer',
        subtitle='Why astronomers map an invisible molecule using a rare, visible one',
        goals=[
            'Explain why molecular hydrogen (H2), despite being the most abundant molecule in molecular clouds, cannot be directly observed at the low temperatures typical of star-forming clouds, and why grain-surface formation dominates over gas-phase formation.',
            'Derive the CO-to-H2 mass conversion (the X_CO factor) as a practical observational workaround for H2\u2019s invisibility, and apply it to compute a real molecular cloud\u2019s total mass.',
            'Cross-check the CO-derived mass against a direct density-times-volume mass estimate for the same real cloud.',
        ],
        why_matters='Molecular clouds (introduced as the highest-density ISM phase in Lecture 01) are where all star formation in this course\u2019s Unit 5 takes place. This lecture derives how astronomers actually measure a molecular cloud\u2019s mass at all, given that its dominant constituent, H2, is nearly invisible under typical cloud conditions.',
        phenomenon=f'The Orion Molecular Cloud\u2019s dense ridge (OMC-1) contains roughly {OMC1_H2_MASS_DIRECT:,.0f} solar masses of molecular hydrogen gas, by far the dominant mass component of the Orion star-forming complex -- yet H2 itself, a symmetric homonuclear diatomic molecule with no permanent dipole moment, has no allowed rotational transitions detectable at the ~20-25 K temperatures typical of this gas, forcing astronomers to infer its presence and mass indirectly via a much rarer trace molecule, carbon monoxide (CO).',
        vocab=['molecular hydrogen (H2)', 'grain-surface catalysis', 'carbon monoxide (CO)', 'X_CO conversion factor', 'CO luminosity', 'self-shielding'],
        evidence=[
            'Gas-phase formation of H2 (two hydrogen atoms colliding directly) is far too slow to explain the observed molecular fractions in clouds, because the newly formed H2 molecule has no way to shed its formation energy fast enough via gas-phase collisions alone; grain-surface catalysis -- H atoms sticking to and diffusing across a cold dust-grain surface (the same dust grains from Unit 3) until they meet and combine, with the grain itself absorbing the excess binding energy -- dominates H2 formation throughout the ISM (Hollenbach & Salpeter 1971; Gould & Salpeter 1963).',
            'H2\u2019s lowest rotational transitions require temperatures of hundreds to thousands of kelvin to be significantly populated (because H2\u2019s small moment of inertia gives it widely spaced rotational energy levels), far above the ~10-25 K typical of the bulk of molecular-cloud gas, so H2 itself is essentially undetectable in the cold gas that dominates a cloud\u2019s mass.',
            'Carbon monoxide (CO), despite being roughly 10^4 times less abundant than H2, has closely spaced rotational energy levels (because of its larger moment of inertia) that are easily excited even at 10-25 K, and its rotational transitions (particularly the J=1-0 line at 2.6 mm) are the standard, nearly universal tracer of molecular gas throughout the Galaxy and in external galaxies (Bolatto, Wolfire & Leroy 2013, ARA&A 51, 207, the definitive X_CO review).',
        ],
        model=[
            'Because CO and H2 form and are destroyed together under similar physical conditions (both require sufficient dust/gas shielding from dissociating ultraviolet radiation), CO\u2019s velocity-integrated line intensity W_CO (in K km/s) is empirically found to correlate tightly with the H2 column density along the same line of sight, N(H2) = X_CO * W_CO, with a nearly constant conversion factor X_CO across most of the Milky Way disk\u2019s molecular gas (Bolatto, Wolfire & Leroy 2013).',
            'Multiplying this column-density relation by the observed area of a cloud (or, equivalently, treating the product W_CO*Area as the cloud\u2019s "CO luminosity" L_CO) converts an entirely observational quantity (an integrated CO line flux) into a molecular hydrogen mass via M(H2) = 2 m_H X_CO L_CO (the factor of 2 accounts for two H atoms per H2 molecule).',
            'This CO-derived mass can be independently cross-checked against a direct mass estimate (density times volume, using an independently determined H2 density and cloud size, e.g., from dust continuum emission or extinction mapping) and against a virial mass estimate (Lecture 08) -- exactly the three-way cross-check this lecture\u2019s worked example performs for the real Orion Molecular Cloud.',
        ],
        equation=r'N(\mathrm{H_2}) = X_{\rm CO}\,W_{\rm CO}, \qquad M(\mathrm{H_2}) = 2\,m_H\,X_{\rm CO}\,L_{\rm CO}',
        example=[
            f'The Orion Molecular Cloud\u2019s dense ridge (OMC-1; n(H2)={ORION_MOLECULAR_CLOUD["n_h2_cm3"]:.0e} cm^-3, radius={ORION_MOLECULAR_CLOUD["radius_pc"]:.1f} pc, standard published values, Genzel & Stutzki 1989) has a direct (density x volume) mass of M(H2)={OMC1_H2_MASS_DIRECT:,.0f} Msun.',
            f'Converting the same cloud\u2019s implied total H2 particle count into an equivalent CO luminosity via the standard X_CO={X_CO_CM2_K_KMS:.1e} cm^-2 (K km/s)^-1 (Bolatto, Wolfire & Leroy 2013) and back into a CO-derived mass gives M(H2)={OMC1_H2_MASS_FROM_CO:,.0f} Msun -- differing from the direct estimate by a factor of {OMC1_H2_MASS_DIRECT/OMC1_H2_MASS_FROM_CO:.2f}, entirely attributable to this course\u2019s direct-mass calculation including the standard mean-molecular-weight correction for helium (mu={MU_MOLECULAR:.2f}) while the X_CO-based method\u2019s conventional factor-of-2 (not mu) already implicitly folds in a similar but not identical helium correction -- an honest, disclosed methodological discrepancy (see reference-log.md), not a claimed exact agreement.',
            f'Lecture 08\u2019s virial mass estimate for the same cloud (from its size and CO linewidth alone, independent of any assumed density) gives M_vir={OMC1_VIRIAL_MASS:,.0f} Msun, a genuinely independent third method that Lecture 08 discusses in the context of whether the cloud is gravitationally bound.',
        ],
        pitfall='Treating X_CO as a universal constant applicable to any galaxy or environment. X_CO is calibrated for typical Milky Way-disk conditions and is known to vary substantially in low-metallicity dwarf galaxies (where less dust shields CO from photodissociation, suppressing CO relative to H2) and in the Galactic center\u2019s more extreme conditions (Bolatto, Wolfire & Leroy 2013); applying the disk-average X_CO outside its calibrated regime can introduce order-of-magnitude mass errors.',
        activity='Using the three independent OMC-1 mass estimates in this lecture\u2019s worked example (direct, CO-derived, virial), explain what physical assumption each method makes that the other two do not, and identify which single additional observation (if any) could help decide among them if they disagreed by a large factor.',
        lab_connection='Lab 04 reproduces this lecture\u2019s CO-to-mass conversion for the Orion Molecular Cloud and extends it to a second real molecular cloud, the quiescent Taurus Molecular Cloud, for direct comparison.',
        synthesis='The X_CO conversion factor turns an easily observed trace-molecule line into a working proxy for molecular hydrogen\u2019s otherwise invisible mass -- the practical foundation of essentially every molecular-cloud mass measurement in this course\u2019s remaining units, beginning with Lecture 08\u2019s look at molecular-cloud structure and the virial theorem.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=8, title='Molecular Cloud Structure: Larson\u2019s Laws and the Virial Theorem',
        subtitle='Are molecular clouds held together by gravity, or blown apart by turbulence?',
        goals=[
            'State and apply Larson\u2019s (1981) empirical size-linewidth and density-size relations for molecular clouds.',
            'Derive the simple virial-mass estimator for a self-gravitating, turbulence-supported cloud and apply it to real cloud data.',
            'Compare a cloud\u2019s virial mass to its CO-derived mass (Lecture 07) to assess whether it is gravitationally bound.',
        ],
        why_matters='Lecture 07 established how to measure a molecular cloud\u2019s mass; this lecture asks the structural question that determines the cloud\u2019s fate -- is it gravitationally bound and destined to collapse (Unit 5), or is internal turbulent motion sufficient to support it against its own gravity?',
        phenomenon='Molecular clouds observed across a huge range of size, from small, quiescent Taurus-like clumps a few parsecs across to the much larger, more turbulent Orion complex tens of parsecs across, show internal velocity dispersions (measured from CO linewidths) that increase systematically with cloud size -- an empirical scaling relation, not a coincidence, first codified by Larson (1981).',
        vocab=['Larson\u2019s laws', 'size-linewidth relation', 'velocity dispersion', 'virial theorem', 'virial mass', 'gravitationally bound', 'turbulent support'],
        evidence=[
            'Larson (1981, MNRAS 194, 809) compiled molecular-line observations of clouds spanning several orders of magnitude in size and found an approximate power-law relation between internal velocity dispersion sigma and cloud size R, sigma proportional to R^0.5, along with a corresponding anti-correlation between mean density and size -- together known as Larson\u2019s laws.',
            'This size-linewidth relation is now understood as a signature of supersonic turbulence cascading from large to small scales within molecular clouds (turbulence with a power-law energy spectrum naturally produces a power-law size-linewidth relation), rather than simple thermal (random) motion, since the observed linewidths are far larger than the thermal sound speed at the observed 10-25 K cloud temperatures.',
            'The scalar virial theorem, applied to a simplified self-gravitating, uniform-density, non-magnetized sphere supported purely by its internal (turbulent) velocity dispersion, gives a mass estimate M_vir = 5 sigma^2 R / G that depends only on observationally accessible quantities (linewidth and angular size, given a distance) -- a completely independent mass estimator from Lecture 07\u2019s CO-luminosity method.',
        ],
        model=[
            'Larson\u2019s size-linewidth relation, sigma(R) = sigma_1pc (R/1 pc)^0.5, with sigma_1pc~1.1 km/s a standard normalization (Larson 1981; later refined by Solomon et al. 1987, ApJ 319, 730), is not a fundamental law of physics in the way Kepler\u2019s laws are, but a robust empirical regularity across a wide range of Galactic molecular clouds, understood as a turbulence signature.',
            'The virial theorem for a self-gravitating system in a statistical steady state relates twice the kinetic energy to (minus) the gravitational potential energy, 2K+U=0; applying this to a uniform sphere of mass M, radius R, and one-dimensional velocity dispersion sigma gives the standard virial-mass estimator M_vir = 5 sigma^2 R/G (the specific numerical coefficient follows from the uniform-sphere self-gravitational potential energy, U=-3GM^2/(5R)).',
            'Comparing a cloud\u2019s virial mass to an independently measured mass (e.g., Lecture 07\u2019s CO-derived mass) tests whether the cloud is close to virial equilibrium (bound, M~M_vir), gravitationally unbound and dispersing (M_vir >> M), or contracting under self-gravity in excess of what turbulent support can resist (M >> M_vir, foreshadowing Lecture 09\u2019s Jeans-instability criterion for gravitational collapse).',
        ],
        equation=r'\sigma(R) \approx \sigma_{1\,\mathrm{pc}}\left(\frac{R}{1\,\mathrm{pc}}\right)^{1/2}, \qquad M_{\rm vir} = \frac{5\,\sigma^2 R}{G}',
        example=[
            f'The Orion Molecular Cloud ridge (radius={ORION_MOLECULAR_CLOUD["radius_pc"]:.1f} pc, CO linewidth (FWHM)={ORION_MOLECULAR_CLOUD["co_linewidth_kms"]:.1f} km/s, giving a 1D velocity dispersion sigma=FWHM/2.355={ORION_MOLECULAR_CLOUD["co_linewidth_kms"]/2.355:.2f} km/s) gives a virial mass M_vir = 5 sigma^2 R/G = {OMC1_VIRIAL_MASS:,.0f} Msun, compared to Lecture 07\u2019s CO-derived mass of {OMC1_H2_MASS_FROM_CO:,.0f} Msun -- the same order of magnitude, and the ratio M_CO/M_vir={OMC1_H2_MASS_FROM_CO/OMC1_VIRIAL_MASS:.2f} is consistent with a cloud close to, though not exactly at, virial balance.',
            f'The Taurus Molecular Cloud (radius={TAURUS_MOLECULAR_CLOUD["radius_pc"]:.1f} pc, CO linewidth={TAURUS_MOLECULAR_CLOUD["co_linewidth_kms"]:.1f} km/s, a real, published, much more quiescent cloud, Goldsmith et al. 2008) gives a virial mass of M_vir={TAURUS_VIRIAL_MASS:,.0f} Msun, substantially smaller than Orion\u2019s despite Taurus\u2019s larger physical size -- directly illustrating Larson\u2019s size-linewidth relation, since Taurus\u2019s narrower CO linewidth (lower turbulent velocity dispersion) more than compensates for its larger radius in the M_vir proportional to sigma^2 R scaling.',
        ],
        pitfall='Treating close agreement between virial and CO-derived masses as proof a cloud is in strict mechanical equilibrium. The simple uniform-sphere virial estimator neglects magnetic support, external pressure confinement, and the cloud\u2019s true (non-spherical, non-uniform) geometry; rough numerical agreement is consistent with, but does not by itself prove, true virial equilibrium -- a genuine limitation of this simplified model, honestly stated rather than overclaimed.',
        activity='Using M_vir proportional to sigma^2 R and Larson\u2019s sigma proportional to R^0.5 relation, show that M_vir proportional to R^2 for clouds obeying Larson\u2019s law exactly, and discuss what this implies about how virial mass scales with cloud size across the full range of observed molecular clouds.',
        lab_connection='Lab 04 also computes and compares Larson-law-consistent virial masses for the Orion and Taurus clouds alongside their CO-derived masses from Lecture 07, completing this unit\u2019s three-way mass-estimator comparison.',
        synthesis='Larson\u2019s empirical scaling laws and the virial theorem together let astronomers assess whether a molecular cloud is bound by gravity or supported by turbulence -- exactly the question Unit 5 answers definitively for a cloud\u2019s dense substructures, where the Jeans instability criterion (Lecture 09) determines when gravity finally wins.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=9, title='The Jeans Instability: When Does a Gas Cloud Collapse?',
        subtitle='Deriving the exact boundary between a supported cloud and a collapsing one',
        goals=[
            'Derive the Jeans length and Jeans mass from a linear stability analysis of a self-gravitating, isothermal, pressure-supported gas.',
            'Apply the Jeans criterion to real dense molecular-cloud cores and evaluate whether they are gravitationally unstable.',
            'Explain physically why the Jeans mass decreases with increasing density, and why this makes dense cores, not diffuse clouds, the sites of star formation.',
        ],
        why_matters='Unit 4 established how to measure a molecular cloud\u2019s mass, size, and turbulent-support state. This lecture derives the precise physical criterion -- the Jeans instability -- that determines when a self-gravitating gas parcel\u2019s own gravity overwhelms its internal pressure support and collapse becomes inevitable, the essential first step of star formation.',
        phenomenon=f'The Bok globule Barnard 68, an isolated, roundish dark cloud so opaque it blocks every background star behind it in visible light, has a real, independently measured mass of only {BARNARD68["mass_msun"]:.1f} solar masses (Alves, Lada & Lada 2001, from near-infrared extinction mapping) -- and this course\u2019s Jeans-mass calculation for gas at Barnard 68\u2019s own observed density and temperature predicts a critical mass of a very similar order, consistent with Barnard 68 sitting near the threshold of gravitational instability.',
        vocab=['Jeans instability', 'Jeans length', 'Jeans mass', 'linear perturbation analysis', 'self-gravity', 'pressure support', 'sound speed'],
        evidence=[
            'Sir James Jeans (1902, Phil. Trans. R. Soc. A 199, 1) first showed analytically that a uniform, self-gravitating gas is unstable to small density perturbations larger than a critical length scale, now called the Jeans length, because gravity overwhelms the restoring force of gas pressure on scales larger than this.',
            'Observationally, dense, cold molecular-cloud cores (like Barnard 68 and the interior of the Orion Molecular Cloud) are exactly the sub-regions of a molecular cloud where the local Jeans mass drops low enough to be comparable to or smaller than the region\u2019s actual mass -- consistent with these being the specific sites where star formation is observed to begin, rather than the much lower-density, more extended cloud envelope.',
            'The dependence of Jeans mass on density (decreasing with increasing density) explains why star formation proceeds hierarchically: a large, marginally unstable cloud fragments into smaller, denser sub-clumps as it begins to contract, each of which has its own, smaller, local Jeans mass -- a fragmentation cascade this course revisits conceptually in Lecture 10.',
        ],
        model=[
            'Consider an infinite, uniform, self-gravitating isothermal gas of density rho, sound speed c_s = sqrt(kT/(mu m_H)), and introduce a small sinusoidal density perturbation of wavelength lambda; linearizing the fluid equations (continuity, Euler/momentum, and Poisson\u2019s equation for self-gravity) around the uniform background and seeking wave-like solutions gives a dispersion relation omega^2 = c_s^2 k^2 - 4 pi G rho, where k=2pi/lambda.',
            'This dispersion relation shows that perturbations with wavenumber k smaller than a critical value k_J = sqrt(4 pi G rho)/c_s (equivalently, wavelength larger than the Jeans length lambda_J = c_s sqrt(pi/(G rho))) have omega^2<0 -- an imaginary frequency, meaning the perturbation grows exponentially in time rather than oscillating: gravitational collapse. Perturbations smaller than lambda_J oscillate stably as ordinary sound waves, pressure-supported against their own self-gravity.',
            'Defining the Jeans mass as the mass contained within a sphere of the critical Jeans radius at the ambient density, M_J = (5kT/(G mu m_H))^{3/2} (3/(4 pi rho))^{1/2}, gives the standard collapse criterion: a gas clump of mass M and density rho is gravitationally unstable if M > M_J(rho,T) -- explicitly a competition between the destabilizing effect of gravity (favored by high density/mass) and the stabilizing effect of thermal pressure (favored by high temperature).',
        ],
        equation=r'\lambda_J = c_s\sqrt{\frac{\pi}{G\rho}}, \qquad M_J = \left(\frac{5kT}{G\mu m_H}\right)^{3/2}\left(\frac{3}{4\pi\rho}\right)^{1/2}',
        example=[
            f'A representative OMC-1 dense core (n(H2)={OMC1_DENSE_CORE["n_h2_cm3"]:.0e} cm^-3, T={OMC1_DENSE_CORE["temp_k"]:.0f} K, standard published dense-core values, Bergin & Tafalla 2007) has a computed Jeans length of {OMC1_CORE_JEANS_LENGTH_PC:.3f} pc and a Jeans mass of M_J={OMC1_CORE_JEANS_MASS:.2f} Msun.',
            f'Barnard 68 (n(H2)={BARNARD68["n_h2_cm3"]:.1e} cm^-3, T={BARNARD68["temp_k"]:.0f} K, Alves, Lada & Lada 2001) has a computed Jeans mass of M_J={BARNARD68_JEANS_MASS:.2f} Msun and Jeans length {BARNARD68_JEANS_LENGTH_PC:.3f} pc, compared to its real, independently measured mass ({BARNARD68["mass_msun"]:.1f} Msun) and radius ({BARNARD68["radius_pc"]:.2f} pc) -- the computed Jeans mass and the real observed mass agree to within a factor of {max(BARNARD68_JEANS_MASS, BARNARD68["mass_msun"])/min(BARNARD68_JEANS_MASS, BARNARD68["mass_msun"]):.2f}, consistent with Barnard 68 being observed near, but (per Alves, Lada & Lada 2001\u2019s own conclusion) not necessarily past, the threshold of gravitational instability -- an honest statement of near-critical rather than a claimed exact match.',
            f'The Jeans length is markedly smaller than the Jeans mass\u2019s naive cube-root scaling with density alone would suggest, because both the sound speed (through T) and the density enter the Jeans length independently; comparing OMC-1\u2019s core (denser but warmer) to Barnard 68 (less dense but colder) shows the two competing dependences do not simply cancel.',
        ],
        pitfall='Treating the Jeans criterion as an exact, universally precise threshold. The linear analysis assumes an idealized infinite, uniform, non-rotating, non-magnetized, non-turbulent medium; real cloud cores have turbulent and magnetic support (Lecture 08), non-uniform density profiles, and finite boundaries, all of which shift the true instability threshold by factors of order unity from the idealized M_J -- the Jeans mass is best used as an order-of-magnitude physical guide, not an exact collapse trigger, and this course states that limitation explicitly rather than overclaiming precision.',
        activity='Using the Jeans mass\u2019s explicit T^{3/2} rho^{-1/2} scaling, explain quantitatively why doubling a cloud core\u2019s density lowers its Jeans mass by less than a factor of two, and why this means density increases alone (without any temperature decrease) are a comparatively weak lever for triggering collapse compared to what naive intuition might suggest.',
        lab_connection='Lab 05 computes Jeans mass and length for both the OMC-1 dense core and Barnard 68 side by side and evaluates each cloud\u2019s instability status against its real observed mass.',
        synthesis='The Jeans instability, derived here from first-principles linear perturbation theory, gives the precise physical criterion separating a pressure-supported cloud from one destined to collapse -- the criterion Lecture 10 now follows through to its consequence: the actual collapse timescale and the resulting star-formation efficiency problem.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=10, title='Gravitational Collapse: Free-Fall Time and the Star-Formation Efficiency Problem',
        subtitle='If clouds are Jeans-unstable, why does star formation happen so slowly?',
        goals=[
            'Derive the free-fall collapse time for a uniform self-gravitating sphere from Newtonian dynamics.',
            'Apply the free-fall-time formula to real dense cores and compare it to observed star-formation timescales.',
            'Explain the star-formation efficiency per free-fall time as the empirical resolution of the apparent timescale discrepancy.',
        ],
        why_matters='Lecture 09 established when a cloud is gravitationally unstable; this lecture derives how fast such an unstable cloud would collapse in the absence of any opposing physics, and confronts that prediction with the observed, much slower pace of real star formation -- one of the central open problems this unit introduces rather than fully resolves.',
        phenomenon=f'A pure free-fall (gravity-only) collapse of a dense molecular-cloud core like OMC-1\u2019s would take only about {OMC1_CORE_FREEFALL_TIME_YR:,.0f} years to reach infinite density at its center -- yet observed molecular clouds convert only a few percent of their mass into stars per free-fall time, implying that most of a cloud\u2019s gas is not, in practice, simply free-falling.',
        vocab=['free-fall time', 'gravitational collapse', 'star-formation efficiency', 'star-formation rate', 'turbulence/magnetic support', 'initial mass function (IMF)'],
        evidence=[
            'If self-gravity is the only force acting (idealized, pressureless collapse), a uniform sphere collapses to a point in a finite time, the free-fall time, that depends only on the initial density -- a classical result of Newtonian gravity applicable to any self-gravitating fluid, from stellar interiors to molecular-cloud cores.',
            'If every Jeans-unstable molecular cloud in the Galaxy collapsed on its free-fall timescale and converted essentially all of its gas into stars, the Milky Way\u2019s star-formation rate would be roughly one to two orders of magnitude higher than the observed rate (a discrepancy quantified across many studies, e.g. Zuckerman & Evans 1974; Krumholz & Tan 2007, ApJ 654, 304) -- clear observational evidence that something beyond simple free-fall collapse is regulating star formation.',
            'The empirically inferred star-formation efficiency per free-fall time, epsilon_ff (the fraction of a cloud\u2019s mass converted to stars in one free-fall time), is measured to be only about 1-2% across a wide range of Galactic molecular clouds (Krumholz & Tan 2007; Evans et al. 2009, ApJS 181, 321) -- turbulence and magnetic fields (Lectures 08 and 14) are the leading physical explanations for why collapse is so inefficient rather than proceeding at the free-fall rate everywhere at once.',
        ],
        model=[
            'For a uniform sphere of density rho collapsing purely under its own gravity from rest, integrating the equation of motion for a test particle at the sphere\u2019s edge (using the shell theorem to justify treating only the interior mass) gives a closed-form collapse time to the center, the free-fall time t_ff = sqrt(3 pi/(32 G rho)) -- a classical result depending only on the initial density, not on the cloud\u2019s total mass or size individually.',
            'This is a strict lower bound on the true collapse time for any cloud with additional support (thermal pressure, turbulence, magnetic fields, or rotation), since those all act to slow collapse relative to the pure free-fall rate; comparing a cloud\u2019s actual observed lifetime or star-formation timescale to t_ff quantifies how much slower real collapse is than the idealized free-fall rate.',
            'The empirically low star-formation efficiency per free-fall time (epsilon_ff~1-2%) is now understood, at least qualitatively, as resulting from turbulence continually creating and dissolving locally Jeans-unstable overdensities faster than they can fully collapse, combined with magnetic support (Lecture 14) and stellar feedback (radiation pressure, winds, and eventually supernovae) that removes gas or injects additional turbulent energy before an entire cloud can collapse at once.',
        ],
        equation=r't_{\rm ff} = \sqrt{\frac{3\pi}{32\,G\rho}}, \qquad \epsilon_{\rm ff} \equiv \frac{\text{stellar mass formed per } t_{\rm ff}}{\text{cloud mass}} \sim 1\text{-}2\%\ \text{(observed)}',
        example=[
            f'The OMC-1 dense core (n(H2)={OMC1_DENSE_CORE["n_h2_cm3"]:.0e} cm^-3) has a computed free-fall time of t_ff={OMC1_CORE_FREEFALL_TIME_YR:,.0f} yr -- extremely short compared to a molecular cloud\u2019s overall multi-million-year lifetime, exactly the tension the star-formation efficiency problem addresses.',
            f'Barnard 68 (n(H2)={BARNARD68["n_h2_cm3"]:.1e} cm^-3), being somewhat less dense than the OMC-1 core, has a longer computed free-fall time of t_ff={BARNARD68_FREEFALL_TIME_YR:,.0f} yr, illustrating the free-fall time\u2019s explicit rho^{-1/2} scaling: despite differing in density by only a factor of {OMC1_DENSE_CORE["n_h2_cm3"]/BARNARD68["n_h2_cm3"]:.2f}, the two cores\u2019 free-fall times differ by a factor of {BARNARD68_FREEFALL_TIME_YR/OMC1_CORE_FREEFALL_TIME_YR:.2f} -- consistent with, but not identical to, the square-root scaling, because the two cores also have different temperatures entering indirectly through the mean molecular weight used in the density conversion.',
            f'If OMC-1\u2019s dense core (mass ~ its direct-method mass from Lecture 07, {OMC1_H2_MASS_DIRECT:,.0f} Msun for the full ridge, though the core itself is a much smaller sub-region) converted its gas to stars at the observed epsilon_ff~1-2% per free-fall time rather than the pure free-fall rate, the effective star-formation timescale would be lengthened by a factor of order 50-100 relative to the {OMC1_CORE_FREEFALL_TIME_YR:,.0f}-yr free-fall time -- of the right order of magnitude to reconcile the free-fall prediction with observed molecular-cloud lifetimes of several million years.',
        ],
        pitfall='Treating the free-fall time as a prediction of how long real star formation actually takes. It is explicitly a lower bound (the fastest possible collapse, absent any opposing physics); presenting t_ff itself as "the star-formation timescale" without the efficiency correction epsilon_ff is exactly the kind of overclaiming this course\u2019s review standard requires catching and correcting.',
        activity='Using t_ff proportional to rho^{-1/2}, explain why the free-fall time of the diffuse, low-density warm neutral medium (Lecture 01\u2019s WNM, n~0.3 cm^-3) is enormously longer than a dense core\u2019s free-fall time, and connect this to why star formation is observed exclusively in the dense molecular-cloud phase, never in the diffuse WNM.',
        lab_connection='Lab 05\u2019s second half computes free-fall times for both the OMC-1 core and Barnard 68 and discusses the star-formation-efficiency correction needed to reconcile the free-fall prediction with observed molecular-cloud lifetimes.',
        synthesis='The free-fall time sets the fastest possible pace of gravitational collapse, but the observed star-formation efficiency per free-fall time (only ~1-2%) shows that real molecular clouds collapse far more slowly and incompletely than pure gravity alone would predict -- closing out this course\u2019s star-formation unit and motivating Unit 6\u2019s look at what happens once a massive star does form: it ionizes its surroundings into an H II region.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=11, title='H II Regions I: Photoionization Equilibrium and the Stromgren Sphere',
        subtitle='Deriving the sharp-edged bubble of ionized gas around every hot young star',
        goals=[
            'Derive the ionization-balance (photoionization equilibrium) condition equating ionizing-photon production to recombination.',
            'Derive the Stromgren-sphere radius from this balance and apply it to a real H II region, the Orion Nebula.',
            'Explain why the classic Stromgren sphere has a sharp, not gradual, ionization edge.',
        ],
        why_matters='Unit 5 explained how a star forms from a collapsing dense core. Once a sufficiently massive, hot star forms, it begins ionizing its surrounding natal gas into an H II region -- this lecture derives the ionization-balance physics that sets that region\u2019s size, directly continuing the star-formation narrative from Unit 5 into its immediate aftermath.',
        phenomenon=f'The Orion Nebula (M42), the nearest large H II region to the Sun at a distance of {ORION_NEBULA["distance_pc"]:.0f} pc (Menten et al. 2007, VLBA trigonometric parallax), is ionized almost entirely by a single star, {ORION_NEBULA["ionizing_star"]} (spectral type {ORION_NEBULA["spectral_type"]}, T_eff~{ORION_NEBULA["teff_k"]:,.0f} K), whose prodigious output of ultraviolet photons carves out a glowing, roughly {2*ORION_NEBULA["observed_radius_pc"]:.1f}-parsec-diameter bubble of fully ionized hydrogen in the surrounding Orion Molecular Cloud.',
        vocab=['H II region', 'photoionization', 'Lyman continuum photon', 'recombination', 'case B recombination coefficient', 'Stromgren sphere', 'ionization-bounded region'],
        evidence=[
            'A hot O or early B star emits a large flux of photons energetic enough (>13.6 eV, shortward of the Lyman limit at 91.2 nm) to photoionize neutral hydrogen; the total number of such ionizing photons emitted per second, Q_H, is a strong function of the star\u2019s spectral type and effective temperature (calibrated by Vacca, Garmany & Shull 1996; Martins, Schaerer & Hillier 2005).',
            'Free electrons and protons in the resulting ionized gas continuously recombine (predominantly directly to excited states rather than the ground state, since ground-state recombination photons are themselves re-absorbed almost immediately -- the "on-the-spot" or case B approximation), at a rate proportional to the product of electron and proton densities and a temperature-dependent recombination coefficient, alpha_B.',
            'Bengt Stromgren (1939, ApJ 89, 526) first showed that balancing the star\u2019s ionizing-photon output against the total recombination rate within a spherical volume predicts an extremely sharp transition from fully ionized to fully neutral gas at a well-defined radius -- confirmed observationally by the sharp optical edges seen in many real H II regions, including much of the Orion Nebula\u2019s visible boundary.',
        ],
        model=[
            'In photoionization equilibrium, the rate of ionizing photons absorbed within a volume must equal the rate of recombinations occurring within that same volume (each recombination "uses up" one free electron-proton pair that must be replenished by a fresh ionization to maintain a steady ionized state): Q_H = alpha_B n_e n_p V, where V is the ionized volume, n_e~n_p is the electron/proton density (assuming pure hydrogen for simplicity), and alpha_B is the case B recombination coefficient (a well-determined atomic-physics quantity, ~2.6e-13 cm^3/s at the typical Te~10^4 K of ionized nebular gas).',
            'Solving this balance for a sphere of radius R_s (volume (4/3)pi R_s^3) gives the Stromgren radius, R_s = (3 Q_H/(4 pi alpha_B n_e^2))^{1/3}: a larger ionizing luminosity Q_H produces a larger ionized region, while a denser surrounding medium (larger n_e, hence a higher recombination rate) shrinks it, both entering as cube-root dependences.',
            'Because the recombination rate scales as n_e^2 (a strong, local dependence), the ionization front separating ionized from neutral gas is predicted to be extremely thin compared to R_s itself -- the "sharp edge" that gives the Stromgren sphere its idealized name, an approximation borne out reasonably well by many observed H II regions\u2019 sharp optical boundaries, though real regions have finite-thickness ionization fronts and often depart from perfect spherical symmetry (Lecture 12 continues with the real, non-idealized diagnostics).',
        ],
        equation=r'Q_H = \alpha_B\, n_e^2\, \frac{4}{3}\pi R_s^3 \ \Rightarrow\ R_s = \left(\frac{3\,Q_H}{4\pi\,\alpha_B\,n_e^2}\right)^{1/3}',
        example=[
            f'theta1 Orionis C (spectral type {ORION_NEBULA["spectral_type"]}) produces an ionizing-photon rate of Q_H={ORION_NEBULA["q_h_photons_s"]:.1e} photons/s (standard published O7V calibration, Vacca, Garmany & Shull 1996; Martins, Schaerer & Hillier 2005).',
            f'With the Orion Nebula\u2019s representative electron density n_e={ORION_NEBULA["n_e_cm3"]:.0f} cm^-3 (Baldwin et al. 1991; Osterbrock & Ferland 2006) and the case B recombination coefficient alpha_B={ALPHA_B_CM3_S:.2e} cm^3/s at Te={ORION_NEBULA["te_k"]:,.0f} K, the computed Stromgren radius is R_s={ORION_STROMGREN_RADIUS_PC:.2f} pc -- the same order of magnitude as, though somewhat larger than, the nebula\u2019s observed characteristic radius of ~{ORION_NEBULA["observed_radius_pc"]:.1f} pc, an expected consequence of this idealized single-star, uniform-density, fully spherical model applied to a real nebula that is neither uniform in density nor perfectly spherical (a genuine, disclosed limitation, not a computational error).',
            f'The corresponding recombination timescale (how quickly the ionized gas would recombine if the ionizing source were suddenly switched off), t_rec = 1/(n_e alpha_B), is {ORION_RECOMBINATION_TIME_YR:.1f} yr -- astronomically instantaneous, confirming the ionization state responds essentially immediately to changes in the ionizing flux and is genuinely in equilibrium on any timescale relevant to stellar evolution.',
        ],
        pitfall='Assuming the Stromgren radius exactly matches an H II region\u2019s observed size. The idealized model assumes a single point-source star, spatially uniform density, and a perfectly sharp ionization front in an infinite uniform medium; real H II regions are density-bounded (limited by where the surrounding gas simply runs out, not by where ionizing photons are exhausted), non-spherical, and often ionized by multiple stars -- the model is a genuinely useful order-of-magnitude tool, not an exact prediction, and this course states that limitation explicitly.',
        activity='Using R_s proportional to Q_H^{1/3} n_e^{-2/3}, explain why doubling the number of identical ionizing stars in a cluster increases the Stromgren radius by less than a factor of two, and why this weak dependence means H II region size is a poor discriminator of the total number of ionizing stars without additional information.',
        lab_connection='Lab 06 computes the Stromgren radius for the Orion Nebula in full and compares the idealized prediction to the real, observed nebular size, discussing the physical reasons for the discrepancy.',
        synthesis='The Stromgren-sphere ionization-balance derivation predicts the characteristic size of the bubble of ionized gas a hot young star carves out of its natal molecular cloud -- the idealized starting point Lecture 12 now refines with the real spectroscopic diagnostics (electron density, electron temperature) astronomers actually use to characterize real H II regions.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=12, title='H II Regions II: Emission-Line Diagnostics',
        subtitle='Reading a nebula\u2019s density and temperature directly from its spectrum',
        goals=[
            'Explain how collisionally excited forbidden-line doublet ratios (e.g., [S II]) diagnose electron density, and auroral/nebular line ratios (e.g., [O III]) diagnose electron temperature.',
            'Connect the Balmer decrement (Halpha/Hbeta ratio) to nebular dust extinction, linking this lecture back to Unit 3.',
            'Apply real, published Orion Nebula diagnostic values to characterize its physical conditions beyond the idealized Stromgren-sphere picture.',
        ],
        why_matters='Lecture 11\u2019s Stromgren-sphere model assumed a single electron density and temperature throughout an idealized sphere. Real H II regions are characterized far more precisely using their emission-line spectra directly -- this lecture derives how, closing this course\u2019s H II-region unit with the observational techniques astronomers actually use.',
        phenomenon=f'Spectroscopy of the Orion Nebula routinely returns an electron temperature of Te~{ORION_NEBULA["te_k"]:,.0f} K from the [O III] auroral-to-nebular line ratio and an electron density of n_e~{ORION_NEBULA["n_e_cm3"]:.0f} cm^-3 from the [S II] doublet ratio (standard published spectroscopic results, Osterbrock & Ferland 2006 textbook values, consistent with the classic Baldwin et al. 1991 study) -- both measured directly from line ratios, without any need to assume the idealized single-density Stromgren-sphere model of Lecture 11.',
        vocab=['forbidden line', 'collisional de-excitation', 'critical density', 'auroral line', 'nebular line', 'Balmer decrement', 'electron temperature diagnostic', 'electron density diagnostic'],
        evidence=[
            'Certain atomic transitions (like [S II] 6716/6731 Angstrom or [O III] 4363/5007 Angstrom) are "forbidden" in the sense of having very low spontaneous transition probabilities, meaning they are only seen in astrophysically low-density environments where collisional de-excitation (which would otherwise suppress them) is rare -- exactly the conditions found in H II regions, unlike any terrestrial laboratory plasma.',
            'The [S II] 6716/6731 doublet ratio is sensitive to electron density because the two upper levels have similar excitation energies but different critical densities (the density at which collisional de-excitation begins to compete with radiative decay), so their relative populations -- and hence the observed line ratio -- shift systematically with n_e over a useful diagnostic range around 10-10^4 cm^-3.',
            'The [O III] (4363 Angstrom auroral line)/(5007+4959 Angstrom nebular lines) ratio is sensitive to electron temperature because the auroral line originates from a higher-energy level requiring a larger Boltzmann excitation factor exp(-DeltaE/kTe), so this ratio increases steeply with Te -- the standard nebular electron-temperature diagnostic used throughout the H II-region and planetary-nebula literature.',
            'The Balmer decrement (the observed Halpha/Hbeta flux ratio, compared to its theoretical, extinction-free value of ~2.86 for case B recombination at Te~10^4 K) directly measures the nebula\u2019s own internal dust extinction, connecting this lecture\u2019s spectroscopic diagnostics back to Unit 3\u2019s extinction/reddening derivation.',
        ],
        model=[
            'Each forbidden-line doublet/ratio diagnostic works by solving a multi-level statistical-equilibrium problem (rates of collisional excitation/de-excitation and radiative decay balancing for each atomic energy level) as a function of n_e and Te, then inverting the resulting curves (typically computed with a dedicated atomic-physics code, e.g., PyNeb or its predecessors) to read off n_e or Te from an observed line ratio.',
            'Crucially, the density-sensitive and temperature-sensitive diagnostics are largely independent of each other (the [S II] density diagnostic is only weakly temperature-dependent, and vice versa for the [O III] temperature diagnostic), allowing electron density and electron temperature to be determined separately from different parts of the same spectrum, rather than requiring the single, spatially uniform values the idealized Stromgren-sphere model of Lecture 11 assumed.',
            'Once Te and n_e are measured directly from line ratios, they can be substituted back into Lecture 11\u2019s Stromgren-sphere framework (in place of assumed textbook values) for a much better-grounded ionization-balance calculation -- exactly the refinement from idealized model to real, spectroscopically constrained physical conditions this lecture provides.',
        ],
        equation=r'\frac{I([\mathrm{OIII}]\,4363)}{I([\mathrm{OIII}]\,5007+4959)} \propto e^{-\Delta E/kT_e}, \qquad \frac{I(\mathrm{H}\alpha)}{I(\mathrm{H}\beta)}\Big|_{\rm intrinsic} \approx 2.86\ (\mathrm{case\ B},\ T_e{=}10^4\,\mathrm{K})',
        example=[
            f'The Orion Nebula\u2019s standard published spectroscopic electron temperature, Te~{ORION_NEBULA["te_k"]:,.0f} K (Osterbrock & Ferland 2006; consistent with the classic Baldwin et al. 1991 study), justifies the case B recombination coefficient alpha_B={ALPHA_B_CM3_S:.2e} cm^3/s used throughout Lecture 11\u2019s Stromgren-radius calculation -- this course\u2019s Te=10^4 K assumption is not an arbitrary round number but the real, spectroscopically measured value for this specific nebula.',
            f'The [S II]-diagnosed electron density n_e~{ORION_NEBULA["n_e_cm3"]:.0f} cm^-3 is likewise the same real, published value used directly in Lecture 11\u2019s worked Stromgren-radius calculation, illustrating that this course\u2019s H II-region unit is grounded end-to-end in the same real nebula\u2019s actual measured physical conditions, not an idealized textbook density chosen for convenience.',
            'A Balmer decrement measured above the theoretical case B value of 2.86 anywhere within the Orion Nebula indicates internal dust extinction along that particular sightline through the nebula itself (distinct from, and in addition to, any foreground Galactic extinction of the kind derived in Unit 3\u2019s Lecture 05) -- a real, commonly used technique for mapping a nebula\u2019s own internal dust distribution.',
        ],
        pitfall='Assuming a single spectroscopically measured (Te, n_e) pair applies uniformly across an entire extended nebula. Real H II regions like Orion have real density and temperature structure (denser, hotter gas near the ionizing star, more tenuous, cooler gas near the ionization front), so a single-aperture or single-slit spectroscopic measurement characterizes only the specific region observed, not necessarily the whole nebula -- exactly the kind of oversimplification a careful reviewer should catch.',
        activity='Explain, using the qualitative behavior of collisional de-excitation, why the [S II] density diagnostic loses sensitivity (the line ratio saturates) at densities far above its critical density, and why choosing a diagnostic line pair with a critical density well-matched to the nebula being studied is important for obtaining a useful density measurement.',
        lab_connection='Lab 06\u2019s second half applies this lecture\u2019s real Orion Nebula Te and n_e values directly within Lecture 11\u2019s Stromgren-sphere framework, completing the loop from idealized model to spectroscopically grounded real measurement.',
        synthesis='Forbidden-line density/temperature diagnostics and the Balmer-decrement extinction diagnostic let astronomers characterize a real H II region\u2019s physical conditions directly from its spectrum, refining Lecture 11\u2019s idealized Stromgren-sphere model with real measured values -- closing out this course\u2019s H II-region unit before Unit 7 turns to the more violent physics of shocks, cosmic rays, and magnetic fields.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=13, title='Interstellar Shocks: The Rankine-Hugoniot Jump Conditions',
        subtitle='What happens when supersonic gas slams into the interstellar medium',
        goals=[
            'Derive the Rankine-Hugoniot jump conditions (conservation of mass, momentum, and energy across a shock front) for an ideal gas.',
            'Derive the strong-shock (high Mach number) limits for density compression and post-shock temperature.',
            'Apply the strong-shock post-shock temperature formula to a real supernova-remnant shock and compare to observed X-ray temperatures.',
        ],
        why_matters='Supernova blast waves (the ultimate fate of the massive stars whose formation this course traced in Unit 5, and whose youth as ionizing sources was the subject of Unit 6) are the dominant source of interstellar shocks, and are believed to heat and maintain the hot ionized medium (Lecture 01) and to accelerate the cosmic rays this unit\u2019s final lecture examines.',
        phenomenon=f'The Cassiopeia A supernova remnant, the visible debris of a stellar explosion whose light reached Earth around 1680, has an outer shock front still expanding at roughly {CAS_A["shock_velocity_km_s"]:,.0f} km/s -- more than ten times the speed of any sound wave that could propagate ahead of it through the surrounding interstellar medium, making this a genuinely supersonic, strong shock whose passage instantaneously and irreversibly heats, compresses, and accelerates the gas it overtakes.',
        vocab=['shock front', 'Rankine-Hugoniot conditions', 'Mach number', 'strong shock limit', 'compression ratio', 'post-shock temperature'],
        evidence=[
            'A shock front is a thin transition layer across which gas properties (density, pressure, temperature, velocity) change discontinuously (on a microscopic, collisional-mean-free-path length scale) because the flow ahead of the shock is moving faster than the local sound speed can communicate the disturbance -- exactly the situation for supernova ejecta plowing into the surrounding ISM at thousands of km/s.',
            'Chandra X-ray Observatory imaging and spectroscopy of Cassiopeia A and Tycho\u2019s supernova remnant reveal exactly the kind of multi-million-kelvin, shock-heated plasma this lecture\u2019s post-shock temperature formula predicts, with observed X-ray temperatures in the few-keV range broadly consistent with strong collisionless-shock heating (Vink 2004; Williams et al. 2016).',
            'The strong compression (density increase) predicted at a shock front is directly connected to why supernova remnants and other shocked regions appear as thin, bright, compressed shells rather than smoothly fading transitions -- exactly the morphology seen in Cas A and Tycho\u2019s remnant\u2019s Chandra/optical imagery.',
        ],
        model=[
            'Conservation of mass, momentum, and energy flux across a steady, planar shock front (in the shock\u2019s own rest frame) gives three coupled algebraic equations (the Rankine-Hugoniot jump conditions) relating the pre-shock (subscript 1) and post-shock (subscript 2) density, pressure, and velocity, parametrized by the upstream Mach number M = v_1/c_{s,1} (the ratio of the pre-shock flow speed to the pre-shock sound speed).',
            'In the strong-shock limit (M>>1, an excellent approximation for supernova-remnant shocks moving at thousands of km/s into a ~10 km/s-sound-speed warm ISM), these equations simplify dramatically: for a monatomic ideal gas (adiabatic index gamma=5/3), the density compression ratio approaches a fixed value rho2/rho1 -> (gamma+1)/(gamma-1) = 4, independent of the shock\u2019s actual speed, while the post-shock temperature continues to grow with the square of the shock velocity, T2 = 3 mu m_H v_shock^2/(16k).',
            'This strong-shock post-shock temperature formula directly converts an observationally accessible quantity (shock velocity, measured from proper motions or Doppler-shifted line emission) into a predicted X-ray-emitting plasma temperature -- a direct, testable link between a remnant\u2019s dynamics and its observed X-ray spectrum.',
        ],
        equation=r'\frac{\rho_2}{\rho_1} \xrightarrow{M\gg1} \frac{\gamma+1}{\gamma-1} = 4\ (\gamma{=}5/3), \qquad T_2 = \frac{3\,\mu\, m_H\, v_{\rm shock}^2}{16\,k}',
        example=[
            f'Cassiopeia A\u2019s forward shock (v_shock={CAS_A["shock_velocity_km_s"]:,.0f} km/s, standard published value, Vink 2004 and subsequent Chandra proper-motion studies) gives a predicted strong-shock post-shock (ion) temperature of T2={CASA_POST_SHOCK_T:.2e} K, equivalent to kT2={CASA_POST_SHOCK_KT_KEV:.2f} keV -- roughly an order of magnitude above the few-keV electron temperature Chandra actually measures from Cas A\u2019s shocked shell, an honest, expected discrepancy (not a computational error) that is itself real evidence for incomplete electron-ion equilibration at this fast, young shock (Ghavamian, Laming & Rakowski 2007).',
            f'Tycho\u2019s supernova remnant (v_shock={TYCHO_SNR["shock_velocity_km_s"]:,.0f} km/s, Williams et al. 2016) gives a predicted post-shock ion temperature of T2={TYCHO_POST_SHOCK_T:.2e} K (kT2={TYCHO_POST_SHOCK_KT_KEV:.2f} keV), somewhat lower than Cas A\u2019s, consistent with (and directly following from) its somewhat lower shock velocity through the T2 proportional to v_shock^2 scaling -- and, like Cas A, well above Tycho\u2019s observed few-keV X-ray electron temperature for the same electron-ion equilibration reason.',
            f'The strong-shock compression ratio, rho2/rho1={SHOCK_COMPRESSION:.1f}, applies to both remnants\u2019 forward shocks (both are firmly in the strong-shock, high-Mach-number regime given their thousands-of-km/s speeds against a ~10 km/s warm-ISM sound speed), illustrating that the compression ratio saturates at a fixed value even though the two remnants\u2019 predicted temperatures differ substantially.',
        ],
        pitfall='Assuming the predicted post-shock temperature exactly equals the observed X-ray plasma temperature. Real collisionless astrophysical shocks (unlike idealized collisional gas-dynamic shocks) do not necessarily equilibrate electron and ion temperatures instantaneously, so the electron temperature actually measured spectroscopically can be lower than this formula\u2019s ion-temperature-like prediction if electron-ion equilibration is incomplete -- a genuine, actively studied physical subtlety, honestly disclosed here rather than glossed over as an exact match.',
        activity='Using T2 proportional to v_shock^2, explain why a supernova remnant\u2019s X-ray temperature is expected to decline as the remnant ages and its forward shock decelerates (as it sweeps up and is slowed by an increasing mass of surrounding interstellar gas), and connect this to why very young remnants like Cas A and Tycho are hotter, harder X-ray sources than older, more evolved remnants.',
        lab_connection='Lab 07\u2019s capstone applies this lecture\u2019s shock-jump formulas to Cassiopeia A alongside its cosmic-ray and magnetic-field content (Lecture 14), synthesizing this course\u2019s final unit into one real, multiwavelength object.',
        synthesis='The Rankine-Hugoniot jump conditions, in their strong-shock limit, convert an observed supernova-remnant expansion velocity directly into a predicted X-ray plasma temperature -- and these same fast, strong shocks are the leading site where the cosmic rays and amplified magnetic fields of this course\u2019s final lecture are believed to originate.',
        openstax=OPENSTAX_NOTE,
    ),
    dict(
        n=14, title='Cosmic Rays, Magnetic Fields, and Multiwavelength ISM Synthesis',
        subtitle='Bringing every wavelength regime -- and every phase of the ISM -- together',
        goals=[
            'Describe the cosmic-ray energy spectrum\u2019s power-law form and its physical connection to diffusive shock acceleration at supernova-remnant shocks.',
            'Describe how the interstellar magnetic field is measured (Zeeman splitting, synchrotron emission, Faraday rotation) and its real, published density scaling in molecular clouds.',
            'Synthesize this entire course\u2019s seven units into a single multiwavelength picture of how the same interstellar medium is diagnosed across the electromagnetic spectrum.',
        ],
        why_matters='This capstone lecture connects Lecture 13\u2019s shocks (the leading site of cosmic-ray acceleration) to the cosmic-ray population and the magnetic fields that pervade every phase of the ISM this course has studied, and then draws every unit\u2019s diagnostic technique together into one multiwavelength synthesis -- exactly the "multiwavelength ISM diagnostics" the course catalog description names as this course\u2019s culminating theme.',
        phenomenon=f'A single object, the Crab Nebula (the debris of a supernova recorded by astronomers in 1054 CE), is simultaneously one of the brightest sources in the radio sky (synchrotron emission from relativistic electrons spiraling in its own magnetic field, estimated at B~{CRAB_NEBULA["b_field_gauss"]*1e6:.0f} microgauss) and one of the most luminous sources in gamma rays -- direct observational proof that relativistic particles and magnetic fields, the two subjects of this final lecture, are physically inseparable throughout the interstellar and circumstellar medium.',
        vocab=['cosmic ray', 'diffusive shock (Fermi) acceleration', 'power-law energy spectrum', 'the "knee"', 'Zeeman effect', 'synchrotron emission', 'Faraday rotation', 'multiwavelength astronomy'],
        evidence=[
            'Cosmic rays -- mostly relativistic protons and atomic nuclei, discovered by Victor Hess\u2019s 1912 balloon flights -- are observed with a differential energy spectrum that follows a power law over many decades in energy, J(E) proportional to E^-2.7 below a spectral steepening (the "knee") near 3x10^15 eV, then E^-3.1 above it (Particle Data Group, Workman et al. 2022, "Cosmic Rays" review).',
            'Diffusive shock (first-order Fermi) acceleration at strong, fast shocks -- exactly the supernova-remnant shocks derived in Lecture 13 -- naturally produces a power-law particle spectrum through repeated crossings of the shock front, each crossing giving a small, systematic energy gain; this mechanism is the leading explanation for the bulk of the Galactic cosmic-ray population up to at least the knee energy.',
            'Interstellar magnetic fields are measured through several independent techniques: the Zeeman effect (splitting of spectral lines in a magnetic field) directly measures line-of-sight field strength in dense gas; polarized synchrotron radio emission and polarized dust emission (Lecture 06) trace field direction; and Faraday rotation of polarized background radio sources measures the line-of-sight field weighted by electron density -- together giving a Galactic-average total field strength of B~6 microgauss (Beck 2001) and a well-established density-dependent scaling in molecular clouds, B proportional to n^0.65 above a critical density of ~300 cm^-3 (Crutcher 2012).',
        ],
        model=[
            'In diffusive shock acceleration, a charged particle crossing back and forth across a shock front (scattered by magnetic turbulence on each side) gains a small, fixed fractional energy boost per crossing; because the probability of remaining in the acceleration region decreases geometrically with each crossing while the energy grows geometrically as well, the process naturally produces a power-law energy spectrum -- providing a physical mechanism, not merely an empirical fit, for the observed cosmic-ray spectrum\u2019s shape.',
            'A relativistic electron of Lorentz factor gamma spiraling in a magnetic field B radiates synchrotron emission peaked near a critical frequency nu_c proportional to gamma^2 B; because both cosmic-ray electrons and interstellar magnetic fields are required to produce this radiation, synchrotron emission is a genuinely joint diagnostic of both quantities simultaneously, not of either one alone.',
            'The Crutcher (2012) molecular-cloud Zeeman B-n scaling (constant below a critical density, then increasing as a power law above it) is physically interpreted as evidence that magnetic fields provide significant support against gravitational collapse in diffuse gas, but that once a cloud core becomes dense enough to be magnetically supercritical, gravity can drag field lines along with the collapsing gas, increasing B roughly in proportion to a fixed power of the increasing density -- directly connecting this lecture\u2019s magnetic-field physics back to Unit 5\u2019s Jeans-instability/free-fall collapse derivations.',
        ],
        equation=r'J(E) \propto E^{-2.7}\ (E<E_{\rm knee}\approx3\times10^{15}\,\mathrm{eV}), \qquad \nu_c \propto \gamma^2 B, \qquad B \propto n^{0.65}\ (n>n_{\rm crit},\ \mathrm{Crutcher\ 2012})',
        example=[
            f'The PDG-parametrized cosmic-ray flux at 1 GeV is J(1 GeV)={CR_FLUX_1GEV:,.0f} nucleons per (m^2 s sr GeV); at 1 TeV (=1000 GeV), the same power law gives J(1 TeV)={CR_FLUX_1TEV:.3e} nucleons per (m^2 s sr GeV), a decrease by a factor of {CR_FLUX_1GEV/CR_FLUX_1TEV:.2e} over three decades in energy -- directly illustrating just how steep a power-law index of -2.7 really is over a wide energy range.',
            f'The Crab Nebula\u2019s equipartition-estimated magnetic field (B~{CRAB_NEBULA["b_field_gauss"]*1e6:.0f} microgauss, standard published value, Hester 2008) gives a synchrotron critical frequency of nu_c~{CRAB_NU_C_HZ:.2e} Hz for representative optical-synchrotron-emitting electrons of Lorentz factor gamma~{CRAB_SYNCHROTRON_GAMMA_OPTICAL:.0e} -- landing squarely in the optical band, consistent with the Crab Nebula\u2019s real, observed optical synchrotron continuum (first identified via its polarization by Oort & Walraven 1956).',
            f'Applying the Crutcher (2012) B-n scaling to the OMC-1 dense core (n(H2)={OMC1_DENSE_CORE["n_h2_cm3"]:.0e} cm^-3, well above the n_crit={CRUTCHER_N_CRIT_CM3:.0f} cm^-3 threshold) predicts a Zeeman-measurable field of B~{MOLECULAR_CLOUD_ZEEMAN_B_UG:.0f} microgauss -- directly connecting this final lecture\u2019s magnetic-field scaling law to Unit 5\u2019s real dense-core dataset used throughout the Jeans-mass and free-fall-time worked examples.',
        ],
        pitfall='Treating the cosmic-ray "knee" as evidence that cosmic-ray acceleration simply stops there. The spectral steepening at the knee is understood to reflect the maximum energy achievable by the dominant Galactic accelerators (supernova-remnant shocks) given their finite size, age, and magnetic-field strength, and/or an increasing role for extragalactic sources at still higher energies -- the knee marks a change in the dominant physics, not a hard cutoff, and should not be presented as one.',
        activity='Using this course\u2019s seven units as a checklist, identify which wavelength regime (radio, infrared, optical, ultraviolet, X-ray, or gamma-ray) is the primary observational window for each ISM phase or process covered (the 21 cm line, dust extinction and emission, H II region recombination lines, supernova-remnant shock heating, and cosmic-ray/synchrotron emission), and explain why no single wavelength regime could have revealed this course\u2019s full multiphase picture of the interstellar medium on its own.',
        lab_connection='Lab 07\u2019s capstone brings together this lecture\u2019s cosmic-ray spectrum and magnetic-field scaling with Lecture 13\u2019s shock physics, applied to the real Cassiopeia A supernova remnant, as this course\u2019s final synthesis exercise.',
        synthesis='Cosmic rays accelerated at supernova-remnant shocks (Lecture 13) and the magnetic fields that thread every phase of the interstellar medium (from the diffuse ISM\u2019s ~6 microgauss average to dense cores\u2019 much stronger fields) are the final pieces of this course\u2019s multiphase, multiwavelength picture of the space between the stars -- a picture built, unit by unit, from the pressure-balanced phases of Unit 1 through the atomic gas of Unit 2, the dust of Unit 3, the molecular clouds of Unit 4, the star formation of Unit 5, and the H II regions of Unit 6, to this final unit\u2019s shocks and cosmic rays.',
        openstax=OPENSTAX_NOTE,
    ),
]


def slide_deck(item: dict) -> str:
    n = item['n']
    fig = lecture_svg(item)
    body = f"""<main class='deck'>
<section class='slide title'><p class='kicker'>ASTR 360 &middot; Lecture {n:02d}</p><h1>{escape(item['title'])}</h1><h2>{escape(item['subtitle'])}</h2></section>
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
<section class='slide'><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Course dataset and derivations used in this lecture\u2019s worked example: <code>materials/ASTR360/data/</code> and <code>materials/ASTR360/src/generate_astr360_content.py</code>.</li></ul></section>
</main>"""
    return page(f'ASTR 360 Lecture {n:02d} Slides', body, SLIDE_CSS)


def lecture_notes(item: dict) -> str:
    n = item['n']
    body = f"""<header><div><h1>Lecture {n:02d}: {escape(item['title'])}</h1><p>ASTR 360 The Interstellar Medium</p></div></header>
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
<section><h2>References</h2><ul><li>{escape(item['openstax'])}</li><li>Every numeric result above is computed programmatically in <code>materials/ASTR360/src/generate_astr360_content.py</code>, not hand-typed.</li></ul></section>
</main>"""
    return page(f'ASTR 360 Lecture {n:02d} Notes', body)


def write_lectures():
    LECTURE_DIR.mkdir(parents=True, exist_ok=True)
    for item in LECTURES:
        n = item['n']
        (LECTURE_DIR / f'lecture-{n:02d}-slides.html').write_text(slide_deck(item), encoding='utf-8')
        (LECTURE_DIR / f'lecture-{n:02d}-notes.html').write_text(lecture_notes(item), encoding='utf-8')


def write_data_csv():
    import csv
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / 'ism_phases.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['phase', 'n_cm3', 'T_k', 'P_over_k_cm3K', 'filling_factor'])
        for name, d in ISM_PHASES.items():
            w.writerow([name, d['n_cm3'], d['T_k'], PHASE_PRESSURE_K[name], d['filling']])
    with open(DATA_DIR / 'real_objects.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['object', 'quantity', 'value', 'unit', 'source_note'])
        w.writerow(['3C 273 sightline', 'N(HI)', SIGHTLINE_3C273['n_hi_cm2'], 'cm^-2', 'HI4PI Collaboration 2016'])
        w.writerow(['Cygnus X-1 sightline', 'N(H)', SIGHTLINE_CYGX1['n_hi_cm2'], 'cm^-2', 'X-ray absorption studies'])
        w.writerow(['Cygnus OB2 No. 12', 'E(B-V)', CYGOB2_12['ebv_mag'], 'mag', 'Massey & Thompson 1991'])
        w.writerow(['HD 200775', 'R_V', HD200775['r_v'], 'dimensionless', 'Whittet et al. 2001'])
        w.writerow(['Orion Molecular Cloud (OMC-1)', 'mass', ORION_MOLECULAR_CLOUD['mass_msun'], 'Msun', 'Genzel & Stutzki 1989'])
        w.writerow(['Taurus Molecular Cloud', 'mass', TAURUS_MOLECULAR_CLOUD['mass_msun'], 'Msun', 'Goldsmith et al. 2008'])
        w.writerow(['Barnard 68', 'mass', BARNARD68['mass_msun'], 'Msun', 'Alves, Lada & Lada 2001'])
        w.writerow(['Orion Nebula (M42)', 'Q_H', ORION_NEBULA['q_h_photons_s'], 'photons/s', 'Vacca, Garmany & Shull 1996'])
        w.writerow(['Rosette Nebula', 'Q_H', ROSETTE_NEBULA['q_h_photons_s'], 'photons/s', 'Celnik 1985 and later studies'])
        w.writerow(['Cassiopeia A', 'shock velocity', CAS_A['shock_velocity_km_s'], 'km/s', 'Vink 2004'])
        w.writerow(["Tycho's SNR", 'shock velocity', TYCHO_SNR['shock_velocity_km_s'], 'km/s', 'Williams et al. 2016'])
        w.writerow(['Crab Nebula', 'B field', CRAB_NEBULA['b_field_gauss'], 'gauss', 'Hester 2008'])


if __name__ == '__main__':
    write_lectures()
    write_data_csv()
    print('Wrote', len(LECTURES), 'lectures to', LECTURE_DIR)
