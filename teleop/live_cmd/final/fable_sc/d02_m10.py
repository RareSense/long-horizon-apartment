# AI-operated (Fable escalation, scooter r126): the left finger pads' real size (how far can the bar sit off their middle),
# then move 10 backward (north) with the same cycle (bar to 0.25 right, left fingers tips-down, move).
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
PF = (-1.92, 0.55)
for b_ in FINGER["left"]:
    R_ = d.xmat[b_].reshape(3, 3)
    for g_ in range(m.ngeom):
        if int(m.geom_bodyid[g_]) == b_ and (m.geom_contype[g_] or m.geom_conaffinity[g_]):
            Rg_ = d.geom_xmat[g_].reshape(3, 3); fx_ = ts.ee_pose("left")[1]
            print("  finger", m.body(b_).name, "geom", g_, "type", int(m.geom_type[g_]), "size", np.round(m.geom_size[g_], 4).tolist(), "pos - pad_mid (hand frame x=fingers,y,z)", np.round(fx_.T @ (d.geom_xpos[g_] - pad_mid("left")), 4).tolist(),
                  "axes in hand frame", np.round(fx_.T @ Rg_, 2).tolist(), flush=True)
print("pads", [np.round(p_, 3).tolist() for p_ in pads("left")], "bar thick", round(scooter_parts(sc_)["bar_thick"], 4), flush=True)
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
try:
    latc(want=-0.24)
    prepitch(-12.0)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
mvto("m10", turn=float(np.degrees(wrapa(np.radians(-90.0) - base()[1]))), to=PF, step=0.15)
topview("d02")
