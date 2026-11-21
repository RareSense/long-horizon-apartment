zz_n = "r116i1_coat_pile"
z_ = np.load(os.path.join(CHAIN, "physics.npz"), allow_pickle=True); q0_ = z_["d_qpos"]
mv_ = []
for b_, inf_ in INFO["bodies"].items():
    bi_ = m.body(b_).id
    if not m.body_jntnum[bi_]:
        continue
    a_ = int(m.jnt_qposadr[m.body_jntadr[bi_]])
    mv_.append((round(float(np.linalg.norm(d.qpos[a_:a_ + 3] - q0_[a_:a_ + 3])), 4), inf_.get("display", b_), np.round(d.qpos[a_:a_ + 2], 2).tolist()))
mv_.sort(reverse=True)
print("moved since the chain end (m):", mv_[:8], flush=True)
zz_chk = in_container(zz_n, laundry_body())
assert zz_chk["inside"] >= 0.9 and zz_chk["below_rim"] >= 0.9 and zz_chk["overhang"] < 0.06 and not fallen() and not LOCK and not HELD
zz_d = tele_item_done(zz_n, note="bigcloth.py skill (Fable's hand-over-hand method as stages), AI-operated: grasp uv (0,0.30) north edge middle (right), frozen-arm carry, front stance from NNE, first end lowered and raised, left hand on the hanging strand, lifted over the centre, right let go; fold stage missed the small drape (hand 13 cm short, skipped: 1.6% outside); left lowered to 0.73 and let go. inside 0.993, below rim 0.978, overhang 0.037.")
print("ITEM DONE", zz_d, flush=True)
print("route head", [item_name(s_) for s_ in ROUTE[POS:POS + 5]], "done", len(DONE), "kit", kit_mem(), flush=True)
