"""Interactive 3D orbit camera with strict pinhole perspective projection."""

from typing import Tuple
import numpy as np
from singularity.utilities.math_utils import project_points, clamp


class Camera3D:
    """3D Orbit camera providing smooth pitch, yaw, zoom, and perspective projection."""

    def __init__(
        self,
        viewport_width: int = 1280,
        viewport_height: int = 720,
        pitch: float = 0.52,
        yaw: float = 0.0,
        zoom: float = 1.0,
        camera_distance: float = 480.0,
        fov_degrees: float = 48.0
    ):
        self.width = viewport_width
        self.height = viewport_height
        self.center_x = viewport_width * 0.5
        self.center_y = viewport_height * 0.5

        # Angular orientation in radians
        self.pitch = pitch
        self.yaw = yaw
        self.zoom = zoom
        self.camera_distance = camera_distance
        self.fov_degrees = fov_degrees

        # Targets for smooth delta-time interpolation
        self.target_pitch = pitch
        self.target_yaw = yaw
        self.target_zoom = zoom

        self._recompute_focal_length()

    def _recompute_focal_length(self) -> None:
        """Compute pinhole camera focal length from vertical FOV."""
        fov_rad = np.radians(clamp(self.fov_degrees, 20.0, 90.0))
        self.focal_length = (self.height * 0.5) / np.tan(fov_rad * 0.5)
        # Compatibility attribute
        self.fov_distance = self.focal_length

    def set_viewport(self, width: int, height: int) -> None:
        """Update viewport dimensions and recompute projection parameters."""
        self.width = max(320, width)
        self.height = max(240, height)
        self.center_x = self.width * 0.5
        self.center_y = self.height * 0.5
        self._recompute_focal_length()

    def update(self, dt: float) -> None:
        """Smoothly lerp pitch, yaw, and zoom toward their target values."""
        # Frame-rate independent exponential smoothing
        damping = 1.0 - np.exp(-dt * 12.0)
        self.pitch += (self.target_pitch - self.pitch) * damping
        self.yaw += (self.target_yaw - self.yaw) * damping
        self.zoom += (self.target_zoom - self.zoom) * damping

    @property
    def effective_distance(self) -> float:
        """Effective world-space camera distance accounting for zoom."""
        safe_zoom = max(0.2, self.zoom)
        return self.camera_distance / safe_zoom

    def get_camera_direction(self) -> np.ndarray:
        """Return unit vector pointing from camera toward the origin in world space."""
        cos_p = np.cos(self.pitch)
        sin_p = np.sin(self.pitch)
        cos_y = np.cos(self.yaw)
        sin_y = np.sin(self.yaw)

        dx = sin_y * cos_p
        dy = sin_p
        dz = cos_y * cos_p
        vec = np.array([dx, dy, dz], dtype=np.float32)
        norm = np.linalg.norm(vec)
        return vec / (norm + 1e-9)

    def get_projected_screen_radius(self, world_radius: float) -> float:
        """Return the exact apparent screen radius (in pixels) of a 3D sphere at the origin."""
        return float((self.focal_length * world_radius) / self.effective_distance)

    def project(self, points_3d: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Project [N, 3] world points to [N, 2] screen coordinates with depth.

        Returns:
            (screen_coords, z_depths)
        """
        screen_coords, z_depths, _ = project_points(
            points_3d,
            self.pitch,
            self.yaw,
            self.effective_distance,
            self.focal_length,
            self.center_x,
            self.center_y
        )
        return screen_coords, z_depths

    def project_with_cam_space(self, points_3d: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Project [N, 3] world points, also returning camera space coordinates."""
        return project_points(
            points_3d,
            self.pitch,
            self.yaw,
            self.effective_distance,
            self.focal_length,
            self.center_x,
            self.center_y
        )
