"""SINGULARITY: Arabic Gravitational Art Engine

CLI entry point module.
"""

import argparse
import sys
import os

from singularity.core.config import EngineConfig, COLOR_PRESETS, QUALITY_PRESETS
from singularity.core.engine import SingularityEngine
from singularity.core.simulation import BlackHoleSimulation
from singularity.core.state import EngineState
from singularity.typography.fonts import FontManager
from singularity.rendering.renderer import SingularityRenderer
from singularity.utilities.profiler import FrameProfiler


def run_benchmark(frames: int = 300, quality: str = "MEDIUM") -> None:
    """Run headless benchmark simulation to verify performance and throughput."""
    import pygame
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()

    print(f"=== SINGULARITY HEADLESS BENCHMARK [{quality}] ===")
    config = EngineConfig()
    config.apply_quality_preset(quality)
    state = EngineState()
    profiler = FrameProfiler()

    screen = pygame.display.set_mode((config.window_width, config.window_height))
    font_manager = FontManager()
    sim = BlackHoleSimulation(config, state)
    renderer = SingularityRenderer(config, font_manager)

    dt = 1.0 / 60.0
    for f in range(frames):
        profiler.start_frame()
        sim.step(dt)
        renderer.camera.update(dt)
        renderer.render(screen, sim.particle_system, state, profiler)

    summary = profiler.get_summary()
    print(f"Rendered {frames} frames.")
    print(f"Average FPS: {summary['fps']}")
    print(f"Average Frame Time: {summary['frame_time_ms']} ms")
    print(f"Absorbed particles: {sim.particle_system.total_absorbed}")
    print("Benchmark complete: SUCCESS")
    pygame.quit()


def main():
    parser = argparse.ArgumentParser(
        description="SINGULARITY: Arabic Gravitational Art Engine"
    )
    parser.add_argument("--config", type=str, default="config.json", help="Path to config file")
    parser.add_argument("--preset", type=str, choices=list(COLOR_PRESETS.keys()), help="Color preset")
    parser.add_argument("--quality", type=str, choices=["LOW", "MEDIUM", "HIGH"], default="MEDIUM", help="Quality preset")
    parser.add_argument("--mode", type=str, choices=["letters", "words", "phrases", "mixed"], help="Typography mode")
    parser.add_argument("--particles", type=int, help="Initial particle count")
    parser.add_argument("--width", type=int, help="Window width")
    parser.add_argument("--height", type=int, help="Window height")
    parser.add_argument("--fullscreen", action="store_true", help="Launch in fullscreen mode")
    parser.add_argument("--benchmark", type=int, nargs="?", const=180, help="Run headless benchmark for N frames")

    args = parser.parse_args()

    if args.benchmark is not None:
        run_benchmark(frames=args.benchmark, quality=args.quality)
        return

    # Load configuration
    config = EngineConfig.load_from_file(args.config)
    if args.quality:
        config.apply_quality_preset(args.quality)
    if args.preset:
        config.color_preset = args.preset
    if args.mode:
        config.typography_mode = args.mode
    if args.particles:
        config.max_particles = args.particles
    if args.width:
        config.window_width = args.width
    if args.height:
        config.window_height = args.height
    if args.fullscreen:
        config.fullscreen = True

    config.validate()

    engine = SingularityEngine(config=config, config_path=args.config)
    engine.run()


if __name__ == "__main__":
    main()
