#!/usr/bin/env python3
"""Generates nahas_city/resourcepack (procedural 16x16 pixel art) + docs/items_sheet.png"""
import json, os, math
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
RP = os.path.join(ROOT, "resourcepack")
TEX = os.path.join(RP, "assets/nahas/textures/item")
MOD = os.path.join(RP, "assets/nahas/models/item")
ITM = os.path.join(RP, "assets/nahas/items")
LANG = os.path.join(RP, "assets/nahas/lang")
for d in (TEX, MOD, ITM, LANG, os.path.join(ROOT, "docs")):
    os.makedirs(d, exist_ok=True)

def H(s):
    s = s.lstrip("#"); return tuple(int(s[i:i+2], 16) for i in (0, 2, 4)) + (255,)
OUT = H("2a1608")
BR = [H(x) for x in ("5a3210", "8a5a1c", "b8802c", "e0aa3e", "fbdc78", "fff4b8")]  # brass ramp dark->light
TQ = [H(x) for x in ("0b4f5a", "138a8f", "24c0b8", "7aeee0")]
EM = [H(x) for x in ("5a1006", "b02a0c", "ff6a1a", "ffc23a", "fff1a0")]
ST = [H(x) for x in ("1a1a5a", "4a4ad0", "9aa8ff", "e8eeff", "ffffff")]
RD = [H(x) for x in ("4a0c1a", "8a1a30", "c8324a", "ee6a78")]
WOOD = [H("3a2210"), H("6b4222"), H("8f5f30")]
STEEL = [H(x) for x in ("4a5560", "8a97a4", "c6d2dc", "f2f8ff")]
GLASS = [H(x) for x in ("2f6f8a", "6fb8d0", "b8ecf8")]

class C:
    def __init__(s): s.p = {}
    def px(s, x, y, c):
        if 0 <= x < 16 and 0 <= y < 16: s.p[(x, y)] = c
    def rect(s, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): s.px(x, y, c)
    def line(s, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            s.px(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)
    def disc(s, cx, cy, r, c):
        for y in range(16):
            for x in range(16):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r: s.px(x, y, c)
    def ring(s, cx, cy, r, c, w=1.0):
        for y in range(16):
            for x in range(16):
                d = math.hypot(x - cx, y - cy)
                if r - w < d <= r: s.px(x, y, c)
    def outline(s, col=OUT):
        add = {}
        for (x, y) in s.p:
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                q = (x+dx, y+dy)
                if q not in s.p and 0 <= q[0] < 16 and 0 <= q[1] < 16: add[q] = col
        s.p.update(add)
    def img(s):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        for (x, y), c in s.p.items(): im.putpixel((x, y), c)
        return im

def lantern():
    c = C()
    c.line(6,1,6,3,BR[1]); c.line(9,1,9,3,BR[1]); c.line(6,1,9,1,BR[2])   # handle
    c.rect(5,3,10,4,BR[3]); c.px(5,3,BR[4])                                 # cap
    c.rect(4,4,11,4,BR[2])
    c.rect(5,5,10,11,BR[1])                                                 # frame
    c.rect(6,5,9,11,EM[2]); c.rect(7,6,8,10,EM[3]); c.rect(7,7,8,8,EM[4])   # flame glow
    c.px(6,5,EM[1]); c.px(9,5,EM[1]); c.px(6,11,EM[1]); c.px(9,11,EM[1])
    c.line(5,5,5,11,BR[3]); c.line(10,5,10,11,BR[0])
    c.rect(4,12,11,13,BR[3]); c.rect(4,13,11,13,BR[1]); c.rect(6,14,9,14,BR[0])
    c.px(4,12,BR[5])
    c.outline(); return c

def scimitar():
    c = C()
    pts = [(2,13),(3,10),(5,8),(7,6),(9,4),(11,3),(13,2),(14,3),(13,5),(11,6),(9,8),(7,10),(5,12)]
    # curved blade: build by thick curve
    curve = [(4,11),(5,9),(6,8),(8,6),(9,5),(11,4),(12,3),(13,3)]
    for i in range(len(curve)-1): c.line(*curve[i], *curve[i+1], STEEL[2])
    for (x,y) in curve: c.px(x,y+1,STEEL[1]); c.px(x+1,y,STEEL[3]) if (x+y)%2 else None
    c.px(13,3,STEEL[3]); c.px(14,2,STEEL[3]); c.px(14,3,STEEL[2])
    c.line(3,9,5,12,BR[3]) ; c.line(2,12,6,10,BR[4]); c.px(6,10,BR[3]); c.px(2,12,BR[2])  # guard
    c.line(3,13,1,15,WOOD[1]); c.px(2,14,WOOD[2]); c.px(1,15,BR[3])                     # grip
    c.px(4,11,TQ[2]); c.px(4,12,TQ[1])
    c.outline(); return c

def carpet():
    c = C()
    for y in range(4, 13):
        off = int((y - 8) * 0.5)
        for x in range(2, 14): c.px(x + (off if 0 else 0), y, RD[2] if y % 2 == 0 else RD[1])
    c.rect(2,4,13,12,RD[1]); c.rect(3,5,12,11,RD[2])
    for x in range(2, 14):  # border stripes
        c.px(x,4,BR[3]); c.px(x,12,BR[3])
    for y in range(4, 13): c.px(2,y,BR[2]); c.px(13,y,BR[2])
    c.rect(4,6,11,10,TQ[1]); c.rect(5,7,10,9,TQ[2])
    c.px(7,8,BR[5]); c.px(8,8,BR[5]); c.px(7,7,BR[4]); c.px(8,9,BR[4]); c.px(6,8,BR[3]); c.px(9,8,BR[3])
    for y in (4,6,8,10,12): c.px(1,y,BR[4]); c.px(14,y,BR[4])   # tassels
    for y in (5,7,9,11): c.px(1,y,BR[2]); c.px(14,y,BR[2])
    c.px(2,3,RD[3]); c.px(13,13,RD[0])
    c.outline(); return c

def astrolabe():
    c = C()
    c.disc(7.5,8.5,6.6,BR[2]); c.disc(7.5,8.5,5.4,BR[0]); c.disc(7.5,8.5,4.6,TQ[0])
    c.ring(7.5,8.5,3.6,TQ[1]); c.ring(7.5,8.5,2.2,TQ[2])
    c.rect(4,4,4,4,BR[4])
    c.line(3,8,12,8,BR[4]); c.line(7,3,7,13,BR[4]); c.line(8,3,8,13,BR[3])    # cross
    c.line(4,12,12,4,BR[5]); c.px(12,4,BR[5])                                  # alidade
    c.disc(7.5,8.5,1,BR[5])
    for a in range(0, 360, 45):                                                # tick marks
        x=round(7.5+6*math.cos(math.radians(a))); y=round(8.5+6*math.sin(math.radians(a))); c.px(x,y,BR[5])
    c.rect(6,0,9,1,BR[3]); c.px(7,0,BR[5]); c.px(6,2,BR[2]); c.px(9,2,BR[2]) # loop
    c.px(7,1,OUT); c.px(8,1,OUT)
    c.outline(); return c

def bottle():
    c = C()
    c.rect(6,1,9,2,WOOD[2]); c.rect(6,1,9,1,WOOD[1]); c.rect(6,3,9,4,GLASS[1])          # cork+neck
    c.px(6,3,GLASS[2]); c.rect(7,2,8,2,BR[3])
    c.rect(4,5,11,13,GLASS[1]); c.rect(5,4,10,4,GLASS[1]); c.rect(5,14,10,14,GLASS[0])
    c.rect(4,5,4,13,GLASS[0]); c.rect(11,5,11,13,GLASS[0])
    c.rect(5,8,10,13,TQ[1]); c.rect(5,8,10,8,TQ[3]); c.rect(6,9,9,13,TQ[2])            # potion
    c.px(7,10,ST[3]); c.px(8,11,ST[4]); c.px(6,12,ST[2])                                # sparkles
    c.px(5,5,GLASS[2]); c.px(5,6,GLASS[2]); c.px(5,7,GLASS[2])
    c.px(8,0,TQ[3]); c.px(9,0,TQ[2])                                                    # wisp
    c.outline(); return c

def seal(n):
    c = C()
    pal = [BR, TQ, EM, ST, RD, BR, BR][n-1]
    body = pal[2] if len(pal) > 4 else pal[2]
    c.disc(7.5,7.5,6.6,BR[1]); c.disc(7.5,7.5,5.7,BR[3]); c.disc(7.5,7.5,4.6,BR[2])
    c.ring(7.5,7.5,4.6,BR[4])
    for x,y in ((3,3),(4,2),(3,4)): c.px(x,y,BR[5])
    # rim ornament dots
    for a in range(0,360,45):
        c.px(round(7.5+5.2*math.cos(math.radians(a))),round(7.5+5.2*math.sin(math.radians(a))),BR[0])
    # inner gem colour differs by seal
    gem = [BR, TQ, EM, ST, RD, TQ, EM][n-1]
    c.disc(7.5,7.5,3.3,gem[0] if n!=1 else BR[0]); c.disc(7.5,7.5,2.6,gem[1])
    # pips = n dots (n=1..7) arranged on ring
    if n == 1: pos=[(7,7)]
    else:
        pos=[(round(7.5+2.6*math.cos(math.radians(-90+360*i/n))),round(7.5+2.6*math.sin(math.radians(-90+360*i/n)))) for i in range(n)]
    for (x,y) in pos: c.px(x,y,gem[3] if len(gem)>3 else BR[5])
    if n in (1,): c.px(8,7,BR[5]); c.px(7,8,BR[4]); c.px(8,8,BR[4])
    c.outline(); return c

def bow():
    c = C()
    arc = [(11,1),(12,2),(13,4),(13,6),(13,8),(12,10),(11,12),(10,14)]  # limb
    arc = [(3,1),(4,2),(5,3),(5,5),(5,7),(5,9),(5,11),(4,13),(3,14)]
    for i in range(len(arc)-1): c.line(*arc[i],*arc[i+1],WOOD[1])
    for (x,y) in arc: c.px(x+1,y,WOOD[2]) if y%3 else None
    c.rect(4,6,6,8,BR[3]); c.px(4,7,BR[5]); c.px(6,8,BR[1])  # grip
    c.px(3,1,BR[4]); c.px(3,14,BR[4]); c.px(2,0,TQ[2]); c.px(2,15,TQ[2])
    c.line(3,1,3,14,STEEL[3]) if False else None
    c.line(2,0,10,7,H("d8ccb0")) if False else None
    c.line(2,1,2,14,H("e8dcc0"))                                       # string
    c.line(3,7,13,7,WOOD[2]); c.px(14,7,STEEL[3]); c.px(13,6,STEEL[2]); c.px(13,8,STEEL[2])  # nocked arrow
    c.px(4,6,RD[2]); c.px(4,8,RD[2])
    c.outline(); return c

def dagger():
    c = C()
    c.line(12,3,5,10,STEEL[2]); c.line(13,3,6,10,STEEL[1]); c.line(12,2,13,2,STEEL[3]); c.px(13,3,STEEL[3])
    c.line(12,3,6,9,STEEL[3])
    c.line(4,7,9,12,BR[3]); c.line(4,8,8,12,BR[2]); c.px(4,7,BR[5])   # guard
    c.line(4,11,2,13,WOOD[1]); c.line(5,12,3,14,WOOD[2]); c.px(1,14,BR[3]); c.px(2,15,BR[3]); c.px(1,15,BR[2])
    c.px(6,9,TQ[2]); c.px(7,9,TQ[1])
    c.outline(); return c

def amulet():
    c = C()
    c.ring(7.5,3.5,3.4,BR[3]); c.px(7,0,BR[5]); c.px(3,3,BR[2])           # chain loop
    c.line(4,5,7,8,BR[2]); c.line(11,5,8,8,BR[2])
    c.disc(7.5,10,4.6,BR[1]); c.disc(7.5,10,3.8,BR[3]); c.disc(7.5,10,3,TQ[0])
    c.disc(7.5,10,2.3,TQ[1]); c.rect(7,9,8,10,TQ[3]); c.px(6,8,TQ[3]); c.px(7,11,TQ[2])
    c.px(7,6,BR[5]); c.px(7,14,BR[0]); c.px(3,10,BR[5]); c.px(12,10,BR[0])
    c.outline(); return c

def key():
    c = C()
    c.ring(4.5,4.5,3.6,BR[3],1.4); c.disc(4.5,4.5,1.3,OUT); c.px(3,2,BR[5]); c.px(2,3,BR[5])
    c.px(4,4,(0,0,0,0)); c.p.pop((4,4),None); c.p.pop((5,4),None); c.p.pop((4,5),None); c.p.pop((5,5),None)
    c.line(7,7,13,13,BR[3]); c.line(8,7,14,13,BR[2]); c.line(7,6,13,12,BR[4])
    c.rect(11,14,12,14,BR[2]); c.rect(13,11,14,12,BR[3]); c.px(14,13,BR[1])   # teeth
    c.line(12,10,10,12,BR[1]) if False else None
    c.px(10,10,TQ[2]); c.px(9,9,TQ[1])
    c.outline(); return c

ITEMS = {"lantern": lantern, "scimitar": scimitar, "carpet": carpet, "astrolabe": astrolabe,
         "bottle": bottle, "bow": bow, "dagger": dagger, "amulet": amulet, "key": key}
for i in range(1, 8): ITEMS[f"seal_{i}"] = (lambda n=i: seal(n))

EN = {"lantern": "Djinn Lantern", "scimitar": "Djinn Scimitar", "carpet": "Flying Carpet", "astrolabe": "Astrolabe",
      "bottle": "Djinn Bottle", "bow": "Desert Bow", "dagger": "Dagger", "amulet": "Amulet", "key": "Gate Key"}
AR = {"lantern": "فانوس الجني", "scimitar": "سيف الجن", "carpet": "بساط الريح", "astrolabe": "الإسطرلاب",
      "bottle": "قارورة الجني", "bow": "قوس الصحراء", "dagger": "خنجر", "amulet": "تعويذة", "key": "مفتاح البوابة"}
for i in range(1, 8):
    EN[f"seal_{i}"] = f"Brass Seal {i}"; AR[f"seal_{i}"] = f"ختم النحاس {i}"

def wj(p, o):
    with open(p, "w", encoding="utf-8") as f: json.dump(o, f, ensure_ascii=False, indent=2); f.write("\n")

images = {}
for name, fn in ITEMS.items():
    im = fn().img(); images[name] = im
    im.save(os.path.join(TEX, name + ".png"))
    wj(os.path.join(MOD, name + ".json"), {"parent": "minecraft:item/generated", "textures": {"layer0": f"nahas:item/{name}"}})
    wj(os.path.join(ITM, name + ".json"), {"model": {"type": "minecraft:model", "model": f"nahas:item/{name}"}})

ui_en = {f"item.nahas.{k}": v for k, v in EN.items()}
ui_ar = {f"item.nahas.{k}": v for k, v in AR.items()}
ui_ar.update({"nahas.title": "مدينة النحاس", "nahas.seals": "أختام النحاس", "nahas.gold": "الذهب"})
ui_en.update({"nahas.title": "City of Brass", "nahas.seals": "Brass Seals", "nahas.gold": "Gold"})
wj(os.path.join(LANG, "ar_sa.json"), ui_ar); wj(os.path.join(LANG, "en_us.json"), ui_en)

wj(os.path.join(RP, "pack.mcmeta"), {"pack": {
    "pack_format": 46,
    "supported_formats": {"min_inclusive": 46, "max_inclusive": 90},
    "min_format": 46, "max_format": 90,
    "description": "مدينة النحاس - City of Brass"}})

# pack.png: lantern on starry gradient
icon = Image.new("RGBA", (128, 128))
for y in range(128):
    for x in range(128):
        t = y / 127
        icon.putpixel((x, y), (int(20 + 30 * t), int(14 + 20 * t), int(60 - 20 * t), 255))
import random; rnd = random.Random(7)
for _ in range(30): icon.putpixel((rnd.randrange(128), rnd.randrange(80)), (255, 244, 184, 255))
big = images["lantern"].resize((112, 112), Image.NEAREST)
icon.alpha_composite(big, (8, 10)); icon.save(os.path.join(RP, "pack.png"))

# contact sheet
S = 8; cols = 8; cell = 16 * S + 24; names = list(ITEMS)
rows = math.ceil(len(names) / cols)
sheet = Image.new("RGBA", (cols * cell, rows * (cell + 16)), (34, 28, 44, 255))
d = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype("DejaVuSans.ttf", 13)
except Exception: font = ImageFont.load_default()
for i, n in enumerate(names):
    cx, cy = (i % cols) * cell, (i // cols) * (cell + 16)
    d.rectangle([cx + 6, cy + 6, cx + cell - 6, cy + 16 * S + 14], fill=(58, 50, 74, 255))
    sheet.alpha_composite(images[n].resize((16 * S, 16 * S), Image.NEAREST), (cx + 12, cy + 10))
    lab = EN[n]; w = d.textlength(lab, font=font)
    d.text((cx + (cell - w) / 2, cy + 16 * S + 18), lab, fill=(240, 220, 160, 255), font=font)
sheet.convert("RGB").save(os.path.join(ROOT, "docs/items_sheet.png"))
print("ok", len(names))
