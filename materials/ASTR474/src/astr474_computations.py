"""Reproducible numerical experiments shared by ASTR 474 materials.

Synthetic experiments are teaching benchmarks, not research-grade simulations.
The embedded JPL Horizons Earth vectors are published ephemeris values whose
original response was not retrieved during the current verification session.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import rebound
import scipy
from astropy import constants as const
from astropy import units as u
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
GENERATED = DATA / "generated"
SEED = 47409
GAMMA_GAS = 1.4

JPL_EARTH = {
    "epoch_jd_tdb": [2460676.5, 2460677.5],
    "position_au": [
        [-1.786834409731047e-1, 9.669827953774551e-1, -5.109423915082682e-5],
        [-1.958590878880783e-1, 9.636382284641026e-1, -5.114611656384336e-5],
    ],
    "velocity_au_day": [
        [-1.720473858166942e-2, -3.193533189307208e-3, 5.457174067040888e-9],
        [-1.714560420414992e-2, -3.495399751114181e-3, -1.066814793631727e-7],
    ],
}

JPL_REQUEST = {
    "provenanceLevel": 2,
    "status": "published ephemeris values; not live-verified this session",
    "source": "NASA/JPL Horizons API",
    "api": "https://ssd-api.jpl.nasa.gov/api/horizons.api",
    "documentation": "https://ssd-api.jpl.nasa.gov/doc/horizons.html",
    "queryParameters": {
        "format": "json", "COMMAND": "'399'", "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'", "EPHEM_TYPE": "'VECTORS'", "CENTER": "'500@10'",
        "START_TIME": "'2025-01-01 00:00'", "STOP_TIME": "'2025-01-03 00:00'",
        "STEP_SIZE": "'1 d'", "TIME_TYPE": "'TDB'", "REF_SYSTEM": "'J2000'",
        "REF_PLANE": "'ECLIPTIC'", "VEC_TABLE": "'2'", "OUT_UNITS": "'AU-D'",
        "VEC_CORR": "'NONE'", "CSV_FORMAT": "'YES'",
    },
    "target": "399, Earth center",
    "center": "500@10, Sun center (body code 10)",
    "epochs": ["2025-01-01 00:00 TDB", "2025-01-02 00:00 TDB"],
    "timeScale": "TDB",
    "referenceSystem": "J2000",
    "referencePlane": "ECLIPTIC",
    "vectorType": "State vectors, table 2; geometric correction NONE",
    "units": "AU and AU/day",
    "accessAttemptDate": "2026-09-25",
    "accessAttemptUrl": "https://ssd-api.jpl.nasa.gov/api/horizons.api?format=json&COMMAND=399&OBJ_DATA=NO&MAKE_EPHEM=YES&EPHEM_TYPE=VECTORS&CENTER=500%4010&START_TIME=2025-01-01%2000%3A00&STOP_TIME=2025-01-03%2000%3A00&STEP_SIZE=1%20d&TIME_TYPE=TDB&REF_SYSTEM=J2000&REF_PLANE=ECLIPTIC&VEC_TABLE=2&OUT_UNITS=AU-D&VEC_CORR=NONE&CSV_FORMAT=YES",
    "accessAttemptResult": "PowerShell Invoke-WebRequest GET returned HTTP 404 Not Found from nginx; no response body or newly fetched vector values were available",
    "embeddedValuesNote": "The CSV contains the values already embedded in this package; this trace does not represent a newly retrieved raw Horizons response.",
}


def float_precision() -> dict[str, float]:
    spacing = float(np.spacing(np.float64(1.0)))
    direct = float((1.0 + spacing / 2.0) - 1.0)
    reordered = float((1.0 - 1.0) + spacing / 2.0)
    return {"unit_roundoff_spacing": spacing, "lost_increment": direct, "reordered_increment": reordered}


def decay_convergence() -> list[dict[str, float]]:
    rows = []
    exact = float(np.exp(-1.0))
    for tolerance in (1e-3, 1e-6, 1e-9, 1e-12):
        solution = solve_ivp(lambda time, state: -state, (0.0, 1.0), [1.0],
                             method="RK45", rtol=tolerance, atol=tolerance * 1e-3)
        rows.append({"rtol": tolerance, "steps": float(solution.t.size),
                     "final": float(solution.y[0, -1]), "absolute_error": abs(float(solution.y[0, -1]) - exact),
                     "analytic": exact})
    return rows


def _rebound_simulation() -> rebound.Simulation:
    sim = rebound.Simulation()
    sim.units = ("day", "AU", "Msun")
    sim.G = (const.GM_sun / const.M_sun).to_value(u.au**3 / u.day**2 / u.Msun)
    sim.integrator = "whfast"
    sim.add(m=1.0)
    sim.add(m=const.M_earth.to_value(u.Msun),
            x=JPL_EARTH["position_au"][0][0], y=JPL_EARTH["position_au"][0][1],
            z=JPL_EARTH["position_au"][0][2],
            vx=JPL_EARTH["velocity_au_day"][0][0], vy=JPL_EARTH["velocity_au_day"][0][1],
            vz=JPL_EARTH["velocity_au_day"][0][2])
    sim.move_to_com()
    return sim


def rebound_ephemeris_check() -> dict[str, float]:
    sim = _rebound_simulation()
    sim.dt = 0.125
    sim.integrator.safe_mode = 0
    sim.integrate(1.0)
    sun = sim.particles[0]
    earth = sim.particles[1]
    position = np.array([earth.x - sun.x, earth.y - sun.y, earth.z - sun.z])
    reference = np.asarray(JPL_EARTH["position_au"][1])
    residual_au = float(np.linalg.norm(position - reference))
    return {"position_residual_au": residual_au,
            "position_residual_km": float((residual_au * u.au).to_value(u.km)),
            "model_scope": "Sun-relative Newtonian two-body propagation compared with DE441 Earth-center state"}


def scipy_ephemeris_check() -> dict[str, float]:
    mu = const.GM_sun.to_value(u.au**3 / u.day**2)
    initial = np.asarray(JPL_EARTH["position_au"][0] + JPL_EARTH["velocity_au_day"][0])

    def derivative(time: float, state: np.ndarray) -> np.ndarray:
        del time
        position = state[:3]
        return np.concatenate((state[3:], -mu * position / np.linalg.norm(position) ** 3))

    result = solve_ivp(derivative, (0.0, 1.0), initial, method="DOP853", rtol=1e-13, atol=1e-15)
    reference = np.asarray(JPL_EARTH["position_au"][1])
    residual_au = float(np.linalg.norm(result.y[:3, -1] - reference))
    return {"position_residual_au": residual_au,
            "position_residual_km": float((residual_au * u.au).to_value(u.km)),
            "function_evaluations": float(result.nfev), "solver_success": float(result.success),
            "model_scope": "independent DOP853 Newtonian Sun-Earth propagation compared with DE441"}


def rebound_timestep_study() -> list[dict[str, float]]:
    gm = (const.GM_sun / const.M_sun).to_value(u.au**3 / u.day**2 / u.Msun)
    period_days = float((2 * np.pi * np.sqrt((1 * u.au) ** 3 / const.GM_sun)).to_value(u.day))
    rows = []
    for steps_per_period in (20, 40, 80, 160):
        sim = rebound.Simulation()
        sim.units = ("day", "AU", "Msun")
        sim.G = gm
        sim.integrator = "whfast"
        sim.dt = period_days / steps_per_period
        sim.integrator.safe_mode = 0
        sim.add(m=1.0)
        sim.add(m=const.M_earth.to_value(u.Msun), a=1.0, e=0.0)
        sim.move_to_com()
        initial = sim.particles[1]
        initial_position = np.array([initial.x, initial.y, initial.z])
        initial_energy = sim.energy()
        initial_angular_momentum = np.array([sim.angular_momentum().x, sim.angular_momentum().y,
                                             sim.angular_momentum().z])
        sim.integrate(period_days)
        final = sim.particles[1]
        final_position = np.array([final.x, final.y, final.z])
        final_angular_momentum = np.array([sim.angular_momentum().x, sim.angular_momentum().y,
                                           sim.angular_momentum().z])
        rows.append({"steps_per_period": float(steps_per_period), "dt_day": sim.dt,
                     "period_day": period_days,
                     "relative_energy_error": abs((sim.energy() - initial_energy) / initial_energy),
                     "relative_angular_momentum_error": float(np.linalg.norm(final_angular_momentum - initial_angular_momentum)
                                                              / np.linalg.norm(initial_angular_momentum)),
                     "endpoint_position_error_au": float(np.linalg.norm(final_position - initial_position))})
    return rows


def rebound_nbody_conservation() -> list[dict[str, float]]:
    gm = (const.GM_sun / const.M_sun).to_value(u.au**3 / u.day**2 / u.Msun)
    earth_mass = const.M_earth.to_value(u.Msun)
    jupiter_mass = (const.GM_jup / const.GM_sun).to_value(u.dimensionless_unscaled)
    duration = 12.0 * 365.25
    rows = []
    for steps_per_earth_year in (64, 128, 256):
        sim = rebound.Simulation()
        sim.units = ("day", "AU", "Msun")
        sim.G = gm
        sim.integrator = "whfast"
        sim.integrator.safe_mode = 0
        sim.dt = 365.25 / steps_per_earth_year
        sim.add(m=1.0)
        sim.add(m=earth_mass, a=1.0, e=0.0167)
        sim.add(m=jupiter_mass, a=5.204, e=0.0489)
        sim.move_to_com()
        initial_energy = sim.energy()
        initial_angular = np.array([sim.angular_momentum().x, sim.angular_momentum().y,
                                    sim.angular_momentum().z])
        initial_momentum = np.array([
            sum(p.m * p.vx for p in sim.particles),
            sum(p.m * p.vy for p in sim.particles),
            sum(p.m * p.vz for p in sim.particles),
        ])
        momentum_scale = sum(p.m * np.linalg.norm([p.vx, p.vy, p.vz]) for p in sim.particles)
        sim.integrate(duration)
        final_angular = np.array([sim.angular_momentum().x, sim.angular_momentum().y,
                                 sim.angular_momentum().z])
        final_momentum = np.array([
            sum(p.m * p.vx for p in sim.particles),
            sum(p.m * p.vy for p in sim.particles),
            sum(p.m * p.vz for p in sim.particles),
        ])
        rows.append({"steps_per_earth_year": float(steps_per_earth_year), "dt_day": sim.dt,
                     "duration_day": duration,
                     "relative_energy_error": abs((sim.energy() - initial_energy) / initial_energy),
                     "relative_angular_momentum_error": float(np.linalg.norm(final_angular - initial_angular)
                                                              / np.linalg.norm(initial_angular)),
                     "scaled_momentum_error": float(np.linalg.norm(final_momentum - initial_momentum)
                                                     / momentum_scale)})
    return rows


def _primitive_to_conserved(rho: np.ndarray, velocity: np.ndarray, pressure: np.ndarray) -> np.ndarray:
    energy = pressure / (GAMMA_GAS - 1.0) + 0.5 * rho * velocity**2
    return np.vstack((rho, rho * velocity, energy))


def _physical_flux(state: np.ndarray) -> np.ndarray:
    rho, momentum, energy = state
    velocity = momentum / rho
    pressure = (GAMMA_GAS - 1.0) * (energy - 0.5 * momentum * velocity)
    return np.vstack((momentum, momentum * velocity + pressure, (energy + pressure) * velocity))


def sod_shock_tube(cells: int, final_time: float = 0.2) -> tuple[np.ndarray, np.ndarray, float]:
    """First-order Rusanov finite-volume teaching solver for the 1-D Euler equations."""
    spacing = 1.0 / cells
    centers = (np.arange(cells) + 0.5) * spacing
    density = np.where(centers < 0.5, 1.0, 0.125)
    pressure = np.where(centers < 0.5, 1.0, 0.1)
    velocity = np.zeros(cells)
    state = _primitive_to_conserved(density, velocity, pressure)
    initial_mass = float(np.sum(state[0]) * spacing)
    time = 0.0
    cfl = 0.35
    while time < final_time:
        rho = state[0]
        momentum = state[1]
        energy = state[2]
        flow_velocity = momentum / rho
        pressure = (GAMMA_GAS - 1.0) * (energy - 0.5 * momentum * flow_velocity)
        if np.any(rho <= 0.0) or np.any(pressure <= 0.0):
            raise RuntimeError("Sod teaching solver produced a non-physical state")
        signal_speed = np.max(np.abs(flow_velocity) + np.sqrt(GAMMA_GAS * pressure / rho))
        dt = min(cfl * spacing / signal_speed, final_time - time)
        padded = np.pad(state, ((0, 0), (1, 1)), mode="edge")
        left_states = padded[:, :-1]
        right_states = padded[:, 1:]
        speed = np.maximum(
            np.abs(left_states[1] / left_states[0]) +
            np.sqrt(GAMMA_GAS * (GAMMA_GAS - 1.0) * (left_states[2] / left_states[0] - 0.5 * (left_states[1] / left_states[0])**2)),
            np.abs(right_states[1] / right_states[0]) +
            np.sqrt(GAMMA_GAS * (GAMMA_GAS - 1.0) * (right_states[2] / right_states[0] - 0.5 * (right_states[1] / right_states[0])**2)),
        )
        numerical_flux = 0.5 * (_physical_flux(left_states) + _physical_flux(right_states)) - 0.5 * speed * (right_states - left_states)
        state -= (dt / spacing) * (numerical_flux[:, 1:] - numerical_flux[:, :-1])
        time += dt
    mass_error = abs(float(np.sum(state[0]) * spacing - initial_mass)) / initial_mass
    return centers, state[0], mass_error


def hydro_resolution_study() -> list[dict[str, float]]:
    reference_x, reference_density, _ = sod_shock_tube(512)
    rows = []
    for cells in (32, 64, 128, 256):
        centers, density, mass_error = sod_shock_tube(cells)
        reference = np.interp(centers, reference_x, reference_density)
        l1_error = float(np.mean(np.abs(density - reference)))
        rows.append({"cells": float(cells), "dx": 1.0 / cells,
                     "relative_mass_error": mass_error, "density_l1_vs_512": l1_error,
                     "density_min": float(np.min(density)), "density_max": float(np.max(density))})
    return rows


def radiative_transfer_check() -> list[dict[str, float]]:
    source = 0.7
    incoming = 0.2
    rows = []
    for optical_depth in (0.01, 0.1, 1.0, 5.0):
        result = solve_ivp(lambda tau, intensity: source - intensity,
                           (0.0, optical_depth), [incoming], method="DOP853",
                           rtol=1e-11, atol=1e-13)
        exact = source + (incoming - source) * np.exp(-optical_depth)
        thin_approx = incoming + (source - incoming) * optical_depth
        rows.append({"tau": optical_depth, "intensity_exact": float(exact),
                     "intensity_scipy": float(result.y[0, -1]),
                     "absolute_solver_error": abs(float(result.y[0, -1]) - float(exact)),
                     "thin_approx": float(thin_approx),
                     "thin_approx_relative_error": abs(float(thin_approx) - float(exact)) / abs(float(exact))})
    return rows


def thin_limit_threshold(relative_tolerance: float = 0.01) -> float:
    source = 0.7
    incoming = 0.2

    def relative_error(optical_depth: float) -> float:
        exact = incoming + (source - incoming) * (1.0 - np.exp(-optical_depth))
        approximation = incoming + (source - incoming) * optical_depth
        return abs(approximation - exact) / abs(exact)

    return float(brentq(lambda depth: relative_error(depth) - relative_tolerance, 1e-10, 1.0))


def monte_carlo_transmission() -> list[dict[str, float]]:
    rng = np.random.default_rng(SEED)
    optical_depth = 2.0
    probability = float(np.exp(-optical_depth))
    trials = rng.random(20_000) < probability
    rows = []
    for count in (100, 500, 2_000, 20_000):
        estimate = float(np.mean(trials[:count]))
        standard_error = float(np.sqrt(estimate * (1.0 - estimate) / count))
        rows.append({"trials": float(count), "seed": float(SEED), "optical_depth": optical_depth,
                     "analytic_transmission": probability, "estimate": estimate,
                     "standard_error": standard_error,
                     "absolute_error": abs(estimate - probability)})
    return rows


def importance_sampling_comparison() -> list[dict[str, float]]:
    optical_depth = 4.0
    probability = float(np.exp(-optical_depth))
    count = 10_000
    rng = np.random.default_rng(SEED + 1)
    standard = (rng.random(count) < probability).astype(float)
    standard_estimate = float(np.mean(standard))
    standard_se = float(np.std(standard, ddof=1) / np.sqrt(count))
    proposal_probability = 0.2
    importance_rng = np.random.default_rng(SEED + 2)
    proposal = (importance_rng.random(count) < proposal_probability).astype(float)
    weights = np.where(proposal > 0, probability / proposal_probability,
                       (1.0 - probability) / (1.0 - proposal_probability))
    weighted = proposal * weights
    return [
        {"method": "ordinary Bernoulli sampling", "trials": count, "estimate": standard_estimate,
         "standard_error": standard_se, "analytic": probability},
        {"method": "tilted proposal q=0.2 with likelihood weights", "trials": count,
         "estimate": float(np.mean(weighted)), "standard_error": float(np.std(weighted, ddof=1) / np.sqrt(count)),
         "analytic": probability},
    ]


def radial_velocity_fit() -> dict[str, object]:
    rng = np.random.default_rng(SEED + 3)
    time_days = np.linspace(0.0, 44.8, 64)
    period_days = 11.2
    truth = np.array([20.0, 0.7, 4.0])
    uncertainty = np.full(time_days.size, 3.0)

    def model(parameters: np.ndarray) -> np.ndarray:
        amplitude, phase, offset = parameters
        return offset + amplitude * np.sin(2.0 * np.pi * time_days / period_days + phase)

    observed = model(truth) + rng.normal(0.0, uncertainty)

    def residual(parameters: np.ndarray) -> np.ndarray:
        return (model(parameters) - observed) / uncertainty

    fit = least_squares(residual, np.array([15.0, 0.2, 0.0]), bounds=([0.0, -np.pi, -100.0], [100.0, np.pi, 100.0]))
    fitted = fit.x
    residuals = observed - model(fitted)
    dof = time_days.size - fitted.size
    covariance = np.linalg.pinv(fit.jac.T @ fit.jac) * float(np.sum(fit.fun**2) / dof)
    standard_errors = np.sqrt(np.diag(covariance))
    return {"time_days": time_days.tolist(), "observed_m_s": observed.tolist(),
            "uncertainty_m_s": uncertainty.tolist(), "truth": truth.tolist(),
            "fit": fitted.tolist(), "fit_standard_errors": standard_errors.tolist(),
            "residual_rms_m_s": float(np.sqrt(np.mean(residuals**2))),
            "weighted_chi2": float(np.sum(fit.fun**2)), "degrees_of_freedom": int(dof),
            "max_abs_residual_m_s": float(np.max(np.abs(residuals))),
            "synthetic_seed": SEED + 3}


def beta_posterior() -> dict[str, object]:
    successes, trials = 84, 100
    rng = np.random.default_rng(SEED + 4)
    draws = rng.beta(successes + 1, trials - successes + 1, size=200_000)
    lower, median, upper = np.quantile(draws, [0.16, 0.5, 0.84])
    return {"successes": successes, "trials": trials, "posterior_a": successes + 1,
            "posterior_b": trials - successes + 1, "seed": SEED + 4,
            "draw_count": int(draws.size), "median": float(median),
            "lower_68": float(lower), "upper_68": float(upper),
            "draws": draws.tolist()}


def period_and_units() -> dict[str, float]:
    period = (2.0 * np.pi * np.sqrt((1 * u.au) ** 3 / const.GM_sun)).to(u.day)
    earth_radius = const.R_earth.to(u.km)
    return {"solar_gm_m3_s2": float(const.GM_sun.to_value(u.m**3 / u.s**2)),
            "earth_orbit_period_day": float(period.value),
            "earth_radius_km": float(earth_radius.value),
            "jupiter_gm_m3_s2": float(const.GM_jup.to_value(u.m**3 / u.s**2))}


def compute_results() -> dict[str, object]:
    posterior = beta_posterior()
    profile_x, profile_density, profile_mass_error = sod_shock_tube(128)
    return {
        "floating_point": float_precision(),
        "ode_convergence": decay_convergence(),
        "jpl_earth_validation": rebound_ephemeris_check(),
        "jpl_earth_scipy_crosscheck": scipy_ephemeris_check(),
        "rebound_timestep_convergence": rebound_timestep_study(),
        "rebound_nbody_conservation": rebound_nbody_conservation(),
        "hydro_resolution_study": hydro_resolution_study(),
        "hydro_profile_128": {"cells": 128, "final_time": 0.2, "x": profile_x.tolist(),
                      "density": profile_density.tolist(), "relative_mass_error": profile_mass_error},
        "radiative_transfer": radiative_transfer_check(),
        "thin_limit_1_percent_tau": thin_limit_threshold(),
        "monte_carlo_transmission": monte_carlo_transmission(),
        "importance_sampling": importance_sampling_comparison(),
        "radial_velocity_fit": {key: value for key, value in radial_velocity_fit().items() if key != "draws"},
        "beta_posterior": {key: value for key, value in posterior.items() if key != "draws"},
        "astronomical_parameters": period_and_units(),
        "software_versions": {"numpy": np.__version__, "scipy": scipy.__version__,
                              "astropy": __import__("astropy").__version__,
                              "rebound": rebound.__version__},
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_outputs() -> dict[str, object]:
    GENERATED.mkdir(parents=True, exist_ok=True)
    results = compute_results()
    (GENERATED / "computed_results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    write_csv(GENERATED / "jpl_earth_vectors.csv",
              ["epoch_jd_tdb", "x_au", "y_au", "z_au", "vx_au_day", "vy_au_day", "vz_au_day"],
              [{"epoch_jd_tdb": JPL_EARTH["epoch_jd_tdb"][index],
                **{axis: JPL_EARTH[field][index][component]
                   for field, axis in (("position_au", ("x_au", "y_au", "z_au")),
                                       ("velocity_au_day", ("vx_au_day", "vy_au_day", "vz_au_day")))
                   for component, axis in enumerate(axis)}}
               for index in range(2)])
    from urllib.parse import urlencode
    request_url = JPL_REQUEST["api"] + "?" + urlencode(JPL_REQUEST["queryParameters"])
    vector_path = GENERATED / "jpl_earth_vectors.csv"
    request_record = {**JPL_REQUEST, "requestUrl": request_url,
                      "vectorCsvSha256": hashlib.sha256(vector_path.read_bytes()).hexdigest()}
    (GENERATED / "jpl_earth_request.json").write_text(
        json.dumps(request_record, indent=2) + "\n", encoding="utf-8")
    write_csv(GENERATED / "rebound_convergence.csv", list(results["rebound_timestep_convergence"][0]),
              results["rebound_timestep_convergence"])
    write_csv(GENERATED / "nbody_conservation.csv", list(results["rebound_nbody_conservation"][0]),
              results["rebound_nbody_conservation"])
    write_csv(GENERATED / "hydro_resolution.csv", list(results["hydro_resolution_study"][0]),
              results["hydro_resolution_study"])
    write_csv(GENERATED / "hydro_profile_128.csv", ["x", "density"],
              [{"x": x, "density": density} for x, density in
               zip(results["hydro_profile_128"]["x"], results["hydro_profile_128"]["density"])])
    write_csv(GENERATED / "monte_carlo_trials.csv", list(results["monte_carlo_transmission"][0]),
              results["monte_carlo_transmission"])
    write_csv(GENERATED / "radial_velocity_observations.csv",
              ["time_days", "observed_m_s", "uncertainty_m_s"],
              [{"time_days": t, "observed_m_s": y, "uncertainty_m_s": sigma}
               for t, y, sigma in zip(results["radial_velocity_fit"]["time_days"],
                                      results["radial_velocity_fit"]["observed_m_s"],
                                      results["radial_velocity_fit"]["uncertainty_m_s"])])
    return results


if __name__ == "__main__":
    output = generate_outputs()
    print(json.dumps({"outputs": str(GENERATED), "software_versions": output["software_versions"],
                      "rebound": output["jpl_earth_validation"],
                      "hydro": output["hydro_resolution_study"],
                      "fit": output["radial_velocity_fit"]}, indent=2))