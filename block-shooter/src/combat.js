import * as THREE from 'three';

// Ray vs AABB (slab method). Returns entry distance along the ray, or null.
function rayAABB(o, d, min, max) {
  let tmin = -Infinity, tmax = Infinity;
  for (let a = 0; a < 3; a++) {
    const oa = o[a], da = d[a], mn = min[a], mx = max[a];
    if (Math.abs(da) < 1e-8) {
      if (oa < mn || oa > mx) return null;
    } else {
      let t1 = (mn - oa) / da;
      let t2 = (mx - oa) / da;
      if (t1 > t2) { const tmp = t1; t1 = t2; t2 = tmp; }
      if (t1 > tmin) tmin = t1;
      if (t2 < tmax) tmax = t2;
      if (tmin > tmax) return null;
    }
  }
  if (tmax < 0) return null;
  return tmin > 0 ? tmin : 0;
}

export class Combat {
  constructor(scene, world) {
    this.scene = scene;
    this.world = world;
    this.combatants = [];
    this.onKill = null; // (shooter, victim) => void
    this.tracers = [];

    this._tracerGeo = new THREE.BufferGeometry();
    this._tracerGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3));
  }

  setCombatants(list) {
    this.combatants = list;
  }

  // Fire a hitscan shot from `shooter`. origin/dir are THREE.Vector3.
  fire(shooter, origin, dir, { damage, range, spread = 0 }) {
    // Apply random cone spread.
    let dx = dir.x, dy = dir.y, dz = dir.z;
    if (spread > 0) {
      dx += (Math.random() * 2 - 1) * spread;
      dy += (Math.random() * 2 - 1) * spread;
      dz += (Math.random() * 2 - 1) * spread;
      const l = Math.hypot(dx, dy, dz);
      dx /= l; dy /= l; dz /= l;
    }

    // Distance to the first wall in the shot's path.
    const wall = this.world.raycast({ x: origin.x, y: origin.y, z: origin.z }, { x: dx, y: dy, z: dz }, range);
    const wallDist = wall.hit ? wall.dist : range;

    // Nearest enemy along the ray, closer than the wall.
    const o = [origin.x, origin.y, origin.z];
    const d = [dx, dy, dz];
    let best = null, bestDist = wallDist;
    for (const c of this.combatants) {
      if (c === shooter || !c.alive || c.team === shooter.team) continue;
      const r = c.radius;
      const min = [c.pos.x - r, c.pos.y, c.pos.z - r];
      const max = [c.pos.x + r, c.pos.y + c.height, c.pos.z + r];
      const t = rayAABB(o, d, min, max);
      if (t !== null && t < bestDist) { bestDist = t; best = c; }
    }

    const end = new THREE.Vector3(o[0] + d[0] * bestDist, o[1] + d[1] * bestDist, o[2] + d[2] * bestDist);
    this._spawnTracer(origin, end, shooter.team);

    if (best) {
      const wasAlive = best.alive;
      best.damage(damage, shooter);
      if (wasAlive && !best.alive && this.onKill) this.onKill(shooter, best);
      return { hitEntity: best, point: end };
    }
    return { hitEntity: null, point: end };
  }

  _spawnTracer(a, b, team) {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array([a.x, a.y, a.z, b.x, b.y, b.z]), 3));
    const color = team === 0 ? 0xffb3c1 : 0xa9d6ff;
    const mat = new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.9 });
    const line = new THREE.Line(geo, mat);
    line.frustumCulled = false;
    this.scene.add(line);
    this.tracers.push({ line, life: 0.07, max: 0.07 });
  }

  update(dt) {
    for (let i = this.tracers.length - 1; i >= 0; i--) {
      const tr = this.tracers[i];
      tr.life -= dt;
      if (tr.life <= 0) {
        this.scene.remove(tr.line);
        tr.line.geometry.dispose();
        tr.line.material.dispose();
        this.tracers.splice(i, 1);
      } else {
        tr.line.material.opacity = 0.9 * (tr.life / tr.max);
      }
    }
  }
}
