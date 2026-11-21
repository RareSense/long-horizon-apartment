zz_b = body_of("r178i1_ball")
for rb0_ in (0.22, 0.18):
    g_ = with_tight(lambda: room_grid((zz_b,)), rb0=rb0_, rf0=0.12)
    print("rb0", rb0_, "x from -6.3 step 0.1 (col 0 = -6.3)")
    for yy_ in np.arange(-0.6, -2.65, -0.1):
        print(f"{yy_:6.2f}", "".join("o" if np.hypot(xx_ + 5.795, yy_ + 2.123) < 0.06 else ("." if g_.free(np.array([xx_, yy_])) else "#") for xx_ in np.arange(-6.3, -4.39, 0.1)), flush=True)
print(close(os.path.join(TELE_DIR, "corner_top.jpg"), np.array([-5.4, -1.6, 2.8]), np.array([-5.45, -1.75, 0.0]), "corner top"), flush=True)
