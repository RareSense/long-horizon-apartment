tt_ = "object_0225_body"; sb_ = SPONGE
lo_t, hi_t = body_aabb(m.body(tt_).id); lo_s, hi_s = obj_box(sb_)
on_ = [b_ for b_ in _thing_contacts(sb_)]
inside_xy = bool(lo_s[0] >= lo_t[0] - 0.005 and hi_s[0] <= hi_t[0] + 0.005 and lo_s[1] >= lo_t[1] - 0.005 and hi_s[1] <= hi_t[1] + 0.005)
print("tray", tt_, np.round(lo_t, 3).tolist(), np.round(hi_t, 3).tolist(), "sponge", np.round(lo_s, 3).tolist(), np.round(hi_s, 3).tolist(), "touching", on_, "inside_xy", inside_xy, flush=True)
c_ = centre(sb_)
print(close(os.path.join(RUN, "look", "f14_c05_sponge_on_tray.jpg"), c_ + np.array([0.0, -0.55, 0.45]), c_, "sponges r83i1 on tray table r94 (AI-operated)"), flush=True)
if inside_xy and set(on_) <= {tt_} and on_:
    print("DONE", item_done_auto("r83i1_sponges", dict(status="done", box=[np.round(lo_s, 3).tolist(), np.round(hi_s, 3).tolist()], squeeze_checks=[{k_: v_ for k_, v_ in r_.items() if k_ != "look"} for r_ in SPONGE_CHECK],
                                                          how="Fable's island_pick under call_mon, stance x 0.68 (knee), two-hand squeeze hold_on(guard=False) after its own force check, f14\\c04_retry.py (AI-operated)")), flush=True)
print("state", state(), "kit", kit_mem(), flush=True)
