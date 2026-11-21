print(floor_first(["r139i1_toy_car", "r178i1_ball", "r179i1_toy_pouch"])[:4], flush=True)
zz_b = body_of("r139i1_toy_car")
mon_start(target=zz_b)
try:
    zz_r = tidy_surface(zz_b, "auto")
    if zz_r.get("error") and "no place to stand" in str(zz_r.get("error")) and not zz_r.get("picks", [{}])[0].get("ok"):
        print("no stance -> tight", flush=True)
        zz_r = with_tight(lambda: tidy_surface(zz_b, "auto"))
    print("tidy", {k_: v_ for k_, v_ in zz_r.items() if k_ != "puts"}, flush=True)
    print("puts", str([{k_: v_ for k_, v_ in p_.items() if k_ != "walk"} for p_ in zz_r.get("puts", [])])[:600], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
except Exception as ex_:
    import traceback as _tb; print("ERR", _tb.format_exc()[-800:], flush=True)
MON["on"] = False
print("car", np.round(centre(zz_b), 3).tolist(), "in basket", inside(zz_b, body_of("r186i1_basket")), "held", {s_: grip_check(s_, zz_b).get("ok") for s_ in SIDES}, "state", state(), "fell", fallen(), "touch", contact_report(), "kit", kit_mem(), flush=True)
print(look3("car_end"), flush=True)
