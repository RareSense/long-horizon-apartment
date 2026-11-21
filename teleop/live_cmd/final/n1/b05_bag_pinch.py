zz_b = body_of("r196i1_plastic_bag"); SD = "left"; OT = "right"
C_, c_, z0_, z1_ = flat_corners(zz_b); zp_ = float(z0_ + 0.4 * (z1_ - z0_))
pl_ = corner_pinch_plan(zz_b, 3, SD)[0]; G_ = pl_["G"]; cd_ = pl_["cd"]
o_ = dict(G=np.round(G_, 3).tolist(), zp=round(zp_, 4))
mon_start(target=zz_b)
try:
    p_, yaw_ = base(); fw_ = RM.rz(yaw_)[:, 0]; lat_ = RM.rz(yaw_)[:, 1]
    T_ = p_ + 0.30 * fw_ - 0.12 * lat_; T_[2] = 0.42
    PRE_ACTION("park_other_hand", dict(side=OT, at=np.round(T_, 3).tolist()))
    op.move({OT: T_.tolist()}, speed=0.15, timeout=3.0, tol=0.02); op.run(0.3)
    o_["other_at"] = np.round(ts.ee_pose(OT)[0], 3).tolist()
    open_jaws(SD, T=0.3)
    PRE_ACTION("crouch", dict(CROUCH)); crouch(T=1.8, **CROUCH)
    o_["other_after_crouch"] = np.round(ts.ee_pose(OT)[0], 3).tolist()
    Q_ = {SD: q_(R_down(cd_))}
    PRE_ACTION("servo_pads", {}); o_["e_above"] = np.round(servo_pads(SD, G_, pl_["top"] + 0.06, Q_, speed=0.2), 4).tolist()
    PRE_ACTION("servo_pads", {}); o_["e_down"] = np.round(servo_pads(SD, G_, zp_, Q_, speed=0.06), 4).tolist()
    o_["look_open"] = look_grasp(zz_b, SD, "n1_corner_open")
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
print("OUT", o_, "state", state(), "touch", contact_report()["body_who"], "bag", np.round(centre(zz_b), 3).tolist(), flush=True)
