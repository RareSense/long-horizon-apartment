MON["on"] = False
open_jaws("right", T=0.3); hp_ = pad_mid("right"); op.move({"right": (ts.ee_pose("right")[0] + np.array([0, 0, 0.10])).tolist()}, speed=0.1, timeout=2.0, tol=0.02)
crouch(0.0, 0.0, T=1.2); rest_hands(SIDES, T=0.6)
print("stood", state(), "fell", fallen(), flush=True)
tb_ = body_of("r158i1_tissue"); lo_, hi_ = obj_box(tb_)
print("tissue", np.round(centre(tb_), 3).tolist(), np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), "mass", round(float(m.body_mass[m.body(tb_).id]), 3), flush=True)
ZZ = surf_item("r158i1_tissue")
if ZZ.get("ok") and inside(tb_, body_of("rubbish_bin")):
    print("DONE", item_done_auto("r158i1_tissue", dict(status="done", how="library tidy_surface + bin drop (AI-operated)")), flush=True)
