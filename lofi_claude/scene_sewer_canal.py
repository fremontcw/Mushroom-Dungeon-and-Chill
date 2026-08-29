"""SewerCanalScene

Side-on sewer: brick back wall along the top, a canal of slowly
flowing water beneath it, and a mossy stone walkway at the bottom.
Tiles are drawn at 2x. The water rows scroll sideways to read as flow.

Status:
    None
Issues:
    None
Todo:
    None
"""

from functools import cache

import pygame

from tileset_loader import TILE, tile

SCALE = 2
T = TILE * SCALE
COLS = 320 // T + 1
ROWS = 6  # wall + water rows + walkway rows
TOP = 180 - ROWS * T  # slightly negative: the wall's top edge runs off the top of the screen
WALL_TILES = [(5, 36), (6, 36)]
WATER_ROWS = [[(5, 37), (6, 37)], [(5, 38), (6, 38)], [(5, 38), (6, 38)]]
WALKWAY_TILES = [(4, 40), (5, 40), (6, 40)]
WALKWAY_ROWS = 2
FLOW_PX_PER_S = 6.0
WATER_TOP = TOP + T
WALKWAY_TOP = WATER_TOP + len(WATER_ROWS) * T


def _scaled(index: tuple[int, int]) -> pygame.Surface:
    return pygame.transform.scale(tile(*index), (T, T))


@cache
def _strip(tiles: tuple[tuple[int, int], ...], extra_cols: int = 0) -> pygame.Surface:
    strip = pygame.Surface(((COLS + extra_cols) * T, T)).convert()
    for col in range(COLS + extra_cols):
        strip.blit(_scaled(tiles[col % len(tiles)]), (col * T, 0))
    return strip


@cache
def _static_surface() -> pygame.Surface:
    surface = pygame.Surface((COLS * T, ROWS * T)).convert()
    surface.blit(_strip(tuple(WALL_TILES)), (0, 0))
    for row in range(WALKWAY_ROWS):
        surface.blit(_strip(tuple(WALKWAY_TILES)), (0, (1 + len(WATER_ROWS) + row) * T))
    return surface


def draw(surface: pygame.Surface, t: float) -> None:
    """Wall along the top, flowing water, walkway at the bottom."""
    surface.fill((0, 0, 0))
    surface.blit(_static_surface(), (0, TOP))
    offset = int(t * FLOW_PX_PER_S) % T
    for row, tiles in enumerate(WATER_ROWS):
        surface.blit(_strip(tuple(tiles), 1), (-offset, WATER_TOP + row * T))
