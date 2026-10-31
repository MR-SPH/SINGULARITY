"""Renders Arabic typography particles with perspective, Doppler beaming, and depth occlusion."""

from typing import Tuple, Dict, Any, List
import numpy as np
import pygame

from singularity.core.config import EngineConfig
from singularity.particles.system import ParticleSystem
from singularity.physics.orbital_motion import (
    compute_doppler_beaming,
    compute_thin_disk_temperature,
    compute_gravitational_redshift
)
from singularity.physics.lensing import deflect_far_disk_screen_coords
from singularity.rendering.camera import Camera3D
from singularity.typography.fonts import GlyphCache
from singularity.utilities.math_utils import clamp


class CharacterRenderer:
    """Projects, colors, and blits Arabic character particles onto the scene."""

    def __init__(self, config: EngineConfig, glyph_cache: GlyphCache):
        self.config = config
        self.glyph_cache = glyph_cache

    def compute_all_colors(
        self,
        radii: np.ndarray,
        inner_r: float,
        outer_r: float,
        rs: float,
        doppler_factors: np.ndarray,
        color_preset: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Vectorized color and flux computation using Shakura-Sunyaev T(r), Doppler, and redshift."""
        n = len(radii)
        if n == 0:
            return np.empty((0, 3), dtype=np.uint8), np.empty((0,), dtype=np.float32)

        # 1. Shakura-Sunyaev normalized temperature T(r) in [0, 1]
        temps = compute_thin_disk_temperature(radii, inner_r, rs)

        # 2. Gravitational redshift attenuation factor sqrt(1 - Rs / r)
        redshift = compute_gravitational_redshift(radii, rs)

        core_c = np.array(color_preset.get("core_color", (255, 255, 255)), dtype=np.float32)
        inner_c = np.array(color_preset.get("inner_disk_color", (255, 220, 100)), dtype=np.float32)
        mid_c = np.array(color_preset.get("mid_disk_color", (255, 120, 25)), dtype=np.float32)
        outer_c = np.array(color_preset.get("outer_disk_color", (180, 25, 5)), dtype=np.float32)
        ionization_c = np.array([205, 240, 255], dtype=np.float32)

        colors = np.zeros((n, 3), dtype=np.float32)

        # Map temperature to blackbody color gradient
        # High T -> Core white/gold; Mid T -> Solar orange; Low T -> Deep red
        t_high = temps > 0.65
        if np.any(t_high):
            frac = ((temps[t_high] - 0.65) / 0.35)[:, np.newaxis]
            colors[t_high] = inner_c + (core_c - inner_c) * frac
            # Add subtle ultraviolet/cyan tint to the hottest peak
            super_hot = temps > 0.88
            if np.any(super_hot):
                colors[super_hot] = colors[super_hot] * 0.82 + ionization_c * 0.18

        t_mid = (temps >= 0.25) & (temps <= 0.65)
        if np.any(t_mid):
            frac = ((temps[t_mid] - 0.25) / 0.40)[:, np.newaxis]
            colors[t_mid] = mid_c + (inner_c - mid_c) * frac

        t_low = temps < 0.25
        if np.any(t_low):
            frac = (temps[t_low] / 0.25)[:, np.newaxis]
            colors[t_low] = outer_c + (mid_c - outer_c) * frac

        # Relativistic Doppler beaming boost
        boost_mask = doppler_factors > 1.05
        if np.any(boost_mask):
            boost_t = np.clip((doppler_factors[boost_mask] - 1.0) * 0.45, 0.0, 0.9)[:, np.newaxis]
            colors[boost_mask] = colors[boost_mask] + (core_c - colors[boost_mask]) * boost_t

        dim_mask = doppler_factors < 0.92
        if np.any(dim_mask):
            dim_f = np.clip(doppler_factors[dim_mask] * 0.95, 0.25, 1.0)[:, np.newaxis]
            colors[dim_mask] *= dim_f

        # Gravitational redshift dimming near the event horizon
        colors *= redshift[:, np.newaxis]

        # Total intensity factor for alpha modulation
        intensity = np.clip((0.35 + 0.65 * temps) * doppler_factors * redshift, 0.05, 3.5)

        # Quantize colors to 32-unit increments for instant glyph cache hits
        quantized = (np.clip(colors, 0.0, 255.0) // 32) * 32
        return np.clip(quantized, 0, 255).astype(np.uint8), intensity.astype(np.float32)

    def prepare_frame(
        self,
        particle_system: ParticleSystem,
        camera: Camera3D,
        color_preset: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Compute spatial projections, Doppler beaming, and depth partitioning once per frame."""
        alive_mask = particle_system.alive
        if not np.any(alive_mask):
            empty = np.empty((0,), dtype=np.int32)
            return (
                np.empty((0, 2), dtype=np.float32),
                np.empty((0,), dtype=np.float32),
                empty, empty,
                np.empty((0, 3), dtype=np.uint8),
                np.empty((0,), dtype=np.float32)
            )

        active_indices = np.where(alive_mask)[0]
        pos_active = particle_system.pos[active_indices]
        vel_active = particle_system.vel[active_indices]
        radii_active = particle_system.radii[active_indices]

        # 3D perspective projection with camera space coordinates
        screen_coords, depths, cam_space = camera.project_with_cam_space(pos_active)

        # Relativistic Doppler beaming
        cam_dir = camera.get_camera_direction()
        doppler_boost = compute_doppler_beaming(
            vel_active,
            cam_dir,
            beaming_intensity=self.config.doppler_beaming_factor
        )

        # Vectorized color and intensity calculation based on Shakura-Sunyaev T(r)
        colors, intensity = self.compute_all_colors(
            radii_active,
            self.config.disk_inner_radius,
            self.config.disk_outer_radius,
            self.config.rs,
            doppler_boost,
            color_preset
        )

        # Far-side gravitational lensing deflection:
        # Points with cam_z > camera.effective_distance are behind the central black hole plane
        is_far_side = cam_space[:, 2] > camera.effective_distance
        if self.config.show_lensing and self.config.lensing_intensity > 0.05:
            einstein_px = camera.get_projected_screen_radius(self.config.rs * 1.55)
            screen_coords = deflect_far_disk_screen_coords(
                screen_coords,
                (camera.center_x, camera.center_y),
                einstein_px,
                is_far_side,
                camera.pitch,
                intensity=self.config.lensing_intensity
            )

        # Depth sort (back to front)
        sort_order = np.argsort(-depths)
        sorted_depths = depths[sort_order]

        center_depth = camera.effective_distance
        is_behind = sorted_depths > center_depth

        bg_indices = sort_order[is_behind]
        fg_indices = sort_order[~is_behind]

        return screen_coords, depths, bg_indices, fg_indices, colors, intensity

    def render_subset(
        self,
        surface: pygame.Surface,
        particle_system: ParticleSystem,
        camera: Camera3D,
        indices_to_render: np.ndarray,
        screen_coords: np.ndarray,
        depths: np.ndarray,
        colors: np.ndarray,
        intensity: np.ndarray
    ) -> None:
        """Render a specific partition (background or foreground) of particles."""
        if len(indices_to_render) == 0:
            return

        alive_indices = np.where(particle_system.alive)[0]
        width, height = surface.get_size()
        char_world_size = self.config.character_world_size

        for sorted_idx in indices_to_render:
            sx = screen_coords[sorted_idx, 0]
            sy = screen_coords[sorted_idx, 1]

            # Screen-space bounding culling
            if sx < -35 or sx > width + 35 or sy < -35 or sy > height + 35:
                continue

            orig_slot = alive_indices[sorted_idx]
            token = particle_system.tokens[orig_slot]
            depth = depths[sorted_idx]
            scale_val = particle_system.scale[orig_slot]
            angle = particle_system.angles[orig_slot]

            # Strict 3D perspective font sizing:
            # font_size_px = focal_length * (world_size * scale) / cam_depth
            font_size = int(clamp((camera.focal_length * char_world_size * scale_val) / max(depth, 1.0), 10, 52))

            col_tuple = (int(colors[sorted_idx, 0]), int(colors[sorted_idx, 1]), int(colors[sorted_idx, 2]))

            glyph_surf = self.glyph_cache.get_rotated_glyph(token, font_size, col_tuple, angle)

            effective_alpha = int(clamp(particle_system.alpha[orig_slot] * intensity[sorted_idx] * 235, 20, 255))
            glyph_surf.set_alpha(effective_alpha)

            gw, gh = glyph_surf.get_size()
            surface.blit(glyph_surf, (int(sx - gw * 0.5), int(sy - gh * 0.5)))
