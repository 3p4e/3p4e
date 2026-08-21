# Block Shooter — Red vs Blue

A browser-based **block-world team shooter**. You drop into a voxel arena on the
**Blue** team and fight an AI-controlled **Red** team. Build blocks to make cover,
destroy blocks to open lines of fire, and out-shoot the enemy. First team to
**25 kills** wins.

Built with vanilla JavaScript + [Three.js](https://threejs.org/). No build
step. Three.js loads from a CDN via an import map, so the first page load
needs internet — see [Offline play](#offline-play) to vendor it locally.

## Play

The game uses native ES modules, so it must be served over HTTP (opening
`index.html` directly via `file://` will not work). Pick any one:

```bash
# Option A — Node (zero dependencies, works offline)
node serve.mjs            # then open http://localhost:8080/
# or:  npm start

# Option B — Python
python3 -m http.server 8080   # then open http://localhost:8080/

# Option C — anything else that serves static files
npx serve .
```

Then open the printed URL and **click to play** (this locks your mouse — press
`Esc` to release / pause).

## Controls

| Input | Action |
|-------|--------|
| **WASD** | Move |
| **Mouse** | Look |
| **Space** | Jump |
| **Shift** | Sprint |
| **Left Click** | Shoot |
| **Right Click** | Place a block (on the face you're aiming at) |
| **Middle Click** / **G** | Destroy the block you're aiming at |
| **Mouse Wheel** / **1–9** | Pick which block to place |
| **Tab** | Scoreboard |
| **Esc** | Pause / release mouse |

- Your shots hit enemies in your crosshair (hitscan) unless a block is in the way —
  so cover matters, and so does breaking theirs.
- The floor and the outer arena walls are **indestructible**; everything else can be
  mined or built over.
- Get killed and you respawn at your team's base after 3 seconds.

## How it works

Everything runs client-side in the browser. The code is small, dependency-free
ES modules under `src/`:

| File | Responsibility |
|------|----------------|
| `src/config.js` | All tuning: world size, block palette, teams, weapon/bot stats, win score |
| `src/world.js` | Voxel data, arena generation, a DDA voxel raycast (for aiming/placing), and instanced-cube rendering (only surface-exposed cubes are drawn) |
| `src/physics.js` | Axis-separated AABB-vs-voxel collision shared by the player and bots |
| `src/player.js` | Pointer-lock mouse look, WASD movement, jumping, health, respawn |
| `src/bots.js` | Per-bot AI (seek → line-of-sight check → hold sightline & fire → chase), plus their team-colored avatars |
| `src/combat.js` | Hitscan resolution (ray vs walls and ray vs entity AABBs), damage, tracers |
| `src/ui.js` | HUD: health, scores, kill feed, block picker, scoreboard, overlays |
| `src/main.js` | Renderer/scene/lights, input routing, the fixed-timestep game loop, scoring & win/restart |

Three.js r160 is pulled in through the import map in `index.html`.

## Offline play

To run with no network at all, download Three.js once and repoint the import
map at the local copy:

```bash
cd block-shooter
mkdir -p vendor
curl -L -o vendor/three.module.js \
  https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js
```

Then edit the import map in `index.html` to use `"./vendor/three.module.js"`
instead of the CDN URL. After that the game runs entirely from local files.

### Tuning

Want a different feel? Edit `src/config.js` — e.g. `RULES.scoreToWin`,
`BOT.perTeam`, `WEAPON.damage`, `WORLD.W/H/D`, or the block `PALETTE`.
No rebuild needed; just reload the page.
