"""Master engine orchestrating event dispatch, rendering, and interactive controls."""

import datetime
import os
import sys
from typing import Optional
import pygame

from singularity.core.config import EngineConfig, COLOR_PRESETS, QUALITY_PRESETS
from singularity.core.state import EngineState
from singularity.core.simulation import BlackHoleSimulation
from singularity.rendering.renderer import SingularityRenderer
from singularity.typography.fonts import FontManager
from singularity.typography.arabic import TypographyMode
from singularity.ui.panel import ControlPanel
from singularity.ui.overlay import HUDOverlay
from singularity.utilities.profiler import FrameProfiler


class SingularityEngine:
    """The central application engine of SINGULARITY."""

    def __init__(self, config: Optional[EngineConfig] = None, config_path: str = "config.json"):
        if not pygame.get_init():
            pygame.init()

        self.config_path = config_path
        self.config = config if config is not None else EngineConfig.load_from_file(config_path)
        self.state = EngineState()
        self.profiler = FrameProfiler()

        # Display window
        flags = pygame.DOUBLEBUF | pygame.RESIZABLE
        if self.config.fullscreen:
            flags |= pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height),
            flags
        )
        pygame.display.set_caption("SINGULARITY // Arabic Gravitational Art Engine")

        # Bring window to foreground on Windows desktop
        try:
            import ctypes
            wm_info = pygame.display.get_wm_info()
            hwnd = wm_info.get("window")
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 5)
                ctypes.windll.user32.SetForegroundWindow(hwnd)
        except Exception:
            pass

        # Fonts and subsystems
        self.font_manager = FontManager(self.config.font_path)
        self.simulation = BlackHoleSimulation(self.config, self.state)
        self.renderer = SingularityRenderer(self.config, self.font_manager)
        self.hud_overlay = HUDOverlay()

        self.control_panel = ControlPanel(
            self.config,
            self.state,
            self.simulation.particle_system,
            on_typography_change=self.simulation.particle_system.refresh_typography,
            on_save_config=self.save_configuration
        )

        self.clock = pygame.time.Clock()
        self.is_running = True

    def save_configuration(self) -> None:
        """Persist current configuration settings to disk."""
        self.config.save_to_file(self.config_path)

    def capture_screenshot(self) -> None:
        """Save a pristine high-resolution capture of the generative black hole scene."""
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(screenshots_dir, f"singularity_{timestamp}.png")
        pygame.image.save(self.screen, file_path)
        self.state.notify(f"Screenshot Captured: {os.path.basename(file_path)}")

    def toggle_cinematic_mode(self) -> None:
        """Toggle autonomous 360-degree cinematic flyby orbit."""
        self.state.cinematic_mode = not self.state.cinematic_mode
        if self.state.cinematic_mode:
            self.state.notify("Cinematic Auto-Tour: ACTIVE [Press C to stop]")
        else:
            self.state.notify("Cinematic Auto-Tour: STOPPED")

    def _cycle_typography_mode(self) -> None:
        modes = list(TypographyMode)
        curr_idx = 0
        for i, m in enumerate(modes):
            if m.value == self.config.typography_mode:
                curr_idx = i
                break
        next_mode = modes[(curr_idx + 1) % len(modes)]
        self.config.typography_mode = next_mode.value
        self.simulation.text_provider.set_mode(next_mode)
        self.simulation.particle_system.refresh_typography()
        self.state.notify(f"Typography: {next_mode.value.upper()}")

    def _cycle_quality_preset(self) -> None:
        presets = ["LOW", "MEDIUM", "HIGH"]
        curr_idx = presets.index(self.config.quality_preset) if self.config.quality_preset in presets else 1
        next_quality = presets[(curr_idx + 1) % len(presets)]
        self.config.apply_quality_preset(next_quality)
        self.simulation.particle_system.set_target_count(self.config.max_particles)
        self.state.notify(f"Quality Preset: {next_quality}")

    def handle_events(self) -> None:
        """Poll and process user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return

            elif event.type == pygame.VIDEORESIZE:
                new_w, new_h = event.w, event.h
                self.config.window_width = new_w
                self.config.window_height = new_h
                self.screen = pygame.display.set_mode((new_w, new_h), pygame.DOUBLEBUF | pygame.RESIZABLE)
                self.renderer.resize(new_w, new_h)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                    return
                elif event.key == pygame.K_SPACE:
                    self.state.is_paused = not self.state.is_paused
                    self.state.notify("Simulation Paused" if self.state.is_paused else "Simulation Resumed")
                elif event.key == pygame.K_r:
                    self.simulation.reset()
                elif event.key == pygame.K_h:
                    self.state.ui_visible = not self.state.ui_visible
                elif event.key == pygame.K_F11:
                    self.config.fullscreen = not self.config.fullscreen
                    flags = pygame.DOUBLEBUF | pygame.RESIZABLE
                    if self.config.fullscreen:
                        flags |= pygame.FULLSCREEN
                    self.screen = pygame.display.set_mode((self.config.window_width, self.config.window_height), flags)
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    self.config.camera_zoom = min(2.5, self.config.camera_zoom + 0.1)
                    self.renderer.camera.target_zoom = self.config.camera_zoom
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self.config.camera_zoom = max(0.4, self.config.camera_zoom - 0.1)
                    self.renderer.camera.target_zoom = self.config.camera_zoom
                elif event.key in (pygame.K_p, pygame.K_F12):
                    self.capture_screenshot()
                elif event.key == pygame.K_t:
                    self._cycle_typography_mode()
                elif event.key == pygame.K_q:
                    self._cycle_quality_preset()
                elif event.key == pygame.K_c:
                    self.toggle_cinematic_mode()
                elif event.key == pygame.K_1:
                    self.config.color_preset = "solar_orange"
                    self.state.notify("Palette: Solar Orange")
                elif event.key == pygame.K_2:
                    self.config.color_preset = "deep_blue"
                    self.state.notify("Palette: Deep Blue")
                elif event.key == pygame.K_3:
                    self.config.color_preset = "purple_nebula"
                    self.state.notify("Palette: Purple Nebula")
                elif event.key == pygame.K_4:
                    self.config.color_preset = "monochrome_white"
                    self.state.notify("Palette: Monochrome Gravitational")
                elif event.key == pygame.K_5:
                    self.config.color_preset = "emerald_singularity"
                    self.state.notify("Palette: Emerald Singularity")

            # UI Event interception
            if self.state.ui_visible and self.config.show_ui:
                if self.control_panel.handle_event(event):
                    continue

            # Orbit camera mouse controls
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):  # Left or Right drag
                    self.state.is_mouse_dragging = True
                    self.state.last_mouse_pos = event.pos
                    if self.state.cinematic_mode:
                        self.state.cinematic_mode = False
                        self.state.notify("Manual Camera Control (Auto-Tour Paused)")
                elif event.button == 4:  # Wheel up
                    self.config.camera_zoom = min(2.5, self.config.camera_zoom + 0.08)
                    self.renderer.camera.target_zoom = self.config.camera_zoom
                elif event.button == 5:  # Wheel down
                    self.config.camera_zoom = max(0.4, self.config.camera_zoom - 0.08)
                    self.renderer.camera.target_zoom = self.config.camera_zoom

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    self.state.is_mouse_dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if self.state.is_mouse_dragging:
                    dx = event.pos[0] - self.state.last_mouse_pos[0]
                    dy = event.pos[1] - self.state.last_mouse_pos[1]
                    self.state.last_mouse_pos = event.pos

                    # Orbit camera yaw and pitch
                    self.renderer.camera.target_yaw += dx * 0.006
                    self.renderer.camera.target_pitch = max(
                        -1.4, min(1.4, self.renderer.camera.target_pitch + dy * 0.006)
                    )

        # Smooth keyboard arrow camera orbit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.renderer.camera.target_yaw -= 0.03
        if keys[pygame.K_RIGHT]:
            self.renderer.camera.target_yaw += 0.03
        if keys[pygame.K_UP]:
            self.renderer.camera.target_pitch = min(1.4, self.renderer.camera.target_pitch - 0.03)
        if keys[pygame.K_DOWN]:
            self.renderer.camera.target_pitch = max(-1.4, self.renderer.camera.target_pitch + 0.03)

    def run(self) -> None:
        """Run the main rendering and simulation loop."""
        while self.is_running:
            self.profiler.start_frame()
            dt = self.clock.tick(self.config.target_fps) / 1000.0
            dt_clamped = min(dt, 0.1)

            # Input processing
            self.handle_events()

            # Physics simulation step
            self.simulation.step(dt_clamped)

            # Cinematic auto-tour camera dynamics
            if self.state.cinematic_mode:
                self.state.cinematic_timer += dt_clamped
                t = self.state.cinematic_timer
                # Continuous 360-degree orbital rotation
                self.renderer.camera.target_yaw += dt_clamped * 0.22
                # Smooth sinusoidal pitch oscillation between ~0.20 rad (edge-on) and ~1.15 rad (face-on)
                import numpy as np
                self.renderer.camera.target_pitch = 0.68 + 0.48 * float(np.sin(t * 0.18))
                # Subtle orbital breathing zoom
                self.renderer.camera.target_zoom = 1.05 + 0.20 * float(np.cos(t * 0.12))

            # Camera smoothing
            self.renderer.camera.update(dt_clamped)

            # Render scene
            self.renderer.render(
                self.screen,
                self.simulation.particle_system,
                self.state,
                self.profiler
            )

            # UI & Telemetry Overlay
            if self.state.ui_visible and self.config.show_ui:
                self.control_panel.draw(self.screen)
                self.hud_overlay.draw(
                    self.screen,
                    self.config,
                    self.state,
                    self.simulation.particle_system,
                    self.profiler
                )

            pygame.display.flip()

        pygame.quit()

