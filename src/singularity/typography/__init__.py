"""Arabic Typography module for SINGULARITY."""

from singularity.typography.arabic import (
    TypographyMode,
    ARABIC_ALPHABET,
    COSMIC_WORDS,
    COSMIC_PHRASES,
    ArabicTextProvider
)
from singularity.typography.shaping import ArabicShaper, shape_arabic
from singularity.typography.fonts import FontManager, GlyphCache

__all__ = [
    "TypographyMode",
    "ARABIC_ALPHABET",
    "COSMIC_WORDS",
    "COSMIC_PHRASES",
    "ArabicTextProvider",
    "ArabicShaper",
    "shape_arabic",
    "FontManager",
    "GlyphCache"
]

