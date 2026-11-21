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
        PRE_ACTION("hand_over_basket", {}); o_["e_over"] = np.round(servo_pads(SD, np.asarray(over), z_drop, Q_, speed=0.06), 3).tolist()
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


R_ = basket_put("r93i1_nugget", "right", Q_)
print("BASKET", R_, flush=True)
print(look3("f12_nugget_basket"), flush=True)
if R_.get("in") and not R_.get("fell"):
    print("DONE", item_done_auto("r93i1_nugget", dict(status="done", how="library surface_pick could not reach (pads 6 cm short, top-down at the counter edge, 4 approaches); AI teleop: level hand fingers forward, jaws closing sideways at the nugget's middle height, contact-checked, hold_on, lift 5 cm, pull back; carried to the toy basket stance (-4.85,-1.05,-125 deg), squat, opened over the basket (AI-operated)")), flush=True)
