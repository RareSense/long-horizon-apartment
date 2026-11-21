MON["on"] = False
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\cpick.py", encoding="utf-8").read())
R1 = corner_pick("r158i1_tissue", "right")
print("PICK", {k_: v_ for k_, v_ in R1.items() if k_ != "Q"}, "state", state(), flush=True)
pm_ = pad_mid("right")
print(close(os.path.join(TELE_DIR, "f12_tissue_pick.jpg"), np.r_[pm_[:2] + np.array([0.25, -0.30]), pm_[2] + 0.15], pm_, "tissue pick"), flush=True)
