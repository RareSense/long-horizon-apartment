print("ck", ck_save("n1_stock_near", kind="act", info=dict(note="west end of the pocket corridor, stocking SW (AI-operated)")), flush=True)
zz_n = "r190i1_stocking"; zz_cb = body_of("r186i1_basket")
mon_start(target=None); MON["t_max"] = 900.0
MON["ignore_names"] = (zz_cb,)
zz_o = dict()
try:
    zz_pk = with_tight(lambda: grasp_cloth(zz_n, "auto"))
    zz_o["pick"] = dict(ok=zz_pk.get("ok"), side=zz_pk.get("side"), tries=len(zz_pk.get("tries", [])))
except Abort as ex_:
    zz_o["abort"] = str(ex_)
except RuntimeError as ex_:
    zz_o["error"] = str(ex_)[:300]
MON["on"] = False
print("PICK", zz_o, "state", state(), "fell", fallen(), "touch", contact_report()["body_who"], "held", list(HELD), list(LOCK) if "LOCK" in globals() else None, flush=True)
print("look", look3("n1_stock_pick"), flush=True)
