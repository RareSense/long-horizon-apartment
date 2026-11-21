# AI-operated (Fable escalation, scooter r126): the left pad has slid 2.5 cm outward along the bar and the bar sits 7 mm
# toward that hand's palm. Re-seat it without letting go: hands down in 5 mm steps until the rear wheel stands on the rug
# and carries (the bar stays in both jaws, the scooter stays tilted), the left squeeze eased, the left pad moved back to its
# place on the bar, squeeze back on. No lift yet.
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)


def rep(tag):
    st_ = sh_state(sc_); w_ = sh_wheel(sc_)
    print(f"[{tag}] bar", st_["bar"], "bar_rel", st_["bar_rel"], "tilt", st_["tilt"], "along", st_["along"], "pad_to_bar", st_["pad_to_bar"], "touch", st_["touch"], "seat", sh_seat(sc_),
          "wheel x", round(w_["x"], 3), "clear mm", round((w_["z"] - w_["r"]) * 1000, 1), "floor", sh_on_floor(sc_), "why", MON.get("why"), "rec", rec.n, flush=True)


try:
    print("ck", ck_save("fsc_before_plant", kind="act", info=dict(note="scooter hanging, facing south at (-1.80,-0.09), before the wheel plant re-seat (AI-operated)")), flush=True)
    rep("start")
    seat_ = sh_seat(sc_); pit_ = {s_: seat_[s_]["pitch"] for s_ in SIDES}
    for j_ in range(10):
        both_move({s_: pad_mid(s_) + np.array([0.0, 0.0, -0.005]) for s_ in SIDES}, sh_level_Q(pit_), speed=0.02, tol=0.004)
        op.run(0.3)
        if MON.get("why"):
            raise Abort(MON["why"])
        if sh_on_floor(sc_):
            break
    rep(f"touch after {j_ + 1} steps")
    for j_ in range(3):                                   # until the wheel carries: the lower pads no longer bear the weight
        s2_ = sh_seat(sc_)
        if max(s2_[s_]["lower_N"] - s2_[s_]["upper_N"] for s_ in SIDES) < 5.0:
            break
        both_move({s_: pad_mid(s_) + np.array([0.0, 0.0, -0.003]) for s_ in SIDES}, sh_level_Q(pit_), speed=0.01, tol=0.003)
        op.run(0.4)
    rep("planted")
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
views("c11")
