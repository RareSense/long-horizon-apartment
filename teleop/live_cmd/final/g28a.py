# only 2 cloth points were between the closed pads (3 needed for a hold): open, 1 cm lower and left where more of the sheet is, squeeze again (AI-operated)
PRE_ACTION("zz_right_reopen3", {})
jaw_force["right"] = 20.0
for jv_ in (0.012, 0.025, JAW_OPEN):
    jaw_target["right"] = jv_; op.run(0.3)
Rb_ = RM.rz(base()[1]); hp_ = ts.ee_pose("right")[0]
op.move({"right": (hp_ + Rb_ @ np.array([0.0, 0.01, -0.012])).tolist()}, speed=0.03, quats=zz_QRF, timeout=3.0, tol=0.004); op.run(0.5)
cg_ = zz_w().caught("right"); a_, b_ = pads("right"); mid_ = (a_ + b_) / 2; ax_ = (b_ - a_) / np.linalg.norm(b_ - a_)
print("pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), "pad_low", round(pad_low("right"), 3), "gap", round(gap("right"), 4), "caught", len(cg_), "along", np.round((zz_w().points(0)[cg_] - mid_) @ ax_, 3).tolist() if len(cg_) else None, "uv", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, flush=True)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\g27_close.py", encoding="utf-8").read())
