MON["on"] = False
print("START", ck_save("umb_start_from_1517", kind="start"), flush=True)
ZR = umbrella_to_entry()
print("RESULT", {k_: v_ for k_, v_ in ZR.items() if k_ != "route"}, flush=True)
print("ROUTE", {k_: v_ for k_, v_ in (ZR.get("route") or {}).items() if k_ in ("ckpt", "done", "pos", "next")}, flush=True)
print(close(os.path.join(LK, "v04_entry.jpg"), np.r_[3.6, -1.7, 1.3], np.r_[3.1, -2.45, 0.0], "entry"), "kit", kit_mem(), flush=True)
