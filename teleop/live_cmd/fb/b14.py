zz_pre = (-2.14, -1.20, -np.pi / 2)
mon_start(target=None); MON["t_max"] = 600.0
phase(f"carry {zz_BL}")
try:
    zz_wk = with_tight(lambda: walk_path(zz_pre, ignore=(zz_BL,), carry=("right",), tol=0.05))
    print("walk", {k_: (v_ if not isinstance(v_, (list, dict)) or k_ in ("way_points",) else str(v_)[:200]) for k_, v_ in (zz_wk or {}).items()}, flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
except Exception as ex_:
    import traceback as tb_; print("ERR", tb_.format_exc()[-800:], flush=True)
MON["on"] = False
print(zz_stat(), "hang", zz_hang("right"), "cloth_held", cloth_held("right"), "mon", MON.get("why"), flush=True)
print("look", look3("at_pre_stance"), flush=True)
