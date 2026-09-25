"""Validate and assemble the ASTR 474 course package."""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import numpy as np

COURSE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
GENERATED = COURSE_ROOT / "data" / "generated"
CHECKSUM_FILE = GENERATED / "SHA256SUMS"
sys.path.insert(0, str(REPO_ROOT))

from materials.ASTR474.src.astr474_computations import compute_results


class ArtifactParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.hrefs: list[str] = []
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
            self.links.append((self._anchor[0], "".join(self._anchor[1]).strip()))
            self._anchor = None
        if tag == "h1" and self._heading is not None:
            self.headings.append("".join(self._heading).strip())
            self._heading = None


def parse_html(path: Path) -> ArtifactParser:
    parser = ArtifactParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def title_from(path: Path) -> str:
    headings = parse_html(path).headings
    if not headings:
        raise AssertionError(f"No h1 title found in {path.relative_to(COURSE_ROOT)}")
    return headings[0]


def title_without_number(title: str, prefix: str, number: int) -> str:
    return re.sub(rf"^{re.escape(prefix)}\s*{number:02d}:?\s*", "", title).strip()


def build_index() -> None:
    template = (REPO_ROOT / "templates" / "course-materials" / "course-index.template.html").read_text(encoding="utf-8")
    manifest = json.loads((COURSE_ROOT / "course-manifest.json").read_text(encoding="utf-8"))
    course = manifest["course"]
    status = manifest["status"]
    replacements = {
        "{{COURSE_CODE}}": course["courseCode"],
        "{{COURSE_TITLE}}": course["title"],
        "{{CREDITS}}": str(course["credits"]),
        "{{TERM_OR_SEQUENCE}}": course["term"],
        "{{PACKAGE_STATUS}}": f"{status['stage']} · {status['reviewStatus']}",
        "{{COURSE_DESCRIPTION}}": course["description"],
        "{{LAST_UPDATED}}": status["lastUpdated"],
        "{{SYLLABUS_STATUS}}": "Generated course specification; local policies remain to be completed.",
        "{{SCHEDULE_STATUS}}": "Fourteen-week schedule with mapped labs and problem sets.",
        "{{REFERENCE_LOG_STATUS}}": "Per-dataset provenance levels and source records included.",
        "{{LECTURE_01_TITLE}}": title_without_number(title_from(COURSE_ROOT / "lectures" / "lecture-01-slides.html"), "Lecture", 1),
        "{{LECTURE_01_STATUS}}": "Slides and notes generated",
        "{{LAB_01_STATUS}}": "Generated",
        "{{PROBLEM_SET_01_STATUS}}": "Assignment, solutions, and assessment instructions generated",
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    review_report = COURSE_ROOT / "review-report.md"
    review_link = ('<p class="meta">Review report: <a href="review-report.md">review-report.md</a></p>'
                   if review_report.exists() else '<p class="meta">Review report: pending reviewer verdict.</p>')
    template = template.replace("{{REVIEW_REPORT_LINK}}", review_link)

    def replace_section_list(document: str, heading: str, items: list[str]) -> str:
        pattern = rf"(<h2>{re.escape(heading)}</h2>.*?<ul>).*?(</ul>)"
        replacement = r"\1" + "\n" + "\n".join(items) + r"\2"
        result, count = re.subn(pattern, replacement, document, count=1, flags=re.DOTALL)
        if count != 1:
            raise AssertionError(f"Could not assemble {heading} list from the course index template")
        return result

    lecture_items = []
    for number in range(1, 15):
        slide_path = COURSE_ROOT / "lectures" / f"lecture-{number:02d}-slides.html"
        notes_path = COURSE_ROOT / "lectures" / f"lecture-{number:02d}-notes.html"
        title = title_from(slide_path)
        expected_prefix = f"Lecture {number:02d}:"
        if not title.startswith(expected_prefix):
            raise AssertionError(f"Slide h1 does not begin with its lecture number: {slide_path.name}: {title}")
        label = title
        lecture_items.append(
            f'<li><a href="lectures/lecture-{number:02d}-slides.html">{label} &mdash; slides</a> · '
            f'<a href="lectures/lecture-{number:02d}-notes.html">{label} &mdash; notes</a></li>')
    lab_items = []
    for number in range(1, 8):
        path = COURSE_ROOT / "labs" / f"lab-{number:02d}.html"
        title = title_from(path)
        lab_items.append(f'<li><a href="labs/lab-{number:02d}.html">{title}</a></li>')
    problem_items = []
    for number in range(1, 8):
        path = COURSE_ROOT / "problem-sets" / f"problem-set-{number:02d}.html"
        title = title_from(path)
        problem_items.append(
            f'<li><a href="problem-sets/problem-set-{number:02d}.html">{title}</a> · '
            f'<a href="problem-sets/problem-set-{number:02d}-solutions.html">solutions</a> · '
            f'<a href="problem-sets/problem-set-{number:02d}-assessment.md">assessment instructions</a></li>')

    template = replace_section_list(template, "Lecture Materials", lecture_items)
    template = replace_section_list(template, "Labs and Observing", lab_items)
    template = replace_section_list(template, "Problem Sets", problem_items)
    if "{{" in template:
        raise AssertionError("Unfilled course-index template placeholder remains")
    (COURSE_ROOT / "index.html").write_text(template, encoding="utf-8")


def checksum_entries() -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(GENERATED.iterdir())
        if path.is_file() and path.name != CHECKSUM_FILE.name
    }


def write_checksums() -> None:
    entries = checksum_entries()
    CHECKSUM_FILE.write_text("".join(f"{digest}  {name}\n" for name, digest in entries.items()), encoding="utf-8")


def verify_checksums() -> None:
    if not CHECKSUM_FILE.exists():
        raise AssertionError(f"Missing checksum manifest: {CHECKSUM_FILE}")
    declared: dict[str, str] = {}
    for line in CHECKSUM_FILE.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        declared[name] = digest
    actual = checksum_entries()
    if declared != actual:
        missing = sorted(set(declared) - set(actual))
        extra = sorted(set(actual) - set(declared))
        changed = sorted(name for name in set(actual) & set(declared) if actual[name] != declared[name])
        raise AssertionError(f"Checksum mismatch: missing={missing}, extra={extra}, changed={changed}")


def verify_local_links() -> int:
    checked = 0
    for page in COURSE_ROOT.rglob("*.html"):
        parser = parse_html(page)
        for href in parser.hrefs:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (page.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                raise AssertionError(f"Broken local link in {page.relative_to(COURSE_ROOT)}: {href}")
            if parsed.fragment and target.suffix.lower() in {".html", ".htm"}:
                if unquote(parsed.fragment) not in parse_html(target).ids:
                    raise AssertionError(f"Broken local fragment in {page.relative_to(COURSE_ROOT)}: {href}")
            checked += 1
    return checked


def verify_index_links() -> dict[str, int]:
    parser = parse_html(COURSE_ROOT / "index.html")
    counts = {
        "slides": sum(bool(re.fullmatch(r"lectures/lecture-\d{2}-slides\.html", href)) for href in parser.hrefs),
        "notes": sum(bool(re.fullmatch(r"lectures/lecture-\d{2}-notes\.html", href)) for href in parser.hrefs),
        "labs": sum(bool(re.fullmatch(r"labs/lab-\d{2}\.html", href)) for href in parser.hrefs),
        "problemSets": sum(bool(re.fullmatch(r"problem-sets/problem-set-\d{2}\.html", href)) for href in parser.hrefs),
        "solutionKeys": sum(bool(re.fullmatch(r"problem-sets/problem-set-\d{2}-solutions\.html", href)) for href in parser.hrefs),
        "assessmentInstructions": sum(bool(re.fullmatch(r"problem-sets/problem-set-\d{2}-assessment\.md", href)) for href in parser.hrefs),
    }
    expected = {"slides": 14, "notes": 14, "labs": 7, "problemSets": 7, "solutionKeys": 7, "assessmentInstructions": 7}
    if counts != expected:
        raise AssertionError(f"Index link counts do not match {expected}: {counts}")
    link_text = dict(parser.links)
    for number in range(1, 15):
        path = f"lectures/lecture-{number:02d}-slides.html"
        title = title_from(COURSE_ROOT / path)
        if title not in link_text.get(path, ""):
            raise AssertionError(f"Index title disagrees with slide h1 for {path}: {link_text.get(path)} != {title}")
        note_path = f"lectures/lecture-{number:02d}-notes.html"
        if title not in link_text.get(note_path, ""):
            raise AssertionError(f"Lecture notes link omits its source slide title: {note_path}")
    return counts


def verify_diagrams() -> int:
    signatures = set()
    for path in sorted((COURSE_ROOT / "lectures").glob("lecture-*-slides.html")):
        content = path.read_text(encoding="utf-8")
        match = re.search(r"<svg\b.*?</svg>", content, flags=re.DOTALL)
        if match is None:
            raise AssertionError(f"No SVG diagram found in {path.name}")
        signature = match.group(0)
        signature = re.sub(r"<(?:title|desc|text)\b.*?</(?:title|desc|text)>", "", signature, flags=re.DOTALL)
        signature = re.sub(r"\s(?:fill|stroke|class|role|aria-[\w-]+|id)=(?:'[^']*'|\"[^\"]*\")", "", signature)
        signatures.add(re.sub(r"\s+", " ", signature).strip())
    if len(signatures) != 14:
        raise AssertionError(f"Expected 14 unique lecture diagram geometries, found {len(signatures)}")
    return len(signatures)


def validate_package() -> dict[str, object]:
    build_index()
    write_checksums()
    verify_checksums()
    expected_patterns = {
        "slides": ("lectures/lecture-*-slides.html", 14),
        "notes": ("lectures/lecture-*-notes.html", 14),
        "labs": ("labs/lab-*.html", 7),
        "problemSets": ("problem-sets/problem-set-*.html", 14),
        "assessmentInstructions": ("problem-sets/problem-set-*-assessment.md", 7),
    }
    for name, (pattern, expected) in expected_patterns.items():
        actual = len(list(COURSE_ROOT.glob(pattern)))
        if actual != expected:
            raise AssertionError(f"{name}: expected {expected}, found {actual}")
    manifest = json.loads((COURSE_ROOT / "course-manifest.json").read_text(encoding="utf-8"))
    manifest_counts = manifest["counts"]
    expected_manifest = {"slides": 14, "notes": 14, "labs": 7, "problemSets": 7,
                         "solutionKeys": 7, "assessmentInstructions": 7}
    if manifest_counts != expected_manifest:
        raise AssertionError(f"Manifest artifact counts differ from disk expectations: {manifest_counts}")
    schedule_text = (COURSE_ROOT / "schedule.html").read_text(encoding="utf-8")
    first_body = re.search(r"<tbody>(.*?)</tbody>", schedule_text, flags=re.DOTALL)
    if first_body is None:
        raise AssertionError("Schedule has no calendar body")
    calendar_rows = re.findall(r"<tr><td>(\d+)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>", first_body.group(1), flags=re.DOTALL)
    if [int(row[0]) for row in calendar_rows] != list(range(1, 15)):
        raise AssertionError("Schedule calendar must contain exactly Weeks 1-14 in order")
    assessments_by_week = {2: "Lab 01; Problem Set 01", 3: "Lab 02; Problem Set 02",
                           4: "Lab 03; Problem Set 03", 6: "Lab 04; Problem Set 04",
                           8: "Lab 05; Problem Set 05", 12: "Lab 06; Problem Set 06",
                           14: "Lab 07; Problem Set 07"}
    for week_text, lecture_cell, _, assessment_cell in calendar_rows:
        week = int(week_text)
        if assessment_cell != assessments_by_week.get(week, "No lab or problem set due"):
            raise AssertionError(f"Week {week} assessment mapping is inconsistent: {assessment_cell}")
        if f"Lecture {week:02d}:" not in lecture_cell:
            raise AssertionError(f"Week {week} must map to Lecture {week:02d}")
    for number in range(1, 8):
        if not (COURSE_ROOT / "problem-sets" / f"problem-set-{number:02d}-solutions.html").is_file():
            raise AssertionError(f"Missing solution key {number:02d}")
    if not (GENERATED / "hydro_profile_128.csv").is_file():
        raise AssertionError("Missing generated 128-zone hydro profile")
    request_record = json.loads((GENERATED / "jpl_earth_request.json").read_text(encoding="utf-8"))
    vector_digest = hashlib.sha256((GENERATED / "jpl_earth_vectors.csv").read_bytes()).hexdigest()
    if request_record["vectorCsvSha256"] != vector_digest or request_record["provenanceLevel"] != 2:
        raise AssertionError("JPL request trace checksum or provenance level is inconsistent")
    stored = json.loads((GENERATED / "computed_results.json").read_text(encoding="utf-8"))
    current = compute_results()
    if stored != current:
        raise AssertionError("Stored computed_results.json differs from a fresh numerical recomputation")
    index_counts = verify_index_links()
    local_links = verify_local_links()
    unique_diagrams = verify_diagrams()
    curriculum = parse_html(REPO_ROOT / "astronomy_curriculum.html")
    if "materials/ASTR474/index.html" not in curriculum.hrefs:
        raise AssertionError("ASTR474 calendar card does not link to its course index")
    return {"indexLinks": index_counts, "localLinksChecked": local_links,
            "uniqueDiagrams": unique_diagrams, "checksumsVerified": len(checksum_entries()),
            "computedResultsRecomputed": True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-checksums", action="store_true")
    args = parser.parse_args()
    if args.verify_checksums:
        verify_checksums()
        print(f"Verified {len(checksum_entries())} generated-data checksums")
    else:
        report = validate_package()
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()