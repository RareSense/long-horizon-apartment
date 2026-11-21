print("ck", ck_save("n1_stock_held", kind="act", info=dict(note="stocking held in the right jaws (grasp_cloth, stance north of it facing south) (AI-operated)")), flush=True)
mon_start(target=None); MON["t_max"] = 900.0; MON["ignore_names"] = (zz_cb,)
globals()["CARRY_JOINTS"] = True
zz_o = {}
try:
    zz_dr = drop_in_cloth(zz_n, zz_cb, "right")
    zz_o = {k_: v_ for k_, v_ in zz_dr.items() if k_ not in ("walk", "carry")}
except Abort as ex_:
    zz_o["abort"] = str(ex_)
except RuntimeError as ex_:
    zz_o["error"] = str(ex_)[:300]
finally:
    globals()["CARRY_JOINTS"] = False
MON["on"] = False
print("DROP", str(zz_o)[:1000], flush=True)
print("in basket", in_container(zz_n, zz_cb), "state", state(), "fell", fallen(), "touch", contact_report()["body_who"], "held", list(HELD), flush=True)
print("look", look3("n1_stock_drop"), flush=True)
