print(floor_first(["r106i1_umbrella"])[:2], flush=True)
zz_pl = corner_pinch_plan(zz_u, 0, "right")[0]
print("plan", np.round(zz_pl["stance"], 3).tolist(), np.round(zz_pl["G"], 3).tolist(), flush=True)
zz_o = corner_pinch_try(zz_u, 0, "right", s_=0.035, z_=0.013, force=14.0, pick=zz_pl)
print("TRY", {k_: v_ for k_, v_ in zz_o.items() if not str(k_).startswith("look")}, flush=True)
print(look_hand("right", "umb_pinch"), flush=True)
