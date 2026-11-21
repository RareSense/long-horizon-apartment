# FINAL CLEAN RECORDED EPISODE (Apartment 1122, G1 Dex1, AI-operated) - progress / hand-over

Goal: repeat the 36 items of the first chain cleanly from the episode START, with full recording (actions.jsonl, 30 Hz
StateRec full state in <run>\states, act checkpoint meta.json never pruned), for the HQ video rendered from states.

## Setup (20 Nov, final-episode agent)
- Code: worktree E:\urc_final, branch final-episode = home-cleaning 6173b19 + replay-tool + final-look (then tag look-final
  4c9a52a) + scout-hall + kitchen-fable2 + scooter-fable; commit aa96c34 repoints the hard-coded E:\urc_home paths to
  E:\urc_final (so live sessions run StateRec / actions.jsonl / merged skills). Never push.
- Start a session: env URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp URC_TEXTURED=1 URC_ROUGH_FLOOR=0.8, then
  py -3.12 E:\urc_final\scripts\home\live\newlive.py <TAG> E:\urc_final\rooms\apartment_1122_full.json
  Send code: py -3.12 E:\urc_final\scripts\isaac_cmd.py --port 47960 <file.py> (write files with the Write tool: no BOM).
- Session files: C:\Users\raresense\sim_home\apartment\live_cmd\final\ (a00_start.py = STEP 1 loader; guard.ps1 -KitPid
  <real kit.exe pid> logs to guard.log and stops at commit free < 3.5 GB / private > 16 GB / avail RAM < 2.5 GB / C: < 2 GB).
- Removed at frame 0 (26): REMOVED_FOR_40.json removed_sink_bound + removed_hard + removed_final (wrapper r87i1, stick
  r154i1, toy vehicle r191i1, towel r100i1: "user: finish at 36").
- Item order = the first chain's chain-end route, first 36 steps (meta of 1120_155109_dex1_floor_14\0557).

## Session restarts / pieces (for the render worker)
(one line per session: run folder, from checkpoint, first frame)
- Session 1: run C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final, kit pid 29644, from seg3 0000_item_start;
  episode starts at frame 100 (0001_start_clean). Frames 0-99 = boot + frame-0 removal settle (skip).
- Reloads inside session 1 (pieces.json; frames after a reload replace the discarded branch):
  * frame 22883: ck_load 0342_act_put_down (r193i3 aside walk put a foot on ball r192; discarded frames ~22200-22880)
  * ~44759 / ~45926: ck_load 0666 (out of the hamper pocket; step_to knee on scooter + side-step branch discarded)
  * ~51227: ck_load 0707 (blanket dragged on the jaws after a failed grasp)
  * ~66065: ck_load 0940 (west strand retry, then discarded); ~68618: ck_load 0800 (blanket held at the entry; north approach)
  * Fable: 80574 load 1164; 85336 load 1267 (84081-85336 dropped); 89780 load 1312 (86633-89780 dropped); 98045 load 1518
    (97798-98045 dropped). Kept but ugly: ~91351-93898 right hand fumbling at the north rim (cut candidate).

## Chain (item checkpoints, in order) - run 1120_181556_dex1_floor_final\checkpoints\
1. 0063_item_r123i1_slipper - go_item (aside spot by the toy bike), clean (final\b01)
2. 0123_item_r195i3_paper - go_item stopped (left knee on the bin 25 N); teleop b04/b06 (step back, squat -0.15 lean 0.6, open over the bin), done b07
3. 0229_item_r195i1_paper - c01 pick_floor + walk_tight (0.16,1.05,90); teleop c02-c04 (0.07 fwd, two-stage servo, lean -0.10/0.5, open)
   (asides, not items: 0321/0322_item_aside_r193i1 set_aside (-2.927,-0.581); 0372_item_aside_r193i3 via reload 0342 +
   tmove back 0.12 + put_away_any at (-2.79,-0.605) - d01/d02/d03)
4. 0468_item_r131i1_knit_hat - go_item, clean (e01)
5. 0529_item_r189i1_santa_hat - go_item, clean (e02)
6. 0662_item_r121i1_jacket - go_item hit the 240 s cap holding it; drop_in_cloth from there (e03-e05)
7. 1587_item_r117i1_blanket - out of the hamper pocket by teleop east along y -1.17 (f11); Fable grasp p136 from (0.912,-1.498,30deg)
   (f15); carry to (-1.45,-1.17) facing east (f21), backward steps west + turn south to the north pre-stance (f22);
   bigcloth step_in + first_end (f23); then FABLE teleop g01-g43 (near-fold strand hold, lift2, teleop releases). ~2 h.
8. 1994_item_r116i1_coat_pile - h01 (teleop out east + bigcloth grasp uv (0,0.30)), h02 (carry to corridor, back west, turn
   south), h03 (step_in + first_end; strand missed); Fable g50-g60: one fore-aft pinch where the sleeves cross (fingers 35
   deg right), lift2, bc_both down, teleop releases, retract. Reload 1785 at rec.n 117833 (one branch kept).
9. 2136_item_r124i1_sandal - exit_pocket teleop + pick_floor left + walk (1.38,-2.08,180) + staged squat/lower/open (i01)
10. 2253_item_r122i1_croc - pick_floor right + put_down (1.20,-2.02) stopped 4 cm off; lower_put finish (i02, i05)
11. 2491_item_close_dishwasher - kitchen_skills.step_mon, one call (i03)

## NO-AI RUNNER (user, 20 Nov ~23:30: as little AI as possible) - items 12-36
- Code (committed, E:\urc_final final-episode 0aecc17): E:\urc_final\scripts\home\final_run\
  runner.py (outside Isaac, drives the live session on port 47960), items_lib.py (one function per item = the proven
  call, attempt 0/1/2 with small variations), common_a.py (= live_cmd\final\chk.py guarded item check + lower_put +
  exit_pocket), common_b.py (_start_item / _finish: item_done_auto only when item_check ok, nothing held, standing),
  resume.py (loader of a fresh session from the last good item checkpoint).
- Started 20 Nov ~23:35 detached (BelowNormal): py -3.12 E:\urc_final\scripts\home\final_run\runner.py
  C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final
- Per item: up to 3 attempts; between attempts route_v3_resume(last good item checkpoint); after 3 failures the item is
  SKIPPED: a line in C:\Users\raresense\sim_home\apartment\RUN_NEEDS_AI.txt, reload, next item. Restart (newlive.py
  dex1_floor_final_sN + resume.py; old frames -> D:\sim_runs_overflow\<run>\frames) when kit private > 15 GB or the
  session died; each restart and each item is appended below. End: RUN_DONE.txt (done / skipped / route left).
- Log: C:\Users\raresense\sim_home\apartment\final_runner.log; per-attempt outputs in live_cmd\final\runner\<item>_a<k>.out
- To restart the runner by hand (session alive): same command with the CURRENT run folder (and session number as 2nd arg).
- Items with a known weak spot (likely SKIPPED -> one AI batch): stocking r190 (first chain needed a teleop release in a
  squat), light saber r130 (the first chain moved scooter r126 0.26 m west first), toy pouch r179 (two-hand pick),
  scooter r126 (last set-down needed the right squeeze eased to 6 N), nugget r93 (on the island), tissue r158.
### Runner item log (appended by runner.py)

## Gotchas seen in this run
- Loader must call sync_cloth(force=True) after a checkpoint load (garment drawings stay stale until the cloth steps;
  StateRec records the true particles anyway). Never re-apply look code in the live session (coordinator).
- Bin drop: from 0.5 m the hand cannot reach the bin's middle; stand ~0.38 m from the bin centre, servo in 2 stages, lean.
- A second kit.exe (render worker, slot cloth) takes ~15 GB: commit free fell to 5.6 GB (coordinator: it yields to this run).
- Item checkpoints go through final\chk.py's guarded route_checkpoint (destination check first; CHECK_FAIL = not saved).
- After the hamper items the robot is boxed in (scooter r126 north, rug toys west): stance_for/walk_path say "no place to
  stand"/inf. Get out by teleop EAST along y -1.17 (f11) - never NE (knee on the scooter).
- Blanket: bigcloth's grasp stance (yaw 0) closed on nothing and the cloth snagged and was dragged: use Fable's stance
  heading 30 deg (f14/f15). West front stance gives no strand reach; north front stance needs teleop (f21/f22).
- Hamper north handle arch at y -1.712, top z 0.67: jaws there never lock (Fable). Release only with steep fingers.
- Guard: guard.ps1 now logs to guard2.log (guard.log got locked by a stray tail); run it via Bash run_in_background.
- 2584_item_r68i1_rag - r68i1_rag (no-AI runner, attempt 0) in C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final

## HAND-OVER 20 Nov ~23:35 (final-episode agent ending its session, by the user's order: no more AI unless needed)
- CHAIN: run C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final, items 1-11 by this agent (list above), item 12
  rag by the runner (2584_item_r68i1_rag, attempt 0, 14.5 min). The no-AI runner keeps going (pid 19964, detached).
- A fresh agent is needed ONLY if RUN_NEEDS_AI.txt has SKIPPED lines (or a STOP line) once RUN_DONE.txt exists: load the
  last good item checkpoint named there (route_v3_resume + gait_on + settle; helpers: final_run\resume.py with CHAIN set)
  and do the skipped items by AI teleop in one batch; the route keeps skipped items behind POS (_bring moves one to POS).
- Final sweep still to do at the very end (all 36 at their place; light saber within 0.15 m of (-4.92,-1.405)): item_check
  over DONE (live_cmd\final\chk.py) or the f14\d01_sweep.py logic.
- Session: slot "home" port 47960, kit pid 29644 at ~14.5 GB private (restart expected at the next item over 15 GB).
- Guard: guard.ps1 (log guard2.log) started by the runner for each kit pid.
- Escalation used: Fable (agent a3936bfee4a1e499a) for the blanket and the coat pile (g01-g60 in live_cmd\final).
- SKIPPED r196i1_plastic_bag (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r190i1_stocking (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r125i2_flat (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r130i1_light_saber (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r120i2_duck (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r125i1_flat (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r175i1_cardboard_box (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r178i1_ball (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r179i1_toy_pouch (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r126i1_scooter (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r149i1_pouch (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r93i1_nugget (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r193i4_toy_piece (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r192i1_ball (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r193i2_toy_piece (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r193i1_toy_piece (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r193i3_toy_piece (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r120i1_duck (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r158i1_tissue (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r105i1_shoe (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r105i2_shoe (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r107i1_umbrella (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r159i1_door (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r83i1_sponges (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)

## FIX 21 Nov ~01:10 (AI-operated short fix: runner failed all 24 items after the rag)
- Root cause: drop_in_cloth left the robot WEST of the hamper at (-2.53,-2.22) yaw 60 with the right hip on it (7 N at rest);
  _start_item's pocket test (x<-1.6, -2.0<y<-0.95) missed that spot, so exit_pocket never ran and every item aborted on the
  first move (MONITOR "pressing r133i1_laundry_basket", "no place to stand", "neighbour knocked").
- Fix: new exit_hamper_west() (common_a.py), called by _start_item for x in (-3.0,-2.42), y in (-2.6,-1.6): side 0.08 left,
  face north, north along x -2.62 to y -1.19, then exit_pocket east along y -1.19 to x -1.45. Driven live by teleop first
  (tele 0227-0253), saved as chain checkpoint 2860_item_r68i1_rag_stepout (rec ~176030).
- Verified: r196 plastic bag a0/a1 walked out and reached its stance, but failed the pick itself (corner_pick: pads 0.4 m
  above the corner; item problem, runner retries k2/skips). r125i2_flat a0 OK -> 3158_item_r125i2_flat, then stood up
  (ended in a deep squat) -> 3161_item_r125i2_flat_stand (chain continues from here).
- Reload frames for the render (StateRec rec.n): runner's 24 failed attempts all reloaded 2584 (rec 161449..172504, discard);
  step-out from 172504 to 176030 (keep); plastic bag a0 discarded by reload of 2860 at rec 180117, a1 by reload of 2860 at
  rec 184208; flat + stand from 184208 (keep).
- Runner relaunched 01:09:57 (pid 20040 py / 17512 python, BelowNormal) from 3161; stdout final_runner_stdout2.txt.
  Old RUN_DONE.txt / RUN_NEEDS_AI.txt renamed *_prev.txt.
- SKIPPED r196i1_plastic_bag (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r190i1_stocking (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r130i1_light_saber (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r120i2_duck (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r125i1_flat (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r175i1_cardboard_box (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r178i1_ball (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- SKIPPED r179i1_toy_pouch (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)

## NIGHT FINISHER 21 Nov ~01:30- (AI-operated agent; runner stopped, session driven by AI teleop + runner subsets)
- Root causes of the 01:10-01:30 skips: (1) 3161 leaves the toes 4 mm from croc r122i1 (mat): every first walk aborted
  "foot on a loose thing: r122i1_croc" -> common_b.clear_feet() (step off a loose floor thing at a toe/heel before the
  first move; 2 x 0.12 m back here). (2) ORDER: the toy-corner items (stocking, duck r120i2, flat r125i1, box) walk over the
  plastic bag r196 -> the bag must go first (as in the first chain). (3) scooter: saber r130 still under its deck.
  (4) ball r178 / toy pouch r179: toy_trip has no stance / no jaw section (first chain: sill teleop / two-hand hold).
- Reloads in session 1 (rec.n, StateRec of run 1120_181556_dex1_floor_final) - discard the branch before each:
  208192 load 3161 (runner's 01:10-01:32 attempts discarded); 211713 + 214423 load 3386_act_n1_off_croc (bag tries);
  218456 load 3480_act_n1_bag_stance; 218919 load 3161; 221774 load 3161 (runner stocking a0). Everything after
  rec 221774 in session 1 is DISCARD (a stray runner attempt ran together with an AI command; the kit died at 02:13).
  Session 1 kept frames end at rec 208192's branch point = 3161 (the chain continues from 3161 in session 2).
- Session 2 (02:13, kit died/guard STOP at C: 1.19 GB transient): run C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2,
  from 3161_item_r125i2_flat_stand (session 1), StateRec frame 100 = 3161. Old run's frames moved to
  D:\sim_runs_overflow\1120_181556_dex1_floor_final\frames.
- PLASTIC BAG r196 GIVEN UP (21 Nov ~02:35, after 6 real tries: corner pinch jams/ejects the 10 g board, two-hand paddles ride
  over its 2 cm edge, pin + pinch tipped). Coordinator: do NOT teleport it (47 min already rendered with it visible): it stays
  lying where it is, untidied, dropped from the task list only (REMOVED_FOR_40.json "given_up_left_in_place"). The off-map
  branch (s2 act 0125 at rec 8836, meta "removed" stripped, marked DISCARDED) and the runner's stocking a0 after it are DISCARD.
  Chain in s2 restarts from a 3161 reload at rec 12969 (act ckpt n1_start_bag_kept right after).
- DISK (21 Nov 03:50): the guards' "C: < 2 GB" STOPs (02:13 and 03:48, both kits killed) come from the pagefile growing on C:
  under commit pressure (C: fell 5 -> 1.4 GB in 30 s with both kits alive). Frames of old non-final runs moved off C: (never
  deleted): 1120_052805_dex1_floor_8 -> D:\sim_runs_overflow\<run>\frames; 1120_032422_dex1_floor_7 ->
  E:\sim_runs_overflow\<run>\frames;
  1120_0826_scooter_fable_AI_operated, 1120_0542_kitchen_sink_AI_operated -> E:\sim_runs_overflow\<run>\frames.
- Session 2 died 03:48:24 (guard STOP, C: 1.37 GB) during the runner's flat r125i1 attempt 1 (attempt 0 FELL at the mat:
  discard). Kept chain end of s2: 0497_item_r120i2_duck (rec 38949). The runner restarts as s3 from 0497.
- Session 3 (no-AI runner restart, session gone): run C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3, from C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\checkpoints\0497_item_r120i2_duck; StateRec starts again at frame 0 in C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3\states (piece boundary). Old run's frames moved to D:\sim_runs_overflow\1121_021343_dex1_floor_final_s2\frames.
- Session 3: run C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3 (runner restart 03:48, from s2 0497_item_r120i2_duck, StateRec frame 100). s2 frames -> D:\sim_runs_overflow\1121_021343_dex1_floor_final_s2\frames. C: free 9.9 GB after the moves.
- 0167_item_r125i1_flat - r125i1_flat (no-AI runner, attempt 2) in C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3
- SKIPPED r93i1_nugget (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- 2182_item_r120i1_duck - r120i1_duck (no-AI runner, attempt 0) in C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3
- 2311_item_r105i1_shoe - r105i1_shoe (no-AI runner, attempt 0) in C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3
- 2408_item_r105i2_shoe - r105i2_shoe (no-AI runner, attempt 0) in C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3
- 2490_item_r107i1_umbrella - r107i1_umbrella (no-AI runner, attempt 0) in C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3
- 09:05: session-3 working frames (old JPEGs, 21404 files, 1.6 GB) moved to E:\sim_runs_overflow\1121_034845_dex1_floor_final_s3\frames (the live session keeps writing new stills, every 300th frame, into the run's frames folder).
- 2923_item_r159i1_door - r159i1_door (no-AI runner, attempt 0) in C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3
- SKIPPED r158i1_tissue (no-AI runner, 3 attempts; see RUN_NEEDS_AI.txt)
- Night chain so far (item checkpoints, in order): s2 (run 1121_021343_dex1_floor_final_s2): 0368 stocking r190, 0497 duck r120i2;
  s3 (run 1121_034845_dex1_floor_final_s3): 0167 flat r125i1, 0668 box r175, 0800 ball r178, 0986 toy pouch r179, 1251 toy r193i4,
  1338 ball r192, 1437 toy r193i2, 1535 toy r193i3, 1632 toy r193i1, 2182 duck r120i1, 2311 shoe r105i1, 2408 shoe r105i2,
  2490 umbrella r107, 2923 TV door r159, 3140 tissue r158, 3261 pouch r149, 3677 light saber r130 (4.8 cm from its spot; it
  rests diagonally across the toy basket's rim). Commands: C:\Users\raresense\sim_home\apartment\live_cmd\final\n1\
  (reload log RELOADS.txt there).
- Scooter r126 by the FABLE escalation (agent a81e5311fe98753ea): 4072_item_r126i1_scooter (s3). Fable reloads (rec.n -> ckpt): 255364 -> 3697_act_n1_scooter_pre (my 3 grip tries 3697..255364 discarded), 258049 -> 3854, 258835 -> 3862, 263781 -> 3966; kept branch 3862 -> 4072. Command files live_cmd\final\fable_sc\.
- Session 3 ended 12:30 (kit 14.9 GB, clean stop) at 4072_item_r126i1_scooter. Its later working frames moved to D:\sim_runs_overflow\1121_034845_dex1_floor_final_s3\frames (the earlier ones are on E:, see above).
- Session 4: run C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4 (12:35, fresh start by the night agent; kit 31708), from s3 4072_item_r126i1_scooter, StateRec frame 100 = 4072 (piece boundary).

## HAND-OVER 21 Nov ~13:20 (night finisher, AI-operated). READ THIS FIRST.
- RESULT: 35 of 36 done; plastic bag r196 given up and LEFT IN PLACE (visible, not hidden, not teleported).
  Chain end: C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\checkpoints\0270_item_r83i1_sponges
  (session 4, kit 31708, slot "home" 47960 still running at the chain end). Summary: C:\Users\raresense\sim_home\apartment\RUN_DONE.txt
- Night chain (item checkpoints, in order):
  - s2 (1121_021343_dex1_floor_final_s2): 0368 stocking r190, 0497 duck r120i2.
  - s3 (1121_034845_dex1_floor_final_s3): 0167 flat r125i1, 0668 box r175, 0800 ball r178, 0986 toy pouch r179, 1251 r193i4,
    1338 ball r192, 1437 r193i2, 1535 r193i3, 1632 r193i1, 2182 duck r120i1, 2311 shoe r105i1, 2408 shoe r105i2,
    2490 umbrella r107, 2923 TV door r159, 3140 tissue r158, 3261 pouch r149, 3677 light saber r130,
    4072 scooter r126 (Fable).
  - s4 (1121_123451_dex1_floor_final_s4): 0134 nugget r93, 0270 sponges r83.
- PIECES FOR THE RENDER (StateRec frame numbers = rec.n of each run):
  - s1 1120_181556_dex1_floor_final: keep up to 3161 (rec 184208 onwards = the flat stand, kept to 3161's frame).
    DISCARD everything after the 3161 point: the 01:10-01:32 runner attempts and all night tries (reloads at rec 208192,
    211713, 214423, 218456, 218919, 221774). Session 1 died 02:13.
  - s2 1121_021343_dex1_floor_final_s2: frame 100 = 3161. DISCARD 100..12969 (bag tries, the off-map branch 0125 at
    8836 = DISCARDED, its meta "removed" stripped). Kept branch starts at the 3161 reload at rec 12969 (act 0170):
    - DISCARD 12969..15824 (stocking a0 over the bag).
    - Reloads: 15824 -> 0170; 19205 and 20107 -> 0231; 24274 -> 0306 (each discards the branch before it).
    - Kept: 0368 stocking.
    - 35901 -> 0368: the duck a0 branch is discarded; kept 0497 duck.
    - After 0497: runner flat attempts (a0 FELL); session died 03:48 -> DISCARD after 0497's frame.
  - s3 1121_034845_dex1_floor_final_s3: frame 100 = s2 0497.
    - Flat a0/a1: runner attempt 2 kept (0167).
    - Box: the a0/a1 branches are discarded by the reload of 0167; 39428 -> 0570 (knee branch discarded); kept 0668.
    - Ball 0800 kept.
    - Pouch: 63061 -> 0934 (the first set-down FELL, discarded); kept 0986.
    - Runner toy r193i4 tries: discarded by the reload of 0986 (my h01); kept 1251, 1338, 1437, 1535, 1632.
    - Runner nugget/pouch r149 tries: reloads of 1632 at 109419, 110198, 114115, 118032 (discard).
    - Runner tissue a0/a1: discarded by the j02 reload of 1632 at rec 136420.
    - Kept: 2182, 2311, 2408, 2490, 2923.
    - Runner tissue a0-a2 (reloads of 2923) discarded; my tissue 3064 -> 3075 -> (reload 3075) -> 3125 -> (reload 3125)
      -> 3140 kept.
    - 210944 -> 3140 (the pouch try with the knee on the bin + FALL discarded); 3152 off bin; kept 3261 pouch.
    - Nugget tries from 3284: discarded (falls); 225526 / 227808 / 228104 + m04 reload -> 3261 (saber tries discarded);
      kept 3415 -> 3677 saber.
    - Scooter: my 3 tries from 3697 discarded; Fable reloads 255364 -> 3697, 258049 -> 3854, 258835 -> 3862,
      263781 -> 3966; kept 3862 -> 4072.
    - Session 3 stopped cleanly at 4072.
  - s4 1121_123451_dex1_floor_final_s4: frame 100 = s3 4072; kept to 0270 sponges (rec 19979). DISCARD after 19979
    (sweep query reloads at 19985 and 20085).
  - Full list: C:\Users\raresense\sim_home\apartment\live_cmd\final\n1\RELOADS.txt (also committed in
    E:\urc_final\scripts\home\final_run\night_21nov\RELOADS.txt).
- Frames (working JPEGs, not needed for the render): s1 -> D:\sim_runs_overflow\1120_181556_dex1_floor_final\frames;
  s2 -> D:\sim_runs_overflow\1121_021343_dex1_floor_final_s2\frames; s3 -> E:\sim_runs_overflow\...s3\frames (early)
  + D:\sim_runs_overflow\...s3\frames (late). Stills now every 300th frame.
- OPEN ISSUE (final sweep): the rubbish bin (bottomless collider) was pushed ~7 cm NW and tilts 4.9 deg. Papers r195i3 / r195i1
  and pouch r149 now lie half under its walls (item_check inside False); the tissue is inside. It was already so at s4 0135,
  most likely from knee contacts at the bin during the tissue / pouch drops in s3 (3125..3261). Fix options:
  (a) pick the three from under the bin edge (corner pinch, floor posture) and drop them in again from 0.45 m;
  (b) redo the chain from s3 3125 with the drop stance 0.45 m from the bin (that loses the saber / Fable scooter / nugget /
      sponges branch).
  - The box r175 sweep "False" is only its description-string destination (1.5 cm from its spot, against the wall).
  - The light saber lies diagonally across the toy basket rim, 4.6 cm from its spot.
- Code (E:\urc_final, branch final-episode, author abdullahanxie, not pushed):
  - 99b5b42: clear_feet, runner subset + fallback ckpt.
  - 13140a8: pocket exit only in the real pocket.
  - 6d24f3a: stills every 300th frame.
  - 7ab0c06: surface_posture is sent with crouch.
  - 2a2e76c: night command files + reload log.

## COORDINATOR 21 Nov ~16:35: episode END fixed at s4 0270_item_r83i1_sponges
- The bin-fix agent made no progress after 14:58 (no item checkpoint after 0270) and was stopped; the robot session (slot home) was stopped to free memory for the user.
- FINAL CHAIN END = C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\checkpoints\0270_item_r83i1_sponges. Everything recorded in s4 AFTER 0270 (the bin push attempts) is NOT part of the episode: the final join must stop at 0270's frame.
- Known final-state flaw, stated openly: the bin is pushed ~7 cm / tilted 4.9 deg, two papers + the pouch lie half under its walls; the plastic bag r196 is given up, left in place.
