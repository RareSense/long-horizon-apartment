zz_b = body_of("r178i1_ball"); zz_sd = "left"; zz_bk = body_of("r186i1_basket")
print("ck", ck_save("n1_ball_held", kind="act", info=dict(note="ball r178 held left (contact-verified) on the sill (AI-operated)")), flush=True)
mon_start(target=None); MON["held"][zz_sd] = zz_b; MON["last_touch"][zz_sd] = float(d.time); MON["t_max"] = 900.0
zz_out = {}
try:
    PRE_ACTION("stand", {}); crouch(0.0, 0.0, T=1.2)
    for k_ in range(2):
        r_ = tmove(fwd=-0.12, carry=(zz_sd,), tag="ball_back")
    globals()["CARRY_JOINTS"] = True
    w_ = walk_tight((-4.85, -1.05, np.radians(-125.0)), carry=(zz_sd,))
    zz_out["walk"] = {k_: v_ for k_, v_ in w_.items() if k_ in ("ok", "err_xy", "way_points")} if isinstance(w_, dict) else str(w_)[:200]
except (Abort, RuntimeError) as ex_:
    zz_out["abort"] = str(ex_)[:300]
finally:
    globals()["CARRY_JOINTS"] = False
MON["on"] = False
print("OUT", zz_out, "state", state(), "ball", np.round(centre(zz_b), 3).tolist(), "grip", grip_check(zz_sd, zz_b).get("ok"), "touch", contact_report()["body_who"], "fell", fallen(), flush=True)
print(look3("n1_ball_at_basket"), flush=True)
