print("ck", ck_save("fb_left_at_strand_before_close", kind="act"), flush=True)
zz_r = zz_close_lock(zz_o)
print("close_lock", zz_r, flush=True)
if zz_o in LOCK:
    hu_ = zz_uv()[LOCK[zz_o][1]]
    print("held n", len(hu_), "uv lo", np.round(hu_.min(0), 2).tolist(), "hi", np.round(hu_.max(0), 2).tolist(), "mean", np.round(hu_.mean(0), 2).tolist(), flush=True)
    for c_ in ((0.5, 0.375), (0.5, -0.375), (0.5, 0.0), (-0.5, 0.375), (-0.5, -0.375)):
        print("  corner", c_, "nearest held dist", round(float(np.linalg.norm(hu_ - np.array(c_), axis=1).min()), 3), flush=True)
print("at_fingers", {s_: zz_w().at_fingers(s_) for s_ in SIDES}, "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), flush=True)
cc_ = pad_mid(zz_o)
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.5, -0.4, 0.2]), cc_, "from the south-east")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([0.45, 0.45, 0.25]), cc_, "from the north-east")
print("look", zz_img(t_, "left_closed"), flush=True)
