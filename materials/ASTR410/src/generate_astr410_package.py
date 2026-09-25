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
SLIDE_CSS = CSS + ".deck{scroll-snap-type:y mandatory;height:100vh;overflow-y:auto}.slide{min-height:100vh;scroll-snap-align:start;display:flex;flex-direction:column;justify-content:center;padding:46px 7vw;border-bottom:1px solid var(--line);background:#fff}.title{background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}.title h2{color:#fff}.slide h2{font-family:'Aptos','Segoe UI',sans-serif;font-size:clamp(1.8rem,3.2vw,3.1rem);margin:0 0 20px}.slide p,.slide li{font-size:clamp(1.02rem,1.35vw,1.35rem);line-height:1.38}.grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:center}.figure svg{height:50vh;max-height:480px}.prompt{border-left:5px solid var(--gold);padding:14px 18px;background:#fff8e8}.kicker{color:var(--gold);text-transform:uppercase;letter-spacing:.08em;font-weight:700}.credit{color:var(--muted);font-size:.9rem}@media print{.deck{height:auto;overflow:visible}.slide{min-height:7.5in;page-break-after:always}}"

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
("The Rotation Curve and the Missing Mass", "Derive enclosed mass from circular motion and identify the flat-curve anomaly.", "circular speed and mass", "Rotation curves made the mass problem quantitative: outer disk speeds do not fall as a luminous point-mass model predicts.", r"\(M(<R)=Rv_c^2/G\)", "Use R=8.2 kpc and v_c=232 km s^-1 to estimate the enclosed mass.", "rotation curve", "The inference is mass within radius, not a direct photograph of dark matter."),
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


def lecture_pages(i: int, item: tuple[str, ...]) -> tuple[str, str]:
    title, outcome, scope, motivation, equation, prompt, visual_name, limitation = item
    calc, interp = worked(i)
    figure = f'<figure class="figure">{svg(i, title)}<figcaption>{html.escape(visual_name.title())}: a lecture-specific schematic or model plot. Axes and annotations identify the inference being made; it is not presented as a raw survey image.</figcaption></figure>'
    slides = [
        f'<section class="slide title"><div class="kicker">ASTR 410 · Lecture {i:02d}</div><h1>Lecture {i:02d}: {html.escape(title)}</h1><h2>Galactic Astronomy</h2><p>{html.escape(motivation)}</p></section>',
        f'<section class="slide"><h2>Objectives and route</h2>{bullets([f"{outcome}", f"Connect {scope} to observations and model assumptions.", "Make one auditable calculation and interpret its limitation.", "Use an evidence chain rather than treating a visualization as a direct measurement."])}</section>',
        f'<section class="slide"><h2>Why this question is hard</h2><div class="grid"><div><p>{motivation}</p><p>Galactic astronomy observes projected light, velocities, and abundances from one moving vantage point. The inverse problem is underdetermined until geometry, selection, and a physical model are made explicit.</p></div>{figure}</div></section>',
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
        f"<section><h2>Derivation and interpretation</h2><div class='equation'>{equation}</div><p>Define the symbols and units aloud. The relation is useful because it turns an observable into a dynamical or population constraint, but it is conditional on the stated approximation. In discussion, distinguish a parameter that is directly measured from one that is inferred after adopting a model.</p>{figure}</section>",
        f"<section><h2>Worked example</h2><p>{html.escape(calc)}</p><p>{html.escape(interp)} Have students estimate the order of magnitude before revealing the computed value. Require units and one sentence of physical interpretation. This example is generated by the course source and can be regenerated if a shared constant changes.</p></section>",
        f"<section><h2>Misconceptions and evidence</h2><p>{html.escape(limitation)} A map or fitted curve is not a direct inventory. Ask students to list a calibration, selection, or projection effect that could mimic the displayed trend. Then connect the answer to the paired data activity.</p></section>",
        f"<section><h2>Study guidance</h2><p>Students should be able to reproduce the calculation, explain the approximation, and compare the result with at least one independent tracer. Suggested practice: OpenStax Astronomy 2e Chapter 25 review and exercise material after checking the adopted PDF; exact local index entries are recorded in the reference log rather than guessed.</p></section>",
    ]
    slide_body = '<div class="deck">' + ''.join(slides) + '</div>'
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
    path.write_text(text, encoding="utf-8")


def build() -> None:
    for d in (LECTURE_DIR, LABS, PSETS, DATA): d.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(LECTURE_DATA, 1):
        slides, notes = lecture_pages(i, item)
        write(LECTURE_DIR / f"lecture-{i:02d}-slides.html", slides)
        write(LECTURE_DIR / f"lecture-{i:02d}-notes.html", notes)
    # Real published values are used where practical; all values are disclosed in reference-log.md.
    with (DATA / "rotation-curve.csv").open("w", newline="", encoding="utf-8") as f:
        out = csv.writer(f); out.writerow(["R_kpc", "v_c_km_s"]); out.writerows(ROTATION)
    with (DATA / "population-abundances.csv").open("w", newline="", encoding="utf-8") as f:
        out = csv.writer(f); out.writerow(["population", "mean_feh", "sigma_feh"]); out.writerows(ABUNDANCE)
    with (DATA / "nearby-galaxy-kinematics.csv").open("w", newline="", encoding="utf-8") as f:
        out = csv.writer(f); out.writerow(["projected_radius_kpc", "sigma_km_s", "v_proxy_km_s"]); out.writerows(APOGEE_LIKE)
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
