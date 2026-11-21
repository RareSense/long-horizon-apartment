MON["on"] = False
tb_ = body_of("r158i1_tissue"); c_ = centre(tb_)
print("tissue contacts", umb_contacts(tb_)[:6], flush=True)
for s_ in INFO["static"]:
    for bx in (s_.get("pieces") or s_["boxes"]):
        cc_ = np.asarray(bx["c"])
        if np.linalg.norm(cc_[:2] - c_[:2]) < 0.6 and bx.get("z1", cc_[2] + bx["s"][2] / 2) > 0.3:
            print("static", s_["name"], np.round(cc_, 2).tolist(), "half", np.round(np.asarray(bx["s"]) / 2, 2).tolist(), "z1", round(float(bx.get("z1", cc_[2] + bx["s"][2] / 2)), 3), flush=True)
print(close(os.path.join(TELE_DIR, "f12_tissue_top.jpg"), np.r_[c_[:2] + np.array([0.35, -0.25]), c_[2] + 0.55], c_, "tissue"), flush=True)
