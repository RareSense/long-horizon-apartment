# right hand (still holding the first end): lower it and turn the fingers down, jaws side by side (AI-operated)
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
a_ = np.radians(ZZ_TILT)
zz_QRT = {"right": q_(zz_R(np.sin(a_) * zz_fwd + np.cos(a_) * np.array([0, 0, -1.0]), zz_lat))}
for zz_t in ZZ_TR:
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=zz_QRT, speed=0.06, step=0.05)
    Rn_ = ts.ee_pose("right")[1]; pa_, pb_ = pads("right")
    print("right to", zz_t, zz_r, "fingers rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 1], 2).tolist(), "pads z", round(float(pa_[2]), 3), round(float(pb_[2]), 3),
          "held L/R", cloth_held("left"), cloth_held("right"), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report(), "knees", zz_knees(), "fell", fallen(), flush=True)
    if fallen() or contact_report()["body"] > 3.0:
        break
print("pads rf", {s_: np.round(zz_to_rf(pad_mid(s_)), 3).tolist() for s_ in SIDES}, "pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "inside", in_container(zz_BL, zz_hb()), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.45, 0.25, 0.15]), cc_, "from the east")
close(t_[1], cc_ + np.array([-0.45, 0.25, 0.15]), cc_, "from the west")
close(t_[2], cc_ + np.array([-0.05, -0.5, 0.2]), cc_, "from the south")
print("look", zz_img(t_, "g10_rdown"), flush=True)
