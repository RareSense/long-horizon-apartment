# AI-operated (Fable escalation, scooter r126): tilt 4.8 deg, wheel 0.384 of 0.44: the last centimetres standing still, as
# the skill's sh_finish_standing does (both hands take the bar forward and down along the arc, 2 cm a step), one step at a
# time, stopping when a front wheel stands too or a jaw pair is about to lose the bar.
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
try:
    for k_ in range(4):
        st_, w_ = sd_rep(f"finish {k_}")
        fl_ = sh_on_floor(sc_); se_ = sh_seat(sc_)
        if len(fl_) >= 2 and st_["tilt"] < 2.0:
            print("STANDING", st_["tilt"], fl_, flush=True); break
        if not all(st_["touch"][s_] > 0 for s_ in SIDES) or se_["left"]["seat_mm"] < -11.0 or abs(se_["right"]["seat_mm"]) > 11.0:
            print("STOP: grip margin", st_["touch"], se_, flush=True); break
        dx_ = float(min(0.02, max(w_["x_up"] - w_["x"], 0.004)))
        hf_ = float(np.clip(w_["z"] - w_["r"], 0.0, 0.03))
        dz_ = float(w_["arc"](min(w_["x"] + dx_, w_["x_up"])) + hf_ - 0.001 - w_["bar_z"])
        f_ = -sh_frame(sc_)["deck"]
        PRE_ACTION("fsc_finish_step", dict(dx=round(dx_, 3), dz=round(dz_, 4)))
        both_move({s_: pad_mid(s_) + np.r_[f_ * dx_, dz_] for s_ in SIDES}, sh_level_Q({s_: se_[s_]["pitch"] for s_ in SIDES}), speed=0.02, tol=0.005)
        op.run(0.5)
        if MON.get("why"):
            raise Abort(MON["why"])
    sd_rep("finish end")
except Abort as ex_:
    print("ABORT", str(ex_)[:400], flush=True)
    sd_rep("abort")
views("e04")
