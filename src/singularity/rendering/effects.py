"""Visual effects: Additive bloom, motion trails, and physically proportioned event horizon."""

from typing import Optional, Tuple, Dict, Any
import numpy as np
import pygame

from singularity.rendering.camera import Camera3D
from singularity.utilities.math_utils import lerp_color


class BloomEffect:
    """Fast, hardware-friendly multi-pass additive bloom using smooth downsampling."""

    def __init__(self, width: int, height: int, downsample_factor: int = 2):
        self.width = width
        self.height = height
        self.downsample = max(1, downsample_factor)
        self._init_surfaces()

    def _init_surfaces(self) -> None:
        dw = max(16, self.width // self.downsample)
        dh = max(16, self.height // self.downsample)
        self.small_surface = pygame.Surface((dw, dh)).convert()
        self.blur_surface = pygame.Surface((dw // 2, dh // 2)).convert()

    def resize(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._init_surfaces()

    def apply_bloom(self, source_surface: pygame.Surface, target_surface: pygame.Surface, intensity: float = 0.8) -> None:
        """Extract bright elements, downscale, smoothscale blur, and additively blend back."""
        if intensity <= 0.05:
            return

        pygame.transform.smoothscale(source_surface, self.small_surface.get_size(), self.small_surface)
        pygame.transform.smoothscale(self.small_surface, self.blur_surface.get_size(), self.blur_surface)
        glow_full = pygame.transform.smoothscale(self.blur_surface, (self.width, self.height))

        alpha_val = int(min(255, 255 * intensity * 0.55))
        glow_full.set_alpha(alpha_val)

        target_surface.blit(glow_full, (0, 0), special_flags=pygame.BLEND_ADD)


class GravitationalRipple:
    """An expanding relativistic spacetime ripple in the disk plane triggered by mass absorption."""

    def __init__(
        self,
        start_radius: float,
        max_radius: float,
        speed: float,
        color: Tuple[int, int, int] = (160, 230, 255)
    ):
        self.radius = start_radius
        self.max_radius = max_radius
        self.speed = speed
        self.color = color
        self.alive = True

    def update(self, dt: float) -> None:
        self.radius += self.speed * dt
        if self.radius >= self.max_radius:
            self.alive = False

    @property
    def progress(self) -> float:
        return min(1.0, max(0.0, self.radius / self.max_radius))


class EventHorizonRenderer:
    """Renders the central Schwarzschild black hole shadow and luminous relativistic photon ring."""

    def __init__(self):
        self._ring_cache: Dict[Tuple[int, int, Tuple[int, int, int]], pygame.Surface] = {}
        self.ripples: list[GravitationalRipple] = []
        self._ripple_cooldown: float = 0.0

    def trigger_ripple(self, rs_world: float, color: Optional[Tuple[int, int, int]] = None) -> None:
        """Trigger a relativistic gravitational wave ripple radiating outward across the disk plane."""
        if self._ripple_cooldown > 0.0 or len(self.ripples) >= 6:
            return
        self._ripple_cooldown = 0.10
        self.ripples.append(GravitationalRipple(
            start_radius=rs_world * 1.05,
            max_radius=rs_world * 4.6,
            speed=rs_world * 4.6,
            color=color or (160, 230, 255)
        ))

    def _get_photon_ring_surface(
        self,
        photon_radius_px: int,
        rs_px: int,
        color_preset: Dict[str, Any]
    ) -> pygame.Surface:
        core_col = color_preset.get("core_color", (255, 255, 255))
        inner_col = color_preset.get("inner_disk_color", (255, 220, 100))
        key = (photon_radius_px, rs_px, inner_col)

        if key in self._ring_cache:
            return self._ring_cache[key]

        dim = photon_radius_px * 2 + 40
        surf = pygame.Surface((dim, dim), pygame.SRCALPHA)
        center = dim // 2

        # 1. Subtle electric-blue relativistic ionization sheath
        ionization_col = (130, 205, 255)
        for offset in range(-4, 6):
            r_ion = photon_radius_px + offset
            if r_ion <= rs_px:
                continue
            alpha_ion = max(15, 65 - abs(offset) * 10)
            pygame.draw.circle(surf, (*ionization_col, alpha_ion), (center, center), r_ion, width=1)

        # 2. Multi-layer warm accretion photon ring
        num_layers = 10
        for b in range(num_layers):
            ring_r = photon_radius_px - (num_layers - b) * 2
            if ring_r <= rs_px:
                continue
            t = b / float(num_layers)
            col = lerp_color(inner_col, core_col, t)
            alpha = int(120 * t + 80)
            pygame.draw.circle(surf, (*col, alpha), (center, center), ring_r, width=2)

        # 3. Brilliant white-hot core line at the photon sphere
        pygame.draw.circle(surf, (*core_col, 245), (center, center), photon_radius_px, width=2)

        if len(self._ring_cache) > 40:
            self._ring_cache.clear()

        self._ring_cache[key] = surf
        return surf

    def render(
        self,
        surface: pygame.Surface,
        center_xy: Tuple[float, float],
        camera: Camera3D,
        rs_world: float,
        r_photon_world: float,
        color_preset: Dict[str, Any],
        show_photon_ring: bool = True
    ) -> None:
        """Render the relativistic photon ring and pitch-black event horizon core strictly scaled by camera."""
        cx, cy = int(center_xy[0]), int(center_xy[1])

        # Exact projected screen radii derived from 3D camera
        rs_px = int(camera.get_projected_screen_radius(rs_world))
        photon_px = int(camera.get_projected_screen_radius(r_photon_world))

        if rs_px <= 2:
            return

        # 0. Render active gravitational wave ripples expanding across the inclined disk plane
        dt_est = 1.0 / 60.0
        self._ripple_cooldown = max(0.0, self._ripple_cooldown - dt_est)
        pitch_factor = max(0.06, abs(float(np.sin(camera.pitch))))

        alive_ripples = []
        for rip in self.ripples:
            rip.update(dt_est)
            if rip.alive:
                alive_ripples.append(rip)
                rx = int(camera.get_projected_screen_radius(rip.radius))
                ry = max(2, int(rx * pitch_factor))
                alpha = int(max(0.0, min(220.0, (1.0 - rip.progress) * 200.0)))
                if rx > 4 and alpha > 10:
                    rw = rx * 2 + 6
                    rh = ry * 2 + 6
                    rip_surf = pygame.Surface((rw, rh), pygame.SRCALPHA)
                    pygame.draw.ellipse(
                        rip_surf,
                        (*rip.color, alpha),
                        pygame.Rect(3, 3, rx * 2, ry * 2),
                        width=max(1, int(rx * 0.025))
                    )
                    surface.blit(rip_surf, (cx - rw // 2, cy - rh // 2), special_flags=pygame.BLEND_ADD)
        self.ripples = alive_ripples

        # 1. Luminous photon sphere ring
        if show_photon_ring and photon_px > rs_px:
            ring_surf = self._get_photon_ring_surface(photon_px, rs_px, color_preset)
            rw, rh = ring_surf.get_size()
            surface.blit(ring_surf, (cx - rw // 2, cy - rh // 2), special_flags=pygame.BLEND_ADD)

        # 2. Gravitational redshift transition rim (deep dark amber/red boundary)
        outer_rim = rs_px + max(2, int(rs_px * 0.08))
        redshift_col = (45, 10, 3)
        pygame.draw.circle(surface, redshift_col, (cx, cy), outer_rim)

        # 3. Absolute event horizon: pitch-black consuming sphere
        pygame.draw.circle(surface, (0, 0, 0), (cx, cy), rs_px)
