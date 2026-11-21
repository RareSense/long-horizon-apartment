zz_b = body_of("r178i1_ball"); zz_sd = "left"
mon_start(target=None); MON["held"][zz_sd] = zz_b; MON["last_touch"][zz_sd] = float(d.time)
zz_out = {}
try:
    pts_ = put_away_any(zz_b, zz_sd)
    zz_out["put"] = str([{k_: v_ for k_, v_ in p_.items() if k_ != "walk"} for p_ in pts_])[:700]
except Abort as ex_:
    zz_out["abort"] = str(ex_)
except RuntimeError as ex_:
    zz_out["err"] = str(ex_)[:300]
MON["on"] = False
print("OUT", zz_out, flush=True)
print("ball", np.round(centre(zz_b), 3).tolist(), "in basket", inside(zz_b, body_of("r186i1_basket")), "held", grip_check(zz_sd, zz_b).get("ok"), "state", state(), "fell", fallen(), "touch", contact_report(), "kit", kit_mem(), flush=True)
print(look3("ball_put"), flush=True)
