MON["on"] = False
pb_ = body_of("r195i1_paper"); bn_ = body_of("rubbish_bin"); SDp = "left"; o_ = {}
print("start", state(), "held", HOLD.holding(SDp), "fingers", len(jaw_fingers_on(SDp, pb_)), flush=True)
mon_start(target=None); MON["held"][SDp] = pb_; MON["last_touch"][SDp] = float(d.time)
try:
    PRE_ACTION("lean", {}); squat_follow((SDp,), -0.05, 0.35)
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
o_.update(paper=np.round(centre(pb_), 3).tolist(), inside=inn_, state=state(), fell=fallen(), touch=contact_report()["body"])
print("DROP", o_, flush=True)
if inn_ and not fallen():
    print("SAVED", ck_save("r195i1_paper_redo", kind="item", info=dict(redo=True, why="the earlier drop (chain) missed the bin: it lay at (-0.03,1.57); re-tidied: pick_floor (guarded hold) + drop over the bin middle (AI-operated)")), flush=True)
print(look3("f13_paper_redo"), flush=True)
