"""Assemble the ASTR 472 landing page from actual artifact headings."""
from __future__ import annotations

import html
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT.parents[1] / "templates" / "course-materials" / "course-index.template.html"


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_h1 = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "h1":
            self.in_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        if self.in_h1:
            self.parts.append(data)


def h1(relative_path: str) -> str:
    parser = HeadingParser()
    parser.feed((ROOT / relative_path).read_text(encoding="utf-8"))
    title = " ".join(" ".join(parser.parts).split())
    if not title:
        raise ValueError(f"No h1 heading found in {relative_path}")
    return title


def link_row(label: str, href: str, suffix: str = "") -> str:
    return f'<a href="{href}">{html.escape(label)}</a>{suffix}'


def assemble() -> None:
    manifest = json.loads((ROOT / "course-manifest.json").read_text(encoding="utf-8"))
    template = TEMPLATE.read_text(encoding="utf-8")
    lectures = [h1(f"lectures/lecture-{number:02d}-slides.html") for number in range(1, 15)]
    labs = [h1(f"labs/lab-{number:02d}.html") for number in range(1, 8)]
    problem_sets = [h1(f"problem-sets/problem-set-{number:02d}.html") for number in range(1, 8)]

    template = template.replace("Lecture 01: {{LECTURE_01_TITLE}}", "{{LECTURE_01_TITLE}}")
    template = template.replace(">Lab 01</a>", ">{{LAB_01_TITLE}}</a>")
    template = template.replace(">Problem Set 01</a>", ">{{PROBLEM_SET_01_TITLE}}</a>")
    additional_lectures = "</li><li>".join(
        link_row(title, f"lectures/lecture-{number:02d}-slides.html", " &mdash; slides")
        + f' · <a href="lectures/lecture-{number:02d}-notes.html">notes</a>'
        for number, title in enumerate(lectures[1:], 2)
    )
    additional_labs = "</li><li>".join(
        link_row(title, f"labs/lab-{number:02d}.html")
        for number, title in enumerate(labs[1:], 2)
    )
    additional_problem_sets = "</li><li>".join(
        link_row(title, f"problem-sets/problem-set-{number:02d}.html")
        + f' · <a href="problem-sets/problem-set-{number:02d}-solutions.html">solutions</a>'
        + f' · <a href="problem-sets/problem-set-{number:02d}-assessment.md">assessment instructions</a>'
        for number, title in enumerate(problem_sets[1:], 2)
    )

    values = {
        "{{COURSE_CODE}}": "ASTR 472",
        "{{COURSE_TITLE}}": "Radio Astronomy",
        "{{CREDITS}}": "3",
        "{{TERM_OR_SEQUENCE}}": "Year 4 elective",
        "{{PACKAGE_STATUS}}": manifest["status"]["reviewStatus"],
        "{{COURSE_DESCRIPTION}}": manifest["course"]["description"],
        "{{LAST_UPDATED}}": manifest["status"]["lastUpdated"],
        "{{SYLLABUS_STATUS}}": "Complete · 14-lecture and seven-unit cadence documented",
        "{{SCHEDULE_STATUS}}": "Complete · labs and problem sets follow each paired unit",
        "{{REFERENCE_LOG_STATUS}}": "Complete · tri-level source/data provenance recorded",
        "{{LECTURE_01_TITLE}}": lectures[0],
        "{{LECTURE_01_STATUS}}": "slides and notes",
        "{{ADDITIONAL_LECTURE_LINKS}}": additional_lectures,
        "{{LAB_01_TITLE}}": labs[0],
        "{{LAB_01_STATUS}}": "complete",
        "{{ADDITIONAL_LAB_LINKS}}": additional_labs,
        "{{PROBLEM_SET_01_TITLE}}": problem_sets[0],
        "{{PROBLEM_SET_01_STATUS}}": "complete",
        "{{ADDITIONAL_PROBLEM_SET_LINKS}}": additional_problem_sets,
    }
    generated_link_markers = {
        "{{ADDITIONAL_LECTURE_LINKS}}",
        "{{ADDITIONAL_LAB_LINKS}}",
        "{{ADDITIONAL_PROBLEM_SET_LINKS}}",
    }
    for marker, value in values.items():
        template = template.replace(marker, value if marker in generated_link_markers else html.escape(value))
    template = template.replace(
        'Manifest: <a href="course-manifest.json">course-manifest.json</a>',
        'Manifest: <a href="course-manifest.json">course-manifest.json</a> · '
        '<a href="review-report.md">review report</a> · <a href="README.md">README</a>',
    )
    generator_links = " · ".join(
        f'<a href="src/{path.name}">{html.escape(path.name)}</a>'
        for path in sorted((ROOT / "src").glob("generate_astr472_*.py"))
    )
    template = template.replace(
        '<p><a href="src/README.md">Open source README</a></p>',
        f'<p><a href="src/README.md">Open source README</a> · {generator_links}</p>',
    )
    if "{{" in template:
        raise ValueError("Unresolved template marker remains in course index")
    (ROOT / "index.html").write_text(template, encoding="utf-8")


if __name__ == "__main__":
    assemble()