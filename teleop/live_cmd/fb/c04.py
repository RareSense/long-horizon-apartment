def zz_spine(us=(-0.08, -0.04, 0.0, 0.04, 0.08, 0.12), vs=(-0.1, 0.0, 0.1)):
    P_ = zz_w().points(0); U_ = zz_uv(); out_ = []
    for u_ in us:
        row_ = []
        for v_ in vs:
            i_ = int(np.argmin(np.linalg.norm(U_ - np.array([u_, v_]), axis=1)))
            row_.append(f"[{i_}: {P_[i_,0]:.3f} {P_[i_,1]:.3f} {P_[i_,2]:.3f}]")
        out_.append(f"u {u_:+.2f}: " + " ".join(row_))
    return out_
ZZ_TARGETS = ZZ_T1
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\b20.py", encoding="utf-8").read())
op.run(1.5)
for l_ in zz_spine():
    print(l_, flush=True)
for zz_z in (0.66, 0.72, 0.80):
    print("strand z", zz_z, zz_strand(zz_z), flush=True)
cc_ = np.array([-2.22, -1.78, 0.74])
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.75, 0.15, 0.2]), cc_, "strand from the east")
close(t_[1], cc_ + np.array([0.3, -0.7, 0.35]), cc_, "strand from the south")
close(t_[2], cc_ + np.array([0.05, 0.02, 0.9]), cc_, "strand from above")
print("look", zz_img(t_, "strand2"), flush=True)
