mon_start(target=None); MON["ignore_names"] = (zz_cb,); MON["held"] = {}
try:
    zQ = {SD: q_(ts.ee_pose(SD)[1])}; bc_ = centre(zz_cb)
    PRE_ACTION("squat_follow", dict(h=-0.30)); squat_follow((SD,), -0.30, 0.40, T=1.4)
    print("squat2", state()["pelvis"], "pad", np.round(pad_mid(SD), 3).tolist(), "in", in_container(zz_n, zz_cb), flush=True)
    for k_ in range(5):
        ic_ = in_container(zz_n, zz_cb)
        if ic_["lowest"] < 0.04 or pad_mid(SD)[2] < 0.20:
            break
        pm_ = pad_mid(SD); e_ = bc_[:2] - pm_[:2]
        r_ = thand(SD, dx=float(np.clip(e_[0], -0.03, 0.03)), dy=float(np.clip(e_[1], -0.03, 0.03)), dz=-0.04, frame="world", Q=zQ, tag="stock_down2")
        print("mv", r_["grip_pt"], r_["err"], "in", in_container(zz_n, zz_cb), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("pad", np.round(pad_mid(SD), 3).tolist(), "in", in_container(zz_n, zz_cb), "state", state(), flush=True)
