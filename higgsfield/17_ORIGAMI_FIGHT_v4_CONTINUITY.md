# 17 — THE ORIGAMI ASCENSION (v4) — CONTINUITY MAP

Supersedes `16_ORIGAMI_SERAPH_FIGHT_v3_SCRIPT.md`.

v3 was a list of 12 spectacular images. **v4 makes it one continuous fight** where
every shot's OUT state is the next shot's IN state, and the kill is caused by
something set up six beats earlier.

---

## CONTINUITY DEFECTS IN v3 (found by audit, all fixed here)

| # | Defect | Consequence |
|---|---|---|
| D1 | or_03 had Azulon **shatter his own wings** into cranes | or_05 and or_09 show six intact wings. Wings cannot grow back unexplained. |
| D2 | or_06 he becomes a **blade**, or_07 he is a **colossus** | Two transformations back to back with no re-fold beat. |
| D3 | or_08 ends in a **burning sphere of annihilation** | or_09 ignores it entirely and starts a fresh attack. |
| D4 | or_09 called his **"ultimate"** but does not win | then a *smaller* spear attack kills. Power logic inverted. |
| D5 | or_04 the Stain **unfolds into a wall** | or_05 it is dripping tar again with no reset. |
| D6 | The Stain's size changes with **no stated cause** | it grows between 04 and 07 for free. |

---

## THE CAUSAL SPINE (this is the fix for D4)

> Azulon's blade storm is **devoured** by the Stain in beat 10.
> So the blades are **inside** it.
> The dart in beat 12 does not kill by force — it **detonates the blades the Stain swallowed**.

The Stain's own hunger is the weapon. Setup at 10, payoff at 12.

Its size also now has a stated cause: **it grows by eating his attacks.**
Beat 04 eats the crane swarm and swells. Beat 10 eats the blade storm and swells.

---

## STATE CHAIN

Each beat declares **IN** (must match previous OUT) and **OUT**.

| Beat | IN | OUT |
|---|---|---|
| 01 corruption revealed | void empty | `stain_revealed_dripping` |
| 02 hunter descends | `stain_revealed_dripping` | `hunter_above_wings_open` |
| 03 thousand cranes | `hunter_above_wings_open` | `crane_swarm_descending_wings_ragged` |
| 04 stain devours | `crane_swarm_descending_wings_ragged` | `stain_cathedral_wall_swarm_eaten` |
| 05 tar tide | `stain_cathedral_wall_swarm_eaten` | `tar_ocean_surging` |
| 06 blade splits tide | `tar_ocean_surging` | `tide_cut_collapsing_hero_as_blade` |
| 07 colossus vs cathedral | `tide_cut_collapsing_hero_as_blade` | `both_colossal_facing` |
| 08 sphere of annihilation | `both_colossal_facing` | `collision_sphere_burning` |
| 09 thousandfold dawn | `collision_sphere_burning` | `blade_storm_expanding_blades_swallowed` |
| 10 final unfold | `blade_storm_expanding_blades_swallowed` | `stain_unfolded_blades_inside` |
| 11 spear pierce | `stain_unfolded_blades_inside` | `hole_punched_fire_igniting_inside` |
| 12 annihilation ascension | `hole_punched_fire_igniting_inside` | `stain_destroyed_hero_lands_void_empty` |

---

## THE BEATS, WITH THE FIXES INLINE

**01 · CORRUPTION REVEALED — monster.** The Stain looms over a vast invisible plane
in a starless void, six ragged wings dripping glossy black into a wide pooled mirror.
*OUT: it is revealed, dripping, alone.*

**02 · THE HUNTER DESCENDS — hero.** Azulon plummets from above, wings snapping open,
white flame racing every edge. The Stain waits below, unimpressed.
*OUT: he is above it, wings open, lit.*

**03 · THOUSAND CRANES — hero.** *Fix D1:* he does not shatter his wings —
**thousands of folded cranes tear free from his outstretched wings**, leaving them
ragged and thinned but still six. The swarm streaks down.
*OUT: ragged-winged hunter above, crane swarm descending.*

**04 · THE STAIN DEVOURS — monster.** Its wings **unfold into a cathedral wall**
and swallow the swarm; white fire drowns in black goo that brightens as it feeds.
*It grows — stated cause: it ate his attack.*
*OUT: wall of stained parchment, swarm eaten, Stain larger.*

**05 · THE TAR TIDE — both.** *Fix D5:* the wall **collapses back into its wings**,
and from those wings a tidal ocean of black tar erupts at Azulon, who is now small
and blazing above it.
*OUT: tar ocean surging up at him.*

**06 · BLADE SPLITS THE TIDE — hero.** He re-folds into a **blade** and dives; the
ocean parts in a steaming canyon and collapses on both sides behind him.
*OUT: tide cut and collapsing, hero beyond it in blade form.*

**07 · COLOSSUS VS CATHEDRAL — both.** *Fix D2:* he **unfolds from the blade into
a colossus**, ivory plates burning white. The Stain answers by unfolding into an
ever-growing mass that fills the frame.
*OUT: both colossal, facing each other.*

**08 · SPHERE OF ANNIHILATION — both.** They collide. White flame meets black tar in
a blinding sphere, concentric shockwaves shredding pages to confetti, the void bowing.
*OUT: sphere burning at frame centre, both silhouettes inside it.*

**09 · THOUSANDFOLD DAWN — hero.** *Fix D3/D4:* this is **not a fresh attack and not
the kill** — it is him **bursting out of the sphere**, all six wings detonating into
uncountable burning blades, a radial storm screaming outward.
*OUT: blade storm expanding outward.*

**10 · THE FINAL UNFOLD — monster.** Cornered, it **unfolds completely** into a
cathedral nest and **eats the blade storm**, swelling beyond the frame — but the blades
are now **inside it**.
*OUT: unfolded nest, blade storm swallowed, blades inside it.*

**11 · THE SPEAR PIERCE — hero.** He compresses to a **single white dart** and punches
a thin clean line straight through the mass — in one side, out the other.
*OUT: hole punched through it, white fire igniting inside.*

**12 · ANNIHILATION AND ASCENSION — both.** *The payoff:* the **blades it swallowed
detonate inside it**. White fire erupts from within, tar burns to vapour, the body
crumbles into glowing dust, clean cranes rise. Azulon lands, wings folding.
*OUT: enemy destroyed, hero landed, void empty.*

---

## RULES FOR THE RENDER

- Every prompt must **name the entry state** so the model cannot restage the world.
- Motion is always **continuing**, never a new tableau ("mid-", "already", "still").
- No shot may show a state the previous shot did not produce.
- 12 beats × ~5 s ≈ **60 s**.
- Seeds 800–811.
