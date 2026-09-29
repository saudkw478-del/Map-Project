#!/usr/bin/env python3
"""Generate the in-game world map item data (map_0) for the Nahas City world.

Output (into out/world/NahasCity/data/):
  map_0.dat     gzipped NBT, Minecraft 1.21.4 map format (DataVersion 3465 root so the game's DFU upgrades it like the region files)
  idcounts.dat  {data:{map:0}}  -> "last used map id = 0", so the next map created in-game gets id 1

Scale 4 (1 pixel = 16 blocks, 128 px = 2048 blocks) centred at (1200,1200) covers X,Z in [176,2224).
The outer ~176 blocks on each side (sea, lighthouse, some shipwrecks) are off the map.
Colour bytes = base_colour_id * 4 + brightness  (brightness 0=LOW 180, 1=NORMAL 220, 2=HIGH 255, 3=LOWEST 135).
Base colour ids come from net.minecraft.world.level.material.MapColor (1.21.x): 1 GRASS, 2 SAND, 8 SNOW, 10 DIRT, 11 STONE,
12 WATER, 14 QUARTZ, 21 COLOR_GRAY, 22 COLOR_LIGHT_GRAY, 28 COLOR_RED, 30 GOLD, 37 TERRACOTTA_ORANGE ...
"""
import gzip, json, os, struct, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
WORLD_DATA = os.path.join(OUT, "world", "NahasCity", "data")
DATA_VERSION = 3465
SCALE = 4
CX = CZ = 1200
BLOCKS_PER_PX = 1 << SCALE            # 16

# terrain class -> (base colour id, default brightness)
CLASS_COLOR = {
    0: (12, 0),    # deep sea       WATER, dark
    1: (12, 1),    # shallow sea    WATER
    2: (2, 1),     # golden dunes   SAND
    3: (37, 1),    # red canyons    TERRACOTTA_ORANGE
    4: (1, 1),     # oasis / grass  GRASS
    5: (8, 1),     # salt flat      SNOW
    6: (21, 0),    # basalt         COLOR_GRAY (dark)
    7: (10, 1),    # caravan road   DIRT
    8: (30, 1),    # brass city     GOLD
    9: (12, 2),    # lake / pond    WATER, bright
    10: (2, 2),    # beach          SAND, bright
    11: (22, 2),   # POI plaza      COLOR_LIGHT_GRAY
}
RELIEF = {2, 3, 4, 5, 6, 10}      # classes that get height-relief shading (like vanilla terrain)
RED, WHITE = 28, 8


def build_colors():
    cls = np.load(os.path.join(OUT, "terrain_raster.npy"))
    hgt = np.load(os.path.join(OUT, "heightmap_u8.npy")).astype(np.float32)
    assert cls.shape == (2400, 2400)
    n = 128
    x0 = CX - 64 * BLOCKS_PER_PX
    z0 = CZ - 64 * BLOCKS_PER_PX
    col = np.zeros((n, n), np.uint8)     # [pz, px]
    for pz in range(n):
        for px in range(n):
            bx, bz = x0 + px * BLOCKS_PER_PX, z0 + pz * BLOCKS_PER_PX
            xs, zs = slice(max(bx, 0), max(min(bx + 16, 2400), 0)), slice(max(bz, 0), max(min(bz + 16, 2400), 0))
            cell = cls[zs, xs]
            if cell.size == 0:
                col[pz, px] = 0      # transparent (outside the pre-generated world)
                continue
            cnt = np.bincount(cell.ravel(), minlength=12)
            k = int(cnt.argmax())
            # thin features vanish under majority vote at 16 blocks/pixel: give them priority
            if cnt[8] >= 64: k = 8
            elif cnt[7] >= 6 and k not in (0, 1, 8, 9): k = 7
            elif cnt[11] >= 40 and k not in (0, 1, 8): k = 11
            elif cnt[9] >= 60: k = 9
            base, br = CLASS_COLOR[k]
            if k in RELIEF:
                hh = hgt[zs, xs]
                # slope along the NW->SE light direction, coarse (vanilla-style relief)
                a = hh[: max(1, hh.shape[0] // 2)].mean(); b = hh[hh.shape[0] // 2:].mean() if hh.shape[0] > 1 else a
                c = hh[:, : max(1, hh.shape[1] // 2)].mean(); d = hh[:, hh.shape[1] // 2:].mean() if hh.shape[1] > 1 else c
                s = (a - b) + (c - d)
                br = 2 if s > 2.5 else (0 if s < -2.5 else 1)
                if k == 6 and hh.mean() > 95: base, br = 11, 1      # high basalt peaks: STONE
            col[pz, px] = base * 4 + br
    # mark the main POIs (3x3 red square, white centre)
    man = json.load(open(os.path.join(OUT, "poi_manifest.json"), encoding="utf-8"))
    marks = []
    for p in man["pois"]:
        if p.get("kind") != "main" or p.get("dimension", "minecraft:overworld") != "minecraft:overworld":
            continue
        px, pz = (p["x"] - x0) // BLOCKS_PER_PX, (p["z"] - z0) // BLOCKS_PER_PX
        if 1 <= px < n - 1 and 1 <= pz < n - 1:
            col[pz - 1:pz + 2, px - 1:px + 2] = RED * 4 + 2
            col[pz, px] = WHITE * 4 + 1
            marks.append((p["id"], int(px), int(pz)))
    return col, marks


def write():
    col, marks = build_colors()
    flat = col.reshape(-1).astype(np.int8)          # index = x + z*128
    assert flat.size == 16384
    os.makedirs(WORLD_DATA, exist_ok=True)

    def nm(n):
        e = n.encode(); return struct.pack(">H", len(e)) + e

    def t_byte(n, v): return b"\x01" + nm(n) + struct.pack(">b", v)
    def t_int(n, v): return b"\x03" + nm(n) + struct.pack(">i", v)
    def t_str(n, v): e = v.encode(); return b"\x08" + nm(n) + struct.pack(">H", len(e)) + e
    def t_bytes(n, arr): return b"\x07" + nm(n) + struct.pack(">i", len(arr)) + arr.tobytes()
    def t_empty_list(n): return b"\x09" + nm(n) + b"\x0a" + struct.pack(">i", 0)   # list of compounds, length 0
    def compound(n, body): return b"\x0a" + nm(n) + body + b"\x00"

    map_body = (t_byte("scale", SCALE) + t_str("dimension", "minecraft:overworld") + t_byte("trackingPosition", 1)
                + t_byte("unlimitedTracking", 0) + t_byte("locked", 1) + t_int("xCenter", CX) + t_int("zCenter", CZ)
                + t_bytes("colors", flat) + t_empty_list("banners") + t_empty_list("frames"))
    root = compound("", compound("data", map_body) + t_int("DataVersion", DATA_VERSION))
    idc = compound("", compound("data", t_int("map", 0)) + t_int("DataVersion", DATA_VERSION))
    for fn, raw in (("map_0.dat", root), ("idcounts.dat", idc)):
        with gzip.GzipFile(os.path.join(WORLD_DATA, fn), "wb", mtime=0) as f:
            f.write(raw)
    # preview PNG (concept render of the map colours; approximate RGB)
    try:
        from PIL import Image
        rgb = {1: (127, 178, 56), 2: (247, 233, 163), 8: (255, 255, 255), 10: (151, 109, 77), 11: (112, 112, 112), 12: (64, 64, 255),
               14: (255, 252, 245), 21: (76, 76, 76), 22: (153, 153, 153), 28: (153, 51, 51), 30: (250, 238, 77), 37: (216, 127, 51)}
        mult = {0: 180, 1: 220, 2: 255, 3: 135}
        im = np.zeros((128, 128, 3), np.uint8)
        for pz in range(128):
            for px in range(128):
                v = int(col[pz, px]); b, s = v >> 2, v & 3
                c = rgb.get(b, (0, 0, 0)) if b else (30, 30, 30)
                im[pz, px] = [c_ * mult[s] // 255 for c_ in c]
        Image.fromarray(im).resize((768, 768), Image.NEAREST).save(os.path.join(OUT, "map_item_preview.png"))
    except Exception as e:                                # pragma: no cover
        print("preview skipped:", e)
    print("map_0.dat + idcounts.dat written; colour ids used:", sorted(set((col.reshape(-1) >> 2).tolist())), "POI marks:", marks)


if __name__ == "__main__":
    write()
