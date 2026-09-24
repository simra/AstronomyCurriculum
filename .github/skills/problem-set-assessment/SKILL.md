---
name: problem-set-assessment
description: "Use when: creating a problem set for each undergraduate astronomy lecture, a separate solution key, and assessment instructions for an agent to grade submitted solutions with high standards and resubmission opportunities."
---

# Problem Set, Solution Key, and Assessment Authoring

Use this skill to create problem sets after the syllabus, lecture schedule, slides, and lecture notes exist. Each problem set should reinforce a specific lecture while also building cumulative mastery.

## Required Inputs

- Approved syllabus and assessment policy.
- Lecture schedule.
- Slide deck and lecture notes for the target lecture.
- Course level, prerequisites, and expected mathematical/computational background.
- Any required datasets, software, readings, or lab context.

If notes or slides are missing, stop and request those artifacts first unless the user explicitly authorizes a provisional problem set.

## Output Artifacts

For each lecture, create three separate artifacts:

1. Student problem set.
2. Instructor solution key.
3. Agent assessment instructions for evaluating submitted solutions.

HTML is acceptable for problem sets and solution keys. Keep the student-facing problem set separate from the solution key.

## Template and Style Requirements

Use `templates/course-materials/STYLE_GUIDE.md` for math notation, student-facing tone, accessibility, grading language, and resubmission framing. Use `templates/course-materials/problem-set.template.html` for student problem sets, `templates/course-materials/solution-key.template.html` for instructor solution keys, and `templates/course-materials/assessment-instructions.template.md` for grading-agent instructions. Track sources and datasets with `templates/course-materials/reference-log.template.md` or a course-specific copy of it.

## Student Problem Set Requirements

Include:

- Course number, lecture number, problem set title, and due date placeholder.
- Learning objectives practiced by the assignment.
- Instructions for units, significant figures, collaboration, citation, code submission, and data use.
- A mix of conceptual, quantitative, computational, observational, and interpretive questions appropriate to the lecture.
- Problems that require reasoning, not only substitution.
- Extension or challenge problems for advanced students when appropriate.
- Clear deliverables for written, mathematical, plotted, or coded responses.

## Solution Key Requirements

Include:

- Complete worked solutions.
- Rubric point allocation or mastery criteria.
- Common valid alternative approaches.
- Expected units, numerical tolerances, and reasoning standards.
- Notes on common mistakes and how they should affect grading.
- For computational problems, expected algorithm, validation checks, and interpretation of outputs.

## Agent Assessment Instructions

Create instructions that another agent can use to assess submissions. Include:

- The exact artifacts to inspect: student submission, problem set, solution key, rubric, and course policies.
- A grading standard that rewards correct reasoning, physical interpretation, units, clarity, and reproducibility.
- Guidance to identify arithmetic slips separately from conceptual errors.
- Guidance to detect unsupported claims, fabricated references, copied text, missing uncertainty analysis, or invalid code outputs.
- Instructions to provide actionable feedback for revision.
- A resubmission pathway: students may revise and resubmit to improve mastery and grade, but feedback should preserve high standards and not simply give away all reasoning unless the solution key is already released.

## Rigor Standards

- Problems should be demanding enough for highly capable undergraduates.
- Include at least one problem that requires synthesis or transfer beyond a worked example when appropriate.
- Quantitative questions must be dimensionally consistent and use plausible astrophysical or physical values.
- Data problems must use real or clearly synthetic data, labeled as such.
- Computational problems must specify expected inputs, outputs, validation, and reproducibility requirements.

## Reference and Data Rules

- Use real references and datasets only when verified.
- Do not invent observatory data releases, catalog names, URLs, papers, or instrument properties.
- If using synthetic data, label it clearly and explain the modeled assumptions.

## Dependency Rules

- Follow the lecture notes and slides for terminology, notation, and assumptions.
- If problem writing exposes an error in notes or slides, send feedback to the relevant authoring stage before finalizing.
- If the assessment load conflicts with the syllabus calendar, send feedback to the syllabus/schedule stage.

## Quality Checklist

Before finishing, verify:

- Every problem maps to lecture objectives.
- Student and instructor artifacts are separate.
- The solution key is complete and internally consistent.
- Rubrics and assessment instructions match the course grading and resubmission policy.
- No problem depends on material not yet taught unless marked as an extension.
- References and datasets are verified or flagged before release.
