# Mushroom Dungeon & Chill — project memory

Pixel-art ambient scene ("lofi") running fullscreen on a Raspberry Pi 3, developed on this Mac.
Public repo: https://github.com/fremontcw/Mushroom-Dungeon-and-Chill (renamed from `sewer-lofi`; local folder
`~/work/Mushroom-Dungeon-and-Chill`, was `rasp_pi_test`). Single squashed initial commit so no Pi host/user ever hit history.

## Repo hygiene
- Nothing identifying goes in tracked files: host/user only in git-ignored `deploy.env`; `lofi-claude.service` has a `PI_USER` placeholder that `deploy.sh` substitutes. A `git grep` for the LAN IP should stay empty (the GitHub handle in the repo URL is public anyway).
- GitHub repo names can't contain `&`; the display name "Mushroom Dungeon & Chill" lives in README/CLAUDE.md, slug is `Mushroom-Dungeon-and-Chill`. Keep `&` out of folder names too.
- Renaming the folder breaks `.venv` (absolute shebangs) — `rm -rf .venv && python3 -m venv .venv && .venv/bin/pip install pygame-ce pillow`.
- README leads with `docs/demo.gif` (10 s, 15 fps, 640x360, ~700 KB) rendered headless via Pillow; regenerate it after visible scene changes. Topics: raspberry-pi, pygame, pixel-art, lofi, ambient-display, screensaver, python.
- Licensing: code MIT (`LICENSE`), assets excluded; `CREDITS.md` names LimeZu (CC BY 4.0, notes crops are unmodified), TAD (CC0), OGA ambience (CC0, +12 dB change noted — CC BY/CC0 etiquette is to state modifications).
- **Release checklist (done 2026-08-29, repeat before announcing a new version):** (1) `git log --all -p | grep -E "192\.168\.[0-9]+\.[0-9]+|PRIVATE KEY|ssh-(ed25519|rsa) AAAA|token|password"` — only the example IP and the CLAUDE.md sentence about passwords may appear; (2) `git ls-files --error-unmatch deploy.env` must fail; (3) fresh `git clone` into the scratchpad, follow README verbatim: venv + pygame-ce, `test_scene_renders.py` → ok, run `main.py --windowed` (with and without `--silent`) and `play_music_on_mac.py` for a few seconds each, then `./deploy.sh` from the clone → Pi `active`. All passed on the first public release.
- macOS has no `timeout`; time-box a run with a Python `subprocess.run(..., timeout=4)` and treat `TimeoutExpired` as success. The "no fast renderer available" warning under `SDL_VIDEODRIVER=dummy` is harmless.
- Nothing on GitHub does quite this (lofi-style composed scene on a Pi HDMI output from asset packs); nearest are LED-matrix vignettes and aquarium sims.

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
- Rejected along the way: hand-drawn sprites, a desk/workstation with a seated refugee + clock monitor (looked wrong), drains in the wall (broke the water flow), 2x walkers (too pixelated), 4 walkers at 2x (user wanted "more, smaller" → ten at 1x).
- Walker roster is one tuple per walker in `sprite_big_walker.WALKERS` (sheet, feet-y lane, speed, phase, alpha); keep sorted by lane so front lanes draw last. `sheet10`/`sheet12` are green goblins, `sheet9` a second red, `sheet11` grey mushroom — user hasn't objected yet.
- Water is a single tile frame; motion comes only from scrolling the water strips by `t * 6 px/s` (a strip one tile wider than the screen, blitted at `-offset`). Anything static drawn ON the water (drains' splash) breaks the flow illusion — that's why drains went.
- Tile indices in the Complete tileset used now: wall (5,36)/(6,36), flowing water (5,37)/(6,37), still water (5,38)/(6,38), mossy walkway (4,40)/(5,40)/(6,40). (7,40) is nearly black — don't mix it into floors.
- `ffmpeg` on this Mac failing mid-chain once pushed a half-edited tree to the Pi; `deploy.sh` now guards with the local check first.
- Static layers are cached with `functools.cache` (ground, glow discs, scaled frames). Never allocate surfaces per frame on the Pi.
- Glow: use `BLEND_RGB_ADD` with dim colours on a non-alpha surface. `BLEND_RGBA_ADD` with alpha discs renders solid.
- `pygame.mixer` must NOT be initialised when silent (`pygame.display.init()` only) — ALSA underrun spam otherwise.
- Check: `.venv/bin/python lofi_claude/test_scene_renders.py` → `ok`. Dev preview: `.venv/bin/python lofi_claude/main.py --windowed`.
- Deploy: `./deploy.sh` — runs the local check, wipes old `.py` files on the Pi, copies, substitutes `PI_USER` and the audio flag into `lofi-claude.service`, restarts. `PI_AUDIO=1` in `deploy.env` makes the Pi play the music itself (3.5 mm jack / whatever PipeWire's default sink is); default is `--silent`. Service: DISPLAY=:0, XDG_RUNTIME_DIR=/run/user/1000, WantedBy=graphical.target.
- Don't chain edit + deploy with `&&` in one shell call — one failed step (or `grep -v` matching nothing) silently skips the rest. Use absolute paths; the shell cwd persists between calls.
- Mac `ffmpeg` has no libvorbis; use `-c:a vorbis -strict -2`. The OGA dungeon ambience is ~-30 dB RMS — needed +12 dB to be audible under the music.

## Art & audio
- Sprites: "Fungus Cave [16x16]" pack in `~/Downloads` (copied into `lofi_claude/assets/`). Characters are RPG-Maker layout: 48×128 sheets = 3 frames × 4 rows (down, left, right, up), 16×32 per frame; walk = ping-pong 0,1,2,1 at 6 fps. `Characters.png` holds 12 more (3-col groups, two bands of 128px). Tileset 128×736 = 8 cols × 46 rows of 16px; useful indices in `scene_cave_tilemap.py`. LimeZu's Fungus Cave pack, **CC BY 4.0** (confirmed on the itch page) — redistributable with credit; see CREDITS.md.
- Hand-drawn char-grid sprites (Claude bot, Omni-Man, Mario) looked derpy; real pack art was the fix. Front-on figures at a desk read their arms as legs.
- Music: CC0 from OpenGameArt in `assets/music/` — `8_bit_ice_cave_lofi.mp3` (TAD) + `dungeon_ambient_loud.ogg` (drips, +12 dB normalised). Clock/timezone code uses `America/New_York` if it ever comes back. Synth-generated loop was rejected (static/noise). Played on the Mac by `play_music_on_mac.py`; stop with `pkill -9 -f play_music_on_mac.py` (plain `pkill` left copies stacking up).

## User preferences observed
- Iterate slowly, one visible change at a time, checking the Pi screen between steps.
- Prefers seeing options visually — three artifacts published today: Fungus Cave Cast (all 23 characters animated), Fungus Cave Tiles (labelled grids), Sewer Theme Mockups (real frames with theme swapped). Mockups-in-artifact-then-deploy worked well; do it again for visual forks.
- Names the sprite by the label on the cast page ("character sheet #8"); place tiles by `(col, row)` from the tiles page.
- Says "perfect"/"cool" briefly when happy and moves on; when something's off says exactly what ("breaks the illusion", "looks like toes"). Don't over-explain; do the change and report in two lines.
- Wants mid-turn corrections applied immediately (they send messages while I'm working — check for them).
- Reset the Pi's password themselves rather than share it; never ask for it. Runs interactive commands via `! cmd` in the prompt when told exactly what to type.
