# AI-operated (Fable escalation, scooter r126): carry begins. Recentre distance 0.35 (the right wrist is near its limits
# with the bar nearer). First left turn, 15 deg.
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
sh_recentre.__defaults__ = (0.35, 0.025, 0.03)
w_ = sh_wheel(sc_)
print("wheel", {k_: (round(v_, 3) if isinstance(v_, float) else v_) for k_, v_ in w_.items() if k_ != "arc"}, "clear mm", round((w_["z"] - w_["r"]) * 1000, 1), flush=True)
try:
    print("item_check", item_check(nm), "place_for", place_for(sc_), "spot_of", spot_of(sc_), "centre", np.round(centre(sc_), 3), flush=True)
except Exception as ex_:
    print("item_check:", str(ex_)[:200], flush=True)
print("TELE_V", TELE_V, "TELE_W", TELE_W, "CARRY_LOW", CARRY_LOW, "wristR", wrist("right"), "wristL", wrist("left"), flush=True)
mv("t1", turn=15.0)
topview("c05")
print("mem", mem(), flush=True)
