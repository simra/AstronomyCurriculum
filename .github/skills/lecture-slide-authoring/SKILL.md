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

Write course-specific slide decks under `materials/<COURSECODE>/lectures/` using two-digit names such as `lecture-01-slides.html`. Place any course-specific code used to generate plots, diagrams, or examples under `materials/<COURSECODE>/src/`, and place datasets under `materials/<COURSECODE>/data/` with provenance notes.

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
- A substantive sequence sized for a typical 60-minute lecture, usually 10-16 content slides plus title, objectives, synthesis, and references.
- Definitions and physical principles with enough explanatory depth to teach from the deck.
- Mathematical derivations, quantitative models, or order-of-magnitude reasoning appropriate to the course level.
- Multiple worked examples or guided calculations with units, assumptions, and interpretation.
- Visuals, diagrams, plots, mission images, spectra, maps, or data displays that carry instructional weight, not decorative filler.
- Short in-class questions or prompts for active reasoning, placed where they test a concept just developed.
- Summary of key takeaways.
- References and visual credits.

## Depth Requirements

- Do not generate slide decks that merely fill the template sections. Template-shaped but shallow decks are unacceptable.
- Each deck must be detailed enough for an instructor to deliver a coherent 60-minute lecture without inventing most of the content live.
- Slides are student-facing instructional materials. Do not include commentary directed at the lecturer, course director, generator, reviewer, or future authoring process.
- Put instructor-only guidance, production notes, visual replacement notes, and review comments in lecture notes, speaker notes, review reports, or source comments, not on student-facing slides.
- Captions and figure labels must explain the astronomy, physics, data, or model. Do not use meta captions such as "lecture-specific reasoning figure", "student task", "placeholder", "instructor-created", or "verify against" in the student deck.
- Student-facing prose must not expose raw LaTeX source. Use MathJax for equations and plain-language descriptions in bullets.
- Do not reuse a single generic diagram shape/layout (e.g., the same three boxes and arrows, or any other fixed schematic skeleton) across every lecture in a course with only the caption or box labels swapped. Each lecture's visual-reasoning figure must be structurally distinct where the underlying content is different: a real plotted curve or data relationship, a labeled geometric/physical diagram specific to that lecture's phenomenon, an annotated real image, or an equivalent lecture-specific visual -- not a generic flow-chart reused as a container for different words. If, after genuine consideration, no meaningfully distinct diagram is possible for a given lecture, the visual-reasoning slide may be omitted or replaced with another substantive slide, but this must be the rare exception (at most a small minority of lectures in a course), not the default pattern, and should not itself be templated.
- Repeated generic slides are unacceptable unless the repeated structure is filled with lecture-specific student-facing explanation, evidence, examples, or questions.
- Ground introductory astronomy decks in the adopted textbook when available, especially OpenStax Astronomy 2e for ASTR 101. Use the textbook for topic scope, terminology, chapter mapping, and standard examples, while writing original explanations.
- Include motivating and historical context where it deepens the lecture: why people studied the question, who made key observations or models, and how formulas emerged from evidence.
- Include a clear lecture arc: motivating phenomenon, observational evidence, physical model, quantitative tool, worked application, limitation or misconception, active question, and synthesis.
- A first-year deck should normally include at least one quantitative reasoning slide, one evidence or data interpretation slide, one misconception or boundary-condition slide, and one synthesis slide.
- Avoid over-compressing a lecture into a handful of generic bullets. If a deck has fewer than 10 substantive teaching slides, explicitly justify why the lecture format requires that.

## Visual Standards

- Use visuals that directly support the scientific point being taught.
- Slide figures should meet the expectations of a rigorous astronomy course at a highly selective university: clear, accurate, large enough to inspect from a classroom screen, and intellectually central to the slide.
- Prefer real data, mission imagery, observatory products, spectra, simulation outputs, or carefully labeled original diagrams.
- When suitable external visuals are needed, delegate research to `VisualReferenceResearchAgent` or perform equivalent source verification before including them.
- Creative Commons, public-domain, NASA/ESA/observatory, and open-data visuals must still be verified for source, credit, license or usage terms, and scientific context.
- Every non-original visual must have a real source and credit.
- Do not use a visual if the source, license, or scientific meaning is uncertain.
- Label axes, units, filters, wavelengths, color scales, and object names when relevant.
- Distinguish schematic diagrams from observational evidence.
- Do not reuse the same generic figure across lectures. Reused figure styles are acceptable only when the actual content is lecture-specific and meaningfully different.
- Avoid tiny figures. For visual-reasoning slides, the visual should normally occupy at least half the slide area unless the slide has a deliberate comparison layout.

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
- It is substantive enough for a typical 60-minute lecture, or the exception is explicitly justified.
- It is addressed to students and contains no instructor-only production commentary.
- It uses the adopted textbook or verified readings for scope and terminology when such resources are available.
- All citations and visual credits are real or explicitly marked as requiring verification.
- Figures have labels and context.
- Figures are lecture-specific, visually legible, and not repeated generic placeholders.
- Mathematical statements are correct for the course level.
- Claims are consistent with the syllabus and neighboring lectures.
- The deck can stand alone as a teaching artifact without relying on hidden context.
