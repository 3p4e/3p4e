import * as THREE from 'three';
import { BOT, TEAM, TEAM_INFO, WORLD, RULES } from './config.js';
import { moveEntity } from './physics.js';

const RED_SPAWN_Z = WORLD.D - 7;
const BLUE_SPAWN_Z = 6;
const SPAWN_CX = WORLD.W / 2;

function spawnZFor(team) {
  return team === TEAM.RED ? RED_SPAWN_Z : BLUE_SPAWN_Z;
}

let BOT_ID = 0;

export class Bot {
  constructor(team) {
    this.id = BOT_ID++;
    this.team = team;
    this.isPlayer = false;
    this.radius = BOT.radius;
    this.height = BOT.height;
    this.eye = BOT.eye;
    this.pos = { x: 0, y: 0, z: 0 };
    this.vel = { x: 0, y: 0, z: 0 };
    this.yaw = 0;
    this.onGround = false;
    this.health = BOT.maxHealth;
    this.alive = true;
    this.respawnTimer = 0;
    this.shootCd = Math.random() * BOT.fireInterval;
    this.wanderTimer = 0;
    this.wander = { x: SPAWN_CX, z: WORLD.D / 2 };
    this.strafeDir = Math.random() < 0.5 ? 1 : -1;
    this.strafeTimer = 0;
    this.kills = 0;
    this.deaths = 0;

    this.mesh = this._buildMesh();
  }

  _buildMesh() {
    const g = new THREE.Group();
    const teamColor = TEAM_INFO[this.team].color;
    const bodyMat = new THREE.MeshLambertMaterial({ color: teamColor });
    const darkMat = new THREE.MeshLambertMaterial({ color: 0x22252b });

    const body = new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.0, 0.4), bodyMat);
    body.position.y = 0.65;
    g.add(body);

    const head = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.45, 0.45), darkMat);
    head.position.y = 1.38;
    g.add(head);

    // A little gun so you can read which way they're facing.
    const gun = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 0.55), darkMat);
    gun.position.set(0.22, 1.0, -0.3);
    g.add(gun);

    g.matrixAutoUpdate = true;
    return g;
  }

  spawn() {
    this.pos.x = SPAWN_CX + (Math.random() * 8 - 4);
    this.pos.y = 2.0;
    this.pos.z = spawnZFor(this.team) + (Math.random() * 3 - 1.5);
    this.vel.x = this.vel.y = this.vel.z = 0;
    this.health = BOT.maxHealth;
    this.alive = true;
    this.shootCd = Math.random() * BOT.fireInterval;
  }

  damage(amount, attacker) {
    if (!this.alive) return;
    this.health -= amount;
    if (this.health <= 0) {
      this.health = 0;
      this.alive = false;
      this.deaths++;
      this.respawnTimer = 0;
    }
  }

  _eyeY() {
    return this.pos.y + this.eye;
  }

  _findTarget(combatants) {
    let best = null, bestD = BOT.sightRange * BOT.sightRange;
    for (const c of combatants) {
      if (c === this || !c.alive || c.team === this.team) continue;
      const dx = c.pos.x - this.pos.x;
      const dz = c.pos.z - this.pos.z;
      const d2 = dx * dx + dz * dz;
      if (d2 < bestD) { bestD = d2; best = c; }
    }
    return best;
  }

  _hasLOS(world, target) {
    const ox = this.pos.x, oy = this._eyeY(), oz = this.pos.z;
    const tx = target.pos.x, ty = target.pos.y + target.eye, tz = target.pos.z;
    let dx = tx - ox, dy = ty - oy, dz = tz - oz;
    const dist = Math.hypot(dx, dy, dz);
    if (dist < 1e-3) return true;
    dx /= dist; dy /= dist; dz /= dist;
    const hit = world.raycast({ x: ox, y: oy, z: oz }, { x: dx, y: dy, z: dz }, dist);
    return !(hit.hit && hit.dist < dist - 0.6);
  }

  update(dt, world, combatants, combat) {
    if (!this.alive) {
      this.respawnTimer += dt;
      if (this.respawnTimer >= RULES.respawnTime) this.spawn();
      this._syncMesh();
      return;
    }

    // The weapon cools down every tick so a bot can fire the instant it gets
    // a clean line, instead of only ticking while already aiming.
    this.shootCd -= dt;
    this.strafeTimer -= dt;
    if (this.strafeTimer <= 0) {
      this.strafeDir = Math.random() < 0.5 ? 1 : -1;
      this.strafeTimer = 0.8 + Math.random() * 1.2;
    }

    const target = this._findTarget(combatants);
    let desiredX = 0, desiredZ = 0, moving = false, speedScale = 1;

    if (target) {
      const dx = target.pos.x - this.pos.x;
      const dz = target.pos.z - this.pos.z;
      const dist = Math.hypot(dx, dz) || 1e-3;
      const ndx = dx / dist, ndz = dz / dist;
      this.yaw = Math.atan2(-ndx, -ndz);

      const los = this._hasLOS(world, target);
      if (los && dist <= BOT.range) {
        // Clean shot: fire when ready, then mostly hold the sightline so the
        // shot actually lands. Only ease in/out and strafe gently.
        if (this.shootCd <= 0) {
          this._shoot(target, combat);
          this.shootCd = BOT.fireInterval * (0.85 + Math.random() * 0.4);
        }
        if (dist < 5) {
          desiredX = -ndx; desiredZ = -ndz; moving = true; speedScale = 0.8; // back off
        } else if (dist > 26) {
          desiredX = ndx; desiredZ = ndz; moving = true; speedScale = 0.9; // close in
        } else {
          // hold position with a slow perpendicular strafe (keeps LOS)
          desiredX = -ndz * this.strafeDir; desiredZ = ndx * this.strafeDir;
          moving = true; speedScale = 0.35;
        }
      } else {
        // No clean shot: advance toward the target to regain one.
        desiredX = ndx; desiredZ = ndz; moving = true;
      }
    } else {
      // No enemy in sight: wander around the arena.
      this.wanderTimer -= dt;
      if (this.wanderTimer <= 0) {
        this.wander.x = 8 + Math.random() * (WORLD.W - 16);
        this.wander.z = 10 + Math.random() * (WORLD.D - 20);
        this.wanderTimer = 2 + Math.random() * 3;
      }
      const dx = this.wander.x - this.pos.x;
      const dz = this.wander.z - this.pos.z;
      const dist = Math.hypot(dx, dz) || 1e-3;
      desiredX = dx / dist; desiredZ = dz / dist; moving = true;
      this.yaw = Math.atan2(-desiredX, -desiredZ);
    }

    if (moving) {
      const l = Math.hypot(desiredX, desiredZ) || 1;
      this.vel.x = (desiredX / l) * BOT.moveSpeed * speedScale;
      this.vel.z = (desiredZ / l) * BOT.moveSpeed * speedScale;
    } else {
      this.vel.x = 0; this.vel.z = 0;
    }

    // Jump over a one-block obstacle directly ahead.
    if (this.onGround && moving) {
      const fx = -Math.sin(this.yaw), fz = -Math.cos(this.yaw);
      const ahead = { x: this.pos.x + fx * 0.6, z: this.pos.z + fz * 0.6 };
      const feetY = Math.floor(this.pos.y + 0.1);
      const blockedAhead = world.isSolid(Math.floor(ahead.x), feetY, Math.floor(ahead.z));
      const clearAbove = !world.isSolid(Math.floor(ahead.x), feetY + 1, Math.floor(ahead.z));
      if (blockedAhead && clearAbove) this.vel.y = BOT.jumpSpeed;
    }

    this.vel.y -= BOT.gravity * dt;
    moveEntity(world, this, dt);

    if (this.pos.y < RULES.killPlaneY) this.damage(9999, null);

    this._syncMesh();
  }

  _shoot(target, combat) {
    const ox = this.pos.x, oy = this._eyeY(), oz = this.pos.z;
    const tx = target.pos.x, ty = target.pos.y + target.eye * 0.9, tz = target.pos.z;
    let dx = tx - ox, dy = ty - oy, dz = tz - oz;
    const l = Math.hypot(dx, dy, dz) || 1;
    const origin = new THREE.Vector3(ox, oy, oz);
    const dir = new THREE.Vector3(dx / l, dy / l, dz / l);
    combat.fire(this, origin, dir, { damage: BOT.damage, range: BOT.range, spread: BOT.spread });
  }

  _syncMesh() {
    this.mesh.visible = this.alive;
    this.mesh.position.set(this.pos.x, this.pos.y, this.pos.z);
    this.mesh.rotation.y = this.yaw;
  }
}

export class BotManager {
  constructor(scene, world, combat, player) {
    this.scene = scene;
    this.world = world;
    this.combat = combat;
    this.player = player;
    this.bots = [];

    for (let i = 0; i < BOT.perTeam; i++) this._add(TEAM.RED);
    for (let i = 0; i < BOT.perTeam - 1; i++) this._add(TEAM.BLUE); // player fills the last blue slot

    this.combatants = [player, ...this.bots];
    combat.setCombatants(this.combatants);
  }

  _add(team) {
    const bot = new Bot(team);
    bot.spawn();
    this.scene.add(bot.mesh);
    this.bots.push(bot);
  }

  update(dt) {
    for (const bot of this.bots) bot.update(dt, this.world, this.combatants, this.combat);
  }
}

export { RED_SPAWN_Z, BLUE_SPAWN_Z, SPAWN_CX };
