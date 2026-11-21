# Grasp geometry v2 (Apartment 1122, Dex1 two-jaw gripper): what each grasp type assumes

All of it is BY GEOMETRY, NOT VERIFIED in simulation. The live agents confirm or reject each type.
Made 18 Nov 2026 by the planning agent (AI-operated, offline: no simulator was run).

## Files (all in C:\Users\raresense\sim_home\apartment\full_plan\)
- `grasp_types.py`: the module, pure numpy. The five searches plus `load()`, `best()`, `candidates()` and `to_world()`.
- `grasps_v2.json`: candidates for all 198 loose things (made by `make_grasps_v2.py`, `py -3.12`, about 30 s).
- `hollow_colliders.json` / `make_hollow_colliders.py`: the hollow cup/glass/bowl colliders the rim pinch needs.

```python
import sys; sys.path.insert(0, r"C:/Users/raresense/sim_home/apartment/full_plan")
import grasp_types as GT
T = GT.load()                                   # {display name: entry}
c = GT.best(T, "r183i1_cup")                    # 'yes' before 'marginal'; order top_down, side, surface_pinch, rim_pinch, edge
GT.candidates(T, "r183i1_cup", "rim_pinch")     # all rim pinches, best first
GT.to_world(c["point"])                         # scene -> episode world (minus 0.90, 0.45)
```

A candidate has these fields:
- `type` and `verdict` (yes / marginal);
- `point`: the middle between the pads;
- `close`: the unit closing direction;
- `approach`: the direction the hand moves in at the end;
- `jaw_gap_m`: the opening to come in with;
- `width_m`: the material between the pads;
- `bite_m`: how much pad is on the thing;
- `pad_bottom_above_support_m`;
- `score` (lower is better);
- `notes` and `needs` (the skill it takes);
- extras per type.

An entry also has:
- `why_not` per type;
- `support` and `z_support_m`;
- `hollow_collider` (true if hollow_colliders.json has the body);
- `opening` (depth, rim radius, axis).

The frame is the pack's scene frame (metres, Z up).

## Gripper numbers used
Sources: E:\urc_home\scripts\towel_prep\build_g1_dex1.py and the dex1_1 meshes, measured.
- The jaws open 7.9 cm between the pad faces. The task text says 8.2 cm.
- Pad: 2.9 cm across the finger x 2.9 cm along it, 1.15 cm thick. The brief says "about 2 cm wide"; the model's pad box is 2.9 cm.
- Jaw body: 1.5 cm behind each pad face. Finger plate: 3.9 cm across.
- Palm (base front face): 6.2 cm behind the pad middle. Base: 6.2 x 5.8 cm across, 7.4 cm long.
- Squeeze: 6 N a pad (measured in the floor agent's runs); motor limit 20 N. Pad friction 1.2.
- Mass limits are applied by the planner, not here: over 1.5 kg is not carried, 0.8-1.5 kg is marginal.

## The five types

### top_down (existing)
The floor agent's section search (`grasp_geom.find`, copied unchanged as `section_search`).
- Points: collision-mesh vertices, face centres and edge middles.
- The jaws come straight down fully open over a section and close horizontally.
- Everything of the thing above the pads' lower edge, within the pad width, fits between the jaws with 4.5 mm to spare a side, so the widest section is 7.0 cm.
- The closing fingers meet nothing wider than the section.
- Pads: lower edge 6 mm above the support, at least 8 mm of pad on the thing, the palm above the thing's top.
- `marginal` if it fits only with 0.5 mm a side (up to 7.8 cm), or if the section is over 8 cm off the middle of a thing over 0.2 kg.

### surface_pinch (new)
The same search with the fingertips 1.5 mm above the support: they touch the floor or table and slide on it while closing.
- Pads need at least 6 mm of bite.
- Only for low things, 1.0 to 6 cm high.
- Verdict by height: `yes` from 1.5 cm, `marginal` from 1.0 to 1.5 cm, nothing under 1.0 cm (no pad contact worth having).
- Needs a new hand posture: the hand pressed lightly onto the support while the jaws close.

### side (new)
The hand is level, the fingers horizontal; the jaws close horizontally on a section at pad-middle height zm.
- Points: collision-mesh surface samples, 3 mm apart.
- 24 approach headings, zm in 1 cm steps.
- The section between the pads (2.9 cm deep along the approach, 2.9 cm high) must be under 7.9 cm. `marginal` when under 4.5 mm to spare a side.
- From fingertip to palm, the fingers must meet nothing wider than that section, and the palm meets nothing.
- Pad lower edge at least 6 mm, and finger plate at least 1 mm, above the support.
- The gripper base hangs 3.1 cm below the pad middle. If it would touch the support with a level hand, the hand must pitch down (computed, at most 35 deg) and the grasp is `marginal`.
- Below the centre of mass of a thing over 0.2 kg: noted (it can tip in the jaws).
- On the floor, a side grasp needs the hand level a few cm above the floor in the deep squat: not measured.

### rim_pinch (new)
One jaw inside the cup / glass / bowl, one outside; the jaws are stopped part-open, at the wall in the pad band plus 2 x 5 mm, and close on the wall.
- Points: the VISUAL mesh, 2 mm apart (the pack's collider is solid).
- The opening comes from `make_hollow_colliders.cavity()`. 24 azimuths. Bite tried at 2.5 / 2 / 1.5 / 1 cm below the rim.
- The inner jaw (1.5 cm body behind the pad) must be clear of the inside: the cavity floor, the far wall, the contents.
- The outer jaw must be clear of handles and flares, and its tip 4 mm above the support.
- `jaw_gap_m` is the opening to stop at. It includes the rim's curve over the 2.9 cm pad: the flat inner pad touches the inner wall at its two corners.
- Verdicts:
  - `yes` only with the hollow collider in the room (`hollow_collider: true`). Without it the verdict is `no`: the inner jaw would stand on the solid hull.
  - `marginal` when the weight's turning moment at the rim (m g r) is over what the pad pair resists at 6 N (6 N x bite); the note says whether 20 N would hold it, or whether it will swing to hang from the grip.
  - `marginal` when the opening faces sideways (the lying tumbler).
- Needs a new skill (jaws stopped part-open, inner jaw lowered inside).

### edge (new)
For flat things on furniture, 8 cm high or less. The gripper is turned so the jaws close VERTICALLY with the fingers horizontal; the lower jaw goes under the part that overhangs the table edge.
- The support's top comes from its collision mesh (1 cm grid). 24 outward directions.
- Overhang: how far the thing's outer edge, across the pad width, is beyond the support edge.
- Overhang of 1.5 cm or more: grasp directly. Otherwise slide it out first (`slide_m`) with a fingertip press-and-drag: within 3 cm of the edge it is `yes`, a longer slide (up to 30 cm) is `marginal`.
- Thickness at the edge must be under 7.9 cm (`marginal` when under 4.5 mm to spare a side).
- Weight held at the edge: the turning moment m g x lever is compared with 6 N x bite. If it is larger, the thing swings down to hang from the grip (fine for carrying to the sink if nothing is hit), or it needs two hands.
- NOT checked here, but checked by the planner: whether that edge is free (not against a wall or other furniture) and whether the robot can stand facing it, and whether the slide path is clear of other things.

## Known limits of the geometry (all types)
- Things are rigid at the pack's start poses. Cloth, crumpled paper and bags are rigid hulls in our model; the 7 garments are cloth and handled by the cloth agent, not here.
- Contact, friction and the reach of the arm are not simulated. The planner adds reach, using its assumed limits or the measured map once one exists.
