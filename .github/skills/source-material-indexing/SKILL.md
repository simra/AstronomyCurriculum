---
name: source-material-indexing
description: "Use when: extracting or indexing adopted textbooks, PDFs, source readings, exercise sets, figure lists, or datasets so course artifacts can cite exact sections, figures, and problems without guessing."
---

# Source Material Indexing

Use this skill when a course depends on an adopted textbook or source bundle and exact references are needed for readings, figures, or problem recommendations.

## Purpose

Create lightweight, source-specific indexes only when they solve a concrete verification need. Do not build a large framework for every source by default.

## Inputs

- Source file or URL.
- Intended use: readings, figures, problems, images, datasets, or citations.
- Course package that will consume the index.
- License or usage context where available.

## Outputs

Place generated indexes under `references/source-indexes/` unless a course-specific source belongs under `materials/<COURSECODE>/data/`.

Useful outputs include:

- Machine-readable JSON index.
- Human-readable Markdown index.
- Extraction script or recipe.
- README describing how to use and verify the index.

## Rules

- Indexes support verification; they do not replace human review of the adopted edition.
- Never invent section numbers, figure numbers, problem numbers, page numbers, titles, source URLs, or licenses.
- If extraction is imperfect, preserve uncertainty in the index and in generated course artifacts.
- Cite exact source title, section or chapter when verified, exercise type, problem number, figure number, extracted line/page location, and a short excerpt when useful.
- Mark items requiring edition spot-check before instructional use.
- If extracted chapter/section numbering could be offset from the adopted edition's actual numbering (a known risk with OCR/plain-text extraction), cross-check the extracted chapter label against numbering embedded directly in the text itself (e.g., figure captions like "Figure 18.11" or table labels like "Table 22.2") rather than trusting a chapter-heading count alone; document any resolved or unresolved offset explicitly in the index.

## Quality Checklist

Before finishing, verify:

- The source index can be searched by future agents.
- Generated course materials cite the index accurately.
- Any extraction limitations are documented.
- The approach is proportional to the need and reusable for other source materials without being OpenStax-specific.
