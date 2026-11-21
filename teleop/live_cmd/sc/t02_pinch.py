exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
MON["on"] = False
LD = os.path.join(RUN, "checkpoints", "0095_item_r107i1_umbrella"); exec(open(r"C:SERSARESENSESIM_HOMEPARTMENTiVE_CMDSCd.PY", ENCODING="UTF-8").READ())
b_ = body_of("r100i1_towel")
C_, cc_, z0_, z1_ = flat_corners(b_)
print("corners", np.round(C_, 3).tolist(), "c", np.round(cc_, 3).tolist(), "z", round(z0_, 3), round(z1_, 3), flush=True)
k_ = int(np.argmin(C_[:, 0] + C_[:, 1]))                     # the SW corner (overhangs the stool, nothing under it)
X_ = C_[k_]; n_ = len(C_); e1_ = C_[(k_ + 1) % n_] - X_; e2_ = C_[(k_ - 1) % n_] - X_
w_ = e1_ / np.linalg.norm(e1_) + e2_ / np.linalg.norm(e2_); w_ /= np.linalg.norm(w_)
G_ = X_ + w_ * 0.02
sd_ = "left"; yaw_ = 0.0
st_ = (float(G_[0] - 0.30), float(G_[1] - 0.24), 0.0)   # facing EAST from the west: the corner 0.30 ahead, 0.24 left. SEEN t02 try 1: facing north from (-0.86,1.01) the right knee went into the stool legs (134 N)
print("corner", np.round(X_, 3).tolist(), "G", np.round(G_, 3).tolist(), "stance", np.round(st_, 3).tolist(), "free", with_tight(lambda: room_grid((b_,)).free(np.array(st_[:2]))), flush=True)
mon_start(target=b_); o_ = {}
try:
    back_off_container()
    o_["walk"] = walk_tight(st_).get("err_xy")
    open_jaws(sd_, T=0.3)
    cd_ = np.r_[-w_[1], w_[0], 0.0]; lat_ = RM.rz(base()[1])[:, 1]; cd_ = cd_ if cd_ @ lat_ >= 0 else -cd_
    Q_ = {sd_: q_(R_down(cd_))}
    PRE_ACTION("hand_above", {}); o_["e_above"] = np.round(servo_pads(sd_, G_, z1_ + 0.06, Q_, speed=0.12), 3).tolist()
    PRE_ACTION("hand_down", {}); o_["e_down"] = np.round(servo_pads(sd_, G_, z0_ + 0.011, Q_, speed=0.05), 3).tolist()
    zc_, tc_ = float(centre(b_)[2]), box_tilt_deg(b_)
    PRE_ACTION("close", {}); close_jaws(sd_, 10.0, T=0.8)
    o_["grip"] = {k: v for k, v in grip_check(sd_, None, min_gap=0.004).items() if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
    o_["fingers"] = len(jaw_fingers_on(sd_, b_)); o_["dz"] = round(float(centre(b_)[2]) - zc_, 4); o_["dtilt"] = round(abs(box_tilt_deg(b_) - tc_), 1)
    o_["look_hold"] = look_hold(b_, sd_)
    print("PINCH", o_, flush=True)
    if o_["grip"]["ok"] and o_["fingers"] == 2 and o_["dz"] < 0.005 and o_["dtilt"] < 10 and hold_on(sd_, b_) is not False:
        MON["held"][sd_] = b_; MON["target"] = None; MON["last_touch"][sd_] = float(d.time)
        hp_ = ts.ee_pose(sd_)[0]
        PRE_ACTION("lift", {}); op.move({sd_: [hp_[0], hp_[1], hp_[2] + 0.10]}, speed=0.06, quats=Q_, timeout=3.0, tol=0.008); op.run(0.5)
        o_["rose"] = round(float(centre(b_)[2]) - zc_, 3); o_["tilt_after"] = round(box_tilt_deg(b_), 1)
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
print("RES", o_, "state", state(), "towel", np.round(centre(b_), 3).tolist(), "touch", finger_touch(sd_, b_), flush=True)
c_ = centre(b_)
print(close(os.path.join(LK, "t02_pinch.jpg"), np.r_[c_[0] - 0.8, c_[1] - 0.9, 1.3], c_, "towel pinched"), flush=True)
