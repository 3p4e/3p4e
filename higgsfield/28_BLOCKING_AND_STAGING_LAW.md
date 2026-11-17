# 28 — Blocking & Staging Law (injected ahead of every prompt)

This block is the mandatory preamble to **every** keyframe prompt and **every** video
prompt from this point on. It exists because three rounds of stills failed for one
reason: the prompts described how characters *look*, never where their bodies *point*.

**Rule of the fix:** a fight scene is a geometry problem. Prompt the geometry before
the costume.

---

## THE BLOCK (inject verbatim first, before all other text)

```
BLOCKING (hard law, do not deviate):
Camera: three-quarter side angle, low, 24mm lens. NEVER frontal to the fight.
Hero A (DD): torso and head oriented AT the boss. Line of action: weapon to boss.
Hero B (Azulon): torso and head oriented AT the boss. Half-step behind Hero A,
  opposite shoulder, weapon at eye line.
Boss (Mal'garot): facing the heroes, centre-right of frame, full silhouette readable.
Sightlines: all three heads converge on one point between them. No body faces the lens.
Depth: midground heroes in focus, background threat visible, ground plane continuous.
```

### Why each line exists

| Line | Defect it kills |
|---|---|
| Camera three-quarter, never frontal | the "poster pose with monster behind" failure |
| Hero A oriented AT boss + line of action | hero staring at the lens |
| Hero B opposite shoulder, half-step back | two statues standing in parallel |
| Boss facing them, centre-right | boss becomes a disconnected backdrop |
| Sightlines converge | the "backs to the threat about to kill them" failure |
| No body faces the lens | every figure posing for a portrait |
| Depth planes named | flat cardboard staging |

---

## 12 STAGED REFERENCE DESCRIPTIONS

Each archetype is a complete, reusable spatial prescription. A shot picks one
archetype and substitutes its characters/ability; the geometry is fixed.

01. **The Standoff** — both heroes side-by-side, facing boss; boss full figure facing
them; low angle behind heroes over one shoulder; boss centred-right.

02. **The Tag-Out** — hero A attacks foreground, hero B crosses behind into the
next position; camera pans to follow the crossing; boss reacts to the *new* threat.

03. **The Flank** — hero A engages frontally, hero B enters from screen edge at an
angle; two sightlines converge on boss from different directions.

04. **The Split-Engagement** — boss between the heroes; one left, one right; both
facing boss; camera two-shot keeps both in frame.

05. **The Pursuit** — boss moving away, heroes chasing toward camera-left; camera
tracks back; heroes' faces in 3/4 profile toward boss, not to lens.

06. **The Trap-Spring** — heroes flank a doorway/choke point; both bodies angled to
where boss will appear; sightlines pre-point to empty space.

07. **The Aerial Combo** — one hero airborne above/behind, other ground-level;
both aligned on boss below; camera low looking up through both.

08. **The Cover-Expose** — hero A distracts front-on, hero B braced behind cover at
edge; camera looks from boss's side so both faces read.

09. **The Disarm** — close 3/4; hero A's weapon hand toward boss, body coiled;
boss's weapon hand toward hero A; profiles facing each other, never the lens.

10. **The Interposition** — hero B steps between boss and a downed hero A; back to
the *downed ally*, front to the boss; camera side-on to both.

11. **The Collapse-Rally** — boss floods the frame, heroes staggered in depth, the
nearer hero partially back-turned but head clearly toward boss; far hero fully facing.

12. **The Killing Blow** — single hero square to boss, profile to camera; the
decisive weapon held on the boss-line of action; boss towering, facing the blow.

---

## INJECTION CONTRACT

1. `build_bossfight_jobs.py` prepends the BLOCK to every START and END prompt.
2. `run_wan_flf.py` prepends the BLOCK to every video prompt body.
3. A build fails (exit 1) if any prompt lacks the BLOCK — a machine-checked gate,
   not a human promise.
4. The 12 archetypes are asserted in the job builder: a shot must name its archetype
   or the builder rejects it.

## ACCEPTANCE

A still FAILS if any of these is true:
- any combatant's body faces the camera front-on
- any combatant's head is oriented away from the boss while the boss is a threat
- the boss is a backdrop behind the heroes rather than a facing opponent
- sightlines do not converge

This is the corrected standard that s19_end met by accident and every other still
missed. It becomes deliberate.
