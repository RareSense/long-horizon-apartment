def pinch_push(side, w, n=8, step=0.02, z=0.018, reach=0.40, Q=None):
    """Corner pinch held (jaws closed on the two side faces at the corner), hand moved INTO the slab along the corner
    bisector w: the wedge jams, the slab slides (AI-operated, run 1120_093820)."""
    w = np.asarray(w, float) / np.linalg.norm(w); log_ = []
    for k_ in range(n):
        c0_ = centre(UMB)[:2].copy()
        tgt_ = pad_mid(side)[:2] + w * step
        if ahead_of_pelvis(tgt_) > reach:
            log_.append(("reach", round(ahead_of_pelvis(tgt_), 3))); break
        PRE_ACTION("pinch_push", dict(k=k_)); servo_pads(side, tgt_, z, Q, speed=0.03, n=2)
        cc_ = [c_ for c_ in umb_contacts() if c_[0] != "world"]
        fsum_ = round(sum(c_[3] for c_ in cc_), 1); top_ = any(c_[2][2] > 0.5 or c_[2][2] < -0.5 for c_ in cc_)
        log_.append((k_, round(float((centre(UMB)[:2] - c0_) @ w), 3), round(slab_yaw(), 1), round(float(pad_mid(side)[2]), 3), fsum_, "TOP" if top_ else "", sorted(set(c_[0] for c_ in cc_))))
        if not cc_:
            log_.append("lost contact"); break
    return log_


SIDE = "left"
C_, c_, z0_, z1_ = flat_corners(UMB)
X_ = C_[1]; W_ = pad_mid(SIDE)[:2] - X_; W_ /= np.linalg.norm(W_)
pl2_ = corner_pinch_plan(UMB, 1, SIDE, 0.02)[0]; QP = {SIDE: q_(R_down(pl2_["cd"]))}
print("corner", np.round(X_, 3).tolist(), "w", np.round(W_, 3).tolist(), "deg", round(float(np.degrees(np.arctan2(W_[1], W_[0]))), 1), "pad ahead", round(ahead_of_pelvis(pad_mid(SIDE)), 3), flush=True)
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
try:
    L_ = pinch_push(SIDE, W_, Q=QP)
except Abort as ex_:
    L_ = ["ABORT " + str(ex_)[:300]]
MON["on"] = False
for l_ in L_:
    print(" ", l_, flush=True)
print("umb", np.round(centre(UMB)[:2], 3).tolist(), "yaw", round(slab_yaw(), 1), "state", state(), flush=True)
pm_ = pad_mid(SIDE)
print(close(os.path.join(TELE_DIR, "f12_e04_push.jpg"), np.r_[pm_[:2] + np.array([0.30, -0.30]), 0.30], np.r_[pm_[:2], 0.01], "pinch push"), flush=True)
