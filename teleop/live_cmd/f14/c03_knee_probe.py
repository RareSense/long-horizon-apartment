import mujoco as _mjc
M_, D_ = br.mjm, br.mjd
f6_ = np.zeros(6)
for i_ in range(int(D_.ncon)):
    c_ = D_.contact[i_]
    n1 = M_.body(M_.geom_bodyid[c_.geom1]).name.split("/")[-1]; n2 = M_.body(M_.geom_bodyid[c_.geom2]).name.split("/")[-1]
    if "knee" in n1 or "knee" in n2 or "hip" in n1 or "hip" in n2:
        _mjc.mj_contactForce(M_, D_, i_, f6_)
        print("contact", n1, n2, "pos", np.round(c_.pos, 3).tolist(), "F", round(float(f6_[0]), 1), "dist", round(float(c_.dist), 4), flush=True)
for nm_ in ("left_knee_link", "right_knee_link", "left_ankle_roll_link", "right_ankle_roll_link", "pelvis"):
    try:
        print(nm_, np.round(d.xpos[m.body(nm_).id], 3).tolist(), flush=True)
    except Exception as ex_:
        print(nm_, ex_)
print("state", state(), "mode", flush=True)
