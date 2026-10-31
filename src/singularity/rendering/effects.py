"""Visual effects: Additive bloom, motion trails, and physically proportioned event horizon."""

from typing import Tuple, Dict, Any
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


class EventHorizonRenderer:
    """Renders the central Schwarzschild black hole shadow and luminous relativistic photon ring."""

    def __init__(self):
        self._ring_cache: Dict[Tuple[int, int, Tuple[int, int, int]], pygame.Surface] = {}

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
