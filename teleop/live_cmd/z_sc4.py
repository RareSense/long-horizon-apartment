ck_load(r"C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\0014_act_sc_hold")
MON["on"] = False
zz_b = body_of("r126i1_scooter")
def zz_st(tag):
    lo_, hi_ = obj_box(zz_b)
    print(tag, "t", round(float(d.time), 2), "pel", np.round(base()[0], 3).tolist(), "yaw", round(float(np.degrees(base()[1])), 1),
          "touch", {s_: finger_touch(s_, zz_b) for s_ in SIDES}, "hold", {s_: bool(HOLD.holding(s_)) for s_ in SIDES} if HOLD is not None else None,
          "sc lo", round(float(lo_[2]), 4), "pads", {s_: np.round(pad_mid(s_), 3).tolist() for s_ in SIDES}, "gap", {s_: round(gap(s_), 4) for s_ in SIDES}, flush=True)
zz_st("before hold")
sc_hold(zz_b)
op.run(0.3); zz_st("held 0.3")
op.run(0.5); zz_st("held 0.8")
print("jaw targets", dict(jaw_target), dict(jaw_force))
