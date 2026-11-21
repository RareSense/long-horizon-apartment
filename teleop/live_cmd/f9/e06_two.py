# right: corner pinch again (force 20) with a 2 cm lift; left: fingers forward (jaws above/below) onto the lifted west edge
zz_C, zz_c, _, _ = flat_corners(zz_u)
print("corners now", np.round(zz_C, 3).tolist(), "state", state(), flush=True)
mon_start(target=None); MON["ignore_names"] = (zz_u,)
zz_out = {}
try:
    open_jaws("right", T=0.3)
    pl_ = corner_pinch_plan(zz_u, 0, "right", s_=0.022)[0]
    G_ = pl_["G"]; cd_ = pl_["cd"]; Qr_ = {"right": q_(R_down(cd_))}
    PRE_ACTION("hand_move", {}); servo_pads("right", G_, 0.06, Qr_, speed=0.15); servo_pads("right", G_, 0.013, Qr_, speed=0.05)
    PRE_ACTION("close_jaws", {}); close_jaws("right", 20.0, T=0.8)
    zz_out["g1"] = {k: v for k, v in grip_check("right", None, min_gap=0.004).items() if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
    hp_ = ts.ee_pose("right")[0]; op.move({"right": [hp_[0], hp_[1], hp_[2] + 0.025]}, speed=0.03, quats=Qr_, timeout=3.0, tol=0.005); op.run(1.0)
    zz_out["g2"] = {k: v for k, v in grip_check("right", None, min_gap=0.004).items() if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
    P_ = list(piece_points(zz_u).values())[0]
    # the west edge point 12 cm from the SW corner, its height now
    e_ = zz_C[3] - zz_C[0]; e_ /= np.linalg.norm(e_)
    W_ = zz_C[0] + e_ * 0.12
    near_ = P_[np.argsort(np.linalg.norm(P_[:, :2] - W_, axis=1))[:4]]
    zz_out["edge_z_near"] = np.round(near_[:, 2], 3).tolist()
    zz_out["slab_lo_hi"] = (round(float(P_[:, 2].min()), 3), round(float(P_[:, 2].max()), 3))
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, flush=True)
print(look_hand("right", "umb_low_lift"), flush=True)
