open_jaws("right", T=0.3)
hp_ = ts.ee_pose("right")[0]; op.move({"right": [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.15, timeout=2.0, tol=0.02)
zz_pl = corner_pinch_plan(zz_u, 0, "right", s_=0.022)[0]
zz_o = corner_pinch_try(zz_u, 0, "right", s_=0.022, z_=0.013, force=14.0, pick=zz_pl)
print("TRY", {k_: v_ for k_, v_ in zz_o.items() if not str(k_).startswith("look")}, flush=True)
print(look_hand("right", "umb_pinch2"), flush=True)
