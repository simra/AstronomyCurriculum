"""Lab and problem-set generator for ASTR370.

Depends on the shared constants and page()/CSS helpers in
generate_astr370_content.py so every number here traces back to the same
real solar/heliophysics datasets (solar structure constants, sunspot
field/pressure data, the AR12673 X9.3 flare/CME/storm case study, the
Carrington Event, Solar Cycle 24/25 sunspot numbers, Parker Solar Probe,
and the magnetopause/Dst framework) used in the paired lectures. Run with
the project interpreter:
    python materials/ASTR370/src/generate_astr370_content.py
    python materials/ASTR370/src/generate_astr370_labs_psets.py
"""
from __future__ import annotations

import math
from html import escape

from generate_astr370_content import (
    CSS, page, li, DATA_DIR,
    G_CONST, C_LIGHT, K_BOLTZMANN, MU0, AU_M, YEAR_S, DAY_S,
    M_SUN, R_SUN, L_SUN, M_H_KG, M_P_KG, EV_J,
    MU_PHOTOSPHERE, MU_CORONA,
    T_EFF_SUN_K, T_CORE_SUN_K, RHO_CORE_SUN_KGM3, RADIATIVE_ZONE_FRAC_R, CORE_FRAC_R,
    G_SURFACE_SUN, P_PHOTOSPHERE_PA, RHO_PHOTOSPHERE_KGM3,
    T_CHROMOSPHERE_TOP_K, T_CORONA_K, N_CORONA_BASE_M3,
    B_SUNSPOT_UMBRA_T,
    CYCLE25_START, CYCLE25_MIN_SMOOTHED_SSN, CYCLE25_MAX_SMOOTHED_SSN, CYCLE25_MAX_MONTHLY_SSN, CYCLE24_MAX_SMOOTHED_SSN,
    FLARE_DATE, FLARE_GOES_CLASS, FLARE_PEAK_FLUX_WM2, FLARE_CME_SPEED_KMS,
    FLARE_AR_AREA_M2, FLARE_AR_HEIGHT_M, STORM_DATE, STORM_DST_MIN_NT, STORM_TRANSIT_HOURS_OBSERVED,
    CARRINGTON_DST_MIN_NT, CARRINGTON_DST_MIN_NT_CONSERVATIVE, CARRINGTON_TRANSIT_HOURS,
    PSP_LAUNCH_DATE, PSP_PERIHELION_RSUN, PSP_PERIHELION_KM, PSP_RECORD_SPEED_KMS, PSP_RECORD_SPEED_KMH,
    SOLAR_WIND_SLOW_V_KMS, SOLAR_WIND_SLOW_N_CM3, SOLAR_WIND_FAST_V_KMS, SOLAR_WIND_FAST_N_CM3,
    SOLAR_WIND_STORM_V_KMS, SOLAR_WIND_STORM_N_CM3, B0_EARTH_T, R_EARTH_M,
    scale_height_m, sunspot_pressure_deficit_pa, flare_free_energy_j,
    parker_wind_residual, solve_parker_wind_speed, coronal_sound_speed_m_s, parker_critical_radius_m,
    travel_time_hours, magnetopause_standoff_re, dps_ring_current_energy_j,
    H_PHOTOSPHERE_M, H_CORONA_M, P_MAG_SUNSPOT_PA, SUNSPOT_PRESSURE_FRACTION, FLARE_FREE_ENERGY_J,
    CORONAL_SOUND_SPEED_KMS, PARKER_RC_M, PARKER_RC_RSUN, CME_TRAVEL_TIME_CONSTANT_SPEED_HR,
    CARRINGTON_IMPLIED_SPEED_KMS, MAGNETOPAUSE_QUIET_RE, MAGNETOPAUSE_STORM_RE,
    RING_CURRENT_ENERGY_SEPT2017_J, RING_CURRENT_ENERGY_CARRINGTON_J, RING_CURRENT_ENERGY_CARRINGTON_CONSERVATIVE_J,
    DPS_E0_J,
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
    return page(f'ASTR 370 Lab {n:02d}', body)


def pset_page(n: int, title: str, focus: str, problems_html: str, reading: str) -> str:
    body = f"""<header><div><h1>ASTR 370 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header>
<main><section><h2>Problems</h2>{problems_html}</section>
<section><h2>Due and Scope</h2><p>Submit a complete derivation with equations, units, labeled quantities, and a short narrative interpretation for each problem. Show every step; a correct final number without a visible derivation receives partial credit at most, and quoting a lecture number without adapting it to this problem's specific inputs receives no credit for that step.</p></section>
<section><h2>OpenStax Companion Reading</h2><p>{escape(reading)}</p></section>
<section><h2>References and Data Sources</h2><ul><li>Corresponding lecture slides and notes for this unit.</li><li>{OPENSTAX}</li><li>Course datasets under <code>materials/ASTR370/data/</code> where referenced above.</li></ul></section>
</main>"""
    return page(f'ASTR 370 Problem Set {n:02d}', body)


def solutions_page(n: int, title: str, solutions_html: str) -> str:
    body = f"<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header><main><section><h2>Worked Solutions</h2>{solutions_html}</section><section><h2>Grading Notes</h2><p>Award full marks for correct method, units, and a numeric result consistent with the arithmetic shown (allow reasonable rounding). Verify that the student re-derives the number for this problem's specific inputs rather than quoting a lecture example without adaptation. Watch specifically for unit-conversion errors (Gauss vs Tesla, nT vs T, km/s vs m/s, hours vs seconds), for comparative-magnitude statements given in the wrong direction, and for level-1/level-2/level-3 data-provenance conflation (e.g., presenting the order-of-magnitude flare free-energy estimate as a precise measurement, or presenting a Carrington-Dst estimate as a directly measured historical value) -- these are the most common sources of mistakes in this course.</p></section></main>"
    return page(f'ASTR 370 Problem Set {n:02d} Solutions', body)


def assessment_md(n: int, title: str, criteria: list, common_errors: list) -> str:
    crit = '\n'.join(f'- {c}' for c in criteria)
    err = '\n'.join(f'- {e}' for e in common_errors)
    return f"""# Assessment Instructions: Problem Set {n:02d} \u2014 {title}

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the referenced dataset(s) under `materials/ASTR370/data/`.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking number but no visible derivation steps should not. Because this is a 300-level quantitative solar physics and space weather course, full marks require a genuine derivation wherever the problem set asks for one, and a genuinely reasoned (not merely asserted) interpretation wherever the problem asks for scientific judgment (e.g., honestly characterizing an order-of-magnitude estimate's uncertainty, or a historical reconstruction's disclosed range).

## Problem-Level Criteria
{crit}

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
{err}
"""


# ===========================================================================
# LAB/PSET 01 (Lectures 1-2): Solar structure, hydrostatic scale height
# ===========================================================================
def make_lab_01() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This is a computational lab (no telescope required) that builds this unit's hydrostatic scale-height calculation for the photosphere and corona from Lectures 01-02's real solar structure parameters, and extends it to predict the coronal density falloff with height.</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Layer</th><th>T (K)</th><th>mu</th><th>Scale height H</th></tr></thead><tbody>
<tr><td>Photosphere</td><td>{T_EFF_SUN_K:.0f}</td><td>{MU_PHOTOSPHERE:.2f}</td><td>{H_PHOTOSPHERE_M/1.0e3:.0f} km</td></tr>
<tr><td>Corona</td><td>{T_CORONA_K:.1e}</td><td>{MU_CORONA:.2f}</td><td>{H_CORONA_M/1.0e3:,.0f} km</td></tr>
</tbody></table>
<p>T_eff and standard solar-model core parameters (T_core={T_CORE_SUN_K:.2e} K, rho_core={RHO_CORE_SUN_KGM3:.1e} kg/m^3) are standard published values, level 2 (see <code>../reference-log.md</code>). g_sun=GM_sun/R_sun^2={G_SURFACE_SUN:.1f} m/s^2 is computed directly from IAU nominal M_sun, R_sun.</p></section>
<section><h2>Procedure</h2><ol>
<li>Recompute g_sun=GM_sun/R_sun^2 from the given constants and confirm it matches the value above.</li>
<li>Recompute the photospheric scale height H=kT/(mu m_H g) and confirm it matches Lecture 01's stated value.</li>
<li>Recompute the coronal scale height at T_corona={T_CORONA_K:.1e} K, mu={MU_CORONA:.2f}, and compute the ratio H_corona/H_photosphere.</li>
<li>Using the coronal base density (n={N_CORONA_BASE_M3/1.0e6:.0e} cm^-3, standard published quiet-Sun value) and an isothermal exponential falloff with the coronal scale height, estimate the coronal density at a height of one solar radius above the photosphere, and compare it (order of magnitude) to the base density.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss why an isothermal, single-scale-height model is a simplification for the real corona (whose temperature and composition vary with height and position, and which is not in a strict static hydrostatic state at all per Lecture 08's Parker wind argument), and state explicitly that this lab's density estimate should be read as an order-of-magnitude illustration of the scale-height concept, not a precise coronal density model.</p></section>
<section><h2>Deliverables</h2><ul><li>Recomputed g_sun, H_photosphere, H_corona with full derivations.</li><li>The H_corona/H_photosphere ratio.</li><li>The estimated coronal density at one solar radius above the photosphere and a discussion of the model's limitations.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct g_sun arithmetic from G, M_sun, R_sun.</li><li>Correct scale-height arithmetic for both layers with correct units (km).</li><li>Honest, non-overclaiming discussion of the isothermal density-falloff model's limitations.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Solar structure parameters: IAU nominal values and standard solar model (Bahcall et al.), level 2; see <code>materials/ASTR370/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR370/src/generate_astr370_content.py</code>.</li></ul></section>
"""
    return lab_page(1, 'Solar Hydrostatic Structure: Scale Heights of the Photosphere and Corona',
                     "Compute and compare the Sun's photospheric and coronal scale heights and estimate the coronal density falloff.", sections)


def make_pset_01():
    problems = (
        problem(1, 'Scale height at the chromospheric temperature',
                f'<p>Compute the scale height using the chromospheric top temperature (T={T_CHROMOSPHERE_TOP_K:.0e} K) and a mean molecular weight intermediate between the photospheric and coronal values, mu=1.0 (partially ionized chromospheric gas, a reasonable order-of-magnitude choice). Compare your result to the lab\'s photospheric and coronal scale heights and state where it falls between the two.</p>') +
        problem(2, 'Surface gravity of a hypothetical star',
                f'<p>A hypothetical star has the Sun\'s mass but twice its radius. Compute this star\'s surface gravity and state whether its atmospheric scale height (at the same temperature and mu as the Sun\'s photosphere) would be larger or smaller than the Sun\'s own photospheric scale height, and by what factor.</p>') +
        problem(3, 'Core-to-surface temperature ratio',
                f'<p>Compute the ratio T_core/T_eff using the values in this unit\'s data table, and compute the same ratio using T_corona/T_eff instead. Compare the two ratios and explain, in one sentence, why the corona\'s temperature can exceed the photosphere\'s despite being much farther from the fusion-powered core.</p>', points=10) +
        problem(4, 'Radiative-convective boundary in physical units',
                f'<p>Convert the radiative-convective boundary\'s fractional radius (r={RADIATIVE_ZONE_FRAC_R:.2f} R_sun) into physical units (km), and compute what fraction of the Sun\'s total volume lies inside this boundary (volume scales as r^3 for a sphere).</p>')
    )
    return pset_page(1, 'Solar Structure and Scale Heights', "Extend this unit's hydrostatic scale-height tool to new temperatures and a hypothetical star, and connect the radiative-convective boundary to physical units.",
                      problems, OPENSTAX)


def make_pset_01_solutions():
    h_chromo = scale_height_m(T_CHROMOSPHERE_TOP_K, 1.0)
    g_hyp = G_CONST * M_SUN / (2 * R_SUN) ** 2
    h_hyp = scale_height_m(T_EFF_SUN_K, MU_PHOTOSPHERE, g_hyp)
    factor_hyp = h_hyp / H_PHOTOSPHERE_M
    ratio_core = T_CORE_SUN_K / T_EFF_SUN_K
    ratio_corona = T_CORONA_K / T_EFF_SUN_K
    rcz_km = RADIATIVE_ZONE_FRAC_R * R_SUN / 1.0e3
    vol_frac = RADIATIVE_ZONE_FRAC_R ** 3
    s = (
        solution(1, 'Scale height at the chromospheric temperature',
                  f'<p>H(chromosphere, T={T_CHROMOSPHERE_TOP_K:.0e} K, mu=1.0) = {h_chromo/1.0e3:,.0f} km -- intermediate between the photospheric ({H_PHOTOSPHERE_M/1.0e3:.0f} km) and coronal ({H_CORONA_M/1.0e3:,.0f} km) scale heights, consistent with the chromosphere\'s intermediate temperature and physical location.</p>',
                  [('Correct scale-height arithmetic', 8), ('Correct ordinal placement between photosphere and corona', 7)]) +
        solution(2, 'Surface gravity of a hypothetical star',
                  f'<p>g = GM/(2R)^2 = g_sun/4 = {g_hyp:.2f} m/s^2. Since H &prop; 1/g at fixed T and mu, this star\'s scale height is 4 times the Sun\'s own photospheric scale height ({h_hyp/1.0e3:.0f} km vs {H_PHOTOSPHERE_M/1.0e3:.0f} km) -- larger, because its weaker surface gravity (same mass, larger radius) is less effective at compressing its atmosphere.</p>',
                  [('Correct surface-gravity arithmetic', 7), ('Correct factor-of-4 scale-height conclusion', 8)]) +
        solution(3, 'Core-to-surface temperature ratio',
                  f'<p>T_core/T_eff = {ratio_core:,.0f}. T_corona/T_eff = {ratio_corona:.1f}. The core ratio is far larger, as expected (fusion happens only in the core); the much smaller corona/photosphere ratio nonetheless represents a real, physically surprising temperature *increase* with distance from the surface, which the core-driven radiative cooling trend alone cannot explain -- requiring the non-radiative (magnetic) heating mechanism of Lecture 02.</p>',
                  [('Correct ratio arithmetic for both', 5), ('Correct physical explanation connecting to Lecture 02', 5)]) +
        solution(4, 'Radiative-convective boundary in physical units',
                  f'<p>r_cz = {RADIATIVE_ZONE_FRAC_R:.2f} x {R_SUN/1.0e3:,.0f} km = {rcz_km:,.0f} km. Volume fraction inside this radius = ({RADIATIVE_ZONE_FRAC_R:.2f})^3 = {vol_frac:.3f}, i.e., about {vol_frac*100:.0f}% of the Sun\'s total volume lies inside the radiative-convective boundary, with the remaining ~{(1-vol_frac)*100:.0f}% forming the (much larger in volume, but much lower in density) convective envelope.</p>',
                  [('Correct unit conversion to km', 5), ('Correct volume-fraction (cube of radius fraction) arithmetic', 10)])
    )
    return solutions_page(1, 'Solar Structure and Scale Heights', s)


def make_pset_01_assessment():
    return assessment_md(1, 'Solar Structure and Scale Heights',
                          ['Problem 1: verify correct scale-height arithmetic and correct ordinal comparison to the lab\'s two computed values.',
                           'Problem 2: verify the inverse-gravity scaling of scale height is applied correctly (larger radius -> smaller g -> larger H).',
                           'Problem 3: verify both ratios are computed correctly and the physical explanation invokes non-radiative heating, not merely restating the temperature values.',
                           'Problem 4: verify the volume fraction uses the cube of the radius fraction, not the radius fraction itself.'],
                          ['Using the radius fraction directly as a volume fraction (forgetting the cube).',
                           'Reversing the direction of the gravity-scale height relationship (claiming larger radius gives smaller scale height).',
                           'Treating the core/surface temperature ratio and the corona/surface temperature ratio as evidence for the same physical mechanism.'])


# ===========================================================================
# LAB/PSET 02 (Lectures 3-4): Solar cycle sunspot data, sunspot pressure balance
# ===========================================================================
def make_lab_02() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab tabulates and compares real SILSO-sourced sunspot-number data across Solar Cycles 24 and 25 (Lecture 03), then computes the thin flux-tube pressure-balance fraction for a range of real sunspot field strengths (Lecture 04).</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Cycle</th><th>Metric</th><th>Value</th><th>Date</th></tr></thead><tbody>
<tr><td>Solar Cycle 24</td><td>Smoothed max SSN</td><td>{CYCLE24_MAX_SMOOTHED_SSN:.1f}</td><td>April 2014</td></tr>
<tr><td>Solar Cycle 25</td><td>Smoothed min SSN</td><td>{CYCLE25_MIN_SMOOTHED_SSN:.1f}</td><td>{CYCLE25_START}</td></tr>
<tr><td>Solar Cycle 25</td><td>Smoothed max SSN</td><td>{CYCLE25_MAX_SMOOTHED_SSN:.1f}</td><td>October 2024</td></tr>
<tr><td>Solar Cycle 25</td><td>Not-smoothed max SSN</td><td>{CYCLE25_MAX_MONTHLY_SSN:.0f}</td><td>August 2024</td></tr>
</tbody></table>
<p>Cycle 25 figures live-verified this session (SILSO/WDC-SILSO via Wikipedia's "Solar cycle 25" article); Cycle 24 figure is a standard published value not independently re-verified this session (level 2; see <code>../reference-log.md</code>). Sunspot umbral field: B={B_SUNSPOT_UMBRA_T*1.0e4:.0f} G (Solanki 2003, level 2). Photospheric gas pressure: P_phot={P_PHOTOSPHERE_PA:,.0f} Pa (level 2).</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute the ratio of Solar Cycle 25's smoothed maximum SSN to Solar Cycle 24's, and state whether Cycle 25 is stronger or weaker.</li>
<li>Compute the ratio of Cycle 25's not-smoothed to smoothed maximum SSN, and discuss what physical effect (short-term variability vs the underlying multi-month trend) this ratio reflects.</li>
<li>Compute the sunspot magnetic pressure P_mag=B^2/(2 mu0) for the given real field strength and confirm it matches Lecture 04's stated value.</li>
<li>Compute P_mag for three additional real, smaller sunspot field strengths (1500 G, 2000 G, 2500 G) and tabulate the pressure-balance fraction P_mag/P_phot for all four field strengths, identifying the threshold field strength at which the fraction first exceeds 1.0.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss why the sunspot-number ratio comparison (Cycle 25 vs Cycle 24) should not be used to conclude anything about future Cycle 26, given the disclosed unpredictability of solar-cycle amplitude discussed in Lecture 03.</p></section>
<section><h2>Deliverables</h2><ul><li>The Cycle 24/25 ratio computations and interpretation.</li><li>The four-field-strength pressure-balance table with the threshold field strength identified.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct ratio arithmetic for both cycle comparisons.</li><li>Correct P_mag arithmetic (B in Tesla, not Gauss, inside the formula) for all four field strengths.</li><li>Correctly identified threshold field strength.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Solar Cycle 25 sunspot numbers: live-verified this session (SILSO/WDC-SILSO); Solar Cycle 24 and sunspot field strength: standard published, level 2; see <code>materials/ASTR370/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR370/src/generate_astr370_content.py</code>.</li></ul></section>
"""
    return lab_page(2, 'The Solar Cycle and Sunspot Pressure Balance',
                     "Compare real Solar Cycle 24/25 sunspot-number data and compute the thin flux-tube pressure-balance fraction for several real sunspot field strengths.", sections)


def make_pset_02():
    problems = (
        problem(1, 'A weaker hypothetical cycle',
                f'<p>Suppose a future solar cycle reaches only 60% of Solar Cycle 24\'s smoothed maximum SSN. Compute this hypothetical cycle\'s smoothed maximum SSN, and state whether it would be weaker or stronger than the weakest well-documented historical cycles (which have reached smoothed maxima below 50).</p>') +
        problem(2, 'Pressure balance at a very strong field',
                f'<p>Compute the sunspot magnetic pressure for an unusually strong umbral field of 3500 G (a real, though rare, published maximum sunspot field strength), and compute the pressure-balance fraction relative to the photospheric gas pressure used in the lab. State whether the simple pressure-balance approximation would require the internal gas pressure to be reduced by more than, or less than, a factor of 10 relative to the ambient photosphere at this field strength.</p>') +
        problem(3, 'Sunspot number ratio sensitivity',
                f'<p>Recompute the Cycle 25/Cycle 24 smoothed-maximum ratio if Cycle 25\'s true smoothed maximum is later revised upward by 10% (a plausible outcome, since SILSO smoothed values are only finalized after a cycle\'s maximum has clearly passed). Compute the revised ratio and compare it to the value computed in the lab.</p>', points=10) +
        problem(4, 'Threshold field strength derivation',
                f'<p>Algebraically solve P_mag=B^2/(2 mu0)=P_phot for B, and evaluate the resulting threshold field strength in both Tesla and Gauss using the photospheric pressure from this unit\'s data. Compare your algebraic threshold to the numerical threshold you identified in the lab\'s four-field-strength table.</p>')
    )
    return pset_page(2, 'Solar Cycle Data and Sunspot Pressure Balance', "Extend this unit's real sunspot-number comparison and pressure-balance tool to new hypothetical and threshold cases.",
                      problems, OPENSTAX)


def make_pset_02_solutions():
    weaker_cycle = 0.6 * CYCLE24_MAX_SMOOTHED_SSN
    p_mag_3500 = sunspot_pressure_deficit_pa(3500 / 1.0e4)
    frac_3500 = p_mag_3500 / P_PHOTOSPHERE_PA
    revised_ratio = (CYCLE25_MAX_SMOOTHED_SSN * 1.10) / CYCLE24_MAX_SMOOTHED_SSN
    original_ratio = CYCLE25_MAX_SMOOTHED_SSN / CYCLE24_MAX_SMOOTHED_SSN
    b_threshold_t = math.sqrt(2 * MU0 * P_PHOTOSPHERE_PA)
    s = (
        solution(1, 'A weaker hypothetical cycle',
                  f'<p>0.60 x {CYCLE24_MAX_SMOOTHED_SSN:.1f} = {weaker_cycle:.1f}. This hypothetical smoothed maximum would still be above the ~50 threshold used here for "weakest historical cycles," so it would not be exceptionally weak by historical standards, though it would be substantially weaker than both Cycle 24 and Cycle 25.</p>',
                  [('Correct arithmetic', 8), ('Correct comparative statement', 7)]) +
        solution(2, 'Pressure balance at a very strong field',
                  f'<p>P_mag(3500 G) = {p_mag_3500:,.0f} Pa, giving a pressure-balance fraction of {frac_3500:.2f} relative to P_phot={P_PHOTOSPHERE_PA:,.0f} Pa -- more than a factor of 10 (specifically {frac_3500:.1f}x), meaning the simple pressure-balance approximation would require reducing internal gas pressure by more than a factor of 10 relative to the ambient photosphere at this strong field.</p>',
                  [('Correct P_mag arithmetic at 3500 G', 8), ('Correct greater-than-10x conclusion', 7)]) +
        solution(3, 'Sunspot number ratio sensitivity',
                  f'<p>Revised ratio = (1.10 x {CYCLE25_MAX_SMOOTHED_SSN:.1f})/{CYCLE24_MAX_SMOOTHED_SSN:.1f} = {revised_ratio:.2f}, compared to the lab\'s original ratio of {original_ratio:.2f} -- a modest but non-negligible increase, illustrating why sunspot-number ratios computed soon after a cycle\'s maximum should be treated as provisional until SILSO\'s official smoothing is finalized.</p>',
                  [('Correct revised-ratio arithmetic', 5), ('Correct comparison to the original ratio', 5)]) +
        solution(4, 'Threshold field strength derivation',
                  f'<p>Solving B^2/(2 mu0)=P_phot for B gives B=sqrt(2 mu0 P_phot) = {b_threshold_t:.4f} T = {b_threshold_t*1.0e4:.0f} G. This lies between the lab\'s 2000 G and 2500 G table entries, consistent with the lab\'s numerically identified threshold falling in that same range.</p>',
                  [('Correct algebraic rearrangement', 7), ('Correct numeric threshold and unit conversion to Gauss', 8)])
    )
    return solutions_page(2, 'Solar Cycle Data and Sunspot Pressure Balance', s)


def make_pset_02_assessment():
    return assessment_md(2, 'Solar Cycle Data and Sunspot Pressure Balance',
                          ['Problem 1: verify correct percentage arithmetic and a reasoned, not merely numeric, comparative statement.',
                           'Problem 2: verify B is converted from Gauss to Tesla before use in the P_mag formula.',
                           'Problem 3: verify the revised ratio correctly applies the 10% increase only to Cycle 25\'s value.',
                           'Problem 4: verify the algebraic rearrangement is shown, not just the final numeric threshold.'],
                          ['Forgetting to convert Gauss to Tesla (a factor-of-10^4 error) before computing P_mag.',
                           'Applying the 10% revision to both cycles instead of only Cycle 25.',
                           'Treating a sunspot-number ratio between two specific past cycles as predictive of a third, future cycle.'])


# ===========================================================================
# LAB/PSET 03 (Lectures 5-6): Flare free energy, AR12673 case study
# ===========================================================================
def make_lab_03() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes the order-of-magnitude free-energy estimate for a range of assumed active-region field strengths and volumes (Lecture 05), then reconstructs the real published timeline of the {FLARE_DATE} X9.3 flare case study (Lecture 06).</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Quantity</th><th>Value</th><th>Provenance</th></tr></thead><tbody>
<tr><td>GOES class</td><td>{FLARE_GOES_CLASS}</td><td>standard published, level 2</td></tr>
<tr><td>Peak flux</td><td>{FLARE_PEAK_FLUX_WM2:.1e} W/m^2</td><td>standard published, level 2</td></tr>
<tr><td>CME LASCO speed</td><td>{FLARE_CME_SPEED_KMS:.0f} km/s</td><td>standard published (CDAW catalog), level 2</td></tr>
<tr><td>Storm Dst minimum</td><td>{STORM_DST_MIN_NT:.0f} nT</td><td>standard published (Kyoto WDC/NOAA), level 2</td></tr>
<tr><td>Observed CME transit time</td><td>~{STORM_TRANSIT_HOURS_OBSERVED:.0f} hours</td><td>standard published range, level 2</td></tr>
</tbody></table>
<p>Representative AR volume (area={FLARE_AR_AREA_M2:.1e} m^2, height scale={FLARE_AR_HEIGHT_M:.1e} m) is an order-of-magnitude, level 3 estimate, explicitly disclosed (see <code>../reference-log.md</code>).</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute the free-energy estimate E_free=(B^2/2 mu0)V for the given sunspot field strength and AR volume, and confirm it matches Lecture 05's stated value.</li>
<li>Recompute E_free for two additional AR volume estimates (half and double the given volume), holding B fixed, and tabulate all three.</li>
<li>Compute the light travel time from the Sun to Earth (1 AU/c) in minutes, and compare it to the real observed CME transit time in hours, expressing the ratio between the two timescales.</li>
<li>Compute the GOES-class-to-flux ratio between the X9.3 flare and a hypothetical M5.0 flare, and state how many M5.0-equivalent peak fluxes would be needed to match the X9.3 flare's peak flux.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss why doubling the assumed AR volume exactly doubles the free-energy estimate (a direct consequence of the linear volume dependence in E_free=(B^2/2 mu0)V), and why this makes the volume assumption the single largest source of uncertainty in this order-of-magnitude estimate.</p></section>
<section><h2>Deliverables</h2><ul><li>The three-volume free-energy table.</li><li>The light-travel-time vs CME-transit-time ratio.</li><li>The X9.3-to-M5.0 flux ratio.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct free-energy arithmetic for all three volumes.</li><li>Correct light-travel-time computation and ratio.</li><li>Correct GOES-class flux ratio arithmetic.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>AR12673/X9.3 flare and storm values: standard published, level 2; AR volume: order-of-magnitude, level 3; see <code>materials/ASTR370/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR370/src/generate_astr370_content.py</code>.</li></ul></section>
"""
    return lab_page(3, 'Flare Free Energy and the 6 September 2017 Case Study',
                     "Compute the order-of-magnitude flare free-energy estimate across assumed volumes and reconstruct the real AR12673 flare/CME/storm timeline.", sections)


def make_pset_03():
    problems = (
        problem(1, 'Free energy at a different field strength',
                f'<p>Recompute the free-energy estimate using a weaker active-region field of 2000 G (rather than this unit\'s {B_SUNSPOT_UMBRA_T*1.0e4:.0f} G) at the same representative volume used in the lab. Compute the factor by which the free energy changes and confirm it matches the B^2 scaling in E_free=(B^2/2 mu0)V.</p>') +
        problem(2, 'GOES class arithmetic',
                f'<p>NOAA classifies a flare as X9.3 if its peak 1-8 Angstrom flux is 9.3 x 10^-4 W/m^2. Compute the peak flux corresponding to an X1.8 flare and a C4.5 flare, and compute the ratio of the X1.8 flare\'s flux to the C4.5 flare\'s flux.</p>') +
        problem(3, 'Timescale ratio sensitivity',
                f'<p>If the real CME transit time had instead been exactly 24 hours (rather than this unit\'s ~{STORM_TRANSIT_HOURS_OBSERVED:.0f} hours), recompute the ratio between this transit time and the light travel time (1 AU/c, computed in the lab), and state whether the flare-radiation-to-CME-arrival lag would be longer or shorter than in the real event.</p>', points=10) +
        problem(4, 'Naive vs observed CME speed implied by transit time',
                f'<p>Using the real observed transit time (~{STORM_TRANSIT_HOURS_OBSERVED:.0f} hours) and the 1 AU Sun-Earth distance, compute the implied average CME speed over its full transit, and compare this "effective" speed to the CME\'s initial LASCO-measured speed ({FLARE_CME_SPEED_KMS:.0f} km/s). State what this comparison implies about the CME\'s average deceleration during transit.</p>')
    )
    return pset_page(3, 'Flare Energetics and CME/Flare Timescales', "Extend this unit's free-energy and timescale tools to new field strengths, GOES classes, and transit-time scenarios.",
                      problems, OPENSTAX)


def make_pset_03_solutions():
    e_free_2000g = flare_free_energy_j(2000 / 1.0e4, FLARE_AR_AREA_M2 * FLARE_AR_HEIGHT_M)
    b_ratio_sq = (2000 / (B_SUNSPOT_UMBRA_T * 1.0e4)) ** 2
    flux_x18 = 1.8e-4
    flux_c45 = 4.5e-6
    ratio_x_c = flux_x18 / flux_c45
    light_travel_min = AU_M / C_LIGHT / 60
    ratio_24h = 24 * 60 / light_travel_min
    ratio_real = STORM_TRANSIT_HOURS_OBSERVED * 60 / light_travel_min
    v_effective = AU_M / (STORM_TRANSIT_HOURS_OBSERVED * 3600) / 1.0e3
    s = (
        solution(1, 'Free energy at a different field strength',
                  f'<p>E_free(2000 G) = {e_free_2000g:.2e} J, a factor of (2000/{B_SUNSPOT_UMBRA_T*1.0e4:.0f})^2 = {b_ratio_sq:.2f} relative to the lab\'s value ({FLARE_FREE_ENERGY_J:.2e} J) -- confirming the B^2 scaling, since free energy depends on the square of the field strength at fixed volume.</p>',
                  [('Correct free-energy recomputation', 8), ('Correct confirmation of B^2 scaling', 7)]) +
        solution(2, 'GOES class arithmetic',
                  f'<p>X1.8 flux = 1.8e-4 W/m^2. C4.5 flux = 4.5e-6 W/m^2. Ratio = {ratio_x_c:.0f} -- an X1.8 flare has {ratio_x_c:.0f} times the peak flux of a C4.5 flare, directly illustrating the classification scheme\'s logarithmic (decade-per-letter) structure.</p>',
                  [('Correct flux values for both classes', 8), ('Correct ratio computed', 7)]) +
        solution(3, 'Timescale ratio sensitivity',
                  f'<p>Light travel time = {light_travel_min:.2f} minutes. At a hypothetical 24-hour transit, ratio = {ratio_24h:.0f}; at the real ~{STORM_TRANSIT_HOURS_OBSERVED:.0f}-hour transit, ratio = {ratio_real:.0f} -- the real event\'s lag between radiation arrival and CME arrival is longer than the hypothetical 24-hour case, since {STORM_TRANSIT_HOURS_OBSERVED:.0f} hours exceeds 24 hours.</p>',
                  [('Correct light-travel-time computation', 5), ('Correct ratio computation for both cases and correct comparative direction', 5)]) +
        solution(4, 'Naive vs observed CME speed implied by transit time',
                  f'<p>Effective average speed = 1 AU / ({STORM_TRANSIT_HOURS_OBSERVED:.0f} hr) = {v_effective:.0f} km/s, substantially lower than the initial LASCO speed ({FLARE_CME_SPEED_KMS:.0f} km/s) -- implying substantial average deceleration during transit, consistent with Lecture 07\'s drag-based propagation physics (the CME decelerating toward the ambient, much slower solar wind speed).</p>',
                  [('Correct effective-speed arithmetic', 8), ('Correct deceleration interpretation', 7)])
    )
    return solutions_page(3, 'Flare Energetics and CME/Flare Timescales', s)


def make_pset_03_assessment():
    return assessment_md(3, 'Flare Energetics and CME/Flare Timescales',
                          ['Problem 1: verify the B^2 scaling factor is derived algebraically, not just asserted.',
                           'Problem 2: verify both GOES-class flux values are correctly converted from the class notation.',
                           'Problem 3: verify both ratios are computed and correctly compared in direction.',
                           'Problem 4: verify the effective-speed comparison correctly concludes net deceleration, not acceleration.'],
                          ['Forgetting to square the field-strength ratio when computing the free-energy scaling factor.',
                           'Misreading GOES class notation (e.g., treating X1.8 as 1.8e-5 rather than 1.8e-4 W/m^2).',
                           'Concluding the CME accelerated rather than decelerated during transit from the effective-speed comparison.'])


# ===========================================================================
# LAB/PSET 04 (Lectures 7-8): CME kinematics, Parker wind numerical solution
# ===========================================================================
def make_lab_04() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes both the naive constant-speed and a simple drag-based transit-time estimate for the real 6 September 2017 CME (Lecture 07), then reproduces Lecture 08's numerical transonic Parker-wind solve at several radii.</p></section>
<section><h2>Materials and Data</h2>
<p>CME LASCO speed: {FLARE_CME_SPEED_KMS:.0f} km/s (level 2). Ambient slow solar wind speed: {SOLAR_WIND_SLOW_V_KMS:.0f} km/s (level 2, OMNI climatology). Coronal temperature: {T_CORONA_K:.1e} K, mu={MU_CORONA:.2f}. Parker critical radius: r_c={PARKER_RC_RSUN:.2f} R_sun (computed in Lecture 08).</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute the naive constant-speed travel time (1 AU/v_CME) and confirm it matches Lecture 07's stated value.</li>
<li>Using the drag-based deceleration functional form from Lecture 07's figure (exponential relaxation toward the ambient wind speed with a 15-hour time constant), numerically integrate or evaluate the CME's distance vs time and estimate the arrival time at 1 AU; compare it to the real observed ~{STORM_TRANSIT_HOURS_OBSERVED:.0f}-hour transit time.</li>
<li>Numerically solve the Parker transonic wind equation (bisection on the physical branch, as in Lecture 08) for u=v/c_s at r/r_c=0.5, 1.0, 2.0, and {AU_M/PARKER_RC_M:.0f} (1 AU), and tabulate v in km/s at each radius.</li>
<li>Confirm that u=1.0 (v=c_s) exactly at r/r_c=1.0, the defining property of the critical point.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss why the drag-based model's specific functional form (and its 15-hour time constant) is an illustrative, level-3 choice calibrated only to roughly reproduce the real observed transit time, not a first-principles solution of the full drag-force differential equation, which would require knowing the ambient solar wind's density profile in detail.</p></section>
<section><h2>Deliverables</h2><ul><li>The naive and drag-based transit-time estimates compared to the real observed value.</li><li>The four-radius Parker-wind speed table with the critical-point check.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct naive travel-time arithmetic.</li><li>Correct numerical root-finding for the Parker wind equation at all four radii.</li><li>Correctly confirmed critical-point property (u=1 at r=r_c).</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>CME speed and solar wind climatology: standard published, level 2; see <code>materials/ASTR370/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR370/src/generate_astr370_content.py</code>.</li></ul></section>
"""
    return lab_page(4, "CME Transit Time and the Parker Wind's Numerical Solution",
                     "Compare naive and drag-based CME transit-time estimates to the real observed value, and numerically solve the Parker transonic wind equation at several radii.", sections)


def make_pset_04():
    problems = (
        problem(1, 'A faster CME\'s naive transit time',
                f'<p>Compute the naive constant-speed transit time for a hypothetical CME twice as fast as the real 6 September 2017 event (2 x {FLARE_CME_SPEED_KMS:.0f} = {2*FLARE_CME_SPEED_KMS:.0f} km/s), and compare it to the real event\'s naive transit time computed in the lab.</p>') +
        problem(2, 'Parker wind speed at Mercury\'s orbit',
                f'<p>Mercury orbits at approximately 0.39 AU. Numerically solve the Parker transonic wind equation for u at r=0.39 AU (convert to r/r_c using the critical radius from this unit\'s data) and report the wind speed in km/s. State whether it is faster or slower than the wind speed at 1 AU computed in the lab, and explain why using the equation\'s r-dependence.</p>') +
        problem(3, 'Sensitivity to coronal temperature',
                f'<p>Recompute the coronal sound speed and critical radius for a somewhat cooler corona (T=1.0e6 K rather than this unit\'s {T_CORONA_K:.1e} K), and state whether the critical radius moves closer to or farther from the Sun as a result.</p>') +
        problem(4, 'Drag-model sensitivity',
                f'<p>Using the drag-based deceleration functional form from the lab but with a time constant of 25 hours instead of 15 hours, describe qualitatively (no need to fully re-derive the arrival time numerically) whether this longer time constant would predict a faster or slower approach to the ambient wind speed, and hence a shorter or longer predicted transit time.</p>', points=10)
    )
    return pset_page(4, "CME Transit and the Parker Wind", "Extend this unit's transit-time and Parker-wind tools to new speeds, radii, and coronal temperatures.",
                      problems, OPENSTAX)


def make_pset_04_solutions():
    t_2x = travel_time_hours(AU_M, 2 * FLARE_CME_SPEED_KMS)
    t_1x = CME_TRAVEL_TIME_CONSTANT_SPEED_HR
    r_mercury_m = 0.39 * AU_M
    u_mercury = solve_parker_wind_speed(r_mercury_m / PARKER_RC_M)
    v_mercury = u_mercury * CORONAL_SOUND_SPEED_KMS
    v_1au = solve_parker_wind_speed(AU_M / PARKER_RC_M) * CORONAL_SOUND_SPEED_KMS
    cs_cooler = coronal_sound_speed_m_s(1.0e6, MU_CORONA) / 1.0e3
    rc_cooler_rsun = parker_critical_radius_m(1.0e6, MU_CORONA) / R_SUN
    s = (
        solution(1, "A faster CME's naive transit time",
                  f'<p>t(2x speed) = {t_2x:.2f} hr, exactly half the real event\'s naive transit time ({t_1x:.1f} hr) -- confirming t &prop; 1/v at fixed distance.</p>',
                  [('Correct arithmetic', 8), ('Correct factor-of-2 confirmation', 7)]) +
        solution(2, "Parker wind speed at Mercury's orbit",
                  f'<p>r/r_c(Mercury)={r_mercury_m/PARKER_RC_M:.2f}. Solving gives u={u_mercury:.3f}, v={v_mercury:.0f} km/s -- slower than the 1 AU speed ({v_1au:.0f} km/s), since the wind continues to accelerate outward beyond the critical point (r/r_c(Mercury) is smaller than r/r_c(1 AU), and the transonic solution\'s speed increases monotonically with r beyond r_c).</p>',
                  [('Correct r/r_c computation for Mercury', 5), ('Correct numerical solve and speed', 5), ('Correct slower-at-Mercury conclusion with reasoning', 5)]) +
        solution(3, 'Sensitivity to coronal temperature',
                  f'<p>At T=1.0e6 K, c_s={cs_cooler:.0f} km/s (lower than the {CORONAL_SOUND_SPEED_KMS:.0f} km/s used in the lab), and r_c={rc_cooler_rsun:.2f} R_sun -- since r_c &prop; 1/c_s^2, a cooler corona has a *larger* critical radius, moving the transonic point farther from the Sun.</p>',
                  [('Correct cooler sound speed', 7), ('Correct larger-critical-radius conclusion', 8)]) +
        solution(4, 'Drag-model sensitivity',
                  '<p>A longer time constant (25 hr vs 15 hr) means the CME approaches the ambient wind speed more slowly, so it remains closer to its initial fast speed for longer -- predicting a *shorter* transit time than the 15-hour-time-constant model, not a longer one, since the CME spends more of its transit moving faster.</p>',
                  [('Correct qualitative direction (slower relaxation -> shorter transit)', 10)])
    )
    return solutions_page(4, 'CME Transit and the Parker Wind', s)


def make_pset_04_assessment():
    return assessment_md(4, 'CME Transit and the Parker Wind',
                          ['Problem 1: verify the inverse speed-time scaling is confirmed numerically.',
                           'Problem 2: verify correct r/r_c conversion for Mercury\'s orbit and correct numerical root-finding.',
                           'Problem 3: verify the direction of the critical-radius temperature dependence (cooler -> larger r_c) is derived from the 1/c_s^2 scaling, not guessed.',
                           'Problem 4: verify the qualitative direction of the time-constant sensitivity is correct (longer time constant -> shorter transit time).'],
                          ['Sign errors in the r_c vs temperature scaling (claiming a hotter corona gives a larger critical radius).',
                           'Choosing the wrong root of the Parker wind transcendental equation (subsonic instead of transonic branch) for r>r_c.',
                           'Reversing the direction of the time-constant sensitivity in Problem 4.'])


# ===========================================================================
# LAB/PSET 05 (Lectures 9-10): Remote sensing, PSP in-situ speed
# ===========================================================================
def make_lab_05() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab works through a simplified schematic helioseismic-frequency reasoning exercise and a coronagraph field-of-view geometry calculation (Lecture 09), then uses Parker Solar Probe's real perihelion distance with Lecture 08's numerically solved wind-speed curve to predict the in-situ solar wind speed near its closest approach (Lecture 10).</p></section>
<section><h2>Materials and Data</h2>
<p>Parker Solar Probe: launched {PSP_LAUNCH_DATE}, perihelion {PSP_PERIHELION_RSUN:.2f} R_sun ({PSP_PERIHELION_KM:.1e} km), record heliocentric speed {PSP_RECORD_SPEED_KMS:.0f} km/s (all live-verified this session). Parker critical radius (Lecture 08): r_c={PARKER_RC_RSUN:.2f} R_sun.</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute PSP's perihelion distance in units of the Parker critical radius (r_perihelion/r_c), and state whether PSP samples plasma inside or outside the critical point.</li>
<li>Using Lecture 08's numerical transonic-solution solver, compute the predicted Parker-wind speed at PSP's exact perihelion distance.</li>
<li>Compare this predicted speed to PSP's own record heliocentric *orbital* speed ({PSP_RECORD_SPEED_KMS:.0f} km/s) and explain explicitly why these are two different physical quantities that should not be numerically compared as if they were measuring the same thing.</li>
<li>Compute the coronagraph occulting-disk geometry: if an occulting disk must block a field of view out to 1.5 solar radii to fully hide the photospheric disk and its immediate surroundings, and the coronagraph's total field of view extends to 6 solar radii, compute what fraction of the coronagraph's total field of view is unusable due to the occulting disk.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss why the simplified isothermal Parker wind model's speed prediction at PSP's perihelion is only an order-of-magnitude comparison point, not a precise prediction to be checked against PSP's actual in-situ SWEAP measurements, given the real corona's non-isothermal, magnetically structured nature (Lecture 08's disclosed limitation).</p></section>
<section><h2>Deliverables</h2><ul><li>PSP's r/r_c ratio and predicted Parker-wind speed at perihelion.</li><li>The explicit orbital-speed-vs-wind-speed distinction discussion.</li><li>The coronagraph field-of-view fraction calculation.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct r/r_c ratio and correct numerical Parker-wind solve at that ratio.</li><li>Explicit, correct statement that orbital speed and wind speed are different physical quantities.</li><li>Correct field-of-view fraction arithmetic.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Parker Solar Probe mission facts: live-verified this session; see <code>materials/ASTR370/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR370/src/generate_astr370_content.py</code>.</li></ul></section>
"""
    return lab_page(5, 'Remote Sensing Geometry and Parker Solar Probe In-Situ Prediction',
                     "Work through coronagraph field-of-view geometry and predict the Parker-wind speed at Parker Solar Probe's real perihelion.", sections)


def make_pset_05():
    problems = (
        problem(1, "PSP's speed at a different perihelion",
                f'<p>If a future Parker Solar Probe extended mission achieved a perihelion of 6 R_sun (closer than the real {PSP_PERIHELION_RSUN:.2f} R_sun), compute the predicted Parker-wind speed at that distance and compare it to the predicted speed at the real perihelion computed in the lab.</p>') +
        problem(2, 'Helioseismic mode counting',
                '<p>If the Sun oscillates in approximately 10 million individually distinguishable p-mode oscillation patterns (a standard order-of-magnitude figure), and a single mode\'s frequency can be measured to a precision of about 1 part in 10^5, discuss (without needing new derivations) why this enormous number of precisely measured modes provides much stronger constraints on interior structure than the single core-temperature estimate used in Lecture 01.</p>', points=10) +
        problem(3, 'Coronagraph field-of-view sensitivity',
                f'<p>Recompute the unusable field-of-view fraction from the lab if the occulting disk instead needs to block out to 2.0 solar radii (rather than 1.5), with the same 6-solar-radius total field of view. State whether this increases or decreases the coronagraph\'s useful observing fraction.</p>') +
        problem(4, "PSP's speed record context",
                f'<p>Compute the ratio of PSP\'s record heliocentric speed ({PSP_RECORD_SPEED_KMS:.0f} km/s) to Earth\'s own orbital speed around the Sun (approximately 29.8 km/s), and state how many times faster PSP was moving at its perihelion than Earth moves in its orbit.</p>')
    )
    return pset_page(5, 'Parker Solar Probe and Remote-Sensing Geometry', "Extend this unit's in-situ wind-speed prediction and coronagraph geometry tools to new scenarios.",
                      problems, OPENSTAX)


def make_pset_05_solutions():
    r6_m = 6.0 * R_SUN
    u_6 = solve_parker_wind_speed(r6_m / PARKER_RC_M)
    v_6 = u_6 * CORONAL_SOUND_SPEED_KMS
    v_real_perihelion = solve_parker_wind_speed(PSP_PERIHELION_KM * 1000 / PARKER_RC_M) * CORONAL_SOUND_SPEED_KMS
    frac_15 = 1.5 / 6.0
    frac_20 = 2.0 / 6.0
    ratio_earth = PSP_RECORD_SPEED_KMS / 29.8
    s = (
        solution(1, "PSP's speed at a different perihelion",
                  f'<p>At r=6 R_sun (closer than r_c={PARKER_RC_RSUN:.2f} R_sun\u2019s outer region, r/r_c={r6_m/PARKER_RC_M:.2f}), the predicted Parker-wind speed is v={v_6:.0f} km/s, versus {v_real_perihelion:.0f} km/s at the real {PSP_PERIHELION_RSUN:.2f} R_sun perihelion -- the closer, hypothetical perihelion samples a *slower* wind, since it is closer to (or below) the critical point where the wind has not yet fully accelerated.</p>',
                  [('Correct numerical solve at 6 R_sun', 8), ('Correct slower-speed-closer-in conclusion', 7)]) +
        solution(2, 'Helioseismic mode counting',
                  '<p>Ten million independently measured, precisely determined mode frequencies constrain the interior sound-speed profile at many different depths and latitudes simultaneously (each mode\'s frequency depends on an integral of sound speed along its own distinct ray path), providing a hugely over-determined inversion problem -- vastly more constraining than a single inferred core temperature, which is only one number derived indirectly from overall energy-balance/neutrino arguments (Lecture 01).</p>',
                  [('Correct qualitative explanation of over-determined inversion vs single-number inference', 10)]) +
        solution(3, 'Coronagraph field-of-view sensitivity',
                  f'<p>Fraction unusable at 1.5 R_sun occulting radius = {frac_15:.3f} (25.0%); at 2.0 R_sun, fraction = {frac_20:.3f} (33.3%) -- a larger occulting disk *decreases* the coronagraph\'s useful observing fraction, from 75% to about 67% of the total field of view.</p>',
                  [('Correct fraction arithmetic for both cases', 8), ('Correct decreasing-usable-fraction conclusion', 7)]) +
        solution(4, "PSP's speed record context",
                  f'<p>Ratio = {PSP_RECORD_SPEED_KMS:.0f}/29.8 = {ratio_earth:.1f} -- PSP was moving about {ratio_earth:.0f} times faster at its perihelion than Earth moves in its own orbit around the Sun.</p>',
                  [('Correct ratio arithmetic', 15)])
    )
    return solutions_page(5, 'Parker Solar Probe and Remote-Sensing Geometry', s)


def make_pset_05_assessment():
    return assessment_md(5, 'Parker Solar Probe and Remote-Sensing Geometry',
                          ['Problem 1: verify the numerical Parker-wind solve at r=6 R_sun and the correct closer-is-slower conclusion.',
                           'Problem 2: verify the explanation invokes the over-determined, many-mode nature of helioseismic inversion, not just restating that more data is better.',
                           'Problem 3: verify both fractions are computed correctly and the decreasing-usable-fraction direction is stated correctly.',
                           'Problem 4: verify correct ratio arithmetic using Earth\'s real orbital speed.'],
                          ['Assuming wind speed increases monotonically as one gets arbitrarily close to the Sun without regard to the critical point\'s location.',
                           'Reversing the direction of the occulting-disk-size sensitivity (claiming a larger disk increases the usable fraction).',
                           'Confusing PSP\'s orbital speed with a solar-wind speed measurement in the final ratio.'])


# ===========================================================================
# LAB/PSET 06 (Lectures 11-12): Magnetopause standoff, Dst/ring current
# ===========================================================================
def make_lab_06() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes the magnetopause standoff distance across a range of real published solar wind conditions (Lecture 11), then computes ring-current energy via the Dessler-Parker-Sckopke relation for both the real 6 September 2017 storm and the Carrington Event's estimated range (Lecture 12).</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Condition</th><th>n (cm^-3)</th><th>v (km/s)</th></tr></thead><tbody>
<tr><td>Quiet solar wind</td><td>{SOLAR_WIND_SLOW_N_CM3:.0f}</td><td>{SOLAR_WIND_SLOW_V_KMS:.0f}</td></tr>
<tr><td>Fast (coronal-hole) wind</td><td>{SOLAR_WIND_FAST_N_CM3:.0f}</td><td>{SOLAR_WIND_FAST_V_KMS:.0f}</td></tr>
<tr><td>CME sheath (storm)</td><td>{SOLAR_WIND_STORM_N_CM3:.0f}</td><td>{SOLAR_WIND_STORM_V_KMS:.0f}</td></tr>
</tbody></table>
<p>All level 2, standard published OMNI-database climatological/storm-time values. Dst values: Sept 2017={STORM_DST_MIN_NT:.0f} nT (level 2); Carrington range {CARRINGTON_DST_MIN_NT_CONSERVATIVE:.0f} to {CARRINGTON_DST_MIN_NT:.0f} nT (live-verified this session).</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute the magnetopause standoff distance for all three solar wind conditions and confirm the quiet and storm values match Lecture 11's stated values.</li>
<li>Compute the dynamic-pressure enhancement factor (storm/quiet) and confirm the standoff-distance reduction is proportionally much smaller, illustrating the one-sixth-power scaling.</li>
<li>Compute the dynamic-pressure enhancement factor that would be required to compress the magnetopause exactly to geosynchronous orbit (6.6 R_E), starting from the quiet-wind dynamic pressure.</li>
<li>Compute ring-current energy (DPS relation) for the real 2017 storm and for both ends of the Carrington Dst range, and tabulate all three alongside their ratio to the 2017 value.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss why the Carrington Event's ring-current-energy range should be presented as a range with an explicit factor-of-two-plus spread (reflecting genuine, disclosed historical-reconstruction uncertainty), not collapsed to a single "best" number.</p></section>
<section><h2>Deliverables</h2><ul><li>The three-condition standoff-distance table.</li><li>The geosynchronous-compression pressure-factor calculation.</li><li>The three-event ring-current-energy comparison table.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct standoff-distance arithmetic for all three conditions.</li><li>Correctly identified one-sixth-power scaling behavior.</li><li>Correct DPS-relation arithmetic for all three Dst values, with correctly disclosed Carrington range.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Solar wind climatology: standard published, level 2. Carrington Dst range: live-verified this session; see <code>materials/ASTR370/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR370/src/generate_astr370_content.py</code>.</li></ul></section>
"""
    return lab_page(6, 'Magnetopause Compression and Ring-Current Energy',
                     "Compute magnetopause standoff distance across real solar wind conditions and ring-current energy for two real/historical geomagnetic storms.", sections)


def make_pset_06():
    problems = (
        problem(1, 'Standoff distance for the fast wind condition',
                f'<p>Compute the magnetopause standoff distance for the fast (coronal-hole) solar wind condition in this unit\'s data table, and state whether it is closer to the quiet-wind or the storm-sheath standoff distance computed in the lab.</p>') +
        problem(2, 'Dst doubling and ring-current energy',
                f'<p>Using the DPS relation\'s linear dependence on Dst, compute the ring-current energy for a hypothetical storm with Dst=-284 nT (exactly double the real 2017 storm\'s Dst magnitude), and confirm it is exactly double the 2017 storm\'s ring-current energy computed in the lab.</p>') +
        problem(3, 'Reference dipole energy sensitivity',
                f'<p>The reference energy E0=B0^2 R_E^3/(6 mu0) depends on Earth\'s equatorial field strength B0. Recompute E0 using a 5% larger B0 (representing the slow secular change in Earth\'s field over centuries) and compute the percent change in E0. Discuss whether this effect is likely to matter for comparing Dst-derived ring-current energies across a 165-year gap (1859 to 2024).</p>', points=10) +
        problem(4, 'Geosynchronous compression revisited',
                f'<p>Using the pressure factor computed in the lab (needed to compress the magnetopause to geosynchronous orbit), and the real quiet-wind dynamic pressure, compute the actual solar wind speed (holding density fixed at the quiet-wind value) that would be required to reach this pressure factor.</p>')
    )
    return pset_page(6, 'Magnetopause and Ring-Current Extensions', "Extend this unit's standoff-distance and DPS ring-current tools to new wind conditions and sensitivity checks.",
                      problems, OPENSTAX)


def make_pset_06_solutions():
    standoff_fast = magnetopause_standoff_re(SOLAR_WIND_FAST_N_CM3, SOLAR_WIND_FAST_V_KMS)
    e_ring_284 = dps_ring_current_energy_j(-284.0)
    e_ring_2017 = RING_CURRENT_ENERGY_SEPT2017_J
    e0_higher = (B0_EARTH_T * 1.05) ** 2 * R_EARTH_M ** 3 / (6 * MU0)
    pct_change_e0 = (e0_higher - DPS_E0_J) / DPS_E0_J * 100
    p_dyn_quiet = SOLAR_WIND_SLOW_N_CM3 * 1.0e6 * M_P_KG * (SOLAR_WIND_SLOW_V_KMS * 1.0e3) ** 2
    p_dyn_geo_ratio = (MAGNETOPAUSE_QUIET_RE / 6.6) ** 6
    p_dyn_geo = p_dyn_quiet * p_dyn_geo_ratio
    v_geo_kms = math.sqrt(p_dyn_geo / (SOLAR_WIND_SLOW_N_CM3 * 1.0e6 * M_P_KG)) / 1.0e3
    s = (
        solution(1, 'Standoff distance for the fast wind condition',
                  f'<p>r_mp(fast wind) = {standoff_fast:.2f} R_E, between the quiet-wind ({MAGNETOPAUSE_QUIET_RE:.2f} R_E) and storm-sheath ({MAGNETOPAUSE_STORM_RE:.2f} R_E) values -- closer to the quiet-wind value, since the fast wind\'s lower density partially offsets its higher speed in the dynamic-pressure product.</p>',
                  [('Correct standoff-distance arithmetic', 8), ('Correct comparative placement', 7)]) +
        solution(2, 'Dst doubling and ring-current energy',
                  f'<p>E_ring(-284 nT) = {e_ring_284:.2e} J, exactly double E_ring(-142 nT) = {e_ring_2017:.2e} J -- confirming the DPS relation\'s exact linear (not merely approximate) dependence on Dst.</p>',
                  [('Correct arithmetic', 8), ('Correct exact-doubling confirmation', 7)]) +
        solution(3, 'Reference dipole energy sensitivity',
                  f'<p>A 5% increase in B0 changes E0 by a factor of 1.05^2={1.05**2:.4f}, i.e., a {pct_change_e0:.1f}% increase in E0 -- since real secular changes in Earth\'s dipole field over 165 years are much smaller than 5% (of order a fraction of a percent per decade), this effect is negligible for comparing the 1859 and 2017/2024 ring-current energies at the precision used in this course.</p>',
                  [('Correct E0 recomputation and percent-change arithmetic', 6), ('Correct negligibility judgment for the real secular-change timescale', 4)]) +
        solution(4, 'Geosynchronous compression revisited',
                  f'<p>P_dyn(quiet)={p_dyn_quiet:.2e} Pa. Required pressure factor = (r_mp,quiet/6.6)^6={p_dyn_geo_ratio:.1f}. Required P_dyn={p_dyn_geo:.2e} Pa. Solving for v at fixed quiet-wind density gives v={v_geo_kms:.0f} km/s -- a very high, though not physically impossible, solar wind speed, consistent with only the most extreme storm-time sheath speeds compressing the magnetopause this far inward.</p>',
                  [('Correct pressure-factor arithmetic', 5), ('Correct solved speed', 10)])
    )
    return solutions_page(6, 'Magnetopause and Ring-Current Extensions', s)


def make_pset_06_assessment():
    return assessment_md(6, 'Magnetopause and Ring-Current Extensions',
                          ['Problem 1: verify the comparative placement (closer to quiet or storm) is justified by the density/speed tradeoff, not merely stated.',
                           'Problem 2: verify the exact doubling is confirmed numerically, not just asserted from the word "linear."',
                           'Problem 3: verify the percent-change arithmetic uses the square of the B0 ratio (since E0 depends on B0^2).',
                           'Problem 4: verify the solved speed follows correctly from the pressure-factor and fixed-density assumption.'],
                          ['Forgetting that E0 depends on B0 squared, not linearly, when computing the percent-change sensitivity.',
                           'Sign or direction errors in the fast-wind standoff-distance comparison.',
                           'Arithmetic errors in extracting v from P_dyn=n m_p v^2 (forgetting the square root).'])


# ===========================================================================
# LAB/PSET 07 (Lectures 13-14): Capstone -- technological impacts and GIC
# ===========================================================================
def make_lab_07() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This capstone lab estimates a representative geomagnetically induced current (GIC)-driving geoelectric field from a specified rate of magnetic-field change (Lecture 14), and synthesizes this course's full flare-to-grid physical chain using the real 6 September 2017 event and the Carrington Event as bracketing case studies.</p></section>
<section><h2>Materials and Data</h2>
<p>2024 Beggan et al. reanalysis (live-verified this session): Carrington-era field-change rate &gt;700 nT/minute, exceeding the modern 1-in-100-year extreme value of 350-400 nT/minute at the same latitude. A simplified geoelectric-field estimate uses a uniform-half-space approximation, E &prop; sqrt(dB/dt) for a given ground conductivity (a standard, simplified space-weather-engineering approximation; level 3 for this course's specific numeric ground-conductivity choice, disclosed in <code>../reference-log.md</code>).</p></section>
<section><h2>Procedure</h2><ol>
<li>Compute the ratio of the Carrington-era field-change rate (using the reported >700 nT/min value) to the modern 1-in-100-year extreme value, and state this ratio as a measure of how anomalous the 1859 event's rate of change was, independent of its Dst magnitude.</li>
<li>Using the simplified E &prop; sqrt(dB/dt) scaling, compute the factor by which the induced geoelectric field (and hence GIC magnitude, which scales linearly with the geoelectric field in a simple resistive-line model) would increase for the Carrington-era rate of change relative to the modern extreme-value benchmark.</li>
<li>Tabulate this course's full seven-unit case-study chain for the real 6 September 2017 event: one specific real numeric quantity from each unit (structure/atmosphere, magnetism/sunspots, flares, CME/solar wind, missions, magnetosphere/Dst, and technological impact).</li>
<li>Identify, from your own tabulated chain, which single quantity is level 1 (live-verified this session), which are level 2 (standard published, not re-verified), and which (if any) are level 3 (order-of-magnitude/illustrative), and confirm this matches <code>../reference-log.md</code>'s disclosure.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Discuss why GIC risk assessment cannot rely on Dst magnitude alone (Lecture 14's central point) and why the Beggan et al. (2024) dB/dt reanalysis is a genuinely distinct, additional piece of evidence for Carrington-level risk, not merely a restatement of the already-known large Dst estimate.</p></section>
<section><h2>Deliverables</h2><ul><li>The dB/dt ratio and the implied geoelectric-field/GIC scaling factor.</li><li>The complete seven-unit case-study chain table with provenance levels for each entry.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct dB/dt ratio arithmetic.</li><li>Correct sqrt-scaling arithmetic for the implied GIC factor.</li><li>Complete, accurate seven-unit chain table with correctly assigned provenance levels for every entry.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>2024 Beggan et al. reanalysis: live-verified this session (via the Carrington Event Wikipedia article, citing Beggan, Clarke, Lawrence, Eaton et al. 2024, Space Weather 22, e2023SW003807); see <code>materials/ASTR370/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR370/src/generate_astr370_content.py</code>.</li></ul></section>
"""
    return lab_page(7, 'Capstone: Geomagnetically Induced Currents and the Full Flare-to-Grid Chain',
                     "Estimate GIC risk scaling from the real Carrington-era field-change rate and synthesize this course's full seven-unit case study chain.", sections)


def make_pset_07():
    problems = (
        problem(1, 'A more conservative dB/dt estimate',
                '<p>Suppose a more conservative reanalysis found the Carrington-era field-change rate to be only 500 nT/minute (rather than the >700 nT/min value used in the lab), still compared to the modern 350-400 nT/minute benchmark (use 375 nT/min as the benchmark\'s midpoint). Recompute the dB/dt ratio and the implied sqrt-scaling GIC factor, and compare both to the lab\'s original values.</p>') +
        problem(2, 'Full chain for a different bracketing event',
                '<p>Using this course\'s seven-unit framework (as tabulated in the lab for the 6 September 2017 event), briefly identify what the equivalent Unit 6 (Dst/magnetosphere) quantity would be if this course instead used the Carrington Event as the primary running case study rather than as a comparison point, and state which one of its two published Dst estimates you would choose to headline and why.</p>', points=10) +
        problem(3, 'GIC scaling with grid length',
                '<p>A simple resistive model predicts total GIC in a power line scales linearly with both the induced geoelectric field and the line\'s length. If a regional grid operator doubles the length of a vulnerable transmission line (through a grid expansion) without changing anything else, state, using this simple scaling, what happens to the GIC magnitude for a fixed geoelectric field, and connect this to why grid operators in high-latitude regions (like Quebec) have historically been more concerned about GIC risk than operators of shorter, lower-latitude grids.</p>') +
        problem(4, 'Course-long synthesis',
                '<p>In two to three sentences, describe the complete physical chain this course has derived from the solar interior (Lecture 01) to a real ground-based technological impact (Lecture 14), naming at least four of the seven thematic units in the correct order.</p>', points=10)
    )
    return pset_page(7, 'Capstone: GIC Risk and Course-Long Synthesis', "Apply this unit's GIC-scaling tool to a revised estimate and synthesize the course's full physical chain.",
                      problems, OPENSTAX)


def make_pset_07_solutions():
    ratio_lab = 700.0 / 375.0
    sqrt_factor_lab = math.sqrt(ratio_lab)
    ratio_conservative = 500.0 / 375.0
    sqrt_factor_conservative = math.sqrt(ratio_conservative)
    s = (
        solution(1, 'A more conservative dB/dt estimate',
                  f'<p>Conservative ratio = 500/375 = {ratio_conservative:.2f}, implied GIC scaling factor = sqrt({ratio_conservative:.2f}) = {sqrt_factor_conservative:.2f} -- both smaller than the lab\'s original values (ratio {ratio_lab:.2f}, factor {sqrt_factor_lab:.2f}), illustrating that even a more conservative reanalysis still implies a substantially elevated (not merely comparable) GIC risk relative to the modern benchmark.</p>',
                  [('Correct ratio and sqrt-factor arithmetic', 8), ('Correct comparison to the lab\'s original values', 7)]) +
        solution(2, 'Full chain for a different bracketing event',
                  '<p>The equivalent Unit 6 quantity would be the Carrington Event\'s estimated Dst itself (rather than the 2017 event\'s published -142 nT). Given the genuine, disclosed uncertainty between the two published estimates (-800 nT conservative vs -1750 nT), a defensible choice is to headline the full estimated range rather than a single number, explicitly noting which study each endpoint comes from -- exactly the disclosure practice this course\'s own lectures and labs follow.</p>',
                  [('Correct identification of the Dst quantity as the Unit 6 equivalent', 5), ('Reasoned, non-overclaiming choice of range-vs-single-number presentation', 5)]) +
        solution(3, 'GIC scaling with grid length',
                  '<p>Doubling the line length doubles the total GIC magnitude at fixed geoelectric field (since GIC &prop; E x length in this simple resistive model). High-latitude grids like Quebec\'s are both longer (spanning greater distances) and experience larger geoelectric fields during storms (since auroral/ring-current-driven magnetic disturbances are strongest at high geomagnetic latitude), so both factors compound to increase their GIC risk relative to shorter, lower-latitude grids.</p>',
                  [('Correct linear length-scaling statement', 5), ('Correct compounding-factors explanation for high-latitude grids', 10)]) +
        solution(4, 'Course-long synthesis',
                  '<p>Example full-credit answer: "The Sun\'s hydrostatic interior structure (Unit 1) sets the stage for the dynamo-driven magnetic cycle and sunspots (Unit 2), whose stored free magnetic energy powers flares (Unit 3); a flare\'s associated CME propagates through the Parker solar wind (Unit 4) until it compresses Earth\'s magnetosphere and drives a ring current measured by Dst (Unit 6), whose rapid field changes ultimately induce the geomagnetically induced currents that can collapse power grids (Unit 7)."</p>',
                  [('At least four units named in correct order with correct one-clause physical link between each', 15)])
    )
    return solutions_page(7, 'Capstone: GIC Risk and Course-Long Synthesis', s)


def make_pset_07_assessment():
    return assessment_md(7, 'Capstone: GIC Risk and Course-Long Synthesis',
                          ['Problem 1: verify both the ratio and its square root are recomputed correctly for the revised 500 nT/min value.',
                           'Problem 2: verify the student explicitly discusses the two-estimate uncertainty rather than presenting a single Carrington Dst value as certain.',
                           'Problem 3: verify the linear length-scaling claim is stated correctly and the high-latitude compounding explanation includes both the length and field-strength factors.',
                           'Problem 4: verify at least four units are named in a physically correct causal order, not merely listed.'],
                          ['Treating the Carrington Dst estimate as a single certain number rather than a disclosed range in Problem 2.',
                           'Omitting the geoelectric-field-strength factor (focusing only on grid length) in the high-latitude risk explanation for Problem 3.',
                           'Listing course units out of causal order in the Problem 4 synthesis (e.g., placing the magnetosphere response before the flare/CME).'])


def write_labs_psets():
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
    for i, (pfn, sfn, afn) in enumerate(psets, start=1):
        (PSET_DIR / f'problem-set-{i:02d}.html').write_text(pfn(), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-solutions.html').write_text(sfn(), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-assessment.md').write_text(afn(), encoding='utf-8')


if __name__ == '__main__':
    write_labs_psets()
    print('Wrote 7 labs and 7 problem sets (with solutions and assessment instructions).')
