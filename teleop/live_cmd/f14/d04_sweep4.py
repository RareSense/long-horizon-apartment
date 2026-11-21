print("STOCKING in basket", in_container("r190i1_stocking", "object_0312_body"), flush=True)
for rk_ in DW_RACKS:
    try:
        a_, bid_ = jointed(rk_); j_ = int(m.body_jntadr[bid_])
        print("RACK", rk_, "q", round(float(d.qpos[a_]), 3), "range", np.round(m.jnt_range[j_], 3).tolist(), flush=True)
    except Exception as ex_:
        print("rack err", rk_, str(ex_)[:120], flush=True)
