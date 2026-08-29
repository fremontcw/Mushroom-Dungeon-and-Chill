"""DungeonMusicPlayback

Loops the CC0 "8 bit lofi - Ice Cave" track (TAD, OpenGameArt) with the CC0
"Loopable Dungeon Ambience" drips layered quietly underneath.

Status:
    None
Issues:
    None
Todo:
    None
"""

from pathlib import Path

import pygame

MUSIC_DIR = Path(__file__).parent / "assets" / "music"
MUSIC_FILE = MUSIC_DIR / "8_bit_ice_cave_lofi.mp3"
AMBIENCE_FILE = MUSIC_DIR / "dungeon_ambient_loud.ogg"
MUSIC_VOLUME = 0.55
AMBIENCE_VOLUME = 1.0


def start() -> None:
    """Initialise the mixer and loop music + ambience forever."""
    pygame.mixer.init(frequency=44100, buffer=2048)
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(loops=-1)
    ambience = pygame.mixer.Sound(AMBIENCE_FILE)
    ambience.set_volume(AMBIENCE_VOLUME)
    ambience.play(loops=-1)
