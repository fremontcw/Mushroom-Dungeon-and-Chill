"""BigFungusWalkerSprite

Fungus folk, at native 1x, walking back and forth on their own lanes.
Deterministic in t. Background comes from a scene module drawn before this.

Status:
    None
Issues:
    None
Todo:
    None
"""

from functools import cache

import pygame

from sprite_fungus_walkers import FRAME_H, FRAME_W, ROW_LEFT, ROW_RIGHT, WALK_FPS
from tileset_loader import character_sheet

SCALE = 1
X_MIN, X_MAX = 8, 320 - 8 - FRAME_W * SCALE
# (sheet name, feet y, speed px/s, phase offset s, alpha) — sorted by feet y so lower walkers draw in front
WALKERS = [
    ("ghost", 70, 6.0, 4.0, 130),      # ghosts drift over the canal
    ("sheet10", 100, 5.0, 40.0, 110),
    ("red", 130, 14.0, 0.0, 255),      # walkway lanes, back to front
    ("sheet9", 130, 11.0, 61.0, 255),
    ("king", 146, 12.0, 17.0, 255),
    ("sheet7", 146, 16.0, 88.0, 255),
    ("violet", 162, 13.0, 33.0, 255),
    ("sheet8", 162, 9.0, 120.0, 255),
    ("sheet11", 178, 10.0, 52.0, 255),
    ("sheet12", 178, 15.0, 75.0, 255),
]


@cache
def _frame(name: str, step: int, row: int, alpha: int) -> pygame.Surface:
    src = character_sheet(name).subsurface(pygame.Rect(step * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H))
    frame = pygame.transform.scale(src, (FRAME_W * SCALE, FRAME_H * SCALE))
    if alpha < 255:
        frame.set_alpha(alpha)
    return frame


def position(speed: float, phase: float, t: float) -> tuple[int, bool]:
    """Return (x, facing_right) for a walker bouncing between X_MIN and X_MAX."""
    span = X_MAX - X_MIN
    d = ((t + phase) * speed) % (2 * span)
    facing_right = d < span
    return int(X_MIN + (d if facing_right else 2 * span - d)), facing_right


def draw_walkers(surface: pygame.Surface, t: float) -> None:
    """Draw every walker on its lane, lowest lane last so it is in front."""
    step = [0, 1, 2, 1][int(t * WALK_FPS) % 4]
    for name, feet_y, speed, phase, alpha in WALKERS:
        x, facing_right = position(speed, phase, t)
        surface.blit(_frame(name, step, ROW_RIGHT if facing_right else ROW_LEFT, alpha), (x, feet_y - FRAME_H * SCALE))
