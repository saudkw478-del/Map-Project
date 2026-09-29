"""World map PNG (English/ID labels only: no Arabic shaping library is available)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import terrain as TR

PAL = {0: (28, 62, 110), 1: (52, 110, 160), 2: (226, 196, 120), 3: (178, 82, 50), 4: (86, 150, 70), 5: (238, 238, 232),
       6: (52, 50, 58), 7: (122, 92, 60), 8: (200, 150, 50), 9: (70, 140, 200), 10: (238, 220, 160), 11: (214, 176, 100)}
KIND_COL = {"main": (255, 60, 60), "minor_oasis": (40, 200, 90), "waystation": (255, 255, 255), "ruin": (250, 160, 40), "tomb": (200, 90, 220),
            "buried_temple": (200, 90, 220), "lore_stone": (100, 220, 255), "watchtower": (240, 240, 100), "shipwreck": (100, 160, 255),
            "salt_mirror": (255, 255, 255), "fossil": (255, 230, 200), "lighthouse": (255, 250, 120), "pond": (70, 140, 200)}


def make_map(T, rows, path, size=1200):
    cls = T.cls
    rgb = np.zeros(cls.shape + (3,), np.float32)
    for k, c in PAL.items():
        rgb[cls == k] = c
    H = T.H.astype(np.float32)
    gy, gx = np.gradient(H)
    shade = np.clip(1 + (-gx * 0.9 - gy * 0.9) * 0.10, 0.65, 1.3)
    rgb = np.clip(rgb * shade[..., None], 0, 255).astype(np.uint8)
    im = Image.fromarray(rgb).resize((size, size), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    s = size / cls.shape[0]
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        f = fs = ImageFont.load_default()
    for r in rows:
        if r.get("dimension", "minecraft:overworld") != "minecraft:overworld":
            continue
        x, z = r["x"] * s, r["z"] * s
        col = KIND_COL.get(r["kind"], (255, 255, 255))
        if r["kind"] == "main":
            d.ellipse((x - 8, z - 8, x + 8, z + 8), fill=col, outline=(0, 0, 0), width=2)
            d.text((x + 11, z - 9), r["id"], fill=(255, 255, 255), font=f, stroke_width=2, stroke_fill=(0, 0, 0))
        else:
            d.ellipse((x - 3, z - 3, x + 3, z + 3), fill=col, outline=(0, 0, 0))
    # legend
    y0 = 12
    d.rectangle((8, 8, 200, 12 + 14 * len(TR.LEGEND) + 24), fill=(0, 0, 0, 160))
    d.text((14, y0), "Nahas City (concept map)", fill=(255, 255, 255), font=fs)
    for k, v in TR.LEGEND.items():
        y0 += 14
        d.rectangle((14, y0 + 16, 26, y0 + 26), fill=PAL[k])
        d.text((32, y0 + 14), v, fill=(255, 255, 255), font=fs)
    im.save(path)
