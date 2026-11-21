# AI-operated, render only: apply the v6 label / print textures on the live session (fresh boot, START state).
import importlib, urc.tasks.home.final_look as FL
importlib.reload(FL)
r_ = FL.label_looks(stage, SCN["top"], log=lambda s: print(s, flush=True))
