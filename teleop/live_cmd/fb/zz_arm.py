# Arm helpers in the robot frame (AI-operated teleop).
def zz_rf(v):
    """Robot-frame point (ahead, left, up from the floor under the pelvis) -> world."""
    p_, y_ = base()
    return np.r_[p_[:2], 0.0] + RM.rz(y_) @ np.asarray(v, float)


def zz_to_rf(pw):
    p_, y_ = base()
    return RM.rz(y_).T @ (np.asarray(pw, float) - np.r_[p_[:2], 0.0])


def zz_pads_to(sd, target_w, Q=None, speed=0.12, n=3, step=0.12, tag=None, timeout=4.0):
    """Pad middle of hand sd to a world point, in moves of at most `step` (closed loop on the pads). Q: {sd: quat} or
    None = orientation free."""
    PRE_ACTION("zz_pads_to", dict(side=sd, target=np.round(target_w, 3).tolist()))
    target_w = np.asarray(target_w, float)
    for k_ in range(40):
        mid_ = pad_mid(sd); e_ = target_w - mid_; n_e = float(np.linalg.norm(e_))
        if n_e < 0.006:
            break
        mv_ = e_ if n_e <= step else e_ * (step / n_e)
        hp_ = ts.ee_pose(sd)[0]
        if Q is None:
            op.move({sd: (hp_ + mv_).tolist()}, speed=speed, timeout=timeout, tol=0.008)
        else:
            op.move({sd: (hp_ + mv_).tolist()}, speed=speed, quats=Q, timeout=timeout, tol=0.008)
        op.run(0.15)
        if float(np.linalg.norm(pad_mid(sd) - mid_)) < 0.004 and n_e > 0.01:      # stalled
            break
    e_ = target_w - pad_mid(sd)
    return dict(err=np.round(e_, 3).tolist(), pad=np.round(pad_mid(sd), 3).tolist(), pad_rf=np.round(zz_to_rf(pad_mid(sd)), 3).tolist(), tilt=round(pelvis_tilt(), 3))


def zz_R(fdir, cdir):
    """Gripper orientation: fingers along fdir, jaws closing along cdir (world vectors; cdir made perpendicular)."""
    x_ = np.asarray(fdir, float); x_ = x_ / np.linalg.norm(x_)
    y_ = np.asarray(cdir, float); y_ = y_ - (y_ @ x_) * x_; y_ = y_ / np.linalg.norm(y_)
    return np.column_stack([x_, y_, np.cross(x_, y_)])


def zz_bunch(z, dz=0.04):
    """Cross-section of the hanging blanket at height z: centre, extents (world x, y) and count."""
    P_ = zz_w().points(0); s_ = np.abs(P_[:, 2] - z) < dz
    if not s_.any():
        return None
    return dict(n=int(s_.sum()), c=np.round(P_[s_, :2].mean(0), 3).tolist(), lo=np.round(P_[s_, :2].min(0), 3).tolist(), hi=np.round(P_[s_, :2].max(0), 3).tolist())


print("[zz] arm helpers loaded", flush=True)
