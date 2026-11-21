TWO["on"] = False
print("bag", np.round(centre(zz_b), 3).tolist(), "box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "padL", np.round(pad_mid("left"), 3).tolist(), "padR", np.round(pad_mid("right"), 3).tolist(), flush=True)
for s_ in SIDES:
    print(s_, "finger tips z", {b_: round(float(d.xpos[m.body(f"{s_}_Dex1_{b_}").id][2]), 3) for b_ in ("finger_link_1", "finger_link_2", "base_link")}, flush=True)
    gs_ = [g_ for g_ in range(m.ngeom) if m.body(int(m.geom_bodyid[g_])).name.startswith(f"{s_}_Dex1_finger")]
    import mujoco as _mj
    zl_ = min(float((d.geom_xpos[g_] - np.abs(d.geom_xmat[g_].reshape(3, 3)) @ m.geom_size[g_])[2]) if m.geom_type[g_] != 7 else 9 for g_ in gs_)
    print(s_, "finger geoms lowest approx", round(zl_, 3), "ts.touch", ts.touch.get(s_), flush=True)
print("state", state(), flush=True)
