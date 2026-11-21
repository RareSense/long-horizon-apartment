SIDE = "left"; K_SE = 1
pl_ = corner_pinch_plan(UMB, K_SE, SIDE, 0.03)[0]
print("plan", np.round(pl_["stance"], 3).tolist(), "G", np.round(pl_["G"], 3).tolist(), flush=True)
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
o_ = {}
try:
    w_ = walk_tight(pl_["stance"])
    o_["walk_err"] = w_.get("err_xy") if isinstance(w_, dict) else str(w_)[:100]
    pl2_ = corner_pinch_plan(UMB, K_SE, SIDE, 0.03)[0]
    G_ = pl2_["G"]; CDp = pl2_["cd"]; QP = {SIDE: q_(R_down(CDp))}
    open_jaws(SIDE, T=0.3)
    PRE_ACTION("squat", {}); crouch(T=1.8, **CROUCH)
    o_["G_ahead"] = round(ahead_of_pelvis(G_), 3)
    o_["e_above"] = np.round(servo_pads(SIDE, G_, 0.09, QP, speed=0.2), 4).tolist()
    o_["e_down"] = np.round(servo_pads(SIDE, G_, 0.016, QP, speed=0.06), 4).tolist()
    PRE_ACTION("pinch_close", {}); close_jaws(SIDE, 14.0, T=0.8)
    g_ = grip_check(SIDE, None, min_gap=0.004)
    o_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
    o_["umb_contacts"] = [c_ for c_ in umb_contacts() if c_[0] != "world"]
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(state=state(), umb=np.round(centre(UMB)[:2], 3).tolist())
print("PINCH", o_, flush=True)
pm_ = pad_mid(SIDE)
print(close(os.path.join(TELE_DIR, "f12_e01_pinch.jpg"), np.r_[pm_[:2] + np.array([0.25, -0.30]), 0.25], np.r_[pm_[:2], 0.01], "pinch"), flush=True)
