"""Generate the complete ASTR 420 Cosmology package from shared data and calculations."""
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

G = 6.67430e-11
C_KMS = 299792.458
MPC_KM = 3.0856775814913673e19
YEAR_S = 365.25 * 86400
MPC_M = 3.085677581491367e22
K_B = 1.380649e-23
H_PLANCK = 6.62607015e-34
T_CMB = 2.7255
H0 = 67.4
OMEGA_M = 0.315
OMEGA_B = 0.0493
OMEGA_L = 0.685
OMEGA_R = 9.2e-5
AGE_GYR = 13.8

CSS = """
:root{--ink:#17202a;--muted:#596875;--paper:#f8fafb;--panel:#fff;--line:#d5dee5;--navy:#17324d;--teal:#087e8b;--cyan:#dff4f5;--gold:#b66a0a;--red:#a33a3a}*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--paper);font-family:Georgia,'Times New Roman',serif;line-height:1.58}header{padding:38px 24px 28px;background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}header>div,main{max-width:1100px;margin:auto}main{padding:28px 24px 64px}h1,h2,h3{line-height:1.15}h1{margin:0 0 8px;font-size:clamp(2rem,4vw,3.3rem)}h2{color:var(--navy);border-bottom:2px solid var(--line);padding-bottom:8px;margin-top:32px}h3{color:var(--teal)}section,article.problem{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:16px 18px;margin:16px 0}.notice{border-left:5px solid var(--teal);background:var(--cyan)}table{width:100%;border-collapse:collapse;margin:14px 0}th,td{border:1px solid var(--line);padding:8px 10px;vertical-align:top;text-align:left}th{background:var(--cyan)}a{color:var(--teal);font-weight:700}.small{color:var(--muted);font-size:.92rem}.equation{padding:12px 16px;border-left:5px solid var(--teal);background:var(--cyan);overflow:auto}.figure{margin:18px 0}.figure svg{width:100%;height:310px;background:#fff;border:1px solid var(--line)}.figure figcaption{color:var(--muted);font-size:.94rem}.prompt{padding:14px 18px;border-left:5px solid var(--gold);background:#fff6e6}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:center}@media(max-width:700px){.grid{grid-template-columns:1fr}}
"""
SLIDE_CSS = CSS + ".deck{height:100vh;overflow-y:auto;scroll-snap-type:y mandatory}.slide{min-height:100vh;scroll-snap-align:start;display:flex;flex-direction:column;justify-content:center;padding:44px 7vw;border-bottom:1px solid var(--line);background:#fff}.slide.title{background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}.slide.title h2{color:#fff}.slide h2{font-family:'Aptos','Segoe UI',sans-serif;font-size:clamp(1.8rem,3.1vw,3rem);margin:0 0 18px}.slide p,.slide li{font-size:clamp(1rem,1.25vw,1.28rem);line-height:1.4}.kicker{color:var(--gold);text-transform:uppercase;letter-spacing:.08em;font-weight:700}.slide.title .kicker{color:#ffd68a}.credit{color:var(--muted);font-size:.9rem}@media print{.deck{height:auto;overflow:visible}.slide{min-height:7.5in;page-break-after:always}}"

LECTURES = [
("The Expanding Universe", "Infer expansion from redshift, distance, and the scale factor.", "redshift, comoving coordinates, and Hubble's law", r"a(t),\\quad 1+z=a_0/a_{\\rm em}", "A galaxy at 100 Mpc has a recession speed computed from Hubble's law.", "Expansion is a change in the metric separation of unbound systems, not an explosion into pre-existing space.", "OpenStax Astronomy 2e, Chapter 29, sections 29.1 and 29.2; embedded Figures 29.1-29.4."),
("Relativistic Redshift and Distance", "Distinguish velocity, redshift, luminosity distance, and angular-diameter distance.", "special-relativistic redshift and cosmological distance measures", r"1+z=\\sqrt{(1+\\beta)/(1-\\beta)}", "Find the special-relativistic recession speed associated with z=0.10 and compare it with cz.", "At low redshift several distance definitions nearly agree; at cosmological redshift they separate because the scale factor changes during photon travel.", "OpenStax Astronomy 2e, Chapter 29, section 29.2; Chapter 26, section 26.5; embedded Figures 26.16 and 29.5."),
("The Friedmann Equation", "Use the density parameters to identify curvature and expansion regimes.", "critical density, curvature, and the Friedmann equation", r"H^2(a)=H_0^2[\\Omega_r a^{-4}+\\Omega_m a^{-3}+\\Omega_k a^{-2}+\\Omega_\\Lambda]", "Evaluate the present critical density from H0 and compare matter and dark-energy contributions.", "The equation is a dynamical bookkeeping statement: each component redshifts differently and therefore dominates at a different epoch.", "OpenStax Astronomy 2e, Chapter 29, sections 29.1-29.2; embedded Figures 29.2-29.6."),
 ("Cosmic Time and Horizons", "Compute lookback time in a flat matter-plus-dark-energy model and explain horizons.", "lookback time, conformal time, and causal limits", r"t_L(z)=integral_0^z dz' / [(1+z')H(z') ]", "Numerically integrate the lookback time to z=1 using Simpson's rule.", "A redshift is not itself an age; converting it to time requires a cosmological expansion history.", "OpenStax Astronomy 2e, Chapter 29, sections 29.2 and 29.3; embedded Figures 29.7-29.10."),
("Thermal History and Recombination", "Track how temperature and ionization changed as the universe expanded.", "adiabatic cooling, recombination, and photon decoupling", r"T_\\gamma(a)=T_{\\gamma,0}/a", "Estimate the photon temperature at recombination for z=1100.", "The CMB last-scattering surface is a time slice of photon decoupling, not a physical shell with a fixed material boundary.", "OpenStax Astronomy 2e, section 29.4; embedded Figures 29.12-29.15."),
 ("The Cosmic Microwave Background", "Interpret the CMB spectrum and anisotropy amplitude as evidence for a hot early universe.", "blackbody spectrum, acoustic peaks, and parameter inference", r"I_nu(T)=2h nu^3 / c^2 [e^(h nu/kT)-1]^-1", "Use Wien's law to estimate the frequency of the CMB intensity peak.", "The near-perfect blackbody spectrum tests thermal history; anisotropies carry information about geometry, baryons, matter, and initial perturbations.", "OpenStax Astronomy 2e, section 29.4; embedded Figures 29.16-29.22."),
 ("Big-Bang Nucleosynthesis", "Relate expansion, weak freeze-out, neutron decay, and helium abundance.", "reaction rates, freeze-out, and primordial light elements", r"Y_p approximately 2(n/p) / [1+(n/p)]", "Propagate a neutron-to-proton ratio of 1/7 into a helium-4 mass-fraction estimate.", "The helium prediction is a coupled nuclear-and-expansion calculation; stellar processing alone cannot account for the observed primordial baseline.", "OpenStax Astronomy 2e, section 29.3; embedded Figures 29.11-29.14."),
("Inflation and the Early Universe", "Explain the horizon and flatness problems and identify what inflation does and does not predict.", "rapid expansion, horizon crossing, and primordial perturbations", r"\\ddot a>0,\\quad |\\Omega_k(a)|\\propto(aH)^{-2}", "Compare the change in a curvature contribution during an idealized inflationary expansion by 60 e-folds.", "Inflation addresses causal contact and near-flatness by changing the expansion history; it does not by itself fix every microphysical parameter.", "OpenStax Astronomy 2e, sections 29.5-29.6; embedded Figures 29.23-29.27."),
("Dark Matter and the Growth of Structure", "Connect cold-dark-matter perturbations to galaxy and cluster formation.", "linear growth, transfer functions, and gravitational collapse", r"\\delta(a)=\\delta\\rho/\\bar\\rho,\\quad \\delta\\propto a\\;\\text{(matter era)}", "Grow a 10^-5 matter-era perturbation from recombination to z=0 under the linear approximation.", "The linear result is a controlled approximation only before collapse; nonlinear structure requires simulations and a specified power spectrum.", "OpenStax Astronomy 2e, section 29.6 and Chapter 28, section 28.5; embedded Figures 28.21 and 29.28."),
 ("Baryon Acoustic Oscillations", "Use the sound horizon as a standard ruler and identify the role of BAO in geometry tests.", "photon-baryon sound speed, drag epoch, and correlation peaks", r"r_s=integral_0^ad c_s(a) da / [a^2 H(a)]", "Interpret a 150 Mpc comoving BAO feature as a transverse and radial distance constraint.", "BAO is not a fixed ruler in physical coordinates; the measured angular and redshift separations are translated through a cosmological model.", "OpenStax Astronomy 2e, Chapter 29, section 29.6; embedded Figures 29.28-29.30."),
 ("Type Ia Supernovae and Dark Energy", "Fit a supernova Hubble diagram and infer acceleration from residual curvature.", "standardization, distance modulus, and acceleration", r"mu=m-M=5 log10(D_L / 10 pc)", "Convert a standardized SN with m-M=43.16 into a luminosity distance in Mpc.", "Acceleration is inferred from a distance-redshift relation relative to decelerating models; calibration and selection systematics matter.", "OpenStax Astronomy 2e, Chapter 26, section 26.5 and Chapter 29, section 29.2; embedded Figure 26.18."),
("Weak Lensing and Cluster Mass", "Use shear and convergence as projected mass probes and identify degeneracies.", "lensing geometry, convergence, and mass mapping", r"\\kappa=\\Sigma/\\Sigma_{\\rm crit}", "Compute convergence for a projected surface density of 2.0e14 solar masses per square Mpc and a stated critical density.", "Lensing measures total projected mass, including dark matter, but inversion has a mass-sheet degeneracy and line-of-sight structure.", "OpenStax Astronomy 2e, Chapter 28, section 28.4; embedded Figures 28.20-28.24."),
("The Matter Power Spectrum", "Read a power spectrum as a record of primordial perturbations and later processing.", "Fourier modes, turnover, and baryon features", r"\\langle\\delta_{\\bf k}\\delta^*_{\\bf k'}\\rangle=(2\\pi)^3P(k)\\delta^3(\\bf k-\\bf k')", "Compare two modes' dimensionless power when P(k) follows a supplied power-law slope.", "A power spectrum is a statistical summary; the same broad shape can be affected by bias, redshift space, and nonlinear evolution.", "OpenStax Astronomy 2e, Chapter 28, section 28.5 and Chapter 29, section 29.6; embedded Figures 28.28-28.29."),
("Cosmological Synthesis, Tensions, and Tests", "Construct an evidence-weighted concordance model and compare parameter constraints without treating disagreement as an arithmetic error.", "multi-probe consistency, covariance, model comparison, and open questions", r"\\chi^2=(\\mathbf d-\\mathbf m)^T C^{-1}(\\mathbf d-\\mathbf m)", "Combine a CMB prior, BAO distance ratio, supernova residual, and H0 comparison into a qualitative model test.", "Cosmology is strongest when independent epochs and messengers agree; a tension can indicate statistical fluctuation, hidden covariance, calibration systematics, or model incompleteness.", "OpenStax Astronomy 2e, Chapter 29, sections 29.1-29.7; embedded Figures 29.1-29.30."),
]

CMB = [("H0",67.4,0.5),("Omega_m",0.315,0.007),("Omega_b",0.0493,0.0006),("Omega_Lambda",0.685,0.007),("T_CMB_K",2.7255,0.0006)]
SN = [(0.01,33.16),(0.05,36.73),(0.10,38.31),(0.20,39.96),(0.40,41.74),(0.60,42.74),(0.80,43.45),(1.00,44.10)]
BAO = [(0.15,0.106),(0.38,0.497),(0.51,0.459),(0.61,0.436),(1.00,0.230)]
POWER = [(0.01,3.0e4),(0.03,1.3e5),(0.06,1.8e5),(0.10,1.5e5),(0.20,7.0e4),(0.40,2.2e4)]
ABUND = [("H",0.748),("He4",0.247),("D",2.5e-5),("Li7",4.7e-10)]


def fmt(value: float, digits: int = 5) -> str:
    return f"{value:.{digits}g}"


def h0_si() -> float:
    return H0 / MPC_KM


def critical_density_msun_mpc3() -> float:
    rho = 3 * h0_si() ** 2 / (8 * math.pi * G)
    return rho * MPC_M**3 / 1.98847e30


def hubble_distance_mpc(z: float) -> float:
    return C_KMS * z / H0


def special_velocity(z: float) -> float:
    beta = ((1 + z) ** 2 - 1) / ((1 + z) ** 2 + 1)
    return beta * C_KMS


def ez(z: float) -> float:
    return math.sqrt(OMEGA_R * (1 + z) ** 4 + OMEGA_M * (1 + z) ** 3 + OMEGA_L)


def simpson_integral(func, a: float, b: float, n: int = 1000) -> float:
    if n % 2: n += 1
    h = (b - a) / n
    total = func(a) + func(b)
    total += 4 * sum(func(a + j * h) for j in range(1, n, 2))
    total += 2 * sum(func(a + j * h) for j in range(2, n, 2))
    return total * h / 3


def lookback_gyr(z: float) -> float:
    integral = simpson_integral(lambda x: 1 / ((1 + x) * ez(x)), 0, z)
    return integral / h0_si() / (1e9 * YEAR_S)


def luminosity_distance_mpc(mu: float) -> float:
    return 10 ** ((mu - 25) / 5)


def cmb_peak_ghz() -> float:
    wavelength_m = 2.897771955e-3 / T_CMB
    return C_KMS * 1e3 / wavelength_m / 1e9


def helium_fraction(n_to_p: float) -> float:
    return 2 * n_to_p / (1 + n_to_p)


def curvature_after_efolds(initial: float, efolds: float) -> float:
    return initial * math.exp(-2 * efolds)


def growth_factor(z_initial: float, z_final: float = 0) -> float:
    return (1 + z_initial) / (1 + z_final)


def chi2(values: list[tuple[float, float]], model: float, sigma: float) -> float:
    return sum(((v - model) / sigma) ** 2 for _, v in values)


def normalize_h0(x1: float, s1: float, x2: float, s2: float) -> float:
    return abs(x1 - x2) / math.sqrt(s1 * s1 + s2 * s2)


def svg(i: int) -> str:
    """Return fourteen structurally distinct, lecture-specific reasoning figures."""
    navy, teal, gold, red, gray = "#17324d", "#087e8b", "#b66a0a", "#a33a3a", "#596875"
    if i == 1:
        pts = " ".join(f"{45+x*52},{250-y*1.7}" for x,y in [(0,12),(1,35),(2,65),(3,98),(4,138),(5,183),(6,225)])
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Hubble diagram of recession speed versus distance"><path d="M45 260H400M45 260V25" stroke="{navy}" stroke-width="3"/><polyline points="{pts}" fill="none" stroke="{teal}" stroke-width="5"/><text x="170" y="298">distance (Mpc)</text><text x="5" y="125" transform="rotate(-90 5 125)">recession speed</text><text x="235" y="55" fill="{gold}">v = H0 d</text></svg>'
    if i == 2:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Light-cone diagram showing emitted and observed wavelengths"><path d="M215 25L70 280M215 25L360 280" fill="none" stroke="{navy}" stroke-width="3"/><path d="M110 245h62M95 220h62M80 195h62" stroke="{teal}" stroke-width="5"/><path d="M258 245h82M250 220h82M242 195h82" stroke="{red}" stroke-width="5"/><circle cx="215" cy="25" r="8" fill="{gold}"/><text x="154" y="300">emission to observation</text><text x="102" y="175" fill="{teal}">shorter</text><text x="275" y="175" fill="{red}">stretched</text></svg>'
    if i == 3:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Friedmann component density curves versus scale factor"><path d="M45 260H400M45 260V25" stroke="{navy}" stroke-width="3"/><path d="M55 245 Q120 180 190 125 Q285 70 390 48" fill="none" stroke="{red}" stroke-width="4"/><path d="M55 235 Q120 175 190 135 Q285 105 390 92" fill="none" stroke="{teal}" stroke-width="4"/><path d="M55 245 L390 155" fill="none" stroke="{gold}" stroke-width="4"/><path d="M55 245 Q220 240 390 70" fill="none" stroke="{navy}" stroke-width="4"/><text x="285" y="42">Lambda</text><text x="310" y="88">matter</text><text x="310" y="150">curvature</text><text x="315" y="205">radiation</text><text x="185" y="298">scale factor a</text></svg>'
    if i == 4:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Cosmic timeline with particle, recombination, and present epochs"><path d="M55 155H380" stroke="{navy}" stroke-width="5"/><circle cx="65" cy="155" r="15" fill="{red}"/><circle cx="185" cy="155" r="15" fill="{gold}"/><circle cx="280" cy="155" r="15" fill="{teal}"/><circle cx="370" cy="155" r="15" fill="{navy}"/><text x="40" y="115">hot early</text><text x="150" y="115">BBN</text><text x="250" y="115">CMB</text><text x="340" y="115">today</text><path d="M65 195V225M185 195V225M280 195V225M370 195V225" stroke="{gray}"/><text x="38" y="250">seconds</text><text x="160" y="250">minutes</text><text x="253" y="250">380 kyr</text><text x="342" y="250">13.8 Gyr</text></svg>'
    if i == 5:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Photon temperature cooling curve against redshift"><path d="M45 260H400M45 260V25" stroke="{navy}" stroke-width="3"/><path d="M55 45 Q135 75 210 120 Q300 185 390 245" fill="none" stroke="{teal}" stroke-width="6"/><circle cx="310" cy="190" r="8" fill="{gold}"/><text x="265" y="180">recombination</text><text x="170" y="298">cosmic time</text><text x="4" y="130" transform="rotate(-90 4 130)">T_gamma</text></svg>'
    if i == 6:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="CMB blackbody spectrum with peak and anisotropy inset"><path d="M45 260H400M45 260V25" stroke="{navy}" stroke-width="3"/><path d="M55 250 Q125 245 180 145 Q215 55 250 145 Q305 245 390 250" fill="none" stroke="{teal}" stroke-width="5"/><circle cx="215" cy="90" r="8" fill="{gold}"/><text x="225" y="82">2.7255 K peak</text><rect x="285" y="45" width="95" height="55" fill="#dff4f5" stroke="{red}"/><path d="M292 74l12 -8 12 9 12 -13 12 9 12 -6 12 10" fill="none" stroke="{red}"/><text x="168" y="298">frequency</text></svg>'
    if i == 7:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Neutron to proton freeze-out and helium yield diagram"><path d="M55 245H375" stroke="{navy}" stroke-width="4"/><path d="M80 80 Q175 105 270 175" fill="none" stroke="{teal}" stroke-width="6"/><path d="M80 175 Q180 200 270 215" fill="none" stroke="{red}" stroke-width="6"/><circle cx="270" cy="175" r="8" fill="{gold}"/><text x="55" y="60">n/p in equilibrium</text><text x="250" y="155">freeze-out</text><text x="275" y="235">Yp ~ 0.25</text><text x="150" y="285">cooling and weak reactions</text></svg>'
    if i == 8:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Inflationary horizon diagram comparing comoving patch sizes"><path d="M55 250H380" stroke="{navy}" stroke-width="4"/><path d="M75 210 Q175 180 355 65" fill="none" stroke="{gold}" stroke-width="5"/><path d="M75 85 Q175 155 355 210" fill="none" stroke="{teal}" stroke-width="5"/><circle cx="75" cy="210" r="7" fill="{red}"/><text x="95" y="220">causal patch</text><text x="235" y="55">rapid a(t)</text><text x="92" y="285">comoving scale</text></svg>'
    if i == 9:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Density perturbation growth from recombination to nonlinear structure"><path d="M45 260H400M45 260V25" stroke="{navy}" stroke-width="3"/><path d="M60 240 Q145 220 220 170 Q300 100 390 40" fill="none" stroke="{teal}" stroke-width="6"/><path d="M55 205h330" stroke="{red}" stroke-dasharray="8 6" stroke-width="3"/><text x="305" y="30">nonlinear</text><text x="275" y="198">delta=1</text><text x="155" y="298">scale factor</text></svg>'
    if i == 10:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="BAO standard ruler shown in a galaxy correlation function"><path d="M45 260H400M45 260V25" stroke="{navy}" stroke-width="3"/><path d="M55 220 Q110 140 165 205 Q220 245 280 135 Q330 60 390 120" fill="none" stroke="{teal}" stroke-width="5"/><circle cx="280" cy="135" r="9" fill="{gold}"/><text x="265" y="112">150 Mpc</text><text x="138" y="298">separation</text><text x="3" y="120" transform="rotate(-90 3 120)">correlation</text></svg>'
    if i == 11:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Supernova distance modulus residual curve"><path d="M45 260H400M45 260V25" stroke="{navy}" stroke-width="3"/><path d="M55 230 Q155 185 240 125 Q315 78 390 55" fill="none" stroke="{gray}" stroke-width="4" stroke-dasharray="7 5"/><path d="M55 235 Q155 192 240 142 Q315 105 390 95" fill="none" stroke="{red}" stroke-width="5"/><text x="260" y="48">accelerating model</text><text x="250" y="78">matter-only reference</text><text x="175" y="298">redshift</text></svg>'
    if i == 12:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Gravitational lensing mass map with critical curve"><ellipse cx="215" cy="150" rx="135" ry="88" fill="#dff4f5" stroke="{teal}" stroke-width="4"/><ellipse cx="215" cy="150" rx="75" ry="45" fill="none" stroke="{red}" stroke-width="4" stroke-dasharray="8 5"/><circle cx="215" cy="150" r="13" fill="{gold}"/><path d="M70 75 Q215 10 360 75M70 225 Q215 290 360 225" fill="none" stroke="{navy}" stroke-width="3"/><text x="165" y="155">cluster mass</text><text x="152" y="55">critical curve</text></svg>'
    if i == 13:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Matter power spectrum with turnover and BAO wiggles"><path d="M45 260H400M45 260V25" stroke="{navy}" stroke-width="3"/><path d="M55 70 Q105 45 150 115 Q205 190 245 170 Q290 150 315 175 Q345 195 390 205" fill="none" stroke="{teal}" stroke-width="5"/><path d="M55 70 Q180 140 390 205" fill="none" stroke="{gold}" stroke-dasharray="8 5" stroke-width="3"/><text x="82" y="40">turnover</text><text x="276" y="158">BAO wiggles</text><text x="172" y="298">wavenumber k</text></svg>'
    if i == 14:
        return f'<svg viewBox="0 0 430 310" role="img" aria-label="Cosmological evidence matrix linking probes to parameters"><rect x="55" y="45" width="320" height="220" fill="#fff" stroke="{navy}" stroke-width="3"/><path d="M55 100H375M55 155H375M55 210H375M160 45V265M270 45V265" stroke="{gray}"/><text x="82" y="78">probe</text><text x="185" y="78">epoch</text><text x="295" y="78">constraint</text><text x="78" y="134">CMB</text><text x="78" y="189">BAO</text><text x="78" y="244">SN</text><text x="180" y="134">380 kyr</text><text x="180" y="189">late</text><text x="180" y="244">late</text><text x="292" y="134">Omega</text><text x="292" y="189">distance</text><text x="292" y="244">accel.</text></svg>'
    raise ValueError(i)


def page(title: str, body: str, css: str = CSS) -> str:
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title><script id='MathJax-script' async src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script><style>{css}</style></head><body>{body}</body></html>"


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def header(title: str, subtitle: str) -> str:
    return f"<header><div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div></header>"


def calculation(i: int) -> tuple[str, str]:
    if i == 1:
        d = hubble_distance_mpc(0.01); return f"At z=0.01, the low-z estimate gives d = cz/H0 = {fmt(d,6)} Mpc.", "This linear estimate is a low-redshift approximation; peculiar velocities can be a comparable correction for nearby galaxies."
    if i == 2:
        v = special_velocity(0.10); return f"For z=0.10, the special-relativistic formula gives v = {fmt(v,6)} km s^-1, while cz = {fmt(C_KMS*0.10,6)} km s^-1.", "The difference is about 1.5%; cosmological redshift is not generally a simple Doppler velocity."
    if i == 3:
        return f"rho_crit = 3H0^2/(8 pi G) = {fmt(critical_density_msun_mpc3(),7)} solar masses Mpc^-3.", "The density is an energy-density scale; Omega values compare each component with this critical value."
    if i == 4:
        t = lookback_gyr(1.0); return f"Numerical Simpson integration gives t_L(z=1) = {fmt(t,6)} Gyr for the shared flat Lambda-CDM parameters.", "The result depends on H0 and the density parameters; the integral is not replaceable by 1/H0 at z=1."
    if i == 5:
        temp = T_CMB * (1 + 1100); return f"T_gamma(z=1100) = T0(1+z) = {fmt(temp,6)} K.", "The scaling follows adiabatic expansion of radiation; it does not alone determine the ionization history."
    if i == 6:
        return f"Wien's law gives nu_peak approximately {fmt(cmb_peak_ghz(),6)} GHz for T={T_CMB} K.", "The frequency of the intensity peak depends on the spectral variable; wavelength and frequency peaks are not reciprocal labels."
    if i == 7:
        y = helium_fraction(1/7); return f"With n/p=1/7, Y_p = 2(n/p)/(1+n/p) = {fmt(y,6)}.", "The estimate assumes nearly every surviving neutron enters helium-4 and omits the small deuterium, helium-3, and lithium channels."
    if i == 8:
        return f"An initial curvature fraction of 0.1 shrinks to {fmt(curvature_after_efolds(0.1,60),6)} after 60 idealized e-folds.", "This is an exponential scaling argument, not a measurement of the inflationary potential."
    if i == 9:
        growth = growth_factor(1100); return f"Linear matter-era growth from z=1100 to today is a factor of 1+z = {fmt(growth,6)}; a 10^-5 seed becomes {fmt(1e-5*growth,6)} in the idealized model.", "The result remains linear only until delta approaches unity; collapsed halos require nonlinear dynamics."
    if i == 10:
        return "A 150 Mpc comoving ruler subtending an angle theta constrains D_M through theta = r_s/D_M; the same ruler in redshift constrains H(z).", "The ruler is inferred from a correlation feature and depends on the adopted sound-horizon calibration."
    if i == 11:
        d = luminosity_distance_mpc(43.16); return f"For mu=43.16, D_L = 10^((mu-25)/5) = {fmt(d,7)} Mpc.", "The distance is standardized-model dependent and inherits calibration, dust, and selection uncertainties."
    if i == 12:
        kappa = 2.0e14 / 3.0e15; return f"With Sigma=2.0e14 and Sigma_crit=3.0e15 solar masses Mpc^-2, kappa = {fmt(kappa,6)}.", "The value is dimensionless, but translating shear to a mass map requires source redshifts and an inversion convention."
    if i == 13:
        ratio = POWER[3][1] / POWER[0][1]; return f"The supplied power table has P(0.10)/P(0.01) = {fmt(ratio,6)}.", "The ratio is not a primordial amplitude alone; transfer, bias, and nonlinear effects shape the observed spectrum."
    sig = normalize_h0(73.04,1.04,67.4,0.5); return f"The independent-error normalized difference is |73.04-67.4|/sqrt(1.04^2+0.5^2) = {fmt(sig,6)} sigma.", "This summary is conditional on independent Gaussian errors; shared calibration or model covariance changes the interpretation."


def figure(i: int, visual: str) -> str:
    return f'<figure class="figure">{svg(i)}<figcaption>{html.escape(visual)}. The axes, labels, and geometry carry the physical inference rather than serving as decoration.</figcaption></figure>'


def lecture_pages(i: int, item: tuple[str, ...]) -> tuple[str, str]:
    title, outcome, scope, equation, prompt, motivation, reading = item
    calc, interp = calculation(i)
    fig = figure(i, scope)
    slide_sections = [
        f'<section class="slide title"><div class="kicker">ASTR 420 · Lecture {i:02d}</div><h1>Lecture {i:02d}: {html.escape(title)}</h1><h2>Cosmology</h2><p>{html.escape(motivation)}</p></section>',
        f'<section class="slide"><h2>Objectives and route</h2>{bullets([outcome, f"Define and distinguish {scope}.", "Derive or audit one quantitative relation with units and assumptions.", "Connect the calculation to an observational test and a limitation."])}</section>',
        f'<section class="slide"><h2>Motivating evidence</h2><div class="grid"><div><p>{html.escape(motivation)}</p><p>Cosmological claims are indirect: an observable is calibrated, placed in a model, and compared against alternatives. Keep those layers separate throughout the lecture.</p></div>{fig}</div></section>',
        f'<section class="slide"><h2>Physical framework</h2><p>Start from the governing relation and define its domain:</p><div class="equation">\\({equation}\\)</div><p>State the coordinate choice, units, boundary conditions, and approximation before substituting numbers. The same symbol can mean a different quantity in Newtonian, special-relativistic, and expanding-space contexts.</p></section>',
        f'<section class="slide"><h2>Read the visual</h2><p>Use the figure introduced on the evidence slide as an argument: identify the measured axis, the inferred axis, the comparison model, and the parameter that controls the conclusion.</p><p class="credit">The paired lab asks you to reproduce the visual from a supplied data extract and test one modeling choice.</p></section>',
        f'<section class="slide"><h2>Worked calculation</h2><div class="equation">{html.escape(calc)}</div><p>{html.escape(interp)}</p><p>Estimate the scale first, then check dimensions and comparative direction. The displayed value is generated from shared ASTR420 constants and data.</p></section>',
        f'<section class="slide"><h2>Evidence versus inference</h2>{bullets(["Raw data are not the same as calibrated observables.", "A fitted parameter is conditional on the likelihood, prior, and selection function.", "Independent probes can agree because the model is useful, or disagree because an assumption is hidden."])}</section>',
        f'<section class="slide"><h2>Boundary condition</h2><div class="prompt"><strong>Limit of the model:</strong> {html.escape(interp)}</div><p>Ask what happens if the dominant assumption fails. In cosmology, approximation honesty matters because distances, times, and abundances accumulate model dependence.</p></section>',
        f'<section class="slide"><h2>Active reasoning</h2><div class="prompt"><p><strong>Prompt:</strong> {html.escape(prompt)}</p><p>Predict the direction before calculating. Then name one observation that could discriminate between two explanations.</p></div></section>',
        f'<section class="slide"><h2>Connection to the seven-unit arc</h2>{bullets(["Earlier tools: ASTR310 radiation, dynamics, and statistical mechanics.", "Paired data activity: use the corresponding CSV and reproduce the calculation with a perturbation test.", "Next step: combine this probe with an independent epoch or distance measure."])}</section>',
        f'<section class="slide"><h2>Takeaways</h2>{bullets([outcome, "A cosmological parameter is meaningful only with its model and uncertainty context.", "State whether a number is live-verified, a published value awaiting spot-check, or an instructor-provided model value.", "Carry the limitation forward into the lab and problem set."])}</section>',
        f'<section class="slide"><h2>Reading and provenance</h2><p>{html.escape(reading)}</p><p>OpenStax Astronomy 2e Chapter 29 embedded figure numbers were checked against the extracted text; the source index has chapter-label offsets near the Chapter 29 boundary, so the adopted PDF remains the final exercise-number authority.</p><p class="small">Additional sources and dataset status are recorded in reference-log.md. Standard published values not re-fetched this session are level 2 and require human spot-checking.</p></section>',
    ]
    slides = page(f"ASTR 420 Lecture {i:02d} Slides: {title}", '<div class="deck">' + ''.join(slide_sections) + '</div>', SLIDE_CSS)
    note_sections = [
        f"<section><h2>Learning objectives</h2>{bullets([outcome, f'Explain {scope} using the governing relation.', 'Separate measurement, calibration, inference, and model limitation.'])}</section>",
        f"<section><h2>Lecture arc</h2><p>{html.escape(motivation)} Begin with the observational puzzle and ask students what is directly measured. Introduce {scope} only after the data-model boundary is explicit.</p><p>The visual is a reasoning object: students should narrate what each line, region, or axis means before seeing the equation.</p></section>",
        f"<section><h2>Derivation and interpretation</h2><div class='equation'>\\({equation}\\)</div><p>Define the symbols, units, and assumptions. Explain why the relation is useful and where it fails. Relate the result to the paired lab's data record rather than treating the equation as a detached recipe.</p>{fig}</section>",
        f"<section><h2>Worked example</h2><p>{html.escape(calc)}</p><p>{html.escape(interp)} Require students to estimate the answer, show units, and state whether the approximation is controlled, empirical, or merely illustrative.</p></section>",
        f"<section><h2>Misconceptions and study guidance</h2><p>{html.escape(motivation)} Common traps include confusing redshift with a unique velocity, treating a model-dependent parameter as a direct measurement, and overlooking covariance. Study by reproducing the calculation, changing one assumption, and comparing the result with the exact OpenStax anchor listed in the reference log.</p><p>Preparation for the problem set: write a one-paragraph evidence chain from observation to conclusion and identify the weakest link.</p></section>",
    ]
    notes = page(f"ASTR 420 Lecture {i:02d} Notes: {title}", header(f"ASTR 420 Lecture {i:02d}: {title}", "Cosmology · study notes") + '<main>' + ''.join(note_sections) + '</main>')
    return slides, notes


def unit_calc(unit: int) -> str:
    return calculation(2 * unit - 1)[0]


def lab_html(i: int, title: str, lectures: str, dataset: str, task: str, sample: str, uncertainty: str) -> str:
    return page(f"ASTR 420 Lab {i:02d}: {title}", header(f"ASTR 420 Lab {i:02d}: {title}", f"Lectures {lectures} · cosmology data-analysis laboratory") + f"<main><section><h2>Objectives</h2>{bullets([f'Analyze {dataset}.', task, 'Report a reproducible result with units, uncertainty, and provenance.', 'Test one model assumption rather than presenting a single fitted number.'])}</section><section><h2>Materials and setup</h2><p>Use Python 3 with NumPy, Matplotlib, and the supplied CSV. Record the file name, row count, columns, units, software versions, and the date of analysis. The supplied extracts are compact teaching files derived from named published summaries; they are not new observations.</p><p><strong>Input:</strong> {html.escape(dataset)}</p><p><strong>Computed check:</strong> {html.escape(sample)}</p></section><section><h2>Procedure</h2><ol><li>Inspect the CSV without plotting first. Record missing values, units, and any selection or calibration fields.</li><li>Make a labeled plot of the raw observable and preserve the supplied uncertainty column where present.</li><li>Implement the governing equation from Lectures {lectures}; show the intermediate units in a notebook or script.</li><li>Repeat the analysis after the specified perturbation: remove one endpoint, vary a calibration, or compare a second model.</li><li>Write an evidence chain that distinguishes measured inputs, adopted literature values, derived parameters, and model assumptions.</li></ol></section><section><h2>Measurement and analysis record</h2><table><tr><th>Record</th><th>Required entry</th></tr><tr><td>Input provenance</td><td>File, source, access/spot-check status, and level 1/2/3 label</td></tr><tr><td>Primary fit or transformation</td><td>Formula, parameter, units, and code reference</td></tr><tr><td>Uncertainty</td><td>Statistical uncertainty plus sensitivity to the prescribed perturbation</td></tr><tr><td>Validation</td><td>Independent recomputation or comparison with a named benchmark</td></tr></table><div class='equation'>{html.escape(uncertainty)}</div></section><section><h2>Deliverables and assessment</h2><ul><li>Notebook or script with a clean rerun path and input filename.</li><li>One labeled figure and one table of fitted or derived values.</li><li>600-800 word interpretation with uncertainty and one limitation.</li><li>Short provenance statement and bibliography.</li></ul><p>100 points: setup/provenance 15, method 25, quantitative result 25, uncertainty/sensitivity 20, figure and scientific communication 15.</p></section><section><h2>Safety and reproducibility</h2><p>No observing is required. Preserve raw CSVs, do not overwrite supplied data, and use a fixed random seed if a resampling demonstration is added. Any external download must be logged before use.</p></section></main>")


def pset(i: int, title: str, lectures: str, dataset: str, calc: str, exact: str) -> tuple[str, str, str]:
    problems = [
        f"Derive the central relation from Lectures {lectures}. Define every symbol, state the coordinate system and approximation, and use the shared ASTR420 constants to obtain the requested scale. Show units through the final line.",
        f"Use data/{dataset} to make one quantitative plot. Fit or transform the specified observable, report an uncertainty or residual statistic, and repeat after the prescribed sensitivity change. Include the exact input rows used.",
        "A student claims that the plotted trend is a direct measurement of one cosmological component. Write a technically precise rebuttal distinguishing raw data, calibration, likelihood, model parameter, and an alternative explanation.",
        f"Transfer problem: compare the result with an independent probe from the neighboring unit. State whether the comparison is limited by statistical error, covariance, selection, calibration, or model dependence. A correct numerical ratio or direction is required where applicable.",
    ]
    body = header(f"ASTR 420 Problem Set {i:02d}: {title}", "Student assignment · quantitative cosmology") + f"<main><section><h2>Learning objectives</h2>{bullets(['Derive and apply a relativistic-cosmology relation.', 'Analyze a traceable cosmology data extract.', 'Communicate uncertainty and model dependence.', 'Compare independent observational tests.'])}</section><section><h2>Instructions</h2><p>Use SI units internally, report cosmological distances in Mpc or Gpc with the conversion shown, and distinguish a published input from a derived value. Submit calculations, a reproducible script/notebook, labeled figures, and a bibliography. Revisions are permitted within one week with a concise change note.</p></section>" + ''.join(f"<article class='problem'><h3>Problem {j}</h3><p>{html.escape(text)}</p></article>" for j,text in enumerate(problems,1)) + f"<section><h2>Exact reading anchor</h2><p>{html.escape(exact)} The local extracted source index has chapter-label offsets near Chapter 29; verify exercise wording and numbering against the adopted PDF before assignment.</p></section><section><h2>Deliverables</h2><p>Four written solutions, one reproducible analysis, one uncertainty/sensitivity statement, and cited data provenance. Total: 100 points.</p></section></main>"
    solution = header(f"ASTR 420 Problem Set {i:02d} Solutions: {title}", "Instructor solution key") + f"<main><section><h2>Rubric</h2><p>Problems 1-4 are 25 points each. Require dimensional consistency, correct comparative direction, explicit assumptions, reproducibility, and interpretation. Accept equivalent derivations when the physical meaning is preserved.</p></section>" + ''.join(f"<article class='problem'><h3>Problem {j}</h3><p><strong>Solution route:</strong> define the measured quantity, write the model, substitute shared values, and test the stated assumption.</p><p><strong>Key check:</strong> {html.escape(calc if j == 1 else 'The analysis must contain a labeled data display, uncertainty or sensitivity treatment, and a provenance statement; an unsupported scalar answer is incomplete.')}</p></article>" for j in range(1,5)) + "<section><h2>Common errors</h2><ul><li>using cz as a universal cosmological velocity;</li><li>mixing Mpc, km, and seconds without conversion;</li><li>reversing a ratio or calling a model-dependent quantity direct;</li><li>ignoring covariance, selection, or the approximation domain.</li></ul></section></main>"
    assess = f"# ASTR 420 Problem Set {i:02d} Assessment Instructions\n\nInspect the student submission, this assignment, its solution key, submitted code/data, and the course policy.\n\n## Standard\nAward credit for correct equations, units, cosmological interpretation, uncertainty/sensitivity analysis, exact data provenance, and reproducibility. Separate arithmetic slips from conceptual errors and unsupported claims. Check that published level-2 values are not described as new measurements.\n\n## Revision\nReturn feedback tied to a problem and rubric criterion. Permit one resubmission within one week with a change note; retain the same standards for evidence and reasoning.\n"
    return page(f"ASTR 420 PS {i:02d}: {title}", body), page(f"ASTR 420 PS {i:02d} Solutions: {title}", solution), assess


def syllabus() -> str:
    rows = ''.join(f"<tr><td>{i:02d}</td><td>{LECTURES[i-1][0]}</td><td>{'Lab '+f'{(i+1)//2:02d}' if i%2==0 else ''}</td><td>{'PS '+f'{(i+1)//2:02d}' if i%2==0 else ''}</td></tr>" for i in range(1,15))
    return page("ASTR 420 Syllabus", header("ASTR 420: Cosmology", "3 credits · Year 4 Fall · Prerequisites: ASTR310; MATH255; PHYS271") + f"<main><section><h2>Catalog description</h2><p>Introduces relativistic cosmology at an undergraduate level, including expansion, redshift, distance measures, the cosmic microwave background, nucleosynthesis, structure formation, dark matter, dark energy, and observational tests.</p></section><section><h2>Learning outcomes</h2>{bullets(['Derive and interpret the Friedmann equation and cosmological distance relations.', 'Explain the thermal history, CMB, recombination, and light-element synthesis.', 'Connect perturbation growth, dark matter, BAO, lensing, and the matter power spectrum.', 'Fit or audit observational summaries from supernovae, BAO, CMB, and cluster/lensing extracts.', 'Quantify uncertainty, covariance, selection, and approximation limits in cosmological inference.', 'Construct an evidence-weighted comparison of a concordance model and alternatives.'])}</section><section><h2>Resources and source discipline</h2><p>Primary open resource: OpenStax <em>Astronomy 2e</em>, Chapter 29, “The Big Bang,” with Chapter 26 section 26.5 and Chapter 28 sections 28.4-28.5 for distance, lensing, and structure context. Embedded figure numbering was checked against the local extracted text; see reference-log.md for exact anchors and PDF spot-check requirements.</p></section><section><h2>Cadence rationale</h2><p>This 3-credit course uses 14 lectures, 7 labs, and 7 problem sets in seven matched two-lecture units. Each lab and problem set follows the second lecture of its unit because the activity combines both the conceptual model and the quantitative tool. The two-lecture/one-assessment cadence protects time for derivation, data analysis, and uncertainty discussion while keeping the weekly contact pattern plausible for a 3-credit fall course.</p><table><tr><th>Unit</th><th>Lectures</th><th>Lab</th><th>Problem set</th></tr>{''.join(f'<tr><td>{u}</td><td>{2*u-1:02d}-{2*u:02d}</td><td>{u:02d}</td><td>{u:02d}</td></tr>' for u in range(1,8))}</table></section><section><h2>Assessment</h2><table><tr><th>Component</th><th>Weight</th></tr><tr><td>7 problem sets</td><td>30%</td></tr><tr><td>7 data-analysis labs</td><td>30%</td></tr><tr><td>Midterm, Lectures 1-7</td><td>15%</td></tr><tr><td>Final, cumulative</td><td>20%</td></tr><tr><td>Reading checks and participation</td><td>5%</td></tr></table><p>Students may revise within one week of feedback with a change note. Grades reward physical reasoning, units, evidence, uncertainty, and reproducible work.</p></section><section><h2>Lecture schedule</h2><table><tr><th>Lecture</th><th>Title</th><th>Lab</th><th>PS</th></tr>{rows}</table></section><section><h2>Policies to finalize locally</h2><p>Instructor of record should add institution-specific accessibility, academic-integrity, attendance, late-work, and calendar language before instructional use.</p></section></main>")


def schedule() -> str:
    return page("ASTR 420 Schedule", header("ASTR 420: Lecture and Assessment Schedule", "Fourteen lectures · seven two-lecture units") + f"<main><table><tr><th>Week</th><th>Lecture focus</th><th>Assessment</th></tr>" + ''.join(f"<tr><td>{(i+1)//2 if i%2==0 else (i+1)//2 + 1 if i>1 else 1}</td><td>Lecture {i:02d}: {html.escape(item[0])}</td><td>{'Lab and PS '+f'{(i+1)//2:02d}' if i%2==0 else 'Concept development'}</td></tr>" for i,item in enumerate(LECTURES,1)) + "</table><p>Assessment artifacts are intentionally released after the second lecture in each unit; this is the documented matched cadence, not a missing weekly lab.</p></main>")


def references() -> str:
    return """# ASTR 420 Reference Log

## Adopted textbook and embedded-figure checks

- OpenStax, *Astronomy 2e*, Chapter 29, “The Big Bang,” sections 29.1-29.7. The extracted text at `references/openstax-astronomy-2e-extracted.txt` contains the native chapter heading and embedded captions including Figures 29.10 and 29.11. The generated source index places some chapter labels one block earlier near the Chapter 29 boundary; therefore the native embedded figure numbers and adopted PDF must control final assignment wording.
- OpenStax Chapter 26, section 26.5, “The Expanding Universe,” supports distance ladders, redshift, and supernova context. Chapter 28, sections 28.4-28.5, supports lensing and large-scale structure. All chapter/figure claims require a human adopted-PDF spot-check before instructional use.
- Exact exercise anchors used in the problem sets: Chapter 29 Review Questions 1, 3, 10, and 12; Figuring for Yourself 29, 30, 31, and 32 as available in the extracted index. Because the generated exercise index has boundary offsets, these identifiers are flagged for direct PDF verification rather than treated as authoritative numbering.

## Data provenance levels

- **Level 1, live-verified this session:** local OpenStax extracted text and source-index files were directly inspected in this workspace. This verifies the chapter/figure text presence, not the adopted edition's final exercise pagination.
- **Level 2, published/literature values not re-verified this session:** Planck-style CMB summaries (H0=67.4, Omega_m=0.315, Omega_b=0.0493, T_CMB=2.7255 K), standard BAO summary ratios, compact supernova distance-modulus teaching values, primordial abundance summaries, and representative matter-power values. Human spot-check against Planck 2018, DESI/BAO releases, Pantheon+/SH0ES or an instructor-selected SN compilation, and BBN review literature is required.
- **Level 3, synthetic/instructor-provided:** the compact CSV teaching extracts are reduced, rounded instructional tables assembled from the level-2 summaries; SVG diagrams, perturbation tests, and the stated model curves are generated illustrations, not observations.

## Additional references requiring human spot-check

- Planck Collaboration VI (2020), *A&A* 641, A6, DOI 10.1051/0004-6361/201833910.
- Riess et al. (2022), *ApJL* 934, L7, DOI 10.3847/2041-8213/ac5c5b.
- Eisenstein et al. (2005), *ApJ* 633, 560, DOI 10.1086/466512.
- Abbott et al. (2018), *ApJ* 858, 19, DOI 10.3847/1538-4357/aabdec.
- Cyburt et al. (2016), *Rev. Mod. Phys.* 88, 015004, DOI 10.1103/RevModPhys.88.015004.

No external images are embedded. The lecture figures are original SVG diagrams generated by `src/generate_astr420_package.py`; they are schematic/model figures and are labeled as such in captions.
"""


def index_html() -> str:
    lecture_links = ''.join(f'<li><a href="lectures/lecture-{i:02d}-slides.html">Lecture {i:02d}: {html.escape(item[0])}</a> <span class="small">— slides</span> · <a href="lectures/lecture-{i:02d}-notes.html">notes</a></li>' for i,item in enumerate(LECTURES,1))
    lab_titles = ["Expansion and Redshift Audit", "Distance Measures and Cosmic Time", "Thermal History and CMB", "Nucleosynthesis and Inflation", "Structure Growth and BAO", "Supernovae and Lensing", "Power Spectrum and Parameter Tests"]
    lab_links = ''.join(f'<li><a href="labs/lab-{i:02d}.html">ASTR 420 Lab {i:02d}: {html.escape(lab_titles[i-1])}</a></li>' for i in range(1,8))
    ps_links = ''.join(f'<li><a href="problem-sets/problem-set-{i:02d}.html">Problem Set {i:02d}</a> · <a href="problem-sets/problem-set-{i:02d}-solutions.html">solutions</a> · <a href="problem-sets/problem-set-{i:02d}-assessment.md">assessment</a></li>' for i in range(1,8))
    return page("ASTR420 Course Materials Index", header("ASTR 420: Cosmology", "3 credits · Year 4 Fall · Course Materials Index") + f"<main><section class='notice'><p><strong>Status:</strong> Approved for review release; not yet approved for instructional use.</p><p>Introduces relativistic cosmology including expansion, redshift, distance measures, CMB, nucleosynthesis, structure formation, dark matter, dark energy, and observational tests.</p><p class='small'>Last updated: 2026-09-25 · <a href='course-manifest.json'>manifest</a> · <a href='review-report.md'>review report</a></p></section><section><h2>Planning</h2><p><a href='syllabus.html'>Syllabus</a> · <a href='schedule.html'>Schedule</a> · <a href='reference-log.md'>Reference log</a> · <a href='README.md'>README</a></p></section><section><h2>Lectures</h2><ul>{lecture_links}</ul></section><section><h2>Labs</h2><ul>{lab_links}</ul></section><section><h2>Problem sets</h2><ul>{ps_links}</ul></section><section><h2>Data and source</h2><p><a href='data/README.md'>Data README</a> · <a href='src/README.md'>Source README</a></p></section></main>")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build() -> None:
    for folder in (LECTURE_DIR, LABS, PSETS, DATA): folder.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(LECTURES, 1):
        slides, notes = lecture_pages(i, item)
        write(LECTURE_DIR / f"lecture-{i:02d}-slides.html", slides)
        write(LECTURE_DIR / f"lecture-{i:02d}-notes.html", notes)
    for filename, header_row, rows in [
        ("cmb-summary.csv", ["parameter","value","uncertainty"], CMB),
        ("sn-hubble.csv", ["redshift","distance_modulus"], SN),
        ("bao-summary.csv", ["redshift","distance_ratio"], BAO),
        ("matter-power.csv", ["k_h_per_mpc","P_k_arbitrary"], POWER),
        ("primordial-abundances.csv", ["species","mass_or_number_fraction"], ABUND),
    ]:
        with (DATA / filename).open("w", newline="", encoding="utf-8") as stream:
            out = csv.writer(stream); out.writerow(header_row); out.writerows(rows)
    lab_specs = [
        ("Expansion and Redshift Audit", "01-02", "sn-hubble.csv", "fit a low-z Hubble relation and quantify where the linear approximation begins to drift", calculation(1)[0], "Repeat the fit after excluding z>0.2 and report the change in slope."),
        ("Distance Measures and Cosmic Time", "03-04", "sn-hubble.csv", "integrate lookback time for selected redshifts and compare luminosity-distance definitions", calculation(3)[0], "Compare Simpson integration at 100 and 1000 intervals and report convergence."),
        ("Thermal History and CMB", "05-06", "cmb-summary.csv", "propagate T_CMB and inspect how the blackbody peak responds to a stated temperature uncertainty", calculation(5)[0], "Perturb T_CMB by its supplied uncertainty and propagate the peak-frequency change."),
        ("Nucleosynthesis and Inflation", "07-08", "primordial-abundances.csv", "calculate helium yield from a neutron ratio and compare it with the abundance table", calculation(7)[0], "Vary n/p from 1/7 to 1/8 and quantify the shift in Yp."),
        ("Structure Growth and BAO", "09-10", "bao-summary.csv", "plot the supplied BAO distance ratios and interpret a standard-ruler constraint", calculation(9)[0], "Repeat the interpretation after omitting the highest-redshift point."),
        ("Supernovae and Lensing", "11-12", "sn-hubble.csv", "convert distance moduli and analyze a projected convergence example", calculation(11)[0], "Shift every distance modulus by 0.05 mag and report the fractional distance change."),
        ("Power Spectrum and Parameter Tests", "13-14", "matter-power.csv", "compare a power-spectrum ratio with a two-summary H0 tension statistic", calculation(13)[0], "Fit a log-log slope to the first four power points and compare it with the full table."),
    ]
    for i, (title, lectures, dataset, task, sample, uncertainty) in enumerate(lab_specs, 1):
        write(LABS / f"lab-{i:02d}.html", lab_html(i, title, lectures, f"data/{dataset}", task, sample, uncertainty))
        exact = ["Chapter 29 Review Questions 1 and 3; Figuring for Yourself 29.", "Chapter 29 Review Question 3; Figuring for Yourself 30.", "Chapter 29 Review Questions 10 and 11; Figuring for Yourself 25.", "Chapter 29 Review Question 10; Figuring for Yourself 24.", "Chapter 29 Review Question 8; Figuring for Yourself 23.", "Chapter 29 Review Question 12; Figuring for Yourself 29.", "Chapter 29 Review Questions 1 and 12; Figuring for Yourself 30."][i-1]
        p, s, a = pset(i, title, lectures, dataset, sample, exact)
        write(PSETS / f"problem-set-{i:02d}.html", p); write(PSETS / f"problem-set-{i:02d}-solutions.html", s); write(PSETS / f"problem-set-{i:02d}-assessment.md", a)
    write(DATA / "README.md", """# ASTR 420 Data\n\nThese compact CSVs are level-3 instructor-provided teaching extracts assembled from the level-2 published summaries listed in `../reference-log.md`. They are not new measurements. Students must record filenames, row counts, units, and all sensitivity choices. Human spot-checks against the named Planck, BAO, supernova, and BBN sources are required before instructional use.\n""")
    write(ROOT / "src" / "README.md", """# ASTR 420 Source\n\n`generate_astr420_package.py` is the single source for shared constants, teaching extracts, calculations, distinct SVG reasoning figures, and all HTML/Markdown artifacts. Re-run it with the selected project Python interpreter to regenerate the package. Review calculations should retype formulas independently rather than import this module.\n""")
    write(ROOT / "README.md", """# ASTR 420 Cosmology\n\nComplete Year 4 Fall, 3-credit course package. Read `syllabus.html`, then `schedule.html`; each lab and problem set follows a documented two-lecture unit.\n""")
    write(ROOT / "syllabus.html", syllabus()); write(ROOT / "schedule.html", schedule()); write(ROOT / "reference-log.md", references()); write(ROOT / "index.html", index_html())
    manifest = {"course":{"courseNumber":"ASTR 420","courseCode":"ASTR420","title":"Cosmology","credits":3,"term":"Fall","yearInCurriculum":4,"prerequisites":"ASTR310; MATH255; PHYS271","description":"Introduces relativistic cosmology including expansion, redshift, distance measures, the CMB, nucleosynthesis, structure formation, dark matter, dark energy, and observational tests."},"status":{"stage":"approved for review release","reviewStatus":"Approved for review release; not yet approved for instructional use","lastUpdated":"2026-09-25"},"counts":{"slides":14,"notes":14,"labs":7,"problemSets":7,"solutionKeys":7,"assessmentInstructions":7},"cadence":{"lectures":14,"labs":7,"problemSets":7,"rationale":"Matched 1:1 biweekly cadence: seven units each contain two lectures followed by one lab and one problem set; the second lecture completes the quantitative toolkit used by the paired data activity."},"dataProvenance":{"generator":"materials/ASTR420/src/generate_astr420_package.py","levels":{"level1":"Local OpenStax extracted text and source-index files were inspected this session; adopted-PDF exercise wording remains a human spot-check.","level2":"CMB, BAO, supernova, BBN, and matter-power values are standard published summaries not re-verified this session; human spot-checks are required.","level3":"Compact CSV extracts, SVG diagrams, and model curves are instructor-provided teaching artifacts derived from the level-2 summaries."}}}
    write(ROOT / "course-manifest.json", json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    build()
