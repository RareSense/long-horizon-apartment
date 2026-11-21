zz_b = body_of("r124i1_sandal")
zz_Q = {"left": q_(ts.ee_pose("left")[1])}
mon_start(target=None); MON["held"]["left"] = zz_b; MON["last_touch"]["left"] = float(d.time)
try:
    for k_ in range(5):
        lo_ = float(obj_box(zz_b)[0][2])
        if lo_ < 0.025:
            break
        dz_ = -min(0.04, lo_ - 0.015)
        PRE_ACTION("bc_hand", dict(side="left", dz=dz_))
        bc_pads_to("left", pad_mid("left") + np.array([0, 0, dz_]), Q=zz_Q, speed=0.04, step=0.04)
        print("down", k_, "bottom", round(float(obj_box(zz_b)[0][2]), 3), "touch", contact_report(), "pelvis", state()["pelvis"], flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
print("look", look_hand("left", "sandal_low"), flush=True)
