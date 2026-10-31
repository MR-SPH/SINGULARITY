"""High-performance vectorized particle dynamics for the relativistic accretion disk."""

from typing import Tuple
import numpy as np

from singularity.physics.gravity import paczynski_wiita_acceleration
from singularity.physics.orbital_motion import relativistic_orbital_speed, generate_disk_turbulence


def update_particles_vectorized(
    pos: np.ndarray,            # [N, 3] float32
    vel: np.ndarray,            # [N, 3] float32
    angles: np.ndarray,         # [N] float32
    angular_vel: np.ndarray,    # [N] float32
    alive: np.ndarray,          # [N] bool
    age: np.ndarray,            # [N] float32
    lifetime: np.ndarray,       # [N] float32
    alpha: np.ndarray,          # [N] float32
    mass: float,
    rs: float,
    isco_radius: float,
    outer_radius: float,
    rotation_speed: float,
    rotation_direction: float,
    turbulence_factor: float,
    dt: float,
    elapsed_time: float
) -> Tuple[np.ndarray, np.ndarray, int]:
    """Vectorized numerical integration of accretion disk particles with realistic orbital wrapping.

    As characters near the black hole core, angular velocity accelerates sharply, causing letters
    to whip tightly around the event horizon in high-speed relativistic spirals.
    """
    n_particles = len(pos)
    if n_particles == 0:
        return np.empty((0,), dtype=np.float32), np.empty((0,), dtype=bool), 0

    active_mask = alive.copy()
    if not np.any(active_mask):
        return np.zeros((n_particles,), dtype=np.float32), np.zeros((n_particles,), dtype=bool), 0

    # Calculate cylindrical radial distance in disk plane (X-Z plane, Y is vertical)
    px = pos[:, 0]
    py = pos[:, 1]
    pz = pos[:, 2]
    radii = np.sqrt(px * px + pz * pz)
    radii_clamped = np.maximum(radii, 1.0)

    # Current azimuthal angle in disk plane
    theta = np.arctan2(pz, px)

    # Relativistic circular orbital speed
    circ_speed = relativistic_orbital_speed(radii_clamped, mass, rs) * rotation_speed

    # Inward accretion plunge:
    # Matter steadily orbits in the disk, but inside ISCO it begins a smooth inward spiral,
    # maintaining strong tangential speed so it wraps around the core multiple times
    inflow_base = 0.04 * (rs / radii_clamped) * circ_speed
    inside_isco = radii < isco_radius
    inflow = np.where(
        inside_isco,
        inflow_base * 2.8 + 22.0 * (1.0 - radii / np.maximum(isco_radius, 1.0)),
        inflow_base
    )

    # Tangential orbital direction unit vector (-sin(theta), cos(theta))
    sin_t = np.sin(theta)
    cos_t = np.cos(theta)

    tangent_x = -sin_t * rotation_direction
    tangent_z = cos_t * rotation_direction

    # Radial inward unit vector (-cos(theta), -sin(theta))
    inward_x = -cos_t
    inward_z = -sin_t

    # Add subtle spiral turbulence for natural density variations
    turb = generate_disk_turbulence(theta, radii_clamped, elapsed_time, amplitude=turbulence_factor)

    # Target orbital velocities
    vx_target = (tangent_x * circ_speed * (1.0 + turb)) + (inward_x * inflow)
    vz_target = (tangent_z * circ_speed * (1.0 + turb)) + (inward_z * inflow)

    # Smooth velocity relaxation for fluid, organic motion
    blend = np.clip(dt * 9.0, 0.05, 1.0)
    vel[active_mask, 0] += (vx_target[active_mask] - vel[active_mask, 0]) * blend
    vel[active_mask, 2] += (vz_target[active_mask] - vel[active_mask, 2]) * blend

    # Vertical damping for slim disk profile
    omega_y = 2.8 * (circ_speed / radii_clamped)
    vel[active_mask, 1] += (-py[active_mask] * (omega_y[active_mask] * omega_y[active_mask] * 0.1) - vel[active_mask, 1] * 2.2) * dt

    # Position integration
    pos[active_mask, 0] += vel[active_mask, 0] * dt
    pos[active_mask, 1] += vel[active_mask, 1] * dt
    pos[active_mask, 2] += vel[active_mask, 2] * dt

    # Flow alignment: characters align with their instantaneous orbital velocity vector
    # When spiraling near the horizon, characters dynamically bend and wrap with the vortex!
    angles[active_mask] = np.degrees(np.arctan2(vel[active_mask, 2], vel[active_mask, 0])) + 90.0

    # Age and lifetime progression
    age[active_mask] += dt

    # Event horizon absorption: active particles at or inside Rs or exceeding lifetime
    newly_absorbed_mask = active_mask & ((radii <= rs) | (age >= lifetime))
    num_absorbed = int(np.sum(newly_absorbed_mask))

    # Dynamic alpha based on distance: brilliant luminous peak near ISCO and photon sphere
    distance_factor = np.clip((radii - rs) / max(outer_radius - rs, 1.0), 0.0, 1.0)
    isco_proximity = np.exp(-0.5 * ((radii - isco_radius) / max(0.42 * isco_radius, 1.0)) ** 2)
    # Brightness flares up right before the event horizon plunge
    inner_flare = np.exp(-0.5 * ((radii - rs * 1.35) / max(0.25 * rs, 1.0)) ** 2) * 0.45
    alpha[active_mask] = np.clip(0.40 + isco_proximity[active_mask] * 0.55 + inner_flare[active_mask], 0.1, 1.0) * np.clip(distance_factor[active_mask] * 2.8, 0.0, 1.0)

    # Deactivate newly absorbed
    alive[newly_absorbed_mask] = False
    alpha[newly_absorbed_mask] = 0.0

    return radii, newly_absorbed_mask, num_absorbed
