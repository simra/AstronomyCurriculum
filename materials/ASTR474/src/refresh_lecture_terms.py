"""Refresh only ASTR 474 lecture term explorers without recomputing datasets."""
from __future__ import annotations

import ast
from pathlib import Path

from term_explorer import (
    TERM_EXPLORER_CSS,
    TERM_EXPLORER_SCRIPT,
    notes_section,
    slide_section,
)


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = Path(__file__).with_name("build_astr474_materials.py")


def load_lectures() -> list[dict[str, str]]:
    tree = ast.parse(GENERATOR.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "LECTURES":
                    return ast.literal_eval(node.value)
    raise RuntimeError("Could not locate literal LECTURES data in active generator")


def add_css(document: str) -> str:
    if ".term-explorer{" not in document:
        document = document.replace("</style>", TERM_EXPLORER_CSS + "</style>", 1)
    return document


def add_script(document: str) -> str:
    if 'document.querySelectorAll("[data-term-explorer]")' not in document:
        document = document.replace("</body>", TERM_EXPLORER_SCRIPT + "</body>", 1)
    return document


def insert_after_section(document: str, section_number: int, addition: str) -> str:
    offset = 0
    for _ in range(section_number):
        offset = document.find("</section>", offset)
        if offset < 0:
            raise RuntimeError(f"Could not find section {section_number} insertion point")
        offset += len("</section>")
    return document[:offset] + addition + document[offset:]


def refresh() -> int:
    lectures = load_lectures()
    changed = 0
    for number, item in enumerate(lectures, 1):
        slide_path = ROOT / "lectures" / f"lecture-{number:02d}-slides.html"
        note_path = ROOT / "lectures" / f"lecture-{number:02d}-notes.html"
        slides = slide_path.read_text(encoding="utf-8")
        notes = note_path.read_text(encoding="utf-8")
        if "data-term-explorer" not in slides:
            slides = insert_after_section(
                slides,
                3,
                slide_section(number, item["title"], item["question"], item["equation"], item["concept"], item["limit"]),
            )
        slides = add_script(add_css(slides))
        if "Terms Developed in Context" not in notes:
            notes = notes.replace(
                "<main>",
                "<main>" + notes_section(number, item["title"], item["question"], item["equation"], item["concept"], item["limit"]),
                1,
            )
        if slide_path.read_text(encoding="utf-8") != slides or b"\r\n" in slide_path.read_bytes():
            slide_path.write_text(slides, encoding="utf-8", newline="\n")
            changed += 1
        if note_path.read_text(encoding="utf-8") != notes or b"\r\n" in note_path.read_bytes():
            note_path.write_text(notes, encoding="utf-8", newline="\n")
            changed += 1
    return changed


if __name__ == "__main__":
    print(f"Updated {refresh()} ASTR 474 lecture HTML files")
