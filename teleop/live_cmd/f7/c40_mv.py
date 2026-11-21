z_ = np.load(os.path.join(RUN, "checkpoints", "0943_item_r68i1_rag", "physics.npz"), allow_pickle=True); q0_ = z_["d_qpos"]
mv_ = []
for b_, inf_ in INFO["bodies"].items():
    bi_ = m.body(b_).id
    if not m.body_jntnum[bi_]:
        continue
    a_ = int(m.jnt_qposadr[m.body_jntadr[bi_]])
    mv_.append((round(float(np.linalg.norm(d.qpos[a_:a_ + 3] - q0_[a_:a_ + 3])), 4), inf_.get("display", b_), np.round(d.qpos[a_:a_ + 2], 2).tolist()))
mv_.sort(reverse=True)
print("moved since 0943:", mv_[:6], flush=True)
