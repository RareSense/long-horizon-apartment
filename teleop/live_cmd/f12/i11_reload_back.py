MON["on"] = False
zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1120_093820_dex1_floor_12\checkpoints\1071_item_r149i1_pouch")
gait_on()
op.run(1.0)
print("loaded", state(), "touch", contact_report()["body"], "knees", np.round([d.qpos[KNEE], d.qpos[m.jnt_qposadr[m.joint('right_knee_joint').id]]], 2).tolist(), flush=True)
b0_ = centre(binb_).copy()
# step back at the standing (carry) height: lowering to the walking height first bent the left knee into the bin, the bin
# pushed it back (42 N, knees 0.53 -> 1.3 rad) and the backward step fell (t 8647.2-8649.0, run 1120_093820)
for k_ in range(2):
    r_ = tmove(fwd=-0.10, carry=("left",), tag="off_bin_tall")
    print("step", k_, state()["pelvis"], "touch", contact_report()["body"], "fell", fallen(), flush=True)
rest_hands(SIDES, T=0.6)
print("bin moved", round(float(np.linalg.norm(centre(binb_) - b0_)), 4), "pouch in", inside(zz_b, binb_), "state", state(), flush=True)
