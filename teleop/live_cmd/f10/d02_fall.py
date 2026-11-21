ck_load(os.path.join(RUN, "checkpoints", "0250_act_stand_up")); gait_on(); op.run(0.05)
print("H_WALK", H_WALK, "state", state(), "ARM_NOW", dict(ARM_NOW), "held", {s_: (HOLD.holding(s_) if HOLD is not None else None) for s_ in SIDES}, flush=True)
print("ee modes", {s_: ts.ee_mode(s_) if hasattr(ts, "ee_mode") else None for s_ in SIDES}, flush=True)
op.send(dict(cmd="posture", height=H_WALK, lean=0.0, duration=1.6))
zz_imgs = []
for k_ in range(12):
    op.run(0.2)
    p_, y_ = base(); q_k = [round(float(v_), 2) for v_ in d.qpos[7:7 + 12]]
    print(round(float(d.time), 1), "pelvis", np.round(p_, 3).tolist(), "fell", fallen(), "legs", q_k, flush=True)
    if k_ in (0, 1, 2, 4, 7):
        zz_imgs.append(close(os.path.join(TELE_DIR, f"_fall{k_}.jpg"), np.r_[p_[:2] + np.array([0.2, 1.3]), 0.9], np.r_[p_[:2], 0.5], f"standup {k_}"))
print(_strip(zz_imgs, os.path.join(TELE_DIR, "fall_strip.jpg")), flush=True)
