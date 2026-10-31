"""Master rendering engine coordinating the multi-pass relativistic visual pipeline."""

from typing import Tuple, Dict, Any, Optional
import pygame

from singularity.core.config import EngineConfig, COLOR_PRESETS
from singularity.core.state import EngineState
from singularity.particles.system import ParticleSystem
from singularity.rendering.camera import Camera3D
from singularity.rendering.character_renderer import CharacterRenderer
from singularity.rendering.star_renderer import StarRenderer
from singularity.rendering.effects import BloomEffect, EventHorizonRenderer
from singularity.typography.fonts import FontManager, GlyphCache
from singularity.utilities.profiler import FrameProfiler


class SingularityRenderer:
    """Coordinates multi-pass rendering of the relativistic Arabic black hole scene."""

    def __init__(self, config: EngineConfig, font_manager: FontManager):
        self.config = config
        self.font_manager = font_manager
        self.glyph_cache = GlyphCache(font_manager)

        self.camera = Camera3D(
            viewport_width=config.window_width,
            viewport_height=config.window_height,
            pitch=config.camera_pitch,
            yaw=config.camera_yaw,
            zoom=config.camera_zoom,
            camera_distance=config.camera_distance,
            fov_degrees=config.camera_fov
        )

        self.star_renderer = StarRenderer(config)
        self.character_renderer = CharacterRenderer(config, self.glyph_cache)
        self.event_horizon_renderer = EventHorizonRenderer()
        self.bloom_effect = BloomEffect(
            config.window_width,
            config.window_height,
            downsample_factor=2
        )

        # Persistent motion blur trail canvas
        self.trail_surface = pygame.Surface(
            (config.window_width, config.window_height)
        ).convert()
        self.trail_surface.fill((0, 0, 0))

    def resize(self, width: int, height: int) -> None:
        """Handle window resize event and adjust framebuffers."""
        self.camera.set_viewport(width, height)
        self.star_renderer.resize(width, height)
        self.bloom_effect.resize(width, height)
        self.trail_surface = pygame.Surface((width, height)).convert()
        self.trail_surface.fill((0, 0, 0))

    def render(
        self,
        target_surface: pygame.Surface,
        particle_system: ParticleSystem,
        state: EngineState,
        profiler: Optional[FrameProfiler] = None
    ) -> None:
        """Execute the full multi-pass rendering pipeline."""
        color_preset = COLOR_PRESETS.get(self.config.color_preset, COLOR_PRESETS["solar_orange"])
        einstein_px = self.camera.get_projected_screen_radius(self.config.rs * 1.55)
        center_xy = (self.camera.center_x, self.camera.center_y)

        # ----------------------------------------------------
        # Stage 1: Background & Motion Blur Trails
        # ----------------------------------------------------
        if profiler:
            profiler.start_stage("background")

        if self.config.show_trails:
            fade_amount = max(6, min(36, self.config.motion_blur_alpha // 2))
            self.trail_surface.fill((fade_amount, fade_amount, fade_amount), special_flags=pygame.BLEND_SUB)
        else:
            self.trail_surface.fill((0, 0, 0))

        if profiler:
            profiler.end_stage("background")

        # ----------------------------------------------------
        # Stage 2: Background Stars with Gravitational Lensing
        # ----------------------------------------------------
        if profiler:
            profiler.start_stage("stars")

        if self.config.show_stars:
            self.star_renderer.render(
                self.trail_surface,
                center_xy,
                self.camera.yaw,
                self.camera.pitch,
                einstein_px,
                state.elapsed_time,
                color_preset
            )

        if profiler:
            profiler.end_stage("stars")

        # ----------------------------------------------------
        # Prepare particles (single projection, lensing, and partition pass)
        # ----------------------------------------------------
        if self.config.show_particles:
            coords, depths, bg_idx, fg_idx, colors, intensity = self.character_renderer.prepare_frame(
                particle_system,
                self.camera,
                color_preset
            )
        else:
            bg_idx, fg_idx = [], []

        # ----------------------------------------------------
        # Stage 3: Back-Side Accretion Disk Particles
        # ----------------------------------------------------
        if profiler:
            profiler.start_stage("disk_back")

        if self.config.show_particles and len(bg_idx) > 0:
            self.character_renderer.render_subset(
                self.trail_surface,
                particle_system,
                self.camera,
                bg_idx,
                coords,
                depths,
                colors,
                intensity
            )

        if profiler:
            profiler.end_stage("disk_back")

        # ----------------------------------------------------
        # Stage 4: Central Black Hole Shadow & Photon Sphere
        # ----------------------------------------------------
        if profiler:
            profiler.start_stage("black_hole")

        if self.config.show_black_hole:
            self.event_horizon_renderer.render(
                self.trail_surface,
                center_xy,
                self.camera,
                self.config.rs,
                self.config.photon_sphere_radius,
                color_preset,
                show_photon_ring=self.config.show_photon_ring
            )

        if profiler:
            profiler.end_stage("black_hole")

        # ----------------------------------------------------
        # Stage 5: Front-Side Accretion Disk Particles
        # ----------------------------------------------------
        if profiler:
            profiler.start_stage("disk_front")

        if self.config.show_particles and len(fg_idx) > 0:
            self.character_renderer.render_subset(
                self.trail_surface,
                particle_system,
                self.camera,
                fg_idx,
                coords,
                depths,
                colors,
                intensity
            )

        if profiler:
            profiler.end_stage("disk_front")

        # Copy trail surface to display surface
        target_surface.blit(self.trail_surface, (0, 0))

        # ----------------------------------------------------
        # Stage 6: Post-Processing Additive Bloom
        # ----------------------------------------------------
        if profiler:
            profiler.start_stage("post_processing")

        if self.config.show_glow and self.config.glow_intensity > 0.05:
            self.bloom_effect.apply_bloom(
                self.trail_surface,
                target_surface,
                intensity=self.config.glow_intensity
            )

        if profiler:
            profiler.end_stage("post_processing")
