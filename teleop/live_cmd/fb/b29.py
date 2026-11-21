def zz_knees():
    hc_ = obj_rect(zz_hb()).c
    out_ = {}
    for n_ in ("left_knee_link", "right_knee_link", "left_ankle_roll_link", "right_ankle_roll_link", "pelvis"):
        p_ = d.xpos[m.body(n_).id]
        out_[n_.replace("_link", "")] = (round(float(np.linalg.norm(p_[:2] - hc_)) - 0.257, 3), round(float(p_[2]), 3))
    return out_
print("before", zz_knees(), "pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), flush=True)
for zz_h, zz_l in ZZ_POSE:
    PRE_ACTION("zz_pose", dict(height=zz_h, lean=zz_l))
    op.send(dict(cmd="posture", height=float(zz_h), lean=float(zz_l), duration=1.2)); op.run(1.8)
    print("pose", zz_h, zz_l, zz_knees(), "pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "pad", np.round(pad_mid("right"), 3).tolist(), "touch", contact_report(), "fell", fallen(), flush=True)
