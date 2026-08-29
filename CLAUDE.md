# rasp_pi_test — project memory

Pixel-art ambient scene ("lofi") running fullscreen on a Raspberry Pi 3, developed on this Mac.

## The Pi
- Pi 3 Model B Rev 1.2, Raspberry Pi OS Bookworm 32-bit, Wayland desktop (labwc), Python 3.11, pygame 2.1.2, numpy 1.24.
- Host and user live in git-ignored `deploy.env` (`PI_HOST`, `PI_USER`). Passwordless SSH via `~/.ssh/id_ed25519` (already in the Pi's authorized_keys).
- **SSH must be `systemctl enable`d, not just started** — we lost it once after a reboot.
- Under-voltage is real (`vcgencmd get_throttled` → `0x50005`): the PSU/cable is weak, the Pi throttles. `avoid_warnings=1` in `/boot/firmware/config.txt` hides the icon only. Proper 5.1V/2.5A micro-USB supply on order.
- Audio: only the 3.5mm jack is exposed to PipeWire; no HDMI audio sink shows up. Music is played from the Mac instead.
- Can't screenshot the Pi from SSH (Wayland, no X auth). The scene is deterministic in `t`, so a local headless render is pixel-identical.

## The app (`lofi_claude/`)
- pygame, native 320×180 canvas, `pygame.SCALED | FULLSCREEN` with `vsync=1` → GPU upscale, ~16% CPU. Software `transform.scale` per frame was 50–100% CPU and tore.
- Every layer is `draw(surface, t_seconds)`; `main.py` picks layers by flag. **Default (the one the user likes): `scene_sewer_canal` + `sprite_big_walker.draw_walkers`** — brick wall off the top edge, 3-row canal of sideways-scrolling water, mossy walkway, ten 1x fungus folk on lanes (two translucent drifters over the water). `--cave` = older tilemap cave with torches/campfire. `--windowed` for Mac dev, `--silent` mutes music (the Pi service runs `--silent`).
- Rejected along the way: hand-drawn sprites, a desk/workstation with a seated refugee + clock monitor (looked wrong), drains in the wall (broke the water flow), 2x walkers (too pixelated).
- Static layers are cached with `functools.cache` (ground, glow discs, scaled frames). Never allocate surfaces per frame on the Pi.
- Glow: use `BLEND_RGB_ADD` with dim colours on a non-alpha surface. `BLEND_RGBA_ADD` with alpha discs renders solid.
- `pygame.mixer` must NOT be initialised when silent (`pygame.display.init()` only) — ALSA underrun spam otherwise.
- Check: `.venv/bin/python lofi_claude/test_scene_renders.py` → `ok`. Dev preview: `.venv/bin/python lofi_claude/main.py --windowed`.
- Deploy: `./deploy.sh` — runs the local check, wipes old `.py` files on the Pi, copies, substitutes `PI_USER` into `lofi-claude.service`, restarts. Service: DISPLAY=:0, XDG_RUNTIME_DIR=/run/user/1000, WantedBy=graphical.target.
- Don't chain edit + deploy with `&&` in one shell call — one failed step (or `grep -v` matching nothing) silently skips the rest. Use absolute paths; the shell cwd persists between calls.
- Mac `ffmpeg` has no libvorbis; use `-c:a vorbis -strict -2`. The OGA dungeon ambience is ~-30 dB RMS — needed +12 dB to be audible under the music.

## Art & audio
- Sprites: "Fungus Cave [16x16]" pack in `~/Downloads` (copied into `lofi_claude/assets/`). Characters are RPG-Maker layout: 48×128 sheets = 3 frames × 4 rows (down, left, right, up), 16×32 per frame; walk = ping-pong 0,1,2,1 at 6 fps. `Characters.png` holds 12 more (3-col groups, two bands of 128px). Tileset 128×736 = 8 cols × 46 rows of 16px; useful indices in `scene_cave_tilemap.py`. LimeZu's Fungus Cave pack, **CC BY 4.0** (confirmed on the itch page) — redistributable with credit; see CREDITS.md.
- Hand-drawn char-grid sprites (Claude bot, Omni-Man, Mario) looked derpy; real pack art was the fix. Front-on figures at a desk read their arms as legs.
- Music: CC0 from OpenGameArt in `assets/music/` — `8_bit_ice_cave_lofi.mp3` (TAD) + `dungeon_ambient_loud.ogg` (drips, +12 dB normalised). Clock/timezone code uses `America/New_York` if it ever comes back. Synth-generated loop was rejected (static/noise). Played on the Mac by `play_music_on_mac.py`; stop with `pkill -9 -f play_music_on_mac.py` (plain `pkill` left copies stacking up).

## User preferences observed
- Iterate slowly, one visible change at a time, checking the Pi screen between steps.
- Prefers seeing options visually (published a character contact-sheet artifact).
