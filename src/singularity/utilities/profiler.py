"""Performance profiling and telemetry utilities for SINGULARITY."""

import time
from typing import Dict


class FrameProfiler:
    """Tracks frame times, stage durations, and computes moving-average FPS."""

    def __init__(self, history_size: int = 60):
        self.history_size = history_size
        self.frame_times = []
        self.stage_durations: Dict[str, float] = {}
        self.stage_start_times: Dict[str, float] = {}
        self._last_frame_time = time.perf_counter()
        self.current_fps: float = 60.0
        self.average_frame_time_ms: float = 16.6

    def start_frame(self) -> None:
        """Call at the beginning of each frame loop."""
        now = time.perf_counter()
        dt = now - self._last_frame_time
        self._last_frame_time = now

        if dt > 0.0:
            self.frame_times.append(dt)
            if len(self.frame_times) > self.history_size:
                self.frame_times.pop(0)

            avg_dt = sum(self.frame_times) / len(self.frame_times)
            self.current_fps = 1.0 / avg_dt if avg_dt > 0 else 60.0
            self.average_frame_time_ms = avg_dt * 1000.0

    def start_stage(self, stage_name: str) -> None:
        """Record the start timestamp of a rendering/physics stage."""
        self.stage_start_times[stage_name] = time.perf_counter()

    def end_stage(self, stage_name: str) -> None:
        """Record the completion of a rendering/physics stage."""
        if stage_name in self.stage_start_times:
            elapsed = (time.perf_counter() - self.stage_start_times[stage_name]) * 1000.0
            # Exponential moving average for stage timing
            prev = self.stage_durations.get(stage_name, elapsed)
            self.stage_durations[stage_name] = prev * 0.8 + elapsed * 0.2

    def get_summary(self) -> Dict[str, float]:
        """Return FPS, average frame time, and individual stage metrics."""
        summary = {
            "fps": round(self.current_fps, 1),
            "frame_time_ms": round(self.average_frame_time_ms, 2)
        }
        for stage, duration in self.stage_durations.items():
            summary[f"{stage}_ms"] = round(duration, 2)
        return summary

