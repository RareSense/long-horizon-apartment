for g_ in ("r117i1_blanket", "r116i1_coat_pile"):
    P_ = GARMENTS[g_]["w"].points(0)
    print(g_, "box", [np.round(v_, 3).tolist() for v_ in garment_box(g_)], "centroid", np.round(P_.mean(0), 3).tolist(), "p136", np.round(P_[136], 3).tolist() if len(P_) > 136 else None, flush=True)
print("state", state(), "T", np.round(np.asarray(INFO["T"])[:3, 3], 3).tolist() if "T" in INFO else None, flush=True)
