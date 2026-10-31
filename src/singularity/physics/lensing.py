"""Screen-space gravitational lensing approximation and Einstein ring deflection.

Implements relativistic light bending for background starfields and accretion disk
structures, including the elevation of the far-side accretion disk above the shadow.
"""

from typing import Tuple
import numpy as np


def compute_einstein_ring_radius(event_horizon_radius: float, intensity: float = 1.0) -> float:
    """Calculate the apparent Einstein ring radius in screen pixels.
    In Schwarzschild geometry, the apparent shadow diameter is sqrt(27)/2 * Rs ~ 2.6 Rs.
    The bright photon ring surrounds this shadow at ~1.5 - 2.6 Rs.
    """
    base_radius = event_horizon_radius * 1.55
    return base_radius * np.sqrt(max(0.1, intensity))


def deflect_stars(
    star_positions_2d: np.ndarray,
    center_xy: Tuple[float, float],
    einstein_radius: float,
    intensity: float = 1.0
) -> Tuple[np.ndarray, np.ndarray]:
    """Deflect 2D background star positions around the black hole center.

    Uses the relativistic lens equation:
        r_app = 0.5 * (r_true + sqrt(r_true^2 + 4 * r_E^2))

    Returns:
        deflected_coords: [N, 2] deflected screen coordinates.
        magnification: [N] flux magnification factor.
    """
    if len(star_positions_2d) == 0:
        return np.empty((0, 2), dtype=np.float32), np.empty((0,), dtype=np.float32)

    cx, cy = center_xy
    delta = star_positions_2d - np.array([cx, cy], dtype=np.float32)
    dist_true = np.linalg.norm(delta, axis=1)

    dist_safe = np.maximum(dist_true, 1e-4)
    unit_dir = delta / dist_safe[:, np.newaxis]

    re_eff = einstein_radius * np.sqrt(max(0.01, intensity))
    re_sq = re_eff * re_eff

    # Primary relativistic image radius
    dist_deflected = 0.5 * (dist_safe + np.sqrt(dist_safe * dist_safe + 4.0 * re_sq))

    # Relativistic magnification factor
    ratio = re_eff / np.maximum(dist_deflected, 1.0)
    denom = np.maximum(1.0 - np.power(ratio, 4.0), 0.12)
    magnification = np.clip(1.0 / denom, 0.8, 3.5).astype(np.float32)

    deflected_coords = np.array([cx, cy], dtype=np.float32) + unit_dir * dist_deflected[:, np.newaxis]
    return deflected_coords.astype(np.float32), magnification


def deflect_far_disk_screen_coords(
    screen_coords: np.ndarray,
    center_xy: Tuple[float, float],
    einstein_radius: float,
    is_far_side_mask: np.ndarray,
    pitch_angle: float,
    intensity: float = 1.0
) -> np.ndarray:
    """Relativistic gravitational lensing deflection for the far side of an inclined accretion disk.

    In general relativity, light from the back side of the disk bends over and under
    the black hole, elevating the back rim so it appears arched above the shadow.
    The effect is proportional to inclination sin(pitch).
    """
    if len(screen_coords) == 0 or not np.any(is_far_side_mask):
        return screen_coords.copy()

    coords = screen_coords.copy()
    cx, cy = center_xy
    re_eff = einstein_radius * np.sqrt(max(0.05, intensity))
    re_sq = re_eff * re_eff

    # Only apply to far-side particles when camera has non-zero inclination
    inclination_factor = np.sin(abs(pitch_angle))
    if inclination_factor < 0.05:
        return coords

    far_indices = np.where(is_far_side_mask)[0]
    for idx in far_indices:
        sx = coords[idx, 0]
        sy = coords[idx, 1]

        dx = sx - cx
        dy = sy - cy
        dist = np.hypot(dx, dy)
        if dist < 1.0:
            continue

        # Invert vertical offset to bend over the top of the event horizon
        # For points above center (dy < 0 in screen coords), deflect further upward (-dy)
        deflection_mag = (re_sq / (dist * dist + re_sq * 0.4)) * re_eff * 0.55 * inclination_factor
        # Primarily deflect vertically in the sky plane
        coords[idx, 1] += (dy / dist) * deflection_mag

    return coords


def compute_photon_ring_glow(
    grid_radii: np.ndarray,
    einstein_radius: float,
    width_px: float = 12.0
) -> np.ndarray:
    """Compute intensity profile of the relativistic photon ring."""
    dist_from_ring = np.abs(grid_radii - einstein_radius)
    intensity = np.exp(-0.5 * (dist_from_ring / max(width_px, 1.0)) ** 2)
    return intensity.astype(np.float32)
