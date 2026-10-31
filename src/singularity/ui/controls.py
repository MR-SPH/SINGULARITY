"""Interactive UI widgets: Sliders, Buttons, and Toggle switches with modern glassmorphism."""

from typing import Callable, Optional, Tuple
import pygame

# UI Color palette
COLOR_BG_PANEL = (15, 18, 24, 225)
COLOR_BORDER = (55, 68, 88)
COLOR_TEXT_TITLE = (240, 245, 255)
COLOR_TEXT_BODY = (180, 195, 215)
COLOR_TEXT_DIM = (110, 125, 145)
COLOR_ACCENT = (255, 175, 45)
COLOR_ACCENT_HOVER = (255, 205, 90)
COLOR_TRACK = (35, 42, 55)
COLOR_TRACK_FILL = (230, 140, 30)
COLOR_BUTTON = (30, 38, 52)
COLOR_BUTTON_HOVER = (45, 58, 78)


class UISlider:
    """Draggable numeric slider widget."""

    def __init__(
        self,
        rect: pygame.Rect,
        label: str,
        min_val: float,
        max_val: float,
        val: float,
        step: float = 0.01,
        format_str: str = "{:.2f}",
        on_change: Optional[Callable[[float], None]] = None
    ):
        self.rect = rect
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.val = val
        self.step = step
        self.format_str = format_str
        self.on_change = on_change
        self.is_dragging = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events. Returns True if event was consumed."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self._update_val_from_mouse(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self._update_val_from_mouse(event.pos[0])
                return True
        return False

    def _update_val_from_mouse(self, mouse_x: int) -> None:
        track_x = self.rect.x
        track_w = self.rect.width
        t = max(0.0, min(1.0, (mouse_x - track_x) / float(track_w)))
        raw_val = self.min_val + t * (self.max_val - self.min_val)
        if self.step > 0:
            raw_val = round(raw_val / self.step) * self.step
        self.val = max(self.min_val, min(self.max_val, raw_val))
        if self.on_change:
            self.on_change(self.val)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        # Label & value text
        val_str = self.format_str.format(self.val)
        lbl_surf = font.render(f"{self.label}: {val_str}", True, COLOR_TEXT_BODY)
        surface.blit(lbl_surf, (self.rect.x, self.rect.y - 18))

        # Track background
        pygame.draw.rect(surface, COLOR_TRACK, self.rect, border_radius=4)

        # Track filled portion
        t = (self.val - self.min_val) / max(1e-5, (self.max_val - self.min_val))
        fill_w = int(self.rect.width * t)
        if fill_w > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.rect.height)
            pygame.draw.rect(surface, COLOR_TRACK_FILL, fill_rect, border_radius=4)

        # Handle knob
        knob_x = self.rect.x + fill_w
        knob_y = self.rect.centery
        knob_color = COLOR_ACCENT_HOVER if self.is_dragging else COLOR_ACCENT
        pygame.draw.circle(surface, knob_color, (knob_x, knob_y), 6)


class UIButton:
    """Clickable interactive button widget."""

    def __init__(
        self,
        rect: pygame.Rect,
        label: str,
        on_click: Optional[Callable[[], None]] = None,
        color: Tuple[int, int, int] = COLOR_BUTTON
    ):
        self.rect = rect
        self.label = label
        self.on_click = on_click
        self.bg_color = color
        self.is_hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True
        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        col = COLOR_BUTTON_HOVER if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, col, self.rect, border_radius=5)
        border_col = COLOR_ACCENT if self.is_hovered else COLOR_BORDER
        pygame.draw.rect(surface, border_col, self.rect, width=1, border_radius=5)

        text_surf = font.render(self.label, True, COLOR_TEXT_TITLE if self.is_hovered else COLOR_TEXT_BODY)
        tx = self.rect.centerx - text_surf.get_width() // 2
        ty = self.rect.centery - text_surf.get_height() // 2
        surface.blit(text_surf, (tx, ty))


class UIToggle:
    """Toggle switch widget for boolean flags."""

    def __init__(
        self,
        rect: pygame.Rect,
        label: str,
        state: bool = True,
        on_change: Optional[Callable[[bool], None]] = None
    ):
        self.rect = rect
        self.label = label
        self.state = state
        self.on_change = on_change

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                if self.on_change:
                    self.on_change(self.state)
                return True
        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        # Checkbox box on the left
        box_size = self.rect.height
        box_rect = pygame.Rect(self.rect.x, self.rect.y, box_size, box_size)
        pygame.draw.rect(surface, COLOR_TRACK, box_rect, border_radius=3)
        pygame.draw.rect(surface, COLOR_BORDER, box_rect, width=1, border_radius=3)

        if self.state:
            inner_rect = box_rect.inflate(-6, -6)
            pygame.draw.rect(surface, COLOR_ACCENT, inner_rect, border_radius=2)

        lbl_surf = font.render(self.label, True, COLOR_TEXT_BODY if self.state else COLOR_TEXT_DIM)
        surface.blit(lbl_surf, (self.rect.x + box_size + 8, self.rect.y + 2))

