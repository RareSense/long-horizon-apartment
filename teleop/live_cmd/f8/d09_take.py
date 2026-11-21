ck_load(os.path.join(RUN, "checkpoints", "0540_act__turn_on_spot")); gait_on(); settle_after_load()
print("loaded", state(), "route at", item_name(ROUTE[POS]), flush=True)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f8\zz_sc.py", encoding="utf-8").read())
zz_s = body_of("r126i1_scooter")
mon_start(target=zz_s); MON["ignore_names"] = (body_of("r130i1_light_saber"),)
old_v = TELE_V; old_w = TELE_W
globals()["TELE_V"] = V_CARRY_HEAVY; globals()["TELE_W"] = SC_PARK["turn_w"]; globals()["CARRY_LOW"] = False
try:
    zz_t = zz_sc_take()
except Abort as ex_:
    zz_t = dict(abort=str(ex_))
print("TAKE", zz_t, flush=True)
print("state", state(), "touch", contact_report(), flush=True)
