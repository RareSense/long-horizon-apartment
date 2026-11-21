HB_ = "r133i1_laundry_basket"
for g_ in GARMENTS:
    try:
        print("GARMENT", g_, in_container(g_, HB_), flush=True)
    except Exception as ex_:
        print("GARMENT", g_, "err", str(ex_)[:150], flush=True)
try:
    DWD_ = globals().get("DW_DOOR")
    a_, bid_ = jointed(DWD_)
    j_ = int(m.body_jntadr[bid_])
    print("DW_DOOR", DWD_, "q", round(float(d.qpos[a_]), 3), "range", np.round(m.jnt_range[j_], 3).tolist(), flush=True)
    for nmr_ in ("DW_RACKS", "DW_RACK", "DW_RACK_TOP", "DW_RACK_BOTTOM"):
        if nmr_ in globals():
            print(nmr_, globals()[nmr_], flush=True)
except Exception as ex_:
    print("dw err", str(ex_)[:200], flush=True)
lsb_ = body_of("r130i1_light_saber"); lo_, hi_ = obj_box(lsb_)
print("saber box", np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), "basket box", np.round(obj_box("object_0312_body")[0], 3).tolist(), np.round(obj_box("object_0312_body")[1], 3).tolist(), flush=True)
c_ = centre(lsb_)
print(close(os.path.join(RUN, "look", "f14_d03_toy_corner.jpg"), c_ + np.array([0.9, 0.2, 1.3]), c_, "final sweep: toy corner, saber r130 / basket r186 (AI-operated)"), flush=True)
hc_ = centre(HB_)
print(close(os.path.join(RUN, "look", "f14_d03_hamper.jpg"), hc_ + np.array([0.6, 0.6, 1.2]), hc_, "final sweep: hamper r133 garments (AI-operated)"), flush=True)
mc_ = centre(body_of("r119i1_mat")) if body_of("r119i1_mat") else np.array([1.5, -2.1, 0.0])
print(close(os.path.join(RUN, "look", "f14_d03_mat.jpg"), mc_ + np.array([-0.9, 0.5, 1.3]), mc_, "final sweep: mat r119 shoes (AI-operated)"), flush=True)
bc_ = np.array([0.1, 1.4, 0.2])
print(close(os.path.join(RUN, "look", "f14_d03_bin.jpg"), bc_ + np.array([0.5, -0.4, 1.0]), bc_, "final sweep: rubbish bin (AI-operated)"), flush=True)
