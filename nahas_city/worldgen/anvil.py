"""(Copied from tools/world/anvil.py for the Nahas City world generator; parametrised for min_y / dimensions / custom dimension registration.)
Minimal Minecraft Java world writer: NBT encoder, chunk serializer (1.18+ section format), region (.mca) files,
level.dat.  Chunks are written with DataVersion 3465 (1.20.1); newer game versions upgrade them automatically."""
import gzip
import os
import struct
import time
import zlib

import numpy as np

DATA_VERSION = 3465
MIN_Y = -64


# ------------------------------------------------------------------ NBT

class Byte(int): pass
class Short(int): pass
class Int(int): pass
class Long(int): pass
class Float(float): pass
class Double(float): pass


class LongArray:
    def __init__(self, arr):
        self.arr = np.asarray(arr, dtype=">i8")


class NList:
    def __init__(self, tag, items):
        self.tag, self.items = tag, list(items)


TAG_BYTE, TAG_SHORT, TAG_INT, TAG_LONG, TAG_FLOAT, TAG_DOUBLE, TAG_BYTEARR, TAG_STRING, TAG_LIST, TAG_COMPOUND, \
    TAG_INTARR, TAG_LONGARR = range(1, 13)


def _tag_of(v):
    if isinstance(v, Byte): return TAG_BYTE
    if isinstance(v, Short): return TAG_SHORT
    if isinstance(v, Int): return TAG_INT
    if isinstance(v, Long): return TAG_LONG
    if isinstance(v, Float): return TAG_FLOAT
    if isinstance(v, Double): return TAG_DOUBLE
    if isinstance(v, str): return TAG_STRING
    if isinstance(v, dict): return TAG_COMPOUND
    if isinstance(v, NList): return TAG_LIST
    if isinstance(v, LongArray): return TAG_LONGARR
    raise TypeError(f"unsupported NBT value {type(v)}")


def _write_payload(out, v):
    t = _tag_of(v)
    if t == TAG_BYTE: out.append(struct.pack(">b", v))
    elif t == TAG_SHORT: out.append(struct.pack(">h", v))
    elif t == TAG_INT: out.append(struct.pack(">i", v))
    elif t == TAG_LONG: out.append(struct.pack(">q", v))
    elif t == TAG_FLOAT: out.append(struct.pack(">f", v))
    elif t == TAG_DOUBLE: out.append(struct.pack(">d", v))
    elif t == TAG_STRING:
        b = v.encode("utf-8"); out.append(struct.pack(">H", len(b))); out.append(b)
    elif t == TAG_LONGARR:
        out.append(struct.pack(">i", len(v.arr))); out.append(v.arr.tobytes())
    elif t == TAG_LIST:
        tag = v.tag if v.items else 0
        out.append(struct.pack(">bi", tag, len(v.items)))
        for it in v.items:
            _write_payload(out, it)
    elif t == TAG_COMPOUND:
        for k, val in v.items():
            out.append(struct.pack(">b", _tag_of(val)))
            kb = k.encode("utf-8"); out.append(struct.pack(">H", len(kb))); out.append(kb)
            _write_payload(out, val)
        out.append(b"\x00")


def nbt_bytes(root, name=""):
    out = [struct.pack(">b", TAG_COMPOUND), struct.pack(">H", len(name.encode())), name.encode()]
    _write_payload(out, root)
    return b"".join(out)


# ------------------------------------------------------------------ blocks

def parse_block(s):
    """'minecraft:stairs[facing=east,half=top]' -> (name, {props})"""
    if "[" in s:
        name, rest = s.split("[", 1)
        props = dict(p.split("=") for p in rest.rstrip("]").split(","))
    else:
        name, props = s, {}
    if ":" not in name:
        name = "minecraft:" + name
    return name, props


class Registry:
    """Global block-string <-> small int ids (0 = air)."""

    def __init__(self):
        self.names = ["minecraft:air"]
        self.ids = {"minecraft:air": 0, "air": 0}

    def id(self, s):
        i = self.ids.get(s)
        if i is None:
            name, props = parse_block(s)
            canon = name + ("[" + ",".join(f"{k}={props[k]}" for k in sorted(props)) + "]" if props else "")
            i = self.ids.get(canon)
            if i is None:
                i = len(self.names)
                self.names.append(canon)
                self.ids[canon] = i
            self.ids[s] = i
        return i

    def compound(self, i):
        name, props = parse_block(self.names[i])
        c = {"Name": name}
        if props:
            c["Properties"] = {k: str(v) for k, v in props.items()}
        return c


def _pack(indices, bits):
    """Pack palette indices (1-D array) into longs without spanning."""
    per = 64 // bits
    n = len(indices)
    nlongs = -(-n // per)
    padded = np.zeros(nlongs * per, dtype=np.uint64)
    padded[:n] = indices
    padded = padded.reshape(nlongs, per)
    shifts = (np.arange(per, dtype=np.uint64) * np.uint64(bits))
    longs = np.bitwise_or.reduce(padded << shifts, axis=1)
    return longs.astype(np.uint64).view(np.int64)


def serialize_chunk(cx, cz, blocks, biomes, reg, block_entities=(), min_y=MIN_Y):
    """blocks: uint16 array [y, z, x] (height multiple of 16, starting at min_y);
    biomes: uint8 array [z4, x4] indexes into biome_names tuple passed as biomes=(names, arr)."""
    biome_names, barr = biomes
    height = blocks.shape[0]
    sections = []
    for si in range(height // 16):
        sec = blocks[si * 16:(si + 1) * 16]
        ids, inv = np.unique(sec, return_inverse=True)
        if len(ids) == 1 and ids[0] == 0 and False:
            continue
        bs = {"palette": NList(TAG_COMPOUND, [reg.compound(int(i)) for i in ids])}
        if len(ids) > 1:
            bits = max(4, int(np.ceil(np.log2(len(ids)))))
            bs["data"] = LongArray(_pack(inv.reshape(-1).astype(np.uint64), bits))
        # biomes: same for all y in a section (x4,z4 resolution)
        bids, binv = np.unique(barr, return_inverse=True)
        bm = {"palette": NList(TAG_STRING, [biome_names[int(i)] for i in bids])}
        if len(bids) > 1:
            bbits = max(1, int(np.ceil(np.log2(len(bids)))))
            full = np.broadcast_to(binv.reshape(4, 4)[None, :, :], (4, 4, 4)).reshape(-1)  # [y4, z4, x4]
            bm["data"] = LongArray(_pack(full.astype(np.uint64), bbits))
        sections.append({"Y": Byte(si + min_y // 16), "block_states": bs, "biomes": bm})
    root = {
        "DataVersion": Int(DATA_VERSION),
        "xPos": Int(cx), "yPos": Int(min_y // 16), "zPos": Int(cz),
        "Status": "minecraft:full",
        "LastUpdate": Long(0), "InhabitedTime": Long(0),
        "isLightOn": Byte(0),
        "sections": NList(TAG_COMPOUND, sections),
        "block_entities": NList(TAG_COMPOUND, list(block_entities)),
        "Heightmaps": {},
        "fluid_ticks": NList(TAG_COMPOUND, []),
        "block_ticks": NList(TAG_COMPOUND, []),
        "structures": {"References": {}, "starts": {}},
    }
    return nbt_bytes(root)


# ------------------------------------------------------------------ region files

def write_region(path, chunks):
    """chunks: {(local_x, local_z): raw_nbt_bytes} for one 32x32 region."""
    header = bytearray(8192)
    body = []
    sector = 2
    now = int(time.time())
    for (lx, lz), raw in sorted(chunks.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        comp = zlib.compress(raw, 6)
        payload = struct.pack(">IB", len(comp) + 1, 2) + comp
        nsec = -(-len(payload) // 4096)
        payload += b"\x00" * (nsec * 4096 - len(payload))
        idx = (lx + lz * 32) * 4
        header[idx:idx + 4] = struct.pack(">I", (sector << 8) | nsec)
        header[4096 + idx:4096 + idx + 4] = struct.pack(">I", now)
        body.append(payload)
        sector += nsec
    with open(path, "wb") as f:
        f.write(header)
        for b in body:
            f.write(b)


# ------------------------------------------------------------------ level.dat

def flat_settings(biome, layers, features=0, lakes=0):
    """layers: list of (block, height)."""
    return {
        "biome": biome,
        "features": Byte(features), "lakes": Byte(lakes),
        "layers": NList(TAG_COMPOUND, [{"block": b, "height": Int(h)} for b, h in layers]),
        "structure_overrides": NList(TAG_STRING, []),
    }


def _flat_ocean_settings(sea_floor_y, sea_level, min_y=-64):
    return flat_settings("minecraft:ocean", [
        ("minecraft:bedrock", 1),
        ("minecraft:stone", sea_floor_y - min_y - 1),
        ("minecraft:sand", 1),
        ("minecraft:water", sea_level - sea_floor_y)])


def write_level_dat(path, name, spawn, sea_floor_y, sea_level, seed=1234567, datapacks=("file/nahas_city",),
                    version_name="1.20.1", extra_dims=None):
    """extra_dims: {"nahas:star_sea": {"type": "minecraft:the_end", "generator": {...}}, ...}
    No GameRules are stored (version-fragile) -> empty compound."""
    dims = {
        "minecraft:overworld": {
            "type": "minecraft:overworld",
            "generator": {"type": "minecraft:flat", "settings": _flat_ocean_settings(sea_floor_y, sea_level)},
        },
        "minecraft:the_nether": {
            "type": "minecraft:the_nether",
            "generator": {"type": "minecraft:noise", "settings": "minecraft:nether",
                          "biome_source": {"type": "minecraft:multi_noise", "preset": "minecraft:nether"}},
        },
        "minecraft:the_end": {
            "type": "minecraft:the_end",
            "generator": {"type": "minecraft:noise", "settings": "minecraft:end",
                          "biome_source": {"type": "minecraft:the_end"}},
        },
    }
    dims.update(extra_dims or {})
    now_ms = int(time.time() * 1000)
    data = {
        "DataVersion": Int(DATA_VERSION),
        "version": Int(19133),
        "Version": {"Id": Int(DATA_VERSION), "Name": version_name, "Series": "main", "Snapshot": Byte(0)},
        "LevelName": name,
        "GameType": Int(0),
        "Difficulty": Byte(2),
        "DifficultyLocked": Byte(0),
        "allowCommands": Byte(1),
        "hardcore": Byte(0),
        "initialized": Byte(1),
        "SpawnX": Int(spawn[0]), "SpawnY": Int(spawn[1]), "SpawnZ": Int(spawn[2]), "SpawnAngle": Float(0.0),
        "Time": Long(0), "DayTime": Long(0), "LastPlayed": Long(now_ms),
        "raining": Byte(0), "thundering": Byte(0),
        "rainTime": Int(100000), "thunderTime": Int(100000), "clearWeatherTime": Int(0),
        "WasModded": Byte(0),
        "MapFeatures": Byte(0),
        "GameRules": {},
        "DataPacks": {
            "Enabled": NList(TAG_STRING, ["vanilla", *datapacks]),
            "Disabled": NList(TAG_STRING, []),
        },
        "WorldGenSettings": {
            "seed": Long(seed),
            "generate_features": Byte(0),
            "bonus_chest": Byte(0),
            "dimensions": dims,
        },
        "ScheduledEvents": NList(TAG_COMPOUND, []),
        "CustomBossEvents": {},
        "DragonFight": {"NeedsStateScanning": Byte(1), "Gateways": NList(TAG_INT, []),
                        "DragonKilled": Byte(0), "PreviouslyKilled": Byte(0)},
        "WanderingTraderSpawnChance": Int(25), "WanderingTraderSpawnDelay": Int(24000),
        "BorderCenterX": Double(0), "BorderCenterZ": Double(0), "BorderSize": Double(59999968),
        "BorderSafeZone": Double(5), "BorderDamagePerBlock": Double(0.2), "BorderWarningBlocks": Double(5),
        "BorderWarningTime": Double(15), "BorderSizeLerpTime": Long(0), "BorderSizeLerpTarget": Double(59999968),
    }
    raw = nbt_bytes({"Data": data})
    with gzip.open(path, "wb") as f:
        f.write(raw)
