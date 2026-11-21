for b_, inf_ in INFO["bodies"].items():
    c_ = d.xpos[m.body(b_).id]
    if -4.2 < c_[0] < -2.8 and -1.6 < c_[1] < -0.3:
        print("near coffee table:", b_, inf_.get("display"), np.round(c_, 3).tolist(), flush=True)
for s_ in INFO["static"]:
    for bx in (s_.get("pieces") or s_["boxes"]):
        c_ = np.asarray(bx["c"])
        if -4.2 < c_[0] < -2.8 and -1.6 < c_[1] < -0.3 and c_[2] > 0.4:
            print("static:", s_["name"], np.round(c_, 2).tolist(), flush=True)
# the Isaac prim of one removed body: where does the renderer have it?
try:
    from pxr import UsdGeom
    import omni.usd
    st_ = omni.usd.get_context().get_stage()
    hits_ = [p_ for p_ in st_.Traverse() if "object_0283" in str(p_.GetPath())][:3]
    for p_ in hits_:
        xf_ = UsdGeom.Xformable(p_).ComputeLocalToWorldTransform(0)
        print("prim", p_.GetPath(), [round(v_, 3) for v_ in xf_.ExtractTranslation()], flush=True)
except Exception as ex_:
    print("usd check", str(ex_)[:200], flush=True)
