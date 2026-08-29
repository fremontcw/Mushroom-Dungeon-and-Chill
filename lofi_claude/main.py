"""LofiClaudeMain

Entry point: opens the display, starts the dungeon music, runs the 30 fps loop,
draws the 320x180 native cave scene and nearest-neighbour scales it to the window.

Status:
    None
Issues:
    None
Todo:
    None
"""

import sys

import pygame

import music_dungeon_playback
import scene_sewer_canal
import scene_cave_tilemap
import sprite_big_walker
import sprite_fungus_walkers

NATIVE_SIZE = (320, 180)
FPS = 30
CAVE_LAYERS = (
    scene_cave_tilemap.draw_ground,
    sprite_fungus_walkers.draw,
    scene_cave_tilemap.draw_fire,
)
SIMPLE_LAYERS = (scene_sewer_canal.draw, sprite_big_walker.draw_walkers)
SCENE_LAYERS = CAVE_LAYERS if "--cave" in sys.argv else SIMPLE_LAYERS


def draw_scene(native: pygame.Surface, t: float) -> None:
    """Draw every layer, back to front, at time t seconds."""
    for draw_layer in SCENE_LAYERS:
        draw_layer(native, t)


def run(windowed: bool) -> None:
    """Run the scene loop until Esc or window close."""
    pygame.display.init()
    if "--silent" not in sys.argv:
        music_dungeon_playback.start()
    # SCALED: GPU upscales the 320x180 canvas (nearest-neighbour); vsync stops tearing on the Pi
    flags = pygame.SCALED | (0 if windowed else pygame.FULLSCREEN)
    native = pygame.display.set_mode(NATIVE_SIZE, flags, vsync=1)
    pygame.display.set_caption("lofi claude")
    pygame.mouse.set_visible(windowed)
    clock = pygame.time.Clock()
    start_ms = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
        t = (pygame.time.get_ticks() - start_ms) / 1000.0
        draw_scene(native, t)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run(windowed="--windowed" in sys.argv)  # flags: --windowed, --silent, --cave
