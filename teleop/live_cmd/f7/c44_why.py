print("0265", INFO["bodies"].get("object_0265_body", {}).get("display"), np.round(d.xpos[m.body("object_0265_body").id], 2).tolist(), "basket", np.round(centre(body_of("r186i1_basket")), 3).tolist(), flush=True)
print([(c_["name"], c_["t"], os.path.basename(c_["path"])) for c_ in CK_LOG[-10:] if c_.get("kind") != "roll"], flush=True)
print("trace", MON["trace"][-40::4], flush=True)
