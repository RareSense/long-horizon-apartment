PRE_ACTION("zz_retract_hands", {})
jaw_target["left"] = 0.0; jaw_target["right"] = 0.0; op.run(0.4)
for zz_t in ((0.36, 0.10, 1.00), (0.22, 0.16, 0.95)):
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=None, speed=0.08, step=0.06)
    print("left to", zz_t, {k_: zz_r[k_] for k_ in ("err", "pad", "tilt")}, "touch", contact_report()["body"], flush=True)
rest_hands(("left", "right")); op.run(1.5)
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=1.2)); op.run(2.0)
print("rested", state(), "tilt", round(pelvis_tilt(), 3), "touch", contact_report(), "knees", zz_knees(), "fell", fallen(), flush=True)
print("hands to hamper wall", {s_: round(float(np.linalg.norm(ts.ee_pose(s_)[0][:2] - obj_rect(zz_hb()).c)) - 0.257, 3) for s_ in SIDES}, "jaws", {s_: round(jaw(s_), 4) for s_ in SIDES}, "gap", {s_: round(gap(s_), 4) for s_ in SIDES}, flush=True)
t0_ = d.time
while not zz_w().asleep and d.time - t0_ < 6.0:
    op.run(0.25)
print("blanket", in_container(zz_BL, zz_hb()), "asleep", bool(zz_w().asleep), "top", round(float(zz_w().points(0)[:, 2].max()), 3), flush=True)
# what moved since the chain end (the checkpoint this run started from)
z_ = np.load(os.path.join(CHAIN, "physics.npz"), allow_pickle=True); q0_ = z_["d_qpos"]
mv_ = []
for b_, inf_ in INFO["bodies"].items():
    bi_ = m.body(b_).id
    if not m.body_jntnum[bi_]:
        continue
    a_ = int(m.jnt_qposadr[m.body_jntadr[bi_]])
    dp_ = float(np.linalg.norm(d.qpos[a_:a_ + 3] - q0_[a_:a_ + 3]))
    mv_.append((round(dp_, 4), inf_.get("display", b_)))
mv_.sort(reverse=True)
print("moved since the chain end (m):", mv_[:8], flush=True)
for n_ in ("r121i1_jacket", "r131i1_knit_hat", "r189i1_santa_hat"):
    print(n_, in_container(n_, zz_hb()), flush=True)
print("look", zz_look(np.array([-2.14, -1.90, 0.6]), "blanket_done", dist=1.4, h=0.9, dirs=(20.0, 160.0), top=True), flush=True)
print("look3", look3("blanket_done"), flush=True)
