# rag r68i1 -> hamper (AI-operated): bc_grasp_at uv (-0.10,0) right, carry with the arm frozen (CARRY_JOINTS: the first
# chain's free arm hit the tray table object_0225), drop_in_cloth under the monitor (cap 900 s).
zz_n = "r68i1_rag"
CK_STATE["item"] = f"{POS + 1:03d}_{zz_n}"
zz_g = bc_grasp_at(zz_n, "right", (-0.10, 0.0))
print("GRASP", zz_g, flush=True)
zz_dr = None
if zz_g.get("ok"):
    CARRY_JOINTS = True
    mon_start(target=None); MON["t_max"] = 900.0
    try:
        zz_dr = drop_in_cloth(zz_n, laundry_body(), "right")
    except Abort as ex_:
        zz_dr = dict(abort=str(ex_))
    except RuntimeError as ex_:
        zz_dr = dict(error=str(ex_)[:300])
    MON["on"] = False
    CARRY_JOINTS = False
print("DROP", {k_: (v_ if not isinstance(v_, (dict, list)) else str(v_)[:200]) for k_, v_ in (zz_dr or {}).items() if k_ != "carry"}, flush=True)
print("rag", in_container(zz_n, laundry_body()), "state", state(), "held", dict(HELD), list(LOCK), "fell", fallen(), "touch", contact_report(), flush=True)
for n_ in ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket", "r117i1_blanket", "r116i1_coat_pile"):
    print(n_, item_check(n_).get("ok"), flush=True)
print("look", look3("rag_end"), flush=True)
