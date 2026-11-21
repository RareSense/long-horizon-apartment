# blanket held right: carry (arm frozen) to the corridor south of the scooter (-1.55,-1.17), facing east. AI-operated
zz_n = "r117i1_blanket"
CARRY_JOINTS = True
MON["trace"] = []
mon_start(target=None)
try:
    wk_ = None
    for g_ in ((-1.55, -1.17, 0.0), (-1.45, -1.17, 0.0), (-1.3, -1.2, 0.0), (-1.2, -1.2, 0.0)):
        try:
            wk_ = with_tight(lambda: walk_path(g_, ignore=(zz_n,), carry=("right",), tol=0.05)); print("goal", g_, flush=True); break
        except RuntimeError as ex_:
            print("no path", g_, str(ex_)[:80], flush=True)
    print("walk", {k_: (v_ if not isinstance(v_, (list, dict)) else str(v_)[:160]) for k_, v_ in (wk_ or {}).items()} if isinstance(wk_, dict) else wk_, flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("state", state(), "touch", contact_report(), "held", cloth_held("right"), "fell", fallen(), "scooter", np.round(centre(body_of("r126i1_scooter")), 3).tolist(), "saber", np.round(centre(body_of("r130i1_light_saber")), 3).tolist(), flush=True)
print("look3", look3("bl_corr"), flush=True)
