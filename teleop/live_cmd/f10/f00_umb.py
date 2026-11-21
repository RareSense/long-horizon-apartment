ck_load(r"C:\Users\raresense\sim_home\runs\1120_075248_dex1_floor_10\checkpoints\0408_item_r178i1_ball"); gait_on()
rest_hands(SIDES); settle_after_load(); refresh_jointed_footprints()
print(floor_first(["r106i1_umbrella"])[:3], flush=True)
ub_ = body_of("r106i1_umbrella")
print("umb", np.round(centre(ub_), 3).tolist(), "corners", np.round(flat_corners(ub_)[0], 3).tolist(), "z", np.round(flat_corners(ub_)[2:], 3).tolist(), flush=True)
for b_ in INFO["bodies"]:
    try: c_ = centre(b_)
    except Exception: continue
    if 0.6 < c_[0] < 3.8 and -2.7 < c_[1] < 0.6: print("loose", INFO["bodies"][b_].get("display"), np.round(c_, 2).tolist(), [np.round(v_, 2).tolist() for v_ in obj_box(b_)], round(float(m.body_mass[m.body(b_).id]), 2), flush=True)
g_ = with_tight(lambda: room_grid((ub_,)), rb0=0.22, rf0=0.12)
print("grid rb0 0.22 ignoring the umbrella; x from 0.6 step 0.1")
for yy_ in np.arange(0.6, -2.75, -0.1):
    print(f"{yy_:6.2f}", "".join("." if g_.free(np.array([xx_, yy_])) else "#" for xx_ in np.arange(0.6, 3.81, 0.1)), flush=True)
print(close(os.path.join(TELE_DIR, "hall_top.jpg"), np.array([2.2, -0.6, 2.4]), np.array([2.2, -1.3, 0.0]), "hall top"), flush=True)
