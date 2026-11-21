M_ = br.mjm
planes_ = [(g_, M_.geom(g_).name, np.round(M_.geom_size[g_], 2).tolist(), np.round(br.mjd.geom_xpos[g_], 2).tolist()) for g_ in range(M_.ngeom) if int(M_.geom_type[g_]) == 0]
print("planes", planes_[:5], flush=True)
import json as _js
RM40 = _js.load(open(r"C:\Users\raresense\sim_home\apartment\REMOVED_FOR_40.json", encoding="utf-8"))
NAMES40 = RM40["removed_sink_bound"] + RM40["removed_hard"]
for n_ in NAMES40:
    b_ = body_of(n_)
    ok_ = b_ in INFO["bodies"]
    j_ = m.body(b_).jntadr if ok_ else None
    print(n_, b_, ok_, "jnt", (int(m.body_jntnum[m.body(b_).id]), int(m.jnt_type[m.body_jntadr[m.body(b_).id]])) if ok_ else None, "at", np.round(centre(b_), 2).tolist() if ok_ else None, flush=True)
print("route left", [item_name(s_) for s_ in ROUTE[POS:]], flush=True)
