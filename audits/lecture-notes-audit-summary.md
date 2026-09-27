# Curriculum-Wide Lecture Notes Supplementarity Audit

## Scope

This summary consolidates the pairwise baseline audits of all 252 lecture-note files and their matching slide decks across 18 courses. The detailed audits used immutable commit `7a8dd53d1a73e4dc74321615337487438a06e962` so concurrent term-explorer updates did not alter the baseline findings.

- [ASTR101-ASTR320 detailed audit](lecture-notes-audit-101-320.md)
- [ASTR330-ASTR410 detailed audit](lecture-notes-audit-330-410.md)
- [ASTR420-ASTR476 detailed audit](lecture-notes-audit-420-476.md)

## Curriculum-Wide Verdict

| Verdict | Lecture pairs | Share |
|---|---:|---:|
| Meets supplementarity standard | 0 | 0.0% |
| Needs targeted expansion | 18 | 7.1% |
| Needs substantial rewrite | 234 | 92.9% |
| **Total** | **252** | **100%** |

The audit verdict is **Needs correction**. The notes generally preserve slide order and repeat the same claims, equations, examples, cautions, and activity prompts rather than functioning as independent-study companions.

The 18 targeted-expansion cases are eight ASTR120 lectures and ten ASTR474 lectures. Every other audited pair requires substantial redevelopment under the new lecture-notes review standard.

## Highest-Priority Findings

1. **Near-paraphrase is systemic.** Most notes mirror the deck section by section, often verbatim or with only connective prose added.
2. **Derivations and worked reasoning are incomplete.** Equations and numerical anchors are commonly repeated without intermediate steps, unit analysis, assumptions, limiting cases, uncertainty, or a distinct transfer example.
3. **Term development was absent in the baseline.** Static vocabulary cards or missing vocabulary sections did not provide selectable explanations, and notes typically repeated terms without defining their use, relationships, or boundaries.
4. **Resources are rarely actionable.** Broad chapter ranges, bare paths, and vague mission or software references do not tell students what to read, inspect, calculate, reproduce, or compare.
5. **Student-facing voice is inconsistent.** Many notes contain instructor directions, timing cues, generator details, review commentary, provenance-session language, or unresolved production placeholders.
6. **Copied content propagates correctness defects.** The detailed reports identify numerical, unit, equation, interpretation, visual-label, and provenance errors that appear in both slides and notes.
7. **Upper-division depth is insufficient.** Many 300- and 400-level notes lack the mathematical, computational, observational, and model-comparison development expected for independent study.

## Recommended Correction Sequence

1. Correct the specific scientific, mathematical, unit, interpretation, and rendering defects identified in the detailed lecture rows.
2. Rewrite the 234 substantial-rewrite notes as study chapters rather than transcripts. For each major concept, add at least three appropriate expansion types: derivation, physical interpretation, a distinct worked example, observational or computational context, historical development, alternative-model comparison, uncertainty/limitations, or an annotated verified resource.
3. Apply targeted additions to the 18 stronger notes while preserving their useful existing derivations and context.
4. Use the newly introduced term explorer as the shared vocabulary contract: every selected deck term must be developed more fully in the notes and connected to an observable, equation, model, neighboring concept, or boundary condition.
5. Add at least one distinct, independently checkable notes-only example or analysis per lecture.
6. Replace vague citations with verified exact resources and a clear student action.
7. Remove instructor, generator, review, and release-process language from student-facing notes.

## Relationship to the Term-Explorer Update

The baseline audit intentionally predates the repository-wide term-explorer implementation. The current working tree now supplies the missing interactive glossary infrastructure and matching term-development sections in all 252 lecture pairs. That update resolves the structural glossary finding, but it does not by itself resolve the broader supplementarity, correctness, derivation, resource, and student-voice findings documented in the detailed reports.
