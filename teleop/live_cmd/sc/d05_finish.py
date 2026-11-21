MON["on"] = False
zz_b = body_of("r120i1_duck"); zz_cb = body_of("r186i1_basket")
print("duck now", np.round(centre(zz_b), 3).tolist(), "box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "basket rect", obj_rect(zz_cb).c.round(3).tolist(), np.round(obj_rect(zz_cb).h, 3).tolist(), "inside", inside(zz_b, zz_cb), flush=True)
print("duck contacts", [(c_[0], c_[3]) for c_ in umb_contacts(zz_b)] if "umb_contacts" in globals() else None, flush=True)
print(close(os.path.join(LK, "d05_basket_w.jpg"), np.r_[-5.55, -0.95, 0.9], np.r_[-5.15, -1.40, 0.08], "basket from NW"), flush=True)
