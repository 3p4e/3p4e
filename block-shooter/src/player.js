import * as THREE from 'three';
import { PLAYER, TEAM, WORLD } from './config.js';
import { moveEntity } from './physics.js';

export class Player {
  constructor(team = TEAM.BLUE) {
    this.team = team;
    this.radius = PLAYER.radius;
    this.height = PLAYER.height;
    this.eye = PLAYER.eye;
    this.pos = { x: 0, y: 0, z: 0 };
    this.vel = { x: 0, y: 0, z: 0 };
    this.yaw = 0;
    this.pitch = 0;
    this.onGround = false;
    this.health = PLAYER.maxHealth;
    this.alive = true;
    this.respawnTimer = 0;
    this.kills = 0;
    this.deaths = 0;
    this.isPlayer = true;

    this.keys = Object.create(null);
    this._forward = new THREE.Vector3();

    window.addEventListener('keydown', (e) => this._onKey(e, true));
    window.addEventListener('keyup', (e) => this._onKey(e, false));
    // Don't let the browser scroll / act on gameplay keys while playing.
    window.addEventListener('keydown', (e) => {
      if ([' ', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) e.preventDefault();
    });
  }

  _onKey(e, down) {
    this.keys[e.code] = down;
  }

  onMouseMove(dx, dy) {
    const sens = 0.0022;
    this.yaw -= dx * sens;
    this.pitch -= dy * sens;
    const lim = Math.PI / 2 - 0.02;
    this.pitch = Math.max(-lim, Math.min(lim, this.pitch));
  }

  getForward(out = this._forward) {
    const cp = Math.cos(this.pitch);
    out.set(-Math.sin(this.yaw) * cp, Math.sin(this.pitch), -Math.cos(this.yaw) * cp);
    return out;
  }

  eyePosition(out = new THREE.Vector3()) {
    return out.set(this.pos.x, this.pos.y + PLAYER.eye, this.pos.z);
  }

  spawn(zStart) {
    // Player is BLUE by default; spawn on the team pad with a little jitter.
    const cx = WORLD.W / 2 + (Math.random() * 4 - 2);
    this.pos.x = cx;
    this.pos.y = 2.0;
    this.pos.z = zStart + 2 + (Math.random() * 2 - 1);
    this.vel.x = this.vel.y = this.vel.z = 0;
    this.yaw = Math.PI; // face down-field toward the enemy (blue base is at low Z)
    this.pitch = 0;
    this.health = PLAYER.maxHealth;
    this.alive = true;
  }

  damage(amount, attacker) {
    if (!this.alive) return;
    this.health -= amount;
    if (this.health <= 0) {
      this.health = 0;
      this.alive = false;
      this.deaths++;
      this.respawnTimer = 0;
      this._lastAttacker = attacker || null;
    }
  }

  update(dt, world) {
    if (!this.alive) return;

    const sprint = this.keys['ShiftLeft'] || this.keys['ShiftRight'];
    const speed = sprint ? PLAYER.sprintSpeed : PLAYER.moveSpeed;

    const fx = -Math.sin(this.yaw), fz = -Math.cos(this.yaw); // forward (horizontal)
    const rx = Math.cos(this.yaw), rz = -Math.sin(this.yaw); // right

    let mx = 0, mz = 0;
    if (this.keys['KeyW']) { mx += fx; mz += fz; }
    if (this.keys['KeyS']) { mx -= fx; mz -= fz; }
    if (this.keys['KeyD']) { mx += rx; mz += rz; }
    if (this.keys['KeyA']) { mx -= rx; mz -= rz; }
    const len = Math.hypot(mx, mz);
    if (len > 0) { mx = (mx / len) * speed; mz = (mz / len) * speed; }
    this.vel.x = mx;
    this.vel.z = mz;

    if (this.keys['Space'] && this.onGround) {
      this.vel.y = PLAYER.jumpSpeed;
      this.onGround = false;
    }
    this.vel.y -= PLAYER.gravity * dt;

    moveEntity(world, this, dt);
  }

  updateCamera(camera) {
    camera.position.set(this.pos.x, this.pos.y + PLAYER.eye, this.pos.z);
    const dir = this.getForward();
    camera.lookAt(
      camera.position.x + dir.x,
      camera.position.y + dir.y,
      camera.position.z + dir.z,
    );
  }
}
