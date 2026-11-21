F_ = sh_frame(SB)
print("frame", {k_: (np.round(v_, 3).tolist() if hasattr(v_, "__len__") else round(float(v_), 3)) for k_, v_ in F_.items() if k_ in ("c", "lft", "deck", "z")}, flush=True)
for s_ in SIDES:
    pm_ = pad_mid(s_)
    out_ = np.r_[F_["lft"], 0.0] * (1.0 if (pm_[:2] - F_["c"]) @ F_["lft"] > 0 else -1.0)
    eye_ = pm_ + out_ * 0.35 + np.array([0, 0, 0.05])
    print(close(os.path.join(TELE_DIR, f"f12_t04_{s_}_axis.jpg"), eye_, pm_, f"{s_} jaw along the bar"), flush=True)
