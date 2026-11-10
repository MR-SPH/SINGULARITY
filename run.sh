#!/usr/bin/env bash
# =====================================================================
#    SINGULARITY - Arabic Gravitational Art Engine
#    Linux & macOS One-Click Launcher Script
# =====================================================================

set -e

# 1. Anchor working directory to script location
cd "$(dirname "$0")"

echo "====================================================================="
echo "   SINGULARITY - Arabic Gravitational Art Engine"
echo "====================================================================="
echo ""

# 2. Check for Python installation (python3 or python)
if command -v python3 >/dev/null 2>&1; then
    PY_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PY_BIN="python"
else
    echo "[ERROR] Python was not found on your system!"
    echo "Please install Python 3.11+ using your package manager (e.g., sudo apt install python3 python3-venv)"
    exit 1
fi

# 3. Setup Virtual Environment if missing
if [ ! -f ".venv/bin/python" ]; then
    echo "[*] Virtual environment not found. Creating .venv ..."
    "$PY_BIN" -m venv .venv
    echo "[*] Virtual environment created successfully."
fi

# 4. Check dependencies and install if missing
if ! .venv/bin/python -c "import pygame, numpy" >/dev/null 2>&1; then
    echo "[*] Installing required dependencies from requirements.txt ..."
    .venv/bin/python -m pip install --upgrade pip --quiet
    .venv/bin/python -m pip install -r requirements.txt
    echo "[*] All dependencies are ready."
    echo ""
fi

# 5. Launch Application
echo "====================================================================="
echo "Launching SINGULARITY..."
echo "Controls: [C] Cinematic Tour - [H] HUD - [Space] Pause - [Esc] Exit"
echo "====================================================================="
echo ""

.venv/bin/python main.py "$@"

