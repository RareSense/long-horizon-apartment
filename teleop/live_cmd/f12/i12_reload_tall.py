MON["on"] = False
zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1120_093820_dex1_floor_12\checkpoints\1071_item_r149i1_pouch")
gait_on()
print("at load", state(), "knees", np.round([d.qpos[KNEE]], 2).tolist(), flush=True)
# 1071 was saved 0.02 s after a lowering posture command (ready_to_walk of the back step) began: cancel it at once, stay tall
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.4)); op.run(1.2)
print("tall", state(), "touch", contact_report(), "knees", np.round([d.qpos[KNEE]], 2).tolist(), flush=True)
