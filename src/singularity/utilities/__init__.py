"""Utilities package for SINGULARITY."""

from singularity.utilities.math_utils import (
    clamp,
    remap,
    smoothstep,
    lerp_color,
    cosine_palette,
    rotate_x,
    rotate_y,
    project_points
)
from singularity.utilities.profiler import FrameProfiler

__all__ = [
    "clamp",
    "remap",
    "smoothstep",
    "lerp_color",
    "cosine_palette",
    "rotate_x",
    "rotate_y",
    "project_points",
    "FrameProfiler"
]

