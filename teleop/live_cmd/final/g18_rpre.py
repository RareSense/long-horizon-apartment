# right hand, fingers DOWN and jaws closing fore-aft, beside the far-end sheet standing at the north rim (AI-operated)
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
zz_QRF = {"right": q_(zz_R(np.array([0, 0, -1.0]), zz_fwd))}
PRE_ACTION("zz_right_pre", {})
jaw_force["right"] = 20.0; jaw_target["right"] = JAW_OPEN; op.run(0.3)
for zz_t in ZZ_TR:
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=zz_QRF, speed=0.07, step=ZZ_STEP)
    Rn_ = ts.ee_pose("right")[1]; pa_, pb_ = pads("right"); Rb_ = RM.rz(base()[1])
    hc_, hr_ = bc_wall(zz_hb())
    print("right to", zz_t, zz_r, "fingers rf", np.round(Rb_.T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(Rb_.T @ Rn_[:, 1], 2).tolist(), "pads rf", np.round(zz_to_rf(pa_), 3).tolist(), np.round(zz_to_rf(pb_), 3).tolist(),
          "pad_low", round(pad_low("right"), 3), "caught", len(zz_w().caught("right")), "at_f", zz_w().at_fingers("right"), "held L", cloth_held("left"), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report(), "knees", zz_knees(), "fell", fallen(), flush=True)
    if fallen() or contact_report()["body"] > 3.0:
        break
cg_ = zz_w().caught("right")
print("between the pads uv:", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "tilt", round(pelvis_tilt(), 3), "pelvis", state()["pelvis"], flush=True)
for uv_ in ((0.42, -0.18), (0.46, -0.14), (0.4, -0.14), (-0.5, 0.0), (0.4, -0.3)):
    i_ = int(np.argmin(np.linalg.norm(zz_uv() - np.array(uv_), axis=1)))
    print("uv", uv_, "idx", i_, "rf", np.round(zz_to_rf(zz_w().points(0)[i_]), 3).tolist(), "in_pads R", zz_in_pads("right", i_), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g18_rpre"), flush=True)
