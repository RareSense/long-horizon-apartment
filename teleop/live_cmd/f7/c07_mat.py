for i_ in range(m.nbody):
    n_ = m.body(i_).name
    if "119" in n_ or "mat" in n_.lower() or "rug" in n_.lower():
        print("body", i_, n_, np.round(d.xpos[i_], 3).tolist(), flush=True)
for g_ in range(m.ngeom):
    n_ = m.geom(g_).name
    if "119" in n_ or "doormat" in n_.lower():
        print("geom", n_, np.round(d.geom_xpos[g_], 3).tolist(), np.round(m.geom_size[g_], 3).tolist(), int(m.geom_type[g_]), flush=True)
print("spots", [ (k_, v_) for k_, v_ in (DESC.get("spots") or {}).items()][:6] if isinstance(DESC.get("spots"), dict) else type(DESC.get("spots")), flush=True)
