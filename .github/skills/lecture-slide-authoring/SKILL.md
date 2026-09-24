---
name: lecture-slide-authoring
description: "Use when: creating lecture slide decks for an undergraduate astronomy course from an existing syllabus and lecture schedule. Requires visuals and real, verifiable references; never invents citations, images, datasets, or mission facts."
---

# Lecture Slide Authoring

Use this skill to create lecture slides for each scheduled lecture in a course. Do not use this skill until the course syllabus and lecture schedule exist.

HTML slide decks are acceptable. When using HTML, produce one deck per lecture or a clearly navigable combined deck, depending on the user's request.

## Template and Style Requirements

Use `templates/course-materials/STYLE_GUIDE.md` for visual identity, math notation, accessibility, and reference standards. Use `templates/course-materials/slides.template.html` as the starting structure for HTML slide decks. Record all references, visuals, data sources, and verification status in `templates/course-materials/reference-log.template.md` or a course-specific copy of it.

Treat the slide template as look-and-feel scaffolding and not enforce a particular lecture trajectory. Shape the deck sequence, pacing, examples, derivations, and visual argument to best meet the lecture learning objectives and the approved course schedule.

## Required Inputs

- Approved course syllabus.
- Approved lecture schedule.
- Course level, prerequisites, and learning outcomes.
- Any required textbook, reading list, datasets, missions, observatories, or software.
- Preferred slide format, if any.

If inputs are missing, request or create only the minimal planning note needed to proceed; do not invent a full course plan inside this skill.

## Deck Structure

For each lecture deck, include:

- Course number, lecture number, lecture title, and date or week placeholder.
- Learning objectives tied to the syllabus.
- Conceptual motivation and connection to previous lectures.
- Definitions and physical principles.
- Mathematical derivations or quantitative models appropriate to the course level.
- Worked examples with units and assumptions.
- Visuals, diagrams, plots, mission images, spectra, maps, or data displays.
- Short in-class questions or prompts for active reasoning.
- Summary of key takeaways.
- References and visual credits.

## Visual Standards

- Use visuals that directly support the scientific point being taught.
- Prefer real data, mission imagery, observatory products, spectra, simulation outputs, or carefully labeled original diagrams.
- Every non-original visual must have a real source and credit.
- Do not use a visual if the source, license, or scientific meaning is uncertain.
- Label axes, units, filters, wavelengths, color scales, and object names when relevant.
- Distinguish schematic diagrams from observational evidence.

## Reference Rules

Never hallucinate references. Apply this rule strictly:

- Only cite a source when it has been verified from a reliable catalog, publisher page, DOI record, mission archive, observatory site, documentation page, or other trustworthy source.
- If a source is remembered but not verified, mark it as "candidate reference requiring verification" and do not present it as a final citation.
- Include links or identifiers when available: DOI, arXiv ID, ISBN, mission archive URL, data release name, or documentation URL.
- Prefer primary or authoritative sources for scientific claims, and use textbooks for standard derivations.

## Rigor Standards

- Slides should challenge highly capable undergraduates without skipping essential scaffolding.
- Mathematical content should be correct, dimensionally consistent, and connected to physical interpretation.
- Quantitative examples should use plausible values and show enough work to be auditable.
- Avoid vague claims such as "scientists believe" when a specific observation, model, or uncertainty can be named.
- For advanced courses, include at least some engagement with current literature or modern survey/mission data where appropriate.

## Dependency Rules

- Follow the approved lecture order unless the user authorizes a schedule revision.
- If slide creation reveals a schedule flaw, stop and send feedback to the syllabus/schedule authoring stage.
- Do not create lecture notes or problem sets here, but include hooks for them: key equations, examples, figures, and concepts that notes and problem sets should expand.

## Quality Checklist

Before finishing a slide deck, verify:

- It maps to the scheduled lecture topic and learning objectives.
- All citations and visual credits are real or explicitly marked as requiring verification.
- Figures have labels and context.
- Mathematical statements are correct for the course level.
- Claims are consistent with the syllabus and neighboring lectures.
- The deck can stand alone as a teaching artifact without relying on hidden context.
