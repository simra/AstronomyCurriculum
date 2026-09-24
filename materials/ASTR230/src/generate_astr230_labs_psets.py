"""Lab and problem-set generator for ASTR230.

Depends on the shared constants and page()/CSS helpers in
generate_astr230_content.py so every number here traces back to the same
verified real-star, Sirius B, rotation-curve, and Hubble-diagram data used
in the paired lectures. Run with the project interpreter:
    python materials/ASTR230/src/generate_astr230_content.py
    python materials/ASTR230/src/generate_astr230_labs_psets.py
"""
from __future__ import annotations

import math
from html import escape

from generate_astr230_content import (
    CSS, page, li, LAB_DIR, PSET_DIR,
    STAR_TABLE, STAR_BY_NAME, SUN, SIRIUS_A, ALPHA_CEN_A, SIRIUS_B, BETELGEUSE, PROXIMA,
    SUN_TEFF, SUN_MV, SIGMA_SB, R_SUN_M, L_SUN_W, L_SUN_PUBLISHED_W,
    ms_luminosity, ms_lifetime_gyr, CLUSTER_TURNOFF_MASS, CLUSTER_TURNOFF_AGE_MYR,
    M_SUN_KG, SIRIUS_B_MASS_KG, SIRIUS_B_RADIUS_M, SIRIUS_B_VOLUME_M3, SIRIUS_B_DENSITY_KGM3,
    CHANDRASEKHAR_LIMIT_MSUN, G_NEWTON, KPC_M, KM, ROTATION_CURVE, R_SUN_KPC, V_SUN_KMS,
    enclosed_mass_msun, MASS_AT_SUN_MSUN, MASS_AT_25KPC_MSUN, VISIBLE_MASS_MSUN,
    GALAXIES, HUBBLE_CLUSTERS, MPC_KM, fit_h0_kms_mpc, H0_FIT, HUBBLE_TIME_GYR,
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
    return page(f'ASTR 230 Lab {n:02d}', body)


def pset_page(n: int, title: str, focus: str, problems_html: str, reading: str) -> str:
    body = f"""<header><div><h1>ASTR 230 Problem Set {n:02d}: {escape(title)}</h1><p>{escape(focus)}</p></div></header>
<main><section><h2>Problems</h2>{problems_html}</section>
<section><h2>Due and Scope</h2><p>Submit a clear solution with equations, units, labeled quantities, and a short narrative interpretation for each problem. Show every step; a correct final number without visible work receives partial credit at most.</p></section>
<section><h2>OpenStax Companion Reading</h2><p>{escape(reading)}</p></section>
<section><h2>References and Data Sources</h2><ul><li>Corresponding lecture slides and notes for this unit.</li><li>{OPENSTAX}.</li><li>Course datasets under <code>materials/ASTR230/data/</code> where referenced above.</li></ul></section>
</main>"""
    return page(f'ASTR 230 Problem Set {n:02d}', body)


def solutions_page(n: int, title: str, solutions_html: str) -> str:
    body = f"<header><div><h1>Problem Set {n:02d}: Solution Key</h1><p>{escape(title)}</p></div></header><main><section><h2>Worked Solutions</h2>{solutions_html}</section><section><h2>Grading Notes</h2><p>Award full marks for correct method, units, and a numeric result consistent with the arithmetic shown (allow reasonable rounding). Verify the student re-derives the number rather than quoting it from the lecture without adapting it to the problem's specific inputs.</p></section></main>"
    return page(f'ASTR 230 Problem Set {n:02d} Solutions', body)


def assessment_md(n: int, title: str, criteria: list, common_errors: list) -> str:
    crit = '\n'.join(f'- {c}' for c in criteria)
    err = '\n'.join(f'- {e}' for e in common_errors)
    return f"""# Assessment Instructions: Problem Set {n:02d} \u2014 {title}

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the referenced dataset(s) under `materials/ASTR230/data/`.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking number but no visible reduction steps should not.

## Problem-Level Criteria
{crit}

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
{err}
"""


# ---------------------------------------------------------------------------
# LAB 01: HR Diagram
# ---------------------------------------------------------------------------
def make_lab_01() -> str:
    rows = ''.join(
        f'<tr><td>{escape(s["name"])}</td><td>{s["spt"]}</td><td>{s["teff"]:.0f}</td><td>{s["v_app"]:.2f}</td>'
        f'<td>{"\u2014" if s["parallax_mas"] is None else f"{s['parallax_mas']:.2f}"}</td><td></td><td></td></tr>'
        for s in STAR_TABLE
    )
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will use the real 20-star sample in <code>../data/nearby_bright_stars.csv</code> (apparent V magnitude, parallax in milliarcseconds, effective temperature, and spectral type for the Sun plus 19 well-known nearby or bright stars; Sirius B values are independently verified against Bond et al. 2017, <em>ApJ</em> 840, 70; see <code>../reference-log.md</code> for full provenance and spot-check notes on the remaining stars). No specialized instrument is required for this lab; it is a data-analysis lab using real published stellar parameters.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Star</th><th>Spectral type</th><th>T_eff (K)</th><th>V (apparent mag)</th><th>Parallax (mas)</th><th>Distance (pc)</th><th>M_V (absolute mag)</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>For each star with a measured parallax, compute distance d = 1/p(arcsec) in parsecs (the Sun has no meaningful stellar parallax; treat its distance as 1 AU = 4.848 &times; 10&#8315;&#8310; pc for scale only, and do not plot the Sun's absolute magnitude derived this way &mdash; use its known M_V = 4.83 directly instead).</li>
<li>Compute each star's distance modulus (m &minus; M) = 5log10(d) &minus; 5, then its absolute magnitude M_V = m &minus; (m&minus;M).</li>
<li>Plot every star on a Hertzsprung-Russell diagram: T_eff (or spectral type, decreasing left to right) on the horizontal axis, M_V (brighter/more negative upward) on the vertical axis.</li>
<li>Identify which stars fall on the main sequence, which are giants/supergiants (well above the main sequence at their temperature), and which are white dwarfs (well below the main sequence at their temperature). Label at least one example of each from your plot.</li>
<li>For Sirius A and Betelgeuse, state which spectral-classification physics from Lecture 02 explains why each shows the line strengths it does at its respective T_eff.</li>
<li>Compute the luminosity ratio between Betelgeuse and Proxima Centauri using each star's absolute magnitude (L1/L2 = 10^((M2 &minus; M1)/2.5)), and comment on how a red giant and a red dwarf can have such different luminosities despite similar surface temperatures (hint: revisit the Stefan-Boltzmann radius dependence from Lecture 01).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Distance-modulus uncertainty is dominated by parallax measurement precision; for a star with parallax uncertainty of a few percent, the resulting distance modulus uncertainty is of order 0.1 mag (a few percent in d translates to a few hundredths of a magnitude in 5log10(d)). State, for the star in your sample with the smallest parallax (largest relative uncertainty), why its derived absolute magnitude and hence its position on the H-R diagram is least certain.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed distance/absolute-magnitude table for all 20 stars.</li><li>One labeled Hertzsprung-Russell diagram with main sequence, giants/supergiants, and white dwarfs identified.</li><li>Betelgeuse/Proxima luminosity-ratio calculation with a physical interpretation.</li><li>A short (150-250 word) paragraph identifying which star in the sample has the least certain H-R diagram position and why.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct distance and absolute-magnitude arithmetic for all stars with parallax data.</li><li>H-R diagram correctly separates main-sequence, giant/supergiant, and white-dwarf populations.</li><li>Luminosity-ratio calculation shown with correct formula and units.</li><li>Uncertainty discussion identifies the correct star and correct reasoning (smallest parallax, not simply "farthest star" without justification).</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 18.1-18.2 and Chapter 19.1.</li><li>Star sample: <code>materials/ASTR230/data/nearby_bright_stars.csv</code>, generated by <code>materials/ASTR230/src/generate_astr230_content.py</code>; provenance and spot-check status logged in <code>materials/ASTR230/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(1, 'Building a Hertzsprung-Russell Diagram from Real Nearby and Bright Stars',
                     'Compute distances and absolute magnitudes for 20 real stars and construct an H-R diagram.', sections)


def make_lab_02() -> str:
    m_defect_u = 4 * 1.007825 - 4.002602
    e_per_reaction_mev = m_defect_u * 931.494
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab has two parts using real data: (1) applying the distance modulus and Stefan-Boltzmann cross-check to two contrasting stars from the Lab 01 sample, and (2) estimating the Sun's nuclear fuel supply and main-sequence lifetime from its measured luminosity, mass, and the proton-proton chain mass defect (Lecture 04).</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Sirius A: V = {SIRIUS_A['v_app']:.2f}, parallax = {SIRIUS_A['parallax_mas']:.2f} mas, T_eff = {SIRIUS_A['teff']:.0f} K, R = {SIRIUS_A['r_rsun']:.2f} R&#9737;</td><td></td></tr>
<tr><td>Alpha Centauri A: V = {ALPHA_CEN_A['v_app']:.2f}, parallax = {ALPHA_CEN_A['parallax_mas']:.2f} mas, T_eff = {ALPHA_CEN_A['teff']:.0f} K, R = {ALPHA_CEN_A['r_rsun']:.2f} R&#9737;</td><td></td></tr>
<tr><td>Solar mass</td><td>{M_SUN_KG:.3e} kg</td></tr>
<tr><td>Solar luminosity (measured)</td><td>{L_SUN_PUBLISHED_W:.3e} W</td></tr>
<tr><td>Energy released per proton-proton chain reaction</td><td>{e_per_reaction_mev:.2f} MeV = {e_per_reaction_mev*1.602e-13:.3e} J</td></tr>
<tr><td>Fraction of the Sun's mass available as core hydrogen fuel (typical estimate)</td><td>10%</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>For Sirius A and Alpha Centauri A, compute distance, distance modulus, and absolute magnitude (as in Lab 01), then compute luminosity two independent ways: from M_V (L = 10^((4.83 &minus; M_V)/2.5) L&#9737;) and from Stefan-Boltzmann (L = R&#178;(T/5778)&#8308; L&#9737;, using the given radius and T_eff).</li>
<li>Compute the percent difference between the two luminosity estimates for each star. State which star's two estimates agree more closely, and explain why, referencing the "V magnitude &asymp; bolometric magnitude" simplifying assumption from Lecture 03.</li>
<li>Using the proton-proton chain mass defect above, compute how many reactions per second are needed to produce the Sun's measured luminosity ({L_SUN_PUBLISHED_W:.3e} W).</li>
<li>Each reaction consumes 4 hydrogen-1 nuclei (mass 1.007825 u = 1.673 &times; 10&#8315;&#178;&#8309; kg each). Compute the mass of hydrogen consumed per second, then per year.</li>
<li>Assuming 10% of the Sun's mass ({M_SUN_KG:.3e} kg) is available as core fuel, compute the Sun's total main-sequence lifetime implied by this consumption rate, and compare it to the mass-luminosity-relation estimate from Lecture 06 (10 Gyr for a 1 M&#9737; star).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The two luminosity estimation methods (magnitude-based and Stefan-Boltzmann-based) rely on different simplifying assumptions (bolometric correction neglect vs. adopted radius/temperature precision); state which source of uncertainty you judge to be larger for each of your two sample stars and why.</p></section>
<section><h2>Deliverables</h2><ul><li>Completed two-method luminosity comparison table for Sirius A and Alpha Centauri A, with percent differences.</li><li>Fuel-consumption-rate calculation (reactions/second, kg H/year).</li><li>Implied main-sequence lifetime from fuel-supply reasoning, compared numerically to the Lecture 06 mass-luminosity-relation estimate.</li><li>A short paragraph explaining any discrepancy between the two lifetime estimates.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct two-method luminosity calculation and percent difference for both stars.</li><li>Correct identification of which star's estimates agree more closely, with a physically grounded explanation.</li><li>Correct reaction-rate and fuel-consumption arithmetic with units shown at each step.</li><li>Lifetime comparison correctly references the Lecture 06 mass-luminosity relation result.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 19.1-19.2 and Chapter 16.1-16.2.</li><li>Star data: <code>materials/ASTR230/data/nearby_bright_stars.csv</code>.</li></ul></section>
"""
    return lab_page(2, "Distance Modulus, Parallax, and the Sun's Nuclear Energy Budget",
                     "Cross-check stellar luminosities by two methods and estimate the Sun's fuel supply and lifetime.", sections)


def make_lab_03() -> str:
    masses = [0.5, 1.0, 3.0, 10.0]
    rows = ''.join(
        f'<tr><td>{m:.1f}</td><td>{ms_luminosity(m):.2f}</td><td>{ms_lifetime_gyr(m):.4f}</td><td>{ms_lifetime_gyr(m)*1000:.1f}</td></tr>'
        for m in masses
    )
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab applies the mass-luminosity relation and main-sequence-lifetime scaling from Lecture 06 to a representative young open cluster whose brightest (most massive) main-sequence star has an inferred mass of {CLUSTER_TURNOFF_MASS:.1f} M&#9737;, consistent with published turnoff masses for clusters of this type (e.g. the Pleiades-class age range); no specialized apparatus is needed, only the mass-luminosity relation itself.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Mass (M&#9737;)</th><th>L = M^3.5 (L&#9737;)</th><th>Main-sequence lifetime (Gyr)</th><th>Lifetime (Myr)</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Verify the four rows in the Materials table by computing L = M^3.5 and t = 10 Gyr &times; M^&minus;2.5 for each mass, showing your arithmetic for at least two of the four masses.</li>
<li>A cluster's main-sequence turnoff mass is observed to be {CLUSTER_TURNOFF_MASS:.1f} M&#9737; (stars above this mass have already evolved off the main sequence; stars at or below it are still core-hydrogen-burning). Using the M^&minus;2.5 scaling, compute the cluster's age.</li>
<li>A second cluster has a turnoff mass of 0.9 M&#9737;. Compute its age and compare it to the age of the universe (about 13.8 Gyr) &mdash; is this turnoff mass plausible for any real cluster? Explain using the concept of globular cluster ages from Lecture 06.</li>
<li>Explain, quantitatively, why a 10 M&#9737; star's main-sequence lifetime is more than an order of magnitude shorter than a 3 M&#9737; star's, even though it has only about 3.3 times more mass (fuel).</li>
<li>Using the first cluster's {CLUSTER_TURNOFF_MASS:.1f} M&#9737; turnoff mass and its derived age, estimate roughly how much longer the cluster's 0.5 M&#9737; stars (still far below the turnoff) will remain on the main sequence before they, too, evolve off it.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The exponent in L &#8733; M^3.5 is itself an empirical fit with some scatter (real exponents range roughly 3-4 depending on mass range); state how a 10% uncertainty in the exponent would change your derived cluster age qualitatively (would the age estimate become more or less uncertain at higher turnoff mass, where the lifetime is most sensitive to the exponent?).</p></section>
<section><h2>Deliverables</h2><ul><li>Verified mass-luminosity-lifetime table with shown arithmetic for at least two masses.</li><li>Cluster age calculation for the {CLUSTER_TURNOFF_MASS:.1f} M&#9737; turnoff case.</li><li>Plausibility analysis for the 0.9 M&#9737; turnoff case.</li><li>Remaining-lifetime estimate for the cluster's 0.5 M&#9737; stars.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct L and lifetime arithmetic for the verification rows.</li><li>Correct cluster age for the {CLUSTER_TURNOFF_MASS:.1f} M&#9737; case (within rounding).</li><li>Correct, well-reasoned plausibility judgment for the 0.9 M&#9737; case referencing the age of the universe.</li><li>Correct comparative reasoning for the 10 M&#9737; vs. 3 M&#9737; lifetime scaling.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 22.1-22.3.</li><li>Mass-luminosity relation and turnoff mass computed in <code>materials/ASTR230/src/generate_astr230_content.py</code>.</li></ul></section>
"""
    return lab_page(3, "Main-Sequence Lifetimes and a Star Cluster's Turnoff Age",
                     'Use the mass-luminosity relation to date a star cluster from its main-sequence turnoff mass.', sections)


def make_lab_04() -> str:
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>This lab uses Sirius B's independently measured mass, radius, luminosity, and temperature (Bond et al. 2017, <em>ApJ</em> 840, 70, combined with the Hipparcos parallax of 2.637 pc; see <code>../reference-log.md</code>) to compute its density and compare it to the Chandrasekhar limit and to familiar densities.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>
<tr><td>Sirius B mass</td><td>1.018 &plusmn; 0.011 M&#9737; = {SIRIUS_B_MASS_KG:.4e} kg</td></tr>
<tr><td>Sirius B radius</td><td>0.008098 R&#9737; = {SIRIUS_B_RADIUS_M:.4e} m (5,634 km)</td></tr>
<tr><td>Sirius B luminosity</td><td>0.02448 L&#9737;</td></tr>
<tr><td>Sirius B effective temperature</td><td>25,000 K</td></tr>
<tr><td>Chandrasekhar limit</td><td>{CHANDRASEKHAR_LIMIT_MSUN} M&#9737;</td></tr>
<tr><td>Water density (comparison)</td><td>1,000 kg/m&#179;</td></tr>
<tr><td>Earth's average density (comparison)</td><td>5,510 kg/m&#179;</td></tr>
</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>Compute Sirius B's volume, V = (4/3)&#960;R&#179;, from its measured radius.</li>
<li>Compute Sirius B's average density, &#961; = M/V, in kg/m&#179; and convert to g/cm&#179;.</li>
<li>Compute the ratio of Sirius B's density to water's and to Earth's average density.</li>
<li>Using Stefan-Boltzmann (L = 4&#960;R&#178;&#963;T&#8308;), independently verify Sirius B's quoted luminosity (0.02448 L&#9737;) from its measured radius and temperature. Report the percent agreement with the quoted value.</li>
<li>State Sirius B's mass as a fraction of the Chandrasekhar limit, and explain what would need to happen (physically) for Sirius B to approach that limit, referencing Lecture 08's Type Ia supernova mechanism.</li>
<li>A hypothetical second white dwarf has a measured radius of 0.0050 R&#9737; and the same average density you computed for Sirius B. Compute its implied mass, and state whether that mass is physically plausible for a white dwarf (compare to the Chandrasekhar limit).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Sirius B's mass carries a published uncertainty of &plusmn;0.011 M&#9737; (about 1%) and its radius carries an uncertainty of about &plusmn;0.6%. Propagate these into density uncertainty using &#963;_&#961;/&#961; = &#8730;[(&#963;_M/M)&#178; + (3&#963;_R/R)&#178;] (the factor of 3 arises because density depends on R&#179;), and report the resulting percent uncertainty on the density you computed.</p></section>
<section><h2>Deliverables</h2><ul><li>Sirius B volume and density calculation (kg/m&#179; and g/cm&#179;), with density uncertainty propagated.</li><li>Density ratio to water and to Earth.</li><li>Stefan-Boltzmann luminosity cross-check with percent agreement to the quoted value.</li><li>Mass-to-Chandrasekhar-limit ratio and physical discussion.</li><li>Hypothetical second-white-dwarf mass calculation and plausibility judgment.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct volume and density arithmetic with units at each step.</li><li>Correct density-uncertainty propagation using the R&#179; scaling factor of 3.</li><li>Stefan-Boltzmann cross-check computed correctly and compared quantitatively to the quoted luminosity.</li><li>Physically sound discussion of the Chandrasekhar limit and the hypothetical white dwarf's plausibility.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 23.1.</li><li>Sirius B measurements: Bond, H. E. et al. (2017), <em>ApJ</em> 840, 70; verified via live retrieval, logged in <code>materials/ASTR230/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(4, 'White Dwarf Density and the Chandrasekhar Limit: Sirius B',
                     "Compute Sirius B's density from real measured mass and radius and compare it to the Chandrasekhar limit.", sections)


def make_lab_05() -> str:
    rows = ''.join(
        f'<tr><td>{r:.1f}</td><td>{v:.0f}</td><td></td></tr>'
        for r, v in ROTATION_CURVE
    )
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will use a representative Milky Way circular-velocity (rotation) curve, <code>../data/milky_way_rotation_curve.csv</code>, consistent with published 21-cm and stellar-tracer rotation curves (e.g. Eilers et al. 2019, <em>ApJ</em> 871, 120; see <code>../reference-log.md</code> for exact provenance and spot-check status of these specific data points), to compute the Milky Way's enclosed mass at several radii and compare it to the visible (stellar + gas) mass.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Radius (kpc)</th><th>Circular velocity (km/s)</th><th>Enclosed mass (M&#9737;)</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small">Solar radius R&#8320; = {R_SUN_KPC:.1f} kpc, solar circular velocity V&#8320; = {V_SUN_KMS:.0f} km/s. Visible (stellar + gas) mass estimate for comparison: {VISIBLE_MASS_MSUN:.1e} M&#9737;.</p></section>
<section><h2>Procedure</h2><ol>
<li>Using M(R) = V(R)&#178;R/G, compute the enclosed mass at R = 2 kpc, R = R&#8320; = {R_SUN_KPC:.1f} kpc, and R = 25 kpc. Show unit conversions (kpc to meters, km/s to m/s) explicitly.</li>
<li>Plot enclosed mass versus radius for all nine data points in the table. Describe the shape of the curve (does mass grow linearly with radius, faster, or slower, over the range where velocity is roughly flat?).</li>
<li>If all of the Galaxy's mass were interior to R = 8 kpc (visible disk), predict qualitatively what the rotation curve should do beyond 8 kpc, and explain why the observed flat curve is inconsistent with that prediction.</li>
<li>Compute the ratio of enclosed mass at 25 kpc to the visible mass estimate ({VISIBLE_MASS_MSUN:.1e} M&#9737;), and state what fraction of the Galaxy's total mass within 25 kpc must be non-luminous (dark matter) under this comparison.</li>
<li>A hypothetical galaxy has a flat rotation curve at 300 km/s out to 40 kpc. Compute its enclosed mass at 40 kpc and compare it (as a ratio) to the Milky Way's enclosed mass at 25 kpc.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The dominant uncertainty in this method is not the velocity measurement itself (21-cm line centroids are measured very precisely) but the assumption of circular, planar orbits and a well-determined distance to the Galactic center; state qualitatively how an error in R&#8320; (e.g. if the true solar radius were 8.5 kpc rather than 8.2 kpc) would propagate into the enclosed-mass estimate at the solar radius.</p></section>
<section><h2>Deliverables</h2><ul><li>Enclosed-mass calculations at R = 2, {R_SUN_KPC:.1f}, and 25 kpc with unit conversions shown.</li><li>Completed enclosed-mass-vs-radius table and plot for all nine data points.</li><li>Dark-matter mass-fraction calculation at 25 kpc.</li><li>Hypothetical-galaxy comparison calculation.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct unit conversions and enclosed-mass arithmetic at all three specified radii.</li><li>Correct qualitative description of the mass-vs-radius trend and its implication for a flat rotation curve.</li><li>Correct dark-matter mass-fraction calculation and physically sound interpretation.</li><li>Correct hypothetical-galaxy mass ratio.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 25.1-25.4.</li><li>Rotation curve: <code>materials/ASTR230/data/milky_way_rotation_curve.csv</code>; representative of published results, logged with spot-check status in <code>materials/ASTR230/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(5, "The Milky Way's Rotation Curve and the Dark Matter Budget",
                     'Compute the enclosed mass of the Milky Way at several radii and quantify the dark matter fraction.', sections)


def make_lab_06() -> str:
    rows = ''.join(
        f'<tr><td>{escape(name)}</td><td>{htype}</td><td>{d:.1f}</td><td>{diam}</td><td>{escape(note)}</td><td></td></tr>'
        for name, htype, d, diam, note in GALAXIES
    )
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will classify six real, well-documented galaxies (data in <code>../data/</code> and the table below; images should be retrieved from a public archive such as the Hubble Legacy Archive or NASA/IPAC Extragalactic Database for the version of this lab used in class, per your instructor's instructions) using the Hubble tuning fork.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Galaxy</th><th>Hubble type</th><th>Distance (Mpc)</th><th>Angular diameter (arcmin, approx.)</th><th>Note</th><th>Your classification reasoning</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>For each galaxy, without looking at the provided Hubble type column, classify it as elliptical, spiral (unbarred), barred spiral, or irregular based on its image, and estimate a bulge-to-disk ratio (large, moderate, small, or none) from its visual structure.</li>
<li>Compare your classification to the published Hubble type in the table. For any disagreement, state what visual feature likely caused the discrepancy (e.g., inclination/viewing angle, image depth, resolution).</li>
<li>Rank the six galaxies from least to most ongoing star formation based on morphology alone (bulge-to-disk ratio and, where visible, blue/red color), then explain your ranking using the physical connections from Lecture 11 (gas content, stellar population age).</li>
<li>M87 and M104 both have prominent bulges and comparatively little ongoing star formation, yet one is classified as an elliptical (E0/cD) and the other as a spiral (SA(s)a). Identify the specific visual feature that distinguishes them despite their morphological similarity.</li>
<li>M82's classification is simply "Irregular (starburst)" rather than a Hubble tuning-fork letter/number. Explain, using Lecture 12's discussion of galaxy interactions, why M82 does not fit cleanly into the elliptical/spiral tuning-fork scheme.</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>Morphological classification by eye has genuine observer-to-observer disagreement, especially for borderline Sa/SBa or highly inclined galaxies where a disk can be mistaken for an elliptical. State which of your six classifications you are least confident in and why (e.g., insufficient spatial resolution, ambiguous inclination, or a genuinely intermediate morphology).</p></section>
<section><h2>Deliverables</h2><ul><li>Completed classification table with your independent reasoning column filled in before comparing to the published types.</li><li>Star-formation ranking with physical justification.</li><li>M87-vs-M104 discriminating-feature discussion.</li><li>M82 tuning-fork-fit discussion.</li><li>Confidence statement for your least-certain classification.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Classifications are justified with specific visual/physical reasoning, not just a label.</li><li>Star-formation ranking is physically grounded in gas content and stellar population age, not guessed.</li><li>M87/M104 and M82 discussions correctly identify the relevant discriminating features.</li><li>Confidence statement identifies a genuine source of classification uncertainty.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 26.1-26.3, Chapter 27.1-27.4, Chapter 28.1-28.2.</li><li>Galaxy properties: standard de Vaucouleurs/RC3-style classifications, widely reproduced in NED and SIMBAD; logged with spot-check status in <code>materials/ASTR230/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(6, 'Classifying Real Galaxies on the Hubble Tuning Fork',
                     'Classify six well-documented real galaxies and connect morphology to physical properties.', sections)


def make_lab_07() -> str:
    rows = ''.join(
        f'<tr><td>{escape(name)}</td><td>{d:.1f}</td><td>{v:.0f}</td><td></td></tr>'
        for name, d, v in HUBBLE_CLUSTERS
    )
    sections = f"""
<section><h2>Apparatus and Setup</h2><p>You will use the classic five-cluster redshift-distance data set, <code>../data/hubble_diagram_clusters.csv</code> (representative of the type of data compiled in early Hubble-diagram studies; see <code>../reference-log.md</code> for spot-check status), to fit Hubble's law and estimate the age of the universe.</p></section>
<section><h2>Materials and Data</h2><table><thead><tr><th>Cluster</th><th>Distance (Mpc)</th><th>Recession velocity (km/s)</th><th>v/d (km/s/Mpc)</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Procedure</h2><ol>
<li>For each cluster, compute v/d in km/s/Mpc, and note how consistent the five ratios are with each other.</li>
<li>Compute a best-fit Hubble constant using H&#8320; = &#931;(v&times;d) / &#931;(d&times;d) (a line through the origin, since Hubble's law predicts v = 0 at d = 0), and show your sum-of-products and sum-of-squares calculations explicitly.</li>
<li>Convert your fitted H&#8320; (in km/s/Mpc) into a Hubble time in years, using 1 Mpc = {MPC_KM:.4e} km and 1 year = 3.156 &times; 10&#8317; s. Show the full unit conversion.</li>
<li>Compare your Hubble-time estimate to the independently measured age of the universe from the cosmic microwave background (about 13.8 billion years). State whether your estimate is higher, lower, or consistent, and explain one physical reason an exactly-constant-expansion-rate assumption (implicit in using 1/H&#8320; as an age) might not exactly match the true age.</li>
<li>Using your fitted H&#8320;, predict the recession velocity of a cluster at 700 Mpc, and state whether such a velocity is physically sensible (compare to the speed of light).</li>
</ol></section>
<section><h2>Analysis and Uncertainty</h2><p>The five v/d ratios you computed in Step 1 are not identical to each other, reflecting both measurement uncertainty and each cluster's own "peculiar velocity" (motion relative to the smooth cosmic expansion, caused by local gravitational interactions). State which cluster's v/d ratio deviates most from your fitted H&#8320;, and explain why a single galaxy's or cluster's peculiar velocity matters more for nearby objects (like Virgo) than for very distant ones (like Bootes).</p></section>
<section><h2>Deliverables</h2><ul><li>Completed v/d ratio table for all five clusters.</li><li>Fitted H&#8320; with the sum-of-products/sum-of-squares calculation shown.</li><li>Hubble-time calculation with full unit conversion shown.</li><li>700 Mpc prediction and physical-sensibility discussion.</li><li>Peculiar-velocity discussion identifying the most-deviant cluster.</li></ul></section>
<section><h2>Assessment Criteria</h2><ul><li>Correct v/d arithmetic for all five clusters.</li><li>Correct H&#8320; fit using the specified through-the-origin method, with visible sums.</li><li>Correct unit conversion from km/s/Mpc to a Hubble time in years.</li><li>Physically sound comparison to the CMB-based age and to the 700 Mpc extrapolation.</li></ul></section>
<section><h2>References and Provenance</h2><ul><li>{OPENSTAX}, Chapter 29.1-29.3.</li><li>Cluster data: <code>materials/ASTR230/data/hubble_diagram_clusters.csv</code>; classic pedagogical data set, logged with spot-check status in <code>materials/ASTR230/reference-log.md</code>.</li></ul></section>
"""
    return lab_page(7, "Hubble's Law: Distance, Redshift, and the Age of the Universe",
                     "Fit Hubble's law to real cluster data and estimate the age of the universe.", sections)


LAB_BUILDERS = [make_lab_01, make_lab_02, make_lab_03, make_lab_04, make_lab_05, make_lab_06, make_lab_07]


def write_labs():
    for i, builder in enumerate(LAB_BUILDERS, start=1):
        (LAB_DIR / f'lab-{i:02d}.html').write_text(builder(), encoding='utf-8')


# ---------------------------------------------------------------------------
# PROBLEM SETS 01-07 (student sheet, solutions, assessment instructions)
# ---------------------------------------------------------------------------

def build_ps01():
    title = 'Stellar Properties, Spectra, and Classification'
    reading = f'{OPENSTAX}, Chapter 18.1-18.2 (brightness/radii of stars) and Chapter 17.1-17.4 (spectral classification).'
    vega = STAR_BY_NAME['Vega']
    rigel = STAR_BY_NAME['Rigel']
    l_rigel = (rigel['r_rsun'] ** 2) * ((rigel['teff'] / SUN_TEFF) ** 4)
    p1 = problem(1, 'Stefan-Boltzmann for Rigel',
                 f"<p>Rigel has T_eff = {rigel['teff']:.0f} K and radius {rigel['r_rsun']:.1f} R&#9737;. Using L = R&#178;(T/5778)&#8308; L&#9737;, compute Rigel's luminosity in solar units. Show every step.</p>")
    p2 = problem(2, 'Inverse-square reasoning',
                 "<p>Two stars have the same luminosity. Star A is 10 pc away and Star B is 40 pc away. Compute the ratio of their apparent brightness (flux), F_A/F_B, and state which star appears brighter and by what factor.</p>")
    p3 = problem(3, 'Spectral classification physics',
                 f"<p>Vega (A0V, T_eff = {vega['teff']:.0f} K) shows the strongest hydrogen Balmer lines of any common spectral type, while both hotter O/B stars and cooler K/M stars show weaker Balmer lines. Explain, in terms of hydrogen ionization and excitation fractions, why Balmer line strength peaks near A0 rather than at the hottest stars.</p>")
    p4 = problem(4, "Textbook problem: Sirius system radii",
                 f"<p>{OPENSTAX}, Chapter 18, Figuring for Yourself, Exercise 18.41-18.43 (Sirius system radius comparison, using T_Sun = 5800 K and T_Sirius A = 10,000 K): work through the radius ratio derivation for Sirius A relative to the Sun, then state how your result compares to the radius given for Sirius A in this course's data table ({SIRIUS_A['r_rsun']:.2f} R&#9737;).</p>")
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Stefan-Boltzmann for Rigel',
                     f"<p>L = ({rigel['r_rsun']:.1f})&#178; &times; ({rigel['teff']:.0f}/5778)&#8308; = {rigel['r_rsun']**2:.1f} &times; {(rigel['teff']/SUN_TEFF)**4:.3f} = {l_rigel:.0f} L&#9737;.</p>",
                     [('Setup and units', 5), ('Calculation', 5), ('Interpretation', 5)])
    ratio = (40/10)**2
    sol2 = solution(2, 'Inverse-square reasoning',
                     f"<p>F &#8733; 1/d&#178;, so F_A/F_B = (d_B/d_A)&#178; = (40/10)&#178; = {ratio:.0f}. Star A appears {ratio:.0f} times brighter than Star B.</p>",
                     [('Correct formula', 5), ('Correct ratio', 5), ('Correct direction (A brighter)', 5)])
    sol3 = solution(3, 'Spectral classification physics',
                     "<p>Balmer lines require neutral hydrogen atoms with their electron in the n=2 excited state. At the hottest temperatures (O/B stars), most hydrogen is ionized (no bound electron at all), so there are few neutral atoms available to produce Balmer absorption. At the coolest temperatures (K/M stars), most hydrogen remains in the unexcited ground state (n=1), unable to absorb Balmer-series photons. Only at intermediate temperatures near A0 (&asymp;9,000-10,000 K) is a large fraction of hydrogen both neutral and in the n=2 excited state, maximizing Balmer line strength.</p>",
                     [('Correct ionization-fraction reasoning (hot end)', 8), ('Correct excitation-fraction reasoning (cool end)', 7)])
    sol4 = solution(4, 'Textbook problem: Sirius system radii',
                     f"<p>Following the OpenStax worked derivation: with L_A/L_Sun and T_A/T_Sun known, R_A/R_Sun = &#8730;(L_A/L_Sun) &times; (T_Sun/T_A)&#178;. The textbook's worked example yields a radius ratio for Sirius A close to 1.7-1.8 R&#9737;, consistent with this course's adopted value of {SIRIUS_A['r_rsun']:.2f} R&#9737; to within the precision of the simplified two-temperature comparison.</p>",
                     [('Correctly reproduces the OpenStax derivation steps', 8), ('Correct numeric comparison to course value', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 Correct Stefan-Boltzmann luminosity for Rigel with units and visible arithmetic.',
        'Problem 2: 15 points \u2014 Correct flux ratio and correct identification of the brighter star.',
        'Problem 3: 15 points \u2014 Correct physical explanation referencing both ionization (hot end) and excitation (cool end).',
        'Problem 4: 15 points \u2014 Correct reproduction of the OpenStax worked radius-ratio method and a sensible numeric comparison.',
    ]
    common_errors = [
        'Confusing luminosity ratio with flux (apparent brightness) ratio.',
        'Explaining Balmer line strength using composition ("more/less hydrogen") instead of ionization/excitation state.',
        'Missing units or unstated reference values (T_Sun, R_Sun) in Stefan-Boltzmann calculations.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps02():
    title = 'Distances, Magnitudes, and Stellar Structure/Energy Generation'
    reading = f'{OPENSTAX}, Chapter 19.1-19.2 (distances and magnitudes) and Chapter 15.4-15.5, 16.1-16.2 (stellar structure and energy generation).'
    altair = STAR_BY_NAME['Altair']
    m_defect_u = 4 * 1.007825 - 4.002602
    e_mev = m_defect_u * 931.494
    p1 = problem(1, 'Parallax to distance',
                 f"<p>Altair has a measured parallax of {altair['parallax_mas']:.2f} mas. Compute its distance in parsecs and in light-years (1 pc = 3.26 ly).</p>")
    p2 = problem(2, 'Distance modulus',
                 f"<p>Altair's apparent magnitude is V = {altair['v_app']:.2f}. Using your distance from Problem 1, compute Altair's distance modulus and absolute magnitude.</p>")
    p3 = problem(3, 'Mass defect and energy release',
                 "<p>Compute the mass defect (in atomic mass units) and the energy released (in MeV) for the fusion of four hydrogen-1 nuclei (each 1.007825 u) into one helium-4 nucleus (4.002602 u), using E = &#916;mc&#178; with 1 u = 931.494 MeV/c&#178;.</p>")
    p4 = problem(4, 'Textbook problem: solar neighborhood',
                 f"<p>{OPENSTAX}, Chapter 19, Figuring for Yourself, Exercise 19.31 (verify that 1 pc = 3.09 &#215; 10&#185;&#179; km and 3.26 ly): show the unit-conversion derivation and confirm it against the parsec-to-light-year conversion you used in Problem 1.</p>")
    problems_html = p1 + p2 + p3 + p4
    d_ly = altair['d_pc'] * 3.26
    sol1 = solution(1, 'Parallax to distance',
                     f"<p>d = 1/p(arcsec) = 1/({altair['parallax_mas']:.2f}/1000) = {altair['d_pc']:.2f} pc = {altair['d_pc']:.2f} &#215; 3.26 = {d_ly:.2f} ly.</p>",
                     [('Correct parallax-to-parsec conversion', 8), ('Correct parsec-to-light-year conversion', 7)])
    sol2 = solution(2, 'Distance modulus',
                     f"<p>m &minus; M = 5log10({altair['d_pc']:.2f}) &minus; 5 = {altair['dist_mod']:.3f}. M = {altair['v_app']:.2f} &minus; ({altair['dist_mod']:.3f}) = {altair['mv']:.2f}.</p>",
                     [('Correct distance modulus', 8), ('Correct absolute magnitude', 7)])
    sol3 = solution(3, 'Mass defect and energy release',
                     f"<p>&#916;m = 4 &#215; 1.007825 &minus; 4.002602 = {m_defect_u:.6f} u. &#916;E = {m_defect_u:.6f} &#215; 931.494 = {e_mev:.2f} MeV.</p>",
                     [('Correct mass defect', 8), ('Correct energy conversion', 7)])
    sol4 = solution(4, 'Textbook problem: solar neighborhood',
                     "<p>1 pc = 206,265 AU &times; 1.496 &#215; 10&#8312; km/AU = 3.086 &#215; 10&#185;&#179; km. In light-years: 3.086 &#215; 10&#185;&#179; km / (9.461 &#215; 10&#185;&#178; km/ly) = 3.26 ly, matching the conversion factor used in Problem 1.</p>",
                     [('Correct AU-to-km derivation', 8), ('Correct final ly comparison', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 Correct parallax-to-distance conversion in both pc and ly.',
        'Problem 2: 15 points \u2014 Correct distance modulus and absolute magnitude.',
        'Problem 3: 15 points \u2014 Correct mass defect and energy-release calculation with units.',
        'Problem 4: 15 points \u2014 Correct unit-conversion derivation matching the textbook exercise.',
    ]
    common_errors = [
        'Forgetting to convert milliarcseconds to arcseconds before taking the reciprocal.',
        'Sign errors in the distance modulus (m minus M, not M minus m).',
        'Using atomic mass (u) directly as MeV without the 931.494 MeV/u conversion factor.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps03():
    title = 'Star Formation, the ISM, and Post-Main-Sequence Evolution'
    reading = f'{OPENSTAX}, Chapter 20.1-20.2 (interstellar medium) and Chapter 22.1-22.3 (post-main-sequence evolution, star clusters).'
    p1 = problem(1, 'Jeans-criterion reasoning',
                 "<p>Cloud A has T = 10 K and n = 10&#8309; molecules/cm&#179;. Cloud B has T = 100 K and n = 10&#178; molecules/cm&#179;. Using the qualitative Jeans-criterion dependence (collapse favored by low T, high n), state which cloud is more likely to be collapsing to form stars, and explain your reasoning.</p>")
    p2 = problem(2, 'Main-sequence lifetime scaling',
                 "<p>Using L = M^3.5 and t = 10 Gyr &times; M^-2.5, compute the main-sequence lifetime of a 6 M&#9737; star. Compare it to the lifetime of a 2 M&#9737; star and state the ratio.</p>")
    p3 = problem(3, 'Cluster age from turnoff mass',
                 "<p>An open cluster's main-sequence turnoff mass is measured to be 5 M&#9737;. Compute the cluster's age in millions of years.</p>")
    p4 = problem(4, 'Textbook problem: cluster ages',
                 f"<p>{OPENSTAX}, Chapter 22, Figuring for Yourself, Exercise 22.34-22.35 (estimating cluster ages from the luminosity of the most massive main-sequence star): using the mass-luminosity relation, identify the mass of a star with luminosity 10&#8308; L&#9737; and compute the implied cluster age using this problem set's t = 10 Gyr &times; M^-2.5 formula.</p>")
    problems_html = p1 + p2 + p3 + p4
    t6 = ms_lifetime_gyr(6.0)
    t2 = ms_lifetime_gyr(2.0)
    t5 = ms_lifetime_gyr(5.0) * 1000
    m_for_1e4 = 10000 ** (1/3.5)
    t_for_1e4 = ms_lifetime_gyr(m_for_1e4) * 1000
    sol1 = solution(1, 'Jeans-criterion reasoning',
                     "<p>Cloud A (cold, dense) is far more likely to be collapsing: low temperature reduces thermal pressure support, and high density increases self-gravity per unit volume, both favoring collapse. Cloud B's higher temperature and much lower density place it firmly in typical diffuse-ISM territory, stable against collapse.</p>",
                     [('Correct qualitative direction (Cloud A collapses)', 8), ('Correct physical reasoning citing both T and n', 7)])
    sol2 = solution(2, 'Main-sequence lifetime scaling',
                     f"<p>t(6 M&#9737;) = 10 &times; 6^-2.5 = {t6:.4f} Gyr. t(2 M&#9737;) = 10 &times; 2^-2.5 = {t2:.4f} Gyr. Ratio t(2)/t(6) = {t2/t6:.2f}.</p>",
                     [('Correct 6 M&#9737; lifetime', 5), ('Correct 2 M&#9737; lifetime', 5), ('Correct ratio', 5)])
    sol3 = solution(3, 'Cluster age from turnoff mass',
                     f"<p>t = 10 Gyr &times; 5^-2.5 = {ms_lifetime_gyr(5.0):.4f} Gyr = {t5:.1f} Myr.</p>",
                     [('Correct formula applied', 8), ('Correct final age in Myr', 7)])
    sol4 = solution(4, 'Textbook problem: cluster ages',
                     f"<p>From L = M^3.5 = 10&#8308;, M = (10&#8308;)^(1/3.5) = {m_for_1e4:.2f} M&#9737;. Age = 10 Gyr &times; ({m_for_1e4:.2f})^-2.5 = {t_for_1e4:.1f} Myr.</p>",
                     [('Correct mass from luminosity', 8), ('Correct implied cluster age', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 Correct qualitative Jeans-criterion conclusion with physical reasoning for both temperature and density.',
        'Problem 2: 15 points \u2014 Correct lifetimes for both masses and correct ratio.',
        'Problem 3: 15 points \u2014 Correct cluster age in Myr.',
        'Problem 4: 15 points \u2014 Correct mass-from-luminosity inversion and correct resulting age.',
    ]
    common_errors = [
        'Reasoning about Jeans collapse using only temperature or only density, not both.',
        'Forgetting to convert Gyr to Myr where requested.',
        'Sign errors in the M^-2.5 exponent (computing M^2.5 instead).',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps04():
    title = 'White Dwarfs, Supernovae, and Neutron Stars'
    reading = f'{OPENSTAX}, Chapter 23.1 (white dwarfs) and Chapter 23.2-23.4 (supernovae, neutron stars, pulsars).'
    hyp_r_rsun = 0.006
    hyp_r_m = hyp_r_rsun * R_SUN_M
    hyp_vol = (4/3) * math.pi * hyp_r_m ** 3
    hyp_mass_kg = SIRIUS_B_DENSITY_KGM3 * hyp_vol
    hyp_mass_msun = hyp_mass_kg / M_SUN_KG
    p1 = problem(1, "Sirius B's mass fraction of the Chandrasekhar limit",
                 f"<p>Sirius B has a measured mass of 1.018 M&#9737;. Express this as a percentage of the Chandrasekhar limit ({CHANDRASEKHAR_LIMIT_MSUN} M&#9737;), and state how much additional mass (in M&#9737;) Sirius B could accrete before reaching that limit.</p>")
    p2 = problem(2, 'Hypothetical white dwarf density and mass',
                 f"<p>Using Sirius B's density ({SIRIUS_B_DENSITY_KGM3:.3e} kg/m&#179;, from Lab 04) as typical of a carbon-oxygen white dwarf, compute the mass of a hypothetical white dwarf with radius {hyp_r_rsun} R&#9737;. State whether this mass is below or above the Chandrasekhar limit.</p>")
    p3 = problem(3, 'Neutron star spin-up from angular momentum conservation',
                 "<p>A massive-star core with radius 1.2 &#215; 10&#8308; km rotates once every 25 days before collapse. It collapses to a neutron star of radius 12 km. Using I &#8733; R&#178; and conservation of angular momentum, compute the neutron star's rotation period in seconds.</p>")
    p4 = problem(4, 'Textbook problem: Type Ia vs. Type II progenitors',
                 f"<p>{OPENSTAX}, Chapter 23, Review Questions (death of low-mass vs. massive stars): in 150-250 words, contrast the progenitor systems and observational signatures that distinguish a Type Ia from a Type II supernova, using this course's Lecture 08 vocabulary (accretion, Chandrasekhar limit, iron core, core collapse).</p>")
    problems_html = p1 + p2 + p3 + p4
    frac = 1.018 / CHANDRASEKHAR_LIMIT_MSUN * 100
    remaining = CHANDRASEKHAR_LIMIT_MSUN - 1.018
    sol1 = solution(1, "Sirius B's mass fraction of the Chandrasekhar limit",
                     f"<p>1.018 / {CHANDRASEKHAR_LIMIT_MSUN} = {frac:.1f}% of the Chandrasekhar limit. Remaining mass before reaching the limit: {CHANDRASEKHAR_LIMIT_MSUN} &minus; 1.018 = {remaining:.3f} M&#9737;.</p>",
                     [('Correct percentage', 8), ('Correct remaining-mass calculation', 7)])
    sol2 = solution(2, 'Hypothetical white dwarf density and mass',
                     f"<p>V = (4/3)&#960;({hyp_r_m:.3e})&#179; = {hyp_vol:.3e} m&#179;. M = &#961;V = {SIRIUS_B_DENSITY_KGM3:.3e} &times; {hyp_vol:.3e} = {hyp_mass_kg:.3e} kg = {hyp_mass_msun:.3f} M&#9737;, which is {'below' if hyp_mass_msun < CHANDRASEKHAR_LIMIT_MSUN else 'above'} the Chandrasekhar limit.</p>",
                     [('Correct volume', 5), ('Correct mass', 5), ('Correct Chandrasekhar comparison', 5)])
    period_days = 25 * (12/1.2e4) ** 2
    period_s = period_days * 24 * 3600
    sol3 = solution(3, 'Neutron star spin-up from angular momentum conservation',
                     f"<p>I &#8733; R&#178;, so P_final = P_initial &times; (R_final/R_initial)&#178; = 25 days &times; (12/12,000)&#178; = 25 &times; (0.001)&#178; = {period_days:.2e} days = {period_s:.4f} s.</p>",
                     [('Correct R ratio squared', 8), ('Correct final period with unit conversion', 7)])
    sol4 = solution(4, 'Textbook problem: Type Ia vs. Type II progenitors',
                     "<p>Full-credit answers should state: Type Ia progenitors are white dwarfs in binary systems that accrete mass (or merge with a companion white dwarf) and approach the Chandrasekhar limit, triggering runaway carbon fusion that disrupts the entire star with no remnant left behind and a strikingly uniform peak luminosity (useful as a standard candle). Type II progenitors are massive stars (&gt;8 M&#9737;) whose iron core cannot release further fusion energy, undergoing catastrophic core collapse that typically leaves a neutron star (or black hole) remnant and is often accompanied by a burst of neutrinos.</p>",
                     [('Correct Type Ia mechanism and remnant', 8), ('Correct Type II mechanism and remnant', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 Correct percentage and correct remaining mass to the Chandrasekhar limit.',
        'Problem 2: 15 points \u2014 Correct volume, mass, and Chandrasekhar-limit comparison.',
        'Problem 3: 15 points \u2014 Correct application of I &#8733; R&#178; angular-momentum conservation with correct final units.',
        'Problem 4: 15 points \u2014 Correct, specific contrast of Type Ia and Type II progenitors, mechanisms, and remnants.',
    ]
    common_errors = [
        'Using R instead of R\u00b2 in the angular-momentum/moment-of-inertia scaling.',
        'Describing Type Ia and Type II supernovae as differing only in brightness rather than in progenitor and mechanism.',
        'Forgetting to convert the spin period into seconds when requested.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps05():
    title = 'Black Holes and the Milky Way Rotation Curve/Dark Matter'
    reading = f'{OPENSTAX}, Chapter 24.1-24.3 (black holes) and Chapter 25.1-25.4 (the Milky Way, dark matter).'
    c_light = 2.998e8
    m_bh = 5 * M_SUN_KG
    rs_5msun = 2 * G_NEWTON * m_bh / c_light ** 2
    m_earth = 5.97e24
    rs_earth = 2 * G_NEWTON * m_earth / c_light ** 2
    r_earth_actual = 6.371e6
    p1 = problem(1, 'Schwarzschild radius of a stellar-mass black hole',
                 "<p>Compute the Schwarzschild radius of a 5 M&#9737; black hole (a plausible mass for many observed stellar-mass black holes). Show your unit conversions.</p>")
    p2 = problem(2, "Earth's Schwarzschild radius",
                 "<p>Compute the Schwarzschild radius for Earth's mass (5.97 &#215; 10&#178;&#8308; kg) and compare it to Earth's actual radius (6,371 km). State by what factor Earth would need to be compressed to become a black hole.</p>")
    p3 = problem(3, 'Enclosed mass from the rotation curve',
                 f"<p>Using M(R) = V&#178;R/G, compute the Milky Way's enclosed mass at R = 14 kpc, given a circular velocity of 224 km/s at that radius (from this unit's rotation-curve data set). Show your unit conversions.</p>")
    p4 = problem(4, 'Textbook problem: dark matter fraction',
                 f"<p>{OPENSTAX}, Chapter 25, Review Questions (evidence for dark matter from rotation curves): using your Problem 3 result and a visible-mass estimate of {VISIBLE_MASS_MSUN:.1e} M&#9737;, compute the implied dark-to-visible mass ratio at R = 14 kpc.</p>")
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Schwarzschild radius of a stellar-mass black hole',
                     f"<p>R_s = 2GM/c&#178; = 2 &times; {G_NEWTON:.3e} &times; {m_bh:.3e} / ({c_light:.3e})&#178; = {rs_5msun:.1f} m &#8776; {rs_5msun/1000:.1f} km.</p>",
                     [('Correct mass conversion to kg', 5), ('Correct formula application', 5), ('Correct final answer in km', 5)])
    factor = r_earth_actual / rs_earth
    sol2 = solution(2, "Earth's Schwarzschild radius",
                     f"<p>R_s = 2 &times; {G_NEWTON:.3e} &times; 5.97e24 / ({c_light:.3e})&#178; = {rs_earth*1000:.1f} mm &#8776; {rs_earth*100:.1f} cm. Earth's actual radius (6,371 km) is about {factor:.2e} times larger than its Schwarzschild radius, so Earth would need to be compressed by roughly that factor to become a black hole.</p>",
                     [('Correct Schwarzschild radius (order of a few cm)', 8), ('Correct compression-factor comparison', 7)])
    m14 = enclosed_mass_msun(14.0, 224.0)
    sol3 = solution(3, 'Enclosed mass from the rotation curve',
                     f"<p>R = 14 kpc = {14*KPC_M:.3e} m, V = 224 km/s = {224*KM:.3e} m/s. M = ({224*KM:.3e})&#178; &times; {14*KPC_M:.3e} / {G_NEWTON:.3e} = {m14*M_SUN_KG:.3e} kg = {m14:.3e} M&#9737;.</p>",
                     [('Correct unit conversions', 8), ('Correct final enclosed mass', 7)])
    ratio14 = (m14 - VISIBLE_MASS_MSUN) / VISIBLE_MASS_MSUN
    sol4 = solution(4, 'Textbook problem: dark matter fraction',
                     f"<p>Dark mass at 14 kpc &#8776; {m14:.3e} &minus; {VISIBLE_MASS_MSUN:.3e} = {m14-VISIBLE_MASS_MSUN:.3e} M&#9737;. Dark-to-visible ratio &#8776; {ratio14:.2f}, i.e. roughly {ratio14:.1f} times as much dark mass as visible mass is enclosed within 14 kpc.</p>",
                     [('Correct dark-mass subtraction', 8), ('Correct ratio and interpretation', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 Correct Schwarzschild radius with visible unit conversions.',
        'Problem 2: 15 points \u2014 Correct Earth Schwarzschild radius and correct compression-factor comparison.',
        'Problem 3: 15 points \u2014 Correct enclosed-mass calculation with unit conversions shown.',
        'Problem 4: 15 points \u2014 Correct dark-to-visible mass ratio and sound interpretation.',
    ]
    common_errors = [
        'Forgetting to square the speed of light in the Schwarzschild radius denominator.',
        'Mixing up kpc-to-meter and km/s-to-m/s conversions (off by factors of 1000).',
        'Reporting a dark-matter fraction rather than the ratio actually requested.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps06():
    title = 'Galaxy Classification, AGN, and Galaxy Evolution'
    reading = f'{OPENSTAX}, Chapter 26.1-26.3 (galaxy types/properties) and Chapter 27.1-27.4 (active galaxies).'
    p1 = problem(1, 'Classifying from a description',
                 "<p>A galaxy is described as: smooth, featureless, no cold gas detected, uniformly old red stellar population, roughly spherical. Classify its likely Hubble type and justify your answer using the physical connections from Lecture 11.</p>")
    p2 = problem(2, 'M-sigma relation scaling',
                 "<p>The M-sigma relation is approximately M_BH &#8733; &#963;^4. If galaxy A's bulge stellar velocity dispersion &#963; is twice galaxy B's, compute the ratio of their predicted black hole masses, M_BH,A / M_BH,B.</p>")
    p3 = problem(3, 'AGN luminosity and compactness',
                 "<p>A quasar varies significantly in brightness over a timescale of 1 day. Using the light-travel-time argument (a source cannot vary coherently on a timescale shorter than the light-crossing time of its emitting region), estimate the maximum size of the emitting region in light-days, and convert this to AU (1 light-day &#8776; 173 AU). Compare this size to the solar system's scale.</p>")
    p4 = problem(4, "Textbook problem: unified AGN model",
                 f"<p>{OPENSTAX}, Chapter 27, Review Questions (the unified model of active galactic nuclei): in 150-250 words, explain how viewing angle and accretion rate in the unified AGN model can account for the observational diversity of Seyfert galaxies, quasars, and radio galaxies.</p>")
    problems_html = p1 + p2 + p3 + p4
    sol1 = solution(1, 'Classifying from a description',
                     "<p>This description matches an elliptical galaxy (likely E0-E3 given the roughly spherical shape): the absence of cold gas and the uniformly old, red stellar population are exactly the properties associated with ellipticals in Lecture 11, since without gas there is no raw material for new (blue, young) star formation.</p>",
                     [('Correct classification (elliptical)', 8), ('Correct physical justification (gas content/age link)', 7)])
    ratio = 2 ** 4
    sol2 = solution(2, 'M-sigma relation scaling',
                     f"<p>M_BH &#8733; &#963;^4, so M_BH,A/M_BH,B = (&#963;_A/&#963;_B)^4 = 2^4 = {ratio}.</p>",
                     [('Correct exponent application', 8), ('Correct final ratio', 7)])
    size_ld = 1.0
    size_au = size_ld * 173
    sol3 = solution(3, 'AGN luminosity and compactness',
                     f"<p>A 1-day coherent variation implies an emitting region no larger than about 1 light-day &#8776; {size_au:.0f} AU across &#8212; smaller than the orbit of Neptune (about 30 AU) is not required, but the region is still remarkably compact (order of the outer solar system's scale) for a source that can outshine an entire galaxy of hundreds of billions of stars.</p>",
                     [('Correct light-travel-time reasoning', 8), ('Correct AU conversion and scale comparison', 7)])
    sol4 = solution(4, 'Textbook problem: unified AGN model',
                     "<p>Full-credit answers should explain: the unified model attributes different observed AGN classes to the same basic structure (black hole, accretion disk, dusty torus, sometimes jets) viewed from different angles (a face-on view can show the luminous accretion disk directly, e.g. quasars/Seyfert 1, while an edge-on view is obscured by the torus, e.g. Seyfert 2) and at different accretion rates and jet strengths (radio galaxies/blazars for strong jets viewed at different angles).</p>",
                     [('Correct viewing-angle explanation', 8), ('Correct accretion-rate/jet explanation', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 Correct classification with physically grounded justification.',
        'Problem 2: 15 points \u2014 Correct application of the M-sigma scaling exponent.',
        'Problem 3: 15 points \u2014 Correct light-travel-time argument and unit conversion.',
        'Problem 4: 15 points \u2014 Correct, specific explanation of the unified AGN model\u2019s viewing-angle and accretion-rate dependence.',
    ]
    common_errors = [
        'Classifying by shape alone without connecting to gas content or star-formation history.',
        'Using the wrong exponent in the M-sigma scaling (e.g., squaring instead of raising to the 4th power).',
        'Treating the unified model as claiming different AGN types are physically different objects rather than the same structure viewed differently.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


def build_ps07():
    title = 'Large-Scale Structure and Observational Cosmology'
    reading = f'{OPENSTAX}, Chapter 28.3-28.5 (dark matter and large-scale structure) and Chapter 29.1-29.3 (Hubble\u2019s law and the Big Bang).'
    h0_low, h0_high = 67.0, 73.0
    t_low = (1/h0_high) * MPC_KM / (3600*24*365.25*1e9)
    t_high = (1/h0_low) * MPC_KM / (3600*24*365.25*1e9)
    p1 = problem(1, "Hubble's law prediction",
                 f"<p>Using this unit's fitted Hubble constant (H&#8320; &#8776; {H0_FIT:.1f} km/s/Mpc, from Lab 07), predict the recession velocity of a galaxy at 250 Mpc.</p>")
    p2 = problem(2, 'Hubble tension range',
                 f"<p>Modern precision measurements place H&#8320; between about {h0_low:.0f} km/s/Mpc (early-universe/CMB-based methods) and {h0_high:.0f} km/s/Mpc (local distance-ladder methods) &mdash; the &ldquo;Hubble tension.&rdquo; Compute the Hubble time implied by each end of this range, and state which is larger.</p>")
    p3 = problem(3, 'Cluster velocity dispersion and dark matter',
                 "<p>A galaxy cluster has member galaxies with velocities scattered by about 1,000 km/s around the cluster mean. Using the same M &#8733; V&#178;R/G logic as the Milky Way's rotation curve (Lecture 10), explain qualitatively why such large velocity dispersions imply a cluster mass far exceeding its visible galaxy mass, and identify one independent line of evidence (not velocity dispersion) that supports the same conclusion.</p>")
    p4 = problem(4, 'Textbook problem: the cosmic microwave background',
                 f"<p>{OPENSTAX}, Chapter 29, Review Questions (the cosmic microwave background as evidence for the Big Bang): in 150-250 words, explain why the discovery of the cosmic microwave background by Penzias and Wilson (1965) was considered strong confirmation of the Big Bang model rather than the (then-competing) Steady State model.</p>")
    problems_html = p1 + p2 + p3 + p4
    v250 = H0_FIT * 250
    sol1 = solution(1, "Hubble's law prediction",
                     f"<p>v = H&#8320;d = {H0_FIT:.1f} &times; 250 = {v250:.0f} km/s.</p>",
                     [('Correct formula application', 8), ('Correct final velocity', 7)])
    sol2 = solution(2, 'Hubble tension range',
                     f"<p>t(H&#8320;={h0_high:.0f}) = {t_low:.2f} Gyr; t(H&#8320;={h0_low:.0f}) = {t_high:.2f} Gyr. The lower H&#8320; ({h0_low:.0f} km/s/Mpc) gives the larger (older) Hubble time, since t &#8733; 1/H&#8320;.</p>",
                     [('Correct Hubble time for both endpoints', 8), ('Correct identification of which is larger and why (inverse relationship)', 7)])
    sol3 = solution(3, 'Cluster velocity dispersion and dark matter',
                     "<p>Just as M(R) = V&#178;R/G for a rotating galaxy, a cluster's dynamical mass can be estimated from its member galaxies' velocity dispersion and size using the same virial-type scaling: large velocities require large gravitating mass to keep the cluster bound, and the implied mass from 1,000 km/s velocities vastly exceeds the visible galaxy light. Independent supporting evidence: gravitational lensing of background sources by the cluster directly maps its total mass distribution and consistently shows far more mass than the visible galaxies account for (e.g., the Bullet Cluster).</p>",
                     [('Correct virial-type mass reasoning', 8), ('Correct independent evidence citation (lensing)', 7)])
    sol4 = solution(4, 'Textbook problem: the cosmic microwave background',
                     "<p>Full-credit answers should explain: the Big Bang model specifically predicted a nearly uniform, blackbody radiation field left over from the hot, dense early universe, redshifted by cosmic expansion to microwave wavelengths (a few Kelvin) today. The Steady State model, which posited a universe with no beginning and continuous matter creation, made no such prediction and had no natural explanation for a uniform microwave background. Penzias and Wilson's accidental detection of exactly this radiation field, with the predicted near-perfect blackbody spectrum and near-perfect isotropy, was therefore strong, specific confirmation of the Big Bang over its main historical competitor.</p>",
                     [('Correct explanation of what the CMB is and why the Big Bang predicted it', 8), ('Correct contrast with the Steady State model\u2019s lack of prediction', 7)])
    solutions_html = sol1 + sol2 + sol3 + sol4
    criteria = [
        'Problem 1: 15 points \u2014 Correct Hubble\u2019s law application.',
        'Problem 2: 15 points \u2014 Correct Hubble time for both endpoints and correct inverse-relationship reasoning.',
        'Problem 3: 15 points \u2014 Correct virial-type mass reasoning and a valid independent line of evidence.',
        'Problem 4: 15 points \u2014 Correct, specific explanation of the CMB\u2019s role in confirming the Big Bang over the Steady State model.',
    ]
    common_errors = [
        'Confusing the direction of the H0-to-age relationship (assuming higher H0 gives an older universe).',
        'Citing rotation curves again as the "independent" evidence for Problem 3 rather than a genuinely different method (lensing, CMB, etc.).',
        'Describing the CMB as evidence against the Steady State model without explaining what specific prediction distinguished the two models.',
    ]
    return title, reading, problems_html, solutions_html, criteria, common_errors


PSET_BUILDERS = [build_ps01, build_ps02, build_ps03, build_ps04, build_ps05, build_ps06, build_ps07]


def write_psets():
    for i, builder in enumerate(PSET_BUILDERS, start=1):
        title, reading, problems_html, solutions_html, criteria, common_errors = builder()
        (PSET_DIR / f'problem-set-{i:02d}.html').write_text(pset_page(i, title, f'Problem set for Unit {i}.', problems_html, reading), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-solutions.html').write_text(solutions_page(i, title, solutions_html), encoding='utf-8')
        (PSET_DIR / f'problem-set-{i:02d}-assessment.md').write_text(assessment_md(i, title, criteria, common_errors), encoding='utf-8')


if __name__ == '__main__':
    write_labs()
    write_psets()
    print(f'Wrote {len(LAB_BUILDERS)} labs and {len(PSET_BUILDERS)} problem sets (+ solutions + assessment instructions).')
