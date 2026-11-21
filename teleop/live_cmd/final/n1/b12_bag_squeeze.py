ZZ_Z = 0.024
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\n1\two_lib.py", encoding="utf-8").read())
zz_b = body_of("r196i1_plastic_bag"); ZZ_Z = globals().get("ZZ_Z", 0.032)
C_, c_, z0_, z1_ = flat_corners(zz_b)
E_ = [(C_[i], C_[(i + 1) % 4]) for i in range(4)]
L_ = [float(np.linalg.norm(b - a)) for a, b in E_]
sh_ = sorted(range(4), key=lambda i: L_[i])[:2]                     # the two short edges
mids_ = [0.5 * (E_[i][0] + E_[i][1]) for i in sh_]
lat_ = RM.rz(base()[1])[:2, 1]
mL_, mR_ = (mids_[0], mids_[1]) if (mids_[0] - mids_[1]) @ lat_ > 0 else (mids_[1], mids_[0])
u_ = (mR_ - mL_) / np.linalg.norm(mR_ - mL_)                        # left -> right
zz_Q = {s_: q_(R_down(np.r_[u_, 0.0])) for s_ in SIDES}
zz_out = dict(short=[round(L_[i], 3) for i in sh_], mL=np.round(mL_, 3).tolist(), mR=np.round(mR_, 3).tolist())
mon_start(target=zz_b); MON["ignore_names"] = (zz_b,)
try:
    PRE_ACTION("close_jaws", {}); close_jaws("left", 10.0, T=0.4); close_jaws("right", 10.0, T=0.4)
    PRE_ACTION("crouch", dict(CROUCH)); crouch(T=1.8, **CROUCH)
    PRE_ACTION("hands_above", {})
    servo_pads("left", mL_ - 0.04 * u_, ZZ_Z + 0.10, zz_Q, speed=0.15, n=2)
    servo_pads("right", mR_ + 0.04 * u_, ZZ_Z + 0.10, zz_Q, speed=0.15, n=2)
    PRE_ACTION("hands_down", {})
    eL_ = servo_pads("left", mL_ - 0.035 * u_, ZZ_Z, zz_Q, speed=0.05, n=3)
    eR_ = servo_pads("right", mR_ + 0.035 * u_, ZZ_Z, zz_Q, speed=0.05, n=3)
    zz_out.update(eL=np.round(eL_, 3).tolist(), eR=np.round(eR_, 3).tolist(), padL=np.round(pad_mid("left"), 3).tolist(), padR=np.round(pad_mid("right"), 3).tolist())
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, "bag", np.round(centre(zz_b), 3).tolist(), "state", state(), "touch", contact_report()["body_who"], "fell", fallen(), flush=True)
print(look_hand("right", "n1_bag_paddles"), flush=True)
