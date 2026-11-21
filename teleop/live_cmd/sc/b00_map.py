MON["on"] = False
def zz_ascii(x0, x1, y0, y1, st=0.1, tight=True):
    g_ = with_tight(lambda: room_grid(())) if tight else room_grid(())
    rows_ = []
    for y_ in np.arange(y1, y0 - 1e-6, -st):
        rows_.append(f"{y_:6.2f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(x0, x1 + 1e-6, st)))
    rows_.append("       " + "".join(str(int(round(x_ * 10)) % 10) for x_ in np.arange(x0, x1 + 1e-6, st)))
    return "\n".join(rows_)
print("x from -5.6 to 4.4 step 0.1 (digit = tenths of x); tight grid", flush=True)
print(zz_ascii(-5.6, 4.4, -2.7, 1.9), flush=True)
for b_ in INFO["bodies"]:
    try: c_ = centre(b_)
    except Exception: continue
    if -6 < c_[0] < 5 and -3 < c_[1] < 2.5 and c_[2] < 1.2:
        lo_, hi_ = obj_box(b_)
        print("loose", b_, str(INFO["bodies"][b_].get("display"))[:18], np.round(c_, 2).tolist(), np.round(lo_[:2], 2).tolist(), np.round(hi_, 2).tolist(), flush=True)
