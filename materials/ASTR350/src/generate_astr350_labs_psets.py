"""Lab and problem-set generator for ASTR350.

Depends on the shared constants and page()/CSS helpers in
generate_astr350_content.py so every number here traces back to the same
real exoplanet datasets (51 Pegasi b, HD 209458 b, TRAPPIST-1, extremophile
records) used in the paired lectures. Run with the project interpreter:
    python materials/ASTR350/src/generate_astr350_content.py
    python materials/ASTR350/src/generate_astr350_labs_psets.py
"""
from __future__ import annotations

import math
from html import escape

from generate_astr350_content import (
    CSS, page, li, LAB_DIR, PSET_DIR, DATA_DIR, fmt,
    G_CONST, C_LIGHT, H_PLANCK, K_BOLTZMANN, SIGMA_SB, AU_M, DAY_S, YEAR_S,
    M_SUN, R_SUN, L_SUN, M_EARTH, R_EARTH, M_JUP, R_JUP, AMU, S_EARTH_W_M2,
    STAR_51PEG, PLANET_51PEGB, STAR_HD209458, PLANET_HD209458B,
    TRAPPIST1_STAR, TRAPPIST1_PLANETS, ECCENTRIC_PLANETS, SOLAR_SYSTEM,
    HZ_S_INNER, HZ_S_OUTER, EXTREMOPHILES, HUMAN_LETHAL_RADIATION_GY,
    MILLER_UREY_RELATIVE_YIELD, OPENSTAX_NOTE,
    kepler_semimajor_axis_m, rv_semi_amplitude_m_s, rv_minimum_mass_kg,
    transit_depth, transit_duration_hr, equilibrium_temperature_k, insolation_w_m2,
    hz_boundaries_au, scale_height_m, jeans_escape_parameter, surface_gravity, drake_n,
    MSTAR_51PEG_KG, MP_51PEGB_TRUE_KG, P_51PEGB_S, A_51PEGB_M, K_51PEGB_PREDICTED,
    MP_SINI_51PEGB_FROM_K_KG, MP_SINI_51PEGB_MJUP, MP_TRUE_51PEGB_FROM_SINI_MJUP,
    MSTAR_HD209458_KG, MP_HD209458B_KG, RSTAR_HD209458_M, RP_HD209458B_M, P_HD209458B_S,
    A_HD209458B_M, TRANSIT_DEPTH_HD209458B_COMPUTED, TRANSIT_DURATION_HD209458B_COMPUTED,
    K_HD209458B_PREDICTED, HD209458B_DENSITY_KG_M3, HD209458B_SURFACE_G,
    HD209458B_SCALE_HEIGHT_H2_M, HD209458B_JEANS_PARAM, HD209458B_MASS_LOSS_TIMESCALE_GYR,
    TRAPPIST1_LUM_W, TRAPPIST1_TEQ, TRAPPIST1_DENSITY_KG_M3,
    TRAPPIST1_HZ_INNER_AU, TRAPPIST1_HZ_OUTER_AU, SUN_HZ_INNER_AU, SUN_HZ_OUTER_AU,
    EARTH_EQ_TEMP_K, EARTH_INSOLATION, MOIST_GREENHOUSE_MARGIN_TRAPPIST1E,
    DRAKE_R_STAR, DRAKE_F_P, DRAKE_N_E, DRAKE_F_L_OPTIMISTIC, DRAKE_F_L_PESSIMISTIC,
    DRAKE_F_I, DRAKE_F_C, DRAKE_L_OPTIMISTIC_YR, DRAKE_L_PESSIMISTIC_YR,
    N_CIV_OPTIMISTIC, N_CIV_PESSIMISTIC,
)

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
    return page(f'ASTR 350 Lab {n:02d}', body)


def pset_page(n: int, title: str, focus: str, problems_html: str, reading: str) -> str:
    body = f"""<header><div><h1>ASTR 350 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header>
<main><section><h2>Problems</h2>{problems_html}</section>
<section><h2>Due and Scope</h2><p>Submit a complete derivation with equations, units, labeled quantities, and a short narrative interpretation for each problem. Show every step; a correct final number without a visible derivation receives partial credit at most, and quoting a lecture number without adapting it to this problem's specific inputs receives no credit for that step.</p></section>
<section><h2>OpenStax Companion Reading</h2><p>{escape(reading)}</p></section>
<section><h2>References and Data Sources</h2><ul><li>Corresponding lecture slides and notes for this unit.</li><li>{OPENSTAX}</li><li>Course datasets under <code>materials/ASTR350/data/</code> where referenced above.</li></ul></section>
</main>"""
    return page(f'ASTR 350 Problem Set {n:02d}', body)


def solutions_page(n: int, title: str, solutions_html: str) -> str:
    body = f"<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header><main><section><h2>Worked Solutions</h2>{solutions_html}</section><section><h2>Grading Notes</h2><p>Award full marks for correct method, units, and a numeric result consistent with the arithmetic shown (allow reasonable rounding). Verify that the student re-derives the number for this problem's specific inputs rather than quoting a lecture example without adaptation. Watch specifically for unit-conversion errors (AU/m, days/seconds, Jupiter/Earth mass-radius units), for comparative-magnitude statements given in the wrong direction, and for level-1/level-2/level-3 data-provenance conflation (e.g., presenting an illustrative Miller-Urey bar height as a precise measured yield) -- these are the most common sources of mistakes in this course.</p></section></main>"
    return page(f'ASTR 350 Problem Set {n:02d} Solutions', body)


def assessment_md(n: int, title: str, criteria: list, common_errors: list) -> str:
    crit = '\n'.join(f'- {c}' for c in criteria)
    err = '\n'.join(f'- {e}' for e in common_errors)
    return f"""# Assessment Instructions: Problem Set {n:02d} \u2014 {title}

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the referenced dataset(s) under `materials/ASTR350/data/`.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking number but no visible derivation steps should not. Because this is a 300-level quantitative exoplanets/astrobiology course, full marks require a genuine derivation wherever the problem set asks for one, and a genuinely reasoned (not merely asserted) interpretation wherever the problem asks for scientific judgment (e.g., biosignature false-positive reasoning, habitability assessment).

## Problem-Level Criteria
{crit}

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
{err}
"""


# ===========================================================================
# LAB/PSET 01: Radial velocity and transit method (51 Peg b, HD 209458 b)
# ===========================================================================
def make_lab_01() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This is a data-analysis lab reproducing the two founding exoplanet-detection measurements of this course using the equations derived in Lectures 01-02: 51 Pegasi b's 1995 radial-velocity discovery and HD 209458 b's 1999 transit discovery. No telescope time is required; all inputs are real, live-verified system parameters.</p></section>
<section><h2>Materials and Data</h2>
<table><thead><tr><th>Quantity</th><th>51 Pegasi b</th><th>HD 209458 b</th></tr></thead><tbody>
<tr><td>Period (d)</td><td>{PLANET_51PEGB['period_d']:.4f}</td><td>{PLANET_HD209458B['period_d']:.4f}</td></tr>
<tr><td>Eccentricity</td><td>{PLANET_51PEGB['e']:.4f}</td><td>{PLANET_HD209458B['e']:.4f}</td></tr>
<tr><td>Measured K (m/s)</td><td>{PLANET_51PEGB['k_rv_m_s']:.2f}</td><td>{PLANET_HD209458B['k_rv_m_s']:.2f}</td></tr>
<tr><td>Inclination (deg)</td><td>{PLANET_51PEGB['inclination_deg']:.1f}</td><td>{PLANET_HD209458B['inclination_deg']:.2f}</td></tr>
<tr><td>Host star mass (Msun)</td><td>{STAR_51PEG['mass_msun']:.2f}</td><td>{STAR_HD209458['mass_msun']:.2f}</td></tr>
</tbody></table>
<p>Both systems' parameters are live-verified this session (direct web fetch of Wikipedia's "51 Pegasi b" and "HD 209458 b" articles, 2026-09-24, citing Mayor &amp; Queloz 1995 and Charbonneau et al. 2000/Henry et al. 2000 respectively). Note: the fetched 51 Pegasi b infobox listed K as "55.77 km/s," a units error caught by cross-checking against the article's own prose and the well-established published value of &asymp;55.9 m/s; this lab uses the corrected units throughout (see <code>../reference-log.md</code>).</p></section>
<section><h2>Procedure</h2><ol>
<li>Using Kepler's third law, compute 51 Pegasi b's semimajor axis from its period and the (star+planet) total mass, and compare to the published value ({PLANET_51PEGB['a_au']:.4f} AU).</li>
<li>Solve the radial-velocity mass function numerically for 51 Pegasi b's minimum mass Mp&nbsp;sin(i), given the measured K, and compare to the published minimum mass ({PLANET_51PEGB['msini_mjup']:.3f} MJup).</li>
<li>Using the independently constrained inclination ({PLANET_51PEGB['inclination_deg']:.1f}&deg;), compute 51 Pegasi b's true mass and compare to the published value ({PLANET_51PEGB['mass_mjup']:.2f} MJup).</li>
<li>Using HD 209458 b's published radius and its host star's radius, compute the predicted transit depth and compare to the measured {PLANET_HD209458B['transit_depth_measured']*100:.1f}% dip.</li>
<li>Using HD 209458 b's period, semimajor axis, and stellar radius, compute the predicted transit duration and compare to the measured &asymp;{PLANET_HD209458B['transit_duration_hr']:.0f}-hour transit.</li>
<li>Using HD 209458 b's independently known mass and inclination (from the transit), predict its radial-velocity semi-amplitude K and compare to the measured value ({PLANET_HD209458B['k_rv_m_s']:.2f} m/s).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly, for each of the six computed quantities above, whether your computed value matches the published value to within the precision of the adopted stellar mass/radius inputs, and identify which single input parameter's uncertainty would most affect each computed result if it were revised.</p></section>
<section><h2>Deliverables</h2><ul><li>All six computed quantities with full derivations and unit tracking.</li><li>A one-paragraph statement of which detection method (RV or transit) supplied which piece of information for each planet, and why combining both methods for HD 209458 b gives more information than either alone.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct Kepler's-third-law and mass-function arithmetic with correct SI units throughout.</li><li>Correct transit depth/duration arithmetic with correctly identified stellar-radius input.</li><li>Correctly identified units correction for 51 Pegasi b's K value, with a stated justification.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>51 Pegasi b and HD 209458 b system parameters: live-verified this session (Wikipedia, 2026-09-24); see <code>materials/ASTR350/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR350/src/generate_astr350_content.py</code>.</li></ul></section>
"""
    return lab_page(1, 'Radial Velocity and Transit Method: 51 Pegasi b and HD 209458 b',
                     'Reproduce the founding 1995 radial-velocity and 1999 transit exoplanet discovery measurements from first principles.', sections)


def make_pset_01():
    problems = problem(1, 'Semi-amplitude sanity check',
                        f'<p>51 Pegasi b has e&asymp;0. Using the mass-function equation, show algebraically that in the limit e&rarr;0 and Mp&lt;&lt;M*, K &prop; Mp sin(i) P^(-1/3) M*^(-2/3). Using this scaling relation (not the full numerical solve), estimate by what factor K would change if 51 Pegasi b\'s period were instead 8.46 days (double the real value) with all other parameters fixed.</p>') + \
               problem(2, 'Minimum mass from a hypothetical measurement',
                       f'<p>A newly discovered planet orbiting a {STAR_51PEG["mass_msun"]:.2f} Msun star (51 Pegasi\'s real mass) shows K=25.0 m/s and P=10.0 days with e&asymp;0. Compute this planet\'s minimum mass in Jupiter masses.</p>') + \
               problem(3, 'HD 209458 b transit depth from scratch',
                       f'<p>Using only HD 209458 b\'s real published mass (0.682 MJup) and mean density (compute it from mass and radius, {PLANET_HD209458B["radius_rjup"]:.3f} RJup) together with the host star\'s radius ({STAR_HD209458["radius_rsun"]:.2f} Rsun), compute the transit depth two independent ways: (a) directly from Rp and Rstar, and (b) by first computing Rp from the mass and density and then applying the same formula. Confirm both methods agree.</p>') + \
               problem(4, 'Transit-duration scaling',
                       '<p>Using T &prop; P^(1/3) (from a &prop; P^(2/3) via Kepler\'s third law, holding Rstar fixed), estimate the transit duration a planet identical to HD 209458 b would have if its period were instead 1.0 day (roughly a quarter of the real value), and state whether this makes such a planet\'s transit easier or harder to schedule follow-up observations for.</p>') + \
               problem(5, 'Combining methods to get bulk density',
                       f'<p>Using HD 209458 b\'s real transit-derived radius and radial-velocity-derived true mass (both given in this problem set\'s reading), compute its bulk density in kg/m^3 and in g/cm^3, and state which solar-system body (if any) it is closest to in density among Mercury, Venus, Earth, Mars, Jupiter (see <code>materials/ASTR350/data/</code>).</p>')
    return pset_page(1, 'Radial Velocity and Transit Method', 'Reproduce and extend this unit\'s founding detection-method calculations.',
                      problems, OPENSTAX)


def make_pset_01_solutions():
    s = solution(1, 'Semi-amplitude sanity check',
                 f'<p>K &prop; P^(-1/3), so doubling P scales K by 2^(-1/3)={2**(-1/3):.4f}, i.e. K would drop to about {2**(-1/3)*100:.1f}% of its original value, roughly {PLANET_51PEGB["k_rv_m_s"]*2**(-1/3):.1f} m/s instead of {PLANET_51PEGB["k_rv_m_s"]:.1f} m/s.</p>',
                 [('Correct derivation of the scaling exponent', 6), ('Correct numeric application', 5), ('Correct interpretation', 4)]) + \
        solution(2, 'Minimum mass from a hypothetical measurement',
                 f'<p>Using the same numerical mass-function solve as Lecture 01\'s worked example with K=25.0 m/s, P=10.0 d, M*={STAR_51PEG["mass_msun"]:.2f} Msun, e=0: Mp sin(i) &asymp; {rv_minimum_mass_kg(25.0, MSTAR_51PEG_KG, 10.0*DAY_S, 0.0)/M_JUP:.3f} MJup.</p>',
                 [('Correct mass-function setup', 6), ('Correct numeric solve/units', 6), ('Reasonable final value', 3)]) + \
        solution(3, 'HD 209458 b transit depth from scratch',
                 f'<p>Method (a): delta=(Rp/Rstar)^2 = {TRANSIT_DEPTH_HD209458B_COMPUTED*100:.3f}%. Method (b): density from mass/radius gives &rho;={HD209458B_DENSITY_KG_M3:.0f} kg/m^3; using M and this density to recover R gives back the same Rp (since R was used to compute the density), so the two methods necessarily agree by construction -- the pedagogical point is recognizing this circularity rather than treating (b) as an independent check.</p>',
                 [('Correct direct transit-depth calculation', 6), ('Correct recognition of circularity in method (b)', 6), ('Clear units/derivation', 3)]) + \
        solution(4, 'Transit-duration scaling',
                 f'<p>T &prop; P^(1/3): at P=1.0 d versus the real 3.52 d, T scales by (1.0/3.525)^(1/3)={(1.0/3.525)**(1/3):.3f}, giving T&asymp;{TRANSIT_DURATION_HD209458B_COMPUTED*(1.0/3.525)**(1/3):.2f} h instead of {TRANSIT_DURATION_HD209458B_COMPUTED:.2f} h -- a shorter transit is harder to schedule precisely but occurs more frequently (shorter period), a real trade-off in real observing proposals.</p>',
                 [('Correct scaling exponent and application', 8), ('Correct qualitative trade-off statement', 7)]) + \
        solution(5, 'Combining methods to get bulk density',
                 f'<p>&rho; = {HD209458B_DENSITY_KG_M3:.0f} kg/m^3 = {HD209458B_DENSITY_KG_M3/1000:.3f} g/cm^3 -- lower than water (1.0 g/cm^3) and far below any solar-system planet in <code>materials/ASTR350/data/</code>, confirming its gas-giant, low-density interior rather than similarity to any specific solar-system body.</p>',
                 [('Correct density calculation and unit conversion', 8), ('Correct, well-justified comparison conclusion', 7)])
    return solutions_page(1, 'Radial Velocity and Transit Method', s)


def make_pset_01_assessment():
    return assessment_md(1, 'Radial Velocity and Transit Method',
                          ['Problem 1: verify the P^(-1/3) scaling exponent is derived, not asserted, and the numeric factor is correct.',
                           'Problem 2: verify the mass-function solve uses e=0 correctly and returns a physically reasonable minimum mass.',
                           'Problem 3: verify the student recognizes the circularity in method (b) rather than presenting it as an independent confirmation.',
                           'Problem 4: verify the correct Kepler-scaling exponent (P^(1/3), not P^(2/3) or P^(1/2)) and a reasoned trade-off statement.',
                           'Problem 5: verify correct unit conversion (kg/m^3 to g/cm^3) and a density-based (not mass-based or radius-based) comparison.'],
                          ['Reporting 51 Pegasi b\'s K in km/s instead of m/s (the caught units error from this unit\'s lecture and lab).',
                           'Treating Mp sin(i) as the true mass without stating the inclination assumption.',
                           'Using the wrong exponent in Kepler-scaling problems (a common error is P^(2/3) where P^(1/3) or P^(-1/3) is required).'])


# ===========================================================================
# LAB/PSET 02: Demographics -- mass-radius diagram and classification
# ===========================================================================
def make_lab_02() -> str:
    rows = ''
    for name, d in SOLAR_SYSTEM.items():
        rows += f"<tr><td>{name}</td><td>{d['mass_earth']:.3f}</td><td>{d['radius_earth']:.3f}</td><td>{d['density_kg_m3']:.0f}</td></tr>"
    for p, d in TRAPPIST1_PLANETS.items():
        rho = TRAPPIST1_DENSITY_KG_M3[p]
        rows += f"<tr><td>TRAPPIST-1{p}</td><td>{d['m_earth']:.3f}</td><td>{d['r_earth']:.3f}</td><td>{rho:.0f}</td></tr>"
    rows += f"<tr><td>HD 209458 b</td><td>{PLANET_HD209458B['mass_mjup']*M_JUP/M_EARTH:.1f}</td><td>{PLANET_HD209458B['radius_rjup']*R_JUP/R_EARTH:.2f}</td><td>{HD209458B_DENSITY_KG_M3:.0f}</td></tr>"
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab builds a full mass-radius-density table and diagram from this course's real dataset (six solar-system planets, seven TRAPPIST-1 planets, and HD 209458 b) and classifies each world by bulk composition regime, applying Lecture 04's demographic reasoning.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Body</th><th>Mass (Mearth)</th><th>Radius (Rearth)</th><th>Density (kg/m&sup3;)</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Plot (by hand or with a simple script) mass versus radius on log-log axes for all 14 bodies in the table, and identify the rocky/gas-giant density branches visually.</li>
<li>Compute the density ratio between the densest and least dense body in the table, and identify both bodies.</li>
<li>Rank the seven TRAPPIST-1 planets by density and identify which one or two are most likely to carry a substantial water/ice mass fraction relative to the others (Lecture 06's composition-degeneracy reasoning).</li>
<li>Using the occurrence-rate framing of Lecture 04, state (in one sentence, using this course's real dataset as an illustration, not as a statistically complete survey) why a demographic conclusion about "typical" planets cannot be drawn from this 14-body sample alone.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly that this lab's 14-body sample is illustrative, not survey-complete or selection-effect-corrected (Lecture 03); a genuine occurrence-rate statement requires a full, completeness-corrected survey sample, which this lab does not attempt to construct.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed mass-radius-density table (already provided; verify/reproduce the TRAPPIST-1 and HD 209458 b density calculations from mass and radius).</li><li>Mass-radius diagram (log-log) with rocky and gas-giant branches labeled.</li><li>Density ranking and composition-degeneracy discussion for the TRAPPIST-1 planets.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correctly reproduced density calculations for all seven TRAPPIST-1 planets and HD 209458 b.</li><li>Correctly identified rocky/gas-giant branches and correctly ranked TRAPPIST-1 densities.</li><li>Clearly stated selection-effect caveat about sample completeness.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>TRAPPIST-1 mass/radius values: standard published (Agol et al. 2021), reused from ASTR320's live verification; see <code>materials/ASTR350/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR350/src/generate_astr350_content.py</code>.</li></ul></section>
"""
    return lab_page(2, 'Exoplanet Demographics: Mass-Radius Diagram and Classification',
                     'Build a full mass-radius-density diagram from this course\'s real planet sample and classify each world\'s bulk composition regime.', sections)


def make_pset_02():
    problems = problem(1, 'Density from first principles',
                        '<p>Derive the formula for bulk density from mass and radius, starting from the volume of a sphere, and use it to compute TRAPPIST-1h\'s density from its real mass and radius (given in this problem set\'s reading). Compare to TRAPPIST-1b\'s density and state which is denser.</p>') + \
               problem(2, 'Rocky/gas-giant transition',
                       f'<p>Using this course\'s dataset, identify the mass range (in Earth masses) over which the transition from a steep, roughly-constant-density mass-radius track to a much flatter gas-giant track occurs, and explain physically (using Lecture 04\'s degeneracy-pressure argument) why the transition is not sharp.</p>') + \
               problem(3, 'Radius valley reasoning',
                       '<p>Using the photoevaporation mechanism from Lecture 04 and the Jeans-escape-parameter tool previewed in Lecture 08, explain qualitatively why a close-in sub-Neptune around an active, young star would be more likely to lose its envelope (and shrink across the radius valley) than an otherwise identical planet at a wider separation.</p>') + \
               problem(4, 'A hypothetical planet\'s classification',
                       '<p>A newly announced planet has M=8.0 Mearth and R=2.2 Rearth. Compute its density and classify it (rocky, transitional/volatile-rich, or gas giant) using this course\'s dataset as a comparison set, with a one-sentence justification.</p>') + \
               problem(5, 'Occurrence-rate caveat',
                       '<p>Explain, using Lecture 03\'s selection-effect reasoning, why a sample dominated by transiting planets (as this course\'s TRAPPIST-1 and HD 209458 b entries are) is biased toward certain orbital separations and inclinations, and what kind of planet this sample would systematically under-represent.</p>')
    return pset_page(2, 'Exoplanet Demographics', 'Extend this unit\'s mass-radius classification reasoning to new cases.', problems, OPENSTAX)


def make_pset_02_solutions():
    s = solution(1, 'Density from first principles',
                 f'<p>&rho;=M/(4/3 &pi; R^3). TRAPPIST-1h: M={TRAPPIST1_PLANETS["h"]["m_earth"]:.3f} Mearth, R={TRAPPIST1_PLANETS["h"]["r_earth"]:.3f} Rearth, &rho;={TRAPPIST1_DENSITY_KG_M3["h"]:.0f} kg/m^3. TRAPPIST-1b: &rho;={TRAPPIST1_DENSITY_KG_M3["b"]:.0f} kg/m^3 -- b is denser than h.</p>',
                 [('Correct derivation from sphere volume', 6), ('Correct numeric density for both planets', 6), ('Correct comparison', 3)]) + \
        solution(2, 'Rocky/gas-giant transition',
                 '<p>The transition occurs roughly in the several-to-tens-of-Earth-mass range (consistent with this course\'s sample: TRAPPIST-1 planets, all under 1.2 Mearth-scale, are rocky-density; Jupiter/HD 209458 b, hundreds of Earth masses, are gas-giant-density); it is not sharp because increasing envelope mass fraction is a continuum, not a step function, and electron-degeneracy-pressure support becomes progressively more important rather than switching on suddenly.</p>',
                 [('Reasonable transition mass range identified from the dataset', 7), ('Correct physical explanation of gradualness', 8)]) + \
        solution(3, 'Radius valley reasoning',
                 '<p>A close-in planet sits in a much higher stellar X-ray/UV flux environment, giving its exobase a higher temperature and thus a smaller Jeans escape parameter (lambda &prop; 1/T) for the same planet mass/radius, pushing it toward the hydrodynamic-escape regime and faster envelope loss than an identical planet farther out with a cooler exobase and larger lambda.</p>',
                 [('Correct linkage between irradiation, exobase temperature, and lambda', 8), ('Correct qualitative escape-rate conclusion', 7)]) + \
        solution(4, 'A hypothetical planet\'s classification',
                 f'<p>&rho; = 8.0 Mearth &times; {M_EARTH:.3e} kg / (4/3 &pi; (2.2&times;{R_EARTH:.3e} m)^3) = {8.0*M_EARTH/(4/3*math.pi*(2.2*R_EARTH)**3):.0f} kg/m^3 -- well below Earth\'s 5514 kg/m^3 but well above HD 209458 b\'s {HD209458B_DENSITY_KG_M3:.0f} kg/m^3, consistent with a transitional, volatile-rich sub-Neptune-class classification.</p>',
                 [('Correct density calculation', 8), ('Correct, dataset-grounded classification', 7)]) + \
        solution(5, 'Occurrence-rate caveat',
                 '<p>Transit surveys require a near-edge-on inclination and are biased toward close-in orbits (higher transit probability, Lecture 02); this systematically under-represents wide-separation and low-inclination (more face-on) systems, meaning a transit-dominated sample cannot be used to claim wide-orbit planets are rare without first correcting for this geometric selection effect.</p>',
                 [('Correct identification of the inclination/separation bias', 8), ('Correct statement of what is under-represented', 7)])
    return solutions_page(2, 'Exoplanet Demographics', s)


def make_pset_02_assessment():
    return assessment_md(2, 'Exoplanet Demographics',
                          ['Problem 1: verify the density formula is derived from sphere volume, not just quoted.',
                           'Problem 2: accept any reasonable mass range consistent with the course dataset; verify the degeneracy-pressure explanation is present.',
                           'Problem 3: verify the lambda &prop; 1/T linkage is stated explicitly, not just asserted qualitatively.',
                           'Problem 4: verify correct SI unit conversion in the density calculation.',
                           'Problem 5: verify the student identifies transit probability (not just "transit is biased") as the specific mechanism.'],
                          ['Confusing mass-radius degeneracy (Lecture 06) with the rocky/gas-giant transition (Lecture 04) -- these are related but distinct claims.',
                           'Treating this course\'s 14-body illustrative sample as if it were a complete, unbiased survey.'])


# ===========================================================================
# LAB/PSET 03: Orbital architecture (TRAPPIST-1 resonances) and interiors
# ===========================================================================
def make_lab_03() -> str:
    names = list(TRAPPIST1_PLANETS.keys())
    ratios = []
    for i in range(len(names) - 1):
        p1, p2 = names[i], names[i + 1]
        r = TRAPPIST1_PLANETS[p2]['period_d'] / TRAPPIST1_PLANETS[p1]['period_d']
        ratios.append((p1, p2, r))
    rows = ''.join(f"<tr><td>{a}-{b}</td><td>{r:.4f}</td></tr>" for a, b, r in ratios)
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes TRAPPIST-1's full chain of adjacent orbital-period ratios from the system's real, live-verified periods and evaluates each against the nearest simple integer resonance (Lecture 05), then computes bulk densities for all seven planets to evaluate the interior mass-radius composition degeneracy (Lecture 06).</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Adjacent pair</th><th>Period ratio</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>For each adjacent period ratio in the table, identify the nearest simple integer ratio (e.g., 3:2, 4:3, 5:3, 8:5) and compute the percent deviation from that exact ratio.</li>
<li>State whether the full six-ratio chain is consistent with a genuine resonant chain (small, consistent percent deviations throughout) or a coincidental near-resonance (large or inconsistent deviations).</li>
<li>Using this course's real TRAPPIST-1 eccentricity dataset (essentially circular orbits) and Lecture 05's tidal-circularization argument, explain why circularization is expected to be efficient for all seven planets despite their being in mean-motion resonance.</li>
<li>Compute the bulk density of each of the seven TRAPPIST-1 planets and rank them from most to least likely to carry a substantial water/ice layer, per Lecture 06's composition-degeneracy reasoning.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly that identifying a near-integer period ratio is necessary but not sufficient evidence of a true dynamical resonance (Lecture 05's pitfall); a full confirmation requires transit-timing-variation or stability-simulation evidence this lab does not itself compute, only cites from the published literature.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed period-ratio table with nearest-integer-ratio identification and percent deviations.</li><li>Density ranking table for all seven TRAPPIST-1 planets with composition-degeneracy discussion.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct period-ratio arithmetic and reasonable nearest-integer-ratio identification for all six adjacent pairs.</li><li>Correct density calculations and ranking for all seven planets.</li><li>Explicit acknowledgment that period-ratio proximity alone does not prove dynamical resonance.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>TRAPPIST-1 orbital periods and mass/radius values: reused from ASTR320's live verification (Wikipedia, 2026-09-24, citing Agol et al. 2021 and Ducrot et al. 2020); see <code>materials/ASTR350/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(3, 'TRAPPIST-1 Orbital Resonances and Interior Density Inference',
                     'Compute TRAPPIST-1\'s full resonant-chain period ratios and each planet\'s bulk density from real system data.', sections)


def make_pset_03():
    problems = problem(1, 'Resonance chain arithmetic',
                        '<p>Using the period-ratio table from this unit\'s lab, compute the overall ratio P_h/P_b (TRAPPIST-1\'s outermost to innermost known planet) two ways: (a) directly from the two periods, and (b) as the product of the six adjacent-pair ratios. Confirm the two methods agree, and explain why they must.</p>') + \
               problem(2, 'Tidal circularization timescale reasoning',
                       f'<p>Using the steep a-dependence of the tidal-circularization timescale from Lecture 05 (t_circ &prop; a^(13/2)), and given that TRAPPIST-1e (a={TRAPPIST1_PLANETS["e"]["a_au"]:.4f} AU) has an orbit only about 1.7 times larger than TRAPPIST-1b (a={TRAPPIST1_PLANETS["b"]["a_au"]:.4f} AU), estimate the ratio of their tidal-circularization timescales, and state whether both should be expected to be circularized within the system\'s age.</p>') + \
               problem(3, 'Density-based composition classification',
                       '<p>Using your computed densities for TRAPPIST-1d and TRAPPIST-1g (this problem set\'s reading), state which is more likely to carry a larger ice/water mass fraction and justify your answer quantitatively using the density comparison to Earth.</p>') + \
               problem(4, 'Composition degeneracy limits',
                       '<p>Explain, using Lecture 06\'s degeneracy argument, what additional measurement (beyond mass and radius) would be needed to determine whether TRAPPIST-1e\'s slightly-lower-than-Earth density reflects a smaller iron core, a modest ice/water layer, or some combination of both.</p>')
    return pset_page(3, 'Orbital Architecture and Interiors', 'Extend this unit\'s resonance-chain and density-inference reasoning.', problems, OPENSTAX)


def make_pset_03_solutions():
    names = list(TRAPPIST1_PLANETS.keys())
    prod = 1.0
    for i in range(len(names) - 1):
        prod *= TRAPPIST1_PLANETS[names[i + 1]]['period_d'] / TRAPPIST1_PLANETS[names[i]]['period_d']
    direct = TRAPPIST1_PLANETS['h']['period_d'] / TRAPPIST1_PLANETS['b']['period_d']
    s = solution(1, 'Resonance chain arithmetic',
                 f'<p>Direct: P_h/P_b = {direct:.4f}. Product of six adjacent ratios: {prod:.4f}. They agree (telescoping product of ratios) because each intermediate period cancels: (P_c/P_b)(P_d/P_c)...(P_h/P_g) = P_h/P_b algebraically, regardless of the specific intermediate values.</p>',
                 [('Correct direct ratio', 5), ('Correct product-of-ratios computation matching the direct value', 6), ('Correct telescoping explanation', 4)]) + \
        solution(2, 'Tidal circularization timescale reasoning',
                 f'<p>t_circ(e)/t_circ(b) &asymp; (a_e/a_b)^(13/2) = (1.7)^6.5 &asymp; {1.7**6.5:.0f} -- TRAPPIST-1e\'s circularization timescale is roughly {1.7**6.5:.0f}&times; longer than b\'s, but both are still almost certainly far shorter than the system\'s multi-Gyr age given how close-in even TRAPPIST-1e is, consistent with both planets\' observed essentially-zero eccentricities.</p>',
                 [('Correct application of the 13/2 power law', 8), ('Correct qualitative conclusion that both are circularized', 7)]) + \
        solution(3, 'Density-based composition classification',
                 f'<p>TRAPPIST-1d has &rho;={TRAPPIST1_DENSITY_KG_M3["d"]:.0f} kg/m^3 versus TRAPPIST-1g\'s {TRAPPIST1_DENSITY_KG_M3["g"]:.0f} kg/m^3; d is markedly less dense (a larger fractional departure from Earth\'s 5514 kg/m^3), consistent with d carrying a proportionally larger ice/water mass fraction than g.</p>',
                 [('Correct density values cited', 6), ('Correct comparative conclusion with quantitative support', 9)]) + \
        solution(4, 'Composition degeneracy limits',
                 '<p>Mass and radius alone cannot distinguish a smaller iron core from an added ice/water layer, both of which lower bulk density from a pure-silicate baseline; breaking the degeneracy would require an independent atmospheric composition measurement (detecting or ruling out a substantial water-vapor/volatile atmosphere, Lecture 07) or, in a favorable case, a measured tidal Love number probing internal structure directly.</p>',
                 [('Correct statement of the degeneracy', 7), ('Correct identification of at least one degeneracy-breaking measurement', 8)])
    return solutions_page(3, 'Orbital Architecture and Interiors', s)


def make_pset_03_assessment():
    return assessment_md(3, 'Orbital Architecture and Interiors',
                          ['Problem 1: verify the telescoping-product explanation is present, not just matching numbers.',
                           'Problem 2: verify the 13/2 exponent is used correctly and the conclusion about circularization is consistent with the observed near-zero eccentricities.',
                           'Problem 3: verify the comparison is density-based and quantitatively supported, not just a qualitative guess.',
                           'Problem 4: accept either atmospheric composition or tidal Love-number measurement as a correct degeneracy-breaking answer.'],
                          ['Treating a close period ratio as proof of resonance without noting that true confirmation requires TTV or stability-simulation evidence.',
                           'Reversing the sign of the density comparison (claiming a lower density means a larger iron core, rather than a smaller one/larger ice fraction).'])


# ===========================================================================
# LAB/PSET 04: Atmospheres and escape (HD 209458 b)
# ===========================================================================
def make_lab_04() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes HD 209458 b's atmospheric scale height and predicted transmission-spectroscopy signal amplitude (Lecture 07), then its Jeans escape parameter and naive mass-loss timescale (Lecture 08), comparing both to the real, published Hubble Space Telescope measurements.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Mass</td><td>{PLANET_HD209458B['mass_mjup']:.3f} MJup</td></tr>
<tr><td>Radius</td><td>{PLANET_HD209458B['radius_rjup']:.3f} RJup</td></tr>
<tr><td>Surface gravity (computed)</td><td>{HD209458B_SURFACE_G:.2f} m/s&sup2;</td></tr>
<tr><td>Exosphere temperature (real, HST-measured)</td><td>{PLANET_HD209458B['exosphere_temp_k']:.0f} K</td></tr>
<tr><td>Real exosphere extent</td><td>{PLANET_HD209458B['exosphere_extent_rjup']:.1f} planetary radii</td></tr>
<tr><td>Real mass-loss rate</td><td>{PLANET_HD209458B['mass_loss_kg_s']:.1e} kg/s</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute HD 209458 b's atmospheric scale height H at its exosphere temperature, for atomic hydrogen (mu=1 amu).</li>
<li>Estimate the transit-depth signal amplitude for N=5 scale heights of absorbing atmosphere above the bulk continuum radius, using Lecture 07's formula, and compare to the real sodium-detection signal's approximate size.</li>
<li>Compute HD 209458 b's Jeans escape parameter at the exosphere temperature and state whether the planet is in the classical Jeans-escape regime or the hydrodynamic blow-off regime.</li>
<li>Compute the naive mass-loss timescale (current mass divided by the real, published mass-loss rate) and state whether the planet is in danger of complete evaporation within a typical few-Gyr system age at its current rate.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly that the naive mass-loss timescale assumes a constant mass-loss rate, which is very likely an overestimate of the timescale (an underestimate of total historical loss), because the host star's X-ray/UV activity -- and therefore the escape rate -- was almost certainly much higher earlier in the system's history (Lecture 08).</p></section>
<section><h2>Deliverables</h2><ul><li>Scale height, transit-signal estimate, Jeans parameter, and mass-loss timescale, all with full derivations.</li><li>A one-paragraph statement of which escape regime HD 209458 b is in and why this matters for interpreting its real, observed extended exosphere.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct scale-height calculation with correct units (K_B, T, mu in kg, g).</li><li>Correct Jeans-parameter calculation and correctly identified escape regime.</li><li>Explicit statement of the constant-rate assumption's limitation.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>HD 209458 b atmospheric/exosphere data: live-verified this session (Wikipedia, "HD 209458 b," 2026-09-24, citing Vidal-Madjar et al. 2003, Charbonneau et al. 2002).</li></ul></section>
"""
    return lab_page(4, 'Atmospheric Scale Height and Escape: HD 209458 b',
                     'Compute HD 209458 b\'s transmission-spectroscopy signal and Jeans escape parameter from first principles and compare to real HST measurements.', sections)


def make_pset_04():
    problems = problem(1, 'Scale height and gravity',
                        '<p>Using this unit\'s reading, explain quantitatively (using the scale-height formula) why a planet with the same temperature but twice HD 209458 b\'s surface gravity would have a transmission-spectroscopy signal only half as large, all else equal.</p>') + \
               problem(2, 'Jeans parameter for a rocky planet',
                       f'<p>Compute the Jeans escape parameter for Earth-mass hydrogen atoms at Earth\'s exobase (assume T&asymp;1000 K, use Earth\'s real mass and radius from <code>materials/ASTR350/data/</code>), and compare it to HD 209458 b\'s value ({HD209458B_JEANS_PARAM:.2f}). State which planet is in more danger of hydrodynamic hydrogen escape and why this is consistent with Earth having retained only trace atmospheric hydrogen today.</p>') + \
               problem(3, 'Mass-loss timescale sensitivity',
                       f'<p>If HD 209458 b\'s real mass-loss rate had instead been measured as {PLANET_HD209458B["mass_loss_kg_s"]*3:.1e} kg/s (three times the real value), recompute the naive mass-loss timescale and state whether this would change the conclusion about the planet\'s long-term survival at the currently observed rate.</p>') + \
               problem(4, 'Escape and the radius valley',
                       '<p>Connect this unit\'s escape-parameter reasoning explicitly to Lecture 04\'s radius-valley discussion: explain why a lower-mass sub-Neptune at HD 209458 b\'s orbital distance would have a smaller Jeans parameter (all else equal) and therefore be more vulnerable to complete envelope loss than HD 209458 b itself.</p>')
    return pset_page(4, 'Atmospheres and Escape', 'Extend this unit\'s scale-height and Jeans-escape reasoning.', problems, OPENSTAX)


def make_pset_04_solutions():
    earth_jeans = jeans_escape_parameter(M_EARTH, R_EARTH, 1000.0, 1.0)
    s = solution(1, 'Scale height and gravity',
                 '<p>H=kT/(mu g); doubling g halves H, and the transit-signal amplitude formula delta(N)-delta(0) &prop; H, so doubling g halves the predicted signal amplitude, all else (temperature, N, Rp, Rstar) held fixed.</p>',
                 [('Correct H &prop; 1/g relation stated', 7), ('Correct propagation to the transit-signal formula', 8)]) + \
        solution(2, 'Jeans parameter for a rocky planet',
                 f'<p>lambda(Earth, hydrogen, T=1000 K) = GMm/(kTR) = {earth_jeans:.1f} -- far larger than HD 209458 b\'s {HD209458B_JEANS_PARAM:.2f}, meaning Earth\'s hydrogen is much more tightly gravitationally bound relative to its thermal energy, so Earth is in the negligible-escape (classical Jeans, not hydrodynamic) regime for hydrogen, consistent with the fact that Earth would have far more atmospheric hydrogen today if it escaped as readily as on HD 209458 b.</p>',
                 [('Correct Jeans-parameter calculation for Earth', 8), ('Correct comparison and physically consistent conclusion', 7)]) + \
        solution(3, 'Mass-loss timescale sensitivity',
                 f'<p>Timescale scales inversely with mass-loss rate: {HD209458B_MASS_LOSS_TIMESCALE_GYR:.1f} Gyr / 3 = {HD209458B_MASS_LOSS_TIMESCALE_GYR/3:.1f} Gyr -- still comparable to or longer than a typical few-Gyr system age, so the qualitative conclusion (not in danger of complete evaporation at this constant rate) would likely still hold, though with reduced margin.</p>',
                 [('Correct inverse scaling', 8), ('Correct, appropriately hedged conclusion', 7)]) + \
        solution(4, 'Escape and the radius valley',
                 '<p>lambda=GMm/(kTR) decreases for smaller planet mass M at fixed T (exobase temperature set mainly by irradiation, not planet mass) and R (which also shrinks less than proportionally with M for a similar-density planet); a lower-mass sub-Neptune therefore has a smaller lambda than HD 209458 b at the same orbital distance, placing it more deeply in the hydrodynamic-escape regime and making full envelope loss (crossing into the radius valley\'s "stripped core" population) far more plausible than for a hot-Jupiter-mass planet like HD 209458 b.</p>',
                 [('Correct mass-dependence argument for lambda', 8), ('Correct explicit connection to the radius valley', 7)])
    return solutions_page(4, 'Atmospheres and Escape', s)


def make_pset_04_assessment():
    return assessment_md(4, 'Atmospheres and Escape',
                          ['Problem 1: verify the inverse proportionality (not direct proportionality) between signal amplitude and g is stated correctly.',
                           'Problem 2: verify Earth\'s Jeans parameter is computed with correct units and compared correctly (larger lambda = less escape).',
                           'Problem 3: verify the inverse-scaling arithmetic and an appropriately hedged (not overconfident) conclusion.',
                           'Problem 4: verify the connection to the radius valley is explicit, not just a restatement of the escape-parameter formula.'],
                          ['Reversing the direction of the lambda-versus-escape relationship (larger lambda means less, not more, escape).',
                           'Treating a single constant-rate mass-loss timescale as a precise prediction rather than an order-of-magnitude, likely-conservative estimate.'])


# ===========================================================================
# LAB/PSET 05: Habitable zone census
# ===========================================================================
def make_lab_05() -> str:
    sun_in, sun_out = SUN_HZ_INNER_AU, SUN_HZ_OUTER_AU
    t1_in, t1_out = TRAPPIST1_HZ_INNER_AU, TRAPPIST1_HZ_OUTER_AU
    rows = ''.join(
        f"<tr><td>TRAPPIST-1{p}</td><td>{d['a_au']:.4f}</td><td>{TRAPPIST1_TEQ[p]:.0f}</td><td>"
        f"{'inside HZ' if t1_in <= d['a_au'] <= t1_out else ('inside inner edge (too hot)' if d['a_au'] < t1_in else 'outside outer edge (too cold)')}</td></tr>"
        for p, d in TRAPPIST1_PLANETS.items())
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab computes the classical (conservative) habitable-zone boundaries for the Sun and for TRAPPIST-1 from their real luminosities (Lecture 09), censuses every TRAPPIST-1 planet against its own star's boundaries, and qualitatively evaluates Venus's and Mars's real climate outcomes against the same framework (Lecture 10).</p></section>
<section><h2>Materials and Data</h2>
<p>Sun: L=1 Lsun, HZ = {sun_in:.3f}-{sun_out:.3f} AU. TRAPPIST-1: L={TRAPPIST1_STAR['lum_lsun']:.3e} Lsun (live-verified), HZ = {t1_in:.4f}-{t1_out:.4f} AU.</p>
<table><thead><tr><th>Planet</th><th>a (AU)</th><th>T_eq (K, zero albedo)</th><th>HZ status</th></tr></thead><tbody>{rows}</tbody></table>
</section>
<section><h2>Procedure</h2><ol>
<li>Reproduce the Sun's and TRAPPIST-1's habitable-zone inner/outer boundaries from their real luminosities using the flux-boundary equation.</li>
<li>Reproduce the HZ-status classification for all seven TRAPPIST-1 planets shown in the table.</li>
<li>Compute Venus's and Mars's real insolation (from their real orbital distances) in units of Earth's insolation, and check each against the Sun's computed habitable-zone boundaries.</li>
<li>State, using Lecture 10's climate-feedback reasoning, why Venus's and Mars's real observed climates (a runaway greenhouse and a frozen, dry surface, respectively) are or are not fully explained by the classical habitable-zone boundaries alone.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly that the classical habitable-zone boundaries used here assume an Earth-like atmosphere and zero-albedo radiative equilibrium; a specific planet's real climate depends on its actual atmospheric composition, albedo, and geological activity (Lecture 10), which this lab's insolation-only calculation does not capture.</p></section>
<section><h2>Deliverables</h2><ul><li>Reproduced HZ boundary calculations for the Sun and TRAPPIST-1.</li><li>Completed HZ-status table for all seven TRAPPIST-1 planets.</li><li>Venus/Mars insolation check with a climate-feedback discussion.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct sqrt(L)-scaling arithmetic for both stars' HZ boundaries.</li><li>Correctly classified HZ status for all seven TRAPPIST-1 planets.</li><li>Explicit statement of the classical-HZ-versus-actual-climate distinction from Lecture 10.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Habitable-zone flux boundaries: Kasting, Whitmire &amp; Reynolds (1993), standard published, level 2. TRAPPIST-1 luminosity: reused from ASTR320's live verification.</li></ul></section>
"""
    return lab_page(5, 'Habitable Zone Census: The Sun, TRAPPIST-1, and the Classical Boundaries',
                     'Compute real habitable-zone boundaries for two real stars and census every known TRAPPIST-1 planet against them.', sections)


def make_pset_05():
    problems = problem(1, 'HZ boundary scaling',
                        f'<p>A star has half the Sun\'s luminosity. Compute its habitable-zone inner and outer boundaries in AU, and state how many times closer in this HZ is compared to the Sun\'s.</p>') + \
               problem(2, '51 Pegasi and HD 209458 habitable zones',
                       '<p>Using the real stellar masses given for 51 Pegasi and HD 209458 in this unit\'s reading (approximate their luminosities as scaling with mass^3.5, a standard main-sequence approximation), estimate each star\'s habitable-zone boundaries, and state whether 51 Pegasi b or HD 209458 b (both hot Jupiters at a fraction of an AU) fall anywhere near their respective habitable zones.</p>') + \
               problem(3, 'Venus insolation check',
                       f'<p>Compute Venus\'s insolation in units of Earth\'s insolation from its real orbital distance (0.723 AU), and state whether it falls above, inside, or below the Sun\'s classical habitable-zone flux range ({HZ_S_OUTER}-{HZ_S_INNER} S_Earth).</p>') + \
               problem(4, 'Habitable zone is necessary, not sufficient',
                       '<p>Using Lecture 10\'s tidal-heating/subsurface-ocean-world discussion, explain why Europa\'s real, spacecraft-confirmed subsurface ocean is not a counterexample that invalidates the classical habitable zone concept, but rather an example of a different physical pathway to liquid water that the classical HZ was never designed to describe.</p>')
    return pset_page(5, 'The Habitable Zone', 'Extend this unit\'s habitable-zone boundary and climate-context reasoning.', problems, OPENSTAX)


def make_pset_05_solutions():
    d_in_half, d_out_half = hz_boundaries_au(0.5)
    l_51peg = STAR_51PEG['mass_msun'] ** 3.5
    l_hd209458 = STAR_HD209458['mass_msun'] ** 3.5
    in_51peg, out_51peg = hz_boundaries_au(l_51peg)
    in_hd, out_hd = hz_boundaries_au(l_hd209458)
    venus_insolation_ratio = insolation_w_m2(L_SUN, 0.723 * AU_M) / EARTH_INSOLATION
    s = solution(1, 'HZ boundary scaling',
                 f'<p>d_inner=sqrt(0.5/{HZ_S_INNER})={d_in_half:.3f} AU, d_outer=sqrt(0.5/{HZ_S_OUTER})={d_out_half:.3f} AU -- both closer in than the Sun\'s {SUN_HZ_INNER_AU:.3f}-{SUN_HZ_OUTER_AU:.3f} AU by a factor of sqrt(0.5)={math.sqrt(0.5):.3f}, i.e. about 1.41&times; closer.</p>',
                 [('Correct HZ boundary calculation', 8), ('Correct scaling-factor statement', 7)]) + \
        solution(2, '51 Pegasi and HD 209458 habitable zones',
                 f'<p>Using L&prop;M^3.5: 51 Pegasi (M={STAR_51PEG["mass_msun"]:.2f} Msun) gives L&asymp;{l_51peg:.2f} Lsun, HZ&asymp;{in_51peg:.2f}-{out_51peg:.2f} AU; HD 209458 (M={STAR_HD209458["mass_msun"]:.2f} Msun) gives L&asymp;{l_hd209458:.2f} Lsun, HZ&asymp;{in_hd:.2f}-{out_hd:.2f} AU. Both 51 Pegasi b (a={PLANET_51PEGB["a_au"]:.3f} AU) and HD 209458 b (a={PLANET_HD209458B["a_au"]:.4f} AU) orbit far interior to their star\'s habitable zone -- neither is anywhere near habitable-zone distance, consistent with both being hot, gas-giant worlds.</p>',
                 [('Correct mass-luminosity scaling application', 8), ('Correct HZ comparison and conclusion for both planets', 7)]) + \
        solution(3, 'Venus insolation check',
                 f'<p>S(Venus)/S(Earth) = {venus_insolation_ratio:.2f} -- above the inner-edge threshold ({HZ_S_INNER} S_Earth), meaning Venus lies inside (interior to) the classical habitable zone\'s inner edge, consistent with its real runaway-greenhouse outcome.</p>',
                 [('Correct insolation ratio calculation', 8), ('Correct classification relative to the inner edge', 7)]) + \
        solution(4, 'Habitable zone is necessary, not sufficient',
                 '<p>The classical HZ answers only "is stellar insolation compatible with surface liquid water assuming an Earth-like atmosphere"; Europa\'s ocean is sustained by tidal heating, an entirely different energy source unrelated to stellar flux, so its existence outside the classical HZ does not contradict the HZ concept -- it simply falls outside the specific physical question the classical HZ was designed to answer, exactly as Lecture 10 states explicitly.</p>',
                 [('Correct statement that classical HZ is insolation-specific', 8), ('Correct, non-contradictory framing of the Europa counter-case', 7)])
    return solutions_page(5, 'The Habitable Zone', s)


def make_pset_05_assessment():
    return assessment_md(5, 'The Habitable Zone',
                          ['Problem 1: verify sqrt(0.5) scaling factor, not 0.5 itself.',
                           'Problem 2: accept reasonable approximate luminosity values from the mass-luminosity scaling; verify the qualitative conclusion (both planets far interior to their HZ) is correct.',
                           'Problem 3: verify correct insolation-ratio arithmetic and correct classification relative to the inner-edge threshold.',
                           'Problem 4: verify the answer does not claim Europa contradicts or invalidates the habitable-zone concept.'],
                          ['Confusing "inside the habitable zone" with "confirmed habitable" (the Lecture 09 pitfall).',
                           'Using the wrong luminosity scaling exponent or forgetting to convert AU/luminosity units consistently.'])


# ===========================================================================
# LAB/PSET 06: Biosignatures and extremophiles
# ===========================================================================
def make_lab_06() -> str:
    rows = ''.join(f"<tr><td>{e['name']}</td><td>{e['trait']}</td><td>{e['value']}</td><td>{e['unit']}</td></tr>" for e in EXTREMOPHILES)
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab works through the abiotic-oxygen false-positive decision logic (Lecture 11) for a real TRAPPIST-1 planet using this course's computed habitable-zone and equilibrium-temperature results, then builds a documented extremophile tolerance summary (Lecture 12) to bound which environments could plausibly support active microbial growth.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Organism</th><th>Trait</th><th>Value</th><th>Unit</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using TRAPPIST-1b's and TRAPPIST-1c's real orbital distances and this course's computed habitable-zone inner edge ({TRAPPIST1_HZ_INNER_AU:.4f} AU), state whether either planet is a plausible candidate for the published abiotic-oxygen-buildup false-positive pathway (Lecture 11).</li>
<li>State what additional atmospheric detections (context gases) would strengthen versus weaken a biosignature interpretation for an oxygen signal on either planet.</li>
<li>Using the extremophile table, compute the ratio of Deinococcus radiodurans's documented radiation tolerance to the human lethal dose.</li>
<li>Using TRAPPIST-1e's computed zero-albedo equilibrium temperature (Lecture 09) and the documented growth-temperature range of known life (-25 to 121 degrees C), state whether TRAPPIST-1e's temperature alone is compatible with the known growth envelope of Earth life (with the explicit caveat that equilibrium temperature is not the same as actual surface temperature, Lecture 09's pitfall).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly that a documented extremophile survival/growth record is evidence about Earth life's known tolerance envelope, not proof that a given exoplanet environment is inhabited or even habitable; this lab draws only the specific, limited conclusions its data can support.</p></section>
<section><h2>Deliverables</h2><ul><li>TRAPPIST-1b/c abiotic-oxygen plausibility assessment with explicit reasoning.</li><li>Radiation-tolerance ratio calculation.</li><li>TRAPPIST-1e temperature-envelope compatibility check with appropriate caveats.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correctly applies the disequilibrium/context-gas reasoning from Lecture 11, not just a generic "life is possible/impossible" statement.</li><li>Correct radiation-tolerance ratio arithmetic.</li><li>Explicit statement of the equilibrium-temperature-versus-actual-surface-temperature caveat.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>Extremophile records: standard published primary literature (Blochl et al. 1997; Kashefi &amp; Lovley 2003; Mykytczuk et al. 2013; Daly 2009; Seki &amp; Toyoshima 1998), level 2, not independently re-verified this session; see <code>materials/ASTR350/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(6, 'Biosignature False-Positive Reasoning and Extremophile Tolerance Limits',
                     'Apply the abiotic-oxygen false-positive decision logic to a real TRAPPIST-1 planet and bound plausible habitability using documented extremophile records.', sections)


def make_pset_06():
    problems = problem(1, 'Chemical residence time',
                        '<p>Earth\'s atmospheric methane has a chemical residence time of roughly a decade. Using the disequilibrium argument from Lecture 11, explain what this short residence time implies about the source of Earth\'s atmospheric methane, and contrast this with a hypothetical planet where methane is detected but has a residence time of a billion years.</p>') + \
               problem(2, 'A specific false-positive scenario',
                       '<p>A newly characterized rocky planet orbiting an active M-dwarf, well inside the star\'s pre-main-sequence-inflated early habitable zone, shows a strong O2 feature but no detectable water vapor, methane, or other reduced gases. Using Lecture 11\'s reasoning, state whether this pattern is more consistent with a biological or an abiotic origin, and justify your answer.</p>') + \
               problem(3, 'Growth versus survival',
                       '<p>Using the distinction from Lecture 12, explain why "tardigrades survive 600 MPa" is not equivalent evidence to "some organism can actively grow and reproduce at 600 MPa," and why this distinction matters for interpreting a hypothetical high-pressure subsurface-ocean-world biosignature claim.</p>') + \
               problem(4, 'Polyextremophile relevance',
                       '<p>Explain why an organism like Chroococcidiopsis, which tolerates extreme desiccation, high UV flux, and large temperature swings simultaneously, is considered a more astrobiologically relevant analog for a Mars-surface or an icy-moon-surface environment than an organism documented to tolerate only one of those extremes in isolation.</p>')
    return pset_page(6, 'Biosignatures and Extremophiles', 'Extend this unit\'s false-positive and extremophile-limit reasoning.', problems, OPENSTAX)


def make_pset_06_solutions():
    ratio = EXTREMOPHILES[3]['value'] / HUMAN_LETHAL_RADIATION_GY
    s = solution(1, 'Chemical residence time',
                 f'<p>A decade-scale residence time is far shorter than the star-planet system\'s age (Gyr-scale), so Earth\'s observed methane abundance requires an ongoing source (biological and anthropogenic) to replenish what reacts away; a hypothetical billion-year residence time would instead be consistent with methane persisting from an ancient, possibly abiotic origin (e.g., primordial outgassing) with no ongoing source required -- the same molecule, very different evidentiary strength depending on the residence time.</p>',
                 [('Correct short-residence-time-implies-active-source reasoning', 8), ('Correct contrast with the long-residence-time case', 7)]) + \
        solution(2, 'A specific false-positive scenario',
                 f'<p>This pattern (strong O2, no water vapor or reduced context gases, close-in planet around an active M-dwarf with a historically inflated early HZ) matches the published abiotic-oxygen-buildup pathway (Luger &amp; Barnes 2015) closely and is therefore more consistent with an abiotic origin than a confident biological claim; a genuinely strong biosignature case would require co-detected reduced gases providing disequilibrium context, which are explicitly absent here.</p>',
                 [('Correct identification of the abiotic pathway as the better-supported explanation', 8), ('Correct justification citing the missing context gases', 7)]) + \
        solution(3, 'Growth versus survival',
                 '<p>Tardigrade pressure survival is documented in a dormant, largely metabolically inactive cryptobiotic state; it says nothing about whether any organism can actively grow, metabolize, and reproduce at 600 MPa. A biosignature claim for a high-pressure subsurface environment requires evidence of active biological processes (e.g., a maintained chemical disequilibrium), not merely evidence that dormant survival at that pressure is possible for some Earth organism.</p>',
                 [('Correct growth-versus-survival distinction applied to this specific case', 8), ('Correct connection to biosignature-claim standards', 7)]) + \
        solution(4, 'Polyextremophile relevance',
                 '<p>A real Mars-surface or icy-moon-surface environment presents multiple simultaneous extremes (desiccation, radiation, temperature swings) rather than one extreme in isolation; an organism documented to tolerate only one of these in a controlled lab setting has not been shown to tolerate their simultaneous combination, so a polyextremophile like Chroococcidiopsis is a more representative real-world analog for assessing plausible habitability of such environments.</p>',
                 [('Correct statement that real environments present combined, not isolated, extremes', 8), ('Correct conclusion favoring polyextremophile analogs', 7)])
    return solutions_page(6, 'Biosignatures and Extremophiles', s)


def make_pset_06_assessment():
    return assessment_md(6, 'Biosignatures and Extremophiles',
                          ['Problem 1: verify the residence-time-versus-system-age comparison is stated explicitly.',
                           'Problem 2: verify the student concludes abiotic origin is better supported and cites the missing context gases as the reason.',
                           'Problem 3: verify the growth/survival (dormancy) distinction is applied correctly to this specific pressure scenario.',
                           'Problem 4: verify the answer addresses simultaneous/combined extremes, not just repeats the definition of polyextremophile.'],
                          ['Treating any detected biosignature gas as automatic proof of life, ignoring the false-positive pathway (the core Lecture 11 pitfall).',
                           'Treating documented survival/dormancy records as equivalent to documented growth records (the core Lecture 12 pitfall).'])


# ===========================================================================
# LAB/PSET 07: Capstone -- Drake equation and synthesis
# ===========================================================================
def make_lab_07() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This capstone lab requires a full written synthesis applying at least three tools from the preceding six labs (detection method, mass-radius/density classification, orbital architecture or interior inference, atmospheric/escape reasoning, habitable-zone census, or biosignature/extremophile reasoning) to one self-chosen, instructor-approved real exoplanet system, together with a personally justified Drake equation estimate (Lecture 14).</p></section>
<section><h2>Materials and Data</h2><p>This course's own real dataset (51 Pegasi b, HD 209458 b, TRAPPIST-1) may be reused, or a different real, published exoplanet system may be chosen with instructor approval and independently sourced real data (with provenance level stated explicitly, per this course's tri-level scheme).</p>
<table><thead><tr><th>Drake term</th><th>This course's adopted value/range</th><th>Provenance level</th></tr></thead><tbody>
<tr><td>R* (new Sun-like stars/yr)</td><td>{DRAKE_R_STAR}</td><td>2 (standard published order-of-magnitude)</td></tr>
<tr><td>f_p (fraction with planets)</td><td>{DRAKE_F_P}</td><td>2</td></tr>
<tr><td>n_e (HZ-compatible planets/system)</td><td>{DRAKE_N_E}</td><td>2</td></tr>
<tr><td>f_l, f_i, f_c</td><td>illustrative, unconstrained</td><td>3 (synthetic/illustrative)</td></tr>
<tr><td>L (yr)</td><td>{DRAKE_L_PESSIMISTIC_YR:.0e} to {DRAKE_L_OPTIMISTIC_YR:.0e}</td><td>3</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Choose a real exoplanet system (this course's dataset or an instructor-approved alternative) and summarize its detection method, mass/radius/density classification, and orbital architecture in a short technical summary.</li>
<li>Evaluate the system against the classical habitable-zone boundaries (Lecture 09) and discuss any relevant climate-feedback or escape concerns (Lectures 08, 10).</li>
<li>Apply the biosignature false-positive decision logic (Lecture 11) to a hypothetical atmospheric detection for this system, and state what additional data would strengthen or weaken a biosignature claim.</li>
<li>Compute your own personally justified Drake equation estimate, stating explicit, defended values for f_l, f_i, f_c, and L, and identify which single term dominates your uncertainty.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>State explicitly, for every claim in your synthesis, whether it is directly measured/live-verified, a standard published value requiring human spot-check, or a personal, explicitly labeled illustrative assumption (this course's tri-level provenance scheme, applied to your own capstone writing).</p></section>
<section><h2>Deliverables</h2><ul><li>A complete written synthesis (recommended 1000-1500 words) covering detection, characterization, habitability, and biosignature reasoning for the chosen system.</li><li>A personally computed and justified Drake equation estimate with explicit term-by-term reasoning.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correctly synthesizes at least three distinct tools from this course's preceding six labs.</li><li>Explicit, correctly applied habitable-zone and biosignature false-positive reasoning.</li><li>Personally justified (not copied) Drake equation term values with a clearly identified dominant-uncertainty term.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}</li><li>See <code>materials/ASTR350/reference-log.md</code> for this course's full data-provenance table.</li></ul></section>
"""
    return lab_page(7, 'Capstone: Full-System Synthesis and the Drake Equation',
                     'Synthesize this course\'s full toolkit for a real exoplanet system and compute a personally justified Drake equation estimate.', sections)


def make_pset_07():
    problems = problem(1, 'Drake equation with your own assumptions',
                        f'<p>Using R*={DRAKE_R_STAR}, f_p={DRAKE_F_P}, n_e={DRAKE_N_E} (this course\'s adopted astronomical terms), choose and justify your own values for f_l, f_i, f_c, and L, and compute your resulting N. State which of your four chosen values you are least confident in and why.</p>', points=25) + \
               problem(2, 'Dominant uncertainty term',
                       f'<p>Compare your Problem 1 result to this course\'s own computed optimistic ({N_CIV_OPTIMISTIC:.1e}) and pessimistic ({N_CIV_PESSIMISTIC:.1e}) bounds, and state whether your assumptions are closer to the optimistic or pessimistic end, and which single term is responsible for most of that difference.</p>', points=20) + \
               problem(3, 'Full synthesis critique',
                       '<p>Choose one real exoplanet system from this course\'s dataset (or, with instructor approval, another well-characterized real system) and write a 300-500 word critique of what a claimed biosignature detection for that system could and could not scientifically establish, explicitly citing at least two named false-positive or degeneracy concerns from this course (e.g., the mass-radius composition degeneracy, the abiotic-oxygen pathway, the growth-versus-survival distinction).</p>', points=30) + \
               problem(4, 'Honest limits statement',
                       '<p>In two to three sentences, state the single most important scientific limitation on current exoplanet life detection that this course has emphasized, and explain why acknowledging it explicitly (rather than glossing over it) makes a scientific claim stronger, not weaker.</p>', points=25)
    return pset_page(7, 'Capstone Synthesis', 'Apply the full semester\'s toolkit to a real system and a personal Drake equation estimate.', problems, OPENSTAX)


def make_pset_07_solutions():
    s = solution(1, 'Drake equation with your own assumptions',
                 '<p>Any internally consistent, explicitly justified set of values is acceptable; full credit requires the calculation to be shown correctly (N = R* f_p n_e f_l f_i f_c L) with the student\'s own stated f_l, f_i, f_c, L, and a genuine (not perfunctory) statement of which value is least confident.</p>',
                 [('Correct equation setup and arithmetic with the student\'s own values', 12), ('Genuine, specific justification for each of the four chosen values', 8), ('Genuine (not perfunctory) least-confident-term statement', 5)], ) + \
        solution(2, 'Dominant uncertainty term',
                 f'<p>Full credit requires an accurate comparison of the student\'s own N to the {N_CIV_PESSIMISTIC:.1e}-{N_CIV_OPTIMISTIC:.1e} range and a correct identification that the spread is dominated by the biological terms (f_l especially, given its factor-of-10^4 assumed range in this course\'s own bounding calculation), not by the astronomical terms.</p>',
                 [('Correct comparison to this course\'s bounds', 10), ('Correct identification of the dominant (biological) term', 10)]) + \
        solution(3, 'Full synthesis critique',
                 '<p>Full credit requires a coherent 300-500 word critique that correctly explains at least two named false-positive/degeneracy concerns (mass-radius composition degeneracy, Lecture 06; abiotic-oxygen false positive, Lecture 11; growth-versus-survival distinction, Lecture 12; or the classical-HZ-is-not-sufficient caveat, Lecture 10) as applied specifically to the chosen system, not as generic statements.</p>',
                 [('Coherent, well-organized critique of appropriate length', 10), ('Correct, system-specific application of at least two named concerns', 15), ('Scientifically honest, appropriately hedged conclusion', 5)]) + \
        solution(4, 'Honest limits statement',
                 '<p>Any well-reasoned answer is acceptable (e.g., the mass-radius composition degeneracy, the abiotic-oxygen false positive, or the unconstrained biological Drake terms); full credit requires a genuine explanation of why stating the limitation strengthens rather than weakens the scientific claim (because an unacknowledged limitation invites a valid rebuttal, while an acknowledged one shows the claim has been tested against its most likely objection).</p>',
                 [('Correctly identified, course-supported limitation', 12), ('Genuine explanation of why acknowledging it strengthens the claim', 13)])
    return solutions_page(7, 'Capstone Synthesis', s)


def make_pset_07_assessment():
    return assessment_md(7, 'Capstone Synthesis',
                          ['Problem 1: any internally consistent, justified value set is acceptable; verify the arithmetic and justification, not a specific "correct" answer.',
                           'Problem 2: verify correct identification of the biological terms (not the astronomical terms) as the dominant source of uncertainty.',
                           'Problem 3: verify at least two named, course-specific concerns are applied to the chosen system specifically, not stated generically.',
                           'Problem 4: accept any well-reasoned, course-supported limitation; verify the "why it strengthens the claim" reasoning is genuine, not perfunctory.'],
                          ['Treating the Drake equation\'s output as a precise prediction rather than an explicitly uncertain, order-of-magnitude estimate (the core Lecture 14 pitfall).',
                           'Writing a generic biosignature critique that does not engage with the specific chosen system\'s real characteristics.'])


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
    for i, (fn_p, fn_s, fn_a) in enumerate(psets, start=1):
        (PSET_DIR / f'problem-set-{i:02d}.html').write_text(fn_p(), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-solutions.html').write_text(fn_s(), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-assessment.md').write_text(fn_a(), encoding='utf-8')


if __name__ == '__main__':
    write_labs_and_psets()
    print('Wrote 7 labs and 7 problem sets (with solutions and assessment instructions).')
