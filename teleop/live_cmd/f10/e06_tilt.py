def zz_tl():
    R_ = d.xmat[m.body("pelvis").id].reshape(3, 3); return round(float(np.arccos(np.clip(R_[2, 2], -1, 1))), 3)
crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2)
print("stand", state()["pelvis"], "tilt", zz_tl(), flush=True)
op.send(dict(cmd="posture", height=H_WALK, lean=0.0, duration=1.0)); op.run(1.5)
print("H_WALK after crouch cycle", state()["pelvis"], "tilt", zz_tl(), flush=True)
c_ = ts.ctrl
print([k_ for k_ in vars(c_).keys()][:200], flush=True)
