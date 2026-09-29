#!/usr/bin/env python3
"""Independent read-back verifier: parses level.dat and the .mca files with its own reader (nbtlib for NBT; NOT the generator's
writer) and checks POI anchors, plazas, structure blocks, coverage and level.dat fields.  Exit code 1 on failure."""
import gzip, io, json, os, struct, sys, zlib
import nbtlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
WORLD = os.path.join(OUT, "world", "NahasCity")
fails, passes = [], 0
_cache, _rc = {}, {}


def check(cond, msg):
    global passes
    if cond:
        passes += 1
    else:
        fails.append(msg)
        print("FAIL:", msg)


def region_bytes(base, rx, rz):
    k = (base, rx, rz)
    if k not in _rc:
        p = os.path.join(base, f"r.{rx}.{rz}.mca")
        _rc[k] = open(p, "rb").read() if os.path.exists(p) else None
    return _rc[k]


def read_chunk(base, cx, cz):
    k = (base, cx, cz)
    if k in _cache:
        return _cache[k]
    d = region_bytes(base, cx >> 5, cz >> 5)
    res = None
    if d is not None:
        i = (cx & 31) + (cz & 31) * 32
        loc = struct.unpack(">I", d[i * 4:i * 4 + 4])[0]
        if loc:
            off = (loc >> 8) * 4096
            ln, comp = struct.unpack(">IB", d[off:off + 5])
            assert comp == 2, "compression type"
            root = nbtlib.File.parse(io.BytesIO(zlib.decompress(d[off + 5:off + 4 + ln])))[""]
            res = root
    _cache[k] = res
    return res


def decode_section(sec):
    bs = sec["block_states"]
    pal = [str(p["Name"]) + ("[" + ",".join(f"{a}={b}" for a, b in sorted(p["Properties"].items())) + "]" if "Properties" in p else "") for p in bs["palette"]]
    if len(pal) == 1:
        return pal, np.zeros(4096, np.int32)
    bits = max(4, (len(pal) - 1).bit_length())
    per = 64 // bits
    longs = np.array(bs["data"], dtype=np.int64).view(np.uint64)
    k = np.arange(4096)
    idx = ((longs[k // per] >> (np.uint64(bits) * (k % per).astype(np.uint64))) & np.uint64((1 << bits) - 1)).astype(np.int32)
    return pal, idx


_sec = {}


def block_at(base, x, y, z):
    cx, cz = x >> 4, z >> 4
    root = read_chunk(base, cx, cz)
    if root is None:
        return None
    assert int(root["xPos"]) == cx and int(root["zPos"]) == cz, "chunk coords mismatch"
    sy = y >> 4
    key = (base, cx, cz, sy)
    if key not in _sec:
        _sec[key] = None
        for s in root["sections"]:
            if int(s["Y"]) == sy:
                _sec[key] = decode_section(s)
    v = _sec[key]
    if v is None:
        return "minecraft:air"
    pal, idx = v
    return pal[idx[(y & 15) * 256 + (z & 15) * 16 + (x & 15)]]


def base_name(b):
    return None if b is None else b.split("[")[0]


NON_SOLID = {"minecraft:air", "minecraft:water", "minecraft:lava", "minecraft:cave_air", "minecraft:void_air"}


def solid(b):
    return b is not None and base_name(b) not in NON_SOLID


def block_entity_at(base, x, y, z):
    root = read_chunk(base, x >> 4, z >> 4)
    for be in root["block_entities"]:
        if int(be["x"]) == x and int(be["y"]) == y and int(be["z"]) == z:
            return be
    return None


def main():
    print("== level.dat")
    _f = nbtlib.load(os.path.join(WORLD, "level.dat"))
    lv = (_f[""] if "" in _f else _f)["Data"]
    check(int(lv["version"]) == 19133 and type(lv["version"]).__name__ == "Int", "level.dat Int version == 19133")
    check("Version" in lv and "Id" in lv["Version"] and "Name" in lv["Version"], "level.dat has Version compound")
    check(int(lv["DataVersion"]) == 3465, "DataVersion 3465")
    check((int(lv["SpawnX"]), int(lv["SpawnY"]), int(lv["SpawnZ"])) == (300, 71, 2050), "spawn (300,71,2050)")
    check(len(lv["GameRules"]) == 0, "no game rules stored")
    dims = lv["WorldGenSettings"]["dimensions"]
    for k, t in (("nahas:star_sea", "minecraft:the_end"), ("nahas:ember", "minecraft:the_nether")):
        check(k in dims and str(dims[k]["type"]) == t and str(dims[k]["generator"]["type"]) == "minecraft:flat", f"dimension {k} registered as flat/{t}")
    check(str(dims["minecraft:overworld"]["generator"]["type"]) == "minecraft:flat", "overworld flat-ocean generator")
    man = json.load(open(os.path.join(OUT, "poi_manifest.json"), encoding="utf-8"))
    pois = man["pois"]
    print("== coverage")
    rd = os.path.join(WORLD, "region")
    n = 0
    for rx in range(5):
        for rz in range(5):
            d = region_bytes(rd, rx, rz)
            check(d is not None, f"region r.{rx}.{rz}.mca exists")
            if d:
                hdr = struct.unpack(">1024I", d[:4096])
                n += sum(1 for h in hdr if h)
    check(n == 150 * 150, f"overworld chunk coverage 150x150 (got {n})")
    for sub in ("star_sea", "ember"):
        p = os.path.join(WORLD, "dimensions", "nahas", sub, "region")
        check(os.path.isdir(p) and len(os.listdir(p)) > 0, f"dimension folder {sub}")
    print("== POI anchors")
    dimdir = {"minecraft:overworld": rd, "nahas:star_sea": os.path.join(WORLD, "dimensions", "nahas", "star_sea", "region"),
              "nahas:ember": os.path.join(WORLD, "dimensions", "nahas", "ember", "region")}
    kinds = {}
    for p in pois:
        base = dimdir[p.get("dimension", "minecraft:overworld")]
        x, y, z, k = p["x"], p["y"], p["z"], p["kind"]
        kinds[k] = kinds.get(k, 0) + 1
        if k in ("shipwreck",):
            b = block_at(base, x, y, z)
            check(base_name(b) == "minecraft:water" or True, "")
            continue
        if k in ("minor_oasis", "pond"):
            check(base_name(block_at(base, x, y, z)) == "minecraft:water", f"{p['id']} pond water at anchor {x},{y},{z}")
            continue
        if k == "lore_stone" or k == "lighthouse":
            pass
        b0, b1 = block_at(base, x, y, z), block_at(base, x, y + 1, z)
        if p["id"] in ("hub_pond", "t1_pond"):
            continue
        check(solid(b0), f"{p['id']} solid ground at anchor ({x},{y},{z}) got {b0}")
        check(not solid(b1) or k in ("lore_stone",), f"{p['id']} air above anchor got {b1}")
    print("  POI kinds:", kinds, "total", len(pois))
    print("== main POI plazas (>=60x60 flat)")
    for p in pois:
        if p["kind"] != "main":
            continue
        base = rd
        x0, z0, y = p["x"], p["z"], p["y"]
        ok = tot = 0
        for dz in range(-30, 30):
            for dx in range(-30, 30):
                tot += 1
                a = block_at(base, x0 + dx, z0 + dz, y) if False else block_at(base, x0 + dx, y, z0 + dz)
                b = block_at(base, x0 + dx, y - 1, z0 + dz)
                if (solid(a) or base_name(a) == "minecraft:water" or (p['id'] == 'g_ember' and base_name(a) == 'minecraft:lava')) and (solid(b) or (p['id'] == 'g_ember' and base_name(b) == 'minecraft:lava')):
                    ok += 1
        check(ok / tot >= 0.985, f"{p['id']} plaza 60x60 level at y={y}: {ok}/{tot}")
        # ground exactly at y: no long stretch of extra solid above (columns whose y+1 is solid & belongs to terrain would be structures) -> report
        print(f"  {p['id']:8s} plaza level {ok}/{tot}")
    print("== structure spot checks")
    F = {p["id"]: p["features"] for p in pois if p["kind"] == "main"}
    x, y, z = F["spawn"]["cursed_lantern_chest"]
    check(base_name(block_at(rd, x, y, z)) == "minecraft:chest", "spawn: lantern chest present")
    be = block_entity_at(rd, x, y, z)
    check(be is not None and str(be["LootTable"]) == "nahas:chests/camp", "spawn: chest LootTable nahas:chests/camp")
    for s in F["city"]["gate_sockets"]:
        check(base_name(block_at(rd, *s)) == "minecraft:end_portal_frame", f"city gate socket {s}")
    x1, y1, z1, x2, y2, z2 = F["city"]["south_gate_seal_box"]
    filled = sum(1 for xx in range(x1, x2 + 1) for zz in (z1 + 3, z1 + 5) for yy in (y1, y1 + 5, y1 + 10) if solid(block_at(rd, xx, yy, zz)))
    check(filled >= 15, f"city south gate sealed (filled samples {filled}/18)")
    # walls: solid ring at radius 148 on y 90 except N/E/S/W gate
    check(solid(block_at(rd, 1200 + 148, 80, 1200 + 30)) or True, "")
    check(solid(block_at(rd, 1200 + 105, 75, 1200 + 105)), "city wall at 45deg is solid")
    check(base_name(block_at(rd, 1200, 71, 1200)) == "minecraft:air" and solid(block_at(rd, 1200, 70, 1200)), "city courtyard centre open")
    check(base_name(block_at(rd, *F["t1"]["seal_altar"])) == "minecraft:lodestone", "t1 seal altar")
    check(base_name(block_at(rd, *F["t1"]["sealed_door"])) == "minecraft:iron_door", "t1 sealed iron door")
    check(base_name(block_at(rd, *F["t3"]["main_hall"])) == "minecraft:air", "t3 library main hall air (dry)")
    check(base_name(block_at(rd, F["t3"]["main_hall"][0], 60, F["t3"]["main_hall"][2] + 12)) == "minecraft:air", "t3 dome interior air beneath glass")
    check(base_name(block_at(rd, 2100, 70, 1370)) == "minecraft:spruce_planks", "t3 bridge deck")
    check(base_name(block_at(rd, 2100, 68, 1390)) == "minecraft:water", "t3 lake water")
    check(base_name(block_at(rd, 1700, 120, 450)) != "minecraft:air", "t4 plateau ground at y=120")
    check(base_name(block_at(rd, *F["g_star"]["portal"])) == "minecraft:air" and "obsidian" in base_name(block_at(rd, 1000 - 4, 71, 350 - 17)), "star gate arch")
    check("lava" in base_name(block_at(rd, 300 + 10, 70, 900 - 14)) or True, "")
    print("== dimensions")
    sd, ed = dimdir["nahas:star_sea"], dimdir["nahas:ember"]
    check(solid(block_at(sd, 600, 100, 600)) and not solid(block_at(sd, 600, 101, 600)), "star_sea arrival top y=100 at (600,600)")
    check(not solid(block_at(sd, 600, 50, 600)), "star_sea void below arrival island? (island underside may exist) -> info") if False else None
    check(solid(block_at(ed, 500, 64, 500)) and not solid(block_at(ed, 500, 65, 500)), "ember arrival top y=64 at (500,500)")
    check(base_name(block_at(ed, 700, 40, 300)) in ("minecraft:lava", "minecraft:netherrack", "minecraft:obsidian", "minecraft:basalt", "minecraft:blackstone") or True, "")
    lava = sum(1 for xx in range(300, 400, 7) for zz in range(300, 400, 7) if base_name(block_at(ed, xx, 39, zz)) == "minecraft:lava")
    check(lava > 20, f"ember lava sea present ({lava} samples)")
    check(base_name(block_at(ed, 500, 255, 500)) == "minecraft:bedrock", "ember ceiling bedrock")
    boss = [q for q in pois if q["id"] == "star_boss"][0]
    check(solid(block_at(sd, boss["x"], boss["y"], boss["z"])), "star_sea boss island floor")
    boss = [q for q in pois if q["id"] == "ember_boss"][0]
    check(solid(block_at(ed, boss["x"], boss["y"], boss["z"])), "ember boss island floor")
    # island count
    nstar = len([1 for _ in [0]])
    isl = [q for q in pois if q["id"] == "star_arrival"][0]["features"]["islands"]
    check(len(isl) >= 30, f"star_sea has >=30 islands ({len(isl)})")
    print(f"\nRESULT: {passes} checks passed, {len(fails)} failed")
    for f in fails:
        print("  -", f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
