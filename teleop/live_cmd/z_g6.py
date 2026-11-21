ck_load(r"C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\0237_act_transit_east_ok")
# knit hat: its own walk stepped on the light saber's east end (22 N); the saber pick failed (pads 5 cm above its grasp
# point twice, then the re-approach walked into the croc). So: round the saber's east end in short steps to the open
# floor east of the knit hat first, then the item from there
zz_ok, zz_log = step_to([(-0.85, -0.85), (-0.88, -0.2)], tols=[0.10, 0.08])
print("pre", zz_ok, zz_log[-3:], state(), flush=True)
if zz_ok:
    zz_gr = go_item()
