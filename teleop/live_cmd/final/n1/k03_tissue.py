ZZ_SIN = 0.025; ZZ_F = 5.0
rec.still_every = 300
nm = "r158i1_tissue"; tb_ = body_of(nm)
_start_item(nm)
mon_start(target=tb_)
try:
    walk_tight((-2.832, -0.505, np.radians(124.3)))
except (Abort, RuntimeError) as ex_:
    print("walk ERR", str(ex_)[:200], flush=True)
MON["on"] = False
print("at", state(), "tissue", np.round(centre(tb_), 3).tolist(), flush=True)
print("ck", ck_save("n1_tissue_stance", kind="act", info=dict(note="sofa-seat stance for tissue r158 (AI-operated)")), flush=True)
for s_in_, f_ in ((ZZ_SIN, ZZ_F),):
    try:
        crouch(*surface_posture(0.47), T=1.2)
    except Abort as ex_:
        print("posture abort", ex_, flush=True)
    c_ = corner_pick(nm, "right", s_in=s_in_, force=f_); print("CORNER", {k_: v_ for k_, v_ in c_.items() if k_ != "Q"}, flush=True)
    if c_.get("held"):
        print("ck", ck_save("n1_tissue_held", kind="act", info=dict(note="tissue held (guarded corner pinch) (AI-operated)")), flush=True)
        _to_bin(nm, "right")
print("tissue", np.round(centre(tb_), 3).tolist(), "check", item_check(nm), "state", state(), "fell", fallen(), flush=True)
print("FIN", _finish(nm, f"AI-operated night finisher: stance (-2.83,-0.51,124 deg) south-east of the sofa seat, seat posture (-0.12,0.45) (the runner's call never sent it), corner_pick right s_in {ZZ_SIN} force {ZZ_F} N (guarded hold), bin_drop"), flush=True)
print(look3("n1_tissue_end"), flush=True)
