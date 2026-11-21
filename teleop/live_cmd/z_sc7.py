ck_load(zz_ck); MON["on"] = False
p_, y_ = base()
zz_pa = os.path.join(TELE_DIR, "sc_take_side.jpg")
close(zz_pa, np.array([-2.2, 0.05, 1.0]), np.array([-2.2, -0.75, 0.75]), "take from north")
zz_pb = look_hand("left", "sc_take_left")
print(zz_pa, zz_pb)
print("ctrl posture?", {k_: v_ for k_, v_ in (getattr(ts.ctrl, "posture_state", {}) or {}).items()} if hasattr(ts.ctrl, "posture_state") else None)
print("pel z", base()[0][2], "joints knee", float(d.qpos[7 + 3]), float(d.qpos[7 + 9]))
