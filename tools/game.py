"""Game logic (waves, boss, kits) as mcfunction text + loot tables. Namespace: got."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "world"))
import geo  # noqa: E402

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
    T["kit/travel"] = table(
        item("elytra", ench=dict(unbreaking=3), title="Wings of Drogon", color="dark_red"),
        food("firework_rocket", 64), food("saddle", 1), food("horse_spawn_egg", 2), food("golden_carrot", 16))
    return T



# ---------------------------------------------------------------- waves / themes

# theme -> (id, gear base, waves); wave = (title, [(mob, base count, extra per additional player)])
Z, SK, HU, ST, VI, WS, RV, PI, EV, WI, CR, WI2 = ("zombie", "skeleton", "husk", "stray", "vindicator", "wither_skeleton",
                                                  "ravager", "pillager", "evoker", "witch", "creeper", "spider")
THEMES = {
    "wildlings": (1, 0, [
        ("The Wildlings Climb the Wall", [(Z, 6, 2)]),
        ("Raiders from Beyond", [(Z, 6, 2), (SK, 4, 1)]),
        ("Thenn Warriors", [(HU, 6, 2), (SK, 4, 2), (VI, 2, 1)]),
        ("Mammoth Riders", [(VI, 5, 2), (Z, 8, 2), (RV, 1, 1)]),
    ]),
    "long_night": (2, 2, [
        ("Wave 1 - The Wildlings", [(Z, 6, 2)]),
        ("Wave 2 - Raiders from Beyond the Wall", [(Z, 6, 2), (SK, 4, 1)]),
        ("Wave 3 - The Dothraki Horde", [(HU, 6, 2), (SK, 4, 2), (VI, 3, 1)]),
        ("Wave 4 - The Ironborn", [(VI, 6, 2), (Z, 6, 2), (SK, 6, 2)]),
        ("Wave 5 - The White Walkers", [(ST, 8, 2), (Z, 8, 2), (WS, 2, 1)]),
        ("Wave 6 - The Army of the Dead", [(Z, 12, 3), (ST, 8, 2), (WS, 4, 1), (RV, 1, 1)]),
        ("FINAL WAVE - The Night King", [(WS, 4, 1), (ST, 6, 2), (Z, 6, 2)]),
    ]),
    "freys": (3, 1, [
        ("The Red Wedding Guests", [(VI, 5, 2), (Z, 6, 2)]),
        ("Frey Crossbowmen", [(PI, 5, 2), (VI, 4, 1)]),
        ("The Twins Reinforcements", [(PI, 5, 2), (VI, 6, 2), (Z, 6, 2)]),
        ("Walder's Vengeance", [(EV, 2, 1), (VI, 6, 2), (PI, 4, 1)]),
    ]),
    "mountain": (4, 1, [
        ("Mountain Clansmen", [(SK, 6, 2), (Z, 6, 2)]),
        ("The Bloody Gate", [(HU, 6, 2), (VI, 4, 1), (SK, 4, 1)]),
        ("Ser Gregor's Men", [(VI, 6, 2), (WS, 3, 1), (RV, 1, 1)]),
    ]),
    "blackwater": (5, 2, [
        ("Stannis Lands at the Blackwater", [(Z, 8, 2), (VI, 3, 1)]),
        ("Wildfire Arrows", [(SK, 6, 2), (CR, 4, 1), (Z, 6, 2)]),
        ("Siege Towers", [(VI, 6, 2), (Z, 8, 2), (CR, 4, 1)]),
        ("The Green Fire", [(CR, 8, 2), (SK, 6, 2), (WS, 2, 1)]),
        ("The Mountain Rides", [(RV, 2, 1), (VI, 6, 2), (Z, 8, 2)]),
    ]),
    "lannister": (6, 2, [
        ("Raiders on the Goldroad", [(SK, 6, 2), (Z, 6, 2)]),
        ("Rebel Army", [(VI, 6, 2), (SK, 6, 2)]),
        ("Ghosts of the Rock", [(WS, 4, 1), (SK, 6, 2), (Z, 6, 2)]),
        ("The Lion's Den", [(WS, 6, 2), (VI, 6, 2), (RV, 1, 1)]),
    ]),
    "reach": (7, 1, [
        ("Rebels Storm the Garden", [(Z, 8, 2), (WI2, 4, 1)]),
        ("Poisoned Roses", [(WI, 3, 1), (SK, 6, 2), (Z, 6, 2)]),
        ("The Reach Army", [(VI, 6, 2), (Z, 8, 2), (SK, 6, 2)]),
        ("The Tyrell Feast Ambush", [(EV, 2, 1), (VI, 6, 2), (PI, 4, 1)]),
    ]),
    "storm": (8, 2, [
        ("The Storm Gathers", [(Z, 8, 2), (SK, 4, 2)]),
        ("The Siege of Storm's End", [(VI, 6, 2), (Z, 8, 2)]),
        ("Shadow Baby", [(WS, 3, 1), (SK, 6, 2), (Z, 6, 2)]),
        ("Stannis Rises", [(VI, 6, 2), (WS, 4, 1), (SK, 6, 2)]),
        ("The Red Priestess' Fire", [(RV, 2, 1), (CR, 6, 2), (Z, 8, 2)]),
    ]),
    "dorne": (9, 2, [
        ("Sand Snakes Attack", [(HU, 8, 2), (SK, 4, 1)]),
        ("The Spear's Guardians", [(HU, 6, 2), (VI, 4, 2), (SK, 6, 2)]),
        ("The Red Viper", [(VI, 6, 2), (WS, 3, 1), (HU, 6, 2)]),
        ("Desert Reavers", [(RV, 2, 1), (HU, 10, 3), (SK, 6, 2)]),
    ]),
}
POINTS = [(-27, 56), (-21, 60), (-15, 56), (-9, 60), (-3, 56), (3, 60), (9, 56), (15, 60), (21, 56), (27, 60)]
MAX_EXTRA_PLAYERS = 7


def json_text(text, color="white", bold=False):
    d = {"text": text, "color": color}
    if bold:
        d["bold"] = True
    return json.dumps(d)


def tell(text, color="white", bold=False):
    return f"tellraw @s {json_text(text, color, bold)}"


def spawn_cmd(mob, i):
    x, z = POINTS[i % len(POINTS)]
    return f'summon minecraft:{mob} ~{x} ~ ~{z} {{Tags:["got_enemy","got_new"],PersistenceRequired:1b}}'


def wave_functions():
    F = {}
    for theme, (tid, base, waves) in THEMES.items():
        for n, (title, groups) in enumerate(waves, start=1):
            final = n == len(waves)
            inner, idx = [], 0
            for mob, cnt, extra in groups:
                for _ in range(cnt):
                    inner.append(spawn_cmd(mob, idx)); idx += 1
                for p in range(2, 2 + MAX_EXTRA_PLAYERS):
                    for _ in range(extra):
                        inner.append(f"execute if score #players {SB} matches {p}.. run " + spawn_cmd(mob, idx)); idx += 1
            if theme == "long_night" and final:
                inner.append('summon minecraft:wither ~0 ~22 ~34 {Tags:["got_enemy","got_boss","got_new"],PersistenceRequired:1b}')
            F[f"wave/{theme}_{n}_spawn"] = inner
            F[f"wave/{theme}_{n}"] = [
                f'title @a title {json_text(title, "red", True)}',
                f'title @a subtitle {json_text(("Final wave! Hold the castle!" if final else f"Wave {n} of {len(waves)}"), "gray")}',
                ("playsound minecraft:entity.wither.spawn master @a" if final else "playsound minecraft:block.bell.use master @a"),
                f"execute at @e[tag=got_origin,limit=1] run function {NS}:wave/{theme}_{n}_spawn",
                f"execute as @e[tag=got_new] at @s run function {NS}:game/equip",
            ]
    return F


TIERS = [((0, 2), "leather", False), ((3, 4), "chainmail", True), ((5, 6), "iron", True), ((7, 99), "diamond", True)]
GEAR_MOBS = ["zombie", "husk", "skeleton", "stray", "vindicator", "pillager"]

# ---------------------------------------------------------------- sites and travel

STORY_ORDER = ["castle_black", "riverrun", "kings_landing", "casterly_rock", "highgarden", "storms_end", "eyrie",
               "sunspear", "winterfell"]
BATTLE_SITES = {s.key: s for s in geo.SITES}

# id -> (title, mode, x, y, z); mode "tp" = exact spot, "spread" = find the surface
DESTS = []
for s in geo.SITES:
    DESTS.append((s.name, "tp", s.x, s.y0, s.z + 32, s.key))
DESTS += [
    ("Top of the Wall", "tp", 258, 136, 174, None),
    ("Beyond the Wall (Haunted Forest)", "spread", 250, 0, 90, None),
    ("Moat Cailin", "spread", 315, 0, 620, None),
    ("The Twins", "spread", 300, 0, 690, None),
    ("Harrenhal", "spread", 340, 0, 830, None),
    ("Dragonstone", "spread", 540, 0, 822, None),
    ("Pyke (Iron Islands)", "spread", 70, 0, 660, None),
    ("Oldtown - the Hightower", "spread", 135, 0, 1200, None),
    ("White Harbor", "spread", 395, 0, 500, None),
]
DEST_BASE = 2   # /trigger got_go set N  (1 = menu)


def region_lines():
    order = ["beyond", "north", "neck", "iron", "riverlands", "vale", "westerlands", "crownlands", "stormlands", "reach", "dorne"]
    L = []
    for i, r in enumerate(order, start=1):
        biome = geo.REGION_BIOME[r]
        L.append(f"execute if biome ~ ~ ~ {biome} unless score @s got_reg matches {i} run function {NS}:region/enter_{i}")
    return order, L


def game_functions():
    F = {}
    order, region_checks = region_lines()
    F["load"] = [
        f'scoreboard objectives add {SB} dummy {json_text("Game of Thrones", "gold")}',
        "scoreboard objectives add got_go trigger",
        "scoreboard objectives add got_battle trigger",
        "scoreboard objectives add got_kit trigger",
        "scoreboard objectives add got_reg dummy",
        "team add got_enemies",
        "team modify got_enemies color red",
        f"execute unless score #state {SB} matches 0.. run scoreboard players set #state {SB} 0",
        f"function {NS}:util/rules",
        f'tellraw @a {json.dumps([{"text": "[Game of Thrones] ", "color": "gold"}, {"text": "Westeros is ready. Type /trigger got_go to travel.", "color": "white"}])}',
    ]
    F["tick"] = [
        "scoreboard players enable @a got_go",
        "scoreboard players enable @a got_battle",
        "scoreboard players enable @a got_kit",
        f"execute as @a[tag=!got_seen] run function {NS}:player/first_join",
        f"execute as @a[scores={{got_go=1..}}] run function {NS}:travel/handle",
        f"execute as @a[scores={{got_battle=1..}}] run function {NS}:battle/handle",
        f"execute as @a[scores={{got_kit=1..}}] run function {NS}:kit/handle",
        f"scoreboard players add #rt {SB} 1",
        f"execute if score #rt {SB} matches 20.. run function {NS}:region/check",
        f"execute if score #state {SB} matches 1..2 run function {NS}:game/loop",
    ]
    F["help"] = [tell(t, c) for t, c in [
        ("=== Game of Thrones: Westeros ===", "gold"),
        ("/trigger got_go            - travel menu (then /trigger got_go set N)", "white"),
        ("/trigger got_battle        - start the battle at the castle you stand in", "white"),
        ("/trigger got_battle set 2  - stop the battle", "white"),
        ("/trigger got_kit           - get your weapons and armor again", "white"),
        ("/trigger got_kit set 2     - travel kit (wings, horse egg)", "white"),
    ]]
    # ---- first join
    F["player/first_join"] = [
        "tag @s add got_seen",
        tell("Winter is coming.", "aqua", True),
        tell("You stand in Winterfell, seat of House Stark. The realm of Westeros lies before you:", "white"),
        tell("the Wall in the north, the Iron Throne in King's Landing, and the sun-scorched land of Dorne far in the south.", "white"),
        tell("Conquer each great castle in battle - and when the Night King comes, hold Winterfell.", "yellow"),
        tell("Type /trigger got_go to travel, /trigger got_battle to fight, /trigger got_kit for gear.", "green"),
        f"function {NS}:kit/give",
        f"function {NS}:kit/give_travel",
    ]
    # ---- travel
    handle = [f"execute if score @s got_go matches 1 run function {NS}:travel/menu"]
    menu = [tell("=== Travel (type /trigger got_go set N) ===", "gold", True)]
    story_num = {k: i + 1 for i, k in enumerate(STORY_ORDER)}
    for i, (name, mode, x, y, z, key) in enumerate(DESTS):
        n = DEST_BASE + i
        handle.append(f"execute if score @s got_go matches {n} run function {NS}:travel/d{n}")
        if mode == "tp":
            body = [f"tp @s {x} {y} {z}", f"spawnpoint @s {x} {y} {z}"]
        else:
            body = [f"spreadplayers {x} {z} 0 3 false @s"]
        F[f"travel/d{n}"] = body + [
            f'title @s actionbar {json_text("Travelling to " + name, "yellow")}',
            "playsound minecraft:entity.enderman.teleport master @s",
        ]
        line = f"{n} - {name}"
        if key:
            line += f"  (battle #{story_num[key]})"
            menu.append(f'execute unless score #won_{key} {SB} matches 1 run tellraw @s {json.dumps({"text": line, "color": "white"})}')
            menu.append(f'execute if score #won_{key} {SB} matches 1 run tellraw @s {json.dumps([{"text": line + " ", "color": "gray"}, {"text": "[conquered]", "color": "green"}])}')
        else:
            menu.append(tell(line, "white"))
    menu.append(tell("Recommended order of battles: " + " > ".join(BATTLE_SITES[k].name for k in STORY_ORDER), "aqua"))
    handle.append(f"scoreboard players set @s got_go 0")
    F["travel/handle"] = handle
    F["travel/menu"] = menu
    # ---- regions
    F["region/check"] = [f"scoreboard players set #rt {SB} 0", f"execute as @a at @s run function {NS}:region/one"]
    F["region/one"] = region_checks
    subtitles = {
        "beyond": "Where the dead walk", "north": "Winter is coming", "neck": "Swamps and lizard-lions",
        "iron": "We do not sow", "riverlands": "Family, Duty, Honor", "vale": "As high as honor",
        "westerlands": "Hear me roar", "crownlands": "The seat of the Iron Throne", "stormlands": "Ours is the Fury",
        "reach": "Growing strong", "dorne": "Unbowed, unbent, unbroken",
    }
    for i, r in enumerate(order, start=1):
        F[f"region/enter_{i}"] = [
            f"scoreboard players set @s got_reg {i}",
            "title @s times 10 50 15",
            f'title @s subtitle {json_text(subtitles[r], "gray")}',
            f'title @s title {json_text(geo.REGION_TITLE[r], "gold", True)}',
        ]
    # ---- kits
    F["kit/give"] = [
        f"loot give @s loot {NS}:kit/weapons",
        f"loot give @s loot {NS}:kit/supplies",
        f"loot replace entity @s armor.head loot {NS}:kit/helmet",
        f"loot replace entity @s armor.chest loot {NS}:kit/chest",
        f"loot replace entity @s armor.legs loot {NS}:kit/legs",
        f"loot replace entity @s armor.feet loot {NS}:kit/boots",
        f"loot replace entity @s weapon.offhand loot {NS}:kit/shield",
    ]
    F["kit/give_travel"] = [f"loot give @s loot {NS}:kit/travel"]
    F["kit/handle"] = [
        f"execute if score @s got_kit matches 1 run function {NS}:kit/give",
        f"execute if score @s got_kit matches 2 run function {NS}:kit/give_travel",
        "scoreboard players set @s got_kit 0",
    ]
    # ---- battles
    bh = [
        f"execute if score @s got_battle matches 2 run function {NS}:game/stop",
        f"execute if score @s got_battle matches 1 run function {NS}:battle/try",
        "scoreboard players set @s got_battle 0",
    ]
    F["battle/handle"] = bh
    try_lines = [
        f"execute unless score #state {SB} matches 0 unless score #state {SB} matches 4 run return run " + tell("A battle is already in progress! (/trigger got_battle set 2 stops it)", "red"),
    ]
    for s in geo.SITES:
        try_lines.append(f"execute positioned {s.x} {s.y0} {s.z} if entity @s[distance=..80] run return run function {NS}:battle/start_{s.key}")
    try_lines.append(tell("Stand inside a great castle (within its walls) to start its battle.", "yellow"))
    F["battle/try"] = try_lines
    theme_of_site = {s.key: s.waves for s in geo.SITES}
    for i, s in enumerate(geo.SITES, start=1):
        tid, base, waves = THEMES[theme_of_site[s.key]]
        F[f"battle/start_{s.key}"] = [
            "kill @e[tag=got_origin]",
            f'summon minecraft:marker {s.x} {s.y0} {s.z} {{Tags:["got_origin"]}}',
            f"scoreboard players set #site {SB} {i}",
            f"scoreboard players set #theme {SB} {tid}",
            f"scoreboard players set #base {SB} {base}",
            f"scoreboard players set #total {SB} {len(waves)}",
            f'tellraw @a {json.dumps([{"text": "[BATTLE] ", "color": "red", "bold": True}, {"text": s.name + ": " + s.blurb, "color": "white"}])}',
            f"function {NS}:battle/begin",
        ]
    F["battle/begin"] = [
        "kill @e[tag=got_enemy]",
        f'scoreboard objectives add {SB} dummy {json_text("Game of Thrones", "gold")}',
        f"scoreboard players set #state {SB} 2",
        f"scoreboard players set #cool {SB} 12",
        f"scoreboard players set #wave {SB} 0",
        f"scoreboard players set #t {SB} 0",
        f"scoreboard players set Wave {SB} 0",
        f"scoreboard players set Enemies {SB} 0",
        f"scoreboard objectives setdisplay sidebar {SB}",
        "difficulty normal", "weather clear",
        f"function {NS}:util/rules",
        "execute at @e[tag=got_origin,limit=1] as @a[distance=..130] run spawnpoint @s ~ ~ ~4",
        f"execute at @e[tag=got_origin,limit=1] as @a[distance=..130] run function {NS}:battle/prepare",
        f'title @a title {json_text("To Arms!", "dark_red", True)}',
        f'title @a subtitle {json_text("Defend the castle. Grab weapons from the armory!", "gray")}',
    ]
    F["battle/prepare"] = [
        "tp @s ~ ~ ~4",
        f"function {NS}:kit/give",
    ]
    # custom worlds (castle built with /function got:build): full 7-wave Long Night at the built castle
    F["game/start"] = [
        f'execute unless entity @e[tag=got_origin] run return run tellraw @s {json.dumps({"text": "Build the castle first: /function got:build", "color": "red"})}',
        f"scoreboard players set #site {SB} 2",
        f"scoreboard players set #theme {SB} 2",
        f"scoreboard players set #base {SB} 2",
        f"scoreboard players set #total {SB} {len(THEMES['long_night'][2])}",
        f"function {NS}:battle/begin",
    ]
    F["game/stop"] = [
        "kill @e[tag=got_enemy]",
        f"scoreboard players set #state {SB} 0",
        "scoreboard objectives setdisplay sidebar",
        f'tellraw @a {json.dumps({"text": "The battle has been stopped.", "color": "gray"})}',
    ]
    # ---- build (optional: build one castle wherever you stand in a normal world)
    F["build"] = [
        "kill @e[tag=got_origin]", "kill @e[tag=got_gate]", "kill @e[tag=got_center]",
        'execute align xyz run summon minecraft:marker ~ ~ ~ {Tags:["got_origin"]}',
        f'tellraw @a {json.dumps({"text": "Building the castle... stay near the center for ~20 seconds.", "color": "yellow"})}',
        "execute at @e[tag=got_origin,limit=1] run forceload add ~-60 ~-60 ~60 ~60",
        f"schedule function {NS}:build/s1_ground 40t",
    ]
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
        f"execute if score #wave {SB} >= #total {SB} run return run function {NS}:game/victory",
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
    nw = [
        f"scoreboard players add #wave {SB} 1",
        f"scoreboard players operation Wave {SB} = #wave {SB}",
        f"scoreboard players operation #gear {SB} = #wave {SB}",
        f"scoreboard players operation #gear {SB} += #base {SB}",
        f"scoreboard players set #state {SB} 1",
    ]
    for theme, (tid, base, waves) in THEMES.items():
        for n in range(1, len(waves) + 1):
            nw.append(f"execute if score #theme {SB} matches {tid} if score #wave {SB} matches {n} run function {NS}:wave/{theme}_{n}")
    F["game/next_wave"] = nw
    victory = [
        f"scoreboard players set #state {SB} 4",
        f'title @a title {json_text("VICTORY!", "gold", True)}',
        f'title @a subtitle {json_text("The castle is held!", "aqua")}',
        "effect give @a minecraft:regeneration 30 2 true",
        "xp add @a 30 levels",
        f"loot give @a loot {NS}:reward/trophy",
        "playsound minecraft:ui.toast.challenge_complete master @a",
        f"scoreboard players add Victories {SB} 1",
    ]
    for i, s in enumerate(geo.SITES, start=1):
        victory.append(f"execute if score #site {SB} matches {i} run scoreboard players set #won_{s.key} {SB} 1")
    victory += [
        f'tellraw @a {json.dumps([{"text": "Castles conquered: ", "color": "gold"}, {"score": {"name": "Victories", "objective": SB}, "color": "white"}, {"text": " of " + str(len(geo.SITES)), "color": "gold"}])}',
        f"execute if score #won_winterfell {SB} matches 1 if score #won_kings_landing {SB} matches 1 if score #won_castle_black {SB} matches 1 run tellraw @a {json.dumps({'text': 'The realm is saved! The Long Night is over and the Iron Throne is safe.', 'color': 'yellow', 'bold': True})}",
        f'tellraw @a {json.dumps({"text": "Start another battle with /trigger got_battle (or travel with /trigger got_go).", "color": "gray"})}',
    ]
    F["game/victory"] = victory
    # ---- equip enemies (runs as/at each new enemy)
    eq = [f"execute if entity @s[type=minecraft:{m}] run function {NS}:wave/gear" for m in GEAR_MOBS]
    eq += ["team join got_enemies @s", "tag @s remove got_new"]
    F["game/equip"] = eq
    gear = []
    for (lo, hi), mat, chest in TIERS:
        gear.append(f"execute if score #gear {SB} matches {lo}..{hi} run item replace entity @s armor.head with minecraft:{mat}_helmet")
        if chest:
            gear.append(f"execute if score #gear {SB} matches {lo}..{hi} run item replace entity @s armor.chest with minecraft:{mat}_chestplate")
    for m in ("zombie", "husk"):
        gear.append(f"execute if entity @s[type=minecraft:{m}] if score #gear {SB} matches 3..5 run item replace entity @s weapon.mainhand with minecraft:iron_sword")
        gear.append(f"execute if entity @s[type=minecraft:{m}] if score #gear {SB} matches 6.. run item replace entity @s weapon.mainhand with minecraft:diamond_sword")
    F["wave/gear"] = gear
    F.update(wave_functions())
    return F


# ---------------------------------------------------------------- build stage glue (optional /function got:build)

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
