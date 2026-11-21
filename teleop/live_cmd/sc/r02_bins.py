OUTD = r"C:\Users\raresense\sim_home\apartment\final_look_preview"
bb_ = centre(body_of("rubbish_bin")); hb_ = centre(body_of("r133i1_laundry_basket"))
print(close(os.path.join(OUTD, "check_rubbish_bin.jpg"), np.r_[bb_[0] - 0.9, bb_[1] - 0.7, 1.2], bb_, "rubbish bin"), flush=True)
print(close(os.path.join(OUTD, "check_hamper_garments.jpg"), np.r_[hb_[0] + 0.5, hb_[1] + 0.5, 1.5], hb_, "hamper + garments"), flush=True)
print(close(os.path.join(OUTD, "check_robot.jpg"), np.r_[base()[0][:2] + np.array([1.2, 0.6]), 1.2], np.r_[base()[0][:2], 0.6], "robot"), flush=True)
