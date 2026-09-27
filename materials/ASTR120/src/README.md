# ASTR 120 Source

Scripts for generating plots, validating data, and rebuilding course artifacts belong here.

## Active terminology workflow

Run `python materials/ASTR120/src/upgrade_astr120_terminology.py` from the
repository root to rebuild and validate the accessible term explorers in all
14 lecture decks and the matching `Terms Developed in Context` sections in
the notes. Use `--validate-only` to check the generated pairings without
rewriting files.

The older full-package generation and polishing scripts document earlier
production passes. Do not rerun them for terminology maintenance: they
regenerate broader course artifacts and can overwrite later authored content.
