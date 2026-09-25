"""Validate completeness and internal consistency of the ASTR 476 package."""
from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []
        self.anchors: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.headings: list[str] = []
        self._anchor: tuple[str, list[str]] | None = None
        self._heading: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(str(attributes["id"]))
        if tag == "a" and attributes.get("href"):
            href = str(attributes["href"])
            self.hrefs.append(href)
            self._anchor = (href, [])
        if tag == "h1":
            self._heading = []

    def handle_data(self, data: str) -> None:
        if self._anchor is not None:
            self._anchor[1].append(data)
        if self._heading is not None:
            self._heading.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._anchor is not None:
            self.anchors.append((self._anchor[0], "".join(self._anchor[1]).strip()))
            self._anchor = None
        if tag == "h1" and self._heading is not None:
            self.headings.append("".join(self._heading).strip())
            self._heading = None


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    text = path.read_text(encoding="utf-8")
    if not text.lstrip().lower().startswith("<!doctype html>"):
        raise AssertionError(f"Missing HTML5 doctype: {path.relative_to(ROOT)}")
    parser.feed(text)
    return parser


def h1(path: Path) -> str:
    headings = parse_page(path).headings
    if not headings:
        raise AssertionError(f"No h1 in {path.relative_to(ROOT)}")
    return headings[0]


def verify_links() -> int:
    count = 0
    for path in ROOT.rglob("*.html"):
        parsed_page = parse_page(path)
        for href in parsed_page.hrefs:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                raise AssertionError(f"Broken local link in {path.relative_to(ROOT)}: {href}")
            if parsed.fragment and target.suffix.lower() in {".html", ".htm"}:
                if unquote(parsed.fragment) not in parse_page(target).ids:
                    raise AssertionError(f"Broken local fragment in {path.relative_to(ROOT)}: {href}")
            count += 1
    return count


def verify_diagrams() -> int:
    signatures: set[str] = set()
    for path in sorted((ROOT / "lectures").glob("lecture-*-slides.html")):
        text = path.read_text(encoding="utf-8")
        matches = re.findall(r"<svg\b.*?</svg>", text, flags=re.DOTALL)
        if len(matches) != 1:
            raise AssertionError(f"Expected exactly one SVG in {path.name}, found {len(matches)}")
        signature = re.sub(r"<(?:title|desc|text)\b.*?</(?:title|desc|text)>", "", matches[0], flags=re.DOTALL)
        signature = re.sub(r"\s(?:fill|stroke|class|role|aria-[\w-]+|id)=(?:'[^']*'|\"[^\"]*\")", "", signature)
        signature = re.sub(r"\s+", " ", signature).strip()
        signatures.add(signature)
    if len(signatures) != 14:
        raise AssertionError(f"Expected 14 structurally unique lecture SVGs; found {len(signatures)}")
    return len(signatures)


def verify_data() -> dict[str, object]:
    with (ROOT / "data" / "pantheonplus-subset.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(__import__("csv").DictReader(stream))
    covariance = np.loadtxt(ROOT / "data" / "pantheonplus-subset-covariance.csv", delimiter=",")
    if len(rows) != 18 or covariance.shape != (18, 18):
        raise AssertionError("Pantheon+ excerpt row/covariance dimensions do not match 18x18")
    if len({row["CID"] for row in rows}) != len(rows):
        raise AssertionError("Pantheon+ excerpt contains duplicate CIDs")
    if not np.all(np.isfinite(covariance)) or not np.allclose(covariance, covariance.T, atol=1e-11, rtol=0):
        raise AssertionError("Pantheon+ excerpt covariance is non-finite or asymmetric")
    np.linalg.cholesky(covariance)
    provenance = json.loads((ROOT / "data" / "pantheonplus-subset-provenance.json").read_text(encoding="utf-8"))
    if provenance["provenanceLevel"] != 1 or provenance["sourceRows"] != 1701:
        raise AssertionError("Pantheon+ source provenance or source row count is invalid")
    for key in ("sourceDataSha256", "sourceCovarianceSha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", provenance[key]):
            raise AssertionError(f"Invalid SHA-256 digest in provenance: {key}")
    if "not a representative random sample" not in provenance["limitations"]:
        raise AssertionError("Pantheon+ excerpt limitations are missing")
    return {"excerptRows": len(rows), "covarianceShape": list(covariance.shape),
            "minimumEigenvalue": float(np.linalg.eigvalsh(covariance).min())}


def validate() -> dict[str, object]:
    required = ["syllabus.html", "schedule.html", "reference-log.md", "course-manifest.json",
                "index.html", "review-report.md", "data/README.md"]
    missing = [name for name in required if not (ROOT / name).is_file()]
    for number in range(1, 15):
        missing.extend(name for name in (f"lectures/lecture-{number:02d}-slides.html",
                                         f"lectures/lecture-{number:02d}-notes.html")
                       if not (ROOT / name).is_file())
    for number in range(1, 8):
        missing.extend(name for name in (f"labs/lab-{number:02d}.html",
                                         f"problem-sets/problem-set-{number:02d}.html",
                                         f"problem-sets/problem-set-{number:02d}-solutions.html",
                                         f"problem-sets/problem-set-{number:02d}-assessment.md")
                       if not (ROOT / name).is_file())
    if missing:
        raise AssertionError(f"Required package files missing: {missing}")

    json_files = list(ROOT.rglob("*.json"))
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "course-manifest.json").read_text(encoding="utf-8"))
    curriculum = json.loads((REPO_ROOT / "astronomy_curriculum.json").read_text(encoding="utf-8"))
    catalog_course = next(course for course in curriculum["courses"] if course["courseNumber"] == "ASTR 476")
    if manifest["course"]["prerequisites"] != catalog_course["prerequisites"]:
        raise AssertionError("ASTR476 manifest prerequisites disagree with astronomy_curriculum.json")
    if "ASTR 420 or concurrent enrollment" not in (ROOT / "syllabus.html").read_text(encoding="utf-8"):
        raise AssertionError("ASTR476 syllabus prerequisites disagree with the catalog")
    expected = {"slides": 14, "notes": 14, "labs": 7, "problemSets": 7,
                "solutionKeys": 7, "assessmentInstructions": 7}
    if manifest["counts"] != expected:
        raise AssertionError(f"Manifest counts differ from expected {expected}: {manifest['counts']}")
    for pattern, wanted in (("lectures/lecture-*-slides.html", 14), ("lectures/lecture-*-notes.html", 14),
                            ("labs/lab-*.html", 7), ("problem-sets/problem-set-*.html", 14),
                            ("problem-sets/problem-set-*-assessment.md", 7)):
        actual = len(list(ROOT.glob(pattern)))
        if actual != wanted:
            raise AssertionError(f"{pattern}: expected {wanted}, found {actual}")

    index_parser = parse_page(ROOT / "index.html")
    index_links = dict(index_parser.anchors)
    for number in range(1, 15):
        title = h1(ROOT / "lectures" / f"lecture-{number:02d}-slides.html")
        slide_href = f"lectures/lecture-{number:02d}-slides.html"
        notes_href = f"lectures/lecture-{number:02d}-notes.html"
        if title not in index_links.get(slide_href, "") or title not in index_links.get(notes_href, ""):
            raise AssertionError(f"Index labels do not match lecture {number:02d} h1")
    calendar = (REPO_ROOT / "astronomy_curriculum.html").read_text(encoding="utf-8")
    if calendar.count("materials/ASTR476/index.html") != 2:
        raise AssertionError("ASTR476 materials link must occur in the calendar card and elective schedule slot")
    if "option: <a href=\"materials/ASTR476/index.html\">ASTR 476 Observational Cosmology</a>" not in calendar:
        raise AssertionError("ASTR476 is not linked from the Year 4 advanced-elective schedule slot")
    if not (REPO_ROOT / "materials/ASTR476/index.html").is_file():
        raise AssertionError("ASTR476 calendar link target is missing")

    schedule = parse_page(ROOT / "schedule.html")
    schedule_text = (ROOT / "schedule.html").read_text(encoding="utf-8")
    if len(re.findall(r"<tr><td>\d+</td><td>Lecture \d{2}:", schedule_text)) != 14:
        raise AssertionError("Schedule must map all 14 weekly lectures")
    for due_week in (2, 4, 6, 8, 10, 12, 14):
        expected_lab = f"Lab {(due_week+1)//2:02d}; Problem Set {(due_week+1)//2:02d}"
        if expected_lab not in schedule_text:
            raise AssertionError(f"Missing paired assessment due in Week {due_week}")
    if "paired" not in schedule_text.lower() or "not a one-to-one" not in (ROOT / "syllabus.html").read_text(encoding="utf-8").lower():
        raise AssertionError("Non-1:1 assessment cadence rationale is not explicit")

    references = (ROOT / "reference-log.md").read_text(encoding="utf-8")
    for exact_title in (
        "The clustering of galaxies in the completed SDSS-III Baryon Oscillation Spectroscopic Survey: cosmological analysis of the DR12 galaxy sample",
        "Dark Energy Survey Year 3 results: Cosmological constraints from galaxy clustering and weak lensing",
    ):
        if exact_title not in references:
            raise AssertionError(f"Reference log lacks exact published paper title: {exact_title}")
    for level in ("Level 1", "Level 2", "Level 3"):
        if level not in references:
            raise AssertionError(f"Reference log is missing {level} provenance labels")
    if "HTTP 401" not in references or "extraction failure" not in references:
        raise AssertionError("Planck archive access limitation is not documented")
    data_validation = verify_data()
    from astr476_computations import self_test
    calculations = self_test()
    links = verify_links()
    diagrams = verify_diagrams()
    return {"htmlPages": len(list(ROOT.rglob("*.html"))), "jsonFiles": len(json_files),
            "localLinks": links, "uniqueLectureDiagrams": diagrams,
            "artifactCounts": expected, "data": data_validation,
            "calculationSelfTest": calculations, "curriculumLink": "materials/ASTR476/index.html"}


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2, sort_keys=True))