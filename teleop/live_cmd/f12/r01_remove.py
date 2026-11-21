exec(open(r"E:\urc_home\scripts\home\live\ops.py", encoding="utf-8").read())
import json as _js
RM40 = _js.load(open(r"C:\Users\raresense\sim_home\apartment\REMOVED_FOR_40.json", encoding="utf-8"))
NAMES40 = RM40["removed_sink_bound"] + RM40["removed_hard"]
gone_ids_ = {body_of(n_) for n_ in NAMES40}
before_ = {b_: d.xpos[m.body(b_).id].copy() for b_ in INFO["bodies"] if b_ not in gone_ids_}
rp_before_ = base()[0].copy()
PRE_ACTION("remove_bodies_40", dict(n=len(NAMES40)))
NEWPOS = remove_bodies(NAMES40)
op.run(2.0)
moved_ = []
for b_, p0_ in before_.items():
    dp_ = float(np.linalg.norm(d.xpos[m.body(b_).id] - p0_))
    if dp_ > 0.005:
        moved_.append((INFO["bodies"][b_].get("display"), round(dp_, 4)))
rest_ = {n_: (np.round(d.xpos[m.body(body_of(n_)).id], 3).tolist(), round(float(np.linalg.norm(d.qvel[m.jnt_dofadr[m.body_jntadr[m.body(body_of(n_)).id]]:][:3])), 4)) for n_ in NAMES40}
print("moved others", moved_, flush=True)
print("robot moved", round(float(np.linalg.norm(base()[0] - rp_before_)), 4), "state", state(), flush=True)
print("removed now", rest_, flush=True)
print("route left", [item_name(s_) for s_ in ROUTE[POS:]], flush=True)
print(close(os.path.join(TELE_DIR, "f12_r01_island.jpg"), np.array([1.8, -1.2, 1.9]), np.array([2.2, 0.0, 0.9]), "island after removal"), flush=True)
print(close(os.path.join(TELE_DIR, "f12_r01_hall.jpg"), np.array([0.6, -0.3, 1.6]), np.array([2.3, -1.3, 0.0]), "hall after removal"), flush=True)
print(close(os.path.join(TELE_DIR, "f12_r01_west.jpg"), np.array([-2.5, -1.8, 1.8]), np.array([-4.5, -0.5, 0.3]), "west after removal"), flush=True)
