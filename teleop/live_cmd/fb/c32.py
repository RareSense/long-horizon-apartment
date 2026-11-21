import json as _js
zz_meta = _js.load(open(os.path.join(RUN, "checkpoints", "0592_item_r117i1_blanket", "meta.json"), encoding="utf-8"))
SEG.update(start_frame=0, from_ckpt=CHAIN, checkpoints=[dict(name="0592_item_r117i1_blanket", frames=zz_meta.get("frames"), t=zz_meta.get("sim_t"), pos=7)])
_seg_write()
RESULT["ok"] = True
RESULT["escalation_blanket"] = dict(by="Fable (AI-operated teleop)", from_ckpt=CHAIN, item_ckpt=os.path.join(RUN, "checkpoints", "0592_item_r117i1_blanket"), blanket=in_container(zz_BL, zz_hb()))
save_partial()
print("segment", SEG, flush=True)
br.on_step = None
try:
    if globals().get("TR") is not None:
        TR.close()
except Exception as ex_:
    print("TR close", ex_, flush=True)
print("videos", rec.close() if globals().get("rec") is not None else None, "frames", getattr(globals().get("rec"), "n", None), flush=True)
