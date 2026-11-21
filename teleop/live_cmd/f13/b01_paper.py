MON["on"] = False
pb_ = body_of("r195i1_paper"); bn_ = body_of("rubbish_bin")
print("paper", np.round(centre(pb_), 3).tolist(), "in bin", inside(pb_, bn_), [np.round(v_, 3).tolist() for v_ in obj_box(pb_)], flush=True)
o_ = {}
mon_start(target=pb_)
try:
    try:
        pk_ = pick_floor(pb_, "auto")
    except RuntimeError as ex_:
        if "no place to stand" not in str(ex_):
            raise
        pk_ = with_tight(lambda: pick_floor(pb_, "auto"))
    o_["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
print("PICK", o_, "held", {s_: HOLD.holding(s_) for s_ in SIDES}, "refused", HOLD_REFUSED[-2:] if "HOLD_REFUSED" in globals() else None, flush=True)
if o_.get("pick", {}).get("ok"):
    sd_ = o_["pick"]["side"]; HELD[sd_] = pk_.get("grip") or {}
    R2 = bin_drop("r195i1_paper", sd_)
    print("BIN", R2, flush=True)
inn_ = inside(pb_, bn_)
print("paper", np.round(centre(pb_), 3).tolist(), "in bin", inn_, "state", state(), "fell", fallen(), flush=True)
if inn_ and not fallen():
    print("SAVED", ck_save("r195i1_paper_redo", kind="item", info=dict(redo=True, why="the earlier drop (chain) missed the bin: it lay at (-0.03,1.57); re-tidied (AI-operated)")), flush=True)
print(look3("f13_paper_redo"), flush=True)
