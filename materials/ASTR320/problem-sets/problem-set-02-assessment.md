# Assessment Instructions: Problem Set 02 — Interior Structure and Heat Budgets

## Inputs to Inspect
Student submission, this problem set, the solution key, the corresponding lecture slides/notes, and the shared
constants in `materials/ASTR320/src/generate_astr320_content.py` where a problem reuses course data.

## Grading Standard
Award credit for correct method and units first, then for the specific numeric result. A student who shows correct
reasoning with a small arithmetic slip should receive most of the available credit; a student with a correct-looking
number but no visible derivation steps should not. Because this is a 300-level quantitative course, full marks require
a genuine derivation (not just formula substitution) wherever the problem set asks for one.

## Problem-Level Criteria
- Problem 1: both percent-deviation values must be computed and correctly compared.
- Problem 2: correct exponential-decay direction (looking backward in time uses e^{+lambda t}, not e^{-lambda t}) is required.
- Problem 3: answer must explicitly name tidal heating/orbital resonance as the resolving mechanism, not a vague reference to "different composition."
- Problem 4: cubic scaling must be shown explicitly (not just stated).
- Problem 5: percent calculation and correct naming of secular cooling both required.

## Resubmission Policy
Students may resubmit within one week of receiving feedback. A resubmission must show a corrected derivation, not
only a corrected final number, and should reference the specific feedback comment it addresses. Regrade to a maximum
of 90% of the original point value unless the error was a grading mistake.

## Common Errors to Flag
- Sign error in the decay-law direction when computing a past abundance rather than a future one (Problem 2).
- Confusing static core-size deviation with dynamic, time-dependent heat flow as though they must always track each other (Problem 3 context).
- Forgetting to cube the ratio in the Rayleigh-number scaling problem (a linear-scaling error).
