import inspect as _insp
print("hold_on sig", str(_insp.signature(hold_on)), "module", getattr(hold_on, "__module__", None), flush=True)
nm_ = [m.body(i).name for i in range(m.nbody) if "dex1" in m.body(i).name.lower()]
print("dex1 bodies", len(nm_), nm_[:40], flush=True)
print("sponge", body_of("r83i1_sponges"), np.round(obj_box(body_of("r83i1_sponges"))[0], 3).tolist(), np.round(obj_box(body_of("r83i1_sponges"))[1], 3).tolist(), flush=True)
