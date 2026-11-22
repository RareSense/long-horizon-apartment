# apartment_g1_dex1_tidy_v2 (LeRobot v2.1)

A Unitree **G1 humanoid with Dex1 parallel grippers** tidies a digital twin of a real apartment ("Apartment 1122") in
simulation (Isaac Sim 6.2). The robot is operated by our own controller,
[universal-robot-control](https://github.com/RareSense/universal-robot-control). The data is **one continuous recorded
episode**, cut into **35 per-item episodes**: walk to the item, pick it up, carry it and put it where it belongs
(laundry hamper, toy basket, rubbish bin, doormat, ...), plus close the dishwasher and a TV cabinet door. The videos are
renders of the recorded simulation states.

| | |
|---|---|
| episodes | 35 (one per done item; item 36, the plastic bag, was not done and has no episode) |
| frames | 361935 at 30 fps = 3.35 h (201.1 min) |
| tasks | 27 distinct task strings (`meta/tasks.jsonl`), one per episode |
| cameras | `observation.images.head` 640x480 (robot head camera), `observation.images.room` 854x480 (fixed corner camera) |
| robot | Unitree G1 29-DoF + 2 Dex1 grippers (2 prismatic finger joints each), floating base |
| format | LeRobot v2.1: `data/chunk-000/episode_*.parquet`, `videos/chunk-000/<camera>/episode_*.mp4`, `meta/` |
| size | 1.72 GB |

## What an episode is

Episode *k* (episode_index *k-1*; item *k* of the repo README's item table) runs from the end of item *k-1* (the start of
the run for item 1) to item *k*'s checkpoint (`docs/item_timeline.json`), so it includes the walk to the item. The
episodes tile the recorded run: **concatenating episodes 0..34 in order gives the full continuous episode**,
the content of the two 1080p final videos in `final_video_v2/` on Google Drive (`DRIVE_MANIFEST.md`), frame for frame.

## Features

- `observation.state` (float32, 40): the **floating-base pose** of the pelvis
  (`base_x, base_y, base_z` in world metres; `base_qw, base_qx, base_qy, base_qz`, quaternion w-x-y-z), then the
  **33 joint positions**: 12 leg, 3 waist and 2 x 7 arm joints (rad), and the 4 Dex1 finger joints (prismatic, metres;
  0.04 = open). Names in `meta/info.json`.
- `action` (float32, 33): **the next frame's joint positions** (same 33 joints, same order). The recording has no
  per-frame commanded joint targets (`actions.jsonl` holds the controller skill calls with their arguments, `trace.jsonl`
  a 10 Hz controller trace of base pose, mode and hand targets), so the action is the joint state 1/30 s later. It
  follows the dataset order across episode boundaries (the episodes are continuous); the very last frame repeats its own
  state.
- `timestamp`, `frame_index`, `episode_index`, `index`, `task_index`, `next.done` (True on the last frame of each episode).
- Provenance (int64): `source.session` (recording session 1-4), `source.rec_frame` (recorded frame number in that
  session's `data/episode/<session>/states`), `source.final_video_frame` (frame of the 1080p final videos; -1 for the
  60 s rendered separately).
- Videos: cut frame-exact from the 1080p final videos and re-encoded: head 1440x1080 -> 640x480, room 1920x1080 ->
  854x480; H.264 yuv420p, 30 fps, CRF 23, GOP 60 (2 s). Each video has exactly as many frames as its parquet file has
  rows.

## Alignment check (by eye)

Which recorded frame each video frame shows comes from `docs/final_video/done.json` (render units in order). It was
checked on the rendered frames for episodes 0, 7, 15, 19, 28 and 34 (first and last frame of each, the jump in the final
video inside episode 15, and both joins of the separately rendered 60 s):
(a) the simulation time in the burned-in caption equals the recorded time of the row (31.04 s / 31.036 s at frame 0,
3203.20 / 3203.198 at the end of episode 7, 2824.98 -> 2825.02 -> 2884.98 -> 2885.02 s across the inserted 60 s,
12094.97 / 12094.966 at the very end); (b) the recorded pelvis position projected into the fixed corner camera lands on
the robot's pelvis; (c) the last head-camera frame of each episode matches that item checkpoint's `look.jpg`, and the arm
pose matches the joint state (e.g. left arm raised in front of the head camera at the end of episode 19, right arm
raised holding the coat in episode 7). **Offset found: 0 frames.** The state is continuous from frame to frame in every episode,
also across render units and sessions (largest per-frame base step 2.1 cm).

## Validation

- **pyarrow + ffprobe (all 35 episodes):** parquet rows = frames of both episode videos (exact), `frame_index` 0..n-1,
  `timestamp` = frame_index / 30, `index` contiguous over the dataset (0..361934), `next.done` only on the last frame,
  columns = `meta/info.json` features, state 40 / action 33 values, all finite; videos H.264 yuv420p 30/1 at 640x480 /
  854x480; per-episode stats of every feature in `meta/episodes_stats.jsonl` (image stats per channel in [0, 1] from
  every 10th frame), aggregate in `meta/stats.json`. Problems found: none.
- **lerobot library:** a copy was converted with lerobot 0.4.4's own `convert_dataset_v21_to_v30` and opened with
  `LeRobotDataset`: 35 episodes, 361935 frames, 30 fps, all 13 features; items 0, 180967 and 361934 read with decoded
  video frames (head 3x480x640, room 3x480x854), the right task strings and timestamps.

## Outcome notes

- **Plastic bag (r196i1): not done**, no episode; it stays lying in place, visible, in every episode.
- **Rubbish bin nudged** about 7 cm and tilted 4.9 deg by knee contacts at the bin; the two papers (episodes 1, 2) and
  the pouch (episode 30) end half under its walls; the tissue (episode 29) is inside.
- **Light saber** ends 4.6 cm from its target spot, lying diagonally across the toy basket rim (episode 31).
- The cardboard box ends 1.5 cm from its spot, upright against the wall (episode 16).
- `success` in `meta/episodes.jsonl` is True for all 35 (each ends at a saved item checkpoint that passed the item check);
  see the notes above for the partial outcomes.
- The record has some small object "pops" (a free body moving > 5 cm between two frames, e.g. at grasps); they are in
  the data as recorded and listed per render unit in `docs/final_video/RENDER_PROGRESS.md`.
- 26 loose objects of the scanned apartment were removed from the scene at frame 0 (`docs/apartment/REMOVED_FOR_40.json`).

## Loading

LeRobot v2.1 (`lerobot` up to 0.3.x): `LeRobotDataset("apartment_g1_dex1_tidy", root="<path>/apartment_g1_dex1_tidy")`.
Newer `lerobot` (dataset format v3.0): convert a copy first with
`python -m lerobot.datasets.v30.convert_dataset_v21_to_v30 --repo-id=apartment_g1_dex1_tidy --root=<parent folder> --push-to-hub=false`.

## Per-episode summary

Start / end = the span in the 1080p final videos the episode was cut from.

| ep | item | task | start | end | frames | notes |
|---|---|---|---|---|---|---|
| 0 | r123i1_slipper | pick up the slipper and set it on the floor beside the doormat, next to its partner | 0:00:00 | 0:02:17 | 4109 (2.3 min) |  |
| 1 | r195i3_paper | pick up the crumpled paper and drop it into the rubbish bin | 0:02:17 | 0:04:22 | 3750 (2.1 min) | ends half under the bin's walls (bin nudged ~7 cm by knee contacts) |
| 2 | r195i1_paper | pick up the crumpled paper and drop it into the rubbish bin | 0:04:22 | 0:08:36 | 7616 (4.2 min) | ends half under the bin's walls (bin nudged ~7 cm by knee contacts) |
| 3 | r131i1_knit_hat | pick up the knit hat and drop it into the laundry hamper | 0:08:36 | 0:17:10 | 15436 (8.6 min) |  |
| 4 | r189i1_santa_hat | pick up the santa hat and drop it into the laundry hamper | 0:17:10 | 0:19:16 | 3777 (2.1 min) |  |
| 5 | r121i1_jacket | pick up the jacket and drop it into the laundry hamper | 0:19:16 | 0:24:16 | 8991 (5.0 min) |  |
| 6 | r117i1_blanket | pick up the blanket and drop it into the laundry hamper | 0:24:16 | 0:40:34 | 29344 (16.3 min) |  |
| 7 | r116i1_coat_pile | pick up the coat pile and drop it into the laundry hamper | 0:40:34 | 0:51:52 | 22147 (12.3 min) | complete: includes 60 s (session 1 frames 112790-114589) that are missing from the 1080p final videos, rendered separately with the same render set-up |
| 8 | r124i1_sandal | pick up the sandal and put it on the doormat beside its partner | 0:51:52 | 0:57:02 | 9285 (5.2 min) |  |
| 9 | r122i1_croc | pick up the croc and set it on the floor beside the doormat, next to its partner | 0:57:02 | 1:01:06 | 7323 (4.1 min) |  |
| 10 | close_dishwasher | push the dishwasher racks in and close the dishwasher door | 1:01:06 | 1:06:55 | 10461 (5.8 min) |  |
| 11 | r68i1_rag | pick up the rag and drop it into the laundry hamper | 1:06:55 | 1:10:59 | 7332 (4.1 min) |  |
| 12 | r125i2_flat | pick up the flat shoe and put it on the doormat beside its pair, toes to the wall | 1:10:59 | 1:19:27 | 15247 (8.5 min) |  |
| 13 | r190i1_stocking | pick up the stocking and put it in the toy basket | 1:19:27 | 1:24:53 | 9768 (5.4 min) |  |
| 14 | r120i2_duck | pick up the toy duck and put it in the toy basket | 1:24:53 | 1:26:34 | 3048 (1.7 min) |  |
| 15 | r125i1_flat | pick up the flat shoe and put it on the doormat beside its pair, toes to the wall | 1:26:34 | 1:33:33 | 11071 (6.2 min) | final-video frames 155834-157330 (1:26:34.5-1:27:24.4) are not included: after them the final videos jump back to the state at 1:26:34.5; this episode starts from that state, so state and video are continuous |
| 16 | r175i1_cardboard_box | push the cardboard box square against the wall by the two-tier table | 1:33:33 | 1:42:56 | 16871 (9.4 min) | ends 1.5 cm from its spot, upright against the wall |
| 17 | r178i1_ball | pick up the ball and put it in the toy basket | 1:42:56 | 1:47:58 | 9081 (5.0 min) |  |
| 18 | r179i1_toy_pouch | pick up the toy pouch and put it in the toy basket | 1:47:58 | 1:54:25 | 11601 (6.4 min) |  |
| 19 | r193i4_toy_piece | pick up the toy piece and put it in the toy basket | 1:54:25 | 1:58:47 | 7863 (4.4 min) |  |
| 20 | r192i1_ball | pick up the ball and put it in the toy basket | 1:58:47 | 2:02:04 | 5895 (3.3 min) |  |
| 21 | r193i2_toy_piece | pick up the toy piece and put it in the toy basket | 2:02:04 | 2:05:28 | 6141 (3.4 min) |  |
| 22 | r193i3_toy_piece | pick up the toy piece and put it in the toy basket | 2:05:28 | 2:09:11 | 6678 (3.7 min) |  |
| 23 | r193i1_toy_piece | pick up the toy piece and put it in the toy basket | 2:09:11 | 2:12:54 | 6683 (3.7 min) |  |
| 24 | r120i1_duck | pick up the toy duck and put it in the toy basket | 2:12:54 | 2:18:14 | 9620 (5.3 min) |  |
| 25 | r105i1_shoe | pick up the shoe and put it on the doormat beside its pair, toes to the wall | 2:18:14 | 2:23:19 | 9145 (5.1 min) |  |
| 26 | r105i2_shoe | pick up the shoe and put it on the doormat beside its pair, toes to the wall | 2:23:19 | 2:26:50 | 6313 (3.5 min) |  |
| 27 | r107i1_umbrella | pick up the umbrella and lay it on the floor by the entry, along the wall | 2:26:50 | 2:29:44 | 5215 (2.9 min) |  |
| 28 | r159i1_door | close the TV cabinet door | 2:29:44 | 2:45:52 | 29040 (16.1 min) |  |
| 29 | r158i1_tissue | pick up the tissue and drop it into the rubbish bin | 2:45:52 | 2:49:33 | 6635 (3.7 min) | knee contacts nudged the bin (~7 cm, 4.9 deg tilt over the bin drops) |
| 30 | r149i1_pouch | pick up the empty pouch and drop it into the rubbish bin | 2:49:33 | 2:54:43 | 9296 (5.2 min) | ends half under the nudged bin's walls |
| 31 | r130i1_light_saber | pick up the light saber and put it on the floor beside the toy basket | 2:54:43 | 3:03:02 | 14995 (8.3 min) | ends 4.6 cm from its target spot, lying diagonally across the toy basket rim |
| 32 | r126i1_scooter | move the scooter to the vehicle corner and park it upright, nose to the hall wall | 3:03:02 | 3:09:48 | 12179 (6.8 min) |  |
| 33 | r93i1_nugget | pick up the toy nugget and put it in the toy basket | 3:09:48 | 3:15:35 | 10394 (5.8 min) |  |
| 34 | r83i1_sponges | pick up the sponges from the food island and put them on the tray table | 3:15:35 | 3:20:54 | 9585 (5.3 min) |  |

## Videos of this version

The videos were rendered again from the recorded states without any text overlay, for exactly this frame list, then cut and re-encoded as described above. Each episode video was checked: frame count = parquet rows, and whole-frame PSNR against the earlier cut of the same frames >= 25 dB (same content, aligned).
