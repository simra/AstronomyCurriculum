---
name: lecture-notes-authoring
description: "Use when: generating rigorous lecture notes for each scheduled undergraduate astronomy lecture after the syllabus and slides exist. Expands slide content into coherent explanations, derivations, examples, references, and study guidance."
---

# Lecture Notes Authoring

Use this skill to create lecture notes for each lecture in a course. Lecture notes should be derived from the approved syllabus, lecture schedule, and slide decks. They should not introduce a new course sequence unless a correction is explicitly required.

## Required Inputs

- Approved syllabus and lecture/lab schedule.
- Approved slide deck for the lecture.
- Course level, prerequisites, and learning outcomes.
- Verified reference list and required readings.

If slides are missing, stop and request slide creation first unless the user explicitly asks for notes to be drafted before slides.

## Template and Style Requirements

Use `templates/course-materials/STYLE_GUIDE.md` for document structure, MathJax notation, figure handling, and reference standards. Use `templates/course-materials/lecture-notes.template.html` as the starting structure for HTML lecture notes. Keep references synchronized with `templates/course-materials/reference-log.template.md` or a course-specific copy of it.

Write course-specific lecture notes under `materials/<COURSECODE>/lectures/` using two-digit names such as `lecture-01-notes.html`. Place any support code under `materials/<COURSECODE>/src/` and any datasets under `materials/<COURSECODE>/data/`.

## Notes Structure

For each lecture, produce notes that include:

- Course number, lecture number, and lecture title.
- Learning objectives.
- Brief connection to previous and upcoming lectures.
- Core concepts and definitions.
- Derivations, equations, and physical interpretation.
- Worked examples with units, assumptions, and intermediate steps.
- Notes on common misconceptions and conceptual traps.
- Connections to observations, experiments, simulations, datasets, missions, or laboratory work.
- Suggested reading and verified references.
- Study questions or reflection prompts.

## Style and Depth

- Write in clear academic prose suitable for capable undergraduates.
- Explain not only what equations state, but what assumptions make them valid.
- Keep mathematical notation consistent with slides and problem sets.
- When deriving results, state boundary conditions, approximations, coordinate systems, and units.
- For observational topics, distinguish raw data, calibrated data, inferred quantities, and model-dependent conclusions.
- For computational topics, explain numerical assumptions and sources of error.
- Notes accompanying a 60-minute lecture should be substantial enough for independent study: develop the lecture arc, expand definitions, include worked reasoning, identify misconceptions, and connect the topic to readings.
- When an adopted textbook is available, especially OpenStax Astronomy 2e for ASTR 101, use it to anchor chapter mapping, terminology, and standard scope while writing original notes.
- Do not produce notes that merely restate slide titles or short slide bullets. Shallow notes should be treated as incomplete.

## Rigor Standards

- Notes should support demanding assignments and examinations.
- Avoid oversimplified analogies that obscure physical mechanisms.
- Include enough detail for independent study without becoming a textbook chapter unless requested.
- Use real examples from astronomy, physics, chemistry, computation, or instrumentation as appropriate.
- Identify open questions, uncertainty, and model limitations in advanced courses.

## Reference Rules

- Use only verified references inherited from the syllabus/slides or newly verified reliable sources.
- Do not invent titles, authors, journal citations, datasets, mission instruments, or URLs.
- If a needed reference cannot be verified, state that verification is required before final release.

## Dependency Rules

- Notes follow the slide deck and lecture schedule.
- If notes reveal an error in slides, send a correction request back to slide authoring.
- If notes reveal a broader sequence problem, send a correction request back to syllabus/schedule authoring.
- Problem sets should draw on notes only after notes are internally consistent.

## Quality Checklist

Before finishing, verify:

- Notes align with the lecture objectives and slide deck.
- Notes are substantive enough to support independent study after a 60-minute lecture.
- Equations and variables use consistent notation.
- Examples are dimensionally correct.
- References are real or explicitly flagged for verification.
- No unexplained concept depends on a later lecture unless intentionally previewed.
- Study prompts prepare students for the planned problem set.
