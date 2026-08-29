"""FungusCaveTilemapScene

Draws the cave: stone floor, brick back wall, big mushrooms, barrels, crates,
and the animated torches and campfire. Tile indices refer to the tileset grid.

Status:
    None
Issues:
    None
Todo:
    None
"""

import math
from functools import cache

import pygame

from tileset_loader import TILE, tile

COLS, ROWS = 20, 12
WALL_ROWS = 3
FLOOR_TILES = [(6, 3), (7, 3), (6, 4), (7, 4)]
WALL_ROW_TILES = [12, 13, 14]  # cap, upper brick, lower brick
# (col, row, tileset col, tileset row, width, height) — static props, drawn in list order
PROPS = [
    (1, 2, 0, 21, 2, 4),    # big mushroom left
    (16, 6, 0, 21, 2, 4),   # big mushroom right
    (18, 3, 6, 18, 1, 1), (19, 3, 7, 18, 1, 1),   # barrels
    (18, 10, 2, 30, 1, 1), (19, 9, 4, 29, 1, 2),  # crates
    (0, 9, 4, 15, 1, 1),    # chest
    (4, 8, 0, 25, 1, 1), (12, 10, 2, 25, 1, 1), (15, 4, 0, 25, 1, 1),  # small mushrooms
    (7, 10, 3, 11, 1, 1), (10, 4, 0, 11, 1, 1),   # bone debris
]
TORCH_FRAMES = [(3, 27), (4, 27), (5, 27)]
TORCH_POSITIONS = [(6, 2), (13, 2)]
CAMPFIRE_FRAMES = [(3, 28), (4, 28), (5, 28)]
CAMPFIRE_POSITION = (9, 7)
GLOW_OUTER = (34, 18, 6)   # additive, so these are dim by design
GLOW_INNER = (30, 16, 5)


FLICKER_STEPS = 8


@cache
def _glow_surface(radius: int, step: int) -> pygame.Surface:
    flicker = 0.75 + 0.25 * step / (FLICKER_STEPS - 1)
    glow = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(glow, tuple(int(c * flicker) for c in GLOW_OUTER), (radius, radius), radius)
    pygame.draw.circle(glow, tuple(int(c * flicker) for c in GLOW_INNER), (radius, radius), radius // 2, 0)
    return glow


def _draw_glow(surface: pygame.Surface, center: tuple[int, int], radius: int, t: float, seed: int) -> None:
    step = int((math.sin(t * 9 + seed) + 1) / 2 * (FLICKER_STEPS - 1))
    surface.blit(_glow_surface(radius, step), (center[0] - radius, center[1] - radius), special_flags=pygame.BLEND_RGB_ADD)


@cache
def _ground_surface() -> pygame.Surface:
    surface = pygame.Surface((COLS * TILE, ROWS * TILE)).convert()
    for row in range(ROWS):
        for col in range(COLS):
            if row < WALL_ROWS:
                surface.blit(tile(col % 3, WALL_ROW_TILES[row]), (col * TILE, row * TILE))
            else:
                surface.blit(tile(*FLOOR_TILES[(col * 7 + row * 3) % 4]), (col * TILE, row * TILE))
    for col, row, tc, tr, w, h in PROPS:
        surface.blit(tile(tc, tr, w, h), (col * TILE, row * TILE))
    return surface


def draw_ground(surface: pygame.Surface, t: float) -> None:
    """Blit the pre-rendered floor, back wall and static props."""
    surface.blit(_ground_surface(), (0, 0))


def draw_fire(surface: pygame.Surface, t: float) -> None:
    """Draw animated torches and campfire with flickering glow; call after the walkers."""
    frame = int(t * 6) % 3
    for i, (col, row) in enumerate(TORCH_POSITIONS):
        surface.blit(tile(*TORCH_FRAMES[frame]), (col * TILE, row * TILE))
        _draw_glow(surface, (col * TILE + 8, row * TILE + 6), 28, t, i)
    col, row = CAMPFIRE_POSITION
    surface.blit(tile(*CAMPFIRE_FRAMES[(frame + 1) % 3]), (col * TILE, row * TILE))
    _draw_glow(surface, (col * TILE + 8, row * TILE + 8), 40, t, 5)
