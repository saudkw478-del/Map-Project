"""Reusable building blocks for structures (all operate on a wg_core.Canvas in world coordinates)."""
import math
import numpy as np
from wg_core import Canvas, B, SKIP

DIRS = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}
LEFT = {"north": "west", "west": "south", "south": "east", "east": "north"}
RIGHT = {v: k for k, v in LEFT.items()}


def stair(mat, facing, half="bottom"):
    return f"minecraft:{mat}_stairs[facing={facing},half={half},shape=straight]"


def slab(mat, t="bottom"):
    return f"minecraft:{mat}_slab[type={t}]"


def wall(mat):
    return f"minecraft:{mat}_wall"


def door(mat, facing, half, hinge="left", open_=False):
    return f"minecraft:{mat}_door[facing={facing},half={half},hinge={hinge},open={'true' if open_ else 'false'}]"


def put_door(cv, x, y, z, facing, mat="acacia", hinge="left", open_=False):
    cv.set(x, y, z, door(mat, facing, "lower", hinge, open_))
    cv.set(x, y + 1, z, door(mat, facing, "upper", hinge, open_))


def lantern(hanging=False):
    return f"minecraft:lantern[hanging={'true' if hanging else 'false'}]"


def rng_for(*a):
    return np.random.default_rng(abs(hash(a)) % (2 ** 32) if False else (sum((i + 1) * 7919 * (int(v) + 13) for i, v in enumerate(a)) % (2 ** 31)))


def palm(cv, x, y, z, h=7, rnd=None, lean=None):
    """Palm tree; y = ground top block y (trunk starts at y+1). Jungle logs + leaves."""
    rnd = rnd or np.random.default_rng(x * 31 + z)
    dx, dz = lean if lean else (int(rnd.integers(-1, 2)), int(rnd.integers(-1, 2)))
    px, pz = x, z
    for i in range(1, h + 1):
        if i in (h // 3, 2 * h // 3):
            px, pz = px + dx, pz + dz
        cv.set(px, y + i, pz, "minecraft:jungle_log[axis=y]")
    top = y + h
    cv.set(px, top + 1, pz, "minecraft:jungle_leaves[persistent=true,distance=1]")
    for (fx, fz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for k in (1, 2, 3):
            yy = top + (1 if k == 1 else 0) - (1 if k == 3 else 0)
            cv.setif(px + fx * k, yy, pz + fz * k, "minecraft:jungle_leaves[persistent=true,distance=1]")
        cv.setif(px + fx * 3, top - 2, pz + fz * 3, "minecraft:jungle_leaves[persistent=true,distance=1]")
    for (fx, fz) in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        cv.setif(px + fx, top, pz + fz, "minecraft:jungle_leaves[persistent=true,distance=1]")
        cv.setif(px + 2 * fx, top - 1, pz + 2 * fz, "minecraft:jungle_leaves[persistent=true,distance=1]")
    cv.set(px, top, pz, "minecraft:jungle_log[axis=y]")


def acacia(cv, x, y, z, rnd):
    h = int(rnd.integers(4, 7))
    for i in range(1, h):
        cv.set(x, y + i, z, "minecraft:acacia_log[axis=y]")
    dx, dz = [(1, 0), (-1, 0), (0, 1), (0, -1)][int(rnd.integers(0, 4))]
    for k in (1, 2):
        cv.set(x + dx * k, y + h + k - 2, z + dz * k, "minecraft:acacia_log[axis=y]")
    cx, cz = x + dx * 2, z + dz * 2
    cy = y + h
    for yy, r in ((cy, 3), (cy + 1, 2)):
        for ax in range(-r, r + 1):
            for az in range(-r, r + 1):
                if ax * ax + az * az <= r * r + 1:
                    cv.setif(cx + ax, yy, cz + az, "minecraft:acacia_leaves[persistent=true,distance=1]")


def cactus(cv, x, y, z, h):
    for i in range(1, h + 1):
        cv.set(x, y + i, z, "minecraft:cactus[age=0]")


def well(cv, x, y, z, mat="sandstone", water=True):
    """3x3 well: y = ground top y. Water inside, roof of 4 posts."""
    cv.fill(x - 1, y, z - 1, x + 1, y, z + 1, f"minecraft:{mat}")
    cv.fill(x - 1, y + 1, z - 1, x + 1, y + 1, z + 1, f"minecraft:cut_{mat}" if mat in ("sandstone", "red_sandstone") else f"minecraft:{mat}")
    cv.set(x, y + 1, z, "minecraft:water" if water else "air")
    cv.set(x, y, z, "minecraft:water" if water else f"minecraft:{mat}")
    for (a, b) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        cv.fill(x + a, y + 2, z + b, x + a, y + 4, z + b, "minecraft:oak_fence")
    cv.fill(x - 1, y + 5, z - 1, x + 1, y + 5, z + 1, slab("oak"))
    cv.set(x, y + 4, z, lantern(True))
    cv.set(x, y + 5, z, "minecraft:oak_planks")


def pillar(cv, x, y, z, h, mat="sandstone", cap=True):
    cv.fill(x, y + 1, z, x, y + h, z, f"minecraft:{mat}")
    if cap:
        cv.set(x, y + h, z, "minecraft:chiseled_sandstone" if mat.endswith("sandstone") else f"minecraft:{mat}")


def dome(cv, cx, y, cz, r, mat, thick=1, inner=None):
    cv.sphere(cx, y, cz, r, mat, thick=thick, upper=True)


def lamp_post(cv, x, y, z, h=4, mat="minecraft:oak_fence", light="lantern"):
    cv.fill(x, y + 1, z, x, y + h, z, mat)
    cv.set(x, y + h + 1, z, lantern(False))


def brazier(cv, x, y, z, soul=False):
    cv.set(x, y + 1, z, "minecraft:soul_campfire[lit=true,facing=north]" if soul else "minecraft:campfire[lit=true,facing=north]")


def statue(cv, x, y, z, facing="south", mat="minecraft:waxed_cut_copper", pose=0):
    """Brass statue of a person, 5 high; y = ground top."""
    cv.fill(x, y + 1, z, x, y + 2, z, mat)                # legs
    cv.set(x - 1, y + 1, z, "air") if False else None
    cv.fill(x, y + 3, z, x, y + 4, z, mat)                # torso
    cv.set(x, y + 5, z, mat)                              # head
    fx, fz = DIRS[facing]
    sx, sz = -fz, fx                                      # side vector
    if pose == 0:      # arms down
        cv.set(x + sx, y + 3, z + sz, mat); cv.set(x - sx, y + 3, z - sz, mat)
        cv.set(x + sx, y + 4, z + sz, mat); cv.set(x - sx, y + 4, z - sz, mat)
    elif pose == 1:    # one arm raised holding lantern
        cv.set(x + sx, y + 4, z + sz, mat); cv.set(x + sx, y + 5, z + sz, mat)
        cv.set(x + sx, y + 6, z + sz, "minecraft:lantern[hanging=false]")
        cv.set(x - sx, y + 3, z - sz, mat); cv.set(x - sx, y + 4, z - sz, mat)
    elif pose == 2:    # both arms forward (frozen mid-step)
        cv.set(x + sx + fx, y + 4, z + sz + fz, mat); cv.set(x - sx + fx, y + 4, z - sz + fz, mat)
        cv.set(x + sx, y + 4, z + sz, mat); cv.set(x - sx, y + 4, z - sz, mat)
    else:              # hands over face
        cv.set(x + sx, y + 5, z + sz, mat); cv.set(x - sx, y + 5, z - sz, mat)
        cv.set(x + sx, y + 4, z + sz, mat); cv.set(x - sx, y + 4, z - sz, mat)
    cv.set(x + fx, y + 5, z + fz, "minecraft:waxed_exposed_copper") if False else None


def stairs_line(cv, x, z, y, length, facing, mat, width=1, up=True):
    """staircase going `facing` direction rising by 1 per step (facing = ascending direction)."""
    fx, fz = DIRS[facing]
    sx, sz = -fz, fx
    for i in range(length):
        for w in range(width):
            cv.set(x + fx * i + sx * w, y + i, z + fz * i + sz * w, stair(mat, facing))
            cv.fill(x + fx * i + sx * w, y + i - 1, z + fz * i + sz * w, x + fx * i + sx * w, y + i - 1, z + fz * i + sz * w, f"minecraft:{mat}_block" if False else "minecraft:stone_bricks") if False else None


def house(cv, x, y, z, w, d, h, door_side="south", wall_mat="minecraft:cut_sandstone", trim="minecraft:smooth_sandstone",
          roof="flat", roof_mat="minecraft:smooth_sandstone", door_mat="acacia", lit=True, rnd=None, furnish=True, win="air"):
    """Simple house; (x,z) = min corner of footprint; y = ground top y; floor at y (existing), walls from y+1.."""
    x2, z2 = x + w - 1, z + d - 1
    cv.fill(x, y, z, x2, y, z2, trim)
    cv.box(x, y + 1, z, x2, y + h, z2, wall_mat, inner="air", roof=False, floor=False)
    # corners trim
    for cx_ in (x, x2):
        for cz_ in (z, z2):
            cv.fill(cx_, y + 1, cz_, cx_, y + h, cz_, trim)
    # roof
    if roof == "flat":
        cv.fill(x, y + h + 1, z, x2, y + h + 1, z2, roof_mat)
        # parapet
        for xx in range(x, x2 + 1):
            for zz in (z, z2):
                cv.set(xx, y + h + 2, zz, slab("smooth_sandstone") if "sandstone" in roof_mat else slab("stone_brick"))
        for zz in range(z, z2 + 1):
            for xx in (x, x2):
                cv.set(xx, y + h + 2, zz, slab("smooth_sandstone") if "sandstone" in roof_mat else slab("stone_brick"))
    elif roof == "dome":
        cv.fill(x, y + h + 1, z, x2, y + h + 1, z2, roof_mat)
    # door
    if door_side in ("south", "north"):
        dx = x + w // 2
        dz = z2 if door_side == "south" else z
        cv.fill(dx, y + 1, dz, dx, y + 2, dz, "air")
        put_door(cv, dx, y + 1, dz, door_side, door_mat)
        # windows
        for wx in (x + 2, x2 - 2):
            if abs(wx - dx) > 1 and x < wx < x2:
                cv.set(wx, y + 2, dz, win)
                cv.set(wx, y + 2, z2 if door_side == "north" else z, win)
    else:
        dz = z + d // 2
        dx = x2 if door_side == "east" else x
        cv.fill(dx, y + 1, dz, dx, y + 2, dz, "air")
        put_door(cv, dx, y + 1, dz, door_side, door_mat)
        for wz in (z + 2, z2 - 2):
            if abs(wz - dz) > 1 and z < wz < z2:
                cv.set(dx, y + 2, wz, win)
                cv.set(x2 if door_side == "west" else x, y + 2, wz, win)
    if lit:
        cv.set(x + w // 2, y + h, z + d // 2, lantern(True))
        cv.set(x + w // 2, y + h + 1, z + d // 2, "minecraft:smooth_sandstone") if False else None
    if furnish and w >= 5 and d >= 5:
        # bed + chest + table
        cv.set(x + 1, y + 1, z + 1, "minecraft:red_bed[facing=south,part=foot]")
        cv.set(x + 1, y + 1, z + 2, "minecraft:red_bed[facing=south,part=head]")
        cv.set(x2 - 1, y + 1, z + 1, "minecraft:crafting_table")
        cv.set(x2 - 1, y + 1, z2 - 1, "minecraft:barrel[facing=up]")


def carpet_floor(cv, x1, z1, x2, z2, y, colors, rnd):
    for xx in range(x1, x2 + 1):
        for zz in range(z1, z2 + 1):
            cv.set(xx, y, zz, f"minecraft:{colors[int(rnd.integers(0, len(colors)))]}_carpet")


def skeleton_camel(cv, x, y, z, axis="x", rnd=None):
    """Skeleton of a camel-ish beast (bone blocks) lying on the ground."""
    fx, fz = (1, 0) if axis == "x" else (0, 1)
    sx, sz = -fz, fx
    for i in range(-3, 4):
        px, pz = x + fx * i, z + fz * i
        cv.set(px, y + 1, pz, "minecraft:bone_block[axis=" + axis + "]")
        if i in (-2, 0, 2):
            for s in (-1, 1):
                cv.set(px + sx * s, y + 1, pz + sz * s, "minecraft:bone_block[axis=y]")
                cv.set(px + sx * s, y + 2, pz + sz * s, "minecraft:bone_block[axis=" + axis + "]") if i == 0 else None
    for i in (3, 4):
        cv.set(x + fx * i, y + 2, z + fz * i, "minecraft:bone_block[axis=y]")
    cv.set(x + fx * 5, y + 3, z + fz * 5, "minecraft:skeleton_skull[rotation=%d]" % (4 if axis == "x" else 0))
    cv.set(x - fx * 3, y + 2, z - fz * 3, "minecraft:bone_block[axis=y]")


def tent(cv, x, y, z, w=7, d=7, color="red", burned=False, rnd=None):
    """Tent: x,z = center; wool tent pitched along x. burned -> collapsed/charred."""
    rnd = rnd or np.random.default_rng(x + z)
    hw, hd = w // 2, d // 2
    wool = f"minecraft:{color}_wool"
    if burned:
        blk = ["minecraft:black_wool", "minecraft:gray_wool", "minecraft:coal_block", "minecraft:black_carpet"]
        for xx in range(x - hw, x + hw + 1):
            for zz in range(z - hd, z + hd + 1):
                if rnd.random() < 0.55:
                    hgt = int(rnd.integers(0, 3))
                    b = blk[int(rnd.integers(0, len(blk)))]
                    if b.endswith("carpet"):
                        cv.set(xx, y + 1, zz, b)
                    else:
                        cv.fill(xx, y + 1, zz, xx, y + max(1, hgt), zz, b)
        # broken poles
        for (a, b) in ((-hw, -hd), (hw, hd), (-hw, hd)):
            cv.fill(x + a, y + 1, z + b, x + a, y + int(rnd.integers(2, 5)), z + b, "minecraft:stripped_dark_oak_log[axis=y]")
        cv.set(x, y + 1, z, "minecraft:campfire[lit=false,facing=north]")
        return
    for k in range(0, hd + 1):
        yy = y + 1 + (hd - k) if False else y + 1 + (hd - k)
    # A-frame across z
    for dz in range(-hd, hd + 1):
        hgt = hd - abs(dz) + 1
        for dx in range(-hw, hw + 1):
            cv.set(x + dx, y + hgt + 1, z + dz, wool)
            if abs(dx) == hw:
                pass
        # side walls of the A-frame below the ridge are open; fill the two end triangles
    for dx in (-hw, hw):
        for dz in range(-hd + 1, hd):
            for yy in range(y + 1, y + hd - abs(dz) + 2):
                cv.set(x + dx, yy, z + dz, wool)
    cv.fill(x - hw + 1, y + 1, z - hd + 1, x + hw - 1, y + 1, z + hd - 1, "air") if False else None
    cv.fill(x - hw + 1, y + 1, z - hd + 1, x + hw - 1, y + 1, z + hd - 1, f"minecraft:{color}_carpet")
    cv.set(x, y + 2, z, lantern(False)) if False else None
    for dx in (-hw + 1, hw - 1):
        cv.set(x + dx, y + 2, z, "minecraft:lantern[hanging=false]") if False else None
    cv.set(x, y + 1 + hd, z, lantern(True))
    cv.fill(x - hw, y + 1, z - hd, x - hw, y + 1, z - hd, "minecraft:oak_fence")


def ruin_wall(cv, x1, z1, x2, z2, y, h, mat, rnd, gap=0.25):
    """Broken wall segment along a line (axis-aligned)."""
    if x1 == x2:
        rng_ = [(x1, zz) for zz in range(min(z1, z2), max(z1, z2) + 1)]
    else:
        rng_ = [(xx, z1) for xx in range(min(x1, x2), max(x1, x2) + 1)]
    for (xx, zz) in rng_:
        hh = int(rnd.integers(0, h + 1))
        if rnd.random() < gap:
            hh = 0
        if hh > 0:
            cv.fill(xx, y + 1, zz, xx, y + hh, zz, mat[int(rnd.integers(0, len(mat)))] if isinstance(mat, (list, tuple)) else mat)


def blob_fill(cv, x, y, z, r, mat, rnd, h=2):
    for xx in range(x - r, x + r + 1):
        for zz in range(z - r, z + r + 1):
            if (xx - x) ** 2 + (zz - z) ** 2 <= r * r and rnd.random() < 0.8:
                cv.fill(xx, y + 1, zz, xx, y + int(rnd.integers(1, h + 1)), zz, mat)
