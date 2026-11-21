# Slab push (umbrella r106: a flat convex slab 0.033 m thick, 0.45 kg), AI-operated, run 1120_093820_dex1_floor_12.
# Closed jaws fingers down as a paddle at pad height ~0.016 from a deep squat, pushed in short hand steps along u through
# the slab's centre, stop at the arm's reach / no progress / slab turning; hand back + up, stand, rest_hands.
from scipy.spatial import ConvexHull as _CHs
UMB = body_of("r106i1_umbrella")


def slab_hull(b_=None):
    b_ = b_ or UMB; zid_ = m.body(b_).id
    for g_ in range(m.ngeom):
        if m.geom_bodyid[g_] == zid_ and m.geom_contype[g_]:
            mid_ = m.geom_dataid[g_]; a_ = m.mesh_vertadr[mid_]; n_ = m.mesh_vertnum[mid_]
            V_ = m.mesh_vert[a_:a_ + n_] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_]
            h_ = _CHs(V_[:, :2])
            return V_[h_.vertices, :2], h_.equations


def slab_yaw(b_=None):
    R_ = d.xmat[m.body(b_ or UMB).id].reshape(3, 3)
    return float(np.degrees(np.arctan2(R_[1, 0], R_[0, 0])))


def slab_entry(a, u, b_=None):
    """First point of the line a + t u (t from -1.5) inside the slab hull, and t."""
    P_, E_ = slab_hull(b_)
    for t_ in np.arange(-1.5, 1.5, 0.004):
        p_ = a + u * t_
        if np.all(E_[:, :2] @ p_ + E_[:, 2] <= 0):
            return p_, t_
    return None, None


def ahead_of_pelvis(p_):
    pb_, yaw_ = base()
    return float((np.asarray(p_[:2]) - pb_[:2]) @ np.array([np.cos(yaw_), np.sin(yaw_)]))


def slab_push(side, u, along, z=0.008, step=0.03, n=14, reach=0.48, poses=((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8), (-0.40, 0.85)), stand=True, gap=0.03, sn=3):
    b_ = UMB; u = np.asarray(u, float) / np.linalg.norm(u); cd_ = np.array([-u[1], u[0]])
    Q_ = {side: q_(R_down(cd_))}; log_ = []; out_ = dict(c0=np.round(centre(b_)[:2], 3).tolist(), yaw0=round(slab_yaw(b_), 1))
    mon_start(target=None); MON["ignore"] = {m.body(b_).id}; MON["ignore_names"] = (b_,)
    try:
        PRE_ACTION("close_jaws", dict(side=side)); close_jaws(side, 10.0, T=0.6)
        if base()[0][2] > 0.55:
            for hh_, ll_ in poses:
                PRE_ACTION("squat", dict(h=hh_, l=ll_)); crouch(hh_, ll_, T=1.2)
        a_ = np.asarray(along, float)
        e_, t_ = slab_entry(a_, u)
        if e_ is None:
            raise Abort("push line misses the slab")
        p0_ = e_ - u * gap
        out_["entry"] = np.round(e_, 3).tolist(); out_["p0_ahead"] = round(ahead_of_pelvis(p0_), 3)
        PRE_ACTION("hand_above", {}); servo_pads(side, p0_, 0.20, Q_, speed=0.10, n=2)
        PRE_ACTION("hand_down", {}); out_["e_down"] = np.round(servo_pads(side, p0_, z, Q_, speed=0.05, n=3), 3).tolist()
        for k_ in range(n):
            c0_ = centre(b_)[:2].copy()
            tgt_ = pad_mid(side)[:2] + u * step
            if ahead_of_pelvis(tgt_) > reach:
                log_.append(("reach", round(ahead_of_pelvis(tgt_), 3))); break
            PRE_ACTION("push", dict(k=k_)); servo_pads(side, tgt_, z, Q_, speed=0.04, n=sn)
            c1_ = centre(b_)[:2]
            log_.append((k_, round(float((c1_ - c0_) @ u), 3), round(slab_yaw(b_), 1), round(float(pad_mid(side)[2]), 3)))
            if k_ > 3 and all(abs(l_[1]) < 0.002 for l_ in log_[-3:] if isinstance(l_[0], int)):
                log_.append("no progress"); break
        hp_ = pad_mid(side)
        PRE_ACTION("hand_back", {}); servo_pads(side, hp_[:2] - u * 0.04, hp_[2] + 0.01, Q_, speed=0.03, n=2); op.run(0.5)
        PRE_ACTION("hand_up", {}); servo_pads(side, hp_[:2] - u * 0.08, 0.25, Q_, speed=0.08, n=2)
        if stand:
            PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2)
        rest_hands((side,))
        out_["ok"] = True
    except Abort as ex_:
        out_["ok"] = False; log_.append(str(ex_)[:300])
    MON["on"] = False
    out_.update(c1=np.round(centre(b_)[:2], 3).tolist(), yaw1=round(slab_yaw(b_), 1), log=log_, state=state(), fell=fallen())
    return out_


print("[slab] slab_hull, slab_yaw, slab_entry, slab_push loaded", flush=True)
