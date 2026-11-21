zz_b = body_of("r126i1_scooter")
zz_sp = scooter_parts(zz_b)
print("r126", zz_b, "bar_c", np.round(zz_sp["bar_c"], 3), "axis", np.round(zz_sp["bar_axis"], 2), "half", round(zz_sp["bar_half"], 3), "stem", np.round(zz_sp["stem"], 3), "deck", np.round(zz_sp["deck"], 2), "com", np.round(zz_sp["com"], 3))
print("r126 box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "mass", float(m.body_mass[m.body(zz_b).id]))
zz_b7 = body_of("r127i1_scooter")
print("r127", zz_b7, [np.round(v_, 3).tolist() for v_ in obj_box(zz_b7)])
print("take stance plan", sc_take_stance(zz_b, dict(take_stance_scene=[-1.45, -0.3, 0])), "auto", sc_take_stance(zz_b))
zz_near = []
for b_, inf_ in INFO["bodies"].items():
    try:
        c_ = d.xpos[m.body(b_).id][:2]
    except Exception:
        continue
    if np.linalg.norm(c_ - zz_sp["com"][:2]) < 1.3:
        zz_near.append((inf_.get("display", b_), b_, np.round(c_, 2).tolist()))
print("near", zz_near)
print(look3("sc0_start"))
