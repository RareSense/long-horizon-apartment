MON["on"] = False
ck_load(CHAIN); gait_on(); settle_after_load(); refresh_jointed_footprints()
print(floor_first(["r120i2_duck"])[:2], "state", state(), flush=True)
zz_b = body_of("r120i2_duck")
mon_start(target=zz_b); MON["trace"] = []
zz_o = {}
try:
    pk_ = with_tight(lambda: pick_floor(zz_b, "right"))
    zz_o["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
    zz_o["tries"] = [(t_.get("grip", {}).get("ok"), t_.get("rose")) for t_ in pk_.get("tries", [])]
    if pk_.get("ok"):
        HELD[pk_["side"]] = pk_.get("grip") or {}
except Abort as ex_:
    zz_o["abort"] = str(ex_)
MON["on"] = False
print("PICK", zz_o, "state", state(), "touch", contact_report(), flush=True)
print(look3("duck2_pick"), flush=True)
