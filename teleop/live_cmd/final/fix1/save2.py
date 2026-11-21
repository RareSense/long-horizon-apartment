c_=item_check("r125i2_flat"); print("CHECK", c_, flush=True)
if c_.get("ok") and not fallen():
    print("CKPT", _route_checkpoint_raw("r125i2_flat_stand"), "POS", POS, "DONE", len(DONE), "next", item_name(ROUTE[POS]), flush=True)
