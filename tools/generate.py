"""Generate the datapack into ../datapack/got_castle and zip it to ../dist/."""
import json, os, shutil, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import castle, game  # noqa: E402

ROOT = os.path.dirname(HERE)
DP = os.path.join(ROOT, "datapack", "got_castle")
DIST = os.path.join(ROOT, "dist")

# Folder names changed in 1.21 (functions -> function, loot_tables -> loot_table, tags/functions -> tags/function).
# We write both spellings so one zip works on every recent version.
FN_DIRS = ["function", "functions"]
LOOT_DIRS = ["loot_table", "loot_tables"]
TAG_DIRS = ["function", "functions"]

MAX_CMDS_PER_FILE = 2500


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_fn(name, lines):
    text = "\n".join(lines) + "\n"
    for d in FN_DIRS:
        w(os.path.join(DP, "data", "got", d, name + ".mcfunction"), text)


def selftest_lines(stage_names):
    L = ['tellraw @s {"text":"--- Game of Thrones Castle self-test ---","color":"gold"}']
    L.append(f'execute if score #state {game.SB} matches 0.. run tellraw @s {{"text":"[OK] scoreboard/state ready","color":"green"}}')
    L.append(f'execute unless score #state {game.SB} matches 0.. run tellraw @s {{"text":"[..] game not started yet (normal before /function got:game/start)","color":"yellow"}}')
    L.append('execute if entity @e[tag=got_origin] run tellraw @s {"text":"[OK] castle origin marker exists (castle was built)","color":"green"}')
    L.append('execute unless entity @e[tag=got_origin] run tellraw @s {"text":"[..] castle not built yet: run /function got:build","color":"yellow"}')
    L.append('execute if entity @e[tag=got_gate] run tellraw @s {"text":"[OK] castle build finished (gate marker exists)","color":"green"}')
    L.append('execute at @e[tag=got_origin,limit=1] if block ~ ~ ~4 red_carpet run tellraw @s {"text":"[OK] throne room carpet found","color":"green"}')
    L.append('execute at @e[tag=got_origin,limit=1] if block ~ ~3 ~-19 polished_blackstone_brick_stairs run tellraw @s {"text":"[OK] Iron Throne found","color":"green"}')
    L.append('execute at @e[tag=got_origin,limit=1] if block ~-36 ~ ~21 chest run tellraw @s {"text":"[OK] armory chests found","color":"green"}')
    L.append(f'execute store success score #ok {game.SB} run loot give @s loot got:kit/weapons')
    L.append(f'execute if score #ok {game.SB} matches 1 run tellraw @s {{"text":"[OK] loot tables work (you just got a Valyrian sword)","color":"green"}}')
    L.append(f'execute unless score #ok {game.SB} matches 1 run tellraw @s {{"text":"[FAIL] loot tables did not load - send the log to the developer","color":"red"}}')
    return L


def build_stages():
    stages = castle.STAGES
    for i, (name, fn) in enumerate(stages):
        b = fn()
        nxt = stages[i + 1][0] if i + 1 < len(stages) else None
        parts = b.chunk(MAX_CMDS_PER_FILE)
        # one _a inner function per stage (parts chained via extra functions)
        inner = parts[0] if parts else []
        extra = []
        for k, part in enumerate(parts[1:], start=1):
            write_fn(f"build/{name}_a{k}", part)
            inner = inner + [f"function got:build/{name}_a{k}"]
        if name == "s7_courtyard":
            inner = inner + game.loot_fill_lines()
        write_fn(f"build/{name}_a", inner)
        after = game.finish_lines() if nxt is None else ()
        if nxt is None:
            # last stage: run inner at origin, then finish (which also runs at the origin marker)
            write_fn(f"build/{name}", game.stage_wrap(name, None, 0, after))
        else:
            write_fn(f"build/{name}", game.stage_wrap(name, nxt, 60 if name == "s1_ground" else 30))
    return


def main():
    if os.path.exists(DP):
        shutil.rmtree(DP)
    build_stages()
    for name, lines in game.game_functions().items():
        write_fn(name, lines)
    write_fn("selftest", selftest_lines([]))
    for name, tbl in game.loot_tables().items():
        for d in LOOT_DIRS:
            w(os.path.join(DP, "data", "got", d, name + ".json"), json.dumps(tbl, indent=1))
    for tag, fn in (("load", "got:load"), ("tick", "got:tick")):
        for d in TAG_DIRS:
            w(os.path.join(DP, "data", "minecraft", "tags", d, tag + ".json"),
              json.dumps({"values": [fn]}))
    meta = {
        "pack": {
            "pack_format": 48,
            "supported_formats": {"min_inclusive": 48, "max_inclusive": 999},
            "min_format": 48,
            "max_format": 999,
            "description": "Game of Thrones Castle: huge castle, 7 waves, Night King boss, weapons and armor",
        }
    }
    w(os.path.join(DP, "pack.mcmeta"), json.dumps(meta, indent=1))
    # zip
    os.makedirs(DIST, exist_ok=True)
    zpath = os.path.join(DIST, "GoT_Castle_Datapack.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(DP):
            for f in files:
                full = os.path.join(base, f)
                z.write(full, os.path.relpath(full, DP))
    n = sum(len(fs) for _, _, fs in os.walk(DP))
    print("files:", n, "->", zpath)


if __name__ == "__main__":
    main()
