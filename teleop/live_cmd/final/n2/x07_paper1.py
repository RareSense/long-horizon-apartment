exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\n2\xlib.py", encoding="utf-8").read())
nm_ = "r195i1_paper"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); SD = "left"; CK_STATE["item"] = "fix_" + nm_
print("ck", ck_save("x_paper3_in", kind="act", info=dict(note="paper r195i3 dropped into the bin again (AI-operated)")), flush=True)
C_ = flat_corners(pb_)[0]; bc_ = centre(bn_)[:2]
G_ = np.asarray(max(C_, key=lambda c_: np.linalg.norm(np.asarray(c_) - bc_)), float)
st_ = (float(G_[0] + 0.25), float(G_[1] + 0.20), np.pi)      # facing west, left hand (world -y side) on the far corner, knees clear of the bin (it is SW)
print(nm_, "corners", np.round(C_, 3).tolist(), "far", np.round(G_, 3).tolist(), "stance", np.round(st_, 3).tolist(), "bin box", [np.round(v_, 3).tolist() for v_ in obj_box(bn_)], flush=True)
mon_start(target=None)
try:
    walk_tight(st_)
except (Abort, RuntimeError) as ex_:
    print("walk ERR", str(ex_)[:200], flush=True)
MON["on"] = False
print("at", state(), "corner rel", np.round(rel(np.r_[G_, 0.0]), 3).tolist(), flush=True)
print(look3("x07_paper1_stance"), flush=True)
