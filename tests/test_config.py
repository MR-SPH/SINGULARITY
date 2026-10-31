"""Unit tests for configuration serialization, validation, and preset application."""

import os
import json
import pytest

from singularity.core.config import EngineConfig, COLOR_PRESETS, QUALITY_PRESETS


class TestEngineConfig:
    """Validate parameter bounds, JSON serialization, and presets."""

    def test_default_config_valid(self):
        config = EngineConfig()
        config.validate()
        assert config.window_width >= 640
        assert config.window_height >= 480
        assert config.event_horizon_radius >= 4.0
        assert config.event_horizon_radius == config.rs
        assert config.color_preset in COLOR_PRESETS
        assert config.typography_mode == "letters"

    def test_clamping_invalid_values(self):
        config = EngineConfig(
            window_width=99999,
            window_height=-10,
            event_horizon_radius=1.0,
            rotation_speed=99.0
        )
        config.validate()
        assert config.window_width <= 3840
        assert config.window_height >= 480
        assert config.event_horizon_radius >= 4.0
        assert config.rotation_speed <= 5.0

    def test_quality_preset_application(self):
        config = EngineConfig()
        config.apply_quality_preset("LOW")
        assert config.quality_preset == "LOW"
        assert config.max_particles == QUALITY_PRESETS["LOW"].particle_count
        assert config.show_glow == QUALITY_PRESETS["LOW"].glow_enabled

        config.apply_quality_preset("HIGH")
        assert config.quality_preset == "HIGH"
        assert config.max_particles == QUALITY_PRESETS["HIGH"].particle_count

    def test_serialization_and_deserialization(self, tmp_path):
        config_file = tmp_path / "test_config.json"
        config = EngineConfig(
            max_particles=1500,
            color_preset="deep_blue",
            typography_mode="letters"
        )
        config.save_to_file(str(config_file))

        loaded = EngineConfig.load_from_file(str(config_file))
        assert loaded.max_particles == 1500
        assert loaded.color_preset == "deep_blue"
        assert loaded.typography_mode == "letters"

    def test_corrupted_config_fallback(self, tmp_path):
        bad_file = tmp_path / "bad_config.json"
        with open(bad_file, "w") as f:
            f.write("{ invalid json format !!!")

        fallback = EngineConfig.load_from_file(str(bad_file))
        assert isinstance(fallback, EngineConfig)
        assert fallback.max_particles == EngineConfig().max_particles

