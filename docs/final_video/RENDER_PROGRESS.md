# Final video render progress (AI_operated replay render of the G1 apartment episode)

Updated 2026-11-21 16:32:56 by render_follow.py (standalone, no AI). State: waiting for the recording (chain 36 pieces, newest checkpoint 0558_roll_t12653.0).
Runs: `C:\Users\raresense\sim_home\runs\*_dex1_floor_final*`; episode from the `_start_clean` checkpoint, chain pieces only. Isaac slot "cloth" port 47970.
Look: tag look-final (E:\urc_look 4c9a52a, merged in E:\urc_final final-episode), RT real-time ray tracing with the final look's still settings (RaytracedLighting, DLSS Quality (stills: DLAA), reflections/translucency/shadows/GI/AO/sampled lighting), ACES + film ISO per camera, bloom / vignette / grain (final_look.cam_look, in render_post.py); no path tracing. Room 1920x1080, head 1440x1080, 30 fps, H.264 CRF 20.

Episode rendered and in the joins: 262 units, 376142 frames = 209.0 min per camera. Chain now: 36 pieces; units known 263. Sessions started: 18. Measured s/frame (room / head): [0.073, 0.075].
Joins: C:\Users\raresense\sim_home\final_video\room_so_far.mp4 and C:\Users\raresense\sim_home\final_video\head_so_far.mp4 ({'room': 208.97, 'head': 208.97}, at 16:32:56).
Room camera: eye -5.35,-2.5,2.45 at 2.5,0.9,-0.1 focal 9.5; room chunks with this view: 262/262 (old views kept in C:\Users\raresense\sim_home\final_video\room_old_view).

## How to check / continue

- status: C:\Users\raresense\sim_home\final_video\status.json; log: C:\Users\raresense\sim_home\final_video\follow.log; guard: C:\Users\raresense\sim_home\final_video\guard.log
- stop: create C:\Users\raresense\sim_home\final_video\STOP; restart: `py -3.12 E:\urc_final\scripts\home\replay\render_follow.py --room-cam-pose -5.35 -2.5 2.45 2.5 0.9 -0.1 --room-focal 9.5 --rerender-room-done` (resumes from done.json)

## Units

| # | run piece | states file | frames | s/frame room/head | status | QC |
|---|---|---|---|---|---|---|
| 0000 | 1120_181556_dex1_floor_final p1 | chunk_00001_f0000100.npz | 100-1899 (1800) | 0.078/0.078 | ok | ok |
| 0001 | 1120_181556_dex1_floor_final p1 | chunk_00002_f0001900.npz | 1900-3699 (1800) | 0.087/0.074 | ok | ok |
| 0002 | 1120_181556_dex1_floor_final p1 | chunk_00003_f0003700.npz | 3700-4208 (509) | 0.091/0.074 | ok | ok |
| 0003 | 1120_181556_dex1_floor_final p1 | chunk_00004_f0004209.npz | 4209-6008 (1800) | 0.086/0.077 | ok | ok |
| 0004 | 1120_181556_dex1_floor_final p1 | chunk_00005_f0006009.npz | 6009-7808 (1800) | 0.086/0.076 | ok | ok |
| 0005 | 1120_181556_dex1_floor_final p1 | chunk_00006_f0007809.npz | 7809-7958 (150) | 0.105/0.074 | ok | body at qpos 656 jumps 0.05 m / 0 deg at frame 7823; body at qpos 656 jumps 0.06 m / 0 deg at frame 7824; body at qpos 656 jumps 0.07 m / 0 deg at frame 7825; body at qpos 656 jumps 0.08 m / 0 deg at frame 7826; body at qpos 656 jumps 0.09 m / 0 deg at frame 7827; body at qpos 656 jumps 0.05 m / 31 deg at frame 7828 |
| 0006 | 1120_181556_dex1_floor_final p1 | chunk_00007_f0007959.npz | 7959-9758 (1800) | 0.088/0.073 | FAILED | static r186i1_basket: crop changed > 4.0 grey levels without robot / motion at 71 frames (first [8925, 8927, 8928, 8986]) |
| 0007 | 1120_181556_dex1_floor_final p1 | chunk_00008_f0009759.npz | 9759-11558 (1800) | 0.084/0.076 | FAILED | static r186i1_basket: crop changed > 4.0 grey levels without robot / motion at 30 frames (first [9818, 9819, 9820, 9822]) |
| 0008 | 1120_181556_dex1_floor_final p1 | chunk_00009_f0011559.npz | 11559-13358 (1800) | 0.077/0.075 | ok | ok |
| 0009 | 1120_181556_dex1_floor_final p1 | chunk_00010_f0013359.npz | 13359-15158 (1800) | 0.077/0.078 | ok | ok |
| 0010 | 1120_181556_dex1_floor_final p1 | chunk_00011_f0015159.npz | 15159-15574 (416) | 0.084/0.082 | ok | body at qpos 642 jumps 0.05 m / 0 deg at frame 15431; body at qpos 642 jumps 0.06 m / 0 deg at frame 15432; body at qpos 642 jumps 0.07 m / 0 deg at frame 15433; body at qpos 642 jumps 0.08 m / 0 deg at frame 15434; body at qpos 642 jumps 0.09 m / 0 deg at frame 15435; body at qpos 642 jumps 0.07 m / 31 deg at frame 15436 |
| 0011 | 1120_181556_dex1_floor_final p1 | chunk_00012_f0015575.npz | 15575-17374 (1800) | 0.078/0.077 | ok | ok |
| 0012 | 1120_181556_dex1_floor_final p1 | chunk_00013_f0017375.npz | 17375-19174 (1800) | 0.078/0.078 | ok | ok |
| 0013 | 1120_181556_dex1_floor_final p1 | chunk_00014_f0019175.npz | 19175-20974 (1800) | 0.077/0.074 | ok | ok |
| 0014 | 1120_181556_dex1_floor_final p1 | chunk_00015_f0020975.npz | 20975-21609 (635) | 0.08/0.059 | ok | ok |
| 0015 | 1120_181556_dex1_floor_final p1 | chunk_00016_f0021610.npz | 21610-22768 (1159) | 0.08/0.074 | ok | ok |
| 0016 | 1120_181556_dex1_floor_final p2 | chunk_00016_f0021610.npz | 22873-23409 (537) | 0.082/0.073 | ok | ok |
| 0017 | 1120_181556_dex1_floor_final p2 | chunk_00017_f0023410.npz | 23410-24699 (1290) | 0.077/0.063 | ok | ok |
| 0018 | 1120_181556_dex1_floor_final p2 | chunk_00018_f0024700.npz | 24700-26499 (1800) | 0.077/0.077 | ok | ok |
| 0019 | 1120_181556_dex1_floor_final p2 | chunk_00019_f0026500.npz | 26500-28299 (1800) | 0.077/0.074 | ok | ok |
| 0020 | 1120_181556_dex1_floor_final p2 | chunk_00020_f0028300.npz | 28300-30099 (1800) | 0.078/0.079 | ok | ok |
| 0021 | 1120_181556_dex1_floor_final p2 | chunk_00021_f0030100.npz | 30100-31114 (1015) | 0.079/0.066 | ok | garment r131i1_knit_hat jumps 0.06 m at frame 30691 |
| 0022 | 1120_181556_dex1_floor_final p2 | chunk_00022_f0031115.npz | 31115-32914 (1800) | 0.078/0.069 | ok | ok |
| 0023 | 1120_181556_dex1_floor_final p2 | chunk_00023_f0032915.npz | 32915-34714 (1800) | 0.079/0.066 | ok | ok |
| 0024 | 1120_181556_dex1_floor_final p2 | chunk_00024_f0034715.npz | 34715-34891 (177) | 0.092/0.077 | ok | ok |
| 0025 | 1120_181556_dex1_floor_final p2 | chunk_00025_f0034892.npz | 34892-36691 (1800) | 0.078/0.064 | ok | ok |
| 0026 | 1120_181556_dex1_floor_final p2 | chunk_00026_f0036692.npz | 36692-38491 (1800) | 0.078/0.065 | ok | ok |
| 0027 | 1120_181556_dex1_floor_final p2 | chunk_00027_f0038492.npz | 38492-40291 (1800) | 0.078/0.066 | ok | ok |
| 0028 | 1120_181556_dex1_floor_final p2 | chunk_00028_f0040292.npz | 40292-42091 (1800) | 0.078/0.066 | ok | ok |
| 0029 | 1120_181556_dex1_floor_final p2 | chunk_00029_f0042092.npz | 42092-43882 (1791) | 0.078/0.066 | ok | ok |
| 0030 | 1120_181556_dex1_floor_final p2 | chunk_00030_f0043883.npz | 43883-44106 (224) | 0.086/0.076 | ok | ok |
| 0031 | 1120_181556_dex1_floor_final p4 | chunk_00031_f0045683.npz | 45916-47053 (1138) | 0.073/0.067 | ok | ok |
| 0032 | 1120_181556_dex1_floor_final p5 | chunk_00034_f0051083.npz | 51217-52882 (1666) | 0.073/0.066 | ok | ok |
| 0033 | 1120_181556_dex1_floor_final p5 | chunk_00035_f0052883.npz | 52883-53010 (128) | 0.101/0.098 | ok | ok |
| 0034 | 1120_181556_dex1_floor_final p7 | chunk_00043_f0067283.npz | 68609-69082 (474) | 0.079/0.082 | ok | garment r117i1_blanket jumps 0.06 m at frame 68621; garment r117i1_blanket jumps 0.05 m at frame 68622 |
| 0035 | 1120_181556_dex1_floor_final p7 | chunk_00044_f0069083.npz | 69083-70882 (1800) | 0.078/0.071 | ok | garment r117i1_blanket jumps 0.06 m at frame 69239 |
| 0036 | 1120_181556_dex1_floor_final p7 | chunk_00045_f0070883.npz | 70883-72682 (1800) | 0.076/0.061 | ok | garment r117i1_blanket jumps 0.06 m at frame 71885; garment r117i1_blanket jumps 0.06 m at frame 71886; garment r117i1_blanket jumps 0.06 m at frame 71887; garment r117i1_blanket jumps 0.07 m at frame 71888; garment r117i1_blanket jumps 0.07 m at frame 71889; garment r117i1_blanket jumps 0.07 m at frame 71890; garment r117i1_blanket jumps 0.06 m at frame 71891 |
| 0037 | 1120_181556_dex1_floor_final p7 | chunk_00046_f0072683.npz | 72683-74482 (1800) | 0.077/0.066 | ok | ok |
| 0038 | 1120_181556_dex1_floor_final p7 | chunk_00047_f0074483.npz | 74483-76282 (1800) | 0.077/0.067 | ok | ok |
| 0039 | 1120_181556_dex1_floor_final p7 | chunk_00048_f0076283.npz | 76283-78029 (1747) | 0.076/0.066 | ok | ok |
| 0040 | 1120_181556_dex1_floor_final p8 | chunk_00050_f0079883.npz | 80574-81682 (1109) | 0.078/0.068 | ok | ok |
| 0041 | 1120_181556_dex1_floor_final p8 | chunk_00051_f0081683.npz | 81683-83482 (1800) | 0.076/0.066 | ok | ok |
| 0042 | 1120_181556_dex1_floor_final p8 | chunk_00052_f0083483.npz | 83483-84080 (598) | 0.08/0.069 | ok | ok |
| 0043 | 1120_181556_dex1_floor_final p9 | chunk_00053_f0085283.npz | 85336-86632 (1297) | 0.077/0.066 | ok | ok |
| 0044 | 1120_181556_dex1_floor_final p10 | chunk_00055_f0088883.npz | 89780-90682 (903) | 0.079/0.068 | ok | ok |
| 0045 | 1120_181556_dex1_floor_final p10 | chunk_00056_f0090683.npz | 90683-92482 (1800) | 0.076/0.063 | ok | ok |
| 0046 | 1120_181556_dex1_floor_final p10 | chunk_00057_f0092483.npz | 92483-94282 (1800) | 0.075/0.065 | ok | ok |
| 0047 | 1120_181556_dex1_floor_final p10 | chunk_00058_f0094283.npz | 94283-96082 (1800) | 0.076/0.066 | ok | ok |
| 0048 | 1120_181556_dex1_floor_final p10 | chunk_00059_f0096083.npz | 96083-97797 (1715) | 0.076/0.067 | ok | ok |
| 0049 | 1120_181556_dex1_floor_final p11 | chunk_00060_f0097883.npz | 98045-99682 (1638) | 0.077/0.067 | ok | ok |
| 0050 | 1120_181556_dex1_floor_final p11 | chunk_00061_f0099683.npz | 99683-101482 (1800) | 0.077/0.064 | ok | ok |
| 0051 | 1120_181556_dex1_floor_final p11 | chunk_00062_f0101483.npz | 101483-101989 (507) | 0.077/0.066 | ok | ok |
| 0052 | 1120_181556_dex1_floor_final p11 | chunk_00063_f0101990.npz | 101990-103789 (1800) | 0.076/0.065 | ok | ok |
| 0053 | 1120_181556_dex1_floor_final p11 | chunk_00064_f0103790.npz | 103790-105589 (1800) | 0.076/0.065 | ok | garment r116i1_coat_pile jumps 0.06 m at frame 105343; garment r116i1_coat_pile jumps 0.07 m at frame 105344; garment r116i1_coat_pile jumps 0.06 m at frame 105345; garment r116i1_coat_pile jumps 0.05 m at frame 105346; garment r116i1_coat_pile jumps 0.06 m at frame 105402; garment r116i1_coat_pile jumps 0.10 m at frame 105409 |
| 0054 | 1120_181556_dex1_floor_final p11 | chunk_00065_f0105590.npz | 105590-107389 (1800) | 0.076/0.066 | ok | ok |
| 0055 | 1120_181556_dex1_floor_final p11 | chunk_00066_f0107390.npz | 107390-109189 (1800) | 0.076/0.061 | ok | garment r116i1_coat_pile jumps 0.05 m at frame 108889; garment r116i1_coat_pile jumps 0.07 m at frame 108890; garment r116i1_coat_pile jumps 0.06 m at frame 108891; garment r116i1_coat_pile jumps 0.07 m at frame 108892; garment r116i1_coat_pile jumps 0.08 m at frame 108893; garment r116i1_coat_pile jumps 0.08 m at frame 108894; garment r116i1_coat_pile jumps 0.07 m at frame 108895; garment r116i1_coat_pile jumps 0.06 m at frame 108896; garment r116i1_coat_pile jumps 0.06 m at frame 108899; garment r116i1_coat_pile jumps 0.06 m at frame 108900; garment r116i1_coat_pile jumps 0.05 m at frame 108908; garment r116i1_coat_pile jumps 0.05 m at frame 108909 |
| 0056 | 1120_181556_dex1_floor_final p11 | chunk_00067_f0109190.npz | 109190-110989 (1800) | 0.076/0.067 | ok | ok |
| 0057 | 1120_181556_dex1_floor_final p11 | chunk_00068_f0110990.npz | 110990-112789 (1800) | 0.077/0.067 | ok | ok |
| 0058 | 1120_181556_dex1_floor_final p11 | chunk_00069_f0112790.npz | 112790-114589 (0) | None/None | FAILED | render failed 3 times |
| 0059 | 1120_181556_dex1_floor_final p11 | chunk_00070_f0114590.npz | 114590-115032 (443) | 0.095/0.075 | ok | ok |
| 0060 | 1120_181556_dex1_floor_final p12 | chunk_00071_f0116390.npz | 117833-118189 (357) | 0.098/0.078 | ok | ok |
| 0061 | 1120_181556_dex1_floor_final p12 | chunk_00072_f0118190.npz | 118190-119989 (1800) | 0.091/0.07 | ok | ok |
| 0062 | 1120_181556_dex1_floor_final p12 | chunk_00073_f0119990.npz | 119990-121789 (1800) | 0.087/0.068 | ok | ok |
| 0063 | 1120_181556_dex1_floor_final p12 | chunk_00074_f0121790.npz | 121790-123589 (1800) | 0.087/0.068 | ok | ok |
| 0064 | 1120_181556_dex1_floor_final p12 | chunk_00075_f0123590.npz | 123590-125389 (1800) | 0.086/0.068 | ok | ok |
| 0065 | 1120_181556_dex1_floor_final p12 | chunk_00076_f0125390.npz | 125390-126936 (1547) | 0.086/0.072 | ok | ok |
| 0066 | 1120_181556_dex1_floor_final p12 | chunk_00077_f0126937.npz | 126937-128736 (1800) | 0.086/0.075 | ok | ok |
| 0067 | 1120_181556_dex1_floor_final p12 | chunk_00078_f0128737.npz | 128737-130536 (1800) | 0.086/0.079 | ok | ok |
| 0068 | 1120_181556_dex1_floor_final p12 | chunk_00079_f0130537.npz | 130537-132336 (1800) | 0.086/0.078 | ok | ok |
| 0069 | 1120_181556_dex1_floor_final p12 | chunk_00080_f0132337.npz | 132337-134136 (1800) | 0.086/0.071 | ok | ok |
| 0070 | 1120_181556_dex1_floor_final p12 | chunk_00081_f0134137.npz | 134137-135936 (1800) | 0.087/0.068 | ok | ok |
| 0071 | 1120_181556_dex1_floor_final p12 | chunk_00082_f0135937.npz | 135937-136221 (285) | 0.096/0.075 | ok | ok |
| 0072 | 1120_181556_dex1_floor_final p12 | chunk_00083_f0136222.npz | 136222-138021 (1800) | 0.086/0.067 | ok | ok |
| 0073 | 1120_181556_dex1_floor_final p12 | chunk_00084_f0138022.npz | 138022-139821 (1800) | 0.087/0.066 | ok | ok |
| 0074 | 1120_181556_dex1_floor_final p12 | chunk_00085_f0139822.npz | 139822-141621 (1800) | 0.087/0.066 | ok | ok |
| 0075 | 1120_181556_dex1_floor_final p12 | chunk_00086_f0141622.npz | 141622-143421 (1800) | 0.086/0.067 | ok | ok |
| 0076 | 1120_181556_dex1_floor_final p12 | chunk_00087_f0143422.npz | 143422-143544 (123) | 0.11/0.087 | ok | ok |
| 0077 | 1120_181556_dex1_floor_final p12 | chunk_00088_f0143545.npz | 143545-145344 (1800) | 0.087/0.068 | ok | ok |
| 0078 | 1120_181556_dex1_floor_final p12 | chunk_00089_f0145345.npz | 145345-147144 (1800) | 0.086/0.067 | ok | ok |
| 0079 | 1120_181556_dex1_floor_final p12 | chunk_00090_f0147145.npz | 147145-148944 (1800) | 0.086/0.067 | ok | ok |
| 0080 | 1120_181556_dex1_floor_final p12 | chunk_00091_f0148945.npz | 148945-150744 (1800) | 0.086/0.067 | ok | ok |
| 0081 | 1120_181556_dex1_floor_final p12 | chunk_00092_f0150745.npz | 150745-152544 (1800) | 0.087/0.067 | ok | ok |
| 0082 | 1120_181556_dex1_floor_final p12 | chunk_00093_f0152545.npz | 152545-154005 (1461) | 0.087/0.067 | ok | ok |
| 0083 | 1120_181556_dex1_floor_final p12 | chunk_00094_f0154006.npz | 154006-155805 (1800) | 0.086/0.067 | ok | garment r68i1_rag jumps 0.06 m at frame 155362; garment r68i1_rag jumps 0.08 m at frame 155363; garment r68i1_rag jumps 0.08 m at frame 155364; garment r68i1_rag jumps 0.08 m at frame 155365; garment r68i1_rag jumps 0.06 m at frame 155366; garment r68i1_rag jumps 0.06 m at frame 155367; garment r68i1_rag jumps 0.06 m at frame 155368; garment r68i1_rag jumps 0.05 m at frame 155380 |
| 0084 | 1120_181556_dex1_floor_final p12 | chunk_00095_f0155806.npz | 155806-157605 (1800) | 0.086/0.068 | ok | ok |
| 0085 | 1120_181556_dex1_floor_final p12 | chunk_00096_f0157606.npz | 157606-159405 (1800) | 0.086/0.068 | ok | ok |
| 0086 | 1120_181556_dex1_floor_final p12 | chunk_00097_f0159406.npz | 159406-161205 (1800) | 0.087/0.068 | ok | garment r68i1_rag jumps 0.06 m at frame 160773; garment r68i1_rag jumps 0.07 m at frame 160774; garment r68i1_rag jumps 0.07 m at frame 160775; garment r68i1_rag jumps 0.08 m at frame 160776; garment r68i1_rag jumps 0.10 m at frame 160777; garment r68i1_rag jumps 0.09 m at frame 160778; garment r68i1_rag jumps 0.08 m at frame 160779 |
| 0087 | 1120_181556_dex1_floor_final p12 | chunk_00098_f0161206.npz | 161206-161337 (132) | 0.108/0.087 | ok | ok |
| 0088 | 1120_181556_dex1_floor_final p84 | chunk_00108_f0171327.npz | 172404-172421 (18) | 0.261/0.24 | ok | ok |
| 0089 | 1120_181556_dex1_floor_final p84 | chunk_00109_f0172422.npz | 172422-173972 (1551) | 0.087/0.068 | ok | ok |
| 0090 | 1120_181556_dex1_floor_final p84 | chunk_00110_f0173973.npz | 173973-175772 (1800) | 0.085/0.066 | ok | ok |
| 0091 | 1120_181556_dex1_floor_final p84 | chunk_00111_f0175773.npz | 175773-176029 (257) | 0.096/0.076 | ok | ok |
| 0092 | 1120_181556_dex1_floor_final p86 | chunk_00116_f0183230.npz | 184108-185029 (922) | 0.087/0.068 | ok | ok |
| 0093 | 1120_181556_dex1_floor_final p86 | chunk_00117_f0185030.npz | 185030-186829 (1800) | 0.086/0.068 | ok | ok |
| 0094 | 1120_181556_dex1_floor_final p86 | chunk_00118_f0186830.npz | 186830-188629 (1800) | 0.086/0.068 | ok | body at qpos 348 jumps 0.06 m / 11 deg at frame 188047; body at qpos 348 jumps 0.07 m / 12 deg at frame 188048; body at qpos 348 jumps 0.07 m / 12 deg at frame 188049 |
| 0095 | 1120_181556_dex1_floor_final p86 | chunk_00119_f0188630.npz | 188630-190429 (1800) | 0.086/0.07 | ok | ok |
| 0096 | 1120_181556_dex1_floor_final p86 | chunk_00120_f0190430.npz | 190430-192229 (1800) | 0.086/0.07 | ok | ok |
| 0097 | 1120_181556_dex1_floor_final p86 | chunk_00121_f0192230.npz | 192230-194029 (1800) | 0.086/0.066 | ok | ok |
| 0098 | 1120_181556_dex1_floor_final p86 | chunk_00122_f0194030.npz | 194030-195728 (1699) | 0.086/0.066 | ok | ok |
| 0099 | 1120_181556_dex1_floor_final p86 | chunk_00123_f0195729.npz | 195729-195842 (114) | 0.111/0.089 | ok | body at qpos 348 jumps 0.06 m / 17 deg at frame 195796; body at qpos 348 jumps 0.07 m / 18 deg at frame 195797; body at qpos 348 jumps 0.08 m / 17 deg at frame 195798; body at qpos 348 jumps 0.06 m / 9 deg at frame 195799 |
| 0100 | 1121_021343_dex1_floor_final_s2 p5 | chunk_00007_f0012600.npz | 12869-12968 (100) | 0.113/0.091 | ok | ok |
| 0101 | 1121_021343_dex1_floor_final_s2 p6 | chunk_00008_f0014400.npz | 15724-16199 (476) | 0.093/0.072 | ok | ok |
| 0102 | 1121_021343_dex1_floor_final_s2 p6 | chunk_00009_f0016200.npz | 16200-17999 (1800) | 0.085/0.073 | ok | ok |
| 0103 | 1121_021343_dex1_floor_final_s2 p6 | chunk_00010_f0018000.npz | 18000-18270 (271) | 0.096/0.081 | ok | ok |
| 0104 | 1121_021343_dex1_floor_final_s2 p8 | chunk_00011_f0019800.npz | 20007-21599 (1593) | 0.086/0.069 | ok | garment r190i1_stocking jumps 0.06 m at frame 21340 |
| 0105 | 1121_021343_dex1_floor_final_s2 p8 | chunk_00012_f0021600.npz | 21600-23399 (1800) | 0.086/0.069 | ok | ok |
| 0106 | 1121_021343_dex1_floor_final_s2 p8 | chunk_00013_f0023400.npz | 23400-23730 (331) | 0.097/0.078 | ok | ok |
| 0107 | 1121_021343_dex1_floor_final_s2 p9 | chunk_00013_f0023400.npz | 24258-25199 (942) | 0.088/0.071 | ok | ok |
| 0108 | 1121_021343_dex1_floor_final_s2 p9 | chunk_00014_f0025200.npz | 25200-26999 (1800) | 0.086/0.067 | ok | ok |
| 0109 | 1121_021343_dex1_floor_final_s2 p9 | chunk_00015_f0027000.npz | 27000-27540 (541) | 0.09/0.07 | ok | ok |
| 0110 | 1121_021343_dex1_floor_final_s2 p10 | chunk_00020_f0034741.npz | 35901-36540 (640) | 0.089/0.07 | ok | ok |
| 0111 | 1121_021343_dex1_floor_final_s2 p10 | chunk_00021_f0036541.npz | 36541-38340 (1800) | 0.086/0.067 | ok | ok |
| 0112 | 1121_021343_dex1_floor_final_s2 p10 | chunk_00022_f0038341.npz | 38341-38948 (608) | 0.09/0.069 | ok | body at qpos 306 jumps 0.02 m / 26 deg at frame 38674; body at qpos 306 jumps 0.02 m / 25 deg at frame 38675; body at qpos 306 jumps 0.03 m / 25 deg at frame 38677 |
| 0113 | 1121_034845_dex1_floor_final_s3 p1 | chunk_00000_f0000000.npz | 0-1799 (1800) | 0.079/0.068 | ok | body at qpos 341 jumps 0.07 m / 11 deg at frame 1616; body at qpos 341 jumps 0.07 m / 10 deg at frame 1617; body at qpos 341 jumps 0.05 m / 16 deg at frame 1618 |
| 0114 | 1121_034845_dex1_floor_final_s3 p1 | chunk_00001_f0001800.npz | 1800-3599 (1800) | 0.077/0.066 | ok | ok |
| 0115 | 1121_034845_dex1_floor_final_s3 p1 | chunk_00002_f0003600.npz | 3600-5399 (1800) | 0.077/0.073 | ok | ok |
| 0116 | 1121_034845_dex1_floor_final_s3 p1 | chunk_00003_f0005400.npz | 5400-7199 (1800) | 0.077/0.067 | ok | ok |
| 0117 | 1121_034845_dex1_floor_final_s3 p1 | chunk_00004_f0007200.npz | 7200-8999 (1800) | 0.077/0.07 | ok | ok |
| 0118 | 1121_034845_dex1_floor_final_s3 p1 | chunk_00005_f0009000.npz | 9000-10799 (1800) | 0.076/0.065 | ok | ok |
| 0119 | 1121_034845_dex1_floor_final_s3 p1 | chunk_00006_f0010800.npz | 10800-11070 (271) | 0.085/0.073 | ok | ok |
| 0120 | 1121_034845_dex1_floor_final_s3 p3 | chunk_00015_f0025471.npz | 25941-27270 (1330) | 0.077/0.066 | ok | ok |
| 0121 | 1121_034845_dex1_floor_final_s3 p3 | chunk_00016_f0027271.npz | 27271-29070 (1800) | 0.077/0.074 | ok | ok |
| 0122 | 1121_034845_dex1_floor_final_s3 p3 | chunk_00017_f0029071.npz | 29071-30870 (1800) | 0.076/0.068 | ok | ok |
| 0123 | 1121_034845_dex1_floor_final_s3 p3 | chunk_00018_f0030871.npz | 30871-32670 (1800) | 0.076/0.067 | ok | ok |
| 0124 | 1121_034845_dex1_floor_final_s3 p3 | chunk_00019_f0032671.npz | 32671-34470 (1800) | 0.076/0.07 | ok | ok |
| 0125 | 1121_021343_dex1_floor_final_s2 p11 | chunk_00026_f0044349.npz | 44652-46148 (1497) | 0.076/0.066 | dropped (not in the chain any more) | ok |
| 0126 | 1121_034845_dex1_floor_final_s3 p3 | chunk_00020_f0034471.npz | 34471-36270 (1800) | 0.077/0.067 | ok | ok |
| 0127 | 1121_034845_dex1_floor_final_s3 p3 | chunk_00021_f0036271.npz | 36271-38070 (1800) | 0.076/0.066 | ok | ok |
| 0128 | 1121_034845_dex1_floor_final_s3 p3 | chunk_00022_f0038071.npz | 38071-38514 (444) | 0.081/0.07 | ok | ok |
| 0129 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00022_f0038071.npz | 39328-39870 (543) | 0.079/0.071 | ok | ok |
| 0130 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00023_f0039871.npz | 39871-41670 (1800) | 0.076/0.066 | ok | ok |
| 0131 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00024_f0041671.npz | 41671-43470 (1800) | 0.076/0.067 | ok | ok |
| 0132 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00025_f0043471.npz | 43471-43624 (154) | 0.093/0.08 | ok | ok |
| 0133 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00026_f0043625.npz | 43625-45424 (1800) | 0.077/0.065 | ok | ok |
| 0134 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00027_f0045425.npz | 45425-47224 (1800) | 0.077/0.063 | ok | ok |
| 0135 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00028_f0047225.npz | 47225-49024 (1800) | 0.077/0.066 | ok | ok |
| 0136 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00029_f0049025.npz | 49025-50824 (1800) | 0.076/0.065 | ok | ok |
| 0137 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00030_f0050825.npz | 50825-52624 (1800) | 0.076/0.065 | ok | body at qpos 551 jumps 0.01 m / 30 deg at frame 52371; body at qpos 551 jumps 0.01 m / 37 deg at frame 52372; body at qpos 551 jumps 0.02 m / 40 deg at frame 52373; body at qpos 551 jumps 0.02 m / 34 deg at frame 52374; body at qpos 551 jumps 0.01 m / 33 deg at frame 52379; body at qpos 551 jumps 0.02 m / 40 deg at frame 52380; body at qpos 551 jumps 0.03 m / 46 deg at frame 52381; body at qpos 551 jumps 0.02 m / 34 deg at frame 52382 |
| 0138 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00031_f0052625.npz | 52625-52705 (81) | 0.109/0.092 | ok | ok |
| 0139 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00032_f0052706.npz | 52706-54505 (1800) | 0.076/0.063 | ok | ok |
| 0140 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00033_f0054506.npz | 54506-56305 (1800) | 0.077/0.062 | ok | ok |
| 0141 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00034_f0056306.npz | 56306-58105 (1800) | 0.076/0.065 | ok | ok |
| 0142 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00035_f0058106.npz | 58106-59905 (1800) | 0.077/0.074 | ok | ok |
| 0143 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00036_f0059906.npz | 59906-61705 (1800) | 0.076/0.067 | ok | ok |
| 0144 | 1121_034845_dex1_floor_final_s3 p4 | chunk_00037_f0061706.npz | 61706-61933 (228) | 0.088/0.076 | ok | ok |
| 0145 | 1121_034845_dex1_floor_final_s3 p5 | chunk_00037_f0061706.npz | 62895-63505 (611) | 0.079/0.068 | ok | ok |
| 0146 | 1121_034845_dex1_floor_final_s3 p5 | chunk_00038_f0063506.npz | 63506-65267 (1762) | 0.077/0.065 | ok | ok |
| 0147 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00044_f0074268.npz | 74609-76067 (1459) | 0.077/0.067 | ok | ok |
| 0148 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00045_f0076068.npz | 76068-77867 (1800) | 0.076/0.066 | ok | body at qpos 635 jumps 0.06 m / 1 deg at frame 77335; body at qpos 635 jumps 0.07 m / 1 deg at frame 77336; body at qpos 635 jumps 0.06 m / 43 deg at frame 77337; body at qpos 635 jumps 0.04 m / 50 deg at frame 77338; body at qpos 635 jumps 0.03 m / 32 deg at frame 77339; body at qpos 635 jumps 0.04 m / 30 deg at frame 77340; body at qpos 635 jumps 0.05 m / 33 deg at frame 77341; body at qpos 635 jumps 0.06 m / 33 deg at frame 77342; body at qpos 635 jumps 0.06 m / 32 deg at frame 77343; body at qpos 635 jumps 0.08 m / 34 deg at frame 77344; body at qpos 635 jumps 0.09 m / 35 deg at frame 77345; body at qpos 635 jumps 0.06 m / 25 deg at frame 77346 |
| 0149 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00046_f0077868.npz | 77868-79667 (1800) | 0.076/0.065 | ok | body at qpos 635 jumps 0.07 m / 11 deg at frame 78684; body at qpos 635 jumps 0.08 m / 12 deg at frame 78685; body at qpos 635 jumps 0.07 m / 9 deg at frame 78686; body at qpos 635 jumps 0.06 m / 6 deg at frame 78687 |
| 0150 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00047_f0079668.npz | 79668-81467 (1800) | 0.077/0.064 | ok | ok |
| 0151 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00048_f0081468.npz | 81468-82471 (1004) | 0.077/0.066 | ok | ok |
| 0152 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00049_f0082472.npz | 82472-84271 (1800) | 0.076/0.065 | ok | ok |
| 0153 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00050_f0084272.npz | 84272-86071 (1800) | 0.076/0.065 | ok | body at qpos 607 jumps 0.06 m / 10 deg at frame 84774; body at qpos 607 jumps 0.08 m / 14 deg at frame 84775; body at qpos 607 jumps 0.08 m / 12 deg at frame 84776; body at qpos 607 jumps 0.06 m / 8 deg at frame 84777 |
| 0154 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00051_f0086072.npz | 86072-87871 (1800) | 0.076/0.065 | ok | ok |
| 0155 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00052_f0087872.npz | 87872-88366 (495) | 0.08/0.068 | ok | body at qpos 607 jumps 0.02 m / 32 deg at frame 88092; body at qpos 607 jumps 0.02 m / 40 deg at frame 88093; body at qpos 607 jumps 0.03 m / 41 deg at frame 88094; body at qpos 607 jumps 0.02 m / 41 deg at frame 88095; body at qpos 607 jumps 0.01 m / 26 deg at frame 88096 |
| 0156 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00053_f0088367.npz | 88367-90166 (1800) | 0.076/0.066 | ok | body at qpos 621 jumps 0.05 m / 0 deg at frame 90064; body at qpos 621 jumps 0.06 m / 0 deg at frame 90065; body at qpos 621 jumps 0.07 m / 14 deg at frame 90066; body at qpos 621 jumps 0.05 m / 60 deg at frame 90067; body at qpos 621 jumps 0.05 m / 11 deg at frame 90072; body at qpos 621 jumps 0.07 m / 12 deg at frame 90073; body at qpos 621 jumps 0.08 m / 12 deg at frame 90074; body at qpos 621 jumps 0.08 m / 11 deg at frame 90075; body at qpos 621 jumps 0.08 m / 7 deg at frame 90076; body at qpos 621 jumps 0.03 m / 45 deg at frame 90077 |
| 0157 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00054_f0090167.npz | 90167-91966 (1800) | 0.076/0.066 | ok | body at qpos 621 jumps 0.07 m / 12 deg at frame 91091; body at qpos 621 jumps 0.07 m / 12 deg at frame 91092; body at qpos 621 jumps 0.07 m / 10 deg at frame 91093; body at qpos 621 jumps 0.06 m / 7 deg at frame 91094 |
| 0158 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00055_f0091967.npz | 91967-93766 (1800) | 0.078/0.065 | ok | ok |
| 0159 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00056_f0093767.npz | 93767-94507 (741) | 0.078/0.066 | ok | body at qpos 621 jumps 0.02 m / 43 deg at frame 94233 |
| 0160 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00057_f0094508.npz | 94508-96307 (1800) | 0.076/0.065 | ok | ok |
| 0161 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00058_f0096308.npz | 96308-98107 (1800) | 0.076/0.065 | ok | body at qpos 628 jumps 0.07 m / 12 deg at frame 97193; body at qpos 628 jumps 0.07 m / 12 deg at frame 97194; body at qpos 628 jumps 0.07 m / 10 deg at frame 97195; body at qpos 628 jumps 0.06 m / 7 deg at frame 97196 |
| 0162 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00059_f0098108.npz | 98108-99907 (1800) | 0.076/0.065 | ok | ok |
| 0163 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00060_f0099908.npz | 99908-101185 (1278) | 0.076/0.065 | ok | ok |
| 0164 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00061_f0101186.npz | 101186-102985 (1800) | 0.076/0.065 | ok | ok |
| 0165 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00062_f0102986.npz | 102986-104785 (1800) | 0.076/0.065 | ok | body at qpos 614 jumps 0.06 m / 9 deg at frame 103971; body at qpos 614 jumps 0.08 m / 12 deg at frame 103972; body at qpos 614 jumps 0.08 m / 10 deg at frame 103973; body at qpos 614 jumps 0.06 m / 7 deg at frame 103974 |
| 0166 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00063_f0104786.npz | 104786-106585 (1800) | 0.076/0.064 | ok | ok |
| 0167 | 1121_034845_dex1_floor_final_s3 p8 | chunk_00064_f0106586.npz | 106586-107868 (1283) | 0.076/0.065 | ok | ok |
| 0168 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00080_f0134869.npz | 136320-136668 (349) | 0.083/0.071 | ok | ok |
| 0169 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00081_f0136669.npz | 136669-138468 (1800) | 0.075/0.063 | ok | ok |
| 0170 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00082_f0138469.npz | 138469-140268 (1800) | 0.076/0.064 | ok | ok |
| 0171 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00083_f0140269.npz | 140269-142068 (1800) | 0.076/0.063 | ok | ok |
| 0172 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00084_f0142069.npz | 142069-143868 (1800) | 0.076/0.064 | ok | ok |
| 0173 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00085_f0143869.npz | 143869-145668 (1800) | 0.076/0.063 | ok | ok |
| 0174 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00086_f0145669.npz | 145669-145939 (271) | 0.083/0.067 | ok | body at qpos 299 jumps 0.03 m / 29 deg at frame 145669; body at qpos 299 jumps 0.03 m / 35 deg at frame 145670; body at qpos 299 jumps 0.01 m / 30 deg at frame 145681; body at qpos 299 jumps 0.01 m / 33 deg at frame 145682; body at qpos 299 jumps 0.01 m / 28 deg at frame 145683; body at qpos 299 jumps 0.01 m / 27 deg at frame 145684 |
| 0175 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00087_f0145940.npz | 145940-147739 (1800) | 0.074/0.064 | ok | ok |
| 0176 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00088_f0147740.npz | 147740-149539 (1800) | 0.076/0.064 | ok | ok |
| 0177 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00089_f0149540.npz | 149540-151339 (1800) | 0.076/0.064 | ok | ok |
| 0178 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00090_f0151340.npz | 151340-153139 (1800) | 0.076/0.064 | ok | ok |
| 0179 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00091_f0153140.npz | 153140-154939 (1800) | 0.075/0.065 | ok | ok |
| 0180 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00092_f0154940.npz | 154940-155084 (145) | 0.094/0.079 | ok | ok |
| 0181 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00093_f0155085.npz | 155085-156884 (1800) | 0.075/0.064 | ok | ok |
| 0182 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00094_f0156885.npz | 156885-158684 (1800) | 0.075/0.064 | ok | ok |
| 0183 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00095_f0158685.npz | 158685-160484 (1800) | 0.075/0.065 | ok | ok |
| 0184 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00096_f0160485.npz | 160485-161397 (913) | 0.077/0.066 | ok | ok |
| 0185 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00097_f0161398.npz | 161398-163197 (1800) | 0.075/0.063 | ok | ok |
| 0186 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00098_f0163198.npz | 163198-164997 (1800) | 0.076/0.064 | ok | ok |
| 0187 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00099_f0164998.npz | 164998-166612 (1615) | 0.076/0.064 | ok | ok |
| 0188 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00100_f0166613.npz | 166613-168412 (1800) | 0.077/0.075 | ok | ok |
| 0189 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00101_f0168413.npz | 168413-170212 (1800) | 0.077/0.068 | ok | ok |
| 0190 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00102_f0170213.npz | 170213-172012 (1800) | 0.075/0.064 | ok | ok |
| 0191 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00103_f0172013.npz | 172013-173812 (1800) | 0.075/0.066 | ok | ok |
| 0192 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00104_f0173813.npz | 173813-175612 (1800) | 0.075/0.065 | ok | ok |
| 0193 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00105_f0175613.npz | 175613-177412 (1800) | 0.075/0.065 | ok | ok |
| 0194 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00106_f0177413.npz | 177413-179212 (1800) | 0.075/0.065 | ok | ok |
| 0195 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00107_f0179213.npz | 179213-181012 (1800) | 0.077/0.059 | ok | ok |
| 0196 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00108_f0181013.npz | 181013-182812 (1800) | 0.075/0.065 | ok | ok |
| 0197 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00109_f0182813.npz | 182813-184612 (1800) | 0.075/0.063 | ok | ok |
| 0198 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00110_f0184613.npz | 184613-186412 (1800) | 0.084/0.064 | ok | ok |
| 0199 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00111_f0186413.npz | 186413-188212 (1800) | 0.083/0.063 | ok | ok |
| 0200 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00112_f0188213.npz | 188213-190012 (1800) | 0.084/0.066 | ok | ok |
| 0201 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00113_f0190013.npz | 190013-191812 (1800) | 0.084/0.065 | ok | ok |
| 0202 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00114_f0191813.npz | 191813-193612 (1800) | 0.084/0.065 | ok | ok |
| 0203 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00115_f0193613.npz | 193613-195412 (1800) | 0.082/0.064 | ok | ok |
| 0204 | 1121_034845_dex1_floor_final_s3 p15 | chunk_00116_f0195413.npz | 195413-195652 (240) | 0.096/0.076 | ok | ok |
| 0205 | 1121_034845_dex1_floor_final_s3 p18 | chunk_00121_f0202853.npz | 204002-204652 (651) | 0.087/0.067 | ok | ok |
| 0206 | 1121_034845_dex1_floor_final_s3 p18 | chunk_00122_f0204653.npz | 204653-205801 (1149) | 0.084/0.066 | ok | ok |
| 0207 | 1121_034845_dex1_floor_final_s3 p19 | chunk_00122_f0204653.npz | 205877-206452 (576) | 0.088/0.068 | ok | ok |
| 0208 | 1121_034845_dex1_floor_final_s3 p19 | chunk_00123_f0206453.npz | 206453-208252 (1800) | 0.084/0.064 | ok | ok |
| 0209 | 1121_034845_dex1_floor_final_s3 p19 | chunk_00124_f0208253.npz | 208253-210052 (1800) | 0.084/0.064 | ok | ok |
| 0210 | 1121_034845_dex1_floor_final_s3 p19 | chunk_00125_f0210053.npz | 210053-210177 (125) | 0.103/0.082 | ok | ok |
| 0211 | 1121_034845_dex1_floor_final_s3 p20 | chunk_00125_f0210053.npz | 210290-210823 (534) | 0.087/0.067 | ok | body at qpos 502 jumps 0.05 m / 0 deg at frame 210693; body at qpos 502 jumps 0.07 m / 0 deg at frame 210694; body at qpos 502 jumps 0.08 m / 0 deg at frame 210695; body at qpos 502 jumps 0.08 m / 0 deg at frame 210696; body at qpos 502 jumps 0.10 m / 0 deg at frame 210697; body at qpos 502 jumps 0.11 m / 0 deg at frame 210698; body at qpos 502 jumps 0.10 m / 12 deg at frame 210699; body at qpos 502 jumps 0.01 m / 56 deg at frame 210700; body at qpos 502 jumps 0.02 m / 44 deg at frame 210701; body at qpos 502 jumps 0.01 m / 30 deg at frame 210702; body at qpos 502 jumps 0.01 m / 28 deg at frame 210703; body at qpos 502 jumps 0.01 m / 31 deg at frame 210704; body at qpos 502 jumps 0.01 m / 35 deg at frame 210705; body at qpos 502 jumps 0.01 m / 36 deg at frame 210706; body at qpos 502 jumps 0.01 m / 27 deg at frame 210707 |
| 0212 | 1121_034845_dex1_floor_final_s3 p21 | chunk_00126_f0210824.npz | 210931-212623 (1693) | 0.082/0.065 | ok | ok |
| 0213 | 1121_034845_dex1_floor_final_s3 p21 | chunk_00127_f0212624.npz | 212624-214423 (1800) | 0.086/0.067 | ok | ok |
| 0214 | 1121_034845_dex1_floor_final_s3 p21 | chunk_00128_f0214424.npz | 214424-216223 (1800) | 0.086/0.071 | ok | ok |
| 0215 | 1121_034845_dex1_floor_final_s3 p21 | chunk_00129_f0216224.npz | 216224-218023 (1800) | 0.087/0.07 | ok | ok |
| 0216 | 1121_034845_dex1_floor_final_s3 p21 | chunk_00130_f0218024.npz | 218024-219823 (1800) | 0.086/0.067 | ok | body at qpos 432 jumps 0.05 m / 0 deg at frame 219773; body at qpos 432 jumps 0.06 m / 0 deg at frame 219774; body at qpos 432 jumps 0.07 m / 0 deg at frame 219775; body at qpos 432 jumps 0.09 m / 0 deg at frame 219776; body at qpos 432 jumps 0.09 m / 0 deg at frame 219777; body at qpos 432 jumps 0.11 m / 0 deg at frame 219778; body at qpos 432 jumps 0.12 m / 1 deg at frame 219779 |
| 0217 | 1121_034845_dex1_floor_final_s3 p21 | chunk_00131_f0219824.npz | 219824-220226 (403) | 0.092/0.071 | ok | ok |
| 0218 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00137_f0229227.npz | 229590-231026 (1437) | 0.086/0.067 | ok | ok |
| 0219 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00138_f0231027.npz | 231027-232826 (1800) | 0.086/0.067 | ok | body at qpos 369 jumps 0.06 m / 7 deg at frame 231759; body at qpos 369 jumps 0.07 m / 8 deg at frame 231760; body at qpos 369 jumps 0.07 m / 7 deg at frame 231761; body at qpos 369 jumps 0.06 m / 6 deg at frame 231762 |
| 0220 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00139_f0232827.npz | 232827-234626 (1800) | 0.083/0.064 | ok | ok |
| 0221 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00140_f0234627.npz | 234627-236426 (1800) | 0.086/0.066 | ok | ok |
| 0222 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00141_f0236427.npz | 236427-238226 (1800) | 0.085/0.067 | ok | ok |
| 0223 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00142_f0238227.npz | 238227-240026 (1800) | 0.083/0.066 | ok | ok |
| 0224 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00143_f0240027.npz | 240027-241826 (1800) | 0.085/0.067 | ok | ok |
| 0225 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00144_f0241827.npz | 241827-243626 (1800) | 0.086/0.066 | ok | ok |
| 0226 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00145_f0243627.npz | 243627-244584 (958) | 0.083/0.058 | ok | ok |
| 0227 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00146_f0244585.npz | 244585-246384 (1800) | 0.072/0.057 | ok | ok |
| 0228 | 1121_034845_dex1_floor_final_s3 p27 | chunk_00147_f0246385.npz | 246385-246412 (28) | 0.177/0.147 | ok | ok |
| 0229 | 1121_034845_dex1_floor_final_s3 p30 | chunk_00151_f0253585.npz | 255364-255384 (21) | 0.208/0.175 | ok | ok |
| 0230 | 1121_034845_dex1_floor_final_s3 p30 | chunk_00152_f0255385.npz | 255385-257184 (1800) | 0.072/0.056 | ok | ok |
| 0231 | 1121_034845_dex1_floor_final_s3 p30 | chunk_00153_f0257185.npz | 257185-257712 (528) | 0.077/0.06 | ok | ok |
| 0232 | 1121_034845_dex1_floor_final_s3 p31 | chunk_00153_f0257185.npz | 258049-258274 (226) | 0.083/0.066 | ok | ok |
| 0233 | 1121_034845_dex1_floor_final_s3 p32 | chunk_00153_f0257185.npz | 258835-258984 (150) | 0.091/0.072 | ok | ok |
| 0234 | 1121_034845_dex1_floor_final_s3 p32 | chunk_00154_f0258985.npz | 258985-260784 (1800) | 0.072/0.056 | ok | ok |
| 0235 | 1121_034845_dex1_floor_final_s3 p32 | chunk_00155_f0260785.npz | 260785-262584 (1800) | 0.073/0.056 | ok | ok |
| 0236 | 1121_034845_dex1_floor_final_s3 p32 | chunk_00156_f0262585.npz | 262585-262956 (372) | 0.08/0.062 | ok | ok |
| 0237 | 1121_034845_dex1_floor_final_s3 p33 | chunk_00156_f0262585.npz | 263781-264384 (604) | 0.075/0.059 | ok | ok |
| 0238 | 1121_034845_dex1_floor_final_s3 p33 | chunk_00157_f0264385.npz | 264385-266184 (1800) | 0.072/0.056 | ok | ok |
| 0239 | 1121_034845_dex1_floor_final_s3 p33 | chunk_00158_f0266185.npz | 266185-267434 (1250) | 0.073/0.057 | ok | ok |
| 0240 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00000_f0000000.npz | 0-1799 (1800) | 0.072/0.057 | ok | ok |
| 0241 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00001_f0001800.npz | 1800-3599 (1800) | 0.073/0.058 | ok | ok |
| 0242 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00002_f0003600.npz | 3600-5399 (1800) | 0.073/0.056 | ok | ok |
| 0243 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00003_f0005400.npz | 5400-7199 (1800) | 0.073/0.058 | ok | ok |
| 0244 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00004_f0007200.npz | 7200-8999 (1800) | 0.074/0.058 | ok | ok |
| 0245 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00005_f0009000.npz | 9000-10393 (1394) | 0.074/0.059 | ok | body at qpos 250 jumps 0.05 m / 0 deg at frame 10098; body at qpos 250 jumps 0.06 m / 23 deg at frame 10099; body at qpos 250 jumps 0.03 m / 124 deg at frame 10100; body at qpos 250 jumps 0.03 m / 135 deg at frame 10101; body at qpos 250 jumps 0.02 m / 121 deg at frame 10102; body at qpos 250 jumps 0.01 m / 56 deg at frame 10103 |
| 0246 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00006_f0010394.npz | 10394-12193 (1800) | 0.074/0.062 | ok | ok |
| 0247 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00007_f0012194.npz | 12194-13993 (1800) | 0.076/0.062 | ok | ok |
| 0248 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00008_f0013994.npz | 13994-15793 (1800) | 0.076/0.064 | ok | ok |
| 0249 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00009_f0015794.npz | 15794-17593 (1800) | 0.077/0.062 | ok | ok |
| 0250 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00010_f0017594.npz | 17594-19393 (1800) | 0.075/0.057 | ok | ok |
| 0251 | 1121_123451_dex1_floor_final_s4 p1 | chunk_00011_f0019394.npz | 19394-19978 (585) | 0.076/0.059 | ok | ok |
| 0252 | 1121_123451_dex1_floor_final_s4 p3 | chunk_00012_f0019979.npz | 19985-20084 (100) | 0.1/0.082 | ok | ok |
| 0253 | 1121_123451_dex1_floor_final_s4 p4 | chunk_00012_f0019979.npz | 21322-21778 (457) | 0.078/0.061 | ok | ok |
| 0254 | 1121_123451_dex1_floor_final_s4 p4 | chunk_00013_f0021779.npz | 21779-23578 (1800) | 0.073/0.057 | ok | ok |
| 0255 | 1121_123451_dex1_floor_final_s4 p4 | chunk_00014_f0023579.npz | 23579-23863 (285) | 0.082/0.064 | ok | ok |
| 0256 | 1121_123451_dex1_floor_final_s4 p5 | chunk_00014_f0023579.npz | 24614-25378 (765) | 0.075/0.059 | ok | ok |
| 0257 | 1121_123451_dex1_floor_final_s4 p5 | chunk_00015_f0025379.npz | 25379-27178 (1800) | 0.073/0.057 | ok | body at qpos 432 jumps 0.06 m / 6 deg at frame 25828; body at qpos 432 jumps 0.07 m / 6 deg at frame 25829; body at qpos 432 jumps 0.08 m / 5 deg at frame 25830; body at qpos 432 jumps 0.10 m / 6 deg at frame 25831; body at qpos 432 jumps 0.11 m / 6 deg at frame 25832; body at qpos 432 jumps 0.07 m / 11 deg at frame 25833; body at qpos 432 jumps 0.04 m / 42 deg at frame 25834 |
| 0258 | 1121_123451_dex1_floor_final_s4 p5 | chunk_00016_f0027179.npz | 27179-28978 (1800) | 0.073/0.057 | ok | ok |
| 0259 | 1121_123451_dex1_floor_final_s4 p5 | chunk_00017_f0028979.npz | 28979-30778 (1800) | 0.074/0.057 | ok | body at qpos 656 jumps 0.05 m / 0 deg at frame 30154; body at qpos 656 jumps 0.07 m / 0 deg at frame 30155; body at qpos 656 jumps 0.07 m / 0 deg at frame 30156; body at qpos 656 jumps 0.09 m / 0 deg at frame 30157; body at qpos 656 jumps 0.10 m / 0 deg at frame 30158; body at qpos 656 jumps 0.10 m / 0 deg at frame 30159; body at qpos 656 jumps 0.09 m / 27 deg at frame 30160; body at qpos 656 jumps 0.01 m / 35 deg at frame 30161 |
| 0260 | 1121_123451_dex1_floor_final_s4 p5 | chunk_00018_f0030779.npz | 30779-32578 (1800) | 0.073/0.057 | ok | ok |
| 0261 | 1121_123451_dex1_floor_final_s4 p5 | chunk_00019_f0032579.npz | 32579-34378 (1800) | 0.074/0.057 | ok | body at qpos 642 jumps 0.01 m / 27 deg at frame 32686 |
| 0262 | 1121_123451_dex1_floor_final_s4 p5 | chunk_00020_f0034379.npz | 34379-36178 (1800) | 0.073/0.057 | ok | ok |
| 0263 | 1121_123451_dex1_floor_final_s4 p5 | chunk_00021_f0036179.npz | 36179-37978 (1800) | 0.073/0.075 | ok | ok |
