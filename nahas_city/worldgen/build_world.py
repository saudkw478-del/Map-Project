#!/usr/bin/env python3
"""Nahas City world generator.  Usage:  python3 build_world.py [--quick]   (writes worldgen/out/...)
--quick: only writes chunks of the POI neighbourhoods (for fast previews) instead of the full 2400x2400 area."""
import json
import multiprocessing as mp
import os
import shutil
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import anvil as A
from poi_defs import *
import terrain as TR
from wg_core import Canvas, B, CanvasIndex, Chunker, write_regions
import pois_a, pois_b, pois_city, pois_extra, dims

OUT = os.path.join(HERE, "out")
WORLD = os.path.join(OUT, "world", "NahasCity")

BIOMES = ["minecraft:desert", "minecraft:badlands", "minecraft:plains", "minecraft:stony_peaks", "minecraft:warm_ocean",
          "minecraft:lukewarm_ocean", "minecraft:deep_lukewarm_ocean", "minecraft:beach"]
G = {}


def log(*a):
    print(f"[{time.time() - G.get('t0', time.time()):6.1f}s]", *a, flush=True)


class World:
    def __init__(self, T):
        self.T = T
        self.canvases = []
        self.pois = {}
        self.order = []

    def main(self, pid):
        return MAINBY[pid]

    def canvas(self, name, x0, y0, z0, x1, y1, z1):
        x0, z0 = max(0, x0), max(0, z0)
        x1, z1 = min(N, x1), min(N, z1)
        cv = Canvas(name, x0, y0, z0, x1, y1, z1)
        self.canvases.append(cv)
        return cv

    def poi(self, pid, ar, x, y, z, kind, **extra):
        d = self.pois.setdefault(pid, {"features": {}})
        d.update(dict(id=pid, ar=ar, x=int(x), y=int(y), z=int(z), kind=kind))
        d["features"].update(extra)
        if pid not in self.order:
            self.order.append(pid)

    def feat(self, pid, **kw):
        d = self.pois.setdefault(pid, {"features": {}})
        d["features"].update(kw)


def jsonable(o):
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    return o


# -------------------------------------------------------------------- chunk assembly (overworld)

def init_static():
    G["STONE"], G["DEEP"], G["BED"] = B("minecraft:stone"), B("minecraft:deepslate"), B("minecraft:bedrock")
    G["WATER"] = B("minecraft:water")
    rng = np.random.default_rng(12)
    terr = ["minecraft:terracotta", "minecraft:orange_terracotta", "minecraft:red_terracotta", "minecraft:yellow_terracotta",
            "minecraft:brown_terracotta", "minecraft:white_terracotta", "minecraft:light_gray_terracotta", "minecraft:terracotta"]
    band = np.zeros(512, np.uint16)
    y = 0
    while y < 512:
        c = B(terr[int(rng.integers(0, len(terr)))])
        L = int(rng.integers(1, 4))
        band[y:y + L] = c
        y += L
    G["BAND"] = band


def overworld_chunk(cx, cz):
    T = G["T"]
    x0, z0 = cx * 16, cz * 16
    sl = (slice(z0, z0 + 16), slice(x0, x0 + 16))
    h = T.H[sl].astype(np.int32)[None]
    wy = T.water[sl].astype(np.int32)[None]
    yy = (np.arange(384) - 64)[:, None, None]
    shape = (384, 16, 16)
    blocks = np.zeros(shape, np.uint16)
    base = np.where(yy < 0, G["DEEP"], G["STONE"]).astype(np.uint16)
    blocks[:] = np.where(yy <= h, base, 0)
    mid = np.broadcast_to((yy >= h - 12) & (yy <= h - 4), shape)
    blocks[mid] = np.broadcast_to(T.mid[sl][None], shape)[mid]
    sub = np.broadcast_to((yy >= h - 3) & (yy < h), shape)
    blocks[sub] = np.broadcast_to(T.sub[sl][None], shape)[sub]
    top = np.broadcast_to(yy == h, shape)
    blocks[top] = np.broadcast_to(T.surf[sl][None], shape)[top]
    st = T.strat[sl]
    if st.any():
        stm = np.broadcast_to(st[None] & (yy >= h - 28) & (yy <= h), shape)
        bands = G["BAND"][np.clip(yy + 64, 0, 511)]
        blocks[stm] = np.broadcast_to(bands, shape)[stm]
        # sandy top on flat canyon floors
        flat = T.surf[sl] == B("minecraft:red_sand")
        tt = np.broadcast_to(flat[None] & (yy == h), shape)
        blocks[tt] = B("minecraft:red_sand")
    wat = np.broadcast_to((yy > h) & (yy <= wy), shape)
    blocks[wat] = G["WATER"]
    blocks[0] = G["BED"]
    bes = G["IDX"].apply(cx, cz, blocks, -64)
    b4 = T.biome[z0 + 2:z0 + 16:4, x0 + 2:x0 + 16:4]
    return G["CH"].serialize(cx, cz, blocks, BIOMES, b4, bes)


def region_job(args):
    rx, rz, chunk_filter, outdir = args
    chunks = {}
    for lz in range(32):
        for lx in range(32):
            cx, cz = rx * 32 + lx, rz * 32 + lz
            if cx >= N // 16 or cz >= N // 16:
                continue
            if chunk_filter is not None and (cx, cz) not in chunk_filter:
                continue
            chunks[(lx, lz)] = overworld_chunk(cx, cz)
    if chunks:
        A.write_region(os.path.join(outdir, f"r.{rx}.{rz}.mca"), chunks)
    return rx, rz, len(chunks)


def dim_region_job(args):
    key, rx, rz, coords, outdir = args
    gen = G["DIMGEN"][key]
    chunks = {}
    for (cx, cz) in coords:
        raw = gen(cx, cz)
        if raw is not None:
            chunks[(cx & 31, cz & 31)] = raw
    if chunks:
        A.write_region(os.path.join(outdir, f"r.{rx}.{rz}.mca"), chunks)
    return key, rx, rz, len(chunks)


# -------------------------------------------------------------------- main

def main():
    quick = "--quick" in sys.argv
    G["t0"] = time.time()
    if os.path.isdir(WORLD):
        shutil.rmtree(WORLD)
    os.makedirs(os.path.join(WORLD, "region"))
    init_static()
    T = TR.build_terrain(log)
    TR.carve_roads(T, log)
    W = World(T)
    sites = pois_extra.plan_extras(T, W)
    TR.finalize(T, None, log)
    G["T"] = T
    log("surfaces finalized; extra sites:", len(sites))
    # ---- structures
    for fn in (pois_a.build_spawn, pois_a.build_hub, pois_a.build_t1, pois_b.build_t2, pois_b.build_t3, pois_b.build_t4,
               pois_b.build_star, pois_b.build_ember, pois_city.build_city):
        t = time.time()
        fn(W)
        log(f"built {fn.__name__} ({time.time() - t:.1f}s)")
    pois_extra.build_extras(W, T, sites)
    log(f"canvases: {len(W.canvases)}; registry blocks: {len(A.__dict__.get('x', [])) or len(__import__('wg_core').R.names)}")
    # hub pond oasis (big oases) registered as POIs
    for i, (x, z, r, g) in enumerate(BIG_OASES):
        W.poi(("hub_pond", "t1_pond")[i], ("بركة واحة الدلال", "بركة معبد الواحة")[i], x, 69, z, "pond", note="y = pond water surface block")
    import connect
    log("linked fence/wall/pane connections:", connect.link(W.canvases))
    G["IDX"] = CanvasIndex(W.canvases)
    G["CH"] = Chunker(-64)
    # ---- write overworld
    regs = [(rx, rz) for rx in range(5) for rz in range(5)]
    filt = None
    if quick:
        filt = set()
        for p in W.pois.values():
            for dx in range(-6, 7):
                for dz in range(-6, 7):
                    filt.add(((p["x"] >> 4) + dx, (p["z"] >> 4) + dz))
        for cv in W.canvases:
            for cx in range(cv.x0 >> 4, ((cv.x1 - 1) >> 4) + 1):
                for cz in range(cv.z0 >> 4, ((cv.z1 - 1) >> 4) + 1):
                    filt.add((cx, cz))
    # dimensions
    log("building dimensions")
    S = dims.build_star_sea(log)
    Em = dims.build_ember(log)
    connect.link(S.canvases + Em.canvases)
    sgen, scoords = dims.assemble_star(S)
    egen, ecoords = dims.assemble_ember(Em)
    G["DIMGEN"] = {"star": sgen, "ember": egen}
    star_dir = os.path.join(WORLD, "dimensions", "nahas", "star_sea", "region")
    ember_dir = os.path.join(WORLD, "dimensions", "nahas", "ember", "region")
    os.makedirs(star_dir, exist_ok=True); os.makedirs(ember_dir, exist_ok=True)
    jobs = [(rx, rz, filt, os.path.join(WORLD, "region")) for rx, rz in regs]
    djobs = []
    for key, coords, d in (("star", scoords, star_dir), ("ember", ecoords, ember_dir)):
        byreg = {}
        for c in coords:
            byreg.setdefault((c[0] >> 5, c[1] >> 5), []).append(c)
        for (rx, rz), cs in byreg.items():
            djobs.append((key, rx, rz, cs, d))
    ctx = mp.get_context("fork")
    with ctx.Pool(4) as pool:
        for r in pool.imap_unordered(region_job, jobs):
            log("overworld region", r)
        for r in pool.imap_unordered(dim_region_job, djobs):
            log("dimension region", r)
    # ---- level.dat
    flat_void = lambda biome: {"type": "minecraft:flat", "settings": A.flat_settings(biome, [("minecraft:air", 1)])}
    A.write_level_dat(os.path.join(WORLD, "level.dat"), "NahasCity", SPAWN, 40, SEA, seed=20260929,
                      extra_dims={"nahas:star_sea": {"type": "minecraft:the_end", "generator": flat_void("minecraft:the_end")},
                                  "nahas:ember": {"type": "minecraft:the_nether", "generator": flat_void("minecraft:nether_wastes")}})
    os.makedirs(os.path.join(WORLD, "datapacks"), exist_ok=True)
    # ---- exports
    export(W, T, S, Em)
    log("done")


def export(W, T, S, Em):
    rows = []
    for pid in W.order:
        d = W.pois[pid]
        d = dict(d)
        d["dimension"] = d.get("features", {}).get("dimension") if False else "minecraft:overworld"
        rows.append(jsonable(d))
    for D in (S, Em):
        for d in D.pois:
            r = dict(d)
            r["features"] = jsonable({k: v for k, v in D.feats.items()})
            rows.append(jsonable(r))
    # sanity: main POI anchors must equal SPEC
    for p in MAIN:
        r = next(x for x in rows if x["id"] == p["id"])
        assert (r["x"], r["y"], r["z"]) == (p["x"], p["y"], p["z"]), (p, r)
    man = {"world": "NahasCity", "spawn": list(SPAWN), "note": "coordinates are block coordinates; y = ground top solid block; first air block is y+1",
           "pois": rows}
    with open(os.path.join(OUT, "poi_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    np.save(os.path.join(OUT, "terrain_raster.npy"), T.cls.astype(np.uint8))
    with open(os.path.join(OUT, "terrain_legend.json"), "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in TR.LEGEND.items()}, f, indent=1)
    np.save(os.path.join(OUT, "heightmap_u8.npy"), np.clip(T.H.astype(np.int32) - 20, 0, 255).astype(np.uint8))
    import mapimg
    mapimg.make_map(T, rows, os.path.join(OUT, "world_map.png"))


if __name__ == "__main__":
    main()
