"""FungusCaveSceneRenderCheck

Headless smoke check: frames render without error, a walker is on screen,
and walkers actually move between frames.

Status:
    None
Issues:
    None
Todo:
    None
"""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame  # noqa: E402

pygame.display.init()
pygame.display.set_mode((1, 1))

import main  # noqa: E402
from sprite_fungus_walkers import WALKERS, walker_position  # noqa: E402

native = pygame.Surface(main.NATIVE_SIZE).convert()
for layers in (main.SIMPLE_LAYERS, main.CAVE_LAYERS):
    for t in (0.0, 1.5, 31.05):
        for draw_layer in layers:
            draw_layer(native, t)
name, lane_y, speed, phase, _ = WALKERS[0]
x0 = walker_position(lane_y, speed, phase, 0.0)[0]
x1 = walker_position(lane_y, speed, phase, 1.0)[0]
assert x0 != x1, "walker did not move"
x, y, _ = walker_position(lane_y, speed, phase, 31.05)
assert native.get_at((x + 8, y + 10))[:3] != native.get_at((x + 8, y + 40))[:3], "walker not drawn"
print("ok")
