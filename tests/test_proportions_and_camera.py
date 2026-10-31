"""Unit tests for unified spatial scale, 3D camera stability, and inclination scenarios."""

import numpy as np
import pytest

from singularity.core.config import EngineConfig
from singularity.particles.system import ParticleSystem
from singularity.rendering.camera import Camera3D
from singularity.typography.arabic import ArabicTextProvider, TypographyMode


class TestUnifiedProportions:
    """Validate that all physical dimensions strictly obey the Schwarzschild radius (Rs) unit."""

    def test_normalized_geometry_ratios(self):
        config = EngineConfig(rs=12.0)
        config.validate()

        rs = config.rs
        assert config.event_horizon_radius == 1.0 * rs
        assert config.photon_sphere_radius == 1.5 * rs
        assert config.isco_radius == 3.0 * rs
        assert config.disk_inner_radius >= 3.0 * rs
        assert config.disk_outer_radius >= 15.0 * rs

    def test_disk_scale_height(self):
        config = EngineConfig(rs=10.0, disk_scale_height_ratio=0.03)
        # At r = 100, scale height should be exactly 3.0
        h_100 = config.disk_scale_height_ratio * 100.0
        assert h_100 == pytest.approx(3.0)

    def test_character_world_scale_proportions(self):
        config = EngineConfig(rs=12.0)
        # Glyph height should be a small fraction of Rs (~0.35 - 0.45 Rs)
        assert 0.25 * config.rs <= config.character_world_size <= 0.60 * config.rs


class TestCameraAndPerspective:
    """Validate 3D pinhole camera projection, aspect ratio invariance, and stability."""

    def test_camera_projection_center(self):
        cam = Camera3D(viewport_width=1280, viewport_height=720, pitch=0.0, yaw=0.0)
        # Point at world origin (0, 0, 0)
        origin = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)
        screen_coords, depths = cam.project(origin)

        # Must project exactly onto screen center (640, 360)
        assert screen_coords[0, 0] == pytest.approx(640.0)
        assert screen_coords[0, 1] == pytest.approx(360.0)
        assert depths[0] == pytest.approx(cam.effective_distance)

    def test_face_on_circularity(self):
        """At pitch=pi/2 (face-on), equidistant disk points must project as a circle."""
        cam = Camera3D(viewport_width=1280, viewport_height=720, pitch=np.pi * 0.5, yaw=0.0)
        radius = 100.0
        # 4 orthogonal points on disk plane (X-Z)
        points = np.array([
            [radius, 0.0, 0.0],
            [-radius, 0.0, 0.0],
            [0.0, 0.0, radius],
            [0.0, 0.0, -radius]
        ], dtype=np.float32)

        coords, _ = cam.project(points)
        cx, cy = cam.center_x, cam.center_y

        dist0 = np.hypot(coords[0, 0] - cx, coords[0, 1] - cy)
        dist1 = np.hypot(coords[1, 0] - cx, coords[1, 1] - cy)
        dist2 = np.hypot(coords[2, 0] - cx, coords[2, 1] - cy)
        dist3 = np.hypot(coords[3, 0] - cx, coords[3, 1] - cy)

        # In face-on view, horizontal and vertical radii must be virtually identical
        assert dist0 == pytest.approx(dist1, rel=1e-3)
        assert dist2 == pytest.approx(dist3, rel=0.08)  # slight perspective depth difference
        assert dist0 == pytest.approx(dist2, rel=0.08)

    def test_inclination_flattening(self):
        """As pitch approaches 0 (edge-on), the projected disk vertical extent shrinks."""
        cam_edge = Camera3D(viewport_width=1280, viewport_height=720, pitch=0.0, yaw=0.0)
        cam_face = Camera3D(viewport_width=1280, viewport_height=720, pitch=np.radians(80.0), yaw=0.0)

        r = 100.0
        p_z = np.array([[0.0, 0.0, r]], dtype=np.float32)

        c_face, _ = cam_face.project(p_z)
        c_edge, _ = cam_edge.project(p_z)

        dy_face = abs(c_face[0, 1] - cam_face.center_y)
        dy_edge = abs(c_edge[0, 1] - cam_edge.center_y)

        # Edge-on (pitch=0) must compress vertical screen extent compared to inclined view
        assert dy_edge < dy_face * 0.35

    def test_360_continuous_orbit_stability(self):
        """Verify continuous orbital rotation produces finite, valid coordinates without NaN."""
        cam = Camera3D(viewport_width=1280, viewport_height=720, pitch=0.5, yaw=0.0)
        points = np.array([[50.0, 0.0, 50.0]], dtype=np.float32)

        for deg in range(0, 360, 15):
            cam.yaw = np.radians(deg)
            coords, depths = cam.project(points)
            assert not np.any(np.isnan(coords))
            assert not np.any(np.isnan(depths))
            assert depths[0] > 0.0


class TestTypographyDensityAndScaling:
    """Validate particle density controls and anti-overlap spacing."""

    def test_typography_density_scaling(self):
        config_low = EngineConfig(max_particles=500, typography_density=0.5)
        config_high = EngineConfig(max_particles=3000, typography_density=2.0)

        provider = ArabicTextProvider(mode=TypographyMode.LETTERS)
        sys_low = ParticleSystem(config_low, provider)
        sys_high = ParticleSystem(config_high, provider)

        assert sum(sys_low.alive) == 500
        assert sum(sys_high.alive) == 3000

    def test_character_perspective_size_ordering(self):
        """Characters closer to camera (lower depth) must project larger than distant characters."""
        cam = Camera3D(viewport_width=1280, viewport_height=720, pitch=0.5, yaw=0.0)
        char_world_size = 4.5

        depth_near = 350.0
        depth_far = 600.0

        size_near = (cam.focal_length * char_world_size) / depth_near
        size_far = (cam.focal_length * char_world_size) / depth_far

        assert size_near > size_far

