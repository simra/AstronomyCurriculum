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
- Reference lists, visual credits, datasets, and software requirements.
- Applicable templates and standards from `templates/course-materials/STYLE_GUIDE.md` and `templates/course-materials/`.

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

## Dependency Checks

Verify that:

- The syllabus and schedule exist before lecture artifacts.
- Slides follow the approved schedule.
- Notes expand the slides without changing the sequence unexpectedly.
- Problem sets depend on lecture notes and slides already created.
- Solution keys correspond exactly to problem sets.
- Assessment instructions correspond to the correct problem set and solution key.
- Review feedback is resolved before final release.

## Correctness Checks

Evaluate:

- Dimensional consistency of equations and examples.
- Correct use of physical laws, approximations, and boundary conditions.
- Correct interpretation of astronomical observations and derived quantities.
- Appropriate statistical and computational methods.
- Consistency of notation, symbols, coordinate systems, units, and terminology.
- Whether prerequisites actually prepare students for the expected work.

## Reference and Visual Verification

- Flag any citation, visual, dataset, mission fact, or URL that cannot be verified.
- Identify fabricated or suspicious references explicitly.
- Check that visual credits are present and tied to the correct image or dataset.
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
