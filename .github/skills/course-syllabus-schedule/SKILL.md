---
name: course-syllabus-schedule
description: "Use when: creating a complete syllabus, lecture schedule, lab schedule, assessment plan, or course calendar for any undergraduate astronomy curriculum course. Produces rigorous course-level planning before slides, notes, and problem sets are authored."
---

# Course Syllabus and Schedule Authoring

Use this skill to create the authoritative planning artifact for a course in the astronomy curriculum. This skill must be applied before creating lecture slides, lecture notes, or problem sets.

## Inputs

Request or infer the following from the user or existing curriculum files:

- Course number, title, credits, prerequisites, and catalog description.
- Course level, target student background, and role in the program sequence.
- Term length, meeting pattern, lab frequency, and expected contact hours.
- Whether the course has lecture only, lab only, combined lecture/lab, seminar, research, or capstone structure.
- Any local policies, grading requirements, accessibility expectations, or institutional calendar constraints.

If required information is missing, make conservative assumptions and label them clearly in a short "Assumptions" section.

## Template and Style Requirements

Use the shared standards in `templates/course-materials/STYLE_GUIDE.md` and start from `templates/course-materials/syllabus.template.html` when producing an HTML syllabus. Track recommended resources, visuals, datasets, and readings in `templates/course-materials/reference-log.template.md` or a course-specific copy of it.

Write course-specific outputs under `materials/<COURSECODE>/`, using the repository convention from `course-package-orchestrator`. The syllabus goes in `syllabus.html`, the lecture/lab calendar goes in `schedule.html` when separate from the syllabus, and source/data dependencies are recorded in `course-manifest.json`, `src/`, and `data/`.

## Output Artifacts

Create a complete syllabus package, preferably in HTML when a durable artifact is requested:

- Course identity: number, title, credits, term, meeting pattern, instructor placeholders.
- Course description aligned with the curriculum catalog entry.
- Prerequisites and expected preparation.
- Learning outcomes written for a highly capable undergraduate student body.
- Required and recommended resources, using real sources only.
- Assessment structure with weights and standards.
- Resubmission policy: high standards, with students encouraged to revise and resubmit work to improve mastery and grade.
- Weekly lecture schedule.
- Weekly lab, observing, computing, or seminar schedule where applicable.
- Major assignment and exam calendar.
- Course policies for collaboration, academic integrity, accessibility, late work, data use, and safety.

## Rigor Standards

- Treat students as capable physical science majors preparing for advanced undergraduate work, research, graduate study, teaching, technical work, or science communication.
- Include mathematical, computational, and empirical depth appropriate to the course level.
- Make prerequisites meaningful: do not rely on techniques students have not yet encountered unless they are introduced in the course.
- Use demanding but fair assessments that measure conceptual understanding, quantitative reasoning, data analysis, and scientific communication.
- Ensure labs and projects involve authentic astronomical, physical, chemical, computational, or observational practice where appropriate.

## Schedule Design

Build the schedule in dependency order:

1. Identify the core conceptual arc of the course.
2. Place foundational methods before applications.
3. Place labs after the lecture content needed to perform them, or explicitly mark labs as exploratory previews.
4. Sequence problem sets so each one reinforces recent lectures while maintaining spaced practice.
5. Reserve time for review, project milestones, and synthesis.
6. Avoid overloading a single week with multiple major deadlines unless the course design intentionally requires it.

## Reference Requirements

- Recommended books, articles, datasets, software, and missions must be real.
- If you are not certain a reference exists, do not cite it as real.
- Prefer stable sources: textbooks, peer-reviewed papers, observatory documentation, NASA/ESA/CSA/JAXA mission pages, Astropy documentation, public data archive documentation, or reputable open educational resources.
- Include enough bibliographic information for a human to find each source.

## Quality Checklist

Before finishing, verify:

- Every prerequisite either appears in the program curriculum or is explicitly identified as external placement/background.
- Course outcomes align with course level and assessments.
- The lecture schedule and lab schedule are mutually consistent.
- Assessment weights sum to 100 percent.
- Resubmission policy is present and compatible with high grading standards.
- No later artifact is implied to exist before it has been created.
