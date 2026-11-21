print("0139 is", INFO["bodies"].get("object_0139_body", {}).get("display"), "box", [np.round(v_, 3).tolist() for v_ in obj_box("object_0139_body")] if "object_0139_body" in INFO["bodies"] else "static", flush=True)
mon_start(target=None); MON["ignore_names"] = ("object_0139_body", zz_b)
try:
    PRE_ACTION("open_jaws", dict(side="right"))
    open_jaws("right", T=0.5); HELD.pop("right", None); op.run(0.5)
    for k_ in range(3):
        thand("right", dz=0.04, frame="world", tag="flat1_up")
    jaw_target["right"] = 0.0
    for hh_, ll_ in ((-0.20, 0.35), (0.0, 0.0)):
        PRE_ACTION("crouch", dict(h=hh_, l=ll_)); crouch(hh_, ll_, T=1.4)
    rest_hands(SIDES); op.run(1.5)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("flat", np.round(centre(zz_b), 3).tolist(), "box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "z axis", np.round(d.xmat[m.body(zz_b).id].reshape(3, 3)[:, 2], 2).tolist(), "0139", [np.round(v_, 3).tolist() for v_ in obj_box("object_0139_body")] if "object_0139_body" in INFO["bodies"] else "-", "state", state(), "fell", fallen(), "touch", contact_report(), flush=True)
for n_ in ("r122i1_croc", "r124i1_sandal", "r125i2_flat"):
    print(n_, np.round(centre(body_of(n_)), 3).tolist(), flush=True)
print(look3("flat1_put"), flush=True)
