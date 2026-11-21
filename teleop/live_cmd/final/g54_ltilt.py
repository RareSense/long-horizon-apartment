# left hand: fingers down and tilted to the RIGHT by ZZ_B deg (jaws still fore-aft) so the pads reach across the midline (AI-operated)
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
b_ang = np.radians(ZZ_B)
zz_QLF = {"left": q_(zz_R(-np.sin(b_ang) * zz_lat + np.cos(b_ang) * np.array([0, 0, -1.0]), zz_fwd))}
PRE_ACTION("zz_left_tilt", dict(b=ZZ_B))
zz_r = zz_pads_to("left", zz_rf(ZZ_T0), Q=zz_QLF, speed=0.04, step=0.03)
Rn_ = ts.ee_pose("left")[1]; pa_, pb_ = pads("left"); Rb_ = RM.rz(base()[1]); cg_ = zz_w().caught("left")
print("left tilted", zz_r, "fingers rf", np.round(Rb_.T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(Rb_.T @ Rn_[:, 1], 2).tolist(), "pads rf", np.round(zz_to_rf(pa_), 3).tolist(), np.round(zz_to_rf(pb_), 3).tolist(), "pad_low", round(pad_low("left"), 3),
      "caught", len(cg_), "at_f", zz_w().at_fingers("left"), "touch", contact_report()["body"], "fell", fallen(), flush=True)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\g53_lin.py", encoding="utf-8").read())
