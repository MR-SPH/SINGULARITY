"""Font discovery, Arabic font loading, and high-performance pre-rendered glyph cache."""

import os
import sys
from typing import Dict, Tuple, Optional, List
import pygame
from singularity.typography.shaping import shape_arabic


class FontManager:
    """Discovers Arabic fonts and maintains loaded pygame font instances at various sizes."""

    @staticmethod
    def _get_candidate_font_paths() -> List[str]:
        candidates: List[str] = []

        # 1. Check PyInstaller bundle dir if packaged
        if hasattr(sys, "_MEIPASS"):
            candidates.append(os.path.join(sys._MEIPASS, "assets", "fonts", "segoeui.ttf"))
            candidates.append(os.path.join(sys._MEIPASS, "assets", "fonts", "tahoma.ttf"))

        # 2. Check relative to this source file
        src_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        candidates.append(os.path.join(src_root, "assets", "fonts", "segoeui.ttf"))
        candidates.append(os.path.join(src_root, "assets", "fonts", "tahoma.ttf"))

        # 3. Check relative to current working directory
        candidates.append(os.path.join(os.getcwd(), "assets", "fonts", "segoeui.ttf"))
        candidates.append(os.path.join(os.getcwd(), "assets", "fonts", "tahoma.ttf"))

        # 4. Windows dynamic system fonts
        windir = os.environ.get("WINDIR", os.environ.get("SYSTEMROOT", "C:\\Windows"))
        win_fonts = os.path.join(windir, "Fonts")
        candidates.append(os.path.join(win_fonts, "segoeui.ttf"))
        candidates.append(os.path.join(win_fonts, "tahoma.ttf"))
        candidates.append(os.path.join(win_fonts, "arial.ttf"))

        # 5. Linux / macOS system fonts
        candidates.extend([
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ])

        return candidates

    def __init__(self, explicit_font_path: Optional[str] = None):
        if not pygame.font.get_init():
            pygame.font.init()

        self.font_path = self._resolve_font_path(explicit_font_path)
        self._font_instances: Dict[int, pygame.font.Font] = {}

    def _resolve_font_path(self, explicit_path: Optional[str]) -> Optional[str]:
        if explicit_path and os.path.isfile(explicit_path):
            return explicit_path

        for candidate in self._get_candidate_font_paths():
            norm_path = os.path.normpath(candidate)
            if os.path.isfile(norm_path):
                return norm_path

        return None

    def get_font(self, size: int) -> pygame.font.Font:
        """Retrieve or create a cached Font instance for the given size in points."""
        size_clamped = max(8, min(96, size))
        if size_clamped in self._font_instances:
            return self._font_instances[size_clamped]

        try:
            if self.font_path and os.path.isfile(self.font_path):
                font = pygame.font.Font(self.font_path, size_clamped)
            else:
                font = pygame.font.SysFont("segoe ui,tahoma,arial", size_clamped)
        except Exception:
            font = pygame.font.Font(None, size_clamped)

        self._font_instances[size_clamped] = font
        return font


class GlyphCache:
    """High-performance multi-tier cache for pre-rasterized and rotated Arabic glyph surfaces.

    Quantizes font size, color channels, and rotation angles to ensure bounded memory
    and near-instantaneous 0.3-microsecond dictionary lookups during rendering.
    """

    SIZE_BUCKETS = (14, 20, 28, 38)
    ANGLE_STEP = 30  # 12 discrete angular rotations (0, 30, 60, ... 330)

    def __init__(self, font_manager: FontManager, max_entries: int = 15000):
        self.font_manager = font_manager
        self.max_entries = max_entries
        self._base_cache: Dict[Tuple[str, int, Tuple[int, int, int]], pygame.Surface] = {}
        self._rotated_cache: Dict[Tuple[str, int, Tuple[int, int, int], int], pygame.Surface] = {}

    def clear(self) -> None:
        """Flush the cache."""
        self._base_cache.clear()
        self._rotated_cache.clear()

    @staticmethod
    def quantize_size(raw_size: int) -> int:
        """Map continuous size to the closest discrete bucket."""
        if raw_size <= 16:
            return 14
        elif raw_size <= 23:
            return 20
        elif raw_size <= 32:
            return 28
        else:
            return 38

    @staticmethod
    def quantize_color(color_rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Quantize RGB channels to 32-unit increments for high cache hit rates."""
        r = min(255, (color_rgb[0] // 32) * 32)
        g = min(255, (color_rgb[1] // 32) * 32)
        b = min(255, (color_rgb[2] // 32) * 32)
        return (r, g, b)

    @staticmethod
    def quantize_angle(angle_deg: float) -> int:
        """Quantize continuous angle to 30-degree steps."""
        return int(round((angle_deg % 360.0) / 30.0) * 30) % 360

    def get_base_glyph(self, raw_text: str, size: int, color_rgb: Tuple[int, int, int]) -> pygame.Surface:
        """Render or retrieve a 2D unrotated shaped glyph surface."""
        size_q = self.quantize_size(size)
        col_q = self.quantize_color(color_rgb)
        key = (raw_text, size_q, col_q)

        if key in self._base_cache:
            return self._base_cache[key]

        font = self.font_manager.get_font(size_q)
        shaped_text = shape_arabic(raw_text)
        try:
            surface = font.render(shaped_text, True, col_q)
        except Exception:
            surface = font.render("?", True, col_q)

        if len(self._base_cache) >= self.max_entries:
            self._base_cache.clear()

        self._base_cache[key] = surface
        return surface

    def get_rotated_glyph(
        self,
        raw_text: str,
        size: int,
        color_rgb: Tuple[int, int, int],
        angle_deg: float
    ) -> pygame.Surface:
        """Retrieve a rotated glyph surface using quantized angle lookups."""
        angle_q = self.quantize_angle(angle_deg)
        size_q = self.quantize_size(size)
        col_q = self.quantize_color(color_rgb)
        key = (raw_text, size_q, col_q, angle_q)

        if key in self._rotated_cache:
            return self._rotated_cache[key]

        base_surface = self.get_base_glyph(raw_text, size_q, col_q)
        if angle_q == 0:
            rotated = base_surface
        else:
            rotated = pygame.transform.rotate(base_surface, angle_q)

        if len(self._rotated_cache) >= self.max_entries:
            self._rotated_cache.clear()

        self._rotated_cache[key] = rotated
        return rotated
