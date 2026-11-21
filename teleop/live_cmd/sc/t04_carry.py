MON["on"] = False
b_ = body_of("r100i1_towel"); sd_ = "left"; hb_ = body_of("r133i1_laundry_basket")
mon_start(target=None); MON["held"][sd_] = b_; MON["last_touch"][sd_] = float(d.time)
o_ = {}
try:
    Q_ = {sd_: q_(ts.ee_pose(sd_)[1])}
    hp_ = ts.ee_pose(sd_)[0]
    if hp_[2] < 0.80:
        PRE_ACTION("lift2", {}); op.move({sd_: [hp_[0], hp_[1], hp_[2] + 0.12]}, speed=0.06, quats=Q_, timeout=3.0, tol=0.01); op.run(0.5)
    p_, y_ = base()
    if p_[0] > -1.6:
        PRE_ACTION("back_from_stool", {}); walk((float(p_[0] - 0.30), float(p_[1]), float(y_)), carry=(sd_,))
    lo_c, hi_c = obj_box(hb_); hc_ = (lo_c[:2] + hi_c[:2]) / 2
    p_, y_ = base(); Rt_ = RM.rz(y_)[:2, :2].T
    Vt_ = _hull_pts(b_); tc_ = (Vt_[:, :2].min(0) + Vt_[:, :2].max(0)) / 2; lo_t = Vt_.min(0)
    rel_ = Rt_ @ (tc_ - p_[:2])                                 # towel centre in the robot frame (fixed by the hold)
    o_["towel_rel"] = np.round(rel_, 3).tolist(); o_["towel_low"] = round(float(lo_t[2]), 3)
    g_ = with_tight(lambda: room_grid((b_,)))
    cands_ = []
    for h_ in np.radians(np.arange(-180, 180, 15)):
        P_ = hc_ - RM.rz(h_)[:2, :2] @ rel_
        if g_.free(P_):
            cands_.append((float(np.linalg.norm(P_ - p_[:2])), float(h_), P_))
    o_["n_cands"] = len(cands_)
    if not cands_:
        raise Abort("no stance at the hamper for the towel")
    cands_.sort(key=lambda c: c[0])
    o_["stance"] = [round(float(cands_[0][2][0]), 3), round(float(cands_[0][2][1]), 3), round(cands_[0][1], 3)]
    print("plan", o_, flush=True)
    for c_ in cands_:
        st_ = (float(c_[2][0]), float(c_[2][1]), c_[1])
        try:
            w_ = walk_tight(st_, carry=(sd_,)); o_["stance"] = np.round(st_, 3).tolist(); o_["walk"] = w_.get("err_xy"); break
        except RuntimeError as ex_:
            print("no path", np.round(st_, 3).tolist(), str(ex_)[:60], flush=True)
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
print("CARRY", o_, "state", state(), "touch", finger_touch(sd_, b_), "towel hull lo/hi", np.round(_hull_pts(b_).min(0), 3).tolist(), np.round(_hull_pts(b_).max(0), 3).tolist(), flush=True)
print(look3("t04_at_hamper"), flush=True)
