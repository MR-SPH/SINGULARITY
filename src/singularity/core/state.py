"""Mutable runtime state for the SINGULARITY interactive session."""

from dataclasses import dataclass, field
from typing import Tuple, Optional


@dataclass
class EngineState:
    """Live interactive state that changes during engine execution."""

    is_paused: bool = False
    time_scale: float = 1.0
    elapsed_time: float = 0.0
    frame_count: int = 0

    # Camera & navigation
    is_mouse_dragging: bool = False
    last_mouse_pos: Tuple[int, int] = (0, 0)
    target_pitch: float = 0.42
    target_yaw: float = 0.0
    target_zoom: float = 1.0

    # Cinematic auto-tour mode
    cinematic_mode: bool = False
    cinematic_timer: float = 0.0

    # Astrophysical event telemetry
    newly_absorbed_count: int = 0

    # Interaction & telemetry
    ui_visible: bool = True
    active_slider: Optional[str] = None
    status_notification: str = "SINGULARITY Initialized"
    notification_timer: float = 3.5

    # Trigger flags
    screenshot_requested: bool = False
    reset_requested: bool = False
    randomize_requested: bool = False

    def notify(self, message: str, duration: float = 2.5) -> None:
        """Display a temporary banner notification on the HUD."""
        self.status_notification = message
        self.notification_timer = duration

    def update_timers(self, dt: float) -> None:
        """Update notification and animation timers."""
        if self.notification_timer > 0.0:
            self.notification_timer = max(0.0, self.notification_timer - dt)
            if self.notification_timer == 0.0:
                self.status_notification = ""

