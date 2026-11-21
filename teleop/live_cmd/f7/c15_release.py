zz_b = body_of("r124i1_sandal")
try:
    PRE_ACTION("open_jaws", dict(side="left"))
    open_jaws("left", T=0.5); HELD.pop("left", None); MON["held"].pop("left", None)
    op.run(0.5)
    hp_ = pad_mid("left")
    bc_pads_to("left", hp_ + np.array([0, 0, 0.10]), speed=0.06, step=0.05)
    print("released: sandal", np.round(centre(zz_b), 3).tolist(), "box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], flush=True)
    jaw_target["left"] = 0.0
    for hh_, ll_ in ((-0.20, 0.35), (0.0, 0.0)):
        PRE_ACTION("crouch", dict(h=hh_, l=ll_))
        crouch(hh_, ll_, T=1.4)
    rest_hands(("left", "right")); op.run(1.5)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("state", state(), "tilt", round(pelvis_tilt(), 3), "fell", fallen(), "touch", contact_report(), "sandal", np.round(centre(zz_b), 3).tolist(), flush=True)
print("look", look3("sandal_put"), flush=True)
