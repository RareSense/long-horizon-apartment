exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\basket_put.py", encoding="utf-8").read())
MON["on"] = False
zz_b = body_of("r93i1_nugget"); o_ = {}
mon_start(target=zz_b)
try:
    try:
        pk_ = pick_floor(zz_b, "auto")
    except RuntimeError as ex_:
        if "no place to stand" not in str(ex_):
            raise
        pk_ = with_tight(lambda: pick_floor(zz_b, "auto"))
    o_["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
print("PICK", o_, "held", {s_: HOLD.holding(s_) for s_ in SIDES}, "at", np.round(centre(zz_b), 3).tolist(), "state", state(), flush=True)
if o_.get("pick", {}).get("ok"):
    SD = o_["pick"]["side"]; HELD[SD] = pk_.get("grip") or {}
    Rn_ = ts.ee_pose(SD)[1]; cd_ = Rn_[:, 1].copy(); cd_[2] = 0; cd_ /= np.linalg.norm(cd_)
    QB = {SD: q_(R_down(cd_))}
    R_ = basket_put("r93i1_nugget", SD, QB)
    print("BASKET", R_, flush=True)
    if R_.get("in") and not R_.get("fell"):
        print("DONE", item_done_auto("r93i1_nugget", dict(status="done", how="surface pick by AI teleop (level hand) at the island edge; first basket drop missed (hand 31 cm short, opened without checking: it fell beside the basket); library pick_floor, then the basket stance with a deep squat and the hand checked over the basket before opening (AI-operated)")), flush=True)
print(look3("f12_nugget_basket2"), flush=True)
