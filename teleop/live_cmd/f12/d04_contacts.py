import mujoco as _mj
def umb_contacts():
    zid_ = m.body(UMB).id; out_ = []
    for i_ in range(d.ncon):
        c_ = d.contact[i_]; b1_ = m.geom_bodyid[c_.geom1]; b2_ = m.geom_bodyid[c_.geom2]
        if zid_ not in (b1_, b2_):
            continue
        f6_ = np.zeros(6); _mj.mj_contactForce(m, d, i_, f6_)
        other_ = b2_ if b1_ == zid_ else b1_
        n_ = c_.frame[:3] * (1 if b1_ == zid_ else -1)
        out_.append((m.body(other_).name, np.round(c_.pos, 3).tolist(), np.round(n_, 2).tolist(), round(float(f6_[0]), 2)))
    return out_
SIDE = "left"; U = np.array([-1.0, 0.0])
QT = {SIDE: q_(R_tilt(np.array([-U[1], U[0]]), U, TILT))}
hp_ = ts.ee_pose(SIDE)[0]
print("before", umb_contacts(), flush=True)
op.move({SIDE: (hp_ + np.r_[U * 0.03, -0.01]).tolist()}, speed=0.04, quats=QT, timeout=2.0, tol=0.004)
print("during", umb_contacts(), "pad", np.round(pad_mid(SIDE), 3).tolist(), "ee err", np.round(ts.ee_pose(SIDE)[0] - (hp_ + np.r_[U * 0.03, -0.01]), 3).tolist(), flush=True)
print("joint q left arm", [round(float(d.qpos[m.jnt_qposadr[m.joint(n_).id]]), 2) for n_ in ("left_shoulder_pitch_joint", "left_shoulder_roll_joint", "left_shoulder_yaw_joint", "left_elbow_joint", "left_wrist_roll_joint", "left_wrist_pitch_joint", "left_wrist_yaw_joint")], flush=True)
print("ranges", [np.round(m.jnt_range[m.joint(n_).id], 2).tolist() for n_ in ("left_shoulder_pitch_joint", "left_shoulder_roll_joint", "left_shoulder_yaw_joint", "left_elbow_joint", "left_wrist_roll_joint", "left_wrist_pitch_joint", "left_wrist_yaw_joint")], flush=True)
