zz_b = body_of("r178i1_ball"); zz_sd = "left"
mon_start(target=zz_b)
zz_out = {}
try:
    if ZZ_STEP:
        r_ = tmove(fwd=ZZ_STEP, tag="ball_step"); zz_out["step"] = (r_["at"], r_["yaw_deg"], r_["touch"]["body"])
    print("ball rel", np.round(rel(centre(zz_b)), 3).tolist(), flush=True)
    gp_ = grasp_plan(zz_b); p_, yaw_ = base(); lat_ = RM.rz(yaw_)[:, 1]
    gp_ = grasp_plan(zz_b, near=lat_) or gp_
    cd_ = max(gp_["closes"], key=lambda c: abs(c @ lat_)) if gp_["closes"] else lat_
    cd_ = cd_ if cd_ @ lat_ >= 0 else -cd_
    Q_ = {zz_sd: q_(R_down(cd_))}
    open_jaws(zz_sd, T=0.2)
    PRE_ACTION("crouch", {}); crouch(0.0, ZZ_LEAN, T=1.5)
    PRE_ACTION("servo_pads", {}); e1_ = servo_pads(zz_sd, gp_["point"][:2], gp_["top"] + 0.06, Q_, speed=0.2)
    PRE_ACTION("servo_pads", {}); e2_ = servo_pads(zz_sd, gp_["point"][:2], gp_["z"], Q_, speed=0.08)
    zz_out.update(e1=np.round(e1_, 3).tolist(), e2=np.round(e2_, 3).tolist(), point=np.round(gp_["point"], 3).tolist(), z=round(float(gp_["z"]), 3))
    print("approach", zz_out, "state", state(), flush=True)
    print(look_hand(zz_sd, "ball_down"), flush=True)
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, "fell", fallen(), "touch", contact_report()["body"], flush=True)
