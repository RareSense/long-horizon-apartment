ck_load(os.path.join(RUN, "checkpoints", "0186_act_walk_leg")); gait_on()
exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
TWO["on"] = True; two_keep(4.0); two_keep(1.5)
print("loaded", state()["pelvis"], "F", {s_: zz_force(s_) for s_ in SIDES}, "pouch", np.round(centre(pb_), 3).tolist(), flush=True)
zz_out = {}
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = (pb_,); MON["ignore"] = {m.body(pb_).id}; MON["t_max"] = 900.0
try:
    for wp_ in ((-4.62, -2.05, 45.0), (-4.55, -1.35, 90.0), (-4.85, -1.05, -125.0)):
        w_ = with_tight(lambda: two_hand_walk(wp_, pb_), rb0=0.22, rf0=0.12)
        print("leg", wp_, {k_: w_.get(k_) for k_ in ("ok", "err_xy", "way_points")} if isinstance(w_, dict) else w_, "F", {s_: zz_force(s_) for s_ in SIDES}, "pouch", np.round(centre(pb_), 3).tolist(), flush=True)
except Abort as ex_:
    zz_out["abort"] = str(ex_)
except RuntimeError as ex_:
    zz_out["err"] = str(ex_)[:300]
MON["on"] = False
print("OUT", zz_out, "pouch", np.round(centre(pb_), 3).tolist(), "state", state(), "fell", fallen(), "touch", contact_report()["body"], flush=True)
print(look3("pouch_at_basket2"), flush=True)
