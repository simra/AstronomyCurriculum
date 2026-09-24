# ASTR 310 Generator Scripts

- `generate_astr310_content.py` - defines shared physical constants, the live-verified Alpha Centauri AB/Proxima dataset, standard published comparison datasets (Sirius B carried forward from ASTR230, Io/Jupiter, M15), all derivation-relevant helper functions (Stefan-Boltzmann, Wien, Kepler's third law, escape velocity, hydrostatic/virial estimators, Roche limit, Eddington luminosity, vis-viva), the 14 lecture-content dictionaries, and the HTML rendering functions for lecture slides/notes.
- `generate_astr310_labs_psets.py` - imports the shared constants and helpers above; defines 7 lab builders and 7 problem-set builders (each with a paired solution key and assessment-instructions file).

Run in order from the workspace root:

```
python materials/ASTR310/src/generate_astr310_content.py
python materials/ASTR310/src/generate_astr310_labs_psets.py
```

Every worked numeric example in every lecture, lab, and problem set is computed by these scripts, not hand-typed; regenerate the HTML/Markdown output after any change to a constant or dataset.
