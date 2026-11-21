MON["on"] = False
sync_cloth(force=True)
print(close(os.path.join(LK, "b03_mat_above.jpg"), np.r_[1.52, -2.0, 1.6], np.r_[1.52, -2.18, 0.0], "mat from above"), flush=True)
print(close(os.path.join(LK, "b03_hall_east_above.jpg"), np.r_[2.4, -0.2, 2.6], np.r_[2.6, -1.6, 0.0], "hall east from above"), flush=True)
