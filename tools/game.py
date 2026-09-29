"""Game logic v2 (Arabic): campaign 'The Long Night is coming', houses, powers, shop, scout, NPCs, battles.
Namespace: got.  All player-facing text is Arabic."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "world"))
sys.path.insert(0, HERE)
import geo  # noqa: E402
import ar   # noqa: E402

NS = "got"
SB = "got_g"
HUD = "got_hud"


# ---------------------------------------------------------------- text helpers

def J(obj):
    return json.dumps(obj)          # ASCII-escaped: safe inside .mcfunction files


def T(text, color="white", bold=False, italic=None):
    d = {"text": text, "color": color}
    if bold:
        d["bold"] = True
    if italic is not None:
        d["italic"] = italic
    return d


def tell(text, color="white", bold=False, to="@s"):
    return f"tellraw {to} {J(T(text, color, bold))}"


def tellc(parts, to="@s"):
    return f"tellraw {to} {J(parts)}"


def score(name, obj=SB, color="white"):
    return {"score": {"name": name, "objective": obj}, "color": color}


def title(text, color="white", bold=True, to="@a"):
    return f"title {to} title {J(T(text, color, bold))}"


def subtitle(text, color="gray", to="@a"):
    return f"title {to} subtitle {J(T(text, color))}"


def actionbar(text, color="yellow", to="@a"):
    return f"title {to} actionbar {J(T(text, color))}"


# ---------------------------------------------------------------- loot (Arabic names)

def _t(text, color="gold"):
    return {"text": text, "color": color, "italic": False}


def item(name, count=1, ench=None, title_=None, color="gold", unbreakable=True):
    fns = []
    if count != 1:
        fns.append({"function": "minecraft:set_count", "count": count})
    if title_:
        fns.append({"function": "minecraft:set_name", "name": _t(title_, color)})
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
    return {"type": "minecraft:chest", "pools": [{"rolls": 1, "entries": [e]} for e in entries]}


def pick(*entries, rolls=1):
    """One pool: random pick(s) among the entries (weights equal)."""
    return {"type": "minecraft:chest", "pools": [{"rolls": rolls, "entries": list(entries)}]}


def food(name, count):
    return item(name, count, unbreakable=False)


def armor_piece(kind, piece, prot, title_, color, extra=None):
    ench = {"protection": prot, "unbreaking": 3}
    if extra:
        ench.update(extra)
    return item(f"{kind}_{piece}", ench=ench, title_=title_, color=color)


SWORD_VS = dict(sharpness=5, fire_aspect=2, looting=3)
PIECES = (("helmet", "خوذة"), ("chestplate", "درع الصدر"), ("leggings", "واقي الساقين"), ("boots", "حذاء"))


def loot_tables():
    T_ = {}
    # ---- starting kit
    T_["kit/weapons"] = table(
        item("netherite_sword", ench=SWORD_VS, title_="سيف الفولاذ الفاليري", color="aqua"),
        item("bow", ench=dict(power=5, flame=1, infinity=1, punch=2), title_="قوس الزجاج التنيني", color="dark_purple"),
        item("crossbow", ench=dict(quick_charge=3, piercing=4), title_="العقرب - نشّابة", color="gold"),
        item("arrow", 64, unbreakable=False),
        item("arrow", 64, unbreakable=False),
    )
    T_["kit/shield"] = table(item("shield", ench=dict(unbreaking=3), title_="درع البيت", color="red"))
    T_["kit/supplies"] = table(food("golden_apple", 16), food("cooked_beef", 64), food("torch", 32))
    for slot, (piece, ar_name) in zip(("helmet", "chest", "legs", "boots"), PIECES):
        extra = {"feather_falling": 4} if piece == "boots" else None
        T_[f"kit/{slot}"] = table(armor_piece("diamond", piece, 4, f"{ar_name} الحرس الملكي", "white", extra))
    T_["kit/travel"] = table(
        item("elytra", ench=dict(unbreaking=3), title_="أجنحة التنين", color="dark_red"),
        food("firework_rocket", 64), food("saddle", 1), food("horse_spawn_egg", 2), food("golden_carrot", 16))
    # ---- rewards
    T_["reward/supplies"] = table(food("golden_apple", 4), food("cooked_beef", 16), food("arrow", 32))
    T_["reward/trophy"] = table(
        item("golden_helmet", ench=dict(protection=4, unbreaking=3), title_="تاج الممالك السبع", color="yellow"),
        food("enchanted_golden_apple", 4), food("diamond", 16))
    # ---- shop
    T_["shop/heal"] = table(food("golden_apple", 4), food("cooked_beef", 16))
    T_["shop/arrows"] = table(food("arrow", 48), food("spectral_arrow", 16))
    T_["shop/armor"] = table(*[armor_piece("netherite", p, 4, f"{n} من فولاذ الحرب", "dark_gray") for p, n in PIECES[1:2]])
    T_["shop/sword"] = table(item("diamond_sword", ench=dict(sharpness=5, fire_aspect=1, looting=2, unbreaking=3),
                                  title_="سيف الفارس المحارب", color="aqua"))
    T_["shop/horse"] = table(food("saddle", 1), food("horse_spawn_egg", 1), food("golden_carrot", 16))
    T_["shop/totem"] = table(food("totem_of_undying", 1))
    # ---- armory chests (in every castle)
    T_["armory/swords"] = table(
        item("netherite_sword", ench=SWORD_VS, title_="لونغكلو", color="aqua"),
        item("diamond_sword", ench=dict(sharpness=5, knockback=2, looting=3), title_="الجليد", color="white"),
        item("iron_sword", ench=dict(sharpness=4, unbreaking=3), title_="الإبرة", color="gray"),
        item("stone_sword", ench=dict(sharpness=5, fire_aspect=2), title_="خنجر الزجاج التنيني", color="dark_gray"),
        item("netherite_axe", ench=dict(sharpness=5, efficiency=5), title_="فأس الحديديين", color="dark_red"))
    T_["armory/ranged"] = table(
        item("bow", ench=dict(power=5, punch=2, infinity=1), title_="قوس الشمال الطويل", color="green"),
        item("crossbow", ench=dict(quick_charge=3, multishot=1), title_="نشّابة ثقيلة", color="gold"),
        item("trident", ench=dict(loyalty=3, impaling=5), title_="رمح الكراكن", color="dark_aqua"),
        food("arrow", 64), food("arrow", 64), food("spectral_arrow", 32))
    T_["armory/lannister"] = table(*[armor_piece("golden", p, 4, f"{n} لانستر", "gold") for p, n in PIECES])
    T_["armory/nights_watch"] = table(*[armor_piece("iron", p, 4, f"{n} حرس الليل", "dark_gray", {"thorns": 2}) for p, n in PIECES])
    T_["armory/targaryen"] = table(*[armor_piece("netherite", p, 4, f"{n} تارجاريان", "dark_red") for p, n in PIECES])
    T_["armory/supplies"] = table(
        food("golden_apple", 32), food("enchanted_golden_apple", 4), food("cooked_beef", 64),
        food("totem_of_undying", 3), food("shield", 4), food("torch", 64))
    # ---- world dungeons / secrets
    T_["loot/crypt"] = pick(
        item("iron_sword", ench=dict(sharpness=3), title_="سيف ستارك القديم", color="gray"),
        item("golden_apple", 3, unbreakable=False), item("emerald", 8, unbreakable=False),
        item("diamond", 3, unbreakable=False), item("arrow", 24, unbreakable=False), rolls=3)
    T_["loot/dragonglass"] = table(
        item("stone_sword", ench=dict(sharpness=7, fire_aspect=2, looting=3), title_="خنجر الزجاج التنيني الأصلي", color="dark_purple"),
        item("obsidian", 16, unbreakable=False), item("emerald", 12, unbreakable=False))
    T_["loot/mine"] = pick(
        item("gold_ingot", 12, unbreakable=False), item("emerald", 10, unbreakable=False),
        item("diamond", 4, unbreakable=False), item("golden_apple", 2, unbreakable=False), rolls=3)
    T_["loot/dungeon"] = pick(
        item("emerald", 12, unbreakable=False), item("iron_ingot", 16, unbreakable=False),
        item("diamond", 3, unbreakable=False), item("golden_apple", 3, unbreakable=False),
        item("arrow", 32, unbreakable=False), item("cooked_beef", 12, unbreakable=False), rolls=3)
    T_["loot/nightfort"] = pick(
        item("diamond_sword", ench=dict(sharpness=4), title_="سيف حارس قديم", color="aqua"),
        item("emerald", 15, unbreakable=False), item("golden_apple", 4, unbreakable=False),
        item("enchanted_golden_apple", 1, unbreakable=False), rolls=3)
    T_["loot/tourney"] = table(
        item("emerald", 20, unbreakable=False), item("golden_apple", 6, unbreakable=False),
        item("diamond", 5, unbreakable=False))
    return T_


# ---------------------------------------------------------------- waves / themes (Arabic titles)

Z, SK, HU, ST, VI, WS, RV, PI, EV, WI, CR, SP = ("zombie", "skeleton", "husk", "stray", "vindicator", "wither_skeleton",
                                                 "ravager", "pillager", "evoker", "witch", "creeper", "spider")
THEMES = {
    "wildlings": (1, 0, [
        ("المتوحشون يتسلقون الجدار", [(Z, 6, 2)]),
        ("مغيرون من وراء الجدار", [(Z, 6, 2), (SK, 4, 1)]),
        ("محاربو الثِن", [(HU, 6, 2), (SK, 4, 2), (VI, 2, 1)]),
        ("فرسان الماموث", [(VI, 5, 2), (Z, 8, 2), (RV, 1, 1)]),
    ]),
    "long_night": (2, 2, [
        ("الموجة 1 - الأحياء يتحركون", [(Z, 6, 2)]),
        ("الموجة 2 - مغيرون من وراء الجدار", [(Z, 6, 2), (SK, 4, 1)]),
        ("الموجة 3 - جيش الدوثراكي", [(HU, 6, 2), (SK, 4, 2), (VI, 3, 1)]),
        ("الموجة 4 - الحديديون", [(VI, 6, 2), (Z, 6, 2), (SK, 6, 2)]),
        ("الموجة 5 - السائرون البيض", [(ST, 8, 2), (Z, 8, 2), (WS, 2, 1)]),
        ("الموجة 6 - جيش الموتى", [(Z, 12, 3), (ST, 8, 2), (WS, 4, 1), (RV, 1, 1)]),
        ("الموجة الأخيرة - ملك الليل", [(WS, 4, 1), (ST, 6, 2), (Z, 6, 2)]),
    ]),
    "freys": (3, 1, [
        ("ضيوف العرس الأحمر", [(VI, 5, 2), (Z, 6, 2)]),
        ("رماة آل فراي", [(PI, 5, 2), (VI, 4, 1)]),
        ("تعزيزات التوأمين", [(PI, 5, 2), (VI, 6, 2), (Z, 6, 2)]),
        ("ثأر والدر", [(EV, 2, 1), (VI, 6, 2), (PI, 4, 1)]),
    ]),
    "mountain": (4, 1, [
        ("عشائر الجبال", [(SK, 6, 2), (Z, 6, 2)]),
        ("البوابة الدامية", [(HU, 6, 2), (VI, 4, 1), (SK, 4, 1)]),
        ("رجال الجبل", [(VI, 6, 2), (WS, 3, 1), (RV, 1, 1)]),
    ]),
    "blackwater": (5, 2, [
        ("ستانيس ينزل عند المياه السوداء", [(Z, 8, 2), (VI, 3, 1)]),
        ("سهام النار البرية", [(SK, 6, 2), (CR, 4, 1), (Z, 6, 2)]),
        ("أبراج الحصار", [(VI, 6, 2), (Z, 8, 2), (CR, 4, 1)]),
        ("النار الخضراء", [(CR, 8, 2), (SK, 6, 2), (WS, 2, 1)]),
        ("الجبل يمتطي", [(RV, 2, 1), (VI, 6, 2), (Z, 8, 2)]),
    ]),
    "lannister": (6, 2, [
        ("قطّاع طريق الذهب", [(SK, 6, 2), (Z, 6, 2)]),
        ("جيش المتمردين", [(VI, 6, 2), (SK, 6, 2)]),
        ("أشباح الصخرة", [(WS, 4, 1), (SK, 6, 2), (Z, 6, 2)]),
        ("عرين الأسد", [(WS, 6, 2), (VI, 6, 2), (RV, 1, 1)]),
    ]),
    "reach": (7, 1, [
        ("الثوار يقتحمون الحديقة", [(Z, 8, 2), (SP, 4, 1)]),
        ("الورود المسمومة", [(WI, 3, 1), (SK, 6, 2), (Z, 6, 2)]),
        ("جيش الريتش", [(VI, 6, 2), (Z, 8, 2), (SK, 6, 2)]),
        ("كمين مأدبة تايريل", [(EV, 2, 1), (VI, 6, 2), (PI, 4, 1)]),
    ]),
    "storm": (8, 2, [
        ("العاصفة تتجمع", [(Z, 8, 2), (SK, 4, 2)]),
        ("حصار نهاية العاصفة", [(VI, 6, 2), (Z, 8, 2)]),
        ("طفل الظل", [(WS, 3, 1), (SK, 6, 2), (Z, 6, 2)]),
        ("ستانيس ينهض", [(VI, 6, 2), (WS, 4, 1), (SK, 6, 2)]),
        ("نار الكاهنة الحمراء", [(RV, 2, 1), (CR, 6, 2), (Z, 8, 2)]),
    ]),
    "dorne": (9, 2, [
        ("بنات الرمال يهاجمن", [(HU, 8, 2), (SK, 4, 1)]),
        ("حرس الرمح", [(HU, 6, 2), (VI, 4, 2), (SK, 6, 2)]),
        ("الأفعى الحمراء", [(VI, 6, 2), (WS, 3, 1), (HU, 6, 2)]),
        ("لصوص الصحراء", [(RV, 2, 1), (HU, 10, 3), (SK, 6, 2)]),
    ]),
}
POINTS = [(-27, 56), (-21, 60), (-15, 56), (-9, 60), (-3, 56), (3, 60), (9, 56), (15, 60), (21, 56), (27, 60)]
MAX_EXTRA_PLAYERS = 7


def spawn_cmd(mob, i, tags='"got_enemy","got_new"'):
    x, z = POINTS[i % len(POINTS)]
    return f'summon minecraft:{mob} ~{x} ~ ~{z} {{Tags:[{tags}],PersistenceRequired:1b}}'


def wave_functions():
    F = {}
    for theme, (tid, base, waves) in THEMES.items():
        for n, (ttl, groups) in enumerate(waves, start=1):
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
            inner.append(f"execute if score #fallen {SB} matches 1.. run function {NS}:wave/bonus")
            F[f"wave/{theme}_{n}_spawn"] = inner
            F[f"wave/{theme}_{n}"] = [
                title(ttl, "red"),
                subtitle("الأعداء يتجمعون أمام البوابة الرئيسية!" if not final else "الموجة الأخيرة! احمِ القلعة!", "gray"),
                "playsound minecraft:entity.wither.spawn master @a" if (final and theme == "long_night") else "playsound minecraft:block.bell.use master @a",
                f"execute at @e[tag=got_origin,limit=1] run function {NS}:wave/{theme}_{n}_spawn",
                f"execute as @e[tag=got_new] at @s run function {NS}:game/equip",
            ]
    # extra undead for every castle that has fallen
    bonus = []
    for k in range(1, 9):
        for j in range(3):
            bonus.append(f"execute if score #fallen {SB} matches {k}.. run " + spawn_cmd("zombie", k * 3 + j))
    F["wave/bonus"] = bonus
    return F


TIERS = [((0, 2), "leather", False), ((3, 4), "chainmail", True), ((5, 6), "iron", True), ((7, 99), "diamond", True)]
GEAR_MOBS = ["zombie", "husk", "skeleton", "stray", "vindicator", "pillager"]

# ---------------------------------------------------------------- sites / travel

STORY_ORDER = ["castle_black", "riverrun", "kings_landing", "casterly_rock", "highgarden", "storms_end", "eyrie",
               "sunspear", "winterfell"]
SITE_IDX = {s.key: i for i, s in enumerate(geo.SITES, start=1)}
BATTLE_SITES = {s.key: s for s in geo.SITES}

DESTS = []
for s_ in geo.SITES:
    DESTS.append((ar.SITE_AR[s_.key], "tp", s_.x, s_.y0, s_.z + 32, s_.key))
DESTS += [
    ("قمة الجدار", "tp", 258, 136, 174, None),
    ("ما وراء الجدار (الغابة المسكونة)", "spread", 250, 0, 90, None),
    ("موت كيلين", "spread", 315, 0, 620, None),
    ("التوأمان", "spread", 300, 0, 690, None),
    ("هارينهال", "spread", 340, 0, 830, None),
    ("دراغونستون", "spread", 540, 0, 822, None),
    ("بايك (جزر الحديد)", "spread", 70, 0, 660, None),
    ("أولدتاون - برج هايتاور", "spread", 135, 0, 1200, None),
    ("الميناء الأبيض", "spread", 395, 0, 500, None),
]
DEST_BASE = 2


# ---------------------------------------------------------------- campaign schedule

WARN = 120       # seconds of warning before an attack
SHORT = dict(mode=1, name="حملة قصيرة (30 دقيقة)", attacks=[(300, "castle_black"), (720, "kings_landing"), (1140, "casterly_rock")], final=1680)
LONG = dict(mode=2, name="حملة طويلة (55 دقيقة)", attacks=[(360, "castle_black"), (780, "riverrun"), (1200, "kings_landing"),
                                                          (1620, "casterly_rock"), (2040, "highgarden"), (2460, "storms_end"),
                                                          (2880, "sunspear")], final=3300)
CAMPAIGNS = [SHORT, LONG]

ALLY_POS = [(-6, 22), (-3, 24), (0, 22), (3, 24), (6, 22), (-9, 26), (9, 26), (0, 27)]   # relative to Winterfell centre


def load_npcs():
    p = os.path.join(HERE, "world", "npcs.json")
    if not os.path.exists(p):
        return []
    with open(p) as f:
        return json.load(f)


def game_functions():
    F = {}
    order = ["beyond", "north", "neck", "iron", "riverlands", "vale", "westerlands", "crownlands", "stormlands", "reach", "dorne"]

    # ================================================================ load / tick
    load = [
        f"scoreboard objectives add {SB} dummy {J(T('حرب الممالك', 'gold'))}",
        f"scoreboard objectives add {HUD} dummy {J(T('الليل الطويل', 'aqua', True))}",
    ]
    for trig in ("got_go", "got_battle", "got_kit", "got_house", "got_power", "got_shop", "got_scout", "got_quest",
                 "got_start", "got_accuse"):
        load.append(f"scoreboard objectives add {trig} trigger")
    for dm in ("got_reg", "got_talkcd", "got_gift", "got_gold", "got_renown", "got_pcd", "got_scd", "got_scoutt", "got_id"):
        load.append(f"scoreboard objectives add {dm} dummy")
    load.append("scoreboard objectives add got_deaths deathCount")
    load.append("team add got_enemies")
    load.append("team modify got_enemies color red")
    for key, name, col, *_ in ar.HOUSES:
        load.append(f"team add got_{key} {J(T(name, col))}")
        load.append(f"team modify got_{key} color {col}")
    load += [
        f"execute unless score #state {SB} matches 0.. run scoreboard players set #state {SB} 0",
        f"execute unless score #camp {SB} matches 0.. run scoreboard players set #camp {SB} 0",
        f"scoreboard players set #100 {SB} 100",
        *[f"scoreboard players add {h} {SB} 0" for h in ("#min", "#winter", "#held", "#fallen", "#next_in", "#next_t", "#wave", "#enemies",
                                                       "#camp_battle", "#final", "#mode", "#total_t", "#camp_t", "#idc", "#d", "#d0", "#dd", "#site", "#theme", "#base", "#total", "#gear", "#cool", "#players")],
        f"scoreboard players set #60 {SB} 60",
        f"function {NS}:util/rules",
        "setworldspawn 270 64 378",
        f"function {NS}:hud/names",
        tellc([T("[حرب الممالك] ", "gold", True), T("العالم جاهز. اكتب /trigger got_quest لمعرفة الوضع و /trigger got_house لاختيار بيتك.", "white")], to="@a"),
    ]
    F["load"] = load

    tick = []
    for trig in ("got_go", "got_battle", "got_kit", "got_house", "got_power", "got_shop", "got_scout", "got_quest",
                 "got_start", "got_accuse"):
        tick.append(f"scoreboard players enable @a {trig}")
    tick += [
        f"execute as @a[tag=!got_seen] run function {NS}:player/first_join",
        f"execute as @a[scores={{got_go=1..}}] run function {NS}:travel/handle",
        f"execute as @a[scores={{got_battle=1..}}] run function {NS}:battle/handle",
        f"execute as @a[scores={{got_kit=1..}}] run function {NS}:kit/handle",
        f"execute as @a[scores={{got_house=1..}}] run function {NS}:house/handle",
        f"execute as @a[scores={{got_power=1..}}] run function {NS}:power/handle",
        f"execute as @a[scores={{got_shop=1..}}] run function {NS}:shop/handle",
        f"execute as @a[scores={{got_scout=1..}}] run function {NS}:scout/handle",
        f"execute as @a[scores={{got_quest=1..}}] run function {NS}:quest/handle",
        f"execute as @a[scores={{got_start=1..}}] run function {NS}:camp/handle",
        f"execute as @a[scores={{got_accuse=1..}}] run function {NS}:npc/accuse_handle",
        f"scoreboard players add #t {SB} 1",
        f"execute if score #t {SB} matches 20.. run function {NS}:second",
    ]
    F["tick"] = tick

    # ================================================================ second (1 Hz)
    F["second"] = [
        f"scoreboard players set #t {SB} 0",
        f"execute store result score #players {SB} if entity @a",
        f"execute store result score #enemies {SB} if entity @e[tag=got_enemy]",
        f"execute as @a at @s run function {NS}:region/one",
        "scoreboard players remove @a[scores={got_talkcd=1..}] got_talkcd 1",
        "scoreboard players remove @a[scores={got_gift=1..}] got_gift 1",
        "scoreboard players remove @a[scores={got_pcd=1..}] got_pcd 1",
        "scoreboard players remove @a[scores={got_scd=1..}] got_scd 1",
        "scoreboard players remove @a[scores={got_scoutt=1..}] got_scoutt 1",
        f"execute as @a[tag=got_scouting,scores={{got_scoutt=..0}}] run function {NS}:scout/end",
        f"scoreboard players add #s5 {SB} 1",
        f"execute if score #s5 {SB} matches 5.. run function {NS}:house/passives",
        f"scoreboard players add #s10 {SB} 1",
        f"execute if score #s10 {SB} matches 10.. run function {NS}:cold/tick",
        f"execute if score #camp {SB} matches 1 run function {NS}:camp/second",
        f"execute if score #state {SB} matches 1 run function {NS}:game/running",
        f"execute if score #state {SB} matches 2 run function {NS}:game/intermission",
        f"execute if score #camp {SB} matches 1 run function {NS}:hud/update",
        f"execute if score #camp {SB} matches 0 if score #state {SB} matches 1..2 run function {NS}:hud/update",
        f"function {NS}:rank/check",
    ]

    # ================================================================ HUD
    names = [
        ("hud_time", "الوقت (دقيقة)"), ("hud_winter", "الشتاء ٪"), ("hud_held", "قلاع صامدة"),
        ("hud_fallen", "قلاع سقطت"), ("hud_next", "الهجوم بعد (ث)"), ("hud_wave", "الموجة"), ("hud_enemies", "الأعداء"),
    ]
    F["hud/names"] = [f"scoreboard players set {n} {HUD} 0" for n, _ in names] + \
        [f"scoreboard players display name {n} {HUD} {J(T(a, 'yellow'))}" for n, a in names]
    F["hud/update"] = [
        f"scoreboard players operation hud_time {HUD} = #min {SB}",
        f"scoreboard players operation hud_winter {HUD} = #winter {SB}",
        f"scoreboard players operation hud_held {HUD} = #held {SB}",
        f"scoreboard players operation hud_fallen {HUD} = #fallen {SB}",
        f"scoreboard players operation hud_next {HUD} = #next_in {SB}",
        f"scoreboard players operation hud_wave {HUD} = #wave {SB}",
        f"scoreboard players operation hud_enemies {HUD} = #enemies {SB}",
        f"scoreboard objectives setdisplay sidebar {HUD}",
    ]

    # ================================================================ first join
    F["player/first_join"] = [
        "tag @s add got_seen",
        "tp @s 270.5 64 378.5",
        tell("الشتاء قادم.", "aqua", True),
        tell("أنت في وينترفيل، قلعة آل ستارك. ممالك وستيروس أمامك: الجدار في الشمال والعرش الحديدي في كينغز لاندينغ وصحراء دورن في الجنوب.", "white"),
        tell("خلفَ الجدار يتحرك الموتى، ولن يتوقف الليل الطويل. اجمع الممالك وامنع سقوط القلاع قبل أن يحلّ الظلام.", "yellow"),
        tellc([T("١) اختر بيتك: ", "green", True), T("/trigger got_house", "white")]),
        tellc([T("٢) ابدأ الحملة: ", "green", True), T("/trigger got_start", "white")]),
        tellc([T("٣) للمساعدة والوضع: ", "green", True), T("/trigger got_quest", "white")]),
        f"function {NS}:kit/give",
        f"function {NS}:kit/give_travel",
        "scoreboard players set @s got_gold 20",
    ]

    # ================================================================ houses
    hm = [tell("=== اختر بيتك (اكتب /trigger got_house set الرقم) ===", "gold", True)]
    hh = [f"execute if score @s got_house matches 1 run function {NS}:house/menu"]
    for i, (key, name, col, passive, pname, ptext) in enumerate(ar.HOUSES, start=2):
        hm.append(tellc([T(f"{i} - {name}  ", col, True), T(f"الميزة: {passive}. القدرة ({pname}): {ptext}", "white")]))
        hh.append(f"execute if score @s got_house matches {i} run function {NS}:house/pick_{key}")
        F[f"house/pick_{key}"] = [f"tag @s remove got_h_{k}" for k in ar.HOUSE_KEYS] + [
            f"tag @s add got_h_{key}", "tag @s add got_house_any", f"team join got_{key} @s",
            tellc([T("انضممت إلى ", "green"), T(name, col, True), T(". ", "green"), T(f"ميزتك: {passive}. قدرتك ({pname}) تُستخدم بـ /trigger got_power", "white")]),
            "playsound minecraft:entity.player.levelup master @s",
        ]
    hh.append("scoreboard players set @s got_house 0")
    F["house/menu"] = hm
    F["house/handle"] = hh
    # passives (every 5 s)
    ps = ["scoreboard players set #s5 got_g 0"]
    ps_lines = {
        "stark": [],      # cold immunity handled in cold/tick
        "lannister": [],  # gold bonus handled in battle rewards
        "targaryen": ["effect give @s minecraft:fire_resistance 10 0 true"],
        "martell": ["effect give @s minecraft:speed 10 0 true"],
        "tyrell": ["effect give @s minecraft:saturation 10 0 true", "effect give @s minecraft:regeneration 6 0 true"],
        "baratheon": ["effect give @s minecraft:strength 10 0 true"],
        "greyjoy": ["effect give @s minecraft:water_breathing 10 0 true", "effect give @s minecraft:dolphins_grace 10 0 true"],
        "arryn": ["effect give @s minecraft:slow_falling 10 0 true", "effect give @s minecraft:jump_boost 10 1 true"],
        "tully": ["effect give @s minecraft:luck 20 1 true"],
    }
    for key, lines in ps_lines.items():
        for ln in lines:
            ps.append(f"execute as @a[tag=got_h_{key}] run {ln}")
    F["house/passives"] = ps

    # ================================================================ powers
    ph_use = [
        f"execute if score @s got_pcd matches 1.. run return run {actionbar('القدرة تحتاج وقتًا للتعافي...', 'red', '@s')}",
        f"execute unless entity @s[tag=got_house_any] run return run {tell('اختر بيتًا أولًا: /trigger got_house', 'red')}",
    ]
    for key, name, col, passive, pname, ptext in ar.HOUSES:
        ph_use.append(f"execute if entity @s[tag=got_h_{key}] run function {NS}:power/{key}")
    F["power/handle"] = [f"function {NS}:power/use", "scoreboard players set @s got_power 0"]
    F["power/use"] = ph_use

    def cd(sec):
        return f"scoreboard players set @s got_pcd {sec}"
    P = {}
    P["stark"] = [
        "playsound minecraft:entity.wolf.growl master @a[distance=..40]",
        "particle minecraft:cloud ~ ~1 ~ 1.5 0.6 1.5 0.05 60 force",
        "effect give @a[distance=..20] minecraft:speed 15 1 true", "effect give @a[distance=..20] minecraft:strength 15 0 true",
        actionbar("عوى الذئب!", "white", "@a[distance=..20]"), cd(60)]
    P["lannister"] = [
        f"execute unless score @s got_gold matches 30.. run return run {actionbar('تحتاج 30 ذهبًا', 'red', '@s')}",
        "scoreboard players remove @s got_gold 30",
        "execute at @s run summon minecraft:iron_golem ~2 ~ ~ {Tags:[\"got_ally\"],PlayerCreated:1b,PersistenceRequired:1b}",
        "execute at @s run summon minecraft:iron_golem ~-2 ~ ~ {Tags:[\"got_ally\"],PlayerCreated:1b,PersistenceRequired:1b}",
        "execute at @s run summon minecraft:iron_golem ~ ~ ~2 {Tags:[\"got_ally\"],PlayerCreated:1b,PersistenceRequired:1b}",
        "playsound minecraft:entity.iron_golem.repair master @a[distance=..30]",
        actionbar("الدَّين سُدِّد: 3 حراس!", "gold", "@s"), cd(90)]
    P["targaryen"] = [
        "execute at @s anchored eyes positioned ^ ^ ^5 run particle minecraft:flame ~ ~ ~ 2 1 2 0.08 200 force",
        "execute at @s anchored eyes positioned ^ ^ ^5 as @e[tag=got_enemy,distance=..6] run damage @s 14 minecraft:on_fire by @a[tag=got_me,limit=1]",
        "execute at @s anchored eyes positioned ^ ^ ^5 as @e[tag=got_enemy,distance=..6] run data merge entity @s {Fire:120s}",
        "playsound minecraft:entity.ender_dragon.growl master @a[distance=..40]",
        actionbar("دراكاريس!", "dark_red", "@s"), cd(30)]
    P["martell"] = [
        "execute as @e[tag=got_enemy,distance=..10] run effect give @s minecraft:poison 8 1 true",
        "execute as @e[tag=got_enemy,distance=..10] run effect give @s minecraft:slowness 8 1 true",
        "effect give @s minecraft:speed 12 2 true", "particle minecraft:witch ~ ~1 ~ 1 0.5 1 0.05 40 force",
        "playsound minecraft:entity.spider.ambient master @a[distance=..20]", actionbar("لدغة الأفعى!", "red", "@s"), cd(40)]
    P["tyrell"] = [
        "effect give @a[distance=..15] minecraft:instant_health 1 2 true", "effect give @a[distance=..15] minecraft:regeneration 12 1 true",
        "particle minecraft:heart ~ ~1.5 ~ 2 0.7 2 0.05 25 force",
        "playsound minecraft:entity.player.levelup master @a[distance=..15]", actionbar("ورد الشفاء!", "green", "@a[distance=..15]"), cd(45)]
    P["baratheon"] = [
        "effect give @s minecraft:strength 12 2 true", "effect give @s minecraft:resistance 12 1 true",
        "particle minecraft:angry_villager ~ ~1.5 ~ 0.5 0.5 0.5 0.05 15 force",
        "playsound minecraft:entity.ravager.roar master @a[distance=..30]", actionbar("لنا الغضب!", "yellow", "@s"), cd(45)]
    P["greyjoy"] = [
        "execute as @e[tag=got_enemy,distance=..8] run effect give @s minecraft:levitation 3 3 true",
        "effect give @s minecraft:speed 12 1 true", "particle minecraft:splash ~ ~1 ~ 2 0.5 2 0.1 80 force",
        "playsound minecraft:entity.elder_guardian.curse master @a[distance=..20]", actionbar("المدّ والجزر!", "dark_aqua", "@s"), cd(40)]
    P["arryn"] = [
        "effect give @s minecraft:levitation 2 9 true", "effect give @s minecraft:slow_falling 15 0 true",
        "particle minecraft:cloud ~ ~ ~ 0.5 0.1 0.5 0.1 30 force", "playsound minecraft:entity.phantom.flap master @a[distance=..20]",
        actionbar("قفزة الصقر!", "aqua", "@s"), cd(15)]
    P["tully"] = [
        "effect give @a[distance=..15] minecraft:instant_health 1 1 true", "effect give @a[distance=..15] minecraft:absorption 20 2 true",
        "particle minecraft:falling_water ~ ~2 ~ 3 0.5 3 0.1 60 force", "playsound minecraft:entity.dolphin.splash master @a[distance=..15]",
        actionbar("الفيضان!", "blue", "@a[distance=..15]"), cd(45)]
    for key, lines in P.items():
        # tag the caster so 'by' works
        F[f"power/{key}"] = ["tag @s add got_me"] + lines + ["tag @s remove got_me"]

    # ================================================================ shop
    SHOP = [
        ("علاج وطعام", 5, "shop/heal", "تفاح ذهبي (4) ولحم مطهو (16)"),
        ("سهام", 3, "shop/arrows", "48 سهمًا + 16 سهمًا مضيئًا"),
        ("حصان وسرج", 10, "shop/horse", "حصان للتنقل السريع"),
        ("سيف فارس", 25, "shop/sword", "سيف ألماسي بسحر حاد"),
        ("درع الحرب", 30, "shop/armor", "درع صدر من النذرايت بحماية عالية"),
        ("تميمة الخلود", 40, "shop/totem", "تنقذك من الموت مرة واحدة"),
        ("حرس القلعة", 20, None, "يأتيك حارسان من حديد"),
    ]
    sm = [tell("=== متجر الحرب (اكتب /trigger got_shop set الرقم) ===", "gold", True),
          tellc([T("ذهبك الآن: ", "yellow"), score("@s", "got_gold", "gold")])]
    sh = [f"execute if score @s got_shop matches 1 run function {NS}:shop/menu"]
    for i, (nm, cost, tbl, desc) in enumerate(SHOP, start=2):
        sm.append(tellc([T(f"{i} - {nm} ", "white", True), T(f"({cost} ذهب) ", "gold"), T(desc, "gray")]))
        sh.append(f"execute if score @s got_shop matches {i} run function {NS}:shop/buy_{i}")
        lines = [f"execute unless score @s got_gold matches {cost}.. run return run {actionbar('ذهبك لا يكفي', 'red', '@s')}",
                 f"scoreboard players remove @s got_gold {cost}"]
        if tbl:
            lines.append(f"loot give @s loot {NS}:{tbl}")
        else:
            lines += ['execute at @s run summon minecraft:iron_golem ~2 ~ ~ {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}',
                      'execute at @s run summon minecraft:iron_golem ~-2 ~ ~ {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}']
        lines += [actionbar(f"اشتريت: {nm}", "green", "@s"), "playsound minecraft:entity.villager.trade master @s"]
        F[f"shop/buy_{i}"] = lines
    sh.append("scoreboard players set @s got_shop 0")
    F["shop/menu"] = sm
    F["shop/handle"] = sh

    # ================================================================ scout (raven eye)
    F["scout/handle"] = [
        f"execute if score @s got_scout matches 1.. run function {NS}:scout/start",
        "scoreboard players set @s got_scout 0",
    ]
    F["scout/start"] = [
        f"execute if score @s got_scd matches 1.. run return run {actionbar('الغراب متعب... انتظر قليلًا', 'red', '@s')}",
        f"execute if entity @s[tag=got_scouting] run return 0",
        f"execute unless score @s got_id matches 1.. run function {NS}:util/assign_id",
        "scoreboard players set @s got_scoutt 30", "scoreboard players set @s got_scd 120",
        "tag @s add got_scouting", "tag @s add got_me",
        'execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["got_back","got_new_back"]}',
        "execute as @e[type=minecraft:marker,tag=got_new_back] run scoreboard players operation @s got_id = @a[tag=got_me,limit=1] got_id",
        "tag @e[type=minecraft:marker,tag=got_new_back] remove got_new_back",
        'execute if entity @e[tag=got_origin] at @e[tag=got_origin,limit=1] run summon minecraft:bat ~ ~40 ~ {Tags:["got_eye","got_new_eye"],NoAI:1b,NoGravity:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b}',
        'execute unless entity @e[tag=got_origin] at @s run summon minecraft:bat ~ ~40 ~ {Tags:["got_eye","got_new_eye"],NoAI:1b,NoGravity:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b}',
        "execute as @e[type=minecraft:bat,tag=got_new_eye] run scoreboard players operation @s got_id = @a[tag=got_me,limit=1] got_id",
        "tag @e[type=minecraft:bat,tag=got_new_eye] remove got_new_eye",
        "gamemode spectator @s",
        "spectate @e[type=minecraft:bat,tag=got_eye,sort=nearest,limit=1] @s",
        title("عين الغراب", "dark_gray", True, "@s"), subtitle("ترى ساحة المعركة من الأعلى لمدة 30 ثانية", "gray", "@s"),
        "tag @s remove got_me",
    ]
    F["scout/end"] = [
        "tag @s add got_me", "spectate", "gamemode survival @s",
        "execute as @e[type=minecraft:marker,tag=got_back] if score @s got_id = @a[tag=got_me,limit=1] got_id at @s run tp @a[tag=got_me,limit=1] @s",
        "execute as @e[type=minecraft:marker,tag=got_back] if score @s got_id = @a[tag=got_me,limit=1] got_id run kill @s",
        "execute as @e[type=minecraft:bat,tag=got_eye] if score @s got_id = @a[tag=got_me,limit=1] got_id run kill @s",
        "tag @s remove got_scouting", "tag @s remove got_me",
        actionbar("عاد الغراب.", "gray", "@s"),
    ]
    F["util/assign_id"] = [f"scoreboard players add #idc {SB} 1", f"scoreboard players operation @s got_id = #idc {SB}"]

    # ================================================================ cold (winter bites)
    F["cold/tick"] = [
        f"scoreboard players set #s10 {SB} 0",
        f"execute if score #winter {SB} matches ..19 run return 0",
        f"execute as @a[tag=!got_h_stark,gamemode=!spectator,gamemode=!creative] at @s if biome ~ ~ ~ minecraft:snowy_taiga unless entity @e[type=minecraft:marker,tag=got_warm,distance=..70] unless items entity @s weapon.* minecraft:torch run function {NS}:cold/bite",
        f"execute as @a[tag=!got_h_stark,gamemode=!spectator,gamemode=!creative] at @s if biome ~ ~ ~ minecraft:ice_spikes unless entity @e[type=minecraft:marker,tag=got_warm,distance=..70] unless items entity @s weapon.* minecraft:torch run function {NS}:cold/bite",
    ]
    F["cold/bite"] = ["damage @s 1 minecraft:freeze", actionbar("الصقيع يعضّك! اقترب من نار أو قلعة أو أمسك مشعلًا.", "aqua", "@s")]

    # ================================================================ ranks / status
    ranks = [(20, "فارس"), (50, "لورد"), (100, "يد الملك"), (200, "حامي الممالك")]
    rk = []
    for i, (thr, nm) in enumerate(ranks, start=1):
        rk.append(f"execute as @a[scores={{got_renown={thr}..}},tag=!got_r{i}] run function {NS}:rank/up{i}")
        F[f"rank/up{i}"] = ["tag @s add got_r%d" % i,
                            title(f"رتبة جديدة: {nm}", "gold", True, "@s"), subtitle("ذكرك يرتفع بين الممالك", "yellow", "@s"),
                            "playsound minecraft:ui.toast.challenge_complete master @s"]
    F["rank/check"] = rk
    F["quest/handle"] = [f"function {NS}:quest/status", "scoreboard players set @s got_quest 0"]
    F["quest/status"] = [
        tell("=== حالة الحرب ===", "gold", True),
        f"execute if score #camp {SB} matches 0 run {tell('الحملة لم تبدأ. ابدأها بـ /trigger got_start (حملة قصيرة أو طويلة).', 'yellow')}",
        f"execute if score #camp {SB} matches 1 run tellraw @s {J([T('الوقت: ', 'yellow'), score('#min'), T(' دقيقة | الشتاء: ', 'yellow'), score('#winter'), T('٪', 'yellow')])}",
        f"execute if score #camp {SB} matches 1 run tellraw @s {J([T('قلاع صامدة: ', 'green'), score('#held', SB, 'green'), T(' | قلاع سقطت: ', 'red'), score('#fallen', SB, 'red')])}",
        f"execute if score #camp {SB} matches 1 if score #next_in {SB} matches 1.. run tellraw @s {J([T('الهجوم القادم بعد ', 'red'), score('#next_in', SB, 'red'), T(' ثانية.', 'red')])}",
        tellc([T("ذهبك: ", "gold"), score("@s", "got_gold", "gold"), T("   ذكرك: ", "aqua"), score("@s", "got_renown", "aqua")]),
        tell("الأوامر: /trigger got_go (سفر) - got_house (بيت) - got_power (قدرة) - got_shop (متجر) - got_scout (عين الغراب) - got_kit (عدّة) - got_accuse (اتهام مشبوه).", "gray"),
    ]

    # ================================================================ travel
    handle = [f"execute if score @s got_go matches 1 run function {NS}:travel/menu"]
    menu = [tell("=== السفر (اكتب /trigger got_go set الرقم) ===", "gold", True)]
    story_num = {k: i + 1 for i, k in enumerate(STORY_ORDER)}
    for i, (name, mode, x, y, z, key) in enumerate(DESTS):
        n = DEST_BASE + i
        handle.append(f"execute if score @s got_go matches {n} run function {NS}:travel/d{n}")
        body = [f"tp @s {x} {y} {z}", f"spawnpoint @s {x} {y} {z}"] if mode == "tp" else [f"spreadplayers {x} {z} 0 3 false @s"]
        F[f"travel/d{n}"] = body + [actionbar(f"في الطريق إلى {name}", "yellow", "@s"), "playsound minecraft:entity.enderman.teleport master @s"]
        line = f"{n} - {name}"
        if key:
            menu.append(f"execute if score #cs_{key} {SB} matches 2 run tellraw @s {J(T(line + '  (سقطت!)', 'red'))}")
            menu.append(f"execute if score #cs_{key} {SB} matches 3 run tellraw @s {J([T(line + '  ', 'gray'), T('[صامدة]', 'green')])}")
            menu.append(f"execute unless score #cs_{key} {SB} matches 2..3 run tellraw @s {J(T(line, 'white'))}")
        else:
            menu.append(tell(line, "white"))
    handle.append("scoreboard players set @s got_go 0")
    F["travel/handle"], F["travel/menu"] = handle, menu

    # ================================================================ regions
    F["region/one"] = [f"execute if biome ~ ~ ~ {geo.REGION_BIOME[r]} unless score @s got_reg matches {i} run function {NS}:region/enter_{i}"
                       for i, r in enumerate(order, start=1)] + [f"function {NS}:npc/near"]
    for i, r in enumerate(order, start=1):
        F[f"region/enter_{i}"] = [f"scoreboard players set @s got_reg {i}", "title @s times 10 50 15",
                                  subtitle(ar.REGION_SUB_AR[r], "gray", "@s"), title(ar.REGION_AR[r], "gold", True, "@s")]

    # ================================================================ kit
    F["kit/give"] = [f"loot give @s loot {NS}:kit/weapons", f"loot give @s loot {NS}:kit/supplies",
                     f"loot replace entity @s armor.head loot {NS}:kit/helmet", f"loot replace entity @s armor.chest loot {NS}:kit/chest",
                     f"loot replace entity @s armor.legs loot {NS}:kit/legs", f"loot replace entity @s armor.feet loot {NS}:kit/boots",
                     f"loot replace entity @s weapon.offhand loot {NS}:kit/shield"]
    F["kit/give_travel"] = [f"loot give @s loot {NS}:kit/travel"]
    F["kit/handle"] = [f"execute if score @s got_kit matches 1 run function {NS}:kit/give",
                       f"execute if score @s got_kit matches 2 run function {NS}:kit/give_travel", "scoreboard players set @s got_kit 0"]

    # ================================================================ practice battles (no campaign)
    F["battle/handle"] = [
        f"execute if score @s got_battle matches 2 run function {NS}:game/stop",
        f"execute if score @s got_battle matches 1 run function {NS}:battle/try",
        "scoreboard players set @s got_battle 0"]
    try_lines = [
        f"execute unless score #state {SB} matches 0 unless score #state {SB} matches 4 run return run {tell('معركة جارية الآن! (/trigger got_battle set 2 لإيقافها)', 'red')}",
        f"execute if score #camp {SB} matches 1 run return run {tell('الحملة جارية: المعارك تبدأ تلقائيًا عند هجوم الغراب.', 'red')}",
    ]
    for s in geo.SITES:
        try_lines.append(f"execute positioned {s.x} {s.y0} {s.z} if entity @s[distance=..80] run return run function {NS}:battle/start_{s.key}")
    try_lines.append(tell("قف داخل قلعة كبرى (داخل أسوارها) لتبدأ معركتها التدريبية.", "yellow"))
    F["battle/try"] = try_lines
    for i, s in enumerate(geo.SITES, start=1):
        tid, base, waves = THEMES[s.waves]
        F[f"battle/start_{s.key}"] = [
            "kill @e[tag=got_origin]", f'summon minecraft:marker {s.x} {s.y0} {s.z} {{Tags:["got_origin"]}}',
            f"scoreboard players set #site {SB} {i}", f"scoreboard players set #theme {SB} {tid}",
            f"scoreboard players set #base {SB} {base}", f"scoreboard players set #total {SB} {len(waves)}",
            tellc([T("[معركة] ", "red", True), T(f"{ar.SITE_AR[s.key]}", "white", True)], to="@a"),
            f"function {NS}:battle/begin"]
    F["battle/begin"] = [
        "kill @e[tag=got_enemy]",
        f"scoreboard players set #state {SB} 2", f"scoreboard players set #cool {SB} 12", f"scoreboard players set #wave {SB} 0",
        f"scoreboard players set #t2 {SB} 0",
        f"scoreboard players set #enemies {SB} 0",
        "difficulty normal", f"function {NS}:util/weather_clear", f"function {NS}:util/rules",
        f"scoreboard players set #d {SB} 0",
        f"execute as @a run scoreboard players operation #d {SB} += @s got_deaths",
        f"scoreboard players operation #d0 {SB} = #d {SB}",
        "execute at @e[tag=got_origin,limit=1] as @a[distance=..130] run spawnpoint @s ~ ~ ~4",
        f"execute at @e[tag=got_origin,limit=1] as @a[distance=..130] run function {NS}:battle/prepare",
        title("إلى السلاح!", "dark_red"), subtitle("احمِ القلعة. خذ الأسلحة من المخزن أولًا!", "gray"),
    ]
    F["battle/prepare"] = ["tp @s ~ ~ ~4", f"function {NS}:kit/give"]
    F["game/start"] = [
        f'execute unless entity @e[tag=got_origin] run return run {tell("ابنِ القلعة أولًا: /function got:build", "red")}',
        f"scoreboard players set #site {SB} 2", f"scoreboard players set #theme {SB} 2", f"scoreboard players set #base {SB} 2",
        f"scoreboard players set #total {SB} {len(THEMES['long_night'][2])}", f"function {NS}:battle/begin"]
    F["game/stop"] = [
        "kill @e[tag=got_enemy]", f"scoreboard players set #state {SB} 0",
        f"scoreboard players set #camp_battle {SB} 0",
        "scoreboard objectives setdisplay sidebar", tell("أُوقفت المعركة.", "gray", to="@a")]
    F["game/running"] = [
        f"execute if score #enemies {SB} matches 1..5 run effect give @e[tag=got_enemy] minecraft:glowing 3 0 true",
        f"execute as @e[tag=got_enemy,tag=!got_boss] at @s unless entity @a[distance=..30] run function {NS}:game/march",
        f"execute if score #camp_battle {SB} matches 1 run function {NS}:camp/battle_check",
        f"execute if score #enemies {SB} matches 0 run function {NS}:game/wave_clear"]
    F["game/march"] = ["execute facing entity @p feet positioned ^ ^ ^6 if block ~ ~ ~ air if block ~ ~1 ~ air unless block ~ ~-1 ~ air run tp @s ~ ~ ~"]
    F["game/wave_clear"] = [
        f"execute if score #wave {SB} >= #total {SB} run return run function {NS}:game/victory",
        f"scoreboard players set #state {SB} 2", f"scoreboard players set #cool {SB} 15",
        title("انتهت الموجة!", "green"),
        "effect give @a minecraft:regeneration 10 1 true", "effect give @a minecraft:instant_health 1 2 true",
        f"loot give @a loot {NS}:reward/supplies",
        "scoreboard players add @a got_gold 8", "scoreboard players add @a[tag=got_h_lannister] got_gold 4",
        "scoreboard players add @a got_renown 2",
        "playsound minecraft:entity.player.levelup master @a"]
    F["game/intermission"] = [
        f"scoreboard players remove #cool {SB} 1",
        f"execute if score #cool {SB} matches 1..10 run title @a actionbar {J([T('الموجة القادمة بعد ', 'yellow'), score('#cool', SB, 'gold'), T(' ثانية', 'yellow')])}",
        f"execute if score #cool {SB} matches ..0 run function {NS}:game/next_wave"]
    nw = [f"scoreboard players add #wave {SB} 1", f"scoreboard players set #state {SB} 1",
          f"scoreboard players operation #gear {SB} = #wave {SB}", f"scoreboard players operation #gear {SB} += #base {SB}"]
    for theme, (tid, base, waves) in THEMES.items():
        for n in range(1, len(waves) + 1):
            nw.append(f"execute if score #theme {SB} matches {tid} if score #wave {SB} matches {n} run function {NS}:wave/{theme}_{n}")
    F["game/next_wave"] = nw
    F["game/victory"] = [
        f"scoreboard players set #state {SB} 4",
        title("النصر!", "gold"), subtitle("القلعة صامدة!", "aqua"),
        "effect give @a minecraft:regeneration 30 2 true", "xp add @a 30 levels", f"loot give @a loot {NS}:reward/trophy",
        "scoreboard players add @a got_gold 15", "scoreboard players add @a[tag=got_h_lannister] got_gold 8",
        "scoreboard players add @a got_renown 10",
        "playsound minecraft:ui.toast.challenge_complete master @a",
        f"execute if score #camp_battle {SB} matches 0 run tellraw @a {J(T('انتصرتم! ابدأوا معركة أخرى بـ /trigger got_battle أو ابدأوا الحملة بـ /trigger got_start.', 'gray'))}",
        f"execute if score #camp_battle {SB} matches 1 run function {NS}:camp/battle_won"]
    F["game/equip"] = [f"execute if entity @s[type=minecraft:{m}] run function {NS}:wave/gear" for m in GEAR_MOBS] + ["team join got_enemies @s", "tag @s remove got_new"]
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

    # ================================================================ CAMPAIGN
    ch = [f"execute if score @s got_start matches 1 run function {NS}:camp/menu",
          f"execute if score @s got_start matches 2 run function {NS}:camp/start_short",
          f"execute if score @s got_start matches 3 run function {NS}:camp/start_long",
          f"execute if score @s got_start matches 4 run function {NS}:camp/stop",
          "scoreboard players set @s got_start 0"]
    F["camp/handle"] = ch
    F["camp/menu"] = [
        tell("=== الليل الطويل قادم ===", "aqua", True),
        tell("الجيش الميت يزحف من الشمال ويهاجم القلاع واحدة تلو الأخرى. الغراب يخبركم قبل كل هجوم بدقيقتين.", "white"),
        tell("من يحمي قلعة تبقى صامدة وتمدّه بحلفاء في المعركة الأخيرة. ومن تسقط قلعته تقوى الأعداء.", "white"),
        tell("2 - حملة قصيرة (30 دقيقة، 3 هجمات ثم المعركة الأخيرة في وينترفيل)", "green"),
        tell("3 - حملة طويلة (55 دقيقة، 7 هجمات ثم المعركة الأخيرة)", "green"),
        tell("4 - إيقاف الحملة", "red"),
        tell("اكتب /trigger got_start set الرقم", "yellow"),
    ]
    # start
    common_start = [
        "kill @e[tag=got_enemy]", "kill @e[tag=got_wight]", "kill @e[tag=got_ally]",
        f"scoreboard players set #camp {SB} 1", f"scoreboard players set #camp_t {SB} 0", f"scoreboard players set #min {SB} 0",
        f"scoreboard players set #winter {SB} 0", f"scoreboard players set #held {SB} 0", f"scoreboard players set #fallen {SB} 0",
        f"scoreboard players set #next_in {SB} 0", f"scoreboard players set #next_t {SB} 0", f"scoreboard players set #camp_battle {SB} 0",
        f"scoreboard players set #final {SB} 0", f"scoreboard players set #state {SB} 0", f"scoreboard players set #wave {SB} 0",
    ] + [f"scoreboard players reset #cs_{s.key} {SB}" for s in geo.SITES] + [
        f"function {NS}:util/rules", f"function {NS}:util/weather_clear",
        title("الليل الطويل يقترب", "aqua"), subtitle("اجمعوا الممالك... الشتاء قادم", "gray"),
        "playsound minecraft:ambient.cave master @a", f"function {NS}:hud/update",
        tell("ابدأوا الآن: اختاروا بيوتكم (/trigger got_house) وجهّزوا عدّتكم من متجر الحرب (/trigger got_shop).", "yellow", to="@a"),
    ]
    for c in CAMPAIGNS:
        F[f"camp/start_{'short' if c['mode'] == 1 else 'long'}"] = [
            f"execute if score #camp {SB} matches 1 run return run {tell('الحملة جارية! أوقفوها أولًا (/trigger got_start set 4)', 'red')}",
            f"scoreboard players set #mode {SB} {c['mode']}", f"scoreboard players set #total_t {SB} {c['final']}",
            tellc([T("بدأت ", "green", True), T(c["name"], "green", True)], to="@a")] + common_start
    F["camp/stop"] = [f"scoreboard players set #camp {SB} 0", f"scoreboard players set #camp_battle {SB} 0",
                      "kill @e[tag=got_enemy]", "kill @e[tag=got_wight]", f"scoreboard players set #state {SB} 0",
                      "scoreboard objectives setdisplay sidebar", tell("أُوقفت الحملة.", "gray", to="@a")]
    # per-second campaign clock + events
    sec = [f"scoreboard players add #camp_t {SB} 1",
           f"scoreboard players operation #min {SB} = #camp_t {SB}", f"scoreboard players operation #min {SB} /= #60 {SB}",
           f"scoreboard players operation #winter {SB} = #camp_t {SB}", f"scoreboard players operation #winter {SB} *= #100 {SB}",
           f"scoreboard players operation #winter {SB} /= #total_t {SB}",
           f"execute if score #winter {SB} matches 101.. run scoreboard players set #winter {SB} 100",
           f"execute if score #next_t {SB} > #camp_t {SB} run scoreboard players operation #next_in {SB} = #next_t {SB}",
           f"execute if score #next_t {SB} > #camp_t {SB} run scoreboard players operation #next_in {SB} -= #camp_t {SB}",
           f"execute unless score #next_t {SB} > #camp_t {SB} run scoreboard players set #next_in {SB} 0"]
    for c in CAMPAIGNS:
        m = c["mode"]
        for t, key in c["attacks"]:
            sec.append(f"execute if score #mode {SB} matches {m} if score #camp_t {SB} matches {t - WARN} run function {NS}:camp/warn_{key}")
            sec.append(f"execute if score #mode {SB} matches {m} if score #camp_t {SB} matches {t} run function {NS}:camp/attack_{key}")
        sec.append(f"execute if score #mode {SB} matches {m} if score #camp_t {SB} matches {c['final'] - WARN} run function {NS}:camp/final_warn")
        sec.append(f"execute if score #mode {SB} matches {m} if score #camp_t {SB} matches {c['final']} run function {NS}:camp/final_start")
    F["camp/second"] = sec
    used = sorted({k for c in CAMPAIGNS for _, k in c["attacks"]})
    for key in used:
        s = BATTLE_SITES[key]
        i = SITE_IDX[key]
        nm = ar.SITE_AR[key]
        F[f"camp/warn_{key}"] = [
            f"scoreboard players set #next_site {SB} {i}",
            f"scoreboard players operation #next_t {SB} = #camp_t {SB}", f"scoreboard players add #next_t {SB} {WARN}",
            title("غراب عاجل!", "dark_gray"), subtitle(f"{nm} ستُهاجَم بعد دقيقتين", "red"),
            tellc([T("[الغراب] ", "dark_gray", True), T(f"الجيش الميت يقترب من {nm}! اذهبوا إليها بـ /trigger got_go واحموها.", "red", True)], to="@a"),
            "playsound minecraft:entity.parrot.ambient master @a",
        ]
        F[f"camp/attack_{key}"] = [
            f"execute unless score #state {SB} matches 0 unless score #state {SB} matches 4 run return run function {NS}:camp/fell_{key}",
            f"execute positioned {s.x} {s.y0} {s.z} if entity @a[distance=..130] run return run function {NS}:camp/defend_{key}",
            f"function {NS}:camp/fell_{key}"]
        F[f"camp/defend_{key}"] = [
            f"scoreboard players set #camp_battle {SB} 1", tellc([T("[الغراب] ", "dark_gray", True), T(f"بدأ الهجوم على {nm}! قاتلوا!", "red", True)], to="@a"),
            f"function {NS}:battle/start_{key}"]
    # generic per-site handlers (site index dispatch)
    for key in [s.key for s in geo.SITES]:
        nm = ar.SITE_AR[key]
        i = SITE_IDX[key]
        F[f"camp/fell_{key}"] = [
            f"execute if score #cs_{key} {SB} matches 3 run scoreboard players remove #held {SB} 1",
            f"execute unless score #cs_{key} {SB} matches 2 run scoreboard players add #fallen {SB} 1",
            f"scoreboard players set #cs_{key} {SB} 2", f"scoreboard players reset #wt_{key} {SB}",
            title("سقطت قلعة!", "dark_red"), subtitle(f"{nm} في يد الموتى", "red"),
            tellc([T("[الغراب] ", "dark_gray", True), T(f"سقطت {nm}! الأعداء أقوى الآن. يمكنكم استردادها بمعركة (/trigger got_battle) داخلها.", "red", True)], to="@a"),
            "playsound minecraft:entity.wither.death master @a",
            f"execute if score #cs_winterfell {SB} matches 2 run function {NS}:camp/lose",
        ]
    for s2 in geo.SITES:
        F[f"camp/wights_{s2.key}"] = [f"scoreboard players set #wt_{s2.key} {SB} 1"] + [
            f'summon minecraft:zombie {s2.x + dx} {s2.y0} {s2.z + dz} {{Tags:["got_wight"],PersistenceRequired:1b}}'
            for dx, dz in ((-6, 30), (6, 30), (-12, 34), (12, 34), (0, 26), (-18, 28), (18, 28), (-4, 36))]
    F["camp/battle_check"] = [
        f"scoreboard players set #d {SB} 0", f"execute as @a run scoreboard players operation #d {SB} += @s got_deaths",
        f"scoreboard players operation #dd {SB} = #d {SB}", f"scoreboard players operation #dd {SB} -= #d0 {SB}",
        f"execute if score #dd {SB} matches 7.. run function {NS}:camp/battle_lost"]
    F["camp/battle_lost"] = [
        "kill @e[tag=got_enemy]", f"scoreboard players set #state {SB} 0", f"scoreboard players set #camp_battle {SB} 0",
        title("فشلتم في الدفاع!", "dark_red"), subtitle("الأعداء اجتاحوا القلعة", "red")] + \
        [f"execute if score #site {SB} matches {SITE_IDX[s.key]} run function {NS}:camp/fell_{s.key}" for s in geo.SITES]
    won = [f"scoreboard players set #camp_battle {SB} 0", "kill @e[tag=got_wight,distance=..120]"]
    for s in geo.SITES:
        i = SITE_IDX[s.key]
        won.append(f"execute if score #site {SB} matches {i} run function {NS}:camp/held_{s.key}")
        F[f"camp/held_{s.key}"] = [
            f"execute if score #cs_{s.key} {SB} matches 2 run scoreboard players remove #fallen {SB} 1",
            f"execute unless score #cs_{s.key} {SB} matches 3 run scoreboard players add #held {SB} 1",
            f"scoreboard players reset #wt_{s.key} {SB}",
            f"scoreboard players set #cs_{s.key} {SB} 3",
            tellc([T("[الغراب] ", "dark_gray", True), T(f"{ar.SITE_AR[s.key]} صامدة! ستمدّكم بحلفاء في المعركة الأخيرة.", "green", True)], to="@a")]
    won.append(f"execute if score #final {SB} matches 1 run function {NS}:camp/win")
    F["camp/battle_won"] = won
    # final battle
    F["camp/final_warn"] = [title("الليل الطويل يبدأ!", "aqua"), subtitle("المعركة الأخيرة في وينترفيل بعد دقيقتين", "red"),
                            tellc([T("[الغراب] ", "dark_gray", True), T("ملك الليل قادم! اجتمعوا في وينترفيل (/trigger got_go set 3)!", "red", True)], to="@a"),
                            f"scoreboard players set #next_site {SB} 2", f"scoreboard players operation #next_t {SB} = #camp_t {SB}",
                            f"scoreboard players add #next_t {SB} {WARN}"]
    fs = [f"scoreboard players set #final {SB} 1", f"scoreboard players set #winter {SB} 100",
          f"function {NS}:util/weather_thunder",
          "tp @a 270 64 385",
          f"execute unless score #state {SB} matches 0 unless score #state {SB} matches 4 run function {NS}:game/stop",
          f"schedule function {NS}:camp/final_go 60t"]
    F["camp/final_start"] = fs
    fs = []
    for idx, s in enumerate(geo.SITES):
        if s.key == "winterfell":
            continue
        for k in range(2):
            ax, az = ALLY_POS[(idx * 2 + k) % len(ALLY_POS)]
            fs.append(f"execute if score #cs_{s.key} {SB} matches 3 run summon minecraft:iron_golem {270 + ax} 64 {350 + az} "
                      f"{{Tags:[\"got_ally\"],PlayerCreated:1b,PersistenceRequired:1b}}")
    fs += [f"scoreboard players set #camp_battle {SB} 1", f"function {NS}:battle/start_winterfell",
           title("ملك الليل قادم!", "dark_red"), subtitle("هذه هي المعركة الأخيرة", "gray"),
           tellc([T("حلفاؤكم: ", "green", True), score("#held", SB, "green"), T(" قلعة صامدة | أعداؤكم زادوا بسبب ", "gray"), score("#fallen", SB, "red"), T(" قلعة ساقطة", "red")], to="@a")]
    F["camp/final_go"] = fs
    F["camp/win"] = [
        f"scoreboard players set #camp {SB} 0", f"function {NS}:util/weather_clear",
        title("انتصرت الممالك!", "gold"), subtitle("ملك الليل هُزم وانتهى الشتاء", "aqua"),
        tellc([T("انتهت الحملة بنصر عظيم! قلاع صامدة: ", "gold", True), score("#held", SB, "green"), T("  قلاع سقطت: ", "gray"), score("#fallen", SB, "red")], to="@a"),
        "xp add @a 100 levels", "scoreboard players add @a got_renown 50", "scoreboard players add @a got_gold 100",
        "playsound minecraft:ui.toast.challenge_complete master @a", "scoreboard objectives setdisplay sidebar"]
    F["camp/lose"] = [
        f"scoreboard players set #camp {SB} 0", f"scoreboard players set #camp_battle {SB} 0", "kill @e[tag=got_enemy]",
        f"scoreboard players set #state {SB} 0", f"function {NS}:util/weather_thunder",
        title("انتصر الشتاء", "dark_red"), subtitle("سقطت وينترفيل... لكن يمكنكم المحاولة من جديد", "gray"),
        "playsound minecraft:entity.wither.death master @a", "scoreboard objectives setdisplay sidebar"]

    # ================================================================ NPCs
    npcs = load_npcs()
    near = []
    reset = ["kill @e[tag=got_npc]", "kill @e[type=minecraft:marker,tag=got_warm]"]
    for g in npcs:
        gid, house = g["id"], g["house"]
        cx, cy, cz = g["center"]
        sp = [f"scoreboard players set #npc_{gid} {SB} 1", f'summon minecraft:marker {cx} {cy} {cz} {{Tags:["got_warm"]}}']
        for (x, y, z, yaw) in g["spots"]:
            sp.append(f'summon minecraft:villager {x}.5 {y} {z}.5 {{Tags:["got_npc","got_h_{house}","got_grp_{gid}"],'
                      f'VillagerData:{{type:"minecraft:{g["type"]}",profession:"minecraft:none",level:1}},'
                      f'PersistenceRequired:1b,Invulnerable:1b,Rotation:[{yaw}.0f,0.0f]}}')
        sp.append(f"execute as @e[type=minecraft:villager,tag=got_grp_{gid},sort=random,limit=1] run tag @s add got_impostor")
        F[f"npc/spawn_{gid}"] = sp
        near.append(f"execute positioned {cx} {cy} {cz} if entity @s[distance=..70] unless score #npc_{gid} {SB} matches 1 unless score #cs_{gid} {SB} matches 2 run function {NS}:npc/spawn_{gid}")
        if gid in SITE_IDX:
            near.append(f"execute positioned {cx} {cy} {cz} if entity @s[distance=..70] if score #cs_{gid} {SB} matches 2 run kill @e[tag=got_grp_{gid},distance=..90]")
        reset.append(f"scoreboard players reset #npc_{gid} {SB}")
    for s3 in geo.SITES:
        near.append(f"execute positioned {s3.x} {s3.y0} {s3.z} if entity @s[distance=..70] if score #cs_{s3.key} {SB} matches 2 unless score #wt_{s3.key} {SB} matches 1 run function {NS}:camp/wights_{s3.key}")
    F["npc/near"] = near or ["# no npcs"]
    F["npc/reset"] = reset
    F["npc/talk"] = [
        "advancement revoke @s only got:npc_talk", f"execute if score @s got_talkcd matches 1.. run return 0",
        "scoreboard players set @s got_talkcd 30",
        f"execute as @e[type=minecraft:villager,tag=got_npc,sort=nearest,limit=1,distance=..8] at @s run function {NS}:npc/speak",
        f"execute unless score @s got_gift matches 1.. run function {NS}:npc/maybe_gift"]
    F["npc/maybe_gift"] = [f"execute store result score #g {SB} run random value 1..4",
                           f"execute if score #g {SB} matches 1 run function {NS}:npc/gift"]
    F["npc/gift"] = ["scoreboard players set @s got_gift 2400", f"loot give @s loot {NS}:reward/supplies", "scoreboard players add @s got_gold 3",
                    tell("ضغط القروي في يدك مؤونة وثلاث قطع من الذهب.", "green"), "playsound minecraft:entity.villager.celebrate master @s"]
    speak = [f"execute if entity @s[tag=got_impostor] run return run function {NS}:npc/say_impostor"]
    for h, lines in ar.DIALOGUE.items():
        speak.append(f"execute if entity @s[tag=got_h_{h}] run function {NS}:npc/say_{h}")
        L = [f"execute store result score #r {SB} run random value 1..{len(lines) + 1}"]
        for i, line in enumerate(lines, start=1):
            L.append(f"execute if score #r {SB} matches {i} run tellraw @a[distance=..10] {J([T('<' + ar.SPEAKER_AR[h] + '> ', 'aqua'), T(line, 'white')])}")
        dyn = [T('<' + ar.SPEAKER_AR[h] + '> ', 'aqua'), T("الشتاء وصل ", "white"), score("#winter", SB, "aqua"), T("٪. القلاع الصامدة ", "white"), score("#held", SB, "green"), T("، والساقطة ", "white"), score("#fallen", SB, "red"), T(".", "white")]
        L.append(f"execute if score #r {SB} matches {len(lines) + 1} run tellraw @a[distance=..10] {J(dyn)}")
        L.append("playsound minecraft:entity.villager.ambient master @a[distance=..10]")
        F[f"npc/say_{h}"] = L
    F["npc/speak"] = speak
    imp = [f"execute store result score #r {SB} run random value 1..{len(ar.IMPOSTOR_LINES)}"]
    for i, line in enumerate(ar.IMPOSTOR_LINES, start=1):
        imp.append(f"execute if score #r {SB} matches {i} run tellraw @a[distance=..10] {J([T('<مجهول> ', 'dark_gray'), T(line, 'white')])}")
    imp.append("playsound minecraft:entity.villager.no master @a[distance=..10]")
    F["npc/say_impostor"] = imp
    F["npc/accuse_handle"] = [
        f"execute as @e[type=minecraft:villager,tag=got_npc,sort=nearest,limit=1,distance=..5] at @s run function {NS}:npc/accused",
        "scoreboard players set @s got_accuse 0"]
    F["npc/accused"] = [f"execute if entity @s[tag=got_impostor] run function {NS}:npc/reveal",
                        f"execute unless entity @s[tag=got_impostor] run function {NS}:npc/innocent"]
    F["npc/innocent"] = [
        tellc([T("<القروي> ", "aqua"), T("أنا؟ أنا مواطن شريف! كيف تتهمني؟", "white")], to="@a[distance=..8]"),
        "scoreboard players remove @p[distance=..8] got_gold 2", "playsound minecraft:entity.villager.no master @a[distance=..8]"]
    F["npc/reveal"] = [
        title("كُشف الوجه الخفي!", "dark_red", True, "@a[distance=..12]"),
        tellc([T("<القاتل> ", "dark_gray", True), T("...كيف عرفتَ؟! لن تنجو!", "red")], to="@a[distance=..12]"),
        'summon minecraft:vindicator ~ ~ ~ {Tags:["got_assassin","got_assassin_new"],PersistenceRequired:1b}',
        "execute as @e[tag=got_assassin_new] run item replace entity @s armor.head with minecraft:iron_helmet",
        "execute as @e[tag=got_assassin_new] run item replace entity @s armor.chest with minecraft:iron_chestplate",
        "tag @e[tag=got_assassin_new] remove got_assassin_new",
        "scoreboard players add @p[distance=..8] got_gold 15", "scoreboard players add @p[distance=..8] got_renown 5",
        "playsound minecraft:entity.evoker.prepare_summon master @a[distance=..20]", "kill @s"]

    # ================================================================ util
    rules = [("mobGriefing", "mob_griefing", "false"), ("keepInventory", "keep_inventory", "true"),
             ("doMobSpawning", "spawn_mobs", "false"), ("doDaylightCycle", "advance_time", "true")]
    calls = []
    for old, new, val in rules:
        for tag, nm in (("old", old), ("new", new)):
            fn = f"util/rule_{old.lower()}_{tag}"
            F[fn] = [f"$gamerule {nm} $(v)"]
            calls.append(f'function {NS}:{fn} {{v:"{val}"}}')
    F["util/rules"] = calls
    F["util/weather_clear"] = [f'function {NS}:util/weather {{v:"clear"}}']
    F["util/weather_thunder"] = [f'function {NS}:util/weather {{v:"thunder"}}']
    F["util/weather"] = ["$weather $(v)"]
    # help
    F["help"] = F["quest/status"]
    # legacy build helpers
    F["build"] = [
        "kill @e[tag=got_origin]", "kill @e[tag=got_gate]", "kill @e[tag=got_center]",
        'execute align xyz run summon minecraft:marker ~ ~ ~ {Tags:["got_origin"]}',
        tell("جارٍ بناء القلعة... ابقَ قرب المنتصف نحو 20 ثانية.", "yellow", to="@a"),
        "execute at @e[tag=got_origin,limit=1] run forceload add ~-60 ~-60 ~60 ~60",
        f"schedule function {NS}:build/s1_ground 40t"]
    F["tp/hall"] = ["execute at @e[tag=got_origin,limit=1] run tp @a ~ ~ ~4"]
    F["tp/gate"] = ["execute at @e[tag=got_origin,limit=1] run tp @a ~ ~ ~38"]
    F["tp/roof"] = ["execute at @e[tag=got_origin,limit=1] run tp @a ~ ~21 ~-6"]
    return F


# ---------------------------------------------------------------- build stage glue (optional /function got:build)

CHEST_LOOT = [("swords", -36), ("ranged", -34), ("lannister", -32), ("nights_watch", -30), ("targaryen", -28), ("supplies", -26)]


def stage_wrap(name, next_name, delay, extra_after=()):
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
        tellc([T("القلعة جاهزة! ", "green", True), T("الأسلحة في مخزن الأسلحة (الفناء الغربي). للبدء: /function got:game/start", "white")], to="@a")]


ADVANCEMENT_NPC_TALK = {
    "criteria": {"talk": {
        "trigger": "minecraft:player_interacted_with_entity",
        "conditions": {"entity": [{
            "condition": "minecraft:entity_properties", "entity": "this",
            "predicate": {"nbt": "{Tags:[\"got_npc\"]}"}}]}}},
    "rewards": {"function": "got:npc/talk"},
}
