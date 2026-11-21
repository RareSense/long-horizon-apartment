MON["on"] = False
LK = os.path.join(RUN, "look"); os.makedirs(LK, exist_ok=True)
print(close(os.path.join(LK, "b01_hall_east_above.jpg"), np.r_[2.4, -0.2, 2.6], np.r_[2.6, -1.6, 0.0], "hall east from above"), flush=True)
print(close(os.path.join(LK, "b01_hall_mid_above.jpg"), np.r_[0.6, 0.3, 2.6], np.r_[1.0, -1.4, 0.0], "hall mid from above"), flush=True)
print(close(os.path.join(LK, "b01_shoes.jpg"), np.r_[3.3, -1.2, 1.2], np.r_[4.05, -1.75, 0.05], "shoes"), flush=True)
