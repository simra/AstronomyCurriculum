"""Accessible lecture-term explorers for the ASTR 472 generators."""
from __future__ import annotations

import html


TERM_EXPLORER_CSS = """
.glossary-slide{justify-content:flex-start}
.term-explorer{display:grid;grid-template-columns:minmax(220px,.7fr) minmax(0,1.8fr);gap:28px;align-items:stretch;min-height:58vh}
.term-list{display:flex;flex-direction:column;gap:10px}
.term-button{width:100%;padding:12px 14px;border:2px solid var(--line);border-radius:8px;background:#fff;color:var(--navy);font:700 1rem/1.25 'Aptos','Segoe UI',sans-serif;text-align:left;cursor:pointer}
.term-button:hover{border-color:var(--teal)}.term-button:focus-visible{outline:4px solid var(--gold);outline-offset:2px}
.term-button[aria-selected="true"]{color:#fff;background:var(--teal);border-color:var(--teal)}
.term-details{min-width:0}.term-detail{border:1px solid var(--line);border-radius:10px;padding:18px 22px;background:var(--paper);overflow:auto}
.term-detail h3{margin:0 0 10px;color:var(--teal);font:700 1.45rem/1.2 'Aptos','Segoe UI',sans-serif}
.term-detail p{font-size:1rem;margin:9px 0}.term-detail[hidden]{display:none}.term-visual{margin-top:14px}
@media(max-width:800px){.term-explorer{grid-template-columns:1fr}.term-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.term-list{grid-template-columns:1fr}}
@media print{.term-explorer{display:block}.term-list{display:none}.term-detail[hidden]{display:block!important}.term-detail{break-inside:avoid;margin:12px 0}}
"""

TERM_EXPLORER_SCRIPT = """
<script>
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
      if (!["ArrowDown", "ArrowUp", "ArrowRight", "ArrowLeft", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      const forward = event.key === "ArrowDown" || event.key === "ArrowRight";
      const nextIndex = event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 : (index + (forward ? 1 : -1) + tabs.length) % tabs.length;
      tabs[nextIndex].focus();
      select(tabs[nextIndex]);
    });
  });
});
</script>
"""

TERM_SETS = {
    1: [("Synchrotron emission", "Broadband radiation from relativistic charged particles accelerated transverse to a magnetic field."),
        ("Spectral index", "The exponent describing how flux density changes with observing frequency in a power-law spectrum."),
        ("Free-free emission", "Thermal continuum produced when electrons accelerate in the Coulomb fields of ions."),
        ("Brightness temperature", "The temperature a blackbody would need in the Rayleigh-Jeans limit to reproduce a measured specific intensity."),
        ("Polarization", "The orientation and coherence state of the electric field, recorded through Stokes parameters.")],
    2: [("Primary beam", "The angular sensitivity pattern of one antenna and feed on the sky."),
        ("Aperture efficiency", "The fraction of a dish's geometric area that contributes to effective collecting area."),
        ("Feed illumination", "The amplitude and phase pattern with which a feed couples radiation to the reflector aperture."),
        ("System temperature", "The equivalent noise temperature combining receiver, sky, atmosphere, and spillover contributions."),
        ("Effective area", "The collecting area that converts incident flux density into received power after aperture losses.")],
    3: [("Radiometer equation", "The thermal-noise scaling that relates rms uncertainty to system sensitivity and independent time-frequency samples."),
        ("SEFD", "System-equivalent flux density: the source flux that would double the system noise power."),
        ("Channel width", "The frequency interval represented by one spectral sample after channelization."),
        ("Integration time", "The accumulated duration over which statistically independent measurements are averaged."),
        ("Confusion noise", "Brightness fluctuations from unresolved sources that impose a non-thermal sensitivity floor.")],
    4: [("Specific intensity", "Radiant power per projected area, solid angle, and frequency interval, conserved along an empty ray."),
        ("Brightness temperature", "A Rayleigh-Jeans re-expression of specific intensity, not necessarily a gas kinetic temperature."),
        ("Beam solid angle", "The effective angular area of the normalized telescope response."),
        ("Beam dilution", "Reduction of observed peak brightness when a source occupies only part of the beam."),
        ("Jy per beam", "An image unit giving flux density assigned to one synthesized-beam area.")],
    5: [("Complex visibility", "The complex cross-correlation measured by an antenna pair for one projected spatial frequency."),
        ("Geometric delay", "The path-length difference from a sky direction to two antennas, expressed as a signal arrival-time offset."),
        ("Baseline", "The vector separation of two antennas, projected perpendicular to the source direction and measured in wavelengths."),
        ("uv coordinate", "A projected baseline component that identifies the sampled Fourier mode of sky brightness."),
        ("Fringe phase", "The visibility phase accumulated from geometric delay and source position.")],
    6: [("Aperture synthesis", "Reconstruction of sky structure by combining Fourier samples from many baselines and times."),
        ("Dirty image", "The inverse transform of sampled visibilities before deconvolution."),
        ("Dirty beam", "The point-spread function produced by the actual uv sampling and weighting."),
        ("Visibility weighting", "A rule assigning statistical or resolution-driven weights to measured Fourier samples."),
        ("Largest recoverable scale", "The approximate broadest angular structure constrained by the shortest useful baselines.")],
    7: [("Complex gain", "Antenna-based amplitude and phase response that multiplies the true electric-field correlation."),
        ("Bandpass", "The frequency-dependent complex response of the receiving and correlator chain."),
        ("Delay calibration", "Estimation of phase slope with frequency caused by path or clock offsets."),
        ("Flux calibrator", "A source model used to establish the absolute amplitude scale."),
        ("Phase calibrator", "A nearby compact source observed repeatedly to track time-variable phase.")],
    8: [("Thermal noise", "Random receiver and sky fluctuations that average down approximately with the square root of independent samples."),
        ("Flux-scale uncertainty", "A multiplicative calibration uncertainty shared by targets using the same amplitude reference."),
        ("Primary-beam correction", "Division by the antenna sensitivity pattern to estimate off-axis sky brightness."),
        ("Covariance", "A quantitative description of how errors in different measurements vary together."),
        ("Jackknife test", "A repeat analysis on deliberately split data used to expose systematic differences.")],
    9: [("Rest frequency", "The transition frequency in the emitter's rest frame used as the Doppler reference."),
        ("Radio velocity convention", "The linear velocity coordinate defined from fractional frequency offset relative to rest frequency."),
        ("Spectral resolution", "The smallest frequency or velocity separation that the instrumental response can distinguish."),
        ("Velocity frame", "The reference motion, such as topocentric, barycentric, or LSR, to which a Doppler coordinate is referred."),
        ("Bandpass ripple", "Frequency-dependent calibration structure that can imitate broad weak spectral features.")],
    10: [("Hyperfine transition", "The spin-state transition between the hydrogen ground-state triplet and singlet levels."),
         ("Spin temperature", "The excitation temperature that sets the relative populations of the hyperfine levels."),
         ("Optical depth", "The dimensionless line-of-sight absorption coefficient integrated through the emitting gas."),
         ("Brightness-temperature integral", "The velocity integral of line brightness used in the optically thin H I column conversion."),
         ("H I column density", "The number of neutral hydrogen atoms per unit projected area along the line of sight.")],
    11: [("Dispersion measure", "The line-of-sight integral of free-electron density inferred from frequency-dependent pulse delay."),
         ("Dedispersion", "Correction of the frequency-dependent arrival-time sweep before forming a pulse profile or timing point."),
         ("Scattering", "Multipath propagation through plasma irregularities that broadens and asymmetrically tails radio pulses."),
         ("Time of arrival", "A measured pulse phase referred to a template, clock, frequency convention, and observatory epoch."),
         ("Timing residual", "The observed minus model pulse arrival time after applying clock, propagation, and dynamical corrections.")],
    12: [("Selection function", "The probability that a source with specified properties enters the analyzed sample."),
         ("Completeness", "The fraction of a target population recovered by the survey and analysis pipeline."),
         ("Fluence", "Time-integrated flux density, often used to characterize short radio bursts."),
         ("Detection threshold", "The decision boundary in a search statistic above which candidates are retained."),
         ("Injection-recovery test", "A completeness experiment that adds controlled synthetic signals and measures their recovery rate.")],
    13: [("Local standard of rest", "A conventional velocity frame that removes an adopted Solar motion before Galactic interpretation."),
         ("Tangent point", "The minimum Galactocentric radius sampled along an inner-Galaxy line of sight."),
         ("Terminal velocity", "The extremal line-of-sight velocity associated with gas near the tangent point under circular rotation."),
         ("Kinematic distance", "A distance inferred by matching line-of-sight velocity to an adopted Galactic rotation model."),
         ("Rotation curve", "The circular orbital speed of Galactic material as a function of Galactocentric radius.")],
    14: [("Source catalog", "A structured set of detected components with measured properties, flags, and provenance."),
         ("Completeness correction", "A statistical adjustment for sources missed by detection and selection."),
         ("Reliability", "The fraction of catalog entries expected to correspond to real astrophysical sources."),
         ("Confusion", "Blending or background fluctuations caused by multiple unresolved sources within the response."),
         ("Reproducible workflow", "A recorded chain of data, code, configuration, environment, and validation sufficient to audit a claim.")],
}


def _terms(number: int) -> list[tuple[str, str]]:
    terms = TERM_SETS[number]
    if not 5 <= len(terms) <= 8:
        raise ValueError(f"Lecture {number:02d} requires 5-8 terms")
    return terms


def slide_section(number: int, title: str, question: str, equation: str, evidence: str, limitation: str) -> str:
    terms = _terms(number)
    buttons = []
    panels = []
    for index, (name, definition) in enumerate(terms, 1):
        tab_id = f"term-{number:02d}-{index}-tab"
        panel_id = f"term-{number:02d}-{index}-panel"
        selected = "true" if index == 1 else "false"
        hidden = "" if index == 1 else " hidden"
        neighbors = terms[(index - 2) % len(terms)][0], terms[index % len(terms)][0]
        buttons.append(
            f'<button class="term-button" id="{tab_id}" type="button" role="tab" '
            f'aria-selected="{selected}" aria-controls="{panel_id}" data-term-target="{panel_id}">{html.escape(name)}</button>'
        )
        panels.append(
            f'<article class="term-detail" id="{panel_id}" role="tabpanel" aria-labelledby="{tab_id}"{hidden}>'
            f'<h3>{html.escape(name)}</h3><p><strong>Definition:</strong> {html.escape(definition)}</p>'
            f'<p><strong>Why it matters here:</strong> It is needed to answer {html.escape(question)} and to interpret {html.escape(evidence)}</p>'
            f'<p><strong>Relationships:</strong> Use it with <em>{html.escape(neighbors[0])}</em> and <em>{html.escape(neighbors[1])}</em>; the lecture model is <span class="equation-inline">\\({equation}\\)</span>.</p>'
            f'<p><strong>Boundary or common confusion:</strong> {html.escape(limitation)}</p></article>'
        )
    return (
        f'<section class="slide glossary-slide" aria-labelledby="terms-{number:02d}-heading">'
        f'<h2 id="terms-{number:02d}-heading">Terms for This Lecture</h2>'
        f'<div class="term-explorer" data-term-explorer><div class="term-list" role="tablist" aria-label="Lecture terms">'
        + "".join(buttons) + '</div><div class="term-details">' + "".join(panels) + "</div></div></section>"
    )


def notes_section(number: int, title: str, question: str, equation: str, evidence: str, limitation: str) -> str:
    terms = _terms(number)
    entries = []
    for index, (name, definition) in enumerate(terms):
        next_name = terms[(index + 1) % len(terms)][0]
        entries.append(
            f'<dt><strong>{html.escape(name)}</strong></dt><dd><p>{html.escape(definition)} '
            f'In {html.escape(title)}, it helps resolve the question <q>{html.escape(question)}</q></p>'
            f'<p><strong>Use in the reasoning chain:</strong> The term links the observable or diagnostic '
            f'<q>{html.escape(evidence.rstrip(".!?"))}</q> to the model <span class="equation-inline">\\({equation}\\)</span>. '
            f'Compare it directly with <em>{html.escape(next_name)}</em> rather than treating either quantity in isolation.</p>'
            f'<p><strong>Scope:</strong> {html.escape(limitation)} The term therefore supports an inference only when its '
            f'measurement convention, calibration stage, and stated approximation are retained.</p></dd>'
        )
    return (
        "<section><h2>Terms Developed in Context</h2>"
        "<p>These terms connect the measured radio product to the physical model and delimit what the observation can support.</p>"
        "<dl>" + "".join(entries) + "</dl></section>"
    )
