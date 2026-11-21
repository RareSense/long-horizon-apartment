nm_ = "r149i1_pouch"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin")
r0_ = rec.n
ck_load(os.path.join(RUN, "checkpoints", "0272_act_x_fix_start")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
CK_STATE["item"] = "fix_" + nm_
print("RELOADED 0272 at rec", rec.n, "(discard", r0_, "branch: pick_floor pouch aborted, wrist on the bin)", state(), flush=True)
C_, cc0_, zlo_, ztop_ = flat_corners(pb_)
bc_ = centre(bn_)[:2]
print("pouch corners", np.round(C_, 3).tolist(), "zlo", round(float(zlo_), 3), "ztop", round(float(ztop_), 3), flush=True)
k_ = int(np.argmax([np.linalg.norm(np.asarray(c_) - bc_) for c_ in C_])); G_ = np.asarray(C_[k_], float)
st_ = (float(G_[0] - 0.20), float(G_[1] - 0.25), np.pi / 2)
print("far corner", np.round(G_, 3).tolist(), "stance", np.round(st_, 3).tolist(), flush=True)
mon_start(target=None)
try:
    walk_tight(st_)
except (Abort, RuntimeError) as ex_:
    print("walk ERR", str(ex_)[:200], flush=True)
MON["on"] = False
print("at", state(), "corner rel", np.round(rel(np.r_[G_, 0.0]), 3).tolist(), "pouch", np.round(centre(pb_), 3).tolist(), "bin", np.round(centre(bn_), 3).tolist(), "tilt", round(box_tilt_deg(bn_), 1), "rec", rec.n, flush=True)
print(look3("x02_stance"), flush=True)
