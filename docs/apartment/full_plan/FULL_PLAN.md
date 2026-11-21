# Apartment 1122: full tidy plan for one continuous episode

Generated 2026-11-19 00:10 by `C:/Users/raresense/sim_home/apartment/full_plan/make_full_plan.py` (rerun: `py -3.12` on that file, about 25 s).
**Nothing in this file is a simulation result.** Every reach and grasp judgement is by geometry, not verified. Coordinates are the pack's scene frame; the episode's world frame is scene - (0.90, 0.45).

## v2 in short (v1 is kept as FULL_PLAN_v1.md, full_plan_v1.json, route_steps_v1.json, room_patch_v1.json)
- **48 of the 69 mess things are planned** (v1: 25). By grasp type (by geometry, not verified; the live agents confirm or reject each NEW type): top_down 16, cloth 7, side 5, surface_pinch 11, rim_pinch 2, edge 7.
- 8 mess things have no grasp of any of the five types (list below: what remains impossible with a two-jaw gripper, and why); 13 more have a grasp but no standing place within reach, a destination that cannot be reached, or no free target spot.
- The sink decides most of the rest: 3 dishes with a grasp wait for it. Its nearest standing place is 0.56 m from the basin with the dishwasher closed (marginal under the 0.5 m limit; it would be marginal under v1's 0.60 m) and 1.16 m with it open. The measured furniture reach map (cloth/surface agent) settles it; the corner cabinet's 12 cm bottom panel, which sticks out 25 cm in front of its diagonal face, is what keeps the robot away (see 'The sink and the dishwasher').
- New in v2: five grasp types from the collision and visual meshes (grasps_v2.json, grasp_types.py, README_GRASPS.md); hollow colliders for 16 cups / glasses / bowls / mugs (hollow_colliders.json: the pack's colliders are solid hulls, so no rim pinch is possible without them); a collider for the SINK (the pack's sink has none: a dish let go over it falls into the cabinet); the dishwasher closed as an OPTIONAL step (sink stance computed both ways); a target spot for every planned thing (basket and sink slots too); a hook that reads a MEASURED reach map once the cloth/surface agent names one in PROGRESS_CLOTH.md (used: C:\Users\raresense\sim_home\apartment\reach\planner_reach_rows.json).
- v1's own outputs predate the previous agent's last edit of make_full_plan.py (a tight 7.8 cm section fallback and reach limits 0.34 / 0.50 m instead of 0.45 / 0.60 m): part of the change from v1 comes from that, not from the new grasp types. Reach sensitivity (same v2 code, other limits): reach 0.45 / 0.6 m, dishwasher closed: 50 planned; reach 0.34 / 0.5 m, dishwasher open: 28 planned; reach 0.45 / 0.6 m, dishwasher open: 28 planned.

## Counts
- Loose objects in the pack: 198 (+ our added rubbish bin).
- Mess to move: 69 (48 planned in the route, 21 skipped). Mess left on purpose: 13. Already in place: 47. Furniture, appliances and things where they belong: 69.

| Class | all | mess planned | mess skipped | left / in place |
|---|---|---|---|---|
| container | 51 | 7 | 4 | 40 |
| dish | 31 | 11 | 2 | 18 |
| paper | 12 | 5 | 7 | 0 |
| toy | 12 | 10 | 1 | 1 |
| bag | 10 | 1 | 0 | 9 |
| appliance | 8 | 0 | 0 | 8 |
| shoe | 8 | 5 | 2 | 1 |
| textile | 7 | 5 | 0 | 2 |
| plant | 5 | 0 | 0 | 5 |
| electronics | 4 | 0 | 0 | 4 |
| food | 4 | 0 | 1 | 3 |
| cable | 4 | 0 | 0 | 4 |
| table | 4 | 0 | 0 | 4 |
| cushion | 3 | 0 | 0 | 3 |
| clothing | 3 | 1 | 1 | 1 |
| basket | 3 | 0 | 0 | 3 |
| cookware | 3 | 0 | 0 | 3 |
| food_package | 3 | 1 | 0 | 2 |
| tool | 3 | 0 | 1 | 2 |
| toy_vehicle | 3 | 0 | 0 | 3 |
| book | 3 | 0 | 0 | 3 |
| decor | 2 | 0 | 0 | 2 |
| package | 2 | 1 | 1 | 0 |
| stool | 2 | 0 | 0 | 2 |
| umbrella | 2 | 0 | 1 | 1 |
| rug | 1 | 0 | 0 | 1 |
| lamp | 1 | 0 | 0 | 1 |
| kitchenware | 1 | 0 | 0 | 1 |
| hook_rack | 1 | 0 | 0 | 1 |
| stroller | 1 | 0 | 0 | 1 |
| cutlery | 1 | 1 | 0 | 0 |

| Destination | planned | skipped | where the robot stands / reach (by geometry, not verified) |
|---|---|---|---|
| r186i1_basket | 13 | 1 | marginal: the pelvis can stand 0.17 m from it; low shelf: deep squat and a level reach into the cubby (now, before anything is cleared: 0.35 m) |
| floor beside r186i1_basket / r185i1_megabloks_bag (toy corner) | 2 | 0 | floor spots beside the toy basket |
| rubbish_bin | 6 | 7 | marginal: nearest standing place is 0.02 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without) (now, before anything is cleared: 0.38 m) |
| r133i1_laundry_basket | 6 | 0 | yes: the pelvis can stand 0.47 m from it (now, before anything is cleared: 0.83 m) |
| r27i1_sink | 15 | 4 | marginal: nearest standing place is 0.56 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.95 m) limit 0.55 m without) (to the nearest point 6 cm inside the basin; dishwasher closed by the optional step) |
| r119i1_mat | 5 | 2 | marginal: the pelvis can stand 0.22 m from it; low shelf: deep squat and a level reach into the cubby (now, before anything is cleared: 0.81 m) |
| r110i1_console | 0 | 3 | no: nearest standing place is 0.64 m from it (MEASURED (planner_reach_rows.json, pad height 0.80 m) reach 0.43 m at most) (now, before anything is cleared: 1.26 m) |
| r35i1_top | 0 | 2 | no: nearest standing place is 0.63 m from it (MEASURED (planner_reach_rows.json, pad height 0.95 m) reach 0.58 m at most) |
| r94i1_tray_table | 1 | 2 | yes: the pelvis can stand 0.48 m from it |

| Skill needed (planned things) | count | state today |
|---|---|---|
| floor_pick | 20 | exists: proven on one toy piece (run 1118_193303); top-down only |
| cloth_pick | 7 | grasp_cloth written by the cloth agent from its live knit-hat runs (E:/urc_cloth, commit cf4eabf); the other six garments not tried yet |
| surface_pick | 21 | NOT BUILT (no pick from furniture exists) |
| surface_pick, counter 0.91-0.95 m (standing, hand at chest height) | 9 | not built |
| surface_pick, low table / seat 0.45-0.56 m (half squat) | 9 | not built |
| surface_pick, table / sill 0.72-0.78 m (standing) | 3 | not built |
| put: drop_in_sink (lower into the basin) -> r27i1_sink | 15 | NOT BUILT (place into the sink); the sink needs a collider first (none in the pack) |
| put: drop_in -> r133i1_laundry_basket (cloth) | 6 | drop_in_cloth into the open-top hamper: written by the cloth agent from its live knit-hat runs (commit cf4eabf; not checked by the planner) |
| put: place_on (set on a table) -> r94i1_tray_table | 1 | NOT BUILT (place_on a table) |
| put: drop_in -> rubbish_bin | 6 | drop_in: ran in the practice room only, not in the apartment |
| put: put_down (lower into a low basket) -> r186i1_basket | 12 | exists: proven once (toy piece into the toy basket) |
| put: put_down (set on the mat) -> r119i1_mat | 5 | put_down on a flat mat: written, not run yet |
| put: put_down (set on the floor) -> floor beside r186i1_basket / r185i1_megabloks_bag (toy corner) | 2 | put_down on the floor: written, a flat destination is not run yet |
| put: put_down (lower into a low basket) -> r186i1_basket (cloth) | 1 | exists: proven once (toy piece into the toy basket) |
| needs_two_hands | 3 | not built (big garments, things over 1 kg) |
| container_carry | 0 carries | not built |
| door / drawer (OPTIONAL step close_dishwasher) | 1 step | not built; frees the sink. The milk jug (fridge) is still left |

Grasp by geometry over the 69 mess things: yes 39, marginal 22, no 8. Reach: after clearing 17, yes 29, no 10, marginal 13.

## Grasp types (v2, by geometry, not verified)
Exactly what each type assumes: README_GRASPS.md. Counts over the mess things: 'usable' = has a yes / marginal candidate of that type; 'planned with it' = the type the plan uses.

| Grasp type | mess things it can take | planned with it | skill today |
|---|---|---|---|
| top_down | 40 | 16 | fingers-down pick (floor: exists, run 1118_193303; from furniture: not built) |
| side | 44 | 5 | NEW: side grasp, hand level, jaws horizontal (not built) |
| surface_pinch | 22 | 11 | NEW: fingertips on the support while the jaws close (not built) |
| rim_pinch | 7 | 2 | NEW: rim pinch, jaws part-open, one inside (not built; needs the hollow collider) |
| edge | 17 | 7 | NEW: edge grasp, jaws vertical under an overhang, after a slide when needed (not built) |
| cloth (7 garments) | 7 | 7 | cloth pinch (cloth agent's grasp_cloth, written from its live knit-hat runs, commit cf4eabf) |

Planned with a NEW grasp type (the live agents confirm or reject these first):
- r124i1_sandal (shoe): surface_pinch, yes: 4.7 cm high: fingertips at the support, 2.7 cm of pad on it
- r125i1_flat (shoe): surface_pinch, yes: 5.7 cm high: fingertips at the support, 2.6 cm of pad on it
- r148i1_pink_lid (dish): edge, marginal: 6.5 cm from the edge: slide it 8.3 cm out first (more than 3 cm: long slide); 2.4 cm thick at the edge
- r149i1_pouch (food_package): edge, marginal: 24.7 cm from the edge: slide it 26.5 cm out first (more than 3 cm: long slide); 2.0 cm thick at the edge
- r151i1_spoon (cutlery): edge, marginal: 5.1 cm from the edge: slide it 6.9 cm out first (more than 3 cm: long slide); 0.8 cm thick at the edge
- r171i1_glass (dish): rim_pinch, yes: wall 5 mm at the rim (1.0 cm across the 2.9 cm pad band: wall + the rim's curve), jaws open 2.0 cm, 2.5 cm of pad on it, 3.8 cm clear inside behind the inner jaw
- r173i1_tumbler (dish): side, marginal: section 7.2 cm across at 4.1 cm above the support (pad middle); under 4.5 mm to spare a side; side grasp at floor level: hand level a few cm above the floor in the deep squat (not measured)
- r177i1_bowl (dish): rim_pinch, yes: wall 10 mm at the rim (2.0 cm across the 2.9 cm pad band: wall + the rim's curve), jaws open 3.0 cm, 1.5 cm of pad on it, 5.7 cm clear inside behind the inner jaw
- r179i1_toy_pouch (bag): side, marginal: section 7.8 cm across at 16.1 cm above the support (pad middle); under 4.5 mm to spare a side
- r192i1_ball (toy): surface_pinch, yes: 6.0 cm high: fingertips at the support, 2.9 cm of pad on it
- r193i1_toy_piece (container): surface_pinch, yes: 3.1 cm high: fingertips at the support, 2.9 cm of pad on it
- r193i2_toy_piece (container): surface_pinch, yes: 3.1 cm high: fingertips at the support, 2.9 cm of pad on it
- r193i3_toy_piece (container): surface_pinch, yes: 3.1 cm high: fingertips at the support, 2.9 cm of pad on it
- r193i4_toy_piece (container): surface_pinch, yes: 3.1 cm high: fingertips at the support, 2.9 cm of pad on it
- r195i1_paper (paper): surface_pinch, marginal: 3.0 cm high: fingertips at the support, 2.8 cm of pad on it; 7.7 cm across: under 4.5 mm to spare a side
- r195i3_paper (paper): surface_pinch, marginal: 3.0 cm high: fingertips at the support, 2.8 cm of pad on it; 7.7 cm across: under 4.5 mm to spare a side
- r196i1_plastic_bag (paper): surface_pinch, marginal: 1.4 cm high: fingertips at the support, 1.0 cm of pad on it
- r197i1_cup (dish): surface_pinch, yes: 6.0 cm high: fingertips at the support, 2.9 cm of pad on it
- r63i1_glass (dish): side, marginal: section 7.8 cm across at 6.1 cm above the support (pad middle); under 4.5 mm to spare a side
- r83i1_sponges (package): side, yes: section 6.4 cm across at 5.1 cm above the support (pad middle)
- r87i1_wrapper (paper): edge, marginal: 8.1 cm from the edge: slide it 9.9 cm out first (more than 3 cm: long slide); 3.7 cm thick at the edge
- r89i1_salad_bowl (dish): edge, marginal: 5.0 cm from the edge: slide it 6.8 cm out first (more than 3 cm: long slide); 3.4 cm thick at the edge; held at its edge the weight turns it 0.98 N m (pads resist about 0.17 N m at 6 N): it will swing down to hang from the grip, or use two hands; 0.90 kg: heavy for pad friction alone (measured squeeze 6 N a pad)
- r90i1_plate (dish): edge, marginal: 20.5 cm from the edge: slide it 22.3 cm out first (more than 3 cm: long slide); 1.3 cm thick at the edge; held at its edge the weight turns it 0.59 N m (pads resist about 0.17 N m at 6 N): it will swing down to hang from the grip, or use two hands
- r91i1_tan_plate (dish): edge, yes: 1.0 cm from the edge: slide it 2.8 cm out first; 1.3 cm thick at the edge; held at its edge the weight turns it 0.65 N m (pads resist about 0.17 N m at 6 N): it will swing down to hang from the grip, or use two hands
- r92i1_pink_container (container): side, yes: section 6.3 cm across at 4.1 cm above the support (pad middle)

## What remains impossible with a two-jaw gripper, and why
- r108i1_scissors (tool, floor): too thin: 0.9 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r146i1_bowl (dish, r145i1_lift_top): too wide: narrowest silhouette 20 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take; rim pinch: open only 1.2 cm deep (rim inner radius 8.9 cm, 8.0 cm high): filled to near the rim (contents in the mesh): kept solid
- r156i1_clementines (food, r143i1_sofa): too wide: narrowest silhouette 20 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take
- r176i1_cap (clothing, r2i1_sill): too wide: narrowest silhouette 19 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take
- r69i1_scrap (paper, floor): too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i2_scrap (paper, floor): too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i3_scrap (paper, floor): too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i4_scrap (paper, floor): too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
In short: things under 1 cm thick lying flat on the floor (paper scraps, scissors) give two vertical pads nothing to close on, and the floor has no edge to slide them to; things wider than 7.9 cm everywhere with no rim, flange or edge (the clementine net, the cap, the filled bowl) have no section the jaws span. A suction cup, a fingernail-like scoop or a wider hand would be needed.

## The sink and the dishwasher
- The pack's sink r27i1 has NO collider (0 collision pieces) and the countertop's collider has a hole over it: a dish let go over the basin falls through to the corner cabinet's bottom panel (0.12 m). room_patch.json `extras_add` holds a fixed, invisible 5-box basin (floor 0.668-0.68 m, walls to 0.88 m, turned 45 deg like the basin) for OUR merged model.
- The OPTIONAL step `close_dishwasher` (push both racks in, lift the door; door / drawer skill NOT built; ASSUMED 60 s) comes before the first sink trip. Where the robot would stand for it (today's floor, dishwasher open):
  - top rack front (pulled out), 0.46-0.63 m: stand at [3.5, 1.5], hand 0.26 m away: marginal (nearest standing place is 0.26 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without))
  - bottom rack front (pulled out), 0.15-0.31 m: stand at [3.5, 1.55], hand 0.26 m away: marginal (the pelvis can stand 0.26 m from it; low shelf: deep squat and a level reach into the cubby)
  - door's free edge (open, lying), 0.06-0.13 m: stand at [3.5, 1.15], hand 0.25 m away: marginal (the pelvis can stand 0.25 m from it; low shelf: deep squat and a level reach into the cubby)
- Sink stance (nearest standing place to a point 6 cm inside the basin), by geometry, not verified:
  - dishwasher closed, feet may step on the paper scraps (the plan): stand at [4.45, 1.35], 0.56 m to the basin: marginal
  - dishwasher closed, feet kept off the paper scraps: stand at [4.45, 1.35], 0.56 m to the basin: marginal
  - dishwasher closed, furniture as axis-aligned boxes (as the room builder makes them): stand at [4.45, 1.35], 0.56 m to the basin: marginal
  - dishwasher closed, fixed pieces under 15 cm high (the corner cabinet's 12 cm bottom panel, sticking out 25 cm in front of its diagonal face) kept only 16 cm from the feet instead of 28 cm from the pelvis: stand at [4.3, 1.6], 0.49 m to the basin: yes
  - dishwasher open (as the pack is), feet may step on the scraps: stand at [3.5, 1.55], 1.16 m to the basin: no
  - dishwasher open, feet kept off the scraps (v1's condition): stand at [3.5, 1.55], 1.16 m to the basin: no
- The plan uses: dishwasher closed; the feet may step on the 0.5 cm paper scraps r69i1_scrap, r69i2_scrap, r69i3_scrap, r69i4_scrap (no grasp takes them; ASSUMED safe, like the cords and mats).

## Reach: assumed limits, and the hook for the measured map
- MEASURED reach map in use: C:\Users\raresense\sim_home\apartment\reach\planner_reach_rows.json (levels: 0.55 m: 0.00 / 0.43 m, 0.78 m: 0.48 / 0.50 m, 0.80 m: 0.39 / 0.43 m, 0.95 m: 0.55 / 0.58 m); heights it does not cover use the ASSUMED limits.
- Hook: `measured_reach_map()` reads the newest existing JSON whose name contains 'reach' named in PROGRESS_CLOTH.md (rows z, x, y, err_xy, err_z, lean as scripts\home\live\s10_reach_probe.py writes them; reached = err_xy <= 1 cm and |err_z| <= 1.5 cm). Re-run this script after it appears.
- Sensitivity, reach 0.45 / 0.6 m, dishwasher closed: 50 planned (2026-11-18 23:53).
- Sensitivity, reach 0.34 / 0.5 m, dishwasher open: 28 planned (2026-11-18 23:53).
- Sensitivity, reach 0.45 / 0.6 m, dishwasher open: 28 planned (2026-11-18 23:54).

## What a different hand would add (Unitree Dex3-1, coarse, geometry only)
Using the same object geometry, a three-finger Dex3-1 (thumb + two fingers; widest thumb-to-finger gap 14.3 cm, measured on the Menagerie G1-with-hands model) would make **0 more of the 69 mess things graspable** (none): things up to about 13 cm across that no jaw section, rim or edge serves. It would also turn 10 marginal two-jaw grasps into comfortable ones (tight 7.7-7.8 cm fits, hand pitched down, things that swing from a rim or edge grip: r63i1_glass, r105i2_shoe, r125i2_flat, r130i1_light_saber, r173i1_tumbler, r179i1_toy_pouch, r191i1_toy_vehicle, r195i1_paper, r195i2_paper, r195i3_paper). It would not help the 8 that stay impossible (r108i1_scissors, r146i1_bowl, r156i1_clementines, r176i1_cap, r69i1_scrap, r69i2_scrap, r69i3_scrap, r69i4_scrap): flat things under 1 cm still need a nail, a scoop or suction, and the rest are wider than its span or too heavy for the arm. This is a COARSE estimate from object sizes and the hand's span (no finger kinematics, contacts or reach were checked); reach and the destination limits would still apply, so it is not a count of extra planned items.

## Skipped mess, and why
- r107i1_umbrella (umbrella, to r110i1_console): its destination r110i1_console cannot be reached: nearest standing place is 0.64 m from it (MEASURED (planner_reach_rows.json, pad height 0.80 m) reach 0.43 m at most) (now, before anything is cleared: 1.26 m)
- r108i1_scissors (tool, to r110i1_console): not graspable: too thin: 0.9 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r122i1_croc (shoe, to r119i1_mat): NO free place left on the mat for this pair (lamp base and the other pairs fill it): set beside the mat
- r123i1_slipper (shoe, to r119i1_mat): NO free place left on the mat for this pair (lamp base and the other pairs fill it): set beside the mat
- r146i1_bowl (dish, to r27i1_sink): not graspable: too wide: narrowest silhouette 20 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take; rim pinch: open only 1.2 cm deep (rim inner radius 8.9 cm, 8.0 cm high): filled to near the rim (contents in the mesh): kept solid
- r152i1_sippy_cup (container, to r27i1_sink): not reachable: nearest standing place is 0.61 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most)
- r156i1_clementines (food, to r35i1_top): not graspable: too wide: narrowest silhouette 20 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take
- r157i1_paper (paper, to rubbish_bin): never became reachable in the route
- r157i2_paper (paper, to rubbish_bin): never became reachable in the route
- r174i1_plush (toy, to r186i1_basket): not reachable: no pick stance even with every movable thing gone: blocked by brick_wall, r169i1_two_tier_table, r175i1_cardboard_box
- r176i1_cap (clothing, to r110i1_console): not graspable: too wide: narrowest silhouette 19 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take
- r182i1_bottle (container, to r35i1_top): not reachable: nearest standing place is 0.84 m from it (MEASURED (planner_reach_rows.json, pad height 0.95 m) reach 0.58 m at most)
- r183i1_cup (dish, to r27i1_sink): not reachable: nearest standing place is 0.84 m from it (MEASURED (planner_reach_rows.json, pad height 0.80 m) reach 0.43 m at most)
- r195i2_paper (paper, to rubbish_bin): not reachable: no pick stance even with every movable thing gone: blocked by r143i1_sofa, r145i1_base
- r69i1_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i2_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i3_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i4_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r71i1_lysol (container, to r94i1_tray_table): not reachable: nearest standing place is 1.08 m from it (ASSUMED reach 0.50 m at most) (hand comes in from its side grasp's side)
- r78i1_kids_bottle (container, to r27i1_sink): not reachable: nearest standing place is 0.82 m from it (ASSUMED reach 0.50 m at most)
- r83i2_sponges (package, to r94i1_tray_table): NO free place of 22 x 8 cm left on r94i1_tray_table: something there has to be moved together first

Mess left on purpose (no destination the robot can serve):
- r100i1_towel: towel thrown over the stool; a rigid drape shape in our model (not cloth), 53 cm wide: nothing the jaws can take. If it were made cloth it would go to the hamper
- r106i1_umbrella: large open umbrella on the floor (89 x 69 cm): too big to carry between the furniture; left (TIDY_PLAN)
- r154i1_stick: 60 cm stick on the coffee table: 1 cm thin, nothing for the pads; left
- r161i1_hair_dryer: hair dryer on the TV cabinet: belongs in a bathroom or a drawer; the scene has no bathroom and drawers are frozen: left
- r165i1_coat: coat thrown over the armchair; belongs on the hook rack r97 (1.3-2.4 m up, out of reach). It is a rigid drape shape in our model (not one of the 7 cloth garments), 1.1 kg
- r175i1_cardboard_box: cardboard box by the armchair: 28 x 24 x 25 cm, bigger than the bin's opening; a box that stays (TIDY_PLAN)
- r194i1_strap: strap on the rug: 1 cm thin, nothing for the pads to bite (TIDY_PLAN leaves cords and straps in phase 1)
- r198i1_cord: cord on the floor: 1 cm thin, left (TIDY_PLAN)
- r198i2_cord: cord on the floor: 1 cm thin, left (TIDY_PLAN)
- r70i1_tote: tote bag on the kitchen island: 41 cm wide, 0.9 kg, no part the jaws can take from the side at 0.91 m: left
- r74i1_milk_jug: belongs in the fridge: needs the fridge door opened (doors are frozen in our model, no door skill) and 1.2 kg is marginal for the jaws
- r77i1_iron: iron on the kitchen island: no better open place in the scene (cabinets need doors), 1.3 kg: left
- r86i1_cables: cable bundle on the island: 1.4 cm flat, no destination without a drawer: left

Things that are planned but only reachable after a neighbour is gone (the route respects this):
- r105i1_shoe: clear r105i2_shoe first
- r105i2_shoe: clear r105i1_shoe first
- r117i1_blanket: clear r116i1_coat_pile first
- r120i1_duck: clear r117i1_blanket, r116i1_coat_pile first
- r149i1_pouch: clear r155i1_kids_bottle first
- r189i1_santa_hat: clear r191i1_toy_vehicle first
- r190i1_stocking: clear r191i1_toy_vehicle first
- r192i1_ball: clear r193i3_toy_piece, r193i1_toy_piece, r193i4_toy_piece, r189i1_santa_hat, r190i1_stocking, r193i2_toy_piece, r195i1_paper first
- r193i1_toy_piece: clear r193i3_toy_piece, r192i1_ball, r190i1_stocking, r189i1_santa_hat, r193i4_toy_piece, r193i2_toy_piece, r195i1_paper first
- r193i2_toy_piece: clear r188i1_dollhouse first
- r193i3_toy_piece: clear r189i1_santa_hat, r191i1_toy_vehicle first
- r193i4_toy_piece: clear r189i1_santa_hat, r193i2_toy_piece, r188i1_dollhouse first
- r195i1_paper: clear r195i2_paper, r192i1_ball, r193i1_toy_piece, r193i4_toy_piece, r193i3_toy_piece first
- r63i1_glass: clear r68i1_rag first
- r87i1_wrapper: clear r117i1_blanket first
- r92i1_pink_container: clear r68i1_rag first
- r93i1_nugget: clear r68i1_rag first

Planned with a marginal grasp or reach (expect failures here first):
- r105i2_shoe: grasp: section 11 cm off the middle: it can swing or tip in the jaws
- r125i2_flat: grasp: section 9 cm off the middle: it can swing or tip in the jaws
- r130i1_light_saber: grasp: section 8 cm off the middle: it can swing or tip in the jaws
- r138i1_cup: reach: nearest standing place is 0.37 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r139i1_toy_car: reach: nearest standing place is 0.41 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r147i1_purple_container: reach: nearest standing place is 0.37 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r148i1_pink_lid: grasp: 6.5 cm from the edge: slide it 8.3 cm out first (more than 3 cm: long slide); 2.4 cm thick at the edge; reach: now: nearest standing place is 0.81 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most). With the movable things gone: nearest standing place is 0.21 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without) (hand comes in from its edge grasp's side)
- r149i1_pouch: grasp: 24.7 cm from the edge: slide it 26.5 cm out first (more than 3 cm: long slide); 2.0 cm thick at the edge; reach: now: nearest standing place is 0.93 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most). With r155i1_kids_bottle gone: nearest standing place is 0.22 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without) (hand comes in from its edge grasp's side)
- r151i1_spoon: grasp: 5.1 cm from the edge: slide it 6.9 cm out first (more than 3 cm: long slide); 0.8 cm thick at the edge; reach: now: nearest standing place is 1.21 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most). With the movable things gone: nearest standing place is 0.34 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without) (hand comes in from its edge grasp's side)
- r155i1_kids_bottle: reach: now: nearest standing place is 0.86 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most). With the movable things gone: nearest standing place is 0.32 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r158i1_tissue: reach: now: nearest standing place is 0.66 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most). With the movable things gone: nearest standing place is 0.36 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r171i1_glass: reach: nearest standing place is 0.32 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r173i1_tumbler: grasp: section 7.2 cm across at 4.1 cm above the support (pad middle); under 4.5 mm to spare a side; side grasp at floor level: hand level a few cm above the floor in the deep squat (not measured)
- r179i1_toy_pouch: grasp: section 7.8 cm across at 16.1 cm above the support (pad middle); under 4.5 mm to spare a side
- r188i1_dollhouse: grasp: section 8 cm off the middle: it can swing or tip in the jaws
- r191i1_toy_vehicle: grasp: 7.3 cm across: under 4.5 mm to spare a side (the floor agent's search rejects it)
- r195i1_paper: grasp: 3.0 cm high: fingertips at the support, 2.8 cm of pad on it; 7.7 cm across: under 4.5 mm to spare a side
- r195i3_paper: grasp: 3.0 cm high: fingertips at the support, 2.8 cm of pad on it; 7.7 cm across: under 4.5 mm to spare a side
- r196i1_plastic_bag: grasp: 1.4 cm high: fingertips at the support, 1.0 cm of pad on it
- r63i1_glass: grasp: section 7.8 cm across at 6.1 cm above the support (pad middle); under 4.5 mm to spare a side
- r81i1_glass_spoon: grasp: fingers down with its top 1.10 m up: the wrist about 1.20 m (ASSUMED limit 1.05 m); reach: nearest standing place is 0.55 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.95 m) limit 0.55 m without); grasp height about 1.09 m: at or above the shoulder
- r87i1_wrapper: grasp: 8.1 cm from the edge: slide it 9.9 cm out first (more than 3 cm: long slide); 3.7 cm thick at the edge
- r89i1_salad_bowl: grasp: 5.0 cm from the edge: slide it 6.8 cm out first (more than 3 cm: long slide); 3.4 cm thick at the edge; held at its edge the weight turns it 0.98 N m (pads resist about 0.17 N m at 6 N): it will swing down to hang from the grip, or use two hands; 0.90 kg: heavy for pad friction alone (measured squeeze 6 N a pad)
- r90i1_plate: grasp: 20.5 cm from the edge: slide it 22.3 cm out first (more than 3 cm: long slide); 1.3 cm thick at the edge; held at its edge the weight turns it 0.59 N m (pads resist about 0.17 N m at 6 N): it will swing down to hang from the grip, or use two hands

## Route (one episode)
Chosen: toy basket carried to the rug toys: no; bin carried to the living room: no. Whole-route time with the stated speeds for the four ways: basket carried, bin carried: 59 min; basket carried, bin stays: 57 min; basket stays, bin carried: 58 min; basket stays, bin stays: 56 min.
Toy basket spot on the rug (scene): (-2.90, -1.95). Bin spot in the living room (scene): (-3.75, -0.05).

| # | Step (runner form) | What | Items | Walk empty / carrying m | s (stated speeds) | Runs today? |
|---|---|---|---|---|---|---|
| 1 | `tidy_all` | east: rubbish to the bin (bin at home) | 1 | 0.37 / 1.91 | 35 | no: runner form exists; drop_in into the bin ran in the practice room only |
| 2 | `garments` | entry, kitchen, hall: garments to the hamper (big ones one per trip, two hands) | 5 | 47.86 / 53.8 | 640 | no: the CLOTH agent's runner form (E:/urc_cloth/scripts/home/cloth_episode.py); one merged runner for cloth + rigid in the same episode does not exist yet |
| 3 | `tidy_all` | east: shoes to the doormat in pairs | 3 | 20.57 / 11.88 | 196 | no: runner form exists; put_down on the flat mat with a target spot per shoe is NOT run yet (pair spots need a new option) |
| 4 | `close_dishwasher` | OPTIONAL: push both dishwasher racks in, lift the door shut (frees the floor in front of the sink) | 1 | 6.22 / 0.0 | 74 | no: NEW: door / drawer skill (not built); the room file must leave these 3 joints free (doors are frozen today) |
| 5 | `tidy_surface` | kitchen: used dishes from the island and the counter to the sink | 6 | 3.07 / 5.55 | 218 | no: NEW step type: pick from furniture (surface_pick) + drop_in_sink (lower into the basin); floor and cloth things in the list go through their own skills |
| 6 | `tidy_surface` | kitchen: cleaning things from the island to the tray table | 1 | 2.45 / 0.72 | 41 | no: NEW step type: pick from furniture (surface_pick) + place_on (set on a table); floor and cloth things in the list go through their own skills |
| 7 | `tidy_surface` | crossing west: the east half's toys ride along to the toy basket at its home | 2 | 3.15 / 17.84 | 166 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower into a low basket); floor and cloth things in the list go through their own skills |
| 8 | `tidy_surface` | toy corner: toys near the basket's home into it | 3 | 3.35 / 7.88 | 143 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower into a low basket); floor and cloth things in the list go through their own skills |
| 9 | `tidy_surface` | rug and side table: toys to the basket at its home (two per trip) | 8 | 10.08 / 29.16 | 426 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower into a low basket); floor and cloth things in the list go through their own skills |
| 10 | `tidy_all` | rug: the two big toys to the toy corner (one per trip) | 2 | 7.51 / 7.51 | 114 | no: runner form exists; needs a per-object destination spot on the floor (new option) |
| 11 | `garments` | rug: remaining garments to the hamper | 1 | 2.44 / 1.25 | 50 | no: the CLOTH agent's runner form (E:/urc_cloth/scripts/home/cloth_episode.py); one merged runner for cloth + rigid in the same episode does not exist yet |
| 12 | `tidy_surface` | living room: rubbish to the bin at its home (two per trip) | 3 | 11.26 / 20.25 | 214 | no: NEW step type: pick from furniture (surface_pick) + drop_in; floor and cloth things in the list go through their own skills |
| 13 | `tidy_all` | living room: the pair of flats to the doormat | 2 | 6.27 / 9.68 | 124 | no: runner form exists; put_down on the flat mat with a target spot per shoe is NOT run yet (pair spots need a new option) |
| 14 | `tidy_surface` | living room: used dishes to the sink (two per trip, the long way) | 9 | 46.9 / 70.52 | 758 | no: NEW step type: pick from furniture (surface_pick) + drop_in_sink (lower into the basin); floor and cloth things in the list go through their own skills |
| 15 | `tidy_surface` | left-overs that waited for a neighbour: to rubbish_bin | 2 | 16.95 / 13.95 | 171 | no: NEW step type: pick from furniture (surface_pick) + drop_in; floor and cloth things in the list go through their own skills |

The exact step list (names in order, pairs adjacent) is in `route_steps.json`; per-object trips and seconds are in `full_plan.json`.
Step forms: `tidy_all` is the floor agent's (E:\urc_home\scripts\home\episode.py); `garments` is the cloth agent's (E:\urc_cloth\scripts\home\cloth_episode.py). NEW step types this plan needs: `carry` (a container, two hands), `tidy_surface` (pick from furniture; place on a table, a counter, into the sink). Also needed in the runner: one episode that mixes rigid and cloth steps, a destination PER OBJECT with a target spot (the room file maps a class to one place; `room_patch.json` holds the per-object table), and two per trip across neighbouring destinations.

## Time for the whole apartment
- Things moved: 48 in 32 trips, + 0 container carries. Planned walking: 188 m empty-handed, 252 m carrying.
- Today, with the stated speeds (0.45 m/s empty, 0.18 m/s carrying, pick 16 s, put-down 12 s) and the robot walking exactly the planned legs: **56 min** (70 s a thing).
- Today, at the end-to-end rates measured in run 1118_204943 (B2: 4.2 m of legs in 36 s empty, 7 m in 111 s carrying, pick 18 s, put-down 20 s): **2.0 h** (153 s a thing). This is what the code as committed would do, if nothing failed.
- At the target of 20-30 s a thing (container carries at 0.45 m/s on top): **17 min to 25 min**.
- Not in these numbers: failed grasps and second tries, falls, the scene settling at the start, compute time (the CPU path ran about 0.6x real time with recording).

## Top risks
- Most of the plan needs skills that do not exist: of the planned things only the floor toys into the toy basket use skills proven in a clean episode (one toy piece, 176 s). Surface picks, placing on tables / counters / into the sink, the container carry and the cloth pick are not built or not proven.
- 25 planned things rely on a NEW grasp type (side, surface pinch, rim pinch, edge) that exists only as geometry; rim pinches also need the hollow colliders applied, edge grasps a slide skill when the thing does not overhang.
- The sink has no collider in the pack: until SINK_COLLIDER (room_patch.json extras_add) is in the room, every dish 'put in the sink' falls into the cabinet below.
- The living room is far from the kitchen: used dishes travel about 9-10 m each, two per trip. At today's carrying speed this is the largest block of time. A dish caddy (a movable box carried once) would cut it but needs two-hand carrying of about 2.5 kg, over the 1.5 kg limit; not planned.
- Reach onto furniture is ASSUMED (0.45 m from the pelvis, 0.60 m with a lean); no reach map exists for standing or half-squat picks at 0.45-0.95 m. Things in the middle of the island, at the back of the counter and on the window sills behind the armchair and the gold table depend on it.
- The sink is in the corner behind the open dishwasher door and racks; with the optional closing step: marginal: nearest standing place is 0.56 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.95 m) limit 0.55 m without) (to the nearest point 6 cm inside the basin; dishwasher closed by the optional step). Four paper scraps lie on the floor exactly there and cannot be picked up (0.5 cm thin): the plan lets the feet step on them.
- The doormat is half covered by the floor lamp's base; only the free part is used for the shoes: r124i1_sandal: (2.35, -1.97); r105i1_shoe: (2.28, -1.72); r105i2_shoe: (2.40, -1.72); r125i1_flat: (2.05, -1.72); r125i2_flat: (2.16, -1.72); r122i1_croc: NO SPOT; r123i1_slipper: NO SPOT.
- The toy basket is small (33 x 27 x 12 cm, about 10 litres) and already holds a plush: 13 more toys are planned into it. It will be heaped; overflow goes into the megabloks bag beside it (TIDY_PLAN). Carrying a heaped basket can spill.
- Walking distances are planned on the floor as it is AFTER the mess is gone; early trips are a little longer. Things moved to their places (shoes on the mat, a basket on the rug) are not put back into the map as new obstacles.
- Garments: the cloth pick is assumed to work for all seven; the three big ones (jacket, coat pile 1.4 kg, blanket) are assumed to need both hands and one trip each. The coat pile is the first thing that must go: it covers the mat and blocks the console.
- Heavy or off-centre grasps are marked marginal (pad friction alone, 6 N a pad measured): clementines 1.0 kg, salad bowl 0.9 kg, dollhouse 0.8 kg, lysol 0.75 kg, light saber held off its middle.
- A one-hour-plus episode with 198 loose bodies is beyond what the simulator has run: the full loose set ran under 0.02x real time on the GPU path; the room file must keep only the planned things loose (`room_patch.json`).

## Assumptions (all of them)
- Source of truth for names, classes, masses, positions and sizes: D:\apartment_real\mujoco\unzipped (scene_spec.json, environment.xml), read only. Grasp sections and footprints come from the collision meshes at their start poses (the light saber and the santa hat move a little when the scene settles).
- Grasp (v2): five types from grasps_v2.json (README_GRASPS.md says what each assumes): top_down (the floor agent's search, unchanged, plus a tight 7.8 cm fallback marked marginal), side, surface_pinch, rim_pinch (with the hollow colliders), edge. Preference when several work: yes before marginal, then top_down, side, surface pinch, rim pinch, edge (floor: top_down, surface pinch, side, rim pinch); the reach step may pick another usable type when the preferred one has no standing place. Fingers-down grasps on furniture are marginal when the thing's top is over 0.95 m. The jaws open 7.9 cm between the pad faces in the model (the brief says 8.2 cm).
- Side and edge grasps on furniture: the robot must stand on the side the hand comes from (within 60 deg of the approach); an edge grasp's slide must be clear of things that stay; things in the way that are moved anyway make it 'after clearing'.
- Mass: over 1.5 kg not carried; 0.8-1.5 kg marginal.
- Garments (7) are cloth and count as graspable by a pinch; their rigid drape shapes are used only as footprints.
- Floor reach: a pick stance as skills.stance_for builds it (thing 0.17 m ahead and 0.27 m to the side of the standing pelvis, pelvis 0.28 m from furniture and 0.16 m from small things, knees 12 cm clear of anything over 15 cm, feet 4 cm clear of floor things, 12 headings, both hands), checked on a 5 cm grid. Cords, the strap and the mats are walked over, as in the floor agent's room file.
- Furniture reach: the pelvis may stand 0.22 m from furniture; a grasp point within 0.34 m of such a place counts as reachable, within 0.5 m marginal. A MEASURED map is used where it has the height.
- Dishes on the coffee table, side table, two-tier table, sills, island and the right counter are taken as used and go to the sink; dishes in the open dishwasher racks, at the sink and beside the dish basket are taken as in place. The sink is assumed to take 16 small dishes.
- Flat papers on the sofa and the empty pouch are rubbish (TIDY_PLAN). Snack bags, the juice box, the chips can and the paper bag in the kitchen are food or storage, not rubbish.
- Books are already stacked and stay; the remote stays on the two-tier table; keyboard, mouse and notebook stay on the window sill (deviation from TIDY_PLAN's 'books and remote on the coffee table': nothing is gained by moving them and flat books cannot be grasped).
- Santa hat to the hamper and stocking to the toy basket, as TIDY_PLAN classes them.
- Cleaning things from the island go to the tray table beside the mop; the cap, scissors and small umbrella go to the console table (my choice of place; TIDY_PLAN names the console for scissors and umbrella).
- Doors, drawers and lids stay as they are (frozen in our model): nothing is put into the fridge, cabinets, drawers, the ottoman or the lift-top table. The one exception is the OPTIONAL close_dishwasher step (racks in, door up), which needs those 3 joints left free and a door / drawer skill; the dishes in its racks go in with them.
- Target spots: every planned thing has one (room_patch.json target_spots_scene / _world): shoes in pairs on the mat, free places on tables, slots in the toy basket (layered when full) and on the sink's basin floor (nearest the stance first), and a release point over the bin and the hamper. If the toy basket is carried to the rug, its slots move with it.
- Times: floor pick 16 s and put-down 12 s (run B) or 18 s and 20 s (run B2) are measured; cloth pick 30 s (45 s two hands), surface pick 20 s, drop into bin / hamper 8 s, into the sink 10 s, place on a table 12 s, container pick-up 25 s and set-down 15 s are GUESSES. A second thing in a trip costs its own pick and put. A trip's time is shared equally by its things.
- Route: the zone order is fixed by hand (east half first because the robot starts there and the coat pile must leave the mat first; then the crossing west with the east toys; the living room; last the things that leave the living room). Inside a block the nearest available thing is next and the second hand takes a thing within 3 m going to the same place (the runner's own rule). The four ways (basket carried or not, bin carried or not) are all computed and the fastest by the stated speeds is taken. Not a proven optimum.
- Things moved in one trip with two hands (big garments, anything over 1 kg) travel alone.

## Files
- `C:\Users\raresense\sim_home\apartment\full_plan\full_plan.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\route_steps.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\room_patch.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\FULL_PLAN.md`
- `C:\Users\raresense\sim_home\apartment\full_plan\make_full_plan.py`
- `C:\Users\raresense\sim_home\apartment\full_plan\grasps_v2.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\grasp_types.py`
- `C:\Users\raresense\sim_home\apartment\full_plan\make_grasps_v2.py`
- `C:\Users\raresense\sim_home\apartment\full_plan\README_GRASPS.md`
- `C:\Users\raresense\sim_home\apartment\full_plan\hollow_colliders.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\make_hollow_colliders.py`
- `C:\Users\raresense\sim_home\apartment\full_plan\hollow_colliders_qc.png`
- `C:\Users\raresense\sim_home\apartment\full_plan\reach_sensitivity.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\nav_snapshot.py`
- `C:\Users\raresense\sim_home\apartment\full_plan\grasp_geom_snapshot.py`
- `C:\Users\raresense\sim_home\apartment\full_plan\FULL_PLAN_v1.md`
- `C:\Users\raresense\sim_home\apartment\full_plan\full_plan_v1.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\route_steps_v1.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\room_patch_v1.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\make_full_plan_v1.py`
