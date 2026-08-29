"""FungusCaveTilesetLoader

Loads the 16x16 tileset once and hands out tiles by (column, row) index.

Status:
    None
Issues:
    None
Todo:
    None
"""

from functools import cache
from pathlib import Path

import pygame

TILE = 16
ASSETS_DIR = Path(__file__).parent / "assets"


@cache
def _sheet() -> pygame.Surface:
    return pygame.image.load(ASSETS_DIR / "fungus_cave_tileset_16x16.png").convert_alpha()


@cache
def tile(col: int, row: int, cols: int = 1, rows: int = 1) -> pygame.Surface:
    """Return the tile (or cols x rows block of tiles) at grid position (col, row)."""
    return _sheet().subsurface(pygame.Rect(col * TILE, row * TILE, cols * TILE, rows * TILE))


@cache
def character_sheet(name: str) -> pygame.Surface:
    """Return a character walk sheet: 3 columns x 4 rows (down, left, right, up) of 16x32 frames."""
    return pygame.image.load(ASSETS_DIR / f"fungus_{name}.png").convert_alpha()
