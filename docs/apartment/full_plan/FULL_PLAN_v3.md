# Apartment 1122: full tidy plan for one continuous episode

Generated 2026-11-19 10:41 by `C:/Users/raresense/sim_home/apartment/full_plan/make_full_plan_v3.py` (rerun: `py -3.12` on that file, about 126 s).
**Nothing in this file is a simulation result.** Every reach and grasp judgement is by geometry, not verified. Coordinates are the pack's scene frame; the episode's world frame is scene - (0.90, 0.45).

## v3 "looks clean" in short (v2 is kept as it was: FULL_PLAN.md, full_plan.json, route_steps.json, room_patch.json)
- **60 things are planned in ONE route** (v2: 48), out of 81 things counted as mess in v3 (v2: 69 + the big things, the towel, the coat, the strap, the stick and kitchen things). 22 loose things stay NOT clean at the end (list at the end of this section, each with the reason). Every method and reach judgement is by geometry, not verified.
- The big things go FIRST (they stand in walking routes): r127i1_scooter, r126i1_scooter, r106i1_umbrella; before them only the small things lying where the scooters will be parked (r123i1_slipper, r124i1_sandal).
- New step types (runner form, route_steps_v3.json): `["carry2", name, {to_scene, to_world, grip, take_stance_scene, set_down, ...}]`, `["drag", name, {to_scene, grip_point_scene, ...}]`, `["close_door", name, {joint, q_closed, push_point_scene, push_dir, stand_scene}]`; the floor / surface / cloth things use the existing `tidy_all` / `tidy_surface` / `garments` with per-object spots (room_patch_v3.json).
- Time: **59 min** with the stated speeds, **1.9 h** at run B2's end-to-end rates, 23 min to 33 min at the 20-30 s target (big things: carry2 take 30 s + set 20 s, drag 25 + 10 s, close a door 60 s: ASSUMED).

### The big floor things: method, forces at the hand, place (by geometry, not verified)
Hold limits used (urc.tasks.home.hold.Hold defaults): 40 N force, 4.0 N m torque; past them the held thing is pulled out of the hold. Friction: MuJoCo mixes the larger of the two geoms' values (scooters 0.8 on floor 0.6 / rug 0.85). The pack's bodies are single rigid bodies with no wheel joints: they slide, they do not roll; their centre of mass is the middle of their box.

| Thing | kg | recommended | hand load | upright drag | tilted drag | place (scene x, y, yaw) | against | extra walking |
|---|---|---|---|---|---|---|---|---|
| r127i1_scooter | 2.7 | carry2 (both hands on the handlebar) | 13.2 N + 2.28 N m a hand | no: needs 9.3 N m | marginal: 23.3 N one hand | (0.85, -2.05, -95.5 deg) | r20i1_baseboard, wall_grey_shell | 0.0 m |
| r126i1_scooter | 3.0 | carry2 (both hands on the handlebar) | 14.7 N + 2.87 N m a hand | no: needs 13.8 N m | marginal: 25.8 N one hand | (1.19, -2.07, -90.0 deg) | r20i1_baseboard, wall_grey_shell | 0.0 m |
| r106i1_umbrella | 0.45 | drag by the rim (far rim sliding) | 3.1 N | - | - | (-1.08, 1.81, -21.0 deg) | r20i1_baseboard, wall_grey_shell | 0.0 m |

- r127i1_scooter: carry2: the load is split evenly between the hands, nothing balances on a point, the hold limits are not reached (force and torque), it is the same take / stand / walk / set down pattern as the toy-basket carry that worked live (run 1118_232318); dragging upright is impossible by physics (9.3 N m needed at the hand), and the tilted drag puts 23 N on ONE hand at the side of the body with a roll the hold must stop. Place: parked upright, nose to r20i1_baseboard, wall_grey_shell, stem and handlebar out (0.50 m from it), in the vehicle corner by the toy bike. Take: standing take place free now; set-down stance {'stand_scene': [0.86, -1.52, -90], 'pelvis_to_stem_m': 0.36}
- r126i1_scooter: carry2: the load is split evenly between the hands, nothing balances on a point, the hold limits are not reached (force and torque), it is the same take / stand / walk / set down pattern as the toy-basket carry that worked live (run 1118_232318); dragging upright is impossible by physics (13.8 N m needed at the hand), and the tilted drag puts 26 N on ONE hand at the side of the body with a roll the hold must stop. Place: parked upright, nose to r20i1_baseboard, wall_grey_shell, stem and handlebar out (0.51 m from it), in the vehicle corner by the toy bike. Take: standing take place free now; set-down stance {'stand_scene': [1.19, -1.51, -90], 'pelvis_to_stem_m': 0.36}
- r106i1_umbrella: 2-3 N at the hand; the only way the jaws can hold it (the handle is not in the collider). Place: lying open (it cannot be closed), against r20i1_baseboard, wall_grey_shell; 7.05 m from the front door's opening, outside every door's swing; chosen: the least walking cost anywhere (no place by the entry blocks nothing); it adds 0.00 m of walking per key pair on average. Take: no stance now; one appears only when most of the neighbours are gone: r120i1_duck, r117i1_blanket
- The open umbrella by the entry: the best place there ([np.float64(3.6), np.float64(-0.45)]) adds 0.508 m of walking per key pair (it narrows the only way past the stroller); the chosen place adds 0.0 m. Chosen: the least walking cost anywhere (no place by the entry blocks nothing). Its collider is a flat 3 cm slab (the dome is drawn only), so it cannot be stood up or closed; there is no handle in physics.
- The toy bike r128i1 already stands along the hall wall beside the robot vacuum: it is the west end of the vehicle corner and is not moved.
- r107i1_umbrella: moved: to by the entry (floor) at (4.10, -2.12); lying along r20i1_baseboard, wall_grey_shell, 0.56 m from the front door's opening; method: top_down grasp (yes), put_down (set on the floor)
- r175i1_cardboard_box: moved: to against the wall by the two-tier table (floor) at (-4.35, 2.01); square against r20i1_baseboard, wall_grey_shell, 0.16 m from where it stands; method: side grasp (marginal), put_down (set on the floor)
- r70i1_tote: moved: to floor beside the standing bags (by the entry) at (5.04, -0.92); standing beside r104i1_grocery_bag, against r20i1_baseboard, wall_grey_shell; method: top_down grasp (marginal), put_down (lower the bag hanging from its handles until it stands, open)
- Two-hand carry for boxes: the cardboard box is 0.6 kg with a top ridge the jaws can take (top-down section 4.6-5.2 cm): one hand + the contact-verified hold; a push (0.6 x 5.9 = 3.5 N, below 0.23 m or it tips) is the fallback.

### Soft things, cushions, cords and the strap
- r100i1_towel: moved: to r133i1_laundry_basket
- r165i1_coat: NOT tidied: not reachable: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most)
- r144i1_cushion: in place: sofa cushion upright against the sofa back: all three at the same height and yaw (0 deg, 0 deg tilt), evenly spaced 0.567 m: in place, not touched
- r144i2_cushion: in place: sofa cushion upright against the sofa back: all three at the same height and yaw (0 deg, 0 deg tilt), evenly spaced 0.567 m: in place, not touched
- r144i3_cushion: in place: sofa cushion upright against the sofa back: all three at the same height and yaw (0 deg, 0 deg tilt), evenly spaced 0.567 m: in place, not touched
- r198i1_cord: in place: the heater's power cord (one end at the heater r132, the other at the wall, by geometry): where a plugged-in cord belongs; left
- r198i2_cord: in place: a power cord plugged into the outlet r19i7 (one end 1 cm from it) running along the planter: where it belongs; left
- r194i1_strap: NOT tidied: not reachable: no pick stance even with every movable thing gone: blocked by r143i1_sofa, r145i1_base
- Cloth proposal (room_patch_v3.json cloth_new_proposed): as the 7 garments (structure.cloth): the towel one flat panel 53 x 49 cm (0.6 kg), the coat the jacket pattern at 52 x 65 cm (1.1 kg); they lie on furniture (stool r99i2 seat 0.61 m, armchair r164i1): lay() must drape them over it, not on the floor. The towel is in the first garments step (cloth pick from the stool's seat: NOT built); the coat's armchair is in the cut-off south-west corner.

### The kitchen: every thing on the island and the counters
| Thing | on | v3 | why / where |
|---|---|---|---|
| r37i1_blender | r26i1_countertop | in place | appliance standing where it is used: stays (r26i1_countertop) |
| r38i1_coffee_maker | r26i1_countertop | in place | appliance standing where it is used: stays (r26i1_countertop) |
| r39i1_cereal | r26i1_countertop | in place | kitchen / storage item where it is used: in place (r26i1_countertop) |
| r39i2_cereal | r26i1_countertop | in place | kitchen / storage item where it is used: in place (r26i1_countertop) |
| r40i1_tea_box | r26i1_countertop | in place | kitchen / storage item where it is used: in place (r26i1_countertop) |
| r41i1_bread | r26i1_countertop | in place | food on the kitchen counter / island: in place (r26i1_countertop) |
| r41i2_bread | r26i1_countertop | in place | food on the kitchen counter / island: in place (r26i1_countertop) |
| r42i1_dish_basket | r26i1_countertop | in place | dish basket on the counter: in place |
| r43i1_measuring_cup | r26i1_countertop | in place | beside the dish basket: in place |
| r44i1_mug | r26i1_countertop | in place | mug on the counter at the sink: already at the sink |
| r45i1_food_container | r26i1_countertop | in place | kitchen / storage item where it is used: in place (r26i1_countertop) |
| r46i1_spray_bottle | r26i1_countertop | in place | kitchen / storage item where it is used: in place (r26i1_countertop) |
| r47i1_squeeze_bottle | r26i1_countertop | in place | kitchen / storage item where it is used: in place (r26i1_countertop) |
| r48i1_spice_jar | r26i1_countertop | in place | kitchen / storage item where it is used: in place (r26i1_countertop) |
| r50i1_blue_box | r26i1_countertop | in place | kitchen / storage item where it is used: in place (r26i1_countertop) |
| r51i1_paper_bag | r26i1_countertop | in place | standing bag by the wall: stays (TIDY_PLAN) (r26i1_countertop) |
| r52i1_cutting_board | r26i1_countertop | in place | on the kitchen counter: in place (r26i1_countertop) |
| r56i1_olive_oil | r26i1_countertop_right | in place | kitchen / storage item where it is used: in place (r26i1_countertop_right) |
| r57i1_paper_towel | r26i1_countertop_right | in place | kitchen / storage item where it is used: in place (r26i1_countertop_right) |
| r58i1_air_fryer | r26i1_countertop_right | in place | appliance standing where it is used: stays (r26i1_countertop_right) |
| r59i1_pitcher | r26i1_countertop_right | in place | kitchen / storage item where it is used: in place (r26i1_countertop_right) |
| r60i1_vial | r26i1_countertop_right | in place | kitchen / storage item where it is used: in place (r26i1_countertop_right) |
| r61i1_green_tool | r26i1_countertop_right | in place | kitchen / storage item where it is used: in place (r26i1_countertop_right) |
| r62i1_snack_bag | r26i1_countertop_right | in place | snack on the kitchen counter / island: food, not rubbish: stays (r26i1_countertop_right) |
| r63i1_glass | r26i1_countertop_right | moved | to r27i1_sink |
| r54i1_pot | r29i1_range | in place | cookware on the range: in place (r29i1_range) |
| r55i1_skillet | r29i1_range | in place | cookware on the range: in place (r29i1_range) |
| r55i2_skillet | r29i1_range | in place | cookware on the range: in place (r29i1_range) |
| r70i1_tote | r35i1_top | moved | to floor beside the standing bags (by the entry) at (5.04, -0.92) |
| r71i1_lysol | r35i1_top | moved | to r94i1_tray_table at (2.46, 2.00) |
| r72i1_chips_can | r35i1_top | in place | kitchen / storage item where it is used: in place (r35i1_top) |
| r73i1_apples | r35i1_top | in place | food on the kitchen counter / island: in place (r35i1_top) |
| r74i1_milk_jug | r35i1_top | NOT tidied | OPTIONAL fridge round, not in the route: the fridge doors are frozen in our rooms and no door skill exists (the surface agent is building one for the dishwasher); with it: open r34i1_fresh_door, set the jug on the compartment floor, close the door.  |
| r75i1_bottle | r35i1_top | in place | kitchen / storage item where it is used: in place (r35i1_top) |
| r75i2_bottle | r35i1_top | in place | kitchen / storage item where it is used: in place (r35i1_top) |
| r76i1_cotton_vase | r35i1_top | in place | decor: stays (r35i1_top) |
| r77i1_iron | r35i1_top | NOT tidied | not reachable: nearest standing place is 0.78 m from it (ASSUMED reach 0.50 m at most) (hand comes in from its side grasp's side) |
| r78i1_kids_bottle | r35i1_top | moved | to r27i1_sink |
| r79i1_water_bottle | r35i1_top | in place | kitchen / storage item where it is used: in place (r35i1_top) |
| r80i1_orange_cap_bottle | r35i1_top | in place | kitchen / storage item where it is used: in place (r35i1_top) |
| r81i1_glass_spoon | r35i1_top | moved | to r27i1_sink |
| r82i1_juice_box | r35i1_top | in place | kitchen / storage item where it is used: in place (r35i1_top) |
| r83i1_sponges | r35i1_top | moved | to r94i1_tray_table at (2.40, 2.37) |
| r83i2_sponges | r35i1_top | NOT tidied | NO free place of 22 x 8 cm left on r94i1_tray_table: something there has to be moved together first |
| r84i1_succulent | r35i1_top | in place | plant: stays (r35i1_top) |
| r85i1_red_snack_bag | r35i1_top | in place | snack on the kitchen counter / island: food, not rubbish: stays (r35i1_top) |
| r86i1_cables | r35i1_top | NOT tidied | its destination r159i1_cabinet cannot be reached: nearest standing place is 0.53 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most) (now, before anything is cleared: inf m) |
| r87i1_wrapper | r35i1_top | moved | to rubbish_bin |
| r88i1_small_box | r35i1_top | in place | kitchen / storage item where it is used: in place (r35i1_top) |
| r88i2_small_box | r35i1_top | in place | kitchen / storage item where it is used: in place (r35i1_top) |
| r89i1_salad_bowl | r35i1_top | moved | to r27i1_sink |
| r90i1_plate | r35i1_top | moved | to r27i1_sink |
| r91i1_tan_plate | r35i1_top | moved | to r27i1_sink |
| r92i1_pink_container | r35i1_top | moved | to r27i1_sink |
| r93i1_nugget | r35i1_top | moved | to r186i1_basket |
| r49i1_canister | r52i1_cutting_board | in place | storage canister on the cutting board by the range: in place |
| r53i1_jar | r52i1_cutting_board | in place | kitchen / storage item where it is used: in place (r52i1_cutting_board) |
- The fridge compartment is hollow in the collision model (upward surfaces found by vertical rays, doors open: [-0.0, 0.11, 0.3, 0.456, 0.556, 0.756, 0.856, 1.056, 1.156, 1.356, 1.426] m; the one used: 0.856 m): the milk jug (and the drinks on the island) go there in an OPTIONAL round once a door skill exists: open r34i1_fresh_door, place_on the compartment floor, close it. The island drawers r36i1-3 are hollow too (18 cm deep): snacks and the cable bundle could go in with a drawer skill. Neither is in the route.

### Doors
- Open in the pack (by geometry: the leaf / rack sticks out of its housing at q = 0): r32i1_door, r33i1_rack, r33i2_rack, r159i1_door. Everything else (front door, closets, cabinets, drawers, oven, fridge, lift-top, ottoman lid) is closed.
- The dishwasher (door + 2 racks): v2's `close_dishwasher` step, before the first sink trip (the surface agent is building it).
- r159i1_door (TV cabinet door, 2.5 kg, hinge [-2.5, -2.38]): `close_door`, push at [-2.51, -1.95, 0.28] toward [1.0, -0.04], stand at [-2.75, -1.95] (marginal: the pelvis can stand 0.24 m from it; low shelf: deep squat and a level reach into the cubby); 2.5 kg leaf, hinge damping 0.2 N m s: a few newtons; the stroke follows an arc of 0.78 m, longer than one arm stroke: push the free end about 0.25 m, step, push again (or let it swing on: damping is low). Before the rug toys (it stands 0.5 m into the room beside them).

### What stays NOT clean at the end of this plan, and why
- r108i1_scissors (tool): not graspable: too thin: 0.9 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r146i1_bowl (dish): not graspable: too wide: narrowest silhouette 20 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take; rim pinch: open only 1.2 cm deep (rim inner radius 8.9 cm, 8.0 cm high): filled to near the rim (contents in the mesh): kept solid
- r152i1_sippy_cup (container): not reachable: nearest standing place is 0.90 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most)
- r156i1_clementines (food): not graspable: too wide: narrowest silhouette 20 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take
- r157i1_paper (paper): never became reachable in the route
- r157i2_paper (paper): never became reachable in the route
- r161i1_hair_dryer (appliance): hair dryer on the TV cabinet top: belongs in a bathroom or a drawer; there is no bathroom and no hollow storage the robot can open (the storage ottoman's base is solid in the collision model, ray-tested): left on the cabinet top beside the books
- r165i1_coat (clothing): not reachable: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most)
- r174i1_plush (toy): not reachable: no pick stance even with every movable thing gone: blocked by brick_wall, r169i1_two_tier_table, r175i1_cardboard_box@v3
- r176i1_cap (clothing): not graspable: too wide: narrowest silhouette 19 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take
- r182i1_bottle (container): not reachable: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.95 m) reach 0.58 m at most)
- r183i1_cup (dish): not reachable: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.80 m) reach 0.43 m at most)
- r194i1_strap (cable): not reachable: no pick stance even with every movable thing gone: blocked by r143i1_sofa, r145i1_base
- r195i2_paper (paper): not reachable: no pick stance even with every movable thing gone: blocked by r143i1_sofa, r145i1_base
- r69i1_scrap (paper): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i2_scrap (paper): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i3_scrap (paper): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i4_scrap (paper): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r74i1_milk_jug (container): OPTIONAL fridge round, not in the route: the fridge doors are frozen in our rooms and no door skill exists (the surface agent is building one for the dishwasher); with it: open r34i1_fresh_door, set the jug on the compartment floor, close the door. 
- r77i1_iron (appliance): not reachable: nearest standing place is 0.78 m from it (ASSUMED reach 0.50 m at most) (hand comes in from its side grasp's side)
- r83i2_sponges (package): NO free place of 22 x 8 cm left on r94i1_tray_table: something there has to be moved together first
- r86i1_cables (cable): its destination r159i1_cabinet cannot be reached: nearest standing place is 0.53 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most) (now, before anything is cleared: inf m)

## In v2's layout, with the v3 numbers
- **60 of the 81 mess things are planned** (v1: 25). By grasp type (by geometry, not verified; the live agents confirm or reject each NEW type): top_down 22, cloth 8, side 8, surface_pinch 10, rim_pinch 2, edge 7.
- 8 mess things have no grasp of any of the five types (list below: what remains impossible with a two-jaw gripper, and why); 13 more have a grasp but no standing place within reach, a destination that cannot be reached, or no free target spot.
- The sink decides most of the rest: 2 dishes with a grasp wait for it. Its nearest standing place is 0.56 m from the basin with the dishwasher closed (marginal under the 0.5 m limit; it would be marginal under v1's 0.60 m) and 0.92 m with it open. The measured furniture reach map (cloth/surface agent) settles it; the corner cabinet's 12 cm bottom panel, which sticks out 25 cm in front of its diagonal face, is what keeps the robot away (see 'The sink and the dishwasher').
- New in v2: five grasp types from the collision and visual meshes (grasps_v2.json, grasp_types.py, README_GRASPS.md); hollow colliders for 16 cups / glasses / bowls / mugs (hollow_colliders.json: the pack's colliders are solid hulls, so no rim pinch is possible without them); a collider for the SINK (the pack's sink has none: a dish let go over it falls into the cabinet); the dishwasher closed as an OPTIONAL step (sink stance computed both ways); a target spot for every planned thing (basket and sink slots too); a hook that reads a MEASURED reach map once the cloth/surface agent names one in PROGRESS_CLOTH.md (used: C:\Users\raresense\sim_home\apartment\reach\planner_reach_rows.json).
- v1's own outputs predate the previous agent's last edit of make_full_plan.py (a tight 7.8 cm section fallback and reach limits 0.34 / 0.50 m instead of 0.45 / 0.60 m): part of the change from v1 comes from that, not from the new grasp types. Reach sensitivity (same v2 code, other limits): reach 0.45 / 0.6 m, dishwasher closed: 50 planned; reach 0.34 / 0.5 m, dishwasher open: 28 planned; reach 0.45 / 0.6 m, dishwasher open: 28 planned.

## Counts
- Loose objects in the pack: 198 (+ our added rubbish bin).
- Mess to move: 81 (60 planned in the route, 21 skipped). Mess left on purpose: 1. Already in place: 50. Furniture, appliances and things where they belong: 66.

| Class | all | mess planned | mess skipped | left / in place |
|---|---|---|---|---|
| container | 51 | 11 | 3 | 37 |
| dish | 31 | 11 | 2 | 18 |
| paper | 12 | 5 | 7 | 0 |
| toy | 12 | 10 | 1 | 1 |
| bag | 10 | 2 | 0 | 8 |
| appliance | 8 | 0 | 1 | 7 |
| shoe | 8 | 7 | 0 | 1 |
| textile | 7 | 6 | 0 | 1 |
| plant | 5 | 0 | 0 | 5 |
| electronics | 4 | 0 | 0 | 4 |
| food | 4 | 0 | 1 | 3 |
| cable | 4 | 0 | 2 | 2 |
| table | 4 | 0 | 0 | 4 |
| cushion | 3 | 0 | 0 | 3 |
| clothing | 3 | 1 | 2 | 0 |
| basket | 3 | 0 | 0 | 3 |
| cookware | 3 | 0 | 0 | 3 |
| food_package | 3 | 1 | 0 | 2 |
| tool | 3 | 0 | 1 | 2 |
| toy_vehicle | 3 | 2 | 0 | 1 |
| book | 3 | 0 | 0 | 3 |
| decor | 2 | 0 | 0 | 2 |
| package | 2 | 1 | 1 | 0 |
| stool | 2 | 0 | 0 | 2 |
| umbrella | 2 | 2 | 0 | 0 |
| rug | 1 | 0 | 0 | 1 |
| lamp | 1 | 0 | 0 | 1 |
| kitchenware | 1 | 0 | 0 | 1 |
| hook_rack | 1 | 0 | 0 | 1 |
| stroller | 1 | 0 | 0 | 1 |
| cutlery | 1 | 1 | 0 | 0 |

| Destination | planned | skipped | where the robot stands / reach (by geometry, not verified) |
|---|---|---|---|
| r186i1_basket | 13 | 1 | marginal: the pelvis can stand 0.17 m from it; low shelf: deep squat and a level reach into the cubby (now, before anything is cleared: inf m) |
| floor beside r186i1_basket / r185i1_megabloks_bag (toy corner) | 3 | 0 | floor spots beside the toy basket |
| rubbish_bin | 6 | 7 | marginal: nearest standing place is 0.02 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without) (now, before anything is cleared: 0.38 m) |
| r133i1_laundry_basket | 7 | 2 | yes: the pelvis can stand 0.47 m from it |
| r27i1_sink | 16 | 3 | marginal: nearest standing place is 0.56 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.95 m) limit 0.55 m without) (to the nearest point 6 cm inside the basin; dishwasher closed by the optional step) |
| r119i1_mat | 7 | 0 | marginal: the pelvis can stand 0.22 m from it; low shelf: deep squat and a level reach into the cubby (now, before anything is cleared: 1.06 m) |
| r110i1_console | 0 | 2 | no: nearest standing place is 0.64 m from it (MEASURED (planner_reach_rows.json, pad height 0.80 m) reach 0.43 m at most) (now, before anything is cleared: inf m) |
| r35i1_top | 0 | 2 | no: nearest standing place is 0.63 m from it (MEASURED (planner_reach_rows.json, pad height 0.95 m) reach 0.58 m at most) |
| r94i1_tray_table | 2 | 2 | yes: the pelvis can stand 0.48 m from it |
| vehicle corner (hall wall, beside the toy bike) | 2 | 0 | no: nearest standing place is 0.51 m from it (ASSUMED reach 0.50 m at most) |
| by the entry (floor) | 1 | 0 | marginal: the pelvis can stand 0.15 m from it; low shelf: deep squat and a level reach into the cubby (now, before anything is cleared: inf m) |
| against the wall: r20i1_baseboard, wall_grey_shell at (-1.08, 1.81) (floor) | 1 | 0 | no: nearest standing place is 0.51 m from it (ASSUMED reach 0.50 m at most) |
| against the wall by the two-tier table (floor) | 1 | 0 | marginal: nearest standing place is 0.34 m from it: needs a trunk lean over the furniture (ASSUMED limit 0.34 m without); low shelf: deep squat and a level reach into the cubby (now, before anything is cleared: inf m) |
| floor beside the standing bags (by the entry) | 1 | 0 | marginal: nearest standing place is 0.38 m from it: needs a trunk lean over the furniture (ASSUMED limit 0.34 m without); low shelf: deep squat and a level reach into the cubby (now, before anything is cleared: inf m) |
| r159i1_cabinet | 0 | 1 | no: nearest standing place is 0.53 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most) (now, before anything is cleared: inf m) |
| r34i1_body | 0 | 1 | marginal: nearest standing place is 0.55 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.95 m) limit 0.55 m without) |

| Skill needed (planned things) | count | state today |
|---|---|---|
| floor_pick | 24 | exists: proven on one toy piece (run 1118_193303); top-down only |
| cloth_pick | 8 | grasp_cloth written by the cloth agent from its live knit-hat runs (E:/urc_cloth, commit cf4eabf); the other six garments not tried yet |
| surface_pick | 25 | NOT BUILT (no pick from furniture exists) |
| surface_pick, counter 0.91-0.95 m (standing, hand at chest height) | 12 | not built |
| surface_pick, low table / seat 0.45-0.56 m (half squat) | 10 | not built |
| surface_pick, table / sill 0.72-0.78 m (standing) | 3 | not built |
| put: drop_in_sink (lower into the basin) -> r27i1_sink | 16 | NOT BUILT (place into the sink); the sink needs a collider first (none in the pack) |
| put: drop_in -> r133i1_laundry_basket (cloth) | 7 | drop_in_cloth into the open-top hamper: written by the cloth agent from its live knit-hat runs (commit cf4eabf; not checked by the planner) |
| put: put_down (lower the bag hanging from its handles until it stands, open) -> floor beside the standing bags (by the entry) | 1 | put_down on a floor spot: written, not run yet (a bag hanging from its handles: lower until it stands) |
| put: place_on (set on a table) -> r94i1_tray_table | 2 | NOT BUILT (place_on a table) |
| put: drop_in -> rubbish_bin | 6 | drop_in: ran in the practice room only, not in the apartment |
| put: put_down (lower into a low basket) -> r186i1_basket | 12 | exists: proven once (toy piece into the toy basket) |
| put: put_down (set on the mat) -> r119i1_mat | 7 | put_down on a flat mat: written, not run yet |
| put: let go of the dragged rim -> against the wall: r20i1_baseboard, wall_grey_shell at (-1.08, 1.81) (floor) | 1 | NOT BUILT (part of the same new step) |
| put: put_down (set on the floor) -> by the entry (floor) | 1 | put_down on a floor spot: written, a flat destination not run yet |
| put: set_down (carry2: walk in nose first, lower both hands until the wheels touch, open both jaws) -> vehicle corner (hall wall, beside the toy bike) | 2 | NOT BUILT (part of the same new step) |
| put: put_down (set on the floor) -> floor beside r186i1_basket / r185i1_megabloks_bag (toy corner) | 3 | put_down on the floor: written, a flat destination is not run yet |
| put: put_down (set on the floor) -> against the wall by the two-tier table (floor) | 1 | put_down on a floor spot: written, not run yet |
| put: put_down (lower into a low basket) -> r186i1_basket (cloth) | 1 | exists: proven once (toy piece into the toy basket) |
| needs_two_hands | 5 | not built (big garments, things over 1 kg) |
| container_carry | 2 carries | not built |
| door / drawer (OPTIONAL step close_dishwasher) | 1 step | not built; frees the sink. The milk jug (fridge) is still left |

Grasp by geometry over the 81 mess things: yes 42, marginal 31, no 8. Reach: no 11, after clearing 27, yes 24, marginal 19.

## Grasp types (v2, by geometry, not verified)
Exactly what each type assumes: README_GRASPS.md. Counts over the mess things: 'usable' = has a yes / marginal candidate of that type; 'planned with it' = the type the plan uses.

| Grasp type | mess things it can take | planned with it | skill today |
|---|---|---|---|
| top_down | 45 | 22 | fingers-down pick (floor: exists, run 1118_193303; from furniture: not built) |
| side | 47 | 8 | NEW: side grasp, hand level, jaws horizontal (not built) |
| surface_pinch | 25 | 10 | NEW: fingertips on the support while the jaws close (not built) |
| rim_pinch | 7 | 2 | NEW: rim pinch, jaws part-open, one inside (not built; needs the hollow collider) |
| edge | 19 | 7 | NEW: edge grasp, jaws vertical under an overhang, after a slide when needed (not built) |
| cloth (7 garments) | 9 | 8 | cloth pinch (cloth agent's grasp_cloth, written from its live knit-hat runs, commit cf4eabf) |

Planned with a NEW grasp type (the live agents confirm or reject these first):
- r106i1_umbrella (umbrella): drag, marginal: near rim lifted to 0.6 m, far rim slides: 3.1 N at the hand (8 % of the hold), no torque to speak of; the grasp at floor level is the hard part
- r123i1_slipper (shoe): surface_pinch, yes: 4.7 cm high: fingertips at the support, 2.6 cm of pad on it
- r124i1_sandal (shoe): surface_pinch, yes: 4.7 cm high: fingertips at the support, 2.7 cm of pad on it
- r126i1_scooter (toy_vehicle): carry2, yes: 14.7 N a hand (37 % of the hold's 40 N); the centre of mass is 0.19 m off the bar, 2.9 N m a hand (72 % of the 4.0 N m hold torque; past it the deck swings down until its far end touches the floor, which turns the carry into a drag, not a drop); the robot carries 3.0 kg about 0.52 m ahead of the pelvis (the 0.3 kg basket already pitched the pelvis 0.13 rad, run 1119_001520)
- r127i1_scooter (toy_vehicle): carry2, yes: 13.2 N a hand (33 % of the hold's 40 N); the centre of mass is 0.17 m off the bar, 2.3 N m a hand (57 % of the 4.0 N m hold torque; past it the deck swings down until its far end touches the floor, which turns the carry into a drag, not a drop); the robot carries 2.7 kg about 0.50 m ahead of the pelvis (the 0.3 kg basket already pitched the pelvis 0.13 rad, run 1119_001520)
- r148i1_pink_lid (dish): edge, marginal: 6.5 cm from the edge: slide it 8.3 cm out first (more than 3 cm: long slide); 2.4 cm thick at the edge
- r149i1_pouch (food_package): edge, marginal: 24.7 cm from the edge: slide it 26.5 cm out first (more than 3 cm: long slide); 2.0 cm thick at the edge
- r151i1_spoon (cutlery): edge, marginal: 5.1 cm from the edge: slide it 6.9 cm out first (more than 3 cm: long slide); 0.8 cm thick at the edge
- r154i1_stick (container): edge, yes: 2.3 cm from the edge: slide it 4.1 cm out first; 1.0 cm thick at the edge
- r171i1_glass (dish): rim_pinch, yes: wall 5 mm at the rim (1.0 cm across the 2.9 cm pad band: wall + the rim's curve), jaws open 2.0 cm, 2.5 cm of pad on it, 3.8 cm clear inside behind the inner jaw
- r173i1_tumbler (dish): side, marginal: section 6.3 cm across at 5.1 cm above the support (pad middle); side grasp at floor level: hand level a few cm above the floor in the deep squat (not measured)
- r175i1_cardboard_box (container): side, marginal: section 6.1 cm across at 18.1 cm above the support (pad middle); side grasp at floor level: hand level a few cm above the floor in the deep squat (not measured)
- r177i1_bowl (dish): rim_pinch, yes: wall 10 mm at the rim (2.0 cm across the 2.9 cm pad band: wall + the rim's curve), jaws open 3.0 cm, 1.5 cm of pad on it, 5.7 cm clear inside behind the inner jaw
- r179i1_toy_pouch (bag): side, marginal: section 7.8 cm across at 16.1 cm above the support (pad middle); under 4.5 mm to spare a side
- r192i1_ball (toy): side, marginal: section 5.8 cm across at 5.1 cm above the support (pad middle); side grasp at floor level: hand level a few cm above the floor in the deep squat (not measured)
- r193i1_toy_piece (container): surface_pinch, yes: 3.1 cm high: fingertips at the support, 2.9 cm of pad on it
- r193i2_toy_piece (container): surface_pinch, yes: 3.1 cm high: fingertips at the support, 2.9 cm of pad on it
- r193i3_toy_piece (container): surface_pinch, yes: 3.1 cm high: fingertips at the support, 2.9 cm of pad on it
- r193i4_toy_piece (container): surface_pinch, yes: 3.1 cm high: fingertips at the support, 2.9 cm of pad on it
- r195i1_paper (paper): surface_pinch, marginal: 3.0 cm high: fingertips at the support, 2.8 cm of pad on it; 7.7 cm across: under 4.5 mm to spare a side
- r195i3_paper (paper): surface_pinch, marginal: 3.0 cm high: fingertips at the support, 2.8 cm of pad on it; 7.7 cm across: under 4.5 mm to spare a side
- r196i1_plastic_bag (paper): surface_pinch, marginal: 1.4 cm high: fingertips at the support, 1.0 cm of pad on it
- r197i1_cup (dish): surface_pinch, yes: 6.0 cm high: fingertips at the support, 2.9 cm of pad on it
- r63i1_glass (dish): side, marginal: section 7.8 cm across at 6.1 cm above the support (pad middle); under 4.5 mm to spare a side
- r71i1_lysol (container): side, yes: section 3.5 cm across at 26.1 cm above the support (pad middle)
- r83i1_sponges (package): side, yes: section 6.4 cm across at 5.1 cm above the support (pad middle)
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
  - dishwasher open (as the pack is), feet may step on the scraps: stand at [4.4, 0.95], 0.92 m to the basin: no
  - dishwasher open, feet kept off the scraps (v1's condition): stand at [4.4, 0.9], 0.96 m to the basin: no
- The plan uses: dishwasher closed; the feet may step on the 0.5 cm paper scraps r69i1_scrap, r69i2_scrap, r69i3_scrap, r69i4_scrap (no grasp takes them; ASSUMED safe, like the cords and mats).

## Reach: assumed limits, and the hook for the measured map
- MEASURED reach map in use: C:\Users\raresense\sim_home\apartment\reach\planner_reach_rows.json (levels: 0.55 m: 0.00 / 0.43 m, 0.78 m: 0.48 / 0.50 m, 0.80 m: 0.39 / 0.43 m, 0.95 m: 0.55 / 0.58 m); heights it does not cover use the ASSUMED limits.
- Hook: `measured_reach_map()` reads the newest existing JSON whose name contains 'reach' named in PROGRESS_CLOTH.md (rows z, x, y, err_xy, err_z, lean as scripts\home\live\s10_reach_probe.py writes them; reached = err_xy <= 1 cm and |err_z| <= 1.5 cm). Re-run this script after it appears.
- Sensitivity, reach 0.45 / 0.6 m, dishwasher closed: 50 planned (2026-11-18 23:53).
- Sensitivity, reach 0.34 / 0.5 m, dishwasher open: 28 planned (2026-11-18 23:53).
- Sensitivity, reach 0.45 / 0.6 m, dishwasher open: 28 planned (2026-11-18 23:54).

## What a different hand would add (Unitree Dex3-1, coarse, geometry only)
Using the same object geometry, a three-finger Dex3-1 (thumb + two fingers; widest thumb-to-finger gap 14.3 cm, measured on the Menagerie G1-with-hands model) would make **0 more of the 81 mess things graspable** (none): things up to about 13 cm across that no jaw section, rim or edge serves. It would also turn 12 marginal two-jaw grasps into comfortable ones (tight 7.7-7.8 cm fits, hand pitched down, things that swing from a rim or edge grip: r63i1_glass, r87i1_wrapper, r105i1_shoe, r105i2_shoe, r125i1_flat, r125i2_flat, r130i1_light_saber, r179i1_toy_pouch, r191i1_toy_vehicle, r195i1_paper, r195i2_paper, r195i3_paper). It would not help the 8 that stay impossible (r108i1_scissors, r146i1_bowl, r156i1_clementines, r176i1_cap, r69i1_scrap, r69i2_scrap, r69i3_scrap, r69i4_scrap): flat things under 1 cm still need a nail, a scoop or suction, and the rest are wider than its span or too heavy for the arm. This is a COARSE estimate from object sizes and the hand's span (no finger kinematics, contacts or reach were checked); reach and the destination limits would still apply, so it is not a count of extra planned items.

## Skipped mess, and why
- r108i1_scissors (tool, to r110i1_console): not graspable: too thin: 0.9 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r146i1_bowl (dish, to r27i1_sink): not graspable: too wide: narrowest silhouette 20 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take; rim pinch: open only 1.2 cm deep (rim inner radius 8.9 cm, 8.0 cm high): filled to near the rim (contents in the mesh): kept solid
- r152i1_sippy_cup (container, to r27i1_sink): not reachable: nearest standing place is 0.90 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most)
- r156i1_clementines (food, to r35i1_top): not graspable: too wide: narrowest silhouette 20 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take
- r157i1_paper (paper, to rubbish_bin): never became reachable in the route
- r157i2_paper (paper, to rubbish_bin): never became reachable in the route
- r165i1_coat (clothing, to r133i1_laundry_basket): not reachable: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most)
- r174i1_plush (toy, to r186i1_basket): not reachable: no pick stance even with every movable thing gone: blocked by brick_wall, r169i1_two_tier_table, r175i1_cardboard_box@v3
- r176i1_cap (clothing, to r110i1_console): not graspable: too wide: narrowest silhouette 19 cm (jaws 7.9 cm), no rim, edge or section any of the five types can take
- r182i1_bottle (container, to r35i1_top): not reachable: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.95 m) reach 0.58 m at most)
- r183i1_cup (dish, to r27i1_sink): not reachable: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.80 m) reach 0.43 m at most)
- r194i1_strap (cable, to r133i1_laundry_basket): not reachable: no pick stance even with every movable thing gone: blocked by r143i1_sofa, r145i1_base
- r195i2_paper (paper, to rubbish_bin): not reachable: no pick stance even with every movable thing gone: blocked by r143i1_sofa, r145i1_base
- r69i1_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i2_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i3_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r69i4_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)
- r74i1_milk_jug (container, to r34i1_body): OPTIONAL fridge round, not in the route: the fridge doors are frozen in our rooms and no door skill exists (the surface agent is building one for the dishwasher); with it: open r34i1_fresh_door, set the jug on the compartment floor, close the door. 
- r77i1_iron (appliance, to r94i1_tray_table): not reachable: nearest standing place is 0.78 m from it (ASSUMED reach 0.50 m at most) (hand comes in from its side grasp's side)
- r83i2_sponges (package, to r94i1_tray_table): NO free place of 22 x 8 cm left on r94i1_tray_table: something there has to be moved together first
- r86i1_cables (cable, to r159i1_cabinet): its destination r159i1_cabinet cannot be reached: nearest standing place is 0.53 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most) (now, before anything is cleared: inf m)

Mess left on purpose (no destination the robot can serve):
- r161i1_hair_dryer: hair dryer on the TV cabinet top: belongs in a bathroom or a drawer; there is no bathroom and no hollow storage the robot can open (the storage ottoman's base is solid in the collision model, ray-tested): left on the cabinet top beside the books

Things that are planned but only reachable after a neighbour is gone (the route respects this):
- r105i1_shoe: clear r105i2_shoe first
- r105i2_shoe: clear r105i1_shoe first
- r106i1_umbrella: clear r120i1_duck, r117i1_blanket first
- r116i1_coat_pile: clear r121i1_jacket first
- r117i1_blanket: clear r121i1_jacket first
- r120i1_duck: clear r117i1_blanket, r106i1_umbrella, r116i1_coat_pile first
- r120i2_duck: clear r186i1_basket, r196i1_plastic_bag, r197i1_cup, r125i1_flat, r125i2_flat first
- r125i1_flat: clear r197i1_cup, r125i2_flat, r120i2_duck, r186i1_basket, r196i1_plastic_bag first
- r125i2_flat: clear r197i1_cup, r125i1_flat, r173i1_tumbler, r174i1_plush, r120i2_duck, r195i2_paper first
- r147i1_purple_container: clear r188i1_dollhouse first
- r149i1_pouch: clear r155i1_kids_bottle first
- r173i1_tumbler: clear r175i1_cardboard_box, r174i1_plush, r125i2_flat first
- r175i1_cardboard_box: clear r173i1_tumbler, r174i1_plush first
- r188i1_dollhouse: clear r193i2_toy_piece, r189i1_santa_hat, r192i1_ball first
- r189i1_santa_hat: clear r192i1_ball first
- r190i1_stocking: clear r192i1_ball first
- r191i1_toy_vehicle: clear r189i1_santa_hat, r192i1_ball first
- r193i2_toy_piece: clear r189i1_santa_hat, r192i1_ball first
- r193i4_toy_piece: clear r189i1_santa_hat, r192i1_ball first
- r196i1_plastic_bag: clear r120i2_duck, r186i1_basket, r188i1_dollhouse, r197i1_cup, r195i2_paper, r193i2_toy_piece, r125i1_flat first
- r197i1_cup: clear r125i1_flat, r125i2_flat, r120i2_duck, r186i1_basket, r196i1_plastic_bag first
- r71i1_lysol: clear r106i1_umbrella first
- r78i1_kids_bottle: clear r106i1_umbrella first
- r87i1_wrapper: clear r106i1_umbrella first
- r92i1_pink_container: clear r106i1_umbrella first
- r93i1_nugget: clear r106i1_umbrella first

Planned with a marginal grasp or reach (expect failures here first):
- r100i1_towel: reach: nearest standing place is 0.40 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r105i1_shoe: grasp: section 9 cm off the middle: it can swing or tip in the jaws
- r105i2_shoe: grasp: section 11 cm off the middle: it can swing or tip in the jaws
- r106i1_umbrella: grasp: near rim lifted to 0.6 m, far rim slides: 3.1 N at the hand (8 % of the hold), no torque to speak of; the grasp at floor level is the hard part
- r125i1_flat: grasp: section 8 cm off the middle: it can swing or tip in the jaws
- r125i2_flat: grasp: section 9 cm off the middle: it can swing or tip in the jaws
- r130i1_light_saber: grasp: section 8 cm off the middle: it can swing or tip in the jaws
- r138i1_cup: reach: nearest standing place is 0.37 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r139i1_toy_car: reach: nearest standing place is 0.41 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r147i1_purple_container: reach: now: nearest standing place is 0.80 m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most). With r188i1_dollhouse gone: nearest standing place is 0.29 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r148i1_pink_lid: grasp: 6.5 cm from the edge: slide it 8.3 cm out first (more than 3 cm: long slide); 2.4 cm thick at the edge; reach: now: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most). With the movable things gone: nearest standing place is 0.21 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without) (hand comes in from its edge grasp's side)
- r149i1_pouch: grasp: 24.7 cm from the edge: slide it 26.5 cm out first (more than 3 cm: long slide); 2.0 cm thick at the edge; reach: now: nearest standing place is 0.22 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without). With r155i1_kids_bottle gone: nearest standing place is 0.22 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without) (hand comes in from its edge grasp's side)
- r151i1_spoon: grasp: 5.1 cm from the edge: slide it 6.9 cm out first (more than 3 cm: long slide); 0.8 cm thick at the edge; reach: nearest standing place is 0.34 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without) (hand comes in from its edge grasp's side)
- r154i1_stick: reach: now: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most). With the movable things gone: nearest standing place is 0.21 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without) (hand comes in from its edge grasp's side)
- r155i1_kids_bottle: reach: nearest standing place is 0.32 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r158i1_tissue: reach: nearest standing place is 0.36 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r171i1_glass: reach: now: nearest standing place is inf m from it (MEASURED (planner_reach_rows.json, pad height 0.55 m) reach 0.43 m at most). With the movable things gone: nearest standing place is 0.32 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.55 m) limit 0.00 m without)
- r173i1_tumbler: grasp: section 6.3 cm across at 5.1 cm above the support (pad middle); side grasp at floor level: hand level a few cm above the floor in the deep squat (not measured)
- r175i1_cardboard_box: grasp: section 6.1 cm across at 18.1 cm above the support (pad middle); side grasp at floor level: hand level a few cm above the floor in the deep squat (not measured)
- r179i1_toy_pouch: grasp: section 7.8 cm across at 16.1 cm above the support (pad middle); under 4.5 mm to spare a side
- r188i1_dollhouse: grasp: section 8 cm off the middle: it can swing or tip in the jaws
- r191i1_toy_vehicle: grasp: 7.3 cm across: under 4.5 mm to spare a side (the floor agent's search rejects it)
- r192i1_ball: grasp: section 5.8 cm across at 5.1 cm above the support (pad middle); side grasp at floor level: hand level a few cm above the floor in the deep squat (not measured)
- r195i1_paper: grasp: 3.0 cm high: fingertips at the support, 2.8 cm of pad on it; 7.7 cm across: under 4.5 mm to spare a side
- r195i3_paper: grasp: 3.0 cm high: fingertips at the support, 2.8 cm of pad on it; 7.7 cm across: under 4.5 mm to spare a side
- r196i1_plastic_bag: grasp: 1.4 cm high: fingertips at the support, 1.0 cm of pad on it
- r63i1_glass: grasp: section 7.8 cm across at 6.1 cm above the support (pad middle); under 4.5 mm to spare a side
- r70i1_tote: grasp: section 14 cm off the middle: it can swing or tip in the jaws; fingers down with its top 1.20 m up: the wrist about 1.30 m (ASSUMED limit 1.05 m); 0.90 kg: heavy for pad friction alone (measured squeeze 6 N a pad); reach: nearest standing place is 0.44 m from it: needs a trunk lean over the furniture (ASSUMED limit 0.34 m without); grasp height about 1.19 m: at or above the shoulder
- r71i1_lysol: reach: now: nearest standing place is 1.08 m from it (ASSUMED reach 0.50 m at most). With r106i1_umbrella gone: nearest standing place is 0.46 m from it: needs a trunk lean over the furniture (ASSUMED limit 0.34 m without); grasp height about 1.17 m: at or above the shoulder (hand comes in from its side grasp's side)
- r78i1_kids_bottle: grasp: fingers down with its top 1.13 m up: the wrist about 1.23 m (ASSUMED limit 1.05 m); reach: now: nearest standing place is 0.82 m from it (ASSUMED reach 0.50 m at most). With r106i1_umbrella gone: nearest standing place is 0.36 m from it: needs a trunk lean over the furniture (ASSUMED limit 0.34 m without); grasp height about 1.12 m: at or above the shoulder
- r81i1_glass_spoon: grasp: fingers down with its top 1.10 m up: the wrist about 1.20 m (ASSUMED limit 1.05 m); reach: nearest standing place is 0.55 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.95 m) limit 0.55 m without); grasp height about 1.09 m: at or above the shoulder
- r87i1_wrapper: grasp: 7.7 cm across: under 4.5 mm to spare a side (the floor agent's search rejects it); fingers down with its top 0.95 m up: the wrist about 1.05 m (ASSUMED limit 1.05 m)
- r89i1_salad_bowl: grasp: 5.0 cm from the edge: slide it 6.8 cm out first (more than 3 cm: long slide); 3.4 cm thick at the edge; held at its edge the weight turns it 0.98 N m (pads resist about 0.17 N m at 6 N): it will swing down to hang from the grip, or use two hands; 0.90 kg: heavy for pad friction alone (measured squeeze 6 N a pad)
- r90i1_plate: grasp: 20.5 cm from the edge: slide it 22.3 cm out first (more than 3 cm: long slide); 1.3 cm thick at the edge; held at its edge the weight turns it 0.59 N m (pads resist about 0.17 N m at 6 N): it will swing down to hang from the grip, or use two hands

## Route (one episode)
Chosen: toy basket carried to the rug toys: yes; bin carried to the living room: no. Whole-route time with the stated speeds for the four ways: basket carried, bin carried: 60 min; basket carried, bin stays: 59 min; basket stays, bin carried: 60 min; basket stays, bin stays: 58 min.
Toy basket spot on the rug (scene): (-1.75, -0.60). Bin spot in the living room (scene): (-1.80, -0.15).

| # | Step (runner form) | What | Items | Walk empty / carrying m | s (stated speeds) | Runs today? |
|---|---|---|---|---|---|---|
| 1 | `tidy_all` | v3: clear the new places of the big things first (r119i1_mat) | 2 | 1.78 / 2.68 | 75 | no: runner form exists; put_down on the flat mat with a target spot per shoe is NOT run yet (pair spots need a new option) |
| 2 | `carry2` | v3: r127i1_scooter to vehicle corner (hall wall, beside the toy bike) by carry2 (it stands in a walking route) | 1 | 3.14 / 2.55 | 71 | no: NEW step type carry2 (not built): two-hand take of the handlebar, stand, walk at the carrying speed, set down nose to the wall |
| 3 | `carry2` | v3: r126i1_scooter to vehicle corner (hall wall, beside the toy bike) by carry2 (it stands in a walking route) | 1 | 2.85 / 3.19 | 74 | no: NEW step type carry2 (not built): two-hand take of the handlebar, stand, walk at the carrying speed, set down nose to the wall |
| 4 | `tidy_all` | east: rubbish to the bin (bin at home) | 1 | 1.76 / 1.91 | 39 | no: runner form exists; drop_in into the bin ran in the practice room only |
| 5 | `garments` | entry, kitchen, hall: garments to the hamper (big ones one per trip, two hands); v3: the towel from the stool | 6 | 18.05 / 19.65 | 422 | no: the CLOTH agent's runner form (E:/urc_cloth/scripts/home/cloth_episode.py); one merged runner for cloth + rigid in the same episode does not exist yet |
| 6 | `tidy_all` | east: shoes to the doormat in pairs | 3 | 5.45 / 6.28 | 131 | no: runner form exists; put_down on the flat mat with a target spot per shoe is NOT run yet (pair spots need a new option) |
| 7 | `tidy_all` | v3: the small umbrella to the floor by the front door | 1 | 2.15 / 4.59 | 58 | no: runner form exists; put_down on a per-object floor spot (room_patch_v3 target spot) is written, a flat floor destination not run yet |
| 8 | `close_dishwasher` | OPTIONAL: push both dishwasher racks in, lift the door shut (frees the floor in front of the sink) | 1 | 3.98 / 0.0 | 69 | no: NEW: door / drawer skill (not built); the room file must leave these 3 joints free (doors are frozen today) |
| 9 | `tidy_surface` | kitchen: used dishes from the island and the counter to the sink | 5 | 3.07 / 4.49 | 182 | no: NEW step type: pick from furniture (surface_pick) + drop_in_sink (lower into the basin); floor and cloth things in the list go through their own skills |
| 10 | `tidy_surface` | kitchen: cleaning things (and v3: the iron) from the island to the tray table | 1 | 2.45 / 0.72 | 41 | no: NEW step type: pick from furniture (surface_pick) + place_on (set on a table); floor and cloth things in the list go through their own skills |
| 11 | `tidy_surface` | v3: the tote from the island to the standing bags by the entry | 1 | 1.97 / 4.79 | 63 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower the bag hanging from its handles until it stands, open); floor and cloth things in the list go through their own skills |
| 12 | `tidy_all` | crossing west: the east half's toys ride along to the toy basket at its home | 1 | 2.66 / 7.63 | 76 | YES |
| 13 | `drag` | v3: r106i1_umbrella to against the wall: r20i1_baseboard, wall_grey_shell at (-1.08, 1.81) (floor) by drag (it stands in a walking route) | 1 | 9.03 / 6.21 | 90 | no: NEW step type drag (not built): rim grasp at floor level, stand up holding, walk, let go at the spot |
| 14 | `tidy_surface` | toy corner: toys near the basket's home into it | 2 | 5.9 / 2.95 | 94 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower into a low basket); floor and cloth things in the list go through their own skills |
| 15 | `carry` | carry the toy basket to the rug toys | r186i1_basket | 0.0 / 3.17 | 58 | no: NEW step type: carry a container with two hands (not built) |
| 16 | `tidy_surface` | rug and side table: toys into the basket standing on the rug | 9 | 4.62 / 10.94 | 341 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower into a low basket); floor and cloth things in the list go through their own skills |
| 17 | `carry` | carry the full toy basket back to its place | r186i1_basket | 0.0 / 3.17 | 58 | no: NEW step type: carry a container with two hands (not built) |
| 18 | `close_door` | v3: close r159i1_door (open in the pack, standing 0.27 m out on average; its stance is free once the rug toys are gone) | 1 | 2.26 / 0.0 | 65 | no: NEW step type close_door (not built; the surface agent's door work for the dishwasher is the nearest); the room file must leave this joint free (frozen today) |
| 19 | `tidy_surface` | rug: the two big toys (v3: and the stick) to the toy corner (one per trip) | 3 | 6.77 / 7.58 | 145 | no: NEW step type: pick from furniture (surface_pick) + put_down (set on the floor); floor and cloth things in the list go through their own skills |
| 20 | `garments` | rug: remaining garments to the hamper (v3: the strap, the coat from the armchair) | 1 | 2.44 / 1.25 | 50 | no: the CLOTH agent's runner form (E:/urc_cloth/scripts/home/cloth_episode.py); one merged runner for cloth + rigid in the same episode does not exist yet |
| 21 | `tidy_surface` | living room: rubbish to the bin at its home (two per trip) | 3 | 7.79 / 10.61 | 152 | no: NEW step type: pick from furniture (surface_pick) + drop_in; floor and cloth things in the list go through their own skills |
| 22 | `tidy_all` | living room: the pair of flats to the doormat | 2 | 7.12 / 8.19 | 117 | no: runner form exists; put_down on the flat mat with a target spot per shoe is NOT run yet (pair spots need a new option) |
| 23 | `tidy_surface` | living room: used dishes to the sink (two per trip, the long way) | 9 | 40.52 / 54.66 | 656 | no: NEW step type: pick from furniture (surface_pick) + drop_in_sink (lower into the basin); floor and cloth things in the list go through their own skills |
| 24 | `tidy_all` | left-overs that waited for a neighbour: to against the wall by the two-tier table (floor) | 1 | 11.83 / 0.31 | 56 | no: runner form exists; a 25 cm tall box taken by its top ridge (top_down, 0.6 kg with the hold) and put down on a per-object floor spot: not run yet |
| 25 | `tidy_surface` | left-overs that waited for a neighbour: to rubbish_bin | 2 | 9.74 / 8.57 | 125 | no: NEW step type: pick from furniture (surface_pick) + drop_in; floor and cloth things in the list go through their own skills |
| 26 | `tidy_surface` | left-overs that waited for a neighbour: to r27i1_sink | 2 | 4.89 / 2.56 | 85 | no: NEW step type: pick from furniture (surface_pick) + drop_in_sink (lower into the basin); floor and cloth things in the list go through their own skills |
| 27 | `tidy_surface` | left-overs that waited for a neighbour: to r94i1_tray_table | 1 | 3.01 / 4.25 | 62 | no: NEW step type: pick from furniture (surface_pick) + place_on (set on a table); floor and cloth things in the list go through their own skills |
| 28 | `tidy_surface` | left-overs that waited for a neighbour: to r186i1_basket | 1 | 3.65 / 8.48 | 87 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower into a low basket); floor and cloth things in the list go through their own skills |

The exact step list (names in order, pairs adjacent) is in `route_steps.json`; per-object trips and seconds are in `full_plan.json`.
Step forms: `tidy_all` is the floor agent's (E:\urc_home\scripts\home\episode.py); `garments` is the cloth agent's (E:\urc_cloth\scripts\home\cloth_episode.py). NEW step types this plan needs: `carry` (a container, two hands), `tidy_surface` (pick from furniture; place on a table, a counter, into the sink). Also needed in the runner: one episode that mixes rigid and cloth steps, a destination PER OBJECT with a target spot (the room file maps a class to one place; `room_patch.json` holds the per-object table), and two per trip across neighbouring destinations.

## Time for the whole apartment
- Things moved: 60 in 43 trips, + 2 container carries. Planned walking: 169 m empty-handed, 191 m carrying.
- Today, with the stated speeds (0.45 m/s empty, 0.18 m/s carrying, pick 16 s, put-down 12 s) and the robot walking exactly the planned legs: **59 min** (59 s a thing).
- Today, at the end-to-end rates measured in run 1118_204943 (B2: 4.2 m of legs in 36 s empty, 7 m in 111 s carrying, pick 18 s, put-down 20 s): **1.9 h** (114 s a thing). This is what the code as committed would do, if nothing failed.
- At the target of 20-30 s a thing (container carries at 0.45 m/s on top): **23 min to 33 min**.
- Not in these numbers: failed grasps and second tries, falls, the scene settling at the start, compute time (the CPU path ran about 0.6x real time with recording).

## Top risks
- Most of the plan needs skills that do not exist: of the planned things only the floor toys into the toy basket use skills proven in a clean episode (one toy piece, 176 s). Surface picks, placing on tables / counters / into the sink, the container carry and the cloth pick are not built or not proven.
- 30 planned things rely on a NEW grasp type (side, surface pinch, rim pinch, edge) that exists only as geometry; rim pinches also need the hollow colliders applied, edge grasps a slide skill when the thing does not overhang.
- The sink has no collider in the pack: until SINK_COLLIDER (room_patch.json extras_add) is in the room, every dish 'put in the sink' falls into the cabinet below.
- The living room is far from the kitchen: used dishes travel about 9-10 m each, two per trip. At today's carrying speed this is the largest block of time. A dish caddy (a movable box carried once) would cut it but needs two-hand carrying of about 2.5 kg, over the 1.5 kg limit; not planned.
- Reach onto furniture is ASSUMED (0.45 m from the pelvis, 0.60 m with a lean); no reach map exists for standing or half-squat picks at 0.45-0.95 m. Things in the middle of the island, at the back of the counter and on the window sills behind the armchair and the gold table depend on it.
- The sink is in the corner behind the open dishwasher door and racks; with the optional closing step: marginal: nearest standing place is 0.56 m from it: needs a trunk lean over the furniture (MEASURED (planner_reach_rows.json, pad height 0.95 m) limit 0.55 m without) (to the nearest point 6 cm inside the basin; dishwasher closed by the optional step). Four paper scraps lie on the floor exactly there and cannot be picked up (0.5 cm thin): the plan lets the feet step on them.
- The doormat is half covered by the floor lamp's base; only the free part is used for the shoes: r124i1_sandal: (2.35, -1.97); r105i1_shoe: (2.28, -1.72); r105i2_shoe: (2.40, -1.72); r125i1_flat: (2.05, -1.72); r125i2_flat: (2.16, -1.72); r122i1_croc: (2.00, -1.35); r123i1_slipper: (2.16, -1.35).
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
- `C:\Users\raresense\sim_home\apartment\full_plan\full_plan_v3.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\route_steps_v3.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\room_patch_v3.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\clean_targets_v3.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\FULL_PLAN_v3.md`
- `C:\Users\raresense\sim_home\apartment\full_plan\make_full_plan_v3.py`
- `C:\Users\raresense\sim_home\apartment\full_plan\check_clean_look.py`
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
