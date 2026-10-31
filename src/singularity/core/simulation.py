"""Master simulation coordinator managing physics state, particle pools, and typography."""

import random
from typing import Tuple
import numpy as np

from singularity.core.config import EngineConfig, COLOR_PRESETS
from singularity.core.state import EngineState
from singularity.particles.system import ParticleSystem
from singularity.typography.arabic import ArabicTextProvider, TypographyMode


class BlackHoleSimulation:
    """Manages the physics state, particle system, and astrophysical updates."""

    def __init__(self, config: EngineConfig, state: EngineState):
        self.config = config
        self.state = state

        # Initialize typography provider
        mode = TypographyMode(config.typography_mode) if config.typography_mode in [m.value for m in TypographyMode] else TypographyMode.MIXED
        self.text_provider = ArabicTextProvider(mode=mode, custom_words=config.custom_words)

        # Initialize particle system
        self.particle_system = ParticleSystem(config, self.text_provider)

    def reset(self) -> None:
        """Reset the simulation to its initial state."""
        self.particle_system.initialize_pool()
        self.state.elapsed_time = 0.0
        self.state.frame_count = 0
        self.state.notify("Simulation Reset")

    def randomize(self) -> None:
        """Randomize celestial parameters for generative exploration while preserving unified Rs scaling."""
        self.config.rs = float(random.randint(8, 18))
        self.config.event_horizon_radius = 1.0 * self.config.rs
        self.config.photon_sphere_radius = 1.5 * self.config.rs
        self.config.isco_radius = 3.0 * self.config.rs
        self.config.disk_inner_radius = 3.0 * self.config.rs
        self.config.disk_outer_radius = float(random.randint(16, 22)) * self.config.rs
        self.config.black_hole_mass = self.config.rs * float(random.randint(280, 420))
        self.config.rotation_speed = round(random.uniform(0.7, 1.6), 2)
        self.config.turbulence_factor = round(random.uniform(0.03, 0.09), 3)

        palette_keys = list(COLOR_PRESETS.keys())
        self.config.color_preset = random.choice(palette_keys)

        modes = list(TypographyMode)
        new_mode = random.choice(modes)
        self.config.typography_mode = new_mode.value
        self.text_provider.set_mode(new_mode)

        self.particle_system.initialize_pool()
        self.state.notify("Scene Randomized")

    def step(self, dt: float) -> Tuple[int, int]:
        """Advance the astrophysical simulation by dt seconds.

        Returns:
            (active_particles_count, newly_absorbed_count)
        """
        # Handle deferred triggers
        if self.state.reset_requested:
            self.state.reset_requested = False
            self.reset()
            return sum(self.particle_system.alive), 0

        if self.state.randomize_requested:
            self.state.randomize_requested = False
            self.randomize()
            return sum(self.particle_system.alive), 0

        self.state.update_timers(dt)

        if self.state.is_paused:
            return sum(self.particle_system.alive), 0

        effective_dt = dt * self.state.time_scale
        self.state.elapsed_time += effective_dt
        self.state.frame_count += 1

        active_count, absorbed_count = self.particle_system.update(effective_dt, self.state.elapsed_time)
        self.state.newly_absorbed_count = absorbed_count
        return active_count, absorbed_count

