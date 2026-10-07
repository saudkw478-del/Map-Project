"""Cuts faces/figures out of the character sheet (rembg), cleans edges, prepares the hero scene."""
import sys, numpy as np, cv2
from PIL import Image
from rembg import remove, new_session
SP = sys.argv[1]; W = f"{SP}/tr_work"
sheet = Image.open(f"{SP}/tr_in/sheet.png").convert("RGB")
sess = new_session("u2net")

def clean(rgba, erode=2, blur=1.0):
    a = np.array(rgba); al = a[..., 3].astype(np.float32)
    k = np.ones((3, 3), np.uint8); al = cv2.erode(al, k, iterations=erode)
    al = cv2.GaussianBlur(al, (0, 0), blur)
    # pull edge colour inward to kill the light halo from the parchment background
    rgb = a[..., :3].copy(); edge = (al > 8) & (al < 200)
    dark = cv2.erode(rgb, np.ones((5, 5), np.uint8))
    rgb[edge] = (rgb[edge] * 0.35 + dark[edge] * 0.65).astype(np.uint8)
    a[..., :3] = rgb; a[..., 3] = al.astype(np.uint8)
    return Image.fromarray(a, "RGBA")

# full figures (already 3x cut earlier -> redo with cleanup)
for k, box in {"khalid_front": (48, 48, 218, 488), "noura_front": (836, 60, 958, 462)}.items():
    c = sheet.crop(box); c = c.resize((c.width * 4, c.height * 4), Image.LANCZOS)
    clean(remove(c, session=sess), 3, 1.4).save(f"{W}/{k}_cut.png")

# faces: 3 cols x 2 rows per character
EXPR = ["joy", "sad", "fear", "surprise", "anger", "think"]
panels = {"khalid": ([(503, 607), (607, 709), (709, 812)], 500), "noura": ([(1210, 1313), (1313, 1416), (1416, 1530)], 1207)}
rows = [(66, 222), (248, 402)]
for who, (cols, _) in panels.items():
    i = 0
    for (y0, y1) in rows:
        for (x0, x1) in cols:
            c = sheet.crop((x0, y0, x1, y1)); c = c.resize((c.width * 5, c.height * 5), Image.LANCZOS)
            clean(remove(c, session=sess), 4, 1.8).save(f"{W}/face_{who}_{EXPR[i]}.png"); i += 1
# hero scene
Image.open(f"{W}/scene.png").save(f"{W}/hero.png")
print("assets ok")
