from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "problem-sets"
REVIEW = ROOT / "review-report.md"

CSS = """
:root { --ink:#17202a; --muted:#5b6773; --paper:#fbfcfd; --panel:#ffffff; --line:#d9e0e7; --navy:#102a43; --teal:#0f6b78; --teal-soft:#e5f4f6; --gold:#b87911; --warning:#8a4b08; }
body { margin:0; font-family:Georgia,"Times New Roman",serif; color:var(--ink); background:var(--paper); line-height:1.6; }
header { padding:38px 24px 26px; background:linear-gradient(135deg,var(--navy),var(--teal)); color:#fff; }
header div, main { max-width:1040px; margin:0 auto; }
main { padding:30px 24px 64px; }
h1,h2,h3 { line-height:1.15; }
h1 { margin:0 0 8px; font-size:clamp(2rem,4vw,3.2rem); }
h2 { margin-top:34px; color:var(--navy); border-bottom:2px solid var(--line); padding-bottom:8px; }
h3 { color:var(--teal); }
section, article.problem { background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:16px 18px; margin:16px 0; }
.meta { color:var(--muted); }
.notice { border-left:5px solid var(--teal); background:var(--teal-soft); padding:12px 16px; margin:18px 0; }
.points { color:var(--gold); font-weight:700; }
table { width:100%; border-collapse:collapse; margin:14px 0; }
th,td { border:1px solid var(--line); padding:8px 10px; vertical-align:top; text-align:left; }
th { background:var(--teal-soft); }
code { background:#eef3f5; padding:1px 4px; border-radius:3px; }
"""

PROBLEM_SETS = [
    {
        "n": 1,
        "title": "Sky Geometry and Coordinates",
        "lectures": "Lectures 01-02",
        "textbook": [
            "OpenStax Astronomy 2e, Observing the Sky exercises, Review Question 1, extracted index line 5155: latitude/longitude compared with declination/right ascension.",
            "OpenStax Astronomy 2e, Observing the Sky exercises, Review Question 3, extracted index line 5158: Moon phases, rise/set timing, and phase visibility.",
            "OpenStax Astronomy 2e, Observing the Sky exercises, Thought Question 24, extracted index line 5199: seasons and the misconception that distance causes seasons.",
            "OpenStax Astronomy 2e, Observing the Sky exercises, Thought Question 25, extracted index line 5203: sky appearance from different places on Earth.",
        ],
        "problems": [
            {
                "title": "Angular Speed of the Sky",
                "points": 12,
                "prompt": "A student begins observing a bright star when it is 35 degrees above the eastern horizon. Assume the star's apparent motion is dominated by Earth's rotation at about 15 degrees per hour. Estimate the star's altitude change after 90 minutes if its path is approximately vertical near that horizon location. State why this is only an approximation.",
                "solution": "90 minutes is 1.5 hours, so the sky rotates about 22.5 degrees. The altitude would increase from roughly 35 degrees to roughly 57.5 degrees if the path were vertical. This is approximate because real altitude change depends on declination, observer latitude, and where the object is relative to the meridian.",
            },
            {
                "title": "Coordinate Systems for an Observing Plan",
                "points": 14,
                "prompt": "You are given a target at RA 5h 30m, Dec +20 degrees. Explain which parts of that coordinate are reusable by observers anywhere on Earth and which observing quantities still depend on local time and location. Include one sentence about why altitude-azimuth coordinates are still useful at the telescope.",
                "solution": "RA and Dec are celestial-sphere coordinates and can be shared across observers. Whether the object is above the horizon and its altitude/azimuth depend on local sidereal time, latitude, date, and time. Alt-az coordinates are useful because they tell the observer where to point in the local sky at a specific moment.",
            },
            {
                "title": "Moon Phase Geometry",
                "points": 16,
                "prompt": "Draw or describe Sun-Earth-Moon geometry for first quarter Moon. Identify the approximate angle Sun-Earth-Moon, when first quarter is highest in the sky, and why this phase is not a lunar eclipse.",
                "solution": "At first quarter the Sun-Earth-Moon angle is about 90 degrees. First quarter is highest near sunset because it is about 90 degrees east of the Sun. It is not an eclipse because eclipses require alignment near the line of nodes; first quarter is not full Moon and does not pass through Earth's shadow.",
            },
            {
                "title": "Observing Log Critique",
                "points": 8,
                "prompt": "An observing note says: 'Saw Jupiter near the trees. Looked bright.' Rewrite it as a scientifically useful note with at least six pieces of information that would make the observation reproducible.",
                "solution": "A strong note includes date, clock time and time zone, observing location, sky direction/altitude estimate, weather/seeing/transparency, instrument if any, object identification method, and uncertainty or comparison object. Example: '2026-10-03, 21:15 PDT, campus observatory lawn; Jupiter estimated 18 degrees above ESE horizon, clear sky with thin haze, naked eye, identified using Stellarium chart; brightness compared with nearby Saturn; altitude uncertainty +/-5 degrees.'",
            },
        ],
    },
    {
        "n": 2,
        "title": "Scale, Distance, and Gravity",
        "lectures": "Lectures 03-04",
        "textbook": [
            "OpenStax Astronomy 2e, Science and Universe / scale exercises, Review Question 8, extracted index line 2674: angular motion of the Sun relative to fixed stars.",
            "OpenStax Astronomy 2e, Orbits and Gravity exercises, Review Question 1, extracted index line 3826: Kepler's three laws.",
            "OpenStax Astronomy 2e, Orbits and Gravity exercises, Thought Question 22, extracted index line 3867: forces in circular motion.",
            "OpenStax Astronomy 2e, Orbits and Gravity exercises, Thought Question 23, extracted index line 3869: satellite orbital speed during inward spiral.",
        ],
        "problems": [
            {
                "title": "Parallax Distance with Uncertainty",
                "points": 16,
                "prompt": "A nearby star has measured parallax p = 0.040 arcsec with uncertainty +/-0.004 arcsec. Compute its distance in parsecs and light-years. Estimate the fractional uncertainty in the distance.",
                "solution": "d = 1/p = 25 pc. Using 1 pc = 3.26 ly gives about 81.5 ly. Fractional uncertainty is approximately dp/p = 0.004/0.040 = 0.10, so the distance uncertainty is about 10%, or about +/-2.5 pc and +/-8 ly.",
            },
            {
                "title": "Solar-System Scale Model",
                "points": 12,
                "prompt": "In a scale model, Earth is 15 m from the Sun. Neptune is about 30 AU from the Sun. Where should Neptune be placed? If light takes about 8.3 minutes to travel 1 AU, how long does sunlight take to reach Neptune?",
                "solution": "If 1 AU is 15 m, 30 AU is 450 m. Light travel time is 30 x 8.3 min = 249 min, about 4.15 hours.",
            },
            {
                "title": "Kepler's Third Law",
                "points": 14,
                "prompt": "An asteroid orbits the Sun with semi-major axis a = 2.5 AU. Use P^2 = a^3 to estimate its orbital period in years. Show the calculation and interpret why the period is longer than Mars's period but shorter than Jupiter's.",
                "solution": "P^2 = 2.5^3 = 15.625, so P = sqrt(15.625) = 3.95 years. The period is longer than Mars because the orbit is larger than Mars's 1.5 AU orbit, and shorter than Jupiter because Jupiter is much farther out at 5.2 AU.",
            },
            {
                "title": "Tidal Reasoning",
                "points": 10,
                "prompt": "Tidal effects depend strongly on distance because they come from differences in gravity across an extended body. If the Moon were twice as far from Earth, would the ocean tide-raising effect be slightly smaller, about half, or much smaller? Explain qualitatively.",
                "solution": "It would be much smaller. Tidal effects scale approximately as 1/r^3, so doubling distance reduces the effect to about 1/8. Students are not required to know the exact scaling if they explain that tides depend on gravitational differences, not just gravitational force at one point.",
            },
        ],
    },
    {
        "n": 3,
        "title": "Light and Telescopes",
        "lectures": "Lectures 05-06",
        "textbook": [
            "OpenStax Astronomy 2e, Astronomical Instruments exercises, Review Question 1, extracted index line 8320: components of a modern astronomical instrument.",
            "OpenStax Astronomy 2e, Astronomical Instruments exercises, Review Question 4, extracted index line 8326: why larger telescope apertures are better.",
            "OpenStax Astronomy 2e, Astronomical Instruments exercises, Figuring for Yourself 28, extracted index line 8390: pupil diameter and light gathering.",
            "OpenStax Astronomy 2e, Astronomical Instruments exercises, Figuring for Yourself 30, extracted index line 8394: Keck telescope light gathering compared with an amateur telescope.",
        ],
        "problems": [
            {
                "title": "Frequency from Wavelength",
                "points": 12,
                "prompt": "Compute the frequency of red light with wavelength 650 nm and blue light with wavelength 450 nm using c = lambda nu. Use c = 3.00 x 10^8 m/s. Which photon has higher frequency?",
                "solution": "650 nm = 6.50e-7 m, so nu = 3.00e8 / 6.50e-7 = 4.62e14 Hz. 450 nm = 4.50e-7 m, so nu = 6.67e14 Hz. Blue light has higher frequency.",
            },
            {
                "title": "Doppler Shift of H-alpha",
                "points": 16,
                "prompt": "The H-alpha line has rest wavelength 656.3 nm. In a galaxy spectrum it is observed at 658.0 nm. Estimate radial velocity using v/c approximately equals Delta lambda / lambda. Is the galaxy moving toward or away from us along the line of sight?",
                "solution": "Delta lambda = 1.7 nm. Fractional shift = 1.7/656.3 = 0.00259. v = 0.00259c = 777 km/s using c = 3.00e5 km/s. The line is redshifted, so the motion is away along the line of sight.",
            },
            {
                "title": "Collecting Area",
                "points": 12,
                "prompt": "Compare a 20 cm telescope with a 2.0 m telescope. How many times larger is the collecting area of the 2.0 m telescope? What does this improve, and what does it not automatically fix?",
                "solution": "Diameter ratio is 2.0/0.20 = 10. Area scales as D^2, so area ratio is 100. It improves photon collection and ability to detect faint objects. It does not automatically fix atmospheric seeing, poor tracking, detector noise, or bad calibration.",
            },
            {
                "title": "Resolution Limit",
                "points": 14,
                "prompt": "Using theta = 1.22 lambda/D, compare diffraction-limited angular resolution for D = 0.10 m and D = 1.0 m at lambda = 500 nm. Give the ratio and explain why real ground-based images may not reach this limit.",
                "solution": "For the same wavelength, theta scales as 1/D. The 1.0 m telescope has 10 times smaller diffraction limit than the 0.10 m telescope. Ground-based images may be limited by atmospheric seeing, optics, focus, tracking, and detector sampling.",
            },
        ],
    },
    {
        "n": 4,
        "title": "Solar System Reasoning",
        "lectures": "Lectures 07-08",
        "textbook": [
            "OpenStax Astronomy 2e, Solar System formation exercises, Review Question 20, extracted index line 9381: solar nebula and why the Sun formed at its center.",
            "OpenStax Astronomy 2e, Solar System formation exercises, Thought Question 21, extracted index line 9383: what other stars teach about solar-system formation.",
            "OpenStax Astronomy 2e, terrestrial worlds exercises, Review Question 3, extracted index line 9340: requirements for retaining an atmosphere.",
            "OpenStax Astronomy 2e, outer solar-system exercises, Review Question 3, extracted index line 15362: evidence for a liquid-water ocean on Europa and why it matters.",
            "OpenStax Astronomy 2e, planetary evolution exercises, Review Question 8, extracted index line 17915: role of impacts in planetary evolution, including giant and modest impacts.",
        ],
        "problems": [
            {
                "title": "Mean Density and Composition",
                "points": 14,
                "prompt": "Planet A has mass 1.0 Earth masses and radius 1.0 Earth radii. Planet B has mass 0.11 Earth masses and radius 0.53 Earth radii. Compute Planet B's mean density relative to Earth using rho/rho_Earth = M/R^3. Interpret the result.",
                "solution": "rho_B/rho_E = 0.11/(0.53^3) = 0.11/0.149 = 0.74. Planet B's mean density is about 74% of Earth's, suggesting a different interior structure/composition or less compression. This resembles Mars-like comparison.",
            },
            {
                "title": "Crater Counts and Surface Age",
                "points": 10,
                "prompt": "Two airless moon surfaces are imaged at the same resolution. Region X has many overlapping craters; Region Y has few craters and smooth plains. Which region is probably older? Name one assumption behind your inference and one process that could complicate it.",
                "solution": "Region X is probably older because it accumulated more impacts. Assumption: impact rate and preservation conditions are comparable. Complications include resurfacing, lava flows, erosion by ejecta, secondary craters, or different target properties.",
            },
            {
                "title": "Escape Velocity Reasoning",
                "points": 12,
                "prompt": "Without calculating exact values, explain why a small asteroid cannot retain a thick atmosphere while a giant planet can. Use escape velocity and thermal motion in your explanation.",
                "solution": "Small asteroids have low mass and small radius, producing low escape velocity; gas molecules can more easily exceed escape speed. Giant planets have much larger escape velocity and can retain light gases more effectively, though temperature and atmospheric chemistry also matter.",
            },
            {
                "title": "Habitability Evidence Ranking",
                "points": 14,
                "prompt": "Rank Mars, Europa, Titan, and a typical main-belt asteroid by strength of evidence for potentially habitable environments, not life. Justify your ranking with energy, liquid environment, chemistry, and uncertainty.",
                "solution": "Answers may vary, but high-quality responses separate past/present liquid water, energy sources, chemistry, and evidence quality. Europa often ranks high for possible subsurface ocean plus tidal energy; Mars for past water and accessible geology; Titan for organic chemistry but very low surface temperature; typical asteroid lower unless hydrated minerals or subsurface ice are specified.",
            },
        ],
    },
    {
        "n": 5,
        "title": "Stellar Properties and Evolution",
        "lectures": "Lectures 09-10",
        "textbook": [
            "OpenStax Astronomy 2e, Stars exercises, Review Question 6, extracted index line 22241: sketch an H-R diagram and label stellar populations.",
            "OpenStax Astronomy 2e, Stellar distances exercises, Review Question 1, extracted index line 23305: parallax measurements and distance limits.",
            "OpenStax Astronomy 2e, Stellar evolution exercises, Review Question 11, extracted index line 27175: why star clusters are useful for studying stellar evolution.",
            "OpenStax Astronomy 2e, Stellar death exercises, Review Question 3, extracted index line 28874: evolution of a massive star toward supernova.",
            "OpenStax Astronomy 2e, Black holes exercises, Figuring for Yourself 20, extracted index line 30395: Schwarzschild radius for a solar-mass black hole.",
        ],
        "problems": [
            {
                "title": "Inverse-Square Brightness",
                "points": 12,
                "prompt": "Two identical stars have the same luminosity. Star B is three times farther away than Star A. What is the ratio of observed flux F_B/F_A? Explain in words.",
                "solution": "Flux scales as 1/d^2, so F_B/F_A = 1/3^2 = 1/9. The farther star appears nine times fainter even though it has the same luminosity.",
            },
            {
                "title": "Radius from Luminosity and Temperature",
                "points": 16,
                "prompt": "Star X has the same temperature as the Sun but luminosity 100 times the Sun's luminosity. Use L = 4 pi R^2 sigma T^4 to estimate its radius in solar radii. What region of the H-R diagram might it occupy?",
                "solution": "At the same temperature, L scales as R^2. R/Rsun = sqrt(100) = 10. It is much larger than the Sun at the same temperature, consistent with a giant or bright giant region rather than the main sequence Sun.",
            },
            {
                "title": "Main-Sequence Lifetime Scaling",
                "points": 14,
                "prompt": "Suppose a 5 solar-mass star has luminosity about 600 solar luminosities. Estimate its main-sequence lifetime relative to the Sun using t/t_sun approximately (M/Msun)/(L/Lsun). If the Sun's main-sequence lifetime is about 10 billion years, estimate the lifetime.",
                "solution": "t/t_sun = 5/600 = 0.00833. Lifetime = 0.00833 x 10 billion years = 83 million years. The high luminosity overwhelms the larger fuel supply.",
            },
            {
                "title": "Cluster Turnoff Interpretation",
                "points": 14,
                "prompt": "Cluster A has a main-sequence turnoff at hot blue stars. Cluster B has a turnoff near Sun-like stars. Which cluster is older? Explain using stellar mass and lifetime.",
                "solution": "Cluster B is older. Hot blue stars are massive and short-lived, so if they are still on the main sequence the cluster is young. A Sun-like turnoff means more massive stars have already evolved away, implying older age.",
            },
        ],
    },
    {
        "n": 6,
        "title": "Galaxies and Cosmology",
        "lectures": "Lectures 11-13",
        "textbook": [
            "OpenStax Astronomy 2e, galaxies exercises, Review Question 1, extracted index line 32606: distinguishing features of spiral, elliptical, and irregular galaxies.",
            "OpenStax Astronomy 2e, galaxies exercises, Review Question 7, extracted index line 32621: importance of Hubble's law.",
            "OpenStax Astronomy 2e, galaxies exercises, Review Question 8, extracted index line 32622: what it means for the universe to expand.",
            "OpenStax Astronomy 2e, galaxies exercises, Figuring for Yourself 27, extracted index line 32662: Hubble-law recession velocity calculation.",
            "OpenStax Astronomy 2e, galaxies exercises, Figuring for Yourself 30, extracted index line 32669: mass-to-light ratio for a globular cluster.",
        ],
        "problems": [
            {
                "title": "Flat Rotation Curve",
                "points": 14,
                "prompt": "A star at radius r = 8 kpc orbits at 220 km/s. Another star at r = 16 kpc also orbits at about 220 km/s. Using v^2 approximately GM(r)/r, how must enclosed mass change between 8 and 16 kpc? Why is this evidence for unseen mass?",
                "solution": "If v is constant, M(r) is proportional to r. Doubling radius requires roughly doubling enclosed mass. If visible matter fades at large radius, continued mass increase suggests unseen mass such as dark matter.",
            },
            {
                "title": "Galaxy Classification with Evidence",
                "points": 10,
                "prompt": "A galaxy has a smooth reddish light profile, little visible gas or dust, and no obvious spiral arms. Classify it as spiral, elliptical, or irregular, and state one piece of evidence that could complicate the classification.",
                "solution": "Likely elliptical. Complications: projection effects, faint shells/tidal features, dust not visible in the image, low surface-brightness disk, or limited wavelength coverage.",
            },
            {
                "title": "Hubble-Law Distance",
                "points": 14,
                "prompt": "A galaxy has recession speed 7000 km/s. Using H0 = 70 km/s/Mpc, estimate its distance in Mpc. Name two reasons this estimate may be imperfect.",
                "solution": "d = v/H0 = 7000/70 = 100 Mpc. Imperfections include peculiar velocities, measurement uncertainty, local gravitational motions, and limitations of the linear Hubble law at larger redshift.",
            },
            {
                "title": "Redshift Interpretation",
                "points": 12,
                "prompt": "A spectral line with rest wavelength 500.7 nm is observed at 515.7 nm. Compute redshift z and approximate recession speed for low redshift. Use c = 3.00 x 10^5 km/s.",
                "solution": "z = (515.7 - 500.7)/500.7 = 15.0/500.7 = 0.030. Approximate speed = zc = 9000 km/s. This is a low-redshift approximation.",
            },
        ],
    },
    {
        "n": 7,
        "title": "Synthesis and Evidence",
        "lectures": "Cumulative: Lectures 01, 04, 05, 09, 13, 14",
        "textbook": [
            "OpenStax Astronomy 2e, Science and Universe exercises, Review Question 2, extracted index line 2663: evidence that Earth is spherical.",
            "OpenStax Astronomy 2e, astrobiology/frontiers exercises, Review Question 4, extracted index line 38682: biomarkers beyond the solar system.",
            "OpenStax Astronomy 2e, astrobiology/frontiers exercises, Review Question 9, extracted index line 38689: habitable zone.",
            "OpenStax Astronomy 2e, astrobiology/frontiers exercises, Review Question 10, extracted index line 38690: methane and oxygen as biosphere evidence.",
            "OpenStax Astronomy 2e, astrobiology/frontiers exercises, Review Question 12, extracted index line 38693: requirements for habitability.",
        ],
        "problems": [
            {
                "title": "Claim Audit: Exoplanet Habitability",
                "points": 16,
                "prompt": "A headline says: 'Earth-like planet found.' List four different meanings this phrase could have. For each, name the measurement needed to support it, such as radius, mass, density, orbit, atmosphere, or biosignature evidence.",
                "solution": "Earth-like could mean Earth-sized, rocky density, Earth-like insolation/orbit, atmosphere with certain gases, liquid-water conditions, or biosignature evidence. Each requires different measurements: transit radius, radial velocity or TTV mass, density, stellar luminosity and orbital period, atmospheric spectra, and repeated biosignature/context checks.",
            },
            {
                "title": "Evidence Chain Across the Course",
                "points": 14,
                "prompt": "Choose one claim from the course: a star is a giant, a galaxy contains dark matter, or the universe is expanding. Build an evidence chain with at least four links from observation to model conclusion. Identify the weakest link.",
                "solution": "Answers vary. Example for expansion: spectra show redshift; line IDs give z; distances are estimated independently; redshift correlates with distance; expansion model explains pattern. Weak links might include distance calibration, peculiar velocities, or selection effects.",
            },
            {
                "title": "Order-of-Magnitude Sanity Check",
                "points": 12,
                "prompt": "A claim says a galaxy 100 Mpc away changes position on the sky by 1 degree in one year because it is moving sideways. Explain why this is implausible using angular motion and distance. A qualitative order-of-magnitude argument is sufficient.",
                "solution": "At 100 Mpc, 1 degree corresponds to about 0.0175 x 100 Mpc = 1.75 Mpc of transverse motion in one year, many millions of light-years per year, far faster than light. The claim is physically impossible.",
            },
            {
                "title": "Final Reflection with Quantitative Evidence",
                "points": 8,
                "prompt": "Pick one equation from the course and explain what it lets astronomers infer that cannot be measured directly. Include one limitation of the equation.",
                "solution": "Examples: parallax gives distance but only for small measurable angles; Doppler shift gives radial velocity but not transverse motion; inverse-square law gives luminosity if distance is known; Hubble law gives approximate distance/recession relation at low redshift but has scatter and cosmological limits.",
            },
        ],
    },
]


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{escape(title)}</title>
  <script id=\"MathJax-script\" async src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"></script>
  <style>{CSS}</style>
</head>
<body>{body}</body>
</html>
"""


def problem_set_html(data: dict) -> str:
    problems = "\n".join(
        f"<article class=\"problem\"><h3>{idx}. {escape(p['title'])} <span class=\"points\">{p['points']} points</span></h3><p>{escape(p['prompt'])}</p></article>"
        for idx, p in enumerate(data["problems"], start=1)
    )
    refs = "\n".join(f"<li>{escape(item)}</li>" for item in data["textbook"])
    body = f"""
<header><div><h1>Problem Set {data['n']:02d}: {escape(data['title'])}</h1><p>{escape(data['lectures'])} · Student-facing assignment</p></div></header>
<main>
<section class=\"notice\"><h2>Instructions</h2><p>Show reasoning, units, diagrams or plots where useful, and source acknowledgments. Numerical answers without explanation receive limited credit. Eligible submissions may be revised after feedback.</p></section>
<section><h2>Concrete Problems</h2>{problems}</section>
<section><h2>Recommended OpenStax Practice</h2><ul>{refs}</ul><p class=\"meta\">Recommendations are keyed to the extracted local textbook reference at <code>references/openstax-astronomy-2e-extracted.txt</code>; consult the adopted edition before assignment.</p></section>
</main>"""
    return page(f"ASTR 101 Problem Set {data['n']:02d}", body)


def solution_html(data: dict) -> str:
    rows = "\n".join(
        f"<article class=\"problem\"><h3>{idx}. {escape(p['title'])}</h3><p>{escape(p['solution'])}</p><p><strong>Rubric:</strong> Award credit for setup, physical reasoning, units, calculation or evidence, and interpretation. Distinguish arithmetic slips from conceptual errors.</p></article>"
        for idx, p in enumerate(data["problems"], start=1)
    )
    refs = "\n".join(f"<li>{escape(item)}</li>" for item in data["textbook"])
    body = f"""
<header><div><h1>Problem Set {data['n']:02d} Solution Key</h1><p>{escape(data['title'])} · Instructor-facing artifact</p></div></header>
<main>
<section class=\"notice\"><strong>Do not distribute unless solutions are intended for release.</strong></section>
<section><h2>Worked Solutions and Rubric Notes</h2>{rows}</section>
<section><h2>Textbook Problem Rationale</h2><ul>{refs}</ul><p>Use these recommendations for additional practice or adaptation. Confirm numbering against the final adopted edition before assigning.</p></section>
</main>"""
    return page(f"ASTR 101 Problem Set {data['n']:02d} Solutions", body)


def assessment_md(data: dict) -> str:
    return f"""# Assessment Instructions: Problem Set {data['n']:02d} - {data['title']}

## Inputs to Inspect

- Student submission
- `problem-set-{data['n']:02d}.html`
- `problem-set-{data['n']:02d}-solutions.html`
- `../syllabus.html`
- Relevant lecture slides and notes

## Grading Standard

Grade concrete reasoning, not just final answers. Require units, assumptions, evidence interpretation, and clear prose. For quantitative problems, identify whether errors are setup errors, unit errors, arithmetic slips, or interpretation errors.

## Problem-Specific Emphasis

This assignment covers {data['lectures']}. Feedback should explicitly connect each error to the corresponding lecture objective and to the physical model or observational evidence being practiced.

## Resubmission

Students may revise eligible work to improve mastery and grade. Feedback should identify the next reasoning step without simply replacing the student's work with the solution key.
"""


def update_review_report() -> None:
    text = REVIEW.read_text(encoding="utf-8") if REVIEW.exists() else "# ASTR 101 Course Materials Review Report\n"
    marker = "## Problem Set Second-Pass Correction"
    addition = f"""
{marker}

The first problem-set pass used generic, interchangeable prompts. This has been corrected with concrete lecture-specific problems, worked solution keys, and assessment instructions for all seven scheduled ASTR 101 problem sets.

Corrections applied:

- Added numerical, observational, interpretive, and synthesis problems keyed to specific lecture content.
- Added recommended OpenStax practice references by chapter/type/problem-number ranges where the extracted textbook supports identification.
- Added explicit quantitative work to every problem set, while keeping ASTR 101 at an introductory level.
- Left a verification note that final textbook numbering should be checked against the adopted edition before assignment.

Status: problem sets are ready for reviewer evaluation, but the course package remains not approved until the broader slide-visual and textbook-mapping issues are resolved.
"""
    if marker not in text:
        text = text.rstrip() + "\n\n" + addition.strip() + "\n"
    REVIEW.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for data in PROBLEM_SETS:
        n = data["n"]
        (OUT / f"problem-set-{n:02d}.html").write_text(problem_set_html(data), encoding="utf-8")
        (OUT / f"problem-set-{n:02d}-solutions.html").write_text(solution_html(data), encoding="utf-8")
        (OUT / f"problem-set-{n:02d}-assessment.md").write_text(assessment_md(data), encoding="utf-8")
    update_review_report()


if __name__ == "__main__":
    main()

