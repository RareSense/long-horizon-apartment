print(floor_first(["r120i1_duck"])[:2], flush=True)
zz_b = body_of("r120i1_duck"); zz_cb = body_of("r186i1_basket")
mon_start(target=zz_b); MON["trace"] = []; MON["t_max"] = 900.0
zz_o = {}
try:
    try:
        pk_ = pick_floor(zz_b, "right")
    except RuntimeError as ex_:
        pk_ = with_tight(lambda: pick_floor(zz_b, "right"))
    zz_o["pick"] = (pk_.get("ok"), pk_.get("side"), [(t_.get("grip", {}).get("ok"), t_.get("rose")) for t_ in pk_.get("tries", [])])
    if pk_.get("ok"):
        sd_ = pk_["side"]; HELD[sd_] = pk_.get("grip") or {}
        MON["held"][sd_] = zz_b; MON["target"] = None; MON["last_touch"][sd_] = float(d.time)
        globals()["CARRY_JOINTS"] = True
        try:
            w_ = walk_tight((-4.96, -1.03, -np.pi / 2), carry=(sd_,))
        finally:
            globals()["CARRY_JOINTS"] = False
        zz_o["walk"] = {k_: v_ for k_, v_ in w_.items() if k_ in ("ok", "err_xy", "way_points")} if isinstance(w_, dict) else w_
except Abort as ex_:
    zz_o["abort"] = str(ex_)
except RuntimeError as ex_:
    zz_o["error"] = str(ex_)[:200]
MON["on"] = False
print("OUT", zz_o, "state", state(), "duck", np.round(centre(zz_b), 3).tolist(), "touch", contact_report(), "fell", fallen(), "kit", kit_mem(), flush=True)
print(look3("duck1_at_basket"), flush=True)
