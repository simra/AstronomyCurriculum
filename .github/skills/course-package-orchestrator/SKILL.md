---
name: course-package-orchestrator
description: "Use when: coordinating subagents or staged workflows to produce a complete undergraduate astronomy course package from catalog entry to syllabus, lecture schedule, lab schedule, lecture slides, lecture notes, problem set, solution key, assessment instructions, review feedback, correction, and final assembly."
---

# Course Package Orchestrator

Use this skill to coordinate production of a complete course package for any course in the undergraduate astronomy curriculum. Do not create course materials unless the user explicitly asks to produce a course package. This skill manages dependencies among specialized authoring and review skills.

## Coverage Checklist

This orchestrator coordinates syllabus, lecture schedule, lab schedule, lecture slides, visuals, real references, lecture notes, problem set, solution key, assessment instructions, review feedback, dependencies, high standards, resubmission, and final assembly.

## Shared Template Scaffold

Use the shared templates and standards in `templates/course-materials/` unless the user specifies another format:

- `STYLE_GUIDE.md` for visual identity, MathJax notation, references, accessibility, and grading tone.
- `syllabus.template.html` for syllabus and lecture/lab schedule artifacts.
- `slides.template.html` for lecture slide decks.
- `lecture-notes.template.html` for lecture notes.
- `problem-set.template.html` for student problem sets.
- `solution-key.template.html` for instructor solution keys.
- `assessment-instructions.template.md` for grading-agent instructions.
- `reference-log.template.md` for verified references, visuals, datasets, and source status.

These templates enforce consistent look-and-feel, structure, accessibility, and reference discipline. They do not enforce a particular lecture trajectory; each authoring stage should shape the trajectory of slides, notes, labs, and problem sets to best meet the learning objectives and scientific dependencies of the course.

## Core Principle

Respect artifact dependency order. Later artifacts must be based on approved earlier artifacts:

1. Course catalog entry and program context.
2. Full syllabus, lecture schedule, and lab schedule.
3. Lecture slides for each scheduled lecture.
4. Lecture notes for each lecture.
5. Problem set for each lecture.
6. Separate solution key for each problem set.
7. Agent assessment instructions for submitted solutions.
8. Full-course consistency and correctness review.
9. Corrections and re-review.
10. Final assembly and release summary.

## Required Inputs

Before launching production, gather:

- Course number, title, credits, prerequisites, and catalog description.
- Intended term length and meeting pattern.
- Role of the course in the four-year curriculum.
- Whether labs, observing sessions, computing sessions, seminars, or projects are required.
- Preferred artifact formats and folder layout.
- Any required textbook, reference, software, dataset, instrument, or mission constraints.
- Whether the default HTML-with-MathJax workflow should be replaced by LaTeX for print-first or especially math-heavy artifacts.

If the course catalog entry is missing, create a short planning brief first and ask for confirmation unless the user authorizes reasonable assumptions.

## Subagent Coordination Pattern

When subagents are available, use them to isolate work by artifact type. Provide each subagent only the context it needs and require a structured result.

Recommended assignments:

- Syllabus agent: apply `course-syllabus-schedule`.
- Slides agent: apply `lecture-slide-authoring` after syllabus approval.
- Notes agent: apply `lecture-notes-authoring` after slide decks exist.
- Problem set agent: apply `problem-set-assessment` after notes exist.
- Review agent: apply `course-materials-review` after a coherent package exists.

Require each subagent to report:

- Artifacts created or changed.
- Assumptions made.
- References requiring verification.
- Issues to send backward to earlier stages.
- Readiness status for the next dependency stage.

## Workflow

### 1. Plan the Package

- Identify the expected artifact tree.
- Determine the number of lectures, labs, and problem sets.
- Decide naming conventions.
- Confirm the review criteria and resubmission policy.

### 2. Create Syllabus and Schedule

- Apply `course-syllabus-schedule`.
- Validate assessment weights, prerequisites, lecture order, lab placement, and resource list.
- Do not proceed until the syllabus/schedule is internally coherent.

### 3. Create Slides

- Apply `lecture-slide-authoring` lecture by lecture or module by module.
- Ensure every deck follows the schedule and contains verified visual/reference information.
- If slide authoring exposes schedule defects, return to Step 2.

### 4. Create Lecture Notes

- Apply `lecture-notes-authoring` to each lecture after its slide deck exists.
- Ensure notation, examples, references, and assumptions match the slides.
- If notes expose slide defects, return to Step 3; if they expose sequence defects, return to Step 2.

### 5. Create Problem Sets and Grading Materials

- Apply `problem-set-assessment` for each lecture or scheduled problem set.
- Keep student problem sets, solution keys, and agent assessment instructions separate.
- Ensure problem difficulty is high but fair and tied to taught material.
- If problem writing exposes defects in notes, slides, or schedule, route backward.

### 6. Review the Package

- Apply `course-materials-review` to the assembled materials.
- Treat scientific errors, hallucinated references, inconsistent solutions, broken dependencies, and missing assessment instructions as blocking.
- Send materials back to the appropriate stage with concrete feedback.

### 7. Correct and Re-review

- Apply corrections at the originating stage.
- Regenerate dependent downstream artifacts when changes alter content, notation, schedule, or assessment.
- Re-run review on changed artifacts and their dependents.

### 8. Final Assembly

- Produce a release summary listing all artifacts, assumptions, verified references, unresolved risks, and recommended next review steps.
- Do not claim completion without a fresh review result.

## Rigor and Grading Policy

- Materials should serve a highly capable undergraduate student body.
- Assignments and exams should demand precise reasoning, quantitative competence, scientific interpretation, and clear communication.
- Maintain a high grading standard while encouraging resubmission for improved mastery and grade.
- Assessment instructions must explain how revised submissions are evaluated and how feedback should guide improvement.

## Reference Integrity

- No stage may invent references, datasets, image credits, mission facts, software documentation, or URLs.
- Sources must be verified before final release.
- Candidate references may be recorded only when clearly marked as requiring verification.

## Completion Criteria

A course package is complete only when:

- All required artifacts exist.
- Dependencies were followed or documented.
- A review pass approved the package or clearly identified remaining limitations.
- References and visuals are verified or flagged.
- Student-facing and instructor-facing materials are separated where needed.
- The final summary identifies what was produced and what remains for human review.
