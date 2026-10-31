"""Rendering package for SINGULARITY."""

from singularity.rendering.camera import Camera3D
from singularity.rendering.star_renderer import StarRenderer
from singularity.rendering.character_renderer import CharacterRenderer
from singularity.rendering.effects import BloomEffect, EventHorizonRenderer
from singularity.rendering.renderer import SingularityRenderer

__all__ = [
    "Camera3D",
    "StarRenderer",
    "CharacterRenderer",
    "BloomEffect",
    "EventHorizonRenderer",
    "SingularityRenderer"
]

