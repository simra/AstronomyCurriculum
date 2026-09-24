---
name: lab-authoring
description: "Use when: creating or revising concrete astronomy lab, observing, data-analysis, or computational activities with apparatus, procedures, measurements, uncertainty, deliverables, assessment criteria, and provenance."
---

# Lab Authoring

Use this skill to create or revise lab and observing activities for a course package. Labs are not placeholders or demonstrations; they must be runnable student activities with concrete materials, procedures, measurements, analysis, and deliverables.

## Required Inputs

- Approved syllabus and schedule.
- Relevant lecture slides and notes, if already available.
- Course level and student preparation.
- Local equipment, software, observing site, weather constraints, and safety assumptions where known.
- Any required datasets, images, spectra, target lists, instruments, or source materials.

If local equipment or datasets are unknown, make conservative assumptions and mark exact local items as instructor-provided.

## Folder and Naming

Write labs under `materials/<COURSECODE>/labs/` using two-digit names such as `lab-01.html`. Put course-specific code under `materials/<COURSECODE>/src/` and datasets under `materials/<COURSECODE>/data/`.

## Required Lab Sections

Every lab must include:

- Course and lab identity.
- Learning objectives.
- Preparation.
- Materials and data.
- Apparatus and setup.
- Step-by-step procedure.
- Measurement record or data table structure.
- Analysis and uncertainty.
- Deliverables.
- Assessment criteria.
- References, software, and data provenance.

## Quality Standards

- Labs must be specific to the activity. Do not reuse a generic procedure across labs with only the title changed.
- Students must know exactly what to measure, classify, calculate, plot, or observe.
- Include uncertainty treatment appropriate to the level: repeated measurements, measurement error, classification ambiguity, calibration limits, or model assumptions.
- Observing labs must include safety, weather, site, target, and reproducibility considerations.
- Data labs must identify source, access date, processing state, license or usage terms, and whether data are real, synthetic, or instructor-provided.
- Computational labs must identify software, input files, expected outputs, validation checks, and reproducibility expectations.

## Review Checklist

Before finishing, verify:

- The lab aligns with the lecture schedule and prerequisites.
- The procedure is executable without hidden instructor knowledge, except where explicitly marked as instructor-provided.
- Measurement and analysis requirements are concrete.
- Deliverables match assessment criteria.
- Provenance is recorded for images, spectra, datasets, software, and target lists.
