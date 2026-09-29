"""The two extra dimensions: nahas:star_sea (the_end type, floating islands) and nahas:ember (the_nether type, lava sea)."""
import numpy as np
from wg_core import Canvas, B, CanvasIndex, Chunker
from shapes import *
import terrain as TR
from pois_a import scatter

MIN_Y = 0
HEIGHT = 256


class DimWorld:
    def __init__(self, name):
        self.name = name
        self.canvases = []
        self.pois = []
        self.feats = {}

    def canvas(self, name, x0, y0, z0, x1, y1, z1):
        cv = Canvas(name, x0, max(0, y0), z0, x1, min(256, y1), z1)
        self.canvases.append(cv)
        return cv


# ====================================================================== star sea

END_SURF = ["minecraft:end_stone", "minecraft:calcite", "minecraft:light_blue_terracotta", "minecraft:amethyst_block", "minecraft:end_stone_bricks"]


def island(cv, cx, cz, top, r, rnd, decor=True, kind="path"):
    nz = np.random.default_rng(int(cx * 7 + cz * 13)).random((5, 5))
    rr = int(r * 1.25) + 2
    for dz in range(-rr, rr + 1):
        for dx in range(-rr, rr + 1):
            ang = np.arctan2(dz, dx)
            wob = 1 + 0.10 * np.sin(3 * ang + cx) + 0.06 * np.sin(5 * ang + cz)
            d = np.hypot(dx, dz) / (r * wob)
            if d >= 1:
                continue
            depth = int(2 + r * 1.3 * (1 - d) ** 1.4)
            x, z = cx + dx, cz + dz
            rv = rnd.random()
            surf = END_SURF[0] if rv < 0.72 else (END_SURF[1] if rv < 0.82 else (END_SURF[2] if rv < 0.9 else (END_SURF[4] if rv < 0.97 else END_SURF[3])))
            cv.set(x, top, z, surf)
            for k in range(1, depth + 1):
                cv.set(x, top - k, z, "minecraft:end_stone" if k < depth - 1 else ("minecraft:obsidian" if rnd.random() < 0.3 else "minecraft:end_stone"))
    if decor:
        for _ in range(int(r * 0.6)):
            a = rnd.random() * 2 * np.pi
            d = rnd.random() * (r - 2)
            x, z = int(cx + d * np.cos(a)), int(cz + d * np.sin(a))
            v = rnd.random()
            if v < 0.45:
                cv.set(x, top + 1, z, "minecraft:amethyst_cluster[facing=up]")
            elif v < 0.7:
                cv.fill(x, top + 1, z, x, top + 1 + int(rnd.integers(1, 4)), z, "minecraft:purpur_pillar[axis=y]")
                cv.set(x, top + 5, z, "minecraft:end_rod[facing=up]") if False else None
            elif v < 0.8:
                cv.set(x, top, z, "minecraft:sea_lantern")


def portal_arch(cv, x, y, z, mat="minecraft:obsidian", trim="minecraft:crying_obsidian", w=3, h=8, glass="minecraft:light_blue_stained_glass"):
    """Arch in the x-direction plane (facing south) at (x, z); y = floor top."""
    for dx in (-w - 1, w + 1):
        cv.fill(x + dx, y + 1, z, x + dx, y + h, z, mat)
    cv.fill(x - w - 1, y + h + 1, z, x + w + 1, y + h + 1, z, mat)
    cv.fill(x - w, y + 1, z, x + w, y + h, z, "air")
    cv.fill(x - w, y + 1, z + 1, x + w, y + h, z + 1, glass) if glass else None
    for yy in (y + 2, y + 5):
        cv.set(x - w - 1, yy, z + 1, trim); cv.set(x + w + 1, yy, z + 1, trim)
    cv.set(x - w, y + h, z, trim); cv.set(x + w, y + h, z, trim)


def build_star_sea(log=print):
    D = DimWorld("star_sea")
    rnd = np.random.default_rng(2024)
    C = (600, 600)
    islands = []   # (x,z,top,r,kind)
    # arrival island r=32 top 100
    islands.append((600, 600, 100, 32, "arrival"))
    # hop path: random walk with 27 islands
    x, z, top, r = 600.0, 600.0, 100, 32.0
    heading = np.radians(200)
    n_hop = 27
    tries = 0
    while len(islands) - 1 < n_hop and tries < 5000:
        tries += 1
        h2 = heading + np.radians(rnd.uniform(-38, 38))
        r2 = float(rnd.integers(6, 11))
        step = r + r2 + rnd.uniform(1.8, 3.2)
        nx_, nz_ = x + step * np.cos(h2), z + step * np.sin(h2)
        if np.hypot(nx_ - C[0], nz_ - C[1]) > 330 or nx_ < 60 or nz_ < 60 or nx_ > 1140 or nz_ > 1140:
            heading += np.radians(25)
            continue
        if any(np.hypot(nx_ - ix, nz_ - iz) < r2 + ir + 9 for (ix, iz, it, ir, ik) in islands[:-1]):
            continue
        heading = h2
        top2 = int(np.clip(top + rnd.choice([-2, -1, 0, 0, 1, 1, 2]), 90, 112))
        islands.append((int(nx_), int(nz_), top2, int(r2), "hop"))
        x, z, top, r = nx_, nz_, top2, r2
    # boss island
    while True:
        h2 = heading + np.radians(rnd.uniform(-20, 20))
        bx, bz = x + (r + 45 + 3) * np.cos(h2), z + (r + 45 + 3) * np.sin(h2)
        if 200 < bx < 1000 and 200 < bz < 1000 and all(np.hypot(bx - ix, bz - iz) > 45 + ir + 6 for (ix, iz, it, ir, ik) in islands[:-1]):
            break
        heading += np.radians(30)
    islands.append((int(bx), int(bz), top, 45, "boss"))
    # decorative outer islands (harder-to-reach extras)
    dec = 0
    while dec < 16:
        a = rnd.uniform(0, 2 * np.pi)
        d = rnd.uniform(200, 540)
        ix, iz = int(600 + d * np.cos(a)), int(600 + d * np.sin(a))
        rr_ = int(rnd.integers(5, 14))
        if all(np.hypot(ix - jx, iz - jz) > rr_ + jr + 18 for (jx, jz, jt, jr, jk) in islands) and 40 < ix < 1160 and 40 < iz < 1160:
            islands.append((ix, iz, int(rnd.integers(75, 135)), rr_, "outer"))
            dec += 1
    log(f"star_sea islands: {len(islands)}")
    feats = []
    for k, (ix, iz, it, ir, kind) in enumerate(islands):
        m = int(ir * 1.4) + 4
        cv = D.canvas(f"star_{k}", ix - m, it - int(ir * 1.5) - 8, iz - m, ix + m + 1, it + 26, iz + m + 1)
        lrnd = np.random.default_rng(k + 5)
        island(cv, ix, iz, it, ir, lrnd, decor=(kind != "arrival"), kind=kind)
        if kind == "arrival":
            # flat platform r=30: star inlay, return portal arch north, obelisks, sign
            for dz in range(-30, 31):
                for dx in range(-30, 31):
                    d = np.hypot(dx, dz)
                    if d <= 30 and (dx or dz):
                        ang = np.arctan2(dz, dx)
                        b = "minecraft:end_stone_bricks" if (dx + dz) % 2 else "minecraft:end_stone"
                        if d < 12 and d <= 3 + 9 * abs(np.cos(4 * ang)) ** 3:
                            b = "minecraft:purple_concrete" if d > 5 else "minecraft:light_blue_concrete"
                        elif 27 <= d < 29:
                            b = "minecraft:purpur_block"
                        cv.set(ix + dx, it, iz + dz, b)
            portal_arch(cv, ix, it, iz - 17)
            for kk in range(6):
                a = kk * np.pi / 3
                px, pz = int(ix + 24 * np.cos(a)), int(iz + 24 * np.sin(a))
                if abs(pz - (iz - 17)) < 5:
                    continue
                cv.fill(px, it + 1, pz, px, it + 6, pz, "minecraft:purpur_pillar[axis=y]")
                cv.set(px, it + 7, pz, "minecraft:sea_lantern")
            cv.sign(ix + 3, it + 1, iz + 4, ["بحر النجوم", "اقفز بين الجزر", "", ""], "south", wall=False, mat="warped")
            D.feats["arrival"] = dict(pos=(ix, it, iz), return_portal=(ix, it + 1, iz - 17), portal_interior=[(ix - 3, it + 1, iz - 17), (ix + 3, it + 8, iz - 17)])
        elif kind == "boss":
            for dz in range(-45, 46):
                for dx in range(-45, 46):
                    d = np.hypot(dx, dz)
                    if d < 34:
                        b = "minecraft:end_stone_bricks" if (dx + dz) % 2 else "minecraft:purpur_block"
                        if 27 <= d < 30:
                            b = "minecraft:light_blue_terracotta"
                        elif d < 8:
                            b = "minecraft:amethyst_block" if d > 3 else "minecraft:sea_lantern"
                        cv.set(ix + dx, it, iz + dz, b)
                        if d < 30:
                            for kk in range(1, 5):
                                cv.set(ix + dx, it + kk, iz + dz, "air")
            for kk in range(12):
                a = kk * np.pi / 6
                px, pz = int(round(ix + 31 * np.cos(a))), int(round(iz + 31 * np.sin(a)))
                cv.fill(px, it + 1, pz, px, it + 9 + (kk % 3) * 2, pz, "minecraft:purpur_pillar[axis=y]")
                cv.set(px, it + 10 + (kk % 3) * 2, pz, "minecraft:end_rod[facing=up]")
            cv.chest(ix, it + 1, iz - 20, "south", "nahas:chests/boss")
            D.feats["boss"] = dict(center=(ix, it + 1, iz), radius=30, chest=(ix, it + 1, iz - 20))
        elif kind == "outer" and lrnd.random() < 0.6:
            cv.chest(ix, it + 1, iz, "south", "nahas:chests/rare")
            feats.append(("chest", (ix, it + 1, iz)))
        if kind == "hop" and k % 6 == 0:
            cv.set(ix, it + 1, iz, "minecraft:soul_lantern[hanging=false]")
    D.feats["islands"] = [dict(x=i[0], z=i[1], top=i[2], r=i[3], kind=i[4]) for i in islands]
    D.feats["outer_chests"] = [f[1] for f in feats]
    D.pois.append(dict(id="star_arrival", ar="جزيرة الوصول", x=600, y=100, z=600, kind="dimension_arrival", dimension="nahas:star_sea"))
    bi = D.feats["boss"]["center"]
    D.pois.append(dict(id="star_boss", ar="عرش ملكة النجوم", x=bi[0], y=bi[1] - 1, z=bi[2], kind="dimension_boss", dimension="nahas:star_sea"))
    return D


def assemble_star(D):
    idx = CanvasIndex(D.canvases)
    chunker = Chunker(MIN_Y)
    biomes = ["minecraft:the_end", "minecraft:small_end_islands"]

    def gen(cx, cz):
        if (cx, cz) not in idx.map:
            return None
        blocks = np.zeros((HEIGHT, 16, 16), np.uint16)
        bes = idx.apply(cx, cz, blocks, MIN_Y)
        if blocks.max() == 0:
            return None
        return chunker.serialize(cx, cz, blocks, biomes, np.zeros((4, 4), np.uint8), bes)
    return gen, sorted(idx.map.keys())


# ====================================================================== ember

E = 1008


def build_ember(log=print):
    D = DimWorld("ember")
    rnd = np.random.default_rng(77)
    Zg, Xg = np.mgrid[0:E, 0:E].astype(np.float32)
    n1 = TR.fbm(301, 120, 2)[:E, :E] if False else None
    def nz(seed, sc, octs=2):
        t = 0; amp = 1.0; tot = 0
        for i in range(octs):
            t = t + TR.noise(seed + 17 * i, sc / (2 ** i), E) * amp; tot += amp; amp *= 0.5
        return (t / tot / 0.85).astype(np.float32)
    n1 = nz(301, 120)
    dune = nz(302, 40)
    d1 = np.hypot(Xg - 500, Zg - 500) * (1 + 0.22 * n1)
    land1 = 1 - TR.ss(120, 178, d1)
    H = 40 + land1 * (26 + 6 * dune + 5 * nz(303, 18, 1))
    H = np.where(land1 > 0.02, np.maximum(H, 41), 35 + 5 * nz(304, 60, 1))     # sea floor ~30-40 => lava bed
    # arrival plateau r=46 at y=64
    dd = np.hypot(Xg - 500, Zg - 500)
    w = 1 - TR.ss(46, 74, dd)
    H = H * (1 - w) + 64 * w
    # rest islands and boss island
    boss = (860, 250)
    extra_isl = [(700, 700, 22, 60), (250, 720, 24, 60), (330, 250, 20, 61), (650, 130, 26, 62), (880, 560, 20, 62)]
    for (ix, iz, ir, ih) in extra_isl:
        d = np.hypot(Xg - ix, Zg - iz) * (1 + 0.2 * n1)
        wgt = 1 - TR.ss(ir, ir + 14, d)
        H = np.where(wgt > 0, H * (1 - wgt) + ih * wgt, H)
    dB = np.hypot(Xg - boss[0], Zg - boss[1]) * (1 + 0.15 * n1)
    wB = 1 - TR.ss(38, 62, dB)
    H = H * (1 - wB) + 66 * wB
    # border cliff
    edge = np.minimum(np.minimum(Xg, E - 1 - Xg), np.minimum(Zg, E - 1 - Zg))
    cl = 1 - TR.ss(2, 26, edge)
    H = H * (1 - cl) + (150 + 10 * n1) * cl
    H = np.round(H).astype(np.int16)
    # ceiling bottom
    ceil = (176 + 8 * nz(305, 90, 2) - 30 * cl).astype(np.int16)
    D.H, D.ceil = H, ceil
    log("ember terrain done")
    # surfaces (ids)
    r1 = np.random.default_rng(5).random((E, E), dtype=np.float32)
    surf = np.select([r1 < 0.6, r1 < 0.8, r1 < 0.9, r1 < 0.93], [B("minecraft:red_sand"), B("minecraft:netherrack"), B("minecraft:blackstone"), B("minecraft:magma_block")], B("minecraft:red_sand")).astype(np.uint16)
    high = H >= 100
    surf[high] = np.where(r1[high] < 0.5, B("minecraft:basalt[axis=y]"), B("minecraft:blackstone"))
    low = H < 41
    surf[low] = np.where(r1[low] < 0.6, B("minecraft:netherrack"), B("minecraft:blackstone"))
    D.surf = surf
    # canvases: arrival shrine, parkour pillars, boss arena, decorations
    cv = D.canvas("ember_arrival", 500 - 50, 40, 500 - 50, 500 + 51, 100, 500 + 51)
    for dz in range(-44, 45):
        for dx in range(-44, 45):
            d = np.hypot(dx, dz)
            if d <= 44 and (dx or dz):
                b = "minecraft:polished_blackstone_bricks" if (dx + dz) % 2 else "minecraft:polished_blackstone"
                if 40 <= d < 43:
                    b = "minecraft:nether_bricks"
                elif d < 8:
                    b = "minecraft:red_nether_bricks" if d > 4 else "minecraft:gold_block"
                cv.set(500 + dx, 64, 500 + dz, b)
    portal_arch(cv, 500, 64, 500 - 20, "minecraft:crying_obsidian", "minecraft:obsidian", 3, 8, "minecraft:red_stained_glass")
    for k in range(8):
        a = k * np.pi / 4 + 0.39
        px, pz = int(round(500 + 32 * np.cos(a))), int(round(500 + 32 * np.sin(a)))
        cv.fill(px, 65, pz, px, 69, pz, "minecraft:polished_blackstone_bricks")
        cv.set(px, 70, pz, "minecraft:soul_campfire[lit=true,facing=north]")
    cv.sign(503, 65, 505, ["أرض الجمر", "احذر الحمم", "", ""], "south", wall=False, mat="crimson")
    D.feats["arrival"] = dict(pos=(500, 64, 500), return_portal=(500, 65, 480), portal_interior=[(497, 65, 480), (503, 72, 480)])
    # parkour: random walk of pillars from arrival edge to boss island edge
    pillars = []
    x, z = 500 + 62, 500 - 30   # start on arrival island rim toward boss (NE)
    tgt = np.array(boss, float)
    top = 63
    cur = np.array([x, z], float)
    cvp = D.canvas("ember_parkour", 400, 30, 100, 960, 110, 640)
    k = 0
    while np.hypot(*(tgt - cur)) > 62 and k < 400:
        k += 1
        v = tgt - cur
        ang = np.arctan2(v[1], v[0]) + np.radians(rnd.uniform(-40, 40))
        step = rnd.uniform(4.0, 5.6)
        nxt = cur + step * np.array([np.cos(ang), np.sin(ang)])
        if not (30 < nxt[0] < E - 30 and 30 < nxt[1] < E - 30):
            continue
        # skip if over solid land (path only across lava)
        px, pz = int(nxt[0]), int(nxt[1])
        top = int(np.clip(top + rnd.choice([-1, 0, 0, 1, 1]), 60, 70))
        big = rnd.random() < 0.6
        mat = "minecraft:obsidian" if big else "minecraft:basalt[axis=y]"
        if D.H[pz, px] < top - 1:
            s = 2 if big else 1
            for a_ in range(s):
                for b_ in range(s):
                    cvp.fill(px + a_, int(D.H[pz, px]) + 1, pz + b_, px + a_, top, pz + b_, mat if a_ + b_ < 2 else mat)
            pillars.append((px, top + 1, pz))
        cur = nxt
        if k % 14 == 0:
            # rest platform
            for a_ in range(-3, 4):
                for b_ in range(-3, 4):
                    if a_ * a_ + b_ * b_ <= 10:
                        cvp.fill(px + a_, int(D.H[pz, px]) + 1, pz + b_, px + a_, top, pz + b_, "minecraft:blackstone")
            cvp.set(px, top + 1, pz, "minecraft:soul_campfire[lit=true,facing=north]")
            cvp.chest(px + 1, top + 1, pz, "south", "nahas:chests/rare") if k % 28 == 0 else None
    D.feats["pillars"] = pillars
    D.feats["parkour_start"] = pillars[0] if pillars else None
    # boss arena
    bx, bz = boss
    cvb = D.canvas("ember_boss", bx - 50, 40, bz - 50, bx + 51, 110, bz + 51)
    for dz in range(-40, 41):
        for dx in range(-40, 41):
            d = np.hypot(dx, dz)
            if d <= 33:
                b = "minecraft:polished_blackstone_bricks" if (dx + dz) % 2 else "minecraft:basalt[axis=y]"
                if 28 <= d < 31:
                    b = "minecraft:obsidian"
                elif d < 6:
                    b = "minecraft:magma_block" if d > 2.5 else "minecraft:crying_obsidian"
                cvb.set(bx + dx, 66, bz + dz, b)
                for kk in range(67, 76):
                    cvb.set(bx + dx, kk, bz + dz, "air")
    for k in range(10):
        a = k * np.pi / 5
        px, pz = int(round(bx + 30 * np.cos(a))), int(round(bz + 30 * np.sin(a)))
        cvb.fill(px, 67, pz, px, 72 + (k % 3) * 2, pz, "minecraft:obsidian")
        cvb.set(px, 73 + (k % 3) * 2, pz, "minecraft:campfire[lit=true,facing=north]")
    cvb.chest(bx, 67, bz - 26, "south", "nahas:chests/boss")
    D.feats["boss"] = dict(center=(bx, 67, bz), radius=30, chest=(bx, 67, bz - 26))
    # rest islands: lanterns + chests
    for i, (ix, iz, ir, ih) in enumerate(extra_isl):
        cvi = D.canvas(f"ember_isl_{i}", ix - 20, 50, iz - 20, ix + 21, 90, iz + 21)
        cvi.fill(ix - 1, ih + 1, iz - 1, ix + 1, ih + 1, iz + 1, "minecraft:polished_blackstone_bricks")
        cvi.set(ix, ih + 2, iz, "minecraft:soul_campfire[lit=true,facing=north]")
        cvi.chest(ix + 3, ih + 1, iz + 2, "south", "nahas:chests/rare" if i % 2 == 0 else "nahas:chests/common")
    # obsidian spires with glowstone caps
    for (x, z) in scatter(rnd, 500, 500, 210, 420, 14, sep=40):
        if 40 < x < E - 40 and 40 < z < E - 40 and D.H[z, x] < 45:
            cs = D.canvas(f"spire_{x}_{z}", x - 3, 30, z - 3, x + 4, 130, z + 4)
            hh = int(rnd.integers(30, 80))
            cs.fill(x - 1, 35, z - 1, x + 1, 35 + hh, z + 1, "minecraft:obsidian")
            cs.fill(x, 36 + hh, z, x, 38 + hh, z, "minecraft:glowstone")
    D.pois.append(dict(id="ember_arrival", ar="منصة الوصول (أرض الجمر)", x=500, y=64, z=500, kind="dimension_arrival", dimension="nahas:ember"))
    D.pois.append(dict(id="ember_boss", ar="ساحة عملاق الجمر", x=bx, y=66, z=bz, kind="dimension_boss", dimension="nahas:ember"))
    return D


def assemble_ember(D):
    idx = CanvasIndex(D.canvases)
    chunker = Chunker(MIN_Y)
    biomes = ["minecraft:nether_wastes", "minecraft:basalt_deltas"]
    NR, LAV, BED, BLK, GLOW = B("minecraft:netherrack"), B("minecraft:lava"), B("minecraft:bedrock"), B("minecraft:blackstone"), B("minecraft:glowstone")
    yy = np.arange(HEIGHT)[:, None, None]
    rr = np.random.default_rng(3).random((E, E), dtype=np.float32)

    def gen(cx, cz):
        x0, z0 = cx * 16, cz * 16
        h = D.H[z0:z0 + 16, x0:x0 + 16][None].astype(np.int32)
        c = D.ceil[z0:z0 + 16, x0:x0 + 16][None].astype(np.int32)
        sf = D.surf[z0:z0 + 16, x0:x0 + 16][None]
        blocks = np.zeros((HEIGHT, 16, 16), np.uint16)
        solid = yy <= h
        blocks[np.broadcast_to(solid, blocks.shape)] = NR
        top = np.broadcast_to(yy == h, blocks.shape)
        blocks[top] = np.broadcast_to(sf, blocks.shape)[top]
        sub = np.broadcast_to((yy >= h - 3) & (yy < h) & (h >= 41), blocks.shape)
        blocks[sub] = BLK if False else NR
        lava = np.broadcast_to((yy > h) & (yy <= 40), blocks.shape)
        blocks[lava] = LAV
        ceil = np.broadcast_to(yy >= c, blocks.shape)
        blocks[ceil] = NR
        # stalactites
        r = rr[z0:z0 + 16, x0:x0 + 16][None]
        stal = np.broadcast_to((r < 0.02) & (yy >= c - 10) & (yy < c), blocks.shape)
        blocks[stal] = NR
        gl = np.broadcast_to((r > 0.985) & (yy >= c - 3) & (yy < c), blocks.shape)
        blocks[gl] = GLOW
        blocks[HEIGHT - 1] = BED
        blocks[0:3] = BED
        bes = idx.apply(cx, cz, blocks, MIN_Y)
        b4 = np.zeros((4, 4), np.uint8)
        if D.H[min(z0 + 8, E - 1), min(x0 + 8, E - 1)] >= 100:
            b4[:] = 1
        return chunker.serialize(cx, cz, blocks, biomes, b4, bes)
    return gen, [(cx, cz) for cx in range(0, E // 16) for cz in range(0, E // 16)]
