def repinch(side="left", k=1, s=0.020, force=14.0):
    pl_ = corner_pinch_plan(UMB, k, side, s)[0]; G_ = pl_["G"]; Q_ = {side: q_(R_down(pl_["cd"]))}
    open_jaws(side, T=0.3)
    hp_ = pad_mid(side)
    servo_pads(side, hp_[:2], 0.06, Q_, speed=0.05, n=2)
    servo_pads(side, G_, 0.06, Q_, speed=0.05, n=3)
    e_ = servo_pads(side, G_, 0.016, Q_, speed=0.04, n=3)
    PRE_ACTION("pinch_close", {}); close_jaws(side, force, T=0.8)
    return Q_, np.round(e_, 4).tolist(), [c_ for c_ in umb_contacts() if c_[0] != "world"]


def lead_push(side, w, Q, n=6, lead=0.06, z=0.018, reach=0.40, T=1.5):
    w = np.asarray(w, float) / np.linalg.norm(w); log_ = []
    for k_ in range(n):
        c0_ = centre(UMB)[:2].copy(); p0_ = pad_mid(side).copy()
        hp_ = ts.ee_pose(side)[0]
        if ahead_of_pelvis(p0_[:2] + w * lead * 0.5) > reach:
            log_.append(("reach", round(ahead_of_pelvis(p0_), 3))); break
        tgt_ = hp_ + np.r_[w * lead, z - p0_[2]]
        PRE_ACTION("lead_push", dict(k=k_)); op.move({side: tgt_.tolist()}, speed=0.04, quats=Q, timeout=T, tol=0.004)
        cc_ = [c_ for c_ in umb_contacts() if c_[0] != "world"]
        log_.append((k_, "slab", round(float((centre(UMB)[:2] - c0_) @ w), 3), "hand", round(float((pad_mid(side)[:2] - p0_[:2]) @ w), 3), "z", round(float(pad_mid(side)[2]), 3), "F", round(sum(c_[3] for c_ in cc_), 1), sorted(set(c_[0] for c_ in cc_)), "ahead", round(ahead_of_pelvis(pad_mid(side)), 3)))
        if not cc_:
            log_.append("lost contact"); break
    return log_


SIDE = "left"
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
try:
    QP, e_, cc_ = repinch(SIDE)
    print("repinch e", e_, "contacts", cc_, flush=True)
    C_, c_, z0_, z1_ = flat_corners(UMB); W_ = pad_mid(SIDE)[:2] - C_[1]; W_ /= np.linalg.norm(W_)
    L_ = lead_push(SIDE, W_, QP)
except Abort as ex_:
    L_ = ["ABORT " + str(ex_)[:300]]
MON["on"] = False
for l_ in L_:
    print(" ", l_, flush=True)
print("umb", np.round(centre(UMB)[:2], 3).tolist(), "yaw", round(slab_yaw(), 1), "state", state(), flush=True)
