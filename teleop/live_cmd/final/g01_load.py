# Fable escalation, blanket (AI-operated): helpers + reload the checkpoint before the strand stage
for f_ in ("zz_help.py", "zz_grasp.py", "zz_arm.py", "zz_pin.py", "zz_tm.py"):
    exec(open(os.path.join(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb", f_), encoding="utf-8").read())


def zz_knees():
    return bc_knees(zz_hb())


def zz_strand(z, dz=0.025):
    P_ = zz_w().points(0); U_ = zz_uv()
    s_ = np.flatnonzero(np.abs(P_[:, 2] - z) < dz)
    if len(s_) < 5:
        return None
    B_ = np.array([zz_to_rf(P_[i_]) for i_ in s_])
    return dict(n=len(s_), rf_c=np.round(B_.mean(0), 3).tolist(), rf_lo=np.round(B_.min(0), 3).tolist(), rf_hi=np.round(B_.max(0), 3).tolist(),
                uv_mean=np.round(U_[s_].mean(0), 2).tolist(), uv_lo=np.round(U_[s_].min(0), 2).tolist(), uv_hi=np.round(U_[s_].max(0), 2).tolist())


CK_RELOAD = os.path.join(CK_DIR, "1164_act_bc_stage_strand")
print("frame before load", rec.n, flush=True)
ck_load(CK_RELOAD); gait_on(); op.run(0.3); sync_cloth(force=True)
print("RELOADED", CK_RELOAD, "frame", rec.n, flush=True)
print("stat", zz_stat(), flush=True)
hc_ = obj_rect(zz_hb()).c
print("hamper c", np.round(hc_, 3).tolist(), "r", bc_wall(zz_hb())[1], "rim", bc_rim(zz_hb()), "rf of centre", np.round(zz_to_rf(np.r_[hc_, 0.6]), 3).tolist(), "wall gap", round(float(np.linalg.norm(base()[0][:2] - hc_)) - bc_wall(zz_hb())[1], 3), flush=True)
for s_ in SIDES:
    print(s_, "pad rf", np.round(zz_to_rf(pad_mid(s_)), 3).tolist(), flush=True)
if "right" in LOCK:
    hu_ = zz_uv()[LOCK["right"][1]]
    print("right held n", len(hu_), "uv mean", np.round(hu_.mean(0), 2).tolist(), flush=True)
for z_ in (0.62, 0.68, 0.75, 0.82, 0.90, 1.0, 1.1):
    print("strand z", z_, zz_strand(z_), flush=True)
print("out", bc_out(zz_BL, zz_hb()), "knees", zz_knees(), "tilt", round(pelvis_tilt(), 3), "fell", fallen(), flush=True)
for n_ in ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket"):
    print(n_, item_check(n_), flush=True)
print("look", zz_look(np.array([hc_[0], hc_[1], 0.8]), "g01", dist=1.3, h=0.6, dirs=(0.0, 180.0, 270.0), top=True), flush=True)
print("look3", look3("g01_reload"), flush=True)
