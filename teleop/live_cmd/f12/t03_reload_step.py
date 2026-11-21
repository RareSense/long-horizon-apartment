MON["on"] = False
zz_m = route_v3_resume(CK)
gait_on()
globals()["TELE_V"] = V_CARRY_HEAVY; globals()["TELE_W"] = 0.10; globals()["CARRY_LOW"] = False
R0 = sc_report("t03a")      # right after the load, no settle (the call went on from here)
R1 = fin_step(dx_max=0.010, trim=False, tag="t03b")
