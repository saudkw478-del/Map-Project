"""Extra POIs: minor oases, waystations, ruins, tombs, buried temples, lore stones, watchtowers, shipwrecks, salt mirror,
fossil skeleton and lighthouse."""
import numpy as np
from poi_defs import *
from wg_core import Canvas, B
from shapes import *
from pois_a import scatter
import terrain as TR

RUINS = [(900, 700, "أطلال الفجر"), (1450, 1420, "أطلال الحداد"), (2250, 1520, "أطلال القافلة الضائعة"), (250, 1500, "أطلال المنارة القديمة"),
         (1400, 600, "أطلال الحارس"), (800, 2080, "أطلال السوق المنسي"), (1600, 2100, "أطلال قصر الرمل")]
TOMBS = [(1050, 780, "مقبرة الملك الأول"), (1900, 1120, "مقبرة الأميرة"), (520, 1100, "مقبرة الصائغ"), (2000, 2100, "مقبرة الجني الصغير"), (700, 330, "مقبرة العرّاف")]
BURIED = [(1250, 1650, "المدخل المدفون الأول"), (1600, 1500, "المدخل المدفون الثاني"), (300, 1300, "المدخل المدفون الثالث")]
LORE = [(800, 1500, "حجر الحكاية الأول"), (1300, 980, "حجر الحكاية الثاني"), (1880, 560, "حجر الحكاية الثالث"), (600, 1980, "حجر الحكاية الرابع"),
        (2000, 1730, "حجر الحكاية الخامس")]
LORE_TEXT = [["قالوا: مدينة", "من نحاس لا", "يدخلها إلا", "من جمع الأختام"], ["كل ليلة تصحو", "المدينة وتنام", "في الفجر من", "جديد"],
             ["الفانوس يعرف", "طريقه إلى", "القلب الشجاع", ""], ["سبعة أختام", "وسبع تجارب", "وحارس واحد", ""], ["من ضحك في", "الظلام نجا", "منه", ""]]
TOWERS = [(1100, 1500, "برج المراقبة الجنوبي"), (1700, 1620, "برج القافلة"), (800, 900, "برج الغروب"), (1400, 700, "برج الملح")]
SALT_MIRROR = (1560, 950, "مرآة الملح")
FOSSIL = (700, 1250, "عظام العملاق")
LIGHTHOUSE = (42, 1750, "منارة البحر")
SHIP_TARGETS = [(60, 1250, "حطام السفينة الحمراء"), (60, 1950, "حطام سفينة الريح"), (700, 2340, "حطام سفينة اللؤلؤ"), (1500, 2340, "حطام الجنية")]


def flatten_site(T, x, z, half, h=None, blend=8):
    """Flatten terrain to local median (or h) around a site; returns ground y."""
    x0, x1, z0, z1 = max(0, x - half), min(N, x + half + 1), max(0, z - half), min(N, z + half + 1)
    if h is None:
        h = int(np.median(T.H[z0:z1, x0:x1]))
    h = max(h, 66)
    H = T.H.astype(np.float32)
    TR.apply_pad(H, "sq", x, z, half, float(h), blend)
    T.H = np.round(H).astype(np.int16)
    return h


def plan_extras(T, W):
    sites = []
    for name, lst in (("ruin", RUINS), ("tomb", TOMBS), ("buried", BURIED), ("lore", LORE), ("tower", TOWERS)):
        for i, (x, z, ar) in enumerate(lst):
            half = {"ruin": 16, "tomb": 14, "buried": 12, "lore": 5, "tower": 8}[name]
            if T.water[z, x] >= 0 or T.dsea[z, x] < 40:
                print("WARN site in water", name, x, z)
            y = flatten_site(T, x, z, half)
            sites.append(dict(kind=name, id=f"{name}_{i + 1}", ar=ar, x=x, z=z, y=y, idx=i))
    # oasis surroundings: shore level for props
    x, z, ar = SALT_MIRROR
    y = flatten_site(T, x, z, 24, h=66, blend=10)
    sites.append(dict(kind="salt_mirror", id="salt_mirror", ar=ar, x=x, z=z, y=y, idx=0))
    x, z, ar = FOSSIL
    y = flatten_site(T, x, z, 30)
    sites.append(dict(kind="fossil", id="fossil", ar=ar, x=x, z=z, y=y, idx=0))
    # waystations along roads
    stations = []
    main_pts = [(p["x"], p["z"]) for p in MAIN]
    acc = 0
    for name, (pl, prof) in T.road_samples.items():
        dist = 0.0
        nxt = ROUTE_STATION_SPACING * 0.5
        for i in range(1, len(pl)):
            dist += np.hypot(*(pl[i] - pl[i - 1]))
            if dist >= nxt:
                nxt += ROUTE_STATION_SPACING
                x, z = pl[i]
                if any(np.hypot(x - mx, z - mz) < 110 for mx, mz in main_pts):
                    continue
                if any(np.hypot(x - sx, z - sz) < 120 for sx, sz in stations):
                    continue
                if T.water[int(z), int(x)] >= 0:
                    continue
                # pad beside the road (perpendicular offset 9)
                t = pl[min(i + 3, len(pl) - 1)] - pl[i - 3]
                t /= np.linalg.norm(t) + 1e-9
                sx_, sz_ = int(x - t[1] * 11), int(z + t[0] * 11)
                if T.water[sz_, sx_] >= 0:
                    sx_, sz_ = int(x + t[1] * 11), int(z - t[0] * 11)
                y = flatten_site(T, sx_, sz_, 9, h=int(prof[i]) if False else None)
                stations.append((sx_, sz_))
                sites.append(dict(kind="waystation", id=f"waystation_{len(stations)}", ar=f"محطة القافلة {len(stations)}", x=sx_, z=sz_, y=y, idx=len(stations), road=(int(x), int(z))))
    return sites


# ------------------------------------------------------------------- builders

def b_minor_oasis(W, T, i, x, z, r, ar, gr):
    rnd = np.random.default_rng(100 + i)
    y = 70
    cv = W.canvas(f"oasis_{i}", x - gr - 4, 60, z - gr - 4, x + gr + 5, 92, z + gr + 5)
    cnt = 0
    for k in range(int(gr * 0.45)):
        a = rnd.random() * 2 * np.pi
        d = r + 3 + rnd.random() * (gr - r - 6)
        px, pz = int(x + d * np.cos(a)), int(z + d * np.sin(a))
        if T.water[pz, px] >= 0 or not T.grass[pz, px]:
            continue
        palm(cv, px, int(T.H[pz, px]), pz, int(rnd.integers(5, 10)), rnd)
        cnt += 1
    for k in range(int(gr * 0.6)):   # reeds and bushes on the shore
        a = rnd.random() * 2 * np.pi
        d = r + 1 + rnd.random() * 5
        px, pz = int(x + d * np.cos(a)), int(z + d * np.sin(a))
        if T.water[pz, px] >= 0:
            continue
        hy = int(T.H[pz, px])
        for j in range(1, int(rnd.integers(2, 4))):
            cv.set(px, hy + j, pz, "minecraft:sugar_cane[age=0]") if hy < 71 and False else cv.set(px, hy + j, pz, "minecraft:jungle_leaves[persistent=true,distance=1]") if j == 1 and rnd.random() < 0.3 else None
    # tiny camp: tent + campfire + chest
    a = rnd.random() * 2 * np.pi
    tx, tz = int(x + (r + 12) * np.cos(a)), int(z + (r + 12) * np.sin(a))
    ty = int(T.H[tz, tx])
    if T.water[tz, tx] < 0 and abs(int(T.H[tz + 3, tx + 3]) - ty) <= 2:
        cv.fill(tx - 4, ty, tz - 4, tx + 4, ty, tz + 4, "minecraft:grass_block[snowy=false]") if T.grass[tz, tx] else None
        tent(cv, tx, ty, tz, 5, 5, ["red", "blue", "orange", "yellow"][i % 4], False, rnd)
        cv.chest(tx + 1, ty + 1, tz, "south", "nahas:chests/oasis")
        cv.set(tx + 5, ty + 1, tz, "minecraft:campfire[lit=true,facing=north]")
    W.poi(f"oasis_{i}", ar, x, 69, z, "minor_oasis", palms=cnt, pond_radius=r, note="y = pond water surface block")


def b_waystation(W, T, s):
    x, z, y = s["x"], s["z"], s["y"]
    rnd = np.random.default_rng(200 + s["idx"])
    cv = W.canvas(s["id"], x - 10, y - 4, z - 10, x + 11, y + 14, z + 11)
    cv.fill(x - 8, y, z - 8, x + 8, y, z + 8, "minecraft:cut_sandstone") if False else None
    for dz in range(-8, 9):
        for dx in range(-8, 9):
            cv.set(x + dx, y, z + dz, "minecraft:cobblestone" if rnd.random() < 0.2 else ("minecraft:gravel" if rnd.random() < 0.5 else "minecraft:coarse_dirt"))
    well(cv, x - 4, y, z - 4)
    tent(cv, x + 3, y, z - 3, 7, 5, ["red", "orange", "yellow", "blue"][s["idx"] % 4], False, rnd)
    cv.chest(x + 3, y + 1, z - 3, "south", "nahas:chests/common")
    cv.set(x, y + 1, z + 3, "minecraft:campfire[lit=true,facing=north]")
    for dx in (-2, 2):
        cv.set(x + dx, y + 1, z + 3, stair("oak", "west" if dx > 0 else "east"))
    cv.fill(x - 6, y + 1, z + 5, x - 6, y + 4, z + 5, "minecraft:oak_fence")
    cv.set(x - 6, y + 5, z + 5, lantern(False)) if False else cv.set(x - 6, y + 5, z + 5, "minecraft:lantern[hanging=false]")
    cv.sign(x - 6, y + 4, z + 6, ["محطة", "القافلة", str(s["idx"]), ""], "south", wall=True)
    cv.fill(x + 5, y + 1, z + 5, x + 6, y + 1, z + 5, "minecraft:hay_block")
    cv.barrel(x + 6, y + 2, z + 5, "nahas:chests/common")
    W.poi(s["id"], s["ar"], x, y, z, "waystation", road=s["road"])


def b_ruin(W, T, s):
    x, z, y = s["x"], s["z"], s["y"]
    rnd = np.random.default_rng(300 + s["idx"])
    cv = W.canvas(s["id"], x - 20, y - 6, z - 20, x + 21, y + 16, z + 21)
    mats = ["minecraft:sandstone", "minecraft:cut_sandstone", "minecraft:mossy_cobblestone", "minecraft:cracked_stone_bricks", "minecraft:stone_bricks"]
    mats = [m for m in mats if True]
    ruin_wall(cv, x - 12, z - 10, x + 12, z - 10, y, 6, mats, rnd)
    ruin_wall(cv, x - 12, z + 10, x + 12, z + 10, y, 5, mats, rnd, 0.35)
    ruin_wall(cv, x - 12, z - 10, x - 12, z + 10, y, 6, mats, rnd)
    ruin_wall(cv, x + 12, z - 10, x + 12, z + 10, y, 4, mats, rnd, 0.4)
    for (px, pz) in ((x - 6, z - 4), (x + 6, z - 4), (x - 6, z + 4), (x + 6, z + 4)):
        h = int(rnd.integers(3, 9))
        cv.fill(px, y + 1, pz, px, y + h, pz, "minecraft:chiseled_sandstone" if h % 2 else "minecraft:cut_sandstone")
    for dz in range(-9, 10):
        for dx in range(-11, 12):
            if rnd.random() < 0.55:
                cv.set(x + dx, y, z + dz, mats[int(rnd.integers(0, len(mats)))])
    cv.fill(x - 3, y, z - 3, x + 3, y, z + 3, "minecraft:chiseled_sandstone")
    cv.fill(x + 2, y + 1, z + 2, x + 2, y + 1, z + 2, "minecraft:cut_sandstone")
    cv.chest(x + 2, y + 2, z + 2, ["south", "east", "west", "north"][s["idx"] % 4], "nahas:chests/ruins")
    cv.chest(x + 8, y + 1, z + 7, "west", "nahas:chests/ruins", trapped=True) if s["idx"] % 2 == 0 else None
    for k in range(6):
        cv.set(x + int(rnd.integers(-10, 11)), y + 1, z + int(rnd.integers(-8, 9)), "minecraft:cobweb")
    cv.sign(x, y + 1, z + 4, [s["ar"][:14], "", "", ""], "south", wall=False)
    W.poi(s["id"], s["ar"], x, y, z, "ruin", loot="nahas:chests/ruins")


def b_tomb(W, T, s):
    x, z, y = s["x"], s["z"], s["y"]
    rnd = np.random.default_rng(400 + s["idx"])
    cv = W.canvas(s["id"], x - 14, y - 22, z - 24, x + 15, y + 12, z + 18)
    zc = z - 7            # chamber centre (chamber lies north-west of the ramp start, below the mound)
    # surface pyramid mound
    for h in range(0, 6):
        cv.fill(x - 6 + h, y + 1 + h, z - 6 + h - 7, x + 6 - h, y + 1 + h, z + 6 - h - 7, "minecraft:sandstone" if h % 2 else "minecraft:cut_sandstone")
    cy = y - 13
    cv.box(x - 7, cy, zc - 7, x + 7, cy + 6, zc + 7, "minecraft:sandstone", inner="air")
    # ramp: from the surface at z+13 descending north into the chamber's south wall at zc+7 = z
    for i in range(14):
        zz = z + 13 - i
        yy = y - i
        cv.fill(x - 1, yy + 1, zz, x + 1, yy + 4, zz, "air")
        cv.fill(x - 1, yy, zz, x + 1, yy, zz, "minecraft:sandstone")
        cv.set(x - 2, yy + 1, zz, "minecraft:sandstone"); cv.set(x + 2, yy + 1, zz, "minecraft:sandstone")
    cv.fill(x - 1, cy + 1, zc + 7, x + 1, cy + 3, zc + 7, "air")
    for xx in range(x - 6, x + 7):
        for zz in range(zc - 6, zc + 7):
            cv.set(xx, cy, zz, "minecraft:cut_sandstone" if (xx + zz) % 2 else "minecraft:smooth_sandstone")
    for (dx, dz) in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        cv.fill(x + dx, cy + 1, zc + dz, x + dx, cy + 5, zc + dz, "minecraft:chiseled_sandstone")
        cv.set(x + dx, cy + 5, zc + dz + (1 if dz < 0 else -1), "minecraft:wall_torch[facing=%s]" % ("south" if dz < 0 else "north"))
    cv.fill(x - 2, cy + 1, zc - 4, x + 2, cy + 1, zc - 4, "minecraft:cut_sandstone")
    cv.fill(x - 1, cy + 2, zc - 4, x + 1, cy + 2, zc - 4, "minecraft:quartz_slab[type=bottom]")
    cv.chest(x, cy + 1, zc - 6, "south", "nahas:chests/tomb")
    cv.chest(x - 5, cy + 1, zc, "east", "nahas:chests/tomb", trapped=(s["idx"] % 2 == 0))
    for k in range(5):
        cv.set(x + int(rnd.integers(-5, 6)), cy + 1, zc + int(rnd.integers(-5, 6)), "minecraft:cobweb")
    cv.set(x + 2, cy + 1, zc + 2, "minecraft:skeleton_skull[rotation=4]")
    cv.sign(x + 3, y + 1, z + 13, ["مقبرة", "لا تزعج", "الراقدين", ""], "south", wall=False)
    W.poi(s["id"], s["ar"], x, y, z + 13, "tomb", loot="nahas:chests/tomb", chamber=(x, cy + 1, zc), mound=(x, y + 1, zc),
          note="anchor = top of the entrance ramp (ground level)")


def b_buried(W, T, s):
    x, z, y = s["x"], s["z"], s["y"]
    rnd = np.random.default_rng(500 + s["idx"])
    cv = W.canvas(s["id"], x - 10, y - 14, z - 10, x + 11, y + 10, z + 21)
    # sand drifts covering a temple top; only the lintel and columns poke out
    for dz in range(-8, 9):
        for dx in range(-8, 9):
            d = max(abs(dx), abs(dz))
            hh = int(3.5 - d / 2.5 + rnd.random())
            if hh > 0:
                cv.fill(x + dx, y + 1, z + dz, x + dx, y + hh, z + dz, "minecraft:sand")
    cv.fill(x - 3, y + 1, z - 1, x + 3, y + 3, z - 1, "minecraft:cut_sandstone")
    cv.fill(x - 1, y + 1, z - 1, x + 1, y + 2, z - 1, "air")
    cv.fill(x - 3, y + 4, z - 1, x + 3, y + 4, z - 1, "minecraft:chiseled_sandstone")
    for k in (-3, 3):
        cv.fill(x + k, y + 1, z - 2, x + k, y + 5, z - 2, "minecraft:sandstone_wall") if False else cv.fill(x + k, y + 1, z - 2, x + k, y + 6, z - 2, "minecraft:cut_sandstone")
    # entrance corridor down to a small vault
    for i in range(8):
        cv.fill(x - 1, y - i, z + i * 0 - 1 + 1 if False else z, x + 1, y - i + 2, z, "air") if False else None
    for i in range(9):
        cv.fill(x - 1, y - i + 1, z - 1 + 0, x + 1, y - i + 3, z - 1 + 0, "air") if False else None
    cy = y - 9
    for i in range(9):
        zz = z + i
        cv.fill(x - 1, y - i, zz, x + 1, y - i + 2, zz, "air")
        cv.fill(x - 1, y - i - 1, zz, x + 1, y - i - 1, zz, "minecraft:sandstone")
        cv.set(x - 2, y - i, zz, "minecraft:sandstone"); cv.set(x + 2, y - i, zz, "minecraft:sandstone")
    cv.box(x - 4, cy - 1, z + 9, x + 4, cy + 4, z + 17, "minecraft:cut_sandstone", inner="air")
    cv.fill(x - 1, cy, z + 9, x + 1, cy + 2, z + 9, "air")
    cv.chest(x, cy, z + 15, "north", "nahas:chests/tomb")
    cv.set(x - 3, cy + 1, z + 16, "minecraft:wall_torch[facing=south]") if False else cv.set(x - 3, cy, z + 16, "minecraft:torch")
    cv.set(x + 3, cy, z + 16, "minecraft:torch")
    cv.set(x, cy - 1, z + 13, "minecraft:suspicious_sand") if False else None
    W.poi(s["id"], s["ar"], x, cy - 1, z + 14, "buried_temple", loot="nahas:chests/tomb", vault=(x, cy, z + 15), surface_entrance=(x, y, z), note="anchor = vault floor; entrance buried under sand at surface_entrance")


def b_lore(W, T, s):
    x, z, y = s["x"], s["z"], s["y"]
    cv = W.canvas(s["id"], x - 5, y - 2, z - 5, x + 6, y + 10, z + 6)
    cv.fill(x - 1, y, z - 1, x + 1, y, z + 1, "minecraft:smooth_stone") if False else cv.fill(x - 2, y, z - 2, x + 2, y, z + 2, "minecraft:polished_andesite")
    cv.fill(x, y + 1, z, x, y + 5, z, "minecraft:polished_blackstone")
    cv.fill(x - 1, y + 1, z, x + 1, y + 2, z, "minecraft:polished_blackstone") if False else None
    cv.set(x, y + 6, z, "minecraft:chiseled_polished_blackstone")
    cv.set(x, y + 7, z, "minecraft:soul_lantern[hanging=false]")
    t = LORE_TEXT[s["idx"] % len(LORE_TEXT)]
    cv.sign(x, y + 3, z + 1, t, "south", wall=True)
    cv.sign(x, y + 3, z - 1, t, "north", wall=True)
    W.poi(s["id"], s["ar"], x, y, z, "lore_stone", text=" ".join(t))


def b_tower(W, T, s):
    x, z, y = s["x"], s["z"], s["y"]
    rnd = np.random.default_rng(600 + s["idx"])
    cv = W.canvas(s["id"], x - 8, y - 2, z - 8, x + 9, y + 30, z + 9)
    for yy in range(1, 17):
        cv.disc(x, z, 4, y + yy, "minecraft:stone_bricks" if yy % 5 else "minecraft:chiseled_stone_bricks", r_in=3)
    cv.disc(x, z, 4, y, "minecraft:stone_bricks")
    for yy in (5, 10):
        cv.disc(x, z, 3, y + yy, "minecraft:spruce_planks")
    cv.fill(x + 3, y + 1, z, x + 3, y + 2, z, "air")
    put_door(cv, x + 3, y + 1, z, "east", "spruce")
    for yy in range(1, 16):
        cv.set(x - 2, y + yy, z, "minecraft:ladder[facing=east]")
    cv.fill(x - 2, y + 5, z, x - 2, y + 5, z, "air"); cv.fill(x - 2, y + 10, z, x - 2, y + 10, z, "air")
    cv.disc(x, z, 5, y + 16, "minecraft:stone_brick_slab[type=bottom]" if False else "minecraft:stone_bricks")
    for k in range(16):
        a = k * np.pi / 8
        px, pz = int(round(x + 5 * np.cos(a))), int(round(z + 5 * np.sin(a)))
        cv.set(px, y + 17, pz, "minecraft:stone_bricks") if k % 2 == 0 else None
        cv.set(px, y + 17, pz, "minecraft:stone_brick_wall") if False else None
    cv.set(x, y + 17, z, "minecraft:campfire[lit=true,facing=north]")
    cv.chest(x + 1, y + 6, z + 1, "west", "nahas:chests/common")
    cv.set(x + 2, y + 11, z + 2, "minecraft:barrel[facing=up]")
    for yy in (3, 8, 13):
        cv.set(x, y + yy, z + 4 if False else z - 3, "minecraft:iron_bars") if False else None
    W.poi(s["id"], s["ar"], x, y, z, "watchtower", loot="nahas:chests/common")


def b_salt_mirror(W, T, s):
    x, z, y = s["x"], s["z"], s["y"]
    cv = W.canvas("salt_mirror", x - 26, y - 14, z - 26, x + 27, y + 10, z + 27)
    R_ = 18
    for dz in range(-R_, R_ + 1):
        for dx in range(-R_, R_ + 1):
            d = np.hypot(dx, dz)
            if d <= R_:
                cv.set(x + dx, y, z + dz, "minecraft:light_blue_stained_glass" if d < R_ - 1 else "minecraft:quartz_block")
    # room beneath the mirror
    cv.disc(x, z, R_, y - 1, "air")
    for yy in range(y - 8, y - 1):
        cv.disc(x, z, R_ - 1, yy, "air")
    cv.disc(x, z, R_, y - 9, "minecraft:smooth_quartz")
    for yy in range(y - 8, y - 1):
        cv.disc(x, z, R_, yy, "minecraft:quartz_block", r_in=R_)
    for k in range(8):
        a = k * np.pi / 4
        px, pz = int(round(x + 12 * np.cos(a))), int(round(z + 12 * np.sin(a)))
        cv.fill(px, y - 8, pz, px, y - 2, pz, "minecraft:quartz_pillar[axis=y]")
        cv.set(px, y - 8 + 1, pz, "minecraft:sea_lantern") if False else None
    for k in range(6):
        a = k * np.pi / 3 + 0.3
        cv.set(int(round(x + 6 * np.cos(a))), y - 8, int(round(z + 6 * np.sin(a))), "minecraft:sea_lantern")
    cv.set(x, y - 8, z, "minecraft:gold_block")
    cv.fill(x - 1, y - 7, z - 1, x + 1, y - 7, z + 1, "minecraft:chiseled_quartz_block")
    cv.chest(x, y - 6, z, "south", "nahas:chests/epic")
    # hidden entrance: an ordinary-looking salt block with a trapdoor one tile from the north rim -> ladder
    ex, ez = x, z - R_ - 3
    cv.fill(ex, y - 9, ez, ex, y, ez, "air")
    cv.fill(ex, y - 9, z - R_ - 2, ex, y - 5, z - R_ + 1, "air") if False else None
    for yy in range(y - 8, y):
        cv.set(ex, yy, ez, "minecraft:ladder[facing=south]") if False else None
    cv.fill(ex - 1, y - 9, ez - 1, ex + 1, y - 9, ez + 1, "minecraft:quartz_block")
    cv.set(ex, y, ez, "minecraft:iron_trapdoor[facing=north,half=top,open=false]") if False else cv.set(ex, y, ez, "minecraft:calcite")
    # secret shaft: entrance = the calcite block at the north rim; break it, climb the ladder, tunnel leads under the mirror
    for yy in range(y - 8, y):
        cv.set(ex, yy, ez, "air")
    for yy in range(y - 8, y):
        cv.set(ex, yy, ez - 1, "minecraft:calcite") if False else None
    cv.fill(ex, y - 8, ez, ex, y - 2, ez, "minecraft:ladder[facing=south]")
    cv.fill(ex, y - 8, ez + 1, ex, y - 7, z - R_ + 1, "air")
    for zz in range(ez + 1, z - R_ + 2):
        cv.fill(ex - 1, y - 9, zz, ex + 1, y - 9, zz, "minecraft:quartz_block")
        cv.fill(ex - 1, y - 8, zz, ex + 1, y - 6, zz, "air")
    cv.set(ex, y, ez, "minecraft:calcite")
    cv.set(ex, y - 1, ez, "minecraft:iron_trapdoor[facing=south,half=bottom,open=false]") if False else None
    cv.sign(ex + 1, y + 1, ez, ["اكسر الملح", "حيث ينحني", "الظل", ""], "south", wall=False)
    W.poi("salt_mirror", s["ar"], x, y, z, "salt_mirror", secret_entrance=(ex, y, ez), chest=(x, y - 6, z))


def b_fossil(W, T, s):
    x, z, y = s["x"], s["z"], s["y"]
    rnd = np.random.default_rng(700)
    cv = W.canvas("fossil", x - 30, y - 2, z - 14, x + 31, y + 20, z + 15)
    BONE = "minecraft:bone_block"
    L = 44
    for i in range(-L // 2, L // 2 + 1):
        hgt = 1 + int(2 * np.cos(i / 9.0))
        cv.set(x + i, y + 2 + hgt, z, "minecraft:bone_block[axis=x]")
        cv.set(x + i, y + 1 + hgt, z, "minecraft:bone_block[axis=x]")
    for i in range(-16, 17, 3):
        hgt = 1 + int(2 * np.cos(i / 9.0))
        rad = 8 - abs(i) // 5
        for a in np.linspace(0.15, np.pi - 0.15, 18):
            for sgn in (-1, 1):
                px, pz = x + i, z + sgn * int(round(rad * np.sin(a)))
                py = y + 3 + hgt + int(round(rad * 0.9 * np.cos(a))) - 2
                cv.set(px, py, pz, "minecraft:bone_block[axis=y]")
    for i in range(L // 2, L // 2 + 8):
        cv.set(x + i, y + 2, z, "minecraft:bone_block[axis=x]")
    # skull (west)
    sx = x - L // 2 - 8
    cv.fill(sx, y + 2, z - 3, sx + 7, y + 6, z + 3, BONE)
    cv.fill(sx + 1, y + 3, z - 2, sx + 6, y + 5, z + 2, "air")
    cv.set(sx, y + 5, z - 2, "air"); cv.set(sx, y + 5, z + 2, "air")
    cv.fill(sx, y + 1, z - 3, sx + 2, y + 1, z + 3, "minecraft:bone_block[axis=z]") if False else None
    for zz in (-2, 0, 2):
        cv.set(sx, y + 2, z + zz, "minecraft:bone_block[axis=y]")
    cv.chest(sx + 4, y + 3, z, "east", "nahas:chests/ruins")
    W.poi("fossil", s["ar"], x, y, z, "fossil", chest=(sx + 4, y + 3, z))


def b_lighthouse(W, T):
    x, z, ar = LIGHTHOUSE
    y = int(T.H[z, x])
    rnd = np.random.default_rng(800)
    cv = W.canvas("lighthouse", x - 12, y - 4, z - 12, x + 13, y + 50, z + 13)
    cv.disc(x, z, 8, y, "minecraft:stone_bricks")
    for yy in range(1, 34):
        rr = 5 if yy < 20 else 4
        col = "minecraft:white_concrete" if (yy // 5) % 2 == 0 else "minecraft:red_concrete"
        cv.disc(x, z, rr, y + yy, col, r_in=rr - 1)
    for yy in range(1, 33):
        cv.set(x - 3, y + yy, z, "minecraft:ladder[facing=east]")
    cv.fill(x + 4, y + 1, z, x + 4, y + 2, z, "air")
    put_door(cv, x + 4, y + 1, z, "east", "spruce")
    for yy in (10, 20, 30):
        cv.disc(x, z, 4, y + yy, "minecraft:spruce_planks")
        cv.set(x - 3, y + yy, z, "air")
    cv.disc(x, z, 6, y + 34, "minecraft:stone_bricks")
    cv.disc(x, z, 6, y + 35, "minecraft:stone_brick_wall" if False else "minecraft:iron_bars", r_in=6)
    for yy in range(35, 39):
        cv.disc(x, z, 3, y + yy, "minecraft:glass", r_in=3)
    cv.sphere(x, y + 39, z, 3, "minecraft:red_concrete", thick=1, upper=True)
    cv.fill(x, y + 35, z, x, y + 37, z, "minecraft:sea_lantern")
    cv.set(x, y + 43, z, "minecraft:lightning_rod")
    cv.chest(x + 2, y + 1, z + 2, "west", "nahas:chests/ruins")
    W.poi("lighthouse", ar, x, y, z, "lighthouse")


def b_shipwrecks(W, T):
    rnd = np.random.default_rng(900)
    for i, (tx, tz, ar) in enumerate(SHIP_TARGETS):
        # find a spot with 3..8 blocks of water
        best = None
        for r in range(0, 200, 2):
            for a in np.linspace(0, 2 * np.pi, 24, endpoint=False):
                x, z = int(tx + r * np.cos(a)), int(tz + r * np.sin(a))
                if 20 <= x < N - 20 and 20 <= z < N - 20:
                    w = int(T.water[z, x])
                    if w >= 0 and 2 <= w - int(T.H[z, x]) <= 8 and all(T.water[zz, xx] >= 0 for zz in (z - 6, z + 6) for xx in (x - 6, x + 6)):
                        best = (x, z)
                        break
            if best:
                break
        if not best:
            print("WARN no shipwreck spot", ar)
            continue
        x, z = best
        yb = int(T.H[z, x])
        cv = W.canvas(f"ship_{i}", x - 12, yb - 3, z - 8, x + 13, yb + 14, z + 9)
        for k in range(-8, 9):
            half = max(1, 3 - abs(k) // 4)
            for s_ in range(-half, half + 1):
                cv.set(x + k, yb + 1, z + s_, "minecraft:dark_oak_planks")
            for s_ in (-half, half):
                for yy in range(2, 5 if abs(k) < 7 else 6):
                    if rnd.random() < 0.85:
                        cv.set(x + k, yb + yy, z + s_, "minecraft:dark_oak_planks" if yy < 4 else "minecraft:dark_oak_slab[type=bottom]")
        cv.fill(x + 8, yb + 2, z, x + 8, yb + 7, z, "minecraft:dark_oak_log[axis=y]") if False else None
        cv.fill(x - 1, yb + 2, z, x - 1, yb + 8, z, "minecraft:dark_oak_log[axis=y]")   # broken mast
        cv.chest(x + 4, yb + 2, z, "west", "nahas:chests/ruins")
        cv.chest(x - 4, yb + 2, z, "east", "nahas:chests/common")
        cv.set(x + 5, yb + 2, z + 1, "minecraft:barrel[facing=up]")
        W.poi(f"shipwreck_{i + 1}", ar, x, int(T.water[z, x]), z, "shipwreck", loot="nahas:chests/ruins")


def build_extras(W, T, sites):
    for i, (x, z, r, ar, gr) in enumerate(MINOR_OASES, 1):
        b_minor_oasis(W, T, i, x, z, r, ar, gr)
    for s in sites:
        {"waystation": b_waystation, "ruin": b_ruin, "tomb": b_tomb, "buried": b_buried, "lore": b_lore, "tower": b_tower,
         "salt_mirror": b_salt_mirror, "fossil": b_fossil}[s["kind"]](W, T, s)
    b_lighthouse(W, T)
    b_shipwrecks(W, T)
