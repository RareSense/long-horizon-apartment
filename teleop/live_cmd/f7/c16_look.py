zz_b = body_of("r124i1_sandal"); c_ = centre(zz_b)
t_ = [os.path.join(TELE_DIR, f"_s{i}.jpg") for i in range(2)]
close(t_[0], c_ + np.array([0.0, 0.45, 0.45]), c_, "sandal from the north")
close(t_[1], c_ + np.array([0.02, 0.0, 0.7]), c_, "sandal from above")
TELE["n"] += 1
print(_strip(t_, os.path.join(TELE_DIR, f"{TELE['n']:04d}_sandal_on_mat.jpg")), flush=True)
print("R z axis", np.round(d.xmat[m.body(zz_b).id].reshape(3, 3)[:, 2], 2).tolist(), "vel", round(float(np.linalg.norm(d.cvel[m.body(zz_b).id][3:])), 4), flush=True)
