"""Mathematical and geometric utilities for the SINGULARITY engine.

Includes 3D coordinate transformations, perspective projections,
relativistic aberration, and procedural cosine color gradients.
"""

from typing import Tuple, Sequence, Optional
import numpy as np


def clamp(val: float, min_val: float, max_val: float) -> float:
    """Clamp a scalar value to [min_val, max_val]."""
    return max(min_val, min(max_val, val))


def remap(val: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    """Linearly map val from [in_min, in_max] to [out_min, out_max]."""
    if abs(in_max - in_min) < 1e-9:
        return out_min
    t = (val - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def smoothstep(edge0: float, edge1: float, x: float) -> float:
    """Hermite interpolation between two values."""
    if abs(edge1 - edge0) < 1e-9:
        return 0.0
    t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def lerp_color(
    c1: Tuple[int, int, int],
    c2: Tuple[int, int, int],
    t: float
) -> Tuple[int, int, int]:
    """Linearly interpolate between two RGB colors."""
    t_clamped = clamp(t, 0.0, 1.0)
    r = int(c1[0] + (c2[0] - c1[0]) * t_clamped)
    g = int(c1[1] + (c2[1] - c1[1]) * t_clamped)
    b = int(c1[2] + (c2[2] - c1[2]) * t_clamped)
    return (r, g, b)


def cosine_palette(
    t: float,
    a: Tuple[float, float, float] = (0.5, 0.5, 0.5),
    b: Tuple[float, float, float] = (0.5, 0.5, 0.5),
    c: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    d: Tuple[float, float, float] = (0.0, 0.333, 0.667)
) -> Tuple[int, int, int]:
    """Procedural cosine color gradient (Inigo Quilez technique).
    Returns (R, G, B) tuple with values in [0, 255].
    """
    two_pi = 2.0 * np.pi
    r = int(clamp(a[0] + b[0] * np.cos(two_pi * (c[0] * t + d[0])), 0.0, 1.0) * 255.0)
    g = int(clamp(a[1] + b[1] * np.cos(two_pi * (c[1] * t + d[1])), 0.0, 1.0) * 255.0)
    b_val = int(clamp(a[2] + b[2] * np.cos(two_pi * (c[2] * t + d[2])), 0.0, 1.0) * 255.0)
    return (r, g, b_val)


def rotate_y(points: np.ndarray, angle_rad: float) -> np.ndarray:
    """Rotate an [N, 3] array of points around the Y axis."""
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    rot = np.array([
        [cos_a, 0.0, sin_a],
        [0.0, 1.0, 0.0],
        [-sin_a, 0.0, cos_a]
    ], dtype=np.float32)
    return points @ rot.T


def rotate_x(points: np.ndarray, angle_rad: float) -> np.ndarray:
    """Rotate an [N, 3] array of points around the X axis."""
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    rot = np.array([
        [1.0, 0.0, 0.0],
        [0.0, cos_a, -sin_a],
        [0.0, sin_a, cos_a]
    ], dtype=np.float32)
    return points @ rot.T


def project_points(
    points_3d: np.ndarray,
    pitch: float,
    yaw: float,
    camera_distance: float,
    focal_length: float,
    center_x: float,
    center_y: float,
    near_clip: float = 1.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Project [N, 3] 3D world points onto 2D screen coordinates with strict pinhole perspective.

    The camera orbits the world origin (0, 0, 0) at distance camera_distance.
    Camera coordinate frame:
        +X: Right
        +Y: Down (matching Pygame screen coordinates)
        +Z: Forward (view direction into the scene)

    Returns:
        screen_coords: [N, 2] array of (x, y) pixels.
        depths: [N] array of Z-depth values in camera space.
        cam_space: [N, 3] points in camera coordinates.
    """
    if len(points_3d) == 0:
        return (
            np.empty((0, 2), dtype=np.float32),
            np.empty((0,), dtype=np.float32),
            np.empty((0, 3), dtype=np.float32)
        )

    # 1. World to Camera transform:
    # Rotate world by -yaw around Y, then -pitch around X
    p = rotate_y(points_3d, -yaw)
    p = rotate_x(p, -pitch)

    # In camera frame, camera is at (0, 0, -camera_distance), looking toward +Z
    # So points at origin (0, 0, 0) have camera Z = camera_distance
    cam_x = p[:, 0]
    cam_y = p[:, 1]
    cam_z = p[:, 2] + camera_distance

    # Clamp near clip
    z_clamped = np.maximum(cam_z, near_clip)

    factor = focal_length / z_clamped
    screen_x = center_x + cam_x * factor
    # In Pygame, Y increases downward. cam_y increases upward in standard 3D,
    # so we subtract cam_y * factor for proper orientation
    screen_y = center_y - cam_y * factor

    screen_coords = np.column_stack((screen_x, screen_y)).astype(np.float32)
    cam_space = np.column_stack((cam_x, cam_y, cam_z)).astype(np.float32)
    return screen_coords, z_clamped, cam_space
