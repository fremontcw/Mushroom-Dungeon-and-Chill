"""PlayLofiMusicOnMac

Plays the dungeon music + ambience through this Mac's speakers. Ctrl-C to stop.

Status:
    None
Issues:
    None
Todo:
    None
"""

import sys
import time

sys.path.insert(0, "lofi_claude")
import pygame  # noqa: E402

import music_dungeon_playback  # noqa: E402

music_dungeon_playback.start()
print("playing dungeon music on Mac — Ctrl-C to stop")
while True:
    time.sleep(1)
