zz_n = "r68i1_rag"
print("object_0225", INFO["bodies"].get("object_0225_body", {}).get("display"), np.round(d.xpos[m.body("object_0225_body").id], 2).tolist(), flush=True)
ck_load(os.path.join(RUN, "checkpoints", "0891_act_walk_leg")); gait_on(); settle_after_load()
print("loaded", state(), "held", cloth_held("right"), flush=True)
CARRY_JOINTS = True
mon_start(target=None); MON["t_max"] = 900.0; MON["trace"] = []
try:
    zz_dr = drop_in_cloth(zz_n, laundry_body(), "right")
except Abort as ex_:
    zz_dr = dict(abort=str(ex_))
except RuntimeError as ex_:
    zz_dr = dict(error=str(ex_)[:300])
MON["on"] = False
CARRY_JOINTS = False
print("DROP", {k_: v_ for k_, v_ in (zz_dr or {}).items() if k_ != "carry"}, flush=True)
print("rag", in_container(zz_n, laundry_body()), "state", state(), "held", dict(HELD), list(LOCK), "fell", fallen(), "touch", contact_report(), flush=True)
print("look", look3("rag_end2"), flush=True)
