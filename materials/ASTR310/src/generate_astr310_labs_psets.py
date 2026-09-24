"""Lab and problem-set generator for ASTR310.

Depends on the shared constants and page()/CSS helpers in
generate_astr310_content.py so every number here traces back to the same
verified real data (Alpha Centauri AB, live-verified this session; Sirius B
from ASTR230; standard published solar-interior, cluster, and solar-system
values) used in the paired lectures. Run with the project interpreter:
    python materials/ASTR310/src/generate_astr310_content.py
    python materials/ASTR310/src/generate_astr310_labs_psets.py
"""
from __future__ import annotations

import math
from html import escape

from generate_astr310_content import (
    CSS, page, li, LAB_DIR, PSET_DIR, DATA_DIR,
    SIGMA_SB, G_NEWTON, C_LIGHT, H_PLANCK, K_BOLTZMANN, M_PROTON, SIGMA_THOMSON,
    M_SUN_KG, R_SUN_M, L_SUN_W, AU_M, YEAR_S, PC_M, MPC_KM, KM, SUN_TEFF, WIEN_B,
    wien_peak_wavelength_m, stefan_boltzmann_luminosity_w,
    ALPHA_CEN_A, ALPHA_CEN_B, ALPHA_CEN_ORBIT, PROXIMA_ORBIT, SIRIUS_B,
    EARTH_MASS_KG, EARTH_RADIUS_M, MOON_MASS_KG, MOON_RADIUS_M, MOON_ORBIT_M,
    JUPITER_MASS_KG, IO_MASS_KG, IO_RADIUS_M, IO_SEMIMAJOR_M, IO_ECCENTRICITY, IO_SURFACE_GRAVITY_MS2,
    CHANDRASEKHAR_MASS_MSUN, M15_SIGMA_KMS, M15_HALF_LIGHT_PC, M15_PUBLISHED_MASS_MSUN,
    virial_mass_msun, kepler3_total_mass_msun, escape_velocity_ms,
    hydrostatic_central_pressure_pa, virial_core_temperature_k, roche_limit_m,
    eddington_luminosity_w, vis_viva_speed_ms, tidal_acceleration_diff,
    ALPHA_CEN_TOTAL_MASS_KEPLER, ALPHA_CEN_TOTAL_MASS_MEASURED,
    ALPHA_CEN_A_L_FROM_SB_LSUN, ALPHA_CEN_B_L_FROM_SB_LSUN,
    EARTH_ESCAPE_KMS, SUN_ESCAPE_KMS, SIRIUS_B_ESCAPE_KMS,
    SUN_CENTRAL_PRESSURE_EST, SUN_CENTRAL_PRESSURE_PUBLISHED,
    SUN_VIRIAL_TEMP_EST, SUN_CORE_TEMP_PUBLISHED, M15_VIRIAL_MASS_EST,
    MOON_DENSITY, EARTH_DENSITY, EARTH_MOON_ROCHE_M, IO_DENSITY,
    JUPITER_MEAN_DENSITY, IO_ROCHE_M, IO_TIDAL_ACCEL,
    CHANDRASEKHAR_MASS_KG, EDDINGTON_L_CHANDRA_W, EDDINGTON_L_CHANDRA_LSUN, EDDINGTON_L_SUN_W,
    MU_SUN, EARTH_A_AU, EARTH_E, MARS_A_AU, MARS_TRANSFER_A_AU,
    V_EARTH_CIRCULAR, V_TRANSFER_PERIHELION, HOHMANN_DV1, V_MARS_CIRCULAR,
    V_TRANSFER_APHELION, HOHMANN_DV2, HOHMANN_TRANSFER_TIME_YR, SUN_EARTH_L1_KM,
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
    return page(f'ASTR 310 Lab {n:02d}', body)


def pset_page(n: int, title: str, focus: str, problems_html: str, reading: str) -> str:
    body = f"""<header><div><h1>ASTR 310 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header>
<main><section><h2>Problems</h2>{problems_html}</section>
<section><h2>Due and Scope</h2><p>Submit a complete derivation with equations, units, labeled quantities, and a short narrative interpretation for each problem. Show every step; a correct final number without a visible derivation receives partial credit at most, and quoting a lecture number without adapting it to this problem's specific inputs receives no credit for that step.</p></section>
<section><h2>OpenStax Companion Reading</h2><p>{escape(reading)}</p></section>
<section><h2>References and Data Sources</h2><ul><li>Corresponding lecture slides and notes for this unit.</li><li>{OPENSTAX}.</li><li>Course datasets under <code>materials/ASTR310/data/</code> where referenced above.</li></ul></section>
</main>"""
    return page(f'ASTR 310 Problem Set {n:02d}', body)


def solutions_page(n: int, title: str, solutions_html: str) -> str:
    body = f"<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header><main><section><h2>Worked Solutions</h2>{solutions_html}</section><section><h2>Grading Notes</h2><p>Award full marks for correct method, units, and a numeric result consistent with the arithmetic shown (allow reasonable rounding). Verify that the student re-derives the number for this problem's specific inputs rather than quoting a lecture example without adaptation. Watch specifically for unit-conversion errors (AU/m, years/seconds, km/Mpc, Msun/kg) -- these are the most common source of order-of-magnitude mistakes in this course.</p></section></main>"
    return page(f'ASTR 310 Problem Set {n:02d} Solutions', body)


def assessment_md(n: int, title: str, criteria: list, common_errors: list) -> str:
    crit = '\n'.join(f'- {c}' for c in criteria)
    err = '\n'.join(f'- {e}' for e in common_errors)
    return f"""# Assessment Instructions: Problem Set {n:02d} \u2014 {title}

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the referenced dataset(s) under `materials/ASTR310/data/`.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking number but no visible derivation steps should not. Because this is a 300-level quantitative course, full marks require a genuine derivation (not just formula substitution) wherever the problem set asks for one.

## Problem-Level Criteria
{crit}

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
{err}
"""


# ---------------------------------------------------------------------------
# LAB 01: Blackbody radiation law applied to the Sun and Alpha Centauri A/B
# ---------------------------------------------------------------------------
def make_lab_01() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This is a data-analysis lab using real, precisely measured stellar parameters for the Sun and for Alpha Centauri A and B (live-verified this session via a direct fetch of the Alpha Centauri system's measured orbital and stellar parameters, citing Akeson et al. 2021, <em>AJ</em> 162, 14; see <code>../reference-log.md</code> for full provenance). No telescope time is required; the lab reproduces, from first principles, the Stefan-Boltzmann and Wien's-law cross-checks introduced in Lecture 02.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Star</th><th>T_eff (K)</th><th>R (R&#8857;)</th><th>Measured L (L&#8857;)</th><th>Spectral type</th></tr></thead><tbody>
<tr><td>Sun</td><td>{SUN_TEFF:.0f}</td><td>1.000</td><td>1.000</td><td>G2V</td></tr>
<tr><td>{escape(ALPHA_CEN_A['name'])}</td><td>{ALPHA_CEN_A['teff']:.0f}</td><td>{ALPHA_CEN_A['radius_rsun']:.3f}</td><td>{ALPHA_CEN_A['lum_lsun']:.4f}</td><td>{ALPHA_CEN_A['spt']}</td></tr>
<tr><td>{escape(ALPHA_CEN_B['name'])}</td><td>{ALPHA_CEN_B['teff']:.0f}</td><td>{ALPHA_CEN_B['radius_rsun']:.3f}</td><td>{ALPHA_CEN_B['lum_lsun']:.4f}</td><td>{ALPHA_CEN_B['spt']}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>For each of the three stars, compute the Wien's-law peak wavelength &lambda;_max = b/T_eff using b = {WIEN_B:.4e} m&middot;K, and identify which part of the electromagnetic spectrum each peak falls in.</li>
<li>For each star, compute the Stefan-Boltzmann luminosity L = 4&pi;R&sup2;&sigma;T&#8308; from its measured radius and temperature (convert R to meters and T to kelvin first), then convert the result to solar luminosities.</li>
<li>Compare each star's Stefan-Boltzmann luminosity to its independently measured (asteroseismic/interferometric) luminosity from the data table, and compute the percent agreement for each star.</li>
<li>Rank the three stars by T_eff, by radius, and by Stefan-Boltzmann luminosity, and explain in one paragraph why Alpha Centauri B is both cooler and smaller than the Sun yet not simply proportionally less luminous (i.e., discuss how L depends on both R and T, not R or T alone).</li>
<li>Propagate a plausible &plusmn;1% uncertainty in each star's measured radius through the Stefan-Boltzmann formula (noting L &prop; R&sup2;, so a fractional radius uncertainty is doubled in the resulting fractional luminosity uncertainty) and state whether this uncertainty alone could explain the percent agreement found in step 3.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Because L &prop; R&sup2;T&#8308;, the fractional uncertainty in a Stefan-Boltzmann luminosity estimate is approximately 2&times;(fractional radius uncertainty) + 4&times;(fractional temperature uncertainty) added in quadrature; the T&#8308; dependence means that even a small temperature uncertainty can dominate the total luminosity uncertainty budget.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed Wien's-law and Stefan-Boltzmann tables for all three stars, with full unit conversions shown.</li><li>Percent-agreement calculation between the Stefan-Boltzmann and measured luminosity for each star.</li><li>Written comparison paragraph addressing the R&sup2;T&#8308; dependence.</li><li>Uncertainty-propagation estimate and a one-paragraph judgment of whether measurement uncertainty alone explains the observed agreement.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct unit conversions (R&#8857; to m, T_eff already in K) before applying the Stefan-Boltzmann formula.</li><li>Correct percent-agreement arithmetic for all three stars.</li><li>Written comparison correctly explains the R&sup2;T&#8308; scaling rather than attributing luminosity differences to radius or temperature alone.</li><li>Uncertainty propagation correctly applies the doubled/quadrupled fractional-uncertainty scaling for R and T respectively.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 5.4 and Chapter 18.1.</li><li>Alpha Centauri A/B parameters: live-verified this session (Wikipedia "Alpha Centauri," citing Akeson et al. 2021, <em>AJ</em> 162, 14); see <code>materials/ASTR310/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR310/src/generate_astr310_content.py</code>.</li></ul></section>
"""
    return lab_page(1, 'Verifying the Blackbody Radiation Law for the Sun and Alpha Centauri A/B',
                     'Apply Wien\u2019s law and the Stefan-Boltzmann law to three real, precisely measured stars and cross-check against independently measured luminosities.', sections)


# ---------------------------------------------------------------------------
# LAB 02: Optical depth and the Boltzmann excitation equation
# ---------------------------------------------------------------------------
def make_lab_02() -> str:
    e2_minus_e1_j = 1.634e-18  # 10.2 eV, hydrogen n=1 to n=2
    temps = [4000.0, 5750.0, 7500.0, 9900.0, 15000.0]
    rows = ''.join(
        f'<tr><td>{t:.0f}</td><td>{4*math.exp(-e2_minus_e1_j/(K_BOLTZMANN*t)):.3e}</td></tr>' for t in temps
    )
    tau_values = [0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0]
    tau_rows = ''.join(f'<tr><td>{t:.1f}</td><td>{math.exp(-t):.4f}</td></tr>' for t in tau_values)
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab has two parts: (1) computing the transmitted intensity fraction through slabs of increasing optical depth (Lecture 03), and (2) computing the Boltzmann n=2/n=1 hydrogen excitation ratio across a range of real stellar temperatures spanning K to B spectral types (Lecture 04), reproducing the qualitative OBAFGKM Balmer-strength argument from ASTR 230 quantitatively.</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Optical depth &tau;</th><th>Transmitted fraction e&#8315;&#964;</th></tr></thead><tbody>{tau_rows}</tbody></table>
<table><thead><tr><th>T_eff (K)</th><th>Boltzmann n2/n1 ratio (E2&minus;E1 = 10.2 eV, g2/g1 = 4)</th></tr></thead><tbody>{rows}</tbody></table>
</section>
<section><h2>Procedure</h2><ol>
<li>Using I(&tau;)/I(0) = e&#8315;&#964;, complete the transmitted-fraction table above for all seven listed optical depths, and plot transmitted fraction versus &tau; on both linear and semi-log axes; explain which axis choice makes the exponential relationship easiest to verify visually.</li>
<li>Using n2/n1 = (g2/g1) exp[&minus;(E2&minus;E1)/kT], complete the Boltzmann-ratio table above for all five listed temperatures (spanning K-type Alpha Centauri B-like stars to B-type stars), showing the kT calculation explicitly at each temperature.</li>
<li>Compute the ratio of the n2/n1 value at 9,900 K (A-type, near Vega/Sirius A) to the value at 5,750 K (G/K-type, near the Sun and Alpha Centauri A/B), and state whether this is consistent with the much stronger observed Balmer lines in A-type stars discussed in ASTR 230.</li>
<li>Using only the Boltzmann equation (ignoring the Saha ionization turnover from Lecture 04), predict what the n2/n1 ratio would be at 25,000 K (a hot white dwarf's photospheric temperature, comparable to Sirius B's), and explain in one paragraph why this naive extrapolation overstates the expected Balmer-line strength at such a high temperature.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The Boltzmann-ratio calculation above ignores the Saha-equation ionization turnover entirely; state explicitly which physical process (not included in this lab's calculation) becomes important above roughly 10,000 K and would need to be added to obtain a fully correct line-strength prediction across the full OBAFGKM range.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed transmitted-fraction table and both plots (linear and semi-log).</li><li>Completed Boltzmann-ratio table with kT shown explicitly at each temperature.</li><li>Ratio calculation (9,900 K vs. 5,750 K) with a written interpretation.</li><li>Written paragraph on the naive high-temperature extrapolation and the missing Saha-equation physics.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct exponential arithmetic (not linear-approximation arithmetic) for all seven optical-depth values.</li><li>Correct Boltzmann-ratio arithmetic with correctly converted units (eV to J) at all five temperatures.</li><li>Correct qualitative connection to the OBAFGKM Balmer-strength sequence from ASTR 230.</li><li>Correct identification that the Saha equation, not the Boltzmann equation alone, is needed for the high-temperature turnover.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 5.5 and Chapter 17.3.</li><li>Generated by <code>materials/ASTR310/src/generate_astr310_content.py</code>.</li></ul></section>
"""
    return lab_page(2, 'Optical Depth and the Boltzmann Excitation Equation',
                     'Compute exponential radiative attenuation and hydrogen excitation ratios across real stellar temperatures.', sections)


# ---------------------------------------------------------------------------
# LAB 03: Hydrostatic equilibrium (Sun) and the virial theorem (M15)
# ---------------------------------------------------------------------------
def make_lab_03() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>Part 1 estimates the Sun's central pressure from the uniform-density hydrostatic-equilibrium scaling (Lecture 05) and compares it to the published standard-solar-model value. Part 2 applies the virial theorem's cluster-mass estimator (Lecture 06) to the globular cluster M15, using its published velocity dispersion and half-light radius (standard literature values, flagged for spot-check in <code>../reference-log.md</code>).</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Sun mass, radius</td><td>{M_SUN_KG:.3e} kg, {R_SUN_M:.3e} m</td></tr>
<tr><td>Standard solar model central pressure (published)</td><td>{SUN_CENTRAL_PRESSURE_PUBLISHED:.3e} Pa</td></tr>
<tr><td>Standard solar model core temperature (published)</td><td>{SUN_CORE_TEMP_PUBLISHED:.3e} K</td></tr>
<tr><td>M15 velocity dispersion &sigma; (published)</td><td>{M15_SIGMA_KMS:.1f} km/s</td></tr>
<tr><td>M15 half-light radius R_h (published)</td><td>{M15_HALF_LIGHT_PC:.1f} pc</td></tr>
<tr><td>M15 commonly cited dynamical mass (published)</td><td>{M15_PUBLISHED_MASS_MSUN:.1e} M&#8857;</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using P_c &asymp; (3/8&pi;)GM&sup2;/R&#8308;, compute the Sun's estimated central pressure and compare it (percent difference) to the published standard-solar-model value.</li>
<li>Using T &asymp; &mu;m_p GM/(5kR) with &mu; = 0.5 (fully ionized hydrogen), compute the Sun's estimated central/mean temperature and compare it to the published core temperature.</li>
<li>Using M &asymp; 5&sigma;&sup2;R_h/G, compute M15's virial mass from its published velocity dispersion and half-light radius, and compare it (percent difference) to the commonly cited dynamical mass.</li>
<li>State, for each of the three estimates above, whether the simple order-of-magnitude formula over- or under-predicts the more detailed/independently cited value, and propose one physical reason for the direction of each discrepancy (e.g., the Sun's real density profile is far more centrally concentrated than uniform; M15's true mass profile is not a single uniform sphere).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The uniform-density approximation used in both the hydrostatic-pressure and virial-temperature estimates ignores the fact that real self-gravitating systems (stars, clusters) are centrally concentrated, not uniform; state explicitly whether you would expect this to make the true central pressure/temperature higher or lower than the uniform-density estimate, and check whether your Part 1 results are consistent with that expectation.</p></section>
<section><h2>Deliverables</h2><ul><li>Sun central-pressure and central-temperature estimates with percent-difference comparisons to the published values.</li><li>M15 virial-mass estimate with a percent-difference comparison to the published dynamical mass.</li><li>Written discussion of the direction and physical cause of each discrepancy.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct unit conversions and arithmetic for all three order-of-magnitude estimates.</li><li>Correct percent-difference calculations against the stated published comparison values.</li><li>Physically sound (not merely stated) reasoning for the direction of each discrepancy, referencing central concentration.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 15.4-15.5.</li><li>M15 velocity dispersion, half-light radius, and dynamical mass: standard published globular-cluster literature values, not independently re-verified this session; flagged for spot-check against the Harris (1996, 2010 revision) Galactic globular cluster catalog in <code>materials/ASTR310/reference-log.md</code>.</li><li>Standard solar model central pressure/temperature: standard published values, not independently re-verified this session.</li></ul></section>
"""
    return lab_page(3, 'Hydrostatic Equilibrium (the Sun) and the Virial Theorem (M15)',
                     'Estimate the Sun\u2019s central pressure and temperature and a globular cluster\u2019s virial mass from first-principles scaling relations.', sections)


# ---------------------------------------------------------------------------
# LAB 04: Alpha Centauri AB Kepler's-third-law mass determination
# ---------------------------------------------------------------------------
def make_lab_04() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab reproduces, with full unit-conversion detail, the Alpha Centauri AB total-mass determination from Lecture 08 and the shell-theorem/escape-velocity comparisons from Lecture 07, using the live-verified orbital elements and stellar parameters in <code>../data/alpha_centauri_orbit.csv</code> and <code>../data/alpha_centauri_ab.csv</code>.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Orbital period P</td><td>{ALPHA_CEN_ORBIT['period_yr']:.3f} yr</td></tr>
<tr><td>Semimajor axis a</td><td>{ALPHA_CEN_ORBIT['semimajor_au']:.3f} AU</td></tr>
<tr><td>Eccentricity e</td><td>{ALPHA_CEN_ORBIT['eccentricity']:.5f}</td></tr>
<tr><td>{escape(ALPHA_CEN_A['name'])} measured mass</td><td>{ALPHA_CEN_A['mass_msun']:.4f} M&#8857;</td></tr>
<tr><td>{escape(ALPHA_CEN_B['name'])} measured mass</td><td>{ALPHA_CEN_B['mass_msun']:.4f} M&#8857;</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Convert P to seconds and a to meters, then apply the generalized Kepler's third law, (m1+m2) = 4&pi;&sup2;a&sup3;/(GP&sup2;), to obtain the total system mass in kilograms, then convert to solar masses.</li>
<li>Compare your Kepler-derived total mass to the independently measured sum of the two stars' masses, and compute the percent agreement.</li>
<li>Compute the surface escape velocity for Alpha Centauri A and for Alpha Centauri B using their measured masses and radii, and compare both to Earth's and the Sun's escape velocities (also compute these) and to Sirius B's escape velocity (a white dwarf, carried forward from ASTR230; data given in the lecture).</li>
<li>Rank all five objects (Earth, Sun, Alpha Centauri A, Alpha Centauri B, Sirius B) by escape velocity, and explain in one paragraph why Sirius B's escape velocity is so much higher despite its unremarkable mass, tying the explanation explicitly to the 1/&radic;R dependence in the escape-velocity formula.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The published semimajor axis (17.493 &plusmn; 0.0096 arcsec, converted using the measured parallax) and period (79.762 &plusmn; 0.019 yr) both carry small formal uncertainties; propagate the semimajor-axis uncertainty alone through Kepler's third law (noting the total mass scales as a&sup3;, so a fractional semimajor-axis uncertainty is tripled in the resulting fractional mass uncertainty) and compare the resulting mass uncertainty to the percent agreement found in step 2.</p></section>
<section><h2>Deliverables</h2><ul><li>Full unit-conversion chain and Kepler's-third-law total-mass calculation.</li><li>Percent-agreement comparison to the independently measured mass sum.</li><li>Escape-velocity table for all five objects with the full ranking and written explanation.</li><li>Propagated semimajor-axis uncertainty and comparison to the observed agreement.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct unit conversions (years to seconds, AU to meters) before applying Kepler's third law -- this is the most common point of error in this lab.</li><li>Correct percent-agreement arithmetic.</li><li>Correct escape-velocity calculations and ranking for all five objects.</li><li>Correct application of the tripled fractional-uncertainty scaling for the semimajor axis.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 3.1-3.3.</li><li>Alpha Centauri AB orbital elements and masses: live-verified this session; Sirius B: carried forward from ASTR230 (Bond et al. 2017, <em>ApJ</em> 840, 70), provenance already established there.</li></ul></section>
"""
    return lab_page(4, 'Weighing Alpha Centauri AB with Kepler\u2019s Third Law',
                     'Determine the total mass of a real binary star system from its measured orbit alone, and compare escape velocities across five real objects.', sections)


# ---------------------------------------------------------------------------
# LAB 05: Binary mass-ratio splitting and tidal Roche limit / heating
# ---------------------------------------------------------------------------
def make_lab_05() -> str:
    mass_ratio = ALPHA_CEN_B['mass_msun'] / ALPHA_CEN_A['mass_msun']
    m_a_split = ALPHA_CEN_TOTAL_MASS_KEPLER / (1 + mass_ratio)
    m_b_split = ALPHA_CEN_TOTAL_MASS_KEPLER - m_a_split
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>Part 1 reproduces the mass-ratio splitting of the Alpha Centauri AB total mass (Lecture 09) into individual stellar masses. Part 2 computes the Roche limit for the Earth-Moon system and Io's differential tidal acceleration from Jupiter (Lecture 10), using the standard published Io/Jupiter values in <code>../data/io_jupiter_tidal.csv</code>.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Alpha Cen AB Kepler total mass (Lab 04)</td><td>{ALPHA_CEN_TOTAL_MASS_KEPLER:.4f} M&#8857;</td></tr>
<tr><td>Mass ratio M_B/M_A (independently measured)</td><td>{mass_ratio:.4f}</td></tr>
<tr><td>Earth mass, radius, mean density</td><td>{EARTH_MASS_KG:.3e} kg, {EARTH_RADIUS_M:.3e} m, {EARTH_DENSITY:.0f} kg/m&sup3;</td></tr>
<tr><td>Moon mass, radius, mean density</td><td>{MOON_MASS_KG:.3e} kg, {MOON_RADIUS_M:.3e} m, {MOON_DENSITY:.0f} kg/m&sup3;</td></tr>
<tr><td>Jupiter mass, mean density</td><td>{JUPITER_MASS_KG:.3e} kg, {JUPITER_MEAN_DENSITY:.0f} kg/m&sup3;</td></tr>
<tr><td>Io mass, radius, semimajor axis, eccentricity</td><td>{IO_MASS_KG:.3e} kg, {IO_RADIUS_M:.3e} m, {IO_SEMIMAJOR_M:.3e} m, {IO_ECCENTRICITY:.4f}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using the total mass from Lab 04 and the independently measured mass ratio M_B/M_A above, split the total mass into individual masses for Alpha Centauri A and B, and compare your result to the independently quoted individual masses (M_A = {ALPHA_CEN_A['mass_msun']:.4f} M&#8857;, M_B = {ALPHA_CEN_B['mass_msun']:.4f} M&#8857;).</li>
<li>Compute the rigid-body Roche limit for the Earth-Moon system (using each body's mean density) and compare it to the Moon's actual orbital distance ({MOON_ORBIT_M/1000:.0f} km); state whether the Moon is inside or outside its own Roche limit and by what factor.</li>
<li>Compute the differential tidal acceleration across Io due to Jupiter, &Delta;a = 2GM_Jupiter R_Io/a_Io&sup3;, and express the result as a percentage of Io's own surface gravity (g = GM_Io/R_Io&sup2;, not Earth's), since Io's own gravity is the physically relevant comparison for whether the tidal stress is dynamically significant.</li>
<li>Given that Io's orbit is forced to remain slightly eccentric (e = {IO_ECCENTRICITY:.4f}) by an orbital resonance with Europa and Ganymede, explain in one paragraph why a perfectly circular orbit at the same semimajor axis would produce far less tidal heating, even though the differential tidal acceleration computed in step 3 would be identical at every point in a circular orbit.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The mass-ratio splitting in step 1 uses an independently measured mass ratio that was itself derived using stellar-structure/asteroseismic modeling consistent with the quoted individual masses; state explicitly why this makes the "agreement" in step 1 a consistency check on the arithmetic rather than a fully independent confirmation, in contrast to the genuinely independent agreement demonstrated in Lecture 08 between the Kepler-derived and measured total mass.</p></section>
<section><h2>Deliverables</h2><ul><li>Individual-mass splitting calculation and comparison to the quoted individual masses.</li><li>Earth-Moon Roche-limit calculation and comparison to the Moon's actual orbital distance.</li><li>Io tidal-acceleration calculation expressed as a percentage of Io's own surface gravity.</li><li>Written explanation of why orbital eccentricity, not just tidal acceleration magnitude, drives tidal heating.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct mass-ratio splitting arithmetic.</li><li>Correct Roche-limit calculation with correctly computed mean densities.</li><li>Correct tidal-acceleration calculation with correct unit conversions (km to m).</li><li>Written explanation correctly distinguishes tidal-acceleration magnitude from tidal-flexing (heating), which requires a changing tidal configuration over an orbit.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 18.4-18.5 and Chapter 3.6.</li><li>Io/Jupiter parameters: standard published values, not independently re-verified this session; flagged in <code>materials/ASTR310/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(5, 'Splitting a Binary\u2019s Mass and Computing Tidal Effects',
                     'Split Alpha Centauri AB\u2019s total mass into individual masses, and compute the Roche limit and tidal acceleration for real solar-system examples.', sections)


# ---------------------------------------------------------------------------
# LAB 06: Hohmann transfer and Lagrange-point / hierarchy calculations
# ---------------------------------------------------------------------------
def make_lab_06() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>Part 1 reproduces the Earth-to-Mars Hohmann transfer calculation from Lecture 11 in full unit-conversion detail. Part 2 computes the Sun-Earth and Sun-Jupiter L1 distances and evaluates the Alpha Centauri AB-Proxima hierarchy ratio from Lecture 12.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Earth semimajor axis, eccentricity</td><td>{EARTH_A_AU:.4f} AU, {EARTH_E:.4f}</td></tr>
<tr><td>Mars semimajor axis</td><td>{MARS_A_AU:.4f} AU</td></tr>
<tr><td>Sun standard gravitational parameter GM_Sun</td><td>{MU_SUN:.4e} m&sup3;/s&sup2;</td></tr>
<tr><td>Jupiter mass</td><td>{JUPITER_MASS_KG:.3e} kg</td></tr>
<tr><td>Alpha Cen AB semimajor axis</td><td>{ALPHA_CEN_ORBIT['semimajor_au']:.3f} AU</td></tr>
<tr><td>Proxima periastron distance about AB</td><td>{PROXIMA_ORBIT['periastron_au']:.0f} AU</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute the Hohmann transfer orbit's semimajor axis (average of Earth's and Mars's semimajor axes), then compute Earth's circular-orbit speed, the transfer orbit's perihelion speed, and the first burn &Delta;v1.</li>
<li>Compute Mars's circular-orbit speed, the transfer orbit's aphelion speed, and the second burn &Delta;v2, then the total mission &Delta;v (sum of both burns) and the one-way transfer time in days.</li>
<li>Compute the Sun-Earth L1 distance using r_L1 &asymp; R(m_Earth/3m_Sun)^(1/3), and separately compute the Sun-Jupiter L1 distance using the same formula with Jupiter's mass and orbital radius (5.2 AU); compare the two L1 distances and explain why Jupiter's is so much larger despite Jupiter being much farther from the Sun.</li>
<li>Compute the ratio of Proxima Centauri's periastron distance to the Alpha Centauri AB semimajor axis, and state whether this hierarchy ratio is consistent with published long-term stability studies of the Alpha Centauri triple system.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The Hohmann transfer calculation assumes perfectly circular, coplanar orbits for both Earth and Mars; state explicitly which of the two assumptions (circular, coplanar) is least accurate for the real Earth-Mars system (recall Mars's actual eccentricity is about 0.093, ASTR120/ASTR320 territory) and what qualitative effect relaxing that assumption would have on the required &Delta;v.</p></section>
<section><h2>Deliverables</h2><ul><li>Full Hohmann transfer calculation (both burns, total &Delta;v, transfer time).</li><li>Sun-Earth and Sun-Jupiter L1 distance calculations with a written comparison.</li><li>Alpha Centauri AB-Proxima hierarchy-ratio calculation and stability discussion.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct vis-viva arithmetic at all four orbital points (Earth circular, transfer perihelion, transfer aphelion, Mars circular).</li><li>Correct transfer-time calculation using Kepler's third law in AU/yr units.</li><li>Correct L1 distance calculations for both Sun-Earth and Sun-Jupiter, with correct mass ratios.</li><li>Correct hierarchy-ratio arithmetic and a physically sound stability discussion.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 3.4-3.6.</li><li>Alpha Centauri AB and Proxima orbital elements: live-verified this session.</li></ul></section>
"""
    return lab_page(6, 'Interplanetary Transfer Orbits and Gravitational Hierarchy',
                     'Design a Hohmann transfer to Mars and evaluate Lagrange-point distances and hierarchical stability for a real triple star system.', sections)


# ---------------------------------------------------------------------------
# LAB 07: Capstone -- full characterization of Alpha Centauri AB
# ---------------------------------------------------------------------------
def make_lab_07() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This capstone lab has students reproduce every calculation used in Lecture 14's synthesis from the raw measured orbital elements and stellar parameters, combining the radiative (Lectures 01-02) and dynamical (Lectures 07-09) toolkits developed across the entire course, and add a new radiation-pressure check (Lecture 13).</p></section>
<section><h2>Materials and Data</h2><p>Use <code>../data/alpha_centauri_ab.csv</code> and <code>../data/alpha_centauri_orbit.csv</code> for all inputs; do not use any number not present in, or directly derivable from, these files and the physical constants used throughout the course.</p></section>
<section><h2>Procedure</h2><ol>
<li><strong>Radiative chain:</strong> compute the Stefan-Boltzmann luminosity for Alpha Centauri A and for Alpha Centauri B from their measured radii and temperatures, and compare each to its independently measured luminosity (percent agreement).</li>
<li><strong>Dynamical chain:</strong> compute the total system mass from Kepler's third law applied to the measured period and semimajor axis, and compare it to the independently measured sum of individual masses (percent agreement).</li>
<li><strong>Radiation-pressure check:</strong> compute the Eddington luminosity for each star using its own mass, and express each star's actual luminosity as a fraction (in percent, using scientific notation) of its own Eddington luminosity, confirming that radiation pressure is negligible for both stars.</li>
<li><strong>Synthesis:</strong> write a structured, 300-500 word synthesis addressing (a) which of your four percent-agreement checks in steps 1-2 is the strongest confirmation and why, (b) what shared assumption (if any) links the radiative and dynamical chains and therefore limits their mutual independence, and (c) what an astronomer would conclude if steps 1-2 had instead disagreed by, say, 25% rather than a few percent.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Both the radiative chain (which needs a physical radius, derived from angular diameter and distance) and the dynamical chain (which needs a physical semimajor axis, derived from angular separation and distance) depend on the same measured parallax/distance to Alpha Centauri. Explicitly identify this shared dependency in your synthesis paragraph (b) above.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed radiative-chain, dynamical-chain, and Eddington-luminosity calculations for both stars, with all unit conversions shown.</li><li>The 300-500 word structured synthesis paragraph.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct, fully shown arithmetic for all radiative, dynamical, and Eddington-luminosity calculations.</li><li>Synthesis paragraph correctly identifies the shared parallax/distance dependency as a limitation on the independence of the two chains.</li><li>Synthesis paragraph gives a physically sound account of what a large (25%) disagreement would imply (an error in one of the input measurements or an unmodeled physical effect, not simply "one method is right and one is wrong").</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 18 and Chapter 3 (read together, as in Lecture 14).</li><li>All Alpha Centauri AB data: live-verified this session.</li></ul></section>
"""
    return lab_page(7, 'Capstone: A Complete Physical Characterization of Alpha Centauri AB',
                     'Combine every radiative and dynamical tool from this course to fully characterize a real binary star system and reflect on independent verification.', sections)


LAB_BUILDERS = [make_lab_01, make_lab_02, make_lab_03, make_lab_04, make_lab_05, make_lab_06, make_lab_07]


def write_labs():
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    for i, builder in enumerate(LAB_BUILDERS, start=1):
        (LAB_DIR / f'lab-{i:02d}.html').write_text(builder(), encoding='utf-8')


# ---------------------------------------------------------------------------
# Real data used across problem sets (distinct from, but complementary to,
# the Alpha Centauri AB dataset used in the labs and lectures).
# ---------------------------------------------------------------------------
# Sirius A: standard published values (carried forward from ASTR230, where
# Sirius B's provenance was independently verified; Sirius A itself is a
# standard Hipparcos-era literature value, not re-verified this session).
SIRIUS_A_TEFF = 9940.0
SIRIUS_A_R_RSUN = 1.711
SIRIUS_A_L_LSUN_PUBLISHED = 25.4
# Sirius AB orbit: standard published visual-binary orbital elements.
SIRIUS_AB_PERIOD_YR = 50.13
SIRIUS_AB_SEMIMAJOR_AU = 19.78
SIRIUS_A_MASS_MSUN_PUBLISHED = 2.063
SIRIUS_B_MASS_MSUN = SIRIUS_B['mass_msun']
# 47 Tucanae: standard published globular-cluster values (flag for spot-check).
NGC104_SIGMA_KMS = 11.5
NGC104_HALF_LIGHT_PC = 3.8
NGC104_PUBLISHED_MASS_MSUN = 6.4e5
# Europa: standard published values (flag for spot-check).
EUROPA_MASS_KG = 4.7998e22
EUROPA_RADIUS_M = 1560.8e3
EUROPA_SEMIMAJOR_M = 671100e3
EUROPA_ECCENTRICITY = 0.009


def _sb_lum_lsun(r_rsun, teff):
    return stefan_boltzmann_luminosity_w(r_rsun * R_SUN_M, teff) / L_SUN_W


def _boltzmann_ratio(teff, delta_e_j=1.634e-18, g_ratio=4.0):
    return g_ratio * math.exp(-delta_e_j / (K_BOLTZMANN * teff))


SIRIUS_AB_TOTAL_MASS_KEPLER = kepler3_total_mass_msun(SIRIUS_AB_PERIOD_YR, SIRIUS_AB_SEMIMAJOR_AU)
SIRIUS_AB_TOTAL_MASS_MEASURED = SIRIUS_A_MASS_MSUN_PUBLISHED + SIRIUS_B_MASS_MSUN


# ---------------------------------------------------------------------------
# PS 01: Blackbody law -- Sirius A
# ---------------------------------------------------------------------------
def build_ps01():
    title = 'Blackbody Radiation: Wien\u2019s Law and Stefan-Boltzmann for Sirius A'
    reading = f'{OPENSTAX}, Chapter 5.4 and Chapter 18.1.'
    lam = wien_peak_wavelength_m(SIRIUS_A_TEFF) * 1e9
    l_sb = _sb_lum_lsun(SIRIUS_A_R_RSUN, SIRIUS_A_TEFF)
    p1 = problem(1, 'Wien\u2019s law for Sirius A',
                 f"<p>Sirius A has T_eff = {SIRIUS_A_TEFF:.0f} K (a standard published value; see reference-log.md). Using b = {WIEN_B:.4e} m&middot;K, compute Sirius A's peak emission wavelength in nanometers and state which part of the spectrum it falls in.</p>")
    p2 = problem(2, 'Stefan-Boltzmann luminosity for Sirius A',
                 f"<p>Sirius A has a measured radius of {SIRIUS_A_R_RSUN:.3f} R&#8857;. Compute its Stefan-Boltzmann luminosity in solar units, showing the full unit conversion from R&#8857; to meters.</p>")
    p3 = problem(3, 'Percent agreement',
                 f"<p>The independently published luminosity of Sirius A is about {SIRIUS_A_L_LSUN_PUBLISHED:.1f} L&#8857;. Compute the percent agreement between your Problem 2 answer and this value, and state one physical reason a small residual disagreement might remain (e.g., measurement uncertainty in R or T_eff, or a departure from a perfect blackbody spectrum).</p>")
    p4 = problem(4, 'Comparative reasoning',
                 f"<p>Sirius A (T_eff = {SIRIUS_A_TEFF:.0f} K, R = {SIRIUS_A_R_RSUN:.3f} R&#8857;) and Alpha Centauri A (T_eff = {ALPHA_CEN_A['teff']:.0f} K, R = {ALPHA_CEN_A['radius_rsun']:.3f} R&#8857;, from Lecture 02) have similar radii but very different temperatures. Using the R&sup2;T&#8308; scaling, explain quantitatively (with a computed ratio, not just words) why Sirius A is roughly {SIRIUS_A_L_LSUN_PUBLISHED/ALPHA_CEN_A['lum_lsun']:.0f} times more luminous than Alpha Centauri A despite only a factor of {SIRIUS_A_TEFF/ALPHA_CEN_A['teff']:.2f} difference in temperature.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Wien\u2019s law for Sirius A', f"<p>&lambda;_max = b/T = {WIEN_B:.4e}/{SIRIUS_A_TEFF:.0f} = {lam:.0f} nm, in the ultraviolet/blue-visible part of the spectrum, consistent with Sirius A's observed blue-white color.</p>", [('Correct formula and unit handling', 8), ('Correct spectral-region identification', 7)])
    sol2 = solution(2, 'Stefan-Boltzmann luminosity', f"<p>R = {SIRIUS_A_R_RSUN:.3f} &times; {R_SUN_M:.3e} m = {SIRIUS_A_R_RSUN*R_SUN_M:.3e} m. L = 4&pi;R&sup2;&sigma;T&#8308; = {_sb_lum_lsun(SIRIUS_A_R_RSUN, SIRIUS_A_TEFF)*L_SUN_W:.3e} W = {l_sb:.2f} L&#8857;.</p>", [('Correct unit conversion R&#8857; to m', 8), ('Correct final luminosity in solar units', 7)])
    sol3 = solution(3, 'Percent agreement', f"<p>Percent agreement = |{l_sb:.2f} &minus; {SIRIUS_A_L_LSUN_PUBLISHED:.1f}| / {SIRIUS_A_L_LSUN_PUBLISHED:.1f} &times; 100% = {abs(l_sb-SIRIUS_A_L_LSUN_PUBLISHED)/SIRIUS_A_L_LSUN_PUBLISHED*100:.1f}%. A residual difference this size is well within plausible measurement uncertainty in Sirius A's published radius and temperature.</p>", [('Correct percent-agreement arithmetic', 8), ('Valid physical reason for residual disagreement', 7)])
    sol4 = solution(4, 'Comparative reasoning', f"<p>L_Sirius/L_AlphaCenA &asymp; (R ratio)&sup2; &times; (T ratio)&#8308; = ({SIRIUS_A_R_RSUN/ALPHA_CEN_A['radius_rsun']:.3f})&sup2; &times; ({SIRIUS_A_TEFF/ALPHA_CEN_A['teff']:.3f})&#8308; = {(SIRIUS_A_R_RSUN/ALPHA_CEN_A['radius_rsun'])**2 * (SIRIUS_A_TEFF/ALPHA_CEN_A['teff'])**4:.1f}, close to the {SIRIUS_A_L_LSUN_PUBLISHED/ALPHA_CEN_A['lum_lsun']:.0f}&times; luminosity ratio quoted, showing the T&#8308; dependence dominates over the near-unity radius ratio.</p>", [('Correct computed ratio using R&sup2;T&#8308; scaling', 12), ('Correct identification that T&#8308; dominates', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 correct Wien\u2019s law application and spectral region.',
        'Problem 2: 15 points \u2014 correct unit conversion and Stefan-Boltzmann arithmetic.',
        'Problem 3: 15 points \u2014 correct percent-agreement calculation and a valid physical reason for residual disagreement.',
        'Problem 4: 20 points \u2014 correct computed R\u00b2T\u2074 ratio, not just a qualitative statement.',
    ]
    common_errors = [
        'Forgetting to convert solar radii to meters before applying the Stefan-Boltzmann formula.',
        'Reporting Problem 4 as a purely qualitative answer without the required computed ratio.',
        'Using Sirius B\u2019s parameters instead of Sirius A\u2019s by confusing the two stars.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


# ---------------------------------------------------------------------------
# PS 02: Optical depth and Boltzmann excitation for Vega
# ---------------------------------------------------------------------------
def build_ps02():
    title = 'Optical Depth Attenuation and the Boltzmann Equation for Vega'
    reading = f'{OPENSTAX}, Chapter 5.5 and Chapter 17.3.'
    vega_teff = 9602.0
    ratio_vega = _boltzmann_ratio(vega_teff)
    ratio_sun = _boltzmann_ratio(SUN_TEFF)
    p1 = problem(1, 'Transmitted fraction',
                 "<p>A stellar atmosphere layer has optical depth &tau; = 4.5 at a particular wavelength. Compute the transmitted intensity fraction I(&tau;)/I(0), and state what fraction of the incident intensity is absorbed or scattered away.</p>")
    p2 = problem(2, 'Matching optical depth to transmitted fraction',
                 "<p>A different wavelength shows a transmitted fraction of exactly 10% through the same physical layer. Solve for the optical depth &tau; at that wavelength (invert the exponential relationship), and state whether this wavelength has higher or lower opacity than the &tau; = 4.5 wavelength in Problem 1.</p>")
    p3 = problem(3, 'Boltzmann ratio for Vega',
                 f"<p>Vega has T_eff = {vega_teff:.0f} K (a standard published value). Using the hydrogen n=1&rarr;n=2 Boltzmann ratio (&Delta;E = 10.2 eV = 1.634 &times; 10&#8315;&sup1;&#8270; J, g2/g1 = 4), compute Vega's n2/n1 ratio and compare it (as a ratio, not just qualitatively) to the Sun's value ({SUN_TEFF:.0f} K) from Lecture 04/Lab 02.</p>", points=20)
    p4 = problem(4, 'Physical interpretation',
                 "<p>Vega is spectral type A0V and shows much stronger Balmer absorption lines than the Sun (G2V). Using your Problem 3 ratio, explain quantitatively why this is consistent with the Boltzmann-equation prediction, and state one piece of additional physics (not computed in this problem set) that would be needed to predict Balmer-line strength correctly for a star hotter than about 10,000 K.</p>")
    problems_html = p1 + p2 + p3 + p4
    frac1 = math.exp(-4.5)
    tau2 = -math.log(0.10)
    sol1 = solution(1, 'Transmitted fraction', f"<p>I(&tau;)/I(0) = e&#8315;&#8309;&middot;&#8309; = {frac1:.4f}, so about {frac1*100:.1f}% of the incident intensity is transmitted and about {(1-frac1)*100:.1f}% is absorbed or scattered away.</p>", [('Correct exponential arithmetic', 8), ('Correct percent-absorbed statement', 7)])
    sol2 = solution(2, 'Inverted optical depth', f"<p>0.10 = e&#8315;&#964; &rArr; &tau; = &minus;ln(0.10) = {tau2:.3f}. Since {tau2:.2f} &gt; 4.5, this wavelength has higher opacity (more absorbing/scattering material along the line of sight) than the &tau; = 4.5 wavelength in Problem 1.</p>", [('Correct inversion of the exponential relationship', 8), ('Correct higher/lower opacity comparison', 7)])
    sol3 = solution(3, 'Boltzmann ratio for Vega', f"<p>n2/n1 (Vega, {vega_teff:.0f} K) = {ratio_vega:.3e}; n2/n1 (Sun, {SUN_TEFF:.0f} K) = {ratio_sun:.3e}. Ratio = {ratio_vega/ratio_sun:.1f}, i.e., Vega's n=2 population fraction is about {ratio_vega/ratio_sun:.0f} times the Sun's.</p>", [('Correct Boltzmann-ratio arithmetic for Vega', 12), ('Correct computed ratio relative to the Sun', 8)])
    sol4 = solution(4, 'Physical interpretation', "<p>The much larger n2/n1 ratio at Vega's temperature directly predicts much stronger Balmer absorption, consistent with Vega's observed strong Balmer lines. Correctly predicting the further decline in Balmer strength above roughly 10,000 K requires the Saha equation (Lecture 04), which accounts for hydrogen ionization removing the bound electron needed for a Balmer transition.</p>", [('Correct quantitative connection to the computed ratio', 8), ('Correct identification of the Saha equation as the missing physics', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 correct exponential attenuation arithmetic.',
        'Problem 2: 15 points \u2014 correct inversion of the exponential relationship.',
        'Problem 3: 20 points \u2014 correct Boltzmann-ratio arithmetic and computed comparison ratio.',
        'Problem 4: 15 points \u2014 correct quantitative connection and correct identification of the Saha equation.',
    ]
    common_errors = [
        'Using a linear rather than exponential relationship between transmitted fraction and optical depth.',
        'Reporting Problem 3 only qualitatively without the required numeric ratio.',
        'Confusing the Boltzmann equation (excitation) with the Saha equation (ionization) when explaining the missing physics in Problem 4.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


# ---------------------------------------------------------------------------
# PS 03: Hydrostatic equilibrium (Alpha Cen A) and virial theorem (47 Tucanae)
# ---------------------------------------------------------------------------
def build_ps03():
    title = 'Hydrostatic Equilibrium for Alpha Centauri A and the Virial Mass of 47 Tucanae'
    reading = f'{OPENSTAX}, Chapter 15.4-15.5.'
    m_a_kg = ALPHA_CEN_A['mass_msun'] * M_SUN_KG
    r_a_m = ALPHA_CEN_A['radius_rsun'] * R_SUN_M
    p_c_a = hydrostatic_central_pressure_pa(m_a_kg, r_a_m)
    t_c_a = virial_core_temperature_k(m_a_kg, r_a_m)
    m_ngc104 = virial_mass_msun(NGC104_SIGMA_KMS, NGC104_HALF_LIGHT_PC)
    p1 = problem(1, 'Central pressure of Alpha Centauri A',
                 f"<p>Using P_c &asymp; (3/8&pi;)GM&sup2;/R&#8308;, estimate the central pressure of Alpha Centauri A (M = {ALPHA_CEN_A['mass_msun']:.4f} M&#8857;, R = {ALPHA_CEN_A['radius_rsun']:.3f} R&#8857;), showing all unit conversions.</p>")
    p2 = problem(2, 'Comparison to the Sun',
                 f"<p>Compare your Problem 1 answer to the Sun's estimated central pressure from Lecture 05/Lab 03 ({SUN_CENTRAL_PRESSURE_EST:.3e} Pa), and explain, using the P_c &prop; M&sup2;/R&#8308; scaling, why Alpha Centauri A's slightly larger mass and radius than the Sun's produce the sign and rough size of the difference you find.</p>")
    p3 = problem(3, 'Virial mass of 47 Tucanae',
                 f"<p>The globular cluster 47 Tucanae has a published core velocity dispersion of {NGC104_SIGMA_KMS:.1f} km/s and a half-light radius of {NGC104_HALF_LIGHT_PC:.1f} pc. Using M &asymp; 5&sigma;&sup2;R_h/G, estimate its virial mass in solar masses.</p>", points=20)
    p4 = problem(4, 'Agreement check',
                 f"<p>The commonly cited dynamical mass of 47 Tucanae is about {NGC104_PUBLISHED_MASS_MSUN:.1e} M&#8857;. Compute the percent agreement with your Problem 3 answer, and state whether this level of agreement is consistent with the same order-of-magnitude uncertainty seen for M15 in Lab 03.</p>")
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Central pressure', f"<p>M = {m_a_kg:.4e} kg, R = {r_a_m:.4e} m. P_c = (3/8&pi;)GM&sup2;/R&#8308; = {p_c_a:.3e} Pa.</p>", [('Correct unit conversions', 8), ('Correct final pressure', 7)])
    sol2 = solution(2, 'Comparison to the Sun', f"<p>Alpha Centauri A's estimated central pressure ({p_c_a:.3e} Pa) is {p_c_a/SUN_CENTRAL_PRESSURE_EST:.2f} times the Sun's ({SUN_CENTRAL_PRESSURE_EST:.3e} Pa). Because P_c &prop; M&sup2;/R&#8308;, and Alpha Centauri A has both larger mass (raising P_c) and larger radius (lowering P_c, more strongly since R is raised to the fourth power), the net effect and its sign depend on which scaling dominates; the computed ratio above shows which one wins for these specific values.</p>", [('Correct computed ratio', 8), ('Correct qualitative M vs. R\u2074 scaling argument', 7)])
    sol3 = solution(3, 'Virial mass of 47 Tucanae', f"<p>M &asymp; 5&sigma;&sup2;R_h/G = {m_ngc104:.3e} M&#8857;.</p>", [('Correct unit conversions (km/s to m/s, pc to m)', 12), ('Correct final virial mass', 8)])
    sol4 = solution(4, 'Agreement check', f"<p>Percent agreement = |{m_ngc104:.2e} &minus; {NGC104_PUBLISHED_MASS_MSUN:.2e}| / {NGC104_PUBLISHED_MASS_MSUN:.2e} &times; 100% = {abs(m_ngc104-NGC104_PUBLISHED_MASS_MSUN)/NGC104_PUBLISHED_MASS_MSUN*100:.1f}%, a similar order-of-magnitude level of agreement to the M15 case in Lab 03, consistent with the single-mass virial estimator being a genuine but approximate (not exact) mass estimator for real, non-uniform clusters.</p>", [('Correct percent-agreement arithmetic', 8), ('Correct comparison to the M15 precedent', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 correct unit conversions and central-pressure arithmetic.',
        'Problem 2: 15 points \u2014 correct computed ratio and correct M vs. R\u2074 scaling reasoning.',
        'Problem 3: 20 points \u2014 correct unit conversions and virial-mass arithmetic.',
        'Problem 4: 15 points \u2014 correct percent-agreement arithmetic and comparison to the M15 precedent.',
    ]
    common_errors = [
        'Forgetting to convert R\u2609 to meters (fourth-power sensitivity makes this error especially large here).',
        'Forgetting to convert km/s to m/s before squaring in the virial-mass formula.',
        'Treating a 20-40% agreement as a failure of the virial theorem rather than an expected limitation of the uniform-density/single-mass approximations.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


# ---------------------------------------------------------------------------
# PS 04: Kepler's third law for the Sirius AB system
# ---------------------------------------------------------------------------
def build_ps04():
    title = 'Weighing the Sirius AB System with Kepler\u2019s Third Law'
    reading = f'{OPENSTAX}, Chapter 3.1-3.3.'
    p1 = problem(1, 'Unit conversion',
                 f"<p>The Sirius AB system has an orbital period of {SIRIUS_AB_PERIOD_YR:.2f} years and a semimajor axis of {SIRIUS_AB_SEMIMAJOR_AU:.2f} AU (standard published visual-binary orbital elements). Convert both quantities to SI units (seconds and meters).</p>")
    p2 = problem(2, 'Total mass from Kepler\u2019s third law',
                 "<p>Using your Problem 1 results and the generalized Kepler's third law, compute the total mass of the Sirius AB system in solar masses.</p>", points=20)
    p3 = problem(3, 'Comparison to individually measured masses',
                 f"<p>Sirius A's individually measured mass is about {SIRIUS_A_MASS_MSUN_PUBLISHED:.3f} M&#8857; and Sirius B's (from ASTR230, independently verified) is {SIRIUS_B_MASS_MSUN:.3f} M&#8857;. Compute the percent agreement between the sum of these and your Problem 2 answer.</p>")
    p4 = problem(4, 'Escape velocity contrast',
                 f"<p>Using Sirius B's mass ({SIRIUS_B_MASS_MSUN:.3f} M&#8857;) and radius ({SIRIUS_B['radius_rsun']:.6f} R&#8857;), compute its surface escape velocity, and compare it (as a ratio) to Sirius A's surface escape velocity (M = {SIRIUS_A_MASS_MSUN_PUBLISHED:.3f} M&#8857;, R = {SIRIUS_A_R_RSUN:.3f} R&#8857;). Explain the physical reason for the large contrast, referencing Lecture 07.</p>")
    problems_html = p1 + p2 + p3 + p4
    p_s = SIRIUS_AB_PERIOD_YR * YEAR_S
    a_m = SIRIUS_AB_SEMIMAJOR_AU * AU_M
    v_esc_a = escape_velocity_ms(SIRIUS_A_MASS_MSUN_PUBLISHED * M_SUN_KG, SIRIUS_A_R_RSUN * R_SUN_M) / KM
    v_esc_b = escape_velocity_ms(SIRIUS_B_MASS_MSUN * M_SUN_KG, SIRIUS_B['radius_rsun'] * R_SUN_M) / KM
    sol1 = solution(1, 'Unit conversion', f"<p>P = {SIRIUS_AB_PERIOD_YR:.2f} yr &times; {YEAR_S:.4e} s/yr = {p_s:.4e} s. a = {SIRIUS_AB_SEMIMAJOR_AU:.2f} AU &times; {AU_M:.4e} m/AU = {a_m:.4e} m.</p>", [('Correct period conversion', 8), ('Correct semimajor-axis conversion', 7)])
    sol2 = solution(2, 'Total mass', f"<p>(m1+m2) = 4&pi;&sup2;a&sup3;/(GP&sup2;) = {SIRIUS_AB_TOTAL_MASS_KEPLER:.3f} M&#8857;.</p>", [('Correct formula setup with converted units', 12), ('Correct final total mass', 8)])
    sol3 = solution(3, 'Comparison', f"<p>Sum of individual masses = {SIRIUS_A_MASS_MSUN_PUBLISHED:.3f} + {SIRIUS_B_MASS_MSUN:.3f} = {SIRIUS_AB_TOTAL_MASS_MEASURED:.3f} M&#8857;. Percent agreement with the Kepler total ({SIRIUS_AB_TOTAL_MASS_KEPLER:.3f} M&#8857;) = {abs(SIRIUS_AB_TOTAL_MASS_KEPLER-SIRIUS_AB_TOTAL_MASS_MEASURED)/SIRIUS_AB_TOTAL_MASS_MEASURED*100:.1f}%.</p>", [('Correct sum of individual masses', 8), ('Correct percent-agreement arithmetic', 7)])
    sol4 = solution(4, 'Escape velocity contrast', f"<p>v_esc(Sirius A) = {v_esc_a:.1f} km/s; v_esc(Sirius B) = {v_esc_b:.0f} km/s, a ratio of {v_esc_b/v_esc_a:.0f}. Sirius B has less than half of Sirius A's mass yet a radius over 200 times smaller, and because v_esc &prop; 1/&radic;R at fixed mass (and Sirius B's mass is not even fixed, only modestly smaller), its escape velocity is far higher \u2014 exactly the 1/&radic;R sensitivity emphasized in Lecture 07.</p>", [('Correct escape-velocity arithmetic for both stars', 8), ('Correct physical explanation referencing 1/\u221aR scaling', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 correct unit conversions.',
        'Problem 2: 20 points \u2014 correct Kepler\u2019s-third-law setup and arithmetic.',
        'Problem 3: 15 points \u2014 correct percent-agreement calculation.',
        'Problem 4: 15 points \u2014 correct escape-velocity arithmetic and correct physical explanation.',
    ]
    common_errors = [
        'Using years and AU directly in the SI-unit form of Kepler\u2019s third law without converting to seconds and meters.',
        'Confusing Sirius A and Sirius B\u2019s masses/radii when computing escape velocity.',
        'Attributing the escape-velocity contrast to mass alone rather than the dominant radius (1/\u221aR) effect.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


# ---------------------------------------------------------------------------
# PS 05: Mass-ratio splitting and Europa's Roche limit / tidal acceleration
# ---------------------------------------------------------------------------
def build_ps05():
    title = 'Mass-Ratio Splitting and Tidal Effects at Europa'
    reading = f'{OPENSTAX}, Chapter 18.4-18.5 and Chapter 3.6.'
    europa_density = EUROPA_MASS_KG / ((4.0 / 3.0) * math.pi * EUROPA_RADIUS_M ** 3)
    europa_roche = roche_limit_m(JUPITER_MASS_KG, EUROPA_RADIUS_M, JUPITER_MEAN_DENSITY, europa_density)
    europa_tidal = tidal_acceleration_diff(JUPITER_MASS_KG, EUROPA_SEMIMAJOR_M, EUROPA_RADIUS_M)
    p1 = problem(1, 'Splitting the Sirius AB total mass',
                 f"<p>Using your Kepler-derived Sirius AB total mass from Problem Set 04 ({SIRIUS_AB_TOTAL_MASS_KEPLER:.3f} M&#8857;) and the independently measured mass ratio M_B/M_A = {SIRIUS_B_MASS_MSUN/SIRIUS_A_MASS_MSUN_PUBLISHED:.4f}, split the total mass into individual masses for Sirius A and Sirius B.</p>", points=20)
    p2 = problem(2, 'Europa\u2019s Roche limit',
                 f"<p>Europa (M = {EUROPA_MASS_KG:.4e} kg, R = {EUROPA_RADIUS_M:.4e} m) orbits Jupiter (mean density {JUPITER_MEAN_DENSITY:.0f} kg/m&sup3;) at a semimajor axis of {EUROPA_SEMIMAJOR_M/1000:.0f} km. Compute Europa's mean density, then its rigid-body Roche limit around Jupiter, and state whether Europa is safely outside its own Roche limit.</p>")
    p3 = problem(3, 'Europa\u2019s tidal acceleration',
                 "<p>Compute Europa's own surface gravity (g = GM_Europa/R_Europa\u00b2) and the differential tidal acceleration across Europa due to Jupiter, and express the tidal acceleration as a percentage of Europa's own surface gravity. Compare your result (as a ratio) to Io's tidal-acceleration-to-surface-gravity percentage from Lecture 10/Lab 05, and state which moon experiences the stronger relative tidal stress and why (consider both distance and radius).</p>", points=20)
    p4 = problem(4, 'Physical interpretation',
                 "<p>Europa, like Io, is held in a slightly eccentric orbit by the same Laplace orbital resonance (with Io and Ganymede). Europa is thought to have a subsurface liquid water ocean, plausibly maintained partly by tidal heating. Using your Problem 3 comparison to Io, explain qualitatively why Europa's tidal heating is expected to be significant but weaker than Io's, consistent with Europa showing an icy (not volcanically resurfaced) surface.</p>")
    problems_html = p1 + p2 + p3 + p4
    ratio_ab = SIRIUS_B_MASS_MSUN / SIRIUS_A_MASS_MSUN_PUBLISHED
    m_a_split = SIRIUS_AB_TOTAL_MASS_KEPLER / (1 + ratio_ab)
    m_b_split = SIRIUS_AB_TOTAL_MASS_KEPLER - m_a_split
    sol1 = solution(1, 'Mass-ratio splitting', f"<p>M_A = total/(1+ratio) = {m_a_split:.3f} M&#8857;; M_B = total &minus; M_A = {m_b_split:.3f} M&#8857;, consistent with the independently quoted masses.</p>", [('Correct splitting formula setup', 12), ('Correct individual masses', 8)])
    sol2 = solution(2, 'Europa\u2019s Roche limit', f"<p>&rho;_Europa = {europa_density:.0f} kg/m&sup3;. Roche limit &asymp; {europa_roche/1000:.0f} km. Europa's actual orbital distance ({EUROPA_SEMIMAJOR_M/1000:.0f} km) is about {EUROPA_SEMIMAJOR_M/europa_roche:.1f} times the Roche limit, safely outside it.</p>", [('Correct density calculation', 8), ('Correct Roche-limit calculation and comparison', 7)])
    europa_gravity = G_NEWTON * EUROPA_MASS_KG / (EUROPA_RADIUS_M ** 2)
    sol3 = solution(3, 'Europa\u2019s tidal acceleration', f"<p>Europa's surface gravity: g = GM_Europa/R_Europa\u00b2 = {europa_gravity:.3f} m/s\u00b2. &Delta;a(Europa) = {europa_tidal:.3e} m/s\u00b2 = {europa_tidal/europa_gravity*100:.2f}% of Europa's own surface gravity. Io's corresponding fraction (Lecture 10/Lab 05) is {IO_TIDAL_ACCEL/IO_SURFACE_GRAVITY_MS2*100:.2f}% of Io's own surface gravity. Io experiences the stronger relative tidal stress, because Io orbits much closer to Jupiter and tidal acceleration falls off as 1/d\u00b3, more steeply than the modest difference in the two moons' surface gravities can offset.</p>", [('Correct surface-gravity and tidal-acceleration calculation for Europa', 12), ('Correct percentage comparison and correct 1/d\u00b3 explanation', 8)])
    sol4 = solution(4, 'Physical interpretation', "<p>Because tidal acceleration falls steeply (as 1/d\u00b3) with orbital distance and Europa orbits substantially farther from Jupiter than Io, Europa's tidal flexing and resulting heating is weaker than Io's, consistent with Europa retaining an icy crust (implying much less surface heat flow than Io's continuous resurfacing by active volcanism) while still plausibly sustaining a subsurface ocean from a smaller but non-negligible tidal heat source.</p>", [('Correct qualitative reasoning tied to the computed ratio', 15)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 20 points \u2014 correct mass-ratio splitting arithmetic.',
        'Problem 2: 15 points \u2014 correct density and Roche-limit arithmetic.',
        'Problem 3: 20 points \u2014 correct tidal-acceleration arithmetic and correct ratio comparison to Io.',
        'Problem 4: 15 points \u2014 physically sound qualitative reasoning tied to the computed ratio, not a generic restatement of the lecture.',
    ]
    common_errors = [
        'Confusing which moon (Io vs. Europa) has the larger tidal acceleration without checking the computed ratio.',
        'Computing Roche limit using Europa\u2019s mass instead of Jupiter\u2019s mass/density as the primary.',
        'Treating Problem 4 as requiring new calculation rather than qualitative reasoning from the already-computed Problem 3 ratio.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


# ---------------------------------------------------------------------------
# PS 06: Hohmann transfer to Venus and Lagrange-point comparison
# ---------------------------------------------------------------------------
def build_ps06():
    title = 'A Hohmann Transfer to Venus and the Sun-Earth vs. Sun-Jupiter L1 Points'
    reading = f'{OPENSTAX}, Chapter 3.4-3.6.'
    venus_a_au = 0.7233
    transfer_a_au = 0.5 * (EARTH_A_AU + venus_a_au)
    v_transfer_peri = vis_viva_speed_ms(MU_SUN, venus_a_au * AU_M, transfer_a_au * AU_M) / KM
    v_venus_circular = math.sqrt(MU_SUN / (venus_a_au * AU_M)) / KM
    dv2_venus = abs(v_venus_circular - v_transfer_peri)
    v_transfer_apo = vis_viva_speed_ms(MU_SUN, EARTH_A_AU * AU_M, transfer_a_au * AU_M) / KM
    dv1_venus = abs(V_EARTH_CIRCULAR - v_transfer_apo)
    transfer_time_venus = 0.5 * math.sqrt(transfer_a_au ** 3)
    jupiter_a_au = 5.2044
    sun_jupiter_l1_km = jupiter_a_au * AU_M * (JUPITER_MASS_KG / (3 * M_SUN_KG)) ** (1.0 / 3.0) / KM
    p1 = problem(1, 'Transfer orbit setup',
                 f"<p>Design a Hohmann transfer from Earth (a = {EARTH_A_AU:.4f} AU) to Venus (a = {venus_a_au:.4f} AU). Compute the transfer orbit's semimajor axis and its perihelion and aphelion distances.</p>")
    p2 = problem(2, 'Both burns',
                 "<p>Compute both required velocity changes (&Delta;v1 leaving Earth's orbit, &Delta;v2 arriving at Venus's orbit) using the vis-viva equation, and compute the total mission &Delta;v.</p>", points=20)
    p3 = problem(3, 'Transfer time',
                 "<p>Compute the one-way transfer time in days, and compare it (as a ratio) to the Earth-Mars transfer time computed in Lab 06, explaining why the Venus transfer is shorter.</p>")
    p4 = problem(4, 'Sun-Jupiter L1',
                 f"<p>Using r_L1 &asymp; R(m2/3m1)^(1/3), compute the Sun-Jupiter L1 distance (Jupiter's orbital radius is {jupiter_a_au:.4f} AU) and compare it (as a ratio) to the Sun-Earth L1 distance from Lecture 12/Lab 06. Explain why the ratio is much larger than the simple ratio of Jupiter's to Earth's orbital radii alone.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Transfer orbit setup', f"<p>a_transfer = 0.5(1.0000 + {venus_a_au:.4f}) = {transfer_a_au:.4f} AU. Perihelion = {venus_a_au:.4f} AU (Venus's orbit), aphelion = 1.0000 AU (Earth's orbit).</p>", [('Correct transfer semimajor axis', 8), ('Correct identification of perihelion/aphelion', 7)])
    sol2 = solution(2, 'Both burns', f"<p>&Delta;v1 (leaving Earth, at transfer aphelion) = |{V_EARTH_CIRCULAR:.2f} &minus; {v_transfer_apo:.2f}| = {dv1_venus:.2f} km/s. &Delta;v2 (arriving at Venus, at transfer perihelion) = |{v_venus_circular:.2f} &minus; {v_transfer_peri:.2f}| = {dv2_venus:.2f} km/s. Total &Delta;v = {dv1_venus+dv2_venus:.2f} km/s.</p>", [('Correct vis-viva speeds at both transfer points', 12), ('Correct \u0394v arithmetic and total', 8)])
    sol3 = solution(3, 'Transfer time', f"<p>t = 0.5 &times; a_transfer^1.5 = {transfer_time_venus:.3f} yr = {transfer_time_venus*365.25:.0f} days, shorter than the Earth-Mars transfer time ({HOHMANN_TRANSFER_TIME_YR*365.25:.0f} days) by a ratio of {(HOHMANN_TRANSFER_TIME_YR*365.25)/(transfer_time_venus*365.25):.2f}, because the Venus transfer orbit has a smaller semimajor axis and Kepler's third law gives shorter periods for smaller orbits.</p>", [('Correct transfer-time arithmetic', 8), ('Correct comparison and explanation', 7)])
    sol4 = solution(4, 'Sun-Jupiter L1', f"<p>r_L1(Sun-Jupiter) = {jupiter_a_au:.4f} AU &times; ({JUPITER_MASS_KG:.3e}/(3&times;{M_SUN_KG:.3e}))^(1/3) &times; (AU in km) = {sun_jupiter_l1_km:.3e} km, versus {SUN_EARTH_L1_KM:.3e} km for Sun-Earth, a ratio of {sun_jupiter_l1_km/SUN_EARTH_L1_KM:.1f}. This is much larger than the orbital-radius ratio ({jupiter_a_au/EARTH_A_AU:.2f}) alone because r_L1 also scales with (mass ratio)^(1/3), and Jupiter's mass ratio to the Sun is far larger than Earth's, so both factors increase the Jupiter L1 distance relative to a naive orbital-radius-only scaling.</p>", [('Correct L1 arithmetic for Sun-Jupiter', 12), ('Correct explanation combining both R and mass-ratio scaling', 8)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 correct transfer semimajor axis and perihelion/aphelion identification.',
        'Problem 2: 20 points \u2014 correct vis-viva arithmetic at both transfer points and correct total \u0394v.',
        'Problem 3: 15 points \u2014 correct transfer-time arithmetic and correct comparison.',
        'Problem 4: 20 points \u2014 correct Sun-Jupiter L1 arithmetic and correct combined-scaling explanation.',
    ]
    common_errors = [
        'Reversing which orbit (Earth\u2019s or Venus\u2019s) is the transfer-orbit perihelion versus aphelion for an inward transfer.',
        'Forgetting the cube-root mass-ratio scaling and attributing the Sun-Jupiter/Sun-Earth L1 ratio to orbital radius alone.',
        'Using inconsistent units (AU vs. km) when comparing the two L1 distances.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


# ---------------------------------------------------------------------------
# PS 07: Capstone synthesis for the Sirius AB system
# ---------------------------------------------------------------------------
def build_ps07():
    title = 'Capstone Synthesis: Radiative and Dynamical Cross-Checks for Sirius AB'
    reading = f'{OPENSTAX}, Chapter 18 and Chapter 3 (read together, as in Lecture 14).'
    l_sb_a = _sb_lum_lsun(SIRIUS_A_R_RSUN, SIRIUS_A_TEFF)
    sirius_b_l_sb = _sb_lum_lsun(SIRIUS_B['radius_rsun'], SIRIUS_B['teff'])
    sirius_b_l_published = 0.0245
    edd_a = eddington_luminosity_w(SIRIUS_A_MASS_MSUN_PUBLISHED * M_SUN_KG) / L_SUN_W
    edd_b = eddington_luminosity_w(SIRIUS_B_MASS_MSUN * M_SUN_KG) / L_SUN_W
    p1 = problem(1, 'Radiative chain for Sirius A and B',
                 f"<p>Compute the Stefan-Boltzmann luminosity for Sirius A (T_eff = {SIRIUS_A_TEFF:.0f} K, R = {SIRIUS_A_R_RSUN:.3f} R&#8857;) and for Sirius B (T_eff = {SIRIUS_B['teff']:.0f} K, R = {SIRIUS_B['radius_rsun']:.6f} R&#8857;), and compare each to its published luminosity ({SIRIUS_A_L_LSUN_PUBLISHED:.1f} L&#8857; and {sirius_b_l_published:.4f} L&#8857; respectively).</p>", points=25)
    p2 = problem(2, 'Dynamical chain',
                 f"<p>Using your Problem Set 04 result for the Sirius AB total mass from Kepler's third law ({SIRIUS_AB_TOTAL_MASS_KEPLER:.3f} M&#8857;), restate the percent agreement with the independently measured mass sum ({SIRIUS_AB_TOTAL_MASS_MEASURED:.3f} M&#8857;) found there.</p>")
    p3 = problem(3, 'Eddington luminosity check',
                 f"<p>Compute the Eddington luminosity for Sirius A and for Sirius B using their individually measured masses, and express each star's actual (published) luminosity as a percentage of its own Eddington luminosity.</p>", points=20)
    p4 = problem(4, 'Synthesis paragraph',
                 "<p>Write a 250-400 word synthesis addressing: (a) which of your radiative or dynamical cross-checks (Problems 1-2) shows the closer agreement and why that might be, (b) whether Sirius B's white-dwarf structure makes the Stefan-Boltzmann cross-check in Problem 1 any less valid than for an ordinary main-sequence star like Sirius A, and (c) what your Problem 3 result implies about whether radiation pressure plays any role in either star's hydrostatic balance.</p>", points=20)
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Radiative chain', f"<p>Sirius A: L_SB = {l_sb_a:.2f} L&#8857; vs. published {SIRIUS_A_L_LSUN_PUBLISHED:.1f} L&#8857; (agreement {abs(l_sb_a-SIRIUS_A_L_LSUN_PUBLISHED)/SIRIUS_A_L_LSUN_PUBLISHED*100:.1f}%). Sirius B: L_SB = {sirius_b_l_sb:.4f} L&#8857; vs. published {sirius_b_l_published:.4f} L&#8857; (agreement {abs(sirius_b_l_sb-sirius_b_l_published)/sirius_b_l_published*100:.1f}%).</p>", [('Correct Sirius A calculation and agreement', 12), ('Correct Sirius B calculation and agreement', 13)])
    sol2 = solution(2, 'Dynamical chain', f"<p>Percent agreement = {abs(SIRIUS_AB_TOTAL_MASS_KEPLER-SIRIUS_AB_TOTAL_MASS_MEASURED)/SIRIUS_AB_TOTAL_MASS_MEASURED*100:.1f}% (restated from Problem Set 04).</p>", [('Correct restatement/consistency with PS04', 15)])
    sol3 = solution(3, 'Eddington check', f"<p>L_Edd(Sirius A, {SIRIUS_A_MASS_MSUN_PUBLISHED:.3f} M&#8857;) = {edd_a:.2e} L&#8857;; actual/Eddington = {SIRIUS_A_L_LSUN_PUBLISHED/edd_a*100:.2e}%. L_Edd(Sirius B, {SIRIUS_B_MASS_MSUN:.3f} M&#8857;) = {edd_b:.2e} L&#8857;; actual/Eddington = {sirius_b_l_published/edd_b*100:.2e}%. Both are minuscule fractions, confirming radiation pressure is negligible for both stars.</p>", [('Correct Eddington-luminosity arithmetic for both stars', 12), ('Correct percentage-of-Eddington calculation for both', 8)])
    sol4 = solution(4, 'Synthesis paragraph', "<p>Full credit requires: (a) an explicit numeric comparison of the two agreement percentages with a plausible reason for any difference (e.g., different sensitivity to measurement uncertainty in R vs. in P and a); (b) a correct statement that Sirius B's degenerate-matter structure does not undermine the purely radiative (surface-emission) Stefan-Boltzmann argument, which depends only on the emitting surface's R and T, not on what supports the star's interior; (c) a correct conclusion that both stars' actual luminosities are far below their Eddington limits, so radiation pressure is negligible in the hydrostatic balance of both, consistent with Lecture 05's ideal-gas treatment.</p>", [('Correct point (a)', 7), ('Correct point (b)', 7), ('Correct point (c)', 6)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 25 points \u2014 correct Stefan-Boltzmann arithmetic and agreement percentages for both stars.',
        'Problem 2: 15 points \u2014 correct, consistent restatement of the Problem Set 04 result.',
        'Problem 3: 20 points \u2014 correct Eddington-luminosity arithmetic and percentage-of-Eddington for both stars.',
        'Problem 4: 20 points \u2014 synthesis paragraph addresses all three required points with correct physical reasoning, not generic restatement.',
    ]
    common_errors = [
        'Confusing Sirius A and Sirius B\u2019s radii (differing by more than two orders of magnitude) when computing Stefan-Boltzmann luminosity.',
        'Concluding that Sirius B\u2019s degenerate structure invalidates the Stefan-Boltzmann surface-emission argument (it does not; only the interior support mechanism differs).',
        'Treating point (c) of the synthesis paragraph as requiring new calculation rather than interpretation of the already-computed Problem 3 results.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


PSET_BUILDERS = [build_ps01, build_ps02, build_ps03, build_ps04, build_ps05, build_ps06, build_ps07]


def write_psets():
    PSET_DIR.mkdir(parents=True, exist_ok=True)
    for i, builder in enumerate(PSET_BUILDERS, start=1):
        title, reading, problems_html, solutions_html, criteria, common_errors = builder()
        (PSET_DIR / f'problem-set-{i:02d}.html').write_text(pset_page(i, title, f'Problem set for Unit {i}.', problems_html, reading), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-solutions.html').write_text(solutions_page(i, title, solutions_html), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-assessment.md').write_text(assessment_md(i, title, criteria, common_errors), encoding='utf-8')


if __name__ == '__main__':
    write_labs()
    write_psets()
    print(f'Wrote {len(LAB_BUILDERS)} labs and {len(PSET_BUILDERS)} problem sets (+ solutions + assessment instructions).')

