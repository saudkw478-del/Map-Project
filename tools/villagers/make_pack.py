"""Paint Game-of-Thrones villager clothing (procedural pixel art) and write the resource pack + PNGs."""
import json, os, random, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools", "render"))
from entities import uvs  # noqa: E402

PACK = os.path.join(ROOT, "resourcepack", "GoT_Villagers")
TEX_DIR = os.path.join(PACK, "assets", "minecraft", "textures", "entity", "villager")

# body parts: (name, U, V, w, h, d)
BODY = (16, 20, 8, 12, 6)
JACKET = (0, 38, 8, 18, 6)
ARM = (44, 22, 4, 8, 4)
ARMMID = (40, 38, 8, 4, 4)
LEG = (0, 22, 4, 12, 4)
HEAD = (0, 0, 8, 10, 8)
NOSE = (24, 0, 2, 4, 2)
HAT = (32, 0, 8, 10, 8)

F_LEFT, F_RIGHT, F_TOP, F_BOTTOM, F_FRONT, F_BACK = range(6)


def rect(d, x, y, w, h, col):
    if w > 0 and h > 0:
        d.rectangle((x, y, x + w - 1, y + h - 1), fill=col)


def face_rect(part, face):
    U, V, w, h, dd = part
    return uvs(U, V, w, h, dd)[face]


def fill_part(img, part, col, faces=range(6)):
    d = ImageDraw.Draw(img)
    for f in faces:
        x, y, w, h = face_rect(part, f)
        rect(d, x, y, w, h, col)


def band(img, part, row0, rows, col, faces=(F_LEFT, F_RIGHT, F_FRONT, F_BACK)):
    d = ImageDraw.Draw(img)
    for f in faces:
        x, y, w, h = face_rect(part, f)
        rect(d, x, y + row0, w, rows, col)


def speckle(img, box_, amp, seed):
    rnd = random.Random(seed)
    a = np.array(img).astype(int)
    x0, y0, x1, y1 = box_
    for y in range(y0, y1):
        for x in range(x0, x1):
            if a[y, x, 3] > 0:
                k = rnd.randint(-amp, amp)
                a[y, x, :3] = np.clip(a[y, x, :3] + k, 0, 255)
    img.paste(Image.fromarray(a.astype(np.uint8)))


def base_villager():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    skin, skin_d = (222, 168, 128, 255), (196, 142, 104, 255)
    hair = (60, 40, 26, 255)
    # head + nose
    fill_part(img, HEAD, skin)
    fill_part(img, NOSE, skin_d)
    # hair: top, back, upper sides and fringe
    fill_part(img, HEAD, hair, faces=(F_TOP, F_BACK))
    for f in (F_LEFT, F_RIGHT):
        x, y, w, h = face_rect(HEAD, f); rect(d, x, y, w, 5, hair)
    x, y, w, h = face_rect(HEAD, F_FRONT)
    rect(d, x, y, w, 2, hair)
    rect(d, x, y + 2, 1, 2, hair); rect(d, x + w - 1, y + 2, 1, 2, hair)
    # face: unibrow, eyes
    rect(d, x + 1, y + 3, 6, 1, (70, 45, 30, 255))
    for ex in (x + 1, x + 5):
        rect(d, ex, y + 4, 2, 2, (250, 250, 250, 255)); rect(d, ex + (0 if ex == x + 1 else 1), y + 4, 1, 2, (50, 80, 60, 255))
    rect(d, x + 3, y + 8, 2, 1, (170, 110, 90, 255))   # mouth
    # generic undyed peasant tunic + trousers
    tunic, tunic_d = (196, 180, 142, 255), (168, 152, 116, 255)
    fill_part(img, BODY, tunic); fill_part(img, JACKET, tunic); fill_part(img, ARM, tunic); fill_part(img, ARMMID, tunic)
    fill_part(img, LEG, (95, 72, 50, 255))
    band(img, BODY, 8, 1, (110, 76, 40, 255)); band(img, JACKET, 11, 1, (110, 76, 40, 255))
    band(img, JACKET, 16, 2, tunic_d)
    speckle(img, (0, 0, 64, 64), 7, 3)
    return img


def outfit(spec):
    """Transparent overlay that fully covers the clothed parts."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    T, T2, TRIM, BELT = spec["tunic"], spec["tunic2"], spec["trim"], spec["belt"]
    for part in (BODY, JACKET):
        fill_part(img, part, T)
    fill_part(img, ARM, spec["sleeve"]); fill_part(img, ARMMID, spec["sleeve"])
    fill_part(img, LEG, spec["pants"])
    # boots
    band(img, LEG, 9, 3, spec.get("boots", (50, 34, 24, 255)))
    # belt, hem, cuffs
    band(img, BODY, 8, 1, BELT); band(img, JACKET, 11, 1, BELT)
    band(img, JACKET, 16, 2, TRIM)
    band(img, ARM, 6, 2, TRIM); band(img, ARMMID, 0, 1, TRIM, faces=(F_FRONT, F_BACK))
    # shoulder mantle / collar
    if spec.get("mantle"):
        m, m2 = spec["mantle"]
        for part, rows in ((BODY, 3), (JACKET, 4)):
            band(img, part, 0, rows, m)
        fill_part(img, BODY, m, faces=(F_TOP,)); fill_part(img, JACKET, m, faces=(F_TOP,))
        rnd = random.Random(11)
        for part, rows in ((BODY, 3), (JACKET, 4)):
            for f in (F_LEFT, F_RIGHT, F_FRONT, F_BACK):
                x, y, w, h = face_rect(part, f)
                for i in range(w):
                    if rnd.random() < 0.5:
                        rect(d, x + i, y + rows - 1, 1, 1, m2)
                        if rnd.random() < 0.3:
                            rect(d, x + i, y + rows, 1, 1, m2)
    # chest sigil on the robe front
    if spec.get("sigil"):
        x, y, w, h = face_rect(JACKET, F_FRONT)
        s1, s2 = spec["sigil"]
        rect(d, x + 3, y + 5, 2, 4, s1); rect(d, x + 2, y + 6, 4, 2, s1); rect(d, x + 3, y + 6, 2, 2, s2)
    # hat layer
    hat = spec.get("hat")
    if hat:
        col, col2, rows_side, top = hat
        for f in (F_LEFT, F_RIGHT, F_FRONT, F_BACK):
            x, y, w, h = face_rect(HAT, f)
            rect(d, x, y, w, rows_side, col)
            rect(d, x, y + rows_side - 1, w, 1, col2)
        if top:
            fill_part(img, HAT, col, faces=(F_TOP,))
        if spec.get("hat_front_open"):
            x, y, w, h = face_rect(HAT, F_FRONT)
            for yy in range(y, y + rows_side):
                for xx in range(x + 2, x + w - 2):
                    img.putpixel((xx, yy), (0, 0, 0, 0)) if yy >= y + 2 else None
    speckle(img, (0, 0, 64, 64), 9, 5)
    return img


def rgba(r, g, b): return (r, g, b, 255)

OUTFITS = {
    # House Stark / the North: grey wool + white fur mantle and fur hat
    "snow": dict(tunic=rgba(88, 92, 100), tunic2=rgba(70, 74, 82), trim=rgba(215, 215, 222), belt=rgba(60, 40, 26), sleeve=rgba(88, 92, 100),
                 pants=rgba(58, 60, 66), mantle=(rgba(228, 228, 234), rgba(170, 172, 180)), sigil=(rgba(235, 235, 240), rgba(120, 124, 132)),
                 hat=(rgba(215, 215, 222), rgba(160, 160, 170), 3, True)),
    # Night's Watch / Baratheon: black with gold trim, black hood
    "taiga": dict(tunic=rgba(30, 30, 34), tunic2=rgba(20, 20, 24), trim=rgba(214, 170, 30), belt=rgba(120, 90, 30), sleeve=rgba(30, 30, 34),
                  pants=rgba(24, 24, 28), mantle=(rgba(18, 18, 22), rgba(45, 45, 52)), sigil=(rgba(214, 170, 30), rgba(30, 30, 34)),
                  hat=(rgba(22, 22, 26), rgba(40, 40, 46), 4, True)),
    # Tully / Riverlands: blue tunic, red belt
    "plains": dict(tunic=rgba(52, 84, 156), tunic2=rgba(40, 66, 130), trim=rgba(170, 40, 40), belt=rgba(160, 40, 40), sleeve=rgba(70, 100, 170),
                   pants=rgba(60, 60, 70), sigil=(rgba(200, 200, 215), rgba(170, 40, 40))),
    # Martell / Dorne: orange robes, sandy headscarf
    "desert": dict(tunic=rgba(214, 104, 34), tunic2=rgba(190, 84, 24), trim=rgba(240, 190, 60), belt=rgba(240, 190, 60), sleeve=rgba(230, 130, 50),
                   pants=rgba(200, 170, 110), sigil=(rgba(240, 190, 60), rgba(190, 40, 30)),
                   hat=(rgba(232, 214, 168), rgba(190, 60, 30), 4, True), boots=rgba(120, 80, 40)),
    # Tyrell / the Reach: green with gold, flower cap
    "savanna": dict(tunic=rgba(66, 126, 62), tunic2=rgba(52, 104, 52), trim=rgba(226, 190, 60), belt=rgba(226, 190, 60), sleeve=rgba(80, 140, 74),
                    pants=rgba(110, 90, 60), sigil=(rgba(240, 210, 70), rgba(200, 40, 60)),
                    hat=(rgba(90, 150, 70), rgba(230, 90, 120), 2, True)),
    # the Neck / swamp folk: drab olive rags, straw hat
    "swamp": dict(tunic=rgba(92, 100, 62), tunic2=rgba(74, 82, 50), trim=rgba(60, 66, 40), belt=rgba(80, 60, 36), sleeve=rgba(100, 108, 70),
                  pants=rgba(70, 70, 46), hat=(rgba(176, 160, 84), rgba(130, 116, 60), 3, True), boots=rgba(60, 50, 34)),
    # Lannister / Crownlands: crimson and gold
    "jungle": dict(tunic=rgba(146, 26, 34), tunic2=rgba(120, 18, 26), trim=rgba(224, 178, 40), belt=rgba(224, 178, 40), sleeve=rgba(160, 34, 42),
                   pants=rgba(80, 40, 30), mantle=(rgba(224, 178, 40), rgba(160, 120, 30)), sigil=(rgba(224, 178, 40), rgba(146, 26, 34)),
                   hat=(rgba(224, 178, 40), rgba(160, 120, 30), 1, False)),
}
HAT_META = {"snow": "partial", "taiga": "partial", "plains": "none", "desert": "partial", "savanna": "partial",
            "swamp": "partial", "jungle": "partial"}
HOUSE_OF_TYPE = {"snow": "North (Stark)", "taiga": "Night's Watch / Baratheon", "plains": "Riverlands (Tully)",
                 "desert": "Dorne (Martell)", "savanna": "The Reach (Tyrell)", "swamp": "The Neck", "jungle": "Lannister / Crownlands"}


def build():
    os.makedirs(os.path.join(TEX_DIR, "type"), exist_ok=True)
    base = base_villager()
    base.save(os.path.join(TEX_DIR, "villager.png"))
    outs = {}
    for name, spec in OUTFITS.items():
        img = outfit(spec)
        outs[name] = img
        img.save(os.path.join(TEX_DIR, "type", f"{name}.png"))
        with open(os.path.join(TEX_DIR, "type", f"{name}.png.mcmeta"), "w") as f:
            json.dump({"villager": {"hat": HAT_META[name]}}, f)
    with open(os.path.join(PACK, "pack.mcmeta"), "w") as f:
        json.dump({"pack": {"pack_format": 34, "description": "Game of Thrones villagers: Westeros clothing",
                            "supported_formats": {"min_inclusive": 22, "max_inclusive": 999},
                            "min_format": 22, "max_format": 999}}, f, indent=1)
    return base, outs


def composite(base, over):
    return Image.alpha_composite(base, over)


if __name__ == "__main__":
    base, outs = build()
    sheet = Image.new("RGBA", (64 * 4 * 2, 64 * 2 * 2 + 0), (40, 40, 40, 255))
    for i, (n, o) in enumerate(outs.items()):
        c = composite(base, o).resize((128, 128), Image.NEAREST)
        sheet.paste(c, ((i % 4) * 128 * 1, (i // 4) * 128))
    sheet.convert("RGB").save("/tmp/claude-0/prev/shots/villager_textures.png")
    print("written", PACK)
