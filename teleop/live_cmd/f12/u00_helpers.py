# Umbrella r106 two-corner pinch carry helpers (AI-operated, run 1120_093820_dex1_floor_12).
import mujoco as _mj
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\slab.py", encoding="utf-8").read())
_BR_ID = {}


def br_body_id(name):
    if name not in _BR_ID:
        M_ = br.mjm
        _BR_ID[name] = next(i_ for i_ in range(M_.nbody) if M_.body(i_).name.endswith("_" + name) or M_.body(i_).name == name)
    return _BR_ID[name]


def br_short(i_):
    n_ = br.mjm.body(i_).name
    if "_Dex1_" in n_:
        a_, b_ = n_.rsplit("_Dex1_", 1)
        return a_.split("_")[-1] + ":" + b_.replace("finger_link_", "f")
    return n_.split("Geometry_")[-1]


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


def pinch_ok(side, cc_):
    """Both fingers of this hand on the slab's SIDE faces (horizontal normals), none on its top."""
    mine_ = [c_ for c_ in cc_ if c_[0].startswith(side + ":")]
    fingers_ = set(c_[0] for c_ in mine_)
    top_ = [c_ for c_ in mine_ if abs(c_[2][2]) > 0.5]
    return len(fingers_) == 2 and not top_, dict(fingers=sorted(fingers_), N=round(sum(c_[3] for c_ in mine_), 1), top=len(top_))


def corner_points(s_in=0.02):
    """Corners (SW, SE, NE, NW by angle about the centre) with their grasp point s_in in along the bisector and the jaw
    closing direction (across the bisector)."""
    C_, c_, z0_, z1_ = flat_corners(UMB); n_ = len(C_); out_ = []
    for k_ in range(n_):
        X_ = C_[k_]; e1_ = C_[(k_ + 1) % n_] - X_; e2_ = C_[(k_ - 1) % n_] - X_
        w_ = e1_ / np.linalg.norm(e1_) + e2_ / np.linalg.norm(e2_); w_ /= np.linalg.norm(w_)
        out_.append(dict(X=X_, w=w_, G=X_ + w_ * s_in, cd=np.array([-w_[1], w_[0]])))
    return out_, c_


def edge_stance(kA, kB, back=0.17, s_in=0.02):
    """Standing pelvis facing the edge kA-kB (inward), its two grasp points 'back' ahead; which hand takes which."""
    P_, c_ = corner_points(s_in)
    GA_, GB_ = P_[kA]["G"], P_[kB]["G"]; M_ = (GA_ + GB_) / 2
    n_ = c_ - M_; n_ /= np.linalg.norm(n_)
    yaw_ = float(np.arctan2(n_[1], n_[0])); left_ = np.array([-n_[1], n_[0]])
    sideA_ = "left" if (GA_ - M_) @ left_ > 0 else "right"
    who_ = {sideA_: kA, ("right" if sideA_ == "left" else "left"): kB}
    st_ = M_ - n_ * back
    return (float(st_[0]), float(st_[1]), yaw_), who_, float(np.linalg.norm(GA_ - GB_))


print("[u00] umbrella two-corner helpers loaded", flush=True)
