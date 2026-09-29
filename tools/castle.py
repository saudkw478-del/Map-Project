"""Castle geometry. Origin (0,0,0) = the first air block above ground at the player's feet.
x = east, z = south (the main gate faces +z / south)."""
import random

from mc import Build

STONE = "stone_bricks"
COBB = "cobblestone"
POL = "polished_andesite"
PLANK = "dark_oak_planks"
LOG = "dark_oak_log"
BLACK = "polished_blackstone_bricks"
R = 56          # clear / flatten radius
WALL = "stone_brick_wall"
STAIRS = "stone_brick_stairs"
CHISEL = "chiseled_stone_bricks"
BASE2 = "deepslate_bricks"
SLAB = "stone_brick_slab[type=bottom]"
HOUSE1, HOUSE2 = "red", "black"
THRONE = True

CLEAR_H = 46


PALETTES = {
    # name: (stone, base, trim, roof, wall, stairs, chiseled, base2, dark)
    "grey":  ("stone_bricks", "cobblestone", "polished_andesite", "dark_oak_planks", "stone_brick_wall", "stone_brick_stairs", "chiseled_stone_bricks", "deepslate_bricks", "polished_blackstone_bricks"),
    "black": ("polished_blackstone_bricks", "blackstone", "polished_blackstone", "deepslate_tiles", "polished_blackstone_brick_wall", "polished_blackstone_brick_stairs", "chiseled_polished_blackstone", "deepslate_bricks", "polished_blackstone_bricks"),
    "red":   ("red_nether_bricks", "nether_bricks", "smooth_red_sandstone", "dark_oak_planks", "red_nether_brick_wall", "red_nether_brick_stairs", "chiseled_red_sandstone", "deepslate_bricks", "polished_blackstone_bricks"),
    "brick": ("bricks", "stone_bricks", "polished_andesite", "dark_oak_planks", "brick_wall", "brick_stairs", "chiseled_stone_bricks", "stone_bricks", "polished_blackstone_bricks"),
    "white": ("quartz_bricks", "smooth_quartz", "polished_diorite", "light_blue_terracotta", "diorite_wall", "quartz_stairs", "chiseled_quartz_block", "stone_bricks", "polished_blackstone_bricks"),
    "gold":  ("cut_sandstone", "sandstone", "smooth_sandstone", "red_terracotta", "sandstone_wall", "sandstone_stairs", "chiseled_sandstone", "stone_bricks", "polished_blackstone_bricks"),
    "green": ("mossy_stone_bricks", "mossy_cobblestone", "polished_andesite", "oxidized_cut_copper", "mossy_stone_brick_wall", "mossy_stone_brick_stairs", "chiseled_stone_bricks", "stone_bricks", "polished_blackstone_bricks"),
    "storm": ("deepslate_bricks", "cobbled_deepslate", "polished_deepslate", "deepslate_tiles", "deepslate_brick_wall", "deepslate_brick_stairs", "chiseled_deepslate", "stone_bricks", "polished_blackstone_bricks"),
    "sand":  ("sandstone", "smooth_sandstone", "cut_sandstone", "orange_terracotta", "sandstone_wall", "sandstone_stairs", "chiseled_sandstone", "red_sandstone", "polished_blackstone_bricks"),
}


def set_palette(name, banners=("red", "black"), throne=True):
    g = globals()
    stone, base, trim, roof, wall, stairs, chisel, base2, dark = PALETTES[name]
    g.update(STONE=stone, COBB=base, POL=trim, PLANK=roof, WALL=wall, STAIRS=stairs, CHISEL=chisel, BASE2=base2,
             BLACK=dark, SLAB=stairs.replace("_stairs", "_slab") + "[type=bottom]",
             HOUSE1=banners[0], HOUSE2=banners[1], THRONE=throne)


def sgn(v):
    return 1 if v > 0 else -1


def banner(b, x, y, z, color, facing):
    b.set(x, y, z, f"{color}_wall_banner[facing={facing}]")


def parapet(b, x1, z1, x2, z2, y):
    """Crenellated parapet ring around a rectangle: low row at y, merlons at y+1 (every 2nd block)."""
    b.fill(x1, y, z1, x2, y, z1, STONE)
    b.fill(x1, y, z2, x2, y, z2, STONE)
    b.fill(x1, y, z1, x1, y, z2, STONE)
    b.fill(x2, y, z1, x2, y, z2, STONE)
    for x in range(x1, x2 + 1):
        if (x - x1) % 2 == 0:
            b.set(x, y + 1, z1, STONE)
            b.set(x, y + 1, z2, STONE)
    for z in range(z1, z2 + 1):
        if (z - z1) % 2 == 0:
            b.set(x1, y + 1, z, STONE)
            b.set(x2, y + 1, z, STONE)


def lantern_floor(b, x, y, z):
    b.set(x, y, z, "lantern[hanging=false]")


def tower(b, cx, cz, half, top, y0=0, floors=(), openings=(), doors=(), slits=(), roof=None,
          foundation=True, flag=True):
    """Hollow tower. Solid shell from y0..top (top = platform), interior air y0..top-1,
    ladder in the west column, crenellated roof or pyramid roof."""
    x1, x2, z1, z2 = cx - half, cx + half, cz - half, cz + half
    if foundation:
        b.fill(x1, -3, z1, x2, -1, z2, STONE)
    b.fill(x1, y0, z1, x2, top, z2, STONE)
    b.fill(x1 + 1, y0, z1 + 1, x2 - 1, top - 1, z2 - 1, "air")
    # base course
    if y0 == 0:
        b.fill(x1, 0, z1, x2, 1, z2, COBB)
        b.fill(x1 + 1, 0, z1 + 1, x2 - 1, 1, z2 - 1, "air")
    for fy in floors:
        b.fill(x1 + 1, fy, z1 + 1, x2 - 1, fy, z2 - 1, PLANK)
    # ladder (west interior column, attached to west wall)
    lx = x1 + 1
    for y in range(y0, top + 1):
        b.set(lx, y, cz, "ladder[facing=east]")
    # lanterns on the floors so nothing spawns inside
    for fy in [y0 - 1] + list(floors):
        if fy >= y0 or y0 == 0:
            lantern_floor(b, x2 - 1, max(fy, y0 - 1) + 1, z2 - 1)
    for (ox1, oz1, ox2, oz2, oy) in openings:
        b.fill(ox1, oy, oz1, ox2, oy + 1, oz2, "air")
    for (dx, dz) in doors:
        b.fill(dx, y0, dz, dx, y0 + 1, dz, "air")
    for (sx_, sz_, sy) in slits:
        b.fill(sx_, sy, sz_, sx_, sy + 1, sz_, "iron_bars")
    if roof == "pyramid":
        for i in range(half + 2):
            h = half + 1 - i
            b.fill(cx - h, top + 1 + i, cz - h, cx + h, top + 1 + i, cz + h, PLANK)
        py = top + 1 + half + 2
        b.fill(cx, py, cz, cx, py + 3, cz, "dark_oak_fence")
        b.set(cx, py + 4, cz, f"{HOUSE1}_banner[rotation=0]")
    else:
        parapet(b, x1, z1, x2, z2, top + 1)
        if flag:
            b.fill(cx, top + 1, cz, cx, top + 5, cz, "dark_oak_fence")
            b.set(cx, top + 6, cz, f"{HOUSE1}_banner[rotation=0]")


# ---------------------------------------------------------------- stages

def stage_ground():
    b = Build(preview=False)
    b.fill(-R, 0, -R, R, CLEAR_H, R, "air")
    b.fill(-R, -3, -R, R, -2, R, "dirt")
    b.fill(-R, -1, -R, R, -1, R, "grass_block")
    return b


def stage_walls():
    b = Build()
    # foundation + solid wall body
    for (x1, z1, x2, z2) in [(-44, -44, 44, -42), (-44, 42, 44, 44), (-44, -41, -42, 41), (42, -41, 44, 41)]:
        b.fill(x1, -3, z1, x2, -1, z2, STONE)
        b.fill(x1, 0, z1, x2, 1, z2, COBB)
        b.fill(x1, 2, z1, x2, 8, z2, STONE)
        b.fill(x1, 9, z1, x2, 9, z2, POL)
    # parapet on the outside edge, low railing on the inside edge
    parapet(b, -44, -44, 44, 44, 10)
    # remove the outer parapet ring's inner parts: the ring above is a full rectangle; hollow the courtyard side
    b.fill(-43, 10, -43, 43, 11, 43, "air")
    b.fill(-43, 10, -42, 43, 10, -42, WALL)
    b.fill(-43, 10, 42, 43, 10, 42, WALL)
    b.fill(-42, 10, -43, -42, 10, 43, WALL)
    b.fill(42, 10, -43, 42, 10, 43, WALL)
    # arrow slits and torches
    for i in range(-36, 37, 8):
        if abs(i) > 16:
            b.fill(i, 4, 42, i, 5, 44, "air")
            b.set(i, 6, 41, "wall_torch[facing=north]")
        b.fill(i, 4, -44, i, 5, -42, "air")
        b.set(i, 6, -41, "wall_torch[facing=south]")
        b.fill(-44, 4, i, -42, 5, i, "air")
        b.set(-41, 6, i, "wall_torch[facing=east]")
        b.fill(42, 4, i, 44, 5, i, "air")
        b.set(41, 6, i, "wall_torch[facing=west]")
    # wall stairs (2 wide, 10 steps) reaching the walkway
    def stairs(x0, z0, dx, dz, width_axis, facing):
        for i in range(10):
            x, z = x0 + dx * i, z0 + dz * i
            for w in range(2):
                sx_ = x + (w * width_axis[0])
                sz_ = z + (w * width_axis[1])
                if i:
                    b.fill(sx_, 0, sz_, sx_, i - 1, sz_, STONE)
                b.set(sx_, i, sz_, f"{STAIRS}[facing={facing}]")
    stairs(-36, -41, 1, 0, (0, 1), "east")
    stairs(36, 41, -1, 0, (0, -1), "west")
    stairs(-41, 36, 0, -1, (1, 0), "north")
    stairs(41, -36, 0, 1, (-1, 0), "south")
    return b


def stage_towers():
    b = Build()
    # corner towers
    for sx in (-1, 1):
        for sz in (-1, 1):
            cx, cz = sx * 44, sz * 44
            xb = sorted((cx - sx * 2, cx))      # band of the N/S wall? (x-run of the E/W wall)
            zb = sorted((cz - sz * 2, cz))
            inx, inz = cx - sx * 5, cz - sz * 5  # inward faces
            openings = [
                (xb[0], inz, xb[1], inz, 10),    # walkway of the E/W wall enters via the inward z-face
                (inx, zb[0], inx, zb[1], 10),    # walkway of the N/S wall enters via the inward x-face
            ]
            slits = [(cx, cz + sz * 5, 5), (cx + sx * 5, cz, 5), (cx, cz + sz * 5, 14), (cx + sx * 5, cz, 14)]
            tower(b, cx, cz, 5, 24, floors=(9, 18), openings=openings,
                  doors=[(cx - sx * 3, inz)], slits=slits)
    # mid-wall towers
    tower(b, 0, -44, 3, 15, floors=(9,),
          openings=[(-3, -44, -3, -42, 10), (3, -44, 3, -42, 10)],
          doors=[(1, -41)], slits=[(0, -47, 5), (0, -47, 12)])
    tower(b, -44, 0, 3, 15, floors=(9,),
          openings=[(-44, -3, -42, -3, 10), (-44, 3, -42, 3, 10)],
          doors=[(-41, 1)], slits=[(-47, 0, 5), (-47, 0, 12)])
    tower(b, 44, 0, 3, 15, floors=(9,),
          openings=[(42, -3, 44, -3, 10), (42, 3, 44, 3, 10)],
          doors=[(41, 1)], slits=[(47, 0, 5), (47, 0, 12)])
    return b


def stage_gate():
    b = Build()
    x1, x2, z1, z2 = -13, 13, 36, 46
    b.fill(x1, -3, z1, x2, -1, z2, STONE)
    b.fill(x1, 0, z1, x2, 1, z2, COBB)
    b.fill(x1, 2, z1, x2, 16, z2, STONE)
    b.fill(x1, 17, z1, x2, 17, z2, POL)
    # towers' corner pillars in a darker stone
    for px in (x1, x2):
        for pz in (z1, z2):
            b.fill(px, 0, pz, px, 17, pz, POL)
    # passage
    b.fill(-4, 0, z1, 4, 9, z2, "air")
    b.fill(-4, -1, z1, 4, -1, z2, STONE)
    # arch frame
    b.fill(-5, 0, z2, -5, 9, z2, CHISEL)
    b.fill(5, 0, z2, 5, 9, z2, CHISEL)
    b.fill(-5, 10, z2, 5, 10, z2, CHISEL)
    # raised portcullis
    b.fill(-4, 6, 45, 4, 9, 45, "iron_bars")
    for lz in (38, 42):
        b.set(-3, 9, lz, "lantern[hanging=true]")
        b.set(3, 9, lz, "lantern[hanging=true]")
    # arrow slits over the outside
    for x in (-10, -7, 7, 10):
        b.fill(x, 12, z2, x, 13, z2, "iron_bars")
    # banners
    for x, c in ((-8, HOUSE1), (8, HOUSE1), (-11, HOUSE2), (11, HOUSE2)):
        banner(b, x, 6, z2 + 1, c, "south")
    # ladders up to the roof
    for lx in (-11, 11):
        for y in range(0, 18):
            b.set(lx, y, 35, "ladder[facing=north]")
    parapet(b, x1, z1, x2, z2, 18)
    for lx in (-11, 11):
        b.fill(lx, 18, z1, lx, 19, z1, "air")
    for fx in (-13, 13):
        b.fill(fx, 18, 41, fx, 22, 41, "dark_oak_fence")
        b.set(fx, 23, 41, f"{HOUSE1}_banner[rotation=0]")
    # road from the gate outwards
    b.fill(-3, -1, 47, 3, -1, R, "stone_bricks")
    b.fill(-2, -1, 47, 2, -1, R, "cobblestone")
    for z in range(48, 55, 6):
        for x in (-4, 4):
            b.fill(x, 0, z, x, 1, z, WALL)
            b.set(x, 2, z, "lantern[hanging=false]")
    return b


def stage_keep():
    b = Build()
    x1, x2, z1, z2 = -18, 18, -24, 12
    b.fill(x1, -3, z1, x2, -1, z2, BLACK)
    b.fill(x1, 0, z1, x2, 1, z2, BASE2)
    b.fill(x1, 2, z1, x2, 17, z2, STONE)
    b.fill(x1, 18, z1, x2, 19, z2, POL)
    parapet(b, x1, z1, x2, z2, 20)
    turrets = [(18, -24), (-18, -24), (18, 12), (-18, 12)]
    for (cx, cz) in turrets:
        sx, sz = (1 if cx > 0 else -1), (1 if cz > 0 else -1)
        x1_, x2_, z1_, z2_ = cx - 4, cx + 4, cz - 4, cz + 4
        # openings from the keep roof into the turret
        openings = [(cx - sx * 4, cz - sz * 2, cx - sx * 4, cz - sz * 2, 20),
                    (cx - sx * 2, cz - sz * 4, cx - sx * 2, cz - sz * 4, 20)]
        slits = [(cx + sx * 4, cz, 24), (cx, cz + sz * 4, 24)]
        tower(b, cx, cz, 4, 30, floors=(19,), openings=openings, slits=slits, foundation=False)
    # central spire
    tower(b, 0, -6, 6, 39, y0=20, floors=(29,), doors=[(0, 0)],
          slits=[(0, -12, 25), (-6, -6, 25), (6, -6, 25), (0, -12, 33), (-6, -6, 33), (6, -6, 33)],
          roof="pyramid", foundation=False)
    # carve the hall last so turret walls do not stick into it
    b.fill(-16, 0, -22, 16, 17, 10, "air")
    b.fill(-16, -1, -22, 16, -1, 10, BLACK)
    # front entrance
    b.fill(-3, 0, 11, 3, 8, 12, "air")
    b.fill(-4, 0, 12, -4, 9, 12, CHISEL)
    b.fill(4, 0, 12, 4, 9, 12, CHISEL)
    b.fill(-4, 9, 12, 4, 9, 12, CHISEL)
    b.fill(-3, 8, 12, 3, 8, 12, CHISEL)
    b.fill(-2, 0, 13, -2, 4, 13, "air")
    for x, c in ((-9, HOUSE1), (9, HOUSE1), (-13, HOUSE2), (13, HOUSE2)):
        banner(b, x, 9, 13, c, "south")
    # windows in the hall walls
    for zc in (-16, -8, 0, 6):
        for wx in (17, -17):
            b.fill(wx - 1 if wx > 0 else wx, 5, zc - 1, wx if wx > 0 else wx + 1, 13, zc + 1, "gray_stained_glass")
    for xc in (-12, 12):
        b.fill(xc - 1, 5, -24, xc + 1, 13, -23, "gray_stained_glass")
    return b


def stage_hall():
    b = Build()
    # carpet aisle
    b.fill(-1, 0, -13, 1, 0, 10, f"{HOUSE1}_carpet")
    b.fill(-3, 0, 10, 3, 0, 10, f"{HOUSE1}_carpet")
    # dais
    b.fill(-9, 0, -22, 9, 0, -13, BLACK)
    b.fill(-7, 1, -22, 7, 1, -14, BLACK)
    b.fill(-5, 2, -22, 5, 2, -16, BLACK)
    # steps (stairs) in front of each tier
    b.fill(-9, 0, -12, 9, 0, -12, "polished_blackstone_brick_stairs[facing=north]")
    b.fill(-7, 1, -13, 7, 1, -13, "polished_blackstone_brick_stairs[facing=north]")
    b.fill(-5, 2, -15, 5, 2, -15, "polished_blackstone_brick_stairs[facing=north]")
    b.fill(-2, 0, -12, 2, 0, -12, f"{HOUSE1}_carpet")
    b.fill(-1, 1, -13, 1, 1, -13, f"{HOUSE1}_carpet")
    b.fill(-1, 2, -14, 1, 2, -14, f"{HOUSE1}_carpet")
    if THRONE:
        # the Iron Throne
        b.fill(-2, 3, -21, 2, 3, -20, "iron_block")
        b.set(0, 3, -19, "polished_blackstone_brick_stairs[facing=north]")
        b.set(-1, 3, -19, WALL)
        b.set(1, 3, -19, WALL)
        b.fill(-1, 4, -21, 1, 6, -21, "iron_block")
        b.set(0, 4, -20, "iron_block")
        heights21 = {-3: 8, -2: 10, -1: 12, 0: 14, 1: 12, 2: 10, 3: 8}
        heights22 = {-4: 7, -3: 9, -2: 11, -1: 13, 0: 15, 1: 13, 2: 11, 3: 9, 4: 7}
        for x, h in heights21.items():
            b.fill(x, 3, -22, x, h, -22, "iron_bars")
        for x, h in heights22.items():
            b.fill(x, 7, -22, x, h, -22, "iron_bars")
    else:
        # the high seat of the house
        b.fill(-1, 3, -21, 1, 3, -20, "dark_oak_planks")
        b.set(0, 3, -19, "dark_oak_stairs[facing=north]")
        b.set(-1, 3, -19, "dark_oak_fence")
        b.set(1, 3, -19, "dark_oak_fence")
        b.fill(-1, 4, -21, 1, 8, -21, "dark_oak_planks")
        b.fill(0, 9, -21, 0, 10, -21, "dark_oak_planks")
        banner(b, 0, 7, -20, HOUSE1, "south")
        banner(b, -2, 6, -22, HOUSE2, "south")
        banner(b, 2, 6, -22, HOUSE2, "south")
    # torches by the throne
    for x in (-6, 6):
        b.fill(x, 3, -20, x, 3, -20, "polished_blackstone_wall")
        b.set(x, 4, -20, "lantern[hanging=false]")
    # banners on the north wall
    for x, c in ((-7, HOUSE1), (7, HOUSE1), (-11, HOUSE2), (11, HOUSE2), (-15, HOUSE1), (15, HOUSE1)):
        banner(b, x, 8, -22, c, "south")
    # pillars and ceiling beams with lanterns
    for x in (-9, 9):
        for z in (-10, -4, 2, 8):
            b.fill(x, 0, z, x, 17, z, "polished_deepslate")
            b.set(x, 0, z, CHISEL)
            b.set(x, 16, z, CHISEL)
    for z in (-19, -11, -3, 5):
        b.fill(-16, 17, z, 16, 17, z, "dark_oak_log[axis=x]")
        for x in (-12, -5, 5, 12):
            b.set(x, 16, z, "lantern[hanging=true]")
    # long feast tables with chairs
    for tx in (-5, 5):
        b.fill(tx, 0, -10, tx, 0, 8, "spruce_planks")
        for z in range(-10, 9, 2):
            b.set(tx - 1, 0, z, "spruce_stairs[facing=west]")
            b.set(tx + 1, 0, z, "spruce_stairs[facing=east]")
    # fireplaces at the far corners of the hall (decorative)
    for x in (-15, 15):
        b.fill(x, 0, 9, x, 2, 9, "stone_bricks")
        b.set(x, 0, 8, "campfire[lit=true]")
    # wall torches down the sides
    for z in (-14, -6, 2, 8):
        b.set(-16, 4, z, "wall_torch[facing=east]")
        b.set(16, 4, z, "wall_torch[facing=west]")
    return b


def stage_courtyard():
    b = Build()
    # plaza and the road from gate to keep
    b.fill(-27, -1, -32, 27, -1, 20, "gravel")
    b.fill(-2, -1, 13, 2, -1, 36, "stone_bricks")
    b.fill(-3, -1, 13, -3, -1, 36, "cobblestone")
    b.fill(3, -1, 13, 3, -1, 36, "cobblestone")
    for z in range(16, 37, 6):
        for x in (-4, 4):
            b.fill(x, 0, z, x, 1, z, WALL)
            b.set(x, 2, z, "lantern[hanging=false]")
    # ---- armory (west) ----
    ax1, ax2, az1, az2 = -38, -24, 12, 22
    b.fill(ax1, -1, az1, ax2, -1, az2, "stone_bricks")
    b.fill(ax1, 0, az1, ax2, 6, az2, STONE)
    b.fill(ax1 + 1, 0, az1 + 1, ax2 - 1, 5, az2 - 1, "air")
    b.fill(ax1 + 1, 6, az1 + 1, ax2 - 1, 6, az2 - 1, PLANK)
    for k in range(6):
        b.fill(ax1 - 1, 7 + k, az1 - 1 + k, ax2 + 1, 7 + k, az2 + 1 - k, PLANK)
    b.fill(-32, 0, az1, -30, 2, az1, "air")           # door (north)
    b.fill(-32, 0, az1 - 1, -30, 0, az1 - 3, "stone_bricks")
    for (x, tbl) in zip(range(-36, -25, 2), ("swords", "ranged", "lannister", "nights_watch", "targaryen", "supplies")):
        b.chest(x, 0, 21, "north", tbl)
    b.set(-36, 0, 13, "smithing_table")
    b.set(-34, 0, 13, "anvil")
    b.set(-28, 0, 13, "grindstone[face=floor]")
    b.set(-26, 0, 13, "blast_furnace[facing=south]")
    for x in (-34, -28):
        b.set(x, 5, 17, "lantern[hanging=true]")
    b.set(-37, 3, 17, "wall_torch[facing=east]")
    b.set(-25, 3, 17, "wall_torch[facing=west]")
    # ---- godswood (east) ----
    b.fill(24, -1, 12, 38, -1, 36, "grass_block")
    b.fill(26, -2, 26, 31, -1, 30, "water")
    # weirwood: pale trunk with a carved face, spreading branches and a ragged red canopy
    rnd = random.Random(21)
    tx, tz = 33, 19                     # trunk centre (3x3 base)
    b.fill(tx - 2, 0, tz - 2, tx + 2, 0, tz + 2, "birch_log[axis=y]")          # root flare
    b.fill(tx - 1, 1, tz - 1, tx + 1, 9, tz + 1, "birch_log[axis=y]")
    b.fill(tx, 10, tz, tx, 13, tz, "birch_log[axis=y]")
    for (dx, dz, ln) in ((-1, 0, 4), (1, 0, 4), (0, -1, 4), (0, 1, 4)):
        for k in range(2, 2 + ln):
            b.set(tx + dx * k, 8 + k // 2, tz + dz * k, "birch_log[axis=%s]" % ("x" if dx else "z"))
    # the face (south side): eyes, weeping red tears, mouth
    for ex in (tx - 1, tx + 1):
        b.set(ex, 6, tz + 2, "black_wool"); b.set(ex, 5, tz + 2, "red_wool"); b.set(ex, 4, tz + 2, "red_wool")
    b.set(tx, 3, tz + 2, "black_wool"); b.set(tx, 2, tz + 2, "black_wool")
    cx_, cy_, cz_ = tx, 13, tz
    for x in range(cx_ - 8, cx_ + 9):
        for y in range(cy_ - 4, cy_ + 5):
            for z in range(cz_ - 8, cz_ + 9):
                d = ((x - cx_) / 7.0) ** 2 + ((y - cy_) / 3.6) ** 2 + ((z - cz_) / 7.0) ** 2
                if d < 1.0 and rnd.random() < (1.15 - d):
                    b.set(x, y, z, "red_wool" if rnd.random() < 0.7 else "red_terracotta")
    for _ in range(26):                # hanging strands of red leaves
        x, z = rnd.randint(cx_ - 7, cx_ + 7), rnd.randint(cz_ - 7, cz_ + 7)
        if ((x - cx_) / 7.0) ** 2 + ((z - cz_) / 7.0) ** 2 < 0.9:
            for y in range(cy_ - 4, cy_ - 4 - rnd.randint(1, 3), -1):
                b.set(x, y, z, "red_wool")
    # heart-tree pool
    # benches
    for x in (27, 30):
        b.set(x, 0, 32, "oak_stairs[facing=north]")
    b.set(25, 0, 25, "lantern[hanging=false]")
    # ---- well ----
    b.fill(12, 0, 24, 14, 1, 26, "stone_bricks")
    b.set(13, 0, 25, "water")
    b.set(13, 1, 25, "air")
    for (x, z) in ((12, 24), (14, 24), (12, 26), (14, 26)):
        b.fill(x, 2, z, x, 3, z, "dark_oak_fence")
    b.fill(11, 4, 23, 15, 4, 27, "dark_oak_slab[type=bottom]")
    # ---- training yard (dummies + hay) ----
    for x in (12, 16, 20):
        b.fill(x, 0, 32, x, 0, 32, "hay_block")
        b.set(x, 1, 32, "carved_pumpkin[facing=north]")
    # ---- markers used by the game ----
    b.raw("summon marker ~0 ~ ~52 {Tags:[\"got_gate\"]}")
    b.raw("summon marker ~0 ~ ~ {Tags:[\"got_center\"]}")
    return b


STAGES = [
    ("s1_ground", stage_ground),
    ("s2_walls", stage_walls),
    ("s3_towers", stage_towers),
    ("s4_gate", stage_gate),
    ("s5_keep", stage_keep),
    ("s6_hall", stage_hall),
    ("s7_courtyard", stage_courtyard),
]
