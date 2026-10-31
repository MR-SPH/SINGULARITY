"""Unit tests for the Struct-of-Arrays particle pool, emitter, and lifecycle."""

import numpy as np
import pytest

from singularity.core.config import EngineConfig
from singularity.particles.system import ParticleSystem
from singularity.particles.emitter import DiskEmitter
from singularity.typography.arabic import ArabicTextProvider, TypographyMode


class TestParticleSystem:
    """Validate particle pool allocations, updates, and absorption."""

    def setup_method(self):
        self.config = EngineConfig(max_particles=500)
        self.provider = ArabicTextProvider(mode=TypographyMode.LETTERS)
        self.system = ParticleSystem(self.config, self.provider, max_capacity=1000)

    def test_pool_initialization(self):
        active_count = sum(self.system.alive)
        assert active_count == 500
        assert len(self.system.pos) == 1000
        assert len(self.system.tokens) == 1000

    def test_particle_attributes_shape(self):
        assert self.system.pos.shape == (1000, 3)
        assert self.system.vel.shape == (1000, 3)
        assert self.system.angles.shape == (1000,)
        assert self.system.scale.shape == (1000,)
        assert self.system.alpha.shape == (1000,)

    def test_target_count_scaling(self):
        self.system.set_target_count(750)
        assert self.system.target_count == 750

    def test_event_horizon_absorption(self):
        # Force a particle inside the event horizon radius
        rs = self.config.event_horizon_radius
        self.system.pos[0] = np.array([rs * 0.5, 0.0, 0.0], dtype=np.float32)
        self.system.alive[0] = True

        active, absorbed = self.system.update(0.1, 1.0)
        # The particle should have been absorbed
        assert self.system.total_absorbed >= 1

    def test_emitter_batch_generation(self):
        emitter = DiskEmitter(self.provider)
        count = 100
        p, v, ang, avel, life, sc, tok = emitter.spawn_batch(
            count,
            inner_radius=70.0,
            outer_radius=300.0,
            black_hole_mass=3000.0,
            rs=50.0,
            rotation_direction=1.0
        )
        assert len(p) == count
        assert len(v) == count
        assert len(tok) == count
        # Radii should fall between inner and outer bounds
        radii = np.hypot(p[:, 0], p[:, 2])
        assert np.all(radii >= 69.0)
        assert np.all(radii <= 301.0)

