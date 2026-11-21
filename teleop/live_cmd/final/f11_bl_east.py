# AI teleop out of the hamper pocket EAST along y -1.17 (scooter r126 north: its stem at y -0.68; handlebar high)
log_ = []
tmove(turn=-14.8, tag="bl_face_east")
log_.append(("turn", np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), contact_report()["body"]))
tmove(side=-0.05, tag="bl_side_s")
log_.append(("side", np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), contact_report()["body"]))
for k_ in range(9):
    p_ = base()[0]
    if p_[0] > -1.62:
        break
    y_err = -1.17 - float(p_[1])
    tmove(fwd=min(0.12, -1.6 - float(p_[0])), side=float(np.clip(y_err, -0.04, 0.04)), turn=float(np.clip(-np.degrees(base()[1]), -10, 10)), tag=f"bl_east{k_}")
    c_ = contact_report()
    log_.append(("fwd", np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), c_["body"], c_["body_who"]))
    if c_["body"] > 3.0 or fallen():
        break
for l_ in log_:
    print("MV", l_, flush=True)
print("END", state(), "near", near_things(0.6), "fell", fallen(), "scooter", np.round(centre(body_of("r126i1_scooter")), 3).tolist(), flush=True)
print(look3("bl_east_end"), flush=True)
