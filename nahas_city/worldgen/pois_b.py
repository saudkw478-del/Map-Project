"""Main POIs part B: t2 scorpion arena, t3 sunken library, t4 wind fortress, star & ember shrines."""
import numpy as np
from wg_core import Canvas, B
from shapes import *
from pois_a import scatter

RS, CRS, SRS = "minecraft:red_sandstone", "minecraft:cut_red_sandstone", "minecraft:smooth_red_sandstone"
CHRS = "minecraft:chiseled_red_sandstone"


def build_t2(W):
    p = W.main("t2")
    ax, az, y = p["x"], p["z"], p["y"]
    cv = W.canvas("t2", ax - 48, y - 6, az - 48, ax + 49, y + 24, az + 49)
    rnd = np.random.default_rng(4)
    for dz in range(-40, 41):
        for dx in range(-40, 41):
            d = np.hypot(dx, dz)
            x, z = ax + dx, az + dz
            if d <= 30.5:
                b = CRS if (dx + dz) % 2 else SRS
                if 25 <= d < 28.5:
                    b = "minecraft:red_terracotta"
                elif 19 <= d < 21:
                    b = "minecraft:orange_terracotta"
                elif d < 4.5:
                    b = "minecraft:yellow_terracotta" if d > 2.5 else CHRS
                else:
                    ang = np.degrees(np.arctan2(dz, dx)) % 45
                    if (ang < 3 or ang > 42) and 4.5 <= d < 25:
                        b = "minecraft:black_terracotta"
                if (dx or dz):
                    cv.set(x, y, z, b)
                if rnd.random() < 0.03 and d > 6:
                    cv.set(x, y, z, "minecraft:red_sand")
            elif 30.5 < d <= 34:
                gate = min(abs(dx), abs(dz)) <= 3
                cv.set(x, y, z, CRS)
                hgt = 8
                if gate:
                    hgt = 0
                    cv.set(x, y, z, CRS)
                    if dz > 0 and abs(dx) <= 3 and abs(dz) > abs(dx):   # south = open entrance
                        pass
                    elif min(abs(dx), abs(dz)) <= 3 and d < 33:
                        cv.fill(x, y + 1, z, x, y + 6, z, "minecraft:iron_bars")
                if hgt:
                    top = y + hgt + (1 if (dx + dz) % 2 else 0)
                    cv.fill(x, y + 1, z, x, top, z, [RS, CRS, RS, "minecraft:red_sandstone_wall" if False else CRS][int(rnd.integers(0, 4))] if False else CRS)
    # south gate arch
    for dx in range(-4, 5):
        for dz in range(30, 35):
            cv.fill(ax + dx, y + 7, az + dz, ax + dx, y + 9, az + dz, CRS)
    for dz in range(30, 35):
        for dx in (-4, 4):
            cv.fill(ax + dx, y + 1, az + dz, ax + dx, y + 6, az + dz, CHRS)
    # tiered seating (inside the wall, sloped)
    for t in range(3):
        r_ = 29 - t
        # (kept simple: torches on the wall top)
    for k in range(16):
        a = k * np.pi / 8
        x, z = int(ax + 32 * np.cos(a)), int(az + 32 * np.sin(a))
        cv.set(x, y + 10, z, lantern(False))
    # pillars
    for k in range(8):
        a = k * np.pi / 4 + np.pi / 8
        px, pz = int(round(ax + 22 * np.cos(a))), int(round(az + 22 * np.sin(a)))
        h = int(rnd.integers(6, 10))
        cv.fill(px, y + 1, pz, px, y + h, pz, CRS)
        cv.set(px, y + 1, pz, CHRS)
        cv.set(px, y + h, pz, CHRS)
        cv.set(px + 1, y + h - 1, pz, "minecraft:cobweb")
        cv.set(px, y + h - 2, pz + 1, "minecraft:cobweb")
        cv.set(px, y + h + 1, pz, lantern(False))
    # scorpion queen nest (north side of arena)
    nx, nz = ax, az - 20
    for dx in range(-6, 7):
        for dz in range(-6, 7):
            d = np.hypot(dx, dz)
            if d <= 6:
                hh = int(3 - d / 2.2)
                for yy in range(1, max(1, hh) + 1):
                    cv.set(nx + dx, y + yy, nz + dz, "minecraft:soul_sand" if yy == 1 else "minecraft:red_sand")
                if rnd.random() < 0.35:
                    cv.set(nx + dx, y + max(1, hh) + 1, nz + dz, "minecraft:cobweb")
    for k in range(6):   # rib bones
        a = -np.pi / 2 + (k - 2.5) * 0.45
        bx, bz = int(nx + 5 * np.cos(a)), int(nz + 5 * np.sin(a))
        cv.fill(bx, y + 1, bz, bx, y + 5, bz, "minecraft:bone_block[axis=y]")
    cv.set(nx, y + 4, nz, "minecraft:skeleton_skull[rotation=0]") if False else None
    cv.chest(nx, y + 1, nz + 1, "south", "nahas:chests/rare") if False else None
    # bones scattered
    for (x, z) in scatter(rnd, ax, az, 6, 28, 16, sep=4):
        cv.set(x, y + 1, z, "minecraft:bone_block[axis=x]") if rnd.random() < 0.5 else cv.set(x, y + 1, z, "minecraft:skeleton_skull[rotation=%d]" % int(rnd.integers(0, 16)))
    cv.chest(ax - 26, y + 1, az, "east", "nahas:chests/rare")
    cv.sign(ax + 4, y + 1, az + 38, ["وادي", "العقارب", "احذر الملكة", ""], "south", wall=False, mat="acacia")
    W.feat("t2", arena_radius=30, boss_nest=(nx, y + 1, nz), gates=[(ax, y, az - 33), (ax, y, az + 33), (ax - 33, y, az), (ax + 33, y, az)],
           entrance=(ax, y + 1, az + 33))
    W.poi("t2", p["ar"], ax, y, az, "main", plaza=60)


def build_t3(W):
    p = W.main("t3")
    ax, az, y = p["x"], p["z"], p["y"]
    cv = W.canvas("t3", ax - 60, 30, az - 30, ax + 61, y + 30, az + 112)
    rnd = np.random.default_rng(5)
    # island paving
    for dz in range(-34, 35):
        for dx in range(-34, 35):
            b = "minecraft:prismarine_bricks" if (dx // 2 + dz // 2) % 3 == 0 else ("minecraft:cut_sandstone" if (dx + dz) % 2 else "minecraft:smooth_sandstone")
            if max(abs(dx), abs(dz)) in (33, 34):
                b = "minecraft:chiseled_stone_bricks"
            cv.set(ax + dx, y, az + dz, b)
    # compass inlay around the anchor
    for dz in range(-8, 9):
        for dx in range(-8, 9):
            d = np.hypot(dx, dz)
            if 6 <= d < 7.5 and (dx or dz):
                cv.set(ax + dx, y, az + dz, "minecraft:blue_terracotta")
    # island rim wall segments + lanterns
    for k in range(0, 69, 6):
        for (x, z) in ((ax - 34, az - 34 + k), (ax + 34, az - 34 + k), (ax - 34 + k, az - 34), (ax - 34 + k, az + 34)):
            cv.fill(x, y + 1, z, x, y + 2, z, "minecraft:cut_sandstone_wall" if False else "minecraft:sandstone_wall")
            cv.set(x, y + 3, z, lantern(False))
    # palms on island corners
    for (dx, dz) in ((-28, -28), (28, -28), (-28, 26), (28, 26), (-30, 0), (30, 0)):
        cv.fill(ax + dx - 1, y, az + dz - 1, ax + dx + 1, y, az + dz + 1, "minecraft:grass_block[snowy=false]")
        palm(cv, ax + dx, y, az + dz, 7, rnd)
    # ---- bridge from south shore
    for z in range(az + 35, az + 100):
        for x in range(ax - 2, ax + 3):
            cv.set(x, y, z, "minecraft:spruce_planks")
        for x in (ax - 3, ax + 3):
            cv.set(x, y + 1, z, "minecraft:spruce_fence") if z % 2 == 0 or True else None
        if (z - az) % 8 == 0:
            for x in (ax - 3, ax + 3):
                cv.fill(x, y - 24, z, x, y - 1, z, "minecraft:stripped_spruce_log[axis=y]")
                cv.fill(x, y + 1, z, x, y + 2, z, "minecraft:spruce_fence")
                cv.set(x, y + 3, z, lantern(False))
    cv.fill(ax - 2, y, az + 96, ax + 2, y, az + 104, "minecraft:spruce_planks")
    # ---- entrance pavilion on the north side of the island
    px, pz = ax, az - 16
    cv.disc(px, pz, 8, y, "minecraft:polished_diorite", pat=lambda dx, dz: "minecraft:quartz_block" if (abs(dx) + abs(dz)) % 2 else "minecraft:polished_diorite")
    for k in range(8):
        a = k * np.pi / 4 + np.pi / 8
        x, z = int(round(px + 7 * np.cos(a))), int(round(pz + 7 * np.sin(a)))
        cv.fill(x, y + 1, z, x, y + 8, z, "minecraft:quartz_pillar[axis=y]")
        cv.set(x, y + 9, z, "minecraft:chiseled_quartz_block")
    cv.disc(px, pz, 8, y + 10, "minecraft:quartz_slab[type=bottom]")
    cv.sphere(px, y + 10, pz, 8, "minecraft:waxed_oxidized_cut_copper", thick=1, upper=True)
    cv.set(px, y + 19, pz, "minecraft:lightning_rod") if False else cv.set(px, y + 19, pz, "minecraft:gold_block")
    # shaft
    cv.fill(px - 2, 43, pz - 2, px + 2, y, pz + 2, "air")
    ring = [(dx, -2) for dx in range(-2, 3)] + [(2, dz) for dz in range(-1, 3)] + [(dx, 2) for dx in range(1, -3, -1)] + [(-2, dz) for dz in range(1, -2, -1)]
    for k in range(1, 28):
        dx, dz = ring[k % len(ring)]
        cv.set(px + dx, y - k, pz + dz, "minecraft:stone_bricks")
        cv.set(px + dx, y - k + 1, pz + dz, "air")
    for yy in range(46, y, 8):
        for (dx, dz) in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
            cv.set(px + dx, yy, pz + dz, "minecraft:lantern[hanging=false]") if False else None
    for yy in range(48, y - 2, 6):
        cv.set(px - 3, yy, pz, "minecraft:sea_lantern") if False else None
    # shaft walls & lights (walls are natural ground/stone; add lanterns hanging over steps)
    # base chamber + tunnel south to the main hall
    BASE = 42
    cv.fill(px - 3, BASE, pz - 3, px + 3, BASE, pz + 3, "minecraft:stone_bricks")
    cv.fill(px - 3, BASE + 1, pz - 3, px + 3, BASE + 5, pz + 3, "air")
    cv.fill(px - 1, BASE, pz - 1, px + 1, BASE, pz + 1, "minecraft:water")
    hx, hz = ax, az + 60
    cv.fill(ax - 1, BASE, pz + 3, ax + 1, BASE, hz - 16, "minecraft:stone_bricks")
    cv.fill(ax - 1, BASE + 1, pz + 3, ax + 1, BASE + 4, hz - 16, "air")
    cv.fill(ax - 2, BASE, pz + 3, ax - 2, BASE + 5, hz - 16, "minecraft:prismarine_bricks")
    cv.fill(ax + 2, BASE, pz + 3, ax + 2, BASE + 5, hz - 16, "minecraft:prismarine_bricks")
    cv.fill(ax - 2, BASE + 5, pz + 3, ax + 2, BASE + 5, hz - 16, "minecraft:prismarine_bricks")
    for z in range(pz + 5, hz - 16, 5):
        cv.set(ax, BASE + 1, z, "minecraft:sea_lantern")
    # ---- main hall (dome on the lake bed)
    R_ = 18
    cv.fill(hx - R_ - 1, BASE, hz - R_ - 1, hx + R_ + 1, BASE, hz + R_ + 1, "minecraft:stone_bricks") if False else None
    cv.cyl(hx, hz, R_, BASE, BASE, "minecraft:prismarine_bricks")
    for yy in range(BASE + 1, 48):
        cv.disc(hx, hz, R_, yy, "minecraft:stone_bricks", r_in=R_ - 1) if False else None
    for yy in range(BASE + 1, 48):
        cv.disc(hx, hz, R_ - 1, yy, "air")
        cv.disc(hx, hz, R_, yy, "minecraft:stone_bricks", r_in=R_)
        cv.disc(hx, hz, R_ + 1, yy, "minecraft:stone_bricks", r_in=R_ + 1) if False else None
    cv.sphere(hx, 48, hz, R_ - 1, "air", thick=0, upper=True)     # placeholder (no-op)
    r2o, r2i = (R_ + 0.5) ** 2, (R_ - 0.5) ** 2
    for yy in range(48, 48 + R_ + 1):
        for zz in range(hz - R_, hz + R_ + 1):
            for xx in range(hx - R_, hx + R_ + 1):
                d = (xx - hx) ** 2 + (yy - 48) ** 2 + (zz - hz) ** 2
                if d < r2i:
                    cv.set(xx, yy, zz, "air")
                elif d <= r2o:
                    rib = ((xx - hx) % 6 == 0 or (zz - hz) % 6 == 0) and (yy - 48) % 1 == 0
                    cv.set(xx, yy, zz, "minecraft:waxed_oxidized_cut_copper" if rib else "minecraft:glass")
    # floor pattern
    for dz in range(-R_ + 1, R_):
        for dx in range(-R_ + 1, R_):
            d = np.hypot(dx, dz)
            if d < R_ - 0.5:
                b = "minecraft:prismarine_bricks" if (dx + dz) % 2 else "minecraft:dark_prismarine"
                if d < 5:
                    b = "minecraft:gold_block" if d < 2 else "minecraft:cut_sandstone"
                elif 10.5 < d < 11.6 and (abs(dx) + abs(dz)) % 3 == 0:
                    b = "minecraft:sea_lantern"
                cv.set(hx + dx, BASE, hz + dz, b)
    # bookshelves ring
    for k in range(64):
        a = k * 2 * np.pi / 64
        for rr in (15.5, 16.4):
            x, z = int(round(hx + rr * np.cos(a))), int(round(hz + rr * np.sin(a)))
            dxr, dzr = x - hx, z - hz
            if abs(dxr) <= 2 or abs(dzr) <= 2:   # leave 4 doorways
                continue
            cv.fill(x, BASE + 1, z, x, BASE + 5, z, "minecraft:bookshelf")
    # reading dais: lecterns
    for k in range(8):
        a = k * np.pi / 4
        x, z = int(round(hx + 7 * np.cos(a))), int(round(hz + 7 * np.sin(a)))
        cv.set(x, BASE + 1, z, "minecraft:lectern[facing=south,has_book=false]")
    # chandelier
    for yy in range(58, 65):
        cv.set(hx, yy, hz, "minecraft:chain[axis=y]")
    cv.set(hx, 57, hz, lantern(True))
    for (dx, dz) in ((2, 0), (-2, 0), (0, 2), (0, -2)):
        cv.set(hx + dx, 60, hz + dz, "minecraft:sea_lantern")
    # open doorways: north (tunnel), south (seal room), east/west (flooded wings)
    for yy in range(BASE + 1, BASE + 4):
        cv.fill(hx - 1, yy, hz - R_, hx + 1, yy, hz - R_ + 1, "air")
    # ---- seal room to the south
    sz0 = hz + R_
    cv.fill(hx - 1, BASE, sz0, hx + 1, BASE + 4, sz0 + 4, "air")
    cv.fill(hx - 1, BASE, sz0, hx + 1, BASE, sz0 + 4, "minecraft:stone_bricks")
    rx0, rz0, rx1, rz1 = hx - 6, sz0 + 5, hx + 6, sz0 + 14
    cv.box(rx0, BASE, rz0, rx1, BASE + 6, rz1, "minecraft:prismarine_bricks", inner="air")
    cv.fill(hx - 1, BASE + 1, sz0 + 5, hx + 1, BASE + 3, sz0 + 5, "air")
    for xx in range(rx0 + 1, rx1):
        for zz in range(rz0 + 1, rz1):
            cv.set(xx, BASE, zz, "minecraft:dark_prismarine" if (xx + zz) % 2 else "minecraft:prismarine_bricks")
    cv.fill(hx - 1, BASE + 1, rz1 - 3, hx + 1, BASE + 1, rz1 - 1, "minecraft:gold_block")
    cv.set(hx, BASE + 2, rz1 - 2, "minecraft:lodestone")
    cv.set(hx, BASE + 3, rz1 - 2, "minecraft:sea_lantern") if False else None
    cv.chest(rx0 + 1, BASE + 1, rz0 + 1, "east", "nahas:chests/library")
    cv.chest(rx1 - 1, BASE + 1, rz0 + 1, "west", "nahas:chests/library")
    for xx in (rx0 + 2, rx1 - 2):
        cv.set(xx, BASE + 5, (rz0 + rz1) // 2, lantern(True))
    for k in range(0, 9):
        cv.fill(rx0 + 1 + k, BASE + 1, rz1 - 1, rx0 + 1 + k, BASE + 4, rz1 - 1, "minecraft:bookshelf") if k % 2 == 0 and abs(rx0 + 1 + k - hx) > 3 else None
    W.feat("t3", seal_altar=(hx, BASE + 2, rz1 - 2), seal_room=(hx, BASE + 1, (rz0 + rz1) // 2))
    # ---- flooded wings east / west
    for s in (-1, 1):
        wx0, wx1 = (hx + s * 26, hx + s * 46)
        xa, xb = min(wx0, wx1), max(wx0, wx1)
        za, zb = hz - 10, hz + 10
        cv.box(xa, BASE, za, xb, BASE + 6, zb, "minecraft:prismarine_bricks", inner="minecraft:water")
        # corridor from the hall doorway (hx+s*18) to wing wall (hx+s*26)
        cxa, cxb = sorted((hx + s * (R_ - 1), hx + s * 26))
        cv.fill(cxa, BASE, hz - 2, cxb, BASE + 5, hz + 2, "minecraft:prismarine_bricks")
        cv.fill(cxa, BASE + 1, hz - 1, cxb, BASE + 4, hz + 1, "minecraft:water")
        # doorway in hall wall (air->water is contained by glass? corridor opens into hall: seal with iron bars so water stays)
        for yy in range(BASE + 1, BASE + 5):
            for zz in range(hz - 1, hz + 2):
                cv.set(hx + s * R_, yy, zz, "minecraft:iron_bars")
        # bookshelf islands & lights inside
        for k in range(3):
            cv.fill(xa + 3 + k * 6, BASE + 1, za + 3, xa + 3 + k * 6, BASE + 4, za + 3, "minecraft:bookshelf")
            cv.fill(xa + 3 + k * 6, BASE + 1, zb - 3, xa + 3 + k * 6, BASE + 4, zb - 3, "minecraft:bookshelf")
            cv.set(xa + 3 + k * 6, BASE + 1, hz, "minecraft:sea_lantern")
        cv.fill((xa + xb) // 2 - 1, BASE + 5, hz - 1, (xa + xb) // 2, BASE + 5, hz, "air")     # air pocket
        cv.chest((xa + xb) // 2, BASE + 1, hz + 4, "south", "nahas:chests/library")
        W.feat("t3", **{("wing_west" if s < 0 else "wing_east"): ((xa + xb) // 2, BASE + 1, hz)})
    W.feat("t3", pavilion=(px, y + 1, pz), shaft_top=(px, y + 1, pz), main_hall=(hx, BASE + 1, hz), bridge_start=(ax, y + 1, az + 100), lake=(ax, 69, az))
    cv.sign(ax + 4, y + 1, az + 40, ["المكتبة", "الغارقة", "", ""], "south", wall=False, mat="spruce")
    W.poi("t3", p["ar"], ax, y, az, "main", plaza=68)


def build_t4(W):
    p = W.main("t4")
    ax, az, y = p["x"], p["z"], p["y"]
    cv = W.canvas("t4", ax - 40, y - 8, az - 40, ax + 41, y + 60, az + 41)
    rnd = np.random.default_rng(6)
    PB, BL, SB, DS = "minecraft:polished_blackstone_bricks", "minecraft:blackstone", "minecraft:smooth_basalt", "minecraft:deepslate_bricks"
    # courtyard paving
    for dz in range(-31, 32):
        for dx in range(-31, 32):
            b = "minecraft:polished_blackstone" if (dx // 4 + dz // 4) % 2 else "minecraft:polished_basalt[axis=y]"
            if max(abs(dx), abs(dz)) > 29:
                b = DS
            cv.set(ax + dx, y, az + dz, b)
    # outer curtain wall (half=32, thickness 3), height 12 + crenels
    for dz in range(-34, 35):
        for dx in range(-34, 35):
            ch = max(abs(dx), abs(dz))
            if 31 <= ch <= 33:
                if dz > 30 and abs(dx) <= 4:      # south gate
                    cv.set(ax + dx, y, az + dz, DS)
                    continue
                cv.fill(ax + dx, y + 1, az + dz, ax + dx, y + 12, az + dz, PB)
                if (dx + dz) % 2 == 0:
                    cv.set(ax + dx, y + 13, az + dz, PB)
                if ch == 31:
                    cv.set(ax + dx, y + 12, az + dz, "minecraft:polished_blackstone_brick_slab[type=top]") if False else None
    # gate: portcullis + arch
    for dx in range(-4, 5):
        for dz in range(31, 34):
            cv.fill(ax + dx, y + 8, az + dz, ax + dx, y + 12, az + dz, PB)
    for dx in range(-3, 4):
        cv.fill(ax + dx, y + 1, az + 32, ax + dx, y + 7, az + 32, "minecraft:iron_bars")
    for dx in (-4, 4):
        for dz in range(31, 34):
            cv.fill(ax + dx, y + 1, az + dz, ax + dx, y + 12, az + dz, DS)
    # corner towers
    for (sx, sz) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        tx, tz = ax + sx * 33, az + sz * 33
        for h in range(1, 28):
            cv.disc(tx, tz, 5, y + h, PB, r_in=4) if h < 27 else None
        for h in range(0, 27):
            cv.disc(tx, tz, 3, y + h + 1, "air") if False else None
        cv.disc(tx, tz, 5, y + 20, DS)
        cv.disc(tx, tz, 5, y + 27, "minecraft:polished_blackstone_brick_slab[type=bottom]")
        cv.disc(tx, tz, 6, y + 27, "minecraft:polished_blackstone_brick_slab[type=bottom]", r_in=6)
        for h, rr in ((28, 4), (29, 3), (30, 2), (31, 1)):
            cv.disc(tx, tz, rr, y + h, "minecraft:blackstone_slab[type=bottom]" if False else "minecraft:blackstone")
        cv.fill(tx, y + 32, tz, tx, y + 36, tz, "minecraft:iron_bars") if False else cv.fill(tx, y + 32, tz, tx, y + 34, tz, "minecraft:lightning_rod")
        cv.set(tx, y + 20 + 1, tz + (0), lantern(False)) if False else None
        cv.set(tx + sx * 4, y + 22, tz, "minecraft:light_gray_wool")   # wind flags
        cv.set(tx + sx * 5, y + 22, tz, "minecraft:white_wool")
        cv.set(tx + sx * 5, y + 21, tz, "minecraft:white_wool")
        cv.fill(tx - 1, y + 1, tz - 1, tx + 1, y + 18, tz + 1, "air") if False else None
    # keep: center (ax, az-14)
    kx, kz = ax, az - 14
    KH = 30
    cv.box(kx - 10, y + 1, kz - 10, kx + 10, y + KH, kz + 10, PB, inner="air", roof=False, floor=False)
    cv.fill(kx - 10, y + 15, kz - 10, kx + 10, y + 15, kz + 10, DS)          # mid floor
    cv.fill(kx - 3, y + 15, kz - 3, kx + 3, y + 15, kz + 3, "air")           # stair well
    cv.fill(kx - 10, y + KH, kz - 10, kx + 10, y + KH, kz + 10, DS)          # roof/arena floor
    for yy in range(1, KH):
        for xx in (kx - 10, kx + 10):
            if yy % 5 == 0:
                cv.fill(xx, y + yy, kz - 10, xx, y + yy, kz + 10, "minecraft:chiseled_polished_blackstone")
    # keep entrance (south wall), windows
    cv.fill(kx - 2, y + 1, kz + 10, kx + 2, y + 6, kz + 10, "air")
    put_door(cv, kx, y + 1, kz + 10, "south", "iron") if False else None
    for yy in (y + 8, y + 20):
        for xx in range(kx - 8, kx + 9, 4):
            cv.set(xx, yy, kz + 10, "minecraft:iron_bars"); cv.set(xx, yy, kz - 10, "minecraft:iron_bars")
    # interior spiral: stairs around the well, ladders as fallback
    for i in range(14):
        ang = i * (2 * np.pi / 14)
        sx_, sz_ = int(round(kx + 5 * np.cos(ang))), int(round(kz + 5 * np.sin(ang)))
        cv.set(sx_, y + 1 + i, sz_, "minecraft:polished_blackstone")
        cv.fill(sx_, y + 1, sz_, sx_, y + i, sz_, "minecraft:polished_blackstone") if False else None
    for i in range(15, 30):
        ang = i * (2 * np.pi / 15)
        sx_, sz_ = int(round(kx + 5 * np.cos(ang))), int(round(kz + 5 * np.sin(ang)))
        cv.set(sx_, y + 1 + i, sz_, "minecraft:polished_blackstone")
    # ladder shaft as a reliable route
    lx, lz = kx + 8, kz - 8
    cv.fill(lx, y + 1, lz, lx, y + KH - 1, lz, "minecraft:ladder[facing=south]")
    cv.fill(lx, y + 1, lz - 1, lx, y + KH - 1, lz - 1, "minecraft:polished_blackstone") if False else None
    cv.fill(lx, y + 15, lz, lx, y + 15, lz, "air")
    cv.fill(lx, y + KH, lz, lx, y + KH, lz, "air")
    for yy in range(3, KH, 6):
        cv.set(kx, y + yy, kz - 9, lantern(False)) if False else cv.set(kx + 2, y + yy, kz - 8, "minecraft:soul_lantern[hanging=false]") if False else None
    for xx in (kx - 6, kx + 6):
        for zz in (kz - 6, kz + 6):
            for yy in (5, 20):
                cv.set(xx, y + yy, zz, "minecraft:soul_lantern[hanging=false]") if False else cv.set(xx, y + yy, zz, lantern(False))
    cv.chest(kx - 7, y + 1, kz - 7, "east", "nahas:chests/rare")
    cv.chest(kx + 7, y + 16, kz - 7, "west", "nahas:chests/epic")
    # arena on the roof: wide disc r=16 with railing
    cv.disc(kx, kz, 16, y + KH, "minecraft:polished_blackstone", pat=lambda dx, dz: "minecraft:polished_blackstone" if (abs(dx) // 3 + abs(dz) // 3) % 2 else "minecraft:smooth_basalt")
    cv.disc(kx, kz, 16, y + KH - 1, DS)
    cv.disc(kx, kz, 16, y + KH + 1, PB, r_in=16)
    for k in range(0, 16):
        a = k * np.pi / 8
        x, z = int(round(kx + 16 * np.cos(a))), int(round(kz + 16 * np.sin(a)))
        cv.fill(x, y + KH + 1, z, x, y + KH + 3, z, PB)
        cv.set(x, y + KH + 4, z, lantern(False)) if k % 2 == 0 else None
    cv.disc(kx, kz, 3, y + KH, "minecraft:gilded_blackstone")
    W.feat("t4", arena_center=(kx, y + KH + 1, kz), arena_radius=15, keep_door=(kx, y + 1, kz + 10), keep_center=(kx, y + 1, kz))
    # parkour spiral around the keep (radius 14.5), rising to the roof edge
    plat = []
    n = 26
    for i in range(n):
        ang = np.pi / 2 + i * (2 * np.pi * 2.0 / n)      # two full turns starting south
        rr = 14.0
        px_, pz_ = int(round(kx + rr * np.cos(ang))), int(round(kz + rr * np.sin(ang)))
        py = y + 2 + int(i * (KH - 2) / (n - 1))
        m = ["minecraft:basalt[axis=y]", "minecraft:blackstone", "minecraft:smooth_basalt", "minecraft:polished_blackstone"][i % 4]
        cv.fill(px_, py, pz_, px_ + 1, py, pz_ + 1, m)
        plat.append((px_, py + 1, pz_))
        if i % 5 == 0:
            cv.fill(px_, y, pz_, px_, py - 1, pz_, "minecraft:blackstone") if False else None
            cv.set(px_, py + 1, pz_, "minecraft:white_wool") if False else None
        if i % 4 == 0:
            cv.fill(px_, py + 1, pz_, px_, py + 3, pz_, "minecraft:iron_bars")
            cv.set(px_, py + 4, pz_, "minecraft:white_banner[rotation=%d]" % (i % 16)) if False else cv.set(px_, py + 4, pz_, "minecraft:white_wool")
    cv.fill(kx + 14, y + KH - 1, kz, kx + 15, y + KH - 1, kz + 1, PB) if False else None
    W.feat("t4", parkour_start=plat[0], parkour_platforms=plat)
    # wind gauge: white pinwheel on tower tops (decor)
    cv.sign(ax + 4, y + 1, az + 36 if False else az + 26, ["قلعة", "الريح", "اصعد إلى القمة", ""], "south", wall=False, mat="dark_oak")
    W.poi("t4", p["ar"], ax, y, az, "main", plaza=64)


def build_star(W):
    p = W.main("g_star")
    ax, az, y = p["x"], p["z"], p["y"]
    cv = W.canvas("g_star", ax - 44, y - 6, az - 44, ax + 45, y + 26, az + 45)
    rnd = np.random.default_rng(7)
    for dz in range(-38, 39):
        for dx in range(-38, 39):
            d = np.hypot(dx, dz)
            b = None
            if d <= 16:
                ang = np.arctan2(dz, dx)
                star = abs(np.cos(4 * ang))       # 8-point star
                if d < 2.6:
                    b = "minecraft:light_blue_concrete"
                elif d <= 5 + 10 * star ** 3:
                    b = "minecraft:purple_concrete" if d > 8 else "minecraft:magenta_concrete"
                    if star > 0.93 and d > 12:
                        b = "minecraft:light_blue_concrete"
                else:
                    b = "minecraft:polished_deepslate" if (dx + dz) % 2 else "minecraft:deepslate_tiles"
            elif d <= 22:
                b = "minecraft:deepslate_bricks" if (dx // 2 + dz // 2) % 2 else "minecraft:polished_deepslate"
                if 20.5 <= d < 22:
                    b = "minecraft:cyan_terracotta"
            elif max(abs(dx), abs(dz)) <= 38:
                b = "minecraft:smooth_basalt" if rnd.random() < 0.55 else "minecraft:blackstone"
                if rnd.random() < 0.02:
                    b = "minecraft:amethyst_block"
            if b and (dx or dz):
                cv.set(ax + dx, y, az + dz, b)
    # 8 obelisks around
    for k in range(8):
        a = k * np.pi / 4
        x, z = int(round(ax + 22 * np.cos(a))), int(round(az + 22 * np.sin(a)))
        cv.fill(x, y + 1, z, x, y + 9, z, "minecraft:polished_deepslate")
        cv.fill(x, y + 1, z, x, y + 2, z, "minecraft:cut_copper") if False else None
        cv.set(x, y + 10, z, "minecraft:sea_lantern")
        cv.set(x, y + 11, z, "minecraft:end_rod[facing=up]")
        cv.set(x + 1, y + 1, z, "minecraft:amethyst_cluster[facing=up]") if False else None
    # portal arch to the north (z-16)
    gx, gz = ax, az - 17
    cv.fill(gx - 4, y + 1, gz - 1, gx - 4, y + 10, gz + 1, "minecraft:obsidian")
    cv.fill(gx + 4, y + 1, gz - 1, gx + 4, y + 10, gz + 1, "minecraft:obsidian")
    cv.fill(gx - 4, y + 11, gz - 1, gx + 4, y + 11, gz + 1, "minecraft:obsidian")
    cv.fill(gx - 3, y + 10, gz - 1, gx + 3, y + 10, gz + 1, "minecraft:obsidian")
    for yy in (y + 3, y + 6, y + 9):
        cv.set(gx - 4, yy, gz + 2, "minecraft:crying_obsidian"); cv.set(gx + 4, yy, gz + 2, "minecraft:crying_obsidian")
    cv.set(gx - 3, y + 9, gz + 1, "minecraft:crying_obsidian"); cv.set(gx + 3, y + 9, gz + 1, "minecraft:crying_obsidian")
    cv.fill(gx - 3, y + 1, gz - 1, gx + 3, y + 9, gz + 1, "air")
    cv.fill(gx - 3, y + 1, gz - 2, gx + 3, y + 9, gz - 2, "minecraft:black_stained_glass")
    for yy in range(y + 2, y + 9, 2):
        for xx in range(gx - 2, gx + 3, 2):
            cv.set(xx, yy, gz - 3, "minecraft:sea_lantern") if False else None
    cv.fill(gx - 4, y, gz - 2, gx + 4, y, gz + 1, "minecraft:cut_copper") if False else cv.fill(gx - 5, y, gz - 2, gx + 5, y, gz + 1, "minecraft:polished_blackstone")
    for xx in (gx - 6, gx + 6):
        cv.fill(xx, y + 1, gz, xx, y + 5, gz, "minecraft:polished_deepslate")
        cv.set(xx, y + 6, gz, "minecraft:sea_lantern")
    # amethyst crystal cluster decorations
    for (x, z) in scatter(rnd, ax, az, 24, 36, 10, sep=5):
        cv.set(x, y + 1, z, "minecraft:amethyst_cluster[facing=up]")
        if rnd.random() < 0.5:
            cv.set(x, y + 2, z, "minecraft:budding_amethyst") if False else cv.set(x, y + 2, z, "minecraft:amethyst_cluster[facing=up]")
    W.feat("g_star", portal=(gx, y + 1, gz + 0), portal_interior=[(gx - 3, y + 1, gz), (gx + 3, y + 9, gz)], dais=(ax, y, az),
           dimension="nahas:star_sea", dim_arrival=(600, 101, 600))
    W.poi("g_star", p["ar"], ax, y, az, "main", plaza=76)


def build_ember(W):
    p = W.main("g_ember")
    ax, az, y = p["x"], p["z"], p["y"]
    cv = W.canvas("g_ember", ax - 44, y - 16, az - 44, ax + 45, y + 24, az + 45)
    rnd = np.random.default_rng(8)
    for dz in range(-38, 39):
        for dx in range(-38, 39):
            d = np.hypot(dx, dz)
            r = rnd.random()
            b = "minecraft:blackstone" if r < 0.5 else ("minecraft:basalt[axis=y]" if r < 0.8 else ("minecraft:magma_block" if r < 0.87 else "minecraft:smooth_basalt"))
            if d < 9:
                b = "minecraft:polished_blackstone_bricks" if (dx + dz) % 2 else "minecraft:polished_blackstone"
            if dx or dz:
                cv.set(ax + dx, y, az + dz, b)
    # fissure across x at z = az-14 (lava top y-1, contained)
    fz = az - 14
    for dz in range(-3, 4):
        for dx in range(-30, 31):
            wdt = 2 + int(1.2 * np.sin(dx / 4.0)) if abs(dx) > 3 else 0
            if abs(dz) <= wdt and abs(dx) > 3:
                cv.fill(ax + dx, y - 12, fz + dz, ax + dx, y - 2, fz + dz, "minecraft:lava")
                cv.set(ax + dx, y - 13, fz + dz, "minecraft:obsidian")
                cv.set(ax + dx, y - 1, fz + dz, "minecraft:lava")
                cv.set(ax + dx, y, fz + dz, "air") if False else None
                cv.set(ax + dx, y, fz + dz, "minecraft:lava")
            elif abs(dz) == wdt + 1 and abs(dx) > 3:
                cv.set(ax + dx, y, fz + dz, "minecraft:obsidian")
    # the y level of lava is `y` -> keep 1 below by capping with obsidian rims at same level (rims flush) -- fine
    # obsidian bridge (x within +-3)
    for dx in range(-3, 4):
        for dz in range(-5, 6):
            cv.set(ax + dx, y, fz + dz, "minecraft:polished_blackstone_bricks")
    # shrine platform north of the fissure
    sz_ = az - 26
    for dz in range(-8, 9):
        for dx in range(-14, 15):
            cv.set(ax + dx, y, sz_ + dz, "minecraft:polished_blackstone_bricks" if (dx + dz) % 2 else "minecraft:nether_bricks")
    # portal arch (fiery)
    gx, gz = ax, sz_ - 3
    for dx in (-3, 3):
        cv.fill(gx + dx, y + 1, gz, gx + dx, y + 8, gz + 1, "minecraft:crying_obsidian")
    cv.fill(gx - 3, y + 9, gz, gx + 3, y + 9, gz + 1, "minecraft:crying_obsidian")
    cv.fill(gx - 2, y + 1, gz, gx + 2, y + 8, gz + 1, "air")
    cv.fill(gx - 2, y + 1, gz - 1, gx + 2, y + 8, gz - 1, "minecraft:red_stained_glass")
    for dx in (-3, 3):
        cv.fill(gx + dx, y + 1, gz + 2, gx + dx, y + 3, gz + 2, "minecraft:red_nether_bricks")
        cv.set(gx + dx * 2 // 1 if False else gx + dx, y + 10, gz, "minecraft:soul_lantern[hanging=false]") if False else None
    for dx in (-8, 8):
        cv.fill(ax + dx, y + 1, sz_, ax + dx, y + 6, sz_, "minecraft:nether_bricks")
        cv.set(ax + dx, y + 7, sz_, "minecraft:campfire[lit=true,facing=north]")
        cv.set(ax + dx, y + 8, sz_, "minecraft:soul_torch") if False else None
    # scattered basalt columns and magma
    for (x, z) in scatter(rnd, ax, az, 12, 36, 14, sep=5):
        if abs(z - fz) < 6:
            continue
        cv.fill(x, y + 1, z, x, y + int(rnd.integers(2, 8)), z, "minecraft:basalt[axis=y]")
    for k in range(8):
        a = k * np.pi / 4 + 0.3
        x, z = int(round(ax + 26 * np.cos(a))), int(round(az + 26 * np.sin(a)))
        if abs(z - fz) < 6 or abs(z - sz_) < 10:
            continue
        cv.fill(x, y + 1, z, x, y + 4, z, "minecraft:polished_blackstone_bricks")
        cv.set(x, y + 5, z, "minecraft:soul_campfire[lit=true,facing=north]")
    cv.sign(ax + 3, y + 1, az + 4, ["بوابة", "الجمر", "الحمم تحت الجسر", ""], "south", wall=False, mat="crimson")
    W.feat("g_ember", portal=(gx, y + 1, gz), bridge=(ax, y + 1, fz), fissure_z=fz, dimension="nahas:ember", dim_arrival=(500, 65, 500))
    W.poi("g_ember", p["ar"], ax, y, az, "main", plaza=76)
