# Apartment 1122 tidy-up: progress notes (home-cleaning agent, AI-operated)

Updated 18 Nov 2026, evening. Code: E:\urc_home (branch home-cleaning, local commits only). Runs: C:\Users\raresense\sim_home\runs\.

## How to run
- Room file: E:\urc_home\rooms\apartment_1122_phase1.json (written by E:\urc_home\scripts\home\make_apartment_room.py from
  C:\Users\raresense\sim_home\apartment\inventory.json). 44 loose bodies (light floor things + toy basket, laundry basket,
  cardboard box, added rubbish bin); the other loose objects and all doors/drawers are static for the episode.
- One episode in a fresh Isaac session (slot "home", port 47960):
  py -3.12 E:\urc_home\scripts\home\run_episode.py TAG E:\urc_home\rooms\apartment_1122_phase1.json "[[\"tidy\",\"r193i1_toy_piece\"]]" 47960 --keep
- Live session for looking and fixing: py -3.12 E:\urc_home\scripts\home\h_live.py start|restart|stop 47960, then send code with
  py -3.12 E:\urc_home\scripts\isaac_cmd.py --port 47960 file.py (set ROOM, RUN, TASK=[], LIVE=True and exec scripts\home\episode.py).
- CPU tests: E:\universal-robot-control\.venv\Scripts\python.exe -m pytest E:\urc_home\tests\home -q
- Which floor items the jaws can take: py -3.12 E:\urc_home\scripts\home\graspable_report.py ROOM OUT.json
  (result: C:\Users\raresense\sim_home\apartment\graspable_phase1.json; 29 of 40 have a section, by geometry only).

## Done
- A: apartment loads, stable (run 1118_174030_A_apartment_load). 0.20x real time with 44 loose bodies; all 198 loose is unusable (<0.02x).
- Video rules built in: fixed cameras, FXAA, thin visuals lifted, exact 30 fps, video_check.py per episode.

## Milestone B (one floor item to its place): in progress
- Target: toy piece r193i1 (on the living-room rug) -> toy basket r186.
- Seen live: the G1 walks onto the 1 cm rug without trouble, crouches, takes the toy piece first try (both jaws loaded), stands with it.
- Failed so far: (1) walking out with the toy it cut a corner in an arc and fell over the standing scooter's deck. Fixed in
  code (legs are now walked along their line with side-step correction; fixed things always get the body radius) - being
  re-run. (2) The way to the toy basket is 7 m round the furniture (the direct way is blocked by the sofa/coffee table/toys).
- Not reachable with the present clearances (0.28 m to fixed things, 0.16 m to small loose things): 13 of the 29 graspable
  items, and the laundry basket r133 itself (no free place to stand next to it).
- The doormat r119 (shoes' destination) is mostly covered by the coat pile, the blanket, a sandal and the floor lamp's base.

## Not started
- C (all of phase 1), C2 (garments as Style3D cloth; see the coordinator's brief and E:\urc_main\scripts\towel_isaac\p06_squeeze.py),
  D (phases 2, 3), doors/drawers/lids, wipe (model in scripts\home\spill.py, never run).
- Skills are still session code in E:\urc_home\scripts\home\skills.py; SKILLS.md in E:\urc_home\src\urc\tasks\home\ lists them honestly.
- CPU backend of Isaac's Newton MuJoCo solver: NOT to be used without the user's yes (coordinator is asking).

## Update 18 Nov, about 18:35
- Run 1118_181227 (kept, renamed ..._FAILED_fell_squatting_at_basket): toy piece taken first try, carried 7 m round the
  furniture to the toy basket with NO fall and nothing kicked (line-following walk works), then the robot fell backwards
  while squatting with the toy beside the megabloks bag and the ottoman. Fix in code (commit after 6f7a559): squat stances
  need the knees (0.24 m ahead, 0.15 m to each side) 12 cm clear of anything taller than 15 cm. Re-running as B_toy_to_basket.
- Time per item at present: about 137 s simulated, 14 min compute (0.16x real time with recording) for a 2.8 m + 7 m trip.
- Coordinator's speed-ups, NOT started: two items per trip (one per hand), faster walk (try 0.3 then 0.4 m/s), route
  ordering by zone, shorter waits. A second agent (E:\urc_fast, slot "fast") works on Isaac's CPU solver backend; do not
  touch it; it may ask how to call the skills (answered once, see commit 6f7a559 calls: walk_path, crouch(**CROUCH),
  pick_floor(body_of(name), "auto"), tidy_one(body_of(name))).

## Update 18 Nov, about 18:55 (hand-over point)
- Run 1118_182933 (renamed ..._FAILED_three_grasp_misses): with the new knee-clearance rule the pick stance came out
  different (right hand, arriving by a 10 cm sideways last leg). Try 1: the pads stayed 6 cm short SIDEWAYS of the toy
  (above_err and down_err y = 0.061), closed beside it and pushed it; tries 2 and 3 lost it; the robot fell at the end and
  the light saber was knocked 1.9 m. NOT yet looked at frame by frame: C:\Users\raresense\sim_home\runs\1118_182933_B_toy_to_basket_FAILED_three_grasp_misses\grasps\ and room.mp4.
- First things to check there (robot's own state first): the base pose at the stance against the planned one (walk end
  error, yaw), and whether the right arm can reach 0.25 m to the side in the deep squat. If the pads cannot get within 1 cm
  of the grasp point, the skill must NOT close (stand up, step, try again) - that guard is missing in pick_floor.
- Milestone B is therefore NOT done as one clean episode. Seen working in separate runs: grasp of the toy piece first try
  (twice), carry 7 m round the furniture without a fall or a kick (once), rug walking.
- My Isaac session is closed and slot "home" freed at this point.

## Update 18 Nov, about 19:35 (second agent, took over at 18:55)
- Work is now on the CPU physics path inside Isaac (URC_NEWTON_CPU=1; merged home-fast 1fea8cf into home-cleaning). Start a
  live session with it:  set URC_NEWTON_CPU=1 before  py -3.12 E:\urc_home\scripts\home\h_live.py start 47960 . About 0.6x
  real time while recording two views (GPU path: 0.16x). Untouched things lie still on this path (the speed agent's fix);
  only the light saber slides 25 cm in the first seconds.
- Failure 3 (run 1118_182933) looked at: it was the LEFT hand. The walk ended 5.6 cm off; the toy was planned on the inner
  edge of what the hand can reach in the squat, so it ended inside the knee; the pads stayed 6 cm short sideways and the
  jaws closed beside it. The grasp close-ups of that run are black (check camera was switched off while recording; fixed).
- Reach of the hand at floor level in the squat measured live: C:\Users\raresense\sim_home\runs\1118_190907_live_reach_probe_cpu\reach_map_left.json
  Good: 0.23-0.31 m to the side, 0.08-0.24 m ahead of the standing pelvis. Pick place moved to its middle (0.17, 0.27).
- New in scripts\home\skills.py (commit 2e633ec + later): jaws close only with the pads within 1 cm of the grasp point;
  reach window checked before crouching; stances keep both feet 4 cm clear of floor things; stance entered walking forward
  from a point behind it; walk_path slows, stops and turns on the spot at sharp corners (the gait carries on 0.2 m after a
  stop command and walked over the toy, run 1118_191838); tight footprints for askew long things (obj_rect);
  put_down picks a spot inside the basket with a feet-clear stance; trace.jsonl (robot state 10 Hz) in every run.
- Seen live on the CPU path (run 1118_191838_live_pick_toy_cpu): toy piece grasped (6.3 / 5.7 N), lifted, robot stood up
  with it. Put-down into the toy basket: being run live now.
- Falls seen on the CPU path, both understood: (1) run 1118_190310: left toe stepped on the toy piece at the old stance
  (the stance left 1 cm between the toe and the toy); (2) none since.

## Update 18 Nov, about 19:55
- MILESTONE B DONE as one clean episode on the CPU path: C:\Users\raresense\sim_home\runs\1118_193303_B_toy_to_basket_cpu
  (toy piece r193i1 -> toy basket, first-try grasp, 176 s simulated, 289 s compute, video check passes). Reported to main.
  Command: set URC_NEWTON_CPU=1, then
  py -3.12 E:\urc_home\scripts\home\run_episode.py B_toy_to_basket_cpu E:\urc_home\rooms\apartment_1122_phase1.json "[[\"tidy\",\"r193i1_toy_piece\"]]" 47960 --keep
- Milestone C started. New task step in episode.py: ["tidy_all", {"names": [...], "max": n, "pairs": true}] (skips and
  lists what cannot be done). First batch C1 (5 rug toys) STOPPED after item 1: toy piece 3 was picked first try and
  carried, but at the basket the hand did not come down to the release point (26 cm too high, 20 cm off; picture
  C:\Users\raresense\sim_home\runs\1118_194316_C1_rug_toys_cpu_STOPPED_put_down_hand_did_not_reach_the_basket\grasps\01_object_0321_body_not_let_go.jpg).
  In run B the same put-down worked only because the base had settled 10 cm off the planned stance. Likely cause: in the
  DEEP squat the fingers-down hand cannot be held 0.2 m above the floor that close to the body (elbow would be above the
  shoulder). Being measured live now (run 1118_195142_live_put_probe_cpu, put_reach_map_left.json): which squat depth
  reaches the release height. Then put_down gets its own posture.
- Written but NOT yet run: two things per trip (skills.tidy_two, pick_floor(holding=...), put_down with the other hand
  holding); pairing switch "pairs" in tidy_all. Faster walking not started (V_WALK in skills.py, 0.18 now).
- Things that have a pick stance now / not: see the list printed by scratch script l50_map (in SKILLS.md: many things in
  tight clutter get no stance until their neighbours are gone). Containers of the pack are kind "object" in the scene
  info; skills.containers() / floor_objects() / at_place() handle that. Sandal r124i2 and plush r187 are already at
  their places at the start.

## Update 18 Nov, about 20:35: PRIORITY CHANGED by the coordinator: make it FAST before more items
Coordinator's order: (1) time breakdown [sent], (2) bring the container to the mess (carry the toy basket to the rug, fill
it there, carry it back once; same for the bin), (3) walk fast and straight (path walked within 10 % of the planned
route, less turning on the spot, crouch as the last step lands), (4) quick pick, 10-15 s from arriving to standing,
(5) target 20-30 s per rug toy, with a video. Garments are NOT mine any more (another agent, E:\urc_cloth, slot 2,
ports 47970-47979): leave hats, jacket, coat pile, blanket, rag, stocking out of the batches.
- Breakdown of milestone B's 176 s: walking 138 s (pelvis travelled 26 m for a 9 m route), pick 16 s, put-down 12 s.
- Why the robot limped (run 1118_191838) and fell (run 1118_200057_..._FAILED_fell_side_stepping...): my line follower held
  the side step at its limit (0.08 m/s) with a slow forward speed whenever the robot was over 8 cm off its line; the
  robot then drifts the other way, a knee goes straight, it tips. walk_path now walks FORWARD steered by heading toward
  a point ahead on the line (side step at most 0.04 m/s). Seen live: legs of 2.8 m with at most 7-10 cm off the line.
- Walking speed: the G1 set-up caps the gait at v_max [0.2, 0.1, 0.5] (and 0.6 of that while carrying: carry_scale).
  Commands of 0.3 / 0.45 changed nothing until the cap is raised: ts.loco.g["v_max"] = [V, 0.1, 0.5]. Being tested live
  at 0.3 / 0.45 / 0.6 (run 1118_202xxx_live_speed2_cpu, speed_test.json).
- A fall that was my own test's fault: goal on a stool (run 1118_201337): walk_path now refuses goals inside obstacles.
- Two things per trip: both picks worked first try (toy piece left hand, ball right hand while the first rode along).
- put_down into the low basket uses a half squat now (measured: run 1118_195142_live_put_probe_cpu).
- Written, NOT yet run: PICK timing switches in skills.py (PICK dict: t_crouch, reach_in_crouch, v_above, v_down, wait,
  t_close, lift, t_stand, v_carry). Try them one at a time on the rug toys.
- Not started: carrying the basket (plan: two hands on opposite walls, squat with the basket 0.3-0.4 m ahead).

## Update 18 Nov, about 21:10: walking speed (measured), and what is running
- Gait study (empty-handed, free 2.8 m stretch y = 1.15, x -4.55..-1.75): C:\Users\raresense\sim_home\runs\1118_202431_live_gait_study_cpu\gait_study.json
  normal pelvis height: cmd 0.20 -> real 0.18 m/s; 0.25 -> 0.29; 0.30 -> 0.44 with STRAIGHT knees, 1.1 m to stop (runaway).
  pelvis 8 cm lower: 0.30 -> 0.35; 0.35 -> 0.45 (stop 0.37 m); 0.40 -> 0.52 (stop 0.41 m); 0.50 -> 0.81, fell.
  Sent to main; main accepted "0.35 commanded with the lowered pelvis". The study script is scratch (l80_gait.py); the
  facts are in the comment above H_WALK in skills.py.
- skills.py now: H_WALK = -0.08 (all standing / walking postures), V_FAST = 0.35 on legs over 0.9 m, gait cap raised
  (ts.loco.g["v_max"] = [0.40, 0.10, 0.50]), and ts.loco.z_com lowered with the pelvis. WHY the last one: the gait goes
  back to its own height at every stop; the first fast leg after a stop then ran with straight knees and the robot fell
  with the toy (run ..._live_fast_items_cpu_FELL_walking_height_was_lost_after_the_first_stop). The z_com change is
  being checked live now (run ..._live_fast_items2_cpu: one toy to the basket, fast walk, old pick timing).
- Coordinator's notes for later: (a) the real speed runs ahead of the command, probably no feedback of the measured
  pelvis speed in the foot placement (src\urc\locomotion\biped.py, update(): b_x from the filtered COMMAND only); closing
  that loop is the way to 0.8 m/s and belongs in the library with a regression test; (b) measure walking while carrying
  and across the rug edge at the new speed before a full floor run.
- Next after the toy run: PICK switches (PICK.update(...)) in groups on the next rug toys; then carry the toy basket to
  the rug (two hands on opposite walls) and fill it there.

## HAND-OVER 18 Nov, about 21:30 (second agent stopping: working memory nearly used up). READ THIS SECTION FIRST.
State of the code: E:\urc_home, branch home-cleaning, all committed locally (see git log; nothing pushed). CPU physics
path is the one in use: set URC_NEWTON_CPU=1 before h_live.py / run_episode.py. My Isaac session is stopped and slot
"home" is free. The cloth agent works in E:\urc_cloth (slot 2); its runs also land in C:\Users\raresense\sim_home\runs\.

### What is done
- Milestone B, clean (accepted by main): C:\Users\raresense\sim_home\runs\1118_193303_B_toy_to_basket_cpu
- Time breakdown of B sent to main (walking 78 %). Gait study sent and accepted (0.35 asked with the pelvis 8 cm lower).
- Regression episode after all the walking changes (the state of the code now): C:\Users\raresense\sim_home\runs\1118_204943_B2_toy_fast_walk_cpu
  PASSES (toy piece -> toy basket, first-try grasp 5.9 / 5.9 N, no fall, video check OK) but it is NOT faster: 186 s
  (B: 176 s). Walk to the toy 36 s (B: 41), pick 18 s (B: 16; the new stand-up takes 7 s), carry 111 s (B: 106),
  put-down 20 s (B: 12; the half squat's hand moves take 15 s). So far only the empty-handed walk gained.

### The coordinator's CURRENT ORDER (speed first, before more items), and where each point stands
1. Breakdown of the 176 s: DONE.
2. Bring the container to the mess (carry the toy basket to the rug, fill it there, carry it back once; same for the
   bin): NOT STARTED. My plan: two hands on opposite walls of the basket (33 x 27 x 12 cm, 0.3 kg), the robot squatting
   with the basket 0.3-0.4 m ahead (one hand on a rim would let it swing down and spill). The reach maps say the hands
   reach 0.19 m to the side only from about 0.3 m ahead in the deep squat (knees in the way nearer). Unknown: whether the
   pack's basket has thin walls the jaws can straddle (grasp_plan(basket) does find a section; look at it live first).
   With the basket at the rug the per-toy trip is under 1.5 m; that is where 20-30 s per toy can come from.
3. Walk fast and straight: PARTLY.
   - Empty-handed: fast walk works (pelvis 8 cm lower, 0.35 asked = 0.45 m/s real, legs over 0.9 m). Seen three times
     on the way to the rug toy: 34 s instead of 41 s, knees stay bent, 7-15 cm off the line at most.
   - Carrying: NOT fast. Three fast carries fell (runs 1118_203441, 1118_203954, 1118_204417, folders renamed FELL...).
     Causes found in the traces: (a) the gait went back to its own height at each stop [fixed: ts.loco.z_com follows];
     (b) with a hand held at its carry place and the pelvis lowered, the posture settles with the pelvis pitched 0.3 rad,
     and walking begun like that accelerates forward [not fixed; so carrying uses the normal height and 0.18];
     (c) at a corner PR.walk_to steps sideways at its limit with backward speed and a turn at once: the robot drifts the
     other way and falls [side steps now limited to 0.04 m/s in walk(); not yet shown to be enough].
   - Path length against the planned route: the per-leg log (skills.WALK_LOG: L planned, path walked) exists; on the way
     to the toy it was 5.9 m walked for 4.2 m of legs (the rest is turning on the spot and the final stepping).
   - Not done: turning while walking, crouching as the last step lands, walking across the rug edge and carrying at
     the new speed measured on their own.
   - Main's note for the controller library: the real speed runs ahead of the command (0.40 -> 0.52, 0.50 -> 0.81,
     knees straighten): look at src\urc\locomotion\biped.py update(): the foothold offset b_x uses the filtered COMMAND
     speed only. Feeding back the measured pelvis speed and holding the height is the likely way to 0.8 m/s; it belongs
     in the library with a regression test (the study script idea: scratch l80_gait.py, described in SKILLS.md).
4. Quick pick (target 10-15 s): WRITTEN, NOT RUN. skills.PICK holds one switch per step (t_crouch, reach_in_crouch,
   v_above, v_down, wait, t_close, lift, t_stand, v_carry); PICK_SLOW = how B ran (16 s). Try them one group at a time
   in a live session: PICK.update(t_crouch=1.2, t_stand=1.5, v_above=0.35, v_down=0.15, wait=0.1, t_close=0.5), look,
   then reach_in_crouch=True, then lift=False. pick_floor returns pick_s (arrive -> standing with the thing).
5. Rug toys at 20-30 s each with a video: NOT REACHED. Best measured so far per toy: 186 s (B2 above); nothing under 176 s has been measured for a carried trip.

### Also written and only partly seen
- Two things per trip (skills.tidy_two, pick_floor(holding=...), "pairs": true in tidy_all): both picks worked first try
  (toy piece left, ball right while the first rode along), first put-down worked; then the robot fell walking to the
  second put-down (the side-step fault, see 3c). Run: 1118_200057_C1_two_per_trip_cpu_FAILED_...
- put_down into a low basket uses a half squat (measured, run 1118_195142_live_put_probe_cpu). Seen once, in that run.
- tidy_all task step (skips and lists what cannot be done). floor_objects / containers / at_place handle the pack's
  baskets (they are kind "object"). Sandal r124i2 and plush r187 are at their places from the start.

### Rules I found the hard way (all are comments in skills.py too)
- Never hold the side step at its limit; never start a fast walk with the pelvis pitched or at the normal height.
- A test goal must be checked for clearance: walk_path now refuses goals inside obstacles.
- The gait carries on 0.13 m (at 0.18 m/s) to 0.4 m (at 0.5 m/s) after a stop command.
- Leave garments (hats, jacket, coat pile, blanket, rag, stocking) to the cloth agent.
- Folder renames fail with "Permission denied" while the Isaac session that wrote the folder is still open.
  (All my fallen runs are renamed FELL... / FAILED... now.)

### Live tools (in the repo: E:\urc_home\scripts\home\live\)
newlive.py TAG (fresh recorded live session with the state trace; then send code with scripts\isaac_cmd.py --port 47960),
l10_reach.py (floor reach map), l60_put_probe.py (put-down reach by posture), l80_gait.py (gait speed study on the free
stretch; set RUNS first), l90_fast_item.py (one toy, timed per stage; set TARGET and PICK_SET first), l50_map.py
(walkable map and which things have a pick stance now), l40_replay.py (what the robot touched around a moment, from
the 25 Hz record), l22_moved.py (what moved by itself).

## 19 Nov, 00:20 (third home agent, took over 23:00; the 21:30 agent stopped without a hand-over)
- What the stopped agent did 21:00-21:30: looked at the toy basket (run 1118_210110_live_basket_carry, reach_map2_left.json:
  release height and wall-height reach in the deep squat), test room rooms\apartment_1122_test_at_basket.json (robot starts
  0.6 m in front of the basket), tried a duck beside the basket (run 1118_212645_live_basket3: slipped out three times
  standing up) and wrote src\urc\tasks\home\hold.py (contact-verified hold). Committed by me (cf02511) after fixing its test.
- Merged home-cloth 3fd8f04 (c9ecc9c). The cloth skills / cloth_episode are in this checkout now.
- Hold wired into the jaws (skills.py: hold_on after a passed grip_check, off in open_jaws; CPU path only). Duck picked
  with it (run 1118_230541): held, err 1.2 cm. That run then FELL walking to the put-down stance: in walk() (PR.walk_to)
  the robot drifted LEFT at 0.19 m/s on a 0.04 side command with vx about -0.03 and sat back onto the ottoman
  (trace t 233-238). Folder renamed ..._FELL_side_drift_into_ottoman_at_put_down_stepping.
- Basket (run 1118_232318_live_basket_take), all seen in frames: both jaws on the basket's side walls from the deep
  squat (stance facing the basket along its short axis, centre 0.42 m ahead, grip points 5 cm from the walls' near
  ends, pads 1.2 cm under the rim): grips 7.7/6.3 and 7.4/6.6 N, hold on the left, stood up with it (rose 0.525 m, tilt
  2.9 deg, plush stayed in); carried 3 m to the rug toys (94 s at 0.18 m/s, way round the furniture); set down (bottom
  1 cm, tilt 0); from the SAME squat the left hand took toy piece r193i1 into the basket (pick_into, 22.5 s,
  look\a10_after_into1.jpg). Then rest_hands() in the squat dropped the left arm into the basket: the open gripper
  hooked the wall and tipped the basket onto the next toy (look\a13, a14). Fix: park_hands() / stand_from_squat() in
  basket_skills.py; never rest_hands in the squat.
- New files: scripts\home\basket_skills.py (take_basket, set_basket_down, pick_into, plan_hub, fill_basket,
  basket_round, park_hands), scripts\home\make_full_room.py -> rooms\apartment_1122_full.json (cloth room + plan's
  free_add, per-object destinations, spots). episode.py is now the runner (see its header): steps tidy_all /
  tidy_surface / garments / basket_round; failed things retried once then skipped; only a fall stops it.
- The rug toys are cramped: the pelvis-reachable area near them is a strip on one side (coffee table, hamper, scooter,
  stocking, santa hat round them). From any one stance at most one toy per hand is in reach.

## 19 Nov, 00:35: FALLS WITH A LOAD (coordinator's priority) - findings and fixes (home agent)
- Six falls in an hour (3 mine, 3 cloth agent's). In 5 of 6 the command at the fall turned 0.4-0.5 rad/s WHILE
  side-stepping at the caller's 0.04 limit and/or walking (PR.walk_to's final stepping; walk_path legs with wz 0.5),
  at the normal pelvis height (knees 0.6-0.9) with something held or touched; the stance knee straightened, then the fall.
- The foot placement already uses the MEASURED capture point (biped.py ~253): the "no velocity feedback" idea was wrong;
  but the steady-gait offset it aims for uses the commanded speed only (a bias makes the robot crab).
- (The plain-MuJoCo bench scripts\home\gait_bench.py did not reproduce any fall; user's rule: Isaac only, so it is kept
  as a record and NOT used for decisions.)
- Isaac regression 1 (run 1119_001520_..._FELL_lap1_drifted_left_onto_the_flat_shoe): carrying the basket (held by the
  LEFT hand's hold only) the robot crabbed 4 cm/s to the left against a 4 cm/s correction, the shin met the flat shoe
  r125i2 (127 N, trace "touch") and it fell. FALL_REPORT.txt + FALL_closeup_*.jpg in that folder.
- Pelvis pitch with the basket held, measured in Isaac (run 1119_001520): normal height 0.133 rad, lowered 8 cm 0.446 rad
  (the pelvis also went 4 cm lower than asked). So carrying stays at the normal height for now.
- Fixes committed (37f149e, 5283576): biped.BipedWalk.shape (no turn + side step at once, turn rate capped while walking,
  0.15 rad/s carrying, side step over 1.5 s -> 0.02 m/s) + tests\home\test_gait_shape.py; biped speed feedback
  (_speed_feedback: measured CoM speed in the heading frame, low-passed over a stride, integrated error added to the
  foothold's speed; gait setting v_fb); held weight told to the controller (ctrl.ext) so the gait knows it carries;
  basket weight shared by both hands' holds; walk() in phases (never two motions at once); walk_path: turn on the spot
  to 0.12 rad, gentle steering; carrying something that reaches out: ways keep the swept circle of hands + held thing
  clear of furniture tall enough to be hit, and the robot backs straight out to open floor before turning; walking ways
  keep 0.21 m (was 0.16) from small floor things where possible; trace.jsonl now logs "touch" (largest contact force on a
  robot body from furniture / loose things, and on a held thing) and the hold stretch, and writes FALL_REPORT.txt +
  close-ups at a fall.
- Isaac regression script: scripts\home\live\l95_walk_regression.py (route out with a 90 deg turn, 0.3 m side step and
  back, N laps; result regression_<tag>.json in the run folder). Regression 2 (speed feedback + even hold) running now:
  run 1119_002143_live_walk_regression2.
- Merged home-cloth f05bee1 (surface_skills.py: surface_pick seen once, place_into, drop_in_sink written). The runner
  execs surface_skills.py; things on furniture go to a tidy_surface(name) if the cloth agent adds one (none yet), floor
  things to the sink through its drop_in_sink. Full room: scripts\home\make_full_room.py now builds on the cloth agent's
  apartment_1122_cloth_surfaces.json (hollow cups, sink basin collider, dishwasher joints) + the NEW plan patch
  (48 planned things, 72 loose bodies).

## 19 Nov, 00:55: walking regression in Isaac (l95), what each fall was (home agent)
Route in the test room (start by the toy basket): (0.1, 0.45) -> (-1.9, 0.45) [90 deg turn], 0.3 m side step out and back,
route back; empty-handed then carrying the basket. The CPU path is DETERMINISTIC: the same code and commands give the same
run to the last digit (runs 1119_003817 and 1119_004135 identical), so a change can be A/B-tested by one run.
- 1119_001520 (basket, left hold only): crabbed left, shin hit the flat shoe r125i2 (127 N) -> fell.
- 1119_002143 (basket, both holds + speed feedback): crabbed 0.12 m/s; cause found: the gait's heading (yaw_ref) runs ahead
  of the body after a turn on the spot (turns at ~65 % of the command) -> clamp yaw_lead 0.15 (committed aa169df).
- 1119_002646 (empty, 0.35): my shaping cut the speed 0.35 -> 0.05 at a leg end -> ran away (fixed: never cut while moving).
- 1119_003011 / _003326 (empty, 0.35): sped up to 0.7-0.95 m/s; first thought the rug edge, then:
- 1119_003817 / _004135 / _004717 (empty, 0.28; rigid rug / no_robot_contact / bevelled rug): the SAME fall each time:
  the left foot lands on the edge of the flat shoe r125i2 lying 2 cm beside the foot's lane (pelvis passes 0.28 m from it,
  the foot reaches 0.19 m out, plus sway and 5-10 cm of line error) -> sideways lurch 0.55 m/s -> fall. The rug edge next
  to it was NOT the cause (bevelling changed nothing); no_robot_contact also changed nothing (Newton re-encodes contype /
  conaffinity, so that switch never worked on this path) and is OFF in every room file (coordinator: a visible fake).
- Kept: bevelled rug / doormat edges (structure.bevel; apartment.py: inner slab of the same height + 6 cm ramps, checked by
  ray casts: 0 -> 1 cm over 6 cm), a more real rug model. Cords / strap: walking ways keep off them where there is room.
- Fix for the shoe falls: walking ways keep the pelvis 0.30 m from small floor things where there is room (then 0.21, then
  the stance grid); the trace now logs a foot standing on a loose thing ("foot" in touch). Regression 9 running
  (run 1119_005059).

## 19 Nov, 01:20: walking regression continued (home agent)
- 1119_005059 (6 cm bevel + 0.30 floor-thing berth): outbound passes the shoe (off 4-5 cm); return: lurch on the rug ramp.
- 1119_005527 (15 cm bevel): fell on the first 0.47 m leg (always passed with the plain edge). BEVEL REMOVED from all rooms.
- 1119_005735 (plain rug edge): lateral lurch 0.5 m/s just after stepping down off the rug, no contact logged.
- 1119_010048 (ALL tonight's gait changes off, exact A/B): outbound passes (off 3-6 cm); falls in the final side corrections
  at the rug's lower edge (side step drifting opposite to its command at 0.5 m/s): my gait changes are not the cause.
- 1119_010653 (slow 0.18, heading-lead clamp 0.15): the robot could not steer while walking (yaw unchanged for 1 s on
  0.25 rad/s), drifted 1.1 m and its arm hit the sofa. Clamp -> 0.6 rad (safety net); instead walk_path turns on the spot
  and comes to a STAND before each leg (the gait re-takes its heading at the start).
- 1119_011012 (slow, settle before each leg): out and back with both side steps PASS (legs off 7-11 cm); fell on the last
  leg into the cramped start corner while braking with the steering at its limit, 0.6 s after stepping down off the rug.
  Fix: no steering and no side step in the last 0.35 m of a leg (walk corrects standing). Regression 15 running.
Open: stepping DOWN off the 1 cm rug edge is followed by a lurch in 3 runs (2 others crossed fine). Rugs stay as the pack
has them. Speed now: 0.18 everywhere in the regression; 0.28 on long empty legs in the skills (V_FAST).

## 19 Nov, 01:50 (home agent): runner proof R3, full route stopped for two walking fixes
- R3 (report 3): C:\Users\raresense\sim_home\runs\1119_012404_R3_mixed_cloth_rigid (episode_room_and_head.mp4, video check
  PASS). Runner mechanics work: cloth step (knit hat) then rigid step (toy piece) in one session, retry once then skip with
  the reason, partial results after every thing, stop only on a fall. Hat: grasped 6 of 7 closings but every carry failed
  at once with "no free path to [-2.45, -1.56, -1.31]" (the hamper drop stance; NOT diagnosed). Toy piece: picked first
  try, then FELL carrying: the hanging right gripper hit the heater (44 N) and the side table (650 N).
- Coordinator's notes on R3 (fixing now, regression 17 run 1119_014808): (1) steering weaved +-0.15 rad/s every 0.5 s,
  10 cm peak to peak -> heading follower now uses the pelvis place/heading low-passed over 0.5 s, aim 0.6 m+ ahead, gain
  0.8 (was 1.5), 0.05 rad deadband, wz rate-limited; WALK_LOG has "swing" (lateral peak to peak per leg), target < 3 cm.
  (2) free arm out to the side -> free hands are held tucked in front of the hip while walking (tuck_cmds, TUCK
  (0.15, 0.17, 0.60)); the carrying hand at CARRY_HAND (0.28, 0.14, 0.78) in front of the body (was 0.26, 0.20, 0.64).
- The "foot-on-thing" text in FALL_REPORT.txt was only a column label (no foot touched a loose thing); now printed only
  when it happens.
- Full route launcher: py -3.12 E:\urc_home\scripts\home\run_full_route.py TAG (rebuilds the rooms from the current plan,
  plays route_steps.json as one --long episode). Launched once at 01:55 and stopped before the scene loaded (to do the
  two fixes first).
- Cloth agent af976ff stopped (handover in PROGRESS_CLOTH.md); the new one is a86709ccea34d653c. It must merge
  home-cleaning into home-cloth (rooms\*.json: regenerate with make_apartment_cloth_room.py). Its notes: no
  tidy_surface yet; drop_in_sink unreachable while the dishwasher is open (runner now skips sink things with that reason).

## HAND-OVER 19 Nov ~02:00 (third home agent; read this first). Code: E:\urc_home, branch home-cleaning, all committed
## (as abdullahanxie, no push). Last commits: 4004165 + later "walking" commits (see git log).
### User's order (02:00, via coordinator): clear the WHOLE apartment overnight so it LOOKS clean, incl. scooters r126
(3 kg, living room (-0.95,-0.30): a blocker, move it EARLY by a one-hand drag by the stem with the hold, park it upright
at a wall), r127, toy bike r128, open umbrella r106, cardboard box r175, the kitchen. Plan v3 (*_v3.* files in
C:\Users\raresense\sim_home\apartment\full_plan\, offline planning agent) brings destinations/methods for every thing and
a "looks clean" check; branch home-look (textured look) to merge and check in Isaac.
### Order of work: 1) falls (walking regression) 2) scooter r126 drag 3) whole route as ONE episode, repeated, fix first failure each time.
### How to run
- Live session: set URC_NEWTON_CPU=1 & set URC_QP_SOLVER=daqp, then
  py -3.12 E:\urc_home\scripts\home\live\newlive.py TAG E:\urc_home\rooms\apartment_1122_test_at_basket.json
  (robot starts at the toy basket; phase1 / full room start at the entry). Send code: write a .py (no BOM) and
  py -3.12 <scratch>\snd.py file.py  (= scripts\isaac_cmd.py --port 47960 without the BOM problem).
- Walking regression (Isaac, deterministic): in a live test-room session exec
  REG=dict(route=[(x0,y0),(0.10,0.45),(-1.9,0.45)], side=0.3, side_dir=-1, laps=2, carry=(), tag="...") then
  exec(open(r"E:\urc_home\scripts\home\live\l95_walk_regression.py").read()). Result regression_<tag>.json in the run
  folder; WALK_LOG has per-leg "off" (worst distance off the line) and "swing" (lateral peak to peak). Set V_WALK=0.18 first
  for the slow walk (default V_FAST 0.28 on long empty legs).
- Episode / runner: py -3.12 E:\urc_home\scripts\home\run_episode.py TAG ROOM "<task json>" 47960 [--long] [--only-task-garments]
  Whole route: py -3.12 E:\urc_home\scripts\home\run_full_route.py TAG  (rebuilds rooms from the plan, plays route_steps.json).
- Tests (no sim): E:\universal-robot-control\.venv\Scripts\python.exe -m pytest E:\urc_home\tests\home -q --ignore=tests\home\test_cloth_headless.py
### State of walking (the blocker). Every fall since 23:00 is listed in the sections above with its cause. What is in now:
gait shaping (one motion at a time), heading-lead safety net 0.6 rad, stand before every turn on the spot (also between
legs), legs walked forward + steering only (no side step while walking), steering from the pelvis place/heading low-passed
over 0.5 s, aim 0.6 m+ ahead, gain 0.8, 0.05 rad deadband, rate-limited, no steering in the last 0.35 m, slowing from 0.6*rest;
final corrections forward/back only when a foot is on a rug/mat edge (feet_on_edge); walking ways keep 0.36 m from
furniture and 0.30 m from floor things where possible; free hands TUCKED in front of the hips while walking (tuck_cmds),
carrying hand at CARRY_HAND (0.28, 0.14, 0.78). Regression 19 (run 1119_015324) is the first with all of these.
Best earlier result: run 1119_011012 (out-and-back + side steps passed; fell on the last leg). Remaining known fall
kinds: lateral runaways at/after the living-room rug edge; braking at leg ends.
### Other states
- Basket skills (scripts\home\basket_skills.py): take 4/4, carry 2/4 (falls), set down 1 ok 1 tipped, toy from the squat 1/1.
- Runner proof R3: run 1119_012404_R3_mixed_cloth_rigid (mechanics OK; hat carry "no free path" to the hamper stance;
  toy carry fell on furniture contact). The hamper-stance path failure is NOT diagnosed.
- Cloth agent now: a86709ccea34d653c (E:\urc_cloth). It must merge home-cleaning into home-cloth (regenerate rooms\*.json
  with make_apartment_cloth_room.py). Tell it when the walking regression is green.
- Not done: reports 2 (basket at the rug, seconds per toy video) and 4 (whole route episode); PICK speed-up switches
  untested; crumpled papers into the bin (coordinator) untested; scooter drag not started.

## HAND-OVER ADDENDUM 19 Nov ~02:10 (third home agent stopping: working memory nearly used up). My Isaac is stopped,
## slot "home" free, 0 orphan nvngx_update.exe. Everything committed on home-cleaning (last: "Walking: way points ... off rug/mat edges").
Walking regression after the hand-over above (all in the test room, l95, V_WALK 0.18, deterministic):
- 1119_014808 (damped steering + tucked arms): fell, a turn on the spot begun while still walking -> _turn_on_spot now
  stands first. 1119_015050 identical (fix not yet in), 1119_015324 (fix in): fell, sideways runaway (0.4 m/s) while
  STOPPING at the end of a short leg next to the living-room rug's lower edge (y = 0.235 in the test frame).
- Arm tuck switched OFF (TUCK_ON = False in skills.py): with it three runs fell in the first two legs; released arms hang
  at +-0.25 m. (Coordinator wanted tucked arms; a joint-space posture for the arms, not a Cartesian chase of a target that
  sways with the pelvis, is the next thing to try.)
- 1119_015604 / _015855 (no tuck; second one with keep_stops_off_edges): identical falls: the planner (0.36 m furniture
  berth + 0.30 m floor-thing berth from R_BODY_WALK / R_FOOT_WALK) splits the first leg into 0.19 + 0.25 m legs in the
  cramped start corner; the robot stops 0.1 m from the rug edge and runs off sideways while stopping. keep_stops_off_edges
  did not move that stop (no free shift found there). The run before these walking-way changes (1119_011012) crossed the
  same edge in ONE straight leg and passed the whole out-and-back.
WHAT I WOULD DO NEXT (in this order):
1. Make stopping safe: the runaway happens in the gait's stop (idle steps / settle) after walking, with a foot near the rug
   edge. Look at biped.py settle/idle-step logic with a foot 1 cm higher than the other (floor_z is the start's floor; the
   capture-point "catchable" test uses sole xy only). A deterministic A/B: re-run 1119_015855's code with
   ts.loco.g["ground_follow"]=False, then with pl_td_min 0.6, then with R_BODY_WALK = R_BODY (one straight first leg).
2. Until then, for the full route prefer the settings of run 1119_011012: R_BODY_WALK = R_BODY (0.28), keep R_FOOT_WALK
   (the shoe fix), keep stand-before-turn, V_WALK 0.18 on all legs (set V_FAST = 0.18), no basket carry.
3. Scooter r126 (user's order): make it loose (add to structure.free in make_full_room / the v3 room), one-hand top-down grasp
   of the handlebar bar at ~0.85 m standing (cloth agent's reach map: pads 0.80 m standing with lean 0.3 reach 0.33 m
   ahead), hold_on, walk backward slowly dragging it (watch the hold stretch and trace "touch"), park upright at a wall.
4. Whole route: py -3.12 E:\urc_home\scripts\home\run_full_route.py R4 ; fix the first failure each time; merge plan v3
   and branch home-look when they appear.
Reports sent to main: 1 (stopped agent's work), root-cause notes (00:15, 01:00), 3 (runner R3). Not reached: report 2
(basket at the rug, s/toy video) and report 4 (whole route).

## 19 Nov, 10:30 (fourth home agent; took over 02:03, stopped 02:22 by an API outage, resumed 10:15)
Walking: the three exact A/B tests of the 02:10 hand-over (one change each from regression 21's code, l95, test room, 0.18 m/s,
CPU path, deterministic):
- A ground_follow OFF: 2 laps, 0 falls: C:\Users\raresense\sim_home\runs\1119_020423_live_walk_regA_ground_follow_off
- B pl_td_min 0.6: the identical fall of reg 21 (..._1119_021448_live_walk_regB_pl_td_min_06_FELL_identical_to_reg21)
- C R_BODY_WALK 0.28: one straight leg over the rug edge, then fell on the next leg (right gripper hit furniture):
  ..._1119_021651_live_walk_regC_r_body_walk_028_FELL_second_leg_gripper_hit_static
Cause: with ground_follow the swing's landing height was the stance foot's: a step OFF the 1 cm rug was planned 1 cm high and
landed late. Committed 8dddd08 (biped.py: ground_follow default False).
Arms: fixed JOINT tuck while walking tried live (run 1119_021931_live_arm_posture_probe, t00..t04 close-ups): chosen
ARM_TUCK pitch 0.05, roll 0.05, elbow 0.6 (on the G1 a SMALLER elbow angle bends the forearm up; 1.28 = hanging): grippers
0.28 m ahead, 0.17 m to the side, 0.55 m high, in front of the thighs. skills.py: arms_to / ready_to_walk tucks free arms,
crouch / crouch_holding put them back to rest first; CARRY_JOINTS switch (carrying arm frozen as a joint posture at its carry
place, hand command dropped, hold kept). Regression D (tuck, empty) running: 1119_10xxxx_live_walk_regD_tuck_joint.

## 19 Nov, 14:25 STATUS (fourth home agent; stopped 10:55 by the account limit, PC rebooted 14:13 by a power cut)
Committed on home-cleaning: 8dddd08 (ground_follow off), a3ac353 (arm joint tuck), d818707 (V_CREEP 0.08, STALL_S, CARRY_LOW,
v3 plumbing in make_full_room / run_full_route, big_skills.py scooter geometry), f293182 (merged home-look: textured look,
URC_TEXTURED=1 / URC_ROUGH_FLOOR=0.8 or room "look"). Uncommitted at the cut: W_TURN_CARRY 0.2 (skills.py), regenerated rooms.
Walking regressions 10:30-10:55 (test room, l95):
- EMPTY: GREEN twice: A (ground_follow off, 2 laps) and D (+ joint arm tuck, 2 laps, 0 contacts).
- CARRYING: not green. E/E2 (walk to the duck pick) and F (walk to the basket): crept at 0.05 near a leg end, stepped in place,
  drifted sideways into the basket -> fixed by V_CREEP / STALL_S (F2 got past it). F2 (basket, normal height): knees nearly
  straight, ran off sideways by the flat shoe on the way back. F3 (CARRY_LOW + CARRY_JOINTS): a turn on the spot carrying at
  0.4 rad/s drifted 0.25 m, knee met the cup r197, fell. F4 (+ W_TURN_CARRY 0.2, textured look on): FELL at the same place
  (left elbow on the wall) -> folder to be renamed FELL. Turns on the spot move the pelvis ~0.1 m per radian (empty).
- R3's bin (coordinator's question): it first moved at t=589.5 s, 4.5 s AFTER the fall began (585.0): knocked by the falling robot.
- Textured look seen in Isaac (run 1119_105122 00_start.jpg): textures right, floor glare down, startup 84 s (was 70 s),
  physics 1.5 wall s per sim s (same as before).
Next: rename F4 FELL, commit, then scooter r126 carry2 live (big_skills.py), then the v3 full route.

## 19 Nov, 15:05 SAVE GAME + route item by item (home agent; user's rules 14:55 / 15:00: checkpoints everywhere, vision after every action)
- Library urc.tasks.home.savegame (E:\urc_home\src\urc\tasks\home\savegame.py): save_ckpt / load_ckpt / is_quiet. Whole state
  at ANY moment between control steps (solver mj_getState INTEGRATION, bridge, controller model data, controller objects field
  by field, holds, cloth incl. cloth grips). PROVEN EXACT: save in session A, 10 s; fresh session B loads, same 10 s: max
  |qpos| / |qvel| difference 0.0 (runs 1119_142754_live_restore_proof_A_..., 1119_143724_live_restore_proof_B_...; frames
  prove2_A_after_M2.jpg / prove2_B_after_M2.jpg identical).
- Session glue scripts\home\checkpoint.py (loaded by episode.py in LIVE sessions): checkpoint BEFORE EVERY ACTION (wrapped
  primitives: walk, turns, crouch/stand, servo_pads, jaws, carry_pose, both_move, basket moves, cloth lock/unlock, every
  walk_path leg, every op.move), rolling every 5 s (last 20), item-end kept; act/roll of an item pruned when it ends ok.
  Folders RUN\checkpoints\NNNN_<item|act|roll>_<name>; meta.json info has the action + args, route position, USD, git.
  Size: ~2.3 MB each (cloth.npz uncompressed ~2 MB of it), save 0.1-0.5 s.
- scripts\home\route.py: route_start / route_next / route_resume / route_skip; segment.json per session; join_segments.py
  joins the pieces (frames from checkpoint to checkpoint) and runs video_check.
- How to play: newlive.py TAG rooms\apartment_1122_full.json (URC_TEXTURED=1, URC_ROUGH_FLOOR=0.8), exec live\vis.py, then
  route_start(steps) once, route_next() per item, look at look\ grasps\ and see_robot() stills after each.
- Route order change: the doormat (shoe places) is covered by the blanket and coat pile -> those two garments go first.
- Segment 1 running: C:\Users\raresense\sim_home\runs\1119_144818_route_v3_seg1b (item 1 coat pile: closings failing so far).

## 19 Nov, 16:15 STATUS (home agent) - route v3 live, FROZEN room
- Room frozen (rooms\apartment_1122_full.FROZEN). Live session seg3: C:\Users\raresense\sim_home\runs\1119_152622_route_v3_seg3.
- EPISODE CHAIN: checkpoints\0000_item_start -> 0066_item_r123i1_slipper (slipper put aside by the toy bike; goes to the mat
  at the end). 1 of 65 items. 0120_NOT_ON_CHAIN_* is a bogus optional skip (fixed in route.py).
- Blockers seen: (1) scooter r126 boxes in the rug toys (stances exist only without it) -> the scooter carry must work first;
  (2) carry walk with the 2.7 kg scooter fell twice (fast turn on the spot; walking 0.18 at the normal height) -> code now:
  heavy load (>=1 kg in holds) turns in 0.2 rad steps at 0.15 rad/s with stands, walks <= 0.10 m/s; testing CARRY_LOW
  from checkpoint 0038_hold_r127_held (robot holding r127 lifted at its take stance);
  (3) coat pile: fold grip needed (cloth agent builds it); (4) shoe mat spots under cloth -> shoes at the end;
  (5) umbrella r107: no place to stand within 12 cm of its spot (tolerance 0.15) -> end.
- Tools: scripts\home\live\route_v3_setup.py (route_v3_resume, play(n), hot_reload, OVR overrides saved in RESULT),
  live\watch.py (stills of feet + robot from a checkpoint to a failure), scripts\home\join_chain.py (episode from the chain).
- Kitchen agent a9645414001c2dbf1 (E:\urc_cloth): close_dishwasher fixed at release, commit 740863c on home-cloth, being
  proven end to end from seg3 0000_item_start; merge when it reports proven.

## HAND-OVER 19 Nov ~16:45 (fourth home agent; working memory getting low). READ THIS FIRST.
Code: E:\urc_home, branch home-cleaning (all committed, as abdullahanxie, no push). Room FROZEN: rooms\apartment_1122_full.json
(sha256 in rooms\apartment_1122_full.FROZEN). NEVER rebuild it (checkpoints would break). Live session: port 47960, slot "home",
run folder C:\Users\raresense\sim_home\runs\1119_152622_route_v3_seg3 (textured: URC_TEXTURED=1, URC_ROUGH_FLOOR=0.8).
### Episode chain (the real episode): checkpoints\0000_item_start -> 0066_item_r123i1_slipper. 1 of 65 items done.
Everything else in that folder is attempts / side branches (0120_NOT_ON_CHAIN_* is a bogus skip). Pieces of video per load
are in pieces.json; join with: py -3.12 E:\urc_home\scripts\home\join_chain.py OUT_DIR <final checkpoint dir> <run dirs...>
### How to play (live, in the session; send code with scratchpad snd.py or scripts\isaac_cmd.py --port 47960)
  exec(open(r"E:\urc_home\scripts\home\live\route_v3_setup.py").read())   # vis, OVR overrides, play(), hot_reload()
  route_v3_resume(r"...\checkpoints\0066_item_r123i1_slipper")            # state + route position + overrides
  route_v3_proven_first(); play(n)                                         # items one by one, checkpoint after each ok item
  Every action saves a checkpoint first (NNNN_act_<action>, meta.json info = the call). hot_reload(path, names) for code fixes.
  watch.py: watch_from(ckpt, "<call>", t0, t1) = stills of feet + robot; its cameras go inside walls near walls (fix: top view).
### NEW USER RULE (16:45): TRUE TELEOP. Small moves only (<= 0.15 m or <= 15 deg), stand, LOOK at 3 views (feet + floor,
side with knees / hands / held thing, top or room view), decide the next move from what is seen; checkpoint before every move;
crouch / reach / grip / lift / put in small increments too. No long walk_path legs. (Not built yet when I stopped: a
teleop.py with tmove(dx, dy, dyaw) + look3() composite; cameras must be placed toward open floor / from above.)
### What blocks items (all seen in frames or checked on the grid)
- Scooter r126 boxes in the rug toys (3 toys get a stance only if it moves 0.3 m east); it cannot be reached from its west
  take side (no free path). Coordinator's idea: PUSH it 0.3 m east by one hand low on the deck / stem base (slide, not tip).
- Carrying the 2.7 kg scooter (r127): take + lift WORK (look\sc_r127i1_scooter_t3_closed_bar_top.jpg, t4_lifted). Walking
  with it fell 4x: fast turn (fixed: stepped turns 0.2 rad at 0.15 rad/s, now in skills for >= 1 kg loads), walking at the
  normal height (run-off), low carry (shin hits the stem foot, look\watch_lowcarry_t0313.00_feet.jpg), hands forward (stem
  foot swings between the legs, look\watch_fwdcarry_t0302.00_robot.jpg). Checkpoint holding it: checkpoints\0038_hold_r127_held.
- Duck r120i2 and dollhouse r188 (toy corner, far west): both FELL while walking there (duck: pelvis on object_0135 41 N, foot
  on the toy basket; dollhouse: the walk to (-4.75,-1.3) at t 293-297 near the west wall). Checkpoints before the falling walks:
  dollhouse 0294_act_walk (call walk((-4.75,-1.3,-0.644), tol=0.05, carry=[])). To be redone by teleop.
- Coat pile (and garments): pads close above the flat cloth (look\ct_*.jpg of run 1119_144818); fold grip = cloth agent's job.
- Shoe mat spots are under the blanket / coat pile -> shoes after the garments. Umbrella r107: no stance within 12 cm of its spot.
### Kitchen: close_dishwasher PROVEN by the cloth agent (a9645414001c2dbf1) in the frozen room, home-cloth commit fe75acc:
merge home-cloth (code only) and play ["close_dishwasher", {...route_steps_v3 form...}] from the current chain checkpoint.
### Other agents: coordinator = main (SendMessage "main"); cloth/kitchen agent a9645414001c2dbf1 (E:\urc_cloth).

## 19 Nov ~16:55: OLD CHAIN STOPPED (user's decision: five-finger Inspire hands). The Dex1 chain ends at
C:\Users\raresense\sim_home\runs\1119_152622_route_v3_seg3\checkpoints\0066_item_r123i1_slipper (kept as the record; invalid for
the new robot). Last Dex1 work there: teleop of the duck r120i2 from 0257_act__turn_on_spot (one 15 deg turn seen fine,
tele\0002_duck_turnR1.jpg; teleop tool scripts\home\live\teleop.py: tmove(fwd, side, turn) + look3 composite of 3 views).
NEW ROOM (frozen): E:\urc_home\rooms\apartment_1122_full_inspire.json, sha256 A8D5393C0A7EE1B07B6F9FFE7C79FEBEC9BB1A6C6F49F56FC2A7B8A5491CD303
(robot g1_inspire = setups.json g1_inspire, C:\Users\raresense\sim_wbt\models\scene_g1_inspire.xml; everything else identical).
Code: boot.py takes the robot from the room; skills.HANDS = "fingers" (hand_pose(s, k) from the set-up's open / closed poses);
cloth worlds collide with the wrist links when there are no Dex1 pads. NOT yet ported: pads()/grip_check/close_jaws/pick
skills (all Dex1 jaws), cloth grips. Cabinet-task finger code to reuse: E:\urc_main\scripts\cabinet_isaac\k12_grasp.py,
k14_hold.py, cabscene.py.

## HAND-OVER 19 Nov ~17:05 (fourth home agent stopping: working memory used up). READ THIS FIRST.
ROBOT NOW: G1 + five-finger Inspire hands (user's decision 16:45). FROZEN room: E:\urc_home\rooms\apartment_1122_full_inspire.json
(sha256 A8D5393C0A7EE1B07B6F9FFE7C79FEBEC9BB1A6C6F49F56FC2A7B8A5491CD303; robot g1_inspire from configs\robots\setups.json ->
C:\Users\raresense\sim_wbt\models\scene_g1_inspire.xml, the same build the recipe agents use). Never rebuild it.
NEW EPISODE CHAIN: C:\Users\raresense\sim_home\runs\1119_163920_route_inspire_seg1\checkpoints\0000_item_start (start; 0 items).
Seen working: Inspire hands open / closed by the posture reference (tele\hands_open.jpg, hands_closed.jpg in that run).
Old Dex1 chain (record only): ...\1119_152622_route_v3_seg3\checkpoints\0000_item_start -> 0066_item_r123i1_slipper.
### Start a session and play by TELEOP (user's rule: small moves <= 0.15 m / 15 deg, look after each, checkpoint before each)
  set URC_NEWTON_CPU=1, URC_QP_SOLVER=daqp, URC_TEXTURED=1, URC_ROUGH_FLOOR=0.8
  py -3.12 E:\urc_home\scripts\home\live\newlive.py <TAG> E:\urc_home\rooms\apartment_1122_full_inspire.json
  then in the session: exec route_v3_setup.py, teleop.py; route_v3_resume(<chain checkpoint>) (one session = one run folder)
  tmove(fwd=, side=, turn=deg, carry=(side,)) -> {at, yaw, look=<composite jpg: feet | side | ahead>}; look3(tag).
  Hands: ts.ctrl.set_posture(hand_pose(side, k), ts.s, duration=0.6) with k 0 (open) .. 1 (closed).
### TO DO next (in order)
1. Finger grasps into the library (port from E:\urc_main\scripts\cabinet_isaac\k12_grasp.py, k14_hold.py, cabscene.py): pinch
   (thumb + index / middle) for small things and cloth, power grasp for bars (scooter handlebar); contact-verified hold = finger
   and thumb contacts on the thing. skills.pads() / grip_check / close_jaws / open_jaws / pick_floor / put_down are still Dex1.
2. Recipes per item: C:\Users\raresense\sim_home\apartment\recipes\<item>.json (offline agents) = starting plan for each teleop.
3. Route by teleop from 0000_item_start: slipper first (aside spot by the toy bike (-0.75,-2.2), its mat spot is under cloth).
4. Kitchen agent a9645414001c2dbf1 (E:\urc_cloth) ports dishwasher / sink / tables / garments to the fingers; merge home-cloth
   (code only) when it says a step is proven, play it from the route checkpoint in YOUR session.
5. ~21:00: join what exists: py -3.12 E:\urc_home\scripts\home\join_chain.py OUT <final chain checkpoint> <run dirs>; then
   video_check (done by the joiner) and py -3.12 C:\Users\raresense\sim_home\apartment\full_plan\check_clean_look.py RUN --out ...
### Lessons (seen in frames, keep)
- Walking empty: ground_follow off + joint arm tuck = green. Turns on the spot drift ~0.1 m/rad.
- Heavy carry (scooter 2.7 kg in front): stepped turns work (0.2 rad at 0.15 rad/s + stand); walking with it fails (legs reach
  its stem foot when low; run-off at the normal height). Scooter r126 boxes in the rug toys; r126's west take side has no
  free path; coordinator's idea: PUSH it 0.3 m east, one hand low on the deck (frees 3 toys, checked on the grid).
- Coat pile: pads close above flat cloth -> grasp across a fold (cloth agent). Shoe mat spots lie under the cloth.
- Long walks to the far west toy corner fell twice (duck r120i2, dollhouse r188) -> teleop there.
- Checkpoint hygiene: an item's act/roll checkpoints are pruned only for that item; numbers never reused; pieces.json per load.

## 19 Nov ~17:55 (fifth home agent, Inspire hands, TRUE TELEOP; AI-operated) - 2 of 65 items done. READ THIS FIRST.
EPISODE CHAIN (Inspire): seg1 C:\Users\raresense\sim_home\runs\1119_163920_route_inspire_seg1\checkpoints\0000_item_start
  -> run 1119_164726_inspire_tele2 ...\checkpoints\0133_item_r123i1_slipper   (slipper put ASIDE by the toy bike at (-0.74,-2.21),
     clear of every garment footprint; to the mat at the end)
  -> run 1119_172920_inspire_tele3 ...\checkpoints\0123_item_r195i3_paper      (paper in the rubbish bin)
  Route: POS 2 of 65, next r107i1_umbrella (route_v3_proven_first order: umbrella, duck r120i1, rug toys, ...).
  NOTE: an act checkpoint carries the route state of the session START: after loading one, set DONE / POS by hand (see below).
### Code (E:\urc_home, branch home-cleaning, commits c4289da, 6dc92e4; as abdullahanxie, no push)
- scripts\home\finger_skills.py (loaded last by episode.py): pads/pad_mid/gap/close_jaws/open_jaws/grip_check/hold_on for the Inspire
  hand. FSHAPE[side]: "pinch" or None (power wrap). grip_check = simulated contacts: thumb + an opposing finger on the thing,
  both loaded. hold_on = contact-verified hold + lock_fingers (every finger joint holds the angle where it met the thing +0.03 rad,
  a stiffness servo via a dynamic gripper shape "held": no curling past the thing, coordinator's request).
- scripts\home\live\teleop.py: tmove (turn <= 15 deg at 0.15 rad/s with a settle stop BEFORE and after; step <= 0.15 m), thand / hand_to
  / place_step (hand moves <= 4 cm near things, <= 8 cm in free air), tgrip, tpose, look3 / look_hand (3-view composite after
  every move in RUN\tele\), step_wp (aim at a way point), near_things, R_tilt, tele_item_done (records + item checkpoint + prune).
- skills.fallen(): the deep squat (pelvis 0.33 m) is no longer a fall (needs the trunk tipped over or pelvis < 0.22).
### THE FLOOR GRASP THAT WORKS (seen twice: slipper 4.7 cm tall, paper 3 cm tall)
  The Inspire "pinch" shape cannot take a low thing off the floor (thumb closes 5-6 cm above the finger tips). Instead:
  power wrap OPEN (open_jaws(s, shape=None)), deep squat in 3 steps (-0.20/0.35, -0.30/0.6, -0.38/0.8), hand orientation
  R_tilt(c, phi) with c = the robot's left (outward) for the left hand: fingers down and outward, thumb toward the body;
  phi 30 deg for a 4.7 cm thing, 42 deg for a 3 cm thing (thumb and finger tips LEVEL); hand_to over the thing so that thumb tip
  and finger tips are each ~6.5 cm from the centre along c, descend to tips 1.5 cm above the floor, close_jaws(s, 10) ->
  grip_check -> hold_on (locks fingers) -> lift 4-6 cm -> crouch_holding(("left",), -0.22, 0.4) -> crouch_holding(..., 0, 0).
  Stance for the floor grasp: thing at 0.12-0.20 ahead, 0.25-0.31 to the hand's side (in_reach(point, side)).
  Drop into the rubbish bin (0.10,1.48, top 0.40): stand 0.49 ahead / 0.14 left of its centre, crouch_holding(-0.12, 0.45),
  place_step 4x8 cm over the opening at bottom 0.50, open.
### Lessons seen in frames (keep)
- Forward 0.15 m steps drift 20-45 deg sideways after a turn; re-aim every step (step_wp). Side steps are erratic (moved 0.17 / 0.10 /
  south instead of right). Backward 0.15 m steps are stable. Watch the croc r122i1 (box x -0.55..-0.33, y -1.04..-0.81) and the
  jacket (x 0..0.74, y -1.61..-1.16): the passage between them is narrow; the feet touched the jacket's edge twice without dragging it.
- RAM: kit private bytes grow ~0.4 GB per minute of teleop (14.4 -> 24.0 GB in 22 min, run 1119_172920 kit_mem.csv); restart from
  the last item checkpoint after EVERY item (coordinator's rule: when kit passes ~9 GB working set). Cause not found yet.
### How to continue (one session = one run folder)
  set URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp URC_TEXTURED=1 URC_ROUGH_FLOOR=0.8
  py -3.12 E:\urc_home\scripts\home\live\newlive.py <TAG> E:\urc_home\rooms\apartment_1122_full_inspire.json ; start h_live.py guard 47960
  in the session: exec route_v3_setup.py; exec teleop.py; route_v3_resume(<last item checkpoint>); then step_wp / thand / tgrip ...
  scratchpad sender: py -3.12 <scratchpad>\snd.py <codefile> (port 47960).

## HAND-OVER ADDENDUM 19 Nov ~18:05 (fifth home agent stopping: working memory nearly used up). My Isaac is stopped (slot "home"
## free, no orphans). Everything committed on home-cleaning (last 4dbf94f).
- CHAIN END = C:\Users\raresense\sim_home\runs\1119_172920_inspire_tele3\checkpoints\0123_item_r195i3_paper (2 of 65 done:
  slipper aside, paper in bin; robot standing at (0.25,0.95) facing north by the rubbish bin). Run 1119_175501_inspire_tele4 holds
  only a load + memory tests (no moves): start a NEW run folder from 0123.
- RAM LEAK FOUND AND FIXED: boot.close() toggled the check camera's render texture per picture, ~80 MB leaked per close-up
  (4 look3 = +0.9 GB). teleop.py now keeps the check camera on (4 look3 = +0.12 GB, stepping = 0). Still check kit private bytes.
- Next route items (route_v3_proven_first order): r107i1_umbrella (0.95,-0.54) dest "by the entry (floor)" - earlier: no stance
  within 12 cm of its spot, consider the end; r120i1_duck (2.03,-1.7) -> toy basket r186i1 (-5.2,-1.4) (long carry); rug toys
  r192/r193/r191 (x -2.5..-3.5, y -1.3..-2.15) -> basket (short carries, scooter r126 boxes in 3 of them: push it 0.3 m east first,
  one hand low on the deck, only if seen safe). Recipes per item: C:\Users\raresense\sim_home\apartment\recipes\<item>.json
  (paper recipe's stance differed from mine; my floor grasp recipe above worked twice).
- Known gotcha: route_v3_resume(<act checkpoint>) restores the route state of the session START; fix DONE / POS by hand
  (DONE[:] = [...]; move the done items to the front of ROUTE; POS = len(DONE); route_v3_proven_first()).

## 19 Nov ~18:35 (sixth home agent, Inspire, TELEOP; AI-operated) - working notes, 2 of 65 done
- ROUTE-STATE BUG FIXED (commit 3dbd8ea): every checkpoint (item/act/roll) now has info.route (POS/DONE/SKIPPED/ROUTE);
  route_resume keeps the pkl-restored state if a checkpoint has none. VERIFIED LIVE: resume from act ckpt
  ...\1119_180636_inspire_tele5b\checkpoints\0034_act_tele_move gave POS 2, done [slipper, paper], next r192 ball.
- Deferred to the end (route_defer in my session code, kept in the checkpoints' route): r107i1 umbrella (dest spot (3.2,-2.57)
  by the entry boxed in by blanket/coat pile/stroller/red bags), r120i1 duck (no stance until blanket, umbrella r106, coat pile gone).
- Toy basket r186i1 is at world (-5.18,-1.4) in the toy corner (NOT on the rug as the recipes assume). Rug east side is walled
  off from the toy corner (coordinator). Way from the bin to the rug's east: (0.06,0.77) -> (-0.15,-0.1) -> (-0.7,-0.6) passing
  0.35 m west of the croc -> (-1.05,-1.2) -> corridor y -1.0..-1.5 between light saber r130 / scooter r126 and heater r132 / hamper.
- RAM: the h_live guard (under 2.5 GB available) stopped my Isaac 3 times (18:06, 18:25, 18:3x): Premiere Pro 4.5-15.6 GB +
  the cloth agent's Isaac + offline recipe jobs. A guard stop looks like "Simulation App Shutting Down" in isaac_47960.log.
- Session helpers (scratchpad ops.py): lookq (compact views), occ_map (text nav grid), go(wp, fmax) = step_wp + compact report,
  kit_mem. NEVER define a global named look_at in the session: boot.close() uses it (I broke it once and restored it).

## 19 Nov 19:25 status (sixth home agent; AI-operated). PC rebooted 19:19 (power cut). Still 2 of 65 done.
- MODE since 18:45 (user): AUTONOMOUS item runs with a monitor; the AI looks only at item ends and failures.
  Code: E:\urc_home\scripts\home\live\autorun.py (monitor: fall/tilt, held thing lost, robot or held thing pressing furniture
  > 60 N or a loose thing > 20 N, foot on a loose thing > 3 N, neighbour moved > 3 cm, item time cap; raises Abort; static =
  any body not in INFO bodies, incl. scene_static / the rug). pick_floor_fingers (teleop-proven tilted open wrap, works
  from where it stands if the thing is in reach), squat_follow, walk_tight (0.22-0.26 m clearances), walk_via (stop+turn
  at each way point), drop_over (stance FACING the basket 0.40 ahead; library put_down has no feet room at the basket).
- r193i1 toy piece picked (left hand) from the rug pocket and being carried to the toy basket (-5.18,-1.4) by the north
  hall loop. Failures seen + fixed: walk_path ran through a shallow corner and into the hall wall (monitor stopped it at
  95 N on the right wrist) -> walk_via legs; second-hand pick while holding: the deep squat turned the robot 17 deg and
  stepped it back 0.12 m, the fingers pushed r193i3 7 cm -> one toy per trip for now.
- Resume point: C:\Users\raresense\sim_home\runs\1119_182912_inspire_tele5d\checkpoints\0122_act_walk_via (route state in it).

## 19 Nov ~19:40 ALL STOPPED by the user (coordinator note). READ THIS FIRST when work resumes.
- Every agent, both Isaac sessions, recipe runs and the 10-min report are stopped; no kit.exe left; heavy.lock removed.
- DECISION before the stop: back to the two-jaw Dex1 gripper (plan v3: 60 of 81 doable with the jaws; the Inspire hand
  adds nothing in this room). Use the Dex1 frozen room E:\urc_home\rooms\apartment_1122_full.json (sha in
  apartment_1122_full.FROZEN). Resume the Dex1 chain from
  C:\Users\raresense\sim_home\runs\1119_152622_route_v3_seg3\checkpoints\0066_item_r123i1_slipper (1 item done).
  Skills must pick jaws or fingers by hand type (finger_skills.py stays for later).
- MODE: autonomous item runs (autorun.py monitor, checkpoint before every action); the AI looks at item ends + failures.
- Next items: close_dishwasher (proven with the jaws in this room: home-cloth fe75acc, run
  1119_1622_live_frozen_close_dishwasher_e2e_v2_from_seg3_start), paper r195i3 into the bin, then floor items in route order.
- The Inspire chain (2 items: slipper, paper; last ckpt 1119_182912_inspire_tele5d 0122_act_walk_via) is kept as a record.

## 19 Nov ~20:30 DEX1 FLOOR (seventh home agent; Dex1 jaws again, AUTONOMOUS item runs, AI-operated). READ THIS FIRST.
- Order (user 19:45): switch to the Dex1 gripper, clear the WHOLE FLOOR first, fast. Room: E:\urc_home\rooms\apartment_1122_full.json
  (sha D230C315... checked). Chain: seg3 0066_item_r123i1_slipper -> run 1119_193653_dex1_floor_1 0058_item_r195i3_paper
  -> (PC reboot 20:03) run 1119_200527_dex1_floor_2 0044_item_r195i1_paper. Chain items done 3 (slipper, 2 papers).
- Code (E:\urc_home, home-cleaning; home-cloth merged a96eabe; commits 5e47dbe f3c4f29 1847a04):
  autorun.py by hand type: Dex1 -> _run_item_jaws = library pick_floor + put_away_any (tight 0.24/0.14 fallback) or
  tidy_garment for cloth; finish_put(nm, side) to finish after a stop with the thing held; back_off_container at item
  start; CREEPERS (clementines on the sofa creep by themselves); neighbour check only within 1.2 m and not for things
  inside containers. skills.py: grasp_plan falls back to the plan's grasps_v2.json (plan_grasps_v2, moved with the
  thing); Dex1 hold_on locks the jaws where they met the thing (JAW_LOCK_SQ 1.2 mm; without it the 12 N jaws sank
  through the paper and grip_check failed while held); grip_check while held needs 0.4 N a jaw; a tall container (bin)
  is always a drop; drop_in ignores what already lies in the container.
- Session: newlive.py dex1_floor_N rooms\apartment_1122_full.json (env URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp URC_TEXTURED=1
  URC_ROUGH_FLOOR=0.8); then exec route_v3_setup.py, teleop.py, autorun.py, scratchpad ops.py (floor_first(names),
  go_item(), kit_mem); route_v3_resume(<ckpt>); go_item() per item. Write session code with the Write tool (PowerShell
  Set-Content adds a BOM the session cannot parse).
- Coordinator's speed order (20:20): two per trip where close (tidy_two), ONE basket round for the rug toys
  (basket_skills.basket_round), each trip ending near the next. Route head now: knit hat, santa hat, duck r120i2, rug toys,
  stocking, plastic bag, jacket, blanket, coat pile, rag; then shoes, ducks, cups, scooters, umbrellas, box.
- 21:00 status (Dex1 floor agent): still 3 chain items (no new item since 20:14). What blocks, all seen:
  * HAMPER (-2.15,-1.95) has no cloth drop stance with normal clearances (heater r132 east, round side table west, rug
    toys north). Tight clearances: knit hat carried in from the north swept rug toy r193i1 3.8 / 5.6 cm (cloth hangs low);
    jacket: the tight side stance put the left knee on the heater (125 N, monitor stop) and from there the hand stays
    0.29 m short of the opening (look\hamper_top2.jpg, run 1119_200527). => clear the rug toys first, then garments.
  * TOY CORNER: walk_to_stance's pre-stance point near the corner rug edge: the end correction turned 2.4 rad on the spot
    and drifted 0.3 m into cup r197 (knee 22-26 N); straight approach (pre_stance off) reached the plastic bag stance but
    the surface pinch closed on air, then a foot touched duck r120i2. Traced with MON["trace"] (autorun monitor hook).
  * Session gotcha: NEVER assign session globals named TR or LOG (TR is the Trace logger that savegame restores; I
    clobbered it once and restored it from gc). Use Write-tool files for session code.
  * Trying now: run_basket_round(RUG) from 0044 (basket from the toy corner to the rug toys and back).
- 21:35 ROOT CAUSE of the toy-corner failures (seen in the pelvis trace, MON["trace"]): the living-room rug r141 ends at
  x = -4.945 (y -2.235..-0.105). Every walk south into the toy corner ran ALONG that edge (x -4.75..-5.0) with one foot
  on the rug and one off, and the gait ran away sideways to the west (0.35 m in 1 s, t 695.1-695.9 of the basket round
  from 0044) into cup r197 / flat r125i1 / duck r120i2. FIX TO BUILD: no walking leg along a rug edge: legs parallel to
  an edge keep >= 0.30 m from it (on the rug x >= -4.65, or off it x <= -5.25), and edges are crossed square on. Trying
  now: pre-walk via (-4.0,1.05) -> (-4.65,0.8) -> (-4.65,-0.98) -> west across the edge, then the basket round.
- run_basket_round(names) (autorun.py): monitored basket_round + route bookkeeping; with_tight(...) for the clearances;
  checkpoint 0434_item_basket_round_0 in run 1119_200527 is BOGUS (nothing went in; status bug fixed), NOT on the chain.
- Chain end is still C:\Users\raresense\sim_home\runs\1119_200527_dex1_floor_2\checkpoints\0044_item_r195i1_paper (3 items).

## HAND-OVER 19 Nov ~22:00 (seventh home agent, Dex1 floor; working memory used up). READ THIS FIRST.
- CHAIN END: C:\Users\raresense\sim_home\runs\1119_200527_dex1_floor_2\checkpoints\0044_item_r195i1_paper. Chain items
  done 3 of 63 (slipper aside, paper r195i3 + paper r195i1 in the bin); floor items done 2 this session. Robot standing
  by the bin. Load with route_v3_resume(...) after exec route_v3_setup.py, teleop.py, autorun.py (see 20:30 section).
  Its route order still has the plastic bag next: re-run floor_first([...]) after loading (scratchpad ops.py lost with
  the session; it is: floor_first(names) moves names to ROUTE[POS:] front; go_item() = run_item + compact print).
- My Isaac is STOPPED and slot "home" freed (h_live.py stop). Last commit 4351a72 + this note.
- THE FLOOR IS BLOCKED IN THREE PLACES (all seen; each had 3+ fixes):
  1. Toy corner (basket r186, duck r120i2, plastic bag r196, cups r197/r173, flats r125, box r175): the only way in from
     the north is the strip x -4.95..-4.35 between the sofa's west end (x -4.35) and the rug r141's west edge (x -4.945),
     with flat r125i2 (-5.05,0.02), cup r197 (-5.2,-0.55) and flat r125i1 (-5.5,-0.43) just west of it. Walking along the
     rug edge the gait runs away sideways (west, 0.35 m/s); at x -4.65 the hip hit the sofa (113 N); at x -4.72 the robot
     drifted to -4.85 and a foot touched the flat (9 N). Ideas: enter the toy corner ON the rug from the east (from the
     rug toys) and cross the edge square on at y -0.98; or first take flat r125i2 / cup r197 with the arm reaching from
     the rug side; or a slower walk (0.10 m/s) for that strip.
  2. Hamper r133 (-2.15,-1.95): cloth drop_stance (side-high mode, SIDE_CLEAR 0.30, container kept as obstacle) finds no
     place in THIS room (heater r132 east at (-1.72,-1.63), round side table west, rug toys north). The cloth agent's
     proven hamper runs (1118_212840, 1118_231249) were in a different layout. Tight clearances: the knee hit the heater.
     Garment GRASPS work (knit hat 3/3 held, jacket held first try). Idea: move the hamper (1.6 kg loose body) 0.3-0.4 m
     north-west onto open floor first, or clear the rug toys and use the north side stance.
  3. Doormat r119 (shoes' spots) is under the blanket and the coat pile (garments -> hamper first).
  => The rug toys + basket round (run_basket_round in autorun.py; plan_hub finds a hub only with 2 of 6 toys) is the
     unblocker for both the hamper's north side and the toy corner.
- Things learnt and kept in code: Dex1 jaw lock after the hold (JAW_LOCK_SQ), plan grasps_v2 fallback, bin drop rules,
  monitor creepers (clementines, bin), container contents ignored, back_off_container, put_away_any / cloth drop tight
  fallback, MON["trace"] pelvis trace (set MON["trace"] = [] then read it; hot-reloaded _on_step_mon must be put into the
  chain with _WATCH_STEP0 = _on_step_mon when watch.py is loaded).

## 19 Nov ~23:00 (eighth home agent, Dex1 floor; AUTONOMOUS, AI-operated). Working notes.
- Session: run C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3 (Isaac pid of kit in slot "home"), resumed from
  1119_200527_dex1_floor_2\checkpoints\0044_item_r195i1_paper. Bogus ckpt renamed 0434_NOT_ON_CHAIN_item_basket_round_0.
  Load order: route_v3_setup.py, teleop.py, autorun.py, aside.py, ops.py (all in scripts\home\live). Chain still 3 of 63.
- HAMPER cannot be moved usefully (computed on the nav grid, maps look\grid_map.png / grid_map_west.png): its west and
  south sides are unreachable from the east even with 0.22/0.12 clearances; it is reached only from the north strip
  between rug toys r193i1/r193i3 and the heater, so it can only be pulled north (5-10 cm from the heater, closing the one
  east-west corridor y -1.15..-1.35). Every drop stance had r193i1 (object_0319) 0.10-0.24 m from the pelvis.
- DONE: r193i1 SET ASIDE (not a chain item; still goes to the basket) at (-2.927,-0.581), pocket by the coffee table's
  east end: ckpt ...\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece (set_aside in aside.py).
  r193i3 (object_0321) failed 4 fixes (turn runaway x2, foot on ball r192, sideways drift into scooter r126 from an east
  stance): left where it is; with r193i1 gone the side stances at (-2.1..-2.25,-1.4) have >= 0.3 m to it.
- SEEN: after ready_to_walk's ARM TUCK every turn on the spot near the coffee table ran away 0.3-0.5 m (113 N knee on the
  table, 88 N into the sofa); the same turn without the tuck drifted 6 cm (probes from ckpt 0111). Session runs with
  TUCK_JOINTS = False now (set it again after a restart). Session globals I clobbered once: rel (restore with
  hot_reload(skills.py, ["rel"])). Prefix scratch globals with zz_.
- cloth_skills.drop_stance now prefers 0.35 m pelvis room to small floor things and 0.32 m to furniture
  (STANCE_LOW_ROOM / STANCE_FUR_ROOM; hot_reload does not take tuple-assigned constants: set them by hand).
- autorun garments: tidy_garment retried with tight clearances when no cloth grasp stance is reachable (knit hat from
  the pocket).

## HAND-OVER 19 Nov ~22:10 (eighth home agent, Dex1 floor; working memory low). READ THIS FIRST. AI-operated.
- CHAIN END: C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece
  (= 0044_item_r195i1_paper of run 1119_200527 + rug toy r193i1 set aside at (-2.927,-0.581)). Chain items done 3 of 63.
  Load: newlive.py dex1_floor_N rooms\apartment_1122_full.json (env URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp URC_TEXTURED=1
  URC_ROUGH_FLOOR=0.8); exec route_v3_setup.py, teleop.py, autorun.py, aside.py, ops.py; route_v3_resume(<ckpt>);
  then TUCK_JOINTS = False; STANCE_LOW_ROOM, STANCE_FUR_ROOM = 0.35, 0.32; floor_first([...]); go_item().
  Route head at the ckpt is the plastic bag; floor_first(["r189i1_santa_hat","r190i1_stocking","r131i1_knit_hat",
  "r121i1_jacket","r117i1_blanket","r116i1_coat_pile","r68i1_rag"]) puts the garments first.
- Isaac STOPPED, slot "home" freed. Code commits on home-cleaning: 495a2c3, 3cde5b9, 84ca557, c6402c6 (no push).
- ROOT BLOCKER OF THE WHOLE WEST LIVING ROOM = SCOOTER r126 (standing, deck E-W at x -2.14..-1.57, y -0.93..-0.63,
  handlebar at its west end). With normal clearances the west half (rug toys, hamper, pocket) is cut off from the east;
  with tight ones the only way is the corridor y -1.15..-1.35 between the scooter and the heater/rug toys, and the gait
  drifts 0.1-0.3 m sideways there. Seen in this session, all ending at the scooter: r193i3 east-stance walk (left shoulder
  27 N), knit hat walk from the pocket (left knee 27 N), santa hat walk (scooter knocked 3.2 cm). The 16:15 note said the
  same ("scooter r126 boxes in the rug toys; push it 0.3 m east"). => NEXT: move r126 out first (take + lift are proven,
  big_skills.sc_*; walking with it failed before: use stepped turns 0.2 rad at 0.15 rad/s and short BACKWARD legs, e.g.
  take from the west (stance in the pocket, facing east), lift 3 cm, back west 0.3, stepped-turn, ...; or its real
  destination by the south wall). Then the corridor and the hamper's north side stances (-2.1..-2.25,-1.4) are open.
- Garments then: drop stances at the hamper exist on the 0.24/0.14 grid (side/high facing W at (-2.1,-1.4), hamper on the
  left); r193i3 (object_0321, (-2.6,-1.47)) is >= 0.3 m from them. r193i3 failed 4 fixes (see above) and stays for the
  basket round. The rug ball r192 rolls at a touch (a foot came down on it, 8 N).

## 19 Nov ~23:20 (ninth home agent, Dex1 floor; AUTONOMOUS, AI-operated). Working notes.
- Session: run C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4 (slot "home", port 47960), loaded from the chain end
  ...\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece. Chain still 3 of 63. Session command files:
  C:\Users\raresense\sim_home\apartment\live_cmd\z_*.py (z_load.py = exec route_v3_setup/teleop/autorun/aside/ops + resume).
- SCOOTER r126 (scripts\home\live\scooter.py park_scooter_sofa, commit f506a06): target place = standing N-S along the sofa's
  east arm (x -2.14, y -0.15..0.46; open floor east of it 1.7 m wide), not the plan v3 corner (3.8 m of carrying).
  Seen and fixed: (1) from the walking crouch the reach to the 0.97 m bar sank the pelvis to 0.60 (knees 1.5 rad) and pushed
  it back 9 cm -> posture height 0 first (pelvis 0.72). (2) Two pinches on the ROUND bar cannot hold the pitch (5.3 N m
  needed, ~0.3 N m of jaw friction): the "lift" only tips it onto its far wheel; the hold spring then dragged the bar out of
  the jaws -> NO hold spring: wheeled like a real scooter (bar end up 3 cm, far wheel sliding, jaws squeezing 20 N, load
  1 kg a hand told to the controller). (3) The light saber r130's west end lies under the deck's east end (moves 3.6 cm
  with it; ignored as a neighbour). Backward steps 2 x 0.125 m WORK (bar 1.0-1.6 cm off the grip points).
  FAILED: turns with it: 10 deg step -> pelvis 18 cm south, bar 3 cm off; 5 deg steps -> 3.5 cm off; 5 deg + hands pushed
  back to their robot-frame place -> bar out of the jaws (scooter upright again in front of the closed jaws, tele\0019).
  => r126 moved to the END (3 fixes). The saber cannot be reached first: the walk round the scooter puts a knee on it.
- Getting OUT of the pocket east (for the knit hat etc.): planner tight way -> left knee on the scooter's stem foot 27 N
  (3 times); 90 deg turn on the spot at (-2.64,-1.07) -> 0.25 m west into ball r192; diagonal leg -> drifted 0.3 m LEFT in
  0.4 m and the hanging left gripper hit the scooter. Trying short re-aimed steps (step_wp) now.

## HAND-OVER 19 Nov ~23:30 (ninth home agent, Dex1 floor; PAUSED by the user: "solve the drift first"). AI-operated.
- CHAIN END unchanged: C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece
  (3 of 63). No new item finished this session.
- Useful act checkpoints (NOT on the chain; route state = the chain end with floor_first(garments)):
  * ...\1119_220839_dex1_floor_4\checkpoints\0237_act_transit_east_ok - robot OUT of the pocket at (-1.54,-1.38), east of
    scooter r126 (reached by short re-aimed steps, ops.step_to).
  * ...\1119_230636_dex1_floor_5\checkpoints\0077_act_pre_knit_hat_ok - robot at (-0.79,-0.18) facing north, east of the
    knit hat, the light saber avoided (walk_via (-0.75,-1.12) -> (-0.80,-0.15), hold off).
- Session load: C:\Users\raresense\sim_home\apartment\live_cmd\z_load2.py (exec route_v3_setup, teleop, autorun, aside, ops,
  scooter; route_v3_resume(chain); gait_on() = TUCK_JOINTS False, STANCE_*_ROOM 0.35/0.32, hold OFF, hold state reset,
  ARM_TUCK roll 0.15; floor_first(garments)). Call gait_on() again after every ck_load.
- GAIT merged: home-gait eb5a8a3 (8001a76) and 7556985 (106aa08), code only. Safe settings used: ts.loco.g["hold"] = False;
  file defaults TURN_BY_REF/TURN_TOL_REF/TURN_W_MIN = True/0.01/0.08, WALK_BY_ANCHOR etc. defined.
  Seen with eb5a8a3 at 0237: hold ON -> 90 deg turn (walk) TIPPED (pelvis moved 0.49 m), identical in a fresh session (not
  the reload); 0.4 m leg 1.8 cm off (good); short steps toward (-0.85,-0.85) did not converge / foot on the saber.
  Hold OFF: 90 deg turn moved 5.5 cm; 15 deg tmove turns moved 6-10 cm each, 0.12 m tmove steps drifted 7-11 cm sideways.
  Not yet tested: 7556985 in a session (loaded only, Isaac stopped right after).
- Items: scooter r126 at the END (turns with it lose the bar, scooter.py). Knit hat from 0077 (pre-merge code, hold off):
  3 cloth grasps MISSED (jaws closed on air, gap 5.1 cm, 0 N; tele\0017 of run floor_5) - to watch next. Light saber r130:
  set_aside pick failed (pads 5 cm above its grasp point twice) - it still lies with its west end under r126's deck.
- Isaac STOPPED, slot "home" freed.

## 20 Nov ~00:00 USER DECISION (coordinator note) - read before resuming the floor
- Do the EASIEST of the 63 items first; difficult ones go to the end ("first we need to solve the easiest of 63, then the
  difficult, we will see").
- AFTER the walking-drift fix: if a blocker in the apartment still cannot be solved after several real attempts (seen
  in frames, 3+ different fixes), the scene MAY be changed to make it work: move or remove the blocking thing (e.g. a
  toy, the light saber, the scooter, a cup in a tight corner). Not everything: only the hardest blockers, and only
  after trying. Every change must be listed (what, from where to where or removed, why) in PROGRESS.md and in the
  final episode notes. Changes are made in OUR frozen room as a new frozen version (record the new sha256); the chain
  then restarts from that room's start, so batch the changes together, decided BEFORE replaying the easy items.

## 20 Nov ~01:00 (tenth home agent, Dex1 floor; AUTONOMOUS + AI teleop fixes, AI-operated). Working notes.
- Walking fix merged into home-cleaning: f18e6a7 (home-gait 7e48bf0) + 54568a4 (0c297cb). load_floor.py gait_on() sets
  plan=True / hold off / arms at rest; settle_after_load() stands 4+1.5 s after a load (trunk levels). Verified at 0237:
  90 deg turn 2.1 cm / -0.5 deg, 0.12 m step 0.5 cm.
- Session: run C:\Users\raresense\sim_home\runs\1120_004212_dex1_floor_6 (slot home, port 47960). Command files in
  C:\Users\raresense\sim_home\apartment\live_cmd\f6\ (verify.py, chain.py, reload_item.py with ZZ_ITEM preset, ...).
- Chain 4 of 63: knit hat r131 in the hamper, ckpt ...\1120_004212_dex1_floor_6\checkpoints\0134_item_r131i1_knit_hat.
  Fixes (seen in frames): drop_in_cloth's carry place before rest was over the hamper from the north stance (arm hung on
  the wall 94 N) -> kept outside the container (cb151b2). back_off_container crouched to walking height 12 cm from the
  hamper: knee into it, robot fell backward (FALL_REPORT.txt) -> steps back at standing height (8276281).
- r193i3 SET ASIDE (not a chain item) to (-2.79,-0.605) (pocket's north end, 14 cm east of r193i1): its walk was knocked
  by the santa-hat walk (14 cm). The old aside spot (-3.05,-0.95) is BAD: the set-down hand ended on the coffee table and
  knocked the kids bottle (fixed from ckpt 0203 by a new spot). Ckpt 0223_item_aside_r193i3_toy_piece.
- Chain 5: santa hat r189 (autonomous, ckpt 0274_item_r189i1_santa_hat). Chain 6: jacket r121 (autonomous + teleop rest
  fix, ckpt 0379_item_r121i1_jacket); code: side step before the arm rests at a side stance (baef942).
- ESCALATED (20 Nov ~01:55): BLANKET r117 into the hamper. Grasp from (1.15,-1.39) held first try, carried fine. At the
  side stance (pelvis 0.54 m from the hamper centre) the hand reaches only 11 cm inside the north rim (pad 0.735); the
  blanket (hangs 0.77 m from a mid grasp) lies like a saddle over the north-east rim: 43% inside, the rest down the
  outer wall to the floor; after the jaws open it stays on the fingers and the hand's withdrawal pulled it out (15%).
  Teleop tried (all seen in frames, no gain): (1) after let-go lower the hand: stalls at 0.71 standing / 0.59 with the
  pelvis -0.10; (2) from 0448 (held) raise to 1.15 (lowest still 0.11), move over the centre (52% in), lower in 4 cm
  steps -> 45%; (3) squat -0.20 and lower: hand stalls at 0.63 (reach), 43%. Ideas: grasp near an EDGE/corner so it hangs
  as one strip and pile it from the bottom; a stance closer / facing the hamper; release half, then take the outside
  part from the floor and lift it over the rim. Checkpoints: 0448_act_unlock_grip (held over the hamper, before opening),
  chain end 0379_item_r121i1_jacket.

## 20 Nov ~02:05 PLAN of the next easy items (tenth home agent; offline, Isaac stopped while Fable works the blanket)
Resume from Fable's ..._item_r117i1_blanket (or 0379 + Fable's options). Load: set CHAIN, exec load_floor.py, gait_on(),
settle_after_load(); hot_reload cloth_skills.drop_in_cloth and autorun.back_off_container are in the committed files.
Positions are world (from items_left.txt of run 1120_004212_dex1_floor_6).
1. Rag r68 -> hamper (small cloth, like the hats: proven path). Then coat pile r116 -> hamper with whatever Fable found
   for the blanket (big cloth: same saddle-over-the-rim risk). If the coat pile fails 3 ways: to the end.
2. Shoes onto the mat r119 (only after blanket + coat pile are off it): sandal r124i1 (-0.24,-2.37) open floor by the
   entry; croc r122 (-0.40,-0.95) open floor (light saber 1.1 m); shoes r105i1/i2 (4.05,-1.65 / -1.83) side by side in
   the east (pairs on the mat, spots in the room file "spots"); the slipper r123 (aside at (-0.74,-2.22)) stays the
   route's LAST item (final="mat"). Flats r125i1/i2 lie in the toy corner -> later.
3. Small umbrella r107 (0.95,-0.54) -> its floor spot by the entry (put_down on a floor spot, written, not yet run).
4. Rug toys + stocking -> toy basket r186 (in the toy corner at (-5.18,-1.4)): ONE basket round (run_basket_round in
   autorun.py): ball r192 (-2.85,-1.31), r193i1 (aside (-2.927,-0.581)), r193i3 (aside (-2.79,-0.605)), r193i2
   (-3.50,-1.70), r193i4 (-3.20,-1.41), toy vehicle r191 (-3.52,-2.15), stocking r190 (cloth, SW of the santa hat's old
   place). The toy-corner entry failed before only through the OLD gait's sideways run-away along the rug r141 edge
   (x -4.945): first test that entry walk alone with the plan-mode gait (short legs, monitor on), then the round.
   Duck r120i1 (2.03,-1.7, east, open floor) and duck r120i2 / toy car r139 go with the basket later.
5. Plastic bag r196 (-4.45,-1.15, 2 cm flat) -> bin: the surface pinch closed on air before; after the basket round.
6. Tables (tissue r158 on the sofa side -> bin; pouch r149, wrapper r87 -> bin) before the kitchen; dishes -> sink r27
   need drop_in_sink (NOT BUILT, the sink has no collider in the pack) -> end. Scooters r126/r127, umbrella drag r106,
   dishwasher, door r159, light saber r130 (under r126's deck) -> end (hard).

## ESCALATION blanket: SOLVED by Fable (20 Nov ~03:25; AI-operated teleop, first attempt). READ before the coat pile.
- CHAIN END now: C:\Users\raresense\sim_home\runs\1120_015326_dex1_floor_fable_blanket\checkpoints\0592_item_r117i1_blanket
  (7 done; from_ckpt = ...\1120_004212_dex1_floor_6\checkpoints\0379_item_r121i1_jacket; route head: coat pile). Checked:
  blanket inside 1.0, below the rim 1.0, overhang 0, top of the pile 0.35 m; hamper / scooter / saber / toys moved 0.000 m
  (the only movers since 0379 are the known creepers far away: scraps r69, pouch r149, plates r67, same rate as in the
  floor robot's own run); robot standing at (-2.145,-1.466) facing south, arms at rest, jaws free. The checkpoint was
  loaded again and stood still. Isaac stopped, slot "home" free. No code change in E:\urc_home; the session helpers are in
  C:\Users\raresense\sim_home\apartment\live_cmd\fb\ (zz_help / zz_grasp / zz_arm / zz_pin .py + the numbered steps).
- WHY it failed before (seen): the blanket is 1.00 x 0.75 m. Any reachable floor grasp is within ~0.17 m of an edge (the
  feet stay off the cloth; only the WEST edge has a stance, tight clearances), so it hangs 1.0 m from the hand, the hand
  goes to 1.30 m at most, the rim is 0.59 m: about 0.3 m of the far end can never be lifted over the rim in one go.
  The rim's cloth friction (0.8) then keeps that tail outside whatever the hand does inside. The "hang 0.77" in the
  floor robot's note was measured with the cloth still on the floor.
- WHAT WORKED = HAND OVER HAND across the rim (each new hold nearer the far end, taken where the cloth is TAUT):
  1. Right hand takes the west edge middle (particle 136, sheet uv (-0.43, 0)) from stance (0.91,-1.50, 30 deg), tight
     clearances. Carry with CARRY_JOINTS = True (arm frozen as a joint posture): with the default zero-velocity hand
     command the hand swung 0.43 m out to the side in the first turn and hit scooter r126's handlebar (9 cm, monitor stop).
  2. FRONT stance north of the hamper facing south: pre-stance (-2.14,-1.20), raise the hand to 1.30 there, then two
     short steps to pelvis y -1.427 (0.275 m from the wall). 0.15 + 0.15 put the swing knee on the hamper (26 N at
     pelvis y -1.48): the last step must be 0.07. With the orientation left free the hand reaches 0.52 m ahead at
     1.0-1.2 m (over the hamper's centre); with fingers down only 0.30-0.34 m.
  3. Hold the first end high over the centre: the cloth runs taut from the north-west rim up to the hand. LEFT hand
     (fingers sideways, jaws closing fore-aft) closes on that taut strand (it cannot swing away as a free-hanging bunch
     does: that was tried at the mat and failed) -> hold at uv (-0.06,-0.30). Lift it over the centre, let the first
     end go (open, then hand UP and back: moving the open hand down through the cloth dragged it out, reloaded).
  4. The rest of the tail then stands as a fold just OUTSIDE the north-west rim at rim height (free air, 4 cm from the
     wall): right hand, fingers tilted 35 deg forward of straight down (reach), jaws straddling the fold -> hold at
     uv (0.06, 0.30). The two holds are symmetric about the sheet's middle: no point is farther than 0.58 m from a hold.
  5. Both holds up over the opening (1.06-1.14 m): 98.8% inside, nothing below the rim outside. Let the right go, lower
     the left to 0.73 m as far south as it reaches (inside 1.0, below rim 0.91), open, hand straight up (cloth dropped to
     0.40 m), hands back and to rest. Never open with the jaws one above the other: the cloth lay on the lower jaw and
     came up with the hand (seen twice); open with the jaws side by side or the fingers pointing down.
- Gotchas: both arms out over the hamper tilt the trunk 0.33-0.39 rad and bring the knees to 8-10 cm from the wall
  (pelvis sinks to 0.66): bring one arm back before working with the other. The arm near its reach limit moves in
  jerks (stalls, then jumps up to 5 cm): no press-pinch on the rim top itself. Choosing a hold by the sheet's own
  coordinates (ClothWorld._uv, zz_uv() in zz_help.py) is what made every regrasp a planned one.
- For the COAT PILE r116 (1.4 kg, longer): expect the same; use the same hand-over-hand (grasp, front stance, taut-strand
  hold, fold-at-the-rim hold, both up, lower one). A skill should be written from the fb\ steps (c06-c08 strand hold,
  c15-c21 rim-fold hold, c22-c28 lift / lower / let go) before it is run autonomously.

## 20 Nov ~03:25 (eleventh home agent, Dex1 floor; coat pile r116, AI-operated). Working notes.
- Session: run C:\Users\raresense\sim_home\runs\1120_032422_dex1_floor_7 (slot home, port 47960), loaded from the blanket chain end
  ...\1120_015326_dex1_floor_fable_blanket\checkpoints\0592_item_r117i1_blanket. Command files C:\Users\raresense\sim_home\apartment\live_cmd\f7\
  (a00_load.py = CHAIN + load_floor.py + bigcloth.py).
- SKILL (Fable's hand-over-hand made reusable): E:\urc_home\scripts\home\live\bigcloth.py. bigcloth_into(name, cont, s1, start,
  stop_after, uv) runs stages grasp, carry, step_in, first_end, strand, lift2, free1, fold, both_up, lower_release, retract; each
  returns ok + numbers + a look (tele\NNNN_bc_<stage>.jpg); stops at the first failed check (fix by teleop, then start=<next>).
- Coat pile r116: pattern 1.6 x 0.78 m, 1.4 kg, lay folded by the entry console (0.72..1.65, -2.59..-1.91). NO grasp stance with
  the garment's rotated footprint rect as a clearance (it blocks the whole straight north edge) -> bc_grasp_at(uv) keeps only the
  grid's foot clearance and walks with the garment out of the grid. Grasp uv (0, 0.30) (north edge middle, 6 cm in) from stance
  (1.00,-1.74, facing east), right hand: held first try (4 points), hang 0.77. Carry: ok (pre-stance (-1.946,-1.225) heading
  -105 deg). Step in: ok (wall gap 0.274, knees 0.11 m from the hamper, heater 0.18 m from the pelvis). Ckpts 0033 (held), 0051 (pre).
- KITCHEN (cloth agent a8de4ec1786177bfe, 20 Nov ~03:40): close_dishwasher proven again with plan-mode walking (run
  1120_0324_kitchen_dw_recheck_AI_operated). EXACT CALL when ROUTE[POS] is close_dishwasher, after the usual set-up:
    exec(open(r"E:\urc_cloth\scripts\home\kitchen_skills.py", encoding="utf-8").read())
    CREEPERS |= {body_of(n_) for n_ in ("r69i1_scrap", "r69i2_scrap", "r69i3_scrap", "r69i4_scrap")}
    r = step_mon()
  (code: E:\urc_cloth branch home-cloth 842ecdf, 51ee968, a5f5639; the scraps creep by themselves: false "knocked" without the line)
- Chain 8: coat pile r116 (bigcloth.py stages, ckpt ...\1120_032422_dex1_floor_7\checkpoints\0373_item_r116i1_coat_pile; inside 0.993).
- Rag r68 DEFERRED: flat (4 mm) at (3.2..3.5, 0.26..0.53) beside the OPEN dishwasher; no grasp stance even tight -> after close_dishwasher.
- Chain 9: sandal r124i1 on the mat (ckpt 0503_item_r124i1_sandal). The library put (crouch_holding) pushed the held sandal into the
  floor lamp r109's leg (1.68,-2.26) and the robot FELL backward; teleop fix from 0459: stance facing west (1.38,-2.08), squat_follow
  3 steps, set down at (1.34,-2.42). Puts on the mat: keep the hand away from the lamp legs (1.68..1.84, -2.11..-2.26) and the
  console's low shelf (y < -2.47); place shoes FLAT on the mat's open middle-west part (x 1.1..1.5, y -2.0..-2.35).
## FINAL TIDY PASS (do at the end, when the shoes are paired up on the mat)
- Sandal r124i1 rests tilted 40 deg against the console's low shelf at (1.34,-2.42): straighten it flat on the mat (coordinator 20 Nov).
- Chain 10: croc r122 on the mat (ckpt 0599_item_r122i1_croc); its room-file spot (1.1,-1.8) is 7 cm OFF the mat (mat x 1.07..1.97,
  y -2.47..-1.87, body object_0138): re-put at (1.20,-2.02), flat. Shoes r105: put them at (1.30,-2.25)/(1.43,-2.25), not the file spots.
- EAST HALL CUT OFF (tight grid): stroller r101, open umbrella r106, tote r102 block x 1.8..3.0 between the hall and the east
  (shoes r105, umbrella r107's spot (3.2,-2.57)). Umbrella r107 autonomous try: left knee on a static edge at (0.71,-0.38) 87 N,
  undone by reloading 0599.
- Chain 11: close_dishwasher with the kitchen agent's step_mon (ckpt ...\checkpoints\0868_item_close_dishwasher).
- WARNING (coordinator, from Fable's island work): grasps_v2.json can claim narrow sections that do not exist (sponge box 8x22x8 cm
  read as a 3 cm section from 3 vertices on a top-face diagonal). Before trusting a grasps_v2 candidate on a rigid item, check its
  width against the collision hull / live grasp_plan; a plain box wider than 7.9 cm every way needs two hands or is skipped.
- Chain 12: rag r68 in the hamper (ckpt ...\checkpoints\0943_item_r68i1_rag): bc_grasp_at uv (-0.10,0) from (3.10,0.66); the long
  carry needs CARRY_JOINTS = True (zero-velocity hand hit object_0225 at (1.57,1.73), 76 N); the last step into the hamper drop
  stance put the right knee on the hamper (45 N, monitor stop) with the rag already over the opening -> let go there, back off.
- Basket r186 (toy corner): basket_stance only with tight clearances: (-5.246,-0.984, -1.414), pre (-5.28,-0.767); plan_hub covers
  only ball r192 + r193i1 + r193i3 (hub (-2.88,-0.99)). Toy-corner entry walk test from 0943 running (walk_tight to the pre).

## HAND-OVER 20 Nov ~05:20 (eleventh home agent, Dex1 floor; AI-operated). READ THIS FIRST.
- CHAIN END: C:\Users\raresense\sim_home\runs\1120_032422_dex1_floor_7\checkpoints\0943_item_r68i1_rag  -> 12 of 63 done
  (+ coat pile, sandal r124i1, croc, close_dishwasher, rag this session). Load: CHAIN = <that>; exec load_floor.py; exec
  scripts\home\live\bigcloth.py; gait_on(); settle_after_load() (see live_cmd\f7\a00_load.py; drop the floor_first(GARMENTS_FIRST)
  effect with floor_first([...]) as needed).
- TOY-CORNER ENTRY WORKS with the plan-mode gait: walk_tight((-5.28,-0.767,-1.414)) from the hamper side went round by the north
  (way points (-1.35,-1.25) (-0.75,-0.25) (-2.5,1.0) (-4.7,0.8) (-4.8,-0.7) (-5.2,-0.85)), err 0.8 cm, no touch, nothing moved.
  Act ckpt AT the basket pre-stance: ...\1120_032422_dex1_floor_7\checkpoints\0994_act_toy_corner_basket_pre_ok (route = 0943).
  basket_stance(r186) exists only under with_tight: (-5.246,-0.984,-1.414). Next: run_basket_round([...]) under with_tight
  (duck r120i2, ball r192, r193i1/i3/i4/i2, vehicle r191; plan_hub covers ball + r193i1 + r193i3 near (-2.88,-0.99)).
- BLOCKED / deferred: shoes r105i1/i2 + umbrella r107 (its spot (3.2,-2.57)): the east hall is cut off by stroller r101 / open
  umbrella r106 / tote r102 (no path even tight; with the dishwasher closed check again via the kitchen corridor x 3.0..3.5).
  Puts on the mat: the library's room-file spots are bad (croc spot off the mat, lamp legs by the sandal spot): use zz_put.py
  zz_pick_put(name, spot) (live_cmd\f7) with spots on the mat's open part x 1.1..1.5, y -2.0..-2.35, flat.
- Skill bigcloth.py (commits 2462388, 7839022): big garment hand-over-hand; proven on the coat pile.

## HAND-OVER ADDENDUM 20 Nov ~05:50 (eleventh home agent stopping: working memory nearly used up). AI-operated.
- CHAIN END unchanged: C:\Users\raresense\sim_home\runs\1120_032422_dex1_floor_7\checkpoints\0943_item_r68i1_rag (12 of 63).
- BASKET ROUND (rug toys) FAILED twice, not on the chain:
  1. take_basket raised "inhomogeneous shape": CARRY_Z name clash (cloth_skills' (0.72,0.95) tuple vs basket_skills' 0.62) ->
     fixed: basket_skills BASKET_CARRY_Z (commit b612860). Re-exec basket_skills.py in a session that loaded it before.
  2. From 0994 (basket pre-stance): basket taken (both grips ok, rose 0.52 m) and carried the long way round (north, east, then
     south-west) toward hub stance (-2.59,-0.70); the planner routed it through the corridor between scooter r126 and heater r132
     (y -1.15..-1.35): the held basket hit the heater (object_0265, 24 N) and the left hip pressed the basket (21 N) at (-1.44,-1.22).
     Act ckpt before that last leg: ...\checkpoints\1050_act_walk_leg (robot at (-0.76,-0.40) holding the basket).
  3. Teleop try from 1050: way points north of the scooter ((-1.2,-0.38) ...): "no free path" even on the tight grid (sofa / scooter /
     light saber r130). => The basket cannot be carried to the rug toys while scooter r126 stands there. Options: (a) scooter r126 out
     first (scene change candidate: it is THE blocker of the west living room, see 19 Nov notes), (b) basket hub elsewhere, the toys
     by single trips, (c) light saber r130 moved. Basket round -> END of the easy list.
- Other items left reachable and easy: plastic bag r196 (-4.45,-1.15) -> bin (toy corner entry now works: walk_tight to
  (-5.28,-0.767,-1.414)); stocking r190 (cloth) -> basket. Shoes r105 + umbrella r107 need the east hall (blocked by stroller r101 /
  umbrella r106 / tote r102). Table rubbish / dishes: kitchen agent's calls.
- Isaac STOPPED and slot "home" freed at hand-over.

## 20 Nov ~05:28-07:10 (twelfth home agent, Dex1 floor; AUTONOMOUS + AI teleop, AI-operated). Working notes.
- Session: run C:\Users\raresense\sim_home\runs\1120_052805_dex1_floor_8 (slot "home" taken at 10.6 GB available with the coordinator's
  one-time OK to bypass the 12 GB start gate; guard on). Command files C:\Users\raresense\sim_home\apartment\live_cmd\f8\ (a00_load.py loads
  the chain; zz_put.py, zz_corner.py (corner pinch), zz_sc2.py (scooter re-grip + pivot steps)).
- Chain 13: plastic bag r196 in the bin (ckpt 0181). grasp_plan claimed a 5.25 cm section; the collider is a FLAT BOARD 15 x 20 x 1.1 cm (no
  such section). Fix: CORNER PINCH (zz_corner.py: jaws closing across a 90 deg corner 3 cm in along the bisector, 6 cm chord, pad mid z
  0.0255) held first try. finish_put under with_tight; its last turn at the bin put the left knee on the bin (88 N) -> from the act ckpt
  before that turn the bag was already over the opening: hand 3 cm to the middle, let go.
- Chain 14: stocking r190 in toy basket r186 (ckpt 0364). grasp_cloth only with_tight; the library let-go at pad 0.64 m left it on the
  jaws. Fix: squat_follow -0.20 / -0.30 with the hand, lower until it lies on the basket bottom, unlock, open, hand straight up.
  LOW basket (rim 0.12): let go in a squat.
- FALL walking out of the toy corner (with_tight) at (-4.8,-0.4): tight corridor 0.25 m at y 0 between flat r125i2 (5.7 cm) and furniture.
  -> Chain 15: flat r125i2 on the mat at (1.232,-2.259) flat (ckpt 0512): library put stance too far (0.33 m ahead) -> teleop squat
  -0.30 then -0.38/0.8 with the hand following, set down. Standing next to the mat, the first turn put a foot on the croc: step back first.
- SCOOTER r126: autonomous park_scooter_sofa (plan gait): take + lift + 2 back steps + two 6 deg turns OK, third turn: bar twisted out of
  the left jaw (pads 2.2 -> 3.5 -> 13 cm off). Fingers-down fore-aft grip: knocked the scooter over twice (reach). WORKS: re-grip after every
  step (zz_regrip: set down, open, hands back to the grip points, close, lift) + pivot about the FAR WHEEL (zz_pivot_step: side step +
  turn so the pelvis moves on the circle round the far wheel; the deck turns ~half the robot's turn). Every path ran the far wheel over the
  light saber -> scooter set down upright 0.26 m west (box x -2.43..-1.78, y -0.99..-0.58), act ckpt 0756_act_scooter_moved_west_saber_free.
  Releasing: open, hands UP 12 cm first, then back (moving back at once hooked the bar, 57-152 N); the stem ends 6 cm from the pelvis:
  step off with the scooter ignored by the monitor.
- Chain 16: light saber r130 at its spot (-4.92,-1.405) by the basket (ckpt 0840_item_r130i1_light_saber), autonomous zz_pick_put.
- ESCALATED (20 Nov ~07:35): SCOOTER r126 (chain end ...\1120_052805_dex1_floor_8\checkpoints\0840_item_r130i1_light_saber, 16 of 63;
  scooter standing upright at box x -2.43..-1.78, y -0.99..-0.58, bar at the west end (-2.28,-0.80), deck 8 deg, far wheel ~(-1.80,-0.72);
  robot in the toy corner). Seen: (1) autonomous turns lose the bar (twist); (2) fingers-down grip knocks it over / no reach; (3) re-grip
  cycles WORK and far-wheel pivots WORK (scooter.py sc_regrip / sc_pivot_step, commit 3d25075) but the deck turns only ~1/3-1/2 of the
  robot's turn, and the pivot circle (0.89 m round the far wheel) runs into the sofa (CW, y > -0.40 at x < -2.15) or the hamper/heater
  (CCW, y < -1.3 at x -2.45..-1.4) after ~25-50 deg; (4) PUSHING forward (far wheel leading, "wheelbarrow") jams: the scooter is one rigid
  body, its wheels slide, the push pressed it into the floor 71 N and the robot's knee walked into the stem (45 N); W moved 4 cm.
  Towing (walking backward) works, but from here it only leads west into the pocket. Open floor (tight grid, scooter left out): x -2.1..0.7,
  y -1.25..0.9 (sofa x < -2.15 for y > -0.40; hamper/heater x -2.45..-1.4 for y < -1.3).
  Code of this session: scripts\home\live\scooter.py sc_take2 / sc_regrip / sc_pivot_step / sc_fwd_step / sc_state (exec scooter.py after
  the loader; set TELE_V = V_CARRY_HEAVY, TELE_W = SC_PARK["turn_w"], CARRY_LOW False; MON["start"].pop(scooter) while held).

## HAND-OVER 20 Nov ~07:40 (twelfth home agent, Dex1 floor; AI-operated). READ THIS FIRST.
- CHAIN END: C:\Users\raresense\sim_home\runs\1120_052805_dex1_floor_8\checkpoints\0840_item_r130i1_light_saber -> 16 of 63 done
  (this session: plastic bag r196, stocking r190, flat r125i2, light saber r130). Route head after it: r105i1_shoe, r105i2_shoe, r107 umbrella,
  r127 scooter, r126 scooter (floor_first moves things to the front).
- Load: live_cmd\f8\a00_load.py (set CHAIN to the chain end; exec load_floor.py + bigcloth.py + zz_put.py), then gait_on(); settle_after_load();
  and (kitchen agent) refresh_jointed_footprints() after EVERY ck_load (else the floor map keeps the dishwasher door open).
- Scooter r126 ESCALATED to Fable (see the ESCALATED note above); skills in scooter.py (commit 3d25075).
- Toy corner: the walk OUT of it fell once through the 0.25 m tight corridor at (-4.8,0) (flat r125i2 there, now gone: corridor wider).
  Things still in the toy corner: flat r125i1 (-5.5,-0.43), cup r197 (-5.2,-0.55), duck r120i2 (-5.05,-1.19), tumbler r173 (-5.3,1.15),
  plush r174 (-5.56,1.07); the saber now lies at (-4.92,-1.405) by the basket.
- Mat (x 1.07..1.97, y -2.47..-1.87): croc (1.238,-2.024), sandal (1.356,-2.441, tilted on the console shelf), flat r125i2 (1.232,-2.259).
  Free for shoes r105 / flat r125i1: x 1.40..1.62, y -2.0..-2.3 (keep the hand off the lamp legs x 1.68..1.84, y -2.11..-2.26).
- Put stances of the library are often too far for floor spots: hand over the spot, squat_follow -0.30/0.6 then -0.38/0.8, lower, open.

## 20 Nov ~07:20-07:55 (twelfth home agent, session 2: run C:\Users\raresense\sim_home\runs\1120_072140_dex1_floor_9, cmd files live_cmd\f9\). AI-operated.
- Coordinator 07:15: scooter r126 deferred to Fable (after the kitchen); leave it exactly as at 0840. Kitchen/table items NOT ready.
- Chain 17: duck r120i2 in the basket (ckpt 0045_item_r120i2_duck). go_item's back-off step hit stick r154 on the coffee table; pick_floor
  tight, library basket put had no stance -> teleop: hand over the basket middle at 0.75, open.
- Chain 18: flat r125i1 on the mat (1.502,-2.072) (ckpt 0182_item_r125i1_flat): stance (1.77,-1.80) facing south, hand west, squat_follow
  -0.30/-0.38 (torso touches the static lamp object_0139 23 N), lower, open.
- Duck r120i1 (2.05,-1.70) is WEDGED between the static stroller r101 / static tote r102 and the open umbrella r106: no stance even tight;
  turning near it the knee hits the tote -> after the umbrella r106.
- cup r197 / tumbler r173 -> sink (kitchen, not ready); plush r174 has no route entry.
- Umbrella r106: its COLLIDER is one flat slab 1.04 x 0.86 x 0.033 m (corners (1.974,-1.603) (2.87,-1.413) (2.728,-0.74) (1.831,-0.929)),
  0.45 kg; grasp_plan None. Plan: corner pinch (ops.py corner_pinch_try, z 0.013) and drag (far side sliding) to its wall spot (-1.976,1.36).
- Umbrella r106 tries (NOT on the chain; reload 0182): before any walk from the mat stance step NORTH 0.12 and WEST 0.12 first (turning
  there hits the static lamp object_0139 with the hip, or the static tote r102 with the knee). Corner pinch at the SW corner, right hand,
  stance (1.67,-1.59, 57 deg): s 0.035 -> fingertips landed on the slab top (7 cm chord vs 7.9 cm opening); s 0.022, 14 N -> held 7 N but
  SLIPPED OUT on the lift at 3.4 cm (wedge: a 0.45 kg slab is squeezed out once off the floor); 20 N re-pinch -> closed on air.
  Ideas: (1) corner pinch + lift only 1.5-2 cm, then the OTHER hand fingers-forward (jaws above/below the 3.3 cm slab) onto the raised edge
  near the corner: a real two-face hold; (2) drag it by the corner pinch without lifting (floor friction keeps the wedge in) in short
  backward steps; (3) two hands as paddles pushing it. Its wall spot (-1.976,1.36) is ~4.5 m away; any free wall spot nearer would do.
- Easy items still open (no scooter / kitchen needed): cardboard box r175 (-5.26,1.38) -> its wall spot 18 cm north (-5.25,1.56), 32x29x25
  cm (push; the tumbler r173 lies just south of it); toy car r139 (-1.32,-2.37, on furniture 0.5 m) and ball r178 / pouch r179 (toy-corner
  shelf 0.76-0.9 m) -> basket (surface picks). Duck r120i1 waits for the umbrella r106.

## HAND-OVER 20 Nov ~08:05 (twelfth home agent stopping: working memory nearly used up). AI-operated.
- CHAIN END: C:\Users\raresense\sim_home\runs\1120_072140_dex1_floor_9\checkpoints\0182_item_r125i1_flat -> 18 of 63 done.
- Load: copy live_cmd\f9\a00_load.py with that CHAIN (it runs load_floor.py, bigcloth.py, zz_put.py, refresh_jointed_footprints());
  scooter.py (sc_take2 / sc_regrip / sc_pivot_step) and ops.py (corner_pinch_*) are loaded by load_floor.py's exec of the live files
  (ops.py, scooter.py) - re-exec ops.py if a session started before commit 3d25075.
- Scooter r126 is with Fable (ESCALATED); leave it as it stands.
- Isaac stopped and slot "home" freed at hand-over.

## 20 Nov ~07:52- (thirteenth home agent, Dex1 floor; AI-operated). Run C:\Users\raresense\sim_home\runs\1120_075248_dex1_floor_10, cmd files live_cmd\f10\
- Session: slot "home" port 47960 (newlive.py dex1_floor_10 apartment_1122_full.json at 12.2 GB available), guard on, loader f10\a00_load.py.
- Walk from the mat stance (after the north + west 0.12 steps) to the box stance (-4.87,1.08) facing north: ONE walk_tight, err 0.8 cm, no touch.
- Chain 19: cardboard box r175 against the wall (ckpt 0186_item_r175i1_cardboard_box). The box is a solid 8-vertex box, 0.6 kg; the wall is
  at y 1.735. No push skill in the library -> teleop with servo_pads: deep squat (-0.38/0.8), closed left jaws fingers down, push north
  in 3 cm hand steps at x -5.14. SEEN: pushing at pad height 0.11 TIPS the box (centre z 0.125 -> 0.151, lower edge -0.015) instead of
  sliding it -> push at pad height 0.05: slides flat. Arm reach ends ~0.43 m ahead of the squatting pelvis -> stand, step 6 cm, squat, push
  again. End (-5.257,1.537) upright (spot (-5.25,1.56)), 2 cm off the wall. Tumbler r173 / plush r174 unmoved.
- Skill: ops.py push_floor(nm, u, along, goal, side) (commit 373de08) = the box push made reusable (NOT yet run as a function).
- TOY CAR r139 SKIPPED (not tried physically): it lies on the round side table's SE part (-1.32,-2.37, 0.50 m) against the south
  wall; the static wooden walker toy (x ~-0.85, y ~-2.4) and the hamper (west) leave no stance: nearest free pelvis (rb0 0.20)
  (-0.9,-2.1) is 0.50 m from it (fingers-down reach 0.33). tidy_surface: "no place to stand" even tight. Needs the table or the
  walker moved (scene change) or a reach tool.
- Chain 20: ball r178 (window sill r2i1, 0.76 m) in toy basket r186 (ckpt 0408_item_r178i1_ball). SEEN:
  (1) tidy_surface (tight) stance (-5.80,-2.13) facing west, ball 0.33 ahead: servo_pads keeps a FIXED 1.3 cm overshoot (pads past
  the ball, fingertips touching the sill top) -> "NOT closing" twice. Fix: servo to the target minus the measured overshoot along
  the heading (3 passes -> 1.6 mm), z 0.765 aim -> close 12 N, 6 N per jaw, rose 5.9 cm.
  (2) FALL after the 2nd "NOT closing": the retreat (hand up 8 cm + rest_hands) -> knees snapped 0.81 -> 0.1 rad in 0.2 s at
  t 7043.0 and the robot fell backward onto the floor (replay from 0250_act_stand_up falls the same). Avoided by not taking that path.
  (3) put_away "no place to stand" (basket boxed in: static megabloks bag r185 south, ottoman r166 west, saber r130 lies along the
  NE side from (-4.73,-1.51) to (-5.31,-1.04)). CARRY_JOINTS=True while the hand is still over the sill lowers the hand onto it
  (finger 88 N, grip lost) -> step back 2 x 0.12 m first, THEN walk_tight carrying to (-4.85,-1.05, -125 deg) (north of the saber;
  path east round by (-4.65,-2.1) (-4.4,-1.45)); thand over (-5.11,-1.37), squat_follow -0.20/-0.30 reached only x -5.03
  (3.7 cm short) -> squat_follow -0.38/0.8 reached it at 0.22 m; open: ball in. Use this stance for the other basket puts.
- FALL #2 (walk from the basket to the sill, t 7445, run ..._10): ROOT CAUSE FOUND: after my teleop servo_pads / thand moves I
  "rested" the arm with arms_to("rest") which does NOT release the ee pose command: ts.ee["left"] stayed mode 'pose' at the basket
  drop point (ctrl._reach ee_left). At walking height (H_WALK) the controller kept reaching for it: pelvis pitched 0.33 rad (waist
  pitch 0.33, normal 0.005), knees 1.3/1.5, the final turn at the sill never converged, tilt grew and it fell. The item checkpoints
  0186 (box) and 0408 (ball) CARRY that stale command. FIX: rest_hands(SIDES) (op.send ee release) after every teleop and right
  after loading 0186/0408 (verified: tilt 0.005 at H_WALK). ops.push_floor fixed too. RULE: end every teleop with rest_hands().
- Fresh session after the falls: run C:\Users\raresense\sim_home\runs\1120_084921_dex1_floor_11 (slot home, 47960), loader
  live_cmd\f10\a01_load11.py (CHAIN = ..._10\checkpoints\0408_item_r178i1_ball) + rest_hands(SIDES).
- ESCALATED (20 Nov ~09:20): TOY POUCH r179 (sill r2i1, 0.15 kg; convex collider 17 x 11 x 17 cm: no section under the 7.9 cm
  jaw opening, grasp_plan None). Chain end unchanged: ...\1120_075248_dex1_floor_10\checkpoints\0408_item_r178i1_ball (pouch on
  the sill there). Tried (run ..._11, cmd files f10\e02..e19): stance (-5.87,-2.20) facing west (the (0, 0.3) posture moves the
  pelvis back ~10 cm), both jaws CLOSED fingers down as paddles at x -6.18 on the N and S faces, squeeze in 5 mm steps (contact
  force from br.mjm/br.mjd: 6.9 / 5.1 N), lift in 2 cm steps: it ROSE 4.6 cm with the hands (2.4-3.5 N per hand) = a real
  friction hold. SEEN: (a) pulling both hands 1-3.5 cm toward the body drops it back on the sill (squeeze drops to 0-0.4 N; the
  two point contacts let it pivot about their line); (b) re-squeezing after every 1 cm pull still dropped it at the first pull;
  (c) a 6 cm body step back (tmove carry=both) dropped it to the floor at once. Ideas: a real two-hand hold needs the weld
  (hold_on share 0.5) after a contact-verified squeeze - a rule question for the user/Fable; or contacts above the centre of
  mass and centred on it (pads were 3-4 cm toward the robot from its centre), slower whole-body moves; or a reach tool.
- Chain 21: TOY POUCH r179 in toy basket r186 (ckpt C:\Users\raresense\sim_home\runs\1120_084921_dex1_floor_11\checkpoints\0373_item_r179i1_toy_pouch)
  - coordinator OK'd the contact-verified two-hand hold (supersedes the ESCALATED note above). Cmd files f10\g01..g14.
  Pick (g01): stance (-5.87,-2.20, 180 deg), posture (0, 0.3), closed jaws fingers down (R_down [0,1]) at the pouch's middle x,
  3 cm outside the N/S faces, pad z 0.80; op.squeeze("right","left", left->right unit, 10 N, friction 1.2); TWO on; lift
  op.carry((0,0,0.03), 0.05/0.03, mass): rose 5.4 cm, only the hands touch it (_thing_contacts) -> hold_on share 0.5 each.
  NOTE island_skills.two_hand_check reads FINGER links only and reads 0 here (the jaw BASES press, 12 N measured from
  br.mjm/br.mjd contacts) -> checked by contact force instead; the monitor's held/pressing checks need MON["held"] = {},
  MON["ignore"] = {pouch id}, MON["ignore_names"] = (pouch,) for a two-hand base hold.
  Carry: walk_path legs (two_hand_walk, tight) put the right knee on the coffee table r145 corner (-4.23,-1.23) twice ->
  tmove steps (carry=SIDES) through x -4.52 (between the table and the saber), then to (-4.85,-1.05, -125 deg).
  Set-down: island two_hand_set_down stopped at once ("weak": finger-link check) -> own loop with _two_track: squat stages
  alone drifted 8 cm short (reach); squat + LEAN stages (-0.05/0.3, -0.12/0.5, -0.20/0.6, -0.28/0.7, -0.34/0.8, -0.40/0.85)
  kept it within 2 mm of (-5.10,-1.36); arms dz -0.15 to bottom 0.21; two_hand_open; stand with the hands rising; 2 x 0.15
  back; hand_down; rest_hands. A tmove forward from that stance puts the left foot on the saber (aborted, reloaded).

## HAND-OVER 20 Nov ~10:10 (thirteenth home agent, Dex1 floor; working memory low). AI-operated. READ THIS FIRST.
- CHAIN END: C:\Users\raresense\sim_home\runs\1120_084921_dex1_floor_11\checkpoints\0373_item_r179i1_toy_pouch -> 21 of 63 done
  (this agent: cardboard box r175, ball r178, toy pouch r179). Route head after it: r106 umbrella, r139 toy car, shoes r105...
- Load: copy live_cmd\f10\a01_load11.py with that CHAIN, then rest_hands(SIDES) (the 0186/0408 item checkpoints carry a stale
  ee pose command; 0373 does not, but call it anyway). Exec E:\urc_fable3\scripts\home\island_skills.py for two-hand holds.
- RULE learned: end every teleop with rest_hands() (arms_to("rest") keeps the ee command -> pelvis pitch 0.33 at walk height -> fall).
- Skipped: toy car r139 (no stance: table + static walker + hamper; see above). Scooter r126 with Fable.
- Next: umbrella r106 (slab 1.04 x 0.86 x 0.033 m, 0.45 kg, centre (2.371,-1.183), corners (1.966,-1.623) (2.865,-1.448)
  (2.734,-0.772) (1.835,-0.947)). Idea not tried yet: PUSH it (corner pinch / closed jaws pushing INTO the corner jams the wedge,
  pulling opens it) with ops.push_floor at pad z ~0.02; any free wall spot nearer than (-1.976,1.36) is fine. Free floor map
  round it (tight grid, umbrella ignored) printed in f10\f00_umb.py. Then duck r120i1, the east hall (shoes r105 to the mat x
  1.40-1.62 y -2.0..-2.3, umbrella r107 at (0.95,-0.54) now, tote r102).
- Code: E:\urc_home home-cleaning 373de08 (ops.push_floor), 8c8119c (rest_hands fix). Isaac stopped, slot "home" freed.

## FABLE SCOOTER (20 Nov ~08:25-11:50, Fable escalation agent; AI-operated). Scooter r126 parked by the sofa's east arm: OK, ONE CALL verified.
- RESULT: OK. Scooter r126 stands upright, north-south, beside the sofa's east arm, bar at the south end, deck pointing north:
  box x -2.37..-2.04, y -0.31..0.31, bar (-2.202,-0.185), tilt 1.2 deg (front wheels on the 1 cm rug edge), only its three
  wheels touch anything (wheels 5 cm off the arm; the bar's west end is above the arm, 0.97 m up, arm top 0.63). Nothing else
  moved. No hold spring anywhere: the lower jaw pads carry it (15-18 N a hand), the weight is only TOLD to the controller.
  The pocket west of its old place (x -2.8..-1.9, y -0.68..-1.22) is free floor on the tight grid now.
- THE CALL for the floor agent (verified end to end as ONE call from the robot at (-2.0,1.0) with the untouched scooter:
  status done, 16 carry moves, 341 s sim, 853 s wall):
      exec(open(r"E:\urc_fable4\scripts\home\live\scooter_hang.py", encoding="utf-8").read())
      zz_r = park_scooter_hang("r126i1_scooter")          # -> dict(status="done", box, tilt_deg, moves, set_down, release, look)
      item_done_auto("r126i1_scooter", zz_r, spot=(-2.20, 0.0))    # records it on the chain (OVR dest "floor"; room file untouched)
  PRECONDITIONS: (1) usual load (load_floor.py ..., gait_on(), settle_after_load(), refresh_jointed_footprints(), rest_hands(SIDES));
  (2) scooter r126 untouched since 0840: box x -2.43..-1.78, y -0.99..-0.58, bar (-2.284,-0.811), deck 8.5 deg (the stance is
  computed from where it stands, but the way points / headings / goal in SH_PARK are for this pose); (3) the robot stands
  empty-handed with a straight free way to (-1.30, 0.20): verified from (-2.0, 1.0) facing south, e.g. after
  walk_tight((-2.0, 1.0, -1.47)); (4) nothing loose on the floor in x -2.4..-1.2, y -1.1..0.9 (saber, knit hat gone: true on
  the chain). On status FAILED the call tries to stand the scooter down where the robot is (set_down_after_stop); read
  zz_r["why"], reload the checkpoint before, run again or drive the sh_* steps by hand (the fs*.py files below are those steps).
  Code: worktree E:\urc_fable4, branch scooter-fable, commit 069461f (one new file, off home-cleaning 373de08; merge it or
  exec it from there). No push.
- Run (side branch, NOT on the chain): C:\Users\raresense\sim_home\runs\1120_0826_scooter_fable_AI_operated
  (from_ckpt.json: C:\Users\raresense\sim_home\runs\1120_075248_dex1_floor_10\checkpoints\0186_item_r175i1_cardboard_box;
  fable_scooter_result.json = the verified call's record). Slot "cloth", port 47970; Isaac stopped, slot freed.
  End checkpoint of the verified call: ...\1120_0826_scooter_fable_AI_operated\checkpoints\1132_act_fs_VERIFIED_call_scooter_r126_parked
  (robot at (-1.602,0.38) facing south, hands at rest, free cell). End frames looked at: ...\look\v02_verified_end_from_east.jpg,
  ...\look\v01_verified_end_from_above.jpg, ...\tele\0114_end_r126i1_scooter_done.jpg. Live drive before it (same place, bar
  (-2.169,-0.223)): ...\checkpoints\0638_act_fs_END_scooter_r126_parked_by_sofa_arm, ...\look\z02_end_from_east.jpg, z03_end_from_south.jpg.
  Command files: C:\Users\raresense\sim_home\_fable_scooter\ (fs.sh, fs00_setup .. fs95_verify, fs99_close).
- THE METHOD (why it works): the scooter is carried HANGING from its handlebar. With a wheel on the floor every turn drags that
  wheel sideways under load (10 N at the floor, 1 m below a bar held by two jaws 0.2 m apart = 10 N m of roll on the grip, +-45 N
  on jaws that squeeze 20 N): that twisted the bar out for the floor agent. Lifted fully there is no floor force: the round bar
  turns freely in the jaws and the scooter hangs like a pendulum, tilted 22 deg (centre of mass 0.19 m off the bar, 0.48 m
  under it), rear wheel 6 cm to the deck side of the bar, front wheels 0.38 m to the other side and 0.25 m up. So the robot
  stands on the DECK side (from the old stance the front wheels swing into the shins) and BESIDE the deck: bar 0.26 m ahead and
  0.235 m to the right of the pelvis, facing the bar (sh_stance). Right hand on the outer part of the bar fingers forward, left
  hand across the body on the inner part, fingers 45 deg to the right; jaws closing vertically (sh_grip). Lift 11.5 cm straight
  up in 3 cm stages (sh_lift: the rear wheel is dragged in under the bar, then it hangs 2 cm off the floor). Turns on the spot
  (15 deg) and backward steps (0.15 m) by sh_move = tmove + sh_trim + sh_recentre. Set-down = sh_set_down_walk (below), sh_release.
- SEEN per failure (each resumed from the checkpoint before it, never from zero):
  1. Walk to the stance: walk_to_stance planned straight ACROSS the scooter's rear wheel (it leaves a big thing out when the
     stance lies inside its clearance): right foot on the wheel, 26 N (tele 0005). Fix: way points round its east end
     (walk_via (-1.30,0.20) -> (-1.30,-0.93) -> pre point 0.40 m behind the stance), then walk(stance): 0 cm error.
  2. Attempt 1 (6 carry moves fine): the fingers were 10 / 22 deg tips-UP (the hands' orientation task is soft: session.py
     rot_weight 2 against 20 for the place; and my lift re-commanded the hands' PRESENT orientation, freezing the sag in).
     Tips-up, the round bar crept along the 2.9 cm pads toward the palm at every step (0.6 -> 2.1 cm; nothing behind the pads)
     and dropped out of the right jaws when the hand was turned (tele 0027: right gripper above the bar, closed on air).
     Fix: rot_weight 10 while the scooter is held, hands always commanded LEVEL (sh_level_Q), the bar's seat on the pads read
     after every move (sh_seat) and trimmed (sh_trim), the bar gripped a few mm toward the finger tips to begin with.
  3. Attempt 2 (carried 1.0 m, seats held): SET-DOWN. Lowering the bar straight down JAMS: the rear wheel lands 6 cm from the
     bar's line and would have to slide outward against friction 0.8 with the bar 1 m above it (hands stalled 3.7 cm above
     their target, wrists bent 22 deg, tele 0041). A trim with the wrong sign for one move had also left the left seat at
     -10 mm; in the first walking set-down the left jaws lost the bar and the scooter fell onto the hamper (tele 0043).
     Fix: the bar is walked AWAY from the planted wheel: the robot walks FORWARD in 0.12 m legs while the hands come down along
     the arc round the wheel (sh_set_down_walk); the wheel trails behind the bar like a towed thing.
  4. Attempt 3 (grip, lift, 13 moves to (-1.863,0.546), all good): the first arc follower was feedback only: it trailed the arc
     by 4 mm, the wheel came off its load and was dragged along (8 legs, 0.9 m of walking for 0.35 m of tilt-travel), the right
     jaws lost the bar and the scooter ended upright 0.6 m south of the goal. Fix (resumed before the set-down): feed-forward of
     the arc's slope times the walking speed, bar asked 4 mm under the arc, gain 6 /s: three legs took the tilt 22.5 -> 15.2 ->
     9.0 -> 3.8 deg; the last centimetres standing, hands 2 cm forward-and-down a step (sh_finish_standing). The end test must
     be FLOOR CONTACTS (rear wheel + a front wheel, sh_on_floor), not heights: the front wheels landed on the 1 cm rug edge at
     "z 0.070" while my loop waited for 0.062 and pushed on until the right jaws slid off (twice; resumed, fixed). -> parked.
  5. First run of the whole call: FAILED at move 12: the bar had crept 7.5 mm toward the LEFT hand's finger tips (walking
     backward, ~0.7 mm a move; that hand cannot be pitched tips-up enough to trim it), the call set down early, there the wheel
     stood on the RUG (1 cm): the arc was 1 cm too low, the hands pressed, fingers 30 deg up, seats +15.6 / -10 mm -> stop.
     Fix: left hand gripped 4 mm (right 8 mm) toward the tips, early stop only over 9.5 mm, the floor height under the wheel
     measured when it touches (wheel centre minus radius) and added to the arc. Second run of the whole call: done, seats
     within 3.8 mm over 16 moves, set-down 4 legs + 2 standing steps.
  6. A re-grip where the scooter stood after (4) failed twice: the right hand lands 0.37-0.40 m right of the pelvis whatever
     it is asked (arm geometry), so the stance must be within ~1.5 cm of sh_stance; a 4 cm tmove correction overshot (walk(stance)
     gives 0 cm). Not needed in the call.
- DESTINATION: the room file still says "vehicle corner (hall wall, beside the toy bike)", spot (0.29,-2.515) (user's 02:00
  order: upright at a wall). It is parked at the floor agents' nearer place by the sofa's east arm (as this task asked); the
  room file is NOT changed (item_done_auto writes the spot into the run's overrides only). If the wall is wanted: the same
  carry reaches about 1.7-2 m a grip; the vehicle corner (3.8 m, facing the wall at the end) needs other way points in SH_PARK
  and a set-down that walks 0.4 m forward TOWARD the wall (stance north of the spot, facing south) - not tried. Coordinator's call.
- Facts worth keeping: the Dex1 jaws are pads only (2.9 x 2.9 cm), no collision shape between the pads and the gripper base
  5 cm behind: a bar that leaves the pads falls. Contacts creep under a steady side load (finger pitch 10-20 deg = mm a move).
  The rug by the sofa is 1 cm thick. Reaching with both arms the pelvis leans back 0.25-0.3 rad and sinks 8 cm (the arms weigh):
  fine standing, tmove resets the posture. This scooter tips sideways at 4 deg (front wheels 0.14 m apart, centre of mass
  0.49 m up): never let it drop, even 3 cm. ZZ_CK is a global of load_floor.py (do not reuse the name). close() from z 4.2 is
  above the ceiling (grey frame). My run folder holds 814 checkpoints (1.8 GB, C:): all but 0053, 0086, 0638 and 1132 may go.

## 20 Nov ~09:38- (fourteenth home agent, Dex1 floor; AI-operated). Run C:\Users\raresense\sim_home\runs\1120_093820_dex1_floor_12, cmd files live_cmd\f12\
- Session: slot "home" 47960, guard on, loader f12\a00_load.py (chain end 0373 + rest_hands).
- UMBRELLA r106 push tests (side tests, NOT on the chain; the chain was reloaded from 0373 afterwards):
  * Its collider is an 8-vertex BOX 0.916 x 0.688 x 0.03 m, yaw -10 deg (flat_corners' "1.04 x 0.86" was the visual).
  * The only free stance next to it is EAST (x 3.0-3.3, y -0.97..-1.4), reached by walk_path via the kitchen aisle north of
    the island (one walk from the toy corner, err 4 mm). The 0.4 m strip north of it (cabinet r35 at y -0.37) is too narrow.
  * Paddle push (closed jaws fingers down at the edge) FAILS: the Dex1 jaw tips are a pencil point (close-ups f12_d01/d02),
    and the arm is soft: servo_pads 3 cm steps stall under the ~3 N of floor friction (the hand stays 2.5 cm short, rises).
  * Corner pinch 2 cm in (s 0.020) at the SE corner works: in br.mjd both fingers on the SIDE faces (normals horizontal,
    ~5 N each). s 0.03 put the fingertips on the slab's top (the finger is 2 cm wide along the bisector: 2(s+0.01) < 7.9 cm).
    NOTE: contacts must be read from br.mjm/br.mjd (m/d have no contacts here); body names there carry a long prefix.
  * Pushing INTO the corner with the arm target LEADING the hand by 6 cm (op.move to ee + 0.06 along the bisector) moves the
    slab 2-3 cm a step with the pinch held. A squat stroke is only 0.10-0.14 m (the squat moves the pelvis back 8 cm, the
    hand reach ends 0.37-0.40 m ahead): 2.5-3.5 min wall per stroke -> too slow for metres.
  * The slab cannot pass under the stool r99 (legs y -1.02) while duck r120i1 (y -1.65) is there: gap 0.63 < 0.69 m.
  * The entry corner is NOT a spot: the front door r11 is in the south wall at x 3.28-4.18.
  * Plan agreed with the coordinator: two-hand corner pinch on the short east edge (both corners, contact-checked per hand),
    hold_on 0.5 each, carry level at pad z 0.62 (clears stool 0.55, tote 0.38; stroller uprights at x 2.25/2.75 y<-1.73 are
    tall: board south edge must stay > -1.70), walk 0.10 m/s, set down flat at about (-1.78, 1.33) by the living-room north wall.
- Chain 22: SCOOTER r126 (ckpt C:\Users\raresense\sim_home\runs\1120_093820_dex1_floor_12\checkpoints\0894_item_r126i1_scooter).
  Fable's park_scooter_hang from 0373 (walk_tight((-2.0,1.0,-1.47)) first, checks passed) FAILED TWICE in its LAST set-down
  leg (6th, tilt ~5 deg): run 1 lost the right jaw (t 8248.5-8249.5: right hand jumped z 1.008 -> 1.136), run 2 (from the
  call-start ckpt 0432 + a 5.5 s settle) lost the left. At ckpt 0864 (before that leg): right seat -13..-15 mm (pad edge
  14.5) with the fingers pitched 32-41 deg, left -6 mm / 13 deg. From 0864: a 1 cm arc step pushed the right seat past the
  edge; sh_trim's 8 deg re-pitch then knocked the scooter over (reload). Fix (from 0864): the right squeeze eased to 6 N
  to re-seat; the bar left both jaws and the scooter came down the last ~2 cm onto its front wheel: STANDS, tilt 1.2 deg,
  3 pieces on the floor, box x -2.369..-2.009, y -0.438..0.188 (12 cm south of Fable's end). Hands off by moves up/back,
  rest_hands, 2 steps back, 2 side steps. For scooter_hang.py: end the set-down legs at tilt < 6 deg or a seat > 12 mm
  and finish by easing the squeeze (not another leg / not sh_trim). Cmd files f12\s0*.py, t0*.py.
- SCENE REDUCED TO 40 ITEMS (user decision 11:30): ckpt ...\1120_093820_dex1_floor_12\checkpoints\0895_item_scene_removed_40
  (meta info.removed = the 22 names of REMOVED_FOR_40.json). ops.remove_bodies (ad717c8): off-map on the ground plane x 25-32.5,
  y 25-29.5, resting, qvel 0, written to br.mjd + br.sync(); dropped from ROUTE. No other body moved > 5 mm.
  look\f12_removed40_room_head.jpg. progress_pct counts "scene_removed_40" as an item (real: 22 of 40).
- Chain 23: POUCH r149 in the rubbish bin (ckpt ...\1120_093820_dex1_floor_12\checkpoints\1071_item_r149i1_pouch). Collider 9.5 x 15 x 3.1 cm,
  50 g, on the coffee table. go_item: "no place to stand" (floor pick) -> surface item: tidy_surface missed twice (grasp_plan
  takes a CORNER, the pouch pivots: rose 0.024 < 0.04). A pinch WITHOUT hold slipped at 2.5 cm lift. Fix (f12\i06): corner
  pinch 1.8 cm in at the corner NEAREST the robot (grasp_plan's options were all 0.47 m ahead, out of reach), surface_posture
  (-0.12, 0.45), contact check in br.mjd (both fingers on side faces), hold_on, lift 19 cm. put_away walked it to the bin and
  stopped on the left knee at the bin (31 N) with the pouch already over the opening -> jaws opened, in.
  FALL after: the back-off tmove's ready_to_walk lowered the pelvis 9.5 cm with the knee on the bin; the bin pushed it back
  (knees 0.53 -> 1.3), the backward step fell. GOTCHA: 1071 was saved 0.02 s after that lowering began -> after loading
  1071 send posture(height 0) at once, then tmove(fwd=-0.10, carry=("left",)) x2 (tall height): done, robot at (-0.22, 0.96).
- WRAPPER r87 (island top 0.93, 15 cm in from the south edge) NOT done (3 tries): tidy_surface tight -> right knee on stool r99
  (60 N); walk to (1.83,-0.60) -> foot on scissors r108 (21 N); from the counter face it is 0.415 ahead (chest reach ~0.33),
  lean 0.35 -> FELL backward. Reloaded act ckpt 1077 (clean, robot at (-0.22,0.96)). Idea: level hand (as the nugget) from
  the island's EAST or WEST end, or the right hand from x ~1.95 (no stool).
- Chain 24: NUGGET r93 in toy basket (ckpt ...\checkpoints\1370_item_r93i1_nugget). Library top-down surface pick at the island
  edge: pads 6 cm short (4 approaches). TELEOP (f12\k02): LEVEL hand, fingers forward, jaws closing sideways (R = [fwd, lat,
  up]) at the nugget's middle height from behind it (12 cm) then in: grip 3 N/jaw, both fingers in contact -> hold_on, lift
  5 cm, pull back. Basket put helper f12\basket_put.py (basket_put / toy_trip): walk_tight to (-4.85,-1.05,-125 deg)
  carrying, squat_follow -0.20/0.35, -0.30/0.6 (+ -0.38/0.8 if the hand is > 4 cm off), CHECK the hand over the basket
  before opening (my first drop opened 31 cm short: fell beside it), the released thing added to MON ignore (else
  "neighbour knocked" stops the stand-up).

## SCOUT (hall) (20 Nov ~11:45-, scout agent, side branch, AI-operated). Run C:\Users\raresense\sim_home\runs\1120_114552_scout_hall_AI_operated
- Slot "cloth" 47970 (E:\urc_scout\scripts\home\c_live.py, URC_TEXTURED=1), worktree E:\urc_scout branch scout-hall (off
  home-cleaning ad717c8). Cmd files C:\Users\raresense\sim_home\apartment\live_cmd\sc\ (sc.sh runner, a00_setup, ld.py loader).
  Start: 1071_item_r149i1_pouch + posture(0) at once + 2 x tmove(-0.10, carry left): robot (-0.22,0.96), fine.
- GOTCHA (render only): after loading a checkpoint the garments are DRAWN where they lay at the session start (blanket, coat
  pile, jacket on the floor/mat in every picture) until they move: call sync_cloth(force=True) after every load.
- Mat r119 free room (collider hulls): lamp object_0139 is a TRIPOD standing on the mat, feet (1.76,-2.01) (1.587,-2.31)
  (1.933,-2.31), apex (1.76,-2.21) 1.3 m up. Static tote r102 x 1.985-2.152, y -2.072..-1.732. Shoes r105 are 25 x 8.5 cm.
- DUCK r120i1 -> toy basket r186 (code E:\urc_scout\scripts\home\live\hall.py duck_to_basket). SEEN, each from the checkpoint before:
  1. library pick_floor: its section closes along (-0.34,0.94) at the head; the duck lies AGAINST the static tote r102's north
     face (y -1.732), so the south jaw goes into the tote: 2 approaches "pads not at the point" + monitor stop "left finger
     pressing furniture 75 N at z 0.07". (A first live try got it on approach 3, 459 s: luck.)
  2. head across x from the library's stance (1.758,-1.729) facing 65 deg: right knee into the tote 113 N.
  Fix: pick_at(): FIXED stance (1.805,-1.46) facing south, head (hull top 3 cm: 4.8 x 4.2 cm) closed across x by the left
     hand: pads 2 mm off, 5.2/4.5 N, both jaws on it, rose 7.7 cm.
  3. basket drop at squat -0.30: hand 7.8 cm short of the middle, the duck slid onto the east rim. At -0.38/0.8 it is 2.5 cm
     from the middle, released 2.5 cm above the contents: inside (bottom).
  4. rest_hands() still in the deep squat swung the open hand down onto the light saber by the basket (31 N, monitor stop).
     Fix release_and_stand(): hand up, stand with the hand following the pelvis (squat_follow), THEN rest_hands.
  Verified as one call (v4, before the coordinator's grasp guard): status done, 653 s wall, 259 s sim, end ckpt
  ...\1120_114552_scout_hall_AI_operated\checkpoints\0531_item_r120i1_duck, end frame tele\0013_end_r120i1_duck_done.jpg.
- GOTCHA: an item end (item_done_auto -> ck_prune_item) DELETES this item's act/roll checkpoints, incl. the one a verification
  started from. Keep starts as kind "start": ...\checkpoints\0537_start_scout_start (= 1071 + its gotcha, robot (-0.22,0.96)).
- Chain 25-28 (toy_trip = library pick_floor + basket_put, f12\basket_put.py; ~8-13 min each): toy r193i4 (1470), ball r192
  (1577), toy r193i2 (1676), toy r193i1 (1874). r193i1: the LEFT hand at the right-hand basket stance stopped 0.30 m short;
  a re-step left the toy on the floor at the basket corner with the fingers off (monitor stop) -> released, re-picked with
  the RIGHT hand (toy_trip side="right" now), in.
- GRASP QC (coordinator 20 Nov, user's video QC: plastic bag r196 welded after a jaw tip flipped it): skills.hold_on
  refuses (HOLD_REFUSED, EVENTS) unless BOTH jaw fingers of that hand touch THIS item (br.mjd) and the item rose < 5 mm /
  turned < 10 deg DURING the close (close_jaws records CLOSE_REF before/after); hold_on(..., guard=False) only for the
  two-hand jaw-base squeeze (island_skills.two_hand_pick: wrap it at the sponges r83 step). corner_pinch_try pads at low z
  + 0.4 x thickness. Commit 8fa8cc5. Live sessions started before it: exec f12\qc_patch.py.
- Chain 29: toy r193i3 (ckpt ...\checkpoints\1978_item_r193i3_toy_piece).
- TOY VEHICLE r191 NOT done (2 tries): AABB 18.6 x 16.6 x 8.4 cm, library grip gap 6.95 cm (nearly the 7.9 cm opening).
  Try 1: released from pads 0.30 m over the basket -> ended on the floor 0.38 m north of it. Try 2 (BASKET_Z 0.21): the fingers
  lost contact in the carry walk (monitor "held thing lost") -> set down by hand where it was (no spring-only carry). Lies at
  (-5.17,-1.25), against the basket's north edge.
- Chain 30: DUCK r120i1 by the scout's call (E:\urc_scout hall.py duck_to_basket, e8b8038): ckpt ...\checkpoints\2244_item_r120i1_duck.
- STICK r154 NOT done (2 tries): 3 x 60 x 1 cm flat on the coffee table (z 0.475-0.485). tidy_surface closed on the table
  (gap 7 cm, rose 0), then a fingertip on the table 61 N. Tilted 40 deg pinch (f12\n03): pads stall at z 0.509; one finger
  on it -> the grasp-QC guard REFUSED the hold (works); stick pushed 5 cm. Needs slide-to-edge / edge pinch.
- Coordinator's grasp rule is in hall.pick_at (both jaws on THIS item by contacts, rise < 5 mm, tilt < 10 deg during the
  close, else reopen and retry x3; close-up at hold_on into <run>\grasps\hold_<item>_t<time>.jpg). grip_check needs at=gp["at"]
  for things taken at an end (shoe: centre 10 cm off the jaw axis -> "ok False" with both jaws loaded).
- SHOES r105 -> mat (hall.shoe_to_mat(name)). Spots: r105i1 (1.855,-2.00), r105i2 (1.645,-2.00), both N-S, both LEFT hand,
  r105i1 FIRST. SEEN (each from the checkpoint before): (1) put stance 0.11 m beside the spot: the torso leaning in the squat
  reached 0.44 m ahead and hit the lamp's north leg at z 0.72 (64 N). (2) after carry_pose the shoe hung 13.5 deg from one
  contact per jaw at its heel end; the put's first servo (0.56 m below the hand at squat -0.20) twisted it out (lost).
  (3) squatting first left the hand BETWEEN the knees: it could not move sideways (err 4-6 cm per step). (4) following the
  pelvis down, the hanging shoe touched the mat and was dragged (tilt 32, yaw 24). (5) stance 0.30 beside the grip: the knee
  pushed the hand out to 0.43 lateral, 5 cm off. Fixes: no carry_pose, over the spot STANDING, squat with the shoe kept >= 6 cm
  up and re-centred after each stage, lower, release, stand with the hand following; stance 0.40 beside the grip point.
  Live: r105i1 final (1.902,-1.995) yaw 9 tilt 0.9 (spot then 1.875, moved to 1.855); r105i2 (1.639,-1.995) yaw 1 tilt 0.7.
- Chain 31: TISSUE r158 in the bin (ckpt ...\checkpoints\2493_item_r158i1_tissue). On the sofa seat front (z 0.45), 8x8x7 cm, 5 g.
  tidy_surface: stopped by "neighbour knocked" towel r100 (slid 8.7 cm BY ITSELF, robot 1.08 m away: CREEPERS.add(towel));
  retry: fingertip on the seat 68 N. Teleop (f12\cpick.py corner_pick): 6 cm closer, corner pinch 1.8 cm in at the nearest
  corner, pad z max(middle, seat + 1.9 cm), guard passed, hold_on, lift 10 cm; bin_drop (put_away + let go over the opening
  + back off TALL: posture 0 first, tmove carry=("left",)).
- STICK r154 parked after Fable's slide_out + edge_pick one try (f12\n11, inset 1.5 cm): it already overhangs the coffee
  table's west edge (table x -4.23..-3.13) by 6 mm; slide_out's MEASURED press stayed 0 N (command up to 30 N): pads never
  pressed it; MON 240 s item limit. Stick at (-4.20,-0.95).
- TOY VEHICLE r191 parked: 3rd try (squat drop) -> pick_floor "no place to stand" even tight at the basket's north edge
  (-5.17,-1.25) (basket, saber r130, ottoman). It is no longer by the TV door.
- Stool r99 is STATIC (cannot be removed by remove_bodies); scissors r108 is loose.
- SHOES VERIFIED (one call each, from ...\checkpoints\0642_item_r120i1_duck): shoe_to_mat("r105i1_shoe") done 694 s wall
  (ckpt 1419_item_r105i1_shoe), shoe_to_mat("r105i2_shoe") done 537 s (ckpt 1517_item_r105i2_shoe); finals (1.852,-1.994)
  and (1.643,-1.990), yaw <= 1.2 deg, tilt <= 0.9. First verify failed: at the carry start a foot stepped on the other shoe
  (45 N) -> 0.25 m straight back first. Duck call also ran on the floor chain: done, 790 s (floor ckpt 2244_item_r120i1_duck).
- Merged home-cleaning 5b7002f (act meta.json kept, actions.jsonl) + 8fa8cc5 (hold_on guard) into scout-hall; the
  checkpoint part applied live in my session (live_cmd\sc\c01_cklive.py).
- PREVIEW STILLS for the coordinator: C:\Users\raresense\sim_home\apartment\final_look_preview\ (room/head RT 1080p 93-131
  ms/frame, PT 64 spp, close-ups, times.json). Untextured: the added rubbish bin (flat black), toy basket r186 (plain grey),
  hamper r133 (plain white), shoes on the mat render near black (no light in the hall), a wire square round the beige
  container by the basket. Normal session render mode: RealTimePathTracing, aa op 3 (restored after the stills).
- UMBRELLA r107 (hall.umbrella_to_entry): its collider lies south of the island's west end (island y > -0.37, NOT under it;
  a close-up from above looks like it is under the counter). Library: left stance only (by the island corner), right none.
  Custom: right hand, robot facing along the shaft, pelvis (0.622,-0.415) heading 0.52: pick clean (5/5 N, both jaws).
  Put by the entry N-S at (3.10,-2.45), 0.33 m east of the stroller (x <= 2.77), robot facing south, right hand. SEEN: the
  shaft hangs 40-43 deg in the jaws (pivots on the grip) and its tip lands first (off 3.9 cm, rejected at 3 cm) -> item
  tolerance 6 cm / 20 deg; lying test = hull top < 0.09 (its body frame rests rolled 33 deg on the hook, box tilt is no test).
- 15:00 MEMORY SQUEEZE: after the preview stills my kit was ~17 GB private (5 extra 1080p render products made and
  destroyed leaked ~1.6 GB); the umbrella verification died with "Unable to allocate 1.48 MiB" (commit exhausted). My
  session stopped (slot freed); the floor Isaac also restarted at 15:01. RULE: no extra render products in robot sessions.
- New coordinator guard (commit free < 6 GB or kit private > 12 GB) tripped on a plain scene load (12.6 GB while loading;
  the floor kit runs at 13.9 GB; commit 54 GB total, 20 GB free with one session). Asked the coordinator for thresholds;
  guard script C:\Users\raresense\sim_home\apartment\live_cmd\sc\guard2.py. Session-2 run folder (empty, stopped while
  loading): see live_cmd\sc\RUN2.txt.
- TV DOOR r159 (run ..._12, f12\p01): kitchen_skills.close_door_follow under call_mon from the chain (r191 no longer at the door):
  shut 0 -> -0.918 rad (53 of 90 deg) in 741 s sim, then the call died on a numpy allocation error: SYSTEM COMMIT CHARGE
  EXHAUSTED (free virtual 0.05 GB; my kit 14.6 GB private + the scout's 16.9 GB after renders). Both sessions died.
  A FRESH session of this scene has ~14 GB private (working set ~6.5 GB). Guard now: f12\mem_guard.ps1 (stop at commit free
  < 3.5 GB, kit private > 16 GB, C: free < 2 GB); restart at the next item checkpoint when private passes 15 GB.
- C: FULL (0.32 GB) at 15:10: moved (not deleted) run 1120_093820's frames to D:\sim_runs_overflow\1120_093820_dex1_floor_12\frames.
  Move finished-run frames there at each session restart.
- ck_prune_item now KEEPS act meta.json; PRE_ACTION appends every action to <run>\actions.jsonl (commit 5b7002f). Run
  1120_093820's earlier act metas backed up in ...\1120_093820_dex1_floor_12\act_meta\.
- New session: run C:\Users\raresense\sim_home\runs\1120_150110_dex1_floor_13 (slot home), loader live_cmd\f13\a00_load.py
  (chain end 2493 + sync_cloth(force=True) + f12 helpers + towel creeper).
- PAPER r195i1 REDO (look agent: an old drop missed the bin, it lay at (-0.03,1.57)): ckpt
  ...\1120_150110_dex1_floor_13\checkpoints\0091_item_r195i1_paper_redo. pick_floor (guard passed); put_away's drop_in
  "no free path"; teleop beside the bin (pelvis (-0.14,1.76) facing south): lean 0.35, hand over the bin middle, open: inside.
- Chain 32-33: SHOES r105i1 / r105i2 on the mat by the scout's calls (E:\urc_scout hall.py shoe_to_mat): ckpts
  ...\1120_150110_dex1_floor_13\checkpoints\0212_item_r105i1_shoe (721 s wall) and 0328_item_r105i2_shoe (688 s);
  shoes at (1.852,-1.995) / (1.647,-1.99).
- UMBRELLA r107 VERIFIED (session 2, run C:\Users\raresense\sim_home\runs\1120_150255_scout_hall2_AI_operated, from
  ...\1120_114552_scout_hall_AI_operated\checkpoints\1517_item_r105i2_shoe): umbrella_to_entry() done, 524 s wall, final
  (3.084,-2.445) lying (hull top 0.068); end ckpt ...\1120_150255_scout_hall2_AI_operated\checkpoints\0095_item_r107i1_umbrella.
- TOWEL r100: NOT DONE. Its COLLIDER is a flat slab 46 x 50 x 2.2 cm (corners (-1.121,1.305) (-0.817,1.177) (-0.661,1.546)
  (-0.966,1.674), z 0.596-0.618, 0.6 kg) lying on the bar stool object_0231 (top x -0.93..-0.57, y 1.17..1.53, z 0.55-0.61);
  the drape is visual only. Seen: (1) stance facing north at (-0.86,1.01): right knee into the stool legs (134 N);
  (2) from the WEST, stance (-1.403,1.073) facing east, left hand, pinch 2 cm in at the west corner (overhangs 19 cm):
  both jaws 5.3/4.6 N, rise 0, tilt 0, hold ok (live_cmd\sc\t03_pinch.py; close-up ...\hall2\grasps\hold_r100i1_towel_t9730.jpg);
  hand +10 cm -> slab rose only 5 cm, tilted 10 deg (pivots on the pinch: 1.9 N m on 2.9 cm pads, the far side stays on
  the stool); (3) hand +12 cm more and 0.30 m back-step: the slab slid out of the jaws and stayed on the stool ("held thing
  lost"). A flat 46 x 50 slab also cannot lie INSIDE the octagonal hamper (flat-to-flat 0.56 m, half-diagonal 0.34 > 0.30):
  it would rest on the rim. Next idea (not tried): two-hand pinch of the two west-edge corners (the r106 umbrella plan,
  f12\u00_helpers.py edge_stance), lift level, carry, set it ACROSS the hamper top (inside() passes) or ask the coordinator
  for another place (e.g. on the sofa arm / dryer).
- Chain 34: SMALL UMBRELLA r107 by the entry by the scout's umbrella_to_entry (hall.py): ckpt
  ...\1120_150110_dex1_floor_13\checkpoints\0412_item_r107i1_umbrella (461 s wall), at (3.092,-2.436).

## HAND-OVER 20 Nov ~16:45 (fourteenth home agent, Dex1 floor; working memory low). AI-operated. READ THIS FIRST.
- CHAIN END: C:\Users\raresense\sim_home\runs\1120_150110_dex1_floor_13\checkpoints\0412_item_r107i1_umbrella -> 34 of 40
  (progress_pct prints 35: it counts "r195i1_paper_redo" as an item; its "set aside r193i1/i3" line is stale: both are in
  the basket). Robot at (3.54,-2.10) facing south by the entry, hands at rest.
- This agent: scooter r126 (Fable call + teleop finish), scene reduced to 40 (0895_item_scene_removed_40), pouch r149,
  nugget r93, toys r193i4 / r192 / r193i2 / r193i1 / r193i3, duck r120i1 (scout), tissue r158, paper r195i1 redo, shoes
  r105i1 / r105i2 (scout), umbrella r107 (scout).
- Load: copy live_cmd\f13\a00_load.py with CHAIN = the chain end (it calls sync_cloth(force=True), execs the f12 helpers
  u00_helpers / basket_put (toy_trip, basket_put) / cpick (corner_pick, bin_drop) / surf_item, towel in CREEPERS).
  Scout calls: exec E:\urc_scout\scripts\home\live\hall.py (branch scout-hall 3a81441).
- Guard: f12\mem_guard.ps1 -KitPid <kit pid> (stops at commit free < 3.5 GB, kit private > 16 GB, C: < 2 GB). A fresh
  session is ~14 GB private. Restart at an item checkpoint when private > 15 GB; move finished-run frames to D:\sim_runs_overflow\.
- LEFT (6): 
  * TV door r159: kitchen_skills.close_door_follow under call_mon (f12\p01_door.py) reached -0.918 rad (53 of 90 deg) in
    741 s sim before the commit-memory crash; r191 is no longer at the door. Run it again from the chain end (~35 min wall).
  * sponges r83 LAST (Fable's island_pick call). With the grasp guard: island_skills.two_hand_pick calls hold_on(...)
    which the guard REFUSES (jaw bases press, fingers off) -> wrap it: hold_on(s, n, share, guard=False) ONLY after its own
    check (coordinator): both hands' solver contact force on the box > ~5 N each, only the hands touching it; log it and
    look at a close-up at that moment.
  * PARKED pending the user's decision: wrapper r87 (island top 15 cm in; stool r99 is STATIC; scissors r108 loose -> may
    be removed as an obstacle under REMOVED_FOR_40.json "removed_obstacles"; idea: level hand as for the nugget from
    x ~1.95), stick r154 (flat 1 cm on the coffee table, already overhangs the west edge 6 mm; slide_out's measured press
    stayed 0), toy vehicle r191 (at the basket's north edge (-5.17,-1.25), no stance even tight; its 7 cm section fills the
    jaws: fingers lose it in a walk), towel r100 (scout: flat 46 x 50 x 2.2 cm slab on the bar stool, pivots out of a
    one-hand pinch; cannot lie inside the hamper; see SCOUT notes).
  * basket r186 route entries: done when all toys are in and the basket is at its place (r191 is not in).
- Coordinator asks: at every item end check the item is really inside its destination before the item checkpoint, and a
  final sweep over ALL done items with that check (not done yet).
- Code (E:\urc_home home-cleaning): ad717c8 ops.remove_bodies, 8fa8cc5 grasp-QC hold_guard, 5b7002f actions.jsonl + keep
  act meta.json. Session helpers in live_cmd\f12\ (not committed: basket_put.py, cpick.py, u00_helpers.py, slab.py,
  qc_patch.py, ck_patch.py, mem_guard.ps1).

## 20 Nov ~15:51- (fifteenth home agent, Dex1 floor; AI-operated). Run C:\Users\raresense\sim_home\runs\1120_155109_dex1_floor_14, cmd files live_cmd\f14\
- Session: slot "home" 47960 (kit pid 16644, 13.7 GB private after the load), guard f12\mem_guard.ps1 on, loader f14\a00_load.py
  (= f13 loader with CHAIN 0412_item_r107i1_umbrella). Start still look\f14_a01_start.jpg: robot by the entry, all as left.
- TV door r159: f14\b01_door.py = close_door_follow called again (max 3 calls) while each call makes progress (one call
  does only ceil(remaining/20)+2 stages and the last try made ~10.5 deg a stage), all under one call_mon (t_max 3600).
- Chain 35: TV DOOR r159 SHUT (ckpt C:\Users\raresense\sim_home\runs\1120_155109_dex1_floor_14\checkpoints\0429_item_r159i1_door),
  q -1.561 (shut end -1.571, 0.6 deg off), monitor clean, 947 s sim / 2505 s wall (two Isaac sessions running: ~2x slower).
  Call 1 = 7 stages 0 -> -1.352 (stages of 8-20 deg; its own stage count ceil(remaining/20)+2 ran out), call 2 = 1 stage
  -> -1.561. Frames tele\0001_end_r159i1_door_done.jpg, look\f14_b02_door_shut.jpg. Kit peaked 15.07 GB private.
- GOTCHA guard: h_live's "ISAAC READY ... pid N" is the cmd.exe WRAPPER (0.004 GB); mem_guard.ps1 must get the kit.exe
  child pid (Get-CimInstance Win32_Process -Filter "Name='kit.exe'", command line --port 47960). Here 31668.
- Sponges r83i1: f14\c00_sponge_guard.py wraps hold_on for the sponge body (object_0212_body): solver contact force
  (mj_contactForce on br.mjm/br.mjd) per hand (left_*/right_* Dex1/wrist links) > 5 N each and no other body touching,
  logged (SPONGE_CHECK, EVENTS), close-up <run>\grasps\two_squeeze_*.jpg, then hold_on(guard=False); else raises.
  f14\c01_sponges.py = preconditions (dishwasher joints, tray south strip) + island_pick under call_mon.
- Sponges try 1 (f14\c01, from the door item end): FAILED by the monitor, right knee 65 N on the island's base face while
  settling on the stance (0.708,0.066) after the last leg (mode swing). SEEN (frames room/head 30234-30342 =
  look\f14_c01_knee_sheet.jpg + contact probe f14\c03): at walk height (pelvis z 0.673) the knees are 0.19 m AHEAD of the
  pelvis (x 0.895/0.903); the knee shell touched the base face at x 0.96, z 0.26. Fable's runs stood at z 0.77 (knees back).
  Retry 1 (f14\c04): from 0446_act_walk (robot (0.558,0.066) facing east, before the last leg), stance x 0.68 (knee ~3 cm off).
- Sponges retry 1: DONE (one call, monitor clean, 233 s sim / 601 s wall): roll 90 deg, two_hand_pick 10.9/10.8 N, rose 6.1 cm;
  squeeze check at hold_on: solver force L 11.58 N / R 11.56 N, nothing else on the box -> hold_on(guard=False)
  (close-ups grasps\two_squeeze_object_0212_body_left_t13913.jpg / _right_); set down on the tray table (object_0225_body,
  r94) south strip, box x 1.436-1.661, y 1.493-1.589, z 0.755-0.835, 7 mm off the spot, rests on the tray only.
  Chain 36: ckpt C:\Users\raresense\sim_home\runs\1120_155109_dex1_floor_14\checkpoints\0557_item_r83i1_sponges.
  NOTE: body_of("r94i1_tray_table") is None (static); the tray is object_0225_body.
- FINAL SWEEP over ALL 36 done items at 0557 (f14\d01-d04, <run>\final_sweep.json; stills look\f14_d03_toy_corner.jpg,
  _hamper.jpg, _mat.jpg, _bin.jpg):
  * OK (35): 7 garments in the hamper r133 / basket (in_container: rag, blanket, jacket, knit hat, santa hat 100 %, coat
    pile 99.3 % (3 cm over the rim line), stocking r190 100 % in toy basket r186); bin: papers r195i1/i3, plastic bag r196,
    pouch r149, tissue r158 (inside); mat r119: sandal r124, croc r122, flats r125i1/i2, shoes r105i1/i2; toy basket r186:
    ducks r120i1/i2, ball r178, toy pouch r179, nugget r93, ball r192, toy pieces r193i1-i4; floor spots: slipper r123
    (1.7 cm), scooter r126 (0), umbrella r107 (1.6 cm), cardboard box r175 (4.4 cm from its spot; at_place says False only
    because its dest string is not "floor"); TV door r159 q -1.561 (shut -1.571); dishwasher door r32 q -1.571 (shut),
    racks r33 0.358/0.282 (in, door shut over them); sponges r83 on the tray.
  * NOT at its place (1): LIGHT SABER r130: lies flat on the floor beside the toy basket (box x -5.317..-4.764,
    y -1.614..-0.879), centre (-5.041,-1.246), 0.20 m from its recorded spot (-4.92,-1.405) (SPOT_TOL 0.15). Not a mess,
    but moved since it was placed (the scout's rest_hands hit it, 31 N; toy vehicle r191 was dropped beside it).

## HAND-OVER 20 Nov ~17:40 (fifteenth home agent, Dex1 floor; to-do list done). AI-operated. READ THIS FIRST.
- CHAIN END: C:\Users\raresense\sim_home\runs\1120_155109_dex1_floor_14\checkpoints\0557_item_r83i1_sponges -> 36 of 40
  (this agent: TV door r159 = 0429_item_r159i1_door, sponges r83i1 = 0557). Robot at (1.527,0.969) facing north by the
  tray table, hands at rest, standing.
- Load: live_cmd\f14\a00_load.py with CHAIN = the chain end (f13 loader: load_floor, sync_cloth(force=True), helpers).
- LEFT (4), all PARKED for the user's decision: wrapper r87, stick r154, toy vehicle r191, towel r100 (notes above). The
  basket r186 route entries count as done once r191 is in or dropped by the user.
- Final sweep: 35 of 36 done items at their place; light saber r130 is 0.20 m off its spot (beside the basket, on the floor).
- Guard: pass the kit.exe pid (child of h_live's cmd.exe pid) to f12\mem_guard.ps1.
- Isaac STOPPED, slot "home" freed. No code changes in E:\urc_home (session files only in live_cmd\f14\).
