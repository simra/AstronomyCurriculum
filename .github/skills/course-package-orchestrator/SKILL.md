---
name: course-package-orchestrator
description: "Use when: coordinating subagents or staged workflows to produce a complete undergraduate astronomy course package from catalog entry to syllabus, lecture schedule, lab schedule, lecture slides, lecture notes, problem set, solution key, assessment instructions, review feedback, correction, and final assembly."
---

# Course Package Orchestrator

Use this skill to coordinate production of a complete course package for any course in the undergraduate astronomy curriculum. Do not create course materials unless the user explicitly asks to produce a course package. This skill manages dependencies among specialized authoring and review skills.

The orchestrating agent remains responsible for end-to-end completion. Subagents may be used for isolated drafting, review, or exploration, but they are optional helpers and not a substitute for completing, validating, correcting, and assembling the course package. If subagents are unavailable, read-only, incomplete, or return only advisory output, the orchestrating agent must continue the workflow directly from the current artifact state.

When using a custom agent entry point, invoke `CoursePackageOrchestrator` for this workflow.

The orchestrator has agency to keep the process moving through reviewer-designated issues. After any review returns `Needs correction`, the orchestrator must classify each issue by owner, delegate or perform the correction, validate the changed artifacts, and re-run review. Continue this loop until the reviewer approves the requested release stage or a concrete external blocker prevents progress.

## Coverage Checklist

This orchestrator coordinates syllabus, lecture schedule, lab schedule, lecture slides, visuals, real references, source indexes, lecture notes, lab activities, problem set, solution key, assessment instructions, review feedback, dependencies, high standards, resubmission, and final assembly.

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
- `course-index.template.html` for the course folder landing page created during final assembly.

These templates enforce consistent look-and-feel, structure, accessibility, and reference discipline. They do not enforce a particular lecture trajectory; each authoring stage should shape the trajectory of slides, notes, labs, and problem sets to best meet the learning objectives and scientific dependencies of the course.

## Course Folder and File Naming Convention

Place every generated course package under `materials/<COURSECODE>/`, where `<COURSECODE>` removes spaces from the catalog number and preserves uppercase subject letters, for example `materials/ASTR101/`.

Use this structure consistently across all courses:

```text
materials/<COURSECODE>/
	index.html
	README.md
	course-manifest.json
	syllabus.html
	schedule.html
	reference-log.md
	lectures/
		lecture-01-slides.html
		lecture-01-notes.html
		lecture-02-slides.html
		lecture-02-notes.html
	labs/
		lab-01.html
		lab-02.html
	problem-sets/
		problem-set-01.html
		problem-set-01-solutions.html
		problem-set-01-assessment.md
	data/
		README.md
	src/
		README.md
```

Use two-digit numbering for lectures, labs, and problem sets. Place course-specific source code, scripts, notebooks, plotting utilities, data generators, validation tools, and computational examples under `src/`. Place course-specific raw, processed, or synthetic datasets under `data/`, with provenance and license notes. Do not place generated source code or datasets at the repository root.

The orchestrator is responsible for creating `materials/<COURSECODE>/index.html` during final assembly, after the package contents and review status are known. Use `templates/course-materials/course-index.template.html` so all course folders have a consistent landing page that links to the syllabus, schedule, reference log, lecture slides, lecture notes, labs, problem sets, solution keys, assessment instructions, source code, data, and manifest. The index should not imply incomplete artifacts are finished; mark pending items clearly or omit links until files exist.

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
- Whether adopted textbooks or PDFs need lightweight source indexing for exact reading, figure, or problem references.
- Whether the default HTML-with-MathJax workflow should be replaced by LaTeX for print-first or especially math-heavy artifacts.

If the course catalog entry is missing, create a short planning brief first and ask for confirmation unless the user authorizes reasonable assumptions.

## Subagent Coordination Pattern

When subagents are available, use them to isolate work by artifact type. Provide each subagent only the context it needs and require a structured result.

If subagent output is advisory rather than directly written to the workspace, treat it as draft input only. The orchestrating agent must create or update the actual files, run validation, and continue to the next dependency stage.

Recommended assignments:

- Syllabus agent: invoke `CourseSyllabusScheduleAgent` and apply `course-syllabus-schedule`.
- Source index agent: invoke `SourceMaterialIndexAgent` and apply `source-material-indexing` when exact textbook/source references are needed.
- Slides agent: invoke `LectureSlideAuthorAgent` and apply `lecture-slide-authoring` after syllabus approval.
- Visual research agent: invoke `VisualReferenceResearchAgent` when slide or note authors need Creative Commons, public-domain, mission, observatory, dataset, or other externally sourced visuals.
- Notes agent: invoke `LectureNotesAuthorAgent` and apply `lecture-notes-authoring` after slide decks exist.
- Lab agent: invoke `LabAuthorAgent` and apply `lab-authoring` for observing, instrumentation, data-analysis, and computational labs.
- Problem set agent: invoke `ProblemSetAssessmentAgent` and apply `problem-set-assessment` after notes exist.
- Review agent: invoke `CourseMaterialsReviewAgent` and apply `course-materials-review` after a coherent package exists.

Do not use a read-only exploration agent for production. Exploration agents may gather context, but course material creation and review should use the custom production agents above or be completed directly by the orchestrating agent.

Require each subagent to report:

- Artifacts created or changed.
- Assumptions made.
- References requiring verification.
- Issues to send backward to earlier stages.
- Readiness status for the next dependency stage.

Do not stop after a planning handoff. Continue until the requested package scope is complete, blocked by a concrete missing requirement, or explicitly paused by the user.

## Reviewer-Driven Correction Loop

When review identifies defects, use this deterministic loop:

1. Convert each reviewer finding into a tracked correction item with artifact owner, affected files, required action, and re-review criteria.
2. Assign the item to the relevant production agent or handle it directly:
	- syllabus/schedule issues -> `CourseSyllabusScheduleAgent`
	- slide depth, visuals, captions, or student-facing language -> `LectureSlideAuthorAgent`
	- visual/source candidates -> `VisualReferenceResearchAgent`
	- exact textbook/source indexing -> `SourceMaterialIndexAgent`
	- lecture note depth or alignment -> `LectureNotesAuthorAgent`
	- lab specificity, apparatus, measurement, uncertainty, or provenance -> `LabAuthorAgent`
	- problem specificity, textbook references, solutions, rubrics -> `ProblemSetAssessmentAgent`
	- validation of fixes -> `CourseMaterialsReviewAgent`
3. If external visuals are needed, first create a candidate list with source URL, creator/institution, license or usage note, caption context, lecture fit, and verification status. Then send that candidate list to review before inserting visuals into student materials.
4. Apply approved corrections only. Rejected candidates or fixes should be replaced and re-reviewed.
5. Run focused validation after each correction batch.
6. Update `review-report.md`, `course-manifest.json`, and `index.html` so package status matches reviewer status.
7. Repeat until review approval or a concrete blocker, such as unavailable source access or unverifiable licensing, is recorded.

## Workflow

### 1. Plan the Package

- Identify the expected artifact tree.
- Determine the number of lectures, labs, and problem sets.
- Decide naming conventions.
- Create or update `materials/<COURSECODE>/course-manifest.json` to list planned artifacts, dependencies, status, and source/data paths.
- Confirm the review criteria and resubmission policy.

### 2. Create Syllabus and Schedule

- Apply `course-syllabus-schedule`.
- Validate assessment weights, prerequisites, lecture order, lab placement, and resource list.
- Do not proceed until the syllabus/schedule is internally coherent.

### 3. Create Slides

- Apply `lecture-slide-authoring` lecture by lecture or module by module.
- Ensure every deck follows the schedule and contains verified visual/reference information.
- Ensure each lecture deck has enough depth for the intended meeting length. For a typical 60-minute lecture, reject decks that merely populate template sections with brief generic bullets.
- Use adopted textbooks, local reference copies, or verified readings to ground scope and terminology.
- Use `VisualReferenceResearchAgent` or equivalent verification before incorporating Creative Commons, public-domain, mission, observatory, or other external visuals.
- If slide authoring exposes schedule defects, return to Step 2.

### 4. Create Lecture Notes

- Apply `lecture-notes-authoring` to each lecture after its slide deck exists.
- Ensure notation, examples, references, and assumptions match the slides.
- Ensure notes are study-ready and expand the slide content; do not accept notes that simply restate slide bullets.
- If notes expose slide defects, return to Step 3; if they expose sequence defects, return to Step 2.

### 4a. Create Labs and Observing Activities

- Apply `lab-authoring` for each scheduled lab, observing, computational, instrumentation, or data-analysis activity.
- Ensure each lab has concrete apparatus/setup, procedure, measurement record, analysis and uncertainty, deliverables, assessment criteria, and provenance.
- If lab writing exposes missing datasets, equipment constraints, safety concerns, or schedule defects, route backward to the appropriate stage.

### 5. Create Problem Sets and Grading Materials

- Apply `problem-set-assessment` for each lecture or scheduled problem set.
- Keep student problem sets, solution keys, and agent assessment instructions separate.
- Ensure problem difficulty is high but fair and tied to taught material.
- If problem writing exposes defects in notes, slides, or schedule, route backward.

### 6. Review the Package

- Apply `course-materials-review` to the assembled materials.
- Treat scientific errors, hallucinated references, inconsistent solutions, broken dependencies, and missing assessment instructions as blocking.
- Send materials back to the appropriate stage with concrete feedback.
- Do not treat partial scripted validation as reviewer approval. Scripted validation may prove file counts, links, or marker absence, but the review agent must evaluate content quality.

### 7. Correct and Re-review

- Apply corrections at the originating stage.
- Regenerate dependent downstream artifacts when changes alter content, notation, schedule, or assessment.
- Re-run review on changed artifacts and their dependents.

### 8. Final Assembly

- Create or update `materials/<COURSECODE>/index.html` using `templates/course-materials/course-index.template.html` after review status and artifact availability are known.
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
- Adopted textbook copies stored under `references/` may be used for local grounding and chapter mapping, but generated materials must still cite the source and avoid unmarked long copied passages.
- Lightweight source indexes under `references/source-indexes/` may be created when exact sections, figures, or problem numbers are needed. They support verification but do not replace human spot-checking of the adopted edition before instructional use.

## Completion Criteria

A course package is complete only when:

- All required artifacts exist.
- Dependencies were followed or documented.
- A review pass approved the package or clearly identified remaining limitations.
- References and visuals are verified or flagged.
- Student-facing and instructor-facing materials are separated where needed.
- `index.html` exists, uses the course index template, and accurately links only to available or clearly marked pending artifacts.
- The final summary identifies what was produced and what remains for human review.
