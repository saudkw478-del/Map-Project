"""Main POIs part A: spawn camp, hub oasis village, oasis temple."""
import numpy as np
from wg_core import Canvas, B
from shapes import *


def scatter(rnd, cx, cz, rmin, rmax, n, sep=6, taken=None, tries=400):
    taken = taken if taken is not None else []
    out = []
    for _ in range(tries):
        if len(out) >= n:
            break
        a = rnd.random() * 2 * np.pi
        r = rmin + rnd.random() * (rmax - rmin)
        x, z = int(cx + r * np.cos(a)), int(cz + r * np.sin(a))
        if all((x - tx) ** 2 + (z - tz) ** 2 >= sep * sep for tx, tz in taken + out):
            out.append((x, z))
    return out


def build_spawn(W):
    p = W.main("spawn")
    ax, az, y = p["x"], p["z"], p["y"]
    cv = W.canvas("spawn", ax - 44, y - 6, az - 44, ax + 45, y + 30, az + 45)
    rnd = np.random.default_rng(1)
    # trampled ground
    for dz in range(-30, 31):
        for dx in range(-30, 31):
            d = np.hypot(dx, dz)
            if d < 12 and (dx or dz):
                cv.set(ax + dx, y, az + dz, ["minecraft:coarse_dirt", "minecraft:gravel", "minecraft:sand", "minecraft:packed_mud"][int(rnd.integers(0, 4))])
            elif d < 30 and rnd.random() < 0.08:
                cv.set(ax + dx, y, az + dz, "minecraft:coarse_dirt")
    # central fire pit (burnt out) offset east of anchor
    fx, fz = ax + 7, az + 3
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if max(abs(dx), abs(dz)) == 2 and rnd.random() < 0.85:
                cv.set(fx + dx, y + 1, fz + dz, "minecraft:cobblestone")
    cv.set(fx, y, fz, "minecraft:magma_block")
    cv.set(fx, y + 1, fz, "minecraft:campfire[lit=false,facing=north]")
    for (dx, dz) in ((-3, 0), (3, 0), (0, -3), (0, 3)):
        cv.set(fx + dx, y + 1, fz + dz, slab("oak"))
    # cursed lantern altar north of the anchor
    lx, lz = ax, az - 14
    cv.fill(lx - 2, y, lz - 2, lx + 2, y, lz + 2, "minecraft:smooth_sandstone")
    cv.fill(lx - 1, y + 1, lz - 1, lx + 1, y + 1, lz + 1, "minecraft:cut_sandstone")
    cv.chest(lx, y + 2, lz, "south", "nahas:chests/camp")
    cv.set(lx - 1, y + 2, lz, "minecraft:soul_lantern[hanging=false]")
    cv.set(lx + 1, y + 2, lz, "minecraft:soul_lantern[hanging=false]")
    for (dx, dz) in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
        cv.fill(lx + dx, y + 1, lz + dz, lx + dx, y + 4, lz + dz, "minecraft:cut_sandstone_wall" if False else "minecraft:sandstone_wall")
    cv.set(lx, y + 3, lz, "air")
    cv.sign(lx, y + 2, lz + 2, ["الفانوس", "الملعون", "لا تلمسه", "إلا مع الجميع"], "south", wall=False)
    W.feat("spawn", cursed_lantern_chest=(lx, y + 2, lz), altar=(lx, y + 1, lz))
    # burned & ragged tents
    taken = [(ax, az), (fx, fz), (lx, lz)]
    cols = ["red", "orange", "brown", "yellow", "white", "red"]
    pos = scatter(rnd, ax, az, 16, 30, 7, sep=13, taken=taken)
    for i, (x, z) in enumerate(pos):
        tent(cv, x, y, z, 7, 7, cols[i % len(cols)], burned=(i % 3 != 2), rnd=rnd)
        if i % 3 == 2:
            cv.chest(x + 1, y + 1, z, "south", "nahas:chests/camp")
            W.feat("spawn", **{f"tent_chest_{i}": (x + 1, y + 1, z)})
    taken += pos
    # camel skeletons
    for (x, z) in scatter(rnd, ax, az, 12, 32, 4, sep=10, taken=taken):
        skeleton_camel(cv, x, y, z, "x" if rnd.random() < 0.5 else "z", rnd)
        taken.append((x, z))
    # broken wagons
    for (x, z) in scatter(rnd, ax, az, 14, 28, 2, sep=14, taken=taken):
        cv.fill(x - 3, y + 1, z - 1, x + 3, y + 1, z + 1, "minecraft:spruce_planks")
        for xx in (x - 3, x + 3):
            cv.fill(xx, y + 2, z - 1, xx, y + 3, z - 1, "minecraft:spruce_fence")
        cv.fill(x - 2, y + 2, z - 1, x + 2, y + 2, z - 1, "minecraft:spruce_trapdoor[facing=south,half=bottom,open=true]") if False else None
        cv.set(x - 2, y + 2, z + 1, "minecraft:barrel[facing=up]")
        cv.set(x + 3, y, z + 2, "minecraft:spruce_trapdoor[facing=south,half=bottom,open=false]") if False else None
        cv.fill(x - 3, y + 1, z + 2, x - 3, y + 2, z + 2, "minecraft:dark_oak_fence")   # wheel spokes
        cv.set(x + 3, y + 1, z + 2, "minecraft:dark_oak_fence")
        taken.append((x, z))
    # crates / barrels
    for (x, z) in scatter(rnd, ax, az, 6, 30, 9, sep=4, taken=taken):
        if rnd.random() < 0.5:
            cv.barrel(x, y + 1, z, "nahas:chests/camp")
        else:
            cv.set(x, y + 1, z, "minecraft:barrel[facing=up]")
            cv.set(x, y + 2, z, "minecraft:barrel[facing=up]") if rnd.random() < 0.4 else None
    # cacti / dead bushes / drifted sand
    for (x, z) in scatter(rnd, ax, az, 20, 38, 12, sep=5, taken=taken):
        if rnd.random() < 0.5:
            cactus(cv, x, y, z, int(rnd.integers(1, 4)))
        else:
            cv.set(x, y + 1, z, "minecraft:dead_bush")
    # signpost toward hub (north-east)
    sx, sz = ax + 22, az - 22
    cv.fill(sx, y + 1, sz, sx, y + 3, sz, "minecraft:oak_fence")
    cv.sign(sx, y + 3, sz + 1, ["إلى واحة", "الدلال", "->", "شمال شرق"], "south", wall=True)
    lamp_post(cv, ax + 3, y, az + 3, 3)
    # entrance banners (burnt poles)
    for (x, z) in ((ax - 4, az + 30), (ax + 4, az + 30)):
        cv.fill(x, y + 1, z, x, y + 6, z, "minecraft:stripped_dark_oak_log[axis=y]")
    W.poi("spawn", p["ar"], ax, y, az, "main", plaza=64)
    W.feat("spawn", player_spawn=(300, 71, 2050))


def build_hub(W):
    p = W.main("hub")
    ax, az, y = p["x"], p["z"], p["y"]
    cv = W.canvas("hub", ax - 62, y - 8, az - 62, ax + 63, y + 40, az + 63)
    rnd = np.random.default_rng(2)
    # paving
    for dz in range(-56, 57):
        for dx in range(-56, 57):
            ch = max(abs(dx), abs(dz))
            b = None
            if ch <= 13:
                b = "minecraft:smooth_sandstone" if (dx + dz) % 2 else "minecraft:cut_sandstone"
                if ch == 13:
                    b = "minecraft:terracotta"
            elif abs(dx) <= 4 and dz > 13 and dz < 56:   # souq street (south)
                b = "minecraft:cut_sandstone" if (dz % 4) else "minecraft:smooth_sandstone"
            elif abs(dz) <= 3 and (abs(dx) > 13 and abs(dx) < 50):
                b = "minecraft:coarse_dirt" if rnd.random() < 0.5 else "minecraft:packed_mud"
            elif rnd.random() < 0.10:
                b = "minecraft:coarse_dirt"
            if b:
                cv.set(ax + dx, y, az + dz, b)
    # well (NE of the anchor)
    well(cv, ax + 9, y, az - 9)
    W.feat("hub", well=(ax + 9, y + 1, az - 9))
    # quest board (west of anchor): 5-wide wooden board wall
    bx, bz = ax - 9, az - 4
    cv.fill(bx, y + 1, bz - 2, bx, y + 3, bz + 2, "minecraft:spruce_planks")
    cv.fill(bx - 1, y + 1, bz - 2, bx - 1, y + 4, bz - 2, "minecraft:spruce_log[axis=y]")
    cv.fill(bx - 1, y + 1, bz + 2, bx - 1, y + 4, bz + 2, "minecraft:spruce_log[axis=y]")
    cv.fill(bx - 1, y + 4, bz - 2, bx - 1, y + 4, bz + 2, "minecraft:spruce_slab[type=top]")
    cv.sign(bx + 1, y + 2, bz, ["لوحة", "المهام", "", ""], "east", wall=True)
    cv.set(bx + 1, y + 1, bz - 1, "minecraft:lectern[facing=west,has_book=false]")
    cv.set(bx + 1, y + 1, bz + 1, "minecraft:lectern[facing=west,has_book=false]")
    W.feat("hub", quest_board=(bx + 1, y + 1, bz))
    # shop stall east of anchor (with counter)
    sx, sz = ax + 9, az + 5
    for dx in (-2, 2):
        for dz in (-2, 2):
            cv.fill(sx + dx, y + 1, sz + dz, sx + dx, y + 4, sz + dz, "minecraft:oak_fence")
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            cv.set(sx + dx, y + 5, sz + dz, "minecraft:red_wool" if (dx + dz) % 2 else "minecraft:white_wool")
    cv.fill(sx - 2, y + 1, sz + 2, sx + 2, y + 1, sz + 2, "minecraft:dark_oak_planks")
    for dx in (-2, 0, 2):
        cv.barrel(sx + dx, y + 2, sz + 2, None)
    cv.sign(sx, y + 4, sz + 3, ["دكان", "الدلال", "", ""], "south", wall=True) if False else None
    cv.sign(sx, y + 3, sz + 3, ["دكان", "الدلال", "", ""], "south", wall=False)
    cv.set(sx, y + 1, sz, "air")
    W.feat("hub", shop=(sx, y + 1, sz + 1))
    # souq: stalls both sides of the south street
    colors = ["red", "yellow", "blue", "orange", "lime", "purple", "cyan", "magenta"]
    for i in range(6):
        zc = az + 19 + i * 6
        for side in (-1, 1):
            xc = ax + side * 9
            col = colors[(i * 2 + (side > 0)) % len(colors)]
            for dx in (-2, 2):
                for dz in (-2, 2):
                    cv.fill(xc + dx, y + 1, zc + dz, xc + dx, y + 3, zc + dz, "minecraft:oak_fence")
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    cv.set(xc + dx, y + 4, zc + dz, f"minecraft:{col}_wool" if (dx + dz) % 2 == 0 else "minecraft:white_wool")
            face = -side
            cv.fill(xc - 2, y + 1, zc + 2, xc + 2, y + 1, zc + 2, "minecraft:dark_oak_planks") if False else None
            inner = xc - side * 2
            cv.fill(inner, y + 1, zc - 2, inner, y + 1, zc + 2, "minecraft:dark_oak_planks")
            cv.set(inner, y + 2, zc - 1, "minecraft:barrel[facing=up]")
            cv.set(inner, y + 2, zc + 1, "minecraft:melon") if i % 2 else cv.set(inner, y + 2, zc + 1, "minecraft:hay_block")
            cv.set(xc + side * 1, y + 1, zc, "minecraft:chest[facing=%s]" % ("east" if side < 0 else "west")) if False else None
        lamp_post(cv, ax, y, zc, 4, "minecraft:dark_oak_fence")
    # tavern (west-north): two floors
    tx, tz, tw, td = ax - 48, az - 36, 28, 22
    cv.fill(tx, y, tz, tx + tw - 1, y, tz + td - 1, "minecraft:dark_oak_planks")
    cv.box(tx, y + 1, tz, tx + tw - 1, y + 9, tz + td - 1, "minecraft:terracotta", inner="air", roof=False, floor=False)
    for (cxp, czp) in ((tx, tz), (tx + tw - 1, tz), (tx, tz + td - 1), (tx + tw - 1, tz + td - 1)):
        cv.fill(cxp, y + 1, czp, cxp, y + 10, czp, "minecraft:stripped_dark_oak_log[axis=y]")
    cv.fill(tx + 1, y + 5, tz + 1, tx + tw - 2, y + 5, tz + td - 2, "minecraft:dark_oak_planks")     # upper floor
    cv.fill(tx + 8, y + 5, tz + 4, tx + 20, y + 5, tz + 10, "air")                                    # open well over the bar hall
    cv.fill(tx, y + 10, tz, tx + tw - 1, y + 10, tz + td - 1, "minecraft:smooth_sandstone")
    for x_ in range(tx, tx + tw):
        for z_ in (tz, tz + td - 1):
            cv.set(x_, y + 11, z_, slab("smooth_sandstone"))
    for z_ in range(tz, tz + td):
        for x_ in (tx, tx + tw - 1):
            cv.set(x_, y + 11, z_, slab("smooth_sandstone"))
    # door + windows on east side (facing the plaza)
    dxp = tx + tw - 1
    for dz in (tz + 9, tz + 12):
        cv.fill(dxp, y + 1, dz, dxp, y + 2, dz, "air")
    put_door(cv, dxp, y + 1, tz + 10, "east", "dark_oak")
    cv.fill(dxp, y + 1, tz + 11, dxp, y + 2, tz + 11, "air")
    for zz in (tz + 3, tz + 6, tz + 15, tz + 18):
        for yy in (y + 2, y + 7):
            cv.set(dxp, yy, zz, "minecraft:glass_pane")
            cv.set(tx, yy, zz, "minecraft:glass_pane")
    for xx in (tx + 5, tx + 10, tx + 17, tx + 22):
        for yy in (y + 2, y + 7):
            cv.set(xx, yy, tz, "minecraft:glass_pane")
            cv.set(xx, yy, tz + td - 1, "minecraft:glass_pane")
    # bar counter, tables, lanterns
    cv.fill(tx + 3, y + 1, tz + 3, tx + 3, y + 1, tz + 12, "minecraft:dark_oak_planks")
    for zz in range(tz + 3, tz + 13, 2):
        cv.barrel(tx + 2, y + 1, zz, "nahas:chests/oasis")
    cv.set(tx + 3, y + 2, tz + 5, "minecraft:brewing_stand[has_bottle_0=false,has_bottle_1=false,has_bottle_2=false]")
    for (xx, zz) in ((tx + 12, tz + 5), (tx + 12, tz + 15), (tx + 18, tz + 8), (tx + 18, tz + 16), (tx + 8, tz + 17)):
        cv.set(xx, y + 1, zz, "minecraft:dark_oak_fence")
        cv.set(xx, y + 2, zz, "minecraft:dark_oak_pressure_plate")
        for (a, b, f) in ((1, 0, "west"), (-1, 0, "east")):
            cv.set(xx + a, y + 1, zz + b, stair("dark_oak", f))
    for (xx, zz) in ((tx + 8, tz + 5), (tx + 20, tz + 5), (tx + 8, tz + 16), (tx + 20, tz + 16), (tx + 14, tz + 10)):
        cv.set(xx, y + 4, zz, lantern(True))
        cv.set(xx, y + 9, zz, lantern(True))
    # stairs up (west end) + upper rooms
    for i in range(4):
        cv.set(tx + 22 + i, y + 1 + i, tz + td - 3, stair("dark_oak", "east"))
        cv.fill(tx + 22 + i, y + 1, tz + td - 3, tx + 22 + i, y + i, tz + td - 3, "minecraft:dark_oak_planks") if i else None
    for k in range(3):
        rzz = tz + 2 + k * 6
        cv.fill(tx + 2, y + 6, rzz, tx + 2, y + 6, rzz, "minecraft:red_bed[facing=east,part=foot]")
        cv.set(tx + 3, y + 6, rzz, "minecraft:red_bed[facing=east,part=head]")
        cv.fill(tx + 5, y + 6, rzz + 2, tx + 5, y + 9, rzz + 2, "minecraft:dark_oak_planks")
    cv.sign(dxp + 1, y + 4, tz + 10, ["نُزُل", "الدلال", "", ""], "east", wall=True)
    W.feat("hub", tavern_door=(dxp, y + 1, tz + 10), tavern_center=(tx + 14, y + 1, tz + 10))
    # houses
    hs = [(-56, -2, 8, 8, 4, "east"), (-56, 10, 9, 8, 5, "east"), (-56, 24, 8, 9, 4, "east"),
          (40, -12, 9, 8, 4, "west"), (40, 2, 9, 8, 5, "west"), (40, 18, 9, 9, 4, "west"),
          (4, -52, 9, 8, 4, "south"), (20, -52, 8, 8, 5, "south"), (36, -46, 8, 8, 4, "south"),
          (-20, 40, 9, 8, 4, "north"), (-20, 52, 9, 6, 4, "east") if False else (-34, 42, 9, 8, 5, "north"),
          (24, 46, 8, 8, 4, "north") if False else (26, 40, 8, 9, 4, "north")]
    for (rx, rz, w, d, h, door_) in hs:
        house(cv, ax + rx, y, az + rz, w, d, h, door_, rnd=rnd, win="minecraft:glass_pane")
    # palms & benches at the plaza edge
    for (rx, rz) in ((-14, -14), (14, -14), (-14, 14), (14, 14), (-8, 20), (8, 20), (-30, -8), (30, -20), (-26, 30), (32, 32), (-40, 10), (50, 24)):
        cv.fill(ax + rx - 1, y, az + rz - 1, ax + rx + 1, y, az + rz + 1, "minecraft:grass_block[snowy=false]")
        palm(cv, ax + rx, y, az + rz, int(rnd.integers(6, 9)), rnd)
    for (rx, rz) in ((-12, -1), (12, 1), (0, -12), (0, 12)):
        lamp_post(cv, ax + rx, y, az + rz, 4, "minecraft:dark_oak_fence")
    W.poi("hub", p["ar"], ax, y, az, "main", plaza=116)


def build_t1(W):
    p = W.main("t1")
    ax, az, y = p["x"], p["z"], p["y"]
    cv = W.canvas("t1", ax - 50, y - 10, az - 50, ax + 51, y + 34, az + 51)
    rnd = np.random.default_rng(3)
    SS, CS, SM = "minecraft:sandstone", "minecraft:cut_sandstone", "minecraft:smooth_sandstone"
    CH = "minecraft:chiseled_sandstone"
    # plaza pavement
    for dz in range(-40, 41):
        for dx in range(-40, 41):
            if az + dz < 1895 and abs(dx) < 27:
                continue
            ch = max(abs(dx), abs(dz))
            b = SM if (dx // 3 + dz // 3) % 2 == 0 else CS
            if abs(dx) < 3 and dz > 0:
                b = "minecraft:yellow_terracotta"
            cv.set(ax + dx, y, az + dz, b)
    # reflecting pool
    for dz in range(10, 26):
        for dx in range(-9, 10):
            cv.set(ax + dx, y, az + dz, "minecraft:water")
    for dz in range(9, 27):
        for dx in range(-10, 11):
            if abs(dx) == 10 or dz in (9, 26):
                cv.set(ax + dx, y, az + dz, CH)
                cv.set(ax + dx, y + 1, az + dz, slab("sandstone")) if (dx + dz) % 4 == 0 else None
    # temple body: z from az-38 .. az-6, x az-24..+24
    z0, z1 = az - 38, az - 6            # back wall .. front wall
    x0, x1 = ax - 24, ax + 24
    H = 12
    cv.fill(x0 - 1, y, z0 - 1, x1 + 1, y, z1 + 3, SM)     # floor incl. porch
    cv.box(x0, y + 1, z0, x1, y + H, z1, CS, inner="air", roof=True, floor=False)
    cv.fill(x0, y + H, z0, x1, y + H, z1, CS)
    # corner buttresses & frieze
    for (cx_, cz_) in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        cv.fill(cx_ - 1, y + 1, cz_ - 1, cx_ + 1, y + H + 2, cz_ + 1, SS)
        cv.fill(cx_, y + H + 3, cz_, cx_, y + H + 5, cz_, CH)
    for xx in range(x0, x1 + 1):
        cv.set(xx, y + H - 1, z1, CH if xx % 2 else SM)
        cv.set(xx, y + H - 1, z0, CH if xx % 2 else SM)
    for zz in range(z0, z1 + 1):
        cv.set(x0, y + H - 1, zz, CH if zz % 2 else SM)
        cv.set(x1, y + H - 1, zz, CH if zz % 2 else SM)
    # ziggurat roof
    for t in range(0, 6):
        cv.fill(x0 + 3 + t * 3, y + H + 1 + t, z0 + 3 + t * 2, x1 - 3 - t * 3, y + H + 1 + t, z1 - 3 - t * 2, CS if t % 2 == 0 else SM)
    cv.fill(ax - 1, y + H + 7, (z0 + z1) // 2 - 1, ax + 1, y + H + 8, (z0 + z1) // 2 + 1, "minecraft:gold_block")
    cv.set(ax, y + H + 9, (z0 + z1) // 2, "minecraft:gold_block")
    # facade colonnade (porch): pillars in front of z1
    for xx in range(x0 + 2, x1 - 1, 6):
        cv.fill(xx, y + 1, z1 + 3, xx, y + H - 1, z1 + 3, SS)
        cv.set(xx, y + H, z1 + 3, CH)
        cv.set(xx, y + 1, z1 + 3, CH)
    cv.fill(x0, y + H, z1 + 1, x1, y + H, z1 + 3, CS)
    # obelisks
    for sx in (-1, 1):
        ox, oz = ax + sx * 30, az + 4
        cv.fill(ox - 1, y + 1, oz - 1, ox + 1, y + 3, oz + 1, SS)
        cv.fill(ox, y + 4, oz, ox, y + 16, oz, CS)
        cv.set(ox, y + 17, oz, "minecraft:gold_block")
        for yy in range(6, 16, 3):
            cv.set(ox, y + yy, oz - 1, CH) if False else None
    # entrance: portal in front wall
    for xx in range(ax - 2, ax + 3):
        cv.fill(xx, y + 1, z1, xx, y + 6, z1, "air")
    cv.fill(ax - 3, y + 7, z1, ax + 3, y + 7, z1, CH)
    for zz in (z1,):
        for xx in (ax - 3, ax + 3):
            cv.fill(xx, y + 1, zz, xx, y + 6, zz, CH)
    # antechamber (z1-8 .. z1-1): two rows of pillars, braziers
    zh0 = z1 - 9
    cv.fill(x0 + 1, y + 1, zh0, x1 - 1, y + H - 1, zh0, CS)          # partition wall between antechamber and puzzle room
    for xx in range(ax - 2, ax + 3):
        cv.fill(xx, y + 1, zh0, xx, y + 5, zh0, "air")
    for xx in (ax - 3, ax + 3):
        cv.fill(xx, y + 1, zh0, xx, y + 5, zh0, CH)
    cv.fill(ax - 3, y + 6, zh0, ax + 3, y + 6, zh0, CH)
    for xx in range(x0 + 4, x1 - 3, 6):
        for zz in (zh0 + 3, zh0 + 6):
            cv.fill(xx, y + 1, zz, xx, y + H - 1, zz, SS)
            cv.set(xx, y + 1, zz, CH)
    for xx in range(x0 + 4, x1 - 3, 6):
        cv.set(xx + 3, y + 1, zh0 + 2, "minecraft:campfire[lit=true,facing=north]")
        cv.set(xx + 3, y + H - 2, zh0 + 5, lantern(True)) if False else None
    for xx in range(x0 + 3, x1 - 2, 4):
        cv.set(xx, y + H - 1, zh0 + 4, lantern(True))
    cv.chest(x0 + 2, y + 1, zh0 + 8, "east", "nahas:chests/oasis")
    # PUZZLE ROOM: z (z0+8 .. zh0-1), x (x0+1 .. x1-1)
    pz0, pz1 = z0 + 9, zh0 - 1
    pcx, pcz = ax, (pz0 + pz1) // 2
    # mosaic floor
    for zz in range(pz0, pz1 + 1):
        for xx in range(x0 + 1, x1):
            dd = np.hypot(xx - pcx, zz - pcz)
            b = CS if (xx + zz) % 2 else SM
            if dd < 7:
                b = "minecraft:orange_terracotta" if dd > 5 else ("minecraft:yellow_terracotta" if dd > 2.5 else "minecraft:gold_block")
            cv.set(xx, y, zz, b)
    # 3x3 tile grid puzzle (pressure plates) + 4 sun pedestals in corners
    pedestals = []
    for (sx, sz) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        px, pz = pcx + sx * 14, pcz + sz * (pz1 - pz0) // 2 - sz * 2
        cv.fill(px - 1, y + 1, pz - 1, px + 1, y + 1, pz + 1, CH)
        cv.fill(px, y + 2, pz, px, y + 3, pz, SS)
        cv.set(px, y + 4, pz, "minecraft:copper_block") if False else cv.set(px, y + 4, pz, "minecraft:gold_block")
        cv.set(px, y + 5, pz, "minecraft:soul_lantern[hanging=false]")
        cv.set(px - sx * 2, y + 1, pz, "minecraft:stone_pressure_plate")
        pedestals.append((px, y + 4, pz))
    W.feat("t1", pedestals=pedestals)
    # grid of floor plates in the center (visible puzzle)
    grid = []
    for i in range(3):
        for j in range(3):
            gx, gz = pcx - 6 + i * 6, pcz - 4 + j * 4
            cv.set(gx, y, gz, "minecraft:red_terracotta" if (i + j) % 2 else "minecraft:blue_terracotta")
            cv.set(gx, y + 1, gz, "minecraft:polished_blackstone_pressure_plate")
            grid.append((gx, y + 1, gz))
    W.feat("t1", plate_grid=grid, puzzle_room=(pcx, y + 1, pcz))
    for zz in range(pz0 + 2, pz1, 5):
        for xx in (x0 + 2, x1 - 2):
            cv.fill(xx, y + 1, zz, xx, y + H - 2, zz, SS)
            cv.set(xx, y + 1, zz, CH)
            cv.set(xx + (1 if xx < ax else -1), y + 5, zz, "minecraft:wall_torch[facing=%s]" % ("east" if xx < ax else "west"))
    for xx in range(x0 + 4, x1 - 3, 8):
        cv.set(xx, y + H - 1, pcz, lantern(True))
        cv.set(xx, y + H - 1, pcz - 6, lantern(True))
        cv.set(xx, y + H - 1, pcz + 6, lantern(True))
    # hieroglyph walls (chiseled bands with gold dots)
    for zz in (pz0 - 1,):
        for xx in range(x0 + 2, x1 - 1):
            cv.set(xx, y + 3, zz, CH)
            cv.set(xx, y + 7, zz, CH) if xx % 2 else None
    # TRIAL CHAMBER behind the puzzle room (sealed by an iron door)
    zt0, zt1 = z0 + 1, pz0 - 2
    cv.fill(x0 + 1, y + 1, pz0 - 1, x1 - 1, y + H - 1, pz0 - 1, CS)      # dividing wall
    for xx in range(ax - 1, ax + 2):
        cv.fill(xx, y + 1, pz0 - 1, xx, y + 3, pz0 - 1, "air")
    put_door(cv, ax, y + 1, pz0 - 1, "south", "iron", "left", False)
    cv.set(ax - 1, y + 1, pz0 - 1, CH); cv.set(ax + 1, y + 1, pz0 - 1, CH)
    cv.fill(ax - 1, y + 2, pz0 - 1, ax - 1, y + 3, pz0 - 1, CH); cv.fill(ax + 1, y + 2, pz0 - 1, ax + 1, y + 3, pz0 - 1, CH)
    W.feat("t1", sealed_door=(ax, y + 1, pz0 - 1), sealed_door_y2=(ax, y + 2, pz0 - 1))
    for zz in range(zt0, zt1 + 1):
        for xx in range(x0 + 1, x1):
            cv.set(xx, y, zz, "minecraft:polished_blackstone" if (xx + zz) % 3 else "minecraft:gilded_blackstone") if False else cv.set(xx, y, zz, "minecraft:cut_red_sandstone" if (xx + zz) % 2 else "minecraft:red_sandstone")
    ax_z = (zt0 + zt1) // 2
    cv.fill(ax - 3, y + 1, ax_z - 2, ax + 3, y + 1, ax_z + 2, "minecraft:gold_block")       # seal altar dais
    cv.fill(ax - 1, y + 2, ax_z - 1, ax + 1, y + 2, ax_z + 1, CH)
    cv.set(ax, y + 3, ax_z, "minecraft:lodestone")
    cv.set(ax, y + 4, ax_z, lantern(False))
    cv.chest(ax, y + 2, ax_z + 3, "south", "nahas:chests/rare") if False else None
    W.feat("t1", seal_altar=(ax, y + 3, ax_z), trial_chamber=(ax, y + 1, ax_z))
    for xx in range(x0 + 3, x1 - 2, 6):
        cv.set(xx, y + H - 1, ax_z, lantern(True))
    cv.chest(x0 + 3, y + 1, zt0 + 2, "east", "nahas:chests/rare")
    cv.chest(x1 - 3, y + 1, zt0 + 2, "west", "nahas:chests/common")
    # palms near the pool
    for (rx, rz) in ((-16, 12), (16, 12), (-16, 24), (16, 24), (-30, 16), (30, 16), (-34, 28), (34, 28)):
        cv.fill(ax + rx - 1, y, az + rz - 1, ax + rx + 1, y, az + rz + 1, "minecraft:grass_block[snowy=false]")
        palm(cv, ax + rx, y, az + rz, int(rnd.integers(6, 9)), rnd)
    for (rx, rz) in ((-6, 3), (6, 3), (-6, 14), (6, 14)):
        pass
    for (rx, rz) in ((-12, 0), (12, 0), (-12, 30), (12, 30)):
        lamp_post(cv, ax + rx, y, az + rz, 4, "minecraft:birch_fence")
    cv.sign(ax + 4, y + 1, az + 2, ["معبد", "الواحة", "", ""], "south", wall=False, mat="birch")
    W.feat("t1", temple_entrance=(ax, y + 1, z1), antechamber=(ax, y + 1, zh0 + 4))
    W.poi("t1", p["ar"], ax, y, az, "main", plaza=84)
