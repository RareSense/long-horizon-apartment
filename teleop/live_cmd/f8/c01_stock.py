zz_n = "r190i1_stocking"; zz_cb = body_of("r186i1_basket")
print("route at", item_name(ROUTE[POS]), "basket", [np.round(v_, 3).tolist() for v_ in obj_box(zz_cb)], "stocking", [np.round(v_, 3).tolist() for v_ in garment_box(zz_n)], flush=True)
mon_start(target=None); MON["t_max"] = 900.0; MON["trace"] = []
MON["ignore_names"] = (zz_cb,)
zz_o = dict()
try:
    back_off_container()
    try:
        zz_pk = with_tight(lambda: grasp_cloth(zz_n, "auto"))
    except RuntimeError as ex_:
        if "no place to stand" not in str(ex_) and "no free path" not in str(ex_):
            raise
        print("grasp -> tight:", str(ex_)[:120], flush=True)
        zz_pk = with_tight(lambda: grasp_cloth(zz_n, "auto"))
    zz_o["pick"] = dict(ok=zz_pk.get("ok"), side=zz_pk.get("side"), tries=len(zz_pk.get("tries", [])))
except Abort as ex_:
    zz_o["abort"] = str(ex_)
except RuntimeError as ex_:
    zz_o["error"] = str(ex_)[:300]
MON["on"] = False
print("PICK", zz_o, str(zz_pk)[:300] if "zz_pk" in globals() else None, "state", state(), "fell", fallen(), "touch", contact_report(), "held", list(HELD), list(LOCK) if "LOCK" in globals() else None, flush=True)
print("look", look3("stocking_pick"), flush=True)
