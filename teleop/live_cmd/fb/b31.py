hc_ = obj_rect(zz_hb()).c; zz_ang = np.radians(114.0)
zz_rimpt = hc_ + 0.246 * np.array([np.cos(zz_ang), np.sin(zz_ang)])
PRE_ACTION("zz_rim_over", dict(pt=np.round(zz_rimpt, 3).tolist()))
jaw_target["right"] = 0.034
r_ = zz_pads_to("right", np.r_[zz_rimpt, 0.64], Q=zz_QR, speed=0.04, step=0.03)
a_, b_ = pads("right")
lv_ = [cloth_level(zz_BL, x_, r=0.02) for x_ in (a_, b_)]
print("over rim:", r_, "pad_low", round(pad_low("right"), 4), "cloth level under pads", lv_, "pads r", [round(float(np.linalg.norm(x_[:2] - hc_)), 3) for x_ in (a_, b_)], "gap", round(gap("right"), 3), "touch", contact_report(), flush=True)
print("look", zz_look(pad_mid("right"), "rim_over", dist=0.5, h=0.3, dirs=(60.0, 150.0, 240.0), top=True), flush=True)
