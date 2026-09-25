"""Reproducible calculations and published-summary inputs for ASTR 476.

Published values below are transcribed from the cited papers during package
production. Generated curves and test vectors are explicitly model or synthetic
teaching products, not additional observations.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from astropy import units as u
from scipy.integrate import quad


COURSE_ROOT = Path(__file__).resolve().parents[1]
C_KM_S = 299_792.458
H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_LAMBDA = 1.0 - OMEGA_M


# Compact published summaries, not the source surveys' full data vectors.
# Asymmetric bounds are retained separately rather than symmetrized.
PUBLISHED_SUMMARIES = [
    {
        "probe": "Planck 2018 TT,TE,EE+lowE, flat LCDM",
        "observable": "H0", "redshift": "", "value": 67.4,
        "lower_error": 0.5, "upper_error": 0.5,
        "unit": "km s-1 Mpc-1", "source": "Planck2018VI:abstract",
    },
    {
        "probe": "Planck 2018 TT,TE,EE+lowE, flat LCDM",
        "observable": "Omega_m", "redshift": "", "value": 0.315,
        "lower_error": 0.007, "upper_error": 0.007,
        "unit": "dimensionless", "source": "Planck2018VI:abstract",
    },
    {
        "probe": "Planck 2018 TT,TE,EE+lowE, flat LCDM",
        "observable": "100theta_star", "redshift": "", "value": 1.0411,
        "lower_error": 0.0003, "upper_error": 0.0003,
        "unit": "dimensionless", "source": "Planck2018VI:abstract",
    },
    {
        "probe": "Pantheon+ SNe Ia only, flat LCDM",
        "observable": "Omega_M", "redshift": "", "value": 0.334,
        "lower_error": 0.018, "upper_error": 0.018,
        "unit": "dimensionless", "source": "PantheonPlus:abstract",
    },
    {
        "probe": "Pantheon+ SNe Ia only, flat w0CDM",
        "observable": "w0", "redshift": "", "value": -0.90,
        "lower_error": 0.14, "upper_error": 0.14,
        "unit": "dimensionless", "source": "PantheonPlus:abstract",
    },
    {
        "probe": "BOSS DR12 BAO+full shape consensus",
        "observable": "D_V_times_rd_fid_over_rd", "redshift": 0.38,
        "value": 1477.0, "lower_error": 16.0, "upper_error": 16.0,
        "unit": "Mpc", "source": "BOSS_DR12:section8.2_eq21",
    },
    {
        "probe": "BOSS DR12 BAO+full shape consensus",
        "observable": "D_V_times_rd_fid_over_rd", "redshift": 0.51,
        "value": 1877.0, "lower_error": 19.0, "upper_error": 19.0,
        "unit": "Mpc", "source": "BOSS_DR12:section8.2_eq22",
    },
    {
        "probe": "BOSS DR12 BAO+full shape consensus",
        "observable": "D_V_times_rd_fid_over_rd", "redshift": 0.61,
        "value": 2140.0, "lower_error": 22.0, "upper_error": 22.0,
        "unit": "Mpc", "source": "BOSS_DR12:section8.2_eq23",
    },
    {
        "probe": "DES Y3 3x2pt, flat LCDM",
        "observable": "S8", "redshift": "", "value": 0.776,
        "lower_error": 0.017, "upper_error": 0.017,
        "unit": "dimensionless", "source": "DESY3:sectionV.1_eq17",
    },
    {
        "probe": "DES Y3 3x2pt, flat LCDM",
        "observable": "Omega_m", "redshift": "", "value": 0.339,
        "lower_error": 0.031, "upper_error": 0.032,
        "unit": "dimensionless", "source": "DESY3:sectionV.1_eq17",
    },
    {
        "probe": "DES Y3 3x2pt, flat wCDM",
        "observable": "w", "redshift": "", "value": -0.98,
        "lower_error": 0.20, "upper_error": 0.32,
        "unit": "dimensionless", "source": "DESY3:sectionV.2_eq19",
    },
]


def expansion_rate(z: float | np.ndarray, omega_m: float = OMEGA_M) -> float | np.ndarray:
    """H(z)/H0 for a flat matter plus cosmological-constant model."""
    redshift = np.asarray(z, dtype=float)
    result = np.sqrt(omega_m * (1.0 + redshift) ** 3 + 1.0 - omega_m)
    return float(result) if result.ndim == 0 else result


def comoving_distance_mpc(z: float, h0: float = H0_KM_S_MPC,
                          omega_m: float = OMEGA_M) -> float:
    """Line-of-sight comoving distance in flat LCDM, integrated in Mpc."""
    if z < 0:
        raise ValueError("Redshift must be non-negative")
    integral, _ = quad(lambda redshift: 1.0 / expansion_rate(redshift, omega_m), 0.0, z)
    return C_KM_S / h0 * integral


def luminosity_distance_mpc(z: float, h0: float = H0_KM_S_MPC,
                            omega_m: float = OMEGA_M) -> float:
    return (1.0 + z) * comoving_distance_mpc(z, h0, omega_m)


def distance_modulus(z: float, h0: float = H0_KM_S_MPC,
                     omega_m: float = OMEGA_M) -> float:
    distance = luminosity_distance_mpc(z, h0, omega_m)
    if distance <= 0:
        raise ValueError("Distance modulus is undefined at zero distance")
    return 5.0 * np.log10(distance) + 25.0


def transverse_distance_mpc(z: float, h0: float = H0_KM_S_MPC,
                            omega_m: float = OMEGA_M) -> float:
    """Transverse comoving distance for the flat geometry used here."""
    return comoving_distance_mpc(z, h0, omega_m)


def hubble_distance_mpc(z: float, h0: float = H0_KM_S_MPC,
                        omega_m: float = OMEGA_M) -> float:
    return C_KM_S / (h0 * expansion_rate(z, omega_m))


def volume_averaged_distance_mpc(z: float, h0: float = H0_KM_S_MPC,
                                 omega_m: float = OMEGA_M) -> float:
    """D_V = [D_M^2 c z/H(z)]^(1/3), with all distances in Mpc."""
    if z <= 0:
        raise ValueError("D_V is defined here only for positive redshift")
    dm = transverse_distance_mpc(z, h0, omega_m)
    dh = hubble_distance_mpc(z, h0, omega_m)
    return (dm**2 * dh * z) ** (1.0 / 3.0)


def gaussian_chi_square(residual: np.ndarray, covariance: np.ndarray) -> float:
    """Compute r^T C^-1 r using Cholesky solves, without explicit inversion."""
    residual = np.asarray(residual, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    if covariance.shape != (residual.size, residual.size):
        raise ValueError("Covariance shape must match the residual vector")
    factor = np.linalg.cholesky(covariance)
    whitened = np.linalg.solve(factor, residual)
    return float(whitened @ whitened)


def angular_scale_degrees(one_hundred_theta_star: float = 1.0411) -> float:
    """Convert Planck's reported 100 theta_* to an angular scale in degrees."""
    return float(np.degrees(one_hundred_theta_star / 100.0))


def astropy_distance_check(z: float = 1.0) -> float:
    """Compare this integrator to Astropy's independently implemented FLRW model."""
    from astropy.cosmology import FlatLambdaCDM

    cosmology = FlatLambdaCDM(H0=H0_KM_S_MPC * u.km / u.s / u.Mpc,
                              Om0=OMEGA_M, Tcmb0=0.0 * u.K)
    return float(cosmology.luminosity_distance(z).to_value(u.Mpc))


def compute_reference_results() -> dict[str, float]:
    """Calculate shared numerical examples used across course artifacts."""
    z = 1.0
    dl = luminosity_distance_mpc(z)
    h0_per_second = H0_KM_S_MPC / 3.085677581491367e19
    return {
        "h0_s-1": h0_per_second,
        "age_hubble_gyr": 1.0 / h0_per_second / (365.25 * 86400.0 * 1.0e9),
        "z1_comoving_distance_mpc": comoving_distance_mpc(z),
        "z1_luminosity_distance_mpc": dl,
        "z1_distance_modulus_mag": distance_modulus(z),
        "z1_angular_diameter_distance_mpc": dl / (1.0 + z) ** 2,
        "z0_38_dv_mpc": volume_averaged_distance_mpc(0.38),
        "planck_theta_star_deg": angular_scale_degrees(),
        "des_s8_asymmetry_fraction": (0.017 + 0.017) / (2.0 * 0.776),
        "des_source_density_per_arcmin2": 5.9,
        "des_shape_noise_per_component": 0.26,
    }


def write_published_summary_csv(path: Path | None = None) -> Path:
    """Write the compact literature-value table with source and model labels."""
    output = path or COURSE_ROOT / "data" / "published-summary-measurements.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["probe", "observable", "redshift", "value", "lower_error",
                  "upper_error", "unit", "source"]
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(PUBLISHED_SUMMARIES)
    return output


def write_reference_results(path: Path | None = None) -> Path:
    output = path or COURSE_ROOT / "data" / "computed-reference-results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(compute_reference_results(), indent=2) + "\n", encoding="utf-8")
    return output


def self_test() -> dict[str, float]:
    results = compute_reference_results()
    independent_dl = astropy_distance_check()
    if not np.isclose(results["z1_luminosity_distance_mpc"], independent_dl, rtol=2e-5):
        raise AssertionError("Independent Astropy luminosity-distance check failed")
    if not np.isclose(results["z1_distance_modulus_mag"], 44.10, atol=0.15):
        raise AssertionError("z=1 distance-modulus sanity check failed")
    if not np.isclose(angular_scale_degrees(), 0.5964, atol=0.0002):
        raise AssertionError("Planck acoustic-angle unit conversion failed")
    if not 1400.0 < results["z0_38_dv_mpc"] < 1600.0:
        raise AssertionError("BOSS redshift-0.38 D_V scale check failed")
    test_covariance = np.array([[4.0, 1.2], [1.2, 9.0]])
    test_residual = np.array([2.0, -3.0])
    if not np.isclose(gaussian_chi_square(test_residual, test_covariance), 2.5):
        raise AssertionError("Correlated Gaussian likelihood check failed")
    return {**results, "astropy_z1_luminosity_distance_mpc": independent_dl}


if __name__ == "__main__":
    print(json.dumps(self_test(), indent=2, sort_keys=True))