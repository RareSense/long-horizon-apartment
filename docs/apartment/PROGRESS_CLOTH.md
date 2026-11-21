# Apartment 1122: garments as real cloth (cloth agent, AI-operated)

Code: worktree E:\urc_cloth, branch home-cloth (from home-cleaning 0a25cbe; local commits only, never pushed).
Isaac slot "cloth" = the SECOND slot, port 47970. Runs: C:\Users\raresense\sim_home\runs\<MMDD_HHMMSS>_<tag>\.
Session scene files of this checkout: C:\Users\raresense\sim_home\_cloth\ (URC_HOME_OUT), logs in _cloth\_logs\,
live scratch scripts in _cloth\live\ (l00_*.py ...: what was sent to the session, in order).
Do not edit E:\urc_home (the home-cleaning agent's worktree) and do not use ports 47960-47969.

## How to run
- Start a live session:  py -3.12 E:\urc_cloth\scripts\home\c_live.py start 47970   (takes ISAAC_SLOT2.lock as "cloth" when 9 GB
  RAM are available; sets URC_NEWTON_CPU=1, URC_QP_SOLVER=daqp, URC_HOME_OUT). Guard: `c_live.py guard 47970` (stops OUR
  Isaac under 3 GB available RAM). Stop: `c_live.py stop 47970`.
- Load the apartment with garments as cloth, live (no task): send a file with
    ROOM = r'E:\urc_cloth\rooms\apartment_1122_cloth.json'; RUN = r'<new run folder>'; TASK = []; LIVE = True
    CLOTH_NAMES = None   # or a list of garment names
    exec(open(r'E:\urc_cloth\scripts\home\cloth_episode.py', encoding='utf-8').read())
  with  py -3.12 E:\urc_cloth\scripts\isaac_cmd.py --port 47970 file.py
- Headless cost check without Isaac:  D:\isaacsim62\python.bat E:\urc_cloth\scripts\home\cloth_bench.py

## What exists
- src\urc\tasks\home\cloth.py: garment patterns (rag, blanket, knit hat, santa hat, stocking, jacket, coat) as flat
  panels (two-layer garments sewn at the seams), lay() (gathered into the rigid drape's footprint), heightfield_solid(),
  ClothWorld (Newton SolverStyle3D, towel material, cm/g/s inside; colliders copied from MuJoCo data each cloth step;
  the step is a captured CUDA graph; sleep / wake; hold groups; pad_load / caught / ring / follow_grip).
- src\urc\tasks\home\apartment.py: structure.cloth = [names] leaves those rigid drapes out of OUR merged model and
  reports where they lay in info["cloth"]. D:\apartment_real is never changed.
- rooms\apartment_1122_cloth.json: phase-1 room with the 7 garments as cloth.
- scripts\home\cloth_skills.py: session code (cloth_setup, drawn meshes, step hook, force-limited squeeze, helpers).
- scripts\home\cloth_episode.py: episode frame (boot + skills + trace of the home-cleaning work exec'd unchanged).

## Answer to the first question (18 Nov, run 1118_203859_live_cloth_coupling)
Style3D cloth runs beside the fast CPU rigid path. Per physics step, robot standing, full apartment:
no cloth awake 1.06 ms (video 2.73); 1 garment awake 1.29 ms (video 2.82); all 7 awake 7.2 ms (video 9.45);
all 7 asleep 1.15 ms (video 2.68). One world per garment + sleep is therefore essential. timing_stage1.json / 2.json.

## Facts found
- The laundry basket r133 is a CLOSED hamper (domed top 0.58-0.60 m, handles to 0.66 m, one solid convex block).
  Nothing can fall inside. Asked the coordinator: (a) lay garments on top, or (b) our own open-top hamper.
- Drop stance at r133 exists for both hands (stance_for with the basket ignored), e.g. left: (-2.145, -1.561, -120 deg).
- With both Isaac sessions up only 4 - 4.5 GB RAM stay available.

## Next
1. Live: knit hat r131 (world (-1.30, -0.05)): crouch, pads onto it, force-limited close, caught(), hold, lift, stand.
2. Carry to r133, drop, check. 3. Skill functions + regression episode + SKILLS.md. 4. The other six garments.

## 18 Nov, about 23:45 (second cloth agent, took over at 23:00; AI-operated)
State: E:\urc_cloth branch home-cloth, commits 3fd8f04 (stopped agent's work: hat run code) and 3361c61 (below). Never pushed.
Live session tools of mine: C:\Users\raresense\sim_home\_cloth\live\m*.py (m00/m20/m30 setup = load the room LIVE;
m22_garment.py with NAME + STEP "grasp" | "drop"; m32_reload.py re-execs cloth_skills.py into the running session).
Send with: py -3.12 E:\urc_cloth\scripts\isaac_cmd.py --port 47970 FILE   or  -c "NAME='...'; STEP='grasp'; exec(open(r'...m22_garment.py').read())"
Write live files with the Write tool (a PowerShell Set-Content file has a BOM and the session refuses it).

### Garments, per garment (live, this session)
- knit hat r131: DONE (run 1118_212840_hat_to_hamper, recorded, video check passes).
- jacket r121: IN the hamper live (run 1118_231249..., grasps\009_r121i1_jacket_in_container_from_above.jpg). First try (run
  1118_230207) it was let go OUTSIDE: hung 0.66 m under the pads, the arm reaches 1.0 m with fingers down, the hamper
  rim is 0.59 m; the front stance put the hand (carry place 0.26 ahead) over the hamper while walking in, so the jacket
  hung against the near wall. FIX in drop_in_cloth: side stance (hamper beside the robot, wall SIDE_CLEAR from the
  pelvis), hand raised at its carry place to rim + hang + 6 cm (max Z_HIGH 1.32 m, orientation free; measured live:
  pads reach 1.30-1.40 m at 0.30-0.38 m ahead, pelvis tilt 0.2 rad), over the opening, lowered to rim + 12 cm, open.
  NOT yet in a recorded episode.
- TWO FALLS, same cause (runs ..._230207_..._FELL..., ..._231249_..._FELL...): after a drop, rest_hands let the arm hang
  and the hand lay on the hamper rim (left hand stayed at 0.55 m, right dropped to 0.44); the first turn on the spot
  pushed the robot over. FIX: the hand goes back to its carry place above the rim before resting; SIDE_CLEAR 0.40.
  NOT yet seen working after the fix (the next session fell before the fix was in).
- coat pile r116: FAILED (attempt 1, run 1118_232126): two closings on its flat sleeve end (0.8, -1.95) caught nothing
  (pads 6.9 mm up, jaws closed to 1-2 mm, 3.4 N: no cloth between the pad faces). Its folds (5-10 cm thick) are in the
  middle at x 1.0-1.35, y -2.55..-1.9, against the shoe shelf / wall: NO pick stance reaches any of them, even after
  stepping back to open floor (0.30, -1.00). Grasp point choice now prefers folds (relief over 2 cm), not yet run.
- blanket r117: no pick stance (the coat pile and the mat things are in the way); not tried.
- santa hat r189, stocking r190: no pick stance while the rug toys lie round them (toy pieces r193i2/i3/i4, ball r192,
  toy vehicle r191: the floor agent's items). The pelvis cannot get within reach. Not tried.
- rag r68: cut off (kitchen corner behind the frozen oven door r29 and door r32). Not tried.

### Code (commit 3361c61)
- cloth_skills.py: drop_stance(name, container, side, high), drop_in_cloth front / side-high modes, hand back to carry
  place before resting, fold-preferring grasp points (k=30, relief penalty).
- apartment.py: structure.hollow = hollow_colliders.json (planning work) swaps solid cup/glass/bowl hulls for wall boxes
  in our merged model. rooms\apartment_1122_cloth_surfaces.json uses it, with the living-room, sill and counter things loose.
- Coordinator: rim pinches only with the hollow colliders (now loadable; check a close-up first); grasp geometry v2 in
  C:\Users\raresense\sim_home\apartment\full_plan\grasp_types.py (verify each type live and write back "verified in sim").

## 18 Nov, about 23:40 (AI-operated)
- RAM emergency 23:28-23:30: a planning-agent script (scratchpad\gplan\dex3.py, 12.5 GB) took all RAM; the coordinator killed it.
- Third fall (run 1118_233032_live_surface1_FELL_...): with SIDE_CLEAR 0.40 the stepping into the side stance held the
  side step at its 0.04 limit for 7 s carrying the jacket and the robot tipped. SIDE_CLEAR back to 0.30 (the stance that
  walked in fine in run 1118_231249); the after-drop hand fix stays. Not yet seen live after the fix.
- Hollow colliders loaded through the room builder (structure.hollow) and checked live (run 1118_233032): cup r138 has 8
  wall boxes 4 mm thick + floor plate, inside clear (top-view plot m41_cup_boxes.png), it stands still (0.0 mm in 1 s).
  The five dishwasher-rack cups r66 are in too (leave out with hollow_skip in the episode room). Step cost with 69 loose
  things + hollow colliders, robot standing, garments asleep, recording: 3.2-3.5 ms per 2 ms step (37 loose: 2.7 ms).
- scripts\home\surface_skills.py (new, NOT yet run live): surface_pick (top-down section, stance with the thing
  SURF_X ahead, posture by pad height), place_into, sink_basin, drop_in_sink.
- Kitchen geometry (world, from the inventory): sink r27 x 3.56-4.25, y 1.21-1.90, basin 0.67-0.88 m; dishwasher tub r32
  x 2.82-3.40, y 1.43-2.05; its OPEN door lies flat x 2.82-3.40, y 0.71-1.43, z 0.05-0.13; counter right arm from x 3.76;
  range x 3.75-4.40, y 0.03-0.78. The only floor gap beside the open door is 0.36 m wide (x 3.40-3.76): no stance.

## 19 Nov, about 00:15: FURNITURE REACH MAP (planner hook reads this path)
C:\Users\raresense\sim_home\apartment\reach\furniture_reach_map.json  (summary per height band; details in
furniture_reach_map_fingers_down.json and furniture_reach_map_side_on.json beside it). Measured live, free space, left hand,
run C:\Users\raresense\sim_home\runs\1118_233733_live_surface2 (probes scripts\home\live\s10_reach_probe.py, s11_reach_probe_side.py;
summary scripts\home\reach_map_summary.py). Reached = pads within 1 cm across / 1.5 cm in height; the pelvis moves 2-4 cm
back as the arm reaches (counter-balance), accepted.
- Low table / seat (pads 0.50-0.55): fingers down only, half squat (-0.12, lean 0.45): 0.25-0.33 m ahead, 0.12-0.28 side.
  Side-on in that squat stays 2-5 cm too high. Standing cannot get the pads down to 0.55.
- Table / sill (pads 0.78-0.80): fingers down 0.33 only (standing, lean 0.3); side-on 0.33-0.41 standing, 0.49 with lean 0.3.
- Counter (pads 0.95-1.00): fingers down NOT reached at 1.00 m; side-on 0.33-0.49 standing, 0.57 (side 0.12) with lean 0.3.
- Planner meaning: things deeper than (reach - 0.22 m pelvis-to-edge) from a furniture edge are out of reach; the
  plan's ASSUMED 0.45 / 0.60 holds only side-on at counter height.
Commit 7th of the branch (git log): surface_skills.py (surface_pick / place_into / drop_in_sink, NOT yet run),
apartment.py structure.unfreeze + fixed extras (sink basin collider from room_patch.json), room file regenerated.
Dishwasher (to close it): door r32 hinge at (3.11, 1.432, 0.11) axis +x, range -1.571..0 (0 = open, as authored), 5 kg,
damping 0.8, NO spring: lifting the free edge needs about 25 N at horizontal. Racks r33i1 (upper, z 0.48-0.63) and r33i2
(lower, z 0.17-0.31) slide along +y, ranges 0..0.40 / 0..0.35, 1.6 kg, damping 2, pulled out 0.33 / 0.28 m over the open
door. The 9 dishes in the racks (r65 bowls, r66 cups) are FROZEN in our room: they must be made loose or a pushed rack
stops against them. The racks can only be pushed from beside the door (x <= 2.54, the open leaf fills the front).

## 19 Nov, coordinator note (planner hook)
Rows for the planner's measured_reach_map() hook (both probes of run 1118_233733_live_surface2 merged, one row per probe point, "grip" = fingers_down / side_on):
C:\Users\raresense\sim_home\apartment\reach\planner_reach_rows.json

## 19 Nov, about 00:35: HAND-OVER (cloth agent stopping: working memory used up). READ THIS FIRST.
My Isaac is stopped and slot "cloth" is free. Code: E:\urc_cloth branch home-cloth, last commit 005e1ab (all committed, never pushed).
Run folders renamed: ..._1118_232126_live_garments4_coat_pile_two_empty_closings_on_a_flat_sleeve,
..._1118_233733_live_surface2_reach_maps_and_first_surface_pick.

### Seen working live (frames looked at)
- First SURFACE PICK: kids bottle r155 from the coffee table (top-down at the neck, pads 0.643 m, 0.37 m ahead, half
  squat -0.12 / lean 0.45, right hand), first try, 6.2 / 5.8 N, rose 5.8 cm, 64 s sim from the start pose.
  Pictures: run ...surface2...\grasps\00_object_0283_body_surface_try1.jpg, m53_object_0283_body_after_pick.jpg.
- Jacket into the hamper with the side-stance high drop (run 1118_231249..., grasps\009_...from_above.jpg).
- Reach maps (section above). Hollow cup collider close-up (run ...233032..., m41_*).
### Failed / faults found (fixed in code where said, fixes NOT yet seen live)
- After the pick, stand_with took the hand to 0.64 m and set the bottle back on the table (FIXED: carry height = support
  + hang + 8 cm before standing, commit 005e1ab, not run).
- place_into onto the coffee table: the hand was 3.3 cm off; the bottle stood half over the table edge and fell to the
  floor when let go (FIXED: support check, place only if the base stands on the top with 1 cm spare, commit 701071a, not run;
  STILL NEEDED: choose the spot from the furniture top, base radius + 3 cm inside the edge; with fingers-down reach of
  0.33-0.37 m and the pelvis 0.22-0.28 m from the edge this is at the limit: use the side-on hand for placing).
- Three falls this session (two: hand resting on the hamper rim, then a turn; one: 7 s of side steps at the limit
  stepping into the 0.40 side stance with the jacket). Coordinator: avoid long side-stepping with a load until the
  floor agent's walking fix lands (it will message; merge it from home-cleaning then).
### Garments (per garment)
knit hat DONE (recorded, 1118_212840) | jacket IN live, no recorded proof yet | coat pile FAILED (flat sleeve end; folds
out of reach) | blanket, santa hat, stocking: no pick stance until the coat pile / rug toys are gone (not tried) |
rag: cut off behind the frozen oven door and door r32 (not tried).
### Next, in the coordinator's order
1. Fresh session with rooms\apartment_1122_cloth_surfaces.json (now has the sink basin collider + dishwasher joints
   unfrozen; NOT yet loaded live: check the basin in a close-up and that the door stays open at the start).
2. Make the 9 rack dishes (r65i1-4 bowls, r66i1-5 cups) loose in that room (structure.free) before pushing the racks.
3. Close the dishwasher: push the racks in from beside the door (stand x <= 2.54, push along +y), lift the door edge
   (y 0.71, z 0.06-0.11; 25 N at horizontal, no spring) and walk it up to vertical. New skill; nothing exists.
4. Then cup r138 (needs side-on or a stance 0.33 ahead: its table is round, the cup in the middle: only 0.41+ ahead is
   free) or the kids bottle to the sink with drop_in_sink (written, not run). sink_basin() must read
   static_boxes("sink_basin_collider") (now reads r27i1_sink: change it).
5. Recorded proofs: jacket (run_cloth_episode.py TAG "[[\"garment\",\"r121i1_jacket\"]]"), first surface pick.

(Update 00:40: sink_basin() now reads static_boxes("sink_basin_collider") with its 45 deg turn, commit f05bee1; item 4 above is done in code, not run.)

## 19 Nov, 00:15-01:20 (third cloth agent, took over at 00:15; AI-operated)
Runs: C:\Users\raresense\sim_home\runs\1119_0020_live_dishwasher1_sink_collider_xray_and_dishwasher_joints,
C:\Users\raresense\sim_home\runs\1119_0045_live_dishwasher2_racks_pushed_in_FELL_deep_squat_facing_y_sat_back_onto_the_island.
Live scripts: C:\Users\raresense\sim_home\_cloth\live\d*.py (d00 setup ... d32), in order.
### Verified in sim (frames looked at)
- Sink basin collider (room_patch extras, 5 boxes): sits on the visual basin, walls just outside the visual walls, top at
  the rim. X-ray pictures (sink + counter visuals hidden, edges drawn for the picture only): run ..._dishwasher1\d05_*.jpg.
- Dishwasher joints in Isaac: door hinge (3.11, 1.432, 0.11) axis +x range -1.571..0, held open by its limit (q 0.0005,
  5.5 cm off the floor): joint limits work on the CPU path. Racks slide +y, 0..0.40 / 0..0.35, still at start.
- The lower rack holds 6 more dishes (plates r67i1-6 in its tines): 15 rack dishes are now loose in the surface room
  (make_apartment_cloth_room.py RACK_DISHES), all still after settling (0.0 mm in 2 s).
- Collision of the racks = 5 thin plates each (floor + 4 walls, 6 mm) + tines on the lower one; the visual wire front is
  3.6 cm in front of the collision front wall. Door collision = one slab z 0.058-0.110 (5.2 cm), free end at y 0.712.
- RACKS PUSHED IN BY THE LEFT HAND (run ..._dishwasher2): upper q 0.40 (its limit), lower q 0.33 (limit 0.35).
  What worked: stance 3 = base (2.60, 1.04, yaw 0) (the corridor between island and fridge; 12 cm from the fridge in the
  squat), deep squat (-0.38, 0.8).
  * upper rack: pads (2.93, 1.10, 0.53) -> (2.93, front - 0.04, 0.53), orientation free (fingers come out along +x),
    pushed in 4 cm steps at 0.05 m/s: went to the limit.
  * lower rack: FINGERS POINTING +y (into the dishwasher), jaws stacked vertically; pads (2.93, 1.10, 0.27) ->
    (2.93, front - 0.05, 0.235) -> 4 cm steps to y 1.47: q 0.33. With the fingers along +x the forearm lay along the
    fridge face (3-7 cm off it) and could go no further in than q 0.23.
  * the upper rack must be in first (out, it blocked the arm and the head in the squat).
  * taking the hand out: straight back along -y slowly FIRST. Lifting first (13 cm) let the fingers ride over the
    front wall's top and pulled the rack all the way out again (twice). The racks have 0.3 N friction: any rubbing drags them.
  * skills.fallen() says "fallen" in the deep squat (pelvis 0.27 < 0.45): my live scripts used pelvis < 0.18 or tilt > 1 rad.
- Why the door cannot be closed from the corridor alone: the free edge must travel 0.63 m along +y (to the robot's
  left) and 0.7 m up; the door needs 25 N at the free edge near horizontal (5 kg, no spring).
### FALL (mine), run ..._dishwasher2_..._FELL_...
Facing +y at base (2.60, 0.81) beside the door's left edge, a deep squat with the right hand moving out at the same time:
the pelvis went 0.35 m back (to y 0.46) and the robot sat down against the kitchen island (its end frame x 2.68-2.73,
y <= 0.43, 0.38 m behind the pelvis). Rule: a deep squat needs about 0.45 m free behind the pelvis; check it.
### Next (door), plan
Door from its FRONT: base about (3.05, 0.50) facing +y (open floor behind it, reached round the island's south side),
both hands pinch the free edge's front face (fingers +y, jaws stacked vertically, lower finger in the 5.8 cm gap under
the door), lift together (12.5 N each) while the hands pitch from fingers-forward to fingers-down, walk forward behind
the rising edge, push the last part with the hands.

## 19 Nov, 01:20-02:22 and 10:15- (third cloth agent, AI-operated)
### Dishwasher door counterbalance spring (coordinator's decision (a), 02:30): values and why
The pack's door r32i1 is a 5 kg panel; its own provenance note says "the real counterbalance springs are not modelled".
Real doors have them, so OUR merged model gets one (fidelity fix, like the hollow cups; D:\apartment_real untouched).
Room data: structure.joint_springs = {"r32i1_door": {"stiffness": 9.5, "springref": -1.70}} (make_apartment_cloth_room.py
DOOR_SPRING -> rooms\apartment_1122_cloth_surfaces.json; apartment.py writes stiffness/springref on the kept joint).
Seen in the solver's own model dump (newton_internal.xml): stiffness="9.5" springref="-1.7" on object_0108_joint.
Hinge q 0 = open (lying), -pi/2 = shut; centre of mass 0.36 m out, 0.016 m under the axis. Net opening torque
(gravity - spring) at 0/15/30/45/60/75/85/90 deg up: 1.5 / 3.6 / 4.5 / 4.4 / 3.3 / 1.6 / 0.3 / -0.44 N m, i.e. 2.1-6.3 N
at the free edge (0.72 m): rests open, needs a real lift on the way, pulls itself shut only in the last ~3 deg, held shut
with 0.44 N m (+ the hinge's 0.2 N m friction). Checked in Isaac with the robot not touching: open door stays at 0.0 deg
(run 1119_0240). "Stays shut" still to be seen once the robot has shut it.
### Racks: library skill seen working (run 1119_0240): push_racks_in() upper 0.34, lower 0.29, 207 s sim, ok
Two postures from rack_stance() = (2.55, 0.95, facing +x): half squat for the upper rack, deep squat for the lower,
hand turned freely, pads low on the front wall, hand straight back out first. That is enough: the door coming up meets
the lower rack's front edge at about 37 deg and pushes it in (steeper than the 27 deg the friction needs).
### Door lift, so far (spring on)
- Right-hand pinch at the free-end corner: fingers +x into the left edge, jaws across the slab. The pads stop 2 cm high
  in the deep squat and the lower finger meets the slab's side: lower the target step by step until the lower pad is
  under the slab bottom (0.058), then in 3-4.5 cm (seen: x 2.855, grip 10.9 / 9.0 N).
- Lifting with the jaws CLOSED on the slab: the door came to 7.8 deg, then the tilting slab wedged the jaws open
  (gap 5.6 -> 7.2 cm, the jaw motor is 20 N) and it slipped out. Twice. Next: lift with the jaws held fully OPEN (the load
  goes into the jaw's end stop, the upper finger keeps the slab from escaping), following the door's MEASURED angle.
- Two stuck sessions from unbounded loops (hand_back_out, lift_to): every loop in these skills is now bounded.

## 19 Nov 14:20 STATUS (after the 10:50 stop and the 14:13 power cut; AI-operated)
Where the dishwasher close stands (runs 1119_1030_live_dishwasher6_spring, 1119_0240_..._STUCK_lift_loop):
- Racks: library push_racks_in() works and is deterministic (upper 0.337, lower 0.291 twice).
- Spring: in the room, seen in the solver dump; open door stays open with the robot away.
- Door lift from the corridor (rack stance moved back to (2.52, 0.95), facing +x; knees then at x 2.73, clear of the
  door's left side face at 2.824 - at 2.55-2.61 the right knee pressed on that face and stopped the door at 8 deg):
  right hand, jaws held fully OPEN (load into the end stop), fingers +x pitched down 0.17 rad, pads 5.5 cm in over the
  edge, lower finger under the slab. Seen: door to 36 deg when the body rose from the deep squat to the half squat while
  the hand followed the arc (load feedforward ts.ctrl.ext 2.5 x the door's net torque). Holding the deep squat the door
  stalls at 8-11 deg (hand 4-5 cm under its target: the arm alone cannot lift there, the legs must). At 40 deg the
  posture rose further, the hand overshot up and slid off the edge in x, the door fell back (no harm).
- Next: rise smoothly to the half squat only while the right hand carries it to ~45 deg; left hand fingertips onto
  the outer face (PART push_left in live\d62_door.py, written, not run), right hand out along -x, left pushes it along
  the arc to 92 deg while the body rises; then check it stays shut, racks inside, dishes in. Then into the library.
- tidy_surface / place_on: written (commit 4e63592), not run yet.

## 19 Nov ~15:30 (AI-operated; vision at every step from 14:55)
- RENDER FIX: the door and racks moved in the physics but were DRAWN where they started (Newton's state that feeds the
  renderer kept their start pose). Seen: solver door 39 deg, picture flat; racks pushed in, pictures showed them out
  (so every earlier "racks in" picture was stale; the joint values were right). surface_skills.draw_jointed_from_solver()
  writes their poses from the solver before every frame (drawing only). Seen working: run ..._dishwasher7...\v008_*.jpg.
- FALL (run 1119_1425_live_dishwasher7_spring_door_to56deg_FELL_...): the legs lift worked (door 0 -> 21 -> 39 -> 56
  deg, frames v004-v008). What I saw in the trace from 2 s before: the right hand's BASE (palm) pressed the door's left
  edge with 29-33 N, mostly along +x (contact normal 0.92 x); the robot's pelvis crept back 2.41 -> 2.29 m with the
  trunk bent forward (tilt 0.52); at 56-60 deg the contact vanished (hand lost the door) and the robot, still moving
  back, fell backward. Causes: pads 5.5 cm in over the edge put the palm on the edge; the load feedforward (2x) made
  the arm push hard. Fix: pads 3.5-4 cm in, feedforward 1.2x, palm-contact guard (back off 1 cm in x above 10 N).

## 19 Nov ~18:45 HAND-OVER (third cloth agent; working memory nearly used up). READ THIS FIRST.
Code: E:\urc_cloth branch home-cloth, last commits f3c1480 (close_dishwasher), d04c804 (merge of home-cleaning incl. the
save game). Never pushed. Isaac slot "cloth" port 47970 (c_live.py start|stop|guard 47970).
### User's rules now (14:55 / 15:00): vision after EVERY action (close-up + wide picture, look before the next),
no assumptions, checkpoints before every action (checkpoint.py does it automatically for the wrapped primitives; my
item checkpoints with ck_save(name, kind="item")), on a failure load the checkpoint just before it, watch, fix, confirm.
### How I work a live session from a checkpoint (fast; no walking there again)
  C:\Users\raresense\sim_home\_cloth\live\d99b_resume.py : room + session code + checkpoint.py + look2 + ck_load(CKP);
  set CKP / RUN_NEW first:  py -3.12 E:\urc_cloth\scripts\isaac_cmd.py --port 47970 -c "CKP=r'...'; RUN_NEW=r'...'; exec(open(r'C:\Users\raresense\sim_home\_cloth\live\d99b_resume.py').read())"
  After a ck_load: set rec.k0 = br.k - round(rec.n/rec.fps/rec.dt) (else the recorder renders a frame EVERY step to
  catch up: slow, and the frames are useless) - d99b does it. A checkpoint loads into the SAME session too (ck_load).
  look2(tag, at=..., ce=eye offset, wide_eye, wide_at) in live\v00_look.py writes vNNN_*_close / _wide pictures.
### DONE (seen in frames)
- DISHWASHER CLOSED by the hands (run 1119_1640_live_dishwasher10_from_ck_DOOR_SHUT_live_then_library_run_FELL_at_release): door 90.0 deg, stays shut with the robot
  away (v016_door_shut_front.jpg), racks + all 15 dishes inside (X-ray v017_xray_racks_inside_shut_door.jpg).
  Checkpoint with the robot standing beside the shut dishwasher: ...\1119_1640_live_dishwasher10_from_ck_DOOR_SHUT_live_then_library_run_FELL_at_release\checkpoints\0107_item_dishwasher_closed_standing
  Racks-in checkpoint (start of the door work): ...\1119_1535_live_dishwasher8_spring_door_to54_FELL_handover_left_hand_let_door_drop\checkpoints\000_racks_in_at_door
- Library close_dishwasher() (surface_skills.py) written from exactly those steps; END-TO-END TEST was running at the
  hand-over (from 000_racks_in_at_door, output live\d100.out, pictures v0xx_close_dishwasher_library_*). Check it.
- RENDER FIX draw_jointed_from_solver() (door/racks were drawn at their start pose); refresh_jointed_footprints()
  after the door is shut (else the floor map keeps the lying door in the way).
- push_racks_in() library, deterministic (0.337 / 0.291).
### OPEN, in the coordinator's order
1. Confirm close_dishwasher() end to end (d100.out + pictures). Tell main and the floor agent ("a003749ca836cfd55").
2. DISH IN THE SINK: BLOCKED by reach as things stand. From the nearest stance (3.39, 1.11, yaw 47 deg, in front of the
   sink cabinet, checkpoint 0135_item_sink_stance_close_empty in run 1119_1640) the right hand with fingers DOWN cannot
   get over the basin: it stops at z ~0.93-0.95 and 0.25 m short (live probe, v029_sink_reach5_heading_frame_*.jpg);
   first the hand was caught UNDER the counter's overhang (come out, up in front of the counter edge, then forward).
   A fall: crouch(0.0, 0.3) + right hand 0.6 m ahead at 1.0 m -> the robot stepped back and fell (run 1119_1640 trace
   t 489-491). Next to try: hold dishes SIDE-ON (hand level, fingers forward: measured reach at counter height 0.33-0.57 m)
   = a side grasp for cups / bottles, then over the near basin wall (~0.45-0.5 m ahead at 0.95 m) and let go low.
3. tidy_surface(name): written (commit 4e63592), NOT yet run in Isaac. Try it first on a thing NOT going to the sink
   (e.g. r158i1_tissue -> rubbish_bin, r139i1_toy_car -> toy basket), then tell the floor agent.
4. Kitchen items of plan v3 (FULL_PLAN_v3.md "The kitchen" table), 5. close_door for the TV-cabinet door r159i1_door
   (push_door_shut() is the generic piece; add r159i1_door to the room's unfreeze list from room_patch_v3.json first),
   6. remaining garments.
### Facts found (do not guess these again)
- Door spring: 9.5 N m/rad toward q -1.70 (room joint_springs), 2-6 N lift at the free edge.
- The arm alone cannot lift the door from the deep squat (stalls 8-11 deg, hand 4-5 cm under its target): the LEGS lift.
- Jaws held OPEN round the slab: the load goes into the jaw end stop; closed on the slab, the tilting slab wedged them.
- Knee and palm contacts with the door push the robot over: knees 3+ cm left of the door's side face, pads only 4 cm in.
- Taking a hand off the door fast made the robot pitch forward into it (twice); 2.5 cm steps at 0.03 m/s: stable.
- Releasing to re-grip lets the door fall back; hand-overs keep both hands on until the second carries.
- skills.fallen() is True in a deep squat (pelvis < 0.45): use surface_skills.robot_down().
- Bounded loops only (two sessions were lost to loops that waited for a door that did not move).

## 19 Nov ~19:30 LAST NOTE of the third cloth agent (stopping: working memory used up)
- close_dishwasher() END-TO-END (library, from 000_racks_in_at_door, run 1119_1640, live\d100.out): every phase worked
  and the DOOR WAS SHUT (90.0 deg; right lift 53.6, both 57.7, right out 57.7, step forward 68.8, side step 89.9), but
  the robot FELL at the very end while the left hand was being taken off the door's top edge (trace t 365.9-367.1:
  standing, then pelvis forward + yaw spinning -0.1 -> -1.9 rad, onto the floor in front of the dishwasher). Picture:
  ...\1119_1640_live_dishwasher10_from_ck_DOOR_SHUT_live_then_library_run_FELL_at_release\v030_close_dishwasher_library_wide.jpg (robot on the floor, door shut).
- Reproduced from checkpoint ...\1119_1640_live_dishwasher10_from_ck_DOOR_SHUT_live_then_library_run_FELL_at_release\checkpoints\0225_act_hand_move (standing, tilt
  0.06, door 89.9, left hand on the door's top edge): the first move of the left hand away (8 cm at 0.05 m/s) -> fell
  within 1 s (frames NOT looked at yet). In the live run that worked, the side step had gone further (dy 0.096, robot
  turned 21 deg, legs crossed) before the hand came off. Difference to look at first: here the side step stopped at
  dy 0.024 because the door passed 89.5 deg; the robot may be leaning on the door through the left arm.
  NEXT: load 0225 (or 0223_act__turn_on_spot / 0221_act_walk), watch the frames, try: stop command 2 s with the hand
  held, check both feet flat and apart, then take the hand off in 1 cm steps (0.02 m/s) straight UP first (it is on
  the door's top edge), look after every step. Then put the fix into close_dishwasher (the release block at its end).
- Coordinator's newest orders for whoever continues (19 Nov evening): work in the FROZEN room
  E:\urc_home\rooms\apartment_1122_full.json (never edit it; ask the floor agent "a003749ca836cfd55" for a checkpoint
  near each task); order: close_dishwasher as a route step + drop_in_sink + tidy_surface; close_door r159i1_door;
  GARMENT FOLD GRIP (grasp across a ridge: jaws closed across a fold, pads down to the fold's base; floor agent's
  close-ups run 1119_144818_route_v3_seg1b look\ct_2_down, ct_3_closed). If a step is stuck > 30 min: tell main, next.
- Sink: see the hand-over above (fingers-down reach over the basin impossible from the nearest stance; try side-on).

## 19 Nov 15:45-16:00 (FOURTH cloth agent, took over 15:45; AI-operated). Real clock = PKT (the run names 1119_1610/1640
## of the third agent were NOT wall times).
- Merged home-cleaning (fd61208: save game + FROZEN room) into home-cloth: d68dd36. Frozen room sha256 checked (matches).
- close_dishwasher RELEASE FALL: reloaded 0225_act_hand_move (old surfaces room) in run
  C:\Users\raresense\sim_home\runs\1119_1548_live_dw_release_from_0225_repro_FELL_then_fix_seen_ok. SEEN (frames\room_00054-00096,
  sheet_room_fall.jpg, close-ups v003_hand_*.jpg): the left jaws sit over the shut door's top-left corner, beside the cabinet
  frame; the library's first step (-0.04, -0.025, +0.015) ran the jaws into the frame after 5 mm (solver contact
  object_0104, normal x), the move timed out with its goal 3.5 cm inside the frame, the arm kept pushing, the LEFT knee
  straightened 0.74 -> 0.06 rad in 0.4 s and the robot spun round the stuck hand onto the dishwasher. Probes from 0225
  (1.5 cm each): +x, -y, +z, -z free; -x, +y blocked.
- FIX seen working from 0225 (v003 -> v005): -y 2.5 cm, -y 3 cm, then (-0.03, -0.02) at 0.02 m/s, reset_arm, rest_hands,
  stand_up: upright, door 90.0 (v005_rel3_arm_rest_stand_door_front.jpg). Library: commit 740863c (release steps; a blocked
  step puts the goal back where the hand is: _dw_hand_out_slowly).
- Frozen-room session: live\e20_frozen_setup.py (episode.py LIVE + floor vis.py + this branch's surface_skills + CKP),
  Isaac started with URC_TEXTURED=1 URC_ROUGH_FLOOR=0.8 like the floor agent's. close_dishwasher end to end from the floor
  agent's seg3 0000_item_start running (run ...\1119_1625_live_frozen_close_dishwasher_from_seg3_start; started 15:57).

## 19 Nov 16:00-16:25 (fourth cloth agent, AI-operated): close_dishwasher in the FROZEN room
- Run C:\Users\raresense\sim_home\runs\1119_1625_live_frozen_close_dishwasher_from_seg3_start (started 15:57 despite its name;
  from the floor agent's seg3 0000_item_start; my checkpoints only in MY run folder; from_ckpt.json written).
  Racks in (0.351 / 0.259). FAILED at the right lift: door stalled at 8.9 deg. SEEN in the trace (t 292-322): right_knee_link
  pressed the door body object_0108 with 8-30 N; frames room_07746-08826 / head_*: the right knee at the door's free-end side.
  Geometry at the stall: feet middle x 2.548 (2.5 cm ahead of the pelvis after the walk), knees at 2.775, the door's side
  face at 2.824. FIX seen working from checkpoint 0145_act_crouch (same run): feet stepped back to x_edge - 0.33 (2.484),
  crouch: knees 2.71 (v004), right jaws placed round the free-end corner (v005), legs lifted the door to 54.0 deg (v006);
  then the library rest (_dw_finish): both 57.8, right out, step forward 86.3, side step, door 90.0, left released with the
  new -y-first steps (errors 3 mm), arm rest, stand: robot standing, door shut (v007_*.jpg). Checkpoint with the robot
  standing beside the shut dishwasher (frozen room): ...\checkpoints\0273_item_dishwasher_closed_frozen_standing
- Library: commit fe75acc (_dw_feet_back before the squat; _dw_finish split out). step_close_door written (9d41929), not run.
- Clean END-TO-END of close_dishwasher() in one call running: run ...\1119_1622_live_frozen_close_dishwasher_e2e_v2_from_seg3_start.
- Sink geometry (frozen room): corner sink at 45 deg, basin centre (3.905, 1.555), half sizes 0.212 x 0.262, rim 0.881,
  floor 0.681; counter front (corner face) 0.337 m in front of the basin centre, the near basin wall 0.125 m behind it.
  The dishes for the sink lie on the island (x 2.1-2.75, y -0.25..0.39, top 0.91): r81 glass_spoon, r89 salad bowl, r90 /
  r91 plates; r63 glass at (4.10, -0.54). Plan: top-down pick (library), then turn the hand SIDE-ON (fingers forward,
  same closing axis) so the dish swings ahead of the pads, pads ~0.45 ahead at ~0.95 m, open (live\e41_sink.py).

## 19 Nov ~17:00 STATE + HAND-OVER NOTES (fourth cloth agent, AI-operated). READ THIS FIRST if I stop.
### Proven (frozen room, Dex1 jaws)
- close_dishwasher END TO END, one call, from the floor agent's seg3 0000_item_start: racks in, door 90.0, left released
  clean, robot standing. Run C:\Users\raresense\sim_home\runs\1119_1622_live_frozen_close_dishwasher_e2e_v2_from_seg3_start
  (v001_close_dishwasher_end_wide.jpg, v001_door_front.jpg), checkpoint ...\checkpoints\0165_item_dishwasher_closed_frozen.
  Code home-cloth fe75acc. Fixes this afternoon: release -y first (740863c), feet back to door face - 0.33 before the
  squat (fe75acc). Floor agent told the exact call (the route step as written).
- 0120 checkpoint in seg3 was the FLOOR agent's own (its USD path), not mine; told main.
### Not proven
- Sink (jaws): no sink dish graspable with the jaws (plates/bowl solid 25-27 cm; r63 glass rim at 1.03 m, 0.33 m deep;
  r81 glass_spoon 0.29 m deep, spoon handle section 4.3 cm at 1.09 m). Teleop try of r81 PARKED at the island stance:
  run C:\Users\raresense\sim_home\runs\1119_1630_live_frozen_sink_side_on_from_dw_closed, checkpoint
  ...\checkpoints\0007_item_PARKED_r81_sink_try_at_island_stance_jaws (sheets t001-t007).
- step_close_door (9d41929), hollow_rim_grips (1a5e6c4): written, not run.
### USER DECISIONS 19 Nov afternoon
- 16:40 TELEOP: drive like an operator: walk <= 0.15 m or 15 deg per command, small hand increments, checkpoint before
  each move, LOOK after each (close-up + side view). Tool: C:\Users\raresense\sim_home\_cloth\live\e50_tele.py
  (MV=("fwd",m)|("side",m)|("turn",deg)|("hand",sd,dx,dy,dz)|("pads",sd,x,y,z,Q)|("turnhand",sd,R)|("open",sd)|
  ("close",sd,F)|("crouch",h,lean)|("stand",)|("look",focus,sd); writes RUN\tNNN_TAG.jpg = close-up + over-the-shoulder).
  Run any live file with e00_run.py (FILE_=...) so errors print short (KeyErrors list the whole model otherwise).
- 16:45 HANDS: the G1 gets FIVE-FINGER Inspire hands (setup "g1_inspire" in configs\robots\setups.json: shapes default
  wrap, pinch (fork 0.5 rad + thumb), push (flat), edge (fingers straight over the top, thumb under, 5.5 cm span)).
  The floor agent builds the NEW frozen room with the hands and sends the room + a start checkpoint. Then: re-prove
  close_dishwasher by teleop first, then the sink dishes now grippable; report which of the 5 dishes are grippable.
### Hand port plan (from E:\urc_main\scripts\cabinet_isaac\k12_grasp.py palm_down / edge_grasp_top, session gripper cmd)
- Hand frame (build_g1_hands.py mount): ee x = fingers; palm normal = -y (left) / +y (right) in the ee frame.
  palm_down(side,u,th) = Rz(atan2 u) Ry(th) Rx(+pi/2 left | -pi/2 right); palm_up = same with Rx(-pi/2 left | +pi/2 right).
- Commands: op.send(dict(cmd="gripper", name=sd, action="open"|"close", shape=None|"pinch"|"edge"|"push",
  force=.. or object_mass=.., friction=..)); grasp ok = thumb + >= 2 fingers touching (cabscene.finger_contacts).
- close_dishwasher: palm UP under the free-end corner of the lying door (fingers along +x under the slab, slab bottom
  z 0.058), thumb above; "edge" shape closes the thumb onto the top; then the same legs lift (_dw_lift) and hand-over.
- Glasses r81 / r63: side-on WRAP (default shape) round the 8 cm body: side-on reach 0.49-0.57 m at counter height
  covers their depth (0.51-0.55 m from a stance 0.22 m off the edge). Then carry side-on over the basin, open.
- Plate r91 (1-3 cm from the island edge): slide outward ~4 cm by fingertips pressing lightly, then pinch shape: fork
  under the overhang, thumb on top. r90 plate and r89 bowl: not grippable (coordinator: list them).
- Garments: thumb + index/middle pinch (needs a new shape measured live) across a fold, fingertips down to its base.

## 19 Nov ~17:10 INSPIRE ROOM, teleop (fourth cloth agent, AI-operated)
- Merged home-cleaning 1da3ef9 (hands) into home-cloth (b325a89). Session: live\e20_frozen_setup.py with ROOM_NEW =
  E:\urc_home\rooms\apartment_1122_full_inspire.json, then ck_load of the floor chain start
  C:\Users\raresense\sim_home\runs\1119_163920_route_inspire_seg1\checkpoints\0000_item_start. hand_skills.py overrides
  pads() for fingers (thumb distal / index+middle intermediate), so brief()/pad_mid work.
- FALL SEEN (run C:\Users\raresense\sim_home\runs\1119_1639_live_inspire_close_dishwasher_teleop, trace t 29.5-31.0,
  frames head_00126-00168): a raw base turn (wz 0.3 for 0.87 s, then 1 s of zero command) left the gait STEPPING; the
  next turn started while stepping: the pelvis ran 0.30 m sideways in 0.6 s, the right knee straightened, it fell.
  FIX seen working from checkpoint 0002 (same run): stand first (_settle_stop), then wz = 1.5 e clipped 0.15 rad/s,
  then _settle_stop: 15.8 deg with 2 cm drift (t006). Teleop now: ("turns", deg) and ("walkto", ahead, 0) (library
  walk, heading kept); raw base moves settle with _settle_stop. Side steps by raw base barely move (4 mm): avoid.
- Turns on the spot drift the pelvis 4-9 cm sideways each (often toward the turn's outside); watch the hands near
  furniture after every turn. Way to the dishwasher (planner way points, driven by hand): (0.05,0.85) -> (0.95,1.25)
  -> (1.8,0.9) -> (2.45,0.92); a mop stands at about (0.75,1.4), a bin at about (-0.25,1.0).

## 19 Nov 16:58 HAND-OVER (fourth cloth agent; context getting full). READ THIS FIRST.
Code: E:\urc_cloth branch home-cloth (last: b325a89 merge + fdbe9e1 hand_skills; hand_skills pads() override not yet
committed at this line - see git log). Never pushed. Isaac slot "cloth" port 47970 (c_live.py start|stop|guard 47970,
start with URC_TEXTURED=1 URC_ROUGH_FLOOR=0.8 like the floor agent). Floor agent now: "ac29a21ca1719e74d".
LIVE NOW (if still running): run C:\Users\raresense\sim_home\runs\1119_1639_live_inspire_close_dishwasher_teleop, Inspire
room, robot driven by teleop from the floor chain start to the dishwasher: pelvis (2.41, 0.93) facing +x, door open,
racks out (upper r33i1 front wall y 1.11, x 2.865-3.355, z 0.475-0.625; lower r33i2 y 1.155, z 0.165-0.305).
Every move has a checkpoint (RUN\checkpoints\NNNN_act_tele_*), the sheets RUN\tNNN_*.jpg.
How to drive: powershell & C:\Users\raresense\sim_home\_cloth\live\t.ps1 "('turns',-15)" tag  (moves: turns deg,
walkto ahead left (<=0.15 m), hand/handw sd dx dy dz (<=8 cm), pads sd x y z Q, orient sd up|down|toward u th, hcmd sd
open|close shape force, crouch h lean, stand, rest sd, look focus sd); third arg = python run first (e.g. a ck_load).
Read the printed SHEET after every move. New session: e20_frozen_setup.py with ROOM_NEW + RUN_NEW (+CKP), then
exec hand_skills.py again if pads() errors.
Open items, in order: (1) racks in + door shut with the FINGERS (plan: back of the left hand pushes each rack's front
wall +y, ee frame identity = fingers forward, palm right for the left hand; the door: palm UP under the free-end corner,
thumb on top, "edge" shape, then the legs lift as before (_dw_lift), second hand, step forward + side step, release -y);
first try of the left hand toward the rack: the pads point stayed 10 cm high and the pelvis tilted 0.32 (t049): check
the hand pose / reach before pushing. (2) Sink dishes with fingers: glasses r81 / r63 side-on WRAP, plate r91 slide to
the edge then pinch; report which of the 5 are grippable. (3) tidy_surface, close_door (step_close_door written),
garment pinch (thumb + index/middle) across a fold (e40_fold.py / e42_fold_live.py drafts, Dex1-era). Recipes from the
offline agents will appear in C:\Users\raresense\sim_home\apartment\recipes\ (dishes, garments, close_dishwasher.json).

## 19 Nov 17:07 HAND-OVER UPDATE (fourth cloth agent stopping: context nearly full). AI-operated.
Inspire room, teleop run C:\Users\raresense\sim_home\runs\1119_1639_live_inspire_close_dishwasher_teleop (sheets t001-t081):
- Driven by teleop from the floor chain start to the dishwasher (turns 15 deg "turns", walk steps 0.13-0.15 m "walkto",
  a look after each). Then UPPER RACK pushed in by the LEFT hand's fingertips/back: q 0.01 -> 0.281 (sheets t054-t072):
  half squat (-0.20, 0.5), hand flat, fingers forward (ee identity turned with the body), at z 0.55 in front of the
  rack's front wall near its left end, pushed +y in 5-7 cm steps. Limits seen: from stance (2.37, 0.92) yaw 1 deg the
  hand reached only y 1.26 (q 0.19); after a 15 deg turn left (stance (2.36, 0.97) yaw 16.5) it pushed to q 0.281,
  then the PALM hit the cabinet frame at the opening's left side (scene_static, 1.7 N, t072/t074): to get past 0.28 the
  hand must be inside the opening (x > 2.86 for the palm) or the fingers turned to point +y.
- LOWER RACK not pushed yet (q 0.0): deep squat (-0.38, 0.8) gave pelvis 0.25 at first, but with the left hand sent
  low in front of the lower rack (target z 0.26) the pelvis stayed at 0.345 and the hand stopped 6.7 cm high (t080,
  t081, no contacts): reach / posture to be solved (try the hand target first at 0.33, then lower the squat; or push
  the lower rack with the fingertips pointing down at its top edge).
- Checkpoint for the successor: ...\checkpoints\0175_item_upper_rack_in_0281_lower_rack_out_deep_squat_left_hand_at_lo
  (deep squat, left hand at (2.85, 1.10, 0.32) in front of the lower rack, door open 0 deg).
- Turn drift: each 15 deg turn moves the pelvis 4-9 cm sideways. Hand moves: in free air 15 cm steps; the hand lags its
  target 1-5 cm at full reach. pads() = thumb/fingers points (hand_skills.py), pads_to with fingers is imprecise: use
  "handw" (ee deltas) for teleop.
Still to do after the racks: door shut with fingers (palm up under the free-end corner, thumb on top, legs lift as in
_dw_lift), then sink dishes (glasses side-on wrap, plate r91 slide-to-edge pinch), tidy_surface, close_door, garments.

## 19 Nov 17:09-17:30 (FIFTH cloth agent, AI-operated): lower rack, Inspire room
- Session: c_live.py start 47970 (URC_TEXTURED=1 URC_ROUGH_FLOOR=0.8), e20_frozen_setup.py with ROOM_NEW (sha256 checked) +
  CKP 0175 of run 1119_1639. My run: C:\Users\raresense\sim_home\runs\1119_1712_live_inspire_lower_rack_door_fingers_teleop_AI_operated
- Tool: live\f.ps1 = t.ps1 with live\f50_tele.py (copy of e50): sheets 0.75 scale + autocontrast, CAM1=(eye,at) / CAM2=(eye,at)
  one-shot camera overrides in the pre-code, prints fingertips ("tips") and racks/door. live\f11_turn.py = hand turn held
  T_T s (the e50 "turnhand" returns at once: position already in tol, rotation never applied). e00_run.py reads utf-8-sig.
- Geometry (frozen Inspire room): lower rack r33i2 x 2.865-3.355, front wall y 1.151 (+q), z 0.165-0.305, range 0.35;
  upper r33i1 at q 0.281 front y 1.381, z 0.475-0.625; door lying x 2.824-3.396, y 0.712-1.432, hinge (3.11, 1.432, 0.11).
  Panel object_0104 x 2.76-2.82, front face y 1.369 (z 0-2.3) = the left frame of the opening; fridge doors x 1.875-2.754,
  front y 1.369. Dishes in the lower rack up to z 0.469, 5 cm behind its front wall.
- Inspire left hand frame (seen): ee = palm centre; fingertips +0.14 along ee x; index +0.03 / pinky -0.037 along ee z.
- SEEN: (1) stance pelvis (2.42, 0.98) yaw 16-19, deep squat (-0.38, 0.8): back of the left fingers (fingers +x) at the rack's
  front-left corner moved it 0.00 -> 0.02; lower/further impossible: waist_pitch at its limit 0.52, elbow ~0.14 (straight);
  asking the hand down made the WBC RAISE the pelvis (0.31 -> 0.42) instead (t016-t018). (2) stance (2.53, 0.96): the
  left knee is at (2.75-2.78, 1.16, 0.24-0.27) = exactly where the hand must be. (3) "fingers straight down" (R rows
  (0,0,1),(0,1,0),(-1,0,0)) from the hanging arm: the IK flipped the arm up/back (shoulder pitch +2.5, wrist pitch -1.4):
  useless; arms_to('rest') resets it. Note: rest_hands() does not lower arms the walk left raised: arms_to('rest', ...).
- 17:30 coordinator: RAM critical (commit 65.2/65.8 GB): checkpoint saved, Isaac stopped (tree-kill, slot freed).
  Checkpoint: ...\checkpoints\0053_item_item_standing_at_rack_stance_before_side_shift_lower_rack_00 (standing (2.60,0.98) yaw 17)
- NEXT (plan): walkto (-0.03, -0.12) -> squat pelvis ~(2.53, 0.85): left knee y ~1.0 clears the wall (1.17); then the left
  hand (identity R, fingers +x, back of the hand +y) up over the thigh, forward, down to ee z ~0.25 at x ~2.78, push +y
  in 3-4 cm steps; the palm meets the panel at y ~1.35 (q ~0.20): enough for the door (contact angle ~38 deg > 27).

## 19 Nov 17:31-18:03 (FIFTH cloth agent, AI-operated): lower rack PROVEN, door with fingers NOT (to 25 deg)
- LOWER RACK IN by teleop, five-finger left hand: run C:\Users\raresense\sim_home\runs\1119_1731_live_inspire_lower_rack_door_fingers_teleop2_AI_operated
  q 0.02 -> 0.225 (upper 0.281), checkpoint ...\checkpoints\0027_item_item_lower_rack_in_0225_upper_0281_left_hand_on_wall
  Recipe (seen): standing (2.60,0.98) yaw 17 -> walkto(-0.03,-0.12) -> pelvis (2.60,0.84); arms_to('rest',both); crouch(-0.38,0.8);
  hand_cmd('left','open','push'); left up 2x14 cm beside the thigh; turn to world identity (f11_turn.py, ~8 s held);
  handw (+0.08,+0.06,0) past the knee, (+0.10,0,-0.06): fingers z 0.25-0.31 at the wall's left end; push +y 4 cm steps
  (0.075/0.121/0.169/0.214); slide +x 2x8 cm (palm past the panel x 2.76-2.82); push: 0.225, then the hand stays 2-3 cm
  short with no contact (reach; rack free). Frames t008-t018. Door-face geometry: enough (meets the edge at ~45 deg).
- DOOR (fingers): stance pelvis (2.49,0.93) yaw 0, feet 0.31 behind the face, crouch(-0.42,1.0) (more lean = 2-3 cm lower
  reach); right palm up (R_palm_up), "edge" open, fingertips 4 cm under the free-end corner (t042). Lift: live\f12_lift.py
  (ee pose turned about the hinge with the door, posture rising from 0 deg; rise from 4 deg = the arm alone stalls).
  0 -> 16.5 deg ok; stalls at 21-25 deg: ring/pinky carry 2-7 N, fingers yield, hand at reach limit. Thumb close
  ("edge", 8 N / 25 N) does not land on top; 25 N slipped. Left hand: knee blocks r 0.45-0.6; at r 0.33 it bottoms out
  above the face. Door lowered (live\f13_lower.py), robot standing: run ...\1119_1800_live_inspire_door_fingers_teleop3_AI_operated
  checkpoint ...\checkpoints\0016_item_item_racks_in_door_open_standing_at_door_stance
- RAM: camera leak fix (home-cleaning 4dbf94f) = live\f05_camfix.py, exec it right after every session setup.
- 18:05 my guard stopped my Isaac (available RAM < 2.7 GB: the user's Premiere Pro holds ~10-15 GB; never touch it).
  Waiting for > 9 GB. Code d2d2529 (home-cloth): cloth.py five-finger hands collide with the cloth through the palm and
  all thumb / finger links (pad friction); caught_fingers(side) = cloth points between thumb tip and index/middle tips.
  NOT yet seen live (garments step). Hamper (world) centre (-2.15, -1.95), rim 0.59, inner r 0.235. Towel r100 is rigid.
- Door idea to try next: fingers STRAIGHT ("push" shape: straight fingers rest on their joint stop = rigid under load)
  instead of the closed "edge" (the flexed fingers yielded at 21-25 deg); start from teleop2 checkpoint
  0081_item_item_right_fingers_under_door_corner_palm_up, f12_lift with B0=0.
- tidy_surface next: r83i1_sponges (1.089, 0.064) on the island -> r94i1_tray_table top centre (1.57, 1.73) z 0.755,
  from the island's west end facing +x (walk backward from the door stance).

## 19 Nov ~18:35 HAND-OVER (FIFTH cloth agent, AI-operated). READ THIS FIRST.
STATE: NO Isaac of mine is running; coordinator's order: do NOT start Isaac until it says "start" (the user's Premiere
Pro ~10 GB + the floor session leave no room for two sessions; the floor session has priority).
PROVEN (frames looked at): step 1, the LOWER RACK in with the five-finger left hand (0.02 -> 0.225; upper 0.281):
  run C:\Users\raresense\sim_home\runs\1119_1731_live_inspire_lower_rack_door_fingers_teleop2_AI_operated, t008-t018,
  checkpoint ...\checkpoints\0027_item_item_lower_rack_in_0225_upper_0281_left_hand_on_wall (recipe in the 17:31 section).
NOT proven: step 2, door shut with the fingers. The lift reaches 16.5 deg reliably and stalls at 21-25 deg (17:31 section).
READY TO RUN (live\run_ready.ps1 A|B starts Isaac + guard, loads the checkpoint into a NEW run, camera fix):
  A = tidy_surface: sponges r83i1 (object_0212_body, (1.089, 0.064, 0.95)) -> r94i1_tray_table (top centre (1.57,1.73),
      size 0.40 x 0.50, z 0.755). Island r35i1_top x 0.93-2.73, y -0.39..0.43, top 0.91. From 0016 (standing (2.50,0.91)
      yaw -1): walk BACKWARD (walkto -0.15,0) ~12x to x ~0.70, then right (walkto 0,-0.15) ~6x to y ~0.06, facing +x;
      hand ~0.39 ahead. Grip: top-down wrap or pinch across the 8 cm width (sponges 22 x 8 cm), check grasp_ok_f.
  B = door retry with STRAIGHT fingers ("push"): from 0081 (fingers under the corner, palm up), then f12_lift.py with
      LIFT0=None, B0=0, B1=35, TH_TO 16 -> 30 -> 50 (look after each); the straight fingers should sit on their joint stop.
Tools (C:\Users\raresense\sim_home\_cloth\live): f.ps1 "(move)" tag "precode" (f50_tele.py: CAM1/CAM2 one-shot cameras,
  SCALE, tips/racks printout), f11_turn.py (hand turn held T_T s), f12_lift.py / f13_lower.py (door), f04_body.py (knees,
  robot contacts), f03_arm.py (arm joints vs limits), f05_camfix.py (RAM leak fix: exec after every setup).
Lessons: (1) never ask "fingers straight down" from a hanging arm (IK flips the arm up); turn to world identity /
  palm up / palm down instead, ~8 s held. (2) The deep squat (-0.42, 1.0) reaches 2-3 cm lower than (-0.38, 0.8).
  (3) The knee positions decide everything at the dishwasher: probe them (f04_body.py) after each squat.
  (4) A camera eye inside furniture renders black (island at y<0.39, x 2.1-2.75).
Code: home-cloth d2d2529 (cloth.py: finger links collide with cloth + caught_fingers), never pushed.
Floor agent now: "afc3f36360d6574bf".

## 19 Nov ~19:05 HAND-OVER 2 (FIFTH cloth agent stopping: working memory nearly used up). AI-operated. READ THIS FIRST.
MODE (user 18:45): autonomous step calls, a checkpoint before every action, automatic failure checks; look only at the
end of a step and on a failure (load the checkpoint before it, watch, fix, confirm).
tidy_surface sponges r83i1 (object_0212_body, 0.12 kg, box x 1.049-1.129 (8 cm), y -0.046..0.174 (22 cm), z 0.91-0.99):
- live\f20_sponges.py (autonomous: walk_path to the stance, hand up close to the body first, above, down, close,
  grasp_ok_f, lift-check, carry, walk_path to the tray table, place, check). Run C:\Users\raresense\sim_home\runs\1119_1838_live_inspire_tidy_surface_sponges_fingers_AI_operated
- WALK OK: stance (0.62, -0.21) facing +x, LEFT hand (the chair object_0260 x 0.395-0.982, y 0.337-0.68 blocks the
  right-hand stance north of it: "no free path"). Checkpoint ...\checkpoints\0050_act_sponges_before_approach.
- GRASP NOT SOLVED (4 tries, seen t008-t011): palm down fingers +x (pitch 0.15 / 0.6, x offsets -0.06..0, force 25):
  thumb + 3-4 fingers touch with only 1-4 N (thumb 11 N on the TOP when the palm is low: the opposed thumb sits under
  the palm and props it on the top face); the fingertips only reach the far TOP edge; lifting 6-8 cm: the sponge stays
  (fingers slide off). Vertical palm on the -y end (f21_end_grasp.py): the hand pushed the sponge 3.4 cm, no contact.
  BUG fixed in my script: never name a session variable SG (it is the save-game module: import urc.tasks.home.savegame as SG).
  Next to try: measure the closed "wrap"/"pinch" finger and thumb positions in the ee frame on an empty hand first, then
  place the hand so thumb and fingertips land on the two 8 cm-apart side faces at mid-height (a claw, palm ~3 cm over
  the top); or the "pinch" shape across the 8 cm height from the side; the dishes/garments recipe tools have hand
  geometry (C:\Users\raresense\sim_home\apartment\recipes\tools_dishes\cache\hand.json).
Door retry B (straight "push" fingers from teleop2 0081) NOT run yet: live\run_ready.ps1 B.

## 19 Nov 19:25 STATUS (SIXTH cloth agent, took over 18:57; AI-operated)
- 19:00 started Isaac (slot 2, port 47970), run C:\Users\raresense\sim_home\runs\1119_1900_live_inspire_sponges_claw_AI_operated
  (empty: the 19:19 power cut came before the checkpoint was loaded). Resume point unchanged: run 1119_1838 checkpoint
  0050_act_sponges_before_approach (left hand, stance (0.62,-0.21) facing +x).
- Plan for the sponge (geometry from hand.json, to be measured live on an empty hand first): the open thumb sticks out
  10.8 cm from the palm plane only 5 cm beyond the palm centre, so palm-down over an 8 cm box puts the thumb on the top
  or on the island; a box face-to-face grip is blocked by the thumb's own links. Candidates: (a) palm pitched down
  ~0.8-1.0 rad with the "pinch" fork: thumb tip on the west face, fingertips on the east face at the same height
  (~9 cm apart, measured first); (b) slide the sponge to the island's west edge, then palm on top, thumb under the overhang.
- Next after the sponge (30 min box): door with straight "push" fingers (run_ready.ps1 B).

## 19 Nov 19:45 (SIXTH cloth agent, AI-operated): five-finger work STOPPED (user decision 19:40: back to Dex1 jaws)
- Run C:\Users\raresense\sim_home\runs\1119_1928_live_inspire_sponges_claw_AI_operated (from 1838\0050).
- MEASURED on the empty left Inspire hand (ee frame: x along fingers, -y palm side; live\g01_measure.py): thumb tip
  pitch 0 (0.049,-0.107), pitch 0.3 (0.075,-0.057), pitch 0.5 (0.064,-0.028); fingertips flex 0 (0.13,0), 0.5 (0.11,-0.044),
  0.9 (0.077,-0.057), 1.2 (0.052,-0.051). Thumb 0.3 and fingers 0.9 meet: a palm pitched 45 deg gives a level claw
  ~13 cm open. live\g00_shapes.py registers custom shapes (add_shape) in ts.setup.grippers.
- CLAW try (live\g02_claw.py, TH 0.785): the hand stopped 5.7 cm from its target (IK at that reach/pitch), all five
  fingers touched at 1-3.5 N, the lift slipped off (c_FAIL.jpg). Not solved; not continued.
- GOTCHA: never name a session variable CL (the cloth module: import urc.tasks.home.cloth as CL) - sync_cloth breaks.

## 20 Nov ~01:05 KITCHEN / TABLE proofs (SEVENTH cloth agent, Dex1 jaws, AI-operated). READ THIS FIRST for kitchen work.
Task (coordinator): prove the kitchen and table steps of the full apartment episode in parallel with the floor robot
(agent a3c1d3e5a85df465e, slot "home"), side branches only: (1) close_dishwasher re-check with the new walking code,
(2) a dish into the SINK with the dishwasher shut, (3) tidy_surface: one coffee-table item + one counter item,
(4) close_door r159 (TV-cabinet door), (5) more table / kitchen items of plan v3, easiest first.
- Merged home-cleaning 54568a4 into home-cloth: 44cb6da (clean; walking-drift fix = plan mode, autorun.py monitor,
  save game, load_floor.py). Room: E:\urc_home\rooms\apartment_1122_full.json (frozen, never changed).
- Slot "cloth" (ISAAC_SLOT2.lock) is held by the towel mimic test (coordinator: 2-3 more hours from ~01:00); checked
  every 15 min; start when free and >= 9 GB available. Never a third Isaac.
- Prepared (not run yet):
  * E:\urc_cloth\scripts\home\kitchen_skills.py: step_mon(st) = one route step (run_step, as route_next plays it) under
    the autorun monitor, with the step's own moving things exempt (dishwasher door / racks / rack dishes, 120 N furniture
    limit for the door lift; close_door: the door; tidy_surface: the thing and its container), route bookkeeping + item
    checkpoint like route_next. dw_names().
  * C:\Users\raresense\sim_home\_cloth\live\k_start.ps1 <tag> <ckpt>: starts the cloth Isaac (URC_TEXTURED=1,
    URC_ROUGH_FLOOR=0.8, CPU path, daqp), guard, new run folder ...\runs\MMDD_HHMM_kitchen_<tag>_AI_operated, k00_setup.py
    (episode.py LIVE + route_v3_setup + teleop + autorun + aside + ops + kitchen_skills; kload(ckpt) = route_v3_resume +
    gait_on (plan mode) + settle). k.ps1 <file> runs a session file. k01_dw.py = step 1; k02_item.py (NAME_) = a
    tidy_surface item.
- Geometry notes (plan v3 + recipes, world frame): sink basin centre (3.905, 1.555), turned 45 deg, rim 0.88, floor 0.68;
  recipe stances (Inspire, level side-on hand, z 1.0): right (3.481, 1.131, 25 deg) lean 0.3 / (3.361, 1.18, 65 deg) lean
  0.6, left (3.481, 1.131, 65 deg) lean 0.3; cabinet bottom panel flush (not 25 cm out). Counter item candidates with jaw
  grasps (grasps_v2): r92i1_pink_container top_down yes 4.6 cm, pads 0.931, 4 cm from the island's south edge, dest SINK
  (umbrella r106 lies south of the island); r83i1_sponges top_down yes 3.1 cm at pads 0.979 (high), dest tray table r94;
  r87i1_wrapper top_down marginal 7.7 cm -> bin. Coffee table: r155i1_kids_bottle (-3.22,-1.00) top-down neck (proven
  18 Nov in the old room) -> sink; side table: r138i1_cup (-1.37,-2.02) top_down / rim pinch -> sink. TV-cabinet door
  r159: hinge (-3.4,-2.827), leaf open along +y, shut = -1.571 (recipe r159i1_door.json: push the west face, follow it
  round the hinge in 10 deg steps, 2.5 kg, damping 0.2).
- 01:15 routing: the floor robot agent is now ab85b8b49b8974b8d (chain at 7 of 63). Proven step calls go to it. Slot 'cloth' still has the towel test (about 2 more hours).
- 03:24-04:45 (AI-operated) run C:\Users\raresense\sim_home\runs\1120_0324_kitchen_dw_recheck_AI_operated (slot cloth):
  * STEP 1 PROVEN: close_dishwasher as one monitored call (step_mon) from seg3 0000_item_start with the plan-mode walking:
    racks 0.359 / 0.283, door 90.0, released clean, standing at (2.54, 0.97); sim 340 s, wall 13 min. Checkpoint
    ...\checkpoints\0294_item_close_dishwasher_done (tele\0002). First try stopped falsely: paper scrap r69i3 jitters on the
    floor by itself (only floor contacts, robot 1.16 m away) -> scraps in CREEPERS (autorun a5f5639). Call sent to the
    floor robot: exec kitchen_skills.py; CREEPERS |= scraps; step_mon().
  * ESCALATED r83i1_sponges (island west end, grasp pads 0.96-0.98, top 0.99): (1) library stance -> right knee 79 N on the
    island; (2) square stance 0.24 m off, fingers down -> hand stuck at 0.77-0.79 against the island side; (3) tilted 40 deg +
    taller posture -> pads 0.96 only at the edge. Fingers-down pads above ~0.93 m are beyond the arm. Fable gets it.
  * Island south items (r92, r87, r78, r71, r93): NO stance while umbrella r106 lies south of the island (route: after the drag).
  * r155i1_kids_bottle (coffee table) from the episode-start state: "no place to stand" (only east stances (-2.83,-0.99)
    facing W are near-free; the map says not free and the half squat's knees reach the table). Not tried further yet.
  * Sink: the floor map's corner cabinet r21i1_corner / r21i1_corner_face are AXIS-ALIGNED boxes whose corners stick out
    0.24 m in front of the real diagonal face: every near sink stance reads "not free". sink_put (kitchen_skills 4fdce1b)
    walks to a free point behind the recipe stance, then one straight leg, turns the hand side-on, puts the thing over the
    basin 3 cm above the rim. NOT run yet (no dish in hand yet).
  * 04:45 Isaac STOPPED, slot "cloth" freed for the Fable agent (coordinator). Resume from 0294 when the slot is back.
- 20 Nov ~05:00 OFFLINE PREP while Fable has the slot (AI-operated; NOT run):
  * r155 kids bottle: C:\Users\raresense\sim_home\_cloth\live\k11_r155.py - SURF_X (0.36, 0.40), half squat lean 0.6,
    tight clearances 0.24 / 0.14 for the item, sink_put for the sink. Stance east of the coffee table facing west
    (about (-2.84, -0.99 -/+ 0.20)). Blockers there now: table base at 0.28 m (= R_BODY), ball r192i1 (-2.85,-1.30) 0.30 m;
    knees within 3 cm of the table in the half squat. Freed when the floor chain has taken: ball r192i1, rug toys r193i1 /
    r193i3 / r193i4, santa hat r189i1; r193i1 SET ASIDE at (-2.927,-0.581) is 0.41 m north of the stance (must be gone).
  * r159 door: kitchen_skills.door_face / close_door_follow (commit after 4fdce1b): stages of 20 deg, stance per stage
    0.40 m behind the push point along the push direction (pelvis 0.58 m from the hinge, outside the 0.5 m sweep), deep-ish
    squat (-0.30, 0.6), push_door_shut, hand out 2 x 3 cm, stand, next. Files: k10_door.py (library one-stance call
    first), k12_door_follow.py (the staged one as the route's close_door step under step_mon). r191i1 toy vehicle
    (-3.52,-2.15) lies 0.13 m north of the free end: route clears it before (rug toys).

## 20 Nov 04:00-05:37 ISLAND REACH solved for r83i1_sponges: TWO-HAND hold (Fable agent, slot "cloth", AI-operated)
Run C:\Users\raresense\sim_home\runs\1120_0401_kitchen_fable_island_AI_operated (side branch from the kitchen run's 0313;
frames tele\0001-0095; result fable_island_result.json). Code: E:\urc_fable2 (branch kitchen-fable, commit 64a64ed,
not pushed): scripts\home\island_skills.py. Session files: C:\Users\raresense\sim_home\_fable_island\.
- KEY FINDING: r83i1_sponges (and r83i2) is a plain box 8.0 x 22 x 8.0 cm; the "narrow sections near its top" in grasps_v2
  are three mesh vertices on a diagonal of the top face read as a 3 cm section. The Dex1 opens 7.9 cm (8.1 at the joint
  limit): NO jaw pinch of it exists. Sections of box-like meshes in grasps_v2 are not to be trusted (they come from sparse
  hull vertices).
- Reach facts at the island (top 0.91), robot at the west end facing +x, pelvis 0.22 m from the edge: hands only work level
  and pointing ahead; one arm reaches pads x 1.12 at z 1.0 with lean 0.3 (lean moves the pelvis 4 cm back, both arms out
  7 cm back; knees then 4 cm from the island face); a level hand does not come nearer the body's middle than 0.10 m at
  chest height / 0.13 m low in front (25-35 deg inward turn of the hand: 0.10 / on the middle for a top press). The
  force command (cmd ee, mode force) presses cleanly (8.6 N measured on the top).
- Attempt 1, one hand, FAILED: hand with fingers along y not reachable (stopped at pads z 0.90); a fingertip push turns
  the box like a door about its far end (2 cm east per 8 deg); a top drag across tips it (rolls at pull 0.5 x press).
- Attempt 2, two hands, WORKED: (1) roll_nearer: left pads (hand 35 deg inward) pressed 7 N on the top's near edge and
  pulled west: one quarter roll, 7.4 cm nearer; (2) both hands level beside the two end faces, Operator.squeeze (8-12 N
  asked, 7-11 N measured each side); lift 6 cm by that friction (only the hands touching, rose 0.060); (3) the
  contact-verified hold on both hands (0.5 each) and walk_path with the hold's own force commands riding on the base
  (4.5 m round the scooter, 5-7 N all the way); (4) set-down by SQUATTING, hands going down with the body, no lean; hold
  off on touch, hands apart (left only 1.5 cm: the mop), stand up with the hands rising, step back, hands down by moves.
  End: box on the tray top lo (1.394, 1.485, 0.755) hi (1.616, 1.572, 0.835), at_place True, robot standing.
- RULES learnt (all in island_skills.py's header): no lean and no lowering by the arms with a two-hand hold (squeeze gone
  within a second, 5 monitor stops, each resumed from the checkpoint before); after the release only zero-velocity hand
  commands; stand up BEFORE the hands go back (fall 2: sat down in the deep squat); never let a raised hand go near
  furniture (fall 1: it came down on the island's edge); after a load stand 4 s + 1.5 s with the hands' commands before a
  step (a step 0.6 s after a load went 7.5 cm sideways); stand so the right elbow keeps 5 cm off the fridge end panel at
  the tray table (it pressed it 5-21 N in the squat at pelvis x 1.57: stand at x 1.53).
- Skill tests as ONE call each from checkpoints: two_hand_pick from 0219 (after the roll): ok, 10.8 N, rose 0.060, 63 s
  sim; two_hand_set_down from 0366 (at the tray, box square): ok, box 1.4 cm off the spot, robot standing, 65 s sim.
  roll_nearer and island_pick as whole calls are NOT run yet.
- Calls (session after kitchen_skills.py): exec island_skills.py; then
    island_pick(body_of("r83i1_sponges"), stand=(0.708, 0.066, 0.0), put_stand=(1.53, 1.25, 90.0), spot=(1.53, 1.535),
                z_top=0.7553, roll=True)
  or the parts: roll_nearer(b, "left"); two_hand_pick(b); two_hand_walk((1.53, 1.16, 90.0), b); two short steps in;
  two_hand_set_down(b, (1.53, 1.535), 0.7553). The spot is the tray's south strip (the plan's (1.50, 1.92) is the north
  strip: reachable only with the box pointing away from the robot, i.e. a one-hand end grasp, which does not exist).
- Other island things, by geometry (not tried): r83i2_sponges (same box, at the island's south edge, long axis along x):
  two_hand_pick from the south side, no roll needed, once umbrella r106 is off the floor there. Two-hand hold fits things
  0.20-0.30 m long, under about 0.8 kg, ends free 5 cm each side, within 0.18 m of an edge the robot can stand at. Things
  the jaws can take (bottles, cans, juice box: 4-7 cm sections) need the level one-hand side grasp, not built here; its
  reach is the same (pads 0.19 m in from the edge with lean 0.3, 0.10-0.24 m to the hand's side); sections of 7.6-7.8 cm
  (chips can r72, succulent r84, wrapper r87) leave under 2 mm for a 7.9 cm jaw.

## 20 Nov 05:40- KITCHEN AGENT (eighth cloth agent, Dex1 jaws, AI-operated). Working notes.
- Slot "cloth" taken 05:42 (port 47970), run C:\Users\raresense\sim_home\runs\1120_0542_kitchen_sink_AI_operated, loaded
  from ...\1120_0324_kitchen_dw_recheck_AI_operated\checkpoints\0294_item_close_dishwasher_done. Guard: c_live.py guard (2.7 GB).
- home-cloth: 2a6602a = Fable's island_skills.py cherry-picked (64a64ed). kitchen_skills: call_mon(fn, label, target,
  ignore_names) = any skill call under the autorun monitor + item checkpoint + end look (like step_mon, not a route step);
  close_door_follow walks round furniture (walk_path) to the first stance when it is > 0.35 m away.
- NEW table_skills.py (not run yet when written): slice_width (real hull section at a height: every segment between hull
  points crossing the plane), side_grasp_z, side_pick (level one-hand side grasp), side_carry.
- Island geometry (live): top x 0.93..2.73, y -0.39..0.43, z 0.91. Sink dishes: r91 tan plate flush with the EAST edge
  (gap 0.0, N 0.085); r92 pink container S gap 0.02 / E 0.105; r78 kids bottle S 0.059; r81 glass spoon E 0.275 / N 0.297;
  r90 plate E 0.195 / S 0.145; r89 bowl N 0.043 (0.9 kg). r63 glass is on countertop_right (4.10,-0.535).
- Running: island_pick(r83i1) as ONE call from 0294 (live\k21_island.py, call_mon).
- island_pick r83i1 try 1 (from 0294): FAILED by the monitor, right knee 120 N on the island's WEST face while the robot
  turned on the stance (0.708,0.066): walk_to_stance found no free point behind it (stance not free at normal clearance,
  scooter object_0260 north) and walked straight in, arriving at 33 deg (tele\0001, w01_knee.jpg). FIX island_skills
  walk_in(stand): walk_tight to 0.15 m behind the stance at its heading, then one straight leg in.
- try 2 (from 0294): approach OK (no touch), roll FAILED: rolled 0 deg; seen at act ckpt 0069_act_roll_nearer
  (tele\0003): the left hand stayed beside the hip at 0.65 m, the path to the top runs through the island edge. FIX
  roll_nearer raises the hand beside the body first ((0.10,0.30,0.60) then (0.17,0.26,top+0.06)). Confirmed from 0069:
  rolled 90.1 deg, 7.2 cm nearer (tele\0004_roll_try1.jpg). Now try 3 = the whole call from 0294.
- try 3 (whole call from 0294): approach OK, roll 90.1 deg, two-hand pick ok (12.1 N each, rose 0.062), then LOST in the
  carry walk at pelvis (1.20,1.17): head frames (tele\w04_lost.jpg) show the box sliding toward the right hand and out of
  the left during a walk_path leg; at act ckpt 0203_act_walk_leg the squeeze read 4.4 / 5.3 N. Teleop from 0203: three
  0.10 m tmove legs kept 11-13 N and nothing else touched (tele 0009). FIX: two_hand_walk walks at TWO_V 0.10 m/s
  (was V_WALK 0.18). Confirming from 0203 (live\k27_walk_put.py).
- Slow walk CONFIRMED from 0203 (k27 a): two_hand_walk to (1.53,1.25,90) err 0.009 m, squeeze 13.6 N at the stance.
- SET-DOWN at the tray FAILS (4 real tries, all from act ckpts of this run; code e098e50):
  a) stance x 1.53 (k27 a): lost in the squat; head frames tele\w05_put.jpg: box turns, slips out of the LEFT hand.
  b) stance x 1.555 (k27 b): same.
  c) probe live\k28_squat_probe.py from 0244_act_two_hand_squat (stage by stage, 0.25 s rows): with the library's steer to
     the spot the left pads drop 7 cm/s (c_ref only 2.7 cm/s) and go back toward the body, squeeze 11 -> 0 in 1.25 s; with no
     steering stage 1 (pelvis 0.685 -> 0.588, box 1.04 -> 0.94) holds 9-11 N, then in stage 2 the left pads sag again
     (0.919 vs right 0.934, 2.5 cm nearer the body), lost at box z 0.87 (top 0.755). Nothing but the box touches either hand
     (contacts listed every row). Left pads are 0.112 m from the body's middle (Fable: level hands do not come nearer than
     0.10-0.13 m): left arm at its inner limit as the body goes down.
  d) stance x 1.57 (Fable's driven stance) (k27 c): right knee 68 N on the tray table's folding X stand while walking in
     (tele\0019).
  NB: setting op._hold["ride"] False after a load wrecks the hold (right 0 N at once); a session global ZRIDE_ stays set.
  => ESCALATE r83i1 set-down. Checkpoints: 0203_act_walk_leg (held, before the last leg), 0244_act_two_hand_squat (at the
  stance x 1.555, held 11.4 N each). Pick part proven as one call: walk_in + roll + two_hand_pick + slow walk.
- r159 DOOR (close_door_follow as the route's close_door step under step_mon, from the floor chain end
  C:\Users\raresense\sim_home\runs\1120_032422_dex1_floor_7\checkpoints\0943_item_r68i1_rag):
  try 1: "no free path" to the first stance (-3.79,-2.39) at normal clearances -> close_door_follow now falls back to
  walk_tight (the toy-corner way round by the north). try 2: walked there (tight), pushed 0 -> -0.155 -> -0.351 -> -0.496 rad
  in 3 stages, then the monitor stopped it: the right foot knocked toy vehicle r191 (3 cm) walking to the 4th stance
  (tele\0022). r191 is a precondition (the floor robot's rug-toy round, which is blocked). Side branch now: set_aside r191 to
  (-2.95,-1.75) first, then the door (live\k13_door_after_aside.py).
  try 3 (side branch): set_aside r191 first -> "no place to stand" for picking it (normal), tight: its stance
  (-3.0,-2.47) has no free path (the open door leaf and the TV cabinet). try 4: close_door_follow now picks a nearer stance
  (back 0.40..0.30) when a small floor thing is within 0.22 m of the stance / 0.16 m of the leg; resumed from
  0462_act_stand_up (robot squatting at stage 3, 0.18 m from r191): "foot on a loose thing r191 (4 N)" at once (tele 0024).
  => ESCALATE r159 door: shuts 0 -> -0.496 rad (28 deg of 90) by close_door_follow, then toy vehicle r191 (-3.52,-2.15)
  sits where the feet must go for the 30-60 deg stages and cannot be picked while the door is open. Needs r191 gone first
  (floor robot's rug-toy round, blocked by scooter r126) or the scene-change rule. Ckpts: 0943 (chain end, start),
  0462_act_stand_up (door at -0.496, robot by the toy).
- TASK 1 sink: no sink dish has a fingers-down or level-side jaw grasp in reach except plate r91 by its RIM (flush with the
  island's east edge). table_skills.edge_pick: slide the plate out 4.5 cm by pressed pads, vertical rim pinch (R_vpinch),
  contact-verified hold, plate hung below the pads; then sink_put. From the kitchen branch 0294 the east side of the island
  is shut off: the rag r68 still lies at (3.36,0.39) there (the floor chain took it), and after a load the floor map still
  had the dishwasher door OPEN (refresh_jointed_footprints() fixes it; now called in k30_plate.py). So the sink run starts
  from the floor chain end 0943 (dishwasher shut + rag gone). walk_in falls back to tight clearances ignoring scraps.
- r91 plate from 0943 (k30, pick only): approach OK (walk_in pre (3.21,0.04) err 5 mm). slide_out moved it only ~1.2-2.6 cm
  (overhang 1.2-2.2 cm, need >= 3.5), the vertical pinch then stopped 9 mm high (lower jaw on the island's top edge).
  Teleop from there (tele 0028-0030): press 9 N 3 cm in: the pads slid off the rim, plate moved 5 mm; press 8 N 7 cm in:
  the hand pushed the plate 7 cm further IN on the way; fingers-down press 6 cm in: out of reach (0.51 m ahead), plate
  pushed/turned further in. => ESCALATE r91 plate (no other sink dish has a jaw grasp, see below). The plate now lies
  further in in that side branch only.
- REAL hull sections (table_skills.slice_width, live\k23_widths.py): r92 pink container 15 x 12 cm at every height (no jaw
  grasp; grasps_v2's 6.3 / 4.6 cm are fake); r78 kids bottle 8.2 cm body, 6.9-7.5 cm at the very top; r63 glass 7.7; r81
  glass spoon 8.0 (2.4 cm only in the top 1 cm); r71 lysol 6.0 cm across y at z 1.03 (approach along x only: none);
  r87 wrapper 5.8-7.2 (south, umbrella); r147 / r148 / r149 / r151 / r177 / r173 / r171: none. Jaw-able with a stance now:
  r138i1_cup (side table, 6.7 cm, level grasp z 0.507, stance (-1.2,-1.64,-90 deg) right hand) -> sink; r158 tissue 5.3 cm
  (no stance). Running: side_pick r138 + sink_put as one call from 0943 (live\k31_side_sink.py).
- r138 cup (side table r135, top 0.477) with side_pick, from 0943, under with_tight (the robot at 0943 stands in a pocket:
  normal clearances give "no place to stand"): try 2: right hip 152 N on the hamper turning on the stance (tele
  w06_hip.jpg) -> side_pick now uses walk_in and only stances whose point 0.15 m behind is free; try 4: approach OK
  (err 3 mm), level pads stuck 4 cm high in the half squat; try 5 (from 0632_act_walk, deeper squat -0.24): pads 13 cm
  short; seen at 0669 (tele 0036): the level hand at 0.47 m folded back toward the body (wrist beyond the pads). => the
  level side grasp is for counter / island height only; low tables take the library's fingers-down surface_pick.
  Running: surface_pick + sink_put from 0943 (k31, ZHOW2_='top').
- r138 top-down (library surface_pick under with_tight): try 6 "no place to stand" (knees vs the round table at SURF_X
  0.31-0.34); try 7 with xs (0.34,0.37,0.40): right knee 90 N on the hamper while walk_to_stance turned (tele 0038).
  => ESCALATE r138 cup (pocket between hamper r133 and side table r135; level grasp folds back at 0.47 m).
- 20 Nov ~09:40 Isaac STOPPED, slot "cloth" freed (RAM 12.2 GB). Code home-cloth up to 17f9a80 (+ final commit below).
### KITCHEN AGENT SUMMARY (20 Nov, AI-operated)
- PROVEN as calls (frames looked at): island approach walk_in + roll_nearer + two_hand_pick + slow two_hand_walk to the
  tray (from 0294 and 0203). NOT proven: the two-hand set-down at the tray (escalated), r159 door past 28 deg (r191
  precondition), r91 plate slide (escalated), r138 cup (escalated). r83i2 (umbrella r106) and r155 (living-room clutter)
  skipped as told. Real hull widths: no island / counter thing has a jaw grasp while r106 lies south of the island
  (r87 wrapper 5.8-7.2 cm and r71 lysol 6.0 cm only from the south / along x).

## 20 Nov 07:15- FABLE ESCALATION 2 (kitchen items the eighth agent escalated; slot "cloth", AI-operated)
Run C:\Users\raresense\sim_home\runs\1120_0715_kitchen_fable2_setdown_AI_operated (from_ckpt.json: the kitchen run's
0244_act_two_hand_squat; side branch). Code: worktree E:\urc_fable3, branch kitchen-fable2 (from home-cloth 17f9a80),
commit 6a876a0, not pushed. Session files: C:\Users\raresense\sim_home\_fable_kitchen\ (fk*.py, fk.sh).
### ITEM A, r83i1 sponges two-hand SET-DOWN on the tray table r94: OK
- ROOT CAUSE of the four failed set-downs (seen, fk19_ee): a hand in FORCE mode (the pressing hand of the two-hand hold,
  the left) keeps its own position target for the two directions across the force (TeleopSession._force_tasks e["p"]),
  moved by the velocity it is sent, with NO limit on how far it runs from the hand (velocity mode: 6 cm / 2 cm). Tied to the
  other hand through the box, it creeps away whenever reference and hands disagree: at the put stance it sat 0.89 m
  BEHIND and 0.33 m BELOW the left hand (1.38 m off at ckpt 0203, mid-walk). That standing pull folded the left arm to
  its elbow stop (-1.05 rad, wrist 1.4 cm from its own upper arm): the left hand could not go forward / up / down with the
  hold, so in the squat the box turned and left the left hand ("pads sag toward the body" = this pull). Not the stance x,
  not the arm's inner limit, not the steer. My earlier run 0366 just had a smaller offset (elbow -0.96, not on the stop).
  Also found: kload()'s settle (op.run without the hold's commands) halves the squeeze (13 -> 5 N); the small
  two_hand_turn (1.7 deg) turned the reference 2.6 deg but not the box.
- FIX (island_skills.py): two_seat() in every hold command (target within 6 cm standing / 2 cm walking of the hand: left
  hand came 2 cm forward at once, elbow off its stop); two_reanchor() (reference re-taken at the hands, not riding);
  TWO["vise"]: both hands by velocity commands with the squeeze as known load; the hold SERVOED on the box (xy to the spot,
  reference never > 3 cm ahead of the hands) and on the pelvis's measured height; squat in 5 cm stages to 6 cm above the
  top; lean 0.2 (2 cm more reach; without it the box landed on the tray's very edge, y 1.474-1.562, teleop attempt 1);
  last centimetres by the arms at 1.5 cm/s to touch; two_hand_open seats the hands' targets first (hands sprang 4-6 cm
  apart, right wrist touched the fridge end panel 4 N); turn only above 8 deg.
- Reach facts: arms follow a move of the hold with 2-4 cm standing error (cause not found) and reach 0.33 m ahead of the
  pelvis at chest height in the squat; lowering by the arms works about 6 cm from chest height, then stalls; the knees
  (0.32 m apart outside) go between the tray table's side frames (x 1.432..1.708, from y 1.52) in the squat: stance x 1.54,
  y 1.25 is the nearest (knees 4 mm from the frames' south faces standing); no step nearer.
- Attempt 1 (teleop, stage by stage from 0244): box on the tray at its south edge (lo 1.431,1.474,0.755 hi 1.654,1.562,
  0.835), robot standing; ckpt ...\checkpoints\0050_item_r83i1_sponges_on_tray_teleop, frame tele\0039_end.jpg.
- Attempt 2 (the library, ONE monitored call from the kitchen run's 0203_act_walk_leg: two_hand_walk((1.54,1.25,90)) +
  two_hand_set_down(spot (1.545,1.535), 0.7553)): done, monitor clean, squeeze 11-12 N through the walk, box lo (1.428,
  1.482, 0.755) hi (1.656, 1.589, 0.835), 3 mm off the spot, rests on the tray only, robot standing at (1.521, 0.966),
  119 s sim. Ckpt ...\checkpoints\0106_item_r83i1_sponges_walk_put_done; frames tele\0045_call_end.jpg, tele\0044_end_*.jpg.
- CALL for the floor robot (after kitchen_skills.py, with E:\urc_fable3's island_skills.py or after merging 6a876a0):
    island_pick(body_of("r83i1_sponges"), stand=(0.708, 0.066, 0.0), put_stand=(1.54, 1.25, 90.0), spot=(1.545, 1.535),
                z_top=0.7553, roll=True)     under call_mon(fn, "r83i1_sponges", target=body_of("r83i1_sponges"))
  Preconditions: both hands free, jaws; scooter / floor as at the kitchen run's 0294 (walk_in finds its own way);
  nothing on the tray's south strip (y 1.48-1.60). The whole island_pick as one call with the new set-down was NOT re-run
  from 0294 (pick + walk proven by the eighth agent, walk leg + set-down proven here from 0203).
### ITEM B, sink dishes: plate r91 PICK solved, SINK PUT not (FAIL as a whole); Isaac stopped 08:20 (PC clock), slot "cloth" free
Side branch from the kitchen run's ...\1120_0542_kitchen_sink_AI_operated\checkpoints\0520_act_edge_reach (robot at the
plate stance (3.05, 0.045, 180), from the floor chain end 0943). Same run folder (from_ckpt_itemB.json). Code c91fdb1.
- Plate r91 real shape (hull): 0.55 kg, radius 0.135, 2.4 cm high, FLAT top (the hull fills the well), foot radius 0.09,
  conical underside up to a 2 mm edge 2.2 cm above the top. Friction: pads 1.2, plate 0.6, island 0.5 (contact 0.6).
- SLIDE solved (tele\0047_slide.jpg): pads on a plate hold 1.2 x press, the plate needs 0.6 x (5.4 N + press): it moves
  from 5.4 N of REAL press; the kitchen agent's 6 / 9 N commanded were at / under that. slide_out now regulates on the
  force measured at the pads: press 12 N (measured 13 N) -> 5.5 cm in one stroke, overhang 4 cm.
- RIM PINCH: try 1 FAILED (pads only 4 mm inside the rim, came off at the lift): seen: opening the jaws right over the rim
  put the lower pad ON the rim and pushed the plate 1.1 cm back; and the hand entered 1-2 cm low. Try 2 stopped before
  contact: 0.24-0.27 m ahead of the pelvis the level hand sags 3.5 cm and does not come up. Try 3 OK: hand up 4 cm,
  upright, ONE step back 5 cm, lean 0.3; closed jaws 3.5 cm outside the rim and 2 cm high, open there, in 1.8 cm past the
  rim, down to the rim's middle (errors < 3 mm, plate not moved), close 18 N (9.5 / 8.5 N), lift 4 + 4 cm (plate turns up
  13 deg on its far foot, grip holds), hold, hand back 10 cm, two steps back: ONLY the jaws on the plate (tilt 28 deg,
  7.6 / 8.1 N), tele\0058_stepped.jpg. Then fingers-down: plate hangs (tele\0060_hang.jpg).
  Ckpts (this run's checkpoints\): 0207_act_crouch_holding (plate in the level rim pinch, robot (3.36, 0.06)),
  0215_item_r91_plate_held_hanging. edge_pick is rewritten from these steps; the whole call was NOT run again.
- SINK PUT FAILED twice (grip intact both times, 8-10 N, carried 1.5 m to the stance (3.47, 1.11)):
  try 1 (sink_put from 0215, plate hanging): "not over the basin": a plate hung fingers-down reaches 0.30 m below the pads,
  the pads would have to be at 1.21 m to clear the rim (0.881); hand stayed at 0.72 (tele\0062_end_*_FAILED.jpg).
  try 2 (from 0207, level pinch with vertical jaws, hand raised at the stance): the hand stops at 0.73-0.78 m, the held
  plate presses the counter front / edge from below with 2.5-4.9 N (tele\0065_sink2_over.jpg): in the carry pose the
  plate is below the counter level and there is no room to bring it up at the stance.
  NEXT (not tried): from 0207 raise the level hand to pads 1.04-1.06 m (plate lowest about 0.91-0.93, level pinch droops
  28 deg) at the PRE-stance 0.35 m behind, walk the last leg with the hand high, then over the basin, lower, let go.
- Too-wide dishes, ranked by geometry (no runs): (jaw 7.9 cm; pads reach 0.19 m in from an edge; island top 0.91)
  1. r92 pink container (15 x 12 x 5 cm, 0.15 kg, 10.5 cm from the E edge, 2 cm from S): the plate's way: slide_out
     strokes (3 from the east, LEFT hand, pelvis about (3.06, -0.14)) until it overhangs 4 cm, then the vertical top-
     bottom pinch (5.0 cm tall < 7.9, light, short lever: no droop). Best candidate; same skill as r91.
  2. r63 glass (7.7 cm, 0.25 kg, right countertop (4.10, -0.535)): one-hand level side grasp with the jaw fully open
     (7.9-8.1 cm: 1-2 mm a side; side_pick with SIDE_JAW_MAX 0.078, pads servo within 2 mm). Sliding it along the counter
     to the sink is NOT possible: the range r29 (y 0.03..0.78, top 1.1, pot and skillets) lies between the right
     countertop and the sink's.
  3. r78 kids bottle (8.2 cm, 0.35 kg, 5.9 cm from the S edge; umbrella r106 gone first): two-hand pinch with both hands
     turned 30-35 deg inward (a round thing is held by two pads whose normals are 110 deg apart: the line between the
     contacts is 35 deg off each normal, inside the pads' 50 deg friction cone); whether the pads come to +-5 cm of the
     pelvis line at z 1.0 is NOT measured (a 2 minute reach probe). Or its top section (6.9-7.5 cm) one-handed at z 1.11
     (above the level hand's measured 1.06).
  4. r89 salad bowl (25 cm, 0.9 kg, 4.3 cm from the N edge): two-hand squeeze across the diameter (0.25 m fits; needs
     4 N a side at friction 1.2, the hold gives 6-13 N; 0.9 kg is above the 0.8 kg tested), or a level hand lowered
     astride the lip (one pad inside, one outside): it then hangs tilted like the plate. Putting a two-hand held bowl INTO
     the sink is unsolved (basin centre 0.34 m behind the corner face, arms reach 0.33 m).
  5. r90 plate (27 cm, 0.5 kg, 19.5 cm from E, 14.5 cm from S): slide_out strokes from the SOUTH (press point 18.5 cm in:
     at the reach limit; r92 and the umbrella gone first), then the rim pinch as r91.
  6. r81 glass with spoon (8.0 cm, 0.3 kg, 27.5 cm from E, 29.7 from N: the island's middle): out of every reach; a top
     drag tips it (19 cm tall on a 4 cm radius). Last; needs lean 0.6 reach measured or something to pull it with.
  All island dishes share the sink-put problem above; solve it once with r91.
