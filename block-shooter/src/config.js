// Central tuning + data tables for the block-world team shooter.

// ---- World dimensions (in blocks / world units; 1 block = 1 unit) ----
export const WORLD = {
  W: 64, // x
  H: 24, // y (up)
  D: 64, // z
  WALL_H: 6, // perimeter wall height
};

// ---- Block types -------------------------------------------------------
// id 0 is always air. Every other id maps to a solid, colored cube.
export const BLOCK = {
  AIR: 0,
  GRASS: 1,
  STONE: 2,
  BEDROCK: 3,
  RED_BASE: 4,
  BLUE_BASE: 5,
  WOOD: 6,
  WHITE: 7,
  YELLOW: 8,
  GREEN: 9,
  PURPLE: 10,
  ORANGE: 11,
};

// Color per block id (index === block id). Index 0 (air) is never rendered.
export const BLOCK_COLORS = [
  0x000000, // 0 air (unused)
  0x55a630, // 1 grass
  0x8d99ae, // 2 stone
  0x3a3d4a, // 3 bedrock
  0xef476f, // 4 red base
  0x4895ef, // 5 blue base
  0xb5651d, // 6 wood
  0xedf2f4, // 7 white
  0xffd166, // 8 yellow
  0x06d6a0, // 9 green
  0x9b5de5, // 10 purple
  0xf77f00, // 11 orange
];

// Blocks the player can select and place (mouse wheel / number keys).
export const PALETTE = [
  BLOCK.WHITE,
  BLOCK.WOOD,
  BLOCK.STONE,
  BLOCK.YELLOW,
  BLOCK.GREEN,
  BLOCK.PURPLE,
  BLOCK.ORANGE,
  BLOCK.RED_BASE,
  BLOCK.BLUE_BASE,
];

export const PALETTE_NAMES = {
  [BLOCK.WHITE]: 'White',
  [BLOCK.WOOD]: 'Wood',
  [BLOCK.STONE]: 'Stone',
  [BLOCK.YELLOW]: 'Yellow',
  [BLOCK.GREEN]: 'Green',
  [BLOCK.PURPLE]: 'Purple',
  [BLOCK.ORANGE]: 'Orange',
  [BLOCK.RED_BASE]: 'Red',
  [BLOCK.BLUE_BASE]: 'Blue',
};

// ---- Teams -------------------------------------------------------------
export const TEAM = { RED: 0, BLUE: 1 };
export const TEAM_INFO = {
  [TEAM.RED]: { name: 'RED', color: 0xef476f, css: '#ef476f' },
  [TEAM.BLUE]: { name: 'BLUE', color: 0x4895ef, css: '#4895ef' },
};

// ---- Player physics + combat ------------------------------------------
export const PLAYER = {
  radius: 0.3,
  height: 1.7,
  eye: 1.5,
  moveSpeed: 5.5,
  sprintSpeed: 8.5,
  jumpSpeed: 8.2,
  gravity: 24,
  maxHealth: 100,
  reach: 6, // block place/destroy distance
};

export const WEAPON = {
  damage: 22,
  range: 90,
  fireInterval: 0.11, // seconds between shots
  spread: 0.008, // radians of random cone
};

// ---- Bots --------------------------------------------------------------
export const BOT = {
  radius: 0.3,
  height: 1.7,
  eye: 1.4,
  moveSpeed: 3.8,
  jumpSpeed: 8.0,
  gravity: 24,
  maxHealth: 100,
  damage: 12,
  range: 42,
  fireInterval: 0.55,
  spread: 0.045, // less accurate than the player
  sightRange: 72, // how far a bot will seek/track an enemy
  perTeam: 4, // bots per team (player replaces one blue slot)
};

export const RULES = {
  respawnTime: 3.0, // seconds
  scoreToWin: 25,
  killPlaneY: -6, // fall below this = death
};
