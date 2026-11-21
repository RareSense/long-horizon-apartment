# reload before the fold grasp (it took the first end, not the far corner) and map the far end near the rim (AI-operated)
CK_RELOAD = os.path.join(CK_DIR, "1312_act_g_before_fold")
print("frame before load", rec.n, flush=True)
ck_load(CK_RELOAD); gait_on(); op.run(0.3); sync_cloth(force=True)
print("RELOADED", CK_RELOAD, "frame", rec.n, flush=True)
print("held L/R", cloth_held("left"), cloth_held("right"), "LOCK", {s_: len(LOCK[s_][1]) for s_ in LOCK}, "HELD", HELD, "inside", in_container(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), "fell", fallen(), flush=True)
P_ = zz_w().points(0); U_ = zz_uv(); hc_, hr_ = bc_wall(zz_hb())
B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); rr_ = np.linalg.norm(P_[:, :2] - hc_, axis=1)
print("grid of the far end: rows u, columns v; cell = rf x, y, z and r from the hamper centre (wall r %.3f)" % hr_, flush=True)
for u_ in (0.10, 0.20, 0.28, 0.34, 0.40, 0.46, 0.50):
    row_ = []
    for v_ in (-0.375, -0.30, -0.22, -0.14, -0.06, 0.04, 0.2):
        i_ = int(np.argmin(np.linalg.norm(U_ - np.array([u_, v_]), axis=1)))
        row_.append(f"[{i_}: {B_[i_,0]:.2f} {B_[i_,1]:+.2f} {B_[i_,2]:.2f} r{rr_[i_]:.2f}]")
    print(f"u {u_:+.2f}: " + " ".join(row_), flush=True)
print("first end:", flush=True)
for u_ in (-0.50, -0.44, -0.36):
    row_ = []
    for v_ in (-0.375, -0.2, 0.0, 0.2, 0.375):
        i_ = int(np.argmin(np.linalg.norm(U_ - np.array([u_, v_]), axis=1)))
        row_.append(f"[{i_}: {B_[i_,0]:.2f} {B_[i_,1]:+.2f} {B_[i_,2]:.2f} r{rr_[i_]:.2f}]")
    print(f"u {u_:+.2f}: " + " ".join(row_), flush=True)
for s_ in SIDES:
    Rn_ = ts.ee_pose(s_)[1]
    print(s_, "pad rf", np.round(zz_to_rf(pad_mid(s_)), 3).tolist(), "fingers rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 0], 2).tolist(), "gap", round(gap(s_), 3), flush=True)
print("right shoulder rf", np.round(zz_to_rf(d.xpos[m.body("right_shoulder_pitch_link").id]), 3).tolist(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), flush=True)
cc_ = zz_rf((0.36, -0.14, 0.68))
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(4)]
close(t_[0], cc_ + np.array([-0.6, 0.3, 0.3]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.7]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.4, 0.3]), cc_, "from the south-west")
close(t_[3], cc_ + np.array([0.5, -0.35, 0.35]), cc_, "from the south-east")
print("look", zz_img(t_, "g16_far_end"), flush=True)
