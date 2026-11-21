ck_load(os.path.join(RUN, "checkpoints", "0540_act__turn_on_spot")); gait_on(); settle_after_load()
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f8\zz_sc2.py", encoding="utf-8").read())
print("R_fwd is orig", R_fwd is _R_FWD0, flush=True)
zz_s = body_of("r126i1_scooter"); SC_NAME = "r126i1_scooter"
globals()["TELE_V"] = V_CARRY_HEAVY; globals()["TELE_W"] = SC_PARK["turn_w"]; globals()["CARRY_LOW"] = False
mon_start(target=zz_s); MON["ignore_names"] = (body_of("r130i1_light_saber"),)
zz_log = []
try:
    op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.6)); op.run(0.8)
    PRE_ACTION("sc_hands_to", {}); sc_hands_to(zz_s, "pre"); sc_hands_to(zz_s, "on")
    PRE_ACTION("sc_close", {}); g_ = sc_close(zz_s)
    print("grips", {s_: (g_[s_].get("gap"), g_[s_].get("jaw1_N"), g_[s_].get("jaw2_N")) for s_ in SIDES}, flush=True)
    for s_ in SIDES:
        jaw_target[s_] = 0.0; jaw_force[s_] = 20.0
        ts.ctrl.ext[f"hold_{s_}"] = (f"{s_}_wrist_yaw_link", np.array([0.165, 0.0, 0.0]), np.array([0.0, 0.0, -9.81 * SC_PARK["hand_kg"]]))
    op.run(0.3); MON["held"] = {s_: zz_s for s_ in SIDES}; MON["target"] = None
    for s_ in SIDES: MON["last_touch"][s_] = float(d.time)
    PRE_ACTION("sc_lift", {}); print("lift", sc_lift(zz_s, dz=0.03), _sc_in_jaws(zz_s), flush=True)
    SC_REL.clear(); _sc_rel_save()
    for k_ in range(2):
        zz_log.append(zz_fwd_step(zz_s, -0.125, "sc_back")); print(zz_log[-1], flush=True)
except Abort as ex_:
    zz_log.append(("abort", str(ex_)))
print("LOG", zz_log, "state", state(), "touch", contact_report(), flush=True)
print(look3("sc_after_back"), flush=True)
