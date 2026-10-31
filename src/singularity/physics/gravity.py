"""Gravitational physics and relativistic potential calculations.

Uses the Paczyński-Wiita pseudo-Newtonian potential, the standard model
in relativistic astrophysics that accurately reproduces the Schwarzschild
event horizon and the Innermost Stable Circular Orbit (ISCO = 3 Rs).
"""

from typing import Tuple
import numpy as np


def compute_schwarzschild_radius(mass: float, g_const: float = 1.0, c_speed: float = 100.0) -> float:
    """Calculate the Schwarzschild event horizon radius Rs = 2 * G * M / c^2.
    In simulation units, default c_speed is scaled for visual time-steps.
    """
    return (2.0 * g_const * mass) / (c_speed * c_speed)


def compute_isco_radius(rs: float) -> float:
    """Calculate the Innermost Stable Circular Orbit (ISCO) radius = 3 * Rs.
    Inside this boundary, circular orbits become unstable and matter plunges
    inward toward the event horizon.
    """
    return 3.0 * rs


def compute_photon_sphere_radius(rs: float) -> float:
    """Calculate the photon sphere radius = 1.5 * Rs.
    The boundary where photons are bent into circular orbits.
    """
    return 1.5 * rs


def paczynski_wiita_acceleration(
    radii: np.ndarray,
    mass: float,
    rs: float,
    g_const: float = 1.0,
    softening: float = 4.0
) -> np.ndarray:
    """Vectorized calculation of gravitational acceleration magnitude using the
    Paczyński-Wiita relativistic potential:
        a(r) = - G * M / (r - Rs)^2

    Near or inside Rs, acceleration is safely capped with softening to avoid
    non-physical infinite values before absorption is triggered.
    """
    effective_r = np.maximum(radii - rs, softening)
    acc = (g_const * mass) / (effective_r * effective_r)
    return acc


def is_absorbed(radii: np.ndarray, rs: float) -> np.ndarray:
    """Return boolean mask indicating which particles have crossed the event horizon."""
    return radii <= rs

