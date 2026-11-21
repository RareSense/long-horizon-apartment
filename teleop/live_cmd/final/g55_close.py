# jaws of hand ZZ_S squeeze the cloth between the pads and hold; trace of the squeeze (AI-operated)
zz_s = ZZ_S
print("ck", ck_save(f"g_{zz_s}_before_close", kind="act"), "frame", rec.n, flush=True)
PRE_ACTION("zz_close_lock", dict(side=zz_s))
squeeze_on(zz_s, zz_BL)
t0_ = d.time
while d.time - t0_ < 6.0:
    op.run(0.25)
    c_ = SQ[zz_s]
    print("  t %.2f gap %.4f F1 %.1f F2 %.1f pen %.3f n %s e %.2f" % (d.time - t0_, gap(zz_s), c_["F1"], c_["F2"], c_["pen"], c_["n"], c_["e"]), flush=True)
    if c_["e"] > 0.9 and min(c_["F1"], c_["F2"]) > 3.0 and d.time - t0_ > 0.5:
        break
op.run(0.4)
cg_ = zz_w().caught(zz_s)
print("between the pads", len(cg_), "uv", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, flush=True)
n_c = lock_grip(zz_s)
if not n_c:
    squeeze_off(zz_s)
else:
    HELD[zz_s] = dict(cloth=zz_BL)
EVENTS.append(dict(t=round(float(d.time), 2), ev="zz_close_lock", side=zz_s, caught=int(n_c)))
print("lock", n_c, "gap", round(gap(zz_s), 4), "jaw", round(float(jaw(zz_s)), 4), flush=True)
for sd_ in SIDES:
    if sd_ in LOCK:
        hu_ = zz_uv()[LOCK[sd_][1]]
        print(sd_, "held n", len(hu_), "u lo/hi", round(float(hu_[:, 0].min()), 2), round(float(hu_[:, 0].max()), 2), "v lo/hi", round(float(hu_[:, 1].min()), 2), round(float(hu_[:, 1].max()), 2), "near sleeve pts", int((hu_[:, 0] < -0.3).sum()), "far sleeve pts", int((hu_[:, 0] > 0.3).sum()), flush=True)
print("at_fingers", {s_: zz_w().at_fingers(s_) for s_ in SIDES}, "held L/R", cloth_held("left"), cloth_held("right"), "HELD", HELD, "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "out", zz_out_parts(), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "fell", fallen(), flush=True)
cc_ = pad_mid(zz_s)
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.55, 0.25, 0.2]), cc_, "from the east")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
print("look", zz_img(t_, "g55_closed"), flush=True)
