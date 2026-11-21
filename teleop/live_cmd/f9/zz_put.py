def zz_pick_put(nm, spot, side="right", z=0.01):
    """Pick a floor thing (library pick_floor, tight fallback) and put_down at a chosen floor spot, monitored."""
    zz_b = body_of(nm); out_ = dict(item=nm)
    mon_start(target=zz_b)
    try:
        back_off_container()
        try:
            pk_ = pick_floor(zz_b, side)
        except RuntimeError as ex_:
            if "no place to stand" not in str(ex_):
                raise
            pk_ = with_tight(lambda: pick_floor(zz_b, side))
        out_["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
        if pk_.get("ok"):
            sd_ = pk_["side"]; HELD[sd_] = pk_.get("grip") or {}
            MON["held"][sd_] = zz_b; MON["target"] = None; MON["last_touch"][sd_] = float(d.time)
            try:
                pt_ = put_down(zz_b, np.asarray(spot, float), z, sd_)
            except RuntimeError as ex_:
                pt_ = with_tight(lambda: put_down(zz_b, np.asarray(spot, float), z, sd_)) if "no place to stand" in str(ex_) else dict(error=str(ex_))
            MON["held"].pop(sd_, None); HELD.pop(sd_, None)
            out_["put"] = {k_: v_ for k_, v_ in pt_.items() if k_ != "walk"}
    except Abort as ex_:
        out_["abort"] = str(ex_)
    MON["on"] = False
    out_.update(at=np.round(centre(zz_b), 3).tolist(), zaxis=np.round(d.xmat[m.body(zz_b).id].reshape(3, 3)[:, 2], 2).tolist(), fell=fallen(), touch=contact_report()["body"])
    out_["look"] = look3(f"put_{nm}")
    return out_
