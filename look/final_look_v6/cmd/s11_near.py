# AI-operated: list props near the two close-up targets that LABELS does not cover (inspection only).
import urc.tasks.home.final_look as FL
M_ = FL._map(FL.TL.USD_MAP)
for tgt_, rad_ in (((2.2, -0.3), 1.1), ((-3.68, -0.91), 0.8)):
    out_ = []
    for e_ in M_["prims"]:
        p_ = FL._tex_prim(stage, SCN["top"], e_)
        if p_ is None: continue
        b_ = UsdGeom.Imageable(p_).ComputeWorldBound(Usd.TimeCode.Default(), "default").ComputeAlignedRange()
        c_ = (b_.GetMin() + b_.GetMax()) / 2; sz_ = b_.GetMax() - b_.GetMin()
        if abs(c_[0] - tgt_[0]) < rad_ and abs(c_[1] - tgt_[1]) < rad_ and max(sz_) < 0.6 and e_["display"] not in FL.LABELS:
            out_.append((e_["display"], e_.get("cls"), [round(x, 2) for x in c_], [round(x, 2) for x in sz_]))
    print("NEAR", tgt_, out_, flush=True)
