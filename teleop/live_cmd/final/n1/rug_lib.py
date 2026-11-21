# rug toy -> toy basket with an explicit carry route south of the coffee table r145 (x -4.23..-3.13, y -1.23..-0.59):
# the planner's carry turned north-east into the table (hip 61 N) and the ball r192. AI-operated night finisher.
RUG_WAY = [(-3.40, -1.85), (-4.60, -2.00), (-4.80, -1.15)]
def rug_toy(nm, side="left", z_drop=0.30):
    zz_b = body_of(nm); o_ = dict(item=nm)
    _start_item(nm)
    mon_start(target=zz_b)
    try:
        try:
            pk_ = pick_floor(zz_b, side)
        except RuntimeError as ex_:
            if "no place to stand" not in str(ex_):
                raise
            pk_ = with_tight(lambda: pick_floor(zz_b, side))
        o_["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
    except (Abort, RuntimeError) as ex_:
        o_["abort_pick"] = str(ex_)[:300]
    MON["on"] = False
    if o_.get("pick", {}).get("ok"):
        SD_ = o_["pick"]["side"]; HELD[SD_] = pk_.get("grip") or {}
        print("ck", ck_save(f"n1_{nm}_held", kind="act", info=dict(note=f"{nm} held {SD_} (AI-operated)")), flush=True)
        mon_start(target=None); MON["held"][SD_] = zz_b; MON["last_touch"][SD_] = float(d.time)
        globals()["CARRY_JOINTS"] = True
        try:
            p_ = base()[0]
            way_ = [w_ for w_ in RUG_WAY if not (w_ == RUG_WAY[0] and p_[0] < -3.9)]
            for w_ in way_:
                v_ = np.asarray(w_) - base()[0][:2]
                walk_tight((w_[0], w_[1], float(np.arctan2(v_[1], v_[0]))), carry=(SD_,))
        except (Abort, RuntimeError) as ex_:
            o_["abort_carry"] = str(ex_)[:300]
        finally:
            globals()["CARRY_JOINTS"] = False
        MON["on"] = False
        if "abort_carry" not in o_ and not hold_lost(SD_):
            Rn_ = ts.ee_pose(SD_)[1]; cd_ = Rn_[:, 1].copy(); cd_[2] = 0; cd_ /= np.linalg.norm(cd_)
            o_["put"] = basket_put(nm, SD_, {SD_: q_(R_down(cd_))}, z_drop=z_drop)
    o_["in"] = bool(inside(zz_b, body_of("r186i1_basket"))); o_["fell"] = fallen(); o_["state"] = state()
    print("RUG", o_, flush=True)
    print(look3(f"n1_{nm}_end"), flush=True)
    ok_ = _finish(nm, "pick_floor + carry south of the coffee table by way points + basket_put (AI-operated night finisher)") if o_["in"] and not o_["fell"] else False
    return ok_
print("[rug_lib] loaded", flush=True)


def rug_toy_at(nm, side, pref_yaw_deg, z_drop=0.30):
    """rug_toy with the pick stance forced near a preferred heading (the planner found no stance between the coffee
    table, the sofa and the scooter): of the headings the grasp allows, the one nearest pref_yaw; stance from X_REL/Y_REL."""
    global stance_for
    _sf0 = stance_for
    def _sf(pt, sd, xr, yr, **k):
        hs_ = k.get("headings") or [np.radians(pref_yaw_deg)]
        yw_ = min(hs_, key=lambda h_: abs(wrapa(h_ - np.radians(pref_yaw_deg))))
        if abs(wrapa(yw_ - np.radians(pref_yaw_deg))) > np.radians(50) or sd != side:
            return (None, np.inf) if k.get("with_cost") else None
        sg_ = 1.0 if sd == "left" else -1.0
        g_ = np.asarray(pt[:2], float) - RM.rz(yw_)[:2, :2] @ np.array([xr, sg_ * yr])
        print("FORCED stance", nm, np.round(g_, 3).tolist(), round(float(np.degrees(yw_)), 1), flush=True)
        st_ = (float(g_[0]), float(g_[1]), float(yw_))
        return (st_, 0.0) if k.get("with_cost") else st_
    stance_for = _sf
    try:
        return rug_toy(nm, side, z_drop)
    finally:
        stance_for = _sf0
