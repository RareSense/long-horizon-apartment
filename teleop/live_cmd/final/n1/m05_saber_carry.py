nm = "r130i1_light_saber"; sb_ = body_of(nm); SD = "right"; SPOT = (-4.92, -1.405)
print("ck", ck_save("n1_saber_held", kind="act", info=dict(note="saber held right (guarded) (AI-operated)")), flush=True)
out_ = {}
mon_start(target=None); MON["held"][SD] = sb_; MON["last_touch"][SD] = float(d.time); MON["t_max"] = 1200.0
globals()["CARRY_JOINTS"] = True
try:
    stand_with(SD, (sb_,))
    for w_ in ((-1.30, -1.20), (-2.60, -1.45), (-3.40, -1.85), (-4.55, -1.95)):
        v_ = np.asarray(w_) - base()[0][:2]
        walk_tight((w_[0], w_[1], float(np.arctan2(v_[1], v_[0]))), carry=(SD,))
        print("at", np.round(base()[0][:2], 3).tolist(), "held", HOLD.holding(SD), flush=True)
    pt_ = put_down(sb_, np.asarray(SPOT, float), 0.01, SD)
    out_["put"] = {k_: v_ for k_, v_ in pt_.items() if k_ != "walk"} if isinstance(pt_, dict) else str(pt_)[:300]
except (Abort, RuntimeError) as ex_:
    out_["abort"] = str(ex_)[:300]
finally:
    globals()["CARRY_JOINTS"] = False
MON["on"] = False
print("PUT", str(out_)[:800], "saber", np.round(centre(sb_), 3).tolist(), "held", HOLD.holding(SD), "state", state(), "fell", fallen(), flush=True)
if HOLD.holding(SD) and not fallen() and "abort" not in out_:
    lower_put(nm, SD, SPOT, done=False)
print("saber", np.round(centre(sb_), 3).tolist(), "check", item_check(nm), "state", state(), "fell", fallen(), flush=True)
print("FIN", _finish(nm, "AI-operated night finisher: library pick stance missed by 2.4 cm and stepped on it; teleop pick from (-1.455,-0.265) heading -30 (jaws across its middle), guarded hold, rose 9 cm; carried by way points south of the coffee table, put_down at its spot by the basket (+ staged-squat lower when needed)", spot=SPOT), flush=True)
print(look3("n1_saber_end"), flush=True)
