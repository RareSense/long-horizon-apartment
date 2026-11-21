zz_m = tmove(side=0.10, carry=("right",), tag="jk_step_left")
print("STEP", {k: zz_m[k] for k in ("at", "yaw_deg", "fell", "touch", "look")}, flush=True)
if not zz_m["fell"]:
    PRE_ACTION("tele_rest_hand", dict(side="right"))
    rest_hands(("right",)); HELD.pop("right", None); op.run(1.0)
    print("REST", state(), contact_report(), "hand-hamper", round(float(obj_rect(zz_hb).dist(ts.ee_pose("right")[0][None, :2])[0]), 3), look3("jk_rested"), flush=True)
print("jacket", in_container("r121i1_jacket", zz_hb), flush=True)
