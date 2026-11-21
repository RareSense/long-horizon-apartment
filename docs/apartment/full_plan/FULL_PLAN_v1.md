# Apartment 1122: full tidy plan for one continuous episode

Generated 2026-11-18 21:28 by `C:/Users/raresense/sim_home/apartment/full_plan/make_full_plan.py` (rerun: `py -3.12` on that file, about 10 s).
**Nothing in this file is a simulation result.** Every reach and grasp judgement is by geometry, not verified. Coordinates are the pack's scene frame; the episode's world frame is scene - (0.90, 0.45).

## Counts
- Loose objects in the pack: 198 (+ our added rubbish bin).
- Mess to move: 69 (25 planned in the route, 44 skipped). Mess left on purpose: 13. Already in place: 47. Furniture, appliances and things where they belong: 69.

| Class | all | mess planned | mess skipped | left / in place |
|---|---|---|---|---|
| container | 51 | 5 | 6 | 40 |
| dish | 31 | 3 | 10 | 18 |
| paper | 12 | 1 | 11 | 0 |
| toy | 12 | 8 | 3 | 1 |
| bag | 10 | 0 | 1 | 9 |
| appliance | 8 | 0 | 0 | 8 |
| shoe | 8 | 3 | 4 | 1 |
| textile | 7 | 4 | 1 | 2 |
| plant | 5 | 0 | 0 | 5 |
| electronics | 4 | 0 | 0 | 4 |
| food | 4 | 0 | 1 | 3 |
| cable | 4 | 0 | 0 | 4 |
| table | 4 | 0 | 0 | 4 |
| cushion | 3 | 0 | 0 | 3 |
| clothing | 3 | 0 | 2 | 1 |
| basket | 3 | 0 | 0 | 3 |
| cookware | 3 | 0 | 0 | 3 |
| food_package | 3 | 0 | 1 | 2 |
| tool | 3 | 0 | 1 | 2 |
| toy_vehicle | 3 | 0 | 0 | 3 |
| book | 3 | 0 | 0 | 3 |
| decor | 2 | 0 | 0 | 2 |
| package | 2 | 0 | 2 | 0 |
| stool | 2 | 0 | 0 | 2 |
| umbrella | 2 | 1 | 0 | 1 |
| rug | 1 | 0 | 0 | 1 |
| lamp | 1 | 0 | 0 | 1 |
| kitchenware | 1 | 0 | 0 | 1 |
| hook_rack | 1 | 0 | 0 | 1 |
| stroller | 1 | 0 | 0 | 1 |
| cutlery | 1 | 0 | 1 | 0 |

| Destination | planned | skipped | where the robot stands / reach (by geometry, not verified) |
|---|---|---|---|
| r186i1_basket | 9 | 5 | marginal: the pelvis can stand 0.17 m from it; low shelf: deep squat and a level reach into the cubby (now, before anything is cleared: 0.35 m) |
| floor beside r186i1_basket / r185i1_megabloks_bag (toy corner) | 2 | 0 | floor spots beside the toy basket |
| rubbish_bin | 1 | 12 | yes: the pelvis can stand 0.02 m from it (now, before anything is cleared: 0.38 m) |
| r133i1_laundry_basket | 4 | 2 | marginal: nearest standing place is 0.47 m from it: needs a trunk lean over the furniture (ASSUMED limit 0.45 m without) (now, before anything is cleared: 0.83 m) |
| r27i1_sink | 5 | 14 | no: nearest standing place is 1.38 m from it (ASSUMED reach 0.6 m at most) |
| r119i1_mat | 3 | 4 | marginal: the pelvis can stand 0.22 m from it; low shelf: deep squat and a level reach into the cubby (now, before anything is cleared: 0.81 m) |
| r110i1_console | 1 | 2 | no: nearest standing place is 0.64 m from it (ASSUMED reach 0.6 m at most) (now, before anything is cleared: 1.26 m) |
| r35i1_top | 0 | 2 | no: nearest standing place is 0.63 m from it (ASSUMED reach 0.6 m at most) |
| r94i1_tray_table | 0 | 3 | marginal: nearest standing place is 0.48 m from it: needs a trunk lean over the furniture (ASSUMED limit 0.45 m without) |

| Skill needed (planned things) | count | state today |
|---|---|---|
| floor_pick | 13 | exists: proven on one toy piece (run 1118_193303); top-down only |
| cloth_pick | 5 | being built by the cloth agent (E:/urc_cloth); no clean pick yet |
| surface_pick | 7 | NOT BUILT (no pick from furniture exists) |
| surface_pick, counter 0.91-0.95 m (standing, hand at chest height) | 1 | not built |
| surface_pick, low table / seat 0.45-0.56 m (half squat) | 5 | not built |
| surface_pick, table / sill 0.72-0.78 m (standing) | 1 | not built |
| put: drop_in_sink (lower into the basin) | 5 | NOT BUILT (place into the sink) |
| put: place_on (set on a table) | 1 | NOT BUILT (place_on a table) |
| put: drop_in | 5 | drop_in: ran in the practice room only; the hamper rim is 0.65 m |
| put: put_down (lower into a low basket) | 9 | exists: proven once (toy piece into the toy basket) |
| put: put_down (set on the mat) | 3 | put_down on a flat mat: written, not run yet |
| put: put_down (set on the floor) | 2 | put_down on the floor: written, a flat destination is not run yet |
| needs_two_hands | 3 | not built (big garments, things over 1 kg) |
| container_carry | 0 carries | not built |
| needs_door_or_drawer_open | 0 planned | not built; the one thing that needs it (milk jug to the fridge) is left |

Grasp by geometry over the 69 mess things: yes 36, marginal 6, no 27. Reach: no 24, marginal 5, yes 27, after clearing 13.

## Skipped mess, and why
- r105i1_shoe (shoe, to r119i1_mat): not reachable: no pick stance even with every movable thing gone: blocked by no way there (cut off), r103i1_red_bag, r104i1_grocery_bag
- r105i2_shoe (shoe, to r119i1_mat): not reachable: no pick stance even with every movable thing gone: blocked by no way there (cut off), r103i1_red_bag, r20i1_baseboard
- r108i1_scissors (tool, to r110i1_console): not graspable: too thin: 0.9 cm high, nothing above the surface for the pads to bite
- r122i1_croc (shoe, to r119i1_mat): NO free place left on the mat for this pair (lamp base and the other pairs fill it): set beside the mat
- r123i1_slipper (shoe, to r119i1_mat): NO free place left on the mat for this pair (lamp base and the other pairs fill it): set beside the mat
- r146i1_bowl (dish, to r27i1_sink): not graspable: too wide: no part under 8 cm (narrowest silhouette 20 cm) and no rim, neck or strap section the open jaws can come down over
- r148i1_pink_lid (dish, to r27i1_sink): not graspable: too wide: no part under 8 cm (narrowest silhouette 12 cm) and no rim, neck or strap section the open jaws can come down over; flat on a surface: would need a slide-to-the-edge pinch (no such skill)
- r149i1_pouch (food_package, to rubbish_bin): not graspable: too wide: no part under 8 cm (narrowest silhouette 10 cm) and no rim, neck or strap section the open jaws can come down over; flat on a surface: would need a slide-to-the-edge pinch (no such skill)
- r151i1_spoon (cutlery, to r27i1_sink): not graspable: too thin: 0.8 cm high, nothing above the surface for the pads to bite
- r152i1_sippy_cup (container, to r27i1_sink): not reachable: nearest standing place is 0.62 m from it (ASSUMED reach 0.6 m at most)
- r156i1_clementines (food, to r35i1_top): not graspable: too wide: no part under 8 cm (narrowest silhouette 20 cm) and no rim, neck or strap section the open jaws can come down over
- r157i1_paper (paper, to rubbish_bin): not graspable: too thin: 0.7 cm high, nothing above the surface for the pads to bite
- r157i2_paper (paper, to rubbish_bin): not graspable: too thin: 0.7 cm high, nothing above the surface for the pads to bite
- r171i1_glass (dish, to r27i1_sink): not graspable: too wide: no part under 8 cm (narrowest silhouette 8 cm) and no rim, neck or strap section the open jaws can come down over
- r173i1_tumbler (dish, to r27i1_sink): not reachable: no pick stance even with every movable thing gone: blocked by r175i1_cardboard_box, r169i1_two_tier_table, r20i1_baseboard
- r174i1_plush (toy, to r186i1_basket): not reachable: no pick stance even with every movable thing gone: blocked by brick_wall, r169i1_two_tier_table, r175i1_cardboard_box
- r176i1_cap (clothing, to r110i1_console): not graspable: too wide: no part under 8 cm (narrowest silhouette 19 cm) and no rim, neck or strap section the open jaws can come down over
- r177i1_bowl (dish, to r27i1_sink): not graspable: too wide: no part under 8 cm (narrowest silhouette 12 cm) and no rim, neck or strap section the open jaws can come down over
- r179i1_toy_pouch (bag, to r186i1_basket): not graspable: too wide: no part under 8 cm (narrowest silhouette 10 cm) and no rim, neck or strap section the open jaws can come down over
- r182i1_bottle (container, to r35i1_top): not reachable: nearest standing place is 0.84 m from it (ASSUMED reach 0.6 m at most)
- r183i1_cup (dish, to r27i1_sink): not graspable: too wide: no part under 8 cm (narrowest silhouette 8 cm) and no rim, neck or strap section the open jaws can come down over
- r189i1_santa_hat (clothing, to r133i1_laundry_basket): not reachable: no pick stance even with every movable thing gone: blocked by r189i1_santa_hat, r145i1_base
- r191i1_toy_vehicle (toy, to r186i1_basket): not graspable: too wide: no part under 8 cm (narrowest silhouette 10 cm) and no rim, neck or strap section the open jaws can come down over
- r193i4_toy_piece (container, to r186i1_basket): never became reachable in the route
- r195i1_paper (paper, to rubbish_bin): not graspable: no section the open jaws can come down over from above (floor picks are top-down only)
- r195i2_paper (paper, to rubbish_bin): not graspable: no section the open jaws can come down over from above (floor picks are top-down only)
- r195i3_paper (paper, to rubbish_bin): not graspable: no section the open jaws can come down over from above (floor picks are top-down only)
- r196i1_plastic_bag (paper, to rubbish_bin): not graspable: too thin: 1.4 cm high, nothing above the surface for the pads to bite
- r63i1_glass (dish, to r27i1_sink): not graspable: too wide: no part under 8 cm (narrowest silhouette 8 cm) and no rim, neck or strap section the open jaws can come down over
- r68i1_rag (textile, to r133i1_laundry_basket): not reachable: no pick stance even with every movable thing gone: blocked by no way there (cut off), r32i1_door, r29i1_oven_door
- r69i1_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high, nothing above the surface for the pads to bite
- r69i2_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high, nothing above the surface for the pads to bite
- r69i3_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high, nothing above the surface for the pads to bite
- r69i4_scrap (paper, to rubbish_bin): not graspable: too thin: 0.5 cm high, nothing above the surface for the pads to bite
- r71i1_lysol (container, to r94i1_tray_table): not reachable: nearest standing place is 0.85 m from it (ASSUMED reach 0.6 m at most)
- r78i1_kids_bottle (container, to r27i1_sink): not reachable: nearest standing place is 0.94 m from it (ASSUMED reach 0.6 m at most)
- r83i1_sponges (package, to r94i1_tray_table): NO free place of 22 x 8 cm left on r94i1_tray_table: something there has to be moved together first
- r83i2_sponges (package, to r94i1_tray_table): not reachable: nearest standing place is 0.67 m from it (ASSUMED reach 0.6 m at most)
- r87i1_wrapper (paper, to rubbish_bin): not graspable: only 4.0 cm high and no top-down section: nothing for the pads
- r89i1_salad_bowl (dish, to r27i1_sink): not graspable: too wide: no part under 8 cm (narrowest silhouette 25 cm) and no rim, neck or strap section the open jaws can come down over
- r90i1_plate (dish, to r27i1_sink): not graspable: too wide: no part under 8 cm (narrowest silhouette 27 cm) and no rim, neck or strap section the open jaws can come down over; flat on a surface: would need a slide-to-the-edge pinch (no such skill)
- r91i1_tan_plate (dish, to r27i1_sink): not graspable: too wide: no part under 8 cm (narrowest silhouette 27 cm) and no rim, neck or strap section the open jaws can come down over; flat on a surface: would need a slide-to-the-edge pinch (no such skill)
- r92i1_pink_container (container, to r27i1_sink): not reachable: nearest standing place is 0.96 m from it (ASSUMED reach 0.6 m at most)
- r93i1_nugget (toy, to r186i1_basket): not reachable: nearest standing place is 0.98 m from it (ASSUMED reach 0.6 m at most)

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
- r117i1_blanket: clear r116i1_coat_pile first
- r120i1_duck: clear r117i1_blanket, r116i1_coat_pile first
- r190i1_stocking: clear r191i1_toy_vehicle first
- r192i1_ball: clear r193i3_toy_piece, r193i1_toy_piece, r193i4_toy_piece, r189i1_santa_hat, r190i1_stocking, r193i2_toy_piece, r195i1_paper first
- r193i1_toy_piece: clear r193i3_toy_piece, r192i1_ball, r190i1_stocking, r189i1_santa_hat, r193i4_toy_piece, r193i2_toy_piece, r195i1_paper first
- r193i2_toy_piece: clear r188i1_dollhouse first
- r193i3_toy_piece: clear r189i1_santa_hat, r191i1_toy_vehicle first

Planned with a marginal grasp or reach (expect failures here first):
- r130i1_light_saber: grasp: the section is 10 cm off the thing's middle: it can swing or tip in the jaws (the light saber slipped out this way in a live run)
- r81i1_glass_spoon: grasp: only a top-down section, and its top is 1.10 m up: the wrist would have to be about 1.20 m high (ASSUMED limit 1.05 m); reach: nearest standing place is 0.56 m from it: needs a trunk lean over the furniture (ASSUMED limit 0.45 m without)

## Route (one episode)
Chosen: toy basket carried to the rug toys: no; bin carried to the living room: no. Whole-route time with the stated speeds for the four ways: basket carried, bin carried: 35 min; basket carried, bin stays: 33 min; basket stays, bin carried: 33 min; basket stays, bin stays: 31 min.
Toy basket spot on the rug (scene): (-2.90, -1.95). Bin spot in the living room (scene): (-3.75, -0.05).

| # | Step (runner form) | What | Items | Walk empty / carrying m | s (stated speeds) | Runs today? |
|---|---|---|---|---|---|---|
| 1 | `garments` | entry, kitchen, hall: garments to the hamper (big ones one per trip, two hands) | 4 | 32.07 / 41.02 | 496 | no: the CLOTH agent's runner form (E:/urc_cloth/scripts/home/cloth_episode.py); one merged runner for cloth + rigid in the same episode does not exist yet |
| 2 | `tidy_all` | east: shoes to the doormat in pairs | 1 | 10.74 / 1.81 | 62 | no: runner form exists; put_down on the flat mat with a target spot per shoe is NOT run yet (pair spots need a new option) |
| 3 | `tidy_all` | entry: small things to the console table | 1 | 2.15 / 2.15 | 45 | no: runner form exists but tidy_all skips destinations on furniture: place_on is NOT BUILT |
| 4 | `tidy_surface` | kitchen: used dishes from the island and the counter to the sink | 1 | 6.24 / 0.55 | 47 | no: NEW step type: pick from furniture (surface_pick) + drop_in_sink (lower into the basin); floor and cloth things in the list go through their own skills |
| 5 | `tidy_all` | crossing west: the east half's toys ride along to the toy basket at its home | 1 | 6.1 / 9.77 | 96 | YES |
| 6 | `tidy_surface` | toy corner: toys near the basket's home into it | 2 | 0.62 / 5.19 | 90 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower into a low basket); floor and cloth things in the list go through their own skills |
| 7 | `tidy_surface` | rug and side table: toys to the basket at its home (two per trip) | 1 | 8.4 / 8.4 | 97 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower into a low basket); floor and cloth things in the list go through their own skills |
| 8 | `tidy_all` | rug: the two big toys to the toy corner (one per trip) | 2 | 7.51 / 7.51 | 114 | no: runner form exists; needs a per-object destination spot on the floor (new option) |
| 9 | `tidy_surface` | living room: rubbish to the bin at its home (two per trip) | 1 | 3.69 / 10.05 | 92 | no: NEW step type: pick from furniture (surface_pick) + drop_in; floor and cloth things in the list go through their own skills |
| 10 | `tidy_all` | living room: the pair of flats to the doormat | 2 | 5.74 / 10.15 | 125 | no: runner form exists; put_down on the flat mat with a target spot per shoe is NOT run yet (pair spots need a new option) |
| 11 | `tidy_surface` | living room: used dishes to the sink (two per trip, the long way) | 4 | 11.42 / 34.35 | 332 | no: NEW step type: pick from furniture (surface_pick) + drop_in_sink (lower into the basin); floor and cloth things in the list go through their own skills |
| 12 | `tidy_surface` | left-overs that waited for a neighbour: to r186i1_basket | 5 | 19.36 / 11.63 | 262 | no: NEW step type: pick from furniture (surface_pick) + put_down (lower into a low basket); floor and cloth things in the list go through their own skills |

The exact step list (names in order, pairs adjacent) is in `route_steps.json`; per-object trips and seconds are in `full_plan.json`.
Step forms: `tidy_all` is the floor agent's (E:\urc_home\scripts\home\episode.py); `garments` is the cloth agent's (E:\urc_cloth\scripts\home\cloth_episode.py). NEW step types this plan needs: `carry` (a container, two hands), `tidy_surface` (pick from furniture; place on a table, a counter, into the sink). Also needed in the runner: one episode that mixes rigid and cloth steps, a destination PER OBJECT with a target spot (the room file maps a class to one place; `room_patch.json` holds the per-object table), and two per trip across neighbouring destinations.

## Time for the whole apartment
- Things moved: 25 in 20 trips, + 0 container carries. Planned walking: 114 m empty-handed, 143 m carrying.
- Today, with the stated speeds (0.45 m/s empty, 0.18 m/s carrying, pick 16 s, put-down 12 s) and the robot walking exactly the planned legs: **31 min** (74 s a thing).
- Today, at the end-to-end rates measured in run 1118_204943 (B2: 4.2 m of legs in 36 s empty, 7 m in 111 s carrying, pick 18 s, put-down 20 s): **70 min** (168 s a thing). This is what the code as committed would do, if nothing failed.
- At the target of 20-30 s a thing (container carries at 0.45 m/s on top): **8 min to 12 min**.
- Not in these numbers: failed grasps and second tries, falls, the scene settling at the start, compute time (the CPU path ran about 0.6x real time with recording).

## Top risks
- Most of the plan needs skills that do not exist: of the planned things only the floor toys into the toy basket use skills proven in a clean episode (one toy piece, 176 s). Surface picks, placing on tables / counters / into the sink, the container carry and the cloth pick are not built or not proven.
- The living room is far from the kitchen: used dishes travel about 9-10 m each, two per trip. At today's carrying speed this is the largest block of time. A dish caddy (a movable box carried once) would cut it but needs two-hand carrying of about 2.5 kg, over the 1.5 kg limit; not planned.
- Reach onto furniture is ASSUMED (0.45 m from the pelvis, 0.60 m with a lean); no reach map exists for standing or half-squat picks at 0.45-0.95 m. Things in the middle of the island, at the back of the counter and on the window sills behind the armchair and the gold table depend on it.
- The sink is in the corner behind the open dishwasher door and racks; no: nearest standing place is 1.38 m from it (ASSUMED reach 0.6 m at most). Four paper scraps lie on the floor exactly there and cannot be picked up (0.5 cm thin): the feet must be allowed to step on them.
- The doormat is half covered by the floor lamp's base; only the free part is used for the shoes: r124i1_sandal: (2.35, -1.97); r105i1_shoe: (2.28, -1.72); r105i2_shoe: (2.40, -1.72); r125i1_flat: (2.05, -1.72); r125i2_flat: (2.16, -1.72); r122i1_croc: NO SPOT; r123i1_slipper: NO SPOT.
- The toy basket is small (33 x 27 x 12 cm, about 10 litres) and already holds a plush: 9 more toys are planned into it. It will be heaped; overflow goes into the megabloks bag beside it (TIDY_PLAN). Carrying a heaped basket can spill.
- Walking distances are planned on the floor as it is AFTER the mess is gone; early trips are a little longer. Things moved to their places (shoes on the mat, a basket on the rug) are not put back into the map as new obstacles.
- Garments: the cloth pick is assumed to work for all seven; the three big ones (jacket, coat pile 1.4 kg, blanket) are assumed to need both hands and one trip each. The coat pile is the first thing that must go: it covers the mat and blocks the console.
- Heavy or off-centre grasps are marked marginal (pad friction alone, 6 N a pad measured): clementines 1.0 kg, salad bowl 0.9 kg, dollhouse 0.8 kg, lysol 0.75 kg, light saber held off its middle.
- A one-hour-plus episode with 198 loose bodies is beyond what the simulator has run: the full loose set ran under 0.02x real time on the GPU path; the room file must keep only the planned things loose (`room_patch.json`).

## Assumptions (all of them)
- Source of truth for names, classes, masses, positions and sizes: D:\apartment_real\mujoco\unzipped (scene_spec.json, environment.xml), read only. Grasp sections and footprints come from the collision meshes at their start poses (the light saber and the santa hat move a little when the scene settles).
- Grasp: the floor agent's top-down section search (grasp_geom.find, unchanged): a section at most 7.0 cm wide with pad bite. For things on furniture a side-on grasp is also allowed when the narrowest silhouette is under 7.9 cm and the thing is at least 4 cm high; top-down on furniture only when the thing's top is under 0.95 m. The jaws open 7.9 cm between the pad faces in the model (the brief says 8.2 cm).
- Mass: over 1.5 kg not carried; 0.8-1.5 kg marginal.
- Garments (7) are cloth and count as graspable by a pinch; their rigid drape shapes are used only as footprints.
- Floor reach: a pick stance as skills.stance_for builds it (thing 0.17 m ahead and 0.27 m to the side of the standing pelvis, pelvis 0.28 m from furniture and 0.16 m from small things, knees 12 cm clear of anything over 15 cm, feet 4 cm clear of floor things, 12 headings, both hands), checked on a 5 cm grid. Cords, the strap and the mats are walked over, as in the floor agent's room file.
- Furniture reach: the pelvis may stand 0.22 m from furniture; a thing within 0.45 m of such a place counts as reachable, within 0.6 m marginal. NOT measured.
- Dishes on the coffee table, side table, two-tier table, sills, island and the right counter are taken as used and go to the sink; dishes in the open dishwasher racks, at the sink and beside the dish basket are taken as in place. The sink is assumed to take 16 small dishes.
- Flat papers on the sofa and the empty pouch are rubbish (TIDY_PLAN). Snack bags, the juice box, the chips can and the paper bag in the kitchen are food or storage, not rubbish.
- Books are already stacked and stay; the remote stays on the two-tier table; keyboard, mouse and notebook stay on the window sill (deviation from TIDY_PLAN's 'books and remote on the coffee table': nothing is gained by moving them and flat books cannot be grasped).
- Santa hat to the hamper and stocking to the toy basket, as TIDY_PLAN classes them.
- Cleaning things from the island go to the tray table beside the mop; the cap, scissors and small umbrella go to the console table (my choice of place; TIDY_PLAN names the console for scissors and umbrella).
- Doors, drawers and lids stay as they are (frozen in our model): nothing is put into the fridge, cabinets, drawers, the ottoman or the lift-top table; the dishwasher stays open.
- Times: floor pick 16 s and put-down 12 s (run B) or 18 s and 20 s (run B2) are measured; cloth pick 30 s (45 s two hands), surface pick 20 s, drop into bin / hamper 8 s, into the sink 10 s, place on a table 12 s, container pick-up 25 s and set-down 15 s are GUESSES. A second thing in a trip costs its own pick and put. A trip's time is shared equally by its things.
- Route: the zone order is fixed by hand (east half first because the robot starts there and the coat pile must leave the mat first; then the crossing west with the east toys; the living room; last the things that leave the living room). Inside a block the nearest available thing is next and the second hand takes a thing within 3 m going to the same place (the runner's own rule). The four ways (basket carried or not, bin carried or not) are all computed and the fastest by the stated speeds is taken. Not a proven optimum.
- Things moved in one trip with two hands (big garments, anything over 1 kg) travel alone.

## Files
- `C:\Users\raresense\sim_home\apartment\full_plan\full_plan.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\route_steps.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\room_patch.json`
- `C:\Users\raresense\sim_home\apartment\full_plan\FULL_PLAN.md`
- `C:\Users\raresense\sim_home\apartment\full_plan\make_full_plan.py`
- `C:\Users\raresense\sim_home\apartment\full_plan\nav_snapshot.py`
- `C:\Users\raresense\sim_home\apartment\full_plan\grasp_geom_snapshot.py`
