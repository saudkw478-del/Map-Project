"""First-person voxel renderer for the generated Westeros world (concept renders, not real game screenshots).

Reads the region files directly, builds a dense block grid, computes Minecraft-style block/sky light and
ray-casts each pixel with a DDA. Textures are procedural (no Mojang assets are used)."""
import io
import os
import struct
import zlib

import nbtlib
import numba as nb
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WORLD = os.environ.get("GOT_WORLD", "/home/user/Map-Project/world/GoT_Westeros/region")
Y0, Y1 = 44, 196          # rendered vertical range

# ---------------------------------------------------------------- block appearance

WOOL = {"white": (233, 236, 236), "orange": (240, 118, 19), "magenta": (189, 68, 179), "light_blue": (58, 175, 217),
        "yellow": (248, 197, 39), "lime": (112, 185, 25), "pink": (237, 141, 172), "gray": (62, 68, 71),
        "light_gray": (142, 142, 134), "cyan": (21, 137, 145), "purple": (121, 42, 172), "blue": (53, 57, 157),
        "brown": (114, 71, 40), "green": (84, 109, 27), "red": (160, 39, 34), "black": (20, 21, 25)}

# kinds
PLAIN, BRICKS, PLANKS, LOG, GRASS, LEAVES, WATER, GLASS, BARS, LADDER, SMALLLIGHT, SNOW, STONE, SAND, ROOF = range(15)

RULES = [  # substring, rgb, kind, emit light
    ("water", (48, 84, 210), WATER, 0),
    ("white_terracotta", (209, 178, 161), ROOF, 0),
    ("light_gray_terracotta", (135, 106, 97), ROOF, 0),
    ("farmland", (110, 75, 45), PLAIN, 0),
    ("bone_block", (225, 221, 199), PLAIN, 0),
    ("magma_block", (140, 50, 20), PLAIN, 6),
    ("obsidian", (20, 16, 32), PLAIN, 0),
    ("gold_ore", (150, 140, 95), STONE, 0),
    ("raw_gold_block", (215, 175, 50), PLAIN, 0),
    ("gold_block", (250, 220, 70), PLAIN, 0),
    ("smooth_stone", (165, 165, 165), PLAIN, 0),
    ("barrel", (140, 100, 55), PLANKS, 0),
    ("cactus", (30, 110, 40), PLAIN, 0),
    ("jungle_log", (110, 80, 50), LOG, 0),
    ("acacia_log", (120, 110, 100), LOG, 0),
    ("glass", (180, 200, 220), GLASS, 0),
    ("iron_bars", (170, 172, 175), BARS, 0),
    ("ladder", (140, 104, 60), LADDER, 0),
    ("lantern", (255, 190, 90), SMALLLIGHT, 15),
    ("torch", (255, 200, 90), SMALLLIGHT, 14),
    ("campfire", (255, 130, 40), SMALLLIGHT, 15),
    ("sea_lantern", (172, 199, 190), PLAIN, 15),
    ("grass_block", (100, 160, 60), GRASS, 0),
    ("podzol", (110, 75, 30), GRASS, 0),
    ("snow_block", (245, 248, 250), SNOW, 0),
    ("packed_ice", (141, 180, 250), SNOW, 0),
    ("blue_ice", (116, 167, 253), SNOW, 0),
    ("oak_leaves", (58, 120, 40), LEAVES, 0),
    ("spruce_leaves", (40, 82, 50), LEAVES, 0),
    ("leaves", (50, 100, 40), LEAVES, 0),
    ("birch_log", (216, 214, 205), LOG, 0),
    ("dark_oak_log", (62, 46, 28), LOG, 0),
    ("spruce_log", (58, 38, 18), LOG, 0),
    ("oak_log", (105, 84, 50), LOG, 0),
    ("_log", (95, 75, 45), LOG, 0),
    ("dark_oak_planks", (66, 43, 20), PLANKS, 0),
    ("spruce_planks", (114, 84, 48), PLANKS, 0),
    ("oak_planks", (162, 130, 78), PLANKS, 0),
    ("_planks", (150, 120, 70), PLANKS, 0),
    ("dark_oak", (66, 43, 20), PLANKS, 0),
    ("spruce", (114, 84, 48), PLANKS, 0),
    ("oak", (162, 130, 78), PLANKS, 0),
    ("oxidized_cut_copper", (82, 162, 132), ROOF, 0),
    ("deepslate_tiles", (54, 54, 58), ROOF, 0),
    ("_terracotta", (152, 94, 67), ROOF, 0),
    ("terracotta", (152, 94, 67), ROOF, 0),
    ("mossy_stone_brick", (105, 122, 92), BRICKS, 0),
    ("mossy_cobblestone", (100, 118, 90), STONE, 0),
    ("polished_blackstone_brick", (46, 42, 50), BRICKS, 0),
    ("polished_blackstone", (54, 50, 58), PLAIN, 0),
    ("blackstone", (42, 36, 41), STONE, 0),
    ("red_nether_brick", (92, 12, 14), BRICKS, 0),
    ("nether_brick", (48, 24, 28), BRICKS, 0),
    ("deepslate_brick", (72, 72, 76), BRICKS, 0),
    ("cobbled_deepslate", (77, 77, 82), STONE, 0),
    ("polished_deepslate", (72, 72, 76), PLAIN, 0),
    ("deepslate", (77, 77, 81), STONE, 0),
    ("stone_brick", (122, 122, 122), BRICKS, 0),
    ("quartz_brick", (236, 230, 223), BRICKS, 0),
    ("quartz", (236, 230, 223), PLAIN, 0),
    ("diorite", (190, 190, 190), PLAIN, 0),
    ("andesite", (136, 136, 136), PLAIN, 0),
    ("brick", (150, 97, 83), BRICKS, 0),
    ("red_sandstone", (181, 98, 32), SAND, 0),
    ("sandstone", (216, 203, 155), SAND, 0),
    ("red_sand", (190, 102, 33), SAND, 0),
    ("sand", (219, 207, 163), SAND, 0),
    ("cobblestone", (118, 118, 118), STONE, 0),
    ("gravel", (131, 127, 126), STONE, 0),
    ("coarse_dirt", (119, 85, 59), PLAIN, 0),
    ("mud", (62, 58, 62), PLAIN, 0),
    ("dirt", (134, 96, 67), PLAIN, 0),
    ("stone", (125, 125, 125), STONE, 0),
    ("iron_block", (222, 222, 222), PLAIN, 0),
    ("bedrock", (60, 60, 60), STONE, 0),
    ("chest", (150, 105, 40), PLANKS, 0),
    ("hay_block", (200, 170, 40), PLANKS, 0),
    ("pumpkin", (210, 130, 30), PLAIN, 0),
    ("crafting_table", (150, 110, 60), PLANKS, 0),
    ("furnace", (100, 100, 100), STONE, 0),
    ("anvil", (60, 60, 64), PLAIN, 0),
    ("grindstone", (140, 140, 140), STONE, 0),
    ("smithing_table", (60, 50, 60), PLANKS, 0),
    ("birch", (216, 214, 205), PLANKS, 0),
]


def classify(name):
    n = name.replace("minecraft:", "")
    for c, rgb in WOOL.items():
        if n.startswith(c + "_") and ("banner" in n or "carpet" in n or "wool" in n or "concrete" in n):
            return rgb, PLAIN, 0
    if n.endswith("_wool"):
        return (161, 39, 34), PLAIN, 0
    for sub, rgb, kind, emit in RULES:
        if sub in n:
            return rgb, kind, emit
    h = zlib.crc32(n.encode()) & 0xFFFFFF
    return ((h >> 16) & 255 // 1 | 60, (h >> 8) & 255 | 60, h & 255 | 60), PLAIN, 0


PLANTS = {"poppy", "dandelion", "azure_bluet", "oxeye_daisy", "allium", "grass", "short_grass", "fern", "dead_bush", "tall_grass",
          "large_fern", "peony", "rose_bush", "lilac", "cornflower", "red_tulip", "pink_tulip", "wheat", "carrots", "cobweb",
          "skeleton_skull", "wither_rose", "lava_dummy"}


class Grid:
    def __init__(self, x0, x1, z0, z1):
        self.x0, self.x1, self.z0, self.z1 = x0, x1, z0, z1
        self.W, self.H, self.D = x1 - x0, Y1 - Y0, z1 - z0
        self.g = np.zeros((self.W, self.H, self.D), dtype=np.uint8)
        self.names = ["minecraft:air"]
        self.ids = {"minecraft:air": 0}

    def gid(self, name):
        i = self.ids.get(name)
        if i is None:
            i = self.ids[name] = len(self.names)
            self.names.append(name)
        return i


_chunk_cache = {}


def read_chunk(cx, cz):
    key = (cx, cz)
    if key in _chunk_cache:
        return _chunk_cache[key]
    rx, rz = cx >> 5, cz >> 5
    path = os.path.join(WORLD, f"r.{rx}.{rz}.mca")
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        d = f.read()
    i = (cx & 31) + (cz & 31) * 32
    loc = struct.unpack(">I", d[i * 4:i * 4 + 4])[0]
    if not loc:
        return None
    sec = loc >> 8
    ln, _ = struct.unpack(">IB", d[sec * 4096:sec * 4096 + 5])
    root = nbtlib.File.parse(io.BytesIO(zlib.decompress(d[sec * 4096 + 5:sec * 4096 + 4 + ln])))[""]
    _chunk_cache[key] = root
    return root


def load_grid(x0, x1, z0, z1):
    G = Grid(x0, x1, z0, z1)
    for cx in range(x0 >> 4, (x1 - 1 >> 4) + 1):
        for cz in range(z0 >> 4, (z1 - 1 >> 4) + 1):
            root = read_chunk(cx, cz)
            if root is None:
                continue
            for s in root["sections"]:
                sy = int(s["Y"]) * 16
                if sy + 16 <= Y0 or sy >= Y1:
                    continue
                pal = [str(p["Name"]) for p in s["block_states"]["palette"]]
                pid = np.array([G.gid(n) for n in pal], dtype=np.uint8)
                if len(pal) == 1:
                    arr = np.full((16, 16, 16), pid[0], dtype=np.uint8)
                else:
                    bits = max(4, int(np.ceil(np.log2(len(pal)))))
                    per = 64 // bits
                    longs = np.array(s["block_states"]["data"], dtype=np.int64).view(np.uint64)
                    k = np.arange(4096)
                    idx = ((longs[k // per] >> (np.uint64(bits) * (k % per).astype(np.uint64))) & np.uint64((1 << bits) - 1)).astype(int)
                    arr = pid[idx].reshape(16, 16, 16)      # y z x
                arr = arr.transpose(2, 0, 1)                 # x y z
                # clip into the grid
                gx0, gz0 = cx * 16, cz * 16
                xa, xb = max(gx0, x0), min(gx0 + 16, x1)
                za, zb = max(gz0, z0), min(gz0 + 16, z1)
                ya, yb = max(sy, Y0), min(sy + 16, Y1)
                if xa >= xb or za >= zb or ya >= yb:
                    continue
                G.g[xa - x0:xb - x0, ya - Y0:yb - Y0, za - z0:zb - z0] = arr[xa - gx0:xb - gx0, ya - sy:yb - sy, za - gz0:zb - gz0]
    return G


def prepare(G):
    """Preprocess: drop plants, flatten carpets into the floor colour; build appearance tables."""
    names = G.names
    n = len(names)
    rgb = np.zeros((n + 40, 3), dtype=np.float32)
    kind = np.zeros(n + 40, dtype=np.int32)
    emit = np.zeros(n + 40, dtype=np.int32)
    solid = np.ones(n + 40, dtype=np.uint8)
    remap = np.arange(n + 40, dtype=np.uint8)
    carpet_ids = {}
    for i, nm in enumerate(names):
        short = nm.replace("minecraft:", "")
        c, k, e = classify(nm)
        rgb[i], kind[i], emit[i] = c, k, e
        if i == 0:
            solid[i] = 0
        if short in PLANTS:
            remap[i] = 0
            solid[i] = 0
        if k in (WATER, GLASS, BARS, LADDER, SMALLLIGHT):
            solid[i] = 0
        if short.endswith("_carpet"):
            remap[i] = 0
            carpet_ids[i] = c
        if short == "snow":
            remap[i] = 0
            carpet_ids[i] = (246, 249, 252)
    solid[0] = 0
    g = G.g
    # carpets: recolour the block below (top surface reads as carpet)
    extra = n
    for cid, col in carpet_ids.items():
        ys = np.argwhere(g == cid)
        if len(ys) == 0:
            continue
        rgb[extra] = col
        kind[extra] = PLAIN
        for (x, y, z) in ys:
            if y > 0:
                g[x, y - 1, z] = extra
        extra += 1
    g = remap[g]
    return g, rgb[:extra], kind[:extra], emit[:extra], solid[:extra]


@nb.njit(cache=True)
def compute_light(g, solid, emit, night):
    W, H, D = g.shape
    light = np.zeros((W, H, D), dtype=np.uint8)
    qx = np.empty(W * H * D // 2 + 1024, dtype=np.int32)
    qy = np.empty_like(qx)
    qz = np.empty_like(qx)
    head = 0
    tail = 0
    sky = 15
    if night == 1:
        sky = 5
    if night == 2:
        sky = 9
    # sky light: straight down from the top until an opaque block; only cells next to a lower column propagate sideways
    top = np.zeros((W, D), dtype=np.int32)
    for x in range(W):
        for z in range(D):
            t = -1
            for y in range(H - 1, -1, -1):
                if solid[g[x, y, z]] == 1:
                    t = y
                    break
            top[x, z] = t
            for y in range(H - 1, t, -1):
                light[x, y, z] = sky
    for x in range(W):
        for z in range(D):
            for y in range(top[x, z] + 1, min(H, top[x, z] + 40)):
                edge = False
                if x > 0 and top[x - 1, z] >= y: edge = True
                if x < W - 1 and top[x + 1, z] >= y: edge = True
                if z > 0 and top[x, z - 1] >= y: edge = True
                if z < D - 1 and top[x, z + 1] >= y: edge = True
                if edge and tail < qx.shape[0]:
                    qx[tail] = x; qy[tail] = y; qz[tail] = z; tail += 1
    # block light sources
    for x in range(W):
        for y in range(H):
            for z in range(D):
                e = emit[g[x, y, z]]
                if e > light[x, y, z]:
                    light[x, y, z] = e
                    if tail < qx.shape[0]:
                        qx[tail] = x; qy[tail] = y; qz[tail] = z; tail += 1
    # BFS
    while head < tail:
        x = qx[head]; y = qy[head]; z = qz[head]; head += 1
        l = light[x, y, z]
        if l <= 1:
            continue
        for d in range(6):
            nx = x + (1 if d == 0 else (-1 if d == 1 else 0))
            ny = y + (1 if d == 2 else (-1 if d == 3 else 0))
            nz = z + (1 if d == 4 else (-1 if d == 5 else 0))
            if nx < 0 or ny < 0 or nz < 0 or nx >= W or ny >= H or nz >= D:
                continue
            if solid[g[nx, ny, nz]] == 1:
                continue
            if light[nx, ny, nz] < l - 1:
                light[nx, ny, nz] = l - 1
                if tail < qx.shape[0]:
                    qx[tail] = nx; qy[tail] = ny; qz[tail] = nz; tail += 1
    return light


@nb.njit(cache=True, inline="always")
def hsh(a, b, c, d):
    x = (a * 374761393 + b * 668265263 + c * 1274126177 + d * 362437) & 0x7FFFFFFF
    x = (x ^ (x >> 13)) * 1274126177 & 0x7FFFFFFF
    return ((x ^ (x >> 16)) & 1023) / 1023.0


@nb.njit(cache=True)
def texel(kind, base, face, bx, by, bz, u, v):
    """Procedural 16x16 texture. u,v in [0,1). Returns (r,g,b,alpha)."""
    tu = int(u * 16)
    tv = int(v * 16)
    n = hsh(bx * 16 + tu, by * 16 + tv, bz * 16 + tu * 7 + tv, face)
    r, g, b = base[0], base[1], base[2]
    a = 1.0
    f = 0.9 + 0.2 * n
    if kind == 1:        # bricks
        row = tv // 4
        off = 4 if row % 2 == 1 else 0
        if tv % 4 == 3 or (tu + off) % 8 == 7:
            f = 0.62 + 0.08 * n
        else:
            f = 0.95 + 0.1 * n
    elif kind == 2:      # planks
        if tv % 4 == 3:
            f = 0.72
        else:
            f = 0.92 + 0.14 * n
    elif kind == 3:      # log
        if face == 2 or face == 3:
            d = ((tu - 8) ** 2 + (tv - 8) ** 2) ** 0.5
            f = 1.15 - 0.1 * (int(d) % 3) + 0.05 * n
        else:
            f = 0.75 + 0.25 * hsh(bx, tu, bz, 7) + 0.05 * n
    elif kind == 4:      # grass
        if face == 2:
            f = 0.85 + 0.3 * n
        elif face == 3:
            r, g, b = 134.0, 96.0, 67.0
        else:
            if tv < 3 or (tv < 5 and n > 0.5):
                f = 0.85 + 0.3 * n
            else:
                r, g, b = 134.0, 96.0, 67.0
                f = 0.9 + 0.2 * n
    elif kind == 5:      # leaves
        f = 0.5 + 0.7 * n
        if n < 0.08:
            f = 0.3
    elif kind == 6:      # water
        a = 0.62
        f = 0.95 + 0.1 * n
    elif kind == 7:      # glass
        a = 0.35 if not (tu == 0 or tv == 0 or tu == 15 or tv == 15) else 0.9
    elif kind == 8:      # bars
        if not (tu in (7, 8) or tv in (7, 8)):
            a = 0.0
    elif kind == 9:      # ladder
        if not (tu in (2, 3, 12, 13) or (tv % 4 == 1)):
            a = 0.0
    elif kind == 10:     # small emissive light (torch / lantern)
        if not (tu >= 5 and tu <= 10 and tv >= 3 and tv <= 12):
            a = 0.0
        f = 1.0
    elif kind == 11:     # snow / ice
        f = 0.95 + 0.08 * n
    elif kind == 12:     # stone
        f = 0.82 + 0.3 * n
    elif kind == 13:     # sand
        f = 0.92 + 0.14 * n
    elif kind == 14:     # roof tiles
        if tv % 4 == 3:
            f = 0.7
        else:
            f = 0.9 + 0.2 * n
    else:
        f = 0.94 + 0.12 * n
    return r * f, g * f, b * f, a


@nb.njit(cache=True)
def sky_color(dy, dx, dz, night, ox, oz):
    t = min(max(dy, 0.0), 1.0)
    if night == 0:
        r = 0.62 + (0.32 - 0.62) * t ** 0.5
        g = 0.78 + (0.55 - 0.78) * t ** 0.5
        b = 0.95 + (0.92 - 0.95) * t ** 0.3
        return r * 255, g * 255, b * 255
    if night == 2:
        u = 1.0 - min(max(dy, 0.0), 1.0) ** 0.45
        r = 0.10 + 0.78 * u * u
        g = 0.12 + 0.42 * u * u
        b = 0.30 + 0.05 * u - 0.10 * u * u
        return r * 255, g * 255, b * 255
    r = 0.05 + 0.02 * t
    g = 0.07 + 0.04 * t
    b = 0.16 + 0.10 * t
    return r * 255, g * 255, b * 255



@nb.njit(cache=True)
def entity_hit(ox, oy, oz, dx, dy, dz, boxes, bpos, bcs, bcol, btex, buv, tex, tmax):
    """Nearest opaque entity-box hit along the ray. Returns (t, r, g, b, ent_x, ent_y, ent_z) (t=1e30 if none)."""
    best = 1e30
    br = 0.0; bg = 0.0; bb = 0.0
    bx = 0.0; by = 0.0; bz = 0.0
    n = boxes.shape[0]
    for i in range(n):
        c = bcs[i, 0]; s_ = bcs[i, 1]
        px = ox - bpos[i, 0]; py = oy - bpos[i, 1]; pz = oz - bpos[i, 2]
        lox = px * c + pz * s_
        loz = -px * s_ + pz * c
        loy = py
        ldx = dx * c + dz * s_
        ldz = -dx * s_ + dz * c
        ldy = dy
        t0 = 0.0; t1 = tmax
        face_in = -1
        ok = True
        # slab test on 3 axes
        for ax in range(3):
            if ax == 0:
                o = lox; d = ldx
            elif ax == 1:
                o = loy; d = ldy
            else:
                o = loz; d = ldz
            lo = boxes[i, ax]; hi = boxes[i, ax + 3]
            if abs(d) < 1e-9:
                if o < lo or o > hi:
                    ok = False
                    break
            else:
                ta = (lo - o) / d
                tb = (hi - o) / d
                fa = ax * 2 + 1      # entering through the -side when moving +  (face index of the slab we enter)
                if ta > tb:
                    tmp = ta; ta = tb; tb = tmp
                    fa = ax * 2
                if ta > t0:
                    t0 = ta; face_in = fa
                if tb < t1:
                    t1 = tb
                if t0 > t1:
                    ok = False
                    break
        if not ok or face_in < 0 or t0 >= best:
            continue
        hx = lox + ldx * t0; hy = loy + ldy * t0; hz = loz + ldz * t0
        # face_in: 0 = +x face hit (entering from +x), 1 = -x, 2 = +y, 3 = -y, 4 = +z, 5 = -z
        f = face_in
        x0 = boxes[i, 0]; y0 = boxes[i, 1]; z0 = boxes[i, 2]
        x1 = boxes[i, 3]; y1 = boxes[i, 4]; z1 = boxes[i, 5]
        u = 0.0; v = 0.0
        if f == 4:
            u = (hx - x0) / (x1 - x0); v = (y1 - hy) / (y1 - y0)
        elif f == 5:
            u = (x1 - hx) / (x1 - x0); v = (y1 - hy) / (y1 - y0)
        elif f == 0:
            u = (z1 - hz) / (z1 - z0); v = (y1 - hy) / (y1 - y0)
        elif f == 1:
            u = (hz - z0) / (z1 - z0); v = (y1 - hy) / (y1 - y0)
        elif f == 2:
            u = (hx - x0) / (x1 - x0); v = (hz - z0) / (z1 - z0)
        else:
            u = (hx - x0) / (x1 - x0); v = (z1 - hz) / (z1 - z0)
        u = min(max(u, 0.0), 0.9999); v = min(max(v, 0.0), 0.9999)
        shade = 0.85
        if f == 2:
            shade = 1.0
        elif f == 3:
            shade = 0.55
        elif f == 0 or f == 1:
            shade = 0.7
        if btex[i] >= 0:
            uu = buv[i, f, 0] + u * buv[i, f, 2]
            vv = buv[i, f, 1] + v * buv[i, f, 3]
            iu = min(max(int(uu), 0), 63); iv = min(max(int(vv), 0), 63)
            a = tex[btex[i], iv, iu, 3]
            if a < 128:
                continue
            cr = tex[btex[i], iv, iu, 0]; cg = tex[btex[i], iv, iu, 1]; cb = tex[btex[i], iv, iu, 2]
        else:
            cr = bcol[i, 0]; cg = bcol[i, 1]; cb = bcol[i, 2]
            if buv[i, 0, 0] > 0:     # cheap variation for solid boxes
                pass
        best = t0
        br = cr * shade; bg = cg * shade; bb = cb * shade
        bx = bpos[i, 0]; by = bpos[i, 1] + 1.0; bz = bpos[i, 2]
    return best, br, bg, bb, bx, by, bz


@nb.njit(parallel=True, cache=True)
def render(g, light, rgb, kind, emit, solid, eye, fwd, right, up, tanf, aspect, W, H, maxd, night, sunx, suny, sunz,
           boxes, bpos, bcs, bcol, btex, buv, tex):
    GX, GY, GZ = g.shape
    img = np.zeros((H, W, 3), dtype=np.float32)
    for py in nb.prange(H):
        for px in range(W):
            sx = (2.0 * (px + 0.5) / W - 1.0) * tanf * aspect
            sy = (1.0 - 2.0 * (py + 0.5) / H) * tanf
            dx = fwd[0] + right[0] * sx + up[0] * sy
            dy = fwd[1] + right[1] * sx + up[1] * sy
            dz = fwd[2] + right[2] * sx + up[2] * sy
            ln = (dx * dx + dy * dy + dz * dz) ** 0.5
            dx /= ln; dy /= ln; dz /= ln
            # background: sky + sun + clouds
            sr, sg, sb = sky_color(dy, dx, dz, night, eye[0], eye[2])
            dot = dx * sunx + dy * suny + dz * sunz
            if night == 0 and dot > 0.9985:
                sr, sg, sb = 255.0, 250.0, 210.0
            if night == 1:
                hs = hsh(int((dx + 2) * 400), int((dy + 2) * 400), int((dz + 2) * 400), 5)
                if hs > 0.9985 and dy > 0.05:
                    sr, sg, sb = 230.0, 230.0, 255.0
                if dot > 0.998:
                    sr, sg, sb = 235.0, 235.0, 225.0
            if dy > 0.02 and night == 0:
                tcl = (230.0 - eye[1]) / dy
                cx = eye[0] + dx * tcl
                cz = eye[2] + dz * tcl
                if tcl < 2500.0 and hsh(int(cx // 16), 3, int(cz // 16), 9) > 0.7:
                    fade = 1.0 - min(tcl / 2500.0, 1.0)
                    sr = sr + (250.0 - sr) * 0.75 * fade
                    sg = sg + (252.0 - sg) * 0.75 * fade
                    sb = sb + (255.0 - sb) * 0.75 * fade
            et, er, eg, eb, ex_, ey_, ez_ = entity_hit(eye[0], eye[1], eye[2], dx, dy, dz, boxes, bpos, bcs, bcol, btex, buv, tex, maxd)
            # DDA
            mx = int(np.floor(eye[0])); my = int(np.floor(eye[1])); mz = int(np.floor(eye[2]))
            ddx = abs(1.0 / dx) if dx != 0 else 1e30
            ddy = abs(1.0 / dy) if dy != 0 else 1e30
            ddz = abs(1.0 / dz) if dz != 0 else 1e30
            stx = 1 if dx > 0 else -1
            sty = 1 if dy > 0 else -1
            stz = 1 if dz > 0 else -1
            sdx = ((mx + 1 - eye[0]) if dx > 0 else (eye[0] - mx)) * ddx
            sdy = ((my + 1 - eye[1]) if dy > 0 else (eye[1] - my)) * ddy
            sdz = ((mz + 1 - eye[2]) if dz > 0 else (eye[2] - mz)) * ddz
            accr = 0.0; accg = 0.0; accb = 0.0
            trans = 1.0
            t = 0.0
            face = 0
            steps = 0
            hit_end = False
            while steps < 700:
                steps += 1
                if sdx < sdy and sdx < sdz:
                    t = sdx; sdx += ddx; mx += stx; face = 0 if stx < 0 else 1   # 0/1 = -x/+x side hit
                elif sdy < sdz:
                    t = sdy; sdy += ddy; my += sty; face = 2 if sty > 0 else 3   # entering from below => hit bottom(3)? see below
                else:
                    t = sdz; sdz += ddz; mz += stz; face = 4 if stz < 0 else 5
                if t > maxd:
                    break
                if t > et:
                    break
                if mx < 0 or mx >= GX or mz < 0 or mz >= GZ or my < 0 or my >= GY:
                    if my >= GY and dy >= 0:
                        break
                    if my < 0:
                        break
                    if mx < 0 or mx >= GX or mz < 0 or mz >= GZ:
                        break
                    continue
                b = g[mx, my, mz]
                if b == 0:
                    continue
                # face: entering block from the side we came from
                # face codes: 0 -> hit its +x face (moving -x)... normalise below
                hx = eye[0] + dx * t
                hy = eye[1] + dy * t
                hz = eye[2] + dz * t
                fx = hx - mx; fy = hy - my; fz = hz - mz
                # neighbour (air cell we came from) for lighting
                nxm = mx; nym = my; nzm = mz
                if face == 0: nxm = mx + 1; u = fz; v = 1.0 - fy; shade = 0.6; fc = 0
                elif face == 1: nxm = mx - 1; u = fz; v = 1.0 - fy; shade = 0.6; fc = 1
                elif face == 2: nym = my - 1; u = fx; v = fz; shade = 0.5; fc = 3      # moving up: we hit the bottom face
                elif face == 3: nym = my + 1; u = fx; v = fz; shade = 1.0; fc = 2      # moving down: hit top face
                elif face == 4: nzm = mz + 1; u = fx; v = 1.0 - fy; shade = 0.8; fc = 4
                else: nzm = mz - 1; u = fx; v = 1.0 - fy; shade = 0.8; fc = 5
                u = min(max(u, 0.0), 0.9999); v = min(max(v, 0.0), 0.9999)
                tr, tg, tb, ta = texel(kind[b], rgb[b], fc, mx, my, mz, u, v)
                if ta <= 0.02:
                    continue
                lv = 0
                if nxm >= 0 and nxm < GX and nym >= 0 and nym < GY and nzm >= 0 and nzm < GZ:
                    lv = light[nxm, nym, nzm]
                else:
                    lv = 15 if night == 0 else (5 if night == 1 else 9)
                own = emit[b]
                if own > lv:
                    lv = own
                br = (lv / 15.0) ** 1.4 * 0.9 + 0.10
                if own > 0:
                    br = 1.15
                shade_f = shade * br if own == 0 else br
                # distance fog
                fog = min(max((t - maxd * 0.55) / (maxd * 0.45), 0.0), 1.0)
                cr = tr * shade_f; cg = tg * shade_f; cb = tb * shade_f
                cr = cr + (sr - cr) * fog; cg = cg + (sg - cg) * fog; cb = cb + (sb - cb) * fog
                w = trans * ta
                accr += cr * w; accg += cg * w; accb += cb * w
                trans *= (1.0 - ta)
                if trans < 0.03:
                    hit_end = True
                    break
            if not hit_end and et < 1e29:
                lvx = int(ex_); lvy = int(ey_); lvz = int(ez_)
                lv = 15
                if lvx >= 0 and lvx < GX and lvy >= 0 and lvy < GY and lvz >= 0 and lvz < GZ:
                    lv = light[lvx, lvy, lvz]
                bre = (lv / 15.0) ** 1.4 * 0.9 + 0.10
                fogE = min(max((et - maxd * 0.55) / (maxd * 0.45), 0.0), 1.0)
                cr = er * bre; cg = eg * bre; cb = eb * bre
                cr = cr + (sr - cr) * fogE; cg = cg + (sg - cg) * fogE; cb = cb + (sb - cb) * fogE
                accr += cr * trans; accg += cg * trans; accb += cb * trans
                hit_end = True
            if not hit_end:
                accr += sr * trans; accg += sg * trans; accb += sb * trans
            img[py, px, 0] = accr; img[py, px, 1] = accg; img[py, px, 2] = accb
    return img


class Scene:
    def __init__(self, cx, cz, radius=190):
        self.G = load_grid(max(0, cx - radius), cx + radius, max(0, cz - radius), cz + radius)
        self.g, self.rgb, self.kind, self.emit, self.solid = prepare(self.G)
        self.light = {}
        self.ox, self.oz = self.G.x0, self.G.z0

    def ground(self, x, z):
        """Feet height standing on the highest solid block at world (x, z)."""
        gx, gz = int(x) - self.ox, int(z) - self.oz
        col = self.g[gx, :, gz]
        for y in range(self.g.shape[1] - 1, -1, -1):
            if self.solid[col[y]] == 1 or self.kind[col[y]] == WATER:
                return y + Y0 + 1
        return Y0

    def clear_spot(self, x, z, yaw=0.0, need=5, search=14):
        """Nearest standable feet position around (x, z) with open air ahead (so the camera is not inside leaves)."""
        best = None
        yr = np.radians(yaw)
        fx, fz = -np.sin(yr), np.cos(yr)
        for r in range(0, search + 1):
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if max(abs(dx), abs(dz)) != r:
                        continue
                    px, pz = int(x) + dx, int(z) + dz
                    gx, gz = px - self.ox, pz - self.oz
                    if gx < 8 or gz < 8 or gx >= self.g.shape[0] - 8 or gz >= self.g.shape[2] - 8:
                        continue
                    fy = self.ground(px, pz)
                    ok = True
                    for k in range(0, need + 1):
                        ax, az = int(px + fx * k), int(pz + fz * k)
                        for yy in (fy, fy + 1, fy + 2):
                            b = self.g[ax - self.ox, yy - Y0, az - self.oz]
                            if self.solid[b] == 1:
                                ok = False
                    if ok:
                        return px + 0.5, fy, pz + 0.5
        return x + 0.5, self.ground(x, z), z + 0.5

    def light_for(self, night):
        if night not in self.light:
            self.light[night] = compute_light(self.g, self.solid, self.emit, night)
        return self.light[night]

    def shot(self, x, y, z, yaw, pitch, w=1280, h=720, fov=70, night=0, maxd=210.0, hud=True, extra=None, ents=None, textures=()):
        """x,y,z: player feet in world coordinates. yaw: 0 = looking south (+z), 90 = west (-x) like Minecraft."""
        ex, ey, ez = x - self.ox, y + 1.62 - Y0, z - self.oz
        yr, pr = np.radians(yaw), np.radians(pitch)
        fwd = np.array([-np.sin(yr) * np.cos(pr), -np.sin(pr), np.cos(yr) * np.cos(pr)], dtype=np.float64)
        right = np.array([-np.cos(yr), 0.0, -np.sin(yr)], dtype=np.float64)
        up = np.cross(right, fwd)
        up = -up if up[1] < 0 else up
        sun = np.array([0.35, 0.8, -0.45]); sun /= np.linalg.norm(sun)
        if night == 2:
            sun = np.array([0.6, 0.05, -0.8])
        elif night:
            sun = np.array([-0.4, 0.55, 0.3]); sun /= np.linalg.norm(sun)
        tanf = np.tan(np.radians(fov) / 2)
        import entities as E
        shifted = []
        for e in (ents or []):
            e2 = dict(e); e2["x"] = e["x"] - self.ox; e2["y"] = e["y"] - Y0; e2["z"] = e["z"] - self.oz
            shifted.append(e2)
        ea = E.assemble(shifted, list(textures))
        img = render(self.g, self.light_for(night), self.rgb, self.kind, self.emit, self.solid,
                     np.array([ex, ey, ez]), fwd, right, up, tanf, w / h, w, h, maxd, night, sun[0], sun[1], sun[2], *ea)
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        if extra:
            im = extra(im, dict(eye=(ex, ey, ez), fwd=fwd, right=right, up=up, tanf=tanf, w=w, h=h))
        if hud:
            im = draw_hud(im)
        return im


def draw_hud(im):
    w, h = im.size
    d = ImageDraw.Draw(im, "RGBA")
    cx, cy = w // 2, h // 2
    d.rectangle((cx - 1, cy - 9, cx + 1, cy + 9), fill=(255, 255, 255, 190))
    d.rectangle((cx - 9, cy - 1, cx + 9, cy + 1), fill=(255, 255, 255, 190))
    # hotbar
    s = 44
    x0 = cx - 9 * s // 2
    y0 = h - s - 10
    d.rectangle((x0 - 3, y0 - 3, x0 + 9 * s + 3, y0 + s + 3), fill=(30, 30, 30, 170))
    items = [(70, 220, 230), (150, 100, 40), (200, 200, 60), (120, 120, 130), (220, 50, 50), (230, 180, 40), (80, 160, 80), (140, 60, 200), (200, 200, 200)]
    for i in range(9):
        bx = x0 + i * s
        d.rectangle((bx, y0, bx + s - 2, y0 + s - 2), outline=(255, 255, 255, 220) if i == 0 else (90, 90, 90, 220), width=3 if i == 0 else 2)
        if i < 6:
            d.rectangle((bx + 12, y0 + 12, bx + s - 14, y0 + s - 14), fill=items[i] + (255,))
    # hearts + food
    for i in range(10):
        hx = x0 + i * 18
        d.rectangle((hx, y0 - 26, hx + 14, y0 - 13), fill=(215, 30, 40, 255), outline=(60, 0, 0, 255))
        fx = x0 + 9 * s - (i + 1) * 18 + 2
        d.rectangle((fx, y0 - 26, fx + 14, y0 - 13), fill=(190, 120, 50, 255), outline=(60, 30, 0, 255))
    d.rectangle((x0, y0 - 10, x0 + 9 * s, y0 - 6), fill=(20, 20, 20, 200))
    d.rectangle((x0, y0 - 10, x0 + int(9 * s * 0.45), y0 - 6), fill=(110, 220, 60, 255))
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except Exception:
        f = ImageFont.load_default()
    d.text((10, 8), "Concept render (own renderer, not an in-game screenshot)", fill=(255, 255, 255, 200), font=f)
    return im
