# reset the arms: left to rest (jaws closed), right to the carry place at the top of the carry range
PRE_ACTION("zz_reset_arms", {})
jaw_target["left"] = 0.0
rest_hands(("left",)); op.run(0.8)
print("carry_pose", carry_pose("right", z=CARRY_Z[1]), flush=True)
op.run(1.5)
print(zz_stat(), "hang", zz_hang("right"), "tilt", round(pelvis_tilt(), 3), "cloth_held", cloth_held("right"), flush=True)
print("look", look3("carry_ready"), flush=True)
