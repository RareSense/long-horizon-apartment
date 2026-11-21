print(floor_first(["r175i1_cardboard_box"])[:3], flush=True)
import mujoco as _mj
zz_b = body_of("r175i1_cardboard_box")
# the wall north of the box: a ray from the box centre at 0.12 m height, north, static geoms only
zz_gid = np.zeros(1, np.int32)
for xx_ in (-5.35, -5.25, -5.15):
    dist_ = _mj.mj_ray(m, d, np.array([xx_, 1.40, 0.12]), np.array([0.0, 1.0, 0.0]), None, 1, m.body(zz_b).id, zz_gid)
    print("wall ray x", xx_, "dist", round(float(dist_), 3), "-> y", round(1.40 + float(dist_), 3), "geom", int(zz_gid[0]), m.body(int(m.geom_bodyid[zz_gid[0]])).name if zz_gid[0] >= 0 else None, flush=True)
mon_start(target=None)
try:
    r1_ = tmove(fwd=-0.12, tag="box_step_n")
    print("step n", r1_["at"], r1_["yaw_deg"], r1_["touch"], flush=True)
    r2_ = tmove(side=-0.12, tag="box_step_w")
    print("step w", r2_["at"], r2_["yaw_deg"], r2_["touch"], flush=True)
    w_ = walk_tight((-4.87, 1.08, np.pi / 2))
    print("walk", {k_: v_ for k_, v_ in w_.items() if k_ in ("ok", "err_xy", "err_yaw", "way_points")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
except RuntimeError as ex_:
    print("err", str(ex_)[:300], flush=True)
MON["on"] = False
print("state", state(), "fell", fallen(), "touch", contact_report(), "kit", kit_mem(), flush=True)
print(look3("box_stance"), flush=True)
