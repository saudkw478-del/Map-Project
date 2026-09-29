"""The walled brass city (radius ~150) with sealed south gate, palace and courtyard boss arena."""
import numpy as np
from wg_core import Canvas, B, SKIP
from shapes import *

WCC = "minecraft:waxed_cut_copper"
WCB = "minecraft:waxed_copper_block"
WEX = "minecraft:waxed_exposed_cut_copper"
WWE = "minecraft:waxed_weathered_cut_copper"
WOX = "minecraft:waxed_oxidized_cut_copper"
GOLD = "minecraft:gold_block"


def build_city(W):
    p = W.main("city")
    cx, cz, y = p["x"], p["z"], p["y"]
    cv = W.canvas("city", cx - 170, 60, cz - 170, cx + 171, 140, cz + 171)
    rnd = np.random.default_rng(9)
    n = 341
    o = 170
    ii = np.arange(n) - o
    DX, DZ = np.meshgrid(ii, ii)            # [z, x]
    R = np.hypot(DX, DZ)
    a = cv.arr
    gy = y - cv.y0

    def put(mask, yy, blk):
        a[yy - cv.y0][mask] = B(blk)

    # ---------- ground pattern
    ax_ns = (np.abs(DX) <= 4) & (R > 44)
    ax_ew = (np.abs(DZ) <= 4) & (R > 44)
    ring = (R >= 98) & (R <= 104)
    inner = (R > 44) & (R <= 60)
    street = ax_ns | ax_ew | ring
    ground = np.full((n, n), B("minecraft:smooth_sandstone"), np.uint16)
    chk = ((DX // 2 + DZ // 2) % 2 == 0)
    ground[street] = np.where(chk[street], B("minecraft:cut_sandstone"), B("minecraft:smooth_sandstone"))
    ground[street & (np.abs(DX) <= 0)] = B(WEX)
    ground[street & (np.abs(DZ) <= 0)] = B(WEX)
    ground[inner] = np.where(chk[inner], B(WCC), B(WEX))
    ground[inner & (R > 56)] = B("minecraft:polished_blackstone")
    ground[(R < 41)] = B("minecraft:smooth_sandstone")
    inside = R <= 149
    a[gy][inside] = ground[inside]
    # outside the wall: paved apron for the south gate road
    apron = (np.abs(DX) <= 6) & (DZ > 150) & (DZ < 166) & (R > 149)
    a[gy][apron] = B("minecraft:cut_sandstone")

    # ---------- courtyard (boss arena): disc r<=40
    for_ = R <= 40.5
    court = np.full((n, n), B(WCC), np.uint16)
    court[(R > 36) & (R <= 40.5)] = B(GOLD)
    court[(R > 30) & (R <= 36)] = np.where(chk, B("minecraft:polished_blackstone"), B("minecraft:smooth_basalt"))[(R > 30) & (R <= 36)]
    court[(R > 22) & (R <= 30)] = np.where(chk, B(WEX), B(WWE))[(R > 22) & (R <= 30)]
    court[(R > 14) & (R <= 22)] = B("minecraft:cut_sandstone")
    ang = np.arctan2(DZ, DX)
    spoke = (np.abs(np.cos(6 * ang)) > 0.97) & (R > 6) & (R <= 36)
    court[spoke & (R <= 30)] = B(GOLD)
    court[(R > 7) & (R <= 9)] = B("minecraft:black_terracotta")
    court[R <= 7] = np.where(R[R <= 7] > 3, B(WEX), B("minecraft:red_terracotta")).astype(np.uint16)
    court[R <= 1] = B("minecraft:chiseled_sandstone")  # anchor column stays plain solid ground
    a[gy][for_] = court[for_]

    # ---------- outer wall ring 145..150
    wallm = (R >= 145) & (R <= 150.4)
    put_h = lambda mask, y1, y2, blk: [a.__setitem__((yy - cv.y0, mask), B(blk)) for yy in range(y1, y2 + 1)]
    for yy in range(y + 1, y + 18):
        a[yy - cv.y0][wallm] = B(WCC if (yy - y) % 6 else WEX)
    walk = wallm & (R <= 147.2)
    a[y + 18 - cv.y0][walk] = B("minecraft:cut_sandstone")
    par = wallm & (R > 147.2)
    for yy in (y + 18, y + 19, y + 20):
        a[yy - cv.y0][par] = B(WCC)
    crenel = par & (((DX + DZ) % 2) == 0)
    a[y + 21 - cv.y0][crenel] = B(WCC)
    # gold band
    a[y + 12 - cv.y0][wallm] = B(GOLD)
    a[y + 18 - cv.y0][wallm & (R > 147.2) & (R < 148.2)] = B(GOLD)
    # wall stair access at N,S,E,W (tangent direction)
    for side in range(4):
        for i in range(18):
            u, v = 20 + i, -140
            wx, wz = [(u, v), (-v, u), (-u, -v), (v, -u)][side]
            face = ["east", "south", "west", "north"][side]
            for w_ in range(2):
                du = [(0, 1), (-1, 0), (0, -1), (1, 0)][side]
                px, pz = cx + wx + du[0] * w_, cz + wz + du[1] * w_
                cv.set(px, y + 1 + i, pz, stair("stone_brick", face))
                cv.fill(px, y + 1, pz, px, y + i, pz, "minecraft:stone_bricks") if i else None
    # ---------- towers every 30deg (offset 15)
    for k in range(12):
        ang_ = np.radians(k * 30 + 15)
        tx, tz = int(round(cx + 148 * np.cos(ang_))), int(round(cz + 148 * np.sin(ang_)))
        for yy in range(y + 1, y + 34):
            cv.disc(tx, tz, 6, yy, WCC if (yy - y) % 8 else GOLD, r_in=5)
        cv.disc(tx, tz, 6, y + 30, WEX)
        cv.disc(tx, tz, 5, y + 18, "minecraft:cut_sandstone")     # floor at walkway level
        cv.disc(tx, tz, 7, y + 34, WEX)
        cv.sphere(tx, y + 35, tz, 6, WOX, thick=1, upper=True)
        cv.fill(tx, y + 42, tz, tx, y + 45, tz, "minecraft:lightning_rod") if False else cv.set(tx, y + 42, tz, GOLD)
        cv.set(tx, y + 43, tz, "minecraft:lantern[hanging=false]")
        # door to walkway + arrow slits
        for yy in (y + 24, y + 28):
            for (dx_, dz_) in ((6, 0), (-6, 0), (0, 6), (0, -6)):
                cv.set(tx + dx_, yy, tz + dz_, "air") if False else None
    # ---------- gates
    gates = {}
    for side, (gxc, gzc, sx, sz) in {"S": (cx, cz + 148, 1, 0), "N": (cx, cz - 148, 1, 0), "E": (cx + 148, cz, 0, 1), "W": (cx - 148, cz, 0, 1)}.items():
        # opening box: 13 wide, 14 high through wall thickness (r 145..150)
        for t in range(-8, 9):
            for depth in range(-6, 7):
                if side in "NS":
                    x_, z_ = gxc + t, gzc + (depth if side == "S" else -depth)
                else:
                    x_, z_ = gxc + (depth if side == "E" else -depth), gzc + t
                if abs(t) <= 6:
                    for yy in range(y + 1, y + 15):
                        cv.set(x_, yy, z_, WCB if abs(t) > 0 else GOLD)
                    cv.set(x_, y + 15, z_, GOLD) if False else None
                elif abs(t) in (7, 8):
                    for yy in range(y + 1, y + 26):
                        cv.set(x_, yy, z_, GOLD if yy % 5 == 0 else WCC)
        # arch lintel
        for t in range(-8, 9):
            for depth in range(-6, 7):
                if side in "NS":
                    x_, z_ = gxc + t, gzc + (depth if side == "S" else -depth)
                else:
                    x_, z_ = gxc + (depth if side == "E" else -depth), gzc + t
                for yy in range(y + 15, y + 22):
                    cv.set(x_, yy, z_, WEX if yy > y + 15 else GOLD)
        gates[side] = (gxc, gzc)
    # south gate sockets (7 end-portal frames) on the outer face
    sockets = []
    for i in range(7):
        t = -6 + 2 * i
        yy = y + 8 + int(3 * np.cos((t / 6.0) * 1.2 - 0.0)) - 3
        cv.set(cx + t, yy, cz + 151, "minecraft:end_portal_frame[eye=false,facing=south]")
        sockets.append((cx + t, yy, cz + 151))
    for t in (-6, 6):
        for yy in range(y + 1, y + 6):
            pass
    W.feat("city", south_gate_seal_box=(cx - 6, y + 1, cz + 142, cx + 6, y + 14, cz + 154), south_gate_center=(cx, y + 1, cz + 150),
           gate_sockets=sockets, gate_note="datapack opens the gate by fill air over south_gate_seal_box (x1,y1,z1,x2,y2,z2)")
    # statues / lamps at gate
    for t in (-10, 10):
        statue(cv, cx + t, y, cz + 156, "south", WCC, 0)
        cv.fill(cx + t + 3 * (1 if t > 0 else -1), y + 1, cz + 155, cx + t + 3 * (1 if t > 0 else -1), y + 5, cz + 155, "minecraft:polished_blackstone_wall")
        cv.set(cx + t + 3 * (1 if t > 0 else -1), y + 6, cz + 155, "minecraft:lantern[hanging=false]")
    cv.sign(cx + 8, y + 1, cz + 158, ["مدينة", "النحاس", "البوابة مغلقة", "٧ أختام"], "south", wall=False, mat="dark_oak")
    # ---------- courtyard ring wall r 41..44 with 4 gateways
    rw = (R >= 41) & (R <= 44.4)
    gap = (np.minimum(np.abs(DX), np.abs(DZ)) <= 4)
    for yy in range(y + 1, y + 15):
        a[yy - cv.y0][rw & ~gap] = B(WCC if yy % 7 else GOLD)
    a[y + 15 - cv.y0][rw & ~gap & (((DX + DZ) % 2) == 0)] = B(WCC)
    # arches over gaps
    for yy in range(y + 10, y + 15):
        a[yy - cv.y0][rw & gap] = B(WEX)
    # pillars inside ring (r=37) and braziers (r=33)
    for k in range(16):
        ang_ = k * np.pi / 8
        px_, pz_ = int(round(cx + 37 * np.cos(ang_))), int(round(cz + 37 * np.sin(ang_)))
        if min(abs(px_ - cx), abs(pz_ - cz)) <= 5:
            continue
        cv.fill(px_, y + 1, pz_, px_, y + 11, pz_, WEX)
        cv.set(px_, y + 1, pz_, GOLD); cv.set(px_, y + 11, pz_, GOLD)
        cv.set(px_, y + 12, pz_, "minecraft:lantern[hanging=false]")
    for k in range(8):
        ang_ = k * np.pi / 4 + np.pi / 8
        px_, pz_ = int(round(cx + 32 * np.cos(ang_))), int(round(cz + 32 * np.sin(ang_)))
        cv.fill(px_, y + 1, pz_, px_, y + 2, pz_, "minecraft:polished_blackstone_wall") if False else cv.fill(px_, y + 1, pz_, px_, y + 2, pz_, "minecraft:polished_blackstone")
        cv.set(px_, y + 3, pz_, "minecraft:campfire[lit=true,facing=north]")
    # seal-7 altar / reward alcove (north-ish, inside courtyard)
    cv.fill(cx - 2, y + 1, cz - 30, cx + 2, y + 1, cz - 26, GOLD)
    cv.fill(cx - 1, y + 2, cz - 29, cx + 1, y + 2, cz - 27, "minecraft:chiseled_sandstone")
    cv.chest(cx, y + 3, cz - 28, "south", "nahas:chests/boss")
    cv.set(cx - 1, y + 3, cz - 28, "minecraft:soul_lantern[hanging=false]"); cv.set(cx + 1, y + 3, cz - 28, "minecraft:soul_lantern[hanging=false]")
    W.feat("city", courtyard_center=(cx, y + 1, cz), courtyard_radius=40, boss_spawn=(cx, y + 1, cz), seal7_altar=(cx, y + 3, cz - 28),
           courtyard_gates=[(cx, y + 1, cz - 42), (cx, y + 1, cz + 42), (cx - 42, y + 1, cz), (cx + 42, y + 1, cz)])
    # ---------- palace north of courtyard
    px0, px1, pz0, pz1 = cx - 52, cx + 52, cz - 104, cz - 48
    PH = 26
    cv.fill(px0, y, pz0, px1, y, pz1, WCC)
    cv.box(px0, y + 1, pz0, px1, y + PH, pz1, WCC, inner="air", roof=False, floor=False)
    cv.fill(px0, y + PH, pz0, px1, y + PH, pz1, GOLD if False else WEX)
    for yy in (y + 8, y + 16, y + PH - 1):
        cv.fill(px0, yy, pz0, px1, yy, pz0, GOLD); cv.fill(px0, yy, pz1, px1, yy, pz1, GOLD)
        cv.fill(px0, yy, pz0, px0, yy, pz1, GOLD); cv.fill(px1, yy, pz0, px1, yy, pz1, GOLD)
    for xx in range(px0, px1 + 1):
        for zz in (pz0, pz1):
            if (xx + zz) % 2 == 0:
                cv.set(xx, y + PH + 1, zz, WCC)
    # facade openings (south side toward the courtyard): 5 arches
    for ai in range(5):
        ax_ = cx - 40 + ai * 20
        for xx in range(ax_ - 2, ax_ + 3):
            cv.fill(xx, y + 1, pz1, xx, y + 8, pz1, "air") if ai == 2 else cv.fill(xx, y + 1, pz1, xx, y + 7, pz1, "minecraft:orange_stained_glass_pane")
        cv.fill(ax_ - 3, y + 1, pz1, ax_ - 3, y + 9, pz1, GOLD if False else WEX)
        cv.fill(ax_ + 3, y + 1, pz1, ax_ + 3, y + 9, pz1, WEX)
    cv.fill(cx - 3, y + 1, pz1, cx + 3, y + 10, pz1, "air")
    cv.fill(cx - 3, y + 11, pz1, cx + 3, y + 11, pz1, GOLD)
    # steps to the palace door
    for i in range(4):
        cv.fill(cx - 6 - (3 - i), y + 1 + (3 - i) - 4 + 0, pz1 + 1 + (3 - i), cx + 6 + (3 - i), y, pz1 + 1 + (3 - i), "minecraft:cut_sandstone") if False else None
    # domes
    cv.sphere(cx, y + PH + 1, (pz0 + pz1) // 2, 20, WOX, thick=1, upper=True)
    cv.sphere(cx, y + PH + 21, (pz0 + pz1) // 2, 3, GOLD, thick=3, upper=True)
    cv.fill(cx, y + PH + 25, (pz0 + pz1) // 2, cx, y + PH + 30, (pz0 + pz1) // 2, "minecraft:lightning_rod")
    for sx in (-1, 1):
        cv.sphere(cx + sx * 38, y + PH + 1, (pz0 + pz1) // 2, 9, WOX, thick=1, upper=True)
        cv.set(cx + sx * 38, y + PH + 11, (pz0 + pz1) // 2, GOLD)
    # minarets
    for (mx, mz) in ((px0 - 4, pz0 - 4), (px1 + 4, pz0 - 4), (px0 - 4, pz1 + 6), (px1 + 4, pz1 + 6)):
        for yy in range(y + 1, y + 50):
            cv.disc(mx, mz, 3, yy, WCC if yy % 9 else GOLD, r_in=2)
        cv.disc(mx, mz, 4, y + 46, WEX)
        cv.sphere(mx, y + 47, mz, 3, WOX, thick=1, upper=True)
        cv.set(mx, y + 51, mz, GOLD); cv.set(mx, y + 52, mz, "minecraft:lantern[hanging=false]")
    # interior: throne hall
    cz_mid = (pz0 + pz1) // 2
    for xx in range(px0 + 1, px1):
        for zz in range(pz0 + 1, pz1):
            cv.set(xx, y, zz, WEX if (xx // 2 + zz // 2) % 2 else WCC)
    for zz in range(pz0 + 2, pz1):
        for xx in range(cx - 2, cx + 3):
            cv.set(xx, y + 1, zz, "minecraft:red_carpet")
    for xx in (cx - 14, cx + 14):
        for zz in range(pz0 + 8, pz1 - 4, 9):
            cv.fill(xx, y + 1, zz, xx, y + PH - 2, zz, WEX)
            cv.set(xx, y + 1, zz, GOLD); cv.set(xx, y + PH - 2, zz, GOLD)
            cv.set(xx + (2 if xx < cx else -2), y + 9, zz, lantern(False)) if False else None
    for zz in range(pz0 + 6, pz1 - 2, 9):
        for xx in (cx - 8, cx + 8):
            cv.set(xx, y + PH - 1, zz, lantern(True))
        for k in range(-30, 31, 15):
            cv.set(cx + k, y + PH - 1, zz, lantern(True))
    tz_ = pz0 + 4
    cv.fill(cx - 5, y + 1, tz_ - 2, cx + 5, y + 2, tz_ + 2, GOLD)
    cv.fill(cx - 1, y + 3, tz_, cx + 1, y + 3, tz_, GOLD)
    cv.fill(cx - 1, y + 4, tz_ - 1, cx + 1, y + 6, tz_ - 1, GOLD)
    cv.set(cx, y + 3, tz_ + 1, stair("waxed_cut_copper", "south"))
    cv.chest(cx - 8, y + 1, pz0 + 3, "south", "nahas:chests/city")
    cv.chest(cx + 8, y + 1, pz0 + 3, "south", "nahas:chests/city")
    for k in range(5):
        statue(cv, px0 + 8 + k * 20, y, pz0 + 6, "south", WCC, k % 4)
    W.feat("city", throne=(cx, y + 4, tz_), palace_door=(cx, y + 1, pz1), palace_bounds=(px0, y, pz0, px1, y + PH, pz1))
    # ---------- reserved map for houses
    occ = np.zeros((n, n), bool)
    occ |= R < 50
    occ |= (np.abs(DX) <= 7) | (np.abs(DZ) <= 7)
    occ |= (R >= 95) & (R <= 107)
    occ |= R > 139
    occ[(DZ >= -110) & (DZ <= -42) & (np.abs(DX) <= 62)] = True    # palace + gardens
    bazaar = (cx + 72, cz - 40, 20)
    fount = (cx - 74, cz + 36, 13)
    for (bx_, bz_, br) in (bazaar, fount):
        occ |= np.hypot(DX - (bx_ - cx), DZ - (bz_ - cz)) < br + 3
    # bazaar
    bx_, bz_, br = bazaar
    for dz in range(-br, br + 1):
        for dx in range(-br, br + 1):
            if dx * dx + dz * dz <= br * br:
                cv.set(bx_ + dx, y, bz_ + dz, WCC if (dx + dz) % 2 else WEX)
    cols = ["red", "yellow", "orange", "blue", "green", "purple"]
    for k in range(10):
        ang_ = k * 2 * np.pi / 10
        sx_, sz_ = int(round(bx_ + 12 * np.cos(ang_))), int(round(bz_ + 12 * np.sin(ang_)))
        col = cols[k % len(cols)]
        for dx in (-2, 2):
            for dz in (-2, 2):
                cv.fill(sx_ + dx, y + 1, sz_ + dz, sx_ + dx, y + 3, sz_ + dz, "minecraft:polished_blackstone_wall") if False else cv.fill(sx_ + dx, y + 1, sz_ + dz, sx_ + dx, y + 3, sz_ + dz, "minecraft:oak_fence")
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                cv.set(sx_ + dx, y + 4, sz_ + dz, f"minecraft:{col}_wool" if (dx + dz) % 2 == 0 else "minecraft:white_wool")
        cv.set(sx_, y + 1, sz_, "minecraft:barrel[facing=up]")
        statue(cv, sx_ + 1, y, sz_ + 1, "south", WCC, k % 4)   # frozen merchant
    cv.fill(bx_ - 1, y + 1, bz_ - 1, bx_ + 1, y + 2, bz_ + 1, GOLD)
    cv.set(bx_, y + 3, bz_, "minecraft:lantern[hanging=false]")
    # fountain
    fx_, fz_, fr = fount
    for dz in range(-fr, fr + 1):
        for dx in range(-fr, fr + 1):
            d = np.hypot(dx, dz)
            if d <= fr:
                cv.set(fx_ + dx, y, fz_ + dz, WEX if d > 9 else "minecraft:smooth_sandstone")
            if 8 <= d <= 9:
                cv.set(fx_ + dx, y + 1, fz_ + dz, WCC)
    cv.disc(fx_, fz_, 7, y, "minecraft:water")
    cv.fill(fx_, y + 1, fz_, fx_, y + 5, fz_, GOLD)
    cv.set(fx_, y + 6, fz_, "minecraft:water")
    for k in range(6):
        ang_ = k * np.pi / 3
        statue(cv, int(round(fx_ + 11 * np.cos(ang_))), y, int(round(fz_ + 11 * np.sin(ang_))), "south", WCC, 3)
    # ---------- avenues: lamps + statues
    for side in (-1, 1):
        for k in range(0, 100, 8):
            d = 50 + k
            if d > 140:
                break
            for (px_, pz_) in ((cx + side * 6, cz + d), (cx + side * 6, cz - d), (cx + d, cz + side * 6), (cx - d, cz + side * 6)):
                if k % 16 == 0:
                    face = "west" if px_ > cx and abs(pz_ - cz) > abs(px_ - cx) else "east"
                    statue(cv, px_, y, pz_, ["south", "north", "east", "west"][(k // 8 + int(side)) % 4], WCC if k % 24 else WEX, (k // 8) % 4)
                else:
                    cv.fill(px_, y + 1, pz_, px_, y + 4, pz_, "minecraft:polished_blackstone_wall")
                    cv.set(px_, y + 5, pz_, "minecraft:lantern[hanging=false]")
    # ---------- houses
    pal = [("minecraft:smooth_sandstone", WCC, WCC), ("minecraft:cut_sandstone", WEX, WEX), ("minecraft:yellow_terracotta", WCC, WWE),
           ("minecraft:orange_terracotta", "minecraft:cut_sandstone", WCC), ("minecraft:sandstone", GOLD, WCC), ("minecraft:white_terracotta", WEX, WWE)]
    cnt = 0
    st = 0
    for gz_ in range(-138, 138, 16):
        for gx_ in range(-138, 138, 16):
            w_, d_ = int(rnd.integers(8, 12)), int(rnd.integers(8, 12))
            ox, oz = gx_ + int(rnd.integers(0, 16 - w_ + 1)), gz_ + int(rnd.integers(0, 16 - d_ + 1))
            if ox - 1 + o < 0 or oz - 1 + o < 0 or ox + w_ + 1 + o >= n or oz + d_ + 1 + o >= n:
                continue
            if occ[oz - 1 + o: oz + d_ + 2 + o, ox - 1 + o: ox + w_ + 2 + o].any():
                continue
            if rnd.random() < 0.08:
                continue
            h = int(rnd.integers(4, 9))
            wm, tr, rm = pal[int(rnd.integers(0, len(pal)))]
            cxh, czh = ox + w_ // 2, oz + d_ // 2
            if abs(cxh) < abs(czh):
                door_ = "east" if cxh < 0 else "west"
            else:
                door_ = "south" if czh < 0 else "north"
            house(cv, cx + ox, y, cz + oz, w_, d_, h, door_, wall_mat=wm, trim=tr, roof="flat", roof_mat=rm, door_mat="dark_oak", rnd=rnd, win="minecraft:glass_pane")
            # copper dome on some
            if rnd.random() < 0.4:
                r_ = min(w_, d_) // 2 - 1
                cv.sphere(cx + cxh, y + h + 2, cz + czh, r_, WOX, thick=1, upper=True)
                cv.set(cx + cxh, y + h + 2 + r_ + 1, cz + czh, GOLD)
            # frozen resident in front of the door
            fx, fz = {"south": (cxh, oz + d_ + 1), "north": (cxh, oz - 2), "east": (ox + w_ + 1, czh), "west": (ox - 2, czh)}[door_]
            statue(cv, cx + fx, y, cz + fz, {"south": "south", "north": "north", "east": "east", "west": "west"}[door_], WCC, int(rnd.integers(0, 4)))
            st += 1
            if rnd.random() < 0.25:
                cv.chest(cx + ox + 1, y + 1, cz + oz + d_ - 2, "east", "nahas:chests/city")
            cnt += 1
    W.feat("city", houses=cnt, statues_est=st + 60)
    # palms in gardens near palace
    for k in range(-40, 41, 16):
        for zz in (cz - 40 - 4, cz - 40 + 0):
            pass
    W.poi("city", p["ar"], cx, y, cz, "main", plaza=320)
