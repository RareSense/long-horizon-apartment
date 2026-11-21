# left jaws close on the fold and hold (AI-operated)
print("ck", ck_save("g_left_at_fold_before_close", kind="act"), "frame", rec.n, flush=True)
zz_r = zz_close_lock(zz_o)
print("close_lock", zz_r, flush=True)
if zz_o in LOCK:
    hu_ = zz_uv()[LOCK[zz_o][1]]
    print("held n", len(hu_), "uv lo", np.round(hu_.min(0), 2).tolist(), "hi", np.round(hu_.max(0), 2).tolist(), "mean", np.round(hu_.mean(0), 2).tolist(), flush=True)
    for c_ in ((0.5, 0.375), (0.5, -0.375), (0.5, 0.0), (-0.5, 0.375), (-0.5, -0.375)):
        print("  corner", c_, "nearest held dist", round(float(np.linalg.norm(hu_ - np.array(c_), axis=1).min()), 3), flush=True)
print("at_fingers", {s_: zz_w().at_fingers(s_) for s_ in SIDES}, "held L/R", cloth_held("left"), cloth_held("right"), "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "fell", fallen(), flush=True)
a_, b_ = pads(zz_o)
print("pad rf", np.round(zz_to_rf(pad_mid(zz_o)), 3).tolist(), "pads z", round(float(a_[2]), 3), round(float(b_[2]), 3), "gap", round(gap(zz_o), 4), flush=True)
cc_ = pad_mid(zz_o)
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.5, 0.2, 0.2]), cc_, "from the east")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.55]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, 0.2, 0.2]), cc_, "from the west")
print("look", zz_img(t_, "g06_closed"), flush=True)
