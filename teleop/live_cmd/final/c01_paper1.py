# paper r195i1: pick_floor (guarded) -> carry to a stance south of the bin -> lean, hand over the bin middle, open. AI-operated
MON["on"] = False
nm_ = "r195i1_paper"
pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); o_ = {}
CK_STATE["item"] = f"{POS + 1:03d}_{nm_}"
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
    o_["abort_pick"] = str(ex_)[:300]
MON["on"] = False
print("PICK", o_, "held", {s_: HOLD.holding(s_) for s_ in SIDES}, "state", state(), flush=True)
if o_.get("pick", {}).get("ok"):
    SDp = o_["pick"]["side"]; HELD[SDp] = pk_.get("grip") or {}
    mon_start(target=None); MON["held"][SDp] = pb_; MON["last_touch"][SDp] = float(d.time)
    try:
        crouch_holding((SDp,), H_WALK, 0.0, T=2.0)
        w_ = walk_tight((0.16, 1.05, np.pi / 2), carry=(SDp,))
        o_["walk"] = w_.get("err_xy") if isinstance(w_, dict) else str(w_)[:120]
        o_["held_after_walk"] = bool(HOLD.holding(SDp) and not hold_lost(SDp)); o_["touch"] = contact_report()["body"]
        PRE_ACTION("lean", {}); squat_follow((SDp,), -0.15, 0.6)
        bc_ = centre(bn_); lo_, hi_ = obj_box(bn_)
        Rn_ = ts.ee_pose(SDp)[1]; cd_ = Rn_[:, 1].copy(); cd_[2] = 0; cd_ /= np.linalg.norm(cd_); Qp = {SDp: q_(R_down(cd_))}
        plo_, phi_ = obj_box(pb_); hang_ = float(pad_mid(SDp)[2] - plo_[2])
        PRE_ACTION("hand_over_bin", {}); e_ = servo_pads(SDp, bc_[:2], float(hi_[2]) + hang_ + 0.05, Qp, speed=0.06)
        o_["e_over"] = np.round(e_, 3).tolist()
        plo_, phi_ = obj_box(pb_)
        over_ = bool(lo_[0] + 0.03 < plo_[0] and phi_[0] < hi_[0] - 0.03 and lo_[1] + 0.03 < plo_[1] and phi_[1] < hi_[1] - 0.03)
        o_["over"] = over_
        if over_:
            MON["ignore_names"] = (pb_,); MON["start"].pop(pb_, None)
            PRE_ACTION("open_jaws", {}); open_jaws(SDp, T=0.5); HELD.pop(SDp, None); MON["held"] = {}; op.run(1.0)
            hp_ = ts.ee_pose(SDp)[0]; op.move({SDp: [hp_[0], hp_[1], hp_[2] + 0.05]}, speed=0.1, timeout=2.0, tol=0.02)
            crouch(0.0, 0.0, T=1.2); rest_hands(SIDES, T=0.6)
    except Abort as ex_:
        o_["abort"] = str(ex_)[:300]
    except RuntimeError as ex_:
        o_["error"] = str(ex_)[:300]
    MON["on"] = False
inn_ = inside(pb_, bn_)
o_.update(paper=np.round(centre(pb_), 3).tolist(), inside=inn_, state=state(), fell=fallen(), touch2=contact_report()["body"], held={s_: HOLD.holding(s_) for s_ in SIDES})
print("RES", o_, flush=True)
if inn_ and not fallen() and not any(HOLD.holding(s_) for s_ in SIDES):
    print("DONE", tele_item_done(nm_, note="pick_floor (guarded hold) + walk_tight to (0.16,1.05,90 deg) south of the bin + lean (-0.15/0.6), hand over the bin middle, open (AI-operated)"), flush=True)
print(look3("paper1_end"), flush=True)
print("SAY", say_item(), flush=True)
