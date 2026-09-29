"""Overworld terrain: heightmap, water, surface materials, colour classes, roads (numpy)."""
import zlib
import numpy as np
from scipy import ndimage
from poi_defs import *

# colour classes (terrain_raster.npy)
C_DEEP, C_SHALLOW, C_DUNE, C_CANYON, C_OASIS, C_SALT, C_MOUNT, C_ROAD, C_CITY, C_WATER, C_BEACH, C_PLAZA = range(12)
LEGEND = {0: "deep sea", 1: "shallow sea", 2: "golden dunes", 3: "red canyons", 4: "oasis / grass", 5: "salt flat",
          6: "black basalt mountain", 7: "caravan road", 8: "brass city ground", 9: "lake / pond", 10: "beach",
          11: "POI plaza"}


def ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def noise(seed, scale, shape=N):
    rng = np.random.default_rng(seed)
    g = int(shape / scale) + 4
    a = rng.standard_normal((g, g)).astype(np.float32)
    o = ndimage.zoom(a, scale, order=3)[:shape, :shape]
    return (o / 0.9).astype(np.float32)


def fbm(seed, scale, octs=3):
    t = 0
    amp = 1.0
    tot = 0
    for i in range(octs):
        t = t + noise(seed + i * 17, scale / (2 ** i)) * amp
        tot += amp
        amp *= 0.5
    return (t / tot / 0.85).astype(np.float32)


def blob(Xg, Zg, x, z, r, nz=None, wob=0.25):
    d = np.hypot(Xg - x, Zg - z) / r
    if nz is not None:
        d = d * (1 + wob * nz)
    return d


class Terrain:
    pass


def hashn(seed):
    return np.random.default_rng(seed).random((N, N), dtype=np.float32)


def apply_pad(H, kind, cx, cz, size, h0, blend):
    ext = size + blend
    x0, x1 = max(0, cx - ext), min(N, cx + ext + 1)
    z0, z1 = max(0, cz - ext), min(N, cz + ext + 1)
    dx = np.arange(x0, x1)[None, :] - cx
    dz = np.arange(z0, z1)[:, None] - cz
    d = np.maximum(np.abs(dx), np.abs(dz)) if kind == "sq" else np.hypot(dx, dz)
    w = 1 - ss(size, size + blend, d)
    sl = (slice(z0, z1), slice(x0, x1))
    H[sl] = H[sl] * (1 - w) + h0 * w


def build_terrain(log=print):
    T = Terrain()
    Zg, Xg = np.mgrid[0:N, 0:N].astype(np.float32)
    n_a = fbm(11, 700, 2)
    log("noise fields")
    # ---- dunes
    th = np.radians(28)
    warp = fbm(21, 160, 2)
    period = 62.0
    phase = (Xg * np.cos(th) + Zg * np.sin(th)) * (2 * np.pi / period) + 2.6 * warp
    d1 = (0.5 + 0.5 * np.sin(phase)) ** 1.7
    th2 = np.radians(-38)
    phase2 = (Xg * np.cos(th2) + Zg * np.sin(th2)) * (2 * np.pi / 96.0) + 2.2 * fbm(22, 130, 2)
    d2 = (0.5 + 0.5 * np.sin(phase2)) ** 2.0
    mixm = ss(-0.3, 0.3, fbm(23, 500, 2))
    d = d1 * (1 - mixm) + d2 * mixm
    del d1, d2, phase2
    env = ss(-0.6, 1.3, fbm(31, 420, 2))
    amp = 4 + 27 * env ** 1.2
    H = 70 + amp * (d - 0.32) + 1.6 * fbm(41, 26, 2)
    H = np.maximum(H, 64.0)
    del d, phase
    # ---- canyons
    cn = fbm(51, 260, 2)
    cm = np.zeros((N, N), np.float32)
    for (x, z, r) in CANYONS:
        cm = np.maximum(cm, np.exp(-(blob(Xg, Zg, x, z, r, cn, 0.35)) ** 2 * 1.6))
    cm = ss(0.30, 0.62, cm)
    ch = np.abs(fbm(61, 170, 2) + 0.35 * fbm(62, 80, 2))
    depth = 1 - ss(0.10, 0.42, ch)
    mesa = 80 + 4 * np.round(1.4 * fbm(63, 300, 1)) + 2 * fbm(64, 30, 1)
    can_h = mesa - depth * (mesa - 44) + 1.5 * fbm(65, 14, 1)
    can_h = np.maximum(can_h, 41)
    # t2 bowl: inside r<=46 flat at 70, cliffs above
    t2 = MAINBY["t2"]
    rr = np.hypot(Xg - t2["x"], Zg - t2["z"])
    can_h = np.where(rr < 130, can_h * ss(52, 95, rr) + (70 + 24 * ss(44, 66, rr)) * (1 - ss(52, 95, rr)), can_h)
    cm = np.maximum(cm, (1 - ss(120, 170, rr)))  # t2 area is all canyon
    H = H * (1 - cm) + can_h * cm
    T.cm = cm
    # ---- mountains
    mm = np.zeros((N, N), np.float32)
    mn = fbm(71, 300, 2)
    for (x, z, r, s) in MOUNTAINS:
        if r > 0:
            mm = np.maximum(mm, s * np.exp(-(blob(Xg, Zg, x, z, r, mn, 0.3)) ** 2 * 1.5))
    mm = ss(0.18, 0.75, mm)
    rid = 1 - np.abs(fbm(72, 150, 3))
    mh = 70 + 14 * mm + mm * (26 * ss(-0.6, 1.0, fbm(74, 130, 2)) + 46 * np.clip(rid, 0, 1) ** 1.4) + 5 * fbm(73, 22, 1)
    H = H * (1 - mm) + np.minimum(mh, 152) * mm
    T.mm = mm
    # ---- salt flats
    sfm = np.full((N, N), -9.0, np.float32)
    sn = fbm(81, 90, 2)
    for (x, z, rx, rz) in SALT:
        v = 1 - ((Xg - x) / rx) ** 2 - ((Zg - z) / rz) ** 2 + 0.22 * sn
        sfm = np.maximum(sfm, v)
    H = H * (1 - ss(0, 0.3, sfm)) + (66 + 0.4 * fbm(82, 60, 1)) * ss(0, 0.3, sfm)
    T.salt = sfm > 0.05
    log("base terrain done")
    # ---- lake
    lk = LAKE
    rl = np.hypot(Xg - lk["x"], Zg - lk["z"]) + 8 * fbm(91, 60, 2)
    lakem = rl < lk["r"]
    bedh = lk["bed"] + 22 * (1 - ss(lk["r"] - 34, lk["r"] + 6, rl)) * 0 + 22 * ss(lk["r"] - 34, lk["r"] + 4, rl)
    inl = rl < lk["r"] + 14
    H = np.where(inl, H * ss(lk["r"], lk["r"] + 14, rl) + bedh * (1 - ss(lk["r"], lk["r"] + 14, rl)), H)
    water = np.full((N, N), -1, np.int16)
    water[lakem] = lk["level"]
    T.lake = lakem
    # ---- ponds (oases)
    pond_all = [(x, z, r) for (x, z, r, g) in BIG_OASES] + [(x, z, r) for (x, z, r, n, g) in MINOR_OASES]
    pn = fbm(92, 25, 2)
    pondm = np.zeros((N, N), bool)
    for (x, z, r) in pond_all:
        x0, x1, z0, z1 = max(0, x - r - 8), min(N, x + r + 9), max(0, z - r - 8), min(N, z + r + 9)
        sl = (slice(z0, z1), slice(x0, x1))
        rp = np.hypot(Xg[sl] - x, Zg[sl] - z) * (1 + 0.16 * pn[sl])
        inside = rp < r
        dep = 69 - 4 * (1 - ss(0, r, rp))
        H[sl] = np.where(rp < r + 6, np.where(inside, dep - 1.0 * (rp < r * 0.6), 70 - (70 - dep) * (1 - ss(r, r + 6, rp))), H[sl])
        water[sl][inside] = 69
        pondm[sl] |= inside
    T.pond = pondm
    # ---- POI pads (flat plazas)
    for p in MAIN:
        kind, size, blend = p["pad"]
        apply_pad(H, kind, p["x"], p["z"], size, float(p["y"]), blend)
    log("pads done")
    # ---- sea
    sh = fbm(101, 200, 2)
    dw = Xg - (118 + 45 * sh)
    ds = (2300 + 40 * fbm(102, 220, 2)) - Zg
    dnw = np.hypot(Xg, Zg) - (520 + 70 * fbm(103, 260, 2))
    dsea = np.minimum(np.minimum(dw, ds), dnw)
    # smooth min
    T.dsea = dsea
    beach = 63.0 + (H - 63.0) * ss(0, 34, dsea)
    seaf = 63.0 - 34 * np.clip(-dsea / 90.0, 0, 1) ** 0.75
    H = np.where(dsea >= 0, beach, seaf)
    sea = dsea < 0
    water[(H < SEA) & (water < 0)] = SEA
    water[sea & (H >= SEA)] = -1
    # ---- lighthouse islet + shipwreck reefs handled by structure builders (need shore); add islet here
    lx, lz = 42, 1750
    ri = np.hypot(Xg - lx, Zg - lz) + 3 * fbm(104, 12, 1)
    isl = 74 * (1 - ss(6, 24, ri)) + 45 * ss(6, 24, ri)
    H = np.where(ri < 24, np.maximum(H, isl), H)
    water[(ri < 24) & (H >= SEA)] = -1
    T.lighthouse = (lx, lz)
    # ---- oasis grass masks
    grass = np.zeros((N, N), bool)
    on = fbm(111, 30, 2)
    gl = [(x, z, g) for (x, z, r, g) in BIG_OASES] + [(x, z, g) for (x, z, r, n, g) in MINOR_OASES]
    for (x, z, g) in gl:
        grass |= (np.hypot(Xg - x, Zg - z) * (1 + 0.3 * on)) < g
    grass &= (dsea > 30) & (mm < 0.3) & (cm < 0.5)
    T.grass = grass
    H = np.round(H).astype(np.int16)
    T.H = H
    T.water = water
    T.Xg, T.Zg = Xg, Zg
    return T


def carve_roads(T, log=print):
    """Roads: smoothed profile along polylines; returns road mask + centerline samples."""
    H = T.H.astype(np.float32)
    N_ = N
    best = np.full((N_, N_), 1e9, np.float32)
    rh = np.zeros((N_, N_), np.float32)
    samples = {}
    for name, pts in ROADS.items():
        # densify
        P = [np.array(p, float) for p in pts]
        seg = []
        for a, b in zip(P[:-1], P[1:]):
            L = np.hypot(*(b - a))
            k = max(2, int(L))
            t = np.linspace(0, 1, k, endpoint=False)[:, None]
            seg.append(a + (b - a) * t)
        seg.append(P[-1][None, :])
        pl = np.vstack(seg)
        # wiggle for natural look (deterministic)
        rng = np.random.default_rng(zlib.crc32(name.encode()) % 100000)
        w = ndimage.gaussian_filter1d(rng.standard_normal(len(pl)), 40) * 14
        tang = np.gradient(pl, axis=0)
        tang /= np.linalg.norm(tang, axis=1, keepdims=True) + 1e-9
        nrm = np.stack([-tang[:, 1], tang[:, 0]], 1)
        env = np.minimum(1, np.minimum(np.arange(len(pl)), np.arange(len(pl))[::-1]) / 80.0)
        pl = pl + nrm * (w * env)[:, None]
        xs = np.clip(pl[:, 0].astype(int), 0, N_ - 1)
        zs = np.clip(pl[:, 1].astype(int), 0, N_ - 1)
        prof = ndimage.gaussian_filter1d(H[zs, xs], 22, mode="nearest")
        # keep endpoints on the POI ground level
        samples[name] = (pl, prof)
        # rasterise: for each sample point stamp a disc (fast: stamp every 2 blocks)
        W_ = 2.6
        BL = 7
        for i in range(0, len(pl), 2):
            x, z = pl[i]
            x0, x1, z0, z1 = int(x) - 12, int(x) + 13, int(z) - 12, int(z) + 13
            x0, z0 = max(0, x0), max(0, z0)
            x1, z1 = min(N_, x1), min(N_, z1)
            if x0 >= x1 or z0 >= z1:
                continue
            dd = np.hypot(T.Xg[z0:z1, x0:x1] - x, T.Zg[z0:z1, x0:x1] - z)
            sl = (slice(z0, z1), slice(x0, x1))
            m = dd < best[sl]
            best[sl] = np.where(m, dd, best[sl])
            rh[sl] = np.where(m, prof[i], rh[sl])
    w = 1 - ss(W_, W_ + BL, best)
    # do not carve in sea / lake / ponds / plaza interior
    protect = (T.water >= 0)
    w = np.where(protect, 0, w)
    T.road_core = (best < W_ + 0.3) & (~protect)
    Hn = H * (1 - w) + np.round(rh) * w
    T.H = np.round(Hn).astype(np.int16)
    T.road_samples = samples
    log("roads carved")
    return T


def finalize(T, MID, log=print):
    """Surface / sub-surface / mid ids and classes.  `MID` maps names -> block ids (B)."""
    from wg_core import B
    H = T.H
    Xg, Zg = T.Xg, T.Zg
    rnd = hashn(7)
    rnd2 = hashn(8)
    gy, gx = np.gradient(H.astype(np.float32))
    slope = np.hypot(gx, gy)
    surf = np.full((N, N), B("minecraft:sand"), np.uint16)
    sub = np.full((N, N), B("minecraft:sand"), np.uint16)
    mid = np.full((N, N), B("minecraft:sandstone"), np.uint16)
    cls = np.full((N, N), C_DUNE, np.uint8)
    strat = np.zeros((N, N), bool)
    biome = np.zeros((N, N), np.uint8)   # 0 desert 1 badlands 2 oasis 3 stony_peaks 4 warm ocean 5 lukewarm 6 deep lukewarm ocean 7 beach
    cm, mm = T.cm, T.mm
    # canyon
    c = cm > 0.5
    flat = slope < 1.1
    surf[c] = np.where(flat[c], B("minecraft:red_sand"), B("minecraft:orange_terracotta"))
    sub[c] = B("minecraft:red_sand")
    mid[c] = B("minecraft:red_sandstone")
    strat |= c
    cls[c] = C_CANYON
    biome[c] = 1
    # salt
    s = T.salt & (cm < 0.5)
    pick = np.select([rnd < 0.7, rnd < 0.9], [B("minecraft:calcite"), B("minecraft:white_terracotta")], B("minecraft:diorite"))
    surf[s] = pick[s]
    sub[s] = B("minecraft:calcite")
    mid[s] = B("minecraft:sandstone")
    cls[s] = C_SALT
    strat &= ~s
    # mountains
    m = (mm > 0.3) | (H > 105)
    pickm = np.select([rnd < 0.5, rnd < 0.75, rnd < 0.9], [B("minecraft:smooth_basalt"), B("minecraft:blackstone"), B("minecraft:basalt")], B("minecraft:deepslate"))
    surf[m] = pickm[m]
    sub[m] = np.where(rnd2[m] < 0.5, B("minecraft:blackstone"), B("minecraft:smooth_basalt"))
    mid[m] = B("minecraft:stone")
    cls[m] = C_MOUNT
    biome[m] = 3
    strat &= ~m
    # oasis grass
    g = T.grass
    surf[g] = np.where(rnd[g] < 0.08, B("minecraft:coarse_dirt"), B("minecraft:grass_block[snowy=false]"))
    sub[g] = B("minecraft:dirt")
    mid[g] = B("minecraft:sandstone")
    cls[g] = C_OASIS
    biome[g] = 2
    # pond shore sand + bed
    ps = ndimage.binary_dilation(T.pond, iterations=3)
    surf[ps & ~T.pond & g] = B("minecraft:sand")
    surf[T.pond] = np.where(rnd[T.pond] < 0.3, B("minecraft:clay"), B("minecraft:sand"))
    sub[T.pond] = B("minecraft:sand")
    cls[T.pond] = C_WATER
    # lake
    L = T.lake
    surf[L] = np.select([rnd[L] < 0.5, rnd[L] < 0.8], [B("minecraft:sand"), B("minecraft:gravel")], B("minecraft:clay"))
    sub[L] = B("minecraft:sand")
    cls[L] = C_WATER
    strat &= ~L
    # sea + beach
    ds = T.dsea
    sea = ds < 0
    deep = H < 48
    sf = np.select([rnd < 0.55, rnd < 0.85], [B("minecraft:sand"), B("minecraft:gravel")], B("minecraft:clay"))
    surf[sea] = sf[sea]
    sub[sea] = B("minecraft:sand")
    mid[sea] = B("minecraft:stone")
    cls[sea] = np.where(deep[sea], C_DEEP, C_SHALLOW)
    bch = (ds >= 0) & (ds < 9)
    surf[bch] = B("minecraft:sand")
    cls[bch & (cls == C_DUNE)] = C_BEACH
    strat &= ~(sea | bch)
    biome[sea] = np.where(deep[sea], 6, 4)
    biome[bch] = 7 if False else 0
    # roads
    rc = T.road_core & ~sea
    pr = np.select([rnd2 < 0.55, rnd2 < 0.8, rnd2 < 0.92], [B("minecraft:gravel"), B("minecraft:coarse_dirt"), B("minecraft:cobblestone")], B("minecraft:dirt_path"))
    surf[rc] = pr[rc]
    sub[rc] = B("minecraft:coarse_dirt")
    cls[rc] = C_ROAD
    # pads
    for p in MAIN:
        kind, size, blend = p["pad"]
        if p["id"] == "city":
            continue
        x, z = p["x"], p["z"]
        sl = (slice(max(0, z - size), min(N, z + size + 1)), slice(max(0, x - size), min(N, x + size + 1)))
        cls[sl][cls[sl] != C_WATER] = C_PLAZA
    cx, cz = MAINBY["city"]["x"], MAINBY["city"]["z"]
    rr = np.hypot(Xg - cx, Zg - cz)
    cls[rr < 158] = C_CITY
    T.surf, T.sub, T.mid, T.cls, T.strat, T.biome = surf, sub, mid, cls, strat, biome
    return T
