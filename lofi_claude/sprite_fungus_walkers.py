"""FungusWalkersSprite

Fungus folk pacing left and right across the cave floor on their own lanes,
using the pack's 3-frame walk cycles. Deterministic in t.

Status:
    None
Issues:
    None
Todo:
    None
"""

import pygame

from tileset_loader import character_sheet

FRAME_W, FRAME_H = 16, 32
ROW_LEFT, ROW_RIGHT = 1, 2
WALK_FPS = 6
X_MIN, X_MAX = 8, 296
# (sheet name, lane y in px, speed px/s, phase offset s, alpha)
WALKERS = [
    ("red", 60, 22.0, 0.0, 255),
    ("king", 84, 14.0, 7.0, 255),
    ("violet", 110, 26.0, 3.0, 255),
    ("ghost", 138, 10.0, 11.0, 150),
]


def walker_position(lane_y: int, speed: float, phase: float, t: float) -> tuple[int, int, bool]:
    """Return (x, y, facing_right) for a walker bouncing between X_MIN and X_MAX."""
    span = X_MAX - X_MIN
    d = ((t + phase) * speed) % (2 * span)
    facing_right = d < span
    x = X_MIN + (d if facing_right else 2 * span - d)
    return int(x), lane_y - FRAME_H, facing_right


def _frame(name: str, facing_right: bool, t: float) -> pygame.Surface:
    step = [0, 1, 2, 1][int(t * WALK_FPS) % 4]  # ping-pong through the 3 frames
    row = ROW_RIGHT if facing_right else ROW_LEFT
    return character_sheet(name).subsurface(pygame.Rect(step * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H))


def draw(surface: pygame.Surface, t: float) -> None:
    """Draw every walker at its position for time t."""
    for name, lane_y, speed, phase, alpha in WALKERS:
        x, y, facing_right = walker_position(lane_y, speed, phase, t)
        frame = _frame(name, facing_right, t)
        if alpha < 255:
            frame = frame.copy()
            frame.set_alpha(alpha)
        surface.blit(frame, (x, y))
