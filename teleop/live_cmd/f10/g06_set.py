exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
bk_ = body_of("r186i1_basket")
zz_out = {}
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = (pb_, bk_, body_of("r187i1_plush"), body_of("r120i2_duck"), body_of("r178i1_ball"), body_of("r190i1_stocking")) if body_of("r190i1_stocking") in INFO["bodies"] else (pb_, bk_, body_of("r187i1_plush"), body_of("r120i2_duck"), body_of("r178i1_ball")); MON["ignore"] = {m.body(pb_).id}
try:
    r_ = tmove(fwd=0.08, carry=SIDES, tag="pouch_closer")
    print("closer", r_["at"], r_["yaw_deg"], r_["touch"]["body"], "pouch rel", np.round(rel(centre(pb_)), 3).tolist(), flush=True)
    zz_out["set"] = two_hand_set_down(pb_, np.array([-5.13, -1.38]), 0.12, depth=-0.40, back=0.30, lean=0.2)
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", str(zz_out)[:900], flush=True)
print("pouch", np.round(centre(pb_), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(pb_)], "inside", inside(pb_, bk_), "saber", np.round(centre(body_of("r130i1_light_saber")), 3).tolist(), "state", state(), "fell", fallen(), "ee", {k_: v_.get("mode") for k_, v_ in ts.ee.items()}, flush=True)
print(close(os.path.join(TELE_DIR, "pouch_in.jpg"), np.array([-4.9, -1.0, 1.3]), np.array([-5.18, -1.40, 0.05]), "pouch in basket"), flush=True)
