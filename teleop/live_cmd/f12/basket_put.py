def basket_put(nm, SD, Q_, stance=(-4.85, -1.05, np.radians(-125.0)), over=(-5.13, -1.39), z_drop=0.30):
    """Carry the held thing to the toy basket r186 and let it go over the basket's middle (the stance and moves the
    floor agents found: the library's basket stance is boxed in). AI-operated."""
    zz_b = body_of(nm); bk_ = body_of("r186i1_basket"); o_ = {}
    mon_start(target=None); MON["held"][SD] = zz_b; MON["last_touch"][SD] = float(d.time)
    try:
        w_ = walk_tight(stance, carry=(SD,))
        o_["walk"] = w_.get("err_xy") if isinstance(w_, dict) else str(w_)[:120]
        o_["held_after_walk"] = not hold_lost(SD)
        PRE_ACTION("squat", {}); squat_follow((SD,), -0.20, 0.35); squat_follow((SD,), -0.30, 0.6)
        PRE_ACTION("hand_over_basket", {}); e_ = servo_pads(SD, np.asarray(over), z_drop, Q_, speed=0.06)
        if np.linalg.norm(e_[:2]) > 0.04:
            PRE_ACTION("squat_deep", {}); squat_follow((SD,), -0.38, 0.8)
            e_ = servo_pads(SD, np.asarray(over), z_drop, Q_, speed=0.06)
        o_["e_over"] = np.round(e_, 3).tolist()
        if np.linalg.norm(e_[:2]) > 0.05:
            raise Abort(f"hand not over the basket: {o_['e_over']}")
        MON["ignore_names"] = tuple(set(MON.get("ignore_names", ())) | {zz_b}); MON["start"].pop(zz_b, None)
        PRE_ACTION("open_jaws", {}); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}
        op.run(0.8)
        o_["in"] = bool(inside(zz_b, bk_))
        hp_ = pad_mid(SD)
        PRE_ACTION("hand_up", {}); servo_pads(SD, hp_[:2], hp_[2] + 0.10, Q_, speed=0.08, n=1)
        PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2)
        rest_hands(SIDES, T=0.6)
    except Abort as ex_:
        o_["abort"] = str(ex_)[:300]
    MON["on"] = False
    o_.update(at=np.round(centre(zz_b), 3).tolist(), state=state(), fell=fallen())
    return o_




def toy_trip(nm, note="", side="right"):
    """One toy from the floor into the toy basket (library pick_floor, tight fallback; basket_put), recorded when in."""
    zz_b = body_of(nm); o_ = dict(item=nm)
    floor_first([nm])
    MON["on"] = False
    mon_start(target=zz_b)
    try:
        try:
            pk_ = pick_floor(zz_b, side)
        except RuntimeError as ex_:
            if "no place to stand" not in str(ex_):
                raise
            pk_ = with_tight(lambda: pick_floor(zz_b, side))
        o_["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
    except Abort as ex_:
        o_["abort_pick"] = str(ex_)[:300]
    MON["on"] = False
    if o_.get("pick", {}).get("ok"):
        SD_ = o_["pick"]["side"]; HELD[SD_] = pk_.get("grip") or {}
        Rn_ = ts.ee_pose(SD_)[1]; cd_ = Rn_[:, 1].copy(); cd_[2] = 0; cd_ /= np.linalg.norm(cd_)
        o_["put"] = basket_put(nm, SD_, {SD_: q_(R_down(cd_))}, z_drop=globals().get("BASKET_Z", 0.30))
        if o_["put"].get("abort") and HOLD.holding(SD_) is False and not fallen() and float(base()[0][2]) < 0.5:
            # stopped after the release (a monitor stop): stand up
            crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2); rest_hands(SIDES, T=0.6)
    o_["in"] = bool(inside(zz_b, body_of("r186i1_basket"))); o_["fell"] = fallen(); o_["state"] = state()
    if o_["in"] and not o_["fell"]:
        o_["done"] = item_done_auto(nm, dict(status="done", how="library pick_floor + basket stance (-4.85,-1.05,-125 deg), deep squat, hand checked over the basket, released (AI-operated)" + note))
    print("TOY", o_, flush=True)
    print(look3(f"f12_{nm}_end"), flush=True)
    return o_
