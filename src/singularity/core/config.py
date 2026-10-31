"""Configuration system for the SINGULARITY engine with unified world-space scale."""

from dataclasses import dataclass, field, asdict
import json
import os
from typing import Dict, Any, List, Tuple


COLOR_PRESETS: Dict[str, Dict[str, Any]] = {
    "solar_orange": {
        "name": "Solar Orange (Event Horizon Telescope)",
        "core_color": (255, 255, 255),
        "inner_disk_color": (255, 220, 100),
        "mid_disk_color": (255, 120, 25),
        "outer_disk_color": (180, 25, 5),
        "bg_star_tint": (255, 245, 230),
        "glow_color": (255, 140, 30)
    },
    "deep_blue": {
        "name": "Deep Blue (Cherenkov Quasar)",
        "core_color": (245, 255, 255),
        "inner_disk_color": (160, 230, 255),
        "mid_disk_color": (35, 140, 255),
        "outer_disk_color": (10, 45, 160),
        "bg_star_tint": (210, 230, 255),
        "glow_color": (45, 150, 255)
    },
    "purple_nebula": {
        "name": "Purple Nebula (Cosmic Violet)",
        "core_color": (255, 250, 255),
        "inner_disk_color": (255, 165, 245),
        "mid_disk_color": (185, 55, 235),
        "outer_disk_color": (80, 10, 135),
        "bg_star_tint": (245, 225, 255),
        "glow_color": (195, 55, 235)
    },
    "monochrome_white": {
        "name": "Monochrome Gravitational (Scientific Minimalist)",
        "core_color": (255, 255, 255),
        "inner_disk_color": (240, 240, 240),
        "mid_disk_color": (175, 175, 175),
        "outer_disk_color": (85, 85, 85),
        "bg_star_tint": (220, 220, 220),
        "glow_color": (210, 210, 210)
    },
    "emerald_singularity": {
        "name": "Emerald Singularity (Radio Jet)",
        "core_color": (245, 255, 250),
        "inner_disk_color": (140, 255, 195),
        "mid_disk_color": (25, 210, 125),
        "outer_disk_color": (5, 95, 55),
        "bg_star_tint": (220, 255, 235),
        "glow_color": (35, 220, 135)
    }
}


@dataclass
class QualityPreset:
    name: str
    particle_count: int
    star_count: int
    glow_enabled: bool
    lensing_enabled: bool
    bloom_downsample: int
    trails_enabled: bool


QUALITY_PRESETS: Dict[str, QualityPreset] = {
    "LOW": QualityPreset(
        name="LOW",
        particle_count=1000,
        star_count=250,
        glow_enabled=False,
        lensing_enabled=True,
        bloom_downsample=4,
        trails_enabled=True
    ),
    "MEDIUM": QualityPreset(
        name="MEDIUM",
        particle_count=2200,
        star_count=500,
        glow_enabled=True,
        lensing_enabled=True,
        bloom_downsample=2,
        trails_enabled=True
    ),
    "HIGH": QualityPreset(
        name="HIGH",
        particle_count=3800,
        star_count=900,
        glow_enabled=True,
        lensing_enabled=True,
        bloom_downsample=2,
        trails_enabled=True
    )
}


@dataclass
class EngineConfig:
    """Master configuration adhering to unified Schwarzschild radius (Rs) scaling."""

    # -------------------------------------------------------------------------
    # Unified Spatial Scale (Normalized World Units where Rs is base unit)
    # -------------------------------------------------------------------------
    rs: float = 12.0                           # Schwarzschild radius in world units
    event_horizon_radius: float = 12.0          # 1.0 * Rs
    photon_sphere_radius: float = 18.0          # 1.5 * Rs
    isco_radius: float = 36.0                   # 3.0 * Rs
    disk_inner_radius: float = 36.0             # 3.0 * Rs (inner stable accretion boundary)
    disk_outer_radius: float = 240.0            # 20.0 * Rs (outer accretion rim)
    disk_scale_height_ratio: float = 0.03       # H(r) = 0.03 * r
    character_world_size: float = 4.5           # ~0.375 * Rs world-space glyph dimension

    # Display settings
    window_width: int = 1280
    window_height: int = 720
    target_fps: int = 60
    fullscreen: bool = False
    quality_preset: str = "MEDIUM"

    # Physics parameters
    black_hole_mass: float = 4500.0
    rotation_speed: float = 1.05
    rotation_direction: float = 1.0             # 1.0 = CCW, -1.0 = CW
    turbulence_factor: float = 0.05
    gravitational_constant: float = 1.0
    doppler_beaming_factor: float = 1.6

    # Particle system parameters
    max_particles: int = 2200
    typography_density: float = 1.0             # Density scaling factor
    character_base_size: int = 22               # Reference point size for cache

    # Lensing & Visual Effects
    lensing_intensity: float = 1.15
    einstein_radius_px: float = 110.0
    glow_intensity: float = 0.85
    motion_blur_alpha: int = 28
    color_preset: str = "solar_orange"

    # Background Starfield
    star_count: int = 450
    star_twinkle_speed: float = 1.5

    # Typography settings
    typography_mode: str = "letters"
    custom_words: List[str] = field(default_factory=lambda: [
        "جاذبية", "أفق الحدث", "ثقب أسود", "تفرد", "نور", "سرمدي", "فضاء", "طاقة"
    ])
    font_path: str = ""

    # 3D Camera System (World space)
    camera_distance: float = 480.0              # 40.0 * Rs
    camera_pitch: float = 0.52                  # ~30 degrees natural inclination
    camera_yaw: float = 0.0                     # Azimuthal rotation
    camera_zoom: float = 1.0
    camera_fov: float = 48.0                    # Vertical FOV in degrees
    fov_distance: float = 800.0                 # Legacy compatibility focal distance

    # Layer Visibility Flags
    show_black_hole: bool = True
    show_photon_ring: bool = True
    show_particles: bool = True
    show_stars: bool = True
    show_lensing: bool = True
    show_glow: bool = True
    show_trails: bool = True
    show_ui: bool = True

    def validate(self) -> None:
        """Validate and clamp configuration parameters to sensible physical bounds."""
        self.window_width = max(640, min(3840, int(self.window_width)))
        self.window_height = max(480, min(2160, int(self.window_height)))
        self.target_fps = max(15, min(240, int(self.target_fps)))

        # Enforce unified Rs scaling relationships
        self.rs = max(4.0, min(50.0, float(self.rs)))
        self.event_horizon_radius = 1.0 * self.rs
        self.photon_sphere_radius = 1.5 * self.rs
        self.isco_radius = 3.0 * self.rs

        # Accretion disk bounds: strictly at or beyond ISCO
        self.disk_inner_radius = max(self.isco_radius, float(self.disk_inner_radius))
        self.disk_outer_radius = max(self.disk_inner_radius + 4.0 * self.rs, float(self.disk_outer_radius))

        self.character_world_size = max(1.0, min(15.0, float(self.character_world_size)))
        self.camera_distance = max(10.0 * self.rs, min(150.0 * self.rs, float(self.camera_distance)))

        self.rotation_speed = max(0.0, min(5.0, float(self.rotation_speed)))
        self.max_particles = max(100, min(10000, int(self.max_particles)))
        self.lensing_intensity = max(0.0, min(3.0, float(self.lensing_intensity)))
        self.glow_intensity = max(0.0, min(2.0, float(self.glow_intensity)))
        self.camera_zoom = max(0.3, min(3.5, float(self.camera_zoom)))
        self.star_count = max(0, min(2500, int(self.star_count)))

        if self.color_preset not in COLOR_PRESETS:
            self.color_preset = "solar_orange"

        if self.quality_preset not in QUALITY_PRESETS:
            self.quality_preset = "MEDIUM"

    def apply_quality_preset(self, preset_name: str) -> None:
        """Apply performance settings from a named quality preset."""
        preset = QUALITY_PRESETS.get(preset_name.upper())
        if not preset:
            return
        self.quality_preset = preset.name
        self.max_particles = preset.particle_count
        self.star_count = preset.star_count
        self.show_glow = preset.glow_enabled
        self.show_lensing = preset.lensing_enabled
        self.show_trails = preset.trails_enabled

    def save_to_file(self, file_path: str) -> None:
        """Serialize configuration to a JSON file."""
        self.validate()
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4, ensure_ascii=False)

    @classmethod
    def load_from_file(cls, file_path: str) -> "EngineConfig":
        """Deserialize and validate configuration from a JSON file with fallback."""
        if not os.path.exists(file_path):
            config = cls()
            config.validate()
            return config
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            config = cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
            config.validate()
            return config
        except Exception:
            fallback = cls()
            fallback.validate()
            return fallback
