# Fable escalation, coat pile r116 (AI-operated): helpers, reload the checkpoint before the strand stage, measure
for f_ in ("zz_help.py", "zz_grasp.py", "zz_arm.py", "zz_pin.py", "zz_tm.py"):
    exec(open(os.path.join(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb", f_), encoding="utf-8").read())
zz_BL = "r116i1_coat_pile"
ZZ_OTHERS = ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket", "r117i1_blanket")


def zz_knees():
    return bc_knees(zz_hb())


def zz_out_parts():
    P_ = zz_w().points(0); U_ = zz_uv(); hc_, hr_ = bc_wall(zz_hb())
    B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); rr_ = np.linalg.norm(P_[:, :2] - hc_, axis=1)
    o_ = rr_ > hr_
    out_ = dict(n=int(o_.sum()), share=round(float(o_.mean()), 3), below_rim=int((o_ & (P_[:, 2] < bc_rim(zz_hb()))).sum()))
    if o_.any():
        ang_ = np.degrees(np.arctan2(P_[o_, 1] - hc_[1], P_[o_, 0] - hc_[0]))
        out_.update(uv_lo=np.round(U_[o_].min(0), 2).tolist(), uv_hi=np.round(U_[o_].max(0), 2).tolist(), z=[round(float(P_[o_, 2].min()), 3), round(float(P_[o_, 2].max()), 3)],
                    rf_lo=np.round(B_[o_].min(0), 3).tolist(), rf_hi=np.round(B_[o_].max(0), 3).tolist(), ang=[round(float(ang_.min()), 0), round(float(ang_.max()), 0)], r_max=round(float(rr_[o_].max()), 3))
    return out_


def zz_others():
    return {n_: bool(item_check(n_)["ok"]) for n_ in ZZ_OTHERS}


CK_RELOAD = os.path.join(CK_DIR, "1785_act_bc_stage_strand")
print("frame before load", rec.n, flush=True)
ck_load(CK_RELOAD); gait_on(); op.run(0.3); sync_cloth(force=True)
print("RELOADED", CK_RELOAD, "frame", rec.n, flush=True)
print("stat", zz_stat(), flush=True)
U_ = zz_uv(); P_ = zz_w().points(0)
print("particles", len(P_), "uv lo/hi", np.round(U_.min(0), 2).tolist(), np.round(U_.max(0), 2).tolist(), "route item", item_name(ROUTE[POS]), "BC stage", BC.get("stage"), "CARRY_JOINTS", CARRY_JOINTS, flush=True)
hc_ = obj_rect(zz_hb()).c
print("hamper c", np.round(hc_, 3).tolist(), "wall gap", round(float(np.linalg.norm(base()[0][:2] - hc_)) - bc_wall(zz_hb())[1], 3), "knees", zz_knees(), "tilt", round(pelvis_tilt(), 3), flush=True)
for s_ in SIDES:
    Rn_ = ts.ee_pose(s_)[1]
    print(s_, "pad rf", np.round(zz_to_rf(pad_mid(s_)), 3).tolist(), "fingers rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 1], 2).tolist(), "gap", round(gap(s_), 4), flush=True)
if "right" in LOCK:
    print("right held uv", np.round(U_[LOCK["right"][1]], 2).tolist(), flush=True)
for z_ in (0.62, 0.68, 0.75, 0.82, 0.90, 1.0, 1.1):
    print("strand z", z_, zz_strand(z_), flush=True)
print("outside", zz_out_parts(), flush=True)
print("others", zz_others(), "fell", fallen(), flush=True)
# pile inside: heights of the other garments and of the coat inside
for n_ in ZZ_OTHERS:
    Pn_ = GARMENTS[n_]["w"].points(0)
    print("  ", n_, "z lo/hi", round(float(Pn_[:, 2].min()), 3), round(float(Pn_[:, 2].max()), 3), flush=True)
print("look", zz_look(np.array([hc_[0], hc_[1], 0.8]), "g50", dist=1.3, h=0.6, dirs=(20.0, 160.0, 100.0), top=True), flush=True)
