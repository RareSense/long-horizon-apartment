ck_load(os.path.join(RUN, "checkpoints", "0306_act_unlock_grip")); gait_on(); op.run(0.5); refresh_jointed_footprints()
SD = "right"; zz_n = "r190i1_stocking"; zz_cb = body_of("r186i1_basket")
print("loaded 0306 rec", rec.n, "held", list(HELD), list(LOCK), "pad", np.round(pad_mid(SD), 3).tolist(), "in", in_container(zz_n, zz_cb), "basket", [np.round(v_, 3).tolist() for v_ in obj_box(zz_cb)], flush=True)
mon_start(target=None); MON["ignore_names"] = (zz_cb,); MON["held"] = {}
try:
    bc_ = centre(zz_cb)
    zQ = {SD: q_(ts.ee_pose(SD)[1])}
    PRE_ACTION("squat_follow", dict(h=-0.20)); squat_follow((SD,), -0.20, 0.15, T=1.6)
    for k_ in range(6):
        pm_ = pad_mid(SD); e_ = bc_[:2] - pm_[:2]
        ic_ = in_container(zz_n, zz_cb)
        if ic_["lowest"] < 0.04 and np.linalg.norm(e_) < 0.03:
            break
        r_ = thand(SD, dx=float(np.clip(e_[0], -0.04, 0.04)), dy=float(np.clip(e_[1], -0.04, 0.04)), dz=-0.04 if ic_["lowest"] > 0.04 else 0.0, frame="world", Q=zQ, tag="stock_down")
        print("mv", r_["grip_pt"], r_["err"], "in", in_container(zz_n, zz_cb), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("pad", np.round(pad_mid(SD), 3).tolist(), "in", in_container(zz_n, zz_cb), "state", state(), flush=True)
print(look_hand(SD, "n1_stock_low"), flush=True)
