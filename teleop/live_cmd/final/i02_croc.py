# croc r122i1 -> shoe mat at (1.20,-2.02) (the first chain's re-put: the room-file spot is off the mat). AI-operated
zz_n = "r122i1_croc"; zz_b = body_of(zz_n); zz_out = {}
CK_STATE["item"] = f"{POS + 1:03d}_{zz_n}"
DESC["spots"][zz_n] = [1.20, -2.02]
mon_start(target=zz_b)
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
zz_out.update(croc=np.round(centre(zz_b), 3).tolist(), state=state(), fell=fallen(), touch=contact_report(), held={s_: HOLD.holding(s_) for s_ in SIDES}, check=item_check(zz_n),
              sandal=item_check("r124i1_sandal"))
print("OUT", zz_out, flush=True)
print(look3("croc_end"), flush=True)
if zz_out["check"].get("ok") and not fallen() and not any(zz_out["held"].values()) and zz_out["sandal"].get("ok"):
    print("DONE", tele_item_done(zz_n, note="pick_floor (guarded) + put_down at (1.20,-2.02) on the mat (AI-operated)"), flush=True)
print("SAY", say_item(), flush=True)
