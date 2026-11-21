CHAIN = r"C:/Users/raresense/sim_home/runs/1120_084921_dex1_floor_11/checkpoints/0373_item_r179i1_toy_pouch"
exec(open(r"E:\urc_home\scripts\home\live\load_floor.py", encoding="utf-8").read())
exec(open(r"E:\urc_home\scripts\home\live\bigcloth.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f10\zz_put.py", encoding="utf-8").read())
if "refresh_jointed_footprints" in globals():
    refresh_jointed_footprints()
rest_hands(SIDES)
op.run(1.5)
print("RUN", RUN, "SEG", SEG.get("from_ckpt"), flush=True)
print("route head", [item_name(s_) for s_ in ROUTE[POS:POS + 10]], "done", len(DONE), flush=True)
print("kit", kit_mem(), "state", state(), flush=True)
print("pelvis tilt", round(float(np.arccos(np.clip(d.xmat[m.body("pelvis").id].reshape(3, 3)[2, 2], -1, 1))), 3), "waist pitch", round(float(d.qpos[m.jnt_qposadr[m.joint("waist_pitch_joint").id]]), 3), flush=True)
ub_ = body_of("r106i1_umbrella")
print("umb", np.round(centre(ub_), 3).tolist(), "corners", np.round(flat_corners(ub_)[0], 3).tolist(), "z", np.round(flat_corners(ub_)[2:], 3).tolist(), "dest", DESC["destinations"].get("r106i1_umbrella"), (DESC.get("spots") or {}).get("r106i1_umbrella"), flush=True)
for b_ in INFO["bodies"]:
    try: c_ = centre(b_)
    except Exception: continue
    if 0.6 < c_[0] < 3.8 and -2.7 < c_[1] < 0.6: print("loose", b_, INFO["bodies"][b_].get("display"), np.round(c_, 2).tolist(), [np.round(v_, 2).tolist() for v_ in obj_box(b_)], round(float(m.body_mass[m.body(b_).id]), 2), flush=True)
