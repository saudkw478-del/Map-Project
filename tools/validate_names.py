"""Check block/item/entity/enchantment/effect/biome ids we use against the official registries (PrismarineJS
minecraft-data) for several Minecraft versions."""
import glob, json, os, re, sys
MCD = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paths = json.load(open(f"{MCD}/dataPaths.json"))["pc"]
def load(ver, kind):
    p = paths[ver].get(kind)
    return json.load(open(f"{MCD}/{p}/{kind}.json")) if p else None
def names(ver, kind, key="name"):
    d = load(ver, kind)
    return {e[key] for e in d} if d else None

def strip(n): return n.replace("minecraft:", "").split("[")[0].split("{")[0]
world_blocks = {strip(l.strip()) for l in open(f"{ROOT}/tools/world/palette_used.txt") if l.strip()}
dp_blocks, items, entities, ench, effects = set(), set(), set(), set(), set()
for f in glob.glob(f"{ROOT}/datapack/got_castle/data/got/function/**/*.mcfunction", recursive=True):
    for line in open(f):
        t = line.split()
        if not t: continue
        m = re.search(r"\b(?:setblock|fill)\b.*", line)
        if line.startswith("setblock ") or line.startswith("fill "):
            dp_blocks.add(strip(t[-1] if t[0] == "fill" else t[4]))
        for m in re.finditer(r"summon minecraft:(\w+)", line): entities.add(m.group(1))
        for m in re.finditer(r"type=minecraft:(\w+)", line): entities.add(m.group(1))
        for m in re.finditer(r"with minecraft:(\w+)", line): items.add(m.group(1))
        for m in re.finditer(r"effect give \S+ minecraft:(\w+)", line): effects.add(m.group(1))
for f in glob.glob(f"{ROOT}/datapack/got_castle/data/got/loot_table/**/*.json", recursive=True):
    j = json.load(open(f))
    for p in j["pools"]:
        for e in p["entries"]:
            items.add(e["name"].replace("minecraft:", ""))
            for fn in e.get("functions", []):
                for k in fn.get("enchantments", {}): ench.add(k.replace("minecraft:", ""))
sys.path.insert(0, f"{ROOT}/tools/world"); import geo
biomes = {b.replace("minecraft:", "") for b in geo.REGION_BIOME.values()} | {"ocean", "frozen_ocean", "cold_ocean", "lukewarm_ocean", "warm_ocean"}
print("world blocks:", len(world_blocks), "datapack blocks:", len(dp_blocks), "items:", len(items), "entities:", len(entities),
      "enchantments:", len(ench), "effects:", len(effects), "biomes:", len(biomes))
for ver in ["1.20.1", "1.21.1", "1.21.4", "1.21.8", "1.21.11", "26.1"]:
    B = names(ver, "blocks"); I = names(ver, "items"); E = names(ver, "entities"); EN = names(ver, "enchantments"); EF = names(ver, "effects"); BI = names(ver, "biomes")
    print(f"--- {ver}")
    chk = [("world block", world_blocks, B), ("datapack block", dp_blocks, B), ("item", items, I), ("entity", entities, E),
           ("enchantment", ench, EN), ("effect", effects, EF), ("biome", biomes, BI)]
    for label, used, reg in chk:
        if reg is None: print(f"   ({label}: no registry)"); continue
        miss = sorted(u for u in used if u not in reg)
        if miss: print(f"   MISSING {label}: {miss}")
