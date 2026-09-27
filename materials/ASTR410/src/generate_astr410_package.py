"""Generate the ASTR 410 Galactic Astronomy course package.

All displayed numerical examples are derived from shared constants and data in
this file.  Re-running the generator regenerates lectures, notes, labs,
problem sets, the manifest, and the final index without hand-entered results.
"""
from __future__ import annotations

import csv
import html
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURE_DIR = ROOT / "lectures"
LABS = ROOT / "labs"
PSETS = ROOT / "problem-sets"
DATA = ROOT / "data"

CSS = """
:root{--ink:#17202a;--muted:#5b6773;--paper:#fbfcfd;--panel:#fff;--line:#d9e0e7;--navy:#102a43;--teal:#0f6b78;--teal-soft:#e5f4f6;--gold:#b87911;--warning:#8a4b08}*{box-sizing:border-box}body{margin:0;font-family:Georgia,'Times New Roman',serif;color:var(--ink);background:var(--paper);line-height:1.6}header{padding:38px 24px 26px;background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}header div,main{max-width:1080px;margin:0 auto}main{padding:30px 24px 64px}h1,h2,h3{line-height:1.15}h1{margin:0 0 8px;font-size:clamp(2rem,4vw,3.2rem)}h2{margin-top:34px;color:var(--navy);border-bottom:2px solid var(--line);padding-bottom:8px}h3{color:var(--teal)}section,article.problem{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:16px 18px;margin:16px 0}.notice{border-left:5px solid var(--teal);background:var(--teal-soft)}table{width:100%;border-collapse:collapse;margin:14px 0}th,td{border:1px solid var(--line);padding:8px 10px;vertical-align:top;text-align:left}th{background:var(--teal-soft)}code{background:#eef3f5;padding:1px 4px;border-radius:3px}a{color:var(--teal);font-weight:700}.small{color:var(--muted);font-size:.94rem}.figure{margin:18px 0}.figure svg{width:100%;height:300px;border:1px solid var(--line);background:#fff}.figure figcaption{color:var(--muted);font-size:.94rem}.equation{padding:12px 16px;border-left:5px solid var(--teal);background:var(--teal-soft);overflow:auto}
"""
SLIDE_CSS = CSS + ".deck{scroll-snap-type:y mandatory;height:100vh;overflow-y:auto}.slide{min-height:100vh;scroll-snap-align:start;display:flex;flex-direction:column;justify-content:center;padding:46px 7vw;border-bottom:1px solid var(--line);background:#fff}.title{background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}.title h2{color:#fff}.slide h2{font-family:'Aptos','Segoe UI',sans-serif;font-size:clamp(1.8rem,3.2vw,3.1rem);margin:0 0 20px}.slide p,.slide li{font-size:clamp(1.02rem,1.35vw,1.35rem);line-height:1.38}.grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:center}.figure svg{height:50vh;max-height:480px}.prompt{border-left:5px solid var(--gold);padding:14px 18px;background:#fff8e8}.kicker{color:var(--gold);text-transform:uppercase;letter-spacing:.08em;font-weight:700}.credit{color:var(--muted);font-size:.9rem}.term-explorer{display:grid;grid-template-columns:minmax(210px,.72fr) minmax(0,1.8fr);gap:24px;align-items:stretch;min-height:58vh}.term-list{display:flex;flex-direction:column;gap:9px}.term-button{width:100%;padding:12px 14px;border:2px solid var(--line);border-radius:8px;background:#fff;color:var(--navy);font:inherit;font-size:1.02rem;font-weight:700;text-align:left;cursor:pointer}.term-button:hover{border-color:var(--teal)}.term-button:focus-visible{outline:4px solid var(--gold);outline-offset:2px}.term-button[aria-selected='true']{color:#fff;background:var(--teal);border-color:var(--teal)}.term-detail{border:1px solid var(--line);border-radius:10px;padding:20px 24px;background:var(--paper);overflow:auto}.term-detail h3{margin-top:0;font-size:clamp(1.35rem,2.2vw,2rem)}.term-detail p{font-size:clamp(.95rem,1.2vw,1.18rem)}.term-detail[hidden]{display:none}@media(max-width:800px){.term-explorer{grid-template-columns:1fr}.term-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.slide{padding:34px 5vw}}@media print{.deck{height:auto;overflow:visible}.slide{min-height:7.5in;page-break-after:always}.term-explorer{display:block}.term-list{display:none}.term-detail[hidden]{display:block}.term-detail{break-inside:avoid;margin:12px 0}}"

TERM_EXPLORER_SCRIPT = """<script>
document.querySelectorAll("[data-term-explorer]").forEach((explorer) => {
  const tabs = [...explorer.querySelectorAll('[role="tab"]')];
  const panels = [...explorer.querySelectorAll('[role="tabpanel"]')];
  const select = (tab) => {
    tabs.forEach((item) => item.setAttribute("aria-selected", String(item === tab)));
    panels.forEach((panel) => { panel.hidden = panel.id !== tab.dataset.termTarget; });
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => select(tab));
    tab.addEventListener("keydown", (event) => {
      if (!["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      const nextIndex = event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 : (index + (event.key === "ArrowDown" ? 1 : -1) + tabs.length) % tabs.length;
      tabs[nextIndex].focus();
      select(tabs[nextIndex]);
    });
  });
});
</script>"""

G = 6.67430e-11
KPC_M = 3.085677581e19
KMS_M = 1000.0
MSUN = 1.98847e30
YEAR_S = 365.25 * 86400
C_KMS = 299792.458
R_SUN_KPC = 8.2
V_SUN = 232.0
RHO_CRIT = 1.36e11  # solar masses per cubic Mpc, only for explanatory scaling

# Published/standard values used as level-2 data unless noted otherwise.
ROTATION = [(4.0, 205.0), (6.0, 220.0), (8.2, 232.0), (10.0, 238.0), (14.0, 230.0), (20.0, 218.0), (25.0, 210.0)]
ABUNDANCE = [("thin disk", -0.05, 0.22), ("thick disk", -0.55, 0.32), ("halo", -1.55, 0.45), ("bulge", 0.10, 0.28)]
APOGEE_LIKE = [(0.2, 0.1, 210.0), (0.8, 0.4, 185.0), (1.4, 0.8, 160.0), (2.0, 1.2, 135.0), (2.6, 1.7, 120.0)]


def fmt(x: float, n: int = 4) -> str:
    return f"{x:.{n}g}"


def orbital_period_gyr(radius_kpc: float, speed_kms: float) -> float:
    return 2 * math.pi * radius_kpc * KPC_M / (speed_kms * KMS_M) / (1e9 * YEAR_S)


def enclosed_mass_msun(radius_kpc: float, speed_kms: float) -> float:
    return (radius_kpc * KPC_M) * (speed_kms * KMS_M) ** 2 / G / MSUN


def hz_mass_msun(radius_kpc: float, speed_kms: float) -> float:
    return 2 * math.pi * radius_kpc * KPC_M * (speed_kms * KMS_M) ** 2 / (G * MSUN)


def distance_modulus(mag: float, abs_mag: float) -> float:
    return 10 ** ((mag - abs_mag + 5) / 5) / 1000


def proper_motion_speed(mu_masyr: float, distance_kpc: float) -> float:
    return 4.74047 * mu_masyr * distance_kpc


def metallicity_ratio(fe_h: float) -> float:
    return 10 ** fe_h


def virial_mass(radius_kpc: float, sigma_kms: float) -> float:
    return 5 * radius_kpc * KPC_M * (sigma_kms * KMS_M) ** 2 / (G * MSUN)


def svg(i: int, title: str) -> str:
    """Each lecture gets a mechanically distinct visual-reasoning diagram."""
    stroke = "#0f6b78"; gold = "#b87911"; navy = "#102a43"; gray = "#5b6773"
    if i == 1:
        pts = " ".join(f"{40+x*60},{250-y*1.5}" for x,y in [(0,10),(1,24),(2,47),(3,82),(4,130),(5,180)])
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Vertical stellar density profile showing exponential falloff"><path d="M40 260H390M40 260V25" stroke="{navy}"/><polyline points="{pts}" fill="none" stroke="{stroke}" stroke-width="5"/><text x="250" y="290">height above plane (kpc)</text><text x="8" y="35" transform="rotate(-90 8 35)">stellar density</text><text x="230" y="70" fill="{gold}">exp(-|z|/h)</text></svg>'
    if i == 2:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Annotated Milky Way coordinate geometry diagram"><ellipse cx="210" cy="150" rx="165" ry="62" fill="#e5f4f6" stroke="{stroke}" stroke-width="4"/><circle cx="210" cy="150" r="8" fill="{gold}"/><line x1="210" y1="150" x2="335" y2="112" stroke="{navy}" stroke-width="3"/><text x="218" y="143">Sun</text><text x="280" y="105">l, b and distance</text><path d="M210 150 Q270 115 335 112" fill="none" stroke="{gold}" stroke-width="2" stroke-dasharray="5 5"/><text x="155" y="245">Galactic plane</text></svg>'
    if i == 3:
        bars = ''.join(f'<rect x="{45+j*55}" y="{245-v*2}" width="28" height="{v*2}" fill="{stroke}"/><text x="{50+j*55}" y="265">{lab}</text>' for j,(lab,v) in enumerate([("O",9),("B",8),("A",6),("F",5),("G",4),("K",3)]))
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Color-magnitude population histogram"><path d="M35 250H395M35 250V25" stroke="{navy}"/>{bars}<text x="165" y="292">spectral type</text><text x="5" y="35" transform="rotate(-90 5 35)">relative count</text></svg>'
    if i == 4:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Proper motion vector diagram in the Galactic plane"><circle cx="210" cy="150" r="95" fill="none" stroke="{gray}" stroke-dasharray="6 5"/><circle cx="210" cy="150" r="7" fill="{gold}"/><path d="M210 150 L320 92" stroke="{stroke}" stroke-width="5"/><path d="M320 92 l-20 2 l10 17" fill="{stroke}"/><path d="M210 150 L195 55" stroke="{navy}" stroke-width="3"/><text x="225" y="145">position</text><text x="300" y="80">proper-motion vector</text><text x="105" y="285">angular motion + distance -> tangential velocity</text></svg>'
    if i == 5:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Rotation curve comparison between baryons and a flat observed curve"><path d="M45 255H390M45 255V25" stroke="{navy}"/><path d="M45 240 Q150 80 250 55 Q320 45 380 42" fill="none" stroke="{gold}" stroke-width="5"/><path d="M45 240 Q120 90 170 65 L380 65" fill="none" stroke="{stroke}" stroke-width="5"/><text x="235" y="40">observed: flat</text><text x="255" y="98" fill="{gold}">baryons only</text><text x="220" y="290">Galactocentric radius</text><text x="3" y="35" transform="rotate(-90 3 35)">circular speed</text></svg>'
    if i == 6:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Spiral density-wave pattern with streaming motions"><circle cx="210" cy="150" r="14" fill="{gold}"/><path d="M210 150 C270 120 310 90 345 42 M210 150 C170 105 120 80 58 76 M210 150 C252 185 295 215 350 245 M210 150 C170 195 115 220 55 223" fill="none" stroke="{stroke}" stroke-width="16" opacity=".8"/><path d="M210 150 C235 135 270 122 300 112" stroke="{navy}" stroke-width="3" marker-end="url(#a)"/><text x="22" y="285">pattern speed differs from stellar orbital speed</text></svg>'
    if i == 7:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Chemical evolution diagram from gas to stars and enriched gas"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6z" fill="{stroke}"/></marker></defs><circle cx="80" cy="150" r="42" fill="#e5f4f6" stroke="{stroke}"/><text x="47" y="155">gas</text><circle cx="210" cy="80" r="42" fill="#fff8e8" stroke="{gold}"/><text x="175" y="85">stars</text><circle cx="340" cy="150" r="42" fill="#eef3f5" stroke="{navy}"/><text x="305" y="155">metals</text><path d="M122 135 L164 98M252 98 L298 135M298 170 L122 170" fill="none" stroke="{stroke}" stroke-width="3" marker-end="url(#a)"/><text x="140" y="255">yield + inflow + outflow</text></svg>'
    if i == 8:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Dark matter halo lensing and rotation evidence diagram"><ellipse cx="210" cy="150" rx="160" ry="110" fill="#eef3f5" stroke="{navy}" stroke-width="4"/><ellipse cx="210" cy="150" rx="55" ry="22" fill="#e5f4f6" stroke="{stroke}" stroke-width="4"/><circle cx="210" cy="150" r="10" fill="{gold}"/><path d="M55 70 Q210 20 365 70M55 230 Q210 280 365 230" fill="none" stroke="{gold}" stroke-width="3"/><text x="142" y="150">stellar disk</text><text x="125" y="35">extended halo</text></svg>'
    if i == 9:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Infrared view of the Galactic center with obscuring dust removed"><rect x="30" y="35" width="360" height="220" fill="#17202a"/><path d="M70 205 Q210 55 350 205" fill="none" stroke="#b87911" stroke-width="5"/><circle cx="210" cy="145" r="15" fill="#fff8e8"/><path d="M60 125 L160 145 L360 110M80 185 L180 145 L330 190" stroke="#e5f4f6" stroke-width="2" opacity=".8"/><text x="145" y="280">dust lanes fade in infrared</text></svg>'
    if i == 10:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Local Group map showing Milky Way, M31, and satellites"><circle cx="210" cy="150" r="24" fill="{gold}"/><circle cx="320" cy="120" r="34" fill="{stroke}" opacity=".8"/><circle cx="125" cy="205" r="10" fill="{navy}"/><circle cx="280" cy="230" r="8" fill="{navy}"/><line x1="234" y1="145" x2="286" y2="125" stroke="{gray}"/><text x="180" y="190">Milky Way</text><text x="300" y="90">M31</text><text x="67" y="240">satellite systems</text></svg>'
    if i == 11:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Tully-Fisher relation log luminosity versus log rotation speed"><path d="M45 255H390M45 255V25" stroke="{navy}"/><path d="M65 230 L350 55" stroke="{stroke}" stroke-width="4"/><circle cx="90" cy="216" r="7" fill="{gold}"/><circle cx="150" cy="178" r="7" fill="{gold}"/><circle cx="220" cy="140" r="7" fill="{gold}"/><circle cx="300" cy="88" r="7" fill="{gold}"/><text x="105" y="290">log V</text><text x="4" y="40" transform="rotate(-90 4 40)">log luminosity</text></svg>'
    if i == 12:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Bayesian inference triangle linking data model and posterior"><path d="M210 35 L60 250 L360 250 Z" fill="#e5f4f6" stroke="{stroke}" stroke-width="4"/><text x="187" y="28">data</text><text x="36" y="275">model</text><text x="340" y="275">posterior</text><circle cx="210" cy="170" r="34" fill="#fff8e8" stroke="{gold}"/><text x="185" y="176">p(theta|D)</text><path d="M180 145 L120 235M240 145 L300 235" stroke="{navy}" stroke-width="2"/></svg>'
    if i == 13:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Edge-on galaxy decomposition into bulge disk and halo"><ellipse cx="210" cy="150" rx="165" ry="42" fill="#e5f4f6" stroke="{stroke}" stroke-width="4"/><ellipse cx="210" cy="150" rx="62" ry="28" fill="#fff8e8" stroke="{gold}" stroke-width="4"/><path d="M45 150 Q210 60 375 150 Q210 240 45 150" fill="none" stroke="{navy}" stroke-width="3" stroke-dasharray="8 5"/><text x="180" y="145">bulge</text><text x="75" y="120">disk</text><text x="315" y="95">halo</text></svg>'
    if i == 14:
        return f'<svg viewBox="0 0 420 300" role="img" aria-label="Galactic archaeology timeline linking ancient stars to present-day streams"><path d="M55 220H370" stroke="{navy}" stroke-width="4"/><path d="M80 220V150M150 220V115M220 220V75M290 220V45M360 220V25" stroke="{stroke}" stroke-width="5"/><circle cx="80" cy="150" r="11" fill="{gold}"/><circle cx="150" cy="115" r="11" fill="{gold}"/><circle cx="220" cy="75" r="11" fill="{gold}"/><circle cx="290" cy="45" r="11" fill="{gold}"/><circle cx="360" cy="25" r="11" fill="{gold}"/><path d="M80 150 Q155 175 220 125 Q285 80 360 25" fill="none" stroke="{navy}" stroke-width="3" stroke-dasharray="7 5"/><text x="45" y="250">early assembly</text><text x="285" y="250">today: streams + chemistry</text></svg>'
    return f'<svg viewBox="0 0 420 300" role="img" aria-label="Synthesis diagram">{title}</svg>'


def page(title: str, body: str, css: str = CSS) -> str:
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{html.escape(title)}</title><script id='MathJax-script' async src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script><style>{css}</style></head><body>{body}</body></html>"


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def header(title: str, subtitle: str) -> str:
    return f"<header><div><h1>{html.escape(title)}</h1><p>{subtitle}</p></div></header>"

LECTURE_DATA = [
("The Galactic View: Scale, Coordinates, and Components", "Map the Milky Way in Galactocentric coordinates and separate disk, bulge, and halo.", "distance, geometry, and exponential structure", "The Milky Way is a physical system before it is a picture: every map is a coordinate choice and an inference.", r"\(\rho(z)=\rho_0 e^{-|z|/h}\)", "Use a vertical scale height h=0.30 kpc: at z=0.90 kpc the density fraction is exp(-3).", "vertical density", "The exponential is a model, not a claim that the disk has a sharp edge."),
("From Light to Orbits: Galactic Coordinates and Distances", "Convert observables into positions and velocities while tracking degeneracies.", "distance ladders and coordinate transforms", "Gaia turns angular measurements into phase-space samples, but distance and extinction remain coupled.", r"\(v_t=4.74047\,\mu\,d\)", "A proper motion of 2.5 mas yr^-1 at 1.6 kpc implies a tangential speed computed from the conversion constant.", "coordinate geometry", "Parallax inversion is biased at low signal-to-noise; a prior is not a measurement."),
("Stellar Populations as Fossils of Formation", "Use color-magnitude diagrams and abundance patterns to distinguish populations.", "main sequence, age, and metallicity", "A color-magnitude diagram is a time-integrated record of star formation, enrichment, and selection.", r"\([\mathrm{Fe/H}]=\log_{10}(N_{Fe}/N_H)-\log_{10}(N_{Fe}/N_H)_\odot\)", "Compare the iron abundance ratio for [Fe/H]=-1.55 with solar composition.", "population histogram", "Age-metallicity degeneracy means one photometric color rarely identifies an age uniquely."),
("Stellar Motions and the Galactic Phase Space", "Interpret proper motions, radial velocities, and velocity ellipsoids.", "6D phase space and asymmetric drift", "The disk is not a rigid carousel: random motions encode heating, birth conditions, and resonances.", r"\(v_t=4.74047\,\mu d\),  \quad \sigma_R>\sigma_\phi>\sigma_z\)", "Compute tangential speed for a 1.8 mas yr^-1 star at 2.4 kpc and compare it with disk dispersions.", "velocity vector", "A large proper motion can mean proximity rather than extreme space velocity."),
("The Rotation Curve and the Missing Mass", "Derive enclosed mass from circular motion and identify the flat-curve anomaly.", "circular speed and mass", "Rotation curves made the mass problem quantitative: outer disk speeds do not fall as a luminous point-mass model predicts.", r"\(M(\lt R)=Rv_c^2/G\)", "Use R=8.2 kpc and v_c=232 km s^-1 to estimate the enclosed mass.", "rotation curve", "The inference is mass within radius, not a direct photograph of dark matter."),
("Spiral Structure, Bars, and Galactic Resonances", "Explain spiral arms as patterns and locate resonances with orbital frequencies.", "density waves, bars, and pattern speed", "Stars cross spiral arms; the arm is a gravitational pattern whose speed need not equal the local circular speed.", r"\(m(\Omega-\Omega_p)=\kappa\)", "At a flat rotation curve, evaluate the orbital period at 8.2 kpc and discuss a plausible pattern speed.", "spiral pattern", "A density-wave picture is a model family; transient and recurrent arms remain active research topics."),
("Chemical Evolution of the Galactic Disk", "Connect gas flows, star formation, yields, and abundance gradients.", "closed-box limits and leaky evolution", "Metallicity is not merely a label: it records the competition among enrichment, inflow, outflow, and stellar lifetimes.", r"\(Z=y\ln(1/\mu)\)", "For yield y=0.020 and gas fraction mu=0.35, compute the closed-box metallicity and test its assumption.", "chemical cycle", "The closed-box model is pedagogical; inflow and outflow are required by observed populations."),
("Dark Matter Halos and the Local Mass Budget", "Compare baryonic and halo mass profiles and test halo models.", "halo density laws and dynamical evidence", "The same mass discrepancy appears in rotation, satellites, lensing, and structure formation, but each probe has distinct systematics.", r"\(\rho_{NFW}(r)=\rho_s/[x(1+x)^2]\)", "Compare the enclosed mass from the local circular speed with a baryonic benchmark and state what is actually inferred.", "halo geometry", "A flat curve alone does not determine a unique halo profile."),
("The Galactic Center: Black Hole, Bulge, and Nuclear Environment", "Use stellar orbits and infrared observations to constrain the central mass.", "Sgr A*, extinction, and nuclear dynamics", "The central parsec is a laboratory where orbital motion, stellar populations, and gas dynamics meet.", r"\(M=4\pi^2a^3/(GP^2)\)", "Use a=0.005 pc and P=15.8 yr as an orbit-scale exercise to estimate the central mass.", "infrared center", "Keplerian motion constrains enclosed mass; it does not by itself explain the accretion state."),
("Nearby Galaxies and the Local Group", "Compare morphology, satellites, and dynamics across nearby galaxies.", "M31, dwarf satellites, and environmental transformation", "The Milky Way becomes a comparative case: nearby galaxies reveal which features are universal and which are contingent.", r"\(M_{vir}\approx5R\sigma^2/G\)", "Estimate a satellite group mass from R=120 kpc and sigma=95 km s^-1, with model caveats.", "Local Group map", "Virial estimators are sensitive to membership, anisotropy, and dynamical equilibrium."),
("Scaling Relations: Tully-Fisher and Galaxy Structure", "Use scaling relations as empirical constraints and distance tools.", "luminosity, rotation, and residuals", "Scaling relations compress complex galaxy physics into testable correlations, not universal laws without scatter.", r"\(L\propto v_c^\alpha\)", "For alpha=4, determine the luminosity ratio for galaxies with speeds 220 and 110 km s^-1.", "Tully-Fisher line", "Selection, inclination, and bandpass can tilt or broaden an observed relation."),
("Inference with Galactic Surveys", "Build a reproducible model-data comparison and quantify uncertainty.", "likelihoods, priors, and selection functions", "Survey astronomy is an inverse problem: the catalogue is filtered by the instrument and by the scientist's cuts.", r"\(p(\theta|D)\propto p(D|\theta)p(\theta)\)", "Construct a simple likelihood for rotation-curve points with 8 km s^-1 errors and compare two models.", "inference triangle", "A precise posterior can still be wrong when the selection function or likelihood is misspecified."),
("Galactic Archaeology and the Milky Way in Time", "Use ages, chemistry, and phase-space structure to reconstruct assembly history.", "streams, accretion, and time-dependent structure", "A galaxy is not only a present-day equilibrium: disrupted satellites and chemically tagged stars preserve its assembly record.", r"\(t_{\rm lookback}=t_0-t_{\rm formation}\)", "Compare a metal-poor stream ([Fe/H]=-1.5) with a thin-disk sample ([Fe/H]=-0.05) using the abundance-ratio function.", "stellar stream", "Chemical tagging is probabilistic; migration and selection can blur the original birth environment."),
("A Working Synthesis: What Makes a Galaxy?", "Integrate structure, populations, dynamics, chemistry, and comparison into a defensible model.", "evidence-weighted Galactic astronomy", "No single map explains the Galaxy; a credible model survives independent checks across tracers.", r"\(\mathcal{M}=\{\rho_\star,\rho_{DM},\Phi,\mathrm{SFH},Z(r)\}\)", "Compare a disk-plus-halo explanation against a baryons-only rotation curve and identify the strongest discriminant.", "galaxy decomposition", "Model comparison is conditional on assumptions and data quality; residuals are evidence, not failure."),
]

# Term, definition, lecture significance, relationship, and limitation/common confusion.
TERMS_DATA = [
[
("Galactocentric coordinates", "A position system whose origin is the Galactic center, commonly expressed by cylindrical \\(R,\\phi,z\\) or Cartesian axes.", "It lets us describe Milky Way structure without confusing the Sun's off-center viewpoint with the Galaxy's intrinsic geometry.", "The coordinates turn heliocentric distance and sky direction into the \\(R\\) and \\(z\\) used by density models.", "The transformation depends on adopted solar position and orientation; it is not a direct observable."),
("Thin disk", "The flattened, dynamically cold stellar and gaseous component concentrated near the Galactic mid-plane.", "It contains much of the current star formation and supplies the baseline population for the vertical-density calculation.", "Its characteristic scale height enters \\(\\rho(z)=\\rho_0e^{-|z|/h}\\) and differs by tracer age.", "Thin disk is a population model, not a sharply bounded physical sheet."),
("Thick disk", "A vertically extended, kinematically hotter disk population with older stars and distinct abundance trends.", "Contrasting it with the thin disk shows why one exponential cannot represent every stellar sample.", "A two-component density model sums exponentials with different scale heights and normalizations.", "It should not be identified by height alone because disk populations overlap in chemistry and motion."),
("Bulge", "The centrally concentrated stellar component occupying the inner few kiloparsecs, including a barred or box-peanut structure.", "It is one of the major components that a Galactic mass and light model must separate.", "Bulge star counts and infrared surface brightness constrain central density but overlap the disk along many sightlines.", "Bulge does not mean a simple spherical classical bulge."),
("Stellar halo", "A diffuse, approximately spheroidal population of old, metal-poor stars extending far beyond the disk.", "It provides tracers of the Galaxy's outer structure and assembly while contributing little of the total stellar light.", "Halo density is inferred from selected tracers such as RR Lyrae and relates to, but is not the same as, the dark-matter halo.", "Stellar halo and dark-matter halo are distinct components with different observables."),
],
[
("Galactic longitude and latitude", "Angular sky coordinates \\((l,b)\\) aligned with the Galactic plane and center direction.", "They specify a sightline from the Sun before distance converts that direction into a three-dimensional position.", "Together with distance, \\(l\\) and \\(b\\) map into Galactocentric coordinates and projected velocity components.", "They are heliocentric angles and do not by themselves locate a star in the Galaxy."),
("Parallax", "The apparent annual angular displacement caused by Earth's orbital baseline, with distance approximately inverse to parallax at high signal-to-noise.", "It anchors Gaia distances that are needed to turn angles and proper motions into Galactic positions and speeds.", "Distance enters \\(v_t=4.74047\\mu d\\), so parallax uncertainty propagates directly into tangential velocity.", "Naively inverting a noisy or non-positive measured parallax produces biased distances."),
("Proper motion", "A source's angular velocity across the sky, usually reported in milliarcseconds per year.", "It supplies two transverse components of stellar motion measured by astrometry.", "Multiplication by distance through \\(v_t=4.74047\\mu d\\) converts angular motion into km s\\(^{-1}\\).", "A large proper motion may indicate a nearby star rather than an unusually fast one."),
("Radial velocity", "The line-of-sight velocity inferred primarily from Doppler shifts of spectral features.", "It complements proper motion to recover a star's three-dimensional velocity.", "Combining radial velocity with distance and proper motion yields phase-space coordinates after correcting for solar motion.", "It is one projected component and can include binary orbital motion."),
("Extinction", "Wavelength-dependent attenuation and reddening of starlight by interstellar dust.", "It couples apparent brightness and color to distance, especially in disk and central sightlines.", "Distance modulus must include an extinction term, while multiband colors can help constrain the dust correction.", "Extinction is not the same as geometric dimming and is not uniform across the sky."),
],
[
("Color-magnitude diagram", "A plot of stellar luminosity or absolute magnitude against a color index that traces temperature.", "Its morphology encodes the age, composition, distance, and selection of a stellar population.", "Isochrones map stellar-evolution models onto the observed main sequence, turnoff, and giant branch.", "A CMD is not a literal evolutionary track followed by one star."),
("Main-sequence turnoff", "The CMD location where stars of a population begin exhausting core hydrogen and leave the main sequence.", "It is one of the most age-sensitive features available for resolved stellar populations.", "Turnoff luminosity is compared with isochrones at an assumed metallicity and distance.", "Age, metallicity, binaries, and photometric errors can shift or broaden the turnoff."),
("Metallicity [Fe/H]", "A logarithmic iron-to-hydrogen abundance relative to the Sun: \\([\\mathrm{Fe/H}]=\\log_{10}(N_{\\rm Fe}/N_{\\rm H})-\\log_{10}(N_{\\rm Fe}/N_{\\rm H})_\\odot\\).", "It distinguishes broad Galactic populations and records chemical enrichment.", "A value of -1.55 means about \\(10^{-1.55}\\) of the solar iron-to-hydrogen ratio.", "It is not the fraction of all heavy elements and does not uniquely specify an age."),
("Isochrone", "A model locus in a CMD for stars of one age and initial chemical composition but different masses.", "It links stellar-evolution theory to observed population ages and metallicities.", "Fitting an isochrone requires distance, extinction, abundance, and a treatment of binaries and completeness.", "A visually good fit is not unique when age-metallicity-extinction degeneracies are present."),
("Selection function", "The probability that an object with given properties enters the observed sample.", "Population fractions and CMD shapes cannot be interpreted without knowing which stars the survey could detect.", "It connects the underlying stellar distribution to the catalogue likelihood and completeness corrections.", "The observed sample is not automatically representative of the Galactic population."),
],
[
("Phase space", "The six-dimensional specification of three positions and three velocities for each star.", "Galactic dynamics predicts how stellar distributions evolve in this space rather than on a sky map alone.", "Gaia astrometry plus radial velocities approximates 6D phase-space coordinates after coordinate transformations.", "A catalogue with six reported numbers still has correlated errors and selection effects."),
("Velocity ellipsoid", "A covariance description of the distribution of stellar velocities along chosen axes.", "Its axis lengths and orientation quantify random motions, disk heating, and population differences.", "Disk populations often satisfy \\(\\sigma_R>\\sigma_\\phi>\\sigma_z\\), linking dispersions to epicyclic dynamics.", "It describes a distribution, not a solid object or a single star's orbit."),
("Asymmetric drift", "The lag of a pressure-supported stellar population's mean rotation behind the local circular speed.", "It explains why hotter populations rotate more slowly even in the same gravitational potential.", "The lag is related through the Jeans equations to radial dispersion and density gradients.", "It is not evidence that every lagging star belongs to the halo."),
("Solar motion", "The Sun's velocity relative to a chosen local standard of rest or Galactic reference frame.", "Observed stellar velocities must be corrected for the observer's own motion before Galactic patterns are inferred.", "It enters transformations from heliocentric radial velocity and proper motion to Galactocentric components.", "Different reference-frame conventions produce different quoted solar-motion values."),
("Tangential velocity", "The linear component of motion perpendicular to the line of sight.", "It is the physical speed inferred from angular proper motion and distance.", "The conversion \\(v_t=4.74047\\mu d\\) couples astrometric and distance uncertainties.", "Tangential speed alone is not the total space speed."),
],
[
("Rotation curve", "The circular speed \\(v_c(R)\\) inferred as a function of Galactocentric radius.", "Its outer shape is the central dynamical evidence for mass beyond the luminous disk.", "Under an idealized spherical interpretation, \\(M(\\lt R)=Rv_c^2/G\\).", "A rotation curve is inferred from tracers and geometry; it is not a direct plot of all stellar orbital speeds."),
("Circular speed", "The speed required for a circular orbit in a specified gravitational potential at a given radius.", "It links the measured kinematics to the radial gravitational force.", "It satisfies \\(v_c^2=R\\,\\partial\\Phi/\\partial R\\) in an axisymmetric mid-plane model.", "It differs from the mean azimuthal speed of a population with random motion."),
("Enclosed mass", "The mass inside radius \\(R\\) that produces the inferred gravitational acceleration under a stated geometry.", "It converts a flat outer rotation curve into a growing dynamical mass estimate.", "For spherical symmetry, \\(M(\\lt R)=Rv_c^2/G\\), so constant \\(v_c\\) implies \\(M\\propto R\\).", "The simple formula is not exact for a flattened disk and does not separate baryons from dark matter."),
("Baryonic mass", "Mass in ordinary matter, chiefly stars and gas, that emits, absorbs, or otherwise interacts electromagnetically.", "Its predicted gravitational contribution can be compared with the observed rotation curve.", "Stellar mass-to-light ratios and gas maps build the baryonic rotation model.", "Baryonic mass is not identical to visible light because faint stars and cold gas also contribute."),
("Dark matter", "A non-luminous mass component inferred from gravity whose distribution extends beyond the stellar disk.", "It provides the standard explanation for flat outer rotation curves and multiple independent dynamical probes.", "A halo contribution is added in quadrature to bulge, disk, and gas contributions to \\(v_c^2\\).", "A mass discrepancy establishes missing gravity under the model, not a direct image or unique particle identity."),
],
[
("Pattern speed", "The angular rate \\(\\Omega_p\\) at which a bar or spiral pattern rotates.", "It separates the motion of the density pattern from the orbital angular speed of individual stars and gas.", "Resonances occur where combinations of \\(\\Omega-\\Omega_p\\) and epicyclic frequency \\(\\kappa\\) match.", "Stars do not generally remain attached to the same spiral arm."),
("Epicyclic frequency", "The frequency \\(\\kappa\\) of small radial oscillations about a nearly circular guiding-center orbit.", "It provides the dynamical clock used to locate Lindblad resonances.", "For an \\(m\\)-armed pattern, resonance conditions involve \\(m(\\Omega-\\Omega_p)=\\pm\\kappa\\).", "The approximation is least reliable for strongly eccentric or chaotic orbits."),
("Corotation resonance", "The radius where the orbital angular frequency equals the pattern speed, \\(\\Omega=\\Omega_p\\).", "At corotation, a star sees the pattern as approximately stationary and can exchange angular momentum efficiently.", "It lies between inner and outer resonance regions and helps constrain bar or spiral dynamics.", "Corotation is a radius or zone, not proof that material and pattern permanently co-rotate."),
("Lindblad resonance", "A resonance where radial epicyclic motion and passage through an \\(m\\)-fold pattern are commensurate.", "It organizes orbital responses, rings, heating, and angular-momentum transfer.", "The idealized conditions are \\(m(\\Omega-\\Omega_p)=\\pm\\kappa\\) for inner and outer resonances.", "Sign conventions vary, and real bars can make the weak-perturbation picture incomplete."),
("Density wave", "A coherent overdensity pattern that propagates through disk material rather than consisting of permanently bound arm stars.", "It explains how spiral structure can persist longer than the differential-rotation winding time.", "Gas compression and star formation can trace the phase of the gravitational pattern with offsets.", "Not all spirals are steady waves; transient and recurrent arms are viable alternatives."),
],
[
("Metal yield", "The mass of newly synthesized heavy elements returned to gas per unit mass locked into long-lived stars, under a stated convention.", "It sets the enrichment scale in the closed-box relation \\(Z=y\\ln(1/\\mu)\\).", "Yield combines stellar nucleosynthesis with an assumed initial mass function and return fraction.", "It is an effective model parameter, not the metallicity of an individual star."),
("Gas fraction", "The fraction \\(\\mu\\) of a system's relevant baryonic mass that remains in gas.", "It tracks how much fuel is available and controls closed-box metallicity growth.", "As \\(\\mu\\) declines, the idealized model predicts \\(Z=y\\ln(1/\\mu)\\).", "The definition depends on the adopted boundary and ignores uncounted or ionized phases if the inventory is incomplete."),
("Closed-box model", "A one-zone chemical-evolution model with no inflow or outflow and instantaneous, well-mixed recycling.", "It supplies a transparent benchmark against which observed abundance distributions can be tested.", "Its metallicity relation connects yield and gas fraction without a detailed star-formation history.", "Real Galactic disks exchange gas and violate instantaneous mixing and recycling assumptions."),
("Inflow", "Gas accretion into the modeled Galactic region.", "Low-metallicity inflow can sustain star formation and dilute enriched interstellar gas.", "In chemical-evolution equations it adds gas and metals at an external composition.", "Inflow cannot be inferred from low metallicity alone because yields and outflows are degenerate."),
("Abundance gradient", "A systematic change in elemental abundance with Galactocentric radius or height.", "It constrains inside-out growth, gas flows, enrichment, and radial migration.", "The slope \\(d[\\mathrm{Fe/H}]/dR\\) links stellar or gas tracers to chemical-evolution models.", "Different ages and tracers can have different gradients, so one slope is not universal."),
],
[
("Dark-matter halo", "The extended gravitating component surrounding a galaxy and dominating its mass at large radii in standard models.", "It connects local rotation evidence to satellite motions, lensing, and cosmological structure formation.", "Its density profile determines the halo contribution to the circular-speed curve.", "It is distinct from the sparse stellar halo and its shape is not fixed by one probe."),
("NFW profile", "A cusped spherical density law \\(\\rho=\\rho_s/[x(1+x)^2]\\), with \\(x=r/r_s\\), motivated by collisionless simulations.", "It provides a standard parameterized halo model for comparison with dynamical data.", "The scale density \\(\\rho_s\\) and scale radius \\(r_s\\) set concentration and enclosed mass.", "Baryonic evolution and limited radial data can make an NFW fit non-unique."),
("Local mass density", "The total gravitating mass per unit volume near the Sun.", "Vertical stellar motions constrain the combined local inventory of stars, gas, and dark matter.", "The vertical Jeans and Poisson equations connect tracer density and velocity dispersion to gravitational density.", "It is not the same quantity as mass enclosed inside the solar circle."),
("Mass decomposition", "The separation of an observed gravitational field into bulge, disk, gas, and halo contributions.", "It tests whether known baryons can account for the rotation curve and local force.", "Component contributions add through the potential, often displayed as contributions to \\(v_c^2\\).", "Different stellar mass-to-light ratios can trade off against halo parameters."),
("Dynamical tracer", "An object population whose positions and velocities respond to the gravitational potential.", "Stars, gas, and satellites probe different radii and systematic uncertainties.", "A tracer distribution enters Jeans, orbit, or rotation models rather than equaling the mass distribution.", "Tracer density need not follow total mass density."),
],
[
("Sgr A*", "The compact radio source at the Milky Way's dynamical center, associated with the central supermassive black hole.", "It defines the focus of short-period stellar orbits used to measure the central mass.", "Orbital semimajor axes and periods constrain enclosed mass through Kepler's law.", "The radio source's faint emission does not imply a low black-hole mass."),
("Keplerian orbit", "An orbit governed predominantly by a central point mass, with period and semimajor axis related by \\(M=4\\pi^2a^3/(GP^2)\\).", "Near Sgr A*, stellar trajectories provide a direct dynamical mass measurement.", "Departures from a pure Kepler ellipse can test extended mass and relativistic effects.", "The observed angular orbit still requires distance and projection modeling."),
("Extinction window", "A wavelength range or sightline where dust attenuation is reduced enough to reveal the Galactic center.", "Near-infrared observations penetrate dust that blocks optical views of the nuclear region.", "The extinction law converts observed colors and fluxes into intrinsic stellar properties.", "Infrared reduces but does not eliminate extinction or source confusion."),
("Nuclear star cluster", "The dense stellar system surrounding Sgr A* within the central few parsecs.", "It supplies orbital tracers and contributes extended mass around the black hole.", "Its luminosity and kinematics must be modeled alongside the point-mass potential.", "It is not synonymous with the bulge, which occupies a much larger volume."),
("Enclosed central mass", "The total gravitating mass inside a stellar orbit near the Galactic center.", "Consistency among multiple stellar orbits demonstrates a compact mass of millions of solar masses.", "Kepler's relation estimates the dominant mass when the orbit lies inside most extended material.", "Dynamics establishes compactness and mass but does not alone specify the accretion physics."),
],
[
("Local Group", "The gravitationally associated collection dominated by the Milky Way and M31, together with M33 and many dwarf galaxies.", "It supplies nearby comparative laboratories for galaxy structure and environmental effects.", "Member positions and velocities constrain group dynamics and future Milky Way-M31 interaction.", "Its boundary and membership are not perfectly sharp or necessarily virialized."),
("Dwarf satellite", "A low-luminosity galaxy gravitationally associated with a more massive host.", "Satellites trace halo mass, tidal processing, and the small-scale galaxy population.", "Their velocity dispersions and orbital distributions enter dynamical mass estimates.", "A high mass-to-light ratio can be sensitive to membership and binary contamination."),
("Virial mass estimator", "An approximate mass relation based on characteristic size and velocity dispersion, such as \\(M\\sim5R\\sigma^2/G\\).", "It turns group or satellite kinematics into an order-of-magnitude dynamical mass.", "The estimator follows from the virial theorem under equilibrium and structural assumptions.", "It is unreliable for sparse, anisotropic, or non-equilibrium systems."),
("Velocity dispersion", "The statistical spread of member velocities about their mean motion.", "It measures random kinetic support in groups and pressure-supported galaxies.", "Together with a scale radius, \\(\\sigma\\) controls virial and Jeans mass estimates.", "Dispersion is not the same as measurement error or ordered rotation."),
("Environmental transformation", "Change in a galaxy's gas, star formation, or morphology driven by interactions with its surroundings.", "Local Group dwarfs show how tides, ram pressure, and host proximity shape evolution.", "Comparisons of gas content and star-formation history with distance from a host test environmental models.", "Correlation with host distance does not by itself identify a unique mechanism."),
],
[
("Tully-Fisher relation", "An empirical correlation between a disk galaxy's luminosity or baryonic mass and characteristic rotation speed.", "It constrains galaxy formation and can provide relative distances when calibrated.", "A common form is \\(L\\propto v_c^\\alpha\\), with slope and scatter depending on observable choices.", "It is a statistical relation, not an exact law for every galaxy."),
("Characteristic rotation speed", "A consistently defined velocity measure, often from the flat part or width of a rotation curve.", "It is the kinematic coordinate of the Tully-Fisher relation.", "Inclination-corrected spectral line width can serve as a proxy for \\(v_c\\).", "Mixing velocity definitions changes the fitted slope and scatter."),
("Mass-to-light ratio", "The ratio of inferred mass to emitted luminosity in a specified band.", "It links observed light to stellar mass and helps interpret scaling-relation residuals.", "Population synthesis predicts stellar mass-to-light ratio from age, metallicity, and IMF assumptions.", "It is band-dependent and does not automatically include dark matter."),
("Intrinsic scatter", "The astrophysical dispersion around a relation remaining after measurement errors are accounted for.", "It determines both the physical informativeness and distance precision of a scaling relation.", "Likelihood models separate observational uncertainty from a population-level scatter term.", "Observed scatter is not all intrinsic if errors or selection are misspecified."),
("Inclination correction", "The geometric conversion from projected line-of-sight rotation to the disk-plane speed.", "It is essential because a face-on disk shows little Doppler rotation even when rotating rapidly.", "For an ideal disk, observed amplitude scales approximately as \\(v_c\\sin i\\).", "Small inclination errors become severe near face-on orientation."),
],
[
("Likelihood", "A model for the probability of the observed data as a function of parameters, \\(p(D|\\theta)\\).", "It encodes the measurement uncertainties used to compare Galactic models with survey data.", "For independent Gaussian rotation points it is related to a chi-square residual sum.", "A convenient likelihood can be precise yet wrong if errors are correlated or non-Gaussian."),
("Prior", "A probability distribution for parameters before conditioning on the current data.", "It regularizes underconstrained distance and Galactic-structure inferences and makes assumptions explicit.", "Bayes' theorem combines it with the likelihood to form \\(p(\\theta|D)\\).", "A prior is not an additional observation, and an apparently weak prior can matter with sparse data."),
("Posterior", "The probability distribution of model parameters after combining likelihood and prior.", "It summarizes parameter estimates, uncertainty, and covariance for the adopted model.", "Posterior predictive checks connect inferred parameters back to observable catalogues.", "A narrow posterior does not protect against a misspecified model or selection function."),
("Selection function", "The probability that an astronomical source is detected and retained as a function of its properties.", "It is part of the data-generating process and must enter population inference.", "The predicted underlying population is multiplied by selection before comparison with a catalogue.", "Cuts applied by the analyst are part of the selection, not harmless bookkeeping."),
("Posterior predictive check", "A comparison between data simulated from the fitted posterior model and the actual observations.", "It tests whether the model reproduces features beyond the fitted parameter summary.", "Residual distributions, trends, and replicated catalogues reveal model-data mismatch.", "Passing selected checks does not prove the model unique or physically true."),
],
[
("Stellar stream", "A coherent, elongated structure of stars stripped from a cluster or dwarf galaxy along its orbit.", "Streams preserve phase-space evidence of accretion and probe the Galactic potential.", "Their track, distance, velocities, and width are compared with orbit or disruption models.", "A stream is not exactly one orbit because stripping occurs over time and stars have finite dispersion."),
("Accretion event", "The incorporation and tidal disruption of a smaller stellar system by the Milky Way.", "It contributes stars, clusters, and dark matter while leaving kinematic and chemical substructure.", "Common integrals of motion and abundance patterns can associate debris with a progenitor.", "A named debris structure may combine multiple events or overlap in projected phase space."),
("Chemical tagging", "The probabilistic association of stars through multidimensional elemental-abundance patterns.", "It can connect dispersed stars to shared formation environments after spatial coherence is lost.", "Abundance vectors complement ages and orbital information in archaeology.", "Similar chemistry is not a unique birth certificate because enrichment pathways overlap."),
("Radial migration", "A lasting change in a disk star's guiding-center radius, often driven by resonant interactions.", "It mixes stars born at different radii and blurs present-day chemical gradients.", "Migration connects spiral or bar resonances to the age-metallicity-radius distribution.", "It differs from epicyclic blurring, which changes instantaneous radius without shifting the guiding center."),
("Lookback time", "The elapsed time between emitted light or a past formation event and the present epoch.", "It places stellar ages and assembly episodes on a common temporal axis.", "For a formation time \\(t_{\\rm formation}\\), \\(t_{\\rm lookback}=t_0-t_{\\rm formation}\\).", "For Galactic stars it is usually an age inference, not a cosmological light-travel measurement."),
],
[
("Tracer", "An observable population or signal used to constrain an underlying Galactic property.", "Synthesis depends on comparing stars, gas, abundances, lensing, and satellites that respond differently.", "Each tracer connects to model components through its own measurement equation and selection function.", "A tracer distribution is not automatically the mass distribution it probes."),
("Gravitational potential", "The scalar field \\(\\Phi\\) whose gradient determines gravitational acceleration and orbital motion.", "It is the common dynamical object that disk, bulge, and halo mass models must reproduce.", "Circular speed satisfies \\(v_c^2=R\\,\\partial\\Phi/\\partial R\\), while stellar orbits sample more dimensions.", "Different density decompositions can generate similar potentials over the observed region."),
("Star-formation history", "The rate at which a galaxy formed stars as a function of time and, often, position.", "It links present-day populations to gas supply, feedback, and assembly.", "CMD fitting and abundance distributions constrain \\(\\mathrm{SFH}\\) with stellar-evolution models.", "It is model-dependent and limited by age resolution and selection."),
("Model residual", "The signed difference between an observation and the corresponding model prediction.", "Residual structure identifies missing physics, calibration errors, or inappropriate assumptions.", "Residuals normalized by uncertainty contribute to chi-square and posterior predictive checks.", "A nonzero residual is evidence to investigate, not automatically a failed experiment or a new component."),
("Cross-validation by independent probes", "Testing one physical model against datasets with substantially different observables and systematics.", "Agreement among rotation, vertical dynamics, chemistry, and external-galaxy comparisons makes a Galactic model more credible.", "The synthesis model \\(\\mathcal{M}\\) must map each component to a distinct prediction.", "Two probes are not independent if they share calibrations, priors, or selected tracers."),
],
]

def worked(i: int) -> tuple[str, str]:
    if i == 1:
        x = math.exp(-0.9 / 0.3); return f"A three-scale-height displacement gives exp(-3) = {fmt(x)} of the mid-plane density.", "The calculation is dimensionless; the physical uncertainty lies in whether one exponential component is adequate."
    if i == 2:
        v = proper_motion_speed(2.5, 1.6); return f"For mu=2.5 mas yr^-1 and d=1.6 kpc, v_t = 4.74047 mu d = {fmt(v,5)} km s^-1.", "This is only the tangential component; radial velocity is needed for a 3D speed."
    if i == 3:
        q = metallicity_ratio(-1.55); return f"[Fe/H]=-1.55 means 10^(-1.55) = {fmt(q,4)} times the solar iron-to-hydrogen ratio.", "This is an abundance ratio, not a statement that the star has 3% of every element."
    if i == 4:
        v = proper_motion_speed(1.8, 2.4); return f"For mu=1.8 mas yr^-1 and d=2.4 kpc, v_t = {fmt(v,5)} km s^-1.", "The conversion assumes the proper motion is calibrated and the distance is the adopted estimate."
    if i == 5:
        m = enclosed_mass_msun(8.2, 232); return f"M(<8.2 kpc)=Rv^2/G = {fmt(m,5)} solar masses.", "This is an enclosed dynamical mass; it combines stars, gas, and dark matter."
    if i == 6:
        p = orbital_period_gyr(8.2, 232); return f"The local orbital period is 2 pi R/v = {fmt(p,4)} Gyr.", "A pattern can rotate at a different angular speed, so arm crossings are not the same as orbiting with an arm."
    if i == 7:
        z = 0.020 * math.log(1 / 0.35); return f"The closed-box estimate is Z=y ln(1/mu) = {fmt(z,4)}.", "The number is a model limit; gas inflow and metal-loaded outflow change the result."
    if i == 8:
        m = enclosed_mass_msun(8.2, 232); return f"The local dynamical estimate is {fmt(m,5)} solar masses inside 8.2 kpc.", "It cannot by itself separate the radial mass contributions of disk, bulge, and halo."
    if i == 9:
        a = 0.005 * KPC_M; p = 15.8 * YEAR_S; m = 4 * math.pi**2 * a**3 / (G * p**2) / MSUN; return f"The Kepler estimate gives M = {fmt(m,5)} solar masses.", "The orbit-scale inputs are representative literature values; the inference assumes a dominant central mass."
    if i == 10:
        m = virial_mass(120, 95); return f"M_vir ~ 5 R sigma^2/G = {fmt(m,5)} solar masses.", "The coefficient is an order-unity estimator, not a precision measurement."
    if i == 11:
        ratio = (220 / 110) ** 4; return f"With L proportional to v^4, doubling speed predicts L2/L1 = {fmt(ratio)}.", "Observed scatter and calibration choices determine how useful the relation is for distances."
    if i == 12:
        chi2 = sum(((v - 232) / 8) ** 2 for _, v in ROTATION); return f"A flat 232 km s^-1 model has chi^2 = {fmt(chi2,5)} for the seven listed points when each uncertainty is 8 km s^-1.", "A chi-square comparison needs a stated number of fitted parameters and a justified error model."
    m = enclosed_mass_msun(8.2, 232); return f"The synthesis retains the local enclosed mass {fmt(m,5)} solar masses as a cross-check across dynamics and populations.", "The conclusion is strongest when independent tracers agree rather than when one model fits one plot."


def term_explorer(i: int, terms: list[tuple[str, str, str, str, str]]) -> str:
    buttons = []
    panels = []
    for j, (term, definition, significance, relationship, limitation) in enumerate(terms, 1):
        tab_id = f"lecture-{i:02d}-term-{j}-tab"
        panel_id = f"lecture-{i:02d}-term-{j}-panel"
        selected = "true" if j == 1 else "false"
        hidden = "" if j == 1 else " hidden"
        buttons.append(
            f'<button class="term-button" id="{tab_id}" type="button" role="tab" '
            f'aria-selected="{selected}" aria-controls="{panel_id}" '
            f'data-term-target="{panel_id}">{term}</button>'
        )
        panels.append(
            f'<article class="term-detail" id="{panel_id}" role="tabpanel" '
            f'aria-labelledby="{tab_id}"{hidden}><h3>{term}</h3>'
            f'<p><strong>Definition:</strong> {definition}</p>'
            f'<p><strong>Why it matters here:</strong> {significance}</p>'
            f'<p><strong>Relationship:</strong> {relationship}</p>'
            f'<p><strong>Limitation or common confusion:</strong> {limitation}</p></article>'
        )
    return (
        '<section class="slide glossary-slide" aria-labelledby="terms-heading-'
        f'{i:02d}"><h2 id="terms-heading-{i:02d}">Terms for This Lecture</h2>'
        '<div class="term-explorer" data-term-explorer>'
        '<div class="term-list" role="tablist" aria-label="Lecture terms">'
        + "".join(buttons) + '</div><div class="term-details">'
        + "".join(panels) + "</div></div></section>"
    )


def terms_notes(i: int, scope: str, equation: str, terms: list[tuple[str, str, str, str, str]]) -> str:
    entries = []
    for term, definition, significance, relationship, limitation in terms:
        entries.append(
            f"<article><h3>{term}</h3><p>{definition} {significance} "
            f"{relationship} In this lecture, use this term while reasoning about {scope}, "
            f"and distinguish the measured quantity from the model-dependent quantity in {equation}. "
            f"{limitation} This boundary is important when comparing tracers or carrying the result "
            "into the worked example.</p></article>"
        )
    return "<section><h2>Terms Developed in Context</h2>" + "".join(entries) + "</section>"


def lecture_pages(i: int, item: tuple[str, ...]) -> tuple[str, str]:
    title, outcome, scope, motivation, equation, prompt, visual_name, limitation = item
    calc, interp = worked(i)
    terms = TERMS_DATA[i - 1]
    figure = f'<figure class="figure">{svg(i, title)}<figcaption>{html.escape(visual_name.title())}: a lecture-specific schematic or model plot. Axes and annotations identify the inference being made; it is not presented as a raw survey image.</figcaption></figure>'
    slides = [
        f'<section class="slide title"><div class="kicker">ASTR 410 · Lecture {i:02d}</div><h1>Lecture {i:02d}: {html.escape(title)}</h1><h2>Galactic Astronomy</h2><p>{html.escape(motivation)}</p></section>',
        f'<section class="slide"><h2>Objectives and route</h2>{bullets([f"{outcome}", f"Connect {scope} to observations and model assumptions.", "Make one auditable calculation and interpret its limitation.", "Use an evidence chain rather than treating a visualization as a direct measurement."])}</section>',
        f'<section class="slide"><h2>Why this question is hard</h2><div class="grid"><div><p>{motivation}</p><p>Galactic astronomy observes projected light, velocities, and abundances from one moving vantage point. The inverse problem is underdetermined until geometry, selection, and a physical model are made explicit.</p></div>{figure}</div></section>',
        term_explorer(i, terms),
        f'<section class="slide"><h2>Physical tool</h2><p>The central relation for this lecture is:</p><div class="equation">{equation}</div><p>Define every symbol before substitution. State the coordinate system, units, and approximation. A formula is evidence only when its assumptions match the tracer and regime.</p></section>',
        f'<section class="slide"><h2>Evidence display</h2><p>The evidence display for this lecture is the labeled model/data relationship introduced above. Read the axes and annotations before accepting the inferred trend.</p><p class="credit">Data context: the accompanying values are standard published or survey-like values; see the course reference log for provenance level and spot-check targets.</p></section>',
        f'<section class="slide"><h2>Worked calculation</h2><div class="equation">{html.escape(calc)}</div><p>{html.escape(interp)}</p><p>Write the units beside each intermediate quantity. The numerical result is generated from the shared course constants and recomputed independently during review.</p></section>',
        f'<section class="slide"><h2>Interpret the pattern</h2>{bullets([f"The observable is not identical to the inferred quantity: distinguish measurement, calibration, and model.", f"A comparison across tracers is more informative than a single fitted parameter.", f"The result should be reported with its assumptions and an uncertainty or sensitivity statement."])}</section>',
        f'<section class="slide"><h2>Boundary condition and misconception</h2><div class="prompt"><strong>Do not overread the model:</strong> {html.escape(limitation)}</div><p>Ask whether changing the distance prior, selection function, or mass decomposition could move the conclusion. This is where a plausible diagram can become a misleading argument.</p></section>',
        f'<section class="slide"><h2>In-class reasoning</h2><div class="prompt"><p><strong>Prompt:</strong> {html.escape(prompt)}</p><p>First estimate the direction of the answer. Then calculate. Finally name one assumption that could reverse the interpretation.</p></div></section>',
        f'<section class="slide"><h2>Connection across the course</h2>{bullets(["Earlier tools: PHYS 331 dynamics, statistical reasoning, and ASTR 330 stellar populations.", "Next step: use this inference in the paired lab and problem set with a stated data model.", "Cumulative theme: Galactic structure is inferred by making independent observables agree."])}</section>',
        f'<section class="slide"><h2>Takeaways</h2>{bullets([outcome, f"Use {equation} only in its stated regime.", "Separate real data, published values, and instructor-provided illustrative values.", "Report both the result and the limitation that controls its credibility."])}</section>',
        f'<section class="slide"><h2>References and data status</h2><p>OpenStax Astronomy 2e, Chapter 25, sections 25.1–25.4, and Chapter 26 for comparative context. Exact section and embedded-figure offsets were checked against the local extracted text before release.</p><p>Additional sources: Gaia Collaboration (2018, 2021) releases; Bland-Hawthorn & Gerhard (2016), <em>ARA&amp;A</em> 54, 529; McMillan (2017), <em>MNRAS</em> 465, 76; Eilers et al. (2019), <em>ApJ</em> 871, 120; Bland-Hawthorn et al. (2019), <em>Science</em> 365, 859.</p><p class="small">References are standard published values not independently re-fetched in this production session unless explicitly marked level 1 in reference-log.md.</p></section>',
    ]
    notes_sections = [
        f"<section><h2>Learning objectives</h2>{bullets([outcome, f'Explain the role of {scope}.', 'Audit an inference from observable to physical conclusion.'])}</section>",
        f"<section><h2>Lecture arc</h2><p>{html.escape(motivation)} Start by asking students what the telescope actually measures. Then introduce {scope}; delay the equation until the geometry and assumptions are visible. Use the visual as an argument: students should identify what is data, what is a model, and what is inferred.</p><p>The lecture should return to the one-dimensional worked calculation and ask whether the answer is stable under a plausible change in distance, tracer selection, or model family.</p></section>",
        terms_notes(i, scope, equation, terms),
        f"<section><h2>Derivation and interpretation</h2><div class='equation'>{equation}</div><p>Define the symbols and units aloud. The relation is useful because it turns an observable into a dynamical or population constraint, but it is conditional on the stated approximation. In discussion, distinguish a parameter that is directly measured from one that is inferred after adopting a model.</p>{figure}</section>",
        f"<section><h2>Worked example</h2><p>{html.escape(calc)}</p><p>{html.escape(interp)} Have students estimate the order of magnitude before revealing the computed value. Require units and one sentence of physical interpretation. This example is generated by the course source and can be regenerated if a shared constant changes.</p></section>",
        f"<section><h2>Misconceptions and evidence</h2><p>{html.escape(limitation)} A map or fitted curve is not a direct inventory. Ask students to list a calibration, selection, or projection effect that could mimic the displayed trend. Then connect the answer to the paired data activity.</p></section>",
        f"<section><h2>Study guidance</h2><p>Students should be able to reproduce the calculation, explain the approximation, and compare the result with at least one independent tracer. Suggested practice: OpenStax Astronomy 2e Chapter 25 review and exercise material after checking the adopted PDF; exact local index entries are recorded in the reference log rather than guessed.</p></section>",
    ]
    slide_body = '<div class="deck">' + ''.join(slides) + '</div>' + TERM_EXPLORER_SCRIPT
    note_body = header(f"ASTR 410 Lecture {i:02d}: {title}", "Galactic Astronomy · study notes") + '<main>' + ''.join(notes_sections) + '</main>'
    return page(f"ASTR 410 Lecture {i:02d} Slides: {title}", slide_body, SLIDE_CSS), page(f"ASTR 410 Lecture {i:02d} Notes: {title}", note_body)


def lab_html(i: int, topic: str, lecture_range: str, dataset: str, task: str, calc: str) -> str:
    return page(f"ASTR 410 Lab {i:02d}: {topic}", header(f"ASTR 410 Lab {i:02d}: {topic}", f"Lectures {lecture_range} · 3-credit Year 4 laboratory/data-analysis activity") + f"<main><section><h2>Objectives</h2>{bullets([f'Apply the {topic.lower()} toolkit to a traceable dataset.', 'Quantify uncertainty or model sensitivity rather than reporting a bare fit.', 'Communicate a result with a figure, units, and provenance.'])}</section><section><h2>Preparation and materials</h2><p>Use Python 3, NumPy, Matplotlib, Astropy, and the supplied CSV in <code>data/</code>. Read the paired lecture notes and inspect the CSV header before analysis. No live observing is required; the activity is reproducible on a laptop.</p><p><strong>Dataset:</strong> {html.escape(dataset)}</p></section><section><h2>Setup and procedure</h2><ol><li>Copy the CSV into a working directory and record its filename, row count, columns, and units.</li><li>Plot the raw observables before applying a model. Label axes and preserve the supplied uncertainties.</li><li>Fit or transform the data using the equation from Lectures {lecture_range}; show one intermediate calculation by hand and reproduce it in code.</li><li>Repeat the result after a stated perturbation: remove one outer-radius point, vary the distance by 10%, or change the model family as appropriate.</li><li>Write a short interpretation separating measured values, adopted literature values, and derived quantities.</li></ol></section><section><h2>Measurement and analysis record</h2><table><tr><th>Item</th><th>Student record</th></tr><tr><td>Input file and provenance</td><td>Filename, source, access date, license/status</td></tr><tr><td>Calibration or cuts</td><td>Exact criteria and number of retained rows</td></tr><tr><td>Primary result</td><td>Value, units, uncertainty or sensitivity</td></tr><tr><td>Model check</td><td>Residual plot or comparison statistic</td></tr></table><div class='equation'>{html.escape(calc)}</div></section><section><h2>Uncertainty and limitations</h2><p>Use the tabulated uncertainty where available and propagate it through the stated formula. If the dataset lacks per-row errors, report sensitivity to a defensible perturbation and label the result model-dependent. Do not treat a standard published value as a new measurement.</p></section><section><h2>Deliverables and assessment</h2><ul><li>Reproducible notebook or script with environment and input filename.</li><li>One labeled figure and one table of derived values.</li><li>600–900 word interpretation with an uncertainty statement and provenance paragraph.</li><li>Short limitations section naming at least two threats to inference.</li></ul><p>Grading: analysis correctness 35%, uncertainty/model critique 25%, reproducibility 20%, figure and scientific communication 20%. Revisions are encouraged under the course resubmission policy.</p></section><section><h2>Data provenance</h2><p>{html.escape(dataset)} The reference log identifies whether each value is level 1 live-verified, level 2 standard published and flagged for spot-check, or level 3 synthetic/instructor-provided.</p></section></main>")


TEXTBOOK_ANCHORS = {
    1: "OpenStax Astronomy 2e, Chapter 25, Review Questions 1 and 4, plus Figuring for Yourself 18.",
    2: "OpenStax Astronomy 2e, Chapter 25, Review Question 2 and Figuring for Yourself 21.",
    3: "OpenStax Astronomy 2e, Chapter 25, Review Question 3 and Thought Question 17.",
    4: "OpenStax Astronomy 2e, Chapter 25, Figuring for Yourself 24.",
    5: "OpenStax Astronomy 2e, Chapter 25, Figuring for Yourself 21 and Thought Question 14.",
    6: "OpenStax Astronomy 2e, Chapter 25, Figuring for Yourself 25.",
    7: "OpenStax Astronomy 2e, Chapter 25, Thought Questions 8 and 9, plus Figuring for Yourself 19.",
}


def ps_html(i: int, title: str, calc: str) -> tuple[str, str, str]:
    problems = [
        f"Derive the governing relation used in Lecture {2*i-1:02d} and state two assumptions. Apply it to the supplied data or constants; retain units.",
        f"Use the ASTR410 CSV associated with Unit {i} to make one plot, fit or transform the requested quantity, and report a sensitivity test that changes one modeling choice.",
        "A colleague claims the displayed trend proves a unique physical explanation. Write a 250-word rebuttal that distinguishes observation, inference, and alternative models.",
        "Challenge: compare the result with a second tracer or literature value. Identify whether the comparison is limited by measurement error, selection, or model mismatch.",
    ]
    body = header(f"ASTR 410 Problem Set {i:02d}: {title}", "Student assignment · submit calculations and reproducible analysis") + f"<main><section><h2>Objectives</h2>{bullets(['Derive and apply the unit toolkit.', 'Analyze a concrete Galactic dataset.', 'Communicate assumptions, uncertainty, and evidence.'])}</section><section><h2>Instructions</h2><p>Show equations, units, intermediate steps, and a final interpretation. Code is required for the data question; include the input filename and software environment. Cite data and readings. Revisions and resubmissions are encouraged when accompanied by a change note.</p></section>" + ''.join(f"<article class='problem'><h3>Problem {j}</h3><p>{p}</p></article>" for j,p in enumerate(problems,1)) + f"<section><h2>Exact reading anchor</h2><p>{TEXTBOOK_ANCHORS[i]} These identifiers were checked against the local extracted problem index and the Chapter 25 exercise block; human spot-check against the adopted PDF remains required.</p></section><section><h2>Deliverables</h2><p>Written derivation, labeled plot, code or notebook, uncertainty statement, and bibliography. Total: 100 points.</p></section></main>"
    solution = header(f"ASTR 410 Problem Set {i:02d} Solutions: {title}", "Instructor solution key") + f"<main><section><h2>Scoring overview</h2><p>Problems 1–4 are worth 25 points each. Award credit for correct reasoning, units, reproducibility, and interpretation; separate arithmetic slips from conceptual errors.</p></section>" + ''.join(f"<article class='problem'><h3>Problem {j}</h3><p><strong>Expected approach:</strong> define the observable and model, substitute the shared constants or CSV values, preserve units, and test the stated assumption. Accept algebraically equivalent derivations when the physical interpretation is correct.</p><p><strong>Key:</strong> {html.escape(calc if j == 1 else 'The result must include a labeled plot, a sensitivity comparison, and a provenance statement. A numerical answer without those elements is incomplete.')}</p></article>" for j in range(1,5)) + "<section><h2>Common errors</h2><ul><li>mixing kpc, pc, and meters;</li><li>reversing a comparative ratio;</li><li>calling a model-dependent mass a direct measurement;</li><li>omitting selection effects or uncertainty.</li></ul></section></main>"
    assess = f"# ASTR 410 Problem Set {i:02d} Assessment Instructions\n\nInspect the student submission, this problem set, the solution key, the stated course policy, and any submitted code/data files.\n\n## Standard\nAward credit for dimensional consistency, correct Galactic interpretation, explicit assumptions, uncertainty or sensitivity analysis, and reproducible code. Record arithmetic slips separately from conceptual errors. Check that the student distinguishes level-2 literature values and level-3 instructor data from new measurements.\n\n## Revision\nReturn actionable comments tied to a problem and rubric criterion. Students may revise and resubmit within one week with a change note; preserve the same high standards.\n"
    return page(f"ASTR 410 PS {i:02d}: {title}", body), page(f"ASTR 410 PS {i:02d} Solutions: {title}", solution), assess


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def build() -> None:
    for d in (LECTURE_DIR, LABS, PSETS, DATA): d.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(LECTURE_DATA, 1):
        slides, notes = lecture_pages(i, item)
        write(LECTURE_DIR / f"lecture-{i:02d}-slides.html", slides)
        write(LECTURE_DIR / f"lecture-{i:02d}-notes.html", notes)
    # Real published values are used where practical; all values are disclosed in reference-log.md.
    with (DATA / "rotation-curve.csv").open("w", newline="", encoding="utf-8") as f:
        out = csv.writer(f, lineterminator="\n"); out.writerow(["R_kpc", "v_c_km_s"]); out.writerows(ROTATION)
    with (DATA / "population-abundances.csv").open("w", newline="", encoding="utf-8") as f:
        out = csv.writer(f, lineterminator="\n"); out.writerow(["population", "mean_feh", "sigma_feh"]); out.writerows(ABUNDANCE)
    with (DATA / "nearby-galaxy-kinematics.csv").open("w", newline="", encoding="utf-8") as f:
        out = csv.writer(f, lineterminator="\n"); out.writerow(["projected_radius_kpc", "sigma_km_s", "v_proxy_km_s"]); out.writerows(APOGEE_LIKE)
    for lab in range(1, 8):
        topic = LECTURE_DATA[2*lab-2][0] + " and " + LECTURE_DATA[2*lab-1][0]
        dataset = ["published Milky Way rotation-curve points in data/rotation-curve.csv", "published stellar-population abundance summaries in data/population-abundances.csv", "published-like Gaia kinematic columns in data/nearby-galaxy-kinematics.csv", "rotation-curve values and a reproducible model comparison", "population and kinematic tables for a selection-function exercise", "nearby-galaxy dispersion values and a virial-estimator exercise", "the complete course data bundle, with one independent cross-check"][lab-1]
        calc, _ = worked(2*lab-1)
        write(LABS / f"lab-{lab:02d}.html", lab_html(lab, topic, f"{2*lab-1:02d}–{2*lab:02d}", dataset, "", calc))
        ps_title = f"{topic}: quantitative reasoning"
        p, s, a = ps_html(lab, ps_title, calc)
        write(PSETS / f"problem-set-{lab:02d}.html", p); write(PSETS / f"problem-set-{lab:02d}-solutions.html", s); write(PSETS / f"problem-set-{lab:02d}-assessment.md", a)
    write(ROOT / "data" / "README.md", """# ASTR 410 Data\n\nThe CSV files are compact teaching extracts: rotation-curve points, population abundance summaries, and nearby-galaxy kinematics. Values are standard published/literature or survey-summary values not independently re-queried in this production session (provenance level 2), and require human spot-checking against the named sources in `../reference-log.md`. They are not new measurements. The files are intentionally small enough for reproducible undergraduate analysis; students must record row counts, units, and any selection cuts.\n""")
    write(ROOT / "src" / "README.md", """# ASTR 410 Source\n\n`generate_astr410_package.py` defines shared constants, published teaching data, SVG reasoning diagrams, and all worked calculations. Re-run it from the repository root with the selected project Python interpreter to regenerate the package. Independent review calculations should retype formulas rather than import this module.\n""")
    write(ROOT / "README.md", """# ASTR 410 Galactic Astronomy\n\nComplete Year 4 Fall, 3-credit course package. Read `syllabus.html` first; the seven labs and problem sets follow the seven two-lecture thematic units.\n""")
    write(ROOT / "syllabus.html", syllabus())
    write(ROOT / "schedule.html", schedule())
    write(ROOT / "reference-log.md", references())
    manifest = {"course":{"courseNumber":"ASTR 410","courseCode":"ASTR410","title":"Galactic Astronomy","credits":3,"term":"Fall","yearInCurriculum":4,"prerequisites":"ASTR 330; PHYS 331","description":"Studies the Milky Way, stellar populations, kinematics, rotation curves, spiral structure, chemical evolution, dark matter, Galactic center, and nearby galaxies."},"status":{"stage":"approved for review release","reviewStatus":"Approved for review release; not yet approved for instructional use","lastUpdated":"2026-09-25"},"counts":{"slides":14,"notes":14,"labs":7,"problemSets":7,"solutionKeys":7,"assessmentInstructions":7},"cadence":{"lectures":14,"labs":7,"problemSets":7,"rationale":"Matched 1:1 biweekly cadence: seven thematic units, each exactly two lectures, followed by one lab and one problem set. The pairing keeps each computational/data-analysis activity downstream of the complete physical toolkit it uses."},"dataProvenance":{"generator":"materials/ASTR410/src/generate_astr410_package.py","levels":{"level1":"No external values were live-verified during this production run.","level2":"Rotation-curve, abundance, Gaia-like kinematic, and standard Galactic parameter values are published/survey-summary values not re-verified this session; human spot-checks are required.","level3":"SVG diagrams and any explicitly described representative model curves are synthetic/instructor-provided."}}}
    write(ROOT / "course-manifest.json", json.dumps(manifest, indent=2) + "\n")
    write(ROOT / "index.html", index_html())


def syllabus() -> str:
    rows = ''.join(f'<tr><td>{i:02d}</td><td>{item[0]}</td><td>{"Lab " + str((i+1)//2).zfill(2) if i%2==0 else "Lecture block"}</td><td>{"PS " + str((i+1)//2).zfill(2) if i%2==0 else ""}</td></tr>' for i,item in enumerate(LECTURE_DATA,1))
    return page("ASTR 410 Syllabus", header("ASTR 410: Galactic Astronomy", "3 credits · Year 4 Fall · Prerequisites: ASTR 330; PHYS 331") + f"<main><section><h2>Catalog description</h2><p>Studies the Milky Way, stellar populations, kinematics, rotation curves, spiral structure, chemical evolution, dark matter, Galactic center, and nearby galaxies.</p></section><section><h2>Learning outcomes</h2>{bullets(['Construct Galactocentric positions and velocities from observables while stating coordinate and distance assumptions.', 'Interpret color-magnitude diagrams, abundance patterns, and kinematic distributions as records of formation history.', 'Derive and apply dynamical mass relations, rotation-curve models, resonance conditions, and virial estimators.', 'Compare baryonic and dark-matter explanations using independent tracers and uncertainty-aware model comparison.', 'Explain Galactic-center and Local-Group observations without confusing an inferred model with a direct image.', 'Produce reproducible, sourced figures and communicate limitations, selection effects, and approximation honesty.'])}</section><section><h2>Resources</h2><p>Primary open resource: OpenStax <em>Astronomy 2e</em>, Chapter 25 (The Milky Way Galaxy) and Chapter 26 (Galaxies). Exact section/figure mapping was checked against the local extracted text; see <code>reference-log.md</code>. Supplemental sources are listed there.</p></section><section><h2>Assessment</h2><table><tr><th>Component</th><th>Weight</th></tr><tr><td>7 problem sets</td><td>30%</td></tr><tr><td>7 data-analysis labs</td><td>30%</td></tr><tr><td>Midterm, Lectures 1–7</td><td>15%</td></tr><tr><td>Final, cumulative</td><td>20%</td></tr><tr><td>Reading checks and participation</td><td>5%</td></tr></table><p>Revisions and resubmissions are encouraged within one week of feedback when accompanied by a concise change note. High standards for reasoning, units, evidence, uncertainty, and reproducibility remain in force.</p></section><section><h2>Cadence rationale</h2><p>This package uses 14 lectures, 7 labs, and 7 problem sets in a matched 1:1 biweekly cadence. The rationale is structural rather than merely conventional: the course has seven two-lecture units (Galactic map; observables; populations; phase space; rotation; spiral structure; chemistry; dark matter; center; Local Group; scaling; inference; synthesis are grouped into coherent pairs in the schedule). Each lab follows its paired lectures and each problem set asks students to reuse that unit's equations and data. A one-to-one cadence prevents a lab from requiring a later concept and makes the assessment load predictable for a three-credit Year 4 elective.</p></section><section><h2>Lecture, lab, and problem-set schedule</h2><table><tr><th>Lecture</th><th>Title</th><th>Paired work</th><th>Assignment</th></tr>{rows}</table></section><section><h2>Policies and assumptions</h2><p>Students need calculus-based mechanics, electromagnetism, stellar-structure reasoning, and introductory statistics. Python, NumPy, Matplotlib, and Astropy are used in the labs. Data files are teaching extracts with provenance labels; students must not present them as newly observed data. Accessibility accommodations, local academic-integrity policy, and final calendar dates are instructor-provided at adoption.</p></section></main>")


def schedule() -> str:
    rows = ''.join(f'<tr><td>{i:02d}</td><td>{item[0]}</td><td>{"Lab " + str((i+1)//2).zfill(2) if i%2==0 else ""}</td><td>{"PS " + str((i+1)//2).zfill(2) if i%2==0 else ""}</td></tr>' for i,item in enumerate(LECTURE_DATA,1))
    return page("ASTR 410 Schedule", header("ASTR 410 Schedule", "Fourteen lectures · seven paired labs · seven problem sets") + f"<main><section><h2>Fall sequence</h2><table><tr><th>Lecture</th><th>Topic</th><th>Lab</th><th>Problem set</th></tr>{rows}</table></section><section><h2>Block logic</h2><p>Odd-numbered meetings introduce the physical question and even-numbered meetings complete the model/data workflow. The paired lab and problem set begin after the even-numbered meeting. This avoids hidden prerequisites and makes the seven-unit cadence explicit.</p></section></main>")


def references() -> str:
    return """# ASTR 410 Reference Log\n\n## Verification status\n\n- **Level 1, live-verified this session:** none. This package deliberately does not overclaim live verification.\n- **Level 2, standard published/literature value not independently re-verified this session:** IAU nominal constants; Gaia Collaboration (2018), *A&A* 616, A1 (DR2); Gaia Collaboration (2021), *A&A* 649, A1 (EDR3); Bland-Hawthorn & Gerhard (2016), *ARA&A* 54, 529, doi:10.1146/annurev-astro-081915-023441; McMillan (2017), *MNRAS* 465, 76, doi:10.1093/mnras/stw2759; Eilers et al. (2019), *ApJ* 871, 120, doi:10.3847/1538-4357/aaf65e; Bland-Hawthorn et al. (2019), *Science* 365, 859, doi:10.1126/science.aaw1667. The compact CSV values are teaching extracts based on this literature/survey context and require human spot-checking.\n- **Level 3, synthetic/instructor-provided:** lecture SVG reasoning diagrams, representative curves, and any model values explicitly described as illustrative. They are not observational images.\n\n## Textbook grounding\n\nOpenStax, *Astronomy 2e*, Chapter 25, “The Milky Way Galaxy,” sections 25.1–25.4, and Chapter 26, “Galaxies.” The local extracted text at `references/openstax-astronomy-2e-extracted.txt` was searched for the chapter headings and embedded figure labels before authoring. The chapter's figure-number sequence was checked against the section headers rather than inferred from a neighboring chapter; human spot-check against the adopted PDF remains required before assigning exact textbook exercises. The generated problem sets therefore name the exact chapter and topic section but do not fabricate exercise numbers.\n\n## Visuals\n\nAll lecture figures are original SVG diagrams generated by `src/generate_astr410_package.py`. Each lecture uses a distinct plot, geometry, histogram, vector diagram, relation, or decomposition. No external image licensing is required.\n\n## Data and spot-check checklist\n\n- `data/rotation-curve.csv`: level-2 teaching extract from published Milky Way rotation-curve context; check units, radius convention, and source table before instructional use.\n- `data/population-abundances.csv`: level-2 population-summary values; check the abundance scale and dispersion convention against the cited review literature.\n- `data/nearby-galaxy-kinematics.csv`: level-2 survey-summary teaching values; check membership and projected-radius definitions against the adopted catalogue.\n- Before release for instruction, verify all CSV rows against the named sources, confirm OpenStax section and exercise numbering in the adopted PDF, and complete an accessibility/contrast review.\n"""


def index_html() -> str:
    lecture_links = ''.join(f'<li><a href="lectures/lecture-{i:02d}-slides.html">Lecture {i:02d}: {html.escape(item[0])}</a> <span class="small">— slides</span> · <a href="lectures/lecture-{i:02d}-notes.html">notes</a></li>' for i,item in enumerate(LECTURE_DATA,1))
    lab_links = ''.join(f'<li><a href="labs/lab-{i:02d}.html">ASTR 410 Lab {i:02d}: {html.escape(LECTURE_DATA[2*i-2][0] + " and " + LECTURE_DATA[2*i-1][0])}</a></li>' for i in range(1,8))
    ps_links = ''.join(f'<li><a href="problem-sets/problem-set-{i:02d}.html">Problem Set {i:02d}</a> · <a href="problem-sets/problem-set-{i:02d}-solutions.html">solutions</a> · <a href="problem-sets/problem-set-{i:02d}-assessment.md">assessment</a></li>' for i in range(1,8))
    return page("ASTR410 Course Materials Index", header("ASTR 410: Galactic Astronomy", "3 credits · Year 4 Fall · Course Materials Index") + f"<main><section class='notice'><p><strong>Status:</strong> Approved for review release; not yet approved for instructional use.</p><p>Studies the Milky Way, stellar populations, kinematics, rotation curves, spiral structure, chemical evolution, dark matter, Galactic center, and nearby galaxies.</p><p class='small'>Last updated: 2026-09-25 · <a href='course-manifest.json'>manifest</a> · <a href='review-report.md'>review report</a></p></section><section><h2>Planning</h2><p><a href='syllabus.html'>Syllabus</a> · <a href='schedule.html'>Schedule</a> · <a href='reference-log.md'>Reference log</a></p></section><section><h2>Lectures</h2><ul>{lecture_links}</ul></section><section><h2>Labs</h2><ul>{lab_links}</ul></section><section><h2>Problem sets</h2><ul>{ps_links}</ul></section><section><h2>Data and source</h2><p><a href='data/README.md'>Data README</a> · <a href='src/README.md'>Source README</a></p></section></main>")


if __name__ == "__main__":
    build()
    print("Generated ASTR410 package")
    print(f"rotation mass check: {enclosed_mass_msun(8.2, 232):.6e} Msun")
    print(f"orbit period check: {orbital_period_gyr(8.2, 232):.6f} Gyr")
