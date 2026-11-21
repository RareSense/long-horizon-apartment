MON["on"] = False
open_jaws("right", T=0.3); crouch(0.0, 0.0, T=1.0); rest_hands(SIDES, T=0.6)
vb_ = body_of("r191i1_toy_vehicle"); bk_ = body_of("r186i1_basket"); o_ = {}
floor_first(["r191i1_toy_vehicle"])
mon_start(target=vb_)
try:
    try:
        pk_ = pick_floor(vb_, "right")
    except RuntimeError as ex_:
        if "no place to stand" not in str(ex_):
            raise
        pk_ = with_tight(lambda: pick_floor(vb_, "right"))
    o_["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
    o_["fingers_after_pick"] = len(jaw_fingers_on("right", vb_))
    if pk_.get("ok"):
        HELD["right"] = pk_.get("grip") or {}; MON["held"]["right"] = vb_; MON["target"] = None; MON["last_touch"]["right"] = float(d.time)
        Rn_ = ts.ee_pose("right")[1]; cd_ = Rn_[:, 1].copy(); cd_[2] = 0; cd_ /= np.linalg.norm(cd_); Qv = {"right": q_(R_down(cd_))}
        o_["pelvis_after_pick"] = np.round(base()[0][:2], 3).tolist()
        # no walk if the basket middle is within the squat reach from here: squat with the hand following, over, low, open
        over_ = np.array([-5.15, -1.41])
        o_["over_ahead"] = round(ahead_of_pelvis(over_), 3)
        PRE_ACTION("squat", {}); squat_follow(("right",), -0.20, 0.35); squat_follow(("right",), -0.30, 0.6)
        e_ = servo_pads("right", over_, 0.26, Qv, speed=0.04)
        if np.linalg.norm(e_[:2]) > 0.04:
            squat_follow(("right",), -0.38, 0.8); e_ = servo_pads("right", over_, 0.26, Qv, speed=0.04)
        o_["e_over"] = np.round(e_, 3).tolist()
        if np.linalg.norm(e_[:2]) < 0.06:
            lo_, hi_ = obj_box(vb_); hang_ = float(pad_mid("right")[2] - lo_[2])
            e2_ = servo_pads("right", over_, 0.20 + hang_ - 0.06, Qv, speed=0.03)     # bottom ~2 cm over the contents
            MON["ignore_names"] = tuple(set(MON.get("ignore_names", ())) | {vb_}); MON["start"].pop(vb_, None)
            PRE_ACTION("open_jaws", {}); open_jaws("right", T=0.5); HELD.pop("right", None); MON["held"] = {}; op.run(0.8)
        hp_ = pad_mid("right"); servo_pads("right", hp_[:2], hp_[2] + 0.10, Qv, speed=0.08, n=1)
        crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2); rest_hands(SIDES, T=0.6)
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(at=np.round(centre(vb_), 3).tolist(), inside=inside(vb_, bk_), state=state(), fell=fallen())
print("VEH", o_, flush=True)
if o_["inside"] and not o_["fell"]:
    print("DONE", item_done_auto("r191i1_toy_vehicle", dict(status="done", how="3rd try: library pick_floor (right), squat drop with the hand over the basket, bottom ~2 cm over the contents (AI-operated)")), flush=True)
print(look3("f12_vehicle3"), flush=True)
