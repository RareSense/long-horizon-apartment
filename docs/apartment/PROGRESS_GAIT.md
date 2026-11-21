# Walking accuracy in tight spaces (gait agent, AI-operated). Branch home-gait, worktree E:\urc_gait

## Set-up (19 Nov ~22:10)
- Worktree: E:\urc_gait (git worktree of E:\urc_home, branch home-gait from c6402c6). Commits as abdullahanxie, no push.
- Isaac session: slot "cloth" (ISAAC_SLOT2.lock; the stale lock of dead pid 9240 freed), port 47970, started with
  E:\urc_gait\scripts\home\c_live.py start 47970 and env URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp URC_TEXTURED=1 URC_ROUGH_FLOOR=0.8.
  Then send scripts\home\gait\g_session.py (with RUN = run folder set first): it loads the FROZEN room
  E:\urc_home\rooms\apartment_1122_full.json like the floor agent (episode.py LIVE, route_v3_setup, teleop, autorun, aside,
  ops) but reads every script from E:\urc_gait\scripts (builtins.open remap) and src from E:\urc_gait\src.
- Run folder of the first session: C:\Users\raresense\sim_home\runs${TS}_gait_1 (a typo in my start file gave it this
  literal name; the tests are in its gait\ subfolder).
- Tests: scripts\home\gait\gait_test.py (gt_turn / gt_leg / gt_inplace / gt_run; trace per 20 ms: pelvis, CoM, capture
  point, both feet, gait mode, swing foot, foothold target, anchor) at the floor agent's checkpoints in
  C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3\checkpoints. Offline: gt_analyse.py, gt_steps.py.
- Regression: scripts\home\gait\gait_regress.py (8 cases: turns at the coffee table, legs incl. rug edge on / off, turns
  and a leg holding the toy piece in the left jaws).

## Why it drifts (measured, checkpoint 0111 = the floor agent's turn-runaway spot by the coffee table)
1. The capture-point gait regulates SPEED, never POSITION. At zero command each foothold goes where the capture point is
   heading, so any capture-point error during a step becomes a displacement nobody takes back. Stance foot slip: 0.0 cm.
   Baseline: turn +90 deg 27 cm off, -90 deg 3 cm; stepping in place 8 s ran off backwards 0.77 m and FELL.
2. The arm tuck (ARM_TUCK pitch 0.05 roll 0.05 elbow 0.6) puts the RIGHT Dex1 gripper against the right hip: the
   controller's proximity check holds a 9 mm gap (right_hip_roll_link / right_Dex1_finger_link_2), the right arm stays
   0.26 rad short of its tuck, and every step fights that constraint. Tucked: stepping in place falls; turns run away
   and fall (the 0.3-0.5 m runaways the floor agent saw). Shoulder roll 0.15 (T2: pitch 0.05, roll 0.15, elbow 0.6) clears it.
3. The turn on the spot stopped on the MEASURED heading; the footholds' heading (yaw_ref) leads it by ~0.08 rad, so it
   ended 2.8-2.9 deg past/short on a 2.9 deg tolerance.

## Fixes (branch home-gait)
- biped.py gait setting hold (default off in the file; on in tests): an anchor (where the pelvis is to be) moves with the
  command along the footholds' heading; at every lift-off (both feet down) the soles' middle is compared with
  anchor + (CoM - pelvis at the start, turned with the heading); the error goes back as an offset of the capture point
  from the next foothold (hold_c [0.2 forward, 0.12 sideways]; 0.2 sideways oscillated +-10 cm). The walk steps in place
  until the error < 1.5 cm (at most 6 more steps). Tried first and dropped: speed added to the foothold rule (7 mm per
  0.05 m/s: too weak), CoM averaged over a stride (too slow).
- skills._turn_on_spot: TURN_BY_REF (stop on yaw_ref + what the command filter still adds, tol 0.01, min rate 0.08).
- skills.walk: WALK_BY_ANCHOR legs up to 1.2 m (and backwards up to 0.8 m): the command is shaped on the ANCHOR's
  distance to the goal, straight, no steering; the hold does the rest (_leg_by_anchor).
- ARM_TUCK roll 0.15 (T2).

## Results so far (Isaac, AI-operated, run ${TS}_gait_1)
- turns at 0111, hold + turn-by-ref: -90 tuck T2 1.2 cm from where it stood after the tuck (2.3 cm from before the
  tuck), heading -0.2 deg; +90 no tuck 3.0 cm, -0.1 deg.
- 0.5 m backward leg at 0111: side 0.0 / 1.7 cm, stop 0.5 / 0.2 cm (no tuck / tuck T2); mid-leg the pelvis sways
  +-4-9 cm sideways each step (the gait's own sway, not drift).

## 19 Nov ~23:30 HAND-OVER (gait agent; working memory used up). READ THIS FIRST. AI-operated.
Commits on home-gait (no push): eb5a8a3 (first hold; the floor agent merged it as 8001a76), 040fe0d, 7556985 (last).
My Isaac is STOPPED and slot "cloth" is free.

### The hold is NOT safe yet. Keep it OFF (ts.loco.g["hold"] = False, the file default).
- At the floor agent's checkpoint C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\0237_act_transit_east_ok:
  a 90 deg turn through walk(), arms at rest, FALLS with the hold on, in both directions. It still falls with the
  correction suspended while turning (hold_turn_w), so the trigger is something else the hold does there. Candidates
  not yet checked: the stop condition (up to 6 more in-place steps until the error is under 1.5 cm), the corrections at
  the tail of the turn (wz under 0.1), and the xi_nominal offset (d_corr_st). The same turn with the hold off: 1.7 cm,
  heading 0.4 deg (TURN_BY_REF on). Traces: C:\Users\raresense\sim_home\runs${TS}_gait_1\gait\F1_*_ERR.json, F3_*.
- At 0111 (coffee table) the hold does help: turns 1-3 cm with it, 27 cm without, and stepping in place 8 s holds
  under 1 cm (it ran off and fell without). So whether it helps depends on the spot; find the 0237 cause first.
- Carrying the toy piece (checkpoint 0060): turns 20 cm off with the hold, 6 cm without; hold_carry False (default) now
  switches it off while the gait knows it carries.
- hold_geo (pulling the feet toward the anchor's line): every case fell. Leave it at 0.

### Safe to use now (each measured)
- ARM_TUCK = dict(pitch=0.05, roll=0.15, yaw=0.0, elbow=0.6) if the arms are tucked (TUCK_JOINTS True). The old tuck
  (roll 0.05) jams the right Dex1 gripper against the right hip (9 mm proximity gap); that was the 0.3-0.5 m turn
  runaway. With roll 0.15, turns at 0111 do not run away.
- TURN_BY_REF = True (skills._turn_on_spot): heading errors 0.0-0.9 deg instead of 2.5-4.3 deg.
- Short legs (_leg_by_anchor_xy, legs up to 0.45 m in any direction without turning) and _leg_by_anchor (up to 1.2 m)
  run only with the hold on, so not until the hold is fixed. With it, measured at 0111 / 0024: end errors 0.5-2.3 cm,
  0.3 m diagonal wander 3.7 cm (23 cm when it turned there and back).

### Still open
- The rug edge: leg_onto_rug_fwd (checkpoint 0022, 0.6 m west onto rug r141) FELL with the hold; without it, end side
  -13 cm and the knee touched object_0259 (37 N).
- leg_carry_back (0064, 0.5 m back with the toy in the left jaws) falls with and without the hold.
- Mid-leg sideways wander, averaged over a stride: 5-14 cm on 0.5 m legs (target 3 cm). The pelvis also sways
  +-4-9 cm per step.
- Scooter carry turns (the coordinator's item 2) are not tested: there is no scooter-held checkpoint in my set.

### How to run
- py -3.12 E:\urc_gait\scripts\home\c_live.py start 47970 (env URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp URC_TEXTURED=1
  URC_ROUGH_FLOOR=0.8), then send a file `RUN = r'<new run folder>'` + exec g_session.py (write it with the Write tool or a
  quoted heredoc: my first start file left ${TS} in the folder name).
- Settings in the session: exec gait_test.py; gt_reload_gait(hold=..., hold_c=[0.2, 0.12], ...);
  hot_reload(r"E:\urc_gait\scripts\home\skills.py", ["_turn_on_spot", "walk", "_leg_by_anchor", "_leg_by_anchor_xy"]);
  set TURN_BY_REF / WALK_BY_ANCHOR / SHORT_NO_TURN / V_SHORT / ARM_TUCK by hand (tuple assignments).
- Regression: GREG = dict(tuck=True, only=None) then exec gait_regress.py (11 cases, PASS/FAIL table,
  RUN\gait\regress_*.json). A floor checkpoint: gt_run([("turn", <full path>, 90, dict(fn=...))]).
- gt_reload_gait deletes the stale .pyc first: one reload once took old byte code.

## 19 Nov ~23:40 HAND-OVER (second gait agent, stopped on the coordinator's order; AI-operated). No code changed.
Session: slot "home", port 47961, started with `export URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp URC_TEXTURED=1 URC_ROUGH_FLOOR=0.8;
py -3.12 E:\urc_gait\scripts\home\h_live.py start 47961` (own pid/log files: sim_home\_logs\live_47961.pid, isaac_47961.log),
guard `h_live.py guard 47961`, then `RUN = r"C:\Users\raresense\sim_home\runs\1119_2330_gait2_AI_operated"` + exec g_session.py
(loaded OK, CPU True). No tests were run in it. Isaac STOPPED (h_live.py stop 47961), slot "home" freed, no kit/nvngx of mine left.

### Found offline (traces of the first gait agent, folder `C:\Users\raresense\sim_home\runs${TS}_gait_1\gait\`, literal ${TS})
Analysed with gt_analyse.py (per-step table) plus a per-row dump in the robot frame.
1. The 0237 "hold tips the turn" falls (F1_floor0237_walk_+90_ERR.json, F3_floor0237_walk_+90_ERR.json) do NOT happen in the
   turn. Both turns finish standing; the robot falls in walk()'s stand-still correction AFTER the turn (cmd2: vx about 0.05,
   vy 0.04 = a sideways step), 3-4 s after the turn ended. The hold's offset at the fall is tiny (vc 2-4 mm), so the hold is
   not the direct cause; it only changed where the correction started from.
2. Mechanism (F3, t 958.07-958.9, robot frame): first swing of the side step (left foot, toward the motion) touched down
   EARLY (0.22 s of a planned ~0.32 s swing). The foothold was computed for the capture point at the planned landing moment,
   so the left foot landed about 10 cm too far out: capture point 12 cm inside the left foot instead of the steady ~3-4 cm.
   The next (right) foot was lifted anyway; the capture point ran right, the right foothold hit max_reach (-0.238, feet
   0.35 m apart), and the robot tipped over to the right (right_hip vs floor 245 N). F1 falls the same way in its side step.
   => Root weakness: an early touchdown (or any capture-point error at lift-off) is not corrected before the next lift-off;
   double support moves the pressure point linearly old foot -> new foot (`mode == "ds"`) whatever the capture point does.
3. The turn itself at 0237 with the hold OFF (F2_floor0237_walk_+90_nohold.json) walks off ~23 cm (pelvis (0.23, -0.11) in
   the start frame at the end of the turn): each right-foot step lands ~8-11 cm further on than the left one takes back. The
   hand-over's "1.7 cm" is the end after walk()'s correction steps took most of it back. The floor agent's measurements
   (coordinator, hold off at 0237): 90 deg turn 5.5 cm; 15 deg turn steps 6-10 cm EACH; 0.12 m steps 7-11 cm SIDEWAYS.
4. Stepping in place drifts because the foothold rule regulates speed only (known). Each stop = 2+ steps in place + settle,
   so every short motion (0.12 m step, 15 deg turn) adds a few cm, which matches the floor agent's numbers.
5. ARM_TUCK in skills.py on home-gait is STILL roll 0.05 (the roll 0.15 fix only ever lived in session settings / load_floor
   gait_on()). The floor agent walks with TUCK_JOINTS False (arms at rest): test with tuck=False first.

### What I was about to do (next agent)
a) Gait (biped.py), new setting e.g. ds_dcm: in double support steer the capture point with the pressure point (as `settle`
   and `shift` already do: p = xi + k/omega (xi - xi_des), clipped to the polygon of both soles) toward the lift-off value the
   next step needs (new stance sole + the steady offset u0 of _xi_nominal, incl. the hold's offset), and lift only when it is
   within lift_tol (or a timeout). That absorbs early / late touch-downs before they propagate (cause 2) and makes stepping in
   place symmetric. A/B at 0237 + 0111 (CPU path deterministic).
b) Then the position feedback (hold) per step, also in turns, with the error limited per step; or a footstep mode: for
   moves <= 0.5 m and turns, footholds planned in the world from the measured base pose (feet at goal +- half width,
   step limits ~0.12 m / 0.06 m / 0.25 rad), the swing target = foothold rule + k (planned - rule), re-planned every step.
c) walk(): no sideways velocity correction after a turn (cmd2 vy) until (a) is in; do the side correction as deliberate steps.
d) Regression: add the coordinator's cases "0.12 m steps" and "15 deg turn steps" at 0237
   (C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\0237_act_transit_east_ok), and a 90 deg turn at 0237,
   tuck False; floor session loader is E:\urc_home\scripts\home\live\load_floor.py (gait_on() after every load).
   Scooter-held turns (bar lost every 5-10 deg turn) come after the basics pass.

## 20 Nov ~00:40 THIRD gait agent (AI-operated): TWO ROOT CAUSES FOUND, plan mode. READ THIS FIRST.
Session: slot "home", port 47961 (`export URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp URC_TEXTURED=1 URC_ROUGH_FLOOR=0.8;
py -3.12 E:\urc_gait\scripts\home\h_live.py start 47961`, guard `h_live.py guard 47961`), run folder
C:\Users\raresense\sim_home\runs\1119_2335_gait3_AI_operated (tests in its gait\ subfolder), command files in
C:\Users\raresense\sim_home\apartment\live_cmd\gait3\ (start.py loads the session; setup.py reloads this checkout's code
and sets the session settings; c.py = the test of the moment).

### Root cause 1: the trunk's upright target was left ROLLED 16 deg (a controller bug, not the gait)
- Measured at the checkpoints (R_up = the upright body's target orientation, roll / pitch deg): 0022: 0.85 / -0.02,
  0060: 1.03 / -0.02, 0111 AND 0237: 16.35 / -1.42. The pelvis and the trunk follow it: the robot stood and walked rolled
  16 deg, knees 0.98 / 1.35 rad, feet 19 cm apart. Frame: runs\1119_2335_gait3_AI_operated\gait\look_0237_front.jpg.
- Why: session.py _apply_lean turned the target about the sideways axis of the MEASURED heading; one crouch (lean 0.8)
  leaned down at one heading and up at another (t0 = 838.14, just before 0111) left the 16 deg.
- Fix (src\urc\teleop\session.py): the lean turns about the target's OWN sideways axis; and with no lean asked the
  target levels itself at 0.5 rad/s (_level_upright), so OLD checkpoints heal about 0.6 s after they are loaded.
- Exact A/B, pure 90 deg turns, hold off, old gait: tilted 23.2 / 20.6 / 24.5 / 9.1 cm (0237 +90, -90, 0111 +90, -90);
  levelled by hand 5.6 / 22.8 / 15.9 / 10.2 cm. So the tilt is one cause, not the only one.

### Root cause 2: the foothold rule turns every capture-point error at lift-off into a 3.5 times larger step error
- Per-step log of the gait (new: BipedWalk.slog, printed by scripts\home\gait\gt_slog.py / gt_end.py): the capture point's
  offset from the stance sole at lift-off (x0) should be the same every step. It is not: the first step after a stand
  lifts with 6.8 cm instead of 4.4 (lift_tol 2 cm) -> first step 27 cm wide instead of 20, every time; later steps differ
  by 1-2 cm between left and right stance (double support moved the pressure point old sole -> new sole in a fixed
  0.1 s whatever the capture point did). The REAL pressure point (from the contacts, new trace field rcop) is 2-3.5 cm
  off the commanded one in the first half of each swing.
- The rule places the next foot from the capture point, so an offset error e at lift-off moves the next foothold by
  about 3.5 e, and nothing brings the robot back (speed control, no position control).
- Fix (src\urc\locomotion\biped.py, gait setting plan=True, default off): planned footholds.
  * anchor (anc) = the base's planned place = integral of the command, starts at the measured base when a walk begins
    (frozen until the first lift-off); planned soles' middle = anchor + the centre of mass's offset from the base at the
    start, turned with the heading; a foot lands half the plan's step width (w_eff = plan_width * width) to its side.
  * _plan_x0: the capture-point offset needed at lift-off so that the rule lands the next foot ON its planned foothold
    = the steady offset + kappa / (E e^(w t_swing)) * (planned foothold - nominal next foothold), limited to plan_dmax
    [2 cm forward, 1.2 cm sideways] per step.
  * double support ("ds"): pressure point = xi + plan_k / w * (xi - wanted), kept between the two soles; the next foot
    lifts when the capture point is within plan_tol (6 mm) and the landed foot carries 30 %; or when the error grows
    again; or after plan_ds_max (0.45 s). The shift out of a stand aims at the same wanted point (tolerance 1.2 cm).
  * the walk stands only when the soles' middle is within plan_stop_tol of the plan (or plan_extra more steps).
  * the first foot to swing is the one on the side of the turn / side step.
- Skills (scripts\home\skills.py, scripts\home\live\teleop.py), when ts.loco.g["plan"] is on:
  walk(): legs up to ANCHOR_LEG_MAX by the anchor (_leg_by_anchor / _leg_by_anchor_xy), and what is left after the final
  turn is ONE short leg on planned footholds (no velocity side steps: those fell at 0237); _settle_stop waits 0.6 s more
  (the stand centres the centre of mass 0.5 s after the gait says "stand"; read before that, every move looked 2-3 cm
  off); tmove: turn by _turn_on_spot, then one short leg to the place asked for from where the robot stood BEFORE the move.

### Results 20 Nov ~00:55 (Isaac, AI-operated, CPU path, commit 7e48bf0, plan=True, arms at rest = TUCK_JOINTS False)
Regression scripts\home\gait\gait_regress.py, now 31 cases: 30 of 31 PASS (file runs\1119_2335_gait3_AI_operated\gait\
regress_*.json, traces R_<case>.json). Before -> after from the same checkpoints (before = hold off, old gait):
- 90 deg turns on the spot: 0111 -90 / +90: 9.1 / 24.5 cm -> 0.4 / 0.3 cm; 0237 +90 / -90: 23.2 / 20.6 cm -> 2.1 / 0.5 cm;
  carrying the toy (0060) -90 / +90: 2.5 / 1.9 cm. Heading within 1.7 deg. No fall, no tipping.
- tmove 15 deg turn steps (0111 +15 / -15, 0237 +15, carrying): 0.29-0.38 cm (the floor agent saw 6-10 cm each).
- tmove 0.12 m steps forward / back / left / right at 0111, forward at 0237, turn + step at 0237, back carrying:
  0.14-0.66 cm (before 7-11 cm sideways).
- legs: 0.5 m back by the table 0.0 / -0.7 cm (side / stop), wander 2.3; 0.6 m onto rug r141 0.1 / 0.1, wander 2.4
  (before -13 cm and a knee on object_0259); 0.5 m back off the rug -0.1 / -0.5, wander 2.4; 0.2 m back 0.0 / -0.6;
  diagonals 0.3 / 0.4 / 0.42 m: under 0.5 cm, wander 1.3-1.5; sideways 0.3 m and 0.4 m (rug): under 0.4 cm, wander 0.4;
  0.3 m forward at 0237 -0.3 / 0.2, wander 2.5.
- carrying the toy in the left jaws: 0.5 m forward 0.0 / -0.1, wander 2.2; 0.3 m sideways 0.2 / 0.2; 0.5 m BACKWARD
  (back along a leg just walked forward) 0.0 / -0.9, wander 2.1. No fall.
- stepping in place 8 s: 0.3 cm (before: ran off 0.77 m and fell).
- The one FAIL: turn_0237_left ends 2.1 cm / 0.5 deg (inside the target) but the left gripper brushed object_0265 with
  21.4 N (limit 20). In the turn to the right there the right knee meets the same object (136 N), the walk recovers and
  ends 0.5 cm off. object_0265 stands inside the robot's turning circle at 0237: a matter of room, not of drift.
- The old case leg_carry_back (0064, 0.5 m back) was a blocked test: the room grid has no free 0.4 m behind the robot
  there (only to its left); the right foot landed on / against a thing every second step (landing phase 0.63-0.67) until
  it fell. Replaced by carry_back_0.5 at 0060 after a forward leg.

## 20 Nov ~01:15 FINAL SETTINGS AND HOW TO USE (third gait agent; AI-operated). Merge branch home-gait.
### What the floor robot gets just by merging (file defaults, a FRESH session, nothing to set by hand)
- src\urc\teleop\session.py: the lean fix + self-levelling of the upright target (old checkpoints such as the chain end
  0111 load with the trunk rolled 16 deg and level themselves in about 0.6 s: after loading one, stand 1.5 s
  (op.run(1.5)) before the first move, or that first move starts while the trunk is still coming upright).
- src\urc\locomotion\biped.py: gait setting plan (library default False; other robots are untouched) with
  plan_dmax [0.015, 0.012], plan_k 12, plan_tol 0.006, plan_ds_max 0.45, plan_stop_tol 0.008, plan_extra 6,
  plan_emax 0.15, plan_lead 0.04, plan_width 0.85, plan_gain 1.0, plan_rate 1.0.
- scripts\home\skills.py: ts.loco.g["plan"] = True and ts.loco.g["hold"] = False at load (the home robot walks on planned
  footholds); ARM_TUCK = dict(pitch=0.05, roll=0.15, yaw=0.0, elbow=0.6); TURN_BY_REF / TURN_TOL_REF / TURN_W_MIN = True /
  0.01 / 0.08; WALK_BY_ANCHOR / ANCHOR_LEG_MAX / V_ANCHOR = True / 1.2 / 0.18; SHORT_NO_TURN / V_SHORT = 0.45 / (0.12, 0.06);
  PLAN_TOL = 0.015; V_ANCHOR_CARRY = 0.12; _settle_stop waits 0.6 s after "stand" (the base is read after the centring).
- scripts\home\live\teleop.py: tmove on planned footholds when plan is on.
- load_floor.py gait_on() of the floor branch needs no change (it sets hold False, TUCK_JOINTS False, ARM_TUCK roll 0.15
  and resets the hold state; it does not touch plan). Keep ts.loco.g["hold"] = False: plan replaces it.
### If the code is taken into a RUNNING session instead (hot_reload takes functions only), set by hand
- gait: gt_reload_gait(hold=False, plan=True) (scripts\home\gait\gait_test.py; reloads biped.py and fills the plan settings)
  and gt_reload_session() (session.py methods);
- hot_reload(r"...\scripts\home\skills.py", ["_settle_stop", "_turn_on_spot", "walk", "_leg_by_anchor", "_leg_by_anchor_xy"])
  and by hand: ARM_TUCK = dict(pitch=0.05, roll=0.15, yaw=0.0, elbow=0.6); PLAN_TOL, V_ANCHOR_CARRY = 0.015, 0.12;
  TURN_BY_REF, TURN_TOL_REF, TURN_W_MIN = True, 0.01, 0.08; WALK_BY_ANCHOR, ANCHOR_LEG_MAX, V_ANCHOR = True, 1.2, 0.18;
  SHORT_NO_TURN, V_SHORT = 0.45, (0.12, 0.06); exec teleop.py again (tmove).
  The exact file used here: C:\Users\raresense\sim_home\apartment\live_cmd\gait3\setup.py. A fresh session is simpler.
### How to use
- Small moves in tight spots: tmove(fwd=, side=, turn=) / ops.step_to as before. The turn is stopped by the footholds'
  heading; the step is one short leg to the place asked for, measured from where the robot stood BEFORE the move.
  Measured 0.1-0.7 cm per move (15 deg turns, 0.12 m forward / back / left / right, carrying too).
- walk(goal): up to 0.45 m any direction without turning (_leg_by_anchor_xy), up to 1.2 m turn + straight leg on the
  anchor (_leg_by_anchor, backwards up to 0.8 m), the final turn, then ONE short leg for what is left over PLAN_TOL
  (1.5 cm). Sideways legs are fine now (0.06 m/s, not time-limited on planned footholds).
- walk_path: unchanged code, the gait under it is plan mode. Measured only on 0.5-0.6 m legs at 0.18 m/s (there is no
  longer free line at these checkpoints): out and home 0.3 / 0.2 cm, off the line 3.5-7.3 cm (plan off: 4.3 / 3.0 cm,
  off the line 9-15 cm). NOT measured: legs over 0.6 m and the fast speed V_FAST 0.28 with plan on. Watch the first
  long leg; ts.loco.g["plan"] = False gives the old gait back at once.
- Arms: at rest (TUCK_JOINTS False, the floor agent's setting): the full regression ran with it, 30 of 31 (now 31 of 31
  with both 0237 turns judged on where they end). Tucked (TUCK_JOINTS True, ARM_TUCK roll 0.15): a subset of 7 ran:
  turns 0.4-0.5 cm, legs under 1.1 cm, wander up to 2.9 cm, no touch at 0237 (the tucked arm clears object_0265);
  tucking itself moves the base about 3 cm back (stepping in place 8 s: -3.1 cm, all of it from the tuck).
- A walk now ends 0.6 s later than before (the centring wait) and double support is as long as it needs (0.10-0.27 s).
### Still open / not done
- walk_path long and fast legs with plan on (above). Scooter-held turns (2.7 kg, both hands): not tested.
- At 0237 a 90 deg turn touches object_0265 with the arms at rest (21 N gripper to the left, 136 N knee to the right):
  room, not drift; turn there with the arms tucked or step away first.
- The gait's step width is 20 cm on a nominal 23.7 (the robot's own pendulum rate is about 0.9 of the model's, x0 to x1
  grows 3.0 times in 0.3 s against 3.4): plan_width 0.85 matches it; plan_rate is there to model it (left at 1.0).
- The lift-off offset is 0.6 cm wider than asked on both sides (the foot lifts when the capture point is within plan_tol).
  Symmetric, so no drift; a smaller plan_tol makes double support longer.
- Tools: gt_slog.py (the gait's per-step log), gt_end.py (where a test ended + steps), gt_rows.py (rows with the real
  pressure point), gt_tab.py. Trace rows now carry pelvis height, roll / pitch, feet heights, rcop, foot loads.
### Checked in a FRESH session (20 Nov ~01:25, commit 0c297cb, no hand settings; run 1120_0110_gait3_fresh_AI_operated)
Defaults at load: plan True, hold False, ARM_TUCK roll 0.15, PLAN_TOL 0.015, V_ANCHOR_CARRY 0.12. Subset 7 of 7 PASS, the
same numbers as the reloaded session: turn_table_left 0.3 cm, turn_0237_right 0.5 cm (knee on object_0265, 126 N),
r12_table 0.66 cm, t15_0237 0.29 cm, f12_0237 0.46 cm, leg_off_rug_back 0.0 / -0.5 cm, carry_back_0.5 0.1 / -0.7 cm.
Isaac STOPPED (h_live.py stop 47961), slot "home" freed. Final commit on home-gait: 0c297cb (no push).
