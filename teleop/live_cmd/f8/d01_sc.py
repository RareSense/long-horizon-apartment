zz_s = body_of("r126i1_scooter")
SP_ = scooter_parts(zz_s)
print("scooter", zz_s, "box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_s)], {k_: (np.round(v_, 3).tolist() if hasattr(v_, "__len__") else v_) for k_, v_ in SP_.items() if not isinstance(v_, dict)}, flush=True)
b2 = SP_["bar_c"][:2] - SP_["deck"] * SC_PARK["bar_d"]
st_ = (float(b2[0]), float(b2[1]), float(np.arctan2(SP_["deck"][1], SP_["deck"][0])))
print("take stance", np.round(st_, 3).tolist(), "free normal", room_grid((zz_s,)).free(np.array(st_[:2])), "free tight", with_tight(lambda: room_grid((zz_s,)).free(np.array(st_[:2]))), flush=True)
print("saber", np.round(centre(body_of("r130i1_light_saber")), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(body_of("r130i1_light_saber"))], flush=True)
print("near scooter", [(INFO["bodies"][b_].get("display", b_), np.round(centre(b_)[:2], 2).tolist()) for b_ in INFO["bodies"] if np.linalg.norm(centre(b_)[:2] - SP_["bar_c"][:2]) < 1.0], flush=True)
def zz_map(x0=-3.0, x1=-0.9, y0=0.7, y1=-1.6):
    g_ = room_grid(())
    print("      " + "".join(str(int(abs(x_) * 10) % 10) for x_ in np.arange(x0, x1, 0.05)), flush=True)
    for y_ in np.arange(y0, y1, -0.05):
        print(f"{y_:5.2f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(x0, x1, 0.05)), flush=True)
print("TIGHT map", flush=True); with_tight(zz_map)
