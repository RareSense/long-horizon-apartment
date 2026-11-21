zz_n = "r68i1_rag"
op.run(0.5)
print("now", state()["pelvis"], "touch", contact_report(), "pad", np.round(pad_mid("right"), 3).tolist(), "hamper c", np.round(bc_wall(laundry_body())[0], 3).tolist(), flush=True)
zz_af = bc_release(zz_n, "right"); op.run(1.0)
print("released at_fingers", zz_af, bc_w(zz_n).at_fingers("right"), "rag", in_container(zz_n, laundry_body()), flush=True)
hp_ = ts.ee_pose("right")[0]
op.move({"right": [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.1, timeout=3.0, tol=0.01); op.run(0.3)
jaw_target["right"] = 0.0
mon_start(target=None)
try:
    print("back_off", back_off_container(), flush=True)
    rest_hands(("right",)); op.run(1.0)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
t0_ = d.time
while not bc_w(zz_n).asleep and d.time - t0_ < 4.0:
    op.run(0.25)
print("rag", in_container(zz_n, laundry_body()), "state", state(), "touch", contact_report(), "fell", fallen(), "hamper c", np.round(bc_wall(laundry_body())[0], 3).tolist(), flush=True)
print("look", bc_look(laundry_body(), "rag_in"), flush=True)
