zz_sb = body_of("r130i1_light_saber")
print("saber box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_sb)], "pieces", {k_: (np.round(V_.mean(0), 3).tolist(), round(float(V_[:, 2].max()), 3)) for k_, V_ in piece_points(zz_sb).items()}, "basket", [np.round(v_, 3).tolist() for v_ in obj_box(body_of("r186i1_basket"))], "touch with", flush=True)
import mujoco as _mj
zid_ = m.body(zz_sb).id
for i_ in range(br.mjd.ncon):
    c_ = br.mjd.contact[i_]; b1_ = br.mjm.geom_bodyid[c_.geom1]; b2_ = br.mjm.geom_bodyid[c_.geom2]
    if zid_ in (b1_, b2_):
        o_ = b2_ if b1_ == zid_ else b1_
        print(" contact", br.mjm.body(o_).name, np.round(c_.pos, 3).tolist(), flush=True)
c_ = centre(zz_sb); t_ = [os.path.join(TELE_DIR, f"_s{i}.jpg") for i in range(2)]
close(t_[0], c_ + np.array([0.6, 0.3, 0.6]), c_, "saber from the east"); close(t_[1], c_ + np.array([0.02, 0.0, 1.0]), c_, "saber from above")
TELE["n"] += 1; print(_strip(t_, os.path.join(TELE_DIR, f"{TELE['n']:04d}_saber_spot.jpg")), flush=True)
