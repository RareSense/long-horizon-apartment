# AI-operated (Fable escalation, scooter r126): the last two backward moves (17.5 cm each, a little to the west) to the
# set-down start (-1.90, 0.555); same cycle before each (bar to 0.25 right, left fingers tips-down).
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
PF = (-1.90, 0.555)
FSC_STEP_OLD = TELE_MAX_STEP; TELE_MAX_STEP = 0.18
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
try:
    for k_ in (11, 12):
        latc(want=-0.25)
        prepitch(-12.0)
        r_ = mvto(f"m{k_}", turn=float(np.degrees(wrapa(np.radians(-90.0) - base()[1]))), to=PF, step=0.175)
        if r_ is None or r_["along"]["left"] > 0.138 or abs(r_["seat"]["left"]["seat_mm"]) > 11.0:
            print("STOP after", k_, flush=True)
            break
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
TELE_MAX_STEP = FSC_STEP_OLD
topview("d03")
st_ = sh_state(sc_); print("state", {k_: st_[k_] for k_ in ("pel", "yaw", "bar", "bar_rel", "tilt", "along", "pad_to_bar", "touch")}, "seat", sh_seat(sc_), "mem", mem(), flush=True)
