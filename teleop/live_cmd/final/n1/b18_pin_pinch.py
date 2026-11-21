zz_b = body_of("r196i1_plastic_bag"); SD = "left"; PN = "right"
C_, c_, z0_, z1_ = flat_corners(zz_b)
pl_ = corner_pinch_plan(zz_b, 3, SD)[0]
X_ = pl_["corner"]; G_ = pl_["G"]; w_ = (G_ - X_) / np.linalg.norm(G_ - X_)
P_ = X_ + w_ * 0.10
o_ = dict(G=np.round(G_, 3).tolist(), P=np.round(P_, 3).tolist(), top=round(z1_, 4))
mon_start(target=zz_b); MON["ignore_names"] = (zz_b,)
try:
    QP_ = {PN: q_(R_down(np.r_[pl_["cd"], 0.0] if len(pl_["cd"]) == 2 else pl_["cd"]))}
    close_jaws(PN, 10.0, T=0.3)
    PRE_ACTION("pin_hand_above", {}); op.move({PN: [P_[0], P_[1], 0.30]}, speed=0.15, quats=QP_, timeout=3.0, tol=0.03); op.run(0.3)
    open_jaws(SD, T=0.3)
    PRE_ACTION("crouch", dict(CROUCH)); crouch(T=1.8, **CROUCH)
    PRE_ACTION("pin_down", {})
    o_["pin_above"] = np.round(servo_pads(PN, P_, z1_ + 0.05, QP_, speed=0.1, n=2), 3).tolist()
    o_["pin"] = np.round(servo_pads(PN, P_, z1_ + 0.010, QP_, speed=0.03, n=2), 3).tolist()
    o_["pin_F"] = round(float(sum(finger_touch(PN, zz_b).values())) if finger_touch(PN, zz_b) else 0.0, 2)
    o_["bag_after_pin"] = np.round(centre(zz_b), 3).tolist()
    Q_ = {SD: q_(R_down(pl_["cd"]))}
    PRE_ACTION("servo_pads", {}); o_["e_above"] = np.round(servo_pads(SD, G_, z1_ + 0.06, Q_, speed=0.2), 4).tolist()
    PRE_ACTION("servo_pads", {}); o_["e_down"] = np.round(servo_pads(SD, G_, 0.0255, Q_, speed=0.06), 4).tolist()
    c0_ = centre(zz_b).copy()
    PRE_ACTION("close_jaws", {}); close_jaws(SD, 8.0, T=1.2)
    g_ = grip_check(SD, None, min_gap=0.003)
    o_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
    o_["fingers_on"] = len(jaw_fingers_on(SD, zz_b)); o_["moved"] = round(float(np.linalg.norm(centre(zz_b)[:2] - c0_[:2])), 3)
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
print("OUT", o_, "bag", np.round(centre(zz_b), 3).tolist(), "state", state(), "fell", fallen(), flush=True)
print(look_hand(SD, "n1_bag_pin"), flush=True)
