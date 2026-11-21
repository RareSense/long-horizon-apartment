with open(os.path.join(RUN, "items_left.txt"), "w", encoding="utf-8") as zz_f:
    for zz_r in zz_rows:
        zz_f.write(repr(zz_r) + "\n")
print("written", os.path.join(RUN, "items_left.txt"), flush=True)
