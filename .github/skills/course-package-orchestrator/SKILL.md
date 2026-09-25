---
name: course-package-orchestrator
description: "Use when: coordinating subagents or staged workflows to produce a complete undergraduate astronomy course package from catalog entry to syllabus, lecture schedule, lab schedule, lecture slides, lecture notes, problem set, solution key, assessment instructions, review feedback, correction, and final assembly."
---

# Course Package Orchestrator

Use this skill to coordinate production of a complete course package for any course in the undergraduate astronomy curriculum. Do not create course materials unless the user explicitly asks to produce a course package. This skill manages dependencies among specialized authoring and review skills.

The orchestrating agent remains responsible for end-to-end completion. Subagents may be used for isolated drafting, review, or exploration, but they are optional helpers and not a substitute for completing, validating, correcting, and assembling the course package. If subagents are unavailable, read-only, incomplete, or return only advisory output, the orchestrating agent must continue the workflow directly from the current artifact state.

When using a custom agent entry point, invoke `CoursePackageOrchestrator` for this workflow.

The orchestrator has agency to keep the process moving through reviewer-designated issues. After any review returns `Needs correction`, the orchestrator must classify each issue by owner, delegate or perform the correction, validate the changed artifacts, and re-run review. Continue this loop until the reviewer explicitly returns `Approved for review release` or the requested release stage is otherwise blocked by a concrete external constraint. Do not stop after file counts validate, after a draft package is created, or after a structural check passes; the loop ends only at review approval for the target release stage.

## Review-Release Quality Floor

`Approved for review release` is a quality gate, not a template-completion milestone. A package must meet the quality floor established by the reviewed ASTR101 and ASTR120 packages before approval. The benchmark is not merely "complete." It is: lecture-specific explanations, evidence-rich slide decks, concrete quantitative reasoning, lecture-appropriate depth, concrete labs, concrete and non-generic problem sets, verified references, and visually legible student-facing artifacts.

If a package is only structurally complete but substantively shallow, the reviewer is instructed to return `Needs correction`. The orchestrator must not treat template completion as review-release approval, even when counts, manifest entries, and HTML links all validate.

Any course that does not meet the ASTR101/ASTR120 benchmark must remain in the correction loop until a reviewer can reasonably defend its approval. This rule applies to all courses, including 200-level materials and later revisions.

Before drafting the first lecture of a new course, read the full `review-report.md` of at least one prior approved benchmark course (not just its templates or final structure) so the depth, specificity, and data-provenance standard is internalized before writing, not discovered during correction. A course engineered from the outset to the benchmark reaches approval faster than one that is corrected into shape after a shallow first pass.

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

## Specificity and Delegation Standards

Do not allow generic or template-level generation to count as course content. The orchestrator must require substantive specificity from every production stage:

- When an adopted textbook is available, first use `SourceMaterialIndexAgent` and require chapter/section-level or exact problem-level references before slides, notes, or problem sets cite the source.
- Problem sets must be concrete and lecture-specific, with exact figures, quantities, scenarios, or datasets, not generic prompts.
- Lab activities must include step-by-step apparatus/setup, data collection, calculations, uncertainty treatment, and deliverables.
- Lecture slides and notes must contain lecture-specific explanation, evidence, worked examples, and quantitative reasoning, not template bullets.
- If a specialized agent does not produce sufficiently specific content, the orchestrator must rewrite or directly improve the artifact instead of accepting a generic pass.
- Compute every worked example, sample calculation, or numeric result shown in lectures, labs, or problem sets with a script rather than hand-typed arithmetic, and reuse the same underlying constants/data across the lecture, lab, and problem set that reference the same scenario, so numbers stay internally consistent and arithmetic errors cannot creep in silently.
- Before defaulting to synthetic or "instructor-provided" placeholder data for a lab or problem set, check whether real, verifiable local data already exists (e.g., the user's own observing/imaging archives, institutional datasets, or other workspace files) and ground the artifact in it instead, with exact file, instrument, and provenance citations.
- Label the provenance of every real-world dataset or measurement at one of three explicit levels, and disclose the level in `reference-log.md`: (1) live-verified this session (fetched or extracted directly from a primary/authoritative source during production), (2) standard published/literature or textbook value presented from training knowledge but not independently re-verified this session (flag for human spot-check against a named catalog or source), or (3) synthetic/instructor-provided placeholder. Do not present level-2 values as if they were level-1, and do not label real literature values as "synthetic" merely because they were not re-fetched.
- When a lab/problem-set count does not match the lecture count 1:1, or does match but the cadence choice is not obvious, document the cadence rationale explicitly in `syllabus.html` (see the ASTR210 biweekly-cadence and ASTR230 matched-cadence precedents).

The orchestrator is responsible for a quality floor, not a file-count milestone.

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

The orchestrator is responsible for creating `materials/<COURSECODE>/index.html` during final assembly, after the package contents and review status are known. Use `templates/course-materials/course-index.template.html` so all course folders have a consistent landing page that links to the syllabus, schedule, reference log, lecture slides, lecture notes, labs, problem sets, solution keys, assessment instructions, source code, data, and manifest. The index should not imply incomplete artifacts are finished; mark pending items clearly or omit links until files exist. Every lecture-slide/notes link must include the lecture's title alongside its number (see Final Assembly below).

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
11. Continuous improvement and handoff (see below) before moving to the next course.

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
- Source index agent: invoke `SourceMaterialIndexAgent` and apply `source-material-indexing` when exact textbook/source references are needed. This stage is mandatory before citing reading or problem recommendations from an adopted textbook if the artifact must be specific.
- Slides agent: invoke `LectureSlideAuthorAgent` and apply `lecture-slide-authoring` after syllabus approval.
- Visual research agent: invoke `VisualReferenceResearchAgent` when slide or note authors need Creative Commons, public-domain, mission, observatory, dataset, or other externally sourced visuals.
- Notes agent: invoke `LectureNotesAuthorAgent` and apply `lecture-notes-authoring` after slide decks exist.
- Lab agent: invoke `LabAuthorAgent` and apply `lab-authoring` for observing, instrumentation, data-analysis, and computational labs. Do not accept generic lab templates or title-only variants.
- Problem set agent: invoke `ProblemSetAssessmentAgent` and apply `problem-set-assessment` after notes exist. Do not accept generic prompts or vague chapter recommendations.
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
- Every lecture link in `index.html` (and any other generated index/schedule listing lectures) must include the lecture's actual title, not just its number, e.g. `Lecture 01: <Title> — slides`. Pull the title from the lecture's own content (its slide deck heading) rather than retyping it, so the link text cannot drift out of sync with the actual lecture.
- Link the newly created or updated course package from the repository-wide navigation: add or update the course's entry under "Course Calendar Entries" in `astronomy_curriculum.html` to link to `materials/<COURSECODE>/index.html`, and add or update the corresponding row in the "Four-Year Course List" schedule table in the same file so the course name links to the same index page. Do this as soon as a course package exists, even if it is only partially complete, and update the link text/status if the review status changes.
- Do not add or maintain a "Course Materials" section in the repository root `index.html` that enumerates individual course packages by card; that listing does not scale as courses are added. The root `index.html` should link to `astronomy_curriculum.html` as the single place course packages are discoverable, plus repository-wide metadata (templates, style guide) that is not course-specific.
- Produce a release summary listing all artifacts, assumptions, verified references, unresolved risks, and recommended next review steps.
- Do not claim completion without a fresh review result.
- Before declaring a course complete, verify a concrete checklist of expected files actually exists on disk: `syllabus.html`, `schedule.html`, `reference-log.md`, `course-manifest.json`, `index.html`, `review-report.md`, `data/README.md`, every `lectures/lecture-NN-{slides,notes}.html`, every `labs/lab-NN.html`, and every `problem-sets/problem-set-NN{.html,-solutions.html,-assessment.md}`. A long production run can end mid-way through final assembly (content generated but wrap-up files never created) without any error being raised; a `course-manifest.json` that already claims "approved for review release" is not sufficient evidence that `index.html` and `review-report.md` actually exist. Do not trust a self-reported status field over the actual file listing.
- When a course's `index.html` (or any other final-assembly file) is built by adapting a prior course's file as a structural template, verify afterward that every course-specific string was actually substituted: check the `<title>` tag, the header `<h1>`/status line, and any generator-script filenames referenced, for leftover references to the prior course's number. A raw data-structure dump (e.g., a Python dict's `str()` representation) appearing in rendered HTML is also a sign that a template substitution was done incorrectly.

### 9. Continuous Improvement and Handoff

Once the review agent has genuinely returned `Approved for review release`, before moving to another course:

- Review the just-completed production and review cycle for concrete, generalizable lessons: recurring defect classes the reviewer caught (e.g., a specific type of arithmetic/unit error), data-provenance judgment calls that were not clearly covered by existing rules, cadence or structural decisions that needed ad hoc justification, or any point where existing skill/agent instructions were ambiguous or insufficient and had to be resolved by judgment during this course's production.
- If a lesson is genuinely generalizable (would help the next course avoid the same issue or reach approval faster), update the relevant `.github/skills/*/SKILL.md` and `.github/agents/*.agent.md` files directly. Do not create new skill files for a single course-specific quirk; prefer small, targeted additions to existing rules.
- Do not invent lessons to pad this step; if the course's production surfaced nothing new beyond what the skills already cover, say so explicitly and skip straight to committing.
- Stage, commit, and push the completed course package together with any skill/agent updates from this step, using a commit message that names the course and summarizes both the content and any skill changes.
- Only after committing and pushing should the orchestrator consider itself ready to begin the next course.

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
