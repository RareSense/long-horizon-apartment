def fin_step(dx_max=0.015, trim=True, tag="t02"):
    """One small standing step of the set-down's last centimetres (sh_finish_standing's move), AI teleop: bar forward along
    the deck line and down onto the arc round the planted rear wheel, fingers at their current pitch."""
    mon_start(target=None); MON["held"] = {s_: SB for s_ in SIDES}; MON["start"].pop(SB, None); MON["t_max"] = 6000.0
    try:
        w_ = sh_wheel(SB)
        dx_ = float(min(dx_max, max(w_["x_up"] - w_["x"], 0.004)))
        hf_ = float(np.clip(w_["z"] - w_["r"], 0.0, 0.03))
        dz_ = float(w_["arc"](min(w_["x"] + dx_, w_["x_up"])) + hf_ - 0.001 - w_["bar_z"])
        f_ = -sh_frame(SB)["deck"]; seat_ = sh_seat(SB)
        PRE_ACTION("sc_fin_step", dict(dx=round(dx_, 3), dz=round(dz_, 3)))
        both_move({s_: pad_mid(s_) + np.r_[f_ * dx_, dz_] for s_ in SIDES}, sh_level_Q({s_: seat_[s_]["pitch"] for s_ in SIDES}), speed=0.02, tol=0.005)
        op.run(0.5)
        if trim:
            try:
                sh_trim(SB, seat_max=14.5)
            except Abort as ex_:
                print("trim:", str(ex_)[:200], flush=True)
    except Abort as ex_:
        print("ABORT", str(ex_)[:300], flush=True)
    MON["on"] = False
    return sc_report(tag)


R1 = fin_step(tag="t02a")
