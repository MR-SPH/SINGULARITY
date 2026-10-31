"""Heads-Up Display (HUD) overlay: Scientific telemetry, hotkeys, and status notifications."""

from typing import Dict, Any, Optional
import numpy as np
import pygame

from singularity.core.config import EngineConfig, COLOR_PRESETS
from singularity.core.state import EngineState
from singularity.particles.system import ParticleSystem
from singularity.utilities.profiler import FrameProfiler


class HUDOverlay:
    """Renders scientific telemetry, performance stats, and shortcuts bar."""

    def __init__(self):
        self._font_title = pygame.font.SysFont("segoe ui,tahoma,arial", 16, bold=True)
        self._font_body = pygame.font.SysFont("consolas,monospace,segoe ui", 12)
        self._font_notify = pygame.font.SysFont("segoe ui,tahoma,arial", 15, bold=True)

    def draw(
        self,
        surface: pygame.Surface,
        config: EngineConfig,
        state: EngineState,
        particle_system: ParticleSystem,
        profiler: Optional[FrameProfiler]
    ) -> None:
        """Render HUD telemetry, status notifications, and help hints."""
        width, height = surface.get_size()

        # ----------------------------------------------------
        # 1. Top-Right Telemetry Box
        # ----------------------------------------------------
        fps = profiler.current_fps if profiler else 60.0
        frame_time = profiler.average_frame_time_ms if profiler else 16.6

        fps_color = (100, 255, 120) if fps >= 50 else ((255, 210, 60) if fps >= 30 else (255, 80, 80))

        active_particles = sum(particle_system.alive)
        absorbed_total = particle_system.total_absorbed

        r_in_rs = config.disk_inner_radius / max(config.rs, 1.0)
        r_out_rs = config.disk_outer_radius / max(config.rs, 1.0)

        lines = [
            ("SINGULARITY // UNIFIED 3D SCALE", (255, 180, 50)),
            (f"FPS: {fps:.1f} ({frame_time:.1f} ms)", fps_color),
            (f"Particles: {active_particles} / {particle_system.target_count}", (200, 215, 235)),
            (f"Absorbed: {absorbed_total}", (235, 120, 120)),
            (f"Scale: Rs = {config.rs:.1f} | ISCO = 3.0 Rs", (180, 195, 215)),
            (f"Disk Span: [{r_in_rs:.1f} - {r_out_rs:.1f}] Rs", (170, 210, 235)),
            (f"Preset: {config.color_preset.replace('_', ' ').title()}", (220, 230, 245)),
            (f"Quality: {config.quality_preset}", (160, 220, 255))
        ]

        if state.cinematic_mode:
            lines.insert(1, ("MODE: CINEMATIC AUTO-TOUR [C]", (120, 225, 255)))

        box_w = 275
        box_h = len(lines) * 20 + 16
        box_x = width - box_w - 15
        box_y = 15

        hud_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        hud_surf.fill((12, 16, 22, 205))
        pygame.draw.rect(hud_surf, (50, 65, 85), (0, 0, box_w, box_h), width=1, border_radius=6)

        curr_y = 10
        for text, col in lines:
            rendered = self._font_body.render(text, True, col)
            hud_surf.blit(rendered, (14, curr_y))
            curr_y += 20

        surface.blit(hud_surf, (box_x, box_y))

        # ----------------------------------------------------
        # 2. Bottom Keyboard Shortcuts Bar
        # ----------------------------------------------------
        bar_text = "[SPACE] Pause | [C] Cinematic Tour | [R] Reset | [F11] Fullscreen | [H] HUD | [1-5] Palettes | [Arrows/Mouse] Orbit"
        bar_surf = self._font_body.render(bar_text, True, (140, 155, 175))
        bx = (width - bar_surf.get_width()) // 2
        by = height - 26

        bar_bg = pygame.Surface((bar_surf.get_width() + 24, 22), pygame.SRCALPHA)
        bar_bg.fill((10, 14, 20, 180))
        pygame.draw.rect(bar_bg, (40, 50, 65), (0, 0, bar_bg.get_width(), 22), width=1, border_radius=4)
        surface.blit(bar_bg, (bx - 12, by - 2))
        surface.blit(bar_surf, (bx, by))

        # ----------------------------------------------------
        # 3. Status Notification Banner
        # ----------------------------------------------------
        if state.status_notification and state.notification_timer > 0.0:
            notify_surf = self._font_notify.render(state.status_notification, True, (255, 235, 160))
            nw = notify_surf.get_width() + 40
            nh = 34
            nx = (width - nw) // 2
            ny = 50

            alpha = min(255, int(state.notification_timer * 180.0))
            banner_surf = pygame.Surface((nw, nh), pygame.SRCALPHA)
            banner_surf.fill((25, 28, 38, min(230, alpha)))
            pygame.draw.rect(banner_surf, (255, 180, 50, alpha), (0, 0, nw, nh), width=1, border_radius=6)
            notify_surf.set_alpha(alpha)
            banner_surf.blit(notify_surf, (20, 6))

            surface.blit(banner_surf, (nx, ny))
