from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

BASE = Path(__file__).resolve().parent
PDF = BASE / "openstax-astronomy-2e.pdf"
OUT = BASE / "openstax-astronomy-2e-extracted.txt"


def main() -> None:
    reader = PdfReader(str(PDF))
    parts: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = "\n".join(line.rstrip() for line in text.splitlines())
        parts.append(f"\n\n===== PDF PAGE {index} =====\n{text}")
    OUT.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")
    print(f"pages={len(reader.pages)}")
    print(f"output={OUT}")
    print(f"bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
