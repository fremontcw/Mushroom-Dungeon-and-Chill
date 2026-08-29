# Lofi Claude Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fullscreen looping pixel-art scene of a Claude bot typing at a desk on a Pi 3.

**Architecture:** One pygame process draws a 320x180 `pygame.Surface` each frame from four
pure-ish drawing modules (background, bot, effects, terminal), then scales it to the
window. Every module exposes `draw(surface, t_seconds)`; `main.py` owns the loop.

**Tech Stack:** Python 3.11+ (Pi) / 3.14 (Mac), pygame-ce (Mac) or python3-pygame (Pi). No assets.

**Spec:** `docs/superpowers/specs/2026-08-29-lofi-claude-design.md`

## Global Constraints
- Native canvas `320x180`, nearest-neighbour scale (`pygame.transform.scale`, never `smoothscale`).
- All art is code (pixel grids / rect draws). No image files. No audio.
- Every file carries the CLAUDE.md file header (`@status/@issues/@todo`, Python docstring form).
- No git repo — skip commit steps; run checks instead.
- Run on Mac: `.venv/bin/python lofi_claude/main.py --windowed`.

---

### Task 1: main loop + scaling (`lofi_claude/main.py`)
**Produces:** `NATIVE_SIZE = (320, 180)`, `run(windowed: bool)`; each scene module must
expose `draw(surface: pygame.Surface, t: float) -> None`.
- [ ] Write `main.py`: parse `--windowed`; create display (fullscreen unless windowed, windowed = 960x540);
      native `Surface(NATIVE_SIZE)`; loop at 30 fps; `t = elapsed seconds`; call each module's `draw`;
      scale native to window; Esc/QUIT exits. Hide mouse when fullscreen.
- [ ] Temporarily fill native with a solid colour; run `--windowed`; confirm a window appears. Delete the fill once Task 2 lands.

### Task 2: background (`lofi_claude/scene_background.py`)
- [ ] `draw(surface, t)`: night sky rect, window frame with lit glow, wall, desk slab, monitor bezel,
      mug, lamp with warm halo that flickers (`sin(t*7)` amplitude ±1 brightness step).
- [ ] Export constants later tasks anchor to: `MONITOR_SCREEN = pygame.Rect(...)`, `MUG_TOP = (x, y)`,
      `WINDOW_RECT = pygame.Rect(...)`, `BOT_ANCHOR = (x, y)`.
- [ ] Run windowed; eyeball layout.

### Task 3: Claude bot (`lofi_claude/sprite_claude_bot.py`)
- [ ] Define bot as pixel-grid string lists (chars → palette) for: body, head with eyes open, head with
      eyes closed, 4 hand/arm typing frames.
- [ ] `draw(surface, t)`: blit body at `BOT_ANCHOR`; typing frame = `int(t*8) % 4`; blink when
      `(t % blink_period) < 0.15` with blink_period pseudo-random from `int(t // 4)`; head tilt (±1 px x-shift)
      when `int(t // 9) % 3 == 0`.
- [ ] Helper `blit_pixel_grid(surface, grid, palette, pos)` lives here; Task 4/5 may import it.

### Task 4: effects (`lofi_claude/effects_rain_steam.py`)
- [ ] Rain: `N_DROPS=40` deterministic drops seeded with `random.Random(1)`; each has x, speed,
      y = `(seed_y + t*speed) % WINDOW_RECT.height`; draw 1x3 streaks clipped to `WINDOW_RECT`.
- [ ] Steam: 3 wisps from `MUG_TOP`, y rises with `t`, x wobbles with `sin`, fades over 2 s, loops.
- [ ] Lightning: flash when `hash(int(t//30)) % 3 == 0 and (t % 30) < 0.12` → blend white rect over window.
- [ ] Run windowed; confirm rain stays inside window and steam loops.

### Task 5: fake terminal (`lofi_claude/terminal_fake_code.py`)
- [ ] `CODE_LINES`: ~25 short Python-ish lines. Draw with `pygame.font.SysFont(None, 8)`? No — pixel
      fonts are unreliable; draw lines as coloured 1px-tall rects of varying width ("blurred code" look)
      inside `MONITOR_SCREEN`, scrolling 1 line/0.4 s, newest at bottom, cursor blinks at 2 Hz.
- [ ] Run windowed; monitor scrolls.

### Task 6: check + deploy
- [ ] `lofi_claude/test_scene_renders.py`: `SDL_VIDEODRIVER=dummy`; build native surface, call all four
      `draw(surface, 1.5)`; assert pixel at `BOT_ANCHOR` offset ≠ background colour and no exception.
      Run: `.venv/bin/python lofi_claude/test_scene_renders.py` → prints `ok`.
- [ ] `lofi_claude/lofi-claude.service`: `User=PI_USER` (substituted by deploy.sh), `Environment=DISPLAY=:0`,
      `ExecStart=/usr/bin/python3 /home/PI_USER/lofi_claude/main.py`, `Restart=always`, `WantedBy=graphical.target`.
- [ ] Deploy: `scp -r lofi_claude $PI_USER@$PI_HOST:~/`; on Pi `sudo apt install -y python3-pygame`;
      `sudo cp ~/lofi_claude/lofi-claude.service /etc/systemd/system/ && sudo systemctl enable --now lofi-claude`;
      check `systemctl status lofi-claude`.
