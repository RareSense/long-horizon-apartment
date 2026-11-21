SIDE = "left"; U = np.array([-1.0, 0.0])
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
try:
    hp_ = pad_mid(SIDE)
    PRE_ACTION("hand_up", {}); servo_pads(SIDE, hp_[:2] - U * 0.06, 0.25, QT, speed=0.08, n=2)
    PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2); open_jaws(SIDE, T=0.3)
    rest_hands(SIDES)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
print("state", state(), flush=True)
C_, c_, z0_, z1_ = flat_corners(UMB)
print("corners", np.round(C_, 3).tolist(), "centre", np.round(c_, 3).tolist(), "yaw", round(slab_yaw(), 1), flush=True)
for k_ in range(4):
    for sd_ in ("left", "right"):
        for pl_ in corner_pinch_plan(UMB, k_, sd_, 0.03):
            st_ = pl_["stance"]
            print(k_, sd_, "corner", np.round(pl_["corner"], 3).tolist(), "stance", [round(st_[0], 2), round(st_[1], 2), round(np.degrees(st_[2]))], "free", pl_["free"], flush=True)
