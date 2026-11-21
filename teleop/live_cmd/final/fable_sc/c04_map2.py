# AI-operated (Fable escalation, scooter r126): top views of the route (no motion).
out_ = []
for k_, (ex_, ey_) in enumerate([(-1.9, -1.15), (-2.0, -0.1)]):
    pth_ = os.path.join(TELE_DIR, f"fsc_c04_map{k_}.jpg"); close(pth_, np.array([ex_, ey_ - 0.05, 2.38]), np.array([ex_, ey_, 0.0]), f"AI-operated | from above, centre ({ex_},{ey_})")
    out_.append(pth_)
print("MAPS", out_, flush=True)
for n_ in ("object_0265_body", "object_0268_body", "object_0329_body", "object_0125_body", "object_0124_body", "object_0127_body", "object_0229_body"):
    try:
        P_ = piece_points(n_)
        V_ = np.vstack(list(P_.values()))
        print("  ", n_, "pieces", len(P_), "xy lo", np.round(V_.min(0), 2).tolist(), "hi", np.round(V_.max(0), 2).tolist(), flush=True)
    except Exception as e_:
        print("  ", n_, str(e_)[:80], flush=True)
