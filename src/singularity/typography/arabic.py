"""Arabic typography datasets, cosmological vocabularies, and text generators."""

from enum import Enum
import random
from typing import List


class TypographyMode(str, Enum):
    LETTERS = "letters"
    WORDS = "words"
    PHRASES = "phrases"
    MIXED = "mixed"


# Standard 28 Arabic letters in isolated form
ARABIC_ALPHABET: List[str] = [
    "ا", "ب", "ت", "ث", "ج", "ح", "خ",
    "د", "ذ", "ر", "ز", "س", "ش", "ص",
    "ض", "ط", "ظ", "ع", "غ", "ف", "ق",
    "ك", "ل", "م", "ن", "ه", "و", "ي"
]

# Cosmological vocabulary in Arabic (Gravitational & Astrophysical terms)
COSMIC_WORDS: List[str] = [
    "جاذبية",      # Gravity
    "أفق الحدث",    # Event Horizon
    "ثقب أسود",     # Black Hole
    "تفرد",        # Singularity
    "نور",         # Light
    "سرمدي",       # Eternal
    "فضاء",        # Outer Space / Cosmos
    "طاقة",        # Energy
    "زمكان",       # Spacetime
    "فلك",         # Celestial Orbit
    "شعاع",        # Beam / Ray
    "كون",         # Cosmos / Universe
    "مجرّة",       # Galaxy
    "سديم",        # Nebula
    "كتلة",        # Mass
    "انحناء"       # Curvature
]

# Cosmological phrases exploring gravitational mystery and astronomical scale
COSMIC_PHRASES: List[str] = [
    "في فلك يسبحون",
    "والنجم إذا هوى",
    "نور في قلب الظلام",
    "انحناء الزمان والمكان",
    "أسرار التفرد الأعظم",
    "نبض الكون السرمدي"
]


class ArabicTextProvider:
    """Provides shaped Arabic characters, words, and phrases for particle emission."""

    def __init__(self, mode: TypographyMode = TypographyMode.MIXED, custom_words: List[str] = None):
        self.mode = mode
        self.custom_words = custom_words if custom_words else list(COSMIC_WORDS)

    def set_mode(self, mode: TypographyMode) -> None:
        self.mode = mode

    def set_custom_words(self, words: List[str]) -> None:
        if words:
            self.custom_words = list(words)

    def get_token(self) -> str:
        """Return an Arabic token based on the currently selected typography mode."""
        if self.mode == TypographyMode.LETTERS:
            return random.choice(ARABIC_ALPHABET)
        elif self.mode == TypographyMode.WORDS:
            return random.choice(self.custom_words)
        elif self.mode == TypographyMode.PHRASES:
            return random.choice(COSMIC_PHRASES)
        else:  # MIXED
            roll = random.random()
            if roll < 0.65:
                return random.choice(ARABIC_ALPHABET)
            elif roll < 0.90:
                return random.choice(self.custom_words)
            else:
                return random.choice(COSMIC_PHRASES)

    def get_token_list(self, count: int) -> List[str]:
        """Generate a batch of tokens."""
        return [self.get_token() for _ in range(count)]

