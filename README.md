# Long-horizon apartment clean-up (Unitree G1 + Dex1, Isaac Sim 6.2)

> **AI-operated.** Every robot command in this episode was issued either by AI agents (Claude Opus, with escalation to
> Fable on hard failures) or by a fixed, AI-written "no-AI runner" script. No human teleoperated the robot. The videos are
> replay renders of the recorded simulation states, not a live capture.

## The task

A Unitree **G1 humanoid with Dex1 parallel grippers** tidies a digital twin of a real apartment ("Apartment 1122", built
from the owner's photos, see `look/room_photos/`) in **Isaac Sim 6.2** (Newton, MuJoCo solver, CPU backend), as **one
continuous recorded episode**: walk to each item, pick it up (floor, table, couch, mat), carry it and put it where it
belongs (laundry hamper, toy basket, rubbish bin, shoe mat, ...), plus close the dishwasher and a TV cabinet door.

### Result, stated honestly

- **35 of 36 items done.**
- **Plastic bag (r196i1): given up.** Its collider is a 10 g flat board (15 x 20 x 1.1 cm); 6 real tries failed (corner
  pinch jams on the floor or ejects it, two-hand paddles ride over its edge, pin + pinch tipped the robot). It is **left
  lying where it was, visible and untidied**, for the whole video. It was not hidden, removed or teleported.
- **Rubbish bin nudged.** Knee contacts during the tissue / pouch bin drops pushed the bin (a bottomless collider) about
  7 cm north-west and tilted it 4.9 deg. In the final state **the two papers (r195i3, r195i1) and the pouch (r149i1) lie
  half under the bin's walls** instead of fully inside; the tissue is inside. This was not fixed (a later bin-fix attempt
  made no progress and is not part of the episode).
- The light saber (r130i1) ends 4.6 cm from its target spot, lying diagonally across the toy basket rim.
- The cardboard box (r175i1) reports "not at place" in the final sweep only because its destination is a text
  description; it is 1.5 cm from its spot, upright against the wall.
- **Scope:** the scanned apartment holds more loose objects. Before the episode started, 26 objects were removed from the
  scene at frame 0 (16 sink-bound dishes, 6 hard objects, and 4 more on the decision "finish at 36"). They are listed in
  `docs/apartment/REMOVED_FOR_40.json`, are out of every camera from frame 0, and are not claimed as tidied.

## How it was made

1. **Controller skills first.** The universal robot controller (private repo
   [RareSense/universal-robot-control](https://github.com/RareSense/universal-robot-control), branch `final-episode`)
   provides the skills: whole-body gait, `go_item`, `pick_floor`, `put_down`, `drop_in_cloth`, bigcloth grasps, kitchen
   `step_mon`, item checks, etc.
2. **AI teleop on failures.** When a skill failed, an AI agent drove the robot live in small steps (look at the rendered
   frame, send a command, look again) and the working commands were kept. All command files are in `teleop/live_cmd/`.
3. **Escalation to Fable.** Items the Opus agent could not finish went to a Fable agent: the blanket (r117i1), the coat
   pile (r116i1) and the scooter (r126i1). Their command files: `teleop/live_cmd/final/g*.py` and
   `teleop/live_cmd/final/fable_sc/`.
4. **No-AI runner.** From item 12 on, a fixed script (`scripts/home/final_run/runner.py` in universal-robot-control)
   ran the proven call per item with up to 3 attempts; it finished 8 items alone (marked "no-AI runner" below). Items it
   skipped went to an AI batch (`docs/apartment/RUN_NEEDS_AI*.txt`, `teleop/live_cmd/final/n1/`).
5. **Save-game checkpoints.** The full simulation state (physics, controller, cloth particles) was saved after every
   solved step (`checkpoints/NNNN_*`). After a failure the session reloaded the last good checkpoint and continued from
   there, never from zero.
6. **Failed attempts reloaded and excluded.** Every reload discards the branch before it. The full reload / discard log
   is `teleop/live_cmd/final/n1/RELOADS.txt` plus the HAND-OVER section of `docs/apartment/PROGRESS_FINAL.md`;
   `pieces.json` in each session lists the pieces. Only kept pieces are in the final video.
7. **Recording.** Every action with its arguments (`actions.jsonl`), the controller trace (`trace.jsonl`) and the 30 Hz
   full state (`states/chunk_*.npz` + `states/layout.npz`, StateRec) were recorded live. The memory guard ended the Isaac
   session 3 times, so the episode is 4 sessions (s1-s4); each session starts from the previous session's last good item
   checkpoint.

## The look (locked)

The realistic look is locked as tag **`look-final`** in universal-robot-control (commit 4c9a52a, merged into
`final-episode`): RTX real-time ray tracing with the final still settings (reflections, translucency, shadows, GI, AO,
sampled lighting), DLSS Quality, ACES tone mapping and film ISO per camera, bloom / vignette / grain. No path tracing.
Stills and photo-vs-render comparisons are in `look/` (v4 and v6 passes, compare sheets, and the room camera choice
`look/corner_cam_cand_12.jpg`).

## The final video

Two synchronised cameras, rendered from the recorded states by a no-AI render worker (`render_follow.py`):

| camera | file | resolution | fps | duration | size | SHA-256 |
|---|---|---|---|---|---|---|
| room corner camera | `episode_room_1080p.mp4` | 1920x1080 | 30 | 3 h 20 min 54 s (12054.4 s) | 11.29 GB | `9aefeb730c39b9e69ed8a8a5145cee281b13879c5227eccc087bb905517ecb45` |
| robot head camera | `episode_head_1080p.mp4` | 1440x1080 | 30 | 3 h 20 min 54 s (12054.4 s) | 13.04 GB | `dff1135f6a6569045b4e1fa799e0b5a6f63253421215d8e259037d67e773d58c` |

H.264, CRF 20. Google Drive folder `long-horizon-apartment` (see `DRIVE_MANIFEST.md`):

- Room corner camera: **TBD** (upload when the Google Drive app is running)
- Robot head camera: **TBD** (upload when the Google Drive app is running)

Notes: 3 h 21 min is the kept simulation time, not the wall time (the run took about 19 hours of wall time over
20-21 Nov 2026). One 60 s render unit (session 1 frames 112790-114589, during the coat pile) failed to render and is cut
from both videos; otherwise the join holds every kept frame from the start (s1 `0001_start_clean`) to the last item (s4
`0270_item_r83i1_sponges`, frame 19979). Unit list: `docs/final_video/done.json`, `docs/final_video/RENDER_PROGRESS.md`.

## Items and durations

"done at" = timecode in the final video when the item checkpoint was saved; "duration" = video time since the previous
item finished (walking included). Computed from the item checkpoints' StateRec frames and the rendered units
(`docs/item_timeline.json`). All sessions are AI-operated; "controller skill" means a single AI-issued skill call did it.

| # | item | session / checkpoint | done at (video) | duration in video | how |
|---|---|---|---|---|---|
| 1 | slipper (r123i1) | s1 `0063_item_r123i1_slipper` | 0:02:17 | 2:17 | controller skill (go_item) |
| 2 | paper (r195i3) | s1 `0123_item_r195i3_paper` | 0:04:22 | 2:05 | AI teleop + controller skills; ends half under the nudged bin |
| 3 | paper (r195i1) | s1 `0229_item_r195i1_paper` | 0:08:36 | 4:14 | AI teleop + controller skills; ends half under the nudged bin |
| 4 | knit hat (r131i1) | s1 `0468_item_r131i1_knit_hat` | 0:17:10 | 8:35 | controller skill (go_item) |
| 5 | santa hat (r189i1) | s1 `0529_item_r189i1_santa_hat` | 0:19:16 | 2:06 | controller skill (go_item) |
| 6 | jacket (r121i1) | s1 `0662_item_r121i1_jacket` | 0:24:16 | 5:00 | AI teleop + controller skills (drop_in_cloth) |
| 7 | blanket (r117i1) | s1 `1587_item_r117i1_blanket` | 0:40:34 | 16:18 | Fable escalation (AI teleop) |
| 8 | coat pile (r116i1) | s1 `1994_item_r116i1_coat_pile` | 0:51:52 | 11:18 | Fable escalation (AI teleop) |
| 9 | sandal (r124i1) | s1 `2136_item_r124i1_sandal` | 0:57:02 | 5:10 | AI teleop + controller skills |
| 10 | croc (r122i1) | s1 `2253_item_r122i1_croc` | 1:01:06 | 4:04 | AI teleop + controller skills |
| 11 | close dishwasher | s1 `2491_item_close_dishwasher` | 1:06:55 | 5:49 | controller skill (kitchen step_mon) |
| 12 | rag (r68i1) | s1 `2584_item_r68i1_rag` | 1:10:59 | 4:04 | no-AI runner (attempt 0) |
| 13 | flat (r125i2) | s1 `3158_item_r125i2_flat` | 1:19:27 | 8:28 | no-AI runner after an AI fix (exit_hamper_west) |
| 14 | stocking (r190i1) | s2 `0368_item_r190i1_stocking` | 1:24:53 | 5:26 | AI teleop + controller skills |
| 15 | duck (r120i2) | s2 `0497_item_r120i2_duck` | 1:26:34 | 1:42 | AI teleop + controller skills |
| 16 | flat (r125i1) | s3 `0167_item_r125i1_flat` | 1:33:33 | 6:59 | no-AI runner (attempt 2) |
| 17 | cardboard box (r175i1) | s3 `0668_item_r175i1_cardboard_box` | 1:42:56 | 9:22 | AI teleop + controller skills |
| 18 | ball (r178i1) | s3 `0800_item_r178i1_ball` | 1:47:58 | 5:03 | AI teleop + controller skills |
| 19 | toy pouch (r179i1) | s3 `0986_item_r179i1_toy_pouch` | 1:54:25 | 6:27 | AI teleop + controller skills (two-hand) |
| 20 | toy piece (r193i4) | s3 `1251_item_r193i4_toy_piece` | 1:58:47 | 4:22 | AI teleop + controller skills |
| 21 | ball (r192i1) | s3 `1338_item_r192i1_ball` | 2:02:04 | 3:16 | AI teleop + controller skills |
| 22 | toy piece (r193i2) | s3 `1437_item_r193i2_toy_piece` | 2:05:28 | 3:25 | AI teleop + controller skills |
| 23 | toy piece (r193i3) | s3 `1535_item_r193i3_toy_piece` | 2:09:11 | 3:43 | AI teleop + controller skills |
| 24 | toy piece (r193i1) | s3 `1632_item_r193i1_toy_piece` | 2:12:54 | 3:43 | AI teleop + controller skills |
| 25 | duck (r120i1) | s3 `2182_item_r120i1_duck` | 2:18:14 | 5:21 | no-AI runner (attempt 0) |
| 26 | shoe (r105i1) | s3 `2311_item_r105i1_shoe` | 2:23:19 | 5:05 | no-AI runner (attempt 0) |
| 27 | shoe (r105i2) | s3 `2408_item_r105i2_shoe` | 2:26:50 | 3:30 | no-AI runner (attempt 0) |
| 28 | umbrella (r107i1) | s3 `2490_item_r107i1_umbrella` | 2:29:44 | 2:54 | no-AI runner (attempt 0) |
| 29 | TV cabinet door (r159i1) | s3 `2923_item_r159i1_door` | 2:45:52 | 16:08 | no-AI runner (attempt 0) |
| 30 | tissue (r158i1) | s3 `3140_item_r158i1_tissue` | 2:49:33 | 3:41 | AI teleop + controller skills |
| 31 | pouch (r149i1) | s3 `3261_item_r149i1_pouch` | 2:54:43 | 5:10 | AI teleop + controller skills; ends half under the nudged bin |
| 32 | light saber (r130i1) | s3 `3677_item_r130i1_light_saber` | 3:03:02 | 8:20 | AI teleop + controller skills (4.6 cm off its spot) |
| 33 | scooter (r126i1) | s3 `4072_item_r126i1_scooter` | 3:09:48 | 6:46 | Fable escalation (AI teleop) |
| 34 | nugget (r93i1) | s4 `0134_item_r93i1_nugget` | 3:15:35 | 5:46 | AI teleop + controller skills |
| 35 | sponges (r83i1) | s4 `0270_item_r83i1_sponges` | 3:20:54 | 5:20 | AI teleop + controller skills |
| 36 | plastic bag (r196i1) | - | - | - | GIVEN UP after 6 real tries; left lying in place, visible, untidied |

## Folder map

```
README.md                  this file
DRIVE_MANIFEST.md          big files that go to Google Drive (sizes + SHA-256, links TBD)
data/episode/
  s1_1120_181556_dex1_floor_final/     session 1 (items 1-13)
  s2_1121_021343_dex1_floor_final_s2/  session 2 (items 14-15)
  s3_1121_034845_dex1_floor_final_s3/  session 3 (items 16-33)
  s4_1121_123451_dex1_floor_final_s4/  session 4 (items 34-35)
    actions.jsonl          every action + args in order (includes discarded branches: use pieces.json / RELOADS.txt)
    trace.jsonl            controller trace
    pieces.json            session pieces (reload points, saves) used by the render
    segment.json           session start (run, from checkpoint, start frame)
    result_partial.json    item results of the session
    checkpoints/NNNN_*/meta.json       meta of EVERY checkpoint (act, roll, item)
    checkpoints/NNNN_item_*/           FULL state of the item checkpoints: physics.npz, control.pkl, cloth.npz,
                                       cloth_plain.pkl, look.jpg
    states/chunk_*.npz, layout.npz     StateRec 30 Hz full state (replay / render input)
    tele/, grasps/, look_fb/           still frames the AI looked at while operating (JPEG)
    00_start.jpg
docs/
  apartment/               PROGRESS_FINAL.md (read first), PROGRESS.md, PROGRESS_GAIT.md, PROGRESS_CLOTH.md,
                           REMOVED_FOR_40*.json, RUN_DONE*.txt, RUN_NEEDS_AI*.txt, final_runner.log, full_plan/
  final_video/             RENDER_PROGRESS.md, follow.log, done.json, final_join.py, final_join.log, status.json
  item_timeline.json       per-item frames, video timecodes and durations
teleop/live_cmd/           all AI teleop command files (+ outputs) of this episode: final/ (b*, c*, d*, e*, f*, g* = Fable,
                           h*, i*, n1/ = night finisher + RELOADS.txt, n2/, fix1/, fable_sc/ = Fable scooter, runner/ =
                           per-attempt outputs of the no-AI runner), f6-f14, fb, sc, gait3, z_*.py
look/                      final_look_v4/, final_look_v6/ (stills, compare_photo_vs_render.jpg, cmd/), compare_sheets/,
                           corner_cam_cand_12.jpg, room_photos/ (photos of the real apartment)
```

Absolute paths inside the files point to the original machine (`C:\Users\raresense\sim_home\...`, `E:\urc_final\...`).

## Replay / render from the recorded states

The code is in [RareSense/universal-robot-control](https://github.com/RareSense/universal-robot-control), branch
**`final-episode`** (the look is tag `look-final`):

- `src/urc/tasks/home/staterec.py`: StateRec, the 30 Hz full-state recorder and reader (`states/chunk_*.npz`, `layout.npz`).
- `scripts/home/replay/render_lib.py`: loads recorded states into Isaac and renders the room / head cameras with the final look.
- `scripts/home/replay/render_follow.py`: the render worker. It walks the chain pieces of the 4 sessions in order, renders
  each unit, QCs it and joins. Command used:
  `py -3.12 scripts/home/replay/render_follow.py --room-cam-pose -5.35 -2.5 2.45 2.5 0.9 -0.1 --room-focal 9.5`
- `docs/final_video/final_join.py` (this repo): joins the rendered units into the two final videos, ending at s4 frame 19979.
- `scripts/home/final_run/`: the no-AI runner (`runner.py`, `items_lib.py`, `common_a.py`, `common_b.py`, `resume.py`)
  and `night_21nov/` (night finisher command files + RELOADS.txt).
- Room: `rooms/apartment_1122_full.json`. Live session: env `URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp URC_TEXTURED=1
  URC_ROUGH_FLOOR=0.8`, then `py -3.12 scripts/home/live/newlive.py <TAG> rooms/apartment_1122_full.json`.
- To resume the simulation from any item, load that item checkpoint folder (`physics.npz` + `control.pkl` + `cloth.npz`)
  with `scripts/home/final_run/resume.py`.

Point the scripts at the session folders of this repo (`data/episode/sN_*`) instead of `C:\Users\raresense\sim_home\runs\`.

## Dataset plan (next step)

1. Cut the episode into **36 per-task episodes** (one per item: from the previous item checkpoint to this item's
   checkpoint, kept pieces only), using the StateRec frames and `docs/item_timeline.json`.
2. Re-render per-task camera streams from the states (room + head, plus wrist views if wanted).
3. **LeRobot export**: joint positions / velocities, gripper states and actions at 30 Hz plus video per episode, with the
   task text and a success flag (the plastic bag episode marked as given up).
