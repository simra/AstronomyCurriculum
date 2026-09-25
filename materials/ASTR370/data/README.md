# ASTR 370 Data

Generated CSV datasets, produced by `../src/generate_astr370_content.py`. Regenerate with:

```
python materials/ASTR370/src/generate_astr370_content.py
```

## Files

- `solar_cycle_sunspot_numbers.csv` — Solar Cycle 24/25 sunspot-number figures (SILSO/WDC-SILSO). Cycle 25 values are live-verified this session; Cycle 24 value is a standard published, level-2 figure. See `../reference-log.md`.
- `real_events.csv` — The 6 September 2017 AR12673 X9.3 flare/CME/storm case study, the historic Carrington Event's Dst range and CME transit time, and Parker Solar Probe's perihelion/record-speed facts, each with a source-note column indicating live-verified (level 1) vs standard published (level 2) provenance.

## License and Provenance

All values in these CSVs are drawn from real, published solar-physics and heliophysics literature and mission documentation, not synthetic or fabricated. See `../reference-log.md` for the full tri-level provenance disclosure and human spot-check checklist required before instructional use.
