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
    ok = lambda t: f'tellraw @s {{"text":"[OK] {t}","color":"green"}}'
    info = lambda t: f'tellraw @s {{"text":"[..] {t}","color":"yellow"}}'
    fail = lambda t: f'tellraw @s {{"text":"[FAIL] {t}","color":"red"}}'
    L = ['tellraw @s {"text":"--- Game of Thrones self-test ---","color":"gold"}']
    L.append(f'execute if score #state {game.SB} matches 0.. run {ok("scoreboard ready (datapack loaded)")}')
    L.append(f'execute unless score #state {game.SB} matches 0.. run {fail("datapack not loaded - is it enabled? (/datapack list)")}')
    L.append(f'execute store success score #ok {game.SB} run loot give @s loot got:kit/weapons')
    L.append(f'execute if score #ok {game.SB} matches 1 run {ok("loot tables work (you just got a Valyrian sword)")}')
    L.append(f'execute unless score #ok {game.SB} matches 1 run {fail("loot tables did not load")}')
    L.append(f'execute if biome ~ ~ ~ minecraft:snowy_taiga run {ok("you are in the North biome (world map loaded)")}')
    # only meaningful when standing near Winterfell (chunks must be loaded)
    L.append('execute if block 234 64 371 minecraft:chest run ' + ok("Winterfell armory chest found"))
    L.append('execute if block 270 67 331 minecraft:dark_oak_stairs run ' + ok("Winterfell high seat found"))
    L.append('execute unless block 234 64 371 minecraft:chest run ' + info("Winterfell armory not found here (fine if you are far from Winterfell or in a custom world)"))
    L.append(f'execute if entity @e[tag=got_origin] run {ok("a castle battle marker exists (custom-built castle or battle started)")}')
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
    for d in ("advancement", "advancements"):
        w(os.path.join(DP, "data", "got", d, "npc_talk.json"), json.dumps(game.ADVANCEMENT_NPC_TALK, indent=1))
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
