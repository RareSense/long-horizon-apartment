# Long-horizon apartment clean-up (Unitree G1 + Dex1, Isaac Sim 6.2)

A Unitree **G1 humanoid with Dex1 parallel grippers** tidies a digital twin of a real apartment ("Apartment 1122", built
from photos of the real rooms, see `look/room_photos/`) in **Isaac Sim 6.2**, as **one continuous recorded episode** of
3 h 21 min: it walks to each item, picks it up (floor, table, couch, mat), carries it and puts it where it belongs
(laundry hamper, toy basket, rubbish bin, shoe mat, ...), and closes the dishwasher and a TV cabinet door.

The robot is operated by our own controller,
[RareSense/universal-robot-control](https://github.com/RareSense/universal-robot-control) (branch `final-episode`):
whole-body walking and balance, navigation, floor / table / couch picks, two-hand grasps, cloth handling, placing,
door and appliance skills.

## Result

- **35 of 36 items done.**
- **Plastic bag (r196i1): not done.** It is left lying where it was, visible, for the whole video.
- **Rubbish bin nudged** about 7 cm and tilted 4.9 deg by the robot's knee; the two papers (r195i3, r195i1) and the pouch
  (r149i1) end up half under the bin's walls instead of fully inside. The tissue is inside.
- The light saber (r130i1) ends 4.6 cm from its target spot, across the toy basket rim.
- 26 further loose objects of the scanned apartment are not part of this episode; they are removed from the scene at
  frame 0 (list: `docs/apartment/REMOVED_FOR_40.json`).

## Final video

Two synchronised cameras, rendered from the recorded simulation states with the locked realistic look (RTX real-time
ray tracing, DLSS Quality, ACES; tag `look-final` in universal-robot-control).

| camera | resolution | fps | duration | Google Drive |
|---|---|---|---|---|
| room corner camera | 1920x1080 | 30 | 3 h 20 min 54 s | [part 1 of 2](https://drive.google.com/file/d/1EBXDVmoUhFdLWNyr54e4mT9gMKKMMK7R/view), [part 2 of 2](https://drive.google.com/file/d/1sQrCcHpzqHaZt7YAGqal-5rK5lvcPe4y/view) |
| robot head camera | 1440x1080 | 30 | 3 h 20 min 54 s | [part 1 of 4](https://drive.google.com/file/d/13r651ioZo28dDf4SycPmwA19uLb2rLzz/view), [part 2 of 4](https://drive.google.com/file/d/1U8rbFS2FA1yIJWU8yJrVYzm_rZRry5c8/view), [part 3 of 4](https://drive.google.com/file/d/15Eo8KM0BwjLvZvsMVeNzOYGm2sqNLEik/view), [part 4 of 4](https://drive.google.com/file/d/1dXz88I206VM-XNbAJvHpnxwgSTtX8nc7/view) |

H.264, CRF 20. The parts are lossless cuts of one file each; sizes and SHA-256 of the full files and every part are in
`DRIVE_MANIFEST.md`. One 60 s stretch during the coat pile (session 1 frames 112790-114589) is missing from both videos
and is being re-rendered.

## Items

"done at" = timecode in the final video; "duration" = video time since the previous item (walking included).

| # | item | done at | duration | note |
|---|---|---|---|---|
| 1 | slipper (r123i1) | 0:02:17 | 2:17 | |
| 2 | paper (r195i3) | 0:04:22 | 2:05 | ends half under the nudged bin |
| 3 | paper (r195i1) | 0:08:36 | 4:14 | ends half under the nudged bin |
| 4 | knit hat (r131i1) | 0:17:10 | 8:35 | |
| 5 | santa hat (r189i1) | 0:19:16 | 2:06 | |
| 6 | jacket (r121i1) | 0:24:16 | 5:00 | |
| 7 | blanket (r117i1) | 0:40:34 | 16:18 | |
| 8 | coat pile (r116i1) | 0:51:52 | 11:18 | |
| 9 | sandal (r124i1) | 0:57:02 | 5:10 | |
| 10 | croc (r122i1) | 1:01:06 | 4:04 | |
| 11 | close dishwasher | 1:06:55 | 5:49 | |
| 12 | rag (r68i1) | 1:10:59 | 4:04 | |
| 13 | flat (r125i2) | 1:19:27 | 8:28 | |
| 14 | stocking (r190i1) | 1:24:53 | 5:26 | |
| 15 | duck (r120i2) | 1:26:34 | 1:42 | |
| 16 | flat (r125i1) | 1:33:33 | 6:59 | |
| 17 | cardboard box (r175i1) | 1:42:56 | 9:22 | |
| 18 | ball (r178i1) | 1:47:58 | 5:03 | |
| 19 | toy pouch (r179i1) | 1:54:25 | 6:27 | |
| 20 | toy piece (r193i4) | 1:58:47 | 4:22 | |
| 21 | ball (r192i1) | 2:02:04 | 3:16 | |
| 22 | toy piece (r193i2) | 2:05:28 | 3:25 | |
| 23 | toy piece (r193i3) | 2:09:11 | 3:43 | |
| 24 | toy piece (r193i1) | 2:12:54 | 3:43 | |
| 25 | duck (r120i1) | 2:18:14 | 5:21 | |
| 26 | shoe (r105i1) | 2:23:19 | 5:05 | |
| 27 | shoe (r105i2) | 2:26:50 | 3:30 | |
| 28 | umbrella (r107i1) | 2:29:44 | 2:54 | |
| 29 | TV cabinet door (r159i1) | 2:45:52 | 16:08 | |
| 30 | tissue (r158i1) | 2:49:33 | 3:41 | |
| 31 | pouch (r149i1) | 2:54:43 | 5:10 | ends half under the nudged bin |
| 32 | light saber (r130i1) | 3:03:02 | 8:20 | 4.6 cm off its spot |
| 33 | scooter (r126i1) | 3:09:48 | 6:46 | |
| 34 | nugget (r93i1) | 3:15:35 | 5:46 | |
| 35 | sponges (r83i1) | 3:20:54 | 5:20 | |
| 36 | plastic bag (r196i1) | - | - | not done, left in place |

Per-item frames and checkpoints: `docs/item_timeline.json`.

## Folder map

```
README.md              this file
DRIVE_MANIFEST.md      files on Google Drive (sizes, SHA-256, links)
data/episode/sN_*/     the recorded episode, 4 sessions (s1 items 1-13, s2 14-15, s3 16-33, s4 34-35)
  actions.jsonl        every controller command with its arguments
  trace.jsonl          controller trace
  pieces.json          the kept timeline of the session (use it to follow actions.jsonl in order)
  segment.json, result_partial.json
  checkpoints/         meta.json of every saved state; full state (physics.npz, control.pkl, cloth.npz) of every item
  states/              30 Hz full simulation state (chunk_*.npz + layout.npz)
teleop/                command files sent to the controller during the episode
docs/                  notes, item plan, render notes (docs/final_video/), item_timeline.json
look/                  look stills, photo-vs-render comparisons, room photos
```

Absolute paths inside the files point to the original machine.

## Replay / render

Code: [RareSense/universal-robot-control](https://github.com/RareSense/universal-robot-control), branch
`final-episode`.

- `src/urc/tasks/home/staterec.py`: reader for the 30 Hz states.
- `scripts/home/replay/render_lib.py`, `render_follow.py`: load the recorded states into Isaac and render the room / head
  cameras with the final look
  (`py -3.12 scripts/home/replay/render_follow.py --room-cam-pose -5.35 -2.5 2.45 2.5 0.9 -0.1 --room-focal 9.5`).
- `scripts/home/final_run/resume.py`: resume the simulation from any item checkpoint.
- Room: `rooms/apartment_1122_full.json`.

Point the scripts at `data/episode/sN_*` of this repo.

## Training data

`dataset/apartment_g1_dex1_tidy/` is the episode as training data in **LeRobot v2.1** format: **35 episodes**, one per
done item (the plastic bag has none), **361935 frames at 30 fps (3.35 h)**, each episode with one task string, e.g.
"pick up the slipper and set it on the floor beside the doormat, next to its partner" (destinations from the item plan,
`docs/apartment/full_plan/full_plan_v3.json`).

- `observation.state` (40): floating-base pose of the pelvis (position + quaternion) and the 33 joint positions (legs,
  waist, arms, Dex1 fingers), from the 30 Hz recorded states.
- `action` (33): the next frame's joint positions (the recording has no per-frame joint targets).
- Videos per episode: robot head camera 640x480 and room corner camera 854x480, cut frame-exact from the final videos;
  each has exactly as many frames as its parquet file has rows.
- Episode *k* runs from the end of item *k-1* to item *k*'s checkpoint. Concatenated in order, the 35 episodes are the
  full continuous episode, with two differences from the final videos: the 60 s missing from them during the coat pile
  is rendered and included (episode 7), and final-video 1:26:34.5-1:27:24.4, after which the video jumps back to an
  earlier state, is left out (episode 15).
- Alignment checked on the rendered frames (caption time = recorded time, pelvis position, item checkpoint stills):
  0 frames offset. Validated with pyarrow / ffprobe and loaded with `LeRobotDataset` (lerobot 0.4.4, after its own
  v2.1 to v3.0 conversion).
- Details and the per-episode table: `dataset/apartment_g1_dex1_tidy/README.md`. The whole folder as one zip on Google
  Drive: see `DRIVE_MANIFEST.md`.
