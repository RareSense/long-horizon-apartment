# light saber r130 rests against the scooter r126's deck end: it goes first (set aside by the north wall), then the scooter
zz_r = set_aside("r130i1_light_saber", (-1.9, 1.45))
print("ASIDE", {k_: v_ for k_, v_ in zz_r.items() if k_ != "look"})
print("look", zz_r.get("look"), "mem", kit_mem())
print("r126 box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)])
