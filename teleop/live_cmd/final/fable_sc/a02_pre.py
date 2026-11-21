# AI-operated (Fable escalation, scooter r126): at the stance. Checkpoint, full height, both open hands 9 cm behind the bar. Look.
nm = "r126i1_scooter"; sc_ = body_of(nm); SC_NAME = nm
print("ck", ck_save("fsc_at_stance", kind="act", info=dict(note="scooter take stance reached, hands empty (AI-operated)")), "rec", rec.n, flush=True)
mon_start(target=sc_); MON["t_max"] = 6000.0


def arm_lim(s_):
    out_ = {}
    for j_ in range(m.njnt):
        n_ = m.joint(j_).name
        if n_.startswith(s_ + "_") and any(k_ in n_ for k_ in ("shoulder", "elbow", "wrist")):
            q_now = float(d.qpos[m.jnt_qposadr[j_]]); lo_, hi_ = m.jnt_range[j_]
            out_[n_.replace(s_ + "_", "").replace("_joint", "")] = (round(q_now, 2), round(float(lo_), 2), round(float(hi_), 2))
    return out_


def diag(tag, tg_):
    p_, y_ = base(); F_ = sh_frame(sc_); R2_ = RM.rz(y_)[:2, :2]
    print(f"[{tag}] pelvis", np.round(p_, 3), "yaw", round(float(np.degrees(y_)), 1), "bar c", np.round(F_["c"], 3), "z", round(F_["z"], 3), "why", MON.get("why"), flush=True)
    for s_ in SIDES:
        pm_ = pad_mid(s_); e_ = np.asarray(tg_[s_]) - pm_
        fx_ = ts.ee_pose(s_)[1][:, 0]
        print(f"[{tag}] {s_} pad", np.round(pm_, 3), "err world", np.round(e_, 3), "err body (fwd,left)", np.round(R2_.T @ e_[:2], 3), "pad rel pelvis", np.round(R2_.T @ (pm_[:2] - p_[:2]), 3),
              "finger dir", np.round(fx_, 2), "touch", finger_touch(s_, sc_), flush=True)
        print(f"[{tag}] {s_} joints (q, lo, hi)", arm_lim(s_), flush=True)
    print(f"[{tag}] contacts", contact_report(), flush=True)


try:
    op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.6)); op.run(0.9)
    for s_ in SIDES:
        jaw_force[s_] = 20.0; jaw_target[s_] = JAW_OPEN
        ts.setup.end_effectors[s_]["rot_weight"] = float(SH["rot_weight"])
    tg_, Q_, F_ = sh_targets(sc_, back=0.09)
    print("targets", {s_: np.round(tg_[s_], 3).tolist() for s_ in SIDES}, flush=True)
    e1_ = both_move(tg_, Q_, speed=0.15, tol=0.006)
    print("pre_err", e1_, flush=True)
    diag("pre", tg_)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
print("rec", rec.n, "LOOK", look3("fsc_a02_pre"), flush=True)
p_, y_ = base(); fw_ = np.array([np.cos(y_), np.sin(y_)]); F_ = sh_frame(sc_)
pth_ = os.path.join(TELE_DIR, "fsc_a02_top.jpg"); close(pth_, np.r_[F_["c"] - fw_ * 0.25, 2.1], np.r_[F_["c"] - fw_ * 0.10, 0.95], "AI-operated bar from above")
pth2_ = os.path.join(TELE_DIR, "fsc_a02_north.jpg"); close(pth2_, np.r_[F_["c"] + np.array([0.15, 0.9]), 1.15], np.r_[F_["c"] + np.array([0.08, 0.0]), 0.97], "AI-operated bar from the north")
print("TOP", pth_, pth2_, flush=True)
