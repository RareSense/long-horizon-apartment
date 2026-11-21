exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\gait3\setup.py", encoding="utf-8").read())
gt_reload_gait(hold=False, plan=True)
def far_free(Lmax=2.6):
    p_, y_ = base(); g_ = room_grid(()); best = (0.0, None)
    for a_ in np.linspace(0, 2 * np.pi, 24, endpoint=False):
        u_ = np.array([np.cos(a_), np.sin(a_)])
        for L_ in np.arange(Lmax, 0.55, -0.1):
            q_ = p_[:2] + L_ * u_
            if g_.free(q_) and g_.line_free(p_[:2], q_):
                if L_ > best[0]:
                    best = (float(L_), (float(q_[0]), float(q_[1]), float(a_)))
                break
    return best
for ck_ in ("0022_act_walk_leg", CK111):
    for plan_on_ in (True, False):
        ts.loco.g["plan"] = plan_on_
        gt_load(ck_); GT_PRE()
        p0_, y0_ = base(); home_ = (float(p0_[0]), float(p0_[1]), float(y0_))
        L_, far_ = far_free()
        if far_ is None:
            print("WP", os.path.basename(ck_)[:4], "no free line"); continue
        for nm_, tgt_ in (("out", far_), ("home", home_)):
            del WALK_LOG[:]
            t0_ = float(d.time); GT.update(on=True, rows=[], k=0, touch=0.0, touch_who=None)
            try:
                r_ = walk_path(tgt_)
            except Exception as ex:
                r_ = dict(error=str(ex)[:200])
            GT["on"] = False
            p_, y_ = base()
            print("WP", os.path.basename(ck_)[:4], "plan", plan_on_, nm_, f"{L_:.1f} m", {k_: v_ for k_, v_ in r_.items() if k_ in ("error", "steppings")}, "end err cm", round(100 * float(np.hypot(p_[0] - tgt_[0], p_[1] - tgt_[1])), 1),
                  "yaw err deg", round(float(np.degrees(wrapa(tgt_[2] - y_))), 1), "sim s", round(float(d.time) - t0_, 1), "fell", fallen(), "touch", GT["touch"], GT["touch_who"],
                  "legs (L, s, v, off)", [(w_["L"], w_["s"], w_["v"], w_["off"]) for w_ in WALK_LOG], flush=True)
            if fallen():
                break
ts.loco.g["plan"] = True
