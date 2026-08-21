import * as THREE from 'three';
import {
  WORLD, BLOCK, BLOCK_COLORS, PALETTE, PALETTE_NAMES,
  TEAM, TEAM_INFO, PLAYER, WEAPON, RULES,
} from './config.js';
import { World } from './world.js';
import { Player } from './player.js';
import { Combat } from './combat.js';
import { BotManager, BLUE_SPAWN_Z } from './bots.js';
import { UI } from './ui.js';

const hexColor = (id) => '#' + BLOCK_COLORS[id].toString(16).padStart(6, '0');

// ---- Renderer / scene --------------------------------------------------
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x87b7e0);
document.getElementById('app').appendChild(renderer.domElement);
const canvas = renderer.domElement;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87b7e0);
scene.fog = new THREE.Fog(0x87b7e0, 40, 120);

const camera = new THREE.PerspectiveCamera(78, window.innerWidth / window.innerHeight, 0.05, 500);

const hemi = new THREE.HemisphereLight(0xffffff, 0x556070, 0.95);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xffffff, 0.75);
sun.position.set(0.4, 1, 0.25).multiplyScalar(50);
scene.add(sun);

// ---- Game objects ------------------------------------------------------
const world = new World();
scene.add(world.buildMeshes());

const player = new Player(TEAM.BLUE);
player.spawn(BLUE_SPAWN_Z);

const combat = new Combat(scene, world);
const bots = new BotManager(scene, world, combat, player);
const combatants = bots.combatants;

// Targeted-block highlight.
const highlight = new THREE.LineSegments(
  new THREE.EdgesGeometry(new THREE.BoxGeometry(1.001, 1.001, 1.001)),
  new THREE.LineBasicMaterial({ color: 0x101418, transparent: true, opacity: 0.6 }),
);
highlight.visible = false;
scene.add(highlight);

const ui = new UI();
const scores = { [TEAM.RED]: 0, [TEAM.BLUE]: 0 };
let paletteIndex = 0;
let state = 'start'; // 'start' | 'playing' | 'over'

function currentBlock() { return PALETTE[paletteIndex]; }
function refreshBlockUI() {
  const id = currentBlock();
  ui.setBlock(PALETTE_NAMES[id], hexColor(id));
}
refreshBlockUI();
ui.setScores(0, 0);
ui.setHealth(player.health, PLAYER.maxHealth);
ui.showStart(true); // show the "click to play" screen on load
const vsEl = document.querySelector('#scorebar .vs');
if (vsEl) vsEl.textContent = 'first to ' + RULES.scoreToWin;

// ---- Scoring / kill feed ----------------------------------------------
function nameOf(c) {
  if (c.isPlayer) return 'You';
  return (c.team === TEAM.RED ? 'Red' : 'Blue') + ' Bot';
}
combat.onKill = (killer, victim) => {
  scores[killer.team]++;
  killer.kills = (killer.kills || 0) + 1;
  ui.setScores(scores[TEAM.RED], scores[TEAM.BLUE]);
  ui.addKill(nameOf(killer), nameOf(victim), killer.team);
  if (scores[killer.team] >= RULES.scoreToWin) endGame(killer.team);
};

function endGame(team) {
  state = 'over';
  ui.showWin(team);
  if (document.pointerLockElement) document.exitPointerLock();
}

function restart() {
  scores[TEAM.RED] = 0; scores[TEAM.BLUE] = 0;
  ui.setScores(0, 0);
  for (const b of bots.bots) { b.kills = 0; b.deaths = 0; b.spawn(); }
  player.kills = 0; player.deaths = 0; player.respawnTimer = 0;
  player.spawn(BLUE_SPAWN_Z);
  ui.setHealth(player.health, PLAYER.maxHealth);
  ui.hideWin();
  state = 'playing';
  canvas.requestPointerLock();
}

// ---- Input -------------------------------------------------------------
let leftDown = false, rightDown = false, midDown = false;
let fireCd = 0, placeCd = 0, destroyCd = 0;
let showSB = false;

canvas.addEventListener('click', () => {
  if (state === 'start' || (state === 'playing' && !document.pointerLockElement)) {
    canvas.requestPointerLock();
  }
});
document.getElementById('start').addEventListener('click', () => canvas.requestPointerLock());
document.getElementById('win').addEventListener('click', () => restart());

document.addEventListener('pointerlockchange', () => {
  const locked = document.pointerLockElement === canvas;
  if (locked) {
    if (state === 'start') state = 'playing';
    ui.showStart(false);
  } else if (state === 'playing') {
    ui.showStart(true); // paused
  }
});

document.addEventListener('mousemove', (e) => {
  if (document.pointerLockElement === canvas) player.onMouseMove(e.movementX, e.movementY);
});

canvas.addEventListener('mousedown', (e) => {
  if (document.pointerLockElement !== canvas || state !== 'playing') return;
  if (e.button === 0) { leftDown = true; }
  else if (e.button === 2) { rightDown = true; placeCd = 0; }
  else if (e.button === 1) { midDown = true; destroyCd = 0; }
});
window.addEventListener('mouseup', (e) => {
  if (e.button === 0) leftDown = false;
  else if (e.button === 2) rightDown = false;
  else if (e.button === 1) midDown = false;
});
window.addEventListener('contextmenu', (e) => e.preventDefault());

window.addEventListener('wheel', (e) => {
  if (state !== 'playing') return;
  paletteIndex = (paletteIndex + (e.deltaY > 0 ? 1 : -1) + PALETTE.length) % PALETTE.length;
  refreshBlockUI();
});

window.addEventListener('keydown', (e) => {
  if (e.code === 'Tab') { e.preventDefault(); showSB = true; }
  if (e.code.startsWith('Digit')) {
    const n = parseInt(e.code.slice(5), 10) - 1;
    if (n >= 0 && n < PALETTE.length) { paletteIndex = n; refreshBlockUI(); }
  }
  if (e.code === 'KeyG') { destroyBlock(); }
});
window.addEventListener('keyup', (e) => {
  if (e.code === 'Tab') showSB = false;
});

// ---- Actions -----------------------------------------------------------
const _o = new THREE.Vector3();
const _d = new THREE.Vector3();

function firePlayer() {
  player.eyePosition(_o);
  player.getForward(_d);
  combat.fire(player, _o, _d, { damage: WEAPON.damage, range: WEAPON.range, spread: WEAPON.spread });
}

function cellBlockedByEntity(x, y, z) {
  for (const c of combatants) {
    if (!c.alive) continue;
    const minX = c.pos.x - c.radius, maxX = c.pos.x + c.radius;
    const minZ = c.pos.z - c.radius, maxZ = c.pos.z + c.radius;
    const minY = c.pos.y, maxY = c.pos.y + c.height;
    if (maxX > x && minX < x + 1 && maxZ > z && minZ < z + 1 && maxY > y && minY < y + 1) return true;
  }
  return false;
}

function placeBlock() {
  player.eyePosition(_o);
  player.getForward(_d);
  const hit = world.raycast(_o, _d, PLAYER.reach);
  if (!hit.hit) return;
  const nx = hit.x + hit.nx, ny = hit.y + hit.ny, nz = hit.z + hit.nz;
  if (!world.inBounds(nx, ny, nz) || world.isSolid(nx, ny, nz)) return;
  if (cellBlockedByEntity(nx, ny, nz)) return;
  world.setBlock(nx, ny, nz, currentBlock());
}

function destroyBlock() {
  if (state !== 'playing' || document.pointerLockElement !== canvas) return;
  player.eyePosition(_o);
  player.getForward(_d);
  const hit = world.raycast(_o, _d, PLAYER.reach);
  if (!hit.hit) return;
  if (world.isIndestructible(hit.x, hit.y, hit.z)) return;
  world.setBlock(hit.x, hit.y, hit.z, BLOCK.AIR);
}

function updateHighlight() {
  if (state !== 'playing' || !player.alive || document.pointerLockElement !== canvas) {
    highlight.visible = false;
    return;
  }
  player.eyePosition(_o);
  player.getForward(_d);
  const hit = world.raycast(_o, _d, PLAYER.reach);
  if (hit.hit) {
    highlight.visible = true;
    highlight.position.set(hit.x + 0.5, hit.y + 0.5, hit.z + 0.5);
  } else {
    highlight.visible = false;
  }
}

// ---- Simulation --------------------------------------------------------
function stepSim(dt) {
  // Player respawn.
  if (!player.alive) {
    player.respawnTimer += dt;
    ui.showRespawn(RULES.respawnTime - player.respawnTimer);
    if (player.respawnTimer >= RULES.respawnTime) {
      player.spawn(BLUE_SPAWN_Z);
      ui.hideRespawn();
    }
  } else {
    player.update(dt, world);
    if (player.pos.y < RULES.killPlaneY) player.damage(9999, null);

    // Weapons / building.
    fireCd -= dt; placeCd -= dt; destroyCd -= dt;
    if (leftDown && fireCd <= 0) { firePlayer(); fireCd = WEAPON.fireInterval; }
    if (rightDown && placeCd <= 0) { placeBlock(); placeCd = 0.13; }
    if (midDown && destroyCd <= 0) { destroyBlock(); destroyCd = 0.13; }
  }

  bots.update(dt);
  combat.update(dt);
  if (world.dirty) world.rebuild();
}

// ---- Loop --------------------------------------------------------------
let last = performance.now();
let acc = 0;
const STEP = 1 / 60;

function loop(now) {
  requestAnimationFrame(loop);
  let dt = (now - last) / 1000;
  last = now;
  if (dt > 0.1) dt = 0.1;

  if (state === 'playing' && document.pointerLockElement === canvas) {
    acc += dt;
    while (acc >= STEP) { stepSim(STEP); acc -= STEP; }
  } else {
    acc = 0;
    combat.update(dt); // keep tracers fading even while paused
  }

  player.updateCamera(camera);
  updateHighlight();
  ui.setHealth(player.health, PLAYER.maxHealth);
  ui.setCrosshairMode(player.alive);
  ui.showScoreboard(showSB, combatants, scores);

  renderer.render(scene, camera);
}
requestAnimationFrame(loop);

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Expose a few handles for debugging in the console.
window.__game = { world, player, bots, combat, scores };
