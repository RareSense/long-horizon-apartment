mon_start(target=None)
try:
    for k_ in range(2):
        r_ = tmove(fwd=-0.12, tag=f"n1_back{k_}")
        c_ = contact_report()
        print("back", k_, np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), c_["body"], c_["body_who"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
b_ = body_of("r122i1_croc"); print("croc", np.round(centre(b_), 3).tolist(), "state", state(), "fell", fallen(), flush=True)
print("feet", {s_: np.round(d.xpos[m.body(s_ + "_ankle_roll_link").id], 3).tolist() for s_ in SIDES}, flush=True)
print(look3("n1_a02"), flush=True)
