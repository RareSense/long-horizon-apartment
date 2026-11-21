zz_ck = [c_ for c_ in CK_LOG if c_.get("name") == "crouch_holding"][-1]["path"]
print("load", zz_ck, flush=True)
ck_load(zz_ck); gait_on(); settle_after_load()
print("state", state(), "tilt", round(pelvis_tilt(), 3), "held", dict(HELD), "fell", fallen(), flush=True)
for r_ in scene_rects(()):
    if "119" in str(getattr(r_, "name", "")) or "mat" in str(INFO["bodies"].get(getattr(r_, "name", None), {}).get("display", "")):
        print("MAT", getattr(r_, "name", None), np.round(r_.c, 3).tolist(), np.round(r_.h, 3).tolist(), round(float(getattr(r_, "yaw", 0)), 2), r_.low, flush=True)
for n_ in ("left_ankle_roll_link", "right_ankle_roll_link"):
    print(n_, np.round(d.xpos[m.body(n_).id], 3).tolist(), flush=True)
print("look", look3("sandal_before_crouch"), flush=True)
