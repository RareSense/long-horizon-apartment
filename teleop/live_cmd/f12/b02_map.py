ub_ = body_of("r106i1_umbrella")
g_ = with_tight(lambda: room_grid((ub_,)), rb0=0.12, rf0=0.06)
print("grid rb0 0.12 ignoring the umbrella; columns x from -3.0 step 0.1 to 4.4")
print("      " + "".join(str(int(abs(round(xx_)) % 10)) if abs(xx_ - round(xx_)) < 0.01 else " " for xx_ in np.arange(-3.0, 4.41, 0.1)))
for yy_ in np.arange(2.0, -2.85, -0.1):
    print(f"{yy_:6.2f}", "".join("." if g_.free(np.array([xx_, yy_])) else "#" for xx_ in np.arange(-3.0, 4.41, 0.1)), flush=True)
print(close(os.path.join(TELE_DIR, "f12_west_hall.jpg"), np.array([1.8, -1.2, 2.0]), np.array([-1.5, -0.2, 0.0]), "west"), flush=True)
