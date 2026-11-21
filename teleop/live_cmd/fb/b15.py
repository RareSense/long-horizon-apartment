ck_load(os.path.join(RUN, "checkpoints", "0135_act_walk_leg"))
gait_on(); settle_after_load()
print("loaded", zz_stat(), "hand rf", np.round(zz_to_rf(ts.ee_pose("right")[0]), 3).tolist(), "held", cloth_held("right"), flush=True)
print("scooter", np.round(d.xpos[m.body("object_0259_body").id], 3).tolist(), flush=True)
CARRY_JOINTS = True
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\b14.py", encoding="utf-8").read())
print("hand rf", np.round(zz_to_rf(ts.ee_pose("right")[0]), 3).tolist(), "scooter", np.round(d.xpos[m.body("object_0259_body").id], 3).tolist(), "ARM_NOW", ARM_NOW, flush=True)
