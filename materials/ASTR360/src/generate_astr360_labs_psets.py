"""Lab and problem-set generator for ASTR360.

Depends on the shared constants and page()/CSS helpers in
generate_astr360_content.py so every number here traces back to the same
real ISM datasets (ISM phases, HI sightlines, Cyg OB2-12/HD 200775 dust,
Orion/Taurus molecular clouds, Barnard 68, Orion/Rosette H II regions,
Cas A/Tycho shocks, Crab Nebula) used in the paired lectures. Run with the
project interpreter:
    python materials/ASTR360/src/generate_astr360_content.py
    python materials/ASTR360/src/generate_astr360_labs_psets.py
"""
from __future__ import annotations

import math
from html import escape

from generate_astr360_content import (
    CSS, page, li, DATA_DIR, fmt,
    G_CONST, C_LIGHT, H_PLANCK, K_BOLTZMANN, SIGMA_SB, PC_M, YEAR_S,
    M_SUN, M_H_KG, AMU, MU_MOLECULAR, MU_ATOMIC, MU_IONIZED,
    NU_21CM_HZ, LAMBDA_21CM_M, T_STAR_21CM_K,
    ISM_PHASES, PHASE_PRESSURE_K,
    SIGHTLINE_3C273, SIGHTLINE_CYGX1,
    CNM_TSPIN_K, WNM_TSPIN_K, CNM_FWHM_KMS, WNM_FWHM_KMS, CNM_PEAK_TB_K, WNM_PEAK_TB_K,
    R_V_DIFFUSE, CYGOB2_12, HD200775, AV_CYGOB2_12, AV_HD200775,
    X_CO_CM2_K_KMS, ORION_MOLECULAR_CLOUD, TAURUS_MOLECULAR_CLOUD,
    OMC1_DENSE_CORE, BARNARD68,
    ORION_NEBULA, ALPHA_B_CM3_S, ROSETTE_NEBULA,
    CAS_A, TYCHO_SNR, CR_NORM_FLUX, CR_INDEX_BELOW_KNEE, CR_INDEX_ABOVE_KNEE, CR_KNEE_EV,
    B_ISM_AVERAGE_UG, CRUTCHER_B0_UG, CRUTCHER_N_CRIT_CM3, CRUTCHER_EXPONENT, CRAB_NEBULA,
    hi_column_density_cm2, spin_temperature_population_ratio, brightness_temperature_k,
    extinction_av_mag, cardelli_a_lambda_over_av, h2_mass_from_co_msun, virial_mass_msun,
    sound_speed_m_s, jeans_length_m, jeans_mass_msun, free_fall_time_yr,
    stromgren_radius_pc, recombination_timescale_yr, shock_post_temperature_k,
    shock_compression_ratio, cosmic_ray_flux, synchrotron_critical_frequency_hz,
    crutcher_b_field_ug,
    OMC1_H2_MASS_DIRECT, OMC1_H2_MASS_FROM_CO, OMC1_VIRIAL_MASS, TAURUS_VIRIAL_MASS,
    OMC1_CORE_JEANS_MASS, OMC1_CORE_JEANS_LENGTH_PC, OMC1_CORE_FREEFALL_TIME_YR,
    BARNARD68_JEANS_MASS, BARNARD68_JEANS_LENGTH_PC, BARNARD68_FREEFALL_TIME_YR,
    ORION_STROMGREN_RADIUS_PC, ORION_RECOMBINATION_TIME_YR,
    ROSETTE_STROMGREN_RADIUS_PC, ROSETTE_RECOMBINATION_TIME_YR,
    CASA_POST_SHOCK_T, CASA_POST_SHOCK_KT_KEV, TYCHO_POST_SHOCK_T, TYCHO_POST_SHOCK_KT_KEV,
    SHOCK_COMPRESSION, CR_FLUX_1GEV, CR_FLUX_1TEV, CR_KNEE_GEV,
    CRAB_SYNCHROTRON_GAMMA_OPTICAL, CRAB_NU_C_HZ, MOLECULAR_CLOUD_ZEEMAN_B_UG,
    OPENSTAX_NOTE,
)
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB_DIR = ROOT / 'labs'
PSET_DIR = ROOT / 'problem-sets'

OPENSTAX = OPENSTAX_NOTE


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
    return page(f'ASTR 360 Lab {n:02d}', body)


def pset_page(n: int, title: str, focus: str, problems_html: str, reading: str) -> str:
    body = f"""<header><div><h1>ASTR 360 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header>
<main><section><h2>Problems</h2>{problems_html}</section>
<section><h2>Due and Scope</h2><p>Submit a complete derivation with equations, units, labeled quantities, and a short narrative interpretation for each problem. Show every step; a correct final number without a visible derivation receives partial credit at most, and quoting a lecture number without adapting it to this problem's specific inputs receives no credit for that step.</p></section>
<section><h2>OpenStax Companion Reading</h2><p>{escape(reading)}</p></section>
<section><h2>References and Data Sources</h2><ul><li>Corresponding lecture slides and notes for this unit.</li><li>{OPENSTAX}</li><li>Course datasets under <code>materials/ASTR360/data/</code> where referenced above.</li></ul></section>
</main>"""
    return page(f'ASTR 360 Problem Set {n:02d}', body)


def solutions_page(n: int, title: str, solutions_html: str) -> str:
    body = f"<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header><main><section><h2>Worked Solutions</h2>{solutions_html}</section><section><h2>Grading Notes</h2><p>Award full marks for correct method, units, and a numeric result consistent with the arithmetic shown (allow reasonable rounding). Verify that the student re-derives the number for this problem's specific inputs rather than quoting a lecture example without adaptation. Watch specifically for unit-conversion errors (cm^-3 vs m^-3, pc vs m, K km/s integrals), for comparative-magnitude statements given in the wrong direction, and for level-1/level-2/level-3 data-provenance conflation (e.g., presenting the illustrative synthetic HI spectrum shape as an exact measurement of a specific real sightline) -- these are the most common sources of mistakes in this course.</p></section></main>"
    return page(f'ASTR 360 Problem Set {n:02d} Solutions', body)


def assessment_md(n: int, title: str, criteria: list, common_errors: list) -> str:
    crit = '\n'.join(f'- {c}' for c in criteria)
    err = '\n'.join(f'- {e}' for e in common_errors)
    return f"""# Assessment Instructions: Problem Set {n:02d} \u2014 {title}

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the referenced dataset(s) under `materials/ASTR360/data/`.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking number but no visible derivation steps should not. Because this is a 300-level quantitative interstellar-medium course, full marks require a genuine derivation wherever the problem set asks for one, and a genuinely reasoned (not merely asserted) interpretation wherever the problem asks for scientific judgment (e.g., honestly characterizing an idealized model's disagreement with a real object).

## Problem-Level Criteria
{crit}

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
{err}
"""


# ===========================================================================
# LAB/PSET 01 (Lectures 1-2): ISM phases, pressure balance, thermal equilibrium
# ===========================================================================
def make_lab_01() -> str:
    rows = ''.join(
        f"<tr><td>{escape(name)}</td><td>{d['n_cm3']:.3g}</td><td>{d['T_k']:.3g}</td><td>{PHASE_PRESSURE_K[name]:,.0f}</td><td>{d['filling']:.3f}</td></tr>"
        for name, d in ISM_PHASES.items())
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This is a computational lab (no telescope required) that builds this unit's six-phase pressure-balance table and a schematic thermal-equilibrium (heating=cooling) curve from Lectures 01-02's real, standard published ISM phase parameters (McKee &amp; Ostriker 1977).</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Phase</th><th>n (cm^-3)</th><th>T (K)</th><th>P/k (cm^-3 K)</th><th>Filling factor</th></tr></thead><tbody>{rows}</tbody></table>
<p>All values are standard published McKee &amp; Ostriker (1977)/Draine (2011) canonical ISM phase parameters, level 2 (not independently re-verified this session; see <code>../reference-log.md</code>).</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute P/k=nT for all six phases (reproduce the table above from the raw n, T values) and rank the phases by pressure.</li>
<li>Compute the ratio of the WNM's pressure to the CNM's pressure and state whether the two phases are consistent with approximate pressure equilibrium (define "approximate" quantitatively, e.g., within a factor of 2).</li>
<li>Compute the ratio of the molecular-cloud phase's pressure to the CNM's pressure, and explain physically why this large ratio is not evidence against the pressure-balance framework (Lecture 01's self-gravity point).</li>
<li>Build the schematic thermal-equilibrium curve of Lecture 02 (log P/k vs log T) by combining a CNM-like linear branch (cooling &prop; T) and a WNM-like branch (cooling &prop; T^-0.35) with a logistic-function blend, calibrated so the curve passes through both real (T,P/k) points; identify the local slope sign on the connecting branch and confirm it is negative (thermally unstable) between the two stable points.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly which of this lab's numbers are real, standard published values (level 2) and which are this lab's own illustrative curve-fitting choice (level 3, the specific logistic blending function and its width parameter, chosen only to reproduce the qualitative S-shape, not itself a measured quantity). Discuss what physical pressure terms (magnetic, cosmic-ray, turbulent) are omitted from the simple P=nkT model and how their omission could account for any residual CNM/WNM pressure mismatch.</p></section>
<section><h2>Deliverables</h2><ul><li>The six-phase pressure table with your own computed P/k values.</li><li>A plot (or SVG, following the lecture figure style) of your thermal-equilibrium curve with the unstable branch's slope sign explicitly stated.</li><li>A one-paragraph discussion of the CNM/WNM pressure-ratio result and what physics could explain any residual mismatch from exact equality.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct P/k arithmetic for all six phases with correct units (cm^-3 K).</li><li>Correctly identified pressure ratio and a reasoned (not merely asserted) equilibrium judgment.</li><li>Correctly identified negative-slope region on the constructed thermal-equilibrium curve.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>ISM phase parameters: McKee &amp; Ostriker (1977, ApJ 218, 148); Draine (2011) textbook Table 1.1 -- standard published, level 2; see <code>materials/ASTR360/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR360/src/generate_astr360_content.py</code>.</li></ul></section>
"""
    return lab_page(1, 'ISM Phase Pressure Balance and Thermal Equilibrium',
                     'Compute and compare pressures across all six real ISM phases and build a schematic thermal-equilibrium curve.', sections)


def make_pset_01():
    problems = (
        problem(1, 'Pressure balance at a different phase pair',
                f'<p>Using the real published (n,T) values for the warm ionized medium (WIM: n={ISM_PHASES["Warm ionized medium (WIM)"]["n_cm3"]:.2g} cm^-3, T={ISM_PHASES["Warm ionized medium (WIM)"]["T_k"]:.2g} K) and the hot ionized medium (HIM: n={ISM_PHASES["Hot ionized medium (HIM)"]["n_cm3"]:.2g} cm^-3, T={ISM_PHASES["Hot ionized medium (HIM)"]["T_k"]:.2g} K), compute both phases\' P/k and state whether they are closer to or farther from pressure equilibrium than the CNM/WNM pair discussed in the lecture.</p>') +
        problem(2, 'H II region pressure vs its surroundings',
                f'<p>Using the H II region phase\'s published parameters (n={ISM_PHASES["H II regions"]["n_cm3"]:.2g} cm^-3, T={ISM_PHASES["H II regions"]["T_k"]:.2g} K), compute its P/k and compare it quantitatively to the WNM\'s P/k. Given that H II regions are transient, short-lived structures (Unit 6 derives their formation), discuss whether the large pressure mismatch you find is a problem for the pressure-equilibrium framework or expected given their transience.</p>') +
        problem(3, 'A hypothetical seventh phase',
                '<p>Suppose observers discovered a seventh, previously unknown ISM phase in exact pressure equilibrium with the CNM (same P/k as the CNM\'s published value) but with a density of exactly 3.0 cm^-3. Compute this hypothetical phase\'s temperature, and state which of the six real phases in this unit\'s data it would most resemble in temperature (though not necessarily density).</p>') +
        problem(4, 'Filling factor sanity check',
                f'<p>Sum the published volume filling factors of all six phases in this unit\'s data. Comment on whether the sum is close to 1 (as it should be if the six phases genuinely partition the ISM\'s volume) and discuss one physical reason small deviations from exactly 1 might appear in real filling-factor estimates (e.g., overlapping definitions, unaccounted transitional gas).</p>', points=10)
    )
    return pset_page(1, 'ISM Phases and Pressure Balance', 'Apply this unit\'s pressure-balance framework to different real phase pairs and a hypothetical case.',
                      problems, OPENSTAX)


def make_pset_01_solutions():
    wim_p = ISM_PHASES['Warm ionized medium (WIM)']['n_cm3'] * ISM_PHASES['Warm ionized medium (WIM)']['T_k']
    him_p = ISM_PHASES['Hot ionized medium (HIM)']['n_cm3'] * ISM_PHASES['Hot ionized medium (HIM)']['T_k']
    hii_p = ISM_PHASES['H II regions']['n_cm3'] * ISM_PHASES['H II regions']['T_k']
    wnm_p = PHASE_PRESSURE_K['Warm neutral medium (WNM)']
    cnm_p = PHASE_PRESSURE_K['Cold neutral medium (CNM)']
    hypothetical_T = cnm_p / 3.0
    filling_sum = sum(d['filling'] for d in ISM_PHASES.values())
    s = (
        solution(1, 'Pressure balance at a different phase pair',
                  f'<p>P/k(WIM)={wim_p:,.0f} cm^-3 K, P/k(HIM)={him_p:,.0f} cm^-3 K, a ratio of {max(wim_p,him_p)/min(wim_p,him_p):.2f} -- notably farther from equilibrium than the CNM/WNM pair\'s ratio of {wnm_p/cnm_p:.2f}, consistent with the WIM/HIM not being expected to be in simple two-phase thermal-pressure balance the way CNM/WNM are (they are governed by different heating sources, ionizing radiation and supernova energy input respectively, not the same Field-instability mechanism).</p>',
                  [('Correct P/k arithmetic for both phases', 6), ('Correct ratio comparison to CNM/WNM', 5), ('Correct qualitative interpretation', 4)]) +
        solution(2, 'H II region pressure vs its surroundings',
                  f'<p>P/k(H II)={hii_p:,.0f} cm^-3 K versus P/k(WNM)={wnm_p:,.0f} cm^-3 K, a ratio of {hii_p/wnm_p:.1f} -- a large mismatch, but not a problem for the framework: H II regions are actively, freshly ionized and pressurized by a nearby hot star\'s ionizing flux (Unit 6) and are expected to expand and eventually dissipate rather than sit in long-term pressure equilibrium with the surrounding diffuse ISM.</p>',
                  [('Correct P/k arithmetic', 6), ('Correct ratio computed', 5), ('Correct physical reasoning about transience', 4)]) +
        solution(3, 'A hypothetical seventh phase',
                  f'<p>T = P/(k n) = {cnm_p:,.0f} cm^-3 K / 3.0 cm^-3 = {hypothetical_T:,.0f} K -- closest in temperature to the H II region phase (T={ISM_PHASES["H II regions"]["T_k"]:,.0f} K) among the six real phases, though at a much lower density than real H II regions.</p>',
                  [('Correct algebraic solve for T', 6), ('Correct identification of closest real phase', 5), ('Clear units', 4)]) +
        solution(4, 'Filling factor sanity check',
                  f'<p>Sum of published filling factors = {filling_sum:.4f}, close to but not exactly 1 -- the small deviation is expected given that these six phases\' filling factors come from different studies using somewhat different definitions and survey methods, not from a single self-consistent partition of the ISM\'s volume.</p>',
                  [('Correct summation', 5), ('Correct, non-overclaiming interpretation of the near-1 sum', 5)], )
    )
    return solutions_page(1, 'ISM Phases and Pressure Balance', s)


def make_pset_01_assessment():
    return assessment_md(1, 'ISM Phases and Pressure Balance',
                          ['Problem 1: verify correct P/k arithmetic and a reasoned (not just numeric) equilibrium comparison to CNM/WNM.',
                           'Problem 2: verify the student explains the large H II/WNM pressure mismatch physically rather than treating it as a framework failure.',
                           'Problem 3: verify correct algebraic solve for temperature given a fixed pressure and density.',
                           'Problem 4: verify the student does not overclaim the filling-factor sum is or should be exactly 1.'],
                          ['Confusing pressure ratio direction (stating phase A is "N times lower pressure" when it is actually higher).',
                           'Treating the H II region\'s pressure mismatch with the WNM as an error in the pressure-balance framework rather than expected transience.',
                           'Unit errors in P/k arithmetic (cm^-3 K is the conventional unit; watch for missing or extra factors).'])


# ===========================================================================
# LAB/PSET 02 (Lectures 3-4): 21 cm line, spin temperature, HI column density
# ===========================================================================
def make_lab_02() -> str:
    n_hi_cnm = hi_column_density_cm2(CNM_PEAK_TB_K, CNM_FWHM_KMS)
    n_hi_wnm = hi_column_density_cm2(WNM_PEAK_TB_K, WNM_FWHM_KMS)
    n_hi_total = n_hi_cnm + n_hi_wnm
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab applies Lecture 03's radiative-transfer solution and Lecture 04's column-density formula to a representative two-component (CNM+WNM) 21 cm brightness-temperature spectrum, and compares the result to two real, published all-sky-survey HI column densities.</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Component</th><th>T_spin (K)</th><th>Peak T_B (K)</th><th>FWHM (km/s)</th></tr></thead><tbody>
<tr><td>CNM</td><td>{CNM_TSPIN_K:.0f}</td><td>{CNM_PEAK_TB_K:.0f}</td><td>{CNM_FWHM_KMS:.1f}</td></tr>
<tr><td>WNM</td><td>{WNM_TSPIN_K:.0f}</td><td>{WNM_PEAK_TB_K:.0f}</td><td>{WNM_FWHM_KMS:.0f}</td></tr>
</tbody></table>
<p>T_spin values and characteristic linewidths are real, standard published CNM/WNM values (level 2, Kalberla &amp; Kerp 2009 review); the specific peak-T_B synthetic Gaussian profile shape is an illustrative representative spectrum (level 3), not a claimed measurement of one specific real sightline (see <code>../reference-log.md</code>). Real comparison sightlines: 3C 273 (N(HI)={SIGHTLINE_3C273['n_hi_cm2']:.2e} cm^-2, HI4PI Collaboration 2016) and Cygnus X-1 (N(H)={SIGHTLINE_CYGX1['n_hi_cm2']:.1e} cm^-2, X-ray absorption studies).</p></section>
<section><h2>Procedure</h2><ol>
<li>Using the Boltzmann population-ratio formula, compute n1/n0 for both the CNM and WNM spin temperatures and confirm both are close to, but measurably below, the high-temperature limit of 3.0.</li>
<li>Using the Gaussian-integral column-density formula, compute N(HI) separately for the CNM and WNM components and sum them for the total.</li>
<li>Compare your total N(HI) to the real, published 3C 273 sightline value and to the real, published Cygnus X-1 sightline value; state which real sightline your representative spectrum's total is closer to in order of magnitude, and why this is only a loose comparison (your spectrum is illustrative, not a fit to either specific sightline).</li>
<li>Recompute N(HI) for the CNM component using the full (not optically thin) radiative-transfer solution at a specified optical depth of tau=0.05, and confirm the optically thin approximation is accurate to better than 1% at this value.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss what would happen to your total N(HI) estimate if the CNM component were in fact optically thick (tau approaching or exceeding 1) rather than the optically thin tau=0.05 used above, and why narrow, high-peak-brightness CNM features are the ones most likely to violate the optically thin assumption in real spectra.</p></section>
<section><h2>Deliverables</h2><ul><li>Both components' population ratios, column densities, and the summed total.</li><li>A comparison table against the two real published sightline column densities.</li><li>The optically thin vs. full radiative-transfer cross-check at tau=0.05.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct Boltzmann population-ratio arithmetic for both spin temperatures.</li><li>Correct Gaussian-integral column-density arithmetic with the 1.8224e18 coefficient applied correctly.</li><li>Correctly disclosed level-1/level-2/level-3 distinctions when comparing the illustrative spectrum to real sightline values.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>3C 273 and Cygnus X-1 sightline column densities: standard published, level 2; see <code>materials/ASTR360/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR360/src/generate_astr360_content.py</code>.</li></ul></section>
"""
    return lab_page(2, 'The 21 cm Line: Spin Temperature and HI Column Density',
                     'Apply the 21 cm radiative-transfer solution and column-density formula to a representative spectrum and two real published sightlines.', sections)


def make_pset_02():
    problems = (
        problem(1, 'Population ratio at an intermediate spin temperature',
                f'<p>Compute the hyperfine population ratio n1/n0 for gas at T_spin=500 K (intermediate between the CNM and WNM values used in the lecture), and state whether it is closer to the CNM\'s ratio or to the high-temperature limit of exactly 3.0.</p>') +
        problem(2, 'A single-component column density',
                '<p>A newly observed 21 cm spectral feature has a single Gaussian component with peak T_B=12.0 K and FWHM=6.0 km/s. Compute its HI column density in cm^-2, and state whether it is closer in order of magnitude to this course\'s representative CNM component or its representative WNM component.</p>') +
        problem(3, 'Toward the Galactic center vs. 3C 273',
                f'<p>Using only the given real Cygnus X-1 (N(H)={SIGHTLINE_CYGX1["n_hi_cm2"]:.1e} cm^-2, Galactic latitude b={SIGHTLINE_CYGX1["b_deg"]:.2f} deg) and 3C 273 (N(HI)={SIGHTLINE_3C273["n_hi_cm2"]:.2e} cm^-2, b={SIGHTLINE_3C273["b_deg"]:.2f} deg) values, compute the ratio of their column densities and connect the large difference to the two sightlines\' different Galactic latitudes (without deriving a full Galactic HI disk model).</p>') +
        problem(4, 'Optical depth cross-check',
                f'<p>For CNM gas at T_spin=100 K, compute the brightness temperature predicted by the full radiative-transfer solution at tau=0.5 (no longer safely optically thin) and compare it to the optically thin approximation\'s prediction at the same tau. Compute the percent error the optically thin approximation makes at this tau, and state whether it over- or under-estimates the true brightness temperature.</p>')
    )
    return pset_page(2, 'The 21 cm Line and HI Column Density', 'Extend this unit\'s radiative-transfer and column-density tools to new spin temperatures, spectra, and sightlines.',
                      problems, OPENSTAX)


def make_pset_02_solutions():
    ratio_500 = spin_temperature_population_ratio(500.0)
    n_hi_new = hi_column_density_cm2(12.0, 6.0)
    ratio_sightlines = SIGHTLINE_CYGX1['n_hi_cm2'] / SIGHTLINE_3C273['n_hi_cm2']
    tb_full = brightness_temperature_k(CNM_TSPIN_K, 0.5)
    tb_thin = CNM_TSPIN_K * 0.5
    pct_err = abs(tb_thin - tb_full) / tb_full * 100
    s = (
        solution(1, 'Population ratio at an intermediate spin temperature',
                  f'<p>n1/n0 = 3 exp(-{T_STAR_21CM_K:.4f}/500) = {ratio_500:.5f} -- much closer to the high-temperature limit of 3.0 than the CNM\'s ratio ({spin_temperature_population_ratio(CNM_TSPIN_K):.5f}), because 500 K is already large compared to T*={T_STAR_21CM_K*1000:.1f} mK.</p>',
                  [('Correct formula application', 7), ('Correct qualitative comparison', 8)]) +
        solution(2, 'A single-component column density',
                  f'<p>N(HI) = 1.8224e18 x 12.0 x 6.0 x sqrt(pi/(4 ln2)) = {n_hi_new:.3e} cm^-2 -- intermediate in order of magnitude between this course\'s CNM ({hi_column_density_cm2(CNM_PEAK_TB_K, CNM_FWHM_KMS):.2e} cm^-2) and WNM ({hi_column_density_cm2(WNM_PEAK_TB_K, WNM_FWHM_KMS):.2e} cm^-2) components, consistent with its intermediate peak temperature and linewidth.</p>',
                  [('Correct Gaussian-integral formula application', 8), ('Correct order-of-magnitude comparison', 7)]) +
        solution(3, 'Toward the Galactic center vs. 3C 273',
                  f'<p>Ratio = {ratio_sightlines:.1f} -- Cygnus X-1 lies much closer to the Galactic plane (b={SIGHTLINE_CYGX1["b_deg"]:.2f} deg) than 3C 273 (b={SIGHTLINE_3C273["b_deg"]:.2f} deg), and HI is strongly concentrated toward the Galactic plane, so a low-latitude sightline like Cygnus X-1\'s passes through far more atomic hydrogen than a high-latitude sightline like 3C 273\'s.</p>',
                  [('Correct ratio computed', 7), ('Correct qualitative Galactic-latitude reasoning', 8)]) +
        solution(4, 'Optical depth cross-check',
                  f'<p>Full solution: T_B = 100(1-e^-0.5) = {tb_full:.3f} K. Optically thin approximation: T_B &asymp; 100 x 0.5 = {tb_thin:.1f} K. Percent error = {pct_err:.1f}%, with the optically thin approximation over-estimating the true brightness temperature at this larger, no-longer-safely-thin optical depth.</p>',
                  [('Correct full radiative-transfer calculation', 7), ('Correct percent-error direction (over-, not under-, estimate)', 8)])
    )
    return solutions_page(2, 'The 21 cm Line and HI Column Density', s)


def make_pset_02_assessment():
    return assessment_md(2, 'The 21 cm Line and HI Column Density',
                          ['Problem 1: verify correct exponential evaluation and a reasoned (not merely numeric) qualitative comparison.',
                           'Problem 2: verify the Gaussian-integral coefficient (sqrt(pi/(4 ln2))) is included, not omitted.',
                           'Problem 3: verify the Galactic-latitude reasoning is physically correct (lower latitude means more HI, not less).',
                           'Problem 4: verify the direction of the optically thin approximation\'s error (over-estimate, not under-estimate) is stated correctly.'],
                          ['Omitting the sqrt(pi/(4 ln2)) &asymp; 1.0645 Gaussian-integral factor entirely.',
                           'Reversing which sightline (Cygnus X-1 vs 3C 273) has the higher column density.',
                           'Stating the optically thin approximation always under-estimates N(HI) regardless of optical depth (it can go either direction depending on the specific formula being compared, but for this brightness-temperature comparison at tau=0.5 it over-estimates).'])


# ===========================================================================
# LAB/PSET 03 (Lectures 5-6): Dust extinction, reddening, thermal emission
# ===========================================================================
def make_lab_03() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab applies Lecture 05's Cardelli, Clayton &amp; Mathis (1989) extinction-curve parametrization to the real, heavily reddened star Cygnus OB2 No. 12, computing extinction at multiple bands and propagating the correction to an intrinsic (dereddened) color, then extends into Lecture 06's modified-blackbody dust-temperature model.</p></section>
<section><h2>Materials and Data</h2>
<p>Cygnus OB2 No. 12: E(B-V)={CYGOB2_12['ebv_mag']:.2f} mag, R_V={CYGOB2_12['r_v']:.1f}, distance&asymp;{CYGOB2_12['distance_pc']:.0f} pc (Massey &amp; Thompson 1991, standard published, level 2). Cardelli, Clayton &amp; Mathis (1989) diffuse-ISM optical/NIR parametrization coefficients (Lecture 05).</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute A_V for Cygnus OB2 No. 12 from its published E(B-V) and R_V.</li>
<li>Using the Cardelli parametrization, compute A(lambda)/A_V at V band (x=1/0.545 um^-1), B band (x=1/0.438 um^-1), and a representative near-infrared band, K (x=1/2.19 um^-1), and hence A_V, A_B, and A_K individually for this star.</li>
<li>Confirm A(V)/A_V evaluates to 1.000 (a self-consistency check on the parametrization implementation) and confirm A_K/A_V is much smaller than A_B/A_V (the physical basis for observing heavily reddened stars in the infrared).</li>
<li>Using a representative molecular-cloud dust temperature of 20 K and emissivity index beta=2, evaluate the modified-blackbody spectrum at three wavelengths (100, 250, and 850 micron) and identify which is closest to the emission peak.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss how much your computed A_V would change if you had instead (incorrectly) assumed the diffuse-ISM average R_V=3.1 for Cygnus OB2 No. 12 rather than its own measured R_V=3.0 (a small correction in this case), and contrast this with how much larger an error the same substitution would cause for the anomalous HD 200775 sightline (R_V=5.0) discussed in the lecture.</p></section>
<section><h2>Deliverables</h2><ul><li>Computed A_V, A_B, A_K for Cygnus OB2 No. 12 with full derivations.</li><li>The V-band self-consistency check result.</li><li>The modified-blackbody wavelength evaluation and identified peak.</li><li>The R_V-substitution error discussion for both stars.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct application of the Cardelli parametrization at all three bands with correct x=1/lambda values.</li><li>Correct A_V=R_V E(B-V) arithmetic.</li><li>Correctly reasoned R_V-substitution error comparison between the two real stars.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Cygnus OB2 No. 12 and HD 200775 parameters: standard published, level 2; see <code>materials/ASTR360/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR360/src/generate_astr360_content.py</code>.</li></ul></section>
"""
    return lab_page(3, 'Interstellar Extinction and Dust Emission: Cygnus OB2 No. 12',
                     'Apply the Cardelli extinction-curve parametrization and a modified-blackbody dust-emission model to real reddened-star and molecular-cloud data.', sections)


def make_pset_03():
    problems = (
        problem(1, 'A different heavily reddened star',
                '<p>A star has E(B-V)=1.80 mag and R_V=3.1 (the diffuse-ISM average). Compute its A_V, and compute the flux dimming factor 10^(A_V/2.5) this extinction causes.</p>') +
        problem(2, 'HD 200775\'s own extinction',
                f'<p>Using HD 200775\'s own real published parameters (E(B-V)={HD200775["ebv_mag"]:.2f} mag, R_V={HD200775["r_v"]:.1f}), compute its A_V, and compare it to Cygnus OB2 No. 12\'s A_V computed in the lab. State which star suffers greater total visual extinction despite having a smaller color excess, and explain why in one sentence.</p>') +
        problem(3, 'R_V misassumption error',
                f'<p>If an observer incorrectly assumed the diffuse-ISM average R_V=3.1 for HD 200775 (rather than its real R_V={HD200775["r_v"]:.1f}) while using its real measured E(B-V)={HD200775["ebv_mag"]:.2f} mag, compute the resulting (incorrect) A_V and state the percent error relative to the correct A_V computed using the real R_V.</p>') +
        problem(4, 'Dust emission peak shift',
                '<p>Using the modified-blackbody model at beta=2, compare the wavelength of peak emission for dust at 15 K versus dust at 50 K (both values used in the lecture\'s figure). State qualitatively (using Wien\'s-law-like reasoning) which is expected to peak at shorter wavelength and why, and name one real astronomical survey/telescope wavelength band well-suited to detecting the 50 K component that would be poorly suited for the 15 K component.</p>', points=10)
    )
    return pset_page(3, 'Extinction, Reddening, and Dust Emission', 'Apply this unit\'s extinction and dust-emission tools to a second real anomalous-extinction star and a temperature-contrast case.',
                      problems, OPENSTAX)


def make_pset_03_solutions():
    av_new = extinction_av_mag(1.80, 3.1)
    dim_factor = 10 ** (av_new / 2.5)
    av_hd200775_wrong = extinction_av_mag(HD200775['ebv_mag'], 3.1)
    pct_err = abs(av_hd200775_wrong - AV_HD200775) / AV_HD200775 * 100
    s = (
        solution(1, 'A different heavily reddened star',
                  f'<p>A_V = 3.1 x 1.80 = {av_new:.2f} mag, giving a flux dimming factor of 10^({av_new:.2f}/2.5) = {dim_factor:.2f}.</p>',
                  [('Correct A_V arithmetic', 7), ('Correct dimming-factor arithmetic', 8)]) +
        solution(2, 'HD 200775\'s own extinction',
                  f'<p>A_V(HD 200775) = {AV_HD200775:.2f} mag, versus A_V(Cyg OB2-12) = {AV_CYGOB2_12:.2f} mag -- Cygnus OB2 No. 12 suffers substantially greater total extinction despite the comparison depending on both E(B-V) and R_V together (A_V=R_V E(B-V)); Cyg OB2-12\'s much larger E(B-V) more than compensates for HD 200775\'s larger R_V.</p>',
                  [('Correct A_V arithmetic for HD 200775', 7), ('Correct comparative statement in the right direction', 8)]) +
        solution(3, 'R_V misassumption error',
                  f'<p>Incorrect A_V (using R_V=3.1) = 3.1 x {HD200775["ebv_mag"]:.2f} = {av_hd200775_wrong:.2f} mag, versus the correct A_V (using R_V={HD200775["r_v"]:.1f}) = {AV_HD200775:.2f} mag -- a percent error of {pct_err:.1f}%, a substantial systematic underestimate from assuming the diffuse-ISM R_V for this anomalous dense-cloud sightline.</p>',
                  [('Correct incorrect-R_V A_V arithmetic', 7), ('Correct percent-error computation and direction (underestimate)', 8)]) +
        solution(4, 'Dust emission peak shift',
                  '<p>The 50 K component peaks at shorter wavelength than the 15 K component (Wien\'s-law-like behavior even for a modified blackbody); a far-infrared instrument like Herschel/PACS (70-160 micron) is well-suited to the warmer 50 K component but would miss much of the emission from the colder 15 K component, better captured at longer submillimeter wavelengths (e.g., Herschel/SPIRE or ALMA).</p>',
                  [('Correct qualitative peak-shift direction', 5), ('Correct, reasoned wavelength-regime example', 5)])
    )
    return solutions_page(3, 'Extinction, Reddening, and Dust Emission', s)


def make_pset_03_assessment():
    return assessment_md(3, 'Extinction, Reddening, and Dust Emission',
                          ['Problem 1: verify A_V=R_V E(B-V) arithmetic and the flux-ratio formula 10^(A_V/2.5).',
                           'Problem 2: verify the student correctly compares total A_V (not just E(B-V)) between the two stars.',
                           'Problem 3: verify the percent-error direction (underestimate) is stated correctly, not just the magnitude.',
                           'Problem 4: verify the Wien\'s-law-like peak-shift direction is correct (warmer dust peaks at shorter wavelength).'],
                          ['Comparing E(B-V) alone instead of A_V=R_V E(B-V) when asked which star has greater total extinction.',
                           'Sign errors in percent-error calculations (reporting an underestimate as an overestimate or vice versa).',
                           'Confusing which SED (15 K or 50 K) peaks at shorter wavelength.'])


# ===========================================================================
# LAB/PSET 04 (Lectures 7-8): Molecular clouds, CO, virial mass
# ===========================================================================
def make_lab_04() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab reproduces Lecture 07's three-way OMC-1 mass comparison (direct, CO-derived, virial) and extends it to the real, quiescent Taurus Molecular Cloud, applying Lecture 08's Larson-law virial-mass estimator to both.</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Cloud</th><th>Distance (pc)</th><th>Radius (pc)</th><th>n(H2) (cm^-3)</th><th>T (K)</th><th>CO FWHM (km/s)</th></tr></thead><tbody>
<tr><td>Orion Molecular Cloud (OMC-1)</td><td>{ORION_MOLECULAR_CLOUD['distance_pc']:.0f}</td><td>{ORION_MOLECULAR_CLOUD['radius_pc']:.1f}</td><td>{ORION_MOLECULAR_CLOUD['n_h2_cm3']:.1e}</td><td>{ORION_MOLECULAR_CLOUD['temp_k']:.0f}</td><td>{ORION_MOLECULAR_CLOUD['co_linewidth_kms']:.1f}</td></tr>
<tr><td>Taurus Molecular Cloud</td><td>{TAURUS_MOLECULAR_CLOUD['distance_pc']:.0f}</td><td>{TAURUS_MOLECULAR_CLOUD['radius_pc']:.1f}</td><td>{TAURUS_MOLECULAR_CLOUD['n_h2_cm3']:.1e}</td><td>{TAURUS_MOLECULAR_CLOUD['temp_k']:.0f}</td><td>{TAURUS_MOLECULAR_CLOUD['co_linewidth_kms']:.1f}</td></tr>
</tbody></table>
<p>Standard published values, level 2 (Genzel &amp; Stutzki 1989 for OMC-1; Goldsmith et al. 2008 for Taurus). X_CO={X_CO_CM2_K_KMS:.1e} cm^-2 (K km/s)^-1 (Bolatto, Wolfire &amp; Leroy 2013).</p></section>
<section><h2>Procedure</h2><ol>
<li>For Taurus, compute the direct (density x volume) H2 mass, exactly as Lecture 07 did for OMC-1.</li>
<li>For Taurus, compute the CO-derived mass via the X_CO conversion, following Lecture 07's method.</li>
<li>For Taurus, compute the virial mass using Lecture 08's M_vir=5 sigma^2 R/G estimator, with sigma=FWHM/2.355.</li>
<li>Tabulate all three mass estimates for both Orion and Taurus side by side, and discuss which cloud shows better agreement among its three independent estimates, and why (Taurus's more quiescent, less turbulent nature is a reasonable hypothesis to test against the numbers).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Using Larson's sigma &prop; R^0.5 relation, explain why Taurus's larger radius but much narrower linewidth than OMC-1 illustrates the size-linewidth relation's role in setting virial mass, and identify which single measurement (radius or linewidth) you would most want an independent, higher-precision check on if the two clouds' virial-to-CO mass ratios disagreed substantially.</p></section>
<section><h2>Deliverables</h2><ul><li>Taurus's direct, CO-derived, and virial mass estimates with full derivations.</li><li>The four-cloud (Orion + Taurus, three methods each) mass comparison table.</li><li>A short discussion of which cloud's three estimates agree best and why.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct direct-mass volume/density arithmetic for Taurus.</li><li>Correct X_CO conversion arithmetic for Taurus.</li><li>Correct virial-mass arithmetic (including the sigma=FWHM/2.355 conversion) for Taurus.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Orion Molecular Cloud and Taurus Molecular Cloud parameters: standard published, level 2; see <code>materials/ASTR360/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR360/src/generate_astr360_content.py</code>.</li></ul></section>
"""
    return lab_page(4, 'Molecular Cloud Mass: Orion and Taurus Compared',
                     'Compute and compare direct, CO-derived, and virial mass estimates for two real molecular clouds.', sections)


def make_pset_04():
    problems = (
        problem(1, 'A denser hypothetical clump',
                f'<p>A hypothetical molecular clump has the same radius as OMC-1 ({ORION_MOLECULAR_CLOUD["radius_pc"]:.1f} pc) but twice its density (2 x {ORION_MOLECULAR_CLOUD["n_h2_cm3"]:.1e} cm^-3). Compute its direct H2 mass and state the exact factor by which it exceeds OMC-1\'s own direct mass (derive this factor algebraically before computing the number, since density enters the mass linearly at fixed volume).</p>') +
        problem(2, 'CO luminosity from a mass',
                f'<p>Using the X_CO conversion factor (X_CO={X_CO_CM2_K_KMS:.1e} cm^-2 (K km/s)^-1), compute the implied CO luminosity (in K km/s pc^2) for a cloud with H2 mass 5.0e3 Msun, and state whether this luminosity is larger or smaller than the value implied by Taurus\'s real mass.</p>') +
        problem(3, 'Virial mass sensitivity to linewidth',
                f'<p>Recompute Taurus\'s virial mass assuming its CO linewidth were instead 3.0 km/s (double the real published value, with the radius unchanged). Compute the factor by which the virial mass changes, and confirm it matches the M_vir &prop; sigma^2 scaling derived in the lecture.</p>') +
        problem(4, 'Bound or unbound?',
                f'<p>Using your Taurus virial mass from the lab and Taurus\'s CO-derived mass, compute the ratio M_CO/M_vir, and using the same ratio computed for OMC-1 in the lab, state which cloud appears closer to virial balance and which appears more likely to be gravitationally unbound (M_vir substantially exceeding M_CO) or bound/contracting (M_CO substantially exceeding M_vir).</p>')
    )
    return pset_page(4, 'Molecular Cloud Mass Estimators', 'Extend this unit\'s three-way mass-estimator comparison to new hypothetical and real scenarios.',
                      problems, OPENSTAX)


def make_pset_04_solutions():
    denser_mass = ORION_MOLECULAR_CLOUD['n_h2_cm3'] * 2.0 * 1.0e6 * (4.0 / 3.0) * math.pi * (ORION_MOLECULAR_CLOUD['radius_pc'] * PC_M) ** 3 * MU_MOLECULAR * M_H_KG / M_SUN
    factor = denser_mass / OMC1_H2_MASS_DIRECT
    l_co_5000 = 5.0e3 * M_SUN / (2.0 * M_H_KG) / X_CO_CM2_K_KMS / (PC_M * 100.0) ** 2
    l_co_taurus = TAURUS_MOLECULAR_CLOUD['mass_msun'] * M_SUN / (2.0 * M_H_KG) / X_CO_CM2_K_KMS / (PC_M * 100.0) ** 2
    taurus_vir_doubled = virial_mass_msun(3.0, TAURUS_MOLECULAR_CLOUD['radius_pc'])
    doubled_factor = taurus_vir_doubled / TAURUS_VIRIAL_MASS
    ratio_taurus = TAURUS_MOLECULAR_CLOUD['mass_msun'] / TAURUS_VIRIAL_MASS
    ratio_omc1 = OMC1_H2_MASS_FROM_CO / OMC1_VIRIAL_MASS
    s = (
        solution(1, 'A denser hypothetical clump',
                  f'<p>Since M &prop; n at fixed volume, doubling density exactly doubles the direct mass: M={denser_mass:,.0f} Msun, a factor of {factor:.2f} above OMC-1\'s direct mass ({OMC1_H2_MASS_DIRECT:,.0f} Msun) -- confirming the predicted factor-of-2 scaling.</p>',
                  [('Correct algebraic factor-of-2 derivation', 7), ('Correct numeric mass', 8)]) +
        solution(2, 'CO luminosity from a mass',
                  f'<p>L_CO(5.0e3 Msun) = {l_co_5000:.1f} K km/s pc^2, versus L_CO(Taurus real mass, {TAURUS_MOLECULAR_CLOUD["mass_msun"]:,.0f} Msun) = {l_co_taurus:.1f} K km/s pc^2 -- the 5.0e3 Msun hypothetical cloud\'s implied CO luminosity is smaller than Taurus\'s real value, consistent with its smaller assumed mass.</p>',
                  [('Correct inverse X_CO conversion', 8), ('Correct comparison direction', 7)]) +
        solution(3, 'Virial mass sensitivity to linewidth',
                  f'<p>M_vir(sigma doubled)={taurus_vir_doubled:,.0f} Msun, a factor of {doubled_factor:.2f} above the original Taurus virial mass ({TAURUS_VIRIAL_MASS:,.0f} Msun) -- matching the predicted M_vir &prop; sigma^2 scaling (doubling sigma should quadruple M_vir).</p>',
                  [('Correct virial-mass recomputation', 7), ('Correct confirmation of the sigma^2 scaling', 8)]) +
        solution(4, 'Bound or unbound?',
                  f'<p>Taurus: M_CO/M_vir={ratio_taurus:.2f}. OMC-1: M_CO/M_vir={ratio_omc1:.2f}. Both ratios are within roughly a factor of 2 of unity, but OMC-1\'s ratio is closer to 1, suggesting it is somewhat closer to virial balance, while Taurus\'s lower ratio is more consistent with a cloud that is comparatively less centrally concentrated/bound relative to its turbulent support -- stated as a comparative, not absolute, conclusion given the simplified uniform-sphere virial model\'s known limitations (Lecture 08).</p>',
                  [('Correct ratio computation for both clouds', 8), ('Correctly hedged, comparative (not absolute) conclusion', 7)])
    )
    return solutions_page(4, 'Molecular Cloud Mass Estimators', s)


def make_pset_04_assessment():
    return assessment_md(4, 'Molecular Cloud Mass Estimators',
                          ['Problem 1: verify the algebraic factor-of-2 scaling is derived before the numeric answer is given.',
                           'Problem 2: verify correct inversion of the X_CO conversion (mass to luminosity, not luminosity to mass).',
                           'Problem 3: verify the M_vir &prop; sigma^2 scaling is confirmed numerically, not just asserted.',
                           'Problem 4: verify the bound/unbound conclusion is stated comparatively and hedged given the model\'s known limitations, not as an absolute claim.'],
                          ['Forgetting the factor of 2 (H2 molecules, not H atoms) in the X_CO mass conversion.',
                           'Treating M_vir=M_CO exactly as proof of virial equilibrium rather than a rough, hedged consistency check.',
                           'Sign/direction errors in the sigma-doubling scaling check (reporting a factor of 2 instead of 4).'])


# ===========================================================================
# LAB/PSET 05 (Lectures 9-10): Jeans mass, free-fall time
# ===========================================================================
def make_lab_05() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes Jeans mass, Jeans length, and free-fall time for the OMC-1 dense core and Barnard 68 side by side, and evaluates each against its own observed (or, for OMC-1, representative) mass.</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Core</th><th>n(H2) (cm^-3)</th><th>T (K)</th><th>Observed mass (Msun)</th></tr></thead><tbody>
<tr><td>OMC-1 dense core</td><td>{OMC1_DENSE_CORE['n_h2_cm3']:.1e}</td><td>{OMC1_DENSE_CORE['temp_k']:.0f}</td><td>(representative dense-core values; not individually mass-measured in this course\'s dataset)</td></tr>
<tr><td>Barnard 68</td><td>{BARNARD68['n_h2_cm3']:.1e}</td><td>{BARNARD68['temp_k']:.0f}</td><td>{BARNARD68['mass_msun']:.1f}</td></tr>
</tbody></table>
<p>Standard published values, level 2 (Bergin &amp; Tafalla 2007 for the representative dense-core values; Alves, Lada &amp; Lada 2001 for Barnard 68's real measured mass, radius, and density).</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute the Jeans length and Jeans mass for both cores using Lecture 09's formulas.</li>
<li>Compute the free-fall time for both cores using Lecture 10's formula.</li>
<li>For Barnard 68, compare the computed Jeans mass to its real observed mass ({BARNARD68['mass_msun']:.1f} Msun) and state whether it is above, below, or comparable to the instability threshold.</li>
<li>Using the observed star-formation efficiency per free-fall time (epsilon_ff~1-2%, Lecture 10), estimate an effective star-formation timescale for the OMC-1 core, and compare it to the core's own free-fall time.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss explicitly why the simple Jeans criterion's idealized assumptions (uniform density, no turbulence, no magnetic support, no rotation) mean Barnard 68's near-critical Jeans-mass result should be read as "consistent with marginal instability," not as a precise, exact prediction of imminent collapse.</p></section>
<section><h2>Deliverables</h2><ul><li>Jeans length, Jeans mass, and free-fall time for both cores with full derivations.</li><li>The Barnard 68 instability-threshold comparison.</li><li>The OMC-1 effective star-formation timescale estimate.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct Jeans length/mass arithmetic with correct SI-to-cm^-3 density conversion.</li><li>Correct free-fall time arithmetic.</li><li>Correctly hedged (not overclaimed) Barnard 68 instability conclusion.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>OMC-1 dense-core and Barnard 68 parameters: standard published, level 2; see <code>materials/ASTR360/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR360/src/generate_astr360_content.py</code>.</li></ul></section>
"""
    return lab_page(5, 'Jeans Mass, Jeans Length, and Free-Fall Time',
                     'Compute and compare gravitational-instability and collapse-timescale criteria for two real dense cores.', sections)


def make_pset_05():
    problems = (
        problem(1, 'Barnard 68 at a colder temperature',
                f'<p>Recompute Barnard 68\'s Jeans mass assuming its temperature were instead 8 K (colder than the real published {BARNARD68["temp_k"]:.0f} K, with density unchanged). State whether this makes Barnard 68 more or less prone to gravitational instability, and connect your answer to the Jeans mass\'s explicit T^(3/2) dependence.</p>') +
        problem(2, 'A denser hypothetical core\'s free-fall time',
                f'<p>Compute the free-fall time for a hypothetical dense core with n(H2)=1.0e6 cm^-3 (ten times the OMC-1 core\'s density), and state the exact factor by which it differs from the OMC-1 core\'s free-fall time, connecting your answer to the t_ff &prop; rho^(-1/2) scaling.</p>') +
        problem(3, 'Jeans length in AU',
                f'<p>Convert the OMC-1 dense core\'s Jeans length (computed in the lab, in pc) into astronomical units (AU), and compare it to the solar system\'s scale (e.g., Neptune\'s orbital radius, about 30 AU) to give a physically intuitive sense of the Jeans length\'s size.</p>', points=10) +
        problem(4, 'Star-formation efficiency sensitivity',
                '<p>Using the OMC-1 core\'s free-fall time from the lab, compute the effective star-formation timescale for two different assumed efficiencies, epsilon_ff=1% and epsilon_ff=2%, and state the factor by which the two timescale estimates differ from each other.</p>')
    )
    return pset_page(5, 'Jeans Instability and Collapse Timescales', 'Extend this unit\'s Jeans-mass and free-fall-time tools to new temperatures, densities, and efficiency assumptions.',
                      problems, OPENSTAX)


def make_pset_05_solutions():
    mj_cold = jeans_mass_msun(8.0, MU_MOLECULAR, BARNARD68['n_h2_cm3'])
    tff_denser = free_fall_time_yr(1.0e6, MU_MOLECULAR)
    tff_factor = OMC1_CORE_FREEFALL_TIME_YR / tff_denser
    jeans_length_au = OMC1_CORE_JEANS_LENGTH_PC * PC_M / 1.496e11
    t_sf_1pct = OMC1_CORE_FREEFALL_TIME_YR / 0.01
    t_sf_2pct = OMC1_CORE_FREEFALL_TIME_YR / 0.02
    s = (
        solution(1, 'Barnard 68 at a colder temperature',
                  f'<p>M_J(8 K) = {mj_cold:.2f} Msun, lower than the real-temperature result ({BARNARD68_JEANS_MASS:.2f} Msun at {BARNARD68["temp_k"]:.0f} K) -- colder gas has a smaller Jeans mass (M_J &prop; T^{{3/2}}), so Barnard 68 would be *more* prone to instability at this lower, hypothetical temperature, since less mass would be required to exceed the (now smaller) critical threshold.</p>',
                  [('Correct Jeans-mass recomputation at 8 K', 8), ('Correct qualitative direction (more, not less, unstable)', 7)]) +
        solution(2, 'A denser hypothetical core\'s free-fall time',
                  f'<p>t_ff(1.0e6 cm^-3)={tff_denser:,.0f} yr, a factor of {tff_factor:.2f} shorter than the OMC-1 core\'s free-fall time ({OMC1_CORE_FREEFALL_TIME_YR:,.0f} yr) -- consistent with the t_ff &prop; rho^(-1/2) scaling, since a factor-of-10 density increase should shorten t_ff by a factor of sqrt(10)={math.sqrt(10):.2f}.</p>',
                  [('Correct free-fall-time recomputation', 8), ('Correct confirmation of the sqrt(10) scaling factor', 7)]) +
        solution(3, 'Jeans length in AU',
                  f'<p>Jeans length = {OMC1_CORE_JEANS_LENGTH_PC:.4f} pc = {jeans_length_au:,.0f} AU -- roughly {jeans_length_au/30:.0f} times Neptune\'s orbital radius, i.e. a Jeans-unstable region at this core\'s density and temperature spans a region many times larger than the entire solar system.</p>',
                  [('Correct pc-to-AU conversion', 5), ('Correct, physically intuitive comparison', 5)]) +
        solution(4, 'Star-formation efficiency sensitivity',
                  f'<p>At epsilon_ff=1%: t_SF&asymp;{t_sf_1pct:,.0f} yr. At epsilon_ff=2%: t_SF&asymp;{t_sf_2pct:,.0f} yr -- a factor of exactly 2 difference between the two timescale estimates, directly reflecting the inverse relationship between assumed efficiency and effective star-formation timescale.</p>',
                  [('Correct arithmetic for both efficiency assumptions', 8), ('Correct factor-of-2 relationship identified', 7)])
    )
    return solutions_page(5, 'Jeans Instability and Collapse Timescales', s)


def make_pset_05_assessment():
    return assessment_md(5, 'Jeans Instability and Collapse Timescales',
                          ['Problem 1: verify the T^(3/2) scaling direction is correctly connected to increased, not decreased, instability at lower T.',
                           'Problem 2: verify the rho^(-1/2) scaling is confirmed numerically against the sqrt(10) prediction.',
                           'Problem 3: verify correct pc-to-AU unit conversion (1 pc = 206,265 AU).',
                           'Problem 4: verify the inverse efficiency-timescale relationship is correctly identified as a factor of 2, not 1% or 2% directly.'],
                          ['Reversing the direction of the Jeans-mass temperature dependence (claiming colder gas is more stable rather than less).',
                           'Unit-conversion errors between pc and AU (a factor-of-206,265 error is easy to introduce).',
                           'Confusing free-fall time with the efficiency-corrected star-formation timescale.'])


# ===========================================================================
# LAB/PSET 06 (Lectures 11-12): Stromgren sphere, H II region diagnostics
# ===========================================================================
def make_lab_06() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes the Stromgren radius for the Orion Nebula in full, compares it to the nebula's real observed size, and applies real Orion Nebula spectroscopic diagnostics (Te, n_e) to justify the input parameters used.</p></section>
<section><h2>Materials and Data</h2>
<p>theta1 Orionis C: spectral type {ORION_NEBULA['spectral_type']}, T_eff&asymp;{ORION_NEBULA['teff_k']:,.0f} K, Q_H={ORION_NEBULA['q_h_photons_s']:.1e} photons/s (Vacca, Garmany &amp; Shull 1996; Martins, Schaerer &amp; Hillier 2005, standard published, level 2). Orion Nebula: n_e={ORION_NEBULA['n_e_cm3']:.0f} cm^-3, Te={ORION_NEBULA['te_k']:,.0f} K (Baldwin et al. 1991; Osterbrock &amp; Ferland 2006, level 2), observed radius&asymp;{ORION_NEBULA['observed_radius_pc']:.1f} pc, distance={ORION_NEBULA['distance_pc']:.0f} pc (Menten et al. 2007).</p></section>
<section><h2>Procedure</h2><ol>
<li>Using the case B recombination coefficient at Te={ORION_NEBULA['te_k']:,.0f} K, compute the Stromgren radius from Q_H and n_e.</li>
<li>Compare your computed Stromgren radius to the nebula's real observed radius, and compute the percent difference.</li>
<li>Discuss, quantitatively where possible, at least two real physical reasons for the discrepancy (e.g., non-uniform density with a lower average density than the quoted representative n_e over the nebula's full extent, density-bounded rather than ionization-bounded geometry, or contributions from additional fainter ionizing stars in the Trapezium cluster beyond theta1 Ori C alone).</li>
<li>Compute the recombination timescale and confirm it is astronomically short compared to theta1 Ori C's stellar lifetime, justifying the equilibrium assumption.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Explain why a factor-of-order-unity discrepancy between the idealized Stromgren radius and a real nebula's observed size should be considered an expected, honest limitation of the idealized model rather than a computational error, and identify what additional observation (e.g., a resolved density map) would let you test which of your proposed explanations in Step 3 dominates.</p></section>
<section><h2>Deliverables</h2><ul><li>The computed Stromgren radius with full derivation.</li><li>The percent-difference comparison to the observed radius.</li><li>At least two specific, physically reasoned explanations for the discrepancy.</li><li>The recombination-timescale equilibrium justification.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct Stromgren-radius arithmetic with correct alpha_B and unit handling (cm, then converted to pc).</li><li>Correctly computed percent difference.</li><li>At least two specific, non-generic physical explanations for the model-observation discrepancy.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Orion Nebula and theta1 Orionis C parameters: standard published, level 2; see <code>materials/ASTR360/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR360/src/generate_astr360_content.py</code>.</li></ul></section>
"""
    return lab_page(6, 'The Stromgren Sphere: The Orion Nebula',
                     'Compute the Stromgren radius for a real H II region and reconcile it with the nebula\'s observed size using real spectroscopic diagnostics.', sections)


def make_pset_06():
    problems = (
        problem(1, 'The Rosette Nebula',
                f'<p>Using the Rosette Nebula\'s real published parameters (Q_H={ROSETTE_NEBULA["q_h_photons_s"]:.1e} photons/s from the NGC 2244 cluster, n_e={ROSETTE_NEBULA["n_e_cm3"]:.0f} cm^-3), compute its Stromgren radius and compare it to its real observed radius ({ROSETTE_NEBULA["observed_radius_pc"]:.0f} pc). State whether the Rosette Nebula\'s model-observation discrepancy is larger or smaller (in percentage terms) than the Orion Nebula\'s from the lab, and suggest one physical reason low-density, evolved H II regions like the Rosette might show a different-sized discrepancy than compact, young ones like Orion.</p>') +
        problem(2, 'Ionizing photon rate needed for a target radius',
                f'<p>Using the Orion Nebula\'s real n_e, compute what value of Q_H would be required to produce a Stromgren radius exactly equal to the nebula\'s observed radius ({ORION_NEBULA["observed_radius_pc"]:.1f} pc), and compare this required Q_H to theta1 Ori C\'s real published value. State what this comparison implies about whether Orion is more consistent with an ionization-bounded or a density-bounded picture.</p>') +
        problem(3, 'Recombination-line ratio sanity check',
                '<p>Using the theoretical case B Balmer decrement value (Halpha/Hbeta=2.86 at Te=10^4 K, given in the lecture), state what an observed ratio of 4.0 in a specific region of a nebula would imply about that region\'s internal dust extinction, and explain in one sentence why this diagnostic is independent of the Stromgren-radius calculation in this unit\'s other problems.</p>', points=10) +
        problem(4, 'Electron density sensitivity',
                f'<p>Recompute the Orion Nebula\'s Stromgren radius assuming n_e were instead 1200 cm^-3 (double the real published value, with Q_H unchanged), and state the exact factor by which the Stromgren radius changes, connecting your answer to the R_s &prop; n_e^(-2/3) scaling derived in the lecture.</p>')
    )
    return pset_page(6, 'H II Region Diagnostics and the Stromgren Sphere', 'Extend this unit\'s ionization-balance and diagnostic tools to a second real H II region and sensitivity checks.',
                      problems, OPENSTAX)


def make_pset_06_solutions():
    rosette_pct = abs(ROSETTE_STROMGREN_RADIUS_PC - ROSETTE_NEBULA['observed_radius_pc']) / ROSETTE_NEBULA['observed_radius_pc'] * 100
    orion_pct = abs(ORION_STROMGREN_RADIUS_PC - ORION_NEBULA['observed_radius_pc']) / ORION_NEBULA['observed_radius_pc'] * 100
    q_h_needed = (4.0 / 3.0) * math.pi * ALPHA_B_CM3_S * ORION_NEBULA['n_e_cm3'] ** 2 * (ORION_NEBULA['observed_radius_pc'] * PC_M * 100.0) ** 3
    r_s_doubled_ne = stromgren_radius_pc(ORION_NEBULA['q_h_photons_s'], 1200.0)
    factor = r_s_doubled_ne / ORION_STROMGREN_RADIUS_PC
    s = (
        solution(1, 'The Rosette Nebula',
                  f'<p>R_s(Rosette)={ROSETTE_STROMGREN_RADIUS_PC:.2f} pc versus observed {ROSETTE_NEBULA["observed_radius_pc"]:.0f} pc, a percent difference of {rosette_pct:.1f}%, versus Orion\'s {orion_pct:.1f}% from the lab -- the Rosette\'s discrepancy is larger in this course\'s simplified single-density model, plausibly because large, evolved, lower-density H II regions like the Rosette have had more time to develop non-uniform density structure (e.g., a central cavity swept clear by stellar winds) that the idealized uniform-density Stromgren model does not capture.</p>',
                  [('Correct Rosette Stromgren-radius arithmetic', 6), ('Correct percent-difference comparison to Orion', 5), ('Reasoned, non-generic physical explanation', 4)]) +
        solution(2, 'Ionizing photon rate needed for a target radius',
                  f'<p>Solving R_s formula for Q_H at R_s={ORION_NEBULA["observed_radius_pc"]:.1f} pc gives Q_H={q_h_needed:.2e} photons/s, smaller than theta1 Ori C\'s real published Q_H ({ORION_NEBULA["q_h_photons_s"]:.1e} photons/s) -- consistent with Orion being at least partly density-bounded (some ionizing photons escape or are absorbed by dust rather than all going into ionizing gas within the observed radius) rather than purely ionization-bounded.</p>',
                  [('Correct algebraic inversion for Q_H', 7), ('Correct, reasoned ionization-vs-density-bounded interpretation', 8)]) +
        solution(3, 'Recombination-line ratio sanity check',
                  '<p>An observed Halpha/Hbeta ratio of 4.0, above the theoretical case B value of 2.86, implies significant internal dust extinction along that specific sightline through the nebula; this diagnostic depends only on the relative line fluxes at fixed atomic physics (Te), independent of the separate ionization-balance (Q_H, n_e) calculation used to derive the Stromgren radius.</p>',
                  [('Correct extinction interpretation', 5), ('Correct independence reasoning', 5)]) +
        solution(4, 'Electron density sensitivity',
                  f'<p>R_s(n_e=1200)={r_s_doubled_ne:.3f} pc, a factor of {factor:.3f} relative to the original ({ORION_STROMGREN_RADIUS_PC:.2f} pc) -- consistent with the R_s &prop; n_e^(-2/3) scaling, since doubling n_e should scale R_s by 2^(-2/3)={2**(-2.0/3.0):.3f}.</p>',
                  [('Correct Stromgren-radius recomputation', 7), ('Correct confirmation of the n_e^(-2/3) scaling factor', 8)])
    )
    return solutions_page(6, 'H II Region Diagnostics and the Stromgren Sphere', s)


def make_pset_06_assessment():
    return assessment_md(6, 'H II Region Diagnostics and the Stromgren Sphere',
                          ['Problem 1: verify correct Rosette Stromgren-radius arithmetic and a genuinely physical (not generic) explanation for the discrepancy comparison.',
                           'Problem 2: verify the algebraic inversion for Q_H is correct and the ionization/density-bounded interpretation follows logically from the comparison.',
                           'Problem 3: verify the student correctly identifies the Balmer decrement as an independent diagnostic from the Stromgren-radius calculation.',
                           'Problem 4: verify the n_e^(-2/3) scaling is confirmed numerically, not just asserted.'],
                          ['Treating a factor-of-2 or larger model-observation discrepancy as a computational error rather than an expected idealized-model limitation.',
                           'Confusing which diagnostic (Balmer decrement vs Stromgren radius) depends on which physical inputs.',
                           'Sign/direction errors in the n_e^(-2/3) scaling (reporting an increase instead of a decrease in R_s for increased n_e).'])


# ===========================================================================
# LAB/PSET 07 (Lectures 13-14): Shocks, cosmic rays, magnetic fields (capstone)
# ===========================================================================
def make_lab_07() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This capstone lab applies Lecture 13's shock-jump conditions and Lecture 14's cosmic-ray spectrum and magnetic-field scaling to the real Cassiopeia A supernova remnant, synthesizing this course's final unit into one real, multiwavelength object.</p></section>
<section><h2>Materials and Data</h2>
<p>Cassiopeia A: distance={CAS_A['distance_pc']:.0f} pc, age&asymp;{CAS_A['age_yr']:.0f} yr, shock velocity={CAS_A['shock_velocity_km_s']:,.0f} km/s (Vink 2004 and subsequent Chandra proper-motion studies, level 2). Cosmic-ray PDG spectrum parametrization (Lecture 14). Crutcher (2012) molecular-cloud B-n scaling. Crab Nebula B field (Hester 2008, level 2).</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute Cassiopeia A's strong-shock compression ratio and post-shock (ion) temperature from its real shock velocity.</li>
<li>State the expected observed X-ray (electron) temperature range given incomplete electron-ion equilibration at fast collisionless shocks (Ghavamian, Laming &amp; Rakowski 2007), and compute the ratio between your computed ion temperature and a representative observed electron temperature of kT=3 keV.</li>
<li>Using the PDG cosmic-ray flux parametrization, compute the flux at 100 GeV and at the knee energy (3x10^15 eV), and compute the ratio between them.</li>
<li>Using the Crutcher (2012) B-n relation, compute the predicted magnetic-field strength for gas at the OMC-1 core's density (from Unit 5) and compare it to the Galactic-average diffuse-ISM field strength.</li>
<li>Using the Crab Nebula's real published magnetic-field strength, compute the synchrotron critical frequency for an electron of Lorentz factor 1.0e6, and identify what part of the electromagnetic spectrum this frequency falls in.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Write a short (200-300 word) synthesis connecting Cassiopeia A's shock physics (Lecture 13) to the cosmic rays it is believed to accelerate and the magnetic field needed for that acceleration and for the resulting synchrotron emission (Lecture 14), explicitly naming which observed wavelength regime (X-ray, gamma-ray, radio) provides evidence for each piece of physics.</p></section>
<section><h2>Deliverables</h2><ul><li>All five computed quantities above with full derivations.</li><li>The 200-300 word multiwavelength synthesis paragraph.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct shock-jump and cosmic-ray-flux arithmetic.</li><li>Correct, non-overclaiming statement of the ion-vs-electron temperature discrepancy.</li><li>A genuinely multiwavelength, specific (not generic) synthesis paragraph.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Cassiopeia A, cosmic-ray spectrum, Crutcher B-n relation, and Crab Nebula parameters: standard published, level 2; see <code>materials/ASTR360/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR360/src/generate_astr360_content.py</code>.</li></ul></section>
"""
    return lab_page(7, 'Capstone: Shocks, Cosmic Rays, and Magnetic Fields in Cassiopeia A',
                     'Synthesize shock, cosmic-ray, and magnetic-field physics applied to one real supernova remnant.', sections)


def make_pset_07():
    problems = (
        problem(1, "Tycho's SNR shock",
                f'<p>Using Tycho\'s real published shock velocity ({TYCHO_SNR["shock_velocity_km_s"]:,.0f} km/s), compute its post-shock ion temperature, and compare it to Cassiopeia A\'s (computed in the lab), stating which remnant\'s shock produces the hotter predicted plasma and by what percentage.</p>') +
        problem(2, 'Cosmic-ray flux above the knee',
                f'<p>Using the steeper above-knee power-law index ({CR_INDEX_ABOVE_KNEE}), compute the cosmic-ray flux at 10x the knee energy (3x10^16 eV) relative to the flux exactly at the knee, and compare the steepness of this decline to the flux decline over the same energy ratio using the below-knee index ({CR_INDEX_BELOW_KNEE}) instead.</p>') +
        problem(3, 'Magnetic field in a less-dense cloud',
                f'<p>Using the Crutcher (2012) B-n relation, compute the predicted magnetic-field strength for gas at Barnard 68\'s density ({BARNARD68["n_h2_cm3"]:.1e} cm^-3, from Unit 5), and compare it to the OMC-1 core\'s predicted field (computed in the lab), stating which core is predicted to have the stronger field and why, given the two cores\' different densities.</p>') +
        problem(4, 'Synchrotron frequency for a lower-energy electron',
                f'<p>Using the Crab Nebula\'s real magnetic field, compute the synchrotron critical frequency for a lower-energy electron with Lorentz factor 1.0e4 (rather than the lab\'s 1.0e6), and identify what part of the electromagnetic spectrum this frequency falls in, connecting your answer to the nu_c &prop; gamma^2 scaling.</p>')
    )
    return pset_page(7, 'Shocks, Cosmic Rays, and Magnetic Fields', 'Extend this unit\'s capstone tools to a second real supernova remnant and additional density/energy regimes.',
                      problems, OPENSTAX)


def make_pset_07_solutions():
    tycho_pct = (CASA_POST_SHOCK_T - TYCHO_POST_SHOCK_T) / TYCHO_POST_SHOCK_T * 100
    flux_ratio_above = cosmic_ray_flux(CR_KNEE_GEV * 10) / cosmic_ray_flux(CR_KNEE_GEV) if False else (10.0) ** (-CR_INDEX_ABOVE_KNEE)
    flux_ratio_below = (10.0) ** (-CR_INDEX_BELOW_KNEE)
    b_barnard68 = crutcher_b_field_ug(BARNARD68['n_h2_cm3'])
    nu_c_low = synchrotron_critical_frequency_hz(CRAB_NEBULA['b_field_gauss'], 1.0e4)
    s = (
        solution(1, "Tycho's SNR shock",
                  f'<p>T2(Tycho)={TYCHO_POST_SHOCK_T:.2e} K versus T2(Cas A)={CASA_POST_SHOCK_T:.2e} K -- Cas A\'s shock produces the hotter predicted plasma, by {tycho_pct:.1f}%, directly reflecting its somewhat higher shock velocity through the T2 &prop; v_shock^2 scaling.</p>',
                  [('Correct post-shock temperature arithmetic for Tycho', 8), ('Correct percentage comparison', 7)]) +
        solution(2, 'Cosmic-ray flux above the knee',
                  f'<p>Above the knee (index {CR_INDEX_ABOVE_KNEE}): flux ratio over a factor-of-10 energy increase = 10^(-{CR_INDEX_ABOVE_KNEE})={flux_ratio_above:.2e}. Below the knee (index {CR_INDEX_BELOW_KNEE}): 10^(-{CR_INDEX_BELOW_KNEE})={flux_ratio_below:.2e} -- the above-knee decline is steeper (a smaller ratio), consistent with the steeper power-law index above the knee.</p>',
                  [('Correct power-law ratio arithmetic for both indices', 8), ('Correct comparison of steepness', 7)]) +
        solution(3, 'Magnetic field in a less-dense cloud',
                  f'<p>B(Barnard 68 density)={b_barnard68:.1f} microG versus B(OMC-1 core density)={MOLECULAR_CLOUD_ZEEMAN_B_UG:.0f} microG -- OMC-1\'s denser core is predicted to have the stronger field, consistent with the Crutcher (2012) B &prop; n^0.65 scaling above the critical density.</p>',
                  [('Correct B-field arithmetic for Barnard 68', 8), ('Correct comparison and scaling justification', 7)]) +
        solution(4, 'Synchrotron frequency for a lower-energy electron',
                  f'<p>nu_c(gamma=1.0e4)={nu_c_low:.3e} Hz, in the radio regime -- consistent with the nu_c &prop; gamma^2 scaling, since a factor-of-100 decrease in gamma (from 1.0e6 to 1.0e4) should decrease nu_c by a factor of 100^2=10,000, moving the emission from optical (lab\'s gamma=1.0e6 case) down to radio frequencies.</p>',
                  [('Correct synchrotron-frequency arithmetic', 8), ('Correct identification of the radio regime and the gamma^2 scaling', 7)])
    )
    return solutions_page(7, 'Shocks, Cosmic Rays, and Magnetic Fields', s)


def make_pset_07_assessment():
    return assessment_md(7, 'Shocks, Cosmic Rays, and Magnetic Fields',
                          ['Problem 1: verify correct post-shock temperature arithmetic and percentage-comparison direction.',
                           'Problem 2: verify correct power-law ratio arithmetic for both the above- and below-knee indices.',
                           'Problem 3: verify the Crutcher B-n scaling is applied correctly (denser core has stronger field, not weaker).',
                           'Problem 4: verify the gamma^2 scaling is used correctly (factor-of-100 gamma decrease gives factor-of-10,000 frequency decrease).'],
                          ['Sign errors in percentage-comparison direction (Cas A vs Tycho).',
                           'Confusing which cosmic-ray spectral index (above or below the knee) applies to which energy range.',
                           'Arithmetic errors in the gamma^2 synchrotron-frequency scaling (a common error is using gamma instead of gamma^2).'])


def write_labs_and_psets():
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    PSET_DIR.mkdir(parents=True, exist_ok=True)
    labs = [make_lab_01, make_lab_02, make_lab_03, make_lab_04, make_lab_05, make_lab_06, make_lab_07]
    for i, fn in enumerate(labs, start=1):
        (LAB_DIR / f'lab-{i:02d}.html').write_text(fn(), encoding='utf-8')
    psets = [
        (make_pset_01, make_pset_01_solutions, make_pset_01_assessment),
        (make_pset_02, make_pset_02_solutions, make_pset_02_assessment),
        (make_pset_03, make_pset_03_solutions, make_pset_03_assessment),
        (make_pset_04, make_pset_04_solutions, make_pset_04_assessment),
        (make_pset_05, make_pset_05_solutions, make_pset_05_assessment),
        (make_pset_06, make_pset_06_solutions, make_pset_06_assessment),
        (make_pset_07, make_pset_07_solutions, make_pset_07_assessment),
    ]
    for i, (p_fn, s_fn, a_fn) in enumerate(psets, start=1):
        (PSET_DIR / f'problem-set-{i:02d}.html').write_text(p_fn(), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-solutions.html').write_text(s_fn(), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-assessment.md').write_text(a_fn(), encoding='utf-8')


if __name__ == '__main__':
    write_labs_and_psets()
    print('Wrote 7 labs and 7 problem sets')
