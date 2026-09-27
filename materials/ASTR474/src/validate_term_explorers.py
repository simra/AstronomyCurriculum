"""Validate the 14 ASTR 474 slide/note term-explorer pairs."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path


class TermParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tabs: list[dict[str, str]] = []
        self.panels: list[dict[str, str | bool]] = []
        self.note_terms: list[str] = []
        self.headings: list[str] = []
        self.slide_number = 0
        self.explorer_slide: int | None = None
        self._capture: tuple[str, list[str]] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: "" if value is None else value for key, value in attrs}
        if tag == "section" and "slide" in values.get("class", "").split():
            self.slide_number += 1
        if "data-term-explorer" in values and self.explorer_slide is None:
            self.explorer_slide = self.slide_number
        if tag == "button" and values.get("role") == "tab":
            self.tabs.append(values)
        if tag == "article" and values.get("role") == "tabpanel":
            self.panels.append({**values, "hidden": "hidden" in values})
        if tag in {"button", "dt", "h2"}:
            self._capture = (tag, [])

    def handle_data(self, data: str) -> None:
        if self._capture is not None:
            self._capture[1].append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._capture is None or self._capture[0] != tag:
            return
        text = " ".join("".join(self._capture[1]).split())
        if tag == "button":
            self.tabs[-1]["text"] = text
        elif tag == "dt":
            self.note_terms.append(text)
        else:
            self.headings.append(text)
        self._capture = None


def validate_all(root: Path) -> dict[str, int]:
    validated = 0
    terms_checked = 0
    for number in range(1, 15):
        slide_path = root / "lectures" / f"lecture-{number:02d}-slides.html"
        note_path = root / "lectures" / f"lecture-{number:02d}-notes.html"
        slide_text = slide_path.read_text(encoding="utf-8")
        note_text = note_path.read_text(encoding="utf-8")
        if not slide_text.lstrip().lower().startswith("<!doctype html>") or not note_text.lstrip().lower().startswith("<!doctype html>"):
            raise AssertionError(f"Lecture {number:02d} is not HTML5")
        slide_parser, note_parser = TermParser(), TermParser()
        slide_parser.feed(slide_text)
        note_parser.feed(note_text)
        if not 5 <= len(slide_parser.tabs) <= 8 or len(slide_parser.tabs) != len(slide_parser.panels):
            raise AssertionError(f"Lecture {number:02d} requires 5-8 one-to-one tabs and panels")
        if slide_parser.explorer_slide is None or slide_parser.explorer_slide > 4:
            raise AssertionError(f"Lecture {number:02d} term explorer is not early in the deck")
        panel_by_id = {str(panel.get("id", "")): panel for panel in slide_parser.panels}
        term_names = []
        for index, tab in enumerate(slide_parser.tabs):
            target = tab.get("data-term-target")
            if not target or tab.get("aria-controls") != target or target not in panel_by_id:
                raise AssertionError(f"Lecture {number:02d} tab {index + 1} has no exact target panel")
            panel = panel_by_id[target]
            if panel.get("aria-labelledby") != tab.get("id"):
                raise AssertionError(f"Lecture {number:02d} panel {target} is not labelled by its tab")
            if (index == 0) != (tab.get("aria-selected") == "true"):
                raise AssertionError(f"Lecture {number:02d} has invalid initial selected state")
            if (index != 0) != bool(panel.get("hidden")):
                raise AssertionError(f"Lecture {number:02d} has invalid first-panel fallback")
            term_names.append(str(tab.get("text", "")))
        for marker in ("Definition:", "Why it matters here:", "Relationships:", "Boundary or common confusion:"):
            if slide_text.count(marker) != len(term_names):
                raise AssertionError(f"Lecture {number:02d} is missing panel content marker {marker}")
        for marker in ("@media print", ".term-list{display:none}", ".term-detail[hidden]{display:block!important}", "@media(max-width:800px)", "ArrowDown", "ArrowUp", "Home", "End"):
            if marker not in slide_text:
                raise AssertionError(f"Lecture {number:02d} lacks interaction/print marker {marker}")
        if "Terms Developed in Context" not in note_parser.headings:
            raise AssertionError(f"Lecture {number:02d} notes lack Terms Developed in Context")
        if note_parser.note_terms != term_names:
            raise AssertionError(f"Lecture {number:02d} note terms do not exactly match deck terms")
        validated += 1
        terms_checked += len(term_names)
    return {"lecturePairs": validated, "terms": terms_checked}


if __name__ == "__main__":
    print(validate_all(Path(__file__).resolve().parents[1]))
