for _f in ("route_v3_setup.py", "teleop.py", "autorun.py", "aside.py", "ops.py", "scooter.py"):
    exec(open(r"E:\urc_home\scripts\home\live\\" + _f, encoding="utf-8").read())
CHAIN = r"C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece"
ZZ_CK = r"C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\0237_act_transit_east_ok"
GARMENTS_FIRST = ["r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket", "r117i1_blanket", "r116i1_coat_pile", "r190i1_stocking", "r68i1_rag"]


def gait_on():
    """home-gait eb5a8a3 (merged 8001a76): the gait's position hold ON, arms at rest (coordinator 19 Nov ~23:55); the
    session settings of the hand-over too. Call after every load (a checkpoint may bring the gait settings back)."""
    global TUCK_JOINTS, STANCE_LOW_ROOM, STANCE_FUR_ROOM
    TUCK_JOINTS = False
    STANCE_LOW_ROOM, STANCE_FUR_ROOM = 0.35, 0.32
    ts.loco.g["hold"] = False             # home-gait 7556985 safe settings: hold OFF (it still tips turns at 0237)
    globals()["ARM_TUCK"] = dict(pitch=0.05, roll=0.15, yaw=0.0, elbow=0.6)
    # the hold's own state is not in older checkpoints: a stale anchor from before a load would pull the robot back
    # toward a place it never was
    lo_ = ts.loco
    lo_.anc = None; lo_.d_corr = np.zeros(2); lo_.d_corr_st = np.zeros(2); lo_._hold_steps = []; lo_._hold_acc = [np.zeros(2), 0]; lo_.hold_err = np.zeros(2)
    if hasattr(lo_, "_hold_off"):
        lo_._hold_off = np.zeros(2)
    return {k_: ts.loco.g[k_] for k_ in ts.loco.g if k_.startswith("hold")}


zz_m = route_v3_resume(CHAIN)
print(gait_on())
print(floor_first(GARMENTS_FIRST))
print(state(), kit_mem())
