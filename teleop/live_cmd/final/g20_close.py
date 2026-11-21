# one more small move left and down, then the right jaws close on the far-end sheet and hold (AI-operated)
Rb_ = RM.rz(base()[1])
PRE_ACTION("zz_right_in", dict(d=list(ZZ_D)))
hp_ = ts.ee_pose("right")[0]
op.move({"right": (hp_ + Rb_ @ np.asarray(ZZ_D, float)).tolist()}, speed=0.04, quats=zz_QRF, timeout=3.0, tol=0.006); op.run(0.3)
cg_ = zz_w().caught("right")
print("pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), "pad_low", round(pad_low("right"), 3), "caught", len(cg_), "uv", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, "touch", contact_report(), "fell", fallen(), flush=True)
print("ck", ck_save("g_right_at_sheet_before_close", kind="act"), "frame", rec.n, flush=True)
zz_r = zz_close_lock("right")
print("close_lock", zz_r, flush=True)
for sd_ in SIDES:
    if sd_ in LOCK:
        hu_ = zz_uv()[LOCK[sd_][1]]
        print(sd_, "held n", len(hu_), "uv", np.round(hu_, 2).tolist(), flush=True)
if "right" in LOCK:
    hu_ = zz_uv()[LOCK["right"][1]]
    for c_ in ((0.5, -0.375), (0.5, 0.0), (0.4, -0.375), (0.3, -0.375)):
        print("  point", c_, "dist to the right hold", round(float(np.linalg.norm(hu_ - np.array(c_), axis=1).min()), 3), flush=True)
print("at_fingers", {s_: zz_w().at_fingers(s_) for s_ in SIDES}, "held L/R", cloth_held("left"), cloth_held("right"), "touch", contact_report(), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "out", bc_out(zz_BL, zz_hb()), "fell", fallen(), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g20_closed"), flush=True)
