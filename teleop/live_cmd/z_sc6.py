import glob as _gl
zz_ck = sorted(_gl.glob(r"C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\*_act_sc_hold"))[-1]
ck_load(zz_ck); print("loaded", zz_ck)
MON["on"] = False
zz_b = body_of("r126i1_scooter")
def zz_st(tag):
    lo_, hi_ = obj_box(zz_b)
    tilt = float(np.degrees(np.arccos(np.clip(obj_pos(zz_b)[1][2, 2], -1, 1))))
    print(tag, "t", round(float(d.time), 2), "pel", np.round(base()[0], 3).tolist(),
          "touch", {s_: sum(finger_touch(s_, zz_b).values()) for s_ in SIDES}, "lost", {s_: bool(HOLD.lost(s_)) for s_ in SIDES},
          "err", {s_: round(HOLD.items[s_]["err"], 4) for s_ in SIDES if s_ in HOLD.items},
          "sc lo", round(float(lo_[2]), 4), "tilt", round(tilt, 1), "padsz", {s_: round(float(pad_mid(s_)[2]), 3) for s_ in SIDES}, "gap", {s_: round(gap(s_), 4) for s_ in SIDES}, flush=True)
sc_hold(zz_b)
for s_ in SIDES:
    jaw_target[s_] = 0.0; jaw_force[s_] = 14.0
for _k in range(4):
    op.run(0.25); zz_st(f"held {_k}")
zz_l = sc_lift(zz_b, dz=0.03)
print("lift", zz_l)
for _k in range(4):
    op.run(0.25); zz_st(f"lifted {_k}")
