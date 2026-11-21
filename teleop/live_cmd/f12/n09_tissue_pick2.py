MON["on"] = False
hp_ = ts.ee_pose("right")[0]; op.move({"right": [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.1, timeout=2.0, tol=0.02)
crouch(0.0, 0.0, T=1.0); rest_hands(SIDES, T=0.5)
mon_start(target=body_of("r158i1_tissue")); tmove(fwd=0.06, tag="tissue_closer"); MON["on"] = False
h_, ln_ = surface_posture(0.47); crouch(h_, ln_, T=1.5)
R1 = corner_pick("r158i1_tissue", "right")
print("PICK", {k_: v_ for k_, v_ in R1.items() if k_ != "Q"}, "state", state(), flush=True)
pm_ = pad_mid("right")
print(close(os.path.join(TELE_DIR, "f12_tissue_pick.jpg"), np.r_[pm_[:2] + np.array([0.25, -0.30]), pm_[2] + 0.15], pm_, "tissue pick"), flush=True)
