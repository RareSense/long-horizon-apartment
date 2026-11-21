print("DESC keys", list(DESC.keys())[:20], flush=True)
for k_, v_ in DESC["destinations"].items():
    if "wall" in str(v_).lower():
        print(k_, v_, (DESC.get("spots") or {}).get(k_), flush=True)
# static boxes of the scene near the hall: what are the obstacles round the umbrella route
for b_, inf_ in INFO["bodies"].items():
    try: lo_, hi_ = obj_box(b_)
    except Exception: continue
    c_ = (lo_ + hi_) / 2
    if -0.5 < c_[0] < 4.5 and -2.9 < c_[1] < -0.4 and lo_[2] < 0.3:
        print("B", b_, inf_.get("display"), np.round(lo_, 2).tolist(), np.round(hi_, 2).tolist(), "dyn", inf_.get("dynamic", inf_.get("kind")), flush=True)
