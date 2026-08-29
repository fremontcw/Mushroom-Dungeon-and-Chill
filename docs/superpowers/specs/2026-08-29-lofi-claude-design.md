# Lofi Claude — pixel-art ambient scene for a Raspberry Pi 3

## Goal
A silent, looping pixel-art animation (lofi-girl homage) of a "Claude bot"
typing at a desk, displayed fullscreen on the Pi 3's HDMI output at boot.

## Target
- Raspberry Pi 3 Model B, Raspberry Pi OS Bookworm 32-bit, python3 + pygame.
- Also runs windowed on macOS for development (same code).

## Scene
Native canvas 320x180, nearest-neighbour scaled to the display. ~30 fps.
- Room at night: desk, monitor, mug, window, lamp.
- Claude bot: boxy robot, sparkle mark on chest. Loops: typing hands
  (4 frames, ~8 fps), blink every 3-6 s, occasional head tilt.
- Monitor shows scrolling fake code (static line bank, decorative).
- Rain streaks on the window; lightning flash every 20-60 s.
- Steam rising from the mug.
All art is pixel grids in code. No external assets. No audio.

## Structure
```
lofi_claude/
├── main.py               # window/fullscreen, loop, scale, Esc quits
├── scene_background.py   # room, desk, window, lamp
├── sprite_claude_bot.py  # bot frames + animation state
├── effects_rain_steam.py # rain, steam, lightning particles
├── terminal_fake_code.py # scrolling text on in-scene monitor
├── test_scene_renders.py # headless: one frame renders, bot pixels present
└── lofi-claude.service   # systemd unit, fullscreen at boot
```

## Deploy
`scp -r lofi_claude` to the Pi, `sudo apt install python3-pygame`,
install service, `systemctl enable --now lofi-claude`.

## Out of scope (add later if wanted)
Music, live Claude API text, config file, multiple scenes.
