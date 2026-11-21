# read only: what stops the right jaws at 1.5 cm (AI-operated)
import mujoco as _mj
print("jaw right", round(float(jaw("right")), 4), "target", round(float(jaw_target["right"]), 4), "gap", round(gap("right"), 4), "| jaw left", round(float(jaw("left")), 4), "target", round(float(jaw_target["left"]), 4), "gap", round(gap("left"), 4), flush=True)
seen_ = {}
for i_ in range(d.ncon):
    c_ = d.contact[i_]
    b1_ = m.body(m.geom_bodyid[c_.geom1]).name; b2_ = m.body(m.geom_bodyid[c_.geom2]).name
    if "right" in b1_ or "right" in b2_ or "laundry" in b1_ or "laundry" in b2_:
        k_ = (b1_, b2_)
        seen_[k_] = min(seen_.get(k_, 1.0), float(c_.dist))
for k_, v_ in seen_.items():
    print("contact", k_, "dist", round(v_, 4), flush=True)
a_, b_ = pads("right")
print("pads world", np.round(a_, 3).tolist(), np.round(b_, 3).tolist(), "hamper c", np.round(obj_rect(zz_hb()).c, 3).tolist(), "pad r", [round(float(np.linalg.norm(x_[:2] - obj_rect(zz_hb()).c)), 3) for x_ in (a_, b_)], flush=True)
bid_ = m.body(zz_hb()).id
print("hamper body", zz_hb(), "pos", np.round(d.xpos[bid_], 3).tolist(), "ngeom", int((m.geom_bodyid == bid_).sum()), flush=True)
pm_ = pad_mid("right")
for g_ in np.flatnonzero(m.geom_bodyid == bid_):
    dd_ = float(np.linalg.norm(d.geom_xpos[g_] - pm_))
    if dd_ < 0.12:
        print("  hamper geom", int(g_), m.geom(g_).name, "type", int(m.geom_type[g_]), "size", np.round(m.geom_size[g_], 3).tolist(), "pos", np.round(d.geom_xpos[g_], 3).tolist(), "rf", np.round(zz_to_rf(d.geom_xpos[g_]), 3).tolist(), "dist to pad mid", round(dd_, 3), flush=True)
print("right hand qpos-related: jaw joint names", [m.joint(j_).name for j_ in range(m.njnt) if "right" in m.joint(j_).name and ("jaw" in m.joint(j_).name.lower() or "finger" in m.joint(j_).name.lower() or "grip" in m.joint(j_).name.lower() or "Joint" in m.joint(j_).name)][:8], flush=True)
