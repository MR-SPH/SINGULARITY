"""Collapsible glassmorphic control dock with categorized tabbed sections."""

from typing import List, Dict, Any, Callable
import numpy as np
import pygame

from singularity.core.config import EngineConfig, COLOR_PRESETS, QUALITY_PRESETS
from singularity.core.state import EngineState
from singularity.particles.system import ParticleSystem
from singularity.typography.arabic import TypographyMode
from singularity.ui.controls import (
    UISlider,
    UIButton,
    UIToggle,
    COLOR_BG_PANEL,
    COLOR_BORDER,
    COLOR_TEXT_TITLE,
    COLOR_ACCENT,
    COLOR_TRACK
)


class ControlPanel:
    """Collapsible floating side dock with tabbed categories for intuitive real-time control."""

    def __init__(
        self,
        config: EngineConfig,
        state: EngineState,
        particle_system: ParticleSystem,
        on_typography_change: Callable[[], None],
        on_save_config: Callable[[], None]
    ):
        self.config = config
        self.state = state
        self.particle_system = particle_system
        self.on_typography_change = on_typography_change
        self.on_save_config = on_save_config

        self.width = 320
        self.is_collapsed = False
        self.active_tab = "PHYSICS"  # "PHYSICS", "VISUALS", "LAYERS", "SYSTEM"
        self._font_small = pygame.font.SysFont("segoe ui,tahoma,arial", 12)
        self._font_title = pygame.font.SysFont("segoe ui,tahoma,arial", 14, bold=True)

        self._init_widgets()

    def _init_widgets(self) -> None:
        """Create controls partitioned into tabs."""
        x = 20
        w = self.width - 40

        # Tabs
        tab_w = (self.width - 40) // 4
        self.tab_buttons = [
            UIButton(pygame.Rect(20 + 0 * tab_w, 48, tab_w - 4, 26), "Physics", lambda: self._set_tab("PHYSICS")),
            UIButton(pygame.Rect(20 + 1 * tab_w, 48, tab_w - 4, 26), "Visuals", lambda: self._set_tab("VISUALS")),
            UIButton(pygame.Rect(20 + 2 * tab_w, 48, tab_w - 4, 26), "Layers", lambda: self._set_tab("LAYERS")),
            UIButton(pygame.Rect(20 + 3 * tab_w, 48, tab_w - 4, 26), "System", lambda: self._set_tab("SYSTEM"))
        ]

        # -------------------------------------------------------------------------
        # Tab 1: PHYSICS & PROPORTIONS
        # -------------------------------------------------------------------------
        self.physics_widgets = [
            UISlider(
                pygame.Rect(x, 110, w, 10), "Schwarzschild Rs",
                6.0, 24.0, self.config.rs, step=0.5,
                on_change=self._set_rs
            ),
            UISlider(
                pygame.Rect(x, 155, w, 10), "Disk Outer (Rs)",
                12.0, 32.0, self.config.disk_outer_radius / max(self.config.rs, 1.0), step=1.0, format_str="{:.0f} Rs",
                on_change=lambda v: setattr(self.config, "disk_outer_radius", float(v * self.config.rs))
            ),
            UISlider(
                pygame.Rect(x, 200, w, 10), "Disk Rotation Speed",
                0.0, 3.0, self.config.rotation_speed, step=0.05,
                on_change=lambda v: setattr(self.config, "rotation_speed", v)
            ),
            UISlider(
                pygame.Rect(x, 245, w, 10), "Doppler Beaming Boost",
                0.0, 2.5, self.config.doppler_beaming_factor, step=0.05,
                on_change=lambda v: setattr(self.config, "doppler_beaming_factor", v)
            ),
            UISlider(
                pygame.Rect(x, 290, w, 10), "Disk Turbulence",
                0.0, 0.20, self.config.turbulence_factor, step=0.01,
                on_change=lambda v: setattr(self.config, "turbulence_factor", v)
            ),
            UIButton(
                pygame.Rect(x, 335, w, 28), "Reverse Orbital Direction",
                self._toggle_rotation_direction
            )
        ]

        # -------------------------------------------------------------------------
        # Tab 2: VISUALS & TYPOGRAPHY
        # -------------------------------------------------------------------------
        btn_w = (w - 10) // 2
        self.visuals_widgets = [
            UISlider(
                pygame.Rect(x, 110, w, 10), "Active Particles",
                200, 4000, self.config.max_particles, step=50, format_str="{:.0f}",
                on_change=self._set_particle_count
            ),
            UISlider(
                pygame.Rect(x, 155, w, 10), "Character Scale",
                2.0, 8.0, self.config.character_world_size, step=0.2, format_str="{:.1f}",
                on_change=lambda v: setattr(self.config, "character_world_size", float(v))
            ),
            UISlider(
                pygame.Rect(x, 200, w, 10), "Lensing Intensity",
                0.0, 2.5, self.config.lensing_intensity, step=0.05,
                on_change=lambda v: setattr(self.config, "lensing_intensity", v)
            ),
            UISlider(
                pygame.Rect(x, 245, w, 10), "Additive Glow",
                0.0, 1.8, self.config.glow_intensity, step=0.05,
                on_change=lambda v: setattr(self.config, "glow_intensity", v)
            ),
            # Typography Modes
            UIButton(pygame.Rect(x, 280, btn_w, 24), "Letters", lambda: self._set_typography(TypographyMode.LETTERS)),
            UIButton(pygame.Rect(x + btn_w + 10, 280, btn_w, 24), "Words", lambda: self._set_typography(TypographyMode.WORDS)),
            UIButton(pygame.Rect(x, 310, btn_w, 24), "Phrases", lambda: self._set_typography(TypographyMode.PHRASES)),
            UIButton(pygame.Rect(x + btn_w + 10, 310, btn_w, 24), "Mixed", lambda: self._set_typography(TypographyMode.MIXED)),
            # Color Palettes
            UIButton(pygame.Rect(x, 345, btn_w, 24), "Solar Orange", lambda: self._set_palette("solar_orange")),
            UIButton(pygame.Rect(x + btn_w + 10, 345, btn_w, 24), "Deep Blue", lambda: self._set_palette("deep_blue")),
            UIButton(pygame.Rect(x, 375, btn_w, 24), "Purple Nebula", lambda: self._set_palette("purple_nebula")),
            UIButton(pygame.Rect(x + btn_w + 10, 375, btn_w, 24), "Monochrome", lambda: self._set_palette("monochrome_white")),
            UIButton(pygame.Rect(x, 405, w, 24), "Emerald Singularity", lambda: self._set_palette("emerald_singularity"))
        ]

        # -------------------------------------------------------------------------
        # Tab 3: LAYERS
        # -------------------------------------------------------------------------
        y_l = 105
        spacing = 35
        self.layer_widgets = [
            UIToggle(pygame.Rect(x, y_l + 0 * spacing, w, 20), "Event Horizon Core", self.config.show_black_hole, lambda s: setattr(self.config, "show_black_hole", s)),
            UIToggle(pygame.Rect(x, y_l + 1 * spacing, w, 20), "Relativistic Photon Ring", self.config.show_photon_ring, lambda s: setattr(self.config, "show_photon_ring", s)),
            UIToggle(pygame.Rect(x, y_l + 2 * spacing, w, 20), "Arabic Character Particles", self.config.show_particles, lambda s: setattr(self.config, "show_particles", s)),
            UIToggle(pygame.Rect(x, y_l + 3 * spacing, w, 20), "Cosmic Starfield", self.config.show_stars, lambda s: setattr(self.config, "show_stars", s)),
            UIToggle(pygame.Rect(x, y_l + 4 * spacing, w, 20), "Gravitational Lensing Deflection", self.config.show_lensing, lambda s: setattr(self.config, "show_lensing", s)),
            UIToggle(pygame.Rect(x, y_l + 5 * spacing, w, 20), "Additive Bloom & Glow", self.config.show_glow, lambda s: setattr(self.config, "show_glow", s)),
            UIToggle(pygame.Rect(x, y_l + 6 * spacing, w, 20), "Motion Blur Trails", self.config.show_trails, lambda s: setattr(self.config, "show_trails", s))
        ]

        # -------------------------------------------------------------------------
        # Tab 4: SYSTEM & PRESETS
        # -------------------------------------------------------------------------
        q_w = (w - 10) // 3
        self.system_widgets = [
            UISlider(
                pygame.Rect(x, 110, w, 10), "Simulation Speed",
                0.0, 2.5, self.state.time_scale, step=0.1,
                on_change=lambda v: setattr(self.state, "time_scale", v)
            ),
            UISlider(
                pygame.Rect(x, 155, w, 10), "Camera Zoom",
                0.4, 3.0, self.config.camera_zoom, step=0.05,
                on_change=lambda v: setattr(self.config, "camera_zoom", v)
            ),
            UIButton(pygame.Rect(x, 195, q_w, 26), "Low", lambda: self._apply_quality("LOW")),
            UIButton(pygame.Rect(x + q_w + 5, 195, q_w, 26), "Medium", lambda: self._apply_quality("MEDIUM")),
            UIButton(pygame.Rect(x + (q_w + 5) * 2, 195, q_w, 26), "High", lambda: self._apply_quality("HIGH")),
            UIButton(pygame.Rect(x, 240, w, 30), "Save Configuration", self._save_config_action),
            UIButton(pygame.Rect(x, 280, w, 30), "Reset Simulation", self._reset_action),
            UIButton(pygame.Rect(x, 320, w, 30), "Randomize Scene", self._randomize_action)
        ]

        # Toggle Panel Button (small tab on the right edge of panel)
        self.collapse_button = UIButton(pygame.Rect(self.width, 10, 24, 28), "«", self.toggle_collapsed)

    def _set_rs(self, val: float) -> None:
        self.config.rs = float(val)
        self.config.event_horizon_radius = 1.0 * self.config.rs
        self.config.photon_sphere_radius = 1.5 * self.config.rs
        self.config.isco_radius = 3.0 * self.config.rs
        self.config.disk_inner_radius = 3.0 * self.config.rs
        self.config.disk_outer_radius = max(self.config.disk_inner_radius + 50.0, 20.0 * self.config.rs)
        self.particle_system.initialize_pool()
        self.state.notify(f"Scale: Rs = {self.config.rs:.1f} (ISCO = {self.config.isco_radius:.1f})")

    def _set_tab(self, tab_name: str) -> None:
        self.active_tab = tab_name

    def toggle_collapsed(self) -> None:
        self.is_collapsed = not self.is_collapsed
        self.collapse_button.label = "»" if self.is_collapsed else "«"
        self.collapse_button.rect.x = 0 if self.is_collapsed else self.width

    def _set_particle_count(self, count: float) -> None:
        self.config.max_particles = int(count)
        self.particle_system.set_target_count(int(count))

    def _toggle_rotation_direction(self) -> None:
        self.config.rotation_direction *= -1.0
        self.state.notify(f"Rotation: {'Counter-Clockwise' if self.config.rotation_direction > 0 else 'Clockwise'}")

    def _set_typography(self, mode: TypographyMode) -> None:
        self.config.typography_mode = mode.value
        self.particle_system.text_provider.set_mode(mode)
        self.particle_system.refresh_typography()
        self.state.notify(f"Typography: {mode.value.upper()}")

    def _set_palette(self, palette_name: str) -> None:
        if palette_name in COLOR_PRESETS:
            self.config.color_preset = palette_name
            self.state.notify(f"Palette: {COLOR_PRESETS[palette_name]['name']}")

    def _apply_quality(self, quality: str) -> None:
        self.config.apply_quality_preset(quality)
        self.particle_system.set_target_count(self.config.max_particles)
        self.state.notify(f"Quality Preset: {quality}")

    def _save_config_action(self) -> None:
        self.on_save_config()
        self.state.notify("Configuration Saved Successfully")

    def _reset_action(self) -> None:
        self.state.reset_requested = True
        self.state.notify("Simulation Reset")

    def _randomize_action(self) -> None:
        self.state.randomize_requested = True
        self.state.notify("Scene Randomized")

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse clicks and drags on UI elements. Returns True if consumed."""
        if self.collapse_button.handle_event(event):
            return True

        if self.is_collapsed:
            return False

        panel_rect = pygame.Rect(0, 0, self.width, 480)
        is_in_panel = panel_rect.collidepoint(event.pos) if hasattr(event, "pos") else False

        for btn in self.tab_buttons:
            if btn.handle_event(event):
                return True

        active_widgets = []
        if self.active_tab == "PHYSICS":
            active_widgets = self.physics_widgets
        elif self.active_tab == "VISUALS":
            active_widgets = self.visuals_widgets
        elif self.active_tab == "LAYERS":
            active_widgets = self.layer_widgets
        elif self.active_tab == "SYSTEM":
            active_widgets = self.system_widgets

        for widget in active_widgets:
            if widget.handle_event(event):
                return True

        return is_in_panel

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the glassmorphic control dock."""
        self.collapse_button.draw(surface, self._font_small)
        if self.is_collapsed:
            return

        panel_h = min(surface.get_height() - 20, 460)
        panel_surf = pygame.Surface((self.width, panel_h), pygame.SRCALPHA)
        panel_surf.fill(COLOR_BG_PANEL)
        pygame.draw.rect(panel_surf, COLOR_BORDER, (0, 0, self.width, panel_h), width=1, border_radius=8)

        # Header title
        title_surf = self._font_title.render("CONTROL MATRIX", True, COLOR_ACCENT)
        panel_surf.blit(title_surf, (20, 16))

        surface.blit(panel_surf, (0, 10))

        # Draw tabs
        for btn in self.tab_buttons:
            is_active = (btn.label.upper() == self.active_tab)
            btn.bg_color = (60, 75, 105) if is_active else (30, 38, 52)
            btn.draw(surface, self._font_small)

        active_widgets = []
        if self.active_tab == "PHYSICS":
            active_widgets = self.physics_widgets
        elif self.active_tab == "VISUALS":
            active_widgets = self.visuals_widgets
        elif self.active_tab == "LAYERS":
            active_widgets = self.layer_widgets
        elif self.active_tab == "SYSTEM":
            active_widgets = self.system_widgets

        for widget in active_widgets:
            widget.draw(surface, self._font_small)
