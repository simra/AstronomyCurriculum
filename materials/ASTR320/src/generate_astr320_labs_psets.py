"""Lab and problem-set generator for ASTR320.

Depends on the shared constants and page()/CSS helpers in
generate_astr320_content.py so every number here traces back to the same
verified real data (solar system planetary parameters; TRAPPIST-1, live-
verified this session) used in the paired lectures. Run with the project
interpreter, after generate_astr320_content.py:
    python materials/ASTR320/src/generate_astr320_content.py
    python materials/ASTR320/src/generate_astr320_labs_psets.py
"""
from __future__ import annotations

import math
from html import escape

from generate_astr320_content import (
    CSS, page, li, LAB_DIR, PSET_DIR,
    G_NEWTON, SIGMA_SB, K_BOLTZMANN, M_PROTON, AU_M, DAY_S, YEAR_S, L_SUN_W,
    M_SUN_KG, R_SUN_M,
    PLANETS, MOON, EARTH_ATM_SCALE_HEIGHT_M, EARTH_SURFACE_G,
    JUPITER_MASS_KG, IO, EUROPA, ENCELADUS,
    SATURN, SATURN_A_RING_OUTER_M, ICE_DENSITY_KGM3, SATURN_MEAN_DENSITY_KGM3,
    TRAPPIST1_STAR, TRAPPIST1_PLANETS, TRAPPIST1_LUM_W, TRAPPIST1_TEQ,
    equilibrium_temperature_k, scale_height_m, roche_limit_rigid_m, roche_limit_fluid_m,
    jeans_parameter, surface_gravity, escape_velocity, thermal_speed_most_probable,
    tidal_acceleration, DENSITIES, GRAVITIES, ESCAPE_VS, TEQ_ZERO_ALBEDO, TEQ_BOND,
    EARTH_H_N2, VENUS_G, VENUS_H_CO2, MARS_G, MARS_H_CO2,
    EARTH_ESCAPE_V, MARS_ESCAPE_V, EARTH_TEQ_ZERO_ALBEDO,
    ROCHE_ICE_SATURN_M, ROCHE_ICE_SATURN_RS, ROCHE_FLUID_SATURN_M, ROCHE_FLUID_SATURN_RS, A_RING_OUTER_RS,
    IO_TIDAL_A, IO_OWN_G, IO_TIDAL_FRAC, EUROPA_TIDAL_A, EUROPA_OWN_G, EUROPA_TIDAL_FRAC,
    ENCELADUS_TIDAL_A, ENCELADUS_OWN_G, ENCELADUS_TIDAL_FRAC,
    AMU, H2_MASS, N2_MASS, CO2_MASS,
)

OPENSTAX = 'OpenStax Astronomy 2e (local reference copy: references/openstax-astronomy-2e-extracted.txt)'


def fmt(x, nd=3):
    return f"{x:.{nd}g}"


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
    return page(f'ASTR 320 Lab {n:02d}', body)


def pset_page(n: int, title: str, focus: str, problems_html: str, reading: str) -> str:
    body = f"""<header><div><h1>ASTR 320 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header>
<main><section><h2>Problems</h2>{problems_html}</section>
<section><h2>Due and Scope</h2><p>Submit a complete derivation with equations, units, labeled quantities, and a short narrative interpretation for each problem. Show every step; a correct final number without a visible derivation receives partial credit at most, and quoting a lecture number without adapting it to this problem's specific inputs receives no credit for that step.</p></section>
<section><h2>OpenStax Companion Reading</h2><p>{escape(reading)}</p></section>
<section><h2>References and Data Sources</h2><ul><li>Corresponding lecture slides and notes for this unit.</li><li>{OPENSTAX}.</li><li>Course datasets and constants under <code>materials/ASTR320/src/generate_astr320_content.py</code> where referenced above.</li></ul></section>
</main>"""
    return page(f'ASTR 320 Problem Set {n:02d}', body)


def solutions_page(n: int, title: str, solutions_html: str) -> str:
    body = (f"<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header>"
            f"<main><section><h2>Worked Solutions</h2>{solutions_html}</section>"
            f"<section><h2>Grading Notes</h2><p>Award full marks for correct method, units, and a numeric result "
            f"consistent with the arithmetic shown (allow reasonable rounding). Verify that the student re-derives "
            f"the number for this problem's specific inputs rather than quoting a lecture example without adaptation. "
            f"Watch specifically for unit-conversion errors (AU/m, days or years/seconds, bar/Pa) and for comparative-"
            f"magnitude statements stated in the wrong direction (e.g., a tidal acceleration or greenhouse excess "
            f"described as a multiple when it is actually a small fraction, or vice versa) -- these are the most "
            f"common sources of silent error in this course.</p></section></main>")
    return page(f'ASTR 320 Problem Set {n:02d} Solutions', body)


def assessment_md(n: int, title: str, criteria: list, common_errors: list) -> str:
    crit = '\n'.join(f'- {c}' for c in criteria)
    err = '\n'.join(f'- {e}' for e in common_errors)
    return f"""# Assessment Instructions: Problem Set {n:02d} \u2014 {title}

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the shared
constants in `materials/ASTR320/src/generate_astr320_content.py` where a problem reuses course data.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct
reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking
number but no visible derivation steps should not. Because this is a 300-level quantitative course, full marks require
a genuine derivation (not just formula substitution) wherever the problem set asks for one.

## Problem-Level Criteria
{crit}

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not
only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum
of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
{err}
"""


# ---------------------------------------------------------------------------
# Additional real, standard-published (level-2) datasets used only in labs
# and problem sets, not in the lectures, so lab/pset content is distinct
# from lecture worked examples while remaining internally consistent.
# ---------------------------------------------------------------------------
CERES = dict(mass=9.393e20, radius=469.7e3, a_au=2.7675)
VESTA = dict(mass=2.590e20, radius=262.7e3, a_au=2.3615)
PLUTO = dict(mass=1.303e22, radius=1188.3e3, a_au=39.48)
TITAN = dict(mass=1.3452e23, radius=2574.7e3, a_au=SATURN['a_au'], teff=93.7, albedo=0.22)
MERCURY_CMR2 = 0.346  # MESSENGER-derived value (Margot et al. 2018), standard published
EARTH_CMR2 = 0.3307
MARS_CMR2 = 0.3644
MOON_CMR2 = 0.3931
MARS_HEAT_FLOW_MWM2 = 22.0  # representative published estimate, InSight-adjacent modeling
EARTH_HEAT_FLOW_MWM2 = 91.5
K40_HALFLIFE_GYR = 1.25
U238_HALFLIFE_GYR = 4.47
TH232_HALFLIFE_GYR = 14.0
URANUS_B0_T = 2.28e-5  # equatorial surface field, standard published (Ness et al. 1986)
NEPTUNE_B0_T = 1.42e-5
JUPITER_B0_T = 4.28e-4
SOLAR_WIND_RHO_KGM3 = 8.4e-21
SOLAR_WIND_V_MS = 4.0e5
MU0 = 4 * math.pi * 1e-7


def magnetopause_distance_m(b0_t: float, radius_m: float, rho_sw: float, v_sw: float) -> float:
    """Pressure-balance standoff distance for a dipole field vs. solar-wind ram pressure."""
    p_sw = rho_sw * v_sw ** 2
    return radius_m * (b0_t ** 2 / (2 * MU0 * p_sw)) ** (1 / 6)


PHOBOS = dict(mass=1.0659e16, radius=11.267e3, a_m=9376e3, primary_mass=6.4171e23)
MIRANDA = dict(mass=6.6e19, radius=235.8e3, density=1200.0)
URANUS_DENSITY = PLANETS['Uranus']['mass'] / (4 / 3 * math.pi * PLANETS['Uranus']['radius'] ** 3)

KEPLER186F = dict(a_au=0.432, period_d=129.9, star_lum_lsun=0.041, radius_rearth=1.17)


# ---------------------------------------------------------------------------
# LAB 01: Testing the condensation sequence with Ceres and Vesta
# ---------------------------------------------------------------------------
def make_lab_01() -> str:
    ceres_density = CERES['mass'] / (4 / 3 * math.pi * CERES['radius'] ** 3)
    vesta_density = VESTA['mass'] / (4 / 3 * math.pi * VESTA['radius'] ** 3)
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This is a data-analysis lab using real, spacecraft-measured parameters for the
two most massive main-belt asteroids, Ceres and Vesta, both characterized in detail by NASA's Dawn mission
(2011-2018; standard published values, not independently re-verified by live fetch this session -- see
<code>../reference-log.md</code>). No telescope time is required; the lab tests Lecture 02's frost-line and
condensation-sequence prediction directly against two real bodies straddling the frost line.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Body</th><th>Mass (kg)</th><th>Radius (km)</th><th>Semimajor axis (AU)</th></tr></thead><tbody>
<tr><td>Ceres</td><td>{CERES['mass']:.3e}</td><td>{CERES['radius']/1000:.1f}</td><td>{CERES['a_au']}</td></tr>
<tr><td>Vesta</td><td>{VESTA['mass']:.3e}</td><td>{VESTA['radius']/1000:.1f}</td><td>{VESTA['a_au']}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute the mean density of Ceres and Vesta from their measured mass and radius, using the identical density formula from Lecture 01 (&rho; = M/(4/3&pi;R&sup3;)).</li>
<li>Using Lecture 02's frost-line estimate (&sim;2.8 AU from the equilibrium-temperature calculation, or your own recomputation of it), state whether each asteroid's semimajor axis places it inside, at, or beyond the frost line.</li>
<li>Compare the two computed densities to the terrestrial-planet and icy-body density ranges established in Lecture 01's table (terrestrial planets: &sim;3900-5510 kg/m&sup3;; icy satellites are typically 1000-2000 kg/m&sup3;) and state whether the condensation-sequence prediction (bodies closer to the frost line should be less dense/more ice-rich) is supported.</li>
<li>Ceres shows direct spectroscopic and gravity evidence (Dawn mission) for a partially differentiated interior with a hydrated, ice-and-salt-rich mantle, while Vesta shows a basaltic crust and an iron core (confirmed by its HED meteorite family, directly linked to Vesta by spectroscopy). Explain in one paragraph how this differentiation evidence is or is not consistent with your density comparison.</li>
<li>Estimate the uncertainty in each computed density given a plausible &plusmn;2% uncertainty in each body's measured radius (recall from Lecture 01 that density depends on R&#8315;&sup3;, so a small radius uncertainty is tripled in the resulting density uncertainty), and state whether this uncertainty could account for any part of the density difference found in step 3.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Because &rho; &prop; R&#8315;&sup3;, the fractional uncertainty in a body's computed density is approximately three times its fractional radius uncertainty (for a fixed, precisely known mass); Dawn's radar and imaging-derived radii for Ceres and Vesta are precise to well under 1%, so this uncertainty is small compared to the roughly 60% density difference between the two bodies, meaning the observed density contrast is a real physical result, not a measurement artifact.</p></section>
<section><h2>Deliverables</h2><ul><li>Computed densities for Ceres and Vesta, with full unit conversions shown.</li><li>A frost-line comparison stating each body's position relative to the &sim;2.8 AU frost line from Lecture 02.</li><li>A written paragraph connecting the density comparison to each body's independently known differentiation and meteorite-family evidence.</li><li>An uncertainty propagation estimate and a judgment of whether it could explain the observed density contrast.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct density calculation for both bodies with correct units.</li><li>Correct identification of each body's position relative to the frost line.</li><li>Written paragraph correctly connects density and differentiation evidence rather than treating them as unrelated facts.</li><li>Uncertainty propagation correctly applies the tripled fractional-uncertainty scaling for density versus radius.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Section 7.2 and Section 15.3 (asteroids).</li><li>Ceres and Vesta mass, radius, and orbital parameters: standard published Dawn mission values (Russell et al. 2012, 2016, <em>Science</em>), not independently re-verified by live fetch this session; see <code>materials/ASTR320/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR320/src/generate_astr320_labs_psets.py</code>.</li></ul></section>
"""
    return lab_page(1, 'Testing the Condensation Sequence with Ceres and Vesta',
                     'Use real Dawn-mission asteroid data to test whether bodies straddling the solar nebula frost line show the predicted density/composition contrast.', sections)


# ---------------------------------------------------------------------------
# PS 01: Solar nebula, condensation, and planet formation
# ---------------------------------------------------------------------------
def make_pset_01():
    plu_density = PLUTO['mass'] / (4 / 3 * math.pi * PLUTO['radius'] ** 3)
    titan_density = TITAN['mass'] / (4 / 3 * math.pi * TITAN['radius'] ** 3)
    frost_line_faint_au = math.sqrt(0.5 * L_SUN_W / (16 * math.pi * SIGMA_SB * 150.0 ** 4)) / AU_M
    frost_line_bright_au = math.sqrt(2.0 * L_SUN_W / (16 * math.pi * SIGMA_SB * 150.0 ** 4)) / AU_M
    problems = (
        problem(1, 'Density and Composition of Pluto',
                 f"<p>Pluto has mass {PLUTO['mass']:.3e} kg and radius {PLUTO['radius']/1000:.1f} km, and orbits at a mean "
                 f"semimajor axis of {PLUTO['a_au']} AU, far beyond the frost line. Compute Pluto's mean density and compare it "
                 f"to Ceres's and Vesta's densities from Lab 01 and to the icy-satellite density range from Lecture 01. "
                 f"State whether Pluto's density is consistent with the condensation-sequence prediction for a Kuiper Belt object.</p>"),
        problem(2, "Titan's Density and the Ice/Rock Mixture",
                 f"<p>Titan has mass {TITAN['mass']:.4e} kg and radius {TITAN['radius']/1000:.1f} km. Compute Titan's mean "
                 f"density. A pure water-ice body would have density &asymp; 917 kg/m&sup3;; a pure rocky body would have density "
                 f"&asymp; 3000 kg/m&sup3; or higher. Estimate, using a simple linear mixing argument, what mass fraction of rock "
                 f"(versus ice) Titan's bulk density implies, and state one reason this simple estimate is only approximate.</p>"),
        problem(3, 'Frost Line for a Fainter and a Brighter Young Star',
                 f"<p>Using the equilibrium-temperature-based frost-line method from Lecture 02 (setting T(r) = 150 K), compute "
                 f"the frost-line distance for a young star with (a) half the Sun's luminosity and (b) twice the Sun's "
                 f"luminosity. Compare both results to the Sun's own frost line (&sim;2.8 AU) and state, in one sentence, how "
                 f"frost-line distance scales with stellar luminosity.</p>"),
        problem(4, 'Runaway versus Oligarchic Growth: A Conceptual Comparison',
                 "<p>In two to three sentences each, explain (a) why gravitational focusing makes runaway growth "
                 "self-reinforcing for the largest body in a local planetesimal swarm, and (b) why oligarchic growth "
                 "eventually slows this process down once a few embryos dominate their feeding zones. Your answer must "
                 "reference the gravitational-focusing cross-section argument from Lecture 02, not just restate that "
                 "'bigger objects grow faster.'</p>"),
        problem(5, 'Critical Core Mass and the Gas Giant/Ice Giant Divide',
                 "<p>Jupiter's core accretion is estimated to have reached the &sim;5-10 Earth-mass critical core mass while "
                 "the gas disk still had several Myr of lifetime remaining, while Uranus's and Neptune's cores are thought "
                 "to have formed more slowly. Using the core-accretion argument from Lecture 02, explain quantitatively "
                 "(with reference to the &sim;90% hydrogen/helium mass fraction of Jupiter and Saturn versus the &sim;10-20% "
                 "hydrogen/helium mass fraction of Uranus and Neptune) why this timing difference alone is sufficient to "
                 "explain the compositional gas-giant/ice-giant divide.</p>"),
    )
    solutions = (
        solution(1, 'Density and Composition of Pluto',
                 f"<p>&rho; = M/(4/3&pi;R&sup3;) = {PLUTO['mass']:.3e} / [(4/3)&pi;({PLUTO['radius']:.4e})&sup3;] = "
                 f"{plu_density:.0f} kg/m&sup3;. This is well below any solid rocky-planet density (&gt;3900 kg/m&sup3;) and "
                 f"comparable to the icy-satellite range (1000-2000 kg/m&sup3;), consistent with Pluto being a Kuiper Belt "
                 f"object built largely from ices condensed far beyond the frost line, as the condensation sequence predicts.</p>",
                 [('Correct density calculation with unit conversion', 6), ('Correct comparison to icy-body density range', 5), ('Correct qualitative conclusion tied to condensation sequence', 4)]),
        solution(2, "Titan's Density and the Ice/Rock Mixture",
                 f"<p>&rho; = {TITAN['mass']:.4e} / [(4/3)&pi;({TITAN['radius']:.4e})&sup3;] = {titan_density:.0f} kg/m&sup3;. "
                 f"A simple linear mixing estimate, x&#183;3000 + (1-x)&#183;917 = {titan_density:.0f}, gives x &asymp; "
                 f"{(titan_density-917.0)/(3000.0-917.0):.2f}, i.e., roughly {(titan_density-917.0)/(3000.0-917.0)*100:.0f}% "
                 f"rock by mass. This estimate is only approximate because real planetary ices and rock do not simply "
                 f"average their densities when mixed (compression, porosity, and phase changes at Titan's actual internal "
                 f"pressures all modify the true mixed density), and because Titan is now known (from Cassini gravity data) "
                 f"to be at least partially differentiated rather than a uniform mixture.</p>",
                 [('Correct density calculation', 5), ('Correct linear-mixing rock-fraction estimate', 6), ('Correctly identifies a specific limitation of the simple mixing model', 4)]),
        solution(3, 'Frost Line for a Fainter and a Brighter Young Star',
                 f"<p>r = &radic;[L/(16&pi;&sigma;T&#8308;)], so r &prop; &radic;L. For L = 0.5 L&#8857;: r = "
                 f"{frost_line_faint_au:.2f} AU. For L = 2 L&#8857;: r = {frost_line_bright_au:.2f} AU. Compared to the Sun's "
                 f"own frost line (&sim;2.8 AU), the frost line moves inward for a fainter young star and outward for a "
                 f"brighter one, scaling as the square root of luminosity.</p>",
                 [('Correct application of the frost-line formula to both cases', 8), ('Correctly states the sqrt(L) scaling', 7)]),
        solution(4, 'Runaway versus Oligarchic Growth: A Conceptual Comparison',
                 "<p>(a) Runaway growth is self-reinforcing because an embryo's effective gravitational-focusing cross-section "
                 "grows with its own escape velocity relative to the surrounding planetesimals' velocity dispersion (cross-"
                 "section &prop; 1 + (v_esc/v_rel)&sup2;), so a slightly larger embryo accretes disproportionately faster, "
                 "widening the gap with its neighbors. (b) Oligarchic growth slows this process once a handful of embryos "
                 "dominate their local feeding zones, because each embryo's own gravity begins to stir up (increase the "
                 "velocity dispersion of) the remaining planetesimals in its zone, reducing the gravitational-focusing "
                 "advantage and roughly equalizing growth rates among the surviving embryos.</p>",
                 [('Correctly explains runaway growth via gravitational focusing (not just size)', 8), ('Correctly explains the transition to oligarchic growth via self-stirring', 7)]),
        solution(5, 'Critical Core Mass and the Gas Giant/Ice Giant Divide',
                 "<p>Once a core exceeds the critical mass (&sim;5-10 Earth masses), runaway gas accretion can capture "
                 "hundreds of Earth masses of hydrogen/helium within &sim;10&#8308;-10&#8309; years, but only if the gas disk is "
                 "still present. If Jupiter's and Saturn's cores reached this threshold with several Myr of disk lifetime "
                 "remaining, they could accrete gas for an extended period, explaining their &sim;90%+ hydrogen/helium "
                 "composition. If Uranus's and Neptune's cores formed more slowly (plausible given the much lower disk "
                 "density at 19-30 AU) and only reached, or never fully reached, the critical mass shortly before the gas "
                 "disk dispersed, they would have captured only a comparatively small hydrogen/helium envelope before the "
                 "gas supply ran out, leaving them dominated by their icy/rocky cores -- exactly the observed &sim;10-20% "
                 "hydrogen/helium mass fraction.</p>",
                 [('Correctly explains the critical-mass/runaway-accretion mechanism', 7), ('Correctly connects accretion timing to the observed compositional divide', 8)]),
    )
    pset_html = pset_page(1, 'Solar Nebula, Condensation, and Planet Formation',
                           'Apply the frost-line, condensation-sequence, and core-accretion concepts from Lectures 01-02 to real dwarf planets, satellites, and formation-timing arguments.',
                           ''.join(problems), 'OpenStax Astronomy 2e, Sections 7.2 and 8.5.')
    sol_html = solutions_page(1, 'Solar Nebula, Condensation, and Planet Formation', ''.join(solutions))
    asmt = assessment_md(1, 'Solar Nebula, Condensation, and Planet Formation',
                          ['Problem 1: density calculation and icy-body comparison both required for full credit.',
                           'Problem 2: linear-mixing estimate must show the algebra, not just state a rock fraction.',
                           'Problem 3: both frost-line values and the sqrt(L) scaling statement are required.',
                           'Problem 4: answer must invoke gravitational focusing and self-stirring specifically, not generic size arguments.',
                           'Problem 5: answer must connect accretion timing to the specific observed compositional percentages.'],
                          ['Forgetting to convert radius from km to m before computing density (an extremely common unit-conversion slip).',
                           'Treating density differences as automatically proof of composition without considering measurement uncertainty (Problem 1).',
                           'Applying the frost-line formula without correctly propagating the square-root scaling with luminosity (Problem 3).'])
    return pset_html, sol_html, asmt


# ---------------------------------------------------------------------------
# LAB 02: Moment of inertia and radiogenic heat budget, Earth vs. Mars
# ---------------------------------------------------------------------------
def make_lab_02() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This is a data-analysis lab combining two independent real datasets: measured
moment of inertia factors (from spacecraft tracking and precession) and measured/modeled surface heat flow, for Earth
and Mars. Standard published values, not independently re-verified by live fetch this session (see
<code>../reference-log.md</code>).</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Body</th><th>C/MR&sup2;</th><th>Mean surface heat flow (mW/m&sup2;)</th><th>Mean radius (km)</th></tr></thead><tbody>
<tr><td>Earth</td><td>{EARTH_CMR2}</td><td>{EARTH_HEAT_FLOW_MWM2}</td><td>{PLANETS['Earth']['radius']/1000:.1f}</td></tr>
<tr><td>Mars</td><td>{MARS_CMR2}</td><td>{MARS_HEAT_FLOW_MWM2}</td><td>{PLANETS['Mars']['radius']/1000:.1f}</td></tr>
<tr><td>Moon</td><td>{MOON_CMR2}</td><td>16-21 (Apollo heat-flow probes)</td><td>{MOON['radius']/1000:.1f}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using the moment-of-inertia deviation-from-uniform method demonstrated in Lecture 03 (deviation from the uniform-sphere value 0.4), rank Earth, Mars, and the Moon from most to least core-concentrated, and state what this ranking implies about relative core size (as a fraction of planetary radius) for each body.</li>
<li>Compute the ratio of Earth's to Mars's mean surface heat flow, and compare it to the ratio of their radii cubed (a proxy for total volume, and hence for total radiogenic heat generation, if radiogenic element concentration per unit mass were identical).</li>
<li>Using the surface-to-volume cooling scaling argument from Lecture 04 (heat loss/generation ratio &prop; 1/R), predict qualitatively which planet should show a higher heat flow per unit surface area, and check whether your data are consistent with that prediction.</li>
<li>Using the radiogenic decay law from Lecture 04, compute what fraction of &#8308;&#8308;K's original (4.5 Gyr ago) abundance remains today, and explain in one paragraph why this isotope was proportionally more important to a planet's heat budget in its early history than it is now.</li>
<li>Mars's moment of inertia factor (0.3644) is intermediate between Earth's (0.3307) and the Moon's (0.3931). State whether Mars's heat flow, given in the data table, is also intermediate between Earth's and the Moon's, and discuss in one paragraph whether core size and heat flow should necessarily track each other exactly.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Mars's heat flow value in this lab is a representative published geophysical estimate rather than a directly measured value, because InSight's HP&sup3; heat-flow probe did not achieve its planned burial depth; students should treat this number as having larger uncertainty than Earth's or the Moon's directly measured heat flow values, and should state this explicitly in their analysis.</p></section>
<section><h2>Deliverables</h2><ul><li>A ranked comparison of core concentration (via C/MR&sup2;) for Earth, Mars, and the Moon.</li><li>A computed heat-flow ratio and volume-ratio comparison for Earth and Mars.</li><li>A radiogenic decay-law calculation for &#8308;&#8308;K's remaining fraction after 4.5 Gyr.</li><li>Written paragraphs addressing the surface-to-volume prediction and the core-size/heat-flow relationship.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct ranking and interpretation of moment-of-inertia deviations.</li><li>Correct heat-flow ratio and volume-ratio arithmetic.</li><li>Correct radiogenic decay-law calculation with the correct half-life and decay constant.</li><li>Written analysis correctly distinguishes core size (a static structural property) from heat flow (a dynamic, time-dependent property) rather than conflating the two.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Section 9.1.</li><li>Moment of inertia factors and heat-flow values: standard published geophysical values (Earth and Moon well established; Mars heat flow a representative modeled estimate given InSight's incomplete HP&sup3; deployment), not independently re-verified by live fetch this session; see <code>materials/ASTR320/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR320/src/generate_astr320_labs_psets.py</code>.</li></ul></section>
"""
    return lab_page(2, "Moment of Inertia and Radiogenic Heat Budget: Earth versus Mars",
                     "Combine moment-of-inertia and heat-flow data to test whether core concentration and heat flow track each other across three terrestrial bodies.", sections)


# ---------------------------------------------------------------------------
# PS 02: Interior structure and heat budgets
# ---------------------------------------------------------------------------
def make_pset_02():
    lam_k40 = math.log(2) / K40_HALFLIFE_GYR
    lam_u238 = math.log(2) / U238_HALFLIFE_GYR
    lam_th232 = math.log(2) / TH232_HALFLIFE_GYR
    mercury_deviation = (0.4 - MERCURY_CMR2) / 0.4 * 100
    earth_deviation = (0.4 - EARTH_CMR2) / 0.4 * 100
    problems = (
        problem(1, "Mercury's Moment of Inertia and Core Size",
                 f"<p>MESSENGER measurements give Mercury's moment of inertia factor as C/MR&sup2; = {MERCURY_CMR2}. Compute "
                 f"its percent deviation below the uniform-sphere value of 0.4, and compare this deviation to Earth's "
                 f"({earth_deviation:.1f}% computed from C/MR&sup2; = {EARTH_CMR2}). State what this comparison implies about "
                 f"Mercury's core, in light of Lecture 03's giant-impact hypothesis for Mercury's anomalously large core.</p>"),
        problem(2, "Radiogenic Heat Production 2 Gyr Ago",
                 f"<p>Using the decay constants &#955; = ln2/t&#8321;&#8260;&sup2; for &#8308;&#8308;K (t&#8321;&#8260;&sup2; = "
                 f"{K40_HALFLIFE_GYR} Gyr) and &sup2;&sup3;&#8310;U (t&#8321;&#8260;&sup2; = {U238_HALFLIFE_GYR} Gyr), compute "
                 f"what fraction of each isotope's present-day abundance existed 2 Gyr ago (i.e., the ratio of abundance at "
                 f"t = -2 Gyr relative to today, noting this ratio is e&#8314;&#955;t for t = 2 Gyr since we are looking "
                 f"backward in time). Explain which isotope's heat contribution changed more dramatically over this "
                 f"interval and why.</p>"),
        problem(3, "Surface-to-Volume Scaling for Io versus the Moon",
                 "<p>Io (radius 1821.6 km) and the Moon (radius 1737.4 km) are nearly the same size, yet Io is the most "
                 "volcanically active body in the solar system while the Moon is essentially geologically dead. Using the "
                 "surface-to-volume cooling argument from Lecture 04, explain why this argument alone would predict "
                 "similar (low) geological activity for both bodies, and then explain what additional physical mechanism "
                 "(introduced in Lecture 04 as a preview and developed fully in Lecture 13) resolves this apparent "
                 "contradiction.</p>"),
        problem(4, "Rayleigh Number Scaling",
                 "<p>The Rayleigh number is Ra = (&rho;g&alpha;&Delta;Td&sup3;)/(&kappa;&mu;). If a planet's mantle thickness "
                 "d were doubled while all other quantities (&rho;, g, &alpha;, &Delta;T, &kappa;, &mu;) stayed fixed, by what "
                 "factor would its Rayleigh number change? Given that Earth's mantle Rayleigh number is estimated at "
                 "10&#8310;-10&#8311;, vastly above the critical value of &sim;1000-2000, would this change plausibly push a "
                 "convecting mantle below the critical threshold into a non-convecting regime? Justify your answer "
                 "quantitatively.</p>"),
        problem(5, "Comparing Bulk Silicate Earth's Heat Budget to Observed Heat Flow",
                 "<p>Earth's present-day radiogenic heat production is estimated at roughly 20 TW, while its total observed "
                 "surface heat flow is roughly 47 TW. Compute the percent of Earth's total heat flow that is NOT accounted "
                 "for by present-day radiogenic heat production, and explain, using the concept introduced in Lecture 04, "
                 "what additional heat source is thought to make up this difference.</p>"),
    )
    solutions = (
        solution(1, "Mercury's Moment of Inertia and Core Size",
                 f"<p>Mercury: (0.4 - {MERCURY_CMR2})/0.4 &times; 100 = {mercury_deviation:.1f}%. Earth: {earth_deviation:.1f}%. "
                 f"Mercury's deviation below the uniform-sphere value is substantially larger than Earth's, implying an "
                 f"even more strongly core-concentrated interior relative to its total size than Earth's -- consistent "
                 f"with Mercury's core occupying an unusually large fraction (&sim;85%) of its radius, and with the "
                 f"giant-impact hypothesis that one or more early impacts stripped away a disproportionate share of "
                 f"Mercury's original silicate mantle, leaving its iron core relatively more dominant than on any other "
                 f"terrestrial planet.</p>",
                 [('Correct percent-deviation calculation for Mercury', 6), ('Correct comparison to Earth\'s deviation', 5), ('Correct connection to the giant-impact hypothesis', 4)]),
        solution(2, "Radiogenic Heat Production 2 Gyr Ago",
                 f"<p>Fraction 2 Gyr ago relative to today = e&#8314;&#955;t. For &#8308;&#8308;K: e&#8314;({lam_k40:.4f})(2) = "
                 f"{math.exp(lam_k40*2.0):.3f}, i.e., &#8308;&#8308;K was about {math.exp(lam_k40*2.0):.2f} times more abundant "
                 f"(and hence produced about {math.exp(lam_k40*2.0):.2f} times more heat) 2 Gyr ago than today. For "
                 f"&sup2;&sup3;&#8310;U: e&#8314;({lam_u238:.4f})(2) = {math.exp(lam_u238*2.0):.3f}, only about "
                 f"{math.exp(lam_u238*2.0):.2f} times more abundant. &#8308;&#8308;K's much shorter half-life (1.25 Gyr versus "
                 f"4.47 Gyr) means its heat contribution changed far more dramatically over this interval than "
                 f"&sup2;&sup3;&#8310;U's, which decays much more slowly and so contributed comparably to both eras.</p>",
                 [('Correct decay-law calculation for both isotopes', 8), ('Correct identification and explanation of which isotope changed more', 7)]),
        solution(3, "Surface-to-Volume Scaling for Io versus the Moon",
                 "<p>Because Io and the Moon are nearly the same size, the surface-to-volume scaling argument (heat loss/"
                 "generation &prop; 1/R) predicts nearly identical cooling rates and hence nearly identical present-day "
                 "geological activity for both bodies -- both should have long since radiated away their formation-era and "
                 "radiogenic heat and become geologically quiescent. This prediction is correct for the Moon but "
                 "dramatically wrong for Io, because Io receives an enormous additional, non-radiogenic heat source: "
                 "tidal heating, sustained by its orbital resonance with Europa and Ganymede (Lecture 13), which has no "
                 "analog for the Moon (whose orbit around Earth has already circularized and is not maintained in a "
                 "forced-eccentricity resonance with another body).</p>",
                 [('Correctly applies the surface-to-volume argument to predict similar activity', 7), ('Correctly identifies tidal heating/resonance as the resolving mechanism', 8)]),
        solution(4, "Rayleigh Number Scaling",
                 "<p>Since Ra &prop; d&sup3;, doubling d increases Ra by a factor of 2&sup3; = 8. Starting from Ra &sim; "
                 "10&#8310;-10&#8311; and multiplying by 8 gives Ra &sim; 8&times;10&#8310;-8&times;10&#8311;, still vastly above "
                 "the critical value of &sim;1000-2000 by four to five orders of magnitude. This change would not plausibly "
                 "push Earth's mantle into a non-convecting regime; Earth's mantle convection is so strongly super-"
                 "critical that even an order-of-magnitude change in a single parameter would not be sufficient to "
                 "suppress convection.</p>",
                 [('Correct cubic scaling calculation', 8), ('Correct quantitative conclusion about remaining super-criticality', 7)]),
        solution(5, "Comparing Bulk Silicate Earth's Heat Budget to Observed Heat Flow",
                 "<p>(47 - 20)/47 &times; 100 &asymp; 57%. Just over half of Earth's total observed surface heat flow is not "
                 "accounted for by present-day radiogenic heat production alone. Lecture 04 attributes this difference to "
                 "secular cooling: Earth's core and mantle are still releasing heat left over from formation and "
                 "differentiation (accretional and differentiation heat, discussed as one-time heat sources at the start "
                 "of Lecture 04), in addition to their ongoing radiogenic heat production.</p>",
                 [('Correct percent calculation', 7), ('Correctly identifies secular cooling as the additional source', 8)]),
    )
    pset_html = pset_page(2, 'Interior Structure and Heat Budgets',
                           'Apply moment-of-inertia interpretation, the Rayleigh-number criterion, and the radiogenic decay law from Lectures 03-04 to Mercury, Io, and Earth\'s overall heat budget.',
                           ''.join(problems), 'OpenStax Astronomy 2e, Section 9.1-9.2.')
    sol_html = solutions_page(2, 'Interior Structure and Heat Budgets', ''.join(solutions))
    asmt = assessment_md(2, 'Interior Structure and Heat Budgets',
                          ['Problem 1: both percent-deviation values must be computed and correctly compared.',
                           'Problem 2: correct exponential-decay direction (looking backward in time uses e^{+lambda t}, not e^{-lambda t}) is required.',
                           'Problem 3: answer must explicitly name tidal heating/orbital resonance as the resolving mechanism, not a vague reference to "different composition."',
                           'Problem 4: cubic scaling must be shown explicitly (not just stated).',
                           'Problem 5: percent calculation and correct naming of secular cooling both required.'],
                          ['Sign error in the decay-law direction when computing a past abundance rather than a future one (Problem 2).',
                           'Confusing static core-size deviation with dynamic, time-dependent heat flow as though they must always track each other (Problem 3 context).',
                           'Forgetting to cube the ratio in the Rayleigh-number scaling problem (a linear-scaling error).'])
    return pset_html, sol_html, asmt


# ---------------------------------------------------------------------------
# LAB 03: Crater scaling and surface age dating using real lunar mare data
# ---------------------------------------------------------------------------
MARE_TRANQUILLITATIS_AGE_GYR = 3.7
MARE_TRANQUILLITATIS_CRATER_DENSITY = 3.5e-3  # craters/km^2 above 1 km diameter, representative published value
MARE_IMBRIUM_AGE_GYR = 3.85
MARE_IMBRIUM_CRATER_DENSITY = 2.7e-3
HIGHLANDS_AGE_GYR = 4.3
HIGHLANDS_CRATER_DENSITY = 2.0e-2


def make_lab_03() -> str:
    slope = (MARE_TRANQUILLITATIS_CRATER_DENSITY - MARE_IMBRIUM_CRATER_DENSITY) / (MARE_TRANQUILLITATIS_AGE_GYR - MARE_IMBRIUM_AGE_GYR)
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab uses real, radiometrically anchored lunar chronology calibration
points from Apollo sample-return sites, following the lunar chronology function methodology introduced in Lecture 06.
Representative published crater densities (craters per km&sup2; above 1 km diameter) are provided for three
radiometrically dated regions.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Region</th><th>Radiometric age (Gyr)</th><th>Crater density (craters/km&sup2;, D&gt;1 km)</th></tr></thead><tbody>
<tr><td>Mare Tranquillitatis (Apollo 11 site)</td><td>{MARE_TRANQUILLITATIS_AGE_GYR}</td><td>{MARE_TRANQUILLITATIS_CRATER_DENSITY}</td></tr>
<tr><td>Mare Imbrium (Apollo 15 site)</td><td>{MARE_IMBRIUM_AGE_GYR}</td><td>{MARE_IMBRIUM_CRATER_DENSITY}</td></tr>
<tr><td>Lunar highlands (Apollo 16 site)</td><td>{HIGHLANDS_AGE_GYR}</td><td>{HIGHLANDS_CRATER_DENSITY}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Plot (by hand or with a simple script) crater density versus radiometric age for the three calibration points, and note that the relationship is strongly nonlinear (crater density rises much more steeply for the oldest surfaces), consistent with the higher impact flux before &sim;3.8-3.9 Gyr ago described in Lecture 06.</li>
<li>Using a simple local linear interpolation between the two youngest points (Tranquillitatis and Imbrium) as an approximation, estimate the local slope of crater density versus age in this age range, and use it to estimate the age of a hypothetical fourth surface with crater density 3.1 &times; 10&#8315;&sup3; craters/km&sup2;.</li>
<li>Explain, in one paragraph, why this same local linear interpolation would give a badly wrong age estimate if applied to a much older surface (e.g., one with crater density comparable to the highlands value), and connect your answer to the nonlinearity noted in step 1.</li>
<li>Using the pi-group crater-scaling relation from Lecture 06 (D &prop; E&sup2;&#8260;&#8309;), estimate by what factor the final crater diameter increases if an impactor's kinetic energy increases by a factor of 100.</li>
<li>List two specific sources of systematic uncertainty (from Lecture 06's discussion) that would affect a crater-count age estimate for a surface that had never been sampled by any lander, and explain briefly how each one could bias the estimated age.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The local linear interpolation used in step 2 is explicitly an approximation, valid only over a narrow age range where the true crater-density-versus-age curve is not changing its slope too rapidly; extending it far beyond the calibration points it was fit to (as the highlands comparison in step 3 illustrates) is a common and serious methodological error in real crater-count studies.</p></section>
<section><h2>Deliverables</h2><ul><li>A plot or table of crater density versus age for the three calibration points.</li><li>A computed local slope and an age estimate for the hypothetical fourth surface.</li><li>A written explanation of why linear interpolation fails when extrapolated to much older surfaces.</li><li>The crater-scaling factor computed from the pi-group relation.</li><li>Two specific, correctly explained sources of systematic uncertainty.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct slope and interpolated-age calculation.</li><li>Correct qualitative and quantitative explanation of chronology-function nonlinearity.</li><li>Correct application of the D &prop; E&sup2;&#8260;&#8309; scaling relation.</li><li>Two distinct, correctly explained uncertainty sources (not the same source restated twice).</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Section 9.5 (cratering) and Section 9.6 (the Moon).</li><li>Crater density values are representative published estimates consistent with the lunar chronology function (Neukum et al. 2001; Stoffler & Ryder 2001), not independently re-verified by live fetch this session; radiometric ages are standard published Apollo sample-return results; see <code>materials/ASTR320/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR320/src/generate_astr320_labs_psets.py</code>.</li></ul></section>
"""
    return lab_page(3, 'Crater-Count Chronology Using Real Lunar Calibration Data',
                     'Use radiometrically anchored Apollo-site crater densities to test the lunar chronology function\'s local linearity and its limits.', sections)


# ---------------------------------------------------------------------------
# PS 03: Impact cratering and comparative surface geology
# ---------------------------------------------------------------------------
def make_pset_03():
    tunguska_d_km = 0.06  # impactor diameter estimate, km (representative)
    tunguska_v = 15000.0
    tunguska_rho = 2000.0
    tunguska_mass = 4/3*math.pi*(tunguska_d_km*500)**3*tunguska_rho
    tunguska_energy = 0.5*tunguska_mass*tunguska_v**2
    tunguska_mt = tunguska_energy/4.184e15
    olympus_mons_height_km = 22.0
    olympus_mons_diameter_km = 600.0
    hawaii_chain_length_km = 2400.0
    pacific_plate_speed_cmyr = 7.0
    hawaii_age_myr = hawaii_chain_length_km*1e5/(pacific_plate_speed_cmyr)/1e6
    problems = (
        problem(1, 'Estimating the Tunguska Event Energy',
                 f"<p>The 1908 Tunguska event is estimated to have involved a stony/icy impactor roughly 60 m in diameter "
                 f"striking at &sim;15 km/s (it exploded in the atmosphere before reaching the ground, an airburst rather "
                 f"than a cratering impact, but its kinetic energy can still be estimated the same way). Using an assumed "
                 f"density of 2000 kg/m&sup3;, compute the impactor's kinetic energy and express it in megatons of TNT "
                 f"equivalent (1 MT = 4.184 &times; 10&#185;&#8309; J). Compare your result to the commonly cited estimate of "
                 f"3-15 megatons for the Tunguska event.</p>"),
        problem(2, 'Olympus Mons and the Hawaiian Hotspot Track',
                 f"<p>The Pacific Plate moves at roughly {pacific_plate_speed_cmyr} cm/yr over the fixed Hawaiian hotspot, "
                 f"and the resulting Hawaiian-Emperor seamount chain is roughly {hawaii_chain_length_km} km long. Estimate "
                 f"the total time this chain took to form, in millions of years, and compare it to the estimated multi-"
                 f"hundred-million-year construction time of Mars's single, stationary Olympus Mons ({olympus_mons_height_km} "
                 f"km tall, {olympus_mons_diameter_km} km diameter). Explain, referencing Lecture 05's plate-tectonic "
                 f"argument, why Mars produced one enormous volcano rather than a long chain of smaller ones.</p>"),
        problem(3, 'Crater Density and Venus\u2019s Resurfacing Event',
                 "<p>Venus's crater population is far below saturation and shows a narrow range of degradation states "
                 "across its entire surface, despite Venus being 4.5 Gyr old. Using the concepts from Lectures 05-06, "
                 "explain in a short paragraph why this observation supports a discrete, relatively recent (&sim;300-700 "
                 "Myr ago) global resurfacing event rather than either (a) a surface that has simply never been struck by "
                 "many impactors, or (b) a surface that formed recently at the same time as the planet itself.</p>"),
        problem(4, 'Simple versus Complex Crater Transition',
                 "<p>The simple-to-complex crater transition diameter is expected to be smaller on more massive bodies "
                 "(because stronger gravity more effectively collapses the initial transient cavity). Mars (g = 3.71 "
                 "m/s&sup2;) has stronger surface gravity than the Moon (g = 1.62 m/s&sup2;), so gravity alone predicts "
                 "Mars should have a <em>smaller</em> transition diameter than the Moon. Yet published values give the "
                 "Moon a transition diameter of roughly 2-4 km, while Mars's is roughly 5-10 km -- <em>larger</em>, the "
                 "opposite of the gravity-only prediction. Explain, in a short paragraph, why this is not actually a "
                 "contradiction of the underlying physics.</p>"),
        problem(5, 'Mercury\u2019s Crater-Count Volcanic History',
                 "<p>MESSENGER-based crater counts indicate Mercury's youngest volcanic plains are roughly 3.7-3.9 Gyr old. "
                 "Using the surface-to-volume cooling argument from Lecture 04 and Mercury's small size relative to Earth "
                 "and Mars, explain in a short paragraph why an early cessation of volcanism on Mercury is consistent with "
                 "theoretical expectation, and state one specific piece of independent evidence (from Lecture 03 or 05) "
                 "that supports the same conclusion.</p>"),
    )
    solutions = (
        solution(1, 'Estimating the Tunguska Event Energy',
                 f"<p>Mass = (4/3)&pi;(30 m)&sup3;(2000 kg/m&sup3;) = {tunguska_mass:.3e} kg. Energy = &#189;mv&sup2; = "
                 f"&#189;({tunguska_mass:.3e})(15000)&sup2; = {tunguska_energy:.3e} J = {tunguska_mt:.1f} MT. This result "
                 f"({tunguska_mt:.1f} MT) is broadly consistent with, though somewhat below, the commonly cited 3-15 MT "
                 f"range, which reflects genuine uncertainty in the actual impactor size and airburst altitude, not an "
                 f"error in the basic kinetic-energy calculation.</p>",
                 [('Correct mass calculation with unit conversion', 6), ('Correct kinetic energy and MT conversion', 6), ('Correctly and honestly compares to the published range rather than overstating precision', 3)]),
        solution(2, 'Olympus Mons and the Hawaiian Hotspot Track',
                 f"<p>Time = distance/speed = {hawaii_chain_length_km} km / (0.07 km/yr) = {hawaii_age_myr:.1f} Myr &asymp; "
                 f"{hawaii_age_myr:.0f} Myr, comparable in order of magnitude to Olympus Mons's estimated multi-hundred-"
                 f"Myr construction time. On Earth, the Pacific Plate's motion over the fixed Hawaiian hotspot spreads "
                 f"volcanic material into a long chain of progressively older, smaller volcanic islands and seamounts. On "
                 f"Mars, with no plate tectonics (Lecture 05), the lithosphere never moves relative to the underlying "
                 f"mantle hotspot, so all the erupted material from repeated eruptions over a comparably long timescale "
                 f"piles up in a single location, building one enormous volcano instead of a chain of smaller ones.</p>",
                 [('Correct time calculation with unit conversion', 7), ('Correctly explains the plate-tectonics/stationary-lithosphere contrast', 8)]),
        solution(3, 'Crater Density and Venus\u2019s Resurfacing Event',
                 "<p>A surface that had simply never been struck by many impactors, or one that formed at the same time "
                 "as the planet itself (4.5 Gyr ago) with no subsequent resurfacing, would both be expected to show a "
                 "wide range of crater degradation states (heavily degraded ancient craters mixed with sharper younger "
                 "ones accumulated steadily over 4.5 Gyr), because impacts would have been accumulating and being "
                 "progressively degraded by subsequent smaller impacts and weathering throughout that entire span. "
                 "Instead, Venus shows a low but narrow, roughly uniform range of crater degradation and density across "
                 "its whole surface, which is the specific signature expected if nearly the entire surface was reset "
                 "(buried by volcanism or otherwise resurfaced) at approximately the same time, comparatively recently, "
                 "after which a much shorter interval of impact accumulation began anew.</p>",
                 [('Correctly explains why continuous accumulation over 4.5 Gyr would look different', 8), ('Correctly explains why a narrow degradation range specifically implies a discrete resurfacing event', 7)]),
        solution(4, 'Simple versus Complex Crater Transition',
                 "<p>The apparent contradiction is resolved because the simple-to-complex transition diameter depends on "
                 "target material strength as well as gravity, and Mars's surface (a mix of regolith, sedimentary, and "
                 "volcanic rock, in some places ice-rich) does not have uniformly stronger material strength than the "
                 "Moon's regolith/rock in a way that offsets its stronger gravity in the direction assumed here; more "
                 "importantly, the specific transition-diameter values quoted for the Moon versus Mars in the published "
                 "literature reflect a real, measured combination of both the gravity dependence and material-strength "
                 "differences (including, for icy or volatile-rich near-surface material on parts of Mars, weaker "
                 "effective strength than typical dry lunar regolith), so gravity alone is not the only variable and "
                 "should not be used in isolation to predict the transition diameter, which is exactly the caveat this "
                 "problem is testing.</p>",
                 [('Correctly identifies that gravity is not the sole controlling variable', 8), ('Correctly explains the role of target material strength as a compensating factor', 7)]),
        solution(5, 'Mercury\u2019s Crater-Count Volcanic History',
                 "<p>Mercury, the smallest of the terrestrial planets (aside from dwarf planets), has the largest surface-"
                 "to-volume ratio and is therefore expected, by the 1/R cooling-rate scaling from Lecture 04, to cool and "
                 "lose active volcanism earliest among the terrestrial planets, all else equal; Mercury's crater-count-"
                 "derived cessation of volcanism by roughly 3.7-3.9 Gyr ago is directly consistent with this expectation. "
                 "Independent supporting evidence includes Mercury's widespread lobate scarps (Lecture 05), interpreted "
                 "as a record of global contraction as its large core cooled and shrank -- itself a direct geological "
                 "signature of the same rapid interior cooling implied by the crater-count volcanic-cessation age.</p>",
                 [('Correctly applies the surface-to-volume cooling argument to Mercury', 8), ('Correctly cites lobate scarps as independent supporting evidence', 7)]),
    )
    pset_html = pset_page(3, 'Impact Cratering and Comparative Surface Geology',
                           'Apply crater-scaling, chronology, and plate-tectonic-versus-stagnant-lid arguments from Lectures 05-06 to Tunguska, Olympus Mons, Venus, and Mercury.',
                           ''.join(problems), 'OpenStax Astronomy 2e, Sections 9.4-9.6.')
    sol_html = solutions_page(3, 'Impact Cratering and Comparative Surface Geology', ''.join(solutions))
    asmt = assessment_md(3, 'Impact Cratering and Comparative Surface Geology',
                          ['Problem 1: unit conversion to megatons must be shown explicitly.',
                           'Problem 2: both the numeric time estimate and the plate-tectonics explanation are required.',
                           'Problem 3: answer must specifically address why a narrow (not wide) degradation range is the key diagnostic.',
                           'Problem 4: answer must identify material strength as the compensating factor, not merely restate the contradiction.',
                           'Problem 5: both the surface-to-volume argument and the specific independent evidence (lobate scarps) are required.'],
                          ['Reporting kinetic energy without converting to megatons for comparison to the published range (Problem 1).',
                           'Treating the Hawaiian-chain formation time and Olympus Mons\'s construction time as needing to match exactly rather than being compared at order-of-magnitude precision (Problem 2).',
                           'Assuming gravity alone fully determines the simple-to-complex crater transition diameter (Problem 4).'])
    return pset_html, sol_html, asmt


# ---------------------------------------------------------------------------
# LAB 04: Scale height and equilibrium temperature for Titan and comparison
# ---------------------------------------------------------------------------
def make_lab_04() -> str:
    titan_g = surface_gravity(TITAN['mass'], TITAN['radius'])
    titan_h_n2 = scale_height_m(TITAN['teff'], N2_MASS, titan_g)
    titan_teq = equilibrium_temperature_k(L_SUN_W, TITAN['a_au'] * AU_M, TITAN['albedo'])
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab applies the hydrostatic scale-height formula (Lecture 07) and the
radiative-equilibrium-temperature formula (Lecture 08) to Titan, using real Cassini-Huygens-measured parameters, and
compares the results to Earth, Venus, and Mars (recomputed here rather than simply copied from the lecture table).</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Body</th><th>Mass (kg)</th><th>Radius (km)</th><th>Semimajor axis (AU)</th><th>Surface/effective temperature (K)</th><th>Bond albedo</th></tr></thead><tbody>
<tr><td>Titan</td><td>{TITAN['mass']:.4e}</td><td>{TITAN['radius']/1000:.1f}</td><td>{TITAN['a_au']}</td><td>{TITAN['teff']}</td><td>{TITAN['albedo']}</td></tr>
<tr><td>Earth</td><td>{PLANETS['Earth']['mass']:.4e}</td><td>{PLANETS['Earth']['radius']/1000:.1f}</td><td>{PLANETS['Earth']['a_au']}</td><td>{PLANETS['Earth']['teq_obs']}</td><td>{PLANETS['Earth']['albedo']}</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute Titan's surface gravity from its measured mass and radius, using the identical formula from Lecture 01.</li>
<li>Compute Titan's atmospheric scale height, assuming a nitrogen-dominated atmosphere (mean molecular mass &asymp; 28 amu, close to N&#8322;'s 28.014 amu) at its measured &sim;93.7 K surface temperature, using the identical scale-height formula from Lecture 07.</li>
<li>Compare Titan's scale height to Earth's (recompute Earth's using the same formula and Earth's measured temperature and gravity) and explain, referencing the scale-height formula's dependence on T and g, why Titan's scale height is comparable to or even larger than Earth's despite being much colder.</li>
<li>Compute Titan's zero-greenhouse equilibrium temperature using its measured Bond albedo, semimajor axis (same as Saturn's, since Titan orbits Saturn), and the Sun's luminosity, using the identical equilibrium-temperature formula from Lecture 08.</li>
<li>Compute the greenhouse temperature excess for Titan (observed surface temperature minus computed equilibrium temperature) and compare it, as a fraction of the total observed temperature, to Earth's and Venus's greenhouse excess fractions from Lecture 08's table.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Titan's actual atmosphere also contains a few percent methane and trace hydrocarbons, which slightly changes its true mean molecular mass from pure N&#8322;'s 28.014 amu; students should state this simplification explicitly and note that it introduces a small (a few percent) systematic uncertainty in the computed scale height.</p></section>
<section><h2>Deliverables</h2><ul><li>Computed surface gravity and scale height for Titan, with all steps shown.</li><li>A comparison to Earth's independently recomputed scale height.</li><li>Computed equilibrium temperature and greenhouse excess for Titan.</li><li>A comparison of Titan's, Earth's, and Venus's greenhouse-excess fractions.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct surface-gravity and scale-height calculations with correct units.</li><li>Correct qualitative explanation of why Titan's scale height is large despite low temperature (weak gravity compensating).</li><li>Correct equilibrium-temperature and greenhouse-excess calculations.</li><li>Correct, properly labeled comparison of greenhouse-excess fractions across three bodies.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Section 10.1-10.4.</li><li>Titan's mass, radius, and surface temperature: standard published Cassini-Huygens values (Niemann et al. 2005, <em>Nature</em>; Fulchignoni et al. 2005, <em>Nature</em>), not independently re-verified by live fetch this session; see <code>materials/ASTR320/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR320/src/generate_astr320_labs_psets.py</code>.</li></ul></section>
"""
    return lab_page(4, 'Scale Height and Equilibrium Temperature for Titan',
                     'Apply the hydrostatic scale-height and radiative-equilibrium formulas to Titan\u2019s real Cassini-Huygens-measured atmosphere and compare to Earth and Venus.', sections)


# ---------------------------------------------------------------------------
# PS 04: Atmospheric structure, radiative balance, and the greenhouse effect
# ---------------------------------------------------------------------------
def make_pset_04():
    mars_greenhouse = PLANETS['Mars']['teq_obs'] - TEQ_BOND['Mars']
    venus_greenhouse = PLANETS['Venus']['teq_obs'] - TEQ_BOND['Venus']
    earth_greenhouse = PLANETS['Earth']['teq_obs'] - TEQ_BOND['Earth']
    problems = (
        problem(1, 'Why Mercury Has (Essentially) No Scale Height to Compute',
                 "<p>The scale-height formula H = kT/(mg) requires a bound atmosphere in hydrostatic equilibrium. "
                 "Mercury's escape velocity is 4.25 km/s and its dayside surface temperature reaches &sim;700 K. Using the "
                 "Jeans-escape reasoning previewed in Lecture 07 and developed fully in Lecture 09, explain in a short "
                 "paragraph why Mercury cannot sustain a substantial bound atmosphere, making a meaningful scale-height "
                 "calculation for a thick Mercury atmosphere physically inapplicable.</p>"),
        problem(2, "Mars's Small Greenhouse Excess",
                 f"<p>Using the equilibrium-temperature table values from Lecture 08, Mars's greenhouse excess is "
                 f"&Delta;T_gh = {mars_greenhouse:+.0f} K, compared to Venus's {venus_greenhouse:+.0f} K, despite both "
                 f"planets having CO&#8322;-dominated atmospheres. Compute the ratio of Venus's to Mars's surface pressure "
                 f"(92 bar versus 6 mbar) and use it to explain, in a short paragraph, why atmospheric mass/opacity, not "
                 f"merely the presence of CO&#8322;, controls the size of the greenhouse excess.</p>"),
        problem(3, "Earth's Scale Height with a Different Surface Temperature",
                 f"<p>Recompute Earth's atmospheric scale height (using N&#8322; as the dominant species) for a "
                 f"hypothetical mean surface temperature of 250 K (an ice-age-like scenario) instead of the standard 288 "
                 f"K, holding gravity fixed. Compare your result to the standard {EARTH_H_N2/1000:.2f} km value from "
                 f"Lecture 07 and state the percent change.</p>"),
        problem(4, 'Bond Albedo and Cloud Cover',
                 "<p>Venus has the highest Bond albedo (0.76) of any planet, due to its global sulfuric-acid cloud deck, "
                 "while Mercury has the lowest (0.088), due to its dark, airless regolith surface. Using the equilibrium-"
                 "temperature formula, compute what Venus's zero-greenhouse equilibrium temperature would be if its "
                 "albedo were instead equal to Mercury's (0.088), holding its semimajor axis fixed, and explain in one "
                 "sentence why this hypothetical value is higher than Venus's real computed equilibrium temperature.</p>"),
        problem(5, 'The Runaway Greenhouse and D/H Ratio',
                 "<p>Venus's atmospheric deuterium-to-hydrogen ratio is roughly 100-150 times Earth's. Using the "
                 "differential-escape reasoning previewed in Lecture 08 and developed in Lecture 09 (lighter isotopes "
                 "escape preferentially), explain in a short paragraph why this elevated D/H ratio is considered strong "
                 "indirect evidence that Venus once had a much larger water inventory than it has today, rather than "
                 "simply having formed with unusually deuterium-rich water.</p>"),
    )
    solutions = (
        solution(1, 'Why Mercury Has (Essentially) No Scale Height to Compute',
                 "<p>Mercury's low mass and correspondingly low escape velocity (4.25 km/s), combined with its very high "
                 "dayside temperature (&sim;700 K, giving even heavy atmospheric molecules substantial thermal speeds), "
                 "together give even relatively heavy gas species a Jeans escape parameter &lambda; small enough for "
                 "rapid, geologically fast atmospheric loss (the same &lambda; = v_esc&sup2;/v_mp&sup2; reasoning applied "
                 "quantitatively to Earth and Mars in Lecture 09). Any substantial primordial atmosphere Mercury may have "
                 "had would therefore have been lost long ago, leaving only an extremely tenuous, transient exosphere "
                 "(supplied by solar-wind sputtering and micrometeorite vaporization) far too thin to be usefully "
                 "described by a hydrostatic scale-height formula.</p>",
                 [('Correctly connects low escape velocity and high temperature to a small Jeans parameter', 8), ('Correctly concludes the scale-height formula is not meaningfully applicable', 7)]),
        solution(2, "Mars's Small Greenhouse Excess",
                 f"<p>92 bar / 6 mbar = 92000/6 &asymp; 15,300, i.e., Venus's surface pressure (and hence total atmospheric "
                 f"mass and infrared opacity) is roughly four orders of magnitude greater than Mars's, despite both "
                 f"atmospheres being &gt;95% CO&#8322; by composition. This confirms that the greenhouse effect's magnitude "
                 f"depends on total atmospheric mass and column opacity to outgoing infrared radiation, not merely on "
                 f"which gas is present: Mars's atmosphere, though chemically similar to Venus's, is simply too thin to "
                 f"trap much outgoing thermal radiation, giving it only a small greenhouse excess despite its CO&#8322;-"
                 f"dominated composition.</p>",
                 [('Correct pressure-ratio calculation', 6), ('Correctly explains that mass/opacity, not composition alone, controls greenhouse magnitude', 9)]),
        solution(3, "Earth's Scale Height with a Different Surface Temperature",
                 f"<p>H(250 K) = H(288 K) &times; (250/288) = {EARTH_H_N2/1000:.2f} &times; (250/288) = "
                 f"{EARTH_H_N2/1000*(250.0/288.0):.2f} km, a decrease of {(1-250.0/288.0)*100:.1f}% relative to the "
                 f"standard 288 K value, since H &prop; T linearly at fixed g and m.</p>",
                 [('Correctly applies the linear T-scaling of the scale-height formula', 8), ('Correct percent-change calculation', 7)]),
        solution(4, 'Bond Albedo and Cloud Cover',
                 f"<p>T_eq(A=0.088) = [(1-0.088)/(1-0.76)]&#185;&#8260;&#8308; &times; T_eq(A=0.76) = "
                 f"[{(1-0.088)/(1-0.76):.3f}]&#185;&#8260;&#8308; &times; {TEQ_BOND['Venus']:.1f} K = "
                 f"{((1-0.088)/(1-0.76))**0.25 * TEQ_BOND['Venus']:.1f} K. This hypothetical value is higher than Venus's "
                 f"real computed equilibrium temperature because a lower albedo means Venus would absorb a larger "
                 f"fraction of the sunlight it intercepts, requiring a higher equilibrium temperature to radiate that "
                 f"larger absorbed power back to space.</p>",
                 [('Correct proportional recomputation using the (1-A)^(1/4) scaling', 9), ('Correct one-sentence physical explanation', 6)]),
        solution(5, 'The Runaway Greenhouse and D/H Ratio',
                 "<p>Because hydrogen (light) escapes far more readily than deuterium (heavier by roughly a factor of two "
                 "in mass) via Jeans escape, any water vapor that is photodissociated high in Venus's atmosphere loses "
                 "its hydrogen preferentially, progressively enriching the remaining hydrogen inventory in deuterium over "
                 "time. The presently observed, strongly elevated D/H ratio is therefore best explained as the cumulative "
                 "fossil signature of a much larger original water/hydrogen inventory having been lost over billions of "
                 "years, rather than as evidence that Venus's water was unusually deuterium-rich from the start (which "
                 "would require an ad hoc, unexplained difference in Venus's initial volatile delivery relative to "
                 "Earth's, for which there is no independent supporting evidence).</p>",
                 [('Correctly explains the differential-escape mechanism', 8), ('Correctly argues why this is stronger evidence than an alternative "born deuterium-rich" hypothesis', 7)]),
    )
    pset_html = pset_page(4, 'Atmospheric Structure, Radiative Balance, and the Greenhouse Effect',
                           'Apply scale-height scaling, equilibrium-temperature/albedo relationships, and the greenhouse-excess concept from Lectures 07-08 to Mercury, Mars, Venus, and Earth.',
                           ''.join(problems), 'OpenStax Astronomy 2e, Sections 10.1-10.4.')
    sol_html = solutions_page(4, 'Atmospheric Structure, Radiative Balance, and the Greenhouse Effect', ''.join(solutions))
    asmt = assessment_md(4, 'Atmospheric Structure, Radiative Balance, and the Greenhouse Effect',
                          ['Problem 1: must connect escape velocity AND temperature to Jeans escape, not just assert Mercury has no atmosphere.',
                           'Problem 2: must state the pressure-ratio order of magnitude AND correctly conclude mass/opacity (not composition) controls greenhouse magnitude.',
                           'Problem 3: must show the linear T-scaling explicitly, not just state a new H value.',
                           'Problem 4: must use the (1-A)^(1/4) proportional scaling correctly (a common error is treating T_eq as scaling linearly with (1-A)).',
                           'Problem 5: must explain why differential escape is favored over the "born deuterium-rich" alternative, not just describe the escape mechanism alone.'],
                          ['Treating T_eq as proportional to (1-A) rather than (1-A) to the one-fourth power (Problem 4).',
                           'Confusing scale-height\'s linear dependence on temperature with the equilibrium-temperature formula\'s quarter-power dependence on flux (Problems 3 vs. 4).',
                           'Describing Venus\'s and Mars\'s CO2 atmospheres as fundamentally different in composition rather than in total mass/opacity (Problem 2).'])
    return pset_html, sol_html, asmt


# ---------------------------------------------------------------------------
# LAB 05: Jeans escape and magnetopause standoff comparison
# ---------------------------------------------------------------------------
def make_lab_05() -> str:
    jupiter_standoff = magnetopause_distance_m(JUPITER_B0_T, PLANETS['Jupiter']['radius'], SOLAR_WIND_RHO_KGM3, SOLAR_WIND_V_MS)
    earth_standoff = magnetopause_distance_m(3.1e-5, PLANETS['Earth']['radius'], SOLAR_WIND_RHO_KGM3, SOLAR_WIND_V_MS)
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab combines the Jeans-escape formalism (Lecture 09) with the magnetopause
pressure-balance model (Lecture 10), using real measured planetary magnetic-field strengths, to compare Earth's and
Jupiter's magnetospheric standoff distances quantitatively.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Planet</th><th>Equatorial surface field B&#8320; (T)</th><th>Radius (km)</th></tr></thead><tbody>
<tr><td>Earth</td><td>3.1 &times; 10&#8315;&#8309;</td><td>{PLANETS['Earth']['radius']/1000:.1f}</td></tr>
<tr><td>Jupiter</td><td>{JUPITER_B0_T:.2e}</td><td>{PLANETS['Jupiter']['radius']/1000:.1f}</td></tr>
</tbody></table><p>Assume typical solar-wind conditions at 1 AU (&#961;_sw &asymp; {SOLAR_WIND_RHO_KGM3:.1e} kg/m&sup3;, v_sw &asymp; {SOLAR_WIND_V_MS/1000:.0f} km/s) for Earth; for Jupiter, note that the solar wind is roughly 27 times less dense at 5.2 AU than at 1 AU (inverse-square dilution), a correction you must apply.</p></section>
<section><h2>Procedure</h2><ol>
<li>Using the magnetopause pressure-balance formula from Lecture 10, compute Earth's magnetopause standoff distance in Earth radii, using the solar-wind density and speed given above.</li>
<li>Correct the solar-wind density for Jupiter's greater distance (5.2 AU versus 1 AU) using the inverse-square dilution law, then compute Jupiter's magnetopause standoff distance in Jupiter radii.</li>
<li>Compare your computed standoff distances (in units of each planet's own radius) to the observed values (&sim;10 R_E for Earth; &sim;50-100 R_J for Jupiter, which varies substantially with solar-wind pressure) and discuss whether the order of magnitude matches.</li>
<li>Using the Jeans-escape parameter formula from Lecture 09, compute &lambda; for atomic hydrogen at Jupiter's cloud-top temperature (&sim;165 K) using Jupiter's escape velocity (59.5 km/s, from Lecture 01's table), and compare it to Earth's value from Lecture 09's worked example. Explain why Jupiter, despite its much colder cloud tops, retains hydrogen far more effectively than Earth does.</li>
<li>In one paragraph, explain how a much larger magnetopause standoff distance (relative to the planet's own radius) might, in principle, provide additional protection against non-thermal atmospheric escape, and state why this is a plausible but not fully quantified effect (per Lecture 10's discussion).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Solar-wind density and speed both vary substantially with solar activity (by roughly a factor of a few), so the specific standoff-distance values computed here should be understood as representative, not exact, and should be reported with this caveat.</p></section>
<section><h2>Deliverables</h2><ul><li>Computed Earth and Jupiter magnetopause standoff distances, with the solar-wind density correction shown explicitly for Jupiter.</li><li>A comparison to observed standoff distances.</li><li>A computed Jeans parameter for hydrogen at Jupiter, compared to Earth's.</li><li>A written paragraph on magnetic shielding and atmospheric escape.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct pressure-balance calculation for both planets, including the inverse-square solar-wind density correction for Jupiter.</li><li>Correct comparison to observed standoff distances with appropriate uncertainty caveats.</li><li>Correct Jeans-parameter calculation and correct qualitative explanation (large escape velocity, not just cold temperature, is the dominant factor for Jupiter).</li><li>Written paragraph correctly hedges the magnetic-shielding claim as plausible but not fully quantified.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Section 10.3 and Section 11.2.</li><li>Jupiter's and Earth's equatorial magnetic field strengths: standard published values (Connerney et al. 2018, <em>Geophysical Research Letters</em>, for Jupiter's Juno-derived field), not independently re-verified by live fetch this session; see <code>materials/ASTR320/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR320/src/generate_astr320_labs_psets.py</code>.</li></ul></section>
"""
    return lab_page(5, 'Jeans Escape and Magnetopause Standoff: Earth versus Jupiter',
                     'Combine atmospheric-escape and magnetosphere pressure-balance physics to compare Earth\'s and Jupiter\'s protective magnetic environments.', sections)


# ---------------------------------------------------------------------------
# PS 05: Atmospheric escape and planetary magnetic fields
# ---------------------------------------------------------------------------
def make_pset_05():
    mars_lambda_o2 = jeans_parameter(MARS_ESCAPE_V, thermal_speed_most_probable(300.0, 32.0 * AMU))
    earth_lambda_o2 = jeans_parameter(EARTH_ESCAPE_V, thermal_speed_most_probable(1000.0, 32.0 * AMU))
    neptune_standoff_ratio = NEPTUNE_B0_T ** 2 / URANUS_B0_T ** 2
    problems = (
        problem(1, 'Jeans Escape of Molecular Oxygen: Earth versus Mars',
                 "<p>Compute the Jeans escape parameter &lambda; for molecular oxygen (m = 32 amu) at Earth (assume "
                 "exospheric T = 1000 K) and at Mars (assume exospheric T = 300 K, since Mars's thinner atmosphere and "
                 "weaker greenhouse give it a cooler exosphere than Earth's). Compare both values to the hydrogen values "
                 "computed in Lecture 09 (Earth &lambda;_H2, Mars &lambda;_H2) and state which species (H&#8322; or "
                 "O&#8322;) is retained more effectively on each planet, and why.</p>"),
        problem(2, "Mars's Ion Pickup Loss and MAVEN",
                 "<p>NASA's MAVEN mission has directly measured Mars's present-day ion-pickup atmospheric loss rate. "
                 "Explain, in a short paragraph referencing Lecture 09 and Lecture 10, why this present-day measured loss "
                 "rate, even if precisely known, cannot alone establish how much atmosphere Mars has lost over its entire "
                 "4.5 Gyr history, and what additional information or assumption would be required to make that "
                 "extrapolation.</p>"),
        problem(3, 'Comparing Uranus\u2019s and Neptune\u2019s Magnetic Fields',
                 f"<p>Uranus's equatorial surface field is roughly {URANUS_B0_T:.2e} T and Neptune's is roughly "
                 f"{NEPTUNE_B0_T:.2e} T. Compute the ratio of their magnetic pressures (B&sup2;) and state what this "
                 f"implies about their relative magnetopause standoff distances (in planetary radii), holding solar-wind "
                 f"conditions and planetary radius ratio approximately fixed for this estimate.</p>"),
        problem(4, "Venus's Induced Magnetosphere",
                 "<p>Venus has no measurable intrinsic magnetic field, yet it does have a weak, induced magnetosphere "
                 "formed by the interaction between the solar wind and Venus's ionosphere. Explain, in a short paragraph, "
                 "why this induced magnetosphere is expected to provide much less protection against atmospheric erosion "
                 "than Earth's intrinsic, dynamo-generated magnetosphere, referencing the dynamo requirements from "
                 "Lecture 10.</p>"),
        problem(5, 'Escape Velocity and the Retention of Helium',
                 "<p>Helium (m = 4 amu) is lighter than most atmospheric gases but heavier than atomic hydrogen. Using "
                 "Earth's escape velocity (11.2 km/s) and an assumed exospheric temperature of 1000 K, compute the Jeans "
                 "escape parameter for helium and compare it to the hydrogen value from Lecture 09. State whether Earth's "
                 "atmosphere should retain helium more or less effectively than hydrogen, and explain why Earth's "
                 "atmosphere nonetheless contains only trace helium today (a fact not fully explained by Jeans escape "
                 "alone).</p>"),
    )
    solutions = (
        solution(1, 'Jeans Escape of Molecular Oxygen: Earth versus Mars',
                 f"<p>O&#8322; thermal speed at 1000 K: v_mp = &radic;(2kT/m) = &radic;(2 &times; 1.381e-23 &times; 1000 / "
                 f"({32*AMU:.3e})) &asymp; 721 m/s; at Earth, &lambda;_O2 = (11200/721)&sup2; &asymp; "
                 f"{earth_lambda_o2:.0f}. At Mars (T=300 K), v_mp &asymp; 395 m/s; &lambda;_O2 = (5030/395)&sup2; &asymp; "
                 f"{mars_lambda_o2:.0f}. Both &lambda;_O2 values are far larger than the corresponding &lambda;_H2 values "
                 f"from Lecture 09 (&sim;15 for Earth, &sim;3 for Mars), confirming that molecular oxygen is retained far "
                 f"more effectively than hydrogen on both planets, because oxygen's much larger mass gives it both a "
                 f"lower thermal speed and (through &lambda; &prop; m) a much larger Jeans parameter at the same "
                 f"temperature and escape velocity.</p>",
                 [('Correct thermal-speed and Jeans-parameter calculations for both planets', 9), ('Correct comparison to Lecture 09\'s hydrogen values with correct physical explanation', 6)]),
        solution(2, "Mars's Ion Pickup Loss and MAVEN",
                 "<p>A present-day measured loss rate gives only a snapshot of current conditions; extrapolating it "
                 "across 4.5 Gyr would implicitly assume the loss rate has been constant throughout Mars's history, which "
                 "is almost certainly false, since both the solar wind's intensity (much stronger from the young, more "
                 "active Sun) and Mars's own atmosphere (likely much thicker early on) have changed dramatically over "
                 "time. Making a reliable historical extrapolation would require independent modeling of the young Sun's "
                 "solar-wind and XUV output (informed by observations of young solar-type stars) combined with a model "
                 "of how Mars's atmospheric thickness itself evolved over time, not simply multiplying today's measured "
                 "rate by 4.5 Gyr.</p>",
                 [('Correctly identifies that a present-day rate cannot simply be extrapolated linearly', 8), ('Correctly identifies what additional modeling would be required', 7)]),
        solution(3, 'Comparing Uranus\u2019s and Neptune\u2019s Magnetic Fields',
                 f"<p>Ratio of magnetic pressures (B&sup2;) = ({NEPTUNE_B0_T:.2e})&sup2; / ({URANUS_B0_T:.2e})&sup2; = "
                 f"{neptune_standoff_ratio:.2f}. Since magnetopause standoff distance scales as B&sup2;/6 (the sixth root "
                 f"of B&sup2;, from the dipole field's r&#8315;&sup3; falloff and the pressure balance derived in Lecture "
                 f"10), a magnetic-pressure ratio of {neptune_standoff_ratio:.2f} implies Neptune's standoff distance "
                 f"(in its own planetary radii) should be only modestly larger than Uranus's (roughly "
                 f"{neptune_standoff_ratio**(1/6):.2f} times as large), since the sixth-root dependence strongly "
                 f"compresses even a substantial pressure-ratio difference into a much smaller distance-ratio "
                 f"difference.</p>",
                 [('Correct magnetic-pressure ratio calculation', 7), ('Correctly applies the sixth-root scaling to standoff distance rather than a linear or squared scaling', 8)]),
        solution(4, "Venus's Induced Magnetosphere",
                 "<p>Lecture 10 established that a self-sustaining dynamo requires a convecting, electrically "
                 "conducting fluid organized by planetary rotation into helical flow; Venus's induced magnetosphere, by "
                 "contrast, arises passively from the solar wind interacting with Venus's ionosphere and does not require "
                 "any internal dynamo process at all. An induced field is generally much weaker and more variable than an "
                 "intrinsic dipole field, and it does not extend nearly as far from the planet, meaning it stands off the "
                 "solar wind much closer to Venus's ionosphere/atmosphere than Earth's intrinsic magnetosphere does "
                 "relative to Earth's atmosphere, providing correspondingly less protective standoff distance against "
                 "direct atmospheric erosion.</p>",
                 [('Correctly distinguishes induced from intrinsic (dynamo-generated) fields', 8), ('Correctly explains why an induced field provides less standoff protection', 7)]),
        solution(5, 'Escape Velocity and the Retention of Helium',
                 f"<p>Helium thermal speed at 1000 K: v_mp = &radic;(2 &times; 1.381e-23 &times; 1000 / (4 &times; "
                 f"1.66054e-27)) &asymp; 2029 m/s. &lambda;_He = (11200/2029)&sup2; &asymp; 30.4, about twice the hydrogen "
                 f"value (&sim;15) from Lecture 09, since helium is roughly twice as massive as H&#8322;. Earth should "
                 f"retain helium somewhat more effectively than hydrogen via Jeans escape alone. However, Earth's "
                 f"atmosphere contains only trace helium today primarily because Earth's helium is continuously but only "
                 f"slowly replenished by radioactive decay (alpha decay of uranium and thorium, Lecture 04) and, unlike "
                 f"nitrogen or oxygen, has no significant chemical sink that would otherwise retain it at the surface; "
                 f"the modest but non-negligible Jeans and non-thermal escape over geological time is therefore "
                 f"sufficient to keep helium's atmospheric abundance low despite its relatively large &lambda;, since its "
                 f"supply rate is also very low.</p>",
                 [('Correct thermal-speed and Jeans-parameter calculation for helium', 8), ('Correctly explains the low supply-rate resolution rather than treating Jeans escape as the full explanation', 7)]),
    )
    pset_html = pset_page(5, 'Atmospheric Escape and Planetary Magnetic Fields',
                           'Apply Jeans escape and magnetopause pressure-balance reasoning from Lectures 09-10 to oxygen and helium retention, ion pickup, and the ice giants\u2019 magnetic fields.',
                           ''.join(problems), 'OpenStax Astronomy 2e, Sections 10.3 and 10.5.')
    sol_html = solutions_page(5, 'Atmospheric Escape and Planetary Magnetic Fields', ''.join(solutions))
    asmt = assessment_md(5, 'Atmospheric Escape and Planetary Magnetic Fields',
                          ['Problem 1: both planets\' Jeans parameters must be computed and correctly compared to Lecture 09\'s hydrogen values.',
                           'Problem 2: must identify BOTH that solar activity and Mars\'s own atmospheric thickness likely changed over time, not just one factor.',
                           'Problem 3: must apply the sixth-root scaling, not a linear or squared scaling, to the standoff-distance ratio.',
                           'Problem 4: must explicitly distinguish induced from intrinsic fields using the dynamo-requirement language from Lecture 10.',
                           'Problem 5: must correctly resolve the apparent tension between helium\'s relatively large lambda and its low observed abundance via the low-supply-rate argument.'],
                          ['Applying a linear or squared (rather than sixth-root) scaling to the magnetopause standoff-distance ratio (Problem 3).',
                           'Treating a present-day measured escape rate as directly applicable to the entire planetary history without qualification (Problem 2).',
                           'Concluding from a large Jeans parameter alone that a species must be abundant in the atmosphere, without considering its supply rate (Problem 5).'])
    return pset_html, sol_html, asmt


# ---------------------------------------------------------------------------
# LAB 06: Giant planet density comparison and the Roche limit for Uranus's rings
# ---------------------------------------------------------------------------
def make_lab_06() -> str:
    uranus_roche_fluid = roche_limit_fluid_m(PLANETS['Uranus']['radius'], URANUS_DENSITY, ICE_DENSITY_KGM3)
    epsilon_ring_m = 51149e3  # Uranus epsilon ring radius, standard published value
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab extends Lecture 11's giant-planet density comparison and Lecture 12's
Roche-limit derivation to Uranus, using real Voyager 2 and stellar-occultation-derived ring data.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Uranus mass</td><td>{PLANETS['Uranus']['mass']:.4e} kg</td></tr>
<tr><td>Uranus radius</td><td>{PLANETS['Uranus']['radius']/1000:.0f} km</td></tr>
<tr><td>Uranus mean density (to be computed)</td><td>&mdash;</td></tr>
<tr><td>Uranus's outermost major ring (epsilon ring) radius</td><td>{epsilon_ring_m/1000:.0f} km</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute Uranus's mean density from its mass and radius, and compare it to Jupiter's and Saturn's densities from Lecture 11.</li>
<li>Compute the fluid-body Roche limit for ice-density ring particles around Uranus, using the identical formula from Lecture 12.</li>
<li>Compare your computed Roche limit to the epsilon ring's real orbital radius (expressed in Uranus radii), and state whether the epsilon ring lies inside or outside your computed Roche limit.</li>
<li>Uranus's rings are known to be composed of unusually dark material, with lower albedo than Saturn's icy rings, suggesting a different (or processed) composition rather than pure water ice. Explain in one paragraph how this composition difference could affect the accuracy of your Roche-limit estimate from step 2, which assumed pure ice density.</li>
<li>Using the giant-planet interior concepts from Lecture 11, explain briefly why Uranus, despite being much less massive than Jupiter, still generates its own magnetic field (previewed in Lecture 10), even though its interior lacks a metallic-hydrogen layer.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The exact density of Uranus's ring particles is not independently well constrained; using pure ice density is a simplifying assumption whose effect on the computed Roche limit should be explicitly stated as a limitation, not hidden, following this course's standard for honestly characterizing approximations.</p></section>
<section><h2>Deliverables</h2><ul><li>Computed Uranus mean density, compared to Jupiter and Saturn.</li><li>Computed fluid Roche limit for Uranus.</li><li>A comparison to the real epsilon ring radius, correctly stating whether it lies inside or outside the Roche limit.</li><li>Written paragraphs on ring-composition uncertainty and Uranus's magnetic field.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct density calculation and comparison.</li><li>Correct Roche-limit calculation using the fluid-body formula.</li><li>Correct, properly qualified comparison to the real ring radius.</li><li>Correctly explains that Uranus's dynamo operates in an ionic water/ammonia mantle rather than metallic hydrogen.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Section 11.4.</li><li>Uranus's ring radii: standard published Voyager 2/stellar-occultation values (Elliot et al. 1977; Voyager Imaging Team 1986), not independently re-verified by live fetch this session; see <code>materials/ASTR320/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR320/src/generate_astr320_labs_psets.py</code>.</li></ul></section>
"""
    return lab_page(6, "Giant Planet Density and the Roche Limit at Uranus",
                     "Extend the Roche-limit and density-comparison tools from Lectures 11-12 to Uranus's real, dark, narrow ring system.", sections)


# ---------------------------------------------------------------------------
# PS 06: Giant planets, rings, and satellites
# ---------------------------------------------------------------------------
def make_pset_06():
    phobos_roche = roche_limit_fluid_m(PLANETS['Mars']['radius'], PLANETS['Mars']['mass']/(4/3*math.pi*PLANETS['Mars']['radius']**3), PHOBOS['mass']/(4/3*math.pi*PHOBOS['radius']**3))
    phobos_a = PHOBOS['a_m']
    saturn_jupiter_density_ratio = SATURN_MEAN_DENSITY_KGM3 / DENSITIES['Jupiter']
    problems = (
        problem(1, "Phobos and Mars's Roche Limit",
                 f"<p>Phobos (mass {PHOBOS['mass']:.4e} kg, radius {PHOBOS['radius']/1000:.2f} km) orbits Mars at "
                 f"{PHOBOS['a_m']/1000:.0f} km, well outside Mars's Roche limit today, but is known to be spiraling "
                 f"slowly inward due to tidal dissipation inside Mars. Compute Phobos's own density from its mass and "
                 f"radius, then compute the fluid Roche limit for a body of that density orbiting Mars (mean density "
                 f"computed from Mars's mass and radius). Compare Phobos's current orbital radius to this Roche limit "
                 f"and state, in one sentence, what this comparison implies about Phobos's long-term fate.</p>"),
        problem(2, 'Saturn versus Jupiter: Why Does Density Differ Despite Similar Composition?',
                 f"<p>Saturn's and Jupiter's mean densities differ substantially (ratio "
                 f"{saturn_jupiter_density_ratio:.3f}) despite both planets sharing a similar bulk hydrogen/helium-"
                 f"dominated composition. Using the self-compression argument introduced for terrestrial planets in "
                 f"Lecture 03 and revisited for giant planets in Lecture 11, explain in a short paragraph why Jupiter's "
                 f"much stronger self-gravity is sufficient to explain this density difference without requiring the two "
                 f"planets to have fundamentally different compositions.</p>"),
        problem(3, "Neptune's Ring Arcs",
                 "<p>Neptune's rings include unusual partial arcs of clumped material rather than a uniformly distributed "
                 "ring, maintained by resonant confinement with the nearby moon Galatea. Using the shepherd-moon concept "
                 "from Lecture 12 (developed there for Saturn's F ring), explain in a short paragraph how a single nearby "
                 "moon's resonant gravitational influence could concentrate ring material into discrete arcs rather than "
                 "spreading it uniformly around the full ring circumference.</p>"),
        problem(4, "Jupiter's Zonal Wind Depth and Gravity Harmonics",
                 "<p>Juno's gravity-field measurements indicate Jupiter's zonal winds persist to a depth of roughly 3000 "
                 "km below the visible cloud tops before being damped out. Using the concept of increasing electrical "
                 "conductivity with depth (Lecture 11), explain in a short paragraph why the winds should be expected to "
                 "damp out at increasing depth, rather than persisting all the way to Jupiter's center.</p>"),
        problem(5, 'Why Ice Giants Are Not Simply Small Gas Giants',
                 "<p>Explain, in a short paragraph referencing both Lecture 02's core-accretion timing argument and "
                 "Lecture 11's compositional data (&sim;90%+ hydrogen/helium for Jupiter/Saturn versus &sim;10-20% for "
                 "Uranus/Neptune), why classifying Uranus and Neptune as 'ice giants' rather than merely 'smaller gas "
                 "giants' reflects a genuine compositional and formation-history distinction, not just an arbitrary size "
                 "cutoff.</p>"),
    )
    solutions = (
        solution(1, "Phobos and Mars's Roche Limit",
                 f"<p>Phobos's density: &rho; = {PHOBOS['mass']:.4e} / [(4/3)&pi;({PHOBOS['radius']:.3e})&sup3;] &asymp; "
                 f"1876 kg/m&sup3;. Mars's mean density (from Lecture 01's table) is {DENSITIES['Mars']:.0f} kg/m&sup3;. "
                 f"Fluid Roche limit: d = 2.44 R_Mars (&rho;_Mars/&rho;_Phobos)&#185;&#8260;&sup3; = "
                 f"{phobos_roche/1000:.0f} km. Phobos's current orbital radius ({phobos_a/1000:.0f} km) is larger than "
                 f"this computed Roche limit but is decreasing over time due to tidal dissipation inside Mars, implying "
                 f"that Phobos will eventually cross inside the Roche limit and be tidally disrupted, likely within the "
                 f"next tens of millions of years.</p>",
                 [('Correct Phobos density and Mars mean density calculations', 6), ('Correct fluid Roche-limit calculation', 6), ('Correct qualitative conclusion about Phobos\'s eventual fate', 3)]),
        solution(2, 'Saturn versus Jupiter: Why Does Density Differ Despite Similar Composition?',
                 "<p>Jupiter's substantially larger mass produces much stronger self-gravity throughout its interior, "
                 "compressing its hydrogen/helium envelope (and any core material) to higher density at any given "
                 "pressure level than Saturn's weaker self-gravity can achieve, exactly as Lecture 03 showed that Earth's "
                 "stronger self-compression (relative to Mercury) raises its bulk density above what its material "
                 "composition alone would suggest. This self-compression effect, not any difference in bulk hydrogen/"
                 "helium/heavy-element composition, is sufficient on its own to explain why Jupiter is denser than "
                 "Saturn despite both planets sharing a broadly similar protosolar-like composition.</p>",
                 [('Correctly identifies self-compression, not composition difference, as the explanation', 9), ('Correctly connects this to the analogous terrestrial-planet argument from Lecture 03', 6)]),
        solution(3, "Neptune's Ring Arcs",
                 "<p>A shepherd moon in resonance with a ring can exert a gravitational torque that varies periodically "
                 "as the moon and a given ring particle repeatedly return to the same relative orbital geometry; this "
                 "resonant torque can trap ring material at specific longitudes relative to the moon's orbit (librating "
                 "around stable resonance points) rather than allowing it to spread freely around the entire ring "
                 "circumference, producing discrete, confined arcs of enhanced ring-particle density at those resonance "
                 "points instead of a smooth, uniform ring.</p>",
                 [('Correctly explains resonant trapping/libration as the confinement mechanism', 15)]),
        solution(4, "Jupiter's Zonal Wind Depth and Gravity Harmonics",
                 "<p>As depth increases inside Jupiter, pressure and temperature both rise, and hydrogen's electrical "
                 "conductivity increases correspondingly (eventually reaching the fully metallic state described in "
                 "Lecture 11). Once the surrounding fluid becomes sufficiently electrically conductive, magnetic forces "
                 "(generated by Jupiter's own dynamo-produced field) become strong enough to resist and damp out organized "
                 "large-scale zonal flow, effectively braking the winds at the depth where conductivity becomes "
                 "significant -- roughly the depth Juno's gravity data indicate, &sim;3000 km.</p>",
                 [('Correctly connects increasing conductivity with depth to magnetic braking of the winds', 15)]),
        solution(5, 'Why Ice Giants Are Not Simply Small Gas Giants',
                 "<p>The gas-giant/ice-giant distinction is not simply a matter of Uranus and Neptune being smaller "
                 "versions of Jupiter and Saturn; if Uranus and Neptune had captured hydrogen/helium gas as efficiently "
                 "as Jupiter and Saturn did, they would be expected to show a similarly dominant (&sim;90%+) hydrogen/"
                 "helium mass fraction regardless of their smaller total mass. Instead, their measured &sim;10-20% "
                 "hydrogen/helium fraction reflects a genuine difference in formation history: their cores are thought to "
                 "have formed more slowly (in a lower-density, more slowly orbiting part of the disk, per Lecture 02's "
                 "core-accretion argument) and so captured comparatively little nebular gas before the gas disk "
                 "dispersed, leaving them dominated by ices and rock rather than hydrogen/helium -- a compositional "
                 "outcome, not merely a size difference.</p>",
                 [('Correctly explains why size alone would not predict the observed composition difference', 8), ('Correctly connects the composition difference to core-accretion formation timing', 7)]),
    )
    pset_html = pset_page(6, 'Giant Planets, Rings, and Satellites',
                           'Apply the Roche limit, self-compression, and core-accretion timing arguments from Lectures 02, 03, 11, and 12 to Phobos, Saturn/Jupiter, and Neptune\u2019s ring arcs.',
                           ''.join(problems), 'OpenStax Astronomy 2e, Sections 11.1-11.4.')
    sol_html = solutions_page(6, 'Giant Planets, Rings, and Satellites', ''.join(solutions))
    asmt = assessment_md(6, 'Giant Planets, Rings, and Satellites',
                          ['Problem 1: both the Phobos density and Mars Roche-limit calculations are required, plus a correctly reasoned conclusion about Phobos\'s fate.',
                           'Problem 2: must correctly attribute the density difference to self-compression, not to a claimed composition difference.',
                           'Problem 3: must specifically invoke resonant trapping/libration, not a vague "gravity holds it there" explanation.',
                           'Problem 4: must connect conductivity increase with depth to magnetic braking specifically.',
                           'Problem 5: must explain why size alone is an insufficient explanation before giving the core-accretion-timing resolution.'],
                          ['Attributing Jupiter/Saturn density differences to composition differences rather than self-compression (Problem 2).',
                           'Using the rigid-body rather than fluid-body Roche-limit formula without justification (Problem 1), inconsistent with Lecture 12\'s stated preference for the fluid formula for rubble-pile bodies like Phobos.',
                           'Vague, non-mechanistic explanations for ring-arc confinement that do not reference resonance (Problem 3).'])
    return pset_html, sol_html, asmt


# ---------------------------------------------------------------------------
# LAB 07: Capstone -- tidal heating and habitability synthesis for TRAPPIST-1
# ---------------------------------------------------------------------------
def make_lab_07() -> str:
    # Illustrative tidal-heating estimate for TRAPPIST-1e assuming an Io-like
    # forced eccentricity, to synthesize Lecture 13's tidal framework with the
    # Lecture 14 TRAPPIST-1 dataset. Uses the same tidal_acceleration function.
    trappist1e_a_m = TRAPPIST1_PLANETS['e']['a_au'] * AU_M
    # Approximate TRAPPIST-1e as Earth-sized/massed for this order-of-magnitude estimate (stated explicitly as an approximation).
    trappist1e_tidal_a = tidal_acceleration(TRAPPIST1_STAR['mass_msun'] * M_SUN_KG, PLANETS['Earth']['radius'], trappist1e_a_m)
    trappist1e_tidal_frac = trappist1e_tidal_a / EARTH_SURFACE_G * 100
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This capstone lab combines the tidal-acceleration framework from Lecture 13
with the real, live-verified TRAPPIST-1 system data introduced in Lecture 14, synthesizing the semester's tidal and
radiative-balance tools on a single exoplanet system.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>TRAPPIST-1 stellar mass</td><td>{TRAPPIST1_STAR['mass_msun']} M&#8857;</td></tr>
<tr><td>TRAPPIST-1e semimajor axis</td><td>{TRAPPIST1_PLANETS['e']['a_au']} AU</td></tr>
<tr><td>TRAPPIST-1e orbital period</td><td>{TRAPPIST1_PLANETS['e']['period_d']} days</td></tr>
<tr><td>Io tidal acceleration fraction (Lecture 13, for comparison)</td><td>{IO_TIDAL_FRAC:.2f}% of Io's own surface gravity</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Using the tidal-acceleration formula from Lecture 13, and approximating TRAPPIST-1e as Earth-sized and Earth-massed (a stated simplification, since TRAPPIST-1e's exact mass carries larger uncertainty than its radius), compute the tidal acceleration TRAPPIST-1e would experience from its host star, and express it as a fraction of Earth's own surface gravity (never as a multiple).</li>
<li>Compare this fraction to Io's tidal-acceleration fraction from Lecture 13 (recomputed there as {IO_TIDAL_FRAC:.2f}% of Io's own gravity) and state which body experiences the larger relative tidal stress.</li>
<li>Because TRAPPIST-1e's orbital eccentricity is measured to be very low (consistent with strong tidal circularization, though some residual forced eccentricity from the system's resonant chain is expected), explain in one paragraph why a small tidal acceleration combined with even a small non-zero eccentricity could still produce meaningful sustained tidal heating, referencing Lecture 13's resonance-sustained-eccentricity argument.</li>
<li>Recompute TRAPPIST-1e's zero-albedo equilibrium temperature (identical formula to Lecture 14's worked example) and compare it to Earth's zero-albedo equilibrium temperature computed in Lecture 08.</li>
<li>Synthesize your results in a short written summary (150-250 words) addressing whether TRAPPIST-1e is a plausible candidate for a temperate, geologically active world, explicitly citing which of this semester's tools (equilibrium temperature, tidal heating, atmospheric escape, magnetic shielding) most strongly support or undercut that conclusion, and stating clearly which parts of your answer are well-constrained versus speculative.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Approximating TRAPPIST-1e as Earth-sized/massed for the tidal-acceleration calculation is a genuine simplification (its true mass is less precisely measured than its radius); students must state this explicitly rather than presenting the resulting tidal-heating estimate as equally well-constrained as the equilibrium-temperature calculation, which uses only directly measured quantities (semimajor axis and stellar luminosity).</p></section>
<section><h2>Deliverables</h2><ul><li>Computed tidal-acceleration fraction for TRAPPIST-1e, correctly labeled as a fraction of Earth's own gravity.</li><li>A comparison to Io's tidal fraction with a correctly stated conclusion about relative tidal stress.</li><li>A written paragraph on resonance-sustained eccentricity and its implications for TRAPPIST-1e.</li><li>Recomputed equilibrium temperature for TRAPPIST-1e compared to Earth's.</li><li>A synthesis paragraph explicitly distinguishing well-constrained from speculative conclusions.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct tidal-acceleration calculation, correctly expressed as a fraction (not a multiple) of surface gravity.</li><li>Correct, properly directioned comparison to Io.</li><li>Correct equilibrium-temperature recomputation.</li><li>Synthesis paragraph explicitly and correctly separates well-constrained results from speculative extrapolations, per this course's standard of honest uncertainty characterization.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 13.</li><li>TRAPPIST-1 system parameters: live-verified this session via direct web fetch (Wikipedia "TRAPPIST-1," citing Agol et al. 2021, <em>PSJ</em> 2, 1); see <code>materials/ASTR320/reference-log.md</code>.</li><li>Generated by <code>materials/ASTR320/src/generate_astr320_labs_psets.py</code>.</li></ul></section>
"""
    return lab_page(7, 'Capstone: Tidal Heating and Habitability Synthesis for TRAPPIST-1e',
                     "Synthesize this semester's tidal, radiative, and escape tools on a single real exoplanet, TRAPPIST-1e, while explicitly separating well-constrained from speculative conclusions.", sections)


# ---------------------------------------------------------------------------
# PS 07: Capstone problem set -- exoplanet comparative planetology
# ---------------------------------------------------------------------------
def make_pset_07():
    trappist1b_teq = TRAPPIST1_TEQ['b']
    trappist1h_teq = TRAPPIST1_TEQ['h']
    kepler186f_teq = equilibrium_temperature_k(KEPLER186F['star_lum_lsun'] * L_SUN_W, KEPLER186F['a_au'] * AU_M, 0.0)
    problems = (
        problem(1, 'Kepler-186f: A Second Real Exoplanet Comparison',
                 f"<p>Kepler-186f orbits a red dwarf star with luminosity {KEPLER186F['star_lum_lsun']} L&#8857; at a "
                 f"semimajor axis of {KEPLER186F['a_au']} AU (orbital period {KEPLER186F['period_d']} days), and has a "
                 f"measured radius of {KEPLER186F['radius_rearth']} Earth radii. Using the identical equilibrium-"
                 f"temperature formula from Lecture 08/14, compute Kepler-186f's zero-albedo equilibrium temperature and "
                 f"compare it to TRAPPIST-1e's ({TRAPPIST1_TEQ['e']:.1f} K, from Lecture 14) and Earth's "
                 f"({EARTH_TEQ_ZERO_ALBEDO:.1f} K, from Lecture 08).</p>", points=20),
        problem(2, 'TRAPPIST-1b and 1h: The Hottest and Coldest Planets in the System',
                 f"<p>Using the equilibrium-temperature table from Lecture 14, TRAPPIST-1b's zero-albedo equilibrium "
                 f"temperature is {trappist1b_teq:.1f} K and TRAPPIST-1h's is {trappist1h_teq:.1f} K. Compute the ratio "
                 f"T_eq(b)/T_eq(h) and compare it to the ratio of their semimajor axes (a_h/a_b), verifying that the "
                 f"ratio of equilibrium temperatures follows the expected inverse-square-root scaling with orbital "
                 f"distance (T_eq &prop; a&#8315;&#185;&#8260;&sup2;).</p>", points=20),
        problem(3, 'Tidal Locking Timescale Reasoning',
                 "<p>Tidal-locking timescales decrease steeply with decreasing orbital distance and increasing host-star "
                 "mass (roughly as a&#8310; for fixed stellar/planetary parameters, from standard tidal-despinning theory, "
                 "not derived in this course but stated here for use). Given that all seven TRAPPIST-1 planets orbit "
                 "within 0.062 AU (compared to Mercury's 0.39 AU orbit around the much more massive Sun), explain in a "
                 "short paragraph why essentially all TRAPPIST-1 planets are expected to be tidally locked today, even "
                 "though Mercury itself is not (Mercury is in a 3:2 spin-orbit resonance rather than a strict 1:1 "
                 "lock).</p>", points=15),
        problem(4, 'Detection-Method Bias in the Exoplanet Census',
                 "<p>Explain, in a short paragraph, why the radial-velocity method's greater sensitivity to massive, "
                 "close-in planets caused early exoplanet surveys to discover a disproportionate number of 'hot "
                 "Jupiters,' and why this early sample is not representative of the exoplanet population as a whole, "
                 "referencing Lecture 14's discussion of detection bias.</p>", points=15),
        problem(5, 'Capstone Synthesis: Our Solar System in Context',
                 "<p>In 200-300 words, synthesize this course's comparative-planetology themes (formation, interior "
                 "structure, atmospheres, magnetism, tides) to address the open question posed in Lecture 01: how "
                 "representative is our solar system's architecture of planetary systems generally? Your answer must "
                 "cite at least three specific pieces of evidence developed across the semester (e.g., the frost-line "
                 "argument, the exoplanet mass-radius degeneracy, TRAPPIST-1's compact resonant architecture) and must "
                 "distinguish which parts of your answer are well-supported by current data versus still genuinely "
                 "open questions in the research literature.</p>", points=30),
    )
    solutions = (
        solution(1, 'Kepler-186f: A Second Real Exoplanet Comparison',
                 f"<p>T_eq = [L/(16&pi;&sigma;a&sup2;)]&#185;&#8260;&#8308; = [({KEPLER186F['star_lum_lsun']*L_SUN_W:.3e}) / "
                 f"(16&pi;&times;5.670374e-8&times;({KEPLER186F['a_au']*AU_M:.3e})&sup2;)]&#185;&#8260;&#8308; = "
                 f"{kepler186f_teq:.1f} K. This is comparable to TRAPPIST-1e's {TRAPPIST1_TEQ['e']:.1f} K and to Earth's "
                 f"{EARTH_TEQ_ZERO_ALBEDO:.1f} K, placing Kepler-186f, like TRAPPIST-1e, within the temperature range "
                 f"commonly associated with the habitable zone, though (as with TRAPPIST-1e) this equilibrium-temperature "
                 f"calculation alone cannot confirm habitability without atmospheric and albedo information.</p>",
                 [('Correct equilibrium-temperature calculation with correct unit conversions', 12), ('Correct, appropriately hedged comparison to TRAPPIST-1e and Earth', 8)]),
        solution(2, 'TRAPPIST-1b and 1h: The Hottest and Coldest Planets in the System',
                 f"<p>T_eq(b)/T_eq(h) = {trappist1b_teq:.1f}/{trappist1h_teq:.1f} = {trappist1b_teq/trappist1h_teq:.3f}. "
                 f"&radic;(a_h/a_b) = &radic;({TRAPPIST1_PLANETS['h']['a_au']}/{TRAPPIST1_PLANETS['b']['a_au']}) = "
                 f"{math.sqrt(TRAPPIST1_PLANETS['h']['a_au']/TRAPPIST1_PLANETS['b']['a_au']):.3f}. These two ratios agree "
                 f"closely (both &asymp; {trappist1b_teq/trappist1h_teq:.2f}), confirming the expected T_eq &prop; "
                 f"a&#8315;&#185;&#8260;&sup2; scaling directly from real TRAPPIST-1 data.</p>",
                 [('Correct temperature-ratio calculation', 8), ('Correct semimajor-axis-ratio square-root calculation and correct verification of the scaling law', 12)]),
        solution(3, 'Tidal Locking Timescale Reasoning',
                 "<p>Because tidal-despinning timescale falls off steeply with decreasing orbital distance (roughly as "
                 "a&#8310;), even a modest decrease in orbital distance produces an enormous decrease in locking "
                 "timescale. All seven TRAPPIST-1 planets orbit at less than one-sixth of Mercury's orbital distance "
                 "from the Sun, and TRAPPIST-1 itself, though much less massive than the Sun, is old (&sim;7.6 Gyr), "
                 "giving even a slower-acting tidal torque ample time to act; the combination of extremely small orbital "
                 "distance (steeply reducing the timescale) and a old system age is expected to be more than sufficient "
                 "to have tidally locked essentially every TRAPPIST-1 planet, whereas Mercury's larger orbital distance "
                 "from a more massive star left it in a more weakly torqued regime where it settled into a 3:2 rather "
                 "than a strict 1:1 resonance.</p>",
                 [('Correctly invokes the steep (a^6-type) distance scaling of tidal locking timescale', 8), ('Correctly contrasts with Mercury\'s different regime rather than treating all close orbits identically', 7)]),
        solution(4, 'Detection-Method Bias in the Exoplanet Census',
                 "<p>Radial-velocity amplitude scales with planet mass and inversely with orbital distance and stellar "
                 "mass, so the method most easily detects massive planets orbiting very close to their star (the 'hot "
                 "Jupiter' population); lower-mass planets, or planets on wider orbits, produce a smaller reflex "
                 "stellar wobble that is harder to distinguish from instrumental and stellar-activity noise. Because "
                 "early radial-velocity surveys were the dominant discovery method before large-scale transit surveys "
                 "(e.g., Kepler, TESS) came online, the earliest confirmed exoplanets were disproportionately hot "
                 "Jupiters, giving an initially skewed impression of typical exoplanet system architecture that later, "
                 "less biased transit-survey statistics have substantially corrected.</p>",
                 [('Correctly explains the radial-velocity sensitivity bias', 8), ('Correctly explains how this biased early demographic conclusions', 7)]),
        solution(5, 'Capstone Synthesis: Our Solar System in Context',
                 "<p>[Model answer, 200-300 words; graded for content and correct hedging rather than for an exact "
                 "match] A strong answer should note: (1) the frost-line argument (Lecture 02) shows our solar system's "
                 "terrestrial/giant-planet split is a specific, well-understood consequence of where the frost line fell "
                 "in our particular protoplanetary disk, not a universal necessity -- other disks with different "
                 "temperature profiles or disk masses could plausibly produce very different architectures; (2) the "
                 "exoplanet mass-radius degeneracy (Lecture 14) shows that our confidence in solar-system-like "
                 "interior compositions elsewhere is genuinely limited by current data, an honestly open question; (3) "
                 "TRAPPIST-1's compact, resonant, tidally locked architecture (Lecture 14) has no solar-system analog at "
                 "all, and such compact systems appear statistically common in the broader exoplanet census, suggesting "
                 "our solar system's wider-orbit, non-resonant architecture may not be the 'default' outcome of planet "
                 "formation. A strong answer explicitly separates well-supported claims (the existence of common compact "
                 "systems, the basic frost-line physics) from open questions (whether Earth-like habitability is common, "
                 "whether TRAPPIST-1 planets can retain atmospheres) rather than presenting a falsely confident overall "
                 "conclusion.</p>",
                 [('Cites at least three specific pieces of evidence from across the semester', 12), ('Correctly and explicitly distinguishes well-supported claims from open questions', 12), ('Coherent, well-organized synthesis within the word limit', 6)]),
    )
    pset_html = pset_page(7, 'Capstone: Exoplanet Comparative Planetology',
                           'Synthesize the full semester\u2019s toolkit -- equilibrium temperature, tidal locking, detection-method bias, and comparative architecture -- using real TRAPPIST-1 and Kepler-186f data.',
                           ''.join(problems), 'OpenStax Astronomy 2e, Chapter 13.')
    sol_html = solutions_page(7, 'Capstone: Exoplanet Comparative Planetology', ''.join(solutions))
    asmt = assessment_md(7, 'Capstone: Exoplanet Comparative Planetology',
                          ['Problem 1: full unit-converted equilibrium-temperature calculation required, plus an appropriately hedged (not overconfident) habitability comment.',
                           'Problem 2: both ratios must be computed and explicitly compared to verify the scaling law, not just asserted.',
                           'Problem 3: must invoke the steep distance-scaling of tidal-locking timescale and correctly contrast with Mercury\'s different resonance outcome.',
                           'Problem 4: must explain the RV sensitivity bias mechanistically, not just state that hot Jupiters were found first.',
                           'Problem 5 (capstone): must cite at least three specific pieces of semester evidence and explicitly separate well-supported from open conclusions; a fluent but generic essay without specific citations or without honest hedging should not receive full credit.'],
                          ['Presenting equilibrium-temperature agreement with Earth as proof of habitability rather than as one necessary but insufficient condition (Problem 1).',
                           'Treating Mercury and the TRAPPIST-1 planets as following identical tidal-locking outcomes without accounting for the steep distance/mass scaling (Problem 3).',
                           'Writing an overly generic capstone synthesis (Problem 5) that could apply to any course rather than citing this course\'s specific quantitative results.'])
    return pset_html, sol_html, asmt


def main():
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    PSET_DIR.mkdir(parents=True, exist_ok=True)

    labs = [make_lab_01, make_lab_02, make_lab_03, make_lab_04, make_lab_05, make_lab_06, make_lab_07]
    for i, fn in enumerate(labs, start=1):
        (LAB_DIR / f"lab-{i:02d}.html").write_text(fn(), encoding='utf-8')

    psets = [make_pset_01, make_pset_02, make_pset_03, make_pset_04, make_pset_05, make_pset_06, make_pset_07]
    for i, fn in enumerate(psets, start=1):
        pset_html, sol_html, asmt = fn()
        (PSET_DIR / f"problem-set-{i:02d}.html").write_text(pset_html, encoding='utf-8')
        (PSET_DIR / f"problem-set-{i:02d}-solutions.html").write_text(sol_html, encoding='utf-8')
        (PSET_DIR / f"problem-set-{i:02d}-assessment.md").write_text(asmt, encoding='utf-8')

    print(f"Wrote {len(labs)} labs and {len(psets)} problem sets (with solutions and assessment instructions) "
          f"to {LAB_DIR} and {PSET_DIR}")


if __name__ == '__main__':
    main()









