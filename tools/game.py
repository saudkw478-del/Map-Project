"""Game logic (waves, boss, kits) as mcfunction text + loot tables. Namespace: got."""
import json

NS = "got"
SB = "got_g"

# ---------------------------------------------------------------- loot helpers

def _t(text, color="gold"):
    return {"text": text, "color": color, "italic": False}


def item(name, count=1, ench=None, title=None, color="gold", unbreakable=True):
    fns = []
    if count != 1:
        fns.append({"function": "minecraft:set_count", "count": count})
    if title:
        fns.append({"function": "minecraft:set_name", "name": _t(title, color)})
    if ench:
        fns.append({"function": "minecraft:set_enchantments",
                    "enchantments": {f"minecraft:{k}": v for k, v in ench.items()}})
    if unbreakable:
        fns.append({"function": "minecraft:set_components", "components": {"minecraft:unbreakable": {}}})
    e = {"type": "minecraft:item", "name": f"minecraft:{name}"}
    if fns:
        e["functions"] = fns
    return e


def table(*entries):
    """Every entry is its own pool (1 roll) so a table hands out ALL its items."""
    return {"type": "minecraft:chest",
            "pools": [{"rolls": 1, "entries": [e]} for e in entries]}


def food(name, count):
    return item(name, count, unbreakable=False)


def armor_piece(kind, piece, prot, title, color, extra=None):
    ench = {"protection": prot, "unbreaking": 3}
    if extra:
        ench.update(extra)
    return item(f"{kind}_{piece}", ench=ench, title=title, color=color)


SWORD_VS = dict(sharpness=5, fire_aspect=2, looting=3)


def loot_tables():
    T = {}
    # ---- starting kit
    T["kit/weapons"] = table(
        item("netherite_sword", ench=SWORD_VS, title="Valyrian Steel Longsword", color="aqua"),
        item("bow", ench=dict(power=5, flame=1, infinity=1, punch=2), title="Dragonglass Bow", color="dark_purple"),
        item("crossbow", ench=dict(quick_charge=3, piercing=4), title="Scorpion Crossbow", color="gold"),
        item("arrow", 64, unbreakable=False),
        item("arrow", 64, unbreakable=False),
    )
    T["kit/shield"] = table(item("shield", ench=dict(unbreaking=3), title="House Shield", color="red"))
    T["kit/supplies"] = table(food("golden_apple", 16), food("cooked_beef", 64), food("torch", 32))
    for slot, piece, name in (("helmet", "helmet", "Kingsguard Helm"), ("chest", "chestplate", "Kingsguard Plate"),
                              ("legs", "leggings", "Kingsguard Greaves"), ("boots", "boots", "Kingsguard Boots")):
        extra = {"feather_falling": 4} if piece == "boots" else None
        T[f"kit/{slot}"] = table(armor_piece("diamond", piece, 4, name, "white", extra))
    # ---- rewards
    T["reward/supplies"] = table(food("golden_apple", 4), food("cooked_beef", 16), food("arrow", 32))
    T["reward/trophy"] = table(
        item("golden_helmet", ench=dict(protection=4, unbreaking=3), title="Crown of the Seven Kingdoms", color="yellow"),
        food("enchanted_golden_apple", 4),
        food("diamond", 16),
    )
    # ---- armory chests
    T["armory/swords"] = table(
        item("netherite_sword", ench=SWORD_VS, title="Longclaw", color="aqua"),
        item("diamond_sword", ench=dict(sharpness=5, knockback=2, looting=3), title="Ice", color="white"),
        item("iron_sword", ench=dict(sharpness=4, unbreaking=3), title="Needle", color="gray"),
        item("stone_sword", ench=dict(sharpness=5, fire_aspect=2), title="Dragonglass Dagger", color="dark_gray"),
        item("netherite_axe", ench=dict(sharpness=5, efficiency=5), title="Ironborn War Axe", color="dark_red"),
    )
    T["armory/ranged"] = table(
        item("bow", ench=dict(power=5, punch=2, infinity=1), title="Longbow of the North", color="green"),
        item("crossbow", ench=dict(quick_charge=3, multishot=1), title="Heavy Crossbow", color="gold"),
        item("trident", ench=dict(loyalty=3, impaling=5), title="Kraken Spear", color="dark_aqua"),
        food("arrow", 64), food("arrow", 64), food("spectral_arrow", 32),
    )
    T["armory/lannister"] = table(*[
        armor_piece("golden", p, 4, f"Lannister {n}", "gold")
        for p, n in (("helmet", "Helm"), ("chestplate", "Plate"), ("leggings", "Greaves"), ("boots", "Boots"))])
    T["armory/nights_watch"] = table(*[
        armor_piece("iron", p, 4, f"Night's Watch {n}", "dark_gray", {"thorns": 2})
        for p, n in (("helmet", "Helm"), ("chestplate", "Plate"), ("leggings", "Greaves"), ("boots", "Boots"))])
    T["armory/targaryen"] = table(*[
        armor_piece("netherite", p, 4, f"Targaryen {n}", "dark_red")
        for p, n in (("helmet", "Helm"), ("chestplate", "Plate"), ("leggings", "Greaves"), ("boots", "Boots"))])
    T["armory/supplies"] = table(
        food("golden_apple", 32), food("enchanted_golden_apple", 4), food("cooked_beef", 64),
        food("totem_of_undying", 3), food("shield", 4), food("torch", 64))
    return T


# ---------------------------------------------------------------- waves

# (mob, base count, extra per additional player)
WAVES = {
    1: ("Wave 1 - The Wildlings", [("zombie", 6, 2)]),
    2: ("Wave 2 - Raiders from Beyond the Wall", [("zombie", 6, 2), ("skeleton", 4, 1)]),
    3: ("Wave 3 - The Dothraki Horde", [("husk", 6, 2), ("skeleton", 4, 2), ("vindicator", 3, 1)]),
    4: ("Wave 4 - The Ironborn", [("vindicator", 6, 2), ("zombie", 6, 2), ("skeleton", 6, 2)]),
    5: ("Wave 5 - The White Walkers", [("stray", 8, 2), ("zombie", 8, 2), ("wither_skeleton", 2, 1)]),
    6: ("Wave 6 - The Army of the Dead", [("zombie", 12, 3), ("stray", 8, 2), ("wither_skeleton", 4, 1), ("ravager", 1, 1)]),
    7: ("FINAL WAVE - The Night King", [("wither_skeleton", 4, 1), ("stray", 6, 2), ("zombie", 6, 2)]),
}
POINTS = [(-27, 56), (-21, 60), (-15, 56), (-9, 60), (-3, 56), (3, 60), (9, 56), (15, 60), (21, 56), (27, 60)]
MAX_EXTRA_PLAYERS = 7


def json_text(text, color="white", bold=False):
    d = {"text": text, "color": color}
    if bold:
        d["bold"] = True
    return json.dumps(d)


def spawn_cmd(mob, i):
    x, z = POINTS[i % len(POINTS)]
    return f'summon minecraft:{mob} ~{x} ~ ~{z} {{Tags:["got_enemy","got_new"],PersistenceRequired:1b}}'


def wave_functions():
    F = {}
    for n, (title, groups) in WAVES.items():
        inner = []
        idx = 0
        for mob, base, extra in groups:
            for _ in range(base):
                inner.append(spawn_cmd(mob, idx)); idx += 1
            for p in range(2, 2 + MAX_EXTRA_PLAYERS):
                for _ in range(extra):
                    inner.append(f"execute if score #players {SB} matches {p}.. run " + spawn_cmd(mob, idx)); idx += 1
        if n == 7:
            inner.append('summon minecraft:wither ~0 ~22 ~34 {Tags:["got_enemy","got_boss","got_new"],PersistenceRequired:1b}')
        F[f"wave/w{n}_spawn"] = inner
        F[f"wave/w{n}"] = [
            f"title @a title {json_text(title, 'red', True)}",
            f"title @a subtitle {json_text('Enemies are gathering outside the main gate!' if n < 7 else 'The Night King has come. Hold the castle!', 'gray')}",
            "playsound minecraft:entity.wither.spawn master @a" if n == 7 else "playsound minecraft:block.bell.use master @a",
            f"execute at @e[tag=got_origin,limit=1] run function {NS}:wave/w{n}_spawn",
            f"execute as @e[tag=got_new] at @s run function {NS}:game/equip",
        ]
    return F


TIERS = [((1, 2), "leather", False), ((3, 4), "chainmail", True), ((5, 5), "iron", True), ((6, 7), "diamond", True)]
GEAR_MOBS = ["zombie", "husk", "skeleton", "stray", "vindicator"]


def game_functions():
    F = {}
    F["load"] = [
        f'scoreboard objectives add {SB} dummy {json_text("Game of Thrones", "gold")}',
        "team add got_enemies",
        "team modify got_enemies color red",
        f'tellraw @a {json.dumps([{"text": "[Game of Thrones Castle] ", "color": "gold"}, {"text": "Datapack loaded. Type /function got:help", "color": "white"}])}',
    ]
    F["tick"] = [f"execute if score #state {SB} matches 1..2 run function {NS}:game/loop"]
    F["help"] = [
        f'tellraw @s {json.dumps({"text": t, "color": c}) }' for t, c in [
            ("=== Game of Thrones Castle ===", "gold"),
            ("/function got:build        - build the castle where you stand (flat ground)", "white"),
            ("/function got:game/start   - start the waves + boss (gives everyone weapons and armor)", "white"),
            ("/function got:game/stop    - stop the game", "white"),
            ("/function got:kit/give     - give yourself the starter kit again", "white"),
            ("/function got:tp/hall      - teleport everyone to the throne room", "white"),
            ("/function got:tp/gate      - teleport everyone to the main gate", "white"),
            ("/function got:tp/roof      - teleport everyone to the keep roof", "white"),
        ]]
    # ---- build
    F["build"] = [
        "kill @e[tag=got_origin]", "kill @e[tag=got_gate]", "kill @e[tag=got_center]",
        'execute align xyz run summon minecraft:marker ~ ~ ~ {Tags:["got_origin"]}',
        f'tellraw @a {json.dumps({"text": "Building the castle... stay near the center for ~20 seconds.", "color": "yellow"})}',
        "execute at @e[tag=got_origin,limit=1] run forceload add ~-60 ~-60 ~60 ~60",
        f"schedule function {NS}:build/s1_ground 40t",
    ]
    # ---- teleports
    F["tp/hall"] = ["execute at @e[tag=got_origin,limit=1] run tp @a ~ ~ ~4"]
    F["tp/gate"] = ["execute at @e[tag=got_origin,limit=1] run tp @a ~ ~ ~38"]
    F["tp/roof"] = ["execute at @e[tag=got_origin,limit=1] run tp @a ~ ~21 ~-6"]
    # ---- game rules (one macro function per command: an unknown rule name only fails that one)
    rules = [("mobGriefing", "mob_griefing", "false"), ("keepInventory", "keep_inventory", "true"),
             ("doMobSpawning", "spawn_mobs", "false")]
    calls = []
    for old, new, val in rules:
        for tag, name in (("old", old), ("new", new)):
            fn = f"util/rule_{old.lower()}_{tag}"
            F[fn] = [f"$gamerule {name} $(v)"]
            calls.append(f'function {NS}:{fn} {{v:"{val}"}}')
    F["util/rules"] = calls
    # ---- game flow
    F["game/start"] = [
        f'execute unless entity @e[tag=got_origin] run return run tellraw @s {json.dumps({"text": "Build the castle first: /function got:build", "color": "red"})}',
        "kill @e[tag=got_enemy]",
        f'scoreboard objectives add {SB} dummy {json_text("Game of Thrones", "gold")}',
        f"scoreboard players set #state {SB} 2",
        f"scoreboard players set #cool {SB} 12",
        f"scoreboard players set #wave {SB} 0",
        f"scoreboard players set #t {SB} 0",
        f"scoreboard players set Wave {SB} 0",
        f"scoreboard players set Enemies {SB} 0",
        f"scoreboard objectives setdisplay sidebar {SB}",
        "difficulty normal", "time set night", "weather clear",
        f"function {NS}:util/rules",
        "execute at @e[tag=got_origin,limit=1] run spawnpoint @a ~ ~ ~4",
        f"function {NS}:tp/hall",
        f"execute as @a run function {NS}:kit/give",
        f'title @a title {json_text("The Long Night Begins", "dark_red", True)}',
        f'title @a subtitle {json_text("Hold the castle through 7 waves. Slay the Night King!", "gray")}',
        "playsound minecraft:ambient.cave master @a",
    ]
    F["game/stop"] = [
        "kill @e[tag=got_enemy]",
        f"scoreboard players set #state {SB} 0",
        "scoreboard objectives setdisplay sidebar",
        f'tellraw @a {json.dumps({"text": "Game stopped.", "color": "gray"})}',
    ]
    F["game/loop"] = [
        f"scoreboard players add #t {SB} 1",
        f"execute if score #t {SB} matches 20.. run function {NS}:game/second",
    ]
    F["game/second"] = [
        f"scoreboard players set #t {SB} 0",
        f"execute store result score #players {SB} if entity @a",
        f"execute store result score #enemies {SB} if entity @e[tag=got_enemy]",
        f"scoreboard players operation Enemies {SB} = #enemies {SB}",
        f"execute if score #state {SB} matches 1 run function {NS}:game/running",
        f"execute if score #state {SB} matches 2 run function {NS}:game/intermission",
    ]
    F["game/running"] = [
        f"execute if score #enemies {SB} matches 1..5 run effect give @e[tag=got_enemy] minecraft:glowing 3 0 true",
        f"execute as @e[tag=got_enemy,tag=!got_boss] at @s unless entity @a[distance=..30] run function {NS}:game/march",
        f"execute if score #enemies {SB} matches 0 run function {NS}:game/wave_clear",
    ]
    F["game/march"] = [
        "execute facing entity @p feet positioned ^ ^ ^6 if block ~ ~ ~ air if block ~ ~1 ~ air unless block ~ ~-1 ~ air run tp @s ~ ~ ~",
    ]
    F["game/wave_clear"] = [
        f"execute if score #wave {SB} matches 7.. run return run function {NS}:game/victory",
        f"scoreboard players set #state {SB} 2",
        f"scoreboard players set #cool {SB} 15",
        f'title @a title {json_text("Wave cleared!", "green", True)}',
        "effect give @a minecraft:regeneration 10 1 true",
        "effect give @a minecraft:instant_health 1 2 true",
        f"loot give @a loot {NS}:reward/supplies",
        "playsound minecraft:entity.player.levelup master @a",
    ]
    F["game/intermission"] = [
        f"scoreboard players remove #cool {SB} 1",
        f'execute if score #cool {SB} matches 1..10 run title @a actionbar {json.dumps([{"text": "Next wave in ", "color": "yellow"}, {"score": {"name": "#cool", "objective": SB}, "color": "gold"}, {"text": " s", "color": "yellow"}])}',
        f"execute if score #cool {SB} matches ..0 run function {NS}:game/next_wave",
    ]
    F["game/next_wave"] = [
        f"scoreboard players add #wave {SB} 1",
        f"scoreboard players operation Wave {SB} = #wave {SB}",
        f"scoreboard players set #state {SB} 1",
    ] + [f"execute if score #wave {SB} matches {n} run function {NS}:wave/w{n}" for n in WAVES]
    F["game/victory"] = [
        f"scoreboard players set #state {SB} 4",
        f'title @a title {json_text("VICTORY!", "gold", True)}',
        f'title @a subtitle {json_text("The Night King has fallen. The realm is saved!", "aqua")}',
        "effect give @a minecraft:regeneration 30 2 true",
        "xp add @a 30 levels",
        f"loot give @a loot {NS}:reward/trophy",
        "playsound minecraft:ui.toast.challenge_complete master @a",
        f'tellraw @a {json.dumps({"text": "You can stop with /function got:game/stop or start again with /function got:game/start", "color": "gray"})}',
    ]
    # ---- equip enemies (runs as/at each new enemy)
    eq = [f"execute if entity @s[type=minecraft:{m}] run function {NS}:wave/gear" for m in GEAR_MOBS]
    eq += ["team join got_enemies @s", "tag @s remove got_new"]
    F["game/equip"] = eq
    gear = []
    for (lo, hi), mat, chest in TIERS:
        gear.append(f"execute if score #wave {SB} matches {lo}..{hi} run item replace entity @s armor.head with minecraft:{mat}_helmet")
        if chest:
            gear.append(f"execute if score #wave {SB} matches {lo}..{hi} run item replace entity @s armor.chest with minecraft:{mat}_chestplate")
    for m in ("zombie", "husk"):
        gear.append(f"execute if entity @s[type=minecraft:{m}] if score #wave {SB} matches 3..5 run item replace entity @s weapon.mainhand with minecraft:iron_sword")
        gear.append(f"execute if entity @s[type=minecraft:{m}] if score #wave {SB} matches 6.. run item replace entity @s weapon.mainhand with minecraft:diamond_sword")
    F["wave/gear"] = gear
    # ---- kit
    F["kit/give"] = [
        f"loot give @s loot {NS}:kit/weapons",
        f"loot give @s loot {NS}:kit/supplies",
        f"loot replace entity @s armor.head loot {NS}:kit/helmet",
        f"loot replace entity @s armor.chest loot {NS}:kit/chest",
        f"loot replace entity @s armor.legs loot {NS}:kit/legs",
        f"loot replace entity @s armor.feet loot {NS}:kit/boots",
        f"loot replace entity @s weapon.offhand loot {NS}:kit/shield",
    ]
    F.update(wave_functions())
    return F


# ---------------------------------------------------------------- build stage glue

CHEST_LOOT = [("swords", -36), ("ranged", -34), ("lannister", -32), ("nights_watch", -30), ("targaryen", -28), ("supplies", -26)]


def stage_wrap(name, next_name, delay, extra_after=()):
    """Outer function (no position) -> runs the inner commands at the origin marker, then schedules the next stage."""
    lines = [f"execute at @e[tag=got_origin,limit=1] run function {NS}:build/{name}_a"]
    lines += list(extra_after)
    if next_name:
        lines.append(f"schedule function {NS}:build/{next_name} {delay}t")
    return lines


def loot_fill_lines():
    return [f"loot insert ~{x} ~ ~21 loot {NS}:armory/{t}" for t, x in CHEST_LOOT]


def finish_lines():
    return [
        "execute at @e[tag=got_origin,limit=1] run forceload remove ~-60 ~-60 ~60 ~60",
        f"function {NS}:util/rules",
        f'tellraw @a {json.dumps([{"text": "The castle is ready! ", "color": "green", "bold": True}, {"text": "Weapons & armor are in the armory (west courtyard). Start the game: /function got:game/start", "color": "white"}])}',
    ]
