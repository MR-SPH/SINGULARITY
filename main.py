#!/usr/bin/env python3
"""SINGULARITY: Arabic Gravitational Art Engine

Root launcher script.
"""

import os
import sys

# Ensure src/ is in python path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from singularity.main import main, run_benchmark

if __name__ == "__main__":
    main()
