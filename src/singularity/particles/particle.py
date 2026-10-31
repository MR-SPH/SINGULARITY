"""Particle specification and attribute definitions for the Arabic Gravitational Engine."""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ParticleDefinition:
    """Logical representation of a single Arabic character particle."""

    # 3D Position
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    # 3D Velocity
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0

    # Rotation (degrees) and angular speed
    angle: float = 0.0
    angular_vel: float = 0.0

    # Physical and visual weight
    mass: float = 1.0
    brightness: float = 1.0
    opacity: float = 1.0
    scale: float = 1.0

    # Typography identity
    token: str = "ا"

    # Lifecycle
    age: float = 0.0
    lifetime: float = 20.0
    is_alive: bool = True

