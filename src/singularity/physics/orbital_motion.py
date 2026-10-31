"""Relativistic orbital motion, Shakura-Sunyaev temperature, and Doppler boosting."""

from typing import Tuple
import numpy as np


def compute_thin_disk_temperature(
    radii: np.ndarray,
    r_in: float,
    rs: float
) -> np.ndarray:
    """Compute normalized radial temperature profile inspired by Shakura-Sunyaev thin-disk model:
        T(r) ~ r^(-3/4) * [1 - sqrt(r_in / r)]^(1/4)

    Analytical peak temperature occurs at r_peak = (49/36) * r_in ~ 1.361 * r_in.
    Returns normalized temperature T(r) in [0.0, 1.0].
    """
    radii_arr = np.asarray(radii, dtype=np.float32)
    # Outside inner boundary
    valid_mask = radii_arr > r_in
    temp = np.zeros_like(radii_arr, dtype=np.float32)

    if np.any(valid_mask):
        r_val = radii_arr[valid_mask]
        ratio = r_in / r_val
        # Numerical guard: clamp inner term to >= 0
        inner_term = np.maximum(1.0 - np.sqrt(ratio), 0.0)
        # T(r) formula
        raw_temp = np.power(r_val / r_in, -0.75) * np.power(inner_term, 0.25)

        # Theoretical peak value at r = (49/36) * r_in
        # (49/36)^(-0.75) * (1 - 6/7)^(0.25) = (0.784) * (0.6147) ~ 0.488
        peak_theoretical = 0.488
        temp[valid_mask] = np.clip(raw_temp / peak_theoretical, 0.0, 1.0)

    # For plunging matter inside r_in down to Rs, assign fading residual ionization
    plunge_mask = (radii_arr <= r_in) & (radii_arr > rs)
    if np.any(plunge_mask):
        # Smooth transition into darkness at the event horizon
        plunge_f = (radii_arr[plunge_mask] - rs) / max(r_in - rs, 1e-4)
        temp[plunge_mask] = np.clip(plunge_f * 0.45, 0.0, 0.45)

    return temp


def compute_gravitational_redshift(radii: np.ndarray, rs: float) -> np.ndarray:
    """Compute gravitational redshift attenuation factor:
        g_redshift = sqrt(1 - Rs / r)

    As r -> Rs, observed photon energy and flux drop to 0 at the event horizon.
    """
    safe_r = np.maximum(radii, rs * 1.001)
    redshift = np.sqrt(np.maximum(1.0 - rs / safe_r, 0.0))
    return np.clip(redshift, 0.0, 1.0).astype(np.float32)


def circular_orbital_angular_velocity(
    radii: np.ndarray,
    mass: float,
    rs: float,
    g_const: float = 1.0
) -> np.ndarray:
    """Compute circular orbital angular velocity Omega(r) with Paczyński-Wiita correction:
        Omega(r) = sqrt(G * M) / [r^(1/2) * (r - Rs)]

    For r >> Rs, asymptotically converges to Keplerian sqrt(GM / r^3).
    Near Rs, Omega diverges, causing inner matter to whip ferociously around the core.
    """
    safe_r = np.maximum(radii, rs * 1.05)
    effective_denom = np.sqrt(safe_r) * np.maximum(safe_r - rs, 1e-3)
    omega = np.sqrt(g_const * mass) / effective_denom
    return omega.astype(np.float32)


def relativistic_orbital_speed(
    radii: np.ndarray,
    mass: float,
    rs: float,
    g_const: float = 1.0,
    speed_of_light: float = 220.0
) -> np.ndarray:
    """Calculate circular orbital velocity v_circ(r) = r * Omega(r).
    Clamped strictly to 0.92 * c to remain subluminal.
    """
    omega = circular_orbital_angular_velocity(radii, mass, rs, g_const)
    speed = radii * omega
    max_allowed = 0.92 * speed_of_light
    return np.clip(speed, 0.0, max_allowed).astype(np.float32)


def compute_doppler_beaming(
    velocities_3d: np.ndarray,
    camera_dir: np.ndarray,
    speed_of_light: float = 220.0,
    beaming_intensity: float = 1.6
) -> np.ndarray:
    """Calculate relativistic Doppler beaming (boosting) factor for particles.

    Approaching matter (v . cam_dir > 0) blazes with amplified brilliance and blueshift.
    Receding matter (v . cam_dir < 0) dims and shifts toward deep interstellar red.
    """
    if len(velocities_3d) == 0:
        return np.empty((0,), dtype=np.float32)

    speeds = np.linalg.norm(velocities_3d, axis=1)
    beta = np.clip(speeds / speed_of_light, 0.0, 0.90)
    gamma = 1.0 / np.sqrt(np.maximum(1.0 - beta * beta, 0.01))

    cam_norm = camera_dir / (np.linalg.norm(camera_dir) + 1e-9)
    v_norm = np.zeros_like(velocities_3d)
    nonzero = speeds > 1e-5
    v_norm[nonzero] = velocities_3d[nonzero] / speeds[nonzero, np.newaxis]

    cos_theta = np.dot(v_norm, cam_norm)
    denom = np.maximum(gamma * (1.0 - beta * cos_theta), 0.08)
    doppler_delta = 1.0 / denom

    boost = np.power(doppler_delta, 2.6 * beaming_intensity)
    return np.clip(boost, 0.22, 4.0).astype(np.float32)


def generate_disk_turbulence(
    angles: np.ndarray,
    radii: np.ndarray,
    time_sec: float,
    amplitude: float = 0.05
) -> np.ndarray:
    """Generate subtle relativistic accretion disk turbulence and spiral density waves."""
    spiral1 = np.sin(2.0 * angles - 0.018 * radii + 1.4 * time_sec)
    spiral2 = np.cos(4.0 * angles + 0.008 * radii - 0.9 * time_sec)
    perturbation = (spiral1 * 0.7 + spiral2 * 0.3) * amplitude
    return perturbation.astype(np.float32)
