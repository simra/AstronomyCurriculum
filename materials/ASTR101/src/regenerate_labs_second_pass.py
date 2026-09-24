from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "labs"
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
section { background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:16px 18px; margin:16px 0; }
.notice { border-left:5px solid var(--teal); background:var(--teal-soft); }
table { width:100%; border-collapse:collapse; margin:14px 0; }
th,td { border:1px solid var(--line); padding:8px 10px; vertical-align:top; text-align:left; }
th { background:var(--teal-soft); }
code { background:#eef3f5; padding:1px 4px; border-radius:3px; }
"""

LABS = [
    {
        "n": 1,
        "title": "Observing Notebook and Angular Measurement",
        "subtitle": "Build reproducible naked-eye observing habits and calibrate hand-angle estimates.",
        "prep": ["Read OpenStax Astronomy 2e section 2.1 on the sky above and angular measure.", "Bring a notebook or digital observing log, pencil, red-light-safe illumination if observing at night, and weather-appropriate clothing."],
        "materials": ["Naked-eye observing site or simulated sky if weather prevents outdoor work", "Printed or digital horizon diagram", "Optional: Stellarium for post-observation verification"],
        "procedure": [
            "Record date, clock time, time zone, observing location, approximate latitude/longitude if known, weather, transparency, and horizon obstructions.",
            "Identify north, east, south, and west using landmarks, compass, phone compass, or instructor-provided site orientation. Note the method used.",
            "Calibrate your hand at arm's length: estimate the width of one finger, three fingers, fist, and thumb-to-little-finger span using the class reference values, then record your personal values.",
            "Choose three bright objects. Estimate each object's altitude and azimuth using hand angles and cardinal directions.",
            "Wait at least 20 minutes or use two observations separated by class time. Re-estimate one object's position and describe the apparent motion.",
            "Sketch a horizon diagram with at least three objects, cardinal directions, altitude estimates, and obstructions."
        ],
        "analysis": ["Compute the difference between two altitude estimates for the repeated object.", "Estimate uncertainty for each hand-angle measurement, using at least +/- one finger width unless your repeated measurements justify a different value.", "State which details would allow another observer to reproduce your observation."],
        "deliverables": ["One complete observing log entry", "One labeled horizon diagram", "A 150-250 word reflection distinguishing direct observation from interpretation"],
        "assessment": ["Completeness of observing metadata", "Reasonable angular estimates with uncertainty", "Clear labeled diagram", "Correct distinction between observation and model"],
        "references": ["OpenStax Astronomy 2e, section 2.1", "Stellarium: https://stellarium.org/ or https://stellarium-web.org/ for optional verification"]
    },
    {
        "n": 2,
        "title": "Sky Coordinates and Observing Plan",
        "subtitle": "Use coordinate systems and planetarium software to plan a reproducible observing session.",
        "prep": ["Read OpenStax Astronomy 2e sections 2.1-2.2 on celestial coordinates and apparent sky motion.", "Install or open Stellarium Web and set the observing location assigned by the instructor."],
        "materials": ["Stellarium Web or desktop", "Instructor-provided target list of 5 objects", "Observing plan worksheet"],
        "procedure": [
            "Set the observing location and date/time to the assigned lab window.",
            "For each target, record RA, Dec, altitude, azimuth, rise/set or visibility notes, and whether the target is above 25 degrees altitude during the lab window.",
            "Select two feasible targets and one infeasible target. For each, explain the evidence from coordinates and local sky position.",
            "Advance time in 30-minute increments across a two-hour observing window and track altitude changes for one selected target.",
            "Create a final observing plan with target order, estimated observing times, finder directions, and backup target."
        ],
        "analysis": ["Explain why RA/Dec are reusable but altitude/azimuth are local and time dependent.", "Use the altitude trend to decide the best observing order.", "Identify one uncertainty or practical constraint such as horizon obstruction, twilight, Moon phase, weather, or instrument field of view."],
        "deliverables": ["Completed target table", "Two-paragraph observing plan", "Screenshot or exported chart with labels and source noted"],
        "assessment": ["Correct coordinate interpretation", "Feasible target selection", "Evidence-based observing sequence", "Clear chart labels and source acknowledgement"],
        "references": ["OpenStax Astronomy 2e, sections 2.1-2.2", "Stellarium Web: https://stellarium-web.org/"]
    },
    {
        "n": 3,
        "title": "Scale Models and Parallax",
        "subtitle": "Model astronomical scale and measure parallax with uncertainty.",
        "prep": ["Review the parallax relation d(pc) = 1/p(arcsec) and the scale discussion in OpenStax Astronomy 2e.", "Bring a ruler or measuring tape if instructed."],
        "materials": ["Meter sticks or measuring tape", "Two observing positions separated by a measured baseline", "Nearby object and distant background markers", "Spreadsheet or calculator"],
        "procedure": [
            "Measure a baseline between two observing positions in meters.",
            "From each baseline endpoint, record the apparent position of a nearby object against distant background markers.",
            "Measure or estimate the angular shift using a protractor, printed scale, or small-angle geometry supplied by the instructor.",
            "Repeat the measurement at least three times and compute the mean shift and range.",
            "Build a scale model in which 1 AU corresponds to a chosen classroom or campus distance, then place Earth, Mars, Jupiter, and Neptune on that scale."
        ],
        "analysis": ["Compute fractional uncertainty in the parallax measurement from repeated trials.", "Use proportional reasoning to explain why smaller parallax means larger distance.", "Compare the classroom parallax setup with stellar parallax and name two limitations of the model."],
        "deliverables": ["Baseline and parallax measurement table", "Distance estimate with uncertainty", "Scale-model table", "Short comparison of classroom and stellar parallax"],
        "assessment": ["Correct measurement procedure", "Uncertainty estimate", "Correct inverse-distance reasoning", "Clear scale conversion"],
        "references": ["OpenStax Astronomy 2e, section 19.2", "OpenStax Fig. 19.6 Parallax"]
    },
    {
        "n": 4,
        "title": "Spectra and Light",
        "subtitle": "Interpret emission and absorption spectra and connect spectral features to composition and motion.",
        "prep": ["Read OpenStax Astronomy 2e sections 5.1-5.6 on light, spectra, spectral lines, and Doppler shifts."],
        "materials": ["Instructor-provided spectra or OpenStax spectral diagrams", "Known rest wavelengths for hydrogen lines", "Calculator or spreadsheet"],
        "procedure": [
            "Classify three spectra as continuous, absorption-line, or emission-line and justify each classification from visual evidence.",
            "Identify at least two spectral lines in a provided spectrum using a rest-wavelength table.",
            "For one shifted line, measure observed wavelength and compute radial velocity using v/c = Delta lambda / lambda.",
            "Compare two spectra of the same object type and identify what changes could be due to temperature, composition, or motion.",
            "Record whether each inference is direct observation or model-dependent interpretation."
        ],
        "analysis": ["Show wavelength shift calculation with units.", "State whether the object is redshifted or blueshifted.", "Explain one reason why calibration matters before interpreting line positions."],
        "deliverables": ["Annotated spectra", "Line-identification table", "Doppler calculation", "Short interpretation paragraph"],
        "assessment": ["Correct spectrum classification", "Correct line identification", "Dimensional calculation", "Evidence/inference distinction"],
        "references": ["OpenStax Astronomy 2e, sections 5.1-5.6", "OpenStax Fig. 5.21 Three Kinds of Spectra"]
    },
    {
        "n": 5,
        "title": "Telescope Setup and Image Scale",
        "subtitle": "Relate aperture, field of view, image scale, detector sampling, and observing constraints.",
        "prep": ["Read OpenStax Astronomy 2e sections 6.1-6.5 on telescopes and instruments."],
        "materials": ["Small telescope or simulated telescope specification", "Eyepiece/camera field information", "Sample image with known angular field", "Calculator"],
        "procedure": [
            "Record telescope aperture, focal length if available, detector or eyepiece information, and observing wavelength or filter if relevant.",
            "Compute collecting-area ratio between the lab telescope and a reference 10 cm telescope.",
            "Estimate field of view using the instructor-provided method or sample image scale.",
            "Use a sample image to estimate angular separation between two objects or features.",
            "Identify at least three observing limits: atmosphere, tracking, focus, detector noise, field of view, or target brightness."
        ],
        "analysis": ["Separate what larger aperture improves from what it does not automatically fix.", "Compute one area or image-scale quantity with units.", "Explain why wavelength affects resolution and what that means for comparing optical and radio observations."],
        "deliverables": ["Instrument specification table", "Collecting-area or image-scale calculation", "Annotated sample image", "Observing-limits paragraph"],
        "assessment": ["Correct instrument quantities", "Unit-aware calculation", "Image annotation quality", "Understanding of observing limitations"],
        "references": ["OpenStax Astronomy 2e, sections 6.1-6.5", "OpenStax Fig. 6.2 and Fig. 6.8"]
    },
    {
        "n": 6,
        "title": "Planetary Surfaces and Small Bodies",
        "subtitle": "Use image evidence to infer cratering, surface age, geological process, and habitability context.",
        "prep": ["Review terrestrial planet and small-body lectures. Read relevant OpenStax solar-system chapters assigned by the instructor."],
        "materials": ["Instructor-provided planetary surface images", "Crater-count grid or digital annotation tool", "Planetary image source notes"],
        "procedure": [
            "Inspect two planetary or moon surface images at comparable scale and resolution.",
            "Count craters in at least two equal-area regions and record obvious resurfacing features such as flows, tectonic cracks, smooth plains, or ejecta blankets.",
            "Classify each region as relatively older or younger and justify the classification.",
            "For one icy moon or Mars image, identify evidence relevant to past or present liquid environments.",
            "Record source, mission/instrument if supplied, scale, wavelength/color notes, and any processing caveats."
        ],
        "analysis": ["Explain the crater-count assumption and one way it can fail.", "Distinguish surface observation from geological interpretation.", "Rank the strength of habitability evidence as weak, moderate, or strong, and justify the ranking."],
        "deliverables": ["Annotated image or crater-count table", "Relative-age interpretation", "Habitability evidence paragraph", "Source/provenance note"],
        "assessment": ["Use of image evidence", "Crater-count reasoning", "Uncertainty and caveat handling", "Source/provenance documentation"],
        "references": ["NASA Solar System Exploration: https://science.nasa.gov/solar-system/", "NASA/JPL Photojournal image pages as assigned", "OpenStax Astronomy 2e solar-system chapters"]
    },
    {
        "n": 7,
        "title": "H-R Diagram and Cluster Age",
        "subtitle": "Use curated stellar data to construct an H-R diagram and infer stellar populations and cluster age.",
        "prep": ["Read OpenStax Astronomy 2e section 18.4 on the H-R diagram and the assigned stellar evolution sections."],
        "materials": ["Instructor-provided CSV of stellar temperature/color and luminosity/absolute magnitude", "Spreadsheet or plotting tool", "OpenStax H-R diagram reference"],
        "procedure": [
            "Import or open the provided stellar dataset and identify columns for temperature or color and luminosity or absolute magnitude.",
            "Create an H-R style plot with temperature increasing to the left if using temperature.",
            "Mark the main sequence, likely giants/supergiants, and possible white dwarfs.",
            "For a cluster dataset, identify the approximate turnoff location and compare it with a younger or older reference cluster.",
            "Record plotting choices, axis units, and any data cleaning or exclusions."
        ],
        "analysis": ["Explain why the H-R diagram is physical rather than just descriptive.", "Use turnoff position to infer relative cluster age.", "Identify one selection effect or uncertainty in the dataset."],
        "deliverables": ["H-R diagram plot", "Population labels", "Cluster-age interpretation", "Short data/provenance note"],
        "assessment": ["Correct axes and orientation", "Reasonable population identification", "Turnoff reasoning", "Data documentation"],
        "references": ["OpenStax Astronomy 2e, section 18.4", "OpenStax Fig. 18.14 H-R diagram"]
    },
    {
        "n": 8,
        "title": "Galaxy Classification and Redshift",
        "subtitle": "Classify galaxies with documented criteria and interpret simple redshift-distance evidence.",
        "prep": ["Read OpenStax Astronomy 2e sections on galaxy morphology, Hubble's law, and redshift interpretation."],
        "materials": ["Instructor-provided galaxy image set", "Classification rubric", "Small redshift-distance table", "Calculator or spreadsheet"],
        "procedure": [
            "Classify at least eight galaxies as spiral, elliptical, irregular, interacting/peculiar, or uncertain using the provided rubric.",
            "For each classification, cite at least two visible criteria such as arms, smoothness, color, dust, asymmetry, tidal features, or star-forming knots.",
            "Compute redshift for two provided spectral-line measurements or use a provided redshift table.",
            "Plot recession speed versus distance for a small sample and estimate the slope.",
            "Identify one outlier or source of scatter and propose a physical or measurement explanation."
        ],
        "analysis": ["Distinguish morphology classification from evolutionary history.", "Compute or interpret Hubble-law slope with units.", "Explain why distance and redshift evidence must be calibrated before making cosmological claims."],
        "deliverables": ["Galaxy classification table", "Annotated example image", "Redshift-distance plot", "Short interpretation of slope and scatter"],
        "assessment": ["Classification evidence", "Redshift/Hubble-law calculation", "Recognition of ambiguity", "Plot labels and units"],
        "references": ["OpenStax Astronomy 2e galaxy and cosmology chapters", "ESA/Hubble image pages or NASA/IPAC metadata as assigned", "NASA/IPAC Extragalactic Database for metadata verification when used"]
    },
]


def html_list(items: list[str], tag: str = "ul") -> str:
    inner = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f"<{tag}>{inner}</{tag}>"


def apparatus_setup(lab: dict) -> list[str]:
    n = lab["n"]
    setups = {
        1: ["Prepare a horizon sheet with a 0-90 degree altitude scale and cardinal direction labels.", "Use a compass or landmark map to establish north before observations begin.", "If using a simulated sky, set location, date, and time before students enter measurements."],
        2: ["Set Stellarium to the assigned observing site and disable atmospheric refraction only if instructed.", "Load the five-object target list and verify each object has RA/Dec visible in the information panel.", "Create a two-hour observing window in 30-minute increments."],
        3: ["Set two observing stations at least 2.0 m apart and measure the baseline to the nearest centimeter.", "Place the nearby target 3-6 m from the baseline and background markers at least three times farther away.", "Provide a printed angular scale or require students to compute angle from lateral shift and background distance."],
        4: ["Provide three labeled data files or printed spectra: continuous, absorption-line, and emission-line examples.", "Provide a rest-wavelength table including H-alpha 656.3 nm, H-beta 486.1 nm, and at least one [O III] line.", "If using software, lock axes so students read wavelengths rather than pixel positions."],
        5: ["Provide telescope aperture, focal length, eyepiece focal length or camera pixel scale, and one sample image with a known field of view.", "If outdoors, complete a safety and setup check before students handle the instrument.", "If indoors, use a fixed sample image and instrument specification sheet."],
        6: ["Provide two planetary surface images at comparable scale, plus one icy-moon or Mars image for habitability evidence.", "Supply scale bars or state that only relative crater density may be inferred.", "Give students a counting grid or digital annotation layer."],
        7: ["Provide a CSV with columns for star ID, color or temperature, luminosity or absolute magnitude, and optional cluster membership.", "Provide plotting instructions for spreadsheet and Python users.", "Give one reference H-R diagram for comparison but require students to generate their own plot."],
        8: ["Provide a galaxy image set with source notes and a classification rubric.", "Provide a redshift-distance table with at least six galaxies, including one likely outlier.", "If spectra are used, provide rest and observed wavelengths for at least two lines."],
    }
    return setups[n]


def measurement_columns(lab: dict) -> list[str]:
    n = lab["n"]
    columns = {
        1: ["object", "time", "azimuth estimate", "altitude estimate", "uncertainty", "identification method"],
        2: ["target", "RA", "Dec", "time", "altitude", "azimuth", "observable?", "reason"],
        3: ["trial", "baseline", "apparent shift", "angle", "distance estimate", "uncertainty source"],
        4: ["spectrum", "line ID", "rest wavelength", "observed wavelength", "shift", "velocity", "interpretation"],
        5: ["instrument", "aperture", "focal length", "field of view", "image scale", "dominant observing limit"],
        6: ["image region", "area", "crater count", "surface features", "relative age", "uncertainty/caveat"],
        7: ["star or bin", "temperature/color", "luminosity/magnitude", "diagram region", "population", "evidence"],
        8: ["galaxy", "morphology", "criteria", "redshift or velocity", "distance", "classification caveat"],
    }
    return columns[n]


def measurement_table(columns: list[str]) -> str:
    header = "".join(f"<th>{escape(col)}</th>" for col in columns)
    cells = "".join("<td>&nbsp;</td>" for _ in columns)
    return f"<table><thead><tr>{header}</tr></thead><tbody><tr>{cells}</tr><tr>{cells}</tr><tr>{cells}</tr></tbody></table>"


def lab_html(lab: dict) -> str:
    body = f"""
<header><div><h1>Lab {lab['n']:02d}: {escape(lab['title'])}</h1><p>{escape(lab['subtitle'])}</p></div></header>
<main>
<section class="notice"><h2>Learning Objectives</h2>{html_list([lab['subtitle'], 'Make measurements or classifications with explicit uncertainty.', 'Separate direct evidence from model-dependent interpretation.'])}</section>
<section><h2>Preparation</h2>{html_list(lab['prep'])}</section>
<section><h2>Materials and Data</h2>{html_list(lab['materials'])}</section>
<section><h2>Apparatus and Setup</h2>{html_list(apparatus_setup(lab))}</section>
<section><h2>Procedure</h2>{html_list(lab['procedure'], 'ol')}</section>
<section><h2>Measurement Record</h2><p>Use this structure or an equivalent table in your lab notebook.</p>{measurement_table(measurement_columns(lab))}</section>
<section><h2>Analysis and Uncertainty</h2>{html_list(lab['analysis'])}</section>
<section><h2>Deliverables</h2>{html_list(lab['deliverables'])}</section>
<section><h2>Assessment Criteria</h2>{html_list(lab['assessment'])}</section>
<section><h2>References, Software, and Data Provenance</h2>{html_list(lab['references'])}<p>Any additional dataset, image, or software source used by an instructor should be added to <code>../reference-log.md</code> with source, access date, license or usage note, and processing steps.</p></section>
</main>"""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ASTR 101 Lab {lab['n']:02d}</title>
  <style>{CSS}</style>
</head>
<body>{body}</body>
</html>
"""


def update_review_report() -> None:
    text = REVIEW.read_text(encoding="utf-8") if REVIEW.exists() else "# ASTR 101 Course Materials Review Report\n"
    marker = "## Lab Second-Pass Correction"
    addition = f"""
{marker}

The CourseMaterialsReviewAgent identified the lab package as the remaining review-release blocker. The first lab pass reused generic procedures across all labs and did not provide concrete measurements, datasets, calculations, uncertainty treatment, or provenance.

Corrections applied:

- Rewrote all eight labs as concrete activities aligned to the schedule.
- Added lab-specific preparation, materials/data, step-by-step procedures, analysis/uncertainty tasks, deliverables, assessment criteria, and references/provenance notes.
- Added explicit source/provenance expectations for datasets, images, software, and observing resources.

Lab status: ready for reviewer evaluation.
"""
    if marker not in text:
        text = text.rstrip() + "\n\n" + addition.strip() + "\n"
    REVIEW.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for lab in LABS:
        (OUT / f"lab-{lab['n']:02d}.html").write_text(lab_html(lab), encoding="utf-8")
    update_review_report()


if __name__ == "__main__":
    main()
