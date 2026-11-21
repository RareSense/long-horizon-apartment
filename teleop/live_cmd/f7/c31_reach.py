def zz_r():
    g_ = room_grid(()); p_ = base()[0][:2]
    print("reach to east (3.9,-2.1)", g_.reach_cost(p_, np.array([3.9, -2.1])), "to hall (1.0,-1.7)", g_.reach_cost(p_, np.array([1.0, -1.7])), "to rag side (3.35,0.75)", g_.reach_cost(p_, np.array([3.35, 0.75])), flush=True)
with_tight(zz_r)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f7\c02_rag_st.py", encoding="utf-8").read().split('print("look"')[0])
