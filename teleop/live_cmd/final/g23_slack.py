# the sheet is taut and tilted between the pads (the squeeze stops at 1.5 cm): lower the left hold a little to slacken it, squeeze again (AI-operated)
PRE_ACTION("zz_left_slack", {})
for zz_t in ZZ_TL:
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=None, speed=0.05, step=0.04)
    cg_ = zz_w().caught("right"); a_, b_ = pads("right"); mid_ = (a_ + b_) / 2; ax_ = (b_ - a_) / np.linalg.norm(b_ - a_)
    print("left to", zz_t, zz_r, "held L", cloth_held("left"), "right caught", len(cg_), "along", np.round((zz_w().points(0)[cg_] - mid_) @ ax_, 3).tolist() if len(cg_) else None, "out", bc_out(zz_BL, zz_hb()), "touch", contact_report()["body"], "fell", fallen(), flush=True)
op.run(0.6)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\g22_close2.py", encoding="utf-8").read())
