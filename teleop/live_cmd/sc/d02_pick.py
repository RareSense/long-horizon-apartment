import time as _tm
MON["on"] = False
_w0 = _tm.time()
zz_b = body_of("r120i1_duck")
mon_start(target=zz_b)
try:
    try:
        pk_ = pick_floor(zz_b, "auto")
    except RuntimeError as ex_:
        if "no place to stand" not in str(ex_): raise
        print("tight", flush=True)
        pk_ = with_tight(lambda: pick_floor(zz_b, "auto"))
    print("PICK", {k_: v_ for k_, v_ in pk_.items() if k_ in ("ok", "side", "pick_s", "held")}, "tries", [(t_.get("grip", {}).get("ok"), t_.get("rose")) for t_ in pk_.get("tries", [])], "appr", len(pk_.get("approaches", [])), flush=True)
    if pk_.get("ok"):
        SD = pk_["side"]; HELD[SD] = pk_.get("grip") or {}
        MON["held"][SD] = zz_b; MON["target"] = None; MON["last_touch"][SD] = float(d.time)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("state", state(), "fell", fallen(), "duck", np.round(centre(zz_b), 3).tolist(), "wall", round(_tm.time() - _w0), flush=True)
print("touch", {s_: finger_touch(s_, zz_b) for s_ in SIDES}, flush=True)
print(look3("d02_duck_picked"), flush=True)
