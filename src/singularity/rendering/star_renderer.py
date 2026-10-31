"""Multi-layer cosmic starfield with gravitational lensing deflection and scintillation."""

from typing import Tuple, Dict, Any
import numpy as np
import pygame

from singularity.core.config import EngineConfig, COLOR_PRESETS
from singularity.physics.lensing import deflect_stars


class StarRenderer:
    """Renders background stars subjected to gravitational light bending and parallax."""

    def __init__(self, config: EngineConfig):
        self.config = config
        self.count = config.star_count
        self._init_stars(config.window_width, config.window_height)

    def _init_stars(self, width: int, height: int) -> None:
        """Initialize procedural star attributes."""
        if self.count <= 0:
            self.positions = np.empty((0, 2), dtype=np.float32)
            self.depths = np.empty((0,), dtype=np.float32)
            self.phases = np.empty((0,), dtype=np.float32)
            self.speeds = np.empty((0,), dtype=np.float32)
            self.sizes = np.empty((0,), dtype=np.int32)
            return

        # Generate stars distributed across a wide virtual canvas
        margin = 300.0
        self.positions = np.column_stack((
            np.random.uniform(-margin, width + margin, size=self.count),
            np.random.uniform(-margin, height + margin, size=self.count)
        )).astype(np.float32)

        self.depths = np.random.uniform(0.3, 1.0, size=self.count).astype(np.float32)
        self.phases = np.random.uniform(0.0, 2.0 * np.pi, size=self.count).astype(np.float32)
        self.speeds = np.random.uniform(0.8, 2.5, size=self.count).astype(np.float32)
        self.sizes = np.random.choice([1, 1, 1, 2, 3], size=self.count, p=[0.70, 0.15, 0.08, 0.05, 0.02]).astype(np.int32)

    def resize(self, width: int, height: int) -> None:
        """Re-generate starfield for new window dimensions."""
        self._init_stars(width, height)

    def render(
        self,
        surface: pygame.Surface,
        center_xy: Tuple[float, float],
        camera_yaw: float,
        camera_pitch: float,
        einstein_radius: float,
        elapsed_time: float,
        color_preset: Dict[str, Any]
    ) -> None:
        """Render all background stars with gravitational deflection and twinkling."""
        if len(self.positions) == 0:
            return

        width, height = surface.get_size()
        cx, cy = center_xy

        # Subtle parallax shift based on camera angle and star depth
        parallax_x = -camera_yaw * 80.0 * self.depths
        parallax_y = -camera_pitch * 80.0 * self.depths

        shifted_pos = np.column_stack((
            self.positions[:, 0] + parallax_x,
            self.positions[:, 1] + parallax_y
        ))

        # Gravitational lensing deflection
        if self.config.show_lensing and self.config.lensing_intensity > 0.01:
            screen_coords, magnification = deflect_stars(
                shifted_pos,
                (cx, cy),
                einstein_radius,
                intensity=self.config.lensing_intensity
            )
        else:
            screen_coords = shifted_pos
            magnification = np.ones((len(shifted_pos),), dtype=np.float32)

        # Scintillation (twinkle) calculation
        twinkle = 0.65 + 0.35 * np.sin(self.phases + elapsed_time * self.speeds * self.config.star_twinkle_speed)
        brightness = np.clip(twinkle * magnification, 0.1, 2.5)

        base_tint = color_preset.get("bg_star_tint", (255, 240, 220))
        rs_event = self.config.event_horizon_radius

        # Fast blit or circle draw
        for i in range(len(screen_coords)):
            sx = screen_coords[i, 0]
            sy = screen_coords[i, 1]

            # Cull off-screen stars
            if sx < -5 or sx > width + 5 or sy < -5 or sy > height + 5:
                continue

            # Cull stars that land inside the event horizon shadow
            dist_to_center = np.hypot(sx - cx, sy - cy)
            if dist_to_center <= rs_event:
                continue

            b = brightness[i]
            r = min(255, int(base_tint[0] * b))
            g = min(255, int(base_tint[1] * b))
            blue = min(255, int(base_tint[2] * b))
            star_color = (r, g, blue)

            sz = self.sizes[i]
            if sz == 1:
                surface.set_at((int(sx), int(sy)), star_color)
            else:
                pygame.draw.circle(surface, star_color, (int(sx), int(sy)), sz)

