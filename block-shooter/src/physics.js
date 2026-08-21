// Axis-separated AABB vs voxel collision + movement.
// An "entity" is any object shaped like:
//   { pos:{x,y,z}, vel:{x,y,z}, radius, height, onGround }
// pos is the entity's feet position; the AABB spans
//   [pos.x-radius, pos.x+radius] x [pos.y, pos.y+height] x [pos.z-radius, pos.z+radius].

const EPS = 1e-4;

// Does the entity's AABB (at the given feet position) overlap any solid voxel?
function collides(world, x, y, z, radius, height) {
  const minX = Math.floor(x - radius + EPS);
  const maxX = Math.floor(x + radius - EPS);
  const minY = Math.floor(y + EPS);
  const maxY = Math.floor(y + height - EPS);
  const minZ = Math.floor(z - radius + EPS);
  const maxZ = Math.floor(z + radius - EPS);
  for (let by = minY; by <= maxY; by++) {
    for (let bz = minZ; bz <= maxZ; bz++) {
      for (let bx = minX; bx <= maxX; bx++) {
        if (world.isSolid(bx, by, bz)) return true;
      }
    }
  }
  return false;
}

// Integrate velocity into position, resolving collisions one axis at a time so
// the entity slides along walls instead of stopping dead. Mutates ent.
export function moveEntity(world, ent, dt) {
  const { radius, height } = ent;
  const p = ent.pos;
  const v = ent.vel;

  // X axis
  let nx = p.x + v.x * dt;
  if (!collides(world, nx, p.y, p.z, radius, height)) p.x = nx;
  else v.x = 0;

  // Z axis
  let nz = p.z + v.z * dt;
  if (!collides(world, p.x, p.y, nz, radius, height)) p.z = nz;
  else v.z = 0;

  // Y axis (track ground contact)
  ent.onGround = false;
  let ny = p.y + v.y * dt;
  if (!collides(world, p.x, ny, p.z, radius, height)) {
    p.y = ny;
  } else {
    if (v.y <= 0) ent.onGround = true;
    v.y = 0;
  }
}

export { collides };
