for i_, mv_ in enumerate(zz_r.get("moves") or []):
    print(i_, str(mv_)[:400], flush=True)
print("set_down", str(zz_r.get("set_down"))[:600], flush=True)
print("scooter box now", [np.round(v_, 3).tolist() for v_ in obj_box(body_of("r126i1_scooter"))], flush=True)
import glob as _g
print(sorted(_g.glob(os.path.join(RUN, "checkpoints", "*")))[-40:], flush=True)
