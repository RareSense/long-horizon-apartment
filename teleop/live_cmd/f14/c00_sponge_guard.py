# Two-hand jaw-base squeeze guard for the sponges r83i1 (coordinator's rule, AI-operated): island_skills.two_hand_pick
# calls hold_on(side, name, 0.5); the grasp-QC guard refuses it (the jaw BASES press, the fingers do not touch). Here
# hold_on for THIS thing is replaced: it holds (guard=False) only when BOTH hands' solver contact force on the box is
# > 5 N each and nothing but the two hands touches it; the check is logged (SPONGE_CHECK, EVENTS) and a close-up saved.
import mujoco as _mjc
_HOLD_ORIG = globals().get("_HOLD_ORIG") or hold_on
SPONGE_CHECK = []
SPONGE = body_of("r83i1_sponges")


def two_squeeze_forces(name):
    """Solver contact forces on `name` per touching body: {'left': N, 'right': N, 'others': {name: N}}."""
    M_, D_ = br.mjm, br.mjd; sb = br.sb_of_ib; gb = br.geom_body; bb = m.body(name).id
    f6 = np.zeros(6); out = dict(left=0.0, right=0.0, others={}, n_left=0, n_right=0)
    for i_ in range(int(D_.ncon)):
        c_ = D_.contact[i_]
        b0, b1 = int(sb[gb[int(c_.geom[0])]]), int(sb[gb[int(c_.geom[1])]])
        if bb not in (b0, b1) or float(c_.dist) > 0.001:
            continue
        o_ = b1 if b0 == bb else b0
        _mjc.mj_contactForce(M_, D_, i_, f6)
        fn_ = abs(float(f6[0]))
        on_ = m.body(o_).name if o_ > 0 else "static"
        low_ = on_.lower()
        hand_ = ("dex1" in low_ or "wrist" in low_ or "hand" in low_)
        if hand_ and low_.startswith("left"):
            out["left"] += fn_; out["n_left"] += 1
        elif hand_ and low_.startswith("right"):
            out["right"] += fn_; out["n_right"] += 1
        else:
            out["others"][on_] = round(out["others"].get(on_, 0.0) + fn_, 2)
    out["left"] = round(out["left"], 2); out["right"] = round(out["right"], 2)
    return out


def hold_on(s, name, share=1.0, guard=True):
    if name != SPONGE:
        return _HOLD_ORIG(s, name, share, guard=guard)
    f_ = two_squeeze_forces(name)
    ok_ = bool(f_["left"] > 5.0 and f_["right"] > 5.0 and not f_["others"])
    rec_ = dict(t=round(float(d.time), 2), side=s, obj=name, forces=f_, ok=ok_)
    try:
        c_ = centre(name); p_, yw_ = base(); fw_ = RM.rz(yw_)[:, 0]
        eye_ = c_ + np.r_[0.55 * fw_[:2], 0.0] + np.array([0.0, 0.0, 0.35])
        rec_["look"] = close(os.path.join(RUN, "grasps", f"two_squeeze_{name}_{s}_t{int(d.time)}.jpg"), eye_, c_, f"two-hand squeeze {name} {s} L {f_['left']} N R {f_['right']} N others {f_['others']} (AI-operated)")
    except Exception as ex_:
        rec_["look_err"] = str(ex_)[:120]
    SPONGE_CHECK.append(rec_)
    EVENTS.append(dict(t=rec_["t"], ev="two-hand squeeze check", obj=name, side=s, forces=f_, ok=ok_))
    print("[two-squeeze]", rec_, flush=True)
    if not ok_:
        HOLD_REFUSED.append(dict(t=rec_["t"], side=s, obj=name, why=f"two-hand squeeze check failed {f_}"))
        raise RuntimeError(f"two-hand squeeze check failed on {s}: {f_}")     # two_hand_pick ignores hold_on's return
    return _HOLD_ORIG(s, name, share, guard=False)


os.makedirs(os.path.join(RUN, "grasps"), exist_ok=True)
print("[two-squeeze] hold_on wrapped for", SPONGE, "forces now", two_squeeze_forces(SPONGE), flush=True)
