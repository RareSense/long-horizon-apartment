zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece")
TUCK_JOINTS = False
STANCE_LOW_ROOM = 0.35
STANCE_FUR_ROOM = 0.32
floor_first(["r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket", "r117i1_blanket", "r116i1_coat_pile", "r190i1_stocking", "r68i1_rag"])


def zz_turn_to(pt):
    for _k in range(14):
        tr_, ds_ = aim(pt)
        if abs(tr_) < 4.0:
            return
        tmove(turn=float(np.clip(tr_, -15, 15)), tag="tr")
        if MON.get("why"):
            raise Abort(MON["why"])


# out of the pocket to the east (AI-operated). The planner's tight way passes the scooter's stem foot (left knee 27 N,
# three times); a 90 deg turn on the spot at (-2.64,-1.07) ran 0.25 m west into ball r192 (right knee 24 N). Now: turns
# in 15 deg steps with a stand after each (tmove), diagonal leg to (-2.2,-1.18), then east along y -1.18
mon_start(); MON["trace"] = []
zz_ok = True
try:
    # the hanging left gripper (0.25-0.3 m to the side) hit the scooter's wheel at (-2.2,-1.1) on the diagonal leg
    # (53 N): the diagonal leg ends west of the scooter's box at (-2.3,-1.24); the arms are tucked (grippers 0.17 m to
    # the side) only for the east leg past the scooter, then released
    for zz_i, zz_wp in enumerate([(-2.3, -1.24), (-1.45, -1.18)]):
        if zz_i == 1:
            TUCK_JOINTS = True
        zz_turn_to(zz_wp)
        walk_via([zz_wp], seg=0.30)
        print("at", zz_wp, state(), flush=True)
    TUCK_JOINTS = False
except Abort as ex:
    zz_ok = False; print("TRANSIT ABORT", ex)
MON["on"] = False
print("transit", zz_ok, state(), "trace", MON["trace"][::6])
MON["trace"] = None
print(look3("transit_east"))
if zz_ok:
    zz_gr = go_item()
