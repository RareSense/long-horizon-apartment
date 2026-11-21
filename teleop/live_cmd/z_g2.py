zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece")
TUCK_JOINTS = False
STANCE_LOW_ROOM = 0.35
STANCE_FUR_ROOM = 0.32
floor_first(["r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket", "r117i1_blanket", "r116i1_coat_pile", "r190i1_stocking", "r68i1_rag"])
# out of the pocket to the east by hand-set way points (the planner's tight way passes the scooter's stem foot: left knee
# 27 N three times this session): south to y -1.10, then east along y -1.20 (0.29 m from the scooter's box, 0.27 m from
# rug toy r193i3), crossing the rug edge (x -2.15) square on, to the open floor at (-1.45,-1.15)
mon_start(); MON["trace"] = []
zz_ok = True
try:
    walk_via([(-2.66, -1.10), (-2.0, -1.20), (-1.45, -1.15)], seg=0.30)
except Abort as ex:
    zz_ok = False; print("TRANSIT ABORT", ex)
MON["on"] = False
print("transit", zz_ok, state(), "trace", MON["trace"][::4])
MON["trace"] = None
print(look3("transit_east"))
if zz_ok:
    zz_gr = go_item()
