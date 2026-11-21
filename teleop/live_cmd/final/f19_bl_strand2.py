# strand retry (AI teleop fix): the left hand reaches only ~0.35 m ahead at the strand height (0.76 m) from the west
# stance; reload the strand stage's checkpoint and choose the strand point within x <= 0.36 (robot frame).
zz_n = "r117i1_blanket"; zz_h = laundry_body()
CK_RELOAD = os.path.join(CK_DIR, "0940_act_bc_stage_strand")
ck_load(CK_RELOAD); gait_on(); op.run(0.3)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print("sync", ex_)
print("RELOADED", CK_RELOAD, "frame", rec.n, state(), "LOCK", list(LOCK), flush=True)
if "_bc_strand_target0" not in globals():
    _bc_strand_target0 = bc_strand_target
BC_XMAX = globals().get("BC_XMAX", 0.36)


def bc_strand_target(name, cont, s2):
    P_ = bc_w(name).points(0); zs_ = bc_rim(cont) + BC_STRAND_DZ; sg2_ = bc_sg(s2)
    for dz_ in (0.011, 0.02, 0.03, 0.05):
        s_ = np.flatnonzero(np.abs(P_[:, 2] - zs_) < dz_)
        B_ = np.array([bc_to_rf(P_[i_]) for i_ in s_]) if len(s_) else np.zeros((0, 3))
        ok_ = (B_[:, 0] > 0.22) & (B_[:, 0] < BC_XMAX) if len(s_) else np.zeros(0, bool)
        if ok_.sum() >= 3:
            break
    if ok_.sum() < 3:
        return None
    s_, B_ = s_[ok_], B_[ok_]
    e_ = float((sg2_ * B_[:, 1]).max())
    xm_ = float(np.median(B_[:, 0]))
    k_ = int(np.argmin(np.abs(sg2_ * B_[:, 1] - (e_ - 0.04)) + 0.5 * np.abs(B_[:, 0] - xm_)))
    return int(s_[k_]), np.round(B_[k_], 3).tolist(), round(e_, 3)


print("target old", _bc_strand_target0(zz_n, zz_h, "left"), "new", bc_strand_target(zz_n, zz_h, "left"), flush=True)
BC["stage"] = "first_end"
zz_r = bigcloth_into(zz_n, s1="right", start="strand", stop_after="strand")
for r_ in zz_r:
    print("RESULT", {k_: (v_ if not isinstance(v_, (dict, list)) else str(v_)[:220]) for k_, v_ in r_.items() if k_ != "look"}, flush=True)
bc_strand_target = _bc_strand_target0
print("held L/R", cloth_held("left"), cloth_held("right"), "inside", in_container(zz_n, zz_h), "touch", contact_report(), "fell", fallen(), flush=True)
print("look", look_hand("left", "bl_strand2"), flush=True)
