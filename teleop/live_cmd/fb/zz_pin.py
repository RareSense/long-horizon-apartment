def zz_in_pads(sd, ip):
    """Particle ip relative to the middle between the pads of hand sd: [along the closing axis, along the fingers, across] m,
    and the half distance between the pad centres."""
    a_, b_ = pads(sd); mid_ = (a_ + b_) / 2; ax_ = (b_ - a_); L_ = float(np.linalg.norm(ax_)); ax_ = ax_ / L_
    Rn_ = ts.ee_pose(sd)[1]; f_ = Rn_[:, 0]; f_ = f_ - (f_ @ ax_) * ax_; f_ = f_ / np.linalg.norm(f_)
    c_ = np.cross(ax_, f_)
    v_ = zz_w().points(0)[ip] - mid_
    return np.round([v_ @ ax_, v_ @ f_, v_ @ c_], 3).tolist(), round(L_ / 2, 3)


def zz_step_to(sd, ip, Q, maxs=0.04, speed=0.05, off=(0.0, 0.0, 0.0)):
    """One hand move of at most maxs: the pad middle toward particle ip (+ a world offset)."""
    tgt_ = zz_w().points(0)[ip] + np.asarray(off, float)
    e_ = tgt_ - pad_mid(sd); n_ = float(np.linalg.norm(e_))
    if n_ > maxs:
        e_ = e_ * (maxs / n_)
    PRE_ACTION("zz_step_to", dict(side=sd, ip=int(ip), d=np.round(e_, 3).tolist()))
    hp_ = ts.ee_pose(sd)[0]
    op.move({sd: (hp_ + e_).tolist()}, speed=speed, quats=Q, timeout=3.0, tol=0.006); op.run(0.3)
    cg_ = zz_w().caught(sd)
    return dict(left=round(float(np.linalg.norm(zz_w().points(0)[ip] + np.asarray(off, float) - pad_mid(sd))), 3), in_pads=zz_in_pads(sd, ip), caught=len(cg_),
                caught_uv=np.round(zz_uv()[cg_].mean(0), 3).tolist() if len(cg_) else None, C_rf=np.round(zz_to_rf(zz_w().points(0)[ip]), 3).tolist(),
                pad_rf=np.round(zz_to_rf(pad_mid(sd)), 3).tolist(), tilt=round(pelvis_tilt(), 3), touch=contact_report()["body"])


print("[zz] pin helpers loaded", flush=True)
