print("ck", ck_save("fb_right_at_fold_before_close", kind="act"), flush=True)
zz_r = zz_close_lock("right")
print("close_lock", zz_r, flush=True)
for sd_ in SIDES:
    if sd_ in LOCK:
        hu_ = zz_uv()[LOCK[sd_][1]]
        print(sd_, "held n", len(hu_), "uv mean", np.round(hu_.mean(0), 2).tolist(), flush=True)
if "right" in LOCK and "left" in LOCK:
    H_ = np.vstack([zz_uv()[LOCK["left"][1]], zz_uv()[LOCK["right"][1]]])
    Ua_ = zz_uv(); dmin_ = np.min(np.linalg.norm(Ua_[:, None, :] - H_[None, :, :], axis=2), axis=1)
    far_ = Ua_[:, 0] > 0.1
    print("farthest sheet point from the two holds:", round(float(dmin_.max()), 3), "at", np.round(Ua_[np.argmax(dmin_)], 2).tolist(), "| on the far side (u > 0.1):", round(float(dmin_[far_].max()), 3), "at", np.round(Ua_[far_][np.argmax(dmin_[far_])], 2).tolist(), flush=True)
print("touch", contact_report(), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "tilt", round(pelvis_tilt(), 3), flush=True)
print("look", zz_look(np.array([-2.2, -1.8, 0.8]), "both_locked", dist=1.3, h=0.7, dirs=(20.0, 160.0), top=True), flush=True)
