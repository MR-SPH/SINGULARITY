"""Package execution entry point: python -m singularity"""
import os
import sys

# Auto-resolve parent src directory when executed directly
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from singularity.main import main

if __name__ == "__main__":
    main()
