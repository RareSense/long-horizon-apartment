zz_n = "r116i1_coat_pile"
print("ck", ck_save("bc_coat_at_pre", kind="act"), flush=True)
zz_r = bigcloth_into(zz_n, s1="right", start="step_in", stop_after="step_in")
print("RESULT", zz_r, flush=True)
print("state", state(), "touch", contact_report(), "inside", in_container(zz_n, laundry_body()), "out", bc_out(zz_n, laundry_body()), "heater dist", [round(float(r_.dist(base()[0][None, :2])[0]), 3) for r_ in scene_rects(()) if "heater" in str(INFO["bodies"].get(getattr(r_, "name", None), {}).get("display", "")) or "r132" in str(getattr(r_, "name", ""))], flush=True)
print("TELE last", TELE["log"][-2:], flush=True)
