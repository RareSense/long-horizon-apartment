import mujoco as _mj
_BR_ID = {}
def br_body_id(name):
    if name not in _BR_ID:
        M_ = br.mjm
        _BR_ID[name] = next(i_ for i_ in range(M_.nbody) if M_.body(i_).name.endswith("_" + name) or M_.body(i_).name == name)
    return _BR_ID[name]


def br_short(i_):
    n_ = br.mjm.body(i_).name
    return n_.split("Geometry_")[-1].split("_")[-1] if "Dex1" in n_ or "link" in n_ else n_.split("Geometry_")[-1]


def umb_contacts(name=None):
    M_, D_ = br.mjm, br.mjd
    zid_ = br_body_id(name or UMB); out_ = []
    for i_ in range(D_.ncon):
        c_ = D_.contact[i_]; b1_ = M_.geom_bodyid[c_.geom1]; b2_ = M_.geom_bodyid[c_.geom2]
        if zid_ not in (b1_, b2_):
            continue
        f6_ = np.zeros(6); _mj.mj_contactForce(M_, D_, i_, f6_)
        other_ = b2_ if b1_ == zid_ else b1_
        n_ = c_.frame[:3] * (1 if b1_ == zid_ else -1)
        out_.append((br_short(other_), np.round(c_.pos, 3).tolist(), np.round(n_, 2).tolist(), round(float(f6_[0]), 2)))
    return out_
MON["on"] = False
print("[cmn] umb_contacts ok", [c_ for c_ in umb_contacts() if "static" not in c_[0]][:6], flush=True)
print("pad", np.round(pad_mid("left"), 3).tolist(), "state", state(), flush=True)
pm_ = pad_mid("left")
print(close(os.path.join(TELE_DIR, "f12_e02_down.jpg"), np.r_[pm_[:2] + np.array([0.30, -0.30]), 0.20], np.r_[pm_[:2], 0.01], "pinch down"), flush=True)
