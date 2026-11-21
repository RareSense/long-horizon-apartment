# right jaws squeeze the far-end sheet above the handle and hold; trace of the squeeze (AI-operated)
print("ck", ck_save("g_right_above_handle_before_close", kind="act"), "frame", rec.n, flush=True)
PRE_ACTION("zz_close_lock", dict(side="right"))
squeeze_on("right", zz_BL)
t0_ = d.time
while d.time - t0_ < 6.0:
    op.run(0.25)
    c_ = SQ["right"]
    print("  t %.2f gap %.4f F1 %.1f F2 %.1f pen %.3f n %s e %.2f" % (d.time - t0_, gap("right"), c_["F1"], c_["F2"], c_["pen"], c_["n"], c_["e"]), flush=True)
    if c_["e"] > 0.9 and min(c_["F1"], c_["F2"]) > 3.0 and d.time - t0_ > 0.5:
        break
op.run(0.4)
cg_ = zz_w().caught("right")
print("between the pads", len(cg_), "uv", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, flush=True)
n_c = lock_grip("right")
if not n_c:
    squeeze_off("right")
else:
    HELD["right"] = dict(cloth=zz_BL)
EVENTS.append(dict(t=round(float(d.time), 2), ev="zz_close_lock", side="right", caught=int(n_c)))
print("lock", n_c, "gap", round(gap("right"), 4), "jaw", round(float(jaw("right")), 4), flush=True)
for sd_ in SIDES:
    if sd_ in LOCK:
        hu_ = zz_uv()[LOCK[sd_][1]]
        print(sd_, "held n", len(hu_), "uv", np.round(hu_, 2).tolist(), flush=True)
if "right" in LOCK:
    hu_ = zz_uv()[LOCK["right"][1]]
    for c_ in ((0.5, -0.375), (0.5, 0.0), (0.4, -0.375), (0.3, -0.375)):
        print("  point", c_, "dist to the right hold", round(float(np.linalg.norm(hu_ - np.array(c_), axis=1).min()), 3), flush=True)
print("at_fingers", {s_: zz_w().at_fingers(s_) for s_ in SIDES}, "held L/R", cloth_held("left"), cloth_held("right"), "HELD", HELD, "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "out", bc_out(zz_BL, zz_hb()), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "fell", fallen(), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g27_closed"), flush=True)
