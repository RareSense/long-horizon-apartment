MON["on"] = False
SDp = "right"; pb_ = body_of("r195i1_paper"); bn_ = body_of("rubbish_bin"); o_ = {}
mon_start(target=None); MON["held"][SDp] = pb_; MON["last_touch"][SDp] = float(d.time)
try:
    bc_ = centre(bn_); lo_, hi_ = obj_box(bn_)
    plo_, phi_ = obj_box(pb_); hang_ = float(pad_mid(SDp)[2] - plo_[2])
    Qp = {SDp: q_(R_down(np.array([0.0, 1.0, 0.0])))}
    for k_, (fx_, z_add) in enumerate([(0.5, 0.12), (1.0, 0.06)]):
        pm_ = pad_mid(SDp); tgt_ = pm_[:2] + fx_ * (bc_[:2] - pm_[:2]) if k_ == 0 else bc_[:2]
        PRE_ACTION("hand_over_bin", dict(stage=k_)); e_ = servo_pads(SDp, tgt_, float(hi_[2]) + hang_ + z_add, Qp, speed=0.06)
        o_[f"e{k_}"] = np.round(e_, 3).tolist(); o_[f"pad{k_}"] = np.round(pad_mid(SDp), 3).tolist()
    plo_, phi_ = obj_box(pb_)
    o_["over"] = bool(lo_[0] + 0.03 < plo_[0] and phi_[0] < hi_[0] - 0.03 and lo_[1] + 0.03 < plo_[1] and phi_[1] < hi_[1] - 0.03)
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
except RuntimeError as ex_:
    o_["error"] = str(ex_)[:300]
MON["on"] = False
o_.update(paper=np.round(centre(pb_), 3).tolist(), state=state(), touch=contact_report(), held=HOLD.holding(SDp), fell=fallen())
print("OVER", o_, flush=True)
print(look3("paper1_over"), flush=True)
