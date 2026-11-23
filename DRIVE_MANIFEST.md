# Drive manifest

Big files of this episode that are **not** in the git repo (GitHub limit 100 MB per file, repo kept small). Upload target:
Google Drive folder **`long-horizon-apartment`**. Sections 2-4 uploaded 22 Nov 2026 (links below, uploads confirmed by Drive id and size). Section 1 (final videos) uploaded 22 Nov 2026 as parts (below).

Verify a download with `sha256sum <file>` (Linux / Git Bash) or `certutil -hashfile <file> SHA256` (Windows).

<!-- v2 files start -->
## Current files (v2, no overlay; updated 23 Nov 2026 07:28)

| file | bytes | SHA-256 | Drive link |
|---|---|---|---|
| `episode_room_1080p_v2_part1of4.mp4` | 2809226265 | `881cd7f5aa31cdaacfdc55dcaf3067d58d5b8bfdfbde1db1cdf72b6f22c47248` | [link](https://drive.google.com/file/d/1plEtH194VjeqJfqkAdrEDDXmAEYQWpNQ/view) |
| `episode_head_1080p_v2_part1of4.mp4` | 3202636685 | `d81c1ee7aea9b41479e72eba0f7fd10ac6e0da00f2b2f0f488e4e57db48fb87f` | [link](https://drive.google.com/file/d/1_sxQIiM-OfuxxtoRO5wsslAgUHf83bul/view) |
| `episode_room_1080p_v2_part2of4.mp4` | 2848334243 | `43ab82f661fef9e0234f541c947f942b9fc84d4f519543789d9f64e19dc9b8cd` | [link](https://drive.google.com/file/d/1ev2voazo7AqOkXxLX9y4QHIKaKcoChFa/view) |
| `episode_head_1080p_v2_part2of4.mp4` | 3169154799 | `f987b229c24c94294bce6dd8146da1c82c1e5d384b4aef65b864c751932ccbe4` | [link](https://drive.google.com/file/d/1ejBx8z_aSrh_P1B5ntfDy-RwypKxTtl2/view) |

<!-- v2 files end -->

## 1. Final video (main deliverable)

| file | source path (original machine) | bytes | SHA-256 | Drive link |
|---|---|---|---|---|
| `episode_room_1080p.mp4` | `D:\apartment_final_video\episode_room_1080p.mp4` | 11294444175 (11.29 GB) | `9aefeb730c39b9e69ed8a8a5145cee281b13879c5227eccc087bb905517ecb45` | TBD (upload when Google Drive app is running) |
| `episode_head_1080p.mp4` | `D:\apartment_final_video\episode_head_1080p.mp4` | 13040056111 (13.04 GB) | `dff1135f6a6569045b4e1fa799e0b5a6f63253421215d8e259037d67e773d58c` | TBD (upload when Google Drive app is running) |

Room corner camera 1920x1080, robot head camera 1440x1080, both 30 fps, H.264 CRF 20, 12054.4 s (3 h 20 min 54 s).
Upload each as one file (Drive allows up to 5 TB per file); if the upload is split, keep the SHA-256 above for the joined file.

### Uploaded parts (lossless cuts of the files above, play one after another)

| part | bytes | SHA-256 | Drive link |
|---|---|---|---|
| `episode_room_1080p_part1of2.mp4` | 5622974861 | `7fa6923e58b8a0bd2137df88d6419838c1af500451a82060bb3daf09a27c7abc` | [link](https://drive.google.com/file/d/1EBXDVmoUhFdLWNyr54e4mT9gMKKMMK7R/view) |
| `episode_room_1080p_part2of2.mp4` | 5671470173 | `4540f89740d87ebecf0a28ec4653056895a429f6928c04909e7f81fa4042dbc9` | [link](https://drive.google.com/file/d/1sQrCcHpzqHaZt7YAGqal-5rK5lvcPe4y/view) |
| `episode_head_1080p_part1of4.mp4` | 3178492036 | `1e1b6db69c0134cf9ab332edb0321fc16e1525aec3b9362bc80db2fc4945cdb2` | [link](https://drive.google.com/file/d/13r651ioZo28dDf4SycPmwA19uLb2rLzz/view) |
| `episode_head_1080p_part2of4.mp4` | 3113684315 | `715c9556e7d82aa51a1022f9ad227c104d4db3143624e7a2c3cd6f9a5cf1a6b5` | [link](https://drive.google.com/file/d/1U8rbFS2FA1yIJWU8yJrVYzm_rZRry5c8/view) |
| `episode_head_1080p_part3of4.mp4` | 3456571851 | `a351fe6f1f19ae40ba3eafa99ff490f75cb71823244445d89807586de774e65f` | [link](https://drive.google.com/file/d/15Eo8KM0BwjLvZvsMVeNzOYGm2sqNLEik/view) |
| `episode_head_1080p_part4of4.mp4` | 3292626098 | `34d305791e99883e0de1dbe0afb7adfa91259c27d73757fc23b5ef6dd37789ca` | [link](https://drive.google.com/file/d/1dXz88I206VM-XNbAJvHpnxwgSTtX8nc7/view) |

Drive folder: `long-horizon-apartment/final_video/`. Room: 2 parts cut by the ffmpeg segment muxer at 6027 s. Head: 4 parts cut at keyframes (3017.43 s, 6026.07 s, 9041.93 s); each head cut repeats 2-3 frames (<0.1 s) at the start of the next part.


## 2. Working preview videos (live session previews, low resolution)

Recorded live by each session (room 960x540, head 640x480). **Drive folder:**
`long-horizon-apartment/working_previews/<session>/`.

| file | source path | bytes | SHA-256 | note | Drive link |
|---|---|---|---|---|---|
| s1 `room.mp4` | `C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\room.mp4` | 186646576 | `ac241ea908834a349297dac7db74413ae9ae3fcda0d7b2369dc40e8e03f1ef3d` | not finalised (session killed: no moov atom; needs `untrunc` / recovery to play) | [s1_room.mp4](https://drive.google.com/file/d/15CPuQZjw3ktS4leQ_Q0Jv30t5T_8P7P0/view) |
| s1 `head.mp4` | `C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\head.mp4` | 643039280 | `fe3d55dfed54344a336271337a88d7ee9786c586e496369b823b174ea9c5c7ba` | not finalised (no moov atom) | [s1_head.mp4](https://drive.google.com/file/d/130N_B7sZ9JqtS0zKnQKmSC35Q_RTGqp_/view) |
| s2 `room.mp4` | `C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\room.mp4` | 37486640 | `882080a3f813fbee62dfc48374d85604fa42b97d70fff1fbc8b3947f269ff9a9` | not finalised (no moov atom) | [s2_room.mp4](https://drive.google.com/file/d/1FHM7YkIBiGFUiKlgk3z2ihvM5qCcI1tJ/view) |
| s2 `head.mp4` | `C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\head.mp4` | 184549424 | `53688827107efbc0aaa3c0fc6a6ad044c78c04b6690fb9dd21f54fa5fd8e1dcc` | not finalised (no moov atom) | [s2_head.mp4](https://drive.google.com/file/d/1eegvfXgFpJcsnSD0J7UyRKibL9iOTwTN/view) |
| s3 `room.mp4` | `C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3\room.mp4` | 211183716 | `7ab2d374d3964498578a5e510036cdf4443fc7ea101bad1acbd099b33cec6e17` | 8914.5 s, playable | [s3_room.mp4](https://drive.google.com/file/d/1HgdQNPsK03t5hMgb-Ad65r6qea8Qt37R/view) |
| s3 `head.mp4` | `C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3\head.mp4` | 906342032 | `99bf16d4a8eb63939b1b72e5d266895bb49cf1421ce225773b875c54c4e6c544` | 8914.5 s, playable | [s3_head.mp4](https://drive.google.com/file/d/1caoSHFvdFOUwio_ynGG7ccp6N50p03ES/view) |
| s4 `room.mp4` | `C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\room.mp4` | 27395733 | `6eb0b8bff3a8a6d042b2e101ee112f18a212be966e1c824a806947e2b4c38a30` | 1291.5 s, playable (includes the bin-fix attempts after frame 19979) | [s4_room.mp4](https://drive.google.com/file/d/1iW5iRGwkUNWubfq53JVij-7N0lx3vNB6/view) |
| s4 `head.mp4` | `C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\head.mp4` | 96872484 | `2e9fd169f6e46c278999abb5f1bc71afbcae9519bb12e89cbbc454b5ce5441b1` | 1291.5 s, playable | [s4_head.mp4](https://drive.google.com/file/d/1cO2MEMTeBtWlEJ-RP5ATv6N1rNCgFgud/view) |

## 3. Working frames (JPEG stills, every 300th frame at the end)

Only the late s3 and the s4 frame folders exist.
Zip each folder before upload and record the zip's SHA-256 here.

| folder | files | bytes | zip SHA-256 | Drive link |
|---|---|---|---|---|
| `D:\sim_runs_overflow\1121_034845_dex1_floor_final_s3\frames` | 612 | 48818478 | `de12a0f5f8c2b540ee8c034a18fce5d541a00ea7003aa541030a7ce5292361de` | [s3_frames.zip](https://drive.google.com/file/d/1_PUKCWSnsEa0gcykz6lbYclxVIVc1Hkh/view) |
| `C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\frames` | 260 | 18946057 | `20f2f441f0cc74c9cbc33d13dd3c54bd7908eba2960e763ea8489e79794b4d6a` | [s4_frames.zip](https://drive.google.com/file/d/13WabwEOeR3NF5MOWMXWGZWfshAOkRGVi/view) |

## 4. Optional: full state of the non-item checkpoints

The repo holds the full state of every **item** checkpoint and the `meta.json` of every checkpoint. The full state
(`physics.npz`, `control.pkl`, `cloth.npz`, `cloth_plain.pkl`, `look.jpg`) of the act / roll checkpoints between items is
not in git; it is only needed to resume from a point between two items (the StateRec `states/` already hold the full
30 Hz state for replay). Zip per session if wanted:

| session folder `...\checkpoints\` (non-item dirs, without meta.json) | files | bytes | zip SHA-256 | Drive link |
|---|---|---|---|---|
| `C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\checkpoints` | 5677 | 1078717114 | `b7dd3a0cc5e1d19f192af356d81de3a2b3c5780baa81e61b01a31538cb3e1137` | [s1_checkpoints_between_items.zip](https://drive.google.com/file/d/1MjDXS9BkV11VAIeeHsiBOhenQVRGtaOD/view) |
| `C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\checkpoints` | 1081 | 264771962 | `c2464bc8889487fed8254812e2aebbbe33059360ffaa7a28871ee25a5e69babb` | [s2_checkpoints_between_items.zip](https://drive.google.com/file/d/14Ghv37_zn-eTFCFXHojeD4qgrcbT3RmW/view) |
| `C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3\checkpoints` | 4905 | 693807296 | `c499b2b0a4f733b9ee82c7d5d4219641d2f905c2c21c0751a029c7ece4b2421e` | [s3_checkpoints_between_items.zip](https://drive.google.com/file/d/1DCFApJ4G1bzx8cxCi36tT-YBNCfNZfeR/view) |
| `C:\Users\raresense\sim_home\runs\1121_123451_dex1_floor_final_s4\checkpoints` | 1128 | 625125597 | `3baa8893fa06ff195edf52b596fec0e0aae03482d44d410345b5c299e4ff563d` | [s4_checkpoints_between_items.zip](https://drive.google.com/file/d/1b9Y6TFq93ARKgmLU8gldA0xC1fEcqDwu/view) |

## 5. Training data (LeRobot v2.1 dataset, zip)

The folder `dataset/apartment_g1_dex1_tidy/` of this repo (35 episodes, 361935 frames, parquet + 480p videos + meta),
zipped without compression (ZIP_STORED, top folder `apartment_g1_dex1_tidy/`). The same files are in git. **Drive
folder:** `long-horizon-apartment/dataset/`. Uploaded 22 Nov 2026, confirmed by Drive id and size.

| file | contents | bytes | SHA-256 | Drive link |
|---|---|---|---|---|
| `apartment_g1_dex1_tidy_lerobot_v2.1.zip` | `dataset/apartment_g1_dex1_tidy/` (111 files, 1719254557 bytes) | 1719279167 | `dad4250ba3b7899ac45fdd59d1fc082348a46abb34209e40b7b9273b82c0fccd` | [apartment_g1_dex1_tidy_lerobot_v2.1.zip](https://drive.google.com/file/d/1l-V8oRfdSCMqIFBpSnA7jt_ErftyBND7/view) |

## Not planned for Drive

- `C:\Users\raresense\sim_home\final_video\room_so_far.mp4` (11748775019 bytes) and `head_so_far.mp4` (13531368493 bytes):
  intermediate joins of the render worker, superseded by section 1 (they also contain units after the episode end).
- No data file of this repo is over 95 MB: everything requested for `data/episode/` (states, item checkpoints, meta,
  actions, traces) fits in git.
