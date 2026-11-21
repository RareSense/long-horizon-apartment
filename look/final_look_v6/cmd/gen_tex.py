# AI-operated: generic print/label textures for flat props (final look v6). No brands, no personal info.
import json, base64, urllib.request, concurrent.futures as cf, os, sys
from pathlib import Path
KEY = Path(r"C:\Users\raresense\Desktop\nova_homes\.ork").read_text().strip()
OUT = Path(r"C:\Users\raresense\sim_home\apartment\look_tex\v6")
BASE = (" Output ONLY the flat texture image: front-facing, perfectly flat, evenly lit, no perspective, no shadows, no object "
        "shown, fills the whole frame edge to edge. Invented generic design: NO real brand names, NO real logos, no trademarks.")
J = {
 "label_detergent": "A wide wrap-around plastic bottle label for a generic laundry detergent, bright blue and white with an invented word 'FRESH' and simple bubbles graphic, 3:1 aspect.",
 "label_water": "A wide wrap-around label band for a generic still water bottle, light blue and white with mountain line art and invented word 'AQUA', 3:1 aspect.",
 "label_sauce": "A wide wrap-around label for a generic tomato sauce bottle, red, cream and green with a tomato drawing and invented word 'SALSA', 3:1 aspect.",
 "label_oil": "A wide wrap-around label for a generic olive oil bottle, gold and dark green with olive branch drawing and invented word 'OLIVA', 3:1 aspect.",
 "chips_wrap": "A wide wrap-around paper tube label for a generic potato chips can, red and yellow with a stack of chips illustration and invented word 'CRISPS', 3:1 aspect.",
 "mug_print": "A wide wrap-around print for a ceramic coffee mug, off-white glaze with a simple hand-drawn botanical leaf pattern in blue, subtle glaze speckle, 3:1 aspect.",
 "cup_glaze": "Seamless texture of glossy speckled stoneware ceramic glaze, warm cream with tiny brown speckles, square.",
 "plate_top": "Top-down view of a round glazed ceramic dinner plate texture, white speckled glaze with a thin dark blue rim band near the edge, circle centred filling the square frame, square.",
 "bowl_top": "Top-down view of a round glazed ceramic bowl interior texture, cream speckled glaze with a terracotta rim band at the outer edge, circle centred filling the square frame, square.",
 "cereal_box": "The front panel print of a generic breakfast cereal box, colourful, bowl of cereal flakes with milk illustration, invented word 'CRUNCHY FLAKES', portrait 3:4.",
 "toy_box": "The front panel print of a generic children's toy building blocks box, bright primary colours, playful illustrated blocks, invented word 'BLOCKS', landscape 4:3.",
 "book_covers": "A 2x2 grid of four different generic hardcover book front covers with invented titles and author names, muted varied colours (navy, burgundy, forest green, ochre), simple typographic designs, square.",
 "book_spines": "A row of eight vertical book spines side by side, invented titles, varied muted colours with gold and white text, square.",
 "block_letters": "A 3x3 grid of square wooden toy block faces, each a different bright colour with a large embossed letter A,B,C,D,E,F,G,H,I, painted wood, square.",
}
def gen(name):
    body = {"model": "google/gemini-3-pro-image-preview", "modalities": ["image", "text"], "image_config": {"image_size": "1K"},
            "max_tokens": 4000, "messages": [{"role": "user", "content": J[name] + BASE}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=300).read())
        ims = r["choices"][0]["message"].get("images") or []
        if not ims: return name, "no image"
        raw = base64.b64decode(ims[0]["image_url"]["url"].split(",", 1)[1])
        (OUT / (name + ".png")).write_bytes(raw); return name, "ok %d" % len(raw)
    except Exception as e:
        return name, "fail " + type(e).__name__ + " " + str(e)[:100]
with cf.ThreadPoolExecutor(14) as ex:
    for n, s in ex.map(gen, list(J)): print(n, s, flush=True)
