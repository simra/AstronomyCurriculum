"""Validate ASTR 101 slide term explorers and matching notes coverage."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LECTURES = ROOT / "lectures"


def parseable(path: Path, text: str, errors: list[str]) -> None:
    try:
        document = BeautifulSoup(text, "html.parser")
    except Exception as exc:
        errors.append(f"{path.name}: HTML parse error: {exc}")
        return
    if not text.lstrip().lower().startswith("<!doctype html>"):
        errors.append(f"{path.name}: missing HTML5 doctype")
    for required in ("html", "head", "body"):
        if document.find(required) is None:
            errors.append(f"{path.name}: parsed document lacks <{required}>")


def validate_pair(number: int) -> tuple[dict[str, int], list[str]]:
    slide_path = LECTURES / f"lecture-{number:02d}-slides.html"
    notes_path = LECTURES / f"lecture-{number:02d}-notes.html"
    errors: list[str] = []
    counts = {"decks": 1, "notes": 1, "buttons": 0, "panels": 0, "note_terms": 0}

    slide_text = slide_path.read_text(encoding="utf-8")
    notes_text = notes_path.read_text(encoding="utf-8")
    parseable(slide_path, slide_text, errors)
    parseable(notes_path, notes_text, errors)
    slide = BeautifulSoup(slide_text, "html.parser")
    notes = BeautifulSoup(notes_text, "html.parser")

    explorers = slide.select("[data-term-explorer]")
    if len(explorers) != 1:
        errors.append(f"{slide_path.name}: expected one term explorer, found {len(explorers)}")
        return counts, errors
    explorer = explorers[0]
    buttons = explorer.select('button[role="tab"]')
    panels = explorer.select('[role="tabpanel"]')
    counts["buttons"] = len(buttons)
    counts["panels"] = len(panels)
    if not 5 <= len(buttons) <= 8:
        errors.append(f"{slide_path.name}: expected 5-8 term buttons, found {len(buttons)}")
    if len(buttons) != len(panels):
        errors.append(f"{slide_path.name}: {len(buttons)} buttons != {len(panels)} panels")

    ids = [tag["id"] for tag in slide.select("[id]")]
    duplicates = sorted(item for item, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append(f"{slide_path.name}: duplicate ids {duplicates}")

    slide_sections = slide.select("section.slide")
    explorer_section = explorer.find_parent("section")
    if explorer_section not in slide_sections or slide_sections.index(explorer_section) > 4:
        errors.append(f"{slide_path.name}: term explorer is not early in the deck")

    terms: list[str] = []
    for index, button in enumerate(buttons):
        control = button.get("aria-controls")
        target = button.get("data-term-target")
        if not control or control != target:
            errors.append(f"{slide_path.name}: button {index + 1} aria-controls/data target mismatch")
            continue
        panel = explorer.find(id=control)
        if panel is None or panel.get("role") != "tabpanel":
            errors.append(f"{slide_path.name}: button {index + 1} lacks one matching panel")
            continue
        if panel.get("aria-labelledby") != button.get("id"):
            errors.append(f"{slide_path.name}: panel {control} aria-labelledby mismatch")
        term = button.get_text(" ", strip=True)
        terms.append(term)
        heading = panel.find("h3")
        if heading is None or heading.get_text(" ", strip=True) != term:
            errors.append(f"{slide_path.name}: panel heading does not exactly match {term!r}")
        panel_text = panel.get_text(" ", strip=True)
        for label in ("Definition:", "Why it matters here:", "Relationships:", "Boundary or common confusion:"):
            if label not in panel_text:
                errors.append(f"{slide_path.name}: {term!r} missing {label}")
        selected = button.get("aria-selected")
        tabindex = button.get("tabindex")
        if index == 0:
            if selected != "true" or tabindex != "0" or panel.has_attr("hidden"):
                errors.append(f"{slide_path.name}: first term is not selected, focusable, and visible")
        elif selected != "false" or tabindex != "-1" or not panel.has_attr("hidden"):
            errors.append(f"{slide_path.name}: inactive term state is invalid for {term!r}")

    controlled = [button.get("aria-controls") for button in buttons]
    if len(set(controlled)) != len(controlled):
        errors.append(f"{slide_path.name}: multiple buttons control the same panel")
    labelled = [panel.get("aria-labelledby") for panel in panels]
    if len(set(labelled)) != len(labelled):
        errors.append(f"{slide_path.name}: multiple panels use the same aria-labelledby")

    required_css = (
        ".term-button:focus-visible",
        "@media (max-width:800px)",
        "@media print",
        ".term-detail[hidden] { display:block !important; }",
    )
    for marker in required_css:
        if marker not in slide_text:
            errors.append(f"{slide_path.name}: missing CSS marker {marker!r}")
    for key in ("ArrowDown", "ArrowUp", "ArrowRight", "ArrowLeft", "Home", "End"):
        if key not in slide_text:
            errors.append(f"{slide_path.name}: missing keyboard support for {key}")

    context_heading = next(
        (h for h in notes.find_all("h2") if h.get_text(" ", strip=True) == "Terms Developed in Context"),
        None,
    )
    if context_heading is None:
        errors.append(f"{notes_path.name}: missing Terms Developed in Context section")
        note_terms: list[str] = []
    else:
        section = context_heading.find_parent("section")
        note_terms = [dt.get_text(" ", strip=True) for dt in section.select("dl.terms-in-context > dt")]
        counts["note_terms"] = len(note_terms)
        if note_terms != terms:
            errors.append(
                f"{notes_path.name}: exact term coverage/order mismatch; deck={terms!r}, notes={note_terms!r}"
            )
        for dt in section.select("dl.terms-in-context > dt"):
            dd = dt.find_next_sibling("dd")
            if dd is None or len(dd.get_text(" ", strip=True)) < 240:
                errors.append(f"{notes_path.name}: term {dt.get_text(' ', strip=True)!r} is not substantively expanded")
            elif "In context:" not in dd.get_text(" ", strip=True) or "Boundary:" not in dd.get_text(" ", strip=True):
                errors.append(f"{notes_path.name}: term {dt.get_text(' ', strip=True)!r} lacks context or boundary")

    return counts, errors


def main() -> int:
    totals = Counter()
    all_errors: list[str] = []
    for number in range(1, 15):
        counts, errors = validate_pair(number)
        totals.update(counts)
        all_errors.extend(errors)
    print(
        "Validated "
        f"{totals['decks']} decks, {totals['notes']} notes, "
        f"{totals['buttons']} buttons, {totals['panels']} panels, "
        f"and {totals['note_terms']} contextual note entries."
    )
    if all_errors:
        print(f"FAILED with {len(all_errors)} issue(s):")
        for error in all_errors:
            print(f"- {error}")
        return 1
    print("PASS: all terminology accessibility, mapping, fallback, parseability, and coverage checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
