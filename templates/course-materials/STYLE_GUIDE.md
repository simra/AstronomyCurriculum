# Course Materials Style Guide

Use this guide for all generated course artifacts: syllabi, schedules, lecture slides, lecture notes, problem sets, solution keys, and assessment instructions.

The templates are presentation scaffolds for consistent look-and-feel, artifact structure, accessibility, and source tracking. They do not enforce a particular lecture trajectory, conceptual order, or pedagogical storyline. Shape the trajectory of slides, notes, labs, and problem sets to best meet the course learning objectives, prerequisite background, and scientific logic of the topic.

## Format Recommendation

Default to HTML with MathJax for reviewable web artifacts. Use LaTeX when the requested deliverable is a print-first packet, a mathematically dense handout, an exam, or a publication-quality PDF.

For this curriculum, the recommended default is a hybrid workflow:

- Author syllabi, slide decks, lecture notes, problem sets, and solution keys in HTML templates using MathJax for equations.
- Keep notation, equation numbering, references, and figure credits disciplined enough that selected artifacts can later be converted to LaTeX/PDF if needed.
- Use LaTeX source for especially equation-heavy derivations, exams, or handouts when typographic precision is more important than browser presentation.

## Visual Identity

Use a consistent academic visual identity across courses:

- Tone: rigorous, calm, precise, and research-oriented.
- Layout: readable, uncluttered, and optimized for sustained study.
- Palette: deep navy, off-white, muted teal, warm gold, and neutral gray.
- Typography: serif for long-form notes and syllabi; clean sans-serif for slide headings and interface-like elements.
- Avoid decorative space imagery unless it directly supports a scientific point.

Suggested CSS variables:

```css
:root {
  --ink: #17202a;
  --muted: #5b6773;
  --paper: #fbfcfd;
  --panel: #ffffff;
  --line: #d9e0e7;
  --navy: #102a43;
  --teal: #0f6b78;
  --teal-soft: #e5f4f6;
  --gold: #b87911;
  --warning: #8a4b08;
}
```

## Document Structure

Every student-facing artifact should include:

- Course number and title.
- Artifact type and title.
- Lecture, week, module, or assignment number where applicable.
- Learning objectives.
- Required preparation or prerequisites for the artifact.
- Main content organized with clear headings.
- References, data sources, and visual credits.
- Revision date or version.

Every instructor-facing artifact should additionally include:

- Internal assumptions.
- Dependencies on earlier artifacts.
- Known verification status for references, visuals, and data.
- Rubrics, solution notes, or assessment criteria where applicable.

## Math Standards

Use MathJax-compatible LaTeX syntax in HTML:

- Inline math: `\( F = ma \)`.
- Display math: `\[ E = \int_0^\infty F_\nu\,d\nu \]`.
- Number equations only when later text refers to them.
- Define variables immediately after first use.
- Include units in examples and final answers.
- State approximations, coordinate systems, and assumptions.
- Keep notation consistent across slides, notes, problem sets, and solution keys.

## Figures, Visuals, and Data

- Every non-original figure must have a verified source and credit.
- Every plot must label axes, units, scale, and data source.
- Distinguish real data, simulated data, schematic diagrams, and artist renderings.
- Do not use image URLs, papers, datasets, or mission facts that have not been verified.
- Maintain a reference log using `reference-log.template.md`.

## Accessibility and Usability

- Use semantic HTML headings in order.
- Provide alt text or adjacent descriptions for figures.
- Avoid relying on color alone to communicate meaning.
- Keep contrast high and text sizes readable.
- Tables should have headers and concise captions when needed.
- Slide decks should remain usable when printed or exported to PDF.

## Grading and Resubmission Tone

Use high standards and clear feedback. Student-facing language should state that revisions and resubmissions are encouraged to improve mastery and grade, while instructor-facing rubrics should preserve demanding expectations for reasoning, units, evidence, reproducibility, and communication.
