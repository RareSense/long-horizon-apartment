nm = "r93i1_nugget"; zz_b = body_of(nm); SD = "right"; bk_ = body_of("r186i1_basket")
ign_ = tuple(b_ for b_ in INFO["bodies"] if b_ == bk_ or inside(b_, bk_)) + (body_of("r130i1_light_saber"),)
mon_start(target=None); MON["held"][SD] = zz_b; MON["last_touch"][SD] = float(d.time); MON["ignore_names"] = ign_
T_ = np.array([-5.16, -1.40]); zQ = {SD: q_(ts.ee_pose(SD)[1])}
try:
    for k_ in range(8):
        e_ = T_ - centre(zz_b)[:2]
        if np.linalg.norm(e_) < 0.03:
            break
        r_ = thand(SD, dx=float(np.clip(e_[0], -0.04, 0.04)), dy=float(np.clip(e_[1], -0.04, 0.04)), dz=0.0, frame="world", Q=zQ, tag="nug_over")
        print("mv", r_["grip_pt"], r_["err"], "nug", np.round(centre(zz_b), 3).tolist(), "touch", contact_report()["body_who"], flush=True)
    lo_, hi_ = obj_box(bk_); c_ = centre(zz_b)
    over_ = bool(lo_[0] + 0.04 < c_[0] < hi_[0] - 0.04 and lo_[1] + 0.04 < c_[1] < hi_[1] - 0.04)
    print("over", over_, np.round(c_, 3).tolist(), flush=True)
    if over_:
        MON["ignore_names"] = ign_ + (zz_b,); MON["start"].pop(zz_b, None)
        PRE_ACTION("open_jaws", {}); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}; op.run(1.0)
        hp_ = pad_mid(SD); PRE_ACTION("hand_up", {}); servo_pads(SD, hp_[:2], hp_[2] + 0.10, zQ, speed=0.08, n=1)
        PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2); rest_hands(SIDES, T=0.6); op.run(0.5)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("nugget", np.round(centre(zz_b), 3).tolist(), "inside", inside(zz_b, bk_), "state", state(), "fell", fallen(), "touch", contact_report()["body_who"], flush=True)
print("FIN", _finish(nm, "AI-operated night finisher (first chain's k02 recipe): island stance (2.164,-0.675) facing north, level hand fingers forward, jaws closing sideways 1.2 cm above the nugget's middle (the first tries at its middle pushed the counter edge and the robot fell back), slow reach-in, guarded hold, lift, pull back; basket_put to (-4.85,-1.05,-125); hand over the basket middle by small moves (the library servo ended over the NW rim), open"), flush=True)
print(look3("n1_nugget_in"), flush=True)
