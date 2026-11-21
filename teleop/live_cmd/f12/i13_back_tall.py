MON["on"] = False
for k_ in range(2):
    r_ = tmove(fwd=-0.10, carry=("left",), tag="off_bin_tall")
    print("step", k_, state(), "touch", contact_report()["body"], "fell", fallen(), flush=True)
    if fallen():
        break
