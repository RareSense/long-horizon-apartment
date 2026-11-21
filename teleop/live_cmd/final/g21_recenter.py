# the jaws stopped on the taut sheet with one pad only: open, centre the pads on the sheet, close again (AI-operated)
PRE_ACTION("zz_right_reopen", {})
jaw_force["right"] = 20.0; jaw_target["right"] = JAW_OPEN; op.run(0.6)
def zz_along(sd):
    cg_ = zz_w().caught(sd)
    a_, b_ = pads(sd); mid_ = (a_ + b_) / 2; ax_ = (b_ - a_) / np.linalg.norm(b_ - a_)
    al_ = (zz_w().points(0)[cg_] - mid_) @ ax_ if len(cg_) else np.zeros(0)
    return cg_, al_, ax_
cg_, al_, ax_ = zz_along("right")
print("open gap", round(gap("right"), 4), "caught", len(cg_), "along the closing axis (m, + = toward the far pad):", np.round(al_, 3).tolist(), "uv", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, flush=True)
if len(cg_):
    sh_ = float(np.clip(np.median(al_), -0.03, 0.03))
    PRE_ACTION("zz_right_centre", dict(shift=round(sh_, 3)))
    hp_ = ts.ee_pose("right")[0]
    op.move({"right": (hp_ + sh_ * ax_).tolist()}, speed=0.03, quats=zz_QRF, timeout=3.0, tol=0.004); op.run(0.4)
    cg_, al_, ax_ = zz_along("right")
    print("shifted", round(sh_, 3), "now caught", len(cg_), "along:", np.round(al_, 3).tolist(), "pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), "pad_low", round(pad_low("right"), 3), "touch", contact_report(), flush=True)
    if len(cg_) and abs(float(np.median(al_))) > 0.006:
        sh_ = float(np.clip(np.median(al_), -0.02, 0.02))
        hp_ = ts.ee_pose("right")[0]
        op.move({"right": (hp_ + sh_ * ax_).tolist()}, speed=0.03, quats=zz_QRF, timeout=3.0, tol=0.004); op.run(0.4)
        cg_, al_, ax_ = zz_along("right")
        print("shifted again", round(sh_, 3), "now caught", len(cg_), "along:", np.round(al_, 3).tolist(), "pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), flush=True)
print("ck", ck_save("g_right_centred_before_close", kind="act"), "frame", rec.n, flush=True)
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
print("gap", round(gap("right"), 4), "at_fingers", {s_: zz_w().at_fingers(s_) for s_ in SIDES}, "held L/R", cloth_held("left"), cloth_held("right"), "touch", contact_report(), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "out", bc_out(zz_BL, zz_hb()), "fell", fallen(), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g21_closed"), flush=True)
