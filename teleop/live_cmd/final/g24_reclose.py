# reopen half-way (the sheet is slack now), let the cloth settle between the pads, squeeze again; prints the squeeze state (AI-operated)
PRE_ACTION("zz_right_reopen2", {})
print("pad_load before", [tuple(np.round(x_, 3).tolist() if hasattr(x_, "tolist") else x_ for x_ in pl_) for pl_ in zz_w().pad_load("right")], flush=True)
jaw_force["right"] = 20.0; jaw_target["right"] = ZZ_JAW; op.run(0.8)
cg_ = zz_w().caught("right"); a_, b_ = pads("right"); mid_ = (a_ + b_) / 2; ax_ = (b_ - a_) / np.linalg.norm(b_ - a_)
print("reopened gap", round(gap("right"), 4), "caught", len(cg_), "along", np.round((zz_w().points(0)[cg_] - mid_) @ ax_, 3).tolist() if len(cg_) else None, "uv", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, flush=True)
squeeze_on("right", zz_BL)
t0_ = d.time
while d.time - t0_ < 6.0:
    op.run(0.25)
    c_ = SQ["right"]
    print("  t %.2f gap %.4f F1 %.1f F2 %.1f pen %.3f n %s e %.2f" % (d.time - t0_, gap("right"), c_["F1"], c_["F2"], c_["pen"], c_["n"], c_["e"]), flush=True)
    if c_["e"] > 0.9 and min(c_["F1"], c_["F2"]) > 3.0 and d.time - t0_ > 0.5:
        break
op.run(0.4)
n_c = lock_grip("right")
if not n_c:
    squeeze_off("right")
else:
    HELD["right"] = dict(cloth=zz_BL)
print("lock", n_c, "gap", round(gap("right"), 4), flush=True)
for sd_ in SIDES:
    if sd_ in LOCK:
        hu_ = zz_uv()[LOCK[sd_][1]]
        print(sd_, "held n", len(hu_), "uv", np.round(hu_, 2).tolist(), flush=True)
print("at_fingers", {s_: zz_w().at_fingers(s_) for s_ in SIDES}, "held L/R", cloth_held("left"), cloth_held("right"), "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), "out", bc_out(zz_BL, zz_hb()), "fell", fallen(), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g24_closed"), flush=True)
