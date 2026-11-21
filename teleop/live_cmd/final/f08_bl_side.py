# AI teleop out of the hamper pocket (boxed in: scooter r126 NE, rug toys NW): face east, side steps north to y -0.40.
log_ = []
r_ = tmove(turn=-14.8, tag="bl_face_east")
log_.append(("turn", state()["pelvis"], state()["yaw_deg"], contact_report()["body"]))
for k_ in range(7):
    p_ = base()[0]
    if p_[1] > -0.43:
        break
    dy_ = min(0.12, -0.40 - float(p_[1]))
    r_ = tmove(side=dy_, tag=f"bl_side{k_}")
    c_ = contact_report()
    log_.append(("side", np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), c_["body"], c_["body_who"]))
    if c_["body"] > 3.0 or fallen():
        break
for l_ in log_:
    print("MV", l_, flush=True)
print("END", state(), "near", near_things(0.6), "fell", fallen(), flush=True)
print(look3("bl_side_end"), flush=True)
