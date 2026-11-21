# AI-operated (Fable escalation, scooter r126): the left pad slid 2 cm outward along the bar: back toward its place, then the
# bar back to 0.27 right of the pelvis line. No walking.
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
try:
    st_ = sh_state(sc_); print("before", {k_: st_[k_] for k_ in ("bar_rel", "deck_deg", "yaw", "along", "pad_to_bar", "tilt")}, "seat", sh_seat(sc_), flush=True)
    lslide()
    latc()
    st_ = sh_state(sc_); print("after", {k_: st_[k_] for k_ in ("bar_rel", "deck_deg", "yaw", "along", "pad_to_bar", "tilt")}, "seat", sh_seat(sc_), "wristL", wrist("left"), "qL", arm_lim("left"), flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
views("c09")
