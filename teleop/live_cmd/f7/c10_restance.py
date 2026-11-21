zz_b = body_of("r124i1_sandal")
mon_start(target=None); MON["held"]["left"] = zz_b; MON["last_touch"]["left"] = float(d.time)
try:
    PRE_ACTION("squat_follow", dict(h=0.0, l=0.0))
    squat_follow(("left",), 0.0, 0.0, T=1.4); op.run(0.6)
    print("stood", state()["pelvis"], "fell", fallen(), flush=True)
    zz_w = walk((1.38, -2.08, np.pi), carry=("left",))
    print("walk", {k_: v_ for k_, v_ in zz_w.items() if k_ in ("err_xy", "err_yaw", "ok")} if isinstance(zz_w, dict) else zz_w, flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("state", state(), "sandal", np.round(centre(zz_b), 3).tolist(), "spot rf", np.round(bc_to_rf(np.r_[1.20, -2.35, 0.0]), 3).tolist(), "touch", contact_report(), flush=True)
for n_ in ("left_ankle_roll_link", "right_ankle_roll_link"):
    print(n_, np.round(d.xpos[m.body(n_).id], 3).tolist(), flush=True)
print("look", look3("sandal_new_stance"), flush=True)
