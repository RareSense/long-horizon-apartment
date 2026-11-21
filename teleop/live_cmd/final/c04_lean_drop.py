MON["on"] = False
SDp = "right"; nm_ = "r195i1_paper"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); o_ = {}
mon_start(target=None); MON["held"][SDp] = pb_; MON["last_touch"][SDp] = float(d.time)
try:
    PRE_ACTION("lean", {}); squat_follow((SDp,), -0.10, 0.5)
    bc_ = centre(bn_); lo_, hi_ = obj_box(bn_)
    plo_, phi_ = obj_box(pb_); hang_ = float(pad_mid(SDp)[2] - plo_[2])
    Qp = {SDp: q_(R_down(np.array([0.0, 1.0, 0.0])))}
    PRE_ACTION("hand_over_bin", {}); e_ = servo_pads(SDp, bc_[:2], float(hi_[2]) + hang_ + 0.05, Qp, speed=0.06)
    o_["e"] = np.round(e_, 3).tolist(); o_["pad"] = np.round(pad_mid(SDp), 3).tolist()
    plo_, phi_ = obj_box(pb_)
    o_["over"] = over_ = bool(lo_[0] + 0.04 < plo_[0] and phi_[0] < hi_[0] - 0.04 and lo_[1] + 0.04 < plo_[1] and phi_[1] < hi_[1] - 0.04)
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
o_.update(paper=np.round(centre(pb_), 3).tolist(), inside=inn_, state=state(), touch=contact_report()["body"], held=HOLD.holding(SDp), fell=fallen())
print("DROP", o_, flush=True)
print(look3("paper1_drop"), flush=True)
if inn_ and not fallen() and not HOLD.holding(SDp):
    print("DONE", tele_item_done(nm_, note="pick_floor (guarded hold), walk_tight to the bin's south side; AI teleop: stand, 0.07 forward, hand over the bin in two servo stages, lean -0.10/0.5, open over the middle (AI-operated)"), flush=True)
print("SAY", say_item(), flush=True)
