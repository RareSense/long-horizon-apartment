import numpy as np
g_=room_grid(())
xs_=np.arange(-3.6,-0.95,0.1); ys_=np.arange(-0.6,-2.65,-0.1)
print("     "+"".join(f"{x:5.1f}"[-2] for x in xs_))
for y in ys_:
    print(f"{y:5.2f} "+"".join("." if g_.free(np.array([x,y])) else "#" for x in xs_))
print("look", look3("fix1_start"))
