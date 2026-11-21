import mujoco as _mj
def umb_contacts(bid_name=None):
    M_, D_ = br.mjm, br.mjd
    zid_ = M_.body(bid_name or UMB).id; out_ = []
    for i_ in range(D_.ncon):
        c_ = D_.contact[i_]; b1_ = M_.geom_bodyid[c_.geom1]; b2_ = M_.geom_bodyid[c_.geom2]
        if zid_ not in (b1_, b2_):
            continue
        f6_ = np.zeros(6); _mj.mj_contactForce(M_, D_, i_, f6_)
        other_ = b2_ if b1_ == zid_ else b1_
        n_ = c_.frame[:3] * (1 if b1_ == zid_ else -1)
        out_.append((M_.body(other_).name, np.round(c_.pos, 3).tolist(), np.round(n_, 2).tolist(), round(float(f6_[0]), 2)))
    return out_
SIDE = "left"; K_SE = 1
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
o_ = {}
try:
    open_jaws(SIDE, T=0.3)
    pl2_ = corner_pinch_plan(UMB, K_SE, SIDE, 0.03)[0]
    G_ = pl2_["G"]; CDp = pl2_["cd"]; QP = {SIDE: q_(R_down(CDp))}
    PRE_ACTION("squat", {}); crouch(-0.40, 0.85, T=1.2)
    o_["G_ahead"] = round(ahead_of_pelvis(G_), 3)
    o_["e_down"] = np.round(servo_pads(SIDE, G_, 0.016, QP, speed=0.05), 4).tolist()
    o_["pad"] = np.round(pad_mid(SIDE), 3).tolist()
    o_["umb_contacts"] = [c_ for c_ in umb_contacts() if "floor" not in c_[0] and c_[0] != "world"]
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(state=state(), umb=np.round(centre(UMB)[:2], 3).tolist())
print("DOWN", o_, flush=True)
print("all umb contacts", umb_contacts()[:8], flush=True)
pm_ = pad_mid(SIDE)
print(close(os.path.join(TELE_DIR, "f12_e02_down.jpg"), np.r_[pm_[:2] + np.array([0.30, -0.30]), 0.20], np.r_[pm_[:2], 0.01], "pinch down"), flush=True)
