"""Unit tests for Arabic typography, contextual shaping, and glyph cache."""

import os
import pytest
import pygame

from singularity.typography.arabic import (
    ARABIC_ALPHABET,
    COSMIC_WORDS,
    COSMIC_PHRASES,
    TypographyMode,
    ArabicTextProvider
)
from singularity.typography.shaping import shape_arabic, ArabicShaper
from singularity.typography.fonts import FontManager, GlyphCache


class TestArabicTypography:
    """Validate shaping, BiDi, and character sets."""

    def test_alphabet_completeness(self):
        # Must contain all 28 traditional letters
        assert len(ARABIC_ALPHABET) == 28
        assert "ا" in ARABIC_ALPHABET
        assert "ي" in ARABIC_ALPHABET

    def test_shaping_contextual_connectivity(self):
        # A multi-letter connected word
        word = "جاذبية"
        shaped = shape_arabic(word)
        assert shaped is not None
        assert len(shaped) > 0
        # Shaped output should differ from raw unshaped disconnected string
        # or be a valid unicode representation
        assert isinstance(shaped, str)

    def test_shaping_memoization(self):
        shaper = ArabicShaper()
        res1 = shaper.shape("ثقب أسود")
        res2 = shaper.shape("ثقب أسود")
        assert res1 == res2
        assert "ثقب أسود" in shaper._cache

    def test_text_provider_modes(self):
        provider = ArabicTextProvider(mode=TypographyMode.LETTERS)
        token_letter = provider.get_token()
        assert token_letter in ARABIC_ALPHABET

        provider.set_mode(TypographyMode.WORDS)
        token_word = provider.get_token()
        assert token_word in COSMIC_WORDS

        provider.set_mode(TypographyMode.PHRASES)
        token_phrase = provider.get_token()
        assert token_phrase in COSMIC_PHRASES


class TestGlyphCache:
    """Validate font loading and discrete quantization."""

    @classmethod
    def setup_class(cls):
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()

    @classmethod
    def teardown_class(cls):
        pygame.quit()

    def test_glyph_quantization(self):
        fm = FontManager()
        cache = GlyphCache(fm)

        assert cache.quantize_size(11) == 14
        assert cache.quantize_size(19) == 20
        assert cache.quantize_size(27) == 28
        assert cache.quantize_size(45) == 38

        assert cache.quantize_angle(14.0) == 0
        assert cache.quantize_angle(29.0) == 30
        assert cache.quantize_angle(88.0) == 90

    def test_glyph_surface_retrieval(self):
        fm = FontManager()
        cache = GlyphCache(fm)
        surf = cache.get_rotated_glyph("ن", size=20, color_rgb=(255, 200, 50), angle_deg=45.0)
        assert isinstance(surf, pygame.Surface)
        assert surf.get_width() > 0
        assert surf.get_height() > 0

    def test_glyph_surface_retrieval_with_connected_word(self):
        fm = FontManager()
        cache = GlyphCache(fm)
        surf_word = cache.get_rotated_glyph("جاذبية", size=28, color_rgb=(255, 220, 100), angle_deg=0.0)
        assert isinstance(surf_word, pygame.Surface)
        assert surf_word.get_width() > 0
        assert surf_word.get_height() > 0

