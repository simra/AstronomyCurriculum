from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
SRC = BASE / "openstax-astronomy-2e-extracted.txt"
OUT_DIR = BASE / "source-indexes"
OUT_JSON = OUT_DIR / "openstax-astronomy-2e-problem-index.json"
OUT_MD = OUT_DIR / "openstax-astronomy-2e-problem-index.md"

SECTION_HEADINGS = {"Review Questions", "Thought Questions", "Figuring for Yourself"}
PROBLEM_RE = re.compile(r"^(\d+)\s*\.\s*(.*)")
SKIP_RE = re.compile(r"^(Access for free|\d+\s+\d+\s+\u2022|\d+\s+\u2022|This OpenStax|Chapter|Appendix|Figure|Table)\b")


def clean(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def main() -> None:
    lines = SRC.read_text(encoding="utf-8", errors="ignore").splitlines()
    chapter = 0
    current_section: str | None = None
    current: dict | None = None
    records: list[dict] = []

    def flush() -> None:
        nonlocal current
        if current is not None:
            current["prompt"] = clean(current["prompt"])
            current["excerpt"] = current["prompt"][:360]
            records.append(current)
            current = None

    for line_number, raw in enumerate(lines, start=1):
        line = clean(raw)
        if not line:
            continue
        if line in SECTION_HEADINGS:
            flush()
            current_section = line
            if line == "Review Questions":
                chapter += 1
            continue
        if current_section is None:
            continue
        if line in {"Collaborative Group Activities", "Exercises", "Key Terms", "Summary", "For Further Exploration"}:
            flush()
            current_section = None
            continue
        match = PROBLEM_RE.match(line)
        if match:
            flush()
            current = {
                "chapter": chapter,
                "section": current_section,
                "number": int(match.group(1)),
                "line": line_number,
                "prompt": match.group(2).strip(),
            }
            continue
        if current is not None and not SKIP_RE.match(line):
            current["prompt"] += " " + line
    flush()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    by_chapter: dict[int, list[dict]] = {}
    for rec in records:
        by_chapter.setdefault(rec["chapter"], []).append(rec)
    md: list[str] = ["# OpenStax Astronomy 2e Problem Index", "", "Generated from `openstax-astronomy-2e-extracted.txt`. Verify against the adopted PDF before final assignment.", ""]
    for chapter_number in sorted(by_chapter):
        md.append(f"## Chapter {chapter_number}")
        md.append("")
        for rec in by_chapter[chapter_number]:
            md.append(f"- {rec['section']} {rec['number']}: {rec['excerpt']}")
        md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print(f"records={len(records)}")
    print(f"chapters={len(by_chapter)}")
    print(f"json={OUT_JSON}")
    print(f"markdown={OUT_MD}")


if __name__ == "__main__":
    main()
