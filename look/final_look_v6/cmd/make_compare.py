# Side-by-side sheet: room photos (17 Nov, messy start) vs final_look_v6 path-traced renders of the episode START state.
# AI-operated. Usage: py make_compare.py [render_folder]
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
P = r"C:\Users\raresense\sim_home\apartment\room_photos"
R = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\raresense\sim_home\apartment\final_look_v5"
pairs = [("20261117_161418.jpg", "room_photo161418_pt_1080.png"), ("20261117_161423.jpg", "room_photo161423_pt_1080.png"),
         ("20261117_161414.jpg", "kitchen_photo161414_pt_1080.png"), ("20261117_161426.jpg", "room_photo161426_pt_1080.png")]
W, H = 960, 540
sheet = Image.new("RGB", (2 * W, len(pairs) * (H + 30) + 40), (20, 20, 20)); d = ImageDraw.Draw(sheet)
try: f = ImageFont.truetype("arial.ttf", 22)
except Exception: f = None
d.text((10, 8), "Photo (17 Nov, messy)  |  Isaac Sim PATH TRACED 64 spp + denoiser, episode START state, final_look_v6 (label + print textures)  (AI-operated)", fill=(255, 255, 255), font=f)
for i, (a, b) in enumerate(pairs):
    y = 40 + i * (H + 30); lum = []
    for j, path in enumerate((os.path.join(P, a), os.path.join(R, b))):
        im = Image.open(path).convert("RGB"); im = im.resize((W, int(W * im.height / im.width))).crop((0, 0, W, H))
        lum.append(float(np.asarray(im.convert("L"), float).mean()))
        sheet.paste(im, (j * W, y)); d.text((j * W + 8, y + H + 4), os.path.basename(path), fill=(220, 220, 220), font=f)
    print(b, "mean luma photo %.0f render %.0f" % tuple(lum))
sheet.save(os.path.join(R, "compare_photo_vs_render.jpg"), quality=90)
print("ok")
