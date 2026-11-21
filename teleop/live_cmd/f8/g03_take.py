exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f8\zz_sc2.py", encoding="utf-8").read())
zz_s = body_of("r126i1_scooter"); SC_NAME = "r126i1_scooter"
globals()["TELE_V"] = V_CARRY_HEAVY; globals()["TELE_W"] = SC_PARK["turn_w"]; globals()["CARRY_LOW"] = False
print(floor_first(["r126i1_scooter"])[:2], flush=True)
mon_start(target=zz_s); MON["t_max"] = 900.0
try:
    zz_t = zz_sc_take2(zz_s); print("TAKE", zz_t, flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
print("SC", zz_sc_state(zz_s), "touch", contact_report(), flush=True)
print(look3("sc_take2"), flush=True)
