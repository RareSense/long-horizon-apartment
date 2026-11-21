ck_load(os.path.join(RUN, "checkpoints", "3261_item_r149i1_pouch")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
rec.still_every = 300
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.3)); op.run(0.4)
print("RELOADED 3261 rec", rec.n, state(), "touch", contact_report()["body_who"], flush=True)
sb_ = body_of("r130i1_light_saber"); sc_ = body_of("r126i1_scooter")
print("saber", [np.round(v_, 3).tolist() for v_ in obj_box(sb_)], "scooter", [np.round(v_, 3).tolist() for v_ in obj_box(sc_)], flush=True)
import mujoco as _mj
M_, D_ = br.mjm, br.mjd; c6_ = np.zeros(6)
sbi_ = [i_ for i_ in range(M_.nbody) if M_.body(i_).name.endswith("_" + sb_)]; sci_ = [i_ for i_ in range(M_.nbody) if M_.body(i_).name.endswith("_" + sc_)]
for i_ in range(D_.ncon):
    c_ = D_.contact[i_]; b1_ = int(M_.geom_bodyid[c_.geom1]); b2_ = int(M_.geom_bodyid[c_.geom2])
    if (b1_ in sbi_ and b2_ in sci_) or (b2_ in sbi_ and b1_ in sci_):
        _mj.mj_contactForce(M_, D_, i_, c6_); print("saber-scooter contact", np.round(c_.pos, 3).tolist(), round(float(c6_[0]), 2), flush=True)
try:
    zz_ok = ITEM_FN["r130i1_light_saber"](0)
except Exception:
    import traceback as _tb; print("EXC", _tb.format_exc()[-1200:], flush=True); zz_ok = False
print("ZZ_OK", zz_ok, "saber", np.round(centre(sb_), 3).tolist(), "scooter moved?", [np.round(v_, 3).tolist() for v_ in obj_box(sc_)], "state", state(), "fell", fallen(), "rec", rec.n, flush=True)
