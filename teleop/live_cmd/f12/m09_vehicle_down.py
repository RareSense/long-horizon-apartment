MON["on"] = False
SDv = "right"; vb_ = body_of("r191i1_toy_vehicle")
print("state", state(), "hold", {s_: HOLD.holding(s_) for s_ in SIDES}, "fingers", len(jaw_fingers_on(SDv, vb_)), "veh", np.round(centre(vb_), 3).tolist(), flush=True)
Rn_ = ts.ee_pose(SDv)[1]; cd_ = Rn_[:, 1].copy(); cd_[2] = 0; cd_ /= np.linalg.norm(cd_); Qv = {SDv: q_(R_down(cd_))}
lo_, hi_ = obj_box(vb_); hang_ = float(pad_mid(SDv)[2] - lo_[2])
# it is held by the hold spring only (fingers off: the 7 cm body nearly fills the 7.9 cm jaws): set it down where it is, no carrying
e_ = servo_pads(SDv, pad_mid(SDv)[:2], hang_ + 0.01, Qv, speed=0.04)
print("lowered", np.round(e_, 3).tolist(), "veh", np.round(centre(vb_), 3).tolist(), flush=True)
open_jaws(SDv, T=0.5); HELD.pop(SDv, None); MON["held"] = {}; op.run(0.6)
hp_ = pad_mid(SDv); servo_pads(SDv, hp_[:2], hp_[2] + 0.12, Qv, speed=0.08, n=1)
crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2); rest_hands(SIDES, T=0.6)
print("after", state(), "fell", fallen(), "veh", np.round(centre(vb_), 3).tolist(), "in", inside(vb_, body_of("r186i1_basket")), "touch", contact_report()["body"], flush=True)
print(look3("f12_vehicle_down"), flush=True)
