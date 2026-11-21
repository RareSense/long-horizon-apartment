MON["on"] = False
print("toy", np.round(centre(zz_b), 3).tolist(), "inside", inside(zz_b, bk_), "basket", np.round(centre(bk_), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(bk_)], flush=True)
print("hold", HOLD.holding(SD), "err", round(HOLD.items[SD]["err"], 4) if SD in HOLD.items else None, "fingers on", len(jaw_fingers_on(SD, zz_b)) if "jaw_fingers_on" in globals() else None, "pads", np.round(pad_mid(SD), 3).tolist(), flush=True)
print("touch", contact_report(), flush=True)
pm_ = pad_mid(SD)
print(close(os.path.join(TELE_DIR, "f12_m04_hand.jpg"), np.r_[pm_[:2] + np.array([0.0, -0.4]), pm_[2] + 0.35], pm_, "left hand at basket"), flush=True)
