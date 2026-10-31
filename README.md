# SINGULARITY // Arabic Gravitational Art Engine
### Relativistic Black Hole Generative-Art Simulation in Arabic Typography

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pytest: 40 Passed](https://img.shields.io/badge/tests-40%20passed-brightgreen.svg)]()
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%99%A5-red.svg)](LICENSE)
[![اقرأ بالعربية](https://img.shields.io/badge/Language-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-green.svg)](README_AR.md)

> **SINGULARITY** is an interactive, real-time generative-art engine and relativistic astrophysical simulation that renders curved spacetime, accretion disk dynamics, and gravitational lensing primarily through **Arabic typography** as the visual matter.

[**📖 اقرأ دليل التوثيق الكامل باللغة العربية (Read in Arabic)**](README_AR.md)

---

## Table of Contents
1. [Overview](#overview)
2. [Astrophysical & Mathematical Foundations](#astrophysical--mathematical-foundations)
3. [Arabic Typography System](#arabic-typography-system)
4. [Key Features & Visual Effects](#key-features--visual-effects)
5. [Prerequisites & Environment](#prerequisites--environment)
6. [Step-by-Step Installation (Windows & Linux)](#step-by-step-installation)
7. [Running & CLI Usage](#running--cli-usage)
8. [Interactive Controls & HUD](#interactive-controls--hud)
9. [Automated Testing](#automated-testing)
10. [License](#license)

---

## Overview

Rather than relying on conventional textured polygons or wireframe meshes, **SINGULARITY** constructs the celestial geometry of a Schwarzschild black hole from thousands of active **Arabic characters**. Characters rotate, plunge, and stretch in accordance with relativistic gravitational dynamics, aligning with orbital stream lines like luminous cosmic calligraphy.

The visual identity is cinematic, scientific, and elegant—deliberately avoiding generic green terminal clichés. The simulation achieves **60 FPS** on standard hardware through vectorized Struct-of-Arrays (SoA) particle pools and a quantized glyph cache.

---

## Astrophysical & Mathematical Foundations

The simulation implements real general-relativistic approximations:

### 1. Unified Spatial Scale ($R_s$)
All scene entities adhere to a single unified scale governed by the **Schwarzschild radius ($R_s$)**:
* **Event Horizon:** Fixed at $1.0 \, R_s$ (consuming boundary).
* **Photon Sphere:** Positioned at $1.5 \, R_s$ where unstable circular photon orbits create the luminous ring.
* **Innermost Stable Circular Orbit (ISCO):** Positioned at $3.0 \, R_s$. Matter crossing inside ISCO plunges rapidly into the event horizon.
* **Accretion Disk:** Extends from $3.0 \, R_s$ to $20.0 \, R_s$.
* **Vertical Scale Height:** Follows physical gas disk geometry $H(r) = 0.03 \, r$.

### 2. Shakura-Sunyaev Temperature Profile
Disk emission and radiation follow the standard thin-disk model:
$$T(r) = T_{\text{peak}} \cdot \left(\frac{r}{r_{\text{in}}}\right)^{-3/4} \left[1 - \sqrt{\frac{r_{\text{in}}}{r}}\right]^{1/4}$$
Reaching peak temperature at $r \approx 4.08 \, R_s$, smoothly transitioning from incandescent white-gold core to solar orange and deep crimson rim.

### 3. Paczyński-Wiita Orbital Dynamics
Pseudo-Newtonian relativistic angular velocity reproduces circular orbits:
$$\Omega(r) = \frac{\sqrt{GM}}{r^{1/2}(r - R_s)}$$
Causing characters near the horizon to whip in tight, accelerating relativistic spirals.

### 4. Relativistic Doppler Beaming
Matter orbiting toward the line of sight is amplified by the relativistic beaming factor $\delta^3$:
$$\delta = \frac{1}{\gamma (1 - \beta \cos\theta)}$$
Creating the signature Event Horizon Telescope (EHT) brightness asymmetry.

### 5. Gravitational Lensing & Far-Disk Elevation
Light from the far side of an inclined accretion disk bends over the top and bottom of the event horizon, rendering the iconic halo arc.

### 6. Gravitational Wave Ripples
Whenever matter crosses the event horizon, a quasinormal spacetime metric perturbation expands outward across the disk plane, dissipating at relativistic speeds.

---

## Arabic Typography System

* **28 Alphabet Glyphs by Default:** The core plasma is composed of pure isolated Arabic letters.
* **Contextual Reshaping & BiDi Layout:** Uses `arabic-reshaper` and `python-bidi` for full right-to-left glyph connectivity when rendering words and phrases.
* **Tangential Flow Alignment:** Character rotation angles dynamically align with orbital velocity streamlines:
  $$\theta_{\text{flow}} = 90^\circ + \arctan2(v_z, v_x)$$
* **Typography Modes:**
  * **Letters (`letters`):** All 28 Arabic alphabet characters.
  * **Words (`words`):** Cosmological terms (*جاذبية، أفق الحدث، ثقب أسود، تفرد، نور، سرمدي، زمكان*).
  * **Phrases (`phrases`):** Astronomical and philosophical verses (*في فلك يسبحون، والنجم إذا هوى*).
  * **Mixed (`mixed`):** A dynamic composite stream.

---

## Key Features & Visual Effects

* **Cinematic Auto-Tour Mode (`[C]`):** Hands-free autonomous orbital camera that glides 360° around the black hole while smoothly oscillating between face-on circular view and edge-on lensing halo.
* **Gravitational Wave Ripples:** Relativistic ripple emissions upon particle absorption.
* **Glassmorphic Telemetry HUD:** Real-time diagnostics for FPS, absorbed matter, active particles, and parameter sliders.
* **5 Color Presets:** Solar Orange, Deep Blue, Purple Nebula, Monochrome, and Emerald Singularity.
* **Additive Multi-Pass Bloom & Phosphorescent Trails:** Smooth downscaled glow and motion blur.

---

## Step-by-Step Installation

### 1. Requirements
* Python 3.11 or higher (Python 3.14 fully supported).
* Windows, Linux, or macOS.

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/your-username/singularity.git
cd singularity

# Create and activate virtual environment
# Windows:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running & CLI Usage

### Launch Interactive Engine
```bash
python main.py
```
Or as a package:
```bash
python -m singularity
```

### CLI Arguments
| Argument | Description | Example |
| :--- | :--- | :--- |
| `--preset` | Color preset | `python main.py --preset deep_blue` |
| `--quality` | Quality preset (`LOW`, `MEDIUM`, `HIGH`) | `python main.py --quality HIGH` |
| `--mode` | Typography mode (`letters`, `words`, `phrases`, `mixed`) | `python main.py --mode phrases` |
| `--particles` | Initial particle pool size | `python main.py --particles 1800` |
| `--fullscreen` | Launch in fullscreen | `python main.py --fullscreen` |
| `--benchmark` | Run headless benchmark | `python main.py --benchmark 120` |

---

## Interactive Controls & HUD

| Key / Input | Action |
| :--- | :--- |
| **Mouse Left Drag** | Orbit camera 360° pitch and yaw |
| **Mouse Wheel / `+` / `-`** | 3D Perspective Zoom In / Out |
| **`C`** | **Toggle Cinematic Auto-Tour Mode** |
| **`Space`** | Pause / Resume simulation |
| **`H`** | Toggle HUD & Control Panel |
| **`R`** | Reset simulation |
| **`T`** | Cycle Typography Mode (Letters &rarr; Words &rarr; Phrases &rarr; Mixed) |
| **`Q`** | Cycle Quality Presets (LOW &rarr; MEDIUM &rarr; HIGH) |
| **`1` - `5`** | Switch Color Presets |
| **`P` or `F12`** | Capture high-resolution screenshot to `screenshots/` |
| **`F11`** | Toggle Fullscreen |
| **`Esc`** | Exit application |

---

## Automated Testing

Run the full automated test suite (40 unit tests):
```bash
pytest
```

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details. Open source and community friendly.
