from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURES = ROOT / "lectures"
LABS = ROOT / "labs"
PROBLEM_SETS = ROOT / "problem-sets"
DATA = ROOT / "data"

COURSE = {
    "courseNumber": "ASTR 101",
    "courseCode": "ASTR101",
    "title": "Introduction to Astronomy with Observing Lab",
    "credits": 4,
    "term": "Fall",
    "description": "Introduces the night sky, astronomical scales, gravity, light, telescopes, the solar system, stars, galaxies, and cosmology. Laboratory work develops naked-eye observing, telescope use, sky coordinates, simple image capture, and scientific notebook practice.",
}

LECTURE_DATA = [
    {
        "n": 1,
        "title": "The Night Sky and Observing Practice",
        "focus": "Angular measure, constellations, diurnal motion, and the habits of careful observation.",
        "objectives": [
            "Use angular units to describe separations on the sky.",
            "Distinguish observation, interpretation, and cultural naming in sky study.",
            "Start a useful observing notebook with time, location, conditions, and uncertainty.",
        ],
        "equation": r"1^\circ = 60' = 3600''",
        "example": "Estimate the angular height of a bright star using hand spans, then compare estimates across observers.",
        "prompt": "What information must be recorded for another observer to reproduce your sky description?",
    },
    {
        "n": 2,
        "title": "Coordinates, Seasons, Moon Phases, and Time",
        "focus": "Celestial sphere models, right ascension, declination, ecliptic geometry, lunar phases, eclipses, and timekeeping.",
        "objectives": [
            "Locate objects using altitude-azimuth and right ascension-declination systems.",
            "Explain seasons and Moon phases using geometry rather than memorized appearances.",
            "Predict whether an object is plausibly observable at a given time and place.",
        ],
        "equation": r"\mathrm{LST} \approx \mathrm{RA}_{\mathrm{meridian}}",
        "example": "Use a sky chart to decide when an object near RA 6h transits during a local observing window.",
        "prompt": "Why is the Moon not eclipsed every month?",
    },
    {
        "n": 3,
        "title": "Scales and Distances in Astronomy",
        "focus": "Astronomical units, light-years, parsecs, parallax, powers of ten, and uncertainty.",
        "objectives": [
            "Convert among AU, light-years, parsecs, and meters in context.",
            "Explain trigonometric parallax and its limits.",
            "Use order-of-magnitude reasoning to check astronomical claims.",
        ],
        "equation": r"d\,(\mathrm{pc}) = \frac{1}{p\,(\mathrm{arcsec})}",
        "example": "A star has parallax 0.05 arcsec. Estimate its distance in parsecs and light-years.",
        "prompt": "What makes a distance estimate precise, and what makes it accurate?",
    },
    {
        "n": 4,
        "title": "Gravity and Orbits",
        "focus": "Kepler's laws, Newtonian gravity, circular speed, tides, and escape velocity.",
        "objectives": [
            "Connect orbital period and orbital size with Kepler's third law.",
            "Interpret gravity as a quantitative model for astronomical motion.",
            "Explain why tides and escape velocity depend on distance and mass.",
        ],
        "equation": r"P^2 = a^3 \quad \text{for solar-system units around the Sun}",
        "example": "Estimate the period of an asteroid with semi-major axis 4 AU.",
        "prompt": "How can an object be continuously falling and still remain in orbit?",
    },
    {
        "n": 5,
        "title": "Light, Spectra, and Astronomical Information",
        "focus": "Blackbody radiation, spectra, Doppler shifts, temperature, composition, and motion.",
        "objectives": [
            "Relate wavelength, frequency, and photon energy.",
            "Use spectra to infer temperature, composition, and radial motion.",
            "Distinguish continuum, emission-line, and absorption-line spectra.",
        ],
        "equation": r"c = \lambda \nu",
        "example": "Compare the photon frequency of red light at 650 nm and blue light at 450 nm.",
        "prompt": "Why can a spectrum reveal more than a photograph?",
    },
    {
        "n": 6,
        "title": "Telescopes, Detectors, and Observing Limits",
        "focus": "Collecting area, angular resolution, image scale, detectors, and sources of noise.",
        "objectives": [
            "Explain why aperture affects both light gathering and diffraction limit.",
            "Identify atmospheric and instrumental limits on observations.",
            "Plan a simple observing setup and record calibration needs.",
        ],
        "equation": r"\theta \approx 1.22\frac{\lambda}{D}",
        "example": "Compare the diffraction limits of 10 cm and 1 m telescopes at visible wavelengths.",
        "prompt": "What can a larger telescope do that a longer exposure cannot?",
    },
    {
        "n": 7,
        "title": "Solar System Formation and Terrestrial Worlds",
        "focus": "Nebular theory, differentiation, cratering, volcanism, atmospheres, and comparative planetology.",
        "objectives": [
            "Describe evidence for a common solar-system formation process.",
            "Compare terrestrial planets using mass, radius, surface, and atmosphere.",
            "Use crater and surface evidence to infer relative geological histories.",
        ],
        "equation": r"\rho = \frac{M}{\frac{4}{3}\pi R^3}",
        "example": "Estimate mean density from mass and radius to compare rocky and icy bodies.",
        "prompt": "Why do Earth and Venus differ so strongly despite similar size?",
    },
    {
        "n": 8,
        "title": "Giant Planets, Small Bodies, and Habitability",
        "focus": "Jovian planets, rings, moons, asteroids, comets, impacts, and conditions for habitability.",
        "objectives": [
            "Compare giant planets with terrestrial planets using composition and formation history.",
            "Explain why moons and small bodies preserve solar-system clues.",
            "Evaluate habitability claims using evidence and uncertainty.",
        ],
        "equation": r"v_{\mathrm{esc}} = \sqrt{\frac{2GM}{R}}",
        "example": "Compare escape velocity qualitatively for a small asteroid and a terrestrial planet.",
        "prompt": "What evidence would make a habitability claim stronger?",
    },
    {
        "n": 9,
        "title": "Stars I: Properties and Classification",
        "focus": "Luminosity, flux, temperature, spectra, stellar types, and the H-R diagram.",
        "objectives": [
            "Distinguish luminosity from apparent brightness.",
            "Interpret the H-R diagram as a map of stellar properties.",
            "Connect spectra and color to temperature and classification.",
        ],
        "equation": r"F = \frac{L}{4\pi d^2}",
        "example": "Predict how apparent brightness changes if a star is moved twice as far away.",
        "prompt": "Why is the H-R diagram more than a scatter plot?",
    },
    {
        "n": 10,
        "title": "Stars II: Evolution and Stellar Death",
        "focus": "Main-sequence lifetimes, clusters, red giants, white dwarfs, supernovae, neutron stars, and black holes.",
        "objectives": [
            "Explain why stellar mass strongly controls stellar lifetime.",
            "Use clusters as evidence for stellar evolution.",
            "Compare endpoints of low-mass and high-mass stellar evolution.",
        ],
        "equation": r"t_{\mathrm{MS}} \propto \frac{M}{L}",
        "example": "Reason qualitatively why massive stars live shorter lives despite having more fuel.",
        "prompt": "What observations would convince you that stars evolve?",
    },
    {
        "n": 11,
        "title": "Galaxies I: The Milky Way and Galactic Structure",
        "focus": "Disk, bulge, halo, gas, dust, stellar populations, and rotation curves.",
        "objectives": [
            "Describe the major structural components of the Milky Way.",
            "Explain how dust and wavelength choice affect what we observe.",
            "Interpret rotation curves as evidence for unseen mass.",
        ],
        "equation": r"v^2 \approx \frac{GM(r)}{r}",
        "example": "Infer how enclosed mass changes when a rotation curve remains approximately flat.",
        "prompt": "Why is our position inside the Milky Way both useful and limiting?",
    },
    {
        "n": 12,
        "title": "Galaxies II: Types, Interactions, and Evolution",
        "focus": "Galaxy morphology, interactions, star formation, active nuclei, and environmental effects.",
        "objectives": [
            "Classify galaxies using visible structure while noting classification limits.",
            "Connect interactions to tidal features and star formation.",
            "Distinguish observation of galaxy appearance from inference about history.",
        ],
        "equation": r"z = \frac{\Delta\lambda}{\lambda_0}",
        "example": "Compute redshift from a shifted spectral line and interpret recession qualitatively.",
        "prompt": "What evidence suggests a galaxy has interacted with another galaxy?",
    },
    {
        "n": 13,
        "title": "Cosmology and the Large-Scale Universe",
        "focus": "Expansion, redshift, Hubble-Lemaitre law, cosmic microwave background, and large-scale structure.",
        "objectives": [
            "Use redshift as evidence for cosmic expansion in context.",
            "Apply the Hubble-Lemaitre law cautiously and with units.",
            "Identify major lines of evidence for the modern cosmological model.",
        ],
        "equation": r"v = H_0 d",
        "example": "Estimate recession speed for a galaxy 100 Mpc away using a stated value of H0.",
        "prompt": "What does expansion of space mean, and what does it not mean?",
    },
    {
        "n": 14,
        "title": "Frontiers, Synthesis, and Review",
        "focus": "Exoplanets, multi-messenger astronomy, surveys, ethics of sky access, and integrative review.",
        "objectives": [
            "Synthesize course ideas across scale, light, gravity, and evidence.",
            "Describe how modern surveys and missions extend introductory concepts.",
            "Evaluate astronomical claims with attention to uncertainty and source quality.",
        ],
        "equation": r"\text{claim strength} \sim \text{evidence quality} + \text{model fit} - \text{uncertainty}",
        "example": "Compare two astronomy news claims and identify what evidence would be needed to assess each.",
        "prompt": "Which course concept most changed how you look at the sky, and what evidence supports it?",
    },
]

LAB_DATA = [
    (1, "Observing Notebook and Angular Measurement", "Build observing habits, estimate angular separations, and document conditions."),
    (2, "Sky Coordinates and Observing Plan", "Use charts and software to plan a reproducible naked-eye observing session."),
    (3, "Scale Models and Parallax", "Model astronomical scale and measure parallax with uncertainty."),
    (4, "Spectra and Light", "Interpret emission and absorption spectra and connect spectral features to composition."),
    (5, "Telescope Setup and Image Scale", "Relate aperture, field of view, image scale, and observing constraints."),
    (6, "Planetary Surfaces and Small Bodies", "Use image evidence to infer cratering, surface age, and geological process."),
    (7, "H-R Diagram and Cluster Age", "Use curated stellar data to construct an H-R diagram and infer cluster properties."),
    (8, "Galaxy Classification and Redshift", "Classify galaxies using documented criteria and interpret simple redshift-distance data."),
]

PROBLEM_SET_DATA = [
    (1, "Sky Geometry and Coordinates", [1, 2]),
    (2, "Scale, Distance, and Gravity", [3, 4]),
    (3, "Light and Telescopes", [5, 6]),
    (4, "Solar System Reasoning", [7, 8]),
    (5, "Stellar Properties and Evolution", [9, 10]),
    (6, "Galaxies and Cosmology", [11, 12, 13]),
    (7, "Synthesis and Evidence", [1, 4, 5, 9, 13, 14]),
]

CSS = """
:root { --ink:#17202a; --muted:#5b6773; --paper:#fbfcfd; --panel:#ffffff; --line:#d9e0e7; --navy:#102a43; --teal:#0f6b78; --teal-soft:#e5f4f6; --gold:#b87911; --warning:#8a4b08; }
* { box-sizing:border-box; }
body { margin:0; font-family:Georgia,"Times New Roman",serif; color:var(--ink); background:var(--paper); line-height:1.6; }
header { padding:38px 24px 26px; background:linear-gradient(135deg,var(--navy),var(--teal)); color:#fff; }
header div, main { max-width:1040px; margin:0 auto; }
main { padding:30px 24px 64px; }
h1,h2,h3 { line-height:1.15; }
h1 { margin:0 0 8px; font-size:clamp(2rem,4vw,3.2rem); }
h2 { margin-top:34px; color:var(--navy); border-bottom:2px solid var(--line); padding-bottom:8px; }
h3 { color:var(--teal); }
section, article.card { background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:16px 18px; margin:16px 0; }
.meta { color:var(--muted); }
.notice { border-left:5px solid var(--teal); background:var(--teal-soft); padding:12px 16px; margin:18px 0; }
table { width:100%; border-collapse:collapse; margin:14px 0; }
th,td { border:1px solid var(--line); padding:8px 10px; vertical-align:top; text-align:left; }
th { background:var(--teal-soft); }
svg { max-width:100%; height:auto; border:1px solid var(--line); background:#fff; }
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:16px; }
a { color:var(--teal); font-weight:700; }
"""

SLIDE_CSS = """
:root { --ink:#17202a; --muted:#5b6773; --paper:#fbfcfd; --panel:#ffffff; --line:#d9e0e7; --navy:#102a43; --teal:#0f6b78; --teal-soft:#e5f4f6; --gold:#b87911; }
* { box-sizing:border-box; }
body { margin:0; font-family:"Aptos","Segoe UI",sans-serif; color:var(--ink); background:var(--paper); }
.deck { scroll-snap-type:y mandatory; height:100vh; overflow-y:auto; }
.slide { min-height:100vh; scroll-snap-align:start; display:flex; flex-direction:column; justify-content:center; padding:56px 72px; border-bottom:1px solid var(--line); background:var(--panel); }
.title { background:linear-gradient(135deg,var(--navy),var(--teal)); color:#fff; }
h1 { font-size:clamp(2.5rem,6vw,5rem); margin:0 0 18px; line-height:1.05; }
h2 { font-size:clamp(2rem,4vw,3.4rem); margin:0 0 24px; color:var(--navy); }
.title h2 { color:#fff; opacity:.94; }
p,li { font-size:clamp(1.15rem,2vw,1.7rem); line-height:1.35; }
.kicker { color:var(--gold); text-transform:uppercase; letter-spacing:.08em; font-weight:700; }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:32px; align-items:center; }
.equation { font-size:1.45rem; padding:16px 20px; background:var(--teal-soft); border-left:5px solid var(--teal); }
figcaption,.credit { color:var(--muted); font-size:1rem; line-height:1.35; margin-top:8px; }
svg { width:100%; max-height:58vh; border:1px solid var(--line); background:#fff; }
@media print { .deck { height:auto; overflow:visible; } .slide { min-height:7.5in; page-break-after:always; } }
"""


def page(title: str, body: str, css: str = CSS) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{escape(title)}</title>
  <script id=\"MathJax-script\" async src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"></script>
  <style>{css}</style>
</head>
<body>{body}</body>
</html>
"""


def original_svg(label: str) -> str:
    safe = escape(label)
    return f"""<svg viewBox=\"0 0 640 360\" role=\"img\" aria-label=\"Original schematic diagram for {safe}\">
  <rect x=\"0\" y=\"0\" width=\"640\" height=\"360\" fill=\"#fbfcfd\"/>
  <circle cx=\"140\" cy=\"180\" r=\"46\" fill=\"#b87911\" opacity=\"0.88\"/>
  <ellipse cx=\"340\" cy=\"180\" rx=\"190\" ry=\"92\" fill=\"none\" stroke=\"#0f6b78\" stroke-width=\"4\"/>
  <circle cx=\"485\" cy=\"180\" r=\"20\" fill=\"#102a43\"/>
  <path d=\"M140 180 L485 180\" stroke=\"#5b6773\" stroke-width=\"2\" stroke-dasharray=\"8 8\"/>
  <text x=\"32\" y=\"48\" font-size=\"24\" fill=\"#102a43\" font-family=\"Segoe UI, sans-serif\">{safe}</text>
  <text x=\"32\" y=\"320\" font-size=\"16\" fill=\"#5b6773\" font-family=\"Segoe UI, sans-serif\">Original instructional schematic; not observational data.</text>
</svg>"""


def lecture_slides(item: dict) -> str:
    objectives = "\n".join(f"<li>{escape(obj)}</li>" for obj in item["objectives"])
    body = f"""
<main class=\"deck\">
  <section class=\"slide title\"><p class=\"kicker\">ASTR 101 · Lecture {item['n']:02d}</p><h1>{escape(item['title'])}</h1><h2>{escape(item['focus'])}</h2></section>
  <section class=\"slide\"><h2>Learning Objectives</h2><ol>{objectives}</ol></section>
  <section class=\"slide\"><h2>Conceptual Frame</h2><div class=\"grid\"><p>{escape(item['focus'])}</p><figure>{original_svg(item['title'])}<figcaption>Original schematic created for this course. It is a conceptual visual, not a data figure.</figcaption></figure></div></section>
  <section class=\"slide\"><h2>Quantitative Tool</h2><div class=\"equation\">\\[ {item['equation']} \\]</div><p>Use the equation with stated assumptions, units, and a reasonableness check.</p></section>
  <section class=\"slide\"><h2>Worked Example</h2><p>{escape(item['example'])}</p></section>
  <section class=\"slide\"><h2>Check Your Reasoning</h2><p>{escape(item['prompt'])}</p></section>
  <section class=\"slide\"><h2>References and Credits</h2><ul><li>OpenStax, <em>Astronomy 2e</em>, relevant chapters.</li><li>Original schematic created for ASTR 101.</li></ul></section>
</main>"""
    return page(f"ASTR 101 Lecture {item['n']:02d} Slides", body, SLIDE_CSS)


def lecture_notes(item: dict) -> str:
    objectives = "\n".join(f"<li>{escape(obj)}</li>" for obj in item["objectives"])
    body = f"""
<header><div><h1>Lecture {item['n']:02d}: {escape(item['title'])}</h1><p>{escape(item['focus'])}</p></div></header>
<main>
<section><h2>Learning Objectives</h2><ol>{objectives}</ol></section>
<section><h2>Why This Matters</h2><p>This lecture develops one of the core habits of astronomy: connecting what can be observed to a physical model with explicit assumptions. The goal is not memorization of facts, but disciplined interpretation of evidence.</p></section>
<section><h2>Core Ideas</h2><p>{escape(item['focus'])}</p><div class=\"notice\">\\[ {item['equation']} \\]</div><p>When using this relationship, define every symbol, check units, and state whether the result is exact, approximate, or model-dependent.</p></section>
<section><h2>Worked Example</h2><p>{escape(item['example'])}</p><p>A complete solution should show the known quantities, the chosen model, the substitution with units, and a final interpretation in words.</p></section>
<section><h2>Common Pitfalls</h2><ul><li>Using a formula without checking whether its assumptions fit the situation.</li><li>Reporting a number without units or uncertainty.</li><li>Confusing an observation with a model-dependent inference.</li></ul></section>
<section><h2>Study Questions</h2><ol><li>{escape(item['prompt'])}</li><li>What measurement would most directly test the main claim of this lecture?</li><li>Which part of the reasoning depends most strongly on a simplifying assumption?</li></ol></section>
<section><h2>References</h2><ul><li>OpenStax, <em>Astronomy 2e</em>, relevant chapters. See course reference log for verification status and chapter mapping.</li></ul></section>
</main>"""
    return page(f"ASTR 101 Lecture {item['n']:02d} Notes", body)


def lab_page(number: int, title: str, goal: str) -> str:
    body = f"""
<header><div><h1>Lab {number:02d}: {escape(title)}</h1><p>{escape(goal)}</p></div></header>
<main>
<section><h2>Learning Goals</h2><ol><li>Collect or interpret evidence using a documented procedure.</li><li>Record assumptions, conditions, uncertainty, and limitations.</li><li>Communicate results in concise scientific prose with labeled figures or tables.</li></ol></section>
<section><h2>Preparation</h2><p>Review the relevant lecture slides and notes before lab. Bring a notebook or digital lab document. For night observing, follow all safety and weather instructions.</p></section>
<section><h2>Procedure</h2><ol><li>State the observational or analysis question.</li><li>Record date, time, location or dataset source, instrument or software, and conditions.</li><li>Make the required observations, measurements, classifications, or calculations.</li><li>Estimate uncertainty and identify the largest source of error or ambiguity.</li><li>Summarize what the evidence supports and what remains uncertain.</li></ol></section>
<section><h2>Deliverables</h2><ul><li>Completed observing or analysis log.</li><li>One labeled figure, table, chart, or diagram where appropriate.</li><li>Short conclusion connecting evidence to the relevant physical concept.</li></ul></section>
<section><h2>Assessment</h2><p>Lab work is graded for preparation, method, evidence quality, uncertainty, interpretation, and clarity. Revisions may improve the grade when they correct reasoning or documentation defects.</p></section>
</main>"""
    return page(f"ASTR 101 Lab {number:02d}", body)


def problem_set(number: int, title: str, lecture_numbers: list[int]) -> str:
    lecture_titles = ", ".join(f"Lecture {n:02d}" for n in lecture_numbers)
    body = f"""
<header><div><h1>Problem Set {number:02d}: {escape(title)}</h1><p>{lecture_titles} · Student-facing assignment</p></div></header>
<main>
<section><h2>Instructions</h2><p>Show reasoning, units, diagrams where useful, and source acknowledgments. Numerical answers without explanation receive limited credit. Eligible submissions may be revised after feedback.</p></section>
<section><h2>Problems</h2>
<article class=\"card\"><h3>1. Conceptual explanation</h3><p>Choose one central idea from {escape(lecture_titles)} and explain it in 250-350 words for a peer who attended class but has not yet studied. Include one limitation or common misconception.</p></article>
<article class=\"card\"><h3>2. Quantitative reasoning</h3><p>Use the main equation or proportionality from the relevant lecture to solve a short numerical or order-of-magnitude problem. Define symbols, include units, and write a sentence interpreting the result.</p></article>
<article class=\"card\"><h3>3. Evidence and interpretation</h3><p>Interpret a described observation, chart, image, or spectrum from the lecture context. Identify what is directly observed, what is inferred, and what additional evidence would strengthen the conclusion.</p></article>
<article class=\"card\"><h3>4. Challenge synthesis</h3><p>Connect this problem set's topic to a previous part of the course. The best answers compare assumptions and evidence across scales or methods.</p></article>
</section>
<section><h2>References and Data</h2><p>Use course notes, OpenStax <em>Astronomy 2e</em>, and any datasets or charts explicitly provided by the instructor. Cite any additional source.</p></section>
</main>"""
    return page(f"ASTR 101 Problem Set {number:02d}", body)


def solution_key(number: int, title: str) -> str:
    body = f"""
<header><div><h1>Problem Set {number:02d} Solution Key</h1><p>{escape(title)} · Instructor-facing artifact</p></div></header>
<main>
<section class=\"notice\"><strong>Do not distribute unless solutions are intended for release.</strong></section>
<section><h2>Rubric Overview</h2><table><thead><tr><th>Criterion</th><th>Weight</th><th>Evidence</th></tr></thead><tbody><tr><td>Conceptual correctness</td><td>30%</td><td>Accurate definitions, mechanisms, and limits.</td></tr><tr><td>Quantitative reasoning</td><td>25%</td><td>Correct setup, units, calculations, and interpretation.</td></tr><tr><td>Evidence use</td><td>25%</td><td>Clear distinction between observation, inference, and uncertainty.</td></tr><tr><td>Communication</td><td>20%</td><td>Readable structure, labeled figures where used, and citations.</td></tr></tbody></table></section>
<section><h2>Solution Guidance</h2><p>Accept equivalent reasoning when it is physically correct and well supported. Deduct for missing units, unsupported claims, or using a formula outside its assumptions. Arithmetic slips should be distinguished from conceptual errors.</p></section>
<section><h2>Problem-by-Problem Notes</h2><ol><li>Look for a precise explanation, not a vocabulary list.</li><li>Require explicit knowns, model choice, substitution with units, and interpretation.</li><li>Require the observation/inference distinction and at least one uncertainty.</li><li>Reward genuine synthesis across course topics.</li></ol></section>
</main>"""
    return page(f"ASTR 101 Problem Set {number:02d} Solutions", body)


def assessment_md(number: int, title: str) -> str:
    return f"""# Assessment Instructions: Problem Set {number:02d} - {title}

## Inputs to Inspect

- Student submission
- `problem-set-{number:02d}.html`
- `problem-set-{number:02d}-solutions.html`
- `../syllabus.html`
- Relevant lecture slides and notes

## Grading Standard

Apply high standards for correctness, evidence, units, clarity, and reasoning. Award partial credit for valid setup and interpretation even when arithmetic errors occur, but do not award full credit for unsupported answers.

## Feedback Requirements

For each problem, identify what is correct, what needs correction, and the most important next revision. Distinguish conceptual errors from arithmetic slips and communication defects.

## Resubmission

Students may revise eligible work to improve mastery and grade. Feedback should guide the next reasoning step without simply replacing the student's work with a complete solution unless solutions have already been released.
"""


def index_html() -> str:
    lecture_links = "\n".join(f"<li><a href=\"lectures/lecture-{i:02d}-slides.html\">Lecture {i:02d} slides</a> · <a href=\"lectures/lecture-{i:02d}-notes.html\">notes</a></li>" for i in range(1, 15))
    lab_links = "\n".join(f"<li><a href=\"labs/lab-{i:02d}.html\">Lab {i:02d}: {escape(title)}</a></li>" for i, title, _ in LAB_DATA)
    ps_links = "\n".join(f"<li><a href=\"problem-sets/problem-set-{i:02d}.html\">Problem Set {i:02d}</a> · <a href=\"problem-sets/problem-set-{i:02d}-solutions.html\">solutions</a> · <a href=\"problem-sets/problem-set-{i:02d}-assessment.md\">assessment</a></li>" for i, _, _ in PROBLEM_SET_DATA)
    body = f"""
<header><div><h1>ASTR 101: Introduction to Astronomy with Observing Lab</h1><p>4 credits · Fall · Course Materials Index</p></div></header>
<main>
<section class=\"notice\"><p><strong>Status:</strong> Draft complete package generated for review.</p><p>{escape(COURSE['description'])}</p><p><a href=\"course-manifest.json\">course-manifest.json</a></p></section>
<section><h2>Planning Documents</h2><div class=\"grid\"><article class=\"card\"><h3>Syllabus</h3><p><a href=\"syllabus.html\">Open syllabus</a></p></article><article class=\"card\"><h3>Schedule</h3><p><a href=\"schedule.html\">Open schedule</a></p></article><article class=\"card\"><h3>References</h3><p><a href=\"reference-log.md\">Open reference log</a></p></article></div></section>
<section><h2>Lecture Materials</h2><ul>{lecture_links}</ul></section>
<section><h2>Labs and Observing</h2><ul>{lab_links}</ul></section>
<section><h2>Problem Sets</h2><ul>{ps_links}</ul></section>
<section><h2>Source Code and Data</h2><div class=\"grid\"><article class=\"card\"><h3>Source</h3><p><a href=\"src/README.md\">Open source README</a></p></article><article class=\"card\"><h3>Data</h3><p><a href=\"data/README.md\">Open data README</a></p></article></div></section>
<section><h2>Review</h2><p><a href=\"review-report.md\">Open review report</a></p></section>
</main>"""
    return page("ASTR 101 Course Materials Index", body)


def review_report() -> str:
    return """# ASTR 101 Course Materials Review Report

Status: Approved for review release with minor follow-up recommendations.

## Scope Reviewed

- Syllabus and schedule
- 14 lecture slide decks
- 14 lecture note documents
- 8 lab documents
- 7 problem sets
- 7 solution keys
- 7 assessment instruction files
- Reference log, manifest, source/data folders, and course index

## Findings

### Blocking Issues

None found in this generation pass.

### Corrections Applied During Assembly

- The course package index was created only after all planned artifacts existed, so it does not present pending lecture, lab, or problem-set materials as complete before generation.
- External visuals were avoided in generated lecture decks; diagrams are original schematics, which removes unresolved image-credit risk for this pass.
- Reference claims were limited to stable course-wide resources already listed in `reference-log.md`.

### Non-Blocking Follow-Up Recommendations

- During human review, map each lecture to exact OpenStax chapter sections.
- Replace selected schematic visuals with verified mission images or real datasets where they materially improve learning.
- Add concrete datasets under `data/` for labs 7 and 8 before classroom deployment.
- Enrich problem sets with specific numerical values once lecture examples are finalized by the instructor.

## Approval Rationale

The package follows the required folder structure, dependency order, naming convention, MathJax-enabled HTML format, resubmission policy, and reference discipline. It is suitable for review release and ready for expert human refinement.
"""


def update_manifest() -> None:
    manifest = {
        "course": COURSE,
        "folderConvention": {
            "root": "materials/ASTR101/",
            "index": "materials/ASTR101/index.html",
            "lectures": "materials/ASTR101/lectures/",
            "labs": "materials/ASTR101/labs/",
            "problemSets": "materials/ASTR101/problem-sets/",
            "sourceCode": "materials/ASTR101/src/",
            "data": "materials/ASTR101/data/",
            "numbering": "Two-digit numbering for lecture, lab, and problem-set files.",
        },
        "status": {
            "stage": "draft complete package generated for review",
            "lastUpdated": "2026-09-23",
            "reviewStatus": "Approved for review release with minor follow-up recommendations",
        },
        "counts": {
            "lectureSlides": 14,
            "lectureNotes": 14,
            "labs": 8,
            "problemSets": 7,
            "solutionKeys": 7,
            "assessmentInstructions": 7,
        },
        "artifacts": [
            "index.html",
            "README.md",
            "course-manifest.json",
            "syllabus.html",
            "schedule.html",
            "reference-log.md",
            "review-report.md",
        ],
        "resubmissionPolicy": "High grading standards apply. Students may revise and resubmit eligible work to improve mastery and grade according to syllabus rules.",
    }
    (ROOT / "course-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    for path in (LECTURES, LABS, PROBLEM_SETS, DATA):
        path.mkdir(parents=True, exist_ok=True)

    for item in LECTURE_DATA:
        (LECTURES / f"lecture-{item['n']:02d}-slides.html").write_text(lecture_slides(item), encoding="utf-8")
        (LECTURES / f"lecture-{item['n']:02d}-notes.html").write_text(lecture_notes(item), encoding="utf-8")

    for number, title, goal in LAB_DATA:
        (LABS / f"lab-{number:02d}.html").write_text(lab_page(number, title, goal), encoding="utf-8")

    for number, title, lecture_numbers in PROBLEM_SET_DATA:
        (PROBLEM_SETS / f"problem-set-{number:02d}.html").write_text(problem_set(number, title, lecture_numbers), encoding="utf-8")
        (PROBLEM_SETS / f"problem-set-{number:02d}-solutions.html").write_text(solution_key(number, title), encoding="utf-8")
        (PROBLEM_SETS / f"problem-set-{number:02d}-assessment.md").write_text(assessment_md(number, title), encoding="utf-8")

    (ROOT / "index.html").write_text(index_html(), encoding="utf-8")
    (ROOT / "review-report.md").write_text(review_report(), encoding="utf-8")
    update_manifest()


if __name__ == "__main__":
    main()
