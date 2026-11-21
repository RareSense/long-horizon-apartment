phase(f"take {zz_BL}: jaws onto the cloth")
print("down", zz_jaws_down(zz_sd, zz_Q), flush=True)
phase(f"take {zz_BL}: close the jaws")
zz_r = zz_close_lock(zz_sd)
print("close_lock", zz_r, flush=True)
print("look", look_hand(zz_sd, "E_closed"), flush=True)
if zz_r["caught"]:
    zz_z0 = float(garment_box(zz_BL)[1][2])
    phase(f"take {zz_BL}: lift")
    PRE_ACTION("zz_lift", dict(side=zz_sd))
    zz_hp = ts.ee_pose(zz_sd)[0]
    op.move({zz_sd: [zz_hp[0], zz_hp[1], zz_hp[2] + 0.08]}, speed=0.06, quats=zz_Q, timeout=4.0, tol=0.008); op.run(0.4)
    print("rose", round(float(garment_box(zz_BL)[1][2]) - zz_z0, 3), "stretch", zz_w().stretch()[0], "held uv", np.round(zz_uv()[LOCK[zz_sd][1]].mean(0), 3).tolist(), flush=True)
    print("look", look_hand(zz_sd, "E_lifted"), flush=True)
