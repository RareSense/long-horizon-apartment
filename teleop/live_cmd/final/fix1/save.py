import numpy as np
for n_ in ("r133i1_laundry_basket","object_0259_body","object_0263_body","object_0318_body","object_0322_body"):
    lo_,hi_=obj_box(n_); print("BOX", n_, np.round(lo_,3).tolist(), np.round(hi_,3).tolist())
print("STATE", state(), contact_report()["body"], fallen(), "POS", POS, "DONE", len(DONE))
rest_hands(SIDES); op.run(0.5)
p_=_route_checkpoint_raw("r68i1_rag_stepout")
print("CKPT", p_, "rec", rec.n, flush=True)
