print(close(os.path.join(TELE_DIR, "f12_entry_a.jpg"), np.array([2.2, -1.0, 1.9]), np.array([3.7, -2.2, 0.0]), "entry from NW"), flush=True)
print(close(os.path.join(TELE_DIR, "f12_entry_b.jpg"), np.array([3.9, -2.5, 1.9]), np.array([3.0, -1.4, 0.0]), "entry from SE"), flush=True)
for s_ in INFO["static"]:
    for bx in (s_.get("pieces") or s_["boxes"]):
        c_ = np.asarray(bx["c"])
        if 3.3 < c_[0] < 4.8 and -3.0 < c_[1] < -0.9:
            print(s_["name"], s_.get("cls"), "c", np.round(c_, 2).tolist(), "half", np.round(np.asarray(bx["s"]) / 2, 2).tolist(), flush=True)
