q0_ = np.load(os.path.join(CHAIN, "physics.npz"), allow_pickle=True)["d_qpos"]
ref_ = r"C:\Users\raresense\sim_home\runs\1120_004212_dex1_floor_6\checkpoints\0599_act_hand_move"
zr_ = np.load(os.path.join(ref_, "physics.npz"), allow_pickle=True); qr_ = zr_["d_qpos"]
print("reference: the floor robot's own last checkpoint, sim t", float(zr_["d_time"]), "| now t", round(float(d.time), 1), "| chain end t 1633.4", flush=True)
rows_ = []
for b_, inf_ in INFO["bodies"].items():
    bi_ = m.body(b_).id
    if not m.body_jntnum[bi_]:
        continue
    a_ = int(m.jnt_qposadr[m.body_jntadr[bi_]])
    dn_ = float(np.linalg.norm(d.qpos[a_:a_ + 3] - q0_[a_:a_ + 3])); dr_ = float(np.linalg.norm(qr_[a_:a_ + 3] - q0_[a_:a_ + 3]))
    dist_ = float(np.linalg.norm(d.qpos[a_:a_ + 2] - np.array([-2.14, -1.45])))
    rows_.append((round(dn_, 4), round(dr_, 4), inf_.get("display", b_), np.round(d.qpos[a_:a_ + 3], 2).tolist(), round(dist_, 2)))
rows_.sort(reverse=True)
for r_ in rows_[:12]:
    print("moved now", r_[0], "| in the floor robot's run by t 1915:", r_[1], "|", r_[2], "at", r_[3], "| from the hamper stance", r_[4], flush=True)
near_ = [r_ for r_ in rows_ if r_[4] < 1.5]
print("things within 1.5 m of the hamper stance:", [(r_[2], r_[0]) for r_ in near_], flush=True)
