# Changelog

All notable changes to **SINGULARITY** will be documented in this file.

## [1.0.0] - 2026-10-31

### Added
- **Core Engine**: Full interactive real-time simulation using `pygame-ce` and `numpy`.
- **Relativistic Physics**:
  - Schwarzschild Event Horizon boundary and absorption mechanism.
  - Innermost Stable Circular Orbit (ISCO = 3 Rs) via the Paczyński-Wiita potential.
  - Relativistic Doppler beaming / boosting creating asymmetric accretion disk luminosity.
  - Screen-space gravitational lensing deflection and photon sphere ring.
- **Arabic Typography System**:
  - Contextual reshaping and BiDi support for connected and isolated glyphs.
  - Standard 28 Arabic alphabet letters set as the default typography particles.
  - Tangential orbital alignment of characters along disk streamlines.
  - Support for cosmological words, philosophical phrases, and mixed modes.
- **Rendering Pipeline**:
  - Multi-pass composition: Background, lensed starfield, back disk, event horizon, front disk, additive bloom, and UI.
  - Fast phosphorescent trail decay via hardware `BLEND_SUB`.
  - Discrete 2-tier glyph cache achieving 60 FPS on dual-core CPUs.
- **Interactive UI**:
  - 4-tab glassmorphic control dock (Physics, Visuals, Layers, System).
  - Real-time telemetry HUD displaying live FPS, frame times, particle counts, and absorbed counts.
  - 5 curated color presets: Solar Orange, Deep Blue, Purple Nebula, Monochrome, and Emerald.
- **Automated Verification**:
  - Comprehensive pytest test suite with 25 unit tests across physics, particles, typography, and config.
  - Headless benchmark mode (`--benchmark`) for automated performance analysis.

