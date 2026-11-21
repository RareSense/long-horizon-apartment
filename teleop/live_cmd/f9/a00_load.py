CHAIN = r"C:\Users\raresense\sim_home\runs\1120_052805_dex1_floor_8\checkpoints\0840_item_r130i1_light_saber"
exec(open(r"E:\urc_home\scripts\home\live\load_floor.py", encoding="utf-8").read())
exec(open(r"E:\urc_home\scripts\home\live\bigcloth.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f9\zz_put.py", encoding="utf-8").read())
if "refresh_jointed_footprints" in globals():
    refresh_jointed_footprints()
print("RUN", RUN, "SEG", SEG.get("from_ckpt"), flush=True)
print("route head", [item_name(s_) for s_ in ROUTE[POS:POS + 8]], "done", len(DONE), flush=True)
print("kit", kit_mem(), "state", state(), flush=True)
for n_ in ("r174i1_plush", "r197i1_cup", "r173i1_tumbler", "r125i1_flat", "r120i2_duck", "r120i1_duck", "r139i1_toy_car", "r178i1_ball", "r179i1_toy_pouch", "r175i1_cardboard_box"):
    b_ = body_of(n_)
    if b_ in INFO["bodies"]:
        print(n_, "->", DESC["destinations"].get(n_), (DESC.get("spots") or {}).get(n_), "at", np.round(centre(b_), 2).tolist(), "box", [np.round(v_, 3).tolist() for v_ in obj_box(b_)], flush=True)
