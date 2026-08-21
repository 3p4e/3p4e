import * as THREE from 'three';
import { WORLD, BLOCK, BLOCK_COLORS } from './config.js';

const { W, H, D, WALL_H } = WORLD;

export class World {
  constructor() {
    this.W = W;
    this.H = H;
    this.D = D;
    this.data = new Uint8Array(W * H * D); // block id per cell, 0 = air
    this.group = new THREE.Group();
    this.meshes = new Map(); // block id -> { mesh, capacity }
    this.dirty = false;
    this._dummy = new THREE.Object3D();
    this.generate();
  }

  idx(x, y, z) {
    return x + W * (z + D * y);
  }

  inBounds(x, y, z) {
    return x >= 0 && x < W && y >= 0 && y < H && z >= 0 && z < D;
  }

  getBlock(x, y, z) {
    if (!this.inBounds(x, y, z)) return BLOCK.AIR;
    return this.data[this.idx(x, y, z)];
  }

  isSolid(x, y, z) {
    if (!this.inBounds(x, y, z)) return false;
    return this.data[this.idx(x, y, z)] !== BLOCK.AIR;
  }

  setBlock(x, y, z, id) {
    if (!this.inBounds(x, y, z)) return;
    this.data[this.idx(x, y, z)] = id;
    this.dirty = true;
  }

  // Floor + perimeter walls are permanent so nobody can dig out of the arena.
  isIndestructible(x, y, z) {
    if (y === 0) return true;
    if (x === 0 || x === W - 1 || z === 0 || z === D - 1) return y <= WALL_H;
    return false;
  }

  // ---- Arena generation ------------------------------------------------
  generate() {
    // Bedrock floor.
    for (let x = 0; x < W; x++) {
      for (let z = 0; z < D; z++) {
        this.data[this.idx(x, 0, z)] = BLOCK.BEDROCK;
        this.data[this.idx(x, 1, z)] = BLOCK.GRASS;
      }
    }

    // Perimeter walls.
    for (let y = 2; y <= WALL_H; y++) {
      for (let x = 0; x < W; x++) {
        this.data[this.idx(x, y, 0)] = BLOCK.STONE;
        this.data[this.idx(x, y, D - 1)] = BLOCK.STONE;
      }
      for (let z = 0; z < D; z++) {
        this.data[this.idx(0, y, z)] = BLOCK.STONE;
        this.data[this.idx(W - 1, y, z)] = BLOCK.STONE;
      }
    }

    // Team bases: colored platforms + low walls at opposite ends (along Z).
    this._buildBase(BLOCK.RED_BASE, D - 9);
    this._buildBase(BLOCK.BLUE_BASE, 4);

    // Cover: scattered pillars and low walls across the mid-field.
    this._buildCover();

    this.dirty = true;
  }

  _buildBase(id, zStart) {
    const cx = Math.floor(W / 2);
    for (let x = cx - 6; x <= cx + 6; x++) {
      for (let z = zStart; z < zStart + 5; z++) {
        this.data[this.idx(x, 1, z)] = id; // colored floor pad
      }
    }
    // Two chest-high side pillars framing the spawn pad.
    for (const px of [cx - 6, cx + 6]) {
      for (let y = 2; y <= 3; y++) {
        this.data[this.idx(px, y, zStart)] = id;
        this.data[this.idx(px, y, zStart + 4)] = id;
      }
    }
  }

  _buildCover() {
    // Deterministic pseudo-random layout (no Math.random dependency at import).
    let seed = 1337;
    const rand = () => {
      seed = (seed * 1103515245 + 12345) & 0x7fffffff;
      return seed / 0x7fffffff;
    };
    const cxWorld = W / 2;
    const czWorld = D / 2;
    for (let i = 0; i < 46; i++) {
      const x = 6 + Math.floor(rand() * (W - 12));
      const z = 14 + Math.floor(rand() * (D - 28));
      const h = 2 + Math.floor(rand() * 3);
      const kind = rand();
      if (kind < 0.5) {
        // vertical pillar
        for (let y = 2; y < 2 + h; y++) this.data[this.idx(x, y, z)] = BLOCK.STONE;
      } else {
        // small L-shaped wall for cover
        const len = 2 + Math.floor(rand() * 3);
        const horiz = rand() < 0.5;
        for (let k = 0; k < len; k++) {
          const bx = horiz ? Math.min(W - 2, x + k) : x;
          const bz = horiz ? z : Math.min(D - 2, z + k);
          for (let y = 2; y < 2 + Math.min(h, 3); y++) {
            this.data[this.idx(bx, y, bz)] = BLOCK.WOOD;
          }
        }
      }
      // Keep the very center clear-ish so bases have sightlines to fight over.
      void cxWorld;
      void czWorld;
    }
  }

  // ---- Voxel raycast (Amanatides & Woo) --------------------------------
  // Returns the first solid voxel hit within maxDist, plus the face normal
  // pointing back toward the ray origin (the empty side, for placement).
  raycast(origin, dir, maxDist) {
    let x = Math.floor(origin.x);
    let y = Math.floor(origin.y);
    let z = Math.floor(origin.z);

    const stepX = dir.x > 0 ? 1 : dir.x < 0 ? -1 : 0;
    const stepY = dir.y > 0 ? 1 : dir.y < 0 ? -1 : 0;
    const stepZ = dir.z > 0 ? 1 : dir.z < 0 ? -1 : 0;

    const invX = dir.x !== 0 ? 1 / Math.abs(dir.x) : Infinity;
    const invY = dir.y !== 0 ? 1 / Math.abs(dir.y) : Infinity;
    const invZ = dir.z !== 0 ? 1 / Math.abs(dir.z) : Infinity;

    let tMaxX =
      stepX > 0 ? (x + 1 - origin.x) * invX : stepX < 0 ? (origin.x - x) * invX : Infinity;
    let tMaxY =
      stepY > 0 ? (y + 1 - origin.y) * invY : stepY < 0 ? (origin.y - y) * invY : Infinity;
    let tMaxZ =
      stepZ > 0 ? (z + 1 - origin.z) * invZ : stepZ < 0 ? (origin.z - z) * invZ : Infinity;

    const tDeltaX = invX;
    const tDeltaY = invY;
    const tDeltaZ = invZ;

    let nx = 0, ny = 0, nz = 0;
    let t = 0;

    // Ignore the origin cell itself (camera should be in air).
    for (let i = 0; i < 512; i++) {
      if (this.isSolid(x, y, z) && !(nx === 0 && ny === 0 && nz === 0)) {
        return { hit: true, x, y, z, nx, ny, nz, dist: t };
      }
      if (tMaxX < tMaxY && tMaxX < tMaxZ) {
        if (tMaxX > maxDist) break;
        x += stepX; t = tMaxX; tMaxX += tDeltaX; nx = -stepX; ny = 0; nz = 0;
      } else if (tMaxY < tMaxZ) {
        if (tMaxY > maxDist) break;
        y += stepY; t = tMaxY; tMaxY += tDeltaY; nx = 0; ny = -stepY; nz = 0;
      } else {
        if (tMaxZ > maxDist) break;
        z += stepZ; t = tMaxZ; tMaxZ += tDeltaZ; nx = 0; ny = 0; nz = -stepZ;
      }
    }
    // Check the final cell we stepped into (up to maxDist).
    if (t <= maxDist && this.isSolid(x, y, z) && !(nx === 0 && ny === 0 && nz === 0)) {
      return { hit: true, x, y, z, nx, ny, nz, dist: t };
    }
    return { hit: false };
  }

  // ---- Rendering (instanced cubes, one InstancedMesh per block color) ---
  _hasAirNeighbor(x, y, z) {
    return (
      !this.isSolid(x + 1, y, z) || !this.isSolid(x - 1, y, z) ||
      !this.isSolid(x, y + 1, z) || !this.isSolid(x, y - 1, z) ||
      !this.isSolid(x, y, z + 1) || !this.isSolid(x, y, z - 1)
    );
  }

  buildMeshes() {
    this.rebuild();
    return this.group;
  }

  rebuild() {
    // Bucket every surface-exposed voxel by block id.
    const buckets = new Map();
    for (let y = 0; y < H; y++) {
      for (let z = 0; z < D; z++) {
        const base = W * (z + D * y);
        for (let x = 0; x < W; x++) {
          const id = this.data[base + x];
          if (id === BLOCK.AIR) continue;
          if (!this._hasAirNeighbor(x, y, z)) continue; // cull enclosed cubes
          let arr = buckets.get(id);
          if (!arr) { arr = []; buckets.set(id, arr); }
          arr.push(x, y, z);
        }
      }
    }

    const geo = World._geometry();
    // Update / create an InstancedMesh per block id.
    for (const [id, coords] of buckets) {
      const count = coords.length / 3;
      let entry = this.meshes.get(id);
      if (!entry || entry.capacity < count) {
        if (entry) { this.group.remove(entry.mesh); entry.mesh.dispose?.(); }
        const capacity = Math.ceil(count * 1.5) + 16;
        const mat = new THREE.MeshLambertMaterial({ color: BLOCK_COLORS[id] });
        const mesh = new THREE.InstancedMesh(geo, mat, capacity);
        mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
        mesh.castShadow = false;
        mesh.receiveShadow = false;
        this.group.add(mesh);
        entry = { mesh, capacity };
        this.meshes.set(id, entry);
      }
      const mesh = entry.mesh;
      const dummy = this._dummy;
      for (let i = 0; i < count; i++) {
        dummy.position.set(coords[i * 3] + 0.5, coords[i * 3 + 1] + 0.5, coords[i * 3 + 2] + 0.5);
        dummy.updateMatrix();
        mesh.setMatrixAt(i, dummy.matrix);
      }
      mesh.count = count;
      mesh.instanceMatrix.needsUpdate = true;
      mesh.computeBoundingSphere();
    }
    // Any block id no longer present -> hide.
    for (const [id, entry] of this.meshes) {
      if (!buckets.has(id)) entry.mesh.count = 0;
    }
    this.dirty = false;
  }

  static _geometry() {
    if (!World.__geo) World.__geo = new THREE.BoxGeometry(1, 1, 1);
    return World.__geo;
  }
}
