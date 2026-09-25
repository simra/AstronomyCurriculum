"""Lab and problem-set generator for ASTR330.

Depends on the shared constants and page()/CSS helpers in
generate_astr330_content.py so every number here traces back to the same
verified real data (Hyades cluster and PSR J0348+0432, live-verified this
session; Alpha Centauri AB, Sirius A/B, and standard solar-model values,
carried forward from ASTR230/ASTR310) used in the paired lectures. Run with
the project interpreter:
    python materials/ASTR330/src/generate_astr330_content.py
    python materials/ASTR330/src/generate_astr330_labs_psets.py
"""
from __future__ import annotations

import math
from html import escape

from generate_astr330_content import (
    CSS, page, li, LAB_DIR, PSET_DIR, DATA_DIR,
    SIGMA_SB, G_NEWTON, C_LIGHT, H_PLANCK, HBAR, K_BOLTZMANN, M_PROTON, SIGMA_THOMSON, EV_J,
    M_SUN_KG, R_SUN_M, L_SUN_W, AU_M, YEAR_S, PC_M, KM, SUN_TEFF, SUN_AGE_GYR,
    ALPHA_CEN_A, ALPHA_CEN_B, SIRIUS_A, SIRIUS_B, HYADES, PSR_J0348,
    stefan_boltzmann_luminosity_w, hydrostatic_central_pressure_pa,
    kramers_opacity_estimate, electron_scattering_opacity_m2_per_kg,
    radiative_gradient_dimensionless, adiabatic_temperature_gradient_ideal_monatomic,
    gamow_peak_energy_kev, epsilon_pp_relative, epsilon_cno_relative,
    mass_luminosity_lsun, ms_lifetime_gyr, chandrasekhar_mass_kg,
    white_dwarf_cooling_age_gyr, triple_alpha_q_value_mev,
    SUN_CENTRAL_PRESSURE_EST, SUN_CENTRAL_PRESSURE_PUBLISHED,
    SUN_CORE_TEMP_PUBLISHED, SUN_CORE_DENSITY_PUBLISHED,
    KAPPA_ES_SUN, KAPPA_KRAMERS_SUN_CORE,
    SUN_ENVELOPE_RADIUS_FRAC, SUN_ENVELOPE_TEMP_K, SUN_ENVELOPE_MASS_ENCLOSED_KG,
    SUN_ENVELOPE_PRESSURE_EST, SUN_RADIATIVE_GRADIENT, SUN_ADIABATIC_GRADIENT_FRACTIONAL,
    SUN_SURFACE_ZONE_TEMP_K, SUN_SURFACE_ZONE_PRESSURE_PA, SUN_SURFACE_ZONE_DENSITY_KGM3,
    KAPPA_SURFACE_ZONE, SUN_SURFACE_ZONE_MASS_ENCLOSED_KG, SUN_SURFACE_RADIATIVE_GRADIENT,
    GAMOW_E0_PP_SUN_KEV, GAMOW_E0_CNO_SUN_KEV, T6_SUN_CORE, SIRIUS_A_CORE_TEMP_EST_K, T6_SIRIUS_A_CORE,
    EPS_PP_SUN, EPS_CNO_SUN, EPS_PP_SIRIUS_A, EPS_CNO_SIRIUS_A,
    PP_CNO_CROSSOVER_T6, CNO_NORMALIZATION, PP_CNO_CROSSOVER_TEMP_K,
    PP_CHAIN_Q_MEV, CNO_CYCLE_Q_MEV, TRIPLE_ALPHA_Q_MEV,
    ALPHA_CEN_A_ML_PRED_LSUN, ALPHA_CEN_B_ML_PRED_LSUN, SIRIUS_A_ML_PRED_LSUN,
    SUN_MS_LIFETIME_CALC_GYR, ALPHA_CEN_A_MS_LIFETIME_GYR, ALPHA_CEN_B_MS_LIFETIME_GYR, SIRIUS_A_MS_LIFETIME_GYR,
    HYADES_TURNOFF_L_PRED_LSUN, HYADES_TURNOFF_LIFETIME_PRED_GYR, HYADES_ACTUAL_AGE_GYR, HYADES_AGE_DISCREPANCY_FACTOR,
    CHANDRASEKHAR_MASS_MUE2_KG, CHANDRASEKHAR_MASS_MUE2_MSUN, SIRIUS_B_TO_CHANDRA_FRACTION,
    SIRIUS_B_LUM_LSUN, SIRIUS_B_COOLING_AGE_GYR,
    PSR_TO_CHANDRA_FRACTION, PSR_WD_TO_CHANDRA_FRACTION, PSR_NS_MEAN_DENSITY_KGM3,
    NUCLEAR_SATURATION_DENSITY_KGM3, PSR_NS_DENSITY_TO_NUCLEAR_FRACTION,
    SN_CORE_MASS_MSUN, SN_PROGENITOR_CORE_RADIUS_M, SN_REMNANT_RADIUS_M,
    SN_BINDING_ENERGY_RELEASED_J, SN_OBSERVED_KINETIC_PLUS_LIGHT_J, SN_NEUTRINO_FRACTION_ESTIMATE,
)

OPENSTAX = 'OpenStax Astronomy 2e (local reference copy: references/openstax-astronomy-2e-extracted.txt)'


def fmt(x, nd=2):
    return f"{x:.{nd}f}"


def problem(i: int, heading: str, body: str, points: int = 15) -> str:
    return f'<article class="problem"><h3>{i}. {escape(heading)} <span class="points">{points} points</span></h3>{body}</article>'


def solution(i: int, heading: str, body: str, rubric) -> str:
    rows = ''.join(f'<tr><td>{escape(k)}</td><td>{v}</td></tr>' for k, v in rubric)
    return (
        f'<article class="problem"><h3>{i}. {escape(heading)}</h3>{body}'
        f'<table><tr><th>Criterion</th><th>Points</th></tr>{rows}</table></article>'
    )


def lab_page(n: int, title: str, focus: str, sections: str) -> str:
    body = f"<header><div><h1>Lab {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header><main>{sections}</main>"
    return page(f'ASTR 330 Lab {n:02d}', body)


def pset_page(n: int, title: str, focus: str, problems_html: str, reading: str) -> str:
    body = f"""<header><div><h1>ASTR 330 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header>
<main><section><h2>Problems</h2>{problems_html}</section>
<section><h2>Due and Scope</h2><p>Submit a complete derivation with equations, units, labeled quantities, and a short narrative interpretation for each problem. Show every step; a correct final number without a visible derivation receives partial credit at most, and quoting a lecture number without adapting it to this problem's specific inputs receives no credit for that step.</p></section>
<section><h2>OpenStax Companion Reading</h2><p>{escape(reading)}</p></section>
<section><h2>References and Data Sources</h2><ul><li>Corresponding lecture slides and notes for this unit.</li><li>{OPENSTAX}.</li><li>Course datasets under <code>materials/ASTR330/data/</code> where referenced above.</li></ul></section>
</main>"""
    return page(f'ASTR 330 Problem Set {n:02d}', body)


def solutions_page(n: int, title: str, solutions_html: str) -> str:
    body = f"<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header><main><section><h2>Worked Solutions</h2>{solutions_html}</section><section><h2>Grading Notes</h2><p>Award full marks for correct method, units, and a numeric result consistent with the arithmetic shown (allow reasonable rounding). Verify that the student re-derives the number for this problem's specific inputs rather than quoting a lecture example without adaptation. Watch specifically for unit-conversion errors (km/AU/m, years/seconds, kg/M&#8857;) and for comparative-magnitude statements stated in the wrong direction (e.g., \"X times greater\" versus \"a small fraction of\") -- these are the most common sources of order-of-magnitude mistakes in this course.</p></section></main>"
    return page(f'ASTR 330 Problem Set {n:02d} Solutions', body)


def assessment_md(n: int, title: str, criteria: list, common_errors: list) -> str:
    crit = '\n'.join(f'- {c}' for c in criteria)
    err = '\n'.join(f'- {e}' for e in common_errors)
    return f"""# Assessment Instructions: Problem Set {n:02d} \u2014 {title}

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the referenced dataset(s) under `materials/ASTR330/data/`.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking number but no visible derivation steps should not. Because this is a 300-level quantitative course exceeding ASTR 310's own rigor, full marks require a genuine derivation (not just formula substitution) wherever the problem set asks for one.

## Problem-Level Criteria
{crit}

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
{err}
"""


# ===========================================================================
# LAB 01: Sun two-zone model -- equation of state, opacity, hydrostatic estimate
# ===========================================================================
def make_lab_01() -> str:
    prad_pgas = (4 * SIGMA_SB / C_LIGHT / 3 * SUN_CORE_TEMP_PUBLISHED ** 4) / (
        (SUN_CORE_DENSITY_PUBLISHED * K_BOLTZMANN * SUN_CORE_TEMP_PUBLISHED) / (0.62 * M_PROTON))
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This is a data-analysis lab using the Sun's standard-model core conditions (standard published values, flagged for spot-check in <code>../reference-log.md</code>) together with the equation-of-state and opacity formalism of Lecture 02 and the hydrostatic-equilibrium estimate carried forward from ASTR 310, Lecture 05. No telescope time is required.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Sun mass, radius</td><td>{M_SUN_KG:.3e} kg, {R_SUN_M:.3e} m</td></tr>
<tr><td>Standard solar-model core density (published)</td><td>{SUN_CORE_DENSITY_PUBLISHED:.2e} kg/m&sup3;</td></tr>
<tr><td>Standard solar-model core temperature (published)</td><td>{SUN_CORE_TEMP_PUBLISHED:.3e} K</td></tr>
<tr><td>Standard solar-model central pressure (published)</td><td>{SUN_CENTRAL_PRESSURE_PUBLISHED:.3e} Pa</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute the uniform-density hydrostatic central-pressure estimate P_c &asymp; (3/8&pi;)GM&sup2;/R&#8308; and compare it (percent difference) to the published standard-solar-model value.</li>
<li>Compute the electron-scattering opacity &kappa;_es = &sigma;_T(1+X)/(2m_p) for X = 0.70, and the schematic Kramers-law opacity &kappa;_Kramers at the published core density and temperature, and compare the two.</li>
<li>Compute the radiation-to-gas pressure ratio P_rad/P_gas at the published core density and temperature (using &mu; = 0.62 for fully ionized solar composition), and state whether radiation pressure is negligible, comparable to, or dominant over gas pressure in the Sun's core.</li>
<li>Using the equation of state P = &rho;kT/(&mu;m_p) + (1/3)aT&#8308;, compute the total pressure implied by the published core density and temperature, and compare it (percent difference) to the published central pressure used in step 1.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The uniform-density hydrostatic estimate in step 1 ignores the Sun's true, centrally concentrated density profile; state whether the direction of the discrepancy you find (over- or under-estimate) is consistent with the same discrepancy direction found for the same calculation in ASTR 310, Lab 03.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed central-pressure, opacity, and pressure-ratio calculations with full unit conversions shown.</li><li>Written comparison of the equation-of-state pressure (step 4) to the published central pressure.</li><li>Written discussion of the hydrostatic-estimate discrepancy direction, cross-checked against ASTR 310.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct unit conversions and arithmetic in all four steps.</li><li>Correct qualitative and quantitative classification of the radiation-to-gas pressure ratio.</li><li>Valid cross-check against the ASTR 310 Lab 03 precedent for the hydrostatic-estimate discrepancy direction.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 16.1-16.2.</li><li>Standard solar-model core density, temperature, and central pressure: standard published values, not independently re-verified this session; see <code>materials/ASTR330/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR330/src/generate_astr330_content.py</code>.</li></ul></section>
"""
    return lab_page(1, 'Building a Two-Zone Model of the Sun: Equation of State, Opacity, and Hydrostatic Pressure',
                     'Apply the equation of state and opacity formalism of Lecture 02 to the Sun\u2019s published core conditions and cross-check against the hydrostatic-equilibrium estimate from ASTR 310.', sections)


# ===========================================================================
# LAB 02: Radiative vs. convective transport in the solar envelope
# ===========================================================================
def make_lab_02() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab evaluates the dimensionless radiative temperature gradient &nabla;_rad (Lecture 03) at two illustrative solar-envelope sample points and applies the Schwarzschild criterion (Lecture 04) to classify each as radiative or convective, reproducing (with schematic, order-of-magnitude opacity coefficients rather than full OPAL/OP tables) the Sun's real radiative-core/convective-envelope structure.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Sample point</th><th>T (K)</th><th>P (Pa)</th><th>&rho; (kg/m&sup3;)</th><th>&kappa; (m&sup2;/kg)</th></tr></thead><tbody>
<tr><td>Deep envelope (r &asymp; {SUN_ENVELOPE_RADIUS_FRAC:.1f} R&#8857;)</td><td>{SUN_ENVELOPE_TEMP_K:.1e}</td><td>{SUN_ENVELOPE_PRESSURE_EST:.1e}</td><td>electron-scattering (Lecture 02)</td><td>{KAPPA_ES_SUN:.4f}</td></tr>
<tr><td>Near-surface</td><td>{SUN_SURFACE_ZONE_TEMP_K:.1e}</td><td>{SUN_SURFACE_ZONE_PRESSURE_PA:.1e}</td><td>{SUN_SURFACE_ZONE_DENSITY_KGM3:.1e}</td><td>{KAPPA_SURFACE_ZONE:.2f} (schematic Kramers)</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using &nabla;_rad = 3&kappa;LP/(16&pi;acGMT&#8308;), compute &nabla;_rad at the deep-envelope sample point, showing every substituted value and its units.</li>
<li>Repeat the calculation at the near-surface sample point.</li>
<li>Compare each computed &nabla;_rad to the ideal monatomic-gas adiabatic gradient &nabla;_ad = 2/5, and classify each sample point as radiatively stable or convectively unstable using the Schwarzschild criterion.</li>
<li>The Sun's real convection-zone base is helioseismically measured at r &asymp; 0.713 R&#8857;. State whether your two classifications (steps 1-3) are qualitatively consistent with this real boundary, and explain in one paragraph which specific input (opacity, temperature, or pressure) is most responsible for the difference between your two computed &nabla;_rad values.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Both sample points use schematic, order-of-magnitude opacity coefficients (electron scattering exactly, Kramers-law approximately) rather than precision OPAL/OP tabulated opacities; state explicitly why this is an acceptable simplification for classifying stability (a qualitative radiative-versus-convective question) but would not be acceptable for computing the Sun's precise internal temperature profile.</p></section>
<section><h2>Deliverables</h2><ul><li>Both &nabla;_rad calculations with full substituted values and units.</li><li>Explicit Schwarzschild-criterion classification for each point.</li><li>Written paragraph connecting the results to the Sun's real convection-zone boundary and identifying the dominant driver of the difference between the two points.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct substitution and arithmetic in both &nabla;_rad calculations.</li><li>Correct Schwarzschild-criterion classification for each point.</li><li>Correct identification of opacity (not temperature or pressure alone) as the dominant driver of the difference between the two computed gradients.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 16.2.</li><li>Envelope temperature, pressure, and density sample values: standard published order-of-magnitude solar-model values, not independently re-verified this session.</li><li>Generated by <code>materials/ASTR330/src/generate_astr330_content.py</code>.</li></ul></section>
"""
    return lab_page(2, 'Radiative vs. Convective Energy Transport in the Solar Envelope',
                     'Compute the dimensionless radiative temperature gradient at two solar-envelope depths and apply the Schwarzschild criterion.', sections)


# ===========================================================================
# LAB 03: Gamow peak and pp/CNO crossover
# ===========================================================================
def make_lab_03() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes the Gamow peak energy (Lecture 05) for proton-proton and CNO-cycle reactions and reproduces the pp-chain/CNO-cycle crossover-temperature calculation (Lecture 06) for the Sun and for Sirius A, using the same schematic power-law energy-generation scalings developed in the lecture.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Star</th><th>Core temperature (K)</th><th>T6</th></tr></thead><tbody>
<tr><td>Sun (standard published core temperature)</td><td>{SUN_CORE_TEMP_PUBLISHED:.3e}</td><td>{T6_SUN_CORE:.2f}</td></tr>
<tr><td>Sirius A ({SIRIUS_A['mass_msun']:.3f} M&#8857;, schematic mass-scaling estimate)</td><td>{SIRIUS_A_CORE_TEMP_EST_K:.3e}</td><td>{T6_SIRIUS_A_CORE:.2f}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute the Gamow peak energy E0 for proton-proton reactions (Z1=Z2=1, &mu;=0.5 amu) at the Sun's core temperature, and compare it to kT at that same temperature.</li>
<li>Compute the Gamow peak energy for a proton-nitrogen-14 reaction (Z1=1, Z2=7, &mu;=12/13 amu, the CNO cycle's rate-limiting step) at the same temperature, and compare it to the pp-chain Gamow peak from step 1.</li>
<li>Using &epsilon;_pp &prop; T6&#8308; and &epsilon;_CNO &prop; T6&sup2;&#8304; (both normalized so the Sun is 1000:1 pp-dominated, per Lecture 06), find the crossover T6 at which the two curves are equal, and verify your answer is consistent with the value quoted in Lecture 06.</li>
<li>Using Sirius A's schematic core-temperature estimate, classify Sirius A as pp-dominated or CNO-dominated, and state whether this is consistent with real stellar models for a star of Sirius A's mass and spectral type.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The Sirius A core-temperature estimate uses a schematic mass-scaling relation (T_core &prop; M^0.7), not a precision stellar model; state explicitly why this is sufficient for a qualitative pp-versus-CNO classification but would not be sufficient for a precise nuclear-burning-rate calculation.</p></section>
<section><h2>Deliverables</h2><ul><li>Both Gamow-peak calculations with a comparison to kT.</li><li>The crossover-temperature calculation, reproduced independently of the lecture's own numbers.</li><li>Sirius A's pp/CNO classification with supporting arithmetic.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct Gamow-peak arithmetic for both reactions.</li><li>Correct, independently reproduced crossover-temperature calculation.</li><li>Correct pp/CNO classification for Sirius A with supporting numbers, not just an assertion.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 16.3.</li><li>Sirius A mass and spectral type: standard published values, carried forward from ASTR 230/ASTR 310.</li><li>Generated by <code>materials/ASTR330/src/generate_astr330_content.py</code>.</li></ul></section>
"""
    return lab_page(3, 'The Gamow Peak and the pp-Chain/CNO-Cycle Crossover Temperature',
                     'Compute Gamow peak energies and the pp/CNO crossover temperature, then classify the Sun and Sirius A.', sections)


# ===========================================================================
# LAB 04: Mass-luminosity relation and main-sequence lifetimes
# ===========================================================================
def make_lab_04() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab applies the mass-luminosity relation and main-sequence lifetime scaling (Lecture 07) to four real, precisely measured stars: the Sun, Alpha Centauri A and B, and Sirius A (all carried forward with established provenance from ASTR 230/ASTR 310).</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Star</th><th>Mass (M&#8857;)</th><th>Measured L (L&#8857;)</th></tr></thead><tbody>
<tr><td>Sun</td><td>1.000</td><td>1.000</td></tr>
<tr><td>{escape(ALPHA_CEN_A['name'])}</td><td>{ALPHA_CEN_A['mass_msun']:.4f}</td><td>{ALPHA_CEN_A['lum_lsun']:.4f}</td></tr>
<tr><td>{escape(ALPHA_CEN_B['name'])}</td><td>{ALPHA_CEN_B['mass_msun']:.4f}</td><td>{ALPHA_CEN_B['lum_lsun']:.4f}</td></tr>
<tr><td>{escape(SIRIUS_A['name'])}</td><td>{SIRIUS_A['mass_msun']:.3f}</td><td>{SIRIUS_A['lum_lsun']:.1f}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>For each of the three non-solar stars, compute the mass-luminosity prediction L &asymp; M^3.5 and the percent agreement with the measured luminosity in the data table.</li>
<li>For each of the four stars, compute the main-sequence lifetime estimate t_MS = 10 Gyr &times; (M/M&#8857;)/(L/L&#8857;) using the measured (not predicted) luminosity.</li>
<li>Rank the four stars by main-sequence lifetime, and state which single input (mass or luminosity) is most responsible for Sirius A having by far the shortest lifetime of the four.</li>
<li>The Sun's actual age is about {SUN_AGE_GYR:.2f} Gyr. Compare this to your computed solar main-sequence lifetime, and state what fraction of its total main-sequence lifetime the Sun has completed so far.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Sirius A's percent agreement (step 1) is expected to be noticeably worse than Alpha Centauri A/B's; state explicitly why a single fixed mass-luminosity exponent (3.5) is not expected to fit equally well across a wide range of stellar masses.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed mass-luminosity prediction table with percent agreements.</li><li>Completed main-sequence lifetime table for all four stars.</li><li>Written ranking and explanation of Sirius A's short lifetime.</li><li>Solar age-versus-lifetime comparison with the completed-fraction calculation.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct mass-luminosity and percent-agreement arithmetic for all three stars.</li><li>Correct lifetime arithmetic for all four stars.</li><li>Correct identification of luminosity (not mass alone) as the dominant driver of Sirius A's short lifetime.</li><li>Correct solar age-completed-fraction arithmetic.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 19.3.</li><li>All four stars' masses and luminosities: carried forward with established provenance from ASTR 230/ASTR 310 (see <code>materials/ASTR330/reference-log.md</code>).</li><li>Generated by <code>materials/ASTR330/src/generate_astr330_content.py</code>.</li></ul></section>
"""
    return lab_page(4, 'Mass-Luminosity Relation and Main-Sequence Lifetimes for Real Stars',
                     'Apply the mass-luminosity relation and lifetime scaling to the Sun, Alpha Centauri A/B, and Sirius A.', sections)


# ===========================================================================
# LAB 05: Hyades cluster main-sequence turnoff age
# ===========================================================================
def make_lab_05() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab reproduces the main-sequence turnoff age calculation for the Hyades open cluster (Lecture 09), using the cluster's live-verified distance, age, turnoff mass, and structural radii (fetched directly this session; see <code>../reference-log.md</code>).</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Distance</td><td>{HYADES['distance_pc']:.0f} pc</td></tr>
<tr><td>Independently measured (isochrone-fit) age</td><td>{HYADES['age_myr']:.0f} Myr</td></tr>
<tr><td>Main-sequence turnoff mass</td><td>{HYADES['turnoff_mass_msun']:.1f} M&#8857;</td></tr>
<tr><td>Total cluster mass</td><td>{HYADES['total_mass_msun']:.0f} M&#8857;</td></tr>
<tr><td>Core radius / half-mass radius / tidal radius</td><td>{HYADES['core_radius_pc']:.1f} / {HYADES['half_mass_radius_pc']:.1f} / {HYADES['tidal_radius_pc']:.0f} pc</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using L &asymp; M^3.5, compute the predicted luminosity of a {HYADES['turnoff_mass_msun']:.1f} M&#8857; turnoff star.</li>
<li>Using t_MS = 10 Gyr &times; M/L, compute the predicted main-sequence lifetime of a {HYADES['turnoff_mass_msun']:.1f} M&#8857; star from your Problem 1 luminosity.</li>
<li>Compare your predicted lifetime to the cluster's independently measured age ({HYADES['age_myr']:.0f} Myr), computing the ratio explicitly, and state honestly (not as "excellent agreement") how large the discrepancy is.</li>
<li>Using the cluster's total mass and tidal radius, estimate its mean mass density in M&#8857;/pc&sup3;, and compare this to its core-radius density (using the core radius instead of the tidal radius in the same formula), stating which is denser and by what factor.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly, using the ratio you computed in step 3, whether the fixed n=3.5 mass-luminosity exponent over- or under-predicts the true main-sequence lifetime for a 2.3 M&#8857; star, and connect this to Lecture 07's discussion of the exponent's mass-dependence.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed luminosity and lifetime predictions with full arithmetic.</li><li>An honest, explicitly quantified statement of the discrepancy between the predicted lifetime and the cluster's measured age (no "excellent agreement" language for a discrepancy of this size).</li><li>Both density estimates (core and tidal radius) with a comparison.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct mass-luminosity and lifetime arithmetic.</li><li>Explicit, correctly computed discrepancy ratio, honestly characterized (not overstated as close agreement).</li><li>Correct density arithmetic and comparison for both radii.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 21.1.</li><li>Hyades cluster distance, age, turnoff mass, total mass, and structural radii: live-verified this session via a direct web fetch of Wikipedia's "Hyades (star cluster)" article, citing Perryman et al. (1998), <em>A&amp;A</em> 331, 81; see <code>materials/ASTR330/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR330/src/generate_astr330_content.py</code>.</li></ul></section>
"""
    return lab_page(5, 'Dating the Hyades Open Cluster from Its Main-Sequence Turnoff',
                     'Reproduce the Hyades turnoff-age calculation and honestly evaluate the size of its discrepancy with the cluster\u2019s independently measured age.', sections)


# ===========================================================================
# LAB 06: Sirius B and the Chandrasekhar mass
# ===========================================================================
def make_lab_06() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes the Chandrasekhar mass from first principles (Lecture 12) and applies it to Sirius B, whose mass, radius, and temperature were independently live-verified in ASTR 230's production and carried forward through ASTR 310.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Sirius B mass</td><td>{SIRIUS_B['mass_msun']:.3f} M&#8857;</td></tr>
<tr><td>Sirius B radius</td><td>{SIRIUS_B['radius_rsun']:.6f} R&#8857;</td></tr>
<tr><td>Sirius B effective temperature</td><td>{SIRIUS_B['teff']:.0f} K</td></tr>
<tr><td>Fundamental constants</td><td>&#295; = {HBAR:.4e} J&middot;s, c = {C_LIGHT:.3e} m/s, G = {G_NEWTON:.4e} m&sup3;kg&#8315;&sup1;s&#8315;&sup2;, m_p = {M_PROTON:.4e} kg</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using M_Ch = (&omega;3&sup0;&radic;3&pi;/2)(&#295;c/G)^(3/2)/(&mu;_e m_p)&sup2; with &omega;3&sup0; = 2.018236 and &mu;_e = 2.0 (carbon-oxygen composition), compute the Chandrasekhar mass numerically, showing every substituted value.</li>
<li>Compute Sirius B's mass as a fraction (percent) of your computed Chandrasekhar mass, and state whether this is consistent with Sirius B's continued existence as a stable white dwarf.</li>
<li>Using the Stefan-Boltzmann law, compute Sirius B's luminosity from its measured radius and temperature, in solar luminosities.</li>
<li>Using the schematic Mestel-type cooling estimate t_cool &asymp; k_cool &times; (M/M&#8857;) &times; (L/L&#8857;)^(-5/7) with k_cool = 0.015, estimate Sirius B's cooling age, and compare it (order of magnitude only) to the commonly cited age of the Sirius system (a few hundred Myr).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly that the cooling-age estimate in step 4 uses a schematic calibration constant (k_cool), not a full white-dwarf cooling-track model, and explain why this is acceptable for an order-of-magnitude age estimate but not for a precision cooling-age measurement.</p></section>
<section><h2>Deliverables</h2><ul><li>The full Chandrasekhar-mass derivation with every substituted constant shown.</li><li>Sirius B's mass-fraction-of-Chandrasekhar-mass calculation.</li><li>Sirius B's Stefan-Boltzmann luminosity calculation.</li><li>The cooling-age estimate with an explicit order-of-magnitude comparison to the Sirius system's commonly cited age.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct substitution and arithmetic in the Chandrasekhar-mass formula.</li><li>Correct mass-fraction and luminosity calculations.</li><li>Correct order-of-magnitude cooling-age estimate with an explicit, honestly qualified comparison.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 22.1-22.2.</li><li>Sirius B mass, radius, and temperature: live-verified in ASTR 230's production (Bond et al. 2017, <em>ApJ</em> 840, 70); carried forward unchanged through ASTR 310 and this course.</li><li>Generated by <code>materials/ASTR330/src/generate_astr330_content.py</code>.</li></ul></section>
"""
    return lab_page(6, 'Sirius B and the Chandrasekhar Mass',
                     'Derive the Chandrasekhar mass from first principles and apply it, together with a cooling-age estimate, to the real white dwarf Sirius B.', sections)


# ===========================================================================
# LAB 07: Capstone -- PSR J0348+0432 and core collapse
# ===========================================================================
def make_lab_07() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This capstone lab applies this course's full compact-object toolkit (the Chandrasekhar mass, Lecture 12; the core-collapse energy budget, Lecture 13) to PSR J0348+0432, a real pulsar-white-dwarf binary whose relativistic orbital parameters and component masses were live-verified this session via a direct web fetch (see <code>../reference-log.md</code>).</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Neutron star mass</td><td>{PSR_J0348['neutron_star_mass_msun']:.2f} &plusmn; {PSR_J0348['neutron_star_mass_err']:.2f} M&#8857;</td></tr>
<tr><td>Neutron star radius</td><td>{PSR_J0348['neutron_star_radius_km']:.0f} km</td></tr>
<tr><td>White dwarf companion mass</td><td>{PSR_J0348['wd_mass_msun']:.3f} M&#8857;</td></tr>
<tr><td>Orbital period</td><td>{PSR_J0348['orbital_period_days']:.9f} days</td></tr>
<tr><td>Orbital semimajor axis</td><td>{PSR_J0348['semimajor_km']:.0f} km</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute the neutron star's mass and the white dwarf companion's mass each as a fraction (percent) of the Chandrasekhar mass derived in Lab 06, and classify each object accordingly.</li>
<li>Compute the neutron star's mean density from its measured mass and radius, and express it as a fraction of standard nuclear saturation density ({NUCLEAR_SATURATION_DENSITY_KGM3:.1e} kg/m&sup3;).</li>
<li>Using the generalized Kepler's third law (ASTR 310, Lecture 08), P&sup2; = 4&pi;&sup2;a&sup3;/[G(m1+m2)], verify that the system's measured orbital period and semimajor axis are consistent with the sum of the neutron star and white dwarf masses given in the data table (convert all units to SI first).</li>
<li>Using the core-collapse binding-energy estimate &Delta;E &asymp; (3/5)GM&sup2;(1/R_remnant &minus; 1/R_core) for a {SN_CORE_MASS_MSUN:.1f} M&#8857; core collapsing from a {SN_PROGENITOR_CORE_RADIUS_M/1000:.0f} km progenitor radius to the neutron star's measured radius, compute the total energy released, and state what percentage of that energy is carried away by channels other than visible kinetic energy and light (using the standard published {SN_OBSERVED_KINETIC_PLUS_LIGHT_J:.0e} J visible-energy value).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Write a short (150-250 word) synthesis connecting this lab's four results: why the neutron star's mass and density together confirm it cannot be a white dwarf, why the companion's mass confirms it can be one, and why the energy budget in step 4 shows the visible supernova was only a small fraction of the total event.</p></section>
<section><h2>Deliverables</h2><ul><li>Both Chandrasekhar-mass-fraction classifications with supporting arithmetic.</li><li>The neutron-star density and nuclear-density-fraction calculation.</li><li>The Kepler's-third-law consistency check with full unit conversions.</li><li>The binding-energy budget calculation and percentage breakdown.</li><li>The written synthesis paragraph.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct Chandrasekhar-mass-fraction arithmetic and classification for both objects.</li><li>Correct density and nuclear-density-fraction arithmetic.</li><li>Correct Kepler's-third-law unit conversions and consistency check.</li><li>Correct binding-energy arithmetic and an honestly characterized (not understated) neutrino-energy-fraction percentage.</li><li>Synthesis paragraph correctly integrates all four results rather than restating them separately.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 22.3-22.5.</li><li>PSR J0348+0432 masses, radius, and orbital parameters: live-verified this session via a direct web fetch of Wikipedia's "PSR J0348+0432" article, citing Antoniadis et al. (2013), <em>Science</em> 340, 1233232; see <code>materials/ASTR330/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR330/src/generate_astr330_content.py</code>.</li></ul></section>
"""
    return lab_page(7, 'Capstone: PSR J0348+0432 and the Physics of Core Collapse',
                     'Apply the Chandrasekhar mass, Kepler\u2019s third law, and the core-collapse energy budget to a real, precisely measured neutron star and its white dwarf companion.', sections)


LAB_BUILDERS = [make_lab_01, make_lab_02, make_lab_03, make_lab_04, make_lab_05, make_lab_06, make_lab_07]


def write_labs():
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    for i, builder in enumerate(LAB_BUILDERS, start=1):
        (LAB_DIR / f'lab-{i:02d}.html').write_text(builder(), encoding='utf-8')


# ===========================================================================
# PROBLEM SETS
# ===========================================================================

def build_ps01():
    title = 'Equation of State and Opacity for Alpha Centauri B'
    reading = f'{OPENSTAX}, Chapter 16.1-16.2.'
    r_m = ALPHA_CEN_B['radius_rsun'] * R_SUN_M
    m_kg = ALPHA_CEN_B['mass_msun'] * M_SUN_KG
    p_c = hydrostatic_central_pressure_pa(m_kg, r_m)
    p1 = problem(1, 'Central pressure',
                 f"<p>Using P_c &asymp; (3/8&pi;)GM&sup2;/R&#8308;, compute Alpha Centauri B's estimated central pressure (M = {ALPHA_CEN_B['mass_msun']:.4f} M&#8857;, R = {ALPHA_CEN_B['radius_rsun']:.3f} R&#8857;), showing all unit conversions.</p>")
    p2 = problem(2, 'Comparison to the Sun',
                 f"<p>Compare your Problem 1 answer to the Sun's estimated central pressure ({SUN_CENTRAL_PRESSURE_EST:.3e} Pa, Lab 01), and explain, using the P_c &prop; M&sup2;/R&#8308; scaling, why Alpha Centauri B's smaller mass and radius than the Sun's produce the sign and rough size of the difference you find.</p>")
    p3 = problem(3, 'Electron-scattering opacity',
                 "<p>Compute the electron-scattering opacity &kappa;_es = &sigma;_T(1+X)/(2m_p) for a hydrogen mass fraction X = 0.70, and state why this value does not depend on which star it is being applied to.</p>")
    p4 = problem(4, 'Radiation-to-gas pressure ratio, order of magnitude',
                 f"<p>Alpha Centauri B's core temperature is expected to be somewhat lower than the Sun's (a cooler, lower-mass K1V star). Without computing an exact value, explain qualitatively, using the P_rad &prop; T&#8308;/&rho; versus P_gas &prop; T/&rho; scaling from Lecture 02, whether you expect Alpha Centauri B's radiation-to-gas pressure ratio to be larger or smaller than the Sun's.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    kappa_es = electron_scattering_opacity_m2_per_kg(0.70)
    sol1 = solution(1, 'Central pressure', f"<p>M = {m_kg:.4e} kg, R = {r_m:.4e} m. P_c = (3/8&pi;)GM&sup2;/R&#8308; = {p_c:.3e} Pa.</p>", [('Correct unit conversions', 8), ('Correct final pressure', 7)])
    sol2 = solution(2, 'Comparison to the Sun', f"<p>Alpha Centauri B's estimated central pressure ({p_c:.3e} Pa) is {p_c/SUN_CENTRAL_PRESSURE_EST:.3f} times the Sun's ({SUN_CENTRAL_PRESSURE_EST:.3e} Pa) -- lower, consistent with both its smaller mass (reducing M&sup2; in the numerator) and smaller radius (reducing R&#8308; in the denominator, which would raise P_c) combining so that the mass effect dominates for these specific values.</p>", [('Correct computed ratio', 8), ('Correct qualitative M vs. R\u2074 scaling argument', 7)])
    sol3 = solution(3, 'Electron-scattering opacity', f"<p>&kappa;_es = &sigma;_T(1+X)/(2m_p) = {kappa_es:.4f} m&sup2;/kg. This value depends only on composition (X) and fundamental constants, not on any star-specific density or temperature, so it is identical for every fully ionized star of the same hydrogen mass fraction.</p>", [('Correct arithmetic', 8), ('Correct composition-only dependence explanation', 7)])
    sol4 = solution(4, 'Radiation-to-gas pressure ratio', "<p>Because P_rad/P_gas &prop; T&sup3;/&rho; and Alpha Centauri B has a lower core temperature than the Sun (and a comparable or somewhat higher core density, given its smaller radius at similar mass), the ratio is expected to be smaller than the Sun's already-negligible value -- radiation pressure is even less important in Alpha Centauri B's core than in the Sun's.</p>", [('Correct qualitative direction (smaller ratio)', 12), ('Correct use of the T\u00b3/\u03c1 scaling to justify the direction', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 correct unit conversions and central-pressure arithmetic.',
        'Problem 2: 15 points \u2014 correct computed ratio and correct M vs. R\u2074 scaling reasoning.',
        'Problem 3: 15 points \u2014 correct opacity arithmetic and composition-only dependence explanation.',
        'Problem 4: 20 points \u2014 correct qualitative direction using the T\u00b3/\u03c1 scaling, not a guess.',
    ]
    common_errors = [
        'Forgetting to convert R\u2609 and M\u2609 to SI units before applying the fourth-power-sensitive pressure formula.',
        'Treating electron-scattering opacity as if it depended on the star\u2019s temperature or density.',
        'Guessing the direction in Problem 4 without citing the T\u00b3/\u03c1 scaling explicitly.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps02():
    title = 'Radiative Gradient and the Schwarzschild Criterion for Sirius A\u2019s Envelope'
    reading = f'{OPENSTAX}, Chapter 16.2.'
    t_test = 3.0e6
    p_test = 1.0e12
    m_enc = 0.95 * SIRIUS_A['mass_msun'] * M_SUN_KG
    nabla = radiative_gradient_dimensionless(SIRIUS_A['lum_lsun'] * L_SUN_W, m_enc, p_test, t_test, KAPPA_ES_SUN)
    p1 = problem(1, 'Radiative gradient for a Sirius A envelope point',
                 f"<p>Using &nabla;_rad = 3&kappa;LP/(16&pi;acGMT&#8308;) with Sirius A's measured luminosity (L = {SIRIUS_A['lum_lsun']:.1f} L&#8857;), electron-scattering opacity (Lecture 02/PS 01), an illustrative enclosed mass of 0.95 &times; Sirius A's mass, and illustrative envelope conditions T = 3.0 &times; 10&#8310; K, P = 1.0 &times; 10&#185;&sup2; Pa, compute &nabla;_rad, showing every substituted value.</p>", points=20)
    p2 = problem(2, 'Schwarzschild classification',
                 "<p>Compare your Problem 1 result to the ideal monatomic-gas adiabatic gradient &nabla;_ad = 2/5, and classify this envelope point as radiatively stable or convectively unstable.</p>")
    p3 = problem(3, 'Comparison to the Sun',
                 f"<p>The Sun's deep-envelope sample point (Lab 02) gave &nabla;_rad = {SUN_RADIATIVE_GRADIENT:.4f}. Given that Sirius A is about {SIRIUS_A['lum_lsun']/1.0:.0f} times more luminous than the Sun, explain qualitatively why a much larger &nabla;_rad for the (much more luminous) Sirius A envelope point is or is not expected, using the direct proportionality &nabla;_rad &prop; L.</p>")
    p4 = problem(4, 'Physical interpretation',
                 "<p>Real stellar models of A-type stars like Sirius A find they have radiative envelopes and convective cores (the opposite arrangement from the Sun). Explain in one paragraph how this problem set's illustrative envelope-point classification (Problem 2) is consistent, or not, with that real structural difference, and identify what additional information (not computed in this problem set) would be needed to properly classify Sirius A's core.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Radiative gradient', f"<p>&nabla;_rad = 3&kappa;LP/(16&pi;acGMT&#8308;) = {nabla:.4e}, using &kappa; = {KAPPA_ES_SUN:.4f} m&sup2;/kg, L = {SIRIUS_A['lum_lsun']*L_SUN_W:.3e} W, P = 1.0 &times; 10&#185;&sup2; Pa, M = {m_enc:.3e} kg, T = 3.0 &times; 10&#8310; K.</p>", [('Correct substitution and unit handling', 12), ('Correct final value', 8)])
    sol2 = solution(2, 'Schwarzschild classification', f"<p>&nabla;_rad ({nabla:.4e}) is far greater than &nabla;_ad (0.4), so this illustrative envelope point is convectively unstable in this model.</p>", [('Correct comparison and classification', 8), ('Correct numeric justification', 7)])
    sol3 = solution(3, 'Comparison to the Sun', f"<p>Since &nabla;_rad &prop; L directly, and Sirius A is about {SIRIUS_A['lum_lsun']:.0f} times more luminous than the Sun, a proportionally larger &nabla;_rad is expected for otherwise similar opacity, pressure, mass, and temperature conditions -- consistent with the much larger value found in Problem 1 relative to the Sun's {SUN_RADIATIVE_GRADIENT:.4f}.</p>", [('Correct use of the direct L proportionality', 8), ('Correct qualitative comparison', 7)])
    sol4 = solution(4, 'Physical interpretation', "<p>This problem set's single illustrative envelope point, using electron-scattering opacity only, finds convective instability there, which is not the same as real A-type stars' radiative envelopes; real A-type stellar envelopes have lower opacity and different pressure/temperature structure than this simplified illustrative point assumes. Correctly classifying Sirius A's actual envelope and core would require a full, depth-resolved stellar model with a realistic opacity table, not a single schematic sample point.</p>", [('Correct acknowledgment that the illustrative point does not match the real structure', 12), ('Correct identification of a full depth-resolved model as the missing ingredient', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 20 points \u2014 correct substitution and arithmetic in the radiative-gradient formula.',
        'Problem 2: 15 points \u2014 correct comparison and Schwarzschild classification.',
        'Problem 3: 15 points \u2014 correct use of the direct L proportionality.',
        'Problem 4: 20 points \u2014 correct, intellectually honest reconciliation with the real A-type-star structure, not an overclaimed match.',
    ]
    common_errors = [
        'Forgetting the fourth-power temperature dependence in the denominator of the radiative-gradient formula.',
        'Claiming the illustrative single-point classification proves Sirius A\u2019s full envelope structure, rather than acknowledging its limitations.',
        'Confusing convective envelopes (Sun-like) with convective cores (Sirius-A-like) when discussing real stellar structure.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps03():
    title = 'The pp-Chain/CNO Crossover Temperature for Alpha Centauri A'
    reading = f'{OPENSTAX}, Chapter 16.3.'
    t_core_a = SUN_CORE_TEMP_PUBLISHED * (ALPHA_CEN_A['mass_msun'] / 1.0) ** 0.7
    t6_a = t_core_a / 1.0e6
    eps_pp_a = epsilon_pp_relative(t6_a)
    eps_cno_a = epsilon_cno_relative(t6_a)
    gamow_a = gamow_peak_energy_kev(1, 1, 0.5, t_core_a)
    p1 = problem(1, 'Schematic core temperature',
                 f"<p>Using the schematic mass-scaling relation T_core &asymp; T_core,&#8857;(M/M&#8857;)^0.7 (Lecture 06), estimate Alpha Centauri A's core temperature (M = {ALPHA_CEN_A['mass_msun']:.4f} M&#8857;), and express your answer as T6.</p>", points=20)
    p2 = problem(2, 'Gamow peak energy',
                 "<p>Using your Problem 1 core temperature, compute the proton-proton Gamow peak energy (Z1=Z2=1, &mu;=0.5 amu), and compare it to the Sun's own pp Gamow peak energy from Lecture 05/Lab 03.</p>")
    p3 = problem(3, 'pp/CNO classification',
                 f"<p>Using the crossover temperature T6 &asymp; {PP_CNO_CROSSOVER_T6:.1f} derived in Lecture 06/Lab 03, classify Alpha Centauri A as pp-dominated or CNO-dominated, and explain whether this is consistent with its near-solar mass and G2V spectral type.</p>")
    p4 = problem(4, 'Comparative reasoning',
                 f"<p>Sirius A (T6 &asymp; {T6_SIRIUS_A_CORE:.1f}, Lecture 06) is CNO-dominated while Alpha Centauri A (your Problem 1 answer) is not. Using the two stars' mass ratio ({SIRIUS_A['mass_msun']/ALPHA_CEN_A['mass_msun']:.2f}), explain quantitatively why such a modest mass difference produces such a sharp qualitative difference in dominant burning mechanism.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Schematic core temperature', f"<p>T_core = {SUN_CORE_TEMP_PUBLISHED:.3e} &times; ({ALPHA_CEN_A['mass_msun']:.4f})^0.7 = {t_core_a:.3e} K = T6 {t6_a:.2f}.</p>", [('Correct exponent application', 10), ('Correct T6 conversion', 10)])
    sol2 = solution(2, 'Gamow peak energy', f"<p>E0 = 1.22(1&middot;1&middot;0.5&middot;{t6_a:.2f}&sup2;)^(1/3) = {gamow_a:.2f} keV, essentially the same order of magnitude as the Sun's own value ({GAMOW_E0_PP_SUN_KEV:.2f} keV), since Alpha Centauri A's core temperature is close to the Sun's.</p>", [('Correct Gamow-peak arithmetic', 8), ('Correct comparison to the Sun', 7)])
    sol3 = solution(3, 'pp/CNO classification', f"<p>Alpha Centauri A's T6 ({t6_a:.2f}) is well below the {PP_CNO_CROSSOVER_T6:.1f} crossover, so it is pp-dominated, consistent with its near-solar mass and G2V spectral type (very similar to the Sun's own pp-dominated core).</p>", [('Correct classification', 8), ('Correct connection to mass/spectral type', 7)])
    sol4 = solution(4, 'Comparative reasoning', f"<p>Because &epsilon;_CNO &prop; T6&sup2;&#8304;, an extremely steep power law, even the modest {SIRIUS_A['mass_msun']/ALPHA_CEN_A['mass_msun']:.2f}&times; mass ratio (via the T &prop; M^0.7 scaling) produces a large relative change in core temperature ratio ({(SIRIUS_A['mass_msun']/ALPHA_CEN_A['mass_msun'])**0.7:.2f}), and raising that ratio to the 20th power amplifies it enormously -- explaining why such a modest mass difference flips the dominant mechanism entirely.</p>", [('Correct quantitative use of the T6\u00b2\u2070 sensitivity', 12), ('Correct connection to the modest mass/temperature ratio', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 20 points \u2014 correct exponent application and T6 conversion.',
        'Problem 2: 15 points \u2014 correct Gamow-peak arithmetic and comparison.',
        'Problem 3: 15 points \u2014 correct classification with supporting reasoning.',
        'Problem 4: 20 points \u2014 correct quantitative use of the T6\u00b2\u2070 sensitivity, not just a qualitative statement.',
    ]
    common_errors = [
        'Forgetting to raise the temperature ratio to the 0.7 power (schematic mass-scaling relation) before comparing stars.',
        'Treating the crossover temperature as an exact reaction-network result rather than a schematic power-law approximation.',
        'Giving only a qualitative answer to Problem 4 without the required T6\u00b2\u2070 quantitative reasoning.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps04():
    title = 'Extrapolating the Mass-Luminosity-Lifetime Scaling to a Hypothetical Massive Star'
    reading = f'{OPENSTAX}, Chapter 19.3.'
    m_hyp = 10.0
    l_hyp = mass_luminosity_lsun(m_hyp)
    t_hyp = ms_lifetime_gyr(m_hyp, l_hyp)
    p1 = problem(1, 'Extrapolated luminosity',
                 f"<p>Using L &asymp; M^3.5, predict the luminosity of a hypothetical {m_hyp:.0f} M&#8857; main-sequence star (an extrapolation exercise, not a specific measured real star).</p>", points=20)
    p2 = problem(2, 'Extrapolated lifetime',
                 f"<p>Using t_MS = 10 Gyr &times; M/L, compute this hypothetical star's main-sequence lifetime from your Problem 1 luminosity, and express the result in millions of years (Myr).</p>")
    p3 = problem(3, 'Comparison to Sirius A',
                 f"<p>Compare your Problem 2 lifetime to Sirius A's computed lifetime ({SIRIUS_A_MS_LIFETIME_GYR:.3f} Gyr, Lab 04), and explain, using the M^-2.5 scaling, why a star only about {m_hyp/SIRIUS_A['mass_msun']:.1f} times more massive than Sirius A has a dramatically shorter lifetime.</p>")
    p4 = problem(4, 'Limits of the extrapolation',
                 "<p>The n=3.5 mass-luminosity exponent is only an approximation, and it is known to be less accurate at high stellar masses (where radiation pressure becomes important, per Lecture 02/PS 01). Explain in one paragraph why this problem set's answer should be treated as an order-of-magnitude estimate rather than a precise prediction, and identify one specific physical effect (from this course) that would need to be included in a more accurate treatment.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Extrapolated luminosity', f"<p>L = {m_hyp:.0f}^3.5 = {l_hyp:.0f} L&#8857;.</p>", [('Correct exponent application', 12), ('Correct final value', 8)])
    sol2 = solution(2, 'Extrapolated lifetime', f"<p>t_MS = 10 Gyr &times; {m_hyp:.0f}/{l_hyp:.0f} = {t_hyp:.4f} Gyr = {t_hyp*1000:.1f} Myr.</p>", [('Correct lifetime arithmetic', 8), ('Correct Gyr-to-Myr conversion', 7)])
    sol3 = solution(3, 'Comparison to Sirius A', f"<p>The {m_hyp:.0f} M&#8857; star's lifetime ({t_hyp*1000:.1f} Myr) is much shorter than Sirius A's ({SIRIUS_A_MS_LIFETIME_GYR*1000:.1f} Myr), consistent with t_MS &prop; M^-2.5: a {m_hyp/SIRIUS_A['mass_msun']:.2f}&times; mass increase produces a ({m_hyp/SIRIUS_A['mass_msun']:.2f})^-2.5 = {(m_hyp/SIRIUS_A['mass_msun'])**-2.5:.3f}&times; lifetime factor, a substantial reduction from a comparatively modest mass increase.</p>", [('Correct quantitative M^-2.5 scaling calculation', 8), ('Correct comparison to Sirius A', 7)])
    sol4 = solution(4, 'Limits of the extrapolation', "<p>The n=3.5 exponent is calibrated primarily from stars near solar mass; at 10 M\u2609, radiation pressure (Lecture 02) becomes progressively more important relative to gas pressure, which changes the star's effective equation of state and hence the true mass-luminosity exponent, so this problem set's answer should be treated as order-of-magnitude only, not a precision prediction.</p>", [('Correct acknowledgment of order-of-magnitude-only validity', 12), ('Correct identification of radiation pressure as the missing physics', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 20 points \u2014 correct exponent arithmetic.',
        'Problem 2: 15 points \u2014 correct lifetime arithmetic and unit conversion.',
        'Problem 3: 15 points \u2014 correct quantitative M^-2.5 scaling calculation, not just a qualitative statement.',
        'Problem 4: 20 points \u2014 correct, intellectually honest limitation discussion identifying radiation pressure specifically.',
    ]
    common_errors = [
        'Reporting the extrapolated numbers as if they were a specific real star\u2019s measured properties rather than a hypothetical extrapolation.',
        'Forgetting to convert Gyr to Myr in Problem 2.',
        'Giving a generic "the model is approximate" answer to Problem 4 without identifying radiation pressure specifically.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps05():
    title = 'Hyades Cluster Structure and Dynamical Timescales'
    reading = f'{OPENSTAX}, Chapter 21.1.'
    core_vol_pc3 = (4.0 / 3.0) * math.pi * HYADES['core_radius_pc'] ** 3
    half_mass_vol_pc3 = (4.0 / 3.0) * math.pi * HYADES['half_mass_radius_pc'] ** 3
    density_half_mass = (HYADES['total_mass_msun'] / 2.0) / half_mass_vol_pc3
    p1 = problem(1, 'Core density',
                 f"<p>Using the Hyades' core radius ({HYADES['core_radius_pc']:.1f} pc) and assuming, as an order-of-magnitude estimate, that about half the cluster's total mass ({HYADES['total_mass_msun']:.0f} M&#8857;) lies within the core, compute the core's mean mass density in M&#8857;/pc&sup3;.</p>", points=20)
    p2 = problem(2, 'Half-mass density',
                 f"<p>Using the half-mass radius ({HYADES['half_mass_radius_pc']:.1f} pc), by definition enclosing exactly half the cluster's total mass, compute the mean density within the half-mass radius in M&#8857;/pc&sup3;, and compare it to your Problem 1 core-density estimate.</p>")
    p3 = problem(3, 'Metallicity comparison',
                 f"<p>The Hyades cluster's overall metallicity is measured at +0.14 dex (live-verified this session), meaning its stars are more metal-rich than the Sun (metallicity 0 dex by definition). Using the fact that higher metallicity increases opacity (Lecture 02), explain qualitatively whether you would expect Hyades stars of a given mass to have systematically longer or shorter main-sequence lifetimes than otherwise-identical solar-metallicity stars.</p>")
    p4 = problem(4, 'Turnoff-age discrepancy, revisited',
                 f"<p>Lab 05 found the fixed n=3.5 mass-luminosity-lifetime scaling overestimates the Hyades' true age by a factor of about {HYADES_AGE_DISCREPANCY_FACTOR:.1f}. Using your Problem 3 answer, state whether the Hyades' above-solar metallicity would be expected to make this specific discrepancy larger or smaller, or whether it is unrelated to the discrepancy's likely cause (the fixed mass-luminosity exponent, per Lecture 07/09).</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Core density', f"<p>Core volume = (4/3)&pi;(2.7 pc)&sup3; = {core_vol_pc3:.1f} pc&sup3;. Assuming half the total mass ({HYADES['total_mass_msun']/2.0:.0f} M&#8857;) lies within it, density &asymp; {(HYADES['total_mass_msun']/2.0)/core_vol_pc3:.2f} M&#8857;/pc&sup3;.</p>", [('Correct volume arithmetic', 10), ('Correct density arithmetic', 10)])
    sol2 = solution(2, 'Half-mass density', f"<p>Half-mass volume = (4/3)&pi;(5.7 pc)&sup3; = {half_mass_vol_pc3:.1f} pc&sup3;; density = {HYADES['total_mass_msun']/2.0:.0f} M&#8857; / {half_mass_vol_pc3:.1f} pc&sup3; = {density_half_mass:.3f} M&#8857;/pc&sup3;, substantially lower than the core density, confirming the Hyades is centrally concentrated.</p>", [('Correct volume and density arithmetic', 8), ('Correct core-vs-half-mass density comparison', 7)])
    sol3 = solution(3, 'Metallicity comparison', "<p>Higher metallicity raises opacity (more bound-free/free-free absorbers), which raises the radiative temperature gradient (Lecture 03) needed to carry a given luminosity; for a fixed mass, this generally corresponds to a somewhat lower luminosity and hence a somewhat longer main-sequence lifetime than an otherwise identical solar-metallicity star.</p>", [('Correct opacity-metallicity connection', 8), ('Correct qualitative lifetime-direction conclusion', 7)])
    sol4 = solution(4, 'Turnoff-age discrepancy, revisited', "<p>The Lab 05 discrepancy is attributed to the fixed n=3.5 mass-luminosity exponent being an approximation, not to metallicity; while the Hyades' above-solar metallicity would be expected to modestly lengthen main-sequence lifetimes (Problem 3), this is a separate, second-order effect from the primary cause of the factor-of-two discrepancy, which is the exponent's inaccuracy at the Hyades' specific turnoff mass, not the cluster's metallicity.</p>", [('Correct identification that metallicity is a secondary, not primary, effect', 12), ('Correct connection back to the fixed-exponent explanation from Lecture 07/09', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 20 points \u2014 correct volume and density arithmetic.',
        'Problem 2: 15 points \u2014 correct half-mass density arithmetic and comparison.',
        'Problem 3: 15 points \u2014 correct opacity-metallicity-lifetime reasoning chain.',
        'Problem 4: 20 points \u2014 correct identification of the primary versus secondary cause of the age discrepancy.',
    ]
    common_errors = [
        'Forgetting the 4/3\u03c0r\u00b3 volume formula or mis-cubing the radius.',
        'Reversing the direction of the metallicity-opacity-lifetime relationship in Problem 3.',
        'Conflating the metallicity effect (Problem 3, secondary) with the fixed-exponent effect (Problem 4, primary cause) as if they were the same explanation.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps06():
    title = 'The Chandrasekhar Mass for a Helium-Core White Dwarf'
    reading = f'{OPENSTAX}, Chapter 22.1-22.2.'
    mue_he = 2.0  # helium is also 2 nucleons per electron, essentially identical to carbon-oxygen
    m_ch_he_kg = chandrasekhar_mass_kg(mue_he)
    m_ch_he_msun = m_ch_he_kg / M_SUN_KG
    mue_hyp = 2.2  # hypothetical higher mu_e for illustration
    m_ch_hyp_kg = chandrasekhar_mass_kg(mue_hyp)
    m_ch_hyp_msun = m_ch_hyp_kg / M_SUN_KG
    p1 = problem(1, 'Helium-core Chandrasekhar mass',
                 f"<p>Compute the Chandrasekhar mass for a pure-helium-core white dwarf (&mu;_e = {mue_he:.1f}, essentially identical to the carbon-oxygen case since helium-4 also has two nucleons per electron), and compare it to the carbon-oxygen value ({CHANDRASEKHAR_MASS_MUE2_MSUN:.4f} M&#8857;, Lab 06).</p>", points=20)
    p2 = problem(2, 'Hypothetical higher mu_e',
                 f"<p>Compute the Chandrasekhar mass for a hypothetical composition with &mu;_e = {mue_hyp:.1f} (somewhat more neutron-rich than carbon-oxygen), and state whether it is larger or smaller than the carbon-oxygen value, consistent with the M_Ch &prop; &mu;_e&#8315;&sup2; scaling.</p>")
    p3 = problem(3, 'Sirius B, revisited',
                 f"<p>Using your Problem 1 helium-core Chandrasekhar mass, recompute Sirius B's mass ({SIRIUS_B['mass_msun']:.3f} M&#8857;) as a percentage of this (slightly different) limit, and compare to the {SIRIUS_B_TO_CHANDRA_FRACTION*100:.1f}% found in Lab 06 using the carbon-oxygen value.</p>")
    p4 = problem(4, 'PSR J0348+0432\u2019s white dwarf companion',
                 f"<p>PSR J0348+0432's white dwarf companion has a measured mass of {PSR_J0348['wd_mass_msun']:.3f} M&#8857; (live-verified this session). Compute this mass as a percentage of the carbon-oxygen Chandrasekhar mass, and state whether this is consistent with its continued existence as a stable white dwarf.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Helium-core Chandrasekhar mass', f"<p>M_Ch(&mu;_e={mue_he:.1f}) = {m_ch_he_msun:.4f} M&#8857;, identical to the carbon-oxygen value ({CHANDRASEKHAR_MASS_MUE2_MSUN:.4f} M&#8857;) because both compositions have exactly two nucleons per electron.</p>", [('Correct arithmetic', 12), ('Correct identification of the identical mu_e values', 8)])
    sol2 = solution(2, 'Hypothetical higher mu_e', f"<p>M_Ch(&mu;_e={mue_hyp:.1f}) = {m_ch_hyp_msun:.4f} M&#8857;, smaller than the carbon-oxygen value ({CHANDRASEKHAR_MASS_MUE2_MSUN:.4f} M&#8857;), consistent with M_Ch &prop; &mu;_e&#8315;&sup2;: a larger &mu;_e produces a smaller limiting mass.</p>", [('Correct arithmetic', 8), ('Correct direction consistent with the mu_e^-2 scaling', 7)])
    sol3 = solution(3, 'Sirius B, revisited', f"<p>{SIRIUS_B['mass_msun']:.3f}/{m_ch_he_msun:.4f} = {SIRIUS_B['mass_msun']/m_ch_he_msun*100:.1f}%, identical (to the precision shown) to the {SIRIUS_B_TO_CHANDRA_FRACTION*100:.1f}% found in Lab 06, since the helium-core and carbon-oxygen Chandrasekhar masses are the same for this &mu;_e.</p>", [('Correct percentage arithmetic', 8), ('Correct recognition that the two results are identical', 7)])
    sol4 = solution(4, 'PSR J0348+0432\u2019s white dwarf companion', f"<p>{PSR_J0348['wd_mass_msun']:.3f}/{CHANDRASEKHAR_MASS_MUE2_MSUN:.4f} = {PSR_WD_TO_CHANDRA_FRACTION*100:.1f}%, comfortably below the Chandrasekhar mass, consistent with its continued existence as a stable white dwarf.</p>", [('Correct percentage arithmetic', 12), ('Correct stability conclusion', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 20 points \u2014 correct arithmetic and identification that helium and carbon-oxygen give identical mu_e.',
        'Problem 2: 15 points \u2014 correct arithmetic and correct mu_e^-2 scaling direction.',
        'Problem 3: 15 points \u2014 correct percentage arithmetic and recognition of the identical result.',
        'Problem 4: 20 points \u2014 correct percentage arithmetic and stability conclusion.',
    ]
    common_errors = [
        'Assuming helium-core and carbon-oxygen white dwarfs must have different Chandrasekhar masses without checking their mu_e values are actually the same.',
        'Getting the direction of the mu_e^-2 scaling backwards in Problem 2.',
        'Forgetting to use the correct (carbon-oxygen) Chandrasekhar mass for Problem 4, mixing it up with Problem 1\u2019s helium value.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps07():
    title = 'Capstone Synthesis: Verifying PSR J0348+0432\u2019s Total Mass from Its Orbit'
    reading = f'{OPENSTAX}, Chapter 3.1-3.3 and Chapter 22.3-22.5.'
    p_s = PSR_J0348['orbital_period_days'] * 86400.0
    a_m = PSR_J0348['semimajor_km'] * KM
    total_mass_kepler_kg = 4 * math.pi ** 2 * a_m ** 3 / (G_NEWTON * p_s ** 2)
    total_mass_kepler_msun = total_mass_kepler_kg / M_SUN_KG
    total_mass_measured_msun = PSR_J0348['neutron_star_mass_msun'] + PSR_J0348['wd_mass_msun']
    p1 = problem(1, 'Unit conversion',
                 f"<p>Convert PSR J0348+0432's orbital period ({PSR_J0348['orbital_period_days']:.9f} days) and semimajor axis ({PSR_J0348['semimajor_km']:.0f} km) to SI units (seconds and meters).</p>")
    p2 = problem(2, 'Total mass from Kepler\u2019s third law',
                 "<p>Using P&sup2; = 4&pi;&sup2;a&sup3;/[G(m1+m2)] (the generalized two-body Kepler's third law, ASTR 310 Lecture 08), solve for the total system mass in solar masses.</p>", points=20)
    p3 = problem(3, 'Cross-check against the measured masses',
                 f"<p>The independently measured neutron star and white dwarf masses (Lecture 12/Lab 07) sum to {total_mass_measured_msun:.3f} M&#8857;. Compute the percent agreement between your Problem 2 answer and this independently measured sum.</p>")
    p4 = problem(4, 'Synthesis',
                 "<p>Write a short (150-200 word) paragraph explaining why this problem set's purely orbital (Keplerian) total-mass determination, agreeing with the independently measured individual masses (obtained via an entirely different method: pulsar timing plus white-dwarf spectroscopy), constitutes strong evidence for both results, in the same spirit as ASTR 310 Lecture 14's Alpha Centauri AB radiative/dynamical cross-check.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Unit conversion', f"<p>P = {PSR_J0348['orbital_period_days']:.9f} days &times; 86400 s/day = {p_s:.6e} s. a = {PSR_J0348['semimajor_km']:.0f} km &times; 1000 m/km = {a_m:.6e} m.</p>", [('Correct period conversion', 8), ('Correct semimajor-axis conversion', 7)])
    sol2 = solution(2, 'Total mass from Kepler\u2019s third law', f"<p>(m1+m2) = 4&pi;&sup2;a&sup3;/(GP&sup2;) = {total_mass_kepler_msun:.4f} M&#8857;.</p>", [('Correct formula rearrangement', 8), ('Correct arithmetic and final mass', 12)])
    sol3 = solution(3, 'Cross-check', f"<p>Percent agreement = |{total_mass_kepler_msun:.3f} &minus; {total_mass_measured_msun:.3f}| / {total_mass_measured_msun:.3f} &times; 100% = {abs(total_mass_kepler_msun-total_mass_measured_msun)/total_mass_measured_msun*100:.2f}%.</p>", [('Correct percent-agreement arithmetic', 8), ('Correct comparison value used', 7)])
    sol4 = solution(4, 'Synthesis', "<p>A strong answer notes that the orbital (Keplerian) total-mass determination depends only on the measured period and semimajor axis and Newtonian/relativistic gravity, while the individually measured neutron-star and white-dwarf masses depend on entirely different physics (pulsar timing, Shapiro delay, and white-dwarf spectroscopy); their close agreement is therefore not a coincidence but strong, largely independent confirmation of both methods, exactly analogous to ASTR 310 Lecture 14's radiative-versus-dynamical cross-check for Alpha Centauri AB.</p>", [('Correct identification of the two independent methods', 10), ('Correct analogy to the ASTR 310 precedent', 10)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 correct unit conversions.',
        'Problem 2: 20 points \u2014 correct Kepler\u2019s-third-law rearrangement and arithmetic.',
        'Problem 3: 15 points \u2014 correct percent-agreement arithmetic.',
        'Problem 4: 20 points \u2014 correct identification of independence and correct analogy to the ASTR 310 precedent, not a generic restatement.',
    ]
    common_errors = [
        'Forgetting to convert days to seconds or km to meters before applying Kepler\u2019s third law.',
        'Using the Sun-planet form of Kepler\u2019s third law (assuming one mass dominates) instead of the full two-body form.',
        'Writing a generic "agreement is good" synthesis in Problem 4 without explaining why the two methods are physically independent.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


PSET_BUILDERS = [build_ps01, build_ps02, build_ps03, build_ps04, build_ps05, build_ps06, build_ps07]


def write_psets():
    PSET_DIR.mkdir(parents=True, exist_ok=True)
    for i, builder in enumerate(PSET_BUILDERS, start=1):
        title, reading, problems_html, solutions_html, criteria, common_errors = builder()
        (PSET_DIR / f'problem-set-{i:02d}.html').write_text(pset_page(i, title, reading, problems_html, reading), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-solutions.html').write_text(solutions_page(i, title, solutions_html), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-assessment.md').write_text(assessment_md(i, title, criteria, common_errors), encoding='utf-8')


if __name__ == '__main__':
    write_labs()
    write_psets()
    print(f'Wrote {len(LAB_BUILDERS)} labs and {len(PSET_BUILDERS)} problem sets (with solutions and assessment instructions).')
