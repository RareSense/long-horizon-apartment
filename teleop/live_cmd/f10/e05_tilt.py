def zz_tl():
    R_ = d.xmat[m.body("pelvis").id].reshape(3, 3); return round(float(np.arccos(np.clip(R_[2, 2], -1, 1))), 3)
PRE_ACTION("posture_test", {})
op.send(dict(cmd="posture", height=H_WALK, lean=0.0, duration=1.0)); op.run(1.5)
print("at H_WALK", state()["pelvis"], "pelvis tilt", zz_tl(), "waist", round(float(d.qpos[m.jnt_qposadr[m.joint("waist_pitch_joint").id]]), 3), "legs", np.round(d.qpos[7:19], 2).tolist(), flush=True)
