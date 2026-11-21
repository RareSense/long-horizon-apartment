zz_n = "r116i1_coat_pile"
zz_P = bc_w(zz_n).points(0); zz_U = bc_uv(zz_n)
print("REACH", REACH_X, REACH_Y, "R tight", flush=True)
def zz_try():
    own_ = garment_rect(zz_n); out_ = []
    print("own rect", np.round(own_.c, 3).tolist(), np.round(own_.h, 3).tolist(), round(float(own_.yaw), 2), flush=True)
    for u_ in (-0.4, -0.2, 0.0, 0.2, 0.4):
        ii_ = int(np.argmin(np.linalg.norm(zz_U - np.array([u_, 0.36]), axis=1)))
        pt = np.r_[zz_P[ii_][:2], 0.0]
        for sd in SIDES:
            for xr, yr in ((0.17, 0.27), (0.24, 0.24), (0.30, 0.20), (0.34, 0.14)):
                for co in (True, False):
                    g_, c_ = stance_for(pt, sd, xr, yr, ignore=(zz_n,), with_cost=True, squat=True, clear_of=(own_,) if co else ())
                    if g_ is not None:
                        out_.append((u_, sd, xr, yr, co, np.round(pt[:2], 2).tolist(), np.round(g_, 2).tolist(), round(float(c_), 2)))
    return out_
for r_ in with_tight(zz_try): print(r_, flush=True)
