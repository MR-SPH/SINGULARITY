# SINGULARITY // Arabic Gravitational Art Engine

[![CI](https://github.com/your-username/singularity/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/singularity/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **SINGULARITY** is an interactive, real-time generative-art engine and relativistic black hole simulator that renders spacetime curvature, accretion dynamics, and gravitational lensing primarily through **Arabic typography**.

---

## Overview

Rather than relying on conventional textured polygons or wireframe meshes, **SINGULARITY** constructs the celestial geometry of a black hole from Arabic character particles. Characters rotate, plunge, and stretch in accordance with relativistic gravitational dynamics, aligning with orbital stream lines like luminous cosmic calligraphy.

The engine features physically grounded approximations of general relativistic effects, including the **Innermost Stable Circular Orbit (ISCO = 3 Rs)**, **Relativistic Doppler Beaming**, **Schwarzschild Event Horizon absorption**, and **Screen-Space Gravitational Lensing**.

---

## Key Features

- **Relativistic Astrophysics Engine**:
  - **Schwarzschild Event Horizon ($R_s = 2GM/c^2$)**: True consuming boundary where matter is pulled across the horizon into the singularity.
  - **Paczyński-Wiita Potential**: Reproduces the exact general relativistic ISCO at $3 R_s$, driving matter into sudden relativistic plunge.
  - **Relativistic Doppler Beaming**: Recreates the signature asymmetry seen in Event Horizon Telescope (EHT) imagery — matter approaching the observer is blazingly amplified and bluer, while receding matter is dimmer and redshifted.
  - **Gravitational Lensing & Photon Ring**: Background stars bend around the black hole, producing Einstein arcs and magnification.

- **Arabic Typography System**:
  - **Pure Alphabet Particle Default**: Features all 28 traditional Arabic letters as distinct swirling stellar particles.
  - **Tangential Streamline Alignment**: Glyphs dynamically align their orientation with the local orbital velocity vector, creating a harmonious liquid plasma flow.
  - **Contextual Shaping & BiDi Layout**: Proper RTL glyph connectivity powered by `arabic-reshaper` and `python-bidi`.
  - **Extended Modes**: Switch instantly between Letters, Cosmological Words (*جاذبية، أفق الحدث، ثقب أسود، تفرد*), Philosophical Verses, and Mixed modes.

- **Cinematic Multi-Pass Rendering**:
  - **Phosphorescent Decay Trails**: Hardware-accelerated motion blur with `BLEND_SUB`.
  - **Multi-Layer 3D Depth**: True depth-sorted rendering separating background disk particles, central shadow occlusion, and foreground disk particles.
  - **Additive Bloom Glow**: Multi-pass downsampled bloom creating realistic luminosity around the inner disk and photon sphere.
  - **Cosmic Starfield**: Depth-layered starfield with scintillation and relativistic deflection.

- **Hardware-Aware Real-Time Performance**:
  - Sustains **60 FPS** on dual-core CPUs with integrated graphics through a **2-tier quantized glyph cache** and **Struct-of-Arrays (SoA)** NumPy vectorization.
  - 3 Performance presets: `LOW`, `MEDIUM`, `HIGH`.

- **Interactive Telemetry HUD**:
  - Collapsible 4-tab glassmorphic dock (*Physics, Visuals, Layers, System*).
  - Real-time gauges: FPS, frame time, active particle count, total absorbed matter counter.

---

## Color Presets

| Preset | Inspiration | Primary Palette |
| :--- | :--- | :--- |
| **Solar Orange** | Event Horizon Telescope (EHT) / M87* | Pure White &rarr; Brilliant Gold &rarr; Solar Orange &rarr; Deep Crimson |
| **Deep Blue** | Cherenkov Quasar & Active Galactic Nuclei | Cyan White &rarr; Electric Blue &rarr; Midnight Azure &rarr; Deep Space |
| **Purple Nebula** | Cosmic Ultraviolet & Gravitational Jet | Pearl White &rarr; Radiant Magenta &rarr; Nebula Violet &rarr; Obsidian |
| **Monochrome** | Scientific Gravitational Minimalist | Pure White &rarr; High-Contrast Greyscale &rarr; Pitch Black |
| **Emerald** | Synchrotron Radio Emission | Mint White &rarr; Electric Emerald &rarr; Jade Green &rarr; Deep Forest |

---

## Interactive Controls

| Control | Action |
| :--- | :--- |
| **Left / Right Mouse Drag** | Orbit camera yaw and pitch in 3D |
| **Mouse Wheel / `+` / `-`** | Zoom in / Zoom out |
| **Arrow Keys** | Smooth keyboard camera orbit |
| **`SPACE`** | Pause / Resume simulation |
| **`H`** | Toggle HUD & Control Panel visibility |
| **`1` - `5`** | Switch Color Presets (*Solar, Blue, Purple, Mono, Emerald*) |
| **`T`** | Cycle Typography Mode (*Letters &rarr; Words &rarr; Phrases &rarr; Mixed*) |
| **`Q`** | Cycle Performance Quality (*LOW &rarr; MEDIUM &rarr; HIGH*) |
| **`R`** | Reset simulation |
| **`P` or `F12`** | Capture high-resolution screenshot to `screenshots/` |
| **`F11`** | Toggle Fullscreen |
| **`ESC`** | Exit Application |

---

## Installation & Quick Start

### 1. Requirements
- Python 3.11 or higher (Python 3.14 fully supported).
- Windows, Linux, or macOS.

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/your-username/singularity.git
cd singularity

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running
```bash
# Launch interactive application
python main.py

# Launch with specific options
python main.py --preset deep_blue --quality HIGH

# Launch in fullscreen
python main.py --fullscreen
```

### 4. Running Headless Benchmark
```bash
python main.py --benchmark 180 --quality MEDIUM
```

---

## Automated Testing

Execute the comprehensive test suite with `pytest`:
```bash
pytest
```
All 25 automated tests validate relativistic velocity curves, ISCO instability, Doppler beaming factors, particle pool invariants, Arabic text shaping, and JSON configuration validation.

---

## Architecture Overview

```
singularity/
├── main.py                  # CLI and application entry point
├── pyproject.toml           # Package configuration & test rules
├── requirements.txt         # Pinned runtime dependencies
├── assets/
│   ├── fonts/               # Arabic OpenType/TrueType fonts
│   └── presets/             # Saved configuration templates
├── src/singularity/
│   ├── core/                # Engine loop, state machine, and JSON config
│   ├── physics/             # Relativistic potential, ISCO, Doppler, and lensing
│   ├── typography/          # Arabic reshaping, BiDi, and quantized glyph cache
│   ├── particles/           # Vectorized Struct-of-Arrays particle pool & emitter
│   ├── rendering/           # Camera, starfield, effects, and multi-pass pipeline
│   ├── ui/                  # Collapsible glassmorphic dock & telemetry HUD
│   └── utilities/           # Math utilities, profiler, and color interpolation
├── tests/                   # 25 automated unit tests
└── docs/                    # Architectural and developer documentation
```

---

## Roadmap

- [x] Vectorized Struct-of-Arrays particle pool.
- [x] Relativistic Doppler beaming and Paczyński-Wiita ISCO modeling.
- [x] Contextual Arabic typography with stream-aligned orientation.
- [x] Discrete 2-tier glyph cache for 60 FPS performance on dual-core hardware.
- [ ] Add Kerr (rotating) black hole frame-dragging / ergosphere visualization.
- [ ] Implement audio-reactive gravitational pulse spectrum analyzer.
- [ ] WebAssembly / WebGL export for browser execution.

---

## License

This project is licensed under the [MIT License](LICENSE).

