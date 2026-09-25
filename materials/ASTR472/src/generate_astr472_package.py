"""Generate the ASTR 472 Radio Astronomy teaching package.

All displayed worked-example results are calculated from the shared inputs
below. Re-run this file after changing constants or teaching records.
"""
from __future__ import annotations

import csv
import html
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURE_DIR = ROOT / "lectures"
LAB_DIR = ROOT / "labs"
PSET_DIR = ROOT / "problem-sets"
DATA_DIR = ROOT / "data"

C = 299_792_458.0
K_B = 1.380649e-23
H = 6.62607015e-34
JY = 1e-26
ARCSEC_PER_RAD = 206264.806247
F_HI = 1_420.40575177e6
YEAR_S = 365.25 * 86400
KPC_M = 3.085677581e19

CSS = """:root{--ink:#17202a;--muted:#596875;--paper:#f8fafb;--panel:#fff;--line:#d5dee5;--navy:#17324d;--teal:#087e8b;--cyan:#dff4f5;--gold:#b66a0a;--red:#a33a3a}*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--paper);font-family:Georgia,'Times New Roman',serif;line-height:1.58}header{padding:38px 24px 28px;background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}header>div,main{max-width:1120px;margin:auto}main{padding:28px 24px 64px}h1,h2,h3{line-height:1.15}h1{margin:0 0 8px;font-size:2.5rem}h2{color:var(--navy);border-bottom:2px solid var(--line);padding-bottom:8px;margin-top:32px}h3{color:var(--teal)}section,article.problem{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:16px 18px;margin:16px 0}.notice{border-left:5px solid var(--teal);background:var(--cyan)}table{width:100%;border-collapse:collapse;margin:14px 0}th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}th{background:var(--cyan)}a{color:var(--teal);font-weight:700}.small{color:var(--muted);font-size:.92rem}.equation{padding:12px 16px;border-left:5px solid var(--teal);background:var(--cyan);overflow:auto}.figure{margin:16px 0}.figure svg{width:100%;height:auto;max-height:460px;background:#fff;border:1px solid var(--line)}.figure figcaption{color:var(--muted);font-size:.94rem}.prompt{padding:14px 18px;border-left:5px solid var(--gold);background:#fff6e6}.deck{height:100vh;overflow-y:auto;scroll-snap-type:y mandatory}.slide{min-height:100vh;scroll-snap-align:start;display:flex;flex-direction:column;justify-content:center;padding:42px 7vw;border-bottom:1px solid var(--line);background:#fff}.slide.title{background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff}.slide.title h2{color:#fff}.slide h2{font-family:'Aptos','Segoe UI',sans-serif;font-size:2rem;margin:0 0 18px}.slide p,.slide li{font-size:1.16rem;line-height:1.42}.kicker{color:var(--gold);text-transform:uppercase;font-weight:700}@media(max-width:700px){main{padding:20px 14px 48px}.slide{padding:32px 22px}.slide p,.slide li{font-size:1rem}table{font-size:.9rem}}@media print{.deck{height:auto;overflow:visible}.slide{min-height:7.5in;page-break-after:always}}"""

LECTURES = [
    {
        "title": "The Radio Sky: Emission Mechanisms and Observables",
        "hook": "Radio maps show jets, cold gas, and coherent pulses that can be faint or invisible in optical images.",
        "objectives": ["Distinguish thermal free-free, synchrotron, coherent, and line emission by spectral and polarization signatures.", "Relate synchrotron characteristic frequency to electron energy and magnetic field.", "Separate measured flux density from source brightness and physical interpretation."],
        "evidence": ["A power-law continuum is consistent with optically thin synchrotron emission, but spectral curvature can signal cooling or absorption.", "Thermal bremsstrahlung can be optically thin or turn over at low frequency; a flat spectrum alone does not uniquely identify a mechanism.", "Radio data preserve frequency, polarization, and time structure that an integrated broadband flux would discard."],
        "derivation": "For a relativistic electron with Lorentz factor gamma in magnetic field B, the characteristic synchrotron frequency scales as nu_c = (3/2) gamma^2 (e B sin(alpha))/(2 pi m_e). Averaging pitch angle gives the teaching approximation nu_c approximately 4.2e6 B_G gamma^2 Hz. It is a characteristic frequency, not a monochromatic emission line.",
        "equation": r"\nu_c\simeq 4.2\times10^6 B_{\rm G}\gamma^2\ {\rm Hz}",
        "example": 1,
        "limit": "The single-electron characteristic frequency ignores the broad synchrotron kernel, pitch-angle distribution, and self-absorption; a measured spectral peak is not automatically nu_c.",
        "prompt": "If the magnetic field is four times stronger but the observed characteristic frequency is unchanged, how must gamma change? State the scaling and one assumption.",
        "reading": "OpenStax Astronomy 2e §5.2 (electromagnetic spectrum), §20.2 (interstellar gas), and §27.1 (radio galaxies); these give introductory context rather than a synchrotron derivation.",
        "figure": 1,
    },
    {
        "title": "Antennas, Feed Systems, and Receiver Chains",
        "hook": "A radio dish is not a bigger optical mirror: feed illumination, spillover, sidelobes, and receiver temperature shape the measurement.",
        "objectives": ["Derive the dish beamwidth scale and effective collecting area.", "Trace a signal through antenna, feed, low-noise amplifier, mixer, and digitizer.", "Explain antenna temperature and the distinction between beam response and source structure."],
        "evidence": ["For a filled circular aperture, beamwidth scales as wavelength divided by diameter; longer wavelengths broaden a single-dish beam.", "Aperture efficiency folds illumination and surface losses into A_eff=eta_a pi D^2/4.", "The receiver adds noise before digitization, so the backend cannot recover information lost to a poor system temperature."],
        "derivation": "Fraunhofer diffraction makes the angular response depend on the dimensionless aperture coordinate D theta/lambda. A uniformly illuminated circular aperture has first null 1.22 lambda/D; practical radio half-power beamwidths are often near 1.02 lambda/D, with illumination-dependent coefficients. Antenna temperature is the beam-weighted sky brightness in the Rayleigh-Jeans limit.",
        "equation": r"\theta_{\rm FWHM}\simeq1.02\frac{\lambda}{D},\qquad A_{\rm eff}=\eta_a\frac{\pi D^2}{4}",
        "example": 2,
        "limit": "The 1.02 coefficient is an approximate FWHM for a tapered aperture, not the Airy first-null coefficient; quote which beam definition is used.",
        "prompt": "At fixed frequency, double dish diameter. What happens to FWHM and collecting area if aperture efficiency remains fixed? Explain the different powers.",
        "reading": "OpenStax Astronomy 2e §6.4; its radio-dish and receiver description is introductory. NRAO Green Bank Telescope and VLA facility documentation give current instrument context.",
        "figure": 2,
    },
    {
        "title": "Sensitivity and the Radiometer Equation",
        "hook": "Longer integrations help only as the square root of time when receiver and sky noise are stationary and samples are independent.",
        "objectives": ["Derive radiometer sensitivity from independent noise samples.", "Convert between system-equivalent flux density and rms flux uncertainty.", "Design a line observation by balancing channel width and integration time."],
        "evidence": ["Thermal noise is reduced by averaging independent time-frequency-polarization samples.", "Narrow spectral channels improve velocity resolution but reduce the number of samples per channel.", "Real observations depart from the ideal through flagged data, correlated noise, gain drift, and atmospheric fluctuations."],
        "derivation": "For system temperature T_sys and bandwidth Delta-nu, one independent sample has fractional thermal uncertainty proportional to T_sys. Averaging n_pol polarizations for time tau produces sigma_T=T_sys/sqrt(n_pol Delta-nu tau). With SEFD=2 k T_sys/A_eff expressed in flux-density units, sigma_S=SEFD/sqrt(n_pol Delta-nu tau); correlator conventions can introduce an efficiency factor eta_s in the denominator.",
        "equation": r"\sigma_S=\frac{\mathrm{SEFD}}{\eta_s\sqrt{n_{\rm pol}\,\Delta\nu\,\tau}}",
        "example": 3,
        "limit": "The radiometer result is a thermal lower bound. RFI flagging, quantization/correlator efficiency, calibration drift, and confusion can dominate, so ideal sqrt(t) extrapolation eventually fails.",
        "prompt": "If a spectral channel is narrowed by a factor of 16, how much longer must you integrate to preserve the same thermal rms, all else equal?",
        "reading": "OpenStax Astronomy 2e §6.4; NRAO VLA Observational Status Summary and ALMA Basics describe practical sensitivity and observing constraints.",
        "figure": 3,
    },
    {
        "title": "Beam Convolution, Brightness Temperature, and Angular Scale",
        "hook": "Flux per synthesized beam becomes a brightness only after specifying the beam solid angle and a temperature convention.",
        "objectives": ["Derive the Rayleigh-Jeans brightness-temperature relation for a Gaussian beam.", "Convert Jy/beam to kelvin with explicit frequency and beam units.", "Explain beam dilution and why flux density is not surface brightness."],
        "evidence": ["A telescope measures sky brightness convolved with its point-spread function, not the unconvolved sky field.", "A source smaller than the beam has a diluted peak brightness even when its integrated flux is conserved.", "At radio frequencies h nu much less than k T for many thermal sources, but brightness temperature can describe nonthermal emission without being a physical gas temperature."],
        "derivation": "In the Rayleigh-Jeans limit I_nu=2 k T_b nu^2/c^2. For a Gaussian synthesized beam with FWHM axes theta_maj and theta_min, Omega_b=pi theta_maj theta_min/(4 ln 2), so T_b=lambda^2 S_nu/(2 k Omega_b) for flux density per beam. Convert Jy to SI and arcseconds to radians before evaluating.",
        "equation": r"T_b=\frac{\lambda^2 S_\nu}{2k\Omega_b},\qquad\Omega_b=\frac{\pi\theta_{\rm maj}\theta_{\rm min}}{4\ln2}",
        "example": 4,
        "limit": "The Rayleigh-Jeans brightness temperature is a coordinate on specific intensity; for coherent and synchrotron sources it can greatly exceed the kinetic temperature.",
        "prompt": "An unresolved source is observed with two beam sizes. Which reported quantity should remain stable under ideal imaging: peak Jy/beam, integrated Jy, or brightness temperature? State conditions.",
        "reading": "OpenStax Astronomy 2e §6.4 introduces the antenna beam; detailed brightness-temperature and convolution treatment is beyond its scope.",
        "figure": 4,
    },
    {
        "title": "Interferometry: Coherence and Complex Visibility",
        "hook": "A pair of antennas measures a spatial Fourier component of the sky, encoded in a complex correlation.",
        "objectives": ["Derive the two-element fringe phase from geometric delay.", "Interpret complex visibility amplitude and phase for a point-source pair.", "Convert baseline in wavelengths to fringe spacing and assess angular sensitivity."],
        "evidence": ["Correlating voltages preserves phase information that single-dish total-power measurements do not contain.", "A baseline samples one spatial frequency (u,v); changing hour angle rotates projected baseline coordinates.", "The longest baseline sets fine angular response while the shortest baseline constrains the largest recoverable structure."],
        "derivation": "For a small sky field (l,m), a baseline vector (u,v) measured in wavelengths yields V(u,v)=integral I(l,m) exp[-2 pi i (u l+v m)] dl dm. For a point source at l0, visibility amplitude is its flux and phase is -2 pi u l0 for a one-dimensional baseline. The fringe spacing is approximately lambda/B_proj; it is not necessarily the final synthesized-beam FWHM.",
        "equation": r"V(u,v)=\iint I(l,m)e^{-2\pi i(ul+vm)}\,dl\,dm,\qquad\theta_{\rm fringe}\simeq\lambda/B_{\rm proj}",
        "example": 5,
        "limit": "The flat-sky Fourier relation assumes a narrow field and ignores the w-term; wide-field imaging needs non-coplanar-baseline correction.",
        "prompt": "A point source moves east by one fringe spacing. What happens to its visibility phase on a fixed baseline? Why does amplitude not change for an ideal point source?",
        "reading": "OpenStax Astronomy 2e §6.4, especially its discussion of interferometer separation and resolution; ALMA Basics §Interferometry formalizes the visibility transform.",
        "figure": 5,
    },
    {
        "title": "Aperture Synthesis and Image Formation",
        "hook": "Earth rotation and multiple baselines fill the uv plane imperfectly; imaging is an inverse problem with a measurable point-spread function.",
        "objectives": ["Connect sampled visibilities to a dirty image and dirty beam.", "Explain how weighting changes resolution and sensitivity.", "Identify missing short spacings and deconvolution non-uniqueness."],
        "evidence": ["A finite uv sampling function multiplies the true visibility function; its Fourier transform convolves the true sky with the dirty beam.", "Natural weighting emphasizes densely sampled short baselines; uniform weighting can improve resolution at a noise cost.", "An interferometer without zero and short spacings filters broad smooth emission, even when a visually plausible deconvolution is produced."],
        "derivation": "Let S(u,v) be the sampling function. The measured visibility is S V, and inverse Fourier transformation gives I_dirty=I_true convolved with B_dirty, where B_dirty is the inverse transform of S. Deconvolution estimates a sky consistent with sampled data and a prior/regularizer; it cannot recreate unconstrained spatial frequencies without single-dish or compact-array information.",
        "equation": r"I_{\rm dirty}=\mathcal{F}^{-1}[S V]=I_{\rm sky}*B_{\rm dirty}",
        "example": 6,
        "limit": "The 1.02 lambda/B_max resolution estimate is a scale, not a full synthesized-beam prediction; uv weighting, taper, flagging, and source declination matter.",
        "prompt": "A smooth 8-arcminute H I cloud is observed with an array whose shortest baseline implies a 2-arcminute maximum recoverable scale. What map artifact or missing-flux behavior do you expect?",
        "reading": "OpenStax Astronomy 2e §6.4 covers VLA/ALMA arrays qualitatively; ALMA Basics provides a shortest-baseline largest-angular-scale estimate.",
        "figure": 6,
    },
    {
        "title": "Calibration I: Complex Gains and Bandpass",
        "hook": "Calibration solves for antenna-based complex gains by comparing measured correlations with a source model.",
        "objectives": ["Write the interferometric measurement equation for antenna gains.", "Distinguish flux-scale, phase, delay, bandpass, and polarization calibration.", "Estimate coherence loss from random residual phase."],
        "evidence": ["A baseline visibility is multiplied by one antenna gain and the complex conjugate of the other.", "A flux calibrator establishes amplitude scale; a nearby phase calibrator tracks rapid atmospheric/instrumental phase changes.", "Residual phase decorrelation reduces coherent amplitude approximately as exp(-sigma_phi^2/2) for Gaussian phase noise."],
        "derivation": "For antennas p and q, V_pq^obs=g_p g_q* V_pq^true+n_pq. With g=a exp(i phi), phase differences and amplitude products are coupled across baselines, so solve a connected antenna graph against a calibrator model. Bandpass calibration estimates frequency dependence; delay is the phase slope dphi/dnu divided by 2 pi.",
        "equation": r"V_{pq}^{\rm obs}(\nu,t)=g_p(\nu,t)g_q^*(\nu,t)V_{pq}^{\rm true}(\nu,t)+n_{pq}",
        "example": 7,
        "limit": "A wrong calibrator model can transfer systematic error to every target. The phase-coherence approximation assumes zero-mean Gaussian residual phase and does not model direction-dependent structure.",
        "prompt": "If residual phase rms doubles from 10 degrees to 20 degrees, does coherence loss double? Compute or reason from the exponential form.",
        "reading": "NRAO VLA calibration-pipeline documentation and ALMA data-processing documentation; OpenStax §6.4 does not cover calibration equations.",
        "figure": 7,
    },
    {
        "title": "Calibration II: Error Budgets and Imaging Systematics",
        "hook": "A formal image rms is not a complete uncertainty when the flux scale, primary beam, and deconvolution add correlated errors.",
        "objectives": ["Propagate independent fractional calibration terms in quadrature.", "Separate thermal noise from multiplicative and spatially correlated systematics.", "Design residual and jackknife checks for a calibrated image."],
        "evidence": ["Independent small fractional errors combine in quadrature, whereas shared calibration errors correlate many image pixels.", "Primary-beam correction amplifies both signal and noise toward the field edge.", "Residual images, calibrator closure quantities, split-data comparisons, and injection tests probe different failure modes."],
        "derivation": "For a derived flux S=f(x_i), first-order propagation gives sigma_S^2=sum_i (partial f/partial x_i)^2 sigma_i^2 plus covariance terms. For independent fractional terms f_j, (sigma_S/S)^2=sum_j f_j^2. A multiplicative flux-scale term remains correlated among sources calibrated with the same solution and should not be averaged down as independent pixel noise.",
        "equation": r"\left(\frac{\sigma_S}{S}\right)^2=\sum_j f_j^2+2\sum_{i<j}\rho_{ij}f_i f_j",
        "example": 8,
        "limit": "Quadrature is justified only for independent zero-mean errors; common-mode flux-scale uncertainty requires covariance-aware comparisons.",
        "prompt": "Two sources share the same 5% flux-scale error but have independent 1% thermal errors. Which uncertainty cancels in their flux ratio, and which does not?",
        "reading": "NRAO VLA calibration and imaging-pipeline documentation; exact error propagation is developed here beyond introductory textbook coverage.",
        "figure": 8,
    },
    {
        "title": "Spectral-Line Observing and Doppler Inference",
        "hook": "A spectral cube combines two-dimensional angular response with a frequency axis whose calibration becomes velocity only after a rest frequency and convention are chosen.",
        "objectives": ["Convert channel frequency to nonrelativistic radial velocity with units.", "Distinguish frequency resolution from velocity resolution.", "Plan line sensitivity without hiding the channel-width trade-off."],
        "evidence": ["A narrow line can be diluted by channels wider than its intrinsic width.", "The radio convention v=c(nu_0-nu)/nu_0 differs slightly from optical and relativistic conventions at high speeds.", "Bandpass ripple, baseline subtraction, and sideband/LO conventions can imitate broad weak lines."],
        "derivation": "For |v| much less than c, the first-order Doppler relation is Delta-nu/nu_0 approximately -v_rad/c. Therefore delta-v=c delta-nu/nu_0. At larger speeds use the chosen relativistic Doppler definition and document the frame correction (topocentric, barycentric, LSR).", 
        "equation": r"v_{\rm rad}\simeq c\frac{\nu_0-\nu}{\nu_0},\qquad\delta v\simeq c\frac{\delta\nu}{\nu_0}",
        "example": 9,
        "limit": "The linear radio Doppler convention is appropriate for Galactic velocities but not precision high-redshift work; frame and relativistic conventions must be recorded.",
        "prompt": "At fixed channel width in Hz, why does velocity resolution change with observing frequency? Which band gives finer km/s channels?",
        "reading": "OpenStax Astronomy 2e §5.6 covers Doppler shift; §6.4 establishes radio spectrometers. ALMA Basics §Spectral resolution provides channel examples.",
        "figure": 9,
    },
    {
        "title": "The 21-cm Hyperfine Line and H I Column Density",
        "hook": "The 21-cm line maps neutral atomic hydrogen through a weak hyperfine transition that penetrates dust but still depends on optical depth and spin temperature.",
        "objectives": ["Explain the hydrogen hyperfine transition and rest frequency.", "Derive the optically thin H I column-density conversion from integrated brightness temperature.", "State when self-absorption and opacity invalidate the thin-line estimate."],
        "evidence": ["The 1420.4058 MHz line is emitted by the ground-state hyperfine transition of neutral hydrogen.", "For optically thin gas with spin temperature well above the background, N_HI=1.823e18 integral T_B dv cm^-2 when T_B is K and dv is km/s.", "The all-sky HI4PI survey combines EBHIS and GASS data and reports angular and spectral response that must be considered before comparing columns."],
        "derivation": "Radiative transfer gives T_B(v) approximately T_s tau(v) for tau much less than one. Integrating the 21-cm absorption coefficient over velocity, using the atomic transition constants and expressing dv in km/s, yields N_HI=1.823e18 integral T_B(v) dv cm^-2. For finite opacity the integrand is T_s tau, not T_B alone; the thin estimate then undercounts column density.",
        "equation": r"N_{\rm HI}=1.823\times10^{18}\int T_B(v)\,dv\quad{\rm cm}^{-2}",
        "example": 10,
        "limit": "The conversion assumes optically thin emission and a consistent brightness-temperature scale; cold H I self-absorption can hide column density.",
        "prompt": "A narrow, cold component has the same observed integrated T_B dv as a warm optically thin cloud. What additional observable would help distinguish their column densities?",
        "reading": "OpenStax Astronomy 2e §20.2 discusses the 21-cm line; HI4PI Collaboration (2016) gives survey response. This course derives the conversion beyond the introductory text.",
        "figure": 10,
    },
    {
        "title": "Pulsars: Dispersion, Scattering, and Precision Timing",
        "hook": "A millisecond-to-second pulse train is an astronomical clock whose arrival times encode plasma column, rotation, orbit, and instrumental delay.",
        "objectives": ["Derive cold-plasma dispersive delay proportional to DM nu^-2.", "Distinguish dedispersion, scattering broadening, and intrinsic pulse evolution.", "Explain a phase-connected timing model and its uncertainty budget."],
        "evidence": ["The plasma group velocity is frequency dependent, so low-frequency pulses arrive later.", "DM is the integral of free-electron density along the line of sight and is not itself a geometric distance without a Galactic electron model.", "Timing residuals combine clock, ephemeris, propagation, instrumental, and rotational-noise terms."],
        "derivation": "For a cold, unmagnetized plasma with nu much greater than plasma frequency, group delay is proportional to integral n_e dl times nu^-2. Astronomical convention gives Delta-t(ms)=4.148808e3 DM(pc cm^-3)[nu_low,GHz^-2-nu_high,GHz^-2]. Dedispersion aligns frequency channels; it cannot undo multipath scattering that broadens the pulse.",
        "equation": r"\Delta t=4.148808\,\mathrm{ms}\,\mathrm{DM}\left(\nu_{\rm low,GHz}^{-2}-\nu_{\rm high,GHz}^{-2}\right)",
        "example": 11,
        "limit": "The cold-plasma law is a propagation model. Solar-wind contributions, frequency-dependent profile shape, and DM variation can bias timing if treated as a constant delay.",
        "prompt": "A pulsar is observed at 400 and 1400 MHz. What happens to the dispersion delay if DM doubles? Why can channel averaging leave residual smearing after dedispersion?",
        "reading": "OpenStax Astronomy 2e §23.4 introduces pulsars; the ATNF Pulsar Catalogue documents P0, P1, DM, and derived parameters. Timing analysis goes beyond the text.",
        "figure": 11,
    },
    {
        "title": "Radio Transients, Pulsar Surveys, and Selection Functions",
        "hook": "A survey detects a population filtered by cadence, beam, propagation, sensitivity, and threshold—not an unbiased census of sources.",
        "objectives": ["Quantify completeness and binomial uncertainty in a detection sample.", "Explain how dispersion smearing and scattering reshape pulsar detectability.", "Separate a survey detection threshold from a physical population boundary."],
        "evidence": ["A flux-limited survey samples more volume for brighter objects, while beaming and pulse broadening affect detectability.", "Fast transients can fall between cadence samples even when their peak flux exceeds a nominal threshold.", "Completeness must be estimated with injection/recovery or external comparisons, not inferred from detected counts alone."],
        "derivation": "For N injected sources and k recovered under a defined pipeline, completeness p_hat=k/N. A first-order binomial standard error is sqrt[p_hat(1-p_hat)/N]. This uncertainty excludes model mismatch in the injected population, spatially varying sensitivity, and correlated failures; stratify by flux, width, sky position, and DM when possible.",
        "equation": r"\hat p=\frac{k}{N},\qquad\sigma_{\hat p}\simeq\sqrt{\frac{\hat p(1-\hat p)}{N}}",
        "example": 12,
        "limit": "Binomial errors assume independent trials with one common recovery probability; a heterogeneous sky requires a stratified completeness model.",
        "prompt": "Two sky tiles each recover 84 of 100 injections, but one tile has twice the thermal noise. Why is the same aggregate completeness not evidence of equal selection functions?",
        "reading": "ATNF Pulsar Catalogue and survey papers provide real selection context; use the named survey release and injection methodology when claiming completeness.",
        "figure": 12,
    },
    {
        "title": "Galactic H I: Rotation, Geometry, and Mapping",
        "hook": "A 21-cm velocity cube turns a line-of-sight Doppler field into a model-dependent map of Galactic gas and kinematics.",
        "objectives": ["Use the flat-rotation inner-Galaxy relation to infer Galactocentric radius from longitude and radial velocity.", "Distinguish measured LSR velocity from inferred distance and radius.", "Explain near-far ambiguity and non-circular motions."],
        "evidence": ["The 21-cm line is observable through much of the Galactic disk, including dusty sightlines.", "For a flat circular rotation curve, v_LSR=(Theta(R)R0/R-Theta0)sin(l) on the inner-Galaxy sightline.", "Streaming motions, spiral arms, and the solar motion perturb the simple axisymmetric conversion."],
        "derivation": "Set Theta(R)=Theta0 and solve v_LSR=Theta0(R0/R-1)sin(l) for R=R0/[1+v_LSR/(Theta0 sin(l))]. This gives Galactocentric radius for a chosen longitude under circular rotation. Heliocentric distance requires a second geometric step and has a near/far ambiguity inside the solar circle.",
        "equation": r"R=\frac{R_0}{1+v_{\rm LSR}/(\Theta_0\sin l)}",
        "example": 13,
        "limit": "The flat, axisymmetric rotation curve is an idealization; streaming velocities of order tens of km/s can shift inferred radii and distances substantially.",
        "prompt": "At fixed longitude, how does a positive non-circular velocity perturbation propagate into inferred R in this model? Give the derivative sign.",
        "reading": "OpenStax Astronomy 2e §20.2 introduces interstellar gas and 21-cm observations; HI4PI (2016) provides an all-sky spectral data product for modern mapping.",
        "figure": 13,
    },
    {
        "title": "Radio Surveys: Catalogs, Confusion, and Reproducible Analysis",
        "hook": "A survey result is a chain from calibrated visibilities or spectra to source catalog, completeness model, and population claim.",
        "objectives": ["Calculate completeness-corrected surface density and Poisson counting uncertainty.", "Compare thermal noise, confusion, and calibration floors.", "Design a reproducible survey-analysis record with provenance and selection cuts."],
        "evidence": ["NVSS and other radio surveys enable population studies but differ in resolution, frequency, coverage, and source-finding thresholds.", "Confusion blends sources when source density approaches the number of independent beams; angular resolution changes the catalog itself.", "A catalog row is not a raw measurement: flux calibration, masking, source association, and completeness corrections intervene."],
        "derivation": "For N_det detections over usable area A with completeness C, the corrected surface density is Sigma=N_det/(A C). Under a simple Poisson model, sigma_Sigma=sqrt(N_det)/(A C), before uncertainty in C, A, flux scale, and source association. If completeness is uncertain, propagate its covariance rather than treating C as exact.",
        "equation": r"\Sigma=\frac{N_{\rm det}}{A C},\qquad\sigma_\Sigma\simeq\frac{\sqrt{N_{\rm det}}}{A C}",
        "example": 14,
        "limit": "The Poisson uncertainty ignores cosmic variance, clustering, completeness uncertainty, and Eddington bias near the threshold; state which terms dominate the intended inference.",
        "prompt": "A deeper survey detects a higher source density. List two physical interpretations and two selection/systematic explanations before claiming population evolution.",
        "reading": "OpenStax Astronomy 2e §6.4 sets the array context. NVSS (Condon et al. 1998) and HI4PI (2016) are survey references; consult each release's own mask and completeness documentation.",
        "figure": 14,
    },
]

LABS = [
    {"title":"Continuum Mechanisms and Spectral Indices","focus":"Lectures 01-02 · radio spectra and antenna response","dataset":"continuum_spectrum.csv","objective":"fit a spectral index to a frequency-flux series and distinguish an optically thin synchrotron slope from a low-frequency turnover","steps":["Read the CSV schema and plot log flux against log frequency, retaining measurement uncertainties.","Fit S_nu proportional to nu^alpha using weighted least squares; compare a single power law with a broken/turnover model using residuals.","Compute the synchrotron characteristic frequency for the supplied B and gamma values and compare its scale with the sampled band.","Convolve a point-source and an extended-source sketch with the listed single-dish beam; explain beam dilution and flux conservation.","Perturb each flux by its quoted uncertainty in 1000 seeded realizations and report the median alpha and central 68% interval."],"measurement":"Record fitted alpha, covariance, residual RMS, beam FWHM at each frequency, and model-selection caveat.","answer":"A single power law is only a local empirical fit; curvature can reflect aging, absorption, or mixed components."},
    {"title":"Radiometer Sensitivity and Brightness Temperature","focus":"Lectures 03-04 · channelized observations","dataset":"radiometer_trials.csv","objective":"predict thermal rms, estimate system temperature from a measured rms, and convert Jy per beam into Rayleigh-Jeans brightness temperature","steps":["Reproduce the radiometer prediction for every bandwidth and integration-time row.","Use the measured rms columns to estimate eta_s or identify a systematic floor; do not fit below the supplied floor.","Convert the listed 1.4-GHz peak flux density per beam to T_b using the Gaussian beam solid angle.","Repeat the T_b calculation after doubling both beam axes and explain the factor-of-four beam-area change.","Propagate SEFD, bandwidth, integration-time, and beam uncertainties to the reported derived quantities."],"measurement":"Deliver an rms-versus-integration plot, one brightness-temperature calculation, and a table separating thermal and systematic terms.","answer":"At fixed SEFD and bandwidth, ideal rms follows tau^-1/2; excess long-time scatter is evidence against pure radiometer noise."},
    {"title":"Baseline Geometry and Visibility Sampling","focus":"Lectures 05-06 · point-source and extended emission","dataset":"uv_samples.csv","objective":"calculate fringe phase and resolution scales, visualize uv coverage, and demonstrate missing short-spacing sensitivity","steps":["Convert the tabulated projected baselines to wavelengths at the stated observing frequency.","For each source offset, calculate complex point-source visibility amplitude and phase from the flat-sky measurement equation.","Plot uv samples with equal axis scale and identify the largest gap in position angle and radial spacing.","Construct a one-dimensional dirty beam from the supplied sampling coordinates using a discrete inverse Fourier sum.","Compare a compact source and a broad Gaussian after applying the same uv sampling; quantify recovered integrated-flux fraction."],"measurement":"Submit the uv plot, dirty-beam plot, recovered-flux table, and a paragraph distinguishing resolution from largest recoverable scale.","answer":"Long baselines supply fine angular scales; absent short baselines suppress smooth emission even when the synthesized beam is narrow."},
    {"title":"Complex Gain Calibration and Error Propagation","focus":"Lectures 07-08 · calibrator and target record","dataset":"calibration_records.csv","objective":"solve a scalar gain model, quantify phase decorrelation, and combine independent plus common-mode uncertainty","steps":["Estimate antenna amplitude and phase residuals from the calibrator rows; flag the injected outlier before averaging.","Apply the scalar gain correction to target visibility amplitudes and compare with the known teaching-model flux.","Calculate Gaussian phase coherence for each residual-phase rms and compare predicted versus observed amplitude ratio.","Build a covariance-aware flux error budget with thermal, gain-amplitude, and common flux-scale terms.","Repeat the target analysis after removing one scan at a time and report leave-one-scan-out stability."],"measurement":"Report gain estimates, outlier rule, residual statistics, corrected flux, uncertainty covariance, and one diagnostic plot.","answer":"The common flux-scale term does not average down across sources sharing the same calibrator solution."},
    {"title":"Spectral Cubes, Doppler Velocity, and Line Width","focus":"Lectures 09-10 · H I spectral-line inference","dataset":"hi_spectrum_teaching.csv","objective":"convert frequency to radio velocity, fit a Gaussian line, integrate brightness temperature, and derive an optically thin H I column","steps":["Use the exact rest frequency and radio convention to create a velocity axis; verify sign with a receding-source test.","Fit a Gaussian plus constant baseline to the supplied spectrum and inspect fit residuals near line wings.","Numerically integrate T_B dv using the channel spacing, then compare with the analytic Gaussian area.","Apply the thin H I column-density conversion and perturb baseline and line amplitude to estimate systematic sensitivity.","State why this teaching spectrum cannot establish real optical depth or Galactic structure."],"measurement":"Submit the velocity spectrum, fit parameters and covariance, integrated brightness, N_HI, and a concise assumptions table.","answer":"The optically thin N_HI is proportional to integrated brightness; a baseline error across a broad line can dominate the formal fit uncertainty."},
    {"title":"Pulsar Dispersion and Timing Residuals","focus":"Lectures 11-12 · frequency-dependent arrival times","dataset":"pulsar_arrivals.csv","objective":"fit a nu^-2 dispersion delay, estimate DM uncertainty, and distinguish dispersion from achromatic timing residuals","steps":["Plot arrival-time offset against observing frequency and fit t=t_inf+K DM nu^-2 with uncertainty weights.","Compare fitted DM with the supplied reference DM and report residuals in milliseconds.","Calculate intra-channel dispersive smearing for the listed channel widths at the lowest observing frequency.","Test a pulse-broadening term proportional to nu^-4 and compare residual structure before and after the fit.","Explain why a survey's measured detection fraction depends on pulse width, DM, and cadence."],"measurement":"Deliver fitted DM, uncertainty, residual plot, channel-smearing table, and a statement separating measured delay from inferred distance.","answer":"A frequency-dependent delay is consistent with dispersion, but frequency-dependent intrinsic profile shape can bias a simple timing fit."},
    {"title":"Survey Completeness and Galactic H I Mapping","focus":"Lectures 13-14 · selection correction and rotation inference","dataset":"survey_injections.csv","objective":"estimate completeness, correct source surface density, infer an inner-Galaxy radius under a stated rotation model, and assess uncertainty","steps":["Partition injection/recovery rows by flux bin and sky tile; compute p_hat and binomial standard error for each stratum.","Compute corrected surface density and Poisson uncertainty for the supplied detection count and usable area.","Propagate completeness uncertainty using first-order derivatives and compare with Poisson-only uncertainty.","Use the supplied l and v_LSR measurements with the stated flat-rotation parameters to compute Galactocentric radii.","Write a reproducible analysis note separating survey products, teaching records, model assumptions, and unresolved systematics."],"measurement":"Submit completeness plot, corrected-density calculation, kinematic radius table, and a one-page method/provenance note.","answer":"A completeness-corrected estimate remains conditional on injection realism, usable-area masks, and the adopted circular-rotation model."},
]

LABS[6]["steps"].append(
    "Use CDS catalog J/A+A/594/A116 and its ReadMe to select a listed 20-by-20-degree Galactic HI4PI FITS subcube nearest l=30 degrees, b=0 degrees. Record the actual file name, coordinates, FITS WCS, velocity convention, units, access date, and checksum; compare one real spectrum and a numerical N_HI integral with the supplied synthetic injection exercise."
)
LABS[2]["steps"][0] = (
    "The supplied u_lambda and v_lambda columns are already spatial frequencies in wavelengths. "
    "Verify the scale by converting a 3-km baseline at 1.4 GHz to wavelengths, then identify each sample's radius and position angle in the uv plane."
)
LABS[3]["steps"][1] = (
    "Treat the target amplitude_ratio values as observed-to-model ratios for a 120-mJy teaching source. "
    "Estimate the scalar amplitude gain from the three good calibrator scans, exclude the 1.55 outlier using a documented rule, "
    "and correct each target estimate before comparing with 120 mJy."
)
LABS[6]["steps"].insert(
    4,
    "Load ../data/hi_kinematics_teaching.csv separately from the injection table and compute model-dependent Galactocentric radii from its longitude and v_LSR columns."
)

def page(title: str, body: str, css: str = CSS) -> str:
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title><script id='MathJax-script' async src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script><style>{css}</style></head><body>{body}</body></html>"

def fmt(value: float, digits: int = 4) -> str:
    return f"{value:.{digits}g}"

def calc(number: int) -> dict[str, float | str]:
    """Shared computations used in lecture, lab, and problem-set artifacts."""
    if number == 1:
        field_gauss, gamma = 10e-6, 1.0e4
        return {"value": 4.2e6 * field_gauss * gamma**2, "unit": "Hz", "label": "nu_c", "inputs": f"B={field_gauss:g} G, gamma={gamma:g}"}
    if number == 2:
        wavelength = C / 1.4e9
        beam_arcmin = 1.02 * wavelength / 25.0 * ARCSEC_PER_RAD / 60
        area_eff = 0.70 * math.pi * 25.0**2 / 4
        return {"value": beam_arcmin, "unit": "arcmin", "label": "FWHM", "area": area_eff, "inputs": "nu=1.4 GHz, D=25 m, eta_a=0.70"}
    if number == 3:
        sigma_jy = 300.0 / math.sqrt(2 * 1.0e6 * 3600.0)
        return {"value": sigma_jy * 1e3, "unit": "mJy", "label": "sigma_S", "inputs": "SEFD=300 Jy, n_pol=2, Delta-nu=1 MHz, tau=3600 s, eta_s=1"}
    if number == 4:
        wavelength = C / 1.4e9
        theta = 45.0 / ARCSEC_PER_RAD
        omega = math.pi * theta**2 / (4 * math.log(2))
        temp = wavelength**2 * JY / (2 * K_B * omega)
        return {"value": temp, "unit": "K", "label": "T_b", "inputs": "nu=1.4 GHz, S=1 Jy/beam, circular FWHM=45 arcsec"}
    if number == 5:
        fringe_arcsec = C / 1.4e9 / 3000.0 * ARCSEC_PER_RAD
        source_offset_rad = 10.0 / ARCSEC_PER_RAD
        phase_deg = -360 * (3000.0 / (C / 1.4e9)) * source_offset_rad
        return {"value": fringe_arcsec, "unit": "arcsec", "label": "fringe spacing", "phase": phase_deg, "inputs": "nu=1.4 GHz, B_proj=3.0 km, source offset=10 arcsec"}
    if number == 6:
        resolution = 1.02 * (C / 100e9) / 16e3 * ARCSEC_PER_RAD
        max_scale = 0.6 * (C / 100e9) / 15.0 * ARCSEC_PER_RAD
        return {"value": resolution, "unit": "arcsec", "label": "synthesized FWHM scale", "max_scale": max_scale, "inputs": "nu=100 GHz, B_max=16 km, B_min=15 m"}
    if number == 7:
        sigma_phase = math.radians(10.0)
        return {"value": math.exp(-sigma_phase**2 / 2), "unit": "", "label": "coherence", "inputs": "Gaussian residual phase rms=10 deg"}
    if number == 8:
        fraction = math.sqrt(0.05**2 + 0.03**2 + 0.02**2)
        return {"value": 120.0 * fraction, "unit": "mJy", "label": "sigma_S", "fraction": fraction, "inputs": "S=120 mJy; independent 5%, 3%, and 2% terms"}
    if number == 9:
        velocity = C * 0.5e6 / F_HI / 1000
        return {"value": velocity, "unit": "km/s", "label": "v_radio", "channel": C * 10e3 / F_HI / 1000, "inputs": "nu0=1420.40575177 MHz, nu0-nu=0.500 MHz; channel=10 kHz"}
    if number == 10:
        integral = 120.0 * 8.0
        return {"value": 1.823e18 * integral, "unit": "cm^-2", "label": "N_HI", "integral": integral, "inputs": "integrated brightness=960 K km/s (top-hat equivalent 120 K x 8 km/s)"}
    if number == 11:
        dm = 56.8
        delay_ms = 4.148808 * dm * (0.4**-2 - 1.4**-2)
        return {"value": delay_ms, "unit": "ms", "label": "dispersion delay", "inputs": "DM=56.8 pc cm^-3; frequencies=0.400 and 1.400 GHz"}
    if number == 12:
        fraction = 84 / 100
        return {"value": fraction, "unit": "", "label": "completeness", "uncertainty": math.sqrt(fraction * (1 - fraction) / 100), "inputs": "84 recovered of 100 injected"}
    if number == 13:
        radius = 8.2 / (1 + 100 / (236 * math.sin(math.radians(30))))
        return {"value": radius, "unit": "kpc", "label": "R_GC", "inputs": "R0=8.2 kpc, Theta0=236 km/s, l=30 deg, v_LSR=100 km/s"}
    corrected = 1200 / (20 * 0.84)
    return {"value": corrected, "unit": "deg^-2", "label": "corrected surface density", "uncertainty": math.sqrt(1200) / (20 * 0.84), "inputs": "N_det=1200, usable area=20 deg^2, completeness=0.84"}

def result_text(number: int) -> str:
    result = calc(number)
    extra = ""
    if "area" in result:
        extra = f"; A_eff = {fmt(float(result['area']))} m^2"
    if "phase" in result:
        phase = float(result["phase"])
        extra = f"; phase = {fmt(phase)} deg ({fmt(phase % 360)} deg modulo 360)"
    if "max_scale" in result:
        extra = f"; largest-scale estimate = {fmt(float(result['max_scale']))} arcsec"
    if "fraction" in result:
        extra = f"; fractional uncertainty = {fmt(float(result['fraction']))}; sigma_S = {fmt(float(result['value']))} mJy" if number == 8 else f"; binomial SE = {fmt(float(result['uncertainty']))}"
    if number == 9:
        extra = f"; 10-kHz channel = {fmt(float(result['channel']))} km/s"
    if number == 10:
        extra = f"; integral = {fmt(float(result['integral']))} K km/s"
    if number == 14:
        extra = f"; Poisson-only uncertainty = {fmt(float(result['uncertainty']))} deg^-2"
    return f"{result['label']} = {fmt(float(result['value']))} {result['unit']}{extra}"

def svg(number: int) -> str:
    """Fourteen hand-authored figures; no shared layout or geometry template."""
    figures = {
        1: '<svg viewBox="0 0 900 440" role="img" aria-label="Synchrotron spectrum with low-frequency absorption turnover and high-frequency cooling break"><path d="M92 350H830M92 350V58" fill="none" stroke="#17324d" stroke-width="4"/><path d="M116 320C175 317 188 268 250 207S374 119 493 105S630 176 795 242" fill="none" stroke="#a33a3a" stroke-width="8"/><line x1="250" y1="207" x2="250" y2="350" stroke="#087e8b" stroke-width="3" stroke-dasharray="8 8"/><line x1="493" y1="105" x2="493" y2="350" stroke="#b66a0a" stroke-width="3" stroke-dasharray="4 9"/><text x="340" y="405" font-size="22">log frequency</text><text x="12" y="80" font-size="21">log Sν</text><text x="170" y="185" font-size="18">self-absorption</text><text x="510" y="92" font-size="18">cooling break</text></svg>',
        2: '<svg viewBox="0 0 900 440" role="img" aria-label="Radio dish cross-section showing feed illumination, aperture, and diffraction beam"><path d="M150 90Q430 400 710 90" fill="none" stroke="#17324d" stroke-width="12"/><path d="M192 140L428 72M668 140L432 72" stroke="#087e8b" stroke-width="5"/><path d="M410 76L386 40L434 40Z" fill="#b66a0a"/><line x1="150" y1="90" x2="150" y2="36" stroke="#a33a3a" stroke-width="4"/><line x1="710" y1="90" x2="710" y2="36" stroke="#a33a3a" stroke-width="4"/><path d="M125 30H735M125 20V40M735 20V40" stroke="#a33a3a" stroke-width="3"/><text x="412" y="25" font-size="20">D</text><text x="390" y="116" font-size="18">feed</text><text x="390" y="340" font-size="20">reflector surface</text><path d="M425 66L378 0M435 66L485 0" stroke="#b66a0a" stroke-width="3" stroke-dasharray="7 7"/></svg>',
        3: '<svg viewBox="0 0 900 440" role="img" aria-label="Radiometer rms sensitivity curve falling as inverse square root of integration time toward a systematic floor"><path d="M98 350H820M98 350V55" stroke="#17324d" stroke-width="4"/><path d="M120 92C210 145 306 198 405 241S587 294 700 313" fill="none" stroke="#087e8b" stroke-width="8"/><line x1="105" y1="324" x2="820" y2="324" stroke="#a33a3a" stroke-width="5" stroke-dasharray="12 8"/><circle cx="700" cy="313" r="10" fill="#b66a0a"/><text x="350" y="400" font-size="21">integration time (log τ)</text><text x="8" y="78" font-size="20">rms noise</text><text x="705" y="306" font-size="17">floor</text><text x="215" y="125" font-size="18">thermal ∝ τ^-1/2</text></svg>',
        4: '<svg viewBox="0 0 900 440" role="img" aria-label="Compact source diluted by a broad Gaussian beam with beam axes and convolved peak brightness"><ellipse cx="445" cy="220" rx="275" ry="125" fill="#dff4f5" stroke="#087e8b" stroke-width="6"/><ellipse cx="445" cy="220" rx="38" ry="23" fill="#a33a3a"/><path d="M170 220H720M445 95V345" stroke="#17324d" stroke-width="2" stroke-dasharray="8 8"/><ellipse cx="445" cy="220" rx="135" ry="62" fill="none" stroke="#b66a0a" stroke-width="4"/><text x="360" y="72" font-size="20">Gaussian beam Ωb</text><text x="467" y="214" font-size="18">source</text><text x="188" y="382" font-size="19">convolution preserves integrated flux, dilutes peak</text></svg>',
        5: '<svg viewBox="0 0 900 440" role="img" aria-label="Two-element interferometer geometry with projected baseline, wavefront, source offset, and fringe phase"><circle cx="160" cy="340" r="19" fill="#17324d"/><circle cx="680" cy="340" r="19" fill="#17324d"/><path d="M160 340L680 340" stroke="#b66a0a" stroke-width="7"/><path d="M80 100Q360 148 640 196M80 160Q360 208 640 256M80 220Q360 268 640 316" fill="none" stroke="#087e8b" stroke-width="4"/><path d="M422 330L510 60" stroke="#a33a3a" stroke-width="5"/><path d="M510 60L495 89M510 60L528 85" stroke="#a33a3a" stroke-width="5"/><text x="380" y="375" font-size="21">projected baseline B</text><text x="520" y="74" font-size="18">source direction</text><text x="84" y="290" font-size="18">equal-phase wavefronts</text></svg>',
        6: '<svg viewBox="0 0 900 440" role="img" aria-label="Sparse Fourier plane coverage and corresponding dirty beam sidelobes"><rect x="72" y="52" width="350" height="320" fill="#fbfcfd" stroke="#17324d" stroke-width="4"/><line x1="247" y1="55" x2="247" y2="370" stroke="#d5dee5" stroke-width="2"/><line x1="75" y1="212" x2="420" y2="212" stroke="#d5dee5" stroke-width="2"/><circle cx="140" cy="140" r="8" fill="#087e8b"/><circle cx="180" cy="285" r="8" fill="#087e8b"/><circle cx="310" cy="130" r="8" fill="#087e8b"/><circle cx="355" cy="260" r="8" fill="#087e8b"/><circle cx="247" cy="212" r="6" fill="#a33a3a"/><text x="158" y="405" font-size="20">sampled uv plane</text><path d="M495 210H846M670 60V365" stroke="#17324d" stroke-width="3"/><path d="M505 210C560 212 577 240 603 294S643 362 670 210S696 60 737 128S784 196 840 210" fill="none" stroke="#b66a0a" stroke-width="7"/><text x="550" y="405" font-size="20">dirty beam cut</text><text x="510" y="80" font-size="18">sidelobes from gaps</text></svg>',
        7: '<svg viewBox="0 0 900 440" role="img" aria-label="Complex-gain calibration phasors comparing measured baseline phase with corrected phase"><circle cx="300" cy="225" r="142" fill="none" stroke="#d5dee5" stroke-width="4"/><line x1="300" y1="225" x2="430" y2="168" stroke="#a33a3a" stroke-width="8"/><line x1="300" y1="225" x2="421" y2="191" stroke="#087e8b" stroke-width="8"/><circle cx="300" cy="225" r="9" fill="#17324d"/><path d="M354 201A60 60 0 0 1 356 206" fill="none" stroke="#b66a0a" stroke-width="5"/><text x="450" y="162" font-size="19">observed phase</text><text x="450" y="202" font-size="19">model-corrected phase</text><text x="170" y="410" font-size="20">gain amplitude and phase are solved together</text></svg>',
        8: '<svg viewBox="0 0 900 440" role="img" aria-label="Flux uncertainty budget showing independent thermal, gain, and common calibration components"><path d="M120 340H820M120 340V60" stroke="#17324d" stroke-width="4"/><rect x="210" y="220" width="110" height="120" fill="#087e8b"/><rect x="390" y="170" width="110" height="170" fill="#b66a0a"/><rect x="570" y="110" width="110" height="230" fill="#a33a3a"/><text x="215" y="375" font-size="18">thermal</text><text x="383" y="375" font-size="18">gain terms</text><text x="558" y="375" font-size="18">common scale</text><path d="M180 88H720" stroke="#596875" stroke-width="3" stroke-dasharray="8 8"/><text x="280" y="78" font-size="18">covariance changes the total</text></svg>',
        9: '<svg viewBox="0 0 900 440" role="img" aria-label="Radio spectral line plotted in frequency and velocity with rest frequency and channel width marked"><path d="M110 345H820M110 345V55" stroke="#17324d" stroke-width="4"/><path d="M150 320C300 318 366 303 420 250S490 110 550 105S630 270 680 310S760 322 800 321" fill="none" stroke="#087e8b" stroke-width="7"/><line x1="550" y1="102" x2="550" y2="347" stroke="#a33a3a" stroke-width="3" stroke-dasharray="8 8"/><path d="M445 370H475M445 362V378M475 362V378" stroke="#b66a0a" stroke-width="4"/><text x="540" y="83" font-size="18">line center</text><text x="280" y="407" font-size="20">frequency → radio velocity</text><text x="390" y="225" font-size="18">channel width</text></svg>',
        10: '<svg viewBox="0 0 900 440" role="img" aria-label="Hydrogen 21-centimeter hyperfine energy levels and emitted radio photon"><line x1="170" y1="130" x2="420" y2="130" stroke="#17324d" stroke-width="9"/><line x1="170" y1="300" x2="420" y2="300" stroke="#087e8b" stroke-width="9"/><path d="M300 150V278" stroke="#a33a3a" stroke-width="6"/><path d="M300 278L288 255M300 278L312 255" stroke="#a33a3a" stroke-width="6"/><path d="M440 215C510 155 565 275 625 215S740 155 800 215" fill="none" stroke="#b66a0a" stroke-width="6"/><text x="175" y="105" font-size="20">F=1 triplet</text><text x="175" y="340" font-size="20">F=0 singlet</text><text x="500" y="300" font-size="19">21-cm photon</text><text x="490" y="125" font-size="18">1420.4058 MHz</text></svg>',
        11: '<svg viewBox="0 0 900 440" role="img" aria-label="Pulsar pulse arrival times dispersed across radio frequencies and aligned by dedispersion"><path d="M110 345H830M110 345V58" stroke="#17324d" stroke-width="4"/><path d="M150 95V315M300 95V315M450 95V315M600 95V315M750 95V315" stroke="#d5dee5" stroke-width="2"/><path d="M150 250Q165 120 180 250M300 210Q315 80 330 210M450 165Q465 65 480 165M600 125Q615 60 630 125M750 95Q765 48 780 95" fill="none" stroke="#a33a3a" stroke-width="7"/><path d="M150 375H780" stroke="#087e8b" stroke-width="4" stroke-dasharray="10 7"/><text x="375" y="415" font-size="19">arrival phase after ν⁻² correction</text><text x="15" y="85" font-size="19">frequency</text><text x="668" y="75" font-size="18">low ν arrives late</text></svg>',
        12: '<svg viewBox="0 0 900 440" role="img" aria-label="Survey completeness curve with injection counts and flux-dependent recovery fraction"><path d="M100 350H820M100 350V55" stroke="#17324d" stroke-width="4"/><path d="M125 315C235 300 320 253 410 188S575 108 685 82S770 73 805 70" fill="none" stroke="#087e8b" stroke-width="8"/><circle cx="170" cy="304" r="11" fill="#a33a3a"/><circle cx="350" cy="226" r="11" fill="#a33a3a"/><circle cx="535" cy="132" r="11" fill="#a33a3a"/><circle cx="720" cy="79" r="11" fill="#a33a3a"/><line x1="100" y1="98" x2="820" y2="98" stroke="#b66a0a" stroke-width="3" stroke-dasharray="8 8"/><text x="335" y="405" font-size="20">injected flux density</text><text x="20" y="76" font-size="19">recovery fraction</text><text x="680" y="120" font-size="18">completeness cut</text></svg>',
        13: '<svg viewBox="0 0 900 440" role="img" aria-label="Galactic longitude-velocity diagram with tangent-point envelope and H I emission ridges"><path d="M100 340H835M100 340V60" stroke="#17324d" stroke-width="4"/><path d="M130 325C245 280 295 130 405 92S570 160 650 225S755 300 810 320" fill="none" stroke="#087e8b" stroke-width="7"/><path d="M130 320C245 305 310 265 392 230S550 205 670 245S760 292 810 315" fill="none" stroke="#a33a3a" stroke-width="5"/><circle cx="406" cy="92" r="12" fill="#b66a0a"/><text x="340" y="405" font-size="20">Galactic longitude l</text><text x="18" y="78" font-size="18">vLSR</text><text x="423" y="84" font-size="18">tangent velocity</text></svg>',
        14: '<svg viewBox="0 0 900 440" role="img" aria-label="Survey analysis flow from calibrated observation through mask and completeness to population inference"><path d="M125 155L265 90L405 155L545 90L685 155L790 115" fill="none" stroke="#087e8b" stroke-width="6"/><circle cx="125" cy="155" r="30" fill="#17324d"/><rect x="230" y="65" width="70" height="50" fill="#b66a0a"/><polygon points="405,118 438,155 405,192 372,155" fill="#a33a3a"/><rect x="510" y="65" width="70" height="50" fill="#087e8b"/><circle cx="685" cy="155" r="32" fill="#b66a0a"/><path d="M125 205V315H685V205" fill="none" stroke="#596875" stroke-width="4" stroke-dasharray="10 8"/><text x="87" y="225" font-size="17">data</text><text x="222" y="145" font-size="17">cal</text><text x="376" y="225" font-size="17">mask</text><text x="510" y="145" font-size="17">selection</text><text x="638" y="225" font-size="17">inference</text><text x="263" y="355" font-size="19">provenance + reproducibility audit</text></svg>',
    }
    return figures[number]

def figure_html(number: int, caption: str) -> str:
    return f'<figure class="figure">{svg(number)}<figcaption>{html.escape(caption)}</figcaption></figure>'

def lecture_pages(number: int, item: dict) -> tuple[str, str]:
    res = result_text(number)
    objectives = "".join(f"<li>{html.escape(text)}</li>" for text in item["objectives"])
    evidence = "".join(f"<li>{html.escape(text)}</li>" for text in item["evidence"])
    title = item["title"]
    slides = [
        f'<section class="slide title"><p class="kicker">ASTR 472 · Lecture {number:02d}</p><h1>Lecture {number:02d}: {html.escape(title)}</h1><h2>Radio Astronomy</h2><p>{html.escape(item["hook"])}</p></section>',
        f'<section class="slide"><h2>Objectives and route</h2><ol>{objectives}</ol><p>Route: identify what the receiver measures, derive the physical/instrument relation, calculate a scale, then test its assumptions against a diagnostic.</p></section>',
        f'<section class="slide"><h2>Observation before interpretation</h2><p>{html.escape(item["hook"])}</p><ul>{evidence}</ul><p>Keep four layers distinct in your notebook: raw correlation or spectrum, calibrated product, model parameter, and physical claim.</p></section>',
        f'<section class="slide"><h2>Physical model</h2><p>{html.escape(item["derivation"])}</p><div class="equation">\\({item["equation"]}\\)</div><p>Define each quantity and convention before substitution. A relation is useful only inside its stated regime.</p></section>',
        f'<section class="slide"><h2>Worked calculation</h2><p>Inputs: {html.escape(str(calc(number)["inputs"]))}.</p><div class="equation">{html.escape(res)}</div><p>{html.escape(item["limit"])}</p><p>Independent audit: carry SI units through the derivation, then check the limiting direction and scale.</p></section>',
        f'<section class="slide"><h2>Read the geometry or data relation</h2>{figure_html(item["figure"], item["evidence"][0])}<p>Identify what is directly encoded in the figure and which inference requires an instrument model or physical assumption.</p></section>',
        f'<section class="slide"><h2>Where the inference can fail</h2><p>{html.escape(item["limit"])}</p><ul><li>Check the frequency, velocity frame, beam definition, and calibration convention before comparing values.</li><li>Use residuals and alternate models to distinguish a weak signal from a plausible but non-unique interpretation.</li><li>Report thermal noise separately from calibration, selection, and model uncertainty.</li></ul></section>',
        f'<section class="slide"><h2>Reasoning prompt</h2><div class="prompt">{html.escape(item["prompt"])}</div><p>Write the predicted scaling first; then identify which measurement would falsify it.</p></section>',
        f'<section class="slide"><h2>Connection to the observing workflow</h2><p>This lecture feeds into the paired lab: {html.escape(LABS[(number-1)//2]["title"])}. Preserve the raw-to-calibrated-to-inferred chain and carry the same units and assumptions into the analysis.</p><p>For a real observation, archive the project identifier, correlator setup, antenna configuration, calibration version, flags, beam, and data-release citation.</p></section>',
        f'<section class="slide"><h2>Synthesis</h2><p>{html.escape(item["title"])} is one stage in a measurement chain: celestial signal → antenna and receiver → sampled data → calibration → image/spectrum → uncertainty-aware inference.</p><p>Next: connect this result to {html.escape(LECTURES[number]["title"] if number < 14 else "the course synthesis and survey-analysis workflow")}.</p></section>',
        f'<section class="slide"><h2>References and scope</h2><p>{html.escape(item["reading"])}</p><p>Primary/authoritative material and provenance levels are recorded in <code>../reference-log.md</code>. Numeric examples are reproducibly calculated by <code>../src/generate_astr472_package.py</code>; figure geometry is original and lecture-specific.</p></section>',
    ]
    notes = f"""<header><div><h1>ASTR 472 Lecture {number:02d}: {html.escape(title)}</h1><p>Radio Astronomy · study notes · 400-level elective</p></div></header><main>
<section><h2>Learning objectives</h2><ol>{objectives}</ol><p><strong>Prerequisites in use:</strong> ASTR 340; PHYS 341 electromagnetism is recommended for receiver and radiation physics.</p></section>
<section><h2>Conceptual entry point</h2><p>{html.escape(item['hook'])} Begin with the receiver product: a spectrum, time series, image, or set of complex visibilities. The object we ultimately discuss is several inference steps removed from that product.</p><p>Radio astronomy's history makes this distinction concrete. Karl Jansky's 1930s rotating antenna detected persistent celestial interference while he investigated radio communication noise; Grote Reber then built a purpose-designed reflector and mapped the radio sky. Instrumental curiosity became a new window on the Galaxy.</p>{figure_html(item['figure'], item['evidence'][0])}</section>
<section><h2>Evidence and measurement layers</h2><ul>{evidence}</ul><p>A calibrated brightness scale is not equivalent to a flux measurement, and a catalog parameter is not equivalent to a direct observable. State the processing stage whenever comparing results.</p></section>
<section><h2>Derivation and assumptions</h2><p>{html.escape(item['derivation'])}</p><div class="equation">\\({item['equation']}\\)</div><p>The approximation is useful because it compresses a full electromagnetic/instrument problem into a scale relation. It is not a substitute for the response model: explicitly retain the beam, bandpass, convention, sampling, or plasma assumptions relevant to this lecture.</p></section>
<section><h2>Worked example</h2><p><strong>Inputs:</strong> {html.escape(str(calc(number)['inputs']))}.</p><p><strong>Programmatically evaluated result:</strong> {html.escape(res)}.</p><p>{html.escape(item['limit'])} Recompute independently from the equation before using the result to compare facilities or source models.</p></section>
<section><h2>Observational interpretation</h2><p>{html.escape(item['evidence'][1])} A defensible interpretation records the competing hypotheses, checks whether the instrument response can mimic the feature, and identifies a measurement that would separate the alternatives. The next layer of evidence should be chosen for discriminating power, not simply because it is available.</p></section>
<section><h2>Common conceptual traps</h2><ul><li>Confusing total flux with flux per beam, or a brightness temperature with a thermodynamic temperature.</li><li>Assuming a narrow thermal-noise estimate includes flux-scale or selection uncertainty.</li><li>Treating spatial resolution, field of view, and largest recoverable scale as interchangeable.</li><li>Using a Doppler or calibration convention without recording its reference frame.</li></ul><p>Lecture-specific limitation: {html.escape(item['limit'])}</p></section>
<section><h2>Study and transfer questions</h2><ol><li>{html.escape(item['prompt'])}</li><li>Change the dominant input by 10%. Predict the direction of the output change before computing it.</li><li>Name one raw diagnostic and one independent data product that could falsify the preferred interpretation.</li></ol></section>
<section><h2>Reading</h2><p>{html.escape(item['reading'])}</p><p>See <code>materials/ASTR472/reference-log.md</code> for sources, verification dates, exact OpenStax anchors, and human spot-check caveats.</p></section>
</main>"""
    slide_css = CSS + ".slide{padding-top:30px;padding-bottom:30px}.slide .figure svg{max-height:42vh}.slide .figure{margin:5px 0}.slide .figure figcaption{font-size:.82rem}.slide h2{font-size:1.8rem}"
    return page(f"ASTR 472 Lecture {number:02d} Slides: {title}", '<main class="deck">'+"".join(slides)+"</main>", slide_css), page(f"ASTR 472 Lecture {number:02d} Notes: {title}", notes)

def lab_page(number: int, item: dict) -> str:
    sample_num = number * 2
    sample = result_text(sample_num)
    steps = "".join(f"<li>{html.escape(step)}</li>" for step in item["steps"])
    return page(f"ASTR 472 Lab {number:02d}: {item['title']}", f"""<header><div><h1>ASTR 472 Lab {number:02d}: {html.escape(item['title'])}</h1><p>{html.escape(item['focus'])}</p></div></header><main>
<section><h2>Learning objectives</h2><ul><li>{html.escape(item['objective'])}.</li><li>Propagate a statistical or calibration uncertainty and report a limitation.</li><li>Preserve a reproducible record of inputs, transformations, and outputs.</li></ul></section>
<section><h2>Preparation, materials, and setup</h2><p>Use Python 3 with the standard library (or a spreadsheet capable of regression and plotting), the supplied <code>../data/{html.escape(item['dataset'])}</code>, and the relevant lecture notes. Record file name, row count, columns, units, and provenance level before editing. No facility observing time is assumed.</p><p>Dataset status: the supplied compact record is synthetic/instructor-provided (level 3), not an archived observation. Compare its analysis workflow with the real survey or observatory source cited in <code>../reference-log.md</code>.</p><p><strong>Computed check:</strong> {html.escape(sample)}.</p></section>
<section><h2>Apparatus and procedure</h2><ol>{steps}</ol></section>
<section><h2>Measurement record and uncertainty</h2><table><thead><tr><th>Record</th><th>Required entry</th></tr></thead><tbody><tr><td>Input</td><td>File, release/source, units, masks or flags, and provenance level.</td></tr><tr><td>Model</td><td>Equation, parameter values, convention, and approximation.</td></tr><tr><td>Statistics</td><td>Fit covariance or counting error plus one calibration/selection/systematic term.</td></tr><tr><td>Validation</td><td>Independent recomputation, residual plot, and limiting-case check.</td></tr></tbody></table><p>{html.escape(item['measurement'])}</p></section>
<section><h2>Deliverables and criteria</h2><ul><li>Reproducible code or spreadsheet with inputs and units documented.</li><li>One publication-quality labeled plot and a short interpretation (400-700 words).</li><li>Uncertainty budget that separates random, common-mode, and model terms where relevant.</li><li>Credit requires correct method, units, interpretation, provenance, and a limitation; a copied numeric result without an audit trail earns at most half credit.</li></ul></section>
<section><h2>Interpretive boundary</h2><p>{html.escape(item['answer'])} State explicitly which parts of your result are facts about this prepared teaching record and which are transferable inference methods.</p></section>
<section><h2>References and provenance</h2><p>Course teaching record: <code>../data/{html.escape(item['dataset'])}</code>, level 3. Real facility/survey context: <a href="../reference-log.md">reference log</a>. No external image is used.</p></section></main>""")

PSET_CONTENT = [
    {"title":"Emission Physics, Antenna Pattern, and Sensitivity","reading":"OpenStax Astronomy 2e Chapter 6 Review Question 15 (interferometric resolution) and Chapter 5 Review Question 31 (frequency/wavelength relation); see reference-log for extraction verification.","problems":[("Synchrotron scaling","For B=10 microgauss and gamma=10^4, calculate the characteristic frequency. Then increase B by 4 at fixed frequency and derive the required new gamma. State why a spectral peak need not equal this frequency."),("Dish design","At 1.4 GHz, compare the approximate FWHM and effective collecting area for 25-m and 50-m dishes with eta_a=0.70. State how the resolution and area ratios differ."),("Sensitivity design","Using SEFD=300 Jy, two polarizations, and eta_s=1, find the integration time needed for 1 mJy rms in a 1-MHz channel. Identify one reason an actual observation may take longer.")],"answers":[lambda:result_text(1),lambda:result_text(2),lambda:result_text(3)]},
    {"title":"Radiometer Equation, Beams, and Brightness Temperature","reading":"OpenStax Astronomy 2e §6.4; Chapter 6 Review Questions 2 and 15 support telescope-window and resolution context. Text does not derive radiometer or brightness-temperature equations.","problems":[("Noise scaling","Starting from independent time-frequency samples, derive sigma_S proportional to (n_pol Delta-nu tau)^-1/2. Compute the rms for the shared 300-Jy SEFD example."),("Brightness temperature","For 1 Jy/beam at 1.4 GHz in a circular 45-arcsec Gaussian beam, compute T_b in kelvin. Repeat for 90 arcsec and explain why integrated flux is not the same quantity."),("Thermal versus systematic floor","An observing program reaches 2.0 mJy after one hour. Predict the ideal rms after four hours and after sixteen hours; then combine a 1.5-mJy calibration floor in quadrature with the sixteen-hour thermal term.")],"answers":[lambda:result_text(3),lambda:result_text(4),lambda:f"ideal 16-hour thermal rms = {fmt(float(calc(3)['value'])/4)} mJy; total with 1.5-mJy floor = {fmt(math.hypot(float(calc(3)['value'])/4,1.5))} mJy"]},
    {"title":"Visibilities, Fourier Synthesis, and Missing Scales","reading":"OpenStax Astronomy 2e §6.4 and Chapter 6 Review Question 15; ALMA Basics §Interferometry gives the visibility-function definition.","problems":[("Visibility phase","For a point source 10 arcsec east of phase center on a 3-km projected baseline at 1.4 GHz, compute fringe phase in cycles and degrees modulo 360. Explain the sign convention."),("Resolution versus scale","At 100 GHz with Bmax=16 km and Bmin=15 m, estimate synthesized resolution 1.02 lambda/Bmax and largest recoverable scale 0.6 lambda/Bmin. Convert both to arcseconds and identify what each baseline extreme controls."),("Inverse problem","A compact array image has a 40-arcsec beam but a 6-arcminute cloud is mostly absent. Explain why increasing deconvolution iterations cannot reconstruct unconstrained low spatial frequencies. Propose the observing component that supplies those data.")],"answers":[lambda:result_text(5),lambda:result_text(6),lambda:"Single-dish total-power or suitably compact-array measurements add zero/short spacings; CLEAN iterations alone do not create measured low-u,v constraints."]},
    {"title":"Complex-Gain Calibration and Error Budgets","reading":"NRAO VLA calibration documentation and ALMA data-processing documentation; OpenStax §6.4 is introductory and contains no calibration equation.","problems":[("Gain measurement equation","For Vpq_obs=g_p g_q* Vpq_true+n, let g_p=1.05 exp(i 8 deg), g_q=0.95 exp(-i 4 deg), and Vtrue=100 mJy real. Compute observed amplitude and phase ignoring noise, then solve back for Vtrue."),("Phase decorrelation","For Gaussian phase residual rms=10 deg, calculate coherence. Repeat at 20 deg and compare the two losses; explain why loss is not linear in rms phase."),("Correlated uncertainty","A 120-mJy source has independent thermal 5%, gain 3%, and flux-scale 2% terms. Compute total uncertainty. If another source shares the flux-scale solution, explain which part cancels in the ratio.")],"answers":[lambda:"Observed amplitude = 1.05 x 0.95 x 100 = 99.75 mJy; phase = 8 - (-4) = 12 deg; division by the gain product recovers 100 mJy.",lambda:result_text(7),lambda:result_text(8)]},
    {"title":"Spectral Lines, H I Columns, and Velocity Structure","reading":"OpenStax Astronomy 2e §5.6 and §20.2; Chapter 6 Review Question 23 discusses long-wavelength emission. Exact text anchors are cross-checked in the local extraction.","problems":[("Radio velocity","For a line at 1420.40575177 MHz measured 0.500 MHz lower, compute v_radio and the velocity width of a 10-kHz channel. State the validity regime."),("H I column","For integrated brightness 120 K x 8 km/s, compute optically thin N_HI. If the optical depth is not small, state the direction of bias and what additional measurement is needed."),("Line inference audit","A Gaussian line has peak 80 K and FWHM 12 km/s. Derive its integrated area using the Gaussian area factor 1.0645 and calculate thin N_HI. Compare with a rectangular approximation peak x FWHM and quantify the fractional approximation gap.")],"answers":[lambda:result_text(9),lambda:result_text(10),lambda:f"Gaussian integral={fmt(80*12*1.0645)} K km/s; N_HI={fmt(1.823e18*80*12*1.0645)} cm^-2; rectangle overestimates relative to Gaussian by {fmt((80*12-80*12*1.0645)/(80*12*1.0645)*100)}%."]},
    {"title":"Pulsar Dispersion, Timing, and Survey Selection","reading":"OpenStax Astronomy 2e §23.4; ATNF Pulsar Catalogue fields include P0, P1, DM, S400, and S1400. Live catalogue page and provenance are logged.","problems":[("Cold-plasma delay","For DM=56.8 pc cm^-3, compute delay between 400 and 1400 MHz. If DM uncertainty is 0.2 pc cm^-3, propagate its contribution to delay uncertainty."),("Timing and channel smearing","A 400-MHz observation uses 0.1-MHz channels and DM=56.8. Estimate intra-channel dispersive smearing from the derivative of the delay law. Compare with a 2-ms pulse width and state the detectability consequence."),("Completeness estimate","For 84 recovered injections out of 100, compute completeness and binomial standard error. Explain why this does not include sky-position or pulse-width model uncertainty.")],"answers":[lambda:result_text(11),lambda:f"Delta t_channel approx 8.3 microseconds x DM x Delta-nu_MHz / nu_GHz^3 = {fmt(8.3e-3*56.8*0.1/0.4**3)} ms; this is a substantial fraction of 2 ms.",lambda:result_text(12)]},
    {"title":"Survey Completeness, H I Kinematics, and Reproducibility","reading":"OpenStax Astronomy 2e §20.2 and §6.4; HI4PI Collaboration 2016 and NVSS (Condon et al. 1998) are named survey sources, with verification status recorded in reference-log.","problems":[("Inner-Galaxy kinematics","At l=30 deg, v_LSR=100 km/s, R0=8.2 kpc, and Theta0=236 km/s, compute R under a flat circular rotation curve. Explain why this is not a unique heliocentric distance."),("Completeness-corrected density","For 1200 detections over 20 deg2 at completeness 0.84, compute corrected surface density and Poisson-only uncertainty. Then include a completeness uncertainty of 0.03 by first-order propagation."),("Comparative survey claim","Survey A has 40-arcsec resolution and 0.5-mJy rms; survey B has 5-arcsec resolution and 1.2-mJy rms. For a 6-arcminute diffuse source, compare which survey is more likely to recover integrated emission and which better separates point sources. State why rms alone is insufficient.")],"answers":[lambda:result_text(13),lambda:result_text(14),lambda:"Survey A is more likely to retain diffuse structure because it is less resolving out the broad source; survey B has finer angular separation but its higher point-source rms may reduce sensitivity. Primary beam, short spacings, surface-brightness sensitivity, and calibration also matter."]},
]

PSET_READINGS = {
    1: "OpenStax Astronomy 2e Chapter 5 Figuring for Yourself 41 (radio wavelength from broadcast frequency) and Chapter 6 Review Question 15 (interferometric resolution).",
    2: "OpenStax Astronomy 2e §6.4 and Chapter 6 Review Questions 2 and 15. These provide telescope-window and interferometer context, not radiometer or brightness-temperature derivations.",
    3: "OpenStax Astronomy 2e §6.4 and Chapter 6 Review Question 15; ALMA Basics §Interferometry defines the visibility transform and baseline coordinates.",
    4: "NRAO VLA calibration documentation and ALMA data-processing documentation; OpenStax Astronomy 2e Chapter 6 Review Questions 1 and 11 provide instrument-chain and radio/radar context.",
    5: "OpenStax Astronomy 2e §§5.6 and 20.2, Chapter 20 Review Question 5, and Chapter 6 Thought Question 23 (the local exercise index identifies this as a Thought Question, not a Review Question). HI4PI Collaboration (2016), Table 1 and §3.1, provides the real survey response and optically-thin column relation.",
    6: "OpenStax Astronomy 2e §23.4 and Chapter 23 Figuring for Yourself 42-43 (pulsar rotation speed) and 53 (pulse count); ATNF Pulsar Catalogue definitions include P0, P1, and DM.",
    7: "OpenStax Astronomy 2e §20.2, Chapter 20 Review Question 5, and Thought Questions 25; HI4PI Collaboration (2016), DOI 10.1051/0004-6361/201629178, and Condon et al. (1998), DOI 10.1086/300337.",
}

def worked_solution(set_number: int, problem_number: int) -> str:
    if set_number == 1 and problem_number == 1:
        frequency = float(calc(1)["value"])
        return f"nu_c=4.2e6 B_G gamma^2={fmt(frequency)} Hz. Holding nu_c fixed while multiplying B by 4 requires gamma_new=gamma/sqrt(4)={fmt(1e4 / math.sqrt(4))}. The synchrotron kernel is broad, so a spectral peak need not equal nu_c."
    if set_number == 1 and problem_number == 2:
        beam_25 = float(calc(2)["value"])
        area_25 = float(calc(2)["area"])
        return f"At 1.4 GHz the 25-m dish gives {fmt(beam_25)} arcmin and A_eff={fmt(area_25)} m^2. Doubling D halves beam FWHM to {fmt(beam_25 / 2)} arcmin and multiplies area by four to {fmt(area_25 * 4)} m^2."
    if set_number == 1 and problem_number == 3:
        seconds = (300 / 0.001) ** 2 / (2 * 1e6)
        return f"From sigma=SEFD/sqrt(n_pol Delta-nu tau), tau=(300/0.001)^2/(2 x 1e6)={fmt(seconds)} s={fmt(seconds / 3600)} h. Flagging, efficiency losses, and calibration overhead make the real time longer."
    if set_number == 2 and problem_number == 1:
        return f"There are n_pol Delta-nu tau independent samples, so their rms falls as the inverse square root: sigma_S=SEFD/sqrt(n_pol Delta-nu tau). Substitution gives {result_text(3)}."
    if set_number == 2 and problem_number == 2:
        temperature = float(calc(4)["value"])
        return f"Omega_b=pi theta^2/(4 ln 2) and T_b=lambda^2 S/(2 k Omega_b). At 45 arcsec, T_b={fmt(temperature)} K. Doubling both beam axes multiplies Omega_b by 4, so T_b={fmt(temperature / 4)} K for the same 1 Jy/beam."
    if set_number == 2 and problem_number == 3:
        return f"Thermal rms scales as tau^-1/2: 2.0/sqrt(4)=1.0 mJy at 4 h and 2.0/sqrt(16)=0.50 mJy at 16 h. Quadrature with 1.5 mJy gives sqrt(0.50^2+1.5^2)={fmt(math.hypot(0.5, 1.5))} mJy."
    if set_number == 3 and problem_number == 1:
        phase = float(calc(5)["phase"])
        cycles = phase / 360
        return f"lambda=c/nu; theta=10/206264.806 rad; cycles=-B theta/lambda={cycles:.6f}. Thus phase={fmt(phase)} deg, equivalent to {fmt(phase % 360)} deg modulo 360 under V=integral I exp(-2 pi i u l) dl."
    if set_number == 3 and problem_number == 2:
        return f"Using lambda=c/nu, 1.02 lambda/Bmax={fmt(float(calc(6)['value']))} arcsec, while 0.6 lambda/Bmin={fmt(float(calc(6)['max_scale']))} arcsec. The former is a fine-scale beam estimate; the latter is a broad-structure recovery limit."
    if set_number == 3 and problem_number == 3:
        return "The finite uv mask removes low spatial frequencies, so the dirty image loses broad flux. Deconvolution cannot determine unmeasured modes from the data alone; single-dish total power or shorter interferometer baselines add the missing constraints."
    if set_number == 4 and problem_number == 1:
        return "The baseline gain product is (1.05 x 0.95) exp[i(8-(-4)) deg]. Therefore |Vobs|=99.75 mJy and arg(Vobs)=12 deg; dividing by both antenna gains recovers Vtrue=100 mJy."
    if set_number == 4 and problem_number == 2:
        return f"For Gaussian phase scatter, coherence=exp(-sigma_phi^2/2). It is {fmt(float(calc(7)['value']))} at 10 deg and {fmt(math.exp(-math.radians(20)**2 / 2))} at 20 deg; phase variance, not rms phase linearly, enters the exponential."
    if set_number == 4 and problem_number == 3:
        return f"Fractional uncertainty=sqrt(0.05^2+0.03^2+0.02^2)={fmt(float(calc(8)['fraction']))}; sigma_S={fmt(float(calc(8)['value']))} mJy. A shared multiplicative flux-scale term cancels to first order in a source ratio; independent thermal errors remain."
    if set_number == 5 and problem_number == 1:
        return f"v_radio=c Delta-nu/nu_0={fmt(float(calc(9)['value']))} km/s. A 10-kHz channel spans {fmt(float(calc(9)['channel']))} km/s. This first-order convention is suitable for Galactic speeds and must be tied to a stated reference frame."
    if set_number == 5 and problem_number == 2:
        return f"The integral is 120 x 8=960 K km/s, giving N_HI=1.823e18 x 960={fmt(float(calc(10)['value']))} cm^-2. For appreciable opacity, the thin estimate is a lower limit; absorption spectra can constrain optical depth."
    if set_number == 5 and problem_number == 3:
        gaussian_area = 80 * 12 * 1.0645
        rectangular_area = 80 * 12
        return f"The Gaussian integral is 1.0645 x 80 x 12={fmt(gaussian_area)} K km/s; N_HI={fmt(1.823e18 * gaussian_area)} cm^-2. The rectangular estimate is {fmt((1 - rectangular_area / gaussian_area) * 100)}% lower, not higher, than the Gaussian integral."
    if set_number == 6 and problem_number == 1:
        delay = float(calc(11)["value"])
        return f"Delta_t=4.148808 DM(0.4^-2-1.4^-2)={fmt(delay)} ms. Since delay is linear in DM, sigma_t=delay(0.2/56.8)={fmt(delay * 0.2 / 56.8)} ms."
    if set_number == 6 and problem_number == 2:
        smear = 8.3e-3 * 56.8 * 0.1 / 0.4**3
        return f"Using |dt/dnu| Delta-nu, intra-channel smearing is 8.3 microseconds x DM x Delta-nu_MHz/nu_GHz^3={fmt(smear)} ms. It is a substantial fraction of 2 ms and lowers pulse peak S/N."
    if set_number == 6 and problem_number == 3:
        return f"p_hat=84/100={fmt(float(calc(12)['value']))}; sigma_p=sqrt[p(1-p)/N]={fmt(float(calc(12)['uncertainty']))}. This binomial error omits sky-dependent sensitivity and injection-model mismatch."
    if set_number == 7 and problem_number == 1:
        return f"For flat circular rotation, R=R0/[1+v/(Theta0 sin l)]={fmt(float(calc(13)['value']))} kpc. This is a model-based Galactocentric radius, not a unique heliocentric distance; near/far geometry and non-circular motion remain."
    if set_number == 7 and problem_number == 2:
        poisson = float(calc(14)["uncertainty"])
        completeness_term = 1200 * 0.03 / (20 * 0.84**2)
        total = math.hypot(poisson, completeness_term)
        return f"Sigma=1200/(20 x 0.84)={fmt(float(calc(14)['value']))} deg^-2; Poisson-only sigma={fmt(poisson)} deg^-2. Completeness contributes N sigma_C/(A C^2)={fmt(completeness_term)} deg^-2, so total first-order sigma={fmt(total)} deg^-2."
    if set_number == 7 and problem_number == 3:
        return "Survey A is more likely to retain diffuse structure because its beam is less likely to resolve out a 6-arcminute cloud; B separates closer point sources better but has higher point-source rms. Short spacings, surface-brightness sensitivity, primary beam, and calibration matter in addition to rms."
    raise ValueError(f"No worked solution for problem set {set_number}, problem {problem_number}")

def pset_pages(number: int, item: dict) -> tuple[str, str, str]:
    n = number
    title = item["title"]
    problem_html = []
    solution_html = []
    for index, (heading, question) in enumerate(item["problems"]):
        answer = worked_solution(n, index + 1)
        problem_html.append(f'<article class="problem"><h3>Problem {index+1}: {html.escape(heading)} <span class="small">(30 points)</span></h3><p>{html.escape(question)}</p><p><strong>Required:</strong> derivation, units, intermediate values, uncertainty/assumption, and an interpretation that identifies what the result does not prove.</p></article>')
        solution_html.append(f'<article class="problem"><h3>Problem {index+1}: {html.escape(heading)}</h3><p><strong>Worked solution:</strong> {html.escape(answer)}</p><p>Show the governing equation, substitute with consistent units, retain intermediate values, and state which approximation limits the inference. Accept equivalent algebra and convention choices when explicitly stated.</p><p><strong>Points:</strong> model and derivation 12; units and numerical work 10; uncertainty/limitation 4; interpretation 4.</p></article>')
    student = f"""<header><div><h1>ASTR 472 Problem Set {n:02d}: {html.escape(title)}</h1><p>Student assignment · due date set by instructor</p></div></header><main><section><h2>Objectives and instructions</h2><p>Submit complete derivations, units, assumptions, and a short physical interpretation. Include reproducible code for multi-step calculations and show intermediate values. Cite any external catalog or data product with its release/version. Collaboration on methods is allowed; submitted derivations and prose must be your own. Corrections and resubmissions with a change log are encouraged.</p></section><section><h2>Problems</h2>{''.join(problem_html)}</section><section><h2>Reading and data</h2><p>{html.escape(item['reading'])}</p><p>The numbered anchors were checked against the local OpenStax Astronomy 2e extraction; exercise numbers/page breaks can vary by edition. Before assigning through an LMS, the instructor should spot-check each recommendation against the adopted print/PDF edition. Exact source scope and extraction notes are in <code>../reference-log.md</code>. Do not present the synthetic teaching records as telescope observations.</p></section><section><h2>Deliverables and scoring</h2><p>Three problems, 100 points total. Submit a PDF or HTML report plus code/notebook where requested. Show figures with axes, units, captions, and data provenance.</p></section></main>"""
    student = student.replace(html.escape(item["reading"]), html.escape(PSET_READINGS[n]))
    solutions = f"""<header><div><h1>ASTR 472 Problem Set {n:02d}: Solution Key</h1><p>{html.escape(title)} · instructor use</p></div></header><main><section><h2>Scoring rubric</h2><p>Each problem is worth 30 points; presentation/reproducibility contributes 10 points across the set. Award credit for correct setup and units before the final number. Identify arithmetic slips separately from conceptual errors. Require correct comparative direction and an honest account of approximation gaps.</p></section>{''.join(solution_html)}<section><h2>Common errors</h2><ul><li>Converting MHz/GHz or arcseconds/radians incorrectly.</li><li>Confusing per-beam flux with integrated flux or brightness temperature with kinetic temperature.</li><li>Treating flux-scale uncertainty as independent for every source.</li><li>Using a linear Doppler approximation outside its regime or silently changing velocity convention.</li><li>Calling a synthetic record an observation or reporting a completeness correction without its selection assumptions.</li></ul></section></main>"""
    assessment = f"""# ASTR 472 Problem Set {n:02d} Assessment Instructions

Inspect the submission, this problem set, solution key, the associated lecture slides/notes, cited catalog/data product, and any submitted code.

## Standard
Grade at a senior undergraduate level. Require the physical model, unit-consistent derivation, correct frame/convention, a numerical result consistent with the shown work, and interpretation. Reward a correct method with a minor arithmetic slip more than an unexplained correct-looking answer.

## Problem-specific checks
- Problem 1 ({item['problems'][0][0]}): verify the governing relation, units, and stated validity domain.
- Problem 2 ({item['problems'][1][0]}): recompute the central value and uncertainty independently; check comparison direction.
- Problem 3 ({item['problems'][2][0]}): require the requested alternative-model, uncertainty, or synthesis discussion, not a generic paragraph.

## Evidence and reproducibility
Check citations, dataset release/version, units, masks, code inputs, random seed where relevant, and figure axes. Flag claims that conflate a teaching record, catalog measurement, calibrated product, and physical inference.

## Feedback and resubmission
Separate arithmetic, unit conversion, conceptual model, uncertainty, provenance, and communication errors. Give actionable feedback without replacing the student's reasoning. One revised submission with a change log is encouraged; preserve the original high standard and follow the instructor's grading policy.
"""
    return page(f"ASTR 472 Problem Set {n:02d}", student), page(f"ASTR 472 Problem Set {n:02d} Solutions", solutions), assessment

def datasets() -> None:
    hi_peak_kelvin = 960.0 / (8.0 * 1.0645)
    hi_velocity_kms = [-16, -12, -8, -4, 0, 4, 8, 12, 16]
    hi_records = []
    for velocity in hi_velocity_kms:
        frequency_mhz = F_HI * (1 - velocity * 1000 / C) / 1e6
        brightness = 4 + hi_peak_kelvin * math.exp(-4 * math.log(2) * (velocity / 8.0) ** 2)
        hi_records.append([frequency_mhz, brightness])
    pulsar_records = []
    for frequency_ghz, timing_residual in zip([0.4, 0.6, 0.8, 1.0, 1.4], [0.2, -0.3, 0.1, -0.1, 0.0]):
        delay_ms = 4.148808 * 56.8 * (frequency_ghz**-2 - 1.4**-2)
        pulsar_records.append([frequency_ghz, delay_ms + timing_residual, 0.5])
    rows = {
        "continuum_spectrum.csv": (["frequency_GHz","flux_Jy","sigma_Jy"], [[0.4,2.31,0.10],[0.6,1.72,0.08],[1.0,1.03,0.05],[1.4,0.75,0.04],[3.0,0.41,0.03],[5.0,0.29,0.03]]),
        "radiometer_trials.csv": (["bandwidth_Hz","integration_s","predicted_rms_mJy","measured_rms_mJy"], [[1000000,900,7.071,7.8],[1000000,3600,3.536,4.0],[250000,3600,7.071,7.9],[1000000,14400,1.768,2.8]]),
        "uv_samples.csv": (["u_lambda","v_lambda","frequency_GHz","l_arcsec","m_arcsec","source_flux_Jy"], [[12000,0,1.4,10,0,0.25],[0,12000,1.4,10,0,0.25],[-12000,0,1.4,10,0,0.25],[0,-12000,1.4,10,0,0.25],[24000,6000,1.4,10,0,0.25],[-24000,-6000,1.4,10,0,0.25]]),
        "calibration_records.csv": (["scan","role","amplitude_ratio","phase_residual_deg","sigma_mJy"], [[1,"calibrator",1.04,7.0,2.0],[2,"calibrator",0.98,11.0,2.0],[3,"calibrator",1.02,9.0,2.0],[4,"calibrator",1.55,48.0,2.0],[5,"target",0.97,8.0,4.0],[6,"target",1.01,12.0,4.0]]),
        "hi_spectrum_teaching.csv": (["frequency_MHz","brightness_K"], hi_records),
        "pulsar_arrivals.csv": (["frequency_GHz","arrival_offset_ms","sigma_ms"], pulsar_records),
        "survey_injections.csv": (["tile","flux_mJy","injected","recovered","usable_area_deg2"], [["A",0.5,100,42,10],["A",1.0,100,84,10],["A",2.0,100,96,10],["B",0.5,100,31,10],["B",1.0,100,78,10],["B",2.0,100,93,10]]),
        "hi_kinematics_teaching.csv": (["longitude_deg","v_lsr_km_s","sigma_v_km_s"], [[30,100,5],[45,80,5],[60,45,5]]),
        "radio_facility_reference.csv": (["facility_or_survey","published_parameter","value","unit","provenance_level"], [["VLA","antennas",27,"count","1-live-verified OpenStax section 6.4; modern facility identity NRAO page"],["ALMA","maximum_baseline",16,"km","1-live-verified ALMA Basics"],["ALMA","frequency_range_approx", "35-950","GHz","1-live-verified ALMA Basics"],["HI4PI","beam_FWHM",16.2,"arcmin","1-live-verified arXiv 1610.06175 and CDS J/A+A/594/A116"],["HI4PI","channel_separation",1.29,"km/s","1-live-verified arXiv 1610.06175 Table 1"],["HI4PI","spectral_resolution",1.49,"km/s","1-live-verified arXiv 1610.06175 Table 1"],["HI4PI","brightness_temperature_rms",43,"mK","1-live-verified arXiv 1610.06175 and CDS J/A+A/594/A116"]]),
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename, (header, records) in rows.items():
        with (DATA_DIR / filename).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(header)
            writer.writerows(records)

def syllabus() -> str:
    schedule_rows = []
    for number, item in enumerate(LECTURES, 1):
        activity = f"Lab {((number+1)//2):02d}; PS {((number+1)//2):02d} due" if number % 2 == 0 else "paired method development"
        schedule_rows.append(f"<tr><td>{number}</td><td>{html.escape(item['title'])}</td><td>{activity}</td><td>{html.escape(item['reading'])}</td></tr>")
    return page("ASTR 472 Radio Astronomy Syllabus", f"""<header><div><h1>ASTR 472: Radio Astronomy</h1><p>3 credits · Year 4 elective · ASTR 340 prerequisite · PHYS 341 recommended</p></div></header><main>
<section><h2>Course information</h2><p><strong>Catalog description:</strong> Covers radio emission mechanisms, antennas, receivers, interferometry, aperture synthesis, calibration, spectral line observations, pulsars, neutral hydrogen mapping, and radio survey analysis.</p><p><strong>Course role:</strong> advanced Year 4 observational/instrumentation elective. ASTR 340 is required; PHYS 341 is recommended preparation in electromagnetic fields and radiation.</p></section>
<section><h2>Learning outcomes</h2><ol><li>Derive and apply the radiometer equation, antenna beam/effective-area relations, brightness temperature, and visibility measurement equation.</li><li>Explain uv sampling, aperture synthesis, calibration solutions, and the origin of imaging systematics.</li><li>Design and interpret radio continuum, spectral-line, pulsar-timing, and survey analyses with explicit assumptions and propagated uncertainty.</li><li>Infer H I column and kinematic scales from calibrated 21-cm data while recognizing opacity, rotation-model, and selection limits.</li><li>Produce reproducible analysis records that distinguish observation, calibrated product, inference, and model.</li></ol></section>
<section><h2>Resources</h2><p>OpenStax Astronomy 2e sections 5.6, 6.4, 20.2, and 23.4 provide introductory anchors, not the advanced derivations. Primary practical references include NRAO VLA documentation, ALMA Basics/Technical Handbook, the ATNF Pulsar Catalogue, HI4PI survey publication/data pages, and CASA documentation. Exact references and provenance are in <a href="reference-log.md">reference-log.md</a>.</p><p>Python 3 with NumPy, SciPy, Matplotlib, and Astropy is recommended for larger archive products; supplied CSV activities can be completed with the standard library and spreadsheet software.</p></section>
<section><h2>Assessment</h2><table><thead><tr><th>Component</th><th>Weight</th><th>Evidence</th></tr></thead><tbody><tr><td>Seven laboratory investigations</td><td>35%</td><td>Reproducible analysis, uncertainty, and provenance.</td></tr><tr><td>Seven problem sets</td><td>35%</td><td>Derivations, quantitative reasoning, and interpretation.</td></tr><tr><td>Midterm observing-design memo</td><td>10%</td><td>Technical setup and calibration plan.</td></tr><tr><td>Survey-analysis project</td><td>15%</td><td>Reproducible end-to-end inference.</td></tr><tr><td>Participation and peer audit</td><td>5%</td><td>Constructive review and response to evidence.</td></tr></tbody></table><p><strong>Total:</strong> 100%.</p><div class="notice"><strong>Revision policy:</strong> Revisions are encouraged to improve mastery and grade. Revised work must include a change log and corrected reasoning; the instructor sets resubmission windows and final grade caps.</div></section>
<section><h2>Cadence rationale</h2><p>The course uses 14 lectures, seven labs, and seven problem sets. Each lab and problem set follows a two-lecture unit so students first establish the source/instrument model and then use it in a concrete analysis. The seven paired units progress from emission and receiving, through sensitivity/beam and interferometric imaging, to calibration, lines/H I, pulsars/survey selection, and Galactic/survey synthesis. The matched 14/7/7 count is intentional, not a missing weekly activity pattern.</p></section>
<section><h2>Lecture schedule</h2><table><thead><tr><th>Week</th><th>Lecture</th><th>Activity</th><th>Reading anchor</th></tr></thead><tbody>{''.join(schedule_rows)}</tbody></table></section>
<section><h2>Policies and assumptions</h2><p>Assumption: a 14-week semester with one lecture meeting per week and seven longer lab blocks scheduled after paired lectures. Local calendar dates, instructor name, safety rules, disability accommodations, late work, collaboration, and academic-integrity procedures must be finalized by the instructor of record. Students must preserve data licenses and citation requirements. Radio-frequency interference is a safety and data-integrity issue; no student transmits without explicit authorization and applicable spectrum compliance.</p></section>
</main>""")

def schedule() -> str:
    rows = []
    for number, item in enumerate(LECTURES, 1):
        lab = f"Lab {number//2:02d} and PS {number//2:02d}" if number % 2 == 0 else "Preparation; build model"
        rows.append(f"<tr><td>{number}</td><td>Lecture {number:02d}: {html.escape(item['title'])}</td><td>{lab}</td><td>{'Submit by end of paired unit' if number%2==0 else 'No new assessment due'}</td></tr>")
    return page("ASTR 472 Lecture and Lab Schedule", f"<header><div><h1>ASTR 472: Radio Astronomy Schedule</h1><p>Fourteen lectures · seven paired lab/problem-set units</p></div></header><main><table><thead><tr><th>Week</th><th>Lecture focus</th><th>Activity</th><th>Assessment timing</th></tr></thead><tbody>{''.join(rows)}</tbody></table><p>Each lab and problem set follows the second lecture in its thematic pair. That placement ensures students have the required instrument and physical context before quantitative analysis.</p></main>")

def reference_log() -> str:
    return """# ASTR 472 Reference Log

## Verified readings and sources

| Use | Source | Verification | Scope and caveat |
|---|---|---|---|
| Introductory radio-instrument context | OpenStax, *Astronomy 2e*, §6.4 “Radio Telescopes” and Chapter 6 Exercises; https://openstax.org/books/astronomy-2e/pages/6-4-radio-telescopes | **Level 1, live-verified 2026-09-25**, page fetched and cross-checked against local extracted text | Correct section 6.4; embedded figure captions 6.17–6.22 occur within the section, confirming no chapter-heading numbering offset. Chapter 6 Review Question 15 asks how radio astronomers obtain visible-like resolution; Review Question 23 asks about very-long/very-short-wavelength sources. The source is introductory, not a substitute for derivations here. |
| Textbook H I/pulsar/Doppler context | OpenStax, *Astronomy 2e*, §§5.6, 20.2, 23.4 | **Level 1** local extracted-text spot-check for section labels; §6.4 live page checked | Introductory coverage only. Exact page/figure anchors and adopted-edition exercise numbering require human PDF spot-check before LMS assignment. |
| Interferometry, ALMA frequency, beam, largest-scale, channels | ALMA Science Portal, “ALMA Basics,” https://almascience.nrao.edu/about-alma/alma-basics | **Level 1, live-verified 2026-09-25** | Page states visibility is the Fourier transform of sky brightness, current frequency range about 35-950 GHz, 12-m maximum baseline about 16 km, field of view set by primary beam, largest structure approximately 0.6 lambda/b_min, and channel/sensitivity details. Values can change by observing cycle; check current handbook for proposals. |
| VLA facility and public observing/archive tools | NSF National Radio Astronomy Observatory, Karl G. Jansky VLA, https://science.nrao.edu/facilities/vla | **Level 1, live-verified 2026-09-25** | The official page and linked Observational Status Summary, archive, and calibration resources were inspected. OpenStax §6.4 supplies the 27 x 25-m / 36-km historical textbook description; current setup details should come from the observing cycle's official documentation. |
| Pulsar parameter definitions and catalogue | ATNF Pulsar Catalogue, https://www.atnf.csiro.au/research/pulsar/psrcat/ ; Manchester et al. 2005, AJ 129, 1993, DOI: 10.1086/428488 | **Level 1, live-verified catalogue interface 2026-09-25** | Interface exposes P0, P1, DM, S400, S1400, and derived Age/BSurf/Edot fields. Individual object parameters are not downloaded into this package; query/version must be cited for student archive work. |
| All-sky H I survey and data products | HI4PI Collaboration, 2016, A&A 594, A116, DOI: 10.1051/0004-6361/201629178; https://arxiv.org/abs/1610.06175; CDS catalog J/A+A/594/A116, https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/594/A116 | **Level 1, live-verified 2026-09-25** | The arXiv HTML and CDS ReadMe/catalog were fetched. They identify full-sky FITS cubes, 20-by-20-degree subcubes, spectra and N_HI products; Table 1 reports 16.2 arcmin FWHM, 1.29 km/s channel separation, 1.49 km/s spectral resolution, and about 43 mK RMS. Do not conflate channel separation with spectral resolution. The survey's standard N_HI relation is explicitly optically thin. The separate Bonn portal and A&A publisher fetch returned 403, but the arXiv and CDS primary records were accessible. |
| Real survey and facility comparisons | NRAO archive and VLA Sky Survey (VLASS) pages; Condon et al. 1998, AJ 115, 1693, DOI: 10.1086/300337 (NVSS) | **Level 1 for official archive navigation; level 2 for literature survey specifications** | No raw radio archive files were present in the workspace during production. Students are directed to retrieve real products with release, project identifier, mask, and calibration provenance recorded; bundled compact CSVs are synthetic level-3 teaching records. |

## Tri-level data provenance

- **Level 1, live-verified this session:** the OpenStax section title/embedded figure sequence and exact exercise anchors; ALMA Basics statements listed above; official NRAO VLA page/navigation; ATNF catalogue field definitions; HI4PI paper metadata, Table 1 beam/channel/spectral/noise values, thin-column relation, and CDS product inventory.
- **Level 2, published/literature values not re-verified this session:** historical NVSS and standard object parameters quoted in literature. The Bonn HI4PI portal and A&A publisher page returned 403, but the same paper and product metadata were live-verified through arXiv and CDS. Human spot-check is still required before proposal-grade use of current specifications.
- **Level 3, synthetic/instructor-provided:** `data/continuum_spectrum.csv`, `radiometer_trials.csv`, `uv_samples.csv`, `calibration_records.csv`, `hi_spectrum_teaching.csv`, `pulsar_arrivals.csv`, and `survey_injections.csv`. These are generated teaching tables, not observational records. `radio_facility_reference.csv` keeps cited real specifications separate and marks their level.

## Computation and visual provenance

All worked results in the slides, notes, labs, and solution keys are calculated by `src/generate_astr472_package.py` from the shared constants and input records. No radio archive data were present locally. The supplied compact exercise tables are level-3 teaching data; Lab 07 additionally requires retrieving one actual HI4PI 20-degree subcube from the verified CDS release and comparing a real spectrum/column integral, with file-level provenance recorded by the student. The fourteen SVG figures are original and use different geometry and data relations; no external image is embedded, so no third-party visual license is implied.

## Human spot-check before instructional use

1. Spot-check the HI4PI 2016 beam/channel/spectral/noise values and the selected CDS FITS product metadata against the adopted release before instructional use; live verification used arXiv HTML and the CDS catalog/ReadMe, while the Bonn portal and publisher page were blocked (403).
2. Check current VLA/ALMA configuration and band/setup details against the relevant observing-cycle manuals before proposing live observations.
3. Spot-check OpenStax Chapter 6 Review Question numbering against the adopted edition PDF and confirm instructor-selected readings/exercises.
4. Query versioned pulsar catalogue values and NVSS/VLASS completeness/calibration documentation before adding catalog measurements to submitted coursework.
"""

def manifest() -> dict:
    return {"course":{"courseNumber":"ASTR 472","courseCode":"ASTR472","title":"Radio Astronomy","credits":3,"term":"Year 4 elective","yearInCurriculum":4,"prerequisites":"ASTR 340; PHYS 341 recommended","description":"Covers radio emission mechanisms, antennas, receivers, interferometry, aperture synthesis, calibration, spectral line observations, pulsars, neutral hydrogen mapping, and radio survey analysis."},"status":{"stage":"in review","reviewStatus":"Draft generated; independent review and correction required","lastUpdated":"2026-09-25"},"counts":{"slides":14,"notes":14,"labs":7,"problemSets":7,"solutionKeys":7,"assessmentInstructions":7},"cadence":{"lectures":14,"labs":7,"problemSets":7,"rationale":"Seven two-lecture units each build the physical/instrument model before the paired lab and problem set; cadence is documented in syllabus.html."},"dataProvenance":{"generator":"materials/ASTR472/src/generate_astr472_package.py","levels":{"level1":"OpenStax §6.4, ALMA Basics, NRAO VLA navigation, and ATNF catalogue interface live-verified 2026-09-25.","level2":"HI4PI and standard published parameters not live-verified; access attempt failures and spot-check requirement are disclosed.","level3":"Compact CSV exercise tables and all computed figures are synthetic/instructor-provided teaching records."}}}

def build() -> None:
    for directory in (LECTURE_DIR, LAB_DIR, PSET_DIR, DATA_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    datasets()
    for number, item in enumerate(LECTURES, 1):
        slides, notes = lecture_pages(number, item)
        (LECTURE_DIR / f"lecture-{number:02d}-slides.html").write_text(slides, encoding="utf-8")
        (LECTURE_DIR / f"lecture-{number:02d}-notes.html").write_text(notes, encoding="utf-8")
    for number, item in enumerate(LABS, 1):
        (LAB_DIR / f"lab-{number:02d}.html").write_text(lab_page(number, item), encoding="utf-8")
        student, solutions, assessment = pset_pages(number, PSET_CONTENT[number-1])
        (PSET_DIR / f"problem-set-{number:02d}.html").write_text(student, encoding="utf-8")
        (PSET_DIR / f"problem-set-{number:02d}-solutions.html").write_text(solutions, encoding="utf-8")
        (PSET_DIR / f"problem-set-{number:02d}-assessment.md").write_text(assessment, encoding="utf-8")
    (ROOT / "syllabus.html").write_text(syllabus(), encoding="utf-8")
    (ROOT / "schedule.html").write_text(schedule(), encoding="utf-8")
    (ROOT / "reference-log.md").write_text(reference_log(), encoding="utf-8")
    manifest_data = manifest()
    manifest_data["dataProvenance"]["levels"]["level1"] = "OpenStax §6.4, ALMA Basics, NRAO VLA navigation, ATNF catalogue definitions, and HI4PI paper/CDS release metadata and response values live-verified 2026-09-25."
    manifest_data["dataProvenance"]["levels"]["level2"] = "Other published object and historical survey parameters not re-verified; see reference-log.md for spot-check requirements."
    (ROOT / "course-manifest.json").write_text(json.dumps(manifest_data, indent=2)+"\n", encoding="utf-8")
    (ROOT / "data" / "README.md").write_text("""# ASTR 472 Data\n\nThe seven compact exercise CSVs are synthetic/instructor-provided (level 3), generated by `../src/generate_astr472_package.py`; they are not telescope observations. `radio_facility_reference.csv` records live-verified VLA/ALMA/HI4PI specifications with per-row provenance. The actual HI4PI spectra/cubes are public through CDS catalog `J/A+A/594/A116`; no raw radio archive file is bundled. Lab 07 directs students to retrieve one 20-degree subcube and record its file-level provenance. See `../reference-log.md` for exact citation, retrieval metadata, and the remaining human spot-check requirements.\n""", encoding="utf-8")
    (ROOT / "src" / "README.md").write_text("""# ASTR 472 Source\n\n`generate_astr472_package.py` calculates all displayed worked results from shared physical constants and builds the HTML artifacts and clearly labeled teaching CSVs. Run from the repository root with `.venv/Scripts/python.exe materials/ASTR472/src/generate_astr472_package.py`. Review edits to generated HTML in the generator/data sources so the next build remains reproducible.\n""", encoding="utf-8")
    (ROOT / "README.md").write_text("""# ASTR 472: Radio Astronomy\n\nThree-credit Year 4 elective. Prerequisite: ASTR 340; PHYS 341 recommended. The package contains 14 lectures with paired notes, seven labs, and seven problem sets with separate solutions and assessment instructions. Start at `index.html`; provenance caveats and source links are in `reference-log.md`. Current package status is shown in `course-manifest.json` and `review-report.md`.\n""", encoding="utf-8")
    report = """# ASTR 472 Course Materials Review Report\n\nStatus: Needs correction.\n\n## Initial Review\n\nA complete draft package has been generated and inspected against the applicable course-materials-review criteria and ASTR 340/370 benchmark reports. The scientific scope, derived examples, unique visual geometry, lab procedures, and separate assessment artifacts are present.\n\n### Blocking issue\n\n- The draft cites exact OpenStax section scope but its generated problem sets do not yet provide an adequately cross-checked, exact numbered exercise recommendation for every paired unit. Chapter 6 section/figure numbering is confirmed; assignments need the extracted exercise anchors and adopted-edition caveat made explicit in the student-facing artifacts.\n\n### Correction required\n\n- Add exact exercise/review-question anchors from the local OpenStax index to all seven sets, and disclose the edition spot-check limitation. Re-review the affected assignments and link text after regeneration.\n\nThis initial finding is recorded to track a genuine review/correction cycle; it is not a release approval.\n"""
    if not (ROOT / "review-report.md").exists():
        (ROOT / "review-report.md").write_text(report, encoding="utf-8")

if __name__ == "__main__":
    build()