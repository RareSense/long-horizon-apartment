p_ = base()[0]
t_ = os.path.join(TELE_DIR, "_top.jpg")
print(close(t_, np.r_[p_[:2] + [0.01, 0.0], 2.6], np.r_[p_[:2], 0.0], "top over the robot"), flush=True)
