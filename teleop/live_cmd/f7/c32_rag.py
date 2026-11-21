zz_n = "r68i1_rag"
print(floor_first([zz_n])[:3], flush=True)
zz_g = bc_grasp_at(zz_n, "right", (-0.10, 0.0))
print("GRASP", zz_g, flush=True)
zz_dr = None
if zz_g.get("ok"):
    mon_start(target=None); MON["t_max"] = 900.0
    try:
        zz_dr = drop_in_cloth(zz_n, laundry_body(), "right")
    except Abort as ex_:
        zz_dr = dict(abort=str(ex_))
    except RuntimeError as ex_:
        zz_dr = dict(error=str(ex_)[:300])
    MON["on"] = False
print("DROP", {k_: v_ for k_, v_ in (zz_dr or {}).items() if k_ != "carry"}, flush=True)
print("rag", in_container(zz_n, laundry_body()), "state", state(), "held", dict(HELD), list(LOCK), "fell", fallen(), "kit", kit_mem(), flush=True)
print("look", look3("rag_end"), flush=True)
