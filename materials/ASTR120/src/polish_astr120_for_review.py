from __future__ import annotations

import json
from html import escape
from pathlib import Path

CSS = """
:root { --ink:#17202a; --paper:#fbfcfd; --panel:#fff; --line:#d9e0e7; --navy:#102a43; --teal:#0f6b78; --teal-soft:#e5f4f6; --gold:#b87911; }
body { margin:0; font-family:Georgia,"Times New Roman",serif; color:var(--ink); background:var(--paper); line-height:1.6; }
header { padding:38px 24px 26px; background:linear-gradient(135deg,var(--navy),var(--teal)); color:#fff; }
header div, main { max-width:1060px; margin:0 auto; }
main { padding:30px 24px 64px; }
h1,h2,h3 { line-height:1.15; }
h1 { margin:0 0 8px; font-size:clamp(2rem,4vw,3.2rem); }
h2 { margin-top:34px; color:var(--navy); border-bottom:2px solid var(--line); padding-bottom:8px; }
section, article.problem { background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:16px 18px; margin:16px 0; }
.points { color:var(--gold); font-weight:700; }
code { background:#eef3f5; padding:1px 4px; border-radius:3px; }
"""

ROOT = Path(__file__).resolve().parents[1]
LECTURES_DIR = ROOT / "lectures"
LABS_DIR = ROOT / "labs"
PSETS_DIR = ROOT / "problem-sets"

LECTURE_FIXES = {
    1: dict(evidence=["Earth can be studied as a planet with atmosphere, surface, water, and interior.", "Spacecraft turned point-like planets into measurable worlds.", "Comparing many worlds reveals which processes are general."], equation="scale ratio = model distance / real distance", q="Use scale ratios to keep sizes, distances, and light-time in the same model.", example="If Earth is a 1 cm marble, the Moon is about 30 cm away; this makes the emptiness of planetary systems tangible."),
    2: dict(evidence=["Planet orbits are nearly coplanar and mostly prograde.", "Rocky and volatile-rich bodies separate with distance from the Sun.", "Meteorites preserve early solids from the disk."], equation="orbital angular momentum is conserved as disk material collapses", q="Use the frost line and angular momentum to explain broad architecture without overfitting details.", example="Inside the frost line, silicates and metals dominate solids; outside, ices increase solid mass available for core growth."),
    3: dict(evidence=["Orbital period increases strongly with semi-major axis.", "Mean-motion resonances appear among moons, rings, and small bodies.", "Tidal flexing can heat interiors."], equation="P^2 = a^3", q="Use period ratios and semi-major axes to identify resonance or Keplerian scaling.", example="A 2:1 resonance means the inner body completes two orbits while the outer completes one."),
    4: dict(evidence=["Mean density differs among rocky, icy, and gas-rich worlds.", "Magnetic fields imply conducting interiors and motion.", "Heat flow and volcanism reveal interior energy."], equation="rho = M / (4 pi R^3 / 3)", q="Density is an average clue, not a full interior model.", example="A moon with density near 1.9 g/cm^3 likely contains substantial ice mixed with rock."),
    5: dict(evidence=["Cratered highlands preserve older surfaces.", "Smooth plains can indicate lava flooding or resurfacing.", "Tectonic features record stress and interior evolution."], equation="relative age increases with crater density when preservation is comparable", q="Use crater density only after checking image scale and resurfacing processes.", example="A smooth volcanic plain with few craters is younger than a nearby saturated crater field at the same resolution."),
    6: dict(evidence=["Venus, Earth, and Mars have different atmospheric pressures and greenhouse histories.", "Escape depends on gravity, temperature, and molecular mass.", "Albedo changes absorbed solar energy."], equation="absorbed sunlight is proportional to (1 - albedo) / distance^2", q="Compare energy input, greenhouse trapping, and atmospheric loss separately.", example="Venus receives more sunlight than Earth, but its extreme surface temperature requires greenhouse trapping by a dense CO2 atmosphere."),
    7: dict(evidence=["Airless surfaces retain craters and space-weathered regolith.", "Mercury has high density and a large metal fraction.", "Lunar samples anchor crater chronology."], equation="impact rate plus crater density gives a relative surface clock", q="Use crater counts as relative ages, not absolute ages without calibration.", example="Bright crater rays suggest fresh material excavated recently compared with darker mature regolith."),
    8: dict(evidence=["Valley networks, deltas, and hydrated minerals point to past water.", "Current Mars has low pressure and cold mean temperature.", "Rover measurements provide ground truth for orbital interpretations."], equation="evidence strength increases when landforms + minerals + stratigraphy agree", q="Treat water evidence as a convergence of independent observations.", example="A fan-shaped delta plus clay minerals is stronger evidence for persistent water than a channel shape alone."),
    9: dict(evidence=["Jupiter and Saturn emit more energy than they receive from the Sun.", "Belts, zones, and storms show fluid dynamics.", "Magnetospheres reveal conducting interiors and rapid rotation."], equation="v_escape = sqrt(2GM/R)", q="Escape speed and low temperature help explain volatile retention.", example="Jupiter's high escape speed helps it retain hydrogen and helium over solar-system time."),
    10: dict(evidence=["Io's volcanoes, Europa's fractures, and Enceladus' plumes all point to tidal energy.", "Rings are thin, structured, and dynamically young in places.", "Titan has a dense atmosphere and organic chemistry."], equation="tidal heating depends on orbital eccentricity and interior flexing", q="Compare energy source, liquid environment, and chemistry for ocean-world claims.", example="Europa and Io are both tidally heated, but one expresses energy through ice deformation while the other through volcanism."),
    11: dict(evidence=["Meteorite chemistry preserves primitive and differentiated materials.", "Comet activity reveals volatile sublimation.", "DART demonstrated measurable asteroid deflection."], equation="impact energy = 1/2 m v^2", q="Velocity matters strongly because impact energy scales with speed squared.", example="Doubling impact speed quadruples kinetic energy for the same mass."),
    12: dict(evidence=["Hot Jupiters exist very close to their stars.", "Transit and radial velocity methods favor different planets.", "Compact multi-planet systems challenge simple solar-system analogies."], equation="transit depth is approximately (R_planet / R_star)^2", q="Detection method shapes the planet sample before interpretation begins.", example="A Jupiter-size planet blocks about 1 percent of a Sun-like star; Earth blocks about 0.01 percent."),
    13: dict(evidence=["Liquid water, energy sources, and chemistry are all required for habitability.", "Biosignatures require planetary context.", "Planetary protection prevents false positives and contamination."], equation="habitability claim = environment + energy + chemistry + context", q="Do not equate habitable zone with inhabited world.", example="Oxygen plus methane is more interesting than either alone, but geology and photochemistry must be ruled out."),
    14: dict(evidence=["Science traceability links question, measurement, instrument, and trajectory.", "Mission design trades risk, cost, resolution, and coverage.", "A payload should test a hypothesis, not just take pretty pictures."], equation="science question -> measurement -> instrument -> mission design", q="A mission is a chain of constraints built around a testable question.", example="Testing for an ocean may require magnetometry, gravity, plume sampling, or repeat imaging depending on the target."),
}

PSETS = {
    1: [("Disk temperature and composition", "Explain why rocky planets dominate the inner solar system while ice-rich bodies are common farther out. Include the frost line and one limitation of the model.", "Strong answers connect condensation temperature, disk radius, and later mixing/migration."), ("Kepler scaling", "A small body orbits at 3.0 AU. Estimate its orbital period in years and compare it with Mars and Jupiter.", "P^2=27, so P=5.2 yr; this is longer than Mars and near Jupiter's orbital scale but still inside Jupiter's orbit.")],
    2: [("Mean density", "World A has 0.815 Earth masses and 0.949 Earth radii. Compute density relative to Earth and interpret.", "rho/rho_E=0.815/0.949^3=0.95, broadly Earth-like mean density."), ("Crater surface age", "Two regions have 120 and 15 craters in equal areas. Which is older and what assumption matters?", "The 120-crater region is older if impact rate, preservation, and resurfacing are comparable.")],
    3: [("Atmospheric retention", "Compare escape velocity qualitatively for Mars and Earth using mass/radius differences. Which better retains atmosphere?", "Earth's larger mass and radius combination yields higher escape speed; retention is stronger, though temperature and chemistry matter."), ("Albedo", "If two planets receive the same sunlight but one has higher albedo, which absorbs less energy and why?", "Higher albedo reflects more, lowering absorbed energy.")],
    4: [("Mars water evidence", "Rank valley networks, hydrated minerals, recurring slope lineae, and polar ice as evidence for past or present liquid water. Justify.", "Best answers separate past/present and direct/indirect evidence."), ("Delta interpretation", "Why is a delta stronger evidence for sustained liquid flow than an isolated channel?", "Deltas require sediment transport into standing water over time.")],
    5: [("Tidal heating", "Explain why Io can be volcanically active despite its small size.", "Orbital resonance maintains eccentricity; tidal flexing dissipates energy as heat."), ("Ring dynamics", "Why do narrow rings imply confinement or replenishment?", "Collisions and spreading would broaden rings without shepherding, resonance, or replenishment.")],
    6: [("Impact energy", "A projectile's speed doubles while mass stays fixed. How does kinetic energy change?", "It increases by a factor of four."), ("Transit depth", "Estimate transit depth for a Jupiter-size planet around a Sun-like star using R_J/R_Sun ≈ 0.1.", "Depth ≈0.1^2=0.01, or 1 percent.")],
    7: [("Mission traceability", "Design a mission measurement for Europa ocean evidence. State question, measurement, instrument, and uncertainty.", "Possible chain: ocean? induced magnetic field; magnetometer; ambiguity from ionosphere/plasma environment."), ("Habitability claim", "A press release says 'possibly habitable.' List four measurements needed before taking the claim seriously.", "Orbit/insolation, radius/mass/density, atmosphere, water/chemistry, stellar activity context.")],
}

def page(title, body, css=CSS):
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{escape(title)}</title><script id='MathJax-script' async src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script><style>{css}</style></head><body>{body}</body></html>"

def li(items): return ''.join(f"<li>{escape(str(x))}</li>" for x in items)

def replace_section(text, heading, html):
    start = text.index(f"<section class=\"slide\"><h2>{heading}</h2>")
    end = text.index("</section>", start) + len("</section>")
    return text[:start] + html + text[end:]

for n, fix in LECTURE_FIXES.items():
    path = Path(f"materials/ASTR120/lectures/lecture-{n:02d}-slides.html")
    t = path.read_text(encoding='utf-8')
    evidence = f"<section class=\"slide\"><h2>Evidence We Need</h2><ul>{li(fix['evidence'])}</ul></section>"
    quant = f"<section class=\"slide\"><h2>Quantitative Tool</h2><div class=\"equation\">\\[ {escape(fix['equation'])} \\]</div><p>{escape(fix['q'])}</p></section>"
    worked = f"<section class=\"slide\"><h2>Worked Reasoning</h2><p>{escape(fix['example'])}</p></section>"
    t = replace_section(t, "Evidence We Need", evidence)
    t = replace_section(t, "Quantitative Tool", quant)
    t = replace_section(t, "Worked Reasoning", worked)
    path.write_text(t, encoding='utf-8')

for n, problems in PSETS.items():
    p = Path(f"materials/ASTR120/problem-sets/problem-set-{n:02d}.html")
    rows=''.join(f"<article class='problem'><h3>{i}. {escape(title)} <span class='points'>15 points</span></h3><p>{escape(prompt)}</p></article>" for i,(title,prompt,sol) in enumerate(problems,1))
    p.write_text(page(f"ASTR 120 Problem Set {n:02d}", f"<header><div><h1>Problem Set {n:02d}</h1><p>Concrete solar-system reasoning</p></div></header><main><section><h2>Problems</h2>{rows}</section><section><h2>OpenStax Practice</h2><p>Use the source index under <code>references/source-indexes/</code> to verify exact companion problems before instructional assignment.</p></section></main>"), encoding='utf-8')
    s = Path(f"materials/ASTR120/problem-sets/problem-set-{n:02d}-solutions.html")
    solrows=''.join(f"<article class='problem'><h3>{i}. {escape(title)}</h3><p>{escape(sol)}</p></article>" for i,(title,prompt,sol) in enumerate(problems,1))
    s.write_text(page(f"ASTR 120 Problem Set {n:02d} Solutions", f"<header><div><h1>Problem Set {n:02d} Solution Key</h1></div></header><main><section><h2>Worked Solutions</h2>{solrows}</section></main>"), encoding='utf-8')

# Update status to pending review after corrections.
manifest = Path('materials/ASTR120/course-manifest.json')
data = json.loads(manifest.read_text(encoding='utf-8'))
data['status']={'stage':'needs correction pending review','reviewStatus':'Needs correction pending review; not approved for instructional use','lastUpdated':'2026-09-23'}
manifest.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
Path('materials/ASTR120/review-report.md').write_text('# ASTR 120 Course Materials Review Report\n\nStatus: Needs correction pending review; not yet approved for instructional use.\n\nSecond-pass corrections added lecture-specific evidence, quantitative tools, and concrete problem sets.\n', encoding='utf-8')
idx = Path('materials/ASTR120/index.html')
t = idx.read_text(encoding='utf-8').replace('Approved for review release; not yet approved for instructional use.', 'Needs correction pending review; not yet approved for instructional use.')
idx.write_text(t, encoding='utf-8')
print('polished ASTR120 second pass')
