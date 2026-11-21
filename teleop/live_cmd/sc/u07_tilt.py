b_ = body_of("r107i1_umbrella")
V_ = _hull_pts(b_); print("now tilt", round(box_tilt_deg(b_), 1), "hull z", round(float(V_[:, 2].min()), 3), round(float(V_[:, 2].max()), 3), "c", np.round(centre(b_), 3).tolist(), flush=True)
import json as _j
m0_ = _j.load(open(os.path.join(RUN, "checkpoints", "1517_item_r105i2_shoe", "meta.json")))
print("meta keys", list(m0_.keys())[:20], flush=True)
