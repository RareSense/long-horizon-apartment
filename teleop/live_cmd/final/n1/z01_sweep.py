res_ = {}; bad_ = []
for nm_ in list(DONE):
    if not isinstance(nm_, str):
        nm_ = item_name(nm_)
    c_ = item_check(nm_)
    res_[nm_] = c_
    if c_.get("ok") is False:
        bad_.append(nm_)
sb_ = body_of("r130i1_light_saber"); off_sb_ = float(np.linalg.norm(centre(sb_)[:2] - np.array([-4.92, -1.405])))
bx_ = body_of("r175i1_cardboard_box"); off_bx_ = float(np.linalg.norm(centre(bx_)[:2] - np.array([-5.25, 1.56])))
bag_ = body_of("r196i1_plastic_bag")
print("SWEEP done", len(DONE), "check-False", bad_, flush=True)
for k_, v_ in res_.items():
    print(" ", k_, {kk_: v_.get(kk_) for kk_ in ("ok", "kind", "dest", "inside", "off_spot", "q")}, flush=True)
print("saber off spot", round(off_sb_, 3), "box off spot", round(off_bx_, 3), "bag at", np.round(centre(bag_), 3).tolist(), "route left", [item_name(s_) for s_ in ROUTE[POS:]], "state", state(), "fell", fallen(), flush=True)
import json as _js
open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\n1\sweep.json", "w").write(_js.dumps(dict(done=len(DONE), check_false=bad_, saber_off=off_sb_, box_off=off_bx_, checks={k_: {kk_: (vv_ if not isinstance(vv_, np.ndarray) else vv_.tolist()) for kk_, vv_ in v_.items()} for k_, v_ in res_.items()}), default=str, indent=1))
