# Drive manifest

Big files of this episode that are **not** in the git repo (GitHub limit 100 MB per file, repo kept small). Upload target:
Google Drive folder **`long-horizon-apartment`**. Links: **TBD (upload when the Google Drive app is running)**.

Verify a download with `sha256sum <file>` (Linux / Git Bash) or `certutil -hashfile <file> SHA256` (Windows).

## 1. Final video (main deliverable)

| file | source path (original machine) | bytes | SHA-256 | Drive link |
|---|---|---|---|---|
| `episode_room_1080p.mp4` | `D:\apartment_final_video\episode_room_1080p.mp4` | 11294444175 (11.29 GB) | `9aefeb730c39b9e69ed8a8a5145cee281b13879c5227eccc087bb905517ecb45` | TBD (upload when Google Drive app is running) |
| `episode_head_1080p.mp4` | `D:\apartment_final_video\episode_head_1080p.mp4` | 13040056111 (13.04 GB) | `dff1135f6a6569045b4e1fa799e0b5a6f63253421215d8e259037d67e773d58c` | TBD (upload when Google Drive app is running) |

Room corner camera 1920x1080, robot head camera 1440x1080, both 30 fps, H.264 CRF 20, 12054.4 s (3 h 20 min 54 s).
Upload each as one file (Drive allows up to 5 TB per file); if the upload is split, keep the SHA-256 above for the joined file.

## 2. Working preview videos (live session previews, low resolution)

Recorded live by each session (room 960x540, head 640x480); they include discarded branches. **Drive folder:**
`long-horizon-apartment/working_previews/<session>/`.

| file | source path | bytes | SHA-256 | note | Drive link |
|---|---|---|---|---|---|
| s1 `room.mp4` | `C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\room.mp4` | 186646576 | `ac241ea908834a349297dac7db74413ae9ae3fcda0d7b2369dc40e8e03f1ef3d` | not finalised (session killed: no moov atom; needs `untrunc` / recovery to play) | TBD |
| s1 `head.mp4` | `C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\head.mp4` | 643039280 | `fe3d55dfed54344a336271337a88d7ee9786c586e496369b823b174ea9c5c7ba` | not finalised (no moov atom) | TBD |
| s2 `room.mp4` | `C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\room.mp4` | 37486640 | `882080a3f813fbee62dfc48374d85604fa42b97d70fff1fbc8b3947f269ff9a9` | not finalised (no moov atom) | TBD |
| s2 `head.mp4` | `C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\head.mp4` | 184549424 | `53688827107efbc0aaa3c0fc6a6ad044c78c04b6690fb9dd21f54fa5fd8e1dcc` | not finalised (no moov atom) | TBD |
| s3 `room.mp4` | `C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3\room.mp4` | 211183716 | `7ab2d374d3964498578a5e510036cdf4443fc7ea101bad1acbd099b33cec6e17` | 8914.5 s, playable | TBD |
| s3 `head.mp4` | `C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3\head.mp4` | 906342032 | `99bf16d4a8eb63939b1b72e5d266895bb49cf1421ce225773b875c54c4e6c544` | 8914.5 s, playable | TBD |
| s4 `room.mp4` | `C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\room.mp4` | 27395733 | `6eb0b8bff3a8a6d042b2e101ee112f18a212be966e1c824a806947e2b4c38a30` | 1291.5 s, playable (includes the bin-fix attempts after frame 19979) | TBD |
| s4 `head.mp4` | `C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\head.mp4` | 96872484 | `2e9fd169f6e46c278999abb5f1bc71afbcae9519bb12e89cbbc454b5ce5441b1` | 1291.5 s, playable | TBD |

## 3. Working frames (JPEG stills, every 300th frame at the end)

Only these still exist (the s1, s2 and early s3 frame folders listed in PROGRESS_FINAL.md are now empty / gone).
Zip each folder before upload and record the zip's SHA-256 here.

| folder | files | bytes | zip SHA-256 | Drive link |
|---|---|---|---|---|
| `D:\sim_runs_overflow\1121_034845_dex1_floor_final_s3\frames` | 612 | 48818478 | TBD (compute on zip) | TBD |
| `C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\frames` | 260 | 18946057 | TBD (compute on zip) | TBD |

## 4. Optional: full state of the non-item checkpoints

The repo holds the full state of every **item** checkpoint and the `meta.json` of every checkpoint. The full state
(`physics.npz`, `control.pkl`, `cloth.npz`, `cloth_plain.pkl`, `look.jpg`) of the act / roll checkpoints between items is
not in git; it is only needed to resume from a point between two items (the StateRec `states/` already hold the full
30 Hz state for replay). Zip per session if wanted:

| session folder `...\checkpoints\` (non-item dirs, without meta.json) | files | bytes | zip SHA-256 | Drive link |
|---|---|---|---|---|
| `C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\checkpoints` | 5677 | 1078717114 | TBD | TBD |
| `C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\checkpoints` | 1081 | 264771962 | TBD | TBD |
| `C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3\checkpoints` | 4905 | 693807296 | TBD | TBD |
| `C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\checkpoints` | 1128 | 625125597 | TBD | TBD |

## Not planned for Drive

- `C:\Users\raresense\sim_home\final_video\room_so_far.mp4` (11748775019 bytes) and `head_so_far.mp4` (13531368493 bytes):
  intermediate joins of the render worker, superseded by section 1 (they also contain units after the episode end).
- No data file of this repo is over 95 MB: everything requested for `data/episode/` (states, item checkpoints, meta,
  actions, traces) fits in git.
