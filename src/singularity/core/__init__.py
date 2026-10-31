"""Core package for SINGULARITY."""

from singularity.core.config import (
    EngineConfig,
    COLOR_PRESETS,
    QUALITY_PRESETS,
    QualityPreset
)
from singularity.core.state import EngineState
from singularity.core.simulation import BlackHoleSimulation
from singularity.core.engine import SingularityEngine

__all__ = [
    "EngineConfig",
    "COLOR_PRESETS",
    "QUALITY_PRESETS",
    "QualityPreset",
    "EngineState",
    "BlackHoleSimulation",
    "SingularityEngine"
]
