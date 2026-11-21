zz_rec = dict(status="done", how="Fable's park_scooter_hang carry (16 moves, verified) + AI-teleop finish: the call's 6th set-down leg lost the left jaw twice in a row (both runs), so from the checkpoint before that leg (0864) the right jaw's squeeze was eased to re-seat the bar (seat -14.9 mm at the pad edge, pitch 41 deg); the bar left both jaws and the scooter came down the last ~2 cm onto its front wheel, standing (tilt 1.2 deg, 3 pieces on the floor); hands off, 2 steps back, 2 side steps (AI-operated)",
              box=[np.round(v_, 3).tolist() for v_ in obj_box(SB)], tilt_deg=sh_state(SB)["tilt"])
c_ = (obj_box(SB)[0] + obj_box(SB)[1]) / 2
zz_d = item_done_auto("r126i1_scooter", zz_rec, spot=(float(c_[0]), float(c_[1])))
print("DONE", zz_d, flush=True)
print("state", state(), "kit", kit_mem(), flush=True)
