"""Validate ASTR210 lecture term explorers and paired note coverage."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURES = ROOT / "lectures"


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.buttons = []
        self.panels = []
        self.headings = []
        self.note_terms = []
        self._stack = []
        self._text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self._stack.append((tag, attrs, len(self._text)))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "button" and attrs.get("role") == "tab":
            self.buttons.append(attrs)
        if attrs.get("role") == "tabpanel":
            self.panels.append((tag, attrs))

    def handle_startendtag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])

    def handle_data(self, data):
        self._text.append(data)

    def handle_endtag(self, tag):
        for index in range(len(self._stack) - 1, -1, -1):
            open_tag, attrs, text_start = self._stack[index]
            if open_tag != tag:
                continue
            text = " ".join("".join(self._text[text_start:]).split())
            if tag == "h2":
                self.headings.append(text)
            if tag == "dt":
                self.note_terms.append(text)
            del self._stack[index:]
            return


def parse(path: Path) -> tuple[str, Collector]:
    text = path.read_text(encoding="utf-8")
    parser = Collector()
    parser.feed(text)
    parser.close()
    return text, parser


def check(condition: bool, message: str, errors: list[str]):
    if not condition:
        errors.append(message)


def main() -> int:
    slides = sorted(LECTURES.glob("lecture-??-slides.html"))
    notes = sorted(LECTURES.glob("lecture-??-notes.html"))
    errors: list[str] = []
    total_buttons = total_panels = total_note_terms = 0

    check(len(slides) == 14, f"Expected 14 slide decks, found {len(slides)}", errors)
    check(len(notes) == 14, f"Expected 14 notes files, found {len(notes)}", errors)

    for number in range(1, 15):
        slide_path = LECTURES / f"lecture-{number:02d}-slides.html"
        note_path = LECTURES / f"lecture-{number:02d}-notes.html"
        check(slide_path.exists(), f"Missing {slide_path.name}", errors)
        check(note_path.exists(), f"Missing {note_path.name}", errors)
        if not slide_path.exists() or not note_path.exists():
            continue

        slide_text, slide = parse(slide_path)
        note_text, note = parse(note_path)

        check("Terms for This Lecture" in slide.headings,
              f"{slide_path.name}: missing term-explorer heading", errors)
        check(slide_text.count("<div class='term-explorer' data-term-explorer>") == 1,
              f"{slide_path.name}: expected one explorer", errors)
        check(5 <= len(slide.buttons) <= 8,
              f"{slide_path.name}: expected 5-8 term buttons, found {len(slide.buttons)}", errors)
        check(len(slide.buttons) == len(slide.panels),
              f"{slide_path.name}: {len(slide.buttons)} buttons != {len(slide.panels)} panels", errors)
        check(len(slide.ids) == len(set(slide.ids)),
              f"{slide_path.name}: duplicate HTML ids", errors)

        panel_by_id = {attrs.get("id"): attrs for _, attrs in slide.panels}
        controls = [button.get("aria-controls") for button in slide.buttons]
        check(len(controls) == len(set(controls)),
              f"{slide_path.name}: more than one button controls the same panel", errors)
        check(set(controls) == set(panel_by_id),
              f"{slide_path.name}: button controls do not cover panels exactly once", errors)
        for index, button in enumerate(slide.buttons):
            control = button.get("aria-controls")
            target = button.get("data-term-target")
            button_id = button.get("id")
            check(button.get("type") == "button",
                  f"{slide_path.name}: tab {index + 1} is not a native type=button control", errors)
            check(bool(button_id), f"{slide_path.name}: tab {index + 1} lacks id", errors)
            check(control == target and control in panel_by_id,
                  f"{slide_path.name}: tab {index + 1} control/target mismatch", errors)
            if control in panel_by_id:
                check(panel_by_id[control].get("aria-labelledby") == button_id,
                      f"{slide_path.name}: panel {control} does not label back to {button_id}", errors)

        if slide.buttons and slide.panels:
            first_button = slide.buttons[0]
            first_panel = slide.panels[0][1]
            check(first_button.get("aria-selected") == "true",
                  f"{slide_path.name}: first tab is not selected", errors)
            check("hidden" not in first_panel,
                  f"{slide_path.name}: first panel is hidden before JavaScript", errors)
            for button in slide.buttons[1:]:
                check(button.get("aria-selected") == "false",
                      f"{slide_path.name}: non-first tab initially selected", errors)
            for _, panel in slide.panels[1:]:
                check("hidden" in panel,
                      f"{slide_path.name}: non-first panel initially visible", errors)

        check(".term-detail[hidden]{display:block}" in slide_text,
              f"{slide_path.name}: print CSS does not reveal hidden panels", errors)
        check(".term-list{display:none}" in slide_text,
              f"{slide_path.name}: print CSS does not suppress interactive controls", errors)
        check('tab.addEventListener("keydown"' in slide_text
              and '"ArrowDown"' in slide_text and '"Home"' in slide_text and '"End"' in slide_text,
              f"{slide_path.name}: keyboard navigation script incomplete", errors)
        check(not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", slide_text),
              f"{slide_path.name}: generated HTML contains control characters", errors)

        check("Terms Developed in Context" in note.headings,
              f"{note_path.name}: missing Terms Developed in Context section", errors)
        panel_terms = []
        for _, attrs in slide.panels:
            panel_id = re.escape(attrs["id"])
            match = re.search(
                rf"<article class='term-detail' id='{panel_id}'.*?<h3>(.*?)</h3>",
                slide_text,
                flags=re.S,
            )
            check(match is not None, f"{slide_path.name}: cannot read term for {attrs['id']}", errors)
            if match:
                panel_terms.append(re.sub(r"<[^>]+>", "", match.group(1)).strip())
        check(note.note_terms == panel_terms,
              f"Lecture {number:02d}: note terms do not exactly match deck terms "
              f"(deck={panel_terms!r}, notes={note.note_terms!r})", errors)
        check(note_text.count("<strong>Developed in this lecture:</strong>") == len(panel_terms),
              f"{note_path.name}: not every term has contextual expansion", errors)
        check(not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", note_text),
              f"{note_path.name}: generated HTML contains control characters", errors)

        total_buttons += len(slide.buttons)
        total_panels += len(slide.panels)
        total_note_terms += len(note.note_terms)

    if errors:
        print(f"FAIL: {len(errors)} validation error(s)")
        for error in errors:
            print(f" - {error}")
        return 1

    print(
        "PASS: 14 slide-note pairs; "
        f"{total_buttons} buttons; {total_panels} panels; "
        f"{total_note_terms} exact note-term expansions; "
        "all ids, ARIA links, initial states, keyboard hooks, print fallbacks, and HTML parses validated."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
