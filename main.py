#!/usr/bin/env python3
"""SINGULARITY: Arabic Gravitational Art Engine

Root launcher script with auto-path resolution and auto-venv detection.
"""

import os
import sys
import subprocess

def _resolve_environment():
    # If running as a frozen PyInstaller executable, skip venv and src lookup
    if getattr(sys, "frozen", False):
        return

    # 1. Determine script directory
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()

    # 2. If not running inside .venv, check if local .venv exists and re-execute
    venv_candidates = [
        os.path.join(script_dir, ".venv", "Scripts", "python.exe"),
        os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"),
        os.path.join(script_dir, "..", ".venv", "Scripts", "python.exe"),
    ]
    for venv_py in venv_candidates:
        if os.path.isfile(venv_py):
            # Check if current interpreter is different from venv interpreter
            if os.path.abspath(sys.executable).lower() != os.path.abspath(venv_py).lower():
                try:
                    result = subprocess.run([venv_py, os.path.abspath(__file__)] + sys.argv[1:])
                    sys.exit(result.returncode)
                except Exception:
                    pass
            break

    # 3. Robustly resolve 'src' directory containing 'singularity'
    search_dirs = [
        os.path.join(script_dir, "src"),
        os.path.join(os.getcwd(), "src"),
        os.path.join(script_dir, "..", "src"),
        os.path.join(os.getcwd(), "..", "src"),
        os.path.join(script_dir, "SINGULARITY", "src"),
        os.path.join(os.getcwd(), "SINGULARITY", "src"),
        script_dir,
        os.getcwd(),
    ]
    for candidate in search_dirs:
        check_path = candidate if os.path.basename(candidate) == "src" else os.path.join(candidate, "src")
        if os.path.isdir(os.path.join(check_path, "singularity")):
            norm_path = os.path.normpath(check_path)
            if norm_path not in sys.path:
                sys.path.insert(0, norm_path)
            break

_resolve_environment()

try:
    from singularity.main import main, run_benchmark
except ModuleNotFoundError as e:
    print(f"\n[ERROR] Could not import singularity: {e}")
    print("Please make sure you are running main.py from the project root or use run.bat.")
    print("If you have not installed dependencies yet, run:")
    print("    pip install -r requirements.txt\n")
    sys.exit(1)

if __name__ == "__main__":
    main()
