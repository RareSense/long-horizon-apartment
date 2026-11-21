exec(open(r'E:\urc_final\scripts\home\final_run\common_b.py', encoding='utf-8').read())
zz_b = body_of("r196i1_plastic_bag"); zid_ = m.body(zz_b).id
print("bag mass", round(float(m.body_subtreemass[zid_]), 3), "friction", [np.round(m.geom_friction[g_], 2).tolist() for g_ in range(m.ngeom) if m.geom_bodyid[g_] == zid_][:2], flush=True)
C_, c_, z0_, z1_ = flat_corners(zz_b)
yaw_ = np.radians(-70.0); f_ = np.array([np.cos(yaw_), np.sin(yaw_)])
for dd_ in (0.30, 0.33, 0.36):
    P_ = c_ - dd_ * f_
    print("stance", dd_, np.round(P_, 3).tolist(), "free", bool(with_tight(lambda: room_grid((zz_b,)).free(P_))), flush=True)
_start_item("r196i1_plastic_bag")
P_ = c_ - 0.33 * f_
mon_start(target=zz_b)
try:
    w_ = walk_tight((float(P_[0]), float(P_[1]), float(yaw_)))
    print("walk", {k_: w_.get(k_) for k_ in ("ok", "err_xy")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("state", state(), "fell", fallen(), "touch", contact_report()["body_who"], "bag", np.round(centre(zz_b), 3).tolist(), flush=True)
if not fallen() and not MON.get("why"):
    print("ck", ck_save("n1_bag_north_stance", kind="act", info=dict(note="north of the plastic bag facing -70 deg for a two-hand edge squeeze (AI-operated)")), flush=True)
print(look3("n1_b10"), flush=True)
