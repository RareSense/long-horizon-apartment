def zz_strand(z, dz=0.025):
    """The cloth strand between the rim and the holding hand at height z: centre, principal axes and extents, uv."""
    P_ = zz_w().points(0); U_ = zz_uv()
    s_ = np.flatnonzero(np.abs(P_[:, 2] - z) < dz)
    if len(s_) < 5:
        return None
    X_ = P_[s_]; c_ = X_.mean(0)
    ev_, V_ = np.linalg.eigh(np.cov((X_ - c_).T))
    o_ = np.argsort(-ev_)
    ax_ = V_[:, o_]; ex_ = [float(np.ptp((X_ - c_) @ ax_[:, k_])) for k_ in range(3)]
    return dict(n=len(s_), c=np.round(c_, 3).tolist(), ax0=np.round(ax_[:, 0], 2).tolist(), ax1=np.round(ax_[:, 1], 2).tolist(), ax2=np.round(ax_[:, 2], 2).tolist(), ext=np.round(ex_, 3).tolist(),
                uv_mean=np.round(U_[s_].mean(0), 2).tolist(), uv_lo=np.round(U_[s_].min(0), 2).tolist(), uv_hi=np.round(U_[s_].max(0), 2).tolist(), rf=np.round(zz_to_rf(c_), 3).tolist())
op.run(1.0)
for zz_z in (0.64, 0.70, 0.76, 0.82, 0.90, 1.0):
    print("strand z", zz_z, zz_strand(zz_z), flush=True)
hc_ = obj_rect(zz_hb()).c
cc_ = np.array([-2.22, -1.82, 0.78])
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(4)]
close(t_[0], cc_ + np.array([0.75, 0.25, 0.25]), cc_, "strand from the east")
close(t_[1], cc_ + np.array([-0.7, 0.3, 0.3]), cc_, "strand from the west")
close(t_[2], cc_ + np.array([0.2, -0.7, 0.45]), cc_, "strand from the south")
close(t_[3], cc_ + np.array([0.05, 0.02, 0.9]), cc_, "strand from above")
print("look", zz_img(t_, "strand"), flush=True)
