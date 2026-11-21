mon_start(target=None)
try:
    PRE_ACTION("open_jaws", dict(side="right"))
    open_jaws("right", T=0.5); HELD.pop("right", None); MON["held"].pop("right", None); op.run(0.5)
    for k_ in range(3):
        thand("right", dz=0.04, frame="world", tag="flat_up")
    print("released: flat", np.round(centre(zz_b), 3).tolist(), "box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "z axis", np.round(d.xmat[m.body(zz_b).id].reshape(3, 3)[:, 2], 2).tolist(), flush=True)
    jaw_target["right"] = 0.0
    for hh_, ll_ in ((-0.20, 0.35), (0.0, 0.0)):
        PRE_ACTION("crouch", dict(h=hh_, l=ll_))
        crouch(hh_, ll_, T=1.4)
    rest_hands(("left", "right")); op.run(1.5)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("state", state(), "tilt", round(pelvis_tilt(), 3), "fell", fallen(), "touch", contact_report(), "flat", np.round(centre(zz_b), 3).tolist(), "croc", np.round(centre(body_of("r122i1_croc")), 3).tolist(), "sandal", np.round(centre(body_of("r124i1_sandal")), 3).tolist(), flush=True)
print("look", look3("flat_put"), flush=True)
