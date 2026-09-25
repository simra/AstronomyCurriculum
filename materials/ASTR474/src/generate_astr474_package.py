"""Build the ASTR 474 Computational Astrophysics course package."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODE = "ASTR474"
TITLE = "Computational Astrophysics"
TODAY = "2026-09-25"

LECTURES = [
    ("Computational Experiments and Floating-Point Arithmetic", "conditioning, precision, units, verification"),
    ("Initial-Value Problems and Error Control", "local/global error, adaptive integration, convergence"),
    ("Kepler Orbits with REBOUND", "two-body benchmarks, symplectic maps, timestep error"),
    ("N-Body Systems, Invariants, and Close Encounters", "many-body dynamics, conservation, chaos, regularization"),
    ("Conservation Laws and Hydrodynamics Concepts", "Euler equations, fluxes, shocks, conservation"),
    ("Finite-Volume Resolution and Shock Tests", "Riemann problems, numerical diffusion, resolution studies"),
    ("Radiative Transfer as a Numerical Problem", "formal solution, optical depth, boundary conditions"),
    ("Radiative-Transfer Approximations and Validation", "escape probabilities, discretization, error budgets"),
    ("Monte Carlo Transport and Random Walks", "sampling, estimators, variance, random seeds"),
    ("Monte Carlo Radiation and Rare Events", "importance sampling, effective sample size, confidence"),
    ("Likelihoods, Residuals, and Parameter Estimation", "weighted fits, likelihood, identifiability, residual checks"),
    ("Bayesian Inference for Astrophysical Models", "priors, posterior sampling, uncertainty, model criticism"),
    ("Reproducible Simulation Workflows", "environments, provenance, testing, scaling, archival"),
    ("Computational Astrophysics Research Synthesis", "end-to-end simulation, convergence evidence, peer audit"),
]

WEEK_FOCI = [
    "Floating-point arithmetic and conditioning",
    "Initial-value problems and error control",
    "Kepler orbits and ephemeris validation",
    "N-body dynamics and close encounters",
    "Euler conservation laws and hydrodynamics",
    "Finite-volume resolution and shock tests",
    "Radiative transfer and optical depth",
    "Radiative-transfer approximations and validation",
    "Monte Carlo transport and random walks",
    "Importance sampling and rare events",
    "Likelihoods, residuals, and parameter estimation",
    "Bayesian inference and posterior uncertainty",
    "Reproducible simulation workflows",
    "Computational research synthesis",
]

WEEK_ASSESSMENTS = {
    2: "Lab 01; Problem Set 01",
    3: "Lab 02; Problem Set 02",
    4: "Lab 03; Problem Set 03",
    6: "Lab 04; Problem Set 04",
    8: "Lab 05; Problem Set 05",
    12: "Lab 06; Problem Set 06",
    14: "Lab 07; Problem Set 07",
}

CSS = """
:root{--ink:#17202a;--muted:#596875;--paper:#fbfcfd;--panel:#fff;--line:#d9e0e7;--navy:#102a43;--teal:#0f6b78;--teal-soft:#e5f4f6;--gold:#b87911;--warning:#8a4b08}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--paper);font:16px/1.6 Georgia,'Times New Roman',serif}
header{padding:32px 24px;background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}header>div,main{max-width:1120px;margin:auto}main{padding:28px 24px 64px}
h1,h2,h3{line-height:1.2}h1{margin:0 0 8px;font-size:2.4rem}h2{margin-top:32px;padding-bottom:8px;border-bottom:2px solid var(--line);color:var(--navy)}h3{color:var(--teal)}
section{margin:18px 0;padding:16px 18px;border:1px solid var(--line);border-radius:5px;background:var(--panel)}
a{color:var(--teal);font-weight:700}table{width:100%;border-collapse:collapse;margin:14px 0}th,td{padding:8px 10px;border:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--teal-soft)}.notice{border-left:5px solid var(--gold);padding:12px 16px;background:#fff6e6}.meta{color:var(--muted);font-size:.94rem}
"""


def page(title: str, body: str) -> str:
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>")


def shell(title: str, subtitle: str, content: str) -> str:
    return (f"<header><div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div></header>"
            f"<main>{content}</main>")


def build_plan() -> None:
    for folder in ("lectures", "labs", "problem-sets", "data", "src"):
        (ROOT / folder).mkdir(parents=True, exist_ok=True)

    schedule_rows = "".join(
        f"<tr><td>{week}</td><td>Lecture {week:02d}: {html.escape(LECTURES[week - 1][0])}</td>"
        f"<td>{html.escape(WEEK_FOCI[week - 1])}</td>"
        f"<td>{WEEK_ASSESSMENTS.get(week, 'No lab or problem set due')}</td></tr>"
        for week in range(1, 15)
    )
    lecture_rows = "".join(
        f"<tr><td>{n:02d}</td><td>{html.escape(title)}</td><td>{html.escape(scope)}</td></tr>"
        for n, (title, scope) in enumerate(LECTURES, 1)
    )
    syllabus_body = f"""
<h2>Course Information</h2><section>
<p><strong>ASTR 474: Computational Astrophysics</strong> · 3 credits · Year 4 elective · 14-week semester</p>
<p><strong>Catalog description:</strong> Applies numerical methods to astronomical problems including N-body integration, hydrodynamics concepts, radiative transfer approximations, Monte Carlo methods, parameter estimation, and reproducible simulation workflows.</p>
<p><strong>Prerequisites:</strong> COMP 260; ASTR 310; MATH 255.</p>
<p>Assumption: two 75-minute meetings weekly. Each numbered lecture is a weekly topic module taught across those two meetings; it is not a single 75-minute meeting. Computing labs are two hours and are scheduled only after their mapped modules are complete. Confirm local dates, instructor, office hours, accommodations, and institutional policies before instructional use.</p></section>
<h2>Learning Outcomes</h2><section><ol>
<li>Choose a numerical method suited to an astrophysical initial- or boundary-value problem and state its assumptions and stability limits.</li>
<li>Use NumPy, SciPy, Astropy, and REBOUND for array computation, units, fitting/integration, and orbital dynamics without misrepresenting educational code as research-grade software.</li>
<li>Validate calculations using analytic limits, dimensional checks, timestep/resolution convergence, conservation diagnostics, and independent implementations.</li>
<li>Quantify stochastic and fitted-parameter uncertainty, inspect residuals, and distinguish numerical error from model inadequacy.</li>
<li>Build reproducible workflows that record software versions, inputs, random seeds, provenance, tests, and run instructions.</li>
<li>Communicate a computational result with a defensible error budget, limitations, and machine-readable evidence.</li>
</ol></section>
<h2>Resources and Computing</h2><section>
<p>Required software is pinned in <a href='requirements.txt'>requirements.txt</a>: CPython 3.14.6, NumPy 2.5.3, SciPy 1.18.1, Astropy 8.0.1, and REBOUND 5.2.0. The package uses libraries for their actual scientific roles; short hand-built schemes are labeled as teaching demonstrations, not production solvers.</p>
<p>Students need a computer able to run the supplied scripts. All listed experiments run on a CPU; no GPU, observatory account, or paid service is assumed. Each activity includes a reproducible command and a validation target.</p></section>
<h2>Assessment</h2><section><table><thead><tr><th>Component</th><th>Weight</th><th>Evidence</th></tr></thead><tbody>
<tr><td>Seven computational labs</td><td>28%</td><td>Runnable analysis, convergence or uncertainty evidence, and concise technical reports</td></tr>
<tr><td>Seven problem sets</td><td>28%</td><td>Derivations, computational reasoning, validation, and interpretation</td></tr>
<tr><td>Code reviews and reproducibility checks</td><td>14%</td><td>Tests, environment capture, provenance, and review of failure modes</td></tr>
<tr><td>Midterm computational audit</td><td>10%</td><td>Independent recomputation, error diagnosis, and numerical-method choice</td></tr>
<tr><td>Final mini-project</td><td>20%</td><td>Reproducible astrophysical computation, validation dossier, and written interpretation</td></tr>
<tr><th>Total</th><th>100%</th><th></th></tr></tbody></table>
<p>Mastery grading rewards correct reasoning, validated results, physical interpretation, uncertainty analysis, and reproducibility. Revisions and resubmissions are encouraged to improve mastery and grade; instructors return actionable feedback and preserve the stated standards.</p></section>
<h2>Cadence and Course Policies</h2><section><p>The fourteen numbered lecture modules each occupy one calendar week and include both 75-minute meetings that week. Seven labs and seven problem sets are intentionally non-uniformly spaced: Labs/PS 01 cover Weeks 1-2; 02 covers Week 3; 03 covers Week 4; 04 covers Weeks 5-6; 05 covers Weeks 7-8; 06 covers Weeks 9-12; and 07 covers Weeks 13-14. Each assessment is due only after its listed lecture span, avoiding one coding deliverable per module while allowing longer computational investigations where the method requires it. The week-by-week mapping and project milestones are in <a href='schedule.html'>schedule.html</a>.</p>
<p>Students may discuss concepts and debug in pairs, but submitted code, explanations, and analysis must be attributable. Cite software, data, and adapted code. Do not report a numerical result without the input, method, units, validation, and uncertainty relevant to the claim. Institutional accessibility, late-work, academic-integrity, and safety policies supersede these placeholders.</p></section>
<p class='meta'>Course specification last updated {TODAY}. Instructor and institution-specific fields remain to be completed.</p>
"""
    (ROOT / "syllabus.html").write_text(page("ASTR 474 Syllabus", shell("ASTR 474: Computational Astrophysics", "3 credits · Year 4 elective", syllabus_body)), encoding="utf-8")

    schedule_body = f"""
<p>Each numbered lecture is a weekly module taught across two 75-minute meetings. Labs and problem sets follow the completed lecture span shown in the calendar. Weeks are placeholders; replace dates to match the local academic calendar.</p>
<table><thead><tr><th>Week</th><th>Lecture sequence</th><th>Unit focus</th><th>Lab and assessment</th></tr></thead><tbody>{schedule_rows}</tbody></table>
<h2>Lecture Scope</h2><table><thead><tr><th>No.</th><th>Lecture</th><th>Methods and checks</th></tr></thead><tbody>{lecture_rows}</tbody></table>
<h2>Assessment Milestones</h2><section><p>Labs and Problem Sets 01-07 are due at the close of Weeks 2, 3, 4, 6, 8, 12, and 14 respectively, after their mapped lecture content. The midterm computational audit follows Week 7. Final mini-project proposal is due Week 10, reproducibility checkpoint Week 13, and validated report/code bundle Week 14.</p></section>
"""
    (ROOT / "schedule.html").write_text(page("ASTR 474 Schedule", shell("ASTR 474 Lecture and Lab Schedule", "14 lectures · 7 computational labs · 7 problem sets", schedule_body)), encoding="utf-8")

    (ROOT / "data" / "README.md").write_text(
        "# ASTR 474 Data\n\n`generated/jpl_earth_vectors.csv` contains two Earth-center state vectors embedded in `src/astr474_computations.py` and attributed to NASA/JPL Horizons DE441. Provenance is level 2: the source response was not retrieved in this session. `generated/jpl_earth_request.json` records target 399, Sun center 500@10, requested TDB epochs (2025-01-01 and 2025-01-02), J2000 ecliptic reference system/plane, vector table 2, geometric correction NONE, AU and AU/day units, the encoded request URL, and the 2026-09-25 HTTP 404 access-attempt result. This trace is not a raw Horizons response. The vector CSV SHA-256 is recorded in the request trace and `generated/SHA256SUMS`.\n\nAll other generated numerical experiments are level-3 synthetic teaching data. Their inputs, algorithms, and random seeds are in `src/astr474_computations.py`; none is an observation. Astropy solar/Earth/Jupiter constants are standard published values supplied by the pinned Astropy release (level 2; see `reference-log.md`).\n",
        encoding="utf-8")
    (ROOT / "src" / "README.md").write_text(
        "# ASTR 474 Source\n\nUse CPython 3.14.6 and the exact pins in `../requirements.txt`. From the repository root, create a clean environment with `py -3.14 -m venv .venv` and install the pins with `.venv/Scripts/python.exe -m pip install -r materials/ASTR474/requirements.txt` (POSIX: `.venv/bin/python -m pip install -r materials/ASTR474/requirements.txt`). Then run `.venv/Scripts/python.exe materials/ASTR474/src/generate_astr474_package.py --stage all` on Windows or `.venv/bin/python materials/ASTR474/src/generate_astr474_package.py --stage all` on POSIX. This command rebuilds the plan, numerical datasets, lecture/lab/problem-set artifacts, title-derived course index, SHA-256 manifest, and runs the package validator. To verify recorded file digests without rebuilding, run `.venv/Scripts/python.exe materials/ASTR474/src/validate_astr474_package.py --verify-checksums` (or the POSIX interpreter path). The validator recomputes shared numerical results and checks counts, local HTML links, lecture titles, unique lecture diagrams, and generated checksums.\n",
        encoding="utf-8")

    manifest = {
        "course": {"courseNumber": "ASTR 474", "courseCode": CODE, "title": TITLE, "credits": 3,
                   "term": "Year 4 elective", "yearInCurriculum": 4,
                   "prerequisites": "COMP 260; ASTR 310; MATH 255",
                   "description": "Applies numerical methods to astronomical problems including N-body integration, hydrodynamics concepts, radiative transfer approximations, Monte Carlo methods, parameter estimation, and reproducible simulation workflows."},
        "status": {"stage": "in production", "reviewStatus": "Not yet reviewed", "lastUpdated": TODAY},
        "counts": {"slides": 14, "notes": 14, "labs": 7, "problemSets": 7, "solutionKeys": 7, "assessmentInstructions": 7},
        "cadence": {"lectures": 14, "labs": 7, "problemSets": 7,
                "rationale": "Each numbered lecture is a weekly module taught across two 75-minute meetings. Labs/problem sets cover lecture spans 01-02, 03, 04, 05-06, 07-08, 09-12, and 13-14 and are due in weeks 2, 3, 4, 6, 8, 12, and 14 after the mapped content."},
        "environment": {"python": "3.14.6", "requirements": "requirements.txt"},
        "dataProvenance": {"generator": "materials/ASTR474/src/generate_astr474_package.py", "levels": {
            "level1": "No course dataset was successfully fetched or verified from a primary source during the 2026-09-25 correction session.",
            "level2": "Embedded JPL Horizons DE441 vectors and Astropy-distributed astronomical constants; sources and verification limits are itemized in reference-log.md and data/generated/jpl_earth_request.json.",
            "level3": "Synthetic instructor-generated numerical experiments; never presented as observations; seeds and algorithms are recorded in the computation source."}},
    }
    (ROOT / "course-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    references = """# ASTR 474 Reference and Provenance Log

## Provenance levels

- Level 1: fetched or extracted from an authoritative source during this session. None of the course datasets reached this level; the JPL API request returned HTTP 404 on 2026-09-25.
- Level 2: standard published/literature data or package-supplied constants not independently re-verified this session; human spot-check required before instructional use.
- Level 3: synthetic/instructor-generated numerical experiments, not observations.

## Dataset and constants records

- Level 2, `data/generated/jpl_earth_vectors.csv`: Earth center (target 399) relative to Sun center (500@10); requested epochs 2025-01-01 and 2025-01-02 00:00 TDB; J2000 reference system and ecliptic plane; state vectors, table 2; geometric correction `NONE`; position in AU and velocity in AU/day. The complete API parameters, encoded request URL, access-attempt date/result, and vector CSV SHA-256 are in `data/generated/jpl_earth_request.json`; the CSV digest is also in `data/generated/SHA256SUMS`. The endpoint returned HTTP 404, so the stored values are attributed to DE441 but were not freshly verified; no raw response is claimed. Sources: [JPL Horizons API](https://ssd-api.jpl.nasa.gov/api/horizons.api) and [API documentation](https://ssd-api.jpl.nasa.gov/doc/horizons.html). Human spot-check required.
- Level 2, Astropy constants: `GM_sun`, `M_sun`, `M_earth`, `GM_jup`, and `R_earth`, as supplied by pinned Astropy 8.0.1. Values were not independently re-verified this session. Source: [Astropy constants documentation](https://docs.astropy.org/en/stable/constants/).
- Level 3, `data/generated/computed_results.json`, `rebound_convergence.csv`, `nbody_conservation.csv`, `hydro_resolution.csv`, `hydro_profile_128.csv`, `monte_carlo_trials.csv`, and `radial_velocity_observations.csv`: deterministic or seeded teaching outputs generated by `src/astr474_computations.py`. The Sod tube uses dimensionless synthetic initial data; Monte Carlo base seed is 47409 (offset seeds are explicit in source); radial-velocity records are synthetic, not observed. Files and checksums are listed in `data/generated/SHA256SUMS`.

## Software and methods

- NumPy 2.5.3: array and random Generator APIs; https://numpy.org/doc/2.5/.
- SciPy 1.18.1: `solve_ivp`, `brentq`, and `least_squares`; https://docs.scipy.org/doc/scipy/.
- Astropy 8.0.1: units and constants; https://docs.astropy.org/en/stable/.
- REBOUND 5.2.0: WHFast and IAS15; https://rebound.hanno-rein.de/ and Rein & Liu (2012), A&A 537, A128, https://doi.org/10.1051/0004-6361/201118085.

Package versions were recorded from the configured CPython 3.14.6 environment on 2026-09-25. Documentation URLs are authoritative references but were not all independently fetched during the correction session. Exact dependency pins are in `requirements.txt`.
"""
    (ROOT / "reference-log.md").write_text(references, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("plan", "all"), default="plan")
    args = parser.parse_args()
    if args.stage in {"plan", "all"}:
        build_plan()
    if args.stage == "all":
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
        from materials.ASTR474.src.astr474_computations import generate_outputs
        from materials.ASTR474.src.build_astr474_materials import build_all
        from materials.ASTR474.src.validate_astr474_package import validate_package

        generate_outputs()
        build_all()
        validation = validate_package()
        print(f"{CODE} clean build and validation passed: {json.dumps(validation, sort_keys=True)}")
    else:
        print(f"{CODE} plan generated: 14 lectures, 7 labs, 7 problem sets")


if __name__ == "__main__":
    main()