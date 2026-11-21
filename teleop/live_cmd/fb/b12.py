p_, y_ = base(); zz_lat = RM.rz(y_)[:, 1]
PRE_ACTION("zz_carry_pose2", {})
tgt_ = zz_rf((CARRY_HAND[0], -CARRY_HAND[1], CARRY_Z[1]))
r_ = op.move({"right": tgt_.tolist()}, speed=0.15, quats={"right": q_(R_down(zz_lat))}, timeout=5.0, tol=0.01); op.run(1.0)
print("move", r_, "hand rf", np.round(zz_to_rf(ts.ee_pose("right")[0]), 3).tolist(), "pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), "tilt", round(pelvis_tilt(), 3), "held", cloth_held("right"), flush=True)
print("look", look3("carry_ready2"), flush=True)
