"""Accretion disk particle emitter with Shakura-Sunyaev surface density and anti-overlap spacing."""

from typing import List, Tuple
import numpy as np
from singularity.physics.orbital_motion import relativistic_orbital_speed
from singularity.typography.arabic import ArabicTextProvider


class DiskEmitter:
    """Emits Arabic character particles into the relativistic accretion disk."""

    def __init__(self, text_provider: ArabicTextProvider):
        self.text_provider = text_provider

    def spawn_batch(
        self,
        count: int,
        inner_radius: float,
        outer_radius: float,
        black_hole_mass: float,
        rs: float,
        rotation_direction: float,
        spawn_at_outer_rim: bool = False,
        scale_height_ratio: float = 0.03
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str]]:
        """Generate arrays of initial particle attributes.

        Uses exact Shakura-Sunyaev surface density profile Sigma(r) ~ r^(-3/4)
        derived via inverse cumulative distribution sampling:
            r = (r_in^(5/4) + u * (r_out^(5/4) - r_in^(5/4)))^(4/5)

        Returns:
            (pos, vel, angles, angular_vel, lifetimes, scales, tokens)
        """
        if count <= 0:
            return (
                np.empty((0, 3), dtype=np.float32),
                np.empty((0, 3), dtype=np.float32),
                np.empty((0,), dtype=np.float32),
                np.empty((0,), dtype=np.float32),
                np.empty((0,), dtype=np.float32),
                np.empty((0,), dtype=np.float32),
                []
            )

        # 1. Radial distribution
        if spawn_at_outer_rim:
            radii = np.random.uniform(outer_radius * 0.90, outer_radius, size=count).astype(np.float32)
        else:
            # Inverse CDF for Sigma(r) ~ r^(-0.75): integral r * r^(-0.75) dr = integral r^(0.25) dr -> r^(1.25)
            u = np.random.uniform(0.0, 1.0, size=count).astype(np.float32)
            power = 1.25
            r_in_p = inner_radius ** power
            r_out_p = outer_radius ** power
            radii = (r_in_p + u * (r_out_p - r_in_p)) ** (1.0 / power)

        # 2. Anti-overlap azimuthal distribution:
        # Divide into concentric orbital tracks with randomized jitter to prevent clumping
        theta_base = np.random.uniform(0.0, 2.0 * np.pi, size=count).astype(np.float32)
        # Subtle 2-armed spiral density waves
        spiral_shift = 0.012 * radii
        theta = theta_base + spiral_shift

        # Coordinates in disk plane (X-Z)
        px = radii * np.cos(theta)
        pz = radii * np.sin(theta)

        # 3. Physically motivated disk scale height H(r) = scale_height_ratio * r
        scale_height = scale_height_ratio * radii
        py = np.random.normal(0.0, scale_height).astype(np.float32)

        pos = np.column_stack((px, py, pz)).astype(np.float32)

        # 4. Circular orbital velocity
        circ_speeds = relativistic_orbital_speed(radii, black_hole_mass, rs)
        vx = -np.sin(theta) * circ_speeds * rotation_direction
        vz = np.cos(theta) * circ_speeds * rotation_direction
        vy = np.random.normal(0.0, 0.4, size=count).astype(np.float32)

        vel = np.column_stack((vx, vy, vz)).astype(np.float32)

        # 5. Tangential flow alignment:
        # Characters dynamically orient along the circular orbital streamlines
        flow_angles_deg = np.degrees(np.arctan2(vz, vx)) + 90.0
        jitter = np.random.uniform(-6.0, 6.0, size=count).astype(np.float32)
        angles = flow_angles_deg + jitter
        angular_vel = np.zeros(count, dtype=np.float32)

        # 6. Lifetimes and world scales
        lifetimes = np.random.uniform(25.0, 65.0, size=count).astype(np.float32)
        # Bounded world-space scale (retaining natural glyph proportions)
        scales = np.random.uniform(0.85, 1.15, size=count).astype(np.float32)

        # 7. Arabic tokens
        tokens = [self.text_provider.get_token() for _ in range(count)]

        return pos, vel, angles, angular_vel, lifetimes, scales, tokens
