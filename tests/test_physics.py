"""Unit tests for relativistic physics, orbital dynamics, temperature, and lensing."""

import numpy as np
import pytest

from singularity.physics.gravity import (
    compute_schwarzschild_radius,
    compute_isco_radius,
    compute_photon_sphere_radius,
    paczynski_wiita_acceleration,
    is_absorbed
)
from singularity.physics.orbital_motion import (
    relativistic_orbital_speed,
    circular_orbital_angular_velocity,
    compute_thin_disk_temperature,
    compute_gravitational_redshift,
    compute_doppler_beaming,
    generate_disk_turbulence
)
from singularity.physics.lensing import (
    compute_einstein_ring_radius,
    deflect_stars,
    deflect_far_disk_screen_coords,
    compute_photon_ring_glow
)


class TestBlackHolePhysics:
    """Validate relativistic Schwarzschild calculations."""

    def test_schwarzschild_radius(self):
        mass = 5000.0
        g = 1.0
        c = 100.0
        rs = compute_schwarzschild_radius(mass, g, c)
        expected = (2.0 * g * mass) / (c * c)
        assert pytest.approx(rs, rel=1e-5) == expected
        assert rs == 1.0

    def test_isco_radius(self):
        rs = 12.0
        isco = compute_isco_radius(rs)
        assert isco == 36.0  # Exactly 3 * Rs

    def test_photon_sphere_radius(self):
        rs = 12.0
        r_ph = compute_photon_sphere_radius(rs)
        assert r_ph == 18.0  # Exactly 1.5 * Rs

    def test_paczynski_wiita_acceleration(self):
        radii = np.array([100.0, 50.0, 20.0], dtype=np.float32)
        rs = 12.0
        mass = 1000.0
        acc = paczynski_wiita_acceleration(radii, mass, rs)
        # Closer to horizon produces strictly higher acceleration
        assert acc[2] > acc[1] > acc[0]
        assert np.all(acc > 0.0)

    def test_event_horizon_absorption_flag(self):
        radii = np.array([5.0, 11.9, 12.0, 12.1, 50.0], dtype=np.float32)
        rs = 12.0
        mask = is_absorbed(radii, rs)
        assert np.array_equal(mask, [True, True, True, False, False])


class TestShakuraSunyaevTemperature:
    """Validate standard thin-disk temperature and gravitational redshift."""

    def test_temperature_profile_peak(self):
        rs = 10.0
        r_in = 30.0  # 3 Rs
        # Sample dense radial grid
        r_grid = np.linspace(r_in, 200.0, 500, dtype=np.float32)
        temps = compute_thin_disk_temperature(r_grid, r_in, rs)

        # Peak must occur near analytical peak r_peak = (49/36) * r_in = 40.83
        peak_idx = np.argmax(temps)
        r_peak_actual = r_grid[peak_idx]
        assert 39.0 <= r_peak_actual <= 43.0
        # Peak normalized temperature must be ~1.0
        assert temps[peak_idx] == pytest.approx(1.0, rel=0.05)

    def test_gravitational_redshift(self):
        rs = 10.0
        radii = np.array([10.05, 20.0, 50.0, 1000.0], dtype=np.float32)
        redshift = compute_gravitational_redshift(radii, rs)

        # As r -> Rs, redshift -> 0 (severe dimming)
        assert redshift[0] < 0.15
        # Redshift increases monotonically with radius
        assert redshift[0] < redshift[1] < redshift[2] < redshift[3]
        # At large distances, redshift factor -> 1.0
        assert redshift[3] == pytest.approx(1.0, rel=0.01)


class TestOrbitalMotion:
    """Validate relativistic orbital velocity, angular speed, and Doppler boosting."""

    def test_angular_velocity_monotonicity(self):
        rs = 12.0
        radii = np.array([20.0, 36.0, 80.0, 200.0], dtype=np.float32)
        omega = circular_orbital_angular_velocity(radii, mass=4000.0, rs=rs)
        # Closer particles must orbit strictly faster
        assert omega[0] > omega[1] > omega[2] > omega[3]

    def test_relativistic_orbital_speed(self):
        radii = np.array([36.0, 72.0, 150.0, 300.0], dtype=np.float32)
        rs = 12.0
        mass = 4000.0
        c = 220.0
        speeds = relativistic_orbital_speed(radii, mass, rs, speed_of_light=c)
        assert np.all(speeds < c)
        assert np.all(speeds > 0.0)
        assert speeds[0] > speeds[1] > speeds[2] > speeds[3]

    def test_doppler_beaming(self):
        cam_dir = np.array([0.0, 0.0, 1.0], dtype=np.float32)
        vel_approaching = np.array([[0.0, 0.0, 50.0]], dtype=np.float32)
        vel_receding = np.array([[0.0, 0.0, -50.0]], dtype=np.float32)

        boost_app = compute_doppler_beaming(vel_approaching, cam_dir)
        boost_rec = compute_doppler_beaming(vel_receding, cam_dir)

        assert boost_app[0] > 1.0
        assert boost_rec[0] < 1.0
        assert boost_app[0] > boost_rec[0]


class TestGravitationalLensing:
    """Validate screen-space light deflection and Einstein ring calculation."""

    def test_einstein_ring_radius(self):
        rs = 12.0
        re = compute_einstein_ring_radius(rs, intensity=1.0)
        assert re > rs
        assert re == pytest.approx(12.0 * 1.55, rel=1e-3)

    def test_star_deflection(self):
        stars = np.array([[700.0, 360.0]], dtype=np.float32)
        center = (640.0, 360.0)
        re = 80.0
        deflected, mag = deflect_stars(stars, center, re, intensity=1.0)

        original_dist = 60.0
        new_dist = np.hypot(deflected[0, 0] - center[0], deflected[0, 1] - center[1])
        assert new_dist > original_dist
        assert mag[0] > 1.0

    def test_far_disk_deflection(self):
        # Particle behind black hole (far side)
        coords = np.array([[640.0, 330.0]], dtype=np.float32)
        center = (640.0, 360.0)
        is_far = np.array([True], dtype=bool)
        deflected = deflect_far_disk_screen_coords(coords, center, 60.0, is_far, pitch_angle=0.5, intensity=1.0)
        # Should be deflected upward (lower Y in screen coords)
        assert deflected[0, 1] < coords[0, 1]


class TestGravitationalRipples:
    """Validate relativistic gravitational wave ripples generated on mass absorption."""

    def test_ripple_expansion_and_lifecycle(self):
        from singularity.rendering.effects import GravitationalRipple, EventHorizonRenderer
        renderer = EventHorizonRenderer()
        renderer.trigger_ripple(rs_world=12.0)
        assert len(renderer.ripples) == 1

        ripple = renderer.ripples[0]
        initial_radius = ripple.radius
        assert initial_radius > 12.0
        assert ripple.alive
        assert ripple.progress < 0.5

        # Advance ripple by update step
        ripple.update(0.5)
        assert ripple.radius > initial_radius
