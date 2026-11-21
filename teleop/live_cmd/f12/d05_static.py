for s_ in INFO["static"]:
    for bx in (s_.get("pieces") or s_["boxes"]):
        c_ = np.asarray(bx["c"]); sz_ = np.asarray(bx["s"])
        z0 = bx.get("z0", c_[2] - sz_[2] / 2); z1 = bx.get("z1", c_[2] + sz_[2] / 2)
        if -0.5 < c_[0] < 3.9 and -2.8 < c_[1] < -0.3 and z0 < 0.2:
            print(s_["name"], s_.get("cls"), "c", np.round(c_[:2], 2).tolist(), "half", np.round(sz_[:2] / 2, 2).tolist(), "yaw", round(float(np.degrees(bx.get("yaw", 0.0))), 0), "z", round(float(z0), 2), round(float(z1), 2), flush=True)
