"""Vectorized Struct-of-Arrays (SoA) particle pool for high-performance updates."""

from typing import List, Tuple
import numpy as np

from singularity.core.config import EngineConfig
from singularity.particles.emitter import DiskEmitter
from singularity.physics.particle_dynamics import update_particles_vectorized
from singularity.typography.arabic import ArabicTextProvider


class ParticleSystem:
    """Vectorized particle system managing Arabic character particles in the accretion disk."""

    def __init__(
        self,
        config: EngineConfig,
        text_provider: ArabicTextProvider,
        max_capacity: int = 8000
    ):
        self.config = config
        self.text_provider = text_provider
        self.emitter = DiskEmitter(text_provider)
        self.capacity = max_capacity
        self.target_count = min(config.max_particles, max_capacity)

        # Allocate contiguous SoA buffers
        self.pos = np.zeros((self.capacity, 3), dtype=np.float32)
        self.vel = np.zeros((self.capacity, 3), dtype=np.float32)
        self.angles = np.zeros((self.capacity,), dtype=np.float32)
        self.angular_vel = np.zeros((self.capacity,), dtype=np.float32)
        self.alive = np.zeros((self.capacity,), dtype=bool)
        self.age = np.zeros((self.capacity,), dtype=np.float32)
        self.lifetime = np.zeros((self.capacity,), dtype=np.float32)
        self.alpha = np.zeros((self.capacity,), dtype=np.float32)
        self.scale = np.ones((self.capacity,), dtype=np.float32)
        self.radii = np.zeros((self.capacity,), dtype=np.float32)
        self.tokens: List[str] = ["ا"] * self.capacity

        self.total_absorbed: int = 0
        self.initialize_pool()

    def initialize_pool(self) -> None:
        """Populate the particle pool up to target_count using normalized geometry."""
        self.alive[:] = False
        self.total_absorbed = 0

        rs = self.config.rs
        inner_r = self.config.disk_inner_radius
        outer_r = self.config.disk_outer_radius

        p, v, ang, avel, life, sc, tok = self.emitter.spawn_batch(
            self.target_count,
            inner_r,
            outer_r,
            self.config.black_hole_mass,
            rs,
            self.config.rotation_direction,
            spawn_at_outer_rim=False,
            scale_height_ratio=self.config.disk_scale_height_ratio
        )

        n = len(p)
        if n > 0:
            self.pos[:n] = p
            self.vel[:n] = v
            self.angles[:n] = ang
            self.angular_vel[:n] = avel
            self.lifetime[:n] = life
            self.scale[:n] = sc
            self.age[:n] = 0.0
            self.alive[:n] = True
            self.alpha[:n] = 0.8
            self.tokens[:n] = tok

    def set_target_count(self, count: int) -> None:
        """Adjust the active particle target count dynamically."""
        self.target_count = max(50, min(self.capacity, int(count)))

    def refresh_typography(self) -> None:
        """Update all active particle tokens when typography mode or vocabulary changes."""
        for i in range(self.capacity):
            if self.alive[i]:
                self.tokens[i] = self.text_provider.get_token()

    def update(self, dt: float, elapsed_time: float) -> Tuple[int, int]:
        """Advance the particle simulation by dt seconds."""
        rs = self.config.rs
        isco = self.config.isco_radius
        outer_r = self.config.disk_outer_radius

        # Vectorized update
        radii, newly_absorbed_mask, newly_absorbed = update_particles_vectorized(
            self.pos,
            self.vel,
            self.angles,
            self.angular_vel,
            self.alive,
            self.age,
            self.lifetime,
            self.alpha,
            self.config.black_hole_mass,
            rs,
            isco,
            outer_r,
            self.config.rotation_speed,
            self.config.rotation_direction,
            self.config.turbulence_factor,
            dt,
            elapsed_time
        )
        self.radii = radii
        self.total_absorbed += newly_absorbed

        # Count active particles
        active_indices = np.where(self.alive)[0]
        active_count = len(active_indices)

        # Replenish dead slots to maintain target particle count
        deficit = self.target_count - active_count
        if deficit > 0:
            dead_indices = np.where(~self.alive)[0]
            spawn_count = min(deficit, len(dead_indices))
            if spawn_count > 0:
                slots = dead_indices[:spawn_count]
                p, v, ang, avel, life, sc, tok = self.emitter.spawn_batch(
                    spawn_count,
                    self.config.disk_inner_radius,
                    outer_r,
                    self.config.black_hole_mass,
                    rs,
                    self.config.rotation_direction,
                    spawn_at_outer_rim=True,
                    scale_height_ratio=self.config.disk_scale_height_ratio
                )
                self.pos[slots] = p
                self.vel[slots] = v
                self.angles[slots] = ang
                self.angular_vel[slots] = avel
                self.lifetime[slots] = life
                self.scale[slots] = sc
                self.age[slots] = 0.0
                self.alive[slots] = True
                self.alpha[slots] = 0.5
                for idx, slot in enumerate(slots):
                    self.tokens[slot] = tok[idx]

        return active_count, newly_absorbed
