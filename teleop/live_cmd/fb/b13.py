PRE_ACTION("zz_right_rest_then_carry", {})
rest_hands(("right",)); op.run(1.5)
Rn_ = ts.ee_pose("right")[1]
print("rested: hand rf", np.round(zz_to_rf(ts.ee_pose("right")[0]), 3).tolist(), "fingers", np.round(Rn_[:, 0], 2).tolist(), "held", cloth_held("right"), "tilt", round(pelvis_tilt(), 3), flush=True)
for zz_z in (0.78, CARRY_Z[1]):
    r_ = carry_pose("right", z=zz_z); op.run(0.5)
    print("carry_pose", zz_z, r_, "hand rf", np.round(zz_to_rf(ts.ee_pose("right")[0]), 3).tolist(), flush=True)
op.run(1.0)
print(zz_stat(), "hang", zz_hang("right"), "tilt", round(pelvis_tilt(), 3), "cloth_held", cloth_held("right"), flush=True)
print("look", look3("carry_ready3"), flush=True)
