print("ck", ck_save("n1_pocket_entry", kind="act", info=dict(note="robot at the hamper-pocket corridor entry (-1.45,-1.19) facing west, for the stocking (AI-operated)")), flush=True)
log_ = []
mon_start(target=None)
try:
    for k_ in range(12):
        p_ = base()[0]
        if p_[0] < -2.60:
            break
        r_ = tmove(fwd=min(0.12, float(p_[0]) + 2.62), side=float(np.clip(float(p_[1]) + 1.19, -0.04, 0.04)) * -1.0, turn=float(np.clip(180.0 - (np.degrees(base()[1]) % 360.0), -10, 10)), tag=f"n1_west{k_}")
        c_ = contact_report(); log_.append((np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), c_["body"], c_["body_who"]))
        if c_["body"] > 3.0:
            break
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
for l_ in log_:
    print("MV", l_, flush=True)
print("state", state(), "fell", fallen(), "stocking", [np.round(v_, 3).tolist() for v_ in garment_box("r190i1_stocking")], flush=True)
print(look3("n1_c07"), flush=True)
