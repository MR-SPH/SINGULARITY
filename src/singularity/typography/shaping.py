"""Arabic text shaping and bidirectional (BiDi) layout processing.

Ensures that Arabic characters are rendered with correct contextual ligatures
(isolated, initial, medial, final) and displayed Right-to-Left without glyph disconnection.
"""

from typing import Dict
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_RESHAPER = True
except ImportError:
    HAS_RESHAPER = False


class ArabicShaper:
    """Singleton-style cached shaper for Arabic strings."""

    def __init__(self):
        self._cache: Dict[str, str] = {}
        if HAS_RESHAPER:
            # Configure reshaper to support all standard ligatures
            configuration = {
                'delete_harakat': False,
                'support_ligatures': True,
                'RIAL': True
            }
            self._reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)
        else:
            self._reshaper = None

    def shape(self, text: str) -> str:
        """Shape Arabic string for contextual letter connectivity and correct BiDi RTL display.

        Results are memoized in an in-memory cache for maximum performance.
        """
        if not text:
            return ""

        if text in self._cache:
            return self._cache[text]

        if not HAS_RESHAPER:
            self._cache[text] = text
            return text

        try:
            reshaped_text = self._reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
            self._cache[text] = bidi_text
            return bidi_text
        except Exception:
            # Safe graceful fallback in case of formatting anomalies
            self._cache[text] = text
            return text


# Global instance for project-wide use
_GLOBAL_SHAPER = ArabicShaper()


def shape_arabic(text: str) -> str:
    """Convenience helper to shape Arabic text."""
    return _GLOBAL_SHAPER.shape(text)

