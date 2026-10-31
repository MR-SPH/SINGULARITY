# Development & Contribution Guide

## 1. Environment Setup

### Prerequisites
- Python 3.11+ (Python 3.14 fully supported)
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/singularity.git
   cd singularity
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. Install runtime and development dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 2. Running the Application

### Interactive Engine
```bash
python main.py
```

### CLI Flags
```bash
# Run with a specific color preset
python main.py --preset deep_blue

# Set quality level (LOW, MEDIUM, HIGH)
python main.py --quality LOW

# Custom resolution
python main.py --width 1920 --height 1080 --fullscreen
```

---

## 3. Running Automated Tests

Run the full pytest suite:
```bash
pytest
```

Run headless benchmark to evaluate throughput:
```bash
python main.py --benchmark 180 --quality MEDIUM
```

---

## 4. Code Standards & Architecture Guidelines

- Maintain modular separation: physics algorithms belong in `src/singularity/physics/`, rendering code in `src/singularity/rendering/`, and typography in `src/singularity/typography/`.
- Never execute per-pixel loops in pure Python during real-time rendering. Use NumPy vectorized routines or cached lookups.
- Preserve Arabic text shaping rules. Avoid naive string slicing on reshaped Arabic text.

