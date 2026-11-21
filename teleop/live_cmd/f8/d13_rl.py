MON["on"] = False
ck_load(os.path.join(RUN, "checkpoints", "0641_act_tele_move")); gait_on(); op.run(0.3)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f8\zz_sc2.py", encoding="utf-8").read())
zz_s = body_of("r126i1_scooter"); SC_NAME = "r126i1_scooter"
globals()["TELE_V"] = V_CARRY_HEAVY; globals()["TELE_W"] = SC_PARK["turn_w"]; globals()["CARRY_LOW"] = False
for s_ in SIDES:
    jaw_target[s_] = 0.0; jaw_force[s_] = 20.0
    ts.ctrl.ext[f"hold_{s_}"] = (f"{s_}_wrist_yaw_link", np.array([0.165, 0.0, 0.0]), np.array([0.0, 0.0, -9.81 * SC_PARK["hand_kg"]]))
mon_start(target=None); MON["ignore_names"] = (body_of("r130i1_light_saber"),)
MON["held"] = {s_: zz_s for s_ in SIDES}
for s_ in SIDES: MON["last_touch"][s_] = float(d.time)
SC_REL.clear(); _sc_rel_save()
print("loaded", state(), "in jaws", _sc_in_jaws(zz_s), "ext", list(ts.ctrl.ext), flush=True)
