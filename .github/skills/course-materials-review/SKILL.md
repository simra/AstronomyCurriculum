---
name: course-materials-review
description: "Use when: reviewing assembled undergraduate astronomy course materials for consistency, correctness, rigor, prerequisites, references, artifact dependencies, and readiness. Sends materials back with specific feedback when correction is needed."
---

# Course Materials Review

Use this skill to review a complete or partial course package. The reviewer acts as a rigorous academic quality gate and should not silently repair major defects unless the user asks for direct editing.

## Review Inputs

Inspect all available course artifacts:

- Course catalog entry.
- Syllabus and lecture/lab schedule.
- Slide decks.
- Lecture notes.
- Problem sets.
- Solution keys.
- Agent assessment instructions.
- Course folder `index.html` landing page when the package is at final assembly or review-release stage.
- Reference lists, visual credits, datasets, and software requirements.
- Source indexes under `references/source-indexes/` when source-exact readings, figures, images, datasets, or textbook problems are cited.
- Applicable templates and standards from `templates/course-materials/STYLE_GUIDE.md` and `templates/course-materials/`.
- The expected course folder under `materials/<COURSECODE>/`, including `course-manifest.json`, `lectures/`, `labs/`, `problem-sets/`, `src/`, and `data/` where applicable.

## Review Priorities

Review in this order:

1. Artifact completeness and dependency order.
2. Prerequisite and sequence consistency.
3. Scientific, mathematical, computational, and observational correctness.
4. Rigor and appropriateness for course level.
5. Alignment among syllabus, slides, notes, problem sets, solution keys, and assessment instructions.
6. Reference, visual, and dataset verification.
7. Grading standards, resubmission policy, and student-facing clarity.
8. HTML validity, navigability, accessibility, and readability where applicable.
9. Consistency with the shared course-material templates and style guide.
10. Consistency with the `materials/<COURSECODE>/` folder structure and two-digit file naming convention.
11. Accuracy of `index.html` links, statuses, and separation of pending versus completed artifacts when final assembly has begun.- Whether `index.html` lecture links include the lecture's actual title (not just its number), and whether the course package is linked from `astronomy_curriculum.html`'s calendar entry and four-year schedule table.
## Dependency Checks

Verify that:

- The syllabus and schedule exist before lecture artifacts.
- Slides follow the approved schedule.
- Notes expand the slides without changing the sequence unexpectedly.
- Problem sets depend on lecture notes and slides already created.
- Solution keys correspond exactly to problem sets.
- Assessment instructions correspond to the correct problem set and solution key.
- `index.html` is created only after enough package status is known and does not present pending materials as complete.
- Review feedback is resolved before final release.

## Correctness Checks

Evaluate:

- Dimensional consistency of equations and examples.
- Correct use of physical laws, approximations, and boundary conditions.
- Correct interpretation of astronomical observations and derived quantities.
- Appropriate statistical and computational methods.
- Consistency of notation, symbols, coordinate systems, units, and terminology.
- Whether prerequisites actually prepare students for the expected work.

## Depth and Pedagogical Substance Checks

Treat shallow materials as blocking defects when they would prevent real instruction:

- Slide decks for lecture courses should contain enough detail for a typical 60-minute class unless the course format justifies otherwise.
- Decks should not simply follow the template trajectory with generic bullets. They need a real lecture arc, explanatory content, evidence, quantitative reasoning, worked examples, and synthesis.
- Student-facing prose must not expose raw LaTeX commands such as `\qquad`, `\mathrm`, `\frac`, `\text`, or unwrapped equation source. Math belongs in MathJax-rendered equation blocks or clean prose.
- Introductory course materials should include appropriate historical and motivational context: why the subject matters, who developed key questions or methods, and how observations led to formulas or models.
- Slide decks are student-facing artifacts. Flag lecturer-facing or production-facing commentary on slides as a correction item.
- If a slide says what the instructor, authoring agent, reviewer, or future course team should do, request replacement with student-directed explanation, evidence, examples, questions, or figures.
- Flag meta labels such as "lecture-specific reasoning figure", "student task", "instructor-created", "verify against", "placeholder", or "to be replaced" when they appear on student-facing slides.
- Repeated visual-reasoning or template slides that do not change meaningfully between lectures should be flagged for lecture-specific replacement.
- Figures that are too small to inspect during lecture should be flagged as blocking defects for slide quality.
- Generic repeated schematics across multiple lectures should be rejected unless each instance carries lecture-specific scientific content.
- Perform a mechanical check across a course's lecture files for a repeated generic visual-reasoning diagram: if the same SVG shape coordinates/layout (e.g., identical rectangle positions and colors) appear across most or all lectures with only text labels differing, treat this as a blocking defect, even if each lecture's surrounding prose is otherwise lecture-specific. A missing visual-reasoning slide in most/all lectures of a course (no figure at all) is likewise a blocking defect; omitting the slide is acceptable only as a rare, individually-justified exception.
- Review slide quality against the standard of a serious undergraduate astronomy course at institutions such as MIT or Stanford: rigorous, visually legible, conceptually precise, and worthy of classroom use.
- Lecture notes should expand slides into study-ready explanations, not merely repeat slide headings.
- Problem sets should contain concrete, lecture-specific questions and should not reuse generic interchangeable prompts across assignments.
- Problem sets should include exact textbook problem recommendations when a textbook is adopted and available. Verify the exercise category/type (for example, Review Question vs. Thought Question vs. Figuring for Yourself) as well as its chapter/section and number against the source index; a correct number with the wrong exercise type is still an inaccurate citation and a correction item. Vague textbook references are also a correction item.
- Quantitative rigor should match course level and should ramp upward across the curriculum; upper-division astronomy courses should not be mostly conceptual unless the course design explicitly justifies it.
- Labs should not be formulaic; formulaic labs are a correction item. Each lab must include lab-specific apparatus or software, concrete setup instructions, exact measurements or classifications, uncertainty treatment, deliverables, assessment criteria, and source/data provenance.
- Source indexes should be lightweight, searchable, and documented. They should identify extraction limitations and human spot-check requirements rather than pretending generated indexes are authoritative editions.
- If an adopted textbook exists, check that slides and notes are grounded in its appropriate chapters, terminology, and scope without copying large passages.
- A review should flag inadequate depth, missing worked examples, missing evidence, missing visual context, or weak textbook alignment as `Needs correction`.
- Independently recompute at least one worked numeric example per lecture, lab, and problem set (do not just read the stated result) to catch arithmetic errors; flag any mismatch as a blocking defect, even if the surrounding content is otherwise strong. Pay particular attention to unit conversions in large-number or logarithmic calculations (e.g., km/Mpc, parsecs to meters, magnitude scales) — these are a recurring source of silent errors even when the surrounding formula is correct.
- Verify comparative-magnitude statements, not just raw computed values: a claim that one quantity is "more than X times" another, or "a small fraction of" another, must match the actual ratio computed (check whether the ratio is above or below 1 and stated in the correct direction). A correct number embedded in a backwards or nonsensical comparison is still a blocking defect.
- Check that worked examples using simplifying approximations (uniform density, point mass, idealized geometry) honestly characterize the size of any discrepancy with the real/measured value. Do not accept prose that calls an order-of-magnitude or larger gap "excellent agreement" or similar; require the text to state the gap accurately and attribute it to the named simplifying assumption.
- When a lab or problem set uses synthetic or "instructor-provided" placeholder data, check whether real, verifiable local data (e.g., the user's own datasets, observing archives, or other workspace files) could ground it instead, and flag this as a correction item rather than a permanent caveat if such data is plausibly available.
- Check that every real-world dataset's provenance is labeled at the correct level in `reference-log.md`: live-verified this session, standard published/literature value not re-verified this session, or synthetic/instructor-provided. Flag mislabeling in either direction (overclaiming live verification, or calling a real literature value "synthetic").

## Reference and Visual Verification

- Flag any citation, visual, dataset, mission fact, or URL that cannot be verified.
- Identify fabricated or suspicious references explicitly.
- Check that visual credits are present and tied to the correct image or dataset.
- Check that Creative Commons or public-domain visuals have source, creator/institution, license or usage note, object/context, and access date where practical.
- Prefer authoritative sources for corrections: textbooks, peer-reviewed papers, observatory or mission documentation, and public archive documentation.

## Feedback Protocol

When corrections are needed, return structured feedback instead of approving:

- Status: `Needs correction`.
- Blocking issues: defects that prevent use.
- Non-blocking improvements: refinements that improve quality but do not prevent use.
- Artifact owner: syllabus/schedule, slides, notes, problem sets, solution keys, assessment instructions, or orchestrator.
- Required correction: concrete action to take.
- Evidence: quote or identify the relevant section, equation, problem, reference, or slide.
- Re-review criteria: what must be true for approval.

When materials are ready, return:

- Status: `Approved for review release` or `Approved for instructional use`, depending on user request.
- Residual risks or assumptions.
- Summary of reviewed artifacts.

## Rigor Standards

- Hold materials to high standards suitable for capable undergraduates.
- Do not dilute challenging work, but flag missing scaffolding when difficulty comes from unclear preparation rather than meaningful rigor.
- Ensure resubmission opportunities support learning while preserving demanding grading criteria.
- Treat hallucinated references, false claims, and inconsistent solution keys as blocking defects.

## Quality Checklist

Before completing the review, verify:

- Every available artifact was considered.
- Findings are specific and actionable.
- Blocking issues are separated from improvements.
- Corrections are routed to the right authoring stage.
- Approval is not granted if references, solutions, or scientific claims remain unverified.
- Approval is not granted for template-complete but substantively shallow slides or notes.
- Approval is not granted for template-complete but substantively shallow or non-specific problem sets.
- Approval is not granted when student-facing slides contain instructor-only commentary that should live in notes or review artifacts.
- Approval is not granted when slide captions describe the production process rather than the scientific content students should learn.
- Approval is not granted when student-facing prose contains raw LaTeX source that should render as mathematics.
- Approval is not granted for labs that differ only by title/subtitle or lack concrete apparatus, measurements, uncertainty, and provenance.
- `Approved for review release` requires the package to meet the quality floor established by the reviewed ASTR101 and ASTR120 examples: lecture-specific evidence, quantitative work, concrete labs, concrete problem sets, and clear visual and explanatory quality.
- Do not grant review-release approval to a package that is only structurally complete. A package must be comparable in quality to the higher-quality reviewed examples before approval. If it falls below that floor, the correct result is `Needs correction`.
- If the package is materially weaker than the reviewed benchmark courses, the review should state the specific quality deficits instead of approving on nominal completeness.
