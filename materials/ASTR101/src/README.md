# ASTR 101 Source Code

Place course-specific source code here.

Use this folder for:

- Python scripts or notebooks used to generate plots for slides and notes.
- Data-cleaning or validation scripts for lab activities.
- Small simulations or numerical examples.
- Reproducible code supporting problem sets or solution keys.

Do not place generated source code at the repository root. Any code that consumes datasets should document the expected input path under `../data/` and the generated artifact path.

## Active Lecture Generator

- `regenerate_slides_notes_second_pass.py` is the active source for all 14 lecture slide/notes pairs. It imports `term_explorer_content.py` for the lecture-specific interactive terminology content.
- Run `validate_term_explorers.py` after regeneration to check the button-panel mapping, unique IDs, ARIA relationships, initial state, print fallback, HTML parsing, and exact notes coverage.
- `generate_astr101_assets.py` is the older first-pass package generator. Do not use it to regenerate lectures because it predates the second-pass depth and terminology upgrades.
