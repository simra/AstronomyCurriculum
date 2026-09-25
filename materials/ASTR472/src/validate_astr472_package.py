"""Independent checks for ASTR 472 package completeness and worked values."""
from __future__ import annotations

import html
import json
import math
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
C = 299_792_458.0
K_B = 1.380649e-23
JY = 1e-26
F_HI = 1_420_405_751.77
ARCSEC_PER_RAD = 206264.806247


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.h1: list[str] = []
        self.current_h1 = False
        self.h1_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag.lower() in {"a", "link", "script", "img"}:
            target = values.get("href") or values.get("src")
            if target:
                self.links.append(target)
        if tag.lower() == "h1":
            self.current_h1 = True
            self.h1_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "h1" and self.current_h1:
            self.h1.append(" ".join(" ".join(self.h1_parts).split()))
            self.current_h1 = False

    def handle_data(self, data: str) -> None:
        if self.current_h1:
            self.h1_parts.append(data)


def read_h1(path: Path) -> str:
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    if not parser.h1:
        raise AssertionError(f"Missing h1: {path.relative_to(ROOT)}")
    return parser.h1[0]


def sig(value: float, digits: int = 4) -> str:
    if value == 0:
        return "0"
    places = digits - 1 - math.floor(math.log10(abs(value)))
    rounded = round(value, places)
    return f"{rounded:.{digits}g}"


def expected_results() -> dict[int, tuple[str, float, str]]:
    beam_25 = 1.02 * (C / 1.4e9) / 25 * ARCSEC_PER_RAD / 60
    area_25 = 0.70 * math.pi * 25**2 / 4
    sigma_mjy = 300 / math.sqrt(2 * 1e6 * 3600) * 1000
    wavelength = C / 1.4e9
    beam_rad = 45 / ARCSEC_PER_RAD
    omega = math.pi * beam_rad**2 / (4 * math.log(2))
    tb = wavelength**2 * JY / (2 * K_B * omega)
    phase_deg = -360 * (3000 / wavelength) * (10 / ARCSEC_PER_RAD)
    synth = 1.02 * (C / 100e9) / 16e3 * ARCSEC_PER_RAD
    largest = 0.6 * (C / 100e9) / 15 * ARCSEC_PER_RAD
    delay_ms = 4.148808 * 56.8 * (0.4**-2 - 1.4**-2)
    galactic_radius = 8.2 / (1 + 100 / (236 * math.sin(math.radians(30))))
    density = 1200 / (20 * 0.84)
    return {
        1: ("nu_c", 4.2e6 * 1e-5 * 1e4**2, "Hz"),
        2: ("FWHM", beam_25, "arcmin"),
        3: ("sigma_S", sigma_mjy, "mJy"),
        4: ("T_b", tb, "K"),
        5: ("fringe spacing", wavelength / 3000 * ARCSEC_PER_RAD, "arcsec"),
        6: ("synthesized FWHM scale", synth, "arcsec"),
        7: ("coherence", math.exp(-math.radians(10)**2 / 2), ""),
        8: ("sigma_S", 120 * math.sqrt(0.05**2 + 0.03**2 + 0.02**2), "mJy"),
        9: ("v_radio", C * 0.5e6 / F_HI / 1000, "km/s"),
        10: ("N_HI", 1.823e18 * 120 * 8, "cm^-2"),
        11: ("dispersion delay", delay_ms, "ms"),
        12: ("completeness", 0.84, ""),
        13: ("R_GC", galactic_radius, "kpc"),
        14: ("corrected surface density", density, "deg^-2"),
    }


def verify_result(path: Path, label: str, value: float, unit: str) -> None:
    text = path.read_text(encoding="utf-8")
    unit_pattern = re.escape(unit)
    match = re.search(re.escape(label) + r"\s*=\s*([-+0-9.eE]+)\s*" + unit_pattern, text)
    if not match:
        raise AssertionError(f"No rendered result {label} in {path.relative_to(ROOT)}")
    observed = float(match.group(1))
    if not math.isclose(observed, value, rel_tol=5e-4, abs_tol=1e-8):
        raise AssertionError(f"Independent result mismatch in {path.relative_to(ROOT)}: {observed} vs {value}")


def verify_required_files() -> None:
    fixed = ["syllabus.html", "schedule.html", "reference-log.md", "course-manifest.json", "README.md", "data/README.md", "review-report.md"]
    missing = [relative for relative in fixed if not (ROOT / relative).is_file()]
    expected = list(fixed)
    for number in range(1, 15):
        expected.extend([f"lectures/lecture-{number:02d}-slides.html", f"lectures/lecture-{number:02d}-notes.html"])
    for number in range(1, 8):
        expected.extend([
            f"labs/lab-{number:02d}.html",
            f"problem-sets/problem-set-{number:02d}.html",
            f"problem-sets/problem-set-{number:02d}-solutions.html",
            f"problem-sets/problem-set-{number:02d}-assessment.md",
        ])
    if (ROOT / "index.html").exists():
        expected.append("index.html")
    missing.extend(relative for relative in expected if not (ROOT / relative).is_file())
    if missing:
        raise AssertionError("Missing required files: " + ", ".join(sorted(set(missing))))
    manifest = json.loads((ROOT / "course-manifest.json").read_text(encoding="utf-8"))
    counts = manifest["counts"]
    assert counts == {"slides": 14, "notes": 14, "labs": 7, "problemSets": 7, "solutionKeys": 7, "assessmentInstructions": 7}
    for path in ROOT.rglob("*.html"):
        content = path.read_text(encoding="utf-8")
        if not content.lower().lstrip().startswith("<!doctype html>"):
            raise AssertionError(f"Missing HTML doctype: {path.relative_to(ROOT)}")


def verify_links() -> None:
    for page_path in list(ROOT.rglob("*.html")) + [REPO / "astronomy_curriculum.html"]:
        parser = LinkParser()
        parser.feed(page_path.read_text(encoding="utf-8"))
        for target in parser.links:
            parsed = urlparse(target)
            if parsed.scheme or target.startswith("#"):
                continue
            path_part = unquote(parsed.path)
            if not path_part:
                continue
            target_path = (page_path.parent / path_part).resolve()
            if target_path.is_dir():
                target_path = target_path / "index.html"
            if target_path == ROOT / "index.html" and not target_path.exists():
                continue
            if not target_path.exists():
                raise AssertionError(f"Broken local link in {page_path}: {target}")


def verify_lecture_examples_and_figures() -> None:
    geometries: set[str] = set()
    for number, (label, value, unit) in expected_results().items():
        lecture = ROOT / f"lectures/lecture-{number:02d}-notes.html"
        verify_result(lecture, label, value, unit)
        slides = (ROOT / f"lectures/lecture-{number:02d}-slides.html").read_text(encoding="utf-8")
        found = re.findall(r"<svg\b.*?</svg>", slides, flags=re.DOTALL)
        if len(found) != 1:
            raise AssertionError(f"Expected one visual-reasoning SVG in lecture {number:02d}; found {len(found)}")
        geometry = re.sub(r"<text\b.*?</text>", "", found[0], flags=re.DOTALL)
        geometry = re.sub(r'aria-label="[^"]*"', "", geometry)
        if geometry in geometries:
            raise AssertionError(f"Repeated lecture diagram geometry at lecture {number:02d}")
        geometries.add(geometry)
    if len(geometries) != 14:
        raise AssertionError("Lecture figure geometry is not unique across all 14 decks")


def verify_assignments() -> None:
    for number in range(1, 8):
        student = ROOT / f"problem-sets/problem-set-{number:02d}.html"
        solutions = ROOT / f"problem-sets/problem-set-{number:02d}-solutions.html"
        assessment = ROOT / f"problem-sets/problem-set-{number:02d}-assessment.md"
        student_text = student.read_text(encoding="utf-8")
        solution_text = solutions.read_text(encoding="utf-8")
        assert student_text.count("<article class=\"problem\">") == 3
        assert solution_text.count("<article class=\"problem\">") == 3
        assert solution_text.count("Worked solution:") == 3
        assert "Problem-specific checks" in assessment.read_text(encoding="utf-8")
    assert "Chapter 5 Figuring for Yourself 41" in (ROOT / "problem-sets/problem-set-01.html").read_text(encoding="utf-8")
    assert "Chapter 23 Figuring for Yourself 42-43" in (ROOT / "problem-sets/problem-set-06.html").read_text(encoding="utf-8")
    assert "Review Question 5" in (ROOT / "problem-sets/problem-set-07.html").read_text(encoding="utf-8")
    gaussian_solution = (ROOT / "problem-sets/problem-set-05-solutions.html").read_text(encoding="utf-8")
    assert "rectangle overestimates relative to Gaussian" not in gaussian_solution
    assert "% lower" in (ROOT / "problem-sets/problem-set-05-solutions.html").read_text(encoding="utf-8")


def verify_index_titles() -> None:
    index_path = ROOT / "index.html"
    if not index_path.exists():
        print("Index not yet assembled; title check deferred to final assembly.")
        return
    index = LinkParser()
    index.feed(index_path.read_text(encoding="utf-8"))
    content = index_path.read_text(encoding="utf-8")
    for number in range(1, 15):
        expected = read_h1(ROOT / f"lectures/lecture-{number:02d}-slides.html")
        if html.escape(expected) not in content:
            raise AssertionError(f"Index title mismatch for lecture {number:02d}: {expected}")
    for number in range(1, 8):
        for folder, filename in [("labs", f"lab-{number:02d}.html"), ("problem-sets", f"problem-set-{number:02d}.html")]:
            expected = read_h1(ROOT / folder / filename)
            if html.escape(expected) not in content:
                raise AssertionError(f"Index title mismatch for {filename}: {expected}")


def main() -> None:
    verify_required_files()
    verify_links()
    verify_lecture_examples_and_figures()
    verify_assignments()
    verify_index_titles()
    print("ASTR 472 independent validation passed: files/counts, HTML/local links, 14 lecture calculations, 14 unique SVG geometries, assignment/solution sets, and index-title agreement where assembled.")


if __name__ == "__main__":
    main()