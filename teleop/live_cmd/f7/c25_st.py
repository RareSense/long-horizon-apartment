zz_b = body_of("r105i2_shoe")
gp_ = grasp_plan(zz_b)

def zz_t():
    out_ = []
    for o in (gp_.get("options") or [gp_]):
        heads = [float(np.arctan2(c[1], c[0])) + s_ * np.pi / 2 for c in o["closes"] for s_ in (-1, 1)] if o["closes"] else None
        for sd in SIDES:
            for sq in (True, False):
                for co in (True, False):
                    g, c_ = stance_for(o["point"], sd, X_REL, Y_REL, ignore=(zz_b,), headings=heads, squat=sq, clear_of=(obj_rect(zz_b),) if co else (), with_cost=True)
                    out_.append((np.round(o["point"], 2).tolist(), sd, sq, co, None if g is None else np.round(g, 2).tolist()))
    return out_
for r_ in with_tight(zz_t): print(r_, flush=True)
g_ = with_tight(lambda: room_grid((zz_b,)))
print("free (3.88,-2.10)", with_tight(lambda: (room_grid((zz_b,)).free(np.array([3.88, -2.10])), room_grid((zz_b,)).free(np.array([3.88, -2.10]), -0.07))), flush=True)
