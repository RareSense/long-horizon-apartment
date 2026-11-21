def zz_turn_test(hold, how):
    ck_load(ZZ_CK); gait_on(); ts.loco.g["hold"] = hold; mon_start(); MON["trace"] = []
    p0_, y0_ = base(); ex_ = None
    try:
        if how == "walk":
            walk((float(p0_[0]), float(p0_[1]), float(y0_ + np.pi / 2)))
        else:
            tmove(turn=15.0, tag="v15")
    except Exception as ex:
        ex_ = str(ex)[:120]
    p1_, y1_ = base()
    print("TEST hold", hold, how, dict(moved_m=round(float(np.linalg.norm(p1_[:2] - p0_[:2])), 3), dyaw=round(float(np.degrees(wrapa(y1_ - y0_))), 1), ex=ex_,
          he=np.round(getattr(ts.loco, "hold_err", np.zeros(2)), 3).tolist()), "trace", MON["trace"][::4][:14], flush=True)
    MON["trace"] = None; MON["on"] = False


zz_turn_test(True, "t15")
zz_turn_test(False, "walk")
