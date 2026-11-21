zz_b = body_of("r122i1_croc"); zz_out = {}
mon_start(target=zz_b); MON["trace"] = []
try:
    back_off_container()
    try:
        pk_ = pick_floor(zz_b, "right")
    except RuntimeError as ex_:
        if "no place to stand" not in str(ex_):
            raise
        pk_ = with_tight(lambda: pick_floor(zz_b, "right"))
    zz_out["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
    if pk_.get("ok"):
        sd_ = pk_["side"]; HELD[sd_] = pk_.get("grip") or {}
        MON["held"][sd_] = zz_b; MON["target"] = None; MON["last_touch"][sd_] = float(d.time)
        try:
            pt_ = put_down(zz_b, np.array([1.20, -2.02]), 0.01, sd_)
        except RuntimeError as ex_:
            pt_ = with_tight(lambda: put_down(zz_b, np.array([1.20, -2.02]), 0.01, sd_)) if "no place to stand" in str(ex_) else dict(error=str(ex_))
        MON["held"].pop(sd_, None)
        zz_out["put"] = {k_: v_ for k_, v_ in pt_.items() if k_ != "walk"}
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, flush=True)
print("croc", np.round(centre(zz_b), 3).tolist(), "z axis", np.round(d.xmat[m.body(zz_b).id].reshape(3, 3)[:, 2], 2).tolist(), "state", state(), "fell", fallen(), "touch", contact_report(), flush=True)
print("look", look3("croc_put2"), flush=True)
