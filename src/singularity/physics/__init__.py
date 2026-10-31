"""Physics module for SINGULARITY."""

from singularity.physics.gravity import (
    compute_schwarzschild_radius,
    compute_isco_radius,
    compute_photon_sphere_radius,
    paczynski_wiita_acceleration,
    is_absorbed
)
from singularity.physics.orbital_motion import (
    relativistic_orbital_speed,
    circular_orbital_angular_velocity,
    compute_thin_disk_temperature,
    compute_gravitational_redshift,
    compute_doppler_beaming,
    generate_disk_turbulence
)
from singularity.physics.lensing import (
    compute_einstein_ring_radius,
    deflect_stars,
    deflect_far_disk_screen_coords,
    compute_photon_ring_glow
)
from singularity.physics.particle_dynamics import update_particles_vectorized

__all__ = [
    "compute_schwarzschild_radius",
    "compute_isco_radius",
    "compute_photon_sphere_radius",
    "paczynski_wiita_acceleration",
    "is_absorbed",
    "relativistic_orbital_speed",
    "circular_orbital_angular_velocity",
    "compute_thin_disk_temperature",
    "compute_gravitational_redshift",
    "compute_doppler_beaming",
    "generate_disk_turbulence",
    "compute_einstein_ring_radius",
    "deflect_stars",
    "deflect_far_disk_screen_coords",
    "compute_photon_ring_glow",
    "update_particles_vectorized"
]
