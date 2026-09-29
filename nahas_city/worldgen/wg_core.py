"""Block registry, sparse Canvas overlays and a fast chunk serializer (Anvil, DataVersion 3465)."""
import numpy as np
import anvil as A
from anvil import Int, Long, Byte, NList, TAG_COMPOUND, TAG_STRING, LongArray

SKIP = 65535
R = A.Registry()


def B(s):
    """block string / int -> global id.  None -> SKIP, 'air' -> 0."""
    if s is None:
        return SKIP
    if isinstance(s, (int, np.integer)):
        return int(s)
    if s == "air":
        return 0
    return R.id(s)


class Canvas:
    """Sparse block overlay over a world-coordinate box [x0,x1) x [y0,y1) x [z0,z1); arr indexed [y,z,x]."""

    def __init__(self, name, x0, y0, z0, x1, y1, z1):
        self.name = name
        self.x0, self.y0, self.z0, self.x1, self.y1, self.z1 = x0, y0, z0, x1, y1, z1
        self.arr = np.full((y1 - y0, z1 - z0, x1 - x0), SKIP, dtype=np.uint16)
        self.be = []

    # -- helpers
    def inb(self, x, y, z):
        return self.x0 <= x < self.x1 and self.y0 <= y < self.y1 and self.z0 <= z < self.z1

    def set(self, x, y, z, b):
        if self.inb(x, y, z):
            self.arr[y - self.y0, z - self.z0, x - self.x0] = B(b)

    def get(self, x, y, z):
        if self.inb(x, y, z):
            return int(self.arr[y - self.y0, z - self.z0, x - self.x0])
        return SKIP

    def setif(self, x, y, z, b):  # only over untouched / air
        if self.inb(x, y, z):
            v = self.arr[y - self.y0, z - self.z0, x - self.x0]
            if v == SKIP or v == 0:
                self.arr[y - self.y0, z - self.z0, x - self.x0] = B(b)

    def fill(self, x1, y1, z1, x2, y2, z2, b):
        x1, x2 = sorted((x1, x2)); y1, y2 = sorted((y1, y2)); z1, z2 = sorted((z1, z2))
        xa, xb = max(x1, self.x0), min(x2 + 1, self.x1)
        ya, yb = max(y1, self.y0), min(y2 + 1, self.y1)
        za, zb = max(z1, self.z0), min(z2 + 1, self.z1)
        if xa >= xb or ya >= yb or za >= zb:
            return
        self.arr[ya - self.y0:yb - self.y0, za - self.z0:zb - self.z0, xa - self.x0:xb - self.x0] = B(b)

    def box(self, x1, y1, z1, x2, y2, z2, b, inner="air", roof=True, floor=True):
        """Hollow box: walls of b; interior cleared to `inner` (None keeps)."""
        x1, x2 = sorted((x1, x2)); y1, y2 = sorted((y1, y2)); z1, z2 = sorted((z1, z2))
        self.fill(x1, y1, z1, x2, y2, z2, b)
        if inner is not None:
            self.fill(x1 + 1, y1 + (1 if floor else 0), z1 + 1, x2 - 1, y2 - (1 if roof else 0), z2 - 1, inner)

    def disc(self, cx, cz, r, y, b, r_in=None, pat=None):
        """Horizontal disc / ring of radius r at height y. pat(dx,dz)->block optional."""
        for z in range(cz - r, cz + r + 1):
            for x in range(cx - r, cx + r + 1):
                d2 = (x - cx) ** 2 + (z - cz) ** 2
                if d2 <= r * r + r and (r_in is None or d2 >= r_in * r_in):
                    self.set(x, y, z, pat(x - cx, z - cz) if pat else b)

    def cyl(self, cx, cz, r, y1, y2, b, hollow=False, inner="air"):
        for y in range(y1, y2 + 1):
            if hollow:
                self.disc(cx, cz, r, y, b)
                if inner is not None and y not in (y1, y2):
                    self.disc(cx, cz, r - 1, y, inner)
            else:
                self.disc(cx, cz, r, y, b)

    def sphere(self, cx, cy, cz, r, b, thick=1, upper=True, inner=None):
        r2o, r2i = (r + 0.5) ** 2, max(0, r - thick + 0.5) ** 2
        for y in range(cy if upper else cy - r, cy + r + 1):
            for z in range(cz - r, cz + r + 1):
                for x in range(cx - r, cx + r + 1):
                    d = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
                    if d <= r2o and d >= r2i:
                        self.set(x, y, z, b)
                    elif inner is not None and d < r2i:
                        self.set(x, y, z, inner)

    def add_be(self, x, y, z, bid, **fields):
        if self.inb(x, y, z):
            d = {"id": bid, "x": Int(x), "y": Int(y), "z": Int(z)}
            d.update(fields)
            self.be.append(d)

    def chest(self, x, y, z, facing="south", loot="nahas:chests/common", trapped=False):
        blk = "minecraft:trapped_chest" if trapped else "minecraft:chest"
        self.set(x, y, z, f"{blk}[facing={facing}]")
        self.add_be(x, y, z, blk, LootTable=loot, LootTableSeed=Long(0))

    def barrel(self, x, y, z, loot=None, facing="up"):
        self.set(x, y, z, f"minecraft:barrel[facing={facing}]")
        if loot:
            self.add_be(x, y, z, "minecraft:barrel", LootTable=loot, LootTableSeed=Long(0))

    def sign(self, x, y, z, lines, facing="south", wall=True, mat="oak", glow=False):
        import json
        msgs = [json.dumps({"text": t}, ensure_ascii=False) for t in (list(lines) + ["", "", "", ""])[:4]]
        blank = json.dumps({"text": ""})
        if wall:
            self.set(x, y, z, f"minecraft:{mat}_wall_sign[facing={facing}]")
        else:
            rot = {"south": 0, "west": 4, "north": 8, "east": 12}.get(facing, 0)
            self.set(x, y, z, f"minecraft:{mat}_sign[rotation={rot}]")
        self.add_be(x, y, z, f"minecraft:{mat}_wall_sign" if wall else f"minecraft:{mat}_sign",
                    front_text={"messages": NList(TAG_STRING, msgs), "color": "black", "has_glowing_text": Byte(1 if glow else 0)},
                    back_text={"messages": NList(TAG_STRING, [blank] * 4), "color": "black", "has_glowing_text": Byte(0)},
                    is_waxed=Byte(1))


# ---------------------------------------------------------------- chunk serialization

class Chunker:
    """Serializes dense [H,16,16] uint16 block arrays (H multiple of 16, starting at min_y)."""

    def __init__(self, min_y):
        self.min_y = min_y
        self._comp = {}

    def comp(self, i):
        c = self._comp.get(i)
        if c is None:
            c = self._comp[i] = R.compound(i)
        return c

    def biome_tag(self, biome_names, b4):
        bids, binv = np.unique(b4, return_inverse=True)
        bm = {"palette": NList(TAG_STRING, [biome_names[int(i)] for i in bids])}
        if len(bids) > 1:
            bbits = max(1, int(np.ceil(np.log2(len(bids)))))
            full = np.broadcast_to(binv.reshape(4, 4)[None, :, :], (4, 4, 4)).reshape(-1)
            bm["data"] = LongArray(A._pack(full.astype(np.uint64), bbits))
        return bm

    def serialize(self, cx, cz, blocks, biome_names, b4, be=()):
        bm = self.biome_tag(biome_names, b4)
        secs = []
        for si in range(blocks.shape[0] // 16):
            sec = blocks[si * 16:(si + 1) * 16]
            mn, mx = int(sec.min()), int(sec.max())
            if mn == mx:
                if mn == 0:
                    continue
                bs = {"palette": NList(TAG_COMPOUND, [self.comp(mn)])}
            else:
                ids, inv = np.unique(sec, return_inverse=True)
                bs = {"palette": NList(TAG_COMPOUND, [self.comp(int(i)) for i in ids])}
                bits = max(4, int(np.ceil(np.log2(len(ids)))))
                bs["data"] = LongArray(A._pack(inv.reshape(-1).astype(np.uint64), bits))
            secs.append({"Y": Byte(si + self.min_y // 16), "block_states": bs, "biomes": bm})
        root = {
            "DataVersion": Int(A.DATA_VERSION), "xPos": Int(cx), "yPos": Int(self.min_y // 16), "zPos": Int(cz),
            "Status": "minecraft:full", "LastUpdate": Long(0), "InhabitedTime": Long(0), "isLightOn": Byte(0),
            "sections": NList(TAG_COMPOUND, secs),
            "block_entities": NList(TAG_COMPOUND, list(be)),
            "Heightmaps": {}, "fluid_ticks": NList(TAG_COMPOUND, []), "block_ticks": NList(TAG_COMPOUND, []),
            "structures": {"References": {}, "starts": {}},
        }
        return A.nbt_bytes(root)


class CanvasIndex:
    def __init__(self, canvases):
        self.map = {}
        for cv in canvases:
            for cx in range(cv.x0 >> 4, ((cv.x1 - 1) >> 4) + 1):
                for cz in range(cv.z0 >> 4, ((cv.z1 - 1) >> 4) + 1):
                    self.map.setdefault((cx, cz), []).append(cv)

    def apply(self, cx, cz, blocks, min_y):
        """Paint canvases into blocks[y,16,16]; returns block entities located in the chunk."""
        bes = []
        for cv in self.map.get((cx, cz), ()):
            xa, xb = max(cv.x0, cx * 16), min(cv.x1, cx * 16 + 16)
            za, zb = max(cv.z0, cz * 16), min(cv.z1, cz * 16 + 16)
            ya, yb = max(cv.y0, min_y), min(cv.y1, min_y + blocks.shape[0])
            if xa >= xb or za >= zb or ya >= yb:
                continue
            sub = cv.arr[ya - cv.y0:yb - cv.y0, za - cv.z0:zb - cv.z0, xa - cv.x0:xb - cv.x0]
            tgt = blocks[ya - min_y:yb - min_y, za - cz * 16:zb - cz * 16, xa - cx * 16:xb - cx * 16]
            m = sub != SKIP
            tgt[m] = sub[m]
            for b in cv.be:
                if cx * 16 <= int(b["x"]) < cx * 16 + 16 and cz * 16 <= int(b["z"]) < cz * 16 + 16:
                    bes.append(b)
        return bes


def write_regions(path, chunks):
    """chunks: {(cx,cz): raw}; groups per region file."""
    import os
    os.makedirs(path, exist_ok=True)
    regs = {}
    for (cx, cz), raw in chunks.items():
        regs.setdefault((cx >> 5, cz >> 5), {})[(cx & 31, cz & 31)] = raw
    for (rx, rz), d in regs.items():
        A.write_region(os.path.join(path, f"r.{rx}.{rz}.mca"), d)
