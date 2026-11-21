ck_load(os.path.join(RUN, "checkpoints", "0540_act__turn_on_spot")); gait_on(); settle_after_load()
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f8\zz_sc.py", encoding="utf-8").read())
zz_s = body_of("r126i1_scooter")
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.6)); op.run(0.8)
G_, fwd_, SP_ = sc_grip_points(zz_s)
print("G", {s_: np.round(G_[s_], 3).tolist() for s_ in SIDES}, "pelvis", state()["pelvis"], flush=True)
Q_ = {s_: q_(zz_Rdown_fwd(fwd_)) for s_ in SIDES}
for s_ in SIDES:
    jaw_force[s_] = 20.0; jaw_target[s_] = JAW_OPEN
# stage 1: hands up in front of the chest, fingers down, well behind the bar
T1 = {s_: np.r_[base()[0][:2] + fwd_ * 0.12 + (G_[s_][:2] - base()[0][:2]) @ np.array([-fwd_[1], fwd_[0]]) * np.array([-fwd_[1], fwd_[0]]), 1.05] for s_ in SIDES}
e_ = both_move(T1, Q_, speed=0.15, tol=0.01)
print("stage1", e_, {s_: np.round(pad_mid(s_), 3).tolist() for s_ in SIDES}, "scooter tilt", round(float(np.degrees(np.arccos(np.clip(obj_pos(zz_s)[1][2, 2], -1, 1)))), 1), "touch", contact_report(), flush=True)
print(look_hand("left", "sc_stage1"), flush=True)
